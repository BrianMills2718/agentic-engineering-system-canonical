# lockstep-plan-check Specification

## Purpose

`lockstep plan check` checks a repository's plan by running Company Planning's `validate_planning_package.py`, the one plan checker `ship` also runs, and adds Lockstep's own work-unit DAG check (`lockstep plan units`). Lockstep holds no copy of the validator's checks (`openspec/changes/archive/2026-11-25-one-plan-checker/proposal.md`).

## Requirements

### Requirement: Work units form a checked DAG

`lockstep plan units` SHALL read `docs/planning/work-units.json` (record type `work_units`, a list `units`) and exit 1, naming each problem, unless: each unit has a unique `id`, a `title`, a `depends_on` list of existing unit ids (empty means it can start now), a `touches` list of repository paths, and a `status` of `planned`, `in progress` or `merged`; a `merged` unit has `evidence`; and the dependencies contain no cycle. It SHALL print the units that are ready (not merged, every dependency merged), the longest chain of unmerged units, and each pair of unmerged units with no dependency path between them whose `touches` overlap (paths are compared as exact strings, so a directory and a file inside it do not overlap). It exits 2 when the file is missing or not JSON. `lockstep plan check` SHALL report the same problems when the file is present.

Source: Brian, 2026-11-14: "we should always have a dag as part of the plans so we can optimally parallelize and stay on track"; approved with "i apporve your recs".

#### Scenario: Independent units are both ready

- **GIVEN** units A and B with empty `depends_on` and different `touches`
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 0 and lists both as ready

#### Scenario: A cycle fails

- **GIVEN** unit A depending on B and B depending on A
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 1 and names the cycle

#### Scenario: A dependency on a missing unit fails

- **GIVEN** a unit whose `depends_on` names an id no unit has
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 1 and names the unit and the missing id

#### Scenario: Independent units touching one file are flagged

- **GIVEN** unmerged units A and B with no dependency path between them that both touch `src/x.py`
- **WHEN** `lockstep plan units` runs
- **THEN** it reports the conflict naming both units and the file

#### Scenario: A merged unit needs evidence

- **GIVEN** a `merged` unit without `evidence`
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 1 naming the unit

### Requirement: `lockstep plan check` runs Company Planning's validator

`lockstep plan check` SHALL accept `--repo PATH` (default the current directory) and `--json`. It SHALL run Company
Planning's `validate_planning_package.py` on `docs/planning/planning-package.json` under the repository, fetched from
origin/main of Company Planning and run by the same function and interpreter choice `ship` uses (so
`SHIP_PLANNING_VALIDATOR`, `SHIP_COMPANY_PLANNING` and `SHIP_VALIDATOR_PYTHON` work the same), print the validator's
output, and exit with the validator's exit status, except that, as in `ship`, a package that fails only the freshness
check (it passes with `--no-freshness`) exits 0 with a warning. When `docs/planning/work-units.json` exists it SHALL also report the
work-unit problems and exit 1 when there are any. It SHALL exit 2, saying why, when the repository has no planning
package or the validator cannot be fetched or run, or exits with a status other than 0 or 1. With `--json` it SHALL print one object with `ok`, the validator's
exit status and output, and the work-unit problems. Lockstep SHALL hold no copy of the validator's checks.

Source: Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 5: "`lockstep plan check` validates it"); one plan checker approved by Brian, 2026-11-25: "ia prpove yourr ecommednations though" (Company Planning's validator kept as that checker: inferred by agent, `openspec/changes/archive/*-one-plan-checker/proposal.md`).

#### Scenario: The validator's verdict is the command's verdict

- **GIVEN** a repository with a planning package and a validator that exits 1
- **WHEN** `lockstep plan check` runs
- **THEN** it prints the validator's output and exits 1; with a validator that exits 0 it exits 0

#### Scenario: A package out of date only by freshness passes with a warning

- **GIVEN** a validator that exits 1, and 0 with `--no-freshness`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 0 and prints a warning that the package is out of date

#### Scenario: A repository with no planning package cannot be checked

- **GIVEN** a repository without `docs/planning/planning-package.json`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 2 and names the missing package

#### Scenario: Work-unit problems are added

- **GIVEN** a planning package the validator passes and a work-units file with a unit depending on a missing unit
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and names the work-unit problem
