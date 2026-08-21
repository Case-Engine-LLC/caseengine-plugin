---
name: pod-2C-virality-research
description: >
  Rescore a candidate question set for virality - take an n-gram table (or seed
  questions from keyword-research / entity-research) and produce a
  virality-optimized rescore against real search behavior and video performance
  data. Five-signal scoring (social trend, community density, YouTube
  engagement, PAA depth, emotional hook) with Koray prominence filter and
  optional localization A/B. Also produces short-form hooks (under 60 chars) for
  Shorts / Reels / TikTok alongside the rephrased podcast questions. Use whenever
  someone says "virality research for [topic]", "score for virality", "optimize
  these questions for search", "viral questions for [episode]", "short-form
  hooks for this episode", or "/pod-2C-virality-research". Research Step 2C of the
  podcast pipeline - OPTIONAL. Runs in tandem with pod-2A-entity-research and
  pod-2B-keyword-research as one in-tandem research pass. The Topic Planner pulls it
  in when present, skips it when absent.
skill_kind: hybrid
modes: multi
inputs: [topic, scope, location, entity-map.json, keyword-research.json, n-gram-table.json, seed-questions]
outputs: [json, markdown, gdoc]
notify: []
metadata:
  version: 3.0.1
  date: 2026-07-10
  owner: Gabe Jordan
  version_history: >
    1.0 - co-work Drive-native version (2026-04-20). 2.0.0 - merged cowork
    canonical content with original local pod-2.75-virality-research
    helper-script flavor (2026-05-14). 3.0.0 - renamed pod-2.75-virality-research
    -> pod-2C-virality-research; full structural refactor to canonical CE skill
    structure; removed skill-folder .env, credentials now pull from 1Password
    (2026-05-20). 3.0.1 - aligned scope/anchor/location language to the canonical
    three-field geo model (Targeting strategy / Optimization scope (show anchor) /
    Episode geo target); localization A/B now keyed to the Episode geo target;
    added anchor-scope-!=-per-episode-target rule; schema gains optional
    targeting_strategy + optimization_scope fields (Gabe directive 2026-07-10,
    Whalen scoping).
---

# Virality Research

> **Drive write governance:** All Drive operations (create, update, rename, move) follow [Ship]. Revise in place via `files.update` against the existing fileId, never delete-and-reupload (breaks the fileId/URL chain and silently kills every downstream reference).

### What is

A virality scoring pass that takes a candidate question set (from an n-gram table, or `keyword-research` PAA stacks, or `entity-research` cluster questions) and rescores each candidate against virality signals - social search trends, Reddit / community discussion density, YouTube video engagement proxies, PAA frequency stacks, and emotional hook. It produces a virality-boosted question set the Topic Planner can optionally layer on top of its standard ranking, plus a short-form hook (under 60 characters) per candidate for Shorts / Reels / TikTok. Output is topic-level and ships to Google Drive as the shared source of truth - markdown source-of-truth, machine-readable JSON sidecar, and human-facing Google Doc. This skill is OPTIONAL - the Research phase runs fine without it; when present, the Topic Planner reads it; when absent, the Topic Planner skips it.

### Workflow

Virality Research is **Step 2C** of **Phase 2 (Research)** of the podcast pipeline, and it is OPTIONAL. The Research phase is LOCKED: `pod-2A-entity-research`, `pod-2B-keyword-research`, and `pod-2C-virality-research` run as ONE in-tandem research pass (Topic Only + Topic+Location scope). This skill rescores the candidate questions 2A and 2B surface; it never invents new topics.

```
PHASE 1: FOUNDATION  (once per client)
┌──────────────────┐
│ pod-1-podcast-bible │  podcast architecture source of truth
└──────────────────┘
        │
PHASE 2: RESEARCH  (one in-tandem pass - Topic Only + Topic+Location)
┌─ 2A ──────────┐ ┌─ 2B ──────────┐ ┌─ 2C ──────────┐
│ Entity        │ │ Keyword       │ │ Virality      │
│ Research      │ │ Research      │ │ Research      │
└───────────────┘ └───────────────┘ └───────────────┘
                                     ◄── YOU ARE HERE
        │
PHASE 3: PLANNING
┌─ 3A ──────────┐ ┌─ 3B ──────────┐
│ Topic Planner │ │ N-Gram Table  │
└───────────────┘ └───────────────┘
        │
PHASE 4: RUN OF SHOW  (per prioritized episode)
┌─ 4A ──────────┐ ┌─ 4B ──────────┐ ┌─ 4C ──────────┐
│ ROS Template  │ │ Client ROS    │ │ Client Guide  │
│               │ │               │ │               │
└───────────────┘ └───────────────┘ └───────────────┘
```

Notes:

- **Phase 1 Foundation** - `pod-1-podcast-bible` runs ONCE per client; it is the architecture source of truth every downstream skill reads.
- **Phase 2 Research** - the three Research skills (2A / 2B / 2C) run together as one research pass. 2C (Virality Research) overlays virality signal onto the candidate questions 2A and 2B surface; it is OPTIONAL. When present, the Topic Planner pulls this skill's scores in; when absent, the Topic Planner runs on 2A and 2B alone.
- **Phase 3 Planning** - `pod-3A-topic-planner` ranks episodes from the research; `pod-3B-n-gram-table` builds the per-episode question framework.
- **Phase 4 Run of Show** - `pod-4A-ros-template`, `pod-4B-client-ros`, and `pod-4C-client-guide` run per prioritized episode.

### Trigger phrases

- `/pod-2C-virality-research`
- "virality research for [topic]"
- "virality pass for [topic]"
- "score for virality [topic]"
- "what podcast topics would go viral for [practice area]"
- "optimize n-gram table for virality"
- "optimize these questions for search"
- "viral questions for [episode]"
- "rephrase questions for search" / "make these questions more searchable"
- "short-form hooks for this episode"
- "how would people actually search for this"

### Greeting

Hi, I'm Virality Research. I'm an OPTIONAL step - if you skip me, the Topic Planner still works; if I run, the Topic Planner pulls in my scores. Before I run, I need to confirm the podcast architecture. If `pod-1-podcast-bible` has been run for this client, I'll read it and confirm in one line. If not, I'll ask:

1. **Client name.** Examples: "The May Firm", "Sutliff & Stout", "Conn Law Firm". Exact firm name as it appears in Drive.

2. **Targeting strategy + Optimization scope (show anchor) - what the podcast as a whole is optimized to rank for.** First, is this a single-location or multi-location firm (does it serve/rank one city, or several)? Then the show anchor:
   - **City-level:** people in your market search the city as a unit ("Houston car accident lawyer"). Anchor: Houston. (Typical single-location anchor.)
   - **State-level:** people search the state as one unit ("California car accident lawyer"). Anchor: California. (Typical multi-location anchor - broad show, a different city per episode.)
   - **County / regional-level:** people search the region ("Inland Empire injury attorney", "Harris County", "Bay Area"). Anchor: the region/county.

3. **Extension locations (if any).** The per-episode **Episode geo targets** - each is the specific city an episode is built to rank for, inheriting from the anchor but surfacing what is different at the smaller scope. "None" if the firm only targets the anchor.

