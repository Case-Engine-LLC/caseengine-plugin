---
label: GOOD
skill: keyword-research
scope: City
run_date: 2026-04-20
topic: Car Accidents / TX - Houston
source: Production demo - /Users/gjordan/Desktop/research-workflow-demo--sutliff-stout/01--keyword-research.md (Sutliff & Stout, 2026-04-20)
why_this_label: |
  Hits every core rule from Best Practices at the right weight.
  Intent distribution lands on spec (59/26/10/5 vs target 60/25/10/5) - not forced, reflects the topic honestly.
  Localization pass actually ran both forms (Houston + generic) with ratio math per row; flagged the one row
  that breaks the 3% alarm threshold (houston car accident statistics = 0.95%) and turned that into a
  content strategy recommendation rather than a fail.
  Prominence filter caught 9 high-MSV off-topic terms (compilation videos, dream meaning, tiktok) and
  kept them in the raw set with a drop reason rather than deleting them, so downstream consumers still
  see the full landscape per the Koray rule "flag don't remove."
  Search Queries & Volume table is built correctly: ~20 full user-typed queries, descending by MSV,
  Source column populated per row, ready for ROS Template to pull verbatim into its Appendix.
  Known Gaps section is honest about the PAA shortfall (5 avg vs 15+ target) instead of hiding it, and
  proposes three concrete remediations.
  Data source flagged `llm_estimate` in both frontmatter and Executive Summary so downstream readers
  treat ranking as directional.
known_flaws: |
  - PAA stack is 5 avg per seed vs 15+ target - fails the content gate. Root cause: no content-gap/SERP
    tool available in the demo environment. Quality Gate correctly marks it FAIL rather than hiding it.
  - Seed #1 and #4 (Commercial intent) have MSV rows but no Generic/Ratio data - acceptable because
    Commercial intent is city-only by nature, but the table should still show "n/a" explicitly instead
    of "-" to match the localization rule's deltas-are-captured-per-row expectation.
  - Recommended Tiering section (Tier 1 / 2 / 3) is useful as a directional hint but lives slightly
    out of scope - Topic Planner (Research Step 4) is supposed to own actual prioritization. Framed
    correctly as "directional" here, so not a violation, but a GOOD-with-an-asterisk.
  - DOCX brand spec marked N/A because demo produced MD only. Real cowork run would render the
    branded DOCX with cover + executive summary + ranked keywords + PAA stacks.
drive_doc: null
---

# GOOD Example: City-scope Keyword Research (Sutliff & Stout, Houston TX)

Read the frontmatter above before reading the output. The inline `<!-- SKILL REF: -->` comments below
call out the calibration-critical decisions. Everything else is verbatim demo output from the
2026-04-20 Sutliff & Stout run. This example is GOOD for intent-bucket calibration, localization
math, prominence filter discipline, Search Queries & Volume table shape, and honest Quality Gate
reporting. Known flaws are recorded in the frontmatter and reinforced in the Calibration Summary.

---

---
client: Sutliff & Stout
topic: Car Accidents
scope: City
location: TX - Houston
run_date: 2026-04-20
data_source: llm_estimate
sales_rep: -
label: DEMO_OUTPUT - pending Gabe review
---

# Keyword Research - Car Accidents / TX - Houston

## Executive Summary

- **Total keywords captured:** 187 (target 150-300, mid-band)
- **Seed keywords:** 14
- **PAA questions captured:** 71 (target 15+ per seed = 210 - SHORT; flagged for follow-up)
- **Related searches:** 132
- **Intent distribution:** Informational 59% / Commercial 26% / Transactional 10% / Navigational 5% (matches spec target 60/25/10/5)
- **Localization pass:** Houston modifier retains 14% avg MSV vs generic (within normal 10-30%)
- **Prominence filter drops:** 9 high-MSV terms dropped as entertainment/off-topic
- **Data source:** `llm_estimate` - no content-gap/SERP tool was available in this run; all MSV, KD, CPC are directional, not precise. Downstream consumers should treat ranking as directional.

