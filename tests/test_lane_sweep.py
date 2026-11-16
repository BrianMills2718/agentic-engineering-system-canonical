"""Tests for scripts/lane_sweep.py against a throwaway repository, a bare remote and linked worktrees."""

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))  # AES tests import src/; lane_sweep lives in scripts/
import lane_sweep  # noqa: E402


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture
def repo(tmp_path, monkeypatch):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    work = tmp_path / "work"
    subprocess.run(["git", "init", "-q", "-b", "main", str(work)], check=True)
    git(work, "config", "user.email", "t@example.com")
    git(work, "config", "user.name", "t")
    (work / "a.txt").write_text("a\n")
    (work / ".gitignore").write_text("build/\n")
    git(work, "add", ".")
    git(work, "commit", "-q", "-m", "base")
    git(work, "remote", "add", "origin", str(remote))
    git(work, "push", "-q", "-u", "origin", "main")
    monkeypatch.setenv("LANE_SWEEP_LOG_DIR", str(tmp_path / "logs"))
    # No test reads the machine's own systemd units: a real timer naming a folder in the temp dir would change the result.
    monkeypatch.setenv("LANE_SWEEP_UNITS_DIR", str(tmp_path / "no-units"))
    # No test reads the person's own settings (gh wrappers, canonical lock).
    monkeypatch.setattr(lane_sweep, "CONFIG", tmp_path / "no-config" / "graph-config.yaml")
    return work


def lane(work: Path, name: str, change: str | None = "b\n") -> Path:
    """Add a worktree on a new branch, optionally committing a change to a.txt."""
    path = work.parent / name
    git(work, "worktree", "add", "-q", "-b", name, str(path))
    if change is not None:
        (path / "a.txt").write_text(change)
        git(path, "commit", "-q", "-am", f"{name} change")
    return path


def age(path: Path, minutes: float = 120) -> None:
    """Make the worktree look idle for the given minutes."""
    gitdir = Path(git(path, "rev-parse", "--absolute-git-dir"))
    old = time.time() - minutes * 60
    for name in ("HEAD", "index", "logs/HEAD"):
        if (gitdir / name).exists():
            os.utime(gitdir / name, (old, old))


def land_on_main(work: Path, branch: str) -> None:
    """Merge the branch into main and push, as a merged pull request would."""
    git(work, "merge", "-q", "--no-ff", "-m", f"merge {branch}", branch)
    git(work, "push", "-q", "origin", "main")


def sweep(work: Path, *extra: str) -> int:
    return lane_sweep.main(["--repo", str(work), *extra])


def branch_exists(work: Path, name: str) -> bool:
    return bool(git(work, "branch", "--list", name))


@pytest.mark.req("lane-sweep/a-clean-lane-whose-commits-are-on-main-is-removed")
def test_a_clean_lane_whose_commits_are_on_main_is_removed(repo):
    wt = lane(repo, "done")
    (wt / "build").mkdir()
    (wt / "build" / "out.bin").write_text("ignored output\n")
    land_on_main(repo, "done")
    age(wt)
    assert sweep(repo, "--apply") == 0
    assert not wt.exists()
    assert not branch_exists(repo, "done")


@pytest.mark.req("lane-sweep/a-squash-merged-lane-is-removed")
def test_a_squash_merged_lane_is_removed(repo):
    wt = lane(repo, "squashed")
    git(repo, "merge", "-q", "--squash", "squashed")
    git(repo, "commit", "-q", "-m", "squash")
    git(repo, "push", "-q", "origin", "main")
    age(wt)
    assert sweep(repo, "--apply") == 0
    assert not wt.exists()
    assert not branch_exists(repo, "squashed")


@pytest.mark.req("lane-sweep/a-lane-with-uncommitted-changes-is-kept")
def test_a_lane_with_uncommitted_changes_is_kept(repo, capsys):
    wt = lane(repo, "dirty")
    land_on_main(repo, "dirty")
    (wt / "a.txt").write_text("edit in progress\n")
    age(wt)
    assert sweep(repo, "--apply") == 0
    assert wt.exists() and branch_exists(repo, "dirty")
    assert "uncommitted changes" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-lane-with-submodules-is-kept-not-failed")
