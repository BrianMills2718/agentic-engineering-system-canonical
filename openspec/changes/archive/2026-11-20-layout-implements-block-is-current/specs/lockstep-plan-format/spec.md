## ADDED Requirements

### Requirement: A planned file without a cog plan copy is judged by its Implements block

Source: Brian, 2026-11-20, "yes" to proving Lockstep on a from-scratch repository (`docs/planning/next.goal.md`, step 3), where every edit to a planned file that predated its layout row was refused; the rule itself inferred by agent from `proposals/one-planning-tool/DESIGN.md` ("one projector ... fed from OpenSpec").

In a layout repository, the edit hook SHALL treat a planned file that holds no cog plan copy as current when `lockstep check project` would not change it, and as stale when that command would rewrite its generated `Implements:` requirement text. A stale file's refusal SHALL name `uv run lockstep check project`, and running that command SHALL clear it. A file with a cog plan copy, and a repository with `.aes/target.yaml`, SHALL be judged as before.

#### Scenario: An existing file with a current Implements block can be edited

- **GIVEN** a file written before its layout row, whose `Implements:` block `lockstep check project` has written
- **WHEN** an agent edits it under `PCW_MODE=block`
- **THEN** the edit is allowed and the agent is handed the requirement text

#### Scenario: A stale Implements block names the command that fixes it

- **GIVEN** that file and an active change that rewords its requirement
- **WHEN** an agent edits it under `PCW_MODE=block`, runs `lockstep check project`, and edits it again
- **THEN** the first edit is refused naming `lockstep check project` and not `make project`, and the second is allowed with the new text
