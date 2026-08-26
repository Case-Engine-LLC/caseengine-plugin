# N-Gram Table Examples

> **QUESTION TEXT CALIBRATION - READ THIS SECTION FIRST.**
> The worked tables further down this file remain valid for the **N-grams / Entities / Predicates** columns. Their **Question Text** column is SUPERSEDED by the pairs below - several of those questions are the exact failure mode this section exists to kill. Calibrate question voice here; calibrate column density there.

## BAD -> GOOD: the 2026-08-21 editorial pass

Source: Eberst Advantage E2, E3, E4 (Stuart + Gainesville, v2 open-interview). Thirty generated questions went to editorial; **twenty-two were rewritten before air, eight shipped clean.** Every pair below is real. `BAD` is what the pipeline generated. `GOOD` is what a human put in the host's mouth.

The governing difference in every single pair: **BAD is written from OUTSIDE the situation, describing a topic. GOOD is written from INSIDE it.**

### Person - kill abstract placeholders

| BAD | GOOD | Rule |
|---|---|---|
| What should you do at the scene of a car accident in Stuart? | I was just in a car accident in Stuart, what do I do? | First-person crisis voice |
| Where does **someone** badly hurt in a Stuart crash actually get treated? | If you're badly hurt in a Stuart crash, where do they take you? | `someone` banned; scenario-first |
| How does **anyone** actually put a number on pain and suffering? | How do **you** actually put a number on pain and suffering? | `you` = the attorney's experience. Note `actually` SURVIVES here - genuine curiosity aimed at the attorney is the one exemption |
| What kinds of crashes actually happen most around Stuart? | What kinds of crashes do **you** see most in Stuart? | Address the attorney's experience |

### Scenario first, question second

| BAD | GOOD |
|---|---|
| How long do you have to see a doctor after a crash in Florida? | If I don't see a doctor right after an accident in Florida will that affect my PIP benefits? |
| Does Florida still pay you if the crash was partly your fault? | If you're partly at fault for a car accident in Florida, will your insurance still cover it? |
| Why does an injury that shows up two days later still count? | What if you felt fine at the scene and woke up hurting two days later? |
| Who writes the crash report in Stuart and across the Treasure Coast? | If you crash in Stuart, who writes the report, Stuart PD or the Martin County Sheriff's Office? |

### Concrete instance beats category

| BAD | GOOD | Rule |
|---|---|---|
| Does **Florida** still pay you...? | ...will **your insurance** still cover it? | A state does not pay you. Name the real actor |
| What changes when a **commercial vehicle** causes the crash in Stuart? | What changes when a **box truck or delivery van** causes your crash in Stuart? | Concrete instance. Note: these are NOT entity-map entities - vividness is allowed in question text |
| **What happens** if the other driver has no insurance? | **Who pays** if the other driver doesn't have insurance? | Vague interrogative -> the real question |

### Named-entity forks (max ONE per episode table)

| BAD | GOOD |
|---|---|
| Who responds to a car accident in Stuart and across the Treasure Coast? | Who responds to a car accident in Stuart, the Martin County Sheriff's Office or the Stuart PD? |
| Who responds to a car accident in Gainesville and across North Central Florida? | Who responds to a car accident in Gainesville, the Alachua County Sheriff's Office or University of Florida Police? |

### Region pairing - deleted 6 of 6 times, no survivors

`and across the Treasure Coast` x2 - `and across North Central Florida` x2 - `or across the Treasure Coast` x1 - `or across North Central Florida` x1. **Never in spoken question text.** Regional retrieval intent lives in the N-grams column and the answer bullets.

### Covert listicles - reframe enumeration into stake or motive

| BAD | GOOD |
|---|---|
| **Which witnesses matter most**, and how fast do they disappear? | **Why do you have to** get a witness's name and number right at the scene? |
| **What medical records** actually prove an injury after a crash in Stuart? | **How much of your case comes down to** your medical records? |
| What evidence disappears first after a crash? | What evidence should be gathered at the scene of a car accident? |

### Writerly hooks and loaded premises

