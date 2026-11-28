## Why

Brian, 2026-11-28: "can you create a version of the session replay (togglable) that looks more like
file://wsl.localhost/Ubuntu-24.04/home/brian/code/inbox/ai-astronauts-hive-brain-explainer.html from the plan code
wiki page". That page (tab 7, "Plan, code, wiki") draws the plan, the code and the wiki as three panes, the agent
above them, and the hooks and checks as a band below, with arrows for who reads and who writes. The replay today
shows a reading pane and a writing pane, so the plan row and requirement behind a write are not on screen.

Closes: lockstep-guard/the-replay-has-a-plan-code-and-wiki-view

Plan size: small

## What Changes

- The replay page gets a toggle between the current timeline view and a plan, code and wiki view. The new view
  steps through the same events with the same controls: the agent and its current step on top; the file's plan
  row and requirement text, the file's code, and the requirement pages and specs read so far as three panes; and
  a band of the hook cards (hand-over, refusal, warning, read marks) lit by the current event.
- The server answers `/api/plan?file=<path>` with that file's `lockstep.yaml` layout row, whether a governed folder
  or a `fixed:` glob covers it, and the text of the requirements it implements.
- Colors are blue, orange and grey, not the explainer's red and green.

## Impact

- `src/lockstep/replay.py`, `src/lockstep/replay.html`, `tests/lockstep/test_replay.py`.
