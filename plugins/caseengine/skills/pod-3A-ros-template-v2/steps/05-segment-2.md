# Step 05 - Segment 2 - Short-Form

> **Exec:** mixed (deterministic for the Topic Plan fetch and the gate assertions, LLM for the selection, the rewrite and the bullets - one call per location)
> **Assets:** `references/short-form.md`, `references/document-structure.md`, `references/placeholders.md`, `scripts/verify-topic-plan.py`

## What

Build one set of exactly ten search-phrase questions per location, geo-governed but never geo-labelled on the page. Each question is a standalone 60 to 90 second answer that gets clipped and published on its own, so it restates its own subject and refers to nothing from S1 and nothing from the question before it. Good output is ten questions per location, every one traceable to a row in the LIVE Topic Plan Doc, in the Doc's relative order, each carrying two to four attorney bullets and nothing else.

## Inputs

- `working_set` - from `steps/02-prepare-inputs.md`: `ngram_rows` (the bank), `entity_map`, `attributes`, `keywords` (may be null), `geo.location`, `geo.region` (plain text, never a token).
- `run_context` - from `steps/01-prerequisites.md`: `episode`, `scope`, `location`, `ngram_path`.
- `introduction` and `attributes` as rendered - from `steps/04-segment-1.md`. S2 must not restate S1's framing or reuse its phrasing, and the attribute-driven questions here are the same attribute set S1 established.
- `topic_plan_doc_id` - the episode's PUBLISHED Topic Plan Doc, resolved in the client's Topic Plan slot at run time. Never a local `topic-plan-v{n}.json` or `topic-plan-v{n}.md` mirror.
- Virality rescore from `/pod-1C-virality-research`, optional. Informs the ranking when present, skipped when absent.

## Procedure

Passes 1 through 3 run once for the episode. Passes 4 through 7 run once per location, and every location gets its own selection pass against that location's material - never one set re-tagged per city.

1. **Load the contract** [deterministic] - read `references/short-form.md` in full: the block shape, the selection ranking, the bullet form, the geo rules and gates SF-1 through SF-12 and TP-1 through TP-6. `references/document-structure.md` carries the render weights and `references/placeholders.md` the eleven-token taxonomy. Where any local note disagrees with `short-form.md`, `short-form.md` wins.

2. **Fetch the live Topic Plan Doc** [deterministic] - `python3 scripts/verify-topic-plan.py --doc-id {topic_plan_doc_id} --episode {N} --dump` fetches the Doc at run time and separates the live question rows from the struck ones. Record `topic_plan_doc_id`, `topic_plan_revision_id` and `topic_plan_fetched_at` in `metadata.json`; a run missing any of the three did not check and fails TP-1. Also fetch the Doc's comments - any row carrying an unresolved comment is excluded and flagged for human review under TP-5, because a client mid-conversation about a question has not approved it. Confirm the episode is in the Doc's lineup at all before going further; the Doc is authoritative for the episode's topic and title, not only for its questions. Record `topic_plan_reconciled` as `true`, or as `"legacy-exempt"` when the plan predates the requirement, per SF-9. **The local mirror is stale the moment a client touches the Doc.** That is the Eberst E5 incident of 2026-06-19, and it is the whole reason this pass exists.

3. **Reconcile the bank against the Doc** [deterministic] - where the local n-gram table and the Doc disagree on a question's substance or wording, the Doc wins and the local table at `run_context.ngram_path` is updated to match so downstream artifacts stay consistent. A silent proceed fails TP-6.

4. **Select the ten** [LLM, one call per location] - rank the bank's live, unvetoed, uncommented rows on four things in this order: **search demand** (real volume behind the phrasing, from `keywords` when present, which is the whole reason S2 exists), **standalone-ness** (answerable in 60 to 90 seconds with no setup and no callback, because every answer gets clipped), **geo fit** (does it support the city naturally, or does forcing the city in produce a sentence nobody says), and **coverage spread** (ten questions answering eight distinct things beats ten answering five; two rows resolving to the same answer collapse into one slot). Where a location has its own scoped n-gram table, rank against that one; where it does not, rank the shared bank against that location's geo fit and demand. Attribute-driven and demand-driven questions carry over across locations largely unchanged. Take a **contiguous run in the Doc's order, truncated from the tail only** - a gap in the middle or a reorder fails TP-3. A vetoed question is dead and is not backfilled from the Appendix; if a veto drops the live count below ten, that goes back to the Topic Plan rather than into a silent substitution.

