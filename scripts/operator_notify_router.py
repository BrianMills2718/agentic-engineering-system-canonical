#!/usr/bin/env python3
"""Route one operator notification to whoever can act on it, and prove arrival.

Implements: operator-notify/notices-route-by-who-must-act

Plan #269 Step 2; re-routed 2026-10-06 (issue #1958). Moved here from Project Meta
(``scripts/operator_notify_router.py`` at ``ee2957b1f``) on 2026-11-17, AES consolidation plan row 11. The
behaviour, the state files and the record format are unchanged; only where the settings come from changed.

SETTINGS. The concern repository is ``concern_repo:`` under ``operator_notify:`` in ``graph-config.yaml`` (the
private aes-config repository, found beside ``$PROJECT_GRAPH``, else ``~/code2/aes-config``), unless
``OPERATOR_CONCERN_REPO`` is set; with neither, the concern route fails and says so. ``legacy_concern_repos:``
lists repositories concerns were filed in before the move: while one of them holds an *open* concern for a key,
that concern is updated or closed there instead of a second one being opened (the same key, label and hidden
marker as ``concern_issue.find_existing``). ``waiting_label:`` names the label a needs-human concern carries
(default ``waiting:brian``). The Telegram token, chat id and ntfy topic are secrets and stay in the environment or
the secrets file, never in that settings file.

WHO ACTS. Every notification now declares, through its severity, who must act:

- ``agent`` (the default): an agent can fix it. It opens or updates a keyed
  concern in the agent work queue (``concern_issue.py``, GitHub Issues under
  ``concern:feedback``). Nothing interrupts Brian.
- ``needs-human``: only Brian can act (sign in, approve, pay). He gets a quiet
  Windows notification (bottom-right; clicking it opens the full text in a
  plain, copyable file) and a Telegram message: first one short line of what
  is wrong plus one of what to do, then the details. The same concern is
  opened (labelled ``waiting:brian``) so the obligation is tracked. The visible
  wording is checked at the sender (``check_human_wording``): short, one line
  each, no paths, file names, flags or error class names. It is sent once per *state* of the key: the
  same unresolved condition does not re-message him every day. ``--resolve``
  clears the key when the condition is fixed, so a later recurrence messages
  him again.
- ``attention`` / ``urgent``: the ntfy phone push the ecosystem-ops notifiers
  already use (cron health, Yep Inbox, feedback watchdog). Unchanged except
  that the desk popup is gone.
- ``info``: recorded only.

THE DESK POPUP IS GONE. The Windows ``msg.exe`` dialog ("Message from ...")
truncated at ~240 characters, could not be selected or copied, stole focus,
and reached Brian for things an agent should have fixed. Brian, 2026-10-06:
"these should go to an autonomous agent to fix unless my input is actually
needed." There is no msg.exe route anywhere in this module or its callers.

ARRIVAL, NOT EXIT CODE. A claim that something left this machine is evidenced
from outside it: Telegram's ``sendMessage`` response must say ``ok`` and carry
a ``message_id``; the concern route returns the issue it created or updated;
ntfy is checked at the broker (``observed_at_broker`` -- the message is held
for the phone, which is not the same as the phone displaying it). The toast
check (``verify_toast_arrival``) reads Windows' own notification store for the
same reason: a toast sender's exit code proved nothing on this machine.

SECRETS. The Telegram bot token and the ntfy topic are read from the
environment or the single matching line of ``~/.secrets/api_keys.env`` and are
never printed, logged, or written into the notification record.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import json
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from email.header import Header
from datetime import datetime, timedelta, timezone
from pathlib import Path

import operator_notification_record as notification_record

WINDOWS_NOTIFICATION_DB = (
    "AppData/Local/Microsoft/Windows/Notifications/wpndatabase.db"
)

# Severity -> the routes attempted, in order. See the module docstring for who
# each severity is for. `agent` is the default: a notification that does not
# say Brian must act is work for an agent, not an interruption.
ROUTES_BY_SEVERITY = {
    "info": (),
    "agent": ("concern",),
    "needs-human": ("toast", "telegram", "concern"),
    "attention": ("ntfy",),
    "urgent": ("ntfy",),
}
DEFAULT_SEVERITY = "agent"

# Severities that attempt EVERY route rather than stopping at the first that
# works: a needs-human notice must reach Brian AND be tracked for agents.
DELIVER_TO_EVERY_ROUTE = frozenset({"needs-human"})

# Severities whose delivery counts only if this route landed. A concern filed
# while the Telegram message failed has not told Brian anything, so the key is
# not stamped and the next run tries again.
REQUIRED_ROUTE = {"needs-human": "telegram"}

# Severities rate-limited by STATE rather than by clock: one message per
# distinct condition, not one per day while it stays unresolved.
STATEFUL_SEVERITIES = frozenset({"needs-human"})

TELEGRAM_API = "https://api.telegram.org"
TELEGRAM_TOKEN_ENV = "TELEGRAM_AGENTS_BOT_TOKEN"
TELEGRAM_CHAT_ENV = "OPERATOR_TELEGRAM_CHAT_ID"
# Telegram rejects messages over 4096 characters; longer text is split rather
# than cut, because a truncated instruction is the defect this replaced.
TELEGRAM_MAX_CHARS = 4000

CONCERN_REPO_ENV = "OPERATOR_CONCERN_REPO"
WAITING_ON_BRIAN_LABEL = "waiting:brian"


def config_path() -> Path:
    """``graph-config.yaml`` beside the project graph (``$PROJECT_GRAPH``, else the aes-config copy)."""
    graph = os.environ.get("PROJECT_GRAPH") or str(Path.home() / "code2/aes-config/PROJECT_GRAPH.json")
    return Path(graph).expanduser().parent / "graph-config.yaml"


def settings() -> dict:
    """The ``operator_notify:`` section of graph-config.yaml, or {} when absent. Read when needed, not at import."""
    try:
        import yaml

        data = yaml.safe_load(config_path().read_text(encoding="utf-8")) or {}
    except OSError:
        return {}
    section = data.get("operator_notify") if isinstance(data, dict) else None
    return section if isinstance(section, dict) else {}


def concern_repo(repo: str | None = None) -> str:
    """The repository concerns are filed in: the argument, else the environment, else the settings.

    Implements: operator-notify/the-concern-repository-comes-from-the-settings
    """
    resolved = repo or os.environ.get(CONCERN_REPO_ENV, "") or str(settings().get("concern_repo") or "")
    if not resolved:
        raise RouterError(
            f"no concern repository is named: set {CONCERN_REPO_ENV} or put `concern_repo:` under "
            f"`operator_notify:` in {config_path()}"
        )
    return resolved


def repo_holding_open_concern(ci, repo: str, key: str, run) -> str:
    """The first legacy repository holding an OPEN concern for ``key``, else ``repo``.

    Concerns filed before the move (Project Meta) stay where they are while open, so a recurrence comments on the
    issue Brian already has instead of opening a second one in the new repository.

    Implements: operator-notify/an-open-legacy-concern-is-not-duplicated
    """
    for legacy in settings().get("legacy_concern_repos") or []:
        if legacy == repo:
            continue
        found = ci.find_existing(legacy, key, run)
        if found is not None and found.state == "OPEN":
            return str(legacy)
    return repo

NTFY_HOST = "https://ntfy.sh"
# The topic is a shared secret: ntfy.sh topics are public to anyone who knows
# the name, so knowing it means being able to read and publish to Brian's
# phone. It is read from the environment and never logged, printed, or written
# into the notification record.
NTFY_TOPIC_ENV = "OPERATOR_NTFY_TOPIC"
# A published message is not queryable the instant the POST returns 200.
# Measured 2026-09-09: an end-to-end send reported observed_absence against a
# message that a manual poll found moments later. Checking once, immediately,
# turns that race into a false "never arrived" -- the opposite of this module's
# error and just as misleading.
NTFY_SETTLE_ATTEMPTS = 4
NTFY_SETTLE_SECONDS = 1.5
MIN_NTFY_WINDOW_SECONDS = 60


class RouterError(RuntimeError):
    """Raised when the router cannot function. Never swallowed."""


@dataclass(frozen=True)
class DeliveryResult:
    """What one route did, and how strongly that is known."""

    route: str
    delivered: bool
    evidence: str
    detail: str | None = None


def windows_notification_db(user: str | None = None) -> Path | None:
    """Return the Windows notification store, or None when not reachable."""
    if user is None:
        user = os.environ.get("WINDOWS_USER", "")
    if not user:
        return None
    path = Path("/mnt/c/Users") / user / WINDOWS_NOTIFICATION_DB
    return path if path.exists() else None


def verify_toast_arrival(
    needle: str,
    *,
    since: datetime,
    db_path: Path | None = None,
) -> DeliveryResult:
    """Ask Windows whether a toast actually arrived, rather than asking the sender.

    Copies the store before reading it: it is live, in WAL mode, and held open
    by Windows. Reading it in place risks a partial view, and this check exists
    precisely because a partial view is what produced the wrong answer before.
    """
    db = db_path or windows_notification_db()
    if db is None:
        return DeliveryResult(
            route="toast",
            delivered=False,
            evidence="unverifiable",
            detail="Windows notification store not reachable from here",
        )
    with tempfile.TemporaryDirectory() as tmp:
        local = Path(tmp) / "wpndatabase.db"
        try:
            local.write_bytes(db.read_bytes())
            for suffix in ("-wal", "-shm"):
                sidecar = db.with_name(db.name + suffix)
                if sidecar.exists():
                    local.with_name(local.name + suffix).write_bytes(sidecar.read_bytes())
            conn = sqlite3.connect(local)
            cutoff = int((since - datetime(1601, 1, 1, tzinfo=timezone.utc)).total_seconds() * 10_000_000)
            rows = conn.execute(
                "SELECT Payload FROM Notification WHERE ArrivalTime >= ?", (cutoff,)
            ).fetchall()
        except (OSError, sqlite3.Error) as exc:
            return DeliveryResult(
                route="toast",
                delivered=False,
                evidence="unverifiable",
                detail=f"could not read the notification store: {exc}",
            )
    target = needle.encode("utf-8", "ignore")
    for (payload,) in rows:
        blob = payload if isinstance(payload, bytes) else str(payload).encode("utf-8", "ignore")
        if target in blob:
            return DeliveryResult(route="toast", delivered=True, evidence="observed_arrival")
    return DeliveryResult(
        route="toast",
        delivered=False,
        evidence="observed_absence",
        detail=f"not present among {len(rows)} notification(s) since {since.isoformat()}",
    )


SECRETS_FILE_ENV = "OPERATOR_SECRETS_FILE"


def _secret_from_file(name: str) -> str:
    """Read only one named line from the workspace secrets file.

    The scheduled units (daily audit, feedback watchdog, google access) do not
    load ``~/.secrets/api_keys.env``, so they logged ``ntfy (not_configured)``
    while the topic existed there (measured 2026-09-14). Loading the whole file
    into those units would also import an unrelated ``GITHUB_TOKEN`` that
    breaks ``gh``; reading the one key keeps that out. The value is never
    printed.
    """
    path = Path(os.environ.get(SECRETS_FILE_ENV, str(Path.home() / ".secrets" / "api_keys.env")))
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    for line in lines:
        key, sep, value = line.strip().removeprefix("export ").partition("=")
        if sep and key.strip() == name:
            return value.strip().strip("'\"")
    return ""


def _topic_from_secrets_file() -> str:
    return _secret_from_file(NTFY_TOPIC_ENV)


def ntfy_topic(topic: str | None = None) -> str | None:
    """Return the configured ntfy topic, or None when the route is not set up."""
    if topic is not None:
        resolved = topic
    else:
        resolved = os.environ.get(NTFY_TOPIC_ENV, "") or _topic_from_secrets_file()
    return resolved.strip() or None


def verify_ntfy_arrival(
    needle: str,
    *,
    since: datetime,
    topic: str | None = None,
    host: str = NTFY_HOST,
    timeout: float = 15.0,
) -> DeliveryResult:
    """Ask ntfy's server what it is holding, rather than trusting the POST's 200.

    ``since`` IS LOAD-BEARING, and omitting it is the trap. ntfy's subscription
    endpoint defaults to ``since=none`` -- it streams what arrives next, not
    what it already has -- so ``?poll=1`` on its own returns an empty list for a
    topic that certainly holds messages. Measured 2026-09-09: the first check
    written here reported zero for a message that was there, and a check that
    can only come back empty is the same defect as a check that can only come
    back green, which is why this module exists.

    What this establishes and what it does not: a hit means the message left
    this machine and is in ntfy.sh's store, which is a strictly stronger claim
    than a 200 from our own POST. It is NOT proof that the phone displayed it --
    that depends on the app being installed, subscribed, and permitted to alert.
    So the evidence is named ``observed_at_broker``, not ``observed_arrival``.
    Overstating it here would repeat the mistake the toast route made.
    """
    resolved = ntfy_topic(topic)
    if resolved is None:
        return DeliveryResult(
            route="ntfy",
            delivered=False,
            evidence="unverifiable",
            detail=f"no ntfy topic configured; set {NTFY_TOPIC_ENV}",
        )
    # Floor the window at a minute. It is evaluated against ntfy's clock, not
    # ours, so a window of a few seconds is at the mercy of clock skew between
    # this machine and the server -- and the match is on message text anyway,
    # so a wider window costs nothing and removes a way for a real delivery to
    # read as absent.
    window = max(int((datetime.now(timezone.utc) - since).total_seconds()), MIN_NTFY_WINDOW_SECONDS)
    url = f"{host}/{resolved}/json?poll=1&since={window}s"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            payload = response.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        return DeliveryResult(
            route="ntfy",
            delivered=False,
            evidence="unverifiable",
            detail=f"could not read the ntfy topic: {exc}",
        )
    messages = []
    for line in payload.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("event") == "message":
            messages.append(event)
    for message in messages:
        haystack = f"{message.get('title', '')}\n{message.get('message', '')}"
        if needle in haystack:
            return DeliveryResult(route="ntfy", delivered=True, evidence="observed_at_broker")
    return DeliveryResult(
        route="ntfy",
        delivered=False,
        evidence="observed_absence",
        detail=f"not present among {len(messages)} message(s) in the last {window}s",
    )


def deliver_ntfy(
    title: str,
    body: str,
    *,
    topic: str | None = None,
    host: str = NTFY_HOST,
    timeout: float = 15.0,
    priority: str | None = None,
    tags: str | None = None,
    markdown: bool = True,
) -> DeliveryResult:
    """Publish to ntfy, then check the broker rather than trusting the POST.

    Message bodies transit a third-party server on a topic anyone who learns
    the name can read, so callers keep them terse and non-sensitive. This is
    the away-from-desk route; it is the only one that works when the operator
    is not at this machine.

    ``priority``, ``tags`` and ``markdown`` exist so that a caller migrating
    onto the router loses nothing it already had. The three scheduled
    notifiers in ecosystem-ops each set some of them -- a stale scout run is
    not the same urgency as a dead one, and ``Markdown: no`` is what keeps a
    multi-line body readable on the phone. Dropping them silently in the name
    of consolidation would make the router a downgrade for its first real
    consumers, which is how consolidations get reverted.
    """
    resolved = ntfy_topic(topic)
    if resolved is None:
        return DeliveryResult(
            route="ntfy",
            delivered=False,
            evidence="not_configured",
            detail=f"no ntfy topic configured; set {NTFY_TOPIC_ENV}",
        )
    sent_at = datetime.now(timezone.utc)
    # http.client sends header values as Latin-1, so a title with "…" or any
    # non-Latin-1 character raised UnicodeEncodeError before the POST and the
    # push never left (attention-page.service, every run with a truncated
    # title, 2026-09-18 to 2026-09-27). ntfy decodes RFC 2047 encoded words.
    title_header = title if title.isascii() else Header(title, "utf-8").encode()
    headers = {"Title": title_header, "Priority": priority or "default"}
    if tags:
        headers["Tags"] = tags
    if not markdown:
        headers["Markdown"] = "no"
    request = urllib.request.Request(
        f"{host}/{resolved}",
        data=body.encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        return DeliveryResult(
            route="ntfy", delivered=False, evidence="send_failed", detail=str(exc)
        )
    if status != 200:
        return DeliveryResult(
            route="ntfy",
            delivered=False,
            evidence="send_failed",
            detail=f"ntfy returned HTTP {status}",
        )
    # The 200 above is this machine talking about itself. Ask the broker --
    # more than once, because the message takes a moment to become queryable.
    result = DeliveryResult(
        route="ntfy", delivered=False, evidence="unverifiable",
        detail="arrival check did not run",
    )
    for attempt in range(NTFY_SETTLE_ATTEMPTS):
        if attempt:
            time.sleep(NTFY_SETTLE_SECONDS)
        result = verify_ntfy_arrival(
            body[:64], since=sent_at, topic=resolved, host=host, timeout=timeout,
        )
        if result.delivered:
            return result
    return result


# ---------------------------------------------------------------------------
# Desk toast (needs-human only). Measured 2026-10-06: a toast shown under
# PowerShell's registered app id appeared in Windows' notification store
# (observed_arrival), whereas the 2026-09-09 attempts under an unregistered id
# and the borrowed Explorer id never did. Arrival is still checked in the store
# on every send, never assumed from the exit code.
TOAST_APP_ID = r"{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe"
POWERSHELL_CANDIDATES = (
    "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
    "/mnt/c/windows/System32/WindowsPowerShell/v1.0/powershell.exe",
)
TOAST_SETTLE_ATTEMPTS = 4
TOAST_SETTLE_SECONDS = 1.5
TOAST_WINDOW_HOURS = 24

# Wording rule for anything Brian sees first (toast, first Telegram message):
# one short plain sentence of what is wrong, one short line of what to do.
# Brian, 2026-10-06: alerts "need to be concise and simply understandable."
# Details (paths, error text) belong in the body, behind the click / in the
# second Telegram message. These are structural checks on identifiers and
# paths, not a judgement of the prose.
MAX_HEADLINE_CHARS = 80
MAX_ACTION_CHARS = 110
_JARGON_PATTERNS = (
    re.compile(r"(^|\s)(~|\.{0,2})/\S"),          # a filesystem path
    re.compile(r"[A-Za-z]:\\"),                     # a Windows path
    re.compile(r"\b[A-Z][A-Za-z]+(Error|Exception)\b"),  # an error class name
    re.compile(r"\S+\.(py|json|sh|txt|yaml|env)\b"),  # a file name
    re.compile(r"--[a-z]"),                         # a command-line flag
)


def check_human_wording(title: str, action: str | None) -> list[str]:
    """Problems with the visible text of a needs-human alert; empty means OK."""
    problems: list[str] = []
    if not action:
        problems.append("needs-human alerts must say what to do (--action)")
    for name, text, limit in (("title", title, MAX_HEADLINE_CHARS), ("action", action or "", MAX_ACTION_CHARS)):
        if len(text) > limit:
            problems.append(f"{name} is {len(text)} characters; keep it to {limit}")
        if "\n" in text:
            problems.append(f"{name} must be one line")
        for pattern in _JARGON_PATTERNS:
            if pattern.search(text):
                problems.append(f"{name} shows a path, file, flag or error name ({pattern.pattern}); move it to the details")
                break
    return problems


def _windows_user() -> str | None:
    user = os.environ.get("WINDOWS_USER", "").strip()
    if user:
        return user
    for cmd in ("/mnt/c/Windows/System32/cmd.exe", "/mnt/c/windows/System32/cmd.exe"):
        if Path(cmd).exists():
            try:
                out = subprocess.run([cmd, "/c", "echo %USERNAME%"], capture_output=True,
                                     text=True, timeout=30, cwd="/").stdout.strip()
            except (OSError, subprocess.SubprocessError):
                return None
            return out if out and out != "%USERNAME%" else None
    return None


def _xml_escape(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&apos;"))


def toast_search_since(now: datetime) -> datetime:
    """Start of the store scan for a just-sent toast (wide on purpose; see deliver_toast)."""
    return now - timedelta(hours=TOAST_WINDOW_HOURS)


def deliver_toast(title: str, action: str, details: str, *, key: str) -> DeliveryResult:
    """Quiet Windows notification (bottom-right, Action Center); click opens the full text.

    The full message is written to a plain text file under the Windows user's
    LocalAppData, and the toast's click launches it, so everything is
    selectable and copyable. Delivery is claimed only when the toast is found
    in Windows' own notification store.
    """
    if os.environ.get("PYTEST_CURRENT_TEST") and os.environ.get("OPERATOR_ALLOW_REAL_TOAST") != "1":
        # A test must never put a notification on Brian's real desktop.
        return DeliveryResult(route="toast", delivered=False, evidence="not_configured",
                              detail="real toasts are disabled under pytest")
    powershell = next((p for p in POWERSHELL_CANDIDATES if Path(p).exists()), None)
    user = _windows_user() if powershell else None
    if not powershell or not user:
        return DeliveryResult(route="toast", delivered=False, evidence="not_configured",
                              detail="no Windows desktop reachable from here")
    nonce = f"{int(time.time())}{os.getpid()}"
    safe_key = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)
    folder = Path("/mnt/c/Users") / user / "AppData/Local/operator-notify"
    name = f"{safe_key}-{nonce}.txt"
    try:
        folder.mkdir(parents=True, exist_ok=True)
        text = f"{title}\n{action}\n\n{details}\n"
        # Notepad-friendly: CRLF line ends and a BOM so it opens as UTF-8.
        (folder / name).write_text(text.replace("\n", "\r\n"), encoding="utf-8-sig", newline="")
    except OSError as exc:
        return DeliveryResult(route="toast", delivered=False, evidence="send_failed",
                              detail=f"could not write the full-text file: {exc}")
    launch = f"file:///C:/Users/{user}/AppData/Local/operator-notify/{name}"
    xml = (
        f'<toast activationType="protocol" launch="{_xml_escape(launch)}">'
        f'<visual><binding template="ToastGeneric"><text>{_xml_escape(title)}</text>'
        f'<text>{_xml_escape(action)}</text><text>Click for the full message.</text>'
        f'</binding></visual><audio silent="true"/></toast>'
    )
    script = (
        "$ErrorActionPreference='Stop';"
        "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;"
        "[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null;"
        "$x = New-Object Windows.Data.Xml.Dom.XmlDocument;"
        f"$x.LoadXml('{xml.replace(chr(39), chr(39) * 2)}');"
        f"[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('{TOAST_APP_ID}')"
        ".Show([Windows.UI.Notifications.ToastNotification]::new($x))"
    )
    import base64

    # The needle (the full-text file name) carries a per-send nonce, so the
    # window only bounds the scan. It must be wide: WSL's clock and Windows'
    # clock disagree. Measured 2026-10-06: WSL ran 2m48s ahead, and a 5-second
    # window reported observed_absence for a toast that was in the store.
    sent_at = toast_search_since(datetime.now(timezone.utc))
    try:
        result = subprocess.run(
            [powershell, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
             "-EncodedCommand", base64.b64encode(script.encode("utf-16-le")).decode("ascii")],
            capture_output=True, text=True, timeout=90, cwd="/mnt/c",
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return DeliveryResult(route="toast", delivered=False, evidence="send_failed", detail=str(exc))
    if result.returncode != 0:
        return DeliveryResult(route="toast", delivered=False, evidence="send_failed",
                              detail=f"powershell exited {result.returncode}")
    db = windows_notification_db(user)
    verdict = DeliveryResult(route="toast", delivered=False, evidence="unverifiable",
                             detail="arrival check did not run")
    for attempt in range(TOAST_SETTLE_ATTEMPTS):
        if attempt:
            time.sleep(TOAST_SETTLE_SECONDS)
        verdict = verify_toast_arrival(name, since=sent_at, db_path=db)
        if verdict.delivered:
            break
    return verdict


def _notify_operator_module():
    """Import the stamp helpers (``due``/``record_sent``) shared with notify_operator."""
    try:
        import notify_operator
    except ImportError as exc:  # pragma: no cover - import wiring
        raise RouterError(f"stamp helpers unavailable: {exc}") from exc
    return notify_operator


def _concern_issue_module():
    try:
        import concern_issue
    except ImportError as exc:  # pragma: no cover - import wiring
        raise RouterError(f"concern route unavailable: {exc}") from exc
    return concern_issue


# Injectable for tests: the gh runner the concern route uses. None means the
# real ``concern_issue.gh_runner``.
CONCERN_RUNNER = None


def telegram_config() -> tuple[str | None, str | None]:
    """Return (bot token, chat id) from the environment or the secrets file."""
    token = os.environ.get(TELEGRAM_TOKEN_ENV, "") or _secret_from_file(TELEGRAM_TOKEN_ENV)
    chat = os.environ.get(TELEGRAM_CHAT_ENV, "") or _secret_from_file(TELEGRAM_CHAT_ENV)
    return (token.strip() or None, chat.strip() or None)


def _telegram_chunks(text: str, limit: int = TELEGRAM_MAX_CHARS) -> list[str]:
    """Split on line boundaries so no part of the message is ever cut off."""
    chunks: list[str] = []
    current = ""
    for line in text.splitlines(keepends=True):
        while len(line) > limit:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(line[:limit])
            line = line[limit:]
        if len(current) + len(line) > limit:
            chunks.append(current)
            current = ""
        current += line
    if current:
        chunks.append(current)
    return chunks or [text]


def deliver_telegram(
    title: str,
    body: str,
    *,
    action: str | None = None,
    host: str = TELEGRAM_API,
    timeout: float = 20.0,
) -> DeliveryResult:
    """Send Brian the full text as plain Telegram message(s); verify by response.

    Plain text, no parse mode: every character he sees can be selected and
    copied, and nothing in a path or command can be eaten as markup. Delivery
    is claimed only when Telegram answers ``ok`` with a ``message_id`` for
    every part -- that is Telegram holding the message for his account, the
    same strength of claim as ntfy's ``observed_at_broker``.

    Uses ``sendMessage`` only. The bot's webhook belongs to another service
    (Paperclip); ``getUpdates``/``deleteWebhook`` would break it.
    """
    token, chat = telegram_config()
    if not token or not chat:
        missing = [name for name, value in ((TELEGRAM_TOKEN_ENV, token), (TELEGRAM_CHAT_ENV, chat)) if not value]
        return DeliveryResult(
            route="telegram", delivered=False, evidence="not_configured",
            detail=f"set {', '.join(missing)} in the environment or ~/.secrets/api_keys.env",
        )
    message_ids: list[str] = []
    # With an action, the first message is the short alert (what is wrong,
    # what to do) and the details follow as a second message.
    parts = (
        [f"{title}\n{action}", *_telegram_chunks(f"Details:\n{body}")]
        if action else _telegram_chunks(f"{title}\n\n{body}")
    )
    for part in parts:
        payload = json.dumps(
            {"chat_id": chat, "text": part, "disable_web_page_preview": True}
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{host}/bot{token}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                answer = json.loads(response.read().decode("utf-8") or "{}")
        except urllib.error.HTTPError as exc:
            try:
                description = json.loads(exc.read().decode("utf-8")).get("description", "")
            except (ValueError, OSError):
                description = ""
            detail = f"Telegram returned HTTP {exc.code} {description}".strip()
            return DeliveryResult(route="telegram", delivered=False, evidence="send_failed",
                                  detail=detail.replace(token, "<token>"))
        except (urllib.error.URLError, OSError, TimeoutError, ValueError) as exc:
            return DeliveryResult(route="telegram", delivered=False, evidence="send_failed",
                                  detail=str(exc).replace(token, "<token>"))
        message_id = (answer.get("result") or {}).get("message_id") if answer.get("ok") else None
        if message_id is None:
            return DeliveryResult(
                route="telegram", delivered=False, evidence="send_failed",
                detail=f"Telegram did not confirm: {str(answer.get('description') or answer)[:200]}",
            )
        message_ids.append(str(message_id))
    return DeliveryResult(
        route="telegram", delivered=True, evidence="accepted_by_telegram",
        detail=f"message_id {','.join(message_ids)}",
    )


def deliver_concern(
    *,
    key: str,
    title: str,
    body: str,
    source: str,
    occurrence: str | None,
    waiting_on_brian: bool = False,
    repo: str | None = None,
) -> DeliveryResult:
    """Open or update the keyed concern an agent works (the agent work queue)."""
    ci = _concern_issue_module()
    label_source = "".join(c if c.isalnum() or c in "-_." else "-" for c in source) or "operator-notify"
    extra = (str(settings().get("waiting_label") or WAITING_ON_BRIAN_LABEL),) if waiting_on_brian else ()
    run = CONCERN_RUNNER or ci.gh_runner
    try:
        resolved_repo = repo_holding_open_concern(ci, concern_repo(repo), key, run)
        outcome = ci.open_concern(
            resolved_repo, key, title, body, label_source, run,
            occurrence=occurrence, extra_labels=extra,
        )
    except Exception as exc:  # noqa: BLE001 -- any gh failure is a failed route, reported
        return DeliveryResult(route="concern", delivered=False, evidence="send_failed", detail=str(exc)[:300])
    return DeliveryResult(route="concern", delivered=True, evidence="filed", detail=f"{resolved_repo} {outcome}")


def state_fingerprint(title: str, body: str, state: str | None) -> str:
    """Identity of one condition: the caller's named state, else the text."""
    if state:
        return state
    return hashlib.sha256(f"{title}\n{body}".encode("utf-8")).hexdigest()[:16]


