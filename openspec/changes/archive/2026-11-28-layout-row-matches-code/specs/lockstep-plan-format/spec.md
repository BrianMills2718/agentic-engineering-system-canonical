## ADDED Requirements

### Requirement: A layout row lists what its file implements

Lockstep SHALL report, as a layout problem, a layout row whose file names in an `Implements:` line a requirement
that the row's `implements` list leaves out, naming the row's path and each missing requirement ID, so that the plan
always names every requirement its code says it implements.

Source: Brian, 2026-11-27 18:50: "The plan row (5) is empty: implements: [], tests: []. Here the link runs only
through the docstring and the test marker, not through the plan. So the plan file can't tell you which requirements
this file is meant to cover." The check form (report the contradiction, not every empty row) is inferred by agent from
the 2026-11-28 measurement: 0 contradictions in a fresh template copy, 37 files in AES.

#### Scenario: A row that leaves out its file's requirement is reported

- **GIVEN** a laid-out file whose docstring says `Implements: greeting/greet-by-name` and whose row has `implements: []`
- **WHEN** the layout is checked, and `lockstep check` runs on the committed tree
- **THEN** the problem names the row's path and `greeting/greet-by-name`, and the check blocks; with the ID restored, neither reports it
