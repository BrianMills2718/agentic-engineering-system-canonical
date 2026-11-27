#!/bin/bash
# Make one build repository for the AES game benchmark (plan: docs/planning/game-benchmark.md).
# Usage: setup_arm.sh <on|off> <run number> [game]. Writes $BENCH/runs/<arm>-<n>/repo and meta-setup.json.
# Both arms get the same files: docs/game-design.md, assets/ (sprite library), vendor/phaser.min.js.
# ON: the repository is made from the AES template (copier), so its instructions, make check and hooks apply.
# OFF: a plain git repository with only those files.
arm=$1; n=$2; game=${3:-abyssal_chain}
BENCH=${BENCH:-/home/brian/projects/data/aes-gamebench}
PHASER_URL=https://cdnjs.cloudflare.com/ajax/libs/phaser/3.90.0/phaser.min.js
TEMPLATE=${AES_TEMPLATE:-gh:BrianMills2718/agentic-engineering-system-canonical}
[[ $arm == on || $arm == off ]] || { echo "arm must be on or off"; exit 2; }
/home/brian/.local/bin/storage-policy --need-gib 2 gate || exit 75
src=$BENCH/games/$game; dir=$BENCH/runs/$arm-$n; repo=$dir/repo
[[ -f $src/gdds/$game.md ]] || { echo "fetch the game first: fetch_game.py big $game $BENCH/games"; exit 1; }
[[ -e $dir ]] && { echo "$dir exists; refusing to overwrite"; exit 1; }
mkdir -p "$dir" || exit 1
if [[ $arm == on ]]; then
  uvx copier copy --trust --defaults --vcs-ref HEAD \
    -d project_name="$game" -d package_name="${game//-/_}" -d description="A 2D browser game built from its design document" \
    -d goal_actor="Brian, testing whether AES delivers every requirement of a long game design document" \
    -d goal_job="build the game the design document describes" -d goal_result="every requirement works in the browser" \
    -d ship_planning_gate=true -d ship_one_page_plans=true -d git_user_name=BrianMills2718 -d git_user_email=69022071+BrianMills2718@users.noreply.github.com \
    "$TEMPLATE" "$repo" > "$dir/copier.log" 2>&1 || { echo "copier failed: $dir/copier.log"; exit 1; }
else
  mkdir -p "$repo" && git -C "$repo" init -q || exit 1
fi
mkdir -p "$repo/docs" "$repo/assets" "$repo/vendor" || exit 1
cp "$src/gdds/$game.md" "$repo/docs/game-design.md" && cp "$src"/library/* "$repo/assets/" || exit 1
curl -sfL --max-time 120 -o "$repo/vendor/phaser.min.js" "$PHASER_URL" || { echo "phaser download failed"; exit 1; }
git -C "$repo" add -A && git -C "$repo" -c user.name=BrianMills2718 -c user.email=69022071+BrianMills2718@users.noreply.github.com \
  commit -q --no-verify -m "Benchmark start: design document, sprite library, Phaser 3.90.0" || exit 1
python3 - "$dir/meta-setup.json" "$arm" "$n" "$game" "$(git -C "$repo" rev-parse HEAD)" \
  "$(sha256sum "$repo/vendor/phaser.min.js" | cut -c1-64)" "$(grep -m1 '_commit' "$repo/.copier-answers.yml" 2>/dev/null)" <<'PY'
import json, sys, time
out, arm, n, game, head, phaser, tpl = sys.argv[1:]
json.dump({"arm": arm, "run": int(n), "game": game, "start_commit": head, "phaser_sha256": phaser,
           "template": tpl, "made": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, open(out, "w"), indent=1)
PY
echo "RESULT setup arm=$arm run=$n repo=$repo"
