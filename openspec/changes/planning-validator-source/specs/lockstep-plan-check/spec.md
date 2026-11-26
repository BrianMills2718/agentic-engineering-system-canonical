## ADDED Requirements

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
