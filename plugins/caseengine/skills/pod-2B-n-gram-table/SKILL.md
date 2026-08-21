---
name: pod-2B-n-gram-table
description: >
  Build the LLM Collation Table (N-Gram Table) for a single podcast episode -
  four columns (Question, N-grams, Entities, Predicates), 25-35 rows per scope
  (Topic Only / Location / Extension). Use whenever someone says "n-gram table
  for [episode]", "build collation table for [topic]", "create question
  framework for [episode]", "llm collation table", or "/pod-2B-n-gram-table".
  Phase 2 Planning of the podcast pipeline; hard dependency on a matching-scope
  entity map; feeds pod-3A-ros-template, pod-3B-client-ros, and pod-3C-client-guide downstream.
skill_kind: hybrid
modes: multi
inputs: [entity-map.json, entity-clusters.md, keyword-research.json, topic-plan.json, podcast-overview.md, case-engine-branding]
outputs: [json, markdown, gdoc]
notify: []
metadata:
  version: 3.1.0
  date: 2026-07-31
  owner: Gabe Jordan
  version_history: >
    1.0 - co-work Drive-native version (2026-04-20). 2.0.0 - merged cowork
    canonical content with original local pod-5-n-gram-table Mode A enrichments
    (2026-05-14). 3.0.0 - renamed pod-5-n-gram-table -> pod-2B-n-gram-table; full
    structural refactor to canonical CE skill structure; probe apparatus
    stripped (2026-05-20). 3.0.1 - PATCH: aligned scope/anchor/location language
    to the canonical three-field geo model (Targeting strategy / Optimization
    scope (show anchor) / Episode geo target) and stamped the anchor-scope !=
    per-episode-target rule; schema scope/location descriptions mapped to the
    model (2026-07-10, Gabe directive from the Whalen scoping).
---

# N-Gram Table

> **Drive write governance:** All Drive operations (create, update, rename, move) follow [Ship]. Revise in place via `files.update` against the existing fileId, never delete-and-reupload (breaks the fileId/URL chain and silently kills every downstream reference).

### What is

An LLM Collation Table (sometimes called an N-Gram Table) for a single podcast episode. Four columns, 25-35 rows: Question Text, N-grams to Mention, Entities to Mention, Predicates to Mention. It is the episode's content backbone - every question becomes a beat in the Run of Show, every entity feeds the localized script, every predicate seeds the attorney response bullets. One table per episode per scope (Topic Only / Location / Extension), saved to Google Drive as the shared source of truth and consumed downstream by pod-3A-ros-template, pod-3B-client-ros, and pod-3C-client-guide.

### Workflow

N-Gram Table is part of **Phase 2 (Planning)** of the podcast pipeline, alongside `pod-2A-topic-planner`. Per-episode, per-scope - a different table for Topic Only, each Location, and each Extension. Hard dependency on a matching-scope entity map from Phase 1 Research.

```
PHASE 1: RESEARCH  (one in-tandem pass - Topic Only + Topic+Location)
┌─ 1A ──────────┐ ┌─ 1B ──────────┐ ┌─ 1C ──────────┐
│ Entity        │ │ Keyword       │ │ Virality      │
│ Research      │ │ Research      │ │ Research      │
└───────────────┘ └───────────────┘ └───────────────┘
        │
PHASE 2: PLANNING
┌─ 2A ──────────┐ ┌─ 2B ──────────┐
│ Topic Planner │ │ N-Gram Table  │
│               │ │               │
└───────────────┘ └───────────────┘
                    ◄── YOU ARE HERE
        │
PHASE 3: RUN OF SHOW  (per prioritized episode)
┌─ 3A ──────────┐ ┌─ 3B ──────────┐ ┌─ 3C ──────────┐
│ ROS Template  │ │ Client ROS    │ │ Client Guide  │
│               │ │               │ │               │
└───────────────┘ └───────────────┘ └───────────────┘
```

Notes:

- **Phase 1 Research** - `pod-1A-entity-research`, `pod-1B-keyword-research`, and `pod-1C-virality-research` run together as one research pass, ONCE per practice area + location cascade.
- **Phase 2 Planning** - `pod-2A-topic-planner` ranks episodes from the research and produces the content plan (= topic plan); `pod-2B-n-gram-table` (this skill) consumes the matching-scope entity map and builds the 4-column collation table for one episode at one scope. The topic plan is a soft prerequisite - see `### Greeting` and `### Inputs`.
- **Phase 3 Run of Show** - `pod-3A-ros-template`, `pod-3B-client-ros`, and `pod-3C-client-guide` run per prioritized episode; each consumes this table directly or transitively.

Prerequisites: a matching-scope entity map from `/pod-1A-entity-research` is a hard dependency - this skill will not run without it. A content plan from `/pod-2A-topic-planner` (= topic plan, same artifact) is a soft prerequisite - the skill checks for it and asks before proceeding if it is missing.

### Trigger phrases

- `/pod-2B-n-gram-table`
- "n-gram table for [episode]"
- "build collation table for [topic]"
- "run n-gram table for [client/city]"
- "create question framework for [episode]"
- "llm collation table for [episode]"

### Greeting

Hi, I'm the N-Gram Table. Before I run, I need to confirm the podcast architecture and check for an existing content plan. If podcast-overview has been run for this client, I'll read it and confirm in one line. If not, I'll ask:

1. **Client name.** Examples: "The May Firm", "Sutliff & Stout", "Conn Law Firm". Exact firm name as it appears in Drive.

2. **Optimization scope (show anchor) - what the podcast as a whole is optimized to rank for; the show-wide breadth the research was gathered at.** This is field 2 of the geo model (see `### Framing`) - the anchor breadth, NOT the city any one episode targets.
   - **City-level:** people in your market search the city as a unit ("Houston car accident lawyer"). Anchor: Houston.
   - **State-level:** people search the state as one unit ("California car accident lawyer"). Anchor: California. Per-episode geo targets (extension cities) per office.
   - **County / regional-level:** people search the region ("Inland Empire injury attorney", "Harris County", "Bay Area"). Anchor: the region/county. Cities within become per-episode geo targets (extensions).

3. **Extension locations (if any).** Extensions are sub-scope episodes - short derivatives (~10 questions, 30-35 minutes) that inherit from the anchor but surface what's different at the smaller scope. Can exist at any anchor level:
   - Houston city anchor -> Sugar Land, Katy, Pasadena suburb extensions
   - California state anchor -> Bakersfield, Fresno, Long Beach city extensions
   - Inland Empire regional anchor -> Ontario, Riverside, San Bernardino city extensions
   - List the extensions if any; "none" if the firm only targets the anchor.

4. **This run's scope (= the Episode geo target)** - anchor or a specific extension? The scope you pick IS field 3 of the geo model (see `### Framing`): a `Location` / `Extension` scope resolves to the one city THIS table is built to emphasize; `Topic Only` carries no episode geo target.

5. **Episode format** - resolved by the client's **Targeting strategy** (field 1 of the geo model; recorded in the podcast overview; ask if absent):
   - **Single-location client** -> Full episodes (~50-55 min, ~20 questions) for the target market. The pre-2026-06 default.
   - **Multi-location client** -> NO anchor/primary episode. Every topic produces one Mini episode (client-facing term; internal scope label stays `Extension`) per target city: ~30-35 min, 10-12 questions, hard cap. No hybrid (no full-plus-minis) unless the client brief explicitly says so.
   - Legacy anchor+extension model (anchor ~20q + per-city extensions): still valid for single-location clients that add satellite markets; extensions inherit from the parent anchor and overlap-with-parent is by design.

Then my skill-specific follow-ups:

6. **Content plan check.** Before generating, I check whether a content plan (= topic plan, the same artifact, output of `pod-2A-topic-planner`) already exists for this client. I auto-resolve it from the per-client Topic Plan slot `{Client Folder}/AEO/Podcast/Topic Plan/Topic Plan: {practice_area} // {client_name}/` - a `topic-plan-v{n}.*` artifact there means it exists.
   - **Found:** I use it as the episode-selection context and proceed.
   - **Not found AND not explicitly provided:** I ask you whether to (a) run `/pod-2A-topic-planner` first, or (b) proceed without it for this one episode. I will not silently invent an episode plan.
7. Does the matching-scope entity map exist?
8. If an n-gram table already exists for this episode + scope, archive and rebuild or refresh in place?

If anything's unclear I'll ask once in a single message. I won't touch Drive until you say go. You only need to know about `{Firm} Podcast/`. I'll handle the foundation lookups and writes transparently.

---

## Best Practices

The WHAT contract. Every other section references these by name; the SOP never restates them.

### Inputs

What is?
The materials this skill ingests - a matching-scope entity map (hard dependency), its sibling clusters file, an optional keyword-research seed set, an optional content plan, the podcast architecture doc, and the Case Engine Branding folder - all resolved before any table is generated.

#### Required

- **Matching-scope entity map** (`entity-map.json`) - the localized entity set from `/pod-1A-entity-research`. Must exist at the scope-matched `entity-map.json` for the resolved scope (`templates [master]/AEO/Podcast/Entity Research/{Topic}/{Scope}/entity-map.json`), or at the auto-detectable local path `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/01-entities/entity-map.json`. No silent fallback - if missing, the skill stops and routes to `/pod-1A-entity-research`.
- **Episode title** - the episode this table is built for.
- **Topic** - practice area (e.g., Personal Injury, Criminal Defense, Family Law).
- **Industry** - top-level industry (Legal, Healthcare, Finance, etc.).
- **Scope** - one of: Topic Only, Location, Extension.
- **Location** - required when scope is Location or Extension. Format: `CA`, `CA - Los Angeles County`, or `CA - Long Beach`. No colons; dashes only.

#### Optional

- **`entity-clusters.md`** - the clusters sibling of the entity map, same folder. Adds cluster context for question grouping; the skill proceeds without it.
- **`keyword-research.json`** - the keyword-research seed set from `/pod-1B-keyword-research`. When present, PAA stacks can be mined as seed questions. If found but undeclared in the handoff contract, the skill stops and asks rather than guessing silently.
- **Content plan** (`topic-plan-v{n}.json` / `topic-plan-v{n}.md`) - the topic plan from `/pod-2A-topic-planner`. "Content plan" and "topic plan" are the SAME artifact. The skill auto-resolves it from the per-client Topic Plan slot `{Client Folder}/AEO/Podcast/Topic Plan/Topic Plan: {practice_area} // {client_name}/`. When present, it supplies the episode-selection context (which episode this table is for, where it sits in the 12-episode arc). When NOT present AND not explicitly provided, the skill ASKS the user before proceeding (see `### Greeting` and `## Checks -> ### Check for content plan`). There is no separate content-plan folder or template - the Topic Plan slot is the single source.
- **Refresh flag** - default: refresh in place (routes to `## Update`). Pass `archive-and-rebuild` to force a full rebuild with prior content archived to `_archive-{YYYY-MM-DD}/`.

#### Auto-read (no action required)