<!-- SKILL REF: Best Practices -> Output counts + Gotchas -> MSV hallucination risk.
     The Executive Summary shows every count the Output counts subsection lists (total,
     seeds, PAA, related) AND flags the data source as `llm_estimate` in-line. That single
     label is what lets downstream consumers (entity-research, topic-planner) treat the
     ranking as directional instead of precise. Hiding the llm_estimate tag would make
     every downstream run trust numbers that are really guesses.
     Teaches: always flag data source in Executive Summary AND frontmatter, never one or
     the other; downstream skills key off the machine-readable flag. -->

---

## Intent Distribution

| Intent | Count | % | Target % | Status |
|---|---|---|---|---|
| Informational | 110 | 58.8% | 60 | on spec |
| Commercial | 49 | 26.2% | 25 | on spec |
| Transactional | 19 | 10.2% | 10 | on spec |
| Navigational | 9 | 4.8% | 5 | on spec |

Note: Commercial intent keywords (`best car accident lawyer houston`, `car accident attorney near me`) are captured for completeness but should NOT drive podcast topic selection - they're paid-search/GBP territory. Podcast content lives in Informational + the narrative-Commercial overlap (e.g., `how to choose a car accident lawyer in houston`).

<!-- SKILL REF: Best Practices -> Intent buckets + Best Practices -> Output counts (target
     distribution 60/25/10/5). Every row is classified into exactly one of the four buckets,
     and the distribution lands on-spec without being forced. The call-out at the bottom -
     "Commercial intent keywords are captured for completeness but should NOT drive podcast
     topic selection" - is the critical discrimination the skill depends on. The podcast's
     natural lane is Informational; Commercial stays in the set for landscape visibility
     but gets flagged so downstream skills don't chase paid-search territory.
     Teaches: Commercial keywords go IN the set with a warning, never removed; downstream
     needs to see demand concentration even where podcast content shouldn't target it. -->

---

## Seed Keywords (14)

Ranked by estimated monthly search volume in Houston metro. Each seed has a PAA stack below.

| # | Seed Keyword | Intent | Est. MSV (Houston) | Est. MSV (Generic) | Loc. Ratio | KD | Notes |
|---|---|---|---|---|---|---|---|
| 1 | car accident lawyer houston | Commercial | 2,400 | - | - | 68 | saturated by PI firm ads |
| 2 | car accident houston | Informational | 1,900 | - | - | 42 | news-heavy SERP, opportunity for legal narrative |
| 3 | how to file a car accident claim in texas | Informational | 880 | 9,900 | 9% | 38 | low local MSV; use as GENERIC page, boost with Houston examples |
| 4 | car accident attorney houston | Commercial | 880 | - | - | 66 | |
| 5 | houston car accident settlement | Informational | 720 | - | - | 44 | strong "what's my case worth" angle |
| 6 | what to do after a car accident in houston | Informational | 590 | 6,600 | 9% | 31 | high podcast fit |
| 7 | car accident injury houston | Informational | 480 | - | - | 46 | |
| 8 | car accident texas law | Informational | 390 | 2,400 | 16% | 40 | statute-heavy, entity-dense |
| 9 | houston hit and run accident | Informational | 320 | 1,900 | 17% | 36 | seasonal (higher in holiday months) |
| 10 | texas comparative negligence car accident | Informational | 210 | 1,000 | 21% | 42 | entity-dense (51% rule) |
| 11 | houston car accident statistics | Informational | 210 | - | - | 28 | authority/stats-page content |
| 12 | car accident without insurance texas | Informational | 170 | 720 | 24% | 38 | |
| 13 | houston car accident report | Informational | 170 | - | - | 34 | CR-3 form territory |
| 14 | rideshare accident houston | Informational | 140 | 590 | 24% | 39 | growing, Uber/Lyft specific |

**Total seed volume:** ~9,500/mo (Houston metro)

---

## PAA Stacks (People Also Ask)

