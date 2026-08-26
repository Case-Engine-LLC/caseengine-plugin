#!/usr/bin/env python3
"""Build the 5 additional format-prototype tabs and push them into the existing Doc."""
import json, re, subprocess, sys, os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from topics import TOPICS

DOC_ID = "1tqEd_s3ST6L7l-rHzctKRtJKAgXfDQEwadcv9Ao50Dc"
DELIV = Path.home() / "Desktop/claude_code/deliverables"
CE_BLUE = {"red": 0.208, "green": 0.451, "blue": 1.0}
CE_DARK = {"red": 0.059, "green": 0.090, "blue": 0.165}
CE_GRAY = {"red": 0.392, "green": 0.455, "blue": 0.545}

INLINE = re.compile(r"(\[[^\]]+\]\{\.underline\}|\*\*[^*]+\*\*|\*[^*]+\*)")


def runs(text):
    """Split text into (text, bold, italic, underline) runs."""
    out = []
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("[") and part.endswith("{.underline}"):
            out.append((part[1:part.index("]{")], False, False, True))
        elif part.startswith("**"):
            out.append((part[2:-2], True, False, False))
        elif part.startswith("*"):
            out.append((part[1:-1], False, True, False))
        else:
            out.append((part, False, False, False))
    return out


def B(kind, text):
    return {"kind": kind, "text": text}


def build_blocks(t):
    """Emit the ordered block list for one topic tab."""
    b = []
    b.append(B("h1", f"Run of Show: {t['title']}"))
    b.append(B("gray", f"Format: Open Interview + Location Blocks (PROTOTYPE)  |  {t['practice_area']}  |  {t['scope_label']}"))
    b.append(B("gray", f"Episode: **{{{{EPISODE_NUMBER}}}}**  |  Recording Date: **{{{{RECORDING_DATE}}}}**  |  Attorney: **{{{{ATTORNEY_NAME}}}}**, **{{{{FIRM_NAME}}}}**"))
    b.append(B("gray", f"Total runtime: {t['runtime']}"))

    b.append(B("h2", "How This Episode Runs"))
    b.append(B("p", "Two modes, recorded differently on purpose. Tell the attorney which mode you are in before each one. If they perform both the same way, the format does not work."))
    b.append(B("p", "**Mode 1 - The Interview (~25 min).** A real conversation. Prompts, not questions. The interviewer follows the answer wherever it goes and skips anything the conversation already covered. Long answers are good. Stories are better."))
    b.append(B("p", "**Mode 2 - Location Blocks (~7 min each).** One city at a time. Each answer is standalone, restates the question, and names the city, because each one gets cut out and used on its own. No callbacks to the interview. Reset between questions."))
    b.append(B("p", "**Standing Follow-Ups apply here too.** The full Proof Prompts set lives on the first tab. The three that do the most work: \"Is there one you can talk about where that's exactly what happened?\", \"What did the other side think it was worth at the start?\", and \"Walk me through one.\""))

    b.append(B("h2", "Producer Notes"))
    b.append(B("p", f"**Jurisdiction:** {t['jurisdiction']}"))
    b.append(B("p", "**About the attorney:** **{{ATTORNEY_NAME}}** at **{{FIRM_NAME}}**. Website **{{WEBSITE}}**."))

    b.append(B("h2", "Introduction (~3 minutes)"))
    b.append(B("i", "[Interviewer]"))
    b.append(B("p", "Welcome back to **{{PODCAST_NAME}}**. I'm **{{HOST_NAME}}**, here with **{{ATTORNEY_NAME}}** from **{{FIRM_NAME}}**."))
    b.append(B("i", "[Interviewer]"))
    b.append(B("p", f"**{{{{ATTORNEY_FIRST_NAME}}}}**, {t['intro']}"))
    b.append(B("i", f"{t['framing']}"))
    b.append(B("i", "Go straight into Prompt 1. No segment announcement."))

    b.append(B("h1", "The Interview (~25 minutes)"))
    b.append(B("i", "Prompts, not questions. Every one hands the floor to the attorney and holds it there. The ground bullets are what the answer should reach, never a script to read. Skipping a prompt the conversation already covered is correct behavior."))
    for i, p in enumerate(t["prompts"], 1):
        b.append(B("h3", f"Prompt {i}: {p['t']}"))
        b.append(B("i", "[Interviewer]"))
        b.append(B("p", f"**{p['q']}**"))
        b.append(B("i", "[Attorney Response]"))
        b.append(B("i", "Open answer. Let it run. Ground worth reaching:"))
        for g in p["g"]:
            b.append(B("bullet", g))
        if p.get("story"):
            b.append(B("i", "This is the story prompt of the episode. Give it room and do not rush the follow-ups."))
        b.append(B("i", "[Interviewer - follow-ups, use as needed]"))
        for f in p["f"]:
            b.append(B("bullet", f))

    b.append(B("h1", "Location Blocks"))
    b.append(B("i", "Mode switch. Say it on mic. Each answer is standalone, 60 to 90 seconds, restates the question, names the city. No follow-ups, no callbacks. These can be retaken - if one comes out flat, do it again."))
    for blk in t["blocks"]:
        b.append(B("h2", f"Location Block: {blk['city']} (~7 minutes)"))
        for j, q in enumerate(blk["qs"], 1):
            b.append(B("h3", f"{q['q']}"))
            b.append(B("i", "[Attorney Response]"))
            for bl in q["b"]:
                b.append(B("bullet", bl))

    b.append(B("h2", "Closing and Call to Action (~4 minutes)"))
    b.append(B("i", "[Interviewer]"))
    b.append(B("p", f"**{t['closing_q']}**"))
    b.append(B("i", "[Attorney Response]"))
    b.append(B("i", "Open answer. A final thought, not a recap of the episode."))
    b.append(B("i", "[Interviewer]"))
    b.append(B("p", "You can reach **{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**."))

    # Source bank
    rows = json.load(open(DELIV / t["ngram"]))["content"]["rows"]
    b.append(B("h1", "Appendix: Source Question Bank"))
    b.append(B("i", f"All {len(rows)} questions verbatim from the episode's N-Gram Table, unedited. INTERNAL. Audit trail that nothing was dropped or invented, and the live pull pool if a client rejects a Location Block question. Note the phrasing: these are query strings, which is right for the Blocks and wrong for the Interview. The gap between a row below and the Interview prompt built from the same substance is the whole format change."))
    for i, r in enumerate(rows, 1):
        b.append(B("bullet", f"**{i}.** {r['question_text']}"))
    b.append(B("gray", f"Source: {t['ngram']}"))
    b.append(B("gray", f"Entity map: {t['emap']}"))
    return b