- **`podcast-overview.md`** - architecture source of truth (anchor scope, extension cities, client name). If present at `{Firm} Podcast/.podcast-overview/podcast-overview.md`, the skill auto-fills Greeting questions 1-3; otherwise it asks.
- **Case Engine Branding folder** - the canonical brand reference at [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) (folder id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`). The `## Ship` render reads logo, `colors.md`, fonts, and `Cover Page Layout.png` from this folder for the client-facing Google Doc cover page and table styling. Brand values are resolved from the folder at render time - never inlined into this skill. A per-client `brand.json` typography block overrides the CE default when present.
- **Local n-gram example references** - bundled `references/examples/n-gram-table-examples.md` as the quality-anchor set. If missing or empty, fall back to the in-skill reference tables in `## INTERNAL` - do not block.

#### Tools the skill calls

This skill runs locally in Claude Code and calls its tools directly - it assumes they exist and uses them in this priority order. On a tool error, it skips that source and degrades to the next; it never probes for availability first.

- **Local filesystem read** - for an auto-detected entity-map at the canonical Desktop path `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/01-entities/entity-map.json`, and a local content plan at the per-client Topic Plan slot. Fastest path; no Drive round-trip.
- **`gws drive`** (or `mcp__claude_ai_Google_Drive__*` connector) - for the matching-scope entity map, clusters file, optional keyword research, the content plan, and the Case Engine Branding folder from the shared Drive.
- **`mcp__ce-services__rag_query`** - for SEO / methodology grounding when calibrating question quality.
- **User-supplied materials** in the greeting (pasted entity sets, dropped files) and user interview for hard requirements still missing - the always-available floor.
- **Hard requirement** - the matching-scope entity map must resolve via local read or Drive. If neither resolves it, the skill stops and routes to `/pod-1A-entity-research`.
- **Behavior on a tool error** - skip that source and degrade to the next. With no reachable source, fall through to user-supplied + interview; flag every Inferred value with `> NEEDS CONFIRMATION:` per Sourcing discipline.

### Outputs

What is?
The artifacts this skill ships - the 3-format trio (a machine-readable JSON sidecar, a markdown source-of-truth, and a human-facing Google Doc) plus a `metadata.json` provenance file - landing in the topic's `N-Gram Tables/{Topic}/{Episode}/{Scope}/` Drive folder, mirrored to the local Desktop path.

#### Output formats

CE-wide default: every persistent artifact ships in three formats.

- **JSON** - `n-gram-table.json` - structured / machine-readable sidecar for downstream programmatic consumption (pod-3A-ros-template and pod-3B-client-ros read this). The JSON has three top-level members: a `content` block (the n-gram table itself - `rows`, `scope`, `location`, `row_count`, `entities_per_row_avg`, `dedup_merges`, `localization_scan_result`), a `research_summary` text field (the generated plain-language Executive Summary lead paragraph), and an `internal` block. The `internal` block carries the four review-tier blocks that DO render under the Doc's bottom `INTERNAL` H1 - `cluster_architecture`, `topic_entities`, `local_anchors`, `bridge_entity_coverage` (in that locked order) - plus the provenance / metadata fields (`topic`, `industry`, `jurisdiction`, `episode`, `version`, `created`, `parent_anchor`, `skill`, run provenance) which by contract NEVER render. The `content` block, `research_summary`, and the four `internal` review-tier blocks render into the client-facing Google Doc; the `internal` provenance / metadata fields do not. Schema in `references/schema/n-gram-table.json`.
- **Markdown** - `N-Gram Table.md` - local source-of-truth mirror. Retains the `## INTERNAL` block. Lives on disk under the local mirror path below.
- **Google Doc** - `N-Gram Table` - human-facing canonical view at the Drive destination below. Created / updated in-place via `files.update` against a stable fileId so the URL never breaks for downstream links. Branded per the Case Engine Branding folder (see `## Ship -> ### How it ships`). Typeface: Roboto for every text element (body, headings, table cells, captions), applied via `batchUpdate` `updateTextStyle` with `weightedFontFamily.fontFamily = "Roboto"` over the full document range as the final pass before sharing. Override only when a per-client `brand.json` typography block specifies otherwise.

A `metadata.json` provenance file ships alongside the trio (internal-only, not a client-facing artifact - records sources, counts, dedup + scan results). The internal metadata header line (the pipe-delimited `Topic: ... | Industry: ... | Jurisdiction: ... | Episode: ... | Version: ... | Created: ... | Parent anchor: ... | Skill: ...` line) is INTERNAL provenance - it lives in `metadata.json` and the JSON `internal` block, and is EXCLUDED from the client-facing Google Doc entirely (not in the body, not under the bottom INTERNAL section).

#### What ships

- **`n-gram-table.json`** - JSON - machine-readable, downstream-consumed; `content` block (full 4-column row set + scope + location + counts + dedup merges + localization scan result) + `research_summary` + `internal` block (the four review-tier blocks `cluster_architecture` / `topic_entities` / `local_anchors` / `bridge_entity_coverage`, plus provenance: topic / industry / jurisdiction / episode / version / created / parent anchor / skill).
- **`N-Gram Table.md`** - Markdown - local source-of-truth mirror, retains the `## INTERNAL` block.
- **`N-Gram Table`** - Google Doc - human-facing canonical view, branded cover page, Roboto typeface, stable fileId.
- **`metadata.json`** - JSON (internal) - provenance: sources, final row count, dedup merges, localization scan result, references status.

#### Drive destination

Shared drive root: `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`). N-Gram Tables live in their own dedicated `N-Gram Tables/` folder (id `1gATbaPKlcwGBLkStF5d2l68Y-qyLkqYE`), organized by topic, then episode, then scope. This replaces the old `Episode Templates/{Topic}/{Episode}/{Scope}/03 N-Gram Table/` destination.

This destination is enforced by the **Canonical destination gate** in `### Quality gates` (hard, pre-write). The four artifacts NEVER live in a client episode delivery folder - the dedicated `N-Gram Tables/` research library is the only valid write target.

```
N-Gram Tables/{Topic}/{Episode}/{Scope}/
  N-Gram Table.md                        source of truth (markdown)
  N-Gram Table                           Google Doc (in-place files.update)
  n-gram-table.json                      machine-readable, downstream-consumed
  metadata.json                          sources, counts, dedup + scan results
  _archive-{YYYY-MM-DD}/                  (if this folder had prior content)
```

The `{Scope}` segment resolves per scope:

| Scope | `{Scope}` path segment |
|---|---|
| Topic Only | `Topic Only/` |
| Location | `Locations/{Location}/` |
| Extension | `Extensions/{Location}/` |

Location naming matches exactly, no colons, dashes only: `CA`, `CA - Los Angeles County`, `CA - Long Beach`. No Topic-level n-gram tables - the table is always episode-specific. The Drive destination is fixed - this skill does not move existing Drive data.

#### Local mirror

`~/Desktop/claude_code/deliverables/podcast/N-Gram Tables/{Topic}/{Episode}/{scope}/` - holds the same `N-Gram Table.md`, `n-gram-table.json`, and `metadata.json`. `{scope}` = `Topic Only`, `Locations/{Location}`, or `Extensions/{Location}` to mirror the Drive scope convention. The mirror enables fast local iteration, downstream local skill consumption (pod-3A-ros-template reads from here when running locally), and offline review. Written on every run.

#### Schema

`references/schema/n-gram-table.json` - the canonical JSON schema `n-gram-table.json` validates against. The schema enforces three top-level members: a `content` block (the n-gram table - `rows` array each with `question_text` / `ngrams` / `entities` / `predicates`, `scope`, `location` conditional, `row_count`, `entities_per_row_avg`, `dedup_merges`, `localization_scan_result`), a `research_summary` text field (the generated Executive Summary lead paragraph), and an `internal` block. The `internal` block carries the four review-tier blocks - `cluster_architecture` (pillar -> Q-refs), `topic_entities` (grouped-by-type universal entities), `local_anchors` (grouped-by-type jurisdiction entities; empty object `{}` at Topic Only scope), `bridge_entity_coverage` (bridge entity -> Q-refs) - plus provenance / metadata (`topic`, `industry`, `jurisdiction`, `episode`, `version`, `created`, `parent_anchor`, `skill`, run provenance). The `content` block, `research_summary`, and the four `internal` review-tier blocks render into the client-facing Doc; the `internal` provenance / metadata fields never render. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed - do not block on a missing schema.

#### Sections - locked Doc order

The client-facing Google Doc renders in this exact order, every run:

