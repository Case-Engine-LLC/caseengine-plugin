---
name: pod-3C-client-guide
description: >
  Generate the attorney-facing podcast episode prep guide from a completed
  Client ROS - a clean, stripped-down prep doc the attorney reads before
  recording day. Use whenever someone says "create client guide for [firm]",
  "build the episode guide", "make the podcast guide for [client]", "client
  prep doc for [episode]", "attorney prep guide", "recording prep for
  [client]", "client guide from the ROS", or "/pod-3C-client-guide". Phase 3 Run
  of Show of the podcast pipeline; hard dependency on a completed Client ROS
  from pod-3B-client-ros. This is the final step of the podcast pipeline.
skill_kind: hybrid
modes: multi
inputs: [client-ros.md, client-ros-data.json, podcast-overview.md, user-supplied-firm-data, case-engine-branding]
outputs: [json, markdown, gdoc]
notify: []
metadata:
  version: 3.3.0
  date: 2026-07-31
  owner: Gabe Jordan
  version_history: >
    1.0 - co-work Drive-native version (2026-04-20). 2.0.0 - merged cowork
    client-guide canonical content with original local pod-9 Mode A
    enrichments (2026-05-14). 3.0.0 - renamed pod-9A-client-guide ->
    pod-3C-client-guide; full structural refactor to the canonical CE skill
    structure; probe apparatus and Mode A/B branching stripped (2026-05-20).
    3.1.0 - Attorney response bullets from the Client ROS now appear as
    sub-bullets under each question in the Segment Breakdown, giving the
    attorney the full mandatory infill as part of prep (2026-05-26).
    3.2.0 - added Episode 1 / Founder Story hardcoded exception: duplicate the
    Founder Story Client Guide master template and populate firm tokens; no
    Client ROS dependency (2026-06-08).
    3.2.1 - three-field geo model terminology alignment: Targeting strategy /
    Optimization scope (show anchor) / Episode geo target; added the
    "anchor scope != per-episode target" rule to Gotchas (2026-07-10, Gabe
    directive from the Whalen scoping).
---

# Client Guide

> **Drive write governance:** All Drive operations (create, update, rename, move) follow [Ship]. Revise in place via `files.update` against the existing fileId, never delete-and-reupload (breaks the fileId/URL chain and silently kills every downstream reference).

### What is

The Client Guide - the attorney-facing podcast episode prep doc. This skill takes a completed Client ROS from `pod-3B-client-ros` and translates the production script into a clean, stripped-down prep document the attorney reads the night before recording. It tells them what the episode covers, what themes to be ready to discuss, how to prepare, what materials to pull together, and what the recording experience looks like. It is NOT the host's script - the Client ROS is the host's live on-air guide with speaker tags, producer notes, and the Entity Checklist. The Client Guide deliberately strips all production scaffolding: no entity architecture, no producer notes, no speaker tags, no n-gram references, no "Run of Show" phrase. The Client Guide lands in the firm's episode `Client Guide:` slot per Map 6, mirrored to the local Desktop path.

### Workflow

Client Guide is the third step of **Phase 3 (Run of Show)** of the podcast pipeline. It runs AFTER `pod-3B-client-ros` completes, consumes the Client ROS as its sole source of truth, and translates it into attorney-facing language. It is the final automated step of the pipeline; after it, AM sends the guide to the attorney before recording day.

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
- **Phase 3 Run of Show** - `pod-3A-ros-template` builds the tokenized template; `pod-3B-client-ros` populates it for a firm; `pod-3C-client-guide` (this skill) derives the attorney guide from the Client ROS. Phase 3 steps are sequential; the Client Guide is the final step.

Prerequisites: a completed Client ROS from `/pod-3B-client-ros` is a hard dependency - this skill will not run without it.

> **Episode 1 - Founder Story is a HARDCODED exception.** Episode 1 of every client's show is the **Founder Story** interview (formerly the "YOU Interview"). Its Client Guide is NOT derived from a Client ROS via the normal flow - a single pre-built, tokenized Client Guide template is the fixed source of truth at `templates [master]/AEO Templates/Podcast/Episode Templates/Founder Story/` (`Client Guide // Founder Story (Episode 1) [TEMPLATE]`, co-located with the Founder Story ROS template). For Episode 1, this skill's job is to **duplicate that Founder Story Client Guide template and populate the firm's tokens** - there is no Client ROS dependency to read from. The content comes from the template, not research - you may lightly vary wording or order so each firm's copy is not 100% identical, but do not regenerate it from scratch.

### Trigger phrases

- `/pod-3C-client-guide`
- "create client guide for [firm]"
- "build the episode guide"
- "make the podcast guide for [client]"
- "client prep doc for [episode]"
- "attorney prep guide"
- "episode prep guide for [client]"
- "recording prep for [client]"
- "client guide from the ROS"

### Greeting

Hi, I'm Client Guide. Before I run, I need to confirm the podcast architecture. If podcast-overview has been run for this client, I'll read it and confirm in one line. If not, I'll ask:

1. **Client name.** Examples: "The May Firm", "Sutliff & Stout", "Conn Law Firm".

2. **Optimization scope (show anchor) - what the podcast as a whole is optimized to rank for?**
   - **City:** people search the city as a unit. Anchor: Houston.
   - **State:** people search the state. Anchor: California. Per-city episodes under it.
   - **County / Regional:** people search the region. Anchor: Inland Empire, Harris County, Bay Area.

3. **Episode geo targets / extension locations (if any).** The specific city each individual episode is built to rank for. Under the legacy single-anchor model these are sub-scope derivatives that inherit from the anchor (10-12 questions, ~30-35 min); under a multi-location targeting strategy each ARE the episode (client-facing term "Mini episode", no single anchor, one per target city). Can exist under any anchor:
   - Houston city anchor -> Sugar Land, Katy, Pasadena suburb targets
   - California state anchor -> Bakersfield, Fresno, Long Beach city targets
   - Inland Empire regional anchor -> Ontario, Riverside, San Bernardino

4. **This run's Episode geo target** - the anchor city itself, or a specific extension city?

5. **Episode format** - resolved by the client's **Targeting strategy** (single-location vs multi-location; recorded in the podcast overview, ask if absent): single-location -> Full episode (~50-55 min, ~20 questions); multi-location -> Mini episode per Episode geo target city (~30-35 min, 10-12 questions, internal scope label stays `Extension`, no single anchor episode).

I translate a completed Client ROS into a clean, client-facing prep doc the attorney reads the night before recording. Different deliverable from the Client ROS. Attorney-friendly tone, no production jargon, no entity architecture, no internal metrics - just the episode overview, what to think about, what to do, segment breakdown, and FAQ.

Then my skill-specific follow-ups:

6. Is there a completed Client ROS in the right slot - `{Firm} Podcast/Episodes/EP{N}: {episode_name} // {client_name}/Run of Show: {episode_name} // {client_name}/Client ROS: {episode_name} // {client_name}/` (produced by `/pod-3B-client-ros`)? If it's not there, I stop and route you to `/pod-3B-client-ros`.
7. Host name for the guide (the name the attorney sees referenced in the FAQ).
8. Does the target `Client Guide:` slot already have a Client Guide? Archive and rebuild, or refresh in place? (I archive only the Client Guide file - the ROS Template + Client ROS siblings stay put.)

If anything's unclear I'll ask once in a single message. I won't touch Drive until you say go. You only need to know about `{Firm} Podcast/` - I handle the foundation lookups and writes transparently.

---

## Best Practices

The WHAT contract. Every other section references these by name; the SOP never restates them.

### Inputs

What is?
The materials this skill ingests - the completed Client ROS and its data payload (hard dependency), the host name, the podcast architecture doc, and the Case Engine Branding folder - all resolved before any guide is drafted.

#### Required

- **Completed Client ROS** (`client-ros.md` + `client-ros-data.json`) - the populated host script from `/pod-3B-client-ros`, read from the cell's `Client ROS:` slot. It is the sole source of truth for the guide's content. No silent fallback - if it is missing, the skill stops and routes to `/pod-3B-client-ros`.
- **Firm name** - matches the Client ROS metadata.
- **Episode title** - matches the Client ROS metadata. **CANONICAL SOURCE:** the episode's topic/title is governed by the PUBLISHED Google Doc Topic Plan (the client edits that Doc manually); the guide inherits the episode from the Client ROS, which must itself trace to the live Doc - never to a local `topic-plan-v{n}.*` or old file. Never produce a guide for a topic absent from the Doc's lineup (Eberst E5 slip-and-fall wrong-episode incident, 2026-06-19).
- **Host name** - the CE host on the recording, used in the FAQ references.

