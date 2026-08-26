#!/usr/bin/env python3
"""E5 - Wrongful Death from a Truck Crash.

TOPIC PLAN FINDING: this episode is NOT legacy-exempt. The live Doc carries a real
25-row question bank for this exact topic under the heading `Additional Topic:
Wrongful Death from a Truck Crash` rather than `Episode 5:`, which is why
scripts/verify-topic-plan.py --episode 5 finds nothing. The 12-Episode Plan table
names Episode 5 as this exact topic, so the bank is this episode's bank. The ten S2
questions are rows 1 through 10 in Doc order, tail-truncated, no reordering and no
substitution, per TP-3.

Research: truck-accidents/wrongful-death-from-a-truck-crash/locations/fl-stuart
(10-row n-gram, REAL) and .../fl-gainesville (12-row n-gram, REAL); Stuart truck
entity map REAL, Gainesville truck entity map STUB with locals recovered from the
Gainesville n-gram local_anchors block and the pedestrian/motorcycle maps.

Rotation: line 2 pattern D, line 3 frame F (the bench), line 4 frame B (the decision,
verb `tell us` because the topic is a judgment call), outro approach `topical`,
sign-off bank index 3.
"""
from common import B, emit
from attributes import ATTRIBUTES as _ATTRS

# Doc rows 3 and 5 are pure federal and state mechanics with no local component.
SHARED = {
 3: ("NEUTRAL", "What is the difference between a claim for the family and a claim for the estate?", B(
     ("They are two different losses", "one is what the survivors lost going forward, the other is what the person themselves went through before they died."),
     ("They get proved differently", "the family's loss is about support and companionship, the estate's is about the medical bills and the suffering in between."),
     ("They are filed together", "the same case carries both, which is why nobody should sign anything before somebody has looked at the whole picture."))),
 5: ("NEUTRAL", "How do the federal rules for truck drivers strengthen a family's case?", B(
     ("There is a rulebook a car does not have", "hours behind the wheel, rest, inspections, maintenance and who is allowed to drive at all."),
     ("There is less to argue about", "when a written safety rule was broken, the fight is no longer about whether the driver was being careful that day."),
     ("It is all written down", "logs, inspection records and hiring files exist for every one of those rules, and we can demand every one of them."))),
}


def localized(probate_note, liable_note, damages_note, carrier_note):
    return {
     2: ("STATE", "Who is actually allowed to file a wrongful death claim in Florida?", B(
         ("One person files for everybody", "the court appoints a representative for the estate, and that is the only person who can bring the case."),
         ("The family members are the ones who recover", "a husband or wife, the children, and in some situations the parents, each with a claim of their own inside the one case."),
         ("It starts at the courthouse", probate_note))),
     4: ("NEUTRAL", "Beyond the driver, who else can be held responsible for a fatal truck crash?", B(
         ("The company behind the driver", "the carrier answers for the person it put on the road and for how it ran the route."),
         ("Whoever owned the truck", "in Florida the owner of the vehicle is on the hook for what the driver did with it."),
         ("The rest of the chain", liable_note))),
     7: ("NEUTRAL", "How does the trucking company end up responsible for what its driver did?", B(
         ("It is not a loophole", "a company that puts a driver on the road answers for that driver on the job."),
         ("It also answers for itself", "who it hired, what training it gave, and whether it pushed a schedule that could not be run legally."),
         ("Why it matters to the family", carrier_note))),
     9: ("STATE", "What can a family actually recover after a fatal truck crash in Florida?", B(
         ("What they lost going forward", "the income, the benefits and the day-to-day help that person provided."),
         ("What cannot be replaced", "the companionship a husband or wife loses, and for a child, a parent's guidance, and the law looks at that separately for every family member."),
         ("What the estate carries", damages_note))),
    }