1. **Branded cover page** - rendered per the Case Engine Branding `Cover Page Layout.png` reference (CE logo, title, subtitle, client name, "Prepared by Case Engine").
2. **Executive Summary** - structured as: section heading -> a GENERATED plain-language narrative paragraph (the research summary - what this run's research found, which entities and themes dominate, the jurisdictional picture, what the episode should emphasize; client-facing, jargon-free) -> the stat bullets (row count, entities/row average, dedup merges, localization scan result). The narrative paragraph is the LEAD of the Executive Summary, not a separate section.
3. **Methodology** - static hard-coded text, identical every run (see `## Ship -> ### How it ships`).
4. **Four-column collation table** - Question Text | N-grams | Entities | Predicates, all rows, with the CE-blue header row, rendered compact to target roughly 2 pages.
5. **Table explainer** - one hard-coded 1-2 sentence line immediately below the table (see `## Ship -> ### How it ships`).
6. **INTERNAL section** - an H1 heading `INTERNAL` colored CE brand blue at the bottom of the Doc. Holds the review-tier blocks in a LOCKED four-block order:
   1. **Cluster Architecture** - the thematic pillars (short lead block: each pillar mapped to its question numbers).
   2. **Topic Entities** - the universal, practice-area entities (accident types, injury types, legal standards / statutes, damages concepts, agencies - the non-local entities), grouped by type: a bold sub-label per type with a bullet list of entries beneath. Always present, every scope.
   3. **Local Anchors** - the jurisdiction-specific entities, grouped by type with the identical bold-sub-label + bullet-list format (Roads/Highways, Law Enforcement, Medical Providers, Courts, County). Heading is just `Local Anchors` (no jurisdiction prefix). Present only at Location/Extension scope; omitted entirely for Topic Only.
   4. **Bridge Entity Coverage** - the cross-cutting bridge entities mapped to question numbers (entity -> Q-ref map).
   Topic Entities and Local Anchors use the identical grouped-by-type format. Localization notes render under the INTERNAL section when scope is Location/Extension.

#### Sections EXCLUDED (never in the client-facing artifact, even under INTERNAL)

- `## Quality Assurance` and everything from that heading onward
- The verbatim reference prompt (internal calibration only)
- Known Gaps, Handoff Contract, provenance block, source inventory
- **The internal metadata header line** - the pipe-delimited `Topic: ... | Industry: ... | Jurisdiction: ... | Episode: ... | Version: ... | Created: ... | Parent anchor: ... | Skill: ...` line. It is internal provenance and lives in `metadata.json` and the JSON `internal` block ONLY. It is EXCLUDED from the client-facing Google Doc entirely - not in the body, not under the bottom INTERNAL section heading. Every n-gram Doc renders clean - no pipe-delimited metadata line anywhere.

Two-tier model: the bottom `INTERNAL` H1 section of the Doc carries the four review-tier blocks (Cluster Architecture, Topic Entities, Local Anchors, Bridge Entity Coverage) so a human can audit entity coverage; the QA / process / provenance content and the metadata header line are internal-tier - they live only in the local markdown mirror, `metadata.json`, and the JSON `internal` block, never in the Doc. The Google Doc renderer truncates the markdown source at the first `## Quality Assurance` heading and strips the internal metadata header line before rendering. See `## INTERNAL` for the grep test.

#### Write destinations

Both destinations are written every run. On a write error to one, the skill ships to the other and surfaces the partial state in the report - it does not silently lose the deliverable.

- **Drive** - `gws drive` (or `mcp__claude_ai_Google_Drive__*` connector) - writes the markdown, the Google Doc, the JSON, and metadata into the `N-Gram Tables/{Topic}/{Episode}/{Scope}/` Drive folder.
- **Local mirror** - local filesystem write to the local mirror path, alongside the Drive write.
- **Behavior on a write error** - if one destination errors, ship to the other and report the partial state. If both error, hard-fail with a clear message; do not silently lose the deliverable.

#### Examples

`references/examples/n-gram-table-examples.md` - single doc with GOOD / BAD / EDGE CASE labeled sections per CE convention. Read 1-2 examples matching the requested scope as calibration before generating. If the folder is empty, proceed on the in-skill reference set in `## INTERNAL` alone and flag `"references": "empty"` in `metadata.json`.

#### Routing

- **Upstream (required, hard dependency):** `/pod-1A-entity-research` - matching-scope entity map.
- **Upstream (soft prerequisite):** `/pod-2A-topic-planner` - the content plan (= topic plan). The skill checks for it and asks before proceeding if it is missing.
- **Downstream (required):** `/pod-3A-ros-template`, `/pod-3B-client-ros`, and `/pod-3C-client-guide` all consume this table directly or transitively.
- **Refresh:** re-run with the same episode + scope (routes to `## Update`).

#### Handoff Contract

This skill produces the following for downstream consumers:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| `n-gram-table.json` (`content` block) | `/pod-3A-ros-template`, `/pod-3B-client-ros` | Full 4-column row set (Question Text, N-grams, Entities, Predicates); row count; per-row entity stack; `content.scope` + location; dedup merges |
| `metadata.json` | (not consumed downstream) | Internal provenance - sources, final row count, dedup merges, localization scan result, references status |
| `N-Gram Table` / `N-Gram Table.md` | `/pod-3A-ros-template` (human-readable reference) | Visible only; machine consumers use the JSON |

Downstream consumers can rely on: the Google Doc URL is stable for the lifetime of the table (preserved via `files.update` across re-runs); `n-gram-table.json` validates against `references/schema/n-gram-table.json` with the `content` / `internal` two-block split; every entity in the Entities column traces to the matching-scope entity map. Upstream pulls (hard dependency): `entity-map.json` and `entity-clusters.md` from `/pod-1A-entity-research` at the scope-matched Entity Research folder. The skill refuses to run without the entity map.

### Framing

The N-Gram Table is the episode's content backbone, not a finished script. It is a machine-readable planning artifact: a structured 4-column set of questions and their supporting n-grams, entities, and predicates that downstream Run of Show skills turn into a host script and attorney bullets. It is never narrative prose, never a listicle, and never a substitute for a localized entity map.

**Geo model (three fields - use these exact labels).** Every episode this skill builds sits inside a three-field geo model, resolved once per client and inherited here:

1. **Targeting strategy** - `single-location` vs `multi-location`. Does the firm serve/rank one city or several? Drives episode format (Greeting Q5): single-location -> Full episodes (~20 questions); multi-location -> one Mini episode per target city (10-12 questions, internal scope label stays `Extension`), no single primary episode.
2. **Optimization scope (show anchor)** - City / State / County / Regional. What the podcast *as a whole* is optimized to rank for - the show-wide breadth the entity and keyword research was gathered at (Greeting Q2). A multi-location firm usually anchors at State or Regional to own the whole footprint; a single-location firm anchors at City. This is the breadth of the research corpus this table draws from, NOT the city any one episode targets.
3. **Episode geo target** - the specific city THIS episode's table is built to rank for. This is what the `Location` / `Extension` scope of the table resolves to (Greeting Q4). In multi-location the show anchors broad (e.g. the state) while each episode targets a different city (one for Denver, one for Aurora, one for Centennial); in single-location every episode shares the one anchor city.

**Mapping the scope labels to the model:** the table's `Location` / `Extension` scope = the **Episode geo target** (the one city this table emphasizes); the **Optimization scope (show anchor)** is the show-wide breadth the upstream entity/keyword research was gathered at. `Topic Only` scope carries no episode geo target - it is the jurisdiction-agnostic layer.

**The rule - anchor scope != per-episode target.** The show can be optimized for a broad scope (e.g. the whole state) while each episode targets a specific city we're trying to rank for. Research runs at the anchor breadth; each episode's questions/titles emphasize that episode's target city naturally - a ceiling, never a forced quota (see Editorial Guideline 4). Getting this wrong is how a multi-location statewide firm ends up with episodes that all sound like one city, or how city emphasis silently becomes a city floor. THIS skill is the enforcement point: proper topic mix plus state-breadth-with-city-emphasis is realized in the questions built here.

### Quality bar

What "good" looks like - the pass / fail intuition.

- Four columns exactly, in order: Question Text, N-grams to Mention, Entities to Mention, Predicates to Mention. No more, no fewer.
- Row count meets scope: Topic Only 25-35, Location 25-35 (push to the upper end where the jurisdictional stack gives more surface area), Extension 10-12 (intentionally tighter - do not pad; this is the Mini episode table under a multi-location strategy, and the per-city extension under the legacy anchor model).
- Questions read like a natural on-air podcast arc - broad to procedural to deep/expert - distributed across all major subtopics, no clumping, no listicle phrasing.
- Every entity traces to the matching-scope entity map. No invented entities, no reaching outside the map's scope.
- When scope is Location or Extension, every entity is localized - generic categories are a hard fail (see `### Quality gates` -> localization scan).
- No two questions produce more than 30% answer overlap (see `### Quality gates` -> dedup).
- No em dashes, no banned vocabulary - the Anti-AI Detection scan fires before publish.

### Sourcing discipline

The Confirmed / Inferred / Unknown three-state pattern. Never block, always ship, never silent. The table still ships when data is incomplete; gaps surface in `## INTERNAL` or with `> NEEDS VERIFICATION:` blocks.

- **Confirmed** - claim traces to a specific source. Every entity pulled verbatim from the matching-scope entity map is Confirmed. Ship as-is, no marker.
- **Inferred** - sensible default applied when the source is insufficient (e.g., a question-arc ordering chosen because the entity clusters file was absent). Ships with `> INFERRED: {what + why}` flag.
- **Unknown / NEEDS CONFIRMATION** - no source AND no defensible default. Ships with `> NEEDS CONFIRMATION: {what's missing}` block, never silently synthesized. An entity that belongs but is not in the map is NEEDS CONFIRMATION - refresh the entity map, never invent it here.

### Editorial Guidelines

Cross-cutting content rules for the table. The SOP points back here; the rules live here once.

**Guideline 1 - Localized entities only when scope is Location/Extension.**

- **Banned:** generic, unqualified entity categories when scope is Location or Extension - `Police Department`, `Sheriff's Office`, `Insurance Company`, `State Bar Association`, `Civil Court`, `District Court`, `Superior Court` (unqualified), `Hospital` (unqualified), `Department of Motor Vehicles`, `Department of Transportation`, `Department of Insurance`, `Highway Patrol` (unqualified).
- **Allowed:** the localized instance from the entity map at matching scope - `Houston Police Department (HPD)`, `Harris County Civil Courts`, `Memorial Hermann Hospital System`, `Texas Department of Insurance (TDI)`. Generic categories are acceptable ONLY when scope is Topic Only.
- **Why:** the entity map was already localized at Research Step 2. A generic category in a localized table is a localization leak - it produces non-localized downstream scripts and erases the jurisdictional authority signal the episode is built on.
- **Where it fires in the SOP:** `## Create -> ### Run the localization scan`, and the localization scan in `### Quality gates`.

**Guideline 2 - Questions are open and exploratory, never listicle.**

- **Banned:** listicle phrasing - "list 5 things...", "what are 10 ways...", "name the top reasons...".
- **Allowed:** natural, conversational, open questions a co-host would ask on air - "What should I do immediately after a car accident to protect my claim?", "How does California's comparative fault rule affect my recovery?".
- **Why:** the table feeds a podcast Run of Show, not a blog post. Listicle questions produce mechanical, enumerated answers that break the on-air conversational arc.
- **Where it fires in the SOP:** `## Create -> ### Generate questions`.

**Guideline 3 - Firm / attorney / podcast names are NOT entities.**

- **Banned:** placing the firm name, attorney names, or the podcast name in the Entities column.
- **Allowed:** real-world named organizations, agencies, statutes, and institutions only - the kind that get cited as authority, not the kind that get underlined as the host.
- **Why:** firm / attorney / podcast names are underlined at populate time (Client ROS, Run of Show Step 3), not treated as authority entities here. Mixing them into the Entities column corrupts the downstream entity stack.
- **Where it fires in the SOP:** `## Create -> ### Map n-grams, entities, predicates`.

**Guideline 4 - Geo in question phrasing: natural placement, no city quota.**

This guideline is where the geo model's **Episode geo target** (see `### Framing`) gets realized in the question text - and it is the enforcement point for **anchor scope != per-episode target**. The upstream research was gathered at the **Optimization scope (show anchor)** breadth (e.g. the whole state); the questions here emphasize THIS episode's target city. City emphasis is a ceiling, NEVER a floor - never force-feed the city to hit a quota. A multi-location statewide firm must NOT end up with every episode sounding like one city, and city emphasis must NEVER silently become a city floor.

- **Rule:** at Location/Extension scope the table must READ as a local show - the city is present and grounding - WITHOUT being stamped onto every line. Aim for the city to land naturally in roughly a THIRD of the questions (a soft center of gravity, not a quota): enough that a listener immediately knows this is a [City] show, never so much that it reads as keyword spam. The city belongs where it falls naturally - the local market, a named local actor, a venue, "here in Glen Burnie", "which Columbia courthouse handles...". The remaining ~two-thirds carry locality through named local entities (the corridor, the county court, the trauma center, the local agency) or stay geo-neutral - both are fine. HARD CEILING: the city in more than HALF the questions reads as spam and FAILS. GUARD THE OTHER WAY TOO: a table where the city is essentially absent is too thin - it must still read as local. Any question whose substance is state law NAMES the state ("Florida's 14-day PIP rule") and does not get a city token bolted on - that is not a city mention. The county appears only where it earns its place (the court sits there, a county agency is the actual actor). Locality is reinforced by the localized ENTITY stack (Guideline 1) running through every row, not by the city token alone - so the non-city questions still signal local authority.
- **Banned:** the city token in most or every question (reads as keyword spam, not authority); the adjective-spam construction where the city is bolted onto a generic noun ("a Stuart claimant", "a Stuart crash", "Stuart drivers") instead of placed naturally ("after a crash in Stuart", "here in Stuart"); county-first or state-first phrasing as the default pattern; padding county mentions into rows to look localized; forcing the city in to satisfy any quota.
- **Allowed:** "What should a Glen Burnie parent expect..." (city placed naturally, where it fits); "Which courthouse handles a Columbia divorce..." with the county court named because that is the real venue; "Maryland's mutual consent divorce" (state law named as state law, no city token forced on); fully geo-neutral questions ("What should I do immediately after a crash to protect my claim?") - these are normal and should be the majority.
- **Why:** the deliverable targets a city market, but a table that tags the city onto question after question reads as keyword spam, not local authority - and it buries the state-law substance that actually answers the searcher. The city is the anchor, not a per-line tax. Question lines become chapter titles, show notes, and clip captions, so saturating them with the city name is the single most visible failure mode. The earlier 60-70% city floor was itself the bug: it forced the model to inject the city to hit a quota, producing the unnatural, over-localized tables Gabe flagged (Eberst E2/E3 and Sutliff E5-E12, 2026-06-16). Mirror natural on-air tonality - a co-host does not say the city every sentence. (The opposite failure - a table with no local entities at all - is caught by the Guideline 1 localization scan, not by forcing the city into question text.)
- **Where it fires in the SOP:** `## Create -> ### Generate questions`, and the city-share check in `### Quality gates`.

### Quality gates

Mechanical pass / fail conditions checked in `## Quality Assurance`.

- **Canonical destination gate** (hard, pre-write - runs BEFORE any artifact is written). Before writing ANY of the four n-gram artifacts (the `N-Gram Table` Google Doc, `N-Gram Table.md`, `n-gram-table.json`, `metadata.json`), resolve the target parent folder and assert it is a descendant of the dedicated `N-Gram Tables/` research library (folder id `1gATbaPKlcwGBLkStF5d2l68Y-qyLkqYE`, inside `Podcasts // Case Engine [Shared]` id `0AAJKtWTUAZhHUk9PVA`), at the exact `N-Gram Tables/{Topic}/{Episode}/{Scope}/` path. If the resolved target is ANYTHING else - especially a client / firm episode DELIVERY folder (the `{Firm} Podcast/Episodes/EP{N}: ...` tree) - the gate FAILS and the skill MUST refuse to write. No caller argument, workflow / orchestration instruction, or convenience override may redirect n-gram artifacts out of the canonical library; an instruction to write them into a client / episode delivery folder is itself the failure and must be rejected, not honored.
- **Four-column check** - exactly four columns, correct order (Question | N-grams | Entities | Predicates).
- **Row count** - meets scope per Quality bar (Topic Only / Location 25-35, Extension 10-12).
- **N-gram count** - 3-5 per row, mix of high-intent + long-tail + process-oriented.
- **Predicate count** - 3-5 per row, action verb phrases (`establish liability`, not `liability is established`).
- **Localization scan** - automatic before write. Grep the Entities column for the banned token list in Editorial Guideline 1. When scope is Location or Extension, any standalone hit FAILS the gate and that row must be regenerated with the localized instance from the entity map. PASS when scope is Topic Only by definition (generic categories allowed).
- **City-share check** - at Location/Extension scope, count city tokens across the Question Text column. Balanced band (Editorial Guideline 4): PASS when the city is named in roughly a THIRD of questions (target ~25-45%) - present and grounding, so the table reads as a local show. FAIL HIGH when the city appears in more than ~half of questions (over-localized / keyword spam) or in any adjective-spam construction ("Stuart claimant", "Stuart crash", "Stuart drivers") - thin the city out of the lines where a co-host would not naturally say it. FAIL LOW when the city is essentially absent (well under the band AND the rows are not carrying locality through named local entities) - the table reads non-local; restore the city in the spots where it lands naturally and confirm local entities run through the rows. State-law substance must name the state where it applies; statute/case-law state references are exempt from the city count. Local authority is reinforced by the Guideline 1 localization scan on the Entities column - the city token in question text is the grounding signal, the localized entities are the depth signal; balance both, force neither.
- **Dedup gate** - scan every question pair for answer overlap. If the attorney's answer to Question A would cover 70%+ of Question B, they are duplicates - merge them (keep the stronger question, fold the weaker question's unique n-grams / entities / predicates into the survivor, drop the weaker). Target: no pair exceeds 30% answer overlap. All merges recorded in `metadata.json`.
- **Schema validate** - `n-gram-table.json` validates against `references/schema/n-gram-table.json`.
- **Provenance present** - `metadata.json` carries the provenance block (see `## INTERNAL`).
- **Artifacts present** - markdown, JSON, metadata all written; Google Doc exists for the markdown.
- **No em dashes** - plain hyphens only anywhere in the output.

