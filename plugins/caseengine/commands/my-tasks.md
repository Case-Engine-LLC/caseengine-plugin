---
description: Pull your open work queue from the Case Engine dashboard.
argument-hint: "[client name or slug]"
---

Pull the work queue from the Case Engine dashboard and present it so the user
can act on it.

Argument: `$ARGUMENTS` — optional. A client name or slug scopes the queue to
that client. Empty means the caller's own "my work" view.

## Steps

1. **Resolve scope.**
   - No argument → call `work_list_items` with no `client_id`.
   - A client named → `client_list` with `query` set to the name, pick the
     exact row, then `work_list_items` with that `id`. Do not hand a guessed
     slug straight to `work_list_items`: a slug that does not exist returns an
     empty queue, which is indistinguishable from a client with no open work.
   - Client not found → say so and list nothing. Do not guess a neighbouring
     client.

2. **Group and present.** Group by client (or by source, for a single-client
   queue). Per item show: title, status, source, due date if set, and its
   `url` — link to the task itself, don't paraphrase a bare id.
   Lead with what is overdue or blocked — not with the longest list.

3. **Surface gaps.** If the response has non-empty `unmatched` or `errors`,
   say so explicitly. A partial queue presented as complete is worse than an
   error. Same for `has_more: true` — `work_list_items` is paginated
   (100/page by default), so a large queue needs more than one call
   (`offset`) before "here's everything" is true; say how many you're
   showing out of `total_count` if you stop short.

4. **Confirm identity once.** State the `identity.personName` / `email` the
   server resolved, so a wrong-key situation is obvious immediately rather
   than after the user acts on someone else's list.

5. **Offer the next step**, do not take it. Reading is safe; transitioning a
   task or creating one is not. Ask before any write. Staff hold `tasks_write`
   automatically, so a `missing_capability` here means the caller does not
   resolve to an active team-member record — surface that rather than
   retrying.

## Notes

- Closed items are excluded by default. Pass `include_closed: true` only when
  the user asks for history.
- Empty queue is a real answer. Report it plainly.
