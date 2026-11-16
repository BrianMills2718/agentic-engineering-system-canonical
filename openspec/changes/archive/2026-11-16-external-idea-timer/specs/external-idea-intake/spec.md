# external-idea-intake Specification

## ADDED Requirements

### Requirement: A daily timer runs the digest with the project profile

A systemd user timer SHALL run `external_ideas.py` with the project profile once a day, from the refreshed clone of AES `main`, writing its output under `~/projects/data/external-ideas/`. A failed run SHALL fail the unit.

#### Scenario: daily-timer-runs-intake

- **WHEN** the unit files are read
- **THEN** the timer fires daily, and the service runs `external_ideas.py` with `--profile` from the clone of `main` and sets the output folder outside the repository
