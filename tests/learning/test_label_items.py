"""Feedback labels: every page of the feedback log is read, and unmatched failures reach an agent."""
import io
import json
import sys
from email.message import Message
from pathlib import Path
from types import SimpleNamespace
from urllib.error import HTTPError
from urllib.response import addinfourl

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import label_items as LI  # noqa: E402

API = "https://api.github.com"
ISSUES = "/repos/o/r/issues?state=open&per_page=100"
OTHERS = "/repos/o/r/issues?state=open&labels=other&per_page=100"


def issue(n, labels):
    return {"number": n, "title": f"report {n}", "body": "", "labels": [{"name": x} for x in labels]}


def response(items, *links):
    body = io.BytesIO(json.dumps(items).encode())
    body.headers = Message()
    for link in links:
        body.headers.add_header("Link", link)
    return body


def fake_github(monkeypatch, pages, posts):
    reads = []

    def open_request(_opener, request, data=None, timeout=None):
        assert request.full_url.startswith(f"{API}/")
        assert request.get_header("Authorization") == "Bearer t"
        path = request.full_url.removeprefix(API)
        if request.get_method() == "POST":
            posts.append((path, json.loads(request.data)))
            return response({})
        reads.append(path)
        page = pages.get(path.removesuffix("&page=1"))
        if page is None:
            raise HTTPError(request.full_url, 422, "Unsupported page number", {}, None)
        if isinstance(page, Exception):
            raise page
        return page

    monkeypatch.setattr(LI.urllib.request.OpenerDirector, "open", open_request)
    return reads


def run_issues(monkeypatch, **options):
    monkeypatch.setattr(LI, "question_set", lambda: {"question": {}, "version": "v2"})
    monkeypatch.setattr(LI, "github_token", lambda: "t")
    monkeypatch.setattr(LI, "ask", lambda state, q: ({"answers": [], "usage": {"cost": 0}}, None, 0.0))
    monkeypatch.setattr(LI, "decide", lambda answers, qs: {
        "outcome": "filed", "families": ["A"], "confident": False, "p": 0.9, "confidence": 0.9,
        "choice": "A", "second": "B"})
    defaults = {"repo": "o/r", "dry_run": False, "summary_issue": 0, "other_concern_repo": "", "max_items": 150}
    args = SimpleNamespace(**(defaults | options))
    return LI.cmd_issues(args)


def test_issues_past_100_pages_are_labelled(monkeypatch):
    paths = [ISSUES] + [f"/repositories/123/issues?state=open&per_page=100&after=abc%2B{n}%3D" for n in range(1, 101)]
    pages = {}
    for index, path in enumerate(paths[:-1]):
        start = 10100 - index * 100
        batch = [issue(n, ["kind:observation", "family:B"]) for n in range(start, start - 100, -1)]
        pages[path] = response(batch, f'<{API}{paths[index + 1]}>; rel="next"')
    # A full last page with only a previous link must terminate the listing.
    pages[paths[-1]] = response(
        [issue(n, ["kind:claim"] if n == 1 else ["problem"]) for n in range(100, 0, -1)],
        f'<{API}{paths[-2]}>; rel="prev"',
    )
    posts = []
    reads = fake_github(monkeypatch, pages, posts)
    assert run_issues(monkeypatch) == 0
    assert reads == paths
    assert [path for path, _ in posts if path.endswith("/labels")] == ["/repos/o/r/issues/1/labels"]


def test_issues_without_a_kind_label_are_skipped(monkeypatch):
    posts = []
    fake_github(monkeypatch, {ISSUES: response([issue(1, ["problem"])])}, posts)
    assert run_issues(monkeypatch) == 0
    assert posts == []


def test_later_page_failure_stops_before_labeling(monkeypatch, capsys):
    next_path = f"{ISSUES}&page=2"
    pages = {
        ISSUES: response([issue(9, ["kind:claim"])], f'<{API}{next_path}>; rel="next"'),
        next_path: HTTPError(f"{API}{next_path}", 503, "Service Unavailable", {}, None),
    }
    posts = []
    reads = fake_github(monkeypatch, pages, posts)
    assert run_issues(monkeypatch) == 2
    result = capsys.readouterr()
    assert reads == [ISSUES, next_path]
    assert posts == [] and result.out == ""
    assert "could not list issues" in result.err and "503" in result.err


@pytest.mark.parametrize(
    ("link", "error"),
    [
        (f'<{API}{ISSUES}>; rel="next"', "repeated"),
        ('<https://api.github.com.example.invalid/issues>; rel="next"', "outside api.github.com"),
        (f'{API}{ISSUES}; rel="next"', "invalid GitHub pagination Link"),
    ],
)
def test_invalid_pagination_stops_without_another_request(monkeypatch, capsys, link, error):
    posts = []
    pages = {ISSUES: response([issue(1, ["kind:claim"])], link)}
    reads = fake_github(monkeypatch, pages, posts)
    assert run_issues(monkeypatch) == 2
    assert reads == [ISSUES] and posts == []
    assert error in capsys.readouterr().err


