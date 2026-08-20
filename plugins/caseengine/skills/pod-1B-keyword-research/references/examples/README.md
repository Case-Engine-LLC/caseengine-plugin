# Reference Examples - Keyword Research

Read before generating. These calibrate what GOOD / BAD / EDGE CASE look like for this skill.

## Format

Every example is a single markdown file with a YAML frontmatter header declaring:
- `label:` GOOD / BAD / EDGE CASE
- `skill:` keyword-research
- `run_date:` YYYY-MM-DD
- `topic:` practice area the research was run on
- `scope:` topic-level / State / City
- `source:` where the example came from (real client run, manufactured reference, competitor teardown)
- `why_this_label:` multi-line explanation of what makes this example good/bad/edge
- `known_flaws:` null if none, else specific issues the reader should see

The body is the verbatim output from the run. For skills that produce JSON, include the JSON as a fenced code block inside the MD so one file covers both narrative + machine-readable shape.

## Current examples

(none yet - placeholder. Seeded by Gabe Jordan from production runs as the skill is exercised in real client work.)

## GOOD

- [good--sutliff-stout-houston-car-accidents](good--sutliff-stout-houston-car-accidents.md) - City-scope keyword research (Sutliff & Stout, Houston TX, 2026-04-20): on-spec intent distribution (59/26/10/5), per-row localization ratios with 3% alarm-threshold handling, prominence filter flagging 9 off-domain high-MSV terms without deleting, canonical Search Queries & Volume table ready for ROS Template handoff. PAA depth falls short of 15+/seed (environmental limitation, flagged FAIL honestly in Quality Gates).

## BAD

<!-- - [Short title](bad--slug.md) - what failed and why -->

## EDGE CASE

<!-- - [Short title](edge--slug.md) - when standard approach doesn't fit -->
