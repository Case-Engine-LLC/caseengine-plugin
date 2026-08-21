#!/usr/bin/env python3
"""
render-topic-ideas.py - writes the INTERNAL `### Topic Ideas` table.

Renders every scored candidate topic, in raw authority_score order, into the
INTERNAL Topic Ideas table of a topic-plan Google Doc.

Columns: Rank | Topic | Theme | Score | Rationale | Notes   widths [32,176,74,46,90,50]
  - Score : the weighted authority_score to 3 decimals.
  - Notes : disposition written at episode selection (MAIN-#, BONUS, RESERVE, CUT).

Usage:  python3 render-topic-ideas.py <doc_id> <topics-by-score.json>

topics-by-score.json shape:
  {"header": ["Rank","Topic","Theme","Score","Rationale","Notes"],
   "rows": [[...], [...], ...]}
"""

import json
import sys

from lib_doc_table import rebuild_table

WIDTHS = [32, 176, 74, 46, 90, 50]


def main():
    if len(sys.argv) != 3:
        print("usage: render-topic-ideas.py <doc_id> <topics-by-score.json>",
              file=sys.stderr)
        sys.exit(1)
    doc_id, data_path = sys.argv[1], sys.argv[2]
    data = json.load(open(data_path))

    rows = [data["header"]] + data["rows"]
    rebuild_table(doc_id, "Topic Ideas", rows, WIDTHS)


if __name__ == "__main__":
    main()
