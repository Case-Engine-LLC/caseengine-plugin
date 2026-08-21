# Reference Examples - Topic Planner

Read before generating. These calibrate what GOOD / BAD / EDGE CASE look like for this skill.

## Format

Every example is a single markdown file with a YAML frontmatter header declaring:
- `label:` GOOD / BAD / EDGE CASE
- `skill:` pod-2A-topic-planner
- `run_date:` YYYY-MM-DD
- `firm:` client firm the plan was built for
- `mode:` production (legacy entries may show `client-level` / `episode-level` / `sales-sketch` — `sales-sketch` was removed in v3.0.0 and is archive-only)
- `scope:` topic scope if episode-level mode
- `source:` where the example came from (real client run, reference teardown)
- `why_this_label:` multi-line explanation of what makes this example good/bad/edge (did the ranking match what the client actually wanted, were client intel modifiers load-bearing, did Content Plan Views land)
- `known_flaws:` null if none, else specific issues the reader should see

The body is the verbatim output from the run. For skills that produce JSON, include the JSON as a fenced code block inside the MD so one file covers both narrative + machine-readable shape.

## GOOD

- [good--sutliff-stout-car-accidents-client-level](good--sutliff-stout-car-accidents-client-level.md) - Client-level plan for Sutliff & Stout with virality boost layer applied. Anchors: composite math reconciled inline (0.72 base + 0.10 virality = 0.82), hardcoded Episode 1 Biography/Founder Story with bolded attorney names, prose-not-tables Top Practice Areas, H3-per-episode Content Plan Views with middle-dot separators, thin-client-intel transparency flagged four places, explicit /pod-2B-n-gram-table handoff with entity-map prereq.
- [family-law-+-sex-abuse/](family-law-+-sex-abuse/README.md) - Canonical Family Law + Sex Abuse production-mode plan, sanitized from a real client run. Demonstrates the full structural skeleton: Show Identity 4-field approval block, 12-Episode Plan main table, Additional Topics bonus table with `Swaps for` column, INTERNAL block with Topics by Practice Area + Fathom Service Weighting + Similarity Filter + reserve catalog, and Provenance trail. Placeholders + folder README explain how to adapt for a new firm.
<!-- - [Short title](good--slug.md) - one-line hook -->

## BAD

<!-- - [Short title](bad--slug.md) - what failed and why -->

## EDGE CASE

<!-- - [Short title](edge--slug.md) - when standard approach doesn't fit -->
