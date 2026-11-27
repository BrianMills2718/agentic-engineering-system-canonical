## Why

Each AES part is switched in `lockstep.yaml` (commit checks, ship's two planning gates, the validator source, the edit
guard), and ship records every planning-gate run, but nothing shows the settings and the last results together: a
person reads the YAML and greps the record files by hand. Brian, 2026-11-25: "the whole systm should be configurable so
you can congfigure what is on or off or any other settings. for any piece" (docs/planning/next.goal.md, parking item
"`lockstep status` prints each part's mode and last result").

Plan: `docs/planning/next.goal.md` (parking list, "`lockstep status` prints each part's mode and last result").

Plan size: small

Planning package: none (small change: this proposal is the plan)

## What Changes

- `lockstep status --parts` prints one table, one row per part: each commit check, `planning.gate`,
  `planning.one_page_plans`, `planning.validator` and `planning.skills` when set, `guard.mode`, and the rules and
  feedback parts as `not built`. The mode is read from the working tree's `lockstep.yaml` with the usual defaults.
- For the two planning gates, the last result is the newest record in ship's `planning-verdicts/*.jsonl` whose `repo`
  is this repository's origin; other rows say `no record`. `--json` prints the same rows as JSON.
- An unreadable `lockstep.yaml` exits 2. Plain `lockstep status`, `--json` and `--md` are unchanged; `lockstep status`
  was already the requirement report, so the parts table is a flag on it rather than a new command.

## Impact

- New `src/lockstep/checks/parts.py`; `src/lockstep/checks/cli.py` (the flag); `tests/lockstep/checks/test_lockstep_check_parts.py`.
- No setting, gate or record format changes.
