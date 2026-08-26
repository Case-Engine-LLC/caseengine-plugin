#!/usr/bin/env python3
"""E10 - Federal Trucking Regulation (FMCSA).

Topic Plan RECONCILED. Live Doc `Episode 10:` table, 25 rows, zero vetoes. S2 ships
rows 1-10 in Doc order, tail-truncated.

Research: truck-accidents/fmcsa-regulations entity map + ROS (both REAL); Stuart truck
entity map REAL; Gainesville locals from the wrongful-death Gainesville n-gram
local_anchors block. Every FMCSA n-gram table on disk is a cloud stub.

TWO SOURCED GAPS, deliberately not asserted anywhere in this build: the ELD data
retention period and the post-crash drug and alcohol testing window. Neither number
appears in any readable source, so the bullets say the records are on a short cycle
without naming a figure. Hours-of-service limits ARE sourced and are stated.

Rotation: line 2 pattern A, line 3 frame A (tenure), line 4 frame B (the decision,
verb `explain` because the rules are a system), outro `reps`, sign-off index 2.
"""
from common import B, emit
from attributes import ATTRIBUTES as _ATTRS

SHARED = {
 3: ("NEUTRAL", "How long is a truck driver actually allowed to drive?", B(
     ("Eleven hours behind the wheel", "and only after ten straight hours off, which is the rule the whole schedule is built around."),
     ("Fourteen hours on the clock", "once that window opens it keeps running through loading, fueling and lunch, and there are only narrow exceptions to it."),
     ("A weekly ceiling too", "sixty hours in seven days, or seventy in eight, plus a required break part way through a driving day."))),
 6: ("NEUTRAL", "What does somebody need to be allowed to drive a truck at all?", B(
     ("A commercial driver's license", "plus extra permissions added on top of it for hauling a tanker, hazardous material, or two trailers at once."),
     ("A current medical card", "the driver has to pass a physical from a doctor on the federal list of approved examiners, and carry the card at all times."),
     ("Training before the test", "new applicants have to complete prescribed training from an approved provider first."))),
 8: ("NEUTRAL", "What are the drug and alcohol rules for truck drivers?", B(
     ("Several different triggers", "before they get hired, at random, after a crash, when a supervisor has a reasonable suspicion, and again on the way back to driving."),
     ("There is a national database", "a company has to check it before hiring and again every year, and a driver with an open violation cannot drive."),
     ("The timing after a crash is tight", "the testing window is short enough that a delay becomes its own evidence, so the records get requested immediately."))),
}

def qs(city, region, corridor, who_regulates, docs_note, eld_note, csa_note,
       dqf_note, maint_note, cargo_note):
    d = {
     1: ("CITY", f"Who actually sets the rules a trucking company near {city} has to follow?", B(
         ("The federal government, not the state", "any truck crossing state lines runs on one national rulebook, whatever road it is on."),
         ("It covers everything", "how long they drive, who is allowed to drive, how the truck is maintained, and how the load is tied down."),
         ("What that means here", who_regulates))),
     2: ("NEUTRAL", "How do the federal rules change what has to be proved?", B(
         ("They set the standard", "there is a written line, so the argument is not about what a careful company would have done."),
         ("Breaking one goes a long way", "when a company breaks a rule that exists to prevent the exact crash that happened, that gets you most of the way there."),
         ("They are all documented", docs_note))),
     4: ("NEUTRAL", "What does the truck itself record about the trip?", B(
         ("The truck logs its own driving", "there is a box wired straight into the engine that records the hours, where the truck went, and how long it ran."),
         ("The driver cannot rewrite it", "it replaced the paper logbook precisely because a paper logbook could be written to suit."),
         ("It does not keep itself", eld_note))),
     5: ("CITY", f"How do you find out whether the company that hit you near {city} had a history?", B(
         ("There is a public safety score", "every trucking company gets scored on unsafe driving, driving hours, maintenance and whether their drivers should be behind the wheel, and anybody can look it up."),
         ("A pattern changes the case", "one violation is an incident, a run of them is how the company operates."),
         ("Where the local record sits", csa_note))),
     7: ("NEUTRAL", "What does a trucking company have to keep on file about its driver?", B(
         ("A full history", "the driving record, the medical certificate, previous employment and the road test."),
         ("It exposes the hiring", "a missing or thin file is evidence about the company, not about the driver."),
         ("You ask for it early", dqf_note))),
     9: ("CITY + REGION", f"How do the inspection and maintenance rules apply after a crash on {corridor}?", B(
         ("The truck gets checked before every trip", "and the driver writes it up before and after, which leaves a paper trail either way."),
         ("A missing write-up is evidence", "if a problem was never written down, either nobody looked, or somebody looked and let it go."),
         ("Roadside records too", maint_note))),
     10: ("CITY", f"How do the rules about tying down a load matter in a {city} crash?", B(
         ("There are actual standards", "how many tie-downs, and how strong, based on what is being carried and how long it is."),
         ("A shifting load causes crashes", "it changes how the trailer behaves before the driver has any idea anything moved."),
         ("It can point at somebody besides the driver", cargo_note))),
    }
    d.update(SHARED)
    return d

