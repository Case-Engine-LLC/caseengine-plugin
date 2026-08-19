# Case Engine plugin for Claude

Connects Claude to the **Case Engine dashboard** (`tool.caseengine.com`)
so you can pull your task queue, read tasks and approvals, dump a client
profile, and drive content generation from Claude Chat, Cowork, Desktop, or
Claude Code.

This is why "pull the tasks from the CE dashboard" used to come back *not
connected*: nothing was wired up. This plugin is the wiring.

## Install

```bash
claude plugin marketplace add Case-Engine-LLC/caseengine-plugin
```

```bash
claude plugin install caseengine@caseengine
```

## Connect

Run `/caseengine:connect` and follow it. In short:

1. Click **Connect** or **Sign in** when Claude prompts you.
2. Sign in to <https://tool.caseengine.com>.
3. Review the access request and click **Allow access**.
4. Return to Claude. No key or environment variable is required.

## Commands

| Command | Does |
|---|---|
| `/caseengine:connect` | Sign in with Case Engine and verify the connection end-to-end |
| `/caseengine:my-tasks` | Your open work queue, or one client's |
| `/caseengine:meeting-doc` | Build a client meeting doc from live board data |

You do not have to use the commands. With the plugin installed, "what's on my
plate in CE?" or "pull Wolf's open tasks" routes correctly on its own.

## What it can do

**`caseengine-tasks`** — `work_list_items`, `work_get_task`, `work_list_tasks`,
`work_list_people`, `work_team_workload`, `work_list_approvals`,
`client_get_profile`, plus (capability-gated) `work_create_task`,
`work_assign_task`, `work_transition_task`, `work_approve_step`. Creating or
assigning a task to someone else needs no special role beyond the standard
OAuth grant below — resolve their id with `work_list_people` first.

**`caseengine-content`** — list/get content pieces, poll and start generation
jobs, cancel a job, transition a piece.

## What it deliberately can't do

- **Publish to WordPress.** Not exposed. `content_transition_piece` does not
  accept `'published'`.
- **Approve your own work.** Enforced in the underlying service, not just
  here — this holds even though the OAuth grant below includes
  `tasks_approve`.
- **Write content generation through the default OAuth grant.** OAuth access
  for `content_generation` stays read-only.
- **Touch site changes.** Separate superadmin domain, not bundled here.
- **Touch ClickUp.** Retired.

## Security

OAuth is per-user and tied to the Case Engine account that approved access.
Claude receives opaque, short-lived access tokens and rotates refresh tokens;
no Case Engine password or copied API key is stored in the plugin.

## Not to be confused with

The **Content Generator MCP** at `contentgenapi.caseengine.com` — a separate
external server with its own shared secret, configured at
`/content-generation/setup` in the dashboard. Different thing.
