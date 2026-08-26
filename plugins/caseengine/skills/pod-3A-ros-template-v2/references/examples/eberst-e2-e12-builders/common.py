#!/usr/bin/env python3
"""Shared payload assembly for the Eberst v2 ROS Templates, E3-E12.

Modelled directly on references/examples/eberst-e2-payload-worked-example.py.
Every episode module defines a SPEC dict and calls build(SPEC).

Rules encoded here so no episode module can violate them by accident:
  - the three STATIC strings are read from statics.json, never retyped
  - Location scope means the geo renders as plain text, so only the eight
    firm-specific tokens survive
  - nothing is ever passed through str.format(); tokens carry doubled braces
"""
import json, pathlib

SKILL = pathlib.Path.home() / ".claude/skills/pod-3A-ros-template-v2"
STATIC = json.loads((SKILL / "references/statics.json").read_text())["strings"]

# The eight tokens that survive at Location scope. The geo is fixed by the
# scope, so Florida, Stuart and Gainesville render as literal text.
TOKENS = ["{{PODCAST_NAME}}", "{{ATTORNEY_NAME}}", "{{ATTORNEY}}", "{{INTERVIEWER}}",
          "{{FIRM_NAME}}", "{{PHONE_NUMBER}}", "{{WEBSITE}}", "{{YEARS_PRACTICING}}"]


# --- spoken register -------------------------------------------------------
# The documents are said out loud on camera. Written English does not contract;
# people do. Applied to GENERATED text only - never to the three STATIC strings
# (gated byte-identical) and never to the appendix bank (verbatim research).
_CONTRACTIONS = [
 ("cannot", "can't"), ("can not", "can't"),
 ("do not", "don't"), ("does not", "doesn't"), ("did not", "didn't"),
 ("is not", "isn't"), ("are not", "aren't"), ("was not", "wasn't"),
 ("were not", "weren't"), ("has not", "hasn't"), ("have not", "haven't"),
 ("had not", "hadn't"), ("will not", "won't"), ("would not", "wouldn't"),
 ("could not", "couldn't"), ("should not", "shouldn't"),
 ("that is", "that's"), ("it is", "it's"), ("there is", "there's"),
 ("they are", "they're"), ("you are", "you're"), ("we are", "we're"),
 ("you have", "you've"), ("we have", "we've"), ("they have", "they've"),
 ("you will", "you'll"), ("what is", "what's"), ("here is", "here's"),
 ("who is", "who's"), ("let us", "let's"),
]

def natural(t):
    if not isinstance(t, str):
        return t
    for a, b in _CONTRACTIONS:
        t = t.replace(a, b)
        t = t.replace(a.capitalize(), b.capitalize())
    return t

B = lambda *pairs: [{"label": l, "detail": d} for l, d in pairs]


def build(spec):
    locs = []
    for loc in spec["locations"]:
        qs = []
        for n in range(1, 11):
            tag, q, bullets = loc["questions"][n]
            bullets = [{"label": natural(b["label"]), "detail": natural(b["detail"])} for b in bullets]
            qs.append({
                "q": natural(q),
                "bullets": bullets,
                "geo_tag": tag,
                "kind": loc.get("kinds", {}).get(n, "search-phrase"),
                "topic_plan_ref": spec["ref_fmt"].format(n=n),
                "source_ngram_ref": f"bank-{loc.get('bank_map', {}).get(n, n)}",
            })
        locs.append({"location": loc["name"], "questions": qs})

    return {
        "schema_version": "2.0.0",
        "episode_format": "v2-open-interview",
        "topic": spec["topic"],
        "episode_title": spec["episode_title"],
        "episode_number_token": spec["episode_number_token"],
        "scope": "Location",
        "location": "Stuart and Gainesville, Florida",
        "city": "Stuart",
        "region": "the Treasure Coast",
        "state": "Florida",
        "episode_goal": spec.get("episode_goal", "Authority"),
        "duration": {"segment_1_min_low": 15, "segment_1_min_high": 30},
        "segment_1": {
            "topic_phrase": spec["topic_phrase"],
            "setup": natural(spec["setup"]),
            "credential": natural(spec["credential"]),
            "prompt": natural(spec["prompt"]),
            "attributes": [{"name": natural(a["name"]), "detail": natural(a["detail"])}
                           for a in spec["attributes"]],
        },
        "segment_2": {"locations": locs},
        "appendix_question_bank": [{"n": i, "question_text": q, "ngram_ref": f"bank-{i}"}
                                   for i, q in enumerate(spec["bank"], 1)],
        "placeholders_used": TOKENS,
        "static": {k: STATIC[k]["value"] for k in ("welcome", "welcome_first", "outro_note")},
        "cover_page": {
            "logo_drive_id": "1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2",
            "logo_width_pt": 180,
            "title": "Run of Show",
            "prepared_by": "Prepared by Case Engine",
        },
        "outro_close": {},
        "outro": {k: natural(v) for k, v in spec["outro"].items()},
        "metadata": spec["metadata"],
    }


def emit(spec, outdir):
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    payload = build(spec)
    p = outdir / f"eberst-{spec['episode_number_token'].lower()}-data.json"
    p.write_text(json.dumps(payload, indent=2))
    print("wrote", p)
    return p
