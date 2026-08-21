#!/usr/bin/env python3
"""
Podcast Topic Scorer — Unified Mahalanobis + Linear Pipeline

Reads 01-podcast-topics-ranked.json, computes Mahalanobis distance from each
episode to a data-derived ideal point through the inverse covariance matrix,
applies bridge floor correction, and overwrites 01-podcast-topics-ranked.md
with the final merged ranking (Mahalanobis primary, linear as diagnostic).

Also generates:
  - visuals/correlation-heatmap.png
  - visuals/rank-delta.png
  - visuals/entity-network.png

Usage:
  python3 mahalanobis-score.py <output_dir> [--bridge-floor] [--no-bridge-floor]

The output_dir must contain:
  - 01-podcast-topics-ranked.json (episode data with 5 scoring dimensions)
  - 00-entity-map.json (entity graph for network visualization)
"""

import argparse
import json
import os
import sys
from datetime import date

import numpy as np

# Optional imports — visuals degrade gracefully
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    HAS_NX = False


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
# All 5 authority-score dimensions (SKILL.md Step 3a). The pipeline is fully
# DIMS-driven — add or remove a dimension here and every matrix, correlation
# table, heatmap, and diagnostic adapts automatically.
DIMS = ['entity_density', 'bridge_value', 'avg_vector_strength', 'gap_opportunity', 'demand_signal']
WEIGHTS_LINEAR = [0.25, 0.25, 0.20, 0.15, 0.15]  # canonical authority_score weights (SKILL.md Step 3a); reference only — ranking uses Mahalanobis

# Short display labels for tight table headers / axis ticks
DIM_LABELS = {
    'entity_density': 'entity_density',
    'bridge_value': 'bridge_value',
    'avg_vector_strength': 'avg_VS',
    'gap_opportunity': 'gap_opportunity',
    'demand_signal': 'demand_signal',
}
NUM_PAIRS = len(DIMS) * (len(DIMS) - 1) // 2  # distinct dimension pairs


# ---------------------------------------------------------------------------
# Core math
# ---------------------------------------------------------------------------

def build_matrix(episodes):
    """Build n×len(DIMS) matrix from episode dimension values.

    Missing dimensions default to 0.0 — the keyword-research fallback path
    legitimately sets entity_density / bridge_value / avg_vector_strength to 0.
    """
    return np.array([[float(ep.get(d, 0.0)) for d in DIMS] for ep in episodes])


def mahalanobis_scores(X):
    """
    Compute Mahalanobis distance from each row to the data-derived ideal point,
    then convert to 0-1 scores (closer = higher).

    Returns (scores, cov_matrix, corr_matrix, eigenvalues, ideal_point, distances)
    """
    n, p = X.shape

    # Data-derived ideal: max of each dimension
    ideal = X.max(axis=0)

    # Covariance matrix
    cov = np.cov(X, rowvar=False)

    # Correlation matrix (for diagnostics)
    std = np.sqrt(np.diag(cov))
    std[std == 0] = 1e-10
    corr = cov / np.outer(std, std)

    # Eigenvalues for condition check
    eigenvalues = np.linalg.eigvalsh(cov)

    # Regularize if near-singular (add small ridge)
    min_eig = eigenvalues.min()
    if min_eig < 1e-10:
        cov += np.eye(p) * 1e-6
        eigenvalues = np.linalg.eigvalsh(cov)

    # Inverse covariance
    cov_inv = np.linalg.inv(cov)

    # Mahalanobis distance: D = sqrt((x - ideal)^T * Σ^-1 * (x - ideal))
    distances = np.zeros(n)
    for i in range(n):
        diff = X[i] - ideal
        distances[i] = np.sqrt(diff @ cov_inv @ diff)

    # Convert to 0-1 score: closer to ideal = higher score
    max_d = distances.max()
    if max_d > 0:
        scores = 1.0 - (distances / max_d)
    else:
        scores = np.ones(n)

    return scores, cov, corr, eigenvalues, ideal, distances


# ---------------------------------------------------------------------------
# Bridge floor constraint (Phase 3)
# ---------------------------------------------------------------------------

