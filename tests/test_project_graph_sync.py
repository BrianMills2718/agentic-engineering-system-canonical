"""project_graph_sync: what counts as missing, and what a new record says.

Ported from Project Meta tests/test_project_graph_sync.py; the settings that were constants there are passed as
the `cfg` the script reads from graph-config.yaml. The refresh tests that file also held are in
tests/test_project_graph_refresh.py. No test calls GitHub.
"""
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import project_graph_sync as sync  # noqa: E402

CFG = {"owner": "BrianMills2718", "default_home": "/home/brian/code2/{name}",
       "record_source": {"owner": "brian-built", "other": "local-brian"},
       "organizations": {"Inside-Success": {"home": "/home/brian/code2/inside-success/repos/{name}", "id_prefix": "repo-",
                                            "tags": ["inside-success"], "utility_tags": ["inside-success-repo"]}}}


def row(full, **kw):
    return {"name": full.split("/")[1], "nameWithOwner": full, "isArchived": False, "pushedAt": "2026-11-01T00:00:00Z", **kw}


GRAPH = [{"id": "x", "github_repo": "BrianMills2718/x"}, {"id": "repo-y", "github_repo": "Inside-Success/y"}]
EXTRAS = {"github_not_projects": {"skipme": "copy", "Inside-Success/frozen": "frozen copy"},
          "github_not_project_patterns": [{"pattern": "-public$", "reason": "mirror"}]}


def names(repos):
    return [r["nameWithOwner"] for r in sync.missing_repos(GRAPH, EXTRAS, repos, "BrianMills2718")]


@pytest.mark.req("project-graph-sync/missing-repositories-get-a-record")
def test_a_new_repo_in_any_account_is_missing():
    assert sorted(names([row("BrianMills2718/new"), row("Inside-Success/new2")])) == ["BrianMills2718/new", "Inside-Success/new2"]


def test_recorded_explained_and_mirrors_are_not_missing():
    repos = [row("BrianMills2718/x"), row("Inside-Success/y"), row("BrianMills2718/skipme"),
             row("Inside-Success/frozen"), row("BrianMills2718/x-public")]
    assert names(repos) == []


def test_an_org_repo_is_not_covered_by_a_personal_record_of_the_same_name():
    assert names([row("Inside-Success/x")]) == ["Inside-Success/x"]


def test_a_personal_copy_of_an_org_repo_is_covered():
    assert names([row("BrianMills2718/y")]) == []


def test_archived_repos_are_not_required():
    assert names([row("BrianMills2718/old", isArchived=True)]) == []


@pytest.mark.req("project-graph-sync/missing-repositories-get-a-record")
def test_new_record_is_unreviewed_without_a_checkout_and_names_its_source():
    rec = sync.new_record(row("Inside-Success/no-such-repo-zz", description="Does a thing"), set(), "2026-11-05", CFG)
    assert rec["id"] == "repo-no-such-repo-zz" and rec["status"] == "unreviewed" and rec["one_liner"] == "Does a thing"
    assert rec["path"] == "/home/brian/code2/inside-success/repos/no-such-repo-zz" and "area-unreviewed" in rec["utility_tags"]
    assert rec["source"] == "local-brian" and "inside-success" in rec["tags"] and "inside-success-repo" in rec["utility_tags"]


def test_an_owner_repo_is_brian_built_and_another_account_is_local():
    assert sync.new_record(row("BrianMills2718/no-such-repo-zz"), set(), "d", CFG)["source"] == "brian-built"
    other = sync.new_record(row("never-absolute/no-such-repo-zz"), set(), "d", CFG)
    assert other["source"] == "local-brian" and other["id"] == "no-such-repo-zz"
    assert other["path"] == "/home/brian/code2/no-such-repo-zz" and "inside-success" not in other["tags"]


def test_new_record_without_a_description_says_it_was_not_reviewed():
    rec = sync.new_record(row("BrianMills2718/no-such-repo-zz"), set(), "2026-11-05", CFG, title="Title")
    assert rec["one_liner"] == "Title (README title; purpose not yet reviewed)"


