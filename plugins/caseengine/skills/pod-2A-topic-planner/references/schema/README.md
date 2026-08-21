# Schema - Topic Planner

Machine-readable JSON schemas for this skill's structured outputs and its scoring model. Downstream consumers (pod-2B-n-gram-table primarily) validate against `topic-plan-schema.json`; `validate-scoring-model.py` validates `scoring-model.json` against `scoring-model.schema.json`.

## Files

| File | Purpose |
|---|---|
| `topic-plan-schema.json` | Canonical schema for `topic-plan-v{n}.json`. Defines metadata, heading hierarchy, table column structure, and INTERNAL section shape that every Drive Doc + markdown + JSON sibling MUST match. |
| `scoring-model.schema.json` | Validates `references/scoring-model.json` - signal shape, bucket structure, corroboration block, and the weights-sum-to-1.0 invariant. Run by `scripts/validate-scoring-model.py`. |

## How validation runs

The Quality Assurance phase in `SKILL.md` validates the generated `topic-plan-v{n}.json` against `topic-plan-schema.json` before reporting success. Failed validation returns the run to the failing scoring step for regeneration — no shipped output without a passing schema check.

## Versioning

Schemas are versioned with the skill. Any breaking change to the schema (renaming a field, changing a type, removing a required field) bumps the skill MAJOR version. Additive changes (new optional fields) bump MINOR.
