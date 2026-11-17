#!/usr/bin/env python3
"""The durable record every operator notification writes before it is delivered.

Plan #269 Step 1. This is the piece that makes "one place they all exist" true
even when nothing is delivered.

WHY THIS IS THE RECORD AND NOT THE DELIVERY: on 2026-09-08 Brian received the
daily-audit notification as a Windows message box, could not select its text,
and could only send a screenshot. `msg.exe` renders unselectable text and
truncates at roughly 240 characters, and the audit body is 249 -- so the dialog
showed a clipped message with no way to reach the rest, and the message existed
nowhere else. Separately, WSL->Windows interop was down that same day
(``UtilAcceptVsock: accept4 failed 110``); in that state every desktop route
fails and, before this module, nothing recorded that the operator was never
reached.

Both failures are the same shape: the notification's only copy was its delivery.
(The msg.exe route itself was removed on 2026-10-06, issue #1958; delivery is now
a keyed agent concern by default and Telegram only when Brian must act -- see
operator_notify_router.py.)

CONTRACT: append first, deliver second. A caller writes the record, attempts
delivery, then marks the outcome. A crash, a rate limit, a dismissed dialog, or
a dead transport all leave a complete, readable entry behind. `delivered` is a
tri-state on purpose -- ``None`` means "written, outcome not yet known", which
is distinguishable from a known failure. A notification that reports nothing is
the failure mode this module exists to remove, so there is no state that means
"probably fine".

This is a SOURCE, not a second inbox. `escalation_inbox.py` remains Brian's one
aggregated review surface and reads this record as one of its inputs; adding a
parallel place to look would recreate the problem Plan #269 is closing.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

def _default_record_dir() -> Path:
    """Return the record's home, overridable so a test suite can isolate it.

    The home-directory default is a live-state hazard: three separate times
    while this record was being wired in, tests calling a CLI without an
    explicit override appended junk entries to the operator's REAL record --
    twelve on the first occasion, five on the third, all with the fixture's
    key "k". Each was repaired by adding an override to the one test that
    leaked, and each time another caller was found doing the same.

    Per-test discipline was the wrong layer. ``OPERATOR_NOTIFY_RECORD_DIR`` lets
    conftest redirect the whole suite once, so a test has to work at it to reach
    real state rather than having to remember not to.
    """
    override = os.environ.get("OPERATOR_NOTIFY_RECORD_DIR")
    if override:
        return Path(override)
    return Path.home() / ".local" / "state" / "operator-notify"
RECORD_NAME = "notifications.jsonl"
LATEST_NAME = "latest.txt"

SEVERITIES = ("info", "agent", "needs-human", "attention", "urgent")


class NotificationRecordError(RuntimeError):
    """Raised when the record cannot be written. Never swallowed."""


@dataclass(frozen=True)
class NotificationEntry:
    """One notification, complete and independent of whether it was delivered."""

    id: str
    recorded_at: str
    key: str
    severity: str
    title: str
    body: str
    source: str
    delivered: bool | None
    route: str | None
    failure_reason: str | None

    def render(self) -> str:
        """Return the operator-facing text, untruncated."""
        status = (
            "delivered" if self.delivered
            else "NOT DELIVERED" if self.delivered is False
            else "delivery not yet attempted"
        )
        via = f" via {self.route}" if self.route else ""
        why = f"\nreason: {self.failure_reason}" if self.failure_reason else ""
        return (
            f"[{self.recorded_at}] {self.severity.upper()} {self.key} "
            f"({status}{via}) from {self.source}\n{self.title}\n\n{self.body}{why}\n"
        )


def record_path(record_dir: Path | None = None) -> Path:
    """Return the append-only record file."""
    return (record_dir or _default_record_dir()) / RECORD_NAME


def latest_path(record_dir: Path | None = None) -> Path:
    """Return the human-facing copy of the most recent notification."""
    return (record_dir or _default_record_dir()) / LATEST_NAME


def append(
    *,
    key: str,
    title: str,
    body: str,
    severity: str = "attention",
    source: str = "unknown",
    record_dir: Path | None = None,
    now: datetime | None = None,
) -> NotificationEntry:
    """Write one notification to the record before any delivery is attempted."""
    if severity not in SEVERITIES:
        raise NotificationRecordError(
            f"unsupported severity {severity!r}; expected one of {', '.join(SEVERITIES)}"
        )
    if not key.strip() or not title.strip():
        raise NotificationRecordError("a notification needs a non-empty key and title")

    entry = NotificationEntry(
        id=uuid.uuid4().hex,
        recorded_at=(now or datetime.now(timezone.utc)).isoformat(),
        key=key,
        severity=severity,
        title=title,
        body=body,
        source=source,
        delivered=None,
        route=None,
        failure_reason=None,
    )
    _write(entry, record_dir)
    return entry


def mark_outcome(
    entry: NotificationEntry,
    *,
    delivered: bool,
    route: str,
    failure_reason: str | None = None,
    record_dir: Path | None = None,
) -> NotificationEntry:
    """Append the delivery outcome for an already-recorded notification.

    Appends rather than rewrites: the record is append-only so a partial write
    can never destroy the original entry, which is the only copy of the message.
    """
    if not delivered and not failure_reason:
        raise NotificationRecordError(
            "an undelivered notification must carry a reason; silence is what this "
            "record exists to prevent"
        )
    resolved = NotificationEntry(
        **{**asdict(entry), "delivered": delivered, "route": route,
           "failure_reason": failure_reason}
    )
    _write(resolved, record_dir)
    return resolved


def undelivered(record_dir: Path | None = None) -> list[NotificationEntry]:
    """Return notifications whose latest known state is not delivered.

    Later entries for the same id supersede earlier ones, so a notification that
    failed and was retried successfully does not linger here.
    """
    latest_by_id: dict[str, NotificationEntry] = {}
    for entry in read_all(record_dir):
        latest_by_id[entry.id] = entry
    return [e for e in latest_by_id.values() if e.delivered is not True]


def read_all(record_dir: Path | None = None) -> list[NotificationEntry]:
    """Return every recorded notification, oldest first."""
    path = record_path(record_dir)
    if not path.exists():
        return []
    entries: list[NotificationEntry] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            # A corrupt line must not hide the rest of the record. Skipping it
            # loses one notification; raising would lose every later one too.
            print(f"operator-record: skipping unparseable line in {path}", file=sys.stderr)
            continue
        entries.append(NotificationEntry(**payload))
    return entries


def _write(entry: NotificationEntry, record_dir: Path | None) -> None:
    directory = record_dir or _default_record_dir()
    try:
        directory.mkdir(parents=True, exist_ok=True)
        with record_path(directory).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(entry), sort_keys=True) + "\n")
        latest_path(directory).write_text(entry.render(), encoding="utf-8")
    except OSError as exc:
        raise NotificationRecordError(f"could not write the notification record: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    """Inspect the record from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--undelivered-only",
        action="store_true",
        help="show only notifications that never reached the operator",
    )
    parser.add_argument("--record-dir", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    entries = undelivered(args.record_dir) if args.undelivered_only else read_all(args.record_dir)
    if args.json:
        print(json.dumps([asdict(e) for e in entries], indent=2, sort_keys=True))
        return 0
    if not entries:
        scope = "undelivered notifications" if args.undelivered_only else "notifications"
        print(f"operator-record: no {scope} in {record_path(args.record_dir)}")
        return 0
    for entry in entries:
        print(entry.render())
    return 0


if __name__ == "__main__":
    sys.exit(main())
