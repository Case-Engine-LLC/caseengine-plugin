# Report Design - Canonical Look and Feel

The client-facing research report Docs (Entity Research and N-Gram Table) follow one
canonical design, modeled by Gabe. Reproduce it exactly - do not restyle per run.

## Canonical sources

- **Model Doc (the look-and-feel target):** Google Doc id
  `1so3CjXTOg1mFdxKFyKYWklsgFPdt1Kq3ZHsMo8XqjNU`
  ("Entity Research - Car Accidents, Location: FL"). Any question about spacing,
  colors, table treatment, or section order is answered by this Doc.
- **Repo renderer (Supabase-backed, the durable implementation):**
  `scripts/render-research-doc.py` in `Case-Engine-LLC/case-engine-webapp`.
  Renders an `entity_maps` or `podcast_ngram_tables` row into this design and
  updates the existing Google Doc in place (`--update <fileId>`), then PATCHes
  `gdoc_file_id` / `gdoc_url` / `rendered_at` back onto the row.
- **Local markdown-based renderers (same design, file inputs):**
  `~/Desktop/claude_code/scripts/entity-map-branded-docx.py` and
  `~/Desktop/claude_code/scripts/ngram-branded-docx.py`.

## Design spec (summary)

- Roboto throughout. CE blue `#3573FF` for the 32pt cover title, 18pt H1s, and
  divider rules. Ink `#0F172A`, gray `#64748B`, light gray `#94A3B8`.
- Cover: centered CE logo (~3.0 in), doc-type title 32pt bold blue, subtitle
  `{Practice Area} - {Scope label}` 14pt, italic "Prepared by Case Engine",
  `Updated YYYY-MM-DD` line, then a page break.
- Blue bottom-border divider before each H1 section.
- Entity report order: What Is Entity Research? (fixed verbatim text + Roboto
  Mono formula line) -> Summary Findings (vector-space chart, Counts, Tier
  distribution, Localization) -> Detailed Findings (tier tables: 9pt, bold
  entity names, fixed skinny numeric columns, vector strength at 2 decimals)
  -> Localization Summary.
- N-gram report locked order (per pod-2B): Executive Summary (generated
  narrative lead + stat bullets) -> Methodology (static verbatim) -> Collation
  Table (CE-blue header row, white bold header text, compact 8pt body) ->
  static table explainer.
- Footer on every page: centered `Case Engine  |  Confidential` 8pt.
- No em dashes anywhere - plain " - " hyphens only.
- Re-renders always go through `files.update` against the existing fileId
  (docx upload, Drive auto-converts in place). Never `files.create` over an
  existing Doc - a new fileId kills every downstream link.
