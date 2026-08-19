---
description: List pending Case Engine approvals waiting on a decision.
argument-hint: "[client name or slug]"
---

Pull pending approvals from the Case Engine dashboard and present them so the
user can act.

Argument: `$ARGUMENTS` — optional. A client name or slug scopes the list to
that client. Empty means every client.

## Steps

1. **Resolve scope.**
   - No argument → call `work_list_approvals` with no `client_id`, filtered to
     open/pending status.
   - A client named → `client_get_profile` with the slug first, then
     `work_list_approvals` with the returned `client.id`.
   - Client not found → say so and list nothing. Do not guess a neighbouring
     client.

2. **Present.** Group by client (skip that grouping for a single-client
   list). Per approval show: entity type, what it's waiting on, the step, who
   it's waiting on (if the data has it), and how long it's been pending. Lead
   with the oldest / most blocking, not the longest list.

3. **Surface gaps.** If the response has non-empty `unmatched` or `errors`,
   say so explicitly.

4. **Offer the next step**, do not take it. Approving or rejecting a step
   (`work_approve_step`) is a write — ask before calling it, and never
   approve something the connected identity itself submitted; the server
   blocks self-approval regardless, but don't attempt it and rely on the
   error either.

## Notes

- Empty list is a real answer. Report it plainly — "nothing pending" is
  useful information for whoever's asking.
