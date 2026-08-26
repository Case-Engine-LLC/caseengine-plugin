# The Attribute Block

The bullets under `ATTORNEY RESPONSE` in S1. Read by `steps/04-segment-1.md`. The third of the three S1 reference docs, alongside `references/introduction.md` and `references/outro.md`.

The attribute block replaced the legacy statute-grounded bullets. It is the answer to one question: **what is a person actually trying to find out before they call anyone?**

## This is an inversion of the research, not a copy of it

`pod-1D-attribute-research` produces a **catalog**. Its unit is *the ask a client can put to the firm* - a screening question, gated through the four gates in `pod-1D-attribute-research/references/attribute-rules.md` (firm property, screening instruction, discriminating, distinct in substance), each row carrying a checkable ask and verbatim evidence.

The ROS needs the same attributes pointed the other way. Its unit is **what the attorney covers when answering**.

| | Catalog (`pod-1D`) | This block |
|---|---|---|
| Unit | The question a client would ask | What the attorney covers |
| Ordered by | How consistently the attribute surfaced | What an attorney naturally covers, credentials through logistics |
| Read by | A researcher, a database | An attorney, top to bottom, while somebody is talking |
| Purpose | Decides what is a signal | Decides what belongs on air |

**They are not the same list, and neither is a subset of the other.** The catalog decides what counts as a signal. The script decides what belongs on air.

## The rule that governs everything else

**No question ever appears in this block.** Not one.

The catalog stores questions because a researcher needs a checkable ask. The moment a question lands on this page, the attorney reads it aloud, and the block becomes the checklist interrogation that v2 exists to replace. This is the specific failure that made earlier drafts of these blocks sound like worksheets.

Wrong, and this is the form currently sitting in the live prototype doc:

> **Trial willingness.** Have you taken these to trial, or do you only settle? If you are a trial firm, say so early and say it plainly.

Right:

> **Trial willingness.** Cases you actually tried rather than settled, and what that changes at the table before a jury is picked.

Same attribute, same substance. The first tells the attorney what a client would ask. The second tells the attorney what to say. Only the second belongs here.

## Building the block

**Source order.**

1. `pod-1D-attribute-research` output for this practice area and market. **Confirmed.**
2. `references/attributes/attributes-fallback.json` - the 2026-08-14 snapshot. **Inferred**, and flagged as such in `metadata.json` with its pull date.

**Transform each catalog row into a response-guidance bullet.**

- **Bold lead-in** - two or three words, and written for THIS episode rather than reused from the last one. `**Death cases tried.**` on a wrongful-death episode, `**Tried a failure to yield.**` on a crosswalk one. See "The lead-in is the whole block, visually" below.
- **What to cover** - one sentence, plain language, in the words a person uses. Concrete enough that the attorney knows what a good answer contains.
- Nothing else. No question, no source count, no rank, no verbatim quote, no "why it lands" note. All of that is catalog metadata and it stays in the catalog.

## The lead-in is the whole block, visually

**The bold lead-in is the only bold text in this block, so it is the only thing a reader's eye lands
on.** The detail sentence is read once, by the attorney, in prep. The label is what everyone sees
every time the document is opened.

That makes a stable label set a library-level failure even when every sentence underneath is
episode-specific. On 2026-08-18 a ten-episode Eberst run shipped with nine of twelve lead-ins
byte-identical across all ten documents. Every AT gate passed. The detail sentences had already been
rewritten per episode. The client's reaction on opening them was that the episodes were all the same,
and he was right, because the nine repeated labels were the only part of the block he was actually
reading.

The catalog row is stable. **Its name on the page is not.** Trial willingness is
`**Death cases tried.**` on a wrongful-death episode, `**Tried against a national carrier.**` on a
trucking-regulation one, and `**Tried in front of a jury.**` on a motorcycle one. Same row, same
substance, named for the episode it sits in. Record the row it derives from in `metadata.json`, not
on the page.

This is the same failure the outro banks exist to prevent, one section earlier in the document. A
listener who works through a library hears the identical outro twelve times; a client who opens a
library sees the identical attribute block twelve times. Both are the moment the work stops looking
generated per episode and starts looking generated once.

**Order by what an attorney naturally covers, not by research rank.** Credentials first, logistics last. The catalog is ranked by how consistently each attribute surfaced, which is the right order for a researcher comparing pulls month over month and the wrong order for somebody reading down a page mid-sentence.

**Ten to twelve bullets.** Past that the attorney stops treating it as a shape and starts treating it as a list to get through.

