# schema/

Canonical JSON schemas for the `pod-2B-keyword-research` skill.

- `keyword-research.json` - the shape `keyword-research.json` (the skill's machine-readable output) validates against. Consumed by `pod-2A-entity-research`, `pod-2C-virality-research`, the N-Gram Table, the Topic Planner, and Run of Show (which reads the `search_queries` array verbatim for its Appendix).

If a field is added, renamed, or reordered: edit the schema here first, then update SKILL.md prose, then bump the schema `version` and append to `version_history`.
