"""Behavior 2.2: every test file a criterion names exists, and every test file is named by a criterion."""

import yaml

from lockstep_support import REPO, sh
from lockstep.linked_tests import link_report


def _route(proj, locator):
    path = proj / ".aes/target.yaml"
    t = yaml.safe_load(path.read_text())
    t["verification_subjects"][0]["locator"] = locator
    path.write_text(yaml.safe_dump(t, sort_keys=False))


def test_linked_both_ways_reports_nothing(proj):
    r = link_report(proj)
    assert r.dangling == r.unnamed == r.unbuilt == []


def test_missing_named_test_and_unnamed_test_file_are_both_reported(proj):
    _route(proj, "tests/test_missing.py")
    (proj / "tests/test_extra.py").write_text("def test_x():\n    assert True\n")
    r = link_report(proj)
    assert r.dangling == ["tests/test_missing.py is named by VS-GREET but does not exist, "
                          "and the plan does not declare it."]
    assert r.unnamed == ["tests/test_extra.py is a test file that no criterion's test route names.",
                         "tests/test_greet.py is a test file that no criterion's test route names."]


def test_planned_test_not_written_yet_is_listed_not_failing(proj):
    sh("git rm -q tests/test_greet.py", proj)
    r = link_report(proj)
    assert r.dangling == [] and r.unnamed == []
    assert r.unbuilt == ["tests/test_greet.py is named by VS-GREET and planned, not written yet."]
