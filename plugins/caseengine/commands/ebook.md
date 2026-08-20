---
description: A client's eBook and run-of-show generation runs, and where each one is.
argument-hint: "<client name or slug> [pipeline]"
---

Show the generated deliverables for a client — eBooks and podcast run-of-shows —
and what state each run is in.

## Where this data lives

There is no eBook table. eBooks and run-of-shows are **content generation runs**,
stored in `content_generation_jobs` and rendered by the run-of-show views in the
dashboard. Pipelines you will see:

- `podcast_ros` — podcast run of show, the newest rollout
- `v3`, `v2` — current eBook generation
- `legacy` — the older pipeline, the bulk of historical runs

## 1. Pull the runs

`client_list_generation_runs` with the client from `$ARGUMENTS`. Pass `pipeline`
to narrow, or `editorial_status` for `generated`, `in_review`, `approved`.

## 2. Report state, not just count

Two states matter and they are different:

- **`status`** — did the run itself finish? (`completed`, `failed`, `queued`)
- **`editorial_status`** — where is the output in review? (`generated`,
  `in_review`, `approved`)

A run can be `completed` and still nowhere near approved. Lead with failures if
there are any, then what is waiting on review.

Include the Google Doc URL where one exists — that is usually what the person
asking actually wants.

## 3. Be careful about approvals

`approved_at` and `approved_by` only reflect sign-off captured **in the
dashboard**. Client approval that came through Slack or an account manager is
not here, and across the whole table almost nothing is.

So an empty `approved_at` means *"no approval was recorded"*, not *"the client
has not approved"*. Never report the second when you only know the first. Check
with the account manager, and when you learn the answer, record it with
`/caseengine:approved` so the next person does not have to ask again.
