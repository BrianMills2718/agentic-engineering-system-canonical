#!/bin/bash
# The whole AES game benchmark, one step at a time: 6 builds alternating ON/OFF, then blind copies and grading.
# Each step refuses to redo finished work, so rerunning after a stop continues where it left off.
# Usage: run_all.sh   (log: $BENCH/run_all.log). Plan: docs/planning/next.goal.md, "Game benchmark plan".
BENCH=${BENCH:-/home/brian/projects/data/aes-gamebench}; here=$(cd "$(dirname "$0")" && pwd)
exec >> "$BENCH/run_all.log" 2>&1; echo "== run_all $(date -Is)"
[[ -d $BENCH/games/abyssal_chain ]] || python3 "$here/fetch_game.py" big abyssal_chain "$BENCH/games" || exit 1
for n in 1 2 3; do for arm in on off; do
  d=$BENCH/runs/$arm-$n
  [[ -d $d/repo ]] || "$here/setup_arm.sh" $arm $n || { echo "STOP setup $arm-$n"; exit 1; }
  [[ -e $d/meta-build.json ]] || "$here/run_build.sh" $arm $n || { echo "STOP build $arm-$n"; exit 1; }
done; done
for n in 1 2 3; do for arm in on off; do
  grep -qP "\t$arm\t$n$" "$BENCH/blind-map.tsv" 2>/dev/null || "$here/blind_copy.sh" $arm $n || exit 1
done; done
cut -f1 "$BENCH/blind-map.tsv" | while read -r id; do
  [[ -e $BENCH/grade/$id/score.json ]] || "$here/grade.sh" "$id" || echo "STOP grade $id"
done
echo "== done $(date -Is)"
