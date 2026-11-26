# AES canonical checks. The claims, worktree, session and PR-flow targets that used to live here
# were retired on 2026-11-12 (docs/retired/2026-11-12.md); `ship` and `claude -w` replaced them.

PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

# --- During Implementation ---
.PHONY: test test-quick check check-full

# pytest and mypy run through $(PYTHON), which prefers .venv/bin/python, so a
# clean clone that followed the README's install uses the venv's tools. A bare
# `pytest` resolves on PATH instead and exits 127 for a cold reader.
test:  ## Run pytest
	$(PYTHON) -m pytest tests/ -v

test-quick:  ## Run pytest (no traceback)
	$(PYTHON) -m pytest tests/ -q --tb=no

check: check-doc-facts  ## Run all checks (test, mypy, lint)
	@echo "Running tests..."
	@$(PYTHON) -m pytest tests/ -q --tb=short -n auto -m "not slow"
	@echo ""
	@echo "Running the instruction-file check..."
	@PYTHONPATH=src $(PYTHON) -c 'import sys; from lockstep.checks.cli import run; sys.exit(run(["instructions"]))'
	@echo ""
	@echo "Running the trace check against its accepted list..."
	@$(MAKE) --no-print-directory check-trace
	@echo ""
	@echo "Running the plan-copy check..."
	@$(MAKE) --no-print-directory check-copies
	@echo ""
	@echo "Running the requirement-order check..."
	@$(MAKE) --no-print-directory check-source-order
	@echo ""
	@echo "Running the code2 format checks..."
	@$(MAKE) --no-print-directory check-format
	@echo ""
	@echo "Running mypy..."
	@$(PYTHON) -m mypy src/ --ignore-missing-imports
	@echo ""
	@echo "All checks passed!"

TRACE_ACCEPTED ?= docs/planning/trace-accepted.txt
TRACE_NOW ?= .trace-now.txt
TRACE_REPO ?= .

check-source-order:  ## Every requirement states its rule before its Source: line (spec lockstep-checks)
	@out=$$(PYTHONPATH=src $(PYTHON) -c 'import sys; from lockstep.checks.cli import run; sys.exit(run(["sources"]))' 2>&1); \
	if ! printf '%s\n' "$$out" | grep -q '^RESULT sources '; then printf '%s\n' "$$out" | tail -n 20; echo "check-source-order: the sources check did not run"; exit 1; fi; \
	bad=$$(printf '%s\n' "$$out" | grep '^source-first '); \
	if [ -n "$$bad" ]; then printf '%s\n' "$$bad"; exit 1; fi; echo "RESULT check-source-order exit=0"

LOCKSTEP ?= $(if $(wildcard .venv/bin/lockstep),.venv/bin/lockstep,uv run lockstep)
FORMAT_BASE ?= origin/main

# One format check: $(1) is the line its summary starts with, $(2) the `lockstep check` arguments. It fails when the
# check exits non-zero or prints no summary line (a check that did not run must not pass).
define format_check
	@out=$$($(LOCKSTEP) check $(2) 2>&1); ec=$$?; \
	if [ $$ec -ne 0 ] || ! printf '%s\n' "$$out" | grep -q '^$(1)'; then printf '%s\n' "$$out" | tail -n 20; echo "check-format: lockstep check $(2) failed (exit $$ec)"; exit 1; fi; \
	printf '%s\n' "$$out" | grep '^$(1)'
endef

check-format:  ## The code2 format checks the template's make check runs: import contracts, Source lines, page front matter, tests first, changed requirements, reasons on added suppressions, and the whole-tree plan check (the docs build does not apply: AES has no zensical site)
	$(call format_check,RESULT arch-check ,arch check)
	$(call format_check,RESULT sources ,sources)
	$(call format_check,docmeta: ,docmeta)
	$(call format_check,RESULT test-first ,test-first --base $(FORMAT_BASE))
	$(call format_check,RESULT changed ,changed --base $(FORMAT_BASE))
	$(call format_check,RESULT suppressions ,suppressions --base $(FORMAT_BASE))
	@base=$$(git merge-base HEAD $(FORMAT_BASE) 2>/dev/null); if [ -z "$$base" ]; then echo "check-format: no merge base with $(FORMAT_BASE)"; exit 1; fi; \
	out=$$($(LOCKSTEP) check --repo . --base "$$base" 2>&1); ec=$$?; \
	if [ $$ec -ne 0 ] || ! printf '%s\n' "$$out" | grep -q '^OUTCOME '; then printf '%s\n' "$$out" | tail -n 20; echo "check-format: the whole-tree check failed (exit $$ec)"; exit 1; fi; \
	printf '%s\n' "$$out" | grep '^OUTCOME '
	@$(MAKE) --no-print-directory check-prior-art
	@$(MAKE) --no-print-directory check-md-cap
	@$(MAKE) --no-print-directory check-maintainability
	@echo "RESULT check-format exit=0"

