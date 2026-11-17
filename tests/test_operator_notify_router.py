"""Tests for scripts/operator_notify_router.py (Plan #269 Step 2); moved with it from project-meta on 2026-11-17.

Each test pins a specific observed failure rather than describing an assertion.
"""

from __future__ import annotations

import importlib.util
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
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


sys.path.insert(0, str(ROOT / "scripts"))
router = _load("operator_notify_router_under_test", "scripts/operator_notify_router.py")


@pytest.fixture(autouse=True)
def _isolate_operator_secrets(monkeypatch, tmp_path):
    """Never let a test resolve Brian's real ntfy topic, Telegram bot, or concern repo."""
    monkeypatch.setenv(router.SECRETS_FILE_ENV, str(tmp_path / "no-secrets.env"))
    for name in (router.NTFY_TOPIC_ENV, router.TELEGRAM_TOKEN_ENV, router.TELEGRAM_CHAT_ENV):
        monkeypatch.delenv(name, raising=False)

    def _no_real_gh(args):
        raise AssertionError(f"a test reached the real concern register: gh {args[:2]}")

    monkeypatch.setattr(router, "CONCERN_RUNNER", _no_real_gh)
    # Nor Brian's real settings (the aes-config graph-config.yaml): each test names its own.
    monkeypatch.setenv("PROJECT_GRAPH", str(tmp_path / "no-config" / "PROJECT_GRAPH.json"))
    monkeypatch.delenv(router.CONCERN_REPO_ENV, raising=False)


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_topic_falls_back_to_the_one_key_in_the_secrets_file(monkeypatch, tmp_path):
    """2026-09-14: scheduled units logged ntfy not_configured although the topic
    existed in the secrets file, because the units never load that file."""
    secrets = tmp_path / "api_keys.env"
    secrets.write_text("GITHUB_TOKEN=unrelated\nexport OPERATOR_NTFY_TOPIC='topic-abc'\n")
    monkeypatch.setenv(router.SECRETS_FILE_ENV, str(secrets))
    assert router.ntfy_topic() == "topic-abc"
    assert router.ntfy_topic("") is None  # an explicit empty topic still means unset
    monkeypatch.setenv(router.NTFY_TOPIC_ENV, "env-wins")
    assert router.ntfy_topic() == "env-wins"
record = _load("record_for_router_tests", "scripts/operator_notification_record.py")


def _store(path: Path, payloads: list[tuple[datetime, str]]) -> Path:
    """Build a minimal stand-in for Windows' notification store."""
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE Notification (ArrivalTime INTEGER, Payload BLOB)")
    epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    for when, text in payloads:
        ticks = int((when - epoch).total_seconds() * 10_000_000)
        conn.execute("INSERT INTO Notification VALUES (?, ?)", (ticks, text.encode()))
    conn.commit()
    conn.close()
    return path


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_absence_from_the_store_is_reported_as_absence_not_as_unknown(tmp_path):
    """Distinguish "Windows says it never arrived" from "could not check".

    The toast route reported success and never delivered: it greps PowerShell's
    output for "sent", which PowerShell prints whether or not Windows displays
    anything, so its own check cannot fail. Measured 2026-09-09 -- 109
    notifications in the store, none of them the toast just sent.
    """
    db = _store(tmp_path / "wpn.db", [(datetime.now(timezone.utc), "<toast>something else</toast>")])

    result = router.verify_toast_arrival(
        "Toast route test", since=datetime.now(timezone.utc) - timedelta(hours=1), db_path=db
    )

    assert result.delivered is False
    assert result.evidence == "observed_absence", "absence is evidence, not ignorance"
    assert "1 notification" in (result.detail or "")


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_presence_in_the_store_is_an_observed_arrival(tmp_path):
    """The toast is gated on evidence, not banned.

    The moment one actually arrives, its own arrival check says so and the route
    can be promoted without anyone re-litigating a docstring.
    """
    db = _store(
        tmp_path / "wpn.db",
        [(datetime.now(timezone.utc), "<toast><text>Toast route test</text></toast>")],
    )

    result = router.verify_toast_arrival(
        "Toast route test", since=datetime.now(timezone.utc) - timedelta(hours=1), db_path=db
    )

    assert result.delivered is True
    assert result.evidence == "observed_arrival"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_an_unreachable_store_is_unverifiable_not_delivered(tmp_path):
    """Not being able to check must never read as success.

    Silence about delivery is the failure this whole plan exists to remove.
    """
    result = router.verify_toast_arrival(
        "x", since=datetime.now(timezone.utc), db_path=tmp_path / "absent.db"
    )

    assert result.delivered is False
    assert result.evidence == "unverifiable"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_a_notification_older_than_the_window_is_not_counted(tmp_path):
    """An arrival must be THIS send's, not a lookalike from hours ago."""
    db = _store(
        tmp_path / "wpn.db",
        [(datetime.now(timezone.utc) - timedelta(hours=5), "<toast>Toast route test</toast>")],
    )

    result = router.verify_toast_arrival(
        "Toast route test", since=datetime.now(timezone.utc) - timedelta(hours=1), db_path=db
    )

    assert result.delivered is False


