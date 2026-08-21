#!/usr/bin/env python3
"""Validate the pod-2A-topic-planner scoring model.

Loads references/scoring-model.json and:
  1. Validates it against references/schema/scoring-model.schema.json (jsonschema).
  2. Asserts every signals[].bucket is a real key in the buckets object.
  3. Asserts the sum of all signals[].weight equals 1.00 (tolerance 0.001) -
     a cross-field invariant JSON Schema cannot express.

Prints PASS / FAIL clearly and exits 0 on pass, 1 on fail.
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("FAIL - jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)

# scripts/ -> skill root -> references/
SKILL_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = SKILL_ROOT / "references" / "scoring-model.json"
SCHEMA_PATH = SKILL_ROOT / "references" / "schema" / "scoring-model.schema.json"
WEIGHT_TARGET = 1.0
WEIGHT_TOLERANCE = 0.001


def fail(msg):
    print(f"FAIL - {msg}")
    sys.exit(1)


def main():
    if not MODEL_PATH.exists():
        fail(f"scoring model not found: {MODEL_PATH}")
    if not SCHEMA_PATH.exists():
        fail(f"schema not found: {SCHEMA_PATH}")

    try:
        model = json.loads(MODEL_PATH.read_text())
    except json.JSONDecodeError as e:
        fail(f"scoring-model.json is not valid JSON: {e}")
    try:
        schema = json.loads(SCHEMA_PATH.read_text())
    except json.JSONDecodeError as e:
        fail(f"scoring-model.schema.json is not valid JSON: {e}")

    # 1. Schema validation
    try:
        jsonschema.validate(instance=model, schema=schema)
    except jsonschema.ValidationError as e:
        loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
        fail(f"schema validation error at {loc}: {e.message}")
    except jsonschema.SchemaError as e:
        fail(f"schema itself is invalid: {e.message}")
    print("  schema validation .......... ok")

    # 2. Cross-field: every signal bucket exists
    bucket_keys = set(model.get("buckets", {}).keys())
    signals = model.get("signals", [])
    bad_buckets = [
        (s.get("name", "<unnamed>"), s.get("bucket"))
        for s in signals
        if s.get("bucket") not in bucket_keys
    ]
    if bad_buckets:
        detail = ", ".join(f"{n} -> '{b}'" for n, b in bad_buckets)
        fail(f"signal(s) reference unknown bucket(s): {detail}. "
             f"Known buckets: {sorted(bucket_keys)}")
    print(f"  bucket references .......... ok ({len(signals)} signals)")

    # 3. Cross-field: signal weights sum to 1.00
    weight_sum = sum(float(s.get("weight", 0)) for s in signals)
    if abs(weight_sum - WEIGHT_TARGET) > WEIGHT_TOLERANCE:
        fail(f"signal weights sum to {weight_sum:.4f}, "
             f"expected {WEIGHT_TARGET:.2f} +/- {WEIGHT_TOLERANCE}")
    print(f"  signal weight sum .......... ok ({weight_sum:.4f})")

    print("PASS - scoring-model.json is valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
