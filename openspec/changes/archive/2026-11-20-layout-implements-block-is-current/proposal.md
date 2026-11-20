## Why

In a repository that plans with `lockstep.yaml` `layout:` rows, the edit hook judged every planned Python file by the old AES plan copy, a cog block (`src/lockstep/stale_edit.py:44` calling `check.docstring_mismatch` at df891e49e). Only `lockstep layout` writes that block, and only into files it creates. A file that already existed when its row was added (every file in a retrofitted repository, and code2-template's own `core.py`) was reported as "the required docstring copy ... is missing", and under `PCW_MODE=block`, which `lockstep init` installs, every edit to it was refused. The refusal named `make project`, which code2-template repositories do not have, and an edit that inserted the block by hand was refused for the same reason.

Seen on 2026-11-20 in the from-scratch proof Brian approved ("yes", `docs/planning/next.goal.md`, step 3): with `src/` governed, a headless agent adding one flag got six such refusals and could not finish (`~/projects/data/notes/aes-local-proofs-20261120.md`, progress 16:25Z).

The design calls for one projector fed from OpenSpec (`proposals/one-planning-tool/DESIGN.md`, "What goes where"). Until the two are merged, the hook accepts the projection code2-template repositories already use.

## What Changes

- In a layout repository, a planned file with no cog block is current when `lockstep check project` would leave it unchanged, and stale when that command would rewrite its `Implements:` requirement text.
- A stale file's refusal there names `uv run lockstep check project`, and the after-edit hint names the same command. A file that has a cog block, and every repository with `.aes/target.yaml`, are judged as before.

## Impact

- `src/lockstep/stale_edit.py`, `src/lockstep/hook.py`; tests in `tests/lockstep/test_lockstep_layout_plan.py`.
- Every repository using the layout plan: planned files that predate their row become editable under block mode.

Plan size: full
Planning package: docs/planning/planning-package.json
