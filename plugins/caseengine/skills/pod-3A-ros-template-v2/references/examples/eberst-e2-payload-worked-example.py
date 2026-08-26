#!/usr/bin/env python3
"""Build the v2 ROS Template payload for Eberst E2, Stuart + Gainesville."""
import json, pathlib

SKILL = pathlib.Path.home() / ".claude/skills/pod-3A-ros-template-v2"
STATIC = json.loads((SKILL / "references/statics.json").read_text())["strings"]

B = lambda *pairs: [{"label": l, "detail": d} for l, d in pairs]

# Six demand-driven questions. Identical in both location sets - what somebody
# wants to know after a crash does not vary by city.
# Genuinely universal. Same in both sets because the research shows no local difference.
SHARED = {
 4: ("NEUTRAL", "Why does the insurance company want a recorded statement?", B(
     ("It is not for your benefit", "the adjuster is building a record they can use to reduce or deny the claim."),
     ("What they are fishing for", "an admission you were partly at fault, or that you felt fine at the scene."),
     ("You can say no", "you are not required to give one to the other driver's insurer."))),
 6: ("STATE", "Does Florida still pay you if the crash was partly your fault?", B(
     ("Partly at fault is not disqualified", "your share reduces what you recover, it does not erase it."),
     ("There is a cutoff", "past a certain share of the blame you recover nothing, so the percentage is the whole fight."),
     ("Their first number is a position", "the blame the adjuster assigns early is rarely where it ends up."))),
 10: ("NEUTRAL", "What is the most common mistake people make after a crash?", B(
     ("Waiting", "the delay costs the medical deadline, the footage, and the witnesses all at once."),
     ("Talking too much", "to the other insurer, and on social media, both of which get used later."),
     ("Taking the first offer", "it lands before treatment is finished, which is before anyone knows the value."))),
}


def localized(who_leaves, ers, uninsured_reality, footage_note):
    """Same question in both sets, but the bullets are drawn from THAT location's research.
    A shared question does not mean shared content."""
    return {
     2: ("STATE", "How long do you have to see a doctor after a crash in Florida?", B(
         ("The window is short", "two weeks from the crash, and it is the deadline that catches the most people out."),
         ("What happens if you miss it", "the no-fault benefits on your own policy are gone, and they do not come back."),
         ("Where to go", ers),
         ("Who gets caught", who_leaves))),
     7: ("NEUTRAL", "What evidence disappears first after a crash?", B(
         ("Camera footage", footage_note),
         ("Witnesses", who_leaves),
         ("The vehicles", "both cars get repaired or scrapped, and the damage is the story."))),
     8: ("NEUTRAL", "What happens if the other driver has no insurance?", B(
         ("It is common here", uninsured_reality),
         ("Check your own policy", "uninsured motorist coverage on your own car is what pays in that situation."),
         ("Look for other policies", "a household policy, a commercial policy, or an employer's can all come into play."))),
    }


def geo(city, region, roads, responders, court, govt_vehicle):
    """The four geo-bearing slots. These are what change per location."""
    return {
     1: ("CITY", f"What should you do at the scene of a car accident in {city}?", B(
         ("Get out of the lanes", f"if the car moves, especially on {roads}, a second crash is the real danger."),
         ("Call it in", f"{responders} needs to document it, and which one responds depends on the road."),
         ("Get the report started", "ask the officer for the crash report before you leave."),
         ("Photograph everything", "both cars, the road, the signage, the skid marks, and any injuries."))),
     3: ("CITY + REGION", f"Who responds to a car accident in {city} and across {region}?", B(
         ("It depends on the road", f"city streets, county roads and the highway each bring a different agency."),
         ("Why it matters", "the responding agency decides where the report lives and how fast you can get it."),
         ("Get the number", "the report number at the scene saves weeks of chasing it later."))),
     5: ("CITY", f"What is a car accident claim actually worth in {city}?", B(
         ("There is no average", "the range runs from a few thousand to seven figures, so an average tells you nothing."),
         ("What sets it", "how badly you were hurt, how long treatment runs, and what coverage exists to pay it."),
         ("Give a real range", "two or three cases you have handled here and where they landed."))),
     9: ("CITY", f"How long do you have to file a car accident lawsuit in {city}?", B(
         ("The clock is shorter than it used to be", "the deadline was cut recently and a lot of people are working off the old number."),
         ("Suing a government vehicle is different", f"a crash with {govt_vehicle} in {city} carries its own much earlier notice deadline."),
         ("Miss it and it is over", f"the {court} will not hear it, no matter how strong the case was."))),
    }


