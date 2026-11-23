## MODIFIED Requirements

### Requirement: Requirement text is written into the implementing docstring

`lockstep check project` SHALL write the text of each requirement a docstring implements, word for word, in a marked block under its `Implements:` line, and `lockstep check project --check` SHALL fail when a block differs from the spec, writing nothing. It SHALL print one `rewrote <path>` line per file it rewrote. It SHALL preserve unrelated Python source and remain idempotent. In a repository with a layout plan it SHALL also rewrite each planned file's cog plan copy from the plan, SHALL write no block inside that copy, and SHALL do both even when no requirement statement text was read.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Opening quote line declarations receive canonical text

- **GIVEN** a docstring whose `Implements:` content starts on the opening quote line
- **WHEN** `project` runs
- **THEN** the text is written under it, other source is unchanged, and a second run changes nothing

#### Scenario: Projection rewrites the block

- **GIVEN** a spec requirement is reworded after its block was written
- **WHEN** `project` runs
- **THEN** the block holds the new wording once

#### Scenario: Stale requirement text fails the check

- **GIVEN** a block differs from the spec
- **WHEN** `project --check` runs
- **THEN** it exits 1, names the file and writes nothing

#### Scenario: A planned file's plan copy follows a reworded requirement

- **GIVEN** a layout repository whose planned file's cog plan copy is current, and its requirement is then reworded
- **WHEN** the edit hook judges the file, then `project` runs, then runs again
- **THEN** the hook finds it stale, `project` rewrites the copy with the new wording and no generated block inside it, and the second run changes nothing
