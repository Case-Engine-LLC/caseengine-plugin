# Scripts - Entity Research

Bundled scripts the skill executes during its SOP. Self-contained; dependencies declared in each script's docstring. Same scripts run in both Mode A (local Claude Code) and Mode B (cowork sandbox).

## Files

| Script | What it does | Invoked from |
|---|---|---|
| [`entity-vector-space.py`](entity-vector-space.py) | Reads `entity-map.json`, plots entities radially by cluster + vector strength, colors by tier (T1 blue, T2 teal, T3 gray), highlights bridges with a gold border, writes `Entity Vector Space.png` to `<scope-folder>/visuals/`. Dependencies: `numpy`, `matplotlib`, optional `adjustText`. | SOP > Push to Drive > Generate vector-space chart |
| [`build-entity-map-docx.py`](build-entity-map-docx.py) | Reads `entity-map.json` + `Entity Vector Space.png` + a CE logo, builds the canonical `Entity Map.docx` (cover page, headers, footers, CE Blue H2s, Calibri body, tier tables with bolded T1 + bridges, cluster architecture, bridge entities, embedded vector-space chart). Auto-generates a Learnings & Insights subsection in the Executive Summary (top entity types, largest cluster, central bridge, tier-balance shape, score consensus, bridge composition). Dependencies: `python-docx`. | SOP > Push to Drive > Build CE-branded DOCX |

## Conventions

- **Self-contained.** Each script runs on its own; no shared imports between scripts. If common helpers are needed, fold them in.
- **Dependencies in docstring.** Top-of-file docstring lists every required + optional Python package. Cowork runtime has `numpy` + `matplotlib` available; `adjustText` is optional and degrades gracefully.
- **Filename convention sourced externally.** Scripts that read deliverables (e.g., `entity-vector-space.py` reads `entity-map.json`) bake in the canonical filename, but the source of truth for the filename is the [Podcast Drive](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU) doc. If the doc changes the convention, update the script to match.
- **Fail gracefully.** If a script can't produce its output (missing dependency, malformed input), it should log the failure and exit non-zero. The calling skill ships the run without that artifact and notes the gap in the metadata.

## Invocation pattern

The skill invokes scripts by:
1. Resolving the script path: `scripts/{name}.py` (relative to the skill folder)
2. Passing the scope folder path (where the freshly-written deliverables live) as a positional arg
3. Optionally passing other CLI args (output path override, etc.)
4. Capturing stdout/stderr for the metadata audit log

Each script's `--help` (via `argparse`) is the canonical CLI reference. Skill prose in `SKILL.md` should not duplicate CLI signatures - just reference the script + describe what it does conceptually.

## Versioning

Scripts are versioned with the skill. If a script changes its CLI, update the skill prose that invokes it. If a script changes its output shape, bump the corresponding schema in `../schemas/`.
