# Examples - ROS Template v2

One file: [`ros-template-v2-examples.md`](ros-template-v2-examples.md), with `## GOOD`, `## BAD`, and `## EDGE CASE` labeled sections per CE convention. Append new entries as labeled sections. Never split into separate files.

**Format locked 2026-08-14.** The GOOD anchors are verbatim from the live doc and match `SKILL.md -> Editorial Guidelines -> Guideline 4` exactly. The earlier "where the live doc and SKILL.md disagree" section is gone; that reconciliation is done.

## What is in it

- **GOOD 1 - Truck Accidents (GA - Savannah)** and **GOOD 2 - Slip and Fall (CA - San Diego)**, both reproduced in full from the live doc rather than summarized. Each carries a "what each section teaches" block. Read those blocks against the current format rather than at face value: both anchors predate 2026-08-18, so their Introductions still show the old merged welcome and their notes still describe a cold open, a lead-in and a three-move answer shape, all of which are retired. `references/document-structure.md` and `references/introduction.md` are the format of record; these two entries are calibration for voice and for the Segment 2 geo treatment, not for the Introduction shape.
- **BAD 1 - the v1 format this replaces.** The real Houston question block, plus the five specific rules that produced the choppiness feedback: no post-response co-host lines between questions, the one-sentence setup cap, read-aloud `**Label:** detail` bullets, statutes in attorney-facing bullets, and the ~25-45 percent city-share quota that produced "in a the Inland Empire car accident claim".
- **BAD 2 - the 8-prompt intermediate version,** rejected on the 2026-08-14 call. Better than v1 and still a list. Documents why halving the count did not fix the complaint.
- **BAD 3 - a non-city label dropped into the city slot.** Observed live in both anchors' Set 2.
- **EDGE 1 - the attorney runs dry at minute 8.** The three-second silence rule and the reserve-bench fallback, in order of use.
- **EDGE 2 - the Ontario problem.** Per-city sets need per-city entity resolution; a regional entity map cannot supply it, so a set is not always buildable.
- **EDGE 3 through 8** - legacy-format client, Founder Story, a legacy sibling in the same folder, no `pod-1D` output, Topic Only scope, and unconfirmed region phrasing.

## Provenance and regeneration

Pulled from doc `1Bv-EWc7HBtKqc09XEfQnBIfSOdm6m4Tc-kJNw5uKErk` via the Docs API with `includeTabsContent`, then demoted three heading levels to nest. Re-fetch the live doc directly when it changes - `gws docs documents get` with `includeTabsContent`, then demote headings three levels. The live doc is the moving target; this file is a snapshot with a date on it.

## How the skill uses them

Read at `## Checks -> ### Orient`. Pick 1-2 matching the requested scope and hold them through `## Create`. They set the structural bar and the voice bar, which matters more here than in most skills because the deliverable is spoken aloud.

## Adding entries

After a run, append what was learned as a labeled section with a one-line note on why. Jargon-scan failures, geo-tag disputes, interpolation breaks, and attribute-set staleness are the categories most worth capturing.