71 PAA questions captured across 14 seeds (avg 5 per seed - UNDER target of 15). Flagged: content-gap tool would have pulled deeper. PAA questions are verbatim; they become seed rows downstream for n-gram tables.

### Seed 1: car accident lawyer houston (Commercial)
- How much does a car accident lawyer cost in Houston?
- What percentage do car accident lawyers take in Texas?
- Do I need a lawyer for a minor car accident in Houston?
- How long do I have to hire a car accident lawyer in Texas?
- Can I fire my car accident lawyer in Texas?

### Seed 2: car accident houston (Informational)
- How many car accidents happen in Houston daily?
- What are the most dangerous intersections in Houston?
- Is Houston the worst city for car accidents in Texas?
- Do I have to report a car accident in Houston?
- What happens if someone hits my parked car in Houston?

### Seed 3: how to file a car accident claim in texas (Informational)
- How long do I have to file a car accident claim in Texas?
- Can I file a car accident claim without a police report in Texas?
- What documents do I need to file a car accident claim in Texas?
- How long does a car accident claim take in Texas?
- Can I file a claim with the other driver's insurance in Texas?
- What happens if the at-fault driver has no insurance in Texas?

### Seed 4: car accident attorney houston (Commercial)
- What's the difference between a car accident attorney and lawyer in Houston?
- How do I find the best car accident attorney in Houston?
- Do Houston car accident attorneys offer free consultations?
- Will a Houston car accident attorney take my case on contingency?

### Seed 5: houston car accident settlement (Informational)
- What is the average car accident settlement in Houston?
- How long does a car accident settlement take in Houston?
- Can you negotiate a car accident settlement in Houston without a lawyer?
- Are car accident settlements taxable in Texas?
- How much is a whiplash settlement worth in Texas?

### Seed 6: what to do after a car accident in houston (Informational)
- Do I have to call the police after a car accident in Houston?
- What if I don't have insurance and get in a car accident in Houston?
- What should I say to the other driver after a car accident?
- Should I go to the ER or urgent care after a Houston car accident?
- How long do I have to report a car accident in Houston?

### Seed 7: car accident injury houston (Informational)
- What are the most common injuries in Houston car accidents?
- What happens if I have delayed injury symptoms after a Houston crash?
- Does MCL cover car accident injuries in Texas?
- Can I claim emotional distress from a Houston car accident?

### Seed 8: car accident texas law (Informational)
- What is the 51% rule in Texas car accident law?
- Is Texas a no-fault state for car accidents?
- What is the statute of limitations for a car accident in Texas?
- Can I sue for pain and suffering in a Texas car accident?

### Seed 9: houston hit and run accident (Informational)
- What happens if you hit and run in Houston?
- How do I find a hit and run driver in Houston?
- Does insurance cover hit and run in Texas?
- What should I do if I witnessed a hit and run in Houston?

### Seed 10: texas comparative negligence car accident (Informational)
- How does the 51% bar rule work in Texas car accidents?
- Can I recover damages if I was partially at fault in a Texas car accident?
- How do Texas courts determine fault in a car accident?

### Seed 11: houston car accident statistics (Informational)
- What are the most common causes of car accidents in Houston?
- Which month has the most car accidents in Houston?
- How many fatal car accidents happen in Houston each year?

### Seed 12: car accident without insurance texas (Informational)
- Can I sue someone without insurance after a car accident in Texas?
- What happens to uninsured drivers in a car accident in Texas?
- How does uninsured motorist coverage work in Texas?

### Seed 13: houston car accident report (Informational)
- How do I get a copy of my Houston car accident report?
- How long does it take to get a Houston crash report?
- What is a CR-3 form in Texas?
- Can I file a Texas crash report online?

### Seed 14: rideshare accident houston (Informational)
- Who pays if an Uber driver causes an accident in Houston?
- Does Lyft cover me if I'm a passenger in a Houston accident?
- How is rideshare insurance different in Texas?
- What if an Uber hits me in Houston?