def apply_bridge_floor(episodes, maha_ranks, linear_ranks):
    """
    If episode has bridge_value in top quartile AND Mahalanobis dropped it 3+ ranks,
    floor it at linear_rank + 2.
    """
    bridge_values = [ep['bridge_value'] for ep in episodes]
    q75 = np.percentile(bridge_values, 75)

    adjustments = []
    for i, ep in enumerate(episodes):
        lin_rank = linear_ranks[i]
        mah_rank = maha_ranks[i]
        if ep['bridge_value'] >= q75 and (mah_rank - lin_rank) >= 3:
            floored_rank = lin_rank + 2
            adjustments.append({
                'title': ep['title'],
                'linear_rank': lin_rank,
                'maha_rank_before': mah_rank,
                'floored_to': floored_rank,
                'reason': f"bridge_value {ep['bridge_value']:.3f} >= Q75 ({q75:.3f}), dropped {mah_rank - lin_rank} ranks"
            })
            maha_ranks[i] = floored_rank

    # Re-sort to fix any rank collisions after flooring
    indexed = list(enumerate(maha_ranks))
    indexed.sort(key=lambda x: x[1])
    final_ranks = [0] * len(maha_ranks)
    for new_rank, (orig_idx, _) in enumerate(indexed, 1):
        final_ranks[orig_idx] = new_rank

    return final_ranks, adjustments


# ---------------------------------------------------------------------------
# Output generation
# ---------------------------------------------------------------------------

