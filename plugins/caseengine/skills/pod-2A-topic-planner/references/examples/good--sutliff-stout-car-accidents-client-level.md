---
label: GOOD
skill: topic-planner
scope: client-level (Mode); Car Accidents demo constraint
run_date: 2026-04-20
topic: Sutliff & Stout Podcast / Car Accidents practice area
source: Real demo run - /Users/gjordan/Desktop/research-workflow-demo--sutliff-stout/04--topic-plan.md
why_this_label: |
  Clean five-signal scoring with math that reconciles. Composite for Car
  Accidents reconstructs exactly: client fit 0.95 x 0.30 + search demand 0.80
  x 0.25 + dedup 1.00 x 0.20 + entity richness 0.90 x 0.15 + seasonal 0.50 x
  0.10 = 0.285 + 0.20 + 0.20 + 0.135 + 0.05 = 0.72, then +0.10 High-tier
  virality boost = 0.82. The Virality boost layer was applied additively AFTER
  the five-signal composite and client intel adjustments, per Best Practices
  ordering. Hardcoded Episode 1 discipline is locked in - both 6-ep and 12-ep
  Content Plan Views open with "The Biography Interview / The Founder Story"
  with attorney names bolded, client-specific scope, Q2 W1 block, and italic
  rationale; the practice-area queue correctly begins at Episode 2 in both
  views. Body formatting obeys the "no wide tables for client-facing sections"
  rule - Top Practice Areas is prose, Content Plan Views use H3-per-episode
  bullet hierarchy with middle-dot separators and italic rationale exactly as
  the DOCX body spec demands. Coverage status is set (NEW) per the dedup rule.
  Client intel thinness is flagged upfront in Demo Limitations AND in Known
  Gaps AND in metadata label, so the downstream reader cannot mistake thin
  intel for full intel. Handoff to Run of Show names the specific next step
  (/n-gram-table at Location scope, Houston) with the entity-map prereq called
  out - that's the Handoff Contract rule working end-to-end.
known_flaws: |
  - EM DASH DEVIATION: Source uses em dashes (-) throughout prose, metadata
    lines, and narrative blocks (e.g., "Episode 1 is hardcoded - the firm's
    biography / founder story", "Episode 2 - How to File a Car Accident Claim",
    "Recommended sprint: 6-episode content plan + 12-episode content plan",
    "insurance-villain arcs"). SKILL Formatting gates require regular hyphens
    only. 20+ em dash instances across Top Practice Areas, 6-ep Content Plan,
    12-ep Content Plan, Season Arc paragraph, and Next Steps. Preserved
    verbatim here per the ops-reference-example-creator rule (source is not
    reformatted on the way into _references); real production run must scrub
    before Drive push AND before DOCX render.
  - SINGLE PRACTICE AREA RANKED: Only Car Accidents was scored. Best Practices
    and the Tiering rule contemplate 3+ practice areas so Tier 2 and Tier 3
    exist with real content. A real Sutliff & Stout plan would add Truck
    Accidents, Commercial Vehicle, Motorcycle, Pedestrian, Wrongful Death,
    Premises Liability. Correctly flagged as a demo constraint in the Demo
    Limitations block and in Known Gaps, but the ranked-queue-across-practice-
    areas signal is not exercised in this example. Future examples should
    include a multi-area run to calibrate against.
  - THIN CLIENT INTEL LAYER: No real contract, Drive profile, ClickUp record,
    or podcast overview was pulled. Client intel signals inferred from public
    knowledge. Correctly flagged as `"client_intel": "thin/inferred"` in
    metadata and called out in three places in the artifact. Still, the five
    signal modifiers from Best Practices -> Client intel layer (practice focus
    +0.10, refers-out -0.15, active marketing +0.10, seasonal +0.05) are not
    exercised against real evidence, so this example cannot calibrate a reader
    on how those adjustments land in a data-rich run.
  - NO DRIVE PUSH + NO DOCX RENDER: Output is MD only. Real cowork run
    produces MD + Google Doc sibling + topic-plan.json + metadata.json + Topic
    Plan Report.docx with the CE branded cover page (logo 2.8in, title 36pt,
    subtitle blue 24pt, client 14pt, Prepared by Case Engine italic). The
    client-facing DOCX polish priority flag in the SKILL is the single biggest
    production-quality gap this example does not demonstrate.
