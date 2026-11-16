"""Tests for scripts/concern_issue.py (ADR-2026-09-14 concern register adapter); moved with it from project-meta on 2026-11-07."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import concern_issue as ci  # noqa: E402


class FakeGh:
    """Records gh calls; answers `issue list` from a canned issue set."""

    def __init__(self, issues: list[dict] | None = None, fail_on: str | None = None):
        self.issues = issues or []
        self.calls: list[list[str]] = []
        self.fail_on = fail_on

    def __call__(self, args):
        args = list(args)
        self.calls.append(args)
        if self.fail_on and args[:2] == self.fail_on.split():
            raise RuntimeError("gh failed")
        if args[:2] == ["issue", "list"]:
            return json.dumps(self.issues)
        if args[:2] == ["issue", "create"]:
            return "https://github.com/o/r/issues/9\n"
        return ""

    def verbs(self):
        return [c[:2] for c in self.calls if c[0] == "issue"]


def issue(number, state, key="daily-audit", title="T"):
    return {"number": number, "state": state, "title": title, "body": f"text\n{ci.marker(key)}\n"}


def test_open_creates_when_no_issue_exists():
    gh = FakeGh()
    assert ci.open_concern("o/r", "daily-audit", "T", "B", "daily-audit", gh) == (
        "created https://github.com/o/r/issues/9"
    )
    create = next(c for c in gh.calls if c[:2] == ["issue", "create"])
    assert ci.marker("daily-audit") in create[create.index("--body") + 1]
    assert "concern:feedback,source:daily-audit" in create


def test_open_comments_on_existing_open_issue_instead_of_duplicating():
    gh = FakeGh([issue(4, "OPEN")])
    assert ci.open_concern("o/r", "daily-audit", "T", "B", "daily-audit", gh) == "commented #4"
    assert ["issue", "create"] not in gh.verbs()


def test_open_reopens_closed_issue_on_recurrence():
    gh = FakeGh([issue(4, "CLOSED")])
    assert ci.open_concern("o/r", "daily-audit", "T", "B", "daily-audit", gh) == "reopened #4"
    assert ["issue", "reopen"] in gh.verbs()


def test_fuzzy_search_hit_without_exact_marker_is_not_the_same_concern():
    gh = FakeGh([issue(4, "OPEN", key="daily-audit-extra")])
    assert ci.open_concern("o/r", "daily-audit", "T", "B", "daily-audit", gh).startswith("created")


def test_close_closes_open_issue_with_evidence():
    gh = FakeGh([issue(4, "OPEN")])
    assert ci.close_concern("o/r", "daily-audit", "green run", gh) == "closed #4"
    assert gh.verbs()[-2:] == [["issue", "comment"], ["issue", "close"]]


def test_close_is_noop_when_nothing_open():
    gh = FakeGh([issue(4, "CLOSED")])
    assert ci.close_concern("o/r", "daily-audit", "green", gh) == "no open concern"
    assert ["issue", "close"] not in gh.verbs()


def test_gh_failure_is_loud():
    gh = FakeGh(fail_on="issue create")
    with pytest.raises(RuntimeError):
        ci.open_concern("o/r", "k", "T", "B", "s", gh)


def test_local_env_drops_github_token_but_actions_keeps_it(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "x")
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert "GITHUB_TOKEN" not in ci._child_env()
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    assert ci._child_env()["GITHUB_TOKEN"] == "x"


def test_open_with_recorded_occurrence_is_left_unchanged():
    """A daily re-run on unchanged evidence must not comment every cycle."""

    class ViewGh(FakeGh):
        def __call__(self, args):
            if list(args)[:2] == ["issue", "view"]:
                self.calls.append(list(args))
                return json.dumps({"body": "x", "comments": [{"body": ci.occurrence_marker("count-5")}]})
            return super().__call__(args)

    gh = ViewGh([issue(4, "OPEN")])
    assert ci.open_concern("o/r", "daily-audit", "T", "B", "s", gh, occurrence="count-5") == "unchanged #4"
    assert ["issue", "comment"] not in gh.verbs()
    assert ci.open_concern("o/r", "daily-audit", "T", "B", "s", gh, occurrence="count-6") == "commented #4"


@pytest.mark.req("compliance-list/an-open-concern-s-title-follows-the-repository-s-current-status")
def test_open_retitles_an_open_issue_whose_status_changed():
    """The seven 'Planning package error' issues of #93: the status moved to out of date, the title did not."""
    gh = FakeGh([issue(4, "OPEN", key="planning-compliance", title="Planning package error")])
    result = ci.open_concern("o/r", "planning-compliance", "Planning package out of date", "B", "compliance-list", gh)
    assert result == "commented #4, retitled"
    assert ["issue", "create"] not in gh.verbs(), "one issue per repository, not one per status"
    edit = next(c for c in gh.calls if c[:2] == ["issue", "edit"])
    assert edit[2] == "4" and edit[edit.index("--title") + 1] == "Planning package out of date"
    assert "-R" in edit and edit[edit.index("-R") + 1] == "o/r"