LOCATIONS = [
 # Stuart. From the fl-stuart location ROS and the Eberst Stuart Client ROS. The distinctive
 # local facts are seasonal residents, tourist witnesses, and the I-95 / Turnpike out-of-state
 # traffic that runs straight through Martin County.
 ("Stuart",
  geo("Stuart", "the Treasure Coast",
      "I-95, Florida's Turnpike, US 1 or the Roosevelt Bridge",
      "the Martin County Sheriff's Office, Stuart Police or the Highway Patrol",
      "Martin County courthouse", "a city or county vehicle"),
  localized(
      who_leaves="seasonal residents and tourists, who are out of state by the next day and gone for the season by the next month.",
      ers="the emergency room at Cleveland Clinic Martin North, or St. Lucie down in Port St. Lucie, both count.",
      uninsured_reality="this state does not require most drivers to carry injury coverage, and I-95 and the Turnpike bring in out-of-state drivers on top of that.",
      footage_note="traffic cameras on US 1 and Kanner Highway record over themselves, and the bridge cameras are on a short loop.")),
 # Gainesville. From the fl-gainesville location ROS. The university is the differentiator and
 # it drives its own search demand: UF students, UF vehicles, UF Police, and a population that
 # turns over every semester.
 ("Gainesville",
  geo("Gainesville", "North Central Florida",
      "I-75, Archer Road, University Avenue or 13th Street",
      "Gainesville Police, the Alachua County Sheriff's Office, University of Florida Police or the Highway Patrol",
      "Alachua County courthouse", "a city, county or University of Florida vehicle"),
  localized(
      who_leaves="students, who leave at the end of the semester and are frequently the witnesses on University Avenue and 13th Street.",
      ers="UF Health Shands or North Florida Regional, and a campus clinic visit does not count on its own.",
      uninsured_reality="this state does not require most drivers to carry injury coverage, and a student driver or a rideshare around campus often has the bare minimum.",
      footage_note="campus and business cameras along Archer Road and University Avenue record over quickly, and UF has its own request process.")),
]

ATTRIBUTES = [
 {"name": "Trial willingness", "detail": "Cases you actually tried rather than settled, and what that changes before a jury is ever picked."},
 {"name": "Case-type experience", "detail": "Not injury cases generally. Crashes like this one, how many, and how recently."},
 {"name": "Verifiable standing", "detail": "Your license and disciplinary history, which carries more weight than any rating."},
 {"name": "Local court familiarity", "detail": "The county court, the judges, and how the local defense firms actually operate."},
 {"name": "Fee structure", "detail": "The percentage, whether it rises if you file suit, who fronts records and experts, and what happens if you lose."},
 {"name": "Evidence preservation speed", "detail": "What you secure in the first days, before footage is recorded over and cars are repaired."},
 {"name": "Expert network", "detail": "The roles you bring in. Reconstructionists, treating physicians, life-care planners. Roles, not names."},
 {"name": "Who handles the case", "detail": "Whether the client is hiring you or an intake operation, and who they talk to day to day."},
 {"name": "Coverage hunting", "detail": "How you find every policy that could pay when the at-fault driver carries little or nothing."},
 {"name": "Deadlines", "detail": "The medical window and the filing deadline, said as numbers, and what happens if either passes."},
 {"name": "Honest assessment", "detail": "What would make this case difficult. Naming the hard part builds more trust than a promise."},
 {"name": "Availability", "detail": "Who answers at two in the morning, and whether that is someone at the firm."},
]

BANK = [
 "What should someone do at the scene of a car accident to protect both their health and their claim?",
 "Why is the fourteen-day medical deadline the single most important deadline after a crash?",
 "What evidence beyond photos and medical records can make or break a car accident claim?",
 "How does the state's no-fault insurance system actually work for a driver here?",
 "How did the 2023 tort reform rewrite the rules for car accident claims?",
 "What types of damages can a claimant recover, and how did the reform affect them?",
 "Why is giving a recorded statement to the at-fault driver's insurer one of the most damaging mistakes?",
 "Why do many drivers assume partial fault disqualifies them from recovering, and why is that often wrong?",
 "What is the statute of limitations for a car accident lawsuit today, and what special deadlines apply to government vehicles?",
 "What special considerations apply when a commercial truck, rideshare, or uninsured driver caused a crash?",
 "How do insurance companies calculate what a claim is worth?",
 "What is the difference between economic and non-economic damages?",
 "How is pain and suffering valued in a car accident claim?",
 "Why does the first settlement offer almost always come in low?",
 "Can I recover lost wages and lost future earning capacity?",
 "How do pre-existing conditions affect settlement value?",
 "How long does it take to get a car accident settlement?",
 "Why does waiting until treatment is finished matter for the settlement?",
 "What happens to a settlement if a medical lien or health insurer paid the bills?",
 "How does a gap in treatment hurt the claim?",
 "What evidence raises the value of a car accident claim the most?",
 "What is the role of policy limits in capping a settlement?",
 "How can someone tell if a settlement offer is actually fair?",
 "What should someone do before accepting any settlement check?",
 "When should an injured driver contact an attorney?",
]


