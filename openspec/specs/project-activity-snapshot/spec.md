# project-activity-snapshot Specification

## Purpose

Build a snapshot of where each registered project stands, read from git and GitHub: last commit, commits in 30 days, branch, uncommitted files, open pull requests, and which file to read first. A project whose checkout is not on this machine is listed as such, never guessed. The graph, the GitHub accounts and their `gh` wrappers are configuration, not code.

Source: inferred by agent from Project Meta `scripts/build_project_activity.py`, ported under Brian's 2026-11-16 "do all the steps" and D20 yes (the project graph machinery is generic and lives in AES; the records and settings are Brian's own in the private `aes-config` repository).

## Requirements

### Requirement: last-commit-per-checkout

Each project whose checkout exists SHALL show its last commit, branch and uncommitted-file count read from git; a missing checkout SHALL be reported as not on this machine; a failed GitHub lookup SHALL be recorded in the output.

#### Scenario: last-commit-per-checkout

- **WHEN** the graph holds one real checkout and one path that does not exist
- **THEN** the first row carries its last commit and the second row says it is not on this machine

### Requirement: settings-come-from-config

The owner and the map of GitHub accounts to `gh` wrappers SHALL come from `graph-config.yaml` beside the graph (the owner may also come from `PROJECT_GRAPH_OWNER`), and a missing value SHALL stop the run naming where to set it.

#### Scenario: settings-come-from-config

- **WHEN** `graph-config.yaml` names no `github_accounts`
- **THEN** the run exits naming `github_accounts` and the file to put it in
