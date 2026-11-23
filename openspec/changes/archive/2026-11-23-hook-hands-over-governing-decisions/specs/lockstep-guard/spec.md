## ADDED Requirements

### Requirement: Agents get the decisions that govern a file

In a repository with OpenSpec specs and a `docs/decisions/` folder, the edit hook SHALL hand an agent that edits a file, or names it in a shell command, each decision record whose `Governs:` line names that file, a folder above it (a target ending in `/` or naming an existing folder), or a requirement or capability the file implements, after any requirement text and without a `permissionDecision`. It SHALL read the record's existing lines only: `Governs:` (or `- Governs:`, comma separated, anchors ignored for paths), `status:` front matter or a `Status:` line, and `superseded_by:` or the text after "superseded by". Each decision SHALL be given as its ID, title, status, file and decision paragraph cut at 600 characters, at most three in full (own path first, then requirement or capability, then folder) and the rest by ID; a superseded decision SHALL be flagged with its successor. The hook SHALL log the decision IDs as `decisions` on the `openspec_text` record. No check SHALL fail on a `Governs:` target that names nothing.

Source: Brian, 2026-11-23: "i approve" (decision -> requirement or code links that the hook hands over, read from lines that already exist); plan docs/planning/links-existing-lines-2026-11-23.md

#### Scenario: An edit to a governed file gets its decisions

- **GIVEN** a file implementing a requirement, a superseded decision governing its path, an accepted decision governing the requirement's capability, and a decision governing its folder
- **WHEN** the agent edits it, edits another file in the folder, or rewrites that file with `sed -i`
- **THEN** the hook's answer gives the requirement text, then the three decisions in that order with the superseded one flagged, the log record names them under `decisions`, and a file nothing governs and nothing implements gets no answer

## MODIFIED Requirements

### Requirement: Agents get requirement text from the shell too

In a repository with OpenSpec specs and no layout plan, the edit hook SHALL answer a shell command that names or writes a file whose docstrings carry `Implements:` lines with those requirements' text, without a `permissionDecision`, and SHALL log the call as `openspec_text` with the requirement IDs; a command naming no such file and no file a decision governs SHALL get no answer.

Source: inferred by agent from the 2026-11-23 linked-chain acceptance run (Claude edited only through Bash, so the text never arrived); plan docs/planning/linked-chain-core-2026-11-23.md

#### Scenario: A shell command on an implementing file gets its requirement text

- **GIVEN** a file whose docstring says `Implements: ship/<requirement>`
- **WHEN** the agent runs `cat` on it, writes it with a heredoc, or edits it with `sed -i`
- **THEN** the hook's answer holds that requirement's text and no decision
