# Schemas - Entity Research

Canonical shape definitions for the structured outputs this skill produces. Every JSON deliverable validates against a schema in this folder. Single source of truth for the JSON contract; if the shape changes, edit the schema first, then update SKILL.md prose.

## Files

| Schema | Output it describes | Consumers |
|---|---|---|
| [`entity-map.json`](entity-map.json) | The `entity-map.json` deliverable (entities + clusters + bridges + localization data + optional supplement + provenance) | `/n-gram-table`, `/ros-template`, `/client-ros`, `/topic-planner`, `/virality-research` |

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
- `min` / `max` / `min_items` / `max_items` / `min_keys` / `max_keys` - bounds
- `item_shape` - for arrays of objects
- `value_shape` - for objects with dynamic keys
- `default` - if optional with a default

## How schemas connect to the skill

- **SKILL.md** references the schema at Best Practices > Outputs > Files written.
- **Run Vector Analysis** SOP procedure produces JSON matching the schema.
- **Quality gates** verify the produced JSON validates against the schema before Push to Drive.
- **Downstream skills** read the schema (or this README) to know what fields to expect.

## Version bumps

Bump `version` and append to `version_history` whenever:
- A field is added, renamed, or removed
- A type changes
- An enum gains/loses values
- A required field becomes optional or vice versa

Schema version is independent of skill version - they're bumped on different cadences.
