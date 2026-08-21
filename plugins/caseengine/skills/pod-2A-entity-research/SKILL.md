---
name: pod-2A-entity-research
description: >
  Build the scored entity relationship map for a topic or practice area using
  Koray's entity attribute methodology - 40-50 entities across three tiers,
  8-15 clusters, 4-6 bridges, jurisdictional localization. Use whenever someone
  says "entity map for [practice area]", "run entity research on [topic]",
  "build an entity map", "koray entity map", or "/pod-2A-entity-research". Research
  Step 2A of the podcast pipeline - the jurisdiction-agnostic foundation every
  downstream skill reads. Runs in tandem with pod-2B-keyword-research and
  pod-2C-virality-research as one in-tandem research pass. Feeds the n-gram table,
  topic planner, run of show, and SEO topical maps downstream.
skill_kind: hybrid
modes: multi
inputs: [practice-area, scope, location, parent-entity-map.json, content-gap-report, keyword-research.json, podcast-overview.md]
outputs: [json, markdown, gdoc]
notify: []
metadata:
  version: 3.0.0
  date: 2026-05-20
  owner: Gabe Jordan
  version_history: >
    1.0 - co-work Drive-native version (2026-04-20). 2.0.0 - merged cowork
    canonical content with original local pod-2-entity-research Mode A
    enrichments (2026-05-14). 3.0.0 - renamed pod-2-entity-research ->
    pod-2A-entity-research; full structural refactor to canonical CE skill
    structure (2026-05-20).
---

# Entity Research

> **Drive write governance:** All Drive operations (create, update, rename, move) follow [Ship]. Revise in place via `files.update` against the existing fileId, never delete-and-reupload (breaks the fileId/URL chain and silently kills every downstream reference).

### What is

A scored entity relationship map for a topic or practice area, saved to Google Drive at Topic Only / Location / Extension scope. Forty to fifty entities across three tiers, 8-15 contextual clusters, 4-6 bridge entities, with optional jurisdictional localization. It runs once per practice area at Topic Only level (the jurisdiction-agnostic foundation), then cascades down with parent-map inheritance. Every downstream skill at matching scope reads this map to ground its output - n-gram table, ROS template, client ROS, client guide, topic planner, virality research, SEO topical maps. Without it, each skill invents entities from scratch (drift, missed localizations, no tier discrimination). With it, every artifact at that scope shares the same entity vocabulary, cluster shape, and jurisdictional instances.

### Workflow

Entity Research is **Step 2A** of **Phase 2 (Research)** of the podcast pipeline. The Research phase is LOCKED: `pod-2A-entity-research`, `pod-2B-keyword-research`, and `pod-2C-virality-research` run as ONE in-tandem research pass (Topic Only + Topic+Location scope). Topic Only-level here is the jurisdiction-agnostic foundation, shared across firms in the same practice area; localized scopes inherit from it. Also runs standalone as the foundation for any SEO / content / topical-map work.

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
- **Phase 2 Research** - the three Research skills (2A / 2B / 2C) run together as one research pass. 2A (Entity Research) is the foundation the other two layer onto; 2B and 2C overlay demand and virality signal. Runs ONCE per practice area + location cascade.
- **Phase 3 Planning** - `pod-3A-topic-planner` ranks episodes from the research; `pod-3B-n-gram-table` builds the per-episode question framework.
- **Phase 4 Run of Show** - `pod-4A-ros-template`, `pod-4B-client-ros`, and `pod-4C-client-guide` run per prioritized episode.

### Trigger phrases

- `/pod-2A-entity-research`
- "entity map for [practice area]"
- "run entity research on [topic]"
- "research entities for [topic]"
- "build entities for [topic/location]"
- "map entities for [topic] in [location]"
- "entities for the [extension] episode"
- "do we have entity research for [topic]"
- "is there an entity map for [topic/location]"
- "koray entity map"
- "entity analysis for [topic]"
- "what entities matter for [practice area]"
- "build an entity map" / "run entity map"

### Greeting

Hi, I'm Entity Research. Before I run, I need to see what we have and what's missing.

#### Tell me what client this is for.

I'll check Drive for the Podcast Show Bible at the path declared by the `pod-1-podcast-bible` skill (resolve via [Podcast Drive](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU) - never inline the path here, the show-bible skill owns it). The flow forks based on what's there.

#### Path A - Show Bible exists

The Show Bible has everything I need to plan the run. I propose the full plan in one message and you confirm or modify:

> "OK great - **{Targeting strategy}** firm; **Optimization scope (show anchor)** = **{Anchor Location}**, with **{Extension Cities}** as the per-episode **Episode geo targets**, target services **{Priority Services}** (in priority order).
>
> Here's what I'll run for **{Top Priority Service}**:
>
> - **Topic Only** foundation (jurisdiction-agnostic, inheritance source for everything below)
> - **Location: {Anchor}** (full jurisdictional cascade)
> - **Extensions:** {Extension city 1}, {Extension city 2}, {Extension city 3}
>
> Sound good? Or modify (different practice area, smaller scope, skip extensions, content-gap report to mine, etc.)."

- **Yes** - I run the plan as proposed.
- **Modify** - tell me what to change. I re-propose, you confirm, then I run.

If anything in the architecture itself is wrong (anchor / extensions / services), say so - I'll patch the Show Bible after this run finishes.

#### Path B - Show Bible missing

> "I don't see a Podcast Show Bible for this client. Two options:
>
> - **Recommended:** run `/pod-1-podcast-bible` first. It captures architecture once; every downstream skill reads it as ground truth.
> - **Inline workaround:** tell me the basics now and I'll proceed with this run only. You'll still want to run `/pod-1-podcast-bible` after to lock it in.
>
> Which do you want?"

If inline workaround, I'll ask for the three geo fields (canonical geo model - use these exact labels):

1. **Targeting strategy** - `single-location` vs `multi-location`. Does the firm serve / rank one city or several? Single-location anchors and builds every episode at the one city; multi-location anchors broad and targets a different city per episode.
2. **Optimization scope (show anchor)** - City / State / County / Regional. What are we optimizing the podcast *as a whole* to rank for? This is the scope this entity map is built at.
   - **City:** "Houston car accident lawyer" - anchor: Houston.
   - **State:** "California car accident lawyer" - anchor: California; a multi-location firm usually anchors here to own the whole footprint.
   - **County / Regional:** "Inland Empire injury attorney", "Harris County", "Bay Area" - anchor: the region / county.
3. **Episode geo target(s) (if any)** - the specific city each individual episode is built to rank for. Each becomes an **Extension** map that inherits from the anchor-scope Location map and surfaces what is different at that city. "None" if single-location - every episode shares the one anchor city.

#### Path C - Lookup intent

If you triggered me with phrases like "do we have entity research for X" or "is there an entity map for Y", I skip the greeting entirely. I go straight to the existence check, report existence + URL + last-updated date, and wait for your call (`rebuild` / `refresh` / `archive-and-rebuild`) before any generation. A stale map should show its last-updated date up front so you can decide whether to trust it before downstream skills consume it.

