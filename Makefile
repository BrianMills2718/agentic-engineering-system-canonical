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
	@echo "Running mypy..."
	@$(PYTHON) -m mypy src/ --ignore-missing-imports
	@echo ""
	@echo "All checks passed!"

TRACE_ACCEPTED ?= docs/planning/trace-accepted.txt
TRACE_NOW ?= .trace-now.txt
TRACE_REPO ?= .

check-source-order:  ## Every requirement states its rule before its Source: line (spec lockstep-checks); items with no Source: line are an older backlog this target does not fail on
	@out=$$(PYTHONPATH=src $(PYTHON) -c 'import sys; from lockstep.checks.cli import run; sys.exit(run(["sources"]))' 2>&1); \
	if ! printf '%s\n' "$$out" | grep -q '^RESULT sources '; then printf '%s\n' "$$out" | tail -n 20; echo "check-source-order: the sources check did not run"; exit 1; fi; \
	bad=$$(printf '%s\n' "$$out" | grep '^source-first '); \
	if [ -n "$$bad" ]; then printf '%s\n' "$$bad"; exit 1; fi; echo "RESULT check-source-order exit=0"

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
