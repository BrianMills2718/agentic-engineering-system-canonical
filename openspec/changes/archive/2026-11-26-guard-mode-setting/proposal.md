## Why

The edit guard's strictness can only be set through the `PCW_MODE` environment variable, and `lockstep init` hardcodes
`PCW_MODE=block` into the hook command it installs, so a repository cannot switch its own guard between refusing and
warning in `lockstep.yaml` like every other part. Brian, 2026-11-25: "the whole systm should be configurable so you can
congfigure what is on or off" (docs/planning/next.goal.md, "Every switch and where it lands": edit-guard strictness,
parking item `guard.mode`).

Plan: `docs/planning/next.goal.md` (parking list, "`guard.mode` replaces the `PCW_MODE` hardcode in the hook command").

Plan size: small

## What Changes

- The edit hook reads `guard.mode` (`block` or `warn`) from `lockstep.yaml`. A set `PCW_MODE` still wins, so a person
  can override it for one session; an absent setting still means `warn` (decision D7). A value that is neither, or a
  `lockstep.yaml` that cannot be read, counts as `block`, and `python -m lockstep.unplanned_files` names the bad value.
- `lockstep init` writes `guard: {mode: block}` into a new `lockstep.yaml` and no longer puts `PCW_MODE=block` in the
  hook command, so a fresh install still refuses as before.
- `lockstep init` rewrites a hook command it wrote earlier (exactly `PCW_MODE=block uvx --from <source> lockstep-hook`)
  to the new command only when the repository's `lockstep.yaml` already has a `guard:` section, so no installed
  repository silently drops from refusing to warning; otherwise it leaves the command and prints how to switch.

## Impact

- `src/lockstep/side_file.py`, `src/lockstep/hook.py`, `src/lockstep/init_repo.py`, `src/lockstep/unplanned_files.py`
  (reports a bad `guard.mode`), `tests/lockstep/test_lockstep_hook.py`, `tests/lockstep/test_lockstep_init.py`.
- Repositories without a `guard:` section, AES itself and template copies included, behave exactly as before.
