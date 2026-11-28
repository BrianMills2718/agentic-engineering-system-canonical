# lockstep-guard Specification

## Purpose

Lockstep's edit hook judges a shell command by the paths it writes, found by code2check's shell-target parser (`src/lockstep/shell_targets.py`; `proposals/one-planning-tool/DESIGN.md`, slice 3).

## Requirements

### Requirement: Shell commands are judged by the paths they write

The edit hook SHALL find the files a shell command writes the way code2check's guard does: redirect and tee
targets read as shell words, the files `mv`, `touch`, `sed -i` and the like write, only the destination of a
copy (`cp`, `install`, `rsync`), and the paths named by code in the command (a `python -c`, a heredoc script)
only when that code calls something that writes; for Python code that parses, only the paths its writing calls
target (worked out from string literals, simple assignments and `Path` joins) SHALL count, and Python code whose
write target cannot be worked out, or other code, SHALL count every path it names; a `cd` in the command SHALL be followed. In block mode it
SHALL refuse a command that writes a file under a governed folder that the plan does not declare, and it
SHALL NOT refuse a command that only reads a planned file.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md, slice 3: "Port code2check's shell-target parsing. Done when lifelike replays the four cases from lockstep#111").
The Python narrowing is inferred by agent from the 2026-11-28 Sonnet end-to-end run, where a script writing
only an OpenSpec proposal was refused because the proposal text named two planned files.

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

#### Scenario: A Python script whose written text names a planned file is not refused

- **GIVEN** the same project, with a planned file `<governed>/rule.py`
- **WHEN** a shell command is `python3 - <<'EOF'` with a script that writes `openspec/changes/x/proposal.md`
  through `pathlib.Path` and whose written text names `<governed>/rule.py` and `<governed>/newfile.py`
- **THEN** the hook does not deny it

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

The edit hook SHALL refuse a write to a file under a governed folder that no `layout:` row names when the
guard mode is `block`, or when it is `warn` and the file matches a `fixed:` glob. In other `warn` cases it
SHALL allow the write with warning context and log `would_block`. In `off` it SHALL skip edit and shell
guard checks, including fixed-file checks. The guard mode SHALL come from nonblank `PCW_MODE`, then
`guard.mode` in `lockstep.yaml`, then `warn`. Each accepts `block`, `warn` or `off`; bare YAML `true`
means block and `false` means off. The hook SHALL use block on invalid input and name invalid
`PCW_MODE`. The side-file check SHALL name an invalid `guard.mode`. The template SHALL mark its
package folder `fixed:`, so a fresh copy refuses an unplanned source file.

Source: Brian, 2026-11-07, decision D7 (`lockstep` repository `.aes/plans/PLAN-014-WARN-BY-DEFAULT.yaml:5-7`):
"Lockstep warns; it blocks only files the plan marks fixed, after two weeks of would-block counts"; Brian,
2026-11-11, "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md:30`, step 4: an unplanned
write "is refused"); Brian, 2026-11-23, "i approve" to the template shipping its planned layout (back-on-design item
c); Brian, 2026-11-25: "the whole systm should be configurable so you can congfigure what is on or off"
(docs/planning/next.goal.md, parking item `guard.mode`). Reading the first two as one rule (refuse where marked fixed,
which the template does for its package), and the order environment, then file, then warn, are inferred by agent.

#### Scenario: A governed file outside every fixed glob is warned about

- **GIVEN** a governed folder with no `fixed:` glob over it, no `guard.mode` and no `PCW_MODE` set
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

#### Scenario: guard.mode block refuses an unplanned governed file

- **GIVEN** `lockstep.yaml` with `guard: {mode: block}`, no `fixed:` glob and no `PCW_MODE` set
- **WHEN** an agent writes a governed file no layout row names
- **THEN** the edit hook refuses it, and with `guard: {mode: warn}` instead the write goes through with the warning

#### Scenario: PCW_MODE overrides guard.mode

- **GIVEN** `lockstep.yaml` with `guard: {mode: block}`
- **WHEN** `PCW_MODE=warn` is set and an agent writes an unplanned governed file
- **THEN** the write goes through with the warning, and with `guard: {mode: warn}` and `PCW_MODE=block` it is refused

#### Scenario: An unknown guard mode refuses and is reported

- **GIVEN** `lockstep.yaml` with `guard: {mode: strict}`
- **WHEN** an agent writes an unplanned governed file, and `python -m lockstep.unplanned_files` runs
- **THEN** the edit hook refuses the write and the check names `guard.mode` and the value `strict`

#### Scenario: Off skips a fixed-file edit and shell write

