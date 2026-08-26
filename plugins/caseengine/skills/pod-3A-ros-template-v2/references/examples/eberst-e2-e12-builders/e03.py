#!/usr/bin/env python3
"""E3 - Car Accident Types, Injury Types, and Their Effect on Compensation.

Research: EP3 `3. car-accident-types-.../locations/fl-stuart|fl-gainesville/06-ros-template`
(both REAL) plus the Gainesville 10-row n-gram table (REAL .docx) and the FL 32-row
parent table (REAL .docx). The Stuart n-gram table is a cloud stub; its ROS carries the
same ten-question structure with Stuart substitutions. Topic Plan has no Episode 3
breakdown table, so this runs legacy-exempt.

Rotation: line 2 pattern D, line 3 frame D (specific case type), line 4 frame F (the
spread, verb `break down` because the topic is a number), outro approach `clarity`,
sign-off bank index 1.
"""
from common import B, emit
from attributes import ATTRIBUTES as _ATTRS

SHARED = {
 2: ("STATE", "Does the kind of crash you were in change what the case is worth in Florida?", B(
     ("Same crash, different case", "two people in the same wreck can end up with very different claims, because it comes down to how badly each of them was hurt."),
     ("The injury sets the number", "what you get paid comes down to how badly you were hurt and how long you need treatment, not how bent up the car was."),
     ("Low damage is not low injury", "an adjuster will hold up a photo of a scuffed bumper, and we answer that with the imaging and the doctor who treated you."))),
 5: ("NEUTRAL", "How does anyone actually put a number on pain and suffering?", B(
     ("There is a method to it", "we start with the bills and the lost pay, and it goes up from there depending on how serious the injury is and whether you are stuck with it."),
     ("Permanence is what moves it", "an injury you are stuck with for life is worth far more than one you get over in six weeks."),
     ("What moves it up", "surgery, scarring, a documented head injury, and anything that changes what you can do for work."))),
}


def localized(late_injury_note, prior_injury_note, early_settle_note, deadline_note):
    return {
     4: ("NEUTRAL", "Why does an injury that shows up two days later still count?", B(
         ("Adrenaline hides it", "people walk away from a crash feeling fine and wake up two mornings later unable to turn their head."),
         ("The clock does not wait", "you have fourteen days to get seen, and if you miss it you lose the medical coverage on your own policy."),
         ("Where people get caught", late_injury_note))),
     7: ("NEUTRAL", "What happens to your case if your back or your knee was already bad?", B(
         ("It does not disqualify you", "if somebody made an existing problem worse, they are responsible for how much worse it got."),
         ("Your old records help you", "the imaging from before the crash is how we show how much worse you are now."),
         ("What it costs you", prior_injury_note))),
     9: ("NEUTRAL", "Why does settling early cost the most?", B(
         ("Nobody knows the number yet", "if they are offering money while you are still in treatment, they are guessing at how bad this gets."),
         ("You only get one shot", "once you sign, it is over, and that closes out the surgery nobody has even recommended yet."),
         ("What that means here", early_settle_note))),
     10: ("STATE", "What deadlines end a Florida injury case before it ever starts?", B(
         ("Two weeks to be seen", "miss it and the medical coverage on your own policy is gone for good."),
         ("Two years to file", "that deadline got cut back a few years ago, and plenty of people are still going off the old number."),
         ("A government vehicle is different", deadline_note))),
    }


def geo(city, region, crash_pattern, ers, fault_fight, commercial, roads):
    return {
     1: ("CITY", f"What kinds of crashes actually happen most around {city}?", B(
         ("Where you drive changes what happens", crash_pattern),
         ("Each one hurts differently", "a rear-end hit is a neck case, a side impact is a head and hip case, a rollover is a spine case."),
         ("Say what you see", f"the crashes you actually handle off {roads}, and what they do to people."))),
     3: ("CITY", f"Where does someone badly hurt in a {city} crash actually get treated?", B(
         ("Name the hospital", ers),
         ("Why that matters to the case", "the records from the first hours are the backbone of proving how bad it was."),
         ("Follow through matters more", "if you stop going to the doctor for a month, the insurance company will say you were fine that month."))),
     6: ("CITY + REGION", f"What changes when a commercial vehicle causes the crash in {city} or across {region}?", B(
         ("There is more coverage behind it", commercial),
         ("There is more evidence too", "the truck records what it was doing, and that data gets overwritten unless somebody asks for it fast."),
         ("More people can be responsible", "the driver, the company that hired them, and whoever owned the vehicle."))),
     8: ("CITY", f"How does where you got hit in {city} change the fight over fault?", B(
         ("Some places are genuinely ambiguous", fault_fight),
         ("The percentage is the whole case", "past a certain share of the blame you recover nothing, so a few points is real money."),
         ("What settles it", "the road itself, the sightlines, the signal timing, and anybody who saw it."))),
    }


