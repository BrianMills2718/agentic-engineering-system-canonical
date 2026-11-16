"""project_graph_refresh: step order, the step log, landing in the settings repository, the data branch, the concern.

Rewritten with the script from Project Meta tests/test_project_graph_sync.py (its refresh tests). The step runner is
injected or the git remotes are local bare repositories in tmp_path: no network, no real repository, no concern filed.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import project_graph_refresh as refresh  # noqa: E402

S = {"concern_repo": "owner/concerns", "ssh_host_alias": "github-x", "graph_page.repo": "owner/workspace",
     "graph_page.data_branch": "shaping/project-graph-data", "graph_page.viewer": "/viewer.js",
     "git_identity.name": "Test Person", "git_identity.email": "test@example.invalid", "remote": "unused"}


def git(*a):
    return subprocess.run(["git", *a], check=True, capture_output=True, text=True).stdout


@pytest.fixture
def where(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh, "LOG_DIR", tmp_path / "logs")
    monkeypatch.setattr(refresh, "RUNTIME", tmp_path / "runtime")
    return tmp_path


def settings_repo(tmp_path):
    """A bare origin and a clone of it holding PROJECT_GRAPH.json, as aes-config does."""
    origin, clone = tmp_path / "config.git", tmp_path / "config"
    git("init", "--bare", "-q", "-b", "main", str(origin))
    git("clone", "-q", str(origin), str(clone))
    (clone / "PROJECT_GRAPH.json").write_text("[]\n")
    (clone / "graph-config.yaml").write_text("owner: me\n")
    git("-C", str(clone), "add", ".")
    git("-C", str(clone), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "seed")
    git("-C", str(clone), "push", "-q", "origin", "HEAD:main")
    return origin, clone


class Fake(refresh.Run):
    """Records each step; `fail` names steps that exit 1; `edit` steps write a new record into the staged graph."""

    def __init__(self, log_dir, fail=(), edit=(), real=()):
        super().__init__(log_dir)
        self.steps, self.fail, self.edit, self.real = [], set(fail), set(edit), set(real)

    def __call__(self, name, cmd, cwd=None, check=True, timeout=900):
        self.steps.append(name)
        if name in self.real or name.startswith("graph-repo") or name.endswith("-graph"):
            return super().__call__(name, cmd, cwd, check, timeout)
        if name in self.fail:
            if check:
                raise refresh.StepFailed(f"{name} exit 1: boom")
            return subprocess.CompletedProcess(cmd, 1, "", "boom")
        if name in self.edit:
            graph = Path(cmd[cmd.index("--graph") + 1])
            graph.write_text(json.dumps(json.loads(graph.read_text()) + [{"id": "new"}], indent=2) + "\n")
        return subprocess.CompletedProcess(cmd, 1 if name == "diff-data" else 0, "", "")


def run_refresh(monkeypatch, where, live, push=True, **fake):
    monkeypatch.setattr(refresh, "prepare_workspace", lambda run, s: where / "workspace")
    monkeypatch.setattr(refresh, "prepare_data_branch", lambda run, s: where / "data")
    run = Fake(where / "logs", **fake)
    return refresh.refresh(run, push=push, live=live, s=S), run.steps


@pytest.mark.req("project-graph-refresh/step-log")
def test_refresh_stops_at_the_first_failed_step_and_logs_it(where):
    run = refresh.Run()
    assert run("ok", [sys.executable, "-c", "print('hello')"]).returncode == 0
    with pytest.raises(refresh.StepFailed, match="bad exit 3.*broken"):
        run("bad", [sys.executable, "-c", "import sys; print('broken'); sys.exit(3)"])
    log = run.log_path.read_text()
    assert run.log_path.name == f"project-graph-refresh-{time.strftime('%Y-%m-%d')}.log"
    assert "step=ok exit=0 seconds=" in log and "step=bad exit=3" in log and "hello" in log and "broken" in log


def test_a_timeout_kills_the_workers_too(tmp_path):
    marker = tmp_path / "child.pid"
    child = f"import subprocess,time;p=subprocess.Popen(['sleep','30']);open(r'{marker}','w').write(str(p.pid));time.sleep(30)"
    with pytest.raises(subprocess.TimeoutExpired):
        refresh.run_group([sys.executable, "-c", child], None, 2)
    pid = int(marker.read_text())
    time.sleep(0.3)
    state = Path(f"/proc/{pid}/stat").read_text().split()[2] if os.path.exists(f"/proc/{pid}") else "gone"
    assert state in ("gone", "Z")


def test_steps_run_in_order_and_a_failed_scan_does_not_stop_the_page(where, monkeypatch):
    _, clone = settings_repo(where)
    problems, steps = run_refresh(monkeypatch, where, clone / "PROJECT_GRAPH.json", fail={"fill-depends-on"})
    assert len(problems) == 1 and "boom" in problems[0]
    order = ["register-new-repositories", "fill-depends-on", "taxonomy", "activity", "page", "push-data"]
    assert [s for s in steps if s in order] == order


def test_a_failed_taxonomy_stops_the_run_and_leaves_the_live_graph_alone(where, monkeypatch):
    _, clone = settings_repo(where)
    live = clone / "PROJECT_GRAPH.json"
    with pytest.raises(refresh.StepFailed):
        run_refresh(monkeypatch, where, live, edit={"register-new-repositories"}, fail={"taxonomy"})
    assert live.read_text() == "[]\n" and git("-C", str(clone), "status", "--porcelain") == ""


def test_an_unchanged_graph_commits_nothing(where, monkeypatch):
    origin, clone = settings_repo(where)
    before = git("-C", str(origin), "rev-parse", "main")
    problems, steps = run_refresh(monkeypatch, where, clone / "PROJECT_GRAPH.json")
    assert problems == [] and "commit-graph" not in steps and git("-C", str(origin), "rev-parse", "main") == before


@pytest.mark.req("project-graph-refresh/graph-lands-in-settings-repo")
def test_a_changed_graph_is_committed_and_pushed_to_main_with_the_configured_identity(where, monkeypatch):
    origin, clone = settings_repo(where)
    problems, steps = run_refresh(monkeypatch, where, clone / "PROJECT_GRAPH.json", edit={"register-new-repositories"})
    assert problems == [] and steps.index("push-graph") < steps.index("page")
    assert json.loads(git("-C", str(origin), "show", "main:PROJECT_GRAPH.json")) == [{"id": "new"}]
    assert git("-C", str(origin), "log", "-1", "--format=%an <%ae>", "main").strip() == "Test Person <test@example.invalid>"
    assert git("-C", str(origin), "diff", "--name-only", "main~1", "main").split() == ["PROJECT_GRAPH.json"]


@pytest.mark.req("project-graph-refresh/graph-lands-in-settings-repo")
def test_a_dirty_settings_repo_is_never_committed_or_pushed(where, monkeypatch):
    origin, clone = settings_repo(where)
    (clone / "graph-config.yaml").write_text("owner: someone-else-is-editing\n")
    before = git("-C", str(origin), "rev-parse", "main")
    problems, steps = run_refresh(monkeypatch, where, clone / "PROJECT_GRAPH.json", edit={"register-new-repositories"})
    assert len(problems) == 1 and "uncommitted changes" in problems[0] and "page" in steps
    assert "commit-graph" not in steps and git("-C", str(origin), "rev-parse", "main") == before
    assert (clone / "PROJECT_GRAPH.json").read_text() == "[]\n"


@pytest.mark.req("project-graph-refresh/no-push-changes-nothing")
def test_no_push_runs_every_step_but_commits_pushes_and_files_nothing(where, monkeypatch):
    origin, clone = settings_repo(where)
    before = git("-C", str(origin), "rev-parse", "main")
    problems, steps = run_refresh(monkeypatch, where, clone / "PROJECT_GRAPH.json", push=False,
                                  edit={"register-new-repositories"})
    assert problems == [] and {"register-new-repositories", "fill-depends-on", "taxonomy", "activity", "page"} <= set(steps)
    assert not {"graph-repo-pull", "commit-graph", "push-graph", "commit-data", "push-data"} & set(steps)
    assert git("-C", str(origin), "rev-parse", "main") == before and (clone / "PROJECT_GRAPH.json").read_text() == "[]\n"
    filed = []
    monkeypatch.setattr(refresh, "settings", lambda: S)
    monkeypatch.setattr(refresh, "refresh", lambda run, push, live, s, scan: [])
    monkeypatch.setattr(refresh, "report", lambda *a: filed.append(a))
    assert refresh.main(["--no-push"]) == 0 and filed == []


@pytest.mark.req("project-graph-refresh/page-goes-to-data-branch")
def test_data_branch_starts_empty_then_adds_commits_without_touching_main(where):
    origin, seed = where / "origin.git", where / "seed"
    git("init", "--bare", "-q", "-b", "main", str(origin))
    git("init", "-q", "-b", "main", str(seed))
    (seed / "code.py").write_text("x")
    git("-C", str(seed), "add", ".")
    git("-C", str(seed), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "seed")
    git("-C", str(seed), "push", "-q", str(origin), "main")
    main = git("-C", str(origin), "rev-parse", "main")
    s = {**S, "remote": str(origin)}
    branch = s["graph_page.data_branch"]
    for day in ("one", "two"):
        run = refresh.Run()
        path = refresh.prepare_data_branch(run, s)
        (path / refresh.PAGE).write_text(day)
        (path / refresh.ACTIVITY).write_text(day)
        refresh.publish_data(run, path, day, True, branch)
    assert git("-C", str(origin), "rev-parse", "main") == main
    assert git("-C", str(origin), "ls-tree", "-r", "--name-only", branch).split() == sorted([refresh.PAGE, refresh.ACTIVITY])
    assert git("-C", str(origin), "show", f"{branch}:{refresh.PAGE}") == "two"
    assert git("-C", str(origin), "rev-list", "--count", branch).strip() == "2"
    assert git("-C", str(origin), "log", "-1", "--format=%ae", branch).strip() == "test@example.invalid"


@pytest.mark.req("project-graph-refresh/failure-opens-one-concern")
def test_concern_arguments_are_accepted_by_the_real_tool(where):
    """The first real run of the old job failed here: the call left out required arguments."""
    import re
    tool = Path(refresh.__file__).parent / "concern_issue.py"
    seen = []

    class Record(refresh.Run):
        def __call__(self, name, cmd, cwd=None, check=True, timeout=900):
            seen.append(cmd)
            return subprocess.CompletedProcess(cmd, 0, "", "")

    refresh.report(Record(), [sys.executable, str(tool)], ["boom"], S["concern_repo"])
    refresh.report(Record(), [sys.executable, str(tool)], [], S["concern_repo"])
    required = set(re.findall(r'add_argument\("(--[a-z-]+)", required=True', tool.read_text()))
    for cmd in seen:
        action = cmd[2]
        needed = {"--repo", "--key"} | ({"--title", "--body", "--source"} if action == "open" else {"--evidence"})
        assert needed <= required and needed <= set(cmd)
        assert cmd[cmd.index("--repo") + 1] == "owner/concerns" and cmd[cmd.index("--key") + 1] == "project-graph-refresh"


def test_a_missing_setting_stops_loudly(where, monkeypatch, capsys):
    (where / "g").mkdir()
    (where / "g/PROJECT_GRAPH.json").write_text("[]\n")
    (where / "g/graph-config.yaml").write_text("concern_repo: o/r\n")
    monkeypatch.setenv("PROJECT_GRAPH", str(where / "g/PROJECT_GRAPH.json"))
    assert refresh.main(["--no-push"]) == 2
    err = capsys.readouterr().err
    assert "graph_page.viewer" in err and "git_identity.email" in err
