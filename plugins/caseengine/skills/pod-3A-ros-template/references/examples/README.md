# Reference Examples - ROS Template

Read before generating. These calibrate what GOOD / BAD / EDGE CASE look like for this skill across two dimensions: **structure** (markdown source-of-truth shape - segments, questions, timing) and **rendering** (CE-branded Google Doc / DOCX output).

## Files

| File | What it calibrates | Read when |
|---|---|---|
| [`good--ros-template-city.docx`](good--ros-template-city.docx) | **Rendered styling** - canonical CE-branded ROS Template export. Visual reference for the final Google Doc / DOCX (cover page, segment headings, Q&A formatting, producer notes, timing markers). | Before running, to set the visual bar. Open in Word / Google Docs to see fonts, spacing, segment dividers, table formatting. |
| [`good--ros-template-city.md`](good--ros-template-city.md) | **Structure** - real city-scope ROS for "How to File a Car Accident Claim in Savannah, Georgia". Segments S1-S4+ with per-segment timing, question-by-question prompts with target durations, Producer Notes header, Introduction segment. The structural anchor for what a city-anchor ROS looks like. | Before generating, to set the content bar. Match the segment progression, question count per segment, timing budgets, producer-note style. |

## How to use them together

- **Structure first** - read the `.md` to understand segment progression, how questions are framed, and how timing budgets ladder up to the total runtime.
- **Styling second** - open the `.docx` to see how that structure renders: cover page, segment dividers, question formatting, producer notes.
- The skill produces a deliverable named `ROS Template - {Episode Short Title} - {Location}.md` (matching the structure of the `.md` reference). Example: `ROS Template - How to File a Car Accident Claim - GA Savannah.md`. The paired Google Doc (same name, no extension) is what downstream `/client-ros` reads to populate. Generic names like `Run of Show.md` or `ROS Template.md` are NOT allowed — every episode/scope would collide in any aggregated view (Drive search, recent files). The calibration anchors in this folder use a separate `good--{slug}.md` naming convention because they are repo-internal lookups, not Drive deliverables.

## Format - structural anchor (`.md`)

Every `.md` example carries a YAML frontmatter header (where present):

- `label:` GOOD / BAD / EDGE CASE
- `skill:` ros-template
- `run_date:` YYYY-MM-DD
- `topic:` practice area + episode title
- `scope:` Topic Only / Location / Extension
- `location:` if applicable
- `source:` real client run, manufactured reference, or template seed
- `why_this_label:` multi-line explanation
- `known_flaws:` null if none, else specific issues the reader should see

The body is the verbatim ROS structure - segments, questions, timing, producer notes.

## Format - rendered anchor (`.docx`)

`.docx` files match the canonical [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) spec - cover page with logo, CE Blue (#3573FF) section headings, Calibri 11pt body, footer with `Case Engine | Confidential | Page {PAGE}`.

When swapping in a new `.docx` reference, make sure it follows the canonical brand. Off-brand `.docx` examples poison the calibration.

## Adding new examples

- Pair every example: a `.md` for structure + a `.docx` for rendering, when possible.
- Add one paired example per scope as the set grows. Right now we have a city-scope anchor; state-anchor and extension references add later when good production runs exist.
- For BAD examples, capture real failure modes (off-brand renders, segment timing that doesn't add up, weak questions, missing producer notes) and annotate `why_this_label` with the specific Quality gate that failed.

## Current GOOD examples

- **`good--ros-template-city.docx`** - city-anchor Run of Show, rendered. Visual calibration anchor.
- **`good--ros-template-city.md`** - same Savannah, GA car accidents ROS, markdown source. Structural calibration anchor.

## BAD examples

<!-- - [Short title](bad--slug.md) - what failed and why -->

## EDGE CASE examples

<!-- - [Short title](edge--slug.md) - when standard approach doesn't fit -->
