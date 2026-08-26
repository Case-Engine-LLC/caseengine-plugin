# S2: Short-Form

The per-location blocks that follow S1. Read by `steps/05-segment-2.md`. The fourth S1/S2 reference doc, alongside `introduction.md`, `attributes.md` and `outro.md`.

S2 is a **separate recording session in a different register**. Higher energy, 60 to 90 second answers, and every answer is clipped and published on its own. That last part governs everything else: each question is self-contained, restates its own subject, and refers to nothing from S1 and nothing from the question before it.

## The block shape

```
## Location: {{CITY}}          H2, one per location

**Q1: {question}**                 the whole question bold, label included
  - [{Label}]{.underline}: {what to cover}
  - [{Label}]{.underline}: {what to cover}
  - [{Label}]{.underline}: {what to cover}

**Q2: {question}**
  - ...
```

Ten questions per location. **Hard cap, not a range.** Ten is what the contract commits to and ten is what the block renders. Nine or eleven fails.

Two to four bullets under each question, three as the default. **Compact is the point** - a 60 to 90 second answer does not have room for six bullets, and a block that runs long stops being scannable on the day.

## Where the questions come from

**The N-Gram Table is the bank.** `pod-2B-n-gram-table` produces 25 to 35 questions for this episode at this scope. S2 takes the **ten best** and writes them in search-phrase form.

**Rewritten, not lifted.** The bank rows are research strings. A row reads "How do insurance companies actually calculate what my claim is worth?" and the S2 question reads "What is a car accident case actually worth around here?" Same substance, phrased the way a person searches and the way a host says it out loud. The full bank still ships verbatim in the Appendix as the audit trail and the pull pool.

**Selecting the ten.** Rank the bank on four things, in this order:

- **Search demand** - real volume behind the phrasing, from `keyword-research.json` when present. This is the whole reason S2 exists.
- **Standalone-ness** - can it be answered in 60 to 90 seconds with no setup and no callback? A question that needs S1's context to make sense cannot be clipped, and every S2 answer gets clipped.
- **Geo fit** - does it support the city naturally, or does forcing the city into it produce a sentence nobody says?
- **Coverage spread** - ten questions answering eight distinct things beats ten answering five. Two bank rows that resolve to the same answer collapse into one slot.

When `pod-1C-virality-research` exists for this episode, its rescore informs the ranking. When it does not, skip it. It is optional by design.

## Topic Plan reconciliation

**The published Google Doc Topic Plan is the only authority. Nothing else counts.**

The client reads that Doc and edits it by hand. They rewrite questions, they strike questions, they veto whole sections. None of that propagates back to `topic-plan-v{n}.json` or `topic-plan-v{n}.md`, so every local mirror is stale the moment a client touches the Doc. A run that builds from a local file ships questions the client already rejected.

This is not hypothetical. The Eberst E5 slip-and-fall incident on 2026-06-19 built an entire episode from a stale local mirror against a topic the live Doc no longer carried.

**Fetch the Doc live, every run.** Resolve the episode's Topic Plan Doc in the client's Topic Plan slot, fetch it at run time, and record `topic_plan_doc_id`, `topic_plan_revision_id` and `topic_plan_fetched_at` in `metadata.json`. A run without those three fields did not check and fails.

### What must match

**Substance, not strings.** S2 rewrites bank rows into search phrasing, so a question will not be string-identical to its Topic Plan row. Every one of the ten carries a `topic_plan_ref` pointing at the Doc row it derives from. A question with no ref is an invented question.

**Order is preserved.** The ten render in the same relative order they appear in the Doc. The client sees a sequence and expects that sequence.

**Truncating from the tail is allowed. Reordering and substitution are not.** Over-engineering an initial plan to twenty questions and shipping the first ten is fine and expected. Taking questions 1 through 8 plus 14 and 19 is not, and neither is shipping 1 through 10 in a different order. If a later question genuinely belongs in the ten, it moves in the Topic Plan Doc first and the client sees the change.

**Client edits win, always.** If a question's wording changed in the Doc, the Doc's wording is the substance to build from. If the Doc and the N-Gram Table disagree, the Doc wins and the N-Gram Table is updated to match so downstream artifacts stay consistent.

**A vetoed question is dead, and its replacement does not come from the Appendix.** Struck-through, deleted or crossed-out text in the Doc is a veto. A vetoed question cannot appear in S2, and it cannot be quietly swapped for a bank row the client never saw. The pull pool is for a rejection at ROS review, not for backfilling something the client already killed in the plan. If a veto drops the count below ten, that goes back to the Topic Plan, not into a silent substitution.

