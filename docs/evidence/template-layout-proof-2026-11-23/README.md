# Template layout proof run, 2026-11-23

Step 6 of [the template-layout plan](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/template-layout-2026-11-23.md). Source: Brian, 2026-11-23: "i approve",
item (c) of [back-on-design](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/ddf7c9e96d4392b021756f16f4fb5c4e5919be86/docs/planning/back-on-design-2026-11-23.md).

## What was run

1. A fresh copy made from the public address after #1027 merged
   (`uvx copier copy --trust --defaults gh:BrianMills2718/agentic-engineering-system-canonical greeter`), committed.
2. One plan commit (`ffba464`): OpenSpec change `add-greeting` (requirement `greeting/greet-by-name`, two
   scenarios) plus one `layout:` row for `src/greeter/greet.py` exporting `greet(name: str) -> str`.
3. `uv run lockstep run-plan add-greeting --agent claude` (run `20261123T212157Z-0625`, exit 0).
4. [collect.py](collect.py) copied the run's records here, with machine paths replaced by `<copy>`, `<worktree>`
   and `<runs>`.

## What the files show

| Claim | File |
| --- | --- |
| Before the run, the planned file and its export are in the link file with `state: planned` | [links-at-plan-commit.json](links-at-plan-commit.json) (`src/greeter/greet.py`, `greeter.greet.greet`) |
| The implementer was told to run `uv run lockstep layout` and read the rows | [implementer-prompt.md](implementer-prompt.md) |
| The agent ran `uv run lockstep layout` (call 2) before it first wrote `greet.py` (call 7) | [tool-calls.txt](tool-calls.txt) |
| The file as `lockstep layout` wrote it holds the requirement, both scenarios, the test name and the signature | [greet-first-text.py](greet-first-text.py) |
| The hook refused the agent's shell write to the planned file (call 7, `deny shell_write`), then allowed its Edit and handed it the requirement text (21:23:29, `allow`, `text_from: openspec`) | [hook-log.jsonl](hook-log.jsonl), [tool-calls.txt](tool-calls.txt) |
| The hook refuses an unplanned file under `src/greeter/` | [hook-log.jsonl](hook-log.jsonl), last line, `tool_use_id: probe-unplanned`: a scripted probe sent after the run, because the agent never tried an unplanned file |
| The hidden tests failed before implementation (3 of 3) and passed after (3 of 3); `make check` exited 0 | [accept-before.log](accept-before.log), [accept.log](accept.log), [check-tail.log](check-tail.log), [summary.json](summary.json) |
| The departure report does not list the planned file | [summary.json](summary.json) `departures.outside_tasks` |

## Two things the run found, fixed in the same pull request

- The departure report listed `tests/test_greet.py`, which the layout row names in `tests:`, and
  `docs/specs/greeting/spec.md`, the link `make docs-specs` writes. Both are planned or generated, so the report now
  skips them (OpenSpec change `2026-11-23-departures-skip-row-tests`).
  [departures-after-fix.json](departures-after-fix.json) is the same commits re-read with the fixed code: none.
- The hook's record for an allowed edit of a planned file has no `tool` field (the 21:23:29 line); the record still
  names the file and the decision. Not changed.
