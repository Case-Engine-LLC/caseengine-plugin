---
description: Check that a task's work actually landed, then record what you observed.
argument-hint: "<task id or search> [what to check]"
---

Confirm a piece of Case Engine work really happened, and leave the evidence
behind so the close gate — and the next person — can see it.

Do not stop at "the job ran." Look at the result.

## 1. Resolve the task

`$ARGUMENTS` may be a `campaign_task` UUID, or words to search for.

- A UUID → `work_get_task` for the full record.
- Anything else → `work_list_items` or `work_list_tasks` and pick the match.
  More than one plausible hit, ask which; do not guess and prove the wrong thing.

Read the task properly before checking anything. You need to know what was
promised, not just what it is called. Note the client, the deliverable, and any
URL in the description or the linked Marker issue — the reported URL is usually
the exact surface you are meant to check.

## 2. Work out what would prove it

The question is always the same: **what could someone else look at, right now,
that would settle whether this worked?**

| Deliverable | What to check |
|---|---|
| Website change or bug fix | The reported URL, cache-busted, showing the change |
| Blog or page published | The live URL returns 200, title and body match, in the sitemap |
| Podcast episode | The RSS entry resolves, and the show appears in the directories |
| eBook | The PDF downloads, the landing page links it |
| GBP post | The post is visible on the profile with its image |
| Citation or directory listing | The listing resolves and the name, address and phone match |
| Backlink | The anchor is on the live page, pointing where it should, not nofollowed |
| Tracking install | The expected container ID is present in page source |
| Form or intake | A submission actually arrives where it is supposed to |

If the user named something to check in `$ARGUMENTS`, use that.

If nothing about this task is observable from outside, say so plainly rather
than inventing a check. Some work is judgment, and judgment is closed by a
person, not by evidence. Tell the user that is what is happening.

## 3. Actually check it

Use whatever fits — `WebFetch`, `curl -sI`, the browser tools, an API call.
Bust the cache on anything served by a CDN. Prefer the exact URL the client
reported over a URL you constructed.

Report what you found, including when it contradicts the task. **A failed check
is a good outcome for this command.** It is much cheaper to find out here than
from the client.

## 4. Record it

Once you have genuinely looked:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/record.py" \
  --task <uuid> \
  --status pass \
  --observed "<the URL, screenshot path, id or query you checked>" \
  --note "<what it showed>" \
  --method "<how you checked>"
```

Use `--status failed` when it did not pass. Record it either way — a failed
observation is still knowledge, and it stops the task being closed on a
misunderstanding.

## 5. Then, and only then

If the check passed and the user wants it closed, transition the task with
`work_transition_task`. The proof gate will find the observation you just
recorded and allow it.

If the check failed, do not close anything. Report what is broken and offer to
fix it or reopen the work.

## Rules

- Never record an observation you did not make. The value of this whole
  mechanism is that entries in the ledger are true.
- Never let "the deploy succeeded" or "the script exited 0" stand in for
  looking at the result. That substitution is the exact failure this exists to
  prevent.
- If you cannot check something, say you cannot check it. An honest gap beats a
  fabricated pass.
