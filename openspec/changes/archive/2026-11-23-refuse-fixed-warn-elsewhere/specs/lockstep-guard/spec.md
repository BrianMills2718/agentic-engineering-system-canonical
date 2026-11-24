## ADDED Requirements

### Requirement: An unplanned file is refused where the plan marks it fixed and warned about elsewhere

The edit hook SHALL refuse a write to a file under a governed folder that no `layout:` row names when the file
matches a `fixed:` glob in `lockstep.yaml` or `PCW_MODE=block` is set, showing where the file must be planned. For any
other governed file it SHALL let the write through with the refusal text as a warning and log
`"decision": "would_block"`. The template SHALL mark its package folder `fixed:`, so a fresh copy refuses an
unplanned source file.

Source: Brian, 2026-11-07, decision D7 (`lockstep` repository `.aes/plans/PLAN-014-WARN-BY-DEFAULT.yaml:5-7`):
"Lockstep warns; it blocks only files the plan marks fixed, after two weeks of would-block counts"; Brian,
2026-11-11, "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md:30`, step 4: an unplanned
write "is refused"); Brian, 2026-11-23, "i approve" to the template shipping its planned layout (back-on-design item
c). Reading the two as one rule (refuse where marked fixed, which the template does for its package) is inferred by
agent.

#### Scenario: A governed file outside every fixed glob is warned about

- **GIVEN** a governed folder with no `fixed:` glob over it and no `PCW_MODE` set
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
