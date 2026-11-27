## Why

Where `ship` finds the project graph (whose folder holds `graph-config.yaml`, which names the plan list) is hardcoded:
`$PROJECT_GRAPH`, else `~/code2/aes-config/PROJECT_GRAPH.json` (`src/lockstep/ship.py`). A person whose settings live
elsewhere must export a variable in every shell and timer that runs ship. Brian, 2026-11-25: "the whole systm should be
configurable so you can congfigure what is on or off or any other settings. for any piece" (docs/planning/next.goal.md,
parking item "`planning.project_graph` replaces the `~/code2/aes-config` default").

Plan: `docs/planning/next.goal.md` (parking list, "`planning.project_graph` replaces the `~/code2/aes-config` default").

Plan size: small

Wording-only: ship/settings-come-from-config

That requirement still reads the same plan-list keys with the same environment overrides and refusal.
Its description of graph selection now points to the new requirement, which owns and tests the changed behavior.

Planning package: none (small change: this proposal is the plan)

## What Changes

- `ship` finds the project graph from `$PROJECT_GRAPH`, else `planning.project_graph` in `lockstep.yaml` on the default
  branch at origin (never the branch being shipped), else the old default, so nothing changes until a repository sets it.
- It prints and logs `ship: project graph: <folder> (<source>)` when it reads the plan list.
- The value must be a local path to a `.json` file starting with `~` or `/`. Anything else (a git address, a relative
  path, a folder) is named by the side-file check and refused as a plan-list refusal at merge time, which
  `planning.gate` then refuses or warns about.
- `planning_modes` accepts the new key.

## Impact

- New `src/lockstep/checks/project_graph.py` (the lookup, its check and the graph-config reader moved out of ship.py,
  which shrinks by 9 lines); `src/lockstep/ship.py`, `src/lockstep/checks/config.py`, `src/lockstep/side_file.py`.
- Tests: `tests/lockstep/checks/test_lockstep_check_project_graph.py`, `tests/test_ship.py`.
- Not changed: `lane_sweep.py` keeps its own `$PROJECT_GRAPH` lookup; it sweeps many repositories and has no one
  repository's `lockstep.yaml` to read.