I'll only ask once. I won't touch Drive until you say go.

---

## Best Practices

The WHAT contract. Every other section references these by name; the SOP never restates them.

### Inputs

What is?
The materials this skill ingests - the practice area + scope, an optional parent entity map to inherit from, optional content-gap and keyword-research overlays, and the podcast architecture doc - all resolved before any analysis runs.

#### Required

- **Practice Area** - the practice area or topic name. Resolves to the `{Practice Area}/` Drive folder under `templates [master]/AEO/Podcast/Entity Research/`. Examples: Car Accidents, Wrongful Death, Premises Liability.
- **Scope** - one of: Topic Only, Location, Extension.
- **Location** - required when scope is Location or Extension. State-prefixed jurisdictional folder name. Format: `CA` (state-only), `CA - Inland Empire` (region), `CA - Los Angeles County` (county), `CA - Long Beach` (city). No colons; dashes only.

#### Optional

- **Parent entity map** - path to a parent `entity-map.json` to inherit from. Defaults to the practice area's `Topic Only/entity-map.json` for sub-scope runs.
- **Content-gap report** - competitor entity data. Auto-detected at `~/Desktop/claude_code/mcps/content-gap-mcp-server-andrew/data/reports/{practice-area-slug}/`, or uploaded to `_inputs/` in the matching scope folder. The skill mines competitor entities, popularity counts, and relevance scores from it.
- **`keyword-research.json`** - the keyword-research seed set from `pod-2B-keyword-research` at `templates [master]/AEO/Podcast/Keyword Research/{Practice Area}/{matching scope}/`. When present, PAA stacks seed candidate entity surface area. Optional signal overlay, not a required input.
- **Refresh flag** - default: refresh in place (routes to `## Update`). Pass `archive-and-rebuild` to force a full rebuild with prior content archived to `_archive-{YYYY-MM-DD}/`.

#### Auto-read (no action required)

- **`podcast-overview.md`** / **Podcast Show Bible** - architecture source of truth produced by `pod-1-podcast-bible`. Path is owned by that skill and resolved via [Podcast Drive](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU). If present, the skill auto-fills Greeting questions 1-3 (firm name, anchor scope, extensions); otherwise it asks.
- **Local entity-map example references** - `references/examples/`. If missing or empty, fall back to the `## INTERNAL` reference set only - do not block.

#### Tools the skill calls

This skill runs locally in Claude Code and calls its tools directly - it assumes they exist and uses them in this priority order. On a tool error, it skips that source and degrades to the next; it never probes for availability first.

- **Local filesystem read** - for an auto-detected content-gap report at `~/Desktop/claude_code/mcps/content-gap-mcp-server-andrew/data/reports/{practice-area-slug}/` and a parent entity map at the canonical Desktop deliverables path.
- **`gws drive`** (or `mcp__claude_ai_Google_Drive__*` connector) - for the parent entity map, optional keyword research, and `_inputs/` content-gap uploads from the shared Drive.
- **`mcp__ce-services__rag_query`** with `rag_name: koray` - for Koray entity-methodology grounding when calibrating tier and vector scoring.
- **User-supplied materials** in the greeting (pasted entity sets, dropped files) and user interview for hard requirements still missing - the always-available floor.
- **Behavior on a tool error** - skip that source and degrade to the next. With no content-gap report or parent map, the skill runs on LLM domain knowledge plus user-supplied materials; flag every Inferred value with `> NEEDS CONFIRMATION:` per Sourcing discipline. A Koray RAG error logs `koray_rag: unreachable` and proceeds on in-skill methodology.

### Outputs

What is?
The artifacts this skill ships - the 3-format trio (a machine-readable JSON sidecar, a markdown source-of-truth, and a human-facing Google Doc) plus a `metadata.json` provenance file - landing in the practice area's dedicated `Entity Research/{Practice Area}/{Scope}/` Drive folder, mirrored to the local Desktop path.

#### Output formats

CE-wide default: every persistent artifact ships in three formats.

- **JSON** - `entity-map.json` - structured / machine-readable sidecar for downstream programmatic consumption. Carries entities + clusters + bridges + localization data + optional `localization_supplement` block + provenance metadata. Schema in `references/schema/entity-map.json`.
- **Markdown** - `Entity Map.md` - local source-of-truth mirror. Combined: executive summary + tier table + cluster architecture + bridge entities + localization summary + optional Localization Supplement section + embedded vector-space chart reference + the `## INTERNAL` block.
- **Google Doc** - `Entity Map` - human-facing canonical view at the Drive destination below. Created / updated in-place via `files.update` against a stable fileId so the URL never breaks for downstream links. Typeface: Roboto for every text element (body, headings, table cells, captions), applied via `batchUpdate` `updateTextStyle` with `weightedFontFamily.fontFamily = "Roboto"` over the full document range as the final pass before sharing. Override only when a per-client `brand.json` typography block specifies otherwise.

A `metadata.json` provenance file ships alongside the trio (internal-only, not a client-facing artifact - records sources, counts, localization coverage, scan results).

#### What ships

- **`entity-map.json`** - JSON - machine-readable, downstream-consumed; entities + tiers + vector strengths + cluster assignments + bridge flags + localization coverage + optional `localization_supplement` block + provenance metadata.
- **`Entity Map.md`** - Markdown - local source-of-truth mirror, retains the `## INTERNAL` block.
- **`Entity Map`** - Google Doc - human-facing canonical view, Roboto typeface, stable fileId, vector-space chart embedded inline.
- **`metadata.json`** - JSON (internal) - provenance: sources, run date, entity / cluster / bridge counts, localization coverage, supplement status, references status.

#### Drive destination

Shared drive root: `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`). The `templates [master]/AEO/Podcast/Entity Research/` folder id is `1iKEslJ5JWScmRwjTAEUDrAvBakzQ81Ee`.

Entity Research lives in its own dedicated `Entity Research/` folder under `templates [master]/AEO/Podcast/`, parallel to `Keyword Research/` and `Virality Research/`. Each practice area gets one folder (`{Practice Area}/`), with all scope variants as parallel subfolders inside.

```
templates [master]/AEO/Podcast/Entity Research/{Practice Area}/{Scope}/
  Entity Map.md                          source of truth (markdown)
  Entity Map                             Google Doc (in-place files.update)
  entity-map.json                        machine-readable, downstream-consumed
  metadata.json                          sources, counts, localization coverage
  visuals/Entity Vector Space.png         vector-space chart (local post-step)
  _inputs/                                (optional uploaded content-gap reports)
  _archive-{YYYY-MM-DD}/                  (if this folder had prior content)
```

The `{Scope}` segment resolves per scope:

| Scope | When | `{Scope}` path segment |
|---|---|---|
| **Topic Only** | Foundation map; jurisdiction-agnostic, inheritance source for everything below | `Topic Only/` |
| **Location** | Full-length jurisdictional cascade for a specific state / county / city | `Locations/{Location}/` |
| **Extension** | Sub-market derivative inherited from a Location | `Extensions/{Location}/` |

