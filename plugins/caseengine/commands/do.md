---
description: Work a task by its own SOP — read the steps, gather what they need, do it, hand it off.
argument-hint: "<task id or search>"
---

Most tasks here already carry their instructions. **82% of open tasks have a
Standard Operating Procedure in the description**, averaging six steps, often
with Loom walkthroughs. Do not invent a process, and do not write your own
checklist — read theirs and work it.

## 1. Get the task and its SOP

`work_get_task` for a UUID, or `work_list_items` / `work_list_tasks` to find it.

The description is the SOP. It usually carries:

- a role and time estimate — `seo analyst, sr. seo analyst | 15m`
- a **What is?** line saying what the deliverable is for
- numbered or bulleted steps, sometimes grouped under sub-headings
- Loom links for anything visual
- a handoff instruction at the end, often "add the link in the parent thread and
  tag the PM"

Read all of it before starting. Then restate the steps back as a short working
list so the person can see what they are committing to.

## 2. Handle what the SOP gets wrong

These are known and recur; do not follow them blindly.

**Dead ClickUp links.** 178 open tasks still send you to `app.clickup.com`.
ClickUp is retired. Where an SOP says "go to the service tab of the client
profile" and links ClickUp, use `client_get_profile` instead and say you
substituted it.

**Unfilled template headers.** Around 2,000 SOPs still read `role, backup role |
hr` or `X | Xm` — the placeholder was never filled in. Ignore it rather than
treating it as the estimate, and do not repeat it back as if it were real.

**`{screenshot}` and `{date}` tokens.** Unrendered template placeholders. Skip
them silently.

**Steps that assume a tab is already open.** Many SOPs start mid-flow. If a step
refers to something you have no link for, ask rather than guessing.

## 3. Gather what the steps need, before doing them

Read the whole SOP first and collect the inputs in one pass — it is faster than
stopping at every step. Typically:

- `client_get_profile` for the client, its sites, tracking IDs, team
- `client_list_websites` when the SOP touches a site
- `client_list_blogs` or `client_list_podcast_episodes` for the deliverable
- the Google Doc, sheet or workbook the SOP names

Tell the person what you could not find, rather than working around it quietly.

## 4. Work the steps

Do what you can do. Say plainly what you cannot.

Plenty of these steps are human — recording a video, taking a screenshot in
Local Falcon, running a client meeting, making a design judgment. Do the parts
that are yours, prepare what you can for the parts that are not, and be explicit
about which is which.

Where a step is mechanical and touches a live site, `/caseengine:check` settles
it. Where it is writing, the `legal-content-review` and `algorithmic-authorship`
skills carry the house rules.

## 5. Do the handoff the SOP asks for

SOPs usually end with one — post the link in the parent thread, tag the PM, mark
it ready for the next stage. That instruction is part of the task, not an
optional nicety, and it is the step most often skipped.

Then close it properly: `/caseengine:prove` if there is something observable, or
`/caseengine:approved` if what you have is a client's sign-off.

## Rules

- **The SOP is the instruction.** If your plan differs from it, say so and why,
  rather than quietly doing something else.
- **Do not tick a step you did not do.** A half-worked SOP reported as complete
  is worse than an honest partial.
- **If the SOP is wrong, say so.** These are living documents written by the
  people doing the work; a step that no longer matches reality is worth flagging
  to them, not silently routing around.