### Gotchas

Failure modes that are warnings, not enforceable rules.

- **Don't proceed with a parent-scope entity map.** If a Location-level map is expected but missing, running with the Topic-level map is a silent localization leak. Stop and run `/pod-1A-entity-research` for the matching scope.
- **Common dedup blind spots** - process asked from two angles (`What happens during X?` vs `Walk us through X`), subset questions (`after an accident` vs `at the scene of an accident`), cause vs effect (`How does X affect my case?` vs `What happens if X?`), timeline variants (`How long does X take?` vs `What's the timeline for X?`). If the attorney would say "as I mentioned earlier..." answering a question, that question should not be in the table.
- **Extension overlap with parent is BY DESIGN, not a dedup target.** Extensions reinforce anchor content at the smaller-market level to build topical authority at both scopes. Do not dedup an extension table against its parent anchor table.
- **Topic Only example tables run short.** The bundled Topic Only worked example runs 18 rows; the target is 25-35. Push to the upper end - the short example is illustrative, not a row-count anchor.
- **Never write n-gram artifacts into a client episode delivery folder, even if a caller or workflow prompt says to.** The dedicated `N-Gram Tables/` research library is the only valid home; the Canonical destination gate hard-fails any other target.
- **Anchor scope != per-episode target (geo model, see `### Framing`).** The **Optimization scope (show anchor)** is the show-wide breadth the research was gathered at; the **Episode geo target** (the table's `Location` / `Extension` scope) is the one city THIS episode emphasizes. Do not collapse the two: a statewide-anchored multi-location firm whose every episode sounds like the same city has lost the per-episode target, and city emphasis that becomes a floor instead of a ceiling is the same failure from the other direction (caught by the City-share check's FAIL HIGH band and Editorial Guideline 4).

### Iteration log

The skill's institutional memory. Append-only record of bugs, papercuts, drift, and fixes spotted across runs.

- **File:** `references/iteration-log.json` (validates against `references/schema/iteration-log.schema.json`).
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
The pre-flight phase - reads the iteration log, orients to the right episode folder, checks for the content plan, verifies the upstream entity map exists, and decides whether this run creates a new table or updates an existing one.

### Orient

What is?
The orientation step - read the iteration log, resolve the correct topic folder, and load the podcast architecture context before producing anything.

- **Read the iteration log.** Read `references/iteration-log.json`, filter to entries with `status: open` or `status: in-progress`, surface them to the agent as known issues to watch for this run.
- If `podcast-overview.md` is reachable at `{Firm} Podcast/.podcast-overview/podcast-overview.md`, read it and auto-fill Greeting questions 1-3 (anchor scope, extension cities, client name); confirm in one line. Otherwise ask the Greeting questions.
- Resolve the destination folder under `N-Gram Tables/{Topic}/{Episode}/{Scope}/` (folder id `1gATbaPKlcwGBLkStF5d2l68Y-qyLkqYE`). If the topic / episode subfolders do not exist yet, create them per the destination convention.
- Read `references/examples/n-gram-table-examples.md` and pick 1-2 examples matching the requested scope as quality anchors. If the file is empty, proceed on the `## INTERNAL` reference set alone and flag `"references": "empty"` in `metadata.json`.

### Check for content plan

What is?
The soft-prerequisite gate - resolve whether a content plan (= topic plan, the `pod-2A-topic-planner` output) already exists for this client, and ask the user before proceeding when it does not.

**CANONICAL SOURCE (hard rule).** The SINGLE source of truth for the episode lineup and each episode's topic/title is the PUBLISHED Google Doc Topic Plan in the client Topic Plan slot - the client sees that Doc and makes manual adjustments to it, so it is authoritative. NEVER take the episode or its topic from a local `topic-plan-v{n}.md`/`.json` or any cached/older file; those are stale mirrors that drift from the Doc. Resolve the episode and its topic from the live Google Doc and confirm it matches before building. If a local file disagrees with the Doc, the Doc wins. Do NOT build a topic that is not in the Doc's lineup. (Why: a divergent local v3 md once swapped E5 to a topic the firm does not even handle - Eberst slip-and-fall, 2026-06-19 - and produced an entire wrong episode before anyone caught it.)

- "Content plan" and "topic plan" are the SAME artifact. Auto-resolve it from the per-client Topic Plan slot `{Client Folder}/AEO/Podcast/Topic Plan/Topic Plan: {practice_area} // {client_name}/`. A `topic-plan-v{n}.json` or `topic-plan-v{n}.md` artifact in that slot means a content plan exists. Check that slot first.
- **Found:** use it as the episode-selection context (which episode this table is for, where it sits in the episode arc); log `content_plan: found` + the resolved path in `metadata.json`; proceed.
- **Not found AND not explicitly provided by the user:** STOP and ask: "I don't see a content plan (topic plan) for this client at the Topic Plan slot. Do you want me to (a) run `/pod-2A-topic-planner` first to build it, or (b) proceed without it for just this episode?" Do not silently invent an episode plan. Log `content_plan: not_found` and the user's choice in `metadata.json`.
- There is no separate content-plan folder or template - the Topic Plan slot is the single source. Do not invent one.

### Verify upstream entity map

What is?
The hard-dependency gate - confirm the matching-scope entity map exists before any table generation, and refuse to run on a parent-scope map.

- Resolve `entity-map.json` at the matching scope. Try the local Desktop path first (`~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/01-entities/entity-map.json`), then fall back to Drive at the scope-matched `templates [master]/AEO/Podcast/Entity Research/{Topic}/{Scope}/entity-map.json`. Log `entity_map_source: local | drive` in `metadata.json`.
- Also read `entity-clusters.md` from the same folder when present.
- If the entity map is missing at the matching scope, STOP and route the user to `/pod-1A-entity-research`. Do not substitute a parent-scope map (Gotchas - localization leak).
- **Handoff Contract check.** Verify upstream paths match the declared Inputs. If `keyword-research.json` or any other undeclared upstream file shows up and is under consideration, STOP and ask: "I see upstream output at {path} but my Inputs contract doesn't declare it as required. Should I (a) mine it as seed questions, (b) skip it, or (c) pause while you update the handoff contract?" Do not guess silently.

