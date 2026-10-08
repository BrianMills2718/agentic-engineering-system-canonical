"""Read Claude Code and Codex transcripts as plain turns, and split closeout fields.

Pure standard library, no LLM: collect_feedback.py imports it, and the tests use
it on synthetic transcripts. Only structure is parsed here (record types, the
fixed bold closeout headings); meaning is left to the LLM and Jev steps.

Claude Code: ~/.claude/projects/<project>/<session>.jsonl (subagent transcripts in
<session>/subagents/ are not read: their "user" turns are the parent agent).
Codex: ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl, a session_meta record first.
Both are append-only JSONL, so a byte offset is a safe resume point.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

# Text that arrives as a "user" turn but was not typed by a person.
_NOT_HUMAN_PREFIXES = (
    "<task-notification", "<local-command", "<command-", "<system-reminder",
    "This session is being continued", "[Request interrupted", "Caveat:",
    "# AGENTS.md instructions", "<environment_context", "<user_instructions",
    "<INSTRUCTIONS>", "<turn_aborted", "<realtime_delegation", "<send_user_message_question_reply",
)

# Closeout headings from the workspace AGENTS.md "Persist and close" format.
CLOSEOUT_HEADINGS = (
    "Answer", "Session goal", "Active subgoals", "Done", "Verification", "Policy",
    "Concerns", "Feedback", "Learnings", "Decisions", "Recommended next", "Need anything from human",
)  # "Feedback" replaced "Learnings" on 2026-10-07; both are read (feedback_log.REPORT_FIELDS)
COLLECTED_FIELDS = ("Learnings", "Concerns", "Policy", "Decisions")
_HEADING_RE = re.compile(
    r"^[ \t]*(?:[-*][ \t]+)?\*\*(" + "|".join(re.escape(h) for h in CLOSEOUT_HEADINGS)
    + r")(?::\*\*|\*\*[ \t]*(?:[:—–-][ \t]*)?)", re.M)
# A register entry id or path means the learning was already recorded by the `learned` skill.
_RECORDED_RE = re.compile(r"lrn-\d{8}T\d{6}|learnings/entries/")
_NONE_RE = re.compile(r"^[`*_ ]*none\b", re.I)


@dataclass
class Turn:
    role: str            # "human" or "agent"
    text: str
    ts: str
    offset: int          # byte offset of the record in the transcript file
    cwd: str = ""        # working directory the session was in when the turn was written


@dataclass
class Transcript:
    path: str
    client: str          # "claude" or "codex"
    session_id: str
    interactive: bool    # a person typed in it (Claude cli entrypoint; Codex non-exec, non-subagent)
    turns: list[Turn] = field(default_factory=list)
    end_offset: int = 0
    bad_lines: int = 0
    cwd: str = ""        # latest working directory seen


def _texts(content, kinds: tuple[str, ...]) -> list[str]:
    if isinstance(content, str):
        return [content]
    if isinstance(content, list):
        return [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") in kinds]
    return []


def is_human_text(text: str) -> bool:
    s = text.lstrip()
    return bool(s) and not s.startswith(_NOT_HUMAN_PREFIXES)


def read_transcript(path: Path, client: str, offset: int = 0, since: str = "") -> Transcript:
    """Turns from byte `offset` on (only complete lines), skipping records older than `since` (ISO)."""
    t = Transcript(str(path), client, path.stem, interactive=False, end_offset=offset)
    if client == "codex":
        t.session_id = path.stem[-36:]
    with open(path, "rb") as fh:
        if client == "codex":  # session metadata is always the first line, even when resuming
            try:
                meta = json.loads(fh.readline()).get("payload", {})
                t.session_id = meta.get("id") or t.session_id
                t.cwd = str(meta.get("cwd") or "")
                t.interactive = meta.get("originator") != "codex_exec" and meta.get("thread_source") != "subagent" \
                    and not isinstance(meta.get("source"), dict)
            except ValueError:
                pass
        fh.seek(offset)
        for raw in fh:
            if not raw.endswith(b"\n"):
                break  # a line still being written; read it next run
            at = t.end_offset
            t.end_offset += len(raw)
            try:
                d = json.loads(raw)
            except ValueError:
                t.bad_lines += 1
                continue
            ts = str(d.get("timestamp") or "")
            if client == "claude" and d.get("cwd"):
                t.cwd = str(d["cwd"])
            for role, text in (_claude(d, t) if client == "claude" else _codex(d)):
                if since and ts and ts < since:
                    continue
                t.turns.append(Turn(role, text, ts, at, t.cwd))
    return t


def _claude(d: dict, t: Transcript):
    if d.get("isSidechain") or d.get("type") not in ("user", "assistant"):
        return
    if d.get("sessionId"):
        t.session_id = d["sessionId"]
    msg = d.get("message") if isinstance(d.get("message"), dict) else {}
    if d["type"] == "assistant":
        for text in _texts(msg.get("content"), ("text",)):
            if text.strip():
                yield "agent", text
        return
    if d.get("entrypoint") == "cli":
        t.interactive = True
    if d.get("isMeta") or d.get("userType", "external") != "external":
        return
    for text in _texts(msg.get("content"), ("text",)):
        if is_human_text(text):
            yield "human", text


def _codex(d: dict):
    p = d.get("payload") if isinstance(d.get("payload"), dict) else {}
    if d.get("type") != "response_item" or p.get("type") != "message":
        return
    if p.get("role") == "assistant":
        for text in _texts(p.get("content"), ("output_text",)):
            if text.strip():
                yield "agent", text
    elif p.get("role") == "user":
        for text in _texts(p.get("content"), ("input_text",)):
            if is_human_text(text):
                yield "human", text


def split_closeout(text: str) -> tuple[str, dict[str, str]]:
    """(text before the closeout, {heading: value}) when `text` holds at least 3 closeout headings."""
    hits = list(_HEADING_RE.finditer(text))
    if len({m.group(1) for m in hits}) < 3:
        return text, {}
    fields: dict[str, str] = {}
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        fields.setdefault(m.group(1), text[m.end():end].strip())
    return text[:hits[0].start()].rstrip(), fields


def field_is_none(value: str) -> bool:
    return bool(_NONE_RE.match(value))


def already_recorded(value: str) -> bool:
    return bool(_RECORDED_RE.search(value))