4. **This run's Episode geo target** - the anchor scope, or a specific extension city? (Anchor scope != per-episode target: the show can be optimized for a broad scope while this episode targets one city.)

Then my skill-specific follow-ups:

5. Which topic (practice area)?
6. Source - do keyword-research and entity-research outputs exist in Drive? (I'll read them if yes; I can also run without them, but the results are thinner.)
7. Any seed questions to prioritize scoring for? (or score the entire available set)
8. Refresh in place, or archive and rebuild if a prior virality file exists?

If anything is unclear I'll ask once in a single message. I won't touch Drive until you say go. You only need to know about `{Firm} Podcast/`. I'll handle the foundation lookups and writes transparently.

---

## Best Practices

The WHAT contract. Every other section references these by name; the SOP never restates them.

### Inputs

What is?
The materials this skill ingests - the topic + scope, the candidate question set (from an n-gram table or upstream research), and the podcast architecture doc - all resolved before any scoring runs.

#### Required

- **Topic** - the practice area name (e.g., "Car Accidents").

#### Optional

- **Scope** - one of: Topic, Topic Only, Location, Extension. Defaults to Topic-level.
- **Location** - required when scope is Location or Extension. State-prefixed jurisdictional folder name. Format: `CA`, `CA - Los Angeles County`, `CA - Long Beach`. No colons; dashes only.
- **`n-gram-table.json`** - per-episode 4-column table. When present, every row is a candidate; the N-grams / Entities / Predicates columns are preserved unchanged. Drive at `templates [master]/AEO/Podcast/Episode Templates/{Topic}/{Scope}/03 N-Gram Table/`, or auto-detected locally at `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/03-n-gram/`.
- **`entity-map.json`** - from `pod-2A-entity-research`. Cluster questions and bridge entities seed additional candidates.
- **`keyword-research.json`** - from `pod-2B-keyword-research`. PAA stacks and seed keywords seed additional candidates.
- **Seed questions** - a direct seed list if all upstream outputs are missing.
- **Refresh flag** - default: refresh in place (routes to `## Update`). Pass `archive-and-rebuild` to force a full rebuild with prior content archived to `_archive-{YYYY-MM-DD}/`.

#### Auto-read (no action required)

- **Podcast Show Bible** - architecture source of truth produced by `pod-1-podcast-bible`, resolved via [Podcast Drive](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU). If present, the skill auto-fills Greeting questions 1-3; otherwise it asks.
- **Local virality-research example references** - `references/examples/`. If missing or empty, fall back to in-skill methodology only - do not block.

#### Tools the skill calls

This skill runs locally in Claude Code and calls its tools directly - it assumes they exist and uses them in this priority order. On a tool error, it skips that source and degrades to the next; it never probes for availability first.

- **Bundled `scripts/youtube-virality-fetch.py` + `scripts/reddit-virality-fetch.py`** - for live YouTube Data API + Reddit API signals. API credentials pull from 1Password at runtime via `op read` (`YOUTUBE_API_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`) - never a skill-folder `.env`. If the `op` CLI errors or the vault is locked, mark these signals `skipped` and degrade.
- **Local filesystem read** - for an auto-detected n-gram table at `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/03-n-gram-table/`.
- **`mcp__content-gap__*`** (`get-serp`, `query-fanout`) - for PAA questions and related searches. PAA is the most reliable "how people actually search" signal.
- **`gws drive`** (or `mcp__claude_ai_Google_Drive__*` connector) - for upstream `entity-map.json`, `keyword-research.json`, and the Drive-resident n-gram table.
- **User-supplied materials** in the greeting (pasted seed questions) and LLM domain knowledge for signal inference - the always-available floor.
- **Behavior on a tool error** - skip that source and degrade to the next. When no API path resolves, score on Content Gap MCP + LLM inference and flag every inferred signal transparently in `metadata.json`. The skill never blocks - it is OPTIONAL by design, and degraded virality data is still useful.

### Outputs

What is?
The artifacts this skill ships - the 3-format trio (a machine-readable JSON sidecar, a markdown source-of-truth, and a human-facing Google Doc) plus a `metadata.json` provenance file and optional API appendices - landing in the topic's `Virality Research/{Topic}/{Scope}/` Drive folder, mirrored to the local Desktop path.

#### Output formats

CE-wide default: every persistent artifact ships in three formats.

- **JSON** - `virality-research.json` - structured / machine-readable sidecar for downstream programmatic consumption. Carries the scored candidate list with virality_score, tier, emotional hook category, prominence flag, and optional short-form hooks. Schema in `references/schema/virality-research.json`.
- **Markdown** - `Virality Research.md` - local source-of-truth mirror. Side-by-side comparison: original question vs optimized podcast question + short-form hook + rationale, plus the `## INTERNAL` block.
- **Google Doc** - `Virality Research` - human-facing canonical view at the Drive destination below. Created / updated in-place via `files.update` against a stable fileId so the URL never breaks for downstream links. Typeface: Roboto for every text element (body, headings, table cells, captions), applied via `batchUpdate` `updateTextStyle` with `weightedFontFamily.fontFamily = "Roboto"` over the full document range as the final pass before sharing. Override only when a per-client `brand.json` typography block specifies otherwise.

A `metadata.json` provenance file ships alongside the trio (internal-only, not a client-facing artifact). Optional API appendices (`appendix-youtube.md`, `appendix-reddit.md`, `appendix-paa.md`) ship when the API path ran.

#### What ships

- **`virality-research.json`** - JSON - machine-readable, downstream-consumed; scored candidate list with virality_score, tier (High/Medium/Low), emotional hook category, prominence flag, optional short-form hooks.
- **`Virality Research.md`** - Markdown - local source-of-truth mirror, retains the `## INTERNAL` block.
- **`Virality Research`** - Google Doc - human-facing canonical view, Roboto typeface, stable fileId.
- **`metadata.json`** - JSON (internal) - provenance: run date, scope, source_priority, API status, n-gram-table source, references status, tier distribution.
- **`appendix-{youtube,reddit,paa}.md`** - Markdown (optional) - supporting API data when the API path ran.

#### Drive destination

Shared drive root: `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`). The `templates [master]/AEO/Podcast/Virality Research/` folder id is `1ZCLgror4sf3Z8I8jv8ahZTHkOLa4denz`.

Virality Research lives in its own dedicated `Virality Research/` folder under `templates [master]/AEO/Podcast/`, parallel to `Entity Research/` and `Keyword Research/`. Each topic gets one folder (`{Topic}/`), with all scope variants as parallel subfolders inside. This location is enforced by the **Canonical destination gate** (Best Practices -> Quality gates) - the artifacts never live in a client/firm episode delivery folder, and no caller arg or workflow instruction can redirect them.

```
templates [master]/AEO/Podcast/Virality Research/{Topic}/{Scope}/
  Virality Research.md                    source of truth (markdown)
  Virality Research                       Google Doc (in-place files.update)
  virality-research.json                  machine-readable, downstream-consumed
  metadata.json                           sources, date, scope, tier distribution
  appendix-{youtube,reddit,paa}.md         (optional, when the API path ran)
  _archive-{YYYY-MM-DD}/                  (if this folder had prior content)
```

The `{Scope}` segment resolves per scope:

