# Reference Examples - Client ROS

Read before generating. These calibrate what GOOD / BAD / EDGE CASE look like for this skill across two dimensions: **structure** (markdown source-of-truth shape - segments, questions with placeholders filled in for the specific firm) and **rendering** (CE-branded Google Doc / DOCX output).

## Files

| File | What it calibrates | Read when |
|---|---|---|
| [`good--spaulding-truck-accidents.docx`](good--spaulding-truck-accidents.docx) | **Rendered styling** - canonical CE-branded Client ROS export (Spaulding Injury Law, Atlanta Truck Accidents). Visual reference for the final Google Doc / DOCX (cover page, segment headings, Q&A formatting with attorney/firm/statute/highway underlines). | Before running, to set the visual bar. Open in Word / Google Docs to see fonts, spacing, segment dividers, underline rendering. |
| [`good--may-firm-ca-file-claim-v1.md`](good--may-firm-ca-file-claim-v1.md) | **Structure** - real California Car Accidents Client ROS for The May Firm. Pre-Show Checks → Segments S1-S4 with full per-question prompts and placeholders filled in (firm name, attorney name, California statutes, locations) → Outro → Post-Show Wrap-up. | Before generating, to set the content bar. Match the segment progression, prompt voice, placeholder-fill style, and pandoc underline usage for emphasis. |
| [`bonus--spaulding-trucking-company-liability-v1.md`](bonus--spaulding-trucking-company-liability-v1.md) | **Structure - bonus episode variant** - Spaulding Atlanta truck accidents bonus ROS. Demonstrates the bonus-episode shape (single deep-dive topic vs full 4-segment ROS) and heavy use of `[text]{.underline}` markup for legal references. | When building a bonus episode rather than a standard 4-segment ROS. Read alongside the .docx to see how underlined references render in CE branding. |

## How to use them together

- **Structure first** - read the `.md` files to understand segment progression, prompt voice, and how placeholders get filled in for a specific firm.
- **Styling second** - open the `.docx` to see how that structure renders: cover page, segment dividers, attorney/statute/location underlines.
- The skill produces a deliverable named `Client ROS - E{N} - {Episode Short Title} - {Location}.md` (matching the structure of the `.md` references) which is uploaded as raw markdown alongside the `.docx`/Google Doc sibling. Example: `Client ROS - E2 - How to File a Car Accident Claim - CA Santa Maria.md`. Generic names like `Client ROS.md` are NOT allowed — every episode would collide in any aggregated view (Drive search, recent files). The calibration anchors in this folder use a separate `good--{slug}.md` naming convention because they are repo-internal lookups, not client deliverables.

## Format - structural anchor (`.md`)

`.md` examples carry firm-specific filled-in content. Pandoc-style underlines (`[text]{.underline}`) are intentional in the `.md` source - they get stripped to plain text on `.md` upload but converted to proper underline runs in the `.docx` output. The build script handles both paths.

## Format - rendered anchor (`.docx`)

`.docx` files match the canonical [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) spec - cover page with logo, CE Blue (#3573FF) section headings, Calibri 11pt body, footer with `Case Engine | Confidential | Page {PAGE}`.

## Adding new examples

- Pair every example: a `.md` for structure + a `.docx` for rendering, when possible.
- Add one paired example per scope/episode-shape as the set grows.
- For BAD examples, capture real failure modes (off-brand renders, segment timing that doesn't add up, weak prompts, missing placeholders) and annotate `why_this_label` with the specific Quality gate that failed.

## Current GOOD examples

- **`good--spaulding-truck-accidents.docx`** - rendered Atlanta Truck Accidents Client ROS. Visual calibration anchor.
- **`good--may-firm-ca-file-claim-v1.md`** - California Car Accidents Client ROS structure. Standard 4-segment shape.
- **`bonus--spaulding-trucking-company-liability-v1.md`** - bonus-episode variant for deeper-dive topics.

## BAD examples

<!-- - [Short title](bad--slug.md) - what failed and why -->

## EDGE CASE examples

<!-- - [Short title](edge--slug.md) - when standard approach doesn't fit -->
