#!/usr/bin/env python3
"""
render-episode-question-tables.py - writes the `## Episode Breakdown` section.

Builds one per-episode question table for every locked episode from its
pod-2B-n-gram-table output, runs the cross-episode de-duplication pass, and rebuilds
the Doc's Episode Breakdown sub-sections. Episode 1 is the standing exception -
its table is the canonical Founder Story interview set.

Episodes 2-12 + additionals : columns  Question | Keywords | Rationale
Episode 1                    : columns  Question | Rationale

Usage:  python3 render-episode-question-tables.py <doc_id> <ngram_dir> <selection.json>

ngram_dir holds one folder per episode, each with `n-gram-table.json`.
"""

import json
import os
import re
import sys

from lib_doc_table import rebuild_table, get_doc, batch, keywords_cell

# ngram folder slug -> episode heading in the Doc
EPISODE_HEADINGS = [
    ("motorcycle-settlement",  "Episode 2: What a Texas Motorcycle Settlement Is Worth"),
    ("car-settlements",        "Episode 3: Average Car Accident Settlements in Houston by Injury"),
    ("uber-settlement",        "Episode 4: What an Uber Accident Settlement Is Worth"),
    ("hours-of-service",       "Episode 5: Hours of Service: Driver Fatigue and the Federal Rulebook"),
    ("fault-law",              "Episode 6: How Texas Fault Law Works: the 51% Rule and the No-Fault Myth"),
    ("stowers-demand",         "Episode 7: The Stowers Demand: Forcing Insurers Past Policy Limits"),
    ("brain-injuries",         "Episode 8: Proving Brain Injuries and Herniated Discs After a Crash"),
    ("30-day-window",          "Episode 9: The 30-Day Truck Wreck Window: ELD, Black Box, and Spoliation"),
    ("truck-wrongful-death",   "Episode 10: Wrongful Death After a Fatal 18-Wheeler Crash"),
    ("statute-of-limitations", "Episode 11: The 2-Year Deadline: Texas Statute of Limitations"),
    ("truck-law",              "Episode 12: Texas Truck Law: HB 19 and the Filing Deadline"),
    ("insurance-coverage",     "Additional Topic: The Insurance Coverage Houston Drivers Don't Know They Have"),
    ("truck-settlement-range", "Additional Topic: The Real Range of Houston Truck Accident Settlements"),
    ("lane-splitting",         "Additional Topic: Why Lane-Splitting Is Illegal in Texas"),
]
QUESTION_WIDTHS = [210, 150, 108]   # Question | Keywords | Rationale
SLUG_PA = {
    "car-settlements": "car", "fault-law": "car", "stowers-demand": "car",
    "brain-injuries": "car", "statute-of-limitations": "car", "insurance-coverage": "car",
    "hours-of-service": "truck", "30-day-window": "truck", "truck-wrongful-death": "truck",
    "truck-law": "truck", "truck-settlement-range": "truck",
    "motorcycle-settlement": "motorcycle", "lane-splitting": "motorcycle",
    "uber-settlement": "rideshare",
}
KW_BASE = "/Users/gjordan/Desktop/claude_code/deliverables/podcast-research/sutliff-stout"
E1_WIDTHS = [300, 168]              # Question | Rationale
E1_HEADING = "Episode 1: Founder Story"
E1_TOKENS = {"{{LOCATION}}": "Houston, TX", "{{BUSINESS}}": "Sutliff & Stout",
             "{{NICHE}}": "personal injury law"}


def norm(q):
    return re.sub(r"[^a-z0-9 ]", "", q.lower()).strip()


def _keywords(q):
    return set(w for w in norm(q).split() if len(w) > 3)


def load_ngram_episodes(ngram_dir):
    """Load each episode's question rows; apply the cross-episode dedup pass."""
    eps = {}
    for slug, _ in EPISODE_HEADINGS:
        p = os.path.join(ngram_dir, slug, "n-gram-table.json")
        rows = json.load(open(p))["content"]["rows"]
        eps[slug] = rows
    # cross-episode dedup: drop a question already used in an earlier episode -
    # exact match OR a near-duplicate a host would experience as the same
    # question (>= 70% keyword overlap).
    seen = []  # (norm, keyword_set, slug)
    dropped = []
    for slug, _ in EPISODE_HEADINGS:
        kept = []
        for r in eps[slug]:
            q = r["question_text"]
            n, k = norm(q), _keywords(q)
            dup_of = None
            for sn, sk, sslug in seen:
                if n == sn or (k and sk and len(k & sk) / max(len(k), len(sk)) >= 0.7):
                    dup_of = sslug
                    break
            if dup_of:
                dropped.append((slug, q, dup_of))
                continue
            seen.append((n, k, slug))
            kept.append(r)
        eps[slug] = kept
    return eps, dropped


