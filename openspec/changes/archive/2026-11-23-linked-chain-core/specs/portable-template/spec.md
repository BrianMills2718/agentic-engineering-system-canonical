## ADDED Requirements

### Requirement: A copy hands an editing agent the requirement text

A repository made from the template SHALL include `.claude/settings.json` and `.codex/hooks.json` whose PreToolUse hooks run `uv run lockstep-hook` (the copy's own locked Lockstep) on file edits and shell commands, without `PCW_MODE=block`, and SHALL git-ignore `docs/links.json`.

Source: Brian, 2026-11-23: "isnt this the whole thing that makes the whle systme work?"; AES docs/architecture/GOAL.md:88; plan docs/planning/linked-chain-core-2026-11-23.md

#### Scenario: A rendered copy has both hook files

- **GIVEN** the template rendered with its defaults
- **WHEN** its `.claude/settings.json` and `.codex/hooks.json` are read
- **THEN** each runs `uv run lockstep-hook` on edits, neither sets `PCW_MODE=block`, and `.gitignore` lists `docs/links.json`
