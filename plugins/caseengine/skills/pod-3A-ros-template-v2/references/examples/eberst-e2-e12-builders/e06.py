#!/usr/bin/env python3
"""E6 - Commercial Insurance Coverage and Policy Stacks.

Topic Plan RECONCILED. Live Doc `Episode 6:` table, 24 rows, zero vetoes. S2 ships
rows 1-10 in Doc order, tail-truncated.

Research: commercial-insurance-coverage/locations/fl-stuart (Entity Map REAL) and
fl-gainesville (entity-map.json REAL). The fl/03-ngram-ep6 table is a cloud stub;
its REAL metadata.json confirms 24 rows and the two merges. The prior E6 ROS pair on
Drive is a find-and-replace localization of one script - this build does not repeat
that: Stuart is interstate pass-through freight, Gainesville is last-mile and public fleets.

Rotation: line 2 pattern A, line 3 frame A (tenure), line 4 frame E (the other side,
verb `explain` because coverage is a system), outro approach `clarity`, sign-off index 4.
"""
from common import B, emit
from attributes import ATTRIBUTES as _ATTRS

# Rows 6 and 7 are pure policy mechanics. Nothing local attaches to them.
SHARED = {
 6: ("NEUTRAL", "What is the difference between an umbrella policy and an excess policy?", B(
     ("Both sit on top", "neither one pays until the policy underneath it has been used up."),
     ("An excess policy copies the one below it", "same terms, same list of things it will not cover, just a higher ceiling."),
     ("Umbrella can be broader", "it sometimes covers things the policy underneath never did, which is why the wording gets read line by line."))),
 7: ("STATE", "Can you stack insurance policies in Florida?", B(
     ("Sometimes, and it is worth checking", "more than one policy can be added together, and that is often where the real money is."),
     ("A form may have signed it away", "there is a form people sign that trades away stacking for a cheaper premium, and most of them never realize they signed it."),
     ("Go read it", "the one-page summary at the front of the policy from the year of the crash settles the argument, not what anyone remembers choosing."))),
}

def qs(city, region, roads, why_matters, policy_types, uim_note, pip_note, federal_note, limits_note, fleet_note, threshold_note):
    d = {
     1: ("CITY", f"Why does the insurance behind the other vehicle matter so much after a crash in {city}?", B(
         ("A business vehicle is not a car", "the policy behind it is usually many times the size of anything a private driver carries."),
         ("The coverage decides what is possible", "the injury sets what the case is worth, but the insurance behind it sets what you can actually collect."),
         ("Around here specifically", why_matters))),
     2: ("NEUTRAL", "How is a commercial policy different from the car insurance most people have?", B(
         ("It is written for a business", "it covers the vehicle, the driver, and the company running both of them."),
         ("The numbers are not comparable", "a personal policy is written in thousands and a commercial one is often written in millions."),
         ("There is usually more than one", "a business tends to carry layers, and the first policy anybody finds is rarely the only one."),
         ("What that looks like here", fleet_note))),
     3: ("NEUTRAL", "What are policy limits, and why are they the number that matters most?", B(
         ("A policy limit is a ceiling", "no matter how badly somebody is hurt, that policy will not pay a dollar past it."),
         ("It sets the whole strategy", "that number decides how the case gets built and who else gets pulled into it."),
         ("Getting the number in writing", limits_note))),
     4: ("CITY + REGION", f"What kinds of commercial policies turn up in a crash in {city} or across {region}?", B(
         ("It depends on what was on the road", policy_types),
         ("The business itself carries more", "there is often a separate policy covering the company's operations, not just the vehicle."),
         ("Who is named on it matters", "a contractor driving for a larger company may be covered by both, or by neither, and that is a document question."))),
     5: ("NEUTRAL", "What does it actually mean to stack coverage?", B(
         ("Think of it as floors", "the first policy pays to its limit, then the next one starts, then the one above that."),
         ("Every floor is a separate fight", "each insurer above the first one has its own lawyers and its own reasons why the claim is not its problem yet."),
         ("The total is what matters", "the number worth knowing is all of those layers added together, not what the first policy says."))),
     8: ("CITY", f"What happens when the vehicle that hit you in {city} does not have enough coverage?", B(
         ("Your own policy can step in", "the coverage on your own car pays when the other side runs out or never had any."),
         ("It is not automatic", "it has to be claimed, and your own insurer will treat it like any other claim."),
         ("Then look wider", uim_note))),
     9: ("STATE", "How does Florida no-fault fit into a serious injury claim?", B(
         ("It pays first and it is small", "the coverage on your own policy handles the early bills and it runs out fast."),
         ("There is a fourteen-day clock", "see a doctor inside two weeks, or that coverage is gone entirely."),
         ("Serious injuries go outside it", pip_note),
         ("Where that line sits", threshold_note))),
     10: ("CITY", f"What extra protection exists when a truck causes the crash near {city}?", B(
         ("The federal floor", "a carrier running interstate has to carry a minimum set by federal rule, well above any car policy."),
         ("A backstop behind it", "there is a federal guarantee that can force payment to an injured person even when the insurer says the policy does not cover it."),
         ("Where the trucks come from here", federal_note))),
    }
    d.update(SHARED)
    return d

