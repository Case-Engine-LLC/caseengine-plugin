---
name: pod-3A-ros-template
description: >
  Build the tokenized, generic Run of Show template for a podcast episode at
  Topic Only / Location / Extension scope - 12 approved `{{PLACEHOLDERS}}` so
  one template serves every firm that records at that scope. Use whenever
  someone says "ros template for [episode]", "create ros template for [topic]",
  "build run of show template for [topic] in [location]", "tokenized ros
  [episode]", or "/pod-3A-ros-template". Phase 3 Run of Show of the podcast
  pipeline; hard dependency on a matching-scope n-gram table and entity map;
  feeds pod-3B-client-ros and pod-3C-client-guide downstream.
skill_kind: hybrid
modes: multi
inputs: [n-gram-table.json, entity-map.json, entity-clusters.md, keyword-research.json, podcast-overview.md, case-engine-branding]
outputs: [json, markdown, gdoc]
notify: []
metadata:
  version: 3.2.0
  date: 2026-07-31
  owner: Gabe Jordan
  version_history: >
    1.0 - co-work Drive-native version (2026-04-20). 2.0.0 - merged cowork
    ros-template canonical content with original local pod-7-ros-template Mode A
    enrichments (2026-05-14). 3.0.0 - renamed pod-7-ros-template ->
    pod-3A-ros-template; full structural refactor to the canonical CE skill
    structure; probe apparatus and Mode A/B branching stripped (2026-05-20).
    3.1.0 - added Episode 1 / Founder Story hardcoded exception: skip the
    research pipeline; the ROS template is the fixed pre-built Founder Story
    master template at templates [master]/AEO Templates/Podcast/Episode
    Templates/Founder Story/ (2026-06-08). 3.1.1 - three-field geo model
    alignment (Gabe directive 2026-07-10, Whalen scoping): stamped Targeting
    strategy / Optimization scope (show anchor) / Episode geo target with the
    "anchor scope != per-episode target" rule; schema bumped 1.0 -> 1.0.1.
---

# ROS Template

> **Drive write governance:** All Drive operations (create, update, rename, move) follow [Ship]. Revise in place via `files.update` against the existing fileId, never delete-and-reupload (breaks the fileId/URL chain and silently kills every downstream reference).

### What is

A tokenized, generic Case Engine podcast Run of Show (ROS) template for a specific episode (and optionally a location). The template uses `{{PLACEHOLDERS}}` everywhere client-specific data will eventually go - firm, attorney, phone, website - so one template is reusable across every firm that records that episode at that scope. The N-Gram Table (`pod-2B-n-gram-table`) is the content backbone; this skill turns those questions into a script with segment structure, producer notes, speaker tags, and the Appendix. Because the template is generic and reusable across every firm, it lands in the shared template library at every scope - `Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/` per Map 2 - and NEVER in a client/firm episode folder. Downstream, `pod-3B-client-ros` populates the placeholders for a specific firm and writes the firm-specific Client ROS into the client episode folder.

**The ROS Template is INTERNAL - the client never sees it.** That is exactly why it carries the ENTIRE n-gram question set, not just the questions that reach the host script. The selected ~20 questions live in the main run-of-show body, renumbered sequential Q1..N. EVERY remaining (non-selected) n-gram question lives below the run of show in the `## Additional Questions (Optional Pull)` section, renumbered 1..M - this is an internal reserve pool. If the n-gram bank has 30 questions and 20 are selected, the other 10 sit in Additional Questions so that when a client rejects one of the main 20 at review, a vetted replacement can be swapped straight from the reserve without a fresh research pull. The client-facing trim happens downstream at `pod-3B-client-ros`, which ships ONLY the main selected set and NEVER the Additional Questions section.

### Workflow

ROS Template is the first step of **Phase 3 (Run of Show)** of the podcast pipeline. Per-episode, per-scope - a different template for Topic Only, each Location, and each Extension. Hard dependency on a matching-scope N-Gram Table (`pod-2B-n-gram-table`) and a matching-scope entity map (`pod-1A-entity-research`).

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
        │
PHASE 3: RUN OF SHOW  (per prioritized episode)
┌─ 3A ──────────┐ ┌─ 3B ──────────┐ ┌─ 3C ──────────┐
│ ROS Template  │ │ Client ROS    │ │ Client Guide  │
│               │ │               │ │               │
└───────────────┘ └───────────────┘ └───────────────┘
  ◄── YOU ARE HERE
```

Notes:

- **Phase 1 Research** - `pod-1A-entity-research`, `pod-1B-keyword-research`, and `pod-1C-virality-research` run together as one research pass, ONCE per practice area + location cascade.
- **Phase 2 Planning** - `pod-2A-topic-planner` ranks episodes from the research; `pod-2B-n-gram-table` builds the 4-column collation table for one episode at one scope. Both are upstream of this skill.
- **Phase 3 Run of Show** - `pod-3A-ros-template` (this skill) builds the tokenized template; `pod-3B-client-ros` populates it for a firm; `pod-3C-client-guide` derives the attorney guide. Phase 3 steps are sequential - each depends on the prior one.

Prerequisites: a matching-scope N-Gram Table from `/pod-2B-n-gram-table` and a matching-scope entity map from `/pod-1A-entity-research` are hard dependencies - this skill will not run without both.

> **Episode 1 - Founder Story is a HARDCODED exception. Do NOT run this skill's research pipeline for it.** Episode 1 of every client's show is the **Founder Story** interview (the founder / origin-story episode, formerly the "YOU Interview"). It is the ONE episode that does not flow through the n-gram / entity-map / topic-scope generation above. A single pre-built, tokenized ROS template is the fixed source of truth and already exists at `templates [master]/AEO Templates/Podcast/Episode Templates/Founder Story/` (Doc: `Run of Show // Founder Story (Episode 1) [TEMPLATE]`). For Episode 1 there is nothing to generate here - skip the N-Gram Table and entity-map hard dependencies entirely and do not build a new template. The per-client Founder Story Client ROS and Client Guide are produced by `pod-3B-client-ros` and `pod-3C-client-guide` by duplicating the Founder Story templates and populating tokens (from the template, not from research). The Founder Story template's internal shape is intentionally different from the standard ROS - Host script -> Follow-ups -> Mandatory Info Capture -> Host Notes, no entity-woven attorney bullets - leave that structure intact.

### Trigger phrases

- `/pod-3A-ros-template`
- "ros template for [episode]"
- "create ros template for [topic]"
- "build run of show template for [topic] in [location]"
- "ros for [episode] in [location]"
- "tokenized ros [episode]"

### Greeting

Hi, I'm ROS Template. Before I run, I need to confirm the podcast architecture. If podcast-overview has been run for this client, I'll read it and confirm in one line. If not, I'll ask:

1. **Client name.** Examples: "The May Firm", "Sutliff & Stout", "Conn Law Firm". Exact firm name as it appears in Drive. (Not needed at Topic Only scope - the base template has no firm.)

2. **Optimization scope (show anchor) - what the podcast as a whole is optimized to rank for.** This is the show-wide anchor, NOT the per-episode target (see `### Framing -> Geo model`). City / State / County / Regional:
   - **City-level:** people in your market search the city as a unit ("Houston car accident lawyer"). Show anchor: Houston.
   - **State-level:** people search the state as one unit ("California car accident lawyer"). Show anchor: California; each episode still targets its own city.
   - **County / regional-level:** people search the region ("Inland Empire injury attorney", "Harris County", "Bay Area"). Show anchor: the region/county; cities within become individual Episode geo targets.

3. **Extension locations (if any).** Extensions are sub-scope episodes - short derivatives (10-12 questions, ~30-35 minutes). Under the legacy anchor model they inherit from the anchor and surface what's different at the smaller scope. Under a multi-location targeting strategy they ARE the episode - client-facing term "Mini episode", no anchor/primary exists, one Mini per target city:
   - Houston city anchor -> Sugar Land, Katy, Pasadena suburb extensions
   - California state anchor -> Bakersfield, Fresno, Long Beach city extensions
   - Inland Empire regional anchor -> Ontario, Riverside, San Bernardino city extensions
   - List the extensions if any; "none" if the firm only targets the anchor.

4. **This run's scope** - Topic Only, an anchor location, or a specific extension? At Location/Extension scope, the location I resolve is this episode's **Episode geo target** - the specific city this episode is built to rank for - which may differ from the show-wide Optimization scope (show anchor) above.

5. **Episode format** - resolved by the client's targeting strategy (recorded in the podcast overview; ask if absent): single-location -> Full episode (~50-55 min, ~20 questions); multi-location -> Mini episode per target city (~30-35 min, 10-12 questions hard cap, internal scope label stays `Extension`, no anchor episode). Legacy anchor+extension remains valid for single-location clients with satellite markets.

6. **Episode goal** - what is this specific episode trying to accomplish? Authority / education, Lead generation, Differentiation, Narrative / story, or Conversion (see `### Editorial Guidelines -> Guideline 2`). If unspecified I default to Authority.

Then my skill-specific follow-ups:

7. **Scope folder (shared library, every scope):** does the scope folder exist under `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/`? If not, I create the chain. The tokenized template is generic and ALWAYS lives in the shared library - never in a client/firm episode folder, even at Location/Extension scope.
8. Does the matching-scope N-Gram Table exist (`/pod-2B-n-gram-table` output)?
9. Does the matching-scope entity map exist (`/pod-1A-entity-research` output)?
10. **N-Gram Table <-> Topic Plan reconciliation** - does the episode's N-Gram Table question set match the same episode's Episode Breakdown in the `pod-2A-topic-planner` Topic Plan? Both are read and compared; if a question was cut or added in one but not the other, flag the gap and reconcile before generating - never silently proceed with a mismatched set (see `### Inputs`).
11. If a ROS Template already exists for this episode + scope, archive and rebuild or refresh in place?

