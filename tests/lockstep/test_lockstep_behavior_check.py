"""Behavior 7.2: every behavior has exactly one source file of its own and a criterion with a test route."""

import subprocess
import sys

from lockstep_support import ENV, REPO
from lockstep.aes_bridge import target
from lockstep.behavior_check import behavior_problems


def _plan() -> dict:
    """Five behaviors, each broken a different way except BEH-OK, plus a shared helper."""
    beh = lambda i: {"id": i, "kind": "behavior", "statement": i}  # noqa: E731
    src = lambda i, p: {"id": i, "kind": "source", "locator": {"exact_path": p}}  # noqa: E731
    return {
        "normative_items": [beh(b) for b in ["BEH-OK", "BEH-NOFILE", "BEH-SHARE1", "BEH-SHARE2", "BEH-TWO", "BEH-NOROUTE"]],
        "planned_artifacts": [src("A-OK", "src/ok.py"), src("A-SHARED", "src/shared.py"), src("A-T1", "src/t1.py"),
                              src("A-T2", "src/t2.py"), src("A-NR", "src/nr.py"), src("A-HELP", "src/helper.py"),
                              {"id": "T-OK", "kind": "test", "locator": {"exact_path": "tests/test_ok.py"}}],
        "components": [
            {"id": "C-OK", "target_refs": ["BEH-OK"], "planned_artifact_refs": ["A-OK", "T-OK"]},
            {"id": "C-S1", "target_refs": ["BEH-SHARE1"], "planned_artifact_refs": ["A-SHARED"]},
            {"id": "C-S2", "target_refs": ["BEH-SHARE2"], "planned_artifact_refs": ["A-SHARED"]},
            {"id": "C-TWO", "target_refs": ["BEH-TWO"], "planned_artifact_refs": ["A-T1", "A-T2"]},
            {"id": "C-NR", "target_refs": ["BEH-NOROUTE"], "planned_artifact_refs": ["A-NR"]},
            {"id": "C-SHARED", "target_refs": ["REQ-1"], "planned_artifact_refs": ["A-HELP"]},
        ],
        "success_criteria": [{"id": f"SC-{b}", "target_refs": [b]} for b in
                             ["BEH-OK", "BEH-NOFILE", "BEH-SHARE1", "BEH-SHARE2", "BEH-TWO", "BEH-NOROUTE"]],
        "verification_subjects": [{"id": f"VS-{b}", "criterion_refs": [f"SC-{b}"], "locator": "tests/test_ok.py"}
                                  for b in ["BEH-OK", "BEH-NOFILE", "BEH-SHARE1", "BEH-SHARE2", "BEH-TWO"]]
                                 + [{"id": "VS-BEH-NOROUTE", "criterion_refs": ["SC-BEH-NOROUTE"]}],
    }


def test_each_break_is_reported_once_and_nothing_else():
    problems = behavior_problems(_plan())
    assert problems == [
        "BEH-NOFILE has no source file: no component that targets it lists a planned source artifact.",
        "BEH-TWO is spread over 2 source files (src/t1.py, src/t2.py); a behavior has exactly one.",
        "BEH-NOROUTE has no routed criterion: no verification subject with a locator proves SC-BEH-NOROUTE.",
        "src/shared.py holds 2 behaviors (BEH-SHARE1, BEH-SHARE2); each behavior gets a file of its own.",
    ]


def test_a_behavior_with_no_criterion_is_reported():
    plan = _plan()
    plan["success_criteria"] = [sc for sc in plan["success_criteria"] if sc["id"] != "SC-BEH-OK"]
    assert "BEH-OK has no criterion: no success criterion targets it." in behavior_problems(plan)
