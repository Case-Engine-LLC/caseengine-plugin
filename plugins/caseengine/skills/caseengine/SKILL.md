---
name: caseengine
description: Read and act on work in the Case Engine dashboard — the internal staff tool at tool.caseengine.com. Use whenever someone refers to "the CE dashboard", "the CE tool", "Case Engine", "the dashboard", "the tool", "my tasks", "our tasks", "the task board", "the work queue", "approvals", "a client profile", or asks to pull Case Engine data into a meeting doc, status update, brief, or report. Also use for content-generation pieces and jobs. Covers which MCP tools exist, how to authenticate, and the naming so a request phrased any of those ways resolves to the right server instead of "not connected".
---

# Case Engine dashboard

## What it is (and what it is called)

The **Case Engine dashboard** is the internal staff platform at
`https://tool.caseengine.com`. People on the team call it, interchangeably:

- "the CE dashboard" / "the CE tool" / "CE"
- "Case Engine" / "the Case Engine dashboard"
- "the dashboard" / "the tool" (when no other product is in play)
- "the task board" / "my tasks" / "the work queue"

All of those mean this one system. It is reached through the MCP servers this
plugin installs — **not** through a browser, a scrape, or a Supabase query.

Two adjacent things it is **not**:

- **ClickUp.** Retired. Do not create, close, or comment on ClickUp work.
  Native `campaign_plan` / `campaign_task` lifecycle is the only operational
  task system. `work_list_items` no longer has a `clickup` source at all —
  it used to, and would routinely fail with an aggregator error
  (`invalid input syntax for type json`) reading the stale ClickUp mirror
  table. If you see a `clickup` entry in `errors` again, that's a
  regression, not expected noise — say so rather than reporting a partial
  queue as complete.
- **The Content Generator MCP** at `contentgenapi.caseengine.com`. That is a
  separate external server with its own shared secret. This plugin's
  `caseengine-content` server is the dashboard's own per-user content layer.

## Servers this plugin installs

| Server | Endpoint | Covers |
|---|---|---|
| `caseengine-tasks` | `/api/mcp/tasks` | work queue, tasks, approvals, client profiles |
| `caseengine-content` | `/api/mcp/content-generation` | content pieces, generation jobs |

Both authenticate with per-user OAuth through the Case Engine plugin. If Claude
shows a Connect or Sign in action, have the user complete it. If tool calls
still return `401 Unauthorized`, send the user to `/caseengine:connect`; never
ask for a key or an environment variable.

## Tools

### Reading work

- `work_list_items` — the main entry point. Lists work items across every
  lifecycle source (delivery, internal, marker, request, approval) through the
  unified aggregator.
  - Omit `client_id` for the caller's **own** "my work" view.
  - Pass `client_id` for one client's queue.
  - `include_closed: true` to see completed items (default is open only).
  - Paginated — `limit` (default 100, max 500) and `offset`; the response
    carries `total_count` and `has_more`. A default-scoped personal query
    across every source routinely runs past 500 open items, so check
    `has_more` before treating a page as the whole queue.
  - Every row carries **two** statuses. `status` is the canonical bucket
    (`backlog` / `active` / `blocked` / `in_review` / `approved` / `done` /
    `dropped`); `rawStatus` is the source's own value (`todo`,
    `in_progress`, `needs_approval`, …). Only `rawStatus` is a legal
    `work_transition_task` argument. The response ships `status_legend`,
    `my_role_legend` and `counting_basis` so the mapping is on screen rather
    than guessed — including `myRole: "both"`, a task where the caller is
    deliverer *and* verifier (self-review, no second pair of eyes).
- `work_get_task` — one `campaign_task` by id, full row (including
  `description`, the SOP body the list tools omit), plus `url`: the task's
  in-app deep link (`https://tool.caseengine.com/my-tasks?taskId=…`) and
  `allowed_transitions`, the statuses `work_transition_task` will accept from
  where this task is now.
- `work_list_tasks` — one selected person's tasks across all clients (or the
  whole team's), with an `active_only` filter — the team-planning counterpart
  to `work_list_items`'s "my work" view. Each task includes `url`. Also
  paginated — `limit` (default 200, max 1000) and `offset`, response carries
  `total_count`/`has_more`. Pass `active_only: true` whenever you don't
  specifically need closed/cancelled history — an unfiltered pull for one
  person can be 800+ rows. Rows return a summary field set that omits
  `description` (the SOP markdown, byte-identical across every task built
  from the same template item) and report `description_chars` instead; pass
  `fields: [...]` to choose columns explicitly, or read the one task you
  actually need with `work_get_task`. `status` here is the **raw** value.
- `work_list_people` — the active staff directory (id, full_name, job_title,
  email, status). Use this to resolve a name like "Connor Gallic" to a
  `person_id` before assigning a task to them — there is no name-matching
  argument on the write tools themselves, by design (a prior fuzzy-match
  helper elsewhere in the system was removed after it silently matched the
  wrong person).
