## ADDED Requirements

### Requirement: The project graph is named in lockstep.yaml

`ship` SHALL find the project graph, whose folder holds `graph-config.yaml`, from `$PROJECT_GRAPH` when set, else from `planning.project_graph` in `lockstep.yaml` on the default branch at `origin` (never from the branch being shipped), else from `~/code2/aes-config/PROJECT_GRAPH.json`. When it reads the plan list it SHALL print and log `ship: project graph: <folder> (<source>)`, the source being `$PROJECT_GRAPH`, `lockstep.yaml planning.project_graph` or `default`. The value SHALL be a local path to a `.json` file starting with `~` or `/`; any other value (a git address, a relative path, a folder) SHALL be named by the side-file check and SHALL be a plan-list refusal at merge time, naming the value.

Source: Brian, 2026-11-25: "yes it should hold all 4 parts btu the whole systm should be configurable so you can congfigure what is on or off or any other settings. for any piece" (docs/planning/next.goal.md, parking item "`planning.project_graph` replaces the `~/code2/aes-config` default"). Inferred by agent: the value is a local path (ship reads `graph-config.yaml` from disk), the old default stays so nothing changes the day it lands, and the environment keeps winning so tests and timers that set it are unchanged.

#### Scenario: planning.project_graph on the default branch names the graph

- **GIVEN** `lockstep.yaml` on the default branch saying `planning: {project_graph: ~/settings/PROJECT_GRAPH.json}` and no `$PROJECT_GRAPH`
- **WHEN** ship reads the plan list
- **THEN** it reads `~/settings/graph-config.yaml` and prints `ship: project graph: ~/settings (lockstep.yaml planning.project_graph)` with `~` expanded; the same key on the branch being shipped only is ignored

#### Scenario: The environment wins over lockstep.yaml

- **GIVEN** `$PROJECT_GRAPH` set and `planning.project_graph` on the default branch
- **WHEN** ship reads the plan list
- **THEN** it uses `$PROJECT_GRAPH` and names it as the source

#### Scenario: With neither the old default is used

- **GIVEN** no `$PROJECT_GRAPH` and no `planning.project_graph`
- **WHEN** ship reads the plan list
- **THEN** it uses `~/code2/aes-config/PROJECT_GRAPH.json` and names `default` as the source

#### Scenario: An unusable planning.project_graph is refused

- **GIVEN** `planning.project_graph` is a git address, a relative path, a folder or not a string
- **WHEN** ship reads the plan list, or the side-file check runs
- **THEN** ship stops with a plan-list refusal naming `planning.project_graph` and the value, nothing is pushed, and the side-file check names the same problem

## MODIFIED Requirements

### Requirement: settings-come-from-config

Where the plan list lives SHALL be read when it is needed: from `$SHIP_PERSONAL_VPS` and `$SHIP_PLAN_LIST`
when set, else from the top-level `plan_list_checkout:` and `plan_list_path:` keys of `graph-config.yaml`
beside the project graph (found as requirement `the-project-graph-is-named-in-lockstep-yaml` says). When either
is not named, a new repository with a package SHALL be refused with a message naming both keys; nothing is
pushed. No other run reads them.

Source: inferred by agent from the AES consolidation plan item 7 task: AES is public, so a person's repository names and paths are their configuration in their private settings repository, as for the project-graph machinery.

#### Scenario: A new repository with no plan list named is refused

- **GIVEN** a new repository with a package, and neither the environment nor `graph-config.yaml` naming the plan list
- **WHEN** ship runs
- **THEN** it exits 1, says no plan list is named and names `plan_list_checkout`, and the branch is not on the remote

#### Scenario: The plan list location is read from graph-config

- **GIVEN** `graph-config.yaml` naming `plan_list_checkout:` and `plan_list_path:`
- **WHEN** ship reads the settings
- **THEN** it returns those values, an environment variable wins over the file, and a key named nowhere is none
