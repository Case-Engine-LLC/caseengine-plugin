# Schemas - Pod Virality Research

Machine-readable JSON schemas declaring the shape of structured outputs.

| File | Purpose | Consumed by |
|---|---|---|
| `virality-research.json` | Scored candidate list with virality_score, tier, emotional hook category, prominence flag, signal breakdown, provenance | `/pod-2A-topic-planner` (boosts composite scores by tier) |

Downstream skills validate output against these schemas. If the schema changes, bump the skill version and update the iteration log.
