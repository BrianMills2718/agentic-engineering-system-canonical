# lockstep-wiki Specification

## Purpose

Give a layout repository a generated wiki: one page per OpenSpec capability showing each requirement's text, the code that implements it, its tagged tests and its coverage state, kept fresh by `lockstep check project`.

## Requirements

### Requirement: A layout repository generates one wiki page per capability

In a layout repository whose `lockstep.yaml` says `generated_wiki: true`, `lockstep check project` SHALL write `generated/wiki/index.md`, with one line per OpenSpec capability (its summary and a link to its page), and `generated/wiki/<capability>.md` for each capability. A capability page SHALL list each requirement's text, the symbols whose docstrings implement it with their `file:line`, each scenario with the tests tagged with its ID, and the requirement's coverage state (unimplemented, untested, or implemented and tested). The pages SHALL hold no commit hash and no pass or fail result, so they are the same in every checkout; `lockstep status` gives pass or fail. A page for a capability that no longer exists SHALL be removed.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 1 (restore the dropped wiki generator); told the agent to proceed without waiting. The `generated_wiki` switch, the coverage-only status and the page layout are inferred by agent.

#### Scenario: A capability page shows requirement, code and tests

- **GIVEN** a layout repository with `generated_wiki: true`, a requirement implemented by a function and a scenario with a tagged test
- **WHEN** `lockstep check project` runs
- **THEN** `generated/wiki/index.md` has one line for the capability and its page shows the requirement text, the function with its file and line, and the test

#### Scenario: A repository without the switch gets no pages

- **GIVEN** a layout repository without `generated_wiki`
- **WHEN** `lockstep check project` runs
- **THEN** no `generated/wiki/` folder is written

### Requirement: Project check fails on stale or unreachable wiki pages

`lockstep check project --check` SHALL name each `generated/wiki/` page that differs from what would be written, and SHALL exit 1. It SHALL also report each generated page that is more than two links from the index or whose link has no summary beside it, and exit 1.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 1 (restore the dropped wiki generator); told the agent to proceed without waiting. Reusing the existing reachability rule inferred by agent.

#### Scenario: A stale page fails the check

- **GIVEN** committed generated pages and a test added after
- **WHEN** `lockstep check project --check` runs
- **THEN** it names the capability page and exits 1, and it writes nothing

### Requirement: Generated wiki pages need no layout row

A file under `generated/wiki/` SHALL NOT be reported as unplanned in a layout repository, and the Markdown file cap SHALL NOT count it.

Source: Brian, 2026-11-17, "skip generated" (the cap); the layout-row exemption inferred by agent, since the pages change with the specs.

#### Scenario: A generated page is not unplanned

- **GIVEN** a layout repository governing `.` and a file `generated/wiki/index.md` with no layout row
- **WHEN** the whole-tree rule judges it
- **THEN** it is not reported as unplanned, and a file `generated/other.md` with no row still is

### Requirement: Python m lockstep wiki prints the layout wiki

`python -m lockstep.wiki` in a layout repository SHALL print the generated wiki pages as plain text and exit 0, and `python -m lockstep.wiki_reach` there SHALL check them, instead of failing for want of `.aes/project.yaml`.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 1 (restore the dropped wiki generator); told the agent to proceed without waiting.

#### Scenario: The wiki command works in a layout repository

- **GIVEN** a layout repository with no `.aes/` folder
- **WHEN** `python -m lockstep.wiki` runs
- **THEN** it prints the index and each capability page and exits 0