### Existence check

What is?
The mode router - decide whether this run creates a new table or updates an existing one based on whether the resolved `N-Gram Tables/{Topic}/{Episode}/{Scope}/` folder already has content.

- Look for an `N-Gram Table` Google Doc + `n-gram-table.json` inside the resolved scope folder.
- **Missing:** no prior artifact - route to `## Create`.
- **Found:** surface provenance (existing `metadata.json` run date, row count) and ask: refresh in place / archive-and-rebuild / cancel.
  - Refresh in place -> route to `## Update`.
  - `archive-and-rebuild` (or the refresh flag passed at invocation) -> move prior content to `_archive-{YYYY-MM-DD}/` and route to `## Create`.

## Prepare Inputs

What is?
The input-preparation phase - load and validate the entity map, clusters, and any seed-question source into a working set ready for the Create or Update phase.

Work through the input sources in priority order; on a tool error, skip that source and degrade to the next.

- **Load the entity map.** Parse `entity-map.json` from the source resolved in Checks. Confirm it carries the localized entity set at the matching scope (Topic Only generic categories, or the localized jurisdictional stack for Location/Extension).
- **Load entity clusters.** Parse `entity-clusters.md` when present - the clusters seed question grouping so the episode arc covers all major subtopics without clumping.
- **Load the content plan.** If the content-plan check found a topic plan, parse it for the episode-selection context (which episode, position in the arc).
- **Load seed questions (optional).** If the Handoff Contract check approved mining `keyword-research.json`, parse the PAA stacks as seed questions.
- **Resolve branding.** Read the Case Engine Branding folder (id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`) - logo, `colors.md` (CE blue hex for the table header row), fonts, `Cover Page Layout.png`. Hold the resolved values for the `## Ship` render. A per-client `brand.json` typography block overrides the CE default when present.
- **Load calibration examples.** Hold the 1-2 scope-matched examples from `references/examples/n-gram-table-examples.md` (or the `## INTERNAL` reference tables) as quality anchors for the Create phase.

## Create

What is?
The create branch - builds the 4-column collation table from scratch when no prior table exists, producing a localized, deduped, schema-valid `n-gram-table.json` plus its markdown and metadata.

**Best Practices.**
These apply to the entire create phase and should be checked after each step.

- Entities come from the matching-scope entity map only - never invent entities to fill gaps (see Sourcing discipline + Editorial Guideline 3).
- Hold the scope-matched calibration examples in view while generating - calibrate row count, question cadence, and entity density against them.
- Row count, question phrasing, n-gram mix, and predicate form follow `### Quality bar` and `### Editorial Guidelines` - do not restate the thresholds, apply them.

If the model generates output that violates any of these, emit a `> NEEDS VERIFICATION:` block at the offending location instead of shipping the claim.

### Generate questions

What is?
The pass that produces the Question Text column - natural, conversational, on-air questions that flow as a logical podcast arc across all major subtopics of the episode.

- Generate questions for the scope's row count (Topic Only / Location 25-35, Extension 10-12 - see `### Quality bar`).
- Phrase every question per Editorial Guideline 2 - open and exploratory, never listicle.
- Place geo per Editorial Guideline 4 - balanced. The table must read as a local show: name the city naturally in roughly a THIRD of questions (present and grounding), let the rest carry locality through named local entities or stay geo-neutral. Never the city on more than half the lines (spam), never essentially absent (too thin). Read each line aloud - keep the city where a co-host would say it, drop it where they would not.
- Order the questions broad -> procedural -> deep/expert so the table reads like a podcast arc.
- Distribute questions across all major subtopics using the entity clusters when available; no clumping.
- **Extension scope, parent anchor exists (legacy anchor+extension model):** do NOT generate new questions from scratch. Select the 10-12 strongest questions from the parent anchor n-gram table and re-angle them for the extension's local context. Overlap with the parent is by design.
- **Extension scope, NO parent anchor (multi-location Mini strategy):** generate the 10-12 questions from the layered research directly. Composition weighting blends the state-level demand with a bias toward the target location: city-specific signals (keywords, entities, local anchors) come first and set the priority; then weave in the strongest STATE-level questions (the high-demand statewide search/PAA topics) so the Mini still captures statewide intent; draw down to the Topic Only layer only when both are thin. State statutes and case law are always correct to weave in - they are set at the state level. The net mix is location-biased but state-blended: the best statewide questions make the cut, re-angled to the target city's context. Note the thin-geo draw-down in the research_summary when it happens. When the SAME topic ships Minis for multiple cities, the cities' tables must not overlap verbatim - partially different question mixes, shared legal ground reworded per city.

### Map n-grams, entities, predicates

What is?
The pass that fills the remaining three columns - 3-5 n-grams, the localized entity stack, and 3-5 action-verb predicates per row, all drawn from the matching-scope entity map and directly relevant to each question.

- **N-grams** - 3-5 per row, directly relevant to the question; a mix of high-intent (how someone searches), long-tail (specific scenarios), and process-oriented (workflow).
- **Entities** - real-world named organizations only, every one pulled from the matching-scope entity map. Per-row count, acronym convention, and separator follow the Localization table in `## INTERNAL`. Firm / attorney / podcast names are NOT entities (Editorial Guideline 3).
- **Predicates** - 3-5 per row, action verb phrases describing what a practitioner does (`establish liability`, not `liability is established`; `calculate break-even point`, not just `calculate`).
- Each question must lead naturally into its n-grams and predicates.

### Run the localization scan

What is?
The gate that catches localization leaks - grep the Entities column for generic unqualified tokens and regenerate any offending row with the localized instance when scope is Location or Extension.

- Run the localization scan per `### Quality gates` - grep the Entities column for the banned token list in Editorial Guideline 1.
- When scope is Location or Extension, any standalone hit fails the scan - regenerate that row with the localized instance from the entity map.
- When scope is Topic Only, the scan passes by definition (generic categories are allowed).
- Record the localization scan result (PASS / FAIL + rows regenerated) for `metadata.json`.

### Dedup pass

What is?
The pass that merges overlapping questions - scan every question pair for answer overlap and fold any pair above 70% into a single stronger survivor.

- Run the dedup gate per `### Quality gates` - scan every question pair for answer overlap.
- For any pair where the attorney's answer to Question A would cover 70%+ of Question B: keep the stronger question (more specific n-grams, better entity coverage, more distinct angle), fold the weaker question's unique n-grams / entities / predicates into the survivor, drop the weaker question.
- Target: no pair exceeds 30% answer overlap.
- **Extension scope:** dedup within the extension table only - never dedup an extension table against its parent anchor table (Gotchas - overlap with parent is by design).
- Record every merge (which questions, which survivor) for `metadata.json`.

### Render markdown

What is?
The pass that assembles the final artifacts - the `N-Gram Table.md` source-of-truth with cover + executive summary + methodology + 4-column table + table explainer + the `## INTERNAL` block, the `n-gram-table.json` sidecar, and `metadata.json`.

- Assemble `N-Gram Table.md` in the locked Doc order: title (H1); `## Executive Summary` (heading, then the GENERATED research-summary narrative paragraph as the lead - a few plain-language sentences on what this run's research found, which entities and themes dominate, the jurisdictional picture, what the episode should emphasize, client-facing and jargon-free - then the stat bullets: final row count, generated count, merged count, entities/row average, localization scan result); the static `## Methodology` section (hard-coded text, see `## Ship -> ### How it ships`); the 4-column table; the static table explainer line; localization notes when scope is Location/Extension; then the `## INTERNAL` block (see `## INTERNAL`).
- **Internal metadata header line.** The pipe-delimited `Topic: ... | Industry: ... | Jurisdiction: ... | Episode: ... | Version: ... | Created: ... | Parent anchor: ... | Skill: ...` line is internal provenance - write it into `metadata.json` and the JSON `internal` block, NEVER into the client-facing Doc body or under the bottom INTERNAL section.
- In the table, bold the strongest 1-2 entities per row in the Entities column. When scope is Location/Extension, the localized instance is always one of the bolded entities.
- Serialize `n-gram-table.json` per `### Outputs -> #### Schema`: the `content` block carries the table; `research_summary` carries the Executive Summary lead paragraph; the `internal` block carries the four review-tier blocks (`cluster_architecture`, `topic_entities`, `local_anchors`, `bridge_entity_coverage`, in that locked order - `local_anchors` is an empty object `{}` at Topic Only scope) plus the provenance fields (topic / industry / jurisdiction / episode / version / created / parent anchor / skill).
- Write `metadata.json` with the provenance block per `## INTERNAL`.

## Update

What is?
The update path - modifies an existing N-Gram Table in place when a prior version exists, preserving any manual edits the producer made since the last skill run.

**Best Practices.**
These apply to the entire update phase and should be checked after each step.

- **Diff before write.** Pull the existing `n-gram-table.json` + `N-Gram Table.md`, compare against the proposed new state, surface every changed row before committing the write.
- **Preserve manual edits.** Any question, n-gram, entity, or predicate that was manually edited since the last skill run keeps its current value. The skill never auto-overwrites a manual edit silently.
- **Flag merge conflicts inline.** When a new auto-generated value disagrees with a preserved manual edit, emit `> NEEDS VERIFICATION: auto-generated value [X] conflicts with manual edit [Y]` at the row; the producer resolves.
- **Stable fileId.** Update uses `files.update` against the existing `N-Gram Table` Google Doc fileId. Never create a new Doc; never delete-and-recreate. URL stability is part of the Update contract.

If the model proposes overwriting a manual edit without flagging it, halt and emit `> NEEDS VERIFICATION:` instead of shipping the change.

### Diff against existing

What is?
The pass that loads the prior table and computes a row-level diff against the proposed new state so nothing changes silently.

- Read the prior `n-gram-table.json`, `N-Gram Table.md`, and `metadata.json` from the resolved `N-Gram Tables/{Topic}/{Episode}/{Scope}/` folder.
- Read the prior `metadata.json` provenance block to recover the last run's entity map source, row count, dedup merges, and references status.
- Run the Create-phase passes (`### Generate questions` through `### Dedup pass`) to compute the proposed new state.
- Compute a row-level diff: rows added, rows removed, rows changed (per column), and rows untouched.

### Merge and resolve conflicts

What is?
The pass that merges the new content into the existing table - new rows in, stale rows out, manual edits preserved, conflicts flagged for the producer.

- Apply the phase-level Best Practices: preserve every manually-edited cell; merge new auto-generated rows; drop rows the dedup pass retired.
- Where a new auto-generated value disagrees with a preserved manual edit, emit the `> NEEDS VERIFICATION:` conflict block inline; do not auto-resolve.
- Re-render `N-Gram Table.md`, `n-gram-table.json`, and `metadata.json` per `### Render markdown`. Bump the `metadata.json` run date and append the run to the provenance history.
- The shared `## Quality Assurance` phase runs after this phase - QA does not re-run inside Update.

## Quality Assurance

What is?
The gate before `## Ship` - a three-tier check (Best Practices by name, the hardwired Anti-AI Detection two-pass scan, then skill-specific mechanical checks) that runs after whichever branch fired (`## Create` or `## Update`).

**First - check against Best Practices.** The deliverable must align with the contract defined upstream in this file. This is always the first gate; skill-specific checks come after.

- **Quality bar** (Best Practices -> Quality bar) - four columns in order, row count meets scope, natural podcast-arc questions, every entity traces to the entity map, no em dashes / banned vocabulary.
- **Sourcing discipline** (Best Practices -> Sourcing discipline) - every entity Confirmed against the entity map; any Inferred ordering flagged `> INFERRED:`; any belongs-but-missing entity flagged `> NEEDS CONFIRMATION:`. No silent synthesis.
- **Editorial Guidelines** (Best Practices -> Editorial Guidelines) - Guideline 1 (localized entities only at Location/Extension scope), Guideline 2 (open exploratory questions, no listicle), Guideline 3 (firm / attorney / podcast names are not entities).
- **Quality gates** (Best Practices -> Quality gates) - full checklist must pass: four-column check, row count, n-gram count, predicate count, localization scan, dedup gate, schema validate, provenance present, artifacts present, no em dashes.

**Second - Anti-AI Detection two-pass scan** (canonical doc: https://docs.google.com/document/d/1hp7bxOFRlMhCuhjHNY0j05JrB97-KOFD0XUCQM3gMBU/edit). Mandatory for every text-producing skill. Run the full Section 7 two-pass audit against the deliverable:

- **Pass 1 (mechanical scan):** em-dashes, banned vocabulary (Section 2), banned phrases (Section 3), triadic rhythms and symmetric paragraphs (Section 4), summary-only section closers, date formatting per destination, specific-claims-trace-to-source, no emojis (unless requested), no clickbait.
- **Pass 2 (skeptical re-read):** restart from the top. Did I actually check every line, or skim? Em-dashes I missed? Banned phrases I rationalized? Triadic rhythms left because they "sounded fine"? Generic questions that should be specific? Am I sure?
- **On any hit:** fix and re-run Pass 2 until clean. One pass is not enough.

**Third - skill-specific mechanical checks.**

- `n-gram-table.json` validates against the canonical schema `references/schema/n-gram-table.json`, including the `content` / `internal` two-block split. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed.
- `metadata.json` provenance block present with at minimum: `run_date`, `entity_map_source` (local / drive), `content_plan` (found / not_found), `references_status` (used / empty), upstream `entity_map_path`, final row count, dedup merges, localization scan PASS/FAIL.
- Localization scan result is PASS when scope is Location or Extension (a FAIL here is a hard block - regenerate offending rows).
- Both write destinations verified: confirm the Drive `N-Gram Tables/{Topic}/{Episode}/{Scope}/` folder AND the local mirror at `~/Desktop/claude_code/deliverables/podcast/N-Gram Tables/{Topic}/{Episode}/{scope}/` contain the same artifacts (markdown, JSON, metadata).
- INTERNAL section grep test: `grep -L "## INTERNAL" {client-facing-export}` returns zero hits for the client-facing Google Doc.
- **Internal metadata header line scan:** grep the entire client-facing Google Doc for the pipe-delimited `Topic: ... | Industry: ... | Jurisdiction: ...` provenance line. Zero hits required - that line belongs in `metadata.json` and the JSON `internal` block only. A hit anywhere in the Doc is a hard block.
- **Branded render check:** the client-facing Google Doc has the branded cover page (per `Cover Page Layout.png`); the Executive Summary structured as heading -> generated narrative paragraph -> stat bullets; the static `## Methodology` section below it; the 4-column collation table (compact, ~2 pages) with the CE-blue header row + white bold header text; the static table explainer below the table; and the bottom `INTERNAL` H1 colored CE blue. A missing or mis-ordered element is a fail.

**On failure:** fix the markdown, regenerate `n-gram-table.json` and `metadata.json`, re-run all checks. Do not proceed to `## Ship` until QA returns clean.

## Ship

What is?
The publish phase - writes the trio plus `metadata.json` to the topic's `N-Gram Tables/{Topic}/{Episode}/{Scope}/` Drive folder and mirrors the same artifacts to the local Desktop path.

### What ships

- **`N-Gram Table`** - Google Doc - human-facing canonical view, branded cover page, Roboto typeface, stable fileId.
- **`N-Gram Table.md`** - Markdown - source-of-truth mirror, retains the `## INTERNAL` block.
- **`n-gram-table.json`** - JSON - machine-readable, downstream-consumed, `content` + `internal` two-block split.
- **`metadata.json`** - JSON (internal) - provenance: sources, counts, dedup merges, localization scan result.

### Where it ships

- **Drive:** `N-Gram Tables/{Topic}/{Episode}/{Scope}/` (folder id `1gATbaPKlcwGBLkStF5d2l68Y-qyLkqYE`) in the shared drive `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`). The `{Scope}` segment resolves per the table in `### Outputs -> #### Drive destination`. This destination is fixed - the skill does not move existing Drive data.
- **Local mirror:** `~/Desktop/claude_code/deliverables/podcast/N-Gram Tables/{Topic}/{Episode}/{scope}/` - written every run.
- **Schema:** `~/.claude/skills/pod-2B-n-gram-table/references/schema/n-gram-table.json`.

### How it ships

Write to both destinations. On a write error to one, ship to the other and report the partial state.

- **Drive write.** Upload `N-Gram Table.md` as `text/markdown`. Create / update the `N-Gram Table` Google Doc in-place via `files.update` against the existing fileId (on a `## Create` run with no prior Doc, create once and record the fileId). Upload `n-gram-table.json` and `metadata.json` as binary.
- **Render rules - the client-facing Google Doc.** These are structural, not suggestions. Every n-gram Doc renders identically clean and sharp with zero manual cleanup.
  - **Resolve branding.** Read the Case Engine Branding folder (id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`) for logo, `colors.md`, fonts, and `Cover Page Layout.png`. Resolve the CE brand-blue hex from `colors.md`. Do not inline brand values.
  - **Doc body content.** Truncate the markdown source at the first `## Quality Assurance` heading. Strip the internal metadata header line (the pipe-delimited `Topic: ... | Industry: ...` provenance line) from the body. The Doc renders in the locked order: Cover -> Executive Summary (heading -> generated narrative paragraph -> stat bullets) -> Methodology (hard-coded) -> Collation table (~2 pages, blue header) -> table explainer (hard-coded) -> INTERNAL section.
  - **Branded cover page.** Render per the `Cover Page Layout.png` reference: CE logo top, title centered, subtitle below, client name + "Prepared by Case Engine" at bottom, branded header + footer, Roboto throughout. Title: `N-Gram Table` set in CE blue at 36pt (CE blue hex resolved from the Branding folder `colors.md`). Subtitle: topic / episode / location (e.g., `How to File a Car Accident Claim (Houston TX)`). Client name: `{Firm}`.
  - **Executive Summary section.** Structure: the `## Executive Summary` heading, then the GENERATED research-summary narrative paragraph as the lead, then the stat bullets (row count, entities/row average, dedup merges, localization scan result). The narrative paragraph is generated per run - plain-language, laymen's-terms, client-facing, jargon-free (no scoring math, no internal terms). Calibration exemplar for structure and voice: "The research for this episode keeps returning to a core set of names and ideas: [top 5-6 recurring entities]. These are the people, places, and rules that come up again and again whenever this topic is searched and discussed, so the conversation should keep circling back to them. The picture is strongly local. The questions are built around [jurisdiction] specifically - its roads, hospitals, courts, and the agencies that handle these cases - rather than generic, anywhere-in-the-country advice. Across [N] planned questions, the episode should emphasize the entities above and walk the listener through them in plain terms - answering the real questions people ask, in the order they would naturally come up." Template: sentence 1 names the top recurring entities; sentence 2 says they recur whenever the topic is searched/discussed so the conversation circles back; then the "strongly local" framing tied to the jurisdiction (roads / hospitals / courts / agencies) - for Topic Only scope drop the local framing and instead note the topic is covered comprehensively; the closing sentence ties to the N planned questions and "plain terms."
  - **Methodology section.** Render this static text directly below the Executive Summary, identical every run, verbatim: "Every question in this table is built from a structured entity analysis of the practice area and its jurisdiction. We map the people, places, institutions, and legal concepts that define how the topic is searched and discussed, score and weight each entity by relevance and authority, and group them into thematic clusters. Each cluster is then translated into episode questions engineered to surface the precise entities, terms, and actions that search engines and AI answer systems reward."
  - **Collation table styling.** The 4-column table (Question Text | N-grams | Entities | Predicates) renders with a CE brand-blue background on the header row and white bold header text - CE blue hex pulled from the Branding folder `colors.md`. The table targets roughly 2 pages: compact font size, tight row height, trimmed cell padding, and tuned column widths - readable but tight. Bold the strongest 1-2 entities per row in the Entities column; when scope is Location/Extension, the localized instance is always one of the bolded entities.
  - **Table explainer.** Immediately below the collation table, render this static text, identical every run, verbatim: "The table above is the complete question framework for this episode. Each row is a planned conversation beat, paired with the entities, terms, and actions to surface as it is discussed; together they form the content backbone the Run of Show and final script are built from."
  - **INTERNAL section.** At the bottom of the Doc, an H1 heading `INTERNAL` colored CE brand blue. Under it render the four review-tier blocks in this LOCKED order, each as an H2:
    1. **Cluster Architecture** - the thematic pillars. A short lead block: each pillar a bold label mapped to its question numbers (`**Pillar Name** - Q1, Q4, Q9`). Always present.
    2. **Topic Entities** - the universal, practice-area entities (accident types, injury types, legal standards / statutes, damages concepts, agencies - the non-local entities). Renders GROUPED BY TYPE - each type a bold sub-label with a bullet list of entries beneath it. Always present, every scope (including Topic Only).
    3. **Local Anchors** - the jurisdiction-specific entities. Heading is just `Local Anchors` (no jurisdiction prefix). Renders GROUPED BY TYPE with the IDENTICAL format as Topic Entities - each type a bold sub-label (`Roads/Highways`, `Law Enforcement`, `Medical Providers`, `Courts`, `County`) with a bullet list beneath, not a flat run of `Type: a, b, c` lines. Present only at Location/Extension scope; OMITTED entirely for Topic Only.
    4. **Bridge Entity Coverage** - the cross-cutting bridge entities mapped to question numbers (entity -> Q-ref map). Always present.
    Topic Entities and Local Anchors use the identical grouped-by-type rendering: section heading -> per-type bold sub-label -> bullet list -> next type. Localization notes render under the INTERNAL section when scope is Location/Extension. The QA / process / provenance content and the metadata header line never appear, even here.
  - **Roboto pass.** After the base text Doc is uploaded, run a `docs.documents.batchUpdate` with `updateTextStyle` setting `weightedFontFamily.fontFamily = "Roboto"` over the full document range as the final pass before sharing. Override only when a per-client `brand.json` typography block specifies otherwise.
  - **Footer.** `Case Engine  |  Confidential  |  Page {PAGE}` auto-applied via the Drive API template.
- **Archive.** If the existence check moved prior content to `_archive-{YYYY-MM-DD}/`, the archive folder ships alongside the new artifacts.
- **Local mirror write.** Write the same `N-Gram Table.md`, `n-gram-table.json`, and `metadata.json` to the local mirror path. If the Drive write fails but the local write succeeds, surface the partial state in the report - do not silently swallow it.
- **Report back:**

  ```
  Done. N-Gram Table - {Topic} / {Episode} ({Scope}{, Location if applicable}).

   Folder: https://drive.google.com/drive/folders/{folder_id}
   N-Gram Table (Doc): https://docs.google.com/document/d/{doc_id}

  Rows: {final_count} (generated {gen_count}, merged {merged_count}).
  Entities/row avg: {avg}. Localization scan: {PASS/FAIL}.

  Next: /pod-3A-ros-template (Phase 3 Run of Show).
  ```

### Who to Notify

`notify: []` - this skill posts no notifications. The producer is informed via the inline report-back above.

---

## INTERNAL (not for client distribution - auto-stripped from all exports; the reference prompt and worked examples ride into the local markdown only, never into the Drive Doc)

### Reference prompt - Main Podcast Episode (tokenized for reuse)

Verbatim reference material - the source the Best Practices section implements. Internal calibration only; never appears in the client-facing Google Doc.

```
Generate an LLM Collation Table for a law industry podcast episode focused on [PRACTICE AREA].

Podcast Topic: [EPISODE TITLE]
Industry: [INDUSTRY / SUB-INDUSTRY]

The table must contain four columns only:
 - Question Text
 - N-grams to Mention (include high-intent, long-tail, and process-oriented n-grams)
 - Entities to Mention (use authoritative, real-world entities only)
 - Predicates to Mention (use action-oriented verbs that reflect legal, insurance, and compensation processes)

Content Requirements:
 - Questions must sound natural and conversational, suitable for a legal podcast discussion.
 - Questions should flow logically, starting from general topics and gradually moving into deeper topics.
 - Focus on [CORE SUBJECT], liability, legal rights, insurance disputes, and settlement processes.
 - Include different [SUB-TYPES].

Entity Rules:
 - Entities must be real-world legal, regulatory, or institutional organizations.
 - Avoid fictional or vague entities.

Predicate Rules:
 - Predicates must represent legal or insurance actions (determine liability, file compensation claim, document injuries, etc.).

Output Requirements:
 - Output ONLY the table.
 - Include 25-35 rows.
 - Questions must be diverse and natural for a podcast conversation.
 - Ensure the structure is clean and machine-readable.
```

### Localization table

The entity map was already localized at Research Step 2. This n-gram table inherits. Every entity must match the entity map at the same scope level. This table is the single source for entity form, acronym convention, separator, and per-row count - referenced by Editorial Guideline 1, `### Quality gates`, and `## Create -> ### Map n-grams, entities, predicates`.

| Scope | Entity form | Acronym convention | Separator | Entities per row |
|---|---|---|---|---|
| **Topic Only** | Generic categories (`Police Department`, `Insurance Company`, `Civil Court`) | not needed | `,` | 2-4 |
| **State-level Location** | State instance + 2+ representative cities (`California Highway Patrol`; `Oakland Police Department`; `Los Angeles Police Department`) | optional | `;` | 2-3 |
| **City-level Location or Extension** | Full jurisdictional stack: federal -> state -> county -> city -> named institutions (`Houston Police Department (HPD)`; `Harris County Civil Courts`; `Memorial Hermann Hospital System`; `Texas Department of Insurance (TDI)`) | **standard** `Full Name (ACRONYM)` | `;` | 3-5 |

Semicolon separator is the default; comma only when no entity name contains an internal comma.

### Worked examples (calibration reference)

Three worked tables - one per scope - held as the in-skill calibration set when `references/examples/n-gram-table-examples.md` is empty. Additional GOOD / BAD / EDGE CASE examples accumulate in that file as real runs ship.

#### Example 1 - "How to File a Car Accident Claim" (Topic Only)

Generic entities, comma separator, 2-3 per row.

| Question Text | N-grams to Mention | Entities to Mention | Predicates to Mention |
|---|---|---|---|
| What should I do immediately after a car accident to protect my claim? | immediately after a car accident, protect your claim, first steps after a crash, preserve evidence | Police Department, Emergency Medical Services | ensure safety, call, document, seek medical care, preserve evidence |
| How do I file a car accident insurance claim step by step? | how to file a car accident claim, insurance claim process, claim filing steps | Insurance Company | notify insurer, submit claim, provide documentation |
| What evidence is most important for a car accident claim? | evidence for car accident claim, photos and videos, witness statements | Police Department | establish liability, support damages, corroborate events |

(Full 18-row reference table in `references/examples/n-gram-table-examples.md`. Note: 18 rows is the illustrative length - the target is 25-35.)

#### Example 2 - State-level (California, threading Oakland + Los Angeles)

Semicolon separator, multiple cities threaded through state entities.

| Question Text | N-grams to Mention | Entities to Mention | Predicates to Mention |
|---|---|---|---|
| What are the most common mistakes drivers make when filing a car accident claim in Oakland or Los Angeles? | car accident claim mistakes in Oakland, Los Angeles insurance claim errors | Oakland Police Department; Los Angeles Police Department; California Department of Insurance | fail to report; provide incomplete information; delay filing |
| What happens if you miss the SR-1 reporting deadline with the California DMV? | SR-1 form California deadline, DMV accident reporting requirement | California Department of Motor Vehicles | mandate filing within 10 days; suspend license; record accident |
| How does California's comparative fault rule affect claim mistakes? | California comparative negligence rule, shared fault accident claim | Superior Court of California, County of Los Angeles; Superior Court of California, County of Alameda | apportion fault; reduce damages; adjudicate disputes |

#### Example 3 - City-level (Houston, Texas)

Full jurisdictional stack. `Full Name (ACRONYM)` convention. Semicolon separator. 3-5 entities per row.

| Question Text | N-grams to Mention | Entities to Mention | Predicates to Mention |
|---|---|---|---|
| In Houston, what are the most common types of car accidents that lead to injury compensation claims? | common Houston car accident injury claims, Houston personal injury accident claim process | Houston Police Department (HPD); Texas Department of Insurance (TDI); Harris County Sheriff's Office; National Highway Traffic Safety Administration (NHTSA) | identify accident type; establish liability under Texas law; initiate claim with insurer |
| When someone gets rear-ended on Houston highways like I-10 or I-45, how does that affect recovery? | rear-end collision claim Houston Texas, Houston freeway rear-end crash injury claim | Houston Police Department (HPD); Texas Department of Transportation (TxDOT); Harris County Civil Courts | determine fault; document crash report (CR-3); process bodily injury claim |
| If a crash happens due to potholes in Houston, can victims pursue compensation from government entities? | Houston road hazard accident claim process, pothole accident claim Houston Texas | Texas Department of Transportation (TxDOT); City of Houston Public Works Department; Texas Tort Claims Act; Harris County Civil Courts | investigate roadway condition; file notice of claim; pursue liability damages |

Observations: the Topic Only example runs 18 rows but the target is 25-35 - push to the upper end. The City-level example runs 21 rows with 3-5 entities each, denser than Topic Only by design. The State-level example threads 2 major cities - that is the pattern.

### Provenance block

`metadata.json` must include a provenance block with at minimum: `run_date`, `entity_map_source` (local / drive), `content_plan` (found / not_found), `references_status` (used / empty), `schema_status` (validated / missing), upstream `entity_map_path`, final row count, generated count, merged count, dedup merges (which questions, which survivor), and localization scan PASS/FAIL.

### Internal metadata header line

The pipe-delimited provenance line - `Topic: {topic} | Industry: {industry} | Jurisdiction: {jurisdiction} | Episode: {episode} | Version: {version} | Created: {date} | Parent anchor: {anchor} | Skill: pod-2B-n-gram-table` - is internal provenance. It lives in `metadata.json` and the JSON `internal` block. It is EXCLUDED from the client-facing Google Doc by contract - the `## Ship` render strips it from the body before rendering, and it never appears under the bottom INTERNAL section either. QA greps the rendered Doc for the pipe-delimited pattern and hard-blocks on any hit.

### Source inventory

Records every input the run consumed: the resolved `entity-map.json` path and source (local / drive), the `entity-clusters.md` path when present, any `keyword-research.json` mined as seed questions, and the calibration examples used (bundled file or in-skill reference set).

---

## Learning & Iteration

- [ ] After each run, note edge cases, localization scan failures, dedup merge counts, and entity-map gaps; append GOOD / BAD / EDGE CASE entries to `references/examples/n-gram-table-examples.md`.
- [ ] Track recurring entity-map gaps - if the same belongs-but-missing entity surfaces across runs, propose an `/pod-1A-entity-research` map refresh.
- [ ] Watch for Topic Only tables shipping under 25 rows; if it recurs, tighten the `### Generate questions` guidance.

## Change Log

| Date | Change |
|---|---|
| 2026-07-10 | **Three-field geo model alignment (v3.0.1, Gabe directive from the Whalen scoping).** Stamped the canonical three-field geo model - **Targeting strategy** (single- vs multi-location) / **Optimization scope (show anchor)** (City/State/County/Regional, the show-wide breadth research was gathered at) / **Episode geo target** (the specific city THIS table emphasizes) - into `### Framing`, and mapped the existing scope labels to it: the table's `Location` / `Extension` scope = the Episode geo target; `Topic Only` carries no episode geo target; the show anchor is the research breadth, not any one episode's target. Stamped the rule **anchor scope != per-episode target** in `### Framing`, reinforced it in Editorial Guideline 4 (this skill is the enforcement point for per-episode city emphasis; city emphasis is a ceiling, never a floor - no city quota), and added a matching `### Gotchas` bullet. Greeting Q2 relabeled "Optimization scope (show anchor)"; Q4 annotated "= the Episode geo target"; Q5 relabeled by "Targeting strategy". Schema PATCH: `content.scope` and `content.location` descriptions mapped to the model (no structural field change). Reinforces the no-city-quota / natural-tonality principle. Revert: remove the geo-model block + rule from Framing, the Guideline 4 lead paragraph, the Gotcha, and the Greeting relabels; restore schema descriptions and version to 3.0.0. |
| 2026-06-17 | **Hard pre-write Canonical destination gate added.** New gate in `### Quality gates` enforces the dedicated `N-Gram Tables/` library (id `1gATbaPKlcwGBLkStF5d2l68Y-qyLkqYE`, inside `Podcasts // Case Engine [Shared]` id `0AAJKtWTUAZhHUk9PVA`) at the exact `N-Gram Tables/{Topic}/{Episode}/{Scope}/` path as the ONLY valid write target for all four artifacts (Google Doc + `N-Gram Table.md` + `n-gram-table.json` + `metadata.json`); rejects any redirect into a client episode delivery folder (`{Firm} Podcast/Episodes/EP{N}: ...`), and no caller / workflow / convenience override may honor such an instruction. Cross-referenced from the Drive destination section + a new Gotcha. Root cause: a workflow prompt overrode the documented fixed destination and wrote the Sutliff E8-E12 n-gram artifacts into the firm delivery folders. Revert: remove the Canonical destination gate bullet, the Drive-destination callout, and this Gotcha. |
| 2026-04-20 | Initial co-work version. Drive-native. Localization gate + dedup gate enforced. Hard dependency on matching-scope entity map. |
| 2026-04-20 | Consolidated all rules under one Best Practices section; removed duplicates from Quality Gates and Gotchas. Restructured: Input above Best Practices; Output, Examples, Routing at the bottom; Change Log dead last. |
| 2026-04-20 | Restructured to canonical 12-section pattern: Greeting + Inputs split out, Quality gates + Gotchas under Best Practices, Examples + Routing under Output. Workflow reframed as Step 1 of Run of Show. |
| 2026-04-20 | Moved YAML frontmatter to the top of the file in bare `---` delimiters. Owner set to Gabe Jordan. |
| 2026-04-20 | 4-step Research workflow update; Keyword Research and Entity Research run independent; Virality Research optional before Topic Planner. |
| 2026-04-20 | Promoted Quality gates to H2 after SOP, split into Content + Formatting subsections. Added Handoff Contract. Scaffolded `_references/` folder. |
| 2026-04-21 | DOCX layer removed. Client-facing artifacts render as Google Docs only. |
| 2026-04-21 | Run of Show phase expanded to 5 steps: Clip Table repositioned as required Step 5. |
| 2026-04-21 | Added `pod-` prefix for producer discoverability. |
| 2026-04-24 | Reverted `pod-` prefix across cowork skills. |
| 2026-05-14 | **v2.0.0** - Merged cowork n-gram-table v1.0 (canonical content) with original local pod-5-n-gram-table (Mode A enrichments). Output schema identical across modes. Bundled scripts + schemas + examples + iteration-log moved into canonical layout. |
| 2026-05-20 | **v3.0.0** - Full structural refactor to the canonical CE skill structure. Frontmatter completed (skill_kind, modes: multi, inputs, outputs, notify; version/date/owner moved to a metadata block). Best Practices restructured to the canonical contract H3s (Inputs / Outputs / Framing / Quality bar / Sourcing discipline / Editorial Guidelines / Quality gates / Gotchas / Iteration log); n-gram methodology relocated into Quality bar + Editorial Guidelines + Quality gates + the deliverable-shaped Create buckets. SOP rebuilt as H2 phase siblings (Checks / Prepare Inputs / Create / Update / Quality Assurance / Ship). Universal State Check versioning logic moved into `## Update`. QA rewritten as the canonical three-tier gate with the hardwired Anti-AI Detection two-pass scan and an On-failure recovery line. Old `## Output` folded into Best Practices Outputs + the new `## Ship` phase. Workflow demoted to H3. Old `## Appendix`-style content moved to `## INTERNAL` two-tier model; reference prompt and 3 worked examples preserved verbatim. Owner Gabe Jordan. |
| 2026-05-20 | **INTERNAL section - Topic Entities block added; 4-block order locked.** The bottom `INTERNAL` H1 of the client-facing Doc now carries FOUR review-tier blocks in a locked order: (1) **Cluster Architecture** - thematic pillars mapped to Q-refs (short lead block); (2) **Topic Entities** - NEW block: the universal, practice-area entities (accident types, injury types, legal standards / statutes, damages concepts, agencies - the non-local entities), grouped by type with a bold sub-label per type and a bullet list beneath; always present, every scope; (3) **Local Anchors** - jurisdiction entities, identical grouped-by-type format (Roads/Highways, Law Enforcement, Medical Providers, Courts, County); Location/Extension scope only, omitted for Topic Only; (4) **Bridge Entity Coverage** - cross-cutting bridge entities mapped to Q-refs. Topic Entities and Local Anchors use the identical grouped-by-type rendering. JSON schema `internal` member updated to carry all four blocks - `cluster_architecture` + `bridge_entity_coverage` as `{pillar/entity: [Q-refs]}` maps, `topic_entities` + `local_anchors` as `GroupedEntityBlock` (`{type: [entities]}`); two new `$defs` added (`QuestionRefList`, `GroupedEntityBlock`); `local_anchors` is an empty object at Topic Only scope. Render scripts at `/tmp/ngram-backfill/` (`prep_ngram.py`, `process_one.sh`, `rerender_one.sh`) updated to derive all four blocks from the collation table itself and accept an authoritative scope argument. |
| 2026-06-17 | **Mini composition: state-blend / location-bias made explicit (Eberst multi-location).** The no-parent multi-location Mini composition rule now states the blend explicitly: city signals set priority, then the strongest STATE-level questions weave in (location-biased but state-blended), Topic Only only when both thin. Row count stays 10-12 (Mini cap unchanged - a hard-10 was tried same day and reverted). City-placement Guideline 4 unchanged. Revert: restore prior composition wording. |
| 2026-06-16 | **City placement rebalanced to ~a third (Eberst + Sutliff E5-E12).** Converged after three swings same day: (1) a 60-70% floor over-localized into spam, (2) a geo-neutral-default / ~1-in-6 ceiling overcorrected into too-thin/non-local, (3) final landing = BALANCED band. Guideline 4: the table must read as a local show with the city present and grounding but never stamped on every line - target the city in roughly a THIRD of questions (~25-45%, soft center not a quota), rest carry locality via named local entities or stay geo-neutral. City-share gate is a two-sided band: FAIL HIGH above ~half (spam), FAIL LOW when the city is essentially absent and entities are not carrying locality (too thin). Adjective-spam ban and state-law-names-the-state kept. Geo-placement pointer in `### Generate questions` set to the balanced target. Research phases untouched - composition/phrasing only. Revert: restore the banded 60-70% floor row below. |
| 2026-06-16 | **(superseded same day)** City-token cap (Eberst E2/E3 spam fix). Guideline 4 + the city-share gate changed from "most-mentioned geo token" to a BANDED rule: city in ~60-70% of questions, floor = exceed county, ceiling = >85% FAILS. This floor over-corrected and was reverted to ceiling-only (row above). Revert target if rolling all the way back: "most-mentioned geo token / city must exceed county" single check. |
| 2026-06-12 | **Geo hierarchy + city-share gate (Mohink run).** Added Editorial Guideline 4 (city-first, county earned, state for law) and the city-share quality gate. Revert: remove Guideline 4 + the city-share bullet in Quality gates. |
| 2026-06-12 | **Targeting-strategy branch (multi-location Mini model).** Greeting Q5 now resolves episode format from the client targeting strategy: single-location -> Full (~20q); multi-location -> NO anchor episode, one Mini (internal scope label stays `Extension`) per target city at 10-12 questions hard cap. Extension row count widened 10 -> 10-12 in Quality bar / Quality gates / Generate questions. Generate-questions Extension rule split into two branches: parent-anchor-exists (legacy select+re-angle, unchanged) and no-parent multi-location Mini (generate from layered research; composition weighting city-first, then state, then Topic Only draw-down when city data is thin; cross-city no-verbatim rule). Research phases 1A/1B/1C and the Topic Only / state Location table targets (25-35) are UNTOUCHED - this changes output composition only. Chain order unchanged. Revert: restore Greeting Q5 to the Full/Extension two-liner, set Extension counts back to 10, collapse the Generate-questions branch back to the single parent-anchor rule. |
| 2026-05-20 | **Probe-strip + content/render hardening.** Renamed `pod-5-n-gram-table` -> `pod-2B-n-gram-table`; description + trigger + all sibling refs repointed to the new pipeline codes (1A/1B/1C/3A/3A/3B/3C/4D). Removed the entire `### Probe environment` H3 and all capability-probing apparatus - this skill runs locally in Claude Code only, calls its tools directly, skips or fails on a tool error. `#### Capabilities` (Inputs) became `#### Tools the skill calls`; `#### Capabilities` (Outputs) became `#### Write destinations`. All `runtime.capabilities` metadata dropped; all "when the FS-write probe succeeds" conditionals removed - local-mirror writes are unconditional. Iteration-log read-at-start contract repointed to `### Orient`. Workflow diagram replaced with the unified 4-phase pipeline diagram. **Task C** - Drive destination moved from `Episode Templates/.../03 N-Gram Table/` to the dedicated `N-Gram Tables/{Topic}/{Episode}/{Scope}/` folder (id `1gATbaPKlcwGBLkStF5d2l68Y-qyLkqYE`); local mirror moved to `~/Desktop/claude_code/deliverables/podcast/N-Gram Tables/`. **Task D** - added a content-plan (= topic plan, `pod-2A-topic-planner` output) prereq check to the Greeting + Inputs + a `### Check for content plan` step; auto-resolves the per-client Topic Plan slot, asks the user when not found. **Task E** - folded the standalone `good--ga-savannah-full-ngram.md` into `n-gram-table-examples.md` under `## GOOD` (content + documented deviations preserved); deleted the standalone file. **Render hardening (canonical format locked).** JSON schema rebuilt to three top-level members - `content` block + generated `research_summary` text field + separated `internal` block; the internal pipe-delimited metadata header line excluded from the client-facing Doc entirely (lives in `metadata.json` + the JSON `internal` block only). Case Engine Branding folder (id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`) added as a referenced input - logo, `colors.md`, fonts, `Cover Page Layout.png` resolved at render time, never inlined. Locked client-facing Doc format: branded cover (title `N-Gram Table` in CE blue 36pt, Roboto, branded header + footer) -> `## Executive Summary` (heading -> generated plain-language research-summary narrative paragraph as the bare lead -> stat bullets) -> `## Methodology` (hard-coded static paragraph, identical every run) -> 4-column collation table (25-35 rows, CE-blue header background + white bold header text, compact ~2 pages) -> hard-coded table explainer -> bottom `INTERNAL` H1 in CE blue holding Cluster Architecture / Local Anchors / Bridge Entity Coverage. QA gates added for the metadata-line scan and the branded-render check. |
| 2026-07-31 | **v3.1.0 - removed the `pod-1-podcast-bible` dependency** ahead of the skill moving to an environment without Fortress DB reach (this skill already had no Fortress calls, so no DB edits were needed). Stripped every podcast-bible reference: the workflow Phase 1 Foundation box + its note, the "helpful context but not a workflow step" prereq sentence in the Prerequisites line, the `Prereq (not a workflow step)` routing bullet, and the `bible_formatting.sh` provenance comment in `scripts/ngram_cover.sh`. Podcast architecture (client name, anchor scope, extensions) still resolves from the optional `podcast-overview.md` when present, else the Greeting asks - unchanged. |
