# Scripts - Topic Planner

Bundled helper scripts the skill invokes. Two scripts run in the scoring phase (`score-topics.py`, `validate-scoring-model.py`); the rest run in the Push to Drive / render phase. `mahalanobis-score.py` is a legacy optional diagnostic only. All scripts are bundled in this folder so the skill is self-contained — no runtime reach into shared global script directories.

## Inventory

| Script | What it does | Invoked from |
|---|---|---|
| `score-topics.py` | The active scoring engine. Reads the ingested corpus, loads the canonical 11-signal model from `references/scoring-model.json`, and computes the weighted `authority_score` + corroboration flag for every candidate topic. Fully model-driven — signals, weights, buckets, and the corroboration mechanic all come from the JSON model, so adding or reweighting a signal needs no code edit. Emits the `Topic Ideas` table (every candidate in unmodified `authority_score` order) plus a draft Rationale per topic from the signal scores + corroboration flag. Pass `--mahalanobis` to additionally run the legacy diagnostic. | SOP > Create > Score topics |
| `validate-scoring-model.py` | Validator for `references/scoring-model.json`. Checks the model against `references/schema/scoring-model.schema.json` and verifies the weights-sum-to-1.0 invariant within tolerance. Run after any edit to the scoring model so the canonical file never desyncs. | After any `scoring-model.json` edit |
| `mahalanobis-score.py` | LEGACY / optional diagnostic only — not the primary ranking. Runs only when `score-topics.py` is invoked with `--mahalanobis`, as a covariance-corrected cross-check to sanity-test whether correlated signals are double-counting. Reads `01-podcast-topics-ranked.json`, scores episodes via Mahalanobis distance, applies the bridge floor, and generates `visuals/` (correlation heatmap, rank delta chart, entity network graph). The primary ranking is always the 11-signal weighted `authority_score` from `score-topics.py`. | SOP > Create > Score topics (optional `--mahalanobis` cross-check) |
| `render-12-episode-plan.py` | Writes the client-facing `## The 12-Episode Plan` table into the Doc, AND syncs the `## Episode Breakdown` per-episode H3 headings (`Episode N: {title}`) to the selected episode names. Takes `<doc_id> <selection.json>`, reads the `episodes` array. Columns `# / Topic / Theme / Keywords / Rationale`. | SOP > Create > Form the episode plan |
| `render-additional-topics.py` | Writes the client-facing `## Additional Topics` table into the Doc. Takes `<doc_id> <selection.json>`, reads the `additional` array (3 swap-ins, one per category). Columns `Topic / Theme / Keywords / Rationale / Swaps for`. | SOP > Create > Form the episode plan |
| `render-topics-by-score.py` | Writes the INTERNAL `### Topic Ideas` table into the Doc. Takes `<doc_id> <topics-by-score.json>`. Six columns `Rank / Topic / Theme / Score / Rationale / Notes`. | SOP > Create > Score topics |
| `render-episode-question-tables.py` | Writes the `## Episode Breakdown` section - one per-episode question table for every locked episode, built from the `pod-2B-n-gram-table` output. Runs the cross-episode de-duplication pass (exact + near-duplicate), resolves each question's n-grams to keyword MSV for the `Keywords` cell, and puts a divider border between episodes. Episode 1 uses the canonical Founder Story set. Takes `<doc_id> <ngram_dir> <selection.json>`. | SOP > Create > Build the Episode Question Tables |
| `lib_doc_table.py` | Shared helper imported by the `render-*.py` scripts - not run directly. Holds `rebuild_table()` (delete + reinsert + populate + brand a Doc table, cleaning accumulated blank paragraphs) and `keywords_cell()` (the locked Keywords-cell format), plus the `gws` / `get_doc` / `batch` helpers. | (imported) |
| `topic-plan-to-docx.sh` | Pandoc render of the canonical `.md` to a CE-branded `.docx` using `references/templates/topic-plan-reference.docx` as the style template. Optional `--header-anchor` patches the page-header text. | SOP > Push to Drive > Generate local .docx |
| `topic-plan-formatting.sh` | Drive Doc styling pass. Rebuilds cover page (logo + CE Blue subtitle + firm name + location + date), applies Roboto across the body, styles every table (CE Blue header + zebra body rows), marks `# INTERNAL` H1 with a CE Blue top border, sets page header + footer. FIRST-PUBLISH ONLY — re-uploads the markdown and wipes collaborator comments/edits; never run on a shared Doc. | SOP > Push to Drive > Apply branded styling |
| `topic-plan-surgical-edit.sh` | Post-publish edit path. Docs API `replaceAllText` wrapper — `--find "..." --replace "..."`. Touches only the exact text being changed, preserving every comment, suggestion, and collaborator edit. Use this instead of the formatter once the Doc has been shared with anyone. | SOP > Push to Drive > Post-publish edit |
| `topic-plan-client-render.sh` | Produces a CLIENT-SAFE clone of the master Doc by truncating everything from `# INTERNAL` onward, uploads as a NEW Google Doc named `Podcast Topic Plan - {Firm} (Client Share)` into the same parent folder. Does NOT touch the master. | SOP > Push to Drive > Client-share render (optional) |

## Dependencies

- `python3` stdlib only (for `score-topics.py` + `validate-scoring-model.py`)
- `python3` with `numpy`, `matplotlib`, `networkx` (for the legacy `mahalanobis-score.py` diagnostic)
- `python3` with `requests` (for Docs API calls in `topic-plan-formatting.sh` + `topic-plan-surgical-edit.sh`)
- `pandoc` (for `topic-plan-to-docx.sh`)
- `gws` CLI + `op` CLI (for the formatting, surgical-edit, and client-render scripts; credentials resolved via 1Password)

Each script's docstring (top-of-file comment block) documents its full invocation, required flags, and dependencies. Read the script header before invoking.
