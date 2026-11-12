"""Behavior 5.2: `pcw check`, the whole-tree check the Project Brain runner calls before it commits."""

import json
import subprocess
import sys

import pytest
from pathlib import Path

from lockstep_support import ENV, sh

from lockstep.check import check
from lockstep.cogtext import CLOSE, OPEN

def run_cli(proj: Path) -> tuple[int, dict]:
    p = subprocess.run([sys.executable, "-m", "lockstep.check", "--repo", str(proj), "--json"],
                       env=ENV, capture_output=True, text=True)
    return p.returncode, json.loads(p.stdout)


def test_matching_planned_file_allows(proj):
    code = proj / "src/greeter/__init__.py"
    code.write_text(code.read_text().replace('f"Hello, {name}!"', 'f"Hello, {name}!"  # same greeting'))
    rc, out = run_cli(proj)
    assert (rc, out["decision"]) == (0, "allow")
    assert [(f["path"], f["kind"]) for f in out["files"]] == [("src/greeter/__init__.py", "planned")]
    assert "1 planned file checked, none stale" in out["summary"]


def test_stale_docstring_blocks(proj):
    code = proj / "src/greeter/__init__.py"
    code.write_text(code.read_text().replace("NI-001:", "NI-001: (edited by hand)"))
    rc, out = run_cli(proj)
    assert (rc, out["decision"]) == (1, "block")
    assert out["files"][0]["kind"] == "stale" and "no longer matches its plan" in out["files"][0]["reason"]


def test_new_unplanned_file_in_governed_folder_blocks(proj):
    (proj / "src/greeter/extra.py").write_text("X = 1\n")
    rc, out = run_cli(proj)
    assert (rc, out["decision"]) == (1, "block")
    assert out["files"] == [{"path": "src/greeter/extra.py", "kind": "unplanned", "blocks": True,
                             "reason": out["files"][0]["reason"]}]
    assert "is not in the plan" in out["files"][0]["reason"]


def test_file_outside_governed_folders_is_ignored(proj):
    (proj / "NOTES.md").write_text("a note\n")
    rc, out = run_cli(proj)
    assert (rc, out["decision"], out["files"], out["ignored"]) == (0, "allow", [], 1)


def test_agent_editing_the_plan_blocks(proj):
    target = proj / ".aes/target.yaml"
    target.write_text(target.read_text() + "\n")
    out = check(proj)
    assert out["decision"] == "block" and out["counts"]["plan_edit"] == 1


def _accept(proj):
    """`aes plan accept` on the example's second plan, left uncommitted as an agent would have it."""
    sh("aes plan accept plans/plan-002.yaml", proj)
    return next((proj / ".aes/plans").glob("*002*.yaml"))


def test_accepted_plan_passes_uncommitted_and_committed(proj):
    plan = _accept(proj)
    rc, out = run_cli(proj)
    assert (rc, out["decision"]) == (0, "allow")
    assert out["counts"]["plan_accepted"] == 2 and out["counts"]["plan_edit"] == 0
    assert {f["path"] for f in out["files"]} == {".aes/target.yaml", plan.relative_to(proj).as_posix()}
    assert "accepted." in out["summary"]
    sh("git add -A && git commit -q -m 'accept plan 2'", proj)
    assert check(proj, "HEAD~1")["decision"] == "allow"  # the branch's view: base before the accept


def test_accepted_plan_then_edited_by_hand_blocks(proj):
    _accept(proj)
    target = proj / ".aes/target.yaml"
    target.write_text(target.read_text().replace("greet returns a greeting", "greet returns a long greeting", 1))
    out = check(proj)
    assert out["decision"] == "block" and out["counts"]["plan_edit"] == 2
    assert all("edited by hand as well as accepted" in f["reason"] for f in out["files"])


