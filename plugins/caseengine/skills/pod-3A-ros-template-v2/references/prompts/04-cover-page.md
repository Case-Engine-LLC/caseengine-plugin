# 04 - Cover Page

> **References:** `references/cover-spec.json` is the format of record for this page - the block
> order, the colors, the sizes and the gates, as data, so the spec has exactly one home. It is read
> by `steps/03-cover-page.md` and by `scripts/build-ros-template-v2-docx.py`. Cross-check against the
> canonical [Cover Page Spec](https://docs.google.com/document/d/1oydpI055jbj1FYDGeZfHQeMNjaWKUCFVGCRveeuJJCk/edit)
> in the Case Engine Branding folder; where they disagree on typeface, Roboto wins. Read the JSON
> before touching anything here.

**Nothing on the cover is generated prose.** You are assembling known values, not writing. This file
exists to say which values and where they come from.

## Inputs
- Episode title - from the live Topic Plan Google Doc for this episode, not a local mirror
- The episode's topic phrase, for `{{TOPIC}}`
- The template's location scope, for `{{CITY}}`

## What is STATIC here (do not generate)
Everything, per `references/cover-spec.json -> blocks`:

- The CE logo, Drive id `1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2`, inserted inline at the SECOND
  paragraph, 180pt wide
- The title string `Run of Show`
- `Prepared by Case Engine`

## Render order
Read it from `references/cover-spec.json -> blocks`, not from a copy. As of spec version 2.1.0:

1. Spacer
2. Spacer, with the CE logo inserted inline here at 180pt
3. Spacer
4. `Run of Show` - CE Blue, 24pt, bold
5. `{episode_title}` - CE Dark, 18pt, bold
6. Spacer
7. `{{TOPIC}}  |  {{CITY}}` - CE Dark, 14pt, both tokens bold
8. Spacer
9. `Prepared by Case Engine` - CE Dark, 11pt
10. Page break, so `S1: Long-Form` begins on its own page

Roboto throughout, everything centered.

## Prompt

There is no generation step. Resolve the episode title from the live Topic Plan Doc, emit the blocks
in the order `cover-spec.json` gives them, and issue the logo insert.

**The cover line is `{{TOPIC}}  |  {{CITY}}`.** Two placeholders from the approved taxonomy, two
spaces on each side of the pipe, no labels. It replaced the labelled `Topic:` / `Location:` pair on
2026-08-17, and it does not carry the practice area or a scope string - `{{TOPIC}}` is the episode's
subject as a phrase and `{{CITY}}` is the city, both resolved downstream by `pod-3B-client-ros`.

**The logo insert is a SEPARATE API call issued after the text batch lands**, because the insertion
index is only known once the text exists. This is why it is the single most likely element to
silently go missing, and why the gate checks for the inline object rather than assuming it.

## Rules
- **Only approved tokens.** `{{TOPIC}}` and `{{CITY}}` are the two the cover carries, both from the
  eleven in `references/placeholders.md`. `{{PRACTICE_AREA}}` and `{{LOCATION}}` are not in the
  taxonomy and never were valid on the v2 cover.
- **The firm name NEVER appears on the cover**, and neither does the attorney's. The template is
  tokenized and brand-agnostic; firm identity is resolved downstream by `pod-3B-client-ros`.
- **No episode number.** `{{EPISODE_NUMBER}}` was retired from the rendered document on 2026-08-17.
  It stays valid for filenames only.
- **No recording date, in any form.** `{{RECORDING_DATE}}` was retired from the taxonomy on
  2026-08-18 and the cover carries neither the token nor a literal date. The template serves every
  firm that records this episode and they all record on different days, so a date here is wrong for
  everyone but one of them, and it dates an asset meant to stay evergreen. The recording date is a
  Client ROS field; `pod-3B-client-ros` collects it per firm.
- Roboto, centered, per the spec. No em dashes.

## Examples

### GOOD
> Run of Show
> **Why Truck Accident Cases Are Worth More Than Car Cases, and Harder to Win**
> **{{TOPIC}}**  |  **{{CITY}}**
> Prepared by Case Engine

Title verbatim, episode title from the live Doc, one tokenized line with two bold tokens and a plain
separator, and nothing after the attribution line.

### BAD
> Run of Show
> **Sutliff & Stout Podcast** - Episode 7
> Truck Accidents  |  GA - Savannah
> Prepared by Case Engine, 08-14-2026

Fails: a firm name on a tokenized template; an episode number where the title belongs; the cover line
hard-codes a practice area and a scope string instead of carrying `{{TOPIC}}` and `{{CITY}}`; and a
recording date on the cover at all, which the taxonomy retired on 2026-08-18.

## Gates
Gates for this page are the four in `references/cover-spec.json -> gates`, checked in
`steps/08-qa.md` tier 1. They supersede the old C-1 through C-5, which named a practice-area line
that the cover no longer carries.

- The logo inline object is present at 180pt.
- Title reads `Run of Show`, CE Blue, 24pt, bold.
- Episode title, the `{{TOPIC}}  |  {{CITY}}` line, and `Prepared by Case Engine` are all present
  and centered.
- The cover is page 1 and S1 starts on page 2.

## Feedback
- **Logo gate fails:** the insert call did not land, or ran before the text batch. Re-issue it
  against the index of the second paragraph. Do not accept the Doc without it; a coverless ROS reads
  as a draft.
- **Title or block gate fails:** re-emit from `references/cover-spec.json -> blocks`. Do not
  hand-patch a block - the spec has one home so the renderer and the QA gate cannot drift apart.
- **A firm, attorney or literal value reached the cover:** strip it and let `pod-3B-client-ros` add
  identity downstream. A hard-coded value here makes the template single-use.
- **Page-break gate fails:** the break after block 10 is missing or a section inherited one it did
  not ask for. Fix the break, not the section spacing.
