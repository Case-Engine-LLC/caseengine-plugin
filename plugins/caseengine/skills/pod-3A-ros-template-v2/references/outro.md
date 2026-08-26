# Outro

## GUARDRAILS

**Calibrate on `examples/intro-outro-examples.md` first.**

- Three lines: thanks-and-credit, sign-off, reach-out. In that order.
- Line 1 is TWO sentences: address and thank, then ONE credit clause. The credit is a required beat, not optional.
- **No CTA. Ever.** No subscribe, like, follow, review, bell. The show is a search asset, not a channel play.
- Line 2 names `{{PODCAST_NAME}}`. It is the sonic bookend - repetition here is the feature, and it is exempt from the uniqueness rule.
- Line 3 opens with a hinge that acknowledges the goodbye it follows, carries `{{STATE}}` (never `{{CITY}}`), and gives phone before website. One reach-out, never two.
- Contractions. No em dashes. No CE credit, no episode number, no next-episode tease, no thanking the audience.
- Lines 1 and 3 must not repeat the wording or the shape of recent episodes.
- Read all three aloud before accepting them.
- **The banks are calibration, not a script.** They are written without contractions and some read stiff. Contract them, trim a trailing "of it", and cut a repeated construction. The bank shows the register; you write the line.



The last 15 to 25 seconds of S1. Read by `steps/04-segment-1.md`. The companion to `references/introduction.md`.

Like the introduction, this is a shape rather than a script. **All three spoken lines are generated per episode.** Only the direction line the host reads off the page is constant.

> **Machine-readable spec:** `references/outro-banks.json`. It carries the required beats, invariants, banks and slots. This file is the reasoning; that file is the contract. If they ever disagree, the JSON wins and this file is the thing to fix.

## Three parts, three lines

The intro opens with branding, sets up the topic, then asks. The outro thanks, closes the show, then points somewhere.

| Line | Job | Carries | Target | Variation |
|---|---|---|---|---|
| 1 | Thank the attorney and credit them | `{{ATTORNEY}}` | Under 30 words | HIGH |
| 2 | Name the show and sign off | `{{PODCAST_NAME}}` | Under 15 words | LOW by design |
| 3 | The reach-out tag | `{{STATE}}`, `{{FIRM_NAME}}`, `{{PHONE_NUMBER}}`, `{{WEBSITE}}` | Under 30 words | MEDIUM |

Roughly 60 words, 15 to 25 seconds. No speaker tag: the `INTERVIEWER` tag was cut 2026-08-18.

**The sign-off is not last, and that is deliberate.** Line 2 closes the show, then line 3 lands as a tag after it. "And remember" is the hinge that makes a line after the close sound natural rather than like the host forgot something. The contact details end up being the last thing the listener hears, without the episode ending on an ad.

Rendered, using the topical credit approach:

