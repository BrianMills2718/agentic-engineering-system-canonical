"""Public demo tests: real `aes` for the sandbox, a fake drafter for the model (no spend), real HTTP for the server."""
from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from public_demo import draft, sandbox, server
from public_demo.limits import Config, LimitError, Sessions, scrub_text

DRAFT = {"criteria": [
    {"statement": f"Criterion {i}.", "disproof": "Something fails.", "requirements": [
        {"kind": "deterministic_test", "requirement": "A test passes.", "how": f"tests/test_{i}.py"},
        {"kind": "human_review", "requirement": "A person agrees.", "how": "The product owner reviews it."}]}
    for i in range(3)]}


@pytest.fixture(autouse=True)
def tmp_root(tmp_path, monkeypatch):
    monkeypatch.setenv("AES_DEMO_TMP", str(tmp_path))
    monkeypatch.setattr(server, "WORK_ROOT", tmp_path / "aes-demo")


def test_greeter_lifecycle_uses_real_aes_standings():
    ws = sandbox.greeter_init()
    done: list[str] = []
    seen = []
    for step in ["plan", "build", "change", "retest"]:
        state = sandbox.greeter_step(ws, done, step)
        done = state["done"]
        seen.append(state["criteria"][0]["standing"])
    assert seen == ["INSUFFICIENT", "SUPPORTED", "INSUFFICIENT", "REFUTED"]
    fresh = {o["id"]: o["freshness"] for o in state["observations"]}
    assert sorted(fresh.values()) == ["CURRENT", "STALE"]
    with pytest.raises(sandbox.SandboxError):
        sandbox.greeter_step(ws, done, "plan")  # already run
    ws.destroy()


def test_greeter_enforces_order():
    ws = sandbox.greeter_init()
    with pytest.raises(sandbox.SandboxError) as e:
        sandbox.greeter_step(ws, [], "build")
    assert e.value.status == 409
    ws.destroy()


def test_refused_plan_is_refused_by_real_aes():
    r = sandbox.refused_proposal_demo()
    assert r["accepted"] is False and r["exit"] == 1
    assert any("has no route" in v for v in r["violations"])
    assert r["tree"]["criteria"][0]["requirements"][0]["problems"]


def test_goal_draft_is_accepted_and_all_criteria_unproven():
    r = sandbox.check_goal("A visitor can do the thing quickly on a phone.", DRAFT)
    assert r["accepted"] is True
    assert [c["standing"] for c in r["state"]["criteria"]] == ["INSUFFICIENT"] * 3


def test_goal_draft_with_bad_route_is_refused_not_repaired():
    bad = json.loads(json.dumps(DRAFT))
    bad["criteria"][0]["requirements"][0]["how"] = "../../etc/passwd"
    r = sandbox.check_goal("A visitor can do the thing quickly on a phone.", bad)
    assert r["accepted"] is False and r["violations"]


def test_outcome_validation():
    with pytest.raises(draft.DraftError):
        draft.check_outcome("short")
    with pytest.raises(draft.DraftError):
        draft.check_outcome("x" * 301)
    with pytest.raises(draft.DraftError):
        draft.check_outcome(["not text"])


def test_limits_hourly_daily_and_single_job():
    now = [1000.0]
    s = Sessions(Config(goal_runs_per_session_per_hour=2, goal_daily_cap=3), clock=lambda: now[0])
    a, _ = s.resolve(None)
    s.claim(a, "goal")
    with pytest.raises(LimitError) as e:
        s.claim(a, "goal")
    assert e.value.status == 409  # still running
    s.release(a)
    s.claim(a, "goal"); s.release(a)
    with pytest.raises(LimitError) as e:
        s.claim(a, "goal")
    assert e.value.status == 429
    b, _ = s.resolve(None)
    s.claim(b, "goal"); s.release(b)
    c, _ = s.resolve(None)
    with pytest.raises(LimitError) as e:
        s.claim(c, "goal")
    assert e.value.status == 429  # daily cap across visitors


