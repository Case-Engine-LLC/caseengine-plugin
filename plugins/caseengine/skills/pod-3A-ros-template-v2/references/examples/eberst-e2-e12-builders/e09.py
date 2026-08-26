#!/usr/bin/env python3
"""E9 - Fault When a Pedestrian Is Hit.

Topic Plan RECONCILED. Live Doc `Episode 9:` table, 25 rows, zero vetoes. S2 ships
rows 1-10 in Doc order, tail-truncated.

Research: the Eberst `fault-when-a-pedestrian-is-hit` n-gram table (REAL, 25 rows) and
both city pedestrian entity maps (REAL). This is the FAULT episode; the crossing rules
belong to E8 and are deliberately kept out so the two documents do not read alike.

Rotation: line 2 pattern D, line 3 frame F (the bench), line 4 frame E (the other side,
verb `tell us` because fault is a judgment call), outro `clarity`, sign-off index 1.
"""
from common import B, emit
from attributes import ATTRIBUTES as _ATTRS

SHARED = {
 2: ("NEUTRAL", "Is the driver always at fault when somebody on foot gets hit?", B(
     ("No, and that surprises people", "being hit is not the same as being in the right, and the insurer knows it."),
     ("Fault comes down to a choice", "maybe the driver was speeding, looking at a phone, or turning without checking, or maybe the person on foot crossed where the driver could not see them."),
     ("Usually it is split", "most of these cases end up with some blame on each side, and the whole fight is over how big each side's share is."))),
 4: ("NEUTRAL", "What happens to your claim if you crossed against the signal?", B(
     ("It hurts your case, it does not end it", "your share of the blame goes up, and what you recover comes down by the same amount."),
     ("The driver still had duties", "a green light in their favor does not give them the right to hit somebody they could see."),
     ("The margin is what counts", "the argument is over ten or fifteen points, and that is real money either way."))),
 9: ("NEUTRAL", "How much does the driver's speed change the fault picture?", B(
     ("It decides whether stopping was possible", "a few miles an hour is the difference between a driver stopping in time and never having a chance."),
     ("Speed is measurable", "the car's own computer stores it, the skid marks show it, and a reconstruction puts an actual number on it."),
     ("It also changes the injuries", "the same kind of collision at a higher speed produces a very different set of injuries, and that is something we can prove."))),
}

def qs(city, region, how_fault, cliff_note, midblock_note, report_note, video_note,
       distracted_note, lot_note):
    d = {
     1: ("CITY", f"How does anyone decide who was at fault when somebody is hit in {city}?", B(
         ("Start with where they were", "the point of impact relative to the crossing does more work than any statement."),
         ("Then what each side could see", "sightlines, parked cars, lighting and the angle the driver was coming from."),
         ("Then who is investigating", how_fault))),
     3: ("STATE", "Can somebody on foot be found partly at fault for their own injuries in Florida?", B(
         ("Yes, and it is the usual outcome", "a share gets assigned to each side and yours comes straight off what you recover."),
         ("There is a hard cutoff", "past a certain share of the blame in Florida you recover nothing at all."),
         ("That is why the fight is over a few points", cliff_note))),
     5: ("CITY", f"What happens when somebody crossed mid-block in {city}?", B(
         ("You gave up the right of way", "away from a crosswalk the person on foot is the one required to yield, so some of the blame does get assigned to them."),
         ("The driver is not excused", "they still had to be looking, and a driver who never braked has a problem of their own."),
         ("Why people do it here", midblock_note))),
     6: ("NEUTRAL", "What does the police report actually decide about fault?", B(
         ("Less than everybody assumes", "the officer got there afterward and wrote down what they were told."),
         ("It rarely reaches a jury", "the report itself usually never gets shown to the jury, so we rebuild the case from the evidence the officer was working from."),
         ("It still sets the opening number", report_note))),
     7: ("CITY", f"How do witnesses and video settle a disputed fault case in {city}?", B(
         ("Video ends the argument", video_note),
         ("Witnesses fade fast", "memory of where somebody was standing degrades within days, and people move away."),
         ("Get both immediately", "send a written preservation letter on day one, because that is the difference between video that exists somewhere and video you actually get to use."))),
     8: ("CITY + REGION", f"How does a distracted driver shift the blame in {city} and across {region}?", B(
         ("It removes their best defense", "a driver who never looked up cannot argue you appeared out of nowhere."),
         ("We can check the phone", "the carrier records show exactly what that phone was doing in the seconds before impact, and we can subpoena them."),
         ("Where it clusters here", distracted_note))),
     10: ("NEUTRAL", "How is fault worked out in a parking lot or a driveway?", B(
         ("The traffic laws do not apply the same way", "a private lot has no marked lanes and no signals, so there is a lot more room to argue."),
         ("Reversing is the common one", "a driver backing out has almost no view of what is directly behind them."),
         ("Cameras carry these", lot_note))),
    }
    d.update(SHARED)
    return d

