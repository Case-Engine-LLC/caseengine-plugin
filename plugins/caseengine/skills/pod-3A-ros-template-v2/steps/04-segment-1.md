# Step 04 - Segment 1 - Long-Form

> **Exec:** mixed (LLM for the introduction, the attribute transform and the outro; deterministic for the constants, the ordering and the rotation)
> **Assets:** `references/introduction.md`, `references/attributes.md`, `references/statics.json`, `references/outro.md`, `references/outro-banks.json`, `references/placeholders.md`, `references/document-structure.md`, `scripts/outro-rotation.py`

## What

Write the whole of S1 in document order - the introduction and its single prompt, the attribute block, and the outro that closes the segment.

## Inputs

- `working_set` - from `steps/02-prepare-inputs.md`: `attributes` (with `source` and `pull_date`), `entity_map`, `clusters`, `ngram_rows`, `keywords`, `geo.location`, `geo.region`, `calibration_examples`.
- `run_context` - from `steps/01-prerequisites.md`: `episode`, `topic`, `scope`, `location`, `episode_goal`.
- Resolved factual claims - from `steps/02-prepare-inputs.md` pass 7: years in practice, case types, caseload, trial record, offices, team, and any market statistic, each with its source and check date. Anything unresolved is not available to a frame.
- `topic_phrase` inputs - the theme phrased the way a person in trouble would say it, and the episode's subject in plain language, from the research corpus.
- Prior episodes' `metadata.json` for this client - for the frame and outro rotation.

## Procedure

Three passes, in document order: the introduction, the attribute block, then the outro. None of them can see what the others wrote, so the cross-section repetition check in `steps/08-qa.md` is what catches a credit or a stakes clause used twice.

**The introduction is four sentences and one beat, and it is a shape rather than a script.** The host reads line 1 as written and says the rest in their own words. Four sentences is the ceiling, not a target. Run it in this order:

