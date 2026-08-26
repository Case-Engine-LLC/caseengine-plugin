---
name: pod-3A-ros-template-v2
description: >
  Build the tokenized, generic Run of Show template in the NEW v2 format -
  Segment 1 is one credential-led prompt and a 15 to 30 minute open interview,
  Segment 2 is per-city short-form blocks of 60-second questions carried verbatim from the n-gram table - the best 8-10 per location in the body plus the rest as a Question Pool with bullets.
  12 approved `{{PLACEHOLDERS}}` so one template serves every firm that records
  at that scope. Use whenever someone says "v2 ros template for [episode]",
  "new format ros for [topic]", "open interview ros [episode]", "short-form
  blocks ros", or "/pod-3A-ros-template-v2". Phase 3 Run of Show of the podcast
  pipeline; hard dependency on a matching-scope n-gram table and entity map;
  feeds pod-3B-client-ros-v2 downstream, which is the final step of the v2 branch. The LEGACY
  four-segment format stays on `pod-3A-ros-template` - both coexist behind the
  `episode_format` flag and this skill never runs unless that flag says v2.
skill_kind: hybrid
modes: multi
inputs: [n-gram-table.json, entity-map.json, entity-clusters.md, keyword-research.json, attribute-research.json, podcast-overview.md, case-engine-branding]
outputs: [json, markdown, gdoc]
notify: []
metadata:
  version: 1.7.0
  date: 2026-08-18
  owner: Gabe Jordan
  version_history: >
    1.0.0 - initial v2 format skill (2026-08-14). Forked in structure (not in
    content) from pod-3A-ros-template v3.2.0. Format decided on the Gabe/Cyle
    call 2026-08-14: single credential-led prompt + open interview for Segment
    1, per-city short-form search-phrase blocks for Segment 2, attributes
    replacing statute bullets, geo pairing replacing the city-share ceiling.
    Legacy skill left untouched and remains the default. 1.1.0 - format locked
    2026-08-14 against the live doc and reference implementation: cover page,
    S1/S2 naming, merged Introduction, Internal Notes below the divider, ten-question
    Short-Form cap, 2 STATIC constants, removed-section gate.
---

# ROS Template v2

> **Drive write governance:** All Drive operations (create, update, rename, move) follow [Ship]. Revise in place via `files.update` against the existing fileId, never delete-and-reupload (breaks the fileId/URL chain and silently kills every downstream reference).

> **FORMAT LOCKED 2026-08-14. STILL A DRAFT FOR SHIP PURPOSES.** The document shape in `### Editorial Guidelines -> Guideline 4` is final and matches the live prototype doc `1Bv-EWc7HBtKqc09XEfQnBIfSOdm6m4Tc-kJNw5uKErk` exactly. **All four downstream blockers cleared 2026-08-18** (see `### Gotchas` - `pod-3B-client-ros-v2` and `pod-3C-client-guide-v2` were built as siblings; the other two were verified false alarms). What is still open: nothing has been written to Drive and this skill is not registered in the Templates [Master] Structure doc - first Drive write is Gabe's call.

> **Coexistence gate (read this first).** This skill ONLY runs when the client's `episode_format` resolves to `v2-open-interview`. The default is `legacy-segments`, which routes to `pod-3A-ros-template`. See `### Framing -> Episode format flag`. Do not run this skill on a client whose format has not been explicitly flipped, and never edit, migrate, or "upgrade" an existing legacy template with it.

### What is

A tokenized, generic Case Engine podcast Run of Show template in the **v2 format** - the format decided on the Gabe/Cyle call of 2026-08-14. It replaces the legacy four-segment, twenty-question interrogation script with two segments that are recorded differently on purpose:

- **Segment 1 - The Interview (15 to 30 minutes).** A four-line introduction - the static welcome, a generated setup, a generated credential that establishes authority, and ONE prompt - and then the attorney talks. No agenda. No question list. The interviewer's job after the prompt is to stay out of the way and fill gaps only.
- **S2: Short-Form (60-90s), per location.** Exactly ten questions per location, 60 to 90 second answers, higher energy, each one self-contained because each one gets clipped. Questions are built on search phrases, not legal elements.

Like the legacy skill, the template uses `{{PLACEHOLDERS}}` everywhere client-specific data will eventually go, so one template is reusable across every firm that records that episode at that scope. It lands in the shared template library at every scope - `Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/` per Map 2 - and NEVER in a client/firm episode folder. Downstream, `pod-3B-client-ros-v2` populates the placeholders and writes the firm-specific Client ROS v2 into the client episode folder.

**The ROS Template is INTERNAL - the client never sees it.** In v2 that matters differently than it did in the legacy format. The legacy template carried the entire n-gram bank because the n-gram questions WERE the script. In v2 the n-gram bank is no longer the script: Segment 1 has one prompt, and Segment 2's questions are rebuilt around search phrasing and attributes rather than lifted verbatim. The full n-gram bank still ships, verbatim and unedited, in `# Appendix: Source Question Bank` - as the audit trail that nothing was silently dropped or invented, and as the live pull pool if a client rejects a Segment 2 question. See `### Editorial Guidelines -> Guideline 5`.

**What actually changed from legacy, in one line each.** One prompt instead of twenty questions. Attributes instead of statute bullets. Search phrases instead of legal elements. City-plus-region pairing instead of a city-share percentage ceiling. Its own eleven-token taxonomy, which adds `{{YEARS_PRACTICING}}` and is not a superset of legacy's.

### Workflow

ROS Template v2 is the first step of **Phase 3 (Run of Show)** of the podcast pipeline, in the v2 branch. Per-episode, per-scope. Hard dependency on a matching-scope N-Gram Table (`pod-2B-n-gram-table`) and a matching-scope entity map (`pod-1A-entity-research`). Optional dependency on `pod-1D-attribute-research` for the attribute set.

```
PHASE 1: RESEARCH  (one in-tandem pass - Topic Only + Topic+Location)
┌─ 1A ──────────┐ ┌─ 1B ──────────┐ ┌─ 1C ──────────┐ ┌─ 1D ──────────┐
│ Entity        │ │ Keyword       │ │ Virality      │ │ Attribute     │
│ Research      │ │ Research      │ │ Research      │ │ Research      │
└───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘
        │                                               (optional, v2 only)
PHASE 2: PLANNING
┌─ 2A ──────────┐ ┌─ 2B ──────────┐
│ Topic Planner │ │ N-Gram Table  │
└───────────────┘ └───────────────┘
        │
PHASE 3: RUN OF SHOW  (per prioritized episode)
        │
        ├── episode_format = legacy-segments (DEFAULT) ──> pod-3A-ros-template
        │
        └── episode_format = v2-open-interview ─────────> pod-3A-ros-template-v2
                                                            ◄── YOU ARE HERE
                    │
        ┌─ 3B ──────────┐ ┌─ 3C ──────────┐
        │ Client ROS    │ │ Client Guide  │
        └───────────────┘ └───────────────┘
```

Notes:

- **Phase 1 Research** - `pod-1A-entity-research`, `pod-1B-keyword-research`, and `pod-1C-virality-research` run together as one research pass, ONCE per practice area + location cascade. `pod-1D-attribute-research` is the v2-only addition and is OPTIONAL - when absent, the static fallback list in `references/attributes/attributes-fallback.json` is used.
- **Phase 2 Planning** - `pod-2A-topic-planner` ranks episodes; `pod-2B-n-gram-table` builds the collation table for one episode at one scope. Both are upstream of this skill and are UNCHANGED by v2 - the same n-gram table feeds either format.
- **Phase 3 Run of Show** - the format flag picks the branch, and each branch has its own full chain: legacy feeds `pod-3B-client-ros` -> `pod-3C-client-guide`; v2 feeds `pod-3B-client-ros-v2` -> `pod-3C-client-guide-v2` (built 2026-08-18, resolving the former downstream blockers - see `### Gotchas`).

Prerequisites: a matching-scope N-Gram Table from `/pod-2B-n-gram-table` and a matching-scope entity map from `/pod-1A-entity-research` are hard dependencies - this skill will not run without both.

> **Episode 1 - Founder Story is a HARDCODED exception and is NOT in the v2 format.** Episode 1 of every client's show is the Founder Story interview. It uses the fixed pre-built template at `templates [master]/AEO Templates/Podcast/Episode Templates/Founder Story/` regardless of the client's `episode_format`. If the requested episode is Episode 1, stop and route to `pod-3B-client-ros`. Do not v2-ify the Founder Story template.

### Trigger phrases

- `/pod-3A-ros-template-v2`
- "v2 ros template for [episode]"
- "new format ros for [topic]"
- "open interview ros [episode]"
- "short-form blocks ros for [episode]"
- "single prompt ros [episode]"
- "ros v2 for [topic] in [location]"

### Greeting

Hi, I'm ROS Template v2. Before I run, I need to confirm the format flag and the podcast architecture. If podcast-overview has been run for this client, I'll read it and confirm in one line. If not, I'll ask:

1. **Episode format confirmation (FIRST, blocking).** Is this episode running the **v2 open-interview format** (single credential-led prompt + a 15-30 minute open interview, then per-city short-form blocks) or the **legacy segmented format** (four segments, ~20 questions, statute-grounded attorney bullets)? Answer `v2-open-interview` or `legacy-segments`. **The default is `legacy-segments`** - if you are not sure, or nobody has explicitly signed this client off on v2, the answer is legacy and I stop and route you to `/pod-3A-ros-template`. I will not build v2 on an unconfirmed answer. This is a per-show decision, not a per-episode one: confirm it once with whoever owns the client, then it holds for the whole library.
   > **Temporary manual ask.** This used to resolve automatically from a per-client architecture doc. Until the format flag is wired into a database, it is a question asked at run time. Record the answer and who gave it.

2. **Client name.** Examples: "The May Firm", "Sutliff & Stout", "Conn Law Firm". Exact firm name as it appears in Drive. (Not needed at Topic Only scope - the base template has no firm.)

3. **Optimization scope (show anchor) - what the podcast as a whole is optimized to rank for.** This is the show-wide anchor, NOT the per-episode target (see `### Framing -> Geo model`). City / State / County / Regional:
   - **City-level:** people in your market search the city as a unit ("Houston car accident lawyer"). Show anchor: Houston.
   - **State-level:** people search the state as one unit ("California car accident lawyer"). Show anchor: California; each episode still targets its own city.
   - **County / regional-level:** people search the region ("Inland Empire injury attorney", "Harris County", "Bay Area"). Show anchor: the region/county; cities within become individual Episode geo targets.

4. **Extension locations (if any).** In v2 these are usually not separate episodes at all - they become additional Segment 2 city blocks inside the same episode. I ask which cities get their own Segment 2 block, and whether any city needs a standalone episode. See `### Framing -> What extensions become in v2`.

5. **This run's scope** - Topic Only, an anchor location, or a specific extension? At Location/Extension scope, the location I resolve is this episode's **Episode geo target**.

6. **The region for the geo pairing.** Segment 2 pairs the city with its surrounding region ("in Fresno and across the Central Valley"). The region is fixed by this template's location scope, so it is PLAIN TEXT, not a placeholder. I need the exact phrasing you want spoken. If podcast-overview carries it, I confirm it in one line; if not, I propose one and ask you to confirm.

7. **Short-Form location list.** Which locations get a set. Every set is exactly ten questions - that is a hard cap, not a choice. Across sets the three city-tagged questions change and the seven attribute questions mostly carry over.

8. **Episode goal** - what is this specific episode trying to accomplish? Authority / education, Lead generation, Differentiation, Narrative / story, or Conversion (see `### Editorial Guidelines -> Guideline 2`). If unspecified I default to Authority.

Then my skill-specific follow-ups:

9. **Attribute source.** Is there a `pod-1D-attribute-research` output for this practice area + market? If yes I use it and record the pull date. If no I use the static fallback in `references/attributes/attributes-fallback.json` (pulled 2026-08-14) and flag it `> INFERRED:` with the pull date, so a stale attribute set is visible rather than silent.
10. **Scope folder (shared library, every scope):** does the scope folder exist under `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/`? If not, I create the chain.
11. Does the matching-scope N-Gram Table exist (`/pod-2B-n-gram-table` output)?
12. Does the matching-scope entity map exist (`/pod-1A-entity-research` output)?
13. **N-Gram Table <-> Topic Plan reconciliation** - does the episode's N-Gram Table question set match the same episode's Episode Breakdown in the `pod-2A-topic-planner` Topic Plan? Both are read and compared; if a question was cut or added in one but not the other, flag the gap and reconcile before generating (see `### Inputs`). In v2 the bank feeds the Appendix and seeds Segment 2 rephrasing rather than becoming the script, but drift between the two upstream artifacts is still a defect.
14. If a v2 ROS Template already exists for this episode + scope, archive and rebuild or refresh in place?

If anything's unclear I'll ask once in a single message. I won't touch Drive until you say go.

---

## Best Practices

The WHAT contract. Every other section references these by name; the SOP never restates them.

### Inputs

What is?
The materials this skill ingests - a matching-scope N-Gram Table and entity map (both hard dependencies), the entity clusters file, an optional keyword-research seed set, an optional attribute-research set, the podcast architecture doc, and the Case Engine Branding folder - all resolved before any template is generated.

#### Required

