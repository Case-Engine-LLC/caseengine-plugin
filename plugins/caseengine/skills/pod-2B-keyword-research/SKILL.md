---
name: pod-2B-keyword-research
description: >
  Run the keyword research pass for a podcast topic or practice area -
  150-300 keywords with MSV, keyword difficulty, CPC, intent classification
  (Informational / Commercial / Transactional / Navigational), SERP features,
  and the full PAA stack per seed keyword, plus a ~20-row Search Queries &
  Volume handoff table. Use whenever someone says "keyword research for
  [topic]", "keywords for [practice area]", "demand signals for [topic]",
  "what's the search volume for [topic]", or "/pod-2B-keyword-research". Research
  Step 2B of the podcast pipeline. Runs in tandem with pod-2A-entity-research and
  pod-2C-virality-research as one in-tandem research pass. Feeds the n-gram table,
  topic planner, run of show, and pod-2C-virality-research downstream.
skill_kind: hybrid
modes: multi
inputs: [topic, scope, location, seed-keywords, content-gap-report, podcast-overview.md]
outputs: [json, markdown, gdoc]
notify: []
metadata:
  version: 3.0.0
  date: 2026-05-20
  owner: Gabe Jordan
  version_history: >
    1.0 - co-work Drive-native version (2026-04-20). 2.0.0 - canonical local
    land as pod-2.5-keyword-research with Ahrefs + content-gap auto-detect
    (2026-05-14). 3.0.0 - renamed pod-2.5-keyword-research ->
    pod-2B-keyword-research; full structural refactor to canonical CE skill
    structure (2026-05-20).
---

# Keyword Research

> **Drive write governance:** All Drive operations (create, update, rename, move) follow [Ship]. Revise in place via `files.update` against the existing fileId, never delete-and-reupload (breaks the fileId/URL chain and silently kills every downstream reference).

### What is

A keyword research pass for a topic (and optionally a location) that surfaces the demand signals every downstream podcast skill reads. It produces a ranked keyword set of 150-300 keywords with monthly search volume, keyword difficulty, CPC, intent classification, SERP features, related searches, and the People Also Ask (PAA) stack per seed keyword, plus a ~20-row Search Queries & Volume table that downstream Run of Show consumes verbatim. Output is topic-level, not per-episode. It ships to Google Drive as the shared source of truth - markdown source-of-truth, machine-readable JSON sidecar, and human-facing Google Doc.

### Workflow

Keyword Research is **Step 2B** of **Phase 2 (Research)** of the podcast pipeline. The Research phase is LOCKED: `pod-2A-entity-research`, `pod-2B-keyword-research`, and `pod-2C-virality-research` run as ONE in-tandem research pass (Topic Only + Topic+Location scope). This skill produces the demand vocabulary; 2A maps the entity vocabulary; 2C overlays virality signal.

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
- **Phase 2 Research** - the three Research skills (2A / 2B / 2C) run together as one research pass. 2B (Keyword Research) maps the demand landscape; 2A maps the entity vocabulary; 2C overlays virality signal. Runs ONCE per practice area + location cascade.
- **Phase 3 Planning** - `pod-3A-topic-planner` ranks episodes from the research; `pod-3B-n-gram-table` builds the per-episode question framework.
- **Phase 4 Run of Show** - `pod-4A-ros-template`, `pod-4B-client-ros`, and `pod-4C-client-guide` run per prioritized episode.

### Trigger phrases

- `/pod-2B-keyword-research`
- "keyword research for [topic]"
- "run keyword research for [topic] in [location]"
- "keywords for [practice area]"
- "kw research [topic]"
- "demand signals for [topic]"
- "what's the search volume for [topic]"

### Greeting

Hi, I'm Keyword Research. Before I run, I need to confirm the podcast architecture. If `podcast-overview.md` has been run for this client, I'll read it and confirm in one line. If not, I'll ask:

1. **Client name.** Examples: "The May Firm", "Sutliff & Stout", "Conn Law Firm". Exact firm name as it appears in Drive.

2. **Podcast geo model - two fields up front:**
   - **Targeting strategy - single-location or multi-location?** Does the firm serve/rank one city or several? Single-location anchors every episode on the one city; multi-location anchors the show broad (usually State/Regional) and targets a different city per episode.
   - **Optimization scope (show anchor) - what is the podcast as a whole optimized to rank for?** This governs the overall keyword-research breadth - the keyword pass runs at this scope.
     - **City:** people in your market search the city as a unit ("Houston car accident lawyer"). Anchor: Houston.
     - **State:** people search the state as one unit ("California car accident lawyer"). Anchor: California. Extension cities per office.
     - **County / Regional:** people search the region ("Inland Empire injury attorney", "Harris County", "Bay Area"). Anchor: the region/county. Cities within become extensions.

3. **Episode geo target / extension locations (if any).** The specific city each episode is built to rank for - the Episode geo target. Short derivatives that inherit from the anchor but surface what is different at the smaller scope. Anchor scope is NOT the per-episode target - the show can anchor at the state while each episode targets a different city. "None" if the firm only targets the anchor.

4. **This run's scope** - anchor or a specific extension / episode geo target?

Then my skill-specific follow-ups:

5. Which topic (practice area)?
6. Source preference - content-gap / SERP / Ahrefs data if available, or LLM-inferred from domain knowledge?
7. Any seed keywords or existing keyword set to expand from?
8. Does a prior keyword research file exist - refresh in place or archive and rebuild?

If anything is unclear I'll ask once in a single message. I won't touch Drive until you say go. You only need to know about `{Firm} Podcast/`. I'll handle the foundation lookups and writes transparently.

---

## Best Practices

The WHAT contract. Every other section references these by name; the SOP never restates them.

### Inputs

What is?
The materials this skill ingests - the topic + scope, optional seed keywords, optional content-gap data, and the podcast architecture doc - all resolved before any keyword mining runs.

#### Required

- **Topic** - the practice area name (e.g., "Car Accidents"). No free-text topics; resolves to a practice area folder.

#### Optional

- **Scope** - one of: Topic, Topic Only, Location, Extension. Defaults to Topic-level. Set to Location/Extension when jurisdictional signals matter.
- **Location** - required when scope is Location or Extension. State-prefixed jurisdictional folder name. Format: `CA`, `CA - Los Angeles County`, `CA - Long Beach`. No colons; dashes only.
- **Seed keywords** - an optional seed list to expand from. If absent, the skill expands from the practice area name + known subtopics.
- **Content-gap data** - a content-gap report or SERP / PAA / keyword-volume extract. Auto-detected at `~/Desktop/claude_code/mcps/content-gap-mcp-server-andrew/data/reports/{practice-area-slug}/`, or uploaded to `_inputs/` in the matching scope folder.
- **Refresh flag** - default: refresh in place (routes to `## Update`). Pass `archive-and-rebuild` to force a full rebuild with prior content archived to `_archive-{YYYY-MM-DD}/`.

#### Auto-read (no action required)

- **`podcast-overview.md`** / **Podcast Show Bible** - architecture source of truth produced by `pod-1-podcast-bible`. If present at `{Firm} Podcast/.podcast-overview/podcast-overview.md`, the skill auto-fills Greeting questions 1-3; otherwise it asks.
- **Local keyword-research example references** - `references/examples/`. If missing or empty, fall back to in-skill methodology only - do not block.

