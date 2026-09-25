"""Distribution and the packaged pre-commit hook (`RU-AES-DISTRIBUTION`).

Roadmap phase 1 closes two consumer kinks: the AES version never moved (so a pin
bump did not reinstall), and whygame5's hand-copied hook broke in linked
worktrees. These tests hold both:

- a clean venv installs this repository in the consumer's pin form
  (`name @ git+file://localhost/…@<sha>`), and `aes --version` names that commit;
- `aes hooks install` writes a hook that blocks a commit staging an orphan under
  a governed root and admits it once the target plans the file;
- installation refuses when it would fail every commit or silence another hook.

The clean install needs network access for dependencies. Set
AES_SKIP_CLEAN_INSTALL=1 to skip it where a venv cannot be built; nothing else
skips it.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from agentic_engineering_system.cli import main
from agentic_engineering_system.hooks import MANAGED_MARKER, HookInstallError, install_hooks

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src"
WHYGAME5_AES = Path(__file__).parent / "fixtures" / "whygame5-54043e2" / ".aes"
REALIZED = (
    "src/whygame5/__init__.py",
    "src/whygame5/contracts.py",
    "src/whygame5/evaluator.py",
    "src/whygame5/graph.py",
    "tests/test_evaluator.py",
    "tests/test_replay.py",
)
ORPHAN = "src/whygame5/stray.py"
PLAN_ORPHAN = """  - id: ART-WG5-STRAY
    locator: {exact_path: src/whygame5/stray.py}
    kind: source
    purpose: planned after the hook refused it
    semantic_justification_refs: [NI-WG5-006]