def test_a_lane_with_submodules_is_kept_not_failed(repo, capsys):
    # 2026-11-11: every run failed on worktrees/sbm-planning-package; git will not move or remove a worktree
    # containing submodules without --force, which the sweep never uses.
    wt = lane(repo, "with-subs", change=None)
    (wt / ".gitmodules").write_text('[submodule "vendor"]\n\tpath = vendor\n\turl = ../vendor.git\n')
    git(wt, "add", ".gitmodules")
    git(wt, "commit", "-q", "-m", "add submodule config")
    land_on_main(repo, "with-subs")
    age(wt)
    assert sweep(repo, "--apply") == 0
    assert wt.exists() and branch_exists(repo, "with-subs")
    assert "submodules" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-locked-worktree-is-kept")
def test_a_locked_worktree_is_kept(repo, capsys):
    # 2026-11-05 to 2026-11-13: the sweep removed process_tracing's pinned llm_client checkout six times
    # (~/code2/.lane-sweep-logs/2026-11-13.log:337). It is a detached worktree at a commit on the default
    # branch, used through an editable install with no process running: by every other check, a finished lane.
    pin = repo.parent / "pinned-runtime"
    git(repo, "worktree", "add", "-q", "--detach", str(pin), "origin/main")
    git(repo, "worktree", "lock", "--reason", "pinned runtime for another project; not a lane", str(pin))
    age(pin, minutes=3 * 24 * 60)
    assert sweep(repo, "--apply") == 0
    assert pin.exists()
    assert f"keep {pin} [detached]: locked: pinned runtime for another project; not a lane" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-locked-worktree-is-kept", existing=True)  # guard: the control, true before the change
def test_the_same_worktree_unlocked_is_removed(repo):
    # The control for the test above: without the lock the sweep removes it.
    pin = repo.parent / "pinned-runtime"
    git(repo, "worktree", "add", "-q", "--detach", str(pin), "origin/main")
    age(pin, minutes=3 * 24 * 60)
    assert sweep(repo, "--apply") == 0
    assert not pin.exists()


@pytest.mark.req("lane-sweep/a-lane-with-work-not-on-main-is-kept")
def test_a_lane_with_work_not_on_main_is_kept(repo, capsys):
    wt = lane(repo, "unmerged")
    age(wt)
    assert sweep(repo, "--apply") == 0
    assert wt.exists() and branch_exists(repo, "unmerged")
    assert "work not on origin/main" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-lane-a-process-is-working-in-is-kept")
def test_a_lane_a_process_is_working_in_is_kept(repo, capsys):
    wt = lane(repo, "busy")
    land_on_main(repo, "busy")
    age(wt)
    proc = subprocess.Popen(["sleep", "30"], cwd=wt, start_new_session=True)  # another agent: its own session
    try:
        assert sweep(repo, "--apply") == 0
    finally:
        proc.kill()
        proc.wait()
    assert wt.exists() and branch_exists(repo, "busy")
    assert f"in use by process {proc.pid}" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-lane-a-systemd-unit-runs-from-is-kept")
def test_a_lane_a_systemd_unit_runs_from_is_kept(repo, capsys, tmp_path, monkeypatch):
    wt = lane(repo, "timer-job")
    land_on_main(repo, "timer-job")
    age(wt)
    units = tmp_path / "units"
    units.mkdir()
    (units / "job.service").write_text(f"[Service]\nWorkingDirectory={wt}\nExecStart=/usr/bin/true\n")
    monkeypatch.setenv("LANE_SWEEP_UNITS_DIR", str(units))
    assert sweep(repo, "--apply") == 0
    assert wt.exists() and branch_exists(repo, "timer-job")
    assert "the systemd unit job.service runs from it" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-lane-a-pending-transient-timer-runs-from-is-kept")
