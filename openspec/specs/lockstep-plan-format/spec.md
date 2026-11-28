# lockstep-plan-format Specification

## Purpose

Lockstep's one plan format: OpenSpec for what the code must do, plus `layout:` rows in `lockstep.yaml` for which files exist and why (`proposals/one-planning-tool/DESIGN.md`, slice 2).

## Requirements

### Requirement: The plan is OpenSpec plus layout rows

In a repository whose `lockstep.yaml` has a `layout:` list and which has no `.aes/target.yaml`, Lockstep SHALL take the
planned files from the `layout:` rows (path, purpose, the OpenSpec requirements it implements, its tests, optionally
its typed exports), the governed folders from `governed:`, and the requirement text from OpenSpec. A `governed:` entry
ending in `/` covers every path under it, `.` covers the whole repository, and any other entry covers that one file or
a folder of that name. A repository with
`.aes/target.yaml` SHALL be read as before.

Source: Brian, 2026-11-11, approving the one-tool design as written ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 2: "Lockstep reads requirements from OpenSpec ... and layout from `lockstep.yaml`. `.aes/target.yaml` stays readable until lifelike and Team-Brains move off it"). How a `governed:` entry matches (`/`, `.`, a file or folder name) inferred by agent, 2026-11-24, after a review found a bare `Makefile` entry covered `Makefile.bak` and a list of top-level names missed a new top-level file.

#### Scenario: The layout is laid out with first docstrings

- **GIVEN** a layout row for `src/greeter/__init__.py` implementing `greeting/greet-by-name`, tested by `tests/test_greet.py`
- **WHEN** `lockstep layout` runs
- **THEN** the file is created with a docstring holding its `Implements:` line, the requirement and its scenarios word for word, the test names and its declared signature, and an existing file is left as it is

#### Scenario: An unplanned file is refused against the layout

- **GIVEN** `governed: [src/]` and no row for `src/greeter/extra.py`
- **WHEN** an agent writes that file under `PCW_MODE=block`
- **THEN** the edit hook refuses it and names `lockstep.yaml` as where the file must be planned

#### Scenario: A planned file's edit hands over its requirement

- **GIVEN** a laid-out planned file
- **WHEN** an agent edits it
- **THEN** the edit is allowed and the agent is handed the OpenSpec requirement text

#### Scenario: The whole-tree check reads the layout

- **GIVEN** a laid-out, committed layout repository
- **WHEN** `lockstep check` runs, and again after an unplanned file is added under `src/`
- **THEN** the first allows and the second blocks with that file as `unplanned`

#### Scenario: A layout row must name real requirements

- **GIVEN** a row whose `implements` names a requirement no spec defines, and a row with no purpose
- **WHEN** the layout is checked
- **THEN** both are reported, naming the row's path

#### Scenario: A governed entry covers what it names

- **GIVEN** `governed:` entries `src/`, `.`, `Makefile` and `src/lockstep`
- **WHEN** paths are matched against each
- **THEN** `src/` covers `src/a/b.py` but not `srcx/b.py`, `.` covers every path, `Makefile` covers `Makefile` but not `Makefile.bak`, and `src/lockstep` covers `src/lockstep/x.py` but not `src/lockstep_old.py`

#### Scenario: An AES plan is still read

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** Lockstep reads its plan
- **THEN** the planned files come from `.aes/target.yaml` exactly as before

### Requirement: A planned file without a cog plan copy is judged by its Implements block

In a layout repository, the edit hook SHALL treat a planned file that holds no cog plan copy as current when `lockstep check project` would not change it, and as stale when that command would rewrite its generated `Implements:` requirement text. A stale file's refusal SHALL name `uv run lockstep check project`, and running that command SHALL clear it. A file with a cog plan copy, and a repository with `.aes/target.yaml`, SHALL be judged as before.

Source: Brian, 2026-11-20, "yes" to proving Lockstep on a from-scratch repository (`docs/planning/next.goal.md`, step 3), where every edit to a planned file that predated its layout row was refused; the rule itself inferred by agent from `proposals/one-planning-tool/DESIGN.md` ("one projector ... fed from OpenSpec").

#### Scenario: An existing file with a current Implements block can be edited

- **GIVEN** a file written before its layout row, whose `Implements:` block `lockstep check project` has written
- **WHEN** an agent edits it under `PCW_MODE=block`
- **THEN** the edit is allowed and the agent is handed the requirement text

#### Scenario: A stale Implements block names the command that fixes it

- **GIVEN** that file and an active change that rewords its requirement
- **WHEN** an agent edits it under `PCW_MODE=block`, runs `lockstep check project`, and edits it again
- **THEN** the first edit is refused naming `lockstep check project` and not `make project`, and the second is allowed with the new text

### Requirement: Every refusal in a layout repository names a layout command

In a layout repository, the whole-tree commit check SHALL judge a planned file's docstring exactly as the edit hook does, and its stale reason SHALL name `uv run lockstep check project`. A refusal for an undeclared, removed or retyped public symbol SHALL name the file's layout row `exports:` in lockstep.yaml as where to declare it. Every edit-hook refusal SHALL end by pointing to the layout rows in `lockstep.yaml` and to `uv run lockstep show <file>`, and SHALL NOT point to `python -m lockstep.wiki`. A repository with `.aes/target.yaml` SHALL keep its current wording.