def persist_dedup(ngram_dir, dropped):
    """Write the cross-episode dedup back into the canonical n-gram tables.

    The dedup decides one question stays in one episode; without this the cut
    lives only in the rendered Doc and the n-gram-table.json files still carry
    the duplicate - so pod-3A-ros-template would pull it back. Rewriting the JSON
    (and the .md mirror) here keeps every downstream consumer reading the same
    deduped set. Idempotent: a re-run reads already-deduped tables, drops 0.
    """
    by_slug = {}
    for slug, q, dup_of in dropped:
        by_slug.setdefault(slug, []).append((q, dup_of))
    for slug, items in by_slug.items():
        drop_texts = {q.strip() for q, _ in items}
        jpath = os.path.join(ngram_dir, slug, "n-gram-table.json")
        d = json.load(open(jpath))
        d["content"]["rows"] = [r for r in d["content"]["rows"]
                                if r["question_text"].strip() not in drop_texts]
        d["content"]["row_count"] = len(d["content"]["rows"])
        for q, dup_of in items:
            d["content"].setdefault("dedup_merges", []).append({
                "merged": q, "cross_episode": True,
                "reason": "Cross-episode duplicate - same question is in the "
                          "%s episode; kept there, dropped here." % dup_of})
        json.dump(d, open(jpath, "w"), indent=2)
        mpath = os.path.join(ngram_dir, slug, "N-Gram Table.md")
        if os.path.exists(mpath):
            out, qn = [], 0
            for ln in open(mpath).read().split("\n"):
                if re.match(r"^\|\s*Q\d+:", ln):
                    body = re.sub(r"^\|\s*Q\d+:\s*", "", ln)
                    if body.split(" |")[0].strip() in drop_texts:
                        continue
                    qn += 1
                    out.append("| Q%d: %s" % (qn, body))
                else:
                    out.append(ln)
            open(mpath, "w").write("\n".join(out))
        print("  persisted dedup -> %s n-gram table (-%d question)" % (slug, len(items)))


def load_e1_questions(skill_root):
    """Parse the 21 canonical Founder Story questions + rationales."""
    path = os.path.join(skill_root, "references", "e1-founder-interview-questions.md")
    out = []
    for line in open(path):
        line = line.strip()
        if not line.startswith("|") or line.startswith("| Question") or set(line) <= set("|- "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 2:
            continue
        q, rat = cells
        for tok, val in E1_TOKENS.items():
            q = q.replace(tok, val)
        out.append([q, rat])
    return out


def rationale_from_row(r):
    preds = r.get("predicates", [])
    txt = "; ".join(preds[:2]) if preds else "covers the episode's core entities"
    return (txt[:1].upper() + txt[1:])[:160]


def fix_additional_headings(doc_id):
    """Rename the stale 'Additional Topic:' headings to this run's 3 additionals
    and delete any surplus Additional Topic sub-sections."""
    targets = [h for s, h in EPISODE_HEADINGS if h.startswith("Additional Topic:")]
    doc = get_doc(doc_id)
    body = doc["body"]["content"]
    add_heads = []
    internal_idx = None
    for el in body:
        if "paragraph" not in el:
            continue
        st = el["paragraph"].get("paragraphStyle", {}).get("namedStyleType", "")
        txt = "".join(r.get("textRun", {}).get("content", "")
                      for r in el["paragraph"].get("elements", [])).strip()
        if st == "HEADING_3" and txt.startswith("Additional Topic:"):
            add_heads.append({"s": el["startIndex"], "e": el["endIndex"], "txt": txt})
        if st in ("HEADING_1",) and txt == "INTERNAL":
            internal_idx = el["startIndex"]
    # delete each surplus Additional Topic sub-section (its start -> next heading)
    heads_sorted = sorted(add_heads, key=lambda h: h["s"])
    boundaries = [h["s"] for h in heads_sorted] + [internal_idx]
    del_ranges = []
    for i, h in enumerate(heads_sorted):
        if i >= len(targets):
            del_ranges.append((h["s"], boundaries[i + 1]))
    for s, e in sorted(del_ranges, key=lambda x: -x[0]):
        batch(doc_id, [{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}}])
    # rename the first len(targets) headings
    doc = get_doc(doc_id)
    add_heads = []
    for el in doc["body"]["content"]:
        if "paragraph" not in el:
            continue
        st = el["paragraph"].get("paragraphStyle", {}).get("namedStyleType", "")
        txt = "".join(r.get("textRun", {}).get("content", "")
                      for r in el["paragraph"].get("elements", [])).strip()
        if st == "HEADING_3" and txt.startswith("Additional Topic:"):
            add_heads.append({"s": el["startIndex"], "e": el["endIndex"], "txt": txt})
    add_heads.sort(key=lambda h: h["s"])
    reqs = []
    for h, new in sorted(zip(add_heads, targets), key=lambda x: -x[0]["s"]):
        if h["txt"] != new:
            reqs.append({"deleteContentRange": {
                "range": {"startIndex": h["s"], "endIndex": h["e"] - 1}}})
            reqs.append({"insertText": {"location": {"index": h["s"]}, "text": new}})
    if reqs:
        batch(doc_id, reqs)