LOCATIONS = [
 # Stuart. Two long-haul corridors, a weigh station on I-95, no trauma center in county,
 # and a winter population insured in other states.
 {"name": "Stuart",
  "questions": qs("Stuart", "the Treasure Coast", "I-95 and the Turnpike",
    why_matters="most of the heavy traffic on I-95 and the Turnpike is freight passing through, so the vehicle that hit you often belongs to a company with far deeper coverage than anyone local.",
    policy_types="on I-95 and the Turnpike it is long-haul freight, and on US 1 and Kanner Highway it is delivery vans and service trucks, and those are different policies entirely.",
    uim_note="a household policy, an employer's policy, and with the number of out-of-state drivers here, sometimes a policy written in another state entirely.",
    pip_note="once an injury is permanent, the case moves past your own coverage and onto the policies behind whoever caused it.",
    federal_note="the trucks through Martin County are mostly running the coast route, and there is a weigh station on I-95 that keeps inspection records on the ones that came through.",
    limits_note="Florida law lets us force the insurer to tell us the limit, and it has to come in writing so nobody can walk it back later.",
    fleet_note="a long-haul trucking company running the coast is insured as an interstate operation, and that policy is far bigger and far better documented than the one on a local van.",
    threshold_note="the serious cases here are moved out of the county for treatment, so the proof that you crossed that line arrives from two hospitals rather than one.")},

 # Gainesville. Last-mile delivery, university and municipal fleets, and the government
 # notice deadline that comes with them. The prior ROS missed this entirely.
 {"name": "Gainesville",
  "questions": qs("Gainesville", "North Central Florida", "I-75 and Archer Road",
    why_matters="between the delivery vans, the university vehicles and the city buses, a lot of the traffic here belongs to an organization rather than a person, and that changes what is behind it.",
    policy_types="on I-75 it is long-haul freight, and around town it is delivery contractors, university vehicles and transit buses, and each of those is a completely different policy to chase.",
    uim_note="a household policy, an employer's policy, and around campus a rideshare policy that only applies during part of the trip.",
    pip_note="once an injury is permanent, the case moves past your own coverage and onto the policies behind whoever caused it.",
    federal_note="I-75 is the freight spine for this whole part of the state, so a truck here is usually interstate and carrying the federal minimum or more.",
    limits_note="Florida law lets us force the insurer to tell us the limit, and if a university, city or county vehicle was involved there is a separate notice that has to go out early.",
    fleet_note="a delivery van may be run by a contractor working for a much larger company, and there is often a policy on each of them.",
    threshold_note="the trauma center is here, so the record that proves how serious it was is complete and it is all in one place.")},
]

ATTRIBUTES = _ATTRS[6]

