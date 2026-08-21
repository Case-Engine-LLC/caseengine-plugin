---
description: A client's blog inventory — what is published, scheduled, or still an idea.
argument-hint: "<client name or slug> [status]"
---

Show what blog content actually exists for a client, as opposed to the tasks
about writing it.

## 1. Pull the inventory

`client_list_blogs` with the client from `$ARGUMENTS`. Pass `status` when the
user asked for a slice — `published`, `scheduled`, `idea`.

It returns each post's title, URL, status, scheduled and published dates, topic
cluster, practice area and workbook provenance, plus a status breakdown.

## 2. Report it usefully

Lead with the shape: how many published, scheduled, and still ideas. Then the
detail that was asked for.

Sort published by date, most recent first. For scheduled work, sort by the
scheduled date and flag anything whose date has passed but which is still not
published — that is the most common real problem in this data.

## 3. If asked whether something is live

Do not answer from the `status` column. It records what someone entered, not
what is true.

Fetch the URL and look. Then record it:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/record.py" \
  --task <campaign_task-uuid> --status pass \
  --observed "<url>" --note "HTTP 200, title matches"
```

`/caseengine:prove` does the whole sequence if there is a task to close.

## Worth knowing

`proof_event_id` exists on every row in this table and is populated on none of
them. The schema anticipated evidence and nothing ever wrote it, so a null there
means "never wired up", not "checked and failed".

Blog *tasks* live in `campaign_task` under the Website Blogs campaign; this is
the content inventory. When someone asks "are we behind on blogs", they usually
want both — the inventory for what exists, the task board for what is owed.
