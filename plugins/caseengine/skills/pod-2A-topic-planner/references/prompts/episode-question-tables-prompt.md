# Episode Question Tables — phase 2 prompt (pod-2A-topic-planner)

The live prompt for the **final build step**: turn the per-episode n-gram tables into the client-facing `## Episode Breakdown` question tables, then run a cross-episode de-duplication pass so no question repeats across the plan.

Triggers automatically once `pod-2B-n-gram-table` has built an n-gram table for every locked episode (main 12 except Episode 1, plus the 3 additional topics). This is the last step of the topic plan.

---

## Inputs

1. **The n-gram tables** — one per episode, from `pod-2B-n-gram-table`. Each carries that episode's question set (the n-gram collation table: Question, N-grams, Entities, Predicates).
2. **The locked plan** — `## The 12-Episode Plan` (12 episodes) and `## Additional Topics` (3).
3. **`references/e1-founder-interview-questions.md`** — the canonical Episode 1 question set.

## Step 1 — Build each per-episode question table

For every episode 2-12 and every additional topic, populate its `## Episode Breakdown` table from that episode's n-gram table. Columns, in exact order: `Question`, `Search Phrases`, `Rationale`.

- **Question** — the question lifted from the episode's n-gram table.
- **Search Phrases** — the search phrases / n-grams behind that question, from the n-gram table.
- **Rationale** — a SHORT plain-language summary of the research signal behind the question: "comes up heavily in People Also Ask", "triggers an AI Overview", "strong related-search cluster". It is a summary of the cited research, never a direct citation, and never filler. Name the real signal (see Editorial Guideline 2 in `SKILL.md`).

**Episode 1 is the standing exception.** `The Founder Interview` is never n-gram-built. Its table is the canonical Founder Story interview set from `references/e1-founder-interview-questions.md` — two columns `Question` / `Rationale`, the 21 questions unnumbered, the Rationale a hard-coded interview-purpose note (establish credibility, position as expert, build local trust, emotional close).

## Step 2 — Cross-episode de-duplication pass

After every per-episode table is built, look at all questions across all episodes together. **No question may appear in two episodes.** If question A is asked in Episode 1, it must not also be asked in Episode 2.

- When a duplicate (or a near-duplicate that a host would experience as the same question) is found, keep it in the episode where it fits best — the strongest topical match, or the earlier funnel stage — and drop it from the other episode.
- Backfill the dropped slot with the next-best unused question from that episode's own n-gram table.
- Re-scan after every change. Repeat until every question across the whole plan is unique.

This is a distinct pass — it may run as its own step/script triggered after all per-episode tables are populated. It looks at the plan as a whole, not one episode at a time.

## Output

`## Episode Breakdown` fully populated — every episode's question table filled from its n-gram table, Episode 1 from the canonical set, and zero cross-episode question overlap across the entire plan.
