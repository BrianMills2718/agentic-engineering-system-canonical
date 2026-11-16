#!/usr/bin/env python3
"""Phone push for the feedback loop (ntfy), the only notice the loop sends.

Implements: feedback-loop-notices/attention-push-arrives

Replaces the loop's attention pushes that went through the old Project Meta router (retirement plan, slice 2).
The loop needed one route from it: severity ``attention``, a short push to the operator's phone.
Agent-fixable alerts are concerns (``scripts/concern_issue.py``), not pushes.

A push counts as sent only when ntfy answers 200 with a JSON ``id`` (the broker accepted it);
that is arrival at the broker, not the phone showing it. The topic is read from
``OPERATOR_NTFY_TOPIC`` or that one line of ``~/.secrets/api_keys.env``; it is never printed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from email.header import Header
from pathlib import Path

HOST = "https://ntfy.sh"
TOPIC_ENV = "OPERATOR_NTFY_TOPIC"
SECRETS_ENV = "OPERATOR_SECRETS_FILE"


def topic() -> str:
    """The configured topic, or "" when the route is not set up (never printed)."""
    value = os.environ.get(TOPIC_ENV, "")
    if value:
        return value.strip()
    path = Path(os.environ.get(SECRETS_ENV, str(Path.home() / ".secrets" / "api_keys.env")))
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    for line in lines:
        key, sep, val = line.strip().removeprefix("export ").partition("=")
        if sep and key.strip() == TOPIC_ENV:
            return val.strip().strip("'\"")
    return ""


def push(title: str, body: str, *, host: str = HOST, timeout: float = 15.0, opener=urllib.request.urlopen) -> dict:
    """Send one push; return {"delivered": bool, "evidence": str}. Never raises on network errors."""
    t = topic()
    if not t:
        return {"delivered": False, "evidence": f"not_configured: set {TOPIC_ENV}"}
    # Header values go out as Latin-1; encode other characters as RFC 2047, which ntfy decodes.
    header = title if title.isascii() else Header(title, "utf-8").encode()
    req = urllib.request.Request(f"{host}/{t}", data=body.encode("utf-8"),
                                 headers={"Title": header, "Priority": "default", "Markdown": "no"}, method="POST")
    try:
        with opener(req, timeout=timeout) as resp:
            status, raw = resp.status, resp.read()
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        return {"delivered": False, "evidence": f"send_failed: {type(exc).__name__}"}
    try:
        message_id = json.loads(raw).get("id")
    except (ValueError, AttributeError):
        message_id = None
    if status == 200 and message_id:
        return {"delivered": True, "evidence": f"accepted_by_broker id={message_id}"}
    return {"delivered": False, "evidence": f"send_failed: HTTP {status}, id={'yes' if message_id else 'no'}"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--title", required=True)
    ap.add_argument("--body", required=True)
    result = push(**{k: v for k, v in vars(ap.parse_args(argv)).items()})
    print(json.dumps(result))
    return 0 if result["delivered"] else 1


if __name__ == "__main__":
    sys.exit(main())
