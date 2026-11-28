## Why

A layout row can say `implements: []` while its file's docstring says `Implements: <requirement>`, and every check
passes. The link then runs only through the docstring and the test marker, so the plan cannot tell a reader which
requirements the file is meant to cover. Brian, 2026-11-27 18:50, reading the end-to-end example: "The plan row (5)
is empty: implements: [], tests: []. Here the link runs only through the docstring and the test marker, not through
the plan. So the plan file can't tell you which requirements this file is meant to cover." (gap 10b in the AES next
steps plan doc).

## What Changes

- `layout_problems` also reports a row whose file names, in an `Implements:` line, a requirement the row's
  `implements` does not list. `lockstep check` already blocks on every layout problem, so the whole-tree check and
  `make check` refuse the contradiction.
- AES's own rows that contradict their code (37 files, measured 2026-11-28) get the missing requirement IDs added.
- Not included: requiring each row to list every test tagged for its requirements. Measured on AES it flags 212 pairs
  in 32 rows, most for one requirement shared by many modules whose tests each cover one module, so it would be
  wrong more often than right.

## Impact

- `src/lockstep/layout_plan.py`, `tests/lockstep/test_lockstep_layout_plan.py`, `lockstep.yaml`.
