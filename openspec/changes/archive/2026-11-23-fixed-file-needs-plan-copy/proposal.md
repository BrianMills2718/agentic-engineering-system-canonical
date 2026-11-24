## Why

A planned file's plan copy (the cog block in its docstring) is what an editing agent reads. Copies went stale after
layout rows changed, and a planned file with no block (`src/lockstep/plan_check.py`) was never given a copy, with no
check failing (alignment cleanup item 14). Brian approved making `make check` fail on both (2026-11-23: "i approve",
to Q53 in `docs/planning/open-questions.json`).

## What Changes

- `lockstep check project` (with or without `--check`) reports each layout row whose file matches a `fixed:` glob,
  is a Python file that exists, and has no cog plan copy naming its ID, as `no-copy <path>`, and exits 1.
- AES's `make check` runs `lockstep check project --check` over its source files, so a stale copy or a missing
  one fails the merge; its committed `docs/status.md` and `docs/links.json` are left to their own refresh.
- The 11 planned files in `src/lockstep/` with no block get one.
