---
description: Show open/overdue/awaiting-review counts per person on the team.
argument-hint: "[as-of date]"
---

Pull team workload from the Case Engine dashboard so a lead can see who's
overloaded.

Argument: `$ARGUMENTS` — optional. A date to evaluate as-of. Empty means
today.

## Steps

1. **Call `work_team_workload`** with the resolved date (today if none was
   given).

2. **Present as a table**, one row per person: open count, overdue count,
   awaiting-review count. Sort by overdue count descending, then open count —
   surface who's actually behind, not just who has the most assigned.

3. **Call out anything that looks wrong**, don't just print the numbers:
   someone with a large overdue count, someone with zero of everything (might
   mean they're not linked to a team member row, not that they're idle).

4. **Do not editorialize about performance.** This is a load-balancing tool,
   not a review. Report the counts and let the human draw conclusions about
   whether to rebalance.

## Notes

- If the caller wants one person's detail instead of the whole team, use
  `work_list_tasks` for that person (resolve their id via `work_list_people`
  first) rather than filtering this output — `work_team_workload` is
  aggregate counts only, it doesn't return the underlying task list.
