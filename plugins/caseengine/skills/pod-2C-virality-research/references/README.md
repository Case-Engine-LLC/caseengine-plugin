# References - Pod Virality Research

Reference assets the skill loads at runtime. Three subfolders + one legacy data file:

| Folder | What's in it |
|---|---|
| [`schemas/`](schemas/) | Machine-readable JSON schemas declaring the shape of structured outputs. Downstream consumers validate against these. |
| [`examples/`](examples/) | Calibration anchors (GOOD / BAD / EDGE CASE) the skill reads before generating to set the quality bar. |
| [`subreddit-map.json`](subreddit-map.json) | Legacy mapping of industry/practice-area → subreddit list. Consumed by `scripts/reddit-virality-fetch.py` when the Reddit API path is exercised. Mode A only. |
| [`iteration-log.json`](iteration-log.json) | Append-only log of issues surfaced by real runs. Each entry has id / category / severity / description / resolution / fix_in_version / status. |

## How the skill consumes these

- **Schemas** - referenced from `SKILL.md` > Best Practices > Outputs. Producer side: skill writes `virality-research.json` matching `schemas/virality-research.json`. Consumer side: downstream skills (Topic Planner) validate against the same schema.
- **Examples** - read at the start of `SKILL.md` > SOP > Capture data (Gather inputs step). Skill picks 1-2 matching the requested scope as quality calibration.
- **subreddit-map.json** - read by `scripts/reddit-virality-fetch.py` to resolve the right subreddits for a given industry. Add new industries here as needed.
- **iteration-log.json** - append-only institutional memory. Read it before changing logic; append after every run that surfaces an issue.

## Versioning

Files here are versioned with the skill. Bump the skill version when any reference changes.
