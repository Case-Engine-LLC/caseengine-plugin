---
label: GOOD
skill: ros-template
scope: Location
run_date: 2026-04-10
topic: Car Accidents / How to File a Claim
episode: How to File a Car Accident Claim in Houston, Texas
location: Houston, TX (Harris County)
source: Real production run - deliverables/podcast-research/car-accidents/2. how-to-file-car-accident-claim/locations/tx-houston/06-ros-template/how-to-file-car-accident-claim-tx-houston-v4.0.md
why_this_label: |
  Clean tokenization across all 12 approved placeholders with zero firm-specific leaks.
  Bold preserved around every {{PLACEHOLDER}} so populate-time values stay bold.
  Compact 2-line metadata header followed by jurisdiction-dense Producer Notes.
  Strict question block format: H3 with time budget, 1-sentence co-host setup,
  bold framing question, attorney bullets in **Label:** detail form.
  No post-response co-host lines inside segments; single segment-transition paragraph
  at each segment boundary.
  Entities underlined throughout the body via inline HTML <u>entity</u> tags, clustered
  in attorney response bullets where density should live per Best Practices.
  Full Appendix with all 5 subsections (Formatting Guide, Producer Notes extended,
  Entity Architecture, Entity Checklist grouped local vs national, Search Queries & Volume).
  Location payoff visible: I-45 / I-10 / 610 Loop, Memorial Hermann / Ben Taub /
  Houston Methodist, Harris County District Court + Civil Court at Law, TxDOT / TxDMV /
  TDI / Texas Tort Claims Act, Port of Houston commercial-truck framing in Q18.
  Closing contains {{PHONE_NUMBER}} and {{WEBSITE}} both bold per Quality gate.
known_flaws: |
  - Uses legacy {{CO_HOST_NAME}} in the Introduction (see intro line 21). The current
    canonical placeholder is {{HOST_NAME}}. Populate still works via the documented
    alias rule in the client-ros SKILL, but a re-run should rewrite to {{HOST_NAME}}
    to avoid the deprecation warning in metadata.json.
  - Entity underlines use HTML <u>entity</u> throughout the body. Canonical CE convention
    is pandoc [entity]{.underline}. Every <u>...</u> in this file is a migration artifact;
    client-ros's populate-time converter rewrites them to pandoc, but fresh ros-template
    output should be pandoc-native.
  - Template Version footer reads 4.0; still treated as a minor-drift inventory change,
    not a structural break. Content preserved from v3b per the v4.0 changelog line.
drive_doc: null
---

# GOOD Example: Full Location-scope ROS Template (Houston, TX)

Read the frontmatter above before reading the template body. The inline `<!-- SKILL REF: -->`
and `<!-- DEVIATION -->` comments below call out the calibration-critical moments. This
example is GOOD for placeholder discipline, compact metadata, strict question block format,
verb-first attorney-response scaffolding, and a complete Appendix. It is NON-CANONICAL on
two formatting rules called out in `known_flaws` and in the Deviations section at the
bottom. Everything else is verbatim production output from the 2026-04-10 run.

---

# Run of Show: How to File a Car Accident Claim in Houston, Texas

**Episode:** **{{EPISODE_NUMBER}}** | **Duration:** ~55 minutes | **Recording Date:** **{{RECORDING_DATE}}**
**Attorney:** **{{ATTORNEY_NAME}}** | **{{FIRM_NAME}}** | Houston, Texas | **{{WEBSITE}}**

<!-- SKILL REF: Best Practices -> Placeholder taxonomy + Best Practices -> Document
     structure. The metadata header is the first downstream-readable surface on the
     document - downstream Client ROS populates values in-place without restructuring.
     Five of the twelve approved placeholders appear in the first four lines
     ({{EPISODE_NUMBER}}, {{RECORDING_DATE}}, {{ATTORNEY_NAME}}, {{FIRM_NAME}},
     {{WEBSITE}}), each wrapped in **bold** so populated values stay bold after populate.
     No hard-coded firm / attorney / phone references. Houston and Texas are static
     because they are the Location scope - not firm-specific, they never get populated.
     Teaches: tokenize every firm-specific field; leave the Location static; preserve
     the **bold** around every placeholder. -->

---

## Producer Notes

**Jurisdiction:** Texas is an at-fault (tort) state. Modified comparative negligence bars recovery at 51%+ fault (<u>Texas Civil Practice and Remedies Code</u> Section 33.001). Statute of limitations: 2 years personal injury, 2 years property damage. Minimum auto insurance: $30,000/$60,000/$25,000. CR-2 crash report (Blue Form) filed with <u>TxDOT</u> within 10 days if officer did not file. Government claims require 6-month notice under the <u>Texas Tort Claims Act</u>. Courts: <u>Harris County District Court</u> and <u>Harris County Civil Court at Law</u>.

**Attorney website:** **{{WEBSITE}}**
**About the attorney:** <u>**{{ATTORNEY_NAME}}**</u> is a personal injury attorney at <u>**{{FIRM_NAME}}**</u> in **{{CITY}}**, **{{STATE}}**.

