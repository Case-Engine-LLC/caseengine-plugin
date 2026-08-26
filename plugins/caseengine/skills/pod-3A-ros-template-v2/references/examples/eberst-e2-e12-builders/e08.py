#!/usr/bin/env python3
"""E8 - Right-of-Way and Crosswalk Law.

Topic Plan RECONCILED. Live Doc `Episode 8:` table, 25 rows, zero vetoes. S2 ships
rows 1-10 in Doc order, tail-truncated.

Research: pedestrian-accidents/locations/fl-stuart and fl-gainesville entity maps
(both REAL), plus the shipped E8 n-gram tables for both markets (REAL). This is the
RULES episode; fault allocation belongs to E9 and is deliberately kept out.

Rotation: line 2 pattern A, line 3 frame E (the local system), line 4 frame D (the
mistake, verb `set us straight on` because the topic is a misconception), outro
approach `topical`, sign-off index 0.
"""
from common import B, emit
from attributes import ATTRIBUTES as _ATTRS

SHARED = {
 3: ("STATE", "Do you still have any rights crossing outside a crosswalk in Florida?", B(
     ("You do, but you have to yield", "away from a crossing the traffic has the right of way, not you."),
     ("That does not make you fair game", "a driver who sees you and does not slow down is still responsible for hitting you."),
     ("Florida never legalized jaywalking", "if you are between two intersections that both have signals, you are supposed to use a marked crosswalk, whatever people assume."))),
 5: ("NEUTRAL", "How does a car that is turning or backing up end up hitting someone?", B(
     ("They are looking the other way", "a driver turning right is watching for a gap in traffic, not for a person already in the crossing."),
     ("A driver backing up can barely see", "in a lot of vehicles there is a stretch right behind the bumper you cannot see at all without a camera."),
     ("The walk signal does not stop them", "having the signal means you were lawfully there, not that the car saw you."))),
 7: ("NEUTRAL", "How does failing to yield actually establish that a driver was at fault?", B(
     ("There is a rule they broke", "the duty to yield to somebody in a crossing is written into the law, so we are not arguing about whether the driver was careful enough."),
     ("It changes what we argue about", "we are no longer arguing whether the driver was careful, we are arguing what this cost you."),
     ("Nobody has to get a ticket", "a driver who was never cited still broke the same rule."))),
}

def qs(city, region, corridors, marked_note, unmarked_note, evidence_note, distracted_note,
       injury_note, fault_note, agencies):
    d = {
     1: ("CITY", f"Who actually has the right of way at a crosswalk in {city}?", B(
         ("The person walking, once they are in it", "traffic has to yield to you, and the one exception is stepping out in front of a car that is already too close to stop."),
         ("The paint is not what makes it a crosswalk", "the duty to yield applies at corners that were never painted, and that is where most of the fighting happens."),
         ("Where it matters most here", corridors))),
     2: ("NEUTRAL", "What does the law actually require a driver to do at a marked crosswalk?", B(
         ("Yield, not creep", marked_note),
         ("Speed is part of it", "a driver who cannot stop for somebody already crossing was going too fast for that crossing."),
         ("Stopping means stopping", "if you roll through while somebody is still in the road you have already broken the rule, and it does not have to be a close call."))),
     4: ("CITY", f"How is it decided who was right at an intersection in {city} with no painted crossing?", B(
         ("An unpainted crossing is still a crossing", unmarked_note),
         ("It is where the sidewalk would continue", "the crossing legally exists along the line the sidewalk takes across the road."),
         ("Nobody knows this", "which is why the driver, the insurer and sometimes the officer all get it wrong at the scene."))),
     6: ("CITY", f"What proves somebody was crossing lawfully in {city}?", B(
         ("Where they were standing", "the point of impact relative to the crossing settles most of the argument by itself."),
         ("What was recording", evidence_note),
         ("Who saw it", "whoever was waiting at the same corner, and anyone working at a business facing the crossing."))),
     8: ("STATE", "What happens if the person walking was partly in the wrong?", B(
         ("It reduces what you get, it does not wipe it out", "your share of the fault comes off the recovery, and being partly wrong does not end the case."),
         ("But there is a hard line", "in Florida, if you are found more than fifty percent at fault, you recover nothing at all."),
         ("It is the whole fight", fault_note))),
     9: ("CITY + REGION", f"How do distracted and speeding drivers cause these crashes in {city} and across {region}?", B(
         ("They are looking down", "a driver checking a phone at a green light has no idea anybody stepped off the curb."),
         ("Speed removes the option", "a few miles an hour is the difference between a hard stop and no stop at all."),
         ("Where it concentrates here", distracted_note))),
     10: ("NEUTRAL", "What injuries actually happen when a car hits a person?", B(
         ("There is nothing protecting you", "the head, the pelvis and the legs take the force, and even a low-speed impact does serious damage."),
         ("Two impacts, not one", "the vehicle, and then the road, and the second one is often the worse of the two."),
         ("Where people get treated here", injury_note))),
    }
    d.update(SHARED)
    return d