LOCATIONS = [
 {"name": "Stuart",
  "questions": qs("Stuart", "the Treasure Coast", "I-95 or the Turnpike",
    who_regulates="most of the trucks moving through Martin County on I-95 and the Turnpike belong to companies hauling across state lines, so the full federal rulebook applies to them.",
    docs_note="every one of those rules generates a record, and on a pass-through carrier those records usually sit in a company office in another state.",
    eld_note="the data sits on the company's own cycle and gets written over, so a written demand has to go out in the first days.",
    csa_note="there is a weigh and inspection station on I-95 in Martin County, so a carrier that came through here may have a roadside inspection record attached to it.",
    dqf_note="the company is the one holding it, so it only comes out through a formal request, and the request has to spell out exactly which records you want.",
    maint_note="anything caught at the I-95 inspection station is on record separately from whatever the company chose to write down.",
    cargo_note="the people who loaded the trailer and the people who arranged the shipment can be on the hook before the driver is, and out here those are usually two separate companies in two other states.")},
 {"name": "Gainesville",
  "questions": qs("Gainesville", "North Central Florida", "I-75",
    who_regulates="I-75 is the freight spine for this whole part of the state, so a truck here is usually interstate, though a local delivery van may be under different rules entirely.",
    docs_note="every one of those rules generates a record, and on a delivery contractor there are often two sets, one at the contractor and one at the company they drive for.",
    eld_note="the data sits on the company's own cycle and gets written over, and on a delivery contractor the vehicle may be back in service the same week.",
    csa_note="the state runs commercial vehicle size and weight inspection on I-75, so the records sit with the state rather than at a single local station.",
    dqf_note="the company is the one holding it, and with a delivery contractor working for a larger company there may be two sets of files at two different employers.",
    maint_note="the state inspection records on I-75 are separate from the company's own write-ups, and a delivery fleet cycles through vehicles fast.",
    cargo_note="the people who loaded it and the people who arranged the shipment can be on the hook before the driver is, and on a delivery route that chain runs back to whoever the van was making deliveries for.")},
]

ATTRIBUTES = _ATTRS[10]

BANK = [
 "What is the FMCSA and why does it matter to a truck accident victim?",
 "How do federal trucking regulations create a standard of care?",
 "What are the hours-of-service rules and how do they prevent driver fatigue?",
 "What is an electronic logging device and how does it track compliance?",
 "What is a CSA score and what does it reveal about a trucking company?",
 "What are the FMCSA's commercial driver's license requirements?",
 "What does the driver qualification file have to contain under federal rules?",
 "What are the federal drug and alcohol testing requirements for truck drivers?",
 "How do federal vehicle inspection and maintenance rules apply to a crash?",
 "What are the federal cargo securement rules and how do violations cause crashes?",
 "How does a federal regulation violation become negligence per se?",
 "How can the FMCSA's records and databases support a truck accident case?",
 "How do hours-of-service violations get proven after a crash?",
 "How does a carrier's pattern of violations strengthen a case?",
 "How does negligent hiring connect to FMCSA driver-screening rules?",
 "Why must FMCSA-related evidence be preserved immediately after a crash?",
 "How do federal trucking rules expand the list of parties who can be liable?",
 "How do FMCSA violations affect the value of a truck accident claim?",
 "How does an attorney use FMCSA regulations to build a truck accident case?",
 "What should a truck accident victim know about the FMCSA before talking to the carrier?",
 "What is post-accident testing and how does the FMCSA require it?",
 "How do FMCSA medical certification rules apply to a truck driver?",
 "How do federal rules treat a carrier that leases drivers or equipment?",
 "How does a federal inspection report become evidence in a truck case?",
 "What is the single most important thing to know about FMCSA rules and a truck crash?",
]

SPEC = {
 "topic": "truck accidents",
 "episode_title": "Federal Trucking Regulation (FMCSA)",
 "episode_number_token": "E10",
 "episode_goal": "Authority",
 "topic_phrase": "the federal rulebook sitting behind every truck on the road",
 "setup": ("I'm **{{INTERVIEWER}}**. Today we are digging into something most people in Florida do not "
           "know exists. There is a federal rulebook every trucking company has to follow, and it "
           "matters enormously if one of their trucks hits you."),
 "credential": ("**{{ATTORNEY}}**, you have spent **{{YEARS_PRACTICING}}** years on the cases most firms "
                "hand straight off to somebody else."),
 "prompt": ("Right now somebody is at home deciding whether their crash is even worth a phone call. "
            "Explain what these federal rules could do for their case. And if you have had one where a "
            "rule violation changed the outcome, take us through it."),
 "attributes": ATTRIBUTES,
 "locations": LOCATIONS,
 "bank": BANK,
 "ref_fmt": "TP-E10-R{n}",
 "outro": {
   "thanks": ("**{{ATTORNEY}}**, I appreciate you taking the time. You do not rattle off the rules on how long a driver can be behind the wheel "
              "like that unless you have had to argue them in front of a judge."),
   "signoff": "That is the episode. **{{PODCAST_NAME}}**. We will see you on the next one.",
   "reach": ("And if nothing else, if you are in Florida and you want somebody to actually look at your crash, "
             "call **{{FIRM_NAME}}**. The number is **{{PHONE_NUMBER}}**, and the site is **{{WEBSITE}}**."),
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
   "outro_line2_index": 2,
   "outro_line3_slots": ["And if nothing else,", 3, "call", 1],
 },
}

if __name__ == "__main__":
    emit(SPEC, "out")
