# Archived 2026-08-17

`reference-impl/` - the working prototype from the 2026-08-14 build (`topics.py`, `topics2.py`,
`topics3.py`, `push_v3.py`, `push_tabs.py`). It produced the six-tab prototype doc the format was
originally signed off against.

Archived because the format changed materially on 2026-08-17 (Internal Notes cut, outro moved into
S1, statics down to five, taxonomy swapped to `{{TOPIC}}` / `{{LOCATION}}`), so this code now builds
a document shape that no longer exists. Kept for reference on the Docs API block-building approach,
which is still the clearest worked example of styling a Doc via batchUpdate.

The ship path is and remains the branded DOCX via `scripts/build-ros-template-v2-docx.py`.
