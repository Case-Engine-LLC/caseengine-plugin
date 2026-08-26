# Update Mode

> **Exec:** deterministic (+ HUMAN gate on every merge conflict)
> **Assets:** `references/schema/ros-template-v2.json`, `references/document-structure.md`, `references/statics.json`

## What

Modify an existing v2 template in place, preserving every manual edit a producer made since the last run and flagging any conflict rather than resolving it silently. Update mode generates a full new state exactly the way `## Create` does, then **diffs it against what is already on disk** and merges. It never writes the new state straight over the old one.

Good output is a template that carries every manual edit it carried before the run, plus whatever genuinely new content the refreshed sources produced, with every disagreement between the two rendered on the page as a `> NEEDS VERIFICATION:` block rather than silently resolved in either direction.

**A manually edited outro line or Short-Form question is PRESERVED.** Those two are the highest-risk fields in the format: the outro's three spoken lines are generated fresh on every run against the beats and banks, so a regenerated outro will always differ from the one on disk, and a producer who rewrote a question at ROS review will always see the regenerated bank row disagree with it. In both cases the version on disk wins and the newly generated one is surfaced as a conflict, never applied.

The single-prompt gate and the ten-question gate still run after a merge. A merge can break both: dropping a preserved credential paragraph back in next to a regenerated prompt can leave two bolded prompts in the Introduction, and preserving edited questions alongside newly added ones can leave a location at nine or eleven. `steps/08-qa.md` runs in full after this step, not a subset of it.

## Inputs

- `run_context` - from `steps/01-prerequisites.md`, with `mode: "update"` (the existence check found a prior `ROS Template v2` + `ros-template-v2-data.json` in the resolved scope folder).
- `working_set` - from `steps/02-prepare-inputs.md`, loaded exactly as on a create run.
- The prior `ros-template-v2-data.json`, `.md` and `metadata.json` from the resolved destination folder. Never the legacy `ROS Template` sibling - that belongs to `pod-3A-ros-template` and is not a prior version of anything here.
- The proposed new state - the outputs of steps 03 through 06, run in full.

## Procedure

1. **Load the prior state** [deterministic] - read the prior payload, markdown and metadata. Recover the last run's upstream sources, attribute source and pull date, location list, question counts, and the rotation record (`line2_pattern`, `line3_frame`, `line4_frame`, the four outro fields). The rotation record is what stops an update from regenerating the same credit approach the prior version already used.

2. **Generate the proposed new state** [as `## Create`] - run steps 03 through 06 in full against the refreshed sources. Do not shortcut to "only the changed section": the sections constrain each other, so a partial regeneration produces a Short-Form set built against an attribute block that no longer exists.

3. **Diff block by block** [deterministic] - compare prior against proposed at the field level, not the file level:
   - `segment_1`: `topic_phrase`, `setup`, `credential`, `prompt`, and each attribute bullet.
   - `outro`: `thanks`, `signoff`, `reach`.
   - `segment_2`: per location, questions added / removed / rephrased, bullets changed, `geo_tag` changed.
   - `appendix_question_bank`: rows added or removed against the n-gram table.
   - Provenance: whether `attribute_source` moved from `static-fallback` to a live `pod-1D` pull, and whether the Topic Plan Doc revision changed since the last run.

4. **Classify every difference** [deterministic] - three buckets, and the bucket decides the action:
   - **Manual edit** - the value on disk differs from what the PRIOR run generated (compare against the prior payload, which is the record of what this skill last wrote). Someone changed it by hand. **Preserve it.**
   - **New content** - a field the prior payload did not carry, or a bank row the prior run did not have. **Merge it in.**
   - **Retired content** - a field the new source set no longer produces. **Drop it**, and name it in the report so a producer sees what left.

5. **Preserve manual edits** [deterministic] - a manually edited value keeps its current wording. Never auto-overwrite one silently, and never "improve" it in passing. Explicitly:
   - **A manually edited outro line is preserved.** All three lines regenerate on every run by design, so a diff on the outro is expected and is not evidence of a change worth applying. If line 1's credit approach was hand-picked, the prior `outro_line1_approach` in metadata carries forward with it.
   - **A manually edited Short-Form question is preserved,** along with its bullets, its `geo_tag` and its `topic_plan_ref`. A question a producer rewrote at ROS review is the version the client agreed to.
   - **The prompt and the credential are the highest-risk fields in S1** and are edited by hand more than anything else in the format. Treat any difference in either as a manual edit unless the prior payload proves otherwise.
   - **A STATIC string is never a manual edit.** If `welcome`, `welcome_first` or `outro_note` differs from `references/statics.json`, that is drift from a prior run, not an edit to protect. Restore the constant and name it in the report.

