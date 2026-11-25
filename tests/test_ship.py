"""Tests for scripts/ship.py against a throwaway repository, a bare remote and a fake gh."""

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))  # AES tests import src/; ship lives in scripts/
import ship  # noqa: E402

PLAN_LIST = "apps/plan-repos.conf"   # the plan list's path inside its checkout, in these tests

FAKE_GH = """#!/usr/bin/env python3
import json, os, sys
log = os.environ["FAKE_GH_LOG"]
open(log, "a").write(" ".join(sys.argv[1:]) + "\\n")
args = sys.argv[1:]
if args[:2] == ["pr", "view"] and "--json" in args and "state,mergeCommit" in args:
    print(json.dumps({"state": os.environ.get("FAKE_GH_STATE", "MERGED"), "mergeCommit": {"oid": "abc123"}}))
elif args[:2] == ["pr", "view"]:
    sys.exit(1)
elif args[:2] == ["pr", "list"]:
    # Only an open pull request is ever listed: the fake keeps no merged ones to return.
    print(os.environ.get("FAKE_GH_OPEN_PR", ""))
elif args[:2] == ["pr", "create"]:
    print("https://github.com/o/r/pull/7")
elif args[:2] == ["pr", "merge"]:
    # GitHub refuses a method the repository disables, and `merge` where main requires linear history.
    method = next(a[2:] for a in args if a in ("--merge", "--rebase", "--squash"))
    if method in os.environ.get("FAKE_GH_DISALLOW", "").split(",") or (
            method == "merge" and os.environ.get("FAKE_GH_LINEAR")):
        sys.stderr.write("GraphQL: Merge commits are not allowed on this repository. (mergePullRequest)\\n")
        sys.exit(1)
elif args[:2] == ["repo", "view"]:
    if os.environ.get("FAKE_GH_REPO_FAIL"):
        sys.exit(1)
    off = os.environ.get("FAKE_GH_DISALLOW", "").split(",")
    print(json.dumps({"mergeCommitAllowed": "merge" not in off, "rebaseMergeAllowed": "rebase" not in off,
                      "squashMergeAllowed": "squash" not in off,
                      "viewerDefaultMergeMethod": os.environ.get("FAKE_GH_DEFAULT", "MERGE"),
                      "defaultBranchRef": {"name": "main"}}))
elif args[:1] == ["api"] and args[1].endswith("/branches/main/protection"):
    if os.environ.get("FAKE_GH_LINEAR") == "protection":
        print(json.dumps({"required_linear_history": {"enabled": True}}))
    else:
        sys.stderr.write("Branch not protected (HTTP 404)\\n")
        sys.exit(1)
elif args[:1] == ["api"] and args[1].endswith("/rules/branches/main"):
    print(json.dumps([{"type": "required_linear_history"}] if os.environ.get("FAKE_GH_LINEAR") == "ruleset" else []))
"""

FAKE_PRIOR_ART = """import os, sys
open(os.environ["FAKE_PRIOR_ART_LOG"], "a").write(" ".join(sys.argv[1:]) + "\\n")
code = int(os.environ.get("FAKE_PRIOR_ART_EXIT", "0"))
if code == 1:
    print("add-x: no prior-art record; create openspec/changes/add-x/prior-art.json")
print(f"prior-art: 1 changes looked at, 1 need a record, {int(code == 0)} passes, {int(code == 1)} fails")
sys.exit(code)
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


def make_repo(tmp_path: Path, monkeypatch, first_commit: str, *, package: bool) -> tuple[Path, Path, Path]:
    """A clone on a feature branch whose first commit has this date, with a bare remote and a fake gh.

    With package, the first commit holds a planning package that a fake validator passes.
    """
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    work = tmp_path / "work"
    subprocess.run(["git", "init", "-q", "-b", "main", str(work)], check=True)
    git(work, "config", "user.email", "t@example.com")
    git(work, "config", "user.name", "t")
    (work / "a.txt").write_text("a\n")
    if package:
        (work / ship.PACKAGE).parent.mkdir(parents=True)
        (work / ship.PACKAGE).write_text("{}\n")
        fake_validator(tmp_path, monkeypatch, 0)
    git(work, "add", "-A")
    dated = {**os.environ, "GIT_AUTHOR_DATE": first_commit, "GIT_COMMITTER_DATE": first_commit}
    subprocess.run(["git", "-C", str(work), "commit", "-q", "-m", "base"], check=True, env=dated)
    git(work, "remote", "add", "origin", str(remote))
    git(work, "push", "-q", "origin", "main")
    git(work, "checkout", "-q", "-b", "feature")
    (work / "a.txt").write_text("b\n")
    git(work, "commit", "-q", "-am", "change")
    bindir = tmp_path / "bin"
    bindir.mkdir()
    gh = bindir / "gh"
    gh.write_text(FAKE_GH)
    gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("FAKE_GH_LOG", str(tmp_path / "gh.log"))
    monkeypatch.setenv("SHIP_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("LANE_SWEEP_LOG_DIR", str(tmp_path / "sweep-logs"))
    monkeypatch.setenv("SHIP_STATE_DIR", str(tmp_path / "state"))
    # No test reads the person's own settings; the plan list path is a test value.
    monkeypatch.setattr(ship, "CONFIG", tmp_path / "no-config" / "graph-config.yaml")
    monkeypatch.setenv("SHIP_PLAN_LIST", PLAN_LIST)
    # The fake validators need no packages; tests of the interpreter choice unset this.
    monkeypatch.setenv("SHIP_VALIDATOR_PYTHON", sys.executable)
    # A fake prior-art check in place of the bundled one; it logs its arguments and exits with FAKE_PRIOR_ART_EXIT (default 0).
    script = tmp_path / "fake-lockstep" / "prior_art.py"
    script.parent.mkdir(parents=True)
    script.write_text(FAKE_PRIOR_ART)
    monkeypatch.setattr(ship, "PRIOR_ART_CHECK", script)
    monkeypatch.setenv("SHIP_PRIOR_ART_PYTHON", sys.executable)
    monkeypatch.setenv("FAKE_PRIOR_ART_LOG", str(tmp_path / "prior-art.log"))
    return work, remote, tmp_path / "gh.log"


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """An older repository with a passing planning package: its first commit is one second before a repository counts as new."""
    return make_repo(tmp_path, monkeypatch, "2026-11-04T23:59:59+00:00", package=True)


@pytest.fixture
def unplanned_repo(tmp_path, monkeypatch):
    """An older repository with no planning package."""
    return make_repo(tmp_path, monkeypatch, "2026-11-04T23:59:59+00:00", package=False)


@pytest.fixture
def new_repo(tmp_path, monkeypatch):
    """A new repository with no planning package: its first commit is the first second that counts."""
    return make_repo(tmp_path, monkeypatch, "2026-11-05T00:00:00+00:00", package=False)


def on_remote(remote: Path, branch: str) -> bool:
    out = subprocess.run(["git", "-C", str(remote), "branch", "--list", branch], capture_output=True, text=True).stdout
    return bool(out.strip())


@pytest.mark.req("ship/a-failing-check-pushes-nothing")
def test_a_failing_check_pushes_nothing(repo):
    work, remote, _ = repo
    assert ship.main(["--repo", str(work), "--check", "exit 1"]) == 1
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-failing-check-pushes-nothing")
def test_a_check_that_fails_inside_a_pipe_pushes_nothing(repo):
    """`cmd | tail -1` used to pass when cmd failed, because only tail's exit status was read."""
    work, remote, _ = repo
    assert ship.main(["--repo", str(work), "--check", "false | cat"]) == 1
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-dirty-tree-is-refused-before-the-check")
def test_a_dirty_tree_is_refused_before_the_check(repo, tmp_path):
    work, remote, _ = repo
    (work / "a.txt").write_text("dirty\n")
    marker = tmp_path / "ran"
    assert ship.main(["--repo", str(work), "--check", f"touch {marker}"]) == 1
    assert not marker.exists()
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-passing-check-merges-the-checked-commit")
def test_a_passing_check_merges_the_checked_commit(repo):
    work, remote, gh_log = repo
    head = git(work, "rev-parse", "HEAD")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    calls = gh_log.read_text()
    assert "pr create" in calls
    assert f"pr merge 7 --merge --match-head-commit {head}" in calls
    assert list((Path(os.environ["SHIP_LOG_DIR"])).glob("*.log")), "the run is appended to the day's log"


@pytest.mark.req("ship/a-branch-whose-earlier-pull-request-merged-gets-a-new-pull-request")
def test_a_branch_whose_earlier_pull_request_merged_gets_a_new_pull_request(repo):
    work, _, gh_log = repo
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    calls = gh_log.read_text()
    assert "pr list --head feature --state open" in calls
    assert "pr view feature" not in calls, "pr view returns a merged pull request too"
    assert "pr create" in calls and "pr merge 7 " in calls


def advance_main(work: Path, path: str, text: str, *, prepend: bool = False) -> None:
    """Commit to main on the remote after the feature branch was cut, then return to the branch."""
    git(work, "checkout", "-q", "main")
    target = work / path
    old = target.read_text() if target.exists() else ""
    target.write_text(text + old if prepend else text)
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "main moved")
    git(work, "push", "-q", "origin", "main")
    git(work, "checkout", "-q", "feature")


@pytest.mark.req("ship/a-branch-behind-the-default-branch-is-rebased-and-merged")
def test_a_branch_behind_the_default_branch_is_rebased_and_merged(repo):
    work, remote, gh_log = repo
    advance_main(work, "other.txt", "other\n")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    head = git(work, "rev-parse", "HEAD")
    assert git(work, "merge-base", "--is-ancestor", "origin/main", "HEAD") == ""
    assert f"--match-head-commit {head}" in gh_log.read_text()
    assert (work / "other.txt").exists()