> **{{ATTORNEY}}**, thank you for your time. Nobody actually explains what a car accident case is really worth. You just did.
>
> That is it for this one. **{{PODCAST_NAME}}**. We will see you next episode.
>
> And remember, if you are in **{{STATE}}** and need a lawyer, reach out to **{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**.

Three more, one per remaining credit approach, live on the **Outro Variations - QA** tab of the prototype doc.

## Why these are generated and not frozen

They were frozen until 2026-08-18. Gabe: the outro has to read relatively unique on every episode while always hitting the same points.

Frozen strings guaranteed the points and guaranteed twelve identical episodes. A listener who works through a client's library hears the identical 60 words twelve times, which is the moment a show stops sounding like a person and starts sounding like a template. The fix is not to loosen the requirements, it is to move the guarantee from the wording to the beats. **The beats are gated. The wording is generated against them.**

**The banks are starting points, not menus.** Each line's bank shows the range that clears the bar. A generated line that satisfies the beats, the invariants and the rules is valid even if it appears nowhere in the JSON. A run that only ever picks bank entries verbatim is doing selection, which will visibly cycle across twelve episodes and defeats the point.

## Angle variants (Gabe, 2026-08-26)

Generation SHOULD produce one primary plus 3-4 alternate angles for each of the three lines, following this file's variation model: different credit clauses for line 1, different close beats around the podcast name for line 2 (all under fifteen words), different hinge phrasings for line 3 (all carrying the state, phone then website). Every alternate clears the same beats, invariants and gates as the primary, because the producer may swap any of them in verbatim from the tool. The alternates ride beside the payload (outro_alternates) and surface in the tool's caret menu; the producer picks the angle there, and a pick keeps the displaced line in the list, so no angle is ever lost.

## Line 1 - the thanks and the credit

**Required beats:** address them with `{{ATTORNEY}}`, thank them explicitly, and one credit clause that alludes to competence rather than announcing it.

**Five credit approaches**, each pointed at a different thing the attorney did. Full clause banks in `outro-banks.json`.

| Approach | Credits | When |
|---|---|---|
| **Topical** | The specific subject | Preferred whenever the topic phrase is concrete |
| **Reps** | Accumulated experience, no number | Safe on any episode |
| **Clarity** | The explaining, not the knowing | After a technical episode |
| **Candor** | The honesty | When they named a weakness or gave an unflattering number |
| **Depth** | The credential, via `{{YEARS_PRACTICING}}` | Sparingly |

**Topical is the strongest and should be the default when it is available.** It is the only approach whose clause cannot be reused on another episode, because it names what this episode was about. Every other approach produces a clause that would fit any episode of any show, which is exactly the sameness this redesign exists to remove. If the topic phrase is concrete, use it.

**Allude, do not gush.** The failure mode is obvious and it is the one an LLM reaches for first: "you're brilliant", "that was incredible", "one of the best in the state". All of it fails the "sounds normal" north star from `references/introduction.md`, and praise that big reads as paid rather than earned. Every approved clause credits a specific thing, which is why they land.

**Do not run Depth on an episode whose intro leaned hard on `{{YEARS_PRACTICING}}`.** Saying the number twice in one recording makes the credential sound like the only thing the firm has.

## Line 2 - the sign-off

**Required beats:** a phrase that signals the end, `{{PODCAST_NAME}}`, and a forward reference to a next episode.

**Variation is LOW here on purpose.** This is the sonic bookend to intro line 1, and repetition is most of its value. Rotate within the six-entry bank; only generate a new form once every entry has fired in the current season. This is the one line where sounding the same is the feature.

**"Produced by Case Engine" was cut 2026-08-18.** It is the firm's show. A production credit in the close puts our name in the client's mouth on their own podcast, the same inversion the no-guest-framing rule exists to prevent. CE attribution belongs in the show description and internal documents. It does not go on air. See `references/editorial-rules.md`.

**"We will see you next episode" on a season's last episode is still correct.** The library is continuous and episodes publish out of order. A special final-episode variant means the bookend is no longer a bookend.

## Line 3 - the reach-out

**Required beats:** a hinge opener, a geo qualifier carrying `{{STATE}}`, a neutral need clause, then `{{FIRM_NAME}}`, `{{PHONE_NUMBER}}` and `{{WEBSITE}}`.

**Assembled from four slots:** hinge, geo-and-need, verb, contact frame. Five by five by three by three is 225 combinations before any generation, which is why this line varies freely without ever risking the tokens.

**"Need a lawyer" is what makes this one line instead of four.** An earlier version opened with "If you were hurt", written for personal injury. It is nonsense on an estate planning show and describes the wrong person entirely on a criminal defense show. A four-trigger pattern set existed briefly to fix that. Gabe's phrasing retired it in one move: "in {{STATE}} and need a lawyer" is true of every client we will ever have, so the practice-area branch disappeared instead of being managed.

**The geo is `{{STATE}}`, never `{{CITY}}`.** Same rule as introduction.md line 2, same reason: S1 is state-governed, so one recording serves every city the firm covers. A city in the outro silently makes the whole long-form segment non-reusable, and the city blocks in S2 are where `{{CITY}}` lives. This is the single edit most likely to be made in good faith and it is why there is a gate on it.

**Two contact routes, once each, phone before website.** No address, no email, no social handle. A listener in a car can hold one number.

## Uniqueness

Uniqueness is enforced by comparing text against the client's prior episodes, not by bookkeeping indices. An index can differ while the line is effectively the same, and the same index can carry different text - the text is what a listener hears, so the text is what gets checked.

- **Line 1 and line 3 must not repeat, near-verbatim, any prior episode for this client.**
- **Line 2 is EXEMPT.** It is the sonic bookend and repetition is most of its value. This is the one line where sounding the same is the feature.
- **The banks are calibration, not a menu.** They show what good sounds like. Sampling them at random produces exactly the generic credit this file warns about; write the line, then check it against the bank for register.
- **Uniqueness is necessary, not sufficient - vary the SHAPE too.** Ten differently-worded lines built on one skeleton read as one line to anyone consuming the library in order. Check this episode's line 1 and line 3 against the last three episodes for the same structure, not just the same words.
- **Only claim what the firm has told us.** Line 1's credit clause describes the attorney's performance in the episode, which is always safe. Line 3 carries no claims. Anything that asserts a fact about the practice belongs in the introduction's line 3, under its sourcing rule.
- **The arbiter is the read-aloud.** If it sounds like a person and it is not what a previous episode said, it passes. No quota, no rotation counter. Every mechanical rule of that shape tried on this pipeline made the output worse by forcing it.

*Retired 2026-08-21 (Gabe): `scripts/outro-rotation.py` and the metadata fields `outro_line1_approach`, `outro_line1_stem_index`, `outro_line2_index`, `outro_line3_slots`. Superseded by the text comparison above.*

## Delivery - contractions and flow

The banks are authored without contractions. **The delivered line uses them.** "That is it for this one" reads stiff against an introduction written in contractions; "That's it for this one" is what a person says. The banks stay as they are - canonical wording and calibration - and the host contracts them naturally, which the "host says all of it in their own words" rule already permits.

**Line 1 is two sentences, not three.** Address-and-thank, then ONE credit clause. A credit split into two clauses says the same thing twice: "That is genuinely hard to explain simply. You made it sound easy." becomes "That's genuinely hard to explain simply, and you made it sound easy."

**Match the credit clause to the episode.** Clarity fits a process episode, candor fits a subject attorneys usually dodge (case value, fees, odds), depth fits an episode carried by experience. A generic credit is the tell that the bank was sampled at random.

**Line 3's hinge has to earn the line.** Line 2 says goodbye and line 3 keeps talking, so the hinge is what makes that sound intentional rather than tacked on. "And before you go," and "One more thing," acknowledge the goodbye; "And remember," does not.

**No em dashes anywhere.** CE house rule. A hinge that wants a dash takes a comma.

## Rules

- **Do not recap.** The most common thing a host adds unprompted, and the reason `outro_note` says so out loud. A recap tells the listener the episode is over before it is, and the summary is always worse than the thing it summarizes.
- **One reach-out. Never two.** Two reads as a hard sell and undoes the authority S1 just spent 20 minutes building.
- **Do not stack a CTA.** No subscribe, like, follow, review or bell. The show is a search asset, not a channel play, and the CTA stack is the loudest possible AI-podcast tell.
- **Do not thank the audience for listening.** It is a radio reflex. Line 1 thanks the person who did the work.
- **Do not tease the next episode.** Publish order changes and a stale tease outlives the episode it was recorded for.
- **The outro closes S1, not the recording session.** S2 is a separate session in a different register. Never reference the short-form block, and never let the host close S1 twice because S2 is still to come.
- **The host says all of it in their own words.** Same rule as the introduction. Line 3's tokens have to be said correctly; the phrasing around them does not have to be read.

## Do not

- **Do not add an episode number.** The intro does not carry one either. Numbers date an evergreen asset.
- **Do not frame the attorney as a guest.** "Thanks for coming on" fails the guest gate. It is their show, and the outro is historically where this violation appears.
- **Do not name Case Engine anywhere in the section.**
- **Do not put `{{CITY}}` in line 3.**
- **Do not use a superlative, a ranking or an award in the credit.**
- **Do not use `.format()` on any of these strings.** They carry `{{PLACEHOLDER}}` tokens and Python's `str.format` collapses doubled braces to single ones, silently destroying every token. Substitute with `.replace()`.

## Gates

- **OC-1** Exactly three spoken lines, in the order thanks, sign-off, reach-out. No speaker tag - the `INTERVIEWER` tag was removed from the outro 2026-08-18. The outro note above it already says who is speaking, and a tag on a three-line close is clutter.
- **OC-2** Every required beat for every line is present. Beats are gated; wording is not.
- **OC-3** Line 1 carries `{{ATTORNEY}}` exactly once and names a credit approach recorded in metadata. A clause that credits nothing specific FAILS.
- **OC-4** `{{PODCAST_NAME}}`, `{{STATE}}`, `{{FIRM_NAME}}`, `{{PHONE_NUMBER}}` and `{{WEBSITE}}` each appear exactly once, all bold.
- **OC-5** Zero occurrences of "Case Engine" and zero occurrences of `{{CITY}}` in the rendered section.
- **OC-6** Zero guest framing, zero recap, zero subscribe or follow CTA, zero superlatives, zero em dashes.
- **OC-7** Rotation satisfied against the two preceding episodes, and all four rotation fields written to `metadata.json`.
- **OC-8** `outro_note` renders byte-identical to `references/statics.json`. It is the one constant left in the section.
- **OC-9** The document-level read-through gate passes on all three lines. Read them aloud, in order, immediately after the Introduction, so cross-section repetition is audible. This is the gate that catches a line which satisfies every count above and still is not a sentence anybody would say. See `steps/08-qa.md` tier 4.

## Where this came from

The three-line shape mirrors `references/introduction.md`, out of the two 2026-08-14 Gabe and Cyle calls. The outro was never workshopped there; it was written as boilerplate and frozen, and it got four things wrong. It assumed every client was a personal injury firm. It signed off with our name instead of theirs. It thanked the attorney without ever crediting them, wasting the one moment in the document where the host is allowed to have an opinion. And being frozen, it would have read identically on all twelve episodes of every show we ever built. All four were fixed 2026-08-18.
