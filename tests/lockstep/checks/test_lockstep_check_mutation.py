"""`lockstep check mutation`: mutmut survivors by module, a broken run fails, one agent issue; per repository."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from lockstep.checks import mutation as mutation_report
from lockstep.checks.cli import run as run_check


RESULTS = """    lockstep.checks.suppressions.x_check__mutmut_1: survived
    lockstep.checks.suppressions.x_check__mutmut_2: survived
    lockstep.checks.suppressions.x_check__mutmut_3: killed
    lockstep.plan.xǁPlanǁload__mutmut_4: survived
    lockstep.plan.x_read__mutmut_5: killed
    lockstep.plan.x_read__mutmut_6: killed
"""


@pytest.fixture(autouse=True)
def own_state(tmp_path, monkeypatch):
    """Never touch a real repository's kept state, and never find a real mutmut on PATH or a real origin."""
    monkeypatch.setattr(mutation_report, "state_dir", lambda tree: tmp_path)
    monkeypatch.setattr(mutation_report.shutil, "which", lambda name: None)
    monkeypatch.setattr(mutation_report, "_origin", lambda tree: ("x", "y"))


class Done:
    def __init__(self, rc=0, out=""):
        self.returncode, self.stdout, self.stderr = rc, out, ""


def tree(tmp_path: Path) -> Path:
    """A folder with a `.venv/bin/mutmut` the fakes stand in for."""
    (tmp_path / ".venv" / "bin").mkdir(parents=True)
    (tmp_path / ".venv" / "bin" / "mutmut").write_text("")
    return tmp_path


def fake(monkeypatch, run=Done(), results=RESULTS, log=None):
    def go(cmd, **_):
        if log is not None:
            log.append(cmd)
        if cmd[1] == "results":
            return Done(0, results() if callable(results) else results)
        if cmd[1] == "show":
            return Done(0, f"--- a\n+++ b\n-{cmd[2]}\n")
        if cmd[:3] == ["gh", "issue", "list"]:
            return Done(0, json.dumps(fake.open))
        if cmd[:3] == ["gh", "issue", "create"]:
            fake.open = [{"number": 9}]
            return Done(0, "https://github.com/x/y/issues/9")
        return Done()
    fake.open = []
    monkeypatch.setattr(mutation_report.subprocess, "run", go)

    def run_mutmut(cmd, cwd, env, timeout):
        if log is not None:
            log.append(cmd)
        if run is None:  # stopped at the limit
            return None, "", timeout
        return run.returncode, run.stdout, 1
    monkeypatch.setattr(mutation_report, "run_mutmut", run_mutmut)


@pytest.mark.req("lockstep-checks/mutation-lists-surviving-mutants-per-repository", existing=True)
def test_survivors_are_grouped_by_module(tmp_path, monkeypatch, capsys):
    fake(monkeypatch)
    assert mutation_report.main(["--repo", str(tree(tmp_path))]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0] == "lockstep.checks.suppressions: 2 survived"
    assert out[1] == "lockstep.plan: 1 survived"
    assert out[-1].startswith("mutation: 3 survived, 3 killed of 6 mutants")


@pytest.mark.req("lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure", existing=True)
def test_survivors_do_not_fail_the_night(tmp_path, monkeypatch):
    fake(monkeypatch, results="    lockstep.a.x_f__mutmut_1: survived\n")
    assert mutation_report.main(["--repo", str(tree(tmp_path))]) == 0


@pytest.mark.req("lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure", existing=True)
def test_a_test_failing_in_mutmuts_copy_is_named(tmp_path, monkeypatch, capsys):
    fake(monkeypatch, run=Done(1, "FAILED tests/lockstep/test_x.py::test_y - AssertionError\nfailed to collect stats.\n"))
    assert mutation_report.main(["--repo", str(tree(tmp_path))]) == 2
    last = capsys.readouterr().out.splitlines()[-1]
    assert last.startswith("mutation: could not run:") and "tests/lockstep/test_x.py::test_y" in last


@pytest.mark.req("lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure", existing=True)
def test_a_run_stopped_at_the_limit_fails_only_without_progress(tmp_path, monkeypatch, capsys):
    (tmp_path / "last-not-checked.json").write_text(json.dumps({"stopped": False, "unchecked": 0}))
    five = "".join(f"    lockstep.a.x_f__mutmut_{i}: not checked\n" for i in range(5)) + "    lockstep.a.x_g__mutmut_1: killed\n"
    fake(monkeypatch, run=None, results=five)
    t = str(tree(tmp_path / "t"))
    assert mutation_report.main(["--repo", t, "--timeout", "5"]) == 0
    assert "the next run continues" in capsys.readouterr().out
    assert mutation_report.main(["--repo", t, "--timeout", "5"]) == 2
    assert capsys.readouterr().out.startswith("mutation: could not run: stopped at the 5s limit twice")
    four = five.split("\n", 1)[1]
    fake(monkeypatch, run=None, results=four)
    assert mutation_report.main(["--repo", t, "--timeout", "5"]) == 0