| BAD | GOOD | Rule |
|---|---|---|
| **Why does** settling early **cost the most**? | **What do you give up by** settling early? | The BAD version pre-answers itself |
| What evidence **disappears first** after a crash? | What evidence **do you lose by waiting**? | Evidence does not vanish on its own. Frame it as the listener's own delay. (The GOOD line here shipped unedited) |

### Plain searchable interrogative, and the `actually` ban

| BAD | GOOD | Rule |
|---|---|---|
| What is a car accident claim **actually worth** in Stuart? | **How much is** a car accident claim worth in Stuart? | |
| How do you **actually** get a copy of your Florida crash report? | How do you get a copy of your Florida crash report? | `actually` was the ONLY delta in this pair |
| What kinds of crashes **actually** happen most around Stuart? | What kinds of crashes do you see most in Stuart? | |

### Trailing purpose clauses - fold the purpose in

| BAD | GOOD |
|---|---|
| What should you do at the scene of a crash in Stuart **to protect the report**? | How do you make sure the crash report gets your side right? |

### Ambiguity repair, and hedge-trimming

| BAD | GOOD | Rule |
|---|---|---|
| How does **where you got hit** in Stuart change the fight over fault? | How does **where the crash happened** in Stuart change the fight over fault? | Body part or location? |
| What happens to your case if your back **or your knee** was already bad? | What happens to your case if your back was already bad **before the crash**? | Cut the hedge, add the temporal anchor |
| How does anyone put a number...? | (see Person section) | |

**But KEEP a real second beat:**

| KEPT AS-IS | Why |
|---|---|
| How do I get video of my crash in Stuart, and how long before it's gone? | Two genuine beats, not a hedge. Compound is fine here |

### Grammatical number - match reality

| BAD | GOOD | Rule |
|---|---|---|
| What is the most common **mistake** people make after a crash? | What are the most common **mistakes** people make after a crash? | Several exist; forcing one is artificial |
| What **single piece** of evidence wins the most car accident cases in Florida? | *(shipped unedited)* | Singular is CORRECT when forcing the attorney to commit to one pick is the point |

### The city must earn its place - two lanes only

**Substance lane** (the answer differs by city) and **ranking lane** (deliberate money-phrase target, cap 2-3 per location set). Neither lane = **cut the city.**

| BAD - city serves neither lane | GOOD - city removed |
|---|---|
| What should you do at the scene of a crash **in Stuart** to protect the report? | How do you make sure the crash report gets your side right? |
| What medical records actually prove an injury after a crash **in Stuart**? | How much of your case comes down to your medical records? |

| KEPT - substance lane | KEPT - ranking lane |
|---|---|
| Who writes the report, Stuart PD or the Martin County Sheriff's Office? | How much is a car accident claim worth in Stuart? |
| How do I get video of my crash in Stuart, and how long before it's gone? | How long do you have to file a car accident lawsuit in Stuart? |
| If you're badly hurt in a Stuart crash, where do they take you? | I was just in a car accident in Stuart, what do I do? |

Measured city share across the three revised episodes: **40% / 40% / 20%**, averaging ~33% - produced by the two-lane test, NOT by a quota.

### Carryover - city-free questions are byte-identical across locations

In E4, the revised Q1, Q3, Q7 and Q8 are character-for-character identical between Stuart and Gainesville. That is correct and intended. Only lane-justified city questions vary per location.

## GOOD - shipped unedited (the pass set)

These eight cleared editorial with zero changes. This is the target.

- Why does the insurance company want a recorded statement?  *(the single best model in the set: concrete actor, concrete artifact, reveals motive, no geo, no cleverness)*
- How long do you have to file a car accident lawsuit in Stuart?
- Does the kind of crash you were in change what the case is worth in Florida?
- What deadlines end a Florida injury case before it ever starts?
- Does the police report decide who was at fault in Florida?
- What do you do when the crash report gets the facts wrong?
- What evidence do you lose by waiting?
- What single piece of evidence wins the most car accident cases in Florida?

Note what these share: state law is named as **state** law with no city bolted on; every one names a concrete artifact or actor; none contain `actually`; none are clever.

---


