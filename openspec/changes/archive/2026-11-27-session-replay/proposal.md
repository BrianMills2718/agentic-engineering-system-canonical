## Why

Milestone 1 step 9 of the plan "AES next steps: plan for discussion" (Brian, 2026-11-27; he told the agent to
proceed without waiting): "Replay viewer shows it all. The draft from today, moved into a git repository, with the
hand-over and wiki reads shown as their own events." Milestone 1 is done when "every step below is visible in the
replay viewer"; the plan's viewer table puts these first: the requirement text the hook handed the agent beside the
write (idea 1), hook events (idea 3) and read-before-write per edit (idea 4).

The draft (`~/projects/data/session-replay/server.py`, not in git) reads only `claude -p` stream files laid out as
`runs/<build>/build.jsonl`, drops the hand-over attachments, and cannot read Codex sessions, so it cannot show the
hand-over that step 3 proved reaches the agent.

Closes: lockstep-guard/a-session-replay-shows-each-hand-over-and-read-mark

Plan size: small

## What Changes

- New command `lockstep replay TRANSCRIPT [--repo PATH] [--store DIR] [--port N]` (module `lockstep.replay`, page
  `src/lockstep/replay.html` shipped as package data). The page is the draft's, with hand-over events, requirement
  reads and the per-write marks added and the benchmark-only folder layout removed.
- `lockstep reads` events and rows gain a `call` field (the tool call id) so the page joins each write to its row.
  The report's printed output does not change.

## Not in this slice (parking list)

- Starting a file-version recorder automatically for every session. A run that wants full file versions starts
  the draft recorder itself and passes `--store`; without it the page shows the text each call wrote.
- Planned versus unplanned files (viewer idea 2) and the requirement lens from `docs/links.json` (idea 1 beyond the
  hand-over text).

## Impact

- New: `src/lockstep/replay.py`, `src/lockstep/replay.html`, `tests/lockstep/test_replay.py`; one row in
  `check.py`'s subcommand table; `"*.html"` in the package data.
- The page loads highlight.js from cdnjs; with no network it shows plain text.
