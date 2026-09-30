"""Visitor sessions and limits for the public demo (``AES_DEMO_PUBLIC=1``).

A visitor is an in-memory session keyed by a random, server-issued, HttpOnly cookie. The session carries counters, a
single-job lock and (for the sample project) one throwaway git workspace. The client never names a session, path or
file. Pure policy (no model, no network), so it is unit-testable.
"""

from __future__ import annotations

import os
import re
import secrets
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from http.cookies import CookieError, SimpleCookie
from typing import Any, Callable

COOKIE_NAME = "aes_session"
SESSION_ID = re.compile(r"^[a-f0-9]{32}$")
_SECRET = re.compile(r"(sk-[A-Za-z0-9_\-]{10,}|Bearer\s+[A-Za-z0-9._\-]{16,})")


class LimitError(Exception):
    """A limit or refusal: HTTP status plus one plain sentence."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


def _flag(name: str, default: bool) -> bool:
    raw = (os.environ.get(name) or "").strip().lower()
    if not raw:
        return default
    if raw in {"1", "true"}:
        return True
    if raw in {"0", "false"}:
        return False
    raise ValueError(f"{name} must be 0, 1, true or false (got {raw!r})")


def _num(name: str, default: float, minimum: float, cast: type) -> Any:
    raw = (os.environ.get(name) or "").strip()
    if not raw:
        return default
    try:
        value = cast(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number (got {raw!r})") from exc
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum} (got {raw!r})")
    return value


def public_mode_enabled() -> bool:
    return _flag("AES_DEMO_PUBLIC", False)


@dataclass(frozen=True)
class Config:
    max_sessions: int = 300
    session_ttl_seconds: int = 1800
    max_body_bytes: int = 4096
    run_budget_usd: float = 0.05
    goal_runs_per_session_per_hour: int = 6
    goal_daily_cap: int = 150
    sandbox_runs_per_session_per_hour: int = 80
    max_concurrent_jobs: int = 4
    cookie_secure: bool = True
    socket_timeout_seconds: int = 30

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            max_sessions=_num("AES_DEMO_MAX_SESSIONS", 300, 1, int),
            session_ttl_seconds=_num("AES_DEMO_SESSION_TTL_SECONDS", 1800, 1, int),
            max_body_bytes=_num("AES_DEMO_MAX_BODY_BYTES", 4096, 512, int),
            run_budget_usd=_num("AES_DEMO_RUN_BUDGET", 0.05, 0.001, float),
            goal_runs_per_session_per_hour=_num("AES_DEMO_GOAL_RUNS_PER_SESSION_PER_HOUR", 6, 1, int),
            goal_daily_cap=_num("AES_DEMO_GOAL_DAILY_CAP", 150, 1, int),
            sandbox_runs_per_session_per_hour=_num("AES_DEMO_SANDBOX_RUNS_PER_SESSION_PER_HOUR", 80, 1, int),
            max_concurrent_jobs=_num("AES_DEMO_MAX_CONCURRENT_JOBS", 4, 1, int),
            cookie_secure=_flag("AES_DEMO_COOKIE_SECURE", True),
            socket_timeout_seconds=_num("AES_DEMO_SOCKET_TIMEOUT_SECONDS", 30, 1, int),
        )


@dataclass
class Session:
    session_id: str
    last_seen: float
    goal_times: list[float] = field(default_factory=list)
    sandbox_times: list[float] = field(default_factory=list)
    running: bool = False
    workspace: Any = None  # sandbox.Workspace for the sample project
    done: list[str] = field(default_factory=list)


class Sessions:
    def __init__(self, config: Config, *, clock: Callable[[], float] = time.time,
                 on_expire: Callable[[Session], None] | None = None) -> None:
        self.config = config
        self._clock = clock
        self._on_expire = on_expire
        self._sessions: dict[str, Session] = {}
        self._lock = threading.Lock()
        self._day = ""
        self._day_goal_runs = 0
        self._active = 0

    # -- identity
    def resolve(self, cookie_header: str | None) -> tuple[Session, bool]:
        sid = self._cookie_id(cookie_header)
        now = self._clock()
        with self._lock:
            self._sweep_locked(now)
            if sid and sid in self._sessions:
                found = self._sessions[sid]
                found.last_seen = now
                return found, False
            if len(self._sessions) >= self.config.max_sessions:
                raise LimitError(503, "The demo is full right now. Please try again in a few minutes.")
            session = Session(session_id=secrets.token_hex(16), last_seen=now)
            self._sessions[session.session_id] = session
            return session, True

    @staticmethod
    def _cookie_id(header: str | None) -> str | None:
        if not header:
            return None
        jar: SimpleCookie = SimpleCookie()
        try:
            jar.load(header)
        except CookieError:
            return None
        morsel = jar.get(COOKIE_NAME)
        if morsel is None or not SESSION_ID.fullmatch(morsel.value):
            return None
        return morsel.value

    def sweep(self) -> int:
        with self._lock:
            return self._sweep_locked(self._clock())

    def _sweep_locked(self, now: float) -> int:
        expired = [sid for sid, s in self._sessions.items() if not s.running and now - s.last_seen > self.config.session_ttl_seconds]
        for sid in expired:
            s = self._sessions.pop(sid)
            if self._on_expire:
                self._on_expire(s)
        return len(expired)

    def start_sweeper(self, interval: float = 60.0) -> threading.Thread:
        def loop() -> None:
            while True:
                time.sleep(interval)
                self.sweep()
        t = threading.Thread(target=loop, name="aes-demo-sweeper", daemon=True)
        t.start()
        return t

    def count(self) -> int:
        with self._lock:
            return len(self._sessions)

    # -- jobs
    def claim(self, session: Session, kind: str) -> None:
        """Reserve the visitor's single job slot and count the run, or raise a plain-sentence refusal.

        kind "goal" costs model money (hourly + daily caps); kind "sandbox" is local CPU only (hourly cap)."""
        now = self._clock()
        today = datetime.fromtimestamp(now, timezone.utc).strftime("%Y-%m-%d")
        cfg = self.config
        with self._lock:
            if session.running:
                raise LimitError(409, "Your last step is still running. Wait for it to finish first.")
            if self._active >= cfg.max_concurrent_jobs:
                raise LimitError(503, "Several people are using the demo right now. Try again in a minute.")
            if kind == "goal":
                session.goal_times = [t for t in session.goal_times if now - t < 3600]
                if len(session.goal_times) >= cfg.goal_runs_per_session_per_hour:
                    raise LimitError(429, f"You have used your {cfg.goal_runs_per_session_per_hour} goal drafts for this hour. "
                                          "The recorded example and the sample project still work.")
                if self._day != today:
                    self._day, self._day_goal_runs = today, 0
                if self._day_goal_runs >= cfg.goal_daily_cap:
                    raise LimitError(429, "The demo has reached its daily limit of model drafts. It resets at midnight UTC; "
                                          "the recorded example and the sample project still work.")
                session.goal_times.append(now)
                self._day_goal_runs += 1
            else:
                session.sandbox_times = [t for t in session.sandbox_times if now - t < 3600]
                if len(session.sandbox_times) >= cfg.sandbox_runs_per_session_per_hour:
                    raise LimitError(429, "You have used this hour's steps. Please try again later.")
                session.sandbox_times.append(now)
            session.running = True
            self._active += 1

    def release(self, session: Session) -> None:
        with self._lock:
            if session.running:
                session.running = False
                self._active = max(0, self._active - 1)


def set_cookie_header(session_id: str, config: Config) -> str:
    parts = [f"{COOKIE_NAME}={session_id}", "Path=/", "HttpOnly", "SameSite=Strict", f"Max-Age={config.session_ttl_seconds}"]
    if config.cookie_secure:
        parts.append("Secure")
    return "; ".join(parts)


def scrub_text(text: str, roots: list[tuple[str, str]]) -> str:
    """Remove key-shaped strings and server paths from anything sent to a visitor."""
    for needle, repl in roots:
        text = text.replace(needle, repl)
    return _SECRET.sub("[removed]", text)