**An unresolved comment is a stop, not a signal.** Fetch the Doc's comments. Any question carrying an unresolved comment is flagged for human review and does not auto-include. A client mid-conversation about a question has not approved it.

**Never build an episode absent from the Doc's lineup.** The Doc is authoritative for the episode's topic and title, not just its questions.

### Legacy exemption

A Topic Plan generated before this requirement is exempt and is not retrofitted. The check applies to newly generated plans. Record which path ran in `metadata.json` as `topic_plan_reconciled: true | "legacy-exempt"`. `"legacy-exempt"` on a plan that was in fact newly generated is the failure this field exists to make visible.

Verification helper: `scripts/verify-topic-plan.py`.

## The bullets

Direct descendants of the legacy ROS's attorney response bullets, same slot and same job: tell the attorney **what to cover**, so they answer in their own words rather than reading a script.

- **Format** - `[{Label}]{.underline}: {what to cover}`. The label is two or three words, **underlined and not bold**. The detail is one clause or one short sentence.
- **The question is bold in full; the bullet labels are underlined.** Changed 2026-08-18. Bolding both put the question and its bullets at the same visual weight, so the eye landed on the labels first. The question is what the host reads and what gets clipped, so it carries the only bold on the page and the labels drop to underline. Underline is also the CE convention for entity runs, rendered as pandoc `[text]{.underline}`, never HTML.
- **Two to four per question**, three as the default.
- **What to cover, never a question.** Same rule as the attribute block. The moment a bullet is phrased as a question the attorney reads it aloud and the block becomes an interrogation. See `references/attributes.md`.
- **Plain language, zero jargon.** No statute numbers, no case citations, no element names. "How long it sat there is the whole argument", never "constructive notice".
- **Entities are welcome, jargon is not.** A road name, a county court, a local trauma center, a carrier name - all fine and all sourced from the entity map. A legal term of art is not. This is the same line `references/introduction.md` draws for pattern C.
- **No time budget, no geo tag line, no source ref.** Those render nowhere. The bullets are the only thing under a question.

## Geo

**Three of the ten are city-tagged ranking targets.** They must carry `{{CITY}}` and must never be swapped for the region. The remaining seven carry locality through content rather than through the token.

**Pair the city with its region.** Do not repeat the city on every question. "In Fresno and across the Central Valley" is how the answers themselves phrase it, so the pairing is the retrieval target and the same sentence picks up regional queries alongside city ones.

**The tags govern generation and never render.** Every question is built to one of CITY, CITY + REGION, REGION, NEUTRAL or STATE. The tag stays in `ros-template-v2-data.json` as `geo_tag` for downstream and QA. A producer auditing geo distribution reads the JSON, not the Doc.

**The region is plain text, never a placeholder.** It is fixed by the template's location scope. `{{REGION}}` does not exist.

**`pod-2B`'s city-share ceiling does not apply here.** That roughly 25 to 45 percent aggregate cap was a blunt defense from the legacy format. Applied to a v2 block it trims the three city-tagged ranking targets first, which are exactly the questions that need the city.

**A CITY-tagged question requires a real city name.** Interpolating a sub-scope label into the city slot produces "hiring a slip and fall lawyer in Public property in San Diego", which is not a sentence. Read every city-tagged question aloud with the token resolved before accepting it.

## Multiple locations

**No second city token, decided 2026-08-18.** Each location gets its own full set of ten questions, so a location block never needs to reference another block's city. `{{CITY}}` resolves to the episode's geo target and is used by that location's set. Any additional location names its city in **plain text**, fixed by the template's scope exactly the way the region is. `{{CITY_2}}` does not exist and must not be invented, the same prohibition that applies to `{{REGION}}`.

This works because a location set is self-contained. It carries its own ten questions, its own three city-tagged ranking targets and its own bullets, and it is recorded as its own block. There is no cross-set reference for a token to resolve.

Each location gets **its own selection pass** against that location's n-gram material. Do not generate one set and re-tag it per city.

- Where a location has its own scoped N-Gram Table, rank against that one.
- Where it does not, rank the shared bank against that location's geo fit and demand.
- **Demand-driven questions carry across locations largely unchanged** - what a person wants to know before hiring a lawyer does not vary much by city. In the worked example six of the ten carry over untouched.
- **The geo-bearing slots are what actually change** per location: the three city-tagged targets plus the city-and-region pairing, and any question whose answer genuinely differs by market.
- Every location renders exactly ten. No location gets nine because the bank was thin. If a location cannot support ten good questions, that is a signal it should not be its own set.

