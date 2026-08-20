---
name: pod-3B-client-ros
description: >
  Populate a tokenized ROS template with a specific firm's details (attorney,
  phone, website, episode number, recording date) and ship the recording-ready
  Client ROS - the host's on-air script - to the firm's Drive episode folder.
  Use whenever someone says "create client ros for [firm]", "populate ros for
  [firm]", "run ros for [firm] in [location]", "customize ros for [firm]",
  "build client ros", "make the client run of show", or "/pod-3B-client-ros".
  Phase 3 Run of Show of the podcast pipeline; hard dependency on a
  matching-scope ROS Template from pod-3A-ros-template; feeds pod-3C-client-guide downstream.
skill_kind: hybrid
modes: multi
inputs: [ros-template.md, ros-template-data.json, entity-map.json, podcast-overview.md, user-supplied-firm-data, case-engine-branding]
outputs: [json, markdown, gdoc]
notify: []
metadata:
  version: 3.3.0
  date: 2026-07-31
  owner: Gabe Jordan
  version_history: >
    1.0 - co-work Drive-native version (2026-04-20). 2.0.0 - merged cowork
    client-ros canonical content with original local pod-8-client-ros Mode A
    enrichments (2026-05-14). 3.0.0 - renamed pod-8-client-ros ->
    pod-3B-client-ros; full structural refactor to the canonical CE skill
    structure; probe apparatus and Mode A/B branching stripped (2026-05-20).
    3.1.0 - added Episode 1 / Founder Story hardcoded exception: duplicate the
    Founder Story ROS master template and populate firm tokens; no n-gram /
    entity / Template-ROS-slot dependency (2026-06-08). 3.2.0 - stamped the
    canonical three-field geo model (Targeting strategy / Optimization scope
    (show anchor) / Episode geo target) across Greeting, Editorial Guideline 6,
    Guideline 1, and the Populate SOP; location token fills from Episode geo
    target, not the show anchor; schema bumped 1.0 -> 1.1 (2026-07-10).
---

# Client ROS

> **Drive write governance:** All Drive operations (create, update, rename, move) follow [Ship]. Revise in place via `files.update` against the existing fileId, never delete-and-reupload (breaks the fileId/URL chain and silently kills every downstream reference).

### What is

The Client ROS - the HOST's on-air script for a podcast episode. This skill takes a tokenized ROS Template from `pod-3A-ros-template` and populates every `{{PLACEHOLDER}}` with a specific firm's details (attorney, phone, website, episode number, recording date), then ships the recording-ready result to the firm's Drive episode folder. The Client ROS carries speaker tags, producer notes, entity underlines, attorney-response scaffolding, and the Entity Checklist tally table at the bottom. It is NOT the attorney-facing document - the attorney-facing prep doc is the Client Guide, produced downstream by `pod-3C-client-guide`. The Client ROS is the firm-specific deliverable that lands in the client episode `Run of Show/Client ROS/` slot per Map 6, mirrored to the local Desktop path. The tokenized Template ROS that this skill populates from is NOT in the client folder - it lives ONLY in the shared template library (`templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{scope}/`, per Templates [Master] Structure Map 2); this skill reads it from there.

### Workflow

Client ROS is the second step of **Phase 3 (Run of Show)** of the podcast pipeline. It takes a finished generic ROS Template (`pod-3A-ros-template`) and produces the populated version the co-host reads live on air, then hands off to the Client Guide (`pod-3C-client-guide`), the final step of the pipeline.

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
- **Phase 2 Planning** - `pod-2A-topic-planner` ranks episodes; `pod-2B-n-gram-table` builds the 4-column collation table for one episode at one scope.
- **Phase 3 Run of Show** - `pod-3A-ros-template` builds the tokenized template; `pod-3B-client-ros` (this skill) populates it for a firm; `pod-3C-client-guide` derives the attorney guide from this skill's output. Phase 3 steps are sequential - each depends on the prior one.

Prerequisites: a matching-scope tokenized ROS Template from `/pod-3A-ros-template` is a hard dependency - this skill will not run without it. The Client Guide is NOT a precondition - it is produced downstream by `/pod-3C-client-guide`.

> **Episode 1 - Founder Story is a HARDCODED exception.** Episode 1 of every client's show is the **Founder Story** interview (formerly the "YOU Interview"). Its ROS template is NOT research-generated - a single pre-built, tokenized template is the fixed source of truth at `templates [master]/AEO Templates/Podcast/Episode Templates/Founder Story/` (`Run of Show // Founder Story (Episode 1) [TEMPLATE]`). For Episode 1, this skill's job is to **duplicate that Founder Story ROS template and populate the firm's tokens** - there is no n-gram table, no entity map, and no per-cell `Template ROS:` slot to read from. Populate the founder token set (`{{CLIENT_NAME}}`, `{{BUSINESS}}`, `{{HOST_NAME}}`, `{{TITLE}}`, `{{PODCAST_NAME}}`, `{{NICHE}}`, `{{LOCATION}}`, `{{WEBSITE}}`, `{{PHONE_NUMBER}}`, `{{RECORDING_DATE}}`) - note this differs from the standard `{{ATTORNEY_NAME}}` / `{{FIRM_NAME}}` / `{{CO_HOST_NAME}}` set. Preserve the founder shape (Host script -> Follow-ups -> Mandatory Info Capture -> Host Notes); do not restructure it into entity-woven attorney bullets. The content comes from the template, not research - you may lightly vary wording or order so each firm's copy is not 100% identical, but do not regenerate it from scratch.

### Trigger phrases

- `/pod-3B-client-ros`
- "create client ros for [firm]"
- "populate ros for [firm]"
- "run ros for [firm] in [location]"
- "customize ros for [firm]"
- "build client ros"
- "make the client run of show"

### Greeting

Hi, I'm Client ROS. Before I run, I need to confirm the podcast architecture. If podcast-overview has been run for this client, I'll read it and confirm in one line. If not, I'll ask:

1. **Client name.** Examples: "The May Firm", "Sutliff & Stout", "Conn Law Firm". Exact firm name as it appears in Drive.

2. **Optimization scope (show anchor) - what the podcast AS A WHOLE is optimized to rank for (drives core episodes + search intent).** This is one of the three canonical geo fields (see `### Editorial Guidelines -> Guideline 6`); it is the show-level anchor, NOT necessarily this episode's target city.
   - **City-level:** people in your market search the city as a unit ("Houston car accident lawyer"). Anchor: Houston.
   - **State-level:** people search the state as one unit ("California car accident lawyer"). Anchor: California. Extension cities per office.
   - **County / regional-level:** people search the region ("Inland Empire injury attorney", "Harris County", "Bay Area"). Anchor: the region/county. Cities within become extensions.

3. **Targeting strategy (single-location vs multi-location) + extension locations (if any).** Targeting strategy is the second canonical geo field: does the firm serve/rank one city or several? It drives episode format - single-location produces Full episodes; multi-location produces one Mini episode per target city (no single primary). Extensions are sub-scope episodes - short derivatives (10-12 questions, ~30-35 minutes). Under a single-location strategy they inherit from the anchor; under a multi-location targeting strategy they ARE the episode - client-facing term "Mini episode", no anchor/primary exists, one Mini per target city. Same-topic Minis for different cities must not share verbatim on-air language:
   - Houston city anchor -> Sugar Land, Katy, Pasadena suburb extensions
   - California state anchor -> Bakersfield, Fresno, Long Beach city extensions
   - Inland Empire regional anchor -> Ontario, Riverside, San Bernardino city extensions
   - List the extensions if any; "none" if the firm only targets the anchor.

4. **This run's Episode geo target** - the specific city THIS episode is built to rank for (the third canonical geo field). In single-location this equals the anchor city; in multi-location it is this Mini's target city, which is NOT the show anchor. This value fills the location token (`{{CITY}}`), not the Optimization scope (show anchor).

5. **Episode goal** - what is this episode trying to accomplish for this firm? Authority / education, Lead generation, Differentiation, Narrative / story, or Conversion (see `### Editorial Guidelines -> Guideline 3`). If unspecified I inherit it from the ROS Template `metadata.json`, then default to Authority.

I produce ONE deliverable: the Client ROS (the host's on-air script). The Client Guide (the attorney's prep doc) is a SEPARATE skill, `pod-3C-client-guide`, that runs AFTER me and reads the Client ROS I produce.

Then my skill-specific follow-ups:

6. Does `{Firm} Podcast/` exist in the shared Drive? (fuzzy match - "Conn Law" -> `Conn Law Firm Podcast/`)
7. Does the matching-scope tokenized ROS Template exist in the shared template library - `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/` (produced by `/pod-3A-ros-template`, Map 2)? The tokenized template lives ONLY there, never in the client folder. If it's not there, I stop and route you to `/pod-3A-ros-template`.
8. Do I have all 12 populate values? (firm, attorney, attorney first name, city, state, phone, website, practice area, episode number, recording date, podcast name, host name) - recording date is the one exception: if it's not set, I default it to `TBD` and proceed, never ask just for it.
9. Does the target `Client ROS:` slot already have a Client ROS? Archive and rebuild, or refresh in place? (I archive only the Client ROS file - I won't touch the ROS Template sibling.)
10. Next available episode number for this client, if you didn't provide one?

If anything's unclear I'll ask once in a single message - all missing fields at once, not one at a time. I won't touch Drive until you say go. You only need to know about `{Firm} Podcast/` - I handle the foundation lookups and writes transparently.

---

## Best Practices

The WHAT contract. Every other section references these by name; the SOP never restates them.

### Inputs

What is?
The materials this skill ingests - the matching-scope tokenized ROS Template and its data payload (hard dependency), the entity map for the Entity Checklist, the 12 populate values, the podcast architecture doc, and the Case Engine Branding folder - all resolved before any populate begins.

#### Required

- **Matching-scope ROS Template** (`ros-template.md` + `ros-template-data.json`) - the tokenized template from `/pod-3A-ros-template`, read from the shared template library `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{scope}/` (Map 2). The tokenized template lives ONLY in the shared library, never in the client folder. No silent fallback - if it is not in the matching-scope library folder, the skill stops and routes to `/pod-3A-ros-template`.
- **The 12 populate values** - firm name, attorney name, attorney first name, city, state, phone number, website, practice area, episode number, recording date, podcast name, host name. The full taxonomy lives in `### Editorial Guidelines -> Guideline 1`. **Recording date is non-blocking:** if no date is set yet, populate `{{RECORDING_DATE}}` as `TBD` and proceed - never stop or ask just for the recording date.
- **Firm name** - fuzzy-matched against `{Firm} Podcast/` folders in shared Drive (e.g., "Conn Law" -> `Conn Law Firm Podcast/`).
- **Topic** - practice area (e.g., "Car Accidents").
- **Episode** - matches the firm's parent episode folder under `{Firm} Podcast/Episodes/EP{N}: {episode_name} // {client_name}/`. **CANONICAL SOURCE:** the episode's topic/title is governed by the PUBLISHED Google Doc Topic Plan (the client edits that Doc manually) - confirm the episode against the live Doc, never against a local `topic-plan-v{n}.*` or old file; the Doc wins on any conflict and never build a topic absent from it (Eberst E5 slip-and-fall wrong-episode incident, 2026-06-19).
- **Scope** - Topic Only / Location / Extension.
- **Location** - required when scope is Location or Extension. Format: `CA`, `CA - Los Angeles County`, `CA - Long Beach`. No colons; dashes only.

#### Optional

- **`entity-map.json`** - the matching-scope entity map from `/pod-1A-entity-research`. Drives the Entity Checklist tally table at the bottom of the Client ROS. The skill proceeds without it but the Entity Checklist degrades to entities present in the script body only.
- **Episode goal** - Authority / Lead gen / Differentiation / Narrative / Conversion. Inherited from the ROS Template `metadata.json -> episode_goal` if present, then defaulted to Authority.
- **Refresh flag** - default refresh in place (routes to `## Update`). Pass `archive-and-rebuild` to archive the existing Client ROS to `_archive-{YYYY-MM-DD}/` and rebuild.

#### Auto-read (no action required)

- **`podcast-overview.md`** - architecture source of truth (anchor scope, extension cities, client name, show name, host name). If present at `{Firm} Podcast/.podcast-overview/podcast-overview.md` (or the local mirror), the skill auto-fills Greeting questions 1-3 plus `PODCAST_NAME` and `HOST_NAME`; otherwise it asks.
- **Firm identity fields (required from the user)** - `FIRM_NAME`, `ATTORNEY_NAME`, `ATTORNEY_FIRST_NAME`, `PHONE_NUMBER`, `WEBSITE` are provided directly by the user, or read from the podcast-overview doc when it carries them. There is no CRM / DB lookup; any field not supplied is a required prompt before the skill populates the template.
- **Case Engine Branding folder** - the canonical brand reference at [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) (folder id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`). The `## Ship` build reads logo, colors, fonts, and the [Cover Page Spec](https://docs.google.com/document/d/1oydpI055jbj1FYDGeZfHQeMNjaWKUCFVGCRveeuJJCk/edit). Brand values resolve from the folder at build time - never inlined.
- **Local Client ROS example references** - bundled `references/examples/client-ros-examples.md` as the quality-anchor set. If missing or empty, fall back to methodology and flag `"references": "empty"` in `metadata.json` - do not block.

#### Capabilities

The skill runs locally in Claude Code and calls its tools directly - it assumes they exist and uses them in this priority order. On a tool error, it skips that source and degrades to the next; it never probes for availability first.

- **Local filesystem read** - for an auto-detected local ROS Template at the canonical Desktop path and a local `podcast-overview.md`. Fastest path; no Drive round-trip.
- **`gws drive`** (or `mcp__claude_ai_Google_Drive__*` connector) - for the ROS Template + `ros-template-data.json` from the shared template library (`Episode Templates/{Topic}/{scope}/`, Map 2), the entity map, the podcast-overview doc, and the Case Engine Branding folder.
- **`mcp__ce-services__rag_query`** (`rag_name: koray`) - for SEO / entity-strategy cross-checks on question framing; surfaced as a producer note, never a silent rewrite.
- **User-supplied materials** in the greeting (pasted client fields, dropped files) and user interview for hard requirements still missing - the always-available floor.
- **Hard requirement** - the matching-scope ROS Template must resolve via local read or Drive. If it is missing, the skill stops and routes to `/pod-3A-ros-template`. At least one source for the 12 populate values must be reachable.
- **Behavior on a tool error** - skip that source and degrade to the next. With no reachable source, fall through to user-supplied + interview; flag every Inferred value with `> NEEDS CONFIRMATION:` per Sourcing discipline.

### Outputs

What is?
The artifacts this skill ships - the 3-format trio (a machine-readable JSON payload, a markdown source-of-truth, and a CE-branded Google Doc) plus a `metadata.json` provenance file - landing in the firm's episode `Client ROS:` slot per Map 6, mirrored to the local Desktop path.

#### Output formats

CE-wide default: every persistent artifact ships in three formats.

- **JSON** - `client-ros-data.json` - structured / machine-readable payload, all 12 placeholders resolved, the input the build script renders from. Validates against `references/schema/client-ros.json`. Downstream consumers read this for the populated script structure.
- **Markdown** - the Client ROS `.md` - local source-of-truth mirror, the downstream-readable raw source uploaded to Drive as `text/markdown` (no conversion). Retains the `## INTERNAL` block.
- **Google Doc** - the human-facing CE-branded Client ROS Doc. Built from a CE-branded `.docx` (cover page, logo, Roboto body, real underlined entity runs, "Prepared by Case Engine" footer) emitted by `scripts/build-client-ros-docx.py`, then uploaded with `mimeType: application/vnd.google-apps.document` so Drive auto-converts the DOCX to a clean Google Doc. Created / updated in-place via `files.update` against a stable fileId so the URL never breaks for downstream links.

A `metadata.json` provenance file ships alongside the trio (internal-only, not a client-facing artifact - records sources, the resolved 12 values, episode goal, Drive fileIds, references status).

#### What ships

- **Client ROS** - Google Doc - human-facing CE-branded view, cover page, Roboto typeface, real underlined entity runs, stable fileId.
- **Client ROS `.md`** - Markdown - raw populated source, downstream-readable, retains the `## INTERNAL` block.
- **`client-ros-data.json`** - JSON - machine-readable payload, all 12 placeholders resolved; validates against `references/schema/client-ros.json`.
- **`metadata.json`** - JSON (internal) - provenance: data sources, the resolved 12 values, episode goal, template scope, references status, run timestamp.

#### Drive destination

Shared drive root: `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`). Per [Client Folder Structure](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU/edit) → Map 6, the Client ROS lands in the cell's `Client ROS:` slot.

The tokenized Template ROS this skill populates from is NOT in the client folder - it lives ONLY in the shared template library (`templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{scope}/`, Map 2), read-only for this skill. The client `Run of Show/` folder holds ONLY the `Client ROS:` slot.

```
{Firm} Podcast/Episodes/EP{N}: {episode_name} // {client_name}/Run of Show: {episode_name} // {client_name}/
  Client ROS: {episode_name} // {client_name}/                                        ← THIS SKILL writes here (the only slot in Run of Show/)
    E{N}: {Episode Title} // {Firm Name} // Client ROS - {Location}.md                 raw markdown source (text/markdown)
    E{N}: {Episode Title} // {Firm Name} // Client ROS - {Location}                    branded Google Doc (in-place files.update)
    client-ros-data.json                                                               machine-readable payload, all 12 resolved
    metadata.json                                                                      provenance
    _archive-{YYYY-MM-DD}/                                                             (only the prior Client ROS, if one existed)
```

Each recording cell - anchor or extension - is its own `EP{N}: ...` entry in `Episodes/`; extensions are siblings of the anchor at the EP level, each with its own localized `{episode_name}`. The double-slash ` // ` separator with spaces is literal. Append ` (Extension)` after `{Location}` for extension cells. The Drive destination is fixed - this skill does not move existing Drive data.

**Legacy compatibility:** MVP Accident Attorneys and any other client with pre-2026-05-15 episodes use the older `EP{N}/01 Strategy/` convention. If the resolved episode parent contains a `Run of Show: {episode_name} // {client_name}/` subfolder with a `Client ROS:` slot inside it, it is a Map 6 episode. If instead it contains an `EP{N}: ROS // {Firm}/` or `01 Strategy/` subfolder, it is a legacy episode - read and write per the legacy path for that episode only (do not auto-migrate).

#### Local mirror

`~/Desktop/claude_code/deliverables/podcast/Client ROS/{Topic}/{Episode}/{scope}/` - holds the same Client ROS `.md`, the CE-branded `.docx`, `client-ros-data.json`, and `metadata.json`. `{scope}` = `Topic Only`, `Locations/{Location}`, or `Extensions/{Location}` to mirror the Drive scope convention. The mirror keeps the DOCX (not the auto-converted Google Doc, which only exists in Drive). It enables fast local iteration, downstream local-skill consumption (`pod-3C-client-guide` reads from here when running locally), and offline review. Written on every run.

#### Schema

`references/schema/client-ros.json` - the canonical JSON schema `client-ros-data.json` validates against. The schema enforces all 12 resolved placeholders, segments, questions, durations, the Entity Checklist rows, and the episode goal. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed - do not block on a missing schema.

#### Sections INCLUDED in the client-facing Google Doc

- Branded cover page (CE logo, "Run of Show" title, firm-name subtitle, "Prepared by Case Engine" footer)
- Compact metadata line (Episode + duration + recording date; attorney / firm / location / website populated)
- Producer Notes (brief)
- Introduction
- Segments S1-S4 with questions, speaker tags, attorney response scaffolding, entity underlines
- Closing and Call to Action (with populated `{{PHONE_NUMBER}}` and `{{WEBSITE}}`, both bold)
- The Entity Checklist tally table at the very bottom, after `*End of Run of Show*`

#### Sections EXCLUDED (never in the client-facing artifact)

- `## Quality Assurance` and everything from that heading onward
- Known Gaps, Handoff Contract, Next Steps, provenance block
- Any inline Appendix, Formatting Guide, or producer-reference material (Appendix content stays in the upstream ROS Template)
- The `## Additional Questions (Optional Pull)` section - this is the INTERNAL reserve pool of non-selected n-gram questions; it lives ONLY in the ROS Template and is intentionally excluded from the client-facing Client ROS, which ships the main selected set only

The Google Doc renderer truncates the markdown source at the first `## Quality Assurance` heading and discards everything after - this keeps internal-process content out of client-facing deliverables while the same markdown serves as the internal source of truth. See `## INTERNAL` for the grep test.

#### Capabilities

Both write destinations are written every run. On a write error to one, the skill ships to the other and surfaces the partial state in the report - it does not silently lose the deliverable.

- **Drive** - `gws drive` (or `mcp__claude_ai_Google_Drive__*` connector) - writes the markdown, the branded Google Doc, the JSON, and metadata into the cell's `Client ROS:` slot.
- **Local mirror** - local filesystem write to the local mirror path, alongside the Drive write.
- **Behavior on a write error** - if one destination errors, ship to the other and report the partial state. If both error, hard-fail with a clear message; do not silently lose the deliverable.

#### Examples

`references/examples/client-ros-examples.md` - single doc with GOOD / BAD / EDGE CASE labeled sections per CE convention. Read 1-2 examples matching the requested scope as calibration before generating. If the folder is empty, proceed on methodology and flag `"references": "empty"` in `metadata.json`.

#### Routing

- **Upstream (required, hard dependency):** `/pod-3A-ros-template` - the matching-scope tokenized ROS Template.
- **Downstream (required):** `/pod-3C-client-guide` translates the populated Client ROS into the attorney-facing prep doc.
- **Refresh:** re-run with the same episode + scope (routes to `## Update`).

#### Handoff Contract

This skill produces the host-facing Client ROS and hands off to `/pod-3C-client-guide`:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| Client ROS `.md` + branded Google Doc | `/pod-3C-client-guide` + human (co-host reads live on air) | Full structure: metadata, segments, questions, producer notes, durations, populated `{{PLACEHOLDERS}}`. `pod-3C-client-guide` translates questions verbatim into the Client Guide Segment Breakdown and producer notes into italic segment-goal paragraphs. |
| `client-ros-data.json` | `/pod-3C-client-guide` | All 12 resolved values, segments, questions, durations, episode goal, the Entity Checklist rows |
| `metadata.json` | (not consumed downstream) | Internal provenance - data sources, the resolved 12 values, episode goal, template scope, references status |

Downstream consumers can rely on: the Google Doc URL is stable for the lifetime of the Client ROS (preserved via `files.update` across re-runs); `client-ros-data.json` validates against `references/schema/client-ros.json`; zero leftover `{{...}}` placeholders in the populated output. Upstream pull (hard dependency): the ROS Template + `ros-template-data.json` from `/pod-3A-ros-template` in the shared template library (`Episode Templates/{Topic}/{scope}/`, Map 2). The skill refuses to run without it.

### Framing

The Client ROS is the HOST's recording script - the live on-air document the co-host reads and references during the interview. It is a TRANSLATION of a tokenized template into a firm-specific script, not original content. It is never the attorney-facing prep doc (that is the Client Guide, `pod-3C-client-guide`), never restructures the upstream template, and never invents content the ROS Template did not carry. It is also the CLIENT-FACING TRIMMED view of the ROS Template - the main selected question set ONLY. The ROS Template's `## Additional Questions (Optional Pull)` reserve (the full pool of non-selected n-gram questions) is INTERNAL and stays upstream; it never carries into the Client ROS.

### Quality bar

What "good" looks like - the pass / fail intuition.

- All 12 approved placeholders are resolved to real values; a grep for `{{...}}` in the populated output returns zero.
- Bold is preserved around every populated placeholder (`**{{FIRM_NAME}}**` -> `**Conn Law Firm**`, not `Conn Law Firm`).
- The document structure exactly matches the upstream ROS Template shape - no restructuring during populate.
- Speaker tags stay italic, never bold, never code blocks. Entities (including the populated attorney / firm / podcast name) are pandoc `[entity]{.underline}` runs.
- The Entity Checklist table is present at the very bottom, after `*End of Run of Show*`, with all 4 columns.
- When scope is Location or Extension, every entity is localized - generic unqualified categories are a hard fail.
- The human-facing Google Doc is the CE-branded DOCX→Doc, never a raw-markdown→Doc upload.
- No em dashes, no banned vocabulary - the Anti-AI Detection scan fires before publish.

### Sourcing discipline

The Confirmed / Inferred / Unknown three-state pattern. Never block, always ship, never silent. The Client ROS still ships when data is incomplete; gaps surface in `## INTERNAL` or with `> NEEDS VERIFICATION:` blocks.

- **Confirmed** - claim traces to a specific source. Every placeholder value resolved from the podcast-overview doc or supplied directly by the user is Confirmed. Ship as-is, no marker.
- **Inferred** - sensible default applied when a source is insufficient (e.g., `{{CITY}}` left empty for a state-level scope, or an episode goal defaulted to Authority). Ships with `> INFERRED: {what + why}` flag.
- **Unknown / NEEDS CONFIRMATION** - no source AND no defensible default. Ships with `> NEEDS CONFIRMATION: {what's missing}` block, never silently synthesized. A populate value with no source and no defensible default is NEEDS CONFIRMATION - never guess a firm phone or website.

### Editorial Guidelines

Cross-cutting content rules for the populate. The SOP points back here; the rules live here once.

**Guideline 1 - The 12 approved placeholders, all filled, never invented.**

- **Approved taxonomy** (must match `pod-3A-ros-template` exactly):

  | Placeholder | Source |
  |---|---|
  | `{{FIRM_NAME}}` | Full firm name |
  | `{{ATTORNEY_NAME}}` | Full attorney name |
  | `{{ATTORNEY_FIRST_NAME}}` | First name only |
  | `{{CITY}}` | City name (from Location if city-level) |
  | `{{STATE}}` | State full name (`CA` → `California`) |
  | `{{PHONE_NUMBER}}` | Firm phone `(XXX) XXX-XXXX` |
  | `{{WEBSITE}}` | Firm website (include `https://`) |
  | `{{PRACTICE_AREA}}` | The Topic, lowercase, plural ("car accidents") |
  | `{{EPISODE_NUMBER}}` | Integer, just the N in `E{N}` |
  | `{{RECORDING_DATE}}` | `MM-DD-YYYY`, or `TBD` if no date is set yet |
  | `{{PODCAST_NAME}}` | Client's podcast name (usually `{Firm Name} Podcast`) |
  | `{{HOST_NAME}}` | CE host on the recording (was `{{CO_HOST_NAME}}` - renamed) |

- **Populate rules:** `{{CITY}}` is the episode's **Episode geo target** city - the specific city THIS episode is built to rank for, NOT necessarily the show's Optimization scope (show anchor); it is empty only when the Episode geo target is state-level (or on user override). `{{STATE}}` converts the code to the full name (`CA` -> `California`); `{{PRACTICE_AREA}}` is lowercase plural; `{{EPISODE_NUMBER}}` is the integer only.
- **Migration note:** an older template that still contains `{{CO_HOST_NAME}}` is treated as an alias for `{{HOST_NAME}}` at populate time; log the find in `metadata.json` so the upstream template can be refreshed.
- **Banned:** any unresolved `{{...}}` in the populated output; stripping the bold off a populated placeholder.
- **Why:** an unresolved token ships into the recording as literal markup; a stripped bold loses the visual signal the host relies on.
- **Where it fires in the SOP:** `## Create -> ### Populate placeholders`, and the placeholder gate in `### Quality gates`.

**Guideline 2 - Preserve the ROS Template's formatting and structure exactly; never reformat.**

- **Document structure** (inherited from `pod-3A-ros-template`, never restructured): title H1; metadata block (Practice Area / Episode + Duration / Recording Date / Template Version / Location, every value bold); Producer Notes (brief); Introduction (exactly three `*[Co-Host]*` paragraphs - welcome-back, greet attorney, topic frame - plus `*Transition directly into Q1.*`, zero `*[Attorney Response]*` block); strict question blocks (`### Q{N}: {q}? ({t} min)` -> 1-sentence co-host setup -> bold framing question -> `*[Attorney Response]*` + `**Label:** detail` bullets) - the `### Q{N}:` labels are clean sequential 1..N inherited verbatim from the ROS Template, never the raw n-gram bank index (gaps/out-of-range numbers fail the Sequential numbering gate and route back to `/pod-3A-ros-template`); no post-response co-host lines between questions within a segment; Closing and Call to Action with populated `{{PHONE_NUMBER}}` + `{{WEBSITE}}`, both bold; `*End of Run of Show*`.
- **Formatting** - bold marks mandatory verbatim phrases + populated placeholders; italic marks speaker tags (`*[Co-Host]*`, `*[Attorney Response]*`) and producer notes; entities use pandoc `[entity]{.underline}` (never HTML `<u>`). Populated `{{ATTORNEY_NAME}}`, `{{FIRM_NAME}}`, and `{{PODCAST_NAME}}` are entities too - underlined every time they appear. Legacy `<u>entity</u>` tags from older templates are converted to `[entity]{.underline}` at populate time.
- **Banned:** an inline Appendix in the populated Client ROS (Appendix content lives in the ROS Template only); the `## Additional Questions (Optional Pull)` reserve section (it is INTERNAL to the ROS Template and intentionally excluded here - the Client ROS is the trimmed selected set only); a "Formatting Guide" section in the body; em dashes anywhere.
- **Why:** the co-host reads this script live; a reformat or a structural drift breaks the on-air cadence and the downstream Client Guide translation.
- **Where it fires in the SOP:** `## Create -> ### Populate placeholders` and `### Build the Entity Checklist`.

**Guideline 3 - Research is the palette; the populate layers in the slice that serves THIS episode's goal.**

- Even after a template is built at the right scope, populate decisions are goal-sensitive. The episode goal (Authority / Lead gen / Differentiation / Narrative / Conversion) is taken from the user, inherited from the ROS Template `metadata.json`, or defaulted to Authority.
- **Selection rule at populate time:**
  - **Authority** - statute + agency + insurance entity density; attorney personality held for closing only.
  - **Lead generation** - attorney credentials surface in Producer Notes + S1 wrap + S4 close; phone + website called out twice; CTA bolding doubled.
  - **Differentiation** - pull High-tier virality candidates into S3/S4 via the firm's actual case history; verdict numbers woven where natural; firm-specific entities get extra underline emphasis.
  - **Narrative / story** - chronology-first; attorney bullets are case beats; underlined entities cluster around named courts, opposing insurers, expert witnesses.
  - **Conversion** - consultation + fee-structure language in every segment wrap; phone + website in closing carry tripled bold emphasis.
- **Why:** a firm shooting for lead generation surfaces credential language and CTA emphasis differently than a firm shooting for authority or narrative storytelling.
- **Where it fires in the SOP:** `## Create -> ### Populate placeholders`. The goal is recorded in `client-ros-data.json -> episode_goal` and `metadata.json` so downstream artifacts honor the same framing.

**Guideline 4 - The Entity Checklist tally table at the bottom.**

- Every populated Client ROS includes an Entity Checklist table at the very bottom, AFTER `*End of Run of Show*`. It is the recording-time tally sheet the host / producer uses to verify each named entity gets the target number of mentions.
- **Format - 4 columns, one row per entity drawn from the matching-scope entity map:** Entity (wrapped pandoc `[entity]{.underline}`, Tier 1 + Tier 2 entities, group order national → state → county → city) | Questions (comma-separated Q numbers where attorney bullets reference the entity) | Target Mentions (a range, scaled by question count - 1-2 Qs target 2-3, 3-4 Qs target 3-5, 5-6 Qs target 5-7, 7-9 Qs target 7-10, 10+ Qs target 12-15; headline entities get the upper end) | Actual Mentions (blank - the producer tallies during recording review).
- **Row count target:** 10-15 entities for Location/City scope; 6-10 for Topic Only; 12-18 for state-level anchor episodes.
- **Banned:** the firm / attorney / podcast name in the Entity Checklist (those live in the ROS body, never this table); any Appendix material after the Entity Checklist (the table ends the file).
- **Why:** the producer uses this table during post-recording review to verify entity coverage; a missing or mis-shaped table loses the tally signal.
- **Where it fires in the SOP:** `## Create -> ### Build the Entity Checklist`.

**Guideline 5 - Localized entities only when scope is Location/Extension.**

- **Banned:** generic, unqualified entity categories when scope is Location or Extension - `Police Department`, `Sheriff's Office`, `Insurance Company`, `Civil Court` (unqualified), `Hospital` (unqualified).
- **Allowed:** the localized instance from the matching-scope entity map - `Houston Police Department (HPD)`, `Harris County Civil Courts`. Generic categories are acceptable ONLY when scope is Topic Only.
- **Why:** a generic category in a localized script is a localization leak; an extension's jurisdictional posture must match its parent anchor.
- **Where it fires in the SOP:** `## Create -> ### Populate placeholders`, and the jurisdiction-consistency check in `### Quality gates`.

**Guideline 6 - Geo in the script: natural placement, no city quota.**

- **Three-field geo model (canonical, stamped identically across all pod skills):** (1) **Targeting strategy** - `single-location` vs `multi-location`; drives episode format (single → Full episode; multi → one Mini episode per target city, no single primary). (2) **Optimization scope (show anchor)** - City / State / County / Regional; what the podcast AS A WHOLE is optimized to rank for. (3) **Episode geo target** - the specific city THIS episode is built to rank for; it fills the `{{CITY}}` / location token. **Anchor scope != per-episode target.** The show can be optimized for a broad scope (e.g. the whole state) while each episode targets a specific city we're trying to rank for. Research runs at the anchor breadth; each episode's questions/titles emphasize that episode's Episode geo target city naturally - a ceiling, never a forced quota (see the no-city-quota rule below). Getting this wrong is how a multi-location statewide firm ends up with episodes that all sound like one city, or how city emphasis silently becomes a city floor. At populate time this skill fills the location token with the **Episode geo target** city, NOT necessarily the Optimization scope (show anchor).
- **Rule:** at Location/Extension scope the script must READ as a local show - the target city present and grounding - WITHOUT being stamped onto every on-air line. Aim for the city to land naturally in roughly a THIRD of the question lines (a soft center of gravity, not a quota); the remaining lines carry locality through a named local entity (corridor, circuit court, trauma center, local agency) or stay geo-neutral. HARD CEILING: the city on more than HALF the lines reads as keyword spam and FAILS. Guard the other way too: a script where the city is essentially absent is too thin and must still read as local. Any line whose substance is state law NAMES the state ("Florida's 14-day PIP rule") and does not get a city token bolted on - that is not a city mention. The state-law layer must be visibly woven through the script. The county appears only where it earns its place (the official court name, a county agency that is the real actor) - drop county references rather than pad them. Locality is reinforced by the localized entity stack running through the attorney bullets, not by the city token alone. (Mirrors pod-3B Editorial Guideline 4 - keep the two rules identical.)
- **Banned:** the city token on 100% of question lines; the adjective-spam construction where the city is bolted onto a generic noun ("a Stuart claimant", "a Stuart crash", "Stuart drivers") instead of placed naturally ("after a crash in Stuart", "here in Stuart"); county-first phrasing as the default ("an Anne Arundel County parent" when the market is Glen Burnie); county mentions padded in for localization optics.
- **Allowed:** city-first framing with natural placement ("a Glen Burnie parent", "here in Stuart"); the county court named because it is the real venue; "Maryland's mutual consent divorce" for state law with no city token forced on; a line that names a corridor or hospital to carry locality without repeating the city.
- **Quality check:** in the rendered client-facing doc, the target city lands in roughly a third of the question lines - present and grounding but NOT on every line. City on more than HALF the lines FAILS as spam; city essentially absent (with no local entities carrying locality) FAILS as too thin. There is NO floor that forces the city in to hit a quota. At least one line names the state for its state-law substance. Official entity names like `Circuit Court for {County}` are exempt from the county count. The adjective-spam construction FAILS on sight.
- **Why:** the episode exists to build geo relevance for the target city, but a script that says the city in every line reads as keyword spam to listeners and to the AI systems indexing the transcript - and it buries the state-law substance that actually answers the searcher. Both failure directions are real: county/state-heavy erases the city (Mohink EP2, 2026-06-12); city spammed in every line with state law not woven through (Eberst E2/E3, 2026-06-16).
- **Where it fires in the SOP:** `## Create -> ### Populate placeholders`, and the city-share check in `### Quality gates`.

### Quality gates

Mechanical pass / fail conditions checked in `## Quality Assurance`.

- **Placeholder gate** - all 12 approved placeholders resolved; zero leftover `{{...}}` anywhere (grep explicitly). Bold preserved around each populated value.
- **Document structure** - matches `### Editorial Guidelines -> Guideline 2`. H1 once; metadata block with all five canonical lines; Producer Notes (brief); Introduction (exactly 3 `*[Co-Host]*` paragraphs + transition, zero `*[Attorney Response]*`); strict question blocks; no post-response co-host text between questions; Closing/CTA with populated phone + website both bold; `*End of Run of Show*`. No "Formatting Guide" section, no inline Appendix.
- **Question cap (trimmed, no reserve)** - main-body `### Q{N}:` count is 20 or fewer (Full episode) or 10-12 (Extension/Mini). The Client ROS is the CLIENT-FACING TRIMMED doc - the main selected set ONLY. It MUST NOT carry a `## Additional Questions (Optional Pull)` section; that reserve is INTERNAL and lives ONLY in the ROS Template (`pod-3A-ros-template`). If a `## Additional Questions (Optional Pull)` heading appears in the populated Client ROS, that is a FAIL - it must be stripped before ship. The full n-gram reserve stays upstream so a rejected main question can be swapped in at 4A; the client never sees it.
- **Sequential numbering (VERIFY-and-refuse)** - the host-facing `### Q{N}:` headings MUST run sequential 1..N with NO gaps and NO number exceeding the question count (a 20-question doc ends at Q20, never Q30). Grep the headings and assert the sequence is exactly 1,2,3,...,N. If the numbering is gappy or out of range (e.g., Q1-10, 12, 14, 15, 16, 17, 21, 22, 24, 25, 30 - the Sutliff E8 failure: 20 questions but numbered up to Q30), the doc carried the upstream n-gram bank numbers instead of the ROS Template's sequential numbering and this gate FAILS. This skill is populate-only and must NOT restructure or renumber - on failure STOP and route back to `/pod-3A-ros-template` to renumber the kept set 1..N (4A is the lock point); do NOT silently renumber here. The appendix `## Additional Questions (Optional Pull)` list runs its own sequential 1..M. Any Entity Checklist "Questions" column / appendix cross-reference must use the same sequential numbers, never the raw n-gram bank index.
- **Entity Checklist** - present at the very bottom, after `*End of Run of Show*`, 4 columns (Entity / Questions / Target Mentions / Actual Mentions); entities wrapped `[entity]{.underline}`; the table ends the file.
- **Jurisdiction consistency** - every entity reference uses the localized form per the matching-scope entity map; zero unqualified generic entity categories at Location/Extension scope. Statute citations, court names, and jurisdictional rules internally consistent (an extension matches its parent anchor).
- **Branded render** - the Google Doc was built from `build-client-ros-docx.py` (cover page, logo, Roboto body). Zero leaked pandoc inline-attribute markup as visible text (`[...]{.underline}`, `<u>`, `</u>`, `{.underline}`, `{.smallcaps}`, `{.mark}`). Zero legacy `<u>...</u>` HTML tags.
- **Schema validate** - `client-ros-data.json` validates against `references/schema/client-ros.json`.
- **Provenance present** - `metadata.json` carries the provenance block (see `## INTERNAL`).
- **Artifacts present** - markdown, JSON, metadata all written; branded Google Doc exists; filename follows the canonical pattern.
- **No em dashes** - plain hyphens only anywhere in the output.

### Gotchas

Failure modes that are warnings, not enforceable rules.

- **The ROS Template must be in the shared template library** (`Episode Templates/{Topic}/{scope}/`, Map 2) - that is the ONLY place it lives; it is NOT in the client folder. No fallback. If it is not there at the matching scope, stop and route to `/pod-3A-ros-template`.
- **The Client Guide is a DOWNSTREAM artifact, not a precondition** - it is produced by `/pod-3C-client-guide` AFTER this skill runs. Never block on it, never require it, never generate it from this skill.
- **Firm name fuzzy match** - "Conn Law" resolves to `Conn Law Firm Podcast/`, "May Firm" to `The May Firm Podcast/`. If ambiguous (two firms with similar names), ask.
- **Episode number reuse** - don't renumber. Check existing `Episodes/` folders for the highest E-number, then use the next one if not provided.
- **Archive before overwrite, but only the Client ROS** - never silently replace an existing populated Client ROS; move it to `_archive-{YYYY-MM-DD}/` inside the `Client ROS:` slot. Never archive or overwrite any Client Guide sibling in `Client Guide:`, and never touch the tokenized ROS Template in the shared template library (this skill only reads it).
- **Branded output is mandatory** - do NOT upload the raw `.md` with `convert=true` - Google's markdown import leaks `[entity]{.underline}` as visible text and has no cover page. The pipeline is `markdown → build-client-ros-docx.py → DOCX → Drive upload as gdoc mimeType → clean branded Google Doc`.

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
The pre-flight phase - reads the iteration log, orients to the right episode folder, verifies the upstream ROS Template exists, and decides whether this run creates a new Client ROS or updates an existing one.

### Orient

What is?
The orientation step - read the iteration log, resolve the firm and episode folders, and load the podcast architecture context before producing anything.

- **Read the iteration log.** Read `references/iteration-log.json`, filter to entries with `status: open` or `status: in-progress`, surface them to the agent as known issues to watch for this run.
- Find `{Firm} Podcast/` in the shared Drive (fuzzy match if needed - "Conn Law" -> `Conn Law Firm Podcast/`). If `podcast-overview.md` is reachable, read it and auto-fill Greeting questions 1-3 plus the show name and host name; confirm in one line. Otherwise ask the Greeting questions.
- Navigate to the cell's parent episode folder `Episodes/EP{N}: {episode_name} // {client_name}/`. Find or create the `Run of Show: {episode_name} // {client_name}/` category folder and the `Client ROS: {episode_name} // {client_name}/` slot. Detect a legacy episode per the rule in `### Outputs -> #### Drive destination` and follow legacy paths for that episode only.
- Read `references/examples/client-ros-examples.md` and pick 1-2 examples matching the requested scope as quality anchors. If the file is empty, proceed on methodology alone and flag `"references": "empty"` in `metadata.json`.

### Verify upstream ROS Template

What is?
The hard-dependency gate - confirm the matching-scope ROS Template exists in the shared template library (`Episode Templates/{Topic}/{scope}/`, Map 2) before any populate begins. The tokenized template is NOT in the client folder.

- **Episode 1 / Founder Story exception (check FIRST):** if the episode is Episode 1 (Founder Story), the upstream ROS Template is NOT in a per-cell `Template ROS:` slot - it is the hardcoded master template at `templates [master]/AEO Templates/Podcast/Episode Templates/Founder Story/`. Duplicate that template and populate the firm's tokens; skip the slot-resolution and routing below.
- Resolve the ROS Template (`E{N}: ... // ROS Template - {Location}.md` + `ros-template-data.json`) from the shared template library scope folder `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/` (Map 2). `/pod-3A-ros-template` wrote it there; the tokenized template never lives in the client folder.
- If the ROS Template is NOT in the expected slot, STOP and route the user to `/pod-3A-ros-template` to build it there first. Do not fall back to anything; do not invent a template.
- The Client Guide is NOT checked here - it is produced downstream by `/pod-3C-client-guide`.
- **Handoff Contract check.** Verify upstream paths match the declared Inputs. If any other upstream file shows up (a new Appendix asset, an alternate tokenized format) that is not declared in the Inputs contract, STOP and ask: "I see upstream output at {path} but my Inputs contract doesn't declare it. Should I (a) mine it with my best guess, (b) skip it, or (c) pause while you update the handoff contract?" Do not guess silently.

### Existence check

What is?
The mode router - decide whether this run creates a new Client ROS or updates an existing one based on whether the resolved `Client ROS:` slot already has content.

- Look for a `Client ROS` Google Doc + `client-ros-data.json` inside the resolved `Client ROS:` slot.
- **Missing:** no prior artifact - route to `## Create`.
- **Found:** surface provenance (existing `metadata.json` run date) and ask: refresh in place / archive-and-rebuild / cancel.
  - Refresh in place -> route to `## Update`.
  - `archive-and-rebuild` (or the refresh flag passed at invocation) -> move ONLY the prior Client ROS file (and its paired Doc) to `_archive-{YYYY-MM-DD}/` and route to `## Create`. The ROS Template and Client Guide siblings are left untouched.

## Prepare Inputs

What is?
The input-preparation phase - load the ROS Template, resolve the 12 populate values, load the entity map, and resolve branding into a working set ready for the Create or Update phase.

Work through the input sources in priority order; on a tool error, skip that source and degrade to the next.

- **Load the ROS Template.** Read `ros-template.md` + `ros-template-data.json` from the shared template library scope folder resolved in Checks (`Episode Templates/{Topic}/{scope}/`, Map 2) - the tokenized structure to populate.
- **Resolve the 12 populate values.** Collect the firm identity values (`FIRM_NAME` / `ATTORNEY_NAME` / `ATTORNEY_FIRST_NAME` / `PHONE_NUMBER` / `WEBSITE`) directly from the user; read the podcast-overview doc for `PODCAST_NAME` and `HOST_NAME` (and any firm fields it carries). Prompt the user once for all missing fields at once - these are required before populating.
- **Load the entity map.** Parse `entity-map.json` when present - it drives the Entity Checklist tally table.
- **Resolve the episode goal.** Take it from the user, inherit it from the ROS Template `metadata.json -> episode_goal`, or default to Authority.
- **Resolve branding.** Read the Case Engine Branding folder (id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`) - logo, colors, fonts, the Cover Page Spec. Hold the resolved values for the `## Ship` build. A per-client `brand.json` typography block overrides the CE default when present.
- **Load calibration examples.** Hold the 1-2 scope-matched examples from `references/examples/client-ros-examples.md` as quality anchors for the Create phase.

## Create

What is?
The create branch - populates the tokenized ROS Template with the 12 firm-specific values and builds the Entity Checklist, producing a schema-valid `client-ros-data.json` plus its markdown source and metadata.

**Best Practices.**
These apply to the entire create phase and should be checked after each step.

- Populate only - never restructure the upstream ROS Template (see `### Editorial Guidelines -> Guideline 2`).
- Only the 12 approved placeholders are filled; resolve every one (Editorial Guideline 1).
- Hold the scope-matched calibration examples in view while populating - calibrate bold preservation, acronym handling, and entity underline retention against them.
- Document structure, formatting, and the Entity Checklist shape follow `### Quality bar` and `### Editorial Guidelines` - do not restate the thresholds, apply them.

If the model generates output that violates any of these, emit a `> NEEDS VERIFICATION:` block at the offending location instead of shipping the claim.

### Populate placeholders

What is?
The pass that fills every `{{PLACEHOLDER}}` with the resolved firm value, preserving the template's bold / italic / underline formatting and applying the episode-goal selection rule.

- For each of the 12 placeholders, replace `{{PLACEHOLDER}}` with the resolved value per Editorial Guideline 1. Preserve the `**bold**` around it - populated values stay bold.
- Apply the populate rules: `{{CITY}}` = the episode's **Episode geo target** city (the city THIS episode is built to rank for, not necessarily the show anchor), empty only when that target is state-level; `{{STATE}}` converted to the full name; `{{PRACTICE_AREA}}` lowercase plural; `{{EPISODE_NUMBER}}` integer only.
- Underline the populated `{{ATTORNEY_NAME}}`, `{{FIRM_NAME}}`, and `{{PODCAST_NAME}}` every time they appear, as pandoc `[entity]{.underline}`. Convert any legacy `<u>entity</u>` tag to `[entity]{.underline}`.
- Apply the episode-goal selection rule per Editorial Guideline 3 - layer in the populate-time slice that serves this episode's goal.
- Do NOT restructure the document - populate in place per Editorial Guideline 2.
- After populate, scan the entire text for any remaining `{{...}}` patterns. If any are found, list them and do not proceed - this is a hard gate.

### Build the Entity Checklist

What is?
The pass that builds the Entity Checklist tally table at the bottom of the Client ROS - one row per Tier 1 + Tier 2 entity from the matching-scope entity map, with question references and target-mention ranges.

- Build the Entity Checklist per Editorial Guideline 4 - 4 columns (Entity / Questions / Target Mentions / Actual Mentions), placed after `*End of Run of Show*`.
- Pull each entity's question references directly from the populated script - do not guess. Compute the Target Mentions range from the question count per the heuristic in Editorial Guideline 4.
- Wrap every entity in pandoc `[entity]{.underline}`. The firm / attorney / podcast name do NOT go in this table.
- The table ends the file - no Appendix material after it.

### Render markdown and payload

What is?
The pass that assembles the final artifacts - the Client ROS `.md` source-of-truth with the `## INTERNAL` block, the `client-ros-data.json` machine-readable payload, and `metadata.json`.

- Assemble the Client ROS `.md` - the populated body in the locked structure per Editorial Guideline 2, the Entity Checklist table, then the `## INTERNAL` block (see `## INTERNAL`).
- Serialize `client-ros-data.json` per `### Outputs -> #### Schema` - all 12 resolved values, segments, questions, durations, the Entity Checklist rows, the episode goal.
- Write `metadata.json` with the provenance block per `## INTERNAL` - data sources, the resolved 12 values, episode goal, template scope, references status, run timestamp.

## Update

What is?
The update path - modifies an existing Client ROS in place when a prior version exists, preserving any manual edits the producer made since the last skill run.

**Best Practices.**
These apply to the entire update phase and should be checked after each step.

- **Diff before write.** Pull the existing `client-ros-data.json` + Client ROS `.md`, compare against the proposed new state, surface every changed value / segment before committing the write.
- **Preserve manual edits.** Any populated value, attorney bullet, setup line, or Entity Checklist row that was manually edited since the last skill run keeps its current value. The skill never auto-overwrites a manual edit silently.
- **Flag merge conflicts inline.** When a new auto-generated value disagrees with a preserved manual edit, emit `> NEEDS VERIFICATION: auto-generated value [X] conflicts with manual edit [Y]` at the location; the producer resolves.
- **Stable fileId.** Update uses `files.update` against the existing `Client ROS` Google Doc fileId. Never create a new Doc; never delete-and-recreate. URL stability is part of the Update contract.

If the model proposes overwriting a manual edit without flagging it, halt and emit `> NEEDS VERIFICATION:` instead of shipping the change.

### Diff against existing

What is?
The pass that loads the prior Client ROS and computes a value-level and question-level diff against the proposed new state so nothing changes silently.

- Read the prior `client-ros-data.json`, Client ROS `.md`, and `metadata.json` from the resolved `Client ROS:` slot.
- Read the prior `metadata.json` provenance block to recover the last run's data sources, the resolved 12 values, and episode goal.
- Run the Create-phase passes (`### Populate placeholders` through `### Build the Entity Checklist`) to compute the proposed new state.
- Compute the diff: placeholder values changed, questions added / removed / changed, Entity Checklist rows changed, and pieces untouched.

### Merge and resolve conflicts

What is?
The pass that merges the new populate into the existing Client ROS - new values in, stale content out, manual edits preserved, conflicts flagged for the producer.

- Apply the phase-level Best Practices: preserve every manually-edited piece; merge new auto-generated values and questions; drop content the new template retired.
- Where a new auto-generated value disagrees with a preserved manual edit, emit the `> NEEDS VERIFICATION:` conflict block inline; do not auto-resolve.
- Re-render the Client ROS `.md`, `client-ros-data.json`, and `metadata.json` per `### Render markdown and payload`. Bump the `metadata.json` run date and append the run to the provenance history.
- The shared `## Quality Assurance` phase runs after this phase - QA does not re-run inside Update.

## Quality Assurance

What is?
The gate before `## Ship` - a three-tier check (Best Practices by name, the hardwired Anti-AI Detection two-pass scan, then skill-specific mechanical checks) that runs after whichever branch fired (`## Create` or `## Update`).

**First - check against Best Practices.** The deliverable must align with the contract defined upstream in this file. This is always the first gate; skill-specific checks come after.

- **Quality bar** (Best Practices -> Quality bar) - all 12 placeholders resolved, bold preserved, document structure matches the upstream template, Entity Checklist present, branded Google Doc, no em dashes / banned vocabulary.
- **Sourcing discipline** (Best Practices -> Sourcing discipline) - every populate value Confirmed; any Inferred default flagged `> INFERRED:`; any unresolvable value flagged `> NEEDS CONFIRMATION:`. No silent synthesis.
- **Editorial Guidelines** (Best Practices -> Editorial Guidelines) - Guideline 1 (12 placeholders all filled), Guideline 2 (formatting + structure preserved), Guideline 3 (episode-goal populate slice), Guideline 4 (Entity Checklist at the bottom), Guideline 5 (localized entities at Location/Extension scope).
- **Quality gates** (Best Practices -> Quality gates) - full checklist must pass: placeholder gate, document structure, question cap, Entity Checklist, jurisdiction consistency, branded render, schema validate, provenance present, artifacts present, no em dashes.

**Second - Anti-AI Detection two-pass scan** (canonical doc: https://docs.google.com/document/d/1hp7bxOFRlMhCuhjHNY0j05JrB97-KOFD0XUCQM3gMBU/edit). Mandatory for every text-producing skill. Run the full Section 7 two-pass audit against the deliverable:

- **Pass 1 (mechanical scan):** em-dashes, banned vocabulary (Section 2), banned phrases (Section 3), triadic rhythms and symmetric paragraphs (Section 4), summary-only section closers, date formatting per destination, specific-claims-trace-to-source, no emojis (unless requested), no clickbait.
- **Pass 2 (skeptical re-read):** restart from the top. Did I actually check every line, or skim? Em-dashes I missed? Banned phrases I rationalized? Triadic rhythms left because they "sounded fine"? Generic setup text that should be specific? Am I sure?
- **On any hit:** fix and re-run Pass 2 until clean. One pass is not enough.

**Third - skill-specific mechanical checks.**

- `client-ros-data.json` validates against the canonical schema `references/schema/client-ros.json`. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed.
- All 12 approved placeholders resolved; ZERO leftover `{{...}}` anywhere in the populated output (grep explicitly). Bold preserved around each populated value.
- Document structure matches the upstream ROS Template: H1 once; metadata block with all five canonical lines; Producer Notes (brief); Introduction (exactly 3 `*[Co-Host]*` paragraphs + transition, zero `*[Attorney Response]*`); strict question blocks; no post-response co-host text between questions; Closing/CTA with populated phone + website both bold; `*End of Run of Show*`. No "Formatting Guide" section, no inline Appendix.
- Main-body `### Q{N}:` count is 20 or fewer (Full episode) or 10-12 (Extension/Mini). The Client ROS is the trimmed selected set ONLY - grep confirms ZERO `## Additional Questions (Optional Pull)` heading in the populated output (that reserve is INTERNAL to the ROS Template; it must never reach the client-facing Client ROS).
- Entity Checklist table present at the very bottom, after `*End of Run of Show*`, 4 columns; entities wrapped `[entity]{.underline}`; the table ends the file.
- Zero leaked pandoc inline-attribute markup as visible text in the rendered Doc (`[...]{.underline}`, `<u>`, `</u>`, `{.underline}`, `{.smallcaps}`, `{.mark}`). Zero legacy `<u>...</u>` HTML tags.
- Jurisdiction consistency: every entity reference uses the localized form at Location/Extension scope; statute citations and court names internally consistent (an extension matches its parent anchor).
- The branded Google Doc was built from `build-client-ros-docx.py` - cover page, CE logo, "Run of Show" title, firm-name subtitle, "Prepared by Case Engine" + date footer, Roboto body.
- `metadata.json` provenance block present with at minimum: data sources (podcast-overview path / user-provided), the resolved 12 values, `episode_goal`, template scope, `references_status`, run timestamp.
- Filename follows the canonical pattern `E{N}: {Episode Title} // {Firm Name} // Client ROS - {Location}` (append ` (Extension)` for extension cells).
- Both write destinations verified: confirm the Drive `Client ROS:` slot AND the local mirror contain the same artifacts (markdown, `.docx` locally + Google Doc remotely, JSON, metadata).
- INTERNAL section grep test: `grep -L "## INTERNAL" {client-facing-export}` returns zero hits for the client-facing Google Doc.

**On failure:** fix the markdown, regenerate `client-ros-data.json` and `metadata.json`, rebuild the DOCX, re-upload via `files.update`, re-run all checks. Do not proceed to `## Ship` until QA returns clean.

## Ship

What is?
The publish phase - builds the CE-branded DOCX, writes the trio plus `metadata.json` to the firm's `Client ROS:` slot per Map 6, and mirrors the same artifacts to the local Desktop path.

### What ships

- **Client ROS** - Google Doc - human-facing CE-branded view, cover page, Roboto typeface, real underlined entity runs, stable fileId.
- **Client ROS `.md`** - Markdown - raw populated source-of-truth, retains the `## INTERNAL` block.
- **`client-ros-data.json`** - JSON - machine-readable payload, all 12 placeholders resolved.
- **`metadata.json`** - JSON (internal) - provenance: data sources, the resolved 12 values, episode goal, template scope.

### Where it ships

- **Drive:** the cell's `Client ROS:` slot per Map 6 - `Episodes/EP{N}: {episode_name} // {client_name}/Run of Show: {episode_name} // {client_name}/Client ROS: {episode_name} // {client_name}/`. This destination is fixed - the skill does not move existing Drive data.
- **Local mirror:** `~/Desktop/claude_code/deliverables/podcast/Client ROS/{Topic}/{Episode}/{scope}/` - written every run.
- **Schema:** `~/.claude/skills/pod-3B-client-ros/references/schema/client-ros.json`.

### How it ships

Write to both destinations. On a write error to one, ship to the other and report the partial state.

- **Build the CE-branded DOCX.** The human-facing Google Doc MUST be the branded DOCX→Doc, never a raw markdown→Doc upload (the latter leaks `[entity]{.underline}` markup and has no cover page). Run `scripts/build-client-ros-docx.py` to emit both the `.docx` and the paired `.md` in one pass. The script reads `client-ros-data.json`, translates pandoc `[entity]{.underline}` into a real Word underline run in the DOCX (and to plain `text` in the paired `.md`), applies CE branding per the Case Engine Branding folder (Roboto throughout - if the branding folder still says Calibri, Roboto wins), and emits both files. Never includes the legacy "Internal Setup" checklist.
- **Cover page.** Render per the canonical [Cover Page Spec](https://docs.google.com/document/d/1oydpI055jbj1FYDGeZfHQeMNjaWKUCFVGCRveeuJJCk/edit), with one override - the body and cover-page font is Roboto. Title `Run of Show` (CE Blue, 36pt, bold, Roboto). Subtitle is the firm name (e.g., `Spaulding Injury Law`) - the Client ROS is the host's branded show script, so the firm leads the cover; never omit it. Scope / Topic line carries the episode topic + location. Footer `Case Engine  |  Confidential  |  Page {PAGE}` auto-applied via the Drive API template.
- **Canonical styling** - Title styled as Google Docs "Title" (36pt, bold, dark #0f172a, Roboto); H2 as "Heading 1" (16pt, bold, CE Blue #3573FF, Roboto); H3 as "Heading 2" (13pt, bold, dark, Roboto); H4 as "Heading 3" (11pt, bold, dark, Roboto); body Roboto 11pt dark. Entities are real underlined runs in the DOCX, never literal `[...]{.underline}` text.
- **Drive write.** Upload the `.docx` as `application/vnd.google-apps.document` so Drive auto-converts it to a clean branded Google Doc (the human-facing artifact). Upload the `.md` as `text/markdown` (no conversion - raw source for downstream readers). Upload `client-ros-data.json` + `metadata.json` as-is. First-time create uses `files.create`; subsequent writes use `files.update` against the existing fileId (preserves the URL). Never re-upload the `.md` with `convert=true` to make a second Google Doc - that is the leaky path.
- **Roboto pass.** After the base Doc is uploaded, confirm Roboto over the full document range. Override only when a per-client `brand.json` typography block specifies otherwise.
- **Archive.** If the existence check moved a prior Client ROS file to `_archive-{YYYY-MM-DD}/`, the archive folder ships alongside the new artifacts. Archive ONLY the prior Client ROS file - the Client Guide sibling in `Client Guide:` is untouched, and the tokenized ROS Template in the shared template library is read-only (never archived by this skill).
- **Local mirror write.** Write the same Client ROS `.md`, the CE-branded `.docx`, `client-ros-data.json`, and `metadata.json` to the local mirror path. The mirror keeps the DOCX, not the auto-converted Google Doc. If the Drive write fails but the local write succeeds, surface the partial state in the report - do not silently swallow it.
- **Report back:**

  ```
  Done. Client ROS populated for {Firm} - {Episode} ({Location}).

   Folder: https://drive.google.com/drive/folders/{folder_id}
   Client ROS (branded Google Doc): https://docs.google.com/document/d/{doc_id}

  Placeholders populated: 12/12. Episode goal: {goal}. QA gate: PASS.

  Next: /pod-3C-client-guide (Phase 3 Run of Show) reads this Client ROS and produces the attorney-facing prep doc into the cell's Client Guide slot. Then AM reviews + sends to {Attorney} for pre-recording prep.
  ```

### Who to Notify

`notify: []` - this skill posts no notifications. The producer is informed via the inline report-back above.

---

## INTERNAL (not for client distribution - auto-stripped from all exports; the worked examples ride into the local markdown only, never into the Drive Doc)

### Document structure reference

The Client ROS inherits the canonical document structure from `pod-3A-ros-template` and fills placeholders in place - it does NOT restructure. The authoritative source of the shape is `pod-3A-ros-template/SKILL.md -> ### Editorial Guidelines -> Guideline 4`. Internal calibration only; never appears in the client-facing Doc.

### Provenance block

`metadata.json` must include a provenance block with at minimum: `run_date`, data sources (podcast-overview path or user-provided), the resolved 12 placeholder values, `episode_goal`, `template_scope`, `references_status` (used / empty), `schema_status` (validated / missing), and Drive fileIds (canonical).

### Source inventory

Records every input the run consumed: the resolved ROS Template path, the `entity-map.json` path when used, the user-supplied firm data, the podcast-overview doc path, and the calibration examples used (bundled file or methodology fallback).

---

## Learning & Iteration

- [ ] After each run, note edge cases, placeholder-resolution gaps, jurisdiction-consistency failures, and Entity Checklist drift; append GOOD / BAD / EDGE CASE entries to `references/examples/client-ros-examples.md`.
- [ ] Track recurring missing firm fields - if the same field keeps needing a manual prompt, note it so the podcast-overview doc can capture it up front.
- [ ] Watch for Client ROS docs shipping more than 20 main-body questions; if it recurs, confirm the upstream ROS Template is honoring the question cap.

## Change Log

| Date | Change |
|---|---|
| 2026-07-10 | **Canonical three-field geo model alignment (Gabe directive, Whalen scoping).** Stamped the canonical geo model across this skill: (1) **Targeting strategy** (single-location vs multi-location, drives episode format), (2) **Optimization scope (show anchor)** (City/State/County/Regional, what the show as a whole optimizes for), (3) **Episode geo target** (the specific city THIS episode ranks for, fills the location token). Reworked Greeting Q2 (anchor scope → "Optimization scope (show anchor)"), Q3 (extensions → "Targeting strategy" + extensions), Q4 (this run's scope → "Episode geo target"). Added the three-field model + the "Anchor scope != per-episode target" rule as the lead bullet of Editorial Guideline 6 (the cross-cutting geo rule), making explicit this skill fills `{{CITY}}`/location with the Episode geo target city, not necessarily the show anchor. Sharpened Editorial Guideline 1 populate rules and the `## Create → ### Populate placeholders` SOP step to the same. Bumped schema `client-ros.json` 1.0 → 1.1 (scope/location descriptions retargeted to Episode geo target; no field added/renamed/reordered). Preserved the no-city-quota ceiling-not-floor principle unchanged. Revert: restore "Podcast anchor scope"/"This run's scope" Greeting wording, drop the Guideline 6 three-field lead bullet and the Guideline 1 / SOP Episode-geo-target clauses, and revert schema to 1.0. |
| 2026-06-17 | **Tokenized Template ROS lives ONLY in the shared library; client folder holds only the Client ROS.** Confirmed/encoded the convention: the Client ROS is the firm-specific deliverable that lives in the client episode `Run of Show/Client ROS/` slot (Map 6), and the tokenized Template ROS this skill populates from is NOT in the client folder - it lives ONLY in the shared template library (`Episode Templates/{Topic}/{scope}/`, Map 2). Added the explicit note to `### What is`; rewired every upstream-read reference (Greeting Q7, Inputs Required, Capabilities, Handoff Contract, Gotcha, Verify-upstream gate, Prepare Inputs) from the old per-cell `Template ROS:` slot to the shared library; dropped the read-only `Template ROS:` slot from the Drive-destination file-tree (the client `Run of Show/` now contains only `Client ROS:`); updated the archive/Ship notes that referenced a `Template ROS:` sibling. Pairs with the pod-4A revert (4A now writes the template only to the shared library). No change to placeholders, populate logic, output structure, or schema. Revert: restore the per-cell `Template ROS:` slot as the read source in all the above and re-add it to the file-tree. |
| 2026-06-17 | **Client ROS = client-facing TRIMMED, NO Additional Questions reserve (resolved a self-contradiction).** The `### Quality gates -> Question cap` line wrongly said the `## Additional Questions (Optional Pull)` overflow was "carried over from the ROS Template" into the Client ROS, contradicting both the EXCLUDED-sections rule and the Editorial Guideline 2 "Banned: an inline Appendix in the populated Client ROS." Resolved unambiguously in favor of CLIENT-FACING = TRIMMED: the Client ROS ships the main selected set ONLY and MUST NOT include `## Additional Questions (Optional Pull)` - that reserve is INTERNAL and lives ONLY in the ROS Template (pod-4A). Rewrote the Question cap gate (now "trimmed, no reserve"; a stray Additional Questions heading FAILS and is stripped before ship), added a grep-for-zero check in the third-tier QA mechanical checks, named the section explicitly in the EXCLUDED-sections list and the Guideline 2 Banned list, and added a client-facing-trimmed clause to `### Framing`. No change to placeholders, structure, schema, or chain. Revert: restore "overflow lives in `## Additional Questions (Optional Pull)` ... carried over from the ROS Template" wording and drop the new exclusion clauses + grep check. |
| 2026-06-17 | **Sequential numbering gate (Sutliff E8 gappy-numbering fix).** Added a VERIFY-and-refuse Sequential numbering gate to `### Quality gates`: the host-facing `### Q{N}:` labels must run sequential 1..N with no gaps and no number exceeding the question count. Sutliff E8 shipped 20 questions labeled up to Q30 (Q1-10, 12, 14, 15, 16, 17, 21, 22, 24, 25, 30 - the raw n-gram bank index leaked into the host script) and read as "numbered weird" to the client. Because this skill is populate-only and must not restructure, the gate fails and routes back to `/pod-3A-ros-template` to renumber (4A is the lock point) - it never silently renumbers in 4B. Added a cross-reference in Editorial Guideline 2 noting the `### Q{N}:` labels are clean sequential 1..N, never the n-gram bank index. Revert: remove the Sequential numbering gate bullet and the Guideline 2 cross-reference clause. |
| 2026-06-17 | **Guideline 6 resynced to pod-3B balanced rule (Eberst multi-location).** Guideline 6 + its quality check replaced the stale 60-70% BANDED-FLOOR language (which contradicted pod-3B) with pod-3B's converged rule: natural placement, no city quota, city in roughly a THIRD of lines, two-sided guard (>half FAILS as spam, essentially-absent FAILS as too thin), NO floor. The two skills' geo rules are now identical by design. Row count stays 10-12. Revert: restore the 60-70% banded-floor Guideline 6. |
| 2026-06-16 | **City-token cap (Eberst E2/E3 spam fix).** Guideline 6 + its quality check changed from "city is the default anchor / exceed county" (a maximize rule that drove city tokens to 100% of lines) to a BANDED rule: city named in roughly 60-70% of question lines, floor = exceed county, ceiling = not every line (>85% FAILS as spam). Added explicit ban on the adjective-spam construction ("Stuart claimant/crash/drivers"); required at least one state-law line to name the state and the state-law layer to be visibly woven through. Revert: restore the single "exceed county" check and the "default geo anchor / good percentage" wording. |
| 2026-06-12 | **Geo hierarchy + targeting-strategy branch (Mohink run).** Added Editorial Guideline 6 (geo hierarchy in the script: city-first, county earned, state for law; lighter on county when forced) with the city-share quality check. Extension definition updated for the multi-location Mini model (10-12 questions, ~30-35 min, no anchor episode, one Mini per target city, cross-city no-verbatim rule); question cap ~10 -> 10-12. Document template/formatting/placeholders and chain order UNCHANGED. Revert: remove Guideline 6, restore Extension definition + ~10 caps. |
| 2026-04-20 | Initial co-work version. Drive-native. Restructured to the canonical pattern - Best Practices contract H3s, conversational Greeting, Inputs contract table, Examples + Routing under Output. Step 3 of the Run of Show workflow. |
| 2026-04-20 | Moved YAML frontmatter to the top of the file in bare `---` delimiters. Owner set to Gabe Jordan. Migrated to canonical CE ROS formatting - `{{HOST_NAME}}` rename, pandoc `[entity]{.underline}` convention, full metadata block, strict question block format. Added Handoff Contract + SOP Handoff Contract check. Scaffolded `_references/` folder. |
| 2026-04-21 | DOCX layer reworked - client-facing artifacts render as branded Google Docs built from a CE-branded DOCX. Added `pod-` prefix for producer discoverability. |
| 2026-04-24 | Reverted `pod-` prefix across cowork skills. |
| 2026-05-12 | Reads the ROS Template from the firm's episode folder; removed the Locations→Extensions→Topic Only Drive-tree resolution order. Fixed the Client-Guide dependency-direction bug - the Client Guide is produced DOWNSTREAM, not a precondition. This skill produces ONLY the Client ROS. Branded DOCX→Doc made mandatory. Roboto replaces Calibri. Mandatory QA gate added. |
| 2026-05-14 | **v2.0.0** - Merged cowork client-ros v1.0 (canonical content) with original local pod-8-client-ros (Mode A enrichments). Steps 15/16 (show-notes-draft + chapter-titles inline) retired - their logic moved to the Post-Production Pack. Output schema identical across modes. Bundled scripts + schemas + examples + iteration-log moved into canonical layout. |
| 2026-05-15 | Aligned Drive read + write paths to Client Folder Structure v2.4.0 → Map 6 - reads the ROS Template from the cell's `Template ROS:` slot, writes the Client ROS into the sibling `Client ROS:` slot. Legacy compatibility paragraph added. |
| 2026-05-20 | **v3.0.0** - Full structural refactor to the canonical CE skill structure. Renamed `pod-8-client-ros` -> `pod-3B-client-ros`; description, trigger, and all sibling refs repointed to the new pipeline codes (1A/1B/1C/2A/2B/4A/4C/4D). Removed the entire Mode A/B detection probe and all capability-probing apparatus - this skill runs locally in Claude Code, calls its tools directly, skips or fails on a tool error. Frontmatter completed (skill_kind, modes: multi, inputs, outputs, notify; version/date/owner moved to a metadata block). Best Practices restructured to the canonical contract H3s (Inputs / Outputs / Framing / Quality bar / Sourcing discipline / Editorial Guidelines / Quality gates / Gotchas / Iteration log); the placeholder taxonomy, formatting-preservation rules, research-palette rule, Entity Checklist spec, and localization rule relocated into Editorial Guidelines, Quality bar, and Quality gates. The reference-only Client Guide spec block removed - that spec lives at `pod-3C-client-guide`. SOP rebuilt as H2 phase siblings (Checks / Prepare Inputs / Create / Update / Quality Assurance / Ship). Universal State Check logic moved into the Existence check + `## Update`. `## Workflow` demoted to `### Workflow` H3 carrying the unified 4-phase pipeline diagram. `## Output` folded into Best Practices Outputs. `## Push to Drive` renamed `## Ship` with the canonical H3 sub-structure. QA rewritten as the canonical three-tier gate with the hardwired Anti-AI Detection two-pass scan and an On-failure recovery line. Mode A/B local-mirror writes made unconditional. `references/schemas/` normalized to `references/schema/`. Old `## Appendix`-style content moved to the `## INTERNAL` two-tier model. Owner Gabe Jordan. |
| 2026-07-31 | v3.3.0 - removed the `pod-1-podcast-bible` dependency, all Fortress (`fortress-db` / `crm_clients`) access, and the ClickUp CRM path ahead of the skill moving to an environment without CE infra. Firm identity fields (FIRM_NAME / ATTORNEY_NAME / ATTORNEY_FIRST_NAME / PHONE_NUMBER / WEBSITE) are now required user inputs, auto-filled from the podcast-overview doc when it carries them - no DB or CRM lookup. Stripped all podcast-bible references (Phase 1 box + note, prereq sentence, routing bullet), repointed the auto-read source / tools / Sourcing discipline / Gotchas / Resolve-values SOP step / provenance block / source inventory to user input + podcast-overview, and removed the vestigial "no numbered lists in ClickUp" QA clause. Frontmatter input fortress-db-row -> user-supplied-firm-data. Historical iteration-log entries left intact (append-only). | Gabe Jordan |
