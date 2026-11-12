"""Lockstep installs from AES canonical, and its old `pcw` names keep working (one-tool design, slice 1)."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from lockstep_support import ENV, sh

from lockstep.check import check

BIN = Path(sys.executable).parent


@pytest.mark.req("lockstep-package/the-check-runs-from-an-install")
def test_the_lockstep_command_runs_the_check():
    p = subprocess.run([str(BIN / "lockstep"), "check", "--help"], capture_output=True, text=True, env=ENV)
    assert p.returncode == 0 and "--repo" in p.stdout
    assert shutil.which("lockstep-hook", path=str(BIN))


@pytest.mark.req("lockstep-package/an-old-module-path-runs-the-new-code")
def test_python_m_pcw_runs_the_lockstep_module():
    p = subprocess.run([sys.executable, "-c", "import pcw.check, lockstep; print(pcw.check.__file__)"],
                       capture_output=True, text=True, env=ENV)
    assert p.returncode == 0 and Path(p.stdout.strip()).parent.name == "lockstep"
    p = subprocess.run([sys.executable, "-m", "pcw.check", "--help"], capture_output=True, text=True, env=ENV)
    assert p.returncode == 0 and "--repo" in p.stdout
    for old in ("pcw", "pcw-hook"):
        assert shutil.which(old, path=str(BIN))


@pytest.mark.req("lockstep-package/an-old-cog-block-is-still-a-valid-plan-copy")
def test_a_pcw_cog_block_is_judged_like_a_lockstep_one(proj):
    path = proj / "src/greeter/__init__.py"
    path.write_text(path.read_text().replace("import lockstep.cogtext as c", "import pcw.cogtext as c"))
    assert "import pcw.cogtext" in path.read_text()
    sh("make project", proj)  # cog runs the old import through the alias
    sh("git add -A && git commit -q -m old-name", proj)
    out = check(proj)
    assert out["decision"] == "allow", out
