#!/usr/bin/env python3
"""E11 - E-Bike and E-Scooter Laws and Liability.

Topic Plan RECONCILED. Live Doc `Episode 11:` table, 27 rows, zero vetoes. S2 ships
rows 1-10 in Doc order, tail-truncated.

Research: the Eberst `ebike-escooter-laws-liability-fl` n-gram table (REAL, 27 rows)
and the FL-state e-bike entity map (REAL). That map is STATE SCOPE ONLY - it carries
zero city entities for either market - so the local layer is borrowed from the two
pedestrian entity maps (both REAL) and sourced accordingly.

FOUR THINGS THE RESEARCH DOES NOT SUPPORT, and which are therefore absent here: any
named scooter-share operator in either market, any named trail or campus path, any UF
campus micromobility rule, and any city sidewalk ordinance text. The prior Drive ROS
pair asserted some of these via string-swap and introduced real errors doing it.

Rotation: line 2 pattern D, line 3 frame D (specific case type), line 4 frame A (the
aftermath, verb `lay out` because the ask is a comparison), outro `topical`, index 3.
"""
from common import B, emit
from attributes import ATTRIBUTES as _ATTRS

SHARED = {
 2: ("STATE", "What are the three classes of e-bike in Florida, and why do they matter?", B(
     ("Class one and two stop at twenty", "one helps only while you pedal, the other has a throttle, and both cut out at twenty miles an hour."),
     ("Class three goes to twenty-eight", "faster, more crash energy, tighter rules about who can ride it and where."),
     ("The class is what the fight is about", "it sets where you were allowed to ride and how fast you were allowed to go."))),
 5: ("STATE", "Does Florida make you wear a helmet on one of these?", B(
     ("Only under sixteen", "the requirement is an age rule, and above it the choice is yours."),
     ("Not wearing one is still used", "it is not a violation, but the other side will raise it against a head injury claim anyway."),
     ("It does not end the claim", "the other side can argue it and a jury can reduce what you recover, but it does not take away your right to bring the claim."))),
 6: ("STATE", "Do you need a license, registration or insurance to ride one in Florida?", B(
     ("You do not register one like a car", "and that is exactly why no injury coverage comes attached to it."),
     ("That is the trap", "people assume something covers them the way a car policy does, and nothing does."),
     ("Check before you need to", "the coverage question has an answer, and finding it out after a crash is the expensive way."))),
}

def qs(city, region, classify_note, rented_note, ride_where_note,
       pip_note, gap_note, household_note, pays_note):
    d = {
     1: ("CITY", f"You were on an e-bike or a scooter in {city}. What does Florida law actually call it?", B(
         ("It is the first question in the case", classify_note),
         ("An e-bike is treated like a bicycle", "same rights on the road, same duties, and that is where the rules come from."),
         ("A scooter sits in its own category", "Florida law says it is not a motor vehicle, and that changes everything about coverage."))),
     3: ("CITY", f"Does a rented scooter work differently from your own around {city}?", B(
         ("The state rules are the same", "what changes is the paperwork you agreed to when you unlocked it."),
         ("The rental terms are the fine print", "app coverage tends to carry low limits and exclusions people never read."),
         ("How it shows up here", rented_note))),
     4: ("CITY + REGION", f"Where can you legally ride one in {city} and across {region}?", B(
         ("The road and the bike lane", "an e-bike belongs where a bicycle belongs, which is the road or the bike lane, not the sidewalk in most places."),
         ("Sidewalks are where it changes", "the sidewalk rule is set town by town, so check the rule for the town you actually ride in."),
         ("Where it goes wrong here", ride_where_note))),
     7: ("NEUTRAL", "If a car hits you on a scooter, does your own injury coverage apply?", B(
         ("Not the way you would expect", "no-fault coverage is tied to motor vehicles, and a scooter is not one, so nothing follows the scooter itself."),
         ("So nothing pays the first bills", pip_note),
         ("It sends the claim elsewhere", "straight to the driver who hit you and to your own uninsured coverage."))),
     8: ("NEUTRAL", "A scooter is not a motor vehicle under Florida law. Why does that one fact control the whole claim?", B(
         ("It takes away the automatic coverage", "with a car, something pays your first bills no matter who caused the crash, and on a scooter nothing does."),
         ("Fault becomes everything", "with nothing paying automatically, proving the driver caused it is the only route."),
         ("It changes the urgency", gap_note))),
     9: ("CITY", f"If you own a car, can you still use that policy after a scooter crash in {city}?", B(
         ("Often yes, and people never ask", household_note),
         ("A relative's policy can count too", "somebody in the same household with coverage may bring you inside it."),
         ("Bring every policy", "the declarations page, the summary sheet at the front, from every car in the house, and that is the first thing to gather."))),
     10: ("NEUTRAL", "When your own coverage does not apply, whose insurance actually pays?", B(
         ("The driver who hit you, first", "their liability coverage is the main route, and in Florida that coverage is optional."),
         ("Then your own uninsured coverage", "which is why it matters far more to a rider than to a driver."),
         ("Then the others in the chain", pays_note))),
    }
    d.update(SHARED)
    return d

