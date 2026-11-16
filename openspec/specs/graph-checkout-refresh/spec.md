# graph-checkout-refresh Specification

## Purpose

Fetch every checkout registered in the project graph and fast-forward the ones that are clean, on their default branch and only behind. Anything else (uncommitted changes, another branch, ahead or diverged history, a lock receipt) is reported and left alone. Checkouts held 20 or more commits behind raise one keyed concern in the configured concern repository, closed when none remain.

Source: inferred by agent from Project Meta `scripts/refresh_canonical_checkouts.py`, ported under Brian's 2026-11-16 "do all the steps" and D20 yes (the project graph machinery is generic and lives in AES; the records and settings are Brian's own in the private `aes-config` repository).

## Requirements

### Requirement: never-discards-local-work

The refresh SHALL NOT reset, stash, discard or advance a checkout that is dirty, off its default branch, ahead of or diverged from upstream, or holding a lock receipt, and SHALL report each as non-canonical.

#### Scenario: never-discards-local-work

- **WHEN** a clone has an uncommitted edit and is behind upstream
- **THEN** it is not advanced and the edit is untouched

### Requirement: graph-sweep-covers-registered-checkouts

`--all-graph` SHALL refresh every shared checkout registered in the graph under $HOME, except checkouts (and repositories nested in them) that a baseline file marks as operated on in place.

#### Scenario: graph-sweep-covers-registered-checkouts

- **WHEN** the graph registers a plain checkout and an in-place mirror with a nested checkout
- **THEN** only the plain checkout is refreshed

### Requirement: stuck-checkouts-raise-a-concern

Checkouts left alone while at least the threshold behind SHALL open one keyed concern naming each; when none remain the concern SHALL be closed; a failure to route it SHALL fail the run.

#### Scenario: stuck-checkouts-raise-a-concern

- **WHEN** a dirty checkout is 25 commits behind
- **THEN** one concern is opened in the configured concern repository naming it

### Requirement: settings-come-from-config

The concern repository SHALL come from `CONCERN_REPO` or `concern_repo` in `graph-config.yaml` beside the graph, and a missing value SHALL stop the run naming where to set it.

#### Scenario: settings-come-from-config

- **WHEN** neither names a concern repository
- **THEN** the run exits naming `CONCERN_REPO` and the file