def to_requests(blocks, tab_id, base=1):
    """Return (insertText request, styling requests)."""
    text = ""
    spans = []          # (start, end, kind, raw)
    for blk in blocks:
        plain = "".join(r[0] for r in runs(blk["text"]))
        start = len(text)
        text += plain + "\n"
        spans.append((start, start + len(plain), blk["kind"], blk["text"]))

    reqs = []
    NAMED = {"h1": "HEADING_1", "h2": "HEADING_2", "h3": "HEADING_3", "ctitle": "TITLE", "pagebreak": "HEADING_1"}
    bullet_groups = []
    cur = None
    for (s, e, kind, raw) in spans:
        if kind in ("bullet", "bullet-sub"):
            cur = [s, e] if cur is None else [cur[0], e]
        elif cur is not None:
            bullet_groups.append(cur); cur = None
    if cur is not None:
        bullet_groups.append(cur)

    for (s, e, kind, raw) in spans:

        named = NAMED.get(kind, "NORMAL_TEXT")
        pstyle = {"namedStyleType": named,
                  "spaceAbove": {"magnitude": 10 if kind in ("h1", "h2", "h3", "pagebreak") else 3, "unit": "PT"},
                  "spaceBelow": {"magnitude": 4, "unit": "PT"}}
        fields = "namedStyleType,spaceAbove,spaceBelow"
        if kind == "bullet-sub":
            pstyle["indentStart"] = {"magnitude": 54, "unit": "PT"}; fields += ",indentStart"
        if kind.startswith("c") and kind != "code":
            pstyle["alignment"] = "CENTER"; fields += ",alignment"
        # ALWAYS set explicitly - inserted paragraphs otherwise inherit
        # pageBreakBefore from whatever was at that index.
        pstyle["pageBreakBefore"] = (kind == "pagebreak")
        fields += ",pageBreakBefore"
        reqs.append({"updateParagraphStyle": {
            "range": {"startIndex": base + s, "endIndex": base + e + 1, "tabId": tab_id},
            "paragraphStyle": pstyle, "fields": fields}})

        # base text style for the whole paragraph
        style = {"weightedFontFamily": {"fontFamily": "Roboto"}}
        fields = ["weightedFontFamily"]
        if kind in ("h1", "pagebreak"):
            style.update({"fontSize": {"magnitude": 20, "unit": "PT"}, "bold": True,
                          "foregroundColor": {"color": {"rgbColor": CE_BLUE}}})
            fields += ["fontSize", "bold", "foregroundColor"]
        elif kind == "h2":
            style.update({"fontSize": {"magnitude": 16, "unit": "PT"}, "bold": True,
                          "foregroundColor": {"color": {"rgbColor": CE_DARK}}})
            fields += ["fontSize", "bold", "foregroundColor"]
        elif kind == "h3":
            style.update({"fontSize": {"magnitude": 13, "unit": "PT"}, "bold": True,
                          "foregroundColor": {"color": {"rgbColor": CE_DARK}}})
            fields += ["fontSize", "bold", "foregroundColor"]
        elif kind == "rule":
            style.update({"fontSize": {"magnitude": 11, "unit": "PT"},
                          "foregroundColor": {"color": {"rgbColor": CE_GRAY}}})
            fields += ["fontSize", "foregroundColor"]
        elif kind == "pb":
            style.update({"fontSize": {"magnitude": 11, "unit": "PT"}, "bold": True,
                          "foregroundColor": {"color": {"rgbColor": CE_DARK}}})
            fields += ["fontSize", "bold", "foregroundColor"]
        elif kind == "ctitle":
            # CE deliverable cover spec: CE Blue 24pt bold
            style.update({"fontSize": {"magnitude": 24, "unit": "PT"}, "bold": True,
                          "foregroundColor": {"color": {"rgbColor": CE_BLUE}}})
            fields += ["fontSize", "bold", "foregroundColor"]
        elif kind == "csub":
            # bible spec: dark 18pt bold
            style.update({"fontSize": {"magnitude": 18, "unit": "PT"}, "bold": True,
                          "foregroundColor": {"color": {"rgbColor": CE_DARK}}})
            fields += ["fontSize", "bold", "foregroundColor"]
        elif kind == "cloc":
            # bible spec: dark 14pt normal
            style.update({"fontSize": {"magnitude": 14, "unit": "PT"},
                          "foregroundColor": {"color": {"rgbColor": CE_DARK}}})
            fields += ["fontSize", "foregroundColor"]
        elif kind in ("cmeta", "clogo"):
            # bible spec: dark 11pt normal
            style.update({"fontSize": {"magnitude": 11, "unit": "PT"},
                          "foregroundColor": {"color": {"rgbColor": CE_DARK}}})
            fields += ["fontSize", "foregroundColor"]
        elif kind == "gray":
            style.update({"fontSize": {"magnitude": 10, "unit": "PT"}, "italic": True,
                          "foregroundColor": {"color": {"rgbColor": CE_GRAY}}})
            fields += ["fontSize", "italic", "foregroundColor"]
        elif kind == "i":
            style.update({"fontSize": {"magnitude": 11, "unit": "PT"}, "italic": True,
                          "foregroundColor": {"color": {"rgbColor": CE_GRAY}}})
            fields += ["fontSize", "italic", "foregroundColor"]
        else:
            style.update({"fontSize": {"magnitude": 11, "unit": "PT"},
                          "foregroundColor": {"color": {"rgbColor": CE_DARK}}})
            fields += ["fontSize", "foregroundColor"]
        if e > s:
            reqs.append({"updateTextStyle": {
                "range": {"startIndex": base + s, "endIndex": base + e, "tabId": tab_id},
                "textStyle": style, "fields": ",".join(fields)}})

        # inline runs
        off = s
        for (txt, bo, it, un) in runs(raw):
            if txt and (bo or un):
                ts, fl = {}, []
                if bo:
                    ts["bold"] = True; fl.append("bold")
                if un:
                    ts["underline"] = True; fl.append("underline")
                reqs.append({"updateTextStyle": {
                    "range": {"startIndex": base + off, "endIndex": base + off + len(txt), "tabId": tab_id},
                    "textStyle": ts, "fields": ",".join(fl)}})
            off += len(txt)

    # bullets applied last so paragraph-style writes do not clear them
    for (s, e) in bullet_groups:
        reqs.append({"createParagraphBullets": {
            "range": {"startIndex": base + s, "endIndex": base + e + 1, "tabId": tab_id},
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}})
    logo_idx = None
    for (s_, e_, kind, raw) in spans:
        if kind == "clogo":
            logo_idx = base + s_
            break
    return ({"insertText": {"location": {"index": base, "tabId": tab_id}, "text": text}},
            reqs, logo_idx)


