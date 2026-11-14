"""The ledger reads Project Meta and its callers and changes nothing (retirement plan, slice 0)."""
import importlib.util
import subprocess
from pathlib import Path

spec = importlib.util.spec_from_file_location("ledger", Path(__file__).parents[1] / "scripts" / "project_meta_ledger.py")
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)


def _world(tmp_path):
    pm = tmp_path / "project-meta"
    (pm / "scripts").mkdir(parents=True)
    (pm / "scripts" / "cap.py").write_text("x")
    (pm / "scripts" / "unused.py").write_text("x")
    for cmd in (["init", "-q"], ["add", "-A"], ["-c", "user.email=t@e", "-c", "user.name=t", "commit", "-q", "-m", "f"]):
        subprocess.run(["git", "-C", str(pm), *cmd], check=True)
    other = tmp_path / "other"
    other.mkdir()
    (other / "hook.sh").write_text("python project-meta/scripts/cap.py\n")
    (other / "notes.md").write_text("see project-meta/scripts/unused.py\n")
    return pm, tmp_path


def test_code_callers_are_counted_and_doc_mentions_are_not(tmp_path):
    pm, ws = _world(tmp_path)
    found = ledger.repo_callers(pm, ws, ledger.called_files(pm))
    assert found == {"other": {"scripts/cap.py": 1}}


def test_a_unit_mentioning_the_name_is_listed_and_commands_too(tmp_path):
    ud = tmp_path / "u"
    ud.mkdir()
    (ud / "a.service").write_text("ExecStart=/x/project-meta/scripts/cap.py\n")
    (ud / "b.service").write_text("ExecStart=/x/other\n")
    assert [u["unit"] for u in ledger.units([ud], "project-meta")] == ["a.service"]
    bd = tmp_path / "bin"
    bd.mkdir()
    (bd / "tool").write_text("cd ~/code2/project-meta\n")
    (bd / "other").write_text("nothing\n")
    assert ledger.commands(bd, "project-meta") == ["tool"]


def test_not_a_checkout_is_an_error(tmp_path):
    assert ledger.main(["--repo", str(tmp_path), "--workspace", str(tmp_path), "--bin-dir", str(tmp_path)]) == 2