#### Tools the skill calls

This skill runs locally in Claude Code and calls its tools directly - it assumes they exist and uses them in this priority order. On a tool error, it skips that source and degrades to the next; it never probes for availability first.

- **Keywords Everywhere API** (PRIMARY search-volume source) - real Google Keyword Planner monthly volume + CPC per keyword (`dataSource=gkp`). Endpoint `POST https://api.keywordseverywhere.com/v1/get_keyword_data`, batched 100 keywords per request, 1 credit per keyword. The reusable lookup helper is `scripts/ke_volume_backfill.py` -> `fetch_ke_volumes(keywords, key)`. The KE API key is NEVER hardcoded - it is resolved at runtime from 1Password via the `mcp__op-broker__read_secret` tool (item `Keywords Everywhere API Key`, `caseengine` account, `Paid` team vault) and passed to the helper as the `KE_API_KEY` env var.
- **`mcp__claude_ai_Ahrefs__*`** (fallback) - real MSV / KD / CPC / SERP-feature data per keyword when Keywords Everywhere is unreachable or for KD / SERP-feature signals KE does not return. Authenticate via `mcp__claude_ai_Ahrefs__authenticate` if it returns unauthenticated.
- **Local filesystem read** - for an auto-detected content-gap report at `~/Desktop/claude_code/mcps/content-gap-mcp-server-andrew/data/reports/{practice-area-slug}/` (`serp-*.json`, `paa-*.json`, `keyword-volume-*.json`).
- **`gws drive`** (or `mcp__claude_ai_Google_Drive__*` connector) - for `_inputs/` content-gap uploads from the shared Drive.
- **`mcp__ce-services__rag_query`** with `rag_name: koray` - for prominence-filter and intent-classification methodology grounding.
- **User-supplied materials** in the greeting (pasted seeds, dropped files) and user interview for hard requirements still missing - the always-available floor.
- **Volume source priority chain** - search volume + CPC resolve in this order: Keywords Everywhere (API, `dataSource=gkp`) -> Ahrefs MCP -> LLM estimate. The first source that returns data for a keyword wins; the chain degrades per keyword, not per run.
- **Behavior on a tool error** - skip that source and degrade to the next per the priority chain. When no real keyword data source resolves (Keywords Everywhere, Ahrefs, content-gap report, `_inputs/` upload), LLM-estimate the metrics and tag every estimated row `data_source: "llm_estimate"`. Per-row provenance is preserved - a single keyword set can mix `keywords_everywhere_gkp`, `ahrefs`, `content-gap`, and `llm_estimate` rows. A Koray RAG error logs `koray_rag: unreachable` and proceeds on in-skill methodology.

### Outputs

What is?
The artifacts this skill ships - the 3-format trio (a machine-readable JSON sidecar, a markdown source-of-truth, and a human-facing Google Doc) plus a `metadata.json` provenance file - landing in the topic's `Keyword Research/{Topic}/{Scope}/` Drive folder, mirrored to the local Desktop path.

#### Output formats

CE-wide default: every persistent artifact ships in three formats.

- **JSON** - `keyword-research.json` - structured / machine-readable sidecar for downstream programmatic consumption. Carries the full keyword set + PAA stacks + intent classifications + per-row `data_source` tags + prominence flags + localization deltas + the `search_queries` array. Schema in `references/schema/keyword-research.json`.
- **Markdown** - `Keyword Research.md` - local source-of-truth mirror. Combined: executive summary + ranked keyword set + PAA stacks + related searches + Search Queries & Volume table + localization summary + the `## INTERNAL` block.
- **Google Doc** - `Keyword Research` - human-facing canonical view at the Drive destination below. Created / updated in-place via `files.update` against a stable fileId so the URL never breaks for downstream links. Typeface: Roboto for every text element (body, headings, table cells, captions), applied via `batchUpdate` `updateTextStyle` with `weightedFontFamily.fontFamily = "Roboto"` over the full document range as the final pass before sharing. Override only when a per-client `brand.json` typography block specifies otherwise.

A `metadata.json` provenance file ships alongside the trio (internal-only, not a client-facing artifact - records sources, counts, intent distribution, localization ratio).

#### What ships

- **`keyword-research.json`** - JSON - machine-readable, downstream-consumed; full keyword set + PAA stacks + intent classifications + per-row `data_source` tags + prominence flags + localization deltas + `search_queries` array.
- **`Keyword Research.md`** - Markdown - local source-of-truth mirror, retains the `## INTERNAL` block.
- **`Keyword Research`** - Google Doc - human-facing canonical view, Roboto typeface, stable fileId.
- **`metadata.json`** - JSON (internal) - provenance: sources, run date, scope, location flag, keyword / seed / PAA / related-search counts, intent distribution, localization ratio, references status.

#### Search Queries & Volume table (required output)

Every run produces a Search Queries & Volume table - the canonical handoff format. Downstream Run of Show reads this shape verbatim for its Appendix.

- **Format:** 3 columns (`Query` | `Monthly Volume` | `Source`), ~20 rows, descending by Monthly Volume.
- Query phrases must be the FULL user-typed query, not the seed keyword (e.g., `california car accident lawyer`, not `car accident lawyer`).
- Mix across intent types: entity-rich, injury-type, specific-incident, damages, bad-faith / insurance denial.
- Source column values: `Ahrefs` / `Semrush` / `SerpAPI` / `content-gap` / `LLM estimate` / `N/A`.
- Rendered as a `### Search Queries & Volume` H3 in the markdown body; serialized to `keyword-research.json` under the `search_queries` key.

#### Drive destination

Shared drive root: `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`). The `templates [master]/AEO/Podcast/Keyword Research/` folder id is `1K6V4AoyjDa7OzY9pNvsc6zPgzW9MR5Nj`.

Keyword Research lives in its own dedicated `Keyword Research/` folder under `templates [master]/AEO/Podcast/`, parallel to `Entity Research/` and `Virality Research/`. Each topic gets one folder (`{Topic}/`), with all scope variants as parallel subfolders inside.

```
templates [master]/AEO/Podcast/Keyword Research/{Topic}/{Scope}/
  Keyword Research.md                     source of truth (markdown)
  Keyword Research                        Google Doc (in-place files.update)
  keyword-research.json                   machine-readable, downstream-consumed
  metadata.json                           sources, date, scope, location flag, counts
  _inputs/                                (optional uploaded content-gap reports)
  _archive-{YYYY-MM-DD}/                  (if this folder had prior content)
```

The `{Scope}` segment resolves per scope:

| Scope | When | `{Scope}` path segment |
|---|---|---|
| **Topic** | Foundation demand pass for the whole practice area | (files write directly into `{Topic}/`) |
| **Topic Only** | Generic episode with no jurisdiction | `Topic Only/` |
| **Location** | Full-length episode for a specific state / county / city | `Locations/{Location}/` |
| **Extension** | Short-form derivative for a sub-market | `Extensions/{Location}/` |

