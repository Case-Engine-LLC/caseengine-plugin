#!/usr/bin/env python3
"""E4 - Police Reports and the Evidence That Wins Car Accident Lawsuits.

Research: car-accidents/police-reports-and-evidence/locations/fl-stuart/03-n-gram-table
(REAL, 10 rows) and .../fl-gainesville/06-ros-template (REAL, 10 questions). The
Gainesville n-gram table itself is a cloud stub; its ROS carries the same substance.
Topic Plan has no Episode 4 breakdown table, so this runs legacy-exempt.

Rotation: line 2 pattern A, line 3 frame E (the local system), line 4 frame C (the
first week), outro credit approach `reps`, sign-off bank index 2.
"""
from common import B, emit
from attributes import ATTRIBUTES as _ATTRS

# --- shared, identical in both sets. What the report is and is not. -----------
SHARED = {
 4: ("STATE", "Does the police report decide who was at fault in Florida?", B(
     ("It is an opinion, not a ruling", "the officer arrived after it happened and wrote down what they were told."),
     ("It usually does not reach a jury", "the report itself is generally kept out at trial, so the case gets rebuilt from the underlying proof."),
     ("It still sets the tone", "the adjuster reads it first and puts a number on your claim long before anyone files a lawsuit."))),
 9: ("NEUTRAL", "What evidence do you lose by waiting?", B(
     ("Video first", "most systems record over the old footage on a loop measured in weeks, not months."),
     ("The vehicles", "both cars get repaired or scrapped, and the damage pattern is half the story."),
     ("The road itself", "skid marks, debris, and the sign that got knocked down are all gone after the next rain or the next work crew."))),
}


def localized(report_portal, witness_note, footage_note, correction_note, verdict_note):
    """Same question, both sets, but every bullet is drawn from that market's research."""
    return {
     3: ("NEUTRAL", "How do you actually get a copy of your Florida crash report?", B(
         ("Start with the number", "get the crash report number from the officer at the scene and the rest is paperwork."),
         ("Then the state portal", "the full long form with the diagram comes from the state crash records portal."),
         ("If nobody came out", report_portal))),
     6: ("NEUTRAL", "What do you do when the crash report gets the facts wrong?", B(
         ("You do not edit it", "once the officer files that report it is a permanent record, and it stays exactly as written."),
         ("You go around it", correction_note),
         ("Then you bury it", "photographs, video, and an independent witness carry a lot more weight than one line in an officer's narrative."))),
     7: ("NEUTRAL", "Which witnesses matter most, and how fast do they disappear?", B(
         ("Get the name and the number", "a phone number written down that day is worth more than any statement taken later."),
         ("Some of them are already leaving", witness_note),
         ("The findable ones", "anyone on the clock nearby, because their employer knows exactly who was working."))),
     10: ("STATE", "What single piece of evidence wins the most car accident cases in Florida?", B(
         ("Video, when it exists", "it ends the argument about what happened faster than anything else in the file."),
         ("Treatment records, when there is no video", "an unbroken run of care from the first visit forward is what proves the injury is real."),
         ("The local piece", verdict_note))),
    }


def geo(city, region, roads, agencies, ers, cameras, court):
    """The four geo-bearing slots. These change completely per location."""
    return {
     1: ("CITY", f"What should you do at the scene of a crash in {city} to protect the report?", B(
         ("Get the officer out there", f"on {roads}, the agency that responds changes with the road, and that agency's report is the one that counts."),
         ("Say what you know and nothing else", "if you guess at a speed or a distance at the scene, that is the line they read back to you a year later."),
         ("Photograph before anything moves", "the cars, the signals, the lane lines, the debris field, and the injuries."),
         ("Leave with the report number", "it is the difference between a phone call and a month of chasing paperwork."))),
     2: ("CITY + REGION", f"Who writes the crash report in {city} and across {region}?", B(
         ("It depends on the road", agencies),
         ("Why that matters to you", "each one keeps its own records, has its own request process, and hands them over on its own timeline."),
         ("Body cameras follow the agency", "whoever responded is holding that footage, and you request it from them and nobody else."))),
     5: ("CITY", f"What video exists after a crash in {city}, and how long do you have to get it?", B(
         ("The cameras are private", cameras),
         ("The clock is short", "most of it runs on a thirty to sixty day loop and then it is simply gone."),
         ("Ask in writing, right away", "a written request to preserve the video is the difference between maybe having it and actually having it."))),
     8: ("CITY", f"What medical records actually prove an injury after a crash in {city}?", B(
         ("Where you were taken", ers),
         ("The first visit sets the baseline", "what you reported on day one is what everything afterward gets measured against."),
         ("Gaps get used against you", "stop treating for a month and the insurance company will argue you had already healed up."),
         ("It ends up in front of that court", f"this is what a jury eventually sees, because the file that goes to the {court} is built out of these records."))),
    }


