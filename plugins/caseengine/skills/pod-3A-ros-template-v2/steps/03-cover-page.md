# Step 03 - Cover Page

> **Exec:** deterministic - assembles resolved values, generates no prose
> **Assets:** `references/cover-spec.json` (block order, sizes, colors, logo id, gates)

## What

The branded opening page every CE ROS Template carries: logo, `Run of Show`, the episode title, one topic-and-city line, and the attribution line. Nothing here is written for the episode - every value is already resolved by the time this step runs, so the step's whole job is placing known strings in the locked order. Good output is a cover that is page 1 by itself, with S1 starting on page 2.

## Inputs

- `episode_title` (str) - from the PUBLISHED Topic Plan Doc, verbatim. Never from a local `topic-plan-*.json` mirror.
- `topic` (str) - the episode subject; renders through `{{TOPIC}}`.
- `city` (str) - the Episode geo target city; renders through `{{CITY}}`. Omitted at Topic Only scope.
- `cover_spec` - `references/cover-spec.json`, read at run time. Never inline these values into a step or a script.
- `logo` - Drive id from the spec, resolved against the Case Engine Branding folder.

## Procedure

1. **Load the spec** [deterministic] - read `references/cover-spec.json`. The block list IS the render order; do not reorder, and do not add a block that is not in it.
2. **Emit the text blocks** [deterministic] - walk `blocks` in order, applying each block's size, weight, and color token. Everything is centered Roboto. `bold_spans` bolds only the named substrings, leaving the separator plain.
3. **Insert the logo** [deterministic] - a separate API call after the text batch lands, at 180pt. It is the piece most likely to silently not appear, which is why validation checks for the inline object rather than assuming the call worked.
4. **Page break** [deterministic] - the last block. S1 must open on its own page.

## Template

```
                         [ CE logo, 180pt ]

                            Run of Show                     CE Blue 24pt bold
              {episode_title}                               CE Dark 18pt bold

                   {{TOPIC}}  |  {{CITY}}                   CE Dark 14pt, tokens bold

                      Prepared by Case Engine               11pt
                                                            [page break]
```

## Examples

**GOOD**

```
Run of Show
What Your Inland Empire Car Accident Settlement Is Actually Worth
{{TOPIC}}  |  {{CITY}}
Prepared by Case Engine
```

The episode title is the real title from the Topic Plan. The topic line is one line with two bold tokens. Nothing names the firm.

**BAD**

```
Run of Show
What Your Inland Empire Car Accident Settlement Is Actually Worth
Topic: {{PRACTICE_AREA}}
Location: {{CITY}}
Prepared for Morgan & Morgan
```

Three defects. The labelled `Topic:` / `Location:` pair is the pre-2026-08-17 shape and was replaced by the single line. `{{PRACTICE_AREA}}` on the cover says "car accidents" where the cover wants the episode's subject, which is what `{{TOPIC}}` is for. And the firm name has no business on a template that is meant to serve every firm recording this episode - that is a tokenization failure, not a cosmetic one.

## Outputs

```
cover_page: {
  episode_title: str,
  topic_line: "{{TOPIC}}  |  {{CITY}}",   # city half dropped at Topic Only scope
  logo_present: bool,
  page_break_after: true
}
```

## Validation

- Every block in `cover-spec.json` rendered, in spec order, with no additions.
- The logo inline object exists at 180pt. A missing logo FAILS - do not accept a cover without it.
- `Run of Show` is CE Blue 24pt bold; the episode title is CE Dark 18pt bold; H2-level and below are never CE Blue.
- The topic line is a single line, both tokens bold, separator plain.
- Zero hard-coded firm, attorney, city, or state names.
- The cover occupies page 1 alone and S1 begins on page 2.

## Failure modes

| Failure | Exit behavior | Routes to |
|---|---|---|
| Logo call returns no inline object | Retry once, then fail the step - never ship a coverless-logo template | this step |
| `episode_title` came from a local mirror, not the published Topic Plan Doc | Stop; re-resolve against the Doc, which always wins | `steps/01-prerequisites.md` |
| Topic Only scope with a city in the topic line | Drop the city half and the separator, leaving `{{TOPIC}}` alone | this step |
| Cover spills to a second page | Reduce spacer count, never the type sizes - the sizes are brand, the spacers are not | this step |
