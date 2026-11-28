## MODIFIED Requirements

### Requirement: The replay marks writes to the plan

Each replay event that wrote, and was not refused, `lockstep.yaml`, a file under `openspec/`, or an authored
document (a file ending `.md`, `.rst`, `.txt`, `.adoc`, `.json` or `.c4`) of the checkout holding it SHALL carry
`plan_write: true`, except a file under `wiki/`, `generated/`, `tests/`, `.claude/`, `.agents/`, `.codex/` or
`.github/`, or outside the repository; every other tool event SHALL carry `plan_write: false`. Each tool event SHALL
carry `plan_file`, true when its file is such a file, so the page marks a read of the plan by the same rule. The plan, code and
wiki view SHALL light an "agent writes the plan" arrow for a plan write, and SHALL say for the whole session whether
the first file the agent wrote was a plan file, naming that file and its time.

Source: Brian, 2026-11-28: "ok the first thing i noticed is that the agent didnt write the plan first" (on the
plan, code and wiki view of the step-5 proof session); Brian, 2026-11-28, on what counts as the plan: "i think i
thought of plan as actually all documentation/files that arent code (other than the navigational wiki) but maybe
thats not best?", then "continue through all remainign hihg condience items". Inferred by agent: generated files,
tests and config are left out although they are not code, because a tool writes the first, the second has its own
stage on the requirement track, and the third changes how code runs; the event field and the session line are
inferred by agent.

#### Scenario: A plan write is marked and a code write is not

- **WHEN** a session writes `lockstep.yaml`, then `src/greet.py`
- **THEN** the first write's event has `plan_write` true and the second's false
- **AND** the page holds the "agent writes the plan" arrow and the plan-first line

#### Scenario: A document write is a plan write and a generated, test, config or wiki write is not

- **WHEN** a session writes `docs/architecture/greet.md`, `generated/files.md`, `tests/test_greet.py`,
  `pyproject.toml` and `wiki/index.md`
- **THEN** only the first write's event has `plan_write` true, and only its `plan_file` is true
