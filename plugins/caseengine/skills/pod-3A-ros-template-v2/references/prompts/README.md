# Section Prompts - pod-3A-ros-template-v2

The v2 ROS is generated **section by section**, not in one pass. Each file here is a live generation
prompt for one section.

**A prompt file defers to its reference doc; it does not restate it.** The reference docs in
`references/` are the format of record - they carry the shape, the reasoning and the gates. These
files carry only what a run needs at the moment it generates that section: what to resolve first,
what is constant, the render order, the instruction, the failure modes that bite most often, and a
GOOD / BAD pair. Where a prompt and its reference doc disagree, the reference doc wins and the prompt
is the thing to fix.

Each file carries the same blocks:

- **References** - the doc that governs this section. Read it first.
- **Inputs** - exactly what must be resolved before the section can be written.
- **What is STATIC here** - the constants that render verbatim. Do not regenerate them.
- **Render order** - the locked sequence. Downstream populate reads it positionally.
- **Prompt** - the instruction that generates the parts that actually vary.
- **Rules** - the constraints that break most often. The full set lives in the reference doc.
- **Examples** - one GOOD and one BAD.
- **Gates** - the reference doc's gate IDs. Mechanical pass/fail, no judgment calls.
- **Feedback** - what to do when a gate fails. Every gate has a repair instruction.

## The index

| # | File | Governed by |
|---|---|---|
| 01 | [`01-introduction.md`](01-introduction.md) | [`references/introduction.md`](../introduction.md), [`references/statics.json`](../statics.json) |
| 02 | [`02-attributes.md`](02-attributes.md) | [`references/attributes.md`](../attributes.md) |
| 03 | [`03-shortform-questions.md`](03-shortform-questions.md) | [`references/short-form.md`](../short-form.md) |
| 04 | [`04-cover-page.md`](04-cover-page.md) | [`references/cover-spec.json`](../cover-spec.json) |
| 05 | [`05-outro-close.md`](05-outro-close.md) | [`references/outro.md`](../outro.md), [`references/outro-banks.json`](../outro-banks.json) |

Cross-cutting, read by every section: [`references/document-structure.md`](../document-structure.md)
for the locked shape and the retired list, [`references/placeholders.md`](../placeholders.md) for the
eleven approved tokens, and [`references/editorial-rules.md`](../editorial-rules.md).

## How little is actually generated

**Three STATIC strings**, in `references/statics.json -> strings`: `welcome`, `welcome_first` and
That is the whole constant set (`outro_note` removed 2026-08-21). It was sixteen on 2026-08-14 and six on the morning of
2026-08-18; eleven strings were retired on 2026-08-17 and the outro's three spoken lines stopped
being constants on 2026-08-18. Everything retired is preserved in `statics.json -> retired` so a
future edit does not reintroduce one believing it was lost by accident.

The per-episode generated fields are:

- `topic_phrase` - feeds Introduction line 2 and the outro's topical credit approach
- `setup` - Introduction line 2, carried in the payload as `segment_1.setup`
- `credential` - Introduction line 3, its own paragraph, carried as `segment_1.credential`
- `prompt` - Introduction line 4, the one ask and the only bolded prompt in the document
- the attribute bullets - selected and transformed from the `pod-1D` catalog or the fallback
- the Short-Form question sets **and their bullets** - ten questions per location, two to four
  bullets under each
- the outro's **three spoken lines** - thanks, sign-off, reach-out

Everything else is one of the three constants, a speaker tag, or an n-gram row shipped verbatim in
the Appendix. If you find yourself writing prose that is not in that list, stop - that is drift, not
value.

## Execution order

Sections are generated in this order because each one constrains the next. Do not reorder.

| # | Section | Generates | Depends on |
|---|---|---|---|
| 01 | Introduction | `topic_phrase`, `setup`, the line 3 credential, `prompt` | research corpus, entity map, client profile, prior episodes' rotation record |
| 02 | Attributes | the ten to twelve attribute bullets | `pod-1D` artifact or the fallback snapshot; 01, whose credential frame seeds the block |
| 03 | Short-Form Questions | the question sets and their bullets | the live Topic Plan Doc, the n-gram bank, 02, entity map, keyword research |
| 04 | Cover Page | nothing - assembles known values | the live Topic Plan Doc, for the episode title |
| 05 | Outro | the three spoken lines | 01's `topic_phrase`, prior episodes' rotation record |