def notify(
    *,
    key: str,
    title: str,
    body: str,
    severity: str = DEFAULT_SEVERITY,
    source: str = "router",
    record_dir: Path | None = None,
    routes: tuple[str, ...] | None = None,
    min_interval_hours: float = 0.0,
    stamp_dir: Path | None = None,
    priority: str | None = None,
    tags: str | None = None,
    markdown: bool = True,
    state: str | None = None,
    action: str | None = None,
) -> tuple[notification_record.NotificationEntry, list[DeliveryResult]]:
    """Record the notification, then attempt its routes in order.

    Suppression never touches the record: every occurrence is written to the
    log; what is suppressed is the repeat delivery. Two kinds:

    - ``min_interval_hours`` (any severity): not again within that window.
    - state (``needs-human``): not again while the key's condition is the same
      one already sent. A different ``state`` (or, without one, different
      text) is a new condition and is sent. ``resolve`` clears it.

    A suppressed notice is recorded as delivered with the suppression named in
    its route: the person or agent was already told about this key.

    Implements: operator-notify/notices-route-by-who-must-act
    """
    if severity not in ROUTES_BY_SEVERITY:
        raise RouterError(
            f"unsupported severity {severity!r}; expected one of "
            f"{', '.join(ROUTES_BY_SEVERITY)}"
        )
    if severity == "needs-human":
        problems = check_human_wording(title, action)
        if problems:
            raise RouterError("needs-human wording: " + "; ".join(problems))
    record_body = f"{action}\n\n{body}" if action else body
    entry = notification_record.append(
        key=key, title=title, body=record_body, severity=severity, source=source,
        record_dir=record_dir,
    )
    stamps = _notify_operator_module()
    resolved_stamp_dir = stamp_dir or stamps.DEFAULT_STAMP_DIR
    now = datetime.now(timezone.utc)
    fingerprint = state_fingerprint(title, body, state)

    attempted = routes if routes is not None else ROUTES_BY_SEVERITY[severity]
    if attempted and severity in STATEFUL_SEVERITIES:
        if stamps.last_state(resolved_stamp_dir, key) == fingerprint:
            notification_record.mark_outcome(
                entry, delivered=True,
                route=f"suppressed: this state ({fingerprint}) was already sent; resolve the key to reset",
                record_dir=record_dir,
            )
            return entry, []
    if attempted and min_interval_hours > 0:
        allowed, reason = stamps.due(resolved_stamp_dir, key, min_interval_hours, now)
        if not allowed:
            notification_record.mark_outcome(
                entry, delivered=True, route=reason, record_dir=record_dir,
            )
            return entry, []

    results: list[DeliveryResult] = []
    every_route = severity in DELIVER_TO_EVERY_ROUTE
    for route in attempted:
        if route == "toast":
            result = deliver_toast(title, action or "", body, key=key)
        elif route == "telegram":
            result = deliver_telegram(title, body, action=action)
        elif route == "concern":
            told = [r for r in results if r.route == "telegram"]
            concern_body = body
            if severity == "needs-human":
                status = (
                    f"sent ({told[0].detail})" if told and told[0].delivered
                    else f"FAILED: {told[0].detail or told[0].evidence}" if told else "not attempted"
                )
                concern_body = (
                    f"{action}\n\n{body}\n\n---\nOnly Brian can act on this (needs-human). "
                    f"Telegram to Brian: {status}. Agents: do not redo his step; "
                    "close this concern with evidence once the condition is verified fixed."
                )
            result = deliver_concern(
                key=key, title=title, body=concern_body, source=source,
                occurrence=f"{key}:{fingerprint}",
                waiting_on_brian=severity == "needs-human",
            )
        elif route == "ntfy":
            result = deliver_ntfy(
                title, body, priority=priority, tags=tags, markdown=markdown
            )
        else:
            raise RouterError(f"no enabled transport for route {route!r}")
        results.append(result)
        if result.delivered and not every_route:
            break

    required = REQUIRED_ROUTE.get(severity)
    if required and required in attempted:
        landed = any(r.delivered for r in results if r.route == required)
    else:
        landed = any(r.delivered for r in results)
    summary = ", ".join(
        f"{r.route} ({r.evidence}{': ' + r.detail if r.detail else ''})" for r in results
    )
    if landed:
        stamps.record_sent(
            resolved_stamp_dir, key, now,
            state=fingerprint if severity in STATEFUL_SEVERITIES else None,
        )
        notification_record.mark_outcome(
            entry, delivered=True, route=summary, record_dir=record_dir,
        )
        return entry, results

    reason = (
        "; ".join(f"{r.route}: {r.detail or r.evidence}" for r in results)
        or "no route is attempted at this severity"
    )
    notification_record.mark_outcome(
        entry, delivered=False, route=",".join(attempted) or "none",
        failure_reason=reason, record_dir=record_dir,
    )
    return entry, results


