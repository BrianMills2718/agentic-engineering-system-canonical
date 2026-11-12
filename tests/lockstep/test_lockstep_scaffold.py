"""Behavior 3.3: every declared file that does not exist yet is created with its cog block."""

import subprocess
import sys

from lockstep_support import ENV

from lockstep.cogtext import CLOSE, OPEN


def test_missing_planned_file_is_created_and_others_left_alone(proj):
    code, test = proj / "src/greeter/__init__.py", proj / "tests/test_greet.py"
    before = test.read_bytes()
    code.unlink()
    p = subprocess.run([sys.executable, "-m", "lockstep.scaffold"], cwd=proj, env=ENV, capture_output=True, text=True)
    assert p.returncode == 0 and "src/greeter/__init__.py" in p.stdout, p.stdout + p.stderr
    assert f'{OPEN} import lockstep.cogtext as c; c.docstring("ART-GREET", indent=0){CLOSE}' in code.read_text()
    assert test.read_bytes() == before
