## ADDED Requirements

### Requirement: Arch: Code imports match the diagram

`lockstep check arch check`, when the committed contracts file matches the diagram, SHALL run the contracts against the code with import-linter and exit 1 when any contract is broken, printing the broken contract and the importing module. When import-linter is not installed it SHALL print that and exit 1; it SHALL NOT pass.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md); acceptance entries A2 and A3 in docs/planning/acceptance-criteria.json

#### Scenario: Arch: An import the diagram forbids is refused

- **GIVEN** a current contracts file forbidding `app.detect` to import `app.cli`
- **WHEN** `app.detect` imports `app.cli` and the check runs
- **THEN** the check exits 1 and its output names the broken contract and `app.detect`

#### Scenario: Arch: Missing import-linter fails loudly

- **GIVEN** a current contracts file and no `lint-imports` command
- **WHEN** the check runs
- **THEN** it prints that import-linter is not installed and exits 1

### Requirement: Test-first: A test run that cannot start fails the check

`lockstep check test-first` SHALL exit 1 with a message saying pytest could not run when running the new tests on the base source produces no test report (pytest missing from Lockstep's environment, or a usage error); it SHALL NOT report the tests as not passing before.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md); acceptance entries A2 and A3 in docs/planning/acceptance-criteria.json

#### Scenario: Test-first: Pytest that cannot run fails loudly

- **GIVEN** a new scenario with a marked test and a Python that cannot run pytest
- **WHEN** the check runs
- **THEN** it prints "pytest could not run" and exits 1
