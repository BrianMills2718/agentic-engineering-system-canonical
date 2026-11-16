# project-graph-dependency-scan Specification

## Purpose

Find where one registered repository really uses another (an import of its package, a path into its folder, or a run of its command) and fill the graph's `depends_on` from that use. Report-only unless `--write`; `--write` only adds. The graph path is configuration; the capability registry is optional.

Source: inferred by agent from Project Meta scripts/check_capability_consumption.py, ported under Brian's 2026-11-16 "do all the steps" and D20 yes (the project graph machinery lives in AES; the records and settings live in the private aes-config repository).

## Requirements

### Requirement: graph-from-config

The scan SHALL read the graph named by `--project-graph`, else `PROJECT_GRAPH`, else `~/code2/aes-config/PROJECT_GRAPH.json`, resolved when the scan runs; a missing graph SHALL stop the run (exit 2) naming where to put it. The capability registry SHALL be optional (`--capability-registry` or `CAPABILITY_REGISTRY`); without one the known_consumers check is skipped and the report says so.

#### Scenario: graph-from-config

- **WHEN** `PROJECT_GRAPH` names a graph and no registry is named
- **THEN** only `undeclared_project_dependency` findings come back and the text report says the known_consumers check was skipped

### Requirement: undeclared-use-is-found

The scan SHALL report each use of another active record's package, folder or command that the consumer's `depends_on` does not list, with the evidence.

#### Scenario: undeclared-use-is-found

- **WHEN** a record's code imports a package only another record provides
- **THEN** one `undeclared_project_dependency` finding names consumer, provider and the import

### Requirement: write-only-adds

With `--write` the scan SHALL add each undeclared provider to its consumer's `depends_on` and SHALL never remove a hand-written entry.

#### Scenario: write-only-adds

- **WHEN** `--write` runs on a record with a hand-written link the scan cannot see
- **THEN** the hand-written link stays and the detected one is appended
