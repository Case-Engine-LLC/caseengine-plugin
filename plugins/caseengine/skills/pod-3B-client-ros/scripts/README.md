# Scripts - Client ROS

Bundled scripts the cowork runtime executes during the skill's SOP. Self-contained; dependencies declared in each script's docstring.

## Files

| Script | What it does | Invoked from |
|---|---|---|
| [`build-client-ros-docx.py`](build-client-ros-docx.py) | Reads the Client ROS input data (matching `../references/schemas/client-ros.json`), builds the canonical `Client ROS.docx` (CE-branded cover page, headers, footers, segment tables, per-question prompts with placeholders filled in for the specific firm) and emits a paired `Client ROS.md` (raw markdown source-of-truth, no Drive auto-conversion). Strips pandoc artifacts (`[text]{.underline}` etc.) and converts to proper DOCX underline runs. Never includes legacy "Internal Setup" checklist. Dependencies: `python-docx`. | SOP > Push to Drive > Build CE-branded DOCX |

## Conventions

- **Self-contained.** Each script runs on its own; no shared imports between scripts.
- **Dependencies in docstring.** Top-of-file docstring lists every required + optional Python package.
- **Filename convention sourced externally.** The canonical artifact filename (`Client ROS.md`, `Client ROS.docx`) lives in the [Podcast Drive](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU) doc. If that changes, update this script to match.
- **CE branding sourced externally.** Visual styling pulls from the canonical [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) Drive folder. Don't inline brand details in the script beyond the basic CE color hex codes.
- **Fail gracefully.** If a script can't produce its output, log the failure and exit non-zero. The calling skill ships the run without that artifact and notes the gap in metadata.

## Pandoc artifact handling

Production Client ROS files historically use pandoc-style underlines extensively:
- `[Robert May]{.underline}` for attorney names
- `[O.C.G.A. § 51-12-33]{.underline}` for statutes
- `[Atlanta]{.underline}` for cities
- `[I-285]{.underline}` for highways

The build script handles these in two ways:
- **DOCX output:** convert each `[text]{.underline}` to a proper underlined DOCX run (so it renders as actual underline in Word + Google Docs)
- **MD output:** strip the wrapper, keep just the inner text (so the markdown is clean and downstream-readable)

Same pattern applies to `{.smallcaps}`, `{.mark}`, `{.color=...}` if encountered.

## Versioning

Scripts are versioned with the skill. If a script changes its CLI, update the SKILL.md invocation prose. If a script changes its output shape, bump the corresponding schema in `../references/schemas/`.