LOCATIONS = [
 # Stuart. Two interstate corridors that merge, a bridge with its own crash profile,
 # no trauma center in the county, and a winter population that is not from here.
 {"name": "Stuart",
  "questions": {**SHARED,
    **localized(
      late_injury_note="seasonal residents who head north before they ever get looked at, and then have no record of the first two weeks.",
      prior_injury_note="the insurance company will argue you can still find work around here, so you have to spell out exactly what you used to do and cannot do now.",
      early_settle_note="the serious cases get moved out of the county, so your records sit in two different hospitals and it takes time to pull them together.",
      deadline_note="a crash with a city or county vehicle carries its own much earlier notice deadline, and it is measured in months."),
    **geo("Stuart", "the Treasure Coast",
      "the Roosevelt Bridge gets bad merges and head-on hits, I-95 and the Turnpike get chain reactions, and US 1 downtown is rear-end hits all day long.",
      "Cleveland Clinic Martin North handles the emergency room here, and the worst injuries get moved out of the county to the trauma center in Fort Pierce.",
      "the Roosevelt Bridge approaches and the left turns on US 1, where two drivers each believe they had the light.",
      "a truck on I-95 or the Turnpike is usually running interstate freight, which means a far larger policy than any car carries.",
      "I-95, the Turnpike, US 1 and Kanner Highway")}},

 # Gainesville. One interstate that is a freight spine, fog pileups, a Level I trauma
 # center in town, and campus intersections thick with people who are not in cars.
 {"name": "Gainesville",
  "questions": {**SHARED,
    **localized(
      late_injury_note="students who go home between semesters and let the two weeks run out somewhere else entirely.",
      prior_injury_note="the jobs here are mostly the university and the hospitals, so you have to spell out exactly what you used to do and cannot do now.",
      early_settle_note="the trauma center is here, so the whole record is in one place and it is worth waiting for all of it.",
      deadline_note="a crash with a university, city or county vehicle carries its own much earlier notice deadline, and it is measured in months."),
    **geo("Gainesville", "North Central Florida",
      "I-75 gets high speed wrecks and fog pileups, Archer Road and 13th Street get intersection hits, and University Avenue is where cars hit pedestrians, cyclists and scooters.",
      "UF Health Shands is the trauma center for this whole part of the state, and North Florida Regional is on Archer Road.",
      "the campus intersections on Archer Road and 13th Street, where a car, a bike and a scooter all read the same light differently.",
      "a truck on I-75 is usually running long haul freight, which means a far larger policy than any car carries.",
      "I-75, Archer Road, University Avenue and 13th Street")}},
]

ATTRIBUTES = _ATTRS[3]

