# workspace-map-check Specification

## Purpose

Once a day, check that every top-level entry of `~/code`, `~/projects`, `~/code2` and `~/archive` is explained by the project graph or a hand-written list, and report clutter: unknown entries, duplicate clones, dirty repositories with no recent writer, stale worktrees, local-only commits, broken systemd unit paths, secret-looking files, and GitHub repositories the graph does not cover. New or changed problems open one keyed concern issue and send one phone message; a clean run closes the concern. The graph, the two hand-written lists and the settings are one person's own data in a private repository; the code is generic.

Source: inferred by agent from Project Meta `scripts/workspace_map*.py` (and `scripts/archive_map.py`), ported under Brian's 2026-11-16 "do all the steps" and D21 yes (timers become a job list; port workspace-map-check). Left out on purpose: the coordination-claims reader and the authority-snapshot check (claims retired), and the derived WORKSPACE_MAP.md and ARCHIVE_MAP.md pages and their staleness finding (Brian, 2026-11-16, D20).

## Requirements

### Requirement: settings-come-from-config

The project graph SHALL be read from `PROJECT_GRAPH` or `~/code2/aes-config/PROJECT_GRAPH.json`; `workspace_map_extras.yaml` and `archive_map_registry.yaml` SHALL be read from beside the graph (`WORKSPACE_MAP_EXTRAS` and `ARCHIVE_MAP_REGISTRY` override); the owner, the GitHub accounts and the concern repository SHALL come from the environment or `graph-config.yaml` beside the graph. A missing file or value SHALL stop the run with a message naming where to put it, and the run SHALL exit 2, not the findings code 1.

#### Scenario: settings-come-from-config

- **WHEN** the extras file is not beside the graph and `WORKSPACE_MAP_EXTRAS` is not set
- **THEN** loading stops with a message naming the expected path and `WORKSPACE_MAP_EXTRAS`

### Requirement: dependency-scan-skip-is-visible

While the dependency scanner (`check_capability_consumption.py`) is not in this repository, the check SHALL skip the `depends_on` finding and SHALL say so in the report with an INFO line, which opens no concern.

#### Scenario: dependency-scan-skip-is-visible

- **WHEN** the scanner module cannot be imported
- **THEN** the findings hold only the INFO line "dependency scan not ported yet (retirement plan step 4)", and no actionable finding

### Requirement: alert-once-per-state-change

The alert SHALL open (or comment on) the keyed concern and send one phone message only when the hash of the actionable findings differs from the stored one, stay silent while it is unchanged, and close the concern only when the stored state says it is open. The state files keep the same keys and hash format as Project Meta's.

#### Scenario: alert-once-per-state-change

- **WHEN** a run finds a new set of problems and the next run finds the same set
- **THEN** the first run files one concern and sends one message, and the second run files and sends nothing

#### Scenario: clean-run-closes-only-an-open-concern

- **WHEN** a run is clean and the stored state is not open
- **THEN** no close is filed and no message is sent

### Requirement: crash-is-not-a-finding

A crash of the check SHALL exit 2 and print CRASH, so it never looks like an ordinary day with findings (exit 1).

#### Scenario: crash-is-not-a-finding

- **WHEN** the check raises an exception
- **THEN** the wrapper exits 2 and prints "CRASH: workspace check did not finish"
