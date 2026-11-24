"""Tests for src/lockstep/prior_art.py (ported from code2-workspace tests/test_prior_art_check.py at ec500633) on throwaway repositories."""

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "src" / "lockstep" / "prior_art.py"
SCHEMA = ROOT / "src" / "lockstep" / "prior-art.schema.json"

GOOD = {
    "need": "A feature cannot be committed without a decided prior-art search.",
    "searched": [
        {"place": "own", "where": "capabilities list", "query": "prior art", "found": "no row"},
        {"place": "outside", "where": "PyPI", "query": "prior art check", "found": "nothing that refuses"},
    ],
    "candidates": [
        {"name": "jsonschema", "url": "https://json-schema.org", "covers": "record shape",
         "misses": "selection", "verdict": "combine", "reason": "standard exists"},
        {"name": "template", "url": "https://example.org", "covers": "prose", "verdict": "reject",
         "reason": "cannot be refused"},
    ],
    "decision": "combine",
    "gap": "none that matters",
    "decided": "2026-11-18",
}


def make_change(repo: Path, name="add-x", created="2026-11-18", header="## ADDED Requirements",
                record=None, archived=False) -> Path:
    base = repo / "openspec" / "changes" / ("archive" if archived else "") / name
    (base / "specs" / "cap").mkdir(parents=True)
    (base / ".openspec.yaml").write_text(f"schema: spec-driven\ncreated: {created}\n")
    (base / "specs" / "cap" / "spec.md").write_text(f"{header}\n\n### Requirement: x\n")
    if record is not None:
        (base / "prior-art.json").write_text(record if isinstance(record, str) else json.dumps(record))
    return base


def run(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), "--repo", str(repo), *args],
                          capture_output=True, text=True)


def good(**changes):
    rec = copy.deepcopy(GOOD)
    for key, value in changes.items():
        if value is None:
            rec.pop(key, None)
        else:
            rec[key] = value
    return rec


@pytest.mark.req("prior-art-check/no-record-on-a-change-that-adds-a-requirement")
def test_no_record_on_a_change_that_adds_a_requirement(tmp_path):
    make_change(tmp_path)
    result = run(tmp_path)
    assert result.returncode == 1
    assert "openspec/changes/add-x/prior-art.json" in result.stdout


@pytest.mark.req("prior-art-check/complete-record")
def test_complete_record(tmp_path):
    make_change(tmp_path, record=GOOD)
    result = run(tmp_path)
    assert result.returncode == 0, result.stdout
    assert "1 changes looked at, 1 need a record, 1 passes, 0 fails" in result.stdout


@pytest.mark.req("prior-art-check/invalid-json")
def test_invalid_json(tmp_path):
    make_change(tmp_path, record="{not json")
    assert run(tmp_path).returncode == 1


@pytest.mark.req("prior-art-check/verdict-not-yet-evaluated")
def test_verdict_not_yet_evaluated(tmp_path):
    rec = good()
    rec["candidates"][1]["verdict"] = "not yet evaluated"
    make_change(tmp_path, record=rec)
    assert run(tmp_path).returncode == 1


@pytest.mark.req("prior-art-check/build-without-a-gap")
def test_build_without_a_gap(tmp_path):
    rec = good(decision="build", gap=None)
    rec["candidates"] = [rec["candidates"][1]]
    make_change(tmp_path, record=rec)
    assert run(tmp_path).returncode == 1


@pytest.mark.req("prior-art-check/build-while-a-candidate-is-adopted")
def test_build_while_a_candidate_is_adopted(tmp_path):
    rec = good(decision="build", gap="something")
    rec["candidates"][0]["verdict"] = "adopt"
    make_change(tmp_path, record=rec)
    assert run(tmp_path).returncode == 1


@pytest.mark.req("prior-art-check/adopt-without-an-adopted-candidate")
def test_adopt_without_an_adopted_candidate(tmp_path):
    make_change(tmp_path, record=good(decision="adopt"))
    assert run(tmp_path).returncode == 1