def _result(route, delivered, evidence, detail=None):
    return router.DeliveryResult(route=route, delivered=delivered, evidence=evidence, detail=detail)


def _forbid(name):
    def _explode(*_a, **_k):
        raise AssertionError(f"{name} must not be called")
    return _explode


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_no_desk_popup_route_exists_anywhere():
    """Issue #1958: the msg.exe dialog was truncated, uncopyable, and handed
    Brian work an agent should do. No severity may route to it again."""
    assert not hasattr(router, "deliver_modal")
    used = {route for routes in router.ROUTES_BY_SEVERITY.values() for route in routes}
    assert used <= {"concern", "telegram", "ntfy", "toast"}  # toast = normal Windows notification
    for script in (ROOT / "scripts").glob("*.py"):
        text = script.read_text(encoding="utf-8")
        assert "MSG_EXE" not in text and "System32/msg.exe" not in text, script.name


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_the_default_goes_to_an_agent_and_never_to_brian(tmp_path, monkeypatch):
    """Brian, 2026-10-06: 'these should go to an autonomous agent to fix unless
    my input is actually needed.' A caller that says nothing is agent work."""
    filed: list[dict] = []
    monkeypatch.setattr(router, "deliver_telegram", _forbid("telegram"))
    monkeypatch.setattr(router, "deliver_ntfy", _forbid("ntfy"))
    monkeypatch.setattr(router, "deliver_concern", lambda **k: (
        filed.append(k), _result("concern", True, "filed", "repo created #1"))[1])

    _, results = router.notify(
        key="k", title="t", body="b", record_dir=tmp_path, stamp_dir=tmp_path / "s",
    )

    assert [r.route for r in results] == ["concern"]
    assert filed[0]["key"] == "k" and filed[0]["waiting_on_brian"] is False
    assert record.read_all(tmp_path)[-1].delivered is True


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_a_failed_route_records_the_reason_and_leaves_it_outstanding(tmp_path, monkeypatch):
    """A concern register that cannot be reached is a failure, recorded with why."""
    monkeypatch.setattr(router, "deliver_concern", lambda **k: _result(
        "concern", False, "send_failed", "gh: network down"))

    router.notify(
        key="k", title="t", body="b", severity="agent", record_dir=tmp_path,
        stamp_dir=tmp_path / "stamps",
    )

    outstanding = record.undelivered(tmp_path)
    assert len(outstanding) == 1
    assert "gh: network down" in (outstanding[0].failure_reason or "")


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_info_severity_records_without_interrupting(tmp_path):
    """`info` reaches no route by design: it is recorded and surfaced at session start."""
    entry, results = router.notify(
        key="k", title="t", body="b", severity="info", record_dir=tmp_path
    )

    assert results == []
    outstanding = record.undelivered(tmp_path)
    assert len(outstanding) == 1, "recorded and surfaced at session start, not delivered"
    assert "no route is attempted" in (outstanding[0].failure_reason or "")


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_an_unsupported_severity_fails_loudly(tmp_path):
    with pytest.raises(router.RouterError):
        router.notify(key="k", title="t", body="b", severity="whenever", record_dir=tmp_path)


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_a_suppressed_repeat_still_records_and_is_not_reported_as_a_failure(tmp_path, monkeypatch):
    """A repeat within the interval is recorded, delivered once, and not 'undelivered'."""
    sent: list[str] = []
    monkeypatch.setattr(router, "deliver_concern", lambda **k: (
        sent.append("concern"), _result("concern", True, "filed"))[1])

    stamps = tmp_path / "stamps"
    for _ in range(3):
        router.notify(
            key="daily-audit", title="t", body="b", severity="agent",
            record_dir=tmp_path, stamp_dir=stamps, min_interval_hours=12.0,
        )

    assert sent == ["concern"], "one delivery, not three"
    assert len(record.read_all(tmp_path)) == 6, "every occurrence is still recorded"
    assert record.undelivered(tmp_path) == [], "a suppressed repeat is not an undelivered notice"
    assert "suppressed" in (record.read_all(tmp_path)[-1].route or "")


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_suppression_never_silences_a_notice_that_was_never_delivered(tmp_path, monkeypatch):
    """Suppression keys off a real delivery, so a failed one suppresses nothing."""
    monkeypatch.setattr(router, "deliver_concern", lambda **k: _result(
        "concern", False, "send_failed", "gh down"))

    stamps = tmp_path / "stamps"
    for _ in range(2):
        _, results = router.notify(
            key="daily-audit", title="t", body="b", severity="agent",
            record_dir=tmp_path, stamp_dir=stamps, min_interval_hours=12.0,
        )
        assert results, "a failed send must not suppress the next attempt"

    assert len(record.undelivered(tmp_path)) == 2, "both attempts stay outstanding"


