#!/usr/bin/env python3
"""Mechanical gate runner for a v2 ROS Template.

Runs against BOTH the payload JSON and the rendered markdown, because some gates
are about data shape and some are about what actually reaches the page.
Exit 0 = clean. Exit 1 = at least one FAIL.

    python3 qa.py --data X.json --md X.md
"""
import argparse, json, pathlib, re, sys

TOKENS = {"{{PODCAST_NAME}}", "{{ATTORNEY_NAME}}", "{{ATTORNEY}}", "{{INTERVIEWER}}",
          "{{FIRM_NAME}}", "{{PHONE_NUMBER}}", "{{WEBSITE}}", "{{YEARS_PRACTICING}}"}

RETIRED = ["How This Episode Runs", "Producer Notes", "The Lead-In", "The Prompt",
           "Interviewer: Live Checklist", "Co-Host Notes", "Geo Rule",
           "Internal Notes", "Attributes to Hit", "Alternate introductions"]

GUEST = ["my guest", "our guest", "today's guest", "joining us", "thanks for coming on",
         "welcome to the show", "thank you for coming on"]

# Hard jargon. Anything here above the Appendix is a fail, no adjudication.
JARGON_HARD = [
    r"§", r"\bO\.C\.G\.A", r"\bFla\.\s*Stat", r"\bF\.S\.\s*§?\s*\d", r"\bHB\s*\d{2,}",
    r"\b[A-Z][a-z]+ v\. [A-Z][a-z]+", r"\bdaubert\b", r"\bmcs-?90\b",
    r"\bduty of care\b", r"\bconstructive notice\b", r"\bres ipsa\b",
    r"\bnegligence per se\b", r"\brespondeat superior\b", r"\bproximate cause\b",
    r"\bdangerous instrumentality\b", r"\bcomparative negligence\b",
    r"\bsovereign immunity\b", r"\bnegligent entrustment\b", r"\bvicarious liability\b",
    r"\bstatute of limitations\b", r"\bdram shop\b", r"\bimplied consent\b",
    r"\bself-insured retention\b", r"\breservation.of.rights\b",
    r"\bsurvival action\b", r"\bstrict liability\b", r"\bnon-?economic damages\b",
    r"\bcontributory\b", r"\bjoint and several\b", r"\btort reform\b",
    r"\b\d{3}\.\d{2,}\b",
]


# US English. The documents are spoken by American attorneys to American listeners,
# and a Britishism is an immediate tell. Scoped above the appendix; the appendix is
# verbatim research and is never edited to make a scan pass.
BRITISH = [
    r"\blicence\b", r"\bdefence\b", r"\boffence\b", r"\bfavour", r"\bcolour",
    r"\bhonour", r"\blabour", r"\bneighbour", r"\bcentre\b", r"\bmetre\b",
    r"\borganis", r"\brealis", r"\brecognis", r"\bapologis", r"\banalys",
    r"\bcatalogue\b", r"\bprogramme\b", r"\btravell", r"\bmodell", r"\bfuell",
    r"\bsignall", r"\bjudgement\b", r"\bstorey\b", r"\btyre\b", r"\bkerb\b",
    r"\bgrey\b", r"\bcheque\b", r"\bpractise\b", r"\bprising\b", r"\blearnt\b",
    r"\bspelt\b", r"\bdreamt\b", r"\bburnt\b", r"\bspoilt\b", r"\bamongst\b",
    r"\bwhilst\b", r"\bamidst\b", r"\bafterwards\b", r"\btowards\b",
    r"\bbackwards\b", r"\bforwards\b", r"\bpavement\b", r"\bmotorway\b",
    r"\bcar park\b", r"\bwindscreen\b", r"\blorry\b", r"\bpetrol\b",
    r"\bsolicitor\b", r"\bbarrister\b", r"\bfortnight\b", r"\broundabout\b",
    r"\bcaught out\b", r"\bat speed\b", r"\bwork(ed|s)? out (that|who|how|what)\b",
    r"\bin hospital\b", r"\bat university\b", r"\bstraight away\b",
    r"\bin future\b", r"\bdifferent to\b", r"\btake a decision\b",
    r"\bdisbursement", r"\bpublic body\b", r"\bon the phone to\b", r"\breckon\b",
    # collective nouns take a singular verb in US English
    r"\bthe family are\b", r"\bthe firm are\b", r"\bthe company are\b",
    r"\bthe jury are\b", r"\bthe team are\b", r"\bthe government are\b",
]

