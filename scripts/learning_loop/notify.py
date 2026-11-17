#!/usr/bin/env python3
"""Phone notice for the feedback loop: one Telegram message, the only notice the loop sends.

Implements: feedback-loop-notices/attention-push-arrives

Replaces the loop's attention pushes that went through the old Project Meta router (retirement plan, slice 2).
Agent-fixable alerts are concerns (``scripts/learning_loop/alert.py``), not messages.

Uses Telegram's ``sendMessage`` only. The bot's webhook belongs to another service (Paperclip), so this never
calls ``getUpdates`` or ``deleteWebhook``, which would break it. Plain text, no parse mode. A message counts as
delivered only when Telegram answers ``ok`` with a ``message_id`` (Telegram holds it for the account; that is not
the phone showing it). The token and chat id come from the environment or those two lines of
``~/.secrets/api_keys.env``; neither is ever printed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.telegram.org"
TOKEN_ENV = "TELEGRAM_AGENTS_BOT_TOKEN"
CHAT_ENV = "OPERATOR_TELEGRAM_CHAT_ID"
SECRETS_ENV = "OPERATOR_SECRETS_FILE"
MAX_CHARS = 4000


def secret(name: str) -> str:
    """The named value from the environment, else from that one line of the secrets file, else ""."""
    value = os.environ.get(name, "")
    if value:
        return value.strip()
    path = Path(os.environ.get(SECRETS_ENV, str(Path.home() / ".secrets" / "api_keys.env")))
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    for line in lines:
        key, sep, val = line.strip().removeprefix("export ").partition("=")
        if sep and key.strip() == name:
            return val.strip().strip("'\"")
    return ""


def push(title: str, body: str, *, host: str = API, timeout: float = 15.0, opener=urllib.request.urlopen,
         no_preview: bool = False) -> dict:
    """Send one message; return {"delivered": bool, "evidence": str} plus "message_id" when delivered.

    Never raises on network errors. ``no_preview`` turns off Telegram's link preview card (for a body that is a
    link, as the waiting-issue push sends). An HTTP error carries Telegram's own description, token removed.

    Implements: feedback-loop-notices/link-preview-off-on-request
    """
    token, chat = secret(TOKEN_ENV), secret(CHAT_ENV)
    if not token or not chat:
        missing = [n for n, v in ((TOKEN_ENV, token), (CHAT_ENV, chat)) if not v]
        return {"delivered": False, "evidence": f"not_configured: set {', '.join(missing)}"}
    text = f"{title}\n\n{body}"[:MAX_CHARS]
    payload = {"chat_id": chat, "text": text}
    if no_preview:
        payload["disable_web_page_preview"] = True
    req = urllib.request.Request(f"{host}/bot{token}/sendMessage",
                                 data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with opener(req, timeout=timeout) as resp:
            status, raw = resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        try:
            description = str(json.loads(exc.read().decode("utf-8")).get("description", ""))[:200]
        except (ValueError, OSError, AttributeError):
            description = ""
        return {"delivered": False, "evidence": f"send_failed: HTTP {exc.code} {description}".strip().replace(token, "<token>")}
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        return {"delivered": False, "evidence": f"send_failed: {type(exc).__name__}"}
    try:
        answer = json.loads(raw)
        ok, message_id = answer.get("ok") is True, (answer.get("result") or {}).get("message_id")
    except (ValueError, AttributeError):
        ok, message_id = False, None
    if status == 200 and ok and message_id:
        return {"delivered": True, "evidence": f"accepted_by_telegram message_id={message_id}", "message_id": message_id}
    return {"delivered": False, "evidence": f"send_failed: HTTP {status}, ok={ok}, message_id={'yes' if message_id else 'no'}"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--title", required=True)
    ap.add_argument("--body", required=True)
    result = push(**vars(ap.parse_args(argv)))
    print(json.dumps(result))
    return 0 if result["delivered"] else 1


if __name__ == "__main__":
    sys.exit(main())
