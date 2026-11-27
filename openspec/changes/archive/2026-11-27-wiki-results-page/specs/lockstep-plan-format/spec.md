## ADDED Requirements

### Requirement: A generated wiki shows test results at this checkout

In a layout repository whose `lockstep.yaml` says `generated_wiki: true` and whose git ignores `generated/wiki/results.md`, `lockstep check project` SHALL write that page with every requirement and scenario and the state `lockstep status` gives them (passing, failing, skipped, not run at this revision, untested, unimplemented), a line naming the commit the test results are from or why no results were used, and each plan or change whose `Closes:` IDs are not all passing with those IDs. `--check` SHALL NOT report the page and a run SHALL NOT remove it. When git does not ignore the path the page SHALL NOT be written. The committed index SHALL name the page on one line without linking to it.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 2 ("tests pass at <commit>" written back) and decision 12 (results kept outside git, shown when regenerated); told the agent to proceed without waiting. The page path, the ignore condition and the plan section are inferred by agent: a committed page holding results would make itself stale.

#### Scenario: Results at this commit show on the page

- **GIVEN** a layout repository with `generated_wiki: true`, the results page ignored by git, and test results recorded at HEAD on a clean tree
- **WHEN** `lockstep check project` runs
- **THEN** `generated/wiki/results.md` names that commit and shows a passing scenario as passing and a failing one as failing, and lists the plan that closes the failing ID

#### Scenario: Results from another commit are not used

- **GIVEN** the same repository with results recorded at an older commit
- **WHEN** `lockstep check project` runs
- **THEN** the page says the results are from the older commit and shows the tested scenarios as not run at this revision

#### Scenario: The page is build output

- **GIVEN** the same repository after `lockstep check project` wrote the page
- **WHEN** the results change and `lockstep check project --check` runs
- **THEN** it does not name `generated/wiki/results.md`, and a run of `lockstep check project` keeps the page; without the ignore entry no page is written
