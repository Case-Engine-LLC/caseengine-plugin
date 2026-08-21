# References - pod-3B-client-ros

Reference assets the skill loads at runtime. Three subfolders + one log file:

| Path | What's in it |
|---|---|
| [`schemas/`](schemas/) | Machine-readable JSON schema declaring the shape of the Client ROS deliverable. The build script reads input data validated against this schema. |
| [`examples/`](examples/) | Calibration anchors (paired `.md` for structure + `.docx` for visual). Read before generating to set the quality bar. |
| [`iteration-log.json`](iteration-log.json) | Append-only run-issue log. Future sessions read this as institutional memory. |

Bundled executables live one level up at [`../scripts/`](../scripts/) (canonical CE skill layout - scripts are executable, references are read-only data).

## How the skill consumes these

- **Schemas** - referenced from `SKILL.md` > Best Practices > Outputs. Producer side: skill writes a Client ROS matching `schemas/client-ros.json`. Consumer side: downstream skills (pod-3C-client-guide, pod-4D-post-production-pack) read against the same shape.
- **Scripts** (`../scripts/build-client-ros-docx.py`) - invoked from `SKILL.md` > SOP > Push to Drive. Runtime executes the script against the run's data.
- **Examples** - read at the start of `SKILL.md` > SOP. Skill picks the matching scope or firm shape as quality calibration.
- **Iteration log** - read on every run as a check against known issues. Append on every surfaced learning.

## Versioning

Files here are versioned with the skill. Bump the skill version when any reference changes.
