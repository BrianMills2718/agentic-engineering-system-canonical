## MODIFIED Requirements

### Requirement: Status links each requirement to its code and tests

`lockstep status` SHALL list, for each requirement, the symbols whose docstrings implement it with each symbol's `file:line`, and for each scenario, the tests marked with its ID, recomputed from the repository on every run, as a table, as JSON (`--json`) or as the Markdown page (`--md`). `lockstep check project` SHALL write `docs/links.json` in a repository with a `docs/` folder and recognized OpenSpec requirements: a `version` and a list of `nodes`, each with `id`, `type` (`capability`, `requirement`, `scenario`, `test`, `file` or `symbol`), `title`, `file`, `line` and `links` (the IDs of the nodes it points to: capability to its requirements, requirement to its scenarios and implementing symbols, scenario to its tests, symbol and test to their file), and `--check` SHALL not report the file when git ignores it.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

Source: Brian, 2026-11-23: "isnt there like a file that has how everythign is linked to everythign else like how capabilities link to fils link to successc riteria"; plan docs/planning/linked-chain-core-2026-11-23.md

#### Scenario: Status lists implementers and tests

- **GIVEN** a requirement with an implementer and a marked test
- **WHEN** `lockstep status` runs
- **THEN** both appear, and a RESULT line ends the output

#### Scenario: The link file lists the whole chain

- **GIVEN** a requirement with an implementing function and a scenario with a marked test
- **WHEN** `lockstep check project` runs
- **THEN** `docs/links.json` holds the capability, requirement, scenario, test, symbol and both files as nodes, linked capability to requirement to scenario to test, and requirement to symbol to file with its line
