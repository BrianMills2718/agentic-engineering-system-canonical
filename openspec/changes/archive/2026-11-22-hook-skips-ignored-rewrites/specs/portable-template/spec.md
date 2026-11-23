## ADDED Requirements

### Requirement: The commit check stages rewritten files that git tracks

The `lockstep-fast` pre-commit job of a copy SHALL stage each file `lockstep check project` reports as rewritten,
except a file git ignores, and SHALL then run `make fast`. An ignored rewritten file SHALL NOT make the commit fail.

#### Scenario: An ignored status page does not block a commit

- **GIVEN** a copy whose `.gitignore` lists `docs/status.md`
- **WHEN** the job runs and `lockstep check project` reports `rewrote docs/status.md` and `rewrote src/demo/a.py`
- **THEN** the job exits 0, `src/demo/a.py` is staged and `docs/status.md` is not
