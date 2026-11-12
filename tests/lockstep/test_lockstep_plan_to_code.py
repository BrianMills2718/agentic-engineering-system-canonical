"""Behavior 5.3: a missing planned file, a missing export and a changed signature are each reported."""

import yaml

from lockstep_support import sh
from lockstep.plan_to_code import plan_drift

SRC = "src/greeter/__init__.py"


def _declare_exports(proj, exports):
    path = proj / ".aes/target.yaml"
    t = yaml.safe_load(path.read_text())
    for a in t["planned_artifacts"]:
        if a["id"] == "ART-GREET":
            a["exports"] = exports
    path.write_text(yaml.safe_dump(t, sort_keys=False))


def test_code_matching_the_plan_reports_nothing(proj):
    _declare_exports(proj, ["greet(name: str) -> str"])
    sh("git add -A && git commit -q -m exports", proj)
    drift = plan_drift(proj)
    assert drift.failing == [] and not drift.dirty


def test_removed_export_and_changed_signature_are_both_reported(proj):
    _declare_exports(proj, ["greet(name: str) -> str", "GREETING"])
    src = proj / SRC
    src.write_text(src.read_text().replace("def greet(name: str) -> str:", "def greet(name: str, loud: bool) -> str:"))
    sh("git add -A && git commit -q -m drift", proj)
    failing = plan_drift(proj).failing
    assert len(failing) == 2, failing
    assert any(f.startswith("signature_changed: src/greeter/__init__.py (ART-GREET)") and "(name: str, loud: bool) -> str" in f
               for f in failing), failing
    assert any(f.startswith("missing_export: src/greeter/__init__.py (ART-GREET)") and "'GREETING'" in f
               for f in failing), failing


def test_missing_planned_file_is_reported(proj):
    _declare_exports(proj, ["greet(name: str) -> str"])
    sh(f"git rm -q {SRC} && git add -A && git commit -q -m gone", proj)
    assert plan_drift(proj).failing == [
        "missing_file: src/greeter/__init__.py (ART-GREET) - file with 1 committed export(s) is absent"]


def test_uncommitted_edit_is_flagged_as_not_yet_seen(proj):
    _declare_exports(proj, ["greet(name: str) -> str"])
    sh("git add -A && git commit -q -m exports", proj)
    (proj / SRC).write_text((proj / SRC).read_text().replace("def greet(", "def hello("))
    drift = plan_drift(proj)
    assert drift.dirty and drift.failing == []  # facts are of HEAD until the edit is committed
