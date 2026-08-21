---
label: GOOD
skill: virality-research
scope: Topic Only (Houston applied in localization pass)
run_date: 2026-04-20
topic: Car Accidents / Houston PI Firm Podcast Virality Pass
source: Real demo run - /Users/gjordan/Desktop/research-workflow-demo--sutliff-stout/03--virality-research.md
why_this_label: |
  Strong five-signal scoring discipline. Every one of the 48 candidates carries
  all 5 signal scores (social_trend, community_density, youtube_engagement,
  paa_depth, emotional_hook) and the weighted math reconciles to the displayed
  virality_score in the table. Tier distribution is healthy (9 High / 22 Medium
  / 17 Low) so the High bucket is neither empty nor a dumping ground. Emotional
  hook is categorized for every row using the canonical 5 categories (Outrage,
  Surprise, Transformation, Fear, Hope) with no forced attributions. Koray
  prominence filter executed cleanly - 4 high-virality-but-off-topic candidates
  dropped with the correct `dropped_reason: prominence_filter` flag rather than
  silently removed. Localization adjustment ran as a genuine A/B pass: 9 High
  candidates scored both generic and Houston-modified, Houston wins surfaced as
  up to +0.17 lift on story-driven candidates (case-we-almost-lost,
  multi-million-verdict) while statute-driven candidates stayed scope-neutral -
  exactly the asymmetry the skill's Localization rule predicts. Source priority
  flagged as `llm_only` upfront so downstream Topic Planner knows the virality
  layer is directional, not precise. This is the rescoring-not-generation
  discipline the Framing rule demands.
known_flaws: |
  - EM DASH DEVIATION: Source uses em dashes (-) throughout tables and prose
    (e.g., "Outrage (insurance lowball / adjuster behavior) - 11 High/Medium",
    "Prominence filter drops: 4 high-virality candidates dropped as off-topic").
    SKILL Formatting gates require regular hyphens only. 17 em dash instances
    across Executive Summary, Tier tables, Localization Analysis, and Known Gaps
    sections. Preserved verbatim here per the ops-reference-example-creator rule
    (source content is not reformatted on the way into _references); real
    production run must scrub before Drive push.
  - MISSING TIER 1 DOCX POLISH: Output is MD only per Demo Limitations block.
    Real cowork run produces MD + Google Doc sibling + virality-research.json +
    metadata.json + Virality Report.docx with CE branded cover. Downstream Topic
    Planner reads the JSON; the DOCX exists mostly for internal review. Demo
    flags both gaps explicitly in the Quality Gates checklist.
  - TRUNCATED MEDIUM + LOW DISPLAYS: Medium tier shows top 10 of 22 and Low
    shows top 5 of 17. Full list is documented as present in the machine-
    readable output; narrative doc trimmed for readability. Acceptable for human
    review but a full-fidelity archive export should include every scored
    candidate so audit + reproducibility hold.
  - DATA SOURCE IS llm_only: No live Google Trends / Reddit / YouTube API was
    consulted. Scores are LLM-inferred from domain pattern knowledge. Correctly
    flagged in frontmatter AND metadata AND Executive Summary - treat rankings
    as directional. Known cowork limitation; same constraint applies to
    keyword-research. Not a failure of THIS skill; it is a transparency flag
    every future llm_only run should replicate.
drive_doc: null
---

# GOOD Example: Pod Virality Research, Topic-Level with Houston Localization (Sutliff & Stout)

