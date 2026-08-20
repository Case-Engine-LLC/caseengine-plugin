# Reference Examples - Client Guide

Read before generating. These calibrate what GOOD / BAD / EDGE CASE look like for this skill across two dimensions: **structure** (markdown source-of-truth shape - episode overview, prep sections, segment breakdown, FAQ) and **rendering** (CE-branded Google Doc / DOCX output).

## Files

| File | What it calibrates | Read when |
|---|---|---|
| [`good--client-guide-ca-car-accidents.docx`](good--client-guide-ca-car-accidents.docx) | **Rendered styling** - canonical CE-branded Client Guide export. Visual reference for the final Google Doc / DOCX (cover page, episode overview formatting, prep checklists, segment dividers, FAQ layout). Real production run for The May Firm, California Car Accidents. | Before running, to set the visual bar. Open in Word / Google Docs to see fonts, spacing, table formatting. |
| [`good--client-guide-ca-car-accidents.md`](good--client-guide-ca-car-accidents.md) | **Structure** - real California Car Accidents Client Guide. Episode Overview + Metadata + Episode Plan / Pre-Interview Prep (Things to Think About + Things to Do) / Segment Breakdown (Intro + S1-S4 + Outro) / FAQ. The structural anchor for what a city/state-anchor Client Guide looks like. | Before generating, to set the content bar. Match the section progression, prep checklist style, segment description voice, FAQ tone. |

## How to use them together

- **Structure first** - read the `.md` to understand the section progression and the voice of each section (especially the prep sections, which are the highest-leverage part for the attorney).
- **Styling second** - open the `.docx` to see how that structure renders in CE branding.
- The skill produces a deliverable named `Client Guide - E{N} - {Episode Short Title} - {Location}.md` (matching the structure of the `.md` reference). Example: `Client Guide - E2 - How to File a Car Accident Claim - CA.md`. The paired Google Doc (same name, no extension) is what the attorney reads. Generic names like `Client Guide.md` are NOT allowed — every episode would collide in any aggregated view (Drive search, recent files). The calibration anchors in this folder use a separate `good--{slug}.md` naming convention because they are repo-internal lookups, not client deliverables.

## Internal Setup section - removed by design

**The Internal Setup checklist** (cover photo upload, font sizing, share-settings checklist, "delete this section before publishing") that exists in legacy production runs has been **stripped from the canonical example MD** and should be **stripped from any future production runs by the build script**. The new pipeline configures the deliverable correctly from the jump - no manual cleanup steps before sharing.

If you're authoring a build script for this skill (Phase 1 work), the script must:

1. **Never emit the Internal Setup section.** It was a manual workflow workaround; the new pipeline does it correctly automatically.
2. **Strip pandoc-style markup artifacts.** Underline syntax like `[Michael Grife]{.underline}` and similar `{.smallcaps}` / `{.mark}` / `{.color}` tokens are pandoc DOCX→MD conversion artifacts. They render literally in Google Docs and look broken. The script should either:
   - Convert to proper DOCX underline (when emitting `.docx`)
   - Strip the wrapper and keep the inner text (when emitting `.md`)
3. **Match the canonical section order:** Episode Overview → Pre-Interview Prep → Segment Breakdown → FAQ (with Metadata + Episode Plan as sub-blocks of Episode Overview).
4. **Apply CE branding** per the canonical [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) folder (cover page, headers, footers, CE Blue H2s, Calibri body).

## Format - structural anchor (`.md`)

Every `.md` example carries a YAML frontmatter header (where present):

- `label:` GOOD / BAD / EDGE CASE
- `skill:` client-guide
- `run_date:` YYYY-MM-DD
- `firm:` law firm name
- `topic:` practice area + episode title
- `scope:` Topic Only / Location / Extension
- `location:` if applicable
- `source:` real client run, manufactured reference, or template seed
- `why_this_label:` multi-line explanation
- `known_flaws:` null if none, else specific issues the reader should see

The body is the verbatim Client Guide structure - prep, segment breakdown, FAQ.

## Format - rendered anchor (`.docx`)

`.docx` files match the canonical [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) spec - cover page with logo, CE Blue (#3573FF) section headings, Calibri 11pt body, footer with `Case Engine | Confidential | Page {PAGE}`.

When swapping in a new `.docx` reference, make sure it follows the canonical brand. Off-brand `.docx` examples poison the calibration.

## Adding new examples

- Pair every example: a `.md` for structure + a `.docx` for rendering, when possible.
- Add one paired example per scope as the set grows. Right now we have a CA state-level anchor; Topic Only / Extension references add later.
- For BAD examples, capture real failure modes and annotate `why_this_label` with the specific Quality gate that failed.

## Current GOOD examples

- **`good--client-guide-ca-car-accidents.docx`** - California Car Accidents Client Guide, rendered. Visual calibration anchor.
- **`good--client-guide-ca-car-accidents.md`** - same Client Guide, markdown source. Structural calibration anchor. Internal Setup section stripped.

## BAD examples

<!-- - [Short title](bad--slug.md) - what failed and why -->

## EDGE CASE examples

<!-- - [Short title](edge--slug.md) - when standard approach doesn't fit -->
