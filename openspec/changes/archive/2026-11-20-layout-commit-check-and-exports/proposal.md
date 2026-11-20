## Why

# 977 let the edit hook judge a layout repository's file without a cog plan copy by its `Implements:` block. The rerun of the from-scratch proof on 2026-11-20 (Brian, "yes", `docs/planning/next.goal.md`, step 3) then built the feature with `make check` at exit 0, but could not commit it: the whole-tree commit check (`src/lockstep/check.py:342` at f59dcf2a4) called the same cog-only test and blocked both files, naming `.aes/target.yaml` and `cog -r -c`, neither of which applies there. The edit hook's refusal of an undeclared public function named `aes plan prepare/validate/accept`, a command a layout repository does not use; there the fix is the layout row's `exports:` list

## What Changes

- The layout rule moves into `check.docstring_mismatch`, so the edit hook and the commit check judge a file the same way; a new layout file with no cog block is not refused for lacking one.
- In a layout repository the commit check's stale reason names `uv run lockstep check project`, and the symbol refusals name the layout row's `exports:` in lockstep.yaml. Repositories with `.aes/target.yaml` keep the old wording.

## Impact

- `src/lockstep/check.py`, `src/lockstep/stale_edit.py`, `src/lockstep/symbol_gate.py`; tests in `tests/lockstep/test_lockstep_layout_plan.py`.

Plan size: full
Planning package: docs/planning/planning-package.json
