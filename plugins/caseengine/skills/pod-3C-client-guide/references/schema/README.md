# Schemas - Client Guide

Canonical shape definitions for the structured data this skill produces and consumes. The build script reads `client-guide-data.json` matching the schema in this folder; downstream skills validate against the same. Single source of truth for the JSON contract; if the shape changes, edit the schema first, then update SKILL.md prose.

## Files

| Schema | Output it describes | Consumers |
|---|---|---|
| [`client-guide.json`](client-guide.json) | The `client-guide-data.json` deliverable - episode_topic, practice_area, firm, attorney, scope, location, episode_overview (with metadata + episode_plan sub-blocks), pre_interview_prep (things_to_think_about + things_to_do), segments (intro + ordered list + outro), faq | `/clip-table`, `scripts/build-client-guide-docx.py` |

## Schema format

Each schema is a JSON document with these top-level keys:

- `version` - Semver. Bumped on every shape change.
- `doc` - Filename of the artifact this schema describes.
- `description` - One-paragraph context.
- `consumed_by` - List of downstream skill names + scripts that read this artifact.
- `produced_by` - The skill that produces it.
- `version_history` - Append-only log of schema changes.
- `shape` - The canonical structure: required fields, types, value enums, item shapes for arrays, etc.

Shape entries declare:

- `type` - JSON type (string, number, array, object, boolean, integer)
- `required` - true / false / "conditional"
- `description` - what the field means + how it's used
- `enum` - allowed values (if applicable)
- `min` / `max` / `min_items` / `max_items` / `min_keys` / `max_keys` - bounds
- `item_shape` - for arrays of objects
- `value_shape` - for objects with dynamic keys
- `default` - if optional with a default

## How schemas connect to the skill

- **SKILL.md** references the schema at Best Practices > Outputs > Files written.
- **Build script** (`scripts/build-client-guide-docx.py`) consumes JSON matching the schema and emits paired `.docx` + `.md` deliverables.
- **Quality gates** verify the assembled JSON validates against the schema before Push to Drive.
- **Downstream skills** (`/clip-table`) read the schema (or this README) to know what fields to expect.

## Version bumps

Bump `version` and append to `version_history` whenever:
- A field is added, renamed, or removed
- A type changes
- An enum gains/loses values
- A required field becomes optional or vice versa

Schema version is independent of skill version - they're bumped on different cadences.