5. **Rewrite into search-phrase form** [LLM] - the bank rows are research strings. Same substance, phrased the way a person searches and the way a host says it out loud: a row reading "How do insurance companies actually calculate what my claim is worth?" becomes "What is a car accident case actually worth around here?". Where the client reworded a question in the Doc, the Doc's wording is the substance to build from. Preserve the relative Doc order. Every question carries a `topic_plan_ref` resolving to its live Doc row (TP-2) and a `source_ngram_ref`, or an `attribute_ref` when the question comes from the attribute set instead (SF-7). **The question renders fully bold, `Q{N}:` label included** - `**Q1: What is the average car accident settlement in {{CITY}}?**`. Do not wrap a placeholder in its own `**` markers inside an already-bold question; nested bold breaks the inline parser, the token renders unbold, and the placeholder gate fails. The token inherits the question's bold.

6. **Assign the geo tags** [deterministic, recorded in the payload] - every question is built to exactly one of CITY, CITY + REGION, REGION, NEUTRAL or STATE, and **exactly three per location are CITY-tagged ranking targets** that must carry `{{CITY}}` and must never be swapped for the region (SF-5). Pair the city with its plain-text region rather than repeating the city on every question: "in Fresno and across the Central Valley" is how the answers phrase it, so the pairing is the retrieval target and the same sentence picks up regional queries alongside city ones. The region is plain text fixed by the template's location scope; `{{REGION}}` does not exist. `pod-2B`'s city-share ceiling is NOT applied here - it trims the three city-tagged targets first, which are exactly the questions that need the city. Read every city-tagged question aloud with the token resolved before accepting it; a sub-scope label interpolated into the city slot produces "hiring a slip and fall lawyer in Public property in San Diego", which is not a sentence (SF-6). **The tags govern generation and never render.** They live in `ros-template-v2-data.json` as `geo_tag`, which is where a producer auditing geo distribution reads them.

7. **Generate the attorney bullets** [LLM] - two to four under each question, three as the default, in the form `[{Label}]{.underline}: {what to cover}`. The label is two or three words, **underlined and not bold**, as pandoc `[text]{.underline}` and never HTML `<u>`; the question carries the only bold weight in the block. The detail is one clause or one short sentence. **What to cover, never a question** - the moment a bullet is phrased as a question the attorney reads it aloud and the block becomes an interrogation (SF-3). Plain language and zero jargon: "How long it sat there is the whole argument", never "constructive notice". Entities are welcome and jargon is not, so a road name, a county court, a local trauma center or a carrier name is fine and sourced from the entity map, while a legal term of art is not. **Nothing else renders under a question** - no time budget, no geo tag line, no source ref, no answer-guidance note, no co-host setup line (SF-4).

8. **Assert the gates** [deterministic] - `python3 scripts/verify-topic-plan.py --doc-id {topic_plan_doc_id} --episode {N} --payload {payload}` enforces TP-1 through TP-4 mechanically. TP-5 and TP-6 are not in the script and are asserted from passes 2 and 3. Then check SF-1 through SF-12 against the payload: ten questions per location with the same count everywhere, bullet counts and forms, zero question marks in bullets, nothing else under a question, three CITY tags per location, every question traceable, appendix row count equal to the n-gram table's, `topic_plan_reconciled` recorded, zero invented city tokens (`{{CITY_2}}` does not exist - an additional location names its city in plain text), no outro, close or CTA after S2, and zero jargon and zero em dashes anywhere in the segment.

## Outputs

