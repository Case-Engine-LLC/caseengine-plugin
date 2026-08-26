#!/usr/bin/env python3
"""v3 rebuild - overwrite each tab of the existing v2 doc in place."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import push_tabs as P
from topics3 import V3, ATTRIBUTES, ATTR_SOURCES, ALT_INTROS, s2_v4, REGION, STATIC
from topics2 import TOPICS

LOGO_ID = "1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2"   # CE logo, per the CE deliverable cover spec
DOC = "1Bv-EWc7HBtKqc09XEfQnBIfSOdm6m4Tc-kJNw5uKErk"
P.DOC_ID = DOC
B = P.B


def blocks_for(t):
    v = V3[t["tab"]]
    b = []

    # ---------- COVER PAGE (CE deliverable cover spec) ----------
    b.append(B("cmeta", " "))          # spacer1
    b.append(B("clogo", " "))          # spacer2 - CE logo inserted here
    b.append(B("cmeta", " "))          # spacer3
    b.append(B("ctitle", "Run of Show"))
    b.append(B("csub", t["title"]))
    b.append(B("cmeta", " "))
    b.append(B("cloc", "Topic: **{{PRACTICE_AREA}}**"))
    b.append(B("cloc", "Location: **{{LOCATION}}**"))
    b.append(B("cmeta", " "))
    b.append(B("cmeta", "Prepared by Case Engine"))
    b.append(B("cmeta", "**{{RECORDING_DATE}}**"))

    # ---------- SEGMENT 1 ----------
    b.append(B("pagebreak", "S1: Long-Form (15-30m)"))

    b.append(B("h2", "Introduction"))
    b.append(B("i", "INTERVIEWER"))
    b.append(B("p", STATIC["welcome"].replace("{topic_phrase}", v["topic_phrase"])))
    b.append(B("pb", STATIC["prompt_template"].replace("[VICTIMS]", v["victims"]).replace("[SITUATION]", v["situation"])))
    b.append(B("i", "ATTORNEY"))
    b.append(B("i", STATIC["handoff"]))

    b.append(B("i", "Alternate introductions - swap any of these in for the welcome above."))
    for label, body in ALT_INTROS:
        b.append(B("bullet", f"**{label}.** {body}"))

    b.append(B("h2", "Attributes to Hit"))
    b.append(B("i", STATIC["attr_intro"]))
    for name, detail in ATTRIBUTES:
        b.append(B("bullet", f"**{name}.** {detail}"))

    # ----- internal notes, below the divider -----
    b.append(B("rule", "___________________________________________________________"))
    b.append(B("h3", "Internal Notes (not read on air)"))
    b.append(B("i", STATIC["answer_header"]))
    b.append(B("i", STATIC["answer_intro"]))
    b.append(B("bullet", STATIC["move_1"]))
    b.append(B("bullet", STATIC["move_2"]))
    b.append(B("bullet", f"**Real examples.** {v['examples']}"))
    b.append(B("i", STATIC["attr_note_internal"]))
    b.append(B("i", STATIC["attr_sources_internal"]))
    for n, src in ATTR_SOURCES:
        b.append(B("bullet", f"**{n}** - {src}"))
    b.append(B("i", "What to cover in the second move:"))
    for n in v["need_to_know"]:
        b.append(B("bullet", n))


    # ---------- SEGMENT 2 ----------
    b.append(B("pagebreak", "S2: Short-Form (60-90s)"))
    b.append(B("i", STATIC["shortform_mode"]))
    b.append(B("i", STATIC["shortform_sets"]))
    # One tokenized set. Additional locations are additional copies of this set,
    # each populated with that location - see the static note above.
    for bi in (1,):
        qs = s2_v4(t["tab"])
        b.append(B("h2", "Location Set: **{{LOCATION}}**"))
        for qi, (q, kind, note) in enumerate(qs, 1):
            b.append(B("bullet", f"**Q{qi}:** {q}"))

    b.append(B("h2", "Outro Close"))
    b.append(B("i", STATIC["outro_note"]))
    b.append(B("i", "INTERVIEWER"))
    b.append(B("p", STATIC["outro_thanks"]))
    b.append(B("p", STATIC["outro_plug"]))
    b.append(B("p", STATIC["outro_signoff"]))

    b.append(B("pagebreak", "Appendix: Source Question Bank"))
    b.append(B("i", "The episode's N-Gram Table, verbatim. INTERNAL. In v3 this is reference rather than script: Segment 2 questions were rebuilt around search phrasing and attributes, not lifted from here. Kept as the audit trail and the pull pool."))
    rows = json.load(open(P.DELIV / t["ngram"]))["content"]["rows"] if hasattr(P, "DELIV") else []
    if not rows:
        from pathlib import Path
        rows = json.load(open(Path.home() / "Desktop/claude_code/deliverables" / t["ngram"]))["content"]["rows"]
    for i, r in enumerate(rows, 1):
        b.append(B("bullet", f"**{i}.** {r['question_text']}"))
    return b


if __name__ == "__main__":
    d = P.gws("docs", "documents", "get", params={"documentId": DOC, "includeTabsContent": True})
    for tab in d["tabs"]:
        title = tab["tabProperties"]["title"]
        tid = tab["tabProperties"]["tabId"]
        t = [x for x in TOPICS if x["tab"] == title]
        if not t:
            continue
        t = t[0]
        content = tab["documentTab"]["body"]["content"]
        end = content[-1]["endIndex"]
        if end > 2:
            P.batch([{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end - 1, "tabId": tid}}}])
        ins, styles, logo_idx = P.to_requests(blocks_for(t), tid)
        P.batch([ins]); P.batch(styles)
        if logo_idx:
            P.batch([{"insertInlineImage": {
                "location": {"index": logo_idx, "tabId": tid},
                "uri": f"https://drive.google.com/uc?export=view&id={LOGO_ID}",
                "objectSize": {"width": {"magnitude": 180, "unit": "PT"}}}}])
        print("rebuilt:", title)
    print(f"https://docs.google.com/document/d/{DOC}/edit")
