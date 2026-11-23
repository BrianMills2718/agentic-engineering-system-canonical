## MODIFIED Requirements

### Requirement: A copy hands an editing agent the requirement text

A repository made from the template SHALL include `.claude/settings.json` and `.codex/hooks.json` whose PreToolUse hooks run `uv run lockstep-hook` (the copy's own locked Lockstep) on file edits and shell commands, without `PCW_MODE=block`, and SHALL git-ignore `docs/links.json`. Its first decision record SHALL carry a `- Governs:` line naming a file the copy has.

Source: Brian, 2026-11-23: "isnt this the whole thing that makes the whle systme work?"; AES docs/architecture/GOAL.md:88; plan docs/planning/linked-chain-core-2026-11-23.md

Source: Brian, 2026-11-23: "i approve" (decision -> requirement or code links that the hook hands over, read from lines that already exist); plan docs/planning/links-existing-lines-2026-11-23.md

#### Scenario: A rendered copy has both hook files

- **GIVEN** the template rendered with its defaults
- **WHEN** its `.claude/settings.json` and `.codex/hooks.json` are read
- **THEN** each runs `uv run lockstep-hook` on edits, neither sets `PCW_MODE=block`, and `.gitignore` lists `docs/links.json`

#### Scenario: A rendered copy's decision governs a real file

- **GIVEN** the template rendered with its defaults
- **WHEN** its decision records are read
- **THEN** decision 0001's `Governs:` target is `docs/architecture/model.c4`, a file in the copy