def _needs_human_fakes(monkeypatch, telegram_ok=True):
    calls: list[tuple[str, dict]] = []

    def _tg(title, body, **_k):
        calls.append(("telegram", {"title": title, "body": body}))
        if telegram_ok:
            return _result("telegram", True, "accepted_by_telegram", "message_id 42")
        return _result("telegram", False, "send_failed", "Telegram returned HTTP 401 Unauthorized")

    def _concern(**k):
        calls.append(("concern", k))
        return _result("concern", True, "filed", "repo created #7")

    def _toast(title, action, details, **_k):
        calls.append(("toast", {"title": title, "action": action, "details": details}))
        return _result("toast", True, "observed_arrival")

    monkeypatch.setattr(router, "deliver_toast", _toast)
    monkeypatch.setattr(router, "deliver_telegram", _tg)
    monkeypatch.setattr(router, "deliver_concern", _concern)
    monkeypatch.setattr(router, "deliver_ntfy", _forbid("ntfy"))
    return calls


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_needs_human_messages_brian_once_per_state_not_every_day(tmp_path, monkeypatch):
    """The google-access popup repeated daily for a week with identical text.
    One message per condition; a new condition is a new message; resolving the
    key lets a later recurrence reach him again."""
    calls = _needs_human_fakes(monkeypatch)
    stamps = tmp_path / "stamps"

    def run(state):
        return router.notify(
            key="google-personal-access", title="Google access needs you",
            action="Say: finish Google access setup", body="steps",
            severity="needs-human", state=state,
            record_dir=tmp_path, stamp_dir=stamps,
        )[1]

    first = run("token-missing")
    assert [r.route for r in first] == ["toast", "telegram", "concern"], "Brian AND the agent queue"
    concern = [k for route, k in calls if route == "concern"][0]
    assert concern["waiting_on_brian"] is True
    assert "Telegram to Brian: sent (message_id 42)" in concern["body"]

    assert run("token-missing") == [], "same unresolved condition: not again"
    assert record.undelivered(tmp_path) == []

    assert [r.route for r in run("token-revoked")] == ["toast", "telegram", "concern"], "new condition"

    closed: list[str] = []
    fake_ci = type("CI", (), {
        "close_concern": staticmethod(lambda repo, key, evidence, run: closed.append(key) or "closed #7"),
        "gh_runner": staticmethod(lambda args: ""),
    })
    monkeypatch.setattr(router, "_concern_issue_module", lambda: fake_ci)
    monkeypatch.setenv(router.CONCERN_REPO_ENV, "o/r")  # no built-in default repository since the move to AES
    assert "closed #7" in router.resolve(key="google-personal-access", evidence="check ok", stamp_dir=stamps)
    assert closed == ["google-personal-access"]
    assert [r.route for r in run("token-revoked")] == ["toast", "telegram", "concern"], "recurrence after a fix"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_needs_human_is_not_delivered_until_telegram_lands(tmp_path, monkeypatch):
    """A concern filed while the message to Brian failed has not told Brian.
    Not stamped, recorded undelivered, exit non-zero, retried next run."""
    calls = _needs_human_fakes(monkeypatch, telegram_ok=False)
    stamps = tmp_path / "stamps"
    for _ in range(2):
        _, results = router.notify(
            key="k", title="t", action="do it", body="b", severity="needs-human", state="s",
            record_dir=tmp_path, stamp_dir=stamps,
        )
        assert router.delivery_landed("needs-human", results) is False
    assert [route for route, _ in calls].count("telegram") == 2, "retried, not suppressed"
    concern = [k for route, k in calls if route == "concern"][0]
    assert "FAILED: Telegram returned HTTP 401" in concern["body"], "the agent learns Brian was not told"
    assert len(record.undelivered(tmp_path)) == 2