LOCATIONS = [
 {"name": "Stuart",
  "questions": qs("Stuart", "the Treasure Coast",
    how_fault="Stuart Police, the Martin County Sheriff's Office or the Highway Patrol, depending on the road, and if somebody was killed it goes to the Highway Patrol's traffic homicide investigators.",
    cliff_note="insurers push you toward that line on purpose, and around here their favorite argument is that you crossed away from a marked crosswalk on a road where the crosswalks are a long way apart.",
    midblock_note="on US 1 the shops sit between the signals, so people cross where they need to be rather than walking a quarter mile to a light.",
    report_note="the adjuster reads it before anyone files anything, and if the injured person is from out of town, they will lean on that report hard.",
    video_note="the storefronts, restaurants and banks along US 1 and Kanner Highway hold most of it, and it is gone in about a month.",
    distracted_note="US 1 and Kanner Highway, where drivers are moving fast past shops and restaurants that people walk back and forth between.",
    lot_note="the shopping center and restaurant lots along US 1 keep cameras, and that footage is the whole case when there is no independent witness.")},
 {"name": "Gainesville",
  "questions": qs("Gainesville", "North Central Florida",
    how_fault="Gainesville Police, the Alachua County Sheriff's Office, University of Florida Police or the Highway Patrol, and which agency it is comes down to jurisdiction lines that are invisible from the street.",
    cliff_note="insurers push you toward that line on purpose, and around a campus their favorite argument is that you stepped into the road at night without looking.",
    midblock_note="around campus people cross straight toward wherever they are headed, and if it happened at night in the bar district, expect the insurer to lead with that.",
    report_note="the adjuster reads it before anyone files anything, and if the injured person is a student, they will lean on that report hard.",
    video_note="the university holds its own footage on its own request process, the city has cameras on the corridors it has been rebuilding, and the businesses have theirs.",
    distracted_note="University Avenue and 13th Street, where a bus stop puts a crowd at the curb and the driver is watching for a gap in traffic.",
    lot_note="the apartment complexes and the campus garages record constantly, and getting to that footage means knowing who owns the camera.")},
]

ATTRIBUTES = _ATTRS[9]

BANK = [
 "How is fault determined when a pedestrian is hit by a car?",
 "Is the driver always at fault when a pedestrian is struck?",
 "Can a pedestrian be found partly at fault for their own injuries?",
 "How does crossing against a signal affect a pedestrian's claim?",
 "How is fault handled when a pedestrian crosses mid-block?",
 "What role does the police report play in assigning pedestrian-accident fault?",
 "How do witnesses and video resolve a disputed pedestrian-accident fault?",
 "How does a distracted driver shift fault in a pedestrian case?",
 "How does speeding factor into pedestrian-accident fault?",
 "How is fault decided when a pedestrian is hit in a parking lot or driveway?",
 "How does fault work when multiple vehicles are involved in a pedestrian crash?",
 "What happens to fault when the driver flees the scene?",
 "How do darkness, weather, and visibility affect pedestrian-accident fault?",
 "How does a child pedestrian's age affect fault analysis?",
 "How do insurance companies argue pedestrian fault to cut a claim?",
 "What evidence best protects a pedestrian against unfair fault claims?",
 "How does an attorney rebuild the fault picture in a pedestrian case?",
 "How does the fault percentage change what a pedestrian can recover?",
 "What mistakes make a pedestrian look more at fault than they really were?",
 "When should a pedestrian-accident victim get a lawyer involved over fault?",
 "How does a pedestrian's clothing or conspicuity get raised as a fault issue?",
 "How is fault analyzed when a pedestrian was intoxicated?",
 "How does a driver's right-on-red or turning movement create pedestrian fault?",
 "How does an attorney counter an insurer that overstates pedestrian fault?",
 "What is the single most important point about fault in a pedestrian case?",
]

SPEC = {
 "topic": "pedestrian accidents",
 "episode_title": "Fault When a Pedestrian Is Hit",
 "episode_number_token": "E9",
 "episode_goal": "Differentiation",
 "topic_phrase": "how the blame actually gets divided when somebody on foot is hit",
 "setup": ("I'm **{{INTERVIEWER}}**, and today's subject catches people completely off guard. In Florida, "
           "being hit while you were on foot does not automatically mean the driver was at fault, and "
           "how much of the blame lands on you changes everything."),
 "credential": ("**{{ATTORNEY}}**, your firm has accident reconstruction experts lined up before most clients "
                "even realize fault is being disputed."),
 "prompt": ("Somebody is in a hospital bed and the insurer has already decided how much of this was "
            "their fault. Tell us how they come up with that percentage. And if you have torn one of "
            "those numbers apart, take us through it."),
 "attributes": ATTRIBUTES,
 "locations": LOCATIONS,
 "bank": BANK,
 "ref_fmt": "TP-E9-R{n}",
 "outro": {
   "thanks": ("**{{ATTORNEY}}**, thanks for walking through all of that. Most people have to figure out on their own how "
              "the blame gets divided. That is going to save somebody a lot of trouble."),
   "signoff": "That is where we will leave it. **{{PODCAST_NAME}}**. See you next episode.",
   "reach": ("One more thing, if you are anywhere in Florida and need help with this, get in touch with "
             "**{{FIRM_NAME}}**. The number is **{{PHONE_NUMBER}}**, and the site is **{{WEBSITE}}**."),
 },
 "metadata": {
   "topic_plan_reconciled": True,
   "topic_plan_doc_id": "1P_1tAKXf6_I7EODRnkzDGVhUqPKBncdPKL127YlxgYs",
   "topic_plan_revision_id": "AIroW34FYjoDNe-pyO0zmcS3bcMOn0H73Q9-m2OO7TkOMdkCNXN_YAGDkb1Jlr9B8vTPL2VOBuKMHeoY85-DOkgVPQZv0OMwEA53iwt4JmQ",
   "topic_plan_fetched_at": "2026-08-18T20:40:06Z",
   "attribute_source": "fallback",
   "attribute_source_pulled": "2026-08-14",
   "attribute_source_confidence": "Inferred",
   "outro_line1_approach": "clarity",
   "outro_line2_index": 1,
   "outro_line3_slots": ["One more thing,", 1, "get in touch with", 1],
 },
}

if __name__ == "__main__":
    emit(SPEC, "out")
