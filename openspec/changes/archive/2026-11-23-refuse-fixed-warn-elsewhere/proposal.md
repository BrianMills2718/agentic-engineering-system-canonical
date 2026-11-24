## Why

Slice 3 of `docs/planning/back-on-design-2026-11-23.md` settles what the minimal core built without the settled
design saying so. One item looked like a conflict: `proposals/one-planning-tool/DESIGN.md:30` (step 4) says a
write to a file the plan does not name "is refused", while the edit hook only warns unless `PCW_MODE=block` is set
or the file matches a `fixed:` glob (`src/lockstep/hook.py:257-284`). That default is Brian's decision D7
(2026-11-07, `lockstep` repository `.aes/plans/PLAN-014-WARN-BY-DEFAULT.yaml:5-7`): "Lockstep warns; it blocks only
files the plan marks fixed, after two weeks of would-block counts." The template marks its package `fixed:` and
this repository marks `src/lockstep/` `fixed:`, so planned code is refused as DESIGN step 4 shows and D7 holds for
the rest. No requirement stated the rule; this one does, so a change to it fails a test.

## What Changes

- New requirement in `lockstep-guard` stating the rule; three existing tests are marked for its scenarios.
- No code changes.
