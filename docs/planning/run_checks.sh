#!/usr/bin/env bash
# Run every planning-package check for AES canonical and write docs/planning/checks.txt.
# Each block records the command, its exit status and its full output, so the counts in
# planning-package.json can be read back from this file. Run from the repository root:
#   bash docs/planning/run_checks.sh
# Not run: `aes commit replay` (the commit rule was removed 2026-10-14; ledger Q11), `make aes` and the plan-adoption
# recheck (this repository's own `.aes/` and `docs/plans` were retired 2026-11-12; docs/retired/2026-11-12.md).
cd "$(git rev-parse --show-toplevel)" || exit 2
CP="$HOME/code2/company-planning/plugins/company-planning/scripts"
OUT=docs/planning/checks.txt
{
  echo "Planning-package checks for BrianMills2718/agentic-engineering-system-canonical at $(git rev-parse HEAD), run $(date -u +%Y-%m-%dT%H:%MZ)."
  echo "Company Planning scripts from ~/code2/company-planning at $(git -C "$HOME/code2/company-planning" rev-parse --short HEAD)."
  echo "Not run: aes commit replay (the commit rule was removed 2026-10-14; open question Q11); make aes and the plan-adoption recheck (retired 2026-11-12 with this repository's .aes/ and docs/plans)."
} > "$OUT"
run() {
  echo >> "$OUT"
  echo "=== \$ $1" >> "$OUT"
  bash -c "$1" > /tmp/aes-check.$$ 2>&1
  echo "=== exit status: $?" >> "$OUT"
  sed "s#$PWD#.#g" /tmp/aes-check.$$ >> "$OUT"
  rm -f /tmp/aes-check.$$
}
run "python3 \$HOME/code2/company-planning/plugins/company-planning/scripts/durable_docs_check.py --repo . --arc42"
run "python3 \$HOME/code2/company-planning/plugins/company-planning/scripts/validate_project_navigation.py ."
run "python3 \$HOME/code/project-meta/scripts/md_file_cap.py --repo . --ref HEAD"
run "python3 \$HOME/code2/workspace/scripts/repo_format.py ."
run "python3 -c 'import json,jsonschema,pathlib,sys; s=json.load(open(pathlib.Path.home()/\"code2/representation-router/schemas/typed-graph.schema.json\")); bad=0
for p in (\"docs/planning/domain.graph.json\",\"docs/planning/open-questions.graph.json\"):
    errs=list(jsonschema.Draft202012Validator(s).iter_errors(json.load(open(p))))
    print(p, \"valid\" if not errs else errs[0].message); bad+=bool(errs)
print(f\"graphs_valid={2-bad} graphs_invalid={bad}\"); sys.exit(bad)'"
echo "wrote $OUT"
