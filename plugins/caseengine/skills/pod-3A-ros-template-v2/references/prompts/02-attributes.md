# 02 - Attributes

> **References:** `references/attributes.md` is the format of record for this block - why it is an
> inversion of the `pod-1D` catalog rather than a copy of it, the fee-structure exception, the two
> findings that must survive every edit, and gates AT-1 through AT-9. Read it before touching
> anything here. This file carries only what a generation run needs.

The bullets under `ATTORNEY RESPONSE` in S1. Ten to twelve of them, each a bold lead-in plus one
sentence. Everything in this block is GENERATED per episode; there is no constant in it.

## The rule that governs everything else

**The block stores what the attorney COVERS, never the question a client would ask.** Not one
question mark, anywhere in it. `AT-1` is the gate and it is the one that matters most.

`pod-1D-attribute-research` produces a **catalog** whose unit is the ask a client can put to the
firm, because a researcher needs a checkable ask. This block is the same attributes **pointed the
other way** - what the attorney covers when answering. The two are not the same list and neither is
a subset of the other. The moment a question lands on this page the attorney reads it aloud, and the
block becomes the checklist interrogation that v2 exists to replace.

Wrong:

> **Trial willingness.** Have you taken these to trial, or do you only settle? If you are a trial
> firm, say so early and say it plainly.

Right:

> **Trial willingness.** Cases you actually tried rather than settled, and what that changes at the
> table before a jury is picked.

Same attribute, same substance. The first tells the attorney what a client would ask. The second
tells them what to say.

## Inputs
- **Preferred:** the `pod-1D-attribute-research` artifact for this practice area and market. **Confirmed.**
- **Fallback:** `references/attributes/attributes-fallback.json`, the 2026-08-14 snapshot.
  **Inferred**, and flagged as such in `metadata.json` with its pull date.

## What is STATIC here (do not generate)
Nothing. **`attr_intro`, `attr_note_internal` and `attr_sources_internal` were all retired
2026-08-17** and now sit in `references/statics.json -> retired`; anything still rendering them is
stale. The `Attributes to Hit` heading was retired with them - the bullets sit under
`ATTORNEY RESPONSE` with nothing labelling them.

## Render order
1. `ATTORNEY RESPONSE` speaker tag, gray italic (emitted by `01-introduction.md`)
2. The attribute bullets, ten to twelve, in order

Nothing above them, nothing between them, nothing after them until `## Outro`.

## Prompt

**Transform each catalog row into a response-guidance bullet.** Two parts and nothing else:

- **Bold lead-in** - two or three words, plain rather than branded, and **written for THIS
  episode**. Never "Proven Local Legacy", and equally never a stock label carried over from the last
  episode. The lead-in is the only bold text in the block, so it is the only thing a reader's eye
  lands on: identical lead-ins make twelve different episodes scan as one page even when every
  sentence underneath differs. Trial willingness becomes `**Death cases tried.**` on a wrongful-death
  episode and `**Tried in front of a jury.**` on a motorcycle one. Same catalog row, same substance,
  named for the episode it is in.
- **What to cover** - one sentence, plain language, in the words a person uses, concrete enough that
  the attorney knows what a good answer contains.

No question, no source count, no rank, no verbatim research quote, no "why it lands" note. All of
that is catalog metadata and it stays in the catalog. Provenance goes in `metadata.json`.

**Order by what an attorney naturally covers, credentials first and logistics last.** Do NOT order by
research rank. The catalog is ranked by how consistently each attribute surfaced, which is the right
order for a researcher comparing pulls month over month and the wrong order for somebody reading down
a page mid-sentence.

**Ten to twelve bullets.** Past twelve the attorney stops treating it as a shape and starts treating
it as a list to get through.

**Include fee structure even though the catalog will not carry it.** It fails `pod-1D`'s
discriminating gate - every personal injury firm works on contingency and the answer engines say so
outright - so it is bad research and necessary script. A listener still needs to hear how the firm
gets paid, what happens if they lose, and who fronts records, filing fees and experts. This is the
documented exception to AT-3.

Expect the asymmetry to recur. When a catalog row is missing something obviously worth saying on
air, the catalog is probably right and this block still needs the bullet. Do not "fix" the catalog
to match.

**Carry the two findings.** Both invert what an attorney's instinct will be on the day, which is why
they belong on the page rather than in somebody's head. They are now carried by the bullets
themselves, not by a retired constant:

- Bar standing appears **above** reviews and awards wherever both are present. ChatGPT says so
  explicitly - license and disciplinary history are more meaningful than ratings alone - and every
  attorney will want to lead with reviews.
- A **"name the hard part"** bullet is present. Saying what would make the case difficult reads as a
  positive signal; guaranteeing a number reads as a red flag.

**Record the source.** `metadata.json -> attribute_source` is `pod-1D` or `fallback`, with the pull
date and the confidence. A fallback run is **Inferred, never Confirmed** - flag it, date it, and
re-pull when `pod-1D` output exists for this practice area and market.

## Rules
Full rule set in `references/attributes.md` -> "Rules". The ones that bite most often:

