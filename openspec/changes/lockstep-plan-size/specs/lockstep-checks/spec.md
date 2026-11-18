## ADDED Requirements

### Requirement: Changed: Every plan that names a listed requirement states its size

The changed check SHALL read, in each plan that names a listed requirement, every line `Plan size: small` or `Plan size: full` that stands outside a fenced code block: in the `proposal.md` of an OpenSpec change, or in the page itself for a page in `docs/plans/`. A listed requirement's size SHALL be `full` when any plan naming it says `full`, otherwise `small` when one says `small`. The check SHALL report `no-plan-size` and exit 1 for a listed requirement that a plan names when no plan naming it gives a size, and the finding SHALL name the file the line belongs in. For a requirement whose size is `full` it SHALL report `no-planning-package` and exit 1 unless a plan naming it has, outside a fenced code block, a line `Planning package: <path>` (the path with or without backticks) whose path is a file in the repository. It SHALL print each listed requirement's size in its text block and include it in its JSON output. A requirement reported `unplanned` SHALL get no size finding.

Source: Brian, 2026-11-17: "i approve your reccomendations", answering Decision 7 with its option 7A: "Each plan states its size in one line, small or full. Small: the proposal is the plan, Lockstep's checks are the gate, and the checklist is not run. Full: the whole planning package and checklist, as now. Lockstep prints and counts the declared sizes." (code2-workspace decision 0006, amendment of 2026-11-17; code2-workspace issue 853). Inferred by agent: that a `full` plan must name a planning package file that exists (so that `full` points at something a program can open), that two sizes count as `full`, and the two line forms (the `Plan size:` line `ship` already reads in `docs/plans/` pages, and the `Planning package:` line Company Planning's plan check already requires).

#### Scenario: Changed: A plan marked small passes

- **GIVEN** a requirement that differs from the base, and an OpenSpec change naming it whose `proposal.md` has the line `Plan size: small`
- **WHEN** the check runs
- **THEN** the requirement's block prints the size `small`, there is no size finding, the count line has `small=1`, and it exits 0

#### Scenario: Changed: A plan with no size line fails

- **GIVEN** a requirement that differs from the base, and an OpenSpec change naming it whose `proposal.md` has no `Plan size:` line
- **WHEN** the check runs
- **THEN** it reports `no-plan-size` for the requirement with the path of that `proposal.md`, the count line has `no_plan_size=1`, and it exits 1

#### Scenario: Changed: A size line inside a code block does not count

- **GIVEN** the same change, whose `proposal.md` has the line `Plan size: small` only inside a fenced code block
- **WHEN** the check runs
- **THEN** it reports `no-plan-size` for the requirement and exits 1

#### Scenario: Changed: A full plan that names an existing planning package passes

- **GIVEN** a plan naming the requirement with the lines `Plan size: full` and `Planning package: docs/planning/planning-package.json`, and that file present in the repository
- **WHEN** the check runs
- **THEN** the requirement's block prints the size `full`, there is no size finding, the count line has `full=1`, and it exits 0

#### Scenario: Changed: A full plan with no planning package line fails

- **GIVEN** a plan naming the requirement with the line `Plan size: full` and no `Planning package:` line
- **WHEN** the check runs
- **THEN** it reports `no-planning-package` for the requirement, the count line has `no_planning_package=1`, and it exits 1

#### Scenario: Changed: A full plan naming a planning package that does not exist fails

- **GIVEN** a plan naming the requirement with the lines `Plan size: full` and `Planning package: docs/planning/missing.json`, and no such file in the repository
- **WHEN** the check runs
- **THEN** it reports `no-planning-package` for the requirement, naming the missing path, and exits 1

#### Scenario: Changed: Small in one plan and full in another counts as full

- **GIVEN** two plans naming the requirement, one with `Plan size: small` and one with `Plan size: full` and a `Planning package:` line naming a file that exists
- **WHEN** the check runs
- **THEN** the requirement's size is `full`, and the count line has `small=0` and `full=1`

#### Scenario: Changed: An unplanned requirement gets no size finding

- **GIVEN** a requirement whose statement was edited in `openspec/specs/` since the base, and no change or plan page added or edited since the base
- **WHEN** the check runs
- **THEN** it reports `unplanned` for the requirement and no `no-plan-size`, and the count line has `no_plan_size=0`

## MODIFIED Requirements

### Requirement: Changed: Count line and exit status

The changed check SHALL end with the line `RESULT changed requirements=<n> unplanned=<n> no_scenario=<n> wording_only=<n> small=<n> full=<n> no_plan_size=<n> no_planning_package=<n> exit=<0|1>`, exiting 1 when `unplanned`, `no_scenario`, `no_plan_size` or `no_planning_package` is above zero. `small` and `full` SHALL count the listed requirements of each size. When `<rev>` does not name a commit it SHALL check nothing, print `RESULT changed skipped="base <rev> not found" exit=0` and exit 0. `changed` SHALL be a check name in `lockstep.yaml` with the same `block`, `warn` and `off` modes as the other checks.

Source: inferred by agent (the same count-line, missing-base and mode rules the other Lockstep checks follow; the four size fields count what the plan-size requirement reports)

#### Scenario: Changed: Nothing changed gives a zero count and exit 0

- **GIVEN** a repository whose plan is the same as at the base
- **WHEN** the check runs
- **THEN** its last line is `RESULT changed requirements=0 unplanned=0 no_scenario=0 wording_only=0 small=0 full=0 no_plan_size=0 no_planning_package=0 exit=0`

#### Scenario: Changed: A missing base is reported, not crashed

- **GIVEN** a base revision that does not exist
- **WHEN** the check runs
- **THEN** it prints the skipped line and exits 0

#### Scenario: Changed: Mode off skips the check

- **GIVEN** `lockstep.yaml` with `checks: {changed: off}`
- **WHEN** `lockstep check changed` runs
- **THEN** it prints `skipped (off)` and exits 0