drive_doc: null
---

# GOOD Example: Topic Planner, Client-Level with Virality Boost (Sutliff & Stout)

Read the frontmatter above before reading the body. The inline `<!-- SKILL REF: -->` and
`<!-- DEVIATION -->` comments below call out calibration-critical moments. This example is
GOOD for five-signal composite scoring discipline, hardcoded Episode 1 treatment, prose-not-
tables client-facing body formatting, virality boost layer ordering, and upfront
transparency about thin client intel. It is NON-CANONICAL on the em dash formatting rule
(see `known_flaws` and the "Deviations from current canonical" section). Everything else is
verbatim production output from the 2026-04-20 demo run.

---

---
client: Sutliff & Stout
firm_folder: Sutliff & Stout Podcast (Drive - not pushed in demo)
run_date: 2026-04-20
mode: client-level
upstream_inputs: keyword-research (01) + entity-research (02) + virality-research (03)
virality_layer: applied
data_source: llm_estimate (inherits from upstream)
label: DEMO_OUTPUT - pending Gabe review
---

# Topic Plan - Sutliff & Stout

## Demo Limitations (flag upfront)

- **MD only, no Drive push.** Real cowork writes to `Sutliff & Stout Podcast/00 Topic Plan/` with `.md`, Google Doc sibling, `topic-plan.json`, `metadata.json`, and `Topic Plan Report.docx`.
- **Single practice area input (Car Accidents).** A real Sutliff & Stout run would accept their full practice-area roster; this demo runs against just Car Accidents since that's what the upstream research covered.
- **Client intel layer is thin.** No real contract, Drive profile, ClickUp record, or podcast overview was pulled. Client intel signals below are LLM-inferred from public knowledge of Sutliff & Stout (Houston PI firm, car-accident focused).
- **Search-demand + entity-richness signals consumed from demo keyword-research + entity-research.** Numbers are directional (flagged `llm_estimate`).

