"""Anchored citations: `path#:~:text=<quoted text>` names the text a citation points at, so it survives line moves.

A `path:line` citation passes while the file is long enough, even when the cited text has moved. This form
carries the text it expects (the WICG text-fragment syntax, `#:~:text=[prefix-,]text[,-suffix]`, percent-encoded;
the W3C Web Annotation TextQuoteSelector's exact/prefix/suffix). The text must appear exactly once in the file,
runs of whitespace counting as one space; no fuzzy match. A fragment that starts `:~:text=` but cannot be read
is a problem, never a skipped citation. The range form (`text,text`) is not supported and is a problem.

Company Planning's validator holds the same function (`citation_anchor.py`) and the same cases; the plugin is
installed on its own, so the file is held in both repositories and each runs the shared cases
(`tests/lockstep/fixtures/citation_anchor_cases.json`). A change to the rules is made in both.

Implements: lockstep-plan-check/a-citation-may-name-the-text-it-points-at
"""

from __future__ import annotations

import re
from urllib.parse import unquote

DIRECTIVE = ":~:text="


def _norm(text: str) -> str:
    return " ".join(text.split())


def anchor_problem(file_text: str, fragment: str) -> str | None:
    """None when the fragment's text appears exactly once in file_text, else the problem in one sentence."""
    if not fragment.startswith(DIRECTIVE):
        return "malformed anchor: it must start with #:~:text="
    if re.search(r"%(?![0-9A-Fa-f]{2})", fragment):
        return "malformed anchor: a % is not followed by two hex digits"
    parts = fragment[len(DIRECTIVE):].split(",")
    prefix = suffix = ""
    try:
        if len(parts) >= 2 and parts[0].endswith("-"):
            prefix = _norm(unquote(parts.pop(0)[:-1], errors="strict"))
        if len(parts) >= 2 and parts[-1].startswith("-"):
            suffix = _norm(unquote(parts.pop()[1:], errors="strict"))
        if len(parts) != 1:
            return "malformed anchor: the range form text,text is not supported"
        exact = _norm(unquote(parts[0], errors="strict"))
    except UnicodeDecodeError:
        return "malformed anchor: the text is not valid percent-encoded UTF-8"
    if not exact:
        return "malformed anchor: the text is empty"
    body = _norm(file_text)
    hits, start = 0, body.find(exact)
    while start != -1:
        end = start + len(exact)
        before_ok = not prefix or body[:start].rstrip().endswith(prefix)
        after_ok = not suffix or body[end:].lstrip().startswith(suffix)
        hits += before_ok and after_ok
        start = body.find(exact, start + 1)
    if hits == 0:
        return "text not found: the quoted passage is not in the file (moved or edited)"
    if hits > 1:
        return f"text matches {hits} places: add a prefix or suffix to pick one"
    return None