def _telegram_env(monkeypatch, tmp_path, token="123:SECRET", chat="999"):
    secrets = tmp_path / "keys.env"
    secrets.write_text(
        f"GITHUB_TOKEN=unrelated\nexport TELEGRAM_AGENTS_BOT_TOKEN='{token}'\nOPERATOR_TELEGRAM_CHAT_ID={chat}\n"
    )
    monkeypatch.setenv(router.SECRETS_FILE_ENV, str(secrets))


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_telegram_sends_full_plain_text_and_trusts_only_ok_with_message_id(monkeypatch, tmp_path):
    import json as _json

    _telegram_env(monkeypatch, tmp_path)
    sent: list[dict] = []

    def fake_urlopen(request, timeout=None):
        sent.append({"url": request.full_url, "payload": _json.loads(request.data)})
        return _FakeResponse(_json.dumps({"ok": True, "result": {"message_id": 500 + len(sent)}}))

    monkeypatch.setattr(router.urllib.request, "urlopen", fake_urlopen)
    body = "Step 1: open https://console.cloud.google.com/\n" + ("x" * 300 + "\n") * 20
    result = router.deliver_telegram("Google access needs you", body)

    assert result.delivered and result.evidence == "accepted_by_telegram"
    assert sent[0]["url"].endswith("/bot123:SECRET/sendMessage")
    assert all("parse_mode" not in s["payload"] for s in sent), "plain text: nothing eaten as markup"
    assert all(s["payload"]["chat_id"] == "999" for s in sent)
    joined = "".join(s["payload"]["text"] for s in sent)
    assert joined == f"Google access needs you\n\n{body}", "never truncated"
    assert len(sent) == 2 and all(len(s["payload"]["text"]) <= 4096 for s in sent)
    assert result.detail == "message_id 501,502"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_telegram_without_a_message_id_is_not_delivered_and_never_leaks_the_token(monkeypatch, tmp_path):
    import json as _json

    _telegram_env(monkeypatch, tmp_path)
    monkeypatch.setattr(router.urllib.request, "urlopen",
                        lambda request, timeout=None: _FakeResponse(_json.dumps({"ok": False, "description": "chat not found"})))
    result = router.deliver_telegram("t", "b")
    assert result.delivered is False and "chat not found" in (result.detail or "")

    def boom(request, timeout=None):
        raise router.urllib.error.URLError(f"failed {request.full_url}")

    monkeypatch.setattr(router.urllib.request, "urlopen", boom)
    result = router.deliver_telegram("t", "b")
    assert result.delivered is False and "SECRET" not in (result.detail or "")


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_telegram_unconfigured_is_not_delivered(monkeypatch, tmp_path):
    _telegram_env(monkeypatch, tmp_path, chat="")
    monkeypatch.delenv(router.TELEGRAM_CHAT_ENV, raising=False)
    result = router.deliver_telegram("t", "b")
    assert result.delivered is False and result.evidence == "not_configured"
    assert router.TELEGRAM_CHAT_ENV in (result.detail or "")


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_the_concern_route_files_a_keyed_issue_labelled_for_brian_when_he_must_act(monkeypatch):
    gh_calls: list[list[str]] = []

    def fake_gh(args):
        gh_calls.append(list(args))
        if args[:2] == ["issue", "list"]:
            return "[]"
        if args[:2] == ["issue", "create"]:
            return "https://github.com/o/r/issues/9\n"
        return ""

    monkeypatch.setattr(router, "CONCERN_RUNNER", fake_gh)
    result = router.deliver_concern(
        key="google-personal-access", title="t", body="b", source="google_access",
        occurrence="google-personal-access:token-missing", waiting_on_brian=True, repo="o/r",
    )
    assert result.delivered and "created" in (result.detail or "")
    create = next(c for c in gh_calls if c[:2] == ["issue", "create"])
    labels = create[create.index("--label") + 1]
    assert "waiting:brian" in labels and "source:google_access" in labels
    assert "<!-- concern-key: google-personal-access -->" in create[create.index("--body") + 1]


