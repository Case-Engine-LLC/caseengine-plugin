#!/usr/bin/env python3
"""E2 - How to File a Car Accident Claim and Common Mistakes to Avoid.

E2 predates this build. Its Introduction, prompt, Short-Form questions, outro and
bank are the approved reference copy from the original run and are NOT regenerated
here - they are read from the skill's worked-example payload untouched.

What this builder does change, to bring E2 up to the standard the rest of the
library now holds:
  - the ATTORNEY RESPONSE block, rewritten per-episode per AT-9 (labels and detail)
  - Q3 and Q5, which had city-specific question text but byte-identical bullets,
    so the two location sets read as one. 5 of 10 identical became 3 of 10.
  - the contraction pass, applied to generated text only

Everything else in E2 is byte-for-byte the approved copy.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import natural

SRC = pathlib.Path.home() / ".claude/skills/pod-3A-ros-template-v2/references/examples/eberst-e2-data.json"

ATTRIBUTES = [
 ("Cases you actually tried", "The ones you put in front of a jury instead of settling, and what an adjuster does differently once they know that about you."),
 ("Crashes like this one", "Not injury cases generally. Wrecks like the one they just had, how many, and how recently."),
 ("Your record, and where to check it", "Your license and your disciplinary history, which anybody can look up in about a minute and which say more than a star rating."),
 ("How the local courts run", "The county court, the judges, and how the local defense firms actually handle a claim like this."),
 ("The first forty-eight hours", "What you do immediately, before the car gets repaired and the video gets recorded over."),
 ("The mistakes that cost the most", "The handful of things people do in the first week that quietly take money off the table."),
 ("The recorded statement", "Why the other driver's insurer wants one so early, and what you tell people to do when that call comes."),
 ("Who else you bring in", "The treating doctors, the reconstruction people, and the experts who put a figure on what somebody can no longer do."),
 ("Finding the coverage", "How you track down every policy that could pay when the at-fault driver carries almost nothing."),
 ("Two clocks that matter", "The fourteen-day medical window and the filing deadline, said as real numbers, and what each one costs if it passes."),
 ("What this costs the client", "The percentage, whether it goes up if you file suit, who fronts the records and the experts, and what happens if you lose."),
 ("The part that is hard", "What would make this particular case difficult, said out loud before anybody has to ask."),
]

# The two questions whose bullets were identical across both cities.
LOCAL = {
 "Stuart": {
   3: ("It depends on the road", "Stuart Police inside the city, the Martin County Sheriff's Office in the county, and the Highway Patrol on I-95 and the Turnpike."),
   5: ("Give a real range", "two or three you have handled out of Martin County and where they actually landed."),
 },
 "Gainesville": {
   3: ("It depends on the road", "Gainesville Police in the city, the Alachua County Sheriff's Office in the county, University of Florida Police on campus, and the Highway Patrol on I-75."),
   5: ("Give a real range", "two or three you have handled out of Alachua County and where they actually landed."),
 },
}


def build():
    d = json.loads(SRC.read_text())
    d["segment_1"]["attributes"] = [{"name": natural(n), "detail": natural(t)} for n, t in ATTRIBUTES]
    for loc in d["segment_2"]["locations"]:
        for i, q in enumerate(loc["questions"], 1):
            if i in LOCAL[loc["location"]]:
                lbl, det = LOCAL[loc["location"]][i]
                q["bullets"][0]["label"] = natural(lbl)
                q["bullets"][0]["detail"] = natural(det)
    return d


if __name__ == "__main__":
    out = pathlib.Path(__file__).parent / "out/eberst-e2-data.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(build(), indent=2))
    print("wrote", out)
