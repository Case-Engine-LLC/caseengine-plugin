# ROS Template v2 - Examples

Calibration anchors for `pod-3A-ros-template-v2`. Read 1-2 matching the requested scope before generating. One file, labeled sections (`## GOOD`, `## BAD`, `## EDGE CASE`), appended to over time per CE convention. Never split into separate files.

**Format locked 2026-08-14.** The two GOOD anchors below are pulled verbatim from the live doc `1Bv-EWc7HBtKqc09XEfQnBIfSOdm6m4Tc-kJNw5uKErk` and match `SKILL.md -> Editorial Guidelines -> Guideline 4` exactly. Earlier versions of this file carried a "where the live doc and SKILL.md disagree" section; that reconciliation is done and the section is gone.

## Provenance

Fetched via the Docs API with `includeTabsContent`. Content is verbatim. The only normalizations: headings demoted three levels so they nest inside this file, and the Appendix note's leftover prototype label "In v3" written as "In v2" (the prototype numbered its own iterations; there is no third format).

Read the two together. Truck Accidents is the format on a topic with a hard evidence clock and a corporate defendant. Slip and Fall is the format on a topic carrying public skepticism, where the setup paragraph has to defuse the reputation before anything else can land, and where the examples guidance deliberately asks for a case the firm turned down.

## What is generated and what is constant

The STATIC set is **two strings**: `welcome`, `welcome_first`, and `outro_note`. That is all of it. Per-episode generated fields are `topic_phrase`, the setup paragraph, `prompt`, `need_to_know`, `examples`, the Short-Form question sets, and - as of 2026-08-18 - **all three of the outro's spoken lines**, which are generated against the required beats and banks in `references/outro-banks.json` rather than emitted from constants. Eleven further constants were retired 2026-08-17 and are preserved in `references/statics.json` -> `retired`. When you read an anchor, read the two welcome lines and the outro direction note as fixed and treat everything else as a worked example of a generation, not a document to imitate wholesale.

---

## GOOD

### GOOD 1 - Truck Accidents, GA - Savannah

**What each section teaches.**

- **The Introduction is one section, not four.** Welcome, setup paragraph, prompt, stop-talking note. Earlier drafts split these into `Cold Open`, `The Lead-In`, and `The Prompt` with time budgets on each. Collapsing them was deliberate: on the page the budgets invited the interviewer to pace to a clock, and the split implied three separate beats when it is one continuous opening. There is no `[Interviewer]` tag either - the welcome makes the speaker obvious.
- **The welcome is STATIC and the setup paragraph must not re-greet.** "Welcome back to {{PODCAST_NAME}} with {{ATTORNEY_NAME}}. I'm {{HOST_NAME}}, and today we are talking about ..." is frozen; only the phrase completing that sentence is generated. The paragraph immediately after it goes straight at the tension. A second greeting there reads as a stutter, which is why the under-40-words and no-greeting rules both live on that one paragraph.
- **The prompt is credential-led and ends in silence.** It states the attorney's years and territory back to them, asks wide, asks for proof, then names three deliverables. The instruction after it is a direction, not a suggestion: stop talking, do not narrow it, do not offer an example to get them started. Narrowing the prompt in the room is the most common way this format collapses back into an interrogation.
- **The three moves are below the divider because they are not read on air.** Proof, then what they need to know, then real examples. The order is load-bearing: proof first because for a new listener it is their entire introduction to the firm; facts second because that is what someone in trouble is waiting for; stories last because they only land once the listener believes the teller. Everything under `Internal Notes` is production reference for the host and the attorney, not script.
- **Source-consistency counts moved below the divider too.** The attribute bullets carry the name and the plain-language detail only. "4 of 4" and "2 of 4, high signal" are provenance for the producer, and putting them on mic-facing bullets invited the attorney to read them aloud.
- **Short-Form questions render bare.** Ten per location, `**Q1:**` through `**Q10:**`, nothing underneath. No geo tag line, no answer-guidance note. The geo treatment still governs how each question was written and lives in the JSON; it just never prints, because on the page it read as jargon and invited a mechanical city-drop.
- **Exactly three questions change between Location 1 and Location 2.** Q1, Q2, and Q7 carry the city. The other seven are attribute questions that carry over unchanged, which is what makes the two sets produce a comparable clip set.

**The template, verbatim from the live doc.**

#### **Run of Show**

**Why Truck Accident Cases Are Worth More Than Car Cases, and Harder to Win**

Truck Accidents  |  GA - Savannah

Prepared by Case Engine

