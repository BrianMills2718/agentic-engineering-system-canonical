# lockstep-guard Specification

## Purpose

Lockstep's edit hook judges a shell command by the paths it writes, found by code2check's shell-target parser (`src/lockstep/shell_targets.py`; `proposals/one-planning-tool/DESIGN.md`, slice 3).

## Requirements

### Requirement: Shell commands are judged by the paths they write

The edit hook SHALL find the files a shell command writes the way code2check's guard does: redirect and tee
targets read as shell words, the files `mv`, `touch`, `sed -i` and the like write, only the destination of a
copy (`cp`, `install`, `rsync`), and the paths named by code in the command (a `python -c`, a heredoc script)
only when that code calls something that writes; a `cd` in the command SHALL be followed. In block mode it
SHALL refuse a command that writes a file under a governed folder that the plan does not declare, and it
SHALL NOT refuse a command that only reads a planned file.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md, slice 3: "Port code2check's shell-target parsing. Done when lifelike replays the four cases from lockstep#111").

#### Scenario: A heredoc creating an unplanned file is refused

- **GIVEN** a governed root whose plan does not declare `newfile.py` and PCW_MODE=block
- **WHEN** a shell command is `cat > <governed>/newfile.py <<'EOF' ... EOF`
- **THEN** the hook denies it

#### Scenario: An echo redirect creating an unplanned file is refused

- **GIVEN** the same project
- **WHEN** a shell command is `echo 'x = 1' > <governed>/newfile.py`
- **THEN** the hook denies it

#### Scenario: A python one-liner creating an unplanned file is refused

- **GIVEN** the same project
- **WHEN** a shell command is `python -c "open('<governed>/newfile.py','w').write('x')"`
- **THEN** the hook denies it

#### Scenario: Copying a planned file out is allowed

- **GIVEN** the same project, with a planned file `<governed>/rule.py`
- **WHEN** a shell command is `cp <governed>/rule.py /tmp/x`
- **THEN** the hook allows it and hands over the plan text

### Requirement: A refusal lists the files the plan allows

When the edit hook refuses (or warns about) a write to a file the plan does not name, its message SHALL also list the files the plan does allow, read from whichever plan is in use (`lockstep.yaml` `layout:` rows or the planned artifacts of `.aes/target.yaml`): those in the refused file's folder first, at most 15, then "and N more".

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md); acceptance entries A2 and A3 in docs/planning/acceptance-criteria.json

#### Scenario: A refusal lists the files the plan allows

- **GIVEN** a plan that names `src/greeter/__init__.py` and PCW_MODE=block
- **WHEN** an agent writes `src/greeter/extra.py`, by an edit or by a shell command
- **THEN** the refusal message lists `src/greeter/__init__.py` under "The plan does allow these files" and no more than 15 paths, with "and N more" for the rest

### Requirement: Handing over text never approves an edit

When the edit hook lets a call through with only context (requirement text, a plan, a warning), its answer to Claude Code and to Codex SHALL carry that context without a `permissionDecision`, so the agent's own permission settings still decide whether the edit runs; a refusal SHALL keep `permissionDecision: deny` and its reason.

Source: inferred by agent: Claude Code treats a PreToolUse `allow` as approving the call without the user's prompt (probe 2026-11-23: a context-only answer with no decision still reaches the model); the template now installs the hook in every copy (plan https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/linked-chain-core-2026-11-23.md).

#### Scenario: A context-only answer carries no decision

- **GIVEN** an edit the hook lets through with requirement text
- **WHEN** the hook answers for Claude Code
- **THEN** the answer has `additionalContext` and no `permissionDecision`

### Requirement: Agents get requirement text from the shell too

In a repository with OpenSpec specs and no layout plan, the edit hook SHALL answer a shell command that names or writes a file whose docstrings carry `Implements:` lines with those requirements' text, without a `permissionDecision`, and SHALL log the call as `openspec_text` with the requirement IDs; a command naming no such file and no file a decision governs SHALL get no answer.