def test_id_collision_falls_back_to_the_owner_then_raises():
    assert sync.new_record(row("BrianMills2718/a"), {"a"}, "d", CFG)["id"] == "brianmills2718-a"
    with pytest.raises(ValueError):
        sync.new_record(row("BrianMills2718/a"), {"a", "brianmills2718-a"}, "d", CFG)


def test_a_folder_with_another_remote_is_not_this_repos_checkout(tmp_path):
    clone = tmp_path / "thing"
    subprocess.run(["git", "init", "-q", str(clone)], check=True)
    subprocess.run(["git", "-C", str(clone), "remote", "add", "origin", "https://github.com/BrianMills2718/thing.git"], check=True)
    assert sync.is_checkout_of(str(clone), "brianmills2718/thing")
    assert not sync.is_checkout_of(str(clone), "Inside-Success/thing")
    assert not sync.is_checkout_of(str(tmp_path / "absent"), "BrianMills2718/thing")


def test_a_folder_taken_by_another_repo_of_that_name_gets_an_owner_prefixed_path():
    rec = sync.new_record(row("never-absolute/tmp-exists-probe"), set(), "d", {**CFG, "default_home": "/tmp/{name}"})
    assert rec["path"] == "/tmp/tmp-exists-probe"
    rec = sync.new_record(row("someone/tmp"), set(), "d", {**CFG, "default_home": "/{name}"})  # /tmp is no checkout of someone/tmp
    assert rec["path"] == "/someone-tmp" and rec["status"] == "unreviewed"


def _config_dir(tmp_path, cfg, monkeypatch):
    monkeypatch.setenv("PROJECT_GRAPH", str(tmp_path / "PROJECT_GRAPH.json"))  # main() sets it too; this restores it after
    (tmp_path / "PROJECT_GRAPH.json").write_text("[]\n")
    (tmp_path / "workspace_map_extras.yaml").write_text("github_not_projects: {}\n")
    (tmp_path / "graph-config.yaml").write_text(yaml.safe_dump(cfg))
    return tmp_path / "PROJECT_GRAPH.json"


@pytest.mark.req("project-graph-sync/settings-come-from-config")
def test_a_missing_setting_stops_loudly_and_writes_nothing(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("PROJECT_GRAPH_OWNER", raising=False)
    graph = _config_dir(tmp_path, {"owner": "me", "github_accounts": {"me": "gh"}, "record_source": {"owner": "a", "other": "b"}}, monkeypatch)
    monkeypatch.setattr(sync.wm, "list_repo_details", lambda: [row("me/new")])
    assert sync.main(["--graph", str(graph), "--write"]) == 2
    assert "default_home" in capsys.readouterr().err and graph.read_text() == "[]\n"


@pytest.mark.req("project-graph-sync/settings-come-from-config")
def test_write_adds_records_using_the_configured_settings(tmp_path, monkeypatch):
    monkeypatch.delenv("PROJECT_GRAPH_OWNER", raising=False)
    graph = _config_dir(tmp_path, {**CFG, "owner": "me", "github_accounts": {"me": "gh"}, "default_home": str(tmp_path / "h/{name}")}, monkeypatch)
    monkeypatch.setattr(sync.wm, "list_repo_details", lambda: [row("me/new", description="New thing")])
    assert sync.main(["--graph", str(graph), "--write"]) == 0
    records = yaml.safe_load(graph.read_text())
    assert [(r["id"], r["source"], r["path"]) for r in records] == [("new", "brian-built", str(tmp_path / "h/new"))]


def test_unreadable_github_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.delenv("PROJECT_GRAPH_OWNER", raising=False)
    graph = _config_dir(tmp_path, {**CFG, "owner": "me", "github_accounts": {"me": "gh"}}, monkeypatch)

    def down():
        raise RuntimeError("gh repo list me exit 1")
    monkeypatch.setattr(sync.wm, "list_repo_details", down)
    assert sync.main(["--graph", str(graph), "--write"]) == 1 and graph.read_text() == "[]\n"