def test_a_lane_a_pending_transient_timer_runs_from_is_kept(repo, capsys, tmp_path, monkeypatch):
    """`systemd-run --user --on-calendar` writes its unit to $XDG_RUNTIME_DIR/systemd/transient, not ~/.config (#76)."""
    wt = lane(repo, "pass2-runtime")
    land_on_main(repo, "pass2-runtime")
    age(wt)
    runtime = tmp_path / "run-user"
    transient = runtime / "systemd" / "transient"
    transient.mkdir(parents=True)
    # The file systemd wrote for a real `systemd-run --user --on-calendar=... --working-directory=<lane> ...` (2026-11-09).
    (transient / "run-u123.service").write_text(
        "# This is a transient unit file, created programmatically via the systemd API. Do not edit.\n"
        "[Unit]\nDescription=run pass 2\n\n[Service]\n"
        f'WorkingDirectory={wt}\nEnvironment="PYTHONPATH={wt}/src"\nExecStart=\nExecStart="/usr/bin/true" "{wt}/run.sh"\n'
    )
    (transient / "run-u123.timer").write_text("[Timer]\nOnCalendar=2099-01-01 22:00:00\nRemainAfterElapse=no\n")
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.delenv("LANE_SWEEP_UNITS_DIR")
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    monkeypatch.setenv("HOME", str(home))
    assert sweep(repo, "--apply") == 0
    assert wt.exists() and branch_exists(repo, "pass2-runtime")
    assert "the systemd unit run-u123.service runs from it" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-lane-named-only-in-a-unit-s-drop-in-is-kept")
def test_a_lane_named_only_in_a_unit_drop_in_is_kept(repo, capsys, tmp_path, monkeypatch):
    wt = lane(repo, "drop-in-job")
    land_on_main(repo, "drop-in-job")
    age(wt)
    units = tmp_path / "units"
    (units / "job.service.d").mkdir(parents=True)
    (units / "job.service").write_text("[Service]\nExecStart=/usr/bin/true\n")
    (units / "job.service.d" / "10-where.conf").write_text(f"[Service]\nWorkingDirectory={wt}\n")
    monkeypatch.setenv("LANE_SWEEP_UNITS_DIR", str(units))
    assert sweep(repo, "--apply") == 0
    assert wt.exists() and branch_exists(repo, "drop-in-job")
    assert "the systemd unit job.service runs from it" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-unit-that-names-another-folder-does-not-keep-a-lane", existing=True)  # guard: the old scan did not over-keep either
def test_a_unit_that_names_another_folder_does_not_keep_a_lane(repo, tmp_path, monkeypatch):
    wt = lane(repo, "job")
    land_on_main(repo, "job")
    age(wt)
    units = tmp_path / "units"
    units.mkdir()
    # A sibling whose name starts with the lane's name, and the lane's parent folder, are not the lane.
    (units / "other.service").write_text(f"[Service]\nWorkingDirectory={wt}-2\nExecStart=/usr/bin/test {wt.parent}\n")
    monkeypatch.setenv("LANE_SWEEP_UNITS_DIR", str(units))
    assert sweep(repo, "--apply") == 0
    assert not wt.exists() and not branch_exists(repo, "job")


@pytest.mark.req("lane-sweep/a-lane-a-process-runs-code-from-is-kept")
def test_a_lane_a_process_runs_code_from_is_kept(repo, capsys, tmp_path):
    wt = lane(repo, "runs-from")
    land_on_main(repo, "runs-from")
    age(wt)
    tracked = next(p for p in wt.iterdir() if p.is_file())  # a file of the lane, as `<lane>/script.py` would be
    proc = subprocess.Popen(["python3", "-c", "import time; time.sleep(30)", str(tracked)],
                            cwd=tmp_path, start_new_session=True)  # started outside the lane
    try:
        time.sleep(0.3)
        assert sweep(repo, "--apply") == 0
    finally:
        proc.kill()
        proc.wait()
    assert wt.exists() and branch_exists(repo, "runs-from")
    assert f"in use by process {proc.pid}" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-new-lane-with-no-commits-is-kept")
def test_a_new_lane_with_no_commits_is_kept(repo, capsys):
    wt = lane(repo, "fresh", change=None)
    age(wt, minutes=60)  # past the 30-minute limit, inside the 24-hour one for empty branches
    assert sweep(repo, "--apply") == 0
    assert wt.exists() and branch_exists(repo, "fresh")
    assert "recently active" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-removal-can-be-undone")
def test_a_removal_can_be_undone(repo, tmp_path):
    wt = lane(repo, "undo")
    tip = git(wt, "rev-parse", "HEAD")
    land_on_main(repo, "undo")
    age(wt)
    assert sweep(repo, "--apply") == 0
    log = next((tmp_path / "logs").glob("????-??-??.log")).read_text()
    restore = f"git -C {repo.resolve()} branch undo {tip}"
    assert restore in log
    subprocess.run(restore, shell=True, check=True)
    assert git(repo, "rev-parse", "undo") == tip


