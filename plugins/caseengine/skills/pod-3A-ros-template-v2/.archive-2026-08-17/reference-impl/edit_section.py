#!/usr/bin/env python3
"""Surgical section edits. Replace ONE section in ONE tab (or all tabs) without
touching anything else in the document. Manual edits elsewhere survive.

Usage:
  python3 edit_section.py --list
  python3 edit_section.py --list --tab "Truck Accidents (GA)"
  python3 edit_section.py --section "Introduction"                  # all tabs
  python3 edit_section.py --section "Outro Close" --tab "Birth Injury (MD)"
"""
import argparse, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import push_tabs as P
import push_v3
from topics2 import TOPICS

DOC = push_v3.DOC
P.DOC_ID = DOC
RANK = {"HEADING_1": 1, "HEADING_2": 2, "HEADING_3": 3, "TITLE": 0}


def tab_content(doc, title):
    for t in doc["tabs"]:
        if t["tabProperties"]["title"] == title:
            return t["tabProperties"]["tabId"], t["documentTab"]["body"]["content"]
    raise SystemExit(f"tab not found: {title}")


def paragraphs(content):
    """(startIndex, endIndex, namedStyleType, text) per paragraph."""
    out = []
    for e in content:
        p = e.get("paragraph")
        if not p:
            continue
        txt = "".join(x.get("textRun", {}).get("content", "") for x in p.get("elements", [])).rstrip("\n")
        out.append((e["startIndex"], e["endIndex"],
                    p.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT"), txt))
    return out


def find_section(paras, heading):
    """Return (start, end) covering the heading and everything under it.
    COVER is a special case: the cover page has no heading, so it spans from
    the top of the body to the first HEADING_1."""
    if heading.strip().upper() == "COVER":
        for (s2, _e2, st2, _t2) in paras:
            if st2 == "HEADING_1":
                return 1, s2
        return None
    for i, (s, e, style, txt) in enumerate(paras):
        if txt.strip() == heading.strip() and style in RANK:
            rank = RANK[style]
            end = paras[-1][1]
            for (s2, e2, st2, _t2) in paras[i + 1:]:
                if st2 in RANK and RANK[st2] <= rank:
                    end = s2
                    break
            return s, end
    return None


def section_blocks(t, heading):
    """Slice the freshly built block list down to just this section."""
    blocks = push_v3.blocks_for(t)
    if heading.strip().upper() == "COVER":
        for i, b in enumerate(blocks):
            if b["kind"] == "pagebreak":
                return blocks[:i]
        return blocks
    start = None
    for i, b in enumerate(blocks):
        if b["text"].strip() == heading.strip() and b["kind"] in ("h1", "h2", "h3", "pagebreak"):
            start = i
            rank = {"h1": 1, "pagebreak": 1, "h2": 2, "h3": 3}[b["kind"]]
            break
    if start is None:
        raise SystemExit(f"section not found in builder output: {heading}")
    end = len(blocks)
    for j in range(start + 1, len(blocks)):
        k = blocks[j]["kind"]
        if k in ("h1", "h2", "h3", "pagebreak") and {"h1": 1, "pagebreak": 1, "h2": 2, "h3": 3}[k] <= rank:
            end = j
            break
    return blocks[start:end]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--section")
    ap.add_argument("--tab")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--rename", help="new heading text; renames the heading only, body untouched")
    a = ap.parse_args()

    doc = P.gws("docs", "documents", "get", params={"documentId": DOC, "includeTabsContent": True})
    titles = [x["tabProperties"]["title"] for x in doc["tabs"]]
    targets = [a.tab] if a.tab else titles

    if a.list:
        for title in targets:
            _tid, content = tab_content(doc, title)
            print(f"\n### {title}")
            for (s, e, style, txt) in paragraphs(content):
                if style in RANK and txt.strip():
                    print(f"   {style:<10} [{s:>5}-{e:<5}] {txt[:70]}")
        raise SystemExit

    if not a.section:
        raise SystemExit("--section required (or --list)")

    if a.rename:
        for title in targets:
            tid, content = tab_content(doc, title)
            hit = next(((s_, e_) for (s_, e_, st, txt) in paragraphs(content)
                        if txt.strip() == a.section.strip() and st in RANK), None)
            if not hit:
                print(f"skip (heading absent): {title}"); continue
            s_, e_ = hit
            P.batch([
                {"deleteContentRange": {"range": {"startIndex": s_, "endIndex": e_ - 1, "tabId": tid}}},
                {"insertText": {"location": {"index": s_, "tabId": tid}, "text": a.rename}},
            ])
            print(f"renamed -> '{a.rename}' in {title}")
            doc = P.gws("docs", "documents", "get", params={"documentId": DOC, "includeTabsContent": True})
        raise SystemExit

    for title in targets:
        t = next((x for x in TOPICS if x["tab"] == title), None)
        if not t:
            print(f"skip (no topic data): {title}")
            continue
        tid, content = tab_content(doc, title)
        rng = find_section(paragraphs(content), a.section)
        if not rng:
            print(f"skip (section absent): {title}")
            continue
        start, end = rng
        blocks = section_blocks(t, a.section)
        P.batch([{"deleteContentRange": {"range": {"startIndex": start, "endIndex": end, "tabId": tid}}}])
        ins, styles, logo_idx = P.to_requests(blocks, tid, base=start)
        P.batch([ins]); P.batch(styles)
        if logo_idx:
            P.batch([{"insertInlineImage": {
                "location": {"index": logo_idx, "tabId": tid},
                "uri": f"https://drive.google.com/uc?export=view&id={push_v3.LOGO_ID}",
                "objectSize": {"width": {"magnitude": 180, "unit": "PT"}}}}])
        print(f"replaced '{a.section}' in {title}  ({end - start} chars -> {len(ins['insertText']['text'])})")
        # re-read so the next tab's indices are fresh
        doc = P.gws("docs", "documents", "get", params={"documentId": DOC, "includeTabsContent": True})