@pytest.mark.req("lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure", existing=True)
def test_an_unreadable_results_file_is_set_aside(tmp_path, monkeypatch, capsys):
    t = tree(tmp_path / "t")
    src = t / "mutants" / "src"
    src.mkdir(parents=True)
    for name, text in [("a.py.meta", '{"exit_code_by_key": {"a": 1'), ("a.py", "x = 1"), ("a.py.spans", "[]"),
                       ("b.py.meta", '{"exit_code_by_key": {}}'), ("b.py", "y = 1")]:
        (src / name).write_text(text)
    fake(monkeypatch)
    assert mutation_report.main(["--repo", str(t)]) == 0
    # all three of a.py's files move, so mutmut makes its mutants again; b.py is left alone
    assert sorted(p.name for p in src.iterdir()) == ["a.py.broken", "a.py.meta.broken", "a.py.spans.broken",
                                                      "b.py", "b.py.meta"]
    assert "set aside unreadable mutants/src/a.py.meta" in capsys.readouterr().out


@pytest.mark.req("lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure", existing=True)
def test_set_aside_files_are_made_again_by_mutmut(tmp_path):
    """mutmut itself: with the mutated copy moved too, the next run makes and checks the file's mutants again."""
    mutmut = Path(os.environ.get("MUTMUT_BIN", Path(sys.executable).parent / "mutmut"))
    if not mutmut.exists():
        pytest.skip("no mutmut (set MUTMUT_BIN, or install the mutation extra)")
    proj = tmp_path / "p"
    (proj / "src" / "pkg").mkdir(parents=True)
    (proj / "tests").mkdir()
    (proj / "src" / "pkg" / "__init__.py").write_text("")
    (proj / "src" / "pkg" / "a.py").write_text("def add(x, y):\n    return x + y\n")
    (proj / "tests" / "test_a.py").write_text("from pkg.a import add\n\ndef test_add():\n    assert add(2, 3) == 5\n")
    (proj / "pyproject.toml").write_text('[tool.mutmut]\npaths_to_mutate = ["src/"]\n'
                                         'pytest_add_cli_args_test_selection = ["tests/"]\n'
                                         '[tool.pytest.ini_options]\npythonpath = ["src"]\n')

    def results():
        subprocess.run([str(mutmut), "run", "--max-children", "2"], cwd=proj, capture_output=True, timeout=300)
        out = subprocess.run([str(mutmut), "results", "--all", "true"], cwd=proj, capture_output=True, text=True,
                             timeout=120).stdout
        return mutation_report.parse_results(out)

    first = results()
    assert first
    meta = next((proj / "mutants").rglob("a.py.meta"))
    meta.write_text(meta.read_text()[:10])
    assert mutation_report.set_aside_broken(proj)
    assert results().keys() == first.keys()


@pytest.mark.req("lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure", existing=True)
def test_the_limit_stops_mutmuts_whole_process_group(tmp_path):
    started = tmp_path / "child.pid"
    rc, _, secs = mutation_report.run_mutmut(
        ["bash", "-c", f"sleep 60 & echo $! > {started}; wait"], tmp_path, dict(os.environ), 1)
    assert rc is None and secs < 30
    pid = int(started.read_text())
    time.sleep(0.2)
    assert not Path(f"/proc/{pid}").exists() or "Z" in Path(f"/proc/{pid}/stat").read_text().split()[2]


@pytest.mark.req("lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure", existing=True)
def test_no_mutmut_or_no_results_fails(tmp_path, monkeypatch, capsys):
    assert mutation_report.main(["--repo", str(tmp_path)]) == 2
    fake(monkeypatch, results="")
    assert mutation_report.main(["--repo", str(tree(tmp_path))]) == 2
    assert all(ln.startswith("mutation: could not run:") for ln in capsys.readouterr().out.splitlines())


@pytest.mark.req("lockstep-checks/mutation-one-agent-issue-carries-the-survivors", existing=True)
def test_the_issue_is_opened_once_and_commented_on_when_the_survivors_change(tmp_path, monkeypatch, capsys):
    log = []
    one = "    lockstep.a.x_f__mutmut_1: survived\n"
    t = str(tree(tmp_path / "t"))
    fake(monkeypatch, results=one, log=log)
    assert mutation_report.main(["--repo", t, "--issue"]) == 0
    assert "opened https://github.com/x/y/issues/9" in capsys.readouterr().out
    open_now = fake.open
    fake(monkeypatch, results=one, log=log)
    fake.open = open_now
    assert mutation_report.main(["--repo", t, "--issue"]) == 0
    assert "list unchanged, #9 left as is" in capsys.readouterr().out
    fake(monkeypatch, results=one + "    lockstep.a.x_f__mutmut_2: survived\n", log=log)
    fake.open = open_now
    assert mutation_report.main(["--repo", t, "--issue"]) == 0
    assert "commented on #9" in capsys.readouterr().out
    created = [c for c in log if c[:3] == ["gh", "issue", "create"]]
    assert len(created) == 1 and "-lockstep.a.x_f__mutmut_1" in created[0][created[0].index("--body") + 1]


