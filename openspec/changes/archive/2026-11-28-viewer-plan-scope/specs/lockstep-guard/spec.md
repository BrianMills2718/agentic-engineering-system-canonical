## MODIFIED Requirements

### Requirement: The replay marks writes to the plan

Each replay event that wrote, and was not refused, a plan file SHALL carry `plan_write: true`; every other tool
event SHALL carry `plan_write: false`. A plan file is, by its path inside the checkout holding it (a leading `./`
dropped, letter case ignored for names and endings): `lockstep.yaml`; a document (`.md`, `.json`, `.yaml`, `.yml`,
`.txt`, `.rst`, `.adoc`, `.c4`) under `openspec/` other than `openspec/config.yaml`; or an authored document
(`.md`, `.rst`, `.txt`, `.adoc`, `.json`, `.c4`) anywhere else. A file is not a plan file when it is outside the
repository; when a folder on its path, at any depth, is `wiki`, `generated`, `tests`, `test`, `__tests__`,
`fixtures`, `node_modules`, `.venv`, `venv`, `dist`, `build`, `coverage`, `__pycache__`, `.claude`, `.agents`,
`.codex`, `.github`, `.vscode`, `.cursor` or `raw`, or holds `evidence/runs`; or when its name is
`package.json`, `package-lock.json`, `tsconfig*.json`, `jsconfig.json`, `composer.json`, `requirements*.txt`,
`constraints*.txt`, `CMakeLists.txt`, `LICENSE*` or `*.lock`. Each tool event SHALL
carry `plan_file`, true when its file is such a file, so the page marks a read of the plan by the same rule. The plan, code and
wiki view SHALL light an "agent writes the plan" arrow for a plan write, and SHALL say for the whole session whether
the first file the agent wrote was a plan file, naming that file and its time.

Source: Brian, 2026-11-28: "ok the first thing i noticed is that the agent didnt write the plan first" (on the
plan, code and wiki view of the step-5 proof session); Brian, 2026-11-28, on what counts as the plan: "i think i
thought of plan as actually all documentation/files that arent code (other than the navigational wiki) but maybe
thats not best?", then "continue through all remainign hihg condience items". Inferred by agent: generated files,
tests, dependency folders, raw source material, run evidence and config are left out although they are not code,
because a tool or another person writes them, tests have their own stage on the requirement track, and config
changes how code runs; the event field and the session line are
inferred by agent.

#### Scenario: A plan write is marked and a code write is not

- **WHEN** a session writes `lockstep.yaml`, then `src/greet.py`
- **THEN** the first write's event has `plan_write` true and the second's false
- **AND** the page holds the "agent writes the plan" arrow and the plan-first line

#### Scenario: A document write is a plan write and a generated, test, config or wiki write is not

- **WHEN** a session writes `docs/architecture/greet.md`, `generated/files.md`, `tests/test_greet.py`,
  `pyproject.toml` and `wiki/index.md`
- **THEN** only the first write's event has `plan_write` true, and only its `plan_file` is true

#### Scenario: Excluded folders match at any depth inside the checkout

- **WHEN** the replay judges `docs/a.md`, `pkg/tests/notes.md`, `data/raw/source.txt`, `evidence/runs/r1/out.json`,
  `web/package.json`, `requirements-dev.txt`, `openspec/config.yaml` and `openspec/changes/x/plan.yaml`, at the
  repository root and inside a checkout under `.claude/worktrees/`
- **THEN** only `docs/a.md` and `openspec/changes/x/plan.yaml` are plan files, in both places

#### Scenario: A spec read is a plan read and a requirement read

- **WHEN** a session reads `openspec/specs/greeter/spec.md`, then `generated/wiki/greeter.md`
- **THEN** the first event has `plan_file` and `requirement_read` true, and the second only `requirement_read`
- **AND** the page marks a plan read from `plan_file`

### Requirement: The replay shows each write's plan standing, requirement progress and the wiki read

Each replay write event other than a plan write SHALL carry `planned` (for a shell write, the worst standing of
the files it wrote, in the order below): `planned` when a `lockstep.yaml` layout row names the written file
and no write of that checkout's `lockstep.yaml` after this one added the row; `row added later` when a row names
it, no plan write before this one names it, and an edit of `lockstep.yaml` after this one added it (its new text
holds the path and its old text does not; for a diff, an added line holds it). A later document mention, or a whole
rewrite of `lockstep.yaml` whose earlier text the session does not show, never makes a write `row added later`;
`unplanned` when no row names it and a governed folder covers it; and
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
agent from the layout rows and `lockstep status`. Keeping a write `planned` when only a later document or a whole
rewrite names it is inferred by agent, after documents became plan writes: a row there at the session's start is
not shown by such a write, so it does not prove the row was added.

#### Scenario: A write before its row is added is flagged

- **WHEN** a session writes `src/extra.py`, then writes `lockstep.yaml` with a row naming it, then writes
  `src/other.py`, and the repository's `lockstep.yaml` names `src/extra.py` and governs `src/`
- **THEN** the first write's `planned` is `row added later` and the third's is `unplanned`

#### Scenario: A later document mention does not downgrade a planned write

- **WHEN** the repository's `lockstep.yaml` names `src/greet.py`, `src/extra.py` and `src/late.py`, and a session
  writes `docs/notes.md` naming `src/extra.py`, then `src/extra.py`, `src/greet.py` and `src/late.py`, then
  `docs/after.md` naming `src/greet.py` and `src/late.py`, then all of `lockstep.yaml` with a row for `src/late.py`
- **THEN** each of the three code writes is `planned`

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
