## Why

Brian, 2026-11-28, watching a proof session in the plan, code and wiki view: "ok the first thing i noticed is that
the agent didnt write the plan first". The view lights an arrow when the agent reads the plan, but a write to
`lockstep.yaml` or an OpenSpec change shows only as an ordinary file write, so a plan-first session and a
code-first session look the same. The end-to-end runs of Milestone 1 have to show which one happened.

Closes: lockstep-guard/the-replay-marks-writes-to-the-plan

Plan size: small

## What Changes

- Each event that wrote `lockstep.yaml` or a file under `openspec/changes/` or `openspec/specs/` carries
  `plan_write: true`.
- The plan, code and wiki view lights an "agent writes the plan" arrow for such a step and shows the plan file in
  the plan pane.
- The view says, for the whole session, whether the first file the agent wrote was a plan file, and names it.

## Impact

- `src/lockstep/replay.py`, `src/lockstep/replay.html`, `tests/lockstep/test_replay.py`.
