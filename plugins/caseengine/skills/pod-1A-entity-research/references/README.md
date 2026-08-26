# References - Entity Research

Reference assets the skill loads at runtime. Three subfolders:

| Folder | What's in it |
|---|---|
| [`schemas/`](schemas/) | Machine-readable JSON schemas declaring the shape of structured outputs. Downstream consumers validate against these. |
| [`scripts/`](scripts/) | Bundled Python scripts the cowork runtime can execute (e.g., chart generation). Self-contained, dependencies declared in each script's docstring. |
| [`examples/`](examples/) | Calibration anchors (GOOD / BAD / EDGE CASE) the skill reads before generating to set the quality bar. |

Standalone reference docs at this level:

- [`report-design.md`](report-design.md) - the canonical report look and feel: model Doc id, the repo renderer (`scripts/render-research-doc.py` in `case-engine-webapp`), and the design spec every rendered Doc must match.

Each subfolder has its own `README.md` describing what's there and how it's used.

## How the skill consumes these

- **Schemas** - referenced from `SKILL.md` > Best Practices > Outputs. Producer side: skill writes `entity-map.json` matching `schemas/entity-map.json`. Consumer side: downstream skills validate against the same schema.
- **Scripts** - invoked from `SKILL.md` > SOP > Push to Drive (vector-space chart generation step). Cowork runtime executes `scripts/entity-vector-space.py` against the freshly-written `entity-map.json`.
- **Examples** - read at the start of `SKILL.md` > SOP > Capture data (Gather inputs step). Skill picks 1-2 matching the requested scope as quality calibration.

## Versioning

Files here are versioned with the skill. Bump the skill version when any reference changes.
