## ADDED Requirements

### Requirement: Add-on gates switch off from the copier answers

`scripts/ship.py` SHALL read the keys `ship_planning_gate` and `ship_one_page_plans` from `.copier-answers.yml` on the default branch at `origin` (never from the branch being shipped, so a branch cannot turn its own gate off), reading each as a top-level `key: value` line. When a key's value is `false` (any letter case), ship SHALL skip that gate (the whole planning gate with its plan-repair and upkeep exceptions, or the one-page-plan check) and print and log `ship: planning gate: off (.copier-answers.yml ship_planning_gate: false)` or `ship: one-page plans: off (.copier-answers.yml ship_one_page_plans: false)`. A missing file, a missing key or any other value SHALL leave the gate on. The prior-art check is core and has no switch.

Source: Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable. we shoudl start with the minimal core than add on other things as needed after the first minimal core milestone". The copier answers file as the one switch, and these two gates as add-ons, inferred by agent in docs/planning/minimal-core-2026-11-20.md sections 5 and 7.

#### Scenario: The planning gate is switched off

- **GIVEN** a new repository with no planning package whose `.copier-answers.yml` says `ship_planning_gate: false`
- **WHEN** ship runs with a passing check
- **THEN** it merges and prints `ship: planning gate: off (.copier-answers.yml ship_planning_gate: false)`

#### Scenario: The one-page-plan check is switched off

- **GIVEN** a branch adding an incomplete one-page plan, in a repository whose `.copier-answers.yml` says `ship_one_page_plans: false`
- **WHEN** ship runs with a passing check
- **THEN** it merges

#### Scenario: No answers file keeps every gate on

- **GIVEN** a new repository with no planning package and no `.copier-answers.yml` on the default branch, or one that only the branch being shipped adds
- **WHEN** ship runs
- **THEN** it is refused as before

### Requirement: Refuse a branch whose hidden acceptance run failed or is out of date

After it has caught up with the default branch and before it runs the check, `scripts/ship.py` SHALL read every readable `summary.json` under `${XDG_STATE_HOME:-~/.local/state}/lockstep-runs/<repository>/` (the main checkout's folder name) whose `branch` is the branch being shipped or whose `head` is a commit reachable from HEAD and not from the default branch; an unreadable one SHALL be skipped with a printed warning. When there is at least one, ship SHALL refuse the merge with nothing pushed, naming `lockstep accept check <change>` as the way to record a new run, unless the newest by run id has `accept.exit` 0, `uncommitted` 0, and `head` equal to HEAD as it will be merged (so a branch that was rebased must be checked again). With none, ship SHALL print and log `ship: no hidden-test run recorded for this branch` and go on; a run made by another user or under another `XDG_STATE_HOME` is not found, which this message makes visible.

Source: minimal-core-2026-11-20.md section 6 step 2, hidden tests "must pass before `ship`" (inferred by agent from the 2026-11-20 plan-fidelity test, where they were the check that measured success), under Brian, 2026-11-20: "the goal is to give a well specified plan to an agent on some proejct nad have it faithfulyy and successfully impelemnt it".

#### Scenario: A passing record at HEAD merges

- **GIVEN** a run record for the branch with `accept.exit` 0, `uncommitted` 0 and `head` equal to HEAD
- **WHEN** ship runs with a passing check
- **THEN** it merges

#### Scenario: A failing or out-of-date record is refused

- **GIVEN** a run record for the branch whose hidden tests failed or did not run, or whose `head` is another commit, or which counted uncommitted files
- **WHEN** ship runs
- **THEN** it exits 1, names `lockstep accept check`, and the branch is not on the remote

#### Scenario: No record goes on

- **GIVEN** no run record for the branch
- **WHEN** ship runs with a passing check
- **THEN** it merges and prints `ship: no hidden-test run recorded for this branch`