check-prior-art:  ## The prior-art record check ship runs, on the OpenSpec changes this branch adds or changes since $(FORMAT_BASE), so a bad record fails here and not first at merge (src/lockstep/prior_art.py)
	@base=$$(git merge-base HEAD $(FORMAT_BASE) 2>/dev/null); \
	files=$$(git diff --name-only --diff-filter=d $$base HEAD -- openspec/changes 2>/dev/null); \
	if [ -n "$$base" ] && [ -z "$$files" ]; then echo "check-prior-art: no OpenSpec change added or changed"; exit 0; fi; \
	if [ -n "$$base" ]; then $(PYTHON) src/lockstep/prior_art.py --repo . --files $$files; else $(PYTHON) src/lockstep/prior_art.py --repo .; fi; \
	ec=$$?; if [ $$ec -ne 0 ]; then echo "check-prior-art: failed (exit $$ec)"; exit 1; fi

check-maintainability:  ## Fail on a blind except, a more complex function, more duplicate code or a large file that grew since the branch left $(FORMAT_BASE); old findings never block (lockstep check maintainability, on in lockstep.yaml)
	@out=$$($(LOCKSTEP) check maintainability --repo . --base $(FORMAT_BASE) 2>&1); ec=$$?; \
	if [ $$ec -ne 0 ] || ! printf '%s\n' "$$out" | grep -Eq '^RESULT maintainability |^maintainability: skipped \(off\)'; then printf '%s\n' "$$out" | tail -n 30; echo "check-maintainability: failed (exit $$ec)"; exit 1; fi; \
	printf '%s\n' "$$out" | grep -E '^RESULT maintainability |^maintainability: skipped \(off\)'

LLM_PYTHON ?= $(HOME)/code2/llm_client/.venv/bin/python

check-helper-reuse:  ## Report functions this branch adds that rewrite an existing function under a new name (light model via llm_client, about $$0.006 a run; report-only, not in make check; lockstep.checks.helper_reuse run with llm_client's Python)
	@PYTHONPATH=src $(LLM_PYTHON) -m lockstep.checks.helper_reuse --repo . --base $(FORMAT_BASE)

check-md-cap:  ## The 100-file Markdown cap (Brian, 2026-10-07), its exception in .md-file-cap.yaml, wiki reachability, layout and durable documents, read from the committed tree
	@out=$$($(PYTHON) scripts/md_file_cap.py --repo . --ref HEAD 2>&1); ec=$$?; \
	if [ $$ec -ne 0 ] || ! printf '%s\n' "$$out" | grep -q '^md-file-cap: '; then printf '%s\n' "$$out" | tail -n 20; echo "check-md-cap: failed (exit $$ec)"; exit 1; fi; \
	printf '%s\n' "$$out" | grep '^md-file-cap: '

check-copies:  ## A planned file's plan copy must be current and a fixed: file must have one (spec lockstep-projection); the committed status page and links file keep their own refresh
	@out=$$(PYTHONPATH=src $(PYTHON) -c 'import sys; from lockstep.checks.cli import run; sys.exit(run(["project", "--check"]))' 2>&1); \
	if ! printf '%s\n' "$$out" | grep -q '^RESULT project '; then printf '%s\n' "$$out" | tail -n 20; echo "check-copies: the project check did not run"; exit 1; fi; \
	bad=$$(printf '%s\n' "$$out" | grep -E '^(stale|no-copy) ' | grep -vE ' docs/(status\.md|links\.json)$$'); \
	if [ -n "$$bad" ]; then printf '%s\n' "$$bad"; echo "check-copies: run: lockstep check project (and add a plan copy to each no-copy file)"; exit 1; fi; \
	echo "RESULT check-copies exit=0"

check-trace:  ## Trace findings must equal $(TRACE_ACCEPTED): a new finding fails, and a fixed one must leave the list
	@PYTHONPATH=src $(PYTHON) -c 'import sys; from lockstep.checks.cli import run; sys.exit(run(["trace", "--repo", "$(TRACE_REPO)"]))' 2>/dev/null \
	  | grep -v '^RESULT' | sed -e 's/  (.*//' -e 's/  */ /g' | sort -u > $(TRACE_NOW); \
	if diff -u $(TRACE_ACCEPTED) $(TRACE_NOW); then \
	  echo "RESULT check-trace accepted=$$(wc -l < $(TRACE_ACCEPTED)) exit=0"; \
	else \
	  echo "check-trace: findings differ from $(TRACE_ACCEPTED) (+ a new finding to fix; - a fixed finding to delete from the list)"; exit 1; \
	fi

check-full:  ## make check plus the slow end-to-end tests (installs, the whole-repository status run)
	@$(MAKE) --no-print-directory check
	@$(PYTHON) -m pytest tests/ -q --tb=short -n auto -m slow

.PHONY: check-doc-facts refresh-doc-facts
check-doc-facts:  ## Read-only freshness of declared facts, without whole-tree projection
	@PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from lockstep.doc_projection import project_facts; stale = project_facts(Path.cwd(), check=True); print("Declared fact projections stale:", len(stale)); print("\n".join(stale)); raise SystemExit(bool(stale))'

refresh-doc-facts:  ## Refresh declared facts using the current checkout
	@PYTHONPATH=src $(PYTHON) -c 'from lockstep.doc_projection import refresh_cli; raise SystemExit(refresh_cli([]))'
