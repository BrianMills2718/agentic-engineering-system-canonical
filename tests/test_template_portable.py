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


@pytest.mark.req("portable-template/a-rendered-copy-s-decision-governs-a-real-file")
def test_a_rendered_copy_s_decision_governs_a_real_file(tmp_path):
    from lockstep.decisions import read
    out = render(tmp_path)
    (first,) = read(out)
    assert first.raw == ["docs/architecture/model.c4"] and first.paths == ["docs/architecture/model.c4"]


def _git(repo: Path, *args: str) -> None:
    env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1"}
    for name in ("GIT_DIR", "GIT_INDEX_FILE", "GIT_WORK_TREE"):
        env.pop(name, None)
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
                   check=True, capture_output=True, text=True, env=env)


@pytest.mark.req("portable-template/a-fresh-copy-refuses-an-unplanned-source-file")
def test_a_fresh_copy_refuses_an_unplanned_source_file(tmp_path):
    import json
    import sys

    import yaml

    from lockstep.symbol_gate import added_symbol_problems
    out = render(tmp_path)
    plan = yaml.safe_load((out / "lockstep.yaml").read_text())
    assert plan["governed"] == ["src/demo/"] and plan["fixed"] == ["src/demo/*"]
    rows = {r["path"]: r for r in plan["layout"]}
    assert set(rows) == {"src/demo/__init__.py", "src/demo/core.py", "src/demo/cli.py"}
    assert rows["src/demo/core.py"]["exports"] == ["version() -> str"]
    for rel in rows:
        text = (out / rel).read_text()
        assert "[[[" + "cog" in text and f'c.docstring("{rel.replace("/", ":")}"' in text, rel
        assert added_symbol_problems(out, rel, text, None) == [], rel
    assert "Implements:" not in (out / "src/demo/core.py").read_text()  # the generated text carries it
    call = {"tool_name": "Write", "tool_input": {"file_path": str(out / "src/demo/extra.py"), "content": "x = 1\n"}}
    env = {k: v for k, v in os.environ.items() if k != "PCW_MODE"}
    done = subprocess.run([sys.executable, "-c", "from lockstep.hook import main; raise SystemExit(main())"],
                          input=json.dumps(call), cwd=out, capture_output=True, text=True, env=env, timeout=60)
    decision = json.loads(done.stdout)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny" and "lockstep.yaml" in decision["permissionDecisionReason"]
    agents = (out / "AGENTS.md").read_text()
    assert "uv run lockstep layout" in agents and "`layout:` row" in agents
    assert "lockstep check --repo . --base" in (out / "Makefile").read_text()


