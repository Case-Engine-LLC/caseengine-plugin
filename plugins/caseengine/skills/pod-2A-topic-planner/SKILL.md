---
name: pod-2A-topic-planner
description: >
 Generate the ranked podcast Episode Plan for a signed client - 12 main episodes + 3-5 additional
 topics + a full INTERNAL reserve catalog. Ingests entity research, keyword research, content-gap,
 and optional virality research into one corpus, scores every candidate topic on an 11-signal
 weighted model with a corroboration mechanic, then compiles scored topics into episode-sized
 coherent groups. Use whenever someone says "topic plan for [client]", "podcast topics for
 [practice area]", "what episodes should we record", "plan episodes for [client]", "run podcast
 topics", "episode plan for [client]", "/topic-planner", or "/pod-2A-topic-planner". Asks up front
 whether the client wants a specific practice-area episode breakdown, then auto-builds the
 per-episode n-gram tables and rolls the questions into the plan before shipping.
skill_kind: hybrid
modes: single
inputs: [entity-map.json, keyword-research.json, content-gap-report, virality-research.json, podcast-overview.md, koray-rag]
outputs: [json, markdown, docx, gdoc]
notify: []
metadata:
  version: 4.7.0
  date: 2026-07-31
  owner: Gabe Jordan
---

# Podcast Topic Planner

