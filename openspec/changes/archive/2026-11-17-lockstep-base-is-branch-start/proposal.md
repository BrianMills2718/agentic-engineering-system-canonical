## Why

The changed check and the test-first check compared the current revision with `<rev>` exactly as given. On the
first run of the changed check on a branch that was behind `origin/main` (2026-11-17), four requirements merged
into `origin/main` after the branch started were listed as `removed` and `unplanned`: the check counted other
branches' merges as this branch's changes. A repository that adds `lockstep check changed --base origin/main` to
its `make check` would fail on every branch that is behind main. Test-first has the same property for a scenario
reworded on main.

Source: inferred by agent, from that run.

## What Changes

- Both checks compare with the merge base of `<rev>` and the current commit: the commit the branch started from.
  With no shared history, or no commit yet, they compare with `<rev>` itself.
- `changed --json` adds `compared`, the commit that was compared with.

## Impact

`src/lockstep/checks/changed.py`, `src/lockstep/checks/test_first.py`. A branch that is up to date with `<rev>`
sees no difference: its merge base is `<rev>`.

Closes: lockstep-checks/changed-and-test-first-the-base-is-where-the-branch-started
