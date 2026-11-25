## ADDED Requirements

### Requirement: `lockstep plan check` runs Company Planning's validator

`lockstep plan check` SHALL accept `--repo PATH` (default the current directory) and `--json`. It SHALL run Company
Planning's `validate_planning_package.py` on `docs/planning/planning-package.json` under the repository, fetched from
origin/main of Company Planning and run by the same function and interpreter choice `ship` uses (so
`SHIP_PLANNING_VALIDATOR`, `SHIP_COMPANY_PLANNING` and `SHIP_VALIDATOR_PYTHON` work the same), print the validator's
output, and exit with the validator's exit status. When `docs/planning/work-units.json` exists it SHALL also report the
work-unit problems and exit 1 when there are any. It SHALL exit 2, saying why, when the repository has no planning
package or the validator cannot be fetched or run. With `--json` it SHALL print one object with `ok`, the validator's
exit status and output, and the work-unit problems. Lockstep SHALL hold no copy of the validator's checks.

Source: Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 5: "`lockstep plan check` validates it"); one plan checker approved by Brian, 2026-11-25: "ia prpove yourr ecommednations though" (Company Planning's validator kept as that checker: inferred by agent, `openspec/changes/archive/*-one-plan-checker/proposal.md`).

#### Scenario: The validator's verdict is the command's verdict

- **GIVEN** a repository with a planning package and a validator that exits 1
- **WHEN** `lockstep plan check` runs
- **THEN** it prints the validator's output and exits 1; with a validator that exits 0 it exits 0

#### Scenario: A repository with no planning package cannot be checked

- **GIVEN** a repository without `docs/planning/planning-package.json`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 2 and names the missing package

#### Scenario: Work-unit problems are added

- **GIVEN** a planning package the validator passes and a work-units file with a unit depending on a missing unit
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and names the work-unit problem

## REMOVED Requirements

### Requirement: The command is reached as `lockstep plan check`

**Reason**: Its `--acceptance` option went with the copied acceptance check.
**Migration**: Replaced by "`lockstep plan check` runs Company Planning's validator".

### Requirement: The acceptance-criteria file is validated

**Reason**: A copy of Company Planning's acceptance check (`_check_acceptance`), which the validator still runs.
**Migration**: `lockstep plan check` and `ship` run the validator, which checks the acceptance part of the package.

### Requirement: Each plan requirement is sourced in Brian's words and covered

**Reason**: A copy of Company Planning's `coverage_check.py` checks, which the validator still runs.
**Migration**: The validator checks the stored coverage judgment as part of the package.

### Requirement: A citation may name the text it points at

**Reason**: A copy of Company Planning's `citation_anchor.py`, which the validator still uses.
**Migration**: Anchored citations keep working through the validator.