class _FakeResponse:
    """Minimal stand-in for urllib's response context manager."""

    def __init__(self, payload: str, status: int = 200):
        self._payload = payload.encode()
        self.status = status

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _ntfy_lines(*messages: str) -> str:
    import json as _json

    return "\n".join(
        _json.dumps({"event": "message", "title": "t", "message": m}) for m in messages
    )


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_the_ntfy_check_asks_for_history_and_not_just_what_arrives_next(monkeypatch):
    """The ntfy poll defaults to `since=none`, so a check without it is always empty.

    Measured 2026-09-09: the first version of this check queried `?poll=1` and
    reported zero messages for a topic that demonstrably held one. A check that
    can only come back empty is the same defect as one that can only come back
    green, which is the defect this whole module exists to prevent.
    """
    seen: list[str] = []

    def _fake_urlopen(url, timeout=None):
        seen.append(url if isinstance(url, str) else url.full_url)
        return _FakeResponse(_ntfy_lines("audit is red"))

    monkeypatch.setattr(router.urllib.request, "urlopen", _fake_urlopen)

    result = router.verify_ntfy_arrival(
        "audit is red",
        since=datetime.now(timezone.utc) - timedelta(minutes=5),
        topic="a-topic",
    )

    assert result.delivered is True
    assert "since=" in seen[0], "without since=, ntfy returns only future messages"
    assert "poll=1" in seen[0]


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_reaching_the_broker_is_not_claimed_as_reaching_the_phone(monkeypatch):
    """A hit in ntfy's store proves the message left here, not that it was shown.

    Whether the phone displayed it depends on the app being installed,
    subscribed, and permitted to alert -- none of which this machine can see.
    Naming it `observed_arrival` would repeat the toast's overclaim.
    """
    monkeypatch.setattr(
        router.urllib.request, "urlopen",
        lambda url, timeout=None: _FakeResponse(_ntfy_lines("audit is red")),
    )

    result = router.verify_ntfy_arrival(
        "audit is red", since=datetime.now(timezone.utc), topic="a-topic"
    )

    assert result.evidence == "observed_at_broker"
    assert result.evidence != "observed_arrival"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_an_unconfigured_topic_is_unverifiable_not_delivered():
    """Before 2026-09-09 no ntfy topic had ever been set, and nothing said so."""
    result = router.verify_ntfy_arrival(
        "x", since=datetime.now(timezone.utc), topic=""
    )

    assert result.delivered is False
    assert result.evidence == "unverifiable"
    assert "OPERATOR_NTFY_TOPIC" in (result.detail or "")


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_a_published_message_absent_from_the_broker_is_not_delivered(monkeypatch):
    """The POST returning 200 is this machine talking about itself."""
    monkeypatch.setattr(
        router.urllib.request, "urlopen",
        lambda url, timeout=None: _FakeResponse(_ntfy_lines("something else")),
    )

    result = router.verify_ntfy_arrival(
        "audit is red", since=datetime.now(timezone.utc), topic="a-topic"
    )

    assert result.delivered is False
    assert result.evidence == "observed_absence"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_attention_and_urgent_are_the_phone_push_only(tmp_path, monkeypatch):
    """The ecosystem-ops notifiers keep their ntfy push; the desk dialog that
    used to precede it is gone."""
    monkeypatch.setattr(router, "deliver_ntfy", lambda *a, **k: _result("ntfy", True, "observed_at_broker"))
    monkeypatch.setattr(router, "deliver_concern", _forbid("concern"))
    monkeypatch.setattr(router, "deliver_telegram", _forbid("telegram"))

    for i, severity in enumerate(("attention", "urgent")):
        _, results = router.notify(
            key=f"k{i}", title="t", body="b", severity=severity, record_dir=tmp_path,
            stamp_dir=tmp_path / f"s{i}",
        )
        assert [r.route for r in results] == ["ntfy"]
    assert record.undelivered(tmp_path) == []


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_the_arrival_check_is_retried_because_publishing_is_not_instant(monkeypatch):
    """Measured 2026-09-09: a real send reported absent, then was found moments later.

    ntfy returns 200 before the message is queryable. Checking once, right
    away, converts that race into a confident "never arrived" -- the mirror of
    the toast's confident "delivered", and just as wrong.
    """
    monkeypatch.setattr(router.time, "sleep", lambda _s: None)
    polls: list[str] = []

    def _fake_urlopen(url, timeout=None):
        if not isinstance(url, str):  # the POST
            polls.append("post")
            return _FakeResponse("", status=200)
        polls.append("poll")
        # Empty on the first poll, present on the second.
        body = "" if polls.count("poll") == 1 else _ntfy_lines("the body")
        return _FakeResponse(body)

    monkeypatch.setattr(router.urllib.request, "urlopen", _fake_urlopen)

    result = router.deliver_ntfy("t", "the body", topic="a-topic")

    assert result.delivered is True
    assert polls.count("poll") == 2, "gave the broker a moment, then asked again"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_a_genuinely_absent_message_still_fails_after_the_retries(monkeypatch):
    """The retry must not become a loop that eventually calls anything delivered."""
    monkeypatch.setattr(router.time, "sleep", lambda _s: None)
    monkeypatch.setattr(
        router.urllib.request, "urlopen",
        lambda url, timeout=None: _FakeResponse(
            "" if isinstance(url, str) else "", status=200
        ),
    )

    result = router.deliver_ntfy("t", "the body", topic="a-topic")

    assert result.delivered is False
    assert result.evidence == "observed_absence"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_the_arrival_window_never_narrows_to_a_few_seconds(monkeypatch):
    """A window of seconds is at the mercy of clock skew against ntfy's clock.

    The match is on message text, so a wide window costs nothing; a narrow one
    is another way for a real delivery to read as absent.
    """
    seen: list[str] = []
    monkeypatch.setattr(
        router.urllib.request, "urlopen",
        lambda url, timeout=None: (seen.append(url), _FakeResponse(_ntfy_lines("x")))[1],
    )

    router.verify_ntfy_arrival(
        "x", since=datetime.now(timezone.utc), topic="a-topic"
    )

    assert f"since={router.MIN_NTFY_WINDOW_SECONDS}s" in seen[0]


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_the_ntfy_headers_a_migrating_caller_already_used_survive_the_move(monkeypatch):
    """Consolidation that silently downgrades its first consumers gets reverted.

    The three ecosystem-ops notifiers each set some of these: a stale scout run
    is not the same urgency as a dead one, and `Markdown: no` is what keeps a
    multi-line body readable on the phone. If moving onto the router lost them,
    the router would be a downgrade for exactly the callers it is meant to
    absorb.
    """
    monkeypatch.setattr(router.time, "sleep", lambda _s: None)
    captured: dict = {}

    def _fake_urlopen(url, timeout=None):
        if not isinstance(url, str):
            captured["headers"] = dict(url.header_items())
            return _FakeResponse("", status=200)
        return _FakeResponse(_ntfy_lines("the body"))

    monkeypatch.setattr(router.urllib.request, "urlopen", _fake_urlopen)

    router.deliver_ntfy(
        "t", "the body", topic="a-topic",
        priority="high", tags="eyes,computer", markdown=False,
    )

    headers = {k.lower(): v for k, v in captured["headers"].items()}
    assert headers["priority"] == "high"
    assert headers["tags"] == "eyes,computer"
    assert headers["markdown"] == "no"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_a_title_outside_latin1_is_sent_rather_than_crashing(monkeypatch):
    """A truncated title ends in "…"; http.client cannot put that in a header."""
    monkeypatch.setattr(router.time, "sleep", lambda _s: None)
    captured: dict = {}

    def _fake_urlopen(url, timeout=None):
        if not isinstance(url, str):
            # Encode the way http.client does, so the old code fails here.
            for value in dict(url.header_items()).values():
                value.encode("latin-1")
            captured["headers"] = dict(url.header_items())
            return _FakeResponse("", status=200)
        return _FakeResponse(_ntfy_lines("the body"))

    monkeypatch.setattr(router.urllib.request, "urlopen", _fake_urlopen)

    router.deliver_ntfy("Decide: keep the lane…", "the body", topic="a-topic")

    title = {k.lower(): v for k, v in captured["headers"].items()}["title"]
    from email.header import decode_header, make_header
    assert str(make_header(decode_header(title))) == "Decide: keep the lane…"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_a_caller_that_sets_nothing_still_gets_a_sane_default(monkeypatch):
    """Optional fields must not become required to send a plain notification."""
    monkeypatch.setattr(router.time, "sleep", lambda _s: None)
    captured: dict = {}

    def _fake_urlopen(url, timeout=None):
        if not isinstance(url, str):
            captured["headers"] = dict(url.header_items())
            return _FakeResponse("", status=200)
        return _FakeResponse(_ntfy_lines("the body"))

    monkeypatch.setattr(router.urllib.request, "urlopen", _fake_urlopen)

    router.deliver_ntfy("t", "the body", topic="a-topic")

    headers = {k.lower(): v for k, v in captured["headers"].items()}
    assert headers["priority"] == "default"
    assert "tags" not in headers
    assert "markdown" not in headers, "markdown defaults on; only 'no' is worth sending"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_notify_forwards_the_headers_to_the_ntfy_route(monkeypatch, tmp_path):
    """The passthrough has to survive the dispatch layer, not just the transport."""
    seen: dict = {}

    def _fake_ntfy(title, body, **kwargs):
        seen.update(kwargs)
        return router.DeliveryResult(route="ntfy", delivered=True, evidence="observed_at_broker")

    monkeypatch.setattr(router, "deliver_ntfy", _fake_ntfy)

    router.notify(
        key="k", title="t", body="b", severity="attention", record_dir=tmp_path,
        stamp_dir=tmp_path / "stamps", priority="high", tags="rotating_light",
        markdown=False,
    )

    assert seen["priority"] == "high"
    assert seen["tags"] == "rotating_light"
    assert seen["markdown"] is False


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_needs_human_wording_is_short_plain_and_free_of_paths(tmp_path, monkeypatch):
    """Brian, 2026-10-06: alerts 'need to be concise and simply understandable.'
    The sender refuses visible text that is long or carries paths/error names."""
    assert router.check_human_wording("Google access needs a sign-in", "Say: finish Google access setup") == []
    bad = [
        ("x" * 81, "do it"),
        ("Token missing at ~/.secrets/google_personal_token.json", "do it"),
        ("FileNotFoundError while checking Google", "do it"),
        ("Google broke", "run google_access.py auth"),
        ("Google broke", "run it with --force"),
        ("Google broke", None),
        ("Google broke\nsecond line", "do it"),
    ]
    for title, action in bad:
        assert router.check_human_wording(title, action), (title, action)
    _needs_human_fakes(monkeypatch)
    with pytest.raises(router.RouterError, match="wording"):
        router.notify(key="k", title="FileNotFoundError", action="fix", body="b",
                      severity="needs-human", record_dir=tmp_path, stamp_dir=tmp_path / "s")
    assert record.read_all(tmp_path) == [], "refused before anything is recorded or sent"


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_needs_human_telegram_leads_with_the_short_alert_then_details(monkeypatch, tmp_path):
    import json as _json

    _telegram_env(monkeypatch, tmp_path)
    texts: list[str] = []

    def fake_urlopen(request, timeout=None):
        texts.append(_json.loads(request.data)["text"])
        return _FakeResponse(_json.dumps({"ok": True, "result": {"message_id": len(texts)}}))

    monkeypatch.setattr(router.urllib.request, "urlopen", fake_urlopen)
    result = router.deliver_telegram("Google access needs a sign-in", "detail ~/.secrets/x.json",
                                     action="Say: finish Google access setup")
    assert result.delivered
    assert texts[0] == "Google access needs a sign-in\nSay: finish Google access setup"
    assert texts[1].startswith("Details:") and "~/.secrets/x.json" in texts[1]


