# Client ROS v2 - Examples

Single examples doc per CE convention: `## GOOD`, `## BAD`, `## EDGE CASE` sections, appended over time. Read 1-2 scope-matched entries as calibration before populating.

## GOOD

**Read-through repair - E3 Eberst prompt (2026-08-18).** The template shipped: *"Two crashes that look the same can be worth completely different money. Break down what actually moves that number. And if you have two that went different ways, take us through both."* Three failures: colloquial money-talk below the professional register, a fuzzy antecedent ("two that went different ways" - two what?), and a permission-softened ask ("if you have") where the format wants a directive. Repaired to: *"Two crashes that look identical can produce widely different settlement amounts. Walk us through what actually drives that difference. Then take us through two cases from your own practice that ended in very different places, so people understand why."* Same substance, same length, professional register, directive ask. Origin: template - flagged apply upstream. Gabe supplied the register correction ("widely different settlement amounts... this is a professional podcast").

## BAD

**Leftover-token ship (synthetic, from the negative test).** A payload whose prompt still carried `{{ATTORNEY}}` after populate. The renderer hard-fails and lists every leftover with its path - that is the gate working. The failure to never repeat is bypassing the renderer to "just fix the docx by hand": the token would reach the recording as literal markup read aloud.

## EDGE CASE

**Recording date TBD.** The date is non-blocking by design: the payload carries `"recording_date": "TBD"`, the cover simply omits its date line, and a refresh run after scheduling adds it via `files.update` on the same fileId. Do not hold the populate hostage to scheduling.
