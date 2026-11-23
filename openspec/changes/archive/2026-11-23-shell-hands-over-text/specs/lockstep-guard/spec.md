## ADDED Requirements

### Requirement: Agents get requirement text from the shell too

In a repository with OpenSpec specs and no layout plan, the edit hook SHALL answer a shell command that names or writes a file whose docstrings carry `Implements:` lines with those requirements' text, without a `permissionDecision`, and SHALL log the call as `openspec_text` with the requirement IDs; a command naming no such file SHALL get no answer.

Source: inferred by agent from the 2026-11-23 linked-chain acceptance run (Claude edited only through Bash, so the text never arrived); plan docs/planning/linked-chain-core-2026-11-23.md

#### Scenario: A shell command on an implementing file gets its requirement text

- **GIVEN** a file whose docstring says `Implements: ship/<requirement>`
- **WHEN** the agent runs `cat` on it, writes it with a heredoc, or edits it with `sed -i`
- **THEN** the hook's answer holds that requirement's text and no decision
