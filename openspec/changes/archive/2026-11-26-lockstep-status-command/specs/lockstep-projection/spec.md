## ADDED Requirements

### Requirement: Status lists each part with its mode and last gate result

`lockstep status --parts` SHALL print one row per AES part: each commit check named in `lockstep-checks`' check list
with its mode (`block`, `warn` or `off`, defaults as the commit checks apply them), `planning.gate` and
`planning.one_page_plans` (default `warn`), `planning.validator` and `planning.skills` only when `lockstep.yaml` sets
them, `guard.mode` (`warn (default)` when unset), and `rules` and `feedback` as `per-repository control unavailable`. Modes SHALL be read from
`lockstep.yaml` in the working tree with the same mode normalization as the hook and plugin settings, and the output SHALL say that ship reads the planning settings from the default
branch at origin. For `planning.gate` and `planning.one_page_plans` the last result SHALL be the outcome, time and short
head of the newest record (by its `time`) among `planning-verdicts/*.jsonl` in ship's log folder (`$SHIP_LOG_DIR`, else
`~/code2/.ship-logs` where `~/code2` exists, else the XDG state folder) whose `repo` is this repository's owner/name from
origin, gate `planning gate` or `one-page plans`; every other row, and a gate with no matching record, SHALL say
`no record`. A record line that is not JSON SHALL be skipped. `--json` SHALL print the rows as a JSON list. The command
SHALL exit 0, and 2 when `lockstep.yaml` cannot be read or holds a value the commit checks reject.

Source: Brian, 2026-11-25: "the whole systm should be configurable so you can congfigure what is on or off or any other settings. for any piece" (docs/planning/next.goal.md, parking item "`lockstep status` prints each part's mode and last result"). Inferred by agent: the parts table is a `--parts` flag on the existing `lockstep status` (already the requirement report), the row list, and showing a record's outcome rather than its mode text.

#### Scenario: Each part's mode comes from the working tree's settings

- **GIVEN** a repository whose `lockstep.yaml` sets `checks: {trace: warn}` and `planning: {gate: block}` and no guard
- **WHEN** `lockstep status --parts --json` runs
- **THEN** trace is `warn`, mutation is `off`, arch is `block`, `planning.gate` is `block`, `planning.one_page_plans` is `warn`, `guard.mode` is `warn (default)`, rules and feedback are `per-repository control unavailable`, and no validator row is listed

#### Scenario: The newest planning-gate record for this repository is shown

- **GIVEN** ship's log folder holding records for this repository's planning gate on two days and a newer record for another repository
- **WHEN** `lockstep status --parts` runs
- **THEN** the planning gate row shows the outcome and head of this repository's newer record, and `planning.one_page_plans` says `no record`

#### Scenario: Unreadable settings exit 2

- **GIVEN** a `lockstep.yaml` whose check mode is not block, warn or off
- **WHEN** `lockstep status --parts` runs
- **THEN** it exits 2 naming the problem
