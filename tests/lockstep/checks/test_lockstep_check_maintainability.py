"""`lockstep check maintainability`: only findings this branch adds fail; old ones never do; off unless switched on."""
import json
import subprocess
from pathlib import Path

import pytest

from lockstep.checks import maintainability as m
from lockstep.checks.cli import run as run_check


GIT = ["-c", "user.name=t", "-c", "user.email=t@t"]

COMPLEX = """def busy(a):
    if a == 1:
        return 1
    if a == 2:
        return 2
    if a == 3:
        return 3
    if a == 4:
        return 4
    if a == 5:
        return 5
    if a == 6:
        return 6
    if a == 7:
        return 7
    if a == 8:
        return 8
    if a == 9:
        return 9
    if a == 10:
        return 10
    return 0
"""

BLOCK = "".join(f"    total = total + value * {i} - offset_{i}\n" for i in range(10))
DUPLICATED = f"def first(value):\n    total = 0\n{BLOCK}    return total\n"
COPY = f"def second(value):\n    total = 0\n{BLOCK}    return total\n"


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *GIT, *args], check=True, capture_output=True)


def repo(tmp_path, files):
    root = tmp_path / "r"
    (root / "src").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    for name, text in files.items():
        (root / name).write_text(text)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    git(root, "checkout", "-qb", "work")
    return root