```
segment_2: {
  locations: [
    {
      location: str,                       plain text, one block per location
      questions: [                         EXACTLY ten, in the Doc's relative order
        {
          q: str,                          renders fully bold, `Q{N}:` label included
          bullets: [str],                  2-4, `[{Label}]{.underline}: {detail}`
          geo_tag: "CITY"|"CITY + REGION"|"REGION"|"NEUTRAL"|"STATE",   never rendered
          kind: "top-keyword"|"attribute"|"search-phrase",
          source_ngram_ref: str|null,      null ONLY when kind is attribute
          attribute_ref: str|null,
          topic_plan_ref: str              the live Doc row it derives from, never null
        }
      ]
    }
  ]
}

metadata.json: topic_plan_doc_id, topic_plan_revision_id, topic_plan_fetched_at,
               topic_plan_reconciled: true | "legacy-exempt"
```

## Validation

- Exactly ten questions per location, numbered `**Q1:**` through `**Q10:**`, every location the same count (SF-1).
- Two to four bullets under every question in `[{Label}]{.underline}: {detail}` form; the question renders fully bold and the labels render underlined and not bold (SF-2).
- Zero question marks inside a bullet (SF-3), and nothing renders under a question but its bullets (SF-4).
- Exactly three CITY-tagged questions per location, every question carrying exactly one `geo_tag`, with the `pod-2B` city-share ceiling not applied (SF-5).
- Every city-tagged question reads as a real sentence with `{{CITY}}` resolved, checked out loud (SF-6).
- Every question carries a `source_ngram_ref` or an `attribute_ref` (SF-7), and a `topic_plan_ref` resolving to a live Doc row for this episode (TP-2).
- The ten follow the Doc's relative order as a contiguous run, truncated from the tail only (TP-3).
- Zero questions derive from struck or vetoed Doc text, and no vetoed question was replaced from the Appendix (TP-4). Zero questions carry an unresolved Doc comment (TP-5).
- `topic_plan_doc_id`, `topic_plan_revision_id` and `topic_plan_fetched_at` are all in `metadata.json` (TP-1), and `topic_plan_reconciled` is recorded (SF-9).
- Where the local n-gram table disagreed with the Doc, the Doc won and the local table was updated (TP-6).
- Zero jargon and zero em dashes anywhere in the segment (SF-10). Appendix row count equals the n-gram table row count exactly (SF-8).
- Zero invented city tokens - `{{CITY}}` is the only city placeholder and additional locations are plain text (SF-11). S2 carries no outro, close, sign-off, thanks or CTA; the outro renders inside S1, above the divider (SF-12).

## Failure modes

| Failure | Exit behavior | Routes to |
|---|---|---|
| Topic Plan Doc unreachable, or only a local mirror is available | Stop. A run that could not read the Doc cannot claim TP-1, and a mirror is not a substitute | `steps/01-prerequisites.md` |
| The episode is absent from the Doc's lineup | Stop; never build an episode the Doc does not carry | `/pod-2A-topic-planner` |
| A veto drops the live count below ten | Stop. The shortfall goes back to the Topic Plan, never into a silent substitution from the bank | `/pod-2A-topic-planner` |
| A question carries an unresolved Doc comment | Exclude it, flag it for human review, do not auto-include | user |
| The local n-gram table disagrees with the Doc | The Doc wins; update the local table before continuing | `/pod-2B-n-gram-table` |
| A location's bank is thin | Rank the shared bank against that location's geo fit and demand; every location still renders exactly ten | this step |
| A city-tagged question reads wrong with `{{CITY}}` resolved | Rewrite the question. Never demote it to region - the three city slots are fixed | this step |
| A bullet is phrased as a question | Rewrite it as what to cover; SF-3 is the gate that keeps the block from becoming an interrogation | this step |
| A placeholder renders unbold inside a question | Remove the nested `**` around the token; it inherits the question's bold | `steps/07-render.md` |
| Client rejects a question at ROS review | Pull its replacement from the appendix bank, never invent one | `steps/06-appendix.md` |