<!-- SKILL REF: Best Practices -> Topic-oriented vs Location-oriented mix + Best Practices
     -> Localization hard rule. The Producer Notes jurisdiction paragraph is where the
     Location scope earns its density: specific statute citations (Section 33.001),
     the exact minimum limits (30/60/25), the state-specific form (CR-2 Blue Form), the
     filing deadline (10 days), the government-notice trigger (6 months under TTCA), and
     the county-level courts (Harris County District + Civil Court at Law). Generic
     stand-ins (Superior Court, Police Department, State Insurance Authority) would fail
     the Localization hard rule. The 5-7 named local entities floor is easily cleared
     here - TxDOT, Texas Tort Claims Act, Harris County District Court, Harris County
     Civil Court at Law, Texas Civil Practice and Remedies Code all surface in the
     jurisdiction block alone.
     Teaches: ground the script in jurisdiction FIRST so every downstream entity
     reference is pre-anchored; include negative-space signals (tort state, modified
     comparative negligence) so similar-looking states (no-fault / pure comparative) can
     not cross-contaminate. -->

<!-- DEVIATION from SKILL Best Practices -> Formatting Guide ("Underlined text = named
     entities. Use pandoc inline [entity]{.underline} as the CE canonical convention
     (not HTML <u>entity</u>)"). The Producer Notes block uses HTML <u>Texas Civil
     Practice and Remedies Code</u>, <u>TxDOT</u>, <u>Texas Tort Claims Act</u>,
     <u>Harris County District Court</u>, <u>Harris County Civil Court at Law</u>.
     Every <u>...</u> in this file is non-canonical - client-ros's populate-time converter
     rewrites to pandoc, so it does not block the pipeline, but fresh ros-template output
     should be pandoc-native. Remediation: replace every <u>X</u> with [X]{.underline} in
     a re-run. -->

---

## Introduction (~2 minutes)

*[Co-Host]*

Welcome back to <u>**{{PODCAST_NAME}}**</u>. I'm **{{CO_HOST_NAME}}**, and today I'm here with <u>**{{ATTORNEY_NAME}}**</u> from <u>**{{FIRM_NAME}}**</u>.

*[Co-Host]*

Good to have you back, <u>**{{ATTORNEY_FIRST_NAME}}**</u>. Thanks for being here today.

*[Co-Host]*

<u>Houston</u> has some of the most dangerous freeways in America, millions of commuters, and an accident rate that reflects all of it. If you have been in a wreck anywhere in <u>Harris County</u>, this episode breaks down every step - from the scene, to <u>Texas's fault-based insurance system</u>, to the courtroom if it gets that far.

*Transition directly into Q1.*

<!-- DEVIATION from SKILL Best Practices -> Placeholder taxonomy (12 approved placeholders;
     host field is {{HOST_NAME}}; {{CO_HOST_NAME}} is deprecated and breaks populate if
     left in). The Introduction uses {{CO_HOST_NAME}}. Client ROS treats it as an alias
     per the Migration note in its Placeholder taxonomy table, but a fresh run of
     ros-template should emit {{HOST_NAME}}. Remediation: rename every {{CO_HOST_NAME}}
     to {{HOST_NAME}} before populate. -->

---

## S1: At the Scene - What to Do Right Now in Houston - Duration: ~10 minutes

### Q1: What should you do immediately after a car accident in Houston to protect your claim? (3 minutes)

*[Co-Host]*

Getting hit on <u>I-45</u> during rush hour with cars flying past at seventy miles an hour is a completely different situation than a parking lot fender bender.

**If someone just got into a wreck somewhere in Houston, what should they do in those first few minutes to protect themselves and their claim?**

*[Attorney Response]*

- **Safety first:** move to a safe location if possible, especially on high-speed roads like <u>I-10</u> or <u>I-45</u>
- **Call 911:** the police report creates official documentation - dispatch routes to the <u>Houston Police Department</u> for city streets or <u>Texas Department of Public Safety</u> troopers for highways
- **Document the scene:** take photos and videos of both vehicles, road conditions, traffic signs, skid marks, and any visible injuries before anything moves
- **Exchange information:** get the other driver's name, license, insurance card, license plate, and vehicle description
- **Collect witnesses:** get names and contact information from anyone who saw the accident before they leave
- **Seek medical care:** go to <u>Memorial Hermann</u>, <u>Ben Taub Hospital</u>, or the nearest ER even if you feel fine
- **Do not admit fault:** even saying "I'm sorry" at the scene can be used against you under <u>Texas's fault-based system</u>

<!-- SKILL REF: Best Practices -> Document structure (strict 4-piece block: H3 with time
     budget -> co-host setup 1 sentence -> bold framing question -> attorney bullets in
     **Label:** detail format) + Best Practices -> Formatting Guide ("Setup text is 1
     sentence MAXIMUM before the bolded question. It describes the listener's situation
     only. It NEVER explains how things work - that's the attorney's job.").
     Q1 is the template - everything after this point copies the shape. The co-host
     setup ("Getting hit on I-45 during rush hour...") is ONE sentence, describes the
     listener's situation, and names a local anchor entity (I-45) without explaining how
     anything works. The question itself is in-sentence localized ("in Houston") not
     suffixed. Every attorney bullet leads with a **Bold label:** followed by verb-first
     action detail (move, call, document, exchange, collect, seek, do not admit). Noun-
     first form ("safety", "911 call", "scene documentation") would fail.
     Teaches: the Q-block is the unit of replication - setup = one sentence, question =
     in-sentence localized, bullets = **Label:** + verb-first detail. -->

### Q2: Are you legally required to report every car accident in Texas? (3 minutes)

*[Co-Host]*

Texas has its own reporting rules that are separate from the police showing up at the scene.

**Are you legally required to report every car accident in Texas, and what are the actual rules?**

*[Attorney Response]*

- **Reporting threshold:** Texas requires reporting accidents involving injury, death, or property damage that makes a vehicle unable to be driven safely
- **CR-2 Blue Form:** if an officer did not investigate the crash, drivers must file a <u>CR-2 crash report</u> with <u>TxDOT</u> within 10 days of the accident
- **Dual reporting:** the police report and the CR-2 form are separate documents - in some cases you need both
- **Penalty for not reporting:** failure to file the required report can result in penalties under the <u>Texas Transportation Code</u>
- **Notify your insurer:** contact your insurance company as soon as possible - most policies require prompt notification
- **Report everything:** even "minor" accidents should be reported - damage estimates are often wrong at the scene


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

---

*[Co-Host]*

So the immediate priorities are safety, 911, documentation, and medical care even if nothing hurts yet. Plus the CR-2 form if no officer filed a report. Next up - how the insurance side actually works in Texas.

<!-- SKILL REF: Best Practices -> Document structure ("No post-response co-host lines
     between questions. Attorney bullets end. Next ### Q starts. The ONLY co-host text
     between questions is a segment-transition paragraph at the end of a segment.") +
     Best Practices -> Segment pacing.
     The segment-wrap paragraph lives AT THE END of S1, after Q3's attorney bullets,
     NOT between Q1/Q2 or Q2/Q3. The transition carries forward the three priorities
     from this segment (safety, 911, documentation, medical care, CR-2) and tees up
     the next segment ("how the insurance side actually works in Texas"). One
     paragraph, placed once per segment boundary.
     Teaches: co-host text between questions inside a segment is a hard fail; segment-
     transition paragraphs live at end-of-segment only. -->

---

## S2: Texas Insurance System and Filing the Claim - Duration: ~16 minutes

### Q4: How does Texas's fault-based insurance system work for car accident claims? (4 minutes)

*[Co-Host]*

In a city with this much traffic, understanding how fault works can make or break a claim.

**How does Texas's fault-based insurance system actually work when it comes to car accident claims?**

*[Attorney Response]*

- **Tort/fault state:** Texas is a fault state - the at-fault driver's insurance pays damages, a framework established under <u>Texas law</u> as enacted by the <u>Texas Legislature</u>
- **Filing process:** the injured party files a claim against the at-fault driver's liability insurance
- **No PIP required:** Texas does not require personal injury protection, unlike no-fault states - though optional PIP is available
- **First-party option:** you can also file through your own insurance and let them subrogate
- **Fault determination:** fault is determined based on the police report, evidence, and adjuster investigation
- **TDI oversight:** the <u>Texas Department of Insurance</u> oversees insurance carriers operating in the state but does not adjudicate fault - that happens through the claims process and, if necessary, litigation


### Q5: What are Texas's minimum auto insurance requirements and why do they matter? (3 minutes)

*[Co-Host]*

A lot of drivers on the road right now are carrying the bare minimum, and it is not much.

**What are Texas's minimum auto insurance requirements, and why do they matter if you are the one filing a claim?**

*[Attorney Response]*

- **30/60/25 minimum:** Texas requires minimum liability coverage of $30,000 per person for bodily injury, $60,000 per accident for bodily injury, and $25,000 for property damage
- **Often insufficient:** these minimums are often not enough for serious accidents - a single surgery can easily exceed $30,000
- **Recovery cap:** if the at-fault driver only carries minimum coverage, your recovery may be capped at their policy limit
- **UM/UIM coverage:** uninsured/underinsured motorist coverage fills the gap - strongly recommended in Houston where the uninsured driver rate is among the highest in Texas
- **Registration link:** the <u>TxDMV</u> requires proof of insurance to register a vehicle - but having a registration does not mean the driver's policy is still active


### Q6: How does Texas's modified comparative negligence rule affect your claim? (3 minutes)

*[Co-Host]*

When multiple vehicles are involved on the <u>610 Loop</u> or a construction zone pile-up, figuring out who is at fault gets complicated fast.

**How does Texas's modified comparative negligence rule affect a car accident claim in Houston?**

*[Attorney Response]*

- **Modified rule:** Texas follows modified comparative negligence - you can recover as long as you are not more than 50% at fault
- **Hard cutoff at 51%:** at 51% or more fault, you are completely barred from recovery under the <u>Texas Civil Practice and Remedies Code</u> - this is the 51% bar rule
- **Reduction formula:** damages are reduced by your percentage of fault - 20% at fault means a 20% reduction in your award
- **Concrete example:** $100,000 in damages with 30% fault results in a $70,000 recovery - but at 51% fault, you recover nothing
- **Insurer tactics:** insurance companies aggressively argue higher fault percentages to push you past that 51% bar and eliminate your claim entirely
- **Jury decides:** if the case goes to trial in <u>Harris County District Court</u>, the jury assigns fault percentages


### Q7: Walk through the step-by-step process of filing a car accident insurance claim in Texas. (3 minutes)

*[Co-Host]*

The accident is over, the paperwork is piling up, and most people have no idea where to start.

**How do you actually file an insurance claim step by step in Texas, and who should you contact first?**

*[Attorney Response]*

- **Notify your insurer first:** Texas policies have prompt notice requirements - contact your own insurer regardless of who was at fault
- **File a third-party claim:** if the other driver was at fault, file a claim against their insurance company as well - get the claim number and reference it on every call
- **What to provide:** police report number, photos, medical records, witness information
- **Recorded statements:** do not give a recorded statement to the other driver's insurer without your attorney present
- **Demand letter:** submit a demand letter once you have reached maximum medical improvement
- **Bad faith recourse:** the <u>Texas Department of Insurance</u> can help if the insurer acts in bad faith, and the <u>Texas Insurance Code</u> provides specific protections against unfair claims settlement practices


### Q8: What should you say and not say to an insurance adjuster after a Houston car accident? (3 minutes)

*[Co-Host]*

That first phone call from the adjuster usually comes within a day or two, and they are recording every word.

**What should a Houston car accident victim expect when the adjuster calls, and what should they absolutely not do?**

*[Attorney Response]*

- **Adjuster loyalty:** adjusters work for the insurance company - their goal is to minimize payouts, not help you
- **No recorded statement:** avoid giving a recorded statement without your attorney present
- **First offer is low:** do not accept the first settlement offer - it is almost always a lowball
- **Medical records release:** do not sign a blanket release - provide only accident-related records
- **Common tactics:** delay, deny, and blame you for a higher fault percentage to push you past the 51% bar and eliminate your claim entirely
- **Bad faith laws:** Texas has robust bad faith insurance laws - the <u>Texas Department of Insurance</u> enforces the <u>Texas Insurance Code</u> provisions against unfair settlement practices

---

*[Co-Host]*

We have covered Texas's fault system, the 30/60/25 minimums, comparative negligence with the 51% bar, and how to handle the insurance company. Now let's talk about the legal deadlines and court process specific to Houston and Harris County.

---

## S3: Texas Deadlines, Courts and Evidence - Duration: ~12 minutes

### Q9: How long do you have to file a car accident lawsuit in Texas and what happens if you miss it? (3 minutes)

*[Co-Host]*

People get caught up in doctor appointments and insurance calls and forget there is a hard deadline running in the background.

**How long does someone in Houston actually have to file a car accident claim under Texas law?**

*[Attorney Response]*

- **Two years for personal injury:** the statute of limitations is two years from the date of the accident under the <u>Texas Civil Practice and Remedies Code</u>
- **Two years for property damage:** property damage claims also carry a two-year deadline
- **Two years for wrongful death:** the same two-year window applies
- **Hard deadline:** miss it and the <u>Texas Judicial Branch</u> will dismiss your case - no exceptions
- **Court procedures:** cases filed in <u>Harris County District Court</u> follow the same two-year rule, but procedural requirements add preparation time
- **Insurance claim does not pause it:** filing an insurance claim does not stop or pause the statute of limitations clock


### Q10: Are there situations in Texas where the deadline gets extended or shortened? (2 minutes)

*[Co-Host]*

There is one exception that cuts the timeline down to six months, and it catches people completely off guard.

**Are there situations in Texas where the filing deadline gets extended or shortened?**

*[Attorney Response]*

- **Minors:** the statute is tolled until the child turns 18, then the two-year clock starts
- **Government entities:** under the <u>Texas Tort Claims Act</u>, you must file a notice of claim within 6 months - that applies to the <u>City of Houston</u>, <u>TxDOT</u>, <u>METRO</u>, and any state or local government entity
- **6 months is fatal:** missing that government notice deadline is almost always fatal to the claim
- **Discovery rule:** in rare cases, the clock starts when the injury is discovered, not when the accident happened - Texas courts interpret this narrowly
- **Mental incapacity:** can toll the statute in some circumstances under the <u>Texas Civil Practice and Remedies Code</u>


### Q11: What evidence beyond photos and medical records can make or break a car accident claim in Houston? (2 minutes)

*[Co-Host]*

Houston has traffic cameras everywhere, and that footage does not stick around forever.

**What evidence matters most for a car accident claim in Houston?**

*[Attorney Response]*

- **Police report foundation:** the police report from the <u>Houston Police Department</u> or <u>Texas Department of Public Safety</u> is the foundation - it carries significant weight with adjusters and juries in <u>Harris County</u>
- **Traffic cameras:** Houston has an extensive camera network at major intersections and along freeways - request footage before it gets overwritten
- **Witness statements:** get them at the scene before people leave - memories change fast
- **Cell phone records:** can disprove or prove distracted driving and are increasingly subpoenaed
- **Medical records:** must show a clear causal connection to the accident
- **Accident reconstruction:** experts are critical for serious or disputed crashes - <u>NHTSA</u> crash pattern data helps frame the liability picture
- **Dashcam footage:** your own dashcam or nearby vehicles can capture facts that no one can argue with


### Q12: What types of damages can someone recover in a Houston car accident claim? (2 minutes)

*[Co-Host]*

Between the medical bills, the lost paychecks, and a car that is totaled, the costs stack up fast.

**What can someone actually recover in a car accident claim in Texas?**

*[Attorney Response]*

- **Economic damages:** medical bills past and future, lost wages, diminished earning capacity, property damage, and out-of-pocket expenses
- **Non-economic damages:** pain and suffering, loss of enjoyment of life, mental anguish, disfigurement - the <u>Texas Judicial Branch</u> does not cap non-economic damages in most personal injury cases
- **No economic cap:** Texas does not cap economic damages - the <u>Texas Legislature</u> has left economic recovery uncapped
- **Punitive damages:** called exemplary damages in Texas - available in cases of gross negligence such as drunk driving or extreme recklessness
- **Wrongful death:** includes funeral costs, loss of income, loss of companionship, and mental anguish under the <u>Texas Civil Practice and Remedies Code</u>
- **Property damage:** straightforward but often undervalued - the insurer's market value offer is frequently lower than actual replacement cost


### Q13: What makes Houston car accidents different from other cities? (3 minutes)

*[Co-Host]*

Houston is the fourth largest city in the country with some of the deadliest highways in America, and that changes everything about these cases.

**What makes Houston car accidents different from other cities, and how do those local factors affect claims?**

*[Attorney Response]*

- **Deadliest highways:** <u>I-45</u> between Houston and Dallas is consistently ranked among the most dangerous highways in the country, and the <u>610 Loop</u> and <u>I-10</u> through Houston see massive daily volumes
- **Urban sprawl:** Houston's spread-out geography means longer commutes, more highway miles, and more exposure to high-speed accidents
- **Flooding:** the <u>National Weather Service Houston</u> tracks severe weather events - Houston's flash flooding during tropical storms and hurricanes creates unique liability situations when drivers are trapped on flooded roadways
- **Construction zones:** <u>TxDOT</u> construction on <u>I-45</u>, <u>I-10</u>, and the <u>610 Loop</u> creates constant shifting lane patterns and work zone hazards
- **Uninsured drivers:** Houston has one of the highest rates of uninsured drivers in Texas, making UM/UIM coverage critical
- **Government liability:** if a road defect or drainage failure caused the accident, <u>TxDOT</u> or the <u>City of Houston</u> may be liable - but remember the 6-month notice requirement under the <u>Texas Tort Claims Act</u>

<!-- SKILL REF: Best Practices -> Topic-oriented vs Location-oriented mix ("Target mix:
     60-70% topic-oriented + 30-40% location-oriented. Woven, not segregated.") + Best
     Practices -> Localization hard rule.
     Q13 is the Location-scope payoff row - the single strongest test of whether this
     template is actually localized or is state-level content wearing a city label.
     Real Houston streets (I-45, I-10, 610 Loop) in n-grams; real local factors (flash
     flooding, uninsured driver rate, Port of Houston truck volume) drive the question
     content; governing bodies (TxDOT, City of Houston, National Weather Service
     Houston) appear as entities; the final predicate ties back to the 6-month TTCA
     notice from Q10, demonstrating the federal -> state -> county -> city cascade the
     SKILL requires.
     Swap test: swap Houston for Dallas. Q13 breaks cleanly (no 610 Loop in Dallas, no
     Port of Houston, different flash-flood geography, different uninsured rate). Q11
     (Harris County jury traditions), Q3 (Memorial Hermann TMC / Ben Taub / Houston
     Methodist), and Q18 (Port of Houston truck flow) also break. Four clean breakpoints
     on a 19-row template = genuine localization density.
     Teaches: at Location scope, the template must carry at least one row that fails
     the city-swap stress test; generic topical rows are allowed but the breakpoints
     are mandatory. -->

---

*[Co-Host]*

We have covered the legal deadlines, the evidence you need, what you can recover, and what makes Houston accidents unique. Now let's talk about finding the right attorney and whether to settle or go to court in Harris County.

---

## S4: Legal Help, Settlement and Harris County Courts - Duration: ~12 minutes

### Q14: When should someone seriously consider hiring a car accident attorney in Houston? (3 minutes)

*[Co-Host]*

With the 51% fault bar in Texas, having someone fighting for your side from the beginning matters more than most people realize.

**When should someone in Houston actually pick up the phone and call a car accident attorney?**

*[Attorney Response]*

- **Before any statement:** call before you give any statement to the other driver's insurance company
- **Ongoing treatment:** definitely call if injuries require more than one doctor visit
- **Disputed fault:** Texas's 51% cutoff under modified comparative negligence makes fault percentages critical - you need an advocate
- **Denied or lowballed:** call if the insurance company denies or lowballs the claim
- **Uninsured/underinsured:** you need an attorney in these situations to navigate your own UM/UIM coverage - especially important in Houston given the high uninsured driver rate
- **Free consultations:** standard in Houston - the <u>State Bar of Texas</u> and the <u>Houston Bar Association</u> both offer referral services


### Q15: How does the contingency fee structure work and what does it actually cost the client? (2 minutes)

*[Co-Host]*

Most people do not realize they can talk to an attorney without paying a dime upfront.

**How does the fee structure work if someone hires a car accident attorney in Houston?**

*[Attorney Response]*

- **No upfront cost:** you pay nothing upfront under a contingency fee arrangement
- **Percentage of settlement:** the attorney typically takes 33% of the settlement
- **Trial increase:** the percentage may increase to 40% if the case goes to trial
- **Advanced costs:** filing fees, expert witnesses, and medical records are typically advanced by the firm
- **Written agreement:** the <u>Texas Disciplinary Rules of Professional Conduct</u> require fee agreements in writing - overseen by the <u>State Bar of Texas</u>
- **No financial risk:** if you do not win, you owe nothing


### Q16: When should someone settle a car accident claim versus filing a lawsuit in Harris County? (3 minutes)

*[Co-Host]*

Harris County is the third most populous county in the country, and the court system here has its own rhythm.

**How does someone decide whether to take the settlement or go to trial in Harris County?**

*[Attorney Response]*

- **Settlement rate:** most car accident cases in Houston settle without trial - roughly 95%
- **Evaluate the offer:** does it cover all medical bills, lost wages, future costs, and pain and suffering?
- **Future treatment:** if the offer does not cover future medical treatment, do not take it
- **Trial timeline:** going to trial in <u>Harris County District Court</u> adds one to three years but may yield a significantly higher award
- **Verdict trends:** jury verdicts in Harris County have historically been favorable for personal injury plaintiffs through the <u>Texas Judicial Branch</u>, though results vary by case
- **Model both outcomes:** your attorney should model settlement value versus likely trial outcome so you decide with full information
- **Court options:** smaller claims may go through <u>Harris County Civil Court at Law</u> while larger cases are filed in <u>Harris County District Court</u>


### Q17: What are the most common mistakes that seriously hurt a car accident claim in Texas? (2 minutes)

*[Co-Host]*

After handling hundreds of these cases, there are patterns you see over and over.

**What are the biggest mistakes you see car accident victims in Houston make that hurt their claim?**

*[Attorney Response]*

- **Social media:** posting about the accident - insurance companies monitor everything
- **Delayed treatment:** even 48 hours creates a gap that adjusters will exploit
- **Admitting fault:** even saying "I'm sorry" at the scene can be used against you
- **Early settlement:** accepting before reaching maximum medical improvement
- **CR-2 form:** not filing the CR-2 Blue Form with <u>TxDOT</u> within 10 days when required
- **Government deadline:** missing the 6-month notice when <u>TxDOT</u> or the <u>City of Houston</u> is involved
- **Preserving evidence:** according to <u>NHTSA</u>, crash scene evidence degrades fast - surveillance footage gets overwritten, skid marks disappear
- **Signing blanket releases:** signing a medical records release without attorney review


### Q18: How do rideshare accidents, truck crashes, and commercial traffic change the claim in Houston? (2 minutes)

*[Co-Host]*

Between the <u>Port of Houston</u> sending trucks down <u>I-10</u> all day and rideshare drivers on every block, Houston has accident types you do not see in smaller cities.

**How do rideshare accidents, truck crashes, and commercial traffic change the claim process in Houston?**

*[Attorney Response]*

- **Rideshare coverage:** depends on the driver's status - app off versus waiting versus active trip
- **Active trip:** a $1 million commercial policy kicks in from <u>Uber</u> or <u>Lyft</u> during an active ride
- **Commercial trucks:** federal regulations from the <u>FMCSA</u> apply, with multiple potentially liable parties including the driver, the employer, and the manufacturer
- **Port traffic:** the <u>Port of Houston</u> generates massive commercial truck volume on <u>I-10</u> and <u>SH 225</u> - these trucks are subject to both <u>Texas Department of Public Safety</u> oversight and federal rules
- **Highway truck crashes:** <u>I-10</u> and <u>I-45</u> truck accidents involve both <u>Texas DPS</u> and federal regulations
- **Evidence preservation:** commercial vehicle evidence must be preserved quickly - trucking companies have been known to destroy records
- **Rapid investigation:** contact an attorney immediately - critical evidence can disappear within days

---

## Closing and Call to Action (~2 minutes)

### Q19: What final advice would you give someone in Houston who was just in a car accident? (2 minutes)

*[Co-Host]*

<u>**{{ATTORNEY_FIRST_NAME}}**</u>, this has been incredibly valuable.

**For someone listening right now who has just been in a car accident in Houston - what is the one thing you want them to remember?**

*[Attorney Response]*

- **Document everything:** from the moment the accident happens, document every detail
- **Seek medical attention:** even if you feel okay, get checked out
- **Do not speak to the other driver's insurance:** without consulting an attorney first
- **Consult a qualified attorney:** reach out to a qualified <u>Houston</u> car accident attorney as soon as possible - the <u>State Bar of Texas</u> and the <u>Houston Bar Association</u> are both resources

*[Co-Host]*

**If someone wants to talk to you about their car accident claim, what is the best way to reach** <u>**{{FIRM_NAME}}**</u>?

*Wait for attorney to provide contact info.*

*[Co-Host]*

**And that first consultation - that is free, right?**

*Wait for confirmation.*

*[Co-Host]*

If you have been in a car accident in <u>Houston</u> and you are not sure what to do next - make that call. You can find <u>**{{FIRM_NAME}}**</u> at **{{WEBSITE}}** or call them directly at **{{PHONE_NUMBER}}**. Thanks for watching, and we will see you on the next episode of <u>**{{PODCAST_NAME}}**</u>.

<!-- SKILL REF: Quality gates -> Content ("Closing segment contains {{PHONE_NUMBER}} and
     {{WEBSITE}} both bold") + Best Practices -> Placeholder taxonomy.
     The Closing line surfaces four placeholders in one paragraph ({{FIRM_NAME}},
     {{WEBSITE}}, {{PHONE_NUMBER}}, {{PODCAST_NAME}}) with every one wrapped in **bold**
     so populated values stay bold through Client ROS populate. {{PHONE_NUMBER}} and
     {{WEBSITE}} specifically are the blocking Quality gate at the Closing - if either
     is missing or unbolded, the template fails the Content gate and cannot ship.
     Teaches: the Closing is the hard-gated placeholder surface - phone + website bolded
     is non-negotiable; {{FIRM_NAME}} and {{PODCAST_NAME}} also surface here with
     underline (entity status) + bold (placeholder status) simultaneously. -->

---

*End of Run of Show*

---

# Appendix: Production Reference

## Formatting Guide

Speaker tags appear as [Co-Host] and [Attorney Response] - italic, no color change.

Bold text is reserved for two uses only: mandatory phrases the attorney should say close to verbatim, and {{PLACEHOLDERS}} that get filled before recording. Do not bold for emphasis elsewhere.

Underlined text marks named entities - specific organizations, agencies, courts, statutes, and government bodies. These are the words that drive topical authority. Hit as many as naturally land.

Attorney response bullets are a complete production checklist - every point the attorney should cover. They are not a script. Attorney uses their own words and can reorder.

Co-host setup text is 1 sentence max before the bolded question. Describes the listener's situation, never explains how things work.

No post-response co-host lines. Attorney bullets end. Next question starts. Segment transitions are the only co-host text between questions.

Q headings are the literal question the co-host asks on mic. Read them close to verbatim.

## Producer Notes

Entity density target: 75%. Natural conversation with specific named entities placed where they fit. The co-host should not sound like they are reading a keyword list.

Naturalness target: 85%. If an entity feels forced, let the attorney cover it in their response instead.

Intro setup: Warm, energetic. Co-host establishes the scope in 2-3 sentences before bringing in the attorney.

Segment transitions: Each segment bridge connects the previous theme to the next. Written out but can be paraphrased.

Closing: Attorney gets a final takeaway moment before the call to action. One strong piece of advice, then the plug.

Recording note: Natural pacing. If an entity feels forced, the attorney can drop it and hit it in a follow-up beat instead.

Houston localization note: Fully localized for Houston/Harris County. Texas-specific terminology throughout: "modified comparative negligence," "CR-2 Blue Form," "51% bar rule," "Texas Tort Claims Act." All entities verified for Texas jurisdiction. Houston-specific context: I-45, I-10, 610 Loop, Port of Houston, petrochemical truck traffic, flooding/weather, uninsured driver rate, Memorial Hermann/Ben Taub trauma centers.

## Entity Architecture

**19 questions** | **26 primary entities** | Target mentions: ~190 | Density: 75% | Naturalness: 85% | 4 segments | ~55 min

| Entity | Questions | Target Mentions | Entity Strength |
|---|---|---|---|
| Houston Police Department | Q1, Q11 | 4 | High |
| Texas Department of Public Safety | Q1, Q2, Q11, Q18 | 5 | High |
| Texas Department of Insurance (TDI) | Q4, Q7, Q8 | 4 | High |
| TxDMV | Q2, Q5, Q17 | 3 | Medium |
| Texas Legislature | Q4, Q6, Q12 | 3 | Medium |
| Texas Civil Practice and Remedies Code | Q6, Q9, Q10, Q12 | 4 | Medium |
| Texas Insurance Code | Q7, Q8 | 2 | Medium |
| Texas Transportation Code | Q2 | 2 | Medium |
| Harris County District Court | Q6, Q9, Q16 | 4 | High |
| Harris County Civil Court at Law | Q16 | 2 | Medium |
| Texas Judicial Branch | Q9, Q12, Q16 | 3 | Medium |
| State Bar of Texas | Q14, Q15, Q19 | 3 | Medium |
| Houston Bar Association | Q14, Q19 | 2 | Low |
| Memorial Hermann | Q1, Q3 | 3 | High |
| Houston Methodist | Q3 | 2 | Medium |
| Ben Taub Hospital | Q1, Q3 | 3 | High |
| TxDOT | Q10, Q13, Q17 | 4 | High |
| Texas Tort Claims Act | Q10, Q13 | 3 | High |
| NHTSA | Q11, Q17 | 3 | Medium |
| FMCSA | Q18 | 2 | Medium |
| City of Houston | Q10, Q13, Q17 | 3 | Medium |
| National Weather Service Houston | Q13 | 2 | Low |
| Uber / Lyft | Q18 | 3 | Medium |
| Texas Disciplinary Rules of Professional Conduct | Q15 | 2 | Low |
| METRO (Houston) | Q10 | 2 | Medium |
| Port of Houston | Q18 | 2 | Low |

## Entity Checklist

Use this checklist to verify entity coverage after recording. Every entity below should appear at least once during the episode.

### Texas-Specific Entities

- Houston Police Department - Q1, Q11
- Texas Department of Public Safety - Q1, Q2, Q11, Q18
- Texas Department of Insurance (TDI) - Q4, Q7, Q8
- TxDMV - Q2, Q5, Q17
- Texas Legislature - Q4, Q6, Q12
- Texas Civil Practice and Remedies Code - Q6, Q9, Q10, Q12
- Texas Insurance Code - Q7, Q8
- Texas Transportation Code - Q2
- Harris County District Court - Q6, Q9, Q16
- Harris County Civil Court at Law - Q16
- Texas Judicial Branch - Q9, Q12, Q16
- State Bar of Texas - Q14, Q15, Q19
- Houston Bar Association - Q14, Q19
- TxDOT - Q10, Q13, Q17
- Texas Tort Claims Act - Q10, Q13
- Texas Disciplinary Rules of Professional Conduct - Q15
- METRO (Houston) - Q10
- City of Houston - Q10, Q13, Q17
- National Weather Service Houston - Q13

### Houston-Specific Entities

- Memorial Hermann - Q1, Q3
- Houston Methodist - Q3
- Ben Taub Hospital - Q1, Q3
- Port of Houston - Q18
- Uber / Lyft - Q18

### National Entities

- NHTSA - Q11, Q17
- FMCSA - Q18

<!-- SKILL REF: Best Practices -> Appendix construction ("The Appendix after End of
     Run of Show contains five subsections, in this order: Formatting Guide, Producer
     Notes extended, Entity Architecture, Entity Checklist grouped local vs national,
     Search Queries & Volume").
     All five Appendix subsections land in the required order. Entity Checklist is
     correctly grouped three-way: Texas-Specific (state-level), Houston-Specific (city-
     level), National (federal) - the canonical cascade. Entity Architecture uses the
     4-column table (Entity | Questions | Target Mentions | Entity Strength) which
     downstream Client ROS reads to build its recording-time tally sheet.
     Teaches: the Appendix is not optional and its five-subsection order is fixed;
     entity checklists group by jurisdictional scope (state / city / national), not
     alphabetically. -->

## Search Queries & Volume

| Query | Intent | Notes |
|---|---|---|
| how to file a car accident claim in houston | Informational | Primary target |
| houston car accident lawyer | Commercial | High local volume |
| what to do after a car accident in houston | Informational | Q1 target |
| texas car accident insurance claim | Informational | Q4-Q8 target |
| houston car accident attorney free consultation | Commercial | Q14-Q15 target |
| harris county car accident lawsuit | Informational | Q16 target |
| texas statute of limitations car accident | Informational | Q9-Q10 target |
| texas comparative negligence 51 percent | Informational | Q6 target |
| houston truck accident lawyer | Commercial | Q18 target |
| car accident claim houston tx | Commercial | Primary target variant |
| houston car accident settlement | Informational | Q16 target |
| what to do after a wreck in houston | Informational | Q1 target variant |

---

End of Document

**Version:** 4.0 | **Updated:** 2026-04-10 | **Location:** Houston, TX (Harris County) | **Skill:** producer-ros-template-creator
**Source n-gram:** 03-n-gram-table/n-gram-table.md (18 questions, localized to 19 with Houston-specific additions)
**Changes in v4.0:** Restructured to match _template_city gold standard format: compact 2-line metadata, brief Producer Notes above script, Appendix H1 wrapping all reference material (Formatting Guide, Producer Notes extended, Entity Architecture, Entity Checklist grouped local/national, Search Queries & Volume). Segment headings include "Duration:" label. Content preserved from v3b. Added Search Queries & Volume section. Added Closing section header.

---

## Calibration Summary

Future runs of this skill should replicate these seven rules. If an output misses any
of them, it drops below GOOD threshold:

1. **Tokenize every firm-specific field with the 12 approved placeholders.** Firm, attorney, phone, website, episode number, recording date, podcast name, host name, city, state, practice area - all placeholders. Static Location (Houston, Texas) is OK because it is scope, not firm-specific.
2. **Preserve `**bold**` around every placeholder.** Populate-time values must stay bold downstream. Stripping bold at generation time breaks the Client ROS populate contract.
3. **Compact 2-line metadata header** (Episode + Duration + Recording Date on line 1, Attorney + Firm + Location + Website on line 2), followed by Producer Notes with jurisdiction-dense prose carrying specific statute sections, minimum insurance limits, state-specific forms, filing deadlines, and named county courts.
4. **Strict question block format.** H3 with time budget, 1-sentence co-host setup (describes listener's situation, never explains how things work), bold framing question, attorney bullets in `**Label:** detail` format with verb-first predicates.
5. **No post-response co-host text between questions inside a segment.** One segment-transition paragraph lives at the end of each segment, between Q-of-last and S-of-next.
6. **At least one Location-payoff question (like Q13 here) that fails the city-swap stress test.** Real streets, real local factors, named municipal bodies. If every row still works after swapping Houston for Dallas, the template is state-scope dressed up as location-scope.
7. **Complete Appendix in the correct 5-subsection order**: Formatting Guide, Producer Notes extended, Entity Architecture, Entity Checklist (grouped state / city / national), Search Queries & Volume. Closing carries {{PHONE_NUMBER}} and {{WEBSITE}} both bold.

---

## Deviations from current canonical

This example is GOOD for the seven Calibration Summary rules above. It is NON-CANONICAL
on two rules from SKILL Best Practices -> Formatting Guide and -> Placeholder taxonomy.
Future runs should fix these before writing to Drive.

| # | SKILL rule (section + specific) | What this example does | Scope of deviation |
|---|---|---|---|
| 1 | Best Practices -> Formatting Guide: "Underlined text = named entities. Use pandoc inline `[entity]{.underline}` as the CE canonical convention (not HTML `<u>entity</u>`)" | Uses HTML `<u>entity</u>` throughout the body, Producer Notes, and Introduction | Every entity underline in the file (estimated 60+ instances) |
| 2 | Best Practices -> Placeholder taxonomy: host field is `{{HOST_NAME}}`; `{{CO_HOST_NAME}}` is deprecated and breaks populate if left in | Introduction uses `{{CO_HOST_NAME}}` | 1 instance (line 21 of source) |

**Reader takeaway:** use this example to calibrate placeholder discipline, compact metadata,
Producer Notes jurisdiction density, strict question block format, attorney-bullet verb-first
predicates, the Location payoff question, and Appendix completeness. Do NOT copy the HTML
`<u>...</u>` entity underlines or the `{{CO_HOST_NAME}}` placeholder. Both were left in
place because this run predates the pandoc + HOST_NAME canonicalization pass. A conforming
re-run would rewrite every `<u>X</u>` to `[X]{.underline}` and rename `{{CO_HOST_NAME}}`
to `{{HOST_NAME}}` while keeping every question, setup, bullet, segment transition, and
Appendix row intact.

### The single-question stress test

Pick any row in the template. Ask: "If I swapped Houston for Dallas, would this question
still make sense or would it break?"

- If every question still works after the swap, the template is state-scope dressed up as
  location-scope and fails the Localization hard rule.
- If at least 3-5 questions break after the swap, the template is genuinely localized.

Q13 is the cleanest break point here (swap Houston for Dallas and the 610 Loop, Port of
Houston, flash-flooding context, and uninsured-driver rate all fail). Q18 (Port of Houston
commercial truck volume) breaks. Q3 (Memorial Hermann TMC / Ben Taub / Houston Methodist
trauma centers) breaks. Q16 (Harris County District Court + Civil Court at Law jury
verdict trends) breaks. Q11 (Houston PD + Harris County jury weight) breaks. Five clean
breakpoints on a 19-question template is healthy localization density for City-level
Location scope.