6. **Flag conflicts inline** [HUMAN gate] - where a newly generated value disagrees with a preserved manual edit, emit at that location in the markdown:

   ```
   > NEEDS VERIFICATION: auto-generated value [X] conflicts with manual edit [Y]
   ```

   Do not auto-resolve in either direction, and do not resolve a conflict by picking the longer, newer or better-reading version. The producer decides. A run that resolves a conflict silently has overwritten somebody's work whichever way it went.

   The Topic Plan is the one exception, and it goes the other way: where the live Doc has vetoed or reworded a question, the **Doc wins over a local manual edit**, because the Doc is what the client sees and edits. Apply the Doc's version and name the override in the report rather than flagging it as a conflict.

7. **Re-render** [deterministic] - rebuild the `.md`, `ros-template-v2-data.json` and `metadata.json` from the merged state. Bump the run date, append this run to the provenance history, and carry the rotation record forward so the next episode still rotates correctly.

8. **Re-run QA in full** [routes to `steps/08-qa.md`] - every tier, not the diff. A merge can break a gate that both inputs passed separately.

## Outputs

```
update: {
  prior_payload: path, prior_doc_id: str,
  diff: {
    segment_1: [{field, prior, proposed, classification}],
    outro:     [{line, prior, proposed, classification}],
    segment_2: [{location, question_index, change, classification}],
    appendix:  {rows_added: int, rows_removed: int}
  },
  preserved:  [str],          manual edits kept, by field path
  merged:     [str],          new content applied
  dropped:    [str],          retired content removed, named in the report
  conflicts:  [{location, auto_generated, manual_edit}],
  doc_overrides: [str]        where the live Topic Plan Doc beat a local edit
}

artifacts: same shape as steps/07-render.md, written from the merged state
```

## Validation

- Every difference is classified as manual edit, new content or retired content. An unclassified difference is a silent overwrite waiting to happen.
- Zero manual edits overwritten without a `> NEEDS VERIFICATION:` block at their location.
- Every manually edited outro line and Short-Form question present in the prior artifact is present in the merged one.
- The three STATIC strings render byte-identical to `references/statics.json`. A prior-run drift is restored, not preserved.
- **The single-prompt gate passes after the merge** - exactly ONE bolded prompt paragraph in the Introduction. A merge that leaves two FAILS.
- **The ten-question gate passes after the merge** - exactly ten questions per location, every location the same count. A merge that leaves nine or eleven FAILS.
- `steps/08-qa.md` returns clean on the merged state, every tier.
- The Google Doc was updated via `files.update` against the existing fileId. A new Doc means every downstream link just died.

## Failure modes

| Failure | Exit behavior | Routes to |
|---|---|---|
| No prior v2 payload in the folder, only a legacy `ROS Template` | Not an update. A legacy sibling is not a prior version | `## Create` via `steps/01-prerequisites.md` |
| Prior `ros-template-v2-data.json` is missing or unparseable | Stop. Without it there is no record of what this skill last generated, so no difference can be classified and every manual edit is at risk | user |
| A difference cannot be classified | Treat it as a manual edit and flag it. Preserving something that did not need preserving costs a review; overwriting something that did costs the work | `steps/08-qa.md` |
| Auto-generated value conflicts with a manual edit | Emit `> NEEDS VERIFICATION:` inline, preserve the manual edit, never auto-resolve | user |
| The live Topic Plan Doc vetoed or reworded a question that was manually edited locally | The Doc wins. Apply the Doc's version and name the override in the report | `steps/05-segment-2.md` |
| Single-prompt or ten-question gate fails after the merge | Repair the merged state and re-run the FULL QA set, never just the failed gate | `steps/08-qa.md` |
| A STATIC string on disk differs from `references/statics.json` | Restore the constant and report it. That is drift from a prior run, not an edit to protect | `steps/07-render.md` |
| `archive-and-rebuild` was requested instead | Move ONLY the prior v2 file to `_archive-{YYYY-MM-DD}/` and take the create path. Never touch a legacy sibling or a Client ROS | `## Create` |
