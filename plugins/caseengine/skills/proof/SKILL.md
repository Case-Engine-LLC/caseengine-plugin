---
name: proof
description: Use whenever work is being marked done, completed, resolved, closed, shipped, finished, verified, or approved — in Case Engine or anywhere else. Also when someone asks "is X done?", "did that go out?", "is it live?", "can you close this?", or when an automation finishes a deliverable and needs to report on it. Covers what counts as evidence, how to check the common Case Engine deliverables, and how to record an observation so the close gate accepts it.
---

# Finishing work honestly

There is one rule underneath everything here:

> A thing is not done because the work ran.
> It is done because someone observed the outcome.

That distinction sounds pedantic until you notice how much of it is load
bearing. "The deploy succeeded" is not "the page changed." "The script exited
zero" is not "the posts are live." "I sent it" is not "they got it." Every one
of those substitutions is how a client ends up discovering something before we
do.

## When this applies

Any time work is about to be called finished. That includes closing a Case
Engine task, resolving a Marker issue, reporting that a deliverable shipped, or
just answering someone who asked whether something is done.

It applies to ordinary knowledge work too, not only the things with an API. A
report was sent — was it delivered, did anyone open it. A form was built — can a
stranger submit it, and where does the submission land. Access was granted — can
the person actually log in. The question is always the same: **how do you know?**

## What counts as evidence

Something a different person could look at and reach the same conclusion,
without taking your word for it.

Good: a URL that returned 200 with the expected content, a screenshot of the
live page, an API response showing the post published, a message id, a row
count from the table it should have landed in, a delivery receipt.

Not evidence: an exit code, a green build, a successful write, a status field
someone set, a log line saying "done", your recollection of doing it.

The test is whether it survives being handed to someone who wasn't there.

## Checking the common deliverables

Prefer the exact surface that was promised — for a bug fix, the URL the client
actually reported, not one you constructed. Bust the cache on anything behind a
CDN.

- **Website change** — fetch the reported URL cache-busted, confirm the change
  is present in the response
- **Blog or page** — 200, title and body match the brief, URL in the sitemap,
  page indexable
- **Podcast episode** — resolvable in the RSS feed; show present in the
  directories it was promised in
- **eBook** — the PDF downloads and is a real size, the landing page links it
- **GBP post** — visible on the profile, with its image and link
- **Citation** — listing resolves, and name, address and phone match what was
  filed
- **Backlink** — the anchor exists on the live page, points at the agreed
  target, is not quietly nofollowed
- **Tracking** — the expected container or measurement ID is literally in page
  source; presence of *a* tag is not proof, the right one is
- **Anything with a form** — submit it and confirm the submission arrives

## Recording it

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/record.py" \
  --task <campaign_task-uuid> \
  --status pass \
  --observed "<what you checked>" \
  --note "<what it showed>" \
  --method "<how>"
```

Record failures too, with `--status failed`. A failed observation is knowledge,
and it stops a task being closed on a misunderstanding.

`/caseengine:prove <task>` does the whole sequence — resolve, check, record —
and is usually the right entry point.

## The gate

A `PreToolUse` hook watches for a task being transitioned to `done` or
`approved` and looks for a passing observation recorded against that task in the
last 12 hours.

It defaults to **warn**: it will tell you evidence is missing and let the close
through. Set `CASEENGINE_PROOF_MODE=enforce` and it refuses instead.

It fails open on anything it doesn't understand — an unrecognised tool, a task
id it can't read, an unreadable ledger. It only ever blocks the one case it is
built for. If you hit a genuine false positive, `CASEENGINE_PROOF_BYPASS=1`
allows the call and records the bypass, so the exit is visible rather than
silent.

## Honesty rules

These are the point. Everything else is plumbing.

1. **Never record an observation you did not make.** A ledger of true statements
   is worth a great deal; a ledger of plausible ones is worth less than nothing,
   because people will rely on it.
2. **Never substitute a successful action for a verified outcome.** This is the
   single failure mode the whole mechanism exists to prevent.
3. **Say when you cannot check something.** Plenty of work is judgment, taste or
   relationship, and closes on a person's say-so. That is fine and normal — name
   it as that rather than dressing it up as verification.
4. **A failed check is a good result.** Finding it now is much cheaper than the
   client finding it later. Report it plainly and do not close the task.
