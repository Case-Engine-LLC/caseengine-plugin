# Step 07 - Render

> **Exec:** deterministic
> **Assets:** `references/schema/ros-template-v2.json`, `references/statics.json`, `references/document-structure.md`

## What

Assembles the three artifacts from the section outputs - the markdown source of truth, the JSON payload `pod-3B-client-ros` populates from, and the metadata provenance file. Good output is a payload that validates against the schema and a markdown file whose section order matches the locked structure exactly.

## Inputs

- Section outputs from steps 03 through 06.
- `working_set` and `run_context` - for provenance fields.

## Procedure

1. **Assemble the markdown** [deterministic] - in the locked order from `references/document-structure.md`: cover, S1 (introduction, attributes, outro close), a horizontal rule, S2 (per-location question sets), appendix. Only the cover, S1 and the appendix start a page; S2 flows on from the S1 outro behind the rule. Then the `## INTERNAL` block, which rides into the local markdown only.
2. **Render the constants verbatim** [deterministic] - every string in `references/statics.json` renders byte-identical. Nothing substitutes into any of them; `{topic_phrase}` left `welcome` on 2026-08-18. Compare against the constant, not by eye.
3. **Serialize the payload** [deterministic] - placeholder inventory, S1 blocks, S2 location blocks with per-question `geo_tag` and `source_ngram_ref`, duration band, episode goal, scope, region.
4. **Write metadata** [deterministic] - the provenance block: run date, format and its source, upstream paths, attribute source and pull date, episode goal, counts (locations, questions, appendix rows, placeholders), geo plan, jargon scan result, references status, schema status.

## Outputs

```
artifacts: {
  markdown: path, payload: path, metadata: path,
  schema_status: "valid" | "missing"
}
```

## Validation

- Payload validates against `references/schema/ros-template-v2.json`. A missing schema file logs `schema_status: missing` and proceeds; an invalid payload does not.
- Markdown section order matches the locked structure.
- All constants byte-identical to `statics.json`.
- Metadata carries every provenance field.

## Failure modes

| Failure | Exit behavior | Routes to |
|---|---|---|
| Payload fails schema validation | Fix the payload, never loosen the schema to fit it | the offending section step |
| A constant differs from `statics.json` | Replace with the constant; a regenerated constant is drift, not an improvement | this step |
| Schema file absent | Log `schema_status: missing`, continue | continue |
