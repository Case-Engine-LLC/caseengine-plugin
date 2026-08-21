---
description: Record a client approval that arrived in Slack, by email, or via an account manager.
argument-hint: "<task id or search> [who approved, and where]"
---

Most Case Engine client approvals never touch the dashboard. They arrive as a
Slack message, an email, a sentence in a call, or an account manager saying "the
client's happy with it." That approval is real and it is usually the strongest
signal we have — it just evaporates instead of being written down.

This captures it.

## 1. Resolve the task

`$ARGUMENTS` may be a `campaign_task` UUID or words to search. Use
`work_get_task` or `work_list_items`. If it is ambiguous, ask.

## 2. Establish what actually happened

You need four things, and it is worth asking rather than assuming:

- **Who approved it.** The client contact by name, not "the client."
- **Where it arrived.** `slack`, `email`, `call`, `meeting`, `account-manager`.
- **A link, if one exists.** A Slack permalink is ideal. This is what makes the
  approval checkable months later instead of a memory.
- **Whether you heard it first-hand**, or someone relayed it to you.

That last one matters more than it sounds. "The client approved it" survives
three retellings without anyone able to point at the original, and by then
nobody is sure whether the client saw the current version. Recording who relayed
it keeps the chain visible.

## 3. Record it

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/record.py" \
  --task <uuid> --kind attestation --status pass \
  --observed "<what they approved, in their words if you have them>" \
  --approver "<client contact>" \
  --channel slack \
  --link "<permalink>" \
  --relayed-by "<AM name, only if second-hand>"
```

Omit `--relayed-by` when you saw it yourself; the entry is then marked
first-hand.

## 4. Say what is still missing

An approval is not a verification. The client approving a draft does not mean
the thing is live, and the two get conflated constantly.

If the deliverable also needs to be confirmed live, say so and offer
`/caseengine:prove`. An attestation will satisfy the close gate, so it is on you
to be clear about which question it answered.

## Rules

- **Never record an approval you were not told about.** An invented attestation
  is worse than no record, because it will be believed.
- **Do not upgrade a maybe.** "Looks good so far" and "approved" are different.
  Record what was actually said, in `--observed`.
- **Chase the permalink.** A Slack approval with no link is a claim; with a link
  it is evidence. If there is no link to be had, record it anyway and say so.
