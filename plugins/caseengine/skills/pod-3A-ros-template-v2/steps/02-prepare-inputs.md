# Step 02 - Prepare Inputs

> **Exec:** deterministic
> **Assets:** `references/attributes.md`, `references/attributes/attributes-fallback.json`

## What

Loads every source the section steps read and resolves the two values that are not in any file - the geo pairing and the branding - into one working set. Good output is a loaded corpus where every source is either present and recorded, or absent and flagged, with nothing silently defaulted.

## Inputs

- `run_context` - from `steps/01-prerequisites.md`.
- N-gram table, entity map, entity clusters - paths already resolved upstream.
- `attribute-research.json` from `/pod-1D-attribute-research`, when it exists for this practice area and market.
- `keyword-research.json` from `/pod-1B-keyword-research`, optional.
- Region phrasing - **from the user** when `podcast-overview.md` does not carry it.

## Procedure

1. **Load the n-gram table** [deterministic] - in v2 this is source material, not the script. It ships verbatim in the appendix and its substance seeds the short-form questions.
2. **Load the entity map and clusters** [deterministic] - these ground what the writer knows to be locally true. They never reach the page as named terminology.
3. **Load the attribute set** [deterministic] - a live `pod-1D` output is Confirmed; record its pull date. Absent, fall back to `references/attributes/attributes-fallback.json` and mark the run Inferred with the fallback's date. A fallback run is never Confirmed - it is a point-in-time snapshot of answer-engine output, and answer engines move.
4. **Load keyword research** [deterministic, optional] - only if the handoff check in step 01 approved it. Real query strings beat plausible ones when phrasing short-form questions.
5. **Resolve the geo pairing** [deterministic, may escalate to the user] - confirm the Episode geo target and the plain-text region phrasing. Unconfirmed by both the user and `podcast-overview.md`, propose one and mark it `> NEEDS CONFIRMATION:`. Never assume it silently.
6. **Resolve branding** [deterministic] - read the Case Engine Branding folder for logo, colors, and fonts. A per-client `brand.json` typography block overrides the CE default. Brand values resolve at run time; they are never inlined into a step or a script.
7. **Resolve the factual claims** [deterministic, may escalate to the user] - the introduction asserts facts about a real firm and sometimes about the market. Resolve each one before generation, in order: the CE database first (`mcp__caseengine__*` client profile tools - years in practice, case types, offices, team), the firm's website second (record URL and date read), the producer third, batched into a single question. Anything still unresolved does not get hedged into the script - it gets dropped and the generation falls back to a frame that only needs confirmed facts. Any market statistic additionally clears the four tests in `references/introduction.md` - sourced, credible, current with its year, and matched to this geography. Record every claim with its source and check date in `metadata.json`, and never carry a firm claim forward from a previous episode's ROS.
8. **Load calibration examples** [deterministic] - 1-2 scope-matched entries from `references/examples/ros-template-v2-examples.md`. Empty file is not a blocker; record `references: empty`.

## Outputs

```
working_set: {
  ngram_rows: [...], entity_map: {...}, clusters: {...}|null,
  attributes: {source: "pod-1D"|"static-fallback", pull_date: str, ranked: [...]},
  keywords: {...}|null,
  geo: {location: str, region: str, region_confirmed: bool},
  branding: {logo_id, colors, font},
  calibration_examples: [...]
}
```

## Validation

- Every source is recorded as present-with-path or absent-with-flag. No silent defaults.
- Attribute source and pull date both captured for provenance.
- Region phrasing is a literal string, not a token.
- Nothing loaded from a parent scope to cover a missing matching-scope artifact.

## Failure modes

| Failure | Exit behavior | Routes to |
|---|---|---|
| Attribute research absent | Use the static fallback, flag Inferred with its date | continue |
| Region phrasing unconfirmed | Propose one, mark `> NEEDS CONFIRMATION:` | continue |
| Branding folder unreachable | Use CE defaults, flag it; do not invent brand values | continue |
| Calibration examples file empty | Record `references: empty` | continue |
| A source loads at the wrong scope | Discard it and stop | `steps/01-prerequisites.md` |