| Scope | When | `{Scope}` path segment |
|---|---|---|
| **Topic** | Foundation rescore for the whole practice area | (files write directly into `{Topic}/`) |
| **Topic Only** | Generic episode with no jurisdiction | `Topic Only/` |
| **Location** | Full-length episode for a specific state / county / city | `Locations/{Location}/` |
| **Extension** | Short-form derivative for a sub-market | `Extensions/{Location}/` |

Location naming matches exactly, no colons, dashes only: `CA`, `CA - Los Angeles County`, `CA - Long Beach`. The Drive destination is fixed - this skill does not move existing Drive data.

#### Local mirror

`~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/04-virality/` - holds the same `Virality Research.md`, `virality-research.json`, `metadata.json`, and any `appendix-{youtube,reddit,paa}.md`. `{topic-slug}` = slugified practice area (e.g., `car-accidents`); `{episode-slug}` = slugified scope label (e.g., `topic-only`, `ca-long-beach`, `long-beach-extension`). The mirror enables fast local iteration, downstream local skill consumption, and offline review. Written on every run.

#### Schema

`references/schema/virality-research.json` - the canonical JSON schema `virality-research.json` validates against. Required fields: `candidates` array (each with original question, optimized podcast question, short-form hook, 5 signal scores, virality_score, tier, emotional hook category, prominence flag, rationale), `source_priority`, `provenance` block. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed - do not block on a missing schema.

#### Sections INCLUDED in the client-facing artifact

- Cover page (CE logo, title `Virality Research`, subtitle = topic, scope line, "Prepared by Case Engine")
- Executive Summary (total scored items, tier distribution, source-priority flag, localization status)
- High-tier Virality Candidates (leads the body)
- Medium-tier Virality Candidates
- Signal Breakdown per Candidate (5 signal scores + emotional hook + prominence flag)
- Localization Summary (if scope is Location/Extension)

#### Sections EXCLUDED (internal-only)

- `## Quality Assurance` and everything from that heading onward
- `## INTERNAL` (Known Gaps, Handoff Contract, reference material, provenance)

Any Google Doc renderer MUST truncate the markdown source at the first `## Quality Assurance` heading (or `## INTERNAL`, whichever appears first) and discard everything after, so internal-process-and-QA content stays out of the client-facing deliverable while the same markdown serves as the internal source of truth.

#### Write destinations

Both destinations are written every run. On a write error to one, the skill ships to the other and surfaces the partial state in the report - it does not silently lose the deliverable.

- **Drive** - `gws drive` (or `mcp__claude_ai_Google_Drive__*` connector) - writes the markdown, the Google Doc, the JSON, metadata, and appendices into the `Virality Research/{Topic}/{Scope}/` Drive folder.
- **Local mirror** - local filesystem write to the local mirror path, alongside the Drive write.
- **Behavior on a write error** - if one destination errors, ship to the other and report the partial state. If both error, hard-fail with a clear message; do not silently lose the deliverable.

#### Examples

`references/examples/` - GOOD / BAD / EDGE CASE labeled anchor runs. Read 1-2 examples matching the requested scope as calibration before generating. If the folder is empty, proceed on the `## INTERNAL` reference set alone and flag `"references": "empty"` in `metadata.json`.

#### Routing

- **Upstream (optional, any of these):** `pod-2A-entity-research`, `pod-2B-keyword-research`, or an n-gram table. The skill runs on LLM-seed questions alone if all upstream is missing. The three Research-pass skills (2A / 2B / 2C) run in tandem.
- **Downstream:** the Topic Planner pulls the tier-to-boost mapping (+0.10 / +0.05 / 0) to rerank episodes; Run of Show can optionally pull short-form hooks + rephrased questions when present (downstream numbering pending).
- **Prereq (not a workflow step):** `pod-1-podcast-bible` runs once per firm - helpful for audience context but not required.
- **Refresh:** re-run with the same topic + scope (routes to `## Update`).

#### Handoff Contract

This skill produces the following for downstream consumers:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| `virality-research.json` | Topic Planner, optionally Run of Show | Scored candidate list with virality_score, tier (High/Medium/Low), emotional hook category, prominence flag, optional short-form hooks; the Topic Planner reads the tier-to-boost mapping (+0.10 / +0.05 / 0) |
| `metadata.json` | (not consumed downstream) | Internal provenance - run date, scope, tier distribution, source_priority flag, references status, API status |
| `Virality Research` / `Virality Research.md` | human-only, not machine-consumed | Side-by-side comparison + rationale; client-facing review artifact |

Downstream consumers can rely on: the Google Doc URL is stable for the lifetime of the file (preserved via `files.update` across re-runs); `virality-research.json` validates against `references/schema/virality-research.json`; signal-score math reconciles. Upstream pulls (all optional): `entity-map.json` from `pod-2A-entity-research`, `keyword-research.json` from `pod-2B-keyword-research`, an n-gram table. If all upstream is missing, the skill runs on LLM-seed questions and flags `source_priority: "llm_seed_only"`.

### Framing

Virality Research is a RESCORING pass, not a new topic discovery pass. The skill rescores candidate questions for virality lift; it never invents new ones. If the model catches itself generating original topics, that is keyword research or entity research territory - stop. The output is never narrative prose and never a finished episode script.

### Quality bar

What "good" looks like - the pass / fail intuition.

- 30-80 scored questions / topics. If the upstream input is smaller, score what exists and note the thinness in metadata - do not pad.
- Every scored item has all 5 signal scores; a missing score is a fail, not a zero.
- Scoring formula math reconciles: the sum of weighted signals equals `virality_score` within rounding.
- Tiering distribution sensible - High (>= 0.70), Medium (0.40-0.69), Low (< 0.40); High has at least a few entries, not empty.
- Emotional hook categorized for every item (or explicitly None - never a forced category).
- Prominence filter applied - high-virality off-topic items flagged `prominence_filter: "low"`, never ranked at the top.
- N-gram semantic integrity preserved when consuming an n-gram table - the N-grams / Entities / Predicates columns are NEVER modified; only the Question Text is rephrased.
- Localization A/B ran when scope is Location/Extension.
- Short-form hooks under 60 characters where a strong hook can be derived; null otherwise.
- No em dashes, no banned vocabulary - the Anti-AI Detection scan fires before publish.

### Sourcing discipline

The Confirmed / Inferred / Unknown three-state pattern. Never block, always ship, never silent. The virality file still ships when data is incomplete; gaps surface in `## INTERNAL` or with `> NEEDS VERIFICATION:` blocks.

- **Confirmed** - signal traces to a specific source: live YouTube / Reddit API data, or a Content Gap MCP PAA stack. Ship as-is, no inline marker; the API-status fields in `metadata.json` record the source.
- **Inferred** - a signal LLM-inferred from domain pattern knowledge when no API path was reachable for that signal. Flagged transparently in `metadata.json` (`youtube_api: skipped`, `reddit_api: skipped`, etc.) - the API-status field IS the flag.
- **Unknown / NEEDS CONFIRMATION** - no source AND no defensible inference. Ships with `> NEEDS CONFIRMATION: {what's missing}` block, never silently synthesized.

### Editorial Guidelines

Cross-cutting content rules for the virality scoring. The SOP points back here; the rules live here once.

**Guideline 1 - Score every candidate across all five virality signals.**

