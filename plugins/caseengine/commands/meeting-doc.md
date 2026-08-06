---
description: Build a client meeting doc from live Case Engine dashboard data.
argument-hint: "<client name or slug>"
---

Populate a meeting doc for a client using real Case Engine dashboard data —
not recalled context, not last month's doc.

Argument: `$ARGUMENTS` — the client. Ask for it if missing; do not pick one.

## Steps

1. **Resolve the client.** `client_get_profile` with the name or slug. Keep
   the returned `client.id` for every subsequent call. If it 404s, stop and
   ask — a meeting doc for the wrong firm is worse than a late one.

2. **Pull the work.**
   - `work_list_items` with `client_id` → open work.
   - `work_list_items` with `client_id` and `include_closed: true` → what
     shipped since the last meeting. Filter to the relevant window yourself.
   - `work_list_approvals` with `client_id` → anything waiting on a human.

3. **Draft the doc.** A working default, adjust to whatever house format the
   user names:
   - **Since last time** — completed work, grouped by workstream.
   - **In flight** — open items with status and owner.
   - **Blocked / needs a decision** — blocked tasks and pending approvals,
     each with what specifically unblocks it.
   - **Next** — upcoming and due-dated items.
   - **Open questions** — only things the data actually leaves ambiguous.

4. **Cite the source.** Every line traces to a task, approval, or client-record
   field you actually retrieved. If a section has no data, write "nothing
   recorded" — do not synthesize plausible agency work to fill it out.

5. **Flag the gaps.** Note anything in `unmatched` or `errors`, and say
   plainly if the board looks thinner than the meeting probably warrants. That
   is a real finding about the board, and useful for the meeting.

## Hard rules

- **Do not create tasks from this.** Action items that come out of the meeting
  are proposals until a human confirms each one. `work_create_task` is not
  part of this command.
- **Do not edit task state** while assembling a doc. Reading only.
- **Do not mix in ClickUp.** It is retired; native `campaign_task` lifecycle
  is the only source of truth.
- The client profile dump includes commercial fields (retainer, settlement
  amounts). Those are internal — keep them out of anything client-facing
  unless the user explicitly asks for an internal-only doc.
