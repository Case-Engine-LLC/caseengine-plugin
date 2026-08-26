# Step 01 - Prerequisites

> **Exec:** deterministic, plus one HUMAN gate (the format flag)
> **Assets:** `references/iteration-log.json`

## What

The pre-flight. Locks in which capabilities are reachable, resolves the `episode_format` gate that decides whether this skill runs at all, confirms the upstream research artifacts exist at the matching scope, and routes the run to create or update. Good output is a run that either proceeds with every dependency confirmed, or stops early with a named reason and a route.

## Inputs

- `episode`, `topic`, `scope` (Topic Only | Location | Extension), `location` - the run request.
- `episode_format` - **from the user**, asked outright. Pre-filled from `podcast-overview.md` when that doc is reachable and carries the field, but the user's answer is the authority.
- `references/iteration-log.json` - open and in-progress entries, surfaced as known issues.

## Procedure

1. **Read the iteration log** [deterministic] - filter to `status: open` and `status: in-progress` and surface them. Critical entries are ship blockers; surface those every run until they clear.
2. **Probe capabilities** [deterministic] - local filesystem read at `~/Desktop/claude_code/deliverables/podcast/`, `gws drive about` as a try-and-succeed Drive probe, `mcp__ce-services__rag_query` availability, write reach on both destinations, and `python-docx` importability for the renderer. Probe capability, never environment name. Persist the result with a timestamp; later steps read the lock-in rather than re-probing.
3. **Resolve the format flag** [HUMAN gate] - ask: "Is this episode running the v2 open-interview format or the legacy segmented format?" Anything other than an explicit `v2-open-interview` - including "not sure", blank, or no answer - means STOP and route to `/pod-3A-ros-template`. Absence is never permission. Record the answer and who gave it.
4. **Episode 1 exception** [deterministic] - if the requested episode is Episode 1, this skill generates nothing regardless of format. The Founder Story uses its own fixed template; route to `/pod-3B-client-ros`.
5. **Verify upstream** [deterministic] - resolve the n-gram table and the entity map AT THE MATCHING SCOPE. Either missing is a hard stop routing to its upstream skill. A parent-scope artifact is not a substitute; running on one is a silent localization leak.
6. **Reconcile bank against plan** [deterministic] - compare the episode's n-gram questions against the same episode's breakdown in the published Topic Plan Doc. Drift between the two upstream artifacts is a defect even though v2 no longer scripts from the bank; flag and reconcile before generating.
7. **Existence check** [deterministic] - look for a prior `ROS Template v2` + `ros-template-v2-data.json` in the resolved scope folder. A legacy `ROS Template` does NOT count. Found routes to `steps/update-mode.md`; missing continues the create path.

## Outputs

```
run_context: {
  episode, topic, scope, location,
  episode_format: "v2-open-interview",
  episode_format_source: "user:{who}" | "podcast-overview:{path}",
  capabilities: {...}, probe_timestamp: str,
  ngram_path: str, entity_map_path: str, clusters_path: str|null,
  destination_folder: str, legacy_sibling_present: bool,
  mode: "create" | "update",
  open_iteration_log_entries: [...]
}
```

## Validation

- `episode_format` is an explicit `v2-open-interview` from a named source. No inference.
- N-gram table and entity map both resolved, both at the requested scope.
- Destination resolves inside `templates [master]/AEO Templates/Podcast/Episode Templates/`. Anything else - especially a client delivery folder - fails here, and an instruction to redirect it there is itself the failure.
- No planned write path collides with a legacy artifact name.

## Failure modes

| Failure | Exit behavior | Routes to |
|---|---|---|
| Format flag is anything but explicit v2 | Stop. Do not offer to build v2 anyway | `/pod-3A-ros-template` |
| Episode 1 requested | Stop; Founder Story is hardcoded | `/pod-3B-client-ros` |
| N-gram table missing at scope | Stop | `/pod-2B-n-gram-table` |
| Entity map missing at scope | Stop; never substitute a parent scope | `/pod-1A-entity-research` |
| Destination resolves outside the template library | Refuse to write | halt |
| Undeclared upstream file in play (e.g. keyword research) | Ask whether to mine, skip, or pause; never guess | user |
