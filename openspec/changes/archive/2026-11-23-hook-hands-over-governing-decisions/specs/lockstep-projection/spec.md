## MODIFIED Requirements

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