def load_keyword_msv(pa):
    """Return {lowercased query: msv} from a practice area's keyword research."""
    path = os.path.join(KW_BASE, "%s-accidents-tx-houston" % pa,
                        "02.5-keywords", "keyword-research.json")
    out = {}
    for k in json.load(open(path)).get("keywords", []):
        q = (k.get("query") or "").lower().strip()
        if q:
            out[q] = int(k.get("msv") or 0)
    return out


def question_keywords_cell(ngrams, msv_map):
    """Build the Keywords cell for one question - resolve each n-gram to an MSV
    from the keyword research, then format with the canonical keywords_cell.
    Falls back to a plain n-gram list when no n-gram resolves to an MSV."""
    matched = []
    for ng in ngrams:
        n = ng.lower().strip()
        msv = msv_map.get(n)
        if msv is None:
            for q, v in msv_map.items():
                if len(q) > 6 and (n in q or q in n):
                    msv = v
                    break
        if msv:
            matched.append([ng, msv])
    if matched:
        return keywords_cell({"total": sum(m for _, m in matched), "list": matched})
    return "; ".join(ngrams[:4])


def apply_episode_dividers(doc_id):
    """Put a thin top border on every Episode 2-onward heading - a divider line
    between episodes. Idempotent: re-applying re-sets the same border."""
    targets = {h for _, h in EPISODE_HEADINGS}
    doc = get_doc(doc_id)
    reqs = []
    for el in doc["body"]["content"]:
        if "paragraph" not in el:
            continue
        st = el["paragraph"].get("paragraphStyle", {}).get("namedStyleType", "")
        txt = "".join(r.get("textRun", {}).get("content", "")
                      for r in el["paragraph"].get("elements", [])).strip()
        if st == "HEADING_3" and txt in targets:
            reqs.append({"updateParagraphStyle": {
                "range": {"startIndex": el["startIndex"], "endIndex": el["endIndex"]},
                "paragraphStyle": {"borderTop": {
                    "color": {"color": {"rgbColor": {"red": 0.8, "green": 0.8, "blue": 0.8}}},
                    "width": {"magnitude": 1, "unit": "PT"},
                    "padding": {"magnitude": 8, "unit": "PT"},
                    "dashStyle": "SOLID"}},
                "fields": "borderTop"}})
    if reqs:
        batch(doc_id, reqs)
    print("applied %d episode dividers" % len(reqs))


def main():
    if len(sys.argv) != 4:
        print("usage: render-episode-question-tables.py <doc_id> <ngram_dir> <selection.json>",
              file=sys.stderr)
        sys.exit(1)
    doc_id, ngram_dir, _sel = sys.argv[1], sys.argv[2], sys.argv[3]
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    eps, dropped = load_ngram_episodes(ngram_dir)
    print("cross-episode dedup dropped %d question(s)" % len(dropped))
    for slug, q, src in dropped:
        print("  [%s] dropped (already in %s): %s" % (slug, src, q[:64]))
    # persist the dedup into the canonical n-gram tables so downstream
    # (pod-3A-ros-template) reads the same deduped set - never just the Doc.
    persist_dedup(ngram_dir, dropped)

    fix_additional_headings(doc_id)

    # Episode 1 - canonical Founder Story set
    e1 = load_e1_questions(skill_root)
    rebuild_table(doc_id, E1_HEADING, [["Question", "Rationale"]] + e1, E1_WIDTHS)

    # Episodes 2-12 + additionals - from the n-gram tables
    for slug, heading in EPISODE_HEADINGS:
        msv_map = load_keyword_msv(SLUG_PA[slug])
        rows = [["Question", "Keywords", "Rationale"]]
        for r in eps[slug]:
            kw = question_keywords_cell(r.get("ngrams", []), msv_map)
            rows.append([r["question_text"], kw, rationale_from_row(r)])
        rebuild_table(doc_id, heading, rows, QUESTION_WIDTHS)

    apply_episode_dividers(doc_id)
    print("done -> https://docs.google.com/document/d/%s/edit" % doc_id)


if __name__ == "__main__":
    main()
