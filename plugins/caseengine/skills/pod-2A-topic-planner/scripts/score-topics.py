#!/usr/bin/env python3
"""
Podcast Topic Scoring Engine - pod-2A-topic-planner

Primary scoring engine. Ranks candidate podcast episode topics off a 10-signal,
3-bucket weighted model plus a corroboration mechanic.

The model is defined entirely in references/scoring-model.json. This script
LOADS that file at runtime - signal names, per-signal weights, buckets, and the
corroboration spec all come from the JSON. Tune the model by editing the JSON;
no code change is needed for a weight change to move the ranking.

Mahalanobis covariance-corrected scoring (the old primary model) is preserved
here as an OPTIONAL diagnostic appendix, gated behind --mahalanobis. It is no
longer the primary ranking.

Usage:
  python3 score-topics.py <input.json> [--out <output_dir>] [--mahalanobis]

input.json shape:
  {
    "metadata": {"practice_area": "...", "client": "...", "topic_weighting": "..."},
    "topics": [
      {
        "id": 1, "title": "...", "theme": "...",
        "entity_ids": [...], "primary_cluster": 2, "bridge_clusters": [1,3],
        "intent_stage": "...",
        "has_tier1_or_tier2_entity": true,
        "is_paa_question": true,
        "signals": {
          "entity_density": 0.0, "prominence": 0.0, "relatedness": 0.0,
          "bridge_value": 0.0, "search_volume": 0, "paa_depth": 0,
          "related_search_density": 0, "virality": 0.0,
          "gap_opportunity": 0.0, "popularity": 0.0
        }
      }
    ]
  }

Signal values are RAW: search_volume is an MSV integer, paa_depth and
related_search_density are counts, the rest are 0-1. `virality` is optional
and may be absent or null on every topic.

Outputs to <output_dir> (default: alongside the input file):
  - topics-ranked.json  - per-topic normalized signals, authority_score,
                          corroboration {families_fired, flag}, raw_rank, final_rank
  - topics-ranked.md    - final ranked table, then a "Topic Ideas" section
                          preserving the original raw-score ranking
With --mahalanobis: a collapsed Mahalanobis diagnostic appendix is appended to
the .md and visuals are written to <output_dir>/visuals/.
"""

import argparse
import json
import os
import sys
from datetime import date


# ---------------------------------------------------------------------------
# Model loading - scoring-model.json is the single source of truth
# ---------------------------------------------------------------------------

