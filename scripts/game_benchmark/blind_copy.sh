#!/bin/bash
# Copy one finished build for grading with every AES trace removed, under a random id, so the grader cannot see the arm.
# Usage: blind_copy.sh <on|off> <run number>. The id-to-arm map is $BENCH/blind-map.tsv (the grader is not told of it).
arm=$1; n=$2; BENCH=${BENCH:-/home/brian/projects/data/aes-gamebench}
repo=$BENCH/runs/$arm-$n/repo; [[ -d $repo ]] || { echo "no repo at $repo"; exit 1; }
id=$(od -An -N4 -tx4 /dev/urandom | tr -d ' '); out=$BENCH/grade/$id/game
mkdir -p "$out" || exit 1
rsync -a --exclude .git --exclude 'AGENTS.md' --exclude 'CLAUDE.md' --exclude 'Makefile' --exclude 'lockstep.yaml' \
  --exclude 'openspec/' --exclude 'docs/planning/' --exclude 'docs/decisions/' --exclude 'docs/architecture/' \
  --exclude 'proposals/' --exclude '.claude/' --exclude '.agents/' --exclude '.codex/' --exclude '.githooks/' \
  --exclude 'lefthook.yml' --exclude 'mkdocs.yml' --exclude '.copier-answers.yml' --exclude '.doc-reachability-ignore' \
  --exclude 'generated/' --exclude 'wiki/' --exclude '.project-brain/' --exclude 'node_modules/' "$repo/" "$out/" || exit 1
# What stays: the game (index.html, source, assets, vendor), its own tests and the design document.
left=$(grep -rIl -i -E 'lockstep|openspec|agentic-engineering|copier' "$out" --exclude-dir=assets --exclude-dir=vendor | head -5)
[[ -n $left ]] && echo "WARNING arm traces left in: $left"
printf '%s\t%s\t%s\n' "$id" "$arm" "$n" >> "$BENCH/blind-map.tsv"
echo "RESULT blind id=$id"
