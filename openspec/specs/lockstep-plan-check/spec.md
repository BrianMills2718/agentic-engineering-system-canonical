# lockstep-plan-check Specification

## Purpose

`lockstep plan check` checks a repository's plan by running Company Planning's `validate_planning_package.py`, the one plan checker `ship` also runs, and adds Lockstep's own work-unit DAG check (`lockstep plan units`). Lockstep holds no copy of the validator's checks (the archived one-plan-checker proposal, restored by `docs/retired/2026-11-25.md`).

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

Source: Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 5: "`lockstep plan check` validates it"); one plan checker approved by Brian, 2026-11-25: "ia prpove yourr ecommednations though" (Company Planning's validator kept as that checker: inferred by agent, the archived one-plan-checker proposal, restored by `docs/retired/2026-11-25.md`).

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

### Requirement: The validator's source is set in lockstep.yaml

`ship` and `lockstep plan check` SHALL take Company Planning's validator from the first of: `SHIP_PLANNING_VALIDATOR`
(a file, used as given); `SHIP_COMPANY_PLANNING` (a local Company Planning checkout, read at `origin/<ref>`);
`planning.validator.repo` in `lockstep.yaml` on the repository's default branch at `origin` (an address git can clone,
kept as a bare clone under `$XDG_CACHE_HOME/lockstep/`, default `~/.cache/lockstep/`, in a folder named by a hash of
the address, cloned or fetched under a file lock with `GIT_TERMINAL_PROMPT=0`, ssh `BatchMode=yes` and a 300-second
timeout, and read at `<ref>`); else `~/code2/company-planning` read at `origin/<ref>`. `planning.validator.ref` SHALL
name a branch, `main` when absent. Each run SHALL print and log the line `ship: planning validator: <source>` naming
the source that won and why, and SHALL print and log a warning when an environment variable overrides a configured
repository. A `planning.validator` that is not a mapping of a text `repo` and an optional text `ref` SHALL refuse with
a configuration error naming the setting. A clone or fetch that fails or times out SHALL be reported as the validator
not fetchable, naming the address. Credentials SHALL come only from the user's own git setup, never from
`lockstep.yaml`.

Source: Brian, 2026-11-25: "the whole systm should be configurable so you can congfigure what is on or off or any other settings. for any piece." Inferred by agent: the order of sources, the cache, the default branch `main` and the log line (`docs/planning/next.goal.md`, slice 2).

#### Scenario: A configured repository is the source

- **GIVEN** `lockstep.yaml` on the default branch naming `planning.validator.repo`, and neither environment variable set
- **WHEN** `lockstep plan check` runs
- **THEN** the validator from that repository runs, and the output names that repository as the source

#### Scenario: An environment variable overrides a configured repository with a warning

- **GIVEN** a configured repository and `SHIP_COMPANY_PLANNING` set
- **WHEN** `lockstep plan check` runs
- **THEN** the validator from `SHIP_COMPANY_PLANNING` runs and a warning names the configured repository it overrode

#### Scenario: The ref picks the branch

- **GIVEN** a configured repository whose `release` branch holds a different validator, and `ref: release`
- **WHEN** `lockstep plan check` runs
- **THEN** the validator from the `release` branch runs

#### Scenario: An unreachable configured repository cannot be fetched

- **GIVEN** a configured repository address that does not exist
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 2 and names the address it could not fetch

#### Scenario: A bad validator setting is a configuration error

- **GIVEN** `planning.validator` set to a text instead of a mapping
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 2 and names `planning.validator`

### Requirement: The validator can use an installed graph schema

When the operator sets a nonempty `SHIP_TYPED_GRAPH_SCHEMA`, both `ship` and `lockstep plan check` SHALL pass that local path as the value of the Company Planning validator's `--typed-graph-schema` option for the initial check and any freshness retry. An unset or empty variable SHALL leave the option absent so that the selected validator uses its own default. The validator SHALL continue to judge the graph.

Source: Brian, 2026-11-27, AES clean Linux validator goal. Inferred by agent: reuse the upstream CLI option and the existing trusted shell settings for validator dependencies.

#### Scenario: Both validator entry points use the installed graph schema

- **GIVEN** an operator-provisioned schema whose path contains a space and a real package due for a fresh review
- **WHEN** either command runs the validator and retries without the freshness check
- **THEN** both invocations receive the same schema path as one argument
