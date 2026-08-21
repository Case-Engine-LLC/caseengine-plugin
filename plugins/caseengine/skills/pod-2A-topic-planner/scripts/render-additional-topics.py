#!/usr/bin/env python3
"""
render-additional-topics.py - writes the `## Additional Topics` table.

Renders the 3 swap-in candidates (one car, one truck, one other) into the
client-facing Additional Topics table of a topic-plan Google Doc.

Columns: Topic | Theme | Keywords | Rationale    widths [150,80,128,110]
(v4.4.0, 2026-05-28: the `Swaps for` column was removed - swap relationships
now live only in the INTERNAL `## Topic Ideas` Notes column.)

Usage:  python3 render-additional-topics.py <doc_id> <selection.json>

selection.json carries an `additional` array; each entry:
  {"topic": "...", "theme": "...", "keywords": "...", "rationale": "..."}
"""

import json
import sys

from lib_doc_table import rebuild_table, keywords_cell

WIDTHS = [150, 80, 128, 110]


def main():
    if len(sys.argv) != 3:
        print("usage: render-additional-topics.py <doc_id> <selection.json>",
              file=sys.stderr)
        sys.exit(1)
    doc_id, data_path = sys.argv[1], sys.argv[2]
    additional = json.load(open(data_path))["additional"]

    rows = [["Topic", "Theme", "Keywords", "Rationale"]]
    for a in additional:
        rows.append([a["topic"], a["theme"], keywords_cell(a["keywords"]),
                     a["rationale"]])
    rebuild_table(doc_id, "Additional Topics", rows, WIDTHS)


if __name__ == "__main__":
    main()
