# project-graph-sync Specification

## Purpose

Register every GitHub repository the project graph does not yet account for, so a new repository gets a record instead of sitting in a report. A new record says only what is known without a judgement (where it lives, its GitHub description or README title, status `unreviewed` until a checkout exists). The owner, homes, id prefixes, tags and `source` values are configuration, not code.

Source: inferred by agent from Project Meta scripts/project_graph_sync.py, ported under Brian's 2026-11-16 "do all the steps" and D20 yes (the project graph machinery lives in AES; the records and settings live in the private aes-config repository).

## Requirements

### Requirement: settings-come-from-config

The GitHub owner and accounts, `default_home`, `record_source` (`owner`, `other`) and the per-account `organizations` settings (`home`, `id_prefix`, `tags`, `utility_tags`) SHALL come from `graph-config.yaml` beside the project graph, and a missing value SHALL stop the run (exit 2) with a message naming where to set it, writing nothing.

Source: inferred by agent (port of Project Meta scripts/project_graph_sync.py under the D20 decision that settings are configuration, commit d000eb8c8, 2026-11-16; spec Purpose)

#### Scenario: settings-come-from-config

- **WHEN** `graph-config.yaml` has no `default_home`
- **THEN** the script exits 2 naming `default_home`, and the graph file is unchanged

### Requirement: missing-repositories-get-a-record

A non-archived GitHub repository with neither a graph record nor a reason in `workspace_map_extras.yaml` SHALL be reported, and with `--write` SHALL be added as a record built from the settings. When GitHub cannot be read, or a would-be id collides, nothing SHALL be written (exit 1).

Source: inferred by agent (port of Project Meta scripts/project_graph_sync.py, commit d000eb8c8, 2026-11-16; spec Purpose)

#### Scenario: missing-repositories-get-a-record

- **WHEN** an Inside-Success repository has no record and no checkout here
- **THEN** its record has id `repo-<name>`, the Inside-Success home path, status `unreviewed`, `source` `local-brian` and the organization's tags