- **Social trend strength** - Google Trends last 12 months plus platform-specific momentum. Directional, not precise.
- **Reddit / community discussion density** - relevant subreddits and forum threads: how many active conversations, how recent, how much engagement.
- **YouTube engagement proxies** - view counts combined with engagement rate (likes + comments / views) on close-match videos. Engagement rate matters more than raw views.
- **PAA frequency + depth** - how many related PAA branches exist and how deep the expansion goes.
- **Emotional hook** - outrage, surprise, transformation, fear, hope - categorized. No identifiable hook scores 0 on this signal.
- Formula: `virality_score = (social_trend x 0.20) + (community_density x 0.20) + (youtube_engagement x 0.25) + (paa_depth x 0.15) + (emotional_hook x 0.20)`. Tiers: High >= 0.70, Medium 0.40-0.69, Low < 0.40.
- **Where it fires in the SOP:** `## Create -> ### Score the five signals`.

**Guideline 2 - Virality without prominence is clickbait (Koray).**

- Drop questions that score high for virality but are off-topic for the practice area. Clickbait does not convert for legal podcasts.
- Flag with `prominence_filter: "low"` rather than deleting - downstream may want the full landscape - but never rank a low-prominence item at the top.
- **Where it fires in the SOP:** `## Create -> ### Apply prominence filter`.

**Guideline 3 - N-gram semantic integrity is non-negotiable.**

- When the candidate set came from `n-gram-table.json`, the optimized question MUST preserve every entity, n-gram, and predicate the original row required. The N-grams / Entities / Predicates columns are NEVER modified - only the Question Text gets a virality-optimized rephrase.
- If a rephrase would lose an entity, keep the original and flag `kept_original: entity_preservation` in the rationale. N-gram tables exist to ground episode questions in topical authority; rephrasing for virality can sharpen a question but cannot strip its semantic load.
- **Where it fires in the SOP:** `## Create -> ### Generate optimized question + hook`.

**Guideline 4 - Use the HIGHER score in a localization A/B, keyed to the Episode geo target.**

- The "location" in a localization A/B is the **Episode geo target** - the specific city this episode is built to rank for - not the **Optimization scope (show anchor)**, which is the show-wide breadth (City / State / County / Regional). **Anchor scope != per-episode target:** the show can be optimized for a broad scope (e.g. the whole state) while each episode targets a specific city. Research runs at the anchor breadth; each episode's localization test emphasizes that episode's target city.
- When scope is Location or Extension, run the same scoring twice - once generic, once with the Episode geo target modifier. Use the HIGHER of the two scores.
- Local versions of trending national topics often outperform generic ones (local outrage, local stats, local jurisdictions).
- City emphasis is a ceiling, never a forced quota - apply localization only where the target city genuinely lifts the score, never force-fed into every candidate (see no-city-quota / natural-tonality). Getting this wrong is how a multi-location statewide firm ends up with episodes that all sound like one city, or how city emphasis silently becomes a city floor.
- **Where it fires in the SOP:** `## Create -> ### Apply localization A/B`.

### Quality gates

Mechanical pass / fail conditions checked in `## Quality Assurance`.

- **All 5 signal scores** - every scored item has all five.
- **Formula math** - sum of weighted signals equals `virality_score` within rounding.
- **Output count** - 30-80 scored items; thinness noted in metadata when upstream is smaller, never padded.
- **Tiering distribution** - High has at least a few entries; not empty.
- **Source flagged** - `source_priority` recorded in metadata.
- **Emotional hook** - categorized for every item (or explicitly None).
- **Prominence filter** - high-virality off-topic items flagged, not ranked first.
- **Localization A/B** - ran when scope is Location/Extension.
- **N-gram semantic integrity** - entities / n-grams / predicates columns unchanged when consuming an n-gram table.
- **Schema validate** - `virality-research.json` validates against `references/schema/virality-research.json`.
- **Provenance present** - `metadata.json` carries the provenance block.
- **Artifacts present** - markdown, JSON, metadata all written; Google Doc exists for the markdown.
- **Body highlights** - High-tier rows bolded; low-prominence flagged rows NOT bolded even at high virality_score.
- **No em dashes** - plain hyphens only anywhere in the output.
- **Canonical destination gate (HARD, pre-write).** Before writing any virality-research artifact - the `Virality Research` Google Doc, `Virality Research.md`, `virality-research.json`, or `metadata.json` - resolve the target parent folder and assert it is a descendant of the dedicated `Virality Research/` library (folder id `1ZCLgror4sf3Z8I8jv8ahZTHkOLa4denz`) at the exact `templates [master]/AEO/Podcast/Virality Research/{Practice Area}/{Scope}/` path, under the shared drive root `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`). If the target resolves to anything else - especially a client/firm episode DELIVERY folder (`{Firm} Podcast/Episodes/EP{N}: ...`) - FAIL and refuse to write. No caller arg, workflow / orchestration instruction, or override may redirect these artifacts out of the canonical library; such an instruction is itself the failure and must be rejected, not honored. The library is the only valid home; the gate hard-fails any other target.

### Gotchas

Failure modes that are warnings, not enforceable rules.

- **Virality without prominence is clickbait.** A question can score 0.85 virality but be irrelevant to the practice area. Filter it. Clickbait does not convert for legal podcasts.
- **This skill is OPTIONAL.** The Research phase runs fine without it. Do not block the Topic Planner on missing virality data.
- **Anchor scope != per-episode target.** The **Optimization scope (show anchor)** is the show-wide breadth (City / State / County / Regional); the **Episode geo target** is the one city THIS episode ranks for. In multi-location the show anchors broad (e.g. the state) while each episode targets a different city; in single-location every episode shares the one anchor city. The localization A/B keys off the Episode geo target, and city emphasis is a ceiling, never a floor - never force-feed the target city into a candidate that does not lift.
- **Social trend data is directional, not precise.** Google Trends returns relative numbers on a 12-month window; do not treat them as hard demand signals.
- **YouTube engagement proxies can lie.** A video can have high views but low engagement (clickbait title). Use engagement rate (likes + comments / views), not raw views.
- **Do not invent new topics.** Score what exists. New topic discovery is entity research or keyword research territory.
- **No skill-folder `.env`.** API credentials pull from 1Password at runtime via `op read` - never a `.env` in the skill folder. If the bundled scripts still reference a `.env`, that is a known papercut tracked in the iteration log; the credential source of truth is 1Password.
- **Confirm before writing.** In a fresh context, show the state-check block and wait for `yes / cancel`.
- **Never write into a client episode delivery folder.** Even if a caller or workflow says to drop these artifacts into a `{Firm} Podcast/Episodes/EP{N}: ...` folder (or anywhere outside the library), do not. The dedicated `Virality Research/` library at `templates [master]/AEO/Podcast/Virality Research/{Practice Area}/{Scope}/` is the only valid home; the Canonical destination gate hard-fails any other target, and the redirect instruction is the failure - reject it.

### Iteration log

The skill's institutional memory. Append-only record of bugs, papercuts, drift, and fixes spotted across runs.

