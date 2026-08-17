---
description: Sign in to Case Engine with OAuth and verify the connection.
---

Get the user connected to the Case Engine dashboard MCP servers, then prove it
works. Do not stop at instructions — verify.

## 1. Check whether it is already working

Call `work_list_items` (no arguments) on the `caseengine-tasks` server.
Do not search an MCP registry or plugin catalog: the server is bundled in this
plugin and its tools should already be present in the session.

- **It returns items or an empty list** → already connected. Report the
  identity it resolved (`identity.personName` / `identity.email`) so the user
  can confirm it is really them, and stop here.
- **Claude shows Connect / Sign in** → continue with the browser sign-in.
- **`401 Unauthorized` without a sign-in option** → refresh or restart after
  updating the plugin, then continue.
- **The tool does not exist / server not connected** → the plugin's MCP
  servers did not load. State that exact failure. Do not replace it with a
  walkthrough or claim the user can connect manually. Run `claude mcp list`
  and read the error before doing anything else — in particular, check it
  against the known server-side failure below.

### Known failure: loopback redirect rejected

If `claude mcp list` reports:

```
plugin:caseengine:caseengine-tasks: ... - ✗ Failed to connect —
redirect_uri must be https, or http on a loopback address:
http://localhost:<port>/callback
```

then the plugin is installed correctly and the fault is server-side. The
Case Engine OAuth server's dynamic-client-registration endpoint
(`/api/oauth/register`) rejects `localhost` as a loopback host, and Claude
Code registers exactly that redirect URI. Registration fails, so no Connect
prompt is ever offered.

**Reinstalling the plugin, bumping its version, or starting a new session
will not fix this.** The fix belongs in `case-engine-webapp`: treat the
hostname `localhost` as loopback alongside `127.0.0.1` and `::1`. Report it
and stop; do not loop on plugin reinstalls.

## 2. Sign in

The plugin uses per-user OAuth. Tell the user to click **Connect** or
**Sign in**, then:

1. Sign in to <https://tool.caseengine.com>.
2. Review the Case Engine access request.
3. Click **Allow access**.
4. Return to Claude when the browser redirects back.

Never ask for a key, tell the user to set an environment variable, or direct
them to create a separate custom connector. Authentication belongs to this
plugin and is tied to the Case Engine account that approves access.

## 3. Verify

In the new session, call `work_list_items` again and report:

- the resolved identity (name + email),
- how many open items came back,
- anything in `unmatched` or `errors`.

If it still 401s, disconnect and reconnect the Case Engine plugin, confirm the
same Case Engine account completed consent, then retry in a fresh conversation.

## Scope note

An OAuth grant is **read-only** and scoped to the `tasks` and
`content_generation` domains. Write tools (`work_create_task`,
`work_transition_task`, `work_approve_step`) return
`{ success: false, error: "missing_capability" }`. Site-change tools are a
separate superadmin grant and are not part of this plugin. Do not look for
another route around those controls.
