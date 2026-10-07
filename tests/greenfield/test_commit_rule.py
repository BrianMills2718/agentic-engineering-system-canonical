"""SC-AP-001: the commit-tag rule, through the installed commit-msg hook on real commits.

Each test builds a real Git repository holding the frozen whygame5 records, runs
`aes hooks install`, stages real changes and runs `git commit`, so the verdict
comes from the hook git actually runs, not from calling the rule function.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from agentic_engineering_system.cli import main
from agentic_engineering_system.commit_rule import FileChange, RuleConfig, judge, replay

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src"
WHYGAME5_AES = Path(__file__).parent / "fixtures" / "whygame5-54043e2" / ".aes"
ENV = {**os.environ, "PYTHONPATH": str(SRC)}


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
                          cwd=root, capture_output=True, text=True, check=False, env=ENV)


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _commits(root: Path) -> int:
    return int(_git(root, "rev-list", "--count", "HEAD").stdout)


def _set_mode(root: Path, mode: str) -> None:
    _write(root, ".aes/commit_rule.yaml", f"mode: {mode}\n")


def _adopted_plan(root: Path, plan_id: str = "demo") -> Path:
    """A plan with a Company Planning-shaped adoption decision bound to its bytes."""
    plan = root / "proposals" / plan_id / "README.md"
    _write(root, f"proposals/{plan_id}/README.md",
           f"---\nplan_id: {plan_id}\nmethod_conformance_receipt: proposals/{plan_id}/receipt.json\n---\n\n# Demo plan\n")
    _write(root, f"proposals/{plan_id}/receipt.json", json.dumps({"verdict": "pass"}) + "\n")
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    _write(root, f"proposals/{plan_id}/receipt.adoption-decision.json", json.dumps({
        "decision": "adopted", "plan_ref": f"proposals/{plan_id}/README.md",
        "plan_sha256": digest(plan), "receipt_sha256": digest(root / f"proposals/{plan_id}/receipt.json")}) + "\n")
    return plan


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "consumer"
    (root / ".aes").mkdir(parents=True)
    shutil.copyfile(WHYGAME5_AES / "project.yaml", root / ".aes" / "project.yaml")
    shutil.copyfile(WHYGAME5_AES / "target.yaml", root / ".aes" / "target.yaml")
    for rel in ("src/whygame5/__init__.py", "src/whygame5/contracts.py", "src/whygame5/evaluator.py",
                "src/whygame5/graph.py", "tests/test_evaluator.py", "tests/test_replay.py"):
        _write(root, rel, f"# {rel}\n")
    _write(root, "README.md", "# Consumer\n\nA line with a tpyo.\n")
    assert _git(root, "init", "-q").returncode == 0
    _git(root, "add", ".")
    assert _git(root, "commit", "-q", "-m", "fixture").returncode == 0
    assert main(["hooks", "install", "--root", str(root)]) == 0
    _adopted_plan(root)
    _set_mode(root, "enforce")
    _git(root, "add", ".")
    done = _git(root, "commit", "-m", "[Shaping demo] install hooks and draft plan\n\nEmergency: bootstrap")
    # the bootstrap touches files outside proposals/demo/, so even it is refused under enforce;
    # it lands as an emergency instead
    assert done.returncode != 0 and "Shaping demo" in done.stderr
    assert _git(root, "commit", "-m", "[Unplanned] install hooks and draft plan\n\nEmergency: bootstrap the rule").returncode == 0
    return root


def _stage_worker_tools(root: Path) -> None:
    _write(root, "Dockerfile", "FROM debian\nRUN apt-get install -y make\n")
    _write(root, "compose.yaml", "services:\n  app:\n    build: .\n")
    _git(root, "add", "Dockerfile", "compose.yaml")


def test_unplanned_running_thing_without_emergency_is_refused_naming_the_files(repo: Path) -> None:
    before = _commits(repo)
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-m", "[Unplanned] add worker tools")
    assert done.returncode == 1
    assert "refuse [Unplanned]" in done.stderr
    assert "Dockerfile, compose.yaml" in done.stderr and "needs a plan" in done.stderr
    assert _commits(repo) == before


def test_same_change_under_an_adopted_plan_is_accepted(repo: Path) -> None:
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-m", "[Goal demo] U2: worker tools")
    assert done.returncode == 0, done.stderr
    assert "accept [Goal demo]" in done.stderr and "plan demo adopted" in done.stderr


def test_one_line_readme_fix_is_trivial(repo: Path) -> None:
    _write(repo, "README.md", "# Consumer\n\nA line with a typo.\n")
    _git(repo, "add", "README.md")
    done = _git(repo, "commit", "-m", "[Trivial] fix typo")
    assert done.returncode == 0, done.stderr
    assert "accept [Trivial]" in done.stderr and "1 file(s), 2 line(s)" in done.stderr


def test_plan_changed_after_adoption_is_refused(repo: Path) -> None:
    plan = repo / "proposals" / "demo" / "README.md"
    plan.write_text(plan.read_text(encoding="utf-8") + "\nEdited after adoption.\n", encoding="utf-8")
    _stage_worker_tools(repo)
    _git(repo, "add", str(plan))
    done = _git(repo, "commit", "-m", "[Goal demo] U2: worker tools")
    assert done.returncode == 1
    assert "plan changed since adoption; re-adopt it" in done.stderr


def test_plan_without_receipt_and_unknown_plan_are_refused(repo: Path) -> None:
    _write(repo, "docs/plans/7_old_plan.md", "# Plan 7, written before adoption existed\n")
    _git(repo, "add", "docs/plans/7_old_plan.md")
    done = _git(repo, "commit", "-m", "[Plan #7] old-style plan")
    assert done.returncode == 1 and "no method_conformance_receipt" in done.stderr
    done = _git(repo, "commit", "-m", "[Goal nosuch] work")
    assert done.returncode == 1 and "no plan nosuch found" in done.stderr


@pytest.mark.parametrize(("files", "reason"), [
    ({"hooks/pre-push": "#!/bin/sh\n"}, "touches running-thing file(s): hooks/pre-push"),
    ({"a.md": "a\n", "b.md": "b\n", "c.md": "c\n", "d.md": "d\n"}, "4 files (trivial allows 3)"),
    ({"notes.md": "x\n" * 61}, "61 changed lines (trivial allows 60)"),
    ({"src/whygame5/new.py": "x = 1\n"}, "adds file(s) under a governed root: src/whygame5/new.py"),
])
def test_trivial_is_measured_not_trusted(repo: Path, files: dict[str, str], reason: str) -> None:
    for rel, text in files.items():
        _write(repo, rel, text)
        _git(repo, "add", rel)
    # the same command the installed hook runs, on the staged change, before any commit
    msg = repo / ".git" / "MSG"
    msg.write_text("[Trivial] small thing\n", encoding="utf-8")
    checked = subprocess.run([sys.executable, "-m", "agentic_engineering_system.cli", "commit", "check",
                              str(msg), "--root", str(repo)], cwd=repo, capture_output=True, text=True, env=ENV)
    assert checked.returncode == 1
    assert reason in checked.stderr


def test_emergency_and_shaping(repo: Path) -> None:
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-m", "[Unplanned] hotfix the worker image\n\nEmergency: workers down since 06:00")
    assert done.returncode == 0 and "emergency recorded" in done.stderr
    _write(repo, "proposals/next/README.md", "# Next plan draft\n")
    _git(repo, "add", "proposals/next/README.md")
    done = _git(repo, "commit", "-m", "[Shaping next] first draft")
    assert done.returncode == 0 and "accept [Shaping next]" in done.stderr
    _write(repo, "proposals/next/README.md", "# Next plan draft, v2\n")
    _write(repo, "README.md", "# Consumer\n\nAlso edited.\n")
    _git(repo, "add", "proposals/next/README.md", "README.md")
    done = _git(repo, "commit", "-m", "[Shaping next] second draft")
    assert done.returncode == 1 and "also touches README.md" in done.stderr


def test_observe_mode_logs_and_never_blocks(repo: Path) -> None:
    _set_mode(repo, "observe")
    _stage_worker_tools(repo)
    _git(repo, "add", ".aes/commit_rule.yaml")
    before = _commits(repo)
    done = _git(repo, "commit", "-m", "[Unplanned] add worker tools")
    assert done.returncode == 0
    assert "would refuse (observe mode) [Unplanned]" in done.stderr
    assert _commits(repo) == before + 1
    logs = sorted((repo / ".git" / "aes").glob("commit-rule-*.jsonl"))
    last = json.loads(logs[-1].read_text(encoding="utf-8").splitlines()[-1])
    assert last["mode"] == "observe" and last["verdict"] == "refuse" and last["tag"] == "Unplanned"
    assert last["running_things"] == ["Dockerfile", "compose.yaml"]


def test_no_tag_is_refused_and_git_messages_pass() -> None:
    config = RuleConfig()
    change = [FileChange("README.md", "M", 1, 1)]
    assert judge("fix things", change, [], config).verdict == "refuse"
    assert judge("Merge branch 'x' into main", change, [], config).verdict == "accept"
    assert judge("fixup! [Trivial] fix typo", change, [], config).verdict == "accept"


def test_replay_judges_history_with_counts(repo: Path) -> None:
    _write(repo, "README.md", "# Consumer\n\nA line with a typo.\n")
    _git(repo, "add", "README.md")
    assert _git(repo, "commit", "-m", "[Trivial] fix typo").returncode == 0
    rows, counts = replay(repo, "HEAD", 10)
    verdicts = {subject: v.verdict for _, subject, v in rows}
    assert verdicts["[Trivial] fix typo"] == "accept"
    assert verdicts["[Unplanned] install hooks and draft plan"] == "accept"  # emergency recorded
    assert verdicts["fixture"] == "refuse"  # no tag
    assert counts == {"commits": 3, "accept": 2, "refuse": 1, "tag:Trivial": 1, "tag:Unplanned": 1, "tag:none": 1}


def test_an_older_aes_without_the_rule_warns_and_does_not_block(repo: Path, tmp_path: Path) -> None:
    """A main checkout on an older branch must not stop every commit in every worktree."""
    old_aes = tmp_path / "old-python"
    old_aes.write_text("#!/bin/sh\necho 'aes: error: invalid choice: commit' >&2\nexit 2\n", encoding="utf-8")
    old_aes.chmod(0o755)
    assert _git(repo, "config", "--local", "aes.installer", str(old_aes)).returncode == 0
    _write(repo, "notes.md", "x\n")
    _git(repo, "add", "notes.md")
    done = _git(repo, "commit", "--no-verify", "-m", "placeholder")  # pre-commit would also use the old aes
    assert done.returncode == 0
    _git(repo, "reset", "--soft", "HEAD~1")
    hook = subprocess.run([str(repo / ".githooks" / "commit-msg"), str(repo / ".git" / "COMMIT_EDITMSG")],
                          cwd=repo, capture_output=True, text=True, env=ENV)
    assert hook.returncode == 0
    assert "WARNING: this AES has no 'commit' command, so the commit rule did not run" in hook.stderr


def test_in_aes_itself_the_hooks_run_the_working_copy_code() -> None:
    """Both hooks put `<root>/src` first when the repository is AES, so a worktree is checked
    by its own code, not by the branch the shared venv's editable install points at."""
    from agentic_engineering_system.hooks import render_commit_msg_hook, render_hook

    for body in (render_hook(), render_commit_msg_hook()):
        assert 'if [ -f "$root/src/agentic_engineering_system/cli.py" ]; then' in body
        assert 'PYTHONPATH="$root/src${PYTHONPATH:+:$PYTHONPATH}"; export PYTHONPATH' in body
    # this repository's tracked hooks are the rendered ones
    assert (REPO / ".githooks" / "pre-commit").read_text(encoding="utf-8") == render_hook()
    assert (REPO / ".githooks" / "commit-msg").read_text(encoding="utf-8") == render_commit_msg_hook()