Multi-location firms record the blocks back to back in one session.

## Rules

- **Self-contained, always.** Each answer restates its own subject and refers to nothing from S1 and nothing from the previous question. Each one is published alone.
- **60 to 90 seconds.** Retakes are expected and normal; if one comes out flat, go again.
- **Higher energy than S1.** Different register on purpose, and the host says so on mic at the switch.
- **The full bank ships in the Appendix**, verbatim, unedited, renumbered 1..M. Audit trail and live pull pool when a client rejects a question.
- **A rejected question is replaced from the Appendix**, never invented fresh.
- **S2 has NO outro, no close, and no sign-off. It is straight question and answer.** The block ends when the last question is answered. The outro belongs to S1 and closes S1, because S1 is a complete recording on its own and S2 is a separate session in a different register whose answers are each clipped and published individually. An outro on S2 would be clipped along with them and land on a short that has no show around it. The renderer emitted the outro after S2 until 2026-08-18; that was a bug, not a format.

## Gates

- **SF-1** Exactly ten questions per location, numbered `**Q1:**` through `**Q10:**`. Every location has the same count.
- **SF-2** Two to four bullets under every question, each in `[{Label}]{.underline}: {detail}` form. The question renders fully bold; bullet labels render underlined and NOT bold.
- **SF-3** Zero question marks inside a bullet. Bullets say what to cover.
- **SF-4** Nothing else renders under a question - no time budget, no geo tag line, no source ref, no answer-guidance note.
- **SF-5** Every question carries exactly one `geo_tag` in the payload from {CITY, CITY + REGION, REGION, NEUTRAL, STATE}, with exactly three city-tagged per location. The `pod-2B` city-share ceiling is NOT applied.
- **SF-6** Every city-tagged question reads as a real sentence with `{{CITY}}` resolved. Read it aloud.
- **SF-7** Every question traces to n-gram substance via `source_ngram_ref`, or to the attribute set. An untraceable question is an invented one.
- **SF-8** Appendix row count equals the N-Gram Table row count exactly.
- **SF-9** `topic_plan_reconciled` is recorded as `true` or `"legacy-exempt"`. A newly generated plan left unreconciled FAILS.
- **TP-1** The live Topic Plan Doc was fetched this run. `topic_plan_doc_id`, `topic_plan_revision_id` and `topic_plan_fetched_at` are all present in `metadata.json`. A run built from a local mirror alone FAILS.
- **TP-2** Every one of the ten questions carries a `topic_plan_ref` resolving to a row in the live Doc for THIS episode. Zero unreferenced questions.
- **TP-3** The ten appear in the same relative order as the Doc. Tail truncation is allowed; a gap in the middle or any reordering FAILS.
- **TP-4** Zero questions derive from struck-through, deleted or vetoed Doc text, and no vetoed question was replaced from the Appendix.
- **TP-5** Zero questions carry an unresolved Doc comment. Any that do are flagged for human review and excluded.
- **TP-6** Where the local N-Gram Table disagrees with the Doc, the Doc won and the local table was updated. A silent proceed FAILS.
- **SF-10** Zero jargon and zero em dashes anywhere in the segment.
- **SF-11** Zero occurrences of any invented city token. `{{CITY}}` is the only city placeholder; additional locations are plain text. `{{CITY_2}}` and `{{REGION}}` do not exist.
- **SF-12** S2 carries no outro, close, sign-off, thanks or CTA. The segment ends on the last answer. The outro renders inside S1, above the divider.

## Why the bullets came back

They were cut on 2026-08-14 and restored on 2026-08-18 at Gabe's direction.

The original cut was right about its evidence and wrong about its conclusion. What made the earlier blocks read as worksheets was not that content sat under a question - it was that the content was **answer guidance phrased as instruction to the reader**, alongside geo tag lines and time budgets that turned the block into a form. Attorneys read those aloud because they looked like things to say.

The legacy ROS solved this years ago with `**Label:** detail` bullets that describe what to cover rather than what to say, and that form never had the read-aloud problem. So the bullets return in the legacy form, the tag lines and time budgets stay dead, and SF-3 and SF-4 are the gates that keep the distinction from eroding.