def resolve(
    *,
    key: str,
    evidence: str,
    stamp_dir: Path | None = None,
    close_concern: bool = True,
) -> str:
    """The condition behind ``key`` is verified fixed: reset it and close its concern.

    Clearing the stamp is what lets the next, separate occurrence of the same
    condition reach Brian again instead of being suppressed as "already sent".
    """
    stamps = _notify_operator_module()
    stamps.clear_sent(stamp_dir or stamps.DEFAULT_STAMP_DIR, key)
    if not close_concern:
        return "stamp cleared"
    ci = _concern_issue_module()
    run = CONCERN_RUNNER or ci.gh_runner
    repo = repo_holding_open_concern(ci, concern_repo(), key, run)
    return "stamp cleared; " + ci.close_concern(repo, key, evidence, run)


def main(argv: list[str] | None = None) -> int:
    """Send one notification through the ranked routes."""
    parser = argparse.ArgumentParser(description="Route one operator notification.")
    parser.add_argument("--title")
    parser.add_argument("--body")
    parser.add_argument("--key")
    parser.add_argument(
        "--severity", default=DEFAULT_SEVERITY, choices=sorted(ROUTES_BY_SEVERITY),
        help=(
            "who must act: agent (default; opens a keyed concern), needs-human "
            "(Brian must act; one Telegram message per state plus a concern), "
            "attention/urgent (ntfy phone push), info (record only)"
        ),
    )
    parser.add_argument(
        "--state",
        help="name of the current condition; needs-human sends once per distinct state",
    )
    parser.add_argument(
        "--action",
        help="needs-human: one short plain line of what Brian should do (shown first)",
    )
    parser.add_argument(
        "--resolve", action="store_true",
        help="the condition behind --key is fixed: clear its stamp and close its concern",
    )
    parser.add_argument("--evidence", help="with --resolve: how the fix was verified")
    parser.add_argument("--source", default="router")
    parser.add_argument("--record-dir", type=Path, default=None)
    parser.add_argument("--stamp-dir", type=Path, default=None)
    parser.add_argument(
        "--priority",
        help="ntfy priority (min|low|default|high|urgent); ignored by other routes",
    )
    parser.add_argument("--tags", help="comma-separated ntfy tags; ignored by other routes")
    parser.add_argument(
        "--no-markdown",
        action="store_true",
        help="send ntfy 'Markdown: no', which keeps a multi-line body readable",
    )
    parser.add_argument(
        "--min-interval-hours",
        type=float,
        default=0.0,
        help="suppress the delivery (never the record) if this key notified more recently",
    )
    parser.add_argument(
        "--verify-toast",
        metavar="TEXT",
        help="read Windows' notification store and report whether TEXT arrived in the last hour",
    )
    parser.add_argument(
        "--verify-ntfy",
        metavar="TEXT",
        help="read ntfy's store and report whether TEXT is held for the phone (last hour)",
    )
    args = parser.parse_args(argv)

    if args.verify_ntfy:
        result = verify_ntfy_arrival(
            args.verify_ntfy, since=datetime.now(timezone.utc) - timedelta(hours=1)
        )
        print(f"ntfy: delivered={result.delivered} evidence={result.evidence}")
        if result.detail:
            print(f"  {result.detail}")
        return 0 if result.delivered else 1

    if args.verify_toast:
        result = verify_toast_arrival(
            args.verify_toast, since=datetime.now(timezone.utc) - timedelta(hours=1)
        )
        print(f"toast arrival: delivered={result.delivered} evidence={result.evidence}")
        if result.detail:
            print(f"  {result.detail}")
        return 0 if result.delivered else 1

    if args.resolve:
        if not args.key or not args.evidence:
            parser.error("--resolve needs --key and --evidence")
        print(f"resolved [{args.key}]: {resolve(key=args.key, evidence=args.evidence, stamp_dir=args.stamp_dir)}")
        return 0

    missing = [flag for flag, value in (("--title", args.title), ("--body", args.body), ("--key", args.key)) if not value]
    if missing:
        parser.error(f"missing {', '.join(missing)}")
    try:
        entry, results = notify(
            key=args.key, title=args.title, body=args.body,
            severity=args.severity, source=args.source, record_dir=args.record_dir,
            min_interval_hours=args.min_interval_hours, stamp_dir=args.stamp_dir,
            priority=args.priority, tags=args.tags, markdown=not args.no_markdown,
            state=args.state, action=args.action,
        )
    except RouterError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    for result in results:
        detail = f" ({result.detail})" if result.detail else ""
        print(f"{result.route}: delivered={result.delivered} evidence={result.evidence}{detail}")
    if not results:
        final = notification_record.read_all(args.record_dir)[-1]
        if (final.route or "").startswith("suppressed"):
            print(f"recorded only; {final.route}")
        else:
            print(f"recorded only; severity {args.severity!r} attempts no route")
    print(f"record: {notification_record.latest_path(args.record_dir)}")
    return 0 if delivery_landed(args.severity, results) else 1


def delivery_landed(severity: str, results: list[DeliveryResult]) -> bool:
    """True when nothing was attempted (recorded/suppressed) or the delivery that counts landed."""
    if not results:
        return True
    required = REQUIRED_ROUTE.get(severity)
    if required and any(r.route == required for r in results):
        return any(r.delivered for r in results if r.route == required)
    return any(r.delivered for r in results)


if __name__ == "__main__":
    sys.exit(main())
