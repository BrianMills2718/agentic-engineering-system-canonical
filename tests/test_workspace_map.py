"""Tests for scripts/workspace_map.py, scripts/archive_map.py and scripts/workspace_map_alert.py.

No test scans the real machine, calls GitHub, files a concern or sends a message: the check is fed rows,
the lister and scanner are stand-ins, and the alert gets an injected runner and push.
Ported from Project Meta tests/test_workspace_map.py; dropped nothing (the removed features had no tests).
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("PROJECT_GRAPH_OWNER", "BrianMills2718")  # settings are read lazily; this keeps the tests off the real config


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"scripts/{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


wm = _load("workspace_map")

GRAPH = [{"id": "factgraph", "github_repo": "BrianMills2718/factgraph"}, {"id": "vision", "github_repo": None}]
EXTRAS = {"github_not_projects": {"dotclaude": "agent configuration repository"},
          "github_not_project_patterns": [{"pattern": "-public$", "reason": "public mirror"}]}


def test_a_new_unregistered_repository_is_named():
    out = wm.github_coverage(EXTRAS, GRAPH, lister=lambda: ["factgraph", "vision", "dotclaude", "factgraph-public", "brand-new-thing"])
    assert len(out) == 1 and out[0][1] == ["brand-new-thing"]


def test_registered_explained_and_patterned_repositories_pass():
    assert wm.github_coverage(EXTRAS, GRAPH, lister=lambda: ["FactGraph", "vision", "dotclaude", "x-public"]) == []


def test_unreachable_github_is_a_loud_finding_not_silence():
    def broken():
        raise RuntimeError("gh repo list exit 1: not logged in")
    out = wm.github_coverage(EXTRAS, GRAPH, lister=broken)
    assert out and "NOT CHECKED" in out[0][0] and "not logged in" in out[0][1][0]


def _real_config():
    """The configured graph and extras (private repository), or skip where they are not present."""
    graph, extras = Path(wm.graph_path()), Path(wm.extras_path())
    if not (graph.is_file() and extras.is_file()):
        pytest.skip("no configured project graph and extras on this machine")
    return json.loads(graph.read_text()), yaml.safe_load(extras.read_text())


def test_the_configured_graph_and_extras_cover_their_own_names():
    graph, extras = _real_config()
    sample = [r["id"] for r in graph[:20] if r.get("id")] + list(extras.get("github_not_projects") or {})[:20]
    assert wm.github_coverage(extras, graph, lister=lambda: sample) == []


def test_explained_names_do_not_hide_new_repositories():
    graph, extras = _real_config()
    explained = list(extras.get("github_not_projects") or {})[:5]
    out = wm.github_coverage(extras, graph, lister=lambda: explained + ["genuinely-new-repo-zz9"])
    assert len(out) == 1 and out[0][1] == ["genuinely-new-repo-zz9"]


@pytest.mark.req("workspace-map-check/crash-is-not-a-finding")
def test_a_crash_exits_2_not_the_findings_code_1(capsys):
    """Defect: an uncaught exception exited 1, the same code as 'findings exist', so a crashed daily check looked like a normal day with problems."""
    alert = _load("workspace_map_alert")

    def boom():
        raise RuntimeError("simulated failure")
    alert.main = boom
    assert alert.run_main() == 2
    assert "CRASH: workspace check did not finish" in capsys.readouterr().err


def test_a_code2_repo_with_no_graph_record_is_named(tmp_path, monkeypatch):
    """terminal-bench-tasks and four others sat in ~/code2 with no ~/code symlink and no graph record, unseen by --check."""
    for name in ("brand-new-thing", "listed-in-extras"):
        (tmp_path / name / ".git").mkdir(parents=True)
    (tmp_path / "not-a-repo").mkdir()
    rows = [{"path": str(tmp_path / "already-seen")}]
    (tmp_path / "already-seen" / ".git").mkdir(parents=True)
    graph = tmp_path / "cfg" / "PROJECT_GRAPH.json"
    graph.parent.mkdir()
    graph.write_text("[]")
    monkeypatch.setenv("PROJECT_GRAPH", str(graph))
    extras = {"entries": {"listed-in-extras": {"kind": "app", "purpose": "x"}}}
    assert wm.unregistered_code2_repos(rows, extras, root=str(tmp_path)) == ["brand-new-thing"]


def test_an_import_missing_from_depends_on_is_named_with_its_package():
    """A repo that starts importing another repo's package is reported until the graph records the link."""
    class Result:
        findings = [
            {"kind": "undeclared_project_dependency", "consumer": "app", "provider": "llm_client", "packages": ["llm_client"]},
            {"kind": "unregistered_capability_consumer", "consumer": "app", "provider": "x"},
        ]
    assert wm.undeclared_dependency_links(lambda: Result) == ["app -> llm_client (llm_client)"]
    assert wm.dependency_findings(lambda: Result) == {wm.DEPENDENCY_TITLE: ["app -> llm_client (llm_client)"]}


