#!/bin/bash
# Run one builder for the AES game benchmark: Claude Code, Sonnet, 3 hours wall clock including any planning.
# Usage: run_build.sh <on|off> <run number>. Needs setup_arm.sh first. Full trace: $dir/build.jsonl.
# OFF loads only user-level settings (--setting-sources user); ON also loads the repository's own (AES) settings.
arm=$1; n=$2; BENCH=${BENCH:-/home/brian/projects/data/aes-gamebench}; MODEL=${BUILD_MODEL:-claude-sonnet-5-5}
dir=$BENCH/runs/$arm-$n; repo=$dir/repo; here=$(cd "$(dirname "$0")" && pwd)
[[ -d $repo ]] || { echo "no repo at $repo; run setup_arm.sh"; exit 1; }
[[ -e $dir/build.jsonl ]] && { echo "$dir already built; refusing to rerun"; exit 1; }
/home/brian/.local/bin/storage-policy --need-gib 2 gate || exit 75
extra=(); [[ $arm == off ]] && extra=(--setting-sources user)
start=$(date +%s)
(cd "$repo" && timeout 10800 claude -p "$(cat "$here/builder-prompt.txt")" --model "$MODEL" \
  --permission-mode bypassPermissions --output-format stream-json --verbose "${extra[@]}" \
  > "$dir/build.jsonl" 2> "$dir/build.err")
rc=$?; end=$(date +%s)
python3 - "$dir/meta-build.json" "$arm" "$n" "$MODEL" "$start" "$end" "$rc" "$(git -C "$repo" rev-parse HEAD)" "$dir/build.jsonl" <<'PY'
import json, sys
out, arm, n, model, start, end, rc, head, trace = sys.argv[1:]
cost = None
for line in open(trace, errors="replace"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("type") == "result":
        cost = d.get("total_cost_usd")
json.dump({"arm": arm, "run": int(n), "model": model, "seconds": int(end) - int(start), "exit": int(rc),
           "capped": int(rc) == 124, "end_commit": head, "cost_usd_notional": cost}, open(out, "w"), indent=1)
PY
echo "RESULT build arm=$arm run=$n exit=$rc seconds=$((end-start))"
