# lockstep-projection Specification

## Purpose

Lockstep's projection of requirement text into docstrings and coverage into plans and `docs/status.md` (`lockstep check project`), the status report (`lockstep status`), `lockstep show FILE` and the pytest plugin that registers the `req` marker, ported from code2check (`proposals/one-planning-tool/DESIGN.md`, slice 6).

## Requirements

### Requirement: Requirement text is written into the implementing docstring

`lockstep check project` SHALL write the text of each requirement a docstring implements, word for word, in a marked block under its `Implements:` line, and `lockstep check project --check` SHALL fail when a block differs from the spec, writing nothing. It SHALL print one `rewrote <path>` line per file it rewrote. It SHALL preserve unrelated Python source and remain idempotent.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Opening quote line declarations receive canonical text

- **GIVEN** a docstring whose `Implements:` content starts on the opening quote line
- **WHEN** `project` runs
- **THEN** the text is written under it, other source is unchanged, and a second run changes nothing

#### Scenario: Projection rewrites the block

- **GIVEN** a spec requirement is reworded after its block was written
- **WHEN** `project` runs
- **THEN** the block holds the new wording once

#### Scenario: Stale requirement text fails the check

- **GIVEN** a block differs from the spec
- **WHEN** `project --check` runs
- **THEN** it exits 1, names the file and writes nothing

### Requirement: Status flows back into the plan

`lockstep check project` SHALL write a generated status block into each plan that has a `Closes:` line, listing each ID with its implementers and tests, and `--check` SHALL fail when the block is stale. A block written by code2check SHALL be replaced, not left beside the new one.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Plan block lists coverage

- **GIVEN** a plan with a `Closes:` line
- **WHEN** `project` runs
- **THEN** a block after the `Closes:` paragraph lists each ID's implementers and tests

#### Scenario: A plan block written by code2check is replaced not duplicated

- **GIVEN** a plan holds a code2check status block
- **WHEN** `project` runs
- **THEN** one lockstep block remains and no code2check marker

### Requirement: The docs site shows coverage at its commit

`lockstep check project` SHALL write `docs/status.md` in a repository with a `docs/` folder and recognized OpenSpec requirements, listing every requirement and scenario with the state `lockstep status` gives when no test run is recorded, and `--check` SHALL fail when the page is stale.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Status page lists every requirement with its coverage state

- **GIVEN** a repository with `docs/`
- **WHEN** `project` runs
- **THEN** `docs/status.md` lists every requirement and scenario with its state

#### Scenario: Stale status page fails the check

- **GIVEN** a test is added after the page was written
- **WHEN** `project --check` runs
- **THEN** it names `docs/status.md`

### Requirement: Status links each requirement to its code and tests

`lockstep status` SHALL list, for each requirement, the symbols whose docstrings implement it, and for each scenario, the tests marked with its ID, recomputed from the repository on every run, as a table, as JSON (`--json`) or as the Markdown page (`--md`).

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Status lists implementers and tests

- **GIVEN** a requirement with an implementer and a marked test
- **WHEN** `lockstep status` runs
- **THEN** both appear, and a RESULT line ends the output

### Requirement: Status reads test results from this revision

`lockstep status` SHALL mark a scenario passing, failing or skipped only from a test-result file recorded at the current commit with a clean tree, and SHALL mark it `not run at this revision` otherwise.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Results from this revision set pass and fail

- **GIVEN** results recorded at HEAD on a clean tree
- **WHEN** `lockstep status` runs
- **THEN** scenarios are passing or failing as recorded

#### Scenario: Results from another revision are not used

- **GIVEN** results recorded at an older commit
- **WHEN** `lockstep status` runs
- **THEN** scenarios are `not run at this revision`

### Requirement: A plan closes requirement ids only when they pass

`lockstep status` SHALL read the `Closes:` line of each plan and OpenSpec change and report each listed ID that is unimplemented, untested or not passing as open for that plan.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Open ids of a plan are listed

- **GIVEN** a plan closing an ID that fails and an ID that does not exist
- **WHEN** `lockstep status` runs
- **THEN** both are listed as open with their state

### Requirement: Show prints what a file must keep true

`lockstep show FILE` SHALL print each requirement the file's docstrings implement, with its text, its scenarios and their status.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Show lists a file's requirements

- **GIVEN** a file implementing one requirement
- **WHEN** `lockstep show FILE` runs
- **THEN** the requirement, its text, its scenarios and states print

### Requirement: The pytest plugin ships as a pytest11 entry point

Installing Lockstep SHALL register the `req` marker with pytest through a `pytest11` entry point (`lockstep.checks.plugin`), and registering it SHALL stay compatible with a project that also declares `req` in its own pytest configuration.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: The plugin registers the req marker

- **GIVEN** Lockstep is installed
- **WHEN** pytest starts with `--strict-markers`
- **THEN** tests marked `req` run, with or without the project's own declaration

### Requirement: Project, status and show are Lockstep commands

`lockstep check project`, `lockstep status` and `lockstep show` SHALL be commands of the one `lockstep` tool; `project` SHALL take its mode (block, warn or off) from `lockstep.yaml` like the other checks, and SHALL read source and test folders from `[tool.lockstep]` in `pyproject.toml`, else from `[tool.code2check]`.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: The commands are top-level and check modes apply

- **GIVEN** a repository with a stale docstring block
- **WHEN** `lockstep check project --check` runs with mode block, warn or off
- **THEN** it exits 1, exits 0 with a warning, or skips
