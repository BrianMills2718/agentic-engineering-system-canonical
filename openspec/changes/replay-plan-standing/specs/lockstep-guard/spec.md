## ADDED Requirements

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
