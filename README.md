# Case Engine plugin marketplace

Internal Claude Code marketplace for Case Engine staff. One plugin today:
[`caseengine`](./plugins/caseengine) — connects Claude Code to the Case Engine
dashboard at `tool.caseengine.com`.

## For teammates

```bash
claude plugin marketplace add Case-Engine-LLC/caseengine-plugin
```

```bash
claude plugin install caseengine@caseengine
```

Then run `/caseengine:connect` in a new session.

Full setup, tool inventory, and the security model: [plugins/caseengine/README.md](./plugins/caseengine/README.md).

## For maintainers

The MCP servers this plugin points at live in
[`Case-Engine-LLC/case-engine-webapp`](https://github.com/Case-Engine-LLC/case-engine-webapp):

| Piece | Path in the webapp |
|---|---|
| Transport (JSON-RPC over HTTP) | `src/lib/mcp/server.ts` |
| Auth / key validation | `src/lib/mcp/auth.ts` |
| Scope + capability gates | `src/lib/mcp/capabilities.ts` |
| Tasks tools | `src/lib/mcp/catalogs/tasks.ts` |
| Content-generation tools | `src/lib/mcp/catalogs/content-generation.ts` |
| Routes | `src/app/api/mcp/*/route.ts` |
| Self-serve key minting | `src/app/api/mcp/key/route.ts` |
| In-app connect panel | `src/components/copilot/McpInfoPanel.tsx` |

**Adding a tool** is a webapp change, not a plugin change — add it to the
catalog and it appears in `tools/list` automatically. Only update this repo
when the tool inventory in `skills/caseengine/SKILL.md` drifts far enough to
mislead, or when a new domain/server needs adding to the `mcpServers` block
in `plugins/caseengine/.claude-plugin/plugin.json`.

### Known blocker: OAuth loopback redirect

Connecting currently fails in Claude Code with:

```
✗ Failed to connect — redirect_uri must be https, or http on a
loopback address: http://localhost:<port>/callback
```

This is **not** a plugin bug. `/api/oauth/register` accepts
`http://127.0.0.1:<port>/callback` but rejects `http://localhost:<port>/callback`,
and Claude Code registers the `localhost` form. Because dynamic client
registration fails, no Connect prompt is ever shown.

Fix belongs in `case-engine-webapp`'s redirect-URI validator: treat the
hostname `localhost` as loopback alongside the `127.0.0.1` and `::1` literals
(RFC 8252 §7.3). Until that ships, no change in this repo will connect the
plugin — do not bump versions chasing it.

Validate before pushing:

```bash
claude plugin validate ./plugins/caseengine --strict
```
