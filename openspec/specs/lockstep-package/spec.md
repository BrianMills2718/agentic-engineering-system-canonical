# lockstep-package Specification

## Purpose

Lockstep, the one planning-and-checking tool, installs from this repository, and its old `pcw` names keep working until its users move (`proposals/one-planning-tool/DESIGN.md`, slice 1).

## Requirements

### Requirement: Lockstep installs from AES canonical

Source: Brian, 2026-11-11, approving the one-tool design as written ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 1).

Installing this repository SHALL provide the Python package `lockstep` and the commands `lockstep` and
`lockstep-hook`, which run Lockstep's whole-tree check and its agent edit hook.

#### Scenario: The check runs from an install

- **GIVEN** this repository installed into a fresh environment
- **WHEN** `lockstep check --help` runs
- **THEN** it exits 0 and prints the check's usage

### Requirement: The old pcw names keep working

Source: Brian, 2026-11-11, approving the one-tool design as written; its slice 1 says "`pcw` and `pcw-hook` stay as alias entry points so lifelike and Team-Brains' vendored runner keep working".

The commands `pcw` and `pcw-hook`, `python -m pcw.<module>` and cog blocks that say `import pcw.cogtext as c`
SHALL run the same code as their `lockstep` names, until every user has moved.

#### Scenario: An old module path runs the new code

- **GIVEN** this repository installed
- **WHEN** `python -m pcw.check --help` runs
- **THEN** it runs `lockstep/check.py` and exits 0

#### Scenario: An old cog block is still a valid plan copy

- **GIVEN** a planned file whose docstring block says `import pcw.cogtext as c`
- **WHEN** Lockstep's check reads it
- **THEN** it is judged as a Lockstep plan copy, exactly as `import lockstep.cogtext as c` is
