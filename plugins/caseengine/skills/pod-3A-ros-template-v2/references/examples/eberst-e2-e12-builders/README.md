# Eberst E2-E12 ROS Template v2 builders

Ten episode builders plus the shared payload assembler, the per-episode ATTORNEY
RESPONSE blocks, and the 41-gate QA runner. Produced 2026-08-18. Every episode
shipped at 41/41.

    common.py       payload assembly + the contraction pass (generated text only)
    attributes.py   per-episode ATTORNEY RESPONSE blocks, E2-E12, all 132 unique
    qa.py           41 gates incl. AT-9 uniqueness and the US-English scan
    e02.py..e12.py  one per episode; each holds setup/credential/prompt/S2/bank
    out/            the built payloads, one JSON per episode
    upload.sh       create-or-update a Drive Doc by name (files.update, never create)

Rebuild one episode:
    /usr/bin/arch -arm64 python3 e05.py
    /usr/bin/arch -arm64 python3 ~/.claude/skills/pod-3A-ros-template-v2/scripts/build-ros-template-v2-docx.py \
        --data out/eberst-e5-data.json --output out/E5.docx
    /usr/bin/arch -arm64 python3 qa.py --data out/eberst-e5-data.json --md out/E5.md

`arch -arm64` is required. Plain python3 picks the x86_64 interpreter and jsonschema
fails to import, which silently skips the schema gate.