def build():
    locs = []
    for name, g, loc in LOCATIONS:
        merged = {**SHARED, **loc, **g}
        qs = []
        for n in range(1, 11):
            tag, q, bullets = merged[n]
            qs.append({
                "q": q, "bullets": bullets, "geo_tag": tag,
                "kind": "attribute" if n in (5,) else "search-phrase",
                "topic_plan_ref": f"E2-legacy-R{n}",
                "source_ngram_ref": f"bank-{n}",
            })
        locs.append({"location": name, "questions": qs})

    return {
      "schema_version": "2.0.0",
      "episode_format": "v2-open-interview",
      "topic": "car accidents",
      "episode_title": "How to File a Car Accident Claim and Common Mistakes to Avoid",
      "episode_number_token": "E2",
      "scope": "Location",
      "location": "Stuart and Gainesville, Florida",
      "city": "Stuart",
      "region": "the Treasure Coast",
      "state": "Florida",
      "episode_goal": "Authority",
      "duration": {"segment_1_min_low": 15, "segment_1_min_high": 30},
      "segment_1": {
        "topic_phrase": "what to do after a car crash and the mistakes that sink a claim",
        "setup": ("I'm **{{INTERVIEWER}}**, and today we are talking about something a lot of people in "
                      "Florida end up dealing with, usually with no warning, and what you actually need to know "
                      "if it happens to you."),
        "credential": ("**{{ATTORNEY}}**, you have been handling these cases in Florida for "
                       "**{{YEARS_PRACTICING}}** years."),
        # L4-C, the first-week frame from references/introduction.md. Two short sentences, the
        # ask lands last, and nothing hangs off a noun phrase.
        "prompt": ("Someone was just in a wreck. Walk us through what they need to do. "
                   "And if you have a real world example, please walk us through it."),
        "attributes": ATTRIBUTES,
      },
      "segment_2": {"locations": locs},
      "appendix_question_bank": [{"n": i, "question_text": q, "ngram_ref": f"bank-{i}"}
                                 for i, q in enumerate(BANK, 1)],
      # Location scope fixes the topic, the state and the cities, so all three render as plain
      # text exactly like the region already does. Only firm-specific tokens survive. At Topic
      # Only scope the geo is unknown and {{TOPIC}}, {{CITY}} and {{STATE}} stay tokenized.
      "placeholders_used": ["{{PODCAST_NAME}}", "{{ATTORNEY_NAME}}", "{{ATTORNEY}}", "{{INTERVIEWER}}",
                            "{{FIRM_NAME}}", "{{PHONE_NUMBER}}", "{{WEBSITE}}", "{{YEARS_PRACTICING}}"],
      "static": {k: STATIC[k]["value"] for k in ("welcome", "welcome_first", "outro_note")},
      "cover_page": {
        "logo_drive_id": "1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2",
        "logo_width_pt": 180,
        "title": "Run of Show",
        "prepared_by": "Prepared by Case Engine",
      },
      "outro_close": {},
      "outro": {
        "thanks": ("**{{ATTORNEY}}**, thank you for your time. Nobody actually explains what the first "
                   "two weeks look like. You just did."),
        "signoff": "That is it for this one. **{{PODCAST_NAME}}**. We will see you next episode.",
        "reach": ("And remember, if you are in Florida and need a lawyer, reach out to "
                  "**{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**."),
      },
      "metadata": {
        "topic_plan_reconciled": "legacy-exempt",
        "topic_plan_doc_id": "1P_1tAKXf6_I7EODRnkzDGVhUqPKBncdPKL127YlxgYs",
        "attribute_source": "fallback",
        "outro_line1_approach": "topical",
        "outro_line2_index": 0,
      },
    }


if __name__ == "__main__":
    out = pathlib.Path(__file__).parent / "eberst-e2-data.json"
    out.write_text(json.dumps(build(), indent=2))
    print("wrote", out)
