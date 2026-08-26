---
name: pod-3B-client-ros-v2
description: >
  Populate a v2 (open-interview format) ROS Template with a specific firm's
  details - the twelve v2 tokens including attorney, interviewer, and years
  practicing - strip the internal Source Question Bank appendix, and ship the
  recording-ready Client ROS v2 to the firm's Drive episode folder. Use
  whenever someone says "client ros v2 for [firm]", "populate v2 ros for
  [firm]", "populate the v2 template for [firm]", "v2 client ros", "client ros
  for [firm]" on a v2-format show, or "/pod-3B-client-ros-v2". Phase 3 Run of
  Show of the podcast pipeline, v2 branch; hard dependency on a matching-scope
  ROS Template v2 from pod-3A-ros-template-v2. This is the FINAL step of the
  v2 branch - nothing runs downstream of it. The LEGACY populate stays on
  `pod-3B-client-ros` - both coexist
  behind the `episode_format` flag and this skill never runs unless that flag
  says v2.
skill_kind: hybrid
modes: multi
inputs: [ros-template-v2.md, ros-template-v2-data.json, podcast-overview.md, user-supplied-firm-data, case-engine-branding]
outputs: [json, markdown, gdoc]
notify: []
metadata:
  version: 1.2.0
  date: 2026-08-18
  owner: Gabe Jordan
  version_history: >
    1.0.0 - initial v2 populate skill (2026-08-18). Sibling of
    pod-3B-client-ros (v3.3.0), forked in structure to consume the v2 format
    from pod-3A-ros-template-v2 v1.4.0. Resolves the four v2-only populate
    gaps that were 3A-v2's top ship blocker: the twelve-token taxonomy
    (including {{TOPIC}}, {{CITY}}, {{ATTORNEY}}, {{INTERVIEWER}},
    {{YEARS_PRACTICING}}), stripping `# Appendix: Source Question Bank`
    instead of the legacy Additional Questions reserve, preserving the S2
    geo tags in the JSON payload, and the statics-resolved-verbatim gate.
    Legacy skill left untouched and remains the default.
---

# Client ROS v2

> **Drive write governance:** All Drive operations (create, update, rename, move) follow [Ship]. Revise in place via `files.update` against the existing fileId, never delete-and-reupload (breaks the fileId/URL chain and silently kills every downstream reference).

> **Coexistence gate (read this first).** This skill ONLY runs when the client's `episode_format` resolves to `v2-open-interview` AND the upstream template is a `ROS Template v2` artifact. The default is `legacy-segments`, which routes to `pod-3B-client-ros`. Do not run this skill on a client whose format has not been explicitly flipped, never populate a legacy template with it, and never "upgrade" an existing legacy Client ROS with it.

### What is

The Client ROS v2 - the HOST's on-air script for a v2-format podcast episode. This skill takes a tokenized ROS Template v2 from `pod-3A-ros-template-v2` and populates every one of the twelve `{{PLACEHOLDER}}` tokens with a specific firm's details, strips the internal `# Appendix: Source Question Bank`, and ships the recording-ready result to the firm's Drive episode folder.

**Populate is mechanical, not creative - with ONE bounded exception.** The v2 format moved the lifting upstream: the template arrives with the Introduction generated, the attribute block built, the Short-Form sets written, and the outro's three lines composed. This skill resolves tokens with `.replace()`, strips the appendix and the `## INTERNAL` block, and ships. It never restructures and never regenerates a STATIC string. The one exception is the **read-through edge-rounding pass** (Editorial Guideline 5): after populate, every spoken line is read aloud, and a line that no person would actually say may receive a surface-level repair - reported as a before/after diff and flagged for the upstream template, never silent. Everything the legacy populate skill did that the v2 format retired - the Entity Checklist tally table, entity underline weaving, sequential renumbering repair, episode-goal populate slices, the city-share line count rule - simply does not exist here.

The Client ROS v2 is the interviewer's working document and the TERMINAL artifact of the v2 branch - nothing is generated downstream of it. It lands in the client episode `Run of Show/Client ROS/` slot per Map 6, mirrored to the local Desktop path. The tokenized template it populates from is NOT in the client folder - it lives ONLY in the shared template library (`templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{scope}/`, Map 2); this skill reads it from there.

**The `v2` marker lives in filenames and Doc titles ONLY** - `E{N}: {Episode Title} // {Firm Name} // Client ROS v2 - {Location}`. The rendered document content never says "v2" anywhere. (Gabe, 2026-08-18.)

### Workflow

Client ROS v2 is the second step of **Phase 3 (Run of Show)** of the podcast pipeline, v2 branch. It takes a finished ROS Template v2 and produces the populated version the interviewer works from on air. The v2 chain ends here - there is no downstream step.

```
PHASE 3: RUN OF SHOW  (per prioritized episode)
        │
        ├── episode_format = legacy-segments (DEFAULT)
        │       pod-3A-ros-template ──> pod-3B-client-ros ──> pod-3C-client-guide
        │
        └── episode_format = v2-open-interview
                pod-3A-ros-template-v2 ──> pod-3B-client-ros-v2  (END OF CHAIN)
                                             ◄── YOU ARE HERE
```

Prerequisites: a matching-scope ROS Template v2 (`.md` + `ros-template-v2-data.json`) from `/pod-3A-ros-template-v2` in the shared template library is a hard dependency - this skill will not run without it.

> **Episode 1 - Founder Story is a HARDCODED exception and is NOT in the v2 format.** The Founder Story template and its founder token set (`{{CLIENT_NAME}}`, `{{BUSINESS}}`, etc.) are handled by the LEGACY `/pod-3B-client-ros` regardless of the client's `episode_format`. If the requested episode is Episode 1, stop and route there. Do not v2-ify the Founder Story.

### Trigger phrases

