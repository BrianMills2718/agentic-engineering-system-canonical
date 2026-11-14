"""Docs triage proposes dispositions by fixed rules and changes nothing (retirement plan, slice 0b)."""
import importlib.util
import os
import subprocess
from pathlib import Path

spec = importlib.util.spec_from_file_location("t", Path(__file__).parents[1] / "scripts" / "project_meta_docs_triage.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)


def _repo(tmp_path, date="2020-01-01T00:00:00"):
    repo = tmp_path / "r"
    (repo / "docs" / "old").mkdir(parents=True)
    (repo / "docs" / "gen").mkdir()
    (repo / "scripts").mkdir()
    (repo / "docs" / "old" / "a.md").write_text("x")
    (repo / "docs" / "gen" / "p.wikitext").write_text("y")
    (repo / "scripts" / "render_gen.py").write_text("OUT = 'docs/gen/p.wikitext'\n")
    env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
    for cmd in (["init", "-q"], ["add", "-A"], ["-c", "user.email=t@e", "-c", "user.name=t", "commit", "-q", "-m", "files"]):
        subprocess.run(["git", "-C", str(repo), *cmd], check=True, env=env)
    return repo


def test_old_unreferenced_folder_is_archive_and_hint_is_only_a_hint(tmp_path):
    rows = {r["folder"]: r for r in t.triage(_repo(tmp_path), "2026-01-01", [])}
    assert rows["old"]["proposed"] == "archive" and rows["old"]["last_commit"] == "2020-01-01"
    assert rows["gen"]["proposed"] == "archive" and rows["gen"]["generated_hint"] is True


def test_recent_change_is_read_even_for_a_generated_folder(tmp_path):
    rows = {r["folder"]: r for r in t.triage(_repo(tmp_path), "2019-01-01", [])}
    assert rows["old"]["proposed"] == "read"
    assert rows["gen"]["proposed"] == "read" and rows["gen"]["generated_hint"] is True


def test_changes_nothing(tmp_path):
    repo = _repo(tmp_path)
    assert t.main(["--repo", str(repo), "--cutoff", "2019-01-01"]) == 0
    status = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True).stdout
    assert status == ""


def test_no_docs_folder_is_an_error(tmp_path):
    assert t.main(["--repo", str(tmp_path)]) == 2