def geo(city, region, roads, corridor_note, trauma, court, evidence_note, fatigue_note, support_note):
    return {
     1: ("CITY", f"What makes a fatal truck crash different from any other fatal crash in {city}?", B(
         ("The other side moves first", "a carrier has people working the scene while the family is still being told what happened."),
         ("The roads it happens on", corridor_note),
         ("Where they are taken", trauma))),
     6: ("CITY", f"Why does the evidence disappear so fast after a fatal truck crash near {city}?", B(
         ("The truck is a witness", "it records everything it was doing, and nobody is holding on to that record for you."),
         ("Everything else is on a clock", evidence_note),
         ("One letter changes that", "a written demand to preserve the evidence, sent right away, is what keeps normal business from wiping it out."))),
     8: ("CITY + REGION", f"How do you prove a truck driver out on {roads} was too tired to be driving?", B(
         ("The hours are logged", "the truck keeps its own record of how long it had been running and when it last stopped."),
         ("The route itself tells you a lot", fatigue_note),
         ("The people who saw it", "whoever was on the road and whoever responded, and memories fade fast, so you get to them early."))),
     10: ("CITY", f"How is what the family lost actually calculated in {city}?", B(
         ("Start with what they earned", support_note),
         ("Then what they did that nobody paid for", "the driving, the childcare, the repairs around the house, and somebody has to be paid to do all of that now."),
         ("Then the years", "how long they would have worked and how long the family would have had them."),
         ("It gets filed here", f"the case is heard at the {court}, and a jury from this county is who all of this has to make sense to."))),
    }


LOCATIONS = [
 # Stuart. Two long-haul corridors bracket the county, there is a weigh station on I-95,
 # and there is no trauma center in Martin County, so the medical record splits in two.
 {"name": "Stuart",
  "questions": {**SHARED,
    **localized(
      probate_note="the appointment is made through the Martin County clerk, and nothing else moves until it is done.",
      liable_note="the broker who arranged the load and whoever strapped it down, because if the load shifted on the road that starts with them, not the driver.",
      damages_note="the medical bills and the funeral, and because the critical cases leave the county, those bills arrive from more than one hospital.",
      carrier_note="most of this freight is interstate and passing through, so the company behind it is rarely local and its coverage is far larger than the driver's."),
    **geo("Stuart", "the Treasure Coast",
      "I-95 and the Turnpike",
      "I-95 and the Turnpike both run straight through Martin County, so most of this freight is passing through and never stops here.",
      "there is no trauma center in Martin County, so anyone critically hurt goes to Fort Pierce, and the medical records end up split between two hospitals.",
      "Martin County courthouse",
      "the truck gets repaired or sold, the load is delivered and gone, and the commercial vehicle inspection records at the I-95 weigh station only tell you so much later.",
      "a long haul running the coast does not stop in Stuart, so the question is where it started and when.",
      "what that job actually paid in the Treasure Coast market, not a national average.")}},

 # Gainesville. One interstate that is the region's freight spine, a Level I trauma
 # center in town, and a last-mile delivery fleet that is a different coverage problem.
 {"name": "Gainesville",
  "questions": {**SHARED,
    **localized(
      probate_note="the appointment is made through the Alachua County clerk, and nothing else moves until it is done.",
      liable_note="the broker who arranged the load, whoever loaded it, and on a delivery van the contractor and the company whose name is on the side.",
      damages_note="the medical bills and the funeral, and with the trauma center in town those bills come from one place and land quickly.",
      carrier_note="it may be a long haul carrier off I-75 or a delivery contractor working for a much bigger company, and finding the insurance looks completely different depending on which one it turns out to be."),
    **geo("Gainesville", "North Central Florida",
      "I-75",
      "I-75 carries the freight for this whole part of the state, and the fog out there has set off pileups involving a dozen vehicles at a time.",
      "UF Health Shands is the trauma center for the whole region, so the medical record stays in one place, and it is complete.",
      "Alachua County courthouse",
      "the truck is back in service within days, the delivery vans turn over constantly, and the inspection records on I-75 sit with the state rather than the carrier.",
      "I-75 is a through route, so a driver in Alachua County has usually been going for hours before they get here.",
      "what that job actually paid around here, where most of the work is the university and the hospitals.")}},
]