"""


def _run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False, env=env)


def _git(root: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return _run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args], root, env)


def _touch(root: Path, *paths: str) -> None:
    for rel in paths:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {rel}\n", encoding="utf-8")


def _consumer(root: Path) -> Path:
    """The frozen whygame5 records plus its realized governed files, committed."""
    root.mkdir(parents=True, exist_ok=True)
    (root / ".aes").mkdir()
    shutil.copy(WHYGAME5_AES / "project.yaml", root / ".aes" / "project.yaml")
    shutil.copy(WHYGAME5_AES / "target.yaml", root / ".aes" / "target.yaml")
    _touch(root, *REALIZED)
    assert _git(root, "init", "-q").returncode == 0
    _git(root, "add", ".")
    done = _git(root, "commit", "-q", "-m", "fixture")
    assert done.returncode == 0, done.stderr
    return root


def _plan_orphan(root: Path) -> None:
    target = root / ".aes" / "target.yaml"
    text = target.read_text(encoding="utf-8")
    anchor = "verification_subjects:\n"
    assert text.count(anchor) == 1
    target.write_text(text.replace(anchor, PLAN_ORPHAN + anchor), encoding="utf-8")


def _assert_hook_gates_orphan(root: Path, env: dict[str, str] | None) -> None:
    """The installed hook refuses a staged orphan, then admits it once planned."""
    _touch(root, ORPHAN)
    _git(root, "add", ORPHAN)
    blocked = _git(root, "commit", "-m", "add stray", env=env)
    assert blocked.returncode != 0
    assert f"orphan: {ORPHAN}" in blocked.stderr
    assert _git(root, "rev-list", "--count", "HEAD").stdout == "2\n"  # fixture + hook commit only

    _plan_orphan(root)
    _git(root, "add", ".aes/target.yaml")
    allowed = _git(root, "commit", "-m", "plan and add stray", env=env)
    assert allowed.returncode == 0, allowed.stderr
    assert "OK topology" in allowed.stderr  # git sends hook stdout to stderr
    assert ORPHAN in _git(root, "show", "--name-only", "--format=", "HEAD").stdout.split()


@pytest.fixture
def consumer(tmp_path: Path) -> Path:
    return _consumer(tmp_path / "consumer")


def test_hook_blocks_orphan_commit_and_admits_planned_one(consumer: Path) -> None:
    # the hook runs this interpreter; PYTHONPATH makes it import this tree's source
    assert main(["hooks", "install", "--root", str(consumer)]) == 0
    hook = consumer / ".githooks" / "pre-commit"
    assert os.access(hook, os.X_OK)
    assert hook.read_text(encoding="utf-8").splitlines()[1] == MANAGED_MARKER
    assert _git(consumer, "config", "--local", "--get", "core.hooksPath").stdout.strip() == ".githooks"
    _git(consumer, "add", ".githooks/pre-commit")
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    assert _git(consumer, "commit", "-q", "-m", "install hook", env=env).returncode == 0
    _assert_hook_gates_orphan(consumer, env)


def test_reinstall_rewrites_a_managed_hook(consumer: Path) -> None:
    hook, _ = install_hooks(consumer, interpreter="/old/python")
    hook2, _ = install_hooks(consumer, interpreter="/new/python")
    assert hook == hook2
    text = hook.read_text(encoding="utf-8")
    assert "/new/python" in text and "/old/python" not in text


def test_refuses_outside_a_git_repository(tmp_path: Path) -> None:
    (tmp_path / ".aes").mkdir()
    shutil.copy(WHYGAME5_AES / "project.yaml", tmp_path / ".aes" / "project.yaml")
    shutil.copy(WHYGAME5_AES / "target.yaml", tmp_path / ".aes" / "target.yaml")
    with pytest.raises(HookInstallError, match="not a Git repository"):
        install_hooks(tmp_path)
    assert not (tmp_path / ".githooks").exists()


def test_refuses_a_hook_aes_did_not_write(consumer: Path, capsys: pytest.CaptureFixture[str]) -> None:
    foreign = consumer / ".githooks" / "pre-commit"
    foreign.parent.mkdir()
    foreign.write_text("#!/bin/sh\nexec make lint\n", encoding="utf-8")
    assert main(["hooks", "install", "--root", str(consumer)]) == 1
    assert "a pre-commit hook AES did not write already exists" in capsys.readouterr().err
    assert foreign.read_text(encoding="utf-8") == "#!/bin/sh\nexec make lint\n"
    assert _git(consumer, "config", "--local", "--get", "core.hooksPath").returncode != 0


def test_refuses_a_repository_hook_that_would_go_dark(consumer: Path) -> None:
    repo_hook = consumer / ".git" / "hooks" / "pre-commit"
    repo_hook.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    with pytest.raises(HookInstallError, match="AES did not write"):
        install_hooks(consumer)


def test_refuses_a_local_hooks_path_elsewhere(consumer: Path) -> None:
    _git(consumer, "config", "--local", "core.hooksPath", ".husky")
    with pytest.raises(HookInstallError, match="core.hooksPath is already '.husky'"):
        install_hooks(consumer)
    assert not (consumer / ".githooks").exists()


def test_refuses_without_a_target(consumer: Path) -> None:
    (consumer / ".aes" / "target.yaml").unlink()
    with pytest.raises(HookInstallError, match="target absent"):
        install_hooks(consumer)
    assert not (consumer / ".githooks").exists()


def test_version_fails_loudly_when_not_installed(monkeypatch: pytest.MonkeyPatch,
                                                 capsys: pytest.CaptureFixture[str]) -> None:
    import agentic_engineering_system.cli as cli
    from importlib.metadata import PackageNotFoundError

    def missing(name: str) -> str:
        raise PackageNotFoundError(name)

    monkeypatch.setattr(cli, "version", missing)
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 1
    assert "is not installed" in capsys.readouterr().err


def test_version_prints_the_installed_version_on_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    from importlib.metadata import version

    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert capsys.readouterr().out == version("agentic-engineering-system") + "\n"


@pytest.mark.skipif(os.environ.get("AES_SKIP_CLEAN_INSTALL") == "1", reason="AES_SKIP_CLEAN_INSTALL=1")
def test_clean_install_in_pin_form_reports_commit_version_and_ships_the_hook(tmp_path: Path) -> None:
    head = _git(REPO, "rev-parse", "HEAD").stdout.strip()
    venv = tmp_path / "venv"
    made = _run([sys.executable, "-m", "venv", str(venv)], tmp_path)
    assert made.returncode == 0, made.stderr
    # PEP 508 named URLs need a host; git accepts file://localhost/<path>
    pin = f"agentic-engineering-system @ git+file://localhost{REPO}@{head}"
    installed = _run([str(venv / "bin" / "python"), "-m", "pip", "install", "-q", pin], tmp_path)
    assert installed.returncode == 0, installed.stderr[-2000:]

    aes = venv / "bin" / "aes"
    reported = _run([str(aes), "--version"], tmp_path)
    assert reported.returncode == 0, reported.stderr
    ver = reported.stdout.strip()
    assert ver and ver != "0.1.0"
    # the version names the pinned commit (setuptools-scm: 0.1.devN+g<sha>)
    assert "+g" in ver and head.startswith(ver.split("+g", 1)[1].split(".", 1)[0]), ver

    consumer = _consumer(tmp_path / "consumer")
    hooked = _run([str(aes), "hooks", "install", "--root", str(consumer)], tmp_path)
    assert hooked.returncode == 0, hooked.stderr
    assert str(venv / "bin" / "python") in (consumer / ".githooks" / "pre-commit").read_text(encoding="utf-8")
    _git(consumer, "add", ".githooks/pre-commit")
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    assert _git(consumer, "commit", "-q", "-m", "install hook", env=env).returncode == 0
    _assert_hook_gates_orphan(consumer, env)
