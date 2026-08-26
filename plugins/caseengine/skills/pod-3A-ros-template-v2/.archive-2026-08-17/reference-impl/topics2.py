"""Single-Prompt format: stronger intro, one prompt, the attorney rips.
The old multi-prompt set is retained per topic as the interviewer's reserve bench."""
from topics import TOPICS as FIVE

# The original Inland Empire episode, brought into the same data shape.
INLAND = {
 "tab": "Inland Empire (CA)",
 "emoji": "\U0001F697",
 "title": "What Your Inland Empire Car Accident Settlement Is Actually Worth",
 "practice_area": "Car Accidents",
 "scope_label": "CA - Inland Empire",
 "runtime": "~48 minutes (Interview ~25 min, Location Blocks ~16 min, Intro/Close ~7 min)",
 "ngram": "podcast/N-Gram Tables/Car Accidents/What Your Inland Empire Car Accident Settlement Is Actually Worth/Locations/CA - Inland Empire/n-gram-table.json",
 "emap": "podcast-research/car-accidents/locations/ca-inland-empire/01-entities/entity-map.json",
 "jurisdiction": "California is an at-fault state under pure comparative negligence, so a claimant recovers even at 99 percent fault, reduced by their share ([Li v. Yellow Cab Co. (1975)]{.underline}). Statute of limitations is 2 years ([California Code of Civil Procedure Section 335.1]{.underline}). The Inland Empire spans [Riverside County]{.underline} and [San Bernardino County]{.underline}, each with its own Superior Court and Sheriff's Department. [I-10]{.underline} runs the logistics corridor, so commercial-vehicle involvement is materially more common here than in a typical metro.",
 "prompts": [
  {"t":"The question everybody asks","q":"Someone calls you a week after a wreck. How fast does what's my case worth come up, and what do you actually tell them?","g":[],"f":[]},
  {"t":"What is happening on the other side","q":"Walk me through what is actually going on inside the insurance company when someone over there puts a number on your client's file.","g":[],"f":[]},
  {"t":"The part you can't put on a receipt","q":"There's the part of a claim you can add up from bills and pay stubs, and then there's everything else. How do you explain that second part?","g":[],"f":[]},
  {"t":"How the medical file decides the case","q":"How much of this is decided by what's in the medical file, versus what actually happened at the scene?","g":[],"f":[]},
  {"t":"The first offer","q":"Tell me about the first offer. What does it usually look like, and what's the client's reaction when it lands?","g":[],"f":[]},
  {"t":"When it was partly your fault","q":"California doesn't cut you off if you were partly to blame. How does that actually play out when you're negotiating?","g":[],"f":[]},
  {"t":"When the case is worth more than anyone will pay","q":"Are there cases where the claim is genuinely worth more than the money that's actually available?","g":[],"f":[]},
  {"t":"Taking the money","q":"What's the case for waiting, and what's the case for just taking the money and being done with it?","g":[],"f":[]},
 ],
 "blocks": [
  {"city":"Riverside","qs":[
   {"q":"What is the average car accident settlement in Riverside?","b":["Lead with the honest range and immediately say what moves it","Injury severity, [Medical Records]{.underline}, liability clarity, available [Policy Limits]{.underline}","Say in Riverside in the first sentence of the answer"]},
   {"q":"Which court handles a Riverside car accident lawsuit?","b":["[Superior Court of California, County of Riverside]{.underline}","Most claims resolve before filing; filing is the leverage step","What changes after filing"]},
   {"q":"How long do you have to file a car accident lawsuit in California?","b":["Two years under [California Code of Civil Procedure Section 335.1]{.underline}","Shorter deadline for a claim against a public entity","The deadline is not negotiable with the insurer"]},
   {"q":"Who investigates a car accident in Riverside County?","b":["[Riverside County Sheriff's Department]{.underline} in unincorporated areas","[California Highway Patrol (CHP)]{.underline} on the freeways","The [Police Report]{.underline} is evidence, not a verdict"]},
   {"q":"How does California's comparative fault rule reduce a Riverside settlement?","b":["[California Pure Comparative Negligence Rule]{.underline} reduces and never bars","Give a concrete percentage and the resulting number","Contest the split with [Dashcam / Surveillance Footage]{.underline} and [Accident Reconstruction]{.underline}"]},
   {"q":"What happens when the at-fault driver in Riverside has no insurance?","b":["Check for [Uninsured / Underinsured Motorist Coverage]{.underline} first","Stack every applicable household policy","Underinsured is the more common problem than uninsured"]},
  ]},
  {"city":"San Bernardino","qs":[
   {"q":"What is the average car accident settlement in San Bernardino?","b":["Same structure as Riverside, answered fresh and standalone","Injury severity, [Medical Records]{.underline}, liability, [Policy Limits]{.underline}","Say in San Bernardino in the first sentence"]},
   {"q":"Which court handles a San Bernardino car accident lawsuit?","b":["[Superior Court of California, County of San Bernardino]{.underline}","Filing as leverage, not the default path","Court-set deadlines after filing"]},
   {"q":"Where should you go for medical care after a crash in San Bernardino?","b":["[Loma Linda University Medical Center (Level I Trauma)]{.underline}","[Arrowhead Regional Medical Center]{.underline}","Go even if you feel fine; the gap gets used against the claim"]},
   {"q":"Who investigates a car accident in San Bernardino County?","b":["[San Bernardino County Sheriff's Department]{.underline}","[California Highway Patrol (CHP)]{.underline} on freeways","Fault findings in the [Police Report]{.underline} are challengeable"]},
   {"q":"How does a crash on the I-10 logistics corridor change a San Bernardino claim?","b":["[I-10 (Logistics Corridor)]{.underline} and warehouse-driven commercial density","Commercial defendants carry higher limits","[Dashcam / Surveillance Footage]{.underline} and telematics get overwritten fast"]},
   {"q":"What happens to a San Bernardino settlement when there are medical liens?","b":["Gross is not net; liens and [Subrogation]{.underline} come out first","Treating facilities and health insurers both have claims","Negotiating them down is real recovered value"]},
  ]},
 ],
 "closing_q": "If somebody listening is sitting on an offer right now and trying to decide what to do, what's the one thing you'd tell them?",
}

