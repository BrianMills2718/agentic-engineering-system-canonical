#!/bin/bash
# Copy one finished build for grading with every AES trace removed, under a random id, so the grader cannot see the arm.
# Usage: blind_copy.sh <on|off> <run number>. The id-to-arm map is $BENCH/blind-map.tsv (the grader is not told of it).
arm=$1; n=$2; game=${3:-abyssal_chain}; BENCH=${BENCH:-/home/brian/projects/data/aes-gamebench}
repo=$BENCH/runs/$arm-$n/repo; [[ -d $repo ]] || { echo "no repo at $repo"; exit 1; }
id=$(od -An -N4 -tx4 /dev/urandom | tr -d ' '); out=$BENCH/grade/$id/game
mkdir -p "$out" || exit 1
starter=()
if [[ $arm == on ]]; then
  start=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["start_commit"])' "$BENCH/runs/$arm-$n/meta-setup.json") || exit 1
  # Omit unchanged Python starter files. Keep modified source for the grader and check it for arm markers.
  for path in src/"${game//-/_}"/{__init__,cli,core}.py tests/test_core.py; do
    if git -C "$repo" cat-file -e "$start:$path" &&
       git -C "$repo" diff --quiet "$start" -- "$path"; then
      starter+=(--exclude "/$path")
    fi
  done
fi
rsync -am --exclude .git --exclude 'AGENTS.md' --exclude 'CLAUDE.md' --exclude 'Makefile' --exclude 'lockstep.yaml' \
  --exclude 'openspec/' --exclude 'docs/planning/' --exclude 'docs/decisions/' --exclude 'docs/architecture/' \
  --exclude 'proposals/' --exclude '.claude/' --exclude '.agents/' --exclude '.codex/' --exclude '.githooks/' \
  --exclude 'lefthook.yml' --exclude 'mkdocs.yml' --exclude '.copier-answers.yml' --exclude '.doc-reachability-ignore' \
  "${starter[@]}" --exclude '/.gitignore' --exclude '/.venv/' --exclude '/pyproject.toml' --exclude '/uv.lock' --exclude '/.python-version' \
  --exclude '/.code2check/' --exclude '/.pytest_cache/' --exclude '__pycache__/'  --exclude '/.importlinter' --exclude '/docs/specs/' --exclude '/docs/reference/' \
  --exclude '/docs/GOAL.md' --exclude '/docs/GOAL.sources.json' --exclude '/docs/index.md' \
  --exclude '/docs/status.md' --exclude '/docs/links.json' --exclude '/README.md' \
  --exclude 'generated/' --exclude 'wiki/' --exclude '.project-brain/' --exclude 'node_modules/' "$repo/" "$out/" || exit 1
# What stays: the game (index.html, source, assets, vendor), its own tests and the design document.
left=$(grep -rIl -i -E 'lockstep|openspec|agentic-engineering|copier' "$out" --exclude-dir=assets --exclude-dir=vendor | head -5)
if [[ -n $left ]]; then
  printf 'Arm markers remain in private copy %s:\n%s\n' "$id" "$left" >&2
  exit 2
fi
printf '%s\t%s\t%s\n' "$id" "$arm" "$n" >> "$BENCH/blind-map.tsv" || exit 1
echo "RESULT blind id=$id"
