"""The public demo HTTP server: ``AES_DEMO_PUBLIC=1 python -m public_demo.server``.

A default-deny server with exactly these routes and nothing else:

* ``GET  /``                     the one-page demo (``page.html``)
* ``GET  /api/health``           limits, model, whether live model drafts are available
* ``GET  /api/self``             real ``aes`` over a pinned checkout of the AES repository (computed once, cached)
* ``GET  /api/example/goal``     one recorded real model draft plus the real AES verdict on it
* ``POST /api/greeter``          one fixed step of the sample project: ``{"step": "plan|build|change|retest|reset"}``
* ``POST /api/refused``          the real AES refusal of a plan that has no proof (fixed input, no model)
* ``POST /api/goal``             one real model draft of the visitor's goal, judged by real AES: ``{"outcome": "..."}``

Every other path, method, query and file is a 404. The client never names a path, command or code.
Nothing a visitor types is stored; workspaces are throwaway directories removed when the session expires.
"""

from __future__ import annotations

import json
import os
import shutil
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from . import draft, sandbox
from .limits import Config, LimitError, Session, Sessions, public_mode_enabled, scrub_text, set_cookie_header

HERE = Path(__file__).resolve().parent
PAGE_PATH = HERE / "page.html"
EXAMPLE_PATH = HERE / "examples" / "goal.json"
PAGE_CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
            "connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
WORK_ROOT = Path(os.environ.get("AES_DEMO_TMP", "/tmp")) / "aes-demo"


class SelfCache:
    """AES's judgement of its own repository at the pinned checkout: computed once, then served from memory."""

    def __init__(self, root: str | None) -> None:
        self.root = Path(root) if root else None
        self._value: dict[str, Any] | None = None
        self._lock = threading.Lock()

    def get(self) -> dict[str, Any] | None:
        if self.root is None:
            return None
        with self._lock:
            if self._value is None:
                state = sandbox.self_state(self.root)
                state["computed_at"] = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
                self._value = state
            return self._value


def _expire(session: Session) -> None:
    if session.workspace is not None:
        session.workspace.destroy()
        session.workspace = None


