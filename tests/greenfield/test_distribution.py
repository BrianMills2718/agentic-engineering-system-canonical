"""Distribution and the packaged pre-commit hook (`RU-AES-DISTRIBUTION`).

Roadmap phase 1 closes two consumer kinks: the AES version never moved (so a pin
bump did not reinstall), and whygame5's hand-copied hook broke in linked
worktrees. These tests hold both:

- a clean venv installs this repository in the consumer's pin form
  (`name @ git+file://localhost/…@<sha>`), and `aes --version` names that commit;
- `aes hooks install` writes a hook that blocks a commit staging an orphan under
  a governed root and admits it once the target plans the file;
- installation refuses when it would fail every commit or silence another hook.

The clean install builds its venv with `uv`, the install path the README and
docs/greenfield/GETTING_STARTED.md document, and needs network access for
dependencies. It skips when `uv` is not on `PATH`, and when
AES_SKIP_CLEAN_INSTALL=1 is set; nothing else skips it.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from agentic_engineering_system.cli import main
from agentic_engineering_system.hooks import (INSTALLER_CONFIG_KEY, MANAGED_MARKER, HookInstallError,
                                              install_hooks)

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
    shutil.copyfile(WHYGAME5_AES / "project.yaml", root / ".aes" / "project.yaml")
    shutil.copyfile(WHYGAME5_AES / "target.yaml", root / ".aes" / "target.yaml")
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


UNROUTED_CRITERION = """  - id: SC-WG5-900
    statement: A criterion added with nothing that could ever supply its evidence.
    target_refs: [OUT-WG5-001]
    disproof: No verification subject or external boundary names its requirement.
    evidence_requirements:
      - id: ER-WG5-900-01
        kind: deterministic_test
        requirement: A test that nobody has planned.
"""


def test_hook_refuses_a_criterion_with_no_route_and_admits_it_once_routed(consumer: Path) -> None:
    """Phase 5 exit gate (SC-GF-004 at commit time): the hook's `aes target validate`
    rejects a target in which an evidence requirement has no route."""
    assert main(["hooks", "install", "--root", str(consumer)]) == 0
    _git(consumer, "add", ".githooks/pre-commit")
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    assert _git(consumer, "commit", "-q", "-m", "install hook", env=env).returncode == 0

    target = consumer / ".aes" / "target.yaml"
    text = target.read_text(encoding="utf-8")
    target.write_text(text.replace("components:\n", UNROUTED_CRITERION + "components:\n", 1), encoding="utf-8")
    _git(consumer, "add", ".aes/target.yaml")
    blocked = _git(consumer, "commit", "-m", "add unrouted criterion", env=env)
    assert blocked.returncode != 0
    assert "1 evidence requirement(s) with no route" in blocked.stderr
    assert "'ER-WG5-900-01' (criterion 'SC-WG5-900') has no route" in blocked.stderr
    assert _git(consumer, "rev-list", "--count", "HEAD").stdout == "2\n"

    routed = target.read_text(encoding="utf-8") + (
        "external_boundaries:\n  - evidence_requirement_ref: ER-WG5-900-01\n"
        "    boundary: supplied outside this repository, for the test\n"
    )
    target.write_text(routed, encoding="utf-8")
    _git(consumer, "add", ".aes/target.yaml")
    allowed = _git(consumer, "commit", "-m", "add routed criterion", env=env)
    assert allowed.returncode == 0, allowed.stderr


def test_linked_worktree_falls_back_to_main_checkout_venv(consumer: Path) -> None:
    """whygame5's kink: a linked worktree has no .venv; the hook must find the main one."""
    install_hooks(consumer, interpreter="/nonexistent/python")  # installer gone
    shim = consumer / ".venv" / "bin" / "aes"  # untracked, as a real venv is
    shim.parent.mkdir(parents=True)
    shim.write_text(f'#!/bin/sh\nPYTHONPATH={SRC} exec {sys.executable} -m agentic_engineering_system.cli "$@"\n',
                    encoding="utf-8")
    shim.chmod(0o755)
    (consumer / ".gitignore").write_text(".venv/\n", encoding="utf-8")
    _git(consumer, "add", ".githooks/pre-commit", ".gitignore")
    assert _git(consumer, "commit", "-q", "-m", "install hook").returncode == 0

    linked = consumer.parent / "linked"
    assert _git(consumer, "worktree", "add", "-q", "-b", "lane", str(linked)).returncode == 0
    assert not (linked / ".venv").exists()
    _assert_hook_gates_orphan(linked, None)


def test_reinstall_rewrites_a_managed_hook(consumer: Path) -> None:
    hook, _ = install_hooks(consumer, interpreter="/old/python")
    first = hook.read_text(encoding="utf-8")
    hook2, _ = install_hooks(consumer, interpreter="/new/python")
    assert hook == hook2
    assert hook.read_text(encoding="utf-8") == first  # the body does not depend on the installer
    assert _git(consumer, "config", "--local", "--get", INSTALLER_CONFIG_KEY).stdout.strip() == "/new/python"