## Fee structure is a deliberate exception

Fee structure fails `pod-1D`'s **discriminating** gate. Every personal injury firm works on contingency, and the answer engines say so outright, so it does not discriminate between firms and it does not belong in the catalog.

**It stays in this block anyway.** A listener still needs to hear how the firm gets paid, what happens if they lose, and who fronts records, filing fees and experts. That makes it bad research and necessary script.

Expect this asymmetry to recur. When a catalog row is missing something obviously worth saying on air, the catalog is probably right and this block still needs the bullet. Do not "fix" the catalog to match.

## Two findings that must survive every edit

Both invert what an attorney's instinct will be on the day, which is exactly why they belong on the page instead of in someone's head.

- **Reviews and awards rank BELOW verifiable bar standing.** ChatGPT says so explicitly: license and disciplinary history are more meaningful than ratings alone. Every attorney will want to lead with reviews.
- **Naming a weakness builds more trust than making a promise.** Saying what would make the case difficult reads as a positive signal; guaranteeing a number reads as a red flag.

## How it is delivered on air

- **Hit anywhere, in any order, in the attorney's own words.** Not a checklist to read, not a question list in disguise, not a sequence.
- **The interviewer holds the same list** and fills gaps naturally at the end, after the attorney has run.
- The block sits under `ATTORNEY RESPONSE` in the Introduction. There is no `Attributes to Hit` heading - that was retired 2026-08-17 along with the `Internal Notes` block.

## Rules

- **No jargon.** Same as everywhere else in this document: no statute numbers, no case citations, no element names. "How long it sat there is the whole argument", never "constructive notice".
- **No source counts on the page.** "4 of 4 sources, high signal" was cut 2026-08-17. Gabe: "That's just filler." Provenance lives in `metadata.json`.
- **No superlatives and no marketing language.** Aggressive, nationally recognized, highly personalized, massively reviewed. `pod-1D` Gate 2 kills these in the catalog; they must not reappear here through the transform.
- **Attribute names are plain, not branded.** "Time in the market", not "Proven Local Legacy".
- **A fallback run is Inferred, never Confirmed.** Flag it, date it, and re-pull when `pod-1D` output exists for the practice area and market.

## Gates

- **AT-1** Zero question marks in the block. This is the one that matters most.
- **AT-2** Ten to twelve bullets, each a bold lead-in plus one sentence of what to cover.
- **AT-3** Every bullet traces to a catalog row or a fallback entry, except fee structure which is the documented exception.
- **AT-4** Ordered credentials through logistics, not by research rank.
- **AT-5** Zero source counts, ranks, confidence markers or verbatim research quotes rendered on the page.
- **AT-6** Zero jargon, zero superlatives, zero marketing adjectives.
- **AT-7** Bar standing appears above reviews wherever both are present, and a "name the hard part" bullet is present.
- **AT-9** No bold lead-in and no detail sentence repeats across episodes of the same show. Check against the prior episodes' payloads before shipping. Rewriting the sentence while keeping the label FAILS - the label is what the eye lands on.
- **AT-8** `metadata.json` records `attribute_source` as `pod-1D` or `fallback`, with the pull date and confidence.

## Open

- **The live prototype doc's attribute block is in the OLD question-carrying form** and contradicts AT-1. It needs rewriting to response guidance before it is used as a generation example.
- **The fallback set will drift.** `attributes-fallback.json` is a 2026-08-14 snapshot of live Google AI Overview and ChatGPT output. Answer engines move. Re-pull via `pod-1D` and log what moved; the drift is itself a signal worth keeping.
- **The Houston extraction test raised one unresolved ruling.** Appellate capability, expert network and language access appeared only as comparison-table "Key Advantage" items, which describe firms rather than instructing the reader. They were passed on the logic that a side-by-side comparison exists to help someone choose. A ruling invoked twice belongs in `pod-1D`'s rule file. Worked example archived at `references/examples/_archived-doc-tabs/attribute-extraction-test-houston.md`.

## Beat grouping (Gabe, 2026-08-26)

The ask's question-shaped beats are the chapters of the attorney's answer, and the attributes are the depth inside each chapter. Generation assigns every attribute to exactly one beat of the primary ask (unassignable ones go in a final labeled group, never dropped), and the grouping is stored beside the flat attribute list (segment_1.beat_groups) so nothing downstream of the flat list breaks. When the producer swaps or edits the ask in the tool, the attributes stay untouched and only the grouping is re-derived against the new ask's beats; if no beats can be derived, the tab and the Doc fall back to the flat list.
