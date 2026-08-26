# 03 - Short-Form Questions

> **References:** `references/short-form.md` is the format of record for this segment - the block
> shape, where the questions come from, how the ten are selected, the Topic Plan reconciliation
> requirement, the bullets, the geo rules, and gates SF-1 through SF-12 plus TP-1 through TP-6. Read
> it before touching anything here. This file carries only what a generation run needs.

S2 is a **separate recording session in a different register**. Higher energy, 60 to 90 second
answers, and every answer is clipped and published on its own. That last part governs everything
else: each question is self-contained, restates its own subject, and refers to nothing from S1 and
nothing from the question before it.

Everything in this segment is GENERATED. There is no constant in it. **The two short-form mode notes
were retired 2026-08-17** and sit in `references/statics.json -> retired`; the retake permission and
the self-contained rule are direction to the host and reach them through `pod-3C-client-guide`, not
through the recording script.

## The block shape

```
## Location: {{CITY}}          H2, one per location

**Q1: {question}**                 the whole question bold, label included
  - [{Label}]{.underline}: {what to cover}
  - [{Label}]{.underline}: {what to cover}
  - [{Label}]{.underline}: {what to cover}
```

Ten questions per location, **hard cap, not a range**. Two to four bullets under each question,
three as the default. Nothing else renders under a question.

## Inputs
- **The live Topic Plan Google Doc for this episode.** Fetched this run. Not a local mirror.
- The matching-scope N-Gram Table from `pod-2B-n-gram-table` - the bank, 25 to 35 rows
- The attribute set from `02-attributes.md`
- The matching-scope entity map, for road names, county courts, trauma centers, carriers
- `keyword-research.json` when present, for search demand
- `pod-1C-virality-research` when present - optional by design, skip it when absent
- City and region for each location

## Topic Plan reconciliation - do this first

**The published Google Doc Topic Plan is the only authority. Nothing else counts.**

The client edits that Doc by hand. They rewrite questions, they strike questions, they veto whole
sections, and none of it propagates back to `topic-plan-v{n}.json` or `topic-plan-v{n}.md`. A run
that builds from a local file ships questions the client already rejected. This is not hypothetical:
the Eberst E5 slip-and-fall incident on 2026-06-19 built an entire episode from a stale local mirror
against a topic the live Doc no longer carried.

**Fetch the Doc live, every run.** Record `topic_plan_doc_id`, `topic_plan_revision_id` and
`topic_plan_fetched_at` in `metadata.json`. A run without those three fields did not check and fails
TP-1.

Then, before generating anything:

- **Every one of the ten carries a `topic_plan_ref`** pointing at the Doc row it derives from. A
  question with no ref is an invented question. Match on **substance, not strings** - S2 rewrites
  bank rows into search phrasing, so a question will not be string-identical to its Doc row.
- **Preserve the Doc's relative order.** Tail truncation is allowed and expected; reordering and
  mid-list substitution are not.
- **Client edits win, always.** If the Doc and the N-Gram Table disagree, the Doc wins and the
  N-Gram Table is updated to match so downstream artifacts stay consistent.
- **A vetoed question is dead** - struck-through, deleted or crossed-out text is a veto - **and its
  replacement does not come from the Appendix.** If a veto drops the count below ten, that goes back
  to the Topic Plan, not into a silent substitution.
- **An unresolved comment is a stop, not a signal.** Fetch the Doc's comments. Any question carrying
  one is flagged for human review and does not auto-include.
- **Never build an episode absent from the Doc's lineup.** The Doc is authoritative for the
  episode's topic and title, not just its questions.

Record `topic_plan_reconciled` as `true` or `"legacy-exempt"` in `metadata.json`. A Topic Plan
generated before this requirement is exempt and is not retrofitted; `"legacy-exempt"` on a plan that
was in fact newly generated is the failure that field exists to make visible.

**Verification helper:** `scripts/verify-topic-plan.py`.

## Prompt

**Select the ten.** The N-Gram Table is the bank. Take the ten best and **rewrite them, do not lift
them** - bank rows are research strings, S2 questions are phrased the way a person searches and the
way a host says it out loud. Rank the bank on four things, in this order: search demand,
standalone-ness (answerable in 60 to 90 seconds with no setup and no callback), geo fit, and coverage
spread. Ten questions answering eight distinct things beats ten answering five; two bank rows that
resolve to the same answer collapse into one slot.