def test_machine_config_reaches_repositories_without_their_own(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A plain repository takes the machine-wide mode; a per-repository entry overrides it; a repo file wins."""
    from agentic_engineering_system.commit_rule import load_rule_config

    machine = tmp_path / "machine.yaml"
    machine.write_text("mode: enforce\ntrivial_max_lines: 40\nrepos:\n  quiet:\n    mode: observe\n", encoding="utf-8")
    monkeypatch.setenv("AES_COMMIT_RULE_MACHINE_CONFIG", str(machine))
    plain, quiet, own = tmp_path / "plain", tmp_path / "quiet", tmp_path / "own"
    for root in (plain, quiet, own):
        root.mkdir()
    _write(own, ".aes/commit_rule.yaml", "mode: observe\n")
    assert (load_rule_config(plain).mode, load_rule_config(plain).trivial_max_lines) == ("enforce", 40)
    assert load_rule_config(plain).source == str(machine)
    assert load_rule_config(quiet).mode == "observe"
    assert load_rule_config(own).mode == "observe" and load_rule_config(own).source.endswith(".aes/commit_rule.yaml")
    monkeypatch.setenv("AES_COMMIT_RULE_MACHINE_CONFIG", str(tmp_path / "absent.yaml"))
    assert load_rule_config(plain).mode == "observe" and load_rule_config(plain).source == "default"


def test_auto_tag_names_its_job_and_touches_no_running_thing() -> None:
    """[Auto] is for scheduled jobs: it must name the job and may not change anything that runs."""
    config = RuleConfig(plan_roots=())
    data = [FileChange("data/prices.csv", "M", 4000, 3900)]
    assert judge("[Auto] refresh prices", data, [], config).verdict == "refuse"
    ok = judge("[Auto] refresh prices\n\nAuto-job: price-sync.timer", data, [], config)
    assert ok.verdict == "accept" and "price-sync.timer" in ok.reasons[0]
    risky = judge("[Auto] refresh\n\nAuto-job: price-sync.timer", [FileChange("Dockerfile", "M", 1, 0)], [], config)
    assert risky.verdict == "refuse" and "Dockerfile" in risky.reasons[0]


def test_enforce_with_plan_adoption_observe_blocks_untagged_but_not_unadopted_plans(repo: Path) -> None:
    """Staged enforcement: tags and trivial size are refused; a plan that is not adopted is only logged."""
    _write(repo, ".aes/commit_rule.yaml", "mode: enforce\nplan_adoption: observe\n")
    _git(repo, "add", ".aes/commit_rule.yaml")
    assert _git(repo, "commit", "-m", "[Unplanned] stage config\n\nEmergency: test setup").returncode == 0
    _write(repo, "README.md", "# Consumer\n\nA line with a typo fixed.\n")
    _git(repo, "add", "README.md")
    untagged = _git(repo, "commit", "-m", "fix typo")
    assert untagged.returncode != 0 and "no tag" in untagged.stderr
    unadopted = _git(repo, "commit", "-m", "[Plan #999] fix typo under a plan that does not exist")
    assert unadopted.returncode == 0 and "plan adoption is observe-only" in unadopted.stderr


def test_goal_plan_owned_by_another_repository_resolves_through_the_workspace(repo: Path, tmp_path: Path) -> None:
    """Federated plans: the plan and its receipt live in the repository that owns them; a commit
    in another repository under the same workspace that names it is judged against it."""
    owner = tmp_path / "owner"
    owner.mkdir()
    assert _git(owner, "init", "-q").returncode == 0
    _adopted_plan(owner, "fed")
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-m", "[Goal fed] U1: worker tools")
    assert done.returncode == 1 and "no plan fed found" in done.stderr
    _write(repo, ".aes/commit_rule.yaml", f"mode: enforce\nplan_workspace: {tmp_path}\n")
    _git(repo, "add", ".aes/commit_rule.yaml")
    done = _git(repo, "commit", "-m", "[Goal fed] U1: worker tools")
    assert done.returncode == 0, done.stderr
    assert "plan fed adopted (proposals/fed/README.md)" in done.stderr
    _write(repo, "notes.md", "x\n" * 70)
    _git(repo, "add", "notes.md")
    done = _git(repo, "commit", "-m", "[Goal nosuch] more work")
    assert done.returncode == 1 and f"every repository in {tmp_path}" in done.stderr


def test_goal_plan_on_another_repositorys_main_resolves_when_its_checkout_is_elsewhere(
        repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The owner repository's checkout sits on a branch without the plan; its main has it. The
    working-tree scan cannot see it; the plan index, read from main through git, can."""
    from agentic_engineering_system.commit_rule import build_plan_index

    index = tmp_path / "plan-index.json"
    monkeypatch.setenv("AES_PLAN_INDEX", str(index))
    monkeypatch.setenv("AES_PLAN_INDEX_REFRESH", "0")
    owner = tmp_path / "owner"
    owner.mkdir()
    assert _git(owner, "init", "-q", "-b", "main").returncode == 0
    _adopted_plan(owner, "onmain")
    _git(owner, "add", ".")
    assert _git(owner, "commit", "-q", "-m", "adopt onmain").returncode == 0
    _git(owner, "update-ref", "refs/remotes/origin/main", "main")
    assert _git(owner, "checkout", "-q", "--orphan", "other").returncode == 0
    _git(owner, "rm", "-rq", "--cached", ".")
    shutil.rmtree(owner / "proposals")
    assert not (owner / "proposals").exists()
    _write(repo, ".aes/commit_rule.yaml", f"mode: enforce\nplan_workspace: {tmp_path}\n")
    _git(repo, "add", ".aes/commit_rule.yaml")
    _stage_worker_tools(repo)
    env = {**ENV, "AES_PLAN_INDEX": str(index), "AES_PLAN_INDEX_REFRESH": "0"}
    refused = subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", "commit", "-m",
                              "[Goal onmain] U1: worker tools"], cwd=repo, capture_output=True, text=True, env=env)
    assert refused.returncode == 1 and "no plan onmain found" in refused.stderr, refused.stderr
    built = build_plan_index(tmp_path, index)
    assert built["repos"][str(owner.resolve())]["plans"] == {"onmain": ["proposals/onmain/README.md"]}
    done = subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", "commit", "-m",
                           "[Goal onmain] U1: worker tools"], cwd=repo, capture_output=True, text=True, env=env)
    assert done.returncode == 0, done.stderr
    assert "adopted on the default branch (owner origin/main:proposals/onmain/README.md)" in done.stderr
