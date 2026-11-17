## ADDED Requirements

### Requirement: Changed and test-first: The base is where the branch started

`lockstep check changed --base <rev>` and `lockstep check test-first --base <rev>` SHALL compare the current revision with the merge base of `<rev>` and the current commit, so that what was merged into `<rev>` after the branch started is not counted as this branch's change. When `<rev>` and the current commit share no history, or the repository has no commit yet, they SHALL compare with `<rev>` itself.

Source: inferred by agent, from the first run of the changed check on a branch behind `origin/main` (2026-11-17): four requirements merged there after the branch started were listed as removed and unplanned.

#### Scenario: Changed: A requirement added on the base branch after the branch started is not listed

- **GIVEN** a branch that changed no requirement, and a requirement added on `main` after the branch started
- **WHEN** `lockstep check changed --base main` runs on the branch
- **THEN** it lists no requirement and exits 0

#### Scenario: Test-first: A scenario reworded on the base branch after the branch started is not checked

- **GIVEN** a branch that changed no scenario, and a scenario reworded on `main` after the branch started
- **WHEN** `lockstep check test-first --base main` runs on the branch
- **THEN** it checks no changed scenario and exits 0
