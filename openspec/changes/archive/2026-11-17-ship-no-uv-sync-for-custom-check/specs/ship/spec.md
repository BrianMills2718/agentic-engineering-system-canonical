## MODIFIED Requirements

### Requirement: Prepare a fresh worktree's environment before the check

Before running the check, `scripts/ship.py` SHALL run `uv sync --all-extras` when the repository top
has a `uv.lock` or `pyproject.toml`, no `.venv`, and the check is a `make` command (the repository's own Makefile check,
which the default `make check` is), and `npm ci` when it has a `package-lock.json` and
no `node_modules`. A `--check` that is not a `make` command SHALL NOT trigger `uv sync`, and ship SHALL print one line saying it was skipped.
Each step that runs SHALL be a logged step, and a nonzero exit SHALL stop the run with nothing
pushed and SHALL remove the `.venv` or `node_modules` that the failed step created. An environment that is already present SHALL be left alone.

Source: inferred by agent from a 14-day audit of `~/code2/.ship-logs/`: fresh worktrees failed the check for a missing `.venv` or `node_modules` (three wasted runs of about 2.5 minutes in one session). Changed 2026-11-17 on Brian's instruction: research_v3 could not ship a hook-only change with `--check` because `uv sync` failed on open-web-retrieval and left an empty `.venv`.

#### Scenario: A fresh worktree gets its environment before the check

- **GIVEN** a clean branch with `pyproject.toml` and `package-lock.json` but no `.venv` or `node_modules`
- **WHEN** ship runs with the Makefile check (`make check`), which needs both
- **THEN** it runs `uv sync --all-extras` and `npm ci` first, merges and exits 0, and a later run with both present runs neither

#### Scenario: A failing environment setup pushes nothing

- **GIVEN** a clean branch with `pyproject.toml`, no `.venv`, and `uv sync` exiting 1
- **WHEN** ship runs the Makefile check
- **THEN** it exits 1 without running the check, and the branch is not on the remote

#### Scenario: A failing environment setup leaves no empty folder

- **GIVEN** a clean branch with `pyproject.toml`, no `.venv`, and a `uv sync` that exits 1 after creating an empty `.venv`
- **WHEN** ship runs the Makefile check
- **THEN** it exits 1 and the `.venv` no longer exists

#### Scenario: A custom check does not sync the python environment

- **GIVEN** a clean branch with `pyproject.toml`, no `.venv`, and a `uv sync` that would exit 1
- **WHEN** ship runs with `--check` set to a command that is not a `make` command
- **THEN** `uv` is never called, the check runs, the branch merges and ship exits 0
