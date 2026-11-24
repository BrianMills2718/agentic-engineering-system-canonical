# project-graph-taxonomy Specification

## Purpose

Check the shape of the project graph: required fields, controlled vocabularies, unique ids and paths, references that resolve, and that each record's `github_repo` matches the origin remote of the checkout it points at. With `--fail-on hard` only the structural errors fail the run; descriptive findings are reported but do not. The graph path is configuration, not code.

Source: inferred by agent from Project Meta `scripts/check_project_graph_taxonomy.py`, ported under Brian's 2026-11-16 "do all the steps" and D20 yes (the project graph machinery is generic and lives in AES; the records and settings are Brian's own in the private `aes-config` repository).

## Requirements

### Requirement: graph-path-is-configured

With no `--project-graph` argument the checker SHALL read the graph named by the `PROJECT_GRAPH` environment variable, else `~/code2/aes-config/PROJECT_GRAPH.json`.

Source: inferred by agent (port of Project Meta scripts/check_project_graph_taxonomy.py under the D20 decision that the graph path is configuration, commit d01400338, 2026-11-16; spec Purpose)

#### Scenario: graph-path-is-configured

- **WHEN** `PROJECT_GRAPH` names a graph file and the checker is run with no path argument
- **THEN** it validates that file

### Requirement: records-are-validated

Each record SHALL be checked against the taxonomy (ids, paths, one-liner length, portfolio area, utility tags, cross-references, origin remote) and every violation SHALL be listed.

Source: inferred by agent (port of Project Meta scripts/check_project_graph_taxonomy.py, commit d01400338, 2026-11-16; spec Purpose)

#### Scenario: records-are-validated

- **WHEN** a record has a dangling reference, a bad vocabulary value or a mismatched remote
- **THEN** the run reports it and exits 1

### Requirement: hard-errors-block

With `--fail-on hard` only deterministic structural errors SHALL make the run fail; other findings SHALL be counted as measured and not block.

Source: inferred by agent (port of Project Meta scripts/check_project_graph_taxonomy.py, commit d01400338, 2026-11-16; spec Purpose: --fail-on hard)

#### Scenario: hard-errors-block

- **WHEN** a record has a dangling `depends_on` id
- **THEN** `--fail-on hard` exits 1 and lists it under hard errors
