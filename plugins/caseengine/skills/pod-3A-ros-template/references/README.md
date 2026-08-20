# References - ROS Template

Reference assets the skill loads at runtime. Three subfolders:

| Folder | What's in it |
|---|---|
| [`schemas/`](schemas/) | Machine-readable JSON schemas declaring the shape of structured outputs. Downstream consumers (`/client-ros`, `/client-guide`, `/clip-table`) validate against these. |
| [`scripts/`](scripts/) | Bundled Python scripts the cowork runtime can execute (e.g., CE-branded DOCX build). Self-contained, dependencies declared in each script's docstring. |
| [`examples/`](examples/) | Calibration anchors (GOOD / BAD / EDGE CASE) the skill reads before generating to set the quality bar. Pairs a `.md` (structural anchor) with a `.docx` (rendering anchor) per example. |

Each subfolder has its own `README.md` describing what's there and how it's used.

## How the skill consumes these

- **Schemas** - referenced from `SKILL.md` > Outputs > Files written. Producer side: skill writes `ros-template-data.json` matching `schemas/ros-template.json`. Consumer side: downstream `/client-ros` reads the same shape to populate placeholders.
- **Scripts** - invoked from `SKILL.md` > Push to Drive > Build CE-branded DOCX. Cowork runtime executes `scripts/build-ros-template-docx.py` against the freshly-written `ros-template-data.json` to produce both the `.docx` (Drive auto-converts to Google Doc on upload) and a paired `.md` (raw markdown sibling).
- **Examples** - read at the start of `SKILL.md` > SOP > State Check. Skill picks 1-2 matching the requested scope as quality calibration. The `.md` sets the structural bar (segment progression, question framing, timing budgets); the `.docx` sets the rendering bar (cover page, fonts, headers, footers).

## ROS Template is the tokenized layer

This skill produces the GENERIC reusable script - every firm-specific value lives as a `{{PLACEHOLDER}}` per the 12-token taxonomy (Best Practices > Placeholder taxonomy). Don't expand the example data into firm names, attorney names, or city names at this stage; that's `/client-ros`'s job downstream. Bundled scripts MUST preserve placeholder tokens verbatim.

## Versioning

Files here are versioned with the skill. Bump the skill version when any reference changes. Schemas track their own `version` independently and append to `version_history` on every shape change.
