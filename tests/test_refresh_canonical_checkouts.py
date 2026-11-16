"""Tests for the session-start canonical-checkout refresh.

Each case names a defect observed on 2026-08-23:

* `~/code/active/project-meta` sat 46 commits behind `origin/main` and answered
  anyway. A file a session was asked to review appeared not to exist, and a
  coverage figure derived from its working tree reported 68/139 against a true
  84/139 -- naming 16 already-published projects as outstanding work.
* The prescribed workaround (`git show origin/main:<path>`) is only correct if
  the remote refs are fresh, and nothing was keeping them fresh.
* A fast-forward into a read-only tree fails with "unable to unlink". Both
  outcomes are normal in this ecosystem; an unreported jam is not.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def _load():
    spec = importlib.util.spec_from_file_location(
        "refresh_canonical_checkouts", SCRIPTS / "refresh_canonical_checkouts.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["refresh_canonical_checkouts"] = module
    spec.loader.exec_module(module)
    return module


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.email=t@t", "-c", "user.name=t", *args],
        check=True,
        capture_output=True,
    )


@pytest.fixture(autouse=True)
def _concern_repo(monkeypatch):
    """The stuck-checkout concern repository is a setting; tests name one so no real settings file is read."""
    monkeypatch.setenv("CONCERN_REPO", "Owner/concerns")


@pytest.fixture
def pair(tmp_path):
    """An upstream repo, a clone of it, and one commit the clone has not seen."""
    upstream = tmp_path / "upstream"
    upstream.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(upstream)], check=True)
    (upstream / "fact.txt").write_text("old", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "one")

    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(upstream), str(clone)], check=True)

    (upstream / "fact.txt").write_text("new", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "two")
    return upstream, clone


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_fetches_and_fast_forwards_a_clean_default_branch(pair):
    """The ordinary case: the checkout is behind and can safely catch up."""
    _, clone = pair
    result = _load().refresh(clone)
    assert result["fetched"] is True
    assert result["advanced"] is True
    assert result["behind"] == 0
    assert (clone / "fact.txt").read_text(encoding="utf-8") == "new"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_never_touches_a_checkout_with_uncommitted_work(pair):
    """Another writer's in-flight changes are not this script's to move."""
    _, clone = pair
    (clone / "fact.txt").write_text("someone is editing this", encoding="utf-8")
    result = _load().refresh(clone)
    assert result["fetched"] is True
    assert result["advanced"] is False
    assert "uncommitted" in result["note"]
    assert (clone / "fact.txt").read_text(encoding="utf-8") == "someone is editing this"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_never_touches_a_checkout_on_a_feature_branch(pair):
    """A lane sitting on its own branch must not be fast-forwarded onto main."""
    _, clone = pair
    _git(clone, "checkout", "-q", "-b", "some-lane")
    result = _load().refresh(clone)
    assert result["advanced"] is False
    assert "not the default branch" in result["note"]


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_reports_zero_behind_without_claiming_it_advanced(pair):
    """A current checkout is silent, not a false positive."""
    upstream, clone = pair
    _load().refresh(clone)
    second = _load().refresh(clone)
    assert second["behind"] == 0
    assert second["advanced"] is False


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_reports_ahead_default_branch_as_noncanonical(pair):
    """A local-only default-branch commit must never be called current."""
    _, clone = pair
    _git(clone, "fetch", "origin")
    _git(clone, "merge", "--ff-only", "origin/main")
    (clone / "local.txt").write_text("local", encoding="utf-8")
    _git(clone, "add", "local.txt")
    _git(clone, "commit", "-qm", "local only")

    result = _load().refresh(clone)

    assert result["ahead"] == 1
    assert result["behind"] == 0
    assert result["noncanonical"] is True
    assert "ahead of origin/main" in result["note"]


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_reports_diverged_default_branch_as_noncanonical(pair):
    """A checkout with both local and remote commits must fail the currentness gate."""
    _, clone = pair
    (clone / "local.txt").write_text("local", encoding="utf-8")
    _git(clone, "add", "local.txt")
    _git(clone, "commit", "-qm", "local only")

    result = _load().refresh(clone)

    assert result["ahead"] == 1
    assert result["behind"] == 1
    assert result["noncanonical"] is True
    assert "diverged" in result["note"]


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_reports_exact_tip_on_feature_branch_as_noncanonical(pair):
    """Revision equality does not make a feature-branch checkout canonical."""
    _, clone = pair
    _git(clone, "fetch", "origin")
    _git(clone, "merge", "--ff-only", "origin/main")
    _git(clone, "checkout", "-qb", "feature-at-tip")

    result = _load().refresh(clone)

    assert result["ahead"] == 0
    assert result["behind"] == 0
    assert result["noncanonical"] is True
    assert "not the default branch" in result["note"]


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_strict_mode_fails_for_ahead_checkout(pair, tmp_path, monkeypatch):
    """The fleet gate must propagate an ahead-only anomaly to its exit status."""
    _, clone = pair
    _git(clone, "fetch", "origin")
    _git(clone, "merge", "--ff-only", "origin/main")
    (clone / "local.txt").write_text("local", encoding="utf-8")
    _git(clone, "add", "local.txt")
    _git(clone, "commit", "-qm", "local only")
    module = _load()
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "TARGETS", {"clone": "Test fixture."})
    monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")

    assert module.main(["--strict", "--no-session-repo"]) == 1


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_stale_origin_head_falls_back_to_an_existing_default_ref(pair):
    """A deleted remote default must not make a valid origin/main unknowable."""

    _, clone = pair
    _git(clone, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/develop")
    module = _load()
    assert module.upstream_ref(clone) == "origin/main"
    result = module.refresh(clone)
    assert result["unknown"] is False
    assert result["behind"] == 0
    assert result["advanced"] is True


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_stale_origin_head_repairs_to_nonstandard_advertised_default(tmp_path):
    upstream = tmp_path / "upstream"
    upstream.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "vm", str(upstream)], check=True)
    (upstream / "fact.txt").write_text("old", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "one")
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(upstream), str(clone)], check=True)
    _git(clone, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/develop")

    module = _load()
    assert module.upstream_ref(clone) == "origin/vm"
    assert (
        subprocess.run(
            ["git", "-C", str(clone), "symbolic-ref", "--short", "refs/remotes/origin/HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        == "origin/vm"
    )


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_exits_zero_by_default_even_when_a_target_is_stale(pair, tmp_path, monkeypatch):
    """Session-start hooks must not block a session; --strict is opt-in."""
    module = _load()
    _, clone = pair
    clone.chmod(0o555)
    try:
        monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
        monkeypatch.setattr(module, "TARGETS", {"clone": "Test fixture."})
        monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")
        assert module.main([]) == 0
        assert module.main(["--strict"]) == 1
    finally:
        clone.chmod(0o755)


@pytest.mark.parametrize(
    "outcome",
    [
        {
            "fetched": True,
            "behind": 1,
            "advanced": False,
            "unknown": False,
            "note": "left behind for test",
            "upstream": "origin/main",
        },
        {
            "fetched": True,
            "behind": None,
            "advanced": False,
            "unknown": True,
            "note": "freshness unknown for test",
        },
        {
            "fetched": False,
            "behind": None,
            "advanced": False,
            "unknown": False,
            "note": "fetch failed for test",
        },
    ],
    ids=["stale", "unknown", "unreachable"],
)
@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_strict_json_fails_for_every_noncurrent_result(
    tmp_path, monkeypatch, capsys, outcome
):
    """Machine-readable strict mode must preserve both JSON and its failure signal."""
    module = _load()
    clone = tmp_path / "clone"
    (clone / ".git").mkdir(parents=True)
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")
    monkeypatch.setattr(module, "refresh", lambda _repo: dict(outcome))

    assert module.main(["--targets", "clone", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["results"][0]["name"] == "clone"

    assert module.main(["--targets", "clone", "--strict", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["results"][0]["name"] == "clone"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_stale_report_handles_target_without_a_registered_reason(tmp_path, monkeypatch, capsys):
    """Explicit target overrides need not have TARGETS metadata."""
    module = _load()
    clone = tmp_path / "clone"
    (clone / ".git").mkdir(parents=True)
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")
    monkeypatch.setattr(
        module,
        "refresh",
        lambda _repo: {
            "fetched": True,
            "behind": 1,
            "advanced": False,
            "note": "could not fast-forward: test fixture",
            "upstream": "origin/main",
        },
    )

    assert module.main(["--targets", "clone"]) == 0
    output = capsys.readouterr().out
    assert "STALE CANONICAL CHECKOUT" in output
    assert "Do not trust its working tree for authoritative project content." in output


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_shallow_clone_at_exact_upstream_tip_is_current(tmp_path):
    """Exact tip identity is conclusive even when older history is shallow."""
    module = _load()
    upstream = tmp_path / "upstream"
    upstream.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(upstream)], check=True)
    for i in range(3):
        (upstream / "f.txt").write_text(str(i), encoding="utf-8")
        _git(upstream, "add", "-A")
        _git(upstream, "commit", "-qm", f"commit {i}")

    shallow = tmp_path / "shallow"
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", f"file://{upstream}", str(shallow)], check=True
    )

    result = module.refresh(shallow)
    assert result["fetched"] is True
    assert result["unknown"] is False
    assert result["behind"] == 0
    assert result["advanced"] is False


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_shallow_clone_fast_forwards_when_head_is_proven_ancestor(tmp_path):
    module = _load()
    upstream = tmp_path / "upstream"
    upstream.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(upstream)], check=True)
    (upstream / "f.txt").write_text("one", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "one")
    shallow = tmp_path / "shallow"
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", f"file://{upstream}", str(shallow)],
        check=True,
    )
    (upstream / "f.txt").write_text("two", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "two")

    result = module.refresh(shallow)
    assert result["fetched"] is True
    assert result["unknown"] is False
    assert result["behind"] == 0
    assert result["advanced"] is True
    assert (shallow / "f.txt").read_text(encoding="utf-8") == "two"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_diverged_shallow_clone_remains_unknown(tmp_path):
    module = _load()
    upstream = tmp_path / "upstream"
    upstream.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(upstream)], check=True)
    (upstream / "f.txt").write_text("base", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "base")
    shallow = tmp_path / "shallow"
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", f"file://{upstream}", str(shallow)],
        check=True,
    )
    (shallow / "local.txt").write_text("local", encoding="utf-8")
    _git(shallow, "add", "-A")
    _git(shallow, "commit", "-qm", "local")
    (upstream / "remote.txt").write_text("remote", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "remote")

    result = module.refresh(shallow)
    assert result["fetched"] is True
    assert result["unknown"] is True
    assert result["behind"] is None
    assert result["advanced"] is False
    assert "not provably an ancestor" in result["note"]


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_unknown_result_is_never_folded_into_all_current(tmp_path, monkeypatch, capsys):
    """The exact defect class this script exists to prevent: UNKNOWN silently read as CURRENT."""
    module = _load()
    clone = tmp_path / "clone"
    (clone / ".git").mkdir(parents=True)
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")
    monkeypatch.setattr(
        module,
        "refresh",
        lambda _repo: {
            "fetched": True,
            "behind": None,
            "advanced": False,
            "unknown": True,
            "note": "no origin/HEAD and neither origin/main nor origin/master exists",
        },
    )

    assert module.main(["--targets", "clone"]) == 0
    output = capsys.readouterr().out
    assert "all current" not in output
    assert "CANONICAL CHECKOUT FRESHNESS UNKNOWN" in output
    assert module.main(["--targets", "clone", "--strict"]) == 1


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_current_session_repo_resolves_a_plain_checkout(tmp_path):
    """A session sitting directly in a checkout is detected by its HOME-relative path."""
    module = _load()
    home = tmp_path
    repo = home / "code" / "active" / "agentic-engineering-system"
    repo.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    cwd = Path.cwd()
    try:
        os.chdir(repo)
        detected = module.current_session_repo(home)
    finally:
        os.chdir(cwd)
    assert detected is not None
    repo_root, rel = detected
    assert repo_root == repo.resolve()
    assert rel == "code/active/agentic-engineering-system"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_current_session_repo_resolves_through_a_worktree(tmp_path):
    """A worktree's own feature branch must not be diffed against origin's default branch."""
    module = _load()
    home = tmp_path
    repo = home / "code" / "active" / "agentic-engineering-system"
    repo.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    (repo / "f.txt").write_text("x", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "one")
    worktree = repo / "worktrees" / "some-lane"
    _git(repo, "worktree", "add", "-q", "-b", "some-lane", str(worktree))

    cwd = Path.cwd()
    try:
        os.chdir(worktree)
        detected = module.current_session_repo(home)
    finally:
        os.chdir(cwd)
    assert detected is not None
    repo_root, rel = detected
    assert repo_root == repo.resolve()
    assert rel == "code/active/agentic-engineering-system"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_current_session_repo_returns_none_outside_a_repo(tmp_path):
    """A cwd with no repo must not crash or be silently treated as a target."""
    module = _load()
    plain_dir = tmp_path / "not-a-repo"
    plain_dir.mkdir()
    cwd = Path.cwd()
    try:
        os.chdir(plain_dir)
        detected = module.current_session_repo(tmp_path)
    finally:
        os.chdir(cwd)
    assert detected is None


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_default_invocation_adds_the_session_repo_when_missing_from_targets(tmp_path, monkeypatch):
    """The 2026-09-02 AES gap: a repo not in TARGETS must still be caught by default."""
    module = _load()
    home = tmp_path
    upstream = home / "upstream"
    upstream.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(upstream)], check=True)
    (upstream / "fact.txt").write_text("old", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "one")

    session_repo = home / "code" / "active" / "agentic-engineering-system"
    session_repo.parent.mkdir(parents=True)
    subprocess.run(["git", "clone", "-q", str(upstream), str(session_repo)], check=True)

    (upstream / "fact.txt").write_text("new", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "two")

    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: home))
    monkeypatch.setattr(module, "TARGETS", {})
    monkeypatch.setattr(module, "STAMP", home / "stamp.json")

    cwd = Path.cwd()
    try:
        os.chdir(session_repo)
        assert module.main(["--json"]) == 0
    finally:
        os.chdir(cwd)

    stamp = json.loads((home / "stamp.json").read_text(encoding="utf-8"))
    names = {r["name"]: r for r in stamp["results"]}
    assert "code/active/agentic-engineering-system" in names
    assert names["code/active/agentic-engineering-system"]["advanced"] is True
    assert (session_repo / "fact.txt").read_text(encoding="utf-8") == "new"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_explicit_targets_do_not_auto_add_the_session_repo(tmp_path, monkeypatch):
    """--targets must mean exactly that list; auto-detection is a default-only convenience."""
    module = _load()
    home = tmp_path
    session_repo = home / "code" / "active" / "agentic-engineering-system"
    session_repo.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(session_repo)], check=True)

    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: home))
    monkeypatch.setattr(module, "TARGETS", {})
    monkeypatch.setattr(module, "STAMP", home / "stamp.json")

    cwd = Path.cwd()
    try:
        os.chdir(session_repo)
        assert module.main(["--targets", "some/other/repo", "--json"]) == 0
    finally:
        os.chdir(cwd)

    stamp = json.loads((home / "stamp.json").read_text(encoding="utf-8"))
    names = {r["name"] for r in stamp["results"]}
    assert "code/active/agentic-engineering-system" not in names


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_no_session_repo_flag_suppresses_auto_detection(tmp_path, monkeypatch):
    """The explicit opt-out must actually opt out."""
    module = _load()
    home = tmp_path
    session_repo = home / "code" / "active" / "agentic-engineering-system"
    session_repo.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(session_repo)], check=True)

    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: home))
    monkeypatch.setattr(module, "TARGETS", {})
    monkeypatch.setattr(module, "STAMP", home / "stamp.json")

    cwd = Path.cwd()
    try:
        os.chdir(session_repo)
        assert module.main(["--no-session-repo", "--json"]) == 0
    finally:
        os.chdir(cwd)

    stamp = json.loads((home / "stamp.json").read_text(encoding="utf-8"))
    assert stamp["results"] == []


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_resolve_target_matches_exact_key():
    module = _load()
    targets = {"code/active/project-meta": "reason"}
    assert module.resolve_target("code/active/project-meta", targets) == "code/active/project-meta"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_resolve_target_resolves_a_unique_basename():
    """`--targets project-meta` must resolve to the real key, not stay literal."""
    module = _load()
    targets = {
        "code/active/project-meta": "reason",
        "code/active/enforced-planning": "reason",
    }
    assert module.resolve_target("project-meta", targets) == "code/active/project-meta"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_resolve_target_leaves_an_ambiguous_basename_unresolved():
    module = _load()
    targets = {
        "code/active/foo": "reason",
        "code/other/foo": "reason",
    }
    assert module.resolve_target("foo", targets) == "foo"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_resolve_target_leaves_an_unmatched_name_unresolved():
    module = _load()
    targets = {"code/active/project-meta": "reason"}
    assert module.resolve_target("nonexistent-repo", targets) == "nonexistent-repo"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_targets_short_name_resolves_and_actually_refreshes(tmp_path, monkeypatch):
    """Regression: `--targets project-meta` silently vanished the target and
    printed "all current" with zero checks performed (2026-09-02/03 -- this
    exact command produced two stale, undetected worktree branch points in one
    session). It must resolve to the real key and actually fetch/report on it.
    """
    module = _load()
    home = tmp_path
    upstream = home / "upstream"
    upstream.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(upstream)], check=True)
    (upstream / "fact.txt").write_text("old", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "one")

    clone = home / "code" / "active" / "project-meta"
    clone.parent.mkdir(parents=True)
    subprocess.run(["git", "clone", "-q", str(upstream), str(clone)], check=True)

    (upstream / "fact.txt").write_text("new", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "two")

    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: home))
    monkeypatch.setattr(module, "TARGETS", {"code/active/project-meta": "Ecosystem governance."})
    monkeypatch.setattr(module, "STAMP", home / "stamp.json")

    assert module.main(["--targets", "project-meta", "--json"]) == 0

    stamp = json.loads((home / "stamp.json").read_text(encoding="utf-8"))
    assert len(stamp["results"]) == 1
    result = stamp["results"][0]
    assert result["name"] == "code/active/project-meta"
    assert result["fetched"] is True
    assert result["advanced"] is True
    assert (clone / "fact.txt").read_text(encoding="utf-8") == "new"


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_unmatched_targets_value_is_reported_unreachable_not_all_current(tmp_path, monkeypatch, capsys):
    """A `--targets` value matching nothing must never silently produce 'all current'."""
    module = _load()
    home = tmp_path

    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: home))
    monkeypatch.setattr(module, "TARGETS", {"code/active/project-meta": "Ecosystem governance."})
    monkeypatch.setattr(module, "STAMP", home / "stamp.json")

    exit_code = module.main(["--targets", "totally-unknown-repo"])
    out = capsys.readouterr().out

    assert "all current" not in out
    assert "CANONICAL CHECKOUT UNREACHABLE" in out
    assert "totally-unknown-repo" in out
    # Report-only by default (matches every other unreachable/stale case);
    # --strict is what turns this into a failing exit code.
    assert exit_code == 0

    strict_exit = module.main(["--targets", "totally-unknown-repo", "--strict"])
    assert strict_exit == 1


def _seed_stamp(stamp_path, *, results, ran_at=None):
    import time as _time

    stamp_path.write_text(
        json.dumps({"ran_at": ran_at if ran_at is not None else _time.time(), "results": results}),
        encoding="utf-8",
    )


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_throttled_run_still_reports_a_persistent_noncanonical_problem(tmp_path, monkeypatch, capsys):
    """Regression for the 2026-09-14 silent-for-hours incident.

    project-meta sat noncanonical (dirty + 26 behind origin/main) for hours;
    the SessionStart hook runs this with --min-interval-hours 1, so once ANY
    session's run absorbed that result, every session's hook for the next
    hour returned 0 with no output at all -- the problem never surfaced
    again until an unrelated manual check found it by chance.
    """
    module = _load()
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")
    _seed_stamp(
        tmp_path / "stamp.json",
        results=[
            {
                "name": "code/project-meta",
                "fetched": True,
                "behind": 26,
                "advanced": False,
                "unknown": False,
                "noncanonical": True,
                "note": "2 uncommitted change(s) and 26 commit(s) behind origin/main; left alone",
            }
        ],
    )

    exit_code = module.main(["--min-interval-hours", "1", "--quiet"])

    output = capsys.readouterr().out
    assert "NONCANONICAL CHECKOUT STATE" in output, (
        "a --quiet, throttled run must still surface a real cached problem, "
        f"not just the redundant fetch it skips. Got: {output!r}"
    )
    assert exit_code == 0  # --strict not passed


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_throttled_run_stays_quiet_when_cached_state_was_clean(tmp_path, monkeypatch, capsys):
    """Positive control: the ordinary quiet/throttled case is unaffected."""
    module = _load()
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")
    _seed_stamp(
        tmp_path / "stamp.json",
        results=[
            {
                "name": "code/project-meta",
                "fetched": True,
                "behind": 0,
                "advanced": False,
                "unknown": False,
                "noncanonical": False,
                "note": "current",
            }
        ],
    )

    exit_code = module.main(["--min-interval-hours", "1", "--quiet"])

    assert capsys.readouterr().out == ""
    assert exit_code == 0


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_throttled_strict_json_still_exits_nonzero_for_cached_problem(tmp_path, monkeypatch, capsys):
    """--strict must not lose its signal just because the run was throttled."""
    module = _load()
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")
    _seed_stamp(
        tmp_path / "stamp.json",
        results=[
            {
                "name": "code/project-meta",
                "fetched": True,
                "behind": 26,
                "advanced": False,
                "unknown": False,
                "noncanonical": True,
                "note": "left alone",
            }
        ],
    )

    exit_code = module.main(["--min-interval-hours", "1", "--strict", "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert payload["throttled"] is True
    assert exit_code == 1


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_throttle_still_skips_silently_with_no_cached_results(tmp_path, monkeypatch, capsys):
    """A stamp with no results key (or an empty one) falls back to the old skip, not a crash."""
    module = _load()
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")
    (tmp_path / "stamp.json").write_text(json.dumps({"ran_at": __import__("time").time()}), encoding="utf-8")

    exit_code = module.main(["--min-interval-hours", "1"])

    assert capsys.readouterr().out == ""
    assert exit_code == 0


def _behind_clone(home: Path, rel: str) -> tuple[Path, Path]:
    upstream = home / f"upstream-{Path(rel).name}"
    upstream.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(upstream)], check=True)
    (upstream / "fact.txt").write_text("old", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "one")
    clone = home / rel
    clone.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "-q", str(upstream), str(clone)], check=True)
    (upstream / "fact.txt").write_text("new", encoding="utf-8")
    _git(upstream, "add", "-A")
    _git(upstream, "commit", "-qm", "two")
    return upstream, clone


@pytest.mark.req("graph-checkout-refresh/graph-sweep-covers-registered-checkouts")
def test_graph_targets_lists_registered_checkouts_and_skips_in_place_mirrors(tmp_path):
    """2026-09-26: most registered checkouts had no scheduled refresh at all."""
    module = _load()
    _up, plain = _behind_clone(tmp_path, "code/plain-repo")
    _up2, mirror = _behind_clone(tmp_path, "code/inside-success-mega")
    _up3, nested = _behind_clone(tmp_path, "code/inside-success-mega/repos/member")
    graph = tmp_path / "graph.json"
    graph.write_text(json.dumps([
        {"id": "plain-repo", "path": str(plain)},
        # Baselined as intended_in_place: its own refresh unit owns this tree
        # and the repositories nested inside it.
        {"id": "inside-success-mega", "path": str(mirror)},
        {"id": "member", "path": str(nested)},
    ]), encoding="utf-8")

    (tmp_path / "unattended_execution_sources_baseline.json").write_text(
        json.dumps({"intended_in_place": {"mirror-refresh.service|inside-success-mega": "mirror"}}), encoding="utf-8"
    )

    assert module.graph_targets(tmp_path, graph) == ["code/plain-repo"]


@pytest.mark.req("graph-checkout-refresh/graph-sweep-covers-registered-checkouts")
def test_all_graph_refreshes_unlisted_checkout_without_touching_the_stamp(tmp_path, monkeypatch):
    module = _load()
    _up, clone = _behind_clone(tmp_path, "code/plain-repo")
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "TARGETS", {})
    monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")
    monkeypatch.setattr(module, "graph_targets", lambda home: ["code/plain-repo"])

    assert module.main(["--all-graph", "--json", "--no-session-repo", "--no-concern"]) == 0

    assert (clone / "fact.txt").read_text(encoding="utf-8") == "new"
    assert not (tmp_path / "stamp.json").exists()


class _FakeGh:
    """Records gh calls; serves one optional existing concern issue."""

    def __init__(self, existing=None):
        self.calls = []
        self.existing = existing or []

    def __call__(self, args):
        self.calls.append(list(args))
        if args[:2] == ["issue", "list"]:
            return json.dumps(self.existing)
        if args[:2] == ["issue", "view"]:
            return json.dumps({"body": "", "comments": []})
        if args[:2] == ["issue", "create"]:
            return "https://github.com/x/y/issues/9\n"
        return ""


def _row(name, behind, noncanonical, fetched=True):
    return {"name": name, "behind": behind, "noncanonical": noncanonical, "fetched": fetched,
            "advanced": False, "unknown": False, "note": f"note for {name}"}


@pytest.mark.req("graph-checkout-refresh/stuck-checkouts-raise-a-concern")
def test_stuck_rows_names_only_checkouts_held_far_behind_by_local_changes():
    """2026-10-12: AES canonical sat 494 commits behind for a week behind one stray edit,
    and the sweep only wrote that to the journal. A clean checkout far behind is not stuck
    (the sweep fast-forwards it); a dirty one just under the threshold is not alarmed."""
    module = _load()
    rows = [
        _row("code/aes", 494, True),
        _row("code/dodaf", 56, True),
        _row("code/just-under", 19, True),
        _row("code/clean-behind", 500, False),
        _row("code/unreachable", None, False, fetched=False),
    ]
    assert [r["name"] for r in module.stuck_rows(rows, 20)] == ["code/aes", "code/dodaf"]


@pytest.mark.req("graph-checkout-refresh/stuck-checkouts-raise-a-concern")
def test_stuck_checkout_opens_one_keyed_concern_naming_each_repo():
    module = _load()
    gh = _FakeGh()
    outcome = module.route_stuck_concern([_row("code/aes", 494, True), _row("code/ok", 0, False)], 20, run=gh)
    assert outcome.startswith("created")
    create = next(c for c in gh.calls if c[:2] == ["issue", "create"])
    body = create[create.index("--body") + 1]
    assert "`~/code/aes`: 494 commits behind" in body
    assert "code/ok" not in body
    assert "<!-- concern-key: graph-checkouts-stuck-behind -->" in body
    assert "Trace-Review: none" in body


@pytest.mark.req("graph-checkout-refresh/stuck-checkouts-raise-a-concern")
def test_concern_closes_when_no_checkout_is_stuck():
    module = _load()
    marker = "<!-- concern-key: graph-checkouts-stuck-behind -->"
    gh = _FakeGh(existing=[{"number": 7, "state": "OPEN", "body": marker}])
    outcome = module.route_stuck_concern([_row("code/aes", 0, False)], 20, run=gh)
    assert outcome == "closed #7"
    assert ["issue", "close", "7", "-R", "Owner/concerns", "--reason", "completed"] in gh.calls


@pytest.mark.req("graph-checkout-refresh/stuck-checkouts-raise-a-concern")
def test_all_graph_sweep_routes_a_real_dirty_behind_checkout_to_the_concern(tmp_path, monkeypatch):
    """End to end through main(): a clone with uncommitted work is left behind and reaches the alarm."""
    module = _load()
    _up, clone = _behind_clone(tmp_path, "code/plain-repo")
    (clone / "fact.txt").write_text("someone is editing this", encoding="utf-8")
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "TARGETS", {})
    monkeypatch.setattr(module, "STAMP", tmp_path / "stamp.json")
    monkeypatch.setattr(module, "graph_targets", lambda home: ["code/plain-repo"])
    seen = []
    monkeypatch.setattr(module, "route_stuck_concern", lambda results, threshold: seen.append(
        [r["name"] for r in module.stuck_rows(results, threshold)]) or "created test")

    assert module.main(["--all-graph", "--json", "--no-session-repo", "--stuck-threshold", "1"]) == 0

    assert seen == [["code/plain-repo"]]
    assert (clone / "fact.txt").read_text(encoding="utf-8") == "someone is editing this"


@pytest.mark.req("graph-checkout-refresh/stuck-checkouts-raise-a-concern")
def test_a_dead_concern_route_fails_the_sweep(tmp_path, monkeypatch):
    module = _load()
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(module, "TARGETS", {})
    monkeypatch.setattr(module, "graph_targets", lambda home: [])

    def boom(results, threshold):
        raise RuntimeError("gh unreachable")

    monkeypatch.setattr(module, "route_stuck_concern", boom)
    assert module.main(["--all-graph", "--json", "--no-session-repo"]) == 1


@pytest.mark.req("graph-checkout-refresh/settings-come-from-config")
def test_missing_concern_repo_stops_loudly_naming_where_to_set_it(monkeypatch):
    module = _load()
    monkeypatch.delenv("CONCERN_REPO", raising=False)
    monkeypatch.setattr(module, "CONFIG", Path("/nonexistent/graph-config.yaml"))
    with pytest.raises(SystemExit) as stop:
        module.setting("concern_repo", "CONCERN_REPO")
    assert "CONCERN_REPO" in str(stop.value) and "/nonexistent/graph-config.yaml" in str(stop.value)


@pytest.mark.req("graph-checkout-refresh/never-discards-local-work")
def test_a_checkout_holding_a_lock_receipt_is_left_alone(pair):
    """AES carries no lock controller, so a locked checkout is reported, never unlocked or moved."""
    _, clone = pair
    (clone / ".git" / "canonical-lock-v1.json").write_text("{}", encoding="utf-8")
    result = _load().refresh(clone)
    assert result["advanced"] is False and result["noncanonical"] is True
    assert "lock receipt" in result["note"]
    assert (clone / "fact.txt").read_text(encoding="utf-8") == "old"