def run(root, capsys, **kw):
    code = m.main(["--repo", str(root), "--base", "main", *sum(([f"--{k}", str(v)] for k, v in kw.items()), [])])
    return code, capsys.readouterr().out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_new_blind_except_fails(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": "def f():\n    return 1\n"})
    (root / "src/a.py").write_text("def f():\n    try:\n        return 1\n    except Exception:\n        return 2\n")
    code, out = run(root, capsys)
    assert code == 1 and "BLE001" in out and "RESULT maintainability new=1" in out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_old_blind_except_moved_by_unrelated_edit_passes(tmp_path, capsys):
    old = "def f():\n    try:\n        return 1\n    except Exception:\n        return 2\n"
    root = repo(tmp_path, {"src/a.py": old})
    (root / "src/a.py").write_text("X = 1\n\n\n" + old)
    code, out = run(root, capsys)
    assert code == 0, out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_body_edit_raising_complexity_fails(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": COMPLEX})
    (root / "src/a.py").write_text(COMPLEX.replace("    return 0\n", "    if a == 11:\n        return 11\n    return 0\n"))
    code, out = run(root, capsys)
    assert code == 1 and "C901" in out and "busy" in out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_unrelated_edit_in_complex_function_passes(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": COMPLEX})
    (root / "src/a.py").write_text(COMPLEX.replace("return 5\n", "return 5  # five\n"))
    code, out = run(root, capsys)
    assert code == 0, out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_lowering_complexity_passes(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": COMPLEX.replace("    return 0\n", "    if a == 11:\n        return 11\n    return 0\n")})
    (root / "src/a.py").write_text(COMPLEX)
    code, out = run(root, capsys)
    assert code == 0, out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_renamed_file_keeps_its_old_findings(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": COMPLEX})
    git(root, "mv", "src/a.py", "src/b.py")
    code, out = run(root, capsys)
    assert code == 0, out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_new_duplicate_block_fails(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": DUPLICATED, "src/b.py": "def g():\n    return 1\n"})
    (root / "src/b.py").write_text(COPY)
    code, out = run(root, capsys)
    assert code == 1 and "duplicate" in out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_existing_duplicate_passes(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": DUPLICATED, "src/b.py": COPY})
    (root / "src/b.py").write_text(COPY + "\n\nY = 2\n")
    code, out = run(root, capsys)
    assert code == 0, out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_large_file_growing_fails_and_shrinking_passes(tmp_path, capsys):
    body = "".join(f"V{i} = {i}\n" for i in range(30))
    root = repo(tmp_path, {"src/big.py": body})
    (root / "src/big.py").write_text(body + "V_NEW = 1\n")
    code, out = run(root, capsys, **{"max-lines": 20})
    assert code == 1 and "file-growth src/big.py" in out
    (root / "src/big.py").write_text(body[: body.index("V29")])
    code, out = run(root, capsys, **{"max-lines": 20})
    assert code == 0, out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_untracked_new_file_is_read(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": "A = 1\n"})
    (root / "src/new.py").write_text("def f():\n    try:\n        pass\n    except Exception:\n        pass\n")
    code, out = run(root, capsys)
    assert code == 1 and "src/new.py" in out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_missing_base_is_skipped(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": "A = 1\n"})
    code = m.main(["--repo", str(root), "--base", "no-such-branch"])
    out = capsys.readouterr().out
    assert code == 0 and "skipped=base-missing" in out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_no_python_change_skips_the_tools(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": "A = 1\n", "notes.txt": "x"})
    (root / "notes.txt").write_text("y")
    code, out = run(root, capsys)
    assert code == 0 and "skipped=no-python-change" in out


def _cache_files(root):
    return list((root / ".git" / "maintainability-ratchet").glob("*.json"))


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_ruff_failure_fails_closed_and_caches_nothing(tmp_path, capsys, monkeypatch):
    root = repo(tmp_path, {"src/a.py": "A = 1\n", "src/b.py": "B = 1\n"})
    (root / "src/a.py").write_text("A = 2\n")
    monkeypatch.setattr(m, "RUFF", ["false"])
    code, out = run(root, capsys)
    assert code == 2 and "tool-failed" in out and not _cache_files(root)


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_rename_inside_a_package_keeps_old_duplicates(tmp_path, capsys):
    root = tmp_path / "r"
    (root / "src/pkg").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    for name, text in {"src/pkg/__init__.py": "", "src/pkg/one.py": DUPLICATED, "src/pkg/two.py": COPY}.items():
        (root / name).write_text(text)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    git(root, "checkout", "-qb", "work")
    git(root, "mv", "src/pkg/two.py", "src/pkg/three.py")
    code, out = run(root, capsys)
    assert code == 0, out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_old_finding_moved_to_another_file_passes(tmp_path, capsys):
    blind = "def f():\n    try:\n        return 1\n    except Exception:\n        return 2\n"
    root = repo(tmp_path, {"src/a.py": blind + "\n\n" + COMPLEX, "src/helpers.py": "H = 1\n"})
    (root / "src/a.py").write_text("A = 1\n")
    (root / "src/helpers.py").write_text("H = 1\n\n\n" + blind + "\n\n" + COMPLEX)
    code, out = run(root, capsys)
    assert code == 0, out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_damaged_cache_is_recomputed(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": "A = 1\n", "src/b.py": "B = 1\n"})
    (root / "src/a.py").write_text("A = 2\n")
    assert run(root, capsys)[0] == 0
    [cached] = _cache_files(root)
    cached.write_text("{half")
    code, out = run(root, capsys)
    assert code == 0, out
    assert json.loads(cached.read_text())["dup"] == {}


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_third_copy_of_an_existing_duplicate_fails(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": DUPLICATED, "src/b.py": COPY})
    (root / "src/c.py").write_text(COPY.replace("def second(", "def third("))
    code, out = run(root, capsys)
    assert code == 1 and "duplicate code" in out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_same_docstring_text_in_a_new_file_is_not_duplicate_code(tmp_path, capsys):
    doc = '"""' + "".join(f"Requirement line {i} copied from the plan.\n" for i in range(12)) + '"""\n'
    root = repo(tmp_path, {"src/a.py": doc + "A = 1\n"})
    (root / "src/b.py").write_text(doc + "B = 2\n")
    code, out = run(root, capsys)
    assert code == 0, out


@pytest.mark.req("lockstep-checks/maintainability-only-findings-the-branch-adds-fail", existing=True)  # moved unchanged from scripts/maintainability_ratchet.py
def test_shared_multi_line_import_is_not_duplicate_code(tmp_path, capsys):
    names = "".join(f"    Name{i},\n" for i in range(8))
    root = repo(tmp_path, {"src/a.py": f"from .records import (\n{names})\n\nA = Name1\n"})
    (root / "src/b.py").write_text(f"from .records import (\n{names})\n\nB = Name2\n")
    code, out = run(root, capsys)
    assert code == 0, out


@pytest.mark.req("lockstep-checks/maintainability-off-unless-switched-on")
def test_off_unless_switched_on(tmp_path, capsys):
    root = repo(tmp_path, {"src/a.py": "def ok():\n    return 1\n"})
    (root / "src/a.py").write_text("def ok():\n    try:\n        return 1\n    except Exception:\n        pass\n")
    assert run_check(["maintainability", "--repo", str(root), "--base", "main"]) == 0
    assert "maintainability: skipped (off)" in capsys.readouterr().out
    (root / "lockstep.yaml").write_text("checks:\n  maintainability: block\n")
    assert run_check(["maintainability", "--repo", str(root), "--base", "main", "--folders", "src"]) == 1
    assert "RESULT maintainability new=" in capsys.readouterr().out
