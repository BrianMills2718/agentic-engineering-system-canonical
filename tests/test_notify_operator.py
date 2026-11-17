"""Tests for scripts/notify_operator.py; moved with it from project-meta on 2026-11-17 (its audit-escalation tests stayed there).

Each test is pinned to a specific way this could fail quietly, because the
whole point of the script is that a quiet notification channel already failed
once (the daily audit sat red for 25 days behind a log and an unread inbox).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, relative: str):
    """Load a standalone script as a module, registered before execution."""
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


sys.path.insert(0, str(ROOT / "scripts"))
notify = _load("notify_operator_under_test", "scripts/notify_operator.py")

NOW = datetime(2026, 9, 8, 12, 0, tzinfo=timezone.utc)


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_first_notification_is_always_allowed(tmp_path: Path) -> None:
    """A condition nobody has been told about must never be rate-limited away."""
    allowed, reason = notify.due(tmp_path, "daily-audit", 12.0, NOW)
    assert allowed is True
    assert reason == "never sent"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_repeat_inside_the_interval_is_suppressed(tmp_path: Path) -> None:
    """msg.exe steals focus; an unthrottled caller trains the operator to dismiss it."""
    notify.record_sent(tmp_path, "daily-audit", NOW - timedelta(hours=3))
    allowed, reason = notify.due(tmp_path, "daily-audit", 12.0, NOW)
    assert allowed is False
    assert "next in" in reason


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_repeat_after_the_interval_is_allowed(tmp_path: Path) -> None:
    """Suppression must expire, or one early failure mutes the channel forever."""
    notify.record_sent(tmp_path, "daily-audit", NOW - timedelta(hours=13))
    allowed, _ = notify.due(tmp_path, "daily-audit", 12.0, NOW)
    assert allowed is True


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_corrupt_stamp_does_not_suppress(tmp_path: Path) -> None:
    """A damaged stamp file must fail toward reaching the operator, not away.

    The dangerous direction here is silence: an unreadable stamp that read as
    'sent recently' would mute a real failure with no trace.
    """
    stamp = tmp_path / "daily-audit.json"
    stamp.write_text("{not json", encoding="utf-8")
    assert notify.last_sent(tmp_path, "daily-audit") is None
    allowed, _ = notify.due(tmp_path, "daily-audit", 12.0, NOW)
    assert allowed is True


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_zero_interval_disables_rate_limiting(tmp_path: Path) -> None:
    """--min-interval-hours 0 is the documented way to force a send when testing."""
    notify.record_sent(tmp_path, "daily-audit", NOW)
    allowed, reason = notify.due(tmp_path, "daily-audit", 0, NOW)
    assert allowed is True
    assert reason == "no interval configured"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_key_separates_rate_limit_buckets(tmp_path: Path) -> None:
    """One noisy condition must not silence an unrelated one."""
    notify.record_sent(tmp_path, "daily-audit", NOW)
    allowed, _ = notify.due(tmp_path, "some-other-condition", 12.0, NOW)
    assert allowed is True


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_key_is_filesystem_sanitised(tmp_path: Path) -> None:
    """A key with a slash must not escape the stamp directory."""
    notify.record_sent(tmp_path, "../escape/attempt", NOW)
    written = list(tmp_path.iterdir())
    assert len(written) == 1
    assert written[0].parent == tmp_path


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_stamp_roundtrip_records_the_time(tmp_path: Path) -> None:
    """Suppression is only correct if the recorded timestamp is read back exactly."""
    notify.record_sent(tmp_path, "daily-audit", NOW)
    raw = json.loads((tmp_path / "daily-audit.json").read_text(encoding="utf-8"))
    assert raw["key"] == "daily-audit"
    assert notify.last_sent(tmp_path, "daily-audit") == NOW


sys.path.insert(0, str(ROOT / "scripts"))
import operator_notify_router as router_mod  # noqa: E402  (the module notify.main imports)


@pytest.fixture()
def routes(monkeypatch):
    """Fake every transport; record which ones the CLI reached."""
    calls: list[str] = []
    state = {"telegram_ok": True}

    def _tg(title, body, **_k):
        calls.append("telegram")
        return router_mod.DeliveryResult(
            route="telegram", delivered=state["telegram_ok"],
            evidence="accepted_by_telegram" if state["telegram_ok"] else "send_failed",
            detail="message_id 1" if state["telegram_ok"] else "down",
        )

    def _concern(**_k):
        calls.append("concern")
        return router_mod.DeliveryResult(route="concern", delivered=True, evidence="filed")

    def _ntfy(*_a, **_k):
        raise AssertionError("notify_operator must never reach the phone push")

    def _toast(*_a, **_k):
        calls.append("toast")
        return router_mod.DeliveryResult(route="toast", delivered=True, evidence="observed_arrival")

    monkeypatch.setattr(router_mod, "deliver_toast", _toast)
    monkeypatch.setattr(router_mod, "deliver_telegram", _tg)
    monkeypatch.setattr(router_mod, "deliver_concern", _concern)
    monkeypatch.setattr(router_mod, "deliver_ntfy", _ntfy)
    return calls, state


def _cli(tmp_path: Path, *extra: str) -> int:
    return notify.main([
        "--title", "t", "--body", "b", "--key", "k",
        "--stamp-dir", str(tmp_path / "stamps"), "--record-dir", str(tmp_path / "record"),
        *extra,
    ])


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_the_desk_dialog_is_gone() -> None:
    """Issue #1958: no msg.exe send path survives in this module."""
    assert not hasattr(notify, "send")
    assert not hasattr(notify, "MSG_EXE_CANDIDATES")


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_cli_dry_run_does_not_deliver(tmp_path: Path, routes) -> None:
    calls, _ = routes
    assert _cli(tmp_path, "--dry-run") == 0
    assert calls == []
    assert not (tmp_path / "stamps" / "k.json").exists()


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_cli_default_is_agent_work_not_an_interruption(tmp_path: Path, routes) -> None:
    calls, _ = routes
    assert _cli(tmp_path) == 0
    assert calls == ["concern"], "an agent gets it; Brian is not messaged"
    history = (tmp_path / "stamps" / "history.log").read_text(encoding="utf-8")
    assert "b" in history


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_cli_needs_human_messages_once_per_state(tmp_path: Path, routes) -> None:
    calls, _ = routes
    act = ("--action", "Say: finish Google access setup")
    assert _cli(tmp_path, "--needs-human", "--state", "token-missing", *act) == 0
    assert _cli(tmp_path, "--needs-human", "--state", "token-missing", *act) == 0
    assert calls == ["toast", "telegram", "concern"], "the same condition is not re-sent daily"
    assert _cli(tmp_path, "--needs-human", "--state", "client-missing", *act) == 0
    assert calls == ["toast", "telegram", "concern"] * 2


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_cli_refuses_jargon_in_what_brian_sees(tmp_path: Path, routes) -> None:
    calls, _ = routes
    code = notify.main([
        "--title", "FileNotFoundError: ~/.secrets/x.json", "--action", "fix", "--body", "b",
        "--key", "k", "--needs-human", "--stamp-dir", str(tmp_path / "s"),
        "--record-dir", str(tmp_path / "r"),
    ])
    assert code == 2 and calls == []


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_cli_needs_human_failure_exits_non_zero_and_does_not_stamp(tmp_path: Path, routes) -> None:
    calls, state = routes
    state["telegram_ok"] = False
    assert _cli(tmp_path, "--severity", "needs-human", "--state", "s", "--action", "do it") == 1
    assert notify.last_state(tmp_path / "stamps", "k") is None
    assert _cli(tmp_path, "--severity", "needs-human", "--state", "s", "--action", "do it") == 1
    assert calls.count("telegram") == 2, "a failed message to Brian is retried"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_cli_suppressed_send_returns_success(tmp_path: Path, routes) -> None:
    """Being rate-limited is not an error; a non-zero exit would redden the audit."""
    calls, _ = routes
    notify.record_sent(tmp_path / "stamps", "k", datetime.now(timezone.utc))
    assert _cli(tmp_path, "--min-interval-hours", "12") == 0
    assert calls == []


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_state_stamp_roundtrip_and_clear(tmp_path: Path) -> None:
    notify.record_sent(tmp_path, "k", NOW, state="token-missing")
    assert notify.last_state(tmp_path, "k") == "token-missing"
    assert notify.last_sent(tmp_path, "k") == NOW
    notify.clear_sent(tmp_path, "k")
    assert notify.last_state(tmp_path, "k") is None
    notify.clear_sent(tmp_path, "k")  # idempotent


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_transcript_records_the_full_untruncated_message(tmp_path):
    """Keep the whole message in the append-only history."""
    now = notify.datetime.now(notify.timezone.utc)
    body = "B" * 2000
    path = notify.write_transcript(tmp_path, "daily-audit", "Audit red", body, now)

    latest, history = notify.transcript_paths(tmp_path)
    assert path == latest
    written = history.read_text(encoding="utf-8")
    assert body in written, "the history must keep the body untruncated"
    assert "Audit red" in written
    assert "daily-audit" in written


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_transcript_history_appends_rather_than_replacing(tmp_path):
    now = notify.datetime.now(notify.timezone.utc)
    notify.write_transcript(tmp_path, "k", "First", "first body", now)
    notify.write_transcript(tmp_path, "k", "Second", "second body", now)

    _latest, history = notify.transcript_paths(tmp_path)
    text = history.read_text(encoding="utf-8")
    assert "first body" in text and "second body" in text
