## 1. Departures and prompts

- [x] 1.1 Tests first in `tests/lockstep/test_lockstep_plan_run.py`: the layout-row departure scenario and the prompt
      scenario, failing.
- [x] 1.2 `src/lockstep/plan_run.py`: read layout row paths from `lockstep.yaml` at `REF`; skip them, `lockstep.yaml`
      and `docs/links.json`; prompt text.

## 2. Planned nodes in links

- [x] 2.1 Tests first in `tests/lockstep/checks/test_lockstep_check_links.py`: the two scenarios, failing.
- [x] 2.2 `src/lockstep/checks/status.py`: `file` and `symbol` nodes from layout rows with `state`; a comment
      implementer links its requirement to the file.