@pytest.mark.req("lane-sweep/without-apply-nothing-changes")
def test_without_apply_nothing_changes(repo, capsys):
    wt = lane(repo, "report")
    land_on_main(repo, "report")
    age(wt)
    assert sweep(repo) == 0
    assert wt.exists() and branch_exists(repo, "report")
    out = capsys.readouterr().out
    assert "removable" in out and "removed 0" in out


@pytest.mark.req("lane-sweep/the-command-that-launched-the-sweep-does-not-hold-the-lane")
def test_the_command_that_launched_the_sweep_does_not_hold_the_lane(repo):
    wt = lane(repo, "piped")
    land_on_main(repo, "piped")
    age(wt)
    sibling = subprocess.Popen(["sleep", "30"], cwd=wt)  # same session, like the other end of `ship | tail`
    try:
        assert sweep(repo, "--apply") == 0
    finally:
        sibling.kill()
        sibling.wait()
    assert not wt.exists()


FAKE_GH = """#!/usr/bin/env python3
import json, os, sys
print(json.dumps([{"number": 12, "headRefOid": os.environ["FAKE_PR_HEAD"]}]))
"""


@pytest.mark.req("lane-sweep/a-lane-at-a-merged-pull-request-head-is-removed")
def test_a_lane_at_a_merged_pull_request_head_is_removed(repo, tmp_path, monkeypatch):
    wt = lane(repo, "merged-then-changed")
    tip = git(wt, "rev-parse", "HEAD")
    git(repo, "merge", "-q", "--squash", "merged-then-changed")
    git(repo, "commit", "-q", "-m", "squash")
    (repo / "a.txt").write_text("main changed it again\n")
    git(repo, "commit", "-q", "-am", "later change")
    git(repo, "push", "-q", "origin", "main")
    git(repo, "config", "remote.origin.url", "git@github.com:o/r.git")
    git(repo, "config", f"url.{repo.parent / 'remote.git'}.insteadOf", "git@github.com:o/r.git")
    gh = tmp_path / "fake-gh"
    gh.write_text(FAKE_GH)
    gh.chmod(0o755)
    monkeypatch.setenv("LANE_SWEEP_GH", str(gh))
    monkeypatch.setenv("FAKE_PR_HEAD", "0" * 40)
    age(wt)
    assert sweep(repo, "--apply") == 0
    assert wt.exists(), "a merged pull request at another commit does not count"
    monkeypatch.setenv("FAKE_PR_HEAD", tip)
    assert sweep(repo, "--apply") == 0
    assert not wt.exists()
    assert not branch_exists(repo, "merged-then-changed")


def advance_origin(work: Path, text: str = "from elsewhere\n") -> str:
    """Push a new commit to origin/main from a second clone, as a merged pull request would; return it."""
    other = work.parent / f"other-{time.monotonic_ns()}"
    subprocess.run(["git", "clone", "-q", str(work.parent / "remote.git"), str(other)], check=True)
    git(other, "config", "user.email", "t@example.com")
    git(other, "config", "user.name", "t")
    (other / "c.txt").write_text(text)
    git(other, "add", "c.txt")
    git(other, "commit", "-q", "-m", "merged elsewhere")
    git(other, "push", "-q", "origin", "main")
    return git(other, "rev-parse", "HEAD")


@pytest.mark.req("lane-sweep/a-clean-idle-primary-checkout-is-fast-forwarded")
def test_a_clean_idle_primary_checkout_is_fast_forwarded(repo, tmp_path):
    old = git(repo, "rev-parse", "HEAD")
    new = advance_origin(repo)
    assert sweep(repo, "--apply") == 0
    assert git(repo, "rev-parse", "main") == new
    assert (repo / "c.txt").exists()
    log = next((tmp_path / "logs").glob("????-??-??.log")).read_text()
    assert f"fast-forward {repo.resolve()} [main] {old} -> {new}" in log


