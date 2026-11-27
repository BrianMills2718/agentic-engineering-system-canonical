.PHONY: check fast docs docs-specs
# Git hooks export these (in worktrees especially); they would leak into tests' own throwaway repos.
unexport GIT_DIR GIT_INDEX_FILE GIT_WORK_TREE GIT_PREFIX GIT_COMMON_DIR GIT_OBJECT_DIRECTORY
# Each OpenSpec capability appears in the docs site through a file link (Zensical skips folder links).
docs-specs:
	@for d in openspec/specs/*/; do [ -d "$$d" ] || continue; c=$$(basename $$d); mkdir -p docs/specs/$$c; ln -sfn ../../../openspec/specs/$$c/spec.md docs/specs/$$c/spec.md; done
# Commit-hook checks: each finishes in seconds.
fast:
	uv run lockstep check trace
	uv run lockstep check sources
	uv run lockstep check project --check
	uv run lint-imports
	uv run pydoclint src
	uv run interrogate src
	openspec validate --all --strict --no-interactive
# Everything, run before merging. Lockstep status reads results from .code2check/ (its old name, still the path).
check: docs-specs fast
	mkdir -p .code2check && rm -f .code2check/junit.xml
	printf '{"commit": "%s", "clean": %s}\n' "$$(git rev-parse HEAD)" "$$(test -z "$$(git status --porcelain)" && echo true || echo false)" > .code2check/run.json
	@# On a test failure, still write generated/wiki/results.md (pass or fail per requirement) before stopping.
	uv run pytest --junitxml=.code2check/junit.xml || { status=$$?; uv run lockstep check project; exit $$status; }
	uv run lockstep check arch check
	uv run lockstep check test-first --base origin/main
	uv run lockstep check changed --base origin/main
	uv run lockstep check suppressions --base origin/main
	uv run lockstep check maintainability --base origin/main
	@# Whole-tree check: every file under a governed folder has a layout row in lockstep.yaml (Codex has no refusing hook).
	@base=$$(git merge-base origin/main HEAD 2>/dev/null || git rev-list --max-parents=0 HEAD 2>/dev/null | tail -n 1); \
	if [ -z "$$base" ]; then echo "whole-tree check skipped: no commit yet"; else uv run lockstep check --repo . --base "$$base"; fi
	uv run lockstep check project
	uv run python -m lockstep.wiki_reach
	uv run lockstep check docmeta
	uv run zensical build --strict
# docs/status.md is build output (ignored by git): `lockstep check project` writes it before each docs build.
docs: docs-specs
	uv run lockstep check project
	uv run zensical serve
