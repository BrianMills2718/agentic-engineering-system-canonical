"""Tests for scripts/operator_notification_record.py (Plan #269 Step 1).

Each test pins a specific observed failure rather than describing an assertion.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


record = _load("operator_notification_record_under_test", "scripts/operator_notification_record.py")


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_record_keeps_a_body_longer_than_the_dialog_can_show(tmp_path: Path) -> None:
    """Keep the full body even when a route cannot show it.

    msg.exe truncates at roughly 240 characters and the daily-audit body is 249, so on 2026-09-08 Brian was shown a clipped message
    that existed nowhere else and could only be screenshotted. Truncation is a
    display property of one route and must never reach the record.
    """
    body = "A" * 2000
    entry = record.append(
        key="daily-audit", title="Audit red", body=body, source="test", record_dir=tmp_path
    )

    assert body in entry.render()
    assert body in record.latest_path(tmp_path).read_text(encoding="utf-8")
    assert body in record.read_all(tmp_path)[0].body


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_a_notification_is_recorded_before_delivery_is_attempted(tmp_path: Path) -> None:
    """Append-first is the contract. A crash, rate limit, or dead transport.

    between append and delivery must still leave a readable entry.
    """
    entry = record.append(key="k", title="t", body="b", record_dir=tmp_path)

    assert entry.delivered is None, "unknown must be distinguishable from failed"
    stored = record.read_all(tmp_path)
    assert len(stored) == 1 and stored[0].delivered is None
    assert record.undelivered(tmp_path), "not-yet-delivered counts as outstanding"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_transport_failure_is_recorded_with_its_reason(tmp_path: Path) -> None:
    """WSL interop was down on 2026-09-08 (UtilAcceptVsock: accept4 failed 110).

    Every route fails in that state, and before this module nothing recorded
    that the operator was never reached.
    """
    entry = record.append(key="daily-audit", title="Audit red", body="b", record_dir=tmp_path)
    record.mark_outcome(
        entry,
        delivered=False,
        route="toast",
        failure_reason="UtilAcceptVsock: accept4 failed 110",
        record_dir=tmp_path,
    )

    outstanding = record.undelivered(tmp_path)
    assert len(outstanding) == 1
    assert outstanding[0].failure_reason and "accept4" in outstanding[0].failure_reason
    assert "NOT DELIVERED" in outstanding[0].render()


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_an_undelivered_notification_cannot_be_recorded_without_a_reason(tmp_path: Path) -> None:
    """Silence is the failure mode. A route that fails without saying why is.

    indistinguishable from one that was never tried.
    """
    entry = record.append(key="k", title="t", body="b", record_dir=tmp_path)

    with pytest.raises(record.NotificationRecordError) as excinfo:
        record.mark_outcome(entry, delivered=False, route="toast", record_dir=tmp_path)

    assert "reason" in str(excinfo.value)


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_a_later_success_supersedes_an_earlier_failure(tmp_path: Path) -> None:
    """A retried notification must stop appearing as outstanding, without the.

    record losing the failed attempt.
    """
    entry = record.append(key="k", title="t", body="b", record_dir=tmp_path)
    record.mark_outcome(
        entry, delivered=False, route="toast", failure_reason="interop down", record_dir=tmp_path
    )
    record.mark_outcome(entry, delivered=True, route="modal", record_dir=tmp_path)

    assert record.undelivered(tmp_path) == []
    assert len(record.read_all(tmp_path)) == 3, "the failed attempt stays in the record"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_one_corrupt_line_does_not_hide_the_rest(tmp_path: Path) -> None:
    """Losing one notification to a bad write is recoverable; losing every later.

    one because the reader raised is not.
    """
    record.append(key="first", title="t", body="b", record_dir=tmp_path)
    with record.record_path(tmp_path).open("a", encoding="utf-8") as handle:
        handle.write("{not json\n")
    record.append(key="second", title="t", body="b", record_dir=tmp_path)

    keys = [e.key for e in record.read_all(tmp_path)]
    assert keys == ["first", "second"]


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_an_unsupported_severity_fails_loudly(tmp_path: Path) -> None:
    with pytest.raises(record.NotificationRecordError):
        record.append(
            key="k", title="t", body="b", severity="catastrophic", record_dir=tmp_path
        )


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_the_record_is_machine_readable(tmp_path: Path) -> None:
    """escalation_inbox.py consumes this as a source, so each line must parse."""
    now = datetime(2026, 9, 8, 23, 0, tzinfo=timezone.utc)
    record.append(key="k", title="t", body="b", record_dir=tmp_path, now=now)

    line = record.record_path(tmp_path).read_text(encoding="utf-8").strip()
    payload = json.loads(line)
    assert payload["recorded_at"] == now.isoformat()
    assert payload["severity"] == "attention"
    assert payload["delivered"] is None


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_notify_operator_cli_can_redirect_the_shared_record(tmp_path, monkeypatch) -> None:
    """Keep tests out of the operator's real record.

    Wiring notify_operator to the shared record made the existing CLI tests append to the operator's REAL record at
    ~/.local/state/operator-notify, putting four entries with key 'k' and body
    'b' into live state. A record the tests write into is not a record.
    """
    notify = _load("notify_operator_record_wiring", "scripts/notify_operator.py")
    sys.path.insert(0, str(ROOT / "scripts"))
    import operator_notify_router as router

    monkeypatch.setattr(router, "deliver_concern", lambda **k: router.DeliveryResult(
        route="concern", delivered=True, evidence="filed"))

    record_dir = tmp_path / "record"
    default_before = record.read_all(None)

    exit_code = notify.main(
        [
            "--title", "Audit red", "--body", "B" * 500, "--key", "redirect-probe",
            "--stamp-dir", str(tmp_path / "stamp"),
            "--record-dir", str(record_dir),
        ]
    )

    assert exit_code == 0
    redirected = record.read_all(record_dir)
    assert [e.key for e in redirected] == ["redirect-probe", "redirect-probe"]
    assert redirected[-1].delivered is True
    assert "B" * 500 in redirected[0].body, "the record keeps the untruncated body"
    assert record.read_all(None) == default_before, "the real record must be untouched"