**Write each question fully bold, including its `Q{N}:` label.** The question is what the host reads
and what gets clipped, so it carries the only bold weight in the block. Under 18 words.

**Write two to four bullets under each question, three as the default.** Format
`[{Label}]{.underline}: {what to cover}` - the label is two or three words, **underlined and NOT
bold**; the detail is one clause or one short sentence. They are direct descendants of the legacy
ROS's attorney response bullets, same slot and same job: tell the attorney what to cover so they
answer in their own words rather than reading a script.

Compact is the point. A 60 to 90 second answer does not have room for six bullets, and a block that
runs long stops being scannable on the day.

**Set the geo.** Every question is built to exactly one of CITY, CITY + REGION, REGION, NEUTRAL or
STATE, recorded as `geo_tag` in the payload. **Exactly three per location are city-tagged ranking
targets** - they must carry `{{CITY}}` and must never be swapped for the region. Pair the city with
its plain-text region rather than repeating the city on every question: "in Fresno and across the
Central Valley" is how the answers themselves phrase it, so the pairing is the retrieval target and
the same sentence picks up regional queries alongside city ones. `pod-2B`'s 25 to 45 percent
city-share ceiling does **not** apply here - applied to a v2 block it trims the three ranking targets
first, which are exactly the questions that need the city.

**Do a pass per location.** Each location gets its own block, its own ten, and its own selection pass
against that location's n-gram material. Do not generate one set and re-tag it per city. Rank against
that location's scoped N-Gram Table where one exists, otherwise rank the shared bank against that
location's geo fit and demand. Attribute-driven and demand-driven questions carry over largely
unchanged; the three city-tagged slots are what actually change. Every location renders exactly ten -
no location gets nine because the bank was thin.

## Rules
Full rule set in `references/short-form.md` -> "The bullets", "Geo", "Multiple locations" and
"Rules". The ones that bite most often:

- **Never wrap a placeholder in its own `**` markers inside an already-bold question.** The question
  is bold in full, so `**Q3: ... in **{{CITY}}**?**` nests bold, silently unbolds the token, and
  fails the placeholder gate. Write the token bare inside the bold run.
- **Bullet labels are underlined, never bold.** Changed 2026-08-18. Bolding both put the question
  and its bullets at the same visual weight, so the eye landed on the labels first. Rendered as
  pandoc `[text]{.underline}`, never HTML `<u>`.
- **What to cover, never a question.** Zero question marks inside a bullet. Same rule as the
  attribute block, and the same failure mode: the attorney reads a question aloud.
- **Nothing else renders under a question.** No time budget, no geo tag line, no source ref, no
  answer-guidance note. The tags govern generation and never render - a producer auditing geo
  distribution reads the JSON, not the Doc.
- **Entities are welcome, jargon is not.** A road name, a county court, a local trauma center, a
  carrier name are all fine and all sourced from the entity map. A legal term of art is not.
  "How long it sat there is the whole argument", never "constructive notice".
- **A CITY-tagged question requires a real city name.** Interpolating a sub-scope label into the city
  slot produces "hiring a slip and fall lawyer in Public property in San Diego", which is not a
  sentence. Read every city-tagged question aloud with the token resolved before accepting it.
- **S2 has no outro, no close, no sign-off.** The block ends when the last question is answered. The
  outro belongs to S1 and closes S1. The renderer emitted the outro after S2 until 2026-08-18; that
  was a bug, not a format.
- **The full bank ships in the Appendix**, verbatim, unedited, renumbered 1..M. A question rejected
  at ROS review is replaced from there, never invented fresh - but a question the client vetoed in
  the Topic Plan is not.
- **No em dashes.**

## Examples

### GOOD (rendered form)
> **Q1: What should you look for before hiring a slip and fall lawyer in {{CITY}}?**
>
> - [Bar standing]{.underline}: where anybody can look up a license and its history themselves
> - [Case type]{.underline}: how many of this exact kind the firm handles in a month
> - [The hard part]{.underline}: what would make a case like this difficult, said before anybody asks
>
> **Q5: What is a slip and fall case actually worth around here?**
>
> - [What moves it]{.underline}: the injury, the treatment, and how long the hazard sat there
> - [The spread]{.underline}: two cases that landed in different places and why