- `/pod-3B-client-ros-v2`
- "client ros v2 for [firm]"
- "populate v2 ros for [firm]"
- "populate the v2 template for [firm]"
- "v2 client ros"
- "build the client ros" (when the show's `episode_format` is v2)

### Greeting

Hi, I'm Client ROS v2. Before I run, I need to confirm the format flag and the firm's details. If podcast-overview has been run for this client, I'll read it and confirm in one line. If not, I'll ask:

1. **Episode format confirmation (FIRST, blocking).** Is this show on the **v2 open-interview format** or the **legacy segmented format**? The default is `legacy-segments` - if you are not sure, or nobody has explicitly signed this client off on v2, the answer is legacy and I stop and route you to `/pod-3B-client-ros`. Auto-confirmed when the resolved upstream template is a `ROS Template v2` artifact AND its payload says `episode_format: v2-open-interview` - a v2 template existing at the matching scope is itself the sign-off trail; I confirm rather than re-ask.
2. **Client name.** Exact firm name as it appears in Drive (fuzzy match - "Conn Law" -> `Conn Law Firm Podcast/`).
3. **This run's Episode geo target** - the specific city THIS episode is built to rank for. It fills `{{CITY}}`. The three-field geo model (Targeting strategy / Optimization scope (show anchor) / Episode geo target) is unchanged from the pipeline canon: research runs at the anchor breadth, the token fills from the Episode geo target, never the show anchor.
4. **The 11 populate values** - see `### Editorial Guidelines -> Guideline 1`. Resolved in this order: **Supabase first** (the CE client record - see `#### Supabase firm lookup`), then `podcast-overview.md`, then ONE consolidated ask for anything still missing. I confirm the Supabase-resolved values back in one line rather than re-asking them. `{{YEARS_PRACTICING}}` is new to v2 - integer years in practice, in this market (derived from the firm's open date when Supabase carries it, flagged Inferred until confirmed).
5. **Recording date + episode number** (metadata, not body tokens). Recording date is non-blocking: if not set, it defaults to `TBD` and I proceed - never ask just for it. Episode number: next available under `Episodes/` if not provided.
6. Does the matching-scope **ROS Template v2** exist in the shared template library (Map 2)? If not, I stop and route you to `/pod-3A-ros-template-v2`.
7. Does the target `Client ROS:` slot already have a Client ROS v2? Archive and rebuild, or refresh in place? (I archive only the Client ROS v2 file - never a legacy sibling, never the template.)

If anything's unclear I'll ask once in a single message. I won't touch Drive until you say go.

---

## Best Practices

The WHAT contract. Every other section references these by name; the SOP never restates them.

### Inputs

What is?
The materials this skill ingests - the matching-scope ROS Template v2 and its data payload (hard dependency), the 11 populate values plus recording date and episode number, the podcast architecture doc, and the Case Engine Branding folder - all resolved before any populate begins.

#### Required

- **Matching-scope ROS Template v2** (`ROS Template v2 .md` + `ros-template-v2-data.json`) - the tokenized v2 template from `/pod-3A-ros-template-v2`, read from the shared template library `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{scope}/` (Map 2). The `v2` marker in the filename is load-bearing: a legacy `ROS Template` in the same folder is NOT this skill's input. The payload must carry `episode_format: v2-open-interview` and validate against 3A-v2's `references/schema/ros-template-v2.json`. No silent fallback - if the v2 template is not in the matching-scope library folder, the skill stops and routes to `/pod-3A-ros-template-v2`.
- **The 11 populate values** - the full taxonomy lives in `### Editorial Guidelines -> Guideline 1`. Resolution order: **Supabase (canonical CE client record) -> podcast-overview.md -> user ask**. See `#### Supabase firm lookup` for the field map. A value resolved from Supabase is Confirmed; the user is shown the resolved set in one line and can override any value.
- **Recording date + episode number** - per-firm metadata, NOT body tokens in v2 (`{{RECORDING_DATE}}` and `{{EPISODE_NUMBER}}` were retired from the v2 template body; the date renders only as a small cover line and is omitted while `TBD`; the number lives in filenames).
- **Firm name / Topic / Episode / Scope / Location** - same resolution rules as the legacy skill, including the CANONICAL SOURCE rule: the episode's topic/title is governed by the PUBLISHED Google Doc Topic Plan; never build against a local `topic-plan-v{n}.*` mirror; the Doc wins on any conflict (Eberst E5 incident, 2026-06-19).

#### Optional

- **Episode goal** - inherited from the template `metadata.json -> episode_goal` for provenance only. In v2 the goal shaped GENERATION upstream; there is no goal-sensitive populate slice left at this step.
- **Refresh flag** - default refresh in place (routes to `## Update`). Pass `archive-and-rebuild` to archive the existing Client ROS v2 to `_archive-{YYYY-MM-DD}/` and rebuild.

#### Auto-read (no action required)

- **`podcast-overview.md`** - architecture source of truth (`episode_format`, client name, show name, interviewer, anchor scope, cities). Auto-fills Greeting questions 1-4 when present at `{Firm} Podcast/.podcast-overview/podcast-overview.md`; otherwise the questions are asked.
- **Case Engine Branding folder** - the canonical brand reference at [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) (folder id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`). Brand values resolve from the folder at build time - never inlined.
- **Local example references** - bundled `references/examples/client-ros-v2-examples.md`. If missing or empty, proceed and flag `"references": "empty"` in `metadata.json` - do not block.
- **The v2 taxonomy mirror** - `references/placeholders.md` in THIS skill mirrors `pod-3A-ros-template-v2/references/placeholders.md`. The 3A-v2 copy is canonical; if the two disagree, it wins and this skill's mirror is the bug to fix.

#### Supabase firm lookup

**Supabase is the canonical source for firm data** (Gabe directive 2026-08-18). Instance `fopwynaolryofojzziai.supabase.co`, REST API with the service_role key from 1Password -> Dev team vault -> `Supabase` item (via `mcp__op-broker__read_secret`; `op item get` is the fallback when the broker is not connected - raw `op read` is hook-blocked).

Resolution: match the firm in `client_profiles` (`name ilike`, `status neq merged` - MERGED rows exist and must be skipped), then pull `client_field_values` by `client_id` (`field_key` / `field_value` pairs).

| Token | Supabase source | Note |
|---|---|---|
| `{{FIRM_NAME}}` | `biz_legal_name` (fallback `client_profiles.name`) | legal name preferred - carries the `, P.A.` suffix |
| `{{ATTORNEY_NAME}}` | `aeo_attorney_name` | |
| `{{ATTORNEY}}` | first token of `cont_marketing_poc_name` | derived - confirm ("Jon" from "Jon Eberst") |
| `{{PHONE_NUMBER}}` | `biz_official_phone` (fallback `client_profiles.primary_contact_phone`) | reformat to `(XXX) XXX-XXXX` |
| `{{WEBSITE}}` | `client_profiles.website` | ensure `https://` |
| `{{STATE}}` | `client_profiles.primary_state` | |
| `{{YEARS_PRACTICING}}` | derived from `biz_open_date` | Inferred - confirm with the user |
| `{{CITY}}` | NOT Supabase | the Episode geo target is per-episode, not per-client |
| `{{TOPIC}}` | NOT Supabase | comes from the template payload / Topic Plan |
| `{{PODCAST_NAME}}` | `pod_name` | live since before this skill; `aeo_podcast_name` NEVER existed - that key was the bug (corrected 2026-08-25) |
| `{{PODCAST_DOMAIN}}` | `pod_domain` | where episodes live - the SUBSCRIBE line. Never interchangeable with `{{WEBSITE}}` |
| `{{INTERVIEWER}}` | `pod_ce_host` | the CE interviewer, per-client default. `aeo_ce_host` NEVER existed. Overridable per episode; a name off `hr_team_members` job_title 'Podcast Interviewer'. NOT `pod_cohost`, which is the FIRM's own co-host |

Record per-value provenance in `metadata.json -> firm_data_sources`. When Supabase is unreachable, degrade to podcast-overview -> user ask per the capability ladder - never block on the DB.

#### Capabilities

The skill runs locally in Claude Code and calls its tools directly - it assumes they exist and uses them in this priority order. On a tool error, it skips that source and degrades to the next; it never probes for availability first.

- **Local filesystem read** - for the auto-detected v2 template at `~/Desktop/claude_code/deliverables/podcast/ROS Templates/{Topic}/{Episode}/{scope}/`. Fastest path; no Drive round-trip.
- **Supabase REST** (service_role via op-broker) - the canonical firm-data source per `#### Supabase firm lookup`. Queried once per run; on an auth or network error, degrade to podcast-overview -> user ask.
- **`gws drive`** (or `mcp__claude_ai_Google_Drive__*` connector) - for the ROS Template v2 trio from the shared template library (Map 2), the podcast-overview doc, and the Case Engine Branding folder.
- **User-supplied materials** in the greeting and user interview for hard requirements still missing - the always-available floor.
- **Hard requirement** - the matching-scope ROS Template v2 must resolve via local read or Drive. At least one source for the 12 populate values must be reachable.
- **Behavior on a tool error** - skip that source and degrade to the next. With no reachable source, fall through to user-supplied + interview; flag every Inferred value with `> NEEDS CONFIRMATION:` per Sourcing discipline.

### Outputs

What is?
The artifacts this skill ships - the 3-format trio (a machine-readable JSON payload, a markdown source-of-truth, and a CE-branded Google Doc) plus a `metadata.json` provenance file - landing in the firm's episode `Client ROS:` slot per Map 6, mirrored to the local Desktop path. Filenames and Doc titles carry the `v2` marker; the rendered content never does.

#### Output formats

- **JSON** - `client-ros-v2-data.json` - the populated payload: the template's `ros-template-v2-data.json` shape with every token resolved, a `firm` block added, the appendix and `placeholders_used` removed, and every S2 question still carrying its `geo_tag` and `source_ngram_ref`. Validates against `references/schema/client-ros-v2.json`. The input the build script renders from; still written on every run as the machine-readable record of the episode.
- **Markdown** - the Client ROS v2 `.md` - populated source-of-truth, uploaded to Drive as `text/markdown` (no conversion). Retains the `## INTERNAL` block locally; the Drive-facing render strips it.
- **Google Doc** - the human-facing CE-branded Client ROS v2 Doc. Built from a CE-branded `.docx` emitted by `scripts/build-client-ros-v2-docx.py`, then uploaded with `mimeType: application/vnd.google-apps.document`. Created / updated in-place via `files.update` against a stable fileId.

A `metadata.json` provenance file ships alongside the trio (internal-only - template source path + fileId, the resolved 11 values, recording date, episode number, run timestamp).

#### Drive destination

Shared drive root: `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`). Per [Client Folder Structure](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU/edit) → Map 6, the Client ROS v2 lands in the cell's `Client ROS:` slot - the same slot the legacy skill uses, because an episode is exactly one format and never has both.

```
{Firm} Podcast/Episodes/EP{N}: {episode_name} // {client_name}/Run of Show: {episode_name} // {client_name}/
  Client ROS: {episode_name} // {client_name}/                                           ← THIS SKILL writes here
    E{N}: {Episode Title} // {Firm Name} // Client ROS v2 - {Location}.md                 raw markdown source (text/markdown)
    E{N}: {Episode Title} // {Firm Name} // Client ROS v2 - {Location}                    branded Google Doc (in-place files.update)
    client-ros-v2-data.json                                                               populated payload, downstream-consumed
    metadata.json                                                                         provenance
    _archive-{YYYY-MM-DD}/                                                                (only the prior Client ROS v2, if one existed)
```

Append ` (Extension)` after `{Location}` for extension cells. The double-slash ` // ` separator with spaces is literal. **Never overwrite a legacy `Client ROS` artifact** - if the slot holds a legacy Client ROS for this episode, something is wrong (the episode was recorded in the other format); stop and surface it rather than writing beside or over it.

#### Local mirror

`~/Desktop/claude_code/deliverables/podcast/Client ROS/{Topic}/{Episode}/{scope}/` - the same `.md`, CE-branded `.docx`, `client-ros-v2-data.json`, and `metadata.json`. Written on every run.

#### Schema

`references/schema/client-ros-v2.json` - the canonical JSON schema `client-ros-v2-data.json` validates against. It inherits the template payload shape from 3A-v2's `ros-template-v2.json` (segment_1, segment_2 with per-question `geo_tag` + `source_ngram_ref`, static, outro, duration) and adds the `firm` block while dropping `appendix_question_bank` and `placeholders_used`. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed.

#### Sections INCLUDED in the client-facing Google Doc

- Branded cover page - the template cover plus the two populate deltas: the firm name under the episode title, and the recording date under `Prepared by Case Engine` (omitted while `TBD`)
- `# S1: Long-Form (15-30m)` - `## Introduction` (four lines, populated), `## ATTORNEY RESPONSE` with the attribute bullets, `## Outro`
- A horizontal rule, then `# S2: Short-Form (60-90s)` - the direction line, then `## Location: {city}` blocks of ten questions with their bullets

#### Sections EXCLUDED (never in the client-facing artifact)

- **`# Appendix: Source Question Bank`** - INTERNAL to the ROS Template v2. The strip target in v2 is this heading, NOT the legacy `## Additional Questions (Optional Pull)` (which does not exist in the v2 format). The bank stays upstream as the pull pool when a client rejects a question.
- `## INTERNAL` and everything from `## Quality Assurance` onward
- Anything on the template's removed-sections list (`pod-3A-ros-template-v2/references/document-structure.md`) - populate cannot reintroduce what generation already cut

#### Examples

`references/examples/client-ros-v2-examples.md` - single doc with GOOD / BAD / EDGE CASE labeled sections per CE convention. Read 1-2 examples matching the requested scope as calibration before populating.

#### Routing

- **Upstream (required, hard dependency):** `/pod-3A-ros-template-v2` - the matching-scope ROS Template v2.
- **Sibling (mutually exclusive):** `/pod-3B-client-ros` - the legacy populate. Exactly one of the two runs per episode, decided by `episode_format`. Episode 1 Founder Story always routes there.
- **Downstream:** none - this is the terminal step of the v2 branch.
- **Refresh:** re-run with the same episode + scope (routes to `## Update`).

#### Handoff Contract

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| Client ROS v2 `.md` + branded Google Doc | Human - the interviewer works from it on air | The populated v2 shape: Introduction lines, the single prompt, attribute bullets, per-city Short-Form sets with bullets, outro lines |
| `client-ros-v2-data.json` | (no downstream skill - machine-readable record) | The full populated payload - `firm` block, segment_1, segment_2 city blocks with per-question `geo_tag` + `source_ngram_ref`, statics, outro, duration |
| `metadata.json` | (not consumed downstream) | Internal provenance |

Anyone reading these artifacts can rely on: the Google Doc URL is stable (preserved via `files.update`); zero leftover `{{...}}` tokens anywhere; the appendix is stripped; every S2 question still carries its `geo_tag` and `source_ngram_ref` in the JSON; the statics equal the template constants with tokens resolved.

### Framing

The Client ROS v2 is a MECHANICAL POPULATE of the v2 template - the same document with real values where tokens were, minus the internal appendix. It is never a rewrite, never a restructure, and never invents content the template did not carry. The template's locked shape (`pod-3A-ros-template-v2` Editorial Guideline 4 and `references/document-structure.md`) is the contract this skill preserves exactly; a populated doc that differs from its template by anything other than token values, the two cover deltas, and the stripped appendix is a defect.

### Quality bar

What "good" looks like - the pass / fail intuition.

- All 12 tokens resolved to real values; a grep for `{{...}}` in the populated output returns zero.
- Bold preserved around every populated value (`**{{FIRM_NAME}}**` -> `**Eberst Law Firm**`).
- The document structure byte-matches the upstream template shape - same headings, same order, same counts. Diffing populated against template shows ONLY token resolutions, the two cover deltas, and the missing appendix.
- The 2 STATIC strings equal the template constants with tokens resolved - never regenerated, never "improved".
- Exactly one bolded prompt; exactly ten questions per location; 10-12 attribute bullets with zero question marks.
- The `v2` marker in the filename and Doc title, never in the rendered content.
- The human-facing Google Doc is the CE-branded DOCX→Doc, never a raw-markdown→Doc upload.
- No em dashes, no banned vocabulary - the Anti-AI Detection scan fires before publish.

### Sourcing discipline

The Confirmed / Inferred / Unknown three-state pattern. Never block, always ship, never silent.

- **Confirmed** - every populate value resolved from Supabase (the canonical CE client record), the podcast-overview doc, or supplied directly by the user. Ship as-is, no marker. Derived values (`{{ATTORNEY}}` from a full-name field, `{{YEARS_PRACTICING}}` from the open date) are Inferred until the user confirms them.
- **Inferred** - a sensible default (recording date `TBD`, episode number from the folder scan). Ships with `> INFERRED:` flag in `## INTERNAL`.
- **Unknown / NEEDS CONFIRMATION** - never guess a firm phone, website, or years practicing. A value with no source ships as a blocking ask in the Greeting, not a synthesized guess.

### Editorial Guidelines

**Guideline 1 - The 12 approved v2 tokens, all resolved, never invented.**

> **`{{WEBSITE}}` vs `{{PODCAST_DOMAIN}}` (Gabe directive 2026-08-21).** `{{WEBSITE}}` = the BUSINESS site, used in the conversion CTA. `{{PODCAST_DOMAIN}}` = where episodes live, used in the subscribe line. Never resolve one from the other.

- **Approved taxonomy** (mirror of `pod-3A-ros-template-v2/references/placeholders.md`, which is CANONICAL - it wins on any disagreement):

  | Placeholder | Populate source |
  |---|---|
  | `{{TOPIC}}` | The episode's subject as a spoken phrase (from the template payload / Topic Plan) |
  | `{{CITY}}` | The **Episode geo target** city - NOT the show anchor |
  | `{{STATE}}` | State full name (`CA` -> `California`); multi-state firms resolve to the spoken phrase (`Maryland and DC`) |
  | `{{PODCAST_NAME}}` | Client's podcast name |
  | `{{ATTORNEY_NAME}}` | Full attorney name (Intro line 1 only) |
  | `{{ATTORNEY}}` | First name - how the host addresses them on air |
  | `{{INTERVIEWER}}` | CE host on the recording |
  | `{{FIRM_NAME}}` | Full firm name |
  | `{{PHONE_NUMBER}}` | Firm phone `(XXX) XXX-XXXX` |
  | `{{WEBSITE}}` | Firm website, including `https://` |
  | `{{YEARS_PRACTICING}}` | Integer years in practice, in this market |

- **`{{ATTORNEY_NAME}}` and `{{ATTORNEY}}` are not interchangeable.** Full name appears once, in the branded open; first name is direct address everywhere else. Map both, never one from the other's slot.
- **Resolution is `.replace()`, NEVER `str.format()`** - format collapses the doubled braces and silently destroys every token.
- **Not body tokens in v2:** `{{RECORDING_DATE}}` (cover line + metadata only, `TBD` non-blocking), `{{EPISODE_NUMBER}}` (filenames only), `{{ATTORNEY_FIRST_NAME}}` / `{{HOST_NAME}}` / `{{PRACTICE_AREA}}` (legacy tokens - their presence in a template means it is NOT a v2 template; stop and route to the legacy skill).
- **Banned:** any unresolved `{{...}}` in the populated output; stripping the bold off a populated value; inventing `{{REGION}}` (the region is plain text fixed by the template).

**Guideline 2 - Preserve the v2 template's shape exactly; populate-only.**

- The locked shape lives at `pod-3A-ros-template-v2` Editorial Guideline 4 and `references/document-structure.md`. This skill inherits it wholesale and re-renders it via `scripts/build-client-ros-v2-docx.py`, which is the populate-side mirror of the template renderer - same primitives, same styling (H1 CE Blue / H2 CE Dark, `ATTORNEY RESPONSE` as an H2, S2 flowing behind a rule, compact S2 spacing).
- **The two cover deltas are the ONLY additions:** the firm name under the episode title, and the recording date under `Prepared by Case Engine` (omitted while `TBD`). A template is generic; a Client ROS is one firm's dated recording copy. Nothing else is added anywhere.
- **The appendix strip is the ONLY removal.** `# Appendix: Source Question Bank` and everything under it. The removed-sections list is inherited: populate must not reintroduce `Internal Notes`, `Attributes to Hit`, `Producer Notes`, an `INTERVIEWER` tag, per-question geo tag lines, or anything else generation already cut.
- **The 2 STATIC strings resolve, they do not regenerate.** `welcome` (or `welcome_first` on Episode 1) equals the template constant with `{{PODCAST_NAME}}` / `{{ATTORNEY_NAME}}` resolved; `outro_note` is byte-identical. Embedded-name shows - the podcast name embeds the attorney's name, e.g. "Car Accident Attorney w. Robert May" - take the `welcome_embedded` / `welcome_embedded_first` constants instead, never "with **{{ATTORNEY_NAME}}**", which doubles the name; a "w." in the podcast name is spoken, and rendered in the welcome, as "with" (Gabe 2026-08-26). The renderer compares against the constants and hard-fails on any other delta (Editorial Guideline 8 upstream).

**Guideline 3 - What legacy populate machinery does NOT carry into v2.**

Each of these was deliberate in legacy and is deliberately absent here. Do not reintroduce them "for completeness":

- **No Entity Checklist tally table.** v2 carries no entity underlines and no entity-mention targets; entities informed generation upstream and never reach the page as architecture.
- **No entity underline weaving.** The only underlines in a v2 doc are the Short-Form bullet labels, inherited from the template as-is.
- **No sequential renumbering gate.** v2 questions are born `Q1..Q10` per location; there is no n-gram bank index to leak (the Sutliff E8 failure mode cannot occur).
- **No episode-goal populate slice.** The goal shaped generation at 3A-v2; populate has no goal-sensitive decisions left.
- **No city-share / third-of-lines rule.** v2 geo is governed per-question by `geo_tag` and the city-region pairing, set at generation. Populate preserves the tags in the JSON and changes nothing.

**Guideline 4 - Geo: fill from the Episode geo target; preserve the tags; never render them.**

- `{{CITY}}` fills from the **Episode geo target** - the specific city THIS episode is built to rank for - never the Optimization scope (show anchor). The three-field geo model is unchanged from the pipeline canon.
- Every S2 question's `geo_tag` and `source_ngram_ref` carry through into `client-ros-v2-data.json` unchanged. They are what QA and downstream audits read. They NEVER render in the Doc - a printed geo tag is a format regression.
- Additional location sets name their city in plain text (there is no `{{CITY_2}}`); populate touches only the first block's `{{CITY}}` header token and the credential line.

**Guideline 5 - Read-through and edge-rounding: catch what sounds weird, repair the surface, report everything.**

The 3A-v2 read-through gate exists because a generated line can pass every mechanical gate while being a sentence no person would say out loud. Populate is the LAST stop before a host reads the document on mic, and populated values change how lines land (a long firm name or podcast name can turn a fine template sentence into a mouthful) - so the same read-through runs here, with a bounded license to repair.

- **The read: every spoken line, out loud, in order.** The setup, the credential, the prompt, all attribute bullets, every Short-Form question and bullet, the outro's three lines. Flag any line with: an ambiguous or long-distance antecedent ("two that went different ways" - two WHAT?); a permission-softened ask where the format wants a directive ("if you have..." instead of "give us..."); a main verb stranded more than ~8 words from its subject; a clause hanging off a noun phrase; a sentence that only works on the page; a populated value that made a line unwieldy (repeat of a long podcast name mid-sentence, a title-cased name colliding with sentence flow).
- **What a repair MAY do (surface only):** sharpen an antecedent, harden a softened ask, split a run-on, reorder clauses, swap a pronoun for its noun, trim a stutter, lift a colloquialism to the professional register. The repaired line says the SAME thing at roughly the same length.
- **Register: this is a professional podcast.** Plain language, never slang. Colloquial money-talk fails the read - "worth completely different money" becomes "can produce widely different settlement amounts"; "what moves that number" becomes "what drives that difference". The test is a managing partner hearing their own show: plain enough for a listener, professional enough that the attorney is never embarrassed by the phrasing. (Gabe, 2026-08-18, on the E3 prompt.)
- **What a repair MUST NEVER do:** add or remove substance, facts, or claims; touch a STATIC string (byte gate still applies); change a question's search-phrase meaning; alter question or bullet COUNTS; introduce jargon, guest framing, or an em dash; rewrite a line that merely could be "better" - the bar is *a person would not say this*, not *I would phrase it differently*.
- **Attribute bullets must be reachable from inside the prompt's answer.** The block is what the attorney covers during a 20-30 minute answer to ONE question, so every bullet needs a natural path from that question's theme. A bullet the attorney could only hit by stopping the story (a pure lawyer-vetting fact with no bridge to the episode's subject) gets flagged - and the repair is a re-detail that gives it the bridge, never a deletion (the count is a gate). E3 example: "Checkable credentials... which anyone can verify" had no path from "what drives settlement differences"; re-detailed as what insurers price into their offer, it does. (Gabe, 2026-08-18.)
- **The attribute block must cohere as a whole, not just bullet by bullet.** Two block-level checks: (a) **relatedness** - every bullet is closely tied to THIS episode's topic, not generic lawyer-vetting boilerplate that could sit under any episode; (b) **order** - the sequence reads sensibly against the topic, ideally tracking its natural chronology (how the matter actually unfolds for a client: what happens first, the treatment and evidence window, getting to a number, the offer, trial). REORDERING bullets is an allowed surface repair - it touches no substance and no counts - and is logged like any other edit. A bullet that is on-topic but sitting in a jarring position gets moved, not rewritten. (Gabe, 2026-08-18.)
- **Zero edits is the expected outcome, not a failure.** A line that sounds natural and professional ships untouched - the pass has no quota and gets no credit for finding things. Most runs on a healthy template should report `Read-through: clean`. An itch to polish a line that already works is the signal to leave it alone. (Gabe, 2026-08-18.)
- **Every repair is reported, none are silent.** Each edit ships as a before/after pair in the report-back and in `metadata.json -> readthrough.edits`. A repair on a line the TEMPLATE carries (vs one created by token resolution) is also flagged `template drift: apply upstream` - the template is canonical, and a populate-side patch that never reaches `/pod-3A-ros-template-v2` gets reintroduced on the next firm's populate.
- **When unsure, flag without repairing.** A line you cannot repair within the surface-only rules gets a `> NEEDS VERIFICATION: reads awkward aloud - {why}` block and ships flagged, for the producer to decide.
- **Origin:** the E3 Eberst test run (2026-08-18). The template prompt shipped "And if you have two that went different ways, take us through both" - fuzzy antecedent, permission-softened ask - and populate copied it verbatim because nothing was allowed to catch it. Gabe: round out the edges if needed.
- **Where it fires in the SOP:** `## Create -> ### Read-through and round the edges`, and the read-through gate in `### Quality gates`.

### Quality gates

Mechanical pass / fail conditions checked in `## Quality Assurance`. The renderer (`scripts/build-client-ros-v2-docx.py`) enforces the starred ones itself before writing any file.

- **Format flag gate** (hard, pre-everything). `episode_format` resolves to `v2-open-interview` AND the upstream template is a `ROS Template v2` artifact whose payload says the same.* Legacy anything -> STOP, route to `/pod-3B-client-ros`.
- **Legacy non-collision gate** (hard, pre-write). Never overwrite, archive, or write beside a legacy `Client ROS` artifact. A legacy artifact in the slot means the episode was recorded in the other format - stop and surface it.
- **Placeholder gate.*** Zero leftover `{{...}}` anywhere in the populated payload and both outputs. All 12 values present and non-empty.
- **STATIC resolved-verbatim gate.*** `welcome` / `welcome_first` equal the template constant with tokens resolved; embedded-name shows compare against the `welcome_embedded` variants (Gabe 2026-08-26); `outro_note` byte-identical. Any other delta means boilerplate was regenerated.
- **Appendix stripped.*** Zero occurrences of `Appendix: Source Question Bank` in the payload or either output; `appendix_question_bank` absent from the JSON.
- **Structure preservation** - single bolded prompt*; Introduction order (welcome, setup, credential, prompt, `ATTORNEY RESPONSE`); exactly ten questions per location*; 2-4 bullets per question*; 10-12 attribute bullets with zero question marks*; outro's three generated lines present*; S2 flows behind a rule, never its own page; heading colors per the template contract.
- **Guest-framing gate.*** Zero hits for `my guest|our guest|today's guest|joining us|thanks for coming on`.
- **Geo preservation** - every S2 question in `client-ros-v2-data.json` carries exactly one `geo_tag`; `source_ngram_ref` preserved wherever the template had one; tags never rendered.
- **Diff-against-template** - a structural diff of the populated `.md` against the template `.md` shows ONLY token resolutions, the two cover deltas, the removed appendix, and the read-through repairs reported in `metadata.json -> readthrough.edits`. Anything else is drift.
- **Read-through gate** (LLM, judgment, runs LAST before render). Every spoken line read aloud per Editorial Guideline 5. Output is the list of flagged lines with repairs applied or `> NEEDS VERIFICATION:` flags - a clean result that quotes nothing did not happen and must be re-run. Zero silent edits: every repair appears in the report-back diff and metadata.
- **v2 marker discipline** - filenames and Doc title carry `Client ROS v2`; a grep of the rendered content for `v2` returns zero.
- **Branded render** - the Doc was built by the bundled renderer; zero leaked inline markup as visible text.
- **Schema validate** - `client-ros-v2-data.json` validates against `references/schema/client-ros-v2.json`.
- **No em dashes.*** Plain hyphens only.
- **Provenance present** - `metadata.json` carries template source path + fileId, the resolved 11 values, recording date, episode number, run timestamp.
- **Artifacts present** - markdown, JSON, metadata written; branded Google Doc exists; both destinations verified.

### Gotchas

- **A legacy template is not "close enough".** If the matching-scope folder holds only a legacy `ROS Template`, the v2 template has not been built - route to `/pod-3A-ros-template-v2`, do not populate the legacy one with this skill or vice versa.
- **Do not "fix" template content during populate.** A typo, an awkward line, a question you would phrase differently - all of it routes back to `/pod-3A-ros-template-v2` (refresh mode) so every future firm inherits the fix. Populate-time edits fork the template silently.
- **The recording date is non-blocking but the cover omits `TBD`.** Never print "Recording: TBD" on a client-facing cover; re-run refresh once the date is set.
- **Client question vetoes route upstream.** If the firm rejects a Short-Form question, the replacement comes from the template's Appendix pull pool via `/pod-3A-ros-template-v2` - this skill never swaps questions itself.
- **Branded output is mandatory.** The pipeline is `client-ros-v2-data.json → build-client-ros-v2-docx.py → DOCX → Drive upload as gdoc mimeType → clean branded Google Doc`. Never upload the `.md` with `convert=true`.

### Iteration log

- **File:** `references/iteration-log.json`. Read at start (`## Checks -> ### Orient`), filter to `status: open` / `in-progress`, surface as known issues. Never written at runtime; appended manually post-run. Append-only. ID format `YYYY-MM-DD-NNN`.

---

## Standard Operating Procedure

```
Multi-mode:  [Checks] -> [Prepare Inputs] -> [Create | Update] -> [Quality Assurance] -> [Ship]
```

## Checks

What is?
The pre-flight phase - resolve the format flag, orient to the right episode folder, verify the upstream ROS Template v2 exists, and decide create vs update.

### Resolve the format flag

- If the matching-scope shared-library folder holds a `ROS Template v2` whose payload says `episode_format: v2-open-interview`, the flag is confirmed - state it in one line. Otherwise ask the user outright; `legacy-segments`, "not sure", or blank -> STOP and route to `/pod-3B-client-ros`.
- **Episode 1 / Founder Story (check FIRST):** Episode 1 always routes to `/pod-3B-client-ros` regardless of format.
- Record the resolved value and its source in `metadata.json -> episode_format_source`.

### Orient

- Read the iteration log; surface open entries.
- Find `{Firm} Podcast/` (fuzzy match). Read `podcast-overview.md` if reachable; auto-fill the Greeting; confirm in one line.
- Navigate to `Episodes/EP{N}: .../Run of Show: .../Client ROS:` - find or create the slot chain. Detect legacy-convention episodes per the legacy skill's rule and follow legacy paths for that episode only.
- Read 1-2 scope-matched examples from `references/examples/client-ros-v2-examples.md`.

### Verify upstream ROS Template v2

- Resolve the `ROS Template v2 .md` + `ros-template-v2-data.json` from `templates [master]/AEO Templates/Podcast/Episode Templates/{Topic}/{scope}/` (Map 2). The `v2` filenames are the discriminator; a legacy `ROS Template` in the same folder is expected and ignored.
- Validate the payload: `episode_format: v2-open-interview`, schema-valid, statics present, ten questions per location. A payload that fails here is an upstream defect - STOP and route to `/pod-3A-ros-template-v2`.
- **Handoff Contract check.** Any undeclared upstream file under consideration -> STOP and ask; never guess silently.

### Existence check

- Look for a `Client ROS v2` Doc + `client-ros-v2-data.json` in the slot. A LEGACY `Client ROS` in the slot is a conflict, not a prior version - stop and surface it.
- **Missing:** route to `## Create`. **Found:** surface provenance and ask refresh in place (-> `## Update`) / archive-and-rebuild (move only the prior Client ROS v2 to `_archive-{YYYY-MM-DD}/`, -> `## Create`) / cancel.

## Prepare Inputs

- **Load the template trio.** Parse `ros-template-v2-data.json` (the populate source) and hold the template `.md` for the diff gate.
- **Resolve the 11 values** per Guideline 1 - Supabase first (`#### Supabase firm lookup`), then podcast-overview, then ONE consolidated ask for everything missing. Show the resolved set in one line for confirmation. Apply the conversions: state code -> full name, phone -> `(XXX) XXX-XXXX`, website with `https://`, years as an integer.
- **Resolve recording date (TBD default) and episode number** (next available under `Episodes/` if unset).
- **Resolve branding** (folder id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`); per-client `brand.json` typography overrides the CE default when present.

## Create

What is?
The create branch - the mechanical populate. Best Practices: Guidelines 1-4 apply to every step; a violation emits `> NEEDS VERIFICATION:` at the location instead of shipping.

### Populate the payload

- Deep-copy the template payload. For every string field, resolve the 12 tokens with `.replace()` per Guideline 1. Never `str.format()`.
- Add the `firm` block (the 11 resolved values plus `recording_date` and `episode_number`).
- Set `static.welcome` to the resolved `welcome_first` constant when this is Episode 1 of the show (`is_first_episode: true`) - otherwise the resolved `welcome`. Embedded-name shows take the resolved `welcome_embedded` / `welcome_embedded_first` instead (Gabe 2026-08-26).
- Remove `appendix_question_bank` and `placeholders_used`. Keep every S2 question's `geo_tag`, `source_ngram_ref`, `topic_plan_ref`, and `kind` untouched.
- Scan the whole payload for leftover `{{...}}` - any hit is a hard stop, listed in full.

### Read-through and round the edges

- Run the Editorial Guideline 5 read: every spoken line, aloud, in order - setup, credential, prompt, attribute bullets, every Short-Form question and bullet, the three outro lines.
- Apply surface-only repairs to lines that fail the say-it-aloud bar; record each as a before/after pair in `metadata.json -> readthrough.edits` with an `origin` of `template` (line carried by the template - flag `template drift: apply upstream`) or `populate` (weirdness created by token resolution).
- Lines that cannot be repaired within the surface-only rules get `> NEEDS VERIFICATION:` blocks and ship flagged.
- STATIC strings are read but NEVER repaired here - a STATIC that reads wrong is a template-level change routed to `/pod-3A-ros-template-v2`.

### Render markdown and payload

- Serialize `client-ros-v2-data.json`; validate against `references/schema/client-ros-v2.json`.
- Run `scripts/build-client-ros-v2-docx.py` - it enforces the starred gates and emits the `.docx` + `.md` pair in the locked shape.
- Write `metadata.json` with the provenance block per `## INTERNAL`.

## Update

What is?
The update path - re-populate in place, preserving manual edits.

- **Diff before write.** Existing `client-ros-v2-data.json` + `.md` vs the proposed new state; surface every changed block.
- **Preserve manual edits.** Any line manually edited since the last run keeps its value; conflicts get `> NEEDS VERIFICATION: auto-generated value [X] conflicts with manual edit [Y]` inline, never auto-resolved. Note the template's own Update contract: the outro's three lines regenerate upstream by design, so a diff there when the TEMPLATE was refreshed is expected. Prior read-through repairs (from `readthrough.edits`) follow the same rule as manual edits - EXCEPT when the refreshed template itself fixed the line, in which case the template's version wins and the stale repair is dropped.
- **Stable fileId.** `files.update` against the existing Doc; never delete-and-recreate.
- The shared `## Quality Assurance` phase runs after.

## Quality Assurance

**First - Best Practices by name:** Quality bar, Sourcing discipline, Guidelines 1-4, the full Quality gates checklist.

**Second - Anti-AI Detection two-pass scan** (canonical doc: https://docs.google.com/document/d/1hp7bxOFRlMhCuhjHNY0j05JrB97-KOFD0XUCQM3gMBU/edit). Pass 1 mechanical (em-dashes, banned vocabulary/phrases, triadic rhythms, date formats, no emojis); Pass 2 skeptical re-read from the top; fix and re-run until clean. Populate introduces little new text, but the firm values and any Update-mode merges are exactly where a slip hides.

**Third - skill-specific mechanical checks:** run every gate in `### Quality gates` explicitly - grep for leftover tokens, grep the rendered content for `v2`, grep for the appendix heading, diff structure against the template `.md`, verify both write destinations carry the same artifacts, verify the INTERNAL grep test on the client-facing Doc.

**On failure:** fix the payload, re-render, re-upload via `files.update`, re-run all checks. Do not proceed to `## Ship` until clean.

## Ship

### What ships

Client ROS v2 (branded Google Doc, stable fileId) + `.md` (text/markdown) + `client-ros-v2-data.json` + `metadata.json`.

### Where it ships

- **Drive:** the cell's `Client ROS:` slot per Map 6 (path tree in `### Outputs`).
- **Local mirror:** `~/Desktop/claude_code/deliverables/podcast/Client ROS/{Topic}/{Episode}/{scope}/`.

### How it ships

- Build via `scripts/build-client-ros-v2-docx.py` (never a raw markdown→Doc upload). Upload the `.docx` as `application/vnd.google-apps.document`; the `.md` as `text/markdown`; JSONs as-is. First create uses `files.create`, every subsequent write `files.update` against the stored fileId. Roboto pass after upload.
- On a write error to one destination, ship to the other and report the partial state; if both fail, hard-fail loudly.
- **Report back:**

  ```
  Done. Client ROS v2 populated for {Firm} - {Episode} ({Location}).

   Folder: https://drive.google.com/drive/folders/{folder_id}
   Client ROS v2 (branded Google Doc): https://docs.google.com/document/d/{doc_id}

  Tokens resolved: 12/12. Locations: {n} x 10 questions. Appendix: stripped.
  Statics: verbatim. Recording date: {date|TBD}. QA gate: PASS.
  Read-through: {clean | N edge repairs applied - diffs below | N lines flagged NEEDS VERIFICATION}.
  {before -> after, one line each; template-drift repairs marked "apply upstream"}
  ```

### Who to Notify

`notify: []` - the producer is informed via the inline report-back.

---

## INTERNAL (not for client distribution - auto-stripped from all exports)

### Provenance block

`metadata.json` must include: `run_date`, `episode_format`, `episode_format_source`, `template_source` (path + Drive fileId + template metadata run date), the resolved 11 values, `recording_date`, `episode_number`, `is_first_episode`, `references_status`, `schema_status`, `location_count`, `geo_tag_counts`, `readthrough` (`{result: clean|edited|flagged, edits: [{location, before, after, origin: template|populate, reason}], flags: [...]}`), Drive fileIds (canonical).

### Why this skill exists as a sibling rather than a patch

The legacy `pod-3B-client-ros` populate machinery is load-bearing for every legacy-format client: the Entity Checklist, entity underlining, the sequential-numbering gate, the city-share rule, the 12-token taxonomy. Patching v2 awareness into it would mean every gate branching on format, and a regression in either branch shipping to both. Two skills behind one flag - the same coexistence pattern as `pod-3A-ros-template` / `pod-3A-ros-template-v2` - keeps each format's contract enforceable in isolation. When the last legacy client flips or churns, the legacy skills retire whole.

---

## Learning & Iteration

- [ ] After each run, append GOOD / BAD / EDGE CASE entries to `references/examples/client-ros-v2-examples.md` - especially value-conversion edge cases (multi-state firms, hyphenated cities, firms with no podcast name yet).
- [ ] Track recurring missing firm fields; recurring asks belong in the podcast-overview doc.
- [ ] Watch the diff gate: if populated docs keep drifting from their templates, something upstream or in Update-mode merging is leaking.

## Change Log

| Date | Change |
|---|---|
| 2026-08-26 | **Embedded-name welcome variants and Question Pool rename (Gabe, 2026-08-26).** Populate accepts either welcome constant: the standard string, or `welcome_embedded` / `welcome_embedded_first` when the podcast name embeds the attorney's name (e.g. "Car Accident Attorney w. Robert May") - "with **{{ATTORNEY_NAME}}**" would double the name. A "w." in the podcast name is spoken, and rendered in the welcome, as "with"; the renderer also accepts the resolved constant with that spoken form applied. "Swap pool" renamed "Question Pool" in user-facing text (display labels and prose only). Attribute block pinned as bullets, never a numbered list. Files: this file, `scripts/build-client-ros-v2-docx.py`. | Gabe Jordan |
| 2026-08-21 | **v1.3.0 - v2 branch now TERMINATES at Client ROS v2; `pod-3C-client-guide-v2` retired.** Gabe directive: the v2 pipeline ends here. `pod-3C-client-guide-v2` was removed from `~/.claude/skills/` and archived whole to `~/Desktop/claude_code/_archive/retired-skills/pod-3C-client-guide-v2--retired-2026-08-21/`. Every active downstream reference in this file was cleared: frontmatter description, the "NOT the attorney-facing document" framing (now stated neutrally - this is the interviewer's working document and the final artifact the v2 chain produces; whether the attorney receives a copy is undecided), the Workflow chain prose and ASCII diagram (now ends at pod-3B-client-ros-v2), the JSON output and local-mirror consumer notes, Routing -> Downstream (now "none - terminal step"), both Handoff Contract rows, and the report-back "Next:" line. Artifacts themselves are unchanged - `client-ros-v2-data.json`, the `.md`, the branded Doc, and `metadata.json` are all still written on every run. The LEGACY chain is untouched: `pod-3C-client-guide` (no -v2) still runs downstream of `pod-3B-client-ros`. Revert: restore the archived skill folder to `~/.claude/skills/pod-3C-client-guide-v2/` and re-add it as the downstream consumer at the ten sites listed above. | Gabe Jordan |
| 2026-08-18 | **v1.2.0 - read-through edge-rounding pass added (Editorial Guideline 5).** Populate gains its one bounded editorial license: after token resolution, every spoken line is read aloud, and a line no person would actually say may receive a SURFACE-ONLY repair (antecedent sharpening, hardening a permission-softened ask, splitting a run-on) - same substance, same register, roughly same length. Hard limits: never a STATIC string, never counts or structure, never new substance, never a preference rewrite; the bar is 'a person would not say this'. Zero silent edits: every repair ships as a before/after diff in the report-back and metadata.json -> readthrough.edits, and repairs to template-carried lines are flagged 'template drift: apply upstream' so the canonical fix lands in pod-3A-ros-template-v2 rather than being re-patched per firm. New SOP step (Create -> Read-through and round the edges), new read-through QA gate (LLM, runs last, must quote what it checked), diff-against-template gate amended to admit reported repairs, Update mode drops a stale repair when the refreshed template fixed the line itself. Origin: E3 Eberst test run - the template prompt's 'And if you have two that went different ways, take us through both' (fuzzy antecedent + softened ask) passed populate verbatim because nothing was allowed to catch it. Gabe directive: template side gets the generation fix; this skill rounds the edges. Revert: remove Guideline 5, the SOP step, the read-through gate, and the readthrough metadata block. | Gabe Jordan |
| 2026-08-18 | **v1.1.0 - Supabase wired as the canonical firm-data source; first live test run.** Added `#### Supabase firm lookup` (Gabe directive): resolution order is now Supabase (client_profiles + client_field_values, service_role via op-broker) -> podcast-overview -> user ask, with the full token->field map, MERGED-row skip rule, and per-value provenance in metadata.json. Two KNOWN GAPS flagged: no Supabase field yet for {{PODCAST_NAME}} or {{INTERVIEWER}} (fall back to podcast-overview / prior Client ROS / user until aeo_podcast_name + aeo_ce_host exist). Derived values ({{ATTORNEY}} from cont_marketing_poc_name, {{YEARS_PRACTICING}} from biz_open_date) are Inferred until confirmed. Test run shipped against the live E3 Eberst prototype Doc (Stuart + Gainesville, 7 of 11 tokens present): payload parsed from the Doc, 9 of 11 values resolved from Supabase, populate + render clean (0 leftover tokens, appendix stripped, statics verbatim), uploaded to the Drive TEST folder for review. | Gabe Jordan |
| 2026-08-18 | **v1.0.0 - initial build.** Sibling of pod-3B-client-ros (v3.3.0, untouched), consuming the v2 format from pod-3A-ros-template-v2 v1.4.0. Resolves 3A-v2 ship blocker 2026-08-14-001: populates the eleven-token v2 taxonomy (adds {{TOPIC}}, {{CITY}}, {{ATTORNEY}}, {{INTERVIEWER}}, {{YEARS_PRACTICING}}; drops legacy {{ATTORNEY_FIRST_NAME}}, {{HOST_NAME}}, {{PRACTICE_AREA}}, body {{EPISODE_NUMBER}} and {{RECORDING_DATE}}), strips `# Appendix: Source Question Bank` (not the legacy Additional Questions reserve), preserves per-question `geo_tag` + `source_ngram_ref` into `client-ros-v2-data.json`, and adds the STATIC resolved-verbatim gate. Populate machinery the v2 format retired is deliberately absent (Guideline 3): Entity Checklist, entity underlines, sequential-renumbering gate, episode-goal slices, city-share rule. Renderer `scripts/build-client-ros-v2-docx.py` is the populate-side mirror of the 3A-v2 renderer (same primitives, same locked shape, minus the appendix, plus firm-name and recording-date cover lines) with hard populate gates: zero leftover tokens, statics-resolved-verbatim, appendix absent, guest framing, AT-1/AT-2, ten-per-location, 2-4 bullets, em-dash. Smoke-tested against the Eberst E2 example payload (2 locations x 10, 11/11 tokens, negative tests for leftover-token and scrub gates). Filename/Doc-title carries `Client ROS v2`; rendered content never says v2 (Gabe directive 2026-08-18). Revert: delete this skill folder; nothing else in the pipeline was modified. | Gabe Jordan |
