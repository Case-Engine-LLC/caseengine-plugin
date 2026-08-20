# Select Episodes — phase 3 prompt (pod-2A-topic-planner)

The live prompt for the **episode selection** step. Runs AFTER the `## Topic Ideas` table is populated and reviewed — it turns the raw scored candidate set into the curated `## The 12-Episode Plan` and `## Additional Topics`, and writes each candidate's disposition into the `Notes` column.

This step is the SOP's `### Compile into episodes` + `### Form the episode plan` work, run as one discrete, human-gated pass. It does not re-score — scoring already happened.

---

## Inputs

1. **The scored candidate set** — the `topics_by_score` array from `topic-plan-v{n}.json` (every candidate in raw `authority_score` order, each with its `Theme`, `corroboration_flag`, signal data, and `Rationale`). The rendered `## Topic Ideas` table is the human-readable view of the same data.
2. **Practice-area mix** — read from the `Topic Mix` field of `## Show Identity`. That field is the source of truth for the slot split:
   - If the client **expressly stated a breakdown** at intake, the `Topic Mix` field holds it verbatim and it governs how the 11 thematic slots split across practice areas (e.g. "50% car accidents, 40% truck accidents, the rest split across motorcycle and rideshare").
   - If **no breakdown was given and the firm is Personal Injury**, the `Topic Mix` field carries the **CE Default practice-area mix**: Car Accidents 25% (slots 3,4,6), Medical Malpractice 17% (slots 5,9), Truck Accidents 17% (slots 7,12), Cross-Service Roundup 8% (slot 2), Wrongful Death 8% (slot 8), Founder Story 8% (slot 1), Slip & Fall 8% (slot 11), Bicycle / Pedestrian 8% (slot 10) — trimmed to the areas the firm actually practices, reallocating dropped slots to the next-ranked Car Accidents episode then the highest-scoring remaining confirmed-area episode. Slot 1 stays the Founder Interview, slot 2 stays the Cross-Service Roundup (never dropped — spans the confirmed services), slot 3 stays the flagship ebook anchor (top Car Accidents comprehensive guide). Scoring decides which episode fills each slot; the mix fixes the quota.
   - If **no breakdown was given and the firm is not Personal Injury** (Family Law, Criminal Defense, etc.), the `Topic Mix` field carries the scoring-derived distribution — computed from where search demand, entity coverage, and competitive opportunity actually concentrated across practice areas. In that case pure scoring decides the slots.
   - A preference brief supplied directly at this step overrides the `Topic Mix` field.
3. **The client-preference brief** — supplied by the user / AM at this step, on top of the mix:
   - **Must-include** — topics the client explicitly wants recorded regardless of score.
   - **Must-exclude** — topics to drop (refers the work out, already covered, not a fit).
   - **Emphasis** — any practice area or angle to weight up (e.g. "truck is the priority").
4. **Already-covered episodes (user-supplied)** — practice areas / topics already covered by a shipped Run of Show. Anything already shipped is not re-proposed.

## Steps

1. **Compile.** Group the atomic scored topics into episode-sized units. Two topics belong in one episode when a host would cover them in one coherent 60-90 minute conversation — detection: entity overlap > 50% OR primary-keyword overlap > 40%, or they are plainly sub-angles of one discussion. Each compiled episode inherits the aggregate `authority_score` of its member topics and the strongest `corroboration_flag` among them. The episode boundary is decided HERE — the 12 are compiled units, never "the top 12 rows."
2. **Rank** the compiled episodes by aggregate `authority_score`. Use the `corroboration_flag` as a confidence read and a near-tie breaker — NOT as a hard floor (see the note below).
3. **Apply the mix.** Fill each practice area's slot quota with its top-ranked compiled episodes. Quota source by precedence: a client breakdown if given; else the CE Default PI mix for a PI firm; else (non-PI, no breakdown) take the top 11 by rank with no quota. Force in every must-include; drop every must-exclude.
4. **Lock the 12.** Slot 1 is always **Episode 1, "The Founder Interview," Founder Story** — fixed, never scored, never compiled. Slots 2-12 are the 11 selected compiled episodes. **Distinctness check:** no two of the 12 may cover the same primary concept, and no two may be so similar a host could not record them as genuinely separate episodes. If two selected episodes are not distinct enough, merge them into one and pull the next-ranked compiled episode in the same category, or drop the weaker one. Run the same check across the 3 additionals — each additional must be distinct from every main episode and from the other additionals.
5. **Pick exactly 3 Additional Topics — one per category.** For a PI firm on the Default mix: one Car Accidents alternate, one Medical Malpractice alternate, and one Truck Accidents alternate — the next-ranked compiled episode in each. If the firm doesn't practice one of those, substitute the next category by quota weight (Wrongful Death → Slip & Fall → Bicycle / Pedestrian). When a client breakdown governs the mix, the three categories follow that breakdown's heaviest areas. The Additional Topics table has NO `Swaps for` column (removed v4.4.0) — if you want to record which main episode a candidate could replace and the condition that justifies the swap, put that note in the candidate's `Notes` cell in the INTERNAL `## Topic Ideas` table (step 7), not in the Additional Topics table.
6. **Funnel check.** Confirm the 12 span `awareness` / `consideration` / `decision` intent stages. If the set is lopsided, swap a near-rank episode to balance the funnel.
7. **Write the `Notes` column.** For EVERY row of the `## Topic Ideas` table, stamp the disposition into its `Notes` column — exactly one per candidate:
   - `MAIN-{n}` — landed in the curated 12, with the episode number.
   - `BONUS` — in the Additional Topics swap pool.
   - `RESERVE` — not selected; available for a future season or short-form content.
   - `CUT — {reason}` — explicitly killed, with the reason (duplicate of X, refers out, no demand).
   The `Notes` column is the single source of truth for what made the cut. The `## The 12-Episode Plan` and `## Additional Topics` tables render from the `MAIN-#` and `BONUS` rows.
8. **Render** the `## The 12-Episode Plan` and `## Additional Topics` tables from the dispositioned set.

## Output

The populated `## The 12-Episode Plan` table, the `## Additional Topics` table, and the `Notes` column filled for all candidates. **Propose, do not finalize** — present the proposed plan for human review (AM / Gabe) before it is locked. This step drafts; the human approves.

## Note — the corroboration floor

The `corroboration_flag` is a confidence signal, not an automatic promotion. Do NOT let a low-scoring corroborated topic displace a high-scoring topic purely on the flag. Use the flag to break near-ties and to read confidence; let the weighted `authority_score` plus the client-preference brief drive selection. (The floor in `score-topics.py` currently over-promotes corroborated topics globally — until that is fixed, treat the flag as advisory at this step.)