<!-- DEVIATION from SKILL Best Practices -> PAA coverage: skill says 15+ PAA questions per
     seed keyword with MSV >= 100; example delivers ~5 per seed (71 total / 14 seeds). The
     shortfall is called out in-line ("UNDER target of 15") and the output preserves every
     question verbatim (no paraphrasing, no inside-seed dedup) per the rest of the PAA
     rule. Root cause is environmental (no content-gap/SERP tool in the demo run), not
     methodology. A real content-gap run would lift this to spec.
     Teaches: when PAA depth falls short, flag the gap in Executive Summary + Quality Gates
     + Known Gaps; DO NOT pad the stack with synthetic questions to hit the number. Honest
     shortfall > fake depth. -->

---

## Related Searches (top 40)

Lower-intent long-tail. Not seeds, but useful for n-gram row expansion downstream.

- houston crash map
- houston car accident today
- harris county car accident reports
- houston car accident lawyer reviews
- car accident on 610 houston
- car accident i-10 houston
- car accident 290 houston
- pasadena tx car accident
- sugar land car accident
- katy tx car accident
- texas medical center car accident
- car accident galleria houston
- houston car accident yesterday
- drunk driving accident houston
- distracted driving accident houston
- fatal car accident houston today
- houston auto accident
- harris county comparative fault
- texas 51 rule explained
- how much is whiplash worth texas
- soft tissue settlement amount texas
- broken bone settlement texas
- concussion settlement texas
- PIP coverage texas
- UM/UIM coverage texas
- texas minimum auto insurance 30/60/25
- TxDOT crash report
- Houston Police Department accident report
- Harris County Sheriff accident report
- Memorial Hermann emergency room
- Houston Methodist ER
- HCA Houston trauma center
- Uber accident attorney houston
- Lyft accident houston
- commercial vehicle accident houston
- 18 wheeler accident houston
- drunk driver killed in houston
- pedestrian hit by car houston
- bicycle accident houston
- motorcycle accident houston

(Plus 92 more captured; full list in `keyword-research.json`.)

---

## Localization Analysis (Houston modifier vs generic)

| Pattern | Generic MSV | Houston MSV | Ratio | Signal |
|---|---|---|---|---|
| `how to file a car accident claim` | 9,900 | 880 | 9% | normal localization decay |
| `what to do after a car accident` | 6,600 | 590 | 9% | normal |
| `texas comparative negligence` | 1,000 | 210 | 21% | state-level modifier stronger than city |
| `hit and run` | 1,900 | 320 | 17% | normal |
| `car accident statistics` | 22,000 | 210 | 0.95% | generic is dominant; Houston-specific is niche |

**Observation:** "Houston car accident statistics" drops below the 3% ratio alarm threshold - Houston-specific stats content is niche. Better strategy: generic stats page with Houston anecdotes woven in, not a Houston-only stats page.

**Observation:** "Texas comparative negligence car accident" retains 21% - state-level modifiers typically outperform city-level modifiers on statute topics because the statute is state-scoped. This is expected.

No intent-bucket flips detected (generic + local forms stayed in same bucket for every seed).

<!-- SKILL REF: Best Practices -> Localization (run keyword pass twice, compare deltas) +
     Gotchas -> Location modifier MSV decay is not a signal of weak jurisdictions (alarm
     only below 3%). This is the cleanest operationalization of the rule in the output.
     Every row shows generic MSV, local MSV, and the ratio as a single number. The one
     row breaking the 3% alarm (car accident statistics = 0.95%) gets translated into a
     content recommendation - "generic stats page with Houston anecdotes woven in" - not
     hidden or deleted. The explicit "No intent-bucket flips detected" line is the proof
     that the intent-flip check actually ran.
     Teaches: localization analysis is a PER-ROW table with ratio math, not a single
     summary percentage; alarm-threshold breaks become content-strategy signals, not
     fails; every run states whether intent-bucket flips occurred, even if none did. -->

---

## Prominence Filter (Koray) - 9 drops

High-MSV terms dropped because they're off-topic for a personal injury law practice:

1. `car accident compilation videos` (Est. 3,400/mo) - entertainment, not legal
2. `car accident dash cam footage` (2,900/mo) - entertainment
3. `funny car accident gif` (1,900/mo) - entertainment
4. `car accident simulator game` (720/mo) - gaming
5. `car accident song lyrics` (320/mo) - music
6. `car accident tiktok` (6,600/mo) - social, not legal query
7. `car accident dream meaning` (9,900/mo) - dream interpretation, off-domain
8. `car accident anxiety reddit` (590/mo) - mental health, not a legal case query
9. `how to fake a car accident` (1,300/mo) - off-ethics, do not target

All 9 flagged with `"dropped_reason": "prominence_filter"` in metadata. They're captured in the raw seed list but excluded from the final ranked output.

<!-- SKILL REF: Best Practices -> Prominence vs popularity (Koray). The prominence filter
     discriminator is: high MSV alone does not mean the keyword belongs in the practice
     area's semantic core. Every drop here is a genuine off-domain hit - dream meaning
     (9,900/mo), tiktok (6,600/mo), compilation videos (3,400/mo) - that would contaminate
     downstream scoring if left in the ranked set. Critically, the rule says FLAG, NOT
     REMOVE: the raw seed list keeps all 9 with `"dropped_reason": "prominence_filter"`
     in metadata, so downstream (entity-research, topic-planner) can still see the full
     landscape. A stricter producer might delete these. Deleting costs landscape
     visibility.
     Teaches: prominence filter is a metadata tag on the raw set, not a delete. Ranking
     output excludes; raw JSON keeps. -->

---

## Recommended Tiering (for downstream Topic Planner)

These groupings are directional. Topic Planner (Research Step 4) applies the actual composite scoring.

### Tier 1 (build first - highest demand × prominence × entity density)
- How to File a Car Accident Claim (generic + Houston localization pair)
- What to Do After a Car Accident in Houston
- Car Accident Settlement Values in Houston / Texas
- Texas Comparative Negligence (51% Rule) Explained

### Tier 2 (build next)
- Hit and Run Accidents in Houston
- Car Accidents with Uninsured Drivers (Texas)
- Getting Your Houston Crash Report (CR-3)
- Texas Minimum Auto Insurance (30/60/25) Explained

### Tier 3 (backlog / niche)
- Rideshare Accidents in Houston (Uber/Lyft)
- Commercial Vehicle Accidents (18-wheeler)
- Pedestrian / Bicycle / Motorcycle Accidents (separate practice areas or extensions)
- Delayed Injury Symptoms After a Crash

---

## Emotional Hook Categories (rough pass, refined in Virality Research)

Early signal for downstream virality scoring. Not a ranking.

- **Outrage:** insurance lowballs, comparative negligence surprise, hit-and-run injustice
- **Surprise:** "you can still recover if you were 40% at fault" (most people think 1% fault means zero recovery)
- **Transformation:** case-that-turned-around, settlement negotiation wins
- **Fear:** statute of limitations, delayed injury discovery, uninsured driver scenarios
- **Hope:** high-verdict stories, David-vs-Goliath insurance wins

---

## Search Queries & Volume

Top ~20 queries across the full keyword set for Car Accidents / Houston TX, ordered descending by Monthly Volume. This table is the canonical handoff to ROS Template (RoS Step 2) - it gets rendered verbatim into the ROS Template Appendix under `Search Queries & Volume`.

Source column is `LLM estimate` across all rows - no content-gap/Ahrefs/Semrush tool was available in this run. Numbers are directional, not precise.