@pytest.mark.req("workspace-map-check/undeclared-dependency-is-a-finding")
def test_the_real_scanner_runs_over_the_configured_graph(tmp_path, monkeypatch):
    """The placeholder INFO line is gone: the ported scanner reads the graph PROJECT_GRAPH names."""
    lib, app = tmp_path / "libx", tmp_path / "app"
    (lib / "src/libx").mkdir(parents=True)
    (lib / "src/libx/__init__.py").write_text("")
    app.mkdir()
    (app / "main.py").write_text("import libx\n")
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([{"id": "libx", "path": str(lib), "status": "active"},
                                 {"id": "app", "path": str(app), "status": "active", "depends_on": []}]))
    monkeypatch.setenv("PROJECT_GRAPH", str(graph))
    out = wm.dependency_findings()
    assert out == {wm.DEPENDENCY_TITLE: ["app -> libx (import libx)"]}
    graph.write_text(json.dumps([{"id": "libx", "path": str(lib), "status": "active"},
                                 {"id": "app", "path": str(app), "status": "active", "depends_on": ["libx"]}]))
    assert wm.dependency_findings() == {}


@pytest.mark.req("workspace-map-check/settings-come-from-config")
def test_missing_extras_file_stops_loudly(tmp_path, monkeypatch):
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text("[]")
    monkeypatch.setenv("PROJECT_GRAPH", str(graph))
    monkeypatch.delenv("WORKSPACE_MAP_EXTRAS", raising=False)
    with pytest.raises(wm.ConfigMissing, match="workspace_map_extras.yaml.*WORKSPACE_MAP_EXTRAS"):
        wm.load_extras()
    monkeypatch.setenv("PROJECT_GRAPH", str(tmp_path / "nowhere.json"))
    with pytest.raises(wm.ConfigMissing, match="nowhere.json.*PROJECT_GRAPH"):
        wm.load_graph()


def test_missing_archive_registry_stops_loudly(tmp_path, monkeypatch):
    am = _load("archive_map")
    monkeypatch.setenv("PROJECT_GRAPH", str(tmp_path / "PROJECT_GRAPH.json"))
    monkeypatch.delenv("ARCHIVE_MAP_REGISTRY", raising=False)
    assert am.registry_path() == str(tmp_path / "archive_map_registry.yaml")
    with pytest.raises(FileNotFoundError, match="ARCHIVE_MAP_REGISTRY"):
        am.load_registry()


def test_org_remotes_get_their_own_credential_helper():
    accounts = {"me": "gh-personal", "TheOrg": "gh-org", "side": "gh-personal"}
    assert wm.credential_override("git@github-personal:me/x.git", accounts, "me") == []
    assert wm.credential_override("https://github.com/side/x", accounts, "me") == []
    assert wm.credential_override("https://github.com/TheOrg/x.git", accounts, "me")[-1] == \
        "credential.https://github.com.helper=!gh-org auth git-credential"


# ---------------- the alert: once per state change ----------------

class Calls:
    def __init__(self):
        self.runs, self.pushes = [], []

    def runner(self, cmd, check=False):
        self.runs.append(cmd)

    def push(self, title, body):
        self.pushes.append((title, body))
        return {"delivered": True, "evidence": "stand-in"}


@pytest.fixture
def alert(tmp_path, monkeypatch):
    mod = _load("workspace_map_alert")
    monkeypatch.setattr(mod, "STATE_DIR", str(tmp_path / "state"))
    monkeypatch.setenv("CONCERN_REPO", "example/concerns")
    monkeypatch.setattr(mod.wm, "classify", lambda: ([{"name": "a"}], {}))
    return mod