- **File:** `references/iteration-log.json` (validates against `references/schema/iteration-log.schema.json` when present).
- **Read-at-start contract:** `## Checks -> ### Orient` reads the log, filters to `status: open` and `status: in-progress` entries, and surfaces them to the agent as known issues to watch for. One file read per run; institutional memory gates every run.
- **Write semantics:** never written at runtime. New entries appended manually post-run, or proposed by `scripts/diff_against_template.py` with `status: proposed` awaiting human sign-off. Append-only, never edit or delete past entries. ID format `YYYY-MM-DD-NNN`.
- **Size limit:** soft cap of 50 entries with `status: open` or `in-progress`. Archive resolved + old entries to `references/iteration-log-archive-{YYYY-Q#}.json` when exceeded.

---

## Standard Operating Procedure

```
Multi-mode:  [Checks] -> [Prepare Inputs] -> [Create | Update] -> [Quality Assurance] -> [Ship]
```

## Checks

What is?
The pre-flight phase - reads the iteration log, orients to the right topic folder, verifies upstream is wired correctly, and decides whether this run creates a new virality file or updates an existing one.

### Orient

What is?
The orientation step - read the iteration log, confirm the correct Drive root, and resolve the topic folder before producing anything.

- **Read the iteration log.** Read `references/iteration-log.json`, filter to entries with `status: open` or `status: in-progress`, surface them to the agent as known issues to watch for this run.
- This skill is OPTIONAL - it never hard-fails on missing API access. If no API path resolves, score on Content Gap MCP + LLM inference and flag the degradation in `metadata.json`.
- If the Show Bible is reachable, read it and auto-fill Greeting questions 1-3; confirm in one line. Otherwise ask the Greeting questions.
- Resolve the topic folder under `templates [master]/AEO/Podcast/Virality Research/{Topic}/`. If it does not exist, create per the Podcast Drive convention; if it exists but does not follow the convention, rename. The podcast root is `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`).
- Read `references/examples/` and pick 1-2 examples matching the requested scope as quality anchors. If empty, proceed on the `## INTERNAL` reference set and flag `"references": "empty"` in `metadata.json`.

### Verify upstream

What is?
The handoff-contract gate - confirm upstream artifacts are wired correctly before consuming them, without blocking (this skill is OPTIONAL).

- Resolve `n-gram-table.json` (Drive or local), `entity-map.json` (from `pod-2A-entity-research`), and `keyword-research.json` (from `pod-2B-keyword-research`) against the declared Inputs paths and JSON shapes.
- **Handoff Contract check.** If a new upstream format or path shows up that the Inputs contract does not declare, STOP and ask: "I see upstream output at {path} but my Inputs contract does not declare it. Should I (a) mine it with my best guess, (b) skip it, or (c) pause while you update the handoff contract?" Do not guess silently.
- If all upstream is missing, the skill still runs on LLM-seed questions; flag `source_priority: "llm_seed_only"` in metadata.

### Existence check

What is?
The mode router - decide whether this run creates a new virality file or updates an existing one based on whether `Virality Research/{Topic}/{Scope}/` already has content.

- Look for a `Virality Research` Google Doc + `virality-research.json` inside the resolved scope folder.
- **Missing:** no prior artifact - route to `## Create`.
- **Found:** surface provenance (existing `metadata.json` run date, scored count) and ask: refresh in place / archive-and-rebuild / cancel.
  - Refresh in place - route to `## Update`.
  - `archive-and-rebuild` (or the refresh flag passed at invocation) - move prior content to `_archive-{YYYY-MM-DD}/` and route to `## Create`.

## Prepare Inputs

What is?
The input-preparation phase - loads the candidate question set, the YouTube / Reddit API signals, the Content Gap MCP PAA data, and any upstream research into a working set ready for the Create or Update phase.

Work through the input sources in priority order; on a tool error, skip that source and degrade to the next.

- **YouTube Data API fetch.** Load `YOUTUBE_API_KEY` from 1Password via `op read` and run `scripts/youtube-virality-fetch.py` with 3-5 topic-level queries (NOT per-question - `search.list` costs 100 units per call against a 10K daily quota). Extract top-performing video titles, title patterns, high-coverage subtopics, average engagement rate by title format. If the credential read errors or the call fails, mark `youtube_api: skipped` and degrade.
- **Reddit API fetch.** Look up subreddits from `references/subreddit-map.json` using the industry, load `REDDIT_CLIENT_ID` + `REDDIT_CLIENT_SECRET` from 1Password via `op read`, and run `scripts/reddit-virality-fetch.py`. Extract how real people phrase questions, pain points, language patterns, high-discussion subtopics. Politeness delays are handled by the bundled script. If the credential read errors, mark `reddit_api: skipped` and continue.
- **Content Gap MCP.** Call `mcp__content-gap__get-serp` with 2-3 core n-grams for PAA questions + related searches, and `mcp__content-gap__query-fanout` for query expansion. PAA is the most reliable "how people actually search" signal. On an error, mark `content_gap_mcp: unreachable` and proceed on the remaining signals.
- **Read upstream artifacts.** Mine in source-priority order: (1) `n-gram-table.json` - every row a candidate, the 4-column semantics preserved; (2) `entity-map.json` - cluster questions + bridge entities; (3) `keyword-research.json` - PAA stacks + seed keywords; (4) LLM seed questions only if all upstream is missing. Flag `source_priority` in metadata: `keyword_research+entity_research`, `keyword_research_only`, `entity_research_only`, `n_gram_table_only`, or `llm_seed_only`.
- **Load calibration examples.** Hold the 1-2 scope-matched examples from `references/examples/` as quality anchors for the Create phase.

## Create

What is?
The create branch - builds the virality-scored question set from scratch when no prior file exists, producing a scored, tiered, prominence-filtered, schema-valid `virality-research.json` plus its markdown and metadata.

**Best Practices.**
These apply to the entire create phase and should be checked after each step.

- Virality Research is a rescoring pass, not a topic discovery pass - score what exists, never invent new topics (Framing).
- Hold the scope-matched calibration examples in view while generating - calibrate scored count and tier shape against them.
- Every signal is mandatory - a missing score is a fail, not a zero (Editorial Guideline 1).
- Output count and tier thresholds follow `### Quality bar` and `### Quality gates` - do not restate the thresholds, apply them.

If the model generates output that violates any of these, emit a `> NEEDS VERIFICATION:` block at the offending location instead of shipping the claim.

### Surface candidates

What is?
The pass that assembles the candidate question set - 30-80 questions pulled from the n-gram table, upstream research, or LLM seed, in source-priority order.

- Pull every row from the n-gram table if present; else mine entity-research cluster questions + keyword-research PAA stacks; else LLM seed.
- Target 30-80 scored items per Editorial Guideline 1 and `### Quality bar`. If the upstream input is smaller, score what exists and note the thinness in metadata - do not pad.

### Score the five signals

What is?
The pass that scores each candidate across the five virality signals and computes the composite score.

- Score each candidate on `social_trend`, `community_density`, `youtube_engagement`, `paa_depth`, `emotional_hook` (0.0-1.0 each) per Editorial Guideline 1.
  - With YouTube + Reddit data: use engagement rates and discussion density as direct evidence.
  - With Content Gap MCP only: lean on PAA depth + LLM inference for the other signals.
  - LLM-only: all signals inferred from domain pattern knowledge; flag transparently in metadata.
