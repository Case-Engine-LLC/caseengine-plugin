# Scripts - ROS Template v2

| File | What it does |
|---|---|
| [`build-ros-template-v2-docx.py`](build-ros-template-v2-docx.py) | **The ship path.** Reads `ros-template-v2-data.json`, emits the CE-branded `.docx` and its paired `.md` in one pass. |
| [`reference-impl/`](reference-impl/) | The working implementation that produces the live doc. Reference, not the ship path. |

## build-ros-template-v2-docx.py

```
python3 build-ros-template-v2-docx.py \
    --data ros-template-v2-data.json \
    --logo /path/to/case-engine-logo.png \
    --output "E7: Truck Accidents // ROS Template v2 - GA - Savannah.docx"
```

Writes the `.docx` at `--output` and the `.md` alongside it. Dependencies: `python-docx`, and nothing else outside the standard library.

**This skill is freestanding.** It shares no module, helper, constant or asset with `pod-3A-ros-template` or any other skill, so the directory can be zipped and handed over on its own. No import, `sys.path` insert, symlink or file read may resolve above `SKILL_DIR`. If a helper is needed that lives in another skill, duplicate it into this `scripts/` and customize it for v2. Do not import it.

`--logo` defaults to `assets/case-engine-logo.png` inside this skill when that file is present, so a bundled copy needs no external path. Drop the CE logo there and the cover page renders branded with no arguments. Passing `--logo` explicitly still wins.

It renders the locked shape and refuses anything else:

- **Cover page** - spacer, logo at the second paragraph (180pt), spacer, `Run of Show` in CE Blue 24pt bold, episode title dark 18pt bold, `{practice area}  |  {scope}` dark 14pt, `Prepared by Case Engine`. All centered, Roboto, page break after. The `{{RECORDING_DATE}}` line was removed 2026-08-18 in both the docx and the markdown path; the token is retired from the taxonomy.
- **`S1: Long-Form (15-30m)`** - Introduction, the attribute bullets, then the `Outro` that ends it. S1 is a complete recording, intro through outro, which is why the outro closes S1 rather than following S2. The attribute bullets sit directly under the `ATTORNEY RESPONSE` speaker tag with no heading above them and no divider below: `Attributes to Hit` and the whole `Internal Notes (not read on air)` block were retired 2026-08-17 and are no longer emitted, so `segment_1.internal_notes` and `segment_1.attribute_sources` are read by nothing. See `references/attributes.md` for what the block is now and `references/document-structure.md` for the removed-section list.
- **`S2: Short-Form (60-90s)`** - one italic gray direction line, then `Location: {city}` per location, each with exactly ten questions. A question renders as a paragraph bold in full, the `Q{N}:` label inside the bold, with two to four `[Label]{.underline}: detail` bullets under it. The labels are underlined and never bold, so the question carries the only bold weight in the block. Nothing else renders under a question: no time budget, no geo tag line, no source ref. Spacing is deliberately tight - zero above and below on questions and bullets, 8pt/2pt on the location heading - because the block is scanned on the day rather than read.
- **`Appendix: Source Question Bank`**, on its own page.

**Heading colors:** H1 section headers CE Blue, H2 CE Dark, never a blue H2. Confirmed against `.archive-2026-08-17/reference-impl/push_tabs.py`, which built the live prototype doc and applies the same two colors.

**Page breaks:** cover, S1 and the appendix each begin a new page. S2 does NOT - it flows on from S1 behind a horizontal rule, changed 2026-08-18. The rule is a real bottom border on an empty paragraph, never a row of dash or underscore characters, and the same helper draws the divider above the internal notes. `pageBreakBefore` is set explicitly to False on the S2 heading and on both rules rather than left unset, because a paragraph otherwise inherits whatever sat at its index.

Seven hard refusals, so a malformed payload fails loudly rather than rendering a wrong document:

