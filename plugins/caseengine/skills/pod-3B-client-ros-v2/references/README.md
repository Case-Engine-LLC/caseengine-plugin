# References - pod-3B-client-ros-v2

Layout per the CE skill convention.

- `placeholders.md` - the populate-side mirror of the v2 token taxonomy. The CANONICAL copy is `pod-3A-ros-template-v2/references/placeholders.md`; on any disagreement it wins and this mirror is the bug to fix.
- `schema/client-ros-v2.json` - the canonical schema `client-ros-v2-data.json` validates against. Inherits the template payload shape (3A-v2 `ros-template-v2.json`), adds the `firm` block, drops `appendix_question_bank` and `placeholders_used`.
- `examples/client-ros-v2-examples.md` - single GOOD / BAD / EDGE CASE doc per CE convention.
- `iteration-log.json` - append-only institutional memory. Read at every run start; written manually post-run.
