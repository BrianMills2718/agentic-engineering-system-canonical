# project-graph-refresh Specification

## Purpose

The daily job that keeps the project graph and the "My projects" page current: register new repositories, refill `depends_on`, check the graph's shape, land a changed graph in the private settings repository that holds it, then rebuild the activity snapshot and the page and push both to the page repository's data branch.

Source: inferred by agent from Project Meta scripts/project_graph_refresh.py (rewritten small for the new layout; the project-meta clone, landing through ship and the ten derived pages are dropped), ported under Brian's 2026-11-16 "do all the steps" and D20 yes (the project graph machinery lives in AES; the records and settings live in the private aes-config repository).

## Requirements

### Requirement: step-log

Each step SHALL be timed and appended to one log per day (`project-graph-refresh-YYYY-MM-DD.log`) with its name, command, exit status, seconds and output, in this order: register new repositories, fill `depends_on`, taxonomy check, land the graph, activity snapshot, page, publish. A failed `depends_on` scan SHALL be reported and the run SHALL carry on; any other failed step SHALL stop the run.

#### Scenario: step-log

- **WHEN** a step exits 3
- **THEN** the day's log holds `step=<name> exit=3` and its output, and the run stops with that step named

### Requirement: graph-lands-in-settings-repo

The steps SHALL work on a staging copy of the graph. Only when the copy differs from the live graph after the taxonomy check passes SHALL the job copy it over the live file, commit that one file with the configured `git_identity` and `git push origin HEAD:main` in the settings repository, never through a pull request and never forced. The settings repository SHALL be on main and clean before the run (then `pull --ff-only`) and clean after the commit; otherwise nothing is committed or pushed and the problem is reported, and the page still goes out.

#### Scenario: graph-lands-in-settings-repo

- **WHEN** a new record was registered and the settings repository is clean
- **THEN** its main gains one commit changing only `PROJECT_GRAPH.json`, authored by the configured identity

### Requirement: page-goes-to-data-branch

The activity snapshot and the page SHALL be rebuilt from the staged graph and pushed to the configured data branch of the page repository (`docs/plans/project_activity.json`, `docs/plans/project-graph.review.html`), never to its main; the data branch starts with no history the first time.

#### Scenario: page-goes-to-data-branch

- **WHEN** two daily runs publish
- **THEN** the data branch holds exactly those two files in two commits and main is unchanged

### Requirement: failure-opens-one-concern

A run with problems SHALL open (or comment on) the keyed concern `project-graph-refresh` in the configured concern repository through `scripts/concern_issue.py`; a clean run SHALL close it.

#### Scenario: failure-opens-one-concern

- **WHEN** a run ends with a problem
- **THEN** `concern_issue.py open` is called with the configured repository, key `project-graph-refresh` and every required argument

### Requirement: no-push-changes-nothing

With `--no-push` every step SHALL run but nothing SHALL be committed or pushed, the live graph SHALL stay unchanged, and no concern SHALL be opened or closed.

#### Scenario: no-push-changes-nothing

- **WHEN** `--no-push` runs and a new record is registered
- **THEN** the settings repository and the page repository are unchanged and no concern call is made
