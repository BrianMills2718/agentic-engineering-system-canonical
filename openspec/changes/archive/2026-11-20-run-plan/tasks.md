## 1. Departure report

- [x] 1.1 Tests first in `tests/lockstep/test_lockstep_plan_run.py`: unnamed file and new test file listed, OpenSpec file not, a name added after REF still listed, unticked task listed from an archived change
- [x] 1.2 `departures()` in `src/lockstep/plan_run.py`

## 2. Hidden acceptance and the driver

- [x] 2.1 Tests first, with a fake runner: tests outside the worktree until the last commit, writer worktree removed, before-run flag, collision refused, uncommitted counted, prompt and environment carry no run path, `peek_reads`, agent commands, driver does not merge
- [x] 2.2 `accept_write()`, `accept_check()`, `run_plan()`, the two prompts, `agent_command()` and the CLI in `src/lockstep/plan_run.py`; `accept` and `run-plan` branches in `src/lockstep/check.py`
- [x] 2.3 One live `run-plan --agent claude` on a fresh repository made from code2-template with a one-scenario plan; run id and result in the pull request

## 3. Docs

- [x] 3.1 Spec `openspec/specs/plan-run/spec.md` by archive, Purpose written, linked from the page that lists Lockstep commands