#### **S1: Long-Form (15-30m)**

##### **Introduction**

Welcome back to **{{PODCAST_NAME}}** with **{{ATTORNEY_NAME}}**. I'm **{{HOST_NAME}}**, and today we are talking about **{{PRACTICE_AREA}}** in **{{CITY}}**, and what happens when a commercial truck hits you.

Getting hit by an eighteen-wheeler is not a bigger version of a car wreck. It is a completely different situation, and the trucking company knows that before you do.

**You have been serving {{CITY}} and the surrounding cities as an attorney for {{YEARS_PRACTICING}} years. What do people actually need to know if they have been hit by a commercial truck out here? And what have you done in the past for clients who were in a serious truck wreck? Give us the facts, what they need to do right this second, and then walk us through an example or two of cases your firm has handled so people understand the journey they are about to go through.**

*Then stop talking. Do not narrow it or offer an example to start them. The silence is the format.*

*[Attorney Response]*

*Then turn it over and let them run.*

##### **Attributes to Hit**

*What people are actually trying to find out before they call anyone. Hit these anywhere in your answer, in your own words, in any order.*

- **Trial willingness.** Have you taken these to trial, or do you only settle? If you are a trial firm, say so early and say it plainly.

- **Specific case-type experience.** Not the practice area, the case type. How many of THIS kind, not how many injury cases. How recently.

- **Fee and expenses in detail.** Percentage, whether it rises if you file suit, who pays records, filing fees, investigators, experts and court reporters, and what happens if you lose.

- **Local court familiarity.** The county court, the judges, how the local defense firms operate. Specifics, not "we serve the area".

- **Evidence preservation speed.** What you secure in the first days and how fast, before it is deleted or overwritten.

- **Expert network.** Name the roles you bring in - reconstructionists, safety engineers, code inspectors, medical specialists, economists.

- **Who actually handles the case.** Am I hiring you, or an intake operation that refers this out? Who do I talk to day to day and how often.

- **Honest assessment.** Name what would make the case difficult. Saying the hard part builds more trust than a promise.

- **Verifiable standing.** Bar license and disciplinary history. This ranks above reviews and awards.

- **Deadlines.** Say the number of years and what happens if it passes.

___________________________________________________________

###### **Internal Notes (not read on air)**

*[Attorney Response - 15 to 30 minutes]*

*Three moves, in this order. A shape, not a script.*

- **Proof, about a minute.** How long you have been doing this here, how many of these cases, your results. For a new listener this is the only introduction they get.

- **What they need to know right now.** The facts and the actions, direct. This is what someone in trouble is listening for.

- **Real examples.** One or two real matters. What the company did in the first week, what the evidence showed, how it ended. Name the road or the corridor if it helps people picture it.

*Two findings worth knowing. Reviews and awards rank BELOW verifiable bar standing. Naming what makes a case difficult reads as a positive signal, while guaranteeing a number is treated as a red flag.*

*Source consistency, from live Google AI Overview and ChatGPT pulls on 08-14 across two practice areas and two markets. Ordering above follows this ranking.*

- **Trial willingness** - 4 of 4, usually the first sentence

- **Specific case-type experience** - 4 of 4

- **Fee and expenses in detail** - 4 of 4

- **Local court familiarity** - 4 of 4

- **Evidence preservation speed** - 4 of 4

- **Expert network** - 4 of 4

- **Who actually handles the case** - 3 of 4

- **Honest assessment** - 2 of 4, high signal

- **Verifiable standing** - 1 of 4, explicitly ranked above reviews

- **Deadlines** - 1 of 4, state-specific

*What to cover in the second move:*

- The trucking company has people working on this within hours. You do not.

- The evidence that proves your case gets erased on a schedule unless somebody stops it

- It is almost never just the driver who is responsible

- Trucking companies follow federal rules that regular drivers do not, and breaking one helps your case

- Why these cases are worth more and also harder, and what that means for who you hire

#### **S2: Short-Form (60-90s)**

*Mode switch, and say it on mic. Each answer is a standalone 60 seconds that restates the question. Higher energy than Segment 1, and no callbacks to the interview. Retakes are expected - if one comes out flat, go again.*

*Ten questions per set, one set per location. Multi-location firms record additional sets back to back and each set gets customized to its city.*

##### **Location 1: Savannah**

- **Q1:** What should you look for before hiring a truck accident lawyer in Savannah?

- **Q2:** What does a truck accident lawyer in Savannah actually do for you?

- **Q3:** What is a truck accident case actually worth around here?

- **Q4:** How much does it cost to hire a truck accident attorney?