LOCATIONS = [
 # Stuart. Three responding agencies, no trauma center in town, storefront cameras
 # along US 1, and a witness pool that leaves the state.
 {"name": "Stuart",
  "questions": {**SHARED,
    **localized(
      report_portal="when no officer investigates, you have ten days to file the report yourself, and if you miss that there is no record of the crash at all.",
      witness_note="the tourists are out of state by the next day, and the seasonal residents are gone the minute the season ends.",
      footage_note="",
      correction_note="you can ask the officer to add a supplement, and you make that request to the agency that wrote the report.",
      verdict_note="on a road like I-95 or the Turnpike the highway patrol works the scene, and their file is the deepest one in the case."),
    **geo("Stuart", "the Treasure Coast",
      "I-95, Florida's Turnpike, US 1, Kanner Highway or the Roosevelt Bridge",
      "Stuart Police inside the city, the Martin County Sheriff's Office in the county, and the Highway Patrol on I-95 and the Turnpike.",
      "Cleveland Clinic Martin North runs the emergency room here, and the most serious injuries get transferred out of the county, which means a second hospital and a second set of records.",
      "storefronts, gas stations and banks along US 1 and Kanner Highway, plus the cameras near the Roosevelt Bridge.",
      "Martin County courthouse")}},

 # Gainesville. Four responding agencies including a campus force, a Level I trauma
 # center in town, student housing cameras, and a witness pool that turns over by semester.
 {"name": "Gainesville",
  "questions": {**SHARED,
    **localized(
      report_portal="when no officer investigates, you have ten days to file the report yourself, and on campus that goes to the university police.",
      witness_note="the students are gone at the end of the semester, and a game day crowd is out of town by that night.",
      footage_note="",
      correction_note="you can ask the officer to add a supplement, and with four agencies writing reports in this town, the first job is finding out which one wrote yours.",
      verdict_note="a bus rider is one of the easiest witnesses to track down, because the route, the time and the bus number are all written down."),
    **geo("Gainesville", "North Central Florida",
      "I-75, Archer Road, University Avenue or 13th Street",
      "Gainesville Police in the city, the Alachua County Sheriff's Office in the county, University of Florida Police on campus, and the Highway Patrol on I-75.",
      "UF Health Shands is the trauma center here and North Florida Regional is on Archer Road, so the serious cases stay in town and the records stay in one place.",
      "businesses along Archer Road and University Avenue, the student housing complexes, and the university's own cameras, which have their own request process.",
      "Alachua County courthouse")}},
]

ATTRIBUTES = _ATTRS[4]