- `work_team_workload` — open/overdue/awaiting-review counts per person, as of
  a given date, for reasoning about who's overloaded. Counts `campaign_task`
  only, and `open` counts only tasks a person **delivers** — verifier work is
  in `awaiting_review`, and the other five sources are not counted. That is a
  narrower question than `work_list_items` answers, so the two totals differ
  by design; the response returns `counting_basis` and `tasks_counted` saying
  which. Do not present one number as a correction of the other.
- `work_list_approvals` — approvals with their steps; filter by `client_id`,
  `entity_type`, `status`.
- `client_list` — the client directory: `id`, `name`, `official_name`, `slug`,
  `aliases`, `status`, `canonical_id`, `merged_into`. The client-side
  counterpart to `work_list_people`, and the way to turn a spoken name into an
  exact id. Filter with `query` (matches name, official name, slug and
  aliases), `status`, `include_inactive`, `include_merged`.
- `client_get_profile` — full client dump by UUID **or slug**: the `clients`
  row plus branding, integrations, SEO config, services, team assignments,
  websites, custom fields, links, GBP locations, social accounts. Null columns
  and `gbp_embed_code` (`<iframe>` markup, one per location) are omitted by
  default — pass `include_null_fields` / `include_embed_codes` when you
  genuinely need them.

### Writing work

- `work_create_task` — create a one-off internal task. Defaults to
  self-assigned; pass `deliverer_person_id` (and optionally
  `verifier_person_id`) to assign it to someone else at creation time —
  resolve the name to an id via `work_list_people` first.
- `work_assign_task` — reassign an **existing** task's deliverer or verifier
  to someone else. Use this instead of `work_create_task` when the task
  already exists. No ownership check beyond the target being an active person
  — the same bar the staff UI holds.
- `work_transition_task` — move a task to a new status. `status` is a fixed
  set — `todo`, `in_progress`, `needs_approval`, `approved`, `done`,
  `blocked`, `cancelled` — enumerated in the tool's own schema, so read it
  there rather than guessing between `done`/`complete` or
  `cancelled`/`canceled`. It takes the **raw** value, not the canonical
  bucket `work_list_items` shows in `status`.
- `work_approve_step` — approve or reject a manual approval step.

Staff can write. Creating, assigning, transitioning and approving work all
just work — the server grants that from the caller's team-member record, not
from how they connected, so there is nothing here to check, configure, or
explain to the user before calling a write tool. (Self-approval is still
blocked in the underlying service — a person can't sign off on their own work
through this API any more than through the UI.)

If a write ever returns `{ success: false, error: "missing_capability" }`,
that is an account-access problem on the server side, not something the user
can fix by reconnecting or by using a different credential. Say what failed
and stop; do not send anyone off to mint a key.

### Content generation

`content_generation_list_pieces`, `content_generation_get_piece`,
`content_generation_get_job_status`, `content_start_generation`,
`content_generation_cancel_job`, `content_transition_piece`.

`content_transition_piece` deliberately does not accept `'published'` —
publishing to WordPress is not exposed through MCP.

## How to use it well

**Start with `work_list_items`.** Almost every request ("what's on my plate",
"what's open for Wolf", "pull tasks for the meeting doc") is that call plus
filtering. Do not reach for `work_get_task` in a loop until you know which
tasks matter.

**Resolve the client first when a name is mentioned — from `client_list`, not
from a guess.** Every `client_*` tool and `client_id` filter takes a UUID or a
slug, and a wrong slug returns an empty result that looks exactly like a client
with no work. Call `client_list({ query: "wolf" })`, pick the exact `id`, and
use it — the same discipline `work_list_people` exists to enforce for people.
Guessing a slug from a firm's name is how you report "nothing open" for a busy
client.

**Report what the data says.** These tools return the real board state. If a
queue is empty, say it is empty — do not pad a meeting doc with plausible
work. `work_list_items` also returns `unmatched` and `errors`; if either is
non-empty, surface it rather than silently presenting a partial list.

**Watch `has_more`.** `work_list_items` and `work_list_tasks` are both
paginated (see above). A truncated page silently presented as the whole
queue is worse than the same page with "and N more" — check `has_more`
before you say "that's everything," and page with `offset` (or narrow with
`client_id`/`active_only`) instead of assuming one call got it all.

**Link back to the dashboard, don't paraphrase an id.** Every task-shaped
result now carries a ready-to-use `url` — a bare id or a hand-built path is
never necessary. When presenting tasks to a person, use that `url` directly
rather than composing one.

**Never invent a task from a meeting.** Fathom recordings, transcripts, and
extracted action items are evidence, not authority. Do not call
`work_create_task` for something that merely came up in a meeting — present
the proposed items and get explicit per-item human confirmation first.

**Identity comes from OAuth.** The caller is resolved server-side from the
Case Engine account that authorized the plugin. There is no "acting as"
argument, and self-approval is
blocked in the underlying service — a person cannot sign off on their own
work through this API any more than through the UI.

## Connecting

`/caseengine:connect` walks through it. The user clicks **Connect** or
**Sign in**, signs into `https://tool.caseengine.com`, reviews the requested
access, and clicks **Allow access**. Claude stores and refreshes the OAuth
credential. No key is copied and no environment variable is required.
