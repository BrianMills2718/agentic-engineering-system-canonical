# project-graph-config Specification

## Purpose

Keep one person's list of repositories and settings out of the shared machinery, so the same checks run for anyone who supplies their own two files (retirement plan, step 4).

Source: Brian, 2026-11-16, "i approve d20" (Decision 20 yes) after "the project graph is somethign that is cofnigruable for aes. so that is basically my specific configuration". Inferred by agent: the settings are a `graph-config.yaml` beside the graph, with an environment variable override.

## Requirements

### Requirement: The checks read the graph and owner from the person's own files

`md_file_cap.py` SHALL read the project graph from the `PROJECT_GRAPH` environment variable, else from `~/code2/project-graph/PROJECT_GRAPH.json`, and the GitHub owner to check from `PROJECT_GRAPH_OWNER`, else from `owner:` in `graph-config.yaml` beside the graph. It SHALL exit with a message naming both when no owner is set, and SHALL NOT assume a default owner.

#### Scenario: owner-from-config

- **WHEN** a graph folder holds `graph-config.yaml` with `owner: someone` and no environment override
- **THEN** only graph entries whose GitHub owner is `someone` are checked

#### Scenario: no-owner-fails-loudly

- **WHEN** neither the environment variable nor the settings file names an owner
- **THEN** the run exits with a message naming `PROJECT_GRAPH_OWNER` and the settings file path