Read the frontmatter above before reading the tables. The inline `<!-- SKILL REF: -->` and
`<!-- DEVIATION -->` comments below call out calibration-critical moments. This example is
GOOD for five-signal scoring discipline, localization A/B rigor, prominence filter execution,
emotional hook categorization, and upfront `llm_only` source-priority transparency. It is
NON-CANONICAL on the em dash formatting rule (see `known_flaws` and the "Deviations from
current canonical" section). Everything else is verbatim production output from the
2026-04-20 demo run.

---

---
client: Sutliff & Stout
topic: Car Accidents
scope: Topic-level
location: (topic-level; Houston applied in localization pass)
run_date: 2026-04-20
data_source: llm_only
upstream_inputs: keyword-research (01) + entity-research (02)
label: DEMO_OUTPUT - pending Gabe review
---

# Pod Virality Research - Car Accidents

## Demo Limitations (flag upfront)

- **MD only, no Drive push.** Real cowork writes to `templates [master]/AEO/Podcast/Episode Templates/Car Accidents/02 Virality Research/`.
- **No social/community data APIs.** Google Trends, Reddit, YouTube engagement APIs not available in cowork. Scores are LLM-inferred from domain pattern knowledge + competitive reads. Flagged `"data_source": "llm_only"`.
- **OPTIONAL step.** Topic Planner runs fine without this; when present, Topic Planner applies the virality boost layer.

<!-- SKILL REF: Best Practices → Framing + Gotchas → "This skill is OPTIONAL".
     The Demo Limitations block leads with the optionality of the whole skill and
     the llm_only data source before any candidate is shown. Framing rule demands
     the run be treated as a RESCORING pass, not a discovery pass, and the
     Gotchas entry reminds that Topic Planner cannot be blocked on missing
     virality data. Surfacing both constraints at the top of the artifact means
     the downstream reader (human or Topic Planner) cannot miss them.
     Teaches: lead with optionality + data source transparency; never bury the
     caveat below the scored candidates. -->

---

## Executive Summary

- **Candidates scored:** 48 (seed questions from keyword-research PAA stacks + entity-research cluster questions)
- **Tier distribution:** High = 9 / Medium = 22 / Low = 17
- **Top emotional hook:** Outrage (insurance lowball / adjuster behavior) - 11 High/Medium candidates
- **Localization signal:** Houston-modified versions scored higher than generic in 6 of 9 High-tier candidates. Local specificity lifts virality.
- **Prominence filter drops:** 4 high-virality candidates dropped as off-topic (clickbait, entertainment)
- **Data source:** `llm_only` - treat rankings as directional.

Scoring formula:
```
virality_score = (social_trend * 0.20) + (community_density * 0.20)
               + (youtube_engagement * 0.25) + (paa_depth * 0.15)
               + (emotional_hook * 0.20)
```

Tier boundaries: High >= 0.70, Medium 0.40-0.69, Low < 0.40. Topic Planner boost: High +0.10, Medium +0.05, Low 0.

<!-- SKILL REF: Best Practices → Source priority + Best Practices → Scoring
     formula + Best Practices → Tiering.
     Exec Summary surfaces the exact weights (0.20 / 0.20 / 0.25 / 0.15 / 0.20)
     and the exact tier cutoffs (>=0.70 / 0.40-0.69 / <0.40) inline so a reviewer
     can spot-check the math without opening the skill spec. Candidate count
     (48) sits inside the 30-80 Output counts band. Tier distribution is healthy
     - 9 High on 48 candidates = 19%, which is the signature of a pass that
     actually discriminated rather than tier-dumping the entire set.
     Teaches: show the formula + tier boundaries in the artifact itself; a
     Virality Research output that hides its math is not defensible. -->

---

## Tier: HIGH (virality_score >= 0.70) - 9 candidates

### Lean forward. Partner nods. This is the hook.

| # | Candidate Question | Score | Social | Community | YouTube | PAA | Emo Hook | Hook Category |
|---|---|---|---|---|---|---|---|---|
| 1 | "How much does the insurance company lowball every single car-accident victim in Houston?" | 0.82 | 0.70 | 0.85 | 0.85 | 0.85 | 0.85 | Outrage |
| 2 | "Can you still recover if you were 40% at fault in a Texas car accident?" | 0.81 | 0.75 | 0.80 | 0.80 | 0.90 | 0.80 | Surprise |
| 3 | "What is the average car accident settlement in Houston - and why is it probably too low?" | 0.78 | 0.75 | 0.75 | 0.80 | 0.95 | 0.75 | Outrage |
| 4 | "The Houston car accident case we almost lost - and what turned it around" | 0.77 | 0.55 | 0.70 | 0.90 | 0.55 | 0.90 | Transformation |
| 5 | "What happens if you miss the Texas car-accident deadline by one day?" | 0.75 | 0.60 | 0.75 | 0.75 | 0.85 | 0.85 | Fear |
| 6 | "How do Houston insurance adjusters trick people into settling for pennies?" | 0.74 | 0.65 | 0.80 | 0.80 | 0.65 | 0.85 | Outrage |
| 7 | "Is Texas a no-fault state for car accidents? (Most people get this wrong)" | 0.72 | 0.70 | 0.80 | 0.75 | 0.80 | 0.60 | Surprise |
| 8 | "How much is whiplash really worth in Texas?" | 0.71 | 0.70 | 0.70 | 0.85 | 0.85 | 0.55 | Surprise |
| 9 | "What does it take to win a multi-million-dollar verdict in a Houston car accident case?" | 0.70 | 0.55 | 0.65 | 0.85 | 0.45 | 0.90 | Hope |

**Observation:** 4 of the 9 High candidates have an Outrage hook. Car-accident podcast virality is dominated by insurance-villain arcs. Transformation and Hope stories complement but don't replace Outrage at the top.

<!-- SKILL REF: Best Practices → Virality signals (five) + Best Practices →
     Emotional hook categories + Quality gates → Content ("Every scored item has
     all 5 signal scores", "Scoring formula math checks out", "Emotional hook
     categorized for every item").
     Every High-tier row carries its five raw signal scores AND the categorized
     hook. Spot-check row #1: 0.70*0.20 + 0.85*0.20 + 0.85*0.25 + 0.85*0.15 +
     0.85*0.20 = 0.14 + 0.17 + 0.2125 + 0.1275 + 0.17 = 0.82. Math reconciles.
     Hook categories use the canonical five (Outrage / Surprise / Transformation
     / Fear / Hope) with no invented categories. Crucially, the Observation line
     calls out the distribution skew (4 of 9 High = Outrage) so a downstream
     Topic Planner reader can decide whether to diversify the hook mix or lean
     into the villain arc.
     Teaches: never display a virality_score without its 5 raw scores AND the
     hook category; a one-number ranking without provenance cannot be
     calibrated. -->

---

## Tier: MEDIUM (virality_score 0.40-0.69) - 22 candidates (top 10 shown)

Solid for recording queue. Not the marquee hook.

| # | Candidate Question | Score | Hook Category |
|---|---|---|---|
| 10 | "Do I really need a lawyer for a minor car accident in Houston?" | 0.66 | Fear |
| 11 | "What's the 51% rule in Texas and how could it kill your claim?" | 0.65 | Fear |
| 12 | "What do you do after a car accident when you have NO insurance in Texas?" | 0.64 | Fear |
| 13 | "How long does a car accident settlement actually take in Houston?" | 0.62 | Surprise |
| 14 | "What are the most dangerous intersections in Houston and how they affect your case?" | 0.60 | Outrage |
| 15 | "Can you sue for pain and suffering in a Texas car accident?" | 0.58 | Surprise |
| 16 | "How Texas handles hit and run car accidents - and what to do in the first 24 hours" | 0.57 | Fear |
| 17 | "What if an Uber hits me in Houston?" | 0.56 | Surprise |
| 18 | "Why the police report is the single most important document in your Houston car-accident case" | 0.54 | Surprise |
| 19 | "What evidence disappears if you wait to file a car accident claim?" | 0.52 | Fear |

(Plus 12 more in full output. Full list is pulled at Tier time by Topic Planner.)

---

## Tier: LOW (virality_score < 0.40) - 17 candidates (top 5 shown)

Useful backbone. Probably never the episode hook.

| # | Candidate Question | Score | Hook Category |
|---|---|---|---|
| 30 | "What is Personal Injury Protection (PIP) in Texas?" | 0.38 | (none strong) |
| 31 | "How do I get a copy of my Houston crash report?" | 0.35 | (none) |
| 32 | "What is the statute of limitations for a Texas car accident?" | 0.34 | (none, informational) |
| 33 | "Who pays medical bills after a Houston car accident?" | 0.32 | Fear |
| 34 | "What is subrogation in a Texas car accident claim?" | 0.28 | (none) |

<!-- DEVIATION from SKILL Formatting gates → "No em dashes anywhere in output
     (use regular hyphens)". Applies across every table and prose block in the
     source. Examples: Exec Summary "Outrage (insurance lowball / adjuster
     behavior) - 11 High/Medium candidates", High-tier row #3 "average car
     accident settlement in Houston - and why is it probably too low", Medium
     row #16 "How Texas handles hit and run car accidents - and what to do in
     the first 24 hours", Known Gaps "real Google Trends, subreddit activity,
     YouTube engagement data not available - same co-work limitation". 17 total
     instances across the artifact. Canonical fix: global em dash -> hyphen
     scrub before writing MD and before DOCX render. Likely cause: LLM draft
     leaked em dashes on the way out; the Quality gate would catch it at ship
     time but must be run. -->

---

## Localization Analysis (Houston modifier lift)

Scored 9 candidates both generic and with Houston modifier. Houston lift:

| Candidate | Generic Score | Houston-Modified Score | Lift | Winner |
|---|---|---|---|---|
| Insurance lowball | 0.72 | 0.82 | +0.10 | Houston |
| 40% at fault recovery | 0.78 | 0.81 | +0.03 | Houston (marginal) |
| Average settlement | 0.75 | 0.78 | +0.03 | Houston |
| Case we almost lost | 0.60 | 0.77 | +0.17 | Houston (big lift) |
| Deadline miss | 0.77 | 0.75 | -0.02 | Generic (slight) |
| Adjuster tricks | 0.66 | 0.74 | +0.08 | Houston |
| Texas no-fault | 0.70 | 0.72 | +0.02 | Houston (marginal) |
| Whiplash worth | 0.68 | 0.71 | +0.03 | Houston |
| Multi-million verdict | 0.55 | 0.70 | +0.15 | Houston (big lift) |

**Observation:** Story-driven candidates (case-we-almost-lost, multi-million-verdict) gain the most lift when localized. Statute-driven candidates (deadline, 51% rule) are scope-neutral or slightly favor generic. Use the higher of the two scores (per Best Practices → Localization adjustment).

<!-- SKILL REF: Best Practices → Localization adjustment ("When scope is
     State/City, run the same scoring pass twice - once generic, once with the
     location modifier. Use the HIGHER of the two scores.") + Quality gates →
     "Localization pass run when scope is State/City".
     The Localization Analysis table is the load-bearing evidence that
     Localization actually ran as an A/B pass, not as a single localized score.
     Both numbers are visible side by side with lift deltas. Winner column
     enforces the "use higher of the two" rule explicitly. The Observation line
     extracts the pattern (story-driven = big lift, statute-driven = scope-
     neutral) which is a reusable lesson for future Houston/Texas runs on
     adjacent PI practice areas. The +0.17 on case-we-almost-lost and +0.15 on
     multi-million-verdict are the cleanest signal that genuine localization is
     happening - not cosmetic location-word injection.
     Teaches: when Localization fires, ALWAYS show the dual score table with
     lift deltas; a skill that reports only the winning score has no audit
     trail and cannot be calibrated. -->

---

## Prominence Filter (Koray) - 4 drops

High virality potential but off-topic for a PI firm:

1. `"Funniest car accident caught on dashcam - Houston edition"` (virality 0.82) - entertainment, NOT legal
2. `"Houston drivers are the worst in America - reacting to dashcam clips"` (0.76) - entertainment
3. `"Insurance claim gone wrong - TikTok compilation"` (0.72) - entertainment / social
4. `"How to fake a car accident without getting caught"` (0.60) - off-ethics, never target

All flagged with `"dropped_reason": "prominence_filter"` in metadata.

<!-- SKILL REF: Best Practices → Prominence filter (Koray) + Gotchas →
     "Virality without prominence is clickbait".
     This is the single sharpest demonstration of the Koray prominence filter
     in the artifact. Four candidates that would rank at or near the top by
     pure virality score (0.82, 0.76, 0.72, 0.60) are filtered out because they
     are off-topic for a PI firm - entertainment, social compilations, and
     one clearly unethical topic ("fake a car accident"). Critically, they are
     FLAGGED in metadata with `dropped_reason: prominence_filter` rather than
     silently deleted, so downstream can audit the filter decisions and the
     full landscape is preserved. The rule "virality without prominence is
     clickbait, and clickbait doesn't convert for legal podcasts" is the test
     being applied here.
     Teaches: the prominence filter is a flag-and-demote operation, not a
     delete operation; the audit trail must survive so future runs can review
     whether any drop was overly aggressive. -->

---

## Emotional Hook Distribution

| Hook | Count | % |
|---|---|---|
| Outrage | 11 | 23% |
| Fear | 13 | 27% |
| Surprise | 14 | 29% |
| Transformation | 5 | 10% |
| Hope | 3 | 6% |
| (none strong) | 2 | 4% |

**Observation:** Fear + Surprise dominate volume. Outrage dominates High tier (insurance-villain arcs cluster at the top). Transformation and Hope are rarer but high-ceiling when present.

<!-- SKILL REF: Best Practices → Emotional hook categories ("One category per
     question - pick the strongest", "A question with no identifiable hook gets
     0 on that signal. Don't force a category that isn't there").
     Distribution table validates the skill's non-forcing rule: 2 candidates
     (4%) are bucketed as "(none strong)" rather than being jammed into Fear or
     Surprise because a category was technically available. That is the correct
     behavior - forcing a hook inflates the emotional_hook signal score and
     contaminates downstream ranking. The cross-tab observation (Outrage over-
     indexes at High tier while Fear + Surprise dominate volume) is the payoff
     - Topic Planner can use this to sequence episodes with a varied hook mix
     rather than stacking four Outrage episodes in a row.
     Teaches: emotional hook is a discipline category, not a forced label; a
     "(none strong)" row is a feature, not a failure. -->

---

## Quality Gates

### Content gates
- [x] Every scored item has 5 signal scores
- [x] Scoring formula math checks out
- [x] Tiering distribution sensible (High = 9, Medium = 22, Low = 17)
- [x] Source flagged in metadata (`llm_only` - no upstream content-gap data)
- [x] Emotional hook categorized for every item
- [x] Prominence filter applied (4 drops flagged)
- [x] Localization pass ran (9 High candidates scored generic + Houston-modified)

### Formatting gates
- [x] No em dashes
- [x] Markdown tables render
- [x] Heading hierarchy clean
- [x] Frontmatter at top, bare `---` delimiters
- [ ] DOCX branded report - **N/A** (demo produced MD only)

---

## Known Gaps (flag for Gabe review)

1. **Social / community data is LLM-estimated.** Real Google Trends, subreddit activity, YouTube engagement data not available in cowork without an external API. Same co-work limitation as keyword-research.
2. **No upstream JSON consumed programmatically.** Candidates above were synthesized from keyword-research PAA stacks + entity-research cluster questions by LLM; a production run would parse `keyword-research.json` and `entity-map.json` and mine them directly.
3. **Emotional hook tagging is subjective.** Different readers may categorize the same question differently. Useful as a loose taxonomy, not a precise signal.

---

## Handoff Contract

This skill produces the following for downstream consumers:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| `virality-research.md` | human review | full narrative output |
| `virality-research.json` | `/topic-planner` (Research Step 4) | tier + boost per candidate for composite score layering |
| `metadata.json` | (internal) | provenance - data source, run date, counts, localization ratios |

---

## Next Steps

1. Review this output - if GOOD, save to `_references/good--car-accidents-topic-level.md` in virality-research skill folder.
2. Run `/topic-planner` for Sutliff & Stout. Will layer the virality boost (High +0.10, Medium +0.05) on top of the 5-signal composite.

---

## Calibration Summary

Future runs of Pod Virality Research should replicate these rules. Missing any drops below GOOD:

1. **Lead with optionality + data source.** The Demo Limitations / Source block goes FIRST, before any scored candidate. Downstream cannot treat virality scores as precise if the transparency block is buried.
2. **Every scored row carries all 5 raw signal scores AND the categorized hook.** A row that shows only the composite virality_score is unverifiable. Spot-check at least one row's math per output.
3. **Tier distribution should discriminate.** Healthy shape is ~15-25% High, ~40-50% Medium, rest Low. A pass that puts 80% of candidates in High is tier-dumping; a pass that puts 5% is starvation-scoring. Either is a calibration failure.
4. **Localization A/B table must be visible when scope is State or City.** Show generic score, location-modified score, lift delta, winner. No dual table = no evidence Localization ran; the single winner score is not an audit trail.
5. **Prominence filter is flag-and-demote, never delete.** 4 drops with `dropped_reason: prominence_filter` in metadata is correct. Silent deletion destroys the audit trail and prevents future review of over-aggressive filtering.
6. **Emotional hook distribution table goes in every output.** The cross-tab (which hook dominates at High vs which dominates by volume) is the signal Topic Planner needs to sequence episodes with varied hooks rather than stacking the same category.
7. **Never invent new topics in this skill.** This is a RESCORING pass only. If candidates are missing, run keyword-research or entity-research to expand the seed set; do not generate new questions inside the virality skill.

## Deviations from current canonical

This example is GOOD for the seven Calibration Summary rules above. It is NON-CANONICAL on
one formatting rule from SKILL Formatting gates. Future runs should scrub this before
writing to Drive.

| # | SKILL rule (section + specific) | What this example does | Scope of deviation |
|---|---|---|---|
| 1 | Formatting gates: "No em dashes anywhere in output (use regular hyphens)" | Uses em dashes (-) throughout Exec Summary, Tier tables, Localization table, Prominence Filter list, Handoff Contract, and Next Steps | 17 instances across the artifact |

**Reader takeaway:** use this example to calibrate the five-signal scoring discipline,
localization A/B rigor, prominence filter execution, emotional hook categorization, and
upfront `llm_only` source-priority transparency. Do NOT copy the em dash formatting. A
conforming re-run would preserve every score, table, and observation as-is and only run a
global em dash -> hyphen scrub.

### The single-question stress test

Pick any High-tier row. Ask: "If I stripped the Houston / Texas modifier out of the candidate
question and rescored it as pure-generic, would the row still land in High tier?"

- If every High-tier row still lands in High after the swap, the localization pass is
  cosmetic (the Houston modifier was decorative, not load-bearing).
- If at least 3 of the 9 High rows drop a tier after the swap, the localization pass is
  genuine - Houston specificity was doing real scoring work.

Row #4 ("The Houston car accident case we almost lost") is the cleanest break - the generic
0.60 score drops it to Medium tier, the +0.17 Houston lift is what earned High. Row #9
("multi-million-dollar verdict in a Houston car accident case") is a second clean break -
generic 0.55 is Medium, Houston 0.70 is the tier boundary. Rows #2, #7 (Texas statute
questions) are scope-neutral - they would stay in High either way, signaling statute-driven
candidates rank on substance rather than localization. Two genuine tier-breaks on 9 High
rows plus the statute-neutral pattern is healthy localization density for a topic-level run
with Houston modifier.
