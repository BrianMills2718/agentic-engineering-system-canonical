#!/bin/bash
# The whole AES game benchmark, one step at a time: 6 builds alternating ON/OFF, then blind copies and grading.
# Reruns skip completed steps. An interrupted attempt may need inspection before the runner resumes.
# Usage: run_all.sh   (log: $BENCH/run_all.log). Plan: docs/planning/next.goal.md, "Game benchmark plan".
BENCH=${BENCH:-/home/brian/projects/data/aes-gamebench}; here=$(cd "$(dirname "$0")" && pwd)
exec 9>"$BENCH/.run.lock" || exit 1
flock -n 9 || { echo "Benchmark already running"; exit 2; }
exec >> "$BENCH/run_all.log" 2>&1 || exit 1
echo "== run_all $(date -Is)"
# Refuse before the first build if the benchmark cannot be scored or its inputs cannot be pinned.
export BUILD_MODEL=${BUILD_MODEL:-claude-sonnet-5-5}
[[ -n ${GRADE_MODEL:-} && -x ${PLAYWRIGHT_CHROMIUM_EXECUTABLE:-} ]] || {
  echo "Set GRADE_MODEL and PLAYWRIGHT_CHROMIUM_EXECUTABLE to the selected grader and browser"; exit 2;
}
[[ ${AES_REVISION:-} =~ ^[0-9a-f]{40}$ && ${AES_TEMPLATE:-} == /* ]] || {
  echo "Set AES_REVISION and an absolute AES_TEMPLATE snapshot path"; exit 2;
}
[[ $(git -C "$AES_TEMPLATE" rev-parse refs/heads/main) == "$AES_REVISION" ]] || exit 2
/home/brian/.local/bin/storage-policy --need-gib 2 gate || exit 75
"$here/grade.sh" --check-browser || exit 1
[[ -d $BENCH/games/abyssal_chain ]] || python3 "$here/fetch_game.py" big abyssal_chain "$BENCH/games" || exit 1
if [[ ! -s $BENCH/frozen-phaser.min.js && ! -e $BENCH/run-spec.json ]]; then
  phaser_tmp=$(mktemp "$BENCH/.phaser.XXXXXXXX") || exit 1
  curl -fsSL --max-time 120 -o "$phaser_tmp" https://cdnjs.cloudflare.com/ajax/libs/phaser/3.90.0/phaser.min.js || exit 1
  [[ -s $phaser_tmp ]] && mv "$phaser_tmp" "$BENCH/frozen-phaser.min.js" || exit 1
fi
[[ -s $BENCH/frozen-phaser.min.js ]] || { echo "Frozen Phaser file is missing"; exit 2; }
work=$(mktemp -d "$BENCH/.preflight.XXXXXXXX") || exit 1
python3 "$here/items.py" "$BENCH/games/abyssal_chain" "$work/frozen-items.json" || exit 1
python3 - "$here" "$BENCH" "$work" <<'FREEZE' || exit 2
import hashlib, json, os, subprocess, sys
from pathlib import Path
here, bench, work = map(Path, sys.argv[1:])
def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()
settings = {
    k: os.environ.get(k, "") for k in
    ("AES_REVISION", "AES_TEMPLATE", "BUILD_MODEL", "GRADE_MODEL", "PLAYWRIGHT_CHROMIUM_EXECUTABLE", "PLAYWRIGHT_NODE_PATH")
}
game = bench / "games" / "abyssal_chain"
data = {str(p.relative_to(game)): digest(p) for p in sorted(game.rglob("*")) if p.is_file()}
manifest = {
    "settings": settings,
    "phaser_sha256": digest(bench / "frozen-phaser.min.js"),
    "browser_sha256": digest(Path(settings["PLAYWRIGHT_CHROMIUM_EXECUTABLE"])),
    "items_sha256": digest(work / "frozen-items.json"),
    "harness": {p.name: digest(p) for p in sorted(here.iterdir()) if p.is_file()},
    "game_files": data,
    "claude_version": subprocess.check_output(["claude", "--version"], text=True).strip(),
    "codex_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
}
receipt = bench / "run-spec.json"
items = bench / "frozen-items.json"
if receipt.exists():
    if json.loads(receipt.read_text()) != manifest or digest(items) != manifest["items_sha256"]:
        raise SystemExit("Frozen benchmark inputs changed; inspect run-spec.json before resuming")
else:
    if (bench / "runs").exists() or (bench / "grade").exists() or items.exists():
        raise SystemExit("Existing benchmark artifacts have no frozen manifest; preserve and inspect them")
    (work / "frozen-items.json").replace(items)
    (work / "run-spec.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (work / "run-spec.json").replace(receipt)
FREEZE
if [[ ${1:-} == --preflight ]]; then
  echo "RESULT preflight=ready"
  exit 0
fi
for n in 1 2 3; do for arm in on off; do
  d=$BENCH/runs/$arm-$n
  if [[ ! -f $d/meta-setup.json ]]; then
    "$here/setup_arm.sh" "$arm" "$n" || { rc=$?; echo "STOP setup $arm-$n (exit $rc)"; exit "$rc"; }
  fi
  [[ -e $d/meta-build.json ]] || "$here/run_build.sh" "$arm" "$n" || { rc=$?; echo "STOP build $arm-$n (exit $rc)"; exit "$rc"; }
done; done
for n in 1 2 3; do for arm in on off; do
  grep -qP "\t$arm\t$n$" "$BENCH/blind-map.tsv" 2>/dev/null || "$here/blind_copy.sh" $arm $n || exit 1
done; done
while IFS=$'\t' read -r id arm n; do
  [[ -e $BENCH/grade/$id/score.json ]] || "$here/grade.sh" "$id" || {
    rc=$?; echo "STOP grade $id (exit $rc)"; exit "$rc";
  }
done < "$BENCH/blind-map.tsv"
echo "== done $(date -Is)"
