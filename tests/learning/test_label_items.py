"""Feedback labels: every page of the feedback log is read, and unmatched failures reach an agent."""
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import label_items as LI  # noqa: E402


def issue(n, labels):
    return {"number": n, "title": f"report {n}", "body": "", "labels": [{"name": x} for x in labels]}


def fake_gh(pages, posts):
    def gh(method, path, tok, body=None):
        if method == "POST":
            posts.append((path, body))
            return {}
        page = int(path.rsplit("page=", 1)[1])
        return pages[page - 1] if page <= len(pages) else []
    return gh


def run_issues(monkeypatch, pages, posts):
    monkeypatch.setattr(LI, "question_set", lambda: {"question": {}, "version": "v2"})
    monkeypatch.setattr(LI, "api_key", lambda: "k")
    monkeypatch.setattr(LI, "github_token", lambda: "t")
    monkeypatch.setattr(LI, "gh", fake_gh(pages, posts))
    monkeypatch.setattr(LI, "ask", lambda state, q, key: ({"answers": [], "usage": {"cost": 0}}, None, 0.0))
    monkeypatch.setattr(LI, "decide", lambda answers, qs: {
        "outcome": "filed", "families": ["A"], "confident": False, "p": 0.9, "confidence": 0.9,
        "choice": "A", "second": "B"})
    args = SimpleNamespace(repo="o/r", dry_run=False, summary_issue=0, other_concern_repo="")
    return LI.cmd_issues(args)


def test_issues_past_the_first_page_are_labelled(monkeypatch):
    first = [issue(n, ["kind:observation", "family:B"]) for n in range(1, 101)]
    posts = []
    assert run_issues(monkeypatch, [first, [issue(101, ["kind:claim"])]], posts) == 0
    labelled = {p for p, b in posts if p.endswith("/labels")}
    assert labelled == {"/repos/o/r/issues/101/labels"}


def test_issues_without_a_kind_label_are_skipped(monkeypatch):
    posts = []
    assert run_issues(monkeypatch, [[issue(1, ["problem"])]], posts) == 0
    assert posts == []


def test_one_unmatched_item_opens_no_concern(monkeypatch, capsys):
    import subprocess
    calls = []
    monkeypatch.setattr(LI, "gh", fake_gh([[issue(5, ["other"])]], []))
    monkeypatch.setattr(subprocess, "run", lambda cmd, **k: calls.append(cmd))
    LI.report_others("o/r", "o/skills", "t")
    assert calls == [] and "below 2" in capsys.readouterr().out


def test_two_unmatched_items_open_one_keyed_concern(monkeypatch):
    import subprocess
    calls = []
    monkeypatch.setattr(LI, "gh", fake_gh([[issue(5, ["other"]), issue(9, ["other"])]], []))
    monkeypatch.setattr(subprocess, "run", lambda cmd, **k: calls.append(cmd) or
                        SimpleNamespace(returncode=0, stdout="created x", stderr=""))
    LI.report_others("o/r", "o/skills", "t")
    (cmd,) = calls
    assert cmd[cmd.index("--key") + 1] == "taxonomy:unmatched-failures"
    assert cmd[cmd.index("--repo") + 1] == "o/skills"
    assert cmd[cmd.index("--occurrence") + 1] == "5,9"
