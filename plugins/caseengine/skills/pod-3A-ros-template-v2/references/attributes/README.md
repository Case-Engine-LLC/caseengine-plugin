# Attributes - ROS Template v2

[`attributes-fallback.json`](attributes-fallback.json) is the static ranked attribute set for the Segment 1 attribute block and the Segment 2 attribute questions. The `Attributes to Hit` heading was retired 2026-08-17 - the bullets sit under `ATTORNEY RESPONSE` with nothing labelling them.

## This is the fallback, not the source

The canonical source is `pod-1D-attribute-research`, which runs live Google and ChatGPT pulls for a specific practice area and market. This file is used ONLY when that skill has no output for the requested market.

A fallback run is **always Inferred, never Confirmed.** It must carry `> INFERRED: attribute set from static fallback pulled 2026-08-14, not a live pull` in the markdown, and `attribute_source: static-fallback` plus `attribute_pull_date` in `metadata.json`. Answer engines move. A silently stale attribute set is worse than a visibly stale one.

## What is in it

Ten attributes, ranked by how consistently they appeared across live Google AI Overview and ChatGPT pulls on 2026-08-14, across two practice areas and two markets, on the query family "what to look for when hiring a {practice} lawyer in {city}". Each carries a plain-language `detail` line, a default `segment_2_question` template, and a `default_geo_tag`.

## The two findings that must survive every edit

Both are recorded in the file under `counterintuitive_findings`, and both invert what an attorney's instinct will be on the day, which is exactly why they belong in a document rather than in someone's head.

- **Reviews and awards rank lower than the industry assumes.** ChatGPT explicitly states that verifiable bar standing and disciplinary history is more meaningful than ratings alone. The file ranks verifiable standing above reviews for that reason.
- **Naming a weakness beats making a promise.** Saying what would make a case difficult scored as a positive trust signal. Guaranteeing a number is flagged as a red flag.

Trial willingness is the strongest single attribute and is usually the first sentence of the AI answer. Google asks it in those words: have you taken these to trial, or do you only settle.

## Refresh

When `pod-1D-attribute-research` ships, re-pull and compare against this set. Log what moved rather than just overwriting - answer-engine drift over time is itself a signal worth keeping, and the delta tells you how fast this file goes stale.
