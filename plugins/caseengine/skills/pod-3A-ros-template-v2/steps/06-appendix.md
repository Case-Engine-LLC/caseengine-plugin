# Step 06 - Appendix: Source Question Bank

> **Exec:** deterministic
> **Assets:** none - the bank ships verbatim

## What

Ships the episode's full n-gram bank into the template, unedited and renumbered, on its own page and marked INTERNAL. It is the audit trail that nothing was silently dropped or invented, and the pull pool when a client rejects a short-form question. Good output is a bank whose row count equals the n-gram table's exactly.

## Inputs

- `ngram_rows` - from `steps/02-prepare-inputs.md`, in source order.

## Procedure

1. **Emit the heading** [deterministic] - `# Appendix: Source Question Bank`, H1, starting on a new page.
2. **Emit the internal note** [deterministic] - one line stating the bank is reference rather than script: the short-form questions were rebuilt around search phrasing and attributes, not lifted from here.
3. **Emit every row** [deterministic] - verbatim, renumbered 1..M, in source order. Do not rewrite, merge, trim, or reorder rows.

## Outputs

```
appendix: {row_count: int, rows: [str], renumbered: true}
```

## Validation

- Row count equals the n-gram table row count exactly.
- Rows are byte-identical to the source table apart from renumbering.
- The heading starts a new page.

## Failure modes

| Failure | Exit behavior | Routes to |
|---|---|---|
| A row carries a statute cite that trips the jargon scan | Leave the row alone - the scan is scoped above this heading precisely because the bank is verbatim | `steps/08-qa.md` |
| Row count disagrees with the source table | Fail; a dropped row means the audit trail lies | this step |
| Client rejects a short-form question | Pull its replacement from this bank rather than inventing one | `steps/05-segment-2.md` |
