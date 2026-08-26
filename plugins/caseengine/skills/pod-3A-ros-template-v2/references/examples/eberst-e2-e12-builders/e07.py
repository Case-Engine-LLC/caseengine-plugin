#!/usr/bin/env python3
"""E7 - Drunk Driving Crashes.

Topic Plan RECONCILED. Live Doc `Episode 7:` table, 24 rows, zero vetoes. S2 ships
rows 1-10 in Doc order, tail-truncated.

Research: the Eberst FL n-gram table (REAL, 24 rows) and drunk-driving-crashes/fl-state
entity map (REAL, 50 entities), plus the shipped legacy E7 ROS for both markets (REAL).
Gainesville locals from the Gainesville ROS; Stuart locals from car-accidents/fl-stuart.
NOTE: the research explicitly says Stuart has NO sourced seasonal, waterfront or marina
entity, so no seasonal framing is asserted for Stuart anywhere in this build.

Rotation: line 2 pattern D, line 3 frame D (specific case type), line 4 frame A (the
aftermath, verb `lay out` because the ask is a comparison), outro `reps`, sign-off index 5.
"""
from common import B, emit
from attributes import ATTRIBUTES as _ATTRS

SHARED = {
 4: ("STATE", "What makes an injury serious enough to sue over in Florida?", B(
     ("There is a line", "ordinary soreness gets handled by your own insurance, and it is crossing that line that lets you go after the driver."),
     ("Permanence is the test", "an injury you will carry, a lasting loss of something your body used to do, or scarring that does not go away."),
     ("It is proved with records", "the doctor who treated you and the imaging are what establish it, not how you describe it."))),
 6: ("NEUTRAL", "How reliable is the breath test, really?", B(
     ("It is one machine", "the state uses a single instrument statewide, and it has to be maintained and calibrated on a schedule."),
     ("The paperwork is checkable", "the maintenance and calibration records can be demanded, and gaps in them matter."),
     ("It is not the only proof", "the blood work, the officer's observations and what the driver was doing all stand on their own."))),
 7: ("NEUTRAL", "What happens when the driver refused the breath test?", B(
     ("Refusing is not a clean escape", "the refusal can be shown to a jury, and juries do not think much of it."),
     ("Blood can still be taken", "with a court order, and in a serious crash that is a normal step."),
     ("The rest of the case does not need it", "the driving, the witnesses and the hospital records tell the story without a number."))),
}

def qs(city, region, corridor, agencies, er, court, bars, report_note, pattern_note,
       crim_note, uninsured_note, search_note):
    d = {
     1: ("CITY", f"What makes a case different when a drunk driver caused the crash in {city}?", B(
         ("There is a second case running", "the criminal case moves on its own schedule and your claim does not wait for it."),
         ("The case can be worth more", "when a driver made the choice to drink and drive, a jury can award things they would never award after an ordinary crash."),
         ("Where it happens here", pattern_note))),
     2: ("NEUTRAL", "Does a criminal conviction settle your injury case?", B(
         ("It helps a lot on fault", "a conviction makes it much harder for the other side to argue the driver was being careful."),
         ("It does not set the number", "how badly you were hurt and what it costs you still have to be proved on their own."),
         ("Do not wait for it", crim_note))),
     3: ("STATE", "Can you sue a drunk driver in Florida even though it is a no-fault state?", B(
         ("Yes, once the injury is serious enough", "no-fault pays the first bills, and past that point you can go after the driver directly."),
         ("It changes how they treat you", "the same claim an insurer would grind down after an ordinary crash, they take seriously here."),
         ("Your own coverage still matters", uninsured_note))),
     5: ("CITY + REGION", f"How is it actually proved that the driver was drunk, in {city} and across {region}?", B(
         ("It is layered, not one number", "the breath or blood result, what the officer saw, and how the car was being driven."),
         ("A lot of it is in the report", report_note),
         ("Where they were before", bars))),
     8: ("CITY", f"How does the crash report help an injury claim in {city}?", B(
         ("It captures the first account", agencies),
         ("It usually stays out of court", "the report itself is generally kept out at trial, so the case gets rebuilt from what is underneath it."),
         ("It still drives the number", "the adjuster reads that report long before anyone files anything, and it sets where they start."))),
     9: ("CITY", f"Can you sue the bar that served the driver in {city}?", B(
         ("Almost never", "Florida is one of the strictest states in the country on this, and most claims against a bar go nowhere."),
         ("There are two openings", "serving somebody underage, or serving somebody the bar knew had a serious drinking problem."),
         ("Which one comes up here", bars))),
     10: ("STATE", "Why is it so hard to hold a bar responsible in Florida?", B(
         ("The law was written narrowly", "most states let you sue a bar for overserving an adult, and Florida does not."),
         ("The exceptions are real but small", "underage service, and service to someone known to be habitually addicted."),
         ("It changes where you look", search_note))),
    }
    d.update(SHARED)
    return d

