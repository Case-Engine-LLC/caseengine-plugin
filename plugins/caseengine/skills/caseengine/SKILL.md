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
  task system.
- **The Content Generator MCP** at `contentgenapi.caseengine.com`. That is a
  separate external server with its own shared secret. This plugin's
  `caseengine-content` server is the dashboard's own per-user content layer.

## Servers this plugin installs

| Server | Endpoint | Covers |
|---|---|---|
| `caseengine-tasks` | `/api/mcp/tasks` | work queue, tasks, approvals, client profiles |
| `caseengine-content` | `/api/mcp/content-generation` | content pieces, generation jobs |

Both authenticate with a per-user key in `CASE_ENGINE_MCP_KEY`. If tool calls
come back `401 Unauthorized`, the key is missing, expired, or revoked — send
the user to `/caseengine:connect`, do not work around it.

## Tools

### Reading work

- `work_list_items` — the main entry point. Lists work items across every
  lifecycle source (delivery, internal, marker, request, approval) through the
  unified aggregator.
  - Omit `client_id` for the caller's **own** "my work" view.
  - Pass `client_id` for one client's queue.
  - `include_closed: true` to see completed items (default is open only).
- `work_get_task` — one `campaign_task` by id, full row.
- `work_list_approvals` — approvals with their steps; filter by `client_id`,
  `entity_type`, `status`.
- `client_get_profile` — full client dump by UUID **or slug**: the `clients`
  row plus branding, integrations, SEO config, services, team assignments,
  websites, custom fields, links, GBP locations, social accounts.

### Writing work

- `work_create_task` — create a one-off internal task. **Always self-assigned**
  to the caller; there is no "assign to someone else" option.
- `work_transition_task` — move a task to a new status.
- `work_approve_step` — approve or reject a manual approval step.

Write tools need capabilities on the key (`tasks_write`, and `tasks_approve`
for approving). A self-serve key is **read-only** by default and returns
`{ success: false, error: "missing_capability", required: "tasks_write" }`.
That is a scope grant from Connor, not a bug to route around.

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

**Resolve the client first when a name is mentioned.** `client_get_profile`
accepts a slug, so `client_get_profile({ client_id: "wolf-of-law-street" })`
works without a UUID lookup. Use the returned `client.id` for
`work_list_items`.

**Report what the data says.** These tools return the real board state. If a
queue is empty, say it is empty — do not pad a meeting doc with plausible
work. `work_list_items` also returns `unmatched` and `errors`; if either is
non-empty, surface it rather than silently presenting a partial list.

**Never invent a task from a meeting.** Fathom recordings, transcripts, and
extracted action items are evidence, not authority. Do not call
`work_create_task` for something that merely came up in a meeting — present
the proposed items and get explicit per-item human confirmation first.

**Identity comes from the key.** The caller is resolved server-side from
`CASE_ENGINE_MCP_KEY`. There is no "acting as" argument, and self-approval is
blocked in the underlying service — a person cannot sign off on their own
work through this API any more than through the UI.

## Getting a key

`/caseengine:connect` walks through it. Short version: sign in to
`https://tool.caseengine.com`, open the Copilot widget, click the **plug**
icon ("MCP connection info"), click **Generate my MCP key**, copy the
`ce_mcp_...` value (shown once), and set it as `CASE_ENGINE_MCP_KEY` in the
environment. Max 5 active keys per user; revoke an old one before minting a
sixth.
