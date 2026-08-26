# Schema - pod-3B-client-ros-v2

`client-ros-v2.json` - the canonical schema `client-ros-v2-data.json` validates against.

Shape: the template payload (3A-v2 `references/schema/ros-template-v2.json`) with every token resolved, PLUS the `firm` block (the 11 resolved values + recording_date + episode_number), MINUS `appendix_question_bank` (stripped - internal to the template) and `placeholders_used` (meaningless once resolved). Per-question `geo_tag` and `source_ngram_ref` are REQUIRED to survive populate - downstream audits read them from this payload.

If the schema file is absent at run time, log `schema_status: missing` in metadata.json and proceed - never block on a missing schema.