LOCATIONS = [
 {"name": "Stuart",
  "questions": qs("Stuart", "the Treasure Coast",
    corridor="US 1 and Kanner Highway",
    agencies="it gets written by Stuart Police, the Martin County Sheriff's Office, or the Highway Patrol, depending on which road you were on.",
    er="Cleveland Clinic Martin North",
    court="Martin County courthouse",
    bars="the places out along US 1 and Kanner Highway, where nobody walks home, they drive, and they drive fast.",
    report_note="the long form report gets filled out on any serious injury, and the officer's own observations of the driver are in it.",
    pattern_note="late nights on US 1 and Kanner Highway, and on I-95 and the Turnpike, where the speeds turn one bad decision into a life-changing crash.",
    crim_note="the state's case moves through the Martin County courthouse on its own schedule, and the evidence for your claim goes cold in a matter of weeks.",
    uninsured_note="a lot of the drivers on I-95 and the Turnpike are from out of state and insured somewhere else, so the coverage on your own car is often what pays.",
    search_note="with the bar out, the search moves to every policy behind the driver, and out here that regularly means a policy written in another state.")},
 {"name": "Gainesville",
  "questions": qs("Gainesville", "North Central Florida",
    corridor="Archer Road and University Avenue",
    agencies="it gets written by Gainesville Police, the Alachua County Sheriff's Office, University of Florida Police, or the Highway Patrol, depending on which road you were on.",
    er="UF Health Shands",
    court="Alachua County courthouse",
    bars="the bar district next to campus, where somebody serving an underage kid is not a hypothetical, it happens.",
    report_note="the long form report gets filled out on any serious injury, and four different agencies write reports in this town, so the first job is finding out which one has yours.",
    pattern_note="late nights around campus and on game day weekends, when the bar district empties onto Archer Road, University Avenue and I-75.",
    crim_note="the state's case moves through the Alachua County courthouse on its own schedule, and the evidence for your claim goes cold in a matter of weeks.",
    uninsured_note="a lot of the drivers around campus carry the state minimum and nothing more, so the coverage on your own car is often what actually pays.",
    search_note="with the bar out, the search moves to every policy behind the driver, and around campus that regularly means a parent's policy somewhere else.")},
]

ATTRIBUTES = _ATTRS[7]

BANK = [
 "If I was hit by a drunk driver in Florida, what makes my case different from an ordinary crash?",
 "How does a drunk driving conviction turn ordinary negligence into negligence per se under Florida law?",
 "Can I actually sue a drunk driver in Florida even though we are a no-fault state?",
 "What is Florida's serious injury threshold and why does it decide whether I can sue for pain and suffering?",
 "How is the driver's intoxication actually proven in my civil case?",
 "What is the Intoxilyzer 8000 and how reliable is breath-test evidence in Florida?",
 "What does Florida's implied consent law mean for the driver who refused a breath or blood test?",
 "How does the Florida traffic crash report support an injury claim against a drunk driver?",
 "Can I sue the bar or restaurant that served the drunk driver who hit me?",
 "Why is Florida's dram shop law one of the narrowest in the country, and when does it actually apply?",
 "How do punitive damages work in a Florida drunk driving case, and why does intoxication unlock them?",
 "Is there a cap on punitive damages in Florida, and when can that cap be exceeded?",
 "What is my drunk driving accident case actually worth in Florida?",
 "How are medical bills, lost wages, and future care calculated in a serious DUI crash claim?",
 "What happens if the drunk driver who hit me has no insurance or only minimum coverage?",
 "How does my own uninsured and underinsured motorist coverage protect me against a drunk driver?",
 "Does Florida PIP cover me after a drunk driving crash, and where does it fall short?",
 "When can I bring a bad-faith claim against an insurer that refuses to pay fairly?",
 "How does the drunk driver's criminal DUI case affect my separate civil injury claim?",
 "What is criminal restitution, and is it enough on its own to make me whole?",
 "How does a case change when a drunk driving crash causes a DUI manslaughter charge?",
 "Who can file a wrongful death claim when a drunk driver kills a family member in Florida?",
 "How long do I have to file after HB 837 cut Florida's deadline to two years?",
 "Can the drunk driver's lawyer still blame me, and how does Florida's 51% comparative negligence rule work?",
]

SPEC = {
 "topic": "drunk driving crashes",
 "episode_title": "Drunk Driving Crashes",
 "episode_number_token": "E7",
 "episode_goal": "Authority",
 "topic_phrase": "what changes when the driver who hit you had been drinking",
 "setup": ("I'm **{{INTERVIEWER}}**, and today we are getting into crashes caused by a driver who had been "
           "drinking, and what actually changes about your case when that is what happened."),
 "credential": ("**{{ATTORNEY}}**, your firm handles a lot of different injury work, and crashes caused by "
                "impaired drivers are the ones you go deepest on."),
 "prompt": ("Someone was just hit by a drunk driver. Lay out what makes their case different. "
            "And if you have a real-world example, take us through it."),
 "attributes": ATTRIBUTES,
 "locations": LOCATIONS,
 "bank": BANK,
 "ref_fmt": "TP-E7-R{n}",
 "outro": {
   "thanks": ("**{{ATTORNEY}}**, thanks for being so straight about all of it. Nobody answers the bar question "
              "that honestly unless they have had to sit across from somebody and tell them no."),
   "signoff": "That is all we have for this one. **{{PODCAST_NAME}}**. We will see you next time.",
   "reach": ("And one last thing, if you are in Florida and need a lawyer, call **{{FIRM_NAME}}**. "
             "The number is **{{PHONE_NUMBER}}**, and the site is **{{WEBSITE}}**."),
 },
 "metadata": {
   "topic_plan_reconciled": True,
   "topic_plan_doc_id": "1P_1tAKXf6_I7EODRnkzDGVhUqPKBncdPKL127YlxgYs",
   "topic_plan_revision_id": "AIroW34FYjoDNe-pyO0zmcS3bcMOn0H73Q9-m2OO7TkOMdkCNXN_YAGDkb1Jlr9B8vTPL2VOBuKMHeoY85-DOkgVPQZv0OMwEA53iwt4JmQ",
   "topic_plan_fetched_at": "2026-08-18T20:40:06Z",
   "attribute_source": "fallback",
   "attribute_source_pulled": "2026-08-14",
   "attribute_source_confidence": "Inferred",
   "outro_line1_approach": "reps",
   "outro_line2_index": 5,
   "outro_line3_slots": ["And one last thing,", 0, "call", 1],
 },
}

if __name__ == "__main__":
    emit(SPEC, "out")
