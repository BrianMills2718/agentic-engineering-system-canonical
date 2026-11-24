## ADDED Requirements

### Requirement: Sources: The statement comes before its Source line

The sources check SHALL fail when an OpenSpec requirement's first paragraph is its `Source:` line, printing
`source-first <id>` with the file, so every requirement reads statement first and the spec reader never takes an
empty statement.

Source: Brian, 2026-11-23: "i approve", to Q49 in `docs/planning/open-questions.json` ("Should every requirement put
its statement first and its `Source:` line after it, checked by `lockstep check`?").

#### Scenario: Sources: A Source line before the statement fails

- **GIVEN** a requirement whose first line under its heading is `Source: Brian, 2026-11-23: "yes"` and whose statement follows
- **WHEN** `lockstep check sources` runs
- **THEN** it prints `source-first` with that requirement's ID and exits 1, and once the statement comes first it reports nothing for it