@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_toasts_never_reach_the_real_desktop_from_a_test():
    result = router.deliver_toast("t", "a", "d", key="k")
    assert result.delivered is False and result.evidence == "not_configured"



@pytest.mark.req("operator-notify/routes-by-severity", existing=True)  # ported unchanged from Project Meta
def test_toast_arrival_is_found_despite_wsl_windows_clock_skew(tmp_path):
    """2026-10-06: WSL ran 2m48s ahead of Windows; a 5-second window reported a
    toast that was in the store as absent. The nonce'd needle carries identity."""
    wsl_now = datetime.now(timezone.utc)
    windows_arrival = wsl_now - timedelta(minutes=3)
    db = _store(tmp_path / "wpn.db", [(windows_arrival, "file:///C:/x/google-personal-access-1230.txt")])

    found = router.verify_toast_arrival(
        "google-personal-access-1230.txt", since=router.toast_search_since(wsl_now), db_path=db,
    )
    assert found.delivered, found


# --- Settings and the move from Project Meta (AES consolidation plan row 11, 2026-11-17) ---


def _settings(tmp_path, monkeypatch, text: str) -> None:
    graph = tmp_path / "cfg" / "PROJECT_GRAPH.json"
    graph.parent.mkdir(parents=True, exist_ok=True)
    (graph.parent / "graph-config.yaml").write_text(text, encoding="utf-8")
    monkeypatch.setenv("PROJECT_GRAPH", str(graph))


