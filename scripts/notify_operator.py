#!/usr/bin/env python3
"""Tell the operator side of the ecosystem about a condition: CLI + shared stamps.

Why this exists: the daily governance audit once went 25+ days red because its
only channels were logs nobody read. Ecosystem failures need a channel that
reaches whoever can act, without conscripting an unrelated agent session.

WHAT CHANGED 2026-10-06 (issue #1958). This used to raise a Windows ``msg.exe``
dialog ("Message from ..."). That dialog truncated at ~240 characters, could
not be copied, stole focus, and handed Brian things an agent should fix. Brian:
"these should go to an autonomous agent to fix unless my input is actually
needed." The dialog route is deleted. This CLI now forwards to
``operator_notify_router.py``:

- default (``--severity agent``): opens/updates a keyed concern in the agent
  work queue (``concern_issue.py``); Brian is not interrupted.
- ``--severity needs-human`` (or ``--needs-human``): only Brian can act. He
  gets a quiet Windows notification (click opens the full copyable text) and a
  Telegram message -- ``--title`` (what is wrong) and ``--action`` (what to do)
  first, short and plain, then the details from ``--body`` -- once per
  ``--state``; the concern is opened too, labelled ``waiting:brian``.
- ``--resolve --evidence ...``: the condition is fixed; clear the key and close
  the concern, so a later recurrence reaches him again.

This module still owns the rate-limit stamps (``due``/``record_sent``/
``last_state``/``clear_sent``) the router reuses, and the append-only
``history.log`` transcript.

Failure semantics: fail loud. A notification that cannot be delivered exits
non-zero and says why on stderr; it never degrades to a silent no-op.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import operator_notification_record as notification_record

DEFAULT_STAMP_DIR = Path.home() / ".local" / "state" / "operator-notify"


class NotifyError(RuntimeError):
    """Raised when the operator could not be reached. Never swallowed."""


def _stamp_file(stamp_dir: Path, key: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)
    return stamp_dir / f"{safe}.json"


def last_sent(stamp_dir: Path, key: str) -> datetime | None:
    """When this key last reached the operator, or None if never/unreadable."""
    path = _stamp_file(stamp_dir, key)
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return datetime.fromisoformat(raw["last_sent"])
    except (OSError, ValueError, KeyError, TypeError):
        # A corrupt stamp must not suppress a notification. Treating it as
        # "never sent" errs toward reaching the operator, which is the safe
        # direction for this specific tool.
        return None


def record_sent(
    stamp_dir: Path, key: str, now: datetime, state: str | None = None
) -> None:
    stamp_dir.mkdir(parents=True, exist_ok=True)
    payload: dict[str, str] = {"key": key, "last_sent": now.isoformat()}
    if state is not None:
        payload["state"] = state
    _stamp_file(stamp_dir, key).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def last_state(stamp_dir: Path, key: str) -> str | None:
    """The condition (state fingerprint) last delivered for this key, if any.

    Unreadable means None, which errs toward telling the person again.
    """
    path = _stamp_file(stamp_dir, key)
    try:
        value = json.loads(path.read_text(encoding="utf-8")).get("state")
    except (OSError, ValueError, AttributeError):
        return None
    return value if isinstance(value, str) else None


def clear_sent(stamp_dir: Path, key: str) -> None:
    """Forget that this key was delivered: its condition is resolved."""
    _stamp_file(stamp_dir, key).unlink(missing_ok=True)


def due(
    stamp_dir: Path, key: str, min_interval_hours: float, now: datetime
) -> tuple[bool, str]:
    """Is this key allowed to notify now? Returns (allowed, reason)."""
    if min_interval_hours <= 0:
        return True, "no interval configured"
    previous = last_sent(stamp_dir, key)
    if previous is None:
        return True, "never sent"
    elapsed = now - previous
    if elapsed >= timedelta(hours=min_interval_hours):
        return True, f"last sent {elapsed.total_seconds() / 3600:.1f}h ago"
    remaining = timedelta(hours=min_interval_hours) - elapsed
    return False, (
        f"suppressed: sent {elapsed.total_seconds() / 3600:.1f}h ago, "
        f"next in {remaining.total_seconds() / 3600:.1f}h"
    )


def transcript_paths(stamp_dir: Path) -> tuple[Path, Path]:
    """Return the (latest, history) files holding the full notification text.

    ``latest`` is the SHARED record's file, not a private one. Both this module
    and operator_notification_record.py defaulted to
    ~/.local/state/operator-notify/latest.txt and were overwriting each other --
    a collision introduced when the shared record landed. The record owns that
    filename; this module keeps only the append-only history.log, which the
    record does not provide.
    """
    return notification_record.latest_path(stamp_dir), stamp_dir / "history.log"


def write_transcript(
    stamp_dir: Path, key: str, title: str, body: str, now: datetime
) -> Path:
    """Record the full, untruncated notification in the append-only history.

    Written before any delivery is attempted, so the text survives a send that
    fails or is rate-limited.
    """
    stamp_dir.mkdir(parents=True, exist_ok=True)
    latest, history = transcript_paths(stamp_dir)
    entry = f"[{now.isoformat()}] {key}\n{title}\n\n{body}\n"
    with history.open("a", encoding="utf-8") as handle:
        handle.write(entry + "\n")
    # latest.txt is written by the shared record, which main() appends to
    # immediately after this call. Writing it here too would race the canonical
    # copy for the same path.
    return latest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--title", help="first line, names the system")
    parser.add_argument("--body", help="what is wrong and what to do, in full")
    parser.add_argument(
        "--key",
        required=True,
        help="one key per recurring condition; also the concern key",
    )
    parser.add_argument(
        "--severity",
        choices=("agent", "needs-human"),
        default="agent",
        help="agent (default): an agent fixes it. needs-human: only Brian can act.",
    )
    parser.add_argument(
        "--needs-human",
        dest="severity",
        action="store_const",
        const="needs-human",
        help="shorthand for --severity needs-human",
    )
    parser.add_argument(
        "--state",
        help="name of the current condition; needs-human messages once per state",
    )
    parser.add_argument(
        "--action",
        help=(
            "needs-human: one short plain line of what Brian should do. --title is "
            "one short plain sentence of what is wrong; paths and error text go in --body"
        ),
    )
    parser.add_argument(
        "--min-interval-hours",
        type=float,
        default=0.0,
        help="additionally suppress repeats of this key within this window",
    )
    parser.add_argument("--source", default="notify_operator", help="who is reporting")
    parser.add_argument("--stamp-dir", type=Path, default=DEFAULT_STAMP_DIR)
    parser.add_argument(
        "--record-dir",
        type=Path,
        default=None,
        help=(
            "where the shared operator-notification record lives; tests must set "
            "this so they do not append to the operator's real record"
        ),
    )
    parser.add_argument(
        "--resolve",
        action="store_true",
        help="the condition is fixed: clear the key and close its concern",
    )
    parser.add_argument("--evidence", help="with --resolve: how the fix was verified")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report what would be sent and whether the interval allows it",
    )
    args = parser.parse_args(argv)

    import operator_notify_router as router  # lazy: the router imports this module

    if args.resolve:
        if not args.evidence:
            parser.error("--resolve needs --evidence")
        print(f"operator-notify [{args.key}] resolved: "
              f"{router.resolve(key=args.key, evidence=args.evidence, stamp_dir=args.stamp_dir)}")
        return 0
    if not args.title or not args.body:
        parser.error("--title and --body are required unless --resolve")

    now = datetime.now(timezone.utc)
    if args.dry_run:
        fingerprint = router.state_fingerprint(args.title, args.body, args.state)
        allowed, reason = due(args.stamp_dir, args.key, args.min_interval_hours, now)
        if args.severity == "needs-human" and last_state(args.stamp_dir, args.key) == fingerprint:
            allowed, reason = False, "suppressed: this state was already sent"
        verb = "would send" if allowed else "would suppress"
        print(f"operator-notify [{args.key}] {verb} ({reason}) as {args.severity}: {args.title}")
        return 0

    write_transcript(args.stamp_dir, args.key, args.title,
                     f"{args.action}\n\n{args.body}" if args.action else args.body, now)
    try:
        _entry, results = router.notify(
            key=args.key,
            title=args.title,
            body=args.body,
            severity=args.severity,
            source=args.source,
            record_dir=args.record_dir,
            min_interval_hours=args.min_interval_hours,
            stamp_dir=args.stamp_dir,
            state=args.state,
            action=args.action,
        )
    except router.RouterError as exc:
        print(f"operator-notify [{args.key}] REFUSED: {exc}", file=sys.stderr)
        return 2
    for result in results:
        detail = f" ({result.detail})" if result.detail else ""
        print(f"operator-notify [{args.key}] {result.route}: delivered={result.delivered} "
              f"evidence={result.evidence}{detail}")
    if not results:
        print(f"operator-notify [{args.key}] recorded only (suppressed or no route)")
    if not router.delivery_landed(args.severity, results):
        print(f"operator-notify [{args.key}] FAILED: nothing that counts was delivered",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
