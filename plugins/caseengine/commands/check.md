---
description: Run the automated QA checks against a live URL and record the results as evidence.
argument-hint: "<url> [task id]"
---

Settle the mechanical half of the QA checklist by looking at the live page,
rather than someone ticking boxes.

## What it checks

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/checks.py" --url <url> --check all
```

| Check | Answers |
|---|---|
| `reachable` | Does the URL actually load? |
| `tracking` | Are the tracking tags there — and the *right* containers? |
| `indexable` | Is it blocked by a robots meta or `X-Robots-Tag`? |
| `sitemap` | Does a sitemap exist, and is this page in it? |
| `schema` | Is there JSON-LD, does it parse, any placeholders left? |
| `custom_404` | Does a garbage URL return a real 404? |
| `placeholders` | Lorem ipsum or unfilled template text in the copy? |
| `https_images` | Any images still served over http? |

Pass `--expect-gtm GTM-XXXX` or `--expect-ga4 G-XXXX` when you know what should
be there. Presence of *a* tag is not proof; the right container is. Pull the
expected IDs from `client_get_profile` first when you have a client in hand.

## Record it against a task

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/checks.py" \
  --url <url> --check all --task <campaign_task-uuid> --record
```

Each check writes its own ledger entry, so a close gate can see exactly which
assertions were settled and which failed.

## Reporting

Lead with failures. A run where everything passes needs one line; a run with a
failure needs the detail, because that failure is the reason someone should care.

**A failing check is a good outcome.** It is much cheaper to find a missing tag
or an absent sitemap entry here than to have a client find it. Do not soften it,
and do not close the task.

## What this does not do

It does not judge. It cannot tell you a site passes ADA — a scanner catches
roughly 40% of WCAG issues — and it cannot tell you whether copy is any good or
a design works. Those stay with people. If someone asks this to settle a
judgment call, say plainly that it can gather evidence but not decide.