If anything's unclear I'll ask once in a single message. I won't touch Drive until you say go. You only need to know about `{Firm} Podcast/` - I handle the foundation lookups and writes transparently.

---

## Best Practices

The WHAT contract. Every other section references these by name; the SOP never restates them.

### Inputs

What is?
The materials this skill ingests - a matching-scope N-Gram Table and entity map (both hard dependencies), the entity clusters file, an optional keyword-research seed set, the podcast architecture doc, and the Case Engine Branding folder - all resolved before any template is generated.

#### Required

- **Matching-scope N-Gram Table** (`n-gram-table.json`) - the 4-column collation table from `/pod-2B-n-gram-table`. The Question Text column is the content backbone of the script. No silent fallback - if missing, the skill stops and routes to `/pod-2B-n-gram-table`.
- **The `pod-2A-topic-planner` Topic Plan for this episode** - **CANONICAL SOURCE = the PUBLISHED Google Doc Topic Plan in the client Topic Plan slot** (the client sees that Doc and edits it manually, so it is authoritative for the episode lineup and each episode's topic/title). NEVER take the episode or its topic from a local `topic-plan-v{n}.json`/`.md` or any old/cached file - those are stale mirrors that drift. Confirm the episode's topic/title against the live Doc before building; the Doc wins on any conflict; never build a topic absent from the Doc's lineup (Eberst E5 slip-and-fall wrong-episode incident, 2026-06-19). The Topic Plan is also read as a CROSS-CHECK on the question set. The episode's question set must be the same in the N-Gram Table and the Topic Plan. The skill compares the two and reconciles before generating: if a question was cut or added in one and not the other, that is a gap - flag it, do not silently proceed. The N-Gram Table is the canonical question bank; if the Topic Plan reflects a later edit (a cut or an add) the N-Gram Table is updated to match so every downstream artifact stays consistent. Goal: zero drift between the questions the client reviewed in the Topic Plan and the questions that reach the Run of Show.
- **Matching-scope entity map** (`entity-map.json`) - the localized entity set from `/pod-1A-entity-research`. Powers the Appendix Entity Architecture + Entity Checklist and every underlined entity in the script. No silent fallback - if missing, the skill stops and routes to `/pod-1A-entity-research`.
- **Episode title** - the episode this template is built for.
- **Topic** - practice area (e.g., Personal Injury, Criminal Defense, Family Law).
- **Scope** - one of: Topic Only, Location, Extension.
- **Firm name** - used only to resolve podcast architecture / Greeting auto-fill when a firm is named; the template body stays tokenized and the destination is always the shared template library. Not needed at Topic Only scope.
- **Location** - required when scope is Location or Extension. Format: `CA`, `CA - Los Angeles County`, `CA - Long Beach`. No colons; dashes only.

#### Optional

- **`entity-clusters.md`** - the clusters sibling of the entity map, same source folder. Drives the Appendix Entity Architecture; the skill proceeds without it.
- **`keyword-research.json`** - the keyword-research seed set from `/pod-1B-keyword-research`. When present, the Appendix Search Queries & Volume section is sourced from it; otherwise inferred from the n-gram table. If found but undeclared in the handoff contract, the skill stops and asks rather than guessing silently.
- **Episode duration target** - default 20-25 min for Topic Only/Location, ~30-35 min for Extension/Mini.
- **Segment count** - default 4 segments (S1-S4). Extensions/Minis collapse to 3.
- **Episode goal** - Authority / Lead gen / Differentiation / Narrative / Conversion. Default Authority.
- **Refresh flag** - default refresh in place (routes to `## Update`). Pass `archive-and-rebuild` to force a full rebuild with the prior ROS Template archived to `_archive-{YYYY-MM-DD}/`.

#### Auto-read (no action required)

- **`podcast-overview.md`** - architecture source of truth (anchor scope, extension cities, client name). If present at `{Firm} Podcast/.podcast-overview/podcast-overview.md`, the skill auto-fills Greeting questions 1-3; otherwise it asks.
- **Case Engine Branding folder** - the canonical brand reference at [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) (folder id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`). The `## Ship` build reads logo, colors, fonts, and the [Cover Page Spec](https://docs.google.com/document/d/1oydpI055jbj1FYDGeZfHQeMNjaWKUCFVGCRveeuJJCk/edit) for the branded Google Doc. Brand values resolve from the folder at build time - never inlined into this skill. A per-client `brand.json` typography block overrides the CE default (Roboto) when present.
- **Local ROS Template example references** - bundled `references/examples/ros-template-examples.md` as the quality-anchor set. If missing or empty, fall back to the in-skill reference material in `## INTERNAL` - do not block.

#### Capabilities

The skill runs locally in Claude Code and calls its tools directly - it assumes they exist and uses them in this priority order. On a tool error, it skips that source and degrades to the next; it never probes for availability first.

- **Local filesystem read** - for auto-detected upstream artifacts at the canonical Desktop path `~/Desktop/claude_code/deliverables/podcast/...`. Fastest path; no Drive round-trip.
- **`gws drive`** (or `mcp__claude_ai_Google_Drive__*` connector) - for the matching-scope N-Gram Table, entity map, clusters file, optional keyword research, and the Case Engine Branding folder from the shared Drive.
- **`mcp__ce-services__rag_query`** (`rag_name: koray`) - for SEO / methodology grounding when calibrating segment pacing and attorney-bullet shape; a sanity check, never a content source.
- **User-supplied materials** in the greeting (pasted artifacts, dropped files) and user interview for hard requirements still missing - the always-available floor.
- **Hard requirement** - the matching-scope N-Gram Table and entity map must both resolve via local read or Drive. If either is missing, the skill stops and routes to the upstream skill.
- **Behavior on a tool error** - skip that source and degrade to the next. With no reachable source, fall through to user-supplied + interview; flag every Inferred value with `> NEEDS CONFIRMATION:` per Sourcing discipline.

### Outputs

What is?
The artifacts this skill ships - the 3-format trio (a machine-readable JSON payload, a markdown source-of-truth, and a CE-branded Google Doc) plus a `metadata.json` provenance file - landing in the shared template library under `Episode Templates/{Topic}/{scope}/` per Map 2 at EVERY scope (Topic Only, Location, Extension), mirrored to the local Desktop path. The tokenized template is generic/reusable, so it lives ONLY in the shared library - never in a client/firm episode folder.

#### Output formats

CE-wide default: every persistent artifact ships in three formats.

- **JSON** - `ros-template-data.json` - structured / machine-readable payload, the input the build script renders from and the one `pod-3B-client-ros` populates. Validates against `references/schema/ros-template.json`. Downstream consumers (`pod-3B-client-ros`) read this for the placeholder inventory, segments, questions, duration target, and scope.
- **Markdown** - the ROS Template `.md` - local source-of-truth mirror, the downstream-readable raw source uploaded to Drive as `text/markdown` (no conversion). Retains the `## INTERNAL` block. Tokenized; `{{PLACEHOLDERS}}` preserved verbatim for Client ROS to populate.
- **Google Doc** - the human-facing CE-branded ROS Template Doc. Built from a CE-branded `.docx` (cover page, logo, Roboto body, real underlined entity runs, "Prepared by Case Engine" footer) emitted by `scripts/build-ros-template-docx.py`, then uploaded with `mimeType: application/vnd.google-apps.document` so Drive auto-converts the DOCX to a clean Google Doc. Created / updated in-place via `files.update` against a stable fileId so the URL never breaks for downstream links.

A `metadata.json` provenance file ships alongside the trio (internal-only, not a client-facing artifact - records sources, counts, scope, localization scan result, episode goal).

#### What ships

- **ROS Template `.md`** - Markdown - raw tokenized source, downstream-readable, retains the `## INTERNAL` block.
- **ROS Template** - Google Doc - human-facing CE-branded view, cover page, Roboto typeface, real underlined entity runs, stable fileId.
- **`ros-template-data.json`** - JSON - machine-readable payload, downstream-consumed by `pod-3B-client-ros`; validates against `references/schema/ros-template.json`.
- **`metadata.json`** - JSON (internal) - provenance: sources, question / segment / placeholder counts, scope, episode goal, localization scan result, references status.

#### Drive destination

Shared drive root: `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`).

| Scope | Destination | Why |
|---|---|---|
| Topic Only | `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/Topic Only/` (per [Templates [Master] Structure](https://docs.google.com/document/d/1ciUUzUNG4M6HtgnSBsyq53C79aeZF6PbOa2CVuWHjiQ/edit) → Map 2) | The tokenized template is GENERIC and reusable across every firm, so it lives ONLY in the shared template library, never in a client folder. Topic Only is the base template that Location/Extension templates are derived from. |
| Location (anchor) | `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/Locations/{Location}/` (per [Templates [Master] Structure](https://docs.google.com/document/d/1ciUUzUNG4M6HtgnSBsyq53C79aeZF6PbOa2CVuWHjiQ/edit) → Map 2) | The tokenized template is GENERIC and reusable across every firm recording at this scope, so it lives ONLY in the shared template library, never in a client/firm episode folder. The firm-specific Client ROS (the populated host script) is the only ROS artifact that lands in the client episode folder - produced downstream by pod-3B-client-ros. |
| Extension | `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/Extensions/{Location}/` (per [Templates [Master] Structure](https://docs.google.com/document/d/1ciUUzUNG4M6HtgnSBsyq53C79aeZF6PbOa2CVuWHjiQ/edit) → Map 2) | The tokenized template is GENERIC and reusable across every firm recording this extension at this scope, so it lives ONLY in the shared template library, never in a client/firm episode folder. Each extension's localized `{Location}` is its own subfolder under `Extensions/`. |

```
templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/
  E{N}: {Episode Title} // ROS Template - {Location}.md                     raw markdown source (text/markdown)
  E{N}: {Episode Title} // ROS Template - {Location}                        branded Google Doc (in-place files.update)
  ros-template-data.json                                                    machine-readable payload, downstream-consumed
  metadata.json                                                             sources, counts, scope, episode goal, localization scan
  _archive-{YYYY-MM-DD}/                                                    (only the prior ROS Template file, if one existed)
```

At Topic Only scope the trio is named plainly - `ROS Template.md`, `ROS Template`, `ros-template-data.json` - and the ` - {Location}` suffix is dropped. The tokenized template carries NO firm name (it is generic), so the filename has no `{Firm Name}` token. The Drive destination is fixed - this skill does not move existing Drive data, and it NEVER writes the tokenized template into a client/firm episode folder; the only ROS artifact that lands there is the populated Client ROS, produced downstream by `pod-3B-client-ros`.

**Legacy compatibility:** MVP Accident Attorneys and any other client with pre-2026-05-15 episodes may have a tokenized template still sitting in an old `EP{N}/01 Strategy/` or `Template ROS:` slot inside a client episode folder. Do not auto-migrate those, but the canonical destination for any NEW or refreshed template is the shared template library only (Map 2) - never a client/firm episode folder.

#### Local mirror

`~/Desktop/claude_code/deliverables/podcast/ROS Templates/{Topic}/{Episode}/{scope}/` - holds the same ROS Template `.md`, the CE-branded `.docx`, `ros-template-data.json`, and `metadata.json`. `{scope}` = `Topic Only`, `Locations/{Location}`, or `Extensions/{Location}` to mirror the Drive scope convention. The mirror keeps the DOCX (not the auto-converted Google Doc, which only exists in Drive). It enables fast local iteration, downstream local-skill consumption (`pod-3B-client-ros` reads from here when running locally), and offline review. Written on every run.

#### Schema

`references/schema/ros-template.json` - the canonical JSON schema `ros-template-data.json` validates against. The schema enforces the placeholder inventory (which of the 12 approved placeholders are used), segments, questions, duration target, episode goal, and scope. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed - do not block on a missing schema.

#### Sections INCLUDED in the client-facing Google Doc

- Branded cover page (CE logo, "Run of Show" title, practice-area subtitle, "Prepared by Case Engine" footer)
- Compact metadata line (Episode + duration + recording date; attorney / firm / location / website placeholders)
- Producer Notes (brief)
- Introduction
- Segments S1-S4 with questions, speaker tags, attorney response scaffolding, entity underlines
- Closing and Call to Action
- Appendix: Producer Notes (extended), Entity Architecture, Entity Checklist, Search Queries & Volume

#### Sections EXCLUDED (never in the client-facing artifact)

- `## Quality Assurance` and everything from that heading onward
- Known Gaps, Handoff Contract, Next Steps, provenance block
- The internal Formatting Guide rulebook (it governs the renderer; it is never a deliverable section)

The Google Doc renderer truncates the markdown source at the first `## Quality Assurance` heading and discards everything after - this keeps internal-process content out of client-facing deliverables while the same markdown serves as the internal source of truth. See `## INTERNAL` for the grep test.

#### Capabilities

Both write destinations are written every run. On a write error to one, the skill ships to the other and surfaces the partial state in the report - it does not silently lose the deliverable.

- **Drive** - `gws drive` (or `mcp__claude_ai_Google_Drive__*` connector) - writes the markdown, the branded Google Doc, the JSON, and metadata into the shared template library scope folder (`Episode Templates/{Topic}/{scope}/`, Map 2) at every scope. Never a client/firm episode folder.
- **Local mirror** - local filesystem write to the local mirror path, alongside the Drive write.
- **Behavior on a write error** - if one destination errors, ship to the other and report the partial state. If both error, hard-fail with a clear message; do not silently lose the deliverable.

#### Examples

`references/examples/ros-template-examples.md` - single doc with GOOD / BAD / EDGE CASE labeled sections per CE convention. Read 1-2 examples matching the requested scope as calibration before generating. If the folder is empty, proceed on the in-skill reference material in `## INTERNAL` and flag `"references": "empty"` in `metadata.json`.

#### Routing

- **Upstream (required, hard dependency):** `/pod-2B-n-gram-table` - the matching-scope N-Gram Table; `/pod-1A-entity-research` - the matching-scope entity map.
- **Downstream (required):** `/pod-3B-client-ros` populates the placeholders for a specific firm, which in turn feeds `/pod-3C-client-guide`.
- **Refresh:** re-run with the same episode + scope (routes to `## Update`).

#### Handoff Contract

This skill produces the following for downstream consumers:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| ROS Template `.md` + branded Google Doc | `/pod-3B-client-ros` | Full tokenized script structure; `{{PLACEHOLDER}}` locations; bold / italic / `[entity]{.underline}` formatting to preserve; Appendix (Producer Notes, Entity Architecture, Entity Checklist, Search Queries) |
| `ros-template-data.json` | `/pod-3B-client-ros` | Placeholder inventory (which of the 12 approved placeholders are used), segments, questions, duration target, episode goal, scope - the structured payload Client ROS populates |
| `metadata.json` | (not consumed downstream) | Internal provenance - sources, duration target, segment count, scope, episode goal, localization flag, references status |

Downstream consumers can rely on: the Google Doc URL is stable for the lifetime of the template (preserved via `files.update` across re-runs); `ros-template-data.json` validates against `references/schema/ros-template.json`; only the 12 approved placeholders appear in the template body. Upstream pulls (hard dependency): `n-gram-table.json` from `/pod-2B-n-gram-table` and `entity-map.json` + `entity-clusters.md` from `/pod-1A-entity-research`. The skill refuses to run without both.

### Framing

The ROS Template is the GENERIC reusable script, not a finished client deliverable. Client-specific populating happens at `pod-3B-client-ros`. Everything specific to a firm becomes a `{{PLACEHOLDER}}` - no hard-coded firm names, attorney names, or client-specific language ever appears in the template body. Because it is generic and reusable, the template lives ONLY in the shared template library and never in a client/firm episode folder. It is never a populated host script and never a substitute for the N-Gram Table that feeds it.

**Geo model (three fields, use these exact names).** Every podcast carries three distinct geo fields; this skill's location/scope handling maps to them:

1. **Targeting strategy** - `single-location` vs `multi-location`. Does the firm serve/rank one city or several? Drives episode format (Greeting Q5): single-location -> Full episodes (~20 questions, ~50-55 min); multi-location -> one Mini episode per target city (10-12 questions, ~30-35 min), no single primary episode.
2. **Optimization scope (show anchor)** - City / State / County / Regional. What the podcast *as a whole* is optimized to rank for (Greeting Q2). A multi-location firm usually anchors at State or Regional; a single-location firm anchors at City.
3. **Episode geo target** - the specific city THIS episode is built to rank for. It is what the location/city token in a Location/Extension template resolves to. In multi-location the show anchors broad (e.g. the state) while each episode targets a different city; in single-location every episode shares the one anchor city.

**The rule: anchor scope != per-episode target.** The show can be optimized for a broad scope (e.g. the whole state) while each episode targets a specific city we're trying to rank for. Research runs at the anchor breadth; each episode's questions/titles emphasize that episode's Episode geo target city naturally - a ceiling, never a forced quota (see `### Editorial Guidelines -> Guideline 3` and the no-city-quota / natural-tonality principle). Any location/city `{{PLACEHOLDER}}` in this template resolves to the Episode geo target, NOT the show anchor. Getting this wrong is how a multi-location statewide firm ends up with episodes that all sound like one city, or how city emphasis silently becomes a city floor.

### Quality bar

What "good" looks like - the pass / fail intuition.

- Only the 12 approved placeholders appear; a grep for `{{...}}` outside the taxonomy returns zero (see `### Editorial Guidelines -> Guideline 1`).
- Every question is sourced verbatim from the matching-scope N-Gram Table Question Text column - no invented questions.
- Document structure matches `### Editorial Guidelines -> Guideline 4` every time - downstream Client ROS relies on the exact shape.
- Main-body `### Q{N}:` count is 20 or fewer (Full episode) or 10-12 (Extension/Mini). The template (INTERNAL only) carries ALL n-gram questions: the selected set in the main body, and EVERY non-selected n-gram question - not just overflow beyond a 20 cap - in the `## Additional Questions (Optional Pull)` section below the run of show, renumbered 1..M. That section is the internal reserve a rejected main question gets swapped from; it never reaches the client.
- Speaker tags are italic, never bold, never code blocks. Bold marks mandatory verbatim phrases + every placeholder. Entities are pandoc `[entity]{.underline}` runs.
- When scope is Location or Extension, every entity is localized - generic unqualified categories are a hard fail (see `### Quality gates` -> localization scan).
- The human-facing Google Doc is the CE-branded DOCX→Doc, never a raw-markdown→Doc upload.
- No em dashes, no banned vocabulary - the Anti-AI Detection scan fires before publish.

### Sourcing discipline

The Confirmed / Inferred / Unknown three-state pattern. Never block, always ship, never silent. The template still ships when data is incomplete; gaps surface in `## INTERNAL` or with `> NEEDS VERIFICATION:` blocks.

- **Confirmed** - claim traces to a specific source. Every question pulled from the N-Gram Table and every entity pulled from the entity map is Confirmed. Ship as-is, no marker.
- **Inferred** - sensible default applied when a source is insufficient (e.g., a segment ordering chosen because the entity clusters file was absent, or an episode goal defaulted to Authority). Ships with `> INFERRED: {what + why}` flag.
- **Unknown / NEEDS CONFIRMATION** - no source AND no defensible default. Ships with `> NEEDS CONFIRMATION: {what's missing}` block, never silently synthesized. An entity that belongs but is not in the map is NEEDS CONFIRMATION - refresh the entity map, never invent it here.

### Editorial Guidelines

Cross-cutting content rules for the template. The SOP points back here; the rules live here once.

**Guideline 1 - Only the 12 approved placeholders, never invented tokens.**

- **Approved taxonomy** (must match `pod-3B-client-ros` exactly - this is the taxonomy Client ROS consumes at populate time):

  | Placeholder | Source at populate time |
  |---|---|
  | `{{FIRM_NAME}}` | Full firm name |
  | `{{ATTORNEY_NAME}}` | Full attorney name |
  | `{{ATTORNEY_FIRST_NAME}}` | First name only |
  | `{{CITY}}` | The **Episode geo target** city - the specific city this episode is built to rank for (from Location at Location/Extension scope). May differ from the show-wide Optimization scope (show anchor); see `### Framing -> Geo model`. |
  | `{{STATE}}` | State full name (`CA` -> `California`) |
  | `{{PHONE_NUMBER}}` | Firm phone `(XXX) XXX-XXXX` |
  | `{{WEBSITE}}` | Firm website (include `https://`) |
  | `{{PRACTICE_AREA}}` | Topic lowercase plural |
  | `{{EPISODE_NUMBER}}` | Integer N from `E{N}` |
  | `{{RECORDING_DATE}}` | `MM-DD-YYYY` |
  | `{{PODCAST_NAME}}` | Client's podcast name |
  | `{{HOST_NAME}}` | CE host on the recording (was `{{CO_HOST_NAME}}` - renamed; breaks populate if you use the old name) |

- **Banned:** any `{{TOKEN}}` outside the 12 above; any hard-coded firm / attorney / city / state name in the template body.
- **Why:** Client ROS scans for every `{{...}}` at populate time; an invented token never gets resolved and ships into the recording as literal markup. Hard-coded firm content corrupts the reusability the tokenized template exists for.
- **Where it fires in the SOP:** `## Create -> ### Generate the ROS body`, and the placeholder gate in `### Quality gates`.

**Guideline 2 - Research is the palette; ROS layers in the slice that serves THIS episode's goal.**

- Research outputs capture the FULL topic domain - all keywords, all entities across clusters, all virality candidates. The ROS Template does NOT mechanically consume everything upstream produced; it layers in the slice that serves this episode's goal.
- **Goal types and the selection rule the renderer applies:**
  - **Authority / education** - full statute + agency + insurance entity density. Virality boost ignored; topic + dedup dominate.
  - **Lead generation** - attorney-credential entities (Board Certification, AAJ, trial experience) appear earlier (S1 Producer Notes + S4 close). Closing CTA carries 2x bold emphasis on phone + website.
  - **Differentiation** - pull High-tier virality candidates into S3/S4; weave verdict numbers + named local venues.
  - **Narrative / story** - organize segments around case chronology, not topic taxonomy. Attorney bullets are chronological beats.
  - **Conversion** - consultation + fee-structure language in every segment wrap; closing is 90% CTA.
- **Why:** a single Research run serves many episodes in a series; Episode 2 (procedural) layers in different signals than Episode 7 (narrative) from the same entity map.
- **Where it fires in the SOP:** `## Create -> ### Organize questions into segments` and `### Generate the ROS body`. The goal is recorded in `metadata.json -> episode_goal` so downstream consumers honor the same framing.

**Guideline 3 - Localized entities only when scope is Location/Extension.**

- **Banned:** generic, unqualified entity categories when scope is Location or Extension - `Police Department`, `Sheriff's Office`, `Insurance Company`, `Civil Court`, `District Court`, `Superior Court` (unqualified), `Hospital` (unqualified), `Department of Motor Vehicles`, `Department of Transportation`, `Highway Patrol` (unqualified).
- **Allowed:** the localized instance from the entity map at matching scope - `Houston Police Department (HPD)`, `Harris County Civil Courts`, `Memorial Hermann Hospital System`, `Texas Department of Insurance (TDI)`. Generic categories are acceptable ONLY when scope is Topic Only.
- **Why:** the entity map was already localized at Research Step 1A. A generic category in a localized script is a localization leak - it erases the jurisdictional authority signal the episode is built on. At Location/Extension scope the script must reference at least 5-7 named local entities from the matching-scope entity map.
- **Where it fires in the SOP:** `## Create -> ### Run the localization scan`, and the localization scan in `### Quality gates`.

**Guideline 4 - Locked document structure and formatting conventions.**

- **Document shape** (downstream Client ROS relies on it exactly): title H1; metadata block (Practice Area / Episode / Duration / Recording Date / Template Version / Location); Producer Notes; Introduction (~2 min); Segments S1-S4 each with `### Q{N}:` headings; Closing and Call to Action; the `## Additional Questions (Optional Pull)` section (INTERNAL reserve - see below); `# Appendix: Production Reference` with Producer Notes (extended), Entity Architecture, Entity Checklist, Search Queries & Volume.
- **`## Additional Questions (Optional Pull)` carries the FULL reserve, not just overflow.** Because this template is internal (never client-facing), it holds the ENTIRE n-gram question set. The selected ~20 questions are in the main body; EVERY remaining non-selected n-gram question - not merely overflow beyond a 20 cap - lives in this section below the run of show, renumbered 1..M, each as a list entry of its question text (full attorney-response blocks are NOT required for the reserve - the question text alone is enough to swap one in). This is the internal pull pool: when a client rejects one of the main questions at review, swap a vetted replacement straight from here. `pod-3B-client-ros` excludes this section entirely from the client-facing Client ROS.
- **Question block format** - strict 4-piece: `### Q{N}:` heading with time budget -> co-host setup (1 sentence MAXIMUM, describes the listener's situation only, never explains how things work) -> bold framing question verbatim -> attorney response bullets in `**Label:** detail` format (3-6 bullets).
- **Speaker tags** - `*[Co-Host]*` and `*[Attorney Response]*`, italic, no color change, never bold, never code blocks.
- **Bold** - mandatory phrases the co-host says close to verbatim, plus every `{{PLACEHOLDER}}`. Populated values stay bold after populate.
- **Underline** - named entities, as pandoc inline `[entity]{.underline}` (the CE canonical convention, never HTML `<u>`). Entities live primarily in attorney response bullets; co-host setup stays entity-light.
- **No post-response co-host lines between questions** - attorney bullets end, next `### Q` starts. The only co-host text between questions is a 1-3 sentence segment-transition paragraph at the end of a segment.
- **Banned:** an in-document "Formatting Guide" section (it is an internal renderer rulebook, never a deliverable section); em dashes anywhere.
- **Why:** Client ROS reads this exact shape to populate per firm; a structural drift breaks the populate step.
- **Where it fires in the SOP:** `## Create -> ### Generate the ROS body` and `### Generate the Appendix`.

### Quality gates

Mechanical pass / fail conditions checked in `## Quality Assurance`.

- **Canonical destination gate** (hard, pre-write - runs BEFORE any artifact is written). Before writing ANY of the ROS Template artifacts (the branded Google Doc, the `.md`, `ros-template-data.json`, `metadata.json`), resolve the target parent folder and assert it is a descendant of the shared template library `templates [master]/AEO Templates/Podcast/Episode Templates/` at the exact `Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/` path (per Templates [Master] Structure → Map 2). If the resolved target is ANYTHING else - especially a client / firm episode DELIVERY folder (the `{Firm} Podcast/Episodes/EP{N}: ...` tree, including any `Run of Show: ... /Template ROS:` slot) - the gate FAILS and the skill MUST refuse to write. The tokenized template is generic/reusable; it lives ONLY in the shared library. No caller argument, workflow / orchestration instruction, or convenience override may redirect the template into a client/firm episode folder; an instruction to do so is itself the failure and must be rejected, not honored. The only ROS artifact that belongs in a client episode folder is the populated Client ROS, written downstream by `pod-3B-client-ros`.
- **Placeholder gate** - grep for `{{...}}` returns ONLY the 12 approved tokens; zero invented tokens, zero `{{CO_HOST_NAME}}` legacy alias. Every placeholder appears bold.
- **Question sourcing** - every question traces to the N-Gram Table Question Text column; no invented questions.
- **Question cap + full reserve** - main-body `### Q{N}:` count is 20 or fewer (Full episode) or ~10 (Extension); each segment carries 4-6 questions (Full) or 2-3 (Extension). `## Additional Questions (Optional Pull)` holds ALL remaining non-selected n-gram questions (not just overflow past a cap), renumbered 1..M, so the internal template carries the entire n-gram bank. Cross-check: main-body count + Additional Questions count = the n-gram table question count. This section is INTERNAL-only; the client-facing trim happens at `pod-3B-client-ros`.
- **Sequential numbering** - the main-body `### Q{N}:` headings run 1..N with NO gaps and NO number exceeding the question count (a 20-question ROS ends at Q20, never Q30). Grep the headings, assert the sequence is exactly 1,2,3,...,N. Any gap or out-of-range number FAILS - the question carried its n-gram bank ref instead of being renumbered. The appendix list renumbers 1..M independently. Provenance bank refs live in `ros-template-data.json -> source_ngram_ref`, never in the heading.
- **Document structure** - matches `### Editorial Guidelines -> Guideline 4`. Closing segment contains `{{PHONE_NUMBER}}` and `{{WEBSITE}}`, both bold. Appendix carries all 4 subsections. No "Formatting Guide" section in the body.
- **Tokenization integrity** - zero hard-coded firm / attorney / city / state names in the body.
- **Localization scan** - automatic before write. Grep the script for the banned token list in Editorial Guideline 3. When scope is Location or Extension, any standalone hit FAILS the gate and that piece must be regenerated with the localized instance. At least 5-7 named local entities present. No state-specific forms leak across jurisdictions (CR-2 Texas only, SR-1 California only, DR 2489 Colorado only). PASS when scope is Topic Only by definition.
- **Branded render** - the Google Doc was built from `build-ros-template-docx.py` (cover page, logo, Roboto body, footer). Zero leaked pandoc inline-attribute markup as visible text (`[...]{.underline}`, `<u>`, `{.underline}`, `{.smallcaps}`, `{.mark}`).
- **Schema validate** - `ros-template-data.json` validates against `references/schema/ros-template.json`.
- **Provenance present** - `metadata.json` carries the provenance block (see `## INTERNAL`).
- **Artifacts present** - markdown, JSON, metadata all written; branded Google Doc exists.
- **No em dashes** - plain hyphens only anywhere in the output.

### Gotchas

Failure modes that are warnings, not enforceable rules.

- **Don't proceed with a parent-scope N-Gram Table or entity map.** If a Location-level table is expected but only Topic Only exists, running with the mismatch is a silent localization leak. Stop and run `/pod-2B-n-gram-table` (or `/pod-1A-entity-research`) for the matching scope.
- **Don't invent entities.** If the script needs an entity that is not in the map, refresh the map - never add it here.
- **The Client ROS and Client Guide are NOT this skill's output.** `pod-3B-client-ros` and `pod-3C-client-guide` produce those into the client episode folder. This skill writes only the tokenized ROS Template into the shared template library scope folder (Map 2) - it never writes into, archives, or touches anything in a client/firm episode folder.
- **Branded output is mandatory.** Do NOT upload raw markdown as a Google Doc - Google's markdown import does not render pandoc `[entity]{.underline}` spans, so raw markup leaks into the rendered Doc. The pipeline is `markdown → build-ros-template-docx.py → DOCX → Drive upload as gdoc mimeType → clean branded Google Doc`. The `.md` sibling is uploaded as `text/markdown` with no conversion.
- **Extension overlap with the parent is BY DESIGN.** Extensions reinforce anchor content at the smaller-market level. Select the 10 strongest questions from the parent anchor ROS Template and re-angle them - do not generate 10 new questions from scratch.

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
The pre-flight phase - reads the iteration log, orients to the right episode folder, verifies the upstream N-Gram Table and entity map exist, and decides whether this run creates a new template or updates an existing one.

### Orient

What is?
The orientation step - read the iteration log, resolve the correct destination folder, and load the podcast architecture context before producing anything.

- **Read the iteration log.** Read `references/iteration-log.json`, filter to entries with `status: open` or `status: in-progress`, surface them to the agent as known issues to watch for this run.
- If `podcast-overview.md` is reachable at `{Firm} Podcast/.podcast-overview/podcast-overview.md`, read it and auto-fill Greeting questions 1-3 (anchor scope, extension cities, client name); confirm in one line. Otherwise ask the Greeting questions.
- Resolve the destination folder - ALWAYS the shared template library per Map 2: `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/`. The tokenized template is generic; it NEVER goes into a client/firm episode folder at any scope. If the chain does not exist, create it. The Canonical destination gate (`### Quality gates`) hard-asserts this before any write.
- Read `references/examples/ros-template-examples.md` and pick 1-2 examples matching the requested scope as quality anchors. If the file is empty, proceed on the `## INTERNAL` reference material alone and flag `"references": "empty"` in `metadata.json`.

### Verify upstream dependencies

What is?
The hard-dependency gate - confirm the matching-scope N-Gram Table and entity map both exist before any template generation, and refuse to run on a parent-scope artifact.

- **Episode 1 / Founder Story exception (check FIRST):** if the requested episode is Episode 1 (the Founder Story interview), this skill does not generate anything - the ROS template is the pre-built hardcoded one at `templates [master]/AEO Templates/Podcast/Episode Templates/Founder Story/`. Skip the N-Gram Table and entity-map gates below and route the user to `/pod-3B-client-ros` to populate the firm's copy from that template.
- Resolve `n-gram-table.json` at the matching scope from `/pod-2B-n-gram-table`. If missing, STOP and route the user to `/pod-2B-n-gram-table`.
- Resolve `entity-map.json` + `entity-clusters.md` at the matching scope from `/pod-1A-entity-research`. If the map is missing, STOP and route the user to `/pod-1A-entity-research`. Do not substitute a parent-scope map (Gotchas - localization leak).
- **Handoff Contract check.** Verify upstream paths match the declared Inputs. If `keyword-research.json` or any other undeclared upstream file shows up and is under consideration, STOP and ask: "I see upstream output at {path} but my Inputs contract doesn't declare it as required. Should I (a) mine it for the Appendix, (b) skip it, or (c) pause while you update the handoff contract?" Do not guess silently.

### Existence check

What is?
The mode router - decide whether this run creates a new template or updates an existing one based on whether the resolved destination folder already has a ROS Template.

- Look for an `ROS Template` Google Doc + `ros-template-data.json` inside the resolved destination folder.
- **Missing:** no prior artifact - route to `## Create`.
- **Found:** surface provenance (existing `metadata.json` run date, question count) and ask: refresh in place / archive-and-rebuild / cancel.
  - Refresh in place -> route to `## Update`.
  - `archive-and-rebuild` (or the refresh flag passed at invocation) -> move ONLY the prior ROS Template file to `_archive-{YYYY-MM-DD}/` and route to `## Create`. Sibling Client ROS / Client Guide artifacts are left untouched.

## Prepare Inputs

What is?
The input-preparation phase - load and validate the N-Gram Table, entity map, clusters, optional keyword research, and branding into a working set ready for the Create or Update phase.

Work through the input sources in priority order; on a tool error, skip that source and degrade to the next.

- **Load the N-Gram Table.** Parse `n-gram-table.json` from the source resolved in Checks. The Question Text column is the question backbone for the script.
- **Load the entity map.** Parse `entity-map.json` - confirm it carries the localized entity set at the matching scope.
- **Load entity clusters.** Parse `entity-clusters.md` when present - the clusters seed the Appendix Entity Architecture.
- **Load keyword research (optional).** If the Handoff Contract check approved using `keyword-research.json`, parse it for the Appendix Search Queries & Volume section.
- **Resolve firm metadata (optional).** When a firm is named, read the optional `podcast-overview.md` for anchor scope, extension list, podcast name - to auto-fill the Greeting questions only; otherwise the Greeting asks. The tokenized body still uses `{{PLACEHOLDERS}}`.
- **Resolve branding.** Read the Case Engine Branding folder (id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`) - logo, colors, fonts, the Cover Page Spec. Hold the resolved values for the `## Ship` build. A per-client `brand.json` typography block overrides the CE default when present.
- **Load calibration examples.** Hold the 1-2 scope-matched examples from `references/examples/ros-template-examples.md` (or the `## INTERNAL` reference material) as quality anchors for the Create phase.

## Create

What is?
The create branch - builds the tokenized ROS Template from scratch when no prior template exists, producing a localized, schema-valid `ros-template-data.json` plus its markdown source and metadata.

**Best Practices.**
These apply to the entire create phase and should be checked after each step.

- Questions come from the matching-scope N-Gram Table only - never invent questions (see Sourcing discipline + `### Editorial Guidelines -> Guideline 4`).
- Only the 12 approved placeholders are used; never invent a token (Editorial Guideline 1).
- Hold the scope-matched calibration examples in view while generating - calibrate placeholder density, segment distribution, and entity underline coverage against them.
- Document structure, question phrasing, and formatting conventions follow `### Quality bar` and `### Editorial Guidelines` - do not restate the thresholds, apply them.

If the model generates output that violates any of these, emit a `> NEEDS VERIFICATION:` block at the offending location instead of shipping the claim.

### Organize questions into segments

What is?
The pass that sorts the N-Gram Table questions into the segment structure - broad -> procedural -> deep/expert across S1-S4, distributed by cognitive load and the episode goal.

- Read every question from the N-Gram Table Question Text column. Do not invent questions; do not reorder arbitrarily.
- Organize into segments with logical flow - S1 orient + establish authority (foundational / definitional); S2 process + procedural detail; S3 edge cases + nuance; S4 takeaways + resources. Extensions collapse to 2 segments (intro + punchline), or 3 if the question set justifies it.
- Distribute 20 or fewer questions across 4 segments for Topic Only/Location (4-6 per segment); ~10 across 2-3 for Extensions. The selected set is the main body, renumbered sequential Q1..N.
- **Every non-selected n-gram question goes to the reserve.** This template is internal (never client-facing), so it carries the ENTIRE n-gram set. After choosing the main ~20, route ALL remaining n-gram questions - not just the overflow past a 20 cap - into the `## Additional Questions (Optional Pull)` section below the run of show, renumbered 1..M as a list of question text (full attorney-response blocks not required for the reserve). This is the internal pull pool a rejected main question gets swapped from at client review. Cross-check before shipping: main-body count + Additional Questions count = the n-gram table question count.
- Apply the episode-goal selection rule per Editorial Guideline 2 - layer in the research slice that serves this episode's goal.
- **Extension scope:** select the 10 strongest questions from the parent anchor ROS Template and re-angle them for the extension's local context. Overlap with the parent is by design.

### Generate the ROS body

What is?
The pass that writes the script - metadata block, Producer Notes, Introduction, segments with the strict 4-piece question blocks, and the Closing CTA - tokenized with only the 12 approved placeholders and entities underlined.

- Render the document shape per Editorial Guideline 4 - title, metadata block, Producer Notes, Introduction, segments S1-S4, Closing and Call to Action.
- Each question block is the strict 4-piece format - `### Q{N}:` heading with time budget, 1-sentence co-host setup, bold framing question, 3-6 attorney response bullets in `**Label:** detail` format.
- **Sequential numbering (hard rule).** The `### Q{N}:` heading number is the question's position in the FINAL host script, renumbered **1..N in reading order across S1-S4** - NOT the N-Gram Table bank index. The n-gram table is a 25-35 question bank with stable Q-refs; the ROS keeps a ~20 subset, so its bank refs are gappy (Q1, Q2, Q12, Q14, Q30...). Those gaps must NOT reach the host script - a 20-question ROS is numbered Q1 through Q20, no holes, no number above the question count. Preserve the original bank ref as provenance ONLY: write it to `ros-template-data.json` as `source_ngram_ref` per question (so the Entity Checklist "Questions" column and downstream pod-4D clip mapping can still trace to the n-gram), never in the visible `### Q{N}:` heading. The `## Additional Questions (Optional Pull)` appendix likewise renumbers its own list 1..M. This is the single point where the kept question set AND its numbering are locked - pod-4B populates this template verbatim and must never re-select or renumber.
- Use ONLY the 12 approved placeholders (Editorial Guideline 1). Every placeholder appears bold. No hard-coded firm content.
- Underline every entity reference as pandoc `[entity]{.underline}`, pulled from the matching-scope entity map. Entities cluster in attorney response bullets; co-host setup stays entity-light.
- Speaker tags `*[Co-Host]*` / `*[Attorney Response]*` italic. No post-response co-host lines between questions - only a 1-3 sentence segment-transition paragraph at the end of each segment.
- The Closing and Call to Action contains `{{PHONE_NUMBER}}` and `{{WEBSITE}}`, both bold.
- Apply the episode-goal selection rule per Editorial Guideline 2.

### Generate the Appendix

What is?
The pass that builds the production-reference Appendix - Producer Notes (extended), Entity Architecture, Entity Checklist, and Search Queries & Volume - after the "End of Run of Show" marker.

- **Producer Notes (extended)** - jurisdiction deep-dive (statute citations by section, insurance minimums, county courts by formal name, tolling rules, government-notice deadlines), attorney bio hooks.
- **Entity Architecture** - pulled from `entity-clusters.md` when present.
- **Entity Checklist** - grouped local vs national, pulled from the entity map.
- **Search Queries & Volume** - pulled from `keyword-research.json` if approved for use; otherwise inferred from the N-Gram Table.
- **`## Additional Questions (Optional Pull)`** - render the full internal reserve here, below the run of show. Every non-selected n-gram question (not just overflow past the cap) as a list entry of its question text, renumbered 1..M, attorney-response blocks not required. Confirm main-body count + reserve count = the n-gram table count. INTERNAL-only - `pod-3B-client-ros` strips it from the client-facing Client ROS.
- Do NOT include a "Formatting Guide" section - that rulebook is internal to this skill, never a deliverable section.

### Run the localization scan

What is?
The gate that catches localization leaks - grep the script for generic unqualified entity tokens and regenerate any offending piece with the localized instance when scope is Location or Extension.

- Run the localization scan per `### Quality gates` - grep the script for the banned token list in Editorial Guideline 3.
- When scope is Location or Extension, any standalone hit fails the scan - regenerate that piece with the localized instance from the entity map. Confirm at least 5-7 named local entities are present.
- When scope is Topic Only, the scan passes by definition (generic categories are allowed).
- Record the localization scan result (PASS / FAIL + pieces regenerated) for `metadata.json`.

### Render markdown and payload

What is?
The pass that assembles the final artifacts - the ROS Template `.md` source-of-truth with the `## INTERNAL` block, the `ros-template-data.json` machine-readable payload, and `metadata.json`.

- Assemble the ROS Template `.md` in the locked Doc order per Editorial Guideline 4, with the tokenized body and the Appendix, then the `## INTERNAL` block (see `## INTERNAL`).
- Serialize `ros-template-data.json` per `### Outputs -> #### Schema` - the placeholder inventory, segments, questions, duration target, episode goal, scope.
- Write `metadata.json` with the provenance block per `## INTERNAL` - sources, question / segment / placeholder counts, scope, episode goal, localization scan result, references status.

## Update

What is?
The update path - modifies an existing ROS Template in place when a prior version exists, preserving any manual edits the producer made since the last skill run.

**Best Practices.**
These apply to the entire update phase and should be checked after each step.

- **Diff before write.** Pull the existing `ros-template-data.json` + ROS Template `.md`, compare against the proposed new state, surface every changed segment / question before committing the write.
- **Preserve manual edits.** Any question, attorney bullet, placeholder, or setup line that was manually edited since the last skill run keeps its current value. The skill never auto-overwrites a manual edit silently.
- **Flag merge conflicts inline.** When a new auto-generated value disagrees with a preserved manual edit, emit `> NEEDS VERIFICATION: auto-generated value [X] conflicts with manual edit [Y]` at the location; the producer resolves.
- **Stable fileId.** Update uses `files.update` against the existing `ROS Template` Google Doc fileId. Never create a new Doc; never delete-and-recreate. URL stability is part of the Update contract.

If the model proposes overwriting a manual edit without flagging it, halt and emit `> NEEDS VERIFICATION:` instead of shipping the change.

### Diff against existing

What is?
The pass that loads the prior template and computes a segment-level and question-level diff against the proposed new state so nothing changes silently.

- Read the prior `ros-template-data.json`, ROS Template `.md`, and `metadata.json` from the resolved destination folder.
- Read the prior `metadata.json` provenance block to recover the last run's upstream sources, question count, segment count, and episode goal.
- Run the Create-phase passes (`### Organize questions into segments` through `### Run the localization scan`) to compute the proposed new state.
- Compute the diff: questions added, questions removed, questions changed (per block), segments restructured, and pieces untouched.

### Merge and resolve conflicts

What is?
The pass that merges the new content into the existing template - new questions in, stale questions out, manual edits preserved, conflicts flagged for the producer.

- Apply the phase-level Best Practices: preserve every manually-edited piece; merge new auto-generated questions; drop questions the new question set retired.
- Where a new auto-generated value disagrees with a preserved manual edit, emit the `> NEEDS VERIFICATION:` conflict block inline; do not auto-resolve.
- Re-render the ROS Template `.md`, `ros-template-data.json`, and `metadata.json` per `### Render markdown and payload`. Bump the `metadata.json` run date and append the run to the provenance history.
- The shared `## Quality Assurance` phase runs after this phase - QA does not re-run inside Update.

## Quality Assurance

What is?
The gate before `## Ship` - a three-tier check (Best Practices by name, the hardwired Anti-AI Detection two-pass scan, then skill-specific mechanical checks) that runs after whichever branch fired (`## Create` or `## Update`).

**First - check against Best Practices.** The deliverable must align with the contract defined upstream in this file. This is always the first gate; skill-specific checks come after.

- **Quality bar** (Best Practices -> Quality bar) - 12 placeholders only, every question sourced from the N-Gram Table, locked document structure, question cap honored, branded Google Doc, no em dashes / banned vocabulary.
- **Sourcing discipline** (Best Practices -> Sourcing discipline) - every question Confirmed against the N-Gram Table, every entity Confirmed against the entity map; any Inferred ordering or default flagged `> INFERRED:`; any belongs-but-missing entity flagged `> NEEDS CONFIRMATION:`. No silent synthesis.
- **Editorial Guidelines** (Best Practices -> Editorial Guidelines) - Guideline 1 (12 approved placeholders, no invented tokens), Guideline 2 (episode-goal research slice), Guideline 3 (localized entities at Location/Extension scope), Guideline 4 (locked document structure + formatting conventions).
- **Quality gates** (Best Practices -> Quality gates) - full checklist must pass: placeholder gate, question sourcing, question cap, document structure, tokenization integrity, localization scan, branded render, schema validate, provenance present, artifacts present, no em dashes.

**Second - Anti-AI Detection two-pass scan** (canonical doc: https://docs.google.com/document/d/1hp7bxOFRlMhCuhjHNY0j05JrB97-KOFD0XUCQM3gMBU/edit). Mandatory for every text-producing skill. Run the full Section 7 two-pass audit against the deliverable:

- **Pass 1 (mechanical scan):** em-dashes, banned vocabulary (Section 2), banned phrases (Section 3), triadic rhythms and symmetric paragraphs (Section 4), summary-only section closers, date formatting per destination, specific-claims-trace-to-source, no emojis (unless requested), no clickbait.
- **Pass 2 (skeptical re-read):** restart from the top. Did I actually check every line, or skim? Em-dashes I missed? Banned phrases I rationalized? Triadic rhythms left because they "sounded fine"? Generic setup text that should be specific? Am I sure?
- **On any hit:** fix and re-run Pass 2 until clean. One pass is not enough.

**Third - skill-specific mechanical checks.**

- `ros-template-data.json` validates against the canonical schema `references/schema/ros-template.json`. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed.
- Grep for `{{...}}` returns ONLY the 12 approved tokens - zero invented tokens, zero `{{CO_HOST_NAME}}` legacy alias. Every placeholder appears bold.
- Main-body `### Q{N}:` count is 20 or fewer (Full episode) or ~10 (Extension). `## Additional Questions (Optional Pull)` (INTERNAL reserve) carries ALL remaining non-selected n-gram questions renumbered 1..M; main-body count + Additional Questions count = the n-gram table count.
- Zero hard-coded firm / attorney / city / state names in the tokenized body.
- Zero leaked pandoc inline-attribute markup as visible text in the rendered Doc (`[...]{.underline}`, `<u>`, `</u>`, `{.underline}`, `{.smallcaps}`, `{.mark}`).
- Localization scan result is PASS when scope is Location or Extension (a FAIL here is a hard block - regenerate offending pieces).
- The branded Google Doc was built from `build-ros-template-docx.py` - cover page, CE logo, "Run of Show" title, practice-area subtitle, "Prepared by Case Engine" + date footer, Roboto body.
- `metadata.json` provenance block present with at minimum: `run_date`, upstream `n_gram_source` + `entity_map_source`, `episode_goal`, `references_status`, `question_count`, `segment_count`, `placeholder_count`, `localization_scan` (PASS / FAIL / NA).
- Both write destinations verified: confirm the Drive shared-library scope folder (`Episode Templates/{Topic}/{scope}/`, Map 2) AND the local mirror contain the same artifacts (markdown, `.docx` locally + Google Doc remotely, JSON, metadata).
- Canonical destination gate PASSED: the resolved Drive parent is inside `Episode Templates/` and is NOT a client/firm episode folder (`### Quality gates`).
- INTERNAL section grep test: `grep -L "## INTERNAL" {client-facing-export}` returns zero hits for the client-facing Google Doc.

**On failure:** fix the markdown, regenerate `ros-template-data.json` and `metadata.json`, rebuild the DOCX, re-upload via `files.update`, re-run all checks. Do not proceed to `## Ship` until QA returns clean.

## Ship

What is?
The publish phase - builds the CE-branded DOCX, writes the trio plus `metadata.json` to the shared template library scope folder (`Episode Templates/{Topic}/{scope}/`, Map 2) at every scope, and mirrors the same artifacts to the local Desktop path. Never writes into a client/firm episode folder.

### What ships

- **ROS Template** - Google Doc - human-facing CE-branded view, cover page, Roboto typeface, real underlined entity runs, stable fileId.
- **ROS Template `.md`** - Markdown - raw tokenized source-of-truth, retains the `## INTERNAL` block.
- **`ros-template-data.json`** - JSON - machine-readable payload, downstream-consumed by `pod-3B-client-ros`.
- **`metadata.json`** - JSON (internal) - provenance: sources, counts, scope, episode goal, localization scan result.

### Where it ships

- **Drive:** the shared template library scope folder at every scope - `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/` (per `### Outputs -> #### Drive destination`, Map 2). Never a client/firm episode folder. This destination is fixed - the skill does not move existing Drive data.
- **Local mirror:** `~/Desktop/claude_code/deliverables/podcast/ROS Templates/{Topic}/{Episode}/{scope}/` - written every run.
- **Schema:** `~/.claude/skills/pod-3A-ros-template/references/schema/ros-template.json`.

### How it ships

Write to both destinations. On a write error to one, ship to the other and report the partial state.

- **Build the CE-branded DOCX.** The human-facing Google Doc MUST be the branded DOCX→Doc, never a raw markdown→Doc upload (the latter leaks `[entity]{.underline}` markup and has no cover page). Run `scripts/build-ros-template-docx.py` to emit both the `.docx` and the paired `.md` in one pass. The script reads `ros-template-data.json`, translates pandoc inline markers (`[text]{.underline}` → a real Word underline run in the DOCX; stripped to plain `text` in the paired `.md`), preserves the `{{PLACEHOLDER}}` tokens verbatim, applies CE branding per the Case Engine Branding folder (Roboto throughout - if the branding folder still says Calibri, Roboto wins), and emits both files.
- **Cover page.** Render per the canonical [Cover Page Spec](https://docs.google.com/document/d/1oydpI055jbj1FYDGeZfHQeMNjaWKUCFVGCRveeuJJCk/edit), with one override - the body and cover-page font is Roboto (if the spec still says Calibri, Roboto wins; flag the discrepancy when you spot it). Title `Run of Show` (CE Blue, 36pt, bold, Roboto). Subtitle is the practice area (e.g., `Car Accidents`) - ROS Template is brand-agnostic and tokenized, so the firm name is NEVER on the cover here. Scope / Topic line carries the episode topic + scope. Footer `Case Engine  |  Confidential  |  Page {PAGE}` auto-applied via the Drive API template.
- **Canonical styling** - Title styled as Google Docs "Title" (36pt, bold, dark #0f172a, Roboto); H2 as "Heading 1" (16pt, bold, CE Blue #3573FF, Roboto); H3 as "Heading 2" (13pt, bold, dark, Roboto); H4 as "Heading 3" (11pt, bold, dark, Roboto); body Roboto 11pt dark. Entities are real underlined runs in the DOCX, never literal `[...]{.underline}` text.
- **Drive write.** Upload the `.docx` as `application/vnd.google-apps.document` so Drive auto-converts it to a clean branded Google Doc (the human-facing artifact). Upload the `.md` as `text/markdown` (no conversion - raw source for downstream readers). Upload `ros-template-data.json` + `metadata.json` as-is. First-time create uses `files.create`; subsequent writes use `files.update` against the existing fileId (preserves the URL). Never re-upload the `.md` with `convert=true` to make a second Google Doc - that is the leaky path.
- **Roboto pass.** After the base Doc is uploaded, confirm Roboto over the full document range. Override only when a per-client `brand.json` typography block specifies otherwise.
- **Archive.** If the existence check moved a prior ROS Template file to `_archive-{YYYY-MM-DD}/`, the archive folder ships alongside the new artifacts. Archive ONLY the prior ROS Template file - sibling Client ROS / Client Guide slots are untouched.
- **Local mirror write.** Write the same ROS Template `.md`, the CE-branded `.docx`, `ros-template-data.json`, and `metadata.json` to the local mirror path. The mirror keeps the DOCX, not the auto-converted Google Doc. If the Drive write fails but the local write succeeds, surface the partial state in the report - do not silently swallow it.
- **Report back:**

  ```
  Done. ROS Template - {Topic} / {Episode} ({Scope}{, Location if applicable}).

   Folder: https://drive.google.com/drive/folders/{folder_id}
   ROS Template (branded Google Doc): https://docs.google.com/document/d/{doc_id}

  Segments: {segment_count}. Questions: {question_count}. Duration target: ~{duration} min.
  Placeholders used: {N}/12. Episode goal: {goal}. Localization scan: {PASS/FAIL/NA}. QA gate: PASS.

  Next: /pod-3B-client-ros (Phase 3 Run of Show) reads this ROS Template from the shared template library, populates placeholders for the firm, and writes the firm-specific Client ROS into the client episode `Run of Show/Client ROS/` slot - which then feeds /pod-3C-client-guide.
  ```

### Who to Notify

`notify: []` - this skill posts no notifications. The producer is informed via the inline report-back above.

---

## INTERNAL (not for client distribution - auto-stripped from all exports; the Formatting Guide rulebook and worked examples ride into the local markdown only, never into the Drive Doc)

### Formatting Guide (internal renderer rulebook - NEVER a deliverable section)

The authoritative rulebook the renderer honors. It governs how the document is written; it never appears in the produced document. The rules are the body of `### Editorial Guidelines -> Guideline 4` - speaker tags, bold, underline, attorney response bullets, setup text, no post-response co-host lines, no em dashes, bold tokens throughout. Internal calibration only.

### Producer Targets

- **Entity density target: 75%.** Natural conversation with specific named entities. Over-dense reads like an encyclopedia; under-dense reads generic.
- **Naturalness target: 85%.** If an entity feels forced in co-host setup, let the attorney cover it in their response instead. Natural-sounding on-air cadence beats perfect entity coverage.
- These are qualitative judgment calls during generation, not strict numeric checks. A post-generation read-through catches obvious violations.

### Segment pacing reference

Each segment targets a specific cognitive load: S1 orient + establish authority (foundational / definitional); S2 process + procedural detail; S3 edge cases + nuance; S4 takeaways + resources. Extensions collapse to 2 segments (intro + punchline), or 3 if the question set justifies it. Per-segment duration = floor(total / segment_count), displayed as `(~X min)` next to each segment header. Duration targets: Topic Only 20-25 min, Location 25-30 min, Extension 8-10 min.

### Topic-oriented vs Location-oriented mix (Location / Extension scope)

Location-scope episodes blend topic content with jurisdiction-specific grounding. Target mix: 60-70% topic-oriented (legal framework, process, decision points - scope-neutral) + 30-40% location-oriented (freeway names, local trauma centers, county courts, jurisdictional quirks). Woven, not segregated. Location content clusters in setup text where local framing matters and in attorney bullets with a jurisdictional answer; topic content dominates questions about legal primitives, national-carrier insurance mechanics, and federal-agency questions.

### Extension inheritance rule

Extensions ALWAYS inherit from the anchor. Never build a city extension that contradicts the anchor's statute references, court names, or jurisdictional rules. Extensions share state-level legal content with the parent (statutes, fault rules); only local entities change (city PD vs county PD, city trauma center vs regional). Extensions are still tokenized - client populate runs separately at `/pod-3B-client-ros`.

### Provenance block

`metadata.json` must include a provenance block with at minimum: `run_date`, `n_gram_source`, `entity_map_source`, `episode_goal`, `references_status` (used / empty), `schema_status` (validated / missing), upstream artifact paths, `question_count`, `segment_count`, `placeholder_count`, `localization_scan` (PASS / FAIL / NA).

### Source inventory

Records every input the run consumed: the resolved `n-gram-table.json` path, the `entity-map.json` + `entity-clusters.md` paths, any `keyword-research.json` mined for the Appendix, the firm-metadata source if used, and the calibration examples used (bundled file or in-skill reference material).

---

## Learning & Iteration

- [ ] After each run, note edge cases, localization scan failures, placeholder violations, and entity-map gaps; append GOOD / BAD / EDGE CASE entries to `references/examples/ros-template-examples.md`.
- [ ] Track recurring entity-map gaps - if the same belongs-but-missing entity surfaces across runs, propose a `/pod-1A-entity-research` map refresh.
- [ ] Watch for ROS Templates shipping more than 20 main-body questions; if it recurs, tighten the `### Organize questions into segments` guidance.

## Change Log

| Date | Change |
|---|---|
| 2026-07-10 | **Three-field geo model alignment (Gabe directive 2026-07-10, Whalen scoping).** Stamped the canonical three-field geo model into this skill using the exact field names: **Targeting strategy** (single/multi-location), **Optimization scope (show anchor)** (City/State/County/Regional), **Episode geo target** (the specific city THIS episode ranks for). Added a `### Framing -> Geo model` block defining all three fields plus the rule **anchor scope != per-episode target** (research runs at anchor breadth; each episode emphasizes its Episode geo target city naturally - a ceiling, never a forced quota; preserves no-city-quota / natural-tonality). Relabeled Greeting Q2 "Podcast anchor scope" -> "Optimization scope (show anchor)" and sharpened its City/State/Regional bullets to distinguish show anchor from per-episode target. Clarified Greeting Q4 that the resolved Location is the Episode geo target, which may differ from the show anchor. Updated the `{{CITY}}` placeholder source-of-value to state it resolves to the Episode geo target city. Bumped `references/schema/ros-template.json` 1.0 -> 1.0.1 (description-only clarification of the `location` field as the Episode geo target; no field added/renamed/reordered). No change to the 12-placeholder taxonomy, document structure, chain order, or Drive destinations. Revert: remove the Framing Geo model block, restore Greeting Q2 "Podcast anchor scope" wording + Q4 + `{{CITY}}` description, revert schema to 1.0. |
| 2026-06-17 | **Tokenized template lives ONLY in the shared template library (reverted the client-folder destination).** The Drive destination at Location/Extension scope previously pointed into the client/firm episode `Run of Show: .../Template ROS:` slot (Map 6). That was wrong - the tokenized template is generic and reusable across every firm, so it belongs ONLY in the shared template library at every scope: `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/` (Map 2). DROPPED the `Template ROS:` client-folder destination from the Drive-destination table, file-tree, and all SOP/Ship/Outputs/Gotcha prose; rewrote the "Why" cells to state generic/reusable -> shared library only. Added a hard pre-write **Canonical destination gate** to `### Quality gates` (same pattern as the pod-3B n-gram gate): before writing any artifact, assert the target parent is inside `Episode Templates/` and FAIL if it resolves to a client/firm episode delivery folder; no caller/workflow override may redirect it. The only ROS artifact in a client episode folder is the populated Client ROS (pod-4B). Greeting Q7, `### What is`, `### Framing`, Orient, and the report line updated to match. Revert: restore the Map 6 `Template ROS:` Location/Extension destination rows + file-tree + prose, and remove the Canonical destination gate. |
| 2026-06-17 | **Full n-gram reserve in the internal template (Additional Questions = entire remaining bank).** Clarified that the ROS Template is INTERNAL (the client never sees it), which is why it carries the ENTIRE n-gram question set: selected ~20 in the main body (sequential Q1..N), and EVERY non-selected n-gram question - not just "overflow beyond a 20 cap" - in `## Additional Questions (Optional Pull)` below the run of show, renumbered 1..M as question-text list entries (full attorney-response blocks not required for the reserve). Stated the reserve's purpose: swap in a vetted replacement when the client rejects a main question at review, without a fresh research pull. Strengthened across `### What is`, `### Quality bar`, Editorial Guideline 4 (document shape + new bullet), `### Quality gates` (Question cap + full reserve, with the count cross-check), `## Create -> ### Organize questions into segments`, and `### Generate the Appendix`. Client-facing trim stays downstream at pod-4B (ships main set only, never Additional Questions). No change to placeholders, structure order, schema, or chain. Revert: drop the "entire bank / all remaining" framing and restore "overflow beyond 20" wording; remove the count cross-check. |
| 2026-06-17 | **Sequential host-question numbering (Sutliff E8-E12 "numbered weird" fix).** The `### Q{N}:` heading was carrying the raw N-Gram Table bank index, so a 20-question ROS rendered with gappy numbers up to Q30 (Q1-10, Q12, Q14... Q30) - reads as missing questions. Added the hard rule in `### Generate the ROS body`: renumber the kept main-body questions 1..N in final reading order, decoupled from the bank index; preserve the original ref as `source_ngram_ref` in `ros-template-data.json` (provenance for Entity Checklist + pod-4D clip mapping) only, never in the heading. Appendix renumbers 1..M independently. Added the matching `### Quality gates -> Sequential numbering` gate (assert headings = 1,2,...,N, no gaps, none above count). pod-3B (stable bank refs) and pod-4B (populate-only) unchanged - 4A is the single lock point for kept set + numbering. Revert: remove the renumber rule + gate; restore raw-bank-ref headings. |
| 2026-06-12 | **Targeting-strategy branch (multi-location Mini model).** Greeting Q3/Q5 now resolve episode format from the client targeting strategy: single-location -> Full (~20q, ~50-55 min); multi-location -> one Mini per target city (10-12 questions hard cap, ~30-35 min, 3 segments, internal scope label stays `Extension`, NO anchor episode). Extension duration default corrected 8-10 min -> ~30-35 min (was internally inconsistent with the Greeting); segment default for Extensions set to 3; question cap updated ~10 -> 10-12. Template format/placeholders/structure and chain order UNCHANGED. Revert: restore Q3/Q5 wording, Extension duration 8-10 min, segments 2-3, cap ~10. |
| 2026-04-20 | Initial co-work version. Step 2 of the Run of Show workflow. Drive-native. 12 approved placeholders, matching Client ROS populate taxonomy. Appendix with Entity Architecture, Entity Checklist, Search Queries & Volume. Hard dependency on matching-scope N-Gram Table + entity map. |
| 2026-04-20 | Moved YAML frontmatter to the top of the file in bare `---` delimiters. Owner set to Gabe Jordan. Promoted Quality gates to H2; split into Content + Formatting subsections. Added Handoff Contract. Scaffolded `_references/` folder. |
| 2026-04-21 | DOCX layer reworked - client-facing artifacts render as branded Google Docs built from a CE-branded DOCX. Added `pod-` prefix for producer discoverability. |
| 2026-04-24 | Reverted `pod-` prefix across cowork skills. |
| 2026-05-12 | Template relocation - at Location/Extension scope the tokenized ROS Template lands in the firm's episode delivery folder alongside Client ROS + Client Guide. Branded DOCX→Doc made mandatory. Roboto replaces Calibri. Mandatory QA gate added. |
| 2026-05-14 | **v2.0.0** - Merged cowork ros-template v1.0 (canonical content) with original local pod-7-ros-template (Mode A enrichments). Output schema identical across modes. Bundled scripts + schemas + examples + iteration-log moved into canonical layout. |
| 2026-05-15 | Aligned Drive write paths to Client Folder Structure v2.4.0 → Map 6 - Location/Extension writes into the cell's `Template ROS:` slot; Topic Only into the Map 2 templates tree. Legacy compatibility paragraph added. |
| 2026-05-21 | Added the N-Gram Table <-> Topic Plan reconciliation check. The skill now reads the `pod-2A-topic-planner` Topic Plan for the episode (the `topic-plan-v{n}.json` / Episode Breakdown) as a CROSS-CHECK alongside the N-Gram Table, and confirms the question sets match before generating the ROS Template. If a question was cut or added in one but not the other, the gap is flagged and reconciled (N-Gram Table is the canonical bank; it is updated to match a later Topic Plan edit) - never a silent proceed. Closes the drift risk where a question the client reviewed in the Topic Plan would not match what reaches the Run of Show. Added as Checks item 10 and an `### Inputs` Required entry. | Gabe Jordan |
| 2026-05-20 | **v3.0.0** - Full structural refactor to the canonical CE skill structure. Renamed `pod-7-ros-template` -> `pod-3A-ros-template`; description, trigger, and all sibling refs repointed to the new pipeline codes (1A/1B/1C/2A/2B/4B/4C/4D). Removed the entire Mode A/B detection probe and all capability-probing apparatus - this skill runs locally in Claude Code, calls its tools directly, skips or fails on a tool error. Frontmatter completed (skill_kind, modes: multi, inputs, outputs, notify; version/date/owner moved to a metadata block). Best Practices restructured to the canonical contract H3s (Inputs / Outputs / Framing / Quality bar / Sourcing discipline / Editorial Guidelines / Quality gates / Gotchas / Iteration log); the placeholder taxonomy, formatting rulebook, research-palette rule, and localization rule relocated into Editorial Guidelines, Quality bar, and Quality gates. SOP rebuilt as H2 phase siblings (Checks / Prepare Inputs / Create / Update / Quality Assurance / Ship). Universal State Check logic moved into the Existence check + `## Update`. `## Workflow` demoted to `### Workflow` H3 carrying the unified 4-phase pipeline diagram. `## Output` folded into Best Practices Outputs. `## Push to Drive` renamed `## Ship` with the canonical H3 sub-structure. QA rewritten as the canonical three-tier gate with the hardwired Anti-AI Detection two-pass scan and an On-failure recovery line. Mode A/B local-mirror writes made unconditional. `references/schemas/` normalized to `references/schema/`. Old `## Appendix`-style content moved to the `## INTERNAL` two-tier model. Owner Gabe Jordan. |
| 2026-07-31 | v3.2.0 - removed the `pod-1-podcast-bible` dependency and all Fortress (`fortress-db`) access ahead of the skill moving to an environment without DB reach. Stripped every podcast-bible reference (workflow Phase 1 box + note, the prereq sentence, the routing bullet) and dropped the `mcp__fortress-db__query` firm-metadata lookup + the `crm_clients` Greeting auto-fill; Greeting values now come from the optional `podcast-overview.md` or the user. ClickUp untouched. Historical changelog/iteration-log entries left intact (append-only); the 2026-07-10 geo-model entry name-checks the (now-removed) bible as source of truth as a historical note only. | Gabe Jordan |
