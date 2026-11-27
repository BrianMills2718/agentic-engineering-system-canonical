"""Where the project graph is: `$PROJECT_GRAPH`, else `planning.project_graph` in `lockstep.yaml` on the default
branch at origin, else the old default `~/code2/aes-config/PROJECT_GRAPH.json`.

Only the folder matters to `ship`: `graph-config.yaml` beside the graph names where the plan list lives. The value is a
local file path, never a git address, because ship reads that file from disk.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:project_graph.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: ship/the-project-graph-is-named-in-lockstep-yaml

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

Tested by: tests/lockstep/checks/test_lockstep_check_project_graph.py, tests/test_ship.py

Declares (typed signatures, from the plan):
  project_graph_problem(value: object) -> str | None
  project_graph(repo: Path) -> tuple[Path, str]
  plan_list_config(repo: Path, log: Callable[[str], None]) -> tuple[Path | None, str]
  graph_setting(key: str, env: str, config: Path) -> str | None
[[[end]]]
"""

from __future__ import annotations

import os
import re
from collections.abc import Callable
from pathlib import Path

import yaml

from lockstep.checks.config import SIDE_FILE, ConfigError, _on_default_branch

ENV = "PROJECT_GRAPH"
KEY = "project_graph"
DEFAULT = Path.home() / "code2/aes-config/PROJECT_GRAPH.json"   # the setting before 2026-11-26; tests replace it


def project_graph_problem(value: object) -> str | None:
    """Why a `planning.project_graph` value cannot be used, as a phrase, or None when it is a usable path."""
    if not isinstance(value, str) or not value.strip():
        return f"is {value!r}; it must be a path to the project graph's .json file, such as ~/settings/PROJECT_GRAPH.json"
    if "://" in value or value.startswith("git@"):
        return f"is {value!r}, a git address; it must be a local path, because ship reads graph-config.yaml from disk"
    if not value.startswith(("~", "/")):
        return f"is {value!r}, a relative path; start it with ~ or /, since ship runs in many worktrees"
    if not value.endswith(".json"):
        return f"is {value!r}; it must name the graph's .json file, whose folder holds graph-config.yaml"
    return None


def project_graph(repo: Path) -> tuple[Path, str]:
    """The project graph's path and the source that named it.

    Implements: ship/the-project-graph-is-named-in-lockstep-yaml

    Requirement text (generated):
        ship/the-project-graph-is-named-in-lockstep-yaml: `ship` SHALL find the project graph, whose
            folder holds `graph-config.yaml`, from `$PROJECT_GRAPH` when set, else from
            `planning.project_graph` in `lockstep.yaml` on the default branch at `origin` (never
            from the branch being shipped), else from `~/code2/aes-config/PROJECT_GRAPH.json`. When
            it reads the plan list it SHALL print and log `ship: project graph: <folder>
            (<source>)`, the source being `$PROJECT_GRAPH`, `lockstep.yaml planning.project_graph`
            or `default`. The value SHALL be a local path to a `.json` file starting with `~` or
            `/`; any other value (a git address, a relative path, a folder) SHALL be named by the
            side-file check and SHALL be a plan-list refusal at merge time, naming the value.

    Raises:
        ConfigError: `lockstep.yaml` on the default branch is not YAML, or names an unusable `planning.project_graph`.
    """
    named = os.environ.get(ENV)
    if named:
        return Path(named).expanduser(), f"${ENV}"
    try:
        data = yaml.safe_load(_on_default_branch(repo, SIDE_FILE))
    except yaml.YAMLError as exc:
        raise ConfigError(f"{SIDE_FILE} on the default branch is not YAML ({exc})") from exc
    planning = data.get("planning") if isinstance(data, dict) else None
    if isinstance(planning, dict) and planning.get(KEY) is not None:
        value = planning[KEY]
        problem = project_graph_problem(value)
        if problem:
            raise ConfigError(f"{SIDE_FILE} planning.{KEY} {problem}")
        return Path(value).expanduser(), f"{SIDE_FILE} planning.{KEY}"
    return DEFAULT, "default"


def plan_list_config(repo: Path, log: Callable[[str], None]) -> tuple[Path | None, str]:
    """`graph-config.yaml` beside the project graph and the source that named the graph, after printing both and passing
    the line to `log` (`ship: project graph: <folder> (<source>)`); `(None, reason)` when lockstep.yaml names an unusable graph.

    Implements: ship/the-project-graph-is-named-in-lockstep-yaml

    Requirement text (generated):
        ship/the-project-graph-is-named-in-lockstep-yaml: `ship` SHALL find the project graph, whose
            folder holds `graph-config.yaml`, from `$PROJECT_GRAPH` when set, else from
            `planning.project_graph` in `lockstep.yaml` on the default branch at `origin` (never
            from the branch being shipped), else from `~/code2/aes-config/PROJECT_GRAPH.json`. When
            it reads the plan list it SHALL print and log `ship: project graph: <folder>
            (<source>)`, the source being `$PROJECT_GRAPH`, `lockstep.yaml planning.project_graph`
            or `default`. The value SHALL be a local path to a `.json` file starting with `~` or
            `/`; any other value (a git address, a relative path, a folder) SHALL be named by the
            side-file check and SHALL be a plan-list refusal at merge time, naming the value.
    """
    try:
        graph, source = project_graph(repo)
    except ConfigError as exc:
        return None, str(exc)
    line = f"ship: project graph: {graph.parent} ({source})"
    print(line)
    log(line)
    return graph.parent / "graph-config.yaml", source


def graph_setting(key: str, env: str, config: Path) -> str | None:
    """One value from the environment variable `env`, else top-level `key:` in graph-config.yaml (`config`), else
    None. Read when needed (ship/settings-come-from-config)."""
    named = os.environ.get(env)
    if named:
        return named
    try:
        found = re.search(rf"^{re.escape(key)}:[ \t]*([^\s#]+)", config.read_text(encoding="utf-8"), re.M)
    except OSError:
        found = None
    return found.group(1) if found else None
