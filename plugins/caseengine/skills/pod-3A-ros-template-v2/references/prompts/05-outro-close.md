# 05 - Outro

> **References:** `references/outro.md` is the narrative source of truth for this section - the
> three-line shape, why the sign-off lands before the reach-out, and gates OC-1 through OC-9.
> `references/outro-banks.json` carries the required beats, invariants and banks each line is
> generated against and is the contract: if the two ever disagree, the JSON wins. Read both before
> touching anything here. This file only carries what a generation run needs.

Three spoken lines, all GENERATED per episode. The only constant left in the section is
`outro_note`, which is direction to the host and is never spoken.

## Inputs
- `references/outro-banks.json` - beats, invariants, banks and slots for all three lines
- This episode's `{topic_phrase}`, for the topical credit approach in line 1
- The prior two episodes' `metadata.json` for this client, for rotation

## What is STATIC here (do not generate)
- `outro_note` - read it from `references/statics.json` -> `strings`, not from this file.

Nothing else. `outro_thanks`, `outro_signoff`, `outro_reach` and `outro_praise` were constants
until 2026-08-18 and are not any more; anything still quoting them verbatim is stale.

## Render order
1. `## Outro` heading (H2, CE_DARK)
2. STATIC `outro_note`, italic
3. Line 1 - thanks and credit
4. Line 2 - sign-off
5. Line 3 - reach-out

No speaker tag. The `INTERVIEWER` tag was cut 2026-08-18: `outro_note` sits directly above and
already says who is speaking, so a tag on a three-line close is clutter. Emitting one fails OC-1.

The sign-off is not last. The reach-out lands after it as a tag, so the contact details are the
final thing the listener hears without the episode ending on an ad. Reordering these two fails OC-1.

## Prompt

**Generate line 1 - thanks and credit.** Address the attorney with `{{ATTORNEY}}`, thank them
explicitly, and add one credit clause. Pick a stem from `line_1_thanks.thanks_stems` and a credit
approach from `line_1_thanks.credit_approaches` - topical, reps, clarity, candor, or depth. Prefer
**topical** whenever `{topic_phrase}` is concrete: it is the only approach whose clause cannot be
reused on another episode, which makes it the strongest source of per-episode uniqueness. Every
other approach produces a clause that would fit any episode of any show. Under 30 words.

**Generate line 2 - the sign-off.** Rotate within `line_2_signoff.bank`. Variation here is LOW by
design; this is the sonic bookend to intro line 1 and the repetition is most of its value. Do not
invent a new form until every bank entry has been used in the current season.

**Generate line 3 - the reach-out.** Assemble `hinge + geo_and_need + verb + contact_frame` from
`line_3_reach.slots`. The `call` verb only pairs with a contact frame whose first token is the firm
name.

**Rotate.** Read the prior two episodes' `metadata.json` for this client. Do not reuse a line 1
approach or a line 2 bank entry from either. Line 3 must differ from the immediately preceding
episode in at least two of its four slots. Record `outro_line1_approach`, `outro_line1_stem_index`,
`outro_line2_index` and `outro_line3_slots` in `metadata.json`.

## Rules
Full rule set in `references/outro-banks.json` (per line) and `references/outro.md` -> "Rules" and
"Do not". The ones that bite most often:

- Do not add an episode recap. The outro note says not to, and a recap is the most common thing a
  host adds unprompted.
- Allude, do not gush. "You're brilliant", "that was incredible", "one of the best in the state"
  all fail. Credit something specific the attorney did in this episode.
- Never a superlative, a ranking, or an award.
- The geo is `{{STATE}}`, never `{{CITY}}`. A city here silently makes the whole long-form segment
  non-reusable across the firm's market.
- The need clause stays practice-area neutral. "If you were hurt" is nonsense on an estate planning
  show and describes the wrong person on a criminal defense show.
- One reach-out per episode, never two. Two contact routes, once each, phone before website.
- Never name Case Engine, and never an episode number or a next-episode tease.
- The banks are starting points showing range, not closed menus. A line that satisfies the beats,
  the invariants and the rules is valid even if it appears nowhere in the bank. A run that only ever
  quotes bank entries verbatim is doing selection, which visibly cycles across a library and defeats
  the point.
- Substitute with `.replace()`, never `str.format()`. These strings carry `{{PLACEHOLDER}}` tokens
  and `str.format` collapses the doubled braces, silently destroying every token in the line.

## Examples

### GOOD
> **{{ATTORNEY}}**, thank you for your time. There is almost nothing useful online about
> {topic_phrase}, so that is going to help somebody.
>
> That is where we will leave it. **{{PODCAST_NAME}}**. See you next episode.
>
> And before you go, if you are anywhere in **{{STATE}}** and need help with this, get in touch
> with **{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**.

Hits every beat, credits something specific to this episode, and reuses no line verbatim from the
previous episode.

### BAD
> So that about wraps it up. We covered a lot today - what to do in the first 48 hours, how the
> evidence disappears, who is actually responsible. Really great stuff. Again, if you or a loved
> one has been injured, call **{{FIRM_NAME}}** today at **{{PHONE_NUMBER}}**. And remember, you
> can also visit **{{WEBSITE}}**. Thanks again.

Fails: it recaps the episode, reaches out twice, never addresses the attorney, and the need clause
is injury-only.

## Gates
Gates for this section are **OC-1 through OC-9** in `references/outro.md` -> "Gates", plus the
per-line `required_beats` and `invariant` fields in `references/outro-banks.json`. They supersede
the old O-1 through O-4, which were written when all four lines were frozen strings.

## Feedback
- **OC-1 fails:** the reach-out was rendered before the sign-off, or a line was dropped. Restore the
  six-element render order above.
- **A line's `invariant` fails:** a token was dropped, duplicated, or left unbolded. Regenerate that
  line against its beats rather than patching the token in.
- **OC-5 fails:** a CE credit came back into the sign-off, or `{{CITY}}` reached line 3. Cut it.
- **OC-6 fails:** guest framing, a recap, a subscribe CTA, or an em dash. Regenerate the line.
- **OC-7 / rotation fails:** the run reused a line 1 approach or a line 2 entry from the previous
  two episodes. Reselect and re-record all four rotation fields in `metadata.json`.
- **OC-8 fails:** a run regenerated `outro_note`. Restore it byte-identical from
  `references/statics.json` -> `strings`. It is the one constant left in the section.
- **OC-9 fails:** a line passed every count and is still not a sentence anybody would say. Read all
  three aloud, in order, immediately after the Introduction, so cross-section repetition is audible.
  Rewrite the line rather than trimming words off it. See `steps/08-qa.md` tier 4.