@pytest.mark.req("compliance-list/a-current-title-is-left-alone", existing=True)   # the guard against over-editing: old code never edited
def test_open_leaves_a_current_title_alone():
    gh = FakeGh([issue(4, "OPEN", key="planning-compliance", title="Planning package out of date")])
    result = ci.open_concern("o/r", "planning-compliance", "Planning package out of date", "B", "s", gh)
    assert result == "commented #4"
    assert ["issue", "edit"] not in gh.verbs()


@pytest.mark.req("compliance-list/a-reopened-concern-takes-the-current-title")
def test_open_retitles_a_reopened_issue():
    gh = FakeGh([issue(4, "CLOSED", key="planning-compliance", title="Planning package error")])
    result = ci.open_concern("o/r", "planning-compliance", "Planning package not compliant", "B", "s", gh)
    assert result == "reopened #4, retitled"
    assert ["issue", "edit"] in gh.verbs()


@pytest.mark.req("compliance-list/an-issue-that-already-records-the-occurrence-is-still-retitled")
def test_open_retitles_even_when_the_occurrence_is_already_recorded():
    """An issue that was commented before this fix still holds the old title; the re-run must fix it."""

    class ViewGh(FakeGh):
        def __call__(self, args):
            if list(args)[:2] == ["issue", "view"]:
                self.calls.append(list(args))
                return json.dumps({"body": "x", "comments": [{"body": ci.occurrence_marker("out of date: x")}]})
            return super().__call__(args)

    gh = ViewGh([issue(4, "OPEN", key="planning-compliance", title="Planning package error")])
    result = ci.open_concern("o/r", "planning-compliance", "Planning package out of date", "B", "s", gh,
                             occurrence="out of date: x")
    assert result == "unchanged #4, retitled"
    assert ["issue", "comment"] not in gh.verbs()


@pytest.mark.req("compliance-list/a-failed-retitle-fails-the-call")
def test_a_failed_retitle_is_loud():
    gh = FakeGh([issue(4, "OPEN", title="old")], fail_on="issue edit")
    with pytest.raises(RuntimeError):
        ci.open_concern("o/r", "daily-audit", "new", "B", "s", gh)


def test_trace_review_line_is_appended_after_validation(monkeypatch):
    monkeypatch.setattr(ci, "check_trace_review", lambda p: "/repo/review.json")
    gh = FakeGh()
    assert ci.main(["open", "--repo", "o/r", "--key", "k", "--title", "t", "--body", "diagnosis",
                    "--source", "s", "--trace-review", "review.json"], run=gh) == 0
    body = next(c for c in gh.calls if c[:2] == ["issue", "create"])
    assert "diagnosis\n\nTrace-Review: /repo/review.json" in body[body.index("--body") + 1]


def test_no_run_claim_needs_a_reason_and_excludes_a_review():
    assert ci.trace_review_lines([], "no run discussed here") == "Trace-Review: none (no run discussed here)"
    with pytest.raises(SystemExit):
        ci.trace_review_lines([], "short")
    with pytest.raises(SystemExit):
        ci.trace_review_lines(["r.json"], "no run discussed here", check=lambda p: p)


def test_invalid_trace_review_files_nothing(tmp_path):
    gh = FakeGh()
    with pytest.raises(SystemExit):
        ci.main(["open", "--repo", "o/r", "--key", "k", "--title", "t", "--body", "b",
                 "--source", "s", "--trace-review", str(tmp_path / "missing.json")], run=gh)
    assert gh.calls == []


def test_without_flags_automated_callers_still_file():
    gh = FakeGh()
    assert ci.main(["open", "--repo", "o/r", "--key", "k", "--title", "t", "--body", "b", "--source", "s"], run=gh) == 0
    assert any(c[:2] == ["issue", "create"] for c in gh.calls)


def test_create_that_returns_no_issue_url_is_loud():
    """2026-10-13: under GitHub's secondary rate limit gh 2.102.0 `issue create` exited 0 with empty output,
    and open_concern printed "created " -- a concern reported as filed that did not exist."""
    class SilentGh(FakeGh):
        def __call__(self, args):
            out = super().__call__(args)
            return "" if list(args)[:2] == ["issue", "create"] else out
    with pytest.raises(RuntimeError, match="no issue URL"):
        ci.open_concern("o/r", "k", "T", "B", "s", SilentGh())