Location naming matches exactly, no colons, dashes only: `CA`, `CA - Los Angeles County`, `CA - Long Beach`. The Drive destination is fixed - this skill does not move existing Drive data. This location is enforced by the **Canonical destination gate** (Best Practices -> Quality gates): the gate hard-fails any write that resolves outside the dedicated `Keyword Research/` library, so these artifacts never live in a client/firm episode delivery folder.

#### Local mirror

`~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/02.5-keywords/` - holds the same `Keyword Research.md`, `keyword-research.json`, `metadata.json`, plus a `gdoc-url.txt` pointer to the converted Google Doc. `{topic-slug}` = slugified practice area (e.g., `car-accidents`); `{episode-slug}` = slugified scope label (e.g., `topic-only`, `ca-long-beach`, `long-beach-extension`). The `02.5-` numeric prefix slots between `01-entities/` and `03-virality/` in the per-episode local deliverables folder. The mirror enables fast local iteration, downstream local skill consumption, and offline review. Written on every run.

#### Schema

`references/schema/keyword-research.json` - the canonical JSON schema `keyword-research.json` validates against. Required fields: `keywords` array (each with `query`, `msv`, `kd`, `cpc`, `intent`, `serp_features`, `data_source`, optional `prominence_filter`), `seed_keywords`, `paa_stacks`, `related_searches`, `search_queries` array (each with `query`, `monthly_volume`, `source`), `localization` block (conditional), `provenance` block. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed - do not block on a missing schema.

#### Sections INCLUDED in the client-facing artifact

- Cover page (CE logo, title `Keyword Research`, subtitle = topic, scope line, "Prepared by Case Engine")
- Executive Summary (keyword count, intent distribution, PAA totals, data source)
- Ranked Keyword Set (by intent bucket)
- PAA Stacks (per seed keyword)
- Related Searches
- Search Queries & Volume table
- Localization Summary (if scope is Location/Extension)

#### Sections EXCLUDED (internal-only)

- `## Quality Assurance` and everything from that heading onward
- `## INTERNAL` (Known Gaps, Handoff Contract, reference material, provenance)

Any Google Doc renderer MUST truncate the markdown source at the first `## Quality Assurance` heading (or `## INTERNAL`, whichever appears first) and discard everything after, so internal-process-and-QA content stays out of the client-facing deliverable while the same markdown serves as the internal source of truth.

#### Write destinations

Both destinations are written every run. On a write error to one, the skill ships to the other and surfaces the partial state in the report - it does not silently lose the deliverable.

- **Drive** - `gws drive` (or `mcp__claude_ai_Google_Drive__*` connector) - writes the markdown, the Google Doc, the JSON, and metadata into the `Keyword Research/{Topic}/{Scope}/` Drive folder.
- **Local mirror** - local filesystem write to the local mirror path, alongside the Drive write.
- **Behavior on a write error** - if one destination errors, ship to the other and report the partial state. If both error, hard-fail with a clear message; do not silently lose the deliverable.

#### Examples

`references/examples/` - GOOD / BAD / EDGE CASE labeled anchor runs. Read 1-2 examples matching the requested scope as calibration before generating. If the folder is empty, proceed on the `## INTERNAL` reference set alone and flag `"references": "empty"` in `metadata.json`.

#### Routing

- **Upstream:** none. Keyword Research is one of the three parallel Research-pass skills (2A / 2B / 2C run in tandem).
- **Downstream:** the N-Gram Table seeds its question framework from PAA stacks; the Topic Planner consumes the demand signals; Run of Show reads the `search_queries` array verbatim for its Appendix; `pod-2C-virality-research` reads PAA stacks as candidate questions (downstream numbering pending).
- **Prereq (not a workflow step):** `pod-1-podcast-bible` runs once per firm - helpful for audience context but not required.
- **Refresh:** re-run with the same topic + scope (routes to `## Update`).

#### Handoff Contract

This skill produces the following for downstream consumers:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| `keyword-research.json` | N-Gram Table, Topic Planner, `pod-2A-entity-research`, `pod-2C-virality-research` | Seed keyword list, PAA stacks (consumed verbatim as n-gram seed rows), intent classification, MSV + KD + CPC + per-row `data_source` tag, prominence flags, localization deltas |
| `keyword-research.json` -> `search_queries` | Run of Show (ROS template Appendix) | Read verbatim for the Appendix `Search Queries & Volume` block - same shape, same ordering, same source values |
| `metadata.json` | (not consumed downstream) | Internal provenance only - sources, run date, scope, localization flag, `data_source`, references status |
| `Keyword Research` / `Keyword Research.md` | human-only, not machine-consumed | n/a |

Downstream consumers can rely on: the Google Doc URL is stable for the lifetime of the file (preserved via `files.update` across re-runs); `keyword-research.json` validates against `references/schema/keyword-research.json`; the `search_queries` array has ~20 rows in the verbatim handoff shape. Upstream pulls: none - Keyword Research is a Research-pass entry point.

### Framing

Keyword research is a DEMAND pass, not a topic-selection pass. The Topic Planner consumes this and decides which practice areas to record. Do not dedup practice areas, do not pick winners, do not prioritize - that is downstream. This skill's job is to surface the full demand landscape for a topic so every downstream skill reads from a clean, ranked keyword set. It is never narrative prose and never a finished content plan.

**Anchor scope != per-episode target.** The show can be optimized for a broad Optimization scope (show anchor) - e.g. the whole state - while each episode targets a specific Episode geo target city it is trying to rank for. This skill pulls MSV / keyword data at the anchor breadth AND per target city: the anchor governs the overall research breadth, while the Episode geo target selects which city's location-variant keywords an episode reads downstream. Each episode's questions and titles emphasize that episode's target city naturally - a ceiling, never a forced quota (see the no-city-quota bullet under Editorial Guideline 4). Getting this wrong is how a multi-location statewide firm ends up with episodes that all read like one city, or how city emphasis silently becomes a city floor.

### Quality bar

What "good" looks like - the pass / fail intuition.

- 150-300 total keywords, 10-20 seed keywords, 50-150 PAA questions, 100-200 related searches.
- Every keyword carries MSV, KD, an intent bucket (Informational / Commercial / Transactional / Navigational), and a per-row `data_source` tag.
- Intent distribution lands near 60% Informational / 25% Commercial / 10% Transactional / 5% Navigational; a skew more than 10 points off is noted in metadata, not silently shipped.
- 15+ PAA questions per seed keyword with MSV >= 100, preserved verbatim.
- Search Queries & Volume table: ~20 rows, full query phrases, descending by Monthly Volume, every row tagged with a source.
- Localization pass ran when scope is Location/Extension - keyword pass run twice (with and without the modifier), deltas compared, intent flips flagged.
- Prominence filter applied - high-MSV terms that do not align with the practice area's semantic core flagged `prominence_filter: "low"`, never removed.
- Dedup ran - stem collapse + synonym collapse.
- No em dashes, no banned vocabulary - the Anti-AI Detection scan fires before publish.

### Sourcing discipline

The Confirmed / Inferred / Unknown three-state pattern. Never block, always ship, never silent. The keyword set still ships when data is incomplete; gaps surface in `## INTERNAL` or with `> NEEDS VERIFICATION:` blocks.

