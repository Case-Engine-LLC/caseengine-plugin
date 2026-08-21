# References - Topic Planner

Reference assets the skill loads at runtime:

| Folder / File | What's in it |
|---|---|
| [`schema/`](schema/) | Machine-readable JSON schemas declaring the shape of structured outputs - `topic-plan-schema.json` (output contract, downstream consumers validate against it) and `scoring-model.schema.json` (validates `scoring-model.json` itself). |
| [`examples/`](examples/) | Calibration anchors (GOOD / BAD / EDGE CASE) the skill reads before generating to set the quality bar. |
| [`templates/`](templates/) | Baked-in DOCX reference template used by pandoc to render `.docx` with CE branding. Self-contained, no cross-skill runtime dependency. |
| `scoring-model.json` | The canonical 11-signal scoring model `scripts/score-topics.py` loads at runtime - single source of truth for every signal, weight, and the corroboration mechanic. |
| `topic-seed-catalog.json` | Seed taxonomy: legal domain -> practice areas -> seed episode topics. `### Resolve client, domain, and practice areas` loads it to seed the candidate set before research-derived topics merge in. The evergreen floor; research adds currency + localization on top. Personal Injury and Family Law populated, Criminal Defense stubbed. Compounds - surfaced topics fold back in. |
| `prompts/` | Live generation prompts run as discrete SOP steps - `select-episodes-prompt.md` (episode selection) and `episode-question-tables-prompt.md` (n-gram roll-up + cross-episode dedup). |
| `iteration-log.json` | Append-only run log capturing input context + failure modes + resolutions to spot patterns and iterate the skill / build scripts. |
| `e1-founder-interview-questions.md` | Canonical, hard-coded question set for Episode 1 ("The Founder Interview", Theme "Founder Story"). 21 questions across five segments (S1-S5) + an outro, with `{{LOCATION}}` / `{{BUSINESS}}` / `{{NICHE}}` tokens filled per client. E1 is never n-gram-built; the `## Episode Breakdown` roll-up populates E1's entry from this file. |

Scripts that ship with this skill live at top-level `scripts/` (sibling to `references/`), not inside `references/`. See [`../scripts/README.md`](../scripts/README.md) for the inventory.

## How the skill consumes these

- **Schemas** - referenced from `SKILL.md` > Output Contract. Producer side: skill writes `topic-plan-v{n}.json` matching `schema/topic-plan-schema.json`. Consumer side: downstream skills (pod-2B-n-gram-table) validate against the same schema.
- **Examples** - read at the start of `SKILL.md` > SOP > Capture data (Gather inputs step). Skill picks 1-2 matching the requested mode as quality calibration.
- **Templates** - the baked-in `topic-plan-reference.docx` is fed to pandoc by `scripts/topic-plan-to-docx.sh` as the style reference, so every `.docx` output inherits CE branding.
- **Iteration log** - read at session start to surface recurring issues, append-only after each run that surfaces something off.
- **E1 founder-interview questions** - read by the `### Build the n-gram tables` step and the `## Episode Questions` render step; E1 skips the n-gram build and renders its question set from this file with tokens filled per client.

## Versioning

Files here are versioned with the skill. Bump the skill version when any reference changes.
