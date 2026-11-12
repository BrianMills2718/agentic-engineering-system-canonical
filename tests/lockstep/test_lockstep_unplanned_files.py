"""Behavior 1.1: a file the plan does not declare is reported (code and tests under governed folders)."""

import json

from lockstep.unplanned_files import unplanned_reason


def test_undeclared_governed_file_is_reported(planned):
    reason = unplanned_reason(planned, "src/greeter/extra.py")
    assert reason and "is not in the plan" in reason and "governed folder src/" in reason


def test_declared_ungoverned_and_legacy_files_are_not(proj):
    assert unplanned_reason(proj, "src/greeter/__init__.py") is None
    assert unplanned_reason(proj, "NOTES.md") is None
    (proj / ".aes/legacy_baseline.json").write_text(json.dumps({"files": {"src/greeter/old.py": "0" * 40}}))
    assert unplanned_reason(proj, "src/greeter/old.py") is None