def test_scrub_removes_keys_and_paths():
    out = scrub_text("x sk-abcdefghijklmnop /srv/x/y Bearer abcdefghijklmnopqrstu", [("/srv/x/", "")])
    assert "sk-" not in out and "Bearer" not in out and "/srv/x/" not in out


@pytest.fixture()
def live_server(tmp_path):
    cfg = Config(cookie_secure=False, goal_runs_per_session_per_hour=1, max_body_bytes=1024)
    sessions = Sessions(cfg)
    calls = []

    def fake(outcome, *, max_budget):
        calls.append(max_budget)
        return DRAFT, {"model": "fake", "trace_id": "t", "calls": 1, "cost_usd": 0.0}

    handler = server.make_handler(sessions, server.SelfCache(None), model=draft.DEFAULT_MODEL, live_enabled=True, drafter=fake)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}", calls
    httpd.shutdown()


def _req(base, path, body=None, method=None, cookie=None, ctype="application/json"):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(base + path, data=data, method=method, headers={"Content-Type": ctype, **({"Cookie": cookie} if cookie else {})})
    try:
        with urllib.request.urlopen(r) as resp:
            return resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers


def test_default_deny_and_headers(live_server):
    base, _ = live_server
    for path in ["/docs", "/openapi.json", "/redoc", "/api/nope", "/.git/config", "/../etc/passwd", "/page.html", "/public_demo/server.py", "/api/greeter"]:
        code, _, _ = _req(base, path)
        assert code == 404, path
    for method in ["PUT", "DELETE", "PATCH"]:
        assert _req(base, "/api/goal", {}, method=method)[0] == 404
    code, body, hdr = _req(base, "/")
    assert code == 200 and b"AES" in body and "Content-Security-Policy" in hdr and "HttpOnly" in hdr["Set-Cookie"]
    assert _req(base, "/api/goal", {"outcome": "x" * 40, "path": "/etc"})[0] == 400  # extra field refused
    assert _req(base, "/api/goal", {"outcome": "x" * 2000})[0] == 413
    assert _req(base, "/api/goal", {"outcome": "x" * 40}, ctype="text/plain")[0] == 415
    assert _req(base, "/api/greeter", {"step": "rm -rf /"})[0] == 400


def test_goal_flow_then_429_and_no_secrets(live_server):
    base, calls = live_server
    code, body, hdr = _req(base, "/")
    cookie = hdr["Set-Cookie"].split(";")[0]
    code, body, _ = _req(base, "/api/goal", {"outcome": "A visitor can do the thing quickly on a phone."}, cookie=cookie)
    j = json.loads(body)
    assert code == 200 and j["ok"] and j["result"]["accepted"] and calls == [0.05]
    code, body, _ = _req(base, "/api/goal", {"outcome": "A visitor can do the thing quickly on a phone."}, cookie=cookie)
    assert code == 429 and "goal drafts" in json.loads(body)["error"]
    assert len(calls) == 1
    code, body, _ = _req(base, "/api/goal", {"outcome": "hi"}, cookie=cookie)
    assert code == 400


def test_greeter_over_http_and_refusal(live_server):
    base, _ = live_server
    cookie = _req(base, "/")[2]["Set-Cookie"].split(";")[0]
    for step, standing in [("plan", "INSUFFICIENT"), ("build", "SUPPORTED")]:
        code, body, _ = _req(base, "/api/greeter", {"step": step}, cookie=cookie)
        assert code == 200 and json.loads(body)["state"]["criteria"][0]["standing"] == standing
    code, body, _ = _req(base, "/api/greeter", {"step": "plan"}, cookie=cookie)
    assert code == 409
    assert _req(base, "/api/greeter", {"step": "reset"}, cookie=cookie)[0] == 200
    code, body, _ = _req(base, "/api/refused", {}, cookie=cookie)
    assert code == 200 and json.loads(body)["result"]["accepted"] is False
