"""Behavior 1.1 (documents): a document Lockstep's side file does not declare is reported."""

import yaml

from lockstep_support import REPO
from lockstep.side_file import load_side_file, side_file_problems
from lockstep.unplanned_files import document_report, main, unplanned_reason


def _side(proj, data):
    (proj / "lockstep.yaml").write_text(yaml.safe_dump(data, sort_keys=False))


def _declared(*paths, refs=("NI-001",)):
    return {"schema": "lockstep.side.v1",
            "documents": {"include": ["*.md"],
                          "declared": [{"path": p, "purpose": "why it exists", "refs": list(refs)} for p in paths]}}


def test_no_side_file_means_no_document_rule(proj):
    (proj / "NOTES.md").write_text("notes\n")
    assert load_side_file(proj) is None
    assert unplanned_reason(proj, "NOTES.md") is None
    assert document_report(proj)["side_file"] is False


def test_undeclared_document_is_reported_and_declared_one_is_not(proj):
    _side(proj, _declared("README.md"))
    for name in ["README.md", "NOTES.md", "docs/guide.md"]:
        (proj / name).parent.mkdir(parents=True, exist_ok=True)
        (proj / name).write_text("text\n")
    assert unplanned_reason(proj, "README.md") is None
    reason = unplanned_reason(proj, "docs/guide.md")
    assert reason and "is not in the plan" in reason and "matches *.md in lockstep.yaml" in reason
    assert "documents.declared" in reason
    assert unplanned_reason(proj, "Makefile") is None  # not a document, not governed
    r = document_report(proj)
    assert r["declared"] == ["README.md"] and len(r["undeclared"]) == 2 and r["problems"] == []
    assert main(["--root", str(proj)]) == 1


def test_declared_but_unwritten_document_is_listed_not_failing(proj, capsys):
    _side(proj, _declared("docs/later.md"))
    r = document_report(proj)
    assert r["unbuilt"] == ["docs/later.md"] and r["undeclared"] == []
    assert main(["--root", str(proj)]) == 0
    assert "undeclared=0 unbuilt=1 problems=0" in capsys.readouterr().out


def test_governed_code_still_goes_through_the_plan(proj):
    _side(proj, _declared())
    reason = unplanned_reason(proj, "src/greeter/extra.py")
    assert reason and ".aes/target.yaml does not name it" in reason and "aes plan" in reason


def test_side_file_problems_are_named(proj):
    data = _declared("README.md", "README.md", refs=("REQ-404",))
    data["documents"]["declared"].append({"path": "x.md", "purpose": "", "refs": [], "owner": "me"})
    data["rubrics"] = [{"criterion": "SC-001", "rubric": ""}]
    data["extra"] = 1
    _side(proj, data)
    problems = side_file_problems(proj, yaml.safe_load((proj / ".aes/target.yaml").read_text()))
    text = "\n".join(problems)
    for expected in ["unknown key 'extra'", "README.md is declared twice", "REQ-404, which .aes/target.yaml does not hold",
                     "x.md has an unknown key 'owner'", "x.md has no purpose", "x.md names no plan item",
                     "rubric for SC-001 has no rubric text"]:
        assert expected in text, expected
    side = load_side_file(proj)
    assert list(side.documents) == ["README.md"] and side.rubrics == {}  # malformed entries are skipped


def test_unreadable_side_file_fails_closed(proj):
    (proj / "lockstep.yaml").write_text("documents: [unclosed\n")
    assert "cannot be checked against the side file" in unplanned_reason(proj, "NOTES.md")
    assert unplanned_reason(proj, "lockstep.yaml") is None  # the side file itself stays editable
    assert main(["--root", str(proj)]) == 1
