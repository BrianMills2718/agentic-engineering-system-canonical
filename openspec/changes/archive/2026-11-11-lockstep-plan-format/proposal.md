# Lockstep reads its plan from OpenSpec plus lockstep.yaml layout rows (one-tool design, slice 2)

## Why

The one-tool design has one plan format: OpenSpec for what the code must do, plus `layout:` rows in `lockstep.yaml`
for which files exist and why (`proposals/one-planning-tool/DESIGN.md`, slice 2; Brian, 2026-11-11: "i approve
single tool desing re d4"). Until now Lockstep needed `.aes/target.yaml`.

## What changes

- `src/lockstep/layout_plan.py` reads `governed:` and `layout:` rows (path, purpose, implements, tests, exports) and
  checks them (a purpose on every row, no path twice, every requirement ID defined in OpenSpec).
- `aes_bridge` (Lockstep's one plan reader) uses the layout when a repository has `lockstep.yaml` with `layout:` and
  no `.aes/target.yaml`; with `.aes/target.yaml` everything reads as before.
- A layout row's docstring copy holds its `Implements:` line, each requirement word for word with its scenarios, its
  tests and its signatures.
- `lockstep layout` creates every planned file that does not exist and fills its docstring.
- `lockstep check` reads the layout: unplanned files under `governed:` folders and layout problems block.

## Not in this change

Retiring `.aes/target.yaml` (the design leaves its pace open); moving lifelike and Team-Brains (slice 6).
