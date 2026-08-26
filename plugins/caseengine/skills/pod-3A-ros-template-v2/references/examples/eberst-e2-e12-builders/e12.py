#!/usr/bin/env python3
"""E12 - Lane-Splitting and Lane-Filtering Laws.

Topic Plan RECONCILED. Live Doc `Episode 12:` table, 25 rows, zero vetoes. S2 ships
rows 1-10 in Doc order, tail-truncated. NOTE: no n-gram table exists for this episode
at ANY scope - the Topic Plan question set is the only question spine available, which
is fine because the Doc is the authority anyway.

Research: the lane-splitting FL episode entity map (REAL) and the Gainesville
motorcycle entity map (REAL). The STUART motorcycle entity map is a cloud stub, so
Stuart's local layer is reconstructed from the car, truck and pedestrian Stuart maps.

THREE THINGS NOT ASSERTED, because the research does not support them: seasonal rider
volume in either market, any named Stuart riding route or rider population, and any
drive-time or ridership link between either market and the Daytona events. The sources
carry a statute-number conflict on the splitting ban, which does not reach this document
because statute numbers never appear above the appendix.

Rotation: line 2 pattern A, line 3 frame E (the local system), line 4 frame D (the
mistake, verb `set us straight on`), outro `clarity`, sign-off index 4.
"""
from common import B, emit
from attributes import ATTRIBUTES as _ATTRS

SHARED = {
 4: ("NEUTRAL", "What is rider bias, and how much does it actually cost people?", B(
     ("They decide before they read anything", "the adjuster has already made up their mind about what kind of person rides a motorcycle before they open the file."),
     ("It shows up as a fault percentage", "they assume the rider was speeding, they turn that assumption into a percentage, and they take it straight off what they pay."),
     ("You beat it with evidence, not argument", "reconstruction, the road itself, and the driver's own record are what actually change their mind."))),
 7: ("NEUTRAL", "How is fault decided when a car rear-ends a motorcycle?", B(
     ("The driver in back starts on defense", "you are supposed to leave enough room to stop, so if you hit what is in front of you, you have some explaining to do."),
     ("They will still try", "the usual line is that the rider stopped suddenly or was hard to see."),
     ("The damage tells the story", "where the bike got hit and how far it went tell you most of what happened."))),
 9: ("NEUTRAL", "How does a distracted driver end up hitting a rider?", B(
     ("A bike is easy to miss", "at a glance a motorcycle looks like a gap in traffic, especially to somebody looking at a phone."),
     ("It removes their defense", "a driver who never looked cannot claim the rider came out of nowhere."),
     ("And we can check", "the phone records show exactly what that driver was doing in the seconds before the crash, and we can go get them."))),
}

def qs(city, region, roads, legal_note, split_note, blame_note, visible_note, left_turn_note,
       door_note, helmet_note):
    d = {
     1: ("CITY", f"What is lane-splitting, and how is it different from filtering, on {roads}?", B(
         ("Splitting is through moving traffic", "riding the line between two lanes of cars that are still going."),
         ("Filtering is at a standstill", "moving up between stopped cars at a light, at walking pace."),
         ("Neither one is legal here", legal_note))),
     2: ("CITY", f"If you were splitting lanes when you were hit in {city}, is your case over?", B(
         ("No, and that is the important part", "breaking a traffic rule puts a share of the blame on you. It does not end your claim."),
         ("There is a cutoff", "past a certain share of the blame in Florida you recover nothing, so the size of that share is everything."),
         ("What it looks like locally", split_note))),
     3: ("NEUTRAL", "How do insurance companies use lane-splitting to blame the rider?", B(
         ("They lead with it", "it is the first thing raised, often before anyone has established the rider was even doing it."),
         ("Assumption is not evidence", blame_note),
         ("Make them prove it", "the position of the bike and the damage on both vehicles either support that story or they do not."))),
     5: ("CITY + REGION", f"How much does being seen matter to fault in {city} and across {region}?", B(
         ("It is the standard defense", "the driver says they never saw the bike, like that settles it."),
         ("Not seeing is not an excuse", "you have a duty to look, so a driver who says they never saw the bike has just admitted they were not looking."),
         ("Where it really is hard to see a bike", visible_note))),
     6: ("CITY", f"How does the left-turn crash happen to riders in {city}?", B(
         ("It is the most common one", "a car turns across the rider's path because the driver misjudged the speed or never registered the bike."),
         ("The rider has nowhere to go", "there is no time to brake and no room to swerve once the car has committed."),
         ("Where it happens here", left_turn_note))),
     8: ("NEUTRAL", "What happens when a rider gets hit by an opening car door?", B(
         ("There is no avoiding it", "a door opens into the lane and the rider is on it before anything can be done."),
         ("Whoever opens the door owns it", "you look before you swing a door into traffic, and that goes for passengers too."),
         ("Where riders meet parked cars", door_note))),
     10: ("STATE", "How does wearing a helmet, or not, affect a claim in Florida?", B(
         ("Adults have a choice here", "Florida does not require a helmet if you are over twenty-one and you carry the medical coverage the law requires."),
         ("They will still raise it", "on any head injury the other side will argue a helmet would have changed the outcome."),
         ("It can shrink the claim, not kill it", helmet_note))),
    }
    d.update(SHARED)
    return d

