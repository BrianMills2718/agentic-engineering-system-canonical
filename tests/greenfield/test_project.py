"""`aes init` and project discovery (`RU-AES-PROJECT`, `SC-GF-001`).

Initialization writes exactly the two seed artifacts of the initialization
contract, and the result passes the same commands a consumer runs next:
`aes target validate`, `aes topology check`, `aes evidence status`. Every
refusal leaves the repository byte-for-byte as it was. Discovery finds the
project from a nested directory and from a linked worktree, so no command
needs `--root` there.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from agentic_engineering_system.cli import main
from agentic_engineering_system.project import (
    SEED_ARTIFACTS,
    ProjectError,
    find_project_root,
    initialize_project,
)

OUTCOME = "A new project can be initialized and validated without private files."
ACTOR = "a developer adopting AES"
INIT = ["init", "--project-id", "demo", "--actor", ACTOR, "--outcome", OUTCOME]


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
        cwd=root, capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


def _snapshot(root: Path) -> dict[str, bytes]:
    """Every file and directory under root (outside .git), with file contents."""
    out: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if rel == ".git" or rel.startswith(".git/"):
            continue
        out[rel] = path.read_bytes() if path.is_file() else b"<dir>"
    return out


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    (root / "README.md").write_text("# demo\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "empty project")
    return root


@pytest.fixture
def chdir(monkeypatch: pytest.MonkeyPatch):
    return monkeypatch.chdir


def test_init_writes_only_seed_artifacts_and_passes_the_next_commands(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([*INIT, "--root", str(repo)]) == 0
    out = capsys.readouterr().out
    assert f"wrote {repo / '.aes' / 'project.yaml'}" in out
    assert f"wrote {repo / '.aes' / 'target.yaml'}" in out
    # the printed next step routes through planning, as GETTING_STARTED.md does
    assert ("next: aes plan prepare, write a proposal, aes plan validate/accept; "
            "or edit .aes/target.yaml by hand, then aes target validate") in out
    assert "plan it in .aes/target.yaml" not in out
    created = sorted(p.relative_to(repo).as_posix() for p in (repo / ".aes").rglob("*"))
    assert created == sorted(SEED_ARTIFACTS)  # no plans/, observations/, generated/, analysis

    assert main(["target", "validate", "--root", str(repo)]) == 0
    assert "outcomes=1 normative_items=0" in capsys.readouterr().out
    assert main(["topology", "check", "--root", str(repo)]) == 0
    assert "OK topology" in capsys.readouterr().out
    assert main(["evidence", "status", "--root", str(repo)]) == 0
    assert "0 criteria" in capsys.readouterr().out
    assert not (repo / ".aes" / "observations").exists()  # evidence status reads, never creates

    project = (repo / ".aes" / "project.yaml").read_text(encoding="utf-8")
    assert "project_id: demo" in project and "initialized_at:" in project
    target = (repo / ".aes" / "target.yaml").read_text(encoding="utf-8")
    assert OUTCOME in target and ACTOR in target


def test_init_result_is_strict_and_names_the_installed_version(repo: Path) -> None:
    done = initialize_project(repo, project_id="demo", outcome=f"  {OUTCOME}  ", actor=ACTOR,
                              governed_roots=["lib", "spec/"])
    assert done.project.governed_roots == ["lib/", "spec/"]
    assert done.project.aes.architecture_line == "AES-v0.2"
    assert done.project.aes.distribution_version  # importlib.metadata, never "unknown"
    assert done.project.aes.initialized_at is not None
    assert [o.statement for o in done.target.outcomes] == [OUTCOME]
    assert done.target.target_id == "demo-target"


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        (["--outcome", "   "], "outcome must be non-empty"),
        (["--outcome", ""], "outcome must be non-empty"),
        (["--actor", " "], "actor must be non-empty"),
        (["--project-id", "has space"], "project id must match"),
        (["--governed-root", "../out"], "governed root must be a relative subdirectory"),
        (["--governed-root", "/abs"], "governed root must be a relative subdirectory"),
        (["--governed-root", "src", "--governed-root", "src/"], "governed root given twice"),
    ],
)
def test_bad_inputs_refuse_and_write_nothing(
    repo: Path, argv: list[str], message: str, capsys: pytest.CaptureFixture[str]
) -> None:
    before = _snapshot(repo)
    base = {"--project-id": "demo", "--actor": ACTOR, "--outcome": OUTCOME}
    for flag, value in zip(argv[::2], argv[1::2]):
        base.pop(flag, None)
    args = ["init", *[x for kv in base.items() for x in kv], *argv, "--root", str(repo)]
    assert main(args) == 1
    assert message in capsys.readouterr().err
    assert _snapshot(repo) == before


def test_refuses_outside_git_repository(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    plain = tmp_path / "plain"
    plain.mkdir()
    assert main([*INIT, "--root", str(plain)]) == 1
    assert "not a Git repository" in capsys.readouterr().err
    assert list(plain.iterdir()) == []


def test_refuses_below_the_top_of_the_work_tree(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    nested = repo / "src"
    nested.mkdir()
    before = _snapshot(repo)
    assert main([*INIT, "--root", str(nested)]) == 1
    assert "not the top of its Git work tree" in capsys.readouterr().err
    assert _snapshot(repo) == before


def test_second_init_refuses_and_changes_nothing(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([*INIT, "--root", str(repo)]) == 0
    before = _snapshot(repo)
    assert main(["init", "--project-id", "other", "--actor", "x", "--outcome", "y", "--root", str(repo)]) == 1
    assert "already initialized" in capsys.readouterr().err
    assert _snapshot(repo) == before


def test_refuses_when_aes_exists_without_a_project_file(repo: Path) -> None:
    (repo / ".aes" / "observations").mkdir(parents=True)  # a deferred artifact, made by hand
    before = _snapshot(repo)
    with pytest.raises(ProjectError, match="already exists"):
        initialize_project(repo, project_id="demo", outcome=OUTCOME, actor=ACTOR)
    assert _snapshot(repo) == before


@pytest.mark.parametrize("deferred", ["observations/OBS-1.yaml", "plans/PLAN-1.yaml", "generated/x.md", "analysis.yaml"])
def test_a_deferred_artifact_in_the_staged_tree_refuses_everything(repo: Path, deferred: str) -> None:
    def add_deferred(staging: Path) -> None:
        path = staging / deferred
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x: 1\n", encoding="utf-8")

    before = _snapshot(repo)
    with pytest.raises(ProjectError, match="does not name"):
        initialize_project(repo, project_id="demo", outcome=OUTCOME, actor=ACTOR, _stage_hook=add_deferred)
    assert _snapshot(repo) == before  # no .aes/, no staging directory left behind


def test_failure_between_the_two_files_leaves_no_aes(repo: Path) -> None:
    def fail(_: Path) -> None:
        raise RuntimeError("simulated crash after both files were staged")

    before = _snapshot(repo)
    with pytest.raises(RuntimeError, match="simulated crash"):
        initialize_project(repo, project_id="demo", outcome=OUTCOME, actor=ACTOR, _stage_hook=fail)
    assert _snapshot(repo) == before


def test_find_project_root_from_nested_directory(repo: Path, chdir, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([*INIT, "--root", str(repo)]) == 0
    nested = repo / "src" / "pkg" / "deep"
    nested.mkdir(parents=True)
    assert find_project_root(nested) == repo.resolve()

    chdir(nested)  # no --root: every command discovers the project
    capsys.readouterr()
    assert main(["target", "validate"]) == 0
    assert str(repo / ".aes" / "target.yaml") in capsys.readouterr().out
    assert main(["topology", "check"]) == 0
    assert main(["evidence", "status"]) == 0
    assert main(["context", "OUT-001"]) == 0
    assert OUTCOME in capsys.readouterr().out


def test_find_project_root_from_linked_worktree(repo: Path, tmp_path: Path, chdir,
                                                capsys: pytest.CaptureFixture[str]) -> None:
    assert main([*INIT, "--root", str(repo)]) == 0
    _git(repo, "add", ".aes")
    _git(repo, "commit", "-q", "-m", "aes init")
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-q", "-b", "lane", str(linked))
    (linked / "tests").mkdir()

    # the worktree's own checkout of .aes/, not the main checkout's
    assert find_project_root(linked / "tests") == linked.resolve()
    chdir(linked / "tests")
    capsys.readouterr()
    assert main(["target", "validate"]) == 0
    assert str(linked / ".aes" / "target.yaml") in capsys.readouterr().out
    assert main(["hooks", "install"]) == 0
    assert (linked / ".githooks" / "pre-commit").is_file()


def test_no_project_is_a_clear_error(tmp_path: Path, chdir, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(ProjectError, match="no .aes/project.yaml here or in any parent"):
        find_project_root(tmp_path)
    chdir(tmp_path)
    assert main(["target", "validate"]) == 1
    assert "run `aes init`" in capsys.readouterr().err


def test_init_does_not_touch_git_state(repo: Path) -> None:
    head = _git(repo, "rev-parse", "HEAD")
    initialize_project(repo, project_id="demo", outcome=OUTCOME, actor=ACTOR)
    assert _git(repo, "rev-parse", "HEAD") == head
    assert _git(repo, "status", "--porcelain") == "?? .aes/"
