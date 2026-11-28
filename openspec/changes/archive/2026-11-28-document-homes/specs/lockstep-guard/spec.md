## ADDED Requirements

### Requirement: The edit hook names the home of a misplaced document

When `lockstep.yaml` declares `document_homes:` and an agent writes a Markdown file that sits under no home (the
same rule as the layout check, for a file no layout row names and git does not ignore), the edit hook SHALL let the write through with a warning that names each home and
what belongs there, and log `would_block`, unless the guard mode is `block`, where it SHALL refuse the write.

Source: Brian, 2026-11-27 19:05: "research goes in one place. generated files go in another". Warn rather than
refuse by default is inferred by agent from the guard's existing default (Brian, 2026-11-07, decision D7: Lockstep
warns and blocks only what the plan marks fixed).

#### Scenario: Writing a note outside every home is warned about

- **GIVEN** `document_homes:` declaring `research/`, and guard mode `warn`
- **WHEN** an agent writes `notes.md`
- **THEN** the write goes through with a warning naming `research/` and what belongs there; writing
  `research/notes.md` gives no such warning