LOCATIONS = [
 {"name": "Stuart",
  "questions": qs("Stuart", "the Treasure Coast",
    classify_note="an electric bike, a scooter and a moped are three different things in Florida, and which one you were on decides the coverage.",
    rented_note="most riding here is on somebody's own bike rather than a rental, so the coverage you are looking for is usually a policy on a car in that household.",
    ride_where_note="US 1 and Kanner Highway are built for speed with no real place for two wheels, and A1A puts riders alongside beach traffic at crossings that are a long way apart.",
    pip_note="the emergency room bill shows up and there is no coverage behind it, and around here a serious injury means a transfer out of the county, which is a second bill on top of the first.",
    gap_note="the evidence has to be locked down immediately, because there is no coverage sitting there paying while anyone works it out.",
    household_note="your own car policy can still cover you even though you were nowhere near the car, and around here most riders do own one.",
    pays_note="whoever built it if a part failed, and the county or the city if the road itself was the problem, and a claim against a government carries a much shorter deadline.")},
 {"name": "Gainesville",
  "questions": qs("Gainesville", "North Central Florida",
    classify_note="an electric bike, a scooter and a moped are three different things in Florida, and around campus that argument comes up constantly because the machines all look alike.",
    rented_note="rentals are common around a campus, so the terms you agreed to on the app become part of the case in a way they rarely do elsewhere.",
    ride_where_note="University Avenue, 13th Street and Archer Road, where riders, people on foot and cars all arrive at the same crossing at the same time.",
    pip_note="the emergency room bill shows up and there is no coverage behind it, and here that is the trauma center in town, so the bill comes quickly and it is a big one.",
    gap_note="the evidence has to be locked down immediately, and if it was a rental the ride data sits with the company and does not wait.",
    household_note="a car policy in your household can still cover you even though you were nowhere near the car, and for a student that is often a policy in another county.",
    pays_note="whoever built the scooter if a part failed, the rental company if it was not maintained, and the city or the university if the road itself was the problem, and a claim against a government carries a much shorter deadline.")},
]

ATTRIBUTES = _ATTRS[11]

