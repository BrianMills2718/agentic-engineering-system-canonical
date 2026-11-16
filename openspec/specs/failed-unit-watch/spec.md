# failed-unit-watch Specification

## Purpose

Every 30 minutes, find systemd user units that failed (or whose last run failed), file one keyed concern issue per unit in the repository that owns the unit's script, and close it when the unit is healthy. Also sweeps Healthchecks.io checks. The owner and fallback concern repository are configuration, not code.

Source: inferred by agent from Project Meta's `scripts/failed_unit_watch.py`, ported under Brian's 2026-11-16 "do all the steps" and D21 yes (timers become a job list; port failed-unit-watch).

## Requirements

### Requirement: settings-come-from-config

The owner and the fallback concern repository SHALL come from the environment or from `graph-config.yaml` beside the project graph, and a missing value SHALL stop the run with a message naming where to set it.

#### Scenario: settings-come-from-config

- **WHEN** neither the environment nor `graph-config.yaml` names an owner
- **THEN** the script exits with "no owner named" and files nothing