@pytest.mark.req("ship/two-top-entries-in-a-union-log-both-survive")
def test_two_top_entries_in_a_union_log_both_survive(repo):
    work, remote, _ = repo
    git(work, "checkout", "-q", "main")
    (work / ".gitattributes").write_text("log.md merge=union\n")
    (work / "log.md").write_text("# Log\n\n## old entry\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "log")
    git(work, "push", "-q", "origin", "main")
    git(work, "checkout", "-q", "-B", "feature")
    (work / "log.md").write_text("# Log\n\n## mine\n\n## old entry\n")
    git(work, "commit", "-q", "-am", "my entry")
    git(work, "checkout", "-q", "main")
    (work / "log.md").write_text("# Log\n\n## theirs\n\n## old entry\n")
    git(work, "commit", "-q", "-am", "their entry")
    git(work, "push", "-q", "origin", "main")
    git(work, "checkout", "-q", "feature")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    log = (work / "log.md").read_text()
    assert "## mine" in log and "## theirs" in log and "## old entry" in log


@pytest.mark.req("ship/a-conflicting-rebase-pushes-nothing")
def test_a_conflicting_rebase_pushes_nothing(repo, capsys):
    work, remote, _ = repo
    before = git(work, "rev-parse", "HEAD")
    advance_main(work, "a.txt", "c\n")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert "a.txt" in capsys.readouterr().out
    assert git(work, "rev-parse", "HEAD") == before
    assert git(work, "status", "--porcelain") == ""
    assert not (work / ".git" / "rebase-merge").exists() and not (work / ".git" / "rebase-apply").exists()
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-branch-already-on-the-remote-is-not-rebased")
def test_a_branch_already_on_the_remote_is_not_rebased(repo, capsys):
    work, remote, gh_log = repo
    git(work, "push", "-q", "origin", "feature")
    before = git(work, "rev-parse", "HEAD")
    advance_main(work, "other.txt", "other\n")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert git(work, "rev-parse", "HEAD") == before
    assert "on the remote" in capsys.readouterr().out


@pytest.mark.req("ship/a-merge-that-does-not-read-back-as-merged-fails")
def test_a_merge_that_does_not_read_back_as_merged_fails(repo, monkeypatch):
    work, _, _ = repo
    monkeypatch.setenv("FAKE_GH_STATE", "OPEN")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1


def merge_call(gh_log: Path) -> str:
    """The `gh pr merge` line the fake gh logged, or an empty string."""
    return next((line for line in gh_log.read_text().splitlines() if line.startswith("pr merge")), "")


@pytest.mark.req("ship/a-repository-that-requires-linear-history-is-merged-by-rebase")
@pytest.mark.parametrize("how", ["protection", "ruleset"])
def test_a_repository_that_requires_linear_history_is_merged_by_rebase(repo, monkeypatch, how):
    """llm_client#321: the default method was merge, main required linear history, and GitHub refused the merge."""
    work, _, gh_log = repo
    monkeypatch.setenv("FAKE_GH_LINEAR", how)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert "--rebase" in merge_call(gh_log) and "--merge" not in merge_call(gh_log)


@pytest.mark.req("ship/a-merge-method-that-the-repository-does-not-allow-is-replaced-before-the-check")
def test_a_merge_method_that_the_repository_does_not_allow_is_replaced(repo, monkeypatch, capsys):
    work, _, gh_log = repo
    monkeypatch.setenv("FAKE_GH_LINEAR", "protection")
    assert ship.main(["--repo", str(work), "--check", "true", "--method", "merge"]) == 0
    assert "--rebase" in merge_call(gh_log)
    out = capsys.readouterr().out
    assert "merge is not allowed" in out and "using rebase" in out


@pytest.mark.req("ship/an-allowed-method-that-was-asked-for-is-used", existing=True)   # old ship honored --method too
def test_an_allowed_method_that_was_asked_for_is_used(repo, monkeypatch):
    work, _, gh_log = repo
    assert ship.main(["--repo", str(work), "--check", "true", "--method", "squash"]) == 0
    assert "--squash" in merge_call(gh_log)


@pytest.mark.req("ship/a-ruleset-that-requires-linear-history-is-honored-too")
def test_a_ruleset_that_requires_linear_history_is_honored_too(repo, monkeypatch):
    work, _, gh_log = repo
    monkeypatch.setenv("FAKE_GH_LINEAR", "ruleset")
    assert ship.main(["--repo", str(work), "--check", "true", "--method", "merge"]) == 0
    assert "--rebase" in merge_call(gh_log)


@pytest.mark.req("ship/a-repository-that-disables-a-method-falls-back-to-the-allowed-ones")
def test_a_repository_that_disables_a_method_falls_back_to_the_allowed_ones(repo, monkeypatch):
    work, _, gh_log = repo
    monkeypatch.setenv("FAKE_GH_DISALLOW", "merge")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert "--rebase" in merge_call(gh_log)


@pytest.mark.req("ship/a-repository-that-disables-a-method-falls-back-to-the-allowed-ones")
def test_the_repository_default_is_used_when_it_is_allowed(repo, monkeypatch):
    work, _, gh_log = repo
    monkeypatch.setenv("FAKE_GH_LINEAR", "protection")
    monkeypatch.setenv("FAKE_GH_DEFAULT", "SQUASH")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert "--squash" in merge_call(gh_log)


@pytest.mark.req("ship/a-repository-that-allows-no-merge-method-stops-before-the-check")
def test_a_repository_that_allows_no_merge_method_stops_before_the_check(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    ran = tmp_path / "check-ran"
    monkeypatch.setenv("FAKE_GH_LINEAR", "protection")
    monkeypatch.setenv("FAKE_GH_DISALLOW", "rebase,squash")
    assert ship.main(["--repo", str(work), "--check", f"touch {ran}"]) == 1
    assert not ran.exists(), "the check must not run when no method could merge its result"
    assert not on_remote(remote, "feature")
    assert "no merge method is allowed" in capsys.readouterr().out


@pytest.mark.req("ship/the-merge-settings-are-read-before-the-check")
def test_the_merge_settings_are_read_before_the_check(repo):
    work, _, _ = repo
    # Exits 0 only when the fake gh already logged `repo view`, i.e. the settings were read first.
    assert ship.main(["--repo", str(work), "--check", 'grep -q "repo view" "$FAKE_GH_LOG"']) == 0


@pytest.mark.req("ship/settings-that-cannot-be-read-leave-the-method-unchanged")
def test_settings_that_cannot_be_read_leave_the_method_unchanged(repo, monkeypatch, capsys):
    work, _, gh_log = repo
    monkeypatch.setenv("FAKE_GH_REPO_FAIL", "1")
    assert ship.main(["--repo", str(work), "--check", "true", "--method", "squash"]) == 0
    assert "--squash" in merge_call(gh_log)
    assert "unreadable" in capsys.readouterr().out


FAKE_VALIDATOR = """import os, sys
print("fake validator", " ".join(sys.argv[1:]))
if "--no-freshness" in sys.argv and os.environ.get("FAKE_VALIDATOR_AGE_ONLY") == "1":
    sys.exit(0)
sys.exit(int(os.environ.get("FAKE_VALIDATOR_EXIT", "0")))
"""


def fake_validator(tmp_path: Path, monkeypatch, exit_status: int) -> None:
    validator = tmp_path / "validate_planning_package.py"
    validator.write_text(FAKE_VALIDATOR)
    monkeypatch.setenv("SHIP_PLANNING_VALIDATOR", str(validator))
    monkeypatch.setenv("FAKE_VALIDATOR_EXIT", str(exit_status))


def with_package(work: Path, tmp_path: Path, monkeypatch, exit_status: int) -> None:
    """Commit a planning package if there is none, and make the fake validator exit with this status."""
    if not (work / ship.PACKAGE).is_file():
        (work / ship.PACKAGE).parent.mkdir(parents=True)
        (work / ship.PACKAGE).write_text("{}\n")
        git(work, "add", "-A")
        git(work, "commit", "-q", "-m", "package")
    fake_validator(tmp_path, monkeypatch, exit_status)


@pytest.mark.req("ship/a-failing-planning-package-pushes-nothing")
def test_a_failing_planning_package_pushes_nothing(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    with_package(work, tmp_path, monkeypatch, 1)
    marker = tmp_path / "ran"
    assert ship.main(["--repo", str(work), "--check", f"touch {marker}"]) == 1
    assert not marker.exists(), "the check does not run after the package fails"
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-package-that-is-only-out-of-date-warns-and-proceeds")
def test_a_package_that_is_only_out_of_date_warns_and_proceeds(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    with_package(work, tmp_path, monkeypatch, 1)
    monkeypatch.setenv("FAKE_VALIDATOR_AGE_ONLY", "1")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "is out of date" in capsys.readouterr().out


@pytest.mark.req("ship/a-compliant-planning-package-lets-the-merge-proceed")
def test_a_compliant_planning_package_lets_the_merge_proceed(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    with_package(work, tmp_path, monkeypatch, 0)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "planning package" in capsys.readouterr().out


def plan_list(tmp_path: Path, monkeypatch, text: str) -> None:
    """A personal-vps clone whose origin/main is behind its remote until fetched, as after a merge on GitHub."""
    remote = tmp_path / "vps.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    clone, author = tmp_path / "vps", tmp_path / "vps-author"
    for path in (clone, author):
        subprocess.run(["git", "clone", "-q", str(remote), str(path)], check=True, capture_output=True)
    conf = author / PLAN_LIST
    conf.parent.mkdir(parents=True)
    conf.write_text(text)
    git(author, "add", "-A")
    git(author, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "plan list")
    git(author, "push", "-q", "origin", "HEAD:main")
    monkeypatch.setenv("SHIP_PERSONAL_VPS", str(clone))


@pytest.mark.req("ship/an-older-repository-with-no-package-merges-with-a-warning")
def test_an_older_repository_with_no_package_merges_with_a_warning(unplanned_repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = unplanned_repo
    started = tmp_path / "agent-started"
    claude = tmp_path / "bin" / "claude"
    claude.write_text(f"#!/bin/sh\ntouch {started}\n")
    claude.chmod(claude.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("SHIP_PERSONAL_VPS", str(tmp_path / "no-such-repo"))   # the plan list is not consulted
    marker = tmp_path / "ran"
    assert ship.main(["--repo", str(work), "--check", f"touch {marker}"]) == 0
    assert marker.exists(), "the check runs"
    assert on_remote(remote, "feature")
    out = capsys.readouterr().out
    assert "warning" in out and "no planning package" in out and "company-planning:planning-compliance" in out
    assert not started.exists(), "no detached agent is started"


@pytest.mark.req("ship/an-older-repository-with-a-passing-package-merges")
def test_an_older_repository_with_a_passing_package_merges(unplanned_repo, tmp_path, monkeypatch):
    work, remote, _ = unplanned_repo
    with_package(work, tmp_path, monkeypatch, 0)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")


@pytest.mark.req("ship/a-new-repository-with-no-package-is-refused")
def test_a_new_repository_with_no_package_is_refused(new_repo, tmp_path, capsys):
    work, remote, _ = new_repo
    marker = tmp_path / "ran"
    assert ship.main(["--repo", str(work), "--check", f"touch {marker}"]) == 1
    assert not marker.exists()
    assert not on_remote(remote, "feature")
    out = capsys.readouterr().out
    assert "new repository" in out and "company-planning:planning-compliance" in out


@pytest.mark.req("ship/a-new-repository-whose-package-is-not-on-the-plan-list-is-refused")
def test_a_new_repository_whose_package_is_not_on_the_plan_list_is_refused(new_repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = new_repo
    with_package(work, tmp_path, monkeypatch, 0)
    plan_list(tmp_path, monkeypatch, "# name visibility URL\nother  private  github-plans-other:o/other.git\n"
                                     "# remote  private  github-plans-remote:o/remote.git\n")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert not on_remote(remote, "feature")
    out = capsys.readouterr().out
    assert "new-repository rule" in out and PLAN_LIST in out
    assert "private     github-plans-remote:" in out and "/remote.git" in out, "names the exact line to add"


@pytest.mark.req("ship/a-new-repository-with-a-package-on-the-plan-list-proceeds")
def test_a_new_repository_with_a_package_on_the_plan_list_proceeds(new_repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = new_repo
    with_package(work, tmp_path, monkeypatch, 0)
    plan_list(tmp_path, monkeypatch, "remote  private  github-plans-remote:BrianMills2718/remote.git\n")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "is on the plan list" in capsys.readouterr().out


@pytest.mark.req("ship/a-new-repository-with-a-package-on-the-plan-list-proceeds")
def test_a_new_repository_on_the_plan_list_must_still_pass_the_validator(new_repo, tmp_path, monkeypatch):
    work, remote, _ = new_repo
    with_package(work, tmp_path, monkeypatch, 1)
    plan_list(tmp_path, monkeypatch, "remote  private  github-plans-remote:BrianMills2718/remote.git\n")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/an-unreadable-plan-list-refuses")
def test_an_unreadable_plan_list_refuses(new_repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = new_repo
    with_package(work, tmp_path, monkeypatch, 0)
    monkeypatch.setenv("SHIP_PERSONAL_VPS", str(tmp_path / "no-such-repo"))
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert not on_remote(remote, "feature")
    out = capsys.readouterr().out
    assert "new-repository rule" in out and "could not read" in out


@pytest.mark.req("ship/a-compliant-planning-package-lets-the-merge-proceed")
def test_an_older_repository_with_a_package_needs_no_plan_list(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    with_package(work, tmp_path, monkeypatch, 0)
    monkeypatch.setenv("SHIP_PERSONAL_VPS", str(tmp_path / "no-such-repo"))
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")


@pytest.mark.req("ship/a-validator-that-cannot-run-stops-the-merge")
def test_a_validator_that_cannot_run_stops_the_merge(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    with_package(work, tmp_path, monkeypatch, 0)
    monkeypatch.setenv("SHIP_PLANNING_VALIDATOR", str(tmp_path / "missing.py"))
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-validator-that-cannot-run-stops-the-merge")
def test_an_unreachable_company_planning_stops_the_merge(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    with_package(work, tmp_path, monkeypatch, 0)
    monkeypatch.delenv("SHIP_PLANNING_VALIDATOR")
    monkeypatch.setenv("SHIP_COMPANY_PLANNING", str(tmp_path / "no-such-repo"))
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert not on_remote(remote, "feature")


IMPORTING_VALIDATOR = """import sys
import a_module_that_is_not_installed
sys.exit(0)
"""

PROBED_PYTHON = """#!{python}
import os, sys
if sys.argv[1] == "-c":
    sys.exit(0)             # the probe: this interpreter has the validator's packages
open(os.environ["PROBED_PYTHON_LOG"], "a").write("ran\\n")
os.execv({python!r}, [{python!r}, *sys.argv[1:]])
"""


def probed_python(tmp_path: Path, name: str) -> Path:
    """An interpreter stand-in that passes the import probe and logs each validator run to PROBED_PYTHON_LOG."""
    script = tmp_path / name
    script.write_text(PROBED_PYTHON.format(python=sys.executable))
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return script


@pytest.mark.req("ship/the-validator-runs-under-an-interpreter-that-has-its-packages")
def test_the_validator_runs_under_a_fixed_interpreter_not_the_callers(repo, tmp_path, monkeypatch):
    """ship called from a project venv (uv run) used that venv's python, which lacked jsonschema."""
    work, remote, _ = repo
    with_package(work, tmp_path, monkeypatch, 0)
    log = tmp_path / "interpreter.log"
    monkeypatch.setenv("PROBED_PYTHON_LOG", str(log))
    monkeypatch.delenv("SHIP_VALIDATOR_PYTHON")
    monkeypatch.setattr(ship, "VALIDATOR_PYTHONS", ([str(tmp_path / "not-installed")], [str(probed_python(tmp_path, "good"))]))
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert log.read_text() == "ran\n", "the first candidate that has the packages ran the validator, once"
    assert on_remote(remote, "feature")


@pytest.mark.req("ship/the-validator-runs-under-an-interpreter-that-has-its-packages")
def test_an_interpreter_named_by_the_environment_runs_the_validator(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    with_package(work, tmp_path, monkeypatch, 0)
    log = tmp_path / "interpreter.log"
    monkeypatch.setenv("PROBED_PYTHON_LOG", str(log))
    monkeypatch.setenv("SHIP_VALIDATOR_PYTHON", str(probed_python(tmp_path, "named")))
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert log.read_text() == "ran\n"


@pytest.mark.req("ship/a-validator-that-cannot-run-is-not-reported-as-a-failing-package")
def test_no_interpreter_with_the_packages_stops_the_merge_as_could_not_run(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    with_package(work, tmp_path, monkeypatch, 0)
    monkeypatch.delenv("SHIP_VALIDATOR_PYTHON")
    monkeypatch.setattr(ship, "VALIDATOR_PYTHONS", ([str(tmp_path / "not-installed")], [sys.executable]))
    monkeypatch.setattr(ship, "VALIDATOR_IMPORTS", "import a_module_that_is_not_installed")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    out = capsys.readouterr().out
    assert "could not run" in out and "not compliant" not in out
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-validator-that-cannot-run-is-not-reported-as-a-failing-package")
def test_a_validator_that_fails_to_import_is_not_reported_as_a_failing_package(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    with_package(work, tmp_path, monkeypatch, 0)
    validator = tmp_path / "validate_planning_package.py"
    validator.write_text(IMPORTING_VALIDATOR)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    out = capsys.readouterr().out
    assert "could not run" in out and "a_module_that_is_not_installed" in out
    assert "not compliant" not in out
    assert "without the freshness check" not in out, "an import error is not retried as a freshness-only failure"
    assert not on_remote(remote, "feature")


@pytest.mark.req("lane-sweep/a-shipped-lane-is-removed-right-after-merge")
def test_a_shipped_lane_is_removed_right_after_merge(repo, tmp_path):
    work, remote, _ = repo
    git(work, "checkout", "-q", "main")
    lane = tmp_path / "lane"
    git(work, "worktree", "add", "-q", "-b", "shipped", str(lane))
    (lane / "a.txt").write_text("shipped\n")
    git(lane, "commit", "-q", "-am", "shipped change")
    # The fake gh merges nothing, so put the lane's commit on the remote main as the real merge would.
    git(lane, "push", "-q", "origin", "HEAD:main")
    assert ship.main(["--repo", str(lane), "--check", "true"]) == 0
    assert not lane.exists()
    assert not git(work, "branch", "--list", "shipped")


def shipped_lane(work: Path, tmp_path: Path, name: str) -> Path:
    """A lane with one commit, put on the remote main as the real merge would (the fake gh merges nothing)."""
    lane = tmp_path / name
    git(work, "worktree", "add", "-q", "-b", name, str(lane), "main")
    (lane / f"{name}.txt").write_text(name + "\n")
    git(lane, "add", f"{name}.txt")
    git(lane, "commit", "-q", "-m", f"{name} change")
    git(lane, "push", "-q", "origin", "HEAD:main")
    return lane


def make_idle(lane: Path) -> None:
    """Age the lane's HEAD, index and reflog past the sweep's idle wait."""
    gitdir = Path(git(lane, "rev-parse", "--absolute-git-dir"))
    old = os.path.getmtime(gitdir / "HEAD") - 3 * 86400
    for f in (gitdir / "HEAD", gitdir / "index", gitdir / "logs" / "HEAD"):
        if f.exists():
            os.utime(f, (old, old))


@pytest.mark.req("ship/keep-lane-leaves-this-lane-and-sweeps-the-others")
def test_keep_lane_leaves_this_lane_and_sweeps_the_others(repo, tmp_path, capsys):
    work, remote, _ = repo
    git(work, "checkout", "-q", "main")
    other = shipped_lane(work, tmp_path, "other")
    git(work, "pull", "-q", "--ff-only", "origin", "main")
    lane = shipped_lane(work, tmp_path, "kept")
    make_idle(other)
    assert ship.main(["--repo", str(lane), "--check", "true", "--keep-lane"]) == 0
    assert "ship: kept this lane (--keep-lane); the periodic sweep removes it once idle" in capsys.readouterr().out
    assert lane.exists()
    assert git(work, "branch", "--list", "kept")
    assert not other.exists()
    assert not git(work, "branch", "--list", "other")


@pytest.mark.req("ship/the-environment-variable-keeps-the-lane-too")
def test_the_environment_variable_keeps_the_lane_too(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    git(work, "checkout", "-q", "main")
    lane = shipped_lane(work, tmp_path, "kept")
    monkeypatch.setenv("SHIP_KEEP_LANE", "1")
    assert ship.main(["--repo", str(lane), "--check", "true"]) == 0
    assert lane.exists()
    assert git(work, "branch", "--list", "kept")


@pytest.mark.req("ship/the-lane-sweep-is-found-beside-the-real-ship", existing=True)
def test_the_lane_sweep_is_found_when_ship_runs_through_its_symlink(tmp_path, monkeypatch):
    """~/.local/bin/ship is a symlink: the sweep looked for ~/.local/bin/lane_sweep.py and exited 2 (2026-10-25, #39 and #41)."""
    link = tmp_path / "bin" / "ship"
    link.parent.mkdir()
    link.symlink_to(Path(ship.__file__).resolve())
    monkeypatch.setattr(ship, "__file__", str(link))
    assert ship.sweep_script() == Path(ship.__file__).resolve().with_name("lane_sweep.py")
    assert ship.sweep_script().is_file()


FAKE_TOOL = """#!/usr/bin/env python3
import os, sys
name = os.path.basename(sys.argv[0])
open(os.environ["FAKE_TOOL_LOG"], "a").write(name + " " + " ".join(sys.argv[1:]) + "\\n")
code = int(os.environ.get(f"FAKE_{name.upper()}_EXIT", "0"))
if code == 0 or os.environ.get("FAKE_TOOL_LEAVE"):   # a failed uv sync can leave an empty .venv
    os.makedirs({"uv": ".venv", "npm": "node_modules"}[name], exist_ok=True)
sys.exit(code)
"""


def fake_env_tools(work: Path, tmp_path: Path, monkeypatch, *, node: bool = True, make_check: str | None = None) -> Path:
    """Commit a Python (and Node) project and put a fake uv and npm first on PATH; return their call log.

    With make_check, the project also has a Makefile whose `check` target runs that command.
    """
    (work / "pyproject.toml").write_text("[project]\nname = 'x'\n")
    if make_check is not None:
        (work / "Makefile").write_text(f"check:\n\t{make_check}\n")
    (work / ".gitignore").write_text(".venv/\nnode_modules/\n")
    if node:
        (work / "package-lock.json").write_text("{}\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "project files")
    for name in ("uv", "npm"):
        tool = tmp_path / "bin" / name
        tool.write_text(FAKE_TOOL)
        tool.chmod(tool.stat().st_mode | stat.S_IEXEC)
    log = tmp_path / "tools.log"
    monkeypatch.setenv("FAKE_TOOL_LOG", str(log))
    return log


@pytest.mark.req("ship/a-fresh-worktree-gets-its-environment-before-the-check")
def test_a_fresh_worktree_gets_its_environment_before_the_check(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    log = fake_env_tools(work, tmp_path, monkeypatch, make_check="test -d .venv && test -d node_modules")
    assert ship.main(["--repo", str(work)]) == 0   # the default check is the Makefile's `make check`
    assert log.read_text().splitlines() == ["uv sync --all-extras", "npm ci"]
    assert on_remote(remote, "feature")
    (work / "a.txt").write_text("c\n")
    git(work, "commit", "-q", "-am", "another change")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert log.read_text().splitlines() == ["uv sync --all-extras", "npm ci"], "a present environment is left alone"


@pytest.mark.req("ship/a-failing-environment-setup-pushes-nothing")
def test_a_failing_environment_setup_pushes_nothing(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    marker = tmp_path / "ran"
    log = fake_env_tools(work, tmp_path, monkeypatch, node=False, make_check=f"touch {marker}")
    monkeypatch.setenv("FAKE_UV_EXIT", "1")
    assert ship.main(["--repo", str(work), "--check", "make check"]) == 1
    assert log.read_text().splitlines() == ["uv sync --all-extras"]
    assert not marker.exists()
    assert not on_remote(remote, "feature")
    assert "nothing was pushed" in capsys.readouterr().out


@pytest.mark.req("ship/a-failing-environment-setup-leaves-no-empty-folder")
def test_a_failing_environment_setup_leaves_no_empty_folder(repo, tmp_path, monkeypatch):
    work, _, _ = repo
    fake_env_tools(work, tmp_path, monkeypatch, make_check="true")
    monkeypatch.setenv("FAKE_UV_EXIT", "1")
    monkeypatch.setenv("FAKE_TOOL_LEAVE", "1")   # the failing uv leaves an empty .venv, as the real one can
    assert ship.main(["--repo", str(work)]) == 1
    assert not (work / ".venv").exists(), "an empty .venv would read as a present environment on the next run"
    assert (work / "node_modules").exists() is False


@pytest.mark.req("ship/a-custom-check-does-not-sync-the-python-environment")
def test_a_custom_check_does_not_sync_the_python_environment(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    marker = tmp_path / "ran"
    log = fake_env_tools(work, tmp_path, monkeypatch, node=False, make_check="false")
    monkeypatch.setenv("FAKE_UV_EXIT", "1")   # a sync would fail, as it does for a project with an unbuildable extra
    assert ship.main(["--repo", str(work), "--check", f"touch {marker}"]) == 0
    assert not log.exists(), "uv was not called"
    assert marker.exists()
    assert on_remote(remote, "feature")
    assert "skipped: the check" in capsys.readouterr().out


@pytest.mark.req("ship/a-custom-check-does-not-sync-the-python-environment")
@pytest.mark.parametrize("check,makefile", [("make check", True), ("make -s check", True), ("CI=1 make check", True),
                                            ("bash hooks/test.sh", False), ("uv run pytest", False), ("", False),
                                            ("echo 'unclosed", False)])
def test_only_a_make_command_is_a_makefile_check(check, makefile):
    assert ship.is_makefile_check(check) is makefile


def counting_check(tmp_path: Path) -> tuple[str, Path]:
    """A check that appends a line outside the repository each time it runs."""
    count = tmp_path / "check-runs"
    return f"echo run >> {count}", count


def runs(count: Path) -> int:
    return len(count.read_text().splitlines()) if count.exists() else 0


@pytest.mark.req("ship/a-tree-that-already-passed-skips-the-check")
def test_a_tree_that_already_passed_skips_the_check(repo, tmp_path, capsys):
    work, _, gh_log = repo
    check, count = counting_check(tmp_path)
    tree = git(work, "rev-parse", "HEAD^{tree}")
    assert ship.main(["--repo", str(work), "--check", check]) == 0
    assert runs(count) == 1
    record = [json.loads(line) for line in (tmp_path / "state" / "passed.jsonl").read_text().splitlines()]
    assert record[0]["tree"] == tree and record[0]["check"] == check
    assert {"repo", "head", "time"} <= set(record[0])
    git(work, "checkout", "-q", "-b", "feature-again")
    git(work, "commit", "-q", "--amend", "-m", "same tree, new head")
    head = git(work, "rev-parse", "HEAD")
    capsys.readouterr()
    assert ship.main(["--repo", str(work), "--check", check]) == 0
    assert runs(count) == 1, "the check did not run again"
    out = capsys.readouterr().out
    assert f"ship: check skipped: tree {tree[:12]} already passed `{check}` at" in out
    assert f"--match-head-commit {head}" in gh_log.read_text()
    logged = "".join(p.read_text() for p in Path(os.environ["SHIP_LOG_DIR"]).glob("*.log"))
    assert "check skipped" in logged


@pytest.mark.req("ship/recheck-runs-the-check-again")
def test_recheck_runs_the_check_again(repo, tmp_path):
    work, _, _ = repo
    check, count = counting_check(tmp_path)
    assert ship.main(["--repo", str(work), "--check", check]) == 0
    assert ship.main(["--repo", str(work), "--check", check, "--recheck"]) == 0
    assert runs(count) == 2


@pytest.mark.req("ship/a-different-check-command-or-a-failed-check-is-not-skipped")
def test_a_different_check_command_or_a_failed_check_is_not_skipped(repo, tmp_path):
    work, _, _ = repo
    check, count = counting_check(tmp_path)
    assert ship.main(["--repo", str(work), "--check", f"{check}; exit 1"]) == 1
    assert ship.main(["--repo", str(work), "--check", check]) == 0
    assert runs(count) == 2, "a failed check recorded nothing"
    assert ship.main(["--repo", str(work), "--check", f"{check} # other"]) == 0
    assert runs(count) == 3, "another check command is not skipped"
    assert ship.main(["--repo", str(work), "--check", check]) == 0
    assert runs(count) == 3, "the first command is now skipped"


@pytest.mark.req("ship/a-plan-repair-merges-while-the-package-fails")
def test_a_branch_that_only_repairs_the_plan_merges_while_the_package_fails(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    git(work, "reset", "-q", "--hard", "main")          # drop the fixture's code change on the branch
    (work / "docs" / "planning" / "open-questions.json").write_text("[]\n")
    (work / "NOTES.md").write_text("plan notes\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "repair the plan")
    with_package(work, tmp_path, monkeypatch, 1)        # the package still fails
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "changes only planning and documentation files (2)" in capsys.readouterr().out


@pytest.mark.req("ship/a-plan-repair-never-breaks-a-passing-package")
def test_a_docs_branch_cannot_make_a_passing_package_fail(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    git(work, "reset", "-q", "--hard", "main")
    with_package(work, tmp_path, monkeypatch, 0)        # the package passes on the base ...
    git(work, "push", "-q", "origin", "HEAD:main")
    git(work, "fetch", "-q", "origin")
    (work / "docs" / "plan.md").write_text("a docs-only change\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "docs")
    # ... and fails once the branch is applied: the fake validator keys off the docs file
    validator = tmp_path / "v.py"
    validator.write_text("import sys, pathlib\n"
                         "repo = sys.argv[sys.argv.index('--repo') + 1]\n"
                         "sys.exit(1 if (pathlib.Path(repo) / 'docs' / 'plan.md').exists() else 0)\n")
    monkeypatch.setenv("SHIP_PLANNING_VALIDATOR", str(validator))
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-failing-planning-package-pushes-nothing")
def test_a_code_change_beside_a_plan_repair_is_still_refused(repo, tmp_path, monkeypatch):
    work, remote, _ = repo                              # the fixture's branch changes a.txt
    (work / "docs" / "planning" / "open-questions.json").write_text("[]\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "plan and code")
    with_package(work, tmp_path, monkeypatch, 1)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert not on_remote(remote, "feature")


# A validator with the freshness entry point: plan content here is docs/planning/plan.md and docs/GOAL.md. It logs
# the revision freshness() was given, and when run as a script behaves like FAKE_VALIDATOR.
FRESH_VALIDATOR = """#!/usr/bin/env python3
import os, subprocess, sys
PLAN = ("docs/planning/plan.md", "docs/GOAL.md")
def freshness(repo, manifest_path, manifest):
    rev = ((manifest.get("parts") or {}).get("cold_review") or {}).get("reviewed_revision") or manifest.get("subject_revision")
    with open(os.environ["FAKE_FRESH_LOG"], "a") as fh:
        fh.write(str(rev) + "\\n")
    out = subprocess.run(["git", "-C", str(repo), "diff", "--name-only", rev, "HEAD", "--", *PLAN],
                         capture_output=True, text=True).stdout.split()
    return {"ok": not out, "changed": out, "problems": ["changed: " + ", ".join(out)] if out else []}
if __name__ == "__main__":
    print("fake validator", " ".join(sys.argv[1:]))
    sys.exit(int(os.environ.get("FAKE_VALIDATOR_EXIT", "0")))
"""


def fresh_validator(work: Path, tmp_path: Path, monkeypatch, exit_status: int) -> Path:
    """Use FRESH_VALIDATOR with this exit status; return the log of revisions freshness() was given."""
    with_package(work, tmp_path, monkeypatch, exit_status)
    validator = tmp_path / "fresh_validator.py"
    validator.write_text(FRESH_VALIDATOR)
    monkeypatch.setenv("SHIP_PLANNING_VALIDATOR", str(validator))
    log = tmp_path / "fresh.log"
    monkeypatch.setenv("FAKE_FRESH_LOG", str(log))
    return log


@pytest.mark.req("ship/a-code-only-merge-skips-the-validator")
def test_a_code_only_merge_skips_the_validator(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo                              # the fixture's branch changes only a.txt
    log = fresh_validator(work, tmp_path, monkeypatch, 1)   # the validator would reject the package
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    out = capsys.readouterr().out
    assert "skipped the planning validator" in out and "no plan content" in out
    assert "fake validator" not in out, "the validator does not run"
    assert on_remote(remote, "feature")
    assert log.read_text().split() == [git(work, "merge-base", "HEAD", "origin/main")], "asked from the merge base"


@pytest.mark.req("ship/a-plan-change-is-validated", existing=True)   # validation already ran on every merge; this guards it
def test_a_plan_change_is_validated(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    (work / "docs" / "planning" / "plan.md").write_text("a new plan\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "plan and code")
    fresh_validator(work, tmp_path, monkeypatch, 1)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    out = capsys.readouterr().out
    assert "fake validator" in out and "skipped the planning validator" not in out
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-plan-change-is-validated", existing=True)   # validation already ran on every merge; this guards it
def test_a_plan_change_that_passes_merges(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    (work / "docs" / "GOAL.md").write_text("goal\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "goal")
    fresh_validator(work, tmp_path, monkeypatch, 0)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert "fake validator" in capsys.readouterr().out
    assert on_remote(remote, "feature")


@pytest.mark.req("ship/a-plan-change-is-validated", existing=True)   # validation already ran on every merge; this guards it
def test_a_change_to_the_package_itself_is_validated(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    (work / ship.PACKAGE).write_text('{"initiative": "x"}\n')
    git(work, "commit", "-q", "-am", "package")
    fresh_validator(work, tmp_path, monkeypatch, 1)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert "fake validator" in capsys.readouterr().out
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-validator-without-the-freshness-entry-point-validates-every-merge", existing=True)   # validation already ran on every merge; this guards it
def test_a_validator_without_the_freshness_entry_point_validates_every_merge(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo                              # code only, but FAKE_VALIDATOR has no freshness()
    with_package(work, tmp_path, monkeypatch, 1)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert "fake validator" in capsys.readouterr().out
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-plan-repair-merges-while-the-package-fails")
def test_a_plan_repair_still_validates_the_merge_base(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    git(work, "reset", "-q", "--hard", "main")          # drop the fixture's code change on the branch
    with_package(work, tmp_path, monkeypatch, 1)
    git(work, "push", "-q", "origin", "HEAD:main")      # the failing package is on main ...
    git(work, "fetch", "-q", "origin")
    (work / "docs" / "planning" / "plan.md").write_text("repaired plan\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "repair the plan")
    fresh_validator(work, tmp_path, monkeypatch, 1)     # ... and still fails on the branch
    # The merge base changes nothing against itself; it must still be validated (and fail), so the repair merges.
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert "changes only planning and documentation files" in capsys.readouterr().out
    assert on_remote(remote, "feature")


CP_VALIDATOR = """#!/usr/bin/env python3
import sys
from pathlib import Path
goals = Path(__file__).resolve().parents[3] / "scripts" / "goal_provenance.py"
if not goals.is_file():
    print("Verdict: compliant (validator without goal provenance)")
    sys.exit(0)
mark = goals.read_text().strip()
print(f"{mark} goal provenance: every goal part names its source (required from 2026-11-13) (1 goal page)")
sys.exit(1 if mark == "FAIL" else 0)
"""


def company_planning(tmp_path: Path, monkeypatch, goal_mark: str | None) -> None:
    """A company-planning clone whose origin/main holds a validator and, unless goal_mark is None, goal_provenance.py.

    The fake validator finds goal_provenance.py where the real one does (three folders up, then scripts/),
    prints the goal provenance line with goal_mark, and exits 1 only for FAIL.
    """
    origin = tmp_path / "cp-origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
    cp = tmp_path / "company-planning"
    subprocess.run(["git", "init", "-q", "-b", "main", str(cp)], check=True)
    git(cp, "config", "user.email", "t@example.com")
    git(cp, "config", "user.name", "t")
    validator = cp / ship.VALIDATOR
    validator.parent.mkdir(parents=True)
    validator.write_text(CP_VALIDATOR)
    if goal_mark is not None:
        goals = cp / ship.GOAL_PROVENANCE[0]
        goals.parent.mkdir(parents=True, exist_ok=True)
        goals.write_text(goal_mark + "\n")
        (cp / ship.GOAL_PROVENANCE[1]).write_text("name: prompt\n")
    git(cp, "add", "-A")
    git(cp, "commit", "-q", "-m", "validator")
    git(cp, "remote", "add", "origin", str(origin))
    git(cp, "push", "-q", "origin", "main")
    monkeypatch.delenv("SHIP_PLANNING_VALIDATOR", raising=False)
    monkeypatch.setenv("SHIP_COMPANY_PLANNING", str(cp))


@pytest.mark.req("ship/the-goal-provenance-check-is-extracted-beside-the-validator")
def test_the_goal_provenance_check_is_extracted_beside_the_validator(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    company_planning(tmp_path, monkeypatch, "WAIT")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    out = capsys.readouterr().out
    assert "ship: goal provenance: WAIT (required from 2026-11-13)" in out
    assert on_remote(remote, "feature")


@pytest.mark.req("ship/a-goal-provenance-failure-refuses-the-merge")
def test_a_goal_provenance_failure_refuses_the_merge(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    company_planning(tmp_path, monkeypatch, "FAIL")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert "ship: goal provenance: FAIL (required from 2026-11-13)" in capsys.readouterr().out
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/an-older-company-planning-without-the-check-still-validates", existing=True)
def test_an_older_company_planning_without_the_check_still_validates(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    company_planning(tmp_path, monkeypatch, None)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    out = capsys.readouterr().out
    assert "validator without goal provenance" in out
    assert "ship: goal provenance:" not in out
    assert on_remote(remote, "feature")


def upkeep_branch(work: Path, new_line: str) -> None:
    """Put a file naming a model on main, then change it on the feature branch to new_line."""
    git(work, "checkout", "-q", "main")
    (work / "llm.py").write_text('MODEL = "openrouter/openai/gpt-5.6-luna"\nTIMEOUT = 30\n')
    (work / "poetry.lock").write_text("old\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "model on main")
    git(work, "push", "-q", "origin", "main")
    git(work, "checkout", "-q", "feature")
    git(work, "reset", "-q", "--hard", "main")
    (work / "llm.py").write_text(new_line)
    (work / "poetry.lock").write_text("new\n")
    git(work, "commit", "-q", "-am", "update model")


@pytest.mark.req("ship/an-upkeep-only-branch-merges-without-a-package")
def test_an_upkeep_only_branch_merges_in_a_repository_with_no_package(new_repo, capsys):
    work, remote, _ = new_repo
    upkeep_branch(work, 'MODEL = "openrouter/openai/gpt-6-luna"\nTIMEOUT = 30\n')
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "upkeep only (2 files" in capsys.readouterr().out


@pytest.mark.req("ship/a-behavior-change-beside-a-model-update-is-still-refused", existing=True)
def test_a_behavior_change_beside_a_model_update_is_still_refused(new_repo, capsys):
    work, remote, _ = new_repo
    upkeep_branch(work, 'MODEL = "openrouter/openai/gpt-6-luna"\nTIMEOUT = 90\n')
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert not on_remote(remote, "feature")
    assert "no planning package" in capsys.readouterr().out


def record_branch(work: Path, extra: str | None) -> None:
    """On the feature branch, add a case-folder record, and also change extra (a path) when given."""
    git(work, "checkout", "-q", "main")
    git(work, "checkout", "-q", "feature")
    git(work, "reset", "-q", "--hard", "main")
    case = work / "cases" / "x"
    case.mkdir(parents=True)
    (case / "run.py").write_text("print(1)\n")
    (case / "result.json").write_text("{}\n")
    if extra:
        (work / extra).parent.mkdir(parents=True, exist_ok=True)
        (work / extra).write_text("x = 1\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "record")


@pytest.mark.req("ship/a-branch-that-only-adds-a-case-record-merges-without-a-package")
def test_a_record_only_branch_merges_in_a_repository_with_no_package(new_repo, capsys):
    work, remote, _ = new_repo
    record_branch(work, None)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "upkeep only (2 files" in capsys.readouterr().out


@pytest.mark.req("ship/a-code-change-beside-a-case-record-is-still-refused")
def test_a_code_change_beside_a_record_is_still_refused(new_repo, capsys):
    work, remote, _ = new_repo
    record_branch(work, "src/app.py")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert not on_remote(remote, "feature")
    assert "no planning package" in capsys.readouterr().out


def hold_slots(tmp_path: Path, count: int) -> list:
    """Lock `count` check slots the way another ship run would, and return the open files."""
    import fcntl
    folder = tmp_path / "state" / "check-slots"
    folder.mkdir(parents=True, exist_ok=True)
    held = []
    for n in range(count):
        handle = open(folder / f"slot-{n}.lock", "a+", encoding="utf-8")
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        handle.truncate()
        handle.write(f"other-repo-{n} (pid 1)")
        handle.flush()
        held.append(handle)
    return held


@pytest.mark.req("ship/every-slot-taken-and-none-freed-stops-the-run-with-nothing-pushed")
def test_every_slot_taken_and_none_freed_stops_the_run_with_nothing_pushed(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    monkeypatch.setenv("SHIP_CHECK_SLOTS", "2")
    monkeypatch.setenv("SHIP_SLOT_WAIT", "0.3")
    monkeypatch.setattr(ship, "SLOT_POLL", 0.05)
    held = hold_slots(tmp_path, 2)
    marker = tmp_path / "check-ran"
    try:
        assert ship.main(["--repo", str(work), "--check", f"touch {marker}"]) == 1
    finally:
        for handle in held:
            handle.close()
    out = capsys.readouterr().out
    assert "all 2 check slots are taken" in out and "other-repo-0" in out and "other-repo-1" in out
    assert not marker.exists()
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-slot-that-frees-lets-the-check-run")
def test_a_slot_that_frees_lets_the_check_run(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    monkeypatch.setenv("SHIP_CHECK_SLOTS", "1")
    monkeypatch.setenv("SHIP_SLOT_WAIT", "20")
    monkeypatch.setattr(ship, "SLOT_POLL", 0.05)
    held = hold_slots(tmp_path, 1)
    # Free the slot when ship says it is waiting for it. Not on a timer (on a loaded machine the steps before the
    # check outlasted a 0.4 s timer, 2026-11-11), and not on the first time.sleep: that patch is process-wide, and
    # subprocess.run(..., timeout=...) calls time.sleep while it waits for a child, so the slot could be freed
    # before ship looked and "taken" was never printed (5 failures in the ship logs, 2026-11-09 to 2026-11-16).
    real_write = ship.Run.write
    def write_then_free(self, text):
        real_write(self, text)
        if "check slots are taken" in text and not held[0].closed:
            held[0].close()
    monkeypatch.setattr(ship.Run, "write", write_then_free)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    out = capsys.readouterr().out
    assert "all 1 check slots are taken" in out and "check slot 0 free after" in out
    assert on_remote(remote, "feature")


@pytest.mark.req("ship/the-slot-is-released-after-the-check")
def test_the_slot_is_released_after_the_check(repo, tmp_path, monkeypatch):
    import fcntl
    work, _, _ = repo
    monkeypatch.setenv("SHIP_CHECK_SLOTS", "1")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    with open(tmp_path / "state" / "check-slots" / "slot-0.lock", "a+", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)   # raises BlockingIOError if ship still holds it


def plan_content(work: Path, base: str, head: str, validator: Path) -> subprocess.CompletedProcess:
    """Run scripts/plan_content.py, as the push hook does."""
    script = Path(__file__).resolve().parents[1] / "scripts" / "plan_content.py"
    return subprocess.run([sys.executable, str(script), "--repo", str(work), "--base", base, "--head", head,
                           "--validator", str(validator)], capture_output=True, text=True)


@pytest.mark.req("ship/the-push-hook-asks-the-same-question")
def test_the_push_hook_asks_the_same_question(repo, tmp_path, monkeypatch):
    work, _, _ = repo                                   # the branch changes only a.txt
    fresh_validator(work, tmp_path, monkeypatch, 1)
    validator = tmp_path / "fresh_validator.py"
    base, head = git(work, "merge-base", "HEAD", "origin/main"), git(work, "rev-parse", "HEAD")
    done = plan_content(work, base, head, validator)
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("skip: no plan content changed since")
    (work / "docs" / "planning" / "plan.md").write_text("a new plan\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "plan")
    head = git(work, "rev-parse", "HEAD")
    done = plan_content(work, base, head, validator)
    assert done.returncode == 1 and done.stdout.startswith("validate:")
    assert plan_content(work, base, base, validator).returncode == 1, "a pushed commit that is not HEAD validates"
    assert plan_content(work, "nope", head, validator).returncode == 1, "a base that is no commit validates"


@pytest.mark.req("ship/the-push-hook-asks-the-same-question")
def test_the_push_hook_question_takes_relative_paths(repo, tmp_path, monkeypatch):
    work, _, _ = repo
    fresh_validator(work, tmp_path, monkeypatch, 1)
    base, head = git(work, "merge-base", "HEAD", "origin/main"), git(work, "rev-parse", "HEAD")
    script = Path(__file__).resolve().parents[1] / "scripts" / "plan_content.py"
    done = subprocess.run([sys.executable, str(script), "--repo", ".", "--base", base, "--head", head,
                           "--validator", "../fresh_validator.py"], cwd=work, capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr


# The one-page plan for small planned work (decision record 0010; agents/topics/working-method.md, "Plan size").
ONE_PAGE = """# Plan: a small thing

Plan size: small
Independent read: 2026-11-15, pass (a fresh subagent; nothing to fix)

## Goal

Brian, 2026-11-15: "do the small thing".

## How Brian judges it

He opens the page and sees the thing.

## Cost and time

No model spend (worked out: no model calls).

## Scoring fixed beforehand

No run.

## What already exists

Looked in docs/capabilities.md; nothing is reused.

## Steps

1. Do it.

## How to undo

`git revert` the merge.
"""
NO_COST_PART = ONE_PAGE.replace("## Cost and time", "## Spend")
# The heading is on the page, but only as a quotation inside a code block.
COST_PART_IN_A_FENCE = ONE_PAGE.replace("## Cost and time\n", "```text\n## Cost and time\n```\n")
# The marker is the first line of the file, behind a byte-order mark.
WITH_BYTE_ORDER_MARK = "\ufeff" + NO_COST_PART.replace("# Plan: a small thing\n\n", "", 1)
NOT_UTF8 = NO_COST_PART.encode() + b"\xff\xfe is not UTF-8\n"
QUOTED_FORMAT = """# How to write a one-page plan

Start the page with these two lines:

```text
Plan size: small
Independent read: <YYYY-MM-DD>, pass (<who read it, and what was fixed>)
```
"""


def add_plan(work: Path, text: str | bytes, name: str = "small-thing.md") -> str:
    """Commit a plan page on the current branch; return its repository path."""
    page = work / "docs" / "plans" / name
    page.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        page.write_bytes(text)
    else:
        page.write_text(text, encoding="utf-8")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "plan")
    return f"docs/plans/{name}"


def plan_on_main(work: Path, text: str) -> str:
    """Put a plan page on the default branch, then restart the feature branch from it with a change to a.txt only."""
    git(work, "checkout", "-q", "main")
    path = add_plan(work, text)
    git(work, "push", "-q", "origin", "main")
    git(work, "checkout", "-q", "-B", "feature")
    (work / "a.txt").write_text("c\n")
    git(work, "commit", "-q", "-am", "change")
    return path


def refused_before_the_check(work: Path, remote: Path, tmp_path: Path) -> None:
    """ship exits 1, the check never runs and nothing is pushed."""
    marker = tmp_path / "ran"
    assert ship.main(["--repo", str(work), "--check", f"touch {marker}"]) == 1
    assert not marker.exists(), "the check does not run"
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-complete-one-page-plan-merges")
def test_a_complete_one_page_plan_merges(repo, capsys):
    work, remote, _ = repo
    path = add_plan(work, ONE_PAGE)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    out = capsys.readouterr().out
    assert f"one-page plan {path} is complete" in out
    logged = "".join(p.read_text() for p in Path(os.environ["SHIP_LOG_DIR"]).glob("*.log"))
    assert f"one-page plan {path} is complete" in logged, "the line is logged as well as printed"


@pytest.mark.req("ship/a-one-page-plan-missing-a-part-is-refused")
@pytest.mark.parametrize("text, name", [
    (NO_COST_PART, "small-thing.md"),
    (NO_COST_PART, "2026/small-thing.md"),          # a subfolder of docs/plans/
    (NO_COST_PART, "café plan.md"),                 # git puts such a name in quotes unless asked not to
    (COST_PART_IN_A_FENCE, "small-thing.md"),
    (WITH_BYTE_ORDER_MARK, "small-thing.md"),
    (NOT_UTF8, "small-thing.md"),
], ids=["plain", "subfolder", "accented-name", "heading-only-in-a-code-block", "byte-order-mark", "not-utf8"])
def test_a_one_page_plan_missing_a_part_is_refused(repo, tmp_path, capsys, text, name):
    work, remote, _ = repo
    path = add_plan(work, text, name)
    refused_before_the_check(work, remote, tmp_path)
    out = capsys.readouterr().out
    assert f"{path} lacks" in out and "`## Cost and time`" in out and "Plan size" in out
    assert "`## Goal`" not in out, "only what is missing is named"


@pytest.mark.req("ship/a-one-page-plan-missing-a-part-is-refused")
def test_a_renamed_one_page_plan_is_checked_under_its_new_name(repo, tmp_path, capsys):
    work, remote, _ = repo
    old = plan_on_main(work, NO_COST_PART)
    git(work, "mv", old, "docs/plans/renamed.md")
    git(work, "commit", "-q", "-m", "rename the page")
    refused_before_the_check(work, remote, tmp_path)
    assert "docs/plans/renamed.md lacks" in capsys.readouterr().out


@pytest.mark.req("ship/a-plan-repair-or-an-upkeep-only-branch-does-not-excuse-an-incomplete-one-page-plan")
def test_a_plan_repair_does_not_excuse_an_incomplete_one_page_plan(new_repo, tmp_path, capsys):
    """A new repository with no package fails the planning gate on the branch and on its base, so the plan-repair
    exception would let a documentation-only branch merge; the page check stops it first."""
    work, remote, _ = new_repo
    git(work, "reset", "-q", "--hard", "origin/main")       # drop the a.txt change: the branch adds only the page
    path = add_plan(work, NO_COST_PART)
    refused_before_the_check(work, remote, tmp_path)
    out = capsys.readouterr().out
    assert f"{path} lacks" in out and "may merge" not in out


@pytest.mark.req("ship/a-plan-repair-or-an-upkeep-only-branch-does-not-excuse-an-incomplete-one-page-plan")
def test_an_upkeep_only_branch_does_not_excuse_an_incomplete_one_page_plan(new_repo, tmp_path, capsys):
    """A model name, a lock file and a document: the upkeep exception would let this branch merge."""
    work, remote, _ = new_repo
    upkeep_branch(work, 'MODEL = "openrouter/openai/gpt-6-luna"\nTIMEOUT = 30\n')
    path = add_plan(work, NO_COST_PART)
    refused_before_the_check(work, remote, tmp_path)
    out = capsys.readouterr().out
    assert f"{path} lacks" in out and "may merge" not in out


@pytest.mark.req("ship/with-no-merge-base-every-committed-one-page-plan-is-checked")
def test_with_no_merge_base_every_committed_one_page_plan_is_checked(repo, tmp_path, capsys):
    work, remote, _ = repo
    path = plan_on_main(work, NO_COST_PART)
    git(work, "update-ref", "-d", "refs/remotes/origin/main")       # git can no longer say where the branch left main
    # ship fetches origin first; fetch nothing back into origin/main so the merge base stays unknown.
    git(work, "config", "remote.origin.fetch", "+refs/heads/none:refs/remotes/origin/none")
    refused_before_the_check(work, remote, tmp_path)
    assert f"{path} lacks" in capsys.readouterr().out


@pytest.mark.req("ship/a-one-page-plan-over-150-lines-is-refused")
def test_a_one_page_plan_over_150_lines_is_refused(repo, tmp_path, capsys):
    work, remote, _ = repo
    long_page = ONE_PAGE + "".join(f"{n}. One more step.\n" for n in range(150))
    path = add_plan(work, long_page)
    refused_before_the_check(work, remote, tmp_path)
    out = capsys.readouterr().out
    assert path in out and "at most 150 lines" in out and f"it has {len(long_page.splitlines())}" in out


@pytest.mark.req("ship/a-one-page-plan-over-150-lines-is-refused")
def test_a_one_page_plan_of_exactly_150_lines_merges(repo, capsys):
    work, remote, _ = repo
    page = ONE_PAGE + "".join("One more line.\n" for _ in range(150 - len(ONE_PAGE.splitlines())))
    assert len(page.splitlines()) == 150
    path = add_plan(work, page)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert f"one-page plan {path} is complete" in capsys.readouterr().out


@pytest.mark.req("ship/a-one-page-plan-with-no-passing-independent-read-is-refused")
@pytest.mark.parametrize("read_line", [
    "",                                                              # no line at all
    "Independent read: 2026-11-15, revise (two conditions fail)",    # read, and it did not pass
    "Independent read: pass",                                        # no date
    "Independent read: pending",
    "Independent read: 2026-13-45, pass (no such day)",
    # The page was read again after it changed, and that read did not pass: the last line counts.
    "Independent read: 2026-11-15, pass (first read)\nIndependent read: 2026-11-16, revise (the cost is a guess)",
], ids=["no-line", "revise", "no-date", "pending", "no-such-day", "a-later-read-did-not-pass"])
def test_a_one_page_plan_with_no_passing_independent_read_is_refused(repo, tmp_path, capsys, read_line):
    work, remote, _ = repo
    page = ONE_PAGE.replace("Independent read: 2026-11-15, pass (a fresh subagent; nothing to fix)", read_line)
    path = add_plan(work, page)
    refused_before_the_check(work, remote, tmp_path)
    out = capsys.readouterr().out
    assert path in out and "Independent read: <YYYY-MM-DD>, pass" in out


@pytest.mark.req("ship/a-plan-page-that-does-not-call-itself-small-is-not-checked")
def test_a_plan_page_that_does_not_call_itself_small_is_not_checked(repo, capsys):
    """The branch adds two pages: only the one that calls itself small is read."""
    work, remote, _ = repo
    full = add_plan(work, "# A full plan\n\nPlan size: large\n\nIts package is docs/planning/planning-package.json.\n",
                    "full-plan.md")
    small = add_plan(work, ONE_PAGE)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    out = capsys.readouterr().out
    assert f"one-page plan {small} is complete" in out and full not in out


@pytest.mark.req("ship/a-format-quoted-in-a-code-block-is-not-a-one-page-plan")
def test_a_format_quoted_in_a_code_block_is_not_a_one_page_plan(repo, capsys):
    """The branch adds a page that quotes the two opening lines in a code block, and a real one-page plan."""
    work, remote, _ = repo
    quoted = add_plan(work, QUOTED_FORMAT, "README.md")
    small = add_plan(work, ONE_PAGE)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    out = capsys.readouterr().out
    assert f"one-page plan {small} is complete" in out and quoted not in out


@pytest.mark.req("ship/a-one-page-plan-the-merge-deletes-is-not-checked")
def test_a_one_page_plan_the_merge_deletes_is_not_checked(repo, capsys):
    """An incomplete page is on main; the branch deletes it and adds a complete one."""
    work, remote, _ = repo
    deleted = plan_on_main(work, NO_COST_PART)
    git(work, "rm", "-q", deleted)
    git(work, "commit", "-q", "-m", "drop the page")
    added = add_plan(work, ONE_PAGE, "another-small-thing.md")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    out = capsys.readouterr().out
    assert f"one-page plan {added} is complete" in out and deleted not in out


@pytest.mark.req("ship/a-one-page-plan-the-merge-does-not-touch-is-not-checked")
def test_a_one_page_plan_the_merge_does_not_touch_is_not_checked(repo, capsys):
    """An incomplete page is already on main; the branch adds a complete one: only the added page is checked."""
    work, remote, _ = repo
    untouched = plan_on_main(work, NO_COST_PART)
    added = add_plan(work, ONE_PAGE, "another-small-thing.md")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    out = capsys.readouterr().out
    assert f"one-page plan {added} is complete" in out and untouched not in out


@pytest.mark.req("ship/a-new-repository-with-a-one-page-plan-and-no-package-merges")
def test_a_new_repository_with_a_one_page_plan_and_no_package_merges(new_repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = new_repo
    monkeypatch.setenv("SHIP_PERSONAL_VPS", str(tmp_path / "no-such-clone"))   # reading the plan list would fail
    path = add_plan(work, ONE_PAGE)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    out = capsys.readouterr().out
    assert "new repository" in out and f"one-page plan ({path})" in out
    assert "plan list" not in out


@pytest.mark.req("ship/a-new-repository-with-a-one-page-plan-and-no-package-merges")
def test_a_new_repository_keeps_merging_on_a_one_page_plan_already_on_main(new_repo, capsys):
    work, remote, _ = new_repo
    path = plan_on_main(work, ONE_PAGE)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert f"one-page plan ({path})" in capsys.readouterr().out


@pytest.mark.req("ship/a-new-repository-whose-only-one-page-plan-is-incomplete-is-refused")
def test_a_new_repository_whose_only_one_page_plan_is_incomplete_is_refused(new_repo, tmp_path, capsys):
    work, remote, _ = new_repo
    path = plan_on_main(work, NO_COST_PART)
    refused_before_the_check(work, remote, tmp_path)
    out = capsys.readouterr().out
    assert "new repository" in out and path in out and "`## Cost and time`" in out
    assert "company-planning:planning-compliance" in out


@pytest.mark.req("ship/an-uncommitted-one-page-plan-does-not-stand-in-for-the-package")
def test_an_uncommitted_one_page_plan_does_not_stand_in_for_the_package(new_repo, tmp_path, capsys):
    """git ignores the plans folder, so the complete page in the working tree is not on GitHub for Brian to read."""
    work, remote, _ = new_repo
    (work / ".gitignore").write_text("docs/plans/\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "ignore the plans folder")
    page = work / "docs" / "plans" / "small-thing.md"
    page.parent.mkdir(parents=True)
    page.write_text(ONE_PAGE)
    refused_before_the_check(work, remote, tmp_path)
    out = capsys.readouterr().out
    assert "no complete one-page plan" in out and "is complete" not in out


@pytest.mark.req("ship/a-new-repository-with-no-plan-list-named-is-refused")
def test_a_new_repository_with_no_plan_list_named_is_refused(tmp_path, monkeypatch, capsys):
    """With neither the environment nor graph-config.yaml naming the plan list, the merge stops and nothing is pushed."""
    work, remote, _ = make_repo(tmp_path, monkeypatch, "2026-11-06T00:00:00+00:00", package=True)
    monkeypatch.delenv("SHIP_PLAN_LIST")
    monkeypatch.delenv("SHIP_PERSONAL_VPS", raising=False)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    out = capsys.readouterr().out
    assert "no plan list is named" in out and "plan_list_checkout" in out
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/the-plan-list-location-is-read-from-graph-config")
def test_the_plan_list_location_is_read_from_graph_config(tmp_path, monkeypatch):
    """graph-config.yaml names the checkout and path; the environment wins over it."""
    config = tmp_path / "graph-config.yaml"
    config.write_text("owner: someone\nplan_list_checkout: /srv/plans   # comment\nplan_list_path: a/b.conf\n")
    monkeypatch.setattr(ship, "CONFIG", config)
    monkeypatch.delenv("SHIP_PERSONAL_VPS", raising=False)
    monkeypatch.delenv("SHIP_PLAN_LIST", raising=False)
    assert ship.setting("plan_list_checkout", "SHIP_PERSONAL_VPS") == "/srv/plans"
    assert ship.setting("plan_list_path", "SHIP_PLAN_LIST") == "a/b.conf"
    monkeypatch.setenv("SHIP_PLAN_LIST", "c.conf")
    assert ship.setting("plan_list_path", "SHIP_PLAN_LIST") == "c.conf"
    assert ship.setting("missing", "SHIP_NO_SUCH_VARIABLE") is None


# The prior-art record at the merge point (code2-workspace issue 833, slice 1).
def add_change(work: Path, name: str = "add-x") -> str:
    """Commit an OpenSpec change folder on the current branch; return the path of its proposal."""
    folder = work / "openspec" / "changes" / name
    folder.mkdir(parents=True)
    (folder / "proposal.md").write_text("## Why\n\nBecause.\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "change")
    return f"openspec/changes/{name}/proposal.md"


def prior_art_calls(tmp_path: Path) -> list[str]:
    log = tmp_path / "prior-art.log"
    return log.read_text().splitlines() if log.exists() else []


@pytest.mark.req("ship/a-change-with-no-record-is-refused")
def test_a_change_with_no_record_is_refused(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    add_change(work)
    monkeypatch.setenv("FAKE_PRIOR_ART_EXIT", "1")
    refused_before_the_check(work, remote, tmp_path)
    out = capsys.readouterr().out
    assert "add-x: no prior-art record" in out


@pytest.mark.req("ship/a-change-with-a-record-merges")
def test_a_change_with_a_record_merges(repo, tmp_path, capsys):
    work, remote, _ = repo
    proposal = add_change(work)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    [call] = prior_art_calls(tmp_path)
    assert f"--repo {work}" in call and f"--files {proposal}" in call
    out = capsys.readouterr().out
    assert "prior-art: 1 changes looked at" in out
    logged = "".join(p.read_text() for p in Path(os.environ["SHIP_LOG_DIR"]).glob("*.log"))
    assert "prior-art: 1 changes looked at" in logged


@pytest.mark.req("ship/a-merge-that-touches-no-change-runs-nothing")
def test_a_merge_that_touches_no_change_runs_nothing(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    monkeypatch.setenv("FAKE_PRIOR_ART_EXIT", "1")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert prior_art_calls(tmp_path) == []
    assert "prior-art check not run: this merge adds or changes no OpenSpec change" in capsys.readouterr().out


@pytest.mark.req("ship/a-missing-prior-art-check-refuses")
def test_a_missing_prior_art_check_refuses(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    add_change(work)
    monkeypatch.setattr(ship, "PRIOR_ART_CHECK", tmp_path / "no-lockstep" / "prior_art.py")
    refused_before_the_check(work, remote, tmp_path)
    assert "reinstall ship" in capsys.readouterr().out


@pytest.mark.req("ship/a-prior-art-check-that-cannot-run-refuses")
def test_a_prior_art_check_that_cannot_run_refuses(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    add_change(work)
    monkeypatch.setenv("FAKE_PRIOR_ART_EXIT", "2")
    refused_before_the_check(work, remote, tmp_path)
    out = capsys.readouterr().out
    assert "exit 2" in out and "not a verdict on the record" in out


# ---- add-on switches from the copier answers, and the hidden acceptance gate (2026-11-20) -------------------------


def answers_on_main(work: Path, text: str) -> None:
    """Put .copier-answers.yml on the default branch, then restart the feature branch from it with a change to a.txt."""
    git(work, "checkout", "-q", "main")
    (work / ".copier-answers.yml").write_text(text)
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "answers")
    git(work, "push", "-q", "origin", "main")
    git(work, "checkout", "-q", "-B", "feature")
    (work / "a.txt").write_text("c\n")
    git(work, "commit", "-q", "-am", "change")


@pytest.mark.req("ship/the-planning-gate-is-switched-off")
def test_the_planning_gate_is_switched_off(new_repo, capsys):
    work, remote, _ = new_repo
    answers_on_main(work, "_src_path: gh:o/template\nship_planning_gate: false\n")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "ship: planning gate: off (.copier-answers.yml ship_planning_gate: false)" in capsys.readouterr().out


@pytest.mark.req("ship/the-one-page-plan-check-is-switched-off")
def test_the_one_page_plan_check_is_switched_off(repo, capsys):
    work, remote, _ = repo
    answers_on_main(work, "ship_one_page_plans: false\n")
    add_plan(work, NO_COST_PART)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "ship: one-page plans: off (.copier-answers.yml ship_one_page_plans: false)" in capsys.readouterr().out


@pytest.mark.req("ship/no-answers-file-keeps-every-gate-on")
def test_no_answers_file_keeps_every_gate_on(new_repo, tmp_path):
    work, remote, _ = new_repo
    refused_before_the_check(work, remote, tmp_path)


@pytest.mark.req("ship/no-answers-file-keeps-every-gate-on")
def test_a_branch_cannot_switch_its_own_gate_off(new_repo, tmp_path):
    """The switches are read from the default branch, so a branch that adds `false` is still gated."""
    work, remote, _ = new_repo
    (work / ".copier-answers.yml").write_text("ship_planning_gate: false\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "turn the gate off on the branch")
    refused_before_the_check(work, remote, tmp_path)


# ---- planning gates set in lockstep.yaml (2026-11-25, docs/planning/next.goal.md slice 1) ------------------


def lockstep_on_main(work: Path, text: str) -> None:
    """Put lockstep.yaml on the default branch, then restart the feature branch from it with a change to a.txt."""
    git(work, "checkout", "-q", "main")
    (work / "lockstep.yaml").write_text(text)
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "settings")
    git(work, "push", "-q", "origin", "main")
    git(work, "checkout", "-q", "-B", "feature")
    (work / "a.txt").write_text("d\n")
    git(work, "commit", "-q", "-am", "change")


@pytest.mark.req("ship/off-in-lockstep-yaml-on-the-default-branch-skips-the-gate")
def test_off_in_lockstep_yaml_on_the_default_branch_skips_the_gate(new_repo, capsys):
    work, remote, _ = new_repo
    lockstep_on_main(work, "planning:\n  gate: off\n")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "ship: planning gate: off (lockstep.yaml planning.gate: off)" in capsys.readouterr().out


@pytest.mark.req("ship/off-in-lockstep-yaml-on-the-default-branch-skips-the-gate")
def test_one_page_plans_off_in_lockstep_yaml(repo, capsys):
    work, remote, _ = repo
    lockstep_on_main(work, "planning: {one_page_plans: 'off'}\n")
    add_plan(work, NO_COST_PART)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert "ship: one-page plans: off (lockstep.yaml planning.one_page_plans: off)" in capsys.readouterr().out


@pytest.mark.req("ship/a-branch-cannot-switch-its-own-planning-gate-off-in-lockstep-yaml", existing=True)   # old ship never read lockstep.yaml; this guards it
def test_a_branch_cannot_switch_its_own_planning_gate_off_in_lockstep_yaml(new_repo, tmp_path):
    work, remote, _ = new_repo
    (work / "lockstep.yaml").write_text("planning:\n  gate: off\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "turn the gate off on the branch")
    refused_before_the_check(work, remote, tmp_path)


@pytest.mark.req("ship/warn-passes-a-plan-verdict")
def test_warn_passes_a_missing_package(new_repo, capsys):
    work, remote, _ = new_repo
    lockstep_on_main(work, "planning:\n  gate: warn\n")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "ship: warning: planning gate:" in capsys.readouterr().out


@pytest.mark.req("ship/warn-passes-a-plan-verdict")
def test_warn_passes_a_validator_rejection(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    lockstep_on_main(work, "planning:\n  gate: warn\n")
    with_package(work, tmp_path, monkeypatch, 1)
    (work / ship.PACKAGE).write_text('{"changed": true}\n')
    git(work, "commit", "-q", "-am", "package change")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert "ship: warning: planning gate:" in capsys.readouterr().out


@pytest.mark.req("ship/warn-still-refuses-a-validator-that-cannot-be-fetched", existing=True)   # an unfetchable validator already refused; this guards it under warn
def test_warn_still_refuses_a_validator_that_cannot_be_fetched(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    lockstep_on_main(work, "planning:\n  gate: warn\n")
    with_package(work, tmp_path, monkeypatch, 0)
    (work / ship.PACKAGE).write_text('{"changed": true}\n')
    git(work, "commit", "-q", "-am", "package change")
    monkeypatch.delenv("SHIP_PLANNING_VALIDATOR")
    monkeypatch.setenv("SHIP_COMPANY_PLANNING", str(tmp_path / "no-such-repo"))
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert not on_remote(remote, "feature")


@pytest.mark.req("ship/a-bad-planning-mode-refuses")
def test_a_bad_planning_mode_refuses(repo, tmp_path, capsys):
    work, remote, _ = repo
    lockstep_on_main(work, "planning:\n  gate: sometimes\n")
    refused_before_the_check(work, remote, tmp_path)
    assert "sometimes" in capsys.readouterr().out


def run_record(tmp_path: Path, monkeypatch, work: Path, **fields) -> None:
    """Write a `lockstep accept check` summary for the feature branch at HEAD, overridden by fields."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    rec = {"run_id": "20261120T000000Z-0001", "change": "add-x", "branch": "feature",
           "head": git(work, "rev-parse", "HEAD"), "accept": {"exit": 0, "passed": 2, "failed": 0, "errors": 0},
           "check_exit": 0, "collisions": [], "uncommitted": 0, **fields}
    d = tmp_path / "xdg" / "lockstep-runs" / work.name / rec["run_id"]
    d.mkdir(parents=True)
    (d / "summary.json").write_text(json.dumps(rec))


@pytest.mark.req("ship/a-passing-record-at-head-merges")
def test_a_passing_hidden_test_record_at_head_merges(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    run_record(tmp_path, monkeypatch, work)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert on_remote(remote, "feature")
    assert "hidden tests passed" in capsys.readouterr().out


@pytest.mark.req("ship/a-failing-or-out-of-date-record-is-refused")
@pytest.mark.parametrize("fields", [
    {"accept": {"exit": 1, "passed": 1, "failed": 1, "errors": 0}},
    {"head": "0" * 40},
    {"uncommitted": 2},
    {"accept": None, "collisions": ["tests/test_accept_1.py"]},
], ids=["failed", "other-commit", "uncommitted", "no-hidden-tests-ran"])
def test_a_failing_or_out_of_date_hidden_test_record_is_refused(repo, tmp_path, monkeypatch, capsys, fields):
    work, remote, _ = repo
    run_record(tmp_path, monkeypatch, work, **fields)
    refused_before_the_check(work, remote, tmp_path)
    assert "lockstep accept check add-x" in capsys.readouterr().out


@pytest.mark.req("ship/a-failing-or-out-of-date-record-is-refused")
def test_the_newest_record_counts(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    run_record(tmp_path, monkeypatch, work)  # passing, older
    run_record(tmp_path, monkeypatch, work, run_id="20261120T010000Z-0002", accept={"exit": 1})
    refused_before_the_check(work, remote, tmp_path)


@pytest.mark.req("ship/no-record-goes-on")
def test_no_hidden_test_record_goes_on(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert "ship: no hidden-test run recorded for this branch" in capsys.readouterr().out


@pytest.mark.req("ship/a-passing-record-at-head-merges")
def test_a_record_made_on_a_detached_head_is_found_by_its_commit(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    run_record(tmp_path, monkeypatch, work, branch="HEAD", accept={"exit": 1})
    refused_before_the_check(work, remote, tmp_path)


@pytest.mark.req("ship/a-failing-or-out-of-date-record-is-refused")
def test_an_unreadable_record_is_skipped_with_a_warning(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    d = tmp_path / "xdg" / "lockstep-runs" / work.name / "20261120T000000Z-0001"
    d.mkdir(parents=True)
    (d / "summary.json").write_text("{half")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    out = capsys.readouterr().out
    assert "unreadable run record" in out and "no hidden-test run recorded" in out


# ---- ship installs as a command from the public package (2026-11-20) ----------------------------------------------

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.req("ship/the-command-and-the-old-file-both-run")
def test_the_command_and_the_old_file_both_run():
    bare = subprocess.run(["/usr/bin/python3", "-I", str(ROOT / "scripts" / "ship.py"), "--help"],
                          capture_output=True, text=True)
    assert bare.returncode == 0, bare.stderr
    assert "usage" in bare.stdout.lower()
    module = subprocess.run([sys.executable, "-m", "lockstep.ship", "--help"], capture_output=True, text=True,
                            cwd=ROOT, env={**os.environ, "PYTHONPATH": str(ROOT / "src")})
    assert module.returncode == 0, module.stderr
    assert bare.stdout == module.stdout


@pytest.mark.req("ship/the-old-import-path-is-the-moved-module")
def test_the_old_import_path_is_the_moved_module():
    import lockstep.ship
    import lane_sweep  # noqa: F401  (scripts/ is on the path above)
    import lockstep.lane_sweep

    assert ship is lockstep.ship
    assert sys.modules["lane_sweep"] is lockstep.lane_sweep
    assert ship.PRIOR_ART_CHECK == Path(lockstep.ship.__file__).resolve().with_name("prior_art.py")
    assert ship.PRIOR_ART_CHECK.is_file()


def test_log_folders_leave_no_code2_folder_on_another_machine(tmp_path, monkeypatch):
    """A second user's home gets logs under the XDG state folder; Brian's ~/code2 keeps its log folders."""
    import lockstep.lane_sweep

    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    assert ship.default_log_dir("ship") == tmp_path / ".local" / "state" / "ship" / "logs"
    assert lockstep.lane_sweep.default_log_dir("lane-sweep") == tmp_path / ".local" / "state" / "lane-sweep" / "logs"
    (tmp_path / "code2").mkdir()
    assert ship.default_log_dir("ship") == tmp_path / "code2" / ".ship-logs"
    assert lockstep.lane_sweep.default_log_dir("lane-sweep") == tmp_path / "code2" / ".lane-sweep-logs"


# ---- generated status page conflicts and hidden tests after ship's own rebase (2026-11-22) -------------------------

FAKE_REGENERATE = "printf 'regenerated\\n' > docs/status.md"


def status_conflict(work: Path, *, also: str | None = None) -> None:
    """Branch and main each rewrite docs/status.md (and, with also, the same line of another file)."""
    git(work, "checkout", "-q", "main")
    (work / "docs").mkdir(exist_ok=True)
    (work / "docs" / "status.md").write_text("base\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "status")
    git(work, "push", "-q", "origin", "main")
    git(work, "checkout", "-q", "-B", "feature")
    (work / "docs" / "status.md").write_text("mine\n")
    (work / "mine.txt").write_text("mine\n")
    if also:
        (work / also).write_text("mine\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "my plan")
    git(work, "checkout", "-q", "main")
    (work / "docs" / "status.md").write_text("theirs\n")
    if also:
        (work / also).write_text("theirs\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "their plan")
    git(work, "push", "-q", "origin", "main")
    git(work, "checkout", "-q", "feature")


@pytest.mark.req("ship/a-conflict-only-in-the-status-page-is-regenerated")
def test_a_conflict_only_in_the_status_page_is_regenerated(repo, monkeypatch, capsys):
    work, remote, _ = repo
    monkeypatch.setenv("SHIP_REGENERATE", FAKE_REGENERATE)
    status_conflict(work)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert (work / "docs" / "status.md").read_text() == "regenerated\n"
    assert (work / "mine.txt").exists() and git(work, "status", "--porcelain") == ""
    assert git(work, "merge-base", "--is-ancestor", "origin/main", "HEAD") == ""
    assert "regenerated docs/status.md" in capsys.readouterr().out
    assert on_remote(remote, "feature")


@pytest.mark.req("ship/a-conflict-only-in-the-status-page-is-regenerated")
def test_a_status_page_conflict_with_another_conflict_still_stops(repo, monkeypatch, capsys):
    work, remote, _ = repo
    monkeypatch.setenv("SHIP_REGENERATE", FAKE_REGENERATE)
    status_conflict(work, also="other.txt")
    before = git(work, "rev-parse", "HEAD")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert "other.txt" in capsys.readouterr().out
    assert git(work, "rev-parse", "HEAD") == before and git(work, "status", "--porcelain") == ""
    assert not (work / ".git" / "rebase-merge").exists() and not on_remote(remote, "feature")


def fake_rerun(tmp_path: Path, monkeypatch, exit_status: int) -> Path:
    """A rerun command that rewrites the run record at the current HEAD with the given hidden-test exit."""
    script = tmp_path / "fake_rerun.py"
    script.write_text(
        "import json, subprocess, sys\n"
        "run_dir = sys.argv[sys.argv.index('--run-dir') + 1]\n"
        "p = run_dir + '/summary.json'; rec = json.load(open(p))\n"
        "rec['head'] = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()\n"
        f"rec['accept'] = {{'exit': {exit_status}, 'passed': 2, 'failed': {exit_status}, 'errors': 0}}\n"
        "json.dump(rec, open(p, 'w')); open(run_dir + '/rerun.log', 'w').write(' '.join(sys.argv[1:]))\n")
    monkeypatch.setenv("SHIP_ACCEPT_RERUN", f"{sys.executable} {script} {{change}} --run-dir {{run_dir}}")
    return tmp_path / "xdg" / "lockstep-runs" / "work" / "20261120T000000Z-0001" / "rerun.log"


@pytest.mark.req("ship/hidden-tests-run-again-after-ship-s-own-rebase")
@pytest.mark.parametrize("exit_status, merged", [(0, 0), (1, 1)], ids=["pass", "fail"])
def test_hidden_tests_run_again_after_ships_own_rebase(repo, tmp_path, monkeypatch, capsys, exit_status, merged):
    work, remote, _ = repo
    run_record(tmp_path, monkeypatch, work)  # passing, at the branch head before the rebase
    advance_main(work, "other.txt", "other\n")
    rerun_log = fake_rerun(tmp_path, monkeypatch, exit_status)
    assert ship.main(["--repo", str(work), "--check", "true"]) == merged
    assert rerun_log.read_text().startswith("add-x --run-dir ")
    assert on_remote(remote, "feature") == (merged == 0)
    assert "running the hidden tests again" in capsys.readouterr().out


@pytest.mark.req("ship/hidden-tests-run-again-after-ship-s-own-rebase")
def test_a_record_out_of_date_without_a_ship_rebase_is_still_refused(repo, tmp_path, monkeypatch):
    work, remote, _ = repo
    run_record(tmp_path, monkeypatch, work, head="0" * 40)
    rerun_log = fake_rerun(tmp_path, monkeypatch, 0)
    refused_before_the_check(work, remote, tmp_path)
    assert not rerun_log.exists()


@pytest.mark.req("ship/a-conflict-only-in-the-status-page-is-regenerated")
def test_a_commit_that_only_changed_the_status_page_is_dropped_and_regenerated(repo, monkeypatch):
    work, remote, _ = repo
    monkeypatch.setenv("SHIP_REGENERATE", FAKE_REGENERATE)
    status_conflict(work)
    (work / "docs" / "status.md").write_text("mine again\n")
    git(work, "commit", "-q", "-am", "status only")
    assert ship.main(["--repo", str(work), "--check", "true"]) == 0
    assert (work / "docs" / "status.md").read_text() == "regenerated\n" and (work / "mine.txt").exists()
    assert on_remote(remote, "feature")


@pytest.mark.req("ship/hidden-tests-run-again-after-ship-s-own-rebase")
def test_a_record_under_another_branch_name_is_found_after_ships_rebase(repo, tmp_path, monkeypatch, capsys):
    work, remote, _ = repo
    run_record(tmp_path, monkeypatch, work, branch="HEAD")  # recorded on a detached head at the branch tip
    advance_main(work, "other.txt", "other\n")
    rerun_log = fake_rerun(tmp_path, monkeypatch, 1)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert rerun_log.exists() and not on_remote(remote, "feature")


@pytest.mark.req("ship/a-conflict-only-in-the-status-page-is-regenerated")
def test_a_regenerate_that_changes_other_files_stops(repo, monkeypatch, capsys):
    work, remote, _ = repo
    monkeypatch.setenv("SHIP_REGENERATE", FAKE_REGENERATE + " && echo x > stray.txt")
    status_conflict(work)
    assert ship.main(["--repo", str(work), "--check", "true"]) == 1
    assert "stray.txt" in capsys.readouterr().out and not on_remote(remote, "feature")


@pytest.mark.req("ship/a-bad-planning-mode-refuses")
def test_non_text_planning_keys_refuse_instead_of_crashing():
    """`planning: {1: x, a: y}` raised TypeError (sorting mixed keys), escaping ship's ConfigError handler."""
    from lockstep.checks.config import ConfigError, planning_modes
    with pytest.raises(ConfigError, match="unknown key"):
        planning_modes({"planning": {1: "x", "a": "y"}})
