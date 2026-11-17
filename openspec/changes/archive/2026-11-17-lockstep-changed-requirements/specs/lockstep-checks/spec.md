## ADDED Requirements

### Requirement: Changed: Requirements that differ from the base are listed with their code and tests

`lockstep check changed --base <rev>` SHALL compare the text of every requirement and scenario in the plan at the current revision (`openspec/specs/` with the spec deltas of active changes applied over it) with the plan at the base revision, treating runs of whitespace as one space. It SHALL print, for each requirement that is new, removed, or whose statement or any scenario is new, removed or different: the requirement ID and its kind (`new`, `changed` or `removed`), which parts differ, the symbols whose docstrings implement it, the tests marked for its scenarios, each labelled `changed`, `unchanged` or `new` against the base revision's copy of that test function, and the plan that names it. `--json` SHALL print the same as JSON. It SHALL read the base revision from git without changing the working tree.

Source: Brian, 2026-11-17: "if there is a change in the nromative docuemtnation then that normative docuemtnation gets updated and then the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842; approved for build 2026-11-17, "i approve"). The output columns are inferred by agent.

#### Scenario: Changed: A reworded requirement is listed with its implementer and tests

- **GIVEN** a requirement whose statement differs from the base, with an implementing docstring and a marked test that is the same as at the base
- **WHEN** `lockstep check changed --base <rev>` runs
- **THEN** it lists the requirement as `changed`, names the implementing symbol, and labels the test `unchanged`

#### Scenario: Changed: Re-wrapped text is not a change

- **GIVEN** a requirement whose statement differs from the base only in line breaks and spacing
- **WHEN** the check runs
- **THEN** it lists nothing and exits 0

#### Scenario: Changed: A changed scenario marks its requirement changed

- **GIVEN** a requirement whose statement is the same as at the base and one of whose scenarios has different text
- **WHEN** the check runs
- **THEN** it lists the requirement as `changed` and names that scenario as the part that differs

#### Scenario: Changed: Text in an active change counts before it is archived

- **GIVEN** an active change whose spec delta gives an existing requirement a different statement
- **WHEN** the check runs
- **THEN** it lists the requirement as `changed` and names the change as its plan

#### Scenario: Changed: A test edited since the base is labelled changed

- **GIVEN** a changed requirement whose marked test function differs from the base revision's copy
- **WHEN** the check runs
- **THEN** the test is labelled `changed`

### Requirement: Changed: Every listed requirement is named by a plan in the same change set

The changed check SHALL report a listed requirement as `unplanned` and exit 1 when no plan that is new or different from the base revision names it. A plan names a requirement when it is an OpenSpec change (active, or archived since the base) whose spec delta has a heading for that requirement, or a page in `docs/plans/` or an OpenSpec change's `proposal.md` whose `Closes:` or `Wording-only:` line lists the requirement ID.

Source: Brian, 2026-11-17: "the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842; approved for build 2026-11-17, "i approve"). Which files count as a plan is inferred by agent (the two places `lockstep status` already reads a `Closes:` line from).

#### Scenario: Changed: A spec edited with no plan is unplanned

- **GIVEN** a requirement whose statement was edited in `openspec/specs/` since the base, and no change or plan page added or edited since the base
- **WHEN** the check runs
- **THEN** it reports the requirement as `unplanned` and exits 1

#### Scenario: Changed: An archived change in the same change set is its plan

- **GIVEN** a requirement whose statement differs from the base, and a change archived since the base whose spec delta has a heading for it
- **WHEN** the check runs
- **THEN** it names the archived change as the plan and reports no `unplanned` finding

#### Scenario: Changed: A plan page that was not touched does not count

- **GIVEN** a requirement whose statement differs from the base, and a page in `docs/plans/` with a `Closes:` line for it that is identical at the base
- **WHEN** the check runs
- **THEN** it reports the requirement as `unplanned`

### Requirement: Changed: A changed statement needs a changed scenario or a wording-only declaration

The changed check SHALL report `no-scenario-changed` and exit 1 when a requirement's statement differs from the base while none of its scenarios is new or different, unless a plan that is new or different from the base lists the requirement ID on a `Wording-only:` line. It SHALL print each wording-only declaration it accepted with the plan's path, and count them in its count line. A `Wording-only:` line MAY list scenario IDs as well as requirement IDs; a requirement ID covers its statement and all its scenarios.

Source: inferred by agent (a statement that changes while every scenario stays the same leaves nothing to test the change; the declaration is the one typed statement in the design and is printed so it can be read. Follows code2-workspace decision 0006, "a gap closes only through new evidence").

#### Scenario: Changed: A statement changed with no scenario changed fails

