"""build_project_activity reads each project's state from git; a missing checkout is reported, never guessed."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_project_activity", ROOT / "scripts/build_project_activity.py")
bpa = importlib.util.module_from_spec(spec)
sys.modules["build_project_activity"] = bpa
spec.loader.exec_module(bpa)


ACCOUNTS = {"BrianMills2718": "gh-personal"}


def _no_github(monkeypatch):
    """Settings are named and both GitHub lookups are stubbed, so a test never reaches the network."""
    monkeypatch.setenv("PROJECT_GRAPH_OWNER", "BrianMills2718")
    monkeypatch.setattr(bpa, "github_accounts", lambda graph=None: ACCOUNTS)
    monkeypatch.setattr(bpa, "github_facts", lambda accounts: ({}, "stubbed: no network in tests"))


@pytest.mark.req("project-activity-snapshot/last-commit-per-checkout")
def test_checkout_state_and_missing_path(tmp_path, monkeypatch):
    _no_github(monkeypatch)
    repo = tmp_path / "alpha"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    (repo / "README.md").write_text("alpha\n")
    (repo / "STATE.md").write_text("now\n")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "first"], check=True)
    (repo / "scratch.txt").write_text("x\n")
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([
        {"id": "alpha", "path": str(repo), "github_repo": "BrianMills2718/alpha"},
        {"id": "elsewhere", "path": str(tmp_path / "not-here"), "github_repo": "BrianMills2718/elsewhere"},
    ]))
    monkeypatch.setattr(bpa, "open_prs_by_repo", lambda accounts: ({"brianmills2718/alpha": 2}, None))

    out = bpa.build(graph)

    alpha, elsewhere = out["projects"]
    assert alpha["last_commit_subject"] == "first" and alpha["commits_30d"] == 1 and alpha["branch"] == "main"
    assert alpha["uncommitted_files"] == 1 and alpha["entry_doc"] == "README.md" and alpha["state_doc"] == "STATE.md"
    assert alpha["open_prs"] == 2
    assert elsewhere == {"id": "elsewhere", "open_prs": 0, "on_this_machine": False}
    assert out["summary"]["on_this_machine"] == 1 and "open_prs_error" not in out


@pytest.mark.req("project-activity-snapshot/last-commit-per-checkout")
def test_failed_pr_lookup_is_recorded(tmp_path, monkeypatch):
    _no_github(monkeypatch)
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([{"id": "x", "path": None}]))
    monkeypatch.setattr(bpa, "open_prs_by_repo", lambda accounts: (None, "gh search prs exit 1: offline"))
    out = bpa.build(graph)
    assert out["open_prs_error"].endswith("offline") and "open_prs" not in out["projects"][0]


@pytest.mark.req("project-activity-snapshot/last-commit-per-checkout")
def test_a_git_call_that_hangs_reads_as_empty(monkeypatch):
    """One stuck checkout must not stall the whole snapshot past the refresh's step limit (2026-11-05)."""
    def hang(*a, **k):
        assert k.get("timeout") == bpa.GIT_TIMEOUT
        raise subprocess.TimeoutExpired(a[0], k["timeout"])
    monkeypatch.setattr(bpa.subprocess, "run", hang)
    assert bpa.git("/nowhere", "status", "--porcelain") == ""


@pytest.mark.req("project-activity-snapshot/settings-come-from-config")
def test_missing_accounts_setting_stops_loudly_naming_where_to_set_it(tmp_path):
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text("[]")
    with pytest.raises(SystemExit) as stop:
        bpa.github_accounts(graph)
    assert "github_accounts" in str(stop.value) and str(tmp_path / "graph-config.yaml") in str(stop.value)


@pytest.mark.req("project-activity-snapshot/settings-come-from-config")
def test_accounts_and_owner_are_read_beside_the_graph(tmp_path, monkeypatch):
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text("[]")
    (tmp_path / "graph-config.yaml").write_text("owner: Someone\ngithub_accounts:\n  Someone: gh-someone\n  Org: gh-org\n")
    monkeypatch.delenv("PROJECT_GRAPH_OWNER", raising=False)
    assert bpa.github_accounts(graph) == {"Someone": "gh-someone", "Org": "gh-org"}
    assert bpa.github_owner(graph) == "Someone"