Location naming matches exactly, no colons, dashes only: `CA`, `CA - Los Angeles County`, `CA - Long Beach`. The Drive destination is fixed - this skill does not move existing Drive data.

This destination is enforced by the **Canonical destination gate** (`### Quality gates`), which hard-fails any pre-write target that is not a descendant of the dedicated `Entity Research/` library. These artifacts NEVER live in a client/firm episode delivery folder - the dedicated `Entity Research/` library is their only valid home.

#### Local mirror

`~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/01-entities/` - holds the same `Entity Map.md`, `entity-map.json`, and `metadata.json`. `{topic-slug}` = slugified practice area (e.g., `car-accidents`); `{episode-slug}` = slugified scope label (e.g., `topic-only`, `ca-long-beach`, `long-beach-extension`). The mirror enables fast local iteration, downstream local skill consumption (the n-gram table reads from here), and offline review. Written on every run.

#### Schema

`references/schema/entity-map.json` - the canonical JSON schema `entity-map.json` validates against. Required fields: `entities` array (each with tier, type, vector_strength, prominence, relatedness, popularity, cluster, bridge flag), `clusters`, `bridges`, `localization` block, optional `localization_supplement` block, `provenance` block. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed - do not block on a missing schema.

#### Sections INCLUDED in the client-facing artifact

- Cover page (CE logo, title `Entity Research`, subtitle = practice area, scope line, "Prepared by Case Engine")
- Executive Summary (entity count, tier distribution, cluster + bridge counts, localization scan result)
- Tier Table (Entity | Type | Vector Strength | Prominence | Relatedness | Popularity | Connections)
- Cluster Architecture (contextual layers with entity assignments)
- Bridge Entities
- Localization Summary / optional Localization Supplement (if scope is Location/Extension)

#### Sections EXCLUDED (internal-only)

- `## Quality Assurance` and everything from that heading onward
- `## INTERNAL` (Known Gaps, Handoff Contract, reference material, provenance)

Any Google Doc renderer MUST truncate the markdown source at the first `## Quality Assurance` heading (or `## INTERNAL`, whichever appears first) and discard everything after, so internal-process-and-QA content stays out of the client-facing deliverable while the same markdown serves as the internal source of truth.

#### Write destinations

Both destinations are written every run. On a write error to one, the skill ships to the other and surfaces the partial state in the report - it does not silently lose the deliverable.

- **Drive** - `gws drive` (or `mcp__claude_ai_Google_Drive__*` connector) - writes the markdown, the Google Doc, the JSON, and metadata into the `Entity Research/{Practice Area}/{Scope}/` Drive folder.
- **Local mirror** - local filesystem write to the local mirror path, alongside the Drive write.
- **Behavior on a write error** - if one destination errors, ship to the other and report the partial state. If both error, hard-fail with a clear message; do not silently lose the deliverable.

#### Examples

`references/examples/` - GOOD / BAD / EDGE CASE labeled anchor runs. Read 1-2 examples matching the requested scope as calibration before generating. If the folder is empty, proceed on the `## INTERNAL` reference set alone and flag `"references": "empty"` in `metadata.json`.

#### Routing

- **Upstream (optional):** `pod-2B-keyword-research` - keyword research can run in parallel; this skill runs with just a topic name. The three Research skills run as one in-tandem pass.
- **Downstream:** `pod-3A-topic-planner`, `pod-3B-n-gram-table`, and the Phase 4 Run of Show skills, plus SEO topical maps, content briefs, website architecture all consume `entity-map.json` at matching scope.
- **Prereq (not a workflow step):** `pod-1-podcast-bible` runs once per client - architecture source of truth.
- **Refresh:** re-run with the same practice area + scope (routes to `## Update`).

#### Handoff Contract

This skill produces the following for downstream consumers:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| `entity-map.json` | `pod-3A-topic-planner`, `pod-3B-n-gram-table`, the Phase 4 Run of Show skills, `pod-2C-virality-research` | Scored entity list with tiers + vector strengths + cluster assignments + bridge flags + localization coverage + optional `localization_supplement` block + provenance |
| `Entity Map` / `Entity Map.md` | Run of Show (reads Cluster Architecture + Bridge Entities sections directly), human readers | Full bible-style doc - tier tables, cluster architecture, bridge entities, localization summary |
| `metadata.json` | (not consumed downstream) | Internal provenance - sources, run date, counts, localization coverage, supplement status, references status |

Downstream consumers can rely on: the Google Doc URL is stable for the lifetime of the map (preserved via `files.update` across re-runs); `entity-map.json` validates against `references/schema/entity-map.json`. Upstream pulls (all optional): `keyword-research.json` from `pod-2B-keyword-research`, a parent `entity-map.json` at the `Topic Only/` path (inheritance source), a content-gap report (auto-detected locally or in `_inputs/`).

### Framing

The Entity Map is the foundation research artifact, not a finished deliverable for a single client. It is a machine-readable, scored entity vocabulary that every downstream skill at matching scope reads to ground its output. It is never narrative prose, never a listicle of entities, and never a client-populated artifact - firm / attorney / podcast names do not belong in it.

### Quality bar

What "good" looks like - the pass / fail intuition.

- 40-50 entities total, distributed across three tiers, never padded past 50.
- Tier discrimination is real: Tier 1 (vector strength >= 0.80, core), Tier 2 (0.60-0.79, major), Tier 3 (0.40-0.59, supporting). Nothing below 0.40 ships.
- Entity types cover breadth across all required categories (legal concepts, statutes, agencies, insurance, medical, case types, liable parties, evidence, damages, causes, industry practice, credentials) - breadth, not depth in one.
- 8-15 clusters, each a genuine contextual layer (procedural / medical / financial / regulatory / adversarial), not a bucket of one entity type.
- 4-6 bridge entities, each genuinely spanning >= 2 clusters.
- Inheritance is correct when scope is Location or Extension - universals carried from the parent Topic Only map, only jurisdiction-bound entities swapped or added.
- Vector-space chart embedded inside the markdown / Google Doc.
- No em dashes, no banned vocabulary - the Anti-AI Detection scan fires before publish.

### Sourcing discipline

The Confirmed / Inferred / Unknown three-state pattern. Never block, always ship, never silent. The map still ships when data is incomplete; gaps surface in `## INTERNAL` or with `> NEEDS VERIFICATION:` blocks.

- **Confirmed** - claim traces to a specific source: content-gap competitor data, parent-map inheritance, or Koray RAG methodology grounding. Ship as-is, no marker.
- **Inferred** - a sensible default applied when the source is insufficient (e.g., a vector score estimated from LLM domain knowledge because no content-gap report was reachable). Ships with `> INFERRED: {what + why}` flag.
- **Unknown / NEEDS CONFIRMATION** - no source AND no defensible default. Ships with `> NEEDS CONFIRMATION: {what's missing}` block, never silently synthesized.

