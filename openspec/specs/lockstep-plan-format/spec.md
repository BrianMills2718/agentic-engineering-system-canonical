# lockstep-plan-format Specification

## Purpose

Lockstep's one plan format: OpenSpec for what the code must do, plus `layout:` rows in `lockstep.yaml` for which files exist and why (`proposals/one-planning-tool/DESIGN.md`, slice 2).

## Requirements

### Requirement: The plan is OpenSpec plus layout rows

In a repository whose `lockstep.yaml` has a `layout:` list and which has no `.aes/target.yaml`, Lockstep SHALL take the
planned files from the `layout:` rows (path, purpose, the OpenSpec requirements it implements, its tests, optionally
its typed exports), the governed folders from `governed:`, and the requirement text from OpenSpec. A repository with
`.aes/target.yaml` SHALL be read as before.

Source: Brian, 2026-11-11, approving the one-tool design as written ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 2: "Lockstep reads requirements from OpenSpec ... and layout from `lockstep.yaml`. `.aes/target.yaml` stays readable until lifelike and Team-Brains move off it").

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

In a layout repository, the whole-tree commit check SHALL judge a planned file's docstring exactly as the edit hook does, and its stale reason SHALL name `uv run lockstep check project`. A refusal for an undeclared, removed or retyped public symbol SHALL name the file's layout row `exports:` in lockstep.yaml as where to declare it. Every edit-hook refusal SHALL end by pointing to the layout rows in `lockstep.yaml` and to `uv run lockstep show <file>`, and SHALL NOT point to `python -m lockstep.wiki`, which needs an AES plan. A repository with `.aes/target.yaml` SHALL keep its current wording.

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