- **Confirmed** - claim traces to a specific source: Keywords Everywhere API volume, Ahrefs MCP data, a content-gap report, or a cached PAA stack. Tagged `data_source: "keywords_everywhere_gkp"`, `"ahrefs"`, or `"content-gap"`; PAA tagged `paa_source: "cached"`. Ship as-is, no inline marker.
- **Inferred** - a sensible LLM estimate applied when no real data source is reachable for that row. Tagged `data_source: "llm_estimate"` (and `paa_source: "llm_inferred"` for inferred PAA). The numbers are directional, not precise - the tag IS the flag.
- **Unknown / NEEDS CONFIRMATION** - no source AND no defensible estimate. Ships with `> NEEDS CONFIRMATION: {what's missing}` block, never silently synthesized.

### Editorial Guidelines

Cross-cutting content rules for the keyword set. The SOP points back here; the rules live here once.

**Guideline 1 - Classify every keyword into one of four intent buckets.**

- **Informational** - "what is...", "how to...", "do I need...", "types of...", "causes of..." - the podcast's natural lane.
- **Commercial** - "best X lawyer near me", "top X attorney [city]", "X lawyer reviews" - for paid search and Google Business, not podcast content.
- **Transactional** - "hire a X lawyer", "file a X claim", "free X consultation" - bottom-funnel, rare in podcast targeting.
- **Navigational** - branded queries for specific firms or agencies - informational value only.
- Legal podcast work is mostly Informational with some Commercial the podcast should not chase directly. Keep Commercial keywords in the set for context but flag them.
- **Where it fires in the SOP:** `## Create -> ### Classify intent`.

**Guideline 2 - Prominence is the discriminator, not popularity (Koray).**

- A keyword can have high MSV but not be prominent to the practice area (e.g., "car accident video" is entertainment intent, not legal inquiry). Filter keywords that do not align with the practice area's semantic core even if MSV is high.
- Do not remove them from the JSON - downstream may want the full landscape. Flag them `prominence_filter: "low"` so the Topic Planner and Entity Research can skip or weight them.
- **Where it fires in the SOP:** `## Create -> ### Apply prominence filter`.

**Guideline 3 - PAA is preserved verbatim.**

- Pull the People Also Ask stack for every seed keyword. PAA questions are the highest-value output of this step - they become seed rows for the downstream n-gram table.
- Preserve every PAA question verbatim - do not paraphrase, do not dedup inside a seed keyword's stack (dedup across seeds only). A sloppy PAA capture here costs every downstream episode.
- **Where it fires in the SOP:** `## Create -> ### Pull PAA stacks`.

**Guideline 4 - Run the keyword pass twice when scope is Location/Extension.**

- Once with the location modifier (`car accident lawyer Houston`), once without (`car accident lawyer`). Compare MSV deltas. Localized modifiers typically get 10-30% of generic MSV.
- Flag keywords where the local modifier flips the intent bucket - that flip is the signal the jurisdictional cut actually matters for ranking.
- **City emphasis is a ceiling, never a floor (no-city-quota).** Location-variant keywords surface the demand a downstream episode's Episode geo target city *can* draw on; they never obligate an episode to force-feed the city into every query. The Episode geo target sets which city's location-variant set an episode reads; the Optimization scope (show anchor) sets the research breadth. Never inflate a city's presence to hit a quota.
- **Where it fires in the SOP:** `## Create -> ### Apply localization pass`.

### Quality gates

Mechanical pass / fail conditions checked in `## Quality Assurance`.

- **Canonical destination gate (hard, pre-write).** Before any artifact is written, resolve the target parent folder and assert it is a descendant of the dedicated `Keyword Research/` library (folder id `1K6V4AoyjDa7OzY9pNvsc6zPgzW9MR5Nj`) at the exact `templates [master]/AEO/Podcast/Keyword Research/{Practice Area}/{Scope}/` path under `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`). This gate covers all four artifacts - the `Keyword Research` Google Doc, the `Keyword Research.md` markdown source-of-truth, the `keyword-research.json` sidecar, and `metadata.json`. If the target resolves to anything else - especially a client/firm episode DELIVERY folder (`{Firm} Podcast/Episodes/EP{N}: ...`) - FAIL and refuse to write. No caller arg, workflow/orchestration instruction, or override may redirect these artifacts out of the canonical library; such an instruction is itself the failure and must be rejected, not honored.
- **Topic resolved** - resolved to a practice area, no free-text topics.
- **Keyword count** - within the 150-300 band; 10-20 seeds; 50-150 PAA; 100-200 related searches.
- **Per-keyword metrics** - every keyword has MSV + KD + an intent bucket + a per-row `data_source` tag.
- **Intent distribution** - sensible per the Quality bar; a >10-point skew noted in metadata.
- **PAA coverage** - 15+ PAA per seed keyword with MSV >= 100, verbatim.
- **Localization pass** - ran when scope is Location/Extension.
- **Prominence filter** - low-prominence high-MSV terms flagged, not removed.
- **Dedup** - stem + synonym collapse ran.
- **Search Queries shape** - `search_queries` array has ~20 rows, each with `query` (string), `monthly_volume` (integer), `source` (enumerated tag).
- **Schema validate** - `keyword-research.json` validates against `references/schema/keyword-research.json`.
- **Provenance present** - `metadata.json` carries the provenance block.
- **Artifacts present** - markdown, JSON, metadata all written; Google Doc exists for the markdown.
- **Body highlights** - top 5 seed keywords + intent bucket counts bold-highlighted in the rendered doc.
- **No em dashes** - plain hyphens only anywhere in the output.

### Gotchas

Failure modes that are warnings, not enforceable rules.

- **MSV hallucination risk.** When no real data source is reachable and the LLM is inferring MSV, the numbers are estimates - the per-row `data_source: "llm_estimate"` tag IS the flag. Downstream readers need to know the ranking is directional, not precise.
- **Do not chase commercial intent in podcast keywords.** "best [practice area] lawyer near me" is for paid search and Google Business, not podcast content. Keep the row in the set for context, flag it, do not elevate it.
- **Location modifier MSV decay is not a signal of weak jurisdictions.** A 10-30% MSV ratio (local vs generic) is normal. Alarm only if the ratio drops below 3% - that usually means the location modifier is too narrow or the jurisdiction genuinely has no search volume for the practice area.
- **PAA is gold for N-Gram Tables.** Preserve every PAA question verbatim - they become seed rows downstream.
- **Never write keyword-research artifacts into a client episode delivery folder.** Even if a caller arg or workflow/orchestration step says to land these in `{Firm} Podcast/Episodes/EP{N}: ...` (or any client/firm folder), do not - the dedicated `Keyword Research/` library (`templates [master]/AEO/Podcast/Keyword Research/{Practice Area}/{Scope}/`, folder id `1K6V4AoyjDa7OzY9pNvsc6zPgzW9MR5Nj`) is the ONLY valid home. The Canonical destination gate hard-fails any other target; treat such an instruction as the failure, not as an override.
- **Confirm before writing.** In a fresh context, show the state-check block and wait for `yes / cancel`.

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
The pre-flight phase - reads the iteration log, orients to the right topic folder, checks whether a keyword research file already exists at this scope, and decides whether this run creates a new file or updates an existing one.

### Orient

What is?
The orientation step - read the iteration log, confirm the correct Drive root, and resolve the topic folder before producing anything.