### Editorial Guidelines

Cross-cutting content rules for the entity map. The SOP points back here; the rules live here once.

**Guideline 1 - Vector strength is computed, never guessed wholesale.**

- Every entity has three attributes: Prominence (how central to the contextual domain - weighted highest), Relatedness (how strongly it connects to the core topic and other entities), Popularity (how often it appears across the competitive corpus). Koray: "An entity attribute can be popular, but it might not be prominent." Prominence is the discriminator.
- Formula: `vector_strength = (prominence x 0.45) + (relatedness x 0.35) + (popularity x 0.20)`.
- With content-gap data: `competitorCount / max(competitorCount)` maps to popularity; `avgRelevanceScore` maps to relatedness; LLM estimates prominence from centrality.
- **Where it fires in the SOP:** `## Create -> ### Score and tier entities`.

**Guideline 2 - Topic Only is location-agnostic; jurisdiction is a modifier applied below.**

- The `Topic Only/` map is the jurisdiction-agnostic foundation. When building a Location or Extension map, read the parent `Topic Only/entity-map.json` first, carry forward jurisdiction-neutral Tier 1 + Tier 2 entities, and only add / swap entities that change with jurisdiction (courts, statutes, forms, agencies, hospitals, highways). Do not re-score universal entities.
- **Where it fires in the SOP:** `## Prepare Inputs -> read the parent map`, and `## Create -> ### Cluster and bridge`.

**Guideline 3 - Firm / attorney / podcast names are NOT entities.**

- Entity Research produces a research foundation, not a client deliverable. Firm, attorney, and podcast names get underlined at populate time in the Client ROS downstream, never placed in this map's entity list.
- **Allowed:** real-world named legal, regulatory, and institutional organizations only - the kind cited as authority.
- **Where it fires in the SOP:** `## Create -> ### Surface candidate entities`.

**Guideline 4 - Localization is raw research, not forced substitution.**

- Entity Research at every scope is raw research - no forced localization. Generic entities stay; local entities appear when they score on the vector formula. No substitution, no removal. The localization step tells the LLM how to NAME local entities when they enter the map (entity-form-by-scope convention in `## INTERNAL`), and defines the coverage metric that triggers an optional supplement.
- **Localization Coverage metric:** `generic% = generic entities / total`. If `generic% > 30%` AND scope is City / Extension / a tight scope, inline-ask the producer whether to produce a focused Localization Supplement section.
- **Where it fires in the SOP:** `## Create -> ### Evaluate localization coverage`.

**Guideline 5 - Geo model: this map is built at the show anchor; per-episode targets derive from it.**

- Three fields govern every geo decision - use these exact labels: **Targeting strategy** (`single-location` vs `multi-location` - does the firm serve / rank one city or several?), **Optimization scope (show anchor)** (City / State / County / Regional - what the podcast *as a whole* is optimized to rank for; a multi-location firm usually anchors at State or Regional, a single-location firm at City), and **Episode geo target** (the specific city each individual episode is built to rank for).
- **This entity map is built at the Optimization scope (show anchor).** The map's own scope (Topic Only / Location / Extension) and `location` value ARE the show anchor: a City anchor builds a `Location: {City}` map, a State / County / Regional anchor builds a `Location: {State / County / Region}` map. Per-episode research for a specific **Episode geo target** city does NOT rebuild this map - it reuses / derives from the matching location-scoped map (the Topic Only foundation plus the anchor-scope Location map), inheriting universals per Guideline 2, and adds only the entities that change at that target city (typically as an **Extension** map).
- **Anchor scope != per-episode target.** The show can be optimized for a broad scope (e.g. the whole state) while each episode targets a specific city we're trying to rank for. Research runs at the anchor breadth; each episode's questions / titles emphasize that episode's target city naturally - a ceiling, never a forced quota (see Guideline 4 / no-city-quota). Getting this wrong is how a multi-location statewide firm ends up with a map that all sounds like one city, or how city emphasis silently becomes a city floor.
- **Where it fires in the SOP:** `## Checks -> ### Orient` (resolve the three geo fields from the Show Bible or greeting) and `## Create -> ### Cluster and bridge` / `### Evaluate localization coverage` (build at the anchor breadth; localize toward the Episode geo target as a ceiling, never a floor).

### Quality gates

Mechanical pass / fail conditions checked in `## Quality Assurance`.

- **Canonical destination gate** (hard, pre-write - runs BEFORE any artifact is written). Resolve the target parent folder and assert it is a descendant of the dedicated `Entity Research/` library (folder id `1iKEslJ5JWScmRwjTAEUDrAvBakzQ81Ee`) at the exact `Entity Research/{Practice Area}/{Scope}/` path. If the target resolves to anything else - especially a client/firm episode DELIVERY folder (`{Firm} Podcast/Episodes/EP{N}: ...`) - the gate FAILS and the skill MUST refuse to write the Entity Map Google Doc, the `Entity Map.md` source-of-truth, the `entity-map.json` sidecar, or `metadata.json`. No caller argument, workflow / orchestration instruction, or convenience override may redirect these artifacts out of the canonical library. An instruction to write them into a client/episode delivery folder is itself the failure and must be rejected, not honored.
- **Target counts** - 40-50 entities, 8-15 clusters, 4-6 bridges.
- **Tier structure** - T1 >= 0.80, T2 0.60-0.79, T3 0.40-0.59; nothing below 0.40.
- **Entity types** - breadth across the required categories, not depth in one.
- **Inheritance** - parent-map carry-forward correct when scope is Location or Extension.
- **Localization coverage** - coverage metric logged in `metadata.json`; supplement rendered if the inline-ask was triggered AND the producer opted in.
- **Jurisdiction-flag check** - Topic Only entities that are state-bound annotated with `(<State> only)` - prevents the SR-1 leak gotcha.
- **Vector-space chart** - embedded inside `Entity Map.md` / Google Doc.
- **Schema validate** - `entity-map.json` validates against `references/schema/entity-map.json`.
- **Provenance present** - `metadata.json` carries the provenance block.
- **Artifacts present** - markdown, JSON, metadata all written; Google Doc exists for the markdown.
- **Tier 1 + bridge highlights** - Tier 1 and bridge rows bold-highlighted in the rendered doc.
- **No em dashes** - plain hyphens only anywhere in the output.

### Gotchas

Failure modes that are warnings, not enforceable rules.