@pytest.mark.req("prior-art-check/search-with-nothing-outside")
def test_search_with_nothing_outside(tmp_path):
    rec = good()
    rec["searched"] = [rec["searched"][0]]
    make_change(tmp_path, record=rec)
    assert run(tmp_path).returncode == 1


@pytest.mark.req("prior-art-check/only-modified-requirements")
def test_only_modified_requirements(tmp_path):
    make_change(tmp_path, header="## MODIFIED Requirements")
    result = run(tmp_path)
    assert result.returncode == 0
    assert "0 need a record" in result.stdout


@pytest.mark.req("prior-art-check/change-before-the-start-date")
def test_change_before_the_start_date(tmp_path):
    make_change(tmp_path, created="2026-11-17")
    result = run(tmp_path)
    assert result.returncode == 0
    assert "0 need a record" in result.stdout


def undated(base: Path) -> None:
    (base / ".openspec.yaml").write_text("schema: spec-driven\n")


def git(repo: Path, *args: str, date: str | None = None) -> None:
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t", "PATH": "/usr/bin:/bin", "HOME": str(repo)}
    if date:
        env |= {"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, env=env)


@pytest.mark.req("prior-art-check/undated-change-first-committed-before-the-start-date")
def test_undated_change_first_committed_before_the_start_date(tmp_path):
    undated(make_change(tmp_path))
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "old change", date="2026-11-13T12:00:00+00:00")
    result = run(tmp_path)
    assert result.returncode == 0, result.stdout
    assert "0 need a record" in result.stdout


@pytest.mark.req("prior-art-check/undated-change-never-committed", existing=True)
def test_undated_change_never_committed(tmp_path):
    undated(make_change(tmp_path))
    git(tmp_path, "init", "-q")
    result = run(tmp_path)
    assert result.returncode == 1
    assert "no prior-art record" in result.stdout


@pytest.mark.req("prior-art-check/archived-change")
def test_archived_change(tmp_path):
    make_change(tmp_path, archived=True)
    result = run(tmp_path)
    assert result.returncode == 0
    assert "0 changes looked at" in result.stdout


@pytest.mark.req("prior-art-check/archived-change-named-by-files")
def test_archived_change_named_by_files(tmp_path):
    make_change(tmp_path, name="2026-11-18-add-x", archived=True)
    result = run(tmp_path, "--files", "openspec/changes/archive/2026-11-18-add-x/specs/cap/spec.md")
    assert result.returncode == 1
    assert "2026-11-18-add-x: no prior-art record" in result.stdout
    assert "1 changes looked at, 1 need a record, 0 passes, 1 fails" in result.stdout


@pytest.mark.req("prior-art-check/files-limit-the-check")
def test_files_limit_the_check(tmp_path):
    make_change(tmp_path, name="has-record", record=GOOD)
    make_change(tmp_path, name="no-record")
    only = "openspec/changes/has-record/specs/cap/spec.md"
    assert run(tmp_path, "--files", only).returncode == 0
    assert run(tmp_path).returncode == 1


@pytest.mark.req("prior-art-check/real-record-against-the-real-schema")
def test_real_record_against_the_real_schema():
    from jsonschema import Draft202012Validator

    schema = json.loads(SCHEMA.read_text())
    Draft202012Validator.check_schema(schema)
    # The record of the change that ported the check, copied from its archived folder before the archive was removed.
    own = Path(__file__).with_name("fixtures") / "prior-art-portable-ship.json"
    record = json.loads(own.read_text())
    assert list(Draft202012Validator(schema).iter_errors(record)) == []


@pytest.mark.req("prior-art-check/complete-record")
def test_lockstep_command_runs_the_check(tmp_path, monkeypatch):
    from lockstep import check

    monkeypatch.setattr(sys, "argv", ["lockstep", "check", "prior-art", "--repo", str(tmp_path)])
    make_change(tmp_path, record=GOOD)
    assert check.cli() == 0
    make_change(tmp_path, name="no-record")
    assert check.cli() == 1
