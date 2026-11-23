## ADDED Requirements

### Requirement: Lockstep governs its own package

The design this repository ships says: Its opinionated approach starts with planned structure: name the behavioral units, the files that hold them, their public typed seams, the requirements they implement and the tests or other checks that establish success. Then implement inside those boundaries. In the layout route, OpenSpec owns behavior and `lockstep.yaml` owns file purpose, requirement links, test paths and optional exports. This repository SHALL follow it for its own package: its `lockstep.yaml` SHALL list `src/lockstep/` under `governed:`, SHALL mark it `fixed:`, and SHALL have one `layout:` row for every file tracked under `src/lockstep/`; its `.claude/settings.json` and `.codex/hooks.json` SHALL run `lockstep-hook` before edits.

Source: Brian, 2026-11-23, "i approve" to turning the full system on in AES (`docs/planning/back-on-design-2026-11-23.md`); the checkable form inferred by agent.

#### Scenario: Every package file is planned and the hook refuses an unplanned one

- **GIVEN** this repository at HEAD
- **WHEN** its `lockstep.yaml` and client settings are read
- **THEN** every tracked file under `src/lockstep/` has a layout row, `src/lockstep/` is governed and fixed, both client settings run `lockstep-hook` on PreToolUse, and the hook refuses a write to `src/lockstep/not_planned.py`
