# References - ROS Template v2

Reference assets `pod-3A-ros-template-v2` loads at runtime.

| Folder / file | What's in it |
|---|---|
| [`schema/`](schema/) | `ros-template-v2.json` (v2.4.0) - the canonical shape `ros-template-v2-data.json` validates against, including the three STATIC constants pinned with `const` and the generated `outro` block. Downstream `pod-3B-client-ros` reads the same shape to populate placeholders. Distinct from the legacy `ros-template.json`; neither validates against the other. |
| [`examples/`](examples/) | `ros-template-v2-examples.md` - calibration anchors (GOOD / BAD / EDGE CASE) read before generating to set the quality bar. One file, labeled sections, appended to over time. |
| [`attributes/`](attributes/) | `attributes-fallback.json` - the static ranked attribute set used ONLY when `pod-1D-attribute-research` has no output for the requested market. |
| [`prompts/`](prompts/) | `01..05` - the live generation prompt per document section, each with its rules, a GOOD / BAD pair, mechanical gates, and a repair instruction per gate. The README carries the fixed execution order and the five global gates. The body is generated section by section, not in one pass. |
| `outro.md` | The Outro spec - the three-line shape, why each line reads the way it does, the five credit approaches, the rotation rules, and gates OC-1 through OC-9. The reasoning layer; `outro-banks.json` is the contract. Companion to `introduction.md`. |
| `outro-banks.json` | Machine-readable outro spec - per-line required beats, invariants, clause banks and the line 3 slot grid. Read at generation time. Wins over `outro.md` if the two disagree. |
| `iteration-log.json` | Append-only institutional memory. Read at `## Checks -> ### Orient`, filtered to `status: open` and `in-progress`. Never written at runtime. |

## How the skill consumes these

- **Schema** - referenced from `SKILL.md` > Outputs > Schema. Producer side: the skill writes `ros-template-v2-data.json` matching it. Consumer side: `pod-3B-client-ros` reads the same shape.
- **Examples** - read at `## Checks -> ### Orient`. Pick 1-2 matching the requested scope. If empty, proceed on the `## INTERNAL` reference material and flag `"references": "empty"` in `metadata.json`.
- **Attributes** - loaded at `## Prepare Inputs` only when the live `pod-1D-attribute-research` output is absent. A fallback run is always Inferred, never Confirmed, and carries an `> INFERRED:` flag with the pull date. Answer engines move; the file is a 2026-08-14 snapshot.
- **Outro** - `outro.md` and `outro-banks.json` are read together at `## Create` when Segment 1's outro is generated. All three spoken lines are generated per episode against the beats; only `outro_note` *(removed 2026-08-21 - the STATIC set is now welcome / welcome_first)* is constant. Rotation is checked against the prior episodes' `metadata.json` before selecting a credit approach.
- **Prompts** - the README is read at `## Checks -> ### Orient` for the execution order and global gates; each numbered prompt is read at the moment its section is generated in `## Create`. Section gates are repaired in place before moving on, not deferred to `## Quality Assurance`.
- **Iteration log** - read once per run, surfaced as known issues to watch for. The four open blocking entries are the downstream changes v2 needs before it can ship end to end.

## ROS Template v2 is the tokenized layer

This skill produces the GENERIC reusable script. Every firm-specific value lives as a `{{PLACEHOLDER}}` per the eleven-token taxonomy in [`placeholders.md`](placeholders.md). Do not expand example data into firm names, attorney names, or city names at this stage; that is `pod-3B-client-ros`'s job downstream. Bundled scripts MUST preserve placeholder tokens verbatim.

The region is the one intentional exception: it is fixed by the template's location scope and ships as plain text, never as a token. `{{REGION}}` does not exist.

## Versioning

Files here are versioned with the skill. Bump the skill version when any reference changes. The schema tracks its own `version` independently and appends to `version_history` on every shape change.

- **Examples** - `examples/intro-outro-examples.md` is the calibration set for S1's opening four sentences and closing three lines. Real BAD -> GOOD pairs. **Read it before writing an intro or outro**; it carries more than the rules do.
