"""Tests for `lockstep accept write`, `accept check`, `run-plan` and the departure report (spec plan-run).

No model is called: every agent session is a fake runner that writes files and commits.
"""

import json
import subprocess
from pathlib import Path

import pytest

from lockstep import plan_run

CHANGE = "add-greeting"
TASKS = f"""## 1. Greeting

- [ ] 1.1 Tests first in `tests/test_app.py`
- [ ] 1.2 `greet()` in `src/app.py`
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def commit_all(repo: Path, msg: str) -> None:
    git(repo, "add", "-A")
    git(repo, "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", msg)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repository whose HEAD holds an OpenSpec change naming src/app.py and tests/test_app.py."""
    r = tmp_path / "proj"
    (r / "src").mkdir(parents=True)
    (r / "tests").mkdir()
    (r / "src" / "app.py").write_text("def greet():\n    return None\n")
    (r / "tests" / "test_app.py").write_text("def test_placeholder():\n    assert True\n")
    c = r / "openspec" / "changes" / CHANGE
    c.mkdir(parents=True)
    (c / "proposal.md").write_text("## Why\n\ngreet\n")
    (c / "tasks.md").write_text(TASKS)
    subprocess.run(["git", "init", "-q", "-b", "main", str(r)], check=True)
    git(r, "config", "user.email", "t@example.com")
    git(r, "config", "user.name", "t")
    commit_all(r, "plan")
    return r


def tick_all(wt: Path, archive: bool = False) -> None:
    t = wt / "openspec" / "changes" / CHANGE / "tasks.md"
    text = t.read_text().replace("- [ ]", "- [x]")
    if archive:
        dest = wt / "openspec" / "changes" / "archive" / f"2026-11-20-{CHANGE}"
        dest.mkdir(parents=True)
        (dest / "tasks.md").write_text(text)
        (dest / "proposal.md").write_text("x\n")
        for f in t.parent.iterdir():
            f.unlink()
        t.parent.rmdir()
    else:
        t.write_text(text)


# ---- departure report ------------------------------------------------------------------------


@pytest.mark.req("plan-run/a-file-outside-the-tasks-is-listed")
def test_file_outside_tasks_listed(repo: Path) -> None:
    base = git(repo, "rev-parse", "HEAD")
    (repo / "src" / "app.py").write_text("def greet():\n    return 'hi'\n")
    (repo / "src" / "other.py").write_text("x = 1\n")
    (repo / "tests" / "test_new.py").write_text("def test_x():\n    pass\n")
    tick_all(repo)
    commit_all(repo, "impl")
    rep = plan_run.departures(repo, CHANGE, base)
    assert rep["outside_tasks"] == ["src/other.py", "tests/test_new.py"]
    assert "src/app.py" in rep["changed"]
    assert not any(p.startswith("openspec/") for p in rep["outside_tasks"])
    assert rep["unticked"] == []


@pytest.mark.req("plan-run/a-name-added-to-tasksmd-after-ref-does-not-count")
def test_name_added_after_ref_still_listed(repo: Path) -> None:
    base = git(repo, "rev-parse", "HEAD")
    (repo / "src" / "other.py").write_text("x = 1\n")
    t = repo / "openspec" / "changes" / CHANGE / "tasks.md"
    t.write_text(t.read_text() + "- [x] 1.3 also `src/other.py`\n")
    commit_all(repo, "impl")
    assert plan_run.departures(repo, CHANGE, base)["outside_tasks"] == ["src/other.py"]


@pytest.mark.req("plan-run/an-unticked-task-is-listed-archived-or-not")
def test_unticked_task_listed_from_archive(repo: Path) -> None:
    base = git(repo, "rev-parse", "HEAD")
    tick_all(repo, archive=True)
    arch = repo / "openspec" / "changes" / "archive" / f"2026-11-20-{CHANGE}" / "tasks.md"
    arch.write_text(arch.read_text().replace("- [x] 1.2", "- [ ] 1.2"))
    commit_all(repo, "archive")
    rep = plan_run.departures(repo, CHANGE, base)
    assert rep["unticked"] == ["- [ ] 1.2 `greet()` in `src/app.py`"]


