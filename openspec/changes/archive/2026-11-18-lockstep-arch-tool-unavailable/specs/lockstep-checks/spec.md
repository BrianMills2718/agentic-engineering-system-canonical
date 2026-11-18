## ADDED Requirements

### Requirement: Arch: A diagram check that cannot run fails as a tool failure

`lockstep check arch` SHALL report that LikeC4 could not be run, and SHALL NOT report the diagram
invalid, when `npx` is absent or cannot be started, when `npx likec4 validate` exits non-zero without
LikeC4 having run, or when the JSON export of an already-validated diagram fails. Whether LikeC4 ran
SHALL be decided by running it against no diagram, not by matching words in its output. Each of these
SHALL print `RESULT arch-<action> tool_unavailable=1 exit=1` and exit 1: a check that did not run must
fail, not pass. A diagram LikeC4 read and rejected SHALL still be reported `invalid_diagram=1`.

Source: inferred by agent from the 2026-11-18 nightly failure in `BrianMills2718/enforced-planning`: a valid diagram was reported `invalid_diagram=1` because npm could not write a shared cache containing root-owned directories, which made the run look like a repository defect. Same distinction the module already makes with `ImportLinterMissing`.

#### Scenario: Arch: A missing npx is a tool failure

- **GIVEN** no `npx` on PATH
- **WHEN** `lockstep check arch check` runs
- **THEN** it says npx is not installed, prints `tool_unavailable=1`, does not print `invalid_diagram`, exits 1, and runs no npx

#### Scenario: Arch: A LikeC4 that cannot start is a tool failure

- **GIVEN** an npx whose `validate` and `--version` both exit non-zero, reporting an unwritable npm cache
- **WHEN** `lockstep check arch check` runs
- **THEN** it carries npm's own report, prints `tool_unavailable=1`, does not print `invalid_diagram`, and exits 1

#### Scenario: Arch: A failing diagram export is a tool failure

- **GIVEN** a diagram LikeC4 validates and a JSON export that exits non-zero
- **WHEN** `lockstep check arch check` runs
- **THEN** it prints `tool_unavailable=1`, does not print `invalid_diagram`, and exits 1