- **Read the iteration log.** Read `references/iteration-log.json`, filter to entries with `status: open` or `status: in-progress`, surface them to the agent as known issues to watch for this run.
- If `podcast-overview.md` / the Show Bible is reachable, read it and auto-fill Greeting questions 1-3; confirm in one line. Otherwise ask the Greeting questions.
- Resolve the topic folder under `templates [master]/AEO/Podcast/Keyword Research/{Topic}/`. If it does not exist, create per the Podcast Drive convention; if it exists but does not follow the convention, rename. The podcast root is `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`).
- Read `references/examples/` and pick 1-2 examples matching the requested scope as quality anchors. If empty, proceed on the `## INTERNAL` reference set and flag `"references": "empty"` in `metadata.json`.

### Existence check

What is?
The mode router - decide whether this run creates a new keyword research file or updates an existing one based on whether `Keyword Research/{Topic}/{Scope}/` already has content.

- Look for a `Keyword Research` Google Doc + `keyword-research.json` inside the resolved scope folder.
- **Missing:** no prior artifact - route to `## Create`.
- **Found:** surface provenance (existing `metadata.json` run date, keyword count) and ask: refresh in place / archive-and-rebuild / cancel.
  - Refresh in place - route to `## Update`.
  - `archive-and-rebuild` (or the refresh flag passed at invocation) - move prior content to `_archive-{YYYY-MM-DD}/` and route to `## Create`.
- **Handoff Contract check.** Keyword Research is a Research-pass entry point with no upstream. If any file appears in `_inputs/` that is not declared in the Inputs contract (a new content-gap format, a third-party SERP export), STOP and ask: "I see `{path}` but my Inputs contract does not declare it. Should I (a) mine it with my best guess, (b) skip it, or (c) pause while you update the handoff contract?" Do not guess silently.

## Prepare Inputs

What is?
The input-preparation phase - loads seed keywords, the content-gap report, Ahrefs access, and Koray methodology grounding into a working set ready for the Create or Update phase.

Work through the input sources in priority order; on a tool error, skip that source and degrade to the next.

- **Consult Koray RAG.** Call `mcp__ce-services__rag_query` with `rag_name: "koray"`, `top_k: 6`, discard results with score < 0.40. Run the 5-query table in `## INTERNAL` for prominence-filter and intent-classification grounding. On an error, log `koray_rag: unreachable` and proceed on in-skill methodology.
- **Load the content-gap report.** Scan `~/Desktop/claude_code/mcps/content-gap-mcp-server-andrew/data/reports/{practice-area-slug}/` for `serp-*.json`, `paa-*.json`, `keyword-volume-*.json`. If nothing is there, check `_inputs/` of the matching scope folder in Drive. Mine seed candidates, real MSV, real PAA stacks, related searches, SERP feature presence. If no report exists, log `content_gap: llm_only` and proceed.
- **Confirm Ahrefs availability.** Call an Ahrefs MCP tool; if it returns data, the Create phase pulls real MSV / KD / CPC / SERP-feature data per keyword; on an error, it falls back to LLM estimates per row.
- **Normalize seed keywords.** If the user supplied seeds, normalize and dedup them. If not, prepare to expand from the practice area name + known subtopics in the Create phase.
- **Load calibration examples.** Hold the 1-2 scope-matched examples from `references/examples/` as quality anchors for the Create phase.

## Create

What is?
The create branch - builds the keyword research set from scratch when no prior file exists, producing a ranked, classified, deduped, schema-valid `keyword-research.json` plus its markdown and metadata.

**Best Practices.**
These apply to the entire create phase and should be checked after each step.

- Keyword research is a demand pass, not a topic-selection pass - surface the full demand landscape, do not pick winners (Framing).
- Hold the scope-matched calibration examples in view while generating - calibrate keyword count, PAA yield, and intent distribution against them.
- Per-row `data_source` provenance is preserved on every keyword - a single set can mix `ahrefs`, `content-gap`, and `llm_estimate` rows (Sourcing discipline).
- Output counts and intent distribution follow `### Quality bar` - do not restate the thresholds, apply them.

If the model generates output that violates any of these, emit a `> NEEDS VERIFICATION:` block at the offending location instead of shipping the claim.

### Mine seed keywords

What is?
The pass that produces the 10-20 seed keyword set - the anchor demand terms the full keyword set expands from.

- If the user supplied seeds, normalize and dedup. If not, expand from the practice area name + known subtopics for the domain. Target 10-20 seeds.
- When the Ahrefs MCP is available, cross-check seeds against `keywords_explorer` / `matching_terms` results so the seed set covers what people actually search, not just what the LLM thinks they search.

### Pull metrics

What is?
The pass that fills MSV, KD, CPC, and SERP features for every keyword, tagging each row with its data source.

- For every seed + expansion term, pull MSV, KD, CPC, SERP features following the volume source priority chain - the first source that returns data for a keyword wins; the chain degrades per keyword, not per run.
  - **Keywords Everywhere (PRIMARY for MSV + CPC):** resolve the KE API key from 1Password via `mcp__op-broker__read_secret` (item `Keywords Everywhere API Key`, `caseengine` account, `Paid` team vault), export it as `KE_API_KEY`, and call `scripts/ke_volume_backfill.py` -> `fetch_ke_volumes(keywords, key)` (`POST https://api.keywordseverywhere.com/v1/get_keyword_data`, `dataSource=gkp`, batches of 100, 1 credit/keyword). Capture real Google Keyword Planner MSV + CPC; tag rows `data_source: "keywords_everywhere_gkp"`. The KE key is NEVER hardcoded. KE does not return KD or SERP features - pull those from Ahrefs or estimate them.
  - **Ahrefs (fallback for MSV / CPC; primary for KD + SERP features):** when Keywords Everywhere is unreachable, or for KD / SERP-feature signals KE does not return, call `mcp__claude_ai_Ahrefs__*` tools; capture metrics; tag MSV/CPC rows sourced here `data_source: "ahrefs"`. If a term is rate-limited or returns no data, fall back to LLM estimate for that term only.
  - **Content-gap report mined:** use real MSV / SERP data from the report; tag `data_source: "content-gap"`.
  - **No real data source:** LLM-estimate and tag `data_source: "llm_estimate"`.
- Per-row provenance is preserved - downstream consumers read the per-row tag. A single keyword set can mix `keywords_everywhere_gkp`, `ahrefs`, `content-gap`, and `llm_estimate` rows.

### Classify intent

What is?
The pass that buckets every keyword into one of the four intent categories.

- Bucket every keyword per Editorial Guideline 1 - Informational / Commercial / Transactional / Navigational.
- Keep Commercial keywords in the set for context but flag them - the podcast should not chase commercial intent directly.

### Pull PAA stacks

What is?
The pass that captures the People Also Ask question stack for every seed keyword - the highest-value output of this skill.

- Pull 15+ PAA questions per seed keyword with MSV >= 100, verbatim per Editorial Guideline 3.
- Prefer the cached `paa-*.json` from the content-gap report path; fall back to Ahrefs SERP-feature data (PAA box scrape); fall back to LLM-inferred PAA only as a last resort (tag the row `paa_source: "llm_inferred"`).
- Do not paraphrase, do not dedup inside a seed keyword's stack (dedup across seeds only).