- **Jurisdiction-specific entities leak across maps if not flagged.** Real incident: SR-1 Form (a California-only post-accident report) entered a Topic Only Car Accidents map without a state flag, then propagated into a Colorado client's ROS. Colorado has no SR-1. Two-part fix: (1) at Topic Only scope, never present state-specific forms/statutes/agencies as universal - flag them in the entity row as `(California only)`; (2) at Location and Extension scope, the inheritance step MUST drop flagged entities that do not match the target jurisdiction. If you do not know the jurisdiction at research time, name state-specific entities generically (e.g., "post-accident insurance report form" instead of "SR-1").
- **Vector-space visual is a post-step.** Do not block delivery on the PNG - ship without it if the chart script fails; the bundled `scripts/entity-vector-space.py` runs after the JSON is written and the chart gets dropped in.
- **Local Koray docs the original skill referenced no longer exist on disk.** The Koray methodology source is now `mcp__ce-services__rag_query` with `rag_name: koray` - do not attempt to read `~/Desktop/claude_code/docs/koray/website-content/seo-research-study__entity-*.md`.
- **Confirm before writing.** In a fresh context, show the state-check block and wait for `yes / cancel`.
- **Template folder only.** This skill writes under `templates [master]/AEO/Podcast/Entity Research/`. Client populate is downstream.
- **Never write entity-research artifacts into a client episode delivery folder** - even if a caller, workflow, or orchestration step says to. A recent workflow override wrote research artifacts into client delivery folders; that is the failure this gate exists to stop. The dedicated `Entity Research/{Practice Area}/{Scope}/` library is the only valid home for the Entity Map Doc, `Entity Map.md`, `entity-map.json`, and `metadata.json`. The **Canonical destination gate** (`### Quality gates`) hard-fails any other target - a `{Firm} Podcast/Episodes/EP{N}: ...` destination is rejected, not honored.

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
The pre-flight phase - reads the iteration log, orients to the right practice area folder, checks whether an entity map already exists at this scope, and decides whether this run creates a new map or updates an existing one.

### Orient

What is?
The orientation step - read the iteration log, confirm the correct Drive root, and resolve the practice area folder before producing anything.

- **Read the iteration log.** Read `references/iteration-log.json`, filter to entries with `status: open` or `status: in-progress`, surface them to the agent as known issues to watch for this run.
- Read the canonical [Podcast Drive](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU) reference doc. The podcast root is `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`).
- If `podcast-overview.md` / the Show Bible is reachable, read it and auto-fill Greeting questions 1-3; confirm in one line. Otherwise ask the Greeting questions.
- Verify the practice area folder under `templates [master]/AEO/Podcast/Entity Research/{Practice Area}/`. If it exists and is named correctly, proceed. If it exists but does not follow the convention, rename per Podcast Drive. If it is missing, create per the Podcast Drive decision tree.
- Read `references/examples/` and pick 1-2 examples matching the requested scope as quality anchors. If empty, proceed on the `## INTERNAL` reference set and flag `"references": "empty"` in `metadata.json`.

### Existence check

What is?
The mode router - decide whether this run creates a new map or updates an existing one based on whether `Entity Research/{Practice Area}/{Scope}/` already has content. Also the lookup-intent path.

- When triggered with lookup phrases ("do we have entity research for X"), skip the greeting entirely. Report existence + URL + last-updated date; wait for explicit `rebuild` / `refresh` / `archive-and-rebuild`.
- Look for an `Entity Map` Google Doc + `entity-map.json` inside the resolved scope folder.
- **Missing:** no prior artifact - route to `## Create`. If the closest-scope parent exists (e.g., asked for Long Beach but Topic Only foundation exists), report it; do not auto-promote.
- **Found:** surface provenance (existing `metadata.json` run date, entity count) and ask: refresh in place / archive-and-rebuild / cancel.
  - Refresh in place - route to `## Update`.
  - `archive-and-rebuild` (or the refresh flag passed at invocation) - move prior content to `_archive-{YYYY-MM-DD}/` and route to `## Create`.

## Prepare Inputs

What is?
The input-preparation phase - loads the parent map (for inheritance), the content-gap report, optional keyword research, and Koray methodology grounding into a working set ready for the Create or Update phase.

Work through the input sources in priority order; on a tool error, skip that source and degrade to the next.

- **Consult Koray RAG.** Call `mcp__ce-services__rag_query` with `rag_name: "koray"`, `top_k: 6`, discard results with score < 0.40. Run the 5-query table in `## INTERNAL` for entity-methodology grounding. On an error, log `koray_rag: unreachable` and proceed on in-skill methodology.
- **Load the content-gap report.** Scan `~/Desktop/claude_code/mcps/content-gap-mcp-server-andrew/data/reports/{practice-area-slug}/` for `entity-analysis.json` and `cluster-descriptions.json`. If nothing is there, check `_inputs/` of the matching scope folder in Drive. Extract competitor entities, `competitorCount` (popularity), `avgRelevanceScore` (relatedness), cluster descriptions (thematic seeds). If no report exists, log `content_gap: llm_only` and proceed on LLM domain knowledge.
- **Check for keyword research.** Look for `keyword-research.json` at `templates [master]/AEO/Podcast/Keyword Research/{Practice Area}/{matching scope}/`. If found, mine PAA stacks (candidate entity surface area), high-volume head terms (Tier 1 cross-check), cluster seeds. Log `keyword_research: found | not_found`.
- **Read the parent map (inheritance).** If scope is Location or Extension, read the parent `Topic Only/entity-map.json` for this practice area. Carry forward universals per Editorial Guideline 2.
- **Load calibration examples.** Hold the 1-2 scope-matched examples from `references/examples/` as quality anchors for the Create phase.

## Create

What is?
The create branch - builds the scored entity map from scratch when no prior map exists, producing a tiered, clustered, schema-valid `entity-map.json` plus its markdown and metadata.

**Best Practices.**
These apply to the entire create phase and should be checked after each step.

- Entities are real-world named organizations only - never firm / attorney / podcast names (Editorial Guideline 3).
- Hold the scope-matched calibration examples in view while generating - calibrate entity count, tier shape, and cluster density against them.
- Vector strength is computed via the formula, never guessed wholesale (Editorial Guideline 1).
- Target counts, tier structure, and entity-type breadth follow `### Quality bar` and `### Quality gates` - do not restate the thresholds, apply them.

If the model generates output that violates any of these, emit a `> NEEDS VERIFICATION:` block at the offending location instead of shipping the claim.

### Surface candidate entities

What is?
The pass that produces the raw candidate set - 50-70 entities pulled from LLM domain knowledge, mined content-gap data, and inherited parent-map entities, covering all required entity-type categories.

- Source: LLM domain knowledge for the practice area, plus mined content-gap data when available, plus carried-forward inherited entities from `Topic Only/entity-map.json` when scope is below.
- Cover all required entity-type categories per `### Quality bar` - breadth across legal concepts, statutes, agencies, insurance, medical, case types, liable parties, evidence, damages, causes, industry practice, credentials.
- Output: 50-70 candidate entities.

### Score and tier entities

What is?
The pass that scores each candidate on the three attributes, computes composite vector strength, assigns tiers, and trims to the target count.

