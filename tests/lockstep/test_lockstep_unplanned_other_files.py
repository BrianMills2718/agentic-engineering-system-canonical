"""Behavior 1.1 (every other file, question Q48): with a `files` section in the side file, every
tracked file outside the governed folders that is not a document must be declared there.

[[[cog import lockstep.cogtext as c; c.docstring("TST-UNPLANNED-OTHER-FILES", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

SC-1.1: An undeclared file under a governed folder is reported; a declared
  file, a legacy file and a file outside every governed folder are not,
  unless the side file has a files section, when an undeclared tracked file
  outside the governed folders is reported; an undeclared document is
  reported.
  Disproved if: An undeclared code file, test or document passes without a
  report, a tracked file declared nowhere passes when the side file has a
  files section, or a declared, legacy or (without a files section)
  ungoverned file is reported.
SC-DEC-Q36: A document, another file or a rubric declared in `lockstep.yaml`
  is read and checked; one declared nowhere is reported.
  Disproved if: A declaration in the side file is ignored, or an undeclared
  document passes.
SC-DEC-Q48: With a files section in the side file, a tracked file declared
  by neither the plan nor the side file is reported.
  Disproved if: A tracked file declared nowhere passes.
Proven by: VS-1.1-a (tests/test_unplanned_files.py)
Proven by: VS-1.1-b (tests/test_unplanned_documents.py)
Proven by: VS-1.1-c (tests/test_unplanned_other_files.py)
Proven by: VS-DEC-Q36-a (tests/test_unplanned_documents.py)
Proven by: VS-DEC-Q36-b (tests/test_unplanned_other_files.py)
Proven by: VS-DEC-Q48-a (tests/test_unplanned_other_files.py)
[[[end]]] (sum: NS6yFCr9gj)
"""

import subprocess

import yaml

from lockstep_support import REPO  # noqa: F401
from lockstep.side_file import load_side_file, side_file_problems
from lockstep.unplanned_files import declared_file, document_report, main, unplanned_reason


def _side(proj, files=None, documents=()):
    data = {"schema": "lockstep.side.v1",
            "documents": {"include": ["*.md"],
                          "declared": [{"path": p, "purpose": "why", "refs": ["NI-001"]} for p in documents]}}
    if files is not None:
        data["files"] = [{"path": p, "purpose": "why it exists", "refs": ["NI-001"]} for p in files]
    (proj / "lockstep.yaml").write_text(yaml.safe_dump(data, sort_keys=False))


def _write(proj, *names):
    for name in names:
        (proj / name).parent.mkdir(parents=True, exist_ok=True)
        (proj / name).write_text("x\n")
    subprocess.run(["git", "-C", str(proj), "add", "-A"], check=True)


def test_without_files_section_other_files_pass(proj):
    _side(proj)
    _write(proj, "scripts/tool.py")
    assert load_side_file(proj).whole_repo is False
    assert unplanned_reason(proj, "scripts/tool.py") is None


def test_with_files_section_an_undeclared_file_is_reported(proj, capsys):
    _side(proj, files=["scripts/*.py", "Makefile", "lockstep.yaml", ".aes/*", ".gitignore", "pyproject.toml"])
    _write(proj, "scripts/tool.py", "data/rows.csv")
    side = load_side_file(proj)
    assert side.whole_repo and declared_file(side, "scripts/tool.py") == "scripts/*.py"
    assert unplanned_reason(proj, "scripts/tool.py") is None
    reason = unplanned_reason(proj, "data/rows.csv")
    assert reason and "is not declared" in reason and "under files in lockstep.yaml" in reason
    r = document_report(proj)
    assert any(line.startswith("data/rows.csv is not declared") for line in r["undeclared_files"])
    assert "scripts/tool.py" in r["files"]
    assert main(["--root", str(proj)]) == 1
    assert "undeclared_files=" in capsys.readouterr().out


def test_a_glob_that_matches_nothing_is_reported(proj):
    _side(proj, files=["nowhere/*.py"])
    assert "nowhere/*.py" in document_report(proj)["unused_globs"]


def test_governed_code_and_documents_keep_their_own_rules(proj):
    _side(proj, files=["*"])
    reason = unplanned_reason(proj, "src/greeter/extra.py")
    assert reason and ".aes/target.yaml does not name it" in reason
    reason = unplanned_reason(proj, "NOTES.md")
    assert reason and "documents.declared" in reason


def test_bad_files_entries_are_named(proj):
    (proj / "lockstep.yaml").write_text(yaml.safe_dump({
        "schema": "lockstep.side.v1",
        "files": [{"path": "a", "purpose": "", "refs": ["REQ-404"], "owner": "me"}, {"path": "a", "purpose": "p", "refs": []}]}))
    problems = " | ".join(side_file_problems(proj, {"outcomes": [{"id": "NI-001"}]}))
    for words in ["unknown key 'owner'", "no purpose", "REQ-404", "declared twice", "names no plan item"]:
        assert words in problems
