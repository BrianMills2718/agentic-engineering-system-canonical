#!/bin/bash
# Make one build repository for the AES game benchmark (plan: docs/planning/next.goal.md, "Game benchmark plan").
# Usage: setup_arm.sh <on|off> <run number> [game]. Writes $BENCH/runs/<arm>-<n>/repo and meta-setup.json.
# Both arms get the same files: docs/game-design.md, assets/ (sprite library), vendor/phaser.min.js.
# ON: the repository is made from the AES template (copier), so its instructions, make check and hooks apply.
# OFF: a plain git repository with only those files.
arm=$1; n=$2; game=${3:-abyssal_chain}
BENCH=${BENCH:-/home/brian/projects/data/aes-gamebench}
[[ $arm == on || $arm == off ]] || { echo "arm must be on or off"; exit 2; }
/home/brian/.local/bin/storage-policy --need-gib 2 gate || exit 75
src=$BENCH/games/$game; dir=$BENCH/runs/$arm-$n; repo=$dir/repo
[[ -f $src/gdds/$game.md ]] || { echo "fetch the game first: fetch_game.py big $game $BENCH/games"; exit 1; }
[[ -s $BENCH/frozen-phaser.min.js ]] || { echo "Missing frozen Phaser; run run_all.sh --preflight"; exit 2; }
[[ -e $dir ]] && { echo "$dir exists; refusing to overwrite"; exit 1; }
if [[ $arm == on ]]; then
  # A local snapshot pins both Copier and the uv dependency, which resolves branch main.
  [[ ${AES_REVISION:-} =~ ^[0-9a-f]{40}$ && ${AES_TEMPLATE:-} == /* ]] || {
    echo "Set AES_REVISION to a full commit and AES_TEMPLATE to an absolute local git snapshot path"; exit 2;
  }
  snapshot_rev=$(git -C "$AES_TEMPLATE" rev-parse refs/heads/main) || exit 1
  [[ $snapshot_rev == "$AES_REVISION" ]] || { echo "Snapshot main does not match AES_REVISION"; exit 2; }
fi
mkdir -p "$dir" || exit 1
if [[ $arm == on ]]; then
  uvx copier copy --trust --defaults --vcs-ref "$AES_REVISION" \
    -d project_name="$game" -d package_name="${game//-/_}" -d description="A 2D browser game built from its design document" \
    -d goal_actor="Brian, testing whether AES delivers every requirement of a long game design document" \
    -d goal_job="build the game the design document describes" -d goal_result="every requirement works in the browser" \
    -d ship_planning_gate=true -d ship_one_page_plans=true -d git_user_name=BrianMills2718 -d git_user_email=69022071+BrianMills2718@users.noreply.github.com \
    -d lockstep_git="file://$AES_TEMPLATE" "$AES_TEMPLATE" "$repo" > "$dir/copier.log" 2>&1 || { echo "copier failed: $dir/copier.log"; exit 1; }
  # Match the resolved commit in uv.lock, not just Copier's answer.
  python3 - "$repo/uv.lock" "$AES_REVISION" <<'PIN' || exit 1
import sys, tomllib
from pathlib import Path
lock = tomllib.loads(Path(sys.argv[1]).read_text())
sources = [p["source"].get("git", "") for p in lock["package"] if p["name"] == "agentic-engineering-system"]
if len(sources) != 1 or not sources[0].endswith("#" + sys.argv[2]):
    raise SystemExit("Locked AES dependency does not match the selected revision")
PIN
else
  mkdir -p "$repo" && git -C "$repo" init -q && git -C "$repo" config core.hooksPath .git/no-hooks || exit 1
fi
mkdir -p "$repo/docs" "$repo/assets" "$repo/vendor" || exit 1
cp "$src/gdds/$game.md" "$repo/docs/game-design.md" && cp "$src"/library/* "$repo/assets/" || exit 1
cp "$BENCH/frozen-phaser.min.js" "$repo/vendor/phaser.min.js" || exit 1
git -C "$repo" add -A && git -C "$repo" -c user.name=BrianMills2718 -c user.email=69022071+BrianMills2718@users.noreply.github.com \
  commit -q --no-verify -m "Benchmark start: design document, sprite library, Phaser 3.90.0" || exit 1
python3 - "$dir/meta-setup.json" "$arm" "$n" "$game" "$(git -C "$repo" rev-parse HEAD)" \
  "$(sha256sum "$repo/vendor/phaser.min.js" | cut -c1-64)" "$(grep -m1 '_commit' "$repo/.copier-answers.yml" 2>/dev/null)" <<'PY'
import json, sys, time
out, arm, n, game, head, phaser, tpl = sys.argv[1:]
json.dump({"arm": arm, "run": int(n), "game": game, "start_commit": head, "phaser_sha256": phaser,
           "template": tpl, "made": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, open(out, "w"), indent=1)
PY
[[ $? -eq 0 ]] || exit 1
echo "RESULT setup arm=$arm run=$n repo=$repo"
