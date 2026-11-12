"""Shared fixtures: the smallest example (example-simple), adopted, planned and committed."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent  # tests/lockstep: the examples and e2e scripts
EXAMPLE = REPO / "example-simple"
BIN = Path(sys.executable).parent
# Git exports GIT_DIR, GIT_INDEX_FILE and the like to hooks. Run from Lockstep's pre-push hook
# (`make status` records test results), the example projects' git commands would otherwise act on
# the repository being pushed and commit test fixtures onto its branch. Drop them for every test.
for _var in subprocess.run(["git", "rev-parse", "--local-env-vars"], capture_output=True, text=True).stdout.split():
    os.environ.pop(_var, None)
ENV = {**os.environ, "PATH": f"{BIN}{os.pathsep}{os.environ['PATH']}", "PYTHONDONTWRITEBYTECODE": "1",
       "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
       "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}


def sh(cmd: str, cwd: Path) -> str:
    p = subprocess.run(cmd, shell=True, cwd=cwd, env=ENV, capture_output=True, text=True)
    assert p.returncode == 0, f"{cmd}: {p.stdout}{p.stderr}"
    return p.stdout


@pytest.fixture(scope="session")
def planned(tmp_path_factory) -> Path:
    """The smallest example, adopted and committed: one planned source file with its plan copied in."""
    proj = tmp_path_factory.mktemp("check") / "greeter"
    proj.mkdir()
    (proj / ".gitignore").write_text("__pycache__/\n.lockstep/\n")
    shutil.copytree(EXAMPLE / "plans", proj / "plans")
    shutil.copy(EXAMPLE / "Makefile", proj / "Makefile")
    sh("git init -q -b main", proj)
    sh('aes init --project-id greeter --actor "someone" --outcome "greet returns a greeting."', proj)
    sh("git add -A && git commit -q -m init", proj)
    sh("aes plan accept plans/plan-001.yaml", proj)
    for rel in ["src/greeter/__init__.py", "tests/test_greet.py"]:
        (proj / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(EXAMPLE / rel, proj / rel)
    sh("make project", proj)
    sh("git add -A && git commit -q -m planned", proj)
    return proj


@pytest.fixture
def proj(planned, tmp_path) -> Path:
    dest = tmp_path / "greeter"
    shutil.copytree(planned, dest, symlinks=True)
    return dest
