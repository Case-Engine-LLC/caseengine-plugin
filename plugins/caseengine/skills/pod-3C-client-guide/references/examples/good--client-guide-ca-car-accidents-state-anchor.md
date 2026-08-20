---
label: GOOD
skill: client-guide
scope: Location
run_date: 2026-04-20
firm: The May Firm
topic: Car Accidents / How to File a Claim
episode: How to File a Car Accident Claim in California
location: CA (state-level)
source: ClickUp HQ Wiki canonical production client guide - /Users/gjordan/Desktop/research-workflow-demo--may-firm-ca/client-guide--may-firm--california-state.md
why_this_label: |
  Episode Overview leads with the VALUE PROPOSITION to the attorney's business (SEO
  visibility, trust before the phone call, command of California injury law,
  differentiation from competitors) - not a recap of topics covered. First sentence
  puts the attorney "front and center as the go-to voice on car accident claims
  across California."
  Canonical 5-section structure in the required order: Episode Overview (with
  Metadata + Episode Plan sub-sections), Pre-Interview Prep (Things to Think About +
  Things to Do), Segment Breakdown (italic intro paragraph + per-segment italic
  goal + Questions lists), FAQ (5 seed + 2 episode-specific).
  Sensitive data scrub passes cleanly: zero internal tool names (no ClickUp,
  Fortress, Spanky, PM2, ChromaDB, n-gram, entity architecture), zero "Run of Show"
  phrase (uses "episode outline", "episode plan", "episode" instead), zero SEO /
  production metrics, zero Case Engine internal process references.
  Questions in Segment Breakdown pulled VERBATIM from the upstream Client ROS
  (cleaned for client language - no producer notes, no entity bracketing) rather
  than paraphrased into broad topic areas. Matches the Exact-question rule.
  Every Pre-Interview Prep bullet follows the scannable format:
  `**Bold lead sentence with period.** Regular-weight detail that follows.`
  "Have your contact information ready" appears in Things to Do per the rule.
  Second-person voice throughout ("your expertise", "your practice", "when you")
  addressing the attorney directly. Professional but warm tone. No sales voice.
  FAQ has the 5 mandatory seed questions (recording length, need for written
  answers, not knowing an answer, review-before-publish, record location + gear)
  plus 2 episode-specific FAQs (dollar amounts from past cases, specific California
  locations) properly scoped to a damages + state-level episode.
  Host name (Kara) populated throughout the FAQ - no raw {{HOST_NAME}} tokens.
  Firm-specific breadth-of-service references (Santa Maria, Central Coast, Central
  Valley) anchor the Episode Overview in client-specific geography.