def find_scoring_model():
    """Locate references/scoring-model.json relative to this script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    path = os.path.join(skill_root, 'references', 'scoring-model.json')
    if not os.path.exists(path):
        print(f"ERROR: scoring model not found at {path}", file=sys.stderr)
        sys.exit(1)
    return path


def load_model(path):
    """Load and lightly validate the scoring model JSON."""
    with open(path, 'r') as f:
        model = json.load(f)
    for key in ('signals', 'buckets', 'corroboration', '_meta'):
        if key not in model:
            print(f"ERROR: scoring model missing '{key}' block", file=sys.stderr)
            sys.exit(1)
    return model


# ---------------------------------------------------------------------------
# Weight resolution - active signal set + optional-signal redistribution
# ---------------------------------------------------------------------------

def resolve_weights(model, topics):
    """
    Decide which signals are active and what their weights are.

    An optional signal (per its `optional` flag in the JSON) is dropped from
    the active set when NO topic carries a non-null value for it. Its weight is
    then redistributed proportionally across all remaining present signals so
    the active weights still sum to 1.00 - per
    _meta.invariants.optional_signal_handling.

    Returns (active_signals, weights_by_name, dropped_signal_names).
    """
    all_signals = model['signals']
    dropped = []
    active = []

    for sig in all_signals:
        name = sig['name']
        if sig.get('optional', False):
            # Active only if at least one topic carries a real value.
            present = any(
                t.get('signals', {}).get(name) is not None
                for t in topics
            )
            if not present:
                dropped.append(name)
                continue
        active.append(sig)

    base_weights = {s['name']: float(s['weight']) for s in active}

    if dropped:
        # Redistribute the freed weight proportionally across present signals.
        freed = sum(
            float(s['weight']) for s in all_signals if s['name'] in dropped
        )
        present_total = sum(base_weights.values())
        if present_total <= 0:
            print("ERROR: no present signals to redistribute weight onto",
                  file=sys.stderr)
            sys.exit(1)
        for name in base_weights:
            share = base_weights[name] / present_total
            base_weights[name] += freed * share

    # Validate the invariant - active weights must sum to 1.0.
    tolerance = float(model['_meta']['invariants'].get('tolerance', 0.001))
    target = float(model['_meta']['invariants'].get('weights_sum_to', 1.0))
    total = sum(base_weights.values())
    if abs(total - target) > tolerance:
        print(
            f"ERROR: active weights sum to {total:.6f}, expected "
            f"{target} +/- {tolerance}. Refusing to score with a broken model.",
            file=sys.stderr,
        )
        sys.exit(1)

    return active, base_weights, dropped


# ---------------------------------------------------------------------------
# Normalization - min-max within the topic set, per signal
# ---------------------------------------------------------------------------

def normalize_column(raw_values):
    """
    Min-max normalize a list of raw values to 0-1 within the topic set.

    Zero-variance column (every topic equal): a present-but-flat signal is
    treated as neutral 0.5 if the shared value is positive, 0.0 if it is zero -
    a column that is zero everywhere contributes nothing, while a column that
    is uniformly high carries no discriminating information so it sits neutral.
    """
    lo = min(raw_values)
    hi = max(raw_values)
    if hi == lo:
        return [0.5 if hi > 0 else 0.0 for _ in raw_values]
    span = hi - lo
    return [(v - lo) / span for v in raw_values]


def build_normalized_signals(active_signals, topics):
    """
    Return {topic_index: {signal_name: normalized_value}}.

    Raw values are pulled from each topic's `signals` block. A missing or null
    raw value defaults to 0.0 (the keyword-research fallback / absent-signal
    behavior described in the model's per-signal `absent_when`).
    """
    norm = {i: {} for i in range(len(topics))}
    for sig in active_signals:
        name = sig['name']
        raw = []
        for t in topics:
            v = t.get('signals', {}).get(name)
            raw.append(float(v) if v is not None else 0.0)
        normalized = normalize_column(raw)
        for i, nv in enumerate(normalized):
            norm[i][name] = nv
    return norm


# ---------------------------------------------------------------------------
# Authority score - weighted sum of normalized signals
# ---------------------------------------------------------------------------

def compute_authority_scores(active_signals, weights, norm):
    """authority_score = sum(normalized_signal * weight). Result is 0-1."""
    scores = {}
    for i, sig_vals in norm.items():
        s = 0.0
        for sig in active_signals:
            name = sig['name']
            s += sig_vals.get(name, 0.0) * weights[name]
        # Clamp - weights sum to 1.0 and inputs are 0-1, so this is a guard.
        scores[i] = max(0.0, min(1.0, s))
    return scores


# ---------------------------------------------------------------------------
# Corroboration - breadth-of-evidence flag
# ---------------------------------------------------------------------------

def _percentile_threshold(values, top_fraction):
    """
    Return the cutoff value such that a topic is "in the top `top_fraction`"
    when its value is >= the cutoff.

    Example: top 60% -> cutoff is the 40th-percentile value (40% of the set
    sits below it, 60% at or above).
    """
    if not values:
        return 0.0
    ordered = sorted(values)
    n = len(ordered)
    # Index of the lowest-ranked value still inside the top fraction.
    idx = int((1.0 - top_fraction) * n)
    idx = max(0, min(idx, n - 1))
    return ordered[idx]


def compute_corroboration(model, topics, norm, virality_active):
    """
    Apply the corroboration mechanic from the model JSON.

    Returns {topic_index: {"families_fired": [...], "flag": "..."}}.

    Evidence families (from corroboration.evidence_families):
      - entity:        has_tier1_or_tier2_entity AND normalized entity_density
                       in the top 60% of the set.
      - search-demand: is_paa_question AND normalized related_search_density
                       in the top 60% of the set.
      - trend:         virality present AND normalized virality in the top 40%.

    Flag levels (from corroboration.levels):
      - corroborated+trending: entity + search-demand + trend
      - corroborated:          entity + search-demand
      - single-family:         exactly one family fires
      - uncorroborated:        zero families fire
    """
    n = len(topics)

    # Top-percentage cutoffs are computed once over the whole normalized set.
    ed_values = [norm[i].get('entity_density', 0.0) for i in range(n)]
    rsd_values = [norm[i].get('related_search_density', 0.0) for i in range(n)]
    ed_cutoff = _percentile_threshold(ed_values, 0.60)
    rsd_cutoff = _percentile_threshold(rsd_values, 0.60)

    vir_cutoff = None
    if virality_active:
        vir_values = [norm[i].get('virality', 0.0) for i in range(n)]
        vir_cutoff = _percentile_threshold(vir_values, 0.40)

    result = {}
    for i, t in enumerate(topics):
        fired = []

        # Entity family.
        if t.get('has_tier1_or_tier2_entity', False) and \
                norm[i].get('entity_density', 0.0) >= ed_cutoff:
            fired.append('entity')

        # Search-demand family.
        if t.get('is_paa_question', False) and \
                norm[i].get('related_search_density', 0.0) >= rsd_cutoff:
            fired.append('search-demand')

        # Trend family (optional - only when virality research ran).
        if virality_active and norm[i].get('virality', 0.0) >= vir_cutoff:
            fired.append('trend')

        result[i] = {'families_fired': fired, 'flag': _flag_for(fired)}

    return result


def _flag_for(fired):
    """Map the set of fired families to a corroboration flag."""
    has_entity = 'entity' in fired
    has_demand = 'search-demand' in fired
    has_trend = 'trend' in fired
    if has_entity and has_demand and has_trend:
        return 'corroborated+trending'
    if has_entity and has_demand:
        return 'corroborated'
    if len(fired) == 1:
        return 'single-family'
    return 'uncorroborated'


CORROBORATED_FLAGS = {'corroborated', 'corroborated+trending'}


# ---------------------------------------------------------------------------
# Ranking - raw rank, then corroboration ranking floor
# ---------------------------------------------------------------------------

def raw_rank(scores):
    """
    Rank topics by authority_score descending. Returns {topic_index: rank}.
    Stable on ties via topic index (lower index wins).
    """
    order = sorted(scores.keys(), key=lambda i: (-scores[i], i))
    return {idx: rank for rank, idx in enumerate(order, 1)}


def apply_corroboration_floor(model, scores, corroboration, raw_ranks):
    """
    Enforce the corroboration ranking floor (corroboration.ranking_floor) as a
    BOUNDED LOCAL PROMOTION - not a global two-tier re-sort.

    A 'corroborated' / 'corroborated+trending' topic may rise above a
    non-corroborated topic ranked directly above it, but ONLY when the score
    gap is within `ranking_floor.score_margin`. Corroboration protects a topic
    across a near-tie - it never lets a clearly lower-scoring topic leapfrog a
    clearly higher one. The numeric score is unchanged; only rank order shifts,
    and only within the margin.

    (The previous implementation sorted on a corroborated/uncorroborated tier
    ahead of score, which globally floated every corroborated topic above every
    non-corroborated one regardless of score - a 0.20 topic outranking a 0.59
    topic. This bounded version fixes that.)

    Returns {topic_index: final_rank}.
    """
    floor = model['corroboration'].get('ranking_floor', {})
    if not floor.get('enabled', False):
        return dict(raw_ranks)
    margin = float(floor.get('score_margin', 0.05))

    # Start in raw-score order.
    order = sorted(scores.keys(), key=lambda i: raw_ranks[i])

    def corroborated(i):
        return corroboration[i]['flag'] in CORROBORATED_FLAGS

    # Bubble each corroborated topic up past the non-corroborated topics
    # directly above it, while the score gap stays within the margin.
    changed = True
    while changed:
        changed = False
        for pos in range(1, len(order)):
            cur, above = order[pos], order[pos - 1]
            if corroborated(cur) and not corroborated(above) and \
                    (scores[above] - scores[cur]) <= margin:
                order[pos - 1], order[pos] = cur, above
                changed = True

    return {idx: rank for rank, idx in enumerate(order, 1)}


# ---------------------------------------------------------------------------
# Rationale - plain-language "why this rank" string
# ---------------------------------------------------------------------------

def build_rationale(topic, norm_vals, corro, active_signals):
    """
    Generate a client-readable rationale per the model's rationale.rules.
    Leads with corroboration when present, names the actual top signals,
    capped at 200 chars, no jargon, no em dashes.
    """
    # Top-contributing signals by normalized value.
    ranked_sigs = sorted(
        ((s['name'], norm_vals.get(s['name'], 0.0)) for s in active_signals),
        key=lambda kv: -kv[1],
    )
    top = [name for name, val in ranked_sigs[:2] if val > 0]
    pretty = {
        'entity_density': 'entity coverage',
        'prominence': 'core-entity prominence',
        'relatedness': 'entity relatedness',
        'bridge_value': 'cluster-bridging value',
        'search_volume': 'search volume',
        'paa_depth': 'People Also Ask depth',
        'related_search_density': 'a rich related-search cluster',
        'virality': 'trend momentum',
        'gap_opportunity': 'an open competitive lane',
        'popularity': 'competitor validation',
    }
    drivers = ', '.join(pretty.get(n, n) for n in top) or 'modest signals'

    flag = corro['flag']
    if flag in CORROBORATED_FLAGS:
        text = f"High-confidence. Independent sources agree: strong {drivers}."
        if flag == 'corroborated+trending':
            text = text.rstrip('.') + ', and it is trending now.'
    elif flag == 'single-family':
        text = f"Driven mainly by {drivers}. Verify it is not a one-signal spike before locking."
    else:
        text = f"Thin across the board, best {drivers}. Reserve or cut candidate."

    return text[:200]


# ---------------------------------------------------------------------------
# Output - topics-ranked.json
# ---------------------------------------------------------------------------

def write_json_output(path, model_path, metadata, topics, norm, scores,
                      corroboration, raw_ranks, final_ranks, weights,
                      dropped, active_signals):
    """Write topics-ranked.json - full per-topic scoring detail."""
    records = []
    for i, t in enumerate(topics):
        records.append({
            'id': t.get('id'),
            'title': t.get('title'),
            'theme': t.get('theme'),
            'normalized_signals': {
                name: round(norm[i].get(name, 0.0), 6)
                for name in (s['name'] for s in active_signals)
            },
            'authority_score': round(scores[i], 6),
            'corroboration': {
                'families_fired': corroboration[i]['families_fired'],
                'flag': corroboration[i]['flag'],
            },
            'raw_rank': raw_ranks[i],
            'final_rank': final_ranks[i],
        })
    records.sort(key=lambda r: r['final_rank'])

    out = {
        'metadata': {
            **metadata,
            'scoring_model': os.path.basename(model_path),
            'generated': date.today().isoformat(),
            'active_signals': [s['name'] for s in active_signals],
            'dropped_optional_signals': dropped,
            'active_weights': {k: round(v, 6) for k, v in weights.items()},
        },
        'topics': records,
    }
    with open(path, 'w') as f:
        json.dump(out, f, indent=2)


# ---------------------------------------------------------------------------
# Output - topics-ranked.md
# ---------------------------------------------------------------------------

FLAG_BADGE = {
    'corroborated+trending': 'corroborated+trending',
    'corroborated': 'corroborated',
    'single-family': 'single-family',
    'uncorroborated': 'uncorroborated',
}


def write_md_output(path, metadata, topics, norm, scores, corroboration,
                    raw_ranks, final_ranks, weights, dropped, active_signals,
                    maha_appendix_lines=None):
    """
    Write topics-ranked.md:
      1. Final ranked table (final_rank order, post-floor).
      2. Topic Ideas - the original raw-score ranking, kept so operators
         can recover the pre-floor order after any manual reweighting.
      3. Optional Mahalanobis diagnostic appendix.
    """
    practice = str(metadata.get('practice_area', 'Unknown')).replace('-', ' ').title()
    client = metadata.get('client', 'Unknown')
    n = len(topics)

    lines = []
    lines.append(f"# Podcast Topics - {practice} (Ranked)")
    lines.append("")
    lines.append(f"**Client:** {client}")
    lines.append(f"**Practice Area:** {practice}")
    lines.append(f"**Generated:** {date.today().isoformat()}")
    lines.append(f"**Topics scored:** {n}")
    if dropped:
        lines.append(
            f"**Optional signals absent (weight redistributed):** {', '.join(dropped)}"
        )
    lines.append("")

    # Active model summary.
    lines.append("## Scoring Model")
    lines.append("")
    lines.append("Weighted sum of normalized signals (model: `references/scoring-model.json`).")
    lines.append("")
    lines.append("| Signal | Weight |")
    lines.append("|--------|--------|")
    for sig in active_signals:
        lines.append(f"| {sig['name']} | {weights[sig['name']]:.4f} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ---- 1. Final ranked table (post-floor) -------------------------------
    by_final = sorted(range(n), key=lambda i: final_ranks[i])
    lines.append("## Final Ranking")
    lines.append("")
    lines.append("Authority score plus the corroboration ranking floor "
                 "(corroborated topics protected ahead of single-family topics).")
    lines.append("")
    lines.append("| Rank | Topic | Score | Corroboration | Raw Rank | Rationale |")
    lines.append("|------|-------|-------|---------------|----------|-----------|")
    for i in by_final:
        t = topics[i]
        corro = corroboration[i]
        rationale = build_rationale(t, norm[i], corro, active_signals)
        moved = '' if final_ranks[i] == raw_ranks[i] else \
            f" ({'up' if final_ranks[i] < raw_ranks[i] else 'down'})"
        lines.append(
            f"| {final_ranks[i]} | {t.get('title', '')} | "
            f"{scores[i]:.3f} | {FLAG_BADGE[corro['flag']]} | "
            f"#{raw_ranks[i]}{moved} | {rationale} |"
        )
    lines.append("")

    # Note any floor movements explicitly.
    moved_topics = [i for i in range(n) if final_ranks[i] != raw_ranks[i]]
    if moved_topics:
        lines.append("### Corroboration floor adjustments")
        lines.append("")
        for i in sorted(moved_topics, key=lambda x: final_ranks[x]):
            t = topics[i]
            direction = 'lifted' if final_ranks[i] < raw_ranks[i] else 'displaced'
            lines.append(
                f"- **{t.get('title', '')}** ({corroboration[i]['flag']}): "
                f"raw #{raw_ranks[i]} {direction} to final #{final_ranks[i]}."
            )
        lines.append("")

    lines.append("---")
    lines.append("")

    # ---- 2. Topic Ideas (original ranking) ----------------------------
    # Operators keep this as the internal reference - it preserves the raw
    # authority-score order so the pre-floor ranking is always recoverable.
    by_raw = sorted(range(n), key=lambda i: raw_ranks[i])
    lines.append("## Topic Ideas (original ranking)")
    lines.append("")
    lines.append("Internal reference. Topics in raw authority-score order, "
                 "before the corroboration floor. This is the order to fall "
                 "back to if topics are manually reweighted.")
    lines.append("")
    # Rendered columns (v4.1.0): Rank | Topic | Theme | Rationale. The raw
    # authority_score, corroboration flag, and signal families are kept in
    # topics-ranked.json for the pod-2B-n-gram-table handoff but are no longer
    # rendered as their own columns - the AI-written Rationale (signal-citing
    # plain-language score/rank justification) replaces them.
    lines.append("| Rank | Topic | Theme | Rationale |")
    lines.append("|------|-------|-------|-----------|")
    for i in by_raw:
        t = topics[i]
        rationale = build_rationale(t, norm[i], corroboration[i], active_signals)
        lines.append(
            f"| {raw_ranks[i]} | {t.get('title', '')} | "
            f"{t.get('theme', '')} | {rationale} |"
        )
    lines.append("")

    # ---- 3. Optional Mahalanobis diagnostic appendix ----------------------
    if maha_appendix_lines:
        lines.append("---")
        lines.append("")
        lines.extend(maha_appendix_lines)
        lines.append("")

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


# ---------------------------------------------------------------------------
# Optional Mahalanobis diagnostic (collapsed, --mahalanobis only)
# ---------------------------------------------------------------------------
# Ported from the demoted mahalanobis-score.py. Covariance-corrected ranking
# plus a correlation matrix, DIMS-driven on the active signal set. This is now
# a diagnostic cross-check, not the primary ranking.

def mahalanobis_diagnostic(active_signals, topics, norm, scores,
                           final_ranks, visuals_dir=None):
    """
    Run the Mahalanobis diagnostic. Returns a list of markdown lines for the
    appendix. Writes a correlation heatmap to visuals_dir when possible.
    """
    try:
        import numpy as np
    except ImportError:
        return ["## Mahalanobis Diagnostic (appendix)", "",
                "_numpy not available - diagnostic skipped._"]

    dims = [s['name'] for s in active_signals]
    n = len(topics)
    p = len(dims)

    # Feature matrix from normalized signal values - DIMS-driven.
    X = np.array([[norm[i].get(d, 0.0) for d in dims] for i in range(n)])

    lines = ["## Mahalanobis Diagnostic (appendix)", ""]
    lines.append("Optional covariance-corrected cross-check. Not the primary "
                 "ranking - the Final Ranking above is authoritative. This "
                 "appendix only shows where signal correlations would shift "
                 "the order if double-counting were corrected.")
    lines.append("")

    if n <= p:
        lines.append(f"_Only {n} topics for {p} signals - covariance matrix "
                      "is rank-deficient, diagnostic is unreliable. Skipped._")
        return lines

    # Covariance + correlation.
    cov = np.cov(X, rowvar=False)
    std = np.sqrt(np.diag(cov))
    std[std == 0] = 1e-10
    corr = cov / np.outer(std, std)

    # Regularize a near-singular covariance before inverting.
    eig = np.linalg.eigvalsh(cov)
    if eig.min() < 1e-10:
        cov = cov + np.eye(p) * 1e-6
    cov_inv = np.linalg.inv(cov)

    # Mahalanobis distance to the data-derived ideal point (per-dim max).
    ideal = X.max(axis=0)
    dist = np.array([
        np.sqrt((X[i] - ideal) @ cov_inv @ (X[i] - ideal)) for i in range(n)
    ])
    max_d = dist.max()
    maha_score = 1.0 - (dist / max_d) if max_d > 0 else np.ones(n)

    # Mahalanobis ranking.
    maha_order = sorted(range(n), key=lambda i: -maha_score[i])
    maha_rank = {idx: r for r, idx in enumerate(maha_order, 1)}

    # Correlation matrix table.
    lines.append("### Signal correlations")
    lines.append("")
    lines.append("| | " + " | ".join(dims) + " |")
    lines.append("|---" * (p + 1) + "|")
    for i, d in enumerate(dims):
        row = f"| **{d}** |"
        for j in range(p):
            mark = " *" if abs(corr[i][j]) > 0.3 and i != j else ""
            row += f" {corr[i][j]:.3f}{mark} |"
        lines.append(row)
    lines.append("")
    sig_pairs = [
        (dims[i], dims[j], corr[i][j])
        for i in range(p) for j in range(i + 1, p)
        if abs(corr[i][j]) > 0.3
    ]
    total_pairs = p * (p - 1) // 2
    if sig_pairs:
        lines.append(f"**Correlated signal pairs (|r| > 0.3):** "
                      f"{len(sig_pairs)}/{total_pairs}")
        for d1, d2, r in sig_pairs:
            lines.append(f"- {d1} / {d2}: r = {r:.3f}")
    else:
        lines.append("**No significant signal correlations.** The linear "
                      "weighted sum is already independent - Mahalanobis "
                      "confirms rather than corrects.")
    lines.append("")

    # Final vs Mahalanobis comparison.
    lines.append("### Final ranking vs Mahalanobis")
    lines.append("")
    lines.append("| Topic | Final | Maha | Delta |")
    lines.append("|-------|-------|------|-------|")
    for i in sorted(range(n), key=lambda x: final_ranks[x]):
        t = topics[i]
        delta = final_ranks[i] - maha_rank[i]
        delta_str = f"+{delta}" if delta > 0 else str(delta)
        title = str(t.get('title', ''))[:55]
        lines.append(
            f"| {title} | #{final_ranks[i]} | #{maha_rank[i]} | {delta_str} |"
        )
    lines.append("")

    # Optional heatmap visual - only behind the flag, degrades gracefully.
    if visuals_dir:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            os.makedirs(visuals_dir, exist_ok=True)
            fig, ax = plt.subplots(figsize=(1.1 * p + 1.5, 1.0 * p + 1))
            im = ax.imshow(corr, cmap='RdYlBu_r', vmin=-1, vmax=1, aspect='auto')
            ax.set_xticks(range(p))
            ax.set_yticks(range(p))
            ax.set_xticklabels(dims, rotation=45, ha='right', fontsize=8)
            ax.set_yticklabels(dims, fontsize=8)
            for i in range(p):
                for j in range(p):
                    color = 'white' if abs(corr[i][j]) > 0.6 else 'black'
                    ax.text(j, i, f'{corr[i][j]:.2f}', ha='center',
                            va='center', fontsize=9, color=color)
            plt.colorbar(im, ax=ax, shrink=0.8, label='Pearson r')
            ax.set_title('Signal Correlation Matrix', fontsize=11,
                         fontweight='bold', pad=10)
            plt.tight_layout()
            heatmap_path = os.path.join(visuals_dir, 'correlation-heatmap.png')
            plt.savefig(heatmap_path, dpi=150, bbox_inches='tight')
            plt.close()
            lines.append(f"_Correlation heatmap: {heatmap_path}_")
            lines.append("")
        except ImportError:
            lines.append("_matplotlib not available - heatmap skipped._")
            lines.append("")

    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Score and rank podcast episode topics (JSON-driven).'
    )
    parser.add_argument('input', help='Path to input.json')
    parser.add_argument('--out', dest='out_dir', default=None,
                        help='Output directory (default: alongside the input)')
    parser.add_argument('--mahalanobis', action='store_true',
                        help='Append the optional Mahalanobis diagnostic + visuals')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, 'r') as f:
        data = json.load(f)

    metadata = data.get('metadata', {})
    topics = data.get('topics', [])
    if not topics:
        print("ERROR: input has no topics", file=sys.stderr)
        sys.exit(1)

    out_dir = args.out_dir or os.path.dirname(os.path.abspath(args.input))
    os.makedirs(out_dir, exist_ok=True)

    # 1. Load the canonical model.
    model_path = find_scoring_model()
    model = load_model(model_path)
    print(f"Loaded scoring model: {model_path}")

    # 2. Resolve the active signal set + weights (optional-signal handling).
    active_signals, weights, dropped = resolve_weights(model, topics)
    virality_active = any(s['name'] == 'virality' for s in active_signals)
    print(f"Active signals: {len(active_signals)} "
          f"({'virality present' if virality_active else 'virality absent'})")
    if dropped:
        print(f"Dropped optional signals (weight redistributed): "
              f"{', '.join(dropped)}")
    print(f"Active weights sum to {sum(weights.values()):.6f}")

    # 3. Normalize each signal column within the topic set.
    norm = build_normalized_signals(active_signals, topics)

    # 4. Authority score.
    scores = compute_authority_scores(active_signals, weights, norm)

    # 5. Corroboration flags.
    corroboration = compute_corroboration(model, topics, norm, virality_active)

    # 6. Raw ranking (preserved as the original order).
    raw_ranks = raw_rank(scores)

    # 7. Corroboration ranking floor -> final ranking.
    final_ranks = apply_corroboration_floor(model, scores, corroboration, raw_ranks)

    # 8a. Optional Mahalanobis diagnostic.
    maha_lines = None
    if args.mahalanobis:
        visuals_dir = os.path.join(out_dir, 'visuals')
        maha_lines = mahalanobis_diagnostic(
            active_signals, topics, norm, scores, final_ranks, visuals_dir
        )

    # 8b. Write outputs.
    json_path = os.path.join(out_dir, 'topics-ranked.json')
    md_path = os.path.join(out_dir, 'topics-ranked.md')
    write_json_output(json_path, model_path, metadata, topics, norm, scores,
                      corroboration, raw_ranks, final_ranks, weights, dropped,
                      active_signals)
    write_md_output(md_path, metadata, topics, norm, scores, corroboration,
                    raw_ranks, final_ranks, weights, dropped, active_signals,
                    maha_appendix_lines=maha_lines)

    # Console summary.
    print(f"\n[OK] {json_path}")
    print(f"[OK] {md_path}")
    n = len(topics)
    moved = sum(1 for i in range(n) if final_ranks[i] != raw_ranks[i])
    print(f"\nTop 5 (final rank):")
    by_final = sorted(range(n), key=lambda i: final_ranks[i])[:5]
    for i in by_final:
        print(f"  #{final_ranks[i]}  {scores[i]:.3f}  "
              f"[{corroboration[i]['flag']}]  {topics[i].get('title', '')}")
    print(f"\nCorroboration floor moved {moved} topic(s).")


if __name__ == '__main__':
    main()
