# Reference Examples - Virality Research

Read before generating. These calibrate what GOOD / BAD / EDGE CASE look like for this skill.

## Format

Every example is a single markdown file with a YAML frontmatter header declaring:
- `label:` GOOD / BAD / EDGE CASE
- `skill:` pod-2C-virality-research
- `run_date:` YYYY-MM-DD
- `topic:` practice area the virality pass was run for
- `scope:` Topic Only / Location / Extension
- `source:` where the example came from (real run, reference teardown)
- `why_this_label:` multi-line explanation of what makes this example good/bad/edge (which virality signal dominated, was the emotional hook load-bearing, did it predict actual podcast performance)
- `known_flaws:` null if none, else specific issues the reader should see

The body is the verbatim output from the run. For skills that produce JSON, include the JSON as a fenced code block inside the MD so one file covers both narrative + machine-readable shape.

## GOOD

- [good--sutliff-stout-car-accidents-houston](good--sutliff-stout-car-accidents-houston.md) - Topic-level Car Accidents virality pass with Houston localization A/B. Anchors: five-signal scoring with reconciled math, 48 candidates tiered 9/22/17, Koray prominence filter flagging 4 off-topic drops, localization lift up to +0.17 on story-driven candidates, upfront `llm_only` source transparency.
<!-- - [Short title](good--slug.md) - one-line hook -->

## BAD

<!-- - [Short title](bad--slug.md) - what failed and why -->

## EDGE CASE

<!-- - [Short title](edge--slug.md) - when standard approach doesn't fit -->
