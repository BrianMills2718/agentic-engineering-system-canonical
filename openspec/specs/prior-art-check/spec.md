# prior-art-check Specification

## Purpose

Make an agent look for existing work before building a feature, and write a decision for each candidate it
finds, so that only what is needed gets built. An OpenSpec change that adds a requirement carries a checked
`prior-art.json`; `ship` refuses the merge without one. Ported from code2-workspace (`ec500633`) on 2026-11-20 so
the check is public and runs on any machine.

## Requirements

### Requirement: A change that adds a requirement carries a prior-art record

`src/lockstep/prior_art.py` (`lockstep check prior-art`) SHALL fail (exit 1) for each unarchived OpenSpec change that needs a record and
has no `prior-art.json`, naming the change and the path to create, and for a `prior-art.json` that is not
valid JSON or that breaks `src/lockstep/prior-art.schema.json`, printing each violation with its place in the file.
It SHALL exit 0 when every change that needs a record has a valid one.

Source: Brian, 2026-11-17: "every cpaability/featuer shoul dhave a prior art search so that we are only
buidling what we need to. that needs to be ienforced". Ported from code2-workspace `ec500633` (2026-11-20, minimal core section 7) so the check is public.

#### Scenario: No record on a change that adds a requirement

- **GIVEN** an unarchived change dated 2026-11-18 with `## ADDED Requirements` and no `prior-art.json`
- **WHEN** the check runs
- **THEN** it exits 1 and names the path `prior-art.json` would have

#### Scenario: Complete record

- **GIVEN** the same change with a complete `prior-art.json`
- **WHEN** the check runs
- **THEN** it exits 0

#### Scenario: Invalid JSON

- **GIVEN** a `prior-art.json` that is not JSON
- **WHEN** the check runs
- **THEN** it exits 1

### Requirement: A candidate cannot be left undecided and the decision must follow from the candidates

`src/lockstep/prior-art.schema.json` SHALL state every rule about the record's content, and the check SHALL apply
it with the `jsonschema` package, not with rules written again in Python: each candidate's verdict is one of
adopt, combine, fork or reject; the search lists at least one place in our own work and one outside it; a
decision of adopt, combine or fork needs a candidate with that verdict; a decision of build needs a non-empty
gap and every candidate rejected.

Source: inferred by agent, from the incident above (a candidate list left "not yet evaluated" for 53 days);
the four verdict words and the field names are working defaults.

#### Scenario: Verdict not yet evaluated

- **GIVEN** a record with a candidate whose verdict is "not yet evaluated"
- **WHEN** the check runs
- **THEN** it exits 1

#### Scenario: Build without a gap

- **GIVEN** a record whose decision is `build` and which has no `gap`
- **WHEN** the check runs
- **THEN** it exits 1

#### Scenario: Build while a candidate is adopted

- **GIVEN** a record whose decision is `build` while a candidate's verdict is `adopt`
- **WHEN** the check runs
- **THEN** it exits 1

#### Scenario: Adopt without an adopted candidate

- **GIVEN** a record whose decision is `adopt` and no candidate has verdict `adopt`
- **WHEN** the check runs
- **THEN** it exits 1

#### Scenario: Search with nothing outside

- **GIVEN** a record whose searches are all in our own work
- **WHEN** the check runs
- **THEN** it exits 1

#### Scenario: Real record against the real schema

- **GIVEN** the real schema file and this change's own record
- **WHEN** the record is validated
- **THEN** it has no violations

### Requirement: Only a change that adds a requirement, from the start date, needs a record

The check SHALL require a record only for a change whose date is on or after `--since` (default 2026-11-18) and whose spec deltas hold a line exactly `## ADDED Requirements`. A change's date is its `.openspec.yaml` `created` date; when that is missing or unreadable, it is the date git first committed a file in the change folder; a change with neither counts as needing a record. Without `--files` it SHALL look only at unarchived changes. With `--files` it SHALL look only at the changes those paths belong to, archived (`openspec/changes/archive/<name>/`) or not. It SHALL print one summary line with counts and exit 2 when it cannot run.

Source: inferred by agent: the start date and the ADDED-header test are working defaults; the header marks what OpenSpec treats as new required behavior. Inferred by agent (code2-workspace issue 833, slice 1): archived changes named by `--files` are checked, because `ship` checks a merge after its change has been archived. Inferred by agent (issue 833 follow-up, 2026-11-18): five changes made before the rule had no `created` date and were refused, so git's first commit date stands in for it.

#### Scenario: Only modified requirements

- **GIVEN** a change whose only delta header is `## MODIFIED Requirements`
- **WHEN** the check runs
- **THEN** it exits 0 and counts no change as needing a record

#### Scenario: Change before the start date

- **GIVEN** a change created 2026-11-17 that adds a requirement and has no record
- **WHEN** the check runs
- **THEN** it exits 0 and counts no change as needing a record

#### Scenario: Undated change first committed before the start date

- **GIVEN** a change with no `created` date that adds a requirement, has no record, and was first committed on 2026-11-13
- **WHEN** the check runs
- **THEN** it exits 0 and counts no change as needing a record

#### Scenario: Undated change never committed

- **GIVEN** a change with no `created` date that adds a requirement, has no record, and has never been committed
- **WHEN** the check runs
- **THEN** it reports the missing record and exits 1

#### Scenario: Archived change

- **GIVEN** a change under `openspec/changes/archive/` that adds a requirement and has no record
- **WHEN** the check runs
- **THEN** it exits 0 and looks at no change

#### Scenario: Archived change named by files

- **GIVEN** a change under `openspec/changes/archive/` that adds a requirement and has no record
- **WHEN** the check runs with `--files` naming a file in that change
- **THEN** it reports the missing record and exits 1

#### Scenario: Files limit the check

- **GIVEN** two changes needing a record, only one with a record, and `--files` naming a file of the one with a record
- **WHEN** the check runs
- **THEN** it exits 0