class _Register:
    """A fake gh holding issues per repository; records every call."""

    def __init__(self, issues: dict[str, list[dict]]):
        self.issues = issues
        self.calls: list[list[str]] = []

    def __call__(self, args):
        import json as _json

        args = list(args)
        self.calls.append(args)
        repo = args[args.index("-R") + 1] if "-R" in args else ""
        if args[:2] == ["issue", "list"]:
            return _json.dumps(self.issues.get(repo, []))
        if args[:2] == ["issue", "view"]:
            return _json.dumps({"body": "", "comments": []})
        if args[:2] == ["issue", "create"]:
            return f"https://github.com/{repo}/issues/1\n"
        return ""


def _open_issue(key: str, number: int = 2713) -> dict:
    return {"number": number, "state": "OPEN", "title": "t", "body": f"b\n\n<!-- concern-key: {key} -->\n"}


@pytest.mark.req("operator-notify/concern-repository-comes-from-the-settings")
def test_the_concern_repository_comes_from_the_settings(tmp_path, monkeypatch):
    """Project Meta hard-coded its own repository; AES reads it from the private settings."""
    _settings(tmp_path, monkeypatch, "operator_notify:\n  concern_repo: o/aes\n  waiting_label: waiting:x\n")
    gh = _Register({})
    monkeypatch.setattr(router, "CONCERN_RUNNER", gh)
    result = router.deliver_concern(key="k", title="t", body="b", source="s", occurrence="k:1",
                                    waiting_on_brian=True)
    assert result.delivered and result.detail == "o/aes created https://github.com/o/aes/issues/1"
    create = next(c for c in gh.calls if c[:2] == ["issue", "create"])
    assert "waiting:x" in create[create.index("--label") + 1]
    monkeypatch.setenv(router.CONCERN_REPO_ENV, "o/env")
    assert router.concern_repo() == "o/env"