Source: inferred by agent from the 2026-11-23 linked-chain acceptance run (Claude edited only through Bash, so the text never arrived); plan https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/linked-chain-core-2026-11-23.md

#### Scenario: A shell command on an implementing file gets its requirement text

- **GIVEN** a file whose docstring says `Implements: ship/<requirement>`
- **WHEN** the agent runs `cat` on it, writes it with a heredoc, or edits it with `sed -i`
- **THEN** the hook's answer holds that requirement's text and no decision

### Requirement: Agents get the decisions that govern a file

In a repository with OpenSpec specs and a `docs/decisions/` folder, the edit hook SHALL hand an agent that edits a file, or names it in a shell command, each decision record whose `Governs:` line names that file, a folder above it (a target ending in `/` or naming an existing folder), or a requirement or capability the file implements, after any requirement text and without a `permissionDecision`. It SHALL read the record's existing lines only: `Governs:` (or `- Governs:`, comma separated, anchors ignored for paths), `status:` front matter or a `Status:` line, and `superseded_by:` or the text after "superseded by". Each decision SHALL be given as its ID, title, status, file and decision paragraph cut at 600 characters, at most three in full (own path first, then requirement or capability, then folder) and the rest by ID; a superseded decision SHALL be flagged with its successor. The hook SHALL log the decision IDs as `decisions` on the `openspec_text` record. No check SHALL fail on a `Governs:` target that names nothing.

Source: Brian, 2026-11-23: "i approve" (decision -> requirement or code links that the hook hands over, read from lines that already exist); plan https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/links-existing-lines-2026-11-23.md

#### Scenario: An edit to a governed file gets its decisions

- **GIVEN** a file implementing a requirement, a superseded decision governing its path, an accepted decision governing the requirement's capability, and a decision governing its folder
- **WHEN** the agent edits it, edits another file in the folder, or rewrites that file with `sed -i`
- **THEN** the hook's answer gives the requirement text, then the three decisions in that order with the superseded one flagged, the log record names them under `decisions`, and a file nothing governs and nothing implements gets no answer

### Requirement: An unplanned file is refused where the plan marks it fixed and warned about elsewhere

The edit hook SHALL refuse a write to a file under a governed folder that no `layout:` row names when the file
matches a `fixed:` glob in `lockstep.yaml` or `PCW_MODE=block` is set, showing where the file must be planned. For any
other governed file it SHALL let the write through with the refusal text as a warning and log
`"decision": "would_block"`. The template SHALL mark its package folder `fixed:`, so a fresh copy refuses an
unplanned source file.

Source: Brian, 2026-11-07, decision D7 (`lockstep` repository `.aes/plans/PLAN-014-WARN-BY-DEFAULT.yaml:5-7`):
"Lockstep warns; it blocks only files the plan marks fixed, after two weeks of would-block counts"; Brian,
2026-11-11, "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md:30`, step 4: an unplanned
write "is refused"); Brian, 2026-11-23, "i approve" to the template shipping its planned layout (back-on-design item
c). Reading the two as one rule (refuse where marked fixed, which the template does for its package) is inferred by
agent.

#### Scenario: A governed file outside every fixed glob is warned about

- **GIVEN** a governed folder with no `fixed:` glob over it and no `PCW_MODE` set
- **WHEN** an agent writes a file there that no layout row names
- **THEN** the write goes through with the refusal text as a warning and the hook log records `would_block`

#### Scenario: A file under a fixed glob is refused

- **GIVEN** a file matching a `fixed:` glob
- **WHEN** an agent writes it without a plan entry
- **THEN** the edit hook refuses the write

#### Scenario: A fresh template copy refuses an unplanned source file

- **GIVEN** a fresh copy of the template
- **WHEN** an agent writes an unplanned file in the package folder
- **THEN** the edit hook refuses it