1. **Load the contract** [deterministic] - read `references/introduction.md` for the four line jobs, the line 2 opener bank, the eight EEAT frames and the line 4 beats spec, and `references/statics.json` for the constant. Where the constant already covers the words, the constant wins and nothing regenerates them.
2. **Emit line 1** [deterministic] - the `welcome` string from `references/statics.json`, byte-identical. Nothing substitutes into it: `{topic_phrase}` moved out on 2026-08-18 when the constant shrank to line 1 only. `welcome_first` exists for the launch episode, but Episode 1 routes to `/pod-3B-client-ros` at `steps/01-prerequisites.md` and never reaches this step, so `welcome` is the form in practice. The line is a sonic marker rather than information: adding a tagline, an episode number or a second welcome breaks it.
3. **Generate `topic_phrase` and line 2, the setup** [LLM] - `topic_phrase` is the episode's subject as a plain phrase; it feeds line 2's subject slot and the outro's topical credit approach, and it substitutes into nothing. Line 2 is its own generated paragraph, carried in the payload as `segment_1.setup`, built from four slots in order - host ID (`I'm {{INTERVIEWER}}`), the turn, the subject, the stakes - at 25 to 30 words. It carries the subject slot and the stakes clause that ends line 2. Name the thing in plain language, never the practice area as a category and never the episode title verbatim; if the only name is a legal one, say it once and alias it immediately ("premises liability, or so-called slip and fall"). The stakes clause is one clause about the listener, in the second person, and it is a fact rather than a threat: "what you actually need to know if it happens to you", never "before you lose everything". **NO geo in line 2 (Gabe 2026-08-26)** - the state moved to line 3, the EEAT line; the long-form answer is still state-governed, so one recording serves every city the firm covers. Vary the opener across episodes ("today we're going to discuss X" / "today the topic is X" / "the theme today is X" / "we're going to dive into X" / "today we're talking about X"; Gabe 2026-08-26), add NO hook clause that gives away the episode's insight, and note that pattern C is mostly off in S1 now that the segment speaks at state level, available only when the entity map carries a statewide-recognizable anchor. A number runs only under pattern B and only when it is sourced, credible, current with its year said out loud, and matched to this geography and topic; round toward safety, never invent precision, and fall back to pattern A when any of the four tests fails. Line 2 ends at the stakes clause. Everything after it gets deleted.
4. **Write line 3, the EEAT line** [LLM, over resolved facts only] - carried in the payload as `segment_1.credential`, its own paragraph so the ask in line 4 lands as a turn rather than the tail of a long sentence. Its job is establishing experience, expertise, authority, or trust - a credential is one form, not the definition (Gabe 2026-08-26). Exactly one of the eight frames, stated as a fact and spoken directly to the attorney by first name, under 25 words; one or two sentences, the second may bridge into the topic. Two credentials in one sentence is a bio. Every credential lands on a number or a range, never `countless`, `numerous` or `years of experience` with no figure attached, and rounding follows the same rule as any other number. Use the facts resolved in `steps/02-prepare-inputs.md`; never from memory, never from a previous episode's ROS, and never hedged in when unresolved - switch to L3-A tenure instead, whose one number the profile always has. Tenure is BANNED when any recent episode's credential already used years (Gabe 2026-08-26): go loose instead, a vaguer nod to expertise and experience that sets up the topic, with no years figure. Rotate frames across the library and match the frame to `episode_goal`. **The STATE slides in here (Gabe 2026-08-26)** - line 2 carries no geo, and no city appears anywhere in S1; if geo wants saying beyond the state, say "here". The attorney's name may land at the end of the clause or the front; alternate so neither becomes the tic.
5. **Mark the beat** [deterministic] - after line 3 the attorney says hello, a sentence or two, unscripted. It renders as a direction rather than dialogue, and it exists so the second voice arrives at 25 seconds instead of 40. It is also the one part of S1 that is fair game to cut in post, so the direction says so.
6. **Write line 4, the ask** [LLM] - carried in the payload as `segment_1.prompt` and the only bolded prompt in the document. "Walk us through" plus 2-3 question-shaped beats (Gabe 2026-08-26), each a restartable 5 to 10 minute prompt: DEFINITION (plain "what X is", never "even is"; "For people who are unfamiliar, let's start with..." is sanctioned), then DIFFERENCE, then CHALLENGES - a narrow topic takes two beats. Each beat under roughly twelve words, the whole ask under roughly thirty-five, no subordinate clauses. Ground the beats in the episode's body questions where they cluster, never ask for credentials again - line 3 did that - and do not let a beat repeat what line 2 already said. Then stop talking: no example to get them started, no narrowing, no "for instance".
7. **Record the selections and the claims** [deterministic] - write `line2_pattern`, `line3_frame` and `line4_frame` into `metadata.json`, plus every asserted fact as claim, source and date checked. A run that renders without recording these leaves the next episode unable to rotate and forces the next writer to re-guess the provenance.
8. **Read it aloud** [LLM] - 80 to 110 words across four sentences plus the beat. The north star is "sounds normal": if a line would be strange to say out loud to a person standing in front of you, it fails regardless of how well it reads.

**The attribute block is an inversion of the research, not a copy of it.** `pod-1D-attribute-research` produces a catalog whose unit is the ask a client can put to the firm. This block needs the same attributes pointed the other way, so its unit is what the attorney covers when answering. Run it in this order:

1. **Load the attribute set** [deterministic] - `working_set.attributes`. A live `pod-1D` output is Confirmed; the `references/attributes/attributes-fallback.json` snapshot is Inferred and is flagged with its pull date. Record `attribute_source`, the pull date and the confidence in `metadata.json` (AT-8).
2. **Invert each catalog row into response guidance** [LLM] - **no question ever appears in this block, not one.** The catalog stores questions because a researcher needs a checkable ask; the moment a question lands on this page the attorney reads it aloud and the block becomes the worksheet interrogation v2 exists to replace. "Trial willingness. Have you taken these to trial, or do you only settle?" is the wrong form. "Trial willingness. Cases you actually tried rather than settled, and what that changes at the table before a jury is picked" is the right one - same attribute, same substance, and only the second tells the attorney what to say (AT-1).
3. **Write each bullet to the locked form** [LLM] - a **bold** lead-in of two or three words carrying the plain attribute name, then one sentence of what to cover in the words a person uses, concrete enough that the attorney knows what a good answer contains. Nothing else: no question, no rank, no source count, no verbatim quote, no "why it lands" note, all of which is catalog metadata that stays in the catalog (AT-2, AT-5). **The attribute lead-in is bold, not underlined** - that is the deliberate difference from S2, where the label drops to underline so the question keeps the only bold weight. Do not harmonize the two.
4. **Keep fee structure** [deterministic] - it fails `pod-1D`'s discriminating gate because every personal injury firm works on contingency, and it stays on the page anyway. A listener still needs to hear how the firm gets paid, what happens if they lose, and who fronts records, filing fees and experts. It is the one documented exception to AT-3, and the catalog does not get "fixed" to match.
5. **Order the block** [deterministic] - credentials first, logistics last, by what an attorney naturally covers rather than by research rank. The catalog's ranking is right for a researcher comparing pulls month over month and wrong for somebody reading down a page mid-sentence (AT-4). Bar standing sits above reviews wherever both are present, and a "name the hard part" bullet is present, because naming a weakness builds more trust than making a promise (AT-7).
6. **Lead with what line 3 established** [deterministic] - whichever credential frame line 3 used is the attribute the attorney will hit hardest in the answer, so place it where the answer starts.
7. **Trim to ten to twelve bullets** [deterministic] - past twelve the attorney stops treating it as a shape and starts treating it as a list to get through (AT-2).
8. **Scan the block** [deterministic] - zero jargon, zero superlatives, zero marketing adjectives, and plain attribute names rather than branded ones: "Time in the market", not "Proven Local Legacy" (AT-6).

**The outro is generated, not emitted.** It stopped being boilerplate on 2026-08-18: only `outro_note` is constant, and all three spoken lines are written per episode against required beats. Run it as its own pass, in this order:

1. **Load the contract** [deterministic] - read `references/outro-banks.json` for the per-line beats, invariants, banks and slots, and `references/outro.md` for the reasoning behind them. The JSON wins if the two ever disagree.
2. **Check rotation** [deterministic] - read the prior episodes' `metadata.json` for this client via `scripts/outro-rotation.py`. A line 1 credit approach may not repeat within two episodes, a line 2 bank entry may not repeat within two episodes, and line 3 must differ from the immediately preceding episode in at least two of its four slots.
3. **Select the credit approach** [deterministic, informed by the episode] - topical, reps, clarity, candor or depth. Prefer **topical** whenever `{topic_phrase}` is concrete: it is the only approach whose clause cannot be reused on another episode. Do not run depth if the introduction already leaned on `{{YEARS_PRACTICING}}`, and do not pick an approach the rotation check excluded.
4. **Generate the three lines** [LLM] - line 1 thanks and credit, line 2 the sign-off, line 3 the reach-out tag. The sign-off is deliberately **not** last. Line 2 rotates within its bank because its variation is low by design; lines 1 and 3 are written against the beats rather than picked, since a run that only ever quotes bank entries visibly cycles across a library and defeats the point.
5. **Assert the invariants** [deterministic] - per-line `invariant` fields in the banks plus gates OC-1 through OC-7 in `references/outro.md`. `{{STATE}}` and never `{{CITY}}` in line 3; zero occurrences of "Case Engine" anywhere in the section.
6. **Record the rotation fields** [deterministic] - write `outro_line1_approach`, `outro_line1_stem_index`, `outro_line2_index` and `outro_line3_slots` into `metadata.json`. A run that renders without recording these fails OC-7 and leaves the next episode unable to rotate.

## Outputs

```
introduction: {
  welcome: str,                          STATIC, line 1, nothing substitutes into it
  topic_phrase: str,                     GENERATED - the subject as a plain phrase
  setup: str,                            GENERATED - line 2, its own paragraph
  credential: str,                       GENERATED - line 3, its own paragraph
  prompt: str,                           GENERATED - line 4, the ask, exactly one
                                         prompt, rendered in full bold
  beat: str,                             the unscripted hello, marked as a direction
  line2_pattern: "A".."J",
  line3_frame: "L3-A".."L3-H",
  line4_frame: "L4-A".."L4-F"
}

