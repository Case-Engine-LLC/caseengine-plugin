# References - Keyword Research

Reference assets the skill loads at runtime. One subfolder + one log:

| Path | What's in it |
|---|---|
| [`examples/`](examples/) | Calibration anchors (GOOD / BAD / EDGE CASE) the skill reads before generating to set the quality bar. |
| [`iteration-log.json`](iteration-log.json) | Append-only log of runs that surfaced issues. Every fix lands here with a fixable resolution and a target version. |

## How the skill consumes these

- **Examples** - read at the start of `SKILL.md` > SOP > Capture data (Gather inputs step). Skill picks 1-2 matching the requested scope as quality calibration. If empty, flag `"references_status": "empty"` in metadata and proceed on methodology alone.
- **Iteration log** - read when something feels off mid-run; check if the same issue is already logged before re-investigating. Append-only - never edit past entries.

## Versioning

Files here are versioned with the skill. Bump the skill version when any reference changes.

## Note on schemas + scripts

This skill is data-only (no chart-generation script, no DOCX build script — Google Doc conversion happens at upload time via Drive API). The output JSON shape (`keyword-research.json` with `search_queries`, intent buckets, PAA stacks, related searches) is documented inline in `SKILL.md` under `## Output`. If a downstream consumer needs a strict JSON schema later, add it as `schemas/keyword-research.json` and update this README.
