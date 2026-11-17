#!/usr/bin/env python3
"""Make text safe for a GitHub issue anyone may read: home paths, Windows user names, email and IP addresses removed.

Concern issues land in public repositories too (AES #944, #945 carried journal lines with the host name). The patterns
here match the shape of a path or an address, never the meaning of a sentence.

    redact(text)      home folder and other users' home paths to `~`, `C:\\Users\\<name>` to `C:\\Users\\<you>`,
                      email addresses to `<email>`, IPv4 addresses to `<ip>`
    first_line(text)  the first non-empty line, redacted, at most 300 characters

Implements: failed-unit-watch/issue-body-carries-one-line-not-the-log
Implements: project-graph-refresh/concern-body-carries-first-lines-and-log-path
"""
from __future__ import annotations

import re
from pathlib import Path

LIMIT = 300
_UNIX_HOME = re.compile(r"(?<![\w:])/(?:home|Users)/[^/\s:'\"`]+")  # not the /Users/ of C:/Users/
_WINDOWS_HOME = re.compile(r"([A-Za-z]:[\\/]+Users[\\/]+)[^\\/\s:'\"`]+", re.I)
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")


def redact(text: str, home: str | None = None) -> str:
    """Text with the patterns above replaced. `home` defaults to this user's home folder."""
    home = (home or str(Path.home())).rstrip("/")
    out = text.replace(home, "~") if home else text
    out = _WINDOWS_HOME.sub(r"\1<you>", out)
    out = _UNIX_HOME.sub("~", out)
    out = _EMAIL.sub("<email>", out)
    return _IPV4.sub("<ip>", out)


def first_line(text: str, home: str | None = None, limit: int = LIMIT) -> str:
    """The first non-empty line of text, redacted and cut to `limit` characters; `(no output)` when there is none."""
    line = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
    if not line:
        return "(no output)"
    line = redact(line, home)
    return line if len(line) <= limit else line[: limit - 1] + "…"
