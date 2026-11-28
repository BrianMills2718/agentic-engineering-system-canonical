"""`lockstep replay TRANSCRIPT`: one session stepped through in order, with hand-overs and read marks.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:replay.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-guard/a-session-replay-shows-each-hand-over-and-read-mark

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

Tested by: tests/lockstep/test_replay.py

Declares (typed signatures, from the plan):
  session_events(transcript: Path, root: Path) -> list[dict]
  make_server(transcript: Path, root: Path, store: Path | None, port: int) -> ThreadingHTTPServer
  main(argv: list[str] | None = None) -> int
[[[end]]]
"""