- Compute composite: `virality_score = (social_trend x 0.20) + (community_density x 0.20) + (youtube_engagement x 0.25) + (paa_depth x 0.15) + (emotional_hook x 0.20)`.
- Categorize each candidate's dominant emotional hook - Outrage / Surprise / Transformation / Fear / Hope - or None when no identifiable hook (do not force a category).

### Apply prominence filter

What is?
The pass that flags high-virality candidates that are off-topic for the practice area.

- Per Editorial Guideline 2, scan high-virality candidates for off-topic content; flag (do not delete) with `prominence_filter: "low"`.
- Never rank a low-prominence item at the top - clickbait does not convert for legal podcasts.

### Apply tiering

What is?
The pass that assigns each candidate a virality tier for the Topic Planner's boost mapping.

- High >= 0.70, Medium 0.40-0.69, Low < 0.40. The Topic Planner boosts composite scores by tier (+0.10 / +0.05 / 0).

### Apply localization A/B

What is?
The pass that runs the scoring twice at Location/Extension scope and keeps the higher score.

- When scope is Location or Extension, run the same scoring twice - once generic, once with the **Episode geo target** modifier (the specific city this episode ranks for, NOT the show anchor breadth) - per Editorial Guideline 4.
- Use the HIGHER of the two scores for each candidate. City emphasis is a ceiling, never a floor - keep the generic score where the target city does not lift. Record the localization-pass result for `metadata.json`.

### Generate optimized question + hook

What is?
The pass that rephrases each prominence-passing candidate into a virality-optimized podcast question and a short-form hook, while preserving n-gram semantic integrity.

- **N-gram semantic integrity:** when the candidate came from an n-gram table, preserve every entity, n-gram, and predicate per Editorial Guideline 3. The N-grams / Entities / Predicates columns are NEVER modified. If a rephrase would lose an entity, keep the original and flag `kept_original: entity_preservation` in the rationale.
- **Podcast question:** rephrased using the highest-engagement patterns while staying conversational for a host. Must still naturally lead to discussing all entities / predicates.
- **Short-form hook:** under 60 characters, punchy, curiosity-driven, drawn from best-performing YouTube title patterns + Reddit post titles. Optional - null if a strong hook cannot be derived.
- **Rationale:** 1-2 sentences citing specific data (YouTube view count, Reddit upvote count, PAA match) explaining the rephrase choice.

### Render markdown

What is?
The pass that assembles the final artifacts - the `Virality Research.md` source-of-truth with cover + executive summary + tiered candidate tables + signal breakdown + the `## INTERNAL` block, the `virality-research.json` sidecar, `metadata.json`, and optional API appendices.

- Assemble `Virality Research.md`: title (H1), executive summary (total scored, tier distribution, source-priority flag, localization status), High-tier candidates (leads the body), Medium-tier candidates, signal breakdown per candidate, localization summary (when scope is Location/Extension), then the `## INTERNAL` block.
- Bold every High-tier candidate row; do NOT bold low-prominence flagged rows even at high virality_score.
- Serialize `virality-research.json` per `### Outputs -> #### Schema`, including the provenance block.
- Write `metadata.json` with the provenance block per `## INTERNAL`. Write optional `appendix-{youtube,reddit,paa}.md` when the API path ran.

## Update

What is?
The update path - modifies an existing Virality Research file in place when a prior version exists, preserving any manual edits the producer made since the last skill run.

**Best Practices.**
These apply to the entire update phase and should be checked after each step.

- **Diff before write.** Pull the existing `virality-research.json` + `Virality Research.md`, compare against the proposed new state, surface every changed candidate before committing the write.
- **Preserve manual edits.** Any signal score, optimized question, short-form hook, or prominence flag that was manually edited since the last skill run keeps its current value. The skill never auto-overwrites a manual edit silently.
- **Flag merge conflicts inline.** When a new auto-generated value disagrees with a preserved manual edit, emit `> NEEDS VERIFICATION: auto-generated value [X] conflicts with manual edit [Y]` at the row; the producer resolves.
- **Stable fileId.** Update uses `files.update` against the existing `Virality Research` Google Doc fileId. Never create a new Doc; never delete-and-recreate.

If the model proposes overwriting a manual edit without flagging it, halt and emit `> NEEDS VERIFICATION:` instead of shipping the change.

### Diff against existing

What is?
The pass that loads the prior virality file and computes a candidate-level diff against the proposed new state so nothing changes silently.

- Read the prior `virality-research.json`, `Virality Research.md`, and `metadata.json` from the resolved scope folder.
- Read the prior `metadata.json` provenance block to recover the last run's source_priority, API status, tier distribution, and references status.
- Run the Create-phase passes (`### Surface candidates` through `### Generate optimized question + hook`) to compute the proposed new state.
- Compute a candidate-level diff: candidates added, removed, re-scored, re-tiered, and untouched.

### Merge and resolve conflicts

What is?
The pass that merges the new content into the existing virality file - new candidates in, stale ones out, manual edits preserved, conflicts flagged for the producer.

- Apply the phase-level Best Practices: preserve every manually-edited score / question / hook / flag; merge new candidates; drop candidates the re-score retired.
- Where a new auto-generated value disagrees with a preserved manual edit, emit the `> NEEDS VERIFICATION:` conflict block inline; do not auto-resolve.
- Re-render `Virality Research.md`, `virality-research.json`, and `metadata.json` per `### Render markdown`. Bump the `metadata.json` run date and append the run to the provenance history.
- The shared `## Quality Assurance` phase runs after this phase - QA does not re-run inside Update.

## Quality Assurance

What is?
The gate before `## Ship` - a three-tier check (Best Practices by name, the hardwired Anti-AI Detection two-pass scan, then skill-specific mechanical checks) that runs after whichever branch fired (`## Create` or `## Update`).

**First - check against Best Practices.** The deliverable must align with the contract defined upstream in this file. This is always the first gate; skill-specific checks come after.

- **Quality bar** (Best Practices -> Quality bar) - 30-80 scored items, all 5 signal scores, formula math reconciles, sensible tier distribution, emotional hook categorized, prominence filter applied, n-gram semantic integrity preserved, localization A/B ran at Location/Extension, short-form hooks under 60 chars, no em dashes / banned vocabulary.
- **Sourcing discipline** (Best Practices -> Sourcing discipline) - every signal traces to API data, Content Gap MCP, or flagged LLM inference via the API-status fields; any belongs-but-missing signal flagged `> NEEDS CONFIRMATION:`. No silent synthesis.
- **Editorial Guidelines** (Best Practices -> Editorial Guidelines) - Guideline 1 (all five signals + formula), Guideline 2 (prominence filter, flag not delete), Guideline 3 (n-gram semantic integrity non-negotiable), Guideline 4 (localization A/B uses the higher score).
- **Quality gates** (Best Practices -> Quality gates) - full checklist must pass: all 5 signal scores, formula math, output count, tiering distribution, source flagged, emotional hook, prominence filter, localization A/B, n-gram semantic integrity, schema validate, provenance present, artifacts present, body highlights, no em dashes.

