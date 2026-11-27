"""Where ship finds the project graph: `$PROJECT_GRAPH`, else `planning.project_graph` on the default branch, else the
old default (src/lockstep/checks/project_graph.py)."""

import subprocess
from pathlib import Path

import pytest

import lockstep.checks.project_graph as pg
from lockstep.checks.config import ConfigError, planning_modes
from lockstep.side_file import side_file_problems


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A clone whose origin's main holds no lockstep.yaml yet; PROJECT_GRAPH unset; the default is a test path."""
    monkeypatch.delenv("PROJECT_GRAPH", raising=False)
    monkeypatch.setattr(pg, "DEFAULT", tmp_path / "default" / "PROJECT_GRAPH.json")
    remote, work = tmp_path / "remote.git", tmp_path / "work"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(work)], check=True)
    _git(work, "config", "user.email", "t@example.com")
    _git(work, "config", "user.name", "t")
    (work / "a.txt").write_text("a\n")
    _git(work, "add", "-A")
    _git(work, "commit", "-q", "-m", "base")
    _git(work, "remote", "add", "origin", str(remote))
    _git(work, "push", "-q", "origin", "main")
    _git(work, "fetch", "-q", "origin")
    return work


def _on_main(work: Path, text: str) -> None:
    (work / "lockstep.yaml").write_text(text)
    _git(work, "add", "-A")
    _git(work, "commit", "-q", "-m", "settings")
    _git(work, "push", "-q", "origin", "main")
    _git(work, "fetch", "-q", "origin")


@pytest.mark.req("ship/planning-project-graph-on-the-default-branch-names-the-graph")
def test_the_default_branch_setting_names_the_graph(repo, tmp_path):
    _on_main(repo, "planning:\n  project_graph: ~/settings/PROJECT_GRAPH.json\n")
    said = []
    config, source = pg.plan_list_config(repo, said.append)
    assert config == Path.home() / "settings" / "graph-config.yaml"
    assert source == "lockstep.yaml planning.project_graph"
    assert said == [f"ship: project graph: {Path.home() / 'settings'} (lockstep.yaml planning.project_graph)"]


@pytest.mark.req("ship/planning-project-graph-on-the-default-branch-names-the-graph")
def test_a_branch_cannot_name_its_own_graph(repo):
    _git(repo, "checkout", "-q", "-b", "feature")
    (repo / "lockstep.yaml").write_text("planning:\n  project_graph: /elsewhere/PROJECT_GRAPH.json\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "branch setting")
    assert pg.project_graph(repo) == (pg.DEFAULT, "default")


@pytest.mark.req("ship/the-environment-wins-over-lockstep-yaml")
def test_the_environment_wins_over_lockstep_yaml(repo, tmp_path, monkeypatch):
    _on_main(repo, "planning:\n  project_graph: ~/settings/PROJECT_GRAPH.json\n")
    monkeypatch.setenv("PROJECT_GRAPH", str(tmp_path / "env" / "PROJECT_GRAPH.json"))
    assert pg.project_graph(repo) == (tmp_path / "env" / "PROJECT_GRAPH.json", "$PROJECT_GRAPH")


@pytest.mark.req("ship/with-neither-the-old-default-is-used")
def test_with_neither_the_old_default_is_used(repo):
    assert pg.project_graph(repo) == (pg.DEFAULT, "default")
    _on_main(repo, "planning:\n  gate: warn\n")
    said = []
    assert pg.plan_list_config(repo, said.append) == (pg.DEFAULT.parent / "graph-config.yaml", "default")
    assert said == [f"ship: project graph: {pg.DEFAULT.parent} (default)"]


@pytest.mark.req("ship/an-unusable-planning-project-graph-is-refused")
@pytest.mark.parametrize("value, phrase", [
    ("git@github.com:o/settings.git", "git address"),
    ("https://example.com/PROJECT_GRAPH.json", "git address"),
    ("settings/PROJECT_GRAPH.json", "relative path"),
    ("~/settings", ".json file"),
    ("''", "must be a path"),
    ("[a, b]", "must be a path"),
])
def test_an_unusable_value_is_refused(repo, value, phrase):
    _on_main(repo, f"planning:\n  project_graph: {value}\n")
    with pytest.raises(ConfigError, match="planning.project_graph"):
        pg.project_graph(repo)
    config, why = pg.plan_list_config(repo, lambda line: None)
    assert config is None and phrase in why


@pytest.mark.req("ship/an-unusable-planning-project-graph-is-refused")
def test_the_side_file_check_names_an_unusable_value(tmp_path):
    (tmp_path / "lockstep.yaml").write_text(
        "schema: lockstep.side.v1\nplanning:\n  project_graph: settings/PROJECT_GRAPH.json\n")
    problems = side_file_problems(tmp_path, {})
    assert any("planning.project_graph" in p and "relative path" in p for p in problems)
    (tmp_path / "lockstep.yaml").write_text(
        "schema: lockstep.side.v1\nplanning:\n  project_graph: ~/settings/PROJECT_GRAPH.json\n")
    assert not any("project_graph" in p for p in side_file_problems(tmp_path, {}))


@pytest.mark.req("ship/planning-project-graph-on-the-default-branch-names-the-graph")
def test_the_planning_modes_accept_the_key():
    assert planning_modes({"planning": {"project_graph": "~/s/PROJECT_GRAPH.json"}}) == {
        "gate": planning_modes({})["gate"], "one_page_plans": planning_modes({})["one_page_plans"]}
