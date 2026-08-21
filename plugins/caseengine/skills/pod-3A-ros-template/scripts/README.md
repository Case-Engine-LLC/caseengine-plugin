# Scripts - ROS Template

Bundled scripts the cowork runtime executes during the skill's SOP. Self-contained; dependencies declared in each script's docstring.

## Files

| Script | What it does | Invoked from |
|---|---|---|
| [`build-ros-template-docx.py`](build-ros-template-docx.py) | Reads `ros-template-data.json` + a CE logo, builds the canonical `ROS Template.docx` (cover page, headers/footers, CE Blue H2 segments, Roboto body, Producer Notes block, Introduction, Segments S1..N with per-question prompts and bolded question text + attorney-bullet scaffolding, Closing/CTA outro). Emits a paired `.md` at the same base path so both the raw markdown source and the Drive-converted Google Doc sibling ship side-by-side. Strips pandoc inline markup (`[text]{.underline}`, `{.smallcaps}`, `{.mark}`) and translates underline runs natively into the DOCX. **Preserves placeholder tokens verbatim** - this is the tokenized layer; `/client-ros` resolves tokens downstream. Dependencies: `python-docx`. | SOP > Push to Drive > Build CE-branded DOCX |

## Conventions

- **Self-contained.** Each script runs on its own; no shared imports between scripts.
- **Dependencies in docstring.** Top-of-file docstring lists every required Python package. Cowork runtime has `python-docx` available.
- **Filename convention sourced externally.** The output filename (`ROS Template.docx` / `ROS Template.md`) is fixed per the canonical [Podcast Drive](https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU) doc. If the doc changes the convention, update the script to match.
- **Brand spec sourced externally.** CE colors (#3573FF blue, #0F172A dark, #5B6676 gray) and Roboto font (per Gabe 2026-05-12; Branding folder still says Calibri) come from the canonical [Case Engine Branding](https://drive.google.com/drive/folders/1OulNcg6hZ6caFD0Xc-W50i7ougC_y0qo) folder. Don't inline brand tokens elsewhere; the script references this folder in its docstring.
- **Placeholder tokens are immutable.** The script must NEVER substitute, expand, or guess at the 12 approved `{{PLACEHOLDERS}}` (see SKILL.md > Best Practices > Placeholder taxonomy). Tokens pass through verbatim into both the `.docx` and the `.md` outputs. Token resolution happens in `/client-ros`, not here.
- **Pandoc artifact stripping.** Input data may contain `[text]{.underline}`, `{.smallcaps}`, `{.mark}`, `{.color=...}` patterns. The script translates underlines to native DOCX underline runs and strips the markup tokens entirely from the paired `.md` (so the `.md` reads as clean markdown).
- **No "Internal Setup" section.** The legacy "Complete and delete this section before sharing" checklist is excluded from the rendered output. The skill's SOP runs the equivalent state check at Step 0 - no in-document residue.
- **Fail gracefully.** If a script can't produce its output (missing dependency, malformed input), it should log the failure and exit non-zero. The calling skill ships the run without that artifact and notes the gap in the metadata.

## Invocation pattern

The cowork runtime invokes the script by:
1. Resolving the script path: `scripts/build-ros-template-docx.py`
2. Passing the data file (`--data`), logo (`--logo`), practice area, episode topic, scope, optional location, output DOCX path, and optional run date
3. Capturing stdout/stderr for the metadata audit log

Each script's `--help` (via `argparse`) is the canonical CLI reference. Skill prose in `SKILL.md` should not duplicate CLI signatures - just reference the script + describe what it does conceptually.

## Versioning

Scripts are versioned with the skill. If a script changes its CLI, update the skill prose that invokes it. If a script changes its output shape, bump the corresponding schema in `../schemas/`.
