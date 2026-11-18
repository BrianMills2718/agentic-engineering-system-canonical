## 1. Tests first (each marked `@pytest.mark.req("lockstep-checks/<scenario-slug>")`)

- [ ] 1.1 `tests/lockstep/checks/test_lockstep_check_changed.py`: one test per scenario of "Changed: Every plan that names a listed requirement states its size" (eight), text output and `--json`, on throwaway repositories built with `lockstep_checks_support`
- [ ] 1.2 The test for "Changed: Nothing changed gives a zero count and exit 0" asserts the new zero line
- [ ] 1.3 Run them; every new or changed test fails for the right reason before any source changes
- [ ] 1.4 Existing tests whose plans must now state a size to exit 0 get the line `Plan size: small` (in this file and in `test_lockstep_check_test_first.py` where it asserts the changed count line)

## 2. Source

- [ ] 2.1 `checks/changed.py`: each plan carries the sizes it states and the planning-package paths it names, read outside fenced code blocks; each listed requirement gets a `size`; findings `no-plan-size` and `no-planning-package`; four new counts
- [ ] 2.2 `checks/cli.py`: a `size` line in each requirement's block, the two findings with what to add and where, the new count line
- [ ] 2.3 `Implements:` lines in the docstrings; `lockstep check project` to write the requirement text

## 3. Finish

- [ ] 3.1 `make check` exits 0
- [ ] 3.2 `openspec archive lockstep-plan-size --yes`; `openspec validate --all --strict --no-interactive`
- [ ] 3.3 `wiki/lockstep.md` and `.project-brain/now.md` say that a plan states its size and what each finding means
