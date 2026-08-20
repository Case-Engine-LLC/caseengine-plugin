---
description: Compare what a client's deliverables actually are against what the task board thinks.
argument-hint: "<client name or slug> [podcast|blogs]"
---

The task board and the deliverable inventory are two separate accounts of the
same work, and they disagree — in both directions. This puts them side by side.

## Why this exists

For podcasts, the counts do not reconcile:

- **Conn Law** — 33 episodes, show notes recorded as made on 9, and 12 `Show
  Notes v1.0` tasks still open and unassigned.
- **Eberst** — 38 episodes, show notes made on 8, and **no tasks at all**.
- **Perry** — 12 open Show Notes tasks against **2 episodes** in the inventory.

So an open task does not mean the work is outstanding, and a closed task does not
mean it was done. Neither number can be reported to a client as it stands.

## 1. Pull both sides

- `client_list_podcast_episodes` — the episodes and their run of show. Stage
  flags here are the record of what was **produced**.
- `work_list_tasks` / `work_list_items` for the client — the tasks. These are the
  record of what was **asked for**.
- `client_list_blogs` for content work, against the blog tasks.

## 2. Line them up

Per deliverable type, report three numbers:

```
                        made   tasks open   drift
Show notes                 9           12     +3 tasks with no matching work
Transcript published       0            4     +4
Blog repurpose             0            0      —
```

Do not present either column as the truth. Say which is which: the inventory
records production, the board records intent.

## 3. Name the three failure shapes

- **Task open, work done** — the deliverable exists and nobody closed the task.
  These inflate everyone's queue and make the backlog look worse than it is.
- **Work done, no task** — production happening entirely outside the board. The
  board cannot report on it and nobody is credited for it.
- **Task open, no episode** — tasks deployed for episodes that do not exist,
  usually from a template deployed for a slate bigger than the real one.

## 4. Do not guess which is right

There is no join between a podcast task and an episode — no episode number on
the task, and `campaign_plan.source_deployment_id` is null on every plan. So the
two sides genuinely cannot be matched row by row today.

Report the counts and the drift. Where it matters, ask the person who did the
work. **Do not silently pick a side**, and do not close tasks to make the numbers
agree — that is manufacturing agreement rather than discovering it.

## What good looks like

The fix is upstream: episode identity on the task, and the deliverable's own
completion writing back to it. Until then this command tells you how far apart
the two accounts are, which is worth knowing before anyone reports a number to a
client.