TOPICS = [INLAND] + FIVE

# ---- The new Section 1 per topic ----
NEW = {
"Inland Empire (CA)": {
 "cold_open": "Almost everybody who calls a personal injury lawyer wants the same thing in the first sixty seconds, which is a number. And almost nobody gets one. There are real reasons for that, and they are not the reasons people assume.",
 "setup": [
  "My guest today is **{{ATTORNEY_NAME}}** from **{{FIRM_NAME}}**.",
  "Here is the ground we are going to cover. What actually happens between the crash and the check. How an insurance company builds its number and why the first one is almost always wrong. What the medical record does to the value of a case, for better and for worse. What happens when it was partly your fault, which in California does not end anything. And what to do when the case is worth more than the money that exists.",
 ],
 "prompt": "You have been representing crash victims across the **{{CITY}}** area for **{{YEARS_PRACTICING}}** years. Tell us what people actually need to know if they get into a car accident out here.",
 "runway": [
  "The first call and what gets asked before anything else",
  "Why a number this early is a range, and a wide one",
  "The medical picture forming: [Medical Records]{.underline}, treatment continuity, [Maximum Medical Improvement (MMI)]{.underline}",
  "The adjuster's math: multiplier and per-diem, medical specials as the anchor",
  "[Economic Damages]{.underline} versus [Non-Economic Damages]{.underline} and the part with no receipt",
  "The [Demand Letter]{.underline} going out and the first offer coming back low",
  "The fight over fault: [California Pure Comparative Negligence Rule]{.underline} and [Li v. Yellow Cab Co.]{.underline}",
  "The ceiling nobody controls: [Policy Limits]{.underline} and [Uninsured / Underinsured Motorist Coverage]{.underline}",
  "Liens, [Subrogation]{.underline}, and why gross is not net",
  "The [Release of Liability]{.underline} and why there is no going back",
 ]},

"Truck Accidents (GA)": {
 "cold_open": "Two vehicles hit each other at the same intersection, at the same speed. One is a sedan. One is an eighty-thousand-pound truck. On paper it looks like the same wreck. It is not remotely the same case, and the difference starts within hours.",
 "setup": [
  "I am here with **{{ATTORNEY_NAME}}** from **{{FIRM_NAME}}**.",
  "Here is where we are going. Why the company on the other side is already working before you have called anyone. Who is actually on the hook, which is almost never just the driver. The federal rulebook that applies to them and not to you. Why the evidence has a shorter clock than the statute of limitations. And why these cases are worth more and are harder to win, which are two halves of the same fact.",
 ],
 "prompt": "You have been handling trucking cases in **{{CITY}}** for **{{YEARS_PRACTICING}}** years. Tell us what people actually need to know if they get hit by an eighteen-wheeler.",
 "runway": [
  "The call, and what tells you immediately this is a truck case",
  "The carrier's rapid response team already on scene",
  "The [Spoliation / Preservation Letter]{.underline} going out in days, not weeks",
  "[Truck Black Box / ECM]{.underline}, [Electronic Logging Device (ELD) Data]{.underline}, [Telematics / GPS Fleet Data]{.underline}",
  "Building the defendant list: [Motor Carrier Liability]{.underline}, [Negligent Hiring]{.underline}, [Broker Liability]{.underline}, [Shipper / Cargo-Loader Liability]{.underline}",
  "The federal rulebook: [FMCSA Regulations]{.underline}, [Hours of Service]{.underline}, [CDL]{.underline} qualification files",
  "[Accident Reconstructionist]{.underline} and the [Daubert standard]{.underline} under [O.C.G.A. Section 24-7-702]{.underline}",
  "The coverage stack: [MCS-90 Endorsement]{.underline} and [Primary + Umbrella / Excess]{.underline}",
  "Damages: [Life Care Plan]{.underline}, [Economic Loss / Vocational Rehabilitation Expert]{.underline}, punitives under [O.C.G.A. Section 51-12-5.1]{.underline}",
  "[O.C.G.A. Section 51-12-33]{.underline} and the 50 percent bar as the defense's whole strategy",
 ]},

"Birth Injury (MD)": {
 "cold_open": "There is a question every parent in this situation eventually asks, usually late at night, usually months after the diagnosis. Could this have been prevented. It is the hardest question in medicine and law, and it has an honest answer, but getting to it takes work.",
 "setup": [
  "I am joined by **{{ATTORNEY_NAME}}** from **{{FIRM_NAME}}**.",
  "This one is going to move slower than most of our episodes, and that is deliberate. We are going to cover what a cerebral palsy diagnosis tells a family and what it does not. What oxygen loss actually does and how quickly. What the delivery record shows years later. The difference between proving someone made a mistake and proving that mistake caused the harm, which is the whole ballgame. And what a lifetime of care actually costs.",
  "I want to say one thing before we start. Not every one of these is anyone's fault. That is part of the honest answer too.",
 ],
 "prompt": "You have been representing families in **{{CITY}}** for **{{YEARS_PRACTICING}}** years. Tell us what a parent actually needs to know when their child is diagnosed and nobody will tell them why it happened.",
 "runway": [
  "The first conversation and what a parent is actually asking",
  "What a [Cerebral Palsy]{.underline} diagnosis explains and what it leaves open",
  "Birth injury versus [Birth Defects]{.underline}, and the cases that are nobody's fault",
  "Requesting the [Labor and Delivery Medical Records]{.underline}, [Fetal Monitoring Strips]{.underline}, [Placental Pathology Report]{.underline}",
  "Reading the record: [Category III Tracing]{.underline}, [APGAR Score]{.underline}, [Umbilical Cord Blood Gas Analysis]{.underline}",
  "[Therapeutic Hypothermia]{.underline} as the tell that the team suspected [HIE]{.underline} at the time",
  "[Standard of Care]{.underline}, [ACOG Practice Guidelines]{.underline}, and the [Delayed Emergency Cesarean Section]{.underline} question",
  "Breach versus [Causation (Proximate Cause)]{.underline}, and why [Maryland Contributory Negligence]{.underline} raises the stakes",
  "[HCADRO]{.underline} and the [Certificate of Qualified Expert]{.underline} before anyone sees a courtroom",
  "[Life Care Plan]{.underline}, the [Maryland Noneconomic Damages Cap]{.underline}, and the [Special Needs Trust]{.underline}",
 ]},

"Medical Malpractice (FL)": {
 "cold_open": "When a hospital hurts somebody, almost every family walks in wanting to sue the doctor. And very often the doctor is not an employee of the building you were standing in, is not the one who set the conditions, and is not the one with the money.",
 "setup": [
  "My guest is **{{ATTORNEY_NAME}}** from **{{FIRM_NAME}}**.",
  "Here is the territory. Why the ER doctor who treated you probably does not work for the hospital. How the hospital gets pulled back in anyway. The difference between one person's mistake and an institution that was set up to fail. Where the money actually sits, which is a more uncomfortable conversation than people expect. What the chart and the timestamps prove years later. And the gauntlet Florida makes you run before you are even allowed to file.",
 ],
 "prompt": "You have been suing hospitals in **{{CITY}}** for **{{YEARS_PRACTICING}}** years. Tell us what people actually need to know if they think a hospital hurt someone in their family.",
 "runway": [
  "The first call and the assumption the family walks in with",
  "[Independent-Contractor Physician]{.underline} and the [ER Physician Staffing Company]{.underline} nobody knew existed",
  "Pulling the hospital in: [Apparent Agency]{.underline}, [Vicarious Liability]{.underline}, [Respondeat Superior]{.underline}",
  "[Corporate Negligence]{.underline} and [Negligent Credentialing]{.underline} against the institution itself",
  "[ER Understaffing and Triage Failure]{.underline} as a systemic condition, not an event",
  "The record: [Nurse Charting / EMR Timestamps]{.underline}, [Hospital Incident Reports]{.underline}, [Spoliation]{.underline}",
  "Where the money sits: [Underinsured Defendant Physician]{.underline} versus [Hospital Self-Insurance and Captive Layers]{.underline}",
  "The [FS Chapter 766]{.underline} gauntlet: [Notice of Intent]{.underline}, [Corroborating Affidavit]{.underline}, [Same-Specialty Expert]{.underline}",
  "[Medical Causation]{.underline} and the [Loss of Chance Doctrine]{.underline} deciding viability",
  "No cap after [Kalitan]{.underline}, against the [FS 95.11]{.underline} clock and the statute of repose",
 ]},

"Brain Injury (TX)": {
 "cold_open": "A broken leg proves itself. You hold up the X-ray and the argument is over. A brain injury has to be proven over and over, to people who are actively looking for a reason not to believe it. That one fact shapes everything about these cases.",
 "setup": [
  "I am here with **{{ATTORNEY_NAME}}** from **{{FIRM_NAME}}**.",
  "Here is where this goes. Why the injury often does not show up on the scan at the hospital. What it actually does to somebody's life, which the family sees long before any doctor documents it. How you prove something invisible. The insurance company's playbook, which is more organized than people realize. And how you price a life that changed but did not end.",
 ],
 "prompt": "You have been handling brain injury cases in **{{CITY}}** for **{{YEARS_PRACTICING}}** years. Tell us what people actually need to know if they hit their head in a wreck.",
 "runway": [
  "The call, and how often the client is not the one who noticed",
  "The scene: [Glasgow Coma Scale]{.underline} and why a decent early score misleads everyone",
  "[Concussion / Mild TBI]{.underline}, [Diffuse Axonal Injury]{.underline}, [Subdural Hematoma]{.underline} and why they behave differently",
  "What it does to a life: [Post-Concussion Syndrome]{.underline}, [Loss of Consortium]{.underline}, the things that do not photograph",
  "Building the proof: [Neuroimaging (CT, MRI, DTI, fMRI)]{.underline} and [Neuropsychological Testing]{.underline}",
  "The [Fort Worth / Tarrant County Treating Physician]{.underline} record beating a retained opinion",
  "The defense playbook: [Independent Medical Examination]{.underline}, treatment gaps, [pre-existing conditions]{.underline} and the [Eggshell Skull Doctrine]{.underline}",
  "[Texas 51% Modified Comparative Negligence]{.underline} as the lever on a damages case",
  "Pricing it: [Life Care Plan]{.underline}, [Loss of Earning Capacity]{.underline}, [Future Medical Expenses]{.underline}",
  "[Policy Limits]{.underline} against [Texas minimums of 30/60/25]{.underline}, and the long tail toward [CTE]{.underline}",
 ]},

"Slip and Fall (CA)": {
 "cold_open": "Slip and fall has a reputation, and most of that reputation is wrong. Falling on someone's property is not the case. Proving they knew about the hazard, or should have, is the case. Almost everything turns on that one question, and most of these calls never become anything.",
 "setup": [
  "I am joined by **{{ATTORNEY_NAME}}** from **{{FIRM_NAME}}**.",
  "Here is the ground. What people assume when they call, and how often that is wrong. Why notice is the entire case in one word. How you reconstruct two seconds that nobody filmed, and what happens when somebody did. The blame-the-victim defense, which is the whole playbook. Figuring out who actually owns the floor, which is never just the store. And when these are genuinely serious cases, because sometimes they are.",
 ],
 "prompt": "You have been handling premises cases in **{{CITY}}** for **{{YEARS_PRACTICING}}** years. Tell us what people actually need to know if they fall in a store.",
 "runway": [
  "The call, and the fastest way you know it is not a case",
  "[Premises Liability]{.underline} under [Civil Code Section 1714(a)]{.underline} and [Rowland v. Christian]{.underline}",
  "Notice as the whole case: actual versus [Constructive Notice]{.underline}, and [Ortega v. Kmart Corp.]{.underline}",
  "The race for [Surveillance Footage]{.underline} before the retention window closes",
  "[Maintenance / Inspection Logs]{.underline} as the quiet best evidence, and the gap in the sweep schedule",
  "The [Incident Report]{.underline}, [Witness Statements]{.underline}, and the [Spoliation]{.underline} demand",
  "Untangling [Property Owner]{.underline}, [Property Management Company]{.underline}, [Maintenance / Cleaning Contractor]{.underline}",
  "[Title 24]{.underline} violations, [ADA Compliance]{.underline}, and [Negligence Per Se]{.underline}",
  "The defense: [Open and Obvious Doctrine]{.underline}, [Assumption of Risk]{.underline}, [Pure Comparative Negligence]{.underline}",
  "When it is serious: [Fracture]{.underline}, [TBI]{.underline}, [Spinal Cord / Back Injury]{.underline}, and the [CGL Policy]{.underline} behind it",
 ]},
}
