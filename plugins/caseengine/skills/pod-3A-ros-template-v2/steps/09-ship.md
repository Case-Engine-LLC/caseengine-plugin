# Step 09 - Ship

> **Exec:** script + deterministic
> **Assets:** `scripts/build-ros-template-v2-docx.py`, `references/cover-spec.json`

## What

Builds the CE-branded DOCX and writes the trio plus metadata to the shared template library scope folder and the local mirror, then reports back. Good output is a branded Google Doc at a stable fileId, a raw markdown sibling, the payload, and metadata - in the template library, never in a client folder.

## Inputs

- `artifacts` - from `steps/07-render.md`.
- `destination_folder` - resolved and gated in `steps/01-prerequisites.md`.
- Branding - from `steps/02-prepare-inputs.md`.

## Procedure

1. **Build the DOCX** [script: `scripts/build-ros-template-v2-docx.py`] - reads the payload, emits the `.docx` and its paired `.md` in one pass, preserves `{{PLACEHOLDER}}` tokens verbatim, applies CE branding with Roboto throughout.
2. **Write to Drive** [deterministic] - upload the `.docx` as `application/vnd.google-apps.document` so Drive converts it to a clean branded Doc; upload the `.md` as `text/markdown` with no conversion; upload the JSONs as-is. First run uses `files.create`; every run after uses `files.update` against the existing fileId so the URL never breaks for downstream links. Never delete-and-reupload.
3. **Write the local mirror** [deterministic] - the same `.md`, `.docx`, and JSONs to `~/Desktop/claude_code/deliverables/podcast/ROS Templates/{Topic}/{Episode}/{scope}/`.
4. **Verify the render** [deterministic] - confirm Roboto over the full range and zero leaked inline markup as visible text.
5. **Report back** [deterministic] - folder link, Doc link, format summary, location and question counts, geo plan, placeholder count, attribute source, QA result, and the open ship blockers.

## Outputs

```
shipped: {
  doc_url: str, doc_id: str, folder_id: str,
  markdown: path, payload: path, metadata: path,
  mirror: path, partial: bool
}
```

## Validation

- Every filename carries the `v2` marker. No write path resolves to a legacy artifact name.
- The destination is inside `templates [master]/AEO Templates/Podcast/Episode Templates/` at the Map 2 path - never a client or firm episode folder.
- The Doc was built from the DOCX, not from a raw-markdown upload.
- Both destinations written, or the partial state is surfaced in the report.

## Failure modes

| Failure | Exit behavior | Routes to |
|---|---|---|
| One destination errors | Ship to the other, surface the partial state - never silently lose the deliverable | continue |
| Both destinations error | Hard-fail with the reason; render inline so the work is not lost | halt |
| `python-docx` missing | Ship markdown and JSON, defer the branded Doc, surface the gap - never skip it silently | continue |
| A prior v2 template exists and archive was requested | Move only the prior v2 file to `_archive-{YYYY-MM-DD}/`; never touch a legacy sibling or a Client ROS | continue |