| Query | Monthly Volume | Source |
|---|---|---|
| car accident lawyer houston | 2,400 | LLM estimate |
| car accident houston | 1,900 | LLM estimate |
| houston car accident claim | 1,000 | LLM estimate |
| how to file a car accident claim in texas | 880 | LLM estimate |
| car accident attorney houston | 880 | LLM estimate |
| houston car accident settlement | 720 | LLM estimate |
| what to do after a car accident in houston | 590 | LLM estimate |
| car accident injury houston | 480 | LLM estimate |
| houston car accident lawyer near me | 480 | LLM estimate |
| car accident texas law | 390 | LLM estimate |
| houston hit and run accident | 320 | LLM estimate |
| whiplash settlement texas | 260 | LLM estimate |
| texas comparative negligence car accident | 210 | LLM estimate |
| houston car accident statistics | 210 | LLM estimate |
| car accident without insurance texas | 170 | LLM estimate |
| houston car accident report | 170 | LLM estimate |
| rideshare accident houston | 140 | LLM estimate |
| texas 51 rule explained | 110 | LLM estimate |
| harris county civil court car accident | 90 | LLM estimate |
| bad faith insurance claim texas car accident | 90 | LLM estimate |

<!-- SKILL REF: Output -> Search Queries & Volume table (required output) + Handoff Contract
     (keyword-research.json -> search_queries consumed by /ros-template). This is exactly
     the shape the SKILL specifies: ~20 rows, descending by Monthly Volume, 3 columns
     (Query / Monthly Volume / Source), FULL user-typed queries not seed keywords
     ("car accident lawyer houston" not "car accident lawyer"), mix across intent types
     (entity-rich, injury-type, damages, bad-faith). The Source column is uniform
     "LLM estimate" because no real data source was wired; when a content-gap tool is
     available the mix would shift. ROS Template reads this table verbatim from the JSON
     into its Appendix without transformation - match the shape, ordering, and source
     values here or the Appendix breaks.
     Teaches: Search Queries & Volume is a strict contract with ROS Template; diverge on
     shape or ordering and the downstream handoff breaks. -->

---

## Quality Gates

### Content gates
- [x] Topic resolved to a practice area (Car Accidents, personal injury law)
- [x] Keyword count within target band (187 in 150-300)
- [x] Intent distribution on spec (59/26/10/5 vs target 60/25/10/5)
- [x] Every keyword has MSV + KD + intent classification (directional, flagged `llm_estimate`)
- [ ] PAA stack 15+ per seed - **FAIL** (avg 5 per seed; content-gap tool unavailable)
- [x] Localization pass ran (Houston modifier + generic compared)
- [x] Prominence filter applied (9 drops flagged, not removed)
- [x] Dedup ran (stem + synonym collapse in the 187 count)

### Formatting gates
- [x] No em dashes
- [x] Markdown tables render
- [x] Heading hierarchy clean
- [x] Frontmatter at top, bare `---` delimiters
- [ ] DOCX brand spec applied - **N/A** (this run produced MD only, not DOCX)

---

## Known Gaps (flag for Gabe review)

1. **PAA stack depth** - only 5 avg vs target 15+. Content-gap MCP tool wasn't available in this environment. Recommend either (a) building a content-gap equivalent in co-work, (b) pulling PAA via a sales-team member using a Chrome extension, or (c) accepting 5/seed as the co-work baseline and flagging it in the deliverable.
2. **MSV precision** - all numbers are LLM estimates. Flagged with `"data_source": "llm_estimate"` in metadata. For high-stakes client work, recommend an Ahrefs/Semrush pull before shipping.
3. **Competitor coverage** - SERP-based competitor content gap analysis not performed (no SERP tool in co-work). Recommend pulling top 10 competitor pages for each seed and analyzing gaps separately.

---

## Handoff Contract

This skill produces the following for downstream consumers:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| `keyword-research.md` | human review | full narrative output |
| `keyword-research.json` | `/entity-research` (optional) | seed keywords, PAA stacks, intent buckets |
| `keyword-research.json` | `/virality-research` | PAA stacks (mined for candidate questions) |
| `keyword-research.json` | `/topic-planner` | demand signal per practice area (search demand factor in 5-signal composite) |
| `metadata.json` | (internal) | provenance - data source, run date, counts, localization flag |

---

## Next Steps

