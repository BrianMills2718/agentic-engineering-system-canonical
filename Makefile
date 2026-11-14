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
	@echo "Running mypy..."
	@$(PYTHON) -m mypy src/ --ignore-missing-imports
	@echo ""
	@echo "All checks passed!"

check-full:  ## make check plus the slow end-to-end tests (installs, the whole-repository status run)
	@$(MAKE) --no-print-directory check
	@$(PYTHON) -m pytest tests/ -q --tb=short -n auto -m slow

.PHONY: check-doc-facts refresh-doc-facts
check-doc-facts:  ## Read-only freshness of declared facts, without whole-tree projection
	@PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from lockstep.doc_projection import project_facts; stale = project_facts(Path.cwd(), check=True); print("Declared fact projections stale:", len(stale)); print("\n".join(stale)); raise SystemExit(bool(stale))'

refresh-doc-facts:  ## Refresh declared facts using the current checkout
	@PYTHONPATH=src $(PYTHON) -c 'from lockstep.doc_projection import refresh_cli; raise SystemExit(refresh_cli([]))'
