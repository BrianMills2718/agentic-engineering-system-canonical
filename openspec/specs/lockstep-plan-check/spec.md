# lockstep-plan-check Specification

## Purpose

`lockstep plan check` validates a repository's plan format: the acceptance-criteria file and, when Brian's words and a stored coverage judgment are recorded, that each requirement is sourced in his words and covered (`proposals/one-planning-tool/DESIGN.md`, slice 5).

## Requirements

### Requirement: The acceptance-criteria file is validated

Source: Brian, 2026-10-27: "i am concerned that the success critiria and the demonstration of scucess cirtieria that are jdugemable by me and the represntations of these so tha ti can do this havent alreayd been worked out. i thoguth this was part of company planning ocmpliance" (Company Planning `package-contract.md`, "Acceptance criteria"); its move into Lockstep approved by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 5).

`lockstep plan check` SHALL read `docs/planning/acceptance-criteria.json` (or the path given with `--acceptance`) and
exit 1, naming each problem, unless: the record type is `acceptance_criteria`; it lists at least one entry; each entry
has a unique `id` and the seven fields `criterion`, `demonstration`, `expected`, `failure_example`, `representation`,
`entrypoint` and `status`; `demonstration` is a list of non-empty steps; `representation` has a `view` and a
`router_record` naming an existing repository file (and an existing `variants` file when given); `entrypoint` is a
URL or `planned`; `status` is `not built`, `built`, `judged pass` or `judged fail`; a status other than `not built`
has a URL, not `planned`; and a judged status carries `judgment` with `by` and `source`, the judge's own recorded
words. It exits 2 when the file is missing or is not JSON.

#### Scenario: A complete acceptance file passes

- **GIVEN** an acceptance file with one entry that has all seven fields, a router record that exists and status `not built`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 0 and prints the count of criteria by status

#### Scenario: An entry missing a field fails

- **GIVEN** an entry without one of the seven fields
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and says `A1: no <field>`

#### Scenario: A malformed entry fails

- **GIVEN** an entry whose demonstration is not a list of steps, whose representation has no view or a router record that does not exist, whose entrypoint is neither a URL nor `planned`, or whose status is not one of the four
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and names that problem for that entry

#### Scenario: A built entry that still says planned fails

- **GIVEN** an entry with status `built` and entrypoint `planned`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and asks for the URL it opens at

#### Scenario: A judged status without the judge's words fails

- **GIVEN** an entry with status `judged pass` and no `judgment` with `by` and `source`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1; with `judgment: {by, source}` it exits 0

#### Scenario: Duplicate ids and an empty list fail

- **GIVEN** two entries with the same id, or no entries
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and says `duplicate id` or `entries: none listed`

#### Scenario: A missing or unreadable file cannot be checked

- **GIVEN** no acceptance file, or one that is not JSON
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 2 and says what is wrong

### Requirement: Each plan requirement is sourced in Brian's words and covered

Source: Brian, 2026-10-27, the greer request "start the Greer whole-document graph view now: each hearing as one connected graph you can open and ask questions of" that a rewritten outcome dropped (Company Planning `coverage_check.py`, "Why", and `package-contract.md`, "Goal coverage"); Brian, 2026-11-06, "i approve" (three-call judgment); moved into Lockstep with the approval of 2026-11-11 above (slice 5).

When the acceptance file carries Brian's words (`asked_by`) and a stored coverage judgment (`coverage`, written by Company
Planning's `coverage_check.py`), `lockstep plan check` SHALL exit 1 unless: the judgment lists requirements with unique ids
and exactly one mapping each; each requirement's quote is found in the `asked_by` words it cites (exactly, or word for word
with a few of his typos re-spelled); each requirement not about the planning process is covered in full by criteria that
exist, or deferred by a `deferred` entry recorded as Brian's own words with date and source; an outcome requirement that was
not deferred is kept by the `outcome` line; and the judgment is not stale (Brian's words, the outcome, or a criterion or
deferral it relied on changed since it was judged). Criteria edited or added since are reported as pending, not failed. A
file with `asked_by` but no judgment fails; a file with neither skips this check and says so. Lockstep makes no model call.

#### Scenario: A covered requirement passes

- **GIVEN** a judgment whose one requirement quotes Brian's words and is fully covered by an existing criterion
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 0 and prints the count of requirements covered

#### Scenario: A gap in coverage fails

- **GIVEN** a requirement that is uncovered, only partly covered, covered by a criterion that does not exist, dropped from the outcome line, or deferred without a recorded deferral of Brian's
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and names that requirement and gap

#### Scenario: An invented quote fails and a re-spelled typo passes

- **GIVEN** a requirement whose quote is not in Brian's words, or one that differs from them only by a near spelling of one of his typos
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 for the invented or changed quote and exits 0 for the re-spelled typo

#### Scenario: A deferral in Brian's words counts

- **GIVEN** a requirement mapped to a `deferred` entry with who `Brian`, words, date and source
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 0 and counts it as deferred

#### Scenario: A stale or missing judgment is reported

- **GIVEN** Brian's words changed after the judgment, or `asked_by` without any judgment, or a criterion edited after the judgment
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 for the first two and exits 0 with a pending note for the third

#### Scenario: A file without Brian's words skips the requirement check

- **GIVEN** an acceptance file with no `asked_by` and no `coverage`
- **WHEN** `lockstep plan check` runs
- **THEN** it says the requirement check was skipped and the result depends on the acceptance check alone

### Requirement: The command is reached as `lockstep plan check`

Source: Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 5: "`lockstep plan check` validates it").

`lockstep plan check` SHALL accept `--repo PATH` (default the current directory), `--acceptance PATH` (default
`docs/planning/acceptance-criteria.json` under the repository) and `--json`, which prints the result as one object.

#### Scenario: The acceptance path can be overridden

- **GIVEN** an acceptance file at another path
- **WHEN** `lockstep plan check --acceptance that/path.json` runs
- **THEN** that file is the one checked