### Apply localization pass

What is?
The pass that runs the keyword set twice at Location/Extension scope to surface the jurisdictional demand delta.

- When scope is Location or Extension, run the keyword pass with and without the location modifier per Editorial Guideline 4.
- Compare MSV deltas; flag keywords where the local modifier flips the intent bucket.
- Record the localization ratio (local MSV / generic MSV) for `metadata.json`.

### Apply prominence filter

What is?
The pass that flags high-MSV terms that do not align with the practice area's semantic core.

- Per Editorial Guideline 2, flag low-prominence high-MSV terms `prominence_filter: "low"`.
- Do not remove them - downstream may want the full landscape.

### Dedup, tier, build Search Queries table

What is?
The pass that collapses keyword variants, tiers the set, and assembles the ~20-row Search Queries & Volume handoff table.

- Two-pass dedup: stem collapse (`car accident` + `car accidents` = one canonical, plural/singular recorded as a variant), then synonym collapse (`trucking accident` + `18 wheeler accident` + `semi truck accident` = one canonical with synonyms listed inline). Dedup happens last, after scoring and tiering.
- Tier the set by intent x prominence x MSV.
- Build the `search_queries` array: pick the top ~20 queries by Monthly Volume across the full set (not just seeds - pull from PAA stacks and related searches where they have real volume), order descending by MSV, tag each row's source per `### Outputs -> #### Search Queries & Volume table`.

### Render markdown

What is?
The pass that assembles the final artifacts - the `Keyword Research.md` source-of-truth with cover + executive summary + ranked set + PAA stacks + related searches + Search Queries table + the `## INTERNAL` block, the `keyword-research.json` sidecar, and `metadata.json`.

- Assemble `Keyword Research.md`: title (H1), executive summary (keyword count, intent distribution, PAA totals, data source), ranked keyword set by intent bucket, PAA stacks per seed keyword, related searches, the `### Search Queries & Volume` H3 table, localization summary (when scope is Location/Extension), then the `## INTERNAL` block.
- Bold the top 5 seed keywords and the intent bucket counts in the executive summary.
- Serialize `keyword-research.json` per `### Outputs -> #### Schema`, including the `search_queries` array and the provenance block.
- Write `metadata.json` with the provenance block per `## INTERNAL`.

## Update

What is?
The update path - modifies an existing Keyword Research file in place when a prior version exists, preserving any manual edits the producer made since the last skill run.

**Best Practices.**
These apply to the entire update phase and should be checked after each step.

- **Diff before write.** Pull the existing `keyword-research.json` + `Keyword Research.md`, compare against the proposed new state, surface every changed keyword / PAA stack before committing the write.
- **Preserve manual edits.** Any keyword, MSV value, intent bucket, prominence flag, or PAA question that was manually edited since the last skill run keeps its current value. The skill never auto-overwrites a manual edit silently.
- **Flag merge conflicts inline.** When a new auto-generated value disagrees with a preserved manual edit, emit `> NEEDS VERIFICATION: auto-generated value [X] conflicts with manual edit [Y]` at the row; the producer resolves.
- **Stable fileId.** Update uses `files.update` against the existing `Keyword Research` Google Doc fileId. Never create a new Doc; never delete-and-recreate.

If the model proposes overwriting a manual edit without flagging it, halt and emit `> NEEDS VERIFICATION:` instead of shipping the change.

### Diff against existing

What is?
The pass that loads the prior keyword set and computes a row-level diff against the proposed new state so nothing changes silently.

- Read the prior `keyword-research.json`, `Keyword Research.md`, and `metadata.json` from the resolved scope folder.
- Read the prior `metadata.json` provenance block to recover the last run's sources, counts, intent distribution, and references status.
- Run the Create-phase passes (`### Mine seed keywords` through `### Dedup, tier, build Search Queries table`) to compute the proposed new state.
- Compute a row-level diff: keywords added, removed, re-scored, re-classified, and untouched; PAA stacks added / changed.

### Merge and resolve conflicts

What is?
The pass that merges the new content into the existing keyword set - new keywords in, stale rows out, manual edits preserved, conflicts flagged for the producer.

- Apply the phase-level Best Practices: preserve every manually-edited keyword / MSV / intent bucket / PAA question; merge new rows; drop rows the dedup pass retired.
- Where a new auto-generated value disagrees with a preserved manual edit, emit the `> NEEDS VERIFICATION:` conflict block inline; do not auto-resolve.
- Re-render `Keyword Research.md`, `keyword-research.json`, and `metadata.json` per `### Render markdown`. Bump the `metadata.json` run date and append the run to the provenance history.
- The shared `## Quality Assurance` phase runs after this phase - QA does not re-run inside Update.

## Quality Assurance

What is?
The gate before `## Ship` - a three-tier check (Best Practices by name, the hardwired Anti-AI Detection two-pass scan, then skill-specific mechanical checks) that runs after whichever branch fired (`## Create` or `## Update`).

**First - check against Best Practices.** The deliverable must align with the contract defined upstream in this file. This is always the first gate; skill-specific checks come after.

- **Quality bar** (Best Practices -> Quality bar) - 150-300 keywords, 10-20 seeds, 50-150 PAA, 100-200 related searches; every keyword has MSV + KD + intent + `data_source`; intent distribution near target; 15+ PAA per seed verbatim; Search Queries table ~20 rows; localization pass ran at Location/Extension; prominence filter applied; dedup ran; no em dashes / banned vocabulary.
- **Sourcing discipline** (Best Practices -> Sourcing discipline) - every keyword carries a per-row `data_source` tag; LLM estimates tagged `llm_estimate`; inferred PAA tagged `llm_inferred`; any belongs-but-missing data flagged `> NEEDS CONFIRMATION:`. No silent synthesis.
- **Editorial Guidelines** (Best Practices -> Editorial Guidelines) - Guideline 1 (four intent buckets), Guideline 2 (prominence filter, flag not remove), Guideline 3 (PAA verbatim), Guideline 4 (localization twice-pass at Location/Extension).
- **Quality gates** (Best Practices -> Quality gates) - full checklist must pass: topic resolved, keyword count, per-keyword metrics, intent distribution, PAA coverage, localization pass, prominence filter, dedup, Search Queries shape, schema validate, provenance present, artifacts present, body highlights, no em dashes.