- `episode_format` is not `v2-open-interview` - exits rather than rendering a legacy template in the wrong shape.
- Any of the three STATIC constants missing from `data["static"]` - exits naming the missing keys.
- Any of the three generated outro lines missing from `data["outro"]` - exits naming them. The outro's spoken lines stopped being constants 2026-08-18; they are generated against `references/outro-banks.json`.
- An attribute block outside ten to twelve bullets - exits naming the count. Gate AT-2 in `references/attributes.md`: past twelve the attorney stops treating it as a shape and starts treating it as a list to get through.
- A question mark anywhere in the attribute block, in a bullet's name or its detail - exits naming the offending bullet. Gate AT-1, the one that matters most: a question mark means a catalog row reached the page uninverted, and the attorney reads it aloud.
- Any location with a question count other than exactly 10 - exits naming the location and the count.
- Any Short-Form question with fewer than 2 or more than 4 bullets, or with no question text - exits naming the location and the question number.

Every gate runs before any render work, so a malformed payload writes no partial file.

`{{PLACEHOLDER}}` tokens pass through verbatim in both outputs. Pandoc inline markers become real Word runs in the DOCX and are stripped in the `.md`; nested `**[Name]{.underline}**` renders as one run that is both bold and underlined.

The inline parser is a linear depth-counting scan using CommonMark flanking rules, so bold inside bold nests rather than closing the outer span early. That case was a live bug: a `{{PLACEHOLDER}}` wrapped in its own `**` inside an already bold Short-Form question closed the outer run and rendered the token unbold, failing the placeholder gate. The renderer also strips a question's own `**` markers at the emit site, so the fix holds from both directions.

Upload the `.docx` with `mimeType: application/vnd.google-apps.document` so Drive auto-converts it. Upload the `.md` as `text/markdown`, unconverted. Never re-upload the `.md` with `convert=true` - that leaks markup as visible text and has no cover page.

Verified 2026-08-14 against the live doc: every STATIC string and structural anchor rendered identically at the time. Re-verified 2026-08-18 against the three-string STATIC set and the generated outro block. Not yet run against a real generated template with a full appendix.

## reference-impl/

The implementation that produces the live doc `1Bv-EWc7HBtKqc09XEfQnBIfSOdm6m4Tc-kJNw5uKErk`. It is the source of truth for the format, and it moves - re-read it before relying on any constant.

| File | What it is |
|---|---|
| `topics3.py` | The content model. `STATIC` (frozen strings, 16 at the time of the 2026-08-14 lock), `ATTRIBUTES`, `ATTR_SOURCES` (per-attribute source consistency), `REGION`, `V3` (per-topic cold open, prompt, need-to-know, examples), `s2_v4()` (Short-Form generator). |
| `push_v3.py` | `blocks_for()` - the document shape. This is the structural reference for Editorial Guideline 4, including the cover page block order and the logo insert. |
| `push_tabs.py` | Block model to Docs API requests: inline run splitting, styling, page breaks, bullets, multi-tab creation, and the CE color constants. |
| `edit_section.py` | Targeted section edits against the live doc. |
| `topics.py`, `topics2.py` | Earlier content models. `topics2.TOPICS` still supplies per-topic titles, scope labels, city blocks, and n-gram paths. |

**`references/statics.json` is the source of truth for constants, not `topics3.py`.** The STATIC set is now THREE strings - `welcome`, `welcome_first`, `outro_note` - after eleven constants were retired 2026-08-17 and the outro's three spoken lines became generated on 2026-08-18. `topics3.py` is a 2026-08-14 snapshot from the lock, when `STATIC` briefly went from 15 keys to 16 mid-session; treat it as history. Generate the STATIC table in `SKILL.md` and the `const` values in the schema from `statics.json` rather than transcribing either.

**`push_v3.py` has a hardcoded `DOC` id** and its `__main__` deletes and rewrites every tab in place. Do not run it unmodified against anything you care about.

## What the skill generalizes

The reference implementation hardcodes six topics. The skill derives the same content from the n-gram table, entity map, and attribute set for any topic. `ATTRIBUTES` becomes `references/attributes/attributes-fallback.json` (the fallback once `pod-1D-attribute-research` ships), and the `REGION` map becomes a per-run input confirmed at the Greeting. The prototype ships to Google Docs tabs; the skill ships a branded DOCX carrying the CE cover page.