- Score each candidate on Prominence, Relatedness, Popularity (0.0-1.0 each) per Editorial Guideline 1.
- Compute composite vector strength: `vector_strength = (prominence x 0.45) + (relatedness x 0.35) + (popularity x 0.20)`.
- Assign tiers: T1 >= 0.80 (core), T2 0.60-0.79 (major), T3 0.40-0.59 (supporting). Drop entities below 0.40.
- Trim to 40-50 total. If over, drop the lowest-vector entities first, preserving tier balance.

### Cluster and bridge

What is?
The pass that groups entities into contextual layers and identifies the bridge entities that span multiple clusters.

- Group entities into 8-15 contextual layers (procedural / medical / financial / regulatory / adversarial / etc.). Each cluster is one way the domain is sliced, not a bucket of one entity type.
- Document per cluster: cluster name + contextual layer description, entity assignments with vector strengths, why these entities belong together, bridge connections to other clusters.
- Identify 4-6 bridge entities that span >= 2 clusters, ranked by connection count. Bridges carry the highest authority value - they are where the topical graph reconverges.

### Evaluate localization coverage

What is?
The pass that measures jurisdictional coverage and, at tight scopes, inline-asks the producer whether to produce a Localization Supplement.

- Calculate `generic% = (entities with generic names) / total`.
- If `generic% > 30%` AND scope is City / Extension / a tight county or region, inline-ask the producer:
  > "Localization coverage at this scope is X% (Y of Z entities are jurisdiction-specific). Want me to do additional research and produce a focused Localization Supplement table? Recommended for tight scopes where the foundation did not capture enough local signal. Yes / no / skip."
- If yes - run additional research, render an additional Localization Supplement section inside `Entity Map.md` and a corresponding `localization_supplement` block inside `entity-map.json`. The supplement is a SECTION of the map, not a separate file - the deliverable count stays at 3.
- If no / skip - ship the raw map, log coverage % in metadata, leave `localization_supplement: null`.
- When a local entity enters the map, name it per the entity-form-by-scope convention in `## INTERNAL` (Editorial Guideline 4).

### Flag jurisdiction-specific universals

What is?
The pass that annotates state-bound entities at Topic Only scope so they do not leak into the wrong jurisdiction downstream.

- Scan Topic Only entities for any inherently state-bound (forms, statutes, agencies named after a single state, court systems unique to a state).
- Annotate those rows with `(<State> only)` in the entity name column or a `jurisdiction_flag` JSON field. This prevents the SR-1 leak gotcha.

### Render markdown

What is?
The pass that assembles the final artifacts - the `Entity Map.md` source-of-truth with cover + executive summary + tier table + cluster architecture + bridge entities + localization summary + the `## INTERNAL` block, the `entity-map.json` sidecar, and `metadata.json`.

- Assemble `Entity Map.md`: title (H1), executive summary (entity count, tier distribution, cluster + bridge counts, localization scan result), tier table, cluster architecture, bridge entities, localization summary (and Localization Supplement when triggered), then the `## INTERNAL` block.
- Bold every Tier 1 entity row and every bridge entity row (mark bridges with a bridge glyph) in the tier table.
- Serialize `entity-map.json` per `### Outputs -> #### Schema`, including the provenance block.
- Write `metadata.json` with the provenance block per `## INTERNAL`.

## Update

What is?
The update path - modifies an existing Entity Map in place when a prior version exists, preserving any manual edits the producer made since the last skill run.

**Best Practices.**
These apply to the entire update phase and should be checked after each step.

- **Diff before write.** Pull the existing `entity-map.json` + `Entity Map.md`, compare against the proposed new state, surface every changed entity / cluster / bridge before committing the write.
- **Preserve manual edits.** Any entity, score, cluster assignment, or bridge flag that was manually edited since the last skill run keeps its current value. The skill never auto-overwrites a manual edit silently.
- **Flag merge conflicts inline.** When a new auto-generated value disagrees with a preserved manual edit, emit `> NEEDS VERIFICATION: auto-generated value [X] conflicts with manual edit [Y]` at the row; the producer resolves.
- **Stable fileId.** Update uses `files.update` against the existing `Entity Map` Google Doc fileId. Never create a new Doc; never delete-and-recreate.

If the model proposes overwriting a manual edit without flagging it, halt and emit `> NEEDS VERIFICATION:` instead of shipping the change.

### Diff against existing

What is?
The pass that loads the prior map and computes an entity-level diff against the proposed new state so nothing changes silently.

- Read the prior `entity-map.json`, `Entity Map.md`, and `metadata.json` from the resolved scope folder.
- Read the prior `metadata.json` provenance block to recover the last run's sources, counts, localization coverage, and references status.
- Run the Create-phase passes (`### Surface candidate entities` through `### Flag jurisdiction-specific universals`) to compute the proposed new state.
- Compute an entity-level diff: entities added, removed, re-scored, re-clustered, and untouched.

### Merge and resolve conflicts

What is?
The pass that merges the new content into the existing map - new entities in, retired entities out, manual edits preserved, conflicts flagged for the producer.

- Apply the phase-level Best Practices: preserve every manually-edited entity / score / cluster; merge new entities; drop entities the re-score retired.
- Where a new auto-generated value disagrees with a preserved manual edit, emit the `> NEEDS VERIFICATION:` conflict block inline; do not auto-resolve.
- Re-render `Entity Map.md`, `entity-map.json`, and `metadata.json` per `### Render markdown`. Bump the `metadata.json` run date and append the run to the provenance history.
- The shared `## Quality Assurance` phase runs after this phase - QA does not re-run inside Update.

## Quality Assurance

What is?
The gate before `## Ship` - a three-tier check (Best Practices by name, the hardwired Anti-AI Detection two-pass scan, then skill-specific mechanical checks) that runs after whichever branch fired (`## Create` or `## Update`).

**First - check against Best Practices.** The deliverable must align with the contract defined upstream in this file. This is always the first gate; skill-specific checks come after.

- **Quality bar** (Best Practices -> Quality bar) - 40-50 entities across three tiers, tier discrimination real, entity-type breadth, 8-15 clusters, 4-6 bridges, inheritance correct, vector-space chart embedded, no em dashes / banned vocabulary.
- **Sourcing discipline** (Best Practices -> Sourcing discipline) - every score Confirmed against content-gap data / parent-map / Koray RAG, or flagged `> INFERRED:`; any belongs-but-missing entity flagged `> NEEDS CONFIRMATION:`. No silent synthesis.
- **Editorial Guidelines** (Best Practices -> Editorial Guidelines) - Guideline 1 (vector strength computed), Guideline 2 (Topic Only location-agnostic, inheritance correct), Guideline 3 (firm / attorney / podcast names not entities), Guideline 4 (localization is raw research, supplement only on opt-in).
- **Quality gates** (Best Practices -> Quality gates) - full checklist must pass: target counts, tier structure, entity types, inheritance, localization coverage, jurisdiction-flag check, vector-space chart, schema validate, provenance present, artifacts present, Tier 1 + bridge highlights, no em dashes.