- **No question marks.** AT-1. Everything else in this file is downstream of it.
- **No jargon.** "How long it sat there is the whole argument", never "constructive notice". No
  statute numbers, no case citations, no element names.
- **No source counts on the page.** "4 of 4 sources, high signal" was cut 2026-08-17. Gabe: "That's
  just filler."
- **No superlatives and no marketing language.** Aggressive, nationally recognized, highly
  personalized, massively reviewed. `pod-1D` Gate 2 kills these in the catalog; they must not
  reappear here through the transform.
- **Hit anywhere, in any order, in the attorney's own words.** Not a checklist to read, not a
  sequence. The interviewer holds the same list and fills gaps naturally at the end, after the
  attorney has run.
- **No em dashes.**

## Examples

### GOOD
The same four catalog rows, rendered for two different episodes. Note that neither the labels nor the
sentences repeat.

Wrongful death from a truck crash:

> **Death cases tried.** Fatal cases you actually took to a jury, and what that changes when a
> carrier is pricing the file.
>
> **License and record.** Your license and disciplinary history, which a family can verify
> themselves in about a minute.
>
> **What could go wrong.** What would make this case difficult, including when the person who died
> was partly at fault.
>
> **How you get paid.** The percentage, whether it rises if you file suit, who funds an
> investigation this size, and what happens if you lose.

Right-of-way and crosswalk law:

> **Tried a failure to yield.** Cases you took to a jury, and what they did with a driver who simply
> did not give way.
>
> **Standing over ratings.** Your license and disciplinary history, which is public and checkable in
> a way a rating is not.
>
> **When the crossing was wrong.** When the person genuinely was not crossing lawfully, and say it at
> the start rather than the end.
>
> **Your fee and the costs.** The percentage, whether it rises if you file suit, who pays to get the
> footage and the road data, and what happens if you lose.

Every bullet is a bold lead-in plus one sentence of what to cover. Zero question marks, zero counts,
zero adjectives. Bar standing sits above any reviews bullet, the hard-part bullet is present, and fee
structure is here despite failing `pod-1D`'s discriminating gate.

### BAD
> **Trial willingness (strongest signal, 4 of 4 sources).** Have you taken these to trial, or do you
> only settle? Google asks it in those words.
>
> **Reputation.** Reviews, testimonials, and awards. Mention your five-star ratings.

Fails four ways: the source count renders on the page; the first bullet is phrased as the client's
question rather than what the attorney covers, so the attorney reads it aloud; "Reputation" is a
category label rather than a named attribute; and reviews are presented as the credential when bar
standing outranks them in every pull.

A second BAD, and the one that survives every other gate. Observed live on 2026-08-18 across ten
Eberst episodes:

> E5:  **Trial willingness.** ...   **Verifiable standing.** ...   **Honest assessment.** ...
> E9:  **Trial willingness.** ...   **Verifiable standing.** ...   **Honest assessment.** ...
> E12: **Trial willingness.** ...   **Verifiable standing.** ...   **Honest assessment.** ...

Nine of twelve lead-ins were byte-identical across all ten episodes. Every AT gate passed, every
detail sentence underneath had already been rewritten per episode, and the client still read the
blocks as the same page ten times, because the bold label is the only thing the eye lands on. This is
what AT-9 exists to catch. Rewriting the sentences does not fix it; the labels have to change too.

## Gates
Gates for this section are **AT-1 through AT-9** in `references/attributes.md` -> "Gates". They
supersede the two competing A-1 through A-6 sets that were in this file, which were written when
`attr_intro`, `attr_note_internal` and `attr_sources_internal` were still constants and the counts
still rendered.

## Feedback
- **AT-1 fails:** a bullet is phrased as the client's question. Rewrite it as what the attorney
  covers - same attribute, same substance, pointed the other way. Do not just delete the question
  mark; the sentence is still a question underneath.
- **AT-2 fails:** under ten or over twelve, or a bullet is missing its bold lead-in or ran to two
  sentences. Fix the count first, then the shape.
- **AT-3 fails:** a bullet traces to nothing. Either find its catalog row or cut it - the one
  documented exception is fee structure.
- **AT-4 fails:** the block is in research-rank order. Reorder credentials through logistics.
- **AT-5 fails:** a count, rank or research quote reached the page. Move it to `metadata.json`. The
  bullet is what gets read; the count is provenance.
- **AT-6 fails:** jargon, a superlative or a marketing adjective survived the transform. Rewrite in
  the words a person uses.
- **AT-7 fails:** reviews outrank bar standing, or there is no "name the hard part" bullet. Both
  invert an attorney's instinct, which is exactly why they are gated rather than left to the run.
- **AT-9 fails:** a lead-in or a detail sentence repeats from another episode of the same show. Do
  not settle for rewriting the sentence - the label is what the eye lands on, so the label is what
  has to change. Name the row for the episode it is in.
- **AT-8 fails:** an unmarked fallback is the dangerous case - a reader assumes it was researched for
  this market when it was not. Record `attribute_source`, the pull date and the confidence.