ATTRIBUTES = _ATTRS[5]

# Verbatim from the live Topic Plan Doc, heading `Additional Topic: Wrongful Death from
# a Truck Crash`, 25 rows, revision AIroW34FYjoDNe-pyO0zmcS3bcMOn0H73Q9-m2OO7Tk...
BANK = [
 "What makes a wrongful death claim from a truck crash different from other fatal accidents?",
 "Who has the legal standing to file a wrongful death claim after a fatal truck crash?",
 "What is the difference between a wrongful death claim and a survival action?",
 "Who can be held liable for a fatal commercial truck crash?",
 "How do federal trucking regulations strengthen a wrongful death claim?",
 "Why must evidence in a fatal truck crash be preserved immediately?",
 "How does vicarious liability hold the trucking company responsible for a fatal crash?",
 "How is driver fatigue investigated in a fatal truck crash?",
 "What damages can a family recover in a truck accident wrongful death claim?",
 "How is loss of financial support calculated in a wrongful death case?",
 "How are non-economic losses like companionship and guidance valued?",
 "How does a trucking company's rapid-response team affect a fatal-crash investigation?",
 "How do the at-fault parties' commercial insurance policies affect a death claim?",
 "How does a freight broker or cargo loader share responsibility for a fatal crash?",
 "How is fault investigated and proven in a fatal truck crash?",
 "How does the timeline of a wrongful death truck case unfold?",
 "What role does the personal representative play in a wrongful death claim?",
 "How does the survival action recover the losses the victim suffered before death?",
 "How do criminal charges against a truck driver affect the civil death claim?",
 "How does an attorney coordinate a wrongful death truck case for the family?",
 "What common mistakes can weaken a truck accident wrongful death claim?",
 "When should a grieving family contact an attorney after a fatal truck crash?",
 "What is the single most important thing for a family to understand about a fatal truck claim?",
 "How does the deceased driver being partly at fault affect a wrongful death claim?",
 "How do hours-of-service and electronic logs prove fault in a fatal truck case?",
]

SPEC = {
 "topic": "truck accidents",
 "episode_title": "Wrongful Death from a Truck Crash",
 "episode_number_token": "E5",
 "episode_goal": "Authority",
 "topic_phrase": "what a family is actually facing after a fatal truck crash",
 "setup": ("I'm **{{INTERVIEWER}}**, and today we are talking about something no family in Florida ever "
           "plans for, losing someone in a crash with a truck, and how much of what happens next is settled in the first week."),
 # L3-F, the bench behind them.
 "credential": ("**{{ATTORNEY}}**, your firm has the investigators and the specialists lined up before most "
                "families have even figured out who to call."),
 # L4-B, the decision. `Tell us` because who files and what to ask is a judgment call.
 "prompt": ("A family is deciding whether to call anyone at all. Tell us what they should be asking. "
            "And if you have one where calling early changed how it ended, take us through it."),
 "attributes": ATTRIBUTES,
 "locations": LOCATIONS,
 "bank": BANK,
 # Rows 1-10 of the live Doc bank, in Doc order, tail-truncated. No reordering.
 "ref_fmt": "TP-AT-WrongfulDeathTruck-R{n}",
 "outro": {
   "thanks": ("**{{ATTORNEY}}**, thank you for your time. Most families never hear any of this until they are "
              "living it. You just laid it out."),
   "signoff": "We will leave it there. This is **{{PODCAST_NAME}}**, and we will see you next episode.",
   "reach": ("One more thing, if you are in Florida and need a lawyer, reach out "
             "to **{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or find them at **{{WEBSITE}}**."),
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
   "outro_line3_slots": ["One more thing,", 3, "reach out to", 2],
 },
}

if __name__ == "__main__":
    emit(SPEC, "out")