#### Optional

- **Optimization scope (show anchor)** - City / State / County / Regional. Auto-read from `podcast-overview.md` if present; sets the show-level framing in the Episode Overview ("across California" vs "in Houston"). The specific city an episode is framed around is the **Episode geo target**, inherited from the Client ROS - the anchor is the ceiling, the episode target is what the copy emphasizes (see the "anchor scope != per-episode target" rule in Gotchas).
- **Episode scope** - the internal scope label (Topic Only / Location / Extension) of the parent Client ROS; the Episode geo target city it carries is inherited from the ROS, not re-derived here.
- **Refresh flag** - default refresh in place (routes to `## Update`). Pass `archive-and-rebuild` to archive the existing Client Guide to `_archive-{YYYY-MM-DD}/` and rebuild.

#### Auto-read (no action required)

- **`podcast-overview.md`** - architecture source of truth (Targeting strategy, Optimization scope / show anchor, Episode geo targets, client name). If present at `{Firm} Podcast/.podcast-overview/podcast-overview.md` (or the local mirror), the skill auto-fills Greeting questions 1-3 and supplies the FAQ recording-logistics context; otherwise it asks. The overview is supplemental context only - all episode content must trace back to the Client ROS.
- **Firm identity fields (required from the user)** - the firm's brand name and websites (attorney / podcast / business) are supplied directly by the user, or read from the podcast-overview doc when present, to populate the FAQ and branding hints. There is no CRM / DB lookup; a missing field is a prompt to the user.
- **Case Engine Branding folder** - the canonical brand reference at [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) (folder id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`). The `## Ship` build reads logo, colors, fonts, and the [Cover Page Spec](https://docs.google.com/document/d/1oydpI055jbj1FYDGeZfHQeMNjaWKUCFVGCRveeuJJCk/edit). Brand values resolve from the folder at build time - never inlined.
- **Local Client Guide example references** - bundled `references/examples/client-guide-examples.md` as the quality-anchor set. If missing or empty, fall back to methodology and flag `"references": "empty"` in `metadata.json` - do not block.

#### Capabilities

The skill runs locally in Claude Code and calls its tools directly - it assumes they exist and uses them in this priority order. On a tool error, it skips that source and degrades to the next; it never probes for availability first.

- **Local filesystem read** - for an auto-detected local populated Client ROS at the canonical Desktop path and a local `podcast-overview.md`. Fastest path; no Drive round-trip. If a local populated ROS exists but the matching Drive Client ROS does not, halt and surface the mismatch - do not silently pick one.
- **`gws drive`** (or `mcp__claude_ai_Google_Drive__*` connector) - for the Client ROS + `client-ros-data.json` from the cell's `Client ROS:` slot, the podcast-overview doc, and the Case Engine Branding folder.
- **`mcp__ce-services__rag_query`** (`rag_name: koray`) - optional, for SEO-grounded mental-model prompts when drafting the Pre-Interview Prep "Things to Think About" reflective prompts; supplemental only, every prompt must still trace back to the Client ROS.
- **User-supplied materials** in the greeting (pasted Client ROS content, dropped files) and user interview for hard requirements still missing - the always-available floor.
- **Hard requirement** - the completed Client ROS must resolve via local read or Drive. If it is missing, the skill stops and routes to `/pod-3B-client-ros`.
- **Behavior on a tool error** - skip that source and degrade to the next. With no reachable source, fall through to user-supplied + interview; flag every Inferred value with `> NEEDS CONFIRMATION:` per Sourcing discipline.

### Outputs

What is?
The artifacts this skill ships - the 3-format trio (a machine-readable JSON payload, a markdown source-of-truth, and a CE-branded Google Doc) plus a `metadata.json` provenance file - landing in the firm's episode `Client Guide:` slot per Map 6, mirrored to the local Desktop path.

#### Output formats

CE-wide default: every persistent artifact ships in three formats.

- **JSON** - `client-guide-data.json` - structured / machine-readable payload, the input the build script renders from. Validates against `references/schema/client-guide.json`. Downstream consumers read this for the guide structure.
- **Markdown** - the Client Guide `.md` - local source-of-truth mirror, the raw markdown deliverable uploaded to Drive as `text/markdown` (no conversion). Retains the `## INTERNAL` block.
- **Google Doc** - the human-facing CE-branded Client Guide Doc. Built from a CE-branded `.docx` (cover page, logo, Roboto body, "Prepared by Case Engine" footer) emitted by `scripts/build-client-guide-docx.py`, then uploaded with `mimeType: application/vnd.google-apps.document` so Drive auto-converts the DOCX to a clean Google Doc. Created / updated in-place via `files.update` against a stable fileId so the URL never breaks for downstream links.

A `metadata.json` provenance file ships alongside the trio (internal-only, not a client-facing artifact - records the source Client ROS path, run date, scrub result).

#### What ships

- **Client Guide** - Google Doc - human-facing CE-branded view, cover page, Roboto typeface, stable fileId.
- **Client Guide `.md`** - Markdown - raw markdown deliverable, retains the `## INTERNAL` block.
- **`client-guide-data.json`** - JSON - machine-readable payload; validates against `references/schema/client-guide.json`.
- **`metadata.json`** - JSON (internal) - provenance: source Client ROS path, run date, scrub result, references status.

#### Drive destination

Shared drive root: `Podcasts // Case Engine [Shared]` (id `0AAJKtWTUAZhHUk9PVA`). Per [Client Folder Structure](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU/edit) → Map 6, the Client Guide lands in the cell's `Client Guide:` slot directly inside the episode parent (NOT nested inside `Run of Show:`).

```
{Firm} Podcast/Episodes/EP{N}: {episode_name} // {client_name}/
  Run of Show: {episode_name} // {client_name}/
    Template ROS: {episode_name} // {client_name}/                                     (from pod-3A-ros-template - read-only context)
    Client ROS: {episode_name} // {client_name}/                                       (from pod-3B-client-ros - this skill's source)
  Client Guide: {episode_name} // {client_name}/                                       ← THIS SKILL writes here
    E{N}: {Episode Title} // {Firm Name} // Client Guide - {Location}.md                raw markdown source (text/markdown)
    E{N}: {Episode Title} // {Firm Name} // Client Guide - {Location}                   branded Google Doc (in-place files.update)
    client-guide-data.json                                                              machine-readable payload
    metadata.json                                                                       provenance
    _archive-{YYYY-MM-DD}/                                                              (only the prior Client Guide, if one existed)
```

Each recording cell - anchor or extension - is its own `EP{N}: ...` entry in `Episodes/`; extensions are siblings of the anchor at the EP level, each with its own localized `{episode_name}`. The double-slash ` // ` separator with spaces is literal. Append ` (Extension)` after `{Location}` for extension cells. At Topic Only scope drop the ` - {Location}` suffix and use plain `Client Guide.md` / `Client Guide`. Generic names alone are not allowed for client cells - aggregated Drive views collapse every episode into a single visual line without the episode-first prefix. The Drive destination is fixed - this skill does not move existing Drive data.

**Legacy compatibility:** MVP Accident Attorneys and any other client with pre-2026-05-15 episodes use the older `EP{N}: Client Guides // {Firm}/` or `01 Strategy/` convention. If the resolved episode parent contains a `Client Guide: {episode_name} // {client_name}/` subfolder, it is a Map 6 episode. If instead it contains an `EP{N}: Client Guides // {Firm}/` or `01 Strategy/` subfolder, it is a legacy episode - read the Client ROS and write the Client Guide per the legacy path for that episode only (do not auto-migrate).

#### Local mirror

`~/Desktop/claude_code/deliverables/podcast/Client Guide/{Topic}/{Episode}/{scope}/` - holds the same Client Guide `.md`, the CE-branded `.docx`, `client-guide-data.json`, and `metadata.json`. `{scope}` = `Topic Only`, `Locations/{Location}`, or `Extensions/{Location}` to mirror the Drive scope convention. The mirror keeps the DOCX (not the auto-converted Google Doc, which only exists in Drive). It enables fast local iteration, downstream local-skill consumption, and offline review. Written on every run.

#### Schema

`references/schema/client-guide.json` - the canonical JSON schema `client-guide-data.json` validates against. The build script validates against it. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed - do not block on a missing schema.

#### Sections INCLUDED in the client-facing Google Doc

- Branded cover page (CE logo, "Client Guide" title, the EPISODE TITLE as the prominent subtitle, the CLIENT/FIRM NAME as a secondary line, the "{Practice Area} | Location - {Location}" line, "Prepared by Case Engine" + date footer). The episode title is MANDATORY on the cover.
- `## Episode Overview` (value-prop lead + Metadata + Episode Plan)
- `## Pre-Interview Prep` (Things to Think About + Things to Do)
- `## Segment Breakdown` (italic intro + per-segment italic goal + Questions list, each question carrying its attorney-response bullets verbatim from the Client ROS as sub-bullets)
- `## FAQ` (5 seed + 2-3 episode-specific)

#### Sections EXCLUDED (never in the client-facing artifact)

- `## Quality Assurance` and everything from that heading onward
- Any internal jargon - "Run of Show", "ROS", "n-gram", "entity architecture", internal tool names
- An Internal Setup block (ClickUp-only legacy)
- The Entity Checklist table, Producer Notes, speaker tags, ROS Appendix material (those belong in the Client ROS or ROS Template)

The Google Doc renderer truncates the markdown source at the first `## Quality Assurance` heading and discards everything after - the client-facing Doc is exactly Episode Overview → Pre-Interview Prep → Segment Breakdown → FAQ, nothing before except the cover page. See `## INTERNAL` for the grep test.

#### Capabilities

Both write destinations are written every run. On a write error to one, the skill ships to the other and surfaces the partial state in the report - it does not silently lose the deliverable.

- **Drive** - `gws drive` (or `mcp__claude_ai_Google_Drive__*` connector) - writes the markdown, the branded Google Doc, the JSON, and metadata into the cell's `Client Guide:` slot.
- **Local mirror** - local filesystem write to the local mirror path, alongside the Drive write.
- **Behavior on a write error** - if one destination errors, ship to the other and report the partial state. If both error, hard-fail with a clear message; do not silently lose the deliverable.

#### Examples

`references/examples/client-guide-examples.md` - single doc with GOOD / BAD / EDGE CASE labeled sections per CE convention. Read 1-2 examples matching the requested scope as calibration before generating. If the folder is empty, proceed on methodology and flag `"references": "empty"` in `metadata.json`.

#### Routing

- **Upstream (required, hard dependency):** `/pod-3B-client-ros` - the completed Client ROS.
- **Downstream:** none - the Client Guide is the final automated step of the pipeline. AM sends this guide to the attorney 48-72 hours before recording.
- **Refresh:** re-run with the same episode + scope (routes to `## Update`).

#### Handoff Contract

This skill produces the attorney-facing Client Guide:

| Artifact | Consumed by | What downstream reads |
|---|---|---|
| Client Guide `.md` + branded Google Doc | human (attorney) | The full prep doc - Episode Overview, Pre-Interview Prep, Segment Breakdown, FAQ |
| `client-guide-data.json` | (not consumed downstream) | The structured guide payload - segments, questions, episode metadata |
| `metadata.json` | (not consumed downstream) | Internal provenance - source Client ROS path, run date, scrub result |

Downstream consumers can rely on: the Google Doc URL is stable for the lifetime of the Client Guide (preserved via `files.update` across re-runs); `client-guide-data.json` validates against `references/schema/client-guide.json`; the guide carries zero internal jargon. Upstream pull (hard dependency): the Client ROS + `client-ros-data.json` from `/pod-3B-client-ros` in the cell's `Client ROS:` slot. The skill refuses to run without it.

### Framing

The Client Guide is a TRANSLATION of the Client ROS into attorney-facing language, not a rewrite and not a copy. Every element traces back to what the Client ROS says - if the ROS does not say it, the guide does not invent it. It is never the host's script (that is the Client ROS, `pod-3B-client-ros`), never a legal brief or research document, and never an internal production document - it strips all entity architecture, producer notes, speaker tags, and Appendix content.

### Quality bar

What "good" looks like - the pass / fail intuition.

- The document is exactly Episode Overview → Pre-Interview Prep → Segment Breakdown → FAQ, in that order, nothing before except the cover page, nothing after.
- The Episode Overview opens with the value proposition to the attorney's business, not a topic list.
- The Segment Breakdown lists the actual questions from the Client ROS verbatim (cleaned for client language), not vague paraphrased "topic areas". Each question carries its attorney-response bullets from the Client ROS verbatim as sub-bullets so the attorney has the full mandatory infill in their prep doc.
- Every element traces back to the Client ROS - nothing invented, nothing pulled from podcast-overview that the ROS does not ground.
- Zero internal jargon - no "Run of Show", "ROS", "n-gram", "entity architecture", internal tool names, pricing, or production metrics.
- No Internal Setup block, no Entity Checklist, no Producer Notes, no speaker tags.
- The human-facing Google Doc is the CE-branded DOCX→Doc, never a raw-markdown→Doc upload.
- No em dashes, no banned vocabulary - the Anti-AI Detection scan fires before publish.

### Sourcing discipline

The Confirmed / Inferred / Unknown three-state pattern. Never block, always ship, never silent. The Client Guide still ships when data is incomplete; gaps surface in `## INTERNAL` or with `> NEEDS VERIFICATION:` blocks.

- **Confirmed** - claim traces to a specific source. Every guide element drawn directly from the Client ROS is Confirmed. Ship as-is, no marker.
- **Inferred** - sensible default applied when the Client ROS is insufficient (e.g., a Pre-Interview Prep prompt phrased with content-gap framing, or an episode-specific FAQ inferred from the topic). Ships with `> INFERRED: {what + why}` flag.
- **Unknown / NEEDS CONFIRMATION** - no source AND no defensible default. Ships with `> NEEDS CONFIRMATION: {what's missing}` block, never silently synthesized. A guide element with no ROS grounding and no defensible default is NEEDS CONFIRMATION - never invent content the ROS does not imply.

### Editorial Guidelines

Cross-cutting content rules for the guide. The SOP points back here; the rules live here once.

**Guideline 1 - The locked canonical structure, always this order, always these sections.**

- **Structure:** `## Episode Overview` (value-prop lead + `### Metadata` + `### Episode Plan`) → `---` → `## Pre-Interview Prep` (`### Things to Think About` + `### Things to Do`) → `---` → `## Segment Breakdown` (italic intro paragraph + per-segment `### {Segment}` with an italic goal paragraph + a `#### Questions` list, each question carrying its attorney-response bullets verbatim from the Client ROS as indented sub-bullets) → `---` → `## FAQ`.
- **Episode Overview** opens with the value proposition to the attorney's business (why this recording matters to their practice - SEO visibility, trust, authority, differentiation), then `### Metadata` (Episode Topic in plain language, Estimated Duration as a range with question + segment counts), then `### Episode Plan` (Pre-Show Checks / Episode with Intro + S1..Sn + Outro / Post-Show Wrap-up).
- **Pre-Interview Prep** - `### Things to Think About` is 4-6 reflective mindset prompts (NOT tasks - "How would you explain X?", "What do you wish every client knew about Y?"); `### Things to Do` is 4-6 actionable prep items, always including "Have your contact information ready". Every bullet in both sections uses the scannable format `**Bold lead sentence with period.** Regular-weight detail that follows.`
- **Segment Breakdown** opens with an italic intro paragraph, then per segment an italic segment-goal paragraph + a `#### Questions` list. Each question in the Questions list is rendered as `- Q{N}: {question text}` - the `Q{N}` labels are clean sequential 1..N inherited from the Client ROS, never the raw n-gram bank index (gaps/out-of-range numbers fail the Sequential numbering gate) - followed by the attorney-response bullets from the Client ROS as indented sub-bullets (`  - **Label:** detail`), pulled verbatim including their pandoc `[entity]{.underline}` runs. The Intro and Outro segments get an italic goal paragraph but no Questions list.
- **FAQ** - the 5 seed FAQs (recording length, written answers, not knowing an answer, episode review, recording platform) plus 2-3 episode-specific FAQs. Format `**Question?** Answer.` The host name is resolved into the FAQ references, never left as `{{HOST_NAME}}`.
- **Banned:** anything before `## Episode Overview` except the Google Doc cover page; anything after `## FAQ`; an Internal Setup block (ClickUp-only legacy, never in the Drive-native version).
- **Why:** the attorney reads this the night before recording; the locked structure is what makes it scannable and predictable.
- **Where it fires in the SOP:** `## Create -> ### Draft the guide sections`.

**Guideline 2 - Every element is a TRANSLATION of the Client ROS, never invented.**

- **Translation table:** segment titles -> Episode Plan outline sections; individual questions -> listed verbatim in the Segment Breakdown Questions (cleaned for client language); entity architecture -> omitted entirely; attorney response bullets -> pulled VERBATIM into the Segment Breakdown as indented sub-bullets under their parent question (the attorney needs the mandatory infill in their prep doc), pandoc `[entity]{.underline}` runs preserved; producer notes -> inspiration for the italic segment-goal paragraphs, never copied directly into the body; speaker tags + Entity Checklist -> omitted entirely; `{{PLACEHOLDERS}}` -> already populated in the source Client ROS, copy the populated values.
- **Exact-question rule:** USE the exact question text in the Segment Breakdown Questions list (cleaned - no producer notes, no entity bracketing, no inline annotations). Do NOT paraphrase questions into vague "topic areas" - the Pre-Interview Prep "Things to Think About" handles reflective framing; the Segment Breakdown lists the actual questions the attorney hears on air.
- **Attorney-bullet pull rule:** the attorney-response bullets sit under each parent question as indented sub-bullets, each line in the source ROS's `**Label:** detail` format. Pull them verbatim - same wording, same bolded lead, same pandoc `[entity]{.underline}` runs. The bullets are the attorney's coverage checklist for that question, not a paraphrase. If a bullet feels like production scaffolding the attorney would not need (rare - speaker tags or recording cues), drop that specific bullet and flag `> INFERRED: dropped bullet "{first 5 words}" - production scaffolding`; never drop them silently.
- **Banned:** pulling content from podcast-overview that the Client ROS does not ground; making the guide so vague it is useless ("we will discuss car accidents" is not a talking point - "California's pure comparative negligence system, how shared fault works, and the threshold that matters" is); paraphrasing attorney-response bullets into looser language at pull time (verbatim is the rule).
- **Why:** the guide is a translation, not original content; an invented element misleads the attorney about what the episode will actually cover.
- **Where it fires in the SOP:** `## Create -> ### Draft the guide sections`.

**Guideline 3 - The sensitive-data scrub, every guide must pass.**

- **Banned:** internal tool names (ClickUp, Fortress, Spanky, PM2, ChromaDB, the n-gram table, entity architecture); internal team names (use "your account manager", "your co-host", "our production team"); pricing, contract details, production metrics; entity architecture, vector strengths, SEO strategy language, n-gram targets; "Case Engine" internal process references; the phrase "Run of Show" or "ROS" (call it "episode outline" or "episode plan").
- **Allowed:** the attorney-facing topic areas, themes, talking points, and recording logistics - everything a client needs and nothing about how the sausage is made.
- **Why:** the client never sees the production machinery; a single internal-jargon leak breaks the prep doc's credibility as a clean client deliverable.
- **Where it fires in the SOP:** `## Create -> ### Run the sensitive-data scrub`, and the scrub check in `### Quality gates`.

**Guideline 4 - Attorney-facing tone.**

- **Allowed:** professional but warm - write like a producer briefing talent before a shoot; second-person ("your expertise", "your practice", "when you"); supportive, clear, practical.
- **Banned:** sales voice, marketing copy, internal process references.
- **Why:** the attorney reads this as their prep brief; the right tone makes them feel prepared, not sold to or processed.
- **Where it fires in the SOP:** `## Create -> ### Draft the guide sections`.

### Quality gates

Mechanical pass / fail conditions checked in `## Quality Assurance`.

- **Structure conformance** - the document is exactly `## Episode Overview` → `### Metadata` → `### Episode Plan` → `---` → `## Pre-Interview Prep` (Think About + Do) → `---` → `## Segment Breakdown` (italic intro + per-segment italic goal + Questions list, each Q carrying its attorney-response sub-bullets) → `---` → `## FAQ`. Nothing before `## Episode Overview` except the cover page; nothing after `## FAQ`.
- **Content gates** - Episode Overview opens with the value-prop to the attorney's business; Metadata block present (Episode Topic, Estimated Duration range, question + segment count); Episode Plan nested bullet list present; Things to Think About = 4-6 reflective prompts in `**Bold lead.** Detail.` format; Things to Do = 4-6 actionable items in the same format, including "Have your contact information ready"; Segment Breakdown has an italic intro line + per-segment italic goal paragraph + a Questions list where each `- Q{N}: ...` parent bullet is followed by the attorney-response bullets from the Client ROS as indented `  - **Label:** detail` sub-bullets (3-6 sub-bullets per Q typically); FAQ has 5 seed + 2-3 episode-specific; the host name is resolved in the FAQ.
- **Question verbatim** - the Segment Breakdown lists the actual questions from the Client ROS verbatim (cleaned for client language), not paraphrased into vague "topic areas".
- **Sequential numbering** - the guide inherits the Client ROS question numbering; the Segment Breakdown `- Q{N}: ...` labels MUST run sequential 1..N with NO gaps and NO number exceeding the question count (a 20-question guide ends at Q20, never Q30). Grep the `Q{N}:` labels and assert the sequence is exactly 1,2,3,...,N. If gappy or out of range (e.g., Q1-10, 12, 14, 15, 16, 17, 21, 22, 24, 25, 30 - the Sutliff E8 failure: 20 questions but numbered up to Q30), the upstream n-gram bank numbers leaked through the ROS into the guide and this gate FAILS - the source Client ROS must carry clean sequential numbering before the guide ships. Do not ship a gappy guide; route back through `/pod-3B-client-ros` -> `/pod-3A-ros-template` (the lock point) to renumber. Any FAQ / episode-plan question cross-references must use the same sequential numbers.
- **Attorney-bullet verbatim** - every attorney-response sub-bullet under each Q matches the source Client ROS bullet line-for-line (same `**Label:** detail` format, same pandoc `[entity]{.underline}` runs in the DOCX); zero paraphrase, zero drop without an `> INFERRED:` flag.
- **Source traceability** - every element traces back to the Client ROS; nothing invented, nothing pulled from podcast-overview that the ROS does not ground.
- **Sensitive-data scrub** - zero internal jargon (no "Run of Show", "ROS", "n-gram", "entity architecture", internal tool names, pricing / contract / production metrics); no Internal Setup block; no Entity Checklist table; no Producer Notes; no speaker tags.
- **Branded render** - the Google Doc was built from `build-client-guide-docx.py` (cover page, logo, Roboto body). The cover renders, in order: "Client Guide" title; the EPISODE TITLE as the prominent subtitle (MANDATORY - the gate FAILS if the cover has no episode title); the CLIENT/FIRM NAME as a secondary line; the "{Practice Area} | Location - {Location}" line; "Prepared by Case Engine" + date. Zero leaked pandoc inline-attribute markup as visible text (`[...]{.underline}`, `<u>`, `</u>`, `{.underline}`, `{.smallcaps}`, `{.mark}` - the build script strips any that snuck in from a copied ROS snippet).
- **Schema validate** - `client-guide-data.json` validates against `references/schema/client-guide.json`.
- **Provenance present** - `metadata.json` carries the provenance block (see `## INTERNAL`).
- **Artifacts present** - markdown, JSON, metadata all written; branded Google Doc exists; filename follows the canonical pattern.
- **Doc name carries the episode title** - the rendered Google Doc NAME (and the `.md` filename) must follow the canonical pattern `E{N}: {Episode Title} // {Firm Name} // Client Guide - {Location}` and MUST contain the actual episode title. FAIL on a firm-only name like `E8: Sutliff & Stout; Client Guide` (episode title missing) or any name that omits the ` // {Episode Title} // ` segment. Grep the resolved Drive doc name and the local `.md` filename and assert the episode title substring is present before shipping; if absent, rename via `files.update` (Drive) and re-emit the local mirror with the correct name - do not ship a firm-only name.
- **No em dashes** - plain hyphens only anywhere in the output.

### Gotchas

Failure modes that are warnings, not enforceable rules.

- **The Client ROS is the only source.** Do not pull content from podcast-overview that the Client ROS does not ground - the overview is supplemental context only (recording logistics, show format).
- **Anchor scope != per-episode target.** The show can be optimized for a broad **Optimization scope (show anchor)** - City / State / County / Regional - while each episode has its own **Episode geo target**, the specific city that episode is built to rank for. The guide inherits the episode's geo framing from the Client ROS: the Episode Overview names that episode's target city under the show's anchor, and never flattens every episode to one city. City emphasis in the copy is a ceiling, never a forced quota (see the no-city-quota rule) - getting this wrong is how a multi-location statewide firm ends up with guides that all sound like one city, or how city emphasis silently becomes a city floor.
- **DO copy attorney response bullets verbatim** as indented sub-bullets under their parent question in the Segment Breakdown. They are the attorney's coverage checklist - the mandatory infill they need in front of them at the table. Preserve the `**Label:** detail` format and the pandoc `[entity]{.underline}` runs. The ONLY rare exception is a bullet that is pure recording-cue / speaker-tag scaffolding (almost never happens since the Client ROS already pre-strips those) - drop it and flag with `> INFERRED:` rather than silently.
- **Do not include the Entity Checklist, entity-density targets, n-gram tables, or any SEO / production metrics.** The attorney has no idea these exist.
- **Do not use "Run of Show" or "ROS" in the body.** Call it "episode outline" or "episode plan".
- **Do not make the guide so vague it is useless.** A talking point names the specific concept; "we will discuss car accidents" does not.
- **Do not include an Internal Setup block.** That is ClickUp-only legacy from the local producer skill. The Drive-native guide starts with `## Episode Overview`.
- **Branded output is mandatory.** Do NOT upload the raw `.md` with `convert=true` - Google's markdown import has no cover page and would leak any pandoc span that snuck in from a copied ROS snippet. The pipeline is `markdown → build-client-guide-docx.py → DOCX → Drive upload as gdoc mimeType → clean branded Google Doc`.

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
The pre-flight phase - reads the iteration log, orients to the right episode folder, verifies the upstream Client ROS exists, and decides whether this run creates a new Client Guide or updates an existing one.

### Orient

What is?
The orientation step - read the iteration log, resolve the firm and episode folders, and load the podcast architecture context before producing anything.

- **Read the iteration log.** Read `references/iteration-log.json`, filter to entries with `status: open` or `status: in-progress`, surface them to the agent as known issues to watch for this run.
- Find `{Firm} Podcast/` in the shared Drive (fuzzy match if needed). If `podcast-overview.md` is reachable, read it and auto-fill Greeting questions 1-3; confirm in one line. Otherwise ask the Greeting questions.
- Navigate to the cell's parent episode folder `Episodes/EP{N}: {episode_name} // {client_name}/`. Find or create the `Client Guide: {episode_name} // {client_name}/` slot directly inside it. Detect a legacy episode per the rule in `### Outputs -> #### Drive destination` and follow legacy paths for that episode only.
- Read `references/examples/client-guide-examples.md` and pick 1-2 examples matching the requested scope as quality anchors. If the file is empty, proceed on methodology alone and flag `"references": "empty"` in `metadata.json`.

### Verify upstream Client ROS

What is?
The hard-dependency gate - confirm the completed Client ROS exists in the cell's `Client ROS:` slot before any guide is drafted.

- **Episode 1 / Founder Story exception (check FIRST):** if the episode is Episode 1 (Founder Story), there is no Client ROS dependency - the Client Guide is the hardcoded master template at `templates [master]/AEO Templates/Podcast/Episode Templates/Founder Story/`. Duplicate that template and populate the firm's tokens; skip the Client-ROS slot resolution and routing below.
- Resolve the Client ROS (`E{N}: ... // Client ROS - {Location}.md` + `client-ros-data.json`) from the cell's `Run of Show: ... /Client ROS:` slot.
- If the Client ROS is NOT in the expected slot, STOP and route the user to `/pod-3B-client-ros` to build it first. Do not fall back to anything.
- **Handoff Contract check.** Verify the Client ROS declares the expected shape (metadata block, segments, Questions). If the format is legacy, flag it and proceed with a best-effort translation. If any other upstream file shows up that is not declared in the Inputs contract, STOP and ask: "I see upstream output at {path} but my Inputs contract doesn't declare it. Should I (a) mine it with my best guess, (b) skip it, or (c) pause while you update the handoff contract?" Do not guess silently.

### Existence check

What is?
The mode router - decide whether this run creates a new Client Guide or updates an existing one based on whether the resolved `Client Guide:` slot already has content.

- Look for a `Client Guide` Google Doc + `client-guide-data.json` inside the resolved `Client Guide:` slot.
- **Missing:** no prior artifact - route to `## Create`.
- **Found:** surface provenance (existing `metadata.json` run date) and ask: refresh in place / archive-and-rebuild / cancel.
  - Refresh in place -> route to `## Update`.
  - `archive-and-rebuild` (or the refresh flag passed at invocation) -> move ONLY the prior Client Guide file (and its paired Doc) to `_archive-{YYYY-MM-DD}/` and route to `## Create`. The ROS Template and Client ROS siblings are left untouched.

## Prepare Inputs

What is?
The input-preparation phase - load and parse the Client ROS into segments / questions / metadata, load the podcast-overview context, and resolve branding into a working set ready for the Create or Update phase.

Work through the input sources in priority order; on a tool error, skip that source and degrade to the next.

- **Load the Client ROS.** Read `client-ros.md` + `client-ros-data.json` from the `Client ROS:` slot resolved in Checks. Extract segments, segment titles, durations, questions, and metadata.
- **Load podcast-overview.** Parse `podcast-overview.md` when present - for show framing, recording platform, and host voice. It is supplemental only - every guide element must still trace to the Client ROS.
- **Resolve firm metadata.** Collect the firm's websites and brand name directly from the user, or from the podcast-overview doc when present, to populate the FAQ and branding hints.
- **Resolve branding.** Read the Case Engine Branding folder (id `1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo`) - logo, colors, fonts, the Cover Page Spec. Hold the resolved values for the `## Ship` build. A per-client `brand.json` typography block overrides the CE default when present.
- **Load calibration examples.** Hold the 1-2 scope-matched examples from `references/examples/client-guide-examples.md` as quality anchors for the Create phase.

## Create

What is?
The create branch - drafts the attorney-facing Client Guide from the Client ROS in the locked canonical structure, runs the sensitive-data scrub, and produces a schema-valid `client-guide-data.json` plus its markdown source and metadata.

**Best Practices.**
These apply to the entire create phase and should be checked after each step.

- Translate the Client ROS - never invent content the ROS does not ground (see `### Editorial Guidelines -> Guideline 2`).
- Hold the scope-matched calibration examples in view while drafting - calibrate value-prop framing, prompt specificity, and verbatim-question handling against them.
- The canonical structure, tone, and scrub rules follow `### Quality bar` and `### Editorial Guidelines` - do not restate the thresholds, apply them.

If the model generates output that violates any of these, emit a `> NEEDS VERIFICATION:` block at the offending location instead of shipping the claim.

### Draft the guide sections

What is?
The pass that writes the four canonical sections - Episode Overview, Pre-Interview Prep, Segment Breakdown, FAQ - in the locked order, translating the Client ROS into attorney-facing language.

- **Episode Overview** - lead with the value proposition to the attorney's business per Editorial Guideline 1, then the Metadata block, then the Episode Plan outline.
- **Pre-Interview Prep** - 4-6 "Things to Think About" reflective prompts + 4-6 "Things to Do" actionable items, always including "Have your contact information ready". Every bullet uses the `**Bold lead.** Detail.` format.
- **Segment Breakdown** - the italic intro paragraph, then per segment an italic goal paragraph + a Questions list. The Questions list carries the exact questions from the Client ROS verbatim, cleaned for client language (the parent bullet line is the client-facing question text only - producer notes / inline entity-name annotations dropped). Under each `- Q{N}: ...` parent bullet, render the attorney-response bullets from the source Client ROS as indented sub-bullets verbatim (same `**Label:** detail` format, pandoc `[entity]{.underline}` runs preserved for the DOCX) per the Attorney-bullet pull rule in Editorial Guideline 2.
- **FAQ** - the 5 seed FAQs + 2-3 episode-specific FAQs, the host name resolved into the references.
- Apply the attorney-facing tone per Editorial Guideline 4 throughout.

### Run the sensitive-data scrub

What is?
The pass that catches internal jargon - grep the drafted guide for internal tool names, the "Run of Show" phrase, entity-architecture language, and production metrics, and remove every hit.

- Run the sensitive-data scrub per Editorial Guideline 3 - grep for internal tool names, "Run of Show" / "ROS", "n-gram", "entity architecture", "vector strength", pricing / contract / production metrics, and any "Case Engine" internal process reference.
- Remove every hit. Confirm no Internal Setup block, no Entity Checklist table, no Producer Notes, no speaker tags slipped in.
- Record the scrub result (clean / flagged + what was removed) for `metadata.json`.

### Render markdown and payload

What is?
The pass that assembles the final artifacts - the Client Guide `.md` source-of-truth with the `## INTERNAL` block, the `client-guide-data.json` machine-readable payload, and `metadata.json`.

- Assemble the Client Guide `.md` in the locked canonical structure per Editorial Guideline 1, then the `## INTERNAL` block (see `## INTERNAL`).
- Serialize `client-guide-data.json` per `### Outputs -> #### Schema` - the four sections, segments, questions, episode metadata.
- Write `metadata.json` with the provenance block per `## INTERNAL` - source Client ROS path, run date, scrub result, references status.

## Update

What is?
The update path - modifies an existing Client Guide in place when a prior version exists, preserving any manual edits the producer made since the last skill run.

**Best Practices.**
These apply to the entire update phase and should be checked after each step.

- **Diff before write.** Pull the existing `client-guide-data.json` + Client Guide `.md`, compare against the proposed new state, surface every changed section before committing the write.
- **Preserve manual edits.** Any prompt, FAQ answer, segment-goal paragraph, or question line that was manually edited since the last skill run keeps its current value. The skill never auto-overwrites a manual edit silently.
- **Flag merge conflicts inline.** When a new auto-generated value disagrees with a preserved manual edit, emit `> NEEDS VERIFICATION: auto-generated value [X] conflicts with manual edit [Y]` at the location; the producer resolves.
- **Stable fileId.** Update uses `files.update` against the existing `Client Guide` Google Doc fileId. Never create a new Doc; never delete-and-recreate. URL stability is part of the Update contract.

If the model proposes overwriting a manual edit without flagging it, halt and emit `> NEEDS VERIFICATION:` instead of shipping the change.

### Diff against existing

What is?
The pass that loads the prior Client Guide and computes a section-level diff against the proposed new state so nothing changes silently.

- Read the prior `client-guide-data.json`, Client Guide `.md`, and `metadata.json` from the resolved `Client Guide:` slot.
- Read the prior `metadata.json` provenance block to recover the last run's source Client ROS path and scrub result.
- Run the Create-phase passes (`### Draft the guide sections` through `### Run the sensitive-data scrub`) to compute the proposed new state.
- Compute the diff: sections changed, prompts added / removed / changed, questions changed, FAQs changed, and pieces untouched.

### Merge and resolve conflicts

What is?
The pass that merges the new draft into the existing Client Guide - new content in, stale content out, manual edits preserved, conflicts flagged for the producer.

- Apply the phase-level Best Practices: preserve every manually-edited piece; merge new auto-generated sections; drop content the new Client ROS retired.
- Where a new auto-generated value disagrees with a preserved manual edit, emit the `> NEEDS VERIFICATION:` conflict block inline; do not auto-resolve.
- Re-render the Client Guide `.md`, `client-guide-data.json`, and `metadata.json` per `### Render markdown and payload`. Bump the `metadata.json` run date and append the run to the provenance history.
- The shared `## Quality Assurance` phase runs after this phase - QA does not re-run inside Update.

## Quality Assurance

What is?
The gate before `## Ship` - a three-tier check (Best Practices by name, the hardwired Anti-AI Detection two-pass scan, then skill-specific mechanical checks) that runs after whichever branch fired (`## Create` or `## Update`).

**First - check against Best Practices.** The deliverable must align with the contract defined upstream in this file. This is always the first gate; skill-specific checks come after.

- **Quality bar** (Best Practices -> Quality bar) - the locked four-section structure, value-prop lead, verbatim questions, source traceability, zero internal jargon, branded Google Doc, no em dashes / banned vocabulary.
- **Sourcing discipline** (Best Practices -> Sourcing discipline) - every guide element Confirmed against the Client ROS; any Inferred phrasing flagged `> INFERRED:`; any ungrounded element flagged `> NEEDS CONFIRMATION:`. No silent synthesis.
- **Editorial Guidelines** (Best Practices -> Editorial Guidelines) - Guideline 1 (locked canonical structure), Guideline 2 (translation of the Client ROS, verbatim questions), Guideline 3 (sensitive-data scrub), Guideline 4 (attorney-facing tone).
- **Quality gates** (Best Practices -> Quality gates) - full checklist must pass: structure conformance, content gates, question verbatim, source traceability, sensitive-data scrub, branded render, schema validate, provenance present, artifacts present, no em dashes.

**Second - Anti-AI Detection two-pass scan** (canonical doc: https://docs.google.com/document/d/1hp7bxOFRlMhCuhjHNY0j05JrB97-KOFD0XUCQM3gMBU/edit). Mandatory for every text-producing skill. Run the full Section 7 two-pass audit against the deliverable:

- **Pass 1 (mechanical scan):** em-dashes, banned vocabulary (Section 2), banned phrases (Section 3), triadic rhythms and symmetric paragraphs (Section 4), summary-only section closers, date formatting per destination, specific-claims-trace-to-source, no emojis (unless requested), no clickbait.
- **Pass 2 (skeptical re-read):** restart from the top. Did I actually check every line, or skim? Em-dashes I missed? Banned phrases I rationalized? Triadic rhythms left because they "sounded fine"? Vague talking points that should be specific? Am I sure?
- **On any hit:** fix and re-run Pass 2 until clean. One pass is not enough.

**Third - skill-specific mechanical checks.**

- `client-guide-data.json` validates against the canonical schema `references/schema/client-guide.json`. If the schema file is absent, log `schema_status: missing` in `metadata.json` and proceed.
- Document structure is exactly `## Episode Overview` → `### Metadata` → `### Episode Plan` → `---` → `## Pre-Interview Prep` (Think About + Do) → `---` → `## Segment Breakdown` (italic intro + per-segment italic goal + Questions list with attorney-response sub-bullets under each Q) → `---` → `## FAQ`. Nothing before `## Episode Overview` except the cover page; nothing after `## FAQ`.
- Episode Overview opens with the value-prop to the attorney's business. Things to Think About = 4-6 reflective prompts in `**Bold lead.** Detail.` format; Things to Do = 4-6 actionable items in the same format, including "Have your contact information ready". FAQ has 5 seed + 2-3 episode-specific; the host name is resolved (no raw `{{HOST_NAME}}`).
- Segment Breakdown lists the actual questions from the Client ROS verbatim (cleaned), not paraphrased into vague "topic areas". Every Q parent bullet is followed by its attorney-response sub-bullets pulled verbatim from the Client ROS (3-6 sub-bullets typical, each in `**Label:** detail` format, pandoc `[entity]{.underline}` runs preserved in the DOCX).
- Every element traces back to the source Client ROS - nothing invented, nothing pulled from podcast-overview that the ROS does not ground.
- Sensitive-data scrub: zero internal tool names (ClickUp, Fortress, Spanky, PM2, ChromaDB), zero "Run of Show" / "ROS" / "n-gram" / "entity architecture" / "vector strength", zero pricing / contract / production metrics, no Internal Setup block, no Entity Checklist table, no Producer Notes, no speaker tags.
- Zero leaked pandoc inline-attribute markup as visible text in the rendered Doc (`[...]{.underline}`, `<u>`, `</u>`, `{.underline}`, `{.smallcaps}`, `{.mark}`).
- The branded Google Doc was built from `build-client-guide-docx.py` - cover page, CE logo, "Client Guide" title, the EPISODE TITLE as the prominent subtitle (MANDATORY - fail if absent), the CLIENT/FIRM NAME as a secondary cover line, the "{Practice Area} | Location - {Location}" line, "Prepared by Case Engine" + date, Roboto body.
- `metadata.json` provenance block present with at minimum: `run_date`, the source Client ROS path, `scrub_result` (clean / flagged), `references_status`, the podcast-overview / user-supplied sources used.
- Filename AND the rendered Google Doc name follow the canonical pattern `E{N}: {Episode Title} // {Firm Name} // Client Guide - {Location}` (append ` (Extension)` for extension cells), and MUST contain the actual episode title. FAIL on a firm-only name like `E8: Sutliff & Stout; Client Guide` (missing episode title). Assert the episode-title substring is present in both the Drive doc name and the local `.md` filename before shipping.
- Both write destinations verified: confirm the Drive `Client Guide:` slot AND the local mirror contain the same artifacts (markdown, `.docx` locally + Google Doc remotely, JSON, metadata).
- INTERNAL section grep test: `grep -L "## INTERNAL" {client-facing-export}` returns zero hits for the client-facing Google Doc.

**On failure:** fix the markdown, regenerate `client-guide-data.json` and `metadata.json`, rebuild the DOCX, re-upload via `files.update`, re-run all checks. Do not proceed to `## Ship` until QA returns clean.

## Ship

What is?
The publish phase - builds the CE-branded DOCX, writes the trio plus `metadata.json` to the firm's `Client Guide:` slot per Map 6, and mirrors the same artifacts to the local Desktop path.

### What ships

- **Client Guide** - Google Doc - human-facing CE-branded view, cover page, Roboto typeface, stable fileId.
- **Client Guide `.md`** - Markdown - raw markdown deliverable, retains the `## INTERNAL` block.
- **`client-guide-data.json`** - JSON - machine-readable payload.
- **`metadata.json`** - JSON (internal) - provenance: source Client ROS path, run date, scrub result.

### Where it ships

- **Drive:** the cell's `Client Guide:` slot per Map 6 - `Episodes/EP{N}: {episode_name} // {client_name}/Client Guide: {episode_name} // {client_name}/` (directly inside the episode parent, NOT nested inside `Run of Show:`). This destination is fixed - the skill does not move existing Drive data.
- **Local mirror:** `~/Desktop/claude_code/deliverables/podcast/Client Guide/{Topic}/{Episode}/{scope}/` - written every run.
- **Schema:** `~/.claude/skills/pod-3C-client-guide/references/schema/client-guide.json`.

### How it ships

Write to both destinations. On a write error to one, ship to the other and report the partial state.

- **Build the CE-branded DOCX.** The human-facing Google Doc MUST be the branded DOCX→Doc, never a raw markdown→Doc upload (the latter has no cover page and would leak any pandoc span that snuck in from a copied ROS snippet). Run `scripts/build-client-guide-docx.py` to emit both the `.docx` and the paired `.md` in one pass. The script renders Episode Overview → Pre-Interview Prep → Segment Breakdown → FAQ in canonical order, strips any pandoc inline markers (`[text]{.underline}`, `{.smallcaps}`, `{.mark}`, `{.color=...}`) from the input data, applies CE branding per the Case Engine Branding folder (Roboto throughout - if the branding folder still says Calibri, Roboto wins), and never emits an Internal Setup section.
- **Cover page.** Render per the canonical [Cover Page Spec](https://docs.google.com/document/d/1oydpI055jbj1FYDGeZfHQeMNjaWKUCFVGCRveeuJJCk/edit), with one override - the body and cover-page font is Roboto. Render in this exact order, top to bottom:
  1. **Title** `Client Guide` (CE Blue, 36pt, bold, Roboto).
  2. **Subtitle (MANDATORY) - the EPISODE TITLE** (e.g., `How to File a Car Accident Claim`), rendered as the prominent subtitle (22pt, bold, dark). The episode title is required - a cover that omits it FAILS the branded-render gate. This is the most prominent line after the title.
  3. **Secondary line - the CLIENT / FIRM NAME** (e.g., `Sutliff & Stout`), kept on the cover (16pt, bold, dark). This AMENDS the prior "firm not on cover" rule: both the episode title and the firm name are visible on the cover.
  4. **Practice area + location line** `{Practice Area}  |  Location - {Location}` (14pt, dark). At Topic Only scope drop the ` Location - {Location}` suffix.
  5. **`Prepared by Case Engine`** (11pt, italic, gray) + the run date below it (11pt, gray).
  Footer `Case Engine  |  Confidential  |  Page {PAGE}` auto-applied via the Drive API template.
- **Canonical styling** - Title styled as Google Docs "Title" (36pt, bold, dark #0f172a, Roboto); H2 as "Heading 1" (16pt, bold, CE Blue #3573FF, Roboto); H3 as "Heading 2" (13pt, bold, dark, Roboto); H4 as "Heading 3" (11pt, bold, dark, Roboto); body Roboto 11pt dark.
- **Drive write.** Upload the `.docx` as `application/vnd.google-apps.document` so Drive auto-converts it to a clean branded Google Doc (the human-facing artifact). Upload the `.md` as `text/markdown` (no conversion - raw deliverable). Upload `client-guide-data.json` + `metadata.json` as-is. First-time create uses `files.create`; subsequent writes use `files.update` against the existing fileId (preserves the URL). Never re-upload the `.md` with `convert=true` to make a second Google Doc - that is the leaky path.
- **Roboto pass.** After the base Doc is uploaded, confirm Roboto over the full document range. Override only when a per-client `brand.json` typography block specifies otherwise.
- **Archive.** If the existence check moved a prior Client Guide file to `_archive-{YYYY-MM-DD}/`, the archive folder ships alongside the new artifacts. Archive ONLY the prior Client Guide file - the ROS Template and Client ROS siblings are untouched.
- **Local mirror write.** Write the same Client Guide `.md`, the CE-branded `.docx`, `client-guide-data.json`, and `metadata.json` to the local mirror path. The mirror keeps the DOCX, not the auto-converted Google Doc. If the Drive write fails but the local write succeeds, surface the partial state in the report - do not silently swallow it.
- **Report back:**

  ```
  Done. Client Guide built for {Firm} - {Episode} ({Location}).

   Folder: https://drive.google.com/drive/folders/{folder_id}
   Client Guide (branded Google Doc): https://docs.google.com/document/d/{doc_id}

  Sensitive-data scrub: {clean / flagged}. FAQ count: {N}. QA gate: PASS.

  Next: AM reviews and sends this guide to {Attorney} 48-72 hours before recording. This is the final pre-recording step.
  ```

### Who to Notify

`notify: []` - this skill posts no notifications. The producer is informed via the inline report-back above.

---

## INTERNAL (not for client distribution - auto-stripped from all exports; the worked examples ride into the local markdown only, never into the Drive Doc)

### Provenance block

`metadata.json` must include a provenance block with at minimum: `run_date`, the source `client_ros_source` path, `podcast_overview` (found / not_found), `clients_row` (found / not_found), `koray_rag` (used / unreachable / not-consulted), `scrub_result` (clean / flagged), `references_status` (used / empty), `schema_status` (validated / missing), and the Drive fileIds captured during upload.

### Source inventory

Records every input the run consumed: the resolved Client ROS path, the `podcast-overview.md` path when used, the user-supplied firm data, and the calibration examples used (bundled file or methodology fallback).

---

## Learning & Iteration

- [ ] After each run, note edge cases, sensitive-data-scrub flags, vague-talking-point catches, and translation-fidelity issues; append GOOD / BAD / EDGE CASE entries to `references/examples/client-guide-examples.md`.
- [ ] Track recurring scrub flags - if the same internal-jargon leak keeps surfacing, tighten the `### Draft the guide sections` guidance.
- [ ] Watch for Client Guides paraphrasing questions into vague topic areas; if it recurs, reinforce the exact-question rule.

## Change Log

| Date | Change |
|---|---|
| 2026-07-10 | **v3.2.1 - three-field geo model terminology alignment (Gabe directive, Whalen scoping).** Adopted the canonical three-field geo model - **Targeting strategy** (single-location vs multi-location), **Optimization scope (show anchor)** (City / State / County / Regional), **Episode geo target** (the specific city each episode is built to rank for) - stamped identically across all pod skills. Relabeled Greeting Q2 "Podcast anchor scope" -> "Optimization scope (show anchor)"; sharpened Q3/Q4/Q5 to name Episode geo target + Targeting strategy; updated Inputs Optional ("Podcast series anchor scope" -> "Optimization scope (show anchor)", clarified Episode scope carries the inherited Episode geo target); relabeled the podcast-overview auto-read fields. Added the **"anchor scope != per-episode target"** rule to Gotchas (the show anchors broad while each episode targets its own city; city emphasis is a ceiling, never a floor - preserves the no-city-quota principle). Schema `client-guide.json` bumped 1.1 -> 1.1.1: `scope` and `location` field descriptions clarified against the three-field model (no structural field change). This skill is downstream of the Client ROS, so the pass is terminology-only - the guide still inherits its geo framing verbatim from the ROS. Revert: restore the "anchor scope" labels in Greeting Q2 / Inputs Optional / auto-read, drop the Gotchas rule, revert schema descriptions. |
| 2026-06-17 | **Cover episode-title + firm-name fix; doc-name episode-title gate.** The rendered cover was doing the OPPOSITE of spec - showing the FIRM NAME as the subtitle with the practice area and NO episode title, and the Drive doc name omitted the episode title (e.g. `E8: Sutliff & Stout; Client Guide`). Fixed the cover spec to render, in order: title `Client Guide`; the EPISODE TITLE as the prominent subtitle (now MANDATORY); the CLIENT/FIRM NAME as a secondary line (kept - amends the old "firm not on cover" rule so both are visible); the `{Practice Area} | Location - {Location}` line; `Prepared by Case Engine` + date. Updated the Sections-INCLUDED cover bullet (~180), the Sections-INCLUDED list (~222), the Cover page Ship bullet (~531/562), and the branded-render Quality gate to require the episode title and the firm secondary line. Added a doc-name Quality gate: the rendered Google Doc NAME and the `.md` filename must follow `E{N}: {Episode Title} // {Firm Name} // Client Guide - {Location}` and contain the actual episode title - FAIL on a firm-only name. `build-client-guide-docx.py` cover renderer updated so subtitle = episode title and the firm renders as a secondary line (was emitting firm as subtitle, episode title omitted); added `--episode-title` arg. Roboto + CE branding unchanged. Revert: restore the firm-as-subtitle cover block in the script and the prior cover/render bullets + drop the doc-name gate. |
| 2026-06-17 | **Sequential numbering gate (Sutliff E8 gappy-numbering fix).** Added a Sequential numbering gate to `### Quality gates`: the Segment Breakdown `- Q{N}:` labels must run sequential 1..N with no gaps and no number exceeding the question count. The guide inherits its numbering from the Client ROS, so a gappy ROS (Sutliff E8: 20 questions labeled up to Q30 - the raw n-gram bank index leaked through) would carry the same "numbered weird" defect into the attorney-facing guide. The gate verifies clean 1..N before shipping and, on failure, routes back through `/pod-3B-client-ros` -> `/pod-3A-ros-template` (the lock point) to renumber rather than shipping a gappy guide. Added a cross-reference in Editorial Guideline 1 noting the `Q{N}` labels are clean sequential 1..N, never the n-gram bank index. Revert: remove the Sequential numbering gate bullet and the Guideline 1 cross-reference clause. |
| 2026-06-12 | **Targeting-strategy branch (multi-location Mini model).** Greeting Q3/Q5 resolve episode format from the client targeting strategy (single-location Full ~20q vs multi-location Mini 10-12q per city, no anchor). Guide structure/format and chain order UNCHANGED - the guide inherits question set verbatim from the Client ROS either way. Revert: restore Q3/Q5 wording. |
| 2026-04-20 | Initial cowork skill version. Split from the client-ros SKILL into a dedicated Run of Show step. Canonical structure derived from the local producer-create-podcast-client-guide skill + ClickUp-canonical client guides for The May Firm. ClickUp push path removed (Drive-native only). Internal Setup block removed (ClickUp-only legacy). |
| 2026-04-21 | DOCX layer reworked - client-facing artifacts render as branded Google Docs built from a CE-branded DOCX. Added `pod-` prefix for producer discoverability. |
| 2026-04-24 | Reverted `pod-` prefix across cowork skills. |
| 2026-05-12 | Branded DOCX→Doc made mandatory. Roboto replaces Calibri. Mandatory QA gate added to the SOP - markup cleanliness, stripped-structure conformance, no internal jargon, questions verbatim, no Internal Setup block, no Entity Checklist, branded-DOCX rendering. Drive destination updated to show the Client Guide landing alongside the ROS Template + Client ROS. |
| 2026-05-14 | **v2.0.0** - Renamed `pod-9-client-guide` -> `pod-9A-client-guide`. Merged cowork client-guide v1.0 (canonical content) with original local pod-9 (Mode A enrichments). Bundled scripts + schemas + examples + iteration-log moved into canonical layout. Canonical final-phase `## Quality Assurance` H2 added. |
| 2026-05-15 | Aligned Drive write path to Client Folder Structure v2.4.0 → Map 6 - writes the Client Guide into the cell's `Client Guide:` slot directly inside the episode parent, reads the Client ROS from the sibling `Run of Show: ... /Client ROS:` slot. Legacy compatibility paragraph added. |
| 2026-05-20 | **v3.0.0** - Full structural refactor to the canonical CE skill structure. Renamed `pod-9A-client-guide` -> `pod-3C-client-guide`; description, trigger, and all sibling refs repointed to the new pipeline codes (1A/1B/1C/2A/2B/4A/4B/4D). Removed the entire Mode A/B detection probe and all capability-probing apparatus - this skill runs locally in Claude Code, calls its tools directly, skips or fails on a tool error. Frontmatter completed (skill_kind, modes: multi, inputs, outputs, notify; version/date/owner moved to a metadata block). Best Practices restructured to the canonical contract H3s (Inputs / Outputs / Framing / Quality bar / Sourcing discipline / Editorial Guidelines / Quality gates / Gotchas / Iteration log); the canonical guide structure, translation table, sensitive-data scrub, and tone rules relocated into Editorial Guidelines and Quality gates. SOP rebuilt as H2 phase siblings (Checks / Prepare Inputs / Create / Update / Quality Assurance / Ship). The three overlapping QA blocks (in-SOP Step 12 gate + `## Quality gates` H2 + final `## Quality Assurance` H2) consolidated into one canonical three-tier `## Quality Assurance` phase with the hardwired Anti-AI Detection two-pass scan and the mandatory `**On failure:**` recovery line. Universal State Check logic moved into the Existence check + `## Update`. `## Workflow` demoted to `### Workflow` H3 carrying the unified 4-phase pipeline diagram. `## Output` folded into Best Practices Outputs. `## Push to Drive` renamed `## Ship` with the canonical H3 sub-structure. Mode A/B local-mirror writes made unconditional. `references/schemas/` normalized to `references/schema/`. Old `## Appendix`-style content moved to the `## INTERNAL` two-tier model. Owner Gabe Jordan. |
| 2026-05-26 | **v3.1.0** - Attorney response bullets from the Client ROS now appear as sub-bullets under each question in the Segment Breakdown section, giving the attorney the full mandatory infill as part of their prep. Previously the Client Guide only listed questions. Updates: Editorial Guideline 1 (Segment Breakdown structure now specifies indented sub-bullets per Q), Editorial Guideline 2 (translation table reversed - attorney bullets now PULLED verbatim instead of "never copied"; added Attorney-bullet pull rule with the rare-exception `> INFERRED:` flag path); Quality bar + Quality gates + final QA mechanical checks (added Attorney-bullet verbatim gate); Gotchas (reversed the "do not copy" line to "DO copy"); Sections INCLUDED list updated. Schema bumped to 1.1 with new per-question `attorney_response_bullets` array (label + detail). Build script gains a sub-bullet renderer that emits indented List Bullet 2 paragraphs in DOCX and `  - **Label:** detail` lines in the .md, with pandoc inline runs preserved in DOCX and stripped in .md per existing convention. Calibration example refactored to show the new format. Owner Gabe Jordan. |
| 2026-07-31 | v3.3.0 - removed the `pod-1-podcast-bible` dependency, all Fortress (`fortress-db` / `clients`) access, and the ClickUp CRM path ahead of the skill moving to an environment without CE infra. Firm metadata (brand name, aka, websites) for the FAQ + branding hints is now a required user input, auto-filled from the podcast-overview doc when present - no DB or CRM lookup. Stripped all podcast-bible references (Phase 1 box + note, prereq sentence, routing bullet), repointed the auto-read source / `mcp__fortress-db__query` tool / Resolve-firm-metadata SOP step / provenance block / source inventory to user input + podcast-overview, and removed the vestigial "no numbered lists in ClickUp" QA clause. Frontmatter input fortress-db-row -> user-supplied-firm-data. LEFT the "Fortress" and "ClickUp" entries in the client-facing banned-internal-terms scrub lists (they must keep blocking those words from leaking into attorney output). Historical iteration-log entries left intact (append-only). | Gabe Jordan |
