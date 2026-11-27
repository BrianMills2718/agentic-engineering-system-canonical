## MODIFIED Requirements

### Requirement: An unplanned file is refused where the plan marks it fixed and warned about elsewhere

The edit hook SHALL refuse a write to a file under a governed folder that no `layout:` row names when the
guard mode is `block`, or when it is `warn` and the file matches a `fixed:` glob. In other `warn` cases it
SHALL allow the write with warning context and log `would_block`. In `off` it SHALL skip edit and shell
guard checks, including fixed-file checks. The guard mode SHALL come from nonblank `PCW_MODE`, then
`guard.mode` in `lockstep.yaml`, then `warn`. Each accepts `block`, `warn` or `off`; bare YAML `true`
means block and `false` means off. The hook SHALL use block on invalid input and name invalid
`PCW_MODE`. The side-file check SHALL name an invalid `guard.mode`. The template SHALL mark its
package folder `fixed:`, so a fresh copy refuses an unplanned source file.

Source: Brian, 2026-11-07, decision D7 (`lockstep` repository `.aes/plans/PLAN-014-WARN-BY-DEFAULT.yaml:5-7`):
"Lockstep warns; it blocks only files the plan marks fixed, after two weeks of would-block counts"; Brian,
2026-11-11, "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md:30`, step 4: an unplanned
write "is refused"); Brian, 2026-11-23, "i approve" to the template shipping its planned layout (back-on-design item
c); Brian, 2026-11-25: "the whole systm should be configurable so you can congfigure what is on or off"
(docs/planning/next.goal.md, parking item `guard.mode`). Reading the first two as one rule (refuse where marked fixed,
which the template does for its package), and the order environment, then file, then warn, are inferred by agent.

#### Scenario: A governed file outside every fixed glob is warned about

- **GIVEN** a governed folder with no `fixed:` glob over it, no `guard.mode` and no `PCW_MODE` set
- **WHEN** an agent writes a file there that no layout row names
- **THEN** the write goes through with the refusal text as a warning and the hook log records `would_block`

#### Scenario: A file under a fixed glob is refused

- **GIVEN** a file matching a `fixed:` glob
- **WHEN** an agent writes it without a plan entry
- **THEN** the edit hook refuses the write

#### Scenario: A fresh template copy refuses an unplanned source file

- **GIVEN** a fresh copy of the template
- **WHEN** an agent writes an unplanned file in the package folder
- **THEN** the edit hook refuses it

#### Scenario: guard.mode block refuses an unplanned governed file

- **GIVEN** `lockstep.yaml` with `guard: {mode: block}`, no `fixed:` glob and no `PCW_MODE` set
- **WHEN** an agent writes a governed file no layout row names
- **THEN** the edit hook refuses it, and with `guard: {mode: warn}` instead the write goes through with the warning

#### Scenario: PCW_MODE overrides guard.mode

- **GIVEN** `lockstep.yaml` with `guard: {mode: block}`
- **WHEN** `PCW_MODE=warn` is set and an agent writes an unplanned governed file
- **THEN** the write goes through with the warning, and with `guard: {mode: warn}` and `PCW_MODE=block` it is refused

#### Scenario: An unknown guard mode refuses and is reported

- **GIVEN** `lockstep.yaml` with `guard: {mode: strict}`
- **WHEN** an agent writes an unplanned governed file, and `python -m lockstep.unplanned_files` runs
- **THEN** the edit hook refuses the write and the check names `guard.mode` and the value `strict`

#### Scenario: Off skips a fixed-file edit and shell write

- **GIVEN** a governed file covered by a fixed glob and no layout row for it
- **WHEN** the agent tries an edit and a shell write with `guard.mode: off`
- **THEN** the guard returns no decision, context or log for either call

#### Scenario: Invalid environment mode fails closed

- **GIVEN** a governed unplanned file with `guard.mode: warn`
- **WHEN** `PCW_MODE=strict` overrides the file setting
- **THEN** the guard refuses the edit and names the invalid environment setting