DASHES = ["—", "–"]

results = []
def gate(name, ok, detail=""):
    results.append((name, ok, detail))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--md", required=True)
    a = ap.parse_args()
    d = json.loads(pathlib.Path(a.data).read_text())
    md = pathlib.Path(a.md).read_text()

    # ---- split the rendered doc -------------------------------------------
    ai = md.find("# Appendix")
    if ai < 0:
        ai = len(md)
    above, appendix = md[:ai], md[ai:]
    s2i = above.find("# S2:")
    s1, s2 = above[:s2i], above[s2i:] if s2i > 0 else ""
    oi = s1.find("## Outro")
    outro_txt = s1[oi:] if oi > 0 else ""

    # ---- schema -----------------------------------------------------------
    import jsonschema
    schema = json.loads((pathlib.Path.home() /
        ".claude/skills/pod-3A-ros-template-v2/references/schema/ros-template-v2.json").read_text())
    try:
        jsonschema.validate(d, schema)
        gate("SCHEMA", True, "validates against ros-template-v2.json")
    except jsonschema.ValidationError as e:
        gate("SCHEMA", False, f"{list(e.absolute_path)}: {e.message[:160]}")

    # ---- introduction -----------------------------------------------------
    st = d["static"]["welcome"]
    gate("IN-2 welcome verbatim", st in md, "static welcome renders byte-identical")
    s1d = d["segment_1"]
    intro = " ".join([st, s1d["setup"], s1d["credential"], s1d["prompt"]])
    wc = len(re.sub(r"\*\*|\{\{|\}\}", " ", intro).split())
    gate("IN-8 intro 80-110 words", 80 <= wc <= 110, f"{wc} words")
    sents = [x for x in re.split(r"(?<=[.!?])\s+", s1d["prompt"].strip()) if x]
    gate("IN-6 prompt is 3 sentences", len(sents) == 3, f"{len(sents)}: {sents}")
    gate("IN-6 prompt not one compound question", s1d["prompt"].count("?") == 0,
         f"{s1d['prompt'].count('?')} question marks")

    # ---- attributes -------------------------------------------------------
    at = s1d["attributes"]
    gate("AT-2 10-12 attribute bullets", 10 <= len(at) <= 12, f"{len(at)}")
    qm = sum(x["name"].count("?") + x["detail"].count("?") for x in at)
    gate("AT-1 zero question marks in attributes", qm == 0, f"{qm}")

    # ---- segment 2 --------------------------------------------------------
    for loc in d["segment_2"]["locations"]:
        nm, qs = loc["location"], loc["questions"]
        gate(f"SF-1 {nm} exactly 10 questions", len(qs) == 10, f"{len(qs)}")
        bad = [q["q"][:40] for q in qs if not 2 <= len(q["bullets"]) <= 4]
        gate(f"SF-2 {nm} 2-4 bullets each", not bad, str(bad))
        bqm = [b["detail"] for q in qs for b in q["bullets"] if "?" in b["detail"] or "?" in b["label"]]
        gate(f"SF-3 {nm} zero question marks in bullets", not bqm, str(bqm[:2]))
        city = sum(1 for q in qs if q["geo_tag"] == "CITY")
        gate(f"SF-5 {nm} exactly 3 CITY-tagged", city == 3, f"{city}")
        gate(f"SF-7 {nm} every question traceable",
             all(q.get("topic_plan_ref") for q in qs), "")

    # ---- location differentiation ----------------------------------------
    locs = d["segment_2"]["locations"]
    if len(locs) == 2:
        a_, b_ = locs[0]["questions"], locs[1]["questions"]
        same_q = sum(1 for x, y in zip(a_, b_) if x["q"] == y["q"])
        same_b = sum(1 for x, y in zip(a_, b_) if x["bullets"] == y["bullets"])
        gate("DIFF bullet sets identical <= 3", same_b <= 3, f"{same_b} of 10 identical")
        gate("DIFF question text identical <= 6", same_q <= 6, f"{same_q} of 10 identical")

    # ---- appendix ---------------------------------------------------------
    gate("SF-8 appendix rows present", len(d["appendix_question_bank"]) > 0,
         f"{len(d['appendix_question_bank'])} rows")

    # ---- outro ------------------------------------------------------------
    o = " ".join([d["outro"]["thanks"], d["outro"]["signoff"], d["outro"]["reach"]])
    for t in ("{{PODCAST_NAME}}", "{{FIRM_NAME}}", "{{PHONE_NUMBER}}", "{{WEBSITE}}", "{{ATTORNEY}}"):
        c = o.count(t)
        # {{ATTORNEY}} substring-matches inside {{ATTORNEY_NAME}}; not present here anyway
        gate(f"OC-4 {t} once in outro", c == 1, f"{c}")
    gate("OC-5 no Case Engine in outro", "Case Engine" not in o, "")
    gate("OC-5 no {{CITY}} in outro", "{{CITY}}" not in o, "")
    gate("OC-8 outro_note verbatim", d["static"]["outro_note"] in md, "")
    gate("OUTRO carries Florida", "Florida" in d["outro"]["reach"], "")

    # ---- outro above S2 ---------------------------------------------------
    gate("SF-12 outro renders inside S1", oi > 0 and (s2i < 0 or oi < s2i), "")
    leak = [p for p in ("thank you for your time", "see you next", "reach out to",
                        "subscribe", "That is it for this one") if p.lower() in s2.lower()]
    gate("SF-12 nothing outro-like in S2", not leak, str(leak))

    # ---- tokens -----------------------------------------------------------
    found = set(re.findall(r"\{\{[A-Z_0-9]+\}\}", md))
    gate("TOKENS only the eight", found <= TOKENS, f"unexpected: {sorted(found - TOKENS)}")
    gate("TOKENS no {{CITY}} / {{STATE}} / {{REGION}} / {{TOPIC}}",
         not ({"{{CITY}}", "{{STATE}}", "{{REGION}}", "{{TOPIC}}", "{{CITY_2}}"} & found), "")
    unbold = [m for m in re.finditer(r"\{\{[A-Z_0-9]+\}\}", md)
              if not (md[max(0, m.start()-2):m.start()] == "**" and md[m.end():m.end()+2] == "**")]
    gate("TOKENS all bold", not unbold,
         f"{len(unbold)} unbolded, first at char {unbold[0].start() if unbold else '-'}")

    # ---- house style ------------------------------------------------------
    for ch, nm in zip(DASHES, ("em dash", "en dash")):
        gate(f"STYLE zero {nm}", ch not in md, f"{md.count(ch)} found")
    r = [x for x in RETIRED if x.lower() in md.lower()]
    gate("STRUCT zero retired section names", not r, str(r))
    g = [x for x in GUEST if x.lower() in md.lower()]
    gate("EDIT zero guest framing", not g, str(g))

    # ---- jargon above the appendix ---------------------------------------
    title = d["episode_title"]
    scan = above.replace(title, "")   # client-approved title is exempt
    hits = []
    for pat in JARGON_HARD:
        for m in re.finditer(pat, scan, re.I):
            hits.append(m.group(0))
    gate("EDIT zero jargon above appendix", not hits, str(sorted(set(hits))[:6]))

    brit = []
    for pat in BRITISH:
        for m in re.finditer(pat, scan, re.I):
            brit.append(m.group(0))
    gate("EDIT US English above appendix", not brit, str(sorted(set(brit))[:6]))

    # ---- question count ---------------------------------------------------
    nq = len(re.findall(r"^\*\*Q\d+:", md, re.M))
    gate("SF total 20 questions rendered", nq == 20, f"{nq}")

    # ---- report -----------------------------------------------------------
    w = max(len(n) for n, _, _ in results)
    fails = 0
    for n, ok, det in results:
        if not ok:
            fails += 1
        print(f"{'PASS' if ok else 'FAIL'}  {n:<{w}}  {det}")
    print(f"\n{len(results) - fails}/{len(results)} gates passed")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
