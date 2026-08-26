# Reference implementation

The code that produces the live doc `1Bv-EWc7HBtKqc09XEfQnBIfSOdm6m4Tc-kJNw5uKErk`. It is the
source of truth for the v2 format, and it is actively edited - re-read it before relying on any
constant. Full description of each file lives in `../README.md`.

**Reference, not the ship path.** The ship path is `../build-ros-template-v2-docx.py`, which
renders the same shape into a branded DOCX with the CE cover page.

Two things that will trip you up:

- **`STATIC` moves.** It went from 15 keys to 16 during the 2026-08-14 lock. Generate the STATIC
  table in `SKILL.md` and the `const` values in `references/schema/ros-template-v2.json` from
  `topics3.py` rather than transcribing them by hand.
- **`push_v3.py` has a hardcoded `DOC` id** and its `__main__` deletes and rewrites every tab in
  place. Do not run it unmodified against anything you care about.

`topics3.py` and `push_v3.py` import `topics2` for its `TOPICS` list. Run with the folder on
`PYTHONPATH`.