Q1 is one of the three CITY-tagged ranking targets, with `{{CITY}}` bare inside the bold run rather
than wrapped in its own markers. Q5 is REGION - it carries locality through content, not through the
token. Both questions are bold in full including the label; every bullet label is underlined and not
bold; no bullet is a question; nothing else renders.

### BAD
> - **Q1:** What is duty of care and how is it established under California Civil Code Section 1714(a)?
>   `top-keyword | CITY`
>   *[Attorney Response - 60 sec] Say the city in the first sentence.*
>
> **Q2: What should you look for before hiring a lawyer in **{{CITY}}**?**
>
> - **[Value]{.underline}**: Have you handled cases like this before?

Fails six ways: Q1 is jargon-first and nobody searches it; the citation is banned everywhere above
the Appendix; the geo tag line and the answer note both render; only the `Q1:` label is bold rather
than the whole question; Q2 nests bold around `{{CITY}}` inside an already-bold question, which
unbolds the token; and the bullet is both bold and phrased as a question, so the attorney reads it
aloud.

## Gates
Gates for this section are **SF-1 through SF-12** and **TP-1 through TP-6** in
`references/short-form.md` -> "Gates". They supersede the old S-1 through S-9, which were written
when the bullets were cut from the format and before the Topic Plan requirement existed.

## Feedback
- **SF-1 fails:** cut or add to reach exactly ten per location. Ten is what the contract commits to
  and what the block renders.
- **SF-2 fails:** a question is not bold in full, a bullet label is bold, or the bullet count is
  outside two to four. Check for nested `**` around a placeholder first - that is the common cause of
  a question that looks bold and is not.
- **SF-3 fails:** a bullet is phrased as a question. Rewrite it as what to cover; do not just delete
  the question mark.
- **SF-4 fails:** strip the extra lines. Tag lines and answer notes were removed deliberately - they
  made the block read as a worksheet and the attorney read them aloud.
- **SF-5 fails:** convert the highest-demand questions to `CITY` until there are exactly three. Do
  not apply `pod-2B`'s city-share ceiling to fix it - that trims the ranking targets first.
- **SF-6 fails:** the location has no real city name. Either run city-scope entity research or drop
  its city-tagged slots; never swap a label into the city position.
- **SF-7 fails:** name the untraceable questions and rebuild them from bank rows. Do not pad.
- **SF-8 fails:** the Appendix was edited or truncated. Restore it verbatim from the N-Gram Table.
- **SF-9 / TP-1 fail:** the run did not fetch the live Doc. Fetch it and re-run selection from
  scratch - a set built from a mirror cannot be patched into compliance.
- **TP-2 fails:** an invented question. Cut it and pull its replacement from the Doc's lineup.
- **TP-3 fails:** the ten were reordered or taken with a gap. Restore the Doc's relative order; if a
  later question genuinely belongs in the ten, it moves in the Doc first and the client sees it.
- **TP-4 fails:** a vetoed question survived, or was swapped for a bank row the client never saw.
  Both go back to the Topic Plan, not into a silent substitution.
- **TP-5 fails:** flag the question for human review and exclude it. A client mid-conversation about
  a question has not approved it.
- **TP-6 fails:** the Doc and the N-Gram Table disagreed and the run proceeded anyway. The Doc wins;
  update the N-Gram Table so downstream artifacts stay consistent.
- **SF-10 fails:** jargon or an em dash. Rephrase toward the search, do not delete the substance.
  "What is duty of care" becomes "how do you prove a store knew about the hazard."
- **SF-11 fails:** an invented city token. `{{CITY}}` is the only city placeholder - an additional
  location names its city in plain text, fixed by the template's scope the same way the region is.
  Replace `{{CITY_2}}` or `{{REGION}}` with the literal name; neither token exists and neither will
  ever resolve.
- **SF-12 fails:** an outro, close or CTA rendered after S2. Delete it. The outro renders inside S1,
  above the divider.