**Second - Anti-AI Detection two-pass scan** (canonical doc: https://docs.google.com/document/d/1hp7bxOFRlMhCuhjHNY0j05JrB97-KOFD0XUCQM3gMBU/edit). Mandatory for every text-producing skill. Run the full Section 7 two-pass audit against the deliverable:

- **Pass 1 (mechanical scan):** em-dashes, banned vocabulary (Section 2), banned phrases (Section 3), triadic rhythms and symmetric paragraphs (Section 4), summary-only section closers, date formatting per destination, specific-claims-trace-to-source, no numbered lists in ClickUp, no emojis (unless requested), no clickbait in the podcast-question field (the short-form hook field is allowed to be punchy).
- **Pass 2 (skeptical re-read):** restart from the top. Did I actually check every line, or skim? Em-dashes I missed? Banned phrases I rationalized? Triadic rhythms left because they "sounded fine"? An n-gram entity dropped in a rephrase? Am I sure?
- **On any hit:** fix and re-run Pass 2 until clean. One pass is not enough.

**Third - skill-specific mechanical checks.**

- `virality-research.json` validates against the canonical schema `references/schema/virality-research.json`; signal-score math reconciles. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed.
- `metadata.json` provenance block present with at minimum: `run_date`, `scope`, `source_priority`, `youtube_api` (used / skipped / unreachable), `reddit_api` (used / skipped / unreachable), `content_gap_mcp` (used / skipped / unreachable), `n_gram_table` (path or null), `references_status` (used / empty), `schema_status` (validated / missing), `localization_pass` (boolean or null), and tier distribution.
- N-gram semantic integrity: when an n-gram table was consumed, confirm the N-grams / Entities / Predicates columns are byte-identical to the source.
- Both write destinations verified: confirm the Drive `Virality Research/{Topic}/{Scope}/` folder AND the local mirror at `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/04-virality/` contain the same artifacts.
- INTERNAL section grep test: `grep -L "## INTERNAL" {client-facing-export}` returns zero hits for the client-facing Google Doc.

**On failure:** fix the markdown, regenerate `virality-research.json` and `metadata.json`, re-run all checks. Do not proceed to `## Ship` until QA returns clean.

## Ship

What is?
The publish phase - writes the trio plus `metadata.json` and optional API appendices to the topic's `Virality Research/{Topic}/{Scope}/` Drive folder and mirrors the same artifacts to the local Desktop path.

### What ships

- **`Virality Research`** - Google Doc - human-facing canonical view, Roboto typeface, stable fileId.
- **`Virality Research.md`** - Markdown - source-of-truth mirror, retains the `## INTERNAL` block.
- **`virality-research.json`** - JSON - machine-readable, downstream-consumed.
- **`metadata.json`** - JSON (internal) - provenance: run date, scope, tier distribution, source_priority, API status.
- **`appendix-{youtube,reddit,paa}.md`** - Markdown (optional) - supporting API data when the API path ran.

### Where it ships

- **Drive:** `templates [master]/AEO/Podcast/Virality Research/{Topic}/{Scope}/` in the shared drive `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`); `Virality Research/` folder id `1ZCLgror4sf3Z8I8jv8ahZTHkOLa4denz`. The `{Scope}` segment resolves per the table in `### Outputs -> #### Drive destination`. This destination is fixed - the skill does not move existing Drive data.
- **Local mirror:** `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/04-virality/` - written every run.
- **Schema:** `~/.claude/skills/pod-2C-virality-research/references/schema/virality-research.json`.

### How it ships

Write to both destinations. On a write error to one, ship to the other and report the partial state.

- **Drive write.** Upload `Virality Research.md` as `text/markdown`. Create / update the `Virality Research` Google Doc in-place via `files.update` against the existing fileId (on a `## Create` run with no prior Doc, create once and record the fileId). Upload `virality-research.json`, `metadata.json`, and any `appendix-*.md` as binary. Truncate the markdown source at the first `## Quality Assurance` heading before rendering the Google Doc.
- **Roboto pass.** After the base text Doc is uploaded, run a `docs.documents.batchUpdate` with `updateTextStyle` setting `weightedFontFamily.fontFamily = "Roboto"` over the full document range as the final pass before sharing. Override only when a per-client `brand.json` typography block specifies otherwise.
- **Body highlights.** Bold every High-tier candidate row so the viral top picks are immediately visible. Do NOT bold low-prominence flagged rows even at high virality_score (prominence filter wins over score visibility).
- **Cover + footer.** Render the cover page (CE logo top, title `Virality Research`, subtitle = topic, scope line, "Prepared by Case Engine" + date in `Month D, YYYY`). Footer `Case Engine  |  Confidential  |  Page {PAGE}` auto-applied via the Drive API template.
- **Archive.** If the existence check moved prior content to `_archive-{YYYY-MM-DD}/`, the archive folder ships alongside the new artifacts.
- **Local mirror write.** Write the same `Virality Research.md`, `virality-research.json`, `metadata.json`, and any appendices to the local mirror path. If the Drive write fails but the local write succeeds, surface the partial state in the report - do not silently swallow it.
- **Report back:**

  ```
  Done. Virality Research - {Topic}{ / Location if applicable}.

   Folder: https://drive.google.com/drive/folders/{folder_id}
   Virality Research (Doc): https://docs.google.com/document/d/{doc_id}

  Counts: {N} scored items. High: {h} / Medium: {m} / Low: {l}.
  Source priority: {keyword_research+entity_research | keyword_research_only | entity_research_only | n_gram_table_only | llm_seed_only}.
  Localization: {PASS / n/a}. Sources: youtube_api={used/skipped}, reddit_api={used/skipped}, content_gap_mcp={used/skipped}.

  Next: pod-2A-entity-research and pod-2B-keyword-research run in tandem with this skill. Downstream: Topic Planner folds these scores into the ranking (downstream numbering pending).
  ```

### Who to Notify

`notify: []` - this skill posts no notifications. The producer is informed via the inline report-back above.

---

## INTERNAL (not for client distribution - auto-stripped from all exports; the reference material and worked examples ride into the local markdown only, never into the Drive Doc)

### Five virality signals (reference)

| Signal | Weight | What it measures |
|---|---|---|
| Social trend strength | 0.20 | Google Trends 12-month + platform momentum (directional) |
| Community discussion density | 0.20 | Reddit / forum active conversations, recency, engagement |
| YouTube engagement proxy | 0.25 | Engagement rate (likes + comments / views) on close-match videos |
| PAA frequency + depth | 0.15 | How many PAA branches exist, how deep the expansion goes |
| Emotional hook | 0.20 | Outrage / Surprise / Transformation / Fear / Hope; none scores 0 |

### Emotional hook categories

- **Outrage** - insurance-company villain, cop corruption, systemic unfairness.
- **Surprise** - counterintuitive claim, "you won't believe", hidden rule.
- **Transformation** - before/after case, underdog win, recovery arc.
- **Fear** - missed deadline, lost rights, costly mistake.
- **Hope** - against-all-odds win, little-known remedy, second chance.

One category per question - pick the strongest. A question with no identifiable hook gets 0 on that signal and category None. Do not force a category that is not there.

### Credential source

API credentials pull from 1Password at runtime via `op read` - never a skill-folder `.env`. The bundled scripts (`scripts/youtube-virality-fetch.py`, `scripts/reddit-virality-fetch.py`) accept the keys as environment variables passed by the caller; the caller sources them from 1Password (`YOUTUBE_API_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`). The skill-folder `.env` was removed per the CE no-env-files rule. If the scripts still hardcode a `.env` path internally, that is a tracked papercut in the iteration log - update the scripts to read from caller-passed env vars only.