- **GIVEN** a requirement, named by a plan in the same change set, whose statement differs from the base and whose scenarios are all the same
- **WHEN** the check runs
- **THEN** it reports `no-scenario-changed` for the requirement and exits 1

#### Scenario: Changed: A wording-only declaration is accepted and printed

- **GIVEN** the same requirement, and a plan in the same change set with the line `Wording-only: <requirement id>`
- **WHEN** the check runs
- **THEN** it exits 0, prints the declaration with the plan's path, and its count line has `wording_only=1`

### Requirement: Changed: Count line and exit status

The changed check SHALL end with the line `RESULT changed requirements=<n> unplanned=<n> no_scenario=<n> wording_only=<n> exit=<0|1>`, exiting 1 when `unplanned` or `no_scenario` is above zero. When `<rev>` does not name a commit it SHALL check nothing, print `RESULT changed skipped="base <rev> not found" exit=0` and exit 0. `changed` SHALL be a check name in `lockstep.yaml` with the same `block`, `warn` and `off` modes as the other checks.

Source: inferred by agent (the same count-line, missing-base and mode rules the other Lockstep checks follow)

#### Scenario: Changed: Nothing changed gives a zero count and exit 0

- **GIVEN** a repository whose plan is the same as at the base
- **WHEN** the check runs
- **THEN** its last line is `RESULT changed requirements=0 unplanned=0 no_scenario=0 wording_only=0 exit=0`

#### Scenario: Changed: A missing base is reported, not crashed

- **GIVEN** a base revision that does not exist
- **WHEN** the check runs
- **THEN** it prints the skipped line and exits 0

#### Scenario: Changed: Mode off skips the check

- **GIVEN** `lockstep.yaml` with `checks: {changed: off}`
- **WHEN** `lockstep check changed` runs
- **THEN** it prints `skipped (off)` and exits 0

### Requirement: Test-first: A changed scenario needs a test that fails before the change

`lockstep check test-first --base <rev>` SHALL, for each scenario that both revisions define and whose text differs (runs of whitespace counting as one space; text from an active change's spec delta replacing the spec's), run every test marked for it against the base revision's source, and SHALL report `no-failing-test <scenario id>` and exit 1 when none of them fails there. It SHALL NOT check a scenario that a plan new or different from the base declares on a `Wording-only:` line, by its own ID or its requirement's. Its count line SHALL add `changed=<n>`, the number of changed scenarios checked, and `no_failing_test=<n>`.

Source: Brian, 2026-10-15: "we plan out with models and diagrams and then those are linked to tests presumablhy in a tdd way"; Brian, 2026-11-17: "the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842). That one failing test is enough for a changed scenario, where every test must fail for a new one, is inferred by agent (a changed scenario keeps tests for the parts that did not change).

#### Scenario: Test-first: A changed scenario whose tests all pass on the base fails the check

- **GIVEN** a scenario whose text differs from the base and whose only test passes on the base source
- **WHEN** the check runs
- **THEN** it reports `no-failing-test` for the scenario and exits 1

#### Scenario: Test-first: One test that fails on the base is enough for a changed scenario

- **GIVEN** a scenario whose text differs from the base, with one test that passes on the base source and one that fails there
- **WHEN** the check runs
- **THEN** it exits 0

#### Scenario: Test-first: A wording-only scenario is not checked

- **GIVEN** a scenario whose text differs from the base, whose only test passes on the base source, and a plan in the same change set with `Wording-only:` listing its requirement
- **WHEN** the check runs
- **THEN** it exits 0

## MODIFIED Requirements

### Requirement: Test-first: Tests for existing behavior are exempt and counted

The test-first check SHALL not run a test marked `req(..., existing=True)` for a scenario that is new since the base, and SHALL report how many such tests it skipped. For a scenario whose text changed since the base, `existing=True` SHALL NOT exempt a test: it is run on the base source like any other test marked for that scenario.

Source: inferred by agent (working default awaiting Brian: tests marked existing=True for behavior that already worked are not run on the base revision, so existing repositories can adopt the format) Ported from code2-template `openspec/specs/test-first/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4). The changed-scenario sentence is inferred by agent, 2026-11-17 (once the text changes, the behavior it describes is not the existing one).

#### Scenario: Test-first: Existing-behavior test is skipped and counted

- **GIVEN** a scenario added since the base and its test, marked `existing=True`, that passes on the base
- **WHEN** the check runs
- **THEN** it exits 0 and lists the test as existing

#### Scenario: Test-first: An existing-behavior mark does not exempt a changed scenario

- **GIVEN** a scenario whose text differs from the base and whose only test, marked `existing=True`, passes on the base source
- **WHEN** the check runs
- **THEN** it reports `no-failing-test` for the scenario and exits 1