def test_basename_alone_does_not_match(repo: Path) -> None:
    """A file with the same basename as a named file, in another folder, is still outside the tasks."""
    base = git(repo, "rev-parse", "HEAD")
    (repo / "lib").mkdir()
    (repo / "lib" / "app.py").write_text("x = 1\n")
    commit_all(repo, "impl")
    assert plan_run.departures(repo, CHANGE, base)["outside_tasks"] == ["lib/app.py"]


# ---- hidden acceptance and the driver ----------------------------------------------------------

HIDDEN = "from src.app import greet\n\n\ndef test_greet():\n    assert greet() == 'hi'\n"


class FakeRunner:
    """Plays both sessions: the writer writes HIDDEN into the folder its prompt names; the implementer commits."""

    def __init__(self, leave_uncommitted: bool = False, writer_text: str = HIDDEN, transcript_extra: str = ""):
        self.calls: list[dict] = []
        self.leave_uncommitted = leave_uncommitted
        self.writer_text = writer_text
        self.transcript_extra = transcript_extra

    def __call__(self, agent: str, prompt: str, cwd: Path, transcript: Path, timeout: int,
                 env: dict | None = None, persist: bool = True) -> int:
        self.calls.append({"agent": agent, "prompt": prompt, "cwd": cwd, "env": env, "persist": persist})
        if "ACCEPTANCE TEST WRITER" in prompt:
            out = Path(prompt.split("ACCEPT_DIR=")[1].split()[0])
            (out / "test_accept_1.py").write_text(self.writer_text)
            transcript.write_text('{"type":"result"}\n')
            return 0
        # implementer: hidden tests must not be in its worktree
        assert not list(cwd.rglob("test_accept_*.py")), "hidden test visible to implementer"
        (cwd / "src" / "app.py").write_text("def greet():\n    return 'hi'\n")
        tick_all(cwd, archive=True)
        commit_all(cwd, "implement")
        if self.leave_uncommitted:
            (cwd / "src" / "app.py").write_text("def greet():\n    return 'hi'  # wip\n")
        transcript.write_text('{"type":"result"}\n' + self.transcript_extra)
        return 0


def py_test_cmd() -> str:
    return "python -m pytest -q -p no:cacheprovider"


@pytest.mark.req("plan-run/hidden-tests-are-outside-the-worktree-until-the-last-commit")
def test_hidden_tests_outside_worktree_until_last_commit(repo: Path) -> None:
    fake = FakeRunner()
    s = plan_run.run_plan(repo, CHANGE, ref="HEAD", agent="claude", runner=fake,
                          test_cmd=py_test_cmd(), check_cmd="none", timeout=60)
    run_dir = Path(s["run_dir"])
    assert (run_dir / "accept" / "test_accept_1.py").exists()
    assert not str(run_dir).startswith(str(repo))
    wt = Path(s["worktree"])
    assert not (wt / "tests" / "test_accept_1.py").exists()
    writer_cwd = fake.calls[0]["cwd"]
    assert not writer_cwd.exists()
    assert fake.calls[0]["persist"] is False and fake.calls[1]["persist"] is True
    assert s["accept"]["passed"] == 1 and s["accept"]["failed"] == 0 and s["accept"]["exit"] == 0
    assert s["uncommitted"] == 0
    assert s["head"] == git(wt, "rev-parse", "HEAD")
    assert s["check_exit"] is None
    assert s["departures"]["outside_tasks"] == []
    saved = json.loads((run_dir / "summary.json").read_text())
    assert saved["accept"] == s["accept"]
    assert (run_dir / "writer.jsonl").exists() and (run_dir / "implementer.jsonl").exists()


