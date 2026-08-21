#!/usr/bin/env bash
# rerender_batch.sh - re-render every already-uploaded n-gram Doc IN PLACE
# (files.update against the existing fileId - URL preserved). Applies the
# locked canonical format incl. the 4-block INTERNAL section. Runs in
# parallel waves of 5. Skips idx 12 (pilot, already re-rendered).
WORK="/tmp/ngram-backfill"
mkdir -p "$WORK/rerender-results"
WAVE=5
TOTAL=$(python3 -c "import json;print(len(json.load(open('$WORK/manifest.json'))))")
i=0
while [ "$i" -lt "$TOTAL" ]; do
  pids=()
  for ((k=0; k<WAVE && i<TOTAL; k++, i++)); do
    if [ "$i" -eq 12 ]; then continue; fi   # pilot already re-rendered
    if [ ! -f "$WORK/results/$i.json" ]; then
      echo "{\"idx\":$i,\"error\":\"no result file - skipped\"}" \
        > "$WORK/rerender-results/$i.json"
      continue
    fi
    ( bash "$WORK/rerender_one.sh" "$i" \
        > "$WORK/rerender-results/$i.json" 2>"$WORK/rerender-results/$i.err" ) &
    pids+=($!)
  done
  for p in "${pids[@]}"; do wait "$p"; done
  echo "wave done, next idx=$i / $TOTAL"
done
echo "RERENDER BATCH COMPLETE"