Source: Brian, 2026-11-20, "yes" to proving Lockstep on a from-scratch repository (`docs/planning/next.goal.md`, step 3), whose rerun was blocked at commit by a check naming `.aes/target.yaml`; the rule itself inferred by agent. The refusal pointer added 2026-11-23 after `python -m lockstep.wiki` was found to crash in a layout repository (inferred by agent, while carrying out Q54).

#### Scenario: The commit check judges an Implements block the same way

- **GIVEN** a committed file whose `Implements:` block is current, edited in the working tree
- **WHEN** `lockstep check` runs, then again after an active change rewords its requirement, then after `lockstep check project`
- **THEN** it allows, then blocks the file as stale naming `lockstep check project` and not `.aes/target.yaml`, then allows

#### Scenario: An undeclared public symbol names the layout exports

- **GIVEN** a planned layout file
- **WHEN** an agent's edit adds a public function its layout row does not export, under `PCW_MODE=block`
- **THEN** the edit is refused naming the row's `exports:` in lockstep.yaml and not `aes plan`

#### Scenario: A refusal points to lockstep show, not the wiki

- **GIVEN** a layout repository with no `.aes/` folder
- **WHEN** the edit hook refuses a write to an unplanned file
- **THEN** the refusal names `uv run lockstep show` and does not name `python -m lockstep.wiki`

### Requirement: Lockstep governs its own package

The design this repository ships says: Its opinionated approach starts with planned structure: name the behavioral units, the files that hold them, their public typed seams, the requirements they implement and the tests or other checks that establish success. Then implement inside those boundaries. In the layout route, OpenSpec owns behavior and `lockstep.yaml` owns file purpose, requirement links, test paths and optional exports. This repository SHALL follow it for its own package: its `lockstep.yaml` SHALL list `src/lockstep/` under `governed:`, SHALL mark it `fixed:`, and SHALL have one `layout:` row for every file tracked under `src/lockstep/`; its `.claude/settings.json` and `.codex/hooks.json` SHALL run `lockstep-hook` before edits.

Source: Brian, 2026-11-23, "i approve" to turning the full system on in AES (`https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/back-on-design-2026-11-23.md`); the checkable form inferred by agent.

#### Scenario: Every package file is planned and the hook refuses an unplanned one

- **GIVEN** this repository at HEAD
- **WHEN** its `lockstep.yaml` and client settings are read
- **THEN** every tracked file under `src/lockstep/` has a layout row, `src/lockstep/` is governed and fixed, both client settings run `lockstep-hook` on PreToolUse, and the hook refuses a write to `src/lockstep/not_planned.py`

### Requirement: Old-route checks stay while a repository runs them

For a repository with `.aes/target.yaml`, Lockstep SHALL keep the checks that plan route uses, each importable as
`lockstep.<name>` and `pcw.<name>`, and runnable as `python -m` under both names where it has a command line:
`action_check`, `behavior_check`, `change_list`, `change_log`, `criterion_checks`, `declared_reason`,
`docstring_up`, `linked_tests`, `plan_edit`, `plan_to_code`, `requirement_status`, `unplanned_symbols`, `wiki` and
`wiki_reach`. One SHALL be retired, with a dated record under
`docs/retired/`, only once no repository in `~/code2` runs it (code2-workspace decision 0009: `.aes/target.yaml`
retires one repository at a time).

Source: Brian, 2026-11-23: "i approve", to Q54 in `docs/planning/open-questions.json` ("write one requirement for
the ones the core calls; retire the rest"); the 2026-11-23 search found all 14 still run, so none retired (inferred by
agent from that search).

#### Scenario: An AES-plan repository's checks still run

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** its Makefile or edit hook runs one of the 14 checks
- **THEN** the check runs as before, as each module's own tests show

### Requirement: AES plans every tracked file

This repository's `lockstep.yaml` SHALL have one `layout:` row with a nonempty purpose for every Git-tracked file, SHALL govern the whole repository (`.` under `governed:`), so a new file anywhere, including a new top-level file or folder, is reported, and SHALL project the rows' paths and purposes into `generated/files.md`, which `wiki/index.md` links.

Source: Brian, 2026-11-13, AES #849: "Every Git-tracked file must be reachable and summarized from `wiki/index.md`"; where the rows live: Brian, 2026-11-11, approving `proposals/one-planning-tool/DESIGN.md` (line 41: which files exist and why lives in `lockstep.yaml` `layout:` rows). The checkable form is inferred by agent.

#### Scenario: Every tracked file has a planned row and the catalog page is current

- **GIVEN** this repository at HEAD
- **WHEN** its tracked files, `lockstep.yaml` and `generated/files.md` are read
- **THEN** every tracked file has a layout row with a purpose, a new file in a new top-level folder, at the top level or under `docs/` is governed, the projection of the layout into `generated/files.md` is current, and `wiki/index.md` links `generated/files.md`

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
