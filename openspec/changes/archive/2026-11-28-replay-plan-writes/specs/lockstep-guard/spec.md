## ADDED Requirements

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
