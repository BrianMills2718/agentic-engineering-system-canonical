#!/usr/bin/env bash
# P4 live run (ER-AP-001-02): the three canonical-example commits plus observe mode, through the
# tracked hooks of AES canonical, on a throwaway branch. Prints a transcript; leaves the branch
# scratch/p4-live-<rev> behind (unpushed) and removes its worktree.
# Usage: proposals/aes-planning/evidence/run_p4_live.sh  (from an AES canonical checkout)
set -uo pipefail
repo=$(git rev-parse --show-toplevel); rev=$(git rev-parse --short HEAD)
main=$(cd "$(git rev-parse --git-common-dir)/.." && pwd)
wt="$main/worktrees/p4-live-$rev"
git -C "$main" worktree add -q "$wt" -b "scratch/p4-live-$rev" "$rev" || exit 2
cd "$wt"; unset PYTHONPATH
step() { echo; echo "\$ git commit -m \"$1\"   ($2)"; git commit -m "$1" 2>&1 | grep -v "^OK topology\|unrealized"; echo "exit ${PIPESTATUS[0]}"; }
echo "# P4 live run in AES canonical at $rev, $(date -u +%FT%TZ); tracked hooks, no PYTHONPATH"
sed -i 's/^mode: observe$/mode: enforce/' .aes/commit_rule.yaml; echo "# .aes/commit_rule.yaml set to enforce in this throwaway copy only"
printf 'FROM debian\nRUN apt-get install -y make\n' > Dockerfile; printf 'services:\n  app:\n    build: .\n' > compose.yaml; git add Dockerfile compose.yaml
step "[Unplanned] add worker tools" "staged: Dockerfile, compose.yaml"
step "[Goal aes-planning] U2: worker tools" "same staged change"
sed -i '0,/Agentic Engineering System/s//Agentic  Engineering System/' README.md; git add README.md
step "[Trivial] fix typo" "staged: README.md, one line"
sed -i 's/^mode: enforce$/mode: observe/' .aes/commit_rule.yaml; echo; echo "# back to the committed mode: observe"
printf 'FROM debian\n' > Dockerfile.worker; git add Dockerfile.worker
step "[Unplanned] add another worker image" "staged: Dockerfile.worker"
cd "$main"; git worktree remove "$wt"