- **Q5:** Have you taken truck accident cases to trial, or do you settle them?

- **Q6:** Who will actually handle my case day to day?

- **Q7:** Do you handle truck accident cases across Chatham County and coastal Georgia, or only in Savannah?

- **Q8:** What experts do you bring into a truck accident case?

- **Q9:** How long do you have to file a truck accident claim in Georgia?

- **Q10:** What would make my case difficult?

##### **Location 2: Garden City and the Port corridor**

- **Q1:** What should you look for before hiring a truck accident lawyer in Garden City and the Port corridor?

- **Q2:** What does a truck accident lawyer in Garden City and the Port corridor actually do for you?

- **Q3:** What is a truck accident case actually worth around here?

- **Q4:** How much does it cost to hire a truck accident attorney?

- **Q5:** Have you taken truck accident cases to trial, or do you settle them?

- **Q6:** Who will actually handle my case day to day?

- **Q7:** Do you handle truck accident cases across Chatham County and coastal Georgia, or only in Garden City and the Port corridor?

- **Q8:** What experts do you bring into a truck accident case?

- **Q9:** How long do you have to file a truck accident claim in Georgia?

- **Q10:** What would make my case difficult?

##### **Outro**

*Keep it short. Thank them and mean it, sign off, then the reach-out. Do not recap the episode.*

**{{ATTORNEY}}**, thank you for your time. That is a lot of detail on what makes a truck accident case different that people usually have to piece together on their own.

That is it for this one. **{{PODCAST_NAME}}**. We will see you next episode.

