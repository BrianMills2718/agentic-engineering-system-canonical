## MODIFIED Requirements

### Requirement: The docs site shows coverage at its commit

`lockstep check project` SHALL write `docs/status.md` in a repository with a `docs/` folder and recognized OpenSpec requirements, listing every requirement and scenario with the state `lockstep status` gives when no test run is recorded, and `--check` SHALL fail when the page is stale.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Status page lists every requirement with its coverage state

- **GIVEN** a repository with `docs/`
- **WHEN** `project` runs
- **THEN** `docs/status.md` lists every requirement and scenario with its state

#### Scenario: Stale status page fails the check

- **GIVEN** a test is added after the page was written
- **WHEN** `project --check` runs
- **THEN** it names `docs/status.md`