**Second - Anti-AI Detection two-pass scan** (canonical doc: https://docs.google.com/document/d/1hp7bxOFRlMhCuhjHNY0j05JrB97-KOFD0XUCQM3gMBU/edit). Mandatory for every text-producing skill. Run the full Section 7 two-pass audit against the deliverable:

- **Pass 1 (mechanical scan):** em-dashes, banned vocabulary (Section 2), banned phrases (Section 3), triadic rhythms and symmetric paragraphs (Section 4), summary-only section closers, date formatting per destination, specific-claims-trace-to-source, no numbered lists in ClickUp, no emojis (unless requested), no clickbait.
- **Pass 2 (skeptical re-read):** restart from the top. Did I actually check every line, or skim? Em-dashes I missed? Banned phrases I rationalized? Triadic rhythms left because they "sounded fine"? PAA questions paraphrased instead of verbatim? Am I sure?
- **On any hit:** fix and re-run Pass 2 until clean. One pass is not enough.

**Third - skill-specific mechanical checks.**

- `keyword-research.json` validates against the canonical schema `references/schema/keyword-research.json`. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed.
- `metadata.json` provenance block present with at minimum: `run_date`, `topic`, `scope`, `location` (or null), `koray_rag` (used / unreachable / skipped), `ahrefs_mcp` (used / unavailable), `content_gap_source` (auto-detect / manual-upload / llm-only), `data_source` (per-run summary: ahrefs / content_gap / llm_estimate / mixed), `references_status` (used / empty), `schema_status` (validated / missing), keyword / seed / PAA / related-search counts, intent distribution, and localization ratio.
- Search Queries & Volume shape: `keyword-research.json` has a `search_queries` array with ~20 rows, each with `query` (string), `monthly_volume` (integer), `source` (enumerated tag) - the verbatim handoff shape for Run of Show.
- Spot-check 3 random keyword rows: MSV is numeric (not a string), intent bucket is one of the 4 valid values, prominence flag present when low-prominence high-MSV, `data_source` tag present per row.
- Both write destinations verified: confirm the Drive `Keyword Research/{Topic}/{Scope}/` folder AND the local mirror at `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/02.5-keywords/` contain the same artifacts.
- INTERNAL section grep test: `grep -L "## INTERNAL" {client-facing-export}` returns zero hits for the client-facing Google Doc.

**On failure:** fix the markdown, regenerate `keyword-research.json` and `metadata.json`, re-run all checks. Do not proceed to `## Ship` until QA returns clean.

## Ship

What is?
The publish phase - writes the trio plus `metadata.json` to the topic's `Keyword Research/{Topic}/{Scope}/` Drive folder and mirrors the same artifacts to the local Desktop path.

### What ships

- **`Keyword Research`** - Google Doc - human-facing canonical view, Roboto typeface, stable fileId.
- **`Keyword Research.md`** - Markdown - source-of-truth mirror, retains the `## INTERNAL` block.
- **`keyword-research.json`** - JSON - machine-readable, downstream-consumed, includes the `search_queries` array.
- **`metadata.json`** - JSON (internal) - provenance: sources, counts, intent distribution, localization ratio.

### Where it ships

- **Drive:** `templates [master]/AEO/Podcast/Keyword Research/{Topic}/{Scope}/` in the shared drive `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`); `Keyword Research/` folder id `1K6V4AoyjDa7OzY9pNvsc6zPgzW9MR5Nj`. The `{Scope}` segment resolves per the table in `### Outputs -> #### Drive destination`. This destination is fixed - the skill does not move existing Drive data.
- **Local mirror:** `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/02.5-keywords/` - written every run; includes a `gdoc-url.txt` pointer.
- **Schema:** `~/.claude/skills/pod-2B-keyword-research/references/schema/keyword-research.json`.

### How it ships

Write to both destinations. On a write error to one, ship to the other and report the partial state.

- **Drive write.** Upload `Keyword Research.md` as `text/markdown`. Create / update the `Keyword Research` Google Doc in-place via `files.update` against the existing fileId (on a `## Create` run with no prior Doc, create once and record the fileId). Upload `keyword-research.json` and `metadata.json` as binary. Truncate the markdown source at the first `## Quality Assurance` heading before rendering the Google Doc.
- **Roboto pass.** After the base text Doc is uploaded, run a `docs.documents.batchUpdate` with `updateTextStyle` setting `weightedFontFamily.fontFamily = "Roboto"` over the full document range as the final pass before sharing. Override only when a per-client `brand.json` typography block specifies otherwise.
- **Body highlights.** Bold the top 5 seed keywords and the intent bucket counts (Informational / Commercial / Transactional / Navigational) in the executive summary; render the keyword tables and PAA stacks cleanly.
- **Cover + footer.** Render the cover page (CE logo top, title `Keyword Research`, subtitle = topic, scope line, "Prepared by Case Engine" + date in `Month D, YYYY`). Footer `Case Engine  |  Confidential  |  Page {PAGE}` auto-applied via the Drive API template.
- **Archive.** If the existence check moved prior content to `_archive-{YYYY-MM-DD}/`, the archive folder ships alongside the new artifacts.
- **Local mirror write.** Write the same `Keyword Research.md`, `keyword-research.json`, `metadata.json`, and `gdoc-url.txt` to the local mirror path. If the Drive write fails but the local write succeeds, surface the partial state in the report - do not silently swallow it.
- **Report back:**

  ```
  Done. Keyword Research - {Topic}{ / Location if applicable}.

   Folder: https://drive.google.com/drive/folders/{folder_id}
   Keyword Research (Doc): https://docs.google.com/document/d/{doc_id}

  Counts: {N} keywords, {S} seeds, {P} PAA questions, {R} related searches.
  Intent: {info}% info / {com}% commercial / {tx}% transactional / {nav}% navigational.
  Data source: {ahrefs | content_gap | llm_estimate | mixed}. Koray RAG: {used | unreachable}. Localization: {PASS / n/a}.

  Next: pod-2A-entity-research and pod-2C-virality-research run in tandem with this skill. Downstream: N-Gram Table, Topic Planner, Run of Show (downstream numbering pending).
  ```

### Who to Notify

`notify: []` - this skill posts no notifications. The producer is informed via the inline report-back above.

---

## INTERNAL (not for client distribution - auto-stripped from all exports; the reference material and worked examples ride into the local markdown only, never into the Drive Doc)

### Koray RAG query table

When `mcp__ce-services__rag_query` is reachable, run these 5 queries with `rag_name: "koray"`, `top_k: 6`, discard score < 0.40. Use the returned chunks as methodology grounding for prominence filtering + intent calibration.

| # | Query |
|---|-------|
| 1 | `keyword research prominence vs popularity for {practice_area}` |
| 2 | `intent classification informational commercial transactional navigational seo` |
| 3 | `paa people also ask seed extraction n-gram source` |
| 4 | `localization jurisdictional modifier search volume legal practice areas` |
| 5 | `keyword difficulty serp feature CTR estimation` |

### Output count targets

| Item | Target band |
|---|---|
| Total keywords | 150-300 |
| Seed keywords | 10-20 |
| PAA questions | 50-150 |
| Related searches | 100-200 |

Target intent distribution: 60% Informational / 25% Commercial / 10% Transactional / 5% Navigational. A skew more than 10 points off is noted in metadata - it usually signals the topic itself is lopsided.

### Search Queries & Volume JSON shape

```json
{
  "search_queries": [
    {"query": "california car accident lawyer", "monthly_volume": 6600, "source": "LLM estimate"},
    {"query": "car accident compensation california", "monthly_volume": 1900, "source": "LLM estimate"}
  ]
}
```

When Run of Show builds its Appendix, it reads this `search_queries` array and renders it under `Search Queries & Volume` verbatim - same shape, same ordering, same source values.

### Provenance block

`metadata.json` must include a provenance block with at minimum: `run_date`, `topic`, `scope`, `location` (or null), `koray_rag` (used / unreachable / skipped), `ahrefs_mcp` (used / unavailable), `content_gap_source` (auto-detect / manual-upload / llm-only), `data_source` (per-run summary: ahrefs / content_gap / llm_estimate / mixed), `references_status` (used / empty), `schema_status` (validated / missing), keyword / seed / PAA / related-search counts, intent distribution, and localization ratio.