def make_handler(sessions: Sessions, self_cache: SelfCache, *, model: str | None = None, live_enabled: bool | None = None,
                 drafter=draft.draft_plan) -> type[BaseHTTPRequestHandler]:
    config = sessions.config
    chosen_model = model or draft.model_name()
    kill_switch = os.environ.get("AES_DEMO_MODEL_EXECUTION", "1").strip()
    if kill_switch not in {"0", "1"}:
        raise ValueError("AES_DEMO_MODEL_EXECUTION must be 0 or 1")
    live_available = live_enabled if live_enabled is not None else (kill_switch == "1" and bool(os.environ.get("OPENROUTER_API_KEY")))
    scrub_roots = [(str(WORK_ROOT) + "/", ""), (str(Path.home()), "~")]
    page_bytes = PAGE_PATH.read_bytes()

    class Handler(BaseHTTPRequestHandler):
        server_version = "AesPublicDemo/1"
        timeout = config.socket_timeout_seconds
        _cookie: str | None = None

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return

        def _send(self, status: int, body: bytes, content_type: str, *, page: bool = False) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            if page:
                self.send_header("Content-Security-Policy", PAGE_CSP)
            if self._cookie:
                self.send_header("Set-Cookie", self._cookie)
            self.end_headers()
            if not getattr(self, "_head_only", False):
                self.wfile.write(body)

        def _json(self, payload: dict[str, Any], status: int = 200) -> None:
            self._send(status, scrub_text(json.dumps(payload), scrub_roots).encode("utf-8"), "application/json; charset=utf-8")

        def _not_found(self) -> None:
            self._json({"ok": False, "error": "Not available in the public demo."}, 404)

        def _session(self) -> Session:
            session, is_new = sessions.resolve(self.headers.get("Cookie"))
            self._cookie = set_cookie_header(session.session_id, config) if is_new else None
            return session

        def _body(self) -> dict[str, Any]:
            try:
                length = int(self.headers.get("Content-Length") or "0")
            except ValueError as exc:
                raise LimitError(400, "Invalid request.") from exc
            if length <= 0 or length > config.max_body_bytes:
                raise LimitError(413, "That request is too large for the public demo.")
            if (self.headers.get("Content-Type") or "").split(";")[0].strip().lower() != "application/json":
                raise LimitError(415, "The public demo only accepts JSON requests.")
            try:
                data = json.loads(self.rfile.read(length).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise LimitError(400, "The request was not valid JSON.") from exc
            if not isinstance(data, dict):
                raise LimitError(400, "The request must be a JSON object.")
            return data

        # ------------------------------------------------------------------ GET
        def do_HEAD(self) -> None:
            self._head_only = True
            try:
                self.do_GET()
            finally:
                self._head_only = False

        def do_GET(self) -> None:
            path = urlparse(self.path).path
            try:
                if path in {"/", "/index.html"}:
                    self._session()
                    self._send(200, page_bytes, "text/html; charset=utf-8", page=True)
                elif path == "/favicon.ico":
                    self._send(204, b"", "image/x-icon")
                elif path == "/api/health":
                    self._json({"ok": True, "model": chosen_model, "live_available": live_available,
                                "goal_runs_per_hour": config.goal_runs_per_session_per_hour, "max_run_budget_usd": config.run_budget_usd,
                                "max_goal_chars": draft.MAX_CHARS, "self_available": self_cache.root is not None})
                elif path == "/api/self":
                    self._session()
                    state = self_cache.get()
                    if state is None:
                        raise LimitError(503, "AES's own project view is not configured on this server.")
                    self._json({"ok": True, "state": state})
                elif path == "/api/example/goal":
                    self._json({"ok": True, **json.loads(EXAMPLE_PATH.read_text())})
                else:
                    self._not_found()
            except LimitError as exc:
                self._json({"ok": False, "error": exc.message}, exc.status)
            except sandbox.SandboxError as exc:
                self._json({"ok": False, "error": exc.message}, exc.status)

        # ------------------------------------------------------------------ POST
        def do_POST(self) -> None:
            path = urlparse(self.path).path
            if path not in {"/api/greeter", "/api/refused", "/api/goal"}:
                self._not_found()
                return
            session: Session | None = None
            claimed = False
            try:
                session = self._session()
                body = self._body()
                if path == "/api/goal":
                    if set(body) - {"outcome"}:
                        raise LimitError(400, "Only the goal text can be sent.")
                    outcome = draft.check_outcome(body.get("outcome"))
                    if not live_available:
                        raise LimitError(503, "Live model drafts are paused right now. The recorded example still works.")
                    sessions.claim(session, "goal")
                    claimed = True
                    started = time.time()
                    plan, usage = drafter(outcome, max_budget=config.run_budget_usd)
                    verdict = sandbox.check_goal(outcome, plan)
                    usage["seconds"] = round(time.time() - started, 1)
                    self._json({"ok": True, "result": verdict, "draft": plan, "usage": usage})
                elif path == "/api/refused":
                    if body:
                        raise LimitError(400, "This step takes no input.")
                    sessions.claim(session, "sandbox")
                    claimed = True
                    self._json({"ok": True, "result": sandbox.refused_proposal_demo()})
                else:
                    if set(body) - {"step"} or not isinstance(body.get("step"), str):
                        raise LimitError(400, "Choose one of the steps.")
                    step = body["step"]
                    if step == "reset":
                        _expire(session)
                        session.done = []
                        self._json({"ok": True, "state": {"done": [], "steps": [{"id": k, "label": v[0]} for k, v in sandbox.GREETER_STEPS.items()]}})
                        return
                    sessions.claim(session, "sandbox")
                    claimed = True
                    if session.workspace is None:
                        session.workspace = sandbox.greeter_init()
                        session.done = []
                    started = time.time()
                    state = sandbox.greeter_step(session.workspace, session.done, step)
                    session.done = state["done"]
                    state["seconds"] = round(time.time() - started, 1)
                    self._json({"ok": True, "state": state})
            except LimitError as exc:
                self._json({"ok": False, "error": exc.message}, exc.status)
            except (draft.DraftError, sandbox.SandboxError) as exc:
                self._json({"ok": False, "error": exc.message}, exc.status)
            except Exception as exc:  # noqa: BLE001 - never a silent 200
                self._json({"ok": False, "error": f"Unexpected {exc.__class__.__name__}. Nothing was made up."}, 500)
            finally:
                if claimed and session is not None:
                    sessions.release(session)

        def _method_not_allowed(self) -> None:
            self._not_found()

        do_PUT = do_PATCH = do_DELETE = _method_not_allowed

    return Handler


def run_public_server(host: str, port: int) -> ThreadingHTTPServer:
    if host not in {"127.0.0.1", "::1", "localhost"} and os.environ.get("AES_DEMO_ALLOW_NONLOCAL_BIND", "").strip() not in {"1", "true"}:
        raise ValueError("public mode binds to loopback only, for a reverse proxy in front; set AES_DEMO_ALLOW_NONLOCAL_BIND=1 to bind elsewhere on purpose")
    shutil.rmtree(WORK_ROOT, ignore_errors=True)
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    os.environ["AES_DEMO_TMP"] = str(WORK_ROOT.parent)
    config = Config.from_env()
    sessions = Sessions(config, on_expire=_expire)
    sessions.start_sweeper()
    cache = SelfCache(os.environ.get("AES_DEMO_SELF_ROOT"))
    if cache.root is not None:
        cache.get()  # compute now so a broken checkout stops the server at start, not at a visitor's click
    server = ThreadingHTTPServer((host, port), make_handler(sessions, cache))
    print(f"http://{host}:{server.server_address[1]}", flush=True)
    print(f"public mode: model={draft.model_name()} per-run budget=${config.run_budget_usd:.3f} goal drafts/visitor/hour="
          f"{config.goal_runs_per_session_per_hour} daily cap={config.goal_daily_cap} concurrent={config.max_concurrent_jobs}", flush=True)
    server.serve_forever()
    return server


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8502)
    args = parser.parse_args()
    if not public_mode_enabled():
        raise SystemExit("set AES_DEMO_PUBLIC=1 to confirm you are starting the PUBLIC demo server")
    run_public_server(args.host, args.port)


if __name__ == "__main__":
    main()