attributes: [{ name: str, detail: str }] 10-12, bold lead-in plus one sentence,
                                         credentials first through logistics last

metadata.json: line2_pattern, line3_frame, line4_frame,
               claims: [{claim, source, date_checked}],
               attribute_source: "pod-1D"|"fallback",
               attribute_pull_date, attribute_confidence

outro: { thanks, signoff, reach }        the three generated lines, in render order
metadata.json: outro_line1_approach, outro_line1_stem_index,
               outro_line2_index, outro_line3_slots
```

## Validation

- Line 1 renders byte-identical to `welcome` in `references/statics.json`, with no substitution of any kind (IN-2).
- The introduction is four sentences plus the beat direction, in order (IN-1), 80 to 110 words, read aloud before it is accepted (IN-8).
- Line 2 carries NO geo and NO insight-spoiling hook, names the topic plainly, and ends cleanly (IN-3; Gabe 2026-08-26). Any number in it traces to a source recorded in `metadata.json`; no source means pattern A (IN-4).
- Line 3 carries exactly one EEAT signal and the state (IN-5); a numeric credential lands on a number or a range; no city anywhere in S1 (Gabe 2026-08-26).
- Line 4 opens "Walk us through" and carries 2-3 question-shaped beats, each under roughly twelve words, the whole ask under roughly thirty-five (IN-6; Gabe 2026-08-26).
- Zero guest framing, zero legal jargon, zero em dashes across the section (IN-7). Gates IN-1 through IN-8 are in `references/introduction.md`.
- `line2_pattern`, `line3_frame` and `line4_frame` are recorded in `metadata.json`, and every asserted fact is recorded as claim, source and date checked.
- The attribute block is ten to twelve bullets, each a bold lead-in plus one sentence of what to cover, with zero question marks in it - gates AT-1 through AT-8 in `references/attributes.md`.
- Attribute lead-ins render bold; only S2's bullet labels are underlined.
- The outro carries three spoken lines in the order thanks, sign-off, reach-out, each clearing its `invariant` in `references/outro-banks.json`, with NO speaker tag above them (OC-1).
- The four rotation fields are present in `metadata.json` and none of them repeats a value the rotation rules exclude.

## Failure modes

| Failure | Exit behavior | Routes to |
|---|---|---|
| A credential fact will not resolve | Switch to L3-A tenure - unless years appeared in a recent episode's credential, then a loose expertise nod with no years figure (Gabe 2026-08-26); never hedge an unverified count into the script | `steps/02-prepare-inputs.md` |
| No sourced, current, geo-matched number for line 2 | Drop the quantity entirely and run pattern A, which asserts nothing that can be wrong | `references/introduction.md` |
| Pattern C selected with no local anchor in the entity map | Fall back to A or D; never write a road or an interchange from general knowledge | `references/introduction.md` |
| The line 4 frame repeats what line 2 already said | Reselect the frame; the format has one prompt and cannot spend it twice | this step |
| The introduction runs past four sentences or 110 words | Cut at the stakes clause and read it aloud again | this step |
| An attribute bullet carries a question mark | Rewrite it as what to cover; AT-1 is the gate that matters most | `references/attributes.md` |
| The attribute set came from the fallback | Proceed, flag the run Inferred with the fallback's pull date, and queue a re-pull | `/pod-1D-attribute-research` |
| Fewer than ten usable attribute rows after the transform | Keep the fee structure exception and re-pull; never pad with marketing language | `/pod-1D-attribute-research` |
| An outro line misses a required beat or fails its invariant | Regenerate that line against the beats; do not patch the token in by hand | references/outro-banks.json |
| Rotation would repeat a credit approach or sign-off entry | Reselect before generating | scripts/outro-rotation.py |
| Prior `metadata.json` unreadable or absent (first episode) | Proceed, record the rotation fields for the next run | - |