def test_install_leaves_the_tracked_hook_clean_on_another_machine(consumer: Path) -> None:
    """BRI-31: `.githooks/pre-commit` is tracked and shared, so the installing
    checkout's absolute interpreter path must not land in it — otherwise the
    documented install dirties the worktree and one `git add -A` publishes a
    path that exists on nobody else's machine."""
    hook, _ = install_hooks(consumer, interpreter=sys.executable)
    _git(consumer, "add", ".githooks/pre-commit")
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    assert _git(consumer, "commit", "-q", "-m", "install hook", env=env).returncode == 0
    assert _git(consumer, "status", "--short").stdout == ""

    # a second machine installs over the same clone: no tracked change at all
    install_hooks(consumer, interpreter="/home/other/elsewhere/.venv/bin/python")
    assert _git(consumer, "status", "--short").stdout == ""
    body = hook.read_text(encoding="utf-8")
    assert sys.executable not in body and "/home/other" not in body
    assert INSTALLER_CONFIG_KEY in body  # it reads the path back from .git/config
    assert (_git(consumer, "config", "--local", "--get", INSTALLER_CONFIG_KEY).stdout.strip()
            == "/home/other/elsewhere/.venv/bin/python")


def test_hook_runs_without_the_installer_config(consumer: Path) -> None:
    """A clone that never ran `aes hooks install` (or whose aes.installer is gone)
    falls through to the worktree venv instead of failing on an empty path."""
    install_hooks(consumer, interpreter=sys.executable)
    assert _git(consumer, "config", "--local", "--unset", INSTALLER_CONFIG_KEY).returncode == 0
    shim = consumer / ".venv" / "bin" / "aes"
    shim.parent.mkdir(parents=True)
    shim.write_text(f'#!/bin/sh\nPYTHONPATH={SRC} exec {sys.executable} -m agentic_engineering_system.cli "$@"\n',
                    encoding="utf-8")
    shim.chmod(0o755)
    (consumer / ".gitignore").write_text(".venv/\n", encoding="utf-8")
    _git(consumer, "add", ".githooks/pre-commit", ".gitignore")
    assert _git(consumer, "commit", "-q", "-m", "install hook").returncode == 0
    _assert_hook_gates_orphan(consumer, None)


def test_refuses_outside_a_git_repository(tmp_path: Path) -> None:
    (tmp_path / ".aes").mkdir()
    shutil.copyfile(WHYGAME5_AES / "project.yaml", tmp_path / ".aes" / "project.yaml")
    shutil.copyfile(WHYGAME5_AES / "target.yaml", tmp_path / ".aes" / "target.yaml")
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


def test_version_fails_loudly_when_nothing_names_the_running_code(monkeypatch: pytest.MonkeyPatch,
                                                                  capsys: pytest.CaptureFixture[str]) -> None:
    import agentic_engineering_system.characterize as ch
    from importlib.metadata import PackageNotFoundError

    def missing(name: str) -> str:
        raise PackageNotFoundError(name)

    monkeypatch.setattr(ch, "version", missing)
    monkeypatch.setattr(ch, "_source_checkout_revision", lambda _: None)
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 1
    assert "is not installed" in capsys.readouterr().err


def test_version_names_the_install_and_the_running_checkout(capsys: pytest.CaptureFixture[str]) -> None:
    """Run from this checkout's src/ (pytest pythonpath), the version is the installed
    distribution's plus this checkout's describe, not the install alone (§13 kink)."""
    from importlib.metadata import version

    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    running = _git(REPO, "describe", "--always", "--dirty").stdout.strip()
    assert capsys.readouterr().out == f"{version('agentic-engineering-system')} (running: {running})\n"


@pytest.mark.skipif(os.environ.get("AES_SKIP_CLEAN_INSTALL") == "1", reason="AES_SKIP_CLEAN_INSTALL=1")
@pytest.mark.skipif(shutil.which("uv") is None, reason="uv is not on PATH")
def test_clean_install_in_pin_form_reports_commit_version_and_ships_the_hook(tmp_path: Path) -> None:
    head = _git(REPO, "rev-parse", "HEAD").stdout.strip()
    venv = tmp_path / "venv"
    # with uv, as the README and docs/greenfield/GETTING_STARTED.md install; `uv venv` needs no
    # stdlib ensurepip, and `--python` names the venv to install into without activating it
    made = _run(["uv", "venv", "-q", str(venv)], tmp_path)
    assert made.returncode == 0, made.stderr
    # PEP 508 named URLs need a host; git accepts file://localhost/<path>
    pin = f"agentic-engineering-system @ git+file://localhost{REPO}@{head}"
    installed = _run(["uv", "pip", "install", "-q", "--python", str(venv / "bin" / "python"), pin], tmp_path)
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
    # the installing interpreter is recorded per clone, not baked into the tracked hook
    assert (_git(consumer, "config", "--local", "--get", INSTALLER_CONFIG_KEY).stdout.strip()
            == str(venv / "bin" / "python"))
    assert str(venv) not in (consumer / ".githooks" / "pre-commit").read_text(encoding="utf-8")
    _git(consumer, "add", ".githooks/pre-commit")
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    assert _git(consumer, "commit", "-q", "-m", "install hook", env=env).returncode == 0
    _assert_hook_gates_orphan(consumer, env)