01 runs first because its credential frame is the attribute the attorney hits hardest, so it seeds
02. 03 draws on 02's attribute set. 05 runs last of the spoken sections so the read-through can hear
it against the Introduction, which is the only place cross-section repetition shows up.

## What changed

- **2026-08-18** - The Short-Form bullets came back, in the legacy `[{Label}]{.underline}: {detail}`
  form, at Gabe's direction. The question renders fully bold and the labels drop to underline.
  `welcome` shrank to line 1, so the Introduction's setup is a generated paragraph rather than half a
  frozen constant. The outro's three spoken lines became generated. S2's outro was removed - it was a
  renderer bug, not a format. Topic Plan reconciliation became a hard requirement with its own gate
  family, TP-1 through TP-6.
- **2026-08-17** - `02-move2-need-to-know.md` and `03-move3-examples.md` deleted along with the
  `Internal Notes (not read on air)` block they generated. The three moves, the need-to-know bullets
  and the Real examples line all died with it, and `need_to_know` and `examples` came off the
  generated-field allowlist. `attr_intro`, `attr_sources_internal`, the `Attributes to Hit` heading
  and the two short-form mode notes went with them. `{{HOST_NAME}}` was retired for `{{INTERVIEWER}}`,
  `{{PRACTICE_AREA}}` was retired from the body entirely, and `{{LOCATION}}` was replaced by `{{CITY}}`.
- **2026-08-14** - `01-cold-open.md` and `02-lead-in.md` merged into `01-introduction.md`.
  `07-interviewer-toolkit.md` and `09-producer-notes.md` deleted; that guidance is real and still
  applies, but it reaches people through `pod-3C-client-guide` rather than the recording script.
  Short-Form capped at ten questions per location.

## Global gates

Run by `steps/08-qa.md` across the whole document, after every section and again before Ship. The
authoritative list is in that step; these are the ones a section run can break on its own.

- **G-1 No em dashes.** `grep -c` for the em dash character returns 0.
- **G-2 Placeholders.** Every `{{...}}` is one of the **eleven** approved tokens in
  `references/placeholders.md`. Zero invented, zero `{{REGION}}`. Every token renders bold - and
  never wrapped in its own `**` markers inside an already-bold run, which nests bold and silently
  unbolds it.
- **G-3 Jargon containment is absolute.** Statute citations, case names, section symbols and element
  names return ZERO across the entire document above the Appendix heading. No exempt section.
  Pattern: `§|Section [0-9]| v\. |O\.C\.G\.A|CPRC|Cts\. & Jud|CACI`. The Appendix is scoped out
  because it carries n-gram rows verbatim and is never read on air - do not edit a bank row to make
  the scan pass.
- **G-4 No leaked markup.** Zero `{.underline}`, `<u>`, or literal `**` visible as text.
- **G-5 STATIC verbatim.** All **three** constants render byte-identical to
  `references/statics.json`. Nothing substitutes into any of them - `{topic_phrase}` moved out of
  `welcome` when it shrank to line 1.
- **G-6 Removed sections stay removed.** Zero occurrences of anything in
  `references/document-structure.md` -> "Retired - must not come back".
- **G-7 Anti-AI Detection two-pass scan** per the canonical doc, plus the read-through in
  `steps/08-qa.md` tier 4.

## Why gates and not judgment

The v1 format failed QA on things nobody could check mechanically - "sounds choppy", "too much
jargon". Every gate here is countable, so a run either passes or does not, and the failure names the
repair. The one deliberate exception is the tier 4 read-through, which exists because a generated
outro line once passed every mechanical gate and was still not a sentence anybody would say. Its
criteria are listed, which is what separates it from "sounds choppy". If a new failure mode shows up
that no gate catches, add the gate before shipping the fix.