LOCATIONS = [
 {"name": "Stuart",
  "questions": qs("Stuart", "the Treasure Coast",
    corridors="US 1 through downtown, where the shops and restaurants are on both sides and the marked crossings are a long way apart.",
    marked_note="a driver has to give way to somebody already in a marked crossing, and on a multilane road the drivers in the other lanes have to stop too, rather than swinging around the car that stopped.",
    unmarked_note="at a downtown corner on US 1 with no paint at all, the crossing is legally there and the duty to yield comes with it.",
    evidence_note="the shops, restaurants and banks along US 1 and Kanner Highway keep their own cameras, and a lot of that footage is gone inside a month.",
    distracted_note="US 1 and Kanner Highway, where the road is built for speed and people are still crossing it on foot to get between businesses.",
    injury_note="Cleveland Clinic Martin North handles the emergency room side, and the most serious injuries get moved out of the county to the trauma center in Fort Pierce.",
    fault_note="the insurer will say you crossed somewhere other than a marked crosswalk, and on a road where the crossings are half a mile apart that is easy for them to say and very beatable.",
    agencies="")},
 {"name": "Gainesville",
  "questions": qs("Gainesville", "North Central Florida",
    corridors="University Avenue and 13th Street, where the crossings are constant and the city has been rebuilding them for exactly that reason.",
    marked_note="a driver has to give way to somebody already in a marked crossing, and on University Avenue the city built raised crossings and added time to the walk signal because drivers were not yielding.",
    unmarked_note="on the side streets off campus with no paint at all, the crossing is legally there and the duty to yield comes with it.",
    evidence_note="the university has its own cameras with its own request process, the city has cameras on the corridors it has been rebuilding, and the businesses have theirs.",
    distracted_note="University Avenue, 13th Street and Archer Road, where a bus stop puts a crowd at the curb and a driver is watching traffic instead.",
    injury_note="UF Health Shands is the trauma center for this whole part of the state, so the most serious injuries stay in town and the whole medical record ends up in one place.",
    fault_note="the insurer will say you stepped out between parked cars, or that you were looking at your phone, and around a campus that is the first thing they reach for.",
    agencies="")},
]

ATTRIBUTES = _ATTRS[8]

BANK = [
 "Who has the right-of-way when a pedestrian and a car meet at a crosswalk?",
 "What does the law require of drivers when a pedestrian is in a marked crosswalk?",
 "Does a pedestrian have rights when crossing outside a crosswalk?",
 "How is fault decided when a pedestrian is hit at an unmarked intersection?",
 "How does a backing or turning vehicle create a pedestrian crash?",
 "What evidence proves a pedestrian was lawfully crossing?",
 "How does a driver's failure to yield establish negligence?",
 "How does comparative negligence apply when a pedestrian was partly at fault?",
 "How do distracted or speeding drivers cause crosswalk crashes?",
 "What injuries are most common when a pedestrian is struck by a vehicle?",
 "How does a pedestrian recover when the driver had little or no insurance?",
 "What insurance can an injured pedestrian who does not own a car still use?",
 "How is fault investigated when a pedestrian is hit in a parking lot?",
 "How does a hit-and-run change a pedestrian accident claim?",
 "What should a pedestrian do in the moments after being struck by a vehicle?",
 "How do traffic cameras and surveillance footage make or break these cases?",
 "How does an attorney prove the driver failed in a pedestrian case?",
 "How are damages valued in a serious pedestrian injury case?",
 "What common mistakes weaken a pedestrian accident claim?",
 "When should an injured pedestrian or their family contact an attorney?",
 "How does the time of day or lighting affect a crosswalk-collision claim?",
 "How are crosswalk laws enforced against drivers who routinely fail to yield?",
 "What happens when a pedestrian is struck in a marked school or work zone?",
 "How does an attorney handle a crosswalk case where fault is split?",
 "What is the single most important point about crosswalk right-of-way?",
]

SPEC = {
 "topic": "pedestrian accidents",
 "episode_title": "Right-of-Way and Crosswalk Law",
 "episode_number_token": "E8",
 "episode_goal": "Authority",
 "topic_phrase": "who actually has the right of way when somebody is crossing the road",
 "setup": ("I'm **{{INTERVIEWER}}**, and today we are talking about crosswalks. There is one thing almost "
           "everybody in Florida gets wrong about them, and it matters a great deal if you ever get hit."),
 "credential": ("**{{ATTORNEY}}**, after **{{YEARS_PRACTICING}}** years in these courts you know how the local "
                "insurers are going to argue a case like this before they say a word."),
 "prompt": ("There is one thing people around here get wrong about crosswalks more than anything else. "
            "Set us straight. And if you have seen it cost somebody their case, tell us about that one."),
 "attributes": ATTRIBUTES,
 "locations": LOCATIONS,
 "bank": BANK,
 "ref_fmt": "TP-E8-R{n}",
 "outro": {
   "thanks": ("**{{ATTORNEY}}**, thank you for your time. There is almost nothing useful out there on who "
              "actually has the right of way. Now there is."),
   "signoff": "That is it for this one. **{{PODCAST_NAME}}**. We will see you next episode.",
   "reach": ("And before you go, if you or somebody in your family was hit crossing the street in Florida, reach out to "
             "**{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**."),
 },
 "metadata": {
   "topic_plan_reconciled": True,
   "topic_plan_doc_id": "1P_1tAKXf6_I7EODRnkzDGVhUqPKBncdPKL127YlxgYs",
   "topic_plan_revision_id": "AIroW34FYjoDNe-pyO0zmcS3bcMOn0H73Q9-m2OO7TkOMdkCNXN_YAGDkb1Jlr9B8vTPL2VOBuKMHeoY85-DOkgVPQZv0OMwEA53iwt4JmQ",
   "topic_plan_fetched_at": "2026-08-18T20:40:06Z",
   "attribute_source": "fallback",
   "attribute_source_pulled": "2026-08-14",
   "attribute_source_confidence": "Inferred",
   "outro_line1_approach": "topical",
   "outro_line2_index": 0,
   "outro_line3_slots": ["And before you go,", 4, "reach out to", 0],
 },
}

if __name__ == "__main__":
    emit(SPEC, "out")