- **GIVEN** a governed file covered by a fixed glob and no layout row for it
- **WHEN** the agent tries an edit and a shell write with `guard.mode: off`
- **THEN** the guard returns no decision, context or log for either call

#### Scenario: Invalid environment mode fails closed

- **GIVEN** a governed unplanned file with `guard.mode: warn`
- **WHEN** `PCW_MODE=strict` overrides the file setting
- **THEN** the guard refuses the edit and names the invalid environment setting

### Requirement: A session's writes are listed with what was read first

`lockstep reads TRANSCRIPT` SHALL list, in session order, each write to a file inside the repository (`--repo`,
default the current folder) with three marks: whether the session read that file before the write; whether it
read the file's requirement context before the write, meaning the `generated/wiki/<capability>.md` page or the
`openspec/specs/<capability>/spec.md` of a capability named by the file's `Implements:` lines; and whether the
edit hook's requirement text named that file on that write. A write that created the file SHALL be marked `new`:
the Write tool's result says so, a Codex file change says `add`, and for a shell write git had not recorded the
file on any branch before the second the call was made (outside a git repository a shell write is taken as an
overwrite, and an existing file git never saw is taken as new). A file the session wrote whole (the Write tool, or
a shell write that created it) counts as read for its later writes. A call that failed before it ran (a refused
edit, a hook denial) SHALL count as neither a read nor a write; a delete SHALL not count, and a move SHALL count
only its destination. A Claude session's subagent files (`<session>/subagents/agent-*.jsonl`) SHALL be read too,
each agent measured on its own reads. Requirement context is found for Python files only, from their docstrings.
It
SHALL print one warning line for each write to an existing file with neither read, end with
`RESULT writes=N new=N file_read_first=N context_read_first=N handover=N unread=N agents=N`, give the same rows as JSON with
`--json`, and exit 0 whatever it finds; an unreadable transcript SHALL exit 2.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 4 ("Read-before-write
measured, not forced ... report it as a count and a warning, never a block"); exit codes and the `new` mark
inferred by agent.

#### Scenario: An edit after reading only the file is counted and not warned

- **WHEN** a Claude transcript reads `src/greet.py` with the Read tool and then edits it, and `src/greet.py`
  implements `greeter/the-greeter-says-hello`
- **THEN** the row is marked file read first and not context read first, no warning is printed for it, and the
  command exits 0

#### Scenario: A write with nothing read first is warned but not blocked

- **WHEN** a transcript rewrites an existing `src/greet.py` with a shell redirect and reads nothing first
- **THEN** a warning line names `src/greet.py`, the `RESULT` line counts `unread=1`, and the command exits 0

#### Scenario: Reading the wiki page counts as context

- **WHEN** a transcript runs `cat generated/wiki/greeter.md` and then edits `src/greet.py`
- **THEN** the row is marked context read first

#### Scenario: The hand-over is marked

- **WHEN** a Claude transcript has a `hook_additional_context` attachment holding Lockstep's requirement text
  right after an edit of `src/greet.py`
- **THEN** that row is marked handover

#### Scenario: A created file is new, not unread

- **WHEN** a transcript writes `src/new_mod.py` with the Write tool and the result says the file was created
- **THEN** the row is marked `new` and no warning is printed for it

#### Scenario: An unreadable transcript exits 2

- **WHEN** the transcript path does not exist
- **THEN** the command exits 2

### Requirement: Claude and Codex session files are both read

`lockstep reads` SHALL read the four session formats the agents write: a Claude Code transcript and a
`claude -p --output-format stream-json` stream (Read, Edit, MultiEdit, Write, NotebookEdit and Bash calls), and a
Codex rollout file and a `codex exec --json` stream (command executions and file changes). Shell reads SHALL be
found from the command's read commands (`cat`, `head`, `tail`, `sed` without `-i`, `nl`, `less`, `grep`, `rg`) or,
in a Codex rollout, from Codex's own `parsed_cmd` read entries. Shell writes SHALL be the sure ones the existing
shell target parser finds (redirect and tee targets, and what `mv`, `sed -i` and the like write, in a folder that
exists); paths that code inside a command merely names SHALL NOT count, because
which of them the code writes is unknown. A command's reads and writes SHALL keep the order of its simple commands,
and a Codex command's writes SHALL be found even when Codex parsed reads in it. A relative path SHALL be read
against the folder the call was made in, and paths SHALL be compared after resolving symbolic links. A record that
is not of a known shape SHALL be skipped, never stop the report.

Source: Brian, 2026-11-27, core rule "Claude and Codex behave the same" (code2-workspace `agents/core.md`,
Records); the list of read commands inferred by agent.

#### Scenario: A Codex exec stream is read

- **WHEN** a `codex exec --json` stream holds a `command_execution` of `cat src/greet.py` and then a
  `file_change` updating `src/greet.py`
- **THEN** the row is marked file read first

#### Scenario: A Codex rollout uses Codex's own read parse

- **WHEN** a Codex rollout holds a `CommandExecution` whose `parsed_cmd` has a read of `src/greet.py`, then a
  `FileChange` of that file
- **THEN** the row is marked file read first

### Requirement: A session replay shows each hand-over and read mark

`lockstep replay TRANSCRIPT [--repo PATH] [--store DIR] [--port N]` SHALL serve, on 127.0.0.1 only, a page that
steps through one Claude Code or Codex session file in order: the agent's notes, each tool call with its result,
each edit hook hand-over as an event of its own, and each read of a requirement page (`generated/wiki/`) or spec
(`openspec/specs/`) marked as a requirement read. Each write SHALL carry the marks `lockstep reads` gives that
write (file read first, requirement context read first, hand-over, unread), joined by the tool call that made it,
so the page and the report never disagree. A Claude session's subagent files SHALL be offered as further
sessions. With `--store`, the page SHALL also show each file version a recorder saved there
(`timeline.jsonl` and `blobs/<sha256>`); without it, a write shows the text the call wrote. The page SHALL ship
inside the package, so an install from git serves it. The session file SHALL be read again on each page refresh,
so a running session can be followed.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 9 ("Replay viewer
shows it all. The draft from today, moved into a git repository, with the hand-over and wiki reads shown as their
own events"); he told the agent to proceed without waiting.

#### Scenario: A Claude hand-over is its own event before its write

- **WHEN** a Claude transcript holds an edit whose `hook_additional_context` attachment names the edited file
- **THEN** the events hold a `handover` event with that text and the edit's call id, ahead of the write event
- **AND** the write event's marks say `handover`

#### Scenario: A Codex hand-over is its own event before its write

- **WHEN** a Codex rollout holds a developer message with the edit hook's text just before a file change completes
- **THEN** the events hold a `handover` event with that text ahead of the file change's write event
- **AND** the write event's marks say `handover`

#### Scenario: A write carries the read-before-write marks

- **WHEN** a session writes a file it never read
- **THEN** that write event's marks match the `lockstep reads` row for that call, with `unread` true

#### Scenario: A requirement page read is marked

- **WHEN** a session reads `generated/wiki/<capability>.md` or `openspec/specs/<capability>/spec.md`, with a read
  tool or a shell read
- **THEN** that event is marked as a requirement read

#### Scenario: The page and its data are served locally

- **WHEN** `lockstep replay` runs
- **THEN** it listens on 127.0.0.1, serves the page from the package at `/`, the sessions at `/api/sessions`, one
  session's events and file versions at `/api/data`, and a stored version at `/api/blob/<sha256>`; any other path
  or an unknown version answers 404

### Requirement: The replay has a plan, code and wiki view

The replay page SHALL offer a toggle between its timeline view and a plan, code and wiki view that steps through
the same events with the same controls. That view SHALL show the agent's current step; for the file of that step,
its `lockstep.yaml` layout row and the text of the requirements it implements (or that no row names it), its code,
and the requirement pages and specs the agent has read so far; and a band of hook cards (hand-over, refusal,
warning, read marks) marking the ones the current event shows. The server SHALL answer `/api/plan?file=<path>`
with that layout row (or null), whether a governed folder and a `fixed:` glob cover the file, and each implemented
requirement's id and text.

Source: Brian, 2026-11-28: "can you create a version of the session replay (togglable) that looks more like
file://wsl.localhost/Ubuntu-24.04/home/brian/code/inbox/ai-astronauts-hive-brain-explainer.html from the plan code
wiki page". The panes, the hook band and the plain-JSON route are inferred by agent from that page's tab 7.

#### Scenario: The plan route gives a file's row and requirement text

- **WHEN** the page asks `/api/plan?file=src/greet.py` and `lockstep.yaml` has a layout row for it that implements
  a requirement with text in `openspec/specs/`
- **THEN** the answer holds that row, `governed` and `fixed` as the plan sets them, and the requirement's id and text
- **AND** for a governed file no row names, `row` is null and `governed` is true

#### Scenario: The page offers the view as a toggle

- **WHEN** the page is served
- **THEN** it holds a toggle that switches to the plan, code and wiki view, and the timeline view is shown first

### Requirement: The replay marks writes to the plan

Each replay event that wrote `lockstep.yaml` or a file under `openspec/changes/` or `openspec/specs/`, and was not
refused, SHALL carry `plan_write: true`; every other tool event SHALL carry `plan_write: false`. The plan, code and
wiki view SHALL light an "agent writes the plan" arrow for a plan write, and SHALL say for the whole session whether
the first file the agent wrote was a plan file, naming that file and its time.

Source: Brian, 2026-11-28: "ok the first thing i noticed is that the agent didnt write the plan first" (on the
plan, code and wiki view of the step-5 proof session). Which paths count as the plan, the event field and the
session line are inferred by agent from the layout rows (`lockstep.yaml`) and OpenSpec changes being where a plan is
written.

#### Scenario: A plan write is marked and a code write is not

- **WHEN** a session writes `lockstep.yaml`, then `src/greet.py`
- **THEN** the first write's event has `plan_write` true and the second's false
- **AND** the page holds the "agent writes the plan" arrow and the plan-first line

### Requirement: The edit hook names the home of a misplaced document

When `lockstep.yaml` declares `document_homes:` and an agent writes a Markdown file that sits under no home (the
same rule as the layout check, for a file no layout row names and git does not ignore), the edit hook SHALL let the write through with a warning that names each home and
what belongs there, and log `would_block`, unless the guard mode is `block`, where it SHALL refuse the write.

Source: Brian, 2026-11-27 19:05: "research goes in one place. generated files go in another". Warn rather than
refuse by default is inferred by agent from the guard's existing default (Brian, 2026-11-07, decision D7: Lockstep
warns and blocks only what the plan marks fixed).

#### Scenario: Writing a note outside every home is warned about

- **GIVEN** `document_homes:` declaring `research/`, and guard mode `warn`
- **WHEN** an agent writes `notes.md`
- **THEN** the write goes through with a warning naming `research/` and what belongs there; writing
  `research/notes.md` gives no such warning

### Requirement: The replay shows each write's plan standing, requirement progress and the wiki read

Each replay write event other than a plan write SHALL carry `planned` (for a shell write, the worst standing of
the files it wrote, in the order below): `planned` when a `lockstep.yaml` layout row names the written file
and either no plan write in the session names it or one before this write does; `row added later` when a row names
it and only plan writes after this one name it; `unplanned` when no row names it and a governed folder covers it; and
`outside` otherwise. A plan write names a file when the text it wrote holds the file's path. The timeline SHALL flag
an `unplanned` write in orange and a `row added later` write in grey. The server SHALL answer `/api/status` with
the note on which test results were used and, for each requirement, its state from `lockstep status`, the files that
implement it and the test files tagged with its scenarios; the plan, code and wiki view SHALL show for each
requirement whether, by the current step, the session had written none of those files, its code, or its tests, and
its state now. The server SHALL answer `/api/wiki` with the paths of the pages under `generated/wiki/`, index
first; the wiki pane SHALL list them with the pages read so far highlighted. A file inside a git checkout under the
repository (a worktree the agent made there) SHALL be judged, for the plan write and requirement read marks and for
`planned`, against that checkout's `lockstep.yaml`, specs and wiki; the session data SHALL name the checkout most of
its writes went to, and `/api/status` and `/api/wiki` SHALL take it as `?checkout=`, answering 404 for a folder that
is not such a checkout.

Source: Brian, 2026-11-28: "continue through all remainign hihg condience items", on the list holding viewer ideas 2
(planned versus unplanned files, orange flag on an unplanned write), 5 (requirement status track) and 6 (the wiki as
the agent saw it). The four standings, the route names and judging against the plan as it is now are inferred by
agent from the layout rows and `lockstep status`.

#### Scenario: A write before its row is added is flagged

- **WHEN** a session writes `src/extra.py`, then writes `lockstep.yaml` with a row naming it, then writes
  `src/other.py`, and the repository's `lockstep.yaml` names `src/extra.py` and governs `src/`
- **THEN** the first write's `planned` is `row added later` and the third's is `unplanned`

#### Scenario: A write inside a worktree is judged by that worktree's plan

- **WHEN** a session works in `worktrees/feature/`, a git checkout inside the repository, writing its
  `lockstep.yaml`, a file a row there names and a file no row names
- **THEN** the first is a plan write, the second is `planned` and the third `unplanned`
- **AND** the session data names `worktrees/feature/` and `/api/wiki?checkout=worktrees/feature/` lists its index

#### Scenario: The status and wiki routes answer

- **WHEN** the page asks `/api/status` and `/api/wiki` in a repository with an implemented requirement and a
  generated wiki
- **THEN** the status answer holds the requirement with its state and its implementing file, and the wiki answer
  lists `generated/wiki/index.md` first
- **AND** the page holds the requirement track and the wiki list