@pytest.mark.req("lane-sweep/a-locked-primary-checkout-moves-through-canonical-lock-sync")
def test_a_read_only_primary_checkout_is_moved_through_the_lock_tool(repo, tmp_path, monkeypatch):
    new = advance_origin(repo)
    calls = tmp_path / "calls.txt"
    tool = tmp_path / "canonical_lock.py"
    tool.write_text(
        "import subprocess, sys\n"
        f"open({str(calls)!r}, 'a').write(' '.join(sys.argv[1:]) + '\\n')\n"
        "root = sys.argv[2]\n"
        "subprocess.run(['chmod', 'u+w', root], check=True)\n"
        "r = subprocess.run(['git', '-C', root, 'pull', '-q', '--ff-only'])\n"
        "subprocess.run(['chmod', 'a-w', root], check=True)\n"
        "sys.exit(r.returncode)\n")
    monkeypatch.setenv("LANE_SWEEP_CANONICAL_LOCK", str(tool))
    os.chmod(repo, 0o555)
    try:
        assert sweep(repo, "--apply") == 0
    finally:
        os.chmod(repo, 0o755)
    assert git(repo, "rev-parse", "main") == new
    assert calls.read_text().startswith(f"--sync {repo.resolve()}")


@pytest.mark.req("lane-sweep/a-primary-checkout-with-uncommitted-changes-is-not-moved")
def test_a_primary_checkout_with_uncommitted_changes_is_not_moved(repo, capsys):
    old = git(repo, "rev-parse", "HEAD")
    advance_origin(repo)
    (repo / "a.txt").write_text("edit in progress\n")
    assert sweep(repo, "--apply") == 0
    assert git(repo, "rev-parse", "main") == old
    assert f"skip fast-forward {repo.resolve()} [main]: uncommitted changes" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-primary-checkout-on-another-branch-is-not-moved")
def test_a_primary_checkout_on_another_branch_is_not_moved(repo, capsys):
    old = git(repo, "rev-parse", "HEAD")
    git(repo, "checkout", "-q", "-b", "side")
    advance_origin(repo)
    assert sweep(repo, "--apply") == 0
    assert git(repo, "rev-parse", "main") == old and git(repo, "rev-parse", "side") == old
    assert f"skip fast-forward {repo.resolve()} [side]: not on main" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-primary-checkout-with-its-own-commits-is-not-moved")
def test_a_primary_checkout_with_its_own_commits_is_not_moved(repo, capsys):
    advance_origin(repo)
    (repo / "a.txt").write_text("local only\n")
    git(repo, "commit", "-q", "-am", "local commit")
    local = git(repo, "rev-parse", "HEAD")
    assert sweep(repo, "--apply") == 0
    assert git(repo, "rev-parse", "main") == local
    assert f"skip fast-forward {repo.resolve()} [main]: diverged from origin/main" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-primary-checkout-a-process-is-working-in-is-not-moved")
def test_a_primary_checkout_a_process_is_working_in_is_not_moved(repo, capsys):
    old = git(repo, "rev-parse", "HEAD")
    advance_origin(repo)
    proc = subprocess.Popen(["sleep", "30"], cwd=repo, start_new_session=True)
    try:
        assert sweep(repo, "--apply") == 0
    finally:
        proc.kill()
        proc.wait()
    assert git(repo, "rev-parse", "main") == old
    assert f"skip fast-forward {repo.resolve()} [main]: in use by process {proc.pid}" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-process-in-a-lane-nested-in-the-checkout-does-not-hold-it")
def test_a_process_in_a_lane_nested_in_the_checkout_does_not_hold_it(repo):
    (repo / ".gitignore").write_text("build/\n.claude/\n")
    git(repo, "commit", "-q", "-am", "ignore nested lanes")
    git(repo, "push", "-q", "origin", "main")
    nested = repo / ".claude" / "worktrees" / "inner"
    git(repo, "worktree", "add", "-q", "-b", "inner", str(nested))
    new = advance_origin(repo)
    proc = subprocess.Popen(["sleep", "30"], cwd=nested, start_new_session=True)
    try:
        assert sweep(repo, "--apply") == 0
    finally:
        proc.kill()
        proc.wait()
    assert git(repo, "rev-parse", "main") == new