And remember, if you are in **{{STATE}}** and need a lawyer, reach out to **{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**.

#### **Appendix: Source Question Bank**

*The episode's N-Gram Table, verbatim. INTERNAL. In v2 this is reference rather than script: Segment 2 questions were rebuilt around search phrasing and attributes, not lifted from here. Kept as the audit trail and the pull pool.*

- **1.** Why is a Savannah truck accident case treated so differently from a regular car accident case in Georgia?

- **2.** Who can actually be held responsible after a commercial truck wreck in Savannah?

- **3.** What makes truck accident injuries typically more severe than car accident injuries, and where do Savannah victims go for trauma care?

- **4.** How do the insurance policies behind a commercial truck compare to a personal auto policy in Georgia?

- **5.** What federal regulations govern trucking companies that do not apply to ordinary Georgia drivers?

- **6.** How does a trucking company sometimes try to limit its own exposure after a crash in Chatham County?

- **7.** Why does evidence disappear so fast in a Georgia truck accident case, and what is the role of a Savannah-area spoliation letter?

- **8.** What is a black box on a truck and what does it actually tell investigators at a Savannah crash scene?

- **9.** How do driver logbooks and hours-of-service records become evidence in a Georgia truck case?

- **10.** What role does the truck driver's qualification and history play in a Savannah case, and how does Georgia negligent hiring law work?

- **11.** How can a cargo problem or an overloaded trailer cause a serious crash on I-95 or I-16 outside Savannah?

- **12.** What is negligent maintenance and how does it lead to truck accidents in the Savannah area?

- **13.** How does driver fatigue actually factor into a Georgia truck accident claim?

- **14.** What happens when a truck driver was distracted, impaired, or speeding through Savannah city streets or the I-95 corridor?

- **15.** What is the post-accident drug and alcohol testing record, and why does it matter after a Savannah truck crash?

- **16.** How is the value of a Savannah truck accident case calculated under Georgia damages law?

- **17.** What are economic damages in a catastrophic Savannah trucking case, and how is future care valued?

- **18.** How are non-economic damages valued in Georgia when truck accident injuries are life-altering?

- **19.** When can a family pursue punitive damages against a trucking company in Georgia under OCGA § 51-12-5.1, including the DUI exception to the $250K cap?

- **20.** What does the early investigation of a Savannah truck accident actually involve - and what does the Georgia State Patrol bring to the scene?

- **21.** Why do truck accident cases so often involve expert witnesses, and how does Georgia's Daubert standard under OCGA § 24-7-702 affect qualification?

- **22.** What is the difference between settling a Savannah truck case and taking it to trial in Chatham County State Court?

- **23.** How long does a Savannah truck accident case usually take to resolve under Georgia's 2-year SoL?

- **24.** What happens when a Savannah truck accident results in a fatality - who can file the wrongful death claim under OCGA § 51-4-2?

- **25.** What should someone do in the first days after being hit by a commercial truck in Savannah?

- **26.** Why does hiring a lawyer experienced specifically in Georgia trucking cases matter for a Savannah claim?

- **27.** What is the single biggest mistake people make after a truck accident in Savannah or anywhere in Georgia?

- **28.** How are truck accidents involving Port of Savannah drayage or Garden City Terminal traffic different from over-the-road crashes?

- **29.** Why are I-95 and I-16 around Savannah such high-risk corridors for catastrophic truck crashes?

- **30.** How does the choice between Chatham County State Court, Chatham County Superior Court, and federal court in Savannah affect a truck accident case?

---

### GOOD 2 - Slip and Fall, CA - San Diego

**What each section teaches, beyond what GOOD 1 already covers.**

- **The setup paragraph spends itself defusing a reputation.** "Slip and fall has a reputation, and most of that reputation is wrong." Then the thesis in one line: falling is not the case, proving they should have fixed it is the case. On a topic the audience already has an opinion about, the opening has to address the opinion before it can teach anything.
- **The examples guidance asks for a rejection: "Include one you turned down and why."** That builds the honest-assessment attribute into move 3 rather than hoping it surfaces. It is the strongest available trust move on a topic where listeners assume every case is worth chasing, and it matches the finding that naming what makes a case hard outperforms promising an outcome.
- **The jargon-free rewrite is visible line by line.** Rowland, Ortega, CACI 1000-1012, and the six-month public-entity claim window appear nowhere. What the attorney sees is "the video that proves it gets recorded over fast, often within days" and "they will say you should have been watching. In California that reduces your case, it does not end it." Same substance, no citation - and with Producer Notes gone there is no section that would accept one.
- **Urgency is phrased as an action with a reason.** "Photograph the condition that day, because it gets fixed the next day." The legacy version of this point would have cited the notice standard and left the listener with nothing to do.
- **Location 2 is a sub-scope, and it shows the format's sharp edge.** "Public property in San Diego" is not a city, and interpolating it into the city-tagged question slots produces "hiring a slip and fall lawyer in Public property in San Diego". See BAD 3 and EDGE 2 - this is the failure the read-aloud check exists to catch.

**The template, verbatim from the live doc.**

#### **Run of Show**

**Premises Liability, Duty of Care, and Proving Notice**

Slip and Fall  |  CA - San Diego

Prepared by Case Engine

#### **S1: Long-Form (15-30m)**

##### **Introduction**

Welcome back to **{{PODCAST_NAME}}** with **{{ATTORNEY_NAME}}**. I'm **{{HOST_NAME}}**, and today we are talking about **{{PRACTICE_AREA}}** in **{{CITY}}**, and what actually happens when you fall on someone else's property.

Slip and fall has a reputation, and most of that reputation is wrong. Falling on someone's property is not the case. Proving they should have fixed it is the case.

**You have been serving {{CITY}} as an attorney for {{YEARS_PRACTICING}} years. What do people actually need to know if they have fallen and gotten hurt on someone else's property out here? And what have you done in the past for clients who were seriously injured in a fall? Give us the facts, what they need to do right this second, and then give us an example or two of cases your firm has worked on so people understand what the process actually looks like.**

*Then stop talking. Do not narrow it or offer an example to start them. The silence is the format.*

*[Attorney Response]*

*Then turn it over and let them run.*

##### **Attributes to Hit**

*What people are actually trying to find out before they call anyone. Hit these anywhere in your answer, in your own words, in any order.*

- **Trial willingness.** Have you taken these to trial, or do you only settle? If you are a trial firm, say so early and say it plainly.

- **Specific case-type experience.** Not the practice area, the case type. How many of THIS kind, not how many injury cases. How recently.

- **Fee and expenses in detail.** Percentage, whether it rises if you file suit, who pays records, filing fees, investigators, experts and court reporters, and what happens if you lose.

- **Local court familiarity.** The county court, the judges, how the local defense firms operate. Specifics, not "we serve the area".

- **Evidence preservation speed.** What you secure in the first days and how fast, before it is deleted or overwritten.

- **Expert network.** Name the roles you bring in - reconstructionists, safety engineers, code inspectors, medical specialists, economists.

- **Who actually handles the case.** Am I hiring you, or an intake operation that refers this out? Who do I talk to day to day and how often.

- **Honest assessment.** Name what would make the case difficult. Saying the hard part builds more trust than a promise.

- **Verifiable standing.** Bar license and disciplinary history. This ranks above reviews and awards.

- **Deadlines.** Say the number of years and what happens if it passes.

___________________________________________________________

###### **Internal Notes (not read on air)**

*[Attorney Response - 15 to 30 minutes]*

*Three moves, in this order. A shape, not a script.*

- **Proof, about a minute.** How long you have been doing this here, how many of these cases, your results. For a new listener this is the only introduction they get.

- **What they need to know right now.** The facts and the actions, direct. This is what someone in trouble is listening for.

- **Real examples.** One or two real matters. What the store said at first, what the footage or the logs actually showed, how it ended. Include one you turned down and why.

*Two findings worth knowing. Reviews and awards rank BELOW verifiable bar standing. Naming what makes a case difficult reads as a positive signal, while guaranteeing a number is treated as a red flag.*

*Source consistency, from live Google AI Overview and ChatGPT pulls on 08-14 across two practice areas and two markets. Ordering above follows this ranking.*

- **Trial willingness** - 4 of 4, usually the first sentence

- **Specific case-type experience** - 4 of 4

- **Fee and expenses in detail** - 4 of 4

- **Local court familiarity** - 4 of 4

- **Evidence preservation speed** - 4 of 4

- **Expert network** - 4 of 4

- **Who actually handles the case** - 3 of 4

- **Honest assessment** - 2 of 4, high signal

- **Verifiable standing** - 1 of 4, explicitly ranked above reviews

- **Deadlines** - 1 of 4, state-specific

*What to cover in the second move:*

- Falling is not the case. Proving they knew, or should have, is the case.

- Report it before you leave and get a copy of whatever they write down

- The video that proves it gets recorded over fast, often within days

- They will say you should have been watching. In California that reduces your case, it does not end it.

- Photograph the condition that day, because it gets fixed the next day

#### **S2: Short-Form (60-90s)**

*Mode switch, and say it on mic. Each answer is a standalone 60 seconds that restates the question. Higher energy than Segment 1, and no callbacks to the interview. Retakes are expected - if one comes out flat, go again.*

*Ten questions per set, one set per location. Multi-location firms record additional sets back to back and each set gets customized to its city.*

##### **Location 1: San Diego**

- **Q1:** What should you look for before hiring a slip and fall lawyer in San Diego?

- **Q2:** What does a slip and fall lawyer in San Diego actually do for you?

- **Q3:** What is a slip and fall case actually worth around here?

- **Q4:** How much does it cost to hire a slip and fall attorney?

- **Q5:** Have you taken slip and fall cases to trial, or do you settle them?

- **Q6:** Who will actually handle my case day to day?

- **Q7:** Do you handle slip and fall cases across San Diego County and Southern California, or only in San Diego?

- **Q8:** What experts do you bring into a slip and fall case?

- **Q9:** How long do you have to file a slip and fall claim in California?

- **Q10:** What would make my case difficult?

##### **Location 2: Public property in San Diego**

- **Q1:** What should you look for before hiring a slip and fall lawyer in Public property in San Diego?

- **Q2:** What does a slip and fall lawyer in Public property in San Diego actually do for you?

- **Q3:** What is a slip and fall case actually worth around here?

- **Q4:** How much does it cost to hire a slip and fall attorney?

- **Q5:** Have you taken slip and fall cases to trial, or do you settle them?

- **Q6:** Who will actually handle my case day to day?

- **Q7:** Do you handle slip and fall cases across San Diego County and Southern California, or only in Public property in San Diego?

- **Q8:** What experts do you bring into a slip and fall case?

- **Q9:** How long do you have to file a slip and fall claim in California?

- **Q10:** What would make my case difficult?

##### **Outro**

*Keep it short. Thank them and mean it, sign off, then the reach-out. Do not recap the episode.*

**{{ATTORNEY}}**, thanks for being so straight about all of it. A lot of attorneys would not have answered that as straight as you did.

That is where we will leave it. **{{PODCAST_NAME}}**. See you next episode.

And before you go, if you are anywhere in **{{STATE}}** and need help with this, get in touch with **{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**.

#### **Appendix: Source Question Bank**

*The episode's N-Gram Table, verbatim. INTERNAL. In v2 this is reference rather than script: Segment 2 questions were rebuilt around search phrasing and attributes, not lifted from here. Kept as the audit trail and the pull pool.*

- **1.** What is premises liability and how does it apply to a slip and fall?

- **2.** What duty does a property owner owe to keep visitors safe?

- **3.** How do you prove a property owner knew about the hazard?

- **4.** What is the difference between actual and constructive notice?

- **5.** What are the most common slip-and-fall hazards?

- **6.** How does comparative fault affect a slip-and-fall claim?

- **7.** Can I still recover if I wasn't watching where I was walking?

- **8.** What injuries are common in slip-and-fall accidents?

- **9.** How is a slip-and-fall claim investigated?

- **10.** How important is surveillance footage in a slip-and-fall case?

- **11.** What should I do immediately after a slip and fall?

- **12.** Why does reporting the fall to the property owner matter?

- **13.** How does a slip and fall in a store differ from one on a sidewalk?

- **14.** Can a city or government be liable for a fall on public property?

- **15.** What evidence proves a dangerous condition existed?

- **16.** How long does a property owner have to fix or warn about a hazard?

- **17.** How does a slip-and-fall claim handle a wet floor or spill?

- **18.** What role do witnesses play in a slip-and-fall case?

- **19.** How do you prove the fall caused the injury?

- **20.** How is a slip-and-fall claim valued?

- **21.** What is the property owner's most common defense in these cases?

- **22.** How long do I have to file a slip-and-fall claim in California?

- **23.** What mistakes most hurt a slip-and-fall claim?

- **24.** How does a slip-and-fall claim get resolved without trial?

- **25.** If I just had a slip and fall, what should I do this week?

---

## BAD

### BAD 1 - The v1 format this replaces

The legacy four-segment format, still live on `pod-3A-ros-template` for every currently shipping client. It is not bad work. It is a good version of the wrong shape, and naming exactly which of its rules produced the choppiness feedback is the point of this entry, because several of them look sensible in isolation.

**What v1 looks like.** Nineteen or twenty discrete questions, each with its own time budget of two to three minutes, distributed across four segments. Real example from the Houston car accidents template:

```markdown
### Q3: Where should someone in Houston go for medical care after a crash, even if they feel fine? (3 minutes)

*[Co-Host]*

The adrenaline after a freeway collision can mask injuries for hours or even days.

**Where should someone in Houston go for medical care after a crash, even if they feel fine?**

*[Attorney Response]*

- **Hidden injuries:** adrenaline masks injuries - whiplash, concussions, and internal injuries surface days later
- **Level I trauma centers:** <u>Memorial Hermann</u> - Texas Medical Center is one of the top trauma centers in the country, and <u>Ben Taub Hospital</u> is the Harris County public hospital with a Level I trauma center
- **Other options:** <u>Houston Methodist</u> facilities are located throughout the Houston metro area
- **72-hour window:** seek evaluation within 72 hours - gaps in the treatment timeline hurt credibility with adjusters
- **Documentation trail:** medical records directly link injuries to the accident and form the basis of your damages claim
- **Insurer skepticism:** insurance companies in Texas will question any delay in seeking medical care
```

**The specific rules that produced the choppiness, and why each one seemed reasonable.**

- **"No post-response co-host lines between questions."** The v1 rule: attorney bullets end, the next `### Q` starts, and the only co-host text between questions is a segment-transition paragraph at the end of a segment. It was written to stop the script bloating with filler. What it actually does is remove every natural reaction from the recording. A human being says "wait, within days?" when they hear something surprising. Forbidding that turns a conversation into a deposition, and it is the single biggest contributor to the choppy feel.
- **The one-sentence setup cap.** Co-host setup was capped at one sentence, describing the listener's situation only, never explaining how anything works. The intent was to stop the co-host answering their own question. The effect is that every question arrives cold with a single line of context, so twenty times per episode the attorney restarts from nothing instead of building on what came before.
- **`**Label:** detail` attorney bullets that get read aloud.** Six bullets per question, each a bolded label and a clause. On the page it is a tidy contract. In the room the attorney reads the labels, and "Hidden injuries: adrenaline masks injuries" is not a sentence anyone says out loud. This is the mechanism by which the script's structure leaks into the audio.
- **Statute citations in attorney-facing bullets.** v1 deliberately wove entities and statute references into the response bullets as an authority signal. It reads as authority on paper and as a person reciting a reference card on tape. v2 bans it attorney-facing entirely and moves it to Producer Notes.
- **The ~25 to 45 percent city-share quota.** Applied per question set to control city-token density. Because it was an aggregate percentage rather than a per-question instruction, it pushed city tokens into whatever questions had room, producing the phrasing that got flagged directly: "in a the Inland Empire car accident claim". A quota can tell you how many questions may carry the city. It cannot tell you which ones need it, or how to say it. That is what the geo tags replaced it with.

**The through-line.** Each rule optimized a page-level property (no filler, no rambling, high entity density, controlled city share) at the cost of an audio-level property. v2 inverts the priority: the deliverable is what gets said, so the format optimizes for what a person can actually say.

### BAD 2 - The 8-prompt intermediate version, rejected 2026-08-14

My own intermediate draft, built before the call. It replaced v1's twenty questions with eight open prompts, each with "ground worth reaching" bullets and a set of optional follow-ups. Shape:

```markdown
### Prompt 3: The evidence clock
*[Interviewer]*
**Walk me through what happens to the evidence in the first week after a truck wreck.**
*[Attorney Response]*
*Open answer. Let it run. Ground worth reaching:*
- The black box and what it records
- Why the logs matter more than the police report
- What a preservation letter actually does
*[Interviewer - follow-ups, use as needed]*
- What happens if nobody sends one?
- How fast is fast?
```

**Why it was better than v1.** Prompts instead of questions, so answers could run long. Ground bullets instead of read-aloud labels, so the attorney was not reciting. Follow-ups were explicitly allowed, which fixed the no-reaction problem. Skipping a prompt the conversation already covered was defined as correct behavior.

**Why Gabe and Cyle rejected it anyway.** It is still a list. Eight prompts is a smaller interrogation, not a conversation, and the failure modes survive the reduction:

- **The attorney still performs to the list.** Knowing seven more prompts are coming makes every answer a segment rather than a thought, so nothing runs long enough to become a story. Authority never gets established because it is never asked for directly, only implied across eight topics.
- **Eight prompts means eight restarts.** Each one re-scopes the conversation, so the attorney never builds momentum. The thing that makes the single prompt work is that after about four minutes the attorney stops performing and starts talking. Eight prompts never gets there because it resets before it can.
- **The ground bullets became a script anyway.** In practice the interviewer reads them, which recreates the v1 problem in a new costume.
- **It hid the real fix.** The reason v1 felt choppy was not that the questions were too narrow. It was that there were too many of them. Going from twenty to eight treats the symptom. Going to one treats the cause, and moves the structural work into the lead-in where it belongs.

The lesson worth keeping: when a format change halves a count and the same complaint survives, the count was not the variable.

### BAD 3 - A non-city label dropped into the city slot

Observed live, in both GOOD anchors' Set 2, and it is the reason EDGE 2 exists. Wrong:

> **What should you look for before hiring a slip and fall lawyer in Public property in San Diego?**
>
> **What should you look for before hiring a truck accident lawyer in Garden City and the Port corridor?**

The first is not a sentence. The second is grammatical but is not a search anybody performs. Both come from interpolating a Set label into a question template that expects a city name. "Public property in San Diego" is a sub-scope, not a place; "Garden City and the Port corridor" is a corridor description, not the city token a ranking-target question needs.

Right: a CITY-tagged question takes a real city name (`Garden City`), and the corridor or sub-scope becomes the answer instruction or a REGION-tagged treatment. If a set has no real city of its own, it does not get CITY-tagged questions at all, and its top-keyword slots either take the parent city or drop.

Violates: the geo tag gate, and the search-phrase gate. The check that catches it is reading the interpolated question out loud and asking whether a person would type it.

---

## EDGE CASE

### EDGE 1 - The attorney runs dry at minute 8 of a 15 to 30 minute segment

The format's most predictable live failure. The prompt lands, the attorney does move 1 and move 2 well, and somewhere around minute 8 they finish their thought and stop. There is no next question, because the format does not have one. Everyone freezes.

**First, the three-second rule, and it is a real rule rather than a nicety.** Wait three full seconds before saying anything. Most people restart on their own, because the pause is them thinking rather than them finishing. Interviewers systematically underestimate this, since three seconds of silence feels like fifteen when you are in the room and like a natural beat on tape. Stepping in at one second is what actually truncates the answer, and it is the most common way an interviewer damages this format while trying to help.

**Then the reserve bench, in this order.** These are gap-fills, not a question list, and the interviewer holds them without reading them:

- **The attribute checklist is the bench.** By minute 8 the attorney has usually hit three or four attributes. Six or seven are unhit and each one is a natural question. Fill them with the live-checklist phrasings, not the attribute names: financial risk becomes "I think people assume they cannot afford a lawyer, how does that actually work?", accessibility becomes "if I called your office right now, who am I talking to?"
- **"Walk me through one" is the highest-value move and should be spent here.** If move 3 never happened, this is the moment. It reliably produces another five to ten minutes because a case has its own narrative momentum, and it is the single most useful thing an interviewer can say in this format.
- **"Give me a real example of that"** when they went abstract rather than stopping. Abstraction is usually a sign they are summarizing rather than remembering.
- **The Segment 2 bank is the deep reserve.** Ten questions already exist and are already vetted. Pulling two or three forward into Segment 1 as conversation is fine, and re-recording them self-contained in Segment 2 afterward costs nothing because retakes are expected anyway.

**What not to do.** Do not end the segment at 8 minutes because the low end of the band is 15. Do not stack three questions to fill the space, which converts the segment back into an interrogation for its final third. Do not apologize for the silence on mic.

**If it happens twice with the same attorney, it is a prep problem, not a live problem.** The fix is upstream in `pod-3C-client-guide`: they did not know the three moves were coming, so they treated the prompt as a single question and answered it in eight minutes. That guide is already a ship blocker for v2, and this is the specific failure it needs to prevent.

### EDGE 2 - The Ontario problem: a per-city set that cannot be built

A firm anchored on the Inland Empire wants a Segment 2 set for Ontario. The regional entity map resolves the Inland Empire: Riverside County and San Bernardino County courts, the I-10 logistics corridor, regional trauma centers. It does not resolve Ontario specifically, and a set built on regional entities cannot answer Ontario's CITY-tagged questions.

**Why this is not solvable by rephrasing.** The CITY-tagged questions are ranking targets. Their whole function is to carry the city and be answered with things true of that city: the court the case would actually be filed in, the hospitals someone would actually be taken to, the roads people actually name. Answering "what should you look for before hiring a car accident lawyer in Ontario" with Riverside County facts produces a block that is locally wrong, which is worse than not having it, since the audience it targets is exactly the audience that notices.

**The rule.** A per-city set requires per-city entity resolution. A regional entity map cannot supply it, and a set is not always buildable at the scope the client asked for. Check this at the Greeting, when the city list is collected, rather than discovering it mid-generation.

**Resolution order:**

- **Run `pod-1A-entity-research` at city scope for that city.** The correct fix. It produces the courts, hospitals, and roads the CITY-tagged questions need. Cost is a research pass per city, which is the real price of a per-city set and should be quoted as such.
- **If that is not happening, drop the set and fold the city into the regional pairing.** The city still appears, in the CITY + REGION construction ("in Ontario and across the Inland Empire"), which is honest about the depth available. The client gets regional reach without a block that claims local knowledge the research does not support.
- **Never generate the set from the regional map and swap the city name in.** That is the failure this edge case exists to prevent. It produces a set that looks complete, passes the geo tag gate, and is locally wrong in every answer.

**How to spot it before generating.** For each requested city, ask whether the entity map names a court, a hospital, and a road specific to that city. If any of the three is missing, the set is not buildable and the decision goes back to the producer.

**The live doc already shows the shape of this.** Both GOOD anchors' Set 2 uses a sub-scope label rather than a city ("Public property in San Diego", "Garden City and the Port corridor"), and the interpolation breaks as documented in BAD 3. That is the same root cause: a set was requested at a scope the entity resolution does not support.

### EDGE 3 - Client is on the legacy format

`episode_format` resolves to `legacy-segments` or is unset. Stop and route to `/pod-3A-ros-template`. Do not offer to build v2 anyway, and do not treat an unset flag as an invitation. Absence is legacy by definition, and every currently shipping client is in that state.

### EDGE 4 - Episode 1, Founder Story

Founder Story stays on its fixed pre-built template regardless of the format flag. Nothing to generate. Route to `/pod-3B-client-ros` to populate the firm's copy.

### EDGE 5 - A legacy template already exists in the same scope folder

Expected and normal. Note it, leave it alone, confirm the `v2` filenames do not collide, and write alongside it. Never rename, archive, or migrate the legacy artifact from this skill.

### EDGE 6 - No `pod-1D-attribute-research` output for this market

Use `references/attributes/attributes-fallback.json`, record `attribute_source: static-fallback` with the pull date, and flag `> INFERRED:`. A fallback run is never Confirmed. The set is a 2026-08-14 snapshot of live answer-engine output and answer engines move.

### EDGE 7 - Topic Only scope, so there is no city and no region

The geo pairing has nothing to pair. Segment 2 still runs, every question is tagged NEUTRAL or STATE, `{{CITY}}` does not appear, and the Geo Rule block says the template is scope-neutral and the pairing gets added at localization. Do not invent a placeholder region.

### EDGE 8 - The region phrasing has not been confirmed

Propose one and mark it `> NEEDS CONFIRMATION:`. Never assume it. The region is spoken on air, and a wrong one reads as an outsider immediately. "The Bay Area" for a firm that considers itself Peninsula costs more than the delay of asking.
