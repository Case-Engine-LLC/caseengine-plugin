# References - Client Guide

Reference assets the skill loads at runtime. Three subfolders:

| Folder | What's in it |
|---|---|
| [`schemas/`](schemas/) | Machine-readable JSON schemas declaring the shape of structured inputs/outputs. Build script + downstream consumers validate against these. |
| [`scripts/`](scripts/) | Bundled Python scripts the cowork runtime can execute (e.g., the CE-branded DOCX/MD build). Self-contained, dependencies declared in each script's docstring. |
| [`examples/`](examples/) | Calibration anchors (GOOD / BAD / EDGE CASE) the skill reads before generating to set the quality bar. |

Each subfolder has its own `README.md` describing what's there and how it's used.

## How the skill consumes these

- **Schemas** - referenced from `SKILL.md` > Output > Files written. Producer side: skill writes `client-guide-data.json` matching `schemas/client-guide.json`. Consumer side: the build script + downstream skills (e.g., `/clip-table`) validate against the same schema.
- **Scripts** - invoked from `SKILL.md` > Push to Drive > Build CE-branded DOCX. Cowork runtime executes `scripts/build-client-guide-docx.py` against the freshly-assembled `client-guide-data.json` to emit paired `Client Guide.docx` + `Client Guide.md`.
- **Examples** - read at the start of `SKILL.md` > Standard Operating Procedure > Universal State Check (Gather inputs step). Skill picks 1-2 matching the requested scope as quality calibration. The `.md` calibrates structure; the `.docx` calibrates rendering.

## Versioning

Files here are versioned with the skill. Bump the skill version when any reference changes.
