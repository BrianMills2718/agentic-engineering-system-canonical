# `lockstep plan check` runs Company Planning's validator instead of a copy of two of its checks

Plan size: full
Planning package: docs/planning/planning-package.json

Full, not small: `lockstep plan check` ships in the Lockstep package that other repositories install.

## Why

There were two plan checkers. `ship` runs Company Planning's `validate_planning_package.py` on every merge
(`openspec/specs/ship/spec.md`, "Refuse a planning package the validator rejects"). `lockstep plan check` held a
port of two of that validator's checks (the acceptance-criteria file and requirement coverage, copied at
company-planning b8a53a0) and a copy of its citation-anchor code, so the same rules lived in two places and drifted
apart: the validator has since grown more checks of the acceptance part, and the anchor code was kept equal only by a shared
fixture table. One-tool design slice 5 (`proposals/one-planning-tool/DESIGN.md`) left open which tool calls which.
Brian approved one plan checker (Brian, 2026-11-25: "ia prpove yourr ecommednations though"). Company
Planning's validator stays that checker because it is the original, it checks the whole package, and Inside Success
teammates install it from the Inside-Success/company-planning mirror. Keeping it was inferred by agent from those
three facts and reported to Brian on 2026-11-25.

No automated caller ran `lockstep plan check` (searched `~/code2`: no Makefile, hook, template or ship step), and every
`~/code2` repository with an acceptance file also has a planning package, so no repository loses a check.

## What changes

- `lockstep plan check` runs Company Planning's validator on `docs/planning/planning-package.json`, fetched and run
  the way `ship` does (same function, same `SHIP_PLANNING_VALIDATOR` and `SHIP_VALIDATOR_PYTHON` overrides), and
  exits with its status; it still adds the work-unit DAG problems when `docs/planning/work-units.json` exists.
- Removed from Lockstep: the copied acceptance and requirement checks, `--acceptance`, and `src/lockstep/citation_anchor.py`
  with its fixture table (Company Planning keeps its own copy).
- `ship`'s validator fetch moves into one function both callers use.

## Impact

`src/lockstep/plan_check.py`, `src/lockstep/ship.py`, removed `src/lockstep/citation_anchor.py`, tests under
`tests/lockstep/`, `lockstep.yaml` rows, `openspec/specs/lockstep-plan-check/spec.md`, docs that describe the port.
