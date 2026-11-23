## MODIFIED Requirements

### Requirement: A departure report compares the change with its plan

The departure report SHALL list every file changed in commits since `REF` whose repository-relative path does not appear in the change's `tasks.md` as read from `REF` and is neither the `path` of a `layout:` row in `lockstep.yaml` as read from `REF` nor a file one of those rows names in its `tests:`, excluding files under `openspec/`, the OpenSpec spec links `make docs-specs` writes under `docs/specs/`, `lockstep.yaml` itself and the generated `docs/links.json`, and every task line still unticked in the change's `tasks.md` at the branch head, read from `openspec/changes/<change>/` or, once archived, from the latest `openspec/changes/archive/YYYY-MM-DD-<change>/`. It reports and never blocks.

Source: Brian, 2026-11-20: "the goal is to give a well specified plan to an agent on some proejct nad have it faithfulyy and successfully impelemnt it"; report-only, inferred by agent from minimal-core-2026-11-20.md C4 and K5 (a check becomes blocking only after it is shown to catch something).

#### Scenario: A file outside the tasks is listed

- **GIVEN** a change whose `tasks.md` at `REF` names `src/app.py`, and commits since `REF` that changed `src/app.py`, `src/other.py`, `tests/test_new.py` and the change's `tasks.md`
- **WHEN** the departure report runs
- **THEN** it lists `src/other.py` and `tests/test_new.py` as outside the tasks and lists neither `src/app.py` nor the OpenSpec file

#### Scenario: A name added to tasks.md after REF does not count

- **GIVEN** the implementer added `src/other.py` to `tasks.md` in its own commit
- **WHEN** the departure report runs
- **THEN** `src/other.py` is still listed as outside the tasks

#### Scenario: An unticked task is listed, archived or not

- **GIVEN** the change was archived to `openspec/changes/archive/2026-11-20-<change>/` with one `- [x]` line and one `- [ ]` line in its `tasks.md`
- **WHEN** the departure report runs with the change's name
- **THEN** it lists the `- [ ]` line as unticked and not the ticked one

Source: Brian, 2026-11-23: "i approve", item (c) of `docs/planning/back-on-design-2026-11-23.md` (a plan names its files in `layout:` rows); plan `docs/planning/template-layout-2026-11-23.md`, step 3.

#### Scenario: A file planned by a layout row at REF is not listed

- **GIVEN** `lockstep.yaml` at `REF` has a `layout:` row with path `src/planned.py`, `tasks.md` does not name it, and commits since `REF` added `src/planned.py`, changed `lockstep.yaml` and added `src/late.py`, whose row was added after `REF`
- **WHEN** the departure report runs
- **THEN** it lists `src/late.py` and lists neither `src/planned.py` nor `lockstep.yaml`

Source: inferred by agent from the template-layout proof run of 2026-11-23 (docs/evidence/template-layout-proof-2026-11-23/summary.json): the row's own test file and the `docs/specs/` link of the archived spec were listed as departures although the plan named the one and the other is generated.

#### Scenario: A row's test file and a spec link are not listed

- **GIVEN** `lockstep.yaml` at `REF` has a row for `src/planned.py` whose `tests:` names `tests/test_planned.py`, and commits since `REF` added `tests/test_planned.py`, `docs/specs/greeting/spec.md` and `tests/test_other.py`
- **WHEN** the departure report runs
- **THEN** it lists only `tests/test_other.py`
