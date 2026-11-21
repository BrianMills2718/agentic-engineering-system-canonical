## Why

The clean-home milestone run (2026-11-21, recorded in `docs/planning/minimal-core-2026-11-20.md` section 8) found two
frictions in the minimal core. (1) The generated `docs/status.md` is committed, so any two plans merged one after
the other conflict on it, and `ship`'s catch-up rebase stops (code2-template#37). (2) `run-plan` prints
`... && ship`, but a second user has no `ship` on PATH; in a repository that depends on this package it is
`uv run ship` (#994).

## What Changes

- `lockstep check project --check` skips `docs/status.md` when git ignores it, so a repository can treat the page as
  build output (written by `lockstep check project`, never committed). `project` still writes it. code2-template
  then ignores the page and builds it in `make check` and `make docs`.
- `run-plan` prints `uv run ship` when the repository's `pyproject.toml` depends on `agentic-engineering-system`,
  else `ship`.

## Test seam

- `project(root, check=True)` in a git repository whose `.gitignore` lists `docs/status.md`.
- `plan_run.ship_command(repo) -> str`; `run_plan` output.

## Impact

- `src/lockstep/checks/project.py`, `src/lockstep/plan_run.py`, their tests, specs `lockstep-projection` and `plan-run`.

Plan size: small