def test_github_opener_rejects_redirect_outside_api(monkeypatch, capsys):
    requested = []

    def redirect(_handler, request):
        requested.append(request.full_url)
        assert request.full_url == f"{API}{ISSUES}"
        headers = Message()
        headers.add_header("Location", "https://api.github.com.example.invalid/issues")
        reply = addinfourl(io.BytesIO(), headers, request.full_url, 302)
        reply.msg = "Found"
        return reply

    monkeypatch.setattr(LI.urllib.request.HTTPSHandler, "https_open", redirect)
    assert run_issues(monkeypatch) == 2
    assert requested == [f"{API}{ISSUES}"]
    assert "outside api.github.com" in capsys.readouterr().err


def test_one_unmatched_item_opens_no_concern(monkeypatch, capsys):
    import subprocess
    calls = []
    fake_github(monkeypatch, {OTHERS: response([issue(5, ["other"])])}, [])
    monkeypatch.setattr(subprocess, "run", lambda cmd, **k: calls.append(cmd))
    LI.report_others("o/r", "o/skills", "t")
    assert calls == [] and "below 2" in capsys.readouterr().out


def test_two_unmatched_items_open_one_keyed_concern(monkeypatch):
    import subprocess
    calls = []
    next_path = f"{OTHERS}&after=abc"
    reads = fake_github(monkeypatch, {
        OTHERS: response([issue(5, ["other"])], f'<{API}{next_path}>; rel="next"'),
        next_path: response([issue(5, ["other"]), issue(9, ["other"])]),
    }, [])
    monkeypatch.setattr(subprocess, "run", lambda cmd, **k: calls.append(cmd) or
                        SimpleNamespace(returncode=0, stdout="created x", stderr=""))
    LI.report_others("o/r", "o/skills", "t")
    assert reads == [OTHERS, next_path]
    (cmd,) = calls
    assert cmd[cmd.index("--key") + 1] == "taxonomy:unmatched-failures"
    assert cmd[cmd.index("--repo") + 1] == "o/skills"
    assert cmd[cmd.index("--occurrence") + 1] == "5,9"


def test_incomplete_unmatched_listing_opens_no_concern(monkeypatch, capsys):
    import subprocess
    attempt = []
    posts = []
    next_path = f"{OTHERS}&after=abc"
    fake_github(monkeypatch, {
        ISSUES: response([]),
        OTHERS: response([issue(5, ["other"]), issue(9, ["other"])], f'<{API}{next_path}>; rel="next"'),
        next_path: TimeoutError("page timed out"),
    }, posts)
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kw: attempt.append(cmd))
    assert run_issues(monkeypatch, other_concern_repo="o/skills", summary_issue=12) == 2
    assert attempt == [] and posts == []
    assert "could not list unmatched issues" in capsys.readouterr().err


def test_a_run_labels_oldest_unique_issues_up_to_max_items(monkeypatch, capsys):
    posts = []
    next_path = f"{ISSUES}&page=2"
    pull_request = issue(1, ["kind:claim"]) | {"pull_request": {}}
    fake_github(monkeypatch, {
        ISSUES: response([issue(n, ["kind:claim"]) for n in (8, 7, 5, 4)],
                         f'<{API}{next_path}>; rel="next", <{API}{next_path}>; rel="last"'),
        next_path: response([issue(n, ["kind:claim"]) for n in (4, 3, 2)] + [pull_request]),
    }, posts)
    assert run_issues(monkeypatch, max_items=2) == 0
    assert [path for path, _ in posts if path.endswith("/labels")] == [
        "/repos/o/r/issues/2/labels", "/repos/o/r/issues/3/labels",
    ]
    out = capsys.readouterr().out
    assert "6 open kind:* issues" in out and "'deferred_to_next_run': 4" in out


def test_jev_call_goes_through_llm_client_with_its_tags(monkeypatch):
    """The Jev call is llm_client's `call_decisions` (so it lands in the ledger), never a direct HTTP call."""
    import types
    import urllib.request
    calls = []
    raw = {"answers": {"kind": {"choice": "a", "probabilities": {"a": 0.8, "b": 0.2}, "confidence": 0.7}},
           "usage": {"cost": 0.0001}}

    def call_decisions(model, **kw):
        calls.append((model, kw))
        return SimpleNamespace(raw_response=raw)

    fake = types.ModuleType("llm_client")
    fake.call_decisions = call_decisions
    monkeypatch.setitem(sys.modules, "llm_client", fake)
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: (_ for _ in ()).throw(AssertionError("direct HTTP")))
    question = {"kind": {"type": "choice", "instructions": "which?", "criteria": {"a": "A", "b": "B"}}}
    r, err, _ = LI.ask({"learning": "x", "recommended_action": ""}, question)
    assert err is None and r is raw
    ((model, kw),) = calls
    assert model == LI.MODEL and kw["questions"] == question
    assert kw["task"] == "aes.feedback_labels" and kw["trace_id"].startswith("aes.feedback_labels/")
    assert kw["max_budget"] > 0


def test_a_failed_llm_client_call_is_an_error_record(monkeypatch):
    import types

    def call_decisions(model, **kw):
        raise RuntimeError("OpenRouter Decisions API HTTP 503: down")

    fake = types.ModuleType("llm_client")
    fake.call_decisions = call_decisions
    monkeypatch.setitem(sys.modules, "llm_client", fake)
    r, err, _ = LI.ask({"learning": "x"}, {})
    assert r is None and err.startswith("RuntimeError: OpenRouter Decisions API HTTP 503")