@pytest.mark.req("operator-notify/concern-repository-comes-from-the-settings")
def test_no_named_concern_repository_fails_the_route_and_says_so(tmp_path, monkeypatch):
    """A missing setting is a failed route with the reason, never a guess at a repository."""
    gh = _Register({})
    monkeypatch.setattr(router, "CONCERN_RUNNER", gh)
    result = router.deliver_concern(key="k", title="t", body="b", source="s", occurrence=None)
    assert not result.delivered and "no concern repository is named" in (result.detail or "")
    assert gh.calls == []


@pytest.mark.req("operator-notify/an-open-legacy-concern-is-not-duplicated")
def test_an_open_concern_in_the_old_repository_is_updated_there_not_duplicated(tmp_path, monkeypatch):
    """project-meta #2713 (key usage-pace, waiting:brian) was open at the move; a recurrence must comment on it."""
    _settings(tmp_path, monkeypatch,
              "operator_notify:\n  concern_repo: o/aes\n  legacy_concern_repos: [o/project-meta]\n")
    gh = _Register({"o/project-meta": [_open_issue("usage-pace")]})
    monkeypatch.setattr(router, "CONCERN_RUNNER", gh)
    result = router.deliver_concern(key="usage-pace", title="t", body="b", source="usage_pace",
                                    occurrence="usage-pace:off_track-opus", waiting_on_brian=True)
    assert result.delivered and result.detail == "o/project-meta commented #2713"
    assert not [c for c in gh.calls if c[:2] == ["issue", "create"]]
    assert not [c for c in gh.calls if c[:2] != ["issue", "list"] and "o/aes" in c]


@pytest.mark.req("operator-notify/an-open-legacy-concern-is-not-duplicated")
def test_a_closed_or_missing_legacy_concern_files_in_the_new_repository(tmp_path, monkeypatch):
    """Only an open concern stays put; anything else is filed where agents now work."""
    _settings(tmp_path, monkeypatch,
              "operator_notify:\n  concern_repo: o/aes\n  legacy_concern_repos: [o/project-meta]\n")
    closed = {**_open_issue("usage-pace"), "state": "CLOSED"}
    gh = _Register({"o/project-meta": [closed]})
    monkeypatch.setattr(router, "CONCERN_RUNNER", gh)
    result = router.deliver_concern(key="usage-pace", title="t", body="b", source="usage_pace", occurrence=None)
    assert result.delivered and result.detail == "o/aes created https://github.com/o/aes/issues/1"


@pytest.mark.req("operator-notify/an-open-legacy-concern-is-not-duplicated")
def test_resolve_closes_the_open_legacy_concern(tmp_path, monkeypatch):
    _settings(tmp_path, monkeypatch,
              "operator_notify:\n  concern_repo: o/aes\n  legacy_concern_repos: [o/project-meta]\n")
    gh = _Register({"o/project-meta": [_open_issue("usage-pace")]})
    monkeypatch.setattr(router, "CONCERN_RUNNER", gh)
    assert router.resolve(key="usage-pace", evidence="on track", stamp_dir=tmp_path) == "stamp cleared; closed #2713"
    assert ["issue", "close", "2713", "-R", "o/project-meta", "--reason", "completed"] in gh.calls
