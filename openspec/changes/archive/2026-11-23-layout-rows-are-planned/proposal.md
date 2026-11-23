## Why

A plan names its files in `lockstep.yaml` `layout:` rows (DESIGN steps 2-4), but `run-plan` counts only files named
in `tasks.md`, so a file planned by a row reads as a departure, and its prompts never mention `lockstep layout`.
`docs/links.json` has no node for a planned file that does not exist yet, so the chain from requirement to file and
symbol shows only after the code exists. Source: Brian, 2026-11-23: "i approve", item (c) of
`docs/planning/back-on-design-2026-11-23.md`; plan `docs/planning/template-layout-2026-11-23.md`, steps 3 and 4.

## What Changes

- The departure report treats a path that has a layout row at `REF` as planned; `lockstep.yaml` and
  `docs/links.json` are never departures.
- The implementer's and writer's prompts name the layout rows; the implementer runs `uv run lockstep layout` first.
- `docs/links.json` gets a `file` node per layout row and a `symbol` node per export, each `planned` or `exists`.

## Impact

`src/lockstep/plan_run.py`, `src/lockstep/checks/status.py`, their tests. Repositories without layout rows are read
as before.