# Verbatim from the Stuart n-gram table (REAL) and the Gainesville ROS question set
# (REAL). Bank rows ship unedited, statute references included, per editorial-rules.md.
BANK = [
 "To start, why is the Florida Traffic Crash Report often the most important document in a car accident case, and which agency you call depends on the road?",
 "What information is included in a Florida Traffic Crash Report and which fields actually move an injury claim?",
 "What is Florida's accident report privilege and why does the §316.066 inadmissibility of the Florida Traffic Crash Report itself surprise so many claimants?",
 "Can an officer's opinion about who was at fault influence a Florida car accident lawsuit, especially when modified comparative negligence under §768.81 and HB 837 hangs on a single percentage point?",
 "How important are scene photographs when building a compensation case, and how does Florida Evidence Code §90.901 authentication apply on bridge or interstate crashes?",
 "How can dashcam, surveillance, and body camera footage impact an accident claim, and what authentication and preservation rules apply?",
 "How do attorneys use expert witnesses to strengthen accident compensation cases, and how does Florida Evidence Code §90.702 govern admissibility under Daubert?",
 "Accident reconstruction is often mentioned in serious cases - how does it help prove what really happened in a bridge approach crash or an interstate multi-vehicle pileup?",
 "Why do witness statements often play a decisive role in proving liability, especially when the Florida crash report is privileged under §316.066 and the witness pool is transient?",
 "What role do medical bills and treatment records play in determining compensation amounts, and how does Letters of Protection admissibility post-HB 837 factor in?",
 "What role do medical records play in proving injuries after a crash, and how do PIP timing under §627.736 and the Florida bodily injury causation standard interact?",
 "Why do some injury cases settle quickly when strong evidence is available, and how does the §768.79 Proposal for Settlement accelerate resolution against Florida insurers?",
 "How does evidence drive comparative-fault allocation under §768.81 modified comparative negligence after HB 837, particularly on an ambiguous merge or a multi-vehicle pileup?",
 "Can a weak Florida Traffic Crash Report be overcome with stronger independent evidence in an injury case, especially when comparative fault is contested under §768.81?",
 "How does spoliation of evidence under Florida Rules of Civil Procedure 1.380 support sanctions and an adverse-inference instruction?",
 "How does the sovereign-immunity written presentment requirement under §768.28 apply when a government vehicle is involved?",
 "How does uninsured motorist coverage under §627.727 depend on the crash report in a hit-and-run claim?",
 "What is the Florida Department of Financial Services mediation program and when does it help resolve a claim?",
 "How does statutory bad faith under §624.155 change an insurer's posture once the evidence is assembled?",
 "Finally, what are the most powerful pieces of evidence that tend to win car accident lawsuits, and how does HB 837's two-year SOL under §95.11 force fast collection?",
]

SPEC = {
 "topic": "car accidents",
 "episode_title": "Police Reports and the Evidence That Wins Car Accident Lawsuits",
 "episode_number_token": "E4",
 "episode_goal": "Authority",
 "topic_phrase": "what a crash report actually proves and what evidence wins the case",
 "setup": ("I'm **{{INTERVIEWER}}**. Today we are getting into what actually proves a car accident case "
           "in Florida. We will start with the police report, and what you need to know if you are "
           "ever in a crash."),
 # L3-E, the local system. No city named, because this template serves two of them.
 "credential": ("**{{ATTORNEY}}**, you have been in front of these judges and across the table from these "
                "adjusters for **{{YEARS_PRACTICING}}** years."),
 # L4-C, the first week. Situation, imperative ask, conditional story invitation.
 "prompt": ("Someone just got a copy of their crash report. Walk us through what actually matters in it. "
            "And if you have had one where the report got it wrong, tell us how you turned that around."),
 "attributes": ATTRIBUTES,
 "locations": LOCATIONS,
 "bank": BANK,
 "ref_fmt": "E4-legacy-R{n}",
 "outro": {
   "thanks": ("**{{ATTORNEY}}**, thanks for walking through all of that. You can tell you have read a lot of these."),
   "signoff": "That is the episode. **{{PODCAST_NAME}}**. We will see you on the next one.",
   "reach": ("And before you go, if you are anywhere in Florida and need help with this, get in touch with "
             "**{{FIRM_NAME}}**. The number is **{{PHONE_NUMBER}}**, and the site is **{{WEBSITE}}**."),
 },
 "metadata": {
   "topic_plan_reconciled": "legacy-exempt",
   "topic_plan_doc_id": "1P_1tAKXf6_I7EODRnkzDGVhUqPKBncdPKL127YlxgYs",
   "attribute_source": "fallback",
   "attribute_source_pulled": "2026-08-14",
   "attribute_source_confidence": "Inferred",
   "outro_line1_approach": "reps",
   "outro_line2_index": 2,
   "outro_line3_slots": ["And before you go,", 1, "get in touch with", 1],
 },
}

if __name__ == "__main__":
    emit(SPEC, "out")
