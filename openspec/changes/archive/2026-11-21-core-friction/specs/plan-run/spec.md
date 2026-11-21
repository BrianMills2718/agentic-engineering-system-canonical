## MODIFIED Requirements

### Requirement: One driver runs a plan with Claude or Codex

`lockstep run-plan <change> --agent claude|codex` SHALL run `accept write`, then one headless implementer session in a new worktree on branch `impl/<change>-<run id>`, then `accept check`, saving each session's JSON event stream as its transcript, and SHALL print the `ship` command to run next without running it: `uv run ship` when the repository's `pyproject.toml` depends on `agentic-engineering-system` (which installs `ship`), else `ship`. The agent choice SHALL change only the command that starts each session.

Source: Brian, 2026-09-14: "the answer is always yes" (keep Claude Code and Codex in sync; workspace agents/rule-sources.md, Policy `claude-codex-parity`), via minimal-core-2026-11-20.md K6. Inferred by agent, 2026-11-21 (#994): a second user has `ship` only inside the repository's environment.

#### Scenario: Each agent gets its own command

- **WHEN** `agent_command` is built for `codex` and for `claude` with the same prompt and worktree
- **THEN** the codex command is `codex exec --json` with `-C <worktree>`, the claude command is `claude -p --output-format stream-json` started in the worktree, both carry the prompt, and a session that keeps no history adds `--ephemeral` or `--no-session-persistence`

#### Scenario: The driver does not merge

- **GIVEN** a fake runner whose implementer commits
- **WHEN** `run_plan` finishes
- **THEN** the default branch is unchanged, the implementer branch exists, and the printed output contains the `ship` command

#### Scenario: The printed ship command matches the repository

- **GIVEN** one repository whose `pyproject.toml` lists `agentic-engineering-system` and one that does not
- **WHEN** `ship_command` is asked for each
- **THEN** it gives `uv run ship` for the first and `ship` for the second