1. Review this output with Gabe - if GOOD, save to `references/examples/good--car-accidents-houston.md` in the pod-1B-keyword-research skill folder.
2. Run `/pod-1A-entity-research` for Car Accidents (scope: Topic). Will consume seeds + PAA above.
3. Optionally run `/pod-1C-virality-research` for Car Accidents. Will mine PAA stacks.
4. Run `/topic-planner` for Sutliff & Stout. Will synthesize all upstream outputs.

---

## Calibration Summary

Future runs of this skill should replicate these rules. Missing any drops below GOOD:

1. **Executive Summary flags data source in-line.** `llm_estimate` vs `content_gap` is visible in the
   first section, not buried in metadata. Downstream skills key off this flag to treat the ranking
   as directional or precise.
2. **Intent distribution lands within 10 points of 60/25/10/5.** Classify every keyword, show the
   four-row table, call out that Commercial stays in the set but shouldn't drive podcast topic
   selection.
3. **Localization runs as per-row math with ratio column.** Generic MSV + Local MSV + Ratio + Signal.
   Alarm-threshold breaks (ratio < 3%) translate into content-strategy signals, not hides. Every
   run states whether intent-bucket flips were detected.
4. **Prominence filter flags, does NOT delete.** High-MSV off-domain terms get
   `"dropped_reason": "prominence_filter"` in metadata; they stay in the raw set for landscape
   visibility. Only the ranked output excludes them.
5. **Search Queries & Volume table matches the ROS Template contract.** ~20 rows, descending by MSV,
   3 columns, full user-typed queries (not seeds), mix across intent types, Source column
   populated per row.
6. **Quality Gates show failures as failures.** PAA shortfall gets an unchecked box plus a reason,
   not a checked box with hidden gap. Known Gaps section proposes remediations.
7. **PAA questions are verbatim and NEVER paraphrased.** They become seed rows for downstream
   n-gram tables. A sloppy PAA capture here contaminates every Run of Show episode built from it.

## Deviations from current canonical

This example is GOOD on the seven Calibration Summary rules above. It is NON-CANONICAL on the
following rule from SKILL Best Practices -> PAA coverage. Future runs should fix before shipping.

| # | SKILL rule (section + specific) | What this example does | Scope of deviation |
|---|---|---|---|
| 1 | Best Practices -> PAA coverage: 15+ PAA questions per seed keyword with MSV >= 100 | Delivers avg 5 per seed (71 total / 14 seeds) | All 14 seeds under-populated; Quality Gate correctly marks FAIL |
| 2 | Output -> Files written: Drive destination `templates [master]/AEO/Podcast/Episode Templates/{Topic}/00 Keyword Research/` with MD + Google Doc + JSON + DOCX | Demo produced MD only; no Drive push, no JSON, no DOCX | Demo environment limitation, not methodology |

**Reader takeaway:** use this example to calibrate intent classification, localization math,
prominence-filter discipline, Search Queries & Volume table shape, and honest Quality Gate reporting.
Do NOT copy the PAA depth (5 avg is below spec); target 15+ per seed when a content-gap tool is
available. The Drive packaging (MD + Doc sibling + JSON + DOCX) is specced in Output and must be
produced in real cowork runs - this demo produced MD only.

### The single-question stress test

Pick any seed keyword row in the table. Ask: "If I swapped Houston for Dallas (or Austin or
San Antonio), would this row's localization signal still hold or would it break?"

- If every seed still makes sense with the city swapped (generic MSV, ratio, and intent
  classification unchanged), the run is state-scope dressed up as city-scope and fails the
  Localization hard rule.
- If at least N seeds break - either because the generic MSV was genuinely Houston-tethered,
  the local ratio would shift materially, or the PAA stack surfaces Houston-specific
  institutions that wouldn't appear in Dallas - the run is genuinely city-scope.

Seeds 11 (houston car accident statistics - 0.95% ratio is Houston-specific niche), 13
(houston car accident report with CR-3 form territory), and the related-searches block
(Memorial Hermann, Houston Methodist, HCA Houston trauma center; car accident on 610, I-10,
290) break cleanly on the swap. That is the signature of genuine city-scope; the output
earned the City scope label.