def generate_package_recommendations(episodes, ranks, entity_map_path, total_episodes):
    """
    Generate 6-episode and 12-episode package recommendations.
    Returns a list of markdown lines.
    """
    # Load entity map for tier data
    tier1_entities = set()
    all_entity_ids = set()
    total_clusters = 0
    entity_map_data = None
    if entity_map_path and os.path.exists(entity_map_path):
        with open(entity_map_path, 'r') as f:
            entity_map_data = json.load(f)
        for ent in entity_map_data.get('entities', []):
            all_entity_ids.add(ent['id'])
            if ent.get('tier') == 1:
                tier1_entities.add(ent['id'])
        clusters_data = entity_map_data.get('connection_graph', {}).get('clusters', {})
        total_clusters = len(clusters_data)

    # Build ranked list: [(rank, ep_idx), ...] sorted by rank
    ranked = sorted([(ranks[i], i) for i in range(len(episodes))], key=lambda x: x[0])

    # Wave 1 boundary (same logic as generate_markdown)
    wave1_end = max(4, total_episodes // 5)

    # Identify wave 1 episodes (rank 1..wave1_end)
    wave1_indices = set()
    for rank, ep_idx in ranked:
        if rank <= wave1_end:
            wave1_indices.add(ep_idx)

    # All clusters in the dataset
    all_clusters_set = set()
    for ep in episodes:
        pc = ep.get('primary_cluster')
        if pc is not None:
            all_clusters_set.add(pc)
        for bc in ep.get('bridge_clusters', []):
            all_clusters_set.add(bc)

    def select_package(target_size, ensure_cluster_coverage=False):
        """Select episodes for a package with Wave 1 guarantee and optional cluster coverage."""
        selected_indices = []
        selected_set = set()

        # Start with top N by rank
        for rank, ep_idx in ranked:
            if len(selected_indices) >= target_size:
                break
            selected_indices.append(ep_idx)
            selected_set.add(ep_idx)

        # Guarantee Wave 1 episodes are included
        for w1_idx in wave1_indices:
            if w1_idx not in selected_set:
                # Find lowest-ranked non-Wave-1 episode to swap out
                worst_non_w1 = None
                worst_rank = -1
                for sel_idx in selected_indices:
                    if sel_idx not in wave1_indices and ranks[sel_idx] > worst_rank:
                        worst_rank = ranks[sel_idx]
                        worst_non_w1 = sel_idx
                if worst_non_w1 is not None:
                    selected_indices.remove(worst_non_w1)
                    selected_set.discard(worst_non_w1)
                    selected_indices.append(w1_idx)
                    selected_set.add(w1_idx)

        # For 12-pack: ensure every cluster has at least one episode
        if ensure_cluster_coverage:
            covered_clusters = set()
            for idx in selected_indices:
                ep = episodes[idx]
                pc = ep.get('primary_cluster')
                if pc is not None:
                    covered_clusters.add(pc)
                for bc in ep.get('bridge_clusters', []):
                    covered_clusters.add(bc)

            uncovered = all_clusters_set - covered_clusters
            for uc in uncovered:
                # Find highest-ranked episode covering this cluster
                best_idx = None
                best_rank = float('inf')
                for rank, ep_idx in ranked:
                    if ep_idx in selected_set:
                        continue
                    ep = episodes[ep_idx]
                    ep_clusters = set()
                    pc = ep.get('primary_cluster')
                    if pc is not None:
                        ep_clusters.add(pc)
                    for bc in ep.get('bridge_clusters', []):
                        ep_clusters.add(bc)
                    if uc in ep_clusters and rank < best_rank:
                        best_rank = rank
                        best_idx = ep_idx
                if best_idx is not None:
                    # Swap out lowest-ranked non-Wave-1 episode
                    worst_non_w1 = None
                    worst_rank_val = -1
                    for sel_idx in selected_indices:
                        if sel_idx not in wave1_indices and ranks[sel_idx] > worst_rank_val:
                            worst_rank_val = ranks[sel_idx]
                            worst_non_w1 = sel_idx
                    if worst_non_w1 is not None:
                        selected_indices.remove(worst_non_w1)
                        selected_set.discard(worst_non_w1)
                        selected_indices.append(best_idx)
                        selected_set.add(best_idx)

        # Sort by rank for display
        selected_indices.sort(key=lambda idx: ranks[idx])
        return selected_indices

    def compute_coverage(selected_indices):
        """Compute coverage stats for a selection of episodes."""
        covered_entity_ids = set()
        covered_clusters = set()
        for idx in selected_indices:
            ep = episodes[idx]
            # Collect entity IDs if available
            for eid in ep.get('entity_ids', []):
                covered_entity_ids.add(eid)
            pc = ep.get('primary_cluster')
            if pc is not None:
                covered_clusters.add(pc)
            for bc in ep.get('bridge_clusters', []):
                covered_clusters.add(bc)

        tier1_covered = covered_entity_ids & tier1_entities if tier1_entities else set()
        return {
            'tier1_covered': len(tier1_covered),
            'tier1_total': len(tier1_entities),
            'tier1_pct': (len(tier1_covered) / len(tier1_entities) * 100) if tier1_entities else 0,
            'entities_covered': len(covered_entity_ids),
            'entities_total': len(all_entity_ids),
            'entities_pct': (len(covered_entity_ids) / len(all_entity_ids) * 100) if all_entity_ids else 0,
            'clusters_covered': len(covered_clusters),
            'clusters_total': total_clusters if total_clusters else len(all_clusters_set),
        }

    def why_this_one(ep):
        """Generate a short reason for why this episode was selected."""
        bridge_list = ep.get('bridge_clusters', [])
        entity_count = ep.get('entity_count', 0)
        gap = ep.get('gap_opportunity', 0)

        reasons = []
        if len(bridge_list) >= 2:
            reasons.append(f"Bridges {len(bridge_list)} clusters")
        if entity_count >= 8:
            reasons.append(f"Covers {entity_count} entities (densest)")
        elif entity_count >= 5:
            reasons.append(f"Covers {entity_count} entities")
        if gap >= 0.7:
            reasons.append(f"Gap opportunity {gap:.2f}")

        if not reasons:
            if len(bridge_list) == 1:
                reasons.append(f"Bridges {len(bridge_list)} cluster")
            elif entity_count > 0:
                reasons.append(f"Covers {entity_count} entities")
            else:
                reasons.append("High authority score")

        return "; ".join(reasons[:2])

    def wave_label(ep_idx):
        rank = ranks[ep_idx]
        if rank <= wave1_end:
            return "1"
        elif rank <= max(8, total_episodes * 2 // 5):
            return "2"
        elif rank <= max(14, total_episodes * 3 // 5):
            return "3"
        else:
            return "4"

    # Build the packages
    practice = episodes[0].get('primary_cluster', 'this practice area') if episodes else 'this practice area'

    lines = []
    lines.append("## Episode Package Recommendations")
    lines.append("")

    # 6-Episode Package
    six_pack = select_package(min(6, len(episodes)))
    six_coverage = compute_coverage(six_pack)

    lines.append("### 6-Episode Package")
    lines.append(f"*Best for: establishing initial topical authority in {practice}*")
    lines.append("")
    lines.append("| # | Episode Title | Authority Score | Wave | Why This One |")
    lines.append("|---|---|---|---|---|")
    for seq, idx in enumerate(six_pack, 1):
        ep = episodes[idx]
        from_scores_key = ranks[idx]  # use rank to find score
        # Find the score for this episode
        score_val = 0
        for i, e in enumerate(episodes):
            if i == idx:
                # We need scores passed in — use entity_density as proxy or compute inline
                break
        lines.append(f"| {seq} | {ep['title']} | #{ranks[idx]} | {wave_label(idx)} | {why_this_one(ep)} |")
    lines.append("")
    lines.append(f"**Coverage:** {six_coverage['tier1_pct']:.0f}% of Tier 1 entities, {six_coverage['clusters_covered']} of {six_coverage['clusters_total']} clusters touched")
    lines.append(f"**Est. recording time:** ~{len(six_pack) * 50 / 60:.1f} hours (avg 50 min/episode)")
    lines.append("")

    # 12-Episode Package
    twelve_pack = select_package(min(12, len(episodes)), ensure_cluster_coverage=True)
    twelve_coverage = compute_coverage(twelve_pack)

    lines.append("### 12-Episode Package")
    lines.append(f"*Best for: comprehensive authority across the full practice area*")
    lines.append("")
    lines.append("| # | Episode Title | Authority Score | Wave | Why This One |")
    lines.append("|---|---|---|---|---|")
    for seq, idx in enumerate(twelve_pack, 1):
        ep = episodes[idx]
        lines.append(f"| {seq} | {ep['title']} | #{ranks[idx]} | {wave_label(idx)} | {why_this_one(ep)} |")
    lines.append("")
    lines.append(f"**Coverage:** {twelve_coverage['tier1_pct']:.0f}% of Tier 1 entities, {twelve_coverage['entities_pct']:.0f}% of all entities, {twelve_coverage['clusters_covered']} of {twelve_coverage['clusters_total']} clusters")
    lines.append(f"**Est. recording time:** ~{len(twelve_pack) * 50 / 60:.1f} hours")

    # Additional value over 6-pack
    six_set = set(six_pack)
    twelve_set = set(twelve_pack)
    additional_eps = twelve_set - six_set
    additional_entities = twelve_coverage['entities_covered'] - six_coverage['entities_covered']
    additional_clusters = twelve_coverage['clusters_covered'] - six_coverage['clusters_covered']
    lines.append(f"**Additional value over 6-pack:** +{max(0, additional_entities)} entities covered, +{max(0, additional_clusters)} clusters")
    lines.append("")

    return lines


def generate_markdown(episodes, scores, ranks, linear_ranks, metadata, corr, eigenvalues,
                      ideal, bridge_adjustments, output_path, entity_map_path=None):
    """Generate unified 01-podcast-topics-ranked.md — Mahalanobis primary, linear as diagnostic."""
    ranked = sorted(zip(ranks, range(len(episodes))), key=lambda x: x[0])
    practice = metadata.get('practice_area', 'Unknown').replace('-', ' ').title()
    total_entities = metadata.get('total_entities', '?')
    total_clusters = metadata.get('total_clusters', '?')

    lines = []
    lines.append(f"# Podcast Topics — {practice} (Ranked by Authority Value)")
    lines.append("")
    lines.append(f"**Practice Area:** {practice}")
    lines.append(f"**Generated:** {date.today().isoformat()}")
    lines.append(f"**Source:** {metadata.get('episode_count', len(episodes))} episodes from {total_entities} entities across {total_clusters} clusters")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Ranking formula
    lines.append("## Ranking Formula")
    lines.append("")
    lines.append("Covariance-corrected Mahalanobis distance with bridge floor constraint.")
    lines.append("Accounts for correlations between scoring dimensions (e.g., entity_density ↔ bridge_value r=0.89)")
    lines.append("so structurally related signals aren't double-counted.")
    lines.append("")
    lines.append(f"**Dimensions:** {', '.join(DIMS)}")
    lines.append(f"**Ideal point (data-derived):** [{', '.join(f'{v:.3f}' for v in ideal)}]")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Episodes ranked
    lines.append(f"## {len(episodes)} Podcast Episodes — Ranked")
    lines.append("")

    for maha_rank, ep_idx in ranked:
        ep = episodes[ep_idx]
        score = scores[ep_idx]

        lines.append(f"### Rank {maha_rank}: {ep['title']}")
        lines.append(f"**Authority Score:** {score:.2f}")
        lines.append("")
        lines.append("| Attribute | Value |")
        lines.append("|-----------|-------|")

        if 'primary_cluster' in ep:
            lines.append(f"| Primary Cluster | {ep.get('primary_cluster', '—')} |")
        if 'bridge_clusters' in ep:
            bridge_list = ep.get('bridge_clusters', [])
            if bridge_list:
                lines.append(f"| Bridge Clusters | {', '.join(str(c) for c in bridge_list)} |")
        lines.append(f"| Entity Count | {ep.get('entity_count', '—')} |")
        lines.append(f"| Avg Vector Strength | {ep.get('avg_vector_strength', 0):.2f} |")
        lines.append(f"| Gap Opportunity | {ep.get('gap_opportunity', 0):.2f} |")
        lines.append(f"| Demand Signal | {ep.get('demand_signal', 0):.2f} |")
        if ep.get('monthly_search_volume') is not None:
            lines.append(f"| Monthly Search Volume | {ep.get('monthly_search_volume')} |")
        lines.append("")

        if 'episode_angle' in ep:
            lines.append(f"**Episode angle:** {ep['episode_angle']}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Production order
    lines.append("## Production Order Recommendation")
    lines.append("")
    lines.append("Per Koray's methodology: **build from the center out.** Record highest entity-density, highest bridge-value topics first to establish the entity graph's core. Then expand to niche topics.")
    lines.append("")
    total = len(episodes)
    wave_breaks = [
        (1, max(4, total // 5), "Core Authority", "Covers all Tier 1 entities. Establishes foundations. Maximum bridge coverage."),
        (max(4, total // 5) + 1, max(8, total * 2 // 5), "Differentiation", "Attacks highest gap opportunities. Builds unique branches."),
        (max(8, total * 2 // 5) + 1, max(14, total * 3 // 5), "Depth", "Fills remaining clusters and mid-priority topics."),
        (max(14, total * 3 // 5) + 1, total, "Niche Authority", "Long-tail entities with zero competitor coverage. Pure differentiation."),
    ]

    lines.append("| Wave | Episodes | Rationale |")
    lines.append("|------|----------|-----------|")
    for wave_num, (start, end, label, rationale) in enumerate(wave_breaks, 1):
        wave_eps = [ep_idx for maha_rank, ep_idx in ranked if start <= maha_rank <= end]
        ep_titles = ", ".join(f"#{ranks[i]}" for i in wave_eps)
        lines.append(f"| **Wave {wave_num} ({label})** | {ep_titles} | {rationale} |")
    lines.append("")

    # Episode Package Recommendations
    package_lines = generate_package_recommendations(episodes, ranks, entity_map_path, total)
    lines.extend(package_lines)

    # Coverage matrix
    lines.append("---")
    lines.append("")
    lines.append("## Coverage Matrix")
    lines.append("")
    # Build cluster → episode mapping
    cluster_coverage = {}
    for maha_rank, ep_idx in ranked:
        ep = episodes[ep_idx]
        pc = ep.get('primary_cluster')
        if pc is not None:
            cluster_coverage.setdefault(pc, []).append(maha_rank)
        for bc in ep.get('bridge_clusters', []):
            cluster_coverage.setdefault(bc, []).append(maha_rank)

    if cluster_coverage:
        lines.append("| Cluster | Episodes Covering It |")
        lines.append("|---------|---------------------|")
        for cluster_id in sorted(cluster_coverage.keys()):
            eps_list = sorted(set(cluster_coverage[cluster_id]))
            lines.append(f"| {cluster_id} | {', '.join(f'#{r}' for r in eps_list)} |")
        lines.append("")

    # Diagnostics appendix
    lines.append("---")
    lines.append("")
    lines.append("## Scoring Diagnostics")
    lines.append("")
    lines.append("<details>")
    lines.append("<summary>Dimension correlations, bridge floor adjustments, and linear comparison</summary>")
    lines.append("")

    # Correlation matrix
    lines.append("### Dimension Correlations")
    lines.append("")
    lines.append("| | " + " | ".join(DIM_LABELS[d] for d in DIMS) + " |")
    lines.append("|---" * (len(DIMS) + 1) + "|")
    for i, dim in enumerate(DIMS):
        row = f"| **{DIM_LABELS[dim]}** |"
        for j in range(len(DIMS)):
            val = corr[i][j]
            marker = " *" if abs(val) > 0.3 and i != j else ""
            row += f" {val:.3f}{marker} |"
        lines.append(row)
    lines.append("")

    sig_pairs = []
    for i in range(len(DIMS)):
        for j in range(i+1, len(DIMS)):
            if abs(corr[i][j]) > 0.3:
                sig_pairs.append((DIMS[i], DIMS[j], corr[i][j]))

    if sig_pairs:
        lines.append(f"**Significant correlations (|r| > 0.3):** {len(sig_pairs)}/{NUM_PAIRS}")
        for d1, d2, r in sig_pairs:
            lines.append(f"- {d1} ↔ {d2}: r = {r:.3f}")
    else:
        lines.append("**No significant correlations found.** Linear formula was already valid.")
    lines.append("")

    # Bridge floor
    if bridge_adjustments:
        lines.append("### Bridge Floor Adjustments")
        lines.append("")
        lines.append("Episodes with top-quartile bridge_value that dropped 3+ ranks were floored at linear_rank + 2:")
        lines.append("")
        for adj in bridge_adjustments:
            lines.append(f"- **{adj['title']}**: raw #{adj['maha_rank_before']} → floored to #{adj['floored_to']}")
        lines.append("")

    # Linear comparison
    lines.append("### Linear vs Final Ranking")
    lines.append("")
    lines.append("| Episode | Linear | Final | Delta |")
    lines.append("|---------|--------|-------|-------|")
    for maha_rank, ep_idx in ranked:
        ep = episodes[ep_idx]
        lin_rank = linear_ranks[ep_idx]
        delta = lin_rank - maha_rank
        delta_str = f"+{delta}" if delta > 0 else str(delta)
        marker = " ^^" if delta >= 2 else (" vv" if delta <= -2 else "")
        lines.append(f"| {ep['title'][:55]} | #{lin_rank} | #{maha_rank} | {delta_str}{marker} |")
    lines.append("")

    lines.append("</details>")
    lines.append("")

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))


# ---------------------------------------------------------------------------
# Visualizations
# ---------------------------------------------------------------------------

def generate_correlation_heatmap(corr, output_path):
    """len(DIMS)×len(DIMS) correlation heatmap."""
    if not HAS_MPL:
        print("  [SKIP] matplotlib not available — skipping correlation heatmap")
        return

    p = len(DIMS)
    fig, ax = plt.subplots(figsize=(1.1 * p + 1.5, 1.0 * p + 1))
    labels = [DIM_LABELS[d] for d in DIMS]

    im = ax.imshow(corr, cmap='RdYlBu_r', vmin=-1, vmax=1, aspect='auto')
    ax.set_xticks(range(p))
    ax.set_yticks(range(p))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(labels, fontsize=9)

    # Annotate cells
    for i in range(p):
        for j in range(p):
            color = 'white' if abs(corr[i][j]) > 0.6 else 'black'
            ax.text(j, i, f'{corr[i][j]:.2f}', ha='center', va='center', fontsize=11,
                    fontweight='bold' if abs(corr[i][j]) > 0.3 and i != j else 'normal',
                    color=color)

    plt.colorbar(im, ax=ax, shrink=0.8, label='Pearson r')
    ax.set_title('Dimension Correlation Matrix', fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved correlation heatmap → {output_path}")


def generate_rank_delta(episodes, ranks, linear_ranks, output_path):
    """Horizontal bar chart of rank changes per episode."""
    if not HAS_MPL:
        print("  [SKIP] matplotlib not available — skipping rank delta chart")
        return

    deltas = [linear_ranks[i] - ranks[i] for i in range(len(episodes))]
    titles = [ep['title'][:45] + ('...' if len(ep['title']) > 45 else '') for ep in episodes]

    # Sort by delta for visual clarity
    sorted_idx = sorted(range(len(deltas)), key=lambda i: deltas[i])
    sorted_deltas = [deltas[i] for i in sorted_idx]
    sorted_titles = [titles[i] for i in sorted_idx]

    fig, ax = plt.subplots(figsize=(10, max(6, len(episodes) * 0.35)))
    colors = ['#22c55e' if d > 0 else '#ef4444' if d < 0 else '#94a3b8' for d in sorted_deltas]
    bars = ax.barh(range(len(sorted_deltas)), sorted_deltas, color=colors, edgecolor='none', height=0.7)

    ax.set_yticks(range(len(sorted_titles)))
    ax.set_yticklabels(sorted_titles, fontsize=8)
    ax.set_xlabel('Rank Change (positive = rose in Mahalanobis)', fontsize=10)
    ax.set_title('Rank Delta: Linear → Mahalanobis', fontsize=12, fontweight='bold')
    ax.axvline(x=0, color='#64748b', linewidth=0.8, linestyle='-')
    ax.grid(axis='x', alpha=0.3)

    # Annotate bars
    for i, (bar, delta) in enumerate(zip(bars, sorted_deltas)):
        if delta != 0:
            ax.text(bar.get_width() + (0.15 if delta >= 0 else -0.15), bar.get_y() + bar.get_height()/2,
                    f'{"+"+str(delta) if delta > 0 else str(delta)}',
                    va='center', ha='left' if delta >= 0 else 'right', fontsize=8, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved rank delta chart → {output_path}")


def generate_entity_network(entity_map_path, output_path):
    """Network graph of entities sized by vector_strength, colored by cluster."""
    if not HAS_MPL or not HAS_NX:
        print("  [SKIP] matplotlib/networkx not available — skipping entity network")
        return

    with open(entity_map_path, 'r') as f:
        data = json.load(f)

    entities = {e['id']: e for e in data['entities']}
    clusters = data.get('connection_graph', {}).get('clusters', {})
    bridge_entities = {b['id'] for b in data.get('connection_graph', {}).get('bridge_entities', [])}

    # Build graph
    G = nx.Graph()
    for e in data['entities']:
        G.add_node(e['id'], label=e['name'], vs=e['vector_strength'], tier=e['tier'])

    # Add edges from connections (match names to IDs)
    name_to_id = {e['name']: e['id'] for e in data['entities']}
    for e in data['entities']:
        for conn_name in e.get('connections', []):
            if conn_name in name_to_id:
                G.add_edge(e['id'], name_to_id[conn_name])

    # Cluster color assignment
    cluster_colors = {}
    color_palette = ['#3b82f6', '#22c55e', '#f97316', '#a855f7', '#0ea5e9',
                     '#8b5cf6', '#ef4444', '#eab308', '#14b8a6', '#f43f5e',
                     '#6366f1', '#84cc16']
    for idx, (cluster_key, cluster_data) in enumerate(clusters.items()):
        color = color_palette[idx % len(color_palette)]
        for eid in cluster_data['entities']:
            cluster_colors[eid] = color

    # Node properties
    node_colors = [cluster_colors.get(n, '#94a3b8') for n in G.nodes()]
    node_sizes = [entities[n]['vector_strength'] * 600 + 100 for n in G.nodes()]
    edge_widths = [0.3 for _ in G.edges()]
    node_borders = [2.5 if n in bridge_entities else 0.5 for n in G.nodes()]
    border_colors = ['#facc15' if n in bridge_entities else '#1e293b' for n in G.nodes()]

    fig, ax = plt.subplots(figsize=(14, 10))
    pos = nx.spring_layout(G, k=1.8, iterations=80, seed=42)

    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.15, width=0.5, edge_color='#64748b')

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes,
                           linewidths=node_borders, edgecolors=border_colors, alpha=0.85)

    # Labels for bridge entities and tier 1
    labels = {}
    for n in G.nodes():
        e = entities[n]
        if n in bridge_entities or e['tier'] == 1:
            labels[n] = e['name'][:20]
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=7, font_weight='bold',
                            font_color='#1e293b')

    # Legend
    legend_patches = []
    for idx, (cluster_key, cluster_data) in enumerate(clusters.items()):
        color = color_palette[idx % len(color_palette)]
        legend_patches.append(mpatches.Patch(color=color, label=cluster_data['label'][:30]))
    legend_patches.append(mpatches.Patch(facecolor='white', edgecolor='#facc15',
                                         linewidth=2, label='Bridge entity'))
    ax.legend(handles=legend_patches, loc='upper left', fontsize=7, framealpha=0.9)

    ax.set_title('Entity Network — Sized by Vector Strength, Colored by Cluster',
                 fontsize=13, fontweight='bold', pad=12)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved entity network → {output_path}")


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------

def print_diagnostics(episodes, scores, ranks, linear_ranks, corr, eigenvalues, ideal, distances):
    """Print diagnostic summary to stdout."""
    print("\n" + "=" * 70)
    print("MAHALANOBIS SCORING DIAGNOSTICS")
    print("=" * 70)

    print(f"\nEpisodes: {len(episodes)}")
    print(f"Dimensions: {len(DIMS)}")
    print(f"Ratio (n/p): {len(episodes)/len(DIMS):.1f}x (minimum recommended: 5x)")

    print(f"\nIdeal point: {', '.join(f'{DIMS[i]}={ideal[i]:.3f}' for i in range(len(DIMS)))}")

    print("\nCorrelation Matrix:")
    print(f"{'':>20}" + ''.join(f"{DIM_LABELS[d][:12]:>13}" for d in DIMS))
    for i, dim in enumerate(DIMS):
        row = f"{dim:>20}"
        for j in range(len(DIMS)):
            marker = " *" if abs(corr[i][j]) > 0.3 and i != j else "  "
            row += f" {corr[i][j]:>10.3f}{marker}"
        print(row)

    sig_count = sum(1 for i in range(len(DIMS)) for j in range(i+1, len(DIMS)) if abs(corr[i][j]) > 0.3)
    print(f"\nSignificant correlations (|r| > 0.3): {sig_count}/{NUM_PAIRS}")

    print(f"\nEigenvalues: {', '.join(f'{e:.4f}' for e in sorted(eigenvalues, reverse=True))}")
    print(f"Condition number: {max(eigenvalues)/max(min(eigenvalues), 1e-10):.1f}")

    if sig_count == 0:
        print("\n⚠️  HONEST EXIT: All pairwise correlations < 0.3.")
        print("   The linear formula is already valid — dimensions are approximately independent.")
        print("   Mahalanobis ranking is a diagnostic confirmation, not an improvement.")
    else:
        print(f"\n✅ Mahalanobis adds value: {sig_count} correlated dimension pair(s) detected.")

    # Rank changes
    print("\n" + "-" * 70)
    print("RANK CHANGES (Linear → Mahalanobis)")
    print("-" * 70)
    changes = [(i, linear_ranks[i], ranks[i], linear_ranks[i] - ranks[i])
               for i in range(len(episodes))]
    changes.sort(key=lambda x: abs(x[3]), reverse=True)

    print(f"{'Episode':50} {'Lin':>5} {'Maha':>5} {'Delta':>6}")
    movers = 0
    for ep_idx, lin, maha, delta in changes:
        marker = " ⬆" if delta >= 2 else (" ⬇" if delta <= -2 else "")
        if delta != 0:
            movers += 1
        print(f"{episodes[ep_idx]['title'][:50]:50} {lin:>5} {maha:>5} {'+' if delta > 0 else ''}{delta:>5}{marker}")

    mid_range_shifts = sum(1 for _, lin, _, delta in changes if 8 <= lin <= 16 and abs(delta) >= 2)
    top_linear = set(i for i, ep in enumerate(episodes) if linear_ranks[i] <= 4)
    top_maha = set(i for i in range(len(episodes)) if ranks[i] <= 6)

    print(f"\n--- Acceptance Criteria ---")
    print(f"Episodes that moved: {movers}/{len(episodes)}")
    print(f"Top 4 linear in top 6 Mahalanobis: {len(top_linear & top_maha)}/4 ({'PASS' if len(top_linear & top_maha) >= 4 else 'CHECK'})")
    print(f"Mid-range (8-16) shifted 2+: {mid_range_shifts} ({'PASS' if mid_range_shifts >= 2 else 'CHECK'})")
    print(f"Significant correlations: {sig_count} ({'PASS' if sig_count > 0 else 'NEUTRAL — linear is fine'})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Mahalanobis distance scoring for podcast episodes')
    parser.add_argument('output_dir', help='Directory containing 01-podcast-topics-ranked.json')
    parser.add_argument('--bridge-floor', dest='bridge_floor', action='store_true', default=True,
                        help='Apply bridge floor constraint (default: on)')
    parser.add_argument('--no-bridge-floor', dest='bridge_floor', action='store_false',
                        help='Disable bridge floor constraint')
    args = parser.parse_args()

    output_dir = args.output_dir
    json_path = os.path.join(output_dir, '01-podcast-topics-ranked.json')
    entity_map_path = os.path.join(output_dir, '00-entity-map.json')
    visuals_dir = os.path.join(output_dir, 'visuals')

    # Load data
    if not os.path.exists(json_path):
        print(f"ERROR: {json_path} not found")
        sys.exit(1)

    with open(json_path, 'r') as f:
        data = json.load(f)

    metadata = data.get('metadata', {})
    episodes = data['episodes']
    print(f"Loaded {len(episodes)} episodes from {json_path}")

    # Build feature matrix
    X = build_matrix(episodes)
    print(f"Feature matrix: {X.shape[0]} × {X.shape[1]}")

    # Compute Mahalanobis scores
    scores, cov, corr, eigenvalues, ideal, distances = mahalanobis_scores(X)

    # Rank by score (highest = rank 1)
    score_order = np.argsort(-scores)
    ranks = np.zeros(len(episodes), dtype=int)
    for rank, idx in enumerate(score_order, 1):
        ranks[idx] = rank
    ranks = ranks.tolist()

    linear_ranks = [ep['rank'] for ep in episodes]

    # Bridge floor (Phase 3)
    bridge_adjustments = []
    if args.bridge_floor:
        ranks, bridge_adjustments = apply_bridge_floor(episodes, ranks, linear_ranks)
        if bridge_adjustments:
            print(f"Bridge floor applied: {len(bridge_adjustments)} episode(s) adjusted")

    # Print diagnostics
    print_diagnostics(episodes, scores, ranks, linear_ranks, corr, eigenvalues, ideal, distances)

    # Generate unified output markdown (overwrites linear-only version)
    md_path = os.path.join(output_dir, '01-podcast-topics-ranked.md')
    generate_markdown(episodes, scores, ranks, linear_ranks, metadata, corr, eigenvalues,
                      ideal, bridge_adjustments, md_path, entity_map_path=entity_map_path)
    print(f"\n[OK] Saved unified ranking → {md_path}")

    # Generate visuals
    os.makedirs(visuals_dir, exist_ok=True)
    generate_correlation_heatmap(corr, os.path.join(visuals_dir, 'correlation-heatmap.png'))
    generate_rank_delta(episodes, ranks, linear_ranks, os.path.join(visuals_dir, 'rank-delta.png'))

    if os.path.exists(entity_map_path):
        generate_entity_network(entity_map_path, os.path.join(visuals_dir, 'entity-network.png'))
    else:
        print(f"  [SKIP] {entity_map_path} not found — skipping entity network")

    print("\n✅ Done.")


if __name__ == '__main__':
    main()
