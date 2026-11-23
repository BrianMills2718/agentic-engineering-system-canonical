# lockstep-projection Specification

## Purpose

Lockstep's projection of requirement text into docstrings and coverage into plans and `docs/status.md` (`lockstep check project`), the status report (`lockstep status`), `lockstep show FILE` and the pytest plugin that registers the `req` marker, ported from code2check (`proposals/one-planning-tool/DESIGN.md`, slice 6).

## Requirements

### Requirement: Requirement text is written into the implementing docstring

`lockstep check project` SHALL write the text of each requirement a docstring implements, word for word, in a marked block under its `Implements:` line, and `lockstep check project --check` SHALL fail when a block differs from the spec, writing nothing. It SHALL print one `rewrote <path>` line per file it rewrote. It SHALL preserve unrelated Python source and remain idempotent. In a repository with a layout plan it SHALL also rewrite each planned file's cog plan copy from the plan, SHALL write no block inside that copy, and SHALL do both even when no requirement statement text was read.

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

#### Scenario: A planned file's plan copy follows a reworded requirement

- **GIVEN** a layout repository whose planned file's cog plan copy is current, and its requirement is then reworded
- **WHEN** the edit hook judges the file, then `project` runs, then runs again
- **THEN** the hook finds it stale, `project` rewrites the copy with the new wording and no generated block inside it, and the second run changes nothing

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

