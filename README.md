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

### Resolved: OAuth loopback redirect

Connecting used to fail in Claude Code with `redirect_uri must be https, or
http on a loopback address: http://localhost:<port>/callback` —
`/api/oauth/register` rejected the `localhost` form Claude Code registers.
Fixed server-side in `case-engine-webapp`
[#1587](https://github.com/Case-Engine-LLC/case-engine-webapp/pull/1587),
merged 2026-08-11 and live on `main`. If a teammate still hits this exact
error, they're likely on a session that predates the fix — have them retry
`/caseengine:connect` in a fresh session before assuming it's back.

Validate before pushing:

```bash
claude plugin validate ./plugins/caseengine --strict
```