@pytest.mark.slow
@pytest.mark.req("portable-template/an-update-of-an-older-copy-keeps-it-without-a-plan")
def test_an_update_of_an_older_copy_keeps_it_without_a_plan(tmp_path):
    import sys

    if not shutil.which("uvx"):
        pytest.skip("uvx is not installed")
    old_ref = "2e8791447"  # the template just before it shipped lockstep.yaml (#1027)
    if subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{old_ref}^{{commit}}"]).returncode != 0:
        pytest.skip(f"commit {old_ref} is not in this clone")
    src = tmp_path / "src"
    src.mkdir()
    archive = subprocess.run(["git", "-C", str(ROOT), "archive", old_ref, "copier.yml", "template"],
                             check=True, capture_output=True)
    subprocess.run(["tar", "-x", "-C", str(src)], input=archive.stdout, check=True)
    _git(src, "init", "-q", "-b", "main")
    _git(src, "add", "-A")
    _git(src, "commit", "-qm", "old")
    _git(src, "tag", "v1")
    out = tmp_path / "out"
    base = ["uvx", "copier"]
    subprocess.run([*base, "copy", "--trust", "--defaults", "--skip-tasks", "--vcs-ref", "v1", "--data",
                    "project_name=demo", "--data", "description=Demo", str(src), str(out)],
                   check=True, capture_output=True, text=True, timeout=300)
    assert not (out / "lockstep.yaml").exists()
    starters = {p.name: p.read_text() for p in (out / "src/demo").glob("*.py")}
    assert "Implements: core/reports-its-version" in starters["core.py"]
    _git(out, "init", "-q", "-b", "main")
    _git(out, "add", "-A")
    _git(out, "commit", "-qm", "copy")
    shutil.rmtree(src / "template")
    shutil.copy(ROOT / "copier.yml", src / "copier.yml")
    shutil.copytree(ROOT / "template", src / "template", ignore=shutil.ignore_patterns(".venv", "__pycache__"))
    _git(src, "add", "-A")
    _git(src, "commit", "-qm", "new")
    _git(src, "tag", "v2")
    subprocess.run([*base, "update", "--trust", "--defaults", "--skip-tasks", "--vcs-ref", "v2"], cwd=out,
                   check=True, capture_output=True, text=True, timeout=300)
    assert not (out / "lockstep.yaml").exists()
    assert {p.name: p.read_text() for p in (out / "src/demo").glob("*.py")} == starters
    assert "uv run lockstep layout" in (out / "AGENTS.md").read_text()
    trace = subprocess.run([sys.executable, "-c", "import sys; from lockstep.check import cli; "
                            "sys.argv = ['lockstep', 'check', 'trace', '--repo', '.']; raise SystemExit(cli())"],
                           cwd=out, capture_output=True, text=True, timeout=120)
    assert trace.returncode == 0, trace.stdout + trace.stderr
    _git(out, "add", "-A")
    _git(out, "commit", "-qm", "update")
    (out / "src/demo/extra.py").write_text("x = 1\n")
    _git(out, "add", "-A")
    _git(out, "commit", "-qm", "change")
    whole = subprocess.run([sys.executable, "-c", "import sys; from lockstep.check import cli; "
                            "sys.argv = ['lockstep', 'check', '--repo', '.', '--base', 'HEAD~1']; raise SystemExit(cli())"],
                           cwd=out, capture_output=True, text=True, timeout=120)
    assert whole.returncode == 0 and "decision=allow" in whole.stdout, whole.stdout + whole.stderr


@pytest.mark.slow
@pytest.mark.req("portable-template/a-default-copy-with-no-remote-passes-make-check")
def test_a_default_copy_with_no_remote_passes_make_check(tmp_path):
    if not (shutil.which("uvx") and shutil.which("openspec")):
        pytest.skip("uvx or openspec is not installed")
    src = tmp_path / "src"
    src.mkdir()
    shutil.copy(ROOT / "copier.yml", src)
    shutil.copytree(ROOT / "template", src / "template", ignore=shutil.ignore_patterns(".venv", "__pycache__"))
    out = tmp_path / "out"
    subprocess.run(["uvx", "copier", "copy", "--trust", "--defaults", "--data", "project_name=demo", "--data",
                    "description=Demo", str(src), str(out)], check=True, capture_output=True, text=True, timeout=900)
    _git(out, "add", "-A")
    _git(out, "commit", "-qm", "first", "--no-verify")
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "VIRTUAL_ENV"))}
    done = subprocess.run(["make", "check"], cwd=out, capture_output=True, text=True, env=env, timeout=900)
    assert done.returncode == 0, done.stdout[-3000:] + done.stderr[-3000:]
    assert "OUTCOME decision=allow" in done.stdout
    (out / "src/demo/extra.py").write_text('"""A file no layout row names."""\n')
    _git(out, "add", "-A")
    _git(out, "commit", "-qm", "unplanned", "--no-verify")
    refused = subprocess.run(["make", "check"], cwd=out, capture_output=True, text=True, env=env, timeout=900)
    assert refused.returncode != 0
    assert "src/demo/extra.py" in refused.stdout + refused.stderr
