## 1. Tests first (each marked `@pytest.mark.req("<capability>/<scenario-slug>")`)

- [x] 1.1 `tests/lockstep/checks/test_lockstep_check_changed.py`: one test per scenario of the four `Changed:` requirements, on throwaway git repositories built with `lockstep_checks_support`
- [x] 1.2 `tests/lockstep/checks/test_lockstep_check_test_first.py`: the three changed-scenario tests and the `existing=True` one
- [x] 1.3 `tests/lockstep/checks/test_lockstep_check_status.py`: a requirement reworded in an active change is `changed, not archived` and open
- [x] 1.4 Run them; every new test fails for the right reason before any source changes

## 2. Source

- [x] 2.1 `checks/spec.py`: collect scenario text; a helper that returns the plan with active deltas applied over the specs (REMOVED sections remove)
- [x] 2.2 `checks/changed.py`: read the base revision's `openspec/` and `docs/plans/` from git; compute the list, the plan for each requirement, the findings and the wording-only declarations
- [x] 2.3 `checks/test_first.py`: changed scenarios; at least one test must fail on the base; `existing=True` no exemption there; wording-only skipped
- [x] 2.4 `checks/status.py`: the `changed, not archived` state
- [x] 2.5 `checks/cli.py` and `checks/config.py`: the `changed` check, `--base`, `--json`, modes; the new `test-first` count fields
- [x] 2.6 `Implements:` lines in the docstrings; `lockstep check project` to write the requirement text

## 3. Finish

- [x] 3.1 `make check` exits 0
- [x] 3.2 `openspec archive lockstep-changed-requirements --yes`; `openspec validate --all --strict --no-interactive`
- [x] 3.3 `wiki/lockstep.md` and `.project-brain/now.md` say the check exists and what it does not do