### YouTube quota discipline

`search.list` costs 100 units per call against a 10K daily quota. Run 3-5 topic-level queries per session, never per-question. The bundled Reddit script handles politeness delays (0.3-0.5s between requests) and the configured User-Agent header.

### Provenance block

`metadata.json` must include a provenance block with at minimum: `run_date`, `scope`, `source_priority`, `youtube_api` (used / skipped / unreachable), `reddit_api` (used / skipped / unreachable), `content_gap_mcp` (used / skipped / unreachable), `n_gram_table` (path or null), `references_status` (used / empty), `schema_status` (validated / missing), `localization_pass` (boolean or null), and tier distribution.

### Source inventory

Records every input the run consumed: the n-gram table path and source (local / Drive / none), the `entity-map.json` and `keyword-research.json` paths when present, the YouTube / Reddit / Content Gap signal status, and the calibration examples used.

---

## Learning & Iteration

- [ ] After each run, note which virality signals correlated with actual podcast performance (downloads, watch time, social share rate), source gaps (did LLM-only runs underperform, by how much), localization-ratio behavior at Location/Extension, emotional-hook distribution skew vs actual engagement lift, and prominence-filter catches. Append GOOD / BAD / EDGE CASE entries to `references/examples/`.
- [ ] Track whether the bundled scripts still reference a `.env` path - if so, fix them to read caller-passed env vars only and close the iteration-log papercut.
- [ ] Watch for runs that ship under 30 scored items because upstream was thin; if it recurs for a topic, note the topic genuinely lacks candidate surface area.

## Change Log

| Date | Change |
|---|---|
| 2026-04-20 | Initial co-work version. Optional Step 3 of Research workflow. 5-signal virality scoring with Koray prominence filter. Drive-native. Topic Planner pulls when present, skips when absent. |
| 2026-04-20 | Promoted Quality gates to H2 after SOP, split into Content + Formatting subsections. Added Handoff Contract. |
| 2026-04-21 | DOCX layer removed. Client-facing artifacts render as Google Docs only. |
| 2026-05-14 | **v2.0.0** - merged cowork v1.0.0 + original local `pod-2.75-virality-research` (helper-script + n-gram-consumer flavor). Dual-mode via runtime capability probe; bundled YouTube + Reddit scripts; n-gram semantic-integrity preservation rule; short-form hook generation. `## Quality Assurance` H2 added. Frontmatter: `name: pod-2.75-virality-research`, `skill_kind: hybrid`. |
| 2026-05-20 | **v3.0.0** - renamed `pod-2.75-virality-research` -> `pod-2C-virality-research` (folder + slug + frontmatter `name`). Full structural refactor to the canonical CE skill structure mirroring `pod-5-n-gram-table` v3.0.0. **Removed the skill-folder `.env`** per the CE no-env-files rule - API credentials (`YOUTUBE_API_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`) now pull from 1Password at runtime via `op read`; bundled scripts read caller-passed env vars only. Frontmatter completed (`skill_kind`, `modes: multi`, `inputs`, `outputs`, `notify`; `version`/`date`/`owner` moved to a `metadata` block; the Inputs table replaced by Required / Optional / Auto-read bullets). Best Practices restructured to the canonical contract H3s (Inputs / Outputs / Framing / Quality bar / Sourcing discipline / Editorial Guidelines / Quality gates / Gotchas / Iteration log); five-signal / scoring-formula / tiering / prominence / localization / emotional-hook methodology relocated into Editorial Guidelines + Quality bar + the deliverable-shaped Create buckets. SOP rebuilt as H2 phase siblings (Checks / Prepare Inputs / Create / Update / Quality Assurance / Ship); `## Capture data` -> `## Prepare Inputs`, `## Score & Optimize` folded into the Create buckets, `## Push to Drive` -> `## Ship`, `## Backfill` folded into `## Update` + `## Ship`. QA rewritten as the canonical three-tier gate with the hardwired Anti-AI Detection two-pass scan and an On-failure recovery line. Old `## Output` folded into Best Practices Outputs + the new `## Ship` phase; all Drive folder IDs and the local mirror path preserved verbatim. `references/schemas/` fixed to `references/schema/`. Owner Gabe Jordan. |
| 2026-05-20 | **Probe-strip pass.** Removed the entire `### Probe environment` H3 and all capability-probing apparatus - this skill runs locally in Claude Code only, calls its tools directly, and skips or fails on a tool error rather than probing first. `#### Capabilities` (Inputs) became `#### Tools the skill calls`; `#### Capabilities` (Outputs) became `#### Write destinations`. All `runtime.capabilities` metadata fields dropped; all "when the FS-write probe succeeds" conditionals removed - local-mirror writes are now unconditional. Iteration-log read-at-start contract repointed to `### Orient`. Local n-gram mirror path corrected to `03-n-gram-table/`. Workflow diagram replaced with the unified 4-phase pipeline diagram (Foundation / Research / Planning / Run of Show). |
| 2026-07-10 | **v3.0.1 - three-field geo model alignment (Gabe Jordan, Whalen scoping).** Aligned all scope/anchor/location language to the canonical three-field geo model: **Targeting strategy** (single-location vs multi-location), **Optimization scope (show anchor)** (City / State / County / Regional show-wide breadth), and **Episode geo target** (the specific city each episode ranks for). Greeting Q2-Q4 reframed to name the three fields; Editorial Guideline 4 + the `### Apply localization A/B` SOP step now key the localization A/B to the Episode geo target (not the show anchor) and restate the ceiling-not-floor rule; added an "Anchor scope != per-episode target" Gotchas bullet. Schema (`references/schema/virality-research.json`) gains optional `targeting_strategy` + `optimization_scope` fields and clarified `location` / `localization` descriptions tying them to the Episode geo target; PATCH bump 3.0.0 -> 3.0.1. Preserved no-city-quota / natural-tonality (city emphasis is a ceiling, never a floor). **To revert:** restore the prior Greeting Q2-Q4, Editorial Guideline 4, localization-A/B SOP step, drop the Gotchas rule, and remove the two optional schema fields. |
| 2026-06-17 | **Canonical destination gate added (Gabe Jordan).** Hard, pre-write gate in Best Practices -> Quality gates: before writing the Virality Research Google Doc, `Virality Research.md`, `virality-research.json`, or `metadata.json`, the target parent must resolve to a descendant of the dedicated `Virality Research/` library (folder id `1ZCLgror4sf3Z8I8jv8ahZTHkOLa4denz`) at the exact `templates [master]/AEO/Podcast/Virality Research/{Practice Area}/{Scope}/` path under root `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`); any other target - especially a client/firm episode delivery folder (`{Firm} Podcast/Episodes/EP{N}: ...`) - hard-fails and refuses to write. No caller arg, workflow, or override may redirect these artifacts out of the library; such an instruction is the failure and is rejected. Added matching cross-reference to `#### Drive destination` and a Gotchas entry. **To revert:** remove the Canonical destination gate bullet from `### Quality gates`, the gate sentence from `#### Drive destination`, and the "Never write into a client episode delivery folder" Gotchas bullet. |
