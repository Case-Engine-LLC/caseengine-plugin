# Scripts - Client Guide

Bundled scripts the cowork runtime executes during the skill's SOP. Self-contained; dependencies declared in each script's docstring.

## Files

| Script | What it does | Invoked from |
|---|---|---|
| [`build-client-guide-docx.py`](build-client-guide-docx.py) | Reads `client-guide-data.json` + a CE logo, builds the canonical `Client Guide.docx` (cover page, headers, footers, CE Blue H2s, Roboto body, Episode Overview + Pre-Interview Prep + Segment Breakdown + FAQ in canonical order) AND emits a paired `Client Guide.md` sibling at the same base path. Strips pandoc artifacts (`[text]{.underline}`, `{.smallcaps}`, `{.mark}`, `{.color=...}`) from input data. Never emits an Internal Setup section. Dependencies: `python-docx`. | SOP > Push to Drive > Build CE-branded DOCX |

## Conventions

- **Self-contained.** Each script runs on its own; no shared imports between scripts. If common helpers are needed, fold them in.
- **Dependencies in docstring.** Top-of-file docstring lists every required + optional Python package. Cowork runtime has `python-docx` available.
- **Filename convention sourced externally.** The canonical filename (`Client Guide.docx` / `Client Guide.md`) is owned by the [Podcast Drive](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU) doc. If the doc changes the convention, update the script to match.
- **Brand spec sourced externally.** Cover page layout, colors (CE Blue #3573FF, dark #0F172A, gray #5B6676), and Roboto body font come from the canonical [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) folder. If the brand changes, update the constants at the top of `build-client-guide-docx.py`.
- **Fail gracefully.** If a script can't produce its output (missing dependency, malformed input), it should log the failure and exit non-zero. The calling skill ships the run without that artifact and notes the gap in the metadata.

## Hard rules baked into the build script

The script enforces these every run:

- **Never emit an Internal Setup section.** The legacy "Complete and delete this section before sharing" checklist that lived in older runs is removed by design - the new pipeline configures the deliverable correctly from the jump.
- **Strip pandoc artifacts.** Input data sometimes carries `[text]{.underline}`, `{.smallcaps}`, `{.mark}`, `{.color=...}` from upstream pandoc DOCX-to-markdown conversion. The script renders these as proper inline runs in the DOCX (underline, color, etc.) and strips the wrapper but keeps inner text in the MD output. Markdown can't represent pandoc bracketed spans natively, so MD output gets just the plain inner text.
- **Canonical section order.** Episode Overview -> Pre-Interview Prep -> Segment Breakdown -> FAQ. With Metadata + Episode Plan as sub-blocks of Episode Overview.

## Invocation pattern

The cowork runtime invokes the script by:
1. Resolving the script path: `scripts/build-client-guide-docx.py`
2. Passing the path to the assembled `client-guide-data.json` and the canonical CE logo
3. Passing `--firm`, `--attorney`, `--practice-area`, `--scope`, `--output`, plus `--location` (when scope is Location/Extension) and optionally `--run-date`
4. Capturing stdout/stderr for the metadata audit log

The script's `--help` (via `argparse`) is the canonical CLI reference. Skill prose in `SKILL.md` should not duplicate CLI signatures - just reference the script + describe what it does conceptually.

## Versioning

Scripts are versioned with the skill. If a script changes its CLI, update the skill prose that invokes it. If a script changes its output shape, bump the corresponding schema in `../schemas/`.
