# Document Structure

The locked shape of a v2 ROS Template. `pod-3B-client-ros` reads this exact shape to populate a firm's copy, so structural drift breaks the populate step. Read by `steps/07-render.md`, gated by `steps/08-qa.md`.

Source of truth: the [prototype doc](https://docs.google.com/document/d/1Bv-EWc7HBtKqc09XEfQnBIfSOdm6m4Tc-kJNw5uKErk/edit), as of 2026-08-17.

## The shape

```
Cover page                          per references/cover-spec.json, page break after

# S1: Long-Form (15-30m)            H1, CE Blue, starts its own page
  ## Introduction (45-60s)          H2, CE Dark - the duration is part of the heading
     welcome                        STATIC, line 1, the sonic marker
     setup                          GENERATED, line 2, one of introduction.md's ten patterns
     credential turn                GENERATED, line 3, one credential frame
     the prompt                     GENERATED, line 4, credential-led, exactly one
  ## ATTORNEY RESPONSE              H2, CE Dark
  attribute bullets                 from the attribute set, bold lead-in each
  ## Follow-ups                     H2, CE Dark - INTERVIEWER NOTES, never read on air
     note line                      STATIC, italic direction
     first bullet                   STATIC, hard-coded, byte-identical every episode
     case-study bullets             GENERATED, topic-specific, at least one
  ## Outro                    H2, CE Dark
     outro note                     STATIC, host direction
     thanks / sign-off / reach-out  GENERATED, three lines, no speaker tag

# S2: Short-Form (60-90s)           H1, CE Blue, starts its own page
  ## Location: {{CITY}}     H2, one per location
     **Q{N}: question**             best 8-10 per location, bold in full
        - [{Label}]{.underline}:    2-4 attorney bullets under each, 3 default
          detail                    label underlined, not bold
                                    nothing else renders under a question

# Appendix: Source Question Bank    H1, CE Blue, starts its own page, INTERNAL
     internal note + rows 1..M      verbatim from the n-gram table
```

## Rules

- **S1 is a complete recording.** Intro through outro, start to finish, then stop. S2 is a separate session in a different register - that is why the outro closes S1 rather than following S2.
- **Exactly one prompt in S1.** The single most likely regression across future edits is someone adding a second and third prompt because the silence feels risky. Adding prompts converts v2 back into legacy with fewer questions.
- **Page breaks:** cover, S1, S2, and the appendix each begin a new page. A section may run onto a second page - that is fine and expected for S1 and S2. What is not fine is a paragraph carrying an inherited break it did not ask for.
- **Heading colors:** H1 section headers CE Blue. H2 CE Dark. Never a blue H2.
- **`ATTORNEY RESPONSE` is an H2 in CE Dark**, changed 2026-08-18 from a gray italic speaker tag. It is the handoff point in the document and the only thing separating the prompt from the attribute bullets, so it carries heading weight. There are no gray italic speaker tags left; the outro's `INTERVIEWER` tag was cut the same day.
- **Bold** carries the prompt, every placeholder, the attribute bullet lead-ins, and each Short-Form question IN FULL. Populated values stay bold.
- **Underline** carries the Short-Form bullet labels and entity runs, as pandoc `[text]{.underline}`, never HTML `<u>`. A Short-Form bullet label is underlined and never bold, so the question keeps the only bold weight in the block.

## Retired - must not come back

Cut deliberately. Reintroducing one is a format regression, not an improvement. The QA gate greps for these.

| Section | Cut |
|---|---|
| `How This Episode Runs` | 2026-08-14 |
| `Producer Notes` (any form) | 2026-08-14 |
| `The Lead-In` / `The Prompt` as headings | 2026-08-14 |
| `Interviewer: Live Checklist and Follow-Ups` | 2026-08-14 |
| `Co-Host Notes` | 2026-08-14 |
| `Geo Rule` and per-question geo tag lines | 2026-08-14 |
| Per-question answer-guidance notes phrased as instruction to the reader | 2026-08-14 |
| Per-question time budgets | 2026-08-14 |
| Co-host setup line before a Short-Form question | never in v2 |
| `Internal Notes (not read on air)` and everything under it - the three moves, both findings lines, the source-consistency counts, the need-to-know bullets | 2026-08-17 |
| `Attributes to Hit` as a heading | 2026-08-17 |
| The two short-form mode notes | 2026-08-17 |
| `Alternate introductions` block | 2026-08-17 |

The interviewer and co-host guidance did not evaporate when it was cut - it lives in `## INTERNAL -> Production notes` and reaches people through `pod-3C-client-guide`, which is coaching, not a recording script.

## Open

- **RESOLVED 2026-08-18: the setup paragraph is its own paragraph.** The live prototype doc carries four separate Introduction paragraphs and always did; what was wrong was `statics.json` -> `welcome`, which had merged lines 1 and 2 into one frozen constant. That merge froze the turn verb `introduction.md`'s ten line-2 patterns exist to vary, and it is why this question looked open. `welcome` is now line 1 only. The payload field is `segment_1.setup`, formerly the badly named `cold_open`.
- **The attribute bullets have no heading.** They currently sit under `## Introduction` with nothing labelling them, so on the page they read as a continuation of the prompt.
