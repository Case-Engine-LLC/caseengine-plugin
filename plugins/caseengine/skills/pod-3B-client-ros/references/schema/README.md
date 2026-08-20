# Schemas - Client ROS

Canonical shape definition for the Client ROS deliverable. Single source of truth for the JSON contract; if the shape changes, edit the schema first, then update SKILL.md prose.

## Files

| Schema | Output it describes | Consumers |
|---|---|---|
| [`client-ros.json`](client-ros.json) | The Client ROS deliverable - host-facing recording-day script with placeholders filled in for a specific firm (firm name, attorney, city, statutes, courts, highways) | Client Guide skill (consumes for prep doc generation), Production Package skill, downstream post-production routing |

## Schema format

Each schema is a JSON document with these top-level keys:

- `version` - Semver. Bumped on every shape change.
- `doc` - Filename of the artifact this schema describes.
- `description` - One-paragraph context.
- `consumed_by` - List of downstream skills that read this artifact.
- `produced_by` - The skill that produces it.
- `version_history` - Append-only log of schema changes.
- `shape` - The canonical structure: required fields, types, value enums, item shapes for arrays, etc.

## How the schema connects to the skill

- **SKILL.md** references the schema at Best Practices > Outputs > Files written.
- **Push to Drive** SOP procedure invokes `build-client-ros-docx.py`, which validates input against the schema before rendering.
- **Quality gates** verify the produced JSON validates against the schema.
- **Downstream skills** read the schema (or this README) to know what fields to expect.

## Version bumps

Bump `version` and append to `version_history` whenever:
- A field is added, renamed, or removed
- A type changes
- An enum gains/loses values
- A required field becomes optional or vice versa

Schema version is independent of skill version - they're bumped on different cadences.