def test_editing_an_accepted_plan_file_blocks(proj):
    plan = _accept(proj)
    sh("git add -A && git commit -q -m 'accept plan 2'", proj)
    plan.write_text(plan.read_text() + "# a later note\n")
    out = check(proj)
    assert out["decision"] == "block" and out["counts"]["plan_edit"] == 1
    assert "never edited afterwards" in out["files"][0]["reason"]


def test_not_adopted_allows(tmp_path):
    sh("git init -q -b main", tmp_path)
    (tmp_path / "a.py").write_text("x = 1\n")
    out = check(tmp_path)
    assert out["decision"] == "allow" and out["adopted"] is False


def test_text_output_ends_with_counts(proj):
    (proj / "src/greeter/extra.py").write_text("X = 1\n")
    p = subprocess.run([sys.executable, "-m", "lockstep.check", "--repo", str(proj)], env=ENV, capture_output=True, text=True)
    assert p.returncode == 1
    assert p.stdout.splitlines()[-1].startswith("OUTCOME decision=block files=1 unplanned=1 stale=0")


def test_foreign_cog_code_is_not_run_and_blocks(proj, tmp_path):
    """The runner checks a tree an agent wrote, on the host: a planned file's cog block must never execute."""
    marker = tmp_path / "ran"
    code = proj / "src/greeter/__init__.py"
    code.write_text(code.read_text().replace(       # markers built from constants: cog reads them anywhere
        f'{OPEN} import lockstep.cogtext as c; c.docstring("ART-GREET"){CLOSE}',
        f'{OPEN} import pathlib; pathlib.Path("{marker}").write_text("x"){CLOSE}'))
    rc, out = run_cli(proj)
    assert (rc, out["decision"], out["files"][0]["kind"]) == (1, "block", "stale")
    assert "not the standard plan copy" in out["files"][0]["reason"]
    assert not marker.exists()


def test_plan_changed_without_regenerating_blocks(proj):
    """Plan 2 changes the requirement; the agent edits the code but leaves the old copy: held."""
    sh("aes plan accept plans/plan-002.yaml && git add -A && git commit -q -m 'plan 2'", proj)
    code = proj / "src/greeter/__init__.py"
    code.write_text(code.read_text() + "\n# touched\n")
    out = check(proj)
    assert out["decision"] == "block" and out["files"][0]["kind"] == "stale"
    assert "differs from the plan" in out["files"][0]["reason"]
    sh("make project", proj)          # regenerated from the plan: the same change now passes
    assert check(proj)["decision"] == "allow"


def test_a_new_evidence_record_passes_and_an_edited_or_removed_one_blocks(proj):
    """ER-5.2-b: `aes evidence record` output is not a hand edit of the plan; changing a record afterwards is."""
    from agentic_engineering_system.evidence import record

    rec = record(proj, "VS-GREET", []).path
    rel = rec.relative_to(proj).as_posix()
    rc, out = run_cli(proj)
    assert (rc, [(f["path"], f["kind"]) for f in out["files"]]) == (0, [(rel, "evidence")])
    assert "1 new evidence record(s)" in out["summary"]
    sh("git add -A && git commit -q -m 'record the test result'", proj)
    rec.write_text(rec.read_text() + "# edited afterwards\n")
    rc, out = run_cli(proj)
    assert (rc, out["files"][0]["kind"]) == (1, "evidence_edit") and "the change edits it" in out["files"][0]["reason"]
    rec.unlink()
    rc, out = run_cli(proj)
    assert (rc, out["files"][0]["kind"]) == (1, "evidence_edit") and "the change removes it" in out["files"][0]["reason"]
    sh("git checkout -q -- .aes", proj)
    (rec.parent / "OBS-FORGED.yaml").write_text("observation_id: OBS-FORGED\n")
    rc, out = run_cli(proj)
    assert (rc, out["files"][0]["kind"]) == (1, "evidence_edit")
    assert "is not an evidence record" in out["files"][0]["reason"]