def _findings(mod, monkeypatch, f):
    monkeypatch.setattr(mod.wm, "check", lambda rows, ex: dict(f))


@pytest.mark.req("workspace-map-check/clean-run-closes-only-an-open-concern")
def test_a_clean_run_closes_nothing_when_no_concern_is_open(alert, monkeypatch, tmp_path):
    _findings(alert, monkeypatch, {"INFO only": ["x"]})
    calls = Calls()
    assert alert.main(["--report", str(tmp_path / "r.md")], runner=calls.runner, push=calls.push) == 0
    assert calls.runs == [] and calls.pushes == []
    assert json.loads((tmp_path / "state/workspace-map-check.json").read_text()) == {"open": False, "hash": None}


@pytest.mark.req("workspace-map-check/alert-once-per-state-change")
def test_changed_findings_open_once_then_stay_silent(alert, monkeypatch, tmp_path):
    _findings(alert, monkeypatch, {"dangling symlink": ["old-link"], "INFO big dir": ["x"]})
    calls = Calls()
    report = str(tmp_path / "r.md")
    assert alert.main(["--report", report], runner=calls.runner, push=calls.push) == 1
    assert len(calls.runs) == 1 and len(calls.pushes) == 1
    cmd = calls.runs[0]
    assert cmd[2:7] == ["open", "--repo", "example/concerns", "--key", "workspace-map-check"]
    assert "--no-run-claim" in cmd and "example/concerns" in calls.pushes[0][1]
    state = json.loads((tmp_path / "state/workspace-map-check.json").read_text())
    import hashlib  # same keys and hash format as Project Meta's state files, so the existing ones keep working
    assert state == {"open": True, "hash": hashlib.sha256(json.dumps({"dangling symlink": ["old-link"]}, sort_keys=True).encode()).hexdigest()[:16]}

    assert alert.main(["--report", report], runner=calls.runner, push=calls.push) == 1  # same findings: silent
    assert len(calls.runs) == 1 and len(calls.pushes) == 1

    _findings(alert, monkeypatch, {})  # clean while open: close once, no push
    assert alert.main(["--report", report], runner=calls.runner, push=calls.push) == 0
    assert calls.runs[-1][2] == "close" and len(calls.pushes) == 1


def test_dry_run_files_nothing_and_writes_no_state(alert, monkeypatch, tmp_path):
    _findings(alert, monkeypatch, {"dangling symlink": ["old-link"]})
    calls = Calls()
    assert alert.main(["--dry-run", "--report", str(tmp_path / "r.md")], runner=calls.runner, push=calls.push) == 1
    assert calls.runs == [] and calls.pushes == [] and not (tmp_path / "state").exists()


def test_missing_concern_repo_is_a_crash_not_a_finding(alert, monkeypatch, tmp_path):
    monkeypatch.delenv("CONCERN_REPO")
    monkeypatch.setenv("PROJECT_GRAPH", str(tmp_path / "PROJECT_GRAPH.json"))
    monkeypatch.setattr(alert, "main", lambda: alert.__dict__["setting"]("concern_repo", "CONCERN_REPO"))
    assert alert.run_main() == 2


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))


@pytest.mark.req("workspace-map-check/offloaded-archive-entry-is-not-gone")
def test_an_offloaded_archive_entry_is_not_reported_gone(tmp_path, monkeypatch):
    am = _load("archive_map")
    archive = tmp_path / "archive"
    archive.mkdir()
    registry = tmp_path / "archive_map_registry.yaml"
    entry = {"purpose": "bare mirror", "why": "left the org", "restore": "rclone copyto the tar"}
    registry.write_text(yaml.safe_dump({"entries": {
        "offloaded-mirror": {**entry, "offloaded": "google_brian:Data/90_Archive/offloaded/archive/202610/offloaded-mirror-20261008T021053Z.tar.gz"},
        "really-gone": entry,
        "named-folder-not-tar": {**entry, "offloaded": "google_brian:Data/90_Archive/offloaded/archive/202610/"},
    }}))
    monkeypatch.setenv("ARCHIVE_MAP_REGISTRY", str(registry))
    monkeypatch.setattr(am, "ARCHIVE", str(archive))
    gone = [v for k, v in am.check().items() if "gone from ~/archive" in k]
    assert gone == [["really-gone", "named-folder-not-tar"]] or sorted(gone[0]) == ["named-folder-not-tar", "really-gone"]