### Source inventory

Records every input the run consumed: the Ahrefs MCP status, the resolved content-gap report path and source (local / Drive `_inputs/` / llm-only), the Koray RAG status, any user-supplied seed list, and the calibration examples used.

---

## Learning & Iteration

- [ ] After each run, note MSV data source and whether the estimates held up, PAA yield per seed keyword (is 15+ realistic), intent distribution skew from the 60/25/10/5 target, localization MSV ratio and any intent flips, prominence filter catches. Append GOOD / BAD / EDGE CASE entries to `references/examples/`.
- [ ] Track recurring PAA yield shortfalls - if 15+ per seed is unrealistic for a domain, tighten the `### Pull PAA stacks` target.
- [ ] Watch for intent distributions that skew the same direction across runs of the same topic; if it recurs, note the topic is genuinely lopsided.

## Change Log

| Date | Change |
|---|---|
| 2026-04-20 | Initial co-work version. Drive-native. Koray prominence filter applied. PAA stacks captured per seed keyword to feed downstream n-gram tables. |
| 2026-04-20 | Promoted Quality gates to H2 after SOP, split into Content + Formatting subsections. Added Handoff Contract. Added required Search Queries & Volume table output serialized to the `search_queries` JSON key. |
| 2026-04-21 | DOCX layer removed. Client-facing artifacts render as Google Docs only. |
| 2026-05-14 | **v2.0.0** - canonical local land as `pod-2.5-keyword-research`. Dual-mode via runtime capability probe; Ahrefs MCP + content-gap + PAA-cache auto-detect; per-row `data_source` tag preserves provenance when sources are mixed. `## Quality Assurance` H2 added. Frontmatter: `name: pod-2.5-keyword-research`, `skill_kind: hybrid`. |
| 2026-05-20 | **v3.0.0** - renamed `pod-2.5-keyword-research` -> `pod-2B-keyword-research` (folder + slug + frontmatter `name`). Full structural refactor to the canonical CE skill structure mirroring `pod-5-n-gram-table` v3.0.0. Frontmatter completed (`skill_kind`, `modes: multi`, `inputs`, `outputs`, `notify`; `version`/`date`/`owner` moved to a `metadata` block; the Inputs table replaced by Required / Optional / Auto-read bullets). Best Practices restructured to the canonical contract H3s (Inputs / Outputs / Framing / Quality bar / Sourcing discipline / Editorial Guidelines / Quality gates / Gotchas / Iteration log); intent / prominence / PAA / localization / dedup / output-count methodology relocated into Quality bar + Editorial Guidelines + the deliverable-shaped Create buckets. SOP rebuilt as H2 phase siblings (Checks / Prepare Inputs / Create / Update / Quality Assurance / Ship); the old numbered Step 0-13 SOP replaced; `## Push to Drive` -> `## Ship`; Universal State Check versioning logic moved into `## Update`. QA rewritten as the canonical three-tier gate with the hardwired Anti-AI Detection two-pass scan and an On-failure recovery line. Old `## Output` folded into Best Practices Outputs + the new `## Ship` phase; all Drive folder IDs and the local mirror path preserved verbatim. Owner Gabe Jordan. |
| 2026-05-20 | **Probe-strip pass.** Removed the entire `### Probe environment` H3 and all capability-probing apparatus - this skill runs locally in Claude Code only, calls its tools directly, and skips or fails on a tool error rather than probing first. `#### Capabilities` (Inputs) became `#### Tools the skill calls`; `#### Capabilities` (Outputs) became `#### Write destinations`. All `runtime.capabilities` metadata fields dropped; all "when the FS-write probe succeeds" conditionals removed - local-mirror writes are now unconditional. Iteration-log read-at-start contract repointed to `### Orient`. Workflow diagram replaced with the unified 4-phase pipeline diagram (Foundation / Research / Planning / Run of Show). |
| 2026-05-21 | **Keywords Everywhere wired as PRIMARY volume source.** Added Keywords Everywhere (API, `dataSource=gkp`) ahead of the Ahrefs MCP and the LLM-estimate fallback. Documented the volume source priority chain: Keywords Everywhere -> Ahrefs MCP -> LLM estimate, degrading per keyword. KE API key resolved at runtime from 1Password via `mcp__op-broker__read_secret` (item `Keywords Everywhere API Key`, `caseengine` account, `Paid` vault), passed as `KE_API_KEY`, never hardcoded. Reusable lookup helper `scripts/ke_volume_backfill.py` -> `fetch_ke_volumes(keywords, key)`. Edits landed in `#### Tools the skill calls`, `### Sourcing discipline` (Confirmed tag list now includes `keywords_everywhere_gkp`), and SOP `### Pull metrics`. |
| 2026-07-10 | **Three-field geo model alignment (Gabe directive, Whalen scoping).** Sharpened the Greeting anchor interview and `### Framing` to the canonical geo model - **Targeting strategy** (single/multi-location), **Optimization scope (show anchor)** (City/State/County/Regional), **Episode geo target** (per-episode city). Stamped the rule *anchor scope != per-episode target*: keyword/MSV data pulls at the anchor breadth AND per target city; the Episode geo target selects which city's location-variant keywords an episode reads downstream, the anchor governs research breadth. Added a no-city-quota ceiling-not-floor bullet to Editorial Guideline 4 (preserves natural tonality - city emphasis is a ceiling, never a floor). Schema `references/schema/keyword-research.json` bumped 1.0 -> 1.0.1: added `targeting_strategy` + `optimization_scope`, clarified `location` as the Episode geo target. No existing behavior renamed (Topic/Location/Extension scope + location-variant keyword passes preserved verbatim). Owner Gabe Jordan. **Revert:** remove the Framing rule paragraph, the Greeting two-field reframe, the Guideline 4 no-city-quota bullet, and the schema 1.0.1 fields. |
| 2026-06-17 | **Canonical destination gate added (hard, pre-write).** New `### Quality gates` bullet asserts every artifact (Google Doc, `Keyword Research.md`, `keyword-research.json`, `metadata.json`) writes only into the dedicated `Keyword Research/` library at `templates [master]/AEO/Podcast/Keyword Research/{Practice Area}/{Scope}/` (folder id `1K6V4AoyjDa7OzY9pNvsc6zPgzW9MR5Nj` under `Podcasts // Case Engine [Shared]` id `0AAJKtWTUAZhHUk9PVA`); resolves to a client/firm episode DELIVERY folder (`{Firm} Podcast/Episodes/EP{N}: ...`) FAIL and refuse to write. No caller arg, workflow, or override may redirect the artifacts out of the library - such an instruction is the failure and is rejected. Cross-reference added in `#### Drive destination` and a matching Gotcha. Parallels the gate added to `pod-3B-n-gram-table` and `pod-2A-entity-research`. Owner Gabe Jordan. **Revert:** delete the `### Quality gates` Canonical destination gate bullet, the `#### Drive destination` cross-reference sentence, and the Gotcha; pre-2026-06-17 behavior had no hard destination gate. |