@pytest.mark.req("lane-sweep/without-apply-the-checkout-is-only-reported")
def test_without_apply_the_checkout_is_only_reported(repo, capsys):
    old = git(repo, "rev-parse", "HEAD")
    new = advance_origin(repo)
    assert sweep(repo) == 0
    assert git(repo, "rev-parse", "main") == old
    assert f"fast-forwardable {repo.resolve()} [main] {old[:12]} -> {new[:12]}" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-lane-a-process-imports-from-is-kept")
def test_a_lane_a_process_imports_from_is_kept(repo, capsys, tmp_path):
    wt = lane(repo, "imported")
    land_on_main(repo, "imported")
    age(wt)
    src = wt / "src"  # like PYTHONPATH=<lane>/src in a greer run started from another worktree
    proc = subprocess.Popen(["python3", "-c", "import time; time.sleep(30)"], cwd=tmp_path, start_new_session=True,
                            env={**os.environ, "PYTHONPATH": f"/nowhere:{src}"})
    try:
        time.sleep(0.3)
        assert sweep(repo, "--apply") == 0
    finally:
        proc.kill()
        proc.wait()
    assert wt.exists() and branch_exists(repo, "imported")
    assert f"in use by process {proc.pid}" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-lane-an-editable-install-points-into-is-kept")
def test_a_lane_an_editable_install_points_into_is_kept(repo, capsys, tmp_path):
    wt = lane(repo, "editable")
    land_on_main(repo, "editable")
    age(wt)
    venv = tmp_path / "venv"  # a virtual environment elsewhere with `pip install -e <lane>`
    site = venv / "lib" / "python3.99" / "site-packages"
    site.mkdir(parents=True)
    (site / "_editable.pth").write_text(f"{wt / 'src'}\n")
    (venv / "pyvenv.cfg").write_text(f"home = {Path(os.path.realpath(sys.executable)).parent}\n")
    (venv / "bin").mkdir()
    (venv / "bin" / "python").symlink_to(os.path.realpath(sys.executable))
    proc = subprocess.Popen([str(venv / "bin" / "python"), "-c", "import time; time.sleep(30)"], cwd=tmp_path,
                            start_new_session=True)
    try:
        time.sleep(0.3)
        assert sweep(repo, "--apply") == 0
    finally:
        proc.kill()
        proc.wait()
    assert wt.exists() and branch_exists(repo, "editable")
    assert f"in use by process {proc.pid}" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-removal-that-fails-partway-leaves-no-half-tree-at-the-lane-s-path")
def test_a_removal_that_fails_partway_leaves_no_half_tree_at_the_lanes_path(repo, tmp_path, monkeypatch):
    # The pre-check below would catch an unwritable folder; switch it off to stand for a failure nobody can
    # foresee (a file appearing mid-delete, an immutable file, the sweep being killed).
    monkeypatch.setattr(lane_sweep, "_unwritable_folder", lambda path: None)
    wt = lane(repo, "stuck")
    for i in range(5):
        (wt / f"f{i}.txt").write_text(f"{i}\n")
    git(wt, "add", ".")
    git(wt, "commit", "-q", "-m", "more files")
    land_on_main(repo, "stuck")
    (wt / "build").mkdir()
    (wt / "build" / "out.bin").write_text("ignored output\n")
    (wt / "build").chmod(0o555)  # its file cannot be unlinked, so deletion stops partway
    age(wt)
    aside = wt.with_name(".stuck.lane-sweep-removing")
    try:
        assert sweep(repo, "--apply") == 1
        assert not wt.exists(), "no half-deleted tree is left at the lane's own path"
        assert aside.exists() and branch_exists(repo, "stuck")
        log = next((tmp_path / "logs").glob("????-??-??.log")).read_text()
        assert "lane-sweep: repos 1" in log
        restore = f"git -C {repo.resolve()} worktree add {wt.resolve()} stuck"
        assert restore in log
        subprocess.run(restore, shell=True, check=True, capture_output=True)
        assert git(wt, "status", "--porcelain") == "" and (wt / "f4.txt").read_text() == "4\n"
    finally:
        if (aside / "build").exists():
            (aside / "build").chmod(0o755)


