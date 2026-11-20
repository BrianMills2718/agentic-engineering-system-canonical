## 1. Tests first (each marked `@pytest.mark.req("lockstep-plan-check/<scenario-slug>")`)

- [x] 1.1 `tests/lockstep/test_lockstep_citation_anchor.py`: the shared cases (`tests/lockstep/fixtures/citation_anchor_cases.json`) and one test per scenario through `plan_cli`
- [x] 1.2 Run them; each fails for the right reason before any source changes

## 2. Source

- [x] 2.1 `src/lockstep/citation_anchor.py`: `anchor_problem(file_text, fragment)`
- [x] 2.2 `plan_check._citation` routes any `#:~:text=` string to it
- [x] 2.3 `Implements:` line; `lockstep check project`; `make check` exits 0