def gws(*args, body=None, params=None):
    cmd = ["gws", *args]
    if params:
        cmd += ["--params", json.dumps(params)]
    if body is not None:
        cmd += ["--json", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAILED: {' '.join(args)}\n{r.stdout}\n{r.stderr}")
    out = r.stdout.strip()
    out = out[out.index("{"):] if "{" in out else out
    return json.loads(out) if out else {}


def batch(requests):
    for i in range(0, len(requests), 400):
        gws("docs", "documents", "batchUpdate", params={"documentId": DOC_ID},
            body={"requests": requests[i:i + 400]})


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("tabs", "all"):
        reqs = [{"addDocumentTab": {"tabProperties": {"title": t["tab"], "iconEmoji": t["emoji"], "index": i + 1}}}
                for i, t in enumerate(TOPICS)]
        batch(reqs)
        print("tabs created")

    doc = gws("docs", "documents", "get", params={"documentId": DOC_ID, "includeTabsContent": True})
    tabs = {t["tabProperties"]["title"]: t["tabProperties"]["tabId"] for t in doc.get("tabs", [])}
    print(json.dumps(tabs, indent=1))

    if mode in ("fill", "all"):
        for t in TOPICS:
            tid = tabs[t["tab"]]
            ins, styles = to_requests(build_blocks(t), tid)
            batch([ins])
            batch(styles)
            print(f"filled: {t['tab']} ({len(styles)} style reqs)")
