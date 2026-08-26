#!/usr/bin/env python3
"""Pick outro variation slots that have not fired recently for this client.

The outro's three lines are generated per episode (references/outro-banks.json).
Left alone, a generator gravitates to the same credit approach and the same
sign-off every run, which is the sameness the banks exist to prevent. This reads
the client's prior episode metadata and reports what is off limits.

    python3 outro-rotation.py <client_episodes_dir> [--topical-available]

Prints the approaches and bank indices still in play, and a recommendation.
Exit 0 always - this informs generation, it does not gate it.
"""
import json, sys, pathlib, argparse

BANKS = pathlib.Path(__file__).resolve().parents[1] / "references" / "outro-banks.json"
LOOKBACK = 2  # no approach or sign-off may repeat within this many episodes


def load_history(root):
    """Return prior episodes' outro choices, newest first."""
    out = []
    for m in sorted(pathlib.Path(root).rglob("metadata.json"), reverse=True):
        try:
            d = json.loads(m.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if any(k.startswith("outro_line") for k in d):
            out.append({
                "episode": d.get("episode_number", "?"),
                "approach": d.get("outro_line1_approach"),
                "signoff": d.get("outro_line2_index"),
                "slots": d.get("outro_line3_slots") or {},
                "path": str(m),
            })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes_dir")
    ap.add_argument("--topical-available", action="store_true",
                    help="set when this episode's topic phrase is concrete enough for a topical credit")
    a = ap.parse_args()

    banks = json.loads(BANKS.read_text())
    approaches = list(banks["line_1_thanks"]["credit_approaches"])
    signoffs = list(range(len(banks["line_2_signoff"]["bank"])))

    hist = load_history(a.episodes_dir)
    recent = hist[:LOOKBACK]

    used_appr = {h["approach"] for h in recent if h["approach"]}
    used_sign = {h["signoff"] for h in recent if h["signoff"] is not None}
    free_appr = [x for x in approaches if x not in used_appr]
    free_sign = [i for i in signoffs if i not in used_sign]

    print(f"history: {len(hist)} prior episode(s) with outro data, checking last {LOOKBACK}")
    for h in recent:
        print(f"  E{h['episode']}: approach={h['approach']} signoff={h['signoff']}")
    print()
    print(f"line 1 approach  - blocked {sorted(used_appr) or 'none'} | available {free_appr}")
    print(f"line 2 sign-off  - blocked {sorted(used_sign) or 'none'} | available {free_sign}")

    if recent:
        prev = recent[0]["slots"]
        print(f"line 3 slots     - must differ from E{recent[0]['episode']} "
              f"in >=2 of 4: {prev or 'no slot data recorded'}")
    else:
        print("line 3 slots     - no prior episode, any combination is fine")

    print()
    if a.topical_available and "topical" in free_appr:
        pick = "topical"
        why = "topical is preferred whenever the topic phrase is concrete - it is the only approach whose clause cannot be reused on another episode"
    elif free_appr:
        pick = free_appr[0]
        why = "topical unavailable or blocked; first free approach in bank order"
    else:
        pick = approaches[0]
        why = f"every approach used within {LOOKBACK} episodes; oldest recycles first"
    print(f"RECOMMEND line 1 approach: {pick}")
    print(f"  reason: {why}")
    print(f"RECOMMEND line 2 sign-off index: {free_sign[0] if free_sign else 0}")
    print()
    print("Record outro_line1_approach, outro_line1_stem_index, outro_line2_index "
          "and outro_line3_slots in this episode's metadata.json.")


if __name__ == "__main__":
    main()
