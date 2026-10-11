"""S6 weekly fix owner: an item counts as handled only from what GitHub shows, never the agent's summary."""
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import fix_owner as FO  # noqa: E402

T = "2026-10-11T20:00:00Z"


def comment(body, at="2026-10-11T20:05:00Z"):
    return {"body": body, "createdAt": at}


def disp(kind, reason="r"):
    return comment(f'{FO.DISPOSITION}{json.dumps({"disposition": kind, "reason": reason})} -->')


RECEIPT = comment('<!-- feedback-enforcement {"enforced_at":"%s","revision":"abc123","verification":"https://x/pr/1"} -->' % T)


def fake(monkeypatch, state, reason, comments):
    monkeypatch.setattr(FO, "gh_json", lambda *a: {"state": state, "stateReason": reason, "comments": comments})


def test_implemented_needs_completed_close_and_a_counted_receipt(monkeypatch):
    fake(monkeypatch, "CLOSED", "COMPLETED", [RECEIPT, disp("implemented")])
    assert FO.check(1)["valid"]
    fake(monkeypatch, "CLOSED", "COMPLETED", [disp("implemented")])  # agent said done, no receipt
    assert not FO.check(1)["valid"]


def test_receipt_dated_after_its_comment_is_not_counted(monkeypatch):
    late = comment(RECEIPT["body"].replace(T, "2026-10-11T21:00:00Z"))
    fake(monkeypatch, "CLOSED", "COMPLETED", [late, disp("implemented")])
    assert not FO.check(1)["valid"]


def test_declined_must_be_closed_not_planned_with_a_reason(monkeypatch):
    fake(monkeypatch, "CLOSED", "NOT_PLANNED", [disp("declined", "duplicate of #406")])
    assert FO.check(1)["valid"]
    fake(monkeypatch, "CLOSED", "COMPLETED", [disp("declined", "dup")])  # closed as done: would read as enforced
    assert not FO.check(1)["valid"]
    fake(monkeypatch, "CLOSED", "NOT_PLANNED", [disp("declined", "")])
    assert not FO.check(1)["valid"]


def test_deferred_stays_open_and_closing_silently_is_invalid(monkeypatch):
    fake(monkeypatch, "OPEN", "", [disp("deferred", "blocked on claim x")])
    assert FO.check(1)["valid"]
    fake(monkeypatch, "CLOSED", "NOT_PLANNED", [])
    assert not FO.check(1)["valid"]


def test_recently_attempted_items_wait_a_week(monkeypatch):
    now = dt.datetime(2026, 10, 18, tzinfo=dt.timezone.utc)
    rows = [{"number": 2, "title": "b", "createdAt": "2026-10-02T00:00:00Z",
             "comments": [comment(f'{FO.ATTEMPT}{{}} -->', "2026-10-15T00:00:00Z")]},
            {"number": 1, "title": "a", "createdAt": "2026-10-01T00:00:00Z",
             "comments": [comment(f'{FO.ATTEMPT}{{}} -->', "2026-10-11T00:00:00Z")]},
            {"number": 3, "title": "c", "createdAt": "2026-10-03T00:00:00Z", "comments": []}]
    monkeypatch.setattr(FO, "gh_json", lambda *a: rows)
    assert [r["number"] for r in FO.candidates(None, now)] == [1, 3]