@pytest.mark.req("lockstep-checks/mutation-one-agent-issue-carries-the-survivors", existing=True)
def test_a_survivor_a_new_test_now_kills_leaves_the_issue(tmp_path, monkeypatch, capsys):
    log, state = [], {"rechecked": False}
    before = "    lockstep.a.x_f__mutmut_1: survived\n    lockstep.a.x_f__mutmut_2: survived\n"
    after = "    lockstep.a.x_f__mutmut_1: killed\n    lockstep.a.x_f__mutmut_2: survived\n"
    fake(monkeypatch, results=lambda: after if state["rechecked"] else before, log=log)

    def run_mutmut(cmd, cwd, env, timeout):
        if len(cmd) > 4:
            state["rechecked"] = True
        log.append(cmd)
        return 0, "", 1
    monkeypatch.setattr(mutation_report, "run_mutmut", run_mutmut)
    assert mutation_report.main(["--repo", str(tree(tmp_path / "t")), "--issue"]) == 0
    out = capsys.readouterr().out
    assert "lockstep.a: 1 survived" in out and out.splitlines()[-1].startswith("mutation: 1 survived, 1 killed")
    runs = [c[1:] for c in log if c[1] == "run"]
    assert runs[1] == ["run", "--max-children", "10", "lockstep.a.x_f__mutmut_1", "lockstep.a.x_f__mutmut_2"]
    body = next(c for c in log if c[:3] == ["gh", "issue", "create"])
    text = body[body.index("--body") + 1]
    assert "-lockstep.a.x_f__mutmut_2" in text and "-lockstep.a.x_f__mutmut_1" not in text


@pytest.mark.req("lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure", existing=True)
def test_nothing_survived_opens_no_issue(tmp_path, monkeypatch, capsys):
    log = []
    fake(monkeypatch, results="    lockstep.a.x_f__mutmut_1: killed\n", log=log)
    assert mutation_report.main(["--repo", str(tree(tmp_path / "t")), "--issue"]) == 0
    assert "nothing flagged" in capsys.readouterr().out
    assert not [c for c in log if c[:3] == ["gh", "issue", "create"]]


@pytest.mark.req("lockstep-checks/mutation-survivors-are-a-report-and-a-broken-run-is-a-failure", existing=True)
def test_a_long_issue_body_keeps_whole_diffs_under_the_limit():
    diffs = {f"k{i}": "-a\n+" + "x" * 5000 for i in range(30)}
    body = mutation_report.issue_body({"lockstep.a": list(diffs)}, diffs, "mutation: 30 survived")
    assert len(body) <= mutation_report.BODY_LIMIT and body.count("```diff") == body.count("```") // 2
    assert f"{body.count('```diff')} diffs" in body


@pytest.mark.req("lockstep-checks/mutation-off-unless-switched-on-and-set-per-repository")
def test_off_unless_switched_on_and_set_per_repository(tmp_path, monkeypatch, capsys):
    log = []
    t = tree(tmp_path / "t")
    fake(monkeypatch, log=log)
    assert run_check(["mutation", "--repo", str(t), "--issue"]) == 0
    assert "mutation: skipped (off)" in capsys.readouterr().out and not log
    (t / "lockstep.yaml").write_text("checks:\n  mutation: block\nmutation:\n  issue_repo: Acme/tracker\n  name: Widget\n")
    assert run_check(["mutation", "--repo", str(t), "--issue", "--timeout", "7"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[-1].startswith("mutation: 3 survived, 3 killed of 6 mutants") and "(Widget)" in out[-1]
    made = next(c for c in log if c[:3] == ["gh", "issue", "create"])
    assert made[made.index("-R") + 1] == "Acme/tracker"
    assert made[made.index("--title") + 1] == "Mutation testing: code changes Widget's tests let pass"
    assert (tmp_path / "last-survivors.json").exists() and (tmp_path / "last-not-checked.json").exists()


@pytest.mark.req("lockstep-checks/mutation-off-unless-switched-on-and-set-per-repository")
def test_the_issue_repository_defaults_to_origin_and_state_sits_in_the_git_folder(tmp_path, monkeypatch):
    monkeypatch.undo()
    root = tmp_path / "r"
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin", "git@github.com:Acme/widget.git"], check=True)
    assert mutation_report._origin(root) == ("Acme", "widget")
    assert mutation_report.state_dir(root) == (root / ".git" / "lockstep-mutation").resolve()
    assert mutation_report.title("AES") == "Mutation testing: code changes AES's tests let pass"


@pytest.mark.req("lockstep-checks/mutation-off-unless-switched-on-and-set-per-repository")
def test_mutmut_is_found_in_the_tree_venv_then_on_path(tmp_path, monkeypatch):
    assert mutation_report.find_mutmut(tmp_path) is None
    monkeypatch.setattr(mutation_report.shutil, "which", lambda name: "/opt/bin/mutmut")
    assert mutation_report.find_mutmut(tmp_path) == Path("/opt/bin/mutmut")
    assert mutation_report.find_mutmut(tree(tmp_path)) == tmp_path / ".venv" / "bin" / "mutmut"