@pytest.mark.req("plan-run/a-hidden-test-that-passes-before-implementation-is-flagged")
def test_hidden_test_passing_before_is_flagged(repo: Path, capsys) -> None:
    fake = FakeRunner(writer_text="def test_trivial():\n    assert True\n")
    s = plan_run.accept_write(repo, CHANGE, ref="HEAD", agent="claude", runner=fake,
                              test_cmd=py_test_cmd(), timeout=60)
    assert s["accept_before"]["passed"] == 1
    assert "WARNING" in capsys.readouterr().out


@pytest.mark.req("plan-run/a-name-collision-is-refused")
def test_collision_refused(repo: Path) -> None:
    fake = FakeRunner()
    s = plan_run.accept_write(repo, CHANGE, ref="HEAD", agent="claude", runner=fake,
                              test_cmd=py_test_cmd(), timeout=60)
    (repo / "tests" / "test_accept_1.py").write_text("# mine\n")
    commit_all(repo, "own file")
    r = plan_run.accept_check(repo, CHANGE, run_dir=Path(s["run_dir"]), base=s["ref"],
                              test_cmd=py_test_cmd(), check_cmd="none")
    assert r["collisions"] == ["tests/test_accept_1.py"]
    assert (repo / "tests" / "test_accept_1.py").read_text() == "# mine\n"
    assert plan_run.exit_code(r) != 0


@pytest.mark.req("plan-run/uncommitted-work-is-reported")
def test_uncommitted_reported(repo: Path) -> None:
    s = plan_run.run_plan(repo, CHANGE, ref="HEAD", agent="claude", runner=FakeRunner(leave_uncommitted=True),
                          test_cmd=py_test_cmd(), check_cmd="none", timeout=60)
    assert s["uncommitted"] == 1


@pytest.mark.req("plan-run/the-implementer-is-not-told-where-the-tests-are")
def test_implementer_not_told(repo: Path) -> None:
    fake = FakeRunner(transcript_extra='{"cmd":"ls ~/.local/state/lockstep-runs"}\n')
    s = plan_run.run_plan(repo, CHANGE, ref="HEAD", agent="claude", runner=fake,
                          test_cmd=py_test_cmd(), check_cmd="none", timeout=60)
    impl = fake.calls[1]
    assert s["run_dir"] not in impl["prompt"] and "lockstep-runs" not in impl["prompt"]
    assert not any("lockstep-runs" in str(v) for v in (impl["env"] or {}).values())
    assert s["peek_reads"] == 1


@pytest.mark.req("plan-run/each-agent-gets-its-own-command")
def test_agent_commands(tmp_path: Path) -> None:
    argv, cwd = plan_run.agent_command("codex", "do it", tmp_path, persist=True)
    assert argv[:3] == ["codex", "exec", "--json"] and argv[argv.index("-C") + 1] == str(tmp_path)
    assert argv[-1] == "do it" and "--ephemeral" not in argv
    argv, cwd = plan_run.agent_command("claude", "do it", tmp_path, persist=True)
    assert argv[:2] == ["claude", "-p"] and "stream-json" in argv and cwd == tmp_path and argv[-1] == "do it"
    assert "--ephemeral" in plan_run.agent_command("codex", "p", tmp_path, persist=False)[0]
    assert "--no-session-persistence" in plan_run.agent_command("claude", "p", tmp_path, persist=False)[0]


@pytest.mark.req("plan-run/the-driver-does-not-merge")
def test_driver_does_not_merge(repo: Path, capsys) -> None:
    main_before = git(repo, "rev-parse", "main")
    s = plan_run.run_plan(repo, CHANGE, ref="HEAD", agent="claude", runner=FakeRunner(),
                          test_cmd=py_test_cmd(), check_cmd="none", timeout=60)
    assert git(repo, "rev-parse", "main") == main_before
    assert git(repo, "rev-parse", "--verify", s["branch"])
    assert "ship" in capsys.readouterr().out


def test_pytest_counts_parsed() -> None:
    assert plan_run.pytest_counts("2 failed, 3 passed, 1 error in 0.1s") == {"passed": 3, "failed": 2, "errors": 1}
    assert plan_run.pytest_counts("no summary") == {"passed": None, "failed": None, "errors": None}