known_flaws: |
  - File opens with a "## Real Drive Routing" metadata block and a "Sandbox note"
    explaining that this copy was pulled from ClickUp for review. That block is
    reviewer-facing scaffolding and should not ship in the Drive-native Client Guide
    the attorney receives - the real Drive-native version should start directly
    with `## Episode Overview` per the Document structure preservation rule ("Drive-
    native Client Guide = Episode Overview -> Metadata -> Episode Plan -> Pre-
    Interview Prep (Think About + Do) -> Segment Breakdown -> FAQ. That's it.
    Nothing before, nothing after except standard CE branding on the DOCX cover
    page."). The Real Drive Routing block is fine for this review-canonical copy
    but must be stripped when the guide ships to the attorney.
  - Segment Breakdown does not include an Intro or Outro section header with an
    italic segment-goal paragraph. Current canonical structure requires both
    (Intro ~2 minutes + Outro ~2 minutes) with italic paragraphs describing what
    happens in those structural beats. This example jumps from the segment list
    opening paragraph straight to S1. Remediation: add `### Intro (~2 minutes)`
    and `### Outro (~2 minutes)` italic-paragraph blocks to Segment Breakdown.
    (Outro does appear as the last segment block in the file - between S4 and the
    FAQ - which is correct; only the Intro block is missing.)
  - Table of contents / Episode Plan list uses `*` bullets - the canonical format
    is fine either way; minor convention-only note.
drive_doc: null
---

# GOOD Example: Client Guide at State-level Location scope (The May Firm, California)

Read the frontmatter above before reading the guide body. The inline `<!-- SKILL REF: -->`
and `<!-- DEVIATION -->` comments below call out the calibration-critical moments. This
example is GOOD for value-prop opening, canonical 5-section structure, sensitive data
scrub discipline, verbatim question pull from the upstream Client ROS, second-person
tone, and FAQ composition. It is NON-CANONICAL on two items listed in `known_flaws` and
summarized in the Deviations section at the bottom. Everything else is verbatim from
the 2026-04-20 ClickUp canonical pull.

---

# Client Guide: How to File a Car Accident Claim - California (State-Level) - The May Firm

## Real Drive Routing

In production, this client guide would land at:
`The May Firm Podcast/Episodes/E3 - How to File a Car Accident Claim - CA/01 Strategy/Client Guide.md`

Sandbox note: this copy was pulled from the canonical ClickUp page. Internal ClickUp setup checklist stripped. Otherwise identical.

<!-- DEVIATION from SKILL Best Practices -> Canonical structure ("Drive-native Client
     Guide = Episode Overview -> Metadata -> Episode Plan -> Pre-Interview Prep
     (Think About + Do) -> Segment Breakdown -> FAQ. That's it. Nothing before,
     nothing after except standard CE branding on the DOCX cover page.") + Gotchas
     ("Do NOT include an Internal Setup block. That's ClickUp-only, legacy from the
     local producer skill. Cowork Drive-native guides start with ## Episode
     Overview.").
     This file opens with a Real Drive Routing meta-block and Sandbox note explaining
     its provenance. That block is acceptable on the review-canonical copy used for
     calibration but must be stripped when the guide ships to the attorney via
     Drive. Remediation for the Drive-native output: delete the "# Client Guide:..."
     H1, the "## Real Drive Routing" section, and the Sandbox note; start directly
     with "## Episode Overview". -->

---

## Episode Overview

This episode puts you front and center as the go-to voice on car accident claims across California. Between the heavy freeway traffic, the sheer volume of collisions, and a claims system most people don't understand until they're stuck in it, there are millions of Californians searching for clear answers after a wreck. This recording gets your expertise in front of those people before they find anyone else. It demonstrates your command of California injury law, builds trust before a phone call ever happens, and gives potential clients in Santa Maria, the Central Coast, and the Central Valley a reason to reach out to The May Firm. Every segment works toward making you the attorney people think of when they need help after a crash in California.

<!-- SKILL REF: Best Practices -> Canonical structure ("Episode Overview [LEAD WITH
     THE VALUE PROPOSITION to the attorney's business - not what topics are covered.
     Why should they care about this episode? 2-3 sentences answering 'what does
     this recording do for my practice?' - SEO visibility, trust with potential
     clients, authority, differentiation from competitors, demonstrating command of
     {jurisdiction} law.").
     The Episode Overview paragraph is a textbook value-prop opening: first sentence
     positions the attorney ("puts you front and center as the go-to voice on car
     accident claims across California"); body sentences articulate the practice
     benefit (millions of Californians searching, getting expertise in front of them
     first, building trust pre-call, serving specific geographic markets Santa Maria
     / Central Coast / Central Valley); closing sentence is the authority framing
     ("making you the attorney people think of when they need help after a crash in
     California"). Zero sentences recap episode topics. Zero sentences explain what
     will be covered. The recap lives in Metadata + Episode Plan; the Overview is
     the business-case ONLY.
     Teaches: lead with value-prop, never with topic recap. The attorney reads this
     paragraph to decide whether to give 60 minutes to the recording - make the ROI
     obvious in the first sentence. -->

### Metadata

**Episode Topic:** How to File a Car Accident Claim in California

**Estimated Duration:** ~50-60 minutes (15 questions across 4 segments)

Duration is always a range. Episodes run shorter or longer depending on how the conversation flows, and some topics get extension episodes.

### Episode Plan

*   Pre-Show Checks
*   Episode
    *   Intro
    *   S1: At the Scene - What to Do Right Now
    *   S2: California's Insurance System and Filing the Claim
    *   S3: Fault, Evidence, and Settlement Value
    *   S4: Deadlines, Uninsured Drivers, and the Legal Process
    *   Outro
*   Post-Show Wrap-up
* * *

## Pre-Interview Prep

### Things to Think About

*   **California's pure comparative negligence system.** This is the single most important California-specific concept in the episode. Unlike states that cut off recovery at 50 or 51 percent fault, California lets someone recover damages no matter what percentage of fault is assigned to them. How would you explain that to a client sitting across from you for the first time?
*   **The SR-1 form and why most people have never heard of it.** California requires drivers to file this form with the DMV within 10 days of certain accidents, and most people don't know it exists until their license gets suspended. Think about how you walk someone through this requirement.
*   **What makes California car accident claims different.** The low minimum coverage limits (15/30/5), the pure comparative negligence system, the freeway volume, the government entity claims deadline. What patterns do you see in your practice that are distinctly Californian?
*   **The insurance adjuster call.** Most of your clients get a call from the other driver's insurance company within days. What do you wish every person knew before picking up that phone?
*   **When settlement makes sense versus going to court.** Think about the factors that tip the scale in your experience. What does the timeline look like for straightforward claims versus cases that end up in litigation in Superior Court?

<!-- SKILL REF: Best Practices -> Canonical structure ("Things to Think About
     [Mindset prompts. These are reflective questions, NOT tasks. Frame as 'How
     would you explain X?', 'What do you wish every client knew about Y?', 'What
     patterns do you see in your practice around Z?'. Derive from the Client ROS
     content. 4-6 bullets.]") + "Bullet format rule (applies to both sections):
     Every bullet uses the scannable format: `**Bold lead sentence with period.**
     Regular-weight detail that follows.`".
     Five reflective prompts, all in the required scannable format: bold lead is a
     discrete noun-phrase concept (California's pure comparative negligence, SR-1
     form, what makes CA claims different, insurance adjuster call, settlement vs
     court), then regular-weight detail explains the reflection. Every bullet asks
     the attorney a REFLECTIVE question ("How would you explain that...", "Think
     about how you walk...", "What patterns do you see...", "What do you wish every
     person knew...", "What does the timeline look like..."). Zero tasks. Tasks
     live in Things to Do.
     Teaches: Things to Think About = reflective prompts framed as questions that
     prime mindset, not action. Things to Do = tasks. Mixing them is a hard fail. -->

### Things to Do

*   **Pull 2-3 anonymized case stories from your practice.** Ideally: one where acting quickly on documentation and medical care made the difference, one where a missed deadline or delayed treatment hurt the claim, and one where comparative negligence was a factor and evidence preservation changed the outcome.
*   **Confirm current California minimum auto insurance requirements.** The episode references the 15/30/5 minimums. Verify these are still current as of the recording date.
*   **Review your firm's typical contingency fee structure.** The episode covers how attorney fees work. Be ready to share your standard approach and what happens if a case goes to trial.
*   **Refresh on the government entity claims deadline.** The California Tort Claims Act gives just 6 months to file a claim against a government entity. Be ready to explain why this one catches people off guard and what happens when it's missed.
*   **Have your contact information ready.** At the end of the episode, Kara will ask how listeners can reach The May Firm. Be ready to share your website ([mayfirm.com](http://mayfirm.com)), phone number, and confirm the free consultation.
* * *

<!-- SKILL REF: Best Practices -> Canonical structure ("Things to Do [Actionable
     prep items. Specific research to pull, materials to gather, data to look up,
     confirmations to make. 4-6 bullets. Always include: 'Have your contact
     information ready' as one of the items so the attorney expects the closing
     CTA.]").
     Five Things to Do items. All are TASKS with concrete action verbs (Pull,
     Confirm, Review, Refresh, Have X ready) and specific context (2-3 anonymized
     case stories, 15/30/5 minimums, contingency fee approach, 6-month government
     deadline, contact info for the closing). Last item is the mandatory "Have your
     contact information ready" anchor - the attorney must expect the closing CTA
     so they have phone + website + free-consult language queued up. Host name
     "Kara" is populated (not {{HOST_NAME}}).
     Teaches: Things to Do bullets are tasks with verbs; the Have-contact-
     information-ready item is non-negotiable and must appear in every guide. -->

## Segment Breakdown

_Below is a breakdown of each segment with the topics you should be prepared to discuss. You don't need to memorize answers - just be familiar with the topics so the conversation flows naturally._

### Intro (~2 minutes)

_Kara handles the intro and welcomes viewers to Car Accident Attorney w. Robert May. She'll introduce you, set up the episode topic, and frame it for the California audience. Your role is to greet viewers and settle into the conversation._

### S1: At the Scene - What to Do Right Now (~10 minutes)

_This segment covers what someone should do in the immediate aftermath of a car accident in California. The goal is to give listeners a clear action plan for those chaotic first minutes - from safety and calling 911 to documenting the scene to getting medical care even when they feel fine. California-specific context matters here: the CHP handling freeway accidents, the SR-1 form requirement that most people don't know about, and the importance of getting checked out medically within that first 72-hour window._

#### Questions

*   Q1: What should someone do immediately after a car accident in California to protect their claim?
*   Q2: Should I call the police even if the accident seems minor, and what is the SR-1 form?
*   Q3: Do I need medical care even if I feel fine after the crash?

<!-- SKILL REF: Best Practices -> Exact-question rule ("DO use the exact question
     text in the Segment Breakdown Questions list (cleaned up for client language -
     no producer notes, no entity bracketing, no inline annotations). DO NOT
     paraphrase questions into 'broad topic areas' in the Questions list. The
     earlier version of this skill said paraphrase; the current canonical format
     lists questions directly.") + Best Practices -> Translation table ("Individual
     questions | Listed verbatim in Segment Breakdown Questions").
     Q1/Q2/Q3 pulled verbatim from the upstream Client ROS source at
     /Users/gjordan/Desktop/claude_code/deliverables/podcast-research/car-accidents/
     2. how-to-file-car-accident-claim/locations/ca/client/the may firm/
     how-to-file-car-accident-claim-ca-v1.md. Cleaned only for client-facing display:
     no <u>entity</u> tags, no **bold** markers from the ROS, no producer-note
     annotations, no time budgets. Question text itself is identical to the ROS.
     Italic segment-goal paragraph above the Questions list gives the WHY of the
     segment (chaotic first minutes, CHP / SR-1 / 72-hour window) - derived from
     the upstream ROS producer notes + Q content, NOT invented.
     Teaches: questions are verbatim from ROS; italic paragraphs derive from ROS
     producer notes. Paraphrasing into "broad topic areas" is a legacy pattern that
     the current canonical explicitly rejects. -->

### S2: California's Insurance System and Filing the Claim (~12 minutes)

_This segment walks through the mechanics of how car accident claims actually work in California. Listeners need to understand the fault-based system, the step-by-step filing process, what documents to gather, how to handle the insurance adjuster, and the common mistakes that sink claims. The adjuster conversation and social media warnings are particularly important - most people don't realize how much their own behavior after the accident affects their recovery._

#### Questions

*   Q4: How do I file a car accident insurance claim step by step, and who should I contact first?
*   Q5: What documents do I need to start a car accident claim?
*   Q6: What should you say and not say to an insurance adjuster, and should you give a recorded statement?
*   Q7: What common mistakes can hurt a car accident claim?

### S3: Fault, Evidence, and Settlement Value (~15 minutes)

_This is the longest segment and covers how fault gets assigned, what evidence drives settlement value, and how California's pure comparative negligence system works in practice. The key message is that California has no cutoff - even at 80 percent fault, a person can still recover 20 percent of their damages. Medical records, traffic camera footage, and accident reconstruction are all fair game here. This is also where hiring an attorney comes into the conversation._

#### Questions

*   Q8: How is fault determined in a car accident claim, and how much weight does the police report carry?
*   Q9: What evidence beyond photos and medical records can make or break a car accident claim?
*   Q10: How do medical records and documentation affect a car accident settlement?
*   Q11: Can I still file a claim if I was partially at fault?
*   Q12: When should someone seriously consider hiring a car accident attorney?

### S4: Deadlines, Uninsured Drivers, and the Legal Process (~14 minutes)

_The final segment covers the hard deadlines, settlement-versus-lawsuit decision, and what happens when the other driver has no insurance or flees the scene. The statute of limitations (2 years personal injury, 3 years property damage), the 6-month government entity deadline, and the role of uninsured/underinsured motorist coverage are all critical here. Listeners should walk away knowing exactly what timeline they're working with and what to do if they're in a hit-and-run situation._

#### Questions

*   Q13: How long does a car accident claim usually take, and when should you settle instead of filing a lawsuit?
*   Q14: How long do you have to file a car accident lawsuit in California, and what happens if you miss it?
*   Q15: What happens if the other driver doesn't have insurance or flees the scene?

### Outro (~2 minutes)

_Kara wraps up the episode and directs listeners to The May Firm. Be ready to share your website (_[_mayfirm.com_](http://mayfirm.com)_), phone number, and confirm that the initial consultation is free._
* * *

## FAQ

*   **How long will the recording take?** Plan for 50-60 minutes of recording time, plus a few minutes for setup and a post-show wrap-up. Some topics may run shorter or longer depending on how the conversation flows.
*   **Do I need to prepare written answers?** No. Just review the topics above so they feel familiar. Kara will lead the conversation and ask follow-ups to get the details we need.
*   **What if I don't know the answer to something?** That's completely fine. Kara will move on or rephrase. This is a conversation, not a deposition.
*   **Will I get to review the episode before it goes live?** Yes. You'll have the opportunity to review the edited episode before it's published.
*   **Where do I record and what do I need?** The recording happens on [Riverside.fm](http://Riverside.fm). We'll send you a link before the session. Use a quiet space with minimal background noise, good lighting, and a stable internet connection. This is a video recording, so wear what makes you feel professional and comfortable.
*   **Can I mention specific dollar amounts from past cases?** Be careful with specific numbers. Anonymized ranges ("settlements in the six-figure range") work well. Avoid anything that could identify a past client or create unrealistic expectations.
*   **Should I mention specific California locations?** Absolutely. References to local freeways, the Central Coast, the Central Valley, specific courts, and local landmarks make the episode feel authentic and relevant to California listeners. The more specific to your service area, the better.

<!-- SKILL REF: Best Practices -> Canonical structure ("FAQ [5 seed FAQs always
     included, plus 2-3 episode-specific FAQs. Format: `**Question?** Answer.`]")
     + Quality gates -> Content ("FAQ has 5 seed + 2-3 episode-specific", "Host
     name populated in FAQ references (not {{HOST_NAME}} raw)").
     FAQ has exactly the 5 mandatory seed questions in order: recording length
     (50-60 minutes), no written answers needed, what if I don't know, review-
     before-publish, record location + gear (Riverside.fm). Plus 2 episode-specific
     FAQs scoped correctly to this episode: dollar amounts (damages-heavy episode
     justifies the caution) and California locations (state-level geographic
     guidance). Host name "Kara" populated throughout - no raw {{HOST_NAME}}
     tokens. Format is **Bold Question?** Plain-text answer per the rule.
     Teaches: 5 seed FAQs are non-negotiable; 2-3 episode-specific FAQs must
     derive from the actual episode content (damages episode -> dollar-amount
     caution; state-level episode -> location guidance). Host name populates,
     never leaks as a token. -->

<!-- SKILL REF: Best Practices -> Sensitive data scrub ("No internal tool names
     (ClickUp, Fortress, Spanky, PM2, ChromaDB, n-gram table, entity architecture).
     No internal team names. No pricing, contract details, production metrics.
     No entity architecture, vector strengths, SEO strategy language, n-gram
     targets. No Case Engine internal process references. No 'Run of Show' phrase
     - call it 'episode outline' or 'episode plan'.") + Gotchas ("Do NOT use 'Run
     of Show' or 'ROS' in the client guide body. Call it 'episode outline' or
     'episode plan'.").
     Full-body scrub passes cleanly: zero mentions of ClickUp, Fortress, Spanky,
     PM2, ChromaDB, n-gram, entity architecture, Case Engine-as-internal-process,
     SEO metrics, vector strengths, production tooling. The phrase "Run of Show"
     never appears in the body - the Episode Plan list uses "Episode" and "Pre-
     Show Checks" and "Post-Show Wrap-up" instead. Episode Plan is referenced as
     "episode outline" indirectly via the Segment Breakdown section header
     "Below is a breakdown of each segment". The attorney sees only client-
     appropriate framing.
     Teaches: the scrub is a hard wall. Every internal tool name, every production
     metric, every use of "Run of Show" must be grepped out before the guide ships
     to the attorney. The client never sees how the sausage is made. -->

---

## Calibration Summary

Future runs of this skill should replicate these seven rules. If an output misses any
of them, it drops below GOOD threshold:

1. **Episode Overview opens with the VALUE PROPOSITION to the attorney's business, not a topic recap.** First sentence positions the attorney ("go-to voice", "authority in the space"). Body sentences articulate practice benefits (SEO visibility, trust before the call, geographic reach, authority). Closing sentence is the authority-framing payoff. Topic recap belongs in Metadata + Episode Plan, not the Overview.
2. **Canonical 5-section structure in exact order.** Episode Overview (with Metadata + Episode Plan sub-sections) -> Pre-Interview Prep (Things to Think About + Things to Do) -> Segment Breakdown (italic intro paragraph + per-segment italic goal + Questions list) -> FAQ. Nothing before `## Episode Overview` except standard CE branding on the DOCX cover. Nothing after FAQ.
3. **Pre-Interview Prep bullets use the scannable format: `**Bold lead sentence with period.** Regular-weight detail that follows.`** Every bullet, both sections. Things to Think About bullets are reflective prompts framed as questions; Things to Do bullets are tasks framed as action verbs. Mixing them is a hard fail. "Have your contact information ready" must appear in Things to Do.
4. **Questions in Segment Breakdown pulled VERBATIM from the upstream Client ROS** (cleaned for client language - no producer notes, no entity bracketing, no time budgets, no `**bold**` markers). Paraphrasing into "broad topic areas" is a legacy pattern the current canonical rejects.
5. **Italic segment-goal paragraphs above each Questions list derive from the upstream Client ROS** (producer notes + Q content) - not invented. Each paragraph gives the WHY of the segment, not a topic list.
6. **FAQ has exactly 5 mandatory seed FAQs plus 2-3 episode-specific FAQs.** Format is `**Question?** Answer.` Host name populated in every reference - never leaves `{{HOST_NAME}}` raw. Episode-specific FAQs must derive from actual episode content (damages episode triggers dollar-amount caution; state-level episode triggers location-specificity guidance; etc.).
7. **Full-body sensitive data scrub passes.** Zero internal tool names (ClickUp / Fortress / Spanky / PM2 / ChromaDB / n-gram / entity architecture). Zero "Run of Show" phrase (use "episode outline" or "episode plan"). Zero production metrics, SEO language, or Case Engine internal process references. Zero sales / marketing voice. Second-person throughout ("your expertise", "your practice").

---

## Deviations from current canonical

This example is GOOD for the seven Calibration Summary rules above. It is NON-CANONICAL
on two items. Future runs should fix these before the guide ships to the attorney.

| # | SKILL rule (section + specific) | What this example does | Scope of deviation |
|---|---|---|---|
| 1 | Best Practices -> Canonical structure + Gotchas ("Drive-native Client Guide = Episode Overview -> Metadata -> Episode Plan -> Pre-Interview Prep (Think About + Do) -> Segment Breakdown -> FAQ. That's it. Nothing before, nothing after except standard CE branding on the DOCX cover page.") | Opens with `# Client Guide:...` H1, a `## Real Drive Routing` section, and a Sandbox provenance note before `## Episode Overview` | First 9 lines of the file (review-canonical scaffolding that must be stripped from the Drive-native version) |
| 2 | Best Practices -> Canonical structure ("Segment Breakdown includes `### Intro (~2 minutes)` and `### Outro (~2 minutes)` with italic segment-goal paragraphs") | Outro block is present correctly. Intro block is missing between the "_Below is a breakdown..._" italic opener and the first `### S1:` segment header. | One missing `### Intro (~2 minutes)` block + italic paragraph |

**Reader takeaway:** use this example to calibrate the value-prop opening, canonical
5-section structure, scannable bullet format, verbatim question pull from the upstream
Client ROS, italic-segment-goal derivation, FAQ composition, and the sensitive data
scrub. Do NOT copy the Real Drive Routing opener or the Sandbox note - those are
review-only scaffolding that must be stripped from the attorney-facing Drive-native
version. Add an `### Intro (~2 minutes)` block in Segment Breakdown before S1 to match
current canonical.

### The single-question stress test

Pick any row in the Segment Breakdown (italic segment-goal paragraph, Questions list,
Episode Overview paragraph). Ask: "If I swapped California for Texas and The May Firm
for Sutliff & Stout, would this still work or would it break?"

- If every row still works after the swap, the guide is state-scope-neutral dressed up
  as California and fails the Location-scope inheritance check - the guide would be
  useless for a California-specific prep because it would not prime the attorney on
  California-specific talking points.
- If at least 5-7 rows break after the swap, the guide is genuinely California-bound
  and client-bound.

Breakpoints on this guide: Episode Overview references ("across California", "Santa
Maria, the Central Coast, and the Central Valley", "The May Firm", "after a crash in
California"). Pre-Interview Prep Things to Think About bullet 1 (California's pure
comparative negligence, distinguishes from 50/51 percent bar states). Bullet 2 (SR-1
form, California DMV, 10 days). Bullet 3 (15/30/5 minimums, pure comparative negligence,
California-specific framing). Things to Do bullet 2 (California minimum auto insurance,
15/30/5). Bullet 4 (California Tort Claims Act, 6-month deadline). Bullet 5 (Kara,
mayfirm.com). Segment Breakdown italic goals reference California Highway Patrol,
SR-1 form, California's pure comparative negligence, Superior Court of California,
California Tort Claims Act. FAQ episode-specific questions reference California
locations / Central Coast / Central Valley / mayfirm.com / Kara. Easily 10+ breakpoints
on swap - the guide is tightly bound to California state law + The May Firm client
context. Passes the Location-scope localization check decisively.