> **Drive write governance:** All Drive operations (create, update, rename, move) follow [Push to Drive](https://docs.google.com/document/d/1831TsbxcyNGPmq67zblA5rC66U-XQv20mVsNovFqjfg/edit) (canonical doc at `templates [master]/Skills/Push to Drive`). Revise in place via `files.update` against the existing fileId - never delete-and-reupload (breaks the fileId/URL chain and silently kills every downstream reference).

> ## POST-PUBLISH EDIT RULE - READ FIRST
>
> `scripts/topic-plan-formatting.sh` is a FIRST-PUBLISH ONLY script. It re-uploads the markdown to the Drive Doc, which WIPES every comment, suggested edit, and live collaborator change in the Doc. Acceptable on first publish (the Doc is empty). Never acceptable after the Doc has been shared with anyone - clients leave comments, AMs leave suggestions, producers track changes, and a full re-format destroys all of it.
>
> The rule is binary:
>
> | Doc state | What to run | Why |
> |---|---|---|
> | Empty / not yet published | `scripts/topic-plan-formatting.sh` (full rebuild - cover + Roboto + tables + INTERNAL + header/footer + column widths) | First publish, no collaborator content to preserve. |
> | Published and shared with ANYONE (client, AM, producer, internal review) | `scripts/topic-plan-surgical-edit.sh --find "..." --replace "..."` (Docs API `replaceAllText`) | Preserves comments, suggestions, formatting overrides, every collaborator edit. Touches only the exact text being changed. |
>
> There is no third option. Do not run the formatter "just to refresh styles" on a published Doc. Do not re-upload the markdown to "sync the source." If style drift becomes a real problem, the fix is to add an idempotent style-only pass to the surgical script, not to nuke the Doc.
>
> Markdown source-of-truth still updates locally. Edit the canonical `topic-plan-v{n}.md` on disk so downstream skills read the current state, but do NOT push that md to the live Doc via `files.update`. Use the surgical script to mirror the change into the Doc.
>
> Regenerating `.docx` is safe at any time. `scripts/topic-plan-to-docx.sh` reads only the local md and writes only the local docx; it never touches the Drive Doc.
>
> If you have already wrecked a Doc by re-running the formatter, the comments are gone. Apologize, ask whoever was working in there to re-add what they had, and never do it again on that Doc.

### What is

The post-contract Episode Plan for a signed client's podcast. It produces a ranked set of episodes - 12 main, 3-5 additional, plus a complete INTERNAL reserve catalog - by ingesting all upstream research into one corpus, scoring every candidate topic on an 11-signal weighted model, compiling the scored topics into episode-sized coherent groups, and forming the plan. The episode boundary is an OUTPUT of compilation, not an upfront guess.

The plan ships as four artifacts: the canonical markdown source, a schema-validated JSON sidecar, a Word `.docx`, and a branded Google Doc. The client-facing view truncates at the `# INTERNAL` H1; everything below it (reserve catalog, methodology detail, provenance, branded-search benchmark) is operator-only. Downstream, `pod-2B-n-gram-table` reads the ranked JSON to decide which n-gram tables to build and in what order; `pod-3A-ros-template` and the rest of the Run of Show pipeline consume the locked episodes per-episode.

### Workflow

Topic Planner is part of **Phase 2 (Planning)** of the podcast pipeline - it ingests every upstream research artifact and produces the Episode Plan; `pod-2B-n-gram-table` is the direct downstream consumer.

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

1. **Client architecture (from the Greeting)** - client name, the **Optimization scope (show anchor)**, the **Targeting strategy** (single-location vs multi-location), extensions, and audience are collected at runtime in the Greeting (see `### Geo model`). An optional `podcast-overview.md` auto-fills them when present; otherwise the skill asks.
2. **pod-1A-entity-research** (required) - the entity map this skill ranks topics from. If no entity map exists at the target scope, fall back to keyword research (the keyword-research fallback path).
3. **pod-1B-keyword-research** (required signal) - search-demand data: MSV, PAA stacks, related searches. Drives the Demand bucket.
4. **pod-1C-virality-research** (optional signal) - trend / momentum data. When present, adds the `virality` signal and the `trend` corroboration family. When absent, its weight redistributes; ranking is never deflated.
5. **pod-2A-topic-planner** (this skill) - ingests Steps 1-4 into one corpus, scores every candidate, compiles into episodes, forms the plan.
6. **pod-2B-n-gram-table** - the direct downstream consumer, invoked as a mandatory step inside this skill. The `### Build the n-gram tables` step in `## Create` auto-invokes it for every locked episode (main 12 AND additional); its question output feeds the client-facing `## Episode Breakdown` roll-up.

### Trigger phrases

- `/topic-planner`
- `/pod-2A-topic-planner`
- "topic plan for [client]"
- "podcast topics for [practice area]"
- "what episodes should we record for [practice area]"
- "plan episodes for [client]"
- "run podcast topics"
- "episode plan for [client]"
- "generate podcast topics from entity map"
- "what should {client} record next"
- "prioritize {client} episodes"
- "keyword research for podcast topics" (keyword-research fallback path)
- "podcast topics without entity map" (keyword-research fallback path)

### Greeting

I'm the Podcast Topic Planner. I ingest all of a client's research - entity map, keyword research, content-gap, and virality if it ran - score every candidate topic on an 11-signal model, and compile the winners into a recording-ready Episode Plan: 12 main episodes, 3-5 additional topics, and a full reserve catalog for the team.

Tell me the client and the practice area (or areas) you want planned.

One question before I run, and it is required - I will not start the plan until you answer it:

```
Topic mix (REQUIRED - the skill will not fire without this). How should the 12
main episodes split across practice areas? You must either give me a mix or
explicitly tell me to use the default. Give a mix as a sentence.

Examples:
  - "50% car accidents, 40% truck accidents, 10% rideshare"
  - "8 episodes family law, 3 criminal defense, 1 bonus on CPS"
  - "split evenly between truck and motorcycle accidents"

To take the CE default instead, reply "use the default mix" and for a
personal-injury firm I'll apply it (Car Accidents 25% (3 episodes), Med Mal 17%
(2), Truck 17% (2), Cross-Service Roundup / Wrongful Death / Founder Story /
Slip & Fall / Bicycle-Pedestrian 8% each (1 episode each)), trimmed to the areas
the firm actually practices. For a non-PI firm, "use the default mix" means let
pure research + scoring decide how many episodes each area earns. I will not
proceed on silence - you must provide a mix or say "use the default mix."
```

If the client has multiple verticals, I sequence one plan per practice area by research priority, following the topic mix you gave. I'll also drop any episode you flag as already having a Run of Show. Once the plan is scored and compiled, I build the n-gram tables for every locked episode automatically and roll the questions into the plan, so you QA the topics and the actual questions in one deliverable.

---

## Best Practices

The WHAT contract. Cross-cutting rules, framing, and quality bars. Execution steps and HOW live in the SOP below; rules referenced from the SOP live here.

### Inputs

What is?
The research artifacts and client context the skill ingests into one scoring corpus - entity map (preferred), keyword research, content-gap, optional virality, plus client intel - resolved from whatever capabilities the runtime probe finds reachable.

#### Required

- **Client name** - exact firm name. Used for Drive folder resolution, the cover page, and frontmatter.
- **Practice area(s)** - the vertical(s) to plan episodes for (e.g., "truck accidents", or "family law + criminal defense"). Multiple verticals get sequenced one plan per area.
- **Entity map** - `entity-map.json` from `pod-1A-entity-research` at the target scope (preferred path). Carries the entity graph that feeds the four Authority signals. If no entity map exists at the target scope, the skill does NOT block - it falls through to the keyword-research fallback path (see `### Gotchas`).
- **Keyword research** - `keyword-research.json` from `pod-1B-keyword-research`. Carries MSV, PAA stacks, and related searches that feed the three search-demand signals. Present on both the entity path and the keyword-research fallback path. When entity research is the entry point but keyword research is also present, both feed the corpus.

#### Optional

- **Content-gap report** - `entity-analysis.json` + `cluster-descriptions.json` + SERP data from the content-gap MCP. Feeds `gap_opportunity` and the `serp_features` signal (AI Overview, video pack, featured snippet, image pack presence per query). When unavailable, `gap_opportunity` defaults to 0.5 (neutral) and `serp_features` to 0.0 for all topics, both logged in metadata.
- **Virality research** - `virality-research.json` from `pod-1C-virality-research`. Adds the `virality` signal and the `trend` corroboration family. When absent, its weight redistributes proportionally across the present signals (see `references/scoring-model.json` invariants).
- **Podcast overview** - an optional `podcast-overview.md` / `podcast-overview-{client-slug}.md` architecture doc (client name, anchor scope, extensions, audience, content philosophy, episode-length target, show goals). Read as a client-intel modifier on priority order when present; when absent, the Greeting collects what it needs.
- **Fathom transcripts** - onboarding + strategy meeting transcripts. One optional client-intel input among others (NOT a mandatory dominant scoring layer - see `### Gotchas` for the v4.0.0 change). Used to sense-check the practice-area breakdown and surface stated anti-patterns ("don't pitch X, we refer that out").
- **Practice-area breakdown** - the user's sentence from the Greeting governing how many episodes each practice area gets. Captured verbatim into `metadata.practice_area_breakdown`.
- **Manual / editorial candidate topics** - topics the operator supplies that research will not surface (forward-looking or trend topics with no search data yet). They enter the candidate set, get scored on whatever signals exist, and are marked editorial in the `## Topic Ideas` `Notes` column (see `## Prepare Inputs -> Assemble the corpus`).

#### Auto-read (no action required)

- **`references/scoring-model.json`** - the canonical scoring model. `scripts/score-topics.py` loads it at runtime; the skill never restates its numbers.
- **`references/topic-seed-catalog.json`** - the seed taxonomy: legal domain -> practice areas -> seed episode topics. Read by `### Resolve client, domain, and practice areas` to seed the candidate set before research-derived topics merge in. Personal Injury and Family Law are populated; Criminal Defense is stubbed.
- **`references/iteration-log.json`** - read at run-start by `### Orient`; open + in-progress entries surface as known issues.
- **`references/e1-founder-interview-questions.md`** - the canonical Episode 1 founder-interview question set (21 questions, S1-S5 + Outro, per-client tokens). Read by `### Build the n-gram tables` and the `## Episode Breakdown` render step; E1 is never n-gram-built.

#### Tools the skill calls

This skill runs locally in Claude Code and calls its tools directly - it assumes they exist and uses them in this priority order. On a tool error, it skips that source and degrades to the next; it never probes for availability first.

- **Local filesystem read** - for research artifacts on disk: `entity-map.json`, `keyword-research.json`, `virality-research.json` under the local research mirror. Fastest path, no Drive round-trip.
- **`gws drive`** (or `mcp__claude_ai_Google_Drive__*` connector) - for the same research artifacts when they live only on Drive.
- **`mcp__content-gap__*`** - for live SERP / PAA / query-fanout when no cached content-gap report exists.
- **`mcp__ce-services__rag_query`** (`rag_name: "koray"`) - for methodology grounding on contextual layers + topical authority.
- **`op://` 1Password resolution** - for any credential. CE uses 1Password as the single source of truth for credentials. No env vars, no hardcoded keys, no credentials pasted into conversations.
- **User-supplied materials** in the greeting (pasted research, dropped files, the practice-area breakdown) and user interview for hard requirements still missing - the always-available floor.
- **Hard requirement** - at least one usable research source (a local artifact, a Drive artifact, or user-supplied research). With user-supplied + interview always available as a floor, the skill never hard-blocks; it degrades to the keyword-research fallback or manual mode.
- **Behavior on a tool error** - skip that source and degrade to the next; degrade to the keyword-research fallback path when no entity map resolves, or manual mode when neither entity map nor keyword research resolves (see `### Gotchas`).

### Outputs

What is?
The Episode Plan, shipped as four artifacts - one canonical markdown source plus three renders of it - landing in the per-client Drive Topic Plan folder, with `pod-2B-n-gram-table` as the direct downstream consumer of the JSON.

#### Output formats

CE-wide default trio, plus a `.docx` layer the deliverable type calls for. The `.md` is the build source FOR THIS SKILL'S OWN RENDER PASS only - it is NOT the canonical lineup. **Once the Topic Plan is published, the live Google Doc is canonical:** the client sees that Doc and makes manual adjustments (cuts, swaps, topic changes) directly on it, so it - not the local `.md`/`.json` - is the authoritative episode lineup from that point on. Every downstream skill (`pod-3B`, `pod-4A`, `pod-4B`, `pod-4C`) MUST read the episode topics from the live Google Doc, never from the local `.md`/`.json` (those go stale the moment the client edits the Doc). When this skill re-cuts the plan, mirror the change into the live Doc via the surgical script so the Doc stays the source of truth; never let a local re-cut diverge silently (the Eberst E5 incident, 2026-06-19: a local v3 md swapped E5 to a topic the firm does not handle, and downstream built the wrong episode because it trusted the md over the Doc).

- **JSON** - `topic-plan-v{n}.json` - machine-readable sidecar. Validates against `references/schema/topic-plan-schema.json`. `pod-2B-n-gram-table` and any programmatic consumer read this.
- **Markdown** - `topic-plan-v{n}.md` - local source-of-truth mirror. Retains the `# INTERNAL` reserve block. Hand-edited when refinement is needed; the other three artifacts re-render from it.
- **Google Doc** - human-facing canonical view at the Drive destination below. Created / updated in-place via `files.update` against a stable fileId so the URL never breaks for downstream links. Typeface: Roboto across every text layer (see `### Quality bar` -> font lock).
- **DOCX** - `topic-plan-v{n}.docx` - Word / PDF-friendly local copy, rendered by `scripts/topic-plan-to-docx.sh` from the baked-in reference template.

#### What ships

- **`topic-plan-v{n}.md`** (Markdown) - canonical source. Client-facing sections above `# INTERNAL`; reserve catalog and operator detail below.
- **`topic-plan-v{n}.json`** (JSON) - schema-validated structured episode data, including the full scored-topic set.
- **`topic-plan-v{n}.docx`** (DOCX) - pandoc render using the baked-in reference docx. Page header auto-patched to `Case Engine | Podcast Topic Plan | {anchor}`.
- **Drive Doc** (Google Doc) - branded: cover page (logo, CE Blue subtitle, firm name, location, date), Roboto across every text layer, CE Blue table header rows with zebra body rows, `# INTERNAL` marker with CE Blue top border, page header/footer.

All four ship every run. A run that produces only a partial set is a contract violation - QA asserts presence of all four (see `## Quality Assurance`).

#### Drive destination

Per [Client Folder Structure](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU/edit) -> Map 5 -> `AEO/Podcast/Topic Plan/`, the four artifacts land in a per-practice-area subfolder:

```
.Client Folders/
└── {Client Name} // {start-date}/
    └── AEO/
        └── Podcast/
            └── Topic Plan/
                └── Topic Plan: {practice_area} // {client_name}/
                    ├── topic-plan-v{n}.md
                    ├── topic-plan-v{n}.json
                    ├── topic-plan-v{n}.docx
                    └── Topic Plan: {practice_area} // {client_name}  (Google Doc)
```

One subfolder per practice area - a client doing car accidents + truck accidents gets two. Upstream of `Episodes/`. Never inline the full client-folder path; resolve it at runtime (see `## Ship -> ### Where it ships`).

#### Local mirror

The four artifacts also mirror to `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/02-topics/`. `{topic-slug}` is the slugified practice area; `{episode-slug}` is the slugified scope label. Same naming as `pod-1A-entity-research`'s local mirror so the research tree stays internally consistent. `pod-2B-n-gram-table` reads from here. Written on every run.

#### Schema

`references/schema/topic-plan-schema.json` - the structural contract: heading order, table column definitions, required fields, validation rules. Every run validates the JSON against it before shipping. Edit the schema first when sections, columns, or fields change, then update this skill's prose, then bump the schema version.

#### Sections - what goes where

Client-facing artifacts truncate at the `# INTERNAL` H1; the operator copy keeps everything.

| Section | Client-facing Doc | INTERNAL (operator) |
|---|---|---|
| `# Podcast Topic Plan` H1 + cover frontmatter | yes | yes |
| `## Show Identity` (5 fields) | yes | yes |
| `## Methodology: How topics are selected` (1-2 prose paragraphs) | yes | yes |
| `## The 12-Episode Plan` (main table) | yes | yes |
| `## Additional Topics` (additional table) | yes | yes |
| `## Episode Breakdown` (per-episode question roll-up, one table per episode) | yes | yes |
| `## Research Sources` (Drive nav table) | no | yes |
| `## Topic Ideas` (every candidate, original ranking + `Notes` disposition) | no | yes |
| `## Selection Methodology Detail` | no | yes |
| `## Episode 1 Branded Search Benchmark` | no | yes |
| `## Provenance` | no | yes |

#### Write destinations

Both destinations are written every run. On a write error to one, the skill ships to the other and surfaces the partial state in the report.

- **Drive** - `gws drive create / update` (or the `mcp__claude_ai_Google_Drive__*` connector) for the Drive Doc + `.md` + `.json` + `.docx` siblings at the canonical Map 5 slot.
- **Local mirror** - local FS write at the local mirror path, alongside the Drive write.
- **Behavior on a write error** - if one destination errors, ship to the other and report the partial state. If both error, hard-fail with a clear message naming what is missing; never silently lose the deliverable.

#### Examples

`references/examples/topic-plan-examples.md` - GOOD / BAD / EDGE CASE labeled sections per CE convention. Reference-quality runs (e.g., `good--sutliff-stout-car-accidents-client-level.md`) calibrate quality and format.

#### Routing

- **Upstream:** `pod-1A-entity-research` (required), `pod-1B-keyword-research` (required signal), `pod-1C-virality-research` (optional signal).
- **Downstream:** `pod-2B-n-gram-table` (direct - reads the ranked JSON), then `pod-3A-ros-template` / `pod-3B-client-ros` / `pod-3C-client-guide` per locked episode.
- **Refresh:** re-run when new research lands at the target scope, when the client changes the practice-area breakdown, or when an AM wants to reweight the plan. New version is `v{n+1}`; never overwrite a prior version.

#### Handoff Contract

- `pod-2B-n-gram-table` reads `topic-plan-v{n}.json` to decide which n-gram tables to build and in what order. It consumes the ranked episode array (each episode object carries `rank`, `title`, `theme`, `keywords`, `search_volume_total`, `authority_score`, `corroboration_flag`, `intent_stage`, `primary_cluster`, `entity_ids`) plus the `topics_by_score` array.
- **Schema-change note for v4.0.0:** the JSON now carries `authority_score` (the 11-signal weighted score from `score-topics.py`) and a `corroboration_flag` per episode, plus a top-level `topics_by_score` array (every candidate in original ranking order). The legacy `authority_score_linear` 5-dimension shape is replaced. Downstream consumers that read `rank`, `title`, and the episode metadata are unaffected; consumers that read the old per-dimension keys must move to the new signal set. The schema version bump documents the change.
- Drive Doc fileId is permanent across versions - every revision is in-place via `files.update`. Downstream links never break.

### Framing

The Episode Plan is a research-grounded recording roadmap, not a marketing teaser. It tells the producer and AM exactly which 12 episodes to record, in what order, and why - and gives them a tagged reserve catalog so the show can be swapped or extended over time without re-running the planner. The client-facing view is clean and confident; the operator view below `# INTERNAL` is dense and shows its work. The episode boundary is something the skill decides by compiling scored topics, not something it assumes up front.

### Geo model

Three fields govern how geography flows through the plan. Use these exact labels; every pod skill carries the same model. The Topic Planner is where the per-episode geo target is **assigned and confirmed** - the earlier skills set the anchor, this skill hands each episode its city.

1. **Targeting strategy** - `single-location` vs `multi-location`. Does the firm serve and rank one city or several? It drives episode format: single-location -> Full episodes (~20 questions, ~50-55 min) that all share the one anchor city; multi-location -> one Mini episode per target city (10-12 questions, ~30-35 min), no single primary episode.
2. **Optimization scope (show anchor)** - City / State / County / Regional. What the podcast *as a whole* is optimized to rank for; it governs research breadth and the overall show. A multi-location firm usually anchors at State or Regional to own the whole footprint; a single-location firm anchors at City.
3. **Episode geo target** - the specific city each individual episode is built to rank for. This skill assigns it per episode: in multi-location the show anchors broad (e.g. the state) while each episode targets a different city (one for Denver, one for Aurora, one for Centennial); in single-location every episode shares the one anchor city.

**Anchor scope != per-episode target.** The show can be optimized for a broad scope (e.g. the whole state) while each episode targets a specific city we're trying to rank for. Research runs at the anchor breadth; each episode's questions and titles emphasize that episode's target city naturally - a ceiling, never a forced quota. City emphasis is natural, never a mandated floor (the no-city-quota / natural-tonality principle): never force-feed the target city into every question or the chapter title. Getting this wrong is how a multi-location statewide firm ends up with 12 episodes that all sound like one city, or how city emphasis silently becomes a city floor.

Where the fields fire in this skill: the **Optimization scope (show anchor)** governs research breadth and the overall show (Prepare Inputs ingests at anchor breadth); the planner assigns each episode its **Episode geo target** at `### Form the episode plan`; the **Targeting strategy** flag decides the episode format (single-location -> Full episodes sharing the one anchor city; multi-location -> one Mini episode per target city). EP1 (Founder Story) and EP2 (flagship ebook anchor) keep their fixed rules - their geo target is the show's home / anchor city, since they anchor the whole show rather than one satellite market.

### Quality bar

- **Episodes are compiled, not guessed.** Every episode boundary traces to a compilation decision over scored topics. The skill never starts from "this cluster is 1-3 episodes" and scores the guess afterward.
- **No pre-filtering on perceived strength.** When assembling the candidate topic set, never drop a research-supported topic because it looks like a "weak episode." Exclude ONLY genuine non-topics: entertainment / gore video searches, navigational queries (phone numbers, portals), pure brand head terms. Everything with real research behind it becomes a scored candidate - the score decides if it is weak, not a judgment pass. A pre-filter once silently hid a real topic (Distracted Driving) from a client run; the model makes that call.
- **Every episode earns its rank on the model.** Rank order traces to the 11-signal `authority_score` plus the corroboration mechanic. No episode lands in the main 12 on vibes.
- **Rationale states the real drivers.** Each Rationale cell names the actual top-contributing signals and calls out corroboration when present. No generic filler like "high authority score" (see `### Editorial Guidelines -> Guideline 2`).
- **No duplicate episodes.** No two episodes in the main 12 or additional set cover the same primary concept. Detection signal: entity overlap > 50% OR primary-keyword overlap > 40% between two episodes' source research. When that fires, bundle into one episode with a wider angle.
- **Original ranking stays recoverable.** The INTERNAL `## Topic Ideas` table preserves every candidate in unmodified `authority_score` order so a manual reweight never destroys the research baseline.
- **Practice-area breakdown is honored.** If the user gave a breakdown, the episode mix matches it. If not, pure scoring decides.
- **Font lock - Roboto.** Every Google Doc text layer (cover, body, headings, table cells, headers, footers) is Roboto, applied as the final formatting pass. Matches every CE house Doc. Per-client `brand.json` typography overrides only when present; falls back to Arial only when the Docs API is unavailable, logged as `branding: "font-fallback-arial"` in metadata.

### Sourcing discipline

The Confirmed / Inferred / Unknown three-state pattern. Never block, always ship, never silent.

- **Confirmed** - claim traces to a specific research artifact, DB row, or the user's stated breakdown. Ship as-is, no marker.
- **Inferred** - a sensible default applied when the source is insufficient (e.g., `gap_opportunity` defaults to 0.5 when no content-gap data; keyword-fallback Authority signals default to 0.0). Ship the value with a `> INFERRED: {what + why}` flag and log it in metadata.
- **Unknown / NEEDS VERIFICATION** - no source and no defensible default. Ship with a `> NEEDS VERIFICATION: {what's missing}` block, never silently synthesized.

### Editorial Guidelines

Cross-cutting content rules for the client-facing prose. The SOP points back here; the rule lives once.

**Guideline 1 - client-facing prose is anti-AI clean.**

- **Banned:** em-dashes; `step / step-by-step`; `frequently asked questions` as a heading; `bottom line / overview / conclusion / in short / in essence`; empty headings (a heading immediately followed by another heading); sentences starting with prepositions; a separate "Sources" section; `leverage / navigate / delve / seamless / robust / tapestry`; openers like `Built for / Designed for / Crafted to`; `Heavy emphasis on`; triadic "X, Y, and Z" stacking when one will do.
- **Allowed:** plain hyphens, short declarative sentences, entity-first sentence structure, specific claims grounded in the research.
- **Why:** the client reads the Methodology and Show Identity prose first; AI-tell phrasing reads as templated and erodes trust. Reference: Koray consult `consult__41--2026-04-23` in the koray-rag.
- **Where it fires in the SOP:** `## Create -> ### Render the topic plan` (client-facing prose pass), enforced at `## Quality Assurance` tier two. Applies ONLY to prose above `# INTERNAL`; tables stay factual and untouched; the INTERNAL section is operator-facing and allowed to be denser.

**Guideline 2 - the Rationale column names real signals.**

- **Banned:** generic filler - "high authority score", "strong overall", "good fit", "scored well".
- **Allowed:** the actual top-contributing signals plus the corroboration flag - "High-confidence: surfaces as a PAA question, carries a strong related-search cluster, and maps to core entity {X}."
- **Why:** the AM uses the Rationale to defend the plan to the client. A rationale that names the drivers is auditable; filler is not. The corroboration mechanic in `references/scoring-model.json` exists precisely so the rationale can lead with breadth-of-evidence.
- **Where it fires in the SOP:** `## Create -> ### Form the episode plan`. `score-topics.py` emits a draft rationale per topic from the signal scores + corroboration flag (per the `rationale` rules in `scoring-model.json`); the skill tightens it to one sentence, hard cap 200 characters.

### Quality gates

- All four artifacts present at end-of-run; JSON validates against `references/schema/topic-plan-schema.json`.
- Client-facing structure renders in canonical order: `# Title` -> cover frontmatter -> `## Show Identity` -> `## Methodology` -> `## The 12-Episode Plan` -> `## Additional Topics` -> `## Episode Breakdown` -> `# INTERNAL` cut.
- `## Episode Breakdown` present above `# INTERNAL` with one entry per episode (main 12 AND additional). Episodes 2-12 + additional topics are headed `Episode N: {title}` and render a `Question` / `Keywords` / `Rationale` table sourced from that episode's `pod-2B-n-gram-table` output. The `Keywords` cell is NOT the raw n-gram phrase list - each phrase is resolved to its MSV from keyword research and the cell is formatted by `keywords_cell()` (`{summed MSV}/mo Total Search Demand`, then the `phrase - X/mo` list). Episode 1 is the standing exception - headed `Episode 1: Founder Story` (theme, not title), it renders the canonical Founder Story interview question set as ONE table with two columns, `Question` / `Rationale`, the 21 founder-interview questions top to bottom and unnumbered. E1's `Rationale` is a few hard-coded words naming what the question accomplishes in the interview (establish credibility, position as expert, build local trust, emotional close) - distinct from the research-signal Rationale on episodes 2-12. E1's table has no Keywords column and no Segment column.
- Main table columns in exact order: `#`, `Topic`, `Theme`, `Keywords`, `Rationale`. Widths `[32, 134, 70, 116, 116]` PT (sum 468). No standalone `Search Volume` column.
- Additional Topics table columns in exact order: `Topic`, `Theme`, `Keywords`, `Rationale`. Widths `[150, 80, 128, 110]` PT (sum 468). No standalone `Search Volume` column and no `Swaps for` column.
- Keywords cells follow ONE locked format, built by `scripts/lib_doc_table.py` -> `keywords_cell()` (never hand-authored, so it renders right 100% of the time): line 1 is `{summed MSV}/mo Total Search Demand` (volume first, then the label, comma-grouped thousands), then a line break, then the comma-separated keyword list `keyword - X/mo, keyword - X/mo` - each keyword carrying its own MSV, highest MSV first. The line break between the two parts is the only break; the keyword list stays single-line comma-separated. Episode 1 uses the same format with the label `Total Branded Search Demand`.
- Rationale cells under 200 characters each; schema warns at 130.
- Show Identity block has all five fields (Podcast Name, Tagline, Podcast Description, Audience, Topic Mix) and they match across `.md`, `.json`, and the Doc.
- EP1 is `The Founder Interview` with Theme `Founder Story` (fixed); its row is populated from the branded-search benchmark.
- EP2 is the flagship ebook anchor - the best ebook-worthy topic that also has real search demand (not a low-demand wow-factor topic); see `### Form the episode plan`.
- `# INTERNAL` section present with `## Topic Ideas` AND the operator subsections, in the order defined in `### Outputs -> #### Sections - what goes where`.
- No em dashes or banned vocabulary in prose above `# INTERNAL`.
- Weights and corroboration mechanic are NOT restated in the body - the model lives only in `references/scoring-model.json`.

### Gotchas

- **Fathom Service Weighting is no longer a mandatory dominant scoring layer (v4.0.0 change).** The old skill pulled Fathom onboarding + strategy transcripts and applied them as the dominant scoring modifier. That step is removed. Fathom transcripts are now one optional client-intel input among others, and the practice-area mix is governed by the user's breakdown sentence from the Greeting (or pure scoring when no breakdown is given). Do not reintroduce a Fathom MCP probe or a mandatory transcript pull.
- **Keyword-research fallback path (no entity map).** When `entity-map.json` is missing at the target scope, do not block. Derive topic structure from keyword research (SERP themes, PAA clusters, related searches) and let the four Authority signals default to 0.0 - `score-topics.py` handles sparse signals and the model's optional-signal redistribution keeps the active weights summing to 1.00. Flag `input_source: "keyword_research"` and `upstream: "missing"` in metadata.
- **Manual mode (no entity map AND no keyword research).** Rare - usually a brand-new vertical with zero prior research. Rank qualitatively by the user's stated breakdown + domain knowledge, flag `input_source: "manual"`, produce a research queue instead of a full ranked table, and recommend running entity research to upgrade the plan. Manual mode exists so the skill never blocks; it does not replace real research.
- **Search volume for long-tail podcast topics runs low in absolute terms.** `score-topics.py` normalizes `search_volume` within the topic set, not against absolute MSV benchmarks. A 200 MSV topic can still rank #1 if everything else in the set is 50-100.
- **Content-gap data may be missing for a practice area.** When the content-gap report has no source, `gap_opportunity` defaults to 0.5 (neutral) and `serp_features` defaults to 0.0 for all topics; both log in metadata - not a blocker.
- **Tune weights in `scoring-model.json`, never in code.** `score-topics.py` loads the model at runtime. Editing weights in the script silently desyncs the canonical model.
- **Mahalanobis is now a diagnostic, not the primary ranking (v4.0.0 change).** `scripts/mahalanobis-score.py` is demoted - it runs only when `score-topics.py` is invoked with `--mahalanobis`, as an optional covariance-corrected cross-check. The primary ranking is always the 11-signal weighted `authority_score`.
- **Dedup against existing episodes is mandatory, not optional.** Never produce an episode that already has a Run of Show. Confirm already-covered practice areas with the user (and the local deliverables tree); if an existing ROS covers a practice area partially, only output the uncovered subtopics.
- **Do not pitch practice areas the firm refers out.** Pulled from any user-supplied firm intel or Fathom anti-pattern signal. If the firm explicitly refers a vertical out, do not propose episodes for it even if entity coverage is strong.

### Iteration log

The skill's institutional memory - an append-only record of bugs, papercuts, drift, and fixes spotted across runs.

- **File:** `references/iteration-log.json`.
- **Read-at-start contract:** `## Checks -> ### Orient` reads the log, filters to `status: open` and `status: in-progress` entries, and surfaces them to the agent as known issues to watch for. One file read; institutional memory gates every run.
- **Write semantics:** never written at runtime. New entries are appended manually post-run (ID format `YYYY-MM-DD-NNN`, append-only), or proposed by the skill creator's fold-back loop with `status: proposed` awaiting human sign-off.
- **Runtime behavior:** the skill never writes to the log at runtime; it only reads it at run-start. New entries are appended post-run by a human or the skill creator's fold-back loop.

---

## Standard Operating Procedure

Divider only - the phase H2s below are siblings, not children of this heading.

```
[Checks] -> [Prepare Inputs] -> [Create] -> [Quality Assurance] -> [Ship]
              (Ingest)           Score -> Compile -> Form plan -> Render
```

## Checks

What is?
The pre-flight phase - read the iteration log, verify the scoring script, resolve the client and practice area(s), run the dedup check against existing episodes, and verify the upstream research exists before any scoring or writing happens.

### Orient

What is?
The orientation step - read the iteration log and confirm the scoring engine is in place before any other work.

- **Read the iteration log.** Read `references/iteration-log.json`, filter to `status: open` and `status: in-progress`, surface those entries to the agent as known issues for this run.
- **Verify the scoring script.** Confirm `scripts/score-topics.py` is present and can load `references/scoring-model.json`. If absent, hard-fail with a clear message - the scoring engine is not optional.

### Resolve client, domain, and practice areas

What is?
The orientation step - lock in the client, the legal domain, and which practice areas this run plans for; load the matching seed topics; and resolve the live Drive client folder before any check or write.

- Resolve the client name from the greeting or a `--client` flag.
- **Resolve the legal domain and the active practice areas.** Identify the firm's legal domain (Personal Injury, Family Law, Criminal Defense). Confirm which practice areas the firm ACTUALLY covers - scrape the firm website (the practice-area pages are the ground truth for what this specific firm does). The firm site decides which of the domain's practice areas are in scope; do not assume the firm does every practice area in its domain.
- **Load the seed topics.** For each confirmed practice area, read its `seed_topics` from `references/topic-seed-catalog.json`. These are ONLY the STARTING POINT of the candidate set - not a guaranteed shortlist. They guarantee every evergreen topic is *considered* every run; they earn no scoring or selection advantage. Research-derived topics merge in on top at `## Prepare Inputs`, and `score-topics.py` scores the whole set together - a seed topic the data does not support scores low and lands RESERVE or CUT like any other weak candidate. If a confirmed practice area is a stub (no `seed_topics`) in the catalog, flag it - the catalog should be populated for that practice area before relying on the run, and the run proceeds research-only for that area.
- Resolve the live Drive client folder by searching `.Client Folders/` for `name contains '{client name}'`. If the parent client folder is missing, stop and route the user to `pm-new-client-setup`. If the Map 5 `AEO/Podcast/Topic Plan/` subfolder is missing, create it.
- For multi-vertical clients, sequence one plan per practice area by research priority - explicit client priority, case-value potential, competitive gap, content-volume potential. Do not cram multiple verticals into one ranked table; each vertical gets its own 12 + additional structure.

### Dedup against existing episodes

What is?
The mandatory check that prevents the skill from planning an episode the client already has a Run of Show for - confirm which practice areas are already covered and mark each New / Partial / Covered.

- Ask the user which episodes / practice areas already have a Run of Show, and check the local deliverables tree (`deliverables/podcast-research/{client-slug}/`, `deliverables/podcast-topics/{client-slug}/`) for prior entity maps, topic plans, and n-gram tables.
- Mark each practice area: **New** (full research needed), **Partial** (some episodes exist - output only the uncovered subtopics), **Covered** (ROS already exists - skip unless a refresh is explicitly requested).
- Dedup rule: never produce a topic that already has a Run of Show. This is not optional.

### Verify upstream research

What is?
The existence check that confirms the research the scoring corpus needs is actually reachable, and decides which research path this run takes.

- Look for `entity-map.json` at the target scope (local mirror first, then Drive). Look for `keyword-research.json`. Look for the optional content-gap report and `virality-research.json`.
- Decide the path: entity map present -> entity path. No entity map but keyword research present -> keyword-research fallback path (flag `input_source: "keyword_research"`). Neither present -> manual mode (flag `input_source: "manual"`).
- Show the state-check block and wait for confirmation before any write:

```
pod-2A-topic-planner - state check
  Client:                {client}                        [resolved / needs clarification]
  Practice area(s):      {area(s)}                        [resolved / needs clarification]
  Targeting strategy:    {single-location | multi-location}
  Optimization scope (show anchor): {City | State | County | Regional}
  Episode geo targets:   {single-location: one anchor city, every episode | multi-location: per-episode target cities across the footprint}
  Practice-area breakdown: {user sentence | "no breakdown - pure scoring"}
  Research path:         {entity | keyword-research-fallback | manual}
  Upstream research found:
    - entity-map.json:         {found at {path} | MISSING}
    - keyword-research.json:   {found at {path} | MISSING}
    - content-gap report:      {found | MISSING - OK, gap_opportunity defaults to 0.5}
    - virality-research.json:  {found | MISSING - OK, weight redistributes}
  Dedup check:           {practice areas marked New / Partial / Covered}
  Target folder:         {resolved absolute path}         [exists / will create]
  Existing artifacts:    {list any prior topic-plan-v{n} at target}
  Proceed? (yes / cancel / refresh-in-place / archive-and-rebuild)
```

Do not write files past this block without confirmation. `refresh-in-place` writes a new version; `archive-and-rebuild` moves existing artifacts to `_archive-{YYYY-MM-DD}/` first. If a prior `v{n}` exists, the default target is `v{n+1}` and never overwrites a prior version.

## Prepare Inputs

What is?
The Ingest step - pull every research artifact and client-intel signal reachable for this run into one scoring corpus, normalized into the per-topic shape `score-topics.py` consumes.

**Ingest comprehensively.** Ingest BOTH Topic-Only and Topic+Location research, and ALL location scopes relevant to the client's market - not just one location. Surface every practice area that has research; never silently narrow scope to one area or one scope.

Work through the input sources in priority order; on a tool error, skip that source silently and log it to `metadata.sources_unavailable[]`.

1. **Entity map.** Load `entity-map.json` (and `entity-clusters.md` when present). Extract per-entity prominence, relatedness, popularity, the cluster + bridge structure, and total entity / cluster counts. On the keyword-research fallback path, skip this and let the four Authority signals default to 0.0.
2. **Keyword research.** Load `keyword-research.json`. Extract per-topic MSV, PAA stacks (including whether the topic's core query itself surfaces as a PAA question), and related-search breadth. Present on both research paths.
3. **Content-gap.** Load the cached content-gap report, or run the content-gap MCP live (`mcp__content-gap__get-serp`, `query-fanout`). Extract competitor coverage per topic for `gap_opportunity` and `popularity`, AND capture the SERP feature flags per query for `serp_features` - whether the topic's core query triggers an AI Overview, a video pack, a featured snippet, or an image pack. When the content-gap report is unavailable, default `gap_opportunity` to 0.5 AND `serp_features` to 0.0 for all topics, and log both in metadata.
4. **Virality (optional).** Load `virality-research.json` if present. Extract the per-topic trend / momentum signal. When absent, log `virality: "absent"` - the model redistributes its weight.
5. **Client intel.** Pull any optional `podcast-overview.md` (audience, content philosophy, episode-length target, show goals) and any user-supplied Fathom transcripts or firm intel (practice focus, refers-out, firm type) as client-intel inputs. Use this to sense-check the topic mix and to catch anti-patterns (verticals the firm refers out). This is a priority-order modifier, NOT a dominant scoring layer.
6. **Koray RAG (methodology grounding).** When `mcp__ce-services__rag_query` is reachable, query `rag_name: "koray"`, `top_k: 6`, discard results scoring below 0.40, for contextual-layers / topical-authority / cluster-prioritization grounding. If unreachable, log `koray_rag: "unreachable"` and proceed on the in-skill methodology.
7. **Assemble the corpus.** The candidate list STARTS from the seed topics loaded in `### Resolve client, domain, and practice areas` (each confirmed practice area's `seed_topics` from `references/topic-seed-catalog.json`) - a starting point only, carried in with no scoring advantage. Then merge the research-derived topics on top: everything the entity / keyword / virality research surfaced that the seed did not already hold (location-specific topics, newly-trending topics). De-duplicate against the seed by concept. Seed and research-derived topics are indistinguishable to `score-topics.py` - all compete on signal evidence alone. The result is one list of candidate topics, each carrying the raw values for all 11 signals - including a `serp_features` value per topic (the SERP feature flags from step 3). Signals with no source carry their `absent_when` default from `scoring-model.json`. Pull in any operator-supplied manual / editorial candidate topics here - forward-looking or trend topics with no search data yet; they join the candidate set, score on whatever signals exist, and are marked editorial in the `Notes` column at scoring time. Do NOT pre-filter the set on perceived episode strength - drop only genuine non-topics (entertainment / gore video searches, navigational queries, pure brand head terms); every research-supported topic becomes a scored candidate and the score decides if it is weak. This corpus is the single input to `score-topics.py`. Log every source that fired in `metadata.sources_used[]`.

## Create

What is?
The build phase - score every candidate topic on the 11-signal model, compile scored topics into episode-sized coherent groups, form the 12 + additional + reserve plan, build the per-episode n-gram tables, and render the four artifacts.

**Best Practices.**
These apply to the entire Create phase and should be checked after each step.

- Episodes are an OUTPUT of compilation, never an upfront guess (see `### Quality bar`).
- The scoring model lives in `references/scoring-model.json` - never restate its weights or numbers in the rendered output or this skill.
- Honor the practice-area breakdown when the user gave one; default to pure scoring when they did not.
- The original `authority_score` ranking must stay recoverable - it ships in the INTERNAL `## Topic Ideas` table unmodified.

If the model produces an episode whose rank cannot be traced to the score plus the compilation decision, emit a `> NEEDS VERIFICATION:` block at that episode instead of shipping it.

### Score topics

What is?
The scoring-engine pass - run `score-topics.py` over the ingested corpus to compute the 11-signal weighted `authority_score`, the corroboration flag, and the original ranking for every candidate topic.

The scoring methodology, in prose. The full model - every signal, its definition, its source, its weight, and the corroboration mechanic - is canonical in [`references/scoring-model.json`](references/scoring-model.json). `score-topics.py` loads that file at runtime. This skill explains the model; it does not restate the numbers.

- **Eleven atomic signals in three buckets.** Authority asks "does this episode build the practice area's topical map?" Demand & Trend asks "are people searching for - or trending toward - this topic?" Competitive asks "is the lane winnable?" The buckets carry fixed weights (Authority, Demand & Trend, Competitive) defined in `scoring-model.json`; the eleven signals sum within them to a weighted `authority_score` per topic. The Demand bucket carries the most weight - real search behavior is the strongest predictor of a topic worth recording.
- **Optional-signal redistribution.** When an optional signal (virality) has no source, its weight redistributes proportionally across the present signals so the active weights still sum to 1.00. A missing optional signal never deflates a topic's rank.
- **The corroboration mechanic.** A weighted sum can be carried by one big signal. Corroboration rewards breadth of evidence instead. When a topic clears the evidence bar on multiple INDEPENDENT signal families at once - entity, search-demand, and trend - that convergence is a stronger signal than any single high score. A topic confirmed by the entity map AND search demand gets a high-confidence flag (`corroborated`, or `corroborated+trending` when the trend family also fires) and a ranking floor: a corroborated topic is protected into the main 12 and cannot be displaced by a single-family topic ranked above it on raw score alone. The flag does not change the numeric score - it drives the Rationale text and the floor. The exact family-firing thresholds and floor toggle live in `scoring-model.json`.

Run the engine:

```bash
python3 scripts/score-topics.py {corpus_dir}
```

`score-topics.py` reads the ingested corpus, loads `references/scoring-model.json`, computes the weighted `authority_score` + corroboration flag for every topic, and emits the **Topic Ideas** table - every candidate in unmodified `authority_score` order, columns `Rank | Topic | Theme | Score | Rationale | Notes`. The `Score` column renders the topic's `authority_score` to three decimals (e.g., `0.653`). It also emits a draft Rationale per topic from the signal scores + corroboration flag, per the `rationale` rules in the model file - the AI-written `Rationale` column explains in plain language why the topic earned its score and rank by naming the signals behind it (comma-listed signals, then ` -- `, then a verdict - e.g., `5 PAA, related searches, has AI overview -- great demand for topic`; `high search volume, right intent`). The `Notes` column is a freeform INTERNAL field that records each topic's disposition once episode selection runs (`MAIN-#`, `BONUS`, `RESERVE`, `CUT (reason)`) plus any operator or review comment, and carries the `editorial` mark for any operator-supplied manual candidate; it is empty on a fresh scoring run and populated at episode selection (`### Form the episode plan`).

- **Optional Mahalanobis diagnostic.** Pass `--mahalanobis` to additionally run `scripts/mahalanobis-score.py` as a covariance-corrected cross-check. This is a diagnostic only - it never replaces the weighted `authority_score` as the primary ranking. Use it when an AM wants to sanity-check whether correlated signals are double-counting.

### Compile into episodes

What is?
The genuine-judgment step - cluster the scored topics into episode-sized coherent groups so each group is a recordable 60-90 minute episode; the episode boundary emerges here, it is not assumed.

This is where the skill exercises real judgment. Scoring ranked atomic topics; compilation decides where one episode ends and the next begins.

**Episode-selection pass.** `### Compile into episodes` and `### Form the episode plan` together are the episode-selection pass. Run them from the prompt at [`references/prompts/select-episodes-prompt.md`](references/prompts/select-episodes-prompt.md) - it is triggered after the `## Topic Ideas` table is populated and reviewed, reads the practice-area split from the `Topic Mix` field of `## Show Identity`, and writes each candidate's disposition into the `Notes` column.

- **Group by coherence, not by score adjacency.** Pull together topics that a host could cover in one coherent 60-90 minute conversation - a shared liability theory, a shared stage of a case, a shared audience question. A high-scoring topic and a low-scoring topic can belong in the same episode if they are the same conversation.
- **Size each group to one episode.** Too thin (one narrow subtopic) and it is not an episode - merge it up or send it to the reserve catalog. Too broad (three distinct conversations) and it is three episodes - split it.
- **Bundle duplicates.** When two candidate groups cover the same primary concept (entity overlap > 50% OR primary-keyword overlap > 40%), merge them into one episode with a wider angle. Do not ship both. Examples: "how to file a car accident claim" + "what to do after a car wreck" are one first-steps episode; "underinsured motorist coverage" + "uninsured motorist coverage" are one "the other driver's insurance failed you" episode.
- **Carry the group score forward.** Each compiled episode inherits an `authority_score` (the aggregate of its topics' scores) and the strongest corroboration flag among its topics. The ranking floor applies at the episode level - a corroborated episode is protected into the main 12.
- **Classify intent stage.** Tag each episode `awareness`, `consideration`, or `decision` so the plan covers the full buyer funnel.

### Form the episode plan

What is?
The selection pass - rank the compiled episodes, apply the practice-area breakdown from the `Topic Mix` field, and split them into 12 main + exactly 3 additional (one per category) + the INTERNAL reserve catalog (carried in the `Notes` column).

- **Rank the compiled episodes** by aggregate `authority_score`, with the corroboration ranking floor applied (corroborated episodes cannot be displaced by single-family episodes ranked above them on raw score).
- **Assign each episode its Episode geo target.** This is where the per-episode geo target is set (see `### Geo model`). The show already carries one **Optimization scope (show anchor)**; the **Targeting strategy** flag decides how the 12 episodes inherit geography:
  - **single-location** - every episode's geo target is the one anchor city. All 12 share it; there is no per-episode city variation. Episodes are Full episodes.
  - **multi-location** - the show anchors broad (State / Regional) and each episode is a **Mini episode** built to rank for a different city in the footprint. Carry a per-episode target city on the 12-episode plan (one per city we're trying to rank for) and let that city's questions and title emphasize it naturally - a ceiling, never a forced quota (never force-feed the city; see the no-city-quota principle in `### Geo model`).
  - EP1 (Founder Story) and EP2 (flagship ebook anchor) keep their fixed rules below; their geo target is the show's home / anchor city, since the founder story and the flagship guide anchor the whole show rather than one satellite market.
  Record each episode's geo target on the JSON row (`geo_target`) so `pod-2B-n-gram-table` and the Run of Show pipeline build every episode at its confirmed scope.
- **Apply the practice-area breakdown.** Precedence: (1) a client-stated breakdown always wins - it governs how many of the 12 main slots each practice area gets, fill each area's quota with its top-ranked compiled episodes; (2) with no client breakdown, a **Personal Injury** firm falls to the **Default practice-area mix** below; (3) a non-PI firm (Family Law, Criminal Defense, etc.) with no breakdown takes the top 12 by rank with no practice-area quota (pure scoring). In every case scoring decides *which* episodes fill each area's slots - the mix sets the quota, the score fills it.
- **Default practice-area mix (Personal Injury, no client breakdown).** The CE house-standard PI distribution across the 12 main slots. Scoring picks the specific episode for each slot; this fixes how many slots each area gets and which slot numbers they occupy:
  - Car Accidents - 3 eps (3, 4, 6) -> 25%
  - Medical Malpractice - 2 eps (5, 9) -> 17%
  - Truck Accidents - 2 eps (7, 12) -> 17%
  - Cross-Service Roundup - 1 ep (2) -> 8%
  - Wrongful Death - 1 ep (8) -> 8%
  - Founder Story - 1 ep (1) -> 8%
  - Slip & Fall - 1 ep (11) -> 8%
  - Bicycle / Pedestrian - 1 ep (10) -> 8%

  Slot 1 stays `The Founder Interview` (Founder Story), slot 2 is the **Cross-Service Roundup**, and slot 3 is the **flagship ebook anchor** - the top-ranked Car Accidents comprehensive guide, which satisfies both the ebook-anchor rule and a Car Accidents quota slot (see the EP2 and EP3 rules below). If the firm does not actually practice one of these areas (confirmed at the Checks website scrape), drop that area and reallocate its slot(s) to the next-ranked Car Accidents episode, then to the highest-scoring remaining compiled episode in any confirmed area. The Cross-Service Roundup is never dropped - it spans whatever services the firm confirms. Never invent an episode for a practice area the firm doesn't cover.
- **EP1 is always `The Founder Interview`.** The biographic anchor episode occupies slot #1 of the main 12 - CE house standard, every client. Its `Topic` cell reads exactly `The Founder Interview`; its `Theme` cell is exactly `Founder Story` (fixed - no `Brand / ` prefix, no client variation); its Rationale describes the firm-specific angle (decades of practice, market positioning, defining moat) but the title and theme stay the standard.
- **EP2 is always the Cross-Service Roundup (Default PI mix).** Slot #2 is the **Cross-Service Roundup**: the top AI-cited question per confirmed practice area, grouped by service, so the episode spans the firm's whole book of business and cross-sells every other episode. Its questions come from a grouped-by-service n-gram table - the top-demand question in each service block. It is NOT the ebook anchor (that is EP3) and it is never dropped; it stretches to cover whatever services the firm confirms. When a client breakdown governs the mix instead of the Default, the roundup is optional - keep it only if the breakdown leaves room, otherwise slot #2 follows the client's heaviest area.
- **EP3 is always the flagship ebook anchor.** Slot #3 goes to the single best episode to spin into a flagship ebook / lead magnet that ALSO carries real search demand. It must clear BOTH bars: (a) ebook-worthy - broad, evergreen, comprehensive enough to anchor a full guide and cross-sell the other episodes (the canonical "complete guide to {core practice area}" topic), and (b) demand-backed - meaningful MSV in the keyword research, not a low-volume topic. On the Default PI mix this is the top-ranked Car Accidents comprehensive guide, satisfying both the ebook-anchor rule and a Car Accidents quota slot. A high-scoring but narrow or low-demand wow-factor topic (e.g. a firm's own marquee case) does NOT take slot #3 just because it ranks high - it lands elsewhere in 4-12; slot #3 is reserved for the best ebook + demand topic so the show's third episode doubles as the firm's lead-magnet ebook. When two topics both qualify, prefer the broader comprehensive guide over the higher-MSV narrow topic, and note the runner-up in the INTERNAL Selection Methodology Detail. Episodes 4-12 are the remaining top-ranked thematic episodes (a practice-area breakdown, when given, still governs the overall mix across all 12).
- **Additional Topics:** exactly 3 swap-in candidates, one per category. For a PI firm on the Default mix the three categories are the multi-slot areas: one Car Accidents alternate, one Medical Malpractice alternate, and one Truck Accidents alternate - the next-ranked compiled episode in each. If the firm doesn't practice one of those, substitute the next category by quota weight (Wrongful Death, then Slip & Fall, then Bicycle / Pedestrian). When a client breakdown governs the mix instead, the three categories follow that breakdown's heaviest areas. The swap relationship is no longer a client-facing column; if an operator wants to record which main episode a candidate could replace, that note lives in the INTERNAL `## Topic Ideas` `Notes` column, not in the Additional Topics table.
- **Disposition tagging:** every candidate topic gets a disposition written into the `Notes` column of the INTERNAL `## Topic Ideas` table - `MAIN-#` (landed in the curated 12), `BONUS` (additional / swap-in pool), `RESERVE` (future-season / standalone), `CUT (reason)` (killed, with reason). There is no separate Topics by Theme catalog: the `## Topic Ideas` table already groups by theme (its `Theme` column) and now carries disposition (its `Notes` column), so one table does both jobs - the reserve catalog and the original ranking. Manual / editorial candidates also keep their `editorial` mark in `Notes` alongside the disposition.
- **Write the Rationale per episode.** Tighten `score-topics.py`'s draft rationale to one sentence, hard cap 200 characters, naming the real top-contributing signals and leading with the corroboration flag when present (see `### Editorial Guidelines -> Guideline 2`).
- **Reuse existing per-subtopic research.** Before finalizing an episode title, scan `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/` for canonical per-subtopic research from prior client runs. If a subtopic already has full research at the right scope, match the episode title to the subtopic folder name (proper case) so `pod-2B-n-gram-table` and downstream skills find the existing artifacts without duplication.

### Build the n-gram tables

What is?
The mandatory step that builds a per-episode n-gram table for every locked episode - no longer an optional yes/no handoff. The episode plan is scored and compiled at this point; the n-gram tables must exist before the per-episode `## Episode Breakdown` roll-up (`### Render the topic plan`) can be written.

- **Auto-invoke `pod-2B-n-gram-table` for every locked episode EXCEPT Episode 1.** This runs for main episodes 2-12 AND every additional topic - no prompt, no opt-out. Pass each episode's entry from the formed plan (title, theme, scope, keywords, entity IDs) so `pod-2B-n-gram-table` builds the table at the right scope.
- **Episode 1 is the standing exception - never n-gram-built.** `The Founder Interview` is the biographic founder interview; it asks the same canonical question set for every client, every run. The n-gram build step SKIPS Episode 1 entirely - no `pod-2B-n-gram-table` call is made for it. Its Episode Breakdown roll-up is populated from the canonical Founder Story interview question set at [`references/e1-founder-interview-questions.md`](references/e1-founder-interview-questions.md) - 21 questions across five segments (S1-S5) plus an outro, with `{{LOCATION}}` / `{{BUSINESS}}` / `{{NICHE}}` tokens filled per client at render time. Read that file and fill the tokens; do not invent or score E1 questions.
- **Reuse existing tables.** If an episode (2-12 or additional) already has a current-scope n-gram table from a prior run (per the dedup scan in `## Checks`), reuse it instead of regenerating - do not duplicate.
- **Capture the outputs.** Each `pod-2B-n-gram-table` run produces a per-episode question set. The skill holds these in memory; `### Render the topic plan` rolls them up into the client-facing per-episode `## Episode Breakdown` tables, and `## Ship` records the n-gram tables in the INTERNAL `## Research Sources` table.
- **Feed surfaced topics back into `## Topic Ideas`, and score them.** Building an episode's n-gram table can surface a NEW candidate topic the scored set does not already hold - a distinct sub-topic or question cluster strong enough to stand as its own episode. When that happens: define it as a candidate topic (entity IDs + match terms), add it to the corpus, and re-run `score-topics.py` over the full set so the surfaced topic is scored in context with everything else - it does not wait for a future run. It lands as a new row in the INTERNAL `## Topic Ideas` table with its real `Rank` and `Score`, and `Notes` = `surfaced from n-gram table ({source episode})`. This keeps `## Topic Ideas` the complete, fully-scored candidate record even as the n-gram step uncovers more. **Fold it back into the seed catalog - but only when it is evergreen.** If the surfaced topic is generic and evergreen (it would matter to ANY firm in that practice area, not just this client - e.g. Distracted Driving), genericize it (strip the client / city / jurisdiction specifics) and add it to that practice area's `seed_topics` in `references/topic-seed-catalog.json`, so the catalog compounds and the next client starts richer. If it is location-specific or a passing trend (e.g. a Gulf-Coast-only hurricane-evacuation angle), leave it in this run's `## Topic Ideas` only - do NOT add it to the generic seed. The same evergreen-only test applies to topics the research pass surfaces, not just the n-gram step.
- **On a per-episode failure,** flag that episode with a `> NEEDS VERIFICATION:` note in the roll-up rather than blocking the whole plan; the topic plan still ships.
- **Drive push.** Every n-gram table lands at its canonical Drive location with the full output set `pod-2B-n-gram-table` defines (markdown + JSON + Google Doc). Confirm each episode's artifacts pushed before the question-table step runs.

### Build the Episode Question Tables

What is?
The final build step - turn the per-episode n-gram tables into the client-facing `## Episode Breakdown` question tables, then run a cross-episode de-duplication pass. Runs from the prompt at [`references/prompts/episode-question-tables-prompt.md`](references/prompts/episode-question-tables-prompt.md), triggered automatically once every locked episode has an n-gram table.

- **Roll up per episode.** For episodes 2-12 and every additional topic, populate the episode's `## Episode Breakdown` table from its n-gram table - columns `Question` / `Keywords` / `Rationale`. The `Keywords` cell is the n-gram phrases for that question with each phrase resolved to its MSV from keyword research and formatted by `keywords_cell()` (`{summed MSV}/mo Total Search Demand`, then the `phrase - X/mo` list, highest first) - NOT the raw phrase list. The `Rationale` is a short plain-language summary of the research signal behind the question (see Editorial Guideline 2). Episode 1 is the standing exception - its table is the canonical Founder Story set from `references/e1-founder-interview-questions.md`, never n-gram-derived.
- **Cross-episode de-duplication.** After every per-episode table is built, scan all questions across all episodes together. No question (or host-experienced near-duplicate) may appear in two episodes. Keep each shared question in its best-fit episode, drop it from the other, backfill the dropped slot from that episode's own n-gram table, and re-scan until every question across the whole plan is unique. This pass looks at the plan as a whole and may run as its own step/script after all per-episode tables are populated.

### Render the topic plan

What is?
The rendering pass - write the four artifacts from the formed plan: the canonical markdown (client-facing sections + the full INTERNAL block), the schema-validated JSON, the `.docx`, and the branded Drive Doc.

#### Client-facing structure (above the `# INTERNAL` cut)

Render these sections in this exact order:

1. **`# Podcast Topic Plan`** H1 (Doc title).
2. **Cover frontmatter** - firm name, location / anchor, prepared-by, date. Rendered as centered cover-page text by the formatter, NOT a body H2.
3. **`## Show Identity`** - exactly five client-approval fields, rendered as bold inline labels (NOT H3 headings), in locked order: `**Podcast Name:**`, `**Tagline:**`, `**Podcast Description:**`, `**Audience:**` (followed by a 1-5 bullet list), `**Topic Mix:**`. The skill does not generate a show-name shortlist - the user / AM supplies the name. **Topic Mix** is the practice-area episode split as percentages, with the episode count for each area in parentheses. Each entry renders as `{Practice Area} {percentage}% ({N} episodes)` - e.g. `Car Accidents 25% (3 episodes)` - comma-separated on one line, percentages first to last; pluralize the count (`(1 episode)` singular, `(2 episodes)`+ plural). Its source depends on the practice-area breakdown captured in the Greeting:
   - **Client specified a breakdown at intake** - render the percentages verbatim from the client's stated mix. Render NO footnote; the percentages simply are the client's stated preference and need no explanation.
   - **No breakdown given, PI firm (default mix)** - render the Default practice-area mix percentages from `### Form the episode plan` (Car Accidents 25% (3 episodes), Medical Malpractice 17% (2 episodes), Truck Accidents 17% (2 episodes), Cross-Service Roundup 8% (1 episode), Wrongful Death 8% (1 episode), Founder Story 8% (1 episode), Slip & Fall 8% (1 episode), Bicycle / Pedestrian 8% (1 episode)), adjusted for any area the firm doesn't practice (reallocated slots change the affected counts; the Cross-Service Roundup is never dropped). Render NO footnote - this is the CE house-standard PI distribution.
   - **No breakdown given, non-PI firm (pure scoring)** - derive the percentages from the scoring output (the episode distribution across practice areas in the formed plan) and render exactly this italic footnote immediately under the field: *"The percentages reflect where search demand, entity coverage, and competitive opportunity actually concentrated across the practice areas. It is what is showing up as important in the wild."*
   - Never print "no client topic breakdown was specified" or any variant - that explanatory clause is removed from both branches. The footnote either is the scoring-derived sentence above (no-breakdown case) or it is absent (client-breakdown case).
4. **`## Methodology: How topics are selected`** - 1-2 paragraphs of vague-but-smart prose, enough to telegraph that real research happened without exposing the scoring machinery. Anti-AI pass mandatory (Editorial Guideline 1). No bullets, no numbered steps.
5. **`## The 12-Episode Plan`** - the main table. Columns in exact order: `#`, `Topic`, `Theme`, `Keywords`, `Rationale`. Widths `[32, 134, 70, 116, 116]` PT. There is NO standalone `Search Volume` column - the summed MSV lives inside the `Keywords` cell (see step 7). Row 1 is `The Founder Interview`; its `Keywords` cell uses the same `keywords_cell()` format with the label `Total Branded Search Demand` - line 1 `{summed MSV}/mo Total Branded Search Demand` (sum of the branded MSVs, unranked queries counted at 50/mo), a line break, then the branded-search benchmark queries comma-separated (`{query} - {MSV}/mo, ...`).
6. **`## Additional Topics`** - the additional table. Columns in exact order: `Topic`, `Theme`, `Keywords`, `Rationale`. Widths `[150, 80, 128, 110]` PT. No standalone `Search Volume` column (same merged `Keywords` cell rule as the main table) and no `Swaps for` column - swap relationships, when an operator wants to record them, live in the INTERNAL `## Topic Ideas` `Notes` column.
7. **`## Episode Breakdown`** - the per-episode question roll-up. No section intro paragraph - the H2 is followed directly by the first episode heading. One compact table PER episode (the main 12 AND the additional topics). Episodes 2-12 and the additional topics are headed `Episode N: {episode title}`; **Episode 1's heading is `Episode 1: Founder Story`** (the theme, not the EP1 title - E1 is the standing exception throughout). For episodes 2-12 and the additional topics, the table columns are in exact order `Question`, `Keywords`, `Rationale`; questions are pulled from that episode's `pod-2B-n-gram-table` output (the `### Build the n-gram tables` step). The `Keywords` cell is that question's n-gram phrases with each phrase resolved to its MSV from keyword research, formatted by `keywords_cell()` - line 1 `{summed MSV}/mo Total Search Demand`, line 2 the `phrase - X/mo` list highest first. It is NEVER the raw comma-joined n-gram phrase list; a question table that ships raw phrases with no `/mo` volume is a contract violation (`qa-doc-format.sh` check 6 fails it). The `Rationale` cell is a short plain-language summary of the research signal behind the question - "comes up heavily in People Also Ask", "triggers an AI Overview", "strong related-search cluster" - a summary of the cited research, NOT a direct citation. **Episode 1 is the standing exception:** `The Founder Interview` is never n-gram-built, so its questions are NOT scored or n-gram-derived - they come from the canonical Founder Story interview question set at [`references/e1-founder-interview-questions.md`](references/e1-founder-interview-questions.md). E1 renders as ONE table with two columns, `Question` / `Rationale` - the 21 founder-interview questions top to bottom, UNNUMBERED. E1's `Rationale` is NOT a research signal (E1 is never n-gram-built) - it is a few hard-coded words naming what the question accomplishes in the interview (e.g., establish credibility, position as expert, build local trust, emotional close), one per question in `references/e1-founder-interview-questions.md`. E1's table has no Keywords column and no Segment column. Read the file, fill the `{{LOCATION}}` / `{{BUSINESS}}` / `{{NICHE}}` tokens with the client's values, and render the 21 questions with their rationales. The questions are identical for every client; never invent or substitute E1 questions. Keep the tables intentionally compact: two episodes per page is a density target, not a hard rule. The compact table settings carry it - body 9pt, header 10pt, cell padding 2pt vertical / 6pt horizontal (the locked density values used across this skill's tables). Final pagination varies with each episode's question count: an episode with many questions can run a page on its own. Purpose: the client QAs the topic list AND the actual questions in one deliverable, before recording. This section is client-facing - it stays above the `# INTERNAL` cut.
8. **`# INTERNAL`** - the H1 cut. Everything below is operator-facing.

Keywords cells are two-part and built by `scripts/lib_doc_table.py` -> `keywords_cell()` so the format is identical every run: line 1 `{summed MSV}/mo Total Search Demand`, a line break, then the comma-separated `keyword - X/mo` list (each keyword with its own MSV, highest first). The summed MSV is the total that the dropped standalone `Search Volume` column used to carry; merging it into the `Keywords` cell is the v4 format change (2026-05-20). Table density: body 9pt, header 10pt, cell padding 2pt vertical / 6pt horizontal - the 12-Episode table targets 2 pages of US Letter. The production-wave narrative is INTERNAL-only - it renders under `## Selection Methodology Detail`, never as client-facing text below the 12-Episode Plan table and never as a table column.

#### INTERNAL structure (below the `# INTERNAL` cut)

Everything below `# INTERNAL` is operator-only - never shared with the client. The `# INTERNAL` H1 renders as the most prominent marker in the Doc (28pt CE Blue bold, 1.5pt CE Blue top border) so an AM doing share-prep spots the truncation boundary at a glance. Required subsections, in this order:

1. **`# INTERNAL` H1** + disposition-legend paragraph defining the `Notes`-column values used in the `## Topic Ideas` table (`MAIN-#`, `BONUS`, `RESERVE`, `CUT (reason)`, `editorial`).
2. **`## Research Sources`** - the FIRST H2 under `# INTERNAL`. Operator quick-nav table with a clickable Drive hyperlink to every research artifact that fed the plan. Three columns in exact order: `Name`, `URL`, `Notes`. One row per research artifact actually used - each entity map, keyword-research artifact, virality-research artifact, and n-gram tables folder, named with its practice area and scope (e.g., `Entity Map - Truck Accidents (Houston, TX)`, `Keyword Research - Car Accidents (Houston, TX)`). `URL` carries the Drive link to that artifact; `Notes` carries any pertinent detail (entity counts, coverage caveats, what the artifact contributed). Resolve Drive file/folder IDs at build time and cache them in `metadata.research_sources`.
3. **`## Topic Ideas`** - ALWAYS RENDERED. The complete candidate set, every topic in its original unmodified `authority_score` ranking order as emitted by `score-topics.py`. Six columns in exact order: `Rank | Topic | Theme | Score | Rationale | Notes`. The `Score` column renders the topic's `authority_score` to three decimals (e.g., `0.653`). The `Rationale` column is AI-written - it explains in plain language WHY each topic earned the score and rank it did, by naming the actual signals behind it. Format: comma-listed signals, then ` -- `, then a verdict. Examples: `5 PAA, related searches, has AI overview -- great demand for topic`; `high search volume, right intent`. The `Notes` column is a freeform INTERNAL field that records each topic's disposition once episode selection runs - `MAIN-#`, `BONUS`, `RESERVE`, `CUT (reason)` - plus any operator / review comment and the `editorial` mark for an operator-supplied manual candidate. It is empty on a fresh scoring run and populated at episode selection (`### Form the episode plan`). This single table is both the original-ranking record and the reserve catalog: it groups by theme via the `Theme` column and carries disposition via `Notes`, so a manual reweight ("add more truck accident") still has the original research ranking recoverable. INTERNAL-only - stripped before any client share.
4. **`## Selection Methodology Detail`** - the real methodology the client-facing `## Methodology` section refers to but does not expose: the 11-signal scoring, the corroboration mechanic and ranking floor, the compilation logic, the practice-area breakdown applied, client-intel modifiers. Points at `references/scoring-model.json` as the canonical model. This section also carries the **production-wave narrative** (which episodes record in Wave 1 / 2 / 3): in v4 the wave order is INTERNAL-only operator guidance, rendered here as a short paragraph or `#### Production wave order` sub-section - it is NOT client-facing prose under the 12-Episode Plan table and NOT a table column. If the wave text no longer matches the formed episode set after a re-run, rewrite it to match or drop it; never ship stale wave text.
5. **`## Episode 1 Branded Search Benchmark`** - the pre-launch baseline for `The Founder Interview`. Run `mcp__content-gap__get-serp` on attorney name + variations + brand name + variations (`{first} {last}`, `{first} {middle} {last} attorney`, `{firm short} law firm`, `law offices of {full name}`, `{last} lawyer {city}`, plus any domain head term); capture SERP depth, position-1 ownership, and a directional MSV estimate. This becomes the baseline for measuring branded-search lift at 6 and 12 months, and it populates row 1 of the main table.
6. **`## Provenance`** - research artifacts that fed each version (Drive Doc + local JSON paths), CE artifacts, master catalog backlink, public web sources, open data gaps for the next refresh. Append-only across versions. Do NOT render a "Pipeline position" / upstream-downstream line in the deliverable - that is skill-internal plumbing (it lives in the `### Workflow` section of this SKILL.md, never in the topic plan output).

#### Render the JSON

Write `topic-plan-v{n}.json` from the in-memory episode data. It carries: the `metadata` block (practice areas, episode count, `input_source`, scoring provenance, `sources_used` / `sources_unavailable`); the ranked `episodes` array (each with `rank`, `title`, `theme`, `keywords`, `search_volume_total`, `authority_score`, `corroboration_flag`, `intent_stage`, `primary_cluster`, `bridge_clusters`, `entity_ids`, `episode_angle`, `geo_target` (the confirmed per-episode target city from `### Form the episode plan`), `rationale`, `wave`, and an `episode_questions` array of `{question, search_phrases, rationale}` objects rolled up from that episode's `pod-2B-n-gram-table` output); the `additional_topics` array (same shape, including its `episode_questions`); the `show_identity` object (all five fields); and the top-level `topics_by_score` array (every candidate in original ranking order). The `search_volume_total` value stays in the JSON (downstream consumers still read it); it just renders inside the `Keywords` cell now rather than as a standalone column. Validates against `references/schema/topic-plan-schema.json`.

#### Render the docx

Run `scripts/topic-plan-to-docx.sh` to render `topic-plan-v{n}.docx` from the local `.md` using the baked-in reference template (`references/templates/topic-plan-reference.docx`). The page header is auto-patched to `Case Engine | Podcast Topic Plan | {anchor}`. This reads only the local md and writes only the local docx - it never touches the Drive Doc.

## Quality Assurance

What is?
The gate before `## Ship` - a three-tier check structure that confirms the plan aligns with the Best Practices contract, passes the anti-AI scan, and clears every skill-specific mechanical check before any artifact ships.

**First - check against Best Practices.** The deliverable must align with the contract defined upstream in this file. This is always the first gate.

- **Quality bar** (Best Practices -> Quality bar) - episodes compiled not guessed, every rank traces to the model, rationale names real signals, no duplicate episodes, original ranking recoverable, practice-area breakdown honored, Roboto font lock applied.
- **Sourcing discipline** (Best Practices -> Sourcing discipline) - every value Confirmed, Inferred (flagged `> INFERRED:`), or Unknown (flagged `> NEEDS VERIFICATION:`). No silent synthesis.
- **Editorial Guidelines** (Best Practices -> Editorial Guidelines) - Guideline 1 (client-facing prose anti-AI clean, above `# INTERNAL` only), Guideline 2 (Rationale column names real signals, no filler).
- **Quality gates** (Best Practices -> Quality gates) - the full mechanical checklist must pass.

**Second - Anti-AI Detection two-pass scan** (canonical doc: https://docs.google.com/document/d/1hp7bxOFRlMhCuhjHNY0j05JrB97-KOFD0XUCQM3gMBU/edit). Mandatory for every text-producing skill. Run the full Section 7 two-pass audit against the client-facing prose (Show Identity description + Methodology paragraphs + cover copy). Tables stay factual and untouched; the INTERNAL section is operator-facing and exempt.

- **Pass 1 (mechanical scan):** em-dashes, banned vocabulary (Section 2), banned phrases (Section 3), triadic rhythms and symmetric paragraphs (Section 4), summary-only section closers, date formatting, specific-claims-trace-to-source, no emojis, no clickbait.
- **Pass 2 (skeptical re-read):** restart from the top. Em-dashes missed? Banned phrases rationalized? Triadic rhythms left because they "sounded fine"? Generic Rationale filler that should name a signal? Am I sure?
- **On any hit:** fix and re-run Pass 2 until clean. One pass is not enough.

**Third - skill-specific mechanical checks.**

- **Four-artifact presence:** `topic-plan-v{n}.md`, `.json`, `.docx` exist at the local path; the Drive Doc was formatted by `topic-plan-formatting.sh` since the last `.md` change. A partial set is a contract violation.
- **JSON validates** against `references/schema/topic-plan-schema.json` - required fields present, types correct, enums valid, `show_identity` has all five fields, main table 5 cols at `[32,134,70,116,116]`, additional table 5 cols at `[134,70,116,100,48]`, every episode row carries a `rationale` <= 200 chars.
- **`.docx` regenerated from the current `.md`** (docx mtime >= md mtime).
- **Client-facing structure** renders in canonical order (`# Title` -> cover -> `## Show Identity` -> `## Methodology` -> `## The 12-Episode Plan` -> `## Additional Topics` -> `## Episode Breakdown` -> `# INTERNAL`).
- **`## Episode Breakdown` roll-up present above `# INTERNAL`** - no section intro paragraph, one entry per episode (main 12 AND additional). Episodes 2-12 + additional topics are headed `Episode N: {title}` and have a `Question` / `Keywords` / `Rationale` table sourced from that episode's `pod-2B-n-gram-table` output; the `Keywords` cell carries MSV-joined volume in the `keywords_cell()` format, never raw n-gram phrases. Episode 1 is headed `Episode 1: Founder Story` (theme, not title) and renders the canonical Founder Story interview question set as ONE two-column `Question` / `Rationale` table - 21 questions top to bottom, unnumbered, no Keywords or Segment column - never an n-gram table. E1's `Rationale` is the hard-coded interview-purpose note from `references/e1-founder-interview-questions.md`, not a research signal. A `> NEEDS VERIFICATION:` note is acceptable only where an n-gram run failed (does not apply to E1).
- **N-gram tables built for every locked episode except E1** - `pod-2B-n-gram-table` ran (or an existing current-scope table was reused) for main episodes 2-12 AND every additional topic before the roll-up was rendered. Episode 1 is never n-gram-built.
- **`## Topic Ideas` table is present under `# INTERNAL`** with every candidate topic in original unmodified `authority_score` order. Six columns in exact order: `Rank | Topic | Theme | Score | Rationale | Notes`. The `Score` column renders the topic's `authority_score` to three decimals (e.g., `0.653`). The `Rationale` column is AI-written and names the signals behind the score (comma-listed signals, then ` -- `, then a verdict - e.g., `5 PAA, related searches, has AI overview -- great demand for topic`). The `Notes` column carries each topic's disposition after episode selection (`MAIN-#`, `BONUS`, `RESERVE`, `CUT (reason)`, `editorial`); it is empty only on a fresh pre-selection scoring run. This table is mandatory every run - it is both the original-ranking record (so a manual reweight stays recoverable) and the reserve catalog.
- **All operator subsections present** under `# INTERNAL` in the order from `### Outputs -> #### Sections - what goes where` (Research Sources, Topic Ideas, Selection Methodology Detail, Episode 1 Branded Search Benchmark, Provenance).
- **EP1 row** is `The Founder Interview` / Theme `Founder Story` (fixed, no `Brand / ` prefix), with a populated `Keywords` cell (the branded-search `Total Search Demand` line + branded query list from the benchmark), not `-`.
- **EP2 row** is the flagship ebook anchor - an ebook-worthy comprehensive-guide topic carrying real search demand, NOT a low-demand wow-factor topic. If slot #2 holds a low-MSV narrow topic while a higher-demand ebook-worthy topic sits lower in the main 12, that is a contract violation.
- **No duplicate episodes** in the main 12 or additional set (entity overlap > 50% OR keyword overlap > 40% triggers a bundle).
- **Scoring model not restated** - the weights / numbers / corroboration thresholds appear only in `references/scoring-model.json`, never in the rendered body or this skill.
- **Dedup check ran** - no `Covered` practice area produced episodes without an explicit refresh request.
- **Show Identity match** - the five fields (Podcast Name, Tagline, Podcast Description, Audience, Topic Mix) are identical across `.md`, `.json` `show_identity`, and the Drive Doc; the Topic Mix footnote is present only when no client breakdown was given.
- **No standalone Search Volume column** - the main and additional tables have 5 columns each; the summed MSV renders inside the `Keywords` cell as a bold `Total Search Demand` first line, never as its own column.
- **No client-facing wave narrative** - the production-wave text appears only under the INTERNAL `## Selection Methodology Detail`, never as prose below the 12-Episode Plan table.
- **No pipeline-position metadata** - the rendered deliverable carries no "Pipeline position" / upstream-downstream line anywhere (Provenance or elsewhere).
- **Roboto applied** across the Doc body, headings, tables, headers, footers - or `branding: "font-fallback-arial"` is set in metadata.
- **Comment preservation (post-publish runs only):** if the Drive Doc is already shared, verify the surgical-edit script was used and the comment count delta is >= 0. The formatter on a shared Doc is a contract violation.

**Fourth - Post-render Doc QA (mechanical, scripted).** A manual checklist did not stop the 2026-05-21 batch from shipping 12 Docs with the branding formatter bypassed (iteration-log `2026-05-21-001` / `-002`). Run the scripted validator against the finished Google Doc as the final QA gate, before `## Ship` completes:

```
scripts/qa-doc-format.sh <doc_id>
```

It fetches the Doc JSON via `gws` and FAILS (exit 1, every failure printed) on any of these nine mechanical checks. Each maps to a defect that shipped in the batch:

1. **No cover page** - no page break before `## Show Identity`, or fewer than 3 centered cover lines. Catches a formatter-bypassed Doc (`topic-plan-formatting.sh` Phase A skipped).
2. **No CE logo** - no inline image object on the cover (Phase B skipped).
3. **Font not Roboto** - more than 5% of styled text runs (body + tables) carry a non-Roboto `weightedFontFamily` (Phase C skipped - a pandoc Doc keeps Aptos/Calibri).
4. **Tables unstyled** - any data table whose header row is not CE Blue, or any >=4-row table with no zebra body shading (Phase E skipped).
5. **`# INTERNAL` marker unstyled** - the INTERNAL H1 is not >=20pt, not CE Blue, not bold, or has no top border (Phase F skipped).
6. **Search volume missing from question tables** - any `## Episode Breakdown` 3-column question table (episodes 2+) with zero `/mo` volume markers in its body; also flags the wrong column name `Search Phrases` (canonical is `Keywords`). Catches raw n-gram phrases shipped without the MSV join.
7. **Section-order drift** - the five client-facing H2s not in canonical order, or the first H2 under `# INTERNAL` is not `Research Sources`.
8. **No running page header** - the Doc has no header, or the header text is not `Case Engine | Podcast Topic Plan ...` (Phase H skipped).
9. **ISO date on the cover** - a cover line matches `YYYY-MM-DD` instead of long form (`May 20, 2026`).

**A topic-plan Doc that was not formatted by `topic-plan-formatting.sh` is NOT shippable.** If `topic-plan-formatting.sh` could not run (e.g. the md->Google Doc conversion 500s and an agent reaches for a pandoc md->docx->Doc workaround), the Doc has no cover, no Roboto, unstyled tables, no INTERNAL marker, and no page header - `qa-doc-format.sh` will fail it. Fix the formatter path; do not ship the pandoc output. The validator runs clean (9/9) against the reference standard Sutliff & Stout v2 Doc.

**On failure:** fix the markdown source, regenerate the `.json` and `.docx`, re-run the formatter, re-run all checks including `qa-doc-format.sh`. Do not proceed to `## Ship` until QA returns clean.

## Ship

What is?
The publish phase - write the four artifacts to the per-client Drive Topic Plan folder and the local mirror. The n-gram tables are already built (the mandatory `### Build the n-gram tables` step in `## Create`); Ship publishes the plan and the per-episode question roll-up it produced.

### What ships

- **`topic-plan-v{n}.md`** (Markdown) - canonical source, retains the `# INTERNAL` block.
- **`topic-plan-v{n}.json`** (JSON) - schema-validated structured episode data.
- **`topic-plan-v{n}.docx`** (DOCX) - Word / PDF-friendly local copy.
- **Drive Doc** (Google Doc) - branded human-facing canonical view.

### Where it ships

- **Primary (Drive):** the canonical Map 5 slot `AEO/Podcast/Topic Plan/Topic Plan: {practice_area} // {client_name}/` inside the live client folder. One subfolder per practice area. Resolve `{Client Folder}` via the user-supplied client folder URL. Never inline the full path - see `### Outputs -> #### Drive destination`.
- **Cross-client topic catalog cache:** every candidate topic that did not make the curated 12 also mirrors to `templates [master]/AEO Templates/Podcast/Topic Catalogs/{Practice Area}/{Anchor Scope}/` so the next client in the same vertical starts from a catalog hit. Both writes happen every run.
- **Secondary (local mirror):** `~/Desktop/claude_code/deliverables/podcast-research/{topic-slug}/{episode-slug}/02-topics/`.
- Write to both destinations every run. On a write error to one, ship to the other and surface the partial state in the report; never silently lose the deliverable.

### How it ships

1. **Write the markdown first** - it is the source of truth; the JSON, docx, and Doc are renders of it.
2. **Upload the bundle** following the create-vs-update decision tree in [Push to Drive](https://docs.google.com/document/d/1831TsbxcyNGPmq67zblA5rC66U-XQv20mVsNovFqjfg/edit). First-time create = `files.create` (capture the returned fileId). Subsequent writes = `files.update` against the existing fileId so the URL is preserved. Upload `.md` as `text/markdown`, the Google Doc sibling as `application/vnd.google-apps.document`, `.docx` as the Word MIME type, `.json` as `application/json`.
3. **Brand the Doc.** On first publish run `scripts/topic-plan-formatting.sh` - it builds the cover page, applies Roboto across every text layer, styles the tables (CE Blue header row + zebra body, fixed column widths), styles the `# INTERNAL` marker, and sets the page header/footer. On any post-publish run use `scripts/topic-plan-surgical-edit.sh` instead - see the POST-PUBLISH EDIT RULE banner at the top of this file. The rule is binary; there is no third option. To produce a client-share clone truncated at `# INTERNAL`, use `scripts/topic-plan-client-render.sh`.
4. **Archive on refresh.** When the run is `archive-and-rebuild`, move existing artifacts to `_archive-{YYYY-MM-DD}/` before writing.
5. **Never touch sibling folders** this skill did not produce (e.g., `01 Entities/` from an entity-research run).
6. **Report** the Drive URL on success; on failure report the error and leave the local copy intact. List the n-gram tables built in `### Build the n-gram tables` so the team can see the full per-episode set landed alongside the plan.

### Who to Notify

N/A - `notify: []`. The Topic Planner hands off in-conversation (the final report). No Slack / SMS / email fires after the artifact lands.

---

## Learning & Iteration

- [ ] Track whether 12 main episodes is the right count for a single practice area, or whether it should flex with entity-map size.
- [ ] Measure whether the corroboration ranking floor changes the main 12 often enough to justify the mechanic, or whether raw `authority_score` order would land the same plan.
- [ ] Track whether the compiled episode boundaries hold up at recording time, or whether producers routinely re-split episodes.
- [ ] Evaluate the keyword-research fallback path - does it produce a comparable plan to the entity path, or is the quality gap large enough to always require entity research first?
- [ ] Track `demand` bucket correlation with actual episode performance (views, engagement) once episodes ship, and re-tune `scoring-model.json` weights if the correlation is weak.
- [ ] Consider a "mini-series" grouping (3-4 episode arcs) as a compilation output alongside standalone episodes.
- [ ] Track whether the mandatory n-gram build per episode adds enough run time to warrant parallelizing the `pod-2B-n-gram-table` invocations, or whether sequential is fine.
- [ ] Measure whether the `## Episode Breakdown` roll-up actually shortens the client QA loop, or whether clients still want the full n-gram tables to review.
- [ ] Track how often `serp_features` (especially the AI Overview flag) changes the main 12 versus pre-`serp_features` ranking, to validate the signal's weight in `scoring-model.json`.

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-03-18 | Initial version - piloted with truck accidents (10 clusters, 22 episodes, 4-wave production order). | Gabe Jordan |
| 2026-04-07 | Keyword-research fallback added; search volume + intent classification added; 5th scoring dimension (`demand_signal`). | Gabe Jordan |
| 2026-05-14 | Fathom Service Weighting made mandatory as the dominant scoring modifier; INTERNAL reserve section added; one main table + Additional Topics structure locked; visual standard locked to the entity-research reference docx; four-artifact Output Contract documented. | Gabe Jordan |
| 2026-05-14 | v2.0.0 - cowork merge; Mode A / Mode B runtime probe added; scripts hoisted to top-level `scripts/`. | Gabe Jordan |
| 2026-05-15 | Rationale promoted to a table column; table column widths + density locked; post-publish edit rule + surgical-edit script locked. | Gabe Jordan |
| 2026-05-19 | v3.0.0 - sales-sketch mode removed; Drive target moved into the per-client `AEO/Podcast/Topic Plan/` folder; `## Research Sources` INTERNAL section added; EP1 branded-search rendering rule. | Gabe Jordan |
| 2026-05-20 | v4.0.0 - flagship redesign. New methodology architecture: Ingest -> Score -> Compile -> Episodes; the episode boundary is now an OUTPUT of compilation, not an upfront cluster-to-episode guess. Scoring moved to `scripts/score-topics.py`, which loads the canonical 10-signal model from `references/scoring-model.json` (3 buckets - Authority / Demand & Trend / Competitive - plus a corroboration mechanic with a ranking floor); the SKILL points at the model file as the single source of truth and no longer restates weights. Mahalanobis demoted to an optional `--mahalanobis` diagnostic. Fathom Service Weighting removed as a mandatory dominant scoring layer - replaced by a Greeting-stage practice-area-breakdown ask that governs the episode mix (pure scoring when none given); Fathom is now one optional client-intel input. Added the INTERNAL `## Topic Ideas` table (every candidate in original unmodified ranking order, always rendered, so a manual reweight stays recoverable) and a Ship-phase n-gram handoff that offers to auto-invoke `pod-2B-n-gram-table` for every locked episode (main 12 AND additional). Conformed the whole file to the canonical CE skill structure (frontmatter -> What is -> Workflow -> Trigger phrases -> Greeting -> Best Practices -> Checks -> Prepare Inputs -> Create -> Quality Assurance -> Ship -> Learning & Iteration -> Change Log); consolidated the heavy redundancy of the old Steps / Gotchas / QA restatement. JSON schema note: `authority_score` + `corroboration_flag` per episode and a top-level `topics_by_score` array replace the legacy `authority_score_linear` 5-dimension shape; `pod-2B-n-gram-table` consumers reading `rank` + episode metadata are unaffected. | Gabe Jordan |
| 2026-05-20 | v4.1.0 - probe-strip pass. Removed the `### Probe environment` H3 and all capability-probing apparatus - the skill runs locally in Claude Code, calls its tools directly, skips or fails on a tool error. `#### Capabilities` (Inputs) became `#### Tools the skill calls`; `#### Capabilities` (Outputs) became `#### Write destinations`. `runtime.capabilities` dropped from metadata; cowork-ephemeral-FS branching removed - the local mirror writes unconditionally. `## Checks` opens with `### Orient` (iteration-log read + scoring-script verify). Frontmatter `version`/`date`/`owner` moved into a `metadata` block. Workflow diagram replaced with the unified 4-phase pipeline diagram (Foundation / Research / Planning / Run of Show). Cross-references repointed to the new pipeline codes. | Gabe Jordan |
| 2026-05-20 | v4.0.0 finish pass (pre-launch refinements, same major version). N-gram tables promoted from an optional Ship-phase yes/no handoff to a mandatory `### Build the n-gram tables` step in `## Create` - auto-invokes `pod-2B-n-gram-table` for every locked episode (main 12 AND additional), positioned after the episode plan is formed and before render. Added the client-facing `## Episode Questions` roll-up: one compact table per episode (`Question` / `Search Phrases` / `Rationale`, two episodes per page) sourced from each episode's n-gram output, so the client QAs the topics and the questions in one deliverable; wired into the deliverable structure, Outputs contract, JSON shape, and QA gates. Scoring model gained an 11th signal, `serp_features` (AI Overview / video pack / featured snippet / image pack presence per query); the Ingest step now captures SERP feature flags from the content-gap report and the corpus carries a `serp_features` value per topic. INTERNAL `## Research Sources` table gained a 4th link column for the n-gram tables folder. Resolved the orphan `pod-10` (clip-table) reference - clip table folded into `pod-4D-post-production-pack`, workflow diagram updated. Reconciled `references/schemas/` (plural) into `references/schema/` (singular, canonical); `topic-plan-schema.json` now sits beside `scoring-model.schema.json`. `scripts/README.md` updated for `score-topics.py` + `validate-scoring-model.py`, `mahalanobis-score.py` marked legacy; `__pycache__/` removed from the bundle. | Gabe Jordan |
| 2026-05-20 | v4.0.0 format-feedback pass (same major version) - eleven items from Gabe's review of the v4 format sample. (1) Client-facing body carries NO frontmatter block; the cover page alone holds firm / location / prepared-by / date. (2) Show Identity is now FIVE bold-label fields in order Podcast Name / Tagline / Podcast Description / Audience / Topic Mix (was four; "Target Audience" renamed to "Audience"). (3) New `Topic Mix` field - practice-area episode percentages; sourced from the client breakdown if one was given at intake, else derived from the scoring output's episode distribution. (4) Episode tables (Main 12 + Additional Topics) DROP the standalone `Search Volume` column; the summed MSV now renders inside the `Keywords` cell as a bold `**Total Search Demand:** {sum}` first line, then a `<br>`, then the keyword list. Main table is now 5 cols at `[32,134,70,116,116]`pt; Additional at `[134,70,116,100,48]`pt (both sum 468). `topic-plan-formatting.sh` Phase E.5 header signatures + `MAIN_WIDTHS` / `BONUS_WIDTHS` updated to the 5-col shape. (5) Show Identity labels render bold in the Doc. (6) Production-wave narrative moved from client-facing (under the 12-Episode Plan table) into the INTERNAL `## Selection Methodology Detail` - v4 wave order is operator-only. (7) Pipeline-position / upstream-downstream metadata removed from the rendered deliverable entirely - it is skill-internal plumbing, never shipped. (8) Topic Mix footnote is conditional: scoring-derived case shows the "percentages reflect where search demand..." sentence; client-breakdown case omits the footnote; the "no client topic breakdown was specified" clause is removed from both. (9) Episode 1 ("The YOU Interview") Theme is fixed to `Founder Story` (no `Brand / ` prefix); E1's questions are never n-gram-built - the `### Build the n-gram tables` step skips E1. (10) E1's Episode Questions roll-up is populated from the canonical Founder Story interview set at `references/e1-founder-interview-questions.md` (21 questions, S1-S5 + Outro, `{{LOCATION}}`/`{{BUSINESS}}`/`{{NICHE}}` tokens filled per client). (11) E1's Episode Questions heading reads `Episode 1: Founder Story` (theme), not `Episode 1: {title}` - E1 is the standing exception. Schema (`topic-plan-schema.json`) reconciled - 5-field `show_identity` (+`topic_mix` object with conditional footnote), 5-col table column definitions + widths, INTERNAL-only wave, no client-facing pipeline metadata, E1 Theme = `Founder Story`, `episode_questions[].question_source` enum (`n_gram_table` / `founder_canonical`), `episode_label` E1 exception. | Gabe Jordan |
| 2026-05-20 | v4.0.0 consolidation pass (same major version) - four format-feedback items from Gabe's review of the v4 format sample, applied to the sample md, SKILL.md, and `topic-plan-schema.json`. (1) The INTERNAL "Voice calibration" block (trial-mentality / Houston-specific / AEO-first bullets) was removed. (2) The `## Internal Rationale - Show Name + Audience + Voice` INTERNAL section was removed entirely, including its Show Name Decision Log content and the schema's `internal_section.catalog_by_practice_area.show_name_decision_log` field. (3) `## Research Sources` is now the FIRST H2 under `# INTERNAL` (was after `## Topic Ideas`); the INTERNAL `h2_order` is now Research Sources -> Topic Ideas -> Topics by Theme -> Selection Methodology Detail -> Episode 1 Branded Search Benchmark -> Provenance, reflected in the Sections table, the render-step prose, the QA gate, and the schema `structure_invariant`. (4) Episode 1's Episode Questions now render in TABLE form - the same compact `Question` / `Search Phrases` / `Rationale` per-episode table used for episodes 2-12 - with the 21 founder-interview questions UNNUMBERED and grouped under their S1-S5 + Outro segment headings (one table per segment), the Search Phrases / Rationale cells left blank or `N/A`. Was previously a numbered/segment list with the two columns dropped. SKILL.md `### Render the topic plan` Episode Questions step + both QA gates updated; schema `episode_questions[].question_source` description updated. Schema valid Draft-07; `validate-scoring-model.py` PASS. Version stays 4.0.0. | Gabe Jordan |
| 2026-05-20 | v4.0.0 format pass (same major version) - four items from Gabe's review of the v4 format sample, applied to the sample md, SKILL.md, `topic-plan-schema.json`, and `topic-plan-formatting.sh`. (1) The `## Episode Questions` H2 was renamed to `## Episode Breakdown` - rendered-heading + prose change only; the JSON field key `episode_questions` is unchanged (renaming it would break downstream consumers). All rendered-heading and prose references across SKILL.md and the schema heading const updated. (2) Episode 1's Episode Breakdown entry collapsed from six per-segment `####` sub-headings + six per-segment tables to ONE table - two columns, `Segment` / `Question`, the 21 founder-interview questions top to bottom and UNNUMBERED, the `Segment` column carrying S1-S5 / Outro. E1's table has no Search Phrases column and no Rationale column - neither applies to a founder interview. E2-E12 and the Additional Topics tables keep their `Question` / `Search Phrases` / `Rationale` columns. (3) The `## Episode Breakdown` section intro paragraph ("The questions each episode covers, rolled up from...") was removed - the H2 is followed directly by the first episode heading. (4) `## Research Sources` restructured from a multi-column per-(topic,scope) link table to a simple 3-column `Name` / `URL` / `Notes` table, one row per research artifact actually used. Schema `research_sources` structure rewritten (name/url/notes), `episode_questions` items now carry an optional `segment` field with `search_phrases`/`rationale` E1-exempt, `column_names_invariant` E1 exception noted. `topic-plan-formatting.sh` Phase E.5 header signatures updated (`SIG_SOURCES` -> Name/URL/Notes, new `SIG_QUEST_E1` for the Segment/Question table). Doc re-rendered in place. Schema valid JSON; `validate-scoring-model.py` PASS. Version stays 4.0.0. | Gabe Jordan |
| 2026-05-20 | v4.1.0 format pass (same major version) - Episode 1's Episode Breakdown table redesigned per Gabe's review. (1) The `Segment` column was removed - the interview-flow grouping is no longer a rendered column (the canonical question set stays segment-organized at its source file). (2) A `Rationale` column was added to the right of `Question`. For E1 ONLY, this column carries a few hard-coded words naming what each question accomplishes in the founder interview (e.g., establish credibility, position as expert, emotional close) - distinct from the research-signal Rationale on episodes 2-12. E1's table is now `Question` / `Rationale` (two columns, no Segment, no Search Phrases). SKILL.md (3 spec locations), `topic-plan-schema.json` (`segment` property removed from `episode_questions[].items`; `question_source`, `questions`, `rationale` descriptions + `column_names_invariant` E1 exception updated), and `topic-plan-formatting.sh` (`SIG_QUEST_E1` -> `['question','rationale']`) updated. The per-question E1 rationale strings are hard-coded in `references/e1-founder-interview-questions.md`. | Gabe Jordan |
| 2026-05-20 | v4.1.0 format pass (same major version) - INTERNAL `## Topic Ideas` table redesigned per Gabe's review, and Change 1's E1 follow-through completed. (1) The `## Topic Ideas` table dropped three columns - `Authority Score`, `Corroboration`, and `Signal Families` - and added a `Rationale` column; the table is now `Rank | Topic | Theme | Rationale` (6 cols -> 4 cols). The new `Rationale` column is AI-written: it explains in plain language why the topic earned its score and rank by naming the actual signals behind it (comma-listed signals, then ` -- `, then a verdict - e.g., `5 PAA, related searches, has AI overview -- great demand for topic`; `high search volume, right intent`). Updated across SKILL.md (Outputs INTERNAL-structure item, render-step prose, QA gate), `topic-plan-schema.json` (`topics_by_score` `column_names_invariant` -> `["Rank","Topic","Theme","Rationale"]`, `render_format` description, top-level `description` v4.1.0 note; the JSON data fields `authority_score`/`corroboration_flag`/`signal_families_fired` are KEPT - `pod-2B-n-gram-table` reads them - only the rendered columns changed), and `topic-plan-formatting.sh` (`SIG_SCORE` -> `['rank','topic','theme','rationale']` + comment line). The scoring math and `scoring-model.json` are unchanged. (2) Change 1 follow-through: `topic-plan-formatting.sh` `SIG_QUEST_E1` was set to `['question','rationale']` (its comment block updated), and `references/e1-founder-interview-questions.md` was rebuilt with the 21 hard-coded per-question rationales and a lead-in noting the render is now a flat two-column `Question | Rationale` table. | Gabe Jordan |
| 2026-05-20 | v4.2.0 - `## Topic Ideas` / `## Topics by Theme` consolidation + three gap-closing methodology rules. (1) The INTERNAL `## Topic Ideas` table gained a 5th column, `Notes` - a freeform INTERNAL field that records each topic's disposition once episode selection runs (`MAIN-#`, `BONUS`, `RESERVE`, `CUT (reason)`) plus any operator / review comment and the `editorial` mark for manual candidates. Empty on a fresh scoring run, populated at episode selection. Table is now `Rank | Topic | Theme | Rationale | Notes` (4 cols -> 5). (2) `## Topics by Theme` removed entirely - it was redundant with `## Topic Ideas`, which already groups by theme via its `Theme` column and now carries disposition via `Notes`; one table does both jobs (original-ranking record + reserve catalog). The disposition tags that used to live in the Topics by Theme catalog now live in the Topic Ideas `Notes` column. INTERNAL H2 order is now Research Sources -> Topic Ideas -> Selection Methodology Detail -> Episode 1 Branded Search Benchmark -> Provenance. (3) Three gap-closing rules added: no pre-filtering on perceived strength - never drop a research-supported topic for looking like a weak episode, exclude only genuine non-topics, the score makes the call (a pre-filter once silently hid a real topic, Distracted Driving, from a client run); ingest comprehensively - both Topic-Only and Topic+Location research and all relevant location scopes, surface every practice area with research; manual / editorial candidate topics - operator-supplied forward-looking / trend topics with no search data join the candidate set, score on whatever signals exist, and are marked editorial in `Notes`. Schema (`topic-plan-schema.json`) and formatter (`topic-plan-formatting.sh`) updated in the same pass by sibling agents - 5-col `topics_by_score` `column_names_invariant`, `Topics by Theme` section / `h2_order` removed. | Gabe Jordan |
| 2026-05-20 | v4.2.0 continuation (same-day, version unchanged) - two format items. (1) The INTERNAL `## Topic Ideas` table re-gained a `Score` column, inserted between `Theme` and `Rationale`; it renders the topic's `authority_score` to three decimals (e.g., `0.653`). The table is now `Rank | Topic | Theme | Score | Rationale | Notes` (6 columns). Updated across SKILL.md at every column-list location (the `### Score topics` step, the INTERNAL-structure numbered item for `## Topic Ideas`, and the QA mechanical-checks gate). (2) Episode 1's topic title was renamed from `The YOU Interview` to `The Founder Interview` everywhere it appears; the Theme stays exactly `Founder Story` (unchanged). Schema (`topic-plan-schema.json`) and formatter (`topic-plan-formatting.sh`) updated in the same pass by sibling agents - 6-col `topics_by_score` `column_names_invariant` with the `Score` column, and the E1 title rename. | Gabe Jordan |
| 2026-05-20 | v4.2.0 continuation (same-day) - phase 2/3 pipeline build + the corroboration-floor fix. (1) FIXED the corroboration ranking floor in `score-topics.py`: `apply_corroboration_floor` was a global two-tier sort that floated every corroborated topic above every non-corroborated one regardless of score (a 0.20 topic outranking a 0.59 topic). It is now a BOUNDED LOCAL PROMOTION - a corroborated topic may rise above a non-corroborated topic directly above it only when the score gap is within `corroboration.ranking_floor.score_margin` (new field, 0.05) in `scoring-model.json`; the schema gained `score_margin`. (2) Added the `### Build the Episode Question Tables` SOP step and `references/prompts/episode-question-tables-prompt.md` - rolls each episode's n-gram questions into the `## Episode Breakdown` tables, then a cross-episode de-duplication pass (exact + near-duplicate). (3) Added `references/prompts/select-episodes-prompt.md` - the episode-selection prompt (compile -> apply Topic Mix breakdown -> 12 main + 3 additionals one-per-category -> write disposition into the `Notes` column). (4) Bundled per-table render scripts in `scripts/`: `render-12-episode-plan.py`, `render-additional-topics.py`, `render-topics-by-score.py`, `render-episode-question-tables.py`, and the shared `lib_doc_table.py` (`rebuild_table` cleans accumulated blank paragraphs so tables sit flush; `keywords_cell` locks the Keywords-cell format - `{sum}/mo Total Search Demand` then `keyword - X/mo` list). (5) Keywords-cell format locked across SKILL.md to the `keywords_cell()` output. (6) The n-gram-feedback rule now scores surfaced topics on the spot (re-run `score-topics.py` over the full set) rather than leaving them unscored. (7) Episode Breakdown gets a divider border between episodes; Episode Question table column renamed `Search Phrases` -> `Keywords` with per-question MSV. | Gabe Jordan |
| 2026-05-21 | The cross-episode de-duplication pass now PERSISTS into the canonical n-gram tables. Previously the dedup ran in-memory in `render-episode-question-tables.py` for the Doc render only - the `n-gram-table.json` files still carried the duplicate, so `pod-3A-ros-template` (which reads `n-gram-table.json`) would pull it back. `render-episode-question-tables.py` gained `persist_dedup()`: when the dedup drops a question it rewrites that episode's `n-gram-table.json` (rows, `row_count`, a `cross_episode` entry in `dedup_merges`) and the `N-Gram Table.md` mirror (drop the row, renumber). Idempotent. Paired with the new `pod-3A-ros-template` N-Gram-Table-vs-Topic-Plan reconciliation check so the question set the client reviewed in the Topic Plan is exactly what reaches the Run of Show - zero drift. | Gabe Jordan |
| 2026-05-21 | Added `references/topic-seed-catalog.json` - a seed taxonomy (legal domain -> practice areas -> seed episode topics) that gives the candidate set an evergreen FLOOR instead of being purely research-emergent and agent-judgment-dependent. The `## Checks` step `### Resolve client and practice area` was renamed `### Resolve client, domain, and practice areas` and now resolves the legal domain, confirms the firm's active practice areas by scraping the firm website, and loads each area's `seed_topics`. `## Prepare Inputs -> Assemble the corpus` now starts from the seed topics and merges research-derived topics on top (de-duped). The n-gram-feedback rule folds surfaced topics back into the catalog so it compounds run-over-run. Catalog ships with Personal Injury fully populated (10 practice areas, 77 seed topics) and Family Law populated (9 practice areas, 42 seed topics, genericized from the Law Offices of Todd K. Mohink topic plan); Criminal Defense is stubbed. Added to `#### Auto-read` and `references/README.md`. | Gabe Jordan |
| 2026-05-21 | Renamed the INTERNAL `## Topics by Score` section to `## Topic Ideas` everywhere - the rendered heading and all skill prose across SKILL.md, `topic-plan-schema.json`, `topic-plan-formatting.sh`, the `references/prompts/` prompts, `scripts/README.md`, and the iteration log. The render script `render-topics-by-score.py` was renamed to `render-topic-ideas.py`. The JSON key `topics_by_score` is UNCHANGED - `pod-2B-n-gram-table` reads it as a handoff field; only the rendered section name changed. "Topics by Score" no longer reads cleanly now the section sits inside the `## Topics` H2 and the table is the full scored candidate catalogue, not a score-only view. | Gabe Jordan |
| 2026-05-20 | `topic-plan-formatting.sh` Phase G added - Research Sources URL column clickable-hyperlink self-heal. The INTERNAL `## Research Sources` table authors each URL cell as a markdown link `[Open in Drive](url)`; Drive's markdown->Doc auto-conversion reliably converts body-text links but is unreliable for links inside table cells, sometimes leaving the literal `[label](url)` text non-clickable. New Phase G ([9/9]) runs after the header/footer phase: it finds the Research Sources table, scans the URL column (col index 1) only, and for any cell whose text is a literal markdown link it deletes the literal text, inserts just the label, and applies a real Docs hyperlink (`updateTextStyle` with a `link`). Cells Drive already converted are detected (run carries `textStyle.link`) and left untouched - idempotent on re-run. Name/Notes columns and all other tables are never touched. Phase counters renumbered `[N/8]` -> `[N/9]`. No SKILL.md spec change - the render spec already required a clickable hyperlink; this only hardens the formatter to guarantee it. | Gabe Jordan |
| 2026-05-21 | `topic-plan-formatting.sh` hardened against large Docs - the formatter was failing with `argument list too long` on any topic plan with enough tables. Root cause: every `batchUpdate` call passed its full request body as an inline `--json` shell argument; a 12-episode plan with 20+ tables generates a ~1.8MB table-style body, which overflows the OS `ARG_MAX` (the kernel caps combined argv+envp at exec) and the call dies before reaching the API. Two-part fix: (1) a new `batch_update` shell helper writes the request body to a temp FILE and a python child reads it from disk - the body never crosses an argv or environ boundary - then splits the `requests` array into <=150-request chunks, one `gws` call per chunk (each chunk's `--json` arg is small). All 11 large-body `batchUpdate` call sites route through it (the 2-request `createHeader`/`createFooter` call stays direct). Mirrors the chunking `lib_doc_table.py` already did. (2) Phase G's `RS_LINK_REQ` heredoc was switched from an unquoted `<<PYEOF` to a quoted `<<'PYEOF'` (reading `DOC_JSON_FILE` from the exported env var) so the regex/comment token `[label](url)` is never glob- or command-substitution-expanded by the shell; the regex end-anchor `\)\$` was corrected to `\)$`. No formatter-output change - same branded Doc; the script just no longer dies on big plans. Fixes iteration-log `2026-05-21-001`. | Gabe Jordan |
| 2026-05-28 | v4.3.0 - EP2 ordering rule added. Slot #2 of the main 12 is now ALWAYS the flagship ebook anchor: the single best ebook-worthy topic (broad, evergreen, comprehensive-guide) that ALSO carries real search demand - never a low-demand wow-factor topic (e.g. a firm's own marquee case), even when that topic scores high. The wow-factor topic ranks elsewhere in 3-12 instead. Codified in `### Form the episode plan` (new EP2 bullet beside the EP1 bullet), the Quality gates, and the QA mechanical-checks gate (EP2-row check). Rationale: episode 2 doubles as the firm's lead-magnet ebook, so it must be a meaty demand-backed guide, not a niche highlight. Driven by Gabe directive 2026-05-28 during the Mohink v3 run (where Braun v. Headley - his own published case, 300/mo - was correctly displaced from slot #2 by the Maryland Divorce Timeline, 4,000/mo). EP1 (Founder Story) rule unchanged. | Gabe Jordan |
| 2026-05-28 | v4.4.0 - the `Swaps for` column was removed from the Additional Topics table. The table is now 4 columns - `Topic`, `Theme`, `Keywords`, `Rationale` - at widths `[150, 80, 128, 110]` PT (sum 468, up from the old 5-col `[134, 70, 116, 100, 48]`). Swap relationships are no longer client-facing; when an operator wants to record which main episode a candidate could replace, that note lives in the INTERNAL `## Topic Ideas` `Notes` column instead. Updated across SKILL.md (Quality gates Additional Topics column line, the `### Render the topic plan` Additional Topics step, the `### Form the episode plan` Additional Topics bullet - dropped the `Swaps for` note instruction), `references/schema/topic-plan-schema.json` (bonus `column_names_invariant` and default columns drop `Swaps for`; widths `[150,80,128,110]`; `swaps_for` removed from the bonus item required fields and properties), `scripts/topic-plan-formatting.sh` (`SIG_BONUS` -> `['topic','theme','keywords','rationale']`, `BONUS_WIDTHS` -> `[150,80,128,110]`, comment block), `scripts/render-additional-topics.py` (drops the column), and `references/prompts/select-episodes-prompt.md` (dropped the `Swaps for` note instruction). Driven by Gabe directive 2026-05-28 and applied to the Mohink v3 deliverable in the same pass. | Gabe Jordan |
| 2026-07-10 | v4.5.1 - canonical three-field geo model stamped (Gabe directive 2026-07-10, Whalen scoping). Added the `### Geo model` Best-Practices subsection defining the three fields with exact labels - **Targeting strategy** (single-location vs multi-location), **Optimization scope (show anchor)** (City / State / County / Regional), **Episode geo target** (the per-episode target city) - and the `Anchor scope != per-episode target` rule (research at anchor breadth; each episode emphasizes its target city naturally, a ceiling never a forced quota; no-city-quota / natural-tonality preserved). Made explicit that THIS skill is where the per-episode geo target is assigned and confirmed: added an **Assign each episode its Episode geo target** bullet to `### Form the episode plan` (single-location -> all 12 share the one anchor city as Full episodes; multi-location -> one Mini episode per target city across the footprint), added `geo_target` to the JSON episode shape, and replaced the state-check `Scope:` line with the three geo fields. EP1 (Founder Story) and EP2 (flagship ebook anchor) rules unchanged - their geo target is the show's home / anchor city. Schema (`topic-plan-schema.json`) bumped 4.2.0 -> 4.2.1 (PATCH): added optional `metadata.targeting_strategy`, `metadata.optimization_scope`, and per-episode `geo_target` on main and bonus rows. | Gabe Jordan |
| 2026-06-02 | v4.5.0 - the `## Show Identity` Topic Mix line now carries each practice area's episode count in parentheses. Format changed from `{Practice Area} {percentage}%` to `{Practice Area} {percentage}% ({N} episodes)` (e.g. `Car Accidents 33% (4 episodes)`, pluralized `(1 episode)` / `(2 episodes)`), comma-separated on one line; counts sum to 12. The format lives in the `show_identity.topic_mix.percentages` string (authored when show_identity is built; `topic-plan-formatting.sh` only bolds the label, it does not reformat the content - no script change needed). Updated SKILL.md (the `## Show Identity` render spec + per-entry format rule, the default-mix render example, the Greeting default-mix paraphrase) and `references/schema/topic-plan-schema.json` (the `show_identity` render rule + the `topic_mix` and `topic_mix.percentages` descriptions/examples). Driven by Gabe directive 2026-06-02 during the Grife med-mal topic-mix work. | Gabe Jordan |
| 2026-07-14 | v4.6.0 - added the **Cross-Service Roundup** to the Default PI mix (Gabe directive 2026-07-14). Slot #2 is now the standing Cross-Service Roundup episode (top AI-cited question per confirmed practice area, grouped by service; never dropped - spans whatever services the firm confirms). The flagship ebook anchor moved from slot #2 to **slot #3** (EP2 is NOT the anchor - it is the roundup; EP3 is the anchor, by default the top Car Accidents comprehensive guide). To make room within the fixed 12 slots, **Car Accidents dropped 4 eps -> 3 eps** (25%, slots 3/4/6; was 33%, slots 2/3/4/6). New Default mix: Car Accidents 25% (3), Med Mal 17% (2), Truck 17% (2), Cross-Service Roundup 8% (1, slot 2), Wrongful Death 8% (1), Founder Story 8% (1), Slip & Fall 8% (1), Bicycle/Pedestrian 8% (1) - counts sum to 12. Only the Default (no-client-breakdown) PI path changes; a client-stated breakdown still overrides everything, and non-PI firms still take pure scoring. EP3 (new anchor) inherits the home/anchor-city geo target the EP2 anchor previously carried; EP2 roundup is also home-city. Updated SKILL.md (`### Form the episode plan` Default-mix block + slot note, split the old EP2 rule into an EP2 Cross-Service-Roundup rule and a new EP3 ebook-anchor rule, `## Show Identity` per-entry example + default-mix render branch, Greeting default-mix paraphrase), `references/prompts/select-episodes-prompt.md` (Default-mix slot list), and `references/schema/topic-plan-schema.json` (three Topic Mix example strings). Additional Topics categories unchanged - Car/Med Mal/Truck are still the multi-slot areas. Pattern source: EP2 cross-service-roundup memory (top AI-cited Q per service, grouped-by-service n-gram table). | Gabe Jordan |
| 2026-07-31 | v4.7.0 - removed the `pod-1-podcast-bible` dependency and all Fortress (`fortress-db`) access ahead of the skill moving to an environment without DB reach. (1) All podcast-bible references stripped: workflow Phase 1 box, the prereq workflow item (now "Client architecture (from the Greeting)"), the "flows into pod-1-podcast-bible" Show Identity clause, the Drive "Sibling to Podcast Bible/" note, upstream routing, the font-lock parity note, the schema "feeds Show Bible §X" description clauses, and the `show_bible` `input_source` enum value. Architecture (client name, anchor scope, targeting strategy, extensions, audience) now comes from the Greeting, with an optional `podcast-overview.md` auto-fill. (2) Fortress removed: dropped the `mcp__fortress-db__query` tool bullet, the `clients.clients` client-name / practice-area lookups, the `clients.campaigns` alignment signal, and `clients.clients.drive_folder_id` Drive-folder resolution (now user-supplied client name / folder URL). (3) Topic mix is now a REQUIRED input: the Greeting will not fire the plan until the user provides a mix or explicitly says "use the default mix" - no silent default. Comment cleanup in `scripts/topic-plan-formatting.sh` (dropped bible_formatting.sh provenance lines). | Gabe Jordan |
