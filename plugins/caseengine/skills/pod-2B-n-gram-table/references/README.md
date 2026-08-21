# pod-2B-n-gram-table - references/

Bundled reference data for the skill. Loaded into context as needed; read-only at runtime.

## Layout

```
references/
  README.md             This file - explains what is in here.
  schema/               JSON schemas downstream consumers validate against.
    n-gram-table.json   Canonical shape for the machine-readable n-gram-table.json artifact.
  examples/             Labeled GOOD / BAD / EDGE CASE n-gram tables for calibration.
    examples.md         Index + verbatim reference prompts.
    good--ga-savannah-full-ngram.md   Anchor run, full 25-35 row table.
  iteration-log.json    Append-only record of bugs, papercuts, drift, and fixes spotted across runs.
```

## What each holds

- **README.md** - this file. The map of the folder.
- **schema/** - JSON schemas (draft 2020-12) downstream skills validate against. `n-gram-table.json` defines the four-column row set (`question_text`, `ngrams`, `entities`, `predicates`), top-level `scope` / `location` / `row_count` / `dedup_merges` / `localization_scan_result`, and the `metadata` provenance block. The skill's QA phase validates the artifact it writes against this schema; if the file is absent it logs `schema_status: missing` and proceeds.
- **examples/** - one `{type}-examples.md` doc with labeled GOOD / BAD / EDGE CASE sections, plus full reference tables from real runs. Read 1-2 examples matching the requested scope as calibration anchors before generating. If the folder is empty, the skill runs on in-skill methodology alone and flags `references_status: empty` in metadata.
- **iteration-log.json** - the skill's institutional memory. Append-only record of issues spotted across runs. The skill READS this at run-start, filters to `status: open` and `status: in-progress` entries, and surfaces them as known issues to watch for. The skill never WRITES to it at runtime. Entries are appended post-run (manual, ID format `YYYY-MM-DD-NNN`) or proposed by `scripts/diff_against_template.py` with `status: proposed` awaiting human sign-off. Validates against `ops-skill-creator/references/schema/iteration-log.schema.json`.

## What goes here vs. SKILL.md

- **SKILL.md** owns rules (Best Practices), workflow (SOP), trigger phrases, quality gates.
- **references/schema/** owns machine-readable contracts downstream skills validate against.
- **references/examples/** owns concrete labeled artifacts to calibrate against per run.
- **references/iteration-log.json** owns the cross-run issue history read at every run start.

## Not under references/

- `scripts/` lives at the skill folder root, not under `references/`. Scripts are executable, not reference data.
- `prompts/` and `templates/` are part of the canonical `references/` layout but are not present for this skill; the verbatim reference prompt lives inline in SKILL.md instead. Add the folders here if a future revision moves those resources out of the skill body.
