# Schema - ROS Template v2

[`ros-template-v2.json`](ros-template-v2.json) is the canonical JSON Schema (draft-07) that `ros-template-v2-data.json` validates against.

## Producer / consumer contract

- **Producer:** `pod-3A-ros-template-v2` writes `ros-template-v2-data.json` on every run.
- **Consumer:** `pod-3B-client-ros` reads it for the placeholder inventory, the Segment 1 block set, the Segment 2 city blocks with per-question geo tags, the duration band, the episode goal, and the scope.
- If the schema file is absent at runtime, log `schema_status: missing` in `metadata.json` and proceed. A missing schema never blocks a ship.

## What the schema enforces that prose alone would not

- **`episode_format` is pinned to `v2-open-interview`.** A legacy template cannot validate against this schema, and a v2 template cannot validate against the legacy `ros-template.json`. The two formats are structurally incompatible on purpose, which is what makes coexistence safe.
- **Segment 1 carries exactly one `prompt` string,** not an array. The single most likely regression in this format is a second prompt appearing, and the type makes it impossible to express without a schema failure.
- **Every Segment 2 question requires exactly one `geo_tag`** from the fixed enum. No untagged questions, no multi-tagged questions.
- **`questions` per location is pinned to exactly 10** - `minItems` and `maxItems` both 10. Ten is what the contract commits to and ten is what the block renders; nine or eleven fails validation before it reaches the count gate. Each question additionally requires two to four `bullets` and a `topic_plan_ref`.
- **`placeholders_used` is an enum of the 11 approved tokens.** An invented token fails validation before it reaches the placeholder gate. Note that `{{REGION}}` is deliberately absent - the region is plain text fixed by the template's location scope.
- **`source_ngram_ref` is nullable only where an attribute question legitimately has no bank row.** The prose rule is that a question with no traceable source is invented; the schema keeps the field present so the absence is explicit rather than forgotten.
- **There is no `producer_notes` block to express.** It was removed from the schema entirely in 2.0.0 when the section left the format, so a payload cannot carry one and still validate. With it gone there is no exempt region: the jargon scan returns zero everywhere above the Appendix heading, and the Appendix is scoped out only because it ships n-gram rows verbatim.

## Versioning

The schema tracks its own `version` and appends to `version_history` on every shape change. Bump the skill version alongside it. Adding a field is a minor bump; renaming, removing, or retyping a field downstream reads is a major bump and needs `pod-3B-client-ros` updated in the same pass.