@pytest.mark.req("lane-sweep/a-removal-that-times-out-leaves-the-lane-whole")
def test_a_removal_that_times_out_leaves_the_lane_whole(repo, tmp_path, monkeypatch):
    wt = lane(repo, "slow")
    land_on_main(repo, "slow")
    age(wt)
    real_run = subprocess.run

    def run(cmd, *a, **kw):
        if "worktree" in cmd and "remove" in cmd:
            raise subprocess.TimeoutExpired(cmd, kw.get("timeout") or 0)
        return real_run(cmd, *a, **kw)

    monkeypatch.setattr(lane_sweep.subprocess, "run", run)
    assert sweep(repo, "--apply") == 1
    assert (wt / "a.txt").read_text() == "b\n" and branch_exists(repo, "slow")
    assert git(wt, "status", "--porcelain") == ""
    assert not wt.with_name(".slow.lane-sweep-removing").exists()
    log = next((tmp_path / "logs").glob("????-??-??.log")).read_text()
    assert "timed out" in log and "lane-sweep: repos 1, removed 0" in log


@pytest.mark.req("lane-sweep/a-primary-checkout-with-a-git-lock-is-not-moved")
def test_a_primary_checkout_with_a_git_lock_is_not_moved(repo, capsys):
    old = git(repo, "rev-parse", "HEAD")
    advance_origin(repo)
    (repo / ".git" / "index.lock").write_text("")
    assert sweep(repo, "--apply") == 0
    assert git(repo, "rev-parse", "main") == old
    assert f"skip fast-forward {repo.resolve()} [main]: index.lock present" in capsys.readouterr().out


@pytest.mark.req("lane-sweep/a-lane-with-a-folder-that-cannot-be-written-is-kept-whole")
def test_a_lane_with_a_folder_that_cannot_be_written_is_kept_whole(repo, tmp_path):
    wt = lane(repo, "readonly")
    land_on_main(repo, "readonly")
    (wt / "build").mkdir()
    (wt / "build" / "out.bin").write_text("ignored output\n")
    (wt / "build").chmod(0o555)
    age(wt)
    try:
        assert sweep(repo, "--apply") == 1
        assert (wt / "a.txt").read_text() == "b\n" and (wt / ".gitignore").exists()
        assert git(wt, "status", "--porcelain") == "" and branch_exists(repo, "readonly")
        log = next((tmp_path / "logs").glob("????-??-??.log")).read_text()
        assert "cannot be written" in log and "moved back" in log
    finally:
        (wt / "build").chmod(0o755)


@pytest.mark.req("lane-sweep/the-gh-wrapper-comes-from-graph-config")
def test_the_gh_wrapper_comes_from_graph_config(tmp_path, monkeypatch):
    """An owner listed under github_accounts gets its wrapper; any other owner gets the wrapper of `owner:`."""
    config = tmp_path / "graph-config.yaml"
    config.write_text("owner: Me\ngithub_accounts:   # account -> wrapper\n  Me: gh-me\n  Team: gh-team\n"
                      "default_home: /x\ncanonical_lock: ~/tools/lock.py\n")
    monkeypatch.setattr(lane_sweep, "CONFIG", config)
    for name in ("LANE_SWEEP_GH", "PROJECT_GRAPH_OWNER", "LANE_SWEEP_CANONICAL_LOCK"):
        monkeypatch.delenv(name, raising=False)
    assert lane_sweep.gh_for("Team/repo") == "gh-team"
    assert lane_sweep.gh_for("Me/repo") == "gh-me"
    assert lane_sweep.gh_for("Upstream/repo") == "gh-me"
    assert lane_sweep.canonical_lock() == Path.home() / "tools/lock.py"
    monkeypatch.setenv("LANE_SWEEP_GH", "gh-test")
    assert lane_sweep.gh_for("Team/repo") == "gh-test"


@pytest.mark.req("lane-sweep/no-config-uses-plain-gh-and-no-canonical-lock")
def test_no_config_uses_plain_gh_and_no_canonical_lock(tmp_path, monkeypatch):
    """Without graph-config.yaml the sweep still runs: plain gh, and checkouts move with a plain merge."""
    monkeypatch.setattr(lane_sweep, "CONFIG", tmp_path / "missing.yaml")
    for name in ("LANE_SWEEP_GH", "PROJECT_GRAPH_OWNER", "LANE_SWEEP_CANONICAL_LOCK"):
        monkeypatch.delenv(name, raising=False)
    assert lane_sweep.gh_for("Anyone/repo") == "gh"
    assert lane_sweep.canonical_lock() is None