**Second - Anti-AI Detection two-pass scan** (canonical doc: https://docs.google.com/document/d/1hp7bxOFRlMhCuhjHNY0j05JrB97-KOFD0XUCQM3gMBU/edit). Mandatory for every text-producing skill. Run the full Section 7 two-pass audit against the deliverable:

- **Pass 1 (mechanical scan):** em-dashes, banned vocabulary (Section 2), banned phrases (Section 3), triadic rhythms and symmetric paragraphs (Section 4), summary-only section closers, date formatting per destination, specific-claims-trace-to-source, no numbered lists in ClickUp, no emojis (unless requested), no clickbait.
- **Pass 2 (skeptical re-read):** restart from the top. Did I actually check every line, or skim? Em-dashes I missed? Banned phrases I rationalized? Triadic rhythms left because they "sounded fine"? Generic entities that should be specific at this scope? Am I sure?
- **On any hit:** fix and re-run Pass 2 until clean. One pass is not enough.

**Third - skill-specific mechanical checks.**

- `entity-map.json` validates against the canonical schema `references/schema/entity-map.json`. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed.
- `metadata.json` provenance block present with at minimum: `run_date`, `koray_rag` (used / unreachable / skipped), `content_gap_source` (auto-detect / manual-upload / llm-only), `keyword_research` (found / not_found), `parent_map` (path or null), `references_status` (used / empty), `schema_status` (validated / missing), entity / cluster / bridge counts, localization coverage %, and supplement status.
- Jurisdiction-flag check: Topic Only entities that are state-bound carry the `(<State> only)` annotation.
- Vector-space chart embedded in the rendered markdown / Google Doc.
- Both write destinations verified: confirm the Drive `Entity Research/{Practice Area}/{Scope}/` folder AND the local mirror at `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/01-entities/` contain the same artifacts.
- INTERNAL section grep test: `grep -L "## INTERNAL" {client-facing-export}` returns zero hits for the client-facing Google Doc.

**On failure:** fix the markdown, regenerate `entity-map.json` and `metadata.json`, re-run all checks. Do not proceed to `## Ship` until QA returns clean.

## Ship

What is?
The publish phase - writes the trio plus `metadata.json` to the practice area's `Entity Research/{Practice Area}/{Scope}/` Drive folder and mirrors the same artifacts to the local Desktop path.

### What ships

- **`Entity Map`** - Google Doc - human-facing canonical view, Roboto typeface, stable fileId, vector-space chart embedded inline.
- **`Entity Map.md`** - Markdown - source-of-truth mirror, retains the `## INTERNAL` block.
- **`entity-map.json`** - JSON - machine-readable, downstream-consumed.
- **`metadata.json`** - JSON (internal) - provenance: sources, counts, localization coverage, supplement status.

### Where it ships

- **Drive:** `templates [master]/AEO/Podcast/Entity Research/{Practice Area}/{Scope}/` in the shared drive `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`); `Entity Research/` folder id `1iKEslJ5JWScmRwjTAEUDrAvBakzQ81Ee`. The `{Scope}` segment resolves per the table in `### Outputs -> #### Drive destination`. This destination is fixed - the skill does not move existing Drive data.
- **Local mirror:** `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/01-entities/` - written every run.
- **Schema:** `~/.claude/skills/pod-2A-entity-research/references/schema/entity-map.json`.

### How it ships

Write to both destinations. On a write error to one, ship to the other and report the partial state.

- **Vector-space chart.** Run the bundled `scripts/entity-vector-space.py` against the scope folder containing the freshly-written `entity-map.json`. It plots entities radially by cluster + vector strength, colors by tier, highlights bridges with a gold border, and writes `Entity Vector Space.png` to a `visuals/` subfolder. Dependencies: `numpy` + `matplotlib` (`adjustText` optional, degrades gracefully). If the script fails, ship without the chart and log it in the gaps report - do not block.
- **Drive write.** Upload `Entity Map.md` as `text/markdown`. Create / update the `Entity Map` Google Doc in-place via `files.update` against the existing fileId (on a `## Create` run with no prior Doc, create once and record the fileId). Upload `entity-map.json` and `metadata.json` as binary. Truncate the markdown source at the first `## Quality Assurance` heading before rendering the Google Doc.
- **Roboto pass.** After the base text Doc is uploaded, run a `docs.documents.batchUpdate` with `updateTextStyle` setting `weightedFontFamily.fontFamily = "Roboto"` over the full document range as the final pass before sharing. Override only when a per-client `brand.json` typography block specifies otherwise.
- **Entity highlights.** Bold every Tier 1 entity row and every bridge entity row in the tier table; embed the vector-space chart inline on its own page.
- **Cover + footer.** Render the cover page (CE logo top, title `Entity Research`, subtitle = practice area, scope line, "Prepared by Case Engine" + date in `Month D, YYYY`). Footer `Case Engine  |  Confidential  |  Page {PAGE}` auto-applied via the Drive API template.
- **Archive.** If the existence check moved prior content to `_archive-{YYYY-MM-DD}/`, the archive folder ships alongside the new artifacts.
- **Local mirror write.** Write the same `Entity Map.md`, `entity-map.json`, and `metadata.json` to the local mirror path. If the Drive write fails but the local write succeeds, surface the partial state in the report - do not silently swallow it.
- **Report back:**

  ```
  Done. Entity Research - {Practice Area} ({Scope}{, Location if applicable}).

   Folder: https://drive.google.com/drive/folders/{folder_id}
   Entity Map (Doc): https://docs.google.com/document/d/{doc_id}

  Counts: {N} entities, {M} clusters, {B} bridges. Tier 1: {t1} / Tier 2: {t2} / Tier 3: {t3}.
  Sources: {parent inherited | content-gap mined | LLM-only}. Localization coverage: {X%}. Keyword research: {found | not_found}.

  Next: pod-2B-keyword-research and pod-2C-virality-research run in tandem with this skill. Downstream: pod-3A-topic-planner, pod-3B-n-gram-table, then Phase 4 Run of Show.
  ```

### Who to Notify

`notify: []` - this skill posts no notifications. The producer is informed via the inline report-back above.

---

## INTERNAL (not for client distribution - auto-stripped from all exports; the reference material and worked examples ride into the local markdown only, never into the Drive Doc)

### Koray RAG query table

When `mcp__ce-services__rag_query` is reachable, run these 5 queries with `rag_name: "koray"`, `top_k: 6`, discard score < 0.40. Use the returned chunks as methodology grounding - the vector-strength formula and tier structure in Best Practices already encode Koray's framework; the RAG call surfaces edge cases for the specific practice area.

| # | Query |
|---|-------|
| 1 | `entity attributes connections topical authority for {practice_area}` |
| 2 | `entity types entity relationship semantic content network legal` |
| 3 | `topical map expansion entity clustering contextual layers for legal practice areas` |
| 4 | `vector strength prominence relatedness popularity entity attribute prioritization` |
| 5 | `contextual bridges topical map connected topics content network` |

### Entity form by scope

When a local entity DOES enter the map, name it per this convention (additive - the naming format, not a substitution rule):

