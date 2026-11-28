## ADDED Requirements

### Requirement: A session's writes are listed with what was read first

`lockstep reads TRANSCRIPT` SHALL list, in session order, each write to a file inside the repository (`--repo`,
default the current folder) with three marks: whether the session read that file before the write; whether it
read the file's requirement context before the write, meaning the `generated/wiki/<capability>.md` page or the
`openspec/specs/<capability>/spec.md` of a capability named by the file's `Implements:` lines; and whether the
edit hook's requirement text was attached to that write. A write that created the file SHALL be marked `new`. It
SHALL print one warning line for each write to an existing file with neither read, end with
`RESULT writes=N new=N file_read_first=N context_read_first=N handover=N unread=N`, give the same rows as JSON with
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
in a Codex rollout, from Codex's own `parsed_cmd` read entries; shell writes SHALL be found by the existing shell
target parser (`lockstep.shell_targets.written_paths`).

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
