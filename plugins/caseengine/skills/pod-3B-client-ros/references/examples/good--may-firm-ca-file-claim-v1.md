---
label: GOOD
skill: client-ros
scope: Location
run_date: 2026-04-10
firm: The May Firm
topic: Car Accidents / How to File a Claim
episode: How to File a Car Accident Claim in California
location: CA (state-level)
source: Real production run - deliverables/podcast-research/car-accidents/2. how-to-file-car-accident-claim/locations/ca/client/the may firm/how-to-file-car-accident-claim-ca-v1.md
why_this_label: |
  Clean populate with all 12 approved placeholders filled with real client data.
  Zero remaining {{...}} tokens in the body. Bold preserved around every populated
  value (Robert May, The May Firm, Kara, Car Accident Attorney w. Robert May,
  (805) 440-9666, https://mayfirm.com/) so the downstream Client Guide and on-air
  host see the bolding for mandatory-verbatim text.
  Entities underlined throughout attorney-response bullets where density lives per
  the Formatting preservation rule. Populated attorney name, firm name, and podcast
  name all carry both bold (mandatory-verbatim) and underline (entity) simultaneously.
  Strict 4-piece question block format preserved from the upstream ROS Template:
  H3 with time budget, 1-sentence co-host setup, bold framing question, attorney
  bullets in **Label:** detail form. No post-response co-host lines inside segments.
  Single segment-transition paragraph at each segment boundary.
  Full metadata block with all 5 canonical lines (Practice Area implicit via topic,
  Episode + Duration, Recording Date, Template Version, Location). California
  jurisdiction grounding in Producer Notes preserved verbatim from template.
  Introduction has exactly three *[Co-Host]* paragraphs, no *[Attorney Response]*
  block in the intro, and a *Transition directly into Q1.* line.
  Closing contains populated phone ((805) 440-9666) and website (https://mayfirm.com/)
  both bold per Quality gate.
known_flaws: |
  - Entity underlines use HTML <u>entity</u> throughout the body. Canonical CE
    convention is pandoc [entity]{.underline}. Every <u>...</u> in this file is a
    migration artifact carried through from the upstream ROS Template - the populate
    step should have converted them at populate time per the Formatting preservation
    rule ("Legacy <u>entity</u> tags from older templates must be converted to
    [entity]{.underline} at populate time"). This run pre-dates the converter.
  - Template Version listed as 2.0 in the metadata footer; canonical is newer.
    Minor version drift, not a structural break.
  - No inline Entity Checklist table at the bottom of the file. The current
    canonical client-ros format requires an Entity Checklist table AFTER
    *End of Run of Show* with 4 columns (Entity | Questions | Target Mentions |
    Actual Mentions) as the recording-time tally sheet. This example has the Entity
    Checklist inside the Appendix (grouped California-Specific / National) instead
    of as a separate table post-ROS. Remediation on a re-run: add the 4-column
    table below *End of Run of Show* and keep the Appendix groupings as a reference.
  - Appendix is present in this populated Client ROS. Current canonical client-ros
    format says "No inline Appendix in the populated Client ROS. Appendix content
    lives in the ROS Template (internal reference); Client ROS ends at
    *End of Run of Show*." Remediation on a re-run: strip the Appendix (Formatting
    Guide, Producer Notes extended, Entity Architecture, Entity Checklist groupings,
    Search Queries) from the populated Client ROS and keep it only in the upstream
    ros-template.
drive_doc: null
---

# GOOD Example: Populated Client ROS (The May Firm, California state-level)

Read the frontmatter above before reading the populated script. The inline
`<!-- SKILL REF: -->` and `<!-- DEVIATION -->` comments below call out the calibration-
critical moments. This example is GOOD for placeholder population completeness, bold
preservation, entity underline retention, strict question block preservation, and
introduction-structure discipline. It is NON-CANONICAL on three rules called out in
`known_flaws` and in the Deviations section at the bottom. Everything else is verbatim
production output from the 2026-04-10 run.

---

# Run of Show: How to File a Car Accident Claim in California

**Episode:** **2** | **Duration:** ~55 minutes | **Recording Date:** **April 14, 2026**
**Attorney:** **Robert May** | **The May Firm** | Santa Maria, California | **https://mayfirm.com/**

<!-- SKILL REF: Best Practices -> Placeholder taxonomy + Quality gates -> Content
     ("All 12 placeholders populated with real values (not empty strings)" + "No
     remaining {{PLACEHOLDERS}} in either file (scan explicitly)").
     The metadata header populated 5 of the 12 placeholders in the first four lines:
     {{EPISODE_NUMBER}} -> 2, {{RECORDING_DATE}} -> April 14, 2026, {{ATTORNEY_NAME}}
     -> Robert May, {{FIRM_NAME}} -> The May Firm, {{WEBSITE}} -> https://mayfirm.com/.
     Every populated value stays **bold** after populate - strip the bold and Client
     Guide's downstream translation breaks. "Santa Maria, California" fills the
     {{CITY}} and {{STATE}} placeholders in readable form. No bare {{...}} tokens
     anywhere in the body - the scan-for-remaining-placeholders gate passes.
     Teaches: populate replaces the token INSIDE the bold markers; bold stays, token
     goes, real value lands bold. -->

---

## Producer Notes

**Jurisdiction:** California is a fault-based (tort) state. Pure comparative negligence allows recovery regardless of fault percentage, with damages reduced proportionally. Statute of limitations: 2 years personal injury (CCP Section 335.1), 3 years property damage (CCP Section 338). Minimum auto insurance: 15/30/5 (BI per person/per accident/property damage). SR-1 form required within 10 days for accidents involving injury, death, or $1,000+ property damage, filed with California DMV. Government entity claims: 6-month filing under California Tort Claims Act (Gov. Code Section 810-996.6). No PIP requirement. Courts: Superior Court of California (each county).

**Attorney website:** **https://mayfirm.com/**
**About the attorney:** <u>**Robert May**</u> is a personal injury attorney at <u>**The May Firm**</u> in **Santa Maria**, **California**.

<!-- SKILL REF: Best Practices -> Formatting preservation ("Populated {{ATTORNEY_NAME}},
     {{FIRM_NAME}}, and {{PODCAST_NAME}} are entities too - underline every time they
     appear as [Graham E. Sutliff]{.underline}, [Sutliff & Stout]{.underline},
     [Sutliff & Stout Podcast]{.underline}").
     The About-the-attorney line applies the DOUBLE treatment correctly: <u>**Robert
     May**</u> and <u>**The May Firm**</u> carry BOTH underline (entity status) AND
     bold (populated placeholder status) simultaneously. A correct populate preserves
     both markers - bold because the placeholder was bold; underline because the
     populated name is a named entity. Dropping either treatment fails Quality gates
     -> Formatting.
     Teaches: when a placeholder populates to a named entity (attorney, firm, podcast),
     the output stacks BOTH markers. Never strip one during populate. -->

<!-- DEVIATION from SKILL Best Practices -> Formatting preservation ("Underlined
     entities use pandoc `[entity]{.underline}` as the CE canonical convention (not
     HTML `<u>entity</u>`)" + "Legacy `<u>entity</u>` tags from older templates must
     be converted to `[entity]{.underline}` at populate time. Any HTML `<u>` tag in
     the source is a migration artifact"). This run inherits HTML <u>...</u> tags
     from the upstream ROS Template and ships them through without conversion.
     Reason: this 2026-04-10 run pre-dates the populate-time converter. Remediation:
     rewrite every <u>X</u> to [X]{.underline} at populate time going forward; block
     on the "zero <u> instances" Formatting gate. -->

---

## Introduction (~2 minutes)

*[Co-Host]*

Welcome back to <u>**Car Accident Attorney w. Robert May**</u>. I'm **Kara**, and today I'm here with <u>**Robert May**</u> from <u>**The May Firm**</u>.

*[Co-Host]*

Good to see you, <u>**Robert**</u>. Thanks for being here today.

*[Co-Host]*

Today we are talking about how to file a car accident claim in <u>California</u>. We are going to cover everything from what to do at the scene, to how <u>California's fault-based insurance system</u> works, filing deadlines, dealing with <u>insurance companies</u>, and when you actually need a lawyer. If you have been in a crash anywhere in <u>California</u>, this episode is for you.

*Transition directly into Q1.*

*Co-Host Notes: California's combination of heavy freeway traffic, pure comparative negligence, and low minimum coverage limits creates a unique claims landscape that most drivers don't understand until after the crash.*

<!-- SKILL REF: Best Practices -> Document structure preservation ("Introduction with
     three separate *[Co-Host]* paragraphs (welcome-back -> greet attorney -> topic
     frame) and a *Transition directly into Q1.* line. No *[Attorney Response]* block
     in the intro.") + Quality gates -> Formatting ("Intro has exactly three
     *[Co-Host]* paragraphs and a *Transition directly into Q1.* line, zero
     *[Attorney Response]* blocks").
     The Introduction lands the three-paragraph structure cleanly: para 1 welcomes
     back + introduces podcast and attorney; para 2 greets the attorney by first name;
     para 3 frames the topic in 2-4 sentences with local anchor entities (California,
     California's fault-based insurance system). The *Transition directly into Q1.*
     line closes the intro. Zero *[Attorney Response]* blocks in the intro - attorney
     does not speak in the introduction structure; the attorney's first speaking
     moment is Q1.
     Teaches: intro has exactly three *[Co-Host]* paragraphs + transition line.
     Adding attorney response bullets inside the intro is a hard fail. -->

---

## S1: At the Scene - What to Do Right Now (~10 minutes)

### Q1: What should someone do immediately after a car accident to protect their claim? (3 minutes)

*[Co-Host]*

Most people panic after a crash and have no idea what to do first.

**What should someone do immediately after a car accident in California to protect their claim?**

*[Attorney Response]*

- **Safety first:** move to a safe location if possible, especially on high-speed freeways where secondary collisions are a real risk
- **Call 911:** contact <u>911</u> immediately - the local <u>Police Department</u> handles city streets while the <u>California Highway Patrol</u> covers freeways and unincorporated areas
- **Request a police report:** even for minor collisions, always request a police report - this creates official documentation that the <u>insurance company</u> and courts rely on
- **Document the scene:** take photos and videos of both vehicles, road conditions, traffic signs, skid marks, and any visible injuries before anything moves
- **Exchange information:** get the other driver's name, license, insurance card, license plate, and vehicle description
- **Collect witnesses:** get names and contact information from anyone who saw the accident before they leave
- **Do not admit fault:** even saying "I'm sorry" at the scene can be used against you - under <u>California's pure comparative negligence</u> system, every percentage point of fault matters

<!-- SKILL REF: Best Practices -> Document structure preservation ("Strict question
     block format (every Q1-QN): `### Q{N}: {question}? ({time} min)` H3 with time
     budget -> single *[Co-Host]* + one sentence of setup -> bold framing question
     verbatim -> *[Attorney Response]* + bullets in `**Label:** detail` format.").
     Q1 is the template - every question in the file copies this shape. Setup is
     ONE sentence describing the listener's situation ("Most people panic after a
     crash..."); question is in-sentence localized ("in California") not suffixed;
     attorney bullets use **Label:** + verb-first detail (move, call, request,
     document, exchange, collect, do not admit). Time budget (3 minutes) appears in
     the H3 heading.
     Teaches: the populated Q block is exactly the shape of the tokenized template
     Q block - populate does not restructure; populate fills placeholders inside
     the existing shape. -->

### Q2: Should I call the police even if the accident seems minor? (3 minutes)

*[Co-Host]*

A lot of people skip the police call when the damage looks small.

**Should I call the police even if the accident seems minor, and what is the SR-1 form?**

*[Attorney Response]*

- **Always call:** even minor accidents can involve hidden injuries or more vehicle damage than is visible at the scene
- **Official record:** the police report creates an official record that the <u>insurance company</u> uses when evaluating your claim
- **SR-1 requirement:** <u>California</u> law requires drivers to file the <u>SR-1 form</u> with the <u>California Department of Motor Vehicles</u> within 10 days of an accident involving injury, death, or $1,000 or more in property damage
- **Separate from police report:** the <u>SR-1</u> filed with the <u>California DMV</u> is a completely separate document from the police report filed by the responding officer
- **License consequences:** failure to file the <u>SR-1</u> within the required timeframe can result in license suspension
- **How to file:** the form is available online through the <u>California Department of Motor Vehicles</u> website or at any DMV office


### Q3: Do I need medical care even if I feel fine after the crash? (3 minutes)

*[Co-Host]*

A lot of people walk away feeling fine and skip the doctor entirely.

**Do I need medical care even if I feel fine after a car accident in California?**

*[Attorney Response]*

- **Hidden injuries:** adrenaline masks injuries - whiplash, concussions, and internal injuries often surface days later
- **Emergency room first:** go to the nearest emergency room for serious accidents
- **72-hour window:** seek medical evaluation within 72 hours - gaps in the treatment timeline give the <u>insurance company</u> ammunition to argue your injuries are not related to the accident
- **Documentation trail:** <u>medical records</u> directly link injuries to the accident and form the basis of your damages claim
- **Follow-up care:** establish with a provider who regularly documents accident-related injuries and make sure every appointment connects back to the accident
- **Insurer skepticism:** the <u>insurance company</u> will question any delay in seeking medical care

---

*[Co-Host]*

We have covered what to do at the scene - call 911, document everything, get medical care even if you feel fine, and file that SR-1 form with the DMV. Now let's get into how California's insurance system works and how to actually file a claim.

<!-- SKILL REF: Best Practices -> Document structure preservation ("No post-response
     co-host lines between questions within a segment. Attorney bullets end; next
     ### Q starts. The only co-host text between questions is a single segment-
     transition paragraph at the end of each segment.") + Quality gates -> Formatting
     ("Zero post-response co-host lines between questions within a segment (segment-
     wrap co-host paragraph allowed only at end of segment)").
     S1 closes with ONE co-host paragraph AFTER Q3's attorney bullets, before the
     S2 header. The transition recaps S1's four takeaways (911, documentation, medical
     care, SR-1) and tees up S2 ("California's insurance system"). Zero co-host text
     between Q1/Q2 or Q2/Q3 inside S1.
     Teaches: segment-transition paragraphs live only at end-of-segment; any co-host
     text between questions inside a segment is a hard fail. -->

---

## S2: California's Insurance System and Filing the Claim (~12 minutes)

### Q4: How do I file a car accident insurance claim step by step, and who should I contact first? (3 minutes)

*[Co-Host]*

Someone has been in an accident, they have documented everything, they have been to the doctor - now what?

**Walk me through the step-by-step process of filing a car accident insurance claim in California, and which insurance company should I contact first?**

*[Attorney Response]*

- **Notify your own insurer first:** contact your own <u>insurance company</u> promptly - most policies require prompt notification regardless of who was at fault
- **File a third-party claim:** if the other driver was at fault, file a claim against their <u>insurance company</u> as well
- **Fault-based system:** <u>California</u> is a fault-based state, meaning the at-fault driver's insurance company pays damages through their liability policy
- **No PIP requirement:** unlike no-fault states, <u>California</u> does not require personal injury protection coverage
- **What to provide:** police report number, photos, medical records, witness statements, and the <u>SR-1</u> filing confirmation
- **Demand letter:** submit a demand letter once you have reached maximum medical improvement
- **If fault is unclear:** start with your own <u>insurance company</u> while the investigation determines liability
- **Regulated by:** the <u>California Department of Insurance</u> oversees all insurance practices in the state and can help if the insurance company acts in bad faith


### Q5: What documents do I need to start a car accident claim? (3 minutes)

*[Co-Host]*

Most people are not sure what paperwork they actually need to get this started.

**What documents do I need to start a car accident claim in California?**

*[Attorney Response]*

- **Police report:** the official accident report filed by the responding officer
- **SR-1 confirmation:** proof that you filed the <u>SR-1 form</u> with the <u>California Department of Motor Vehicles</u>
- **Insurance information:** your policy details and the other driver's insurance card
- **Medical records:** all treatment records, bills, and provider notes tied to the accident
- **Photos and video:** scene documentation, vehicle damage, visible injuries, road conditions
- **Witness statements:** written or recorded statements from anyone who saw the accident
- **Lost wage documentation:** pay stubs, employer letters, or tax returns showing income impact
- **Repair estimates:** written estimates or invoices for vehicle damage
- **Out-of-pocket expenses:** receipts for transportation, prescriptions, medical equipment, and anything else connected to the accident


### Q6: What should you say and not say to an insurance adjuster, and should you give a recorded statement? (3 minutes)

*[Co-Host]*

Most people assume the adjuster is on their side.

**What should you say and not say to an insurance adjuster, and should you ever give them a recorded statement?**

*[Attorney Response]*

- **Adjuster loyalty:** the insurance adjuster works for the <u>insurance company</u> - their goal is to minimize payouts
- **Provide basic facts only:** give the date, time, location, and parties involved - nothing more
- **No recorded statement:** do not give a recorded statement to the other driver's <u>insurance company</u> without consulting an attorney first
- **Why it matters:** anything you say in a recorded statement can be taken out of context and used to reduce or deny your claim
- **First offer is low:** do not accept the first settlement offer
- **Medical records release:** do not sign a blanket release - provide only accident-related medical records
- **Refer to your attorney:** once you have legal representation, refer the adjuster directly to your attorney


### Q7: What common mistakes can hurt a car accident claim? (3 minutes)

*[Co-Host]*

You see people make the same mistakes over and over.

**What are the most common mistakes that seriously hurt a car accident claim in California?**

*[Attorney Response]*

- **Social media:** posting about the accident, your injuries, or your activities - the <u>insurance company</u> monitors everything
- **Delayed treatment:** even 48 hours creates a gap that adjusters exploit to question whether injuries are accident-related
- **Admitting fault:** even "I'm sorry" at the scene can increase your fault percentage under <u>California's pure comparative negligence</u> system
- **Early settlement:** accepting before reaching maximum medical improvement - you do not know your full damages yet
- **Missing the SR-1:** failure to file with the <u>California Department of Motor Vehicles</u> within 10 days
- **Signing blanket releases:** signing a medical records release without attorney review gives the <u>insurance company</u> access to your entire medical history
- **Missing the government deadline:** if a government vehicle or road condition caused the accident, missing the 6-month notice under the <u>California Tort Claims Act</u>
- **Bad faith recourse:** the <u>California Department of Insurance</u> can investigate bad faith practices if the insurer is acting unfairly

---

*[Co-Host]*

We have covered the filing process, what documents you need, how to handle the adjuster, and the mistakes that hurt people the most. Now let's talk about how fault works in California and the evidence that drives your settlement.

---

## S3: Fault, Evidence, and Settlement Value (~15 minutes)

### Q8: How is fault determined in a car accident claim? (3 minutes)

*[Co-Host]*

Most people don't know how fault actually gets assigned in the first place.

**How is fault determined in a car accident claim in California, and how much weight does the police report carry?**

*[Attorney Response]*

- **Police report foundation:** the police report from the local <u>Police Department</u> or <u>California Highway Patrol</u> carries significant weight
- **Not binding:** the police report is influential but not legally binding - fault can be disputed in <u>Superior Court of California</u>
- **Evidence review:** adjusters and courts review physical evidence, photos, witness accounts, and traffic camera footage
- **Jury decides at trial:** a jury assigns fault percentages based on all evidence presented
- **California's pure comparative negligence:** under <u>California Civil Code</u>, fault is divided by percentage - there is no bar at any threshold


### Q9: What evidence is most important for a car accident claim? (3 minutes)

*[Co-Host]*

Beyond the basics, there is a lot of evidence that can tip the scale.

**What evidence beyond photos and medical records can make or break a car accident claim in California?**

*[Attorney Response]*

- **Traffic camera footage:** many <u>California</u> intersections have cameras - request footage from <u>Caltrans</u> or the local municipality before it gets overwritten
- **Witness statements:** collect them at the scene before people leave
- **Cell phone records:** can disprove or prove distracted driving
- **Full police report:** request the complete accident report with diagrams from the local <u>Police Department</u> or <u>California Highway Patrol</u>
- **Dashcam footage:** your own dashcam or nearby vehicles
- **Accident reconstruction:** experts can be critical for serious or disputed crashes
- **NHTSA data:** the <u>National Highway Traffic Safety Administration</u> maintains crash data that may be relevant
- **Commercial vehicle records:** if a truck was involved, request driver logbooks and electronic logging device records - commercial trucks are regulated by the <u>Federal Motor Carrier Safety Administration</u>


### Q10: How do medical records affect a car accident settlement? (3 minutes)

*[Co-Host]*

You mentioned the documentation trail earlier - let's dig into that.

**How do medical records and documentation affect a car accident settlement in California?**

*[Attorney Response]*

- **Causation link:** <u>medical records</u> must show a clear causal connection between the accident and your injuries
- **Continuous treatment:** maintain treatment without gaps - any break gives the <u>insurance company</u> grounds to argue the injuries resolved
- **Written prognosis:** obtain a written prognosis from your treating physician documenting future treatment needs
- **Medical liens:** <u>California</u> allows medical liens on settlements - <u>hospitals</u> and medical providers can place a lien ensuring they get paid from your settlement proceeds before you receive the balance
- **Lien negotiation:** your attorney can often negotiate liens down, but you need to know they exist before accepting any settlement
- **Future damages:** <u>California</u> does not cap economic damages - document every dollar of past and future medical costs


### Q11: Can I still file a claim if I was partially at fault? (3 minutes)

*[Co-Host]*

A lot of people assume that if they were partly at fault, they can't do anything.

**Can you still file a claim if you were partially at fault for the accident in California?**

*[Attorney Response]*

- **Pure comparative negligence:** <u>California</u> follows pure comparative negligence under <u>California Civil Code</u> and <u>California Code of Civil Procedure</u> - you can recover damages no matter what percentage of fault is assigned to you
- **No cutoff:** unlike states with a 50 or 51 percent bar, <u>California</u> has no threshold that blocks recovery entirely
- **Proportional reduction:** your compensation is reduced by your percentage of fault - $100,000 in damages with 30 percent fault means you recover $70,000
- **Even at high fault:** at 80 percent fault, you still recover 20 percent of your damages
- **Insurer pressure:** the <u>insurance company</u> will still push hard to assign you a higher fault percentage to reduce their payout
- **Jury decides:** if the case goes to trial in <u>Superior Court of California</u>, the jury assigns fault percentages
- **Preserve evidence:** focus on preserving every piece of evidence that minimizes your share of fault


### Q12: When should I contact a car accident attorney? (3 minutes)

*[Co-Host]*

A lot of people are not sure if their case is big enough to justify calling a lawyer.

**When should someone seriously consider hiring a car accident attorney in California?**

*[Attorney Response]*

- **Before any statement:** call an attorney before giving any statement to the other driver's <u>insurance company</u>
- **Ongoing treatment:** definitely call if injuries require more than one doctor visit
- **Disputed fault:** if comparative negligence is in play and the <u>insurance company</u> is assigning you fault
- **Denied or lowballed:** call if the <u>insurance company</u> denies or lowballs the claim
- **Commercial vehicle:** consult immediately if a commercial truck, delivery vehicle, or government entity was involved
- **Free consultations:** standard practice among personal injury attorneys in <u>California</u> - the <u>State Bar of California</u> has a certified lawyer referral service
- **Contingency fee:** most personal injury attorneys work on a contingency fee basis - no upfront cost, the attorney takes a percentage of the settlement
- **Verify credentials:** confirm the attorney is in good standing with the <u>State Bar of California</u>

---

*[Co-Host]*

We have covered how fault works under California's pure comparative negligence system, the evidence you need, how medical records drive settlement value, and when to bring in a lawyer. Now let's get into the deadlines and what happens if this goes to court.

---

## S4: Deadlines, Uninsured Drivers, and the Legal Process (~14 minutes)

### Q13: How long does a car accident claim usually take, and when should you settle instead of filing a lawsuit? (3 minutes)

*[Co-Host]*

The insurance company makes an offer, and now there is a real decision to make.

**How long does a car accident claim usually take, and when should you settle instead of filing a lawsuit?**

*[Attorney Response]*

- **Settlement tradeoff:** settlement gives you certainty and speed - a verdict in <u>Superior Court of California</u> gives you the possibility of more money but also the risk of less
- **Timeline for settlement:** expect straightforward claims to settle in six to twelve months
- **Timeline for litigation:** if a lawsuit is filed, prepare for one to three years in the court system
- **Evidence strength:** if fault is clear and the offer is far below fair value, trial becomes more viable
- **Future treatment:** if the offer does not cover future medical treatment, do not take it
- **The <u>California Department of Insurance</u>** regulates settlement practices - if the insurer is lowballing or delaying in bad faith, file a complaint
- **Mediation:** <u>California</u> courts encourage mediation before trial - many cases resolve at this stage
- **Lawyer referral:** the <u>State Bar of California</u> can connect you with attorneys experienced in trial work


### Q14: What happens if I miss the deadline to file a claim? (3 minutes)

*[Co-Host]*

This is one of those deadlines that can end your case permanently.

**How long do you have to file a car accident lawsuit in California, and what happens if you miss it?**

*[Attorney Response]*

- **Two years for personal injury:** under <u>California Code of Civil Procedure Section 335.1</u>, the statute of limitations for personal injury claims is two years from the date of the accident
- **Three years for property damage:** property damage claims have a three-year window under <u>California Code of Civil Procedure Section 338</u>
- **Hard deadline:** miss the two-year window and <u>Superior Court of California</u> will dismiss your case - no exceptions
- **Insurance claim does not pause it:** filing a claim with your <u>insurance company</u> does not stop or pause the statute of limitations clock
- **Government entities:** if the at-fault driver was operating a government vehicle, you must file a claim within 6 months under the <u>California Tort Claims Act</u> (Government Code Section 810-996.6) - this is nearly always fatal if missed
- **Minors:** the statute is tolled until the child turns 18, then the standard two-year clock starts
- **Discovery rule:** in rare cases, the clock starts when the injury is discovered, not when the accident happened
- **Start early:** start talking to an attorney well before the deadline


### Q15: How do claims work with uninsured or hit-and-run drivers? (3 minutes)

*[Co-Host]*

This is a situation nobody expects to be in.

**What happens if the other driver does not have insurance or flees the scene in California?**

*[Attorney Response]*

- **File UM claim:** your primary recourse is your own uninsured motorist coverage
- **California requires UM offer:** <u>California</u> law requires insurers to offer uninsured and underinsured motorist coverage - drivers can decline it in writing, but it is included by default
- **Report hit-and-runs immediately:** report to the local <u>Police Department</u> or <u>California Highway Patrol</u> immediately - the police report is required to trigger UM coverage
- **File the SR-1:** the <u>SR-1 form</u> must still be filed with the <u>California DMV</u> within 10 days
- **Identify the driver:** provide any identifying information about the fleeing vehicle
- **Low minimum coverage:** <u>California's</u> minimum coverage is only 15/30/5 - a single surgery can easily exceed the $15,000 per-person limit, making underinsured motorist coverage critical
- **Limited recovery from uninsured:** if the uninsured driver is identified, you can pursue them personally, but they often have limited assets

---

## Closing and Call to Action (~2 minutes)

*[Co-Host]*

<u>**Robert**</u>, this has been incredibly valuable.

**For someone listening right now who has just been in a car accident in California - what is the one thing you want them to remember?**

*[Attorney Response]*

- **Document everything:** from the moment the accident happens, document every detail
- **Seek medical attention:** even if you feel okay, get checked out within 72 hours
- **Do not speak to the other driver's insurance:** without consulting an attorney first
- **Consult a qualified attorney:** reach out to a qualified <u>California</u> car accident attorney as soon as possible

*[Co-Host]*

**If someone wants to talk to you about their car accident claim, what is the best way to reach** <u>**The May Firm**</u>?

*Wait for attorney to provide contact info.*

*[Co-Host]*

**And that first consultation - that is free, right?**

*Wait for confirmation.*

*[Co-Host]*

If you have been in a car accident in <u>California</u> and you are not sure what to do next - make that call. You can find <u>**The May Firm**</u> at **https://mayfirm.com/** or call them directly at **(805) 440-9666**. Thanks for watching, and we will see you on the next episode of <u>**Car Accident Attorney w. Robert May**</u>.

<!-- SKILL REF: Quality gates -> Formatting ("Closing contains populated
     {{PHONE_NUMBER}} and {{WEBSITE}} both bold") + Best Practices -> Placeholder
     taxonomy.
     The Closing line surfaces four populated placeholders in one paragraph: firm
     name (**The May Firm** + underline), website (**https://mayfirm.com/**), phone
     number (**(805) 440-9666**), and podcast name (**Car Accident Attorney w.
     Robert May** + underline). Both {{PHONE_NUMBER}} and {{WEBSITE}} populated and
     bold - the hard-gated closing placeholder surface passes. Three of the four
     are wrapped in underlines as well because they are named entities (firm,
     podcast), while phone + website stay bold-only (they are populated values, not
     entities).
     Teaches: the Closing is the non-negotiable placeholder surface - phone + website
     both bold; firm + podcast carry the double treatment (bold populated + underline
     entity); {{ATTORNEY_FIRST_NAME}} (Robert) earlier in the closing also carries
     both treatments because attorney first name is a named-entity populate. -->

---

*End of Run of Show*

<!-- DEVIATION from SKILL Best Practices -> Entity Checklist table (required - bottom
     of Client ROS) ("Every populated Client ROS includes an Entity Checklist table
     at the very bottom, AFTER *End of Run of Show*. This table is the recording-
     time tally sheet the host/producer uses to verify each named entity gets the
     target number of mentions. It's the canonical CE format... 4 columns, one row
     per entity drawn from the matching-scope entity map: Entity | Questions |
     Target Mentions | Actual Mentions"). This example has NO inline 4-column Entity
     Checklist table after End of Run of Show. Instead, the Entity Checklist
     information appears inside the Appendix as a grouped list (California-Specific
     / National). That grouped list is useful reference but does not carry the
     Actual Mentions column the producer fills in during recording review.
     Reason: this run pre-dates the Entity Checklist-as-recording-tally-table rule.
     Remediation on a re-run: build the 4-column table from the Appendix entity list,
     compute Target Mentions ranges per the heuristic (1-2 questions -> 2-3; 3-4
     questions -> 3-5; 5-6 questions -> 5-7; 7+ -> 7-10+), leave Actual Mentions
     blank for producer fill-in, and place the table AFTER End of Run of Show. -->

<!-- DEVIATION from SKILL Best Practices -> Document structure preservation ("No
     inline Appendix in the populated Client ROS. Appendix content lives in the ROS
     Template (internal reference); Client ROS ends at *End of Run of Show*.").
     This example ships a full Appendix (Formatting Guide, Producer Notes extended,
     Entity Architecture, Entity Checklist groupings, Search Queries) inside the
     populated Client ROS. Current canonical says the populated Client ROS stops at
     End of Run of Show; Appendix is internal-reference-only on the upstream ROS
     Template. Remediation on a re-run: strip the Appendix from the populated Client
     ROS and keep Appendix content only in the upstream ROS Template (which now lives at `{Firm} Podcast/Episodes/E{N} - {Episode} - {Location}/01 Strategy/ROS Template - ....md`, not a .TEMPLATES tree)
     source. Populated Client ROS in 01 Strategy/ ends at End of Run of Show plus
     the Entity Checklist table. -->

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

## Producer Notes (extended)

Entity density target: 70% topical, 30% local. Natural conversation with specific named entities placed where they fit. The co-host should not sound like they are reading a keyword list.

Intro setup: Warm, energetic. Co-host establishes the scope in 2-3 sentences before bringing in the attorney.

Segment transitions: Each segment bridge connects the previous theme to the next. Written out but can be paraphrased.

Closing: Attorney gets a final takeaway moment before the call to action. One strong piece of advice, then the plug.

Recording note: Natural pacing. If an entity feels forced, the attorney can drop it and hit it in a follow-up beat instead.

California localization note: Fully localized for California state level. California-specific terminology throughout: "pure comparative negligence," "SR-1 form," "California Tort Claims Act," "15/30/5 minimums." All entities verified for California jurisdiction. This is the PARENT template for Long Beach, Fresno, and Bakersfield extension episodes.

## Entity Architecture

- **18 entities** across 15 questions | Target mentions: ~90 | Density: 70% | Naturalness: 85% | 4 segments | ~55 min

| Entity | Questions | Target Mentions | Entity Strength |
|--------|-----------|-----------------|-----------------|
| Insurance Company | Q4, Q5, Q6, Q7, Q8, Q10, Q11, Q12, Q13, Q14, Q15 | 14 | High |
| California Department of Motor Vehicles | Q2, Q5, Q7, Q15 | 6 | High |
| California Highway Patrol | Q1, Q9, Q15 | 5 | High |
| California Department of Insurance | Q4, Q7, Q13 | 5 | High |
| Superior Court of California | Q8, Q11, Q13, Q14 | 5 | High |
| SR-1 Form | Q2, Q5, Q7, Q15 | 5 | High |
| California Code of Civil Procedure | Q11, Q14 | 4 | Medium |
| Police Department | Q1, Q2, Q9, Q15 | 4 | Medium |
| State Bar of California | Q12, Q13 | 3 | Medium |
| California Civil Code | Q8, Q11 | 3 | Medium |
| California Tort Claims Act | Q7, Q14 | 3 | High |
| Caltrans | Q9 | 2 | Medium |
| Emergency Medical Services | Q1 | 2 | Medium |
| Hospital | Q3, Q10 | 3 | Medium |
| FMCSA | Q9 | 2 | Medium |
| NHTSA | Q9 | 2 | Medium |
| Law Firm | Q12 | 2 | Medium |
| Civil Court | Q14 | 2 | Medium |

## Entity Checklist

Use this checklist to verify entity coverage after recording. Every entity below should appear at least once during the episode.

### California-Specific Entities

- California Department of Motor Vehicles - Q2, Q5, Q7, Q15
- California Highway Patrol - Q1, Q9, Q15
- California Department of Insurance - Q4, Q7, Q13
- Superior Court of California - Q8, Q11, Q13, Q14
- California Code of Civil Procedure - Q11, Q14
- California Civil Code - Q8, Q11
- California Tort Claims Act - Q7, Q14
- State Bar of California - Q12, Q13
- Caltrans - Q9
- SR-1 Form - Q2, Q5, Q7, Q15

### National Entities

- Insurance Company (generic) - Q1, Q3, Q4, Q6, Q7, Q10, Q11, Q12, Q13, Q14
- Police Department (generic) - Q1, Q2, Q9, Q15
- Emergency Medical Services - Q1
- Hospital - Q10
- National Highway Traffic Safety Administration - Q9
- Federal Motor Carrier Safety Administration - Q9

## Search Queries & Volume

Localized search queries this episode targets. Volume is directional, not exact.

| Query | Intent | Target Q |
|-------|--------|----------|
| how to file a car accident claim in california | Informational | Q4 |
| california car accident claim process | Informational | Q4 |
| what to do after a car accident california | Informational | Q1 |
| california car accident police report | Informational | Q2 |
| sr-1 form california | Informational | Q2 |
| california car accident statute of limitations | Informational | Q14 |
| california comparative negligence car accident | Informational | Q11 |
| car accident attorney california | Commercial | Q12 |
| car accident settlement california | Commercial | Q13 |
| what to say to insurance adjuster after car accident | Informational | Q6 |
| california minimum auto insurance requirements | Informational | Q15 |
| uninsured motorist claim california | Informational | Q15 |
| car accident medical records california | Informational | Q10 |
| california car accident fault determination | Informational | Q8 |
| mistakes after car accident california | Informational | Q7 |
| hit and run accident california | Informational | Q15 |
| car accident claim documents needed | Informational | Q5 |
| california government vehicle accident claim | Informational | Q14 |
| car accident evidence preservation | Informational | Q9 |
| california car accident lawyer free consultation | Commercial | Q12 |

---

End of Document

**Version:** 2.0 | **Updated:** 2026-04-10 | **Location:** California (state-level) | **Skill:** producer-ros-template-creator
**Source n-gram:** 03-n-gram-table/n-gram-table.md (18 questions, 3 merged in dedup)
**Changes in v2.0:** Full regeneration with updated formatting. Matched _template_city.md gold standard: compact metadata, Appendix H1 wrapping all reference material (Entity Architecture moved to Appendix per workflow doc). 3 question merges (Q4+Q5, Q7+Q8, Q13+Q15 from original n-gram). 15 final questions across 4 segments.

---

## Calibration Summary

Future runs of this skill should replicate these seven rules. If an output misses any
of them, it drops below GOOD threshold:

1. **All 12 placeholders populate with real client values; zero raw `{{...}}` tokens remain.** Scan the entire body explicitly before saving. Any leftover token is a hard fail.
2. **Bold stays around every populated value.** `**{{FIRM_NAME}}**` becomes `**The May Firm**`, not `The May Firm`. Strip the bold and the downstream Client Guide translation breaks.
3. **Populated attorney name, firm name, and podcast name carry BOTH bold AND underline.** They are populated placeholders (bold) AND named entities (underline) simultaneously. Strip either marker and the formatting gate fails.
4. **Introduction has exactly three `*[Co-Host]*` paragraphs and a `*Transition directly into Q1.*` line.** Zero `*[Attorney Response]*` blocks in the intro. Attorney's first speaking moment is Q1.
5. **Strict question block format preserved from upstream ROS Template.** H3 with time budget, 1-sentence setup, bold framing question, attorney bullets in `**Label:** detail` form. Populate does not restructure; populate fills placeholders inside the existing shape.
6. **Zero post-response co-host text between questions inside a segment.** Segment-transition paragraphs live only at end-of-segment boundaries.
7. **Closing carries populated `{{PHONE_NUMBER}}` and `{{WEBSITE}}` both bold.** Firm name and podcast name in the closing carry bold-and-underline. This is the hard-gated client-facing CTA surface.

---

## Deviations from current canonical

This example is GOOD for the seven Calibration Summary rules above. It is NON-CANONICAL
on three rules from current client-ros SKILL Best Practices. Future runs should fix
these before writing to Drive.

| # | SKILL rule (section + specific) | What this example does | Scope of deviation |
|---|---|---|---|
| 1 | Best Practices -> Formatting preservation: "Underlined entities use pandoc `[entity]{.underline}` as the CE canonical convention (not HTML `<u>entity</u>`)". Legacy `<u>...</u>` tags must be converted at populate time. | Uses HTML `<u>entity</u>` throughout the body | Every entity underline in the file (estimated 70+ instances) |
| 2 | Best Practices -> Entity Checklist table (required - bottom of Client ROS): 4-column table (Entity / Questions / Target Mentions / Actual Mentions) placed AFTER *End of Run of Show* as the recording-time tally sheet | No 4-column Entity Checklist table; entity information lives inside the Appendix as a grouped list with no Actual Mentions column | Entire Entity Checklist structure |
| 3 | Best Practices -> Document structure preservation: "No inline Appendix in the populated Client ROS. Appendix content lives in the ROS Template (internal reference); Client ROS ends at *End of Run of Show*." | Ships a full Appendix (Formatting Guide, Producer Notes extended, Entity Architecture, Entity Checklist groupings, Search Queries) inside the populated Client ROS | Entire Appendix section |

**Reader takeaway:** use this example to calibrate placeholder population completeness,
bold preservation around populated values, the bold+underline double treatment on
populated named entities, introduction structure discipline, strict question block
preservation from upstream template, zero post-response co-host text inside segments,
and the hard-gated closing placeholder surface. Do NOT copy the HTML `<u>...</u>`
entity underlines, the Appendix-inside-populated-ROS structure, or the missing
4-column Entity Checklist table. A conforming re-run would rewrite every `<u>X</u>`
to `[X]{.underline}`, strip the Appendix (keep it only on the upstream ros-template),
and add a 4-column Entity Checklist table below *End of Run of Show*.

### The single-question stress test

Pick any row in the populated script. Ask: "If I swapped The May Firm for Sutliff &
Stout and California for Texas, would this row still work or would it break?"

- If every row still works after the swap, the populated Client ROS is generic content
  wearing a client label and failed the populate-time jurisdictional inheritance check.
- If at least 3-5 rows break after the swap, the populate is genuinely client-and-
  jurisdiction-bound.

Breakpoints on this populate: every row that references California-specific statutes
(Q14 CCP 335.1 / 338, Q11 California Civil Code, Q7 California Tort Claims Act),
California-specific forms (Q2/Q5/Q7/Q15 SR-1), California-specific agencies (Q1/Q9/Q15
California Highway Patrol, Q9 Caltrans, Q4/Q7/Q13 California Department of Insurance,
Q8/Q11/Q13/Q14 Superior Court of California), and California-specific legal framework
(Q7/Q11 pure comparative negligence at 80% still recovers, vs Texas modified at
51% bar). Additionally, every row that references **Robert May** / **The May Firm** /
**Car Accident Attorney w. Robert May** / **(805) 440-9666** / **https://mayfirm.com/**
breaks the client swap. That is 15+ breakpoints on a 15-question script - the populate
is tightly bound to BOTH the jurisdiction and the client.
