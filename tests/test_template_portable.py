"""Tests that the template in this repository renders a portable repository (spec portable-template).

Moved from code2-template `tests/test_portable.py` on 2026-11-21. Renders with copier and `--skip-tasks`, so no
network, git or tool installs are needed; the full copy with its tasks is run by hand from the public address.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ADDRESS = "gh:BrianMills2718/agentic-engineering-system-canonical"
LOCKSTEP_URL = "https://github.com/BrianMills2718/agentic-engineering-system-canonical"
_OWNER = re.compile(r"~/|github-personal|Brian|[\w.+-]+@[\w-]+\.[\w.]+")


def machine_bound(repo: Path) -> list[str]:
    """Return `<file>:<line>: <text>` for each owner-specific mention in AGENTS.md, pyproject.toml and lefthook.yml.

    A home-folder path, the private SSH alias, the owner's name or an e-mail address counts; the public URL Lockstep
    installs from does not.
    """
    found = []
    for name in ("AGENTS.md", "pyproject.toml", "lefthook.yml"):
        path = repo / name
        if path.exists():
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if _OWNER.search(line.replace(LOCKSTEP_URL, "")):
                    found.append(f"{name}:{number}: {line.strip()}")
    return found


def render(tmp_path: Path, *data: str) -> Path:
    if not shutil.which("uvx"):
        pytest.skip("uvx is not installed")
    src = tmp_path / "src"
    src.mkdir()
    shutil.copy(ROOT / "copier.yml", src)
    shutil.copytree(ROOT / "template", src / "template", ignore=shutil.ignore_patterns(".venv", "__pycache__"))
    out = tmp_path / "out"
    args = ["uvx", "copier", "copy", "--trust", "--defaults", "--skip-tasks", "--data", "project_name=demo",
            "--data", "description=Demo", *[x for d in data for x in ("--data", d)], str(src), str(out)]
    subprocess.run(args, check=True, capture_output=True, text=True, timeout=300)
    return out


@pytest.mark.req("portable-template/default-copy-has-no-machine-bound-parts")
def test_default_copy_has_no_machine_bound_parts(tmp_path):
    out = render(tmp_path)
    hooks = (out / "lefthook.yml").read_text()
    assert "remotes:" not in hooks and "name: no-env-file" in hooks and "name: secrets-staged" in hooks
    assert machine_bound(out) == []
    assert "authors" not in (out / "pyproject.toml").read_text()
    answers = (out / ".copier-answers.yml").read_text()
    for line in ("code2_workspace: false", "ship_planning_gate: false", "ship_one_page_plans: false"):
        assert line in answers


@pytest.mark.req("portable-template/workspace-copy-keeps-the-remote")
def test_workspace_copy_keeps_the_remote(tmp_path):
    out = render(tmp_path, "code2_workspace=true")
    hooks = (out / "lefthook.yml").read_text()
    assert "github-personal:BrianMills2718/code2-workspace.git" in hooks and "hooks/base.yml" in hooks
    assert "`~/code2/AGENTS.md`" in (out / "AGENTS.md").read_text()
    assert "git_user_name: BrianMills2718" in (out / ".copier-answers.yml").read_text()


@pytest.mark.req("portable-template/the-template-is-served-from-here")
def test_the_template_is_served_from_here():
    copier = (ROOT / "copier.yml").read_text()
    assert "_subdirectory: template" in copier and ADDRESS in copier
    assert f"copier copy --trust {ADDRESS}" in (ROOT / "README.md").read_text()


def _commit(repo: Path, name: str) -> str:
    (repo / name).write_text(name)
    env = {"PATH": os.environ["PATH"], "HOME": str(repo.parent), "GIT_CONFIG_NOSYSTEM": "1"}
    subprocess.run(["git", "-C", str(repo), "add", name], check=True, env=env)
    done = subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid",
                           "commit", "-m", name], capture_output=True, text=True, env=env)
    assert done.returncode == 0, done.stderr
    return done.stdout + done.stderr


@pytest.mark.req("portable-template/a-moved-copy-and-a-worktree-still-run-the-hooks")
def test_a_moved_copy_and_a_worktree_still_run_the_hooks(tmp_path):
    if not shutil.which("lefthook"):
        pytest.skip("lefthook is not installed")
    out = render(tmp_path)
    for hook in ("pre-commit", "pre-push"):
        script = out / ".githooks" / hook
        assert os.access(script, os.X_OK) and f"lefthook run {hook}" in script.read_text()
        assert not _OWNER.search(script.read_text()) and "/home/" not in script.read_text()
    tasks = (ROOT / "copier.yml").read_text()
    assert "git config --local core.hooksPath .githooks" in tasks and "lefthook install" not in tasks
    assert "no_auto_install: true" in (out / "lefthook.yml").read_text()
    (out / "lefthook.yml").write_text("pre-commit:\n  jobs:\n    - name: marker\n      run: echo HOOK-MARKER\n")
    subprocess.run(["git", "init", "-q", "-b", "main", str(out)], check=True)
    subprocess.run(["git", "-C", str(out), "config", "--local", "core.hooksPath", ".githooks"], check=True)
    subprocess.run(["git", "-C", str(out), "add", "-A"], check=True)  # a worktree checks out only committed files
    assert "HOOK-MARKER" in _commit(out, "first")
    moved = tmp_path / "moved"
    out.rename(moved)
    assert "HOOK-MARKER" in _commit(moved, "after-move")
    tree = tmp_path / "tree"
    subprocess.run(["git", "-C", str(moved), "worktree", "add", "-q", "-b", "side", str(tree)], check=True)
    assert "HOOK-MARKER" in _commit(tree, "in-worktree")


def test_machine_bound_names_each_mention(tmp_path):
    (tmp_path / "AGENTS.md").write_text("Rules: `~/code2/AGENTS.md`\n")
    (tmp_path / "pyproject.toml").write_text(f'x = "{LOCKSTEP_URL}.git"\n')
    assert machine_bound(tmp_path) == ["AGENTS.md:1: Rules: `~/code2/AGENTS.md`"]


@pytest.mark.req("portable-template/an-ignored-status-page-does-not-block-a-commit")
def test_an_ignored_status_page_does_not_block_a_commit(tmp_path):
    out = render(tmp_path)
    assert "docs/status.md" in (out / ".gitignore").read_text().splitlines()
    hooks = (out / "lefthook.yml").read_text()
    line = re.search(r"name: lockstep-fast\n(?:\s+#.*\n)*\s+run: (.*)", hooks).group(1)
    assert "uv run lockstep check project" in line and line.endswith("&& make fast")
    job = line.replace("uv run lockstep check project",
                       "printf 'rewrote docs/status.md\\nrewrote src/demo/a.py\\n'").replace("make fast", "true")
    subprocess.run(["git", "init", "-q", str(out)], check=True)
    (out / "src" / "demo").mkdir(parents=True, exist_ok=True)
    (out / "src" / "demo" / "a.py").write_text("x = 1\n")
    (out / "docs" / "status.md").write_text("status\n")
    done = subprocess.run(["sh", "-c", job], cwd=out, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    staged = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=out, capture_output=True,
                            text=True, check=True).stdout.split()
    assert staged == ["src/demo/a.py"]


@pytest.mark.req("portable-template/a-rendered-copy-has-both-hook-files")
def test_a_rendered_copy_has_both_hook_files(tmp_path):
    import json
    out = render(tmp_path)
    for rel in (".claude/settings.json", ".codex/hooks.json"):
        config = json.loads((out / rel).read_text())
        commands = [h["command"] for g in config["hooks"]["PreToolUse"] for h in g["hooks"]]
        assert commands and all("uv run" in c and "lockstep-hook" in c and "PCW_MODE" not in c for c in commands), rel
        assert any("Edit" in g["matcher"] or "apply_patch" in g["matcher"] for g in config["hooks"]["PreToolUse"])
    assert "--client codex" in (out / ".codex/hooks.json").read_text()
    assert "docs/links.json" in (out / ".gitignore").read_text().splitlines()