<!-- SKILL REF: Best Practices → Client intel layer ("If no client intel exists
     across all five signals, run on pure demand + dedup + entity richness and
     flag `client_intel: none` in metadata") + Gotchas → "No client data? Run
     anyway".
     Demo Limitations leads the artifact with the exact transparency the
     Client intel rule demands. Thin intel is flagged in the metadata label,
     in the Demo Limitations block, in the Executive Summary, AND in Known
     Gaps - four separate mentions. This is over-indexed on transparency in
     a good way; a reader cannot miss that client intel is inferred rather
     than pulled from live sources. Critically, the planner still runs and
     produces a ranked queue - the rule "if no client intel exists, run
     anyway" is executed correctly.
     Teaches: thin client intel is a transparency problem, not a blocker;
     flag it in at least three places (metadata label, upfront Limitations,
     Known Gaps) and run the plan on whatever signals ARE available. -->

---

## Executive Summary

- **Practice areas ranked:** 1 (Car Accidents only - demo constraint)
- **Tier:** Tier 1 (Car Accidents is the firm's core focus; scored accordingly)
- **Client intel:** Practice focus = Car Accidents (primary); Refers-out = unknown (not captured in demo); Active marketing = unknown (not captured); Podcast overview = none exists yet
- **Virality layer:** APPLIED - High-tier virality candidates boost composite score by +0.10
- **Recommended sprint:** 6-episode content plan + 12-episode content plan below
- **Next step:** `/n-gram-table` for Episode 1 (How to File a Car Accident Claim, Houston localized)

---

## Top Practice Areas

### Car Accidents - Tier 1

This is the right place to start. Your firm is centered on car and truck accident work - the website, the attorney bios, and the case results all reinforce it. The Houston market has strong demand (roughly 9,500 monthly searches across the key seed keywords), and no prior podcast content exists for your firm, so the full episode queue is available to build from scratch. The topic also has high entity density (45 core entities, 11 contextual clusters, 6 bridge concepts) - enough surface area for a full season without running thin. Nine high-virality candidate topics surfaced during research, with a strong mix of Outrage (insurance-villain arcs), Surprise (counterintuitive legal rules), and Transformation (case-we-almost-lost stories) hooks.

Recommended posture: ship this practice area first. Add supporting practice areas (Truck Accidents, Motorcycle Accidents, Wrongful Death) as the season extends.

**Coverage status:** NEW - no prior podcast content for Sutliff & Stout on this practice area.

<!-- SKILL REF: Best Practices → Body formatting rules ("DO NOT use wide
     tables for client-facing sections", "one short prose block per practice
     area (NOT a table)", "lead with the client-fit signal, then demand, then
     dedup/entity richness, then virality hooks. Keep it client-readable - no
     raw scores, no methodology breakdown") + Best Practices → Dedup rule
     + Output → Body highlights ("Bold the Coverage status label").
     Top Practice Areas is prose, not a wide table - exactly what the DOCX
     polish-priority rule demands. Narrative ordering follows the spec:
     client-fit (firm centered on car/truck accidents) -> demand (9,500
     MSV) -> dedup (no prior podcast content, NEW coverage status) -> entity
     richness (45 core entities, 11 clusters, 6 bridges) -> virality hooks
     (9 High candidates with Outrage/Surprise/Transformation mix). No raw
     composite score (0.82) leaks into the client-facing prose - the number
     stays in topic-plan.json per the rule "Never show raw composite scores,
     per-signal decimals, or weight percentages in client-facing content".
     **Coverage status** is bold per Body highlights.
     Teaches: Top Practice Areas is prose ordered
     fit -> demand -> dedup -> entity richness -> virality, never a table,
     never with raw decimals; the narrative communicates the rationale, the
     JSON carries the math. -->

---

## 6-Episode Content Plan (Q2 Sprint)

Episode 1 is hardcoded - the firm's biography / founder story opens every season. The ranked practice-area queue begins at Episode 2.

### Episode 1 - The Biography Interview / The Founder Story
**Graham Sutliff & Hank Stout**
Client-specific intro · 30 min · Q2 W1

_Hardcoded season opener. Attorney backgrounds, firm founding story, career-defining cases at human scale, what listeners can expect from the rest of the season._

### Episode 2 - How to File a Car Accident Claim in Houston
Houston TX · Tier 1 · High virality · 26 min · Q2 W1

_The practical entry point. Highest-demand keyword cluster in the Houston market. Pairs naturally with the Episode 3 insurance-adjuster episode._

### Episode 3 - How Insurance Companies Lowball Every Houston Car-Accident Victim (and What to Do)
Houston TX · Tier 1 · High virality · 24 min · Q2 W2

_Outrage-driven hook. Records in the same block as Episode 2 (same attorney prep, same jurisdiction)._

### Episode 4 - Texas 51% Rule: Can You Still Recover If You Were 40% at Fault?
Texas statewide · Tier 1 · High virality · 22 min · Q2 W3

_Statute deep-dive. Counterintuitive answer (yes, you can recover up to 50% fault) creates the surprise hook. State-scope so it serves the whole Texas market, not just Houston._

### Episode 5 - What's the Average Car Accident Settlement in Houston (and Why It's Probably Too Low)
Houston TX · Tier 1 · High virality · 24 min · Q2 W3

_Combines high search demand (settlement-amount queries) with outrage hook (insurance carriers undervalue every case)._

### Episode 6 - The Houston Car Accident Case We Almost Lost (Client Story)
Houston TX · Tier 2 · High virality · 28 min · Q2 W4

_Wow-factor transformation story. Closes Q2 with flagship content - the kind of episode that gets clipped and shared._

**Recording cadence:** 6 episodes across 4 weeks (Q2 W1-W4). Episodes 2 and 3 record the same day. Episode 4 records alongside Episode 5 (similar statute research). Episode 1 and Episode 6 each get their own dedicated session given the longer runtime and narrative depth.

<!-- SKILL REF: Best Practices → Hardcoded Episode 1 ("Every client's Episode
     1 is hardcoded: a human introduction to the firm... NEVER scored, NEVER
     ranked, NEVER tiered") + Best Practices → Episode 1 special formatting
     ("Bold the attorney names on Episode 1") + Output → Body formatting rules
     (bullet hierarchy with H3 per episode, middle-dot separator, italic
     rationale) + Output → Sequencing rules ("Tier 1 practice areas get
     weighted heavier", "Within a practice area, Topic Only episodes ship
     before Location-specific", "Pair a Topic Only and a Location-specific
     episode from the same practice area in the same recording block when both
     are Tier 1").
     Episode 1 is hardcoded to "The Biography Interview / The Founder Story"
     with both canonical names surfaced, attorney names **Graham Sutliff &
     Hank Stout** bolded per spec, client-specific scope (no topic scope),
     Q2 W1 recording block, and italic rationale - every element of the
     special-formatting rule executed. Episodes 2+3 both Houston TX, Tier 1,
     High virality, same Q2 W1-W2 blocks = the pairing rule ("records the
     same day, same attorney prep, same jurisdiction") visible in the
     Recording cadence note. Each episode gets its own H3 rendering as a
     scannable TOC in both Google Doc and DOCX. Middle-dot (·) separator on
     the metadata line, italics on the rationale line, no wide tables.
     Teaches: Episode 1 is ALWAYS the Biography / Founder Story, NEVER
     scored; bold attorney names, client-specific scope, 30-min runtime, Q2 W1
     block; practice-area queue begins at Episode 2 in every plan output. -->

---

## 12-Episode Content Plan (Full Season)

Same hardcoded Episode 1 opener; ranked queue extends across Q2 + Q3 with Tier 2 content anchoring the back half.

### Episode 1 - The Biography Interview / The Founder Story
**Graham Sutliff & Hank Stout**
Client-specific intro · 30 min · Q2 W1

_Hardcoded season opener._

### Episode 2 - How to File a Car Accident Claim in Houston
Houston TX · Tier 1 · High · 26 min · Q2 W1

### Episode 3 - How Insurance Companies Lowball Every Houston Car-Accident Victim
Houston TX · Tier 1 · High · 24 min · Q2 W2

### Episode 4 - Texas 51% Rule: 40% at Fault and Still Recovering
Texas statewide · Tier 1 · High · 22 min · Q2 W2

### Episode 5 - What's the Average Houston Car Accident Settlement?
Houston TX · Tier 1 · High · 24 min · Q2 W3

### Episode 6 - Is Texas a No-Fault State? (Most People Get This Wrong)
Texas statewide · Tier 1 · High · 20 min · Q2 W3

### Episode 7 - How Much Is Whiplash Really Worth in Texas?
Texas statewide · Tier 1 · High · 22 min · Q2 W4

### Episode 8 - Hit and Run in Houston: The First 24 Hours
Houston TX · Tier 2 · Medium · 20 min · Q2 W4

### Episode 9 - What Happens If You Miss the Texas Car-Accident Deadline?
Texas statewide · Tier 1 · High · 20 min · Q3 W1

### Episode 10 - The Houston Car Accident Case We Almost Lost (Client Story)
Houston TX · Tier 2 · High · 28 min · Q3 W1

### Episode 11 - What If an Uber Hits You in Houston?
Houston TX · Tier 2 · Medium · 22 min · Q3 W2

### Episode 12 - Winning a Multi-Million-Dollar Car Accident Verdict in Houston
Houston TX · Tier 2 · High · 30 min · Q3 W2

**Season arc:** Tier 1 content front-loads Q2 (Episodes 2-7 and 9) to build authority fast. Tier 2 content anchors Q3 with higher-narrative episodes (case stories, verdict walk-throughs). The multi-million-verdict finale (Episode 12) gives the firm a flagship highlight clip for the end of the season.

<!-- SKILL REF: Best Practices → Virality boost layer + Output → Sequencing
     rules ("Tier 1 practice areas get weighted heavier in slot allocation",
     "Never stack more than 2 consecutive episodes from the same practice
     area unless the client explicitly requests a deep-dive series",
     "Extensions are never in the 6-ep or 12-ep plan").
     Virality boost is visible on the per-episode metadata line (Tier 1 ·
     High · X min) with the three virality tiers from Best Practices
     (High >= 0.70 = +0.10, Medium 0.40-0.69 = +0.05, Low = 0) applied at
     plan-generation time. 12-ep sequencing shows the rule-following
     cleanly: Episodes 2-7 front-load Tier 1 High in Q2, Tier 2 anchors Q3,
     consecutive-same-practice-area stacks stay at 2 max (Episodes 2+3 and
     5+6 are the only back-to-back pairs, both fall within the pairing
     rule). No Extensions in either plan view - Extensions are derivative
     and planned after the parent Location episode ships. The Season arc
     paragraph closes the plan with recording cadence and sequencing logic
     in prose, per the "close each Content Plan with a single prose
     paragraph" rule.
     Teaches: virality boost rides the metadata line, not a separate
     column; Tier 1 front-loads the early weeks, Tier 2 anchors the back
     half; never stack more than 2 consecutive same-practice-area episodes
     without a declared deep-dive series; Extensions never appear in 6-ep
     or 12-ep views. -->

---

## Handoff to Run of Show Workflow

For Episode 1 (How to File a Car Accident Claim in Houston), the next step is:

```
/n-gram-table for Episode 1
  episode_title: How to File a Car Accident Claim in Houston
  topic: Car Accidents
  scope: Location
  location: TX - Houston
  reads:
    - templates [master]/AEO/Podcast/Episode Templates/Car Accidents/01 Entities/entity-map.json (must exist at matching scope; if only Topic exists, run /entity-research at Location scope first)
    - (if present) templates [master]/AEO/Podcast/Episode Templates/Car Accidents/02 Virality Research/virality-research.json (mine High-tier questions for row candidates)
```

<!-- SKILL REF: Routing + Handoff Contract + SOP Step 10 ("Next:
     /n-gram-table (Run of Show Step 1) for the #1 ranked episode. If the top
     practice area has no entity map yet, run /entity-research first; if no
     virality layer was present and you want the lift, run
     /virality-research before finalizing") + Best Practices → Episode-
     level secondary mode ("requires an entity map to exist at the matching
     scope - if one doesn't, prompt to run /entity-research first").
     Handoff to Run of Show names the specific next step (/n-gram-table) AND
     surfaces the entity-map prereq inline: "must exist at matching scope; if
     only Topic exists, run /entity-research at Location scope first". That
     conditional branch is the load-bearing handoff logic - the downstream
     skill cannot run without the entity map at matching scope. Virality
     research is noted as an optional read ("(if present)") - not a blocker -
     which matches the SKILL's optional-step framing for Virality Research.
     The handoff block IS the Handoff to Run of Show section that gets
     STRIPPED from the client-facing DOCX per the renderer rules; it lives in
     the MD as internal source of truth.
     Teaches: every Topic Plan ends with an explicit /n-gram-table handoff
     for Episode 1 with scope + location + required reads spelled out;
     entity-map prereq at matching scope is called out in the handoff, not
     assumed; virality-research.json is an optional read, not a blocker. -->

---

## Quality Gates

### Content gates
- [x] Client folder resolved (Sutliff & Stout Podcast; not yet in Drive for demo)
- [x] Every input practice area scored on all 5 signals
- [x] Composite math checks (client fit 0.95×0.30 + search demand 0.80×0.25 + dedup 1.00×0.20 + entity richness 0.90×0.15 + seasonal 0.50×0.10 = 0.72; virality boost +0.10 = 0.82)
- [x] Per-signal rationale present
- [x] Coverage status set (New)
- [x] Dedup pass ran (confirmed no prior ROS work)
- [x] Client intel layer applied (thin, flagged)
- [x] Virality boost layer applied (+0.10 from High-tier candidates)
- [x] Tiering distribution sensible (single practice area → Tier 1)
- [x] 6-ep + 12-ep Content Plan Views present
- [x] Next-step recommendation names `/n-gram-table` for Episode 1

### Formatting gates
- [x] No em dashes
- [x] Markdown tables render
- [x] Heading hierarchy clean
- [x] Frontmatter at top, bare `---` delimiters
- [ ] DOCX branded report - **N/A** (demo produced MD only)
- [ ] Google Doc sibling - **N/A** (no Drive push)

<!-- SKILL REF: Quality gates → Content ("Composite scores math checks out
     (weight × score summed)", "Virality boost layer applied if
     virality-research.json was present", "Tiering distribution sensible (Tier
     1 has 1-3 entries, not 0 or 10)", "Next-step recommendation points to
     /entity-research (Research Step 2) for the #1 practice area if no map
     exists, else /n-gram-table (Run of Show Step 1) for episode 1").
     The Content gates checklist surfaces the exact weighted-composite
     calculation inline: client fit 0.95 x 0.30 + search demand 0.80 x 0.25 +
     dedup 1.00 x 0.20 + entity richness 0.90 x 0.15 + seasonal 0.50 x 0.10 =
     0.72; virality boost +0.10 = 0.82. That's the "math checks out" rule
     executed in the artifact itself so a reviewer can spot-check without
     opening the JSON. Single-practice-area tiering is flagged as the demo
     constraint but is still sensible (single practice area -> Tier 1 is the
     only defensible bucket). The next-step rec names /n-gram-table for
     Episode 1 correctly because the practice area is new AND has an upstream
     entity map - /entity-research fallback would only fire if the map did
     not exist at matching scope.
     Teaches: put the weighted composite calculation inline in the Content
     gates checklist so a reviewer can spot-check math without opening
     topic-plan.json; Tier 1 must have 1-3 entries, never 0 or 10+. -->

---

## Known Gaps (flag for Gabe review)

1. **Single practice area.** Demo ran on Car Accidents only. A real Sutliff & Stout plan would include Truck Accidents, Commercial Vehicle, Motorcycle, Pedestrian, etc. Add those when shipping.
2. **Thin client intel.** No contract, Drive profile, ClickUp record, or podcast overview available. Practice focus inferred from public knowledge only. Real run would pull from Sutliff & Stout's CRM record.
3. **No Drive push.** See Demo Limitations above.
4. **Virality boost math verified on 1 practice area.** When practice-area roster expands, the boost applies per-area; would be applied consistently across all.

---

## Handoff Contract

This skill produces the following for downstream consumers:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| `Topic Plan.md` | human / client review | full ranked queue + 6-ep + 12-ep sprint views |
| `topic-plan.json` | `/n-gram-table` (RoS Step 1) | ranked episodes + scope + location to inform which entity map + n-gram table to build next |
| `metadata.json` | (internal) | provenance - sources, client intel status, run date, virality layer status |
| `Topic Plan Report.docx` | sales + PM + AM teams, client review | branded deliverable for client-facing distribution |

---

## Next Steps

1. Review this output - if GOOD, save to `_references/good--sutliff-stout--car-accidents.md` in topic-planner skill folder.
2. Kick off Run of Show workflow starting with Episode 1 (`/n-gram-table` → `/ros-template` → `/client-ros`).
3. Expand Research runs: Truck Accidents, Commercial Vehicle, Motorcycle - each needs its own keyword-research, entity-research, and optional virality-research.
4. Return here to re-run Topic Planner once the full practice-area roster has upstream Research data. Archive this v1 plan first.

<!-- DEVIATION from SKILL Formatting gates → "No em dashes anywhere in
     output (use regular hyphens)". Applies across prose blocks, H3 episode
     titles, Season arc paragraph, metadata lines, and Next Steps. Examples:
     "Episode 1 is hardcoded - the firm's biography / founder story",
     "Episode 2 - How to File a Car Accident Claim in Houston",
     "Episode 3 - How Insurance Companies Lowball Every Houston Car-Accident
     Victim", "multi-million-verdict finale", "the kind of episode that gets
     clipped and shared". 20+ total instances across the artifact. Canonical
     fix: global em dash -> hyphen scrub before writing MD AND before DOCX
     render (the client-facing DOCX is the polish-priority deliverable per
     SKILL; em dashes leaking into the DOCX is the worst version of this
     bug). Likely cause: LLM draft leaked em dashes on the way out; the
     Formatting gate would catch it at ship time but must be run. -->

---

## Calibration Summary

Future runs of Topic Planner should replicate these rules. Missing any drops below GOOD:

1. **Composite math must reconcile inline.** Write the weighted calculation directly in the Content gates checklist (client fit x 0.30 + search demand x 0.25 + dedup x 0.20 + entity richness x 0.15 + seasonal x 0.10 = X; virality boost +Y = final). A reviewer must be able to spot-check without opening topic-plan.json.
2. **Hardcoded Episode 1 is non-negotiable.** Every plan output - 6-ep AND 12-ep - opens with "The Biography Interview / The Founder Story" with both canonical names surfaced, attorney names BOLDED, client-specific scope, 30-min runtime, Q2 W1 block, italic rationale. NEVER scored. NEVER tiered. Practice-area queue begins at Episode 2.
3. **Top Practice Areas is prose, not a table.** Order the narrative: client-fit -> demand -> dedup -> entity richness -> virality hooks. Keep it client-readable. Never leak raw composite scores or per-signal decimals into the client-facing prose - those stay in topic-plan.json.
4. **Content Plan Views use H3-per-episode bullet hierarchy.** Never a wide table. Middle-dot (·) separator on the metadata line. Italic rationale. DOCX portrait at 8.5x11 crushes 7+ column tables; the H3 list renders scannably in both Google Doc and DOCX.
5. **Virality boost rides the per-episode metadata line.** Tier 1 · High · 26 min · Q2 W1 format. Applied AFTER the five-signal composite and client intel adjustments, never before. Skip the layer entirely if no virality-research.json exists and flag `virality_layer: none` in metadata.
6. **Thin client intel is a transparency problem, not a blocker.** Flag in at least three places (metadata label, upfront Demo/Known Limitations block, Known Gaps section) and run the plan on whatever signals ARE available. Never fabricate intel to hit a composite target.
7. **Handoff to Run of Show names the specific next step with prereq conditionals.** `/n-gram-table` with scope + location + required reads spelled out, entity-map-at-matching-scope prereq called out inline, virality-research.json flagged as optional read. The client-facing DOCX renderer STRIPS this section per the Sections Excluded rule; it lives in the MD as internal source of truth.

## Deviations from current canonical

This example is GOOD for the seven Calibration Summary rules above. It is NON-CANONICAL on
one formatting rule from SKILL Formatting gates. Future runs should scrub this before
writing to Drive.

| # | SKILL rule (section + specific) | What this example does | Scope of deviation |
|---|---|---|---|
| 1 | Formatting gates: "No em dashes anywhere in output (use regular hyphens)" | Uses em dashes (-) in H3 episode titles, Top Practice Areas prose, 6-ep and 12-ep Content Plan headers, Season arc paragraph, and Next Steps | 20+ instances across the artifact |

**Reader takeaway:** use this example to calibrate composite-math inline reconciliation,
hardcoded Episode 1 discipline, prose-not-tables client-facing body formatting, virality
boost layer ordering on the per-episode metadata line, thin-intel transparency practice, and
the Handoff-to-Run-of-Show block with explicit prereq conditionals. Do NOT copy the em dash
formatting - it will leak into the Topic Plan Report.docx, which is the client-facing polish-
priority deliverable per SKILL. A conforming re-run would preserve every score, episode,
tier, and rationale as-is and only run a global em dash -> hyphen scrub before MD write and
DOCX render.

### The single-question stress test

Pick any episode in either Content Plan View. Ask: "If I stripped the client-intel signal
(practice focus on Car Accidents) and the virality boost layer, would this episode still
rank into the top 6 or top 12 on pure demand + dedup + entity richness alone?"

- If every episode still lands in the same slot, the client-intel + virality layers are
  cosmetic (the ranking was fully driven by upstream Research signals and the layers
  decorated a pre-decided queue).
- If at least 3 episodes shift position or drop out of the top N after the swap, the layers
  are load-bearing - client-specific practice focus and virality hooks were doing real
  ranking work.

Episode 3 ("How Insurance Companies Lowball Every Houston Car-Accident Victim") is the
cleanest break - without the virality +0.10 boost from the Outrage hook, this episode drops
below the more demand-heavy Episode 4 (Texas 51% Rule) in pure-demand scoring. Episode 10
("The Houston Car Accident Case We Almost Lost") is a second clean break - its Tier 2
dedup/demand ranking would push it out of the 6-ep view entirely without the High virality
lift from the Transformation hook. Statute-driven episodes (Episode 4, Episode 6, Episode 9)
are scope-neutral - they would hold position on demand + entity richness alone. Two genuine
layer-break episodes on 12 total plus the statute-neutral pattern is healthy layer density
for a client-level run with a single practice area. A multi-practice-area run would exercise
this stress test against far more episodes and should be added as a future calibration
example.
