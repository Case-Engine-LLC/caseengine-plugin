# Schemas - ROS Template

Canonical shape definitions for the structured outputs this skill produces. Every JSON deliverable validates against a schema in this folder. Single source of truth for the JSON contract; if the shape changes, edit the schema first, then update SKILL.md prose.

## Files

| Schema | Output it describes | Consumers |
|---|---|---|
| [`ros-template.json`](ros-template.json) | The `ros-template-data.json` deliverable (practice_area, episode_topic, scope, location, segments with per-question prompts + timing, optional producer notes / intro / outro blocks) | `/client-ros`, `/client-guide`, `/clip-table` |

## Schema format

Each schema is a JSON document with these top-level keys:

- `version` - Semver. Bumped on every shape change.
- `doc` - Filename of the artifact this schema describes.
- `description` - One-paragraph context.
- `consumed_by` - List of downstream skill names that read this artifact.
- `produced_by` - The skill that produces it.
- `version_history` - Append-only log of schema changes.
- `shape` - The canonical structure: required fields, types, value enums, item shapes for arrays, etc.

Shape entries declare:

- `type` - JSON type (string, number, array, object, boolean, integer)
- `required` - true / false / "conditional"
- `description` - what the field means + how it's used
- `enum` - allowed values (if applicable)
- `min` / `max` / `min_items` / `max_items` - bounds
- `item_shape` - for arrays of objects
- `value_shape` - for objects with dynamic keys
- `default` - if optional with a default

## How schemas connect to the skill

- **SKILL.md** references the schema at Outputs > Files written.
- **SOP > Push to Drive** invokes `scripts/build-ros-template-docx.py` against JSON matching this schema.
- **Quality gates** verify the produced JSON validates against the schema before Push to Drive.
- **Downstream `/client-ros`** reads the same shape to populate the 12 approved `{{PLACEHOLDERS}}` for a specific firm.

## Tokenization rule (ROS Template = tokenized stage)

This schema describes the TOKENIZED ROS - placeholder tokens like `{{FIRM_NAME}}`, `{{ATTORNEY_NAME}}`, `{{CITY}}`, `{{STATE}}`, `{{PHONE_NUMBER}}`, `{{WEBSITE}}` MUST appear verbatim in any field that would otherwise carry firm-specific data. Schema validation does not strip or rewrite tokens. `/client-ros` is the only skill in the pipeline that resolves tokens to firm-specific values.

## Version bumps

Bump `version` and append to `version_history` whenever:
- A field is added, renamed, or removed
- A type changes
- An enum gains/loses values
- A required field becomes optional or vice versa

Schema version is independent of skill version - they're bumped on different cadences.
