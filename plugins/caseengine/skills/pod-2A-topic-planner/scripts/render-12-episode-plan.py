#!/usr/bin/env python3
"""
render-12-episode-plan.py - writes the `## The 12-Episode Plan` table.

Renders the curated 12 episodes (Episode 1 Founder Interview + 11 thematic)
into the client-facing 12-Episode Plan table of a topic-plan Google Doc.

Columns: #  |  Topic  |  Theme  |  Keywords  |  Rationale     widths [32,134,70,116,116]

Usage:  python3 render-12-episode-plan.py <doc_id> <selection.json>

selection.json carries an `episodes` array; each entry:
  {"n": 1, "topic": "...", "theme": "...", "keywords": "...", "rationale": "..."}
The `keywords` cell may contain a newline: line 1 the total search demand,
line 2 the comma-separated keyword list.
"""

import json
import re
import sys

from lib_doc_table import rebuild_table, get_doc, batch, keywords_cell

WIDTHS = [32, 134, 70, 116, 116]


def sync_episode_breakdown_headings(doc_id, episodes):
    """Sync the `## Episode Breakdown` per-episode H3 headings to the selected
    episode names. Episodes 2-12 use the episode topic; Episode 1 keeps the
    theme heading `Episode 1: Founder Story` (the E1 exception)."""
    by_n = {e["n"]: e for e in episodes}
    doc = get_doc(doc_id)
    updates = []
    for el in doc["body"]["content"]:
        if "paragraph" not in el:
            continue
        st = el["paragraph"].get("paragraphStyle", {}).get("namedStyleType", "")
        if st != "HEADING_3":
            continue
        txt = "".join(r.get("textRun", {}).get("content", "")
                      for r in el["paragraph"].get("elements", []))
        m = re.match(r"\s*Episode (\d+):", txt)
        if not m:
            continue
        n = int(m.group(1))
        if n not in by_n:
            continue
        new = ("Episode 1: Founder Story" if n == 1
               else "Episode %d: %s" % (n, by_n[n]["topic"]))
        updates.append((el["startIndex"], el["endIndex"] - 1, new))
    reqs = []
    for s, e, new in sorted(updates, key=lambda x: -x[0]):
        if e > s:
            reqs.append({"deleteContentRange": {
                "range": {"startIndex": s, "endIndex": e}}})
        reqs.append({"insertText": {"location": {"index": s}, "text": new}})
    if reqs:
        batch(doc_id, reqs)
    print("synced %d Episode Breakdown headings" % len(updates))


def main():
    if len(sys.argv) != 3:
        print("usage: render-12-episode-plan.py <doc_id> <selection.json>",
              file=sys.stderr)
        sys.exit(1)
    doc_id, data_path = sys.argv[1], sys.argv[2]
    episodes = json.load(open(data_path))["episodes"]

    rows = [["#", "Topic", "Theme", "Keywords", "Rationale"]]
    for e in sorted(episodes, key=lambda x: x["n"]):
        rows.append([str(e["n"]), e["topic"], e["theme"],
                     keywords_cell(e["keywords"]), e["rationale"]])
    rebuild_table(doc_id, "The 12-Episode Plan", rows, WIDTHS)
    sync_episode_breakdown_headings(doc_id, episodes)


if __name__ == "__main__":
    main()
