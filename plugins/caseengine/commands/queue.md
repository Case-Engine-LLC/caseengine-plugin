---
description: Your work queue grouped by what it actually is, not 200 rows of identical names.
argument-hint: "[person name] [client]"
---

For most people here, a task list is not a list of different things to do. It is
the same handful of jobs repeated across clients and episodes — and the rows are
frequently named identically, so a flat list is close to unreadable.

This groups the queue by the work, not the row.

## 1. Pull it

`work_list_items` for the caller, or `work_list_tasks` with a person when
`$ARGUMENTS` names someone else. Resolve names via `work_list_people`.

## 2. Group by task name, then client

Do not print one line per task. Print one line per **kind** of work:

```
66 ×  Clip segments for socials v1.0.1        6 clients   due 18 Aug – 3 Sep
59 ×  IR: Full Episode Video Approval v1.0    5 clients   due 18 & 27 Aug
 4 ×  Schedule blog posts v2.0.1              4 clients   overdue
```

Then expand only what was asked about, or the overdue group.

Lead with anything overdue, then anything due today, then the largest cluster —
because the largest cluster is usually the actual day's work.

## 3. Say when tasks are indistinguishable

This part matters and is easy to skip.

Many repeated tasks carry **nothing that identifies which instance they are** —
no episode number, no title, no order, and a milestone name identical to all the
others. When you detect a cluster like that, say so plainly rather than
presenting 59 interchangeable rows as if the reader can pick one:

> 59 of these are identical. Nothing on the task says which episode it is for.

Then give them something they *can* work from — see below.

## 4. Work from the inventory instead

When the cluster is podcast work, pull `client_list_podcast_episodes` for those
clients. Episodes have numbers, titles and a run of show; tasks do not. Working
down the episode list and closing tasks against it is more tractable than
working down a list of identical task rows.

Same for blogs: `client_list_blogs` has titles and URLs where the tasks are
generic.

## 5. Then help with the actual work

Once the shape is clear, offer the next step rather than stopping at a report:
run `/caseengine:check` across the URLs, pull the client profile, draft the
thing. The queue is the starting point, not the deliverable.

## Rules

- **Never present a wall of identical rows.** If you cannot tell two tasks
  apart, neither can the person reading, and saying so is more useful than
  formatting them nicely.
- **Counts before detail.** "You have 66 clip tasks across 6 clients" orients
  someone. Sixty-six rows do not.
- **Overdue first, always.**