def test_a_new_planned_file_without_its_plan_copy_blocks(proj):
    """ER-5.2-c (#64): a planned Python file the change adds must hold its own plan copy, test files included."""
    from lockstep.aes_bridge import context
    from lockstep.cogtext import END, render

    test = proj / "tests/test_greet.py"
    plain = test.read_text()
    sh("git rm -q tests/test_greet.py && git commit -q -m 'drop the test file'", proj)
    test.parent.mkdir(parents=True, exist_ok=True)
    test.write_text(plain)
    rc, out = run_cli(proj)
    assert (rc, [(f["path"], f["kind"]) for f in out["files"]]) == (1, [("tests/test_greet.py", "stale")])
    assert "new planned file" in out["files"][0]["reason"] and "lockstep.scaffold" in out["files"][0]["reason"]
    body = "\n".join(("    " + line).rstrip() for line in render(context(proj, "ART-TEST")))
    test.write_text(f'"""Tests.\n\n{OPEN} import lockstep.cogtext as c; c.docstring("ART-TEST"){CLOSE}\n{body}\n{END}\n"""\n' + plain)
    rc, out = run_cli(proj)            # the same new file with its copy passes
    assert (rc, [(f["path"], f["kind"]) for f in out["files"]]) == (0, [("tests/test_greet.py", "planned")])


@pytest.mark.parametrize("damage", ["missing", "empty", "wrong_artifact"])
def test_required_source_projection_blocks_when_removed_or_replaced(proj, damage):
    from lockstep.check import docstring_mismatch
    from lockstep.cogtext import END, render
    from lockstep.aes_bridge import context

    code = proj / "src/greeter/__init__.py"
    if damage == "missing":
        code.write_text("def greet(name: str) -> str:\n    return f'Hello, {name}!'\n")
    elif damage == "empty":
        code.write_text(f'{OPEN} import lockstep.cogtext as c; c.docstring("ART-GREET"){CLOSE}\n{END}\n')
    else:
        body = "\n".join(("    " + line).rstrip() for line in render(context(proj, "ART-TEST")))
        code.write_text(f'{OPEN} import lockstep.cogtext as c; c.docstring("ART-TEST"){CLOSE}\n{body}\n{END}\n')
    assert docstring_mismatch(proj, "src/greeter/__init__.py") is not None
    out = check(proj)
    assert out["decision"] == "block" and out["counts"]["stale"] == 1


def test_planned_test_without_projection_remains_allowed(proj):
    code = proj / "tests/test_greet.py"
    code.write_text(code.read_text() + "\n# changed test\n")
    assert check(proj)["decision"] == "allow"


@pytest.mark.parametrize("block", [
    f'{OPEN} print("foreign"){CLOSE}\n',
    f'{OPEN} import lockstep.cogtext as c; c.docstring("ART-GREET"){CLOSE}\n',
])
def test_optional_test_projection_still_rejects_invalid_blocks(proj, block):
    from lockstep.check import docstring_mismatch

    (proj / "tests/test_greet.py").write_text(block)
    assert docstring_mismatch(proj, "tests/test_greet.py") is not None


def test_planned_config_without_projection_remains_allowed(proj):
    import yaml
    from lockstep.check import docstring_mismatch

    plan = proj / ".aes/target.yaml"
    data = yaml.safe_load(plan.read_text())
    data["planned_artifacts"].append({"id": "ART-CONFIG", "kind": "config",
                                     "locator": {"exact_path": "settings.yaml"}})
    plan.write_text(yaml.safe_dump(data))
    (proj / "settings.yaml").write_text("enabled: true\n")
    assert docstring_mismatch(proj, "settings.yaml") is None


def _side_file(proj, *declared, include=("*.md",)):
    import yaml
    data = {"schema": "lockstep.side.v1",
            "documents": {"include": list(include),
                          "declared": [{"path": p, "purpose": "why it exists", "refs": ["NI-001"]} for p in declared]}}
    (proj / "lockstep.yaml").write_text(yaml.safe_dump(data, sort_keys=False))


