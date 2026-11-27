## MODIFIED Requirements

### Requirement: An unplanned file is refused where the plan marks it fixed and warned about elsewhere

The edit hook SHALL refuse a write to a file under a governed folder that no `layout:` row names when the file
matches a `fixed:` glob in `lockstep.yaml` or the guard mode is `block`, showing where the file must be planned. For any
other governed file it SHALL let the write through with the refusal text as a warning and log
`"decision": "would_block"`. The guard mode SHALL be `PCW_MODE` when that environment variable is set and not empty,
else `guard.mode` in `lockstep.yaml`, else `warn`; `block` and a bare YAML `true` mean block, `warn` and a bare `false`
mean warn, and any other value, or a `lockstep.yaml` that cannot be read, SHALL count as block, with
`python -m lockstep.unplanned_files` naming the bad `guard.mode`. The template SHALL mark its package folder `fixed:`,
so a fresh copy refuses an unplanned source file.

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
