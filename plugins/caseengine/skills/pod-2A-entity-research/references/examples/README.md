# Reference Examples - Entity Research

Read before generating. These calibrate what GOOD / BAD / EDGE CASE look like for this skill across two dimensions: **structure** (markdown source-of-truth shape) and **rendering** (CE-branded Google Doc / DOCX output).

## Files

| File | What it calibrates | Read when |
|---|---|---|
| [`good--entity-map-car-accidents-topic-only.docx`](good--entity-map-car-accidents-topic-only.docx) | **Canonical rendered output** - produced by `scripts/build-entity-map-docx.py` from real Car Accidents Topic Only data. Cover page (CE-branded), header / footer, Executive Summary with auto-generated Learnings & Insights + plain-language What does this mean? subsection, embedded vector-space chart, tier tables (T1 + bridges bolded), Cluster Architecture, Bridge Entities, Localization Summary, Inheritance Notes. **This is the primary visual + structural anchor.** | Before running, to set BOTH the visual bar (CE branding, page layout) AND the content bar (section order, table columns, insights shape). |
| [`good--sutliff-stout-car-accidents-topic-level.md`](good--sutliff-stout-car-accidents-topic-level.md) | **Alternate structural anchor** - Topic-level Sutliff & Stout Car Accidents map. 45 entities / 11 clusters / 6 bridges, three-attribute Koray columns preserved alongside composite vector, 12+ entity types for breadth, bridges selected by connection count, pre-declared Inheritance Notes for sub-scope cascade. | Cross-reference for content depth and tier balance. The DOCX above is the primary anchor; this `.md` is a second data point. |
| [`good--example-entity-map-FL-car-accidents.docx`](good--example-entity-map-FL-car-accidents.docx) | **Pre-spec example** - earlier FL Car Accidents export, before the new CE-branded layout was locked in. Kept for historical reference only. **Do not use as a visual anchor** - it doesn't follow the canonical cover page / branding. | Reference only. Use the canonical DOCX above. |

## How to use them together

- **Structure first** - read the `.md` to understand what sections, tier tables, cluster definitions, and bridge callouts should be present and in what shape.
- **Styling second** - open the `.docx` to see how that structure renders: fonts, colors, cover page, footer, body highlights (Tier 1 bold, bridges glyphed), table formatting.
- The skill produces an `Entity Map.md` (matching the `.md` reference's structure) which auto-converts to a Google Doc on Drive upload (matching the `.docx` reference's visual shape).

## Format - structural anchor (`.md`)

Every `.md` example carries a YAML frontmatter header:

- `label:` GOOD / BAD / EDGE CASE
- `skill:` entity-research
- `run_date:` YYYY-MM-DD
- `topic:` practice area the map was built for
- `scope:` Topic Only / Location / Extension
- `location:` if applicable
- `source:` where the example came from (real client run, manufactured reference)
- `why_this_label:` multi-line explanation of what makes this example good / bad / edge
- `known_flaws:` null if none, else specific issues the reader should see

The body is the verbatim output from the run. JSON deliverables can include the JSON as a fenced code block inside the `.md` so one file covers both narrative + machine-readable shape.

## Format - rendered anchor (`.docx`)

`.docx` files match the canonical [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) spec - cover page with logo, CE Blue (#3573FF) H2s, Calibri 11pt body, footer with `Case Engine | Confidential | Page {PAGE}`.

When swapping in a new `.docx` reference, make sure it follows the canonical brand. Off-brand `.docx` examples poison the calibration.

## Adding new examples

- Pair every example: a `.md` for structure + a `.docx` for rendering, when possible.
- Add one paired example per scope as the set grows (Topic Only is foundational; Location and Extension references later when good production runs exist).
- For BAD examples, capture real failure modes (off-brand renders, missing tier balance, generic-token leak in localized scopes) and annotate `why_this_label` with the specific Quality gate that failed.

## Current GOOD examples

- **`good--example-entity-map-FL-car-accidents.docx`** - rendered FL Car Accidents entity map. Visual calibration anchor.
- **`good--sutliff-stout-car-accidents-topic-level.md`** - Sutliff & Stout Topic-level Car Accidents (`.md` source). Structural calibration anchor.

## BAD examples

<!-- - [Short title](bad--slug.md) - what failed and why -->

## EDGE CASE examples

<!-- - [Short title](edge--slug.md) - when standard approach doesn't fit -->
