## 1. Tests first

- [x] 1.1 Replace the ported-check tests with tests that `lockstep plan check` runs the validator (a stand-in through
  `SHIP_PLANNING_VALIDATOR`), passes its exit status through, exits 2 without a package, and still adds work-unit problems

## 2. Build

- [x] 2.1 Move ship's validator fetch into `fetch_planning_validator`; `planning_gate` calls it
- [x] 2.2 Rewrite `plan_check.py` as the thin caller; remove `citation_anchor.py` and its fixture and tests
- [x] 2.3 Layout rows, docs that describe the port, regenerated copies