def test_a_change_cannot_declare_its_own_files_in_the_side_file(proj):
    """ER-5.2-e (#67): the side file is read as it is at the base, so a change cannot admit its own files."""
    (proj / "src/greeter/off_plan.py").write_text("X = 1\n")
    _side_file(proj, "src/greeter/off_plan.py")
    rc, out = run_cli(proj)            # an untracked side file declaring the governed file
    assert (rc, [(f["path"], f["kind"]) for f in out["files"]]) == (
        1, [("lockstep.yaml", "side_file"), ("src/greeter/off_plan.py", "unplanned")])
    assert "as they are at HEAD" in out["files"][0]["reason"]
    (proj / ".gitignore").write_text("lockstep.yaml\n")
    rc, out = run_cli(proj)            # the same side file, ignored, so the change shows no trace of it
    assert (rc, [(f["path"], f["kind"]) for f in out["files"]]) == (1, [("src/greeter/off_plan.py", "unplanned")])


def test_a_side_file_change_applies_once_it_is_committed(proj):
    """ER-5.2-e (#67): a document declared in the change is judged by the committed side file."""
    _side_file(proj)
    sh("git add lockstep.yaml && git commit -q -m 'side file: every .md is a document'", proj)
    (proj / "NOTES.md").write_text("a note\n")
    _side_file(proj, "NOTES.md")
    rc, out = run_cli(proj)
    assert (rc, [(f["path"], f["kind"]) for f in out["files"]]) == (
        1, [("NOTES.md", "unplanned"), ("lockstep.yaml", "side_file")])
    sh("git add lockstep.yaml && git commit -q -m 'declare NOTES.md'", proj)
    rc, out = run_cli(proj)            # committed on its own, the declaration now applies
    assert (rc, out["decision"], out["files"]) == (0, "allow", [])


def test_a_change_cannot_add_its_own_files_to_the_legacy_list(proj):
    """ER-5.2-e (#67): the legacy list is read as it is at the base, even when the change hides its edit."""
    (proj / "src/greeter/extra.py").write_text("X = 1\n")
    (proj / ".gitignore").write_text(".aes/legacy_baseline.json\n")
    (proj / ".aes/legacy_baseline.json").write_text(json.dumps({"files": ["src/greeter/extra.py"]}))
    rc, out = run_cli(proj)
    assert (rc, [(f["path"], f["kind"]) for f in out["files"]]) == (1, [("src/greeter/extra.py", "unplanned")])


def _legacy(proj, files):
    (proj / ".aes/legacy_baseline.json").write_text(json.dumps({
        "schema_version": "aes.v0_2.legacy_baseline.v1", "adopted_at_revision": "0" * 40,
        "adopted_at": "2026-11-09T00:00:00+00:00", "governed_roots": ["src/greeter/"],
        "files": {k: v * 40 for k, v in files.items()}}, indent=1))


def test_accept_pruning_the_legacy_list_passes_and_any_other_edit_blocks(proj):
    """ER-5.2-a: `aes plan accept` drops from the legacy list each file now planned or gone; that alone passes."""
    for name in ("old.py", "keep.py"):
        (proj / "src/greeter" / name).write_text("X = 1\n")
    _legacy(proj, {"src/greeter/old.py": "a", "src/greeter/keep.py": "b"})
    sh("git add -A && git commit -q -m 'two legacy files'", proj)
    sh("git rm -q src/greeter/old.py && git commit -q -m 'old.py goes'", proj)
    _accept(proj)
    _legacy(proj, {"src/greeter/keep.py": "b"})
    rc, out = run_cli(proj)
    assert (rc, out["decision"]) == (0, "allow"), out
    _legacy(proj, {})  # drops keep.py, which is still there and not planned
    out = check(proj)
    assert out["decision"] == "block" and any("still in the tree and not planned" in f["reason"] for f in out["files"])
    _legacy(proj, {"src/greeter/keep.py": "b", "src/greeter/new.py": "c"})
    out = check(proj)
    assert out["decision"] == "block" and any("adds or changes src/greeter/new.py" in f["reason"] for f in out["files"])