- **Episode format flag resolved to `v2-open-interview`** - the coexistence gate. **Supplied by the user at run time** (Greeting Q1): "Is this episode running the v2 open-interview format or the legacy segmented format?" Auto-filled from the client's `podcast-overview.md` when that doc is present and carries an `episode_format` field, but the user's answer is the authority and an absent doc is never a blocker - it just means the question gets asked. Any answer other than an explicit `v2-open-interview` - including "not sure", "legacy-segments", blank, or unknown - means STOP and route to `/pod-3A-ros-template`. This is a hard input, not a preference. *Temporary manual ask pending a future DB wiring for the format flag.*
- **Matching-scope N-Gram Table** (`n-gram-table.json`) - the collation table from `/pod-2B-n-gram-table`. In v2 it is the SOURCE MATERIAL rather than the script: it ships verbatim in the Appendix, and its substance is rephrased into Segment 2 search-phrase questions. No silent fallback - if missing, the skill stops and routes to `/pod-2B-n-gram-table`.
- **The `pod-2A-topic-planner` Topic Plan for this episode** - **CANONICAL SOURCE = the PUBLISHED Google Doc Topic Plan in the client Topic Plan slot** (the client sees that Doc and edits it manually, so it is authoritative for the episode lineup and each episode's topic/title). NEVER take the episode or its topic from a local `topic-plan-v{n}.json`/`.md` or any old/cached file - those are stale mirrors that drift. Confirm the episode's topic/title against the live Doc before building; the Doc wins on any conflict; never build a topic absent from the Doc's lineup (Eberst E5 slip-and-fall wrong-episode incident, 2026-06-19). Also read as a CROSS-CHECK on the question bank - if a question was cut or added in one and not the other, flag it and reconcile before generating.
- **Matching-scope entity map** (`entity-map.json`) - the localized entity set from `/pod-1A-entity-research`. In v2 entities ground what the writer knows to be locally true, which shapes the credential line, the attribute bullets and the Short-Form questions. They are never woven into the page as named-entity underlines or citations the way they were in legacy - see `### Editorial Guidelines -> Guideline 3`. No silent fallback - if missing, the skill stops and routes to `/pod-1A-entity-research`.
- **Episode title** - the episode this template is built for.
- **Topic** - practice area (e.g., Personal Injury, Criminal Defense, Family Law).
- **Scope** - one of: Topic Only, Location, Extension.
- **Firm name** - used only to resolve podcast architecture / Greeting auto-fill when a firm is named; the template body stays tokenized. Not needed at Topic Only scope.
- **Location** - required when scope is Location or Extension. Format: `CA`, `CA - Los Angeles County`, `CA - Long Beach`. No colons; dashes only.
- **Region phrasing** - the plain-text region the city is paired with in Segment 2 ("the Inland Empire", "Chatham County and coastal Georgia"). Required at Location/Extension scope. Not a placeholder - see `### Editorial Guidelines -> Guideline 6`.

#### Optional

- **`attribute-research.json`** - the ranked attribute set from `/pod-1D-attribute-research` (sibling skill, in development). This is the intended long-term source for the Segment 1 attribute block and the Segment 2 attribute questions. When present, use it and record `attribute_source: pod-1D` plus the pull date in `metadata.json`. When absent, fall back to `references/attributes/attributes-fallback.json` and flag `> INFERRED: attribute set from static fallback pulled {date}, not a live pull`.
- **`entity-clusters.md`** - the clusters sibling of the entity map, same source folder. Deepens the writer's jurisdictional grounding without ever surfacing as terminology; the skill proceeds without it.
- **`keyword-research.json`** - the keyword-research seed set from `/pod-1B-keyword-research`. In v2 this matters MORE than it did in legacy: Segment 2 questions are built on search phrases, so real query strings and their volumes are the best available source for how people actually phrase things. When present, mine it for Segment 2 question phrasing and for the Appendix Search Queries block. If found but undeclared in the handoff contract, the skill stops and asks rather than guessing silently.
- **Short-Form location list** - one set of ten questions per location. The count is fixed at ten; only the number of locations varies.
- **Segment 1 duration band** - default 15 to 30 minutes, always stated as a RANGE, never a single number.
- **Episode goal** - Authority / Lead gen / Differentiation / Narrative / Conversion. Default Authority.
- **Refresh flag** - default refresh in place (routes to `## Update`). Pass `archive-and-rebuild` to force a full rebuild with the prior v2 template archived to `_archive-{YYYY-MM-DD}/`.

#### Auto-read (no action required)

- **`podcast-overview.md`** - architecture source of truth (`episode_format`, anchor scope, extension cities, region phrasing, client name). If present at `{Firm} Podcast/.podcast-overview/podcast-overview.md`, the skill auto-fills Greeting questions 1-6; otherwise it asks.
- **Case Engine Branding folder** - the canonical brand reference at [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) (folder id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`). The `## Ship` build reads logo, colors, fonts, and the [Cover Page Spec](https://docs.google.com/document/d/1oydpI055jbj1FYDGeZfHQeMNjaWKUCFVGCRveeuJJCk/edit) for the branded Google Doc. Brand values resolve from the folder at build time - never inlined into this skill. A per-client `brand.json` typography block overrides the CE default (Roboto) when present.
- **Local v2 example references** - bundled `references/examples/ros-template-v2-examples.md` as the quality-anchor set. If missing or empty, fall back to the in-skill reference material in `## INTERNAL` - do not block.
- **Section prompts** - `references/prompts/01..05` plus its README. The v2 body is generated section by section, not in one pass, and each file carries the live generation prompt, its rules, a GOOD / BAD pair, its mechanical gates, and the repair instruction for each gate. The README also defines the fixed execution order (each section constrains the next) and the five global gates. Read the README at Orient and the individual prompt at the moment its section is generated.
- **`references/attributes/attributes-fallback.json`** - the static ranked attribute set, used when `pod-1D-attribute-research` has no output for this market.

#### Capabilities

The skill runs locally in Claude Code and calls its tools directly - it assumes they exist and uses them in this priority order. On a tool error, it skips that source and degrades to the next; it never probes for availability first.

- **Local filesystem read** - for auto-detected upstream artifacts at the canonical Desktop path `~/Desktop/claude_code/deliverables/podcast/...`. Fastest path; no Drive round-trip.
- **`gws drive`** (or `mcp__claude_ai_Google_Drive__*` connector) - for the matching-scope N-Gram Table, entity map, clusters file, optional keyword research, optional attribute research, and the Case Engine Branding folder from the shared Drive.
- **`mcp__ce-services__rag_query`** (`rag_name: koray`) - for SEO / methodology grounding when calibrating Segment 2 search phrasing and the geo pairing; a sanity check, never a content source.
- **User-supplied materials** in the greeting (pasted artifacts, dropped files) and user interview for hard requirements still missing - the always-available floor.
- **Hard requirement** - the matching-scope N-Gram Table and entity map must both resolve via local read or Drive. If either is missing, the skill stops and routes to the upstream skill.
- **Behavior on a tool error** - skip that source and degrade to the next. With no reachable source, fall through to user-supplied + interview; flag every Inferred value with `> NEEDS CONFIRMATION:` per Sourcing discipline.

### Outputs

What is?
The artifacts this skill ships - the 3-format trio (a machine-readable JSON payload, a markdown source-of-truth, and a CE-branded Google Doc) plus a `metadata.json` provenance file - landing in the shared template library under `Episode Templates/{Topic}/{scope}/` per Map 2 at EVERY scope, mirrored to the local Desktop path. Filenames carry a `v2` marker so v2 and legacy templates coexist in the same scope folder without collision.

#### Output formats

CE-wide default: every persistent artifact ships in three formats.

- **JSON** - `ros-template-v2-data.json` - structured / machine-readable payload, the input the build script renders from and the one `pod-3B-client-ros-v2` populates. Validates against `references/schema/ros-template-v2.json`. Note the distinct filename: it does NOT overwrite a legacy `ros-template-data.json` sitting in the same folder.
- **Markdown** - the ROS Template v2 `.md` - local source-of-truth mirror, the downstream-readable raw source uploaded to Drive as `text/markdown` (no conversion). Retains the `## INTERNAL` block. Tokenized; `{{PLACEHOLDERS}}` preserved verbatim for Client ROS to populate.
- **Google Doc** - the human-facing CE-branded ROS Template v2 Doc. Built from a CE-branded `.docx` (cover page, logo, Roboto body, "Prepared by Case Engine" footer) emitted by `scripts/build-ros-template-v2-docx.py`, then uploaded with `mimeType: application/vnd.google-apps.document` so Drive auto-converts the DOCX to a clean Google Doc. Created / updated in-place via `files.update` against a stable fileId so the URL never breaks for downstream links.

A `metadata.json` provenance file ships alongside the trio (internal-only, not a client-facing artifact - records sources, counts, scope, episode goal, geo plan, attribute source and pull date).

#### What ships

- **ROS Template v2 `.md`** - Markdown - raw tokenized source, downstream-readable, retains the `## INTERNAL` block.
- **ROS Template v2** - Google Doc - human-facing CE-branded view, cover page, Roboto typeface, stable fileId.
- **`ros-template-v2-data.json`** - JSON - machine-readable payload, downstream-consumed by `pod-3B-client-ros-v2`; validates against `references/schema/ros-template-v2.json`.
- **`metadata.json`** - JSON (internal) - provenance: sources, question / city / placeholder counts, scope, episode goal, geo plan, attribute source, references status.

#### Drive destination

Shared drive root: `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`).

| Scope | Destination | Why |
|---|---|---|
| Topic Only | `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/Topic Only/` (per [Templates [Master] Structure](https://docs.google.com/document/d/1ciUUzUNG4M6HtgnSBsyq53C79aeZF6PbOa2CVuWHjiQ/edit) → Map 2) | The tokenized template is GENERIC and reusable across every firm, so it lives ONLY in the shared template library, never in a client folder. |
| Location (anchor) | `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/Locations/{Location}/` (Map 2) | Generic and reusable across every firm recording at this scope. The firm-specific Client ROS is the only ROS artifact that lands in the client episode folder - produced downstream by pod-3B-client-ros-v2. |
| Extension | `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/Extensions/{Location}/` (Map 2) | Same reasoning. In v2 most former extensions collapse into Segment 2 city blocks rather than getting their own folder - see `### Framing -> What extensions become in v2`. |

```
templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/
  E{N}: {Episode Title} // ROS Template v2 - {Location}.md              raw markdown source (text/markdown)
  E{N}: {Episode Title} // ROS Template v2 - {Location}                 branded Google Doc (in-place files.update)
  ros-template-v2-data.json                                             machine-readable payload, downstream-consumed
  metadata.json                                                         sources, counts, scope, episode goal, geo plan, attribute source
  _archive-{YYYY-MM-DD}/                                                (only the prior v2 ROS Template file, if one existed)
```

At Topic Only scope the trio is named plainly - `ROS Template v2.md`, `ROS Template v2`, `ros-template-v2-data.json` - and the ` - {Location}` suffix is dropped.

**The `v2` marker in the filename is load-bearing, not cosmetic.** A legacy `ROS Template` and a `ROS Template v2` can sit in the same scope folder for the same episode. Never write a v2 artifact over a legacy filename, never rename or archive a legacy template from this skill, and never assume the folder is empty because no `ROS Template v2` is present.

**Legacy compatibility:** MVP Accident Attorneys and any other client with pre-2026-05-15 episodes may have a tokenized template still sitting in an old `EP{N}/01 Strategy/` or `Template ROS:` slot inside a client episode folder. Do not auto-migrate those. The canonical destination for any NEW or refreshed template is the shared template library only (Map 2).

#### Local mirror

`~/Desktop/claude_code/deliverables/podcast/ROS Templates/{Topic}/{Episode}/{scope}/` - holds the same ROS Template v2 `.md`, the CE-branded `.docx`, `ros-template-v2-data.json`, and `metadata.json`. `{scope}` = `Topic Only`, `Locations/{Location}`, or `Extensions/{Location}` to mirror the Drive scope convention. The mirror keeps the DOCX (not the auto-converted Google Doc, which only exists in Drive). Written on every run. The same `v2` filename discipline applies - a legacy mirror in the same folder is left untouched.

#### Schema

`references/schema/ros-template-v2.json` - the canonical JSON schema `ros-template-v2-data.json` validates against. The schema enforces the placeholder inventory (which of the 12 approved placeholders are used), the Segment 1 block set, the Segment 2 city blocks with per-question geo tags, the duration band, the episode goal, and the scope. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed - do not block on a missing schema.

#### Sections INCLUDED in the client-facing Google Doc

- Branded cover page (CE logo inline at 180pt, `Run of Show` in CE Blue 24pt, episode title, `{practice area}  |  {scope}`, `Prepared by Case Engine`)
- `# S1: Long-Form (15-30m)` - `## Introduction (45-60s)` (welcome, setup, credential, prompt, `ATTORNEY RESPONSE`), the attribute bullets directly under the speaker tag, then `## Outro` Then `## Follow-ups` - interviewer notes, never read on air - then `## Outro`.
- A horizontal rule, then `# S2: Short-Form (60-90s)` - one direction line, then `## Location: {{CITY}}` blocks of ten questions each with their bullets
- `# Appendix: Source Question Bank`

The Appendix ships inside the Doc but is marked not-read-on-air. It is the audit trail and the pull pool, not script.

#### Sections EXCLUDED (never in the client-facing artifact)

- `## Quality Assurance` and everything from that heading onward
- Known Gaps, Handoff Contract, Next Steps, provenance block
- The internal Formatting Guide rulebook (it governs the renderer; it is never a deliverable section)
- `## INTERNAL -> ### Production notes` - the interviewer, co-host, shorts-pull, and editing guidance. It reaches people through `pod-3C-client-guide-v2`, never through the ROS itself.

The Google Doc renderer truncates the markdown source at the first `## Quality Assurance` heading and discards everything after. See `## INTERNAL` for the grep test.

#### Capabilities

Both write destinations are written every run. On a write error to one, the skill ships to the other and surfaces the partial state in the report - it does not silently lose the deliverable.

- **Drive** - `gws drive` (or `mcp__claude_ai_Google_Drive__*` connector) - writes the markdown, the branded Google Doc, the JSON, and metadata into the shared template library scope folder (Map 2) at every scope. Never a client/firm episode folder.
- **Local mirror** - local filesystem write to the local mirror path, alongside the Drive write.
- **Behavior on a write error** - if one destination errors, ship to the other and report the partial state. If both error, hard-fail with a clear message; do not silently lose the deliverable.

#### Examples

`references/examples/ros-template-v2-examples.md` - single doc with GOOD / BAD / EDGE CASE labeled sections per CE convention. The two GOOD anchors are the Truck Accidents (GA - Savannah) and Slip and Fall (CA - San Diego) tabs from the 2026-08-14 prototype build. Read 1-2 examples matching the requested scope as calibration before generating. If the folder is empty, proceed on the in-skill reference material in `## INTERNAL` and flag `"references": "empty"` in `metadata.json`.

#### Routing

- **Upstream (required, hard dependency):** `/pod-2B-n-gram-table` - the matching-scope N-Gram Table; `/pod-1A-entity-research` - the matching-scope entity map.
- **Upstream (optional):** `/pod-1D-attribute-research` - the ranked attribute set; `/pod-1B-keyword-research` - search phrasing for Segment 2.
- **Sibling (mutually exclusive):** `/pod-3A-ros-template` - the legacy format. Exactly one of the two runs per episode, decided by `episode_format`.
- **Downstream (required):** `/pod-3B-client-ros-v2` populates the placeholders for a specific firm, which in turn feeds `/pod-3C-client-guide-v2`. Both built 2026-08-18 as v2 siblings of the legacy skills.
- **Refresh:** re-run with the same episode + scope (routes to `## Update`).

#### Handoff Contract

This skill produces the following for downstream consumers:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| ROS Template v2 `.md` + branded Google Doc | `/pod-3B-client-ros-v2` | Full tokenized v2 structure; `{{PLACEHOLDER}}` locations including `{{YEARS_PRACTICING}}`; bold formatting to preserve; Segment 2 geo tags; Appendix Source Question Bank |
| `ros-template-v2-data.json` | `/pod-3B-client-ros-v2` | Placeholder inventory (which of the 12 approved placeholders are used), Segment 1 blocks, Segment 2 city blocks and per-question geo tags, duration band, episode goal, scope - the structured payload Client ROS populates |
| `metadata.json` | (not consumed downstream) | Internal provenance - sources, duration band, city count, question counts, scope, episode goal, attribute source + pull date, geo plan, references status |

Downstream consumers can rely on: the Google Doc URL is stable for the lifetime of the template (preserved via `files.update` across re-runs); `ros-template-v2-data.json` validates against `references/schema/ros-template-v2.json`; only the 12 approved placeholders appear in the template body; every Segment 2 question carries exactly one geo tag. Upstream pulls (hard dependency): `n-gram-table.json` from `/pod-2B-n-gram-table` and `entity-map.json` + `entity-clusters.md` from `/pod-1A-entity-research`. The skill refuses to run without both.

### Framing

The ROS Template v2 is the GENERIC reusable script, not a finished client deliverable. Client-specific populating happens at `pod-3B-client-ros-v2`. Everything specific to a firm becomes a `{{PLACEHOLDER}}` - no hard-coded firm names, attorney names, or client-specific language ever appears in the template body. Because it is generic and reusable, the template lives ONLY in the shared template library and never in a client/firm episode folder.

**Episode format flag.** A value named `episode_format` is confirmed by the user at run time (Greeting Q1), per client, per show - auto-filled from `podcast-overview.md` when that doc exists and carries the field, otherwise asked outright. Two values:

| Value | Meaning | Skill |
|---|---|---|
| `legacy-segments` | **DEFAULT.** Four segments, ~20 questions, statute-grounded attorney bullets, entity underlines. Every currently shipping client. | `pod-3A-ros-template` |
| `v2-open-interview` | Single credential-led prompt + 15-30 minute open interview, then per-city short-form blocks. | `pod-3A-ros-template-v2` (this skill) |

The flag is resolved ONCE per show, not per episode, so a client's library does not end up half in each format. An unset flag is `legacy-segments` - absence never means v2. Flipping a live client from legacy to v2 mid-season is a producer decision with real consequences for the clients whose episodes were already recorded in the other shape; this skill does not flip it and does not migrate existing templates.

**Why v2 exists (the reasoning from the 2026-08-14 call, so future edits do not undo it).** The legacy format produced a twenty-question interrogation. The attorney was answering, not talking, and the answers came out clipped and defensive because each one was scoped to a narrow question. The single prompt inverts that: it hands the attorney the floor with a credential-led setup and lets a real 15 to 30 minute answer happen. What the question list used to do structurally - establish authority, set scope, prime the shape of the answer - now happens in Introduction lines 2 and 3, the setup and the credential. That is why neither is decorative and neither may be trimmed. `The Lead-In` as a heading was retired 2026-08-14; the work it did survives as line 3.

**Geo model (three fields, use these exact names).** Every podcast carries three distinct geo fields; this skill's location/scope handling maps to them:

1. **Targeting strategy** - `single-location` vs `multi-location`. Does the firm serve/rank one city or several? In v2 this drives the Segment 2 city block count rather than the episode count.
2. **Optimization scope (show anchor)** - City / State / County / Regional. What the podcast *as a whole* is optimized to rank for (Greeting Q3).
3. **Episode geo target** - the specific city THIS episode is built to rank for. It is what `{{CITY}}` resolves to at populate time.

**The rule: anchor scope != per-episode target.** The show can be optimized for a broad scope (e.g. the whole state) while each episode targets a specific city. Research runs at the anchor breadth. Any location/city `{{PLACEHOLDER}}` in this template resolves to the Episode geo target, NOT the show anchor.

**What extensions become in v2.** Under the legacy format, a satellite market got its own Extension episode - a 10-12 question mini derived from the anchor. In v2 the natural home for a satellite market is an additional **Segment 2 city block** inside the same episode: the same question shape, the geo tokens swapped, 60-second self-contained answers that clip cleanly for that city. This is cheaper to record, produces more usable short-form, and avoids the near-duplicate-episode problem. Extension scope remains available for a market that genuinely needs its own episode, and the Drive path for it is unchanged.

### Quality bar

What "good" looks like - the pass / fail intuition.

- Only the 12 approved placeholders appear; a grep for `{{...}}` outside the taxonomy returns zero (see `### Editorial Guidelines -> Guideline 1`).
- **Segment 1 has exactly ONE prompt.** If a second bolded prompt has crept into the Introduction, the format is broken.
- The Segment 1 duration is stated as a RANGE (15 to 30 minutes), never a single number, and never a per-question time budget.
- The Introduction runs in the locked four-line order and each line does real work. The STATIC welcome is line 1 only - it names the podcast and whose show it is, and nothing else. The generated setup is line 2, the credential is line 3 in its own paragraph, and the prompt is line 4. A setup paragraph that re-greets the audience is a fail.
- **Zero legal jargon anywhere above the Appendix.** No statute numbers, no case citations, no element names. There is no exempt section. See `### Editorial Guidelines -> Guideline 3`.
- Every Segment 2 question is phrased the way a person searches, not the way a lawyer categorizes. "What happens if you were partly at fault for the crash?" not "How does comparative negligence apply?"
- Every Segment 2 question carries exactly one geo tag: CITY, CITY + REGION, REGION, NEUTRAL, or STATE.
- The interviewer guidance actually instructs - wait three full seconds before intervening, "walk me through one" for abstraction, a natural-language fill for each missing attribute. It reaches the host through `## INTERNAL -> ### Production notes` and `pod-3C-client-guide-v2`, never as a section in the ROS.
- Document structure matches `### Editorial Guidelines -> Guideline 4` every time - downstream Client ROS relies on the exact shape.
- The human-facing Google Doc is the CE-branded DOCX→Doc, never a raw-markdown→Doc upload.
- No em dashes, no banned vocabulary - the Anti-AI Detection scan fires before publish.

### Sourcing discipline

The Confirmed / Inferred / Unknown three-state pattern. Never block, always ship, never silent. The template still ships when data is incomplete; gaps surface in `## INTERNAL` or with `> NEEDS VERIFICATION:` blocks.

- **Confirmed** - claim traces to a specific source. Every Appendix bank question pulled from the N-Gram Table, every jurisdiction fact pulled from the entity map, and every attribute pulled from a live `pod-1D-attribute-research` output is Confirmed. Ship as-is, no marker.
- **Inferred** - sensible default applied when a source is insufficient. The static attribute fallback is ALWAYS Inferred, never Confirmed, because it is a point-in-time snapshot of what the answer engines surfaced on 2026-08-14 and answer engines move. Ships with `> INFERRED: {what + why + date}` flag.
- **Unknown / NEEDS CONFIRMATION** - no source AND no defensible default. Ships with `> NEEDS CONFIRMATION: {what's missing}` block, never silently synthesized. The region phrasing when nobody has confirmed it is NEEDS CONFIRMATION - propose one, never assume it.
- **Segment 2 rephrasing is Confirmed-with-transformation, and must be traceable.** A Segment 2 question is a rephrasing of n-gram substance into a search phrase. Record the source bank row in `ros-template-v2-data.json -> source_ngram_ref` for every question that has one. A Segment 2 question with no traceable source substance is an invented question and fails the sourcing gate.

### Editorial Guidelines

Cross-cutting content rules for the template. The SOP points back here; the rules live here once.

**Guideline 1 - Only the 12 approved placeholders, never invented tokens.**

> **`{{WEBSITE}}` vs `{{PODCAST_DOMAIN}}` (Gabe directive 2026-08-21).** These are two different things and must never collapse into one token. `{{WEBSITE}}` is the BUSINESS site and belongs in the conversion CTA - a case inquiry has to land on the firm, not the show. `{{PODCAST_DOMAIN}}` is where episodes live and belongs in the subscribe line. Before this split there was one `{{WEBSITE}}` token resolving to the business site by convention rather than by rule, so nothing stopped a run from filling the CTA with the podcast domain and sending injured people to the wrong place.

- **Approved taxonomy** (must match `pod-3B-client-ros-v2` exactly - this is the taxonomy Client ROS v2 consumes at populate time; that skill's `references/placeholders.md` is the populate-side mirror):

  | Placeholder | Source at populate time |
  |---|---|
  | `{{TOPIC}}` | The episode's subject, as a phrase. Cover line. |
  | `{{CITY}}` | The city. Anchors every S2 block; in S1 only in the credential line, naming where the firm practices. |
  | `{{STATE}}` | **SEGMENT 1 geo.** State full name (`CA` -> `California`). Multi-state firms resolve to the spoken phrase. |
  | `{{PODCAST_NAME}}` | Client's podcast name |
  | `{{ATTORNEY_NAME}}` | Full attorney name. Intro line 1 only - the branded open. |
  | `{{ATTORNEY}}` | How the host addresses them on air, first name. Everywhere the attorney is spoken to. |
  | `{{INTERVIEWER}}` | CE host on the recording |
  | `{{FIRM_NAME}}` | Full firm name |
  | `{{PHONE_NUMBER}}` | Firm phone `(XXX) XXX-XXXX` |
  | `{{WEBSITE}}` | Firm website, including `https://` |
  | `{{YEARS_PRACTICING}}` | Integer years in practice, in this market |

- **Canonical source is `references/placeholders.md`.** That file wins if this table ever disagrees with it. The taxonomy settled at ELEVEN tokens on 2026-08-18, matching the live prototype doc exactly. `{{ATTORNEY_FIRST_NAME}}`, `{{HOST_NAME}}` and `{{PRACTICE_AREA}}` were retired and replaced by `{{ATTORNEY}}`, `{{INTERVIEWER}}` and `{{TOPIC}}`; `{{EPISODE_NUMBER}}` left the rendered body and survives only in filenames; `{{RECORDING_DATE}}` was retired outright on 2026-08-18, because a template that serves every firm recording this episode cannot carry any one firm's recording date, and putting one on the cover dated an evergreen asset.
- **The populate side is `pod-3B-client-ros-v2` (built 2026-08-18), which resolves all twelve.** The legacy `pod-3B-client-ros` never learned the v2 tokens and never needs to - it only populates legacy templates. The former top-ship-blocker (five tokens unknown to the legacy populate) is closed; see `### Gotchas`.
- **The region is NOT a placeholder.** It is fixed by this template's location scope, so it is plain text. Do not invent `{{REGION}}`. See Guideline 6.
- **Banned:** any `{{TOKEN}}` outside the twelve above; any hard-coded firm / attorney / city / state name in the template body.
- **Why:** Client ROS scans for every `{{...}}` at populate time; an invented token never gets resolved and ships into the recording as literal markup.
- **Where it fires in the SOP:** `## Create -> ### Generate Segment 1` and `### Generate Segment 2`, and the placeholder gate in `**Guideline 9 - Introduction and outro: calibrate on the examples, obey the guardrails.**

Three files own this, in reading order. This guideline adds nothing to them and must never restate them - an earlier version did and contradicted the spec on four points.

1. **`references/examples/intro-outro-examples.md`** - real BAD -> GOOD pairs. Read first. Calibration beats rules.
2. **`references/introduction.md` -> GUARDRAILS + EXECUTION** - the non-negotiables and the order to write in. Detail lives below it as background.
3. **`references/outro.md` -> GUARDRAILS** - same shape for the close.

**The gate is the read-aloud**, step 8 of EXECUTION. Nothing scriptable replaces it. Every mechanical rule tried on this pipeline - city quotas, scope-list counts, rotation indices, byte-identity carryover - produced worse output by forcing it, and all four were removed on 2026-08-21.

- **Where it fires in the SOP:** `## Create -> ### Generate S1 Long-Form`, `### Generate the outro and appendix`, and the intro/outro gates in `**Guideline 10 - Follow-ups: hard-coded prompt, generated case study, never read on air.**

Segment 1 closes with a `## Follow-ups` block between the attribute bullets and the Outro. It is where the case-study ask went after the story invitation was cut from line 4 on 2026-08-21 - the invitation stopped being a scripted sentence and became a note the interviewer acts on when the moment arrives.

- **The note line and the first bullet are HARD-CODED** and render byte-identical on every episode, from the renderer constants `FOLLOWUP_NOTE` and `FOLLOWUP_STATIC`. They are not generated and never vary: *"Notes for the interviewer. Not read on air."* and *"Follow up when the opportunity presents itself, not on a schedule. Let the answer finish first."*
- **At least one generated bullet must prompt the attorney to expand on a case study for THIS episode's topic.** Generic "ask for an example" fails the point - name the kind of case the topic implies.
- **The ATTORNEY reads this block too (Gabe 2026-08-24).** Write the bullets in the SECOND PERSON, addressed to him - "A case where the first twenty-four hours decided the outcome." / "The mistake you see most often, and what it cost." **Never third-person instructions about him** - "get him to walk through," "push him for," "if he mentions X" all read as talking about the attorney in front of him. Written this way one block serves both readers: the interviewer sees what to ask for, the attorney sees what to prepare.
- **These are notes, not lines.** No question marks, no speaker tag, nothing the host reads out. The renderer fails the build on a question mark or an empty `follow_ups`.
- **S1 only.** Short-Form questions carry their own bullets and never get a follow-up block.
- **Where it fires in the SOP:** `## Create -> ### Generate S1 Long-Form`, and the follow-ups gate in `### Quality gates`.

### Quality gates`.

### Quality gates`.

### Quality gates`.

### Quality gates`.

**Guideline 2 - Research is the palette; the ROS layers in the slice that serves THIS episode's goal.**

- Research outputs capture the FULL topic domain. The template does NOT mechanically consume everything upstream produced.
- **Goal types and the selection rule the renderer applies in v2:**
  - **Authority / education** - the line 3 credential leans on years and case volume; the prompt's "give us the facts" clause carries the weight; Segment 2 weights toward the search-phrase tail questions.
  - **Lead generation** - attribute questions get more of the Segment 2 slots (cost, who handles it, response time); the outro's reach-out line carries the emphasis.
  - **Differentiation** - trial willingness and honest assessment lead the attribute block; Segment 2 opens with the "what would make my case difficult" question.
  - **Narrative / story** - the Follow-ups case-study bullet gets the weight; the interviewer's "walk me through one" is promoted from a fallback to a planned beat (the real-case clause left line 4 on 2026-08-21, and line 4 is now the question-shaped beats per Gabe 2026-08-26).
  - **Conversion** - fee and expense detail is the first attribute; the outro's reach-out carries the CTA.
- **Why:** a single Research run serves many episodes in a series.
- **Where it fires in the SOP:** `## Create -> ### Generate S1 Long-Form` and `### Generate S2 Short-Form`. The goal is recorded in `metadata.json -> episode_goal`.

**Guideline 3 - No jargon anywhere in the document. There is no longer an exempt section.**

- **Banned everywhere:** statute numbers (`O.C.G.A. Section 51-12-33`, `CCP 335.1`), case citations (`Rowland v. Christian`, `Ortega v. Kmart`), rule names (`Daubert`, `MCS-90`), section symbols, and legal element names as such (`duty of care`, `constructive notice`, `comparative negligence`, `res ipsa loquitur`, `sovereign immunity`).
- **Allowed and required instead:** the same substance in the words a person uses. "They will say you should have been watching. In California that reduces your case, it does not end it." "How long it sat there is the whole argument." "The video gets recorded over, often within days."
- **The Producer Notes section is gone, so the containment model is gone with it.** Earlier drafts permitted citations inside a `## Producer Notes (internal, never read on air)` block and ran an inverse check asserting the jurisdiction detail actually landed there. That section is no longer part of the format. The rule is now simpler and stricter: the jargon pattern returns ZERO across the ENTIRE document. There is no section where a citation is acceptable, so there is nothing to contain and nothing to inverse-check.
- **The `# Appendix: Source Question Bank` is the one unavoidable exception, and it is not an exemption.** The appendix carries n-gram rows verbatim, and some of those rows contain statute references because the research phase wrote them that way. Verbatim means verbatim - do not edit the bank to satisfy the scan. Scope the jargon scan to everything above the appendix heading. Nothing in the appendix is ever read on air.
- **The test:** read any line aloud. If it sounds like a citation or a law-school outline heading, it is wrong. Cyle on the 2026-08-14 call: "nobody's going to search 'what is duty of care'."
- **Where the jurisdiction knowledge went.** It still informs generation - the entity map tells the writer what is true - it just never reaches the page as terminology. The attorney gets the consequence, not the rule.
- **Where it fires in the SOP:** `## Create -> ### Run the jargon scan`, and the jargon scan in `### Quality gates`.


**Guideline 4 - Locked document structure. Matches the live prototype doc exactly.**

- **Document shape** (downstream Client ROS relies on it exactly):
  - **Cover page** - the CE deliverable cover spec, inlined here so it has no external dependency (cross-check against the [Cover Page Spec](https://docs.google.com/document/d/1oydpI055jbj1FYDGeZfHQeMNjaWKUCFVGCRveeuJJCk/edit) in the Case Engine Branding folder). Two spacer paragraphs, the CE logo inserted inline at the second paragraph (Drive id `1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2`, 180pt wide), a third spacer, then `Run of Show` in CE Blue 24pt bold, the episode title in dark 18pt bold, a spacer, `{practice area}  |  {scope}` in dark 14pt, a spacer, and `Prepared by Case Engine` at 11pt. Everything centered, Roboto. Page break after.
  - `# S1: Long-Form (15-30m)` (H1, CE Blue, starts on its own page)
    - `## Introduction (45-60s)` - four lines and one beat. Line 1 the STATIC `welcome`, byte-identical, with NO substitution. Line 2 the GENERATED `setup`, its own paragraph. Line 3 the GENERATED `credential`, its own paragraph, not bold in full. Line 4 the GENERATED `prompt`, in full bold, and the only bolded prompt in the document. The beat (the attorney says hello, unscripted) sits between lines 3 and 4 as a direction. Then `ATTORNEY RESPONSE`. There is NO `INTERVIEWER` tag here; the welcome makes the speaker obvious and the tag was removed.
    - The attribute bullets sit directly under the `ATTORNEY RESPONSE` tag - ten to twelve of them, each a bold lead-in plus one sentence of what to cover. **No heading above them and no divider below.** `Attributes to Hit` and the whole `Internal Notes (not read on air)` block were retired 2026-08-17 and the renderer emits neither.
    - `## Outro` (H2, CE Dark) - the three GENERATED lines in order: thanks and credit, sign-off, reach-out. The sign-off is deliberately not last. NO speaker tag - the `INTERVIEWER` tag was cut 2026-08-18, since `outro_note` already says who is speaking. The outro closes S1 because S1 is a complete recording; it never follows S2. See `references/outro.md`.
  - A horizontal rule, then `# S2: Short-Form (60-90s)` (H1, CE Blue). **S2 does NOT start its own page** - it flows on from the S1 outro behind the rule, changed 2026-08-18. Only the cover, S1 and the Appendix begin a page.
    - One shipped italic direction line under the heading. The two STATIC short-form mode notes were retired 2026-08-17.
    - `## Location: {{CITY}}` - one per location, exactly ten questions, hard cap. Each question renders fully bold with its `Q{N}:` label inside the bold, and carries 2 to 4 attorney bullets in `[{Label}]{.underline}: {detail}` form, labels underlined and never bold. **Nothing else renders under a question.**
    - Additional locations are additional sets of ten, customized per city, each naming its city in PLAIN TEXT. There is no second city token; `{{CITY_2}}` does not exist.
  - `# Appendix: Source Question Bank` (H1, CE Blue, starts on its own page) - the n-gram rows verbatim, internal.
- **Removed from the format and must not come back:** `Internal Notes (not read on air)` and everything under it (the three moves, both findings lines, the source-consistency counts, the need-to-know bullets); `Attributes to Hit` as a heading; the two short-form mode notes; the `Alternate introductions` block; `How This Episode Runs`; `Producer Notes` (in any form); `The Lead-In` as its own heading; `The Prompt` as its own heading; `Interviewer: Live Checklist and Follow-Ups`; `Co-Host Notes`; `Geo Rule: pair the city with the region`; per-question geo tag lines; per-question answer-guidance notes; per-question time budgets. Canonical list in `references/document-structure.md`. The interviewer and co-host guidance did not evaporate when the sections were cut - it moved to `## INTERNAL -> ### Production notes` so it reaches the attorney and the host through `pod-3C-client-guide-v2` instead of cluttering the recording script.
- **Heading colors** - H1 section headers (`S1: Long-Form (15-30m)`, `S2: Short-Form (60-90s)`, `Appendix`) are CE Blue. **H2 headings are BLACK (`CE_DARK`)**, not blue. H3 is dark. The cover title is CE Blue; the cover subtitle and location line are dark.
- **Speaker tags** - `ATTORNEY RESPONSE` in the Introduction is the ONLY one left in the document. Gray italic, never bold, never code blocks, never bracketed. The `INTERVIEWER` tag was cut from both the Introduction and the outro on 2026-08-18 and is preserved under `references/statics.json` -> `retired`.
- **Bold** - the prompt in full, every `{{PLACEHOLDER}}`, each Short-Form question IN FULL including its `Q{N}:` label, and the lead-in of each attribute bullet. Populated values stay bold after populate.
- **Underline** - the Short-Form bullet labels and entity runs, as pandoc `[text]{.underline}`, never HTML `<u>`. A Short-Form bullet label is underlined and NEVER bold, so the question keeps the only bold weight in its block. The attribute lead-in is the deliberate opposite - bold, not underlined. Do not harmonize the two.
- **Instruction lines** - the italic direction lines (the S2 direction note, the outro note) are part of the deliverable and ship.
**Guideline - The attorney is never "the guest." It is their podcast.**

- **Banned everywhere:** "my guest", "our guest", "today's guest", "joining us", "thanks for coming on", "welcome to the show" directed at the attorney, and any construction that frames the attorney as a visitor.
- **Why:** the show is co-branded with the firm - `{{PODCAST_NAME}}` with `{{ATTORNEY_NAME}}`. The attorney owns it. The CE interviewer is the one asking questions on someone else's show, so guest framing inverts the relationship and quietly undercuts the authority the whole format is built to establish. Gabe, 08-14.
- **Allowed:** name them directly. "Welcome back to `{{PODCAST_NAME}}` with `{{ATTORNEY_NAME}}`." "`{{ATTORNEY}}` has spent `{{YEARS_PRACTICING}}` years handling these."
- **Where it fires:** the Introduction welcome line, the credential in line 3, and the outro's thanks line. The `Alternate introductions` block was retired 2026-08-17.

- **Banned:** an in-document "Formatting Guide" section; em dashes anywhere; numbered lists in ClickUp-bound content.
- **Why:** Client ROS reads this exact shape to populate per firm; structural drift breaks the populate step.
- **Where it fires in the SOP:** `## Create -> ### Generate the cover page`, `### Generate S1 Long-Form`, `### Generate S2 Short-Form`, `### Generate the outro and appendix`.

**Guideline 5 - Short-Form questions are built on search phrases. Ten per location, hard cap, each with 2-4 attorney bullets.**

- **Carry the question VERBATIM from the N-Gram Table. Do not re-voice it here.** As of 2026-08-21 `pod-2B-n-gram-table` Guideline 2 owns question voice end to end and generates on-air-ready phrasing. The previous instruction here - re-voice n-gram substance into search-box phrasing - is RETIRED: it was the direct cause of the Eberst E2/E3/E4 defect rate (22 of 30 questions needed human rewrite before air). A perfect search string is a terrible spoken question. If a question arrives here reading like a search string rather than something a person would say, that is an upstream defect - route it back to `/pod-2B-n-gram-table`, do not patch it in this skill.
- **EIGHT TO TEN questions per location in the body, plus the remainder as that location's Question Pool (Gabe directive 2026-08-24; renamed from "swap pool" per Gabe 2026-08-26 - display labels and prose only, JSON fields and code identifiers keep their names).** The N-Gram Table still ships 20 rows per location; **the best 8-10 render in the Short-Form block** and the other 10-12 go to the pool with their bullets built. This replaces the 15-per-location count set 2026-08-21, which replaced a ten-per-location hard cap. It is a RANGE, not a cap - 8 is fine, 10 is fine, 11 fails.
- **Picking the best 8-10 is a real editorial step, not a truncation.** Take the top of the table in order and you get clumping. Select for:
  - **Self-contained.** It has to answer in 60 to 90 seconds with no context from S1, because each one gets clipped and published alone. A question that needs a setup is a bad short.
  - **Real demand.** It carries a money phrase or a genuine search query, not a topic the table needed for completeness.
  - **Clippable.** It resolves to a concrete answer rather than opening a discussion.
  - **Spread.** No two selected questions answer substantially the same thing - the dedup bar is tighter here than in the table, because 8 near-duplicates is a worse block than 8 unrelated ones.
  - **Keep the city-tagged ranking targets.** They are the local retrieval anchors and are the reason the block is per-city at all.
- **Everything not selected goes to the pool WITH its bullets** - a client rejection swaps in with zero rebuild.
- **Question mix per location:**
  - **3 city-tagged ranking targets** (always kept) carrying the money phrase (`{practice area} lawyer in {city}`). These are the ones that change per location. The city must earn its place via the two-lane test in `pod-2B-n-gram-table` Guideline 4. **The city-region pairing is NOT a valid construction in spoken question text** - see Guideline 6 as amended.
  - **12 topical questions** drawn from the attribute set and the episode's substance - cost and expenses, trial willingness, who handles the case, local presence, expert network, deadlines, honest assessment. **These are NOT byte-identical across locations.** Each location's table is generated against that city's own entity map (`pod-2B-n-gram-table` multi-location Mini rule: *the cities' tables must not overlap verbatim - shared legal ground reworded per city*), and **their answer bullets carry that city's local stack even when the question text is geo-neutral** - the local freeway, the local trauma center, the county court, the local agency. The city is a **ceiling in the question and a floor in the answer** (Gabe directive 2026-08-21). A block where only the 3 city-tagged questions carry local weight is ~80% generic and the per-city split earns nothing. *(A byte-identity rule was briefly written here on 2026-08-21 and RETRACTED the same day.)*
- **Answer bullets are where localization lives (Gabe directive 2026-08-21).** A geo-neutral question still gets bullets that name THIS city's local stack - the trauma center, the county court, the responding agency, the corridor - drawn from the n-gram row's Entities column and the upstream `local_anchors` set. The city is a **ceiling in the question text and a floor in the answer**. A location block where only the city-tagged questions carry local weight is ~80% generic and the per-city split earns nothing. Do not add the city to a question to compensate; add it to the bullets.
- **Each question carries 2-4 attorney response bullets, three by default**, in the legacy label-plus-detail form, rendered `[{Label}]{.underline}: {detail}` - what the attorney COVERS, never a question and never a line to read aloud. Restored 2026-08-18 at Gabe's direction after being cut 08-14. What actually made the earlier blocks read as worksheets was the geo tag lines, the time budgets, and answer guidance phrased as instruction to the reader. Those stay dead. The `**Label:** detail` form never had the read-aloud problem. **Nothing else renders under a question** - no time budget, no geo tag line, no source ref, no co-host setup line. Full spec in `references/short-form.md`.
- **Self-contained is still mandatory** even though the instruction is no longer printed per question. It lives once in the STATIC short-form mode note. Each answer restates the question and refers to nothing from S1, because each one gets clipped and published on its own.
- **60 to 90 seconds is the target,** per the section heading. Retakes are expected and the mode note says so.
- **The Question Pool carries answer bullets.** Each location's 5 pool questions render with the SAME 2-4 attorney response bullets as body questions (`[{Label}]{.underline}: {detail}`), so a client rejection at review is swapped in with zero rebuild (Gabe directive 2026-08-21 - this overrides the legacy `pod-3A-ros-template` rule that reserve questions need question text only). `# Appendix: Source Question Bank` additionally carries the FULL n-gram bank verbatim and unedited, renumbered 1..M, as the audit trail. Both are INTERNAL - `pod-3B-client-ros-v2` strips the appendix; the Question Pool's disposition is set by that skill.
- **Where it fires in the SOP:** `## Create -> ### Generate S2 Short-Form` and `### Generate the outro and appendix`.

**Guideline 6 - Geo pairing governs GENERATION. It is never printed in the document.**

- **The rule (Cyle, 2026-08-14): do not repeat the city on every question.** Pair the city with its region - "in Fresno and across the Central Valley." That is how the AI answers themselves phrase it, so the pairing is the retrieval target, and the same sentence picks up regional queries alongside city queries.
- **The geo treatments still exist as a generation constraint.** Every question is still built to one of CITY, CITY + REGION, REGION, NEUTRAL, or STATE. Three per location are city-tagged ranking targets that must carry the city and must never be swapped for the region. The rest carry locality through the content.
- **The tags are NOT rendered.** Earlier drafts printed a `top-keyword | CITY` line under each question. That is gone. The tag governs how the question is written, then it stays in `ros-template-v2-data.json` as `geo_tag` for downstream and QA. A producer auditing geo distribution reads the JSON, not the Doc.
- **Why the tags came off the page.** They are instructions to the writer, not to the attorney. On the page they read as jargon, they invite the attorney to say the city mechanically because the label told them to, and they made a ten-question block look like a form. The constraint survives; the label does not ship.
- **What this replaces.** `pod-2B-n-gram-table` carries a roughly 25 to 45 percent aggregate city-share ceiling on questions. **That ceiling does not apply to a v2 Short-Form block and must not be enforced against one.** The ceiling was a blunt defense against city-token stuffing when every question was a standalone city-bearing string and the only lever was "use it less". The pairing solves the same problem structurally, and a percentage cap would trim the three city-tagged ranking targets first, which are exactly the questions that need the city. Per-question treatment is a sharper instrument than an aggregate percentage.
- **The region is plain text, never a placeholder.** It is fixed by the template's location scope. `{{REGION}}` does not exist and must not be invented.
- **Where it fires in the SOP:** `## Create -> ### Generate S2 Short-Form`, and the geo gate in `### Quality gates`.

**Guideline 7 - Attributes replace the statute-heavy bullets.**

- The Segment 1 attribute block is the v2 replacement for the legacy attorney-response bullets full of entities and statute references. It has no heading - `Attributes to Hit` was retired 2026-08-17 and the bullets sit directly under `ATTORNEY RESPONSE`. Attributes are what the answer engines tell people to look for in a lawyer, ranked by how consistently they surfaced across live Google AI Overview and ChatGPT pulls.
- **Source order:** `pod-1D-attribute-research` output for this practice area + market if it exists (Confirmed); otherwise `references/attributes/attributes-fallback.json`, flagged Inferred with its pull date.
- **Where the ranking is shown: nowhere on the page.** The bullets carry the name and the plain-language detail only. The source-consistency counts ("4 of 4", "2 of 4, high signal") were cut from the document entirely on 2026-08-17 along with the Internal Notes block that briefly held them. Gabe: "That's just filler." Provenance lives in `metadata.json` (AT-5).
- **The ranked fallback set** (pulled 2026-08-14 across two practice areas and two markets):
  - **Trial willingness** - the strongest signal, and usually the first sentence of the AI answer. The research records it as a question the client asks; the BULLET states what the attorney covers - cases actually tried rather than settled, and what that changes at the table. A question mark in the block fails AT-1.
  - **Specific case-type experience** - not the practice area, the case TYPE. How many of THIS kind, how recently.
  - **Fee AND expenses in detail** - percentage, whether it rises if suit is filed, who pays records, filing fees, investigators, experts, court reporters, and what happens if you lose.
  - **Local court familiarity** - the county court, the judges, how the local defense firms operate. Specifics, not "we serve the area".
  - **Evidence preservation speed** - what gets secured in the first days, and how fast, before it is deleted or overwritten.
  - **Expert network** - name the roles: reconstructionists, safety engineers, code inspectors, medical specialists, economists.
  - **Who actually handles the case day to day** - am I hiring you, or an intake operation that refers this out.
  - **Honest assessment** - naming what would make a case hard is a POSITIVE signal. Guaranteeing a number is flagged as a RED FLAG.
  - **Verifiable bar standing** - license and disciplinary history. Ranked ABOVE reviews and awards.
  - **Deadlines** - the number of years and what happens if it passes. Surfaced state-specifically rather than everywhere.
- **Two counterintuitive findings that must survive every edit of this skill:** reviews and awards rank LOWER than the industry assumes (ChatGPT explicitly says verifiable bar standing is more meaningful than ratings alone), and naming a weakness builds MORE trust than making a promise. Both invert what an attorney's instinct will be on the day, which is exactly why they belong in the document rather than in someone's head.
- **Attributes are hit anywhere, in any order, in the attorney's own words.** They are not a checklist to read and not a question list in disguise. The interviewer holds the same list and fills gaps naturally at the end.
- **Where it fires in the SOP:** `## Create -> ### Build the Segment 1 spine`.

**Guideline 8 - The STATIC strings are constants. They are never regenerated.**

- **What they are.** A small set of strings that are byte-identical on every episode, every client, and every scope (exactly one welcome variant fires per episode). They are boilerplate in the precise sense: the wording was decided once, it is not a creative surface, and regenerating it per run produces drift with no upside. They live in the JSON template as constants and render verbatim.
- **No substitution exists anywhere in the set.** `{topic_phrase}` moved out of `welcome` on 2026-08-18 when that constant shrank to Introduction line 1. `{{PLACEHOLDER}}` tokens inside these strings are resolved downstream by `pod-3B-client-ros-v2` like any other placeholder, not by this skill. Substitute with `.replace()`, never `str.format()` - format collapses the doubled braces and silently destroys every token.

| Key | Substitution | Value (verbatim) |
|---|---|---|
| `welcome` | none | Welcome back to **{{PODCAST_NAME}}** with **{{ATTORNEY_NAME}}**. Introduction line 1 ONLY. |
| `welcome_first` | none | Welcome to **{{PODCAST_NAME}}** with **{{ATTORNEY_NAME}}**. Episode 1 only. |
| `welcome_embedded` | none | Welcome back to the **{{PODCAST_NAME}}** Podcast. FALLBACK for embedded names with no "w./with" splice point (Gabe 2026-08-26, locked). |
| `welcome_embedded_first` | none | Welcome to the **{{PODCAST_NAME}}** Podcast. Episode 1 of such a show. |
| `outro_note` | none | Keep it short. Thank them and mean it, sign off, then the reach-out. Do not recap the episode. |

- **Embedded-name shows (Gabe 2026-08-26, locked).** A podcast name of the shape "{Prefix} w./with {Attorney}" (e.g. "Car Accident Attorney w. Robert May") SPLITS at the "w./with": line 1 renders "Welcome back to the {Prefix} podcast with {Attorney}." as plain spoken text with NO bolds, computed at populate by `pod-3B-client-ros-v2` - never "with **{{ATTORNEY_NAME}}**", which doubles the name. The `welcome_embedded` constants are the fallback for a name that embeds the attorney with no "w./with" to split at. A "w." is always spoken as "with" (`statics.json -> welcome_split_rule`).
- **Per-episode generated fields are ONLY these:** `topic_phrase`, `setup` (Introduction line 2), `credential` (Introduction line 3), `prompt` (Introduction line 4), the attribute bullets, the Short-Form question sets with their bullets, and the outro's three spoken lines. `cold_open` is a DEPRECATED alias for `setup`; `need_to_know` and `examples` are RETIRED, having lived in the cut Internal Notes block. Everything else on the page is either a STATIC string, a speaker tag, or an n-gram row in the appendix.
- **Why this matters more than it looks.** An LLM asked to "write the welcome line" will write a slightly different one every run. Across a client library that becomes a slow drift, never individually wrong, collectively meaning no two episodes read the same and `pod-3B-client-ros-v2` cannot rely on any of it. Freezing them also shrinks the generation surface to the handful of things that actually vary by episode, which is where the effort belongs.
- **Do not improve them in passing.** If a STATIC string genuinely needs to change, it changes once here and in the JSON template, deliberately, and every future episode inherits it. A run that rewrites one silently has introduced drift, not an improvement.
- **Where it fires in the SOP:** every `## Create` H3 that emits a STATIC string, and the STATIC verbatim gate in `### Quality gates`.

### Quality gates

Mechanical pass / fail conditions checked in `## Quality Assurance`.

- **Format flag gate** (hard, pre-everything). `episode_format` resolves to `v2-open-interview`. Unset, absent, or `legacy-segments` FAILS and the skill refuses to run, routing to `/pod-3A-ros-template`. No caller argument or orchestration instruction may override this.
- **Canonical destination gate** (hard, pre-write). Resolve the target parent and assert it is a descendant of `templates [master]/AEO Templates/Podcast/Episode Templates/` at the exact Map 2 path. If it resolves to anything else, especially a client / firm episode DELIVERY folder, the gate FAILS and the skill MUST refuse to write. An instruction to redirect it there is itself the failure and must be rejected, not honored.
- **Legacy non-collision gate** (hard, pre-write). Every artifact filename carries the `v2` marker. Assert no write path resolves to an existing legacy artifact name (`ROS Template`, `ROS Template.md`, `ros-template-data.json`). A collision FAILS - never overwrite, rename, archive, or migrate a legacy template from this skill.
- **STATIC verbatim gate.** Each of the 2 STATIC strings renders byte-identical to its value in the JSON template. Compare the rendered string against the constant, not by eye. No substitution is permitted in any of them. Any delta FAILS - it means a run regenerated boilerplate (Editorial Guideline 8).
- **Generated-field allowlist.** The only per-episode generated content is `topic_phrase`, `setup`, `credential`, `prompt`, the attribute bullets, the Short-Form question sets with their bullets, and the outro's three lines. `cold_open` is a deprecated alias for `setup` and is not emitted on a new run; `need_to_know` and `examples` are retired, having lived in the cut Internal Notes block. Anything else differing from the template constants is drift.
- **Follow-ups gate** - `## Follow-ups` renders between the attribute bullets and `## Outro`. The note line and first bullet are byte-identical to the renderer constants; at least one generated bullet follows and prompts a topic-specific case study; zero question marks anywhere in the block. Missing section, empty `follow_ups`, or a question mark FAILS.
- **Placeholder gate** - grep for `{{...}}` returns ONLY the 12 approved tokens; zero invented tokens, zero `{{REGION}}`. Every placeholder appears bold.
- **Single prompt gate (hardened 2026-08-21)** - the Introduction contains exactly ONE bolded prompt paragraph, line 4. More than one FAILS. **AND: the `prompt` field contains AT MOST ONE `?`.** The canonical line 4 is a conditional plus an IMPERATIVE ask and carries ZERO question marks; two or more means a rider or a stacked ask was generated. (This check briefly required exactly one on 2026-08-21, which would have failed correct output - the imperative form has none.) **AND: grep `prompt` for `\bplease\b|\bif you have\b|\bif there'?s\b|\bfeel free\b|\bmaybe\b` - zero hits** (permission-softening, Guideline 9).
- **Intro content gate (Guideline 9)** - `setup` names the episode topic explicitly in its first sentence (the topic noun phrase must literally appear); `setup` carries at most ONE relatability clause after the topic; grep `setup` + `prompt` for `suddenly|out of nowhere|little did` (zero hits) and `\bactually\b|\breally\b|\btruly\b` (zero hits); `prompt` contains a 2-4 item scope list; numerals in spoken lines are spelled out. Any hit FAILS. The line 3 credential is not bold in full; only its placeholders carry bold, which is what keeps line 4 the single bolded prompt.
- **Introduction order gate** - the Introduction renders in exactly this order: STATIC `welcome` (line 1), generated `setup` (line 2, its own paragraph), generated `credential` (line 3, its own paragraph), generated `prompt` in full bold (line 4), then `ATTORNEY RESPONSE`. The beat direction sits between lines 3 and 4. No `INTERVIEWER` tag anywhere. A reordered or missing element FAILS.
- **Guest-framing gate** (hard). Grep the whole document, case-insensitive, for `my guest|our guest|today'?s guest|joining us|thanks for coming on`. Zero hits. The attorney owns the show; guest framing inverts the relationship.
- **Jargon scan** (hard, automatic before write). Grep the ENTIRE document above the `# Appendix: Source Question Bank` heading for statute-number patterns (`\b(Section|§|O\.C\.G\.A\.|CCP|FS|CPRC|CACI)\b`, `\d+-\d+-\d+`), `v\.` case-citation patterns, and the banned element-name list in Editorial Guideline 3. **Zero hits, with no exempt section** - Producer Notes no longer exists, so there is nowhere a citation is allowed. The appendix is scoped out because it carries n-gram rows verbatim and is never read on air; do not edit the bank to satisfy the scan.
- **Removed-section gate.** Zero occurrences of `Internal Notes`, `Attributes to Hit`, `Producer Notes`, `How This Episode Runs`, `The Lead-In`, `The Prompt` as a heading, `Interviewer: Live Checklist`, `Co-Host Notes`, or `Geo Rule` anywhere in the rendered document, plus zero per-question geo tag lines and zero per-question time budgets. Canonical list in `references/document-structure.md`. These were cut deliberately and reintroducing one is a format regression.
- **Attribute block gate** - ten to twelve bullets, each a bold lead-in plus one sentence of what to cover, ordered credentials through logistics, with ZERO question marks anywhere in the block. No `Attributes to Hit` heading. AT-1 and AT-2 are enforced mechanically by `scripts/build-ros-template-v2-docx.py` before any render work; AT-3 to AT-8 are in `references/attributes.md`.
- **Outro gate** - three GENERATED spoken lines in the order thanks-and-credit, sign-off, reach-out, with the sign-off deliberately not last. `{{STATE}}` and never `{{CITY}}` in line 3. Zero occurrences of "Case Engine". `outro_note` byte-identical. Gates OC-1 to OC-9 in `references/outro.md`.
- **Speaker tag gate** - `ATTORNEY RESPONSE` in the Introduction is the only speaker tag in the document. Zero `INTERVIEWER` tags: it was cut from both the Introduction and the outro on 2026-08-18.
- **Question count gate** - each location block carries EXACTLY ten questions, numbered `**Q1:**` through `**Q10:**`. Nine or eleven FAILS. Every location has the same count.
- **Bullet gate** - every Short-Form question renders fully bold and carries 2-4 bullets in `[{Label}]{.underline}: {detail}` form, labels underlined and never bold, and NOTHING else renders under a question: no time budget, no geo tag line, no source ref, no setup line. Zero question marks inside a bullet - a bullet says what to cover. See `references/short-form.md` gates SF-2, SF-3, SF-4.
- **Topic Plan reconciliation gate** (hard, pre-generation). The PUBLISHED Google Doc Topic Plan is the only authority - clients edit and veto questions there by hand and none of it propagates back to local `topic-plan-v{n}.json` or `.md` mirrors. Fetch the Doc live every run and record `topic_plan_doc_id`, `topic_plan_revision_id` and `topic_plan_fetched_at`. Every S2 question carries a `topic_plan_ref` to a live Doc row; the ten preserve the Doc's relative order; tail truncation is allowed but reordering and mid-sequence gaps are not; struck-through text is a veto and a vetoed question is never backfilled from the Appendix; a question with an unresolved Doc comment is flagged for review, not auto-included; where the local N-Gram Table disagrees with the Doc, the Doc wins and the table is updated. `metadata.json` records `topic_plan_reconciled` as `true` or `"legacy-exempt"`. Gates TP-1 to TP-6 in `references/short-form.md`. This gate exists because of the Eberst E5 incident on 2026-06-19, where an episode was built from a stale local mirror against a topic the live Doc no longer carried.
- **Geo distribution gate** (reads the JSON, not the Doc) - every question carries exactly one `geo_tag` from {CITY, CITY + REGION, REGION, NEUTRAL, STATE} in `ros-template-v2-data.json`, with exactly 3 city-tagged ranking targets per location. The `pod-2B` city-share percentage ceiling is NOT applied.
- **Read-through gate** (hard, LLM, runs LAST). Read the ENTIRE document top to bottom, in order, as one continuous piece, and read every spoken line aloud. Every sentence must parse on the first pass: no clause hanging off a noun phrase, no ambiguous antecedent, no main verb stranded more than roughly eight words from its subject. Two short sentences beat one long one. Check that the Introduction and the Outro, which are generated blind to each other, do not reuse the same phrase or credit, and that S1 and S2 agree on names, framing and tense. Output is a list of flagged lines with rewrites applied, not an opinion. A clean result that quotes nothing did not happen and must be re-run. **This is the only gate that requires judgment**, and it exists because on 2026-08-18 a generated line passed every mechanical gate while being a sentence no person would say out loud. See `steps/08-qa.md` tier 4.
- **Search-phrase gate** - no question contains a banned element name or reads as a legal category. Read each interpolated question aloud: could a person who has never spoken to a lawyer plausibly type it? A location label interpolated into a city slot ("a slip and fall lawyer in Public property in San Diego") FAILS here.
- **Question sourcing** - every question traces to n-gram substance via `source_ngram_ref`, or is an attribute question traceable to the attribute set. No untraceable questions.
- **Appendix completeness** - `# Appendix: Source Question Bank` carries EVERY n-gram row verbatim, renumbered 1..M. Count matches the n-gram table row count exactly.
- **Cover page gate** - the CE logo inline object is present (Drive id `1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2`, 180pt), the title reads `Run of Show` in CE Blue 24pt bold, and the episode title, `{practice area}  |  {scope}` line, and `Prepared by Case Engine` are all present and centered. A missing logo FAILS - the insert is a separate API call after the text batch and is the most likely piece to silently not land.
- **Heading color gate** - H1 section headers are CE Blue; H2 headings are CE_DARK (black), not blue. A blue H2 means the renderer regressed to the earlier styling.
- **Page break gate** - the cover, `S1: Long-Form` and `Appendix: Source Question Bank` each start on a new page. `S2: Short-Form (60-90s)` does NOT - it flows on from the S1 outro behind a horizontal rule, changed 2026-08-18. A page break before S2 means the renderer regressed.
- **Attribute provenance** - `metadata.json` records `attribute_source` (`pod-1D` or `static-fallback`) and `attribute_pull_date`. A static-fallback run carries an `> INFERRED:` flag.
- **Tokenization integrity** - zero hard-coded firm / attorney / city / state names in the body. The region IS hard-coded plain text and is the sole exception, by design.
- **Branded render** - the Doc was built by the bundled renderer. Zero leaked inline markup as visible text (`[...]{.underline}`, `<u>`, `**` rendering literally).
- **Schema validate** - `ros-template-v2-data.json` validates against `references/schema/ros-template-v2.json`.
- **Provenance present** - `metadata.json` carries the provenance block (see `## INTERNAL`).
- **Artifacts present** - markdown, JSON, metadata all written; branded Google Doc exists.
- **No em dashes** - plain hyphens only anywhere in the output.

### Gotchas

Failure modes that are warnings, not enforceable rules.

#### Downstream changes required before ship - ALL CLEARED 2026-08-18

The four blockers declared at v1.0.0 are all resolved. Kept here as the record; details in `references/iteration-log.json` entries 2026-08-14-001 through -004.

- **`pod-3B-client-ros` populate taxonomy** - RESOLVED by building the sibling `pod-3B-client-ros-v2` v1.0.0 (legacy skill untouched; both coexist behind `episode_format`). It populates the eleven-token v2 taxonomy including `{{YEARS_PRACTICING}}`, strips `# Appendix: Source Question Bank`, preserves per-question `geo_tag` + `source_ngram_ref` into `client-ros-v2-data.json`, and enforces a statics-resolved-verbatim gate.
- **`pod-3A-ros-template` placeholder gate** - FALSE ALARM, verified 2026-08-18. The taxonomies were never shared: the legacy skill carries its own 12-token list inline and never reads v2's. The two ARE separate per-format taxonomies; each populate skill mirrors only its own format's list.
- **`pod-2B-n-gram-table` city-share ceiling** - VERIFIED NON-ISSUE 2026-08-18. The ceiling is a QA gate on 2B's own table output, never applied downstream to a v2 S2 block, and v2's 3-of-10 city-tagged mandate (30%) sits inside 2B's band anyway. `references/short-form.md` states the ceiling is not applied to v2 blocks.
- **`pod-3C-client-guide`** - RESOLVED by building the sibling `pod-3C-client-guide-v2` v1.0.0 (legacy skill untouched). The v2 guide layout is rebuilt for the v2 episode shape - the prompt verbatim, the What to Cover attribute list, per-city quick-answer rounds - and carries the attorney-relevant half of this skill's Production notes via its `references/production-notes.md`.

#### Ordinary gotchas

- **Don't proceed with a parent-scope N-Gram Table or entity map.** If a Location-level table is expected but only Topic Only exists, running with the mismatch is a silent localization leak. Stop and run the upstream skill at the matching scope.
- **Don't let the prompt get "improved" into a question list.** The single most likely failure across future edits is someone adding a second and third prompt to Segment 1 because the silence feels risky. The silence IS the format. Adding prompts converts v2 back into legacy with fewer questions.
- **Don't narrow the prompt in the room.** The doc must say this and the interviewer must be trained on it: after the prompt, stop talking. Do not offer an example to get them started. Three full seconds of silence before any intervention, because most people restart on their own.
- **Don't reintroduce a Producer Notes block.** Earlier drafts had one and it was cut. The pull to add it back is real, because the jurisdiction research has to go somewhere and a notes section feels like the obvious home. It goes into the writer's head and out through the attribute bullets and the Short-Form bullets in plain language, not onto the page as citations.
- **The static attribute set will go stale.** It is a 2026-08-14 snapshot of live answer-engine output. Answer engines change. Treat a fallback run as Inferred and prefer a fresh `pod-1D-attribute-research` pull whenever one exists.
- **The Client ROS and Client Guide are NOT this skill's output.** This skill writes only the tokenized v2 template into the shared template library scope folder (Map 2).
- **Branded output is mandatory.** Do NOT upload raw markdown as a Google Doc. The pipeline is `markdown → build-ros-template-v2-docx.py → DOCX → Drive upload as gdoc mimeType → clean branded Google Doc`. The `.md` sibling is uploaded as `text/markdown` with no conversion.

### Iteration log

The skill's institutional memory. Append-only record of bugs, papercuts, drift, and fixes spotted across runs.

- **File:** `references/iteration-log.json` (validates against `references/schema/iteration-log.schema.json`).
- **Read-at-start contract:** `## Checks -> ### Probe environment` reads the log, filters to `status: open` and `status: in-progress` entries, and surfaces them to the agent as known issues to watch for. One file read per run.
- **Write semantics:** never written at runtime. New entries appended manually post-run. Append-only, never edit or delete past entries. ID format `YYYY-MM-DD-NNN`.
- **Size limit:** soft cap of 50 entries with `status: open` or `in-progress`. Archive resolved + old entries to `references/iteration-log-archive-{YYYY-Q#}.json` when exceeded.

---

## Standard Operating Procedure

```
Multi-mode:  [Checks] -> [Prepare Inputs] -> [Create | Update] -> [Quality Assurance] -> [Ship]
```

## Checks

What is?
The pre-flight phase - locks in which capabilities are reachable, resolves the format flag, orients to the right scope folder, verifies the upstream N-Gram Table and entity map exist, and decides whether this run creates a new template or updates an existing one.

### Probe environment

What is?
The runtime capability lock-in - probe which ingestion sources, write destinations, and credential-bearing capabilities are reachable right now, read the iteration log, and persist the result so downstream phases consume the lock-in instead of re-probing.

- **Read the iteration log.** Read `references/iteration-log.json`, filter to entries with `status: open` or `status: in-progress`, surface them to the agent as known issues to watch for this run. The four `critical` entries (the former downstream ship blockers) all resolved 2026-08-18 - two by the new `pod-3B-client-ros-v2` / `pod-3C-client-guide-v2` siblings, two verified as false alarms.
- **Probe ingestion capabilities** (`### Inputs -> #### Capabilities` tiers): local filesystem read against the canonical Desktop deliverables path; `gws drive about` as a try-and-succeed probe for Drive reach; tool-availability check for `mcp__ce-services__rag_query`. Probe capability, never environment name - the same body runs wherever it is invoked.
- **Probe output destinations** (`### Outputs -> #### Capabilities`): filesystem write test against the local mirror path, and Drive write reach. If neither resolves, the skill still drafts and renders the deliverable in-conversation rather than losing it.
- **Probe the render path**: confirm `python-docx` is importable for `scripts/build-ros-template-v2-docx.py`. Absent, the markdown and JSON still ship and the branded Doc is deferred with the gap surfaced in the report - never silently skipped.
- **Persist** the active capability list to `metadata.json` under `runtime.capabilities` with a `probe_timestamp`. Downstream phases reference it rather than re-probing.

If no Drive and no local filesystem are reachable, degrade to conversation-only: render the template body inline and tell the user it was not persisted.

### Resolve the format flag

What is?
The coexistence gate - resolve `episode_format` and refuse to run on any client not explicitly flipped to v2, before any read of the research artifacts.

- **Ask the user outright:** "Is this episode running the **v2 open-interview format** or the **legacy segmented format**? (`v2-open-interview` / `legacy-segments`)". If `podcast-overview.md` is reachable and carries an `episode_format` field, pre-fill from it and confirm the value back in one line rather than asking cold - but the user's answer is what resolves the gate.
- `v2-open-interview`, explicitly confirmed -> continue.
- `legacy-segments`, "not sure", blank, or no answer -> STOP. Report the resolved value and route the user to `/pod-3A-ros-template`. Do not offer to build v2 anyway. Absence of an answer is never permission.
- Record the resolved value and its source - `user` (with who answered) or `podcast-overview` (with the path) - in `metadata.json -> episode_format_source`.
- *Temporary manual ask: the format flag has no database home yet, so it is a run-time question until one is wired up.*

### Orient

What is?
The orientation step - read the iteration log, resolve the correct destination folder, and load the podcast architecture context before producing anything.

- If `podcast-overview.md` is reachable, read it and auto-fill Greeting questions 1-6 (format flag, client name, anchor scope, cities, region phrasing); confirm in one line. Otherwise ask.
- Resolve the destination folder - ALWAYS the shared template library per Map 2. If the chain does not exist, create it. The Canonical destination gate hard-asserts this before any write.
- **Check for a legacy sibling.** Look for an existing legacy `ROS Template` in the same scope folder. Its presence is normal and expected. Note it, leave it alone, and confirm the v2 filenames will not collide.
- Read `references/examples/ros-template-v2-examples.md` and pick 1-2 examples matching the requested scope as quality anchors. If the file is empty, proceed on the `## INTERNAL` reference material alone and flag `"references": "empty"` in `metadata.json`.
- Read `references/prompts/README.md` for the section generation order and the five global gates. The individual section prompts are read later, each at the moment its section is generated.

### Verify upstream dependencies

What is?
The hard-dependency gate - confirm the matching-scope N-Gram Table and entity map both exist before any generation, and refuse to run on a parent-scope artifact.

- **Episode 1 / Founder Story exception (check FIRST):** if the requested episode is Episode 1, this skill does not generate anything, regardless of format flag. Route the user to `/pod-3B-client-ros` to populate the firm's copy from the fixed Founder Story template.
- Resolve `n-gram-table.json` at the matching scope. If missing, STOP and route to `/pod-2B-n-gram-table`.
- Resolve `entity-map.json` + `entity-clusters.md` at the matching scope. If the map is missing, STOP and route to `/pod-1A-entity-research`. Do not substitute a parent-scope map.
- Resolve `attribute-research.json` from `/pod-1D-attribute-research` if it exists. Absence is fine and routes to the static fallback; record which was used.
- **Handoff Contract check.** Verify upstream paths match the declared Inputs. If `keyword-research.json` or any other undeclared upstream file shows up and is under consideration, STOP and ask: "I see upstream output at {path} but my Inputs contract doesn't declare it as required. Should I (a) mine it for Segment 2 phrasing, (b) skip it, or (c) pause while you update the handoff contract?" Do not guess silently.

### Existence check

What is?
The mode router - decide whether this run creates a new v2 template or updates an existing one.

- Look for a `ROS Template v2` Google Doc + `ros-template-v2-data.json` inside the resolved destination folder. A legacy `ROS Template` does NOT count as an existing v2 template.
- **Missing:** no prior v2 artifact - route to `## Create`.
- **Found:** surface provenance (existing `metadata.json` run date, city count, question count) and ask: refresh in place / archive-and-rebuild / cancel.
  - Refresh in place -> route to `## Update`.
  - `archive-and-rebuild` -> move ONLY the prior v2 ROS Template file to `_archive-{YYYY-MM-DD}/` and route to `## Create`. Legacy siblings and Client ROS / Client Guide artifacts are left untouched.

## Prepare Inputs

What is?
The input-preparation phase - load and validate the N-Gram Table, entity map, clusters, optional keyword and attribute research, and branding into a working set ready for the Create or Update phase.

Work through the input sources in priority order; on a tool error, skip that source and degrade to the next.

- **Load the N-Gram Table.** Parse `n-gram-table.json`. In v2 the Question Text column is source material for Segment 2 rephrasing and ships verbatim in the Appendix. It is not the script.
- **Load the entity map.** Parse `entity-map.json` - confirm it carries the localized entity set at the matching scope. The entities ground what the writer knows to be true locally; they never reach the page as named terminology.
- **Load entity clusters.** Parse `entity-clusters.md` when present - the clusters deepen the writer's jurisdictional grounding.
- **Load the attribute set.** Parse `attribute-research.json` from `/pod-1D-attribute-research` when present (Confirmed). Otherwise load `references/attributes/attributes-fallback.json` and mark the run Inferred with the fallback's `pull_date`.
- **Load keyword research (optional).** If the Handoff Contract check approved using `keyword-research.json`, parse it for real query strings to shape Segment 2 phrasing and for the Appendix.
- **Resolve the geo pairing.** Confirm the city (Episode geo target) and the plain-text region phrasing. If the region was not confirmed by the user or found in podcast-overview, propose one and mark it `> NEEDS CONFIRMATION:`.
- **Resolve branding.** Read the Case Engine Branding folder (id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`) - logo, colors, fonts, the Cover Page Spec. Hold the resolved values for `## Ship`. A per-client `brand.json` typography block overrides the CE default when present.
- **Load calibration examples.** Hold the 1-2 scope-matched examples from `references/examples/ros-template-v2-examples.md` as quality anchors.

## Create

What is?
The create branch - builds the tokenized v2 template from scratch when no prior v2 template exists, producing a schema-valid `ros-template-v2-data.json` plus its markdown source and metadata.

**Best Practices.**
These apply to the entire create phase and should be checked after each step.

- Segment 1 gets exactly one prompt, in Cyle's shape, as Introduction line 4, and the duration is always a range (Quality bar, Editorial Guideline 4).
- No jargon anywhere above the Appendix; there is no exempt section (Editorial Guideline 3).
- Segment 2 questions are search phrases with exactly one geo tag each (Editorial Guidelines 5 and 6).
- Only the 12 approved placeholders; the region is plain text (Editorial Guideline 1).
- Hold the scope-matched calibration examples in view while generating.

If the model generates output that violates any of these, emit a `> NEEDS VERIFICATION:` block at the offending location instead of shipping the claim.

**Generate section by section, in the fixed order.** The body is not written in one pass. `references/prompts/` carries a live generation prompt per section (01 Introduction, 02 Attributes, 03 Short-Form Questions, 04 Cover Page, 05 Outro), each with its own rules, GOOD / BAD pair, mechanical gates, and a repair instruction per gate. The order is fixed because each section constrains the next - the setup paragraph must not repeat the STATIC welcome, the prompt works the territory the Introduction named, and the Short-Form questions draw on the attribute set from 04. Read `references/prompts/README.md` for the order and the five global gates, then read each section's prompt at the moment that section is generated. Run the section's gates before moving to the next; a failed gate is repaired in place, not deferred to QA. The SOP steps below describe WHAT each section contains; the prompt files carry HOW to generate it.

### Generate the cover page

What is?
The pass that emits the branded cover block - logo, title, episode title, and scope line - built to the CE deliverable cover spec (inlined below and in Editorial Guideline 4) so every CE deliverable opens the same way.

- Emit two spacer paragraphs, then the CE logo inline at the second paragraph (Drive id `1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2`, 180pt wide), then a third spacer.
- Then `Run of Show` (CE Blue, 24pt, bold), the episode title (dark, 18pt, bold), a spacer, `{practice area}  |  {scope}` (dark, 14pt), a spacer, and `Prepared by Case Engine` (11pt). All centered, Roboto.
- Page break after the cover so `S1: Long-Form` starts on its own page.
- **The logo insert is a separate API call after the text batch lands.** It is the piece most likely to silently not appear, which is why the cover page gate checks for the inline object rather than assuming it.

### Generate S1 Long-Form

What is?
The pass that writes the interview - the four-line Introduction with its single prompt, then the attribute block.

- **`## Introduction (45-60s)`, in this exact order:** the STATIC `welcome` string byte-identical (line 1), the generated `setup` paragraph (line 2), the generated `credential` paragraph (line 3), the `prompt` in full bold (line 4), then `ATTORNEY RESPONSE`. The beat direction sits between lines 3 and 4. There is NO `INTERVIEWER` tag. The order is a gate; do not rearrange it.
- **Nothing substitutes into the welcome.** `{topic_phrase}` left it on 2026-08-18 when the constant shrank to line 1. `topic_phrase` is still generated - it is the episode's subject as a plain phrase, and it feeds line 2's subject slot and the outro's topical credit approach.
- **The setup is line 2, its own paragraph.** Host ID first and alone, then the topic named plainly, 25 to 30 words, no greeting of its own (the greeting is the STATIC welcome immediately above it). Opener varied per the bank in `references/introduction.md`; NO geo in line 2 and NO insight-spoiling hook - the state moved to line 3, the EEAT line (Gabe 2026-08-26).
- **The credential is line 3, its own paragraph.** One frame from `references/introduction.md`, under 25 words, spoken directly to the attorney. Not bold in full - only its placeholders carry bold, which is what keeps line 4 the single bolded prompt. This is the only place in S1 where `{{CITY}}` is allowed.
- **The prompt - exactly one, line 4, in full bold.** Cyle's shape, with the topic and situation clauses swapped for this episode:

  > You have been serving **{{CITY}}** and the surrounding cities as an attorney for **{{YEARS_PRACTICING}}** years. What do people actually need to know if they **[THEME]**? And what have you done in the past for clients who **[SITUATION]**? Give us the facts, what they need to do right this second, and then give us an example or two of cases your firm has worked on so people understand the journey they are about to go through.

- **The attribute bullets** sit directly under the `ATTORNEY RESPONSE` tag, per Editorial Guideline 7 and `references/attributes.md`. Ten to twelve, each a bold lead-in plus one sentence of what to cover, ordered credentials through logistics, zero question marks anywhere in the block.
- **No heading above them and no divider below.** `Attributes to Hit`, the STATIC `attr_intro` / `attr_note_internal` / `attr_sources_internal` lines, and the whole `### Internal Notes (not read on air)` block with its three moves, need-to-know bullets and source-consistency counts were all retired 2026-08-17. The removed-section gate greps for them. Do not restore any of it, and do not restore the older `## How the Attorney Should Answer` heading either.

### Generate S2 Short-Form

What is?
The pass that builds the per-location question sets - exactly ten bare questions per location, built on search phrases and governed by geo treatment that never prints.

- A horizontal rule after the S1 outro, then the S2 heading. **S2 does not start its own page.** Emit the one shipped direction line under the heading; the two STATIC short-form mode notes were retired 2026-08-17.
- **`## Location: {{CITY}}`** per location, then exactly ten questions, each rendered fully bold with its `Q{N}:` label inside the bold, each carrying 2 to 4 bullets in `[{Label}]{.underline}: {detail}` form with the label underlined and never bold. Nothing else renders under a question - no geo tag, no answer note, no time budget, no source ref.
- Build the mix per Editorial Guideline 5: three city-tagged ranking targets that change per location, seven attribute questions that mostly carry over.
- Record `geo_tag` and `source_ngram_ref` per question in `ros-template-v2-data.json`. The tag governs how the question was written and is what the geo distribution gate reads; it never reaches the page.
- Rephrase from n-gram substance into search phrasing. Mine `keyword-research.json` when available - a real query beats a plausible one.
- **Read every interpolated question aloud before accepting it.** A location label dropped into a city slot ("a slip and fall lawyer in Public property in San Diego") is the failure this catches. If a location has no real city name, it does not get city-tagged questions.

### Generate the outro and appendix

What is?
The pass that closes the episode and ships the internal question bank.

- **`## Outro`** - the three GENERATED lines in order: thanks and credit, sign-off, then the reach-out tag. NO speaker tag; the `INTERVIEWER` tag was cut 2026-08-18. It closes S1 and renders above the S2 divider. The sign-off is deliberately not last. Generated per episode against the beats and banks in `references/outro-banks.json`; reasoning and gates OC-1 to OC-9 in `references/outro.md`.
- **`# Appendix: Source Question Bank`** on its own page - every n-gram row, verbatim and unedited, renumbered 1..M, marked INTERNAL. It is the audit trail that nothing was dropped or invented and the pull pool when a client rejects a question.
- Do not edit bank rows to satisfy the jargon scan. The scan is scoped to everything above this heading precisely because the bank is verbatim.

### Run the jargon scan

What is?
The gate that catches legal terminology leaking into anything the attorney or interviewer reads.

- Run the jargon scan per `### Quality gates` - statute-number patterns, case citations, rule names, and the banned element-name list from Editorial Guideline 3.
- Any hit above the `# Appendix: Source Question Bank` heading fails. Rewrite that piece in the words a person uses, keeping the substance.
- Scope the scan to exclude the Appendix, which carries n-gram rows verbatim and is never read on air. Do not edit bank rows to make the scan pass.
- Record the jargon scan result (PASS / FAIL + pieces rewritten) for `metadata.json`.

### Render markdown and payload

What is?
The pass that assembles the final artifacts.

- Assemble the ROS Template v2 `.md` in the locked order per Editorial Guideline 4, then the `## INTERNAL` block.
- Serialize `ros-template-v2-data.json` per `### Outputs -> #### Schema` - placeholder inventory, Segment 1 blocks, Segment 2 city blocks with per-question geo tags and `source_ngram_ref`, duration band, episode goal, scope, region.
- Write `metadata.json` with the provenance block per `## INTERNAL` - sources, counts, scope, episode goal, geo plan, attribute source + pull date, jargon scan result, references status, `episode_format_source`.

## Update

What is?
The update path - modifies an existing v2 template in place when a prior v2 version exists, preserving any manual edits the producer made since the last skill run.

**Best Practices.**
These apply to the entire update phase and should be checked after each step.

- **Diff before write.** Pull the existing `ros-template-v2-data.json` + `.md`, compare against the proposed new state, surface every changed block before committing the write.
- **Preserve manual edits.** Any prompt wording, setup or credential line, attribute detail, Short-Form question, bullet, or outro line that was manually edited since the last skill run keeps its current value. Never auto-overwrite a manual edit silently. The prompt and the credential get edited by hand more than anything else in this format, and the outro's three lines regenerate on every run by design, so a diff there is expected rather than a change worth applying. Full procedure in `steps/update-mode.md`.
- **Flag merge conflicts inline.** When a new auto-generated value disagrees with a preserved manual edit, emit `> NEEDS VERIFICATION: auto-generated value [X] conflicts with manual edit [Y]` at the location.
- **Stable fileId.** Update uses `files.update` against the existing `ROS Template v2` Google Doc fileId. Never create a new Doc; never delete-and-recreate.

If the model proposes overwriting a manual edit without flagging it, halt and emit `> NEEDS VERIFICATION:` instead of shipping the change.

### Diff against existing

What is?
The pass that loads the prior v2 template and computes a block-level diff against the proposed new state.

- Read the prior `ros-template-v2-data.json`, `.md`, and `metadata.json` from the resolved destination folder. Never read the legacy sibling as if it were the prior version.
- Read the prior provenance block to recover the last run's upstream sources, attribute source and pull date, city list, and question counts.
- Run the Create-phase passes to compute the proposed new state.
- Compute the diff: Segment 1 blocks changed, questions added / removed / rephrased per city, geo tags changed, attribute set changed (and whether the source moved from static fallback to a live `pod-1D` pull), Appendix bank rows added or removed.

### Merge and resolve conflicts

What is?
The pass that merges new content into the existing template - manual edits preserved, conflicts flagged.

- Apply the phase-level Best Practices: preserve every manually-edited piece; merge new auto-generated content; drop content the new source set retired.
- Where a new auto-generated value disagrees with a preserved manual edit, emit the `> NEEDS VERIFICATION:` conflict block inline; do not auto-resolve.
- Re-render the `.md`, `ros-template-v2-data.json`, and `metadata.json`. Bump the run date and append the run to the provenance history.
- The shared `## Quality Assurance` phase runs after this phase.

## Quality Assurance

What is?
The gate before `## Ship` - a three-tier check (Best Practices by name, the hardwired Anti-AI Detection two-pass scan, then skill-specific mechanical checks) that runs after whichever branch fired.

**First - check against Best Practices.** The deliverable must align with the contract defined upstream in this file.

- **Quality bar** (Best Practices -> Quality bar) - 12 placeholders only, exactly one prompt, duration as a range, a credential line that does real work, zero jargon attorney-facing, search-phrase questions, one geo tag each, branded Google Doc, no em dashes.
- **Sourcing discipline** (Best Practices -> Sourcing discipline) - every Appendix row Confirmed against the N-Gram Table, every Segment 2 question traceable via `source_ngram_ref` or the attribute set, the static attribute fallback flagged `> INFERRED:` with its pull date, unconfirmed region phrasing flagged `> NEEDS CONFIRMATION:`.
- **Editorial Guidelines** - Guideline 1 (12 placeholders, region not a token), 2 (episode-goal slice), 3 (no jargon attorney-facing), 4 (locked structure), 5 (search phrases, bank is source material), 6 (geo pairing and tags, ceiling not applied), 7 (attributes).
- **Quality gates** - full checklist must pass: format flag, canonical destination, legacy non-collision, STATIC verbatim, generated-field allowlist, placeholder, single prompt, Introduction order, speaker tag, attribute block, outro, removed-section, jargon scan, geo distribution, search-phrase, question count, bullet, question sourcing, Topic Plan reconciliation, Appendix completeness, attribute provenance, cover page, heading colors, page breaks, tokenization integrity, branded render, schema validate, provenance present, artifacts present, no em dashes, read-through.

**Second - Anti-AI Detection two-pass scan** (canonical doc: https://docs.google.com/document/d/1hp7bxOFRlMhCuhjHNY0j05JrB97-KOFD0XUCQM3gMBU/edit). Mandatory for every text-producing skill. Run the full Section 7 two-pass audit against the deliverable:

- **Pass 1 (mechanical scan):** em-dashes, banned vocabulary (Section 2), banned phrases (Section 3), triadic rhythms and symmetric paragraphs (Section 4), summary-only section closers, date formatting per destination, specific-claims-trace-to-source, no emojis (unless requested), no clickbait.
- **Pass 2 (skeptical re-read):** restart from the top. Did I actually check every line, or skim? Em-dashes I missed? Banned phrases I rationalized? Triadic rhythms left because they "sounded fine"? Generic setup text that should be specific? Am I sure?
- **On any hit:** fix and re-run Pass 2 until clean. One pass is not enough.
- **v2-specific spoken-language check.** This format is spoken aloud more than any other CE deliverable. Read the setup, the credential, the prompt, the three outro lines, and three Segment 2 questions out loud. Anything that only works on the page fails.

**Third - skill-specific mechanical checks.**

- `ros-template-v2-data.json` validates against `references/schema/ros-template-v2.json`. If the schema file is absent, log `schema_status: missing` and proceed.
- All 2 STATIC strings render byte-identical to the JSON template constants. Nothing substitutes into any of them.
- Grep for `{{...}}` returns ONLY the 12 approved tokens - zero invented tokens, zero `{{REGION}}`. Every placeholder appears bold.
- Exactly one bolded prompt paragraph in the Introduction, and the Introduction renders in the locked order - welcome, setup, credential, prompt, `ATTORNEY RESPONSE` - with no `INTERVIEWER` tag anywhere in the document.
- Jargon scan PASS - zero statute numbers, case citations, or element names anywhere above the Appendix heading.
- Zero occurrences of the removed sections: `Internal Notes`, `Attributes to Hit`, `Producer Notes`, `How This Episode Runs`, `The Lead-In`, `The Prompt` as a heading, `Interviewer: Live Checklist`, `Co-Host Notes`, `Geo Rule`.
- Every location set carries exactly ten questions, `**Q1:**` through `**Q10:**`, each fully bold and each carrying 2 to 4 underlined-label bullets, with no geo tag line, answer note, source ref, or time budget rendered under any of them.
- The attribute block is ten to twelve bullets with zero question marks anywhere in it (AT-1, AT-2 - both enforced by the renderer before it writes anything).
- `ros-template-v2-data.json` carries a `geo_tag` on every question with exactly three city-tagged ranking targets per location.
- Appendix row count equals the n-gram table row count exactly.
- Cover page carries the CE logo inline object, the CE Blue 24pt title, the episode title, the `{practice area}  |  {scope}` line, and `Prepared by Case Engine`.
- H2 headings render CE_DARK, not CE Blue. H1 section headers render CE Blue.
- The cover, `S1: Long-Form` and `Appendix: Source Question Bank` each begin on a new page. `S2: Short-Form (60-90s)` does NOT - it flows on from the S1 outro behind a horizontal rule.
- Zero hard-coded firm / attorney / city / state names in the body (the region is the sole intentional plain-text exception).
- Zero leaked inline markup as visible text in the rendered Doc.
- No write path collides with a legacy artifact name.
- `metadata.json` provenance block present with at minimum: `run_date`, `episode_format`, `episode_format_source`, `n_gram_source`, `entity_map_source`, `attribute_source`, `attribute_pull_date`, `episode_goal`, `references_status`, `location_count`, `appendix_row_count`, `placeholder_count`, `jargon_scan`, `static_verbatim`, `geo_plan`.
- Both write destinations verified: Drive shared-library scope folder AND local mirror contain the same artifacts.
- Canonical destination gate PASSED.
- INTERNAL section grep test: `grep -L "## INTERNAL" {client-facing-export}` returns zero hits for the client-facing Google Doc.

**On failure:** fix the markdown, regenerate `ros-template-v2-data.json` and `metadata.json`, rebuild the DOCX, re-upload via `files.update`, re-run all checks. Do not proceed to `## Ship` until QA returns clean.

## Ship

What is?
The publish phase - builds the CE-branded DOCX, writes the trio plus `metadata.json` to the shared template library scope folder (Map 2) at every scope, and mirrors the same artifacts locally. Never writes into a client/firm episode folder and never overwrites a legacy artifact.

### What ships

- **ROS Template v2** - Google Doc - human-facing CE-branded view, cover page, Roboto typeface, stable fileId.
- **ROS Template v2 `.md`** - Markdown - raw tokenized source-of-truth, retains the `## INTERNAL` block.
- **`ros-template-v2-data.json`** - JSON - machine-readable payload, downstream-consumed by `pod-3B-client-ros`.
- **`metadata.json`** - JSON (internal) - provenance.

### Where it ships

- **Drive:** the shared template library scope folder at every scope - `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{Topic Only | Locations/{Location} | Extensions/{Location}}/` (Map 2). Never a client/firm episode folder.
- **Local mirror:** `~/Desktop/claude_code/deliverables/podcast/ROS Templates/{Topic}/{Episode}/{scope}/` - written every run.
- **Schema:** `~/.claude/skills/pod-3A-ros-template-v2/references/schema/ros-template-v2.json`.

### How it ships

Write to both destinations. On a write error to one, ship to the other and report the partial state.

- **Build the CE-branded DOCX.** Run `scripts/build-ros-template-v2-docx.py` to emit both the `.docx` and the paired `.md` in one pass. The script reads `ros-template-v2-data.json`, translates pandoc inline markers (`[text]{.underline}` → a real Word underline run in the DOCX; stripped to plain `text` in the paired `.md`), preserves `{{PLACEHOLDER}}` tokens verbatim, and applies CE branding per the Case Engine Branding folder (Roboto throughout).
- **Cover page.** Render per the canonical [Cover Page Spec](https://docs.google.com/document/d/1oydpI055jbj1FYDGeZfHQeMNjaWKUCFVGCRveeuJJCk/edit), with one override - the body and cover-page font is Roboto (if the spec still says Calibri, Roboto wins; flag the discrepancy when you spot it). Title `Run of Show` (CE Blue, 36pt, bold, Roboto). Subtitle is the practice area. The template is brand-agnostic and tokenized, so the firm name is NEVER on the cover. Footer `Case Engine  |  Confidential  |  Page {PAGE}`.
- **Canonical styling** - Title 36pt bold dark; H1 20pt bold CE Blue; H2 16pt bold CE Blue; H3 13pt bold dark; instruction lines 11pt italic CE Gray; body Roboto 11pt dark.
- **Drive write.** Upload the `.docx` as `application/vnd.google-apps.document` so Drive auto-converts it to a clean branded Google Doc. Upload the `.md` as `text/markdown` (no conversion). Upload the JSONs as-is. First-time create uses `files.create`; subsequent writes use `files.update` against the existing fileId. Never re-upload the `.md` with `convert=true` to make a second Google Doc.
- **Roboto pass.** After upload, confirm Roboto over the full document range.
- **Archive.** If the existence check moved a prior v2 template to `_archive-{YYYY-MM-DD}/`, the archive folder ships alongside. Archive ONLY the prior v2 file - legacy siblings and Client ROS / Client Guide slots are untouched.
- **Local mirror write.** Write the same `.md`, `.docx`, and JSONs to the local mirror path. If the Drive write fails but the local write succeeds, surface the partial state.
- **Report back:**

  ```
  Done. ROS Template v2 - {Topic} / {Episode} ({Scope}{, Location if applicable}).

   Folder: https://drive.google.com/drive/folders/{folder_id}
   ROS Template v2 (branded Google Doc): https://docs.google.com/document/d/{doc_id}

  Format: v2 open interview. Segment 1: one prompt, {low} to {high} min.
  Segment 2: {city_count} cities x {questions_per_city} questions.
  Geo: {city} paired with {region}. CITY-tagged: {n}. Appendix bank rows: {m}.
  Placeholders used: {N}/12. Attribute source: {pod-1D | static-fallback {date}}.
  Episode goal: {goal}. Jargon scan: PASS. QA gate: PASS.

  Next: /pod-3B-client-ros-v2 populates the placeholders for the firm (all twelve
  tokens, Appendix stripped, geo tags preserved). That is the FINAL step of the v2
  branch - nothing runs downstream of it.
  ```

### Who to Notify

`notify: []` - this skill posts no notifications. The producer is informed via the inline report-back above.

---

## INTERNAL (not for client distribution - auto-stripped from all exports; the Formatting Guide rulebook and worked examples ride into the local markdown only, never into the Drive Doc)

### Formatting Guide (internal renderer rulebook - NEVER a deliverable section)

The authoritative rulebook the renderer honors. It governs how the document is written; it never appears in the produced document. The rules are the body of `### Editorial Guidelines -> Guideline 4` - speaker tags, bold, instruction lines, no em dashes, bold tokens throughout. Internal calibration only.

### Why the format changed (keep this - it prevents well-meaning regressions)

The legacy twenty-question format produced answers that sounded like testimony. Every question scoped the answer, so nothing ran long enough to become a story, and the attorney's authority never got established because it was never asked for directly. v2 fixes three things at once: the line 3 EEAT line establishes authority before anything is asked, the single prompt gives the attorney room to actually talk, and the prompt's question-shaped beats (definition, difference, challenges - Gabe 2026-08-26) tell them what a good long answer contains so the room is not just empty. If a future edit adds a second prompt to Segment 1 "for safety", it has undone the whole thing.

### Production notes (INTERNAL to this template, never into the ROS body)

> **2026-08-21:** these notes previously routed downstream to `pod-3C-client-guide-v2`, which is now retired (v2 ends at Client ROS). They stay in this template's `## INTERNAL` block. **OPEN ITEM for Gabe:** the interviewer coaching in this section no longer has a downstream consumer - decide whether `pod-3B-client-ros-v2` should carry it into the Client ROS `## INTERNAL` block, since the Client ROS is now the interviewer's only document.

Guidance from the 2026-08-14 call that used to live in the deliverable as `Interviewer: Live Checklist` and `Co-Host Notes`. Those sections were cut from the ROS because the ROS is a recording script and this is coaching. The guidance itself is still real and still load-bearing, so it lives here and reaches people through `pod-3C-client-guide` and host onboarding instead of cluttering the page the interviewer is reading on mic.

**Interviewers must stop reading the ROS verbatim.** This is the current failure, stated plainly on the call: they read it, and it sounds like they are reading it. The document is a shape, not a script. Understand the premise of the section, then say it in your own words with your own personality. The one thing that IS verbatim is the prompt, because its construction is what earns the long answer. Everything else is direction.

**Co-hosts should be themselves and should not study up.** Not knowing the material is the qualification, not a gap - it is what lets them ask what a listener would actually ask. React honestly when something lands as surprising. The target register, verbatim from the call:

> "so basically you're going to help me get the police report and help with my medical bills, and you guys don't even take any money unless you win my case, then you just get a percentage."

That is the level to aim at. It restates the value in the listener's own words and does more work than a paragraph of explanation.

**Three to five additional shorts come out of the long-form segment in post,** on top of the ten per location set. The contract commits to ten; we deliver roughly twenty. The long-form answer reliably contains several self-contained 60 to 90 second passages, and pulling them is an editing task, not a recording task. Do not plan the interview around producing them and do not interrupt to set one up - they are found in the edit, not staged in the room.

**Editing is asymmetric between the two segments.** S1 needs only ums and ahs removed; leave the pacing, the pauses, and the thinking intact, because that is what makes it sound like a conversation rather than a read. S2 is align the question to the answer, pick the good take, move on.

**Retakes in S2 are expected and encouraged on the spot.** If a take comes out flat, say so and go again immediately. Attorneys who believe they get one shot per question perform worse on every question. The mode note in the deliverable says this; reinforce it verbally before the segment starts.


### Producer targets

- **Naturalness over coverage.** If an attribute feels forced, let it come up naturally later or let the interviewer fill it at the end. A forced attribute costs more than a missed one.
- **The Introduction is the highest-leverage forty-five seconds in the episode.** It gets more editing attention than anything else in the document.
- **Segment 2 clip parity.** Every city block must produce the same set of clips. That is the point of holding the question shape constant across cities.

### Segment pacing reference

S1 Long-Form: 15 to 30 minutes, one prompt, no internal time budgets. S2 Short-Form: ten questions per location at 60 to 90 seconds, so roughly 10 to 15 minutes per set allowing for retakes. A two-location episode lands around 45 to 60 minutes of tape for roughly 30 minutes of usable long-form plus 20 clips (the 20 questions recorded, plus 3 to 5 more pulled from S1 in post).

### Geo pairing reference

The pairing construction is `in {city} and across {region}`, and it governs how questions are written rather than appearing as a printed tag. The region is fixed by the template's location scope. Worked examples from the 2026-08-14 build: Riverside / the Inland Empire; Savannah / Chatham County and coastal Georgia; Baltimore / the Baltimore metro and central Maryland; Boca Raton / Palm Beach County and South Florida; Fort Worth / Tarrant County and North Texas; San Diego / San Diego County and Southern California.

### Provenance block

`metadata.json` must include: `run_date`, `episode_format`, `episode_format_source`, `n_gram_source`, `entity_map_source`, `attribute_source`, `attribute_pull_date`, `keyword_research_source` (or null), `episode_goal`, `references_status`, `schema_status`, `city_count`, `questions_per_city`, `city_tagged_count`, `appendix_row_count`, `placeholder_count`, `jargon_scan` (PASS / FAIL), `geo_plan` (city + region + tag distribution).

### Source inventory

Records every input the run consumed: the resolved `n-gram-table.json` path, the `entity-map.json` + `entity-clusters.md` paths, the attribute source (live `pod-1D` output path or the static fallback path + pull date), any `keyword-research.json` mined, the firm-metadata source if used, and the calibration examples used.

### Reference implementation

`scripts/reference-impl/` holds the working prototype from the 2026-08-14 build - `topics3.py` (content model, ATTRIBUTES, REGION map, `s2_v4()` question generator), `push_v3.py` (block builder for the whole doc shape), `push_tabs.py` (markdown-ish blocks to Google Docs API requests, including multi-tab creation and styling). It produced the six-tab prototype doc that this format was signed off against. It is reference, not the ship path - the ship path is the branded DOCX. See `scripts/README.md`.

---

## Learning & Iteration

- [ ] After each run, note edge cases, jargon-scan failures, geo-tag disputes, and attribute-set staleness; append GOOD / BAD / EDGE CASE entries to `references/examples/ros-template-v2-examples.md`.
- [ ] Track whether interviewers actually hold the silence. If recordings show the interviewer stepping in before three seconds, the instruction needs to be louder in the document, not just in training.
- [ ] Track whether Segment 2 answers stay self-contained. Callbacks to Segment 1 make a clip unusable and are the most likely recording-day failure.
- [ ] Re-pull attributes when `pod-1D-attribute-research` ships. Compare against the 2026-08-14 static set and log what moved - answer-engine drift is itself a signal worth keeping.
- [ ] Watch for the single prompt growing into a list across refreshes. That is the regression this format is most exposed to.

## Change Log

| Date | Change |
|---|---|
| 2026-08-26 | **v1.9.0 - intro rules LOCKED (Gabe, 2026-08-26, consolidated re-sync from ce-ros-v2 prompts.ts / assemble.ts).** (1) **Line 1 split form**: a "{Prefix} w./with {Attorney}" podcast name splits at the "w./with" - "Welcome back to the {Prefix} podcast with {Attorney}.", plain text, NO bolds, computed at populate; the "the {{PODCAST_NAME}} Podcast." constants demoted to no-splice fallback (statics.json welcome_split_rule; schema 2.5.1). (2) **Line 2**: opener variety bank ("today we're going to discuss X" / "today the topic is X" / "the theme today is X" / "we're going to dive into X" / "today we're talking about X"); NO hook clause that gives away the episode's insight (REVERSES the earlier same-day hook-encouraged guidance); NO geo in line 2; still never re-names the attorney. (3) **Line 3 reframed as the EEAT line**: experience / expertise / authority / trust, credential is one form not the definition; one or two sentences, the second may bridge into the topic; the STATE slides in here; no city anywhere in S1 (retires the line 3 base-city allowance); tenure ban stands. (4) **Line 4**: "Walk us through" plus 2-3 question-shaped beats, each under roughly twelve words, whole ask under roughly thirty-five, no subordinate clauses; default triad definition ("even is" banned, "For people who are unfamiliar, let's start with..." sanctioned) -> difference -> challenges; narrow topics take two beats; beats grounded in the body questions; the six setup frames, verb menu and one-sentence form superseded. (5) Philosophy line recorded: "get through the intro to the setup, be clear and concise with the setup, and then just let them talk." Files: references/introduction.md, references/prompts/01-introduction.md, references/statics.json, references/schema/ros-template-v2.json, references/outro.md, steps/04-segment-1.md, steps/08-qa.md, this file, plus pod-3B-client-ros-v2 SKILL.md and renderer. | Gabe Jordan |
| 2026-08-26 | **v1.8.0 - four editorial decisions folded in (Gabe, 2026-08-26).** (1) **Embedded-name welcome variants**: `statics.json` gains `welcome_embedded` / `welcome_embedded_first` for podcast names that embed the attorney's name (e.g. "Car Accident Attorney w. Robert May") - "with **{{ATTORNEY_NAME}}**" would double the name; a "w." in a podcast name is spoken, and rendered in the welcome, as "with"; schema 2.5.0 relaxes the two welcome consts to two-value enums; `pod-3B-client-ros-v2` accepts either constant at populate. (2) **Line 2 never re-names the attorney** - host ID first and alone ("I'm {{INTERVIEWER}}."); the "here with {{ATTORNEY}}" and "sitting down with" near-static forms are retired; two sentences beat one run-on chain; a hook clause after the topic is encouraged when it carries the episode's genuine insight and skipped when the plain name lands. (3) **Tenure ban**: the line 3 tenure credential is banned when any recent episode's credential already used years - a vaguer nod to expertise and experience that sets up the topic is preferred. (4) **"Swap pool" renamed "Question Pool"** in user-facing text only. Attribute block confirmed as bullets, never a numbered list, and pinned in both renderers. Files: `references/statics.json`, `references/introduction.md`, `references/prompts/01-introduction.md`, `references/schema/ros-template-v2.json`, `steps/04-segment-1.md`, `scripts/build-ros-template-v2-docx.py`, this file, plus `pod-3B-client-ros-v2` SKILL.md and renderer. Revert: drop the two new statics keys, restore the schema consts, and restore the 2026-08-21 line 2 / line 3 guidance. | Gabe Jordan |
| 2026-08-18 | **v1.4.1 - all four downstream ship blockers cleared; downstream repointed to the v2 siblings.** `pod-3B-client-ros-v2` v1.0.0 and `pod-3C-client-guide-v2` v1.0.0 built as siblings of the untouched legacy skills (iteration-log 2026-08-14-001 and -004 resolved; -002 and -003 were already verified false alarms). Repointed every downstream reference in this file and `references/placeholders.md` from the legacy 3B/3C names to the v2 siblings (description, What is, Workflow note, Output formats, Routing, Handoff Contract, Framing, Guidelines 1/4/5/8, Probe environment, Ship report-back, Production notes heading) - EXCEPT the two Episode 1 / Founder Story routes, which stay on legacy `pod-3B-client-ros` by design. Gotchas -> Downstream changes rewritten as the resolved record. Ship banner updated: blockers no longer hold the first Drive write; that is now only Gabe's go. Revert: restore the four-blocker Gotchas text and the legacy skill names at the listed sites. | Gabe Jordan |
| 2026-08-24 | **v1.7.0 - `## Follow-ups` block added to Segment 1 (Gabe directive).** New H2 between the attribute bullets and `## Outro`, carrying interviewer notes that are never read on air. The note line and the first bullet are HARD-CODED in both renderers (`FOLLOWUP_NOTE`, `FOLLOWUP_STATIC`) and render byte-identical every episode: *"Notes for the interviewer. Not read on air."* and *"Follow up when the opportunity presents itself, not on a schedule. Let the answer finish first."* At least one generated bullet must prompt the attorney to expand on a case study for THIS episode's topic. **This is where the story invitation went** after it was cut from intro line 4 on 2026-08-21 - it stopped being a scripted sentence and became a note the interviewer acts on when the moment arrives. New Guideline 10, new follow-ups quality gate, `segment_1.follow_ups` added to both schemas as required (minItems 1), both DOCX renderers emit the block, and the renderer fails the build on an empty `follow_ups` or a question mark inside it. **Also fixed: `build-ros-template-v2-docx.py` still enforced 10 questions per location** - the 2026-08-21 change to 15 was applied only to the Client ROS renderer, so the template renderer had been silently wrong for three days. EP2/EP3/EP4 live Docs patched by surgical insert (all three had human edits after the last push; a re-render would have destroyed them). Revert: remove the Follow-ups block from both renderers, drop `follow_ups` from both schemas, delete Guideline 10 and its gate. | Gabe Jordan |
| 2026-08-21 | **v1.6.0 - intro/outro rebuilt as guardrails + examples + execution (Gabe, iterative session).** Guideline 9 reduced to a POINTER at three files; it previously restated `references/introduction.md` and contradicted it on four points (banned the story invitation, banned `please`/`if you have`, banned `actually`, and mandated a 2-4 item scope list - all four are or were canonical). New `references/examples/intro-outro-examples.md` (118 lines) carrying real BAD->GOOD pairs; calibration now leads, rules follow. `introduction.md` restructured: GUARDRAILS (7 hard, 3 judgment) + an 8-step EXECUTION order at the top, ~450 lines of pattern libraries and call history fenced below as background - the operative surface went from 424 lines to ~29. Line 4 settled at ONE sentence: a situation plus an imperative ask **carrying the episode topic phrase** (Gabe's rule - the ask is the retrieval anchor and the clip title); story invitation CUT; "2-4 item scope list" deleted as the cause of invented beats. Line 2: keep the VERB (verbless "Today, the insurance adjuster" is a headline, not speech - Gabe: "sounds weird as fuck"), name the topic never tease it, stakes clause now OPTIONAL and practice-area neutral (the old "if it happens to you" broke on the hiring and deadlines episodes), and line 2 must not echo line 4. Line 3: tenure demoted from requirement to fallback, credential must be germane and SOURCEABLE, vague years permitted ("more than a decade"). Outro: GUARDRAILS added, CTA stack banned (the shipped outro had "Subscribe so you catch the next one"), credit clause restored as a required beat, `{{STATE}}` restored to the reach-out, contractions, hinge must acknowledge the goodbye it follows. Rotation machinery RETIRED (`scripts/outro-rotation.py` + 4 metadata fields) in favour of text-and-shape uniqueness against prior episodes. Four mechanical rules invented earlier the same day were removed after each made output worse by forcing it: city quota, scope-list count, byte-identity carryover, rotation indices. The gate is the read-aloud. Revert: restore from the 2026-08-21 scratchpad backups. | Gabe Jordan |
| 2026-08-21 | **v1.5.0 - questions carried verbatim, 15+5 per location, intro content spec (Gabe directive 2026-08-21).** Guideline 5 rewritten on three axes. (1) **Re-voicing RETIRED** - the rule "make it read like something a person would type into a search box" was the direct cause of the Eberst E2/E3/E4 defect rate (22 of 30 questions rewritten by editorial before air); `pod-2B-n-gram-table` Guideline 2 now owns question voice end to end and questions are carried VERBATIM here. A search-string-sounding question is an upstream defect and routes back to 2B. (2) **Count changed from a ten-per-location hard cap to 15 in the body plus a 5-question swap pool per location**, sourced from 2B's new 20-per-location table; three locations = 45 body, 15 pool, 60 total. (3) **Swap-pool questions now render WITH their 2-4 attorney bullets** so a client rejection at review swaps in with zero rebuild - this overrides the legacy `pod-3A-ros-template` rule that reserve questions carry question text only. Question mix rebalanced to 3 city-tagged + 12 byte-identical carryover per location, with the city justified by 2B Guideline 4's two-lane test and the city-region pairing removed from spoken question text. New **Guideline 9 (Introduction content)**: `setup` must name the topic explicitly and carry one relatability clause then stop; no dramatized hypothetical; `prompt` is exactly ONE ask with no war-story rider and no permission-softening, carrying a 2-4 item scope list with the money phrase; contractions and spelled numbers; `actually` banned. **Single prompt gate hardened** to count question marks inside `prompt` (the old paragraph-count check missed riders sitting inside line 4) and to grep for permission-softening; new intro content gate added. Revert: restore SKILL.md from the 2026-08-21 scratchpad backup. | Gabe Jordan |
| 2026-08-18 | **v1.4.0 - credential line, outro speaker tag, eleven-token taxonomy: consumers reconciled.** Three format decisions that had landed in the reference docs but not in their consumers. **(1) The credential is Introduction line 3 and its own generated field.** It was previously folded into `prompt`, which rendered the credential and the ask as one run-on paragraph even though `references/introduction.md` always specified them as separate lines. The Introduction is now four lines - STATIC `welcome` (line 1, sonic marker, nothing substitutes into it), generated `setup` (line 2), generated `credential` (line 3, its own paragraph, NOT bold in full so line 4 stays the single bolded prompt), generated `prompt` (line 4). `cold_open` survives only as a deprecated alias for `setup`. **(2) The `INTERVIEWER` speaker tag is cut from the whole document.** It went from the outro because `outro_note` sits directly above and already says who is speaking, and from the Introduction because the welcome makes the speaker obvious. `ATTORNEY RESPONSE` in the Introduction is the only tag left. **(3) The taxonomy is ELEVEN tokens** and it is v2's own list, not a superset of legacy's twelve. Repointed here: Editorial Guideline 4's whole document-shape block (four-line Introduction, no `Attributes to Hit`, no `Internal Notes`, S2 no longer starting its own page, underline rule added), the Quality gates list (STATIC verbatim, generated-field allowlist, Introduction order, single prompt, removed-section, page break, plus new attribute-block, outro and speaker-tag gates), the generated-field allowlist in Guideline 8 and the gate that reads it, the Sections-INCLUDED list, Guidelines 2 and 7, `### Generate S1 Long-Form`, `### Generate S2 Short-Form`, `### Generate the outro and appendix`, the QA checklist, and every stale `/13` count. Matching edits in `references/statics.json` (the interviewer speaker tag moved to `retired`, the no-substitution comment corrected), `references/schema/ros-template-v2.json` (2.4.0, descriptions only - no shape change, so every payload valid against 2.3.0 stays valid), `references/document-structure.md` (already correct), `references/prompts/01-introduction.md` and `05-outro-close.md` (render orders drop the tag), `references/prompts/README.md`, `references/README.md`, `references/schema/README.md`, `references/attributes/README.md`, `references/cover-spec.json`, `references/introduction.md` (the eight credential frames were headed "seven"), `steps/02`, `04`, `05`, `07`, `08` and `update-mode.md`. Also added: gates AT-1 (zero question marks in the attribute block) and AT-2 (ten to twelve bullets) to `scripts/build-ros-template-v2-docx.py -> validate_attributes`, both firing before any render work so a bad payload writes no partial file; and `steps/update-mode.md` filled in from stubs. Revert: restore `segment_1.prompt` as the combined credential-plus-ask paragraph and drop `segment_1.credential`, re-add the `INTERVIEWER` speaker tag to the Introduction and the outro render orders and to `statics.json -> speaker_tags`, and delete `validate_attributes` and its call in `build()`. | Gabe Jordan |
| 2026-08-18 | **v1.3.0 - `{{RECORDING_DATE}}` retired; taxonomy drops to ELEVEN.** The token is gone from the taxonomy and from the rendered document. It only ever appeared on the cover, and it did not belong there: a ROS Template is generic and tokenized precisely so one template serves every firm that records that episode at that scope, and different firms record on different dates, so a recording date was never a template-level fact. It also stamped a date on the cover of an asset meant to stay evergreen. The recording date is a Client ROS field and `pod-3B-client-ros` already collects it per firm, so nothing downstream loses it. The cover now ends on `Prepared by Case Engine`. Repointed: the Guideline 1 taxonomy table and every count claim (12 -> 11, plus three stale 13s corrected to eleven: the `outside the 13 above` ban and the two `13 placeholders` recap lines in the QA Best-Practices check), the Guideline 4 cover spec, the cover-page gate, `### Generate the cover page`, and the final QA checklist. Matching edits in `references/placeholders.md` (canonical, with a retired note under Open), `steps/03-cover-page.md`, `references/prompts/04-cover-page.md`, `scripts/README.md` and `references/examples/ros-template-v2-examples.md`; already applied by Gabe in `scripts/build-ros-template-v2-docx.py` (line no longer renders in either the docx or the markdown path), `references/cover-spec.json` (block removed, 2.1.0) and `references/schema/ros-template-v2.json` (dropped from the `placeholders_used` enum and `cover_page.recording_date_token` removed, 2.2.0). Revert: restore the `{{RECORDING_DATE}}` row to `references/placeholders.md`, re-add the 11pt bold cover block after `Prepared by Case Engine` in `cover-spec.json`, restore the enum entry and `cover_page.recording_date_token` in the schema, and move every count back to twelve. | Gabe Jordan |
| 2026-08-17 | **v1.2.0 - `pod-1-podcast-bible` dependency removed; format flag becomes a runtime ask.** The Show Bible skill is deleted, so nothing may read from it. The `episode_format` HARD GATE survives intact but its source changes: Greeting Q1 now asks the user outright - "Is this episode running the v2 open-interview format or the legacy segmented format?" - phrased so a teammate who is not Gabe can answer it, with `legacy-segments` still the default and "not sure" / blank explicitly treated as legacy (absence is never permission to build v2). `podcast-overview.md` stays as an OPTIONAL pre-fill when reachable, but the user's answer is the authority and a missing doc is no longer a blocker. `metadata.json -> episode_format_source` now records `user` (with who answered) or `podcast-overview` (with the path). Repointed: Required inputs, `### Framing -> Episode format flag`, and the `### Resolve the format flag` SOP step. Cover-page spec DE-REFERENCED from the dead `pod-1-podcast-bible/scripts/bible_formatting.sh` and inlined as the CE deliverable cover spec in Editorial Guideline 4 and `### Generate the cover page` (unchanged values: CE logo Drive id `1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2` at 180pt, `Run of Show` CE Blue 24pt bold, episode title dark 18pt bold, practice-area/scope line dark 14pt, `Prepared by Case Engine` 11pt, `{{RECORDING_DATE}}` 11pt bold, centered Roboto), cross-referenced to the Cover Page Spec in the Case Engine Branding folder. Same de-reference applied in `references/prompts/06-cover-page.md`, `references/schema/ros-template-v2.json` (`cover_page.description`), `scripts/reference-impl/push_v3.py`, and `scripts/reference-impl/push_tabs.py`. No behavior change beyond swapping a data source for a user prompt; no schema field added, renamed, or removed. Temporary manual ask pending a future DB wiring for the format flag. Revert: repoint the format flag and cover spec back at `pod-1-podcast-bible` (requires restoring that skill from `.backups/pod-1-podcast-bible-deleted-2026-08-17/`). | Gabe Jordan |
| 2026-08-18 | **v1.2.0 - outro rebuilt, taxonomy reconciled, read-through gate added.** The outro's three spoken lines stopped being constants: Gabe required the outro to read relatively unique per episode while always hitting the same points, so they are now GENERATED against required beats plus variation banks in the new `references/outro-banks.json`, with narrative spec and gates OC-1 to OC-9 in the new `references/outro.md`. Order changed to thanks-and-credit, sign-off, reach-out, with the sign-off deliberately not last and the reach-out landing after it as a tag. Line 1 gained a credit clause across five approaches (topical preferred, being the only one whose clause cannot be reused on another episode). "Produced by Case Engine" cut from the sign-off - it is the firm's show and a CE credit in the close inverts the relationship the same way guest framing does. `outro_plug` deleted entirely: its injury-only "If you were hurt" opener was replaced by the practice-area-neutral "in {{STATE}} and need a lawyer", which retired the four-trigger set it briefly needed. STATIC set cut from 16 to 3 (`welcome`, `welcome_first`, `outro_note`); the other 13 are retired in `statics.json -> retired`. Placeholder taxonomy reconciled to the TWELVE in `references/placeholders.md`, matching the live doc: `{{ATTORNEY_FIRST_NAME}}`, `{{HOST_NAME}}`, `{{PRACTICE_AREA}}` retired for `{{ATTORNEY}}`, `{{INTERVIEWER}}`, `{{TOPIC}}`. Speaker tags unbracketed. Added the **read-through gate** (QA tier 4, hard, LLM, runs last) after a generated line passed every mechanical gate while being a sentence no person would say aloud; this is the one deliberate exception to "a gate that needs judgment is not a gate". Added `scripts/outro-rotation.py`. Revert: restore the 16-string STATIC set, the frozen four-line outro, and the 13-token table. | Gabe Jordan |
| 2026-08-14 | **v1.1.0 - format locked.** Baked the final document shape in from the live doc `1Bv-EWc7HBtKqc09XEfQnBIfSOdm6m4Tc-kJNw5uKErk` and the working implementation in `scripts/reference-impl/`. Cover page modeled on `pod-1-podcast-bible` (CE logo inline at the second paragraph, 180pt, Drive id `1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2`; `Run of Show` CE Blue 24pt; episode title dark 18pt; practice-area and scope line dark 14pt; `Prepared by Case Engine`; `{{RECORDING_DATE}}`). Segments renamed `S1: Long-Form (15-30m)` and `S2: Short-Form (60-90s)`, each starting on its own page. Cold Open, Lead-In and Prompt merged into a single `## Introduction` with no `[Interviewer]` tag. The three moves, the two attribute notes, and the per-attribute source-consistency counts all moved BELOW a divider into `### Internal Notes (not read on air)`. Short-Form capped at TEN questions per location, rendered as bare `**Q{N}:**` bullets with no geo tag line and no answer note. H2 headings changed to CE_DARK. Added Editorial Guideline 8 freezing the 16 STATIC boilerplate strings as JSON-template constants with a verbatim gate, and a generated-field allowlist limiting per-run generation to `topic_phrase`, `cold_open`, `prompt`, `need_to_know`, `examples`, and the question sets. REMOVED from the format: `How This Episode Runs`, `Producer Notes`, `The Lead-In` and `The Prompt` as headings, `Interviewer: Live Checklist`, `Co-Host Notes`, `Geo Rule`, per-question geo tags, per-question answer notes; a removed-section gate keeps them out. Guideline 3 tightened: with Producer Notes gone there is no exempt section, so the jargon scan must return zero across the whole document above the Appendix, and the D-4 inverse containment check was deleted. The interviewer and co-host guidance from the 08-14 call moved to `## INTERNAL -> ### Production notes` so it reaches people via `pod-3C-client-guide`, along with the 3-5 extra shorts pulled from S1 in post, the asymmetric editing rule, and on-the-spot retakes. Prompts reconciled: `01-cold-open` + `02-lead-in` merged into `01-introduction`, `07-interviewer-toolkit` and `09-producer-notes` deleted, `08` became `05-shortform-questions` with the ten cap, `06-cover-page` and `07-outro-close` added, all renumbered. Schema bumped 1.0.0 -> 2.0.1 with a `static` block pinning all 16 constants via `const`, a `cover_page` block, `segment_1.attribute_sources`, locations replacing cities, and `maxItems: 10`. Renderer rewritten to the locked shape and verified against the live doc. Revert: restore Guideline 4's pre-lock shape, the deleted prompt files, and schema 1.0.0. | Gabe Jordan |
| 2026-08-14 | **v1.0.0 - initial build.** New skill, new format, decided on the Gabe/Cyle call of 2026-08-14. Segment 1 becomes one credential-led prompt plus a 15 to 30 minute open interview (cold open, lead-in carrying the structural work a question list used to do, one prompt in Cyle's verbatim shape, an explicit silence instruction, a three-move answer shape, an attribute block, an interviewer live checklist and stall toolkit, co-host notes). Segment 2 becomes per-city short-form blocks of 10 to 20 search-phrase questions at 60 seconds each, self-contained for clipping, retakes expected. Added Editorial Guideline 3 (no jargon attorney-facing; statutes only in Producer Notes marked never-read-on-air) and the matching jargon scan gate. Added Editorial Guideline 6 (geo pairing, per-question CITY / CITY + REGION / REGION / NEUTRAL / STATE tags) which **REPLACES the pod-2B ~25-45% city-share ceiling** for v2 blocks, with the reasoning recorded. Added Editorial Guideline 7 (attributes replace statute-heavy bullets), ranked from live Google AI Overview + ChatGPT pulls on 2026-08-14, with the two counterintuitive findings preserved. Declared `{{YEARS_PRACTICING}}` as the 13th placeholder. Introduced the `episode_format` flag (`legacy-segments` default, `v2-open-interview`) resolved at podcast-overview / show-bible level, plus the format flag gate and the legacy non-collision gate so v2 and legacy coexist in the same scope folder without either touching the other. Inherited unchanged from `pod-3A-ros-template` v3.2.0: Drive write governance, canonical destination gate, branded DOCX render path, Anti-AI Detection two-pass QA, Confirmed / Inferred / Unknown sourcing discipline, the three-field geo model, Episode 1 Founder Story exception, local mirror, and the Create / Update / QA / Ship phase structure. `pod-3A-ros-template` left completely untouched. Four downstream changes are declared as ship blockers and were NOT made here: `pod-3B-client-ros` populate taxonomy + section stripping, the `pod-3A-ros-template` placeholder gate, the `pod-2B-n-gram-table` city-share ceiling, and `pod-3C-client-guide`. Revert: delete this skill folder; nothing else in the pipeline was modified. | Gabe Jordan |