Read before generating. These calibrate what GOOD / BAD / EDGE CASE look like for this skill.

## Format

Each example is a labeled section (`## GOOD` / `## BAD` / `## EDGE CASE`) in this single file - per CE convention, one `{type}-examples.md` doc, never split into separate files. Each example carries a short header block declaring `label`, `scope`, `run_date`, `topic`, `episode`, `location` (if applicable), `source`, `why_this_label`, and `known_flaws` (null if none), followed by the verbatim output - the full 4-column table.

## GOOD

### Full Location-scope N-Gram Table (Savannah, GA)

- **label:** GOOD
- **scope:** Location
- **run_date:** 2026-04-06
- **topic:** Car Accidents / How to File a Claim
- **episode:** How to File a Car Accident Claim in Savannah, Georgia
- **location:** Savannah, GA (Chatham County)
- **source:** Real production run - `deliverables/podcast-research/car-accidents/2. how-to-file-car-accident-claim/locations/ga-savannah/03-n-gram-table/`
- **drive_doc:** https://docs.google.com/document/d/1Vqz__TMxeXV7ye3oN9Mo6QklKo-lPmNzdalYBEWd9zs/edit
- **why_this_label:** Strong jurisdiction grounding (O.C.G.A. citations before any Q&A). Explicit deduplication log with reasoning for each merge (4 merges documented with WHY). Local entity density averages ~3 entities per question with Savannah-specific anchors (Memorial Health University, St. Joseph's/Candler, Chatham County Superior Court, I-16, Victory Drive). Predicates are action-verbs ("call 911", "file a claim", "preserve evidence") not nouns. Jurisdiction-specific procedure captured (ante-litem notice - O.C.G.A. 36-33-5 - rarely surfaces in generic GA tables but is critical for claims against GA government entities). Location extension pulls real Savannah context (tourist traffic, Victory Drive, DeRenne Avenue, I-16) rather than generic Georgia content.
- **known_flaws:**
  - Template Version listed as 2.0 (canonical has since advanced; minor version drift).
  - No explicit segment/arc grouping in the table itself (segment breakdown happens downstream in ROS Template).
  - Result line says "30 generated, 4 merged, 26 final" but the table renumbers Q1-Q26 sequentially rather than preserving original question IDs with merge annotations - minor traceability gap.
  - SEPARATOR DEVIATION: Entities column uses comma separator throughout. Best Practices -> Localization table requires semicolon (`;`) for City-level Location scope.
  - ACRONYM DEVIATION: Entity names are written as plain names with no acronym. Best Practices -> Localization table requires the standard `Full Name (ACRONYM)` convention for City-level Location scope.
  - ENTITIES-PER-ROW DEVIATION: Best Practices -> Localization table requires 3-5 entities per row for City-level Location scope. Q2, Q3, Q4, Q7, Q8, Q9, Q10, Q12, Q21, Q22 fall short of 3. Ten of 26 rows (38%) are under-populated.

Read the header block above before reading the table. This example is GOOD for Jurisdiction Context grounding, Dedup Log rigor, localized question framing, and verb-first predicates. It is NON-CANONICAL on three formatting rules listed in `known_flaws` and summarized in the "Deviations from current canonical" subsection at the bottom of this example. Everything else is verbatim production output from the 2026-04-06 run.

#### N-Gram Table: How to File a Car Accident Claim in Savannah, Georgia

Internal metadata (INTERNAL block / JSON `internal` only - never in the client-facing Doc body): Topic Car Accidents / Filing Claims, Industry Personal Injury Law, Location Savannah GA (Chatham County), Created 2026-04-06, Skill pod-2B-n-gram-table.

**Jurisdiction Context**

- Georgia is an at-fault (tort) state
- Modified comparative negligence: barred at 50%+ fault (O.C.G.A. Section 51-12-33)
- Statute of limitations: 2 years personal injury (O.C.G.A. Section 9-3-33), 4 years property damage (O.C.G.A. Section 9-3-30)
- Minimum auto insurance: $25,000/$50,000/$25,000
- Crash report: Georgia Uniform Motor Vehicle Accident Report (SR-13) filed with Georgia DDS
- Courts: Chatham County State Court, Chatham County Superior Court
- NOT a no-fault state; no PIP requirement

**Deduplication Log**

- Merged "Should I call the police even if the accident seems minor?" into Q1 (scene steps). The police-call answer is a subset of the immediate-steps answer.
- Merged "Which insurance company should I contact first?" into Q7 (step-by-step claim filing). The "who to call first" answer is fully contained within the step-by-step walkthrough.
- Merged "Should I give a recorded statement?" into Q9 (what to say to an adjuster). The recorded statement question is a direct subset of the adjuster-tactics question.
- Merged "How long does a claim take?" into Q13 (settlement vs lawsuit). Timeline information overlaps heavily with the resolution-path discussion.

Result: 30 questions generated, 4 merged, 26 final questions.

| Question Text | N-grams to Mention | Entities to Mention | Predicates to Mention |
|---|---|---|---|
| Q1: What should someone do immediately after a car accident in Savannah to protect their claim? | immediately after a car accident, first steps after a car crash in Savannah, protect your claim from the scene, police report for minor accident Georgia, call 911 after car accident Savannah | Savannah Police Department, Chatham County Police Department, Georgia State Patrol, 911 Chatham County | call 911, move to safety if possible, exchange insurance and contact information, document the scene with photos and video, collect witness names and contact information, request a police report even for minor collisions |
| Q2: Are you legally required to report a car accident to the state of Georgia? | Georgia accident reporting requirements, SR-13 form Georgia, report car accident to Georgia DDS, Georgia Uniform Motor Vehicle Accident Report | Georgia Department of Driver Services, Official Code of Georgia Annotated | file the SR-13 form with Georgia DDS within 30 days, report accidents involving injury death or property damage over $500, understand that the police report is separate from the state report, failure to file can result in license suspension |
| Q3: Where should someone in Savannah go for medical care after a crash even if they feel fine? | delayed injury symptoms after car accident, medical evaluation after car accident Savannah, medical records for car accident claim Georgia | Memorial Health University Medical Center, St. Joseph's/Candler Hospital | seek medical evaluation within 72 hours, document all injuries and treatment, understand that adrenaline masks pain and symptoms, maintain a continuous treatment record without gaps |
| Q4: How does Georgia's fault-based insurance system work for car accident claims? | Georgia fault state car accident, Georgia at-fault insurance system, tort liability Georgia car accident, who pays after car accident Georgia | Georgia General Assembly, Georgia Office of Insurance and Safety Fire Commissioner | determine fault based on evidence and police report, file a claim against the at-fault driver's liability insurance, understand that Georgia does not require PIP coverage, file through your own collision coverage as an alternative |
| Q5: What are Georgia's minimum auto insurance requirements and why do they matter? | Georgia minimum car insurance requirements, 25/50/25 auto insurance Georgia, Georgia liability coverage limits | Georgia Office of Insurance and Safety Fire Commissioner, Georgia Department of Driver Services, Official Code of Georgia Annotated | carry minimum liability of 25/50/25, understand that minimum coverage often falls short of serious injury costs, know that Georgia insurers must offer UM/UIM coverage, verify the other driver's coverage through the police report |
| Q6: How does Georgia's modified comparative negligence rule affect what you can recover? | Georgia comparative negligence rule, 50 percent bar rule Georgia, modified comparative fault Georgia car accident, O.C.G.A. Section 51-12-33 | Georgia General Assembly, Official Code of Georgia Annotated, Chatham County Superior Court | reduce damages by your percentage of fault, understand that 50 percent or more fault bars recovery completely, know that insurers aggressively argue higher fault percentages, preserve evidence that supports the other driver's negligence |
| Q7: Walk through the step-by-step process of filing a car accident insurance claim in Georgia. | how to file car insurance claim Georgia, car accident insurance claim process Savannah, step by step claim filing Georgia, first-party claim vs third-party claim Georgia | Georgia Office of Insurance and Safety Fire Commissioner, National Association of Insurance Commissioners | notify your own insurer promptly after the accident, file a third-party claim against the at-fault driver's insurer, provide the police report photos medical records and witness statements, submit a demand letter once treatment is complete, contact your own insurer first if fault is unclear |
| Q8: What types of damages can someone recover in a Savannah car accident claim? | car accident damages Georgia, economic damages car accident Savannah, non-economic damages Georgia personal injury, pain and suffering Georgia | Georgia General Assembly, Official Code of Georgia Annotated | recover medical expenses past and future, claim lost wages and diminished earning capacity, seek compensation for pain and suffering, pursue property damage repair or replacement costs |
| Q9: What should you say and not say to an insurance adjuster after a Savannah car accident? | dealing with insurance adjuster after car accident, insurance adjuster tactics Georgia, what to say to insurance adjuster, recorded statement insurance company Georgia | Georgia Office of Insurance and Safety Fire Commissioner | provide only basic facts about the accident, avoid speculating about fault or injuries, do not give a recorded statement without consulting an attorney, do not accept the first settlement offer, refer the adjuster to your attorney |
| Q10: What are the most common tactics Georgia insurance companies use to reduce or deny claims? | insurance company deny car accident claim Georgia, lowball settlement offer car accident, bad faith insurance practices Georgia, delay tactics insurance companies | Georgia Office of Insurance and Safety Fire Commissioner, Georgia Department of Law | recognize delay tactics designed to pressure quick settlement, dispute liability determinations that assign excessive fault, document all communication with the insurance company, know that Georgia allows bad faith penalties up to 50 percent plus attorney fees |
| Q11: What evidence beyond photos and medical records can make or break a car accident claim in Savannah? | car accident evidence collection Savannah, dashcam footage car accident, witness statements car accident claim Georgia, traffic camera footage Savannah | Savannah Police Department, Georgia State Patrol, Georgia Department of Transportation, National Highway Traffic Safety Administration | obtain traffic camera or dashcam footage, collect witness statements as soon as possible, preserve cell phone records to address distracted driving, request the full police accident report with diagrams |
| Q12: How do medical records and documentation affect a car accident settlement in Georgia? | medical records settlement value Georgia, injury documentation personal injury claim, treatment gap car accident claim, medical lien Georgia | Memorial Health University Medical Center, St. Joseph's/Candler Hospital | prove injuries are directly linked to the accident, maintain continuous treatment without gaps, obtain a written prognosis from your treating physician, understand that Georgia allows medical liens on settlements |
| Q13: When should someone settle a car accident claim versus filing a lawsuit in Chatham County? | settlement vs lawsuit car accident Georgia, car accident settlement timeline Savannah, filing a lawsuit car accident Chatham County, how long does car accident claim take Georgia | Chatham County Superior Court, Chatham County State Court, Georgia Judicial Branch | weigh the certainty of a settlement against the risk of trial, expect straightforward claims to settle in six to twelve months, prepare for litigation to take one to three years, calculate whether the settlement covers all current and future damages |
| Q14: How long do you have to file a car accident lawsuit in Georgia and what happens if you miss it? | statute of limitations car accident Georgia, two year statute of limitations personal injury Georgia, O.C.G.A. Section 9-3-33, missed filing deadline car accident Georgia | Georgia General Assembly, Official Code of Georgia Annotated, Chatham County Superior Court | file a personal injury lawsuit within two years of the accident, file property damage claims within four years, understand that missing the deadline results in permanent dismissal, know that filing an insurance claim does not pause the lawsuit clock |
| Q15: Are there situations in Georgia where the deadline gets extended or shortened? | tolling statute of limitations Georgia, minor car accident claim Georgia, government vehicle accident claim Georgia, ante-litem notice Georgia | Georgia General Assembly, Official Code of Georgia Annotated, O.C.G.A. Section 36-33-5, Chatham County Government | toll the statute for minors until they turn 18, file an ante-litem notice within six months for claims against Georgia cities and counties, identify whether any exceptions apply to your specific situation |
| Q16: How is fault determined in a car accident claim in Savannah? | determining fault car accident Georgia, liability assessment car accident Savannah, police report fault determination Georgia | Savannah Police Department, Georgia State Patrol, Chatham County Superior Court | investigate the accident using the police report as a starting point, review physical evidence photos and witness accounts, understand that the police report is influential but not binding, know that fault can be disputed in court |
| Q17: Can you still file a claim if you were partially at fault for the accident in Georgia? | partially at fault car accident Georgia, shared fault claim Georgia, reduced compensation comparative negligence Georgia | Georgia General Assembly, Official Code of Georgia Annotated, Chatham County State Court | recover damages as long as you are less than 50 percent at fault, expect your compensation to be reduced by your fault percentage, understand that one percentage point at the 50 percent line changes everything, preserve evidence that minimizes your share of fault |
| Q18: What happens if the other driver does not have insurance or flees the scene in Savannah? | uninsured motorist claim Georgia, hit and run accident Savannah, UM/UIM coverage Georgia car accident | Georgia Office of Insurance and Safety Fire Commissioner, Savannah Police Department, Georgia State Patrol | file an uninsured motorist claim with your own insurance carrier, report a hit and run to Savannah Police immediately, provide any identifying information about the fleeing vehicle, know that Georgia law requires insurers to offer UM/UIM coverage |
| Q19: When should someone seriously consider hiring a car accident attorney in Savannah? | when to hire car accident lawyer Savannah, do I need a car accident attorney Georgia, Savannah car accident attorney free consultation | State Bar of Georgia, Savannah Bar Association, Chatham County Superior Court | consult an attorney when injuries require ongoing treatment, hire a lawyer when liability is disputed, seek legal representation before accepting any settlement offer, consult an attorney if dealing with a commercial vehicle or government entity |
| Q20: What should someone look for when choosing a personal injury attorney in Savannah? | best car accident lawyer Savannah, how to choose personal injury attorney Georgia, Savannah personal injury attorney reviews | State Bar of Georgia, Savannah Bar Association, Georgia Trial Lawyers Association | verify the attorney is in good standing with the State Bar of Georgia, ask about their experience with car accident cases specifically, confirm they work on a contingency fee basis, ask about their trial record in Chatham County courts |
| Q21: How does the contingency fee structure work and what does it actually cost the client? | contingency fee personal injury lawyer Georgia, car accident lawyer fees Savannah, how much does car accident attorney cost Georgia | State Bar of Georgia, Georgia Rules of Professional Conduct | pay nothing upfront under a contingency fee arrangement, understand that the attorney typically takes 33 percent of the settlement, clarify who pays for litigation costs if the case is lost, know that the percentage may increase if the case goes to trial |
| Q22: What are the most common mistakes that seriously hurt a car accident claim in Georgia? | mistakes after car accident that hurt your case Georgia, car accident claim mistakes to avoid, things not to do after car accident Savannah | Georgia Office of Insurance and Safety Fire Commissioner, National Highway Traffic Safety Administration | avoid posting about the accident on social media, do not delay seeking medical treatment, never admit fault at the scene of the accident, keep all medical appointments without exception, do not sign anything from the insurance company without attorney review |
| Q23: What does the litigation process look like if a car accident case goes to trial in Chatham County? | car accident lawsuit process Georgia, personal injury trial Chatham County, filing a lawsuit car accident Savannah | Chatham County Superior Court, Chatham County State Court, Georgia Judicial Branch | file a complaint in the appropriate Chatham County court, complete discovery including depositions and interrogatories, present evidence and testimony at trial, understand that a jury in Chatham County decides fault and damages |
| Q24: What special considerations apply if a commercial truck or delivery vehicle caused the accident? | truck accident claim Savannah, commercial vehicle accident Georgia, 18 wheeler accident liability Savannah, trucking company negligence Georgia | Federal Motor Carrier Safety Administration, Georgia State Patrol, National Transportation Safety Board | request the truck driver's logbook and hours of service records, investigate whether the trucking company violated federal safety regulations, identify all liable parties including driver employer and vehicle manufacturer, know that evidence from commercial vehicles must be preserved quickly |
| Q25: How do Savannah-specific factors like tourist traffic and road conditions affect car accident claims? | Savannah car accident hotspots, I-16 car accident Savannah, Victory Drive accidents Savannah, DeRenne Avenue traffic Savannah, tourist traffic Savannah car accident | Georgia Department of Transportation, City of Savannah, Chatham County Government | document road conditions including potholes or construction zones, note whether tourist traffic congestion contributed to the accident, identify whether the city or county is responsible for road maintenance failures, file an ante-litem notice if a government entity caused or contributed to the crash |
| Q26: What final advice would you give someone in Savannah who was just in a car accident? | what to do right now after car accident Savannah, car accident next steps Georgia, protect your car accident claim Savannah | State Bar of Georgia, Savannah Bar Association, Georgia Office of Insurance and Safety Fire Commissioner | document everything from the moment the accident happens, seek medical attention even if you feel okay, do not speak to the other driver's insurance without consulting an attorney, consult a qualified Savannah car accident attorney as soon as possible |

#### Calibration Summary

Future runs should replicate these six rules. If an output misses any, it is below GOOD threshold:

1. **Jurisdiction Context block always precedes the table.** Include specific statutory citations (O.C.G.A. / state code), not vague "[state] law" references. Include negative-space anchors (what the state is NOT - no-fault, no PIP, etc.) to prevent cross-contamination from similar-looking states.
2. **Deduplication Log is first-class deliverable.** Show every merge with what/where/why. Target merge count: 10-20% of initial generation (4/30 = 13%, healthy range).
3. **Location anchors live IN the question text**, not as a bolted-on suffix. "in Savannah" appears mid-sentence, not at the end in parens.
4. **N-grams blend broad + local.** Every row should carry at least one broad head-term n-gram AND at least one location-specific long-tail variant.
5. **Entities skew specific-regional.** Generic state-level entities are allowed but should not be the only entities. If every row's entities could be swapped city-for-city within the state, the table isn't actually localized.
6. **Predicates are verb-first action phrases.** "file a claim" / "preserve evidence" / "document the scene" - not noun forms ("claim filing" / "evidence preservation").

The single-question stress test: pick any row, ask "if I swapped the location for a different city in the same state, would this row still make sense or would it break?" If every row still works, the table is state-scope dressed up as location-scope. If at least 3-5 rows break, the table is genuinely localized. Q25 is the cleanest break in this example; Q3, Q11, Q19/Q20 also break cleanly. Four genuine breakpoints on a 26-row table is healthy density.

#### Deviations from current canonical

This example is GOOD for the six Calibration Summary rules above. It is NON-CANONICAL on three rules from Best Practices -> Editorial Guideline 1 / the `## INTERNAL` Localization table. Future runs should fix these before writing to Drive.

| # | Rule (section + specific) | What this example does | Scope of deviation |
|---|---|---|---|
| 1 | Localization table: City-level Location uses `;` separator in Entities column | Uses `,` separator throughout | All 26 rows |
| 2 | Localization table: City-level Location uses `Full Name (ACRONYM)` convention (e.g., `Savannah Police Department (SPD)`) | Writes plain names with no acronym | All 26 rows, every acronym-eligible entity |
| 3 | Localization table: City-level Location carries 3-5 entities per row | 10 rows fall below 3 entities | Q2, Q3, Q4, Q7, Q8, Q9, Q10, Q12, Q21, Q22 (Q9 worst at a single entity) |

Reader takeaway: use this example to calibrate Jurisdiction Context grounding, Dedup Log rigor, in-sentence localization of questions, broad-plus-local n-gram blending, specific-regional entity selection, and verb-first predicates. Do NOT copy the Entities-column formatting (separator, acronym form, per-row count). Those three rules were locked in by the 2026-04-20 ship-ready pass and this 2026-04-06 run predates them. A conforming re-run would keep every Question / N-gram / Predicate as-is and only rewrite the Entities column.

## BAD

(none yet - seed from production runs where a table missed the bar. The in-skill `## INTERNAL` reference set carries three canonical reference tables (Topic Only / State / City) as the starting-point quality anchors.)

## EDGE CASE

(none yet - seed when a real run hits a scenario the standard approach does not cover.)