# Verbatim from the Florida-scope n-gram table, fl-n-gram-table-v1.0.docx, 2026-04-30.
# 32 rows, the parent pool the local sets were drawn from. Shipped unedited.
BANK = [
 "How does the type of car accident a Florida driver is in shape the type of injuries they suffer and the value of their claim?",
 "What are the most common types of car accidents that lead to Florida personal injury claims and how do they differ in how they hurt people?",
 "Why are rear-end collisions so often tied to whiplash and soft-tissue injuries, and how does the Clampitt rear-end presumption strengthen a Florida claim?",
 "What makes head-on collisions the most dangerous type of car accident and why do they produce catastrophic-injury claims under Florida law?",
 "How do T-bone and side-impact crashes happen at Florida intersections and what injuries do they typically cause?",
 "Why do rollover accidents produce some of the most severe spinal and crush injuries and who can be held liable in Florida?",
 "What legal options do Florida victims have after a multi-vehicle pileup on I-95 or the Florida Turnpike and how are injuries evaluated in chain-reaction crashes?",
 "How does a hit-and-run accident change both the claims process and a Florida victim's ability to recover for injuries?",
 "What is whiplash really, and why do Florida insurance companies treat it so differently than other car accident injuries under the MIST defense?",
 "What are the signs of a traumatic brain injury after a Florida car accident and how do they affect the value of a claim?",
 "What kinds of spinal cord injuries happen in Florida car accidents and how does paralysis change the compensation picture?",
 "How do broken bones and fractures factor into the value of a Florida personal injury case under the §627.737 tort threshold?",
 "How do internal organ injuries from a Florida car accident affect a compensation claim and why are they harder to prove?",
 "How do pre-existing conditions affect a Florida car accident injury claim and how does the eggshell plaintiff doctrine protect the claimant?",
 "When does a Florida car accident injury cross the §627.737 serious injury threshold to unlock pain and suffering damages?",
 "How are non-economic damages calculated for pain and suffering after a Florida car accident, and how do the multiplier and per diem methods compare?",
 "How does a permanent injury or disfigurement change the strategy for valuing a Florida settlement, and how do hedonic damages factor in?",
 "What types of damages can a Florida claimant recover after a serious car accident injury beyond just medical bills?",
 "How do medical records, continuity of treatment, and reaching Maximum Medical Improvement drive the value of a Florida car accident claim?",
 "How do Florida insurance companies actually evaluate and value different injury types when deciding what to offer?",
 "How are lost wages and lost earning capacity calculated when a Florida injury prevents someone from working?",
 "How do PTSD, mental anguish, and emotional distress from a Florida car accident affect what someone can recover under §627.737?",
 "How do burn injuries and permanent disfigurement from a Florida car accident change the value of a case under the tort threshold and §768.72?",
 "How does Florida's modified comparative negligence rule under §768.81 after HB 837 affect what an injured Florida driver can actually recover?",
 "What role do medical experts and a life care plan play in proving both the cause and the value of a serious Florida injury?",
 "How does Florida's PIP layer interact with serious injury claims that exceed the $10,000 cap, and what triggers the EMC designation?",
 "When does a Florida injury case move from negotiation through demand to litigation, and how do the multiplier and per diem methods anchor the demand value?",
 "What is the statute of limitations for a Florida car accident injury or wrongful death lawsuit today, and how did HB 837 change it?",
 "What special considerations apply when a commercial truck causes a Florida injury crash, and why do those cases produce larger compensation?",
 "What happens when the at-fault driver is uninsured, underinsured, or flees the scene and the injury is catastrophic?",
 "How do punitive damages, loss of consortium, and wrongful death change the compensation picture in catastrophic Florida injury cases?",
 "What final piece of advice would a Florida personal injury attorney give someone who was just in a serious crash today?",
]

SPEC = {
 "topic": "car accidents",
 "episode_title": "Car Accident Types, Injury Types, and Their Effect on Compensation",
 "episode_number_token": "E3",
 "episode_goal": "Authority",
 "topic_phrase": "why two crashes that look the same are worth completely different money",
 # Line 2, pattern D. Nobody plans for this, and the decision window is the first week.
 "setup": ("I'm **{{INTERVIEWER}}**, and today's topic is one nobody plans for. Two crashes in Florida "
           "can look exactly the same and end up worlds apart, and what makes the difference is almost "
           "never what people assume."),
 # L3-D, the specific case type. Concedes breadth, then names the depth.
 "credential": ("**{{ATTORNEY}}**, your firm handles all kinds of injury cases, but car crashes have "
                "always been the core of it."),
 # L4-F, the spread. `Break down` because the topic is a number, not a process.
 "prompt": ("Two cases that look the same can land in completely different places. Break down what "
            "actually moves the number. And if you have two that went different ways, take us "
            "through both."),
 "attributes": ATTRIBUTES,
 "locations": LOCATIONS,
 "bank": BANK,
 "ref_fmt": "E3-legacy-R{n}",
 "outro": {
   "thanks": ("**{{ATTORNEY}}**, thank you for your time. That is a hard thing to explain without a "
              "whiteboard, and you did it in twenty minutes."),
   "signoff": "That is where we will leave it. **{{PODCAST_NAME}}**. See you next episode.",
   "reach": ("And remember, if you are in Florida and need a lawyer, call **{{FIRM_NAME}}**. "
             "The number is **{{PHONE_NUMBER}}**, and the site is **{{WEBSITE}}**."),
 },
 "metadata": {
   "topic_plan_reconciled": "legacy-exempt",
   "topic_plan_doc_id": "1P_1tAKXf6_I7EODRnkzDGVhUqPKBncdPKL127YlxgYs",
   "attribute_source": "fallback",
   "attribute_source_pulled": "2026-08-14",
   "attribute_source_confidence": "Inferred",
   "outro_line1_approach": "clarity",
   "outro_line2_index": 1,
   "outro_line3_slots": ["And remember,", 4, "call", 1],
 },
}

if __name__ == "__main__":
    emit(SPEC, "out")
