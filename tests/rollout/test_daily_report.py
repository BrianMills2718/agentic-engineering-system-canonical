"""The daily commit-rule report reads the rule's quick-plan notes (plan commit-rule-notes-report, AES #279)."""

from __future__ import annotations

import datetime as dt
import importlib.util
from pathlib import Path

REPORT = Path(__file__).resolve().parents[2] / "proposals" / "aes-planning" / "rollout" / "daily_report.py"
_spec = importlib.util.spec_from_file_location("daily_report", REPORT)
assert _spec and _spec.loader
daily_report = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(daily_report)

CLEAN = {"tag": "Goal fix-label", "subject": "[Goal fix-label] fix the typo", "verdict": "accept",
         "notes": ["quick plan fix-label: saved check output docs/plans/fix-label.check.txt present",
                   "quick plan fix-label: every changed file is in the plan's list"]}
MISSING = {"tag": "Goal fix-label", "subject": "[Goal fix-label] second pass", "verdict": "accept",
           "notes": ["quick plan fix-label: saved check output docs/plans/fix-label.check.txt missing",
                     "quick plan fix-label: every changed file is in the plan's list"]}
OUTSIDE = {"tag": "Goal add-dry-run", "subject": "[Goal add-dry-run] also tidy notes", "verdict": "accept",
           "notes": ["quick plan add-dry-run: saved check output docs/plans/add-dry-run.check.txt present",
                     "quick plan add-dry-run: files outside the plan's list: notes.md"]}
FULL_PLAN = {"tag": "Goal aes-planning", "subject": "[Goal aes-planning] work", "verdict": "accept", "notes": []}
TRIVIAL = {"tag": "Trivial", "subject": "[Trivial] typo", "verdict": "accept"}


def test_clean_notes_and_other_tags_are_not_problems() -> None:
    assert daily_report.quick_plan_problems([("site", CLEAN), ("site", FULL_PLAN), ("site", TRIVIAL)]) == []


def test_missing_check_output_and_files_outside_the_list_are_counted_per_commit() -> None:
    rows = [("site", CLEAN), ("site", MISSING), ("tools", OUTSIDE), ("tools", OUTSIDE)]  # a repeated log line counts once
    problems = daily_report.quick_plan_problems(rows)
    assert [(p["repo"], p["plan"], p["subject"]) for p in problems] == [
        ("site", "fix-label", "[Goal fix-label] second pass"),
        ("tools", "add-dry-run", "[Goal add-dry-run] also tidy notes")]
    assert problems[0]["problems"] == ["quick plan fix-label: saved check output docs/plans/fix-label.check.txt missing"]
    assert problems[1]["problems"] == ["quick plan add-dry-run: files outside the plan's list: notes.md"]


def test_concern_names_each_problem_commit_its_repository_plan_and_note() -> None:
    body = daily_report.quick_plan_concern_body(dt.date(2026, 10, 8),
                                                daily_report.quick_plan_problems([("site", MISSING), ("tools", OUTSIDE)]))
    assert "| site | fix-label | [Goal fix-label] second pass | quick plan fix-label: saved check output" in body
    assert "| tools | add-dry-run | [Goal add-dry-run] also tidy notes | quick plan add-dry-run: files outside the plan's list: notes.md |" in body
    assert "2026-10-08" in body
