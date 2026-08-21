#!/usr/bin/env python3
"""
lib_doc_table - shared helper for the pod-2A-topic-planner per-table render scripts.

Not run directly. Imported by:
  - render-12-episode-plan.py     -> writes ## The 12-Episode Plan
  - render-additional-topics.py   -> writes ## Additional Topics
  - render-topic-ideas.py     -> writes ## Topics > ### Topic Ideas

`rebuild_table` deletes the table that follows a given heading in a Google Doc
and rebuilds it: insert a fresh table, populate every cell, brand it (CE Blue
header row, zebra body rows, Roboto 9pt, fixed column widths).
"""

import json
import subprocess
import sys

CE_BLUE = {"red": 0.20784314, "green": 0.4509804, "blue": 1.0}
ZEBRA   = {"red": 0.9607843, "green": 0.96862745, "blue": 0.98039216}
WHITE   = {"red": 1.0, "green": 1.0, "blue": 1.0}
INK     = {"red": 0.05882353, "green": 0.09019608, "blue": 0.16470589}


def gws(args, body=None):
    cmd = ["gws"] + args
    if body is not None:
        cmd += ["--json", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if "{" not in r.stdout:
        print("gws error:", r.stderr or r.stdout, file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout[r.stdout.index("{"):])


def get_doc(doc_id):
    return gws(["docs", "documents", "get", "--params",
                json.dumps({"documentId": doc_id})])


def batch(doc_id, reqs):
    for i in range(0, len(reqs), 200):
        gws(["docs", "documents", "batchUpdate", "--params",
             json.dumps({"documentId": doc_id})],
            body={"requests": reqs[i:i + 200]})


def _color(rgb):
    return {"color": {"rgbColor": rgb}}


def keywords_cell(kw):
    """Build the canonical Keywords-column cell string from structured data.

    LOCKED FORMAT - the render scripts call this so the cell is correct every
    run, never hand-authored:
        line 1 : "{total}/mo Total Search Demand"   (comma-grouped thousands)
        line 2 : "keyword - X/mo, keyword - X/mo, ..."  (highest MSV first)

    `kw` is {"total": int, "label": str (optional), "list": [[query, msv], ...]}.
    `label` defaults to "Total Search Demand"; Episode 1 passes
    "Total Branded Search Demand".
    """
    total = kw.get("total", 0)
    label = kw.get("label") or "Total Search Demand"
    pairs = sorted(kw.get("list", []), key=lambda p: -p[1])
    line2 = ", ".join("%s - %s/mo" % (q, format(int(m), ",")) for q, m in pairs)
    return "%s/mo %s\n%s" % (format(int(total), ","), label, line2)


def find_table_after(doc, heading_text):
    """Return the table element that follows the given heading."""
    seen = False
    for el in doc["body"]["content"]:
        if "paragraph" in el:
            txt = "".join(r.get("textRun", {}).get("content", "")
                          for r in el["paragraph"].get("elements", [])).strip()
            st = el["paragraph"].get("paragraphStyle", {}).get("namedStyleType", "")
            if txt == heading_text and "HEADING" in st:
                seen = True
        if "table" in el and seen:
            return el
    raise RuntimeError("no table found after heading %r" % heading_text)


def rebuild_table(doc_id, heading_text, rows, widths):
    """Delete the table after `heading_text`, rebuild it from `rows`, brand it.

    rows    : list of row lists (row 0 is the header).
    widths  : per-column fixed widths in points; len(widths) == column count.
    """
    nrows, ncols = len(rows), len(rows[0])
    if len(widths) != ncols:
        raise ValueError("widths has %d entries, table has %d columns"
                         % (len(widths), ncols))

    doc = get_doc(doc_id)
    old = find_table_after(doc, heading_text)
    t_start, t_end = old["startIndex"], old["endIndex"]

    batch(doc_id, [{"deleteContentRange": {"range": {
        "startIndex": t_start, "endIndex": t_end}}}])
    batch(doc_id, [{"insertTable": {"rows": nrows, "columns": ncols,
                                    "location": {"index": t_start}}}])

    # populate cells, highest index first so earlier inserts do not shift later
    doc = get_doc(doc_id)
    tbl = next(el for el in doc["body"]["content"]
               if "table" in el and el["startIndex"] >= t_start)
    inserts = []
    for r, row in enumerate(tbl["table"]["tableRows"]):
        for c, cell in enumerate(row["tableCells"]):
            idx = cell["content"][0]["startIndex"]
            txt = str(rows[r][c])
            if txt:
                inserts.append((idx, txt))
    inserts.sort(key=lambda x: -x[0])
    batch(doc_id, [{"insertText": {"location": {"index": i}, "text": t}}
                   for i, t in inserts])

    # brand
    doc = get_doc(doc_id)
    tbl_el = next(el for el in doc["body"]["content"]
                  if "table" in el and el["startIndex"] >= t_start)
    tbl = tbl_el["table"]
    loc = {"index": tbl_el["startIndex"]}

    def crange(row, rowspan=1):
        return {"tableCellLocation": {"tableStartLocation": loc,
                                      "rowIndex": row, "columnIndex": 0},
                "rowSpan": rowspan, "columnSpan": ncols}

    sreqs = [{"updateTableCellStyle": {
        "tableRange": crange(0, nrows),
        "tableCellStyle": {"backgroundColor": _color(WHITE),
                           "paddingTop": {"magnitude": 2, "unit": "PT"},
                           "paddingBottom": {"magnitude": 2, "unit": "PT"},
                           "paddingLeft": {"magnitude": 6, "unit": "PT"},
                           "paddingRight": {"magnitude": 6, "unit": "PT"}},
        "fields": "backgroundColor,paddingTop,paddingBottom,paddingLeft,paddingRight"}},
        {"updateTableCellStyle": {
            "tableRange": crange(0, 1),
            "tableCellStyle": {"backgroundColor": _color(CE_BLUE)},
            "fields": "backgroundColor"}}]
    for r in range(2, nrows, 2):
        sreqs.append({"updateTableCellStyle": {
            "tableRange": crange(r, 1),
            "tableCellStyle": {"backgroundColor": _color(ZEBRA)},
            "fields": "backgroundColor"}})
    for r, row in enumerate(tbl["tableRows"]):
        for cell in row["tableCells"]:
            for para in cell["content"]:
                if "paragraph" not in para:
                    continue
                s, e = para["startIndex"], para["endIndex"] - 1
                if e <= s:
                    continue
                sreqs.append({"updateTextStyle": {
                    "range": {"startIndex": s, "endIndex": e},
                    "textStyle": {
                        "weightedFontFamily": {"fontFamily": "Roboto", "weight": 400},
                        "fontSize": {"magnitude": 9, "unit": "PT"},
                        "bold": r == 0,
                        "foregroundColor": _color(WHITE if r == 0 else INK)},
                    "fields": "weightedFontFamily,fontSize,bold,foregroundColor"}})
    for c, w in enumerate(widths):
        sreqs.append({"updateTableColumnProperties": {
            "tableStartLocation": loc, "columnIndices": [c],
            "tableColumnProperties": {"widthType": "FIXED_WIDTH",
                                      "width": {"magnitude": w, "unit": "PT"}},
            "fields": "widthType,width"}})
    batch(doc_id, sreqs)

    # Remove empty paragraphs that accumulate immediately before the table -
    # insertTable adds a leading newline on every rebuild, so without this the
    # gap above the table grows each run. Leaves the table flush under the
    # heading (or its intro paragraph).
    doc = get_doc(doc_id)
    els = doc["body"]["content"]
    ti = next(i for i, e in enumerate(els)
              if "table" in e and e["startIndex"] >= t_start)
    blanks = []
    j = ti - 1
    while j >= 0 and "paragraph" in els[j]:
        txt = "".join(r.get("textRun", {}).get("content", "")
                      for r in els[j]["paragraph"].get("elements", [])).strip()
        if txt == "":
            blanks.append((els[j]["startIndex"], els[j]["endIndex"]))
            j -= 1
        else:
            break
    for s, e in sorted(blanks, key=lambda x: -x[0]):
        batch(doc_id, [{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}}])
    print("rebuilt %r: %d rows x %d cols (cleaned %d blank paras)"
          % (heading_text, nrows, ncols, len(blanks)))
