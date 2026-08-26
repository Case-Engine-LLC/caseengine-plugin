# Editorial Rules

Cross-cutting content rules. Every section step inherits these; they are not restated per step. Gated in `steps/08-qa.md`.

## No jargon. There is no exempt section.

**Banned everywhere above the appendix:** statute numbers (`O.C.G.A. Section 51-12-33`, `CCP 335.1`), case citations (`Rowland v. Christian`), rule names (`Daubert`, `MCS-90`), section symbols, and legal element names as such (`duty of care`, `constructive notice`, `comparative negligence`, `res ipsa loquitur`, `sovereign immunity`).

**Required instead:** the same substance in the words a person uses.

- "They will say you should have been watching. In California that reduces your case, it does not end it."
- "How long it sat there is the whole argument."
- "The video gets recorded over, often within days."

**The test:** read the line aloud. If it sounds like a citation or a law-school outline heading, it is wrong. Cyle, 2026-08-14: "nobody's going to search 'what is duty of care'."

**Where the jurisdiction knowledge went.** It still informs generation - the entity map tells the writer what is true - it just never reaches the page as terminology. The attorney gets the consequence, not the rule.

**The appendix is the one unavoidable exception, and it is not an exemption.** It carries n-gram rows verbatim and some rows contain statute references because research wrote them that way. Verbatim means verbatim. Scope the scan above the appendix heading; never edit a bank row to make the scan pass.

Earlier drafts allowed citations inside a `Producer Notes` block and ran an inverse check that they landed there. That section is gone, so there is nothing to contain and nothing to inverse-check. The rule is simpler and stricter now: zero, everywhere above the appendix.

## The attorney is never "the guest." It is their podcast.

**Banned:** "my guest", "our guest", "today's guest", "joining us", "thanks for coming on", "welcome to the show" directed at the attorney, and any construction framing them as a visitor.

**Why:** the show is co-branded with the firm - `{{PODCAST_NAME}}` with `{{ATTORNEY_NAME}}`. The attorney owns it. The CE interviewer is the one asking questions on someone else's show, so guest framing inverts the relationship and quietly undercuts the authority the whole format exists to establish. Gabe, 2026-08-14.

**Allowed:** name them. "Welcome back to `{{PODCAST_NAME}}` with `{{ATTORNEY_NAME}}`." "Thank you for your time."

This one has already been violated twice by boilerplate that read fine in isolation - the outro note said "Thank the guest" for three days. Grep for it rather than trusting a read.

## US English, and it is spoken English

Every one of these documents is said out loud by an American host to an American
listener about American law. A Britishism is an immediate tell, and it survives every
other gate because it is spelled correctly and parses fine.

**Banned above the appendix:** British spellings (`licence`, `defence`, `favour`,
`centre`, `organisation`, `realise`, `travelled`, `judgement`, `kerb`, `grey`,
`afterwards`, `towards`, `whilst`, `amongst`), British vocabulary (`pavement` for
sidewalk, `motorway`, `car park`, `lorry`, `petrol`, `solicitor`, `windscreen`,
`fortnight`, `roundabout`), British idiom (`caught out`, `at speed`, `straight away`,
`work out` meaning figure out, `in hospital`, `in future`, `different to`,
`take a decision`, `reckon`, `disbursements`, `public body`), and British collective
agreement (`the family are`, `the firm are`, `the jury are` - all take a singular verb).

`pavement` is the one that actually bit. In British English it means sidewalk, so
"an e-bike belongs where a bicycle belongs, which is not the pavement" told Florida
riders to stay off the road. Correct spelling, clean grammar, opposite of the law.

**Contract, because people do.** "That is the episode" and "You do not edit it" are
written English. Said on camera they are a press release. Every generated line
contracts; the three STATIC strings do not, because they are gated byte-identical.

**The appendix is exempt and is never edited to make the scan pass.** Same rule as
the jargon scan: scope above the appendix heading.

## Research is the palette, not the shopping list

Research captures the FULL topic domain. The template layers in the slice that serves THIS episode's goal - it does not mechanically consume everything upstream produced. A single research run serves many episodes in a series.

| Episode goal | What it weights |
|---|---|
| Authority / education | Years and case volume in the prompt; the search-phrase tail questions in S2 |
| Lead generation | More attribute questions in S2 - cost, who handles it, response time; the plug carries the emphasis |
| Differentiation | Trial willingness and honest assessment lead the attribute block |
| Narrative / story | The examples clause of the prompt gets the weight |
| Conversion | Fee and expense detail leads; the close is mostly CTA |

Default is Authority when unspecified. Recorded in metadata as `episode_goal`.

## House style

- No em dashes anywhere. Plain hyphens.
- No numbered lists in ClickUp-bound content.
- Dates `MM-DD-YYYY` in the document, `DD-MM-YYYY` in ClickUp.
- No emojis.
- The document is spoken aloud more than any other CE deliverable. Anything that only works on the page fails.