BANK = [
 "What does Florida law actually consider an e-bike or an e-scooter, and why does that classification decide everything about my case?",
 "What are Florida's e-bike laws, and how do the Class 1, Class 2, and Class 3 categories change where I can legally ride?",
 "What are Florida's e-scooter laws, and does the state treat a rented scooter differently from one I own?",
 "Where can I legally ride an e-bike or e-scooter in Florida - on the sidewalk, in the bike lane, or in the road?",
 "Does Florida require a helmet on an e-bike or e-scooter, and what changes for riders under 16?",
 "Do I need a license, registration, or insurance to ride an e-scooter in Florida?",
 "If a car hits me while I'm riding an e-scooter in Florida, does any PIP coverage apply to my injuries?",
 "Why is an e-bike or e-scooter not a \"motor vehicle\" under Florida's no-fault law, and why does that distinction control my whole claim?",
 "If I own a car, can I still use my own household auto PIP or MedPay after an e-scooter crash?",
 "When PIP doesn't apply, which at-fault party's insurance actually pays - the driver, the scooter company, or the manufacturer?",
 "How does my uninsured or underinsured motorist coverage protect me when the driver who hit my e-bike has little or no insurance?",
 "When I'm hurt on a rented Lime, Bird, or Spin scooter, does the rental app's insurance cover me?",
 "If a distracted driver doors me or right-hooks me on my e-bike, how do we prove the driver was at fault?",
 "What happens if I'm the e-scooter rider who hits a pedestrian on a Florida sidewalk - am I the one who's liable?",
 "Can I sue Lime, Bird, or Spin when a poorly maintained or defective shared scooter caused my crash?",
 "When a dangerous road or missing bike lane causes a crash, can I hold a Florida city or government responsible?",
 "My e-bike's battery caught fire - who is responsible for a lithium-ion battery fire injury?",
 "If my brakes or throttle failed and caused the crash, do I have a product liability claim against the manufacturer?",
 "How does a CPSC recall or safety notice help prove an e-bike or e-scooter was defective?",
 "How does Florida's 51% comparative negligence bar affect my recovery if I wasn't wearing a helmet or rode where I shouldn't have?",
 "Can the at-fault driver's insurer blame me for breaking an e-scooter operation rule, and how do we fight that?",
 "Can you get a DUI on an e-scooter in Florida, and how does intoxicated riding affect an injury claim?",
 "What evidence matters most after an e-scooter crash, and how fast does the app's ride data disappear?",
 "How do the scooter company's GPS, speed, and maintenance records become evidence in my case?",
 "What are the most common and most serious injuries in e-bike and e-scooter crashes?",
 "What is my e-scooter accident claim worth in Florida, and what damages can I recover?",
 "How long do I have to file an e-bike or e-scooter injury lawsuit in Florida after HB 837?",
]

SPEC = {
 "topic": "e-bike and e-scooter accidents",
 "episode_title": "E-Bike and E-Scooter Laws and Liability",
 "episode_number_token": "E11",
 "episode_goal": "Authority",
 "topic_phrase": "why an electric bike or scooter leaves you with no coverage at all",
 "setup": ("I'm **{{INTERVIEWER}}**, and today we are on something almost nobody looks into until they "
           "need it. If you ride an electric bike or a scooter in Florida, you are outside the "
           "insurance system every driver takes for granted, and almost nobody knows that."),
 "credential": ("**{{ATTORNEY}}**, your firm handles a wide range of injury work, and a lot of it involves "
                "people who were not in a car at all."),
 "prompt": ("Someone was just knocked off a scooter by a car. Lay out what is different about their "
            "situation. And if you have a real-world example, take us through it."),
 "attributes": ATTRIBUTES,
 "locations": LOCATIONS,
 "bank": BANK,
 "ref_fmt": "TP-E11-R{n}",
 "outro": {
   "thanks": ("**{{ATTORNEY}}**, thank you for your time. Nobody actually explains that getting on an e-bike "
              "or a scooter puts you outside Florida's no-fault system. You just did."),
   "signoff": "We will leave it there. This is **{{PODCAST_NAME}}**, and we will see you next episode.",
   "reach": ("And remember, if this is happening to you in Florida, get in touch with **{{FIRM_NAME}}** at "
             "**{{PHONE_NUMBER}}**, or find them at **{{WEBSITE}}**."),
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
   "outro_line2_index": 3,
   "outro_line3_slots": ["And remember,", 2, "get in touch with", 2],
 },
}

if __name__ == "__main__":
    emit(SPEC, "out")