`lockstep check project` SHALL write `docs/status.md` in a repository with a `docs/` folder and recognized OpenSpec requirements, listing every requirement and scenario with the state `lockstep status` gives when no test run is recorded, and `--check` SHALL fail when the page is stale, except that when git ignores `docs/status.md` the page is build output and `--check` SHALL not report it.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows). Inferred by agent, 2026-11-21 (code2-template#37, clean-home milestone run): an ignored page is build output, so parallel plans do not conflict on it

#### Scenario: Status page lists every requirement with its coverage state

- **GIVEN** a repository with `docs/`
- **WHEN** `project` runs
- **THEN** `docs/status.md` lists every requirement and scenario with its state

#### Scenario: Stale status page fails the check

- **GIVEN** a test is added after the page was written
- **WHEN** `project --check` runs
- **THEN** it names `docs/status.md`

#### Scenario: An ignored status page is not reported stale

- **GIVEN** a repository whose `.gitignore` lists `docs/status.md`, and a test added after the page was written
- **WHEN** `project --check` runs
- **THEN** it does not name `docs/status.md`, and `project` still rewrites the page

### Requirement: Status links each requirement to its code and tests

`lockstep status` SHALL list, for each requirement, the symbols whose docstrings implement it with each symbol's `file:line`, and for each scenario, the tests marked with its ID, recomputed from the repository on every run, as a table, as JSON (`--json`) or as the Markdown page (`--md`). `lockstep check project` SHALL write `docs/links.json` in a repository with a `docs/` folder and recognized OpenSpec requirements: a `version` and a list of `nodes`, each with `id`, `type` (`capability`, `requirement`, `scenario`, `test`, `file`, `symbol`, `plan`, `quote` or `decision`), `title`, `file`, `line` and `links` (the IDs of the nodes it points to: capability to its requirements, requirement to its scenarios and implementing symbols, scenario to its tests, symbol and test to their file, plan to the IDs on its `Closes:` line, quote to the ID in its `lockstep quote` marker, decision to the files, folders, requirements and capabilities its `Governs:` line names), and `--check` SHALL not report the file when git ignores it. A `plan` node SHALL be written for each plan in `docs/plans/` and each active or archived OpenSpec change proposal with a `Closes:` line, with `state` `active` or `archived`; a `quote` node, with ID `<file>:<line>`, for each quote marker, with `state` from the trace check; an ID either names that no node has SHALL be listed in its `unknown` field, not in `links`. Each requirement node SHALL carry `source`, the text of its `Source:` line, and `source_kind`, as the sources check classifies it. A `decision` node, with ID `decision/<file stem>`, SHALL be written for each record in `docs/decisions/`, with `status`, `superseded_by`, `source`, `source_kind` and `governs` (every `Governs:` target as written); a path target SHALL also be a `file` node.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

Source: Brian, 2026-11-23: "isnt there like a file that has how everythign is linked to everythign else like how capabilities link to fils link to successc riteria"; plan docs/planning/linked-chain-core-2026-11-23.md

Source: Brian, 2026-11-23: "i approve" (decision -> requirement or code links that the hook hands over, read from lines that already exist); plan docs/planning/links-existing-lines-2026-11-23.md

#### Scenario: Status lists implementers and tests

- **GIVEN** a requirement with an implementer and a marked test
- **WHEN** `lockstep status` runs
- **THEN** both appear, and a RESULT line ends the output

#### Scenario: The link file lists the whole chain

- **GIVEN** a requirement with an implementing function and a scenario with a marked test
- **WHEN** `lockstep check project` runs
- **THEN** `docs/links.json` holds the capability, requirement, scenario, test, symbol and both files as nodes, linked capability to requirement to scenario to test, and requirement to symbol to file with its line

Source: Brian, 2026-11-23: "i approve" (reading the existing `Closes:`, `Source:` and quote lines into `links.json`); plan docs/planning/links-existing-lines-2026-11-23.md

#### Scenario: The link file reads plans, sources and quotes

- **GIVEN** a plan and an archived change proposal with `Closes:` lines, a document with a quote marker, and a requirement with a `Source:` line
- **WHEN** `lockstep check project` runs
- **THEN** `docs/links.json` has an active and an archived `plan` node and a `quote` node linking to the IDs they name, and the requirement node carries its source and its source kind

#### Scenario: The link file lists decisions and what they govern

- **GIVEN** decision records with `Governs:` lines naming a file, a folder, a capability and a rule ID, one of them superseded
- **WHEN** `lockstep check project` runs
- **THEN** `docs/links.json` has a `decision` node for each, linking to the file, folder and capability nodes, with its status, successor, source and every target as written

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

`lockstep status` SHALL read the `Closes:` line of each plan and OpenSpec change and report each listed ID that is unimplemented, untested or not passing as open for that plan. It SHALL give a requirement or scenario the state `changed, not archived` when an active change's spec delta holds text for it that differs from the spec's (runs of whitespace counting as one space), whatever its tests' results, and SHALL report it as open for a plan that lists it.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows). The `changed, not archived` state: Brian, 2026-11-17: "if there is a change in the nromative docuemtnation then ... the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842); its name and rule are inferred by agent.

#### Scenario: Open ids of a plan are listed

- **GIVEN** a plan closing an ID that fails and an ID that does not exist
- **WHEN** `lockstep status` runs
- **THEN** both are listed as open with their state

#### Scenario: A requirement reworded in an active change is open, not passing

- **GIVEN** a requirement with an implementer and a passing test, and an active change whose spec delta gives it a different statement and whose proposal lists it on its `Closes:` line
- **WHEN** `lockstep status` runs
- **THEN** the requirement's state is `changed, not archived` and the plan lists it as open

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

### Requirement: Links show planned files and exports

In a repository whose `lockstep.yaml` has `layout:` rows, `docs/links.json` SHALL hold a `file` node for each row's path and a `symbol` node for each declared export, each with `state` `planned` when the file (or, for an export, the top-level function or class of that name in the file) does not exist yet and `exists` when it does. A row's `file` node SHALL link to the requirements the row implements and to its test files; an export's `symbol` node, with ID the file's module path and the export name, SHALL link to the file. An implementer found in a comment line (no Python symbol) SHALL link its requirement to the `file` node directly.

Source: Brian, 2026-11-23: "i approve", item (c) of `docs/planning/back-on-design-2026-11-23.md`; `docs/architecture/LOCKSTEP.md:23-26` (requirement, file and symbol are one chain); plan `docs/planning/template-layout-2026-11-23.md`, step 4.

#### Scenario: A planned file that does not exist yet is shown as planned

- **GIVEN** a layout row for `src/pkg/new.py` implementing `core/do-the-thing`, with tests `tests/test_new.py` and export `make() -> int`, and no such file
- **WHEN** the links are built
- **THEN** node `src/pkg/new.py` has type `file`, state `planned` and links to `core/do-the-thing` and `tests/test_new.py`, and node `pkg.new.make` has type `symbol`, state `planned` and links to `src/pkg/new.py`

#### Scenario: A laid-out file with its export is shown as existing

- **GIVEN** the same row and `src/pkg/new.py` defining `def make() -> int`
- **WHEN** the links are built
- **THEN** both nodes have state `exists`