LOCATIONS = [
 {"name": "Stuart",
  "questions": qs("Stuart", "the Treasure Coast", "US 1 and Kanner Highway",
    legal_note="Florida bans both, and we get a lot of drivers and riders from out of state, so plenty of people are going off the rules from somewhere it is legal.",
    split_note="on I-95 and the Turnpike, where traffic backs up and the temptation to move between lanes is real, and where the speeds make the outcome severe.",
    blame_note="an adjuster will assume a rider on US 1 was moving between lanes because it is a convenient story, not because anyone saw it.",
    visible_note="US 1 and Kanner Highway, where a rider sits low among larger vehicles and drivers are watching for gaps in traffic rather than for a bike.",
    left_turn_note="the left turns off US 1 into the businesses along it, where a driver is eyeballing a gap and just does not see the bike at all.",
    door_note="the parking along the downtown streets off US 1, where riders pass parked cars closely by necessity.",
    helmet_note="the argument goes to the size of the head injury claim, and here a serious one means a transfer out of the county and a longer record to build.")},
 {"name": "Gainesville",
  "questions": qs("Gainesville", "North Central Florida", "Archer Road and 13th Street",
    legal_note="Florida bans both, and a lot of students rode in another state before they moved here, so this one catches them off guard.",
    split_note="on I-75 where traffic stacks up, and and around campus, where somebody on a scooter or a small bike moves up between cars and never realizes that counts as splitting.",
    blame_note="an adjuster will assume a rider near campus was weaving through traffic, and it gets worse on a scooter or a smaller bike, because now they want to argue about what the rider was even riding.",
    visible_note="Archer Road, University Avenue and 13th Street, where bikes, scooters, cars and people on foot all occupy the same intersection at once.",
    left_turn_note="the campus intersections on Archer Road and 13th Street, where a driver turning across traffic is watching for cars and misses a bike entirely.",
    door_note="the street parking around campus, where somebody swings a door open into the travel lane all the time.",
    helmet_note="the argument goes to the size of the head injury claim, and here the trauma center is in town so the record of that injury is complete and immediate.")},
]

ATTRIBUTES = _ATTRS[12]

BANK = [
 "What is lane-splitting and how is it different from lane-filtering?",
 "Is lane-splitting legal, and how does that affect a motorcycle accident claim?",
 "How do insurance companies use lane-splitting to blame the rider?",
 "What is motorcycle rider bias and how does it hurt injured riders?",
 "How does motorcycle visibility and conspicuity factor into fault?",
 "How does a left-turn collision typically happen in a motorcycle crash?",
 "How is fault decided when a car rear-ends a motorcycle?",
 "How does a door collision or dooring injure a motorcyclist?",
 "How does a distracted driver cause a motorcycle crash?",
 "How does helmet use affect a motorcycle accident claim?",
 "How does comparative fault apply when the rider made a mistake too?",
 "What injuries are most common and most severe in motorcycle crashes?",
 "How is road rash treated as a real and compensable injury?",
 "What insurance covers a motorcyclist when the at-fault driver has too little?",
 "Why are motorcyclists at special risk of a coverage gap?",
 "What should a motorcyclist do at the scene of a crash?",
 "How is fault investigated and proven in a motorcycle crash?",
 "How are damages valued in a serious motorcycle injury case?",
 "How does an attorney counter rider bias in front of an adjuster or jury?",
 "How soon must a motorcycle accident claim be filed?",
 "What common mistakes weaken a motorcycle accident claim?",
 "When should an injured motorcyclist contact an attorney?",
 "What is the single most important point about lane-splitting and rider claims?",
 "How does an accident reconstruction expert help a motorcycle case?",
 "How does punitive exposure change when a drunk or reckless driver hits a rider?",
]

SPEC = {
 "topic": "motorcycle accidents",
 "episode_title": "Lane-Splitting and Lane-Filtering Laws",
 "episode_number_token": "E12",
 "episode_goal": "Differentiation",
 "topic_phrase": "what riding between lanes actually does to a rider's claim",
 "setup": ("I'm **{{INTERVIEWER}}**, and today we are talking about something a lot of Florida riders "
           "never get told straight. What riding between lanes actually does to your claim, and what "
           "to do if you get hit doing it."),
 "credential": ("**{{ATTORNEY}}**, after **{{YEARS_PRACTICING}}** years you know these judges, and you know "
                "exactly how the other side plays a case with a motorcycle in it."),
 "prompt": ("There is one thing about this that almost nobody gets told straight. Set us straight on it. "
            "And if getting it wrong has cost somebody real money, tell us about that one."),
 "attributes": ATTRIBUTES,
 "locations": LOCATIONS,
 "bank": BANK,
 "ref_fmt": "TP-E12-R{n}",
 "outro": {
   "thanks": ("**{{ATTORNEY}}**, thanks for being so straight about all of it. That is the clearest I have "
              "ever heard anybody explain what splitting actually costs a rider."),
   "signoff": "That is a wrap on this one. **{{PODCAST_NAME}}**. See you on the next one.",
   "reach": ("And before you go, if you are in Florida and need a lawyer, reach out to **{{FIRM_NAME}}** at "
             "**{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**."),
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
   "outro_line2_index": 4,
   "outro_line3_slots": ["And before you go,", 0, "reach out to", 0],
 },
}

if __name__ == "__main__":
    emit(SPEC, "out")