# Verbatim from the live Topic Plan Doc, `Episode 6:` table, 24 rows.
BANK = [
 "When someone is seriously hurt in a commercial vehicle crash in Florida, why does the insurance behind the at-fault party matter so much?",
 "What is a commercial insurance policy, and how is it different from the personal auto policy most people carry?",
 "What are policy limits, and why are they the single most important number in a serious-injury case?",
 "What kinds of commercial policies can be in play when a business vehicle or a truck causes a crash?",
 "What does it actually mean to 'stack' coverage, and how do primary, excess, and umbrella layers fit together?",
 "How does an umbrella policy work, and how is it different from an excess liability policy?",
 "Can you stack insurance in Florida, and what does the law say about anti-stacking and the non-stacking election?",
 "When the at-fault driver does not have enough coverage, how do uninsured and underinsured motorist coverage step in?",
 "How does Florida PIP / No-Fault coverage fit in, and when does a serious injury let you step outside the No-Fault system?",
 "In a trucking case, what is the MCS-90 endorsement and what does it actually cover for an injured person?",
 "How much insurance are trucking companies required to carry under federal law, and how do those minimums shape a case?",
 "What is bobtail or non-trucking-liability coverage, and why does it create coverage fights after a crash?",
 "Beyond the driver, who else can be on the hook, and how does Florida's dangerous instrumentality doctrine pull in the vehicle owner?",
 "How do negligent entrustment and broker or shipper liability open up additional policies in a trucking case?",
 "What is a self-insured retention, and how is it different from a regular deductible when a big company is behind the crash?",
 "What are captive insurers and fronting policies, and how can they hide or expose a defendant's real coverage?",
 "How do lawyers actually find every insurance policy that might cover an accident?",
 "Does an insurer in Florida have to disclose its policy limits, and what tools force that disclosure?",
 "What does an insurer's duty to defend and duty to indemnify mean, and why does the difference matter to an injured person?",
 "How do policy exclusions and a reservation-of-rights letter become the insurer's way of fighting coverage?",
 "What is insurance bad faith, and how does Florida's bad-faith statute create real pressure to pay full value?",
 "What is a policy-limits demand, and what is the Florida Civil Remedy Notice that has to come before a bad-faith suit?",
 "What happens when the damages are worth more than every policy limit combined?",
 "What is the single most important thing an injured Floridian should understand about commercial coverage and policy stacks?",
]

SPEC = {
 "topic": "commercial insurance coverage",
 "episode_title": "Commercial Insurance Coverage and Policy Stacks",
 "episode_number_token": "E6",
 "episode_goal": "Authority",
 "topic_phrase": "how much insurance is actually behind the vehicle that hit you",
 "setup": ("I'm **{{INTERVIEWER}}**. Today is about something most people in Florida never think about "
           "until it matters. How much insurance is behind the vehicle that hits you, and why that "
           "number decides almost everything."),
 # L3-A, tenure.
 "credential": ("**{{ATTORNEY}}**, you have been taking these cases apart for **{{YEARS_PRACTICING}}** years."),
 # L4-E, the other side. `Explain` because coverage is a system, not a sequence.
 "prompt": ("Somebody is still in a hospital gown and the insurance company is already building its side. "
            "Explain what they are doing in those first days. And if you have watched it play out on a "
            "case, take us through it."),
 "attributes": ATTRIBUTES,
 "locations": LOCATIONS,
 "bank": BANK,
 "ref_fmt": "TP-E6-R{n}",
 "outro": {
   "thanks": ("**{{ATTORNEY}}**, thanks for walking through all of that. That is the first time I have "
              "heard anyone lay out how the layers actually work in plain English."),
   "signoff": "That is a wrap on this one. **{{PODCAST_NAME}}**. See you on the next one.",
   "reach": ("And if nothing else, if you are in Florida and need a lawyer, get in touch with "
             "**{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or find them at **{{WEBSITE}}**."),
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
   "outro_line3_slots": ["And if nothing else,", 2, "get in touch with", 2],
 },
}

if __name__ == "__main__":
    emit(SPEC, "out")