| Scope | Entity form | Acronym convention | Separator | Entities per row |
|---|---|---|---|---|
| Topic Only | Generic categories | not needed | `,` | 1-2 |
| State-level | State instance + 2+ representative cities | optional | `;` | 2-3 |
| County / Region | County or region instance + relevant cities within | optional | `;` | 2-3 |
| City-level | Full jurisdictional stack: federal -> state -> county -> city -> named institutions | **standard** `Full Name (ACRONYM)` | `;` | 3-5 |

Example: `Houston Police Department (HPD)` is the named city-level form. `Police Department` is the generic Topic Only form. Both are valid - which appears depends on whether the entity scored at this scope, not on a forced substitution.

### Provenance block

`metadata.json` must include a provenance block with at minimum: `run_date`, `koray_rag` (used / unreachable / skipped), `content_gap_source` (auto-detect / manual-upload / llm-only), `keyword_research` (found / not_found), `parent_map` (path or null), `references_status` (used / empty), `schema_status` (validated / missing), entity / cluster / bridge counts, tier distribution, localization coverage %, and supplement status.

### Source inventory

Records every input the run consumed: the resolved content-gap report path and source (local / Drive `_inputs/` / llm-only), the parent `entity-map.json` path when scope is below Topic Only, any `keyword-research.json` mined, the Koray RAG status, and the calibration examples used.

### Build script note

The bundled `scripts/build-entity-map-docx.py` was the legacy DOCX renderer. The canonical client-facing artifact is now the Google Doc rendered from `Entity Map.md` via the Drive API with a Roboto typeface pass. The DOCX script is retained for offline rendering only and is not part of the `## Ship` path.

---

## Learning & Iteration

- [ ] After each run, note edge cases, localization-coverage outcomes, jurisdiction-flag catches, and content-gap availability; append GOOD / BAD / EDGE CASE entries to `references/examples/`.
- [ ] Track recurring jurisdiction leaks - if the same state-bound entity surfaces unflagged across runs, tighten `### Flag jurisdiction-specific universals`.
- [ ] Watch for maps shipping under 40 or over 50 entities; if it recurs, tighten the `### Score and tier entities` trim guidance.

## Change Log

| Date | Change |
|---|---|
| 2026-04-20 | Initial co-work version. Drive-native. Koray methodology inlined. Vector-space visual moved to local post-step. Inheritance model across Topic Only / Location / Extension. |
| 2026-04-20 | Consolidated all rules under Best Practices; removed duplicates. Restructured: Input above Best Practices; Output, Examples, Routing at the bottom. Pipeline split into Research and Run of Show. |
| 2026-04-27 | Structural restructure: methodology rules moved to Best Practices as H3 peers; Localization rewritten as raw-research philosophy with the 30% supplement-trigger; Run Vector Analysis rebuilt as a 9-step procedural flow. |
| 2026-04-27 | **v1.0.0 ship cut.** Canonical-reference pattern locked: brand styling from `Case Engine Branding`, folder layout from `Podcast Drive`, write protocol from `Push to Drive`, JSON shape in bundled schema. Bundled scripts + READMEs + examples added. |
| 2026-05-14 | **v2.0.0** - merged cowork v1.0.0 + original `pod-2-entity-research`. Dual-mode via runtime capability probe; output schema identical across modes. SR-1 jurisdiction gotcha promoted to a worked example. Quality Assurance H2 added. Frontmatter: `name: pod-2-entity-research`, `skill_kind: hybrid`. |
| 2026-06-17 | **Canonical destination gate added.** Hard, pre-write gate in `### Quality gates` asserts the target parent folder is a descendant of the dedicated `Entity Research/` library (folder id `1iKEslJ5JWScmRwjTAEUDrAvBakzQ81Ee`) at the exact `Entity Research/{Practice Area}/{Scope}/` path before any artifact (Entity Map Doc, `Entity Map.md`, `entity-map.json`, `metadata.json`) is written; a client/firm episode delivery folder (`{Firm} Podcast/Episodes/EP{N}: ...`) hard-fails. No caller / workflow / convenience override may redirect the artifacts; such an instruction is itself the failure. Added matching cross-reference in `### Outputs -> #### Drive destination` and a gotcha. Prompted by a workflow override that wrote research artifacts into client delivery folders. Owner Gabe Jordan. Revert: delete the gate bullet, the Drive-destination cross-reference paragraph, the delivery-folder gotcha, and this row to restore prior behavior. |
| 2026-07-10 | **Three-field geo model alignment** (Gabe directive, Whalen scoping). Stamped the canonical geo model - **Targeting strategy** / **Optimization scope (show anchor)** / **Episode geo target** - across the skill: rebuilt Path B inline-workaround questions and labeled the Path A greeting with the exact field names; added **Editorial Guideline 5** carrying the "anchor scope != per-episode target" rule and clarifying that this entity map is built at the Optimization scope (show anchor) while per-episode Episode-geo-target research reuses / derives from the matching location-scoped map (no rebuild). Preserved the no-city-quota ceiling-not-floor principle and the existing Topic Only / Location / Extension scope model and Universal State Check / cached-artifact-reuse behavior. Schema `references/schema/entity-map.json` PATCH-bumped 1.0 -> 1.0.1: enriched `scope` + `location` field descriptions to note they correspond to the show anchor (no field shape change; non-breaking). Owner Gabe Jordan. |
| 2026-05-20 | **v3.0.0** - renamed `pod-2-entity-research` -> `pod-2A-entity-research` (folder + slug + frontmatter `name`). Full structural refactor to the canonical CE skill structure mirroring `pod-5-n-gram-table` v3.0.0. Killed Mode A / Mode B environment-name branching - replaced with `### Probe environment` capability probe (FS-read / FS-write / Drive / RAG tiers); local mirror writes when the FS-write probe succeeds. Frontmatter completed (`skill_kind`, `modes: multi`, `inputs`, `outputs`, `notify`; `version`/`date`/`owner` moved to a `metadata` block). Best Practices restructured to the canonical contract H3s (Inputs / Outputs / Framing / Quality bar / Sourcing discipline / Editorial Guidelines / Quality gates / Gotchas / Iteration log); vector / tier / cluster / bridge / inheritance / localization methodology relocated into Quality bar + Editorial Guidelines + the deliverable-shaped Create buckets. SOP rebuilt as H2 phase siblings (Checks / Prepare Inputs / Create / Update / Quality Assurance / Ship); `## Capture data` -> `## Prepare Inputs`, `## Push to Drive` -> `## Ship`, `## Backfill` folded into `## Update` + `## Ship`. QA rewritten as the canonical three-tier gate with the hardwired Anti-AI Detection two-pass scan and an On-failure recovery line. Workflow demoted to H3 with the locked Research-phase diagram (2A/2B/2C in tandem) + YOU ARE HERE; downstream stages drawn as named boxes without codes (downstream numbering pending). `references/schemas/` fixed to `references/schema/`. Owner Gabe Jordan. |
