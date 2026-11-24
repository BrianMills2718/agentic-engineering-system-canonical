# workspace-map-check Specification

## Purpose

Once a day, check that every top-level entry of `~/code`, `~/projects`, `~/code2` and `~/archive` is explained by the project graph or a hand-written list, and report clutter: unknown entries, duplicate clones, dirty repositories with no recent writer, stale worktrees, local-only commits, broken systemd unit paths, secret-looking files, and GitHub repositories the graph does not cover. New or changed problems open one keyed concern issue and send one phone message; a clean run closes the concern. The graph, the two hand-written lists and the settings are one person's own data in a private repository; the code is generic.

Source: inferred by agent from Project Meta `scripts/workspace_map*.py` (and `scripts/archive_map.py`), ported under Brian's 2026-11-16 "do all the steps" and D21 yes (timers become a job list; port workspace-map-check). Left out on purpose: the coordination-claims reader and the authority-snapshot check (claims retired), and the derived WORKSPACE_MAP.md and ARCHIVE_MAP.md pages and their staleness finding (Brian, 2026-11-16, D20).

## Requirements

### Requirement: settings-come-from-config

The project graph SHALL be read from `PROJECT_GRAPH` or `~/code2/aes-config/PROJECT_GRAPH.json`; `workspace_map_extras.yaml` and `archive_map_registry.yaml` SHALL be read from beside the graph (`WORKSPACE_MAP_EXTRAS` and `ARCHIVE_MAP_REGISTRY` override); the owner, the GitHub accounts and the concern repository SHALL come from the environment or `graph-config.yaml` beside the graph. A missing file or value SHALL stop the run with a message naming where to put it, and the run SHALL exit 2, not the findings code 1.

Source: inferred by agent (port of Project Meta scripts/workspace_map*.py, commit e529a599a, 2026-11-16: graph, lists and settings from aes-config; spec Purpose)

#### Scenario: settings-come-from-config

- **WHEN** the extras file is not beside the graph and `WORKSPACE_MAP_EXTRAS` is not set
- **THEN** loading stops with a message naming the expected path and `WORKSPACE_MAP_EXTRAS`

### Requirement: undeclared-dependency-is-a-finding

The check SHALL run the dependency scanner (`scripts/check_capability_consumption.py`) over the configured project graph and SHALL report, as an actionable finding, every repository that uses another repository (import, path or command) not listed in its `depends_on`. It replaced the INFO line "dependency scan not ported yet" on 2026-11-16, when the scanner was ported (retirement plan step 4).

Source: inferred by agent (port of Project Meta scripts/workspace_map*.py, commits e529a599a and d000eb8c8, 2026-11-16; spec Purpose)

#### Scenario: undeclared-dependency-is-a-finding

- **WHEN** a graph record's code imports another record's package and its `depends_on` does not list that record
- **THEN** the findings hold "consumer -> provider (evidence)" under the depends_on title, and nothing once the link is declared

### Requirement: alert-once-per-state-change

The alert SHALL open (or comment on) the keyed concern and send one phone message only when the hash of the actionable findings differs from the stored one, stay silent while it is unchanged, and close the concern only when the stored state says it is open. The state files keep the same keys and hash format as Project Meta's.

Source: inferred by agent (port of Project Meta scripts/workspace_map_alert.py, commit e529a599a, 2026-11-16; spec Purpose)

#### Scenario: alert-once-per-state-change

- **WHEN** a run finds a new set of problems and the next run finds the same set
- **THEN** the first run files one concern and sends one message, and the second run files and sends nothing

#### Scenario: clean-run-closes-only-an-open-concern

- **WHEN** a run is clean and the stored state is not open
- **THEN** no close is filed and no message is sent

### Requirement: crash-is-not-a-finding

A crash of the check SHALL exit 2 and print CRASH, so it never looks like an ordinary day with findings (exit 1).

Source: inferred by agent (port of Project Meta scripts/workspace_map*.py, commit e529a599a, 2026-11-16; spec Purpose)

#### Scenario: crash-is-not-a-finding

- **WHEN** the check raises an exception
- **THEN** the wrapper exits 2 and prints "CRASH: workspace check did not finish"

### Requirement: offloaded-archive-entry-is-not-gone

An `archive_map_registry.yaml` entry whose folder is absent from `~/archive` SHALL be reported as gone unless the
entry names, in `offloaded:`, the exact Google Drive tar (a path ending in `.tar.gz`) that holds the folder.
Source: inferred by agent from Brian's 2026-11-17 request to correct the archive registry's missing bare mirrors.

#### Scenario: offloaded-archive-entry-is-not-gone

- **WHEN** a registry entry's folder is absent from `~/archive` and the entry names `offloaded: google_brian:Data/90_Archive/offloaded/archive/202610/x-20261008T000000Z.tar.gz`
- **THEN** the check reports no "gone" finding for it, while an absent entry with no `offloaded:` is still reported as gone
