---
description: Connect this session to the Case Engine dashboard (mint an MCP key, set it, verify).
---

Get the user connected to the Case Engine dashboard MCP servers, then prove it
works. Do not stop at instructions — verify.

## 1. Check whether it is already working

Call `work_list_items` (no arguments) on the `caseengine-tasks` server.

- **It returns items or an empty list** → already connected. Report the
  identity it resolved (`identity.personName` / `identity.email`) so the user
  can confirm it is really them, and stop here.
- **`401 Unauthorized`** → the key is missing, expired, or revoked. Continue.
- **The tool does not exist / server not connected** → the plugin's MCP
  servers did not load. Confirm the plugin is installed and the session was
  restarted after installing, then continue.

## 2. Mint a key

Tell the user to do this themselves — never ask them to paste an existing key
into chat, and never try to mint one on their behalf:

1. Sign in to <https://tool.caseengine.com>.
2. Open the Copilot widget (chat bubble, bottom-right of any page).
3. Click the **plug** icon in its header — tooltip "MCP connection info".
4. Click **Generate my MCP key**.
5. Copy the `ce_mcp_...` value. **It is shown exactly once.**

Limit is 5 active keys per user. If they hit it, the same panel lists their
existing keys so they can revoke one first.

## 3. Set it in the environment

The key belongs in the environment as `CASE_ENGINE_MCP_KEY`, not in a file in
a repo. Give them the line for their shell:

**PowerShell (this session only)**

```powershell
$env:CASE_ENGINE_MCP_KEY = "ce_mcp_..."
```

**PowerShell (persistent, per-user)**

```powershell
setx CASE_ENGINE_MCP_KEY "ce_mcp_..."
```

**macOS / Linux (add to `~/.zshrc` or `~/.bashrc`)**

```bash
export CASE_ENGINE_MCP_KEY="ce_mcp_..."
```

`setx` and shell-profile edits only affect **new** shells — they must start a
fresh terminal and a fresh Claude Code session afterwards.

## 4. Verify

In the new session, call `work_list_items` again and report:

- the resolved identity (name + email),
- how many open items came back,
- anything in `unmatched` or `errors`.

If it still 401s, the likely causes in order: the env var did not survive into
the new session, the key was truncated on paste, or the key was revoked. Check
`CASE_ENGINE_MCP_KEY` is actually visible to the process before assuming the
key is bad.

## Scope note

A self-serve key is **read-only** and scoped to the `tasks` and
`content_generation` domains. Write tools (`work_create_task`,
`work_transition_task`, `work_approve_step`) return
`{ success: false, error: "missing_capability" }` until Connor grants
`tasks_write` / `tasks_approve` on that key. Site-change tools are a separate
superadmin grant and are not part of this plugin. If a user needs write
access, tell them to ask Connor — do not look for another route in.
