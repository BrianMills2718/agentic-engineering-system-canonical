import io, json, sys, urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "learning_loop"))
import notify  # noqa: E402
import alert  # noqa: E402


class Resp:
    def __init__(self, status, body):
        self.status, self._b = status, body
    def read(self): return self._b
    def __enter__(self): return self
    def __exit__(self, *a): return False


@pytest.fixture(autouse=True)
def topic(monkeypatch, tmp_path):
    monkeypatch.setenv("OPERATOR_SECRETS_FILE", str(tmp_path / "none.env"))
    monkeypatch.delenv("OPERATOR_NTFY_TOPIC", raising=False)


@pytest.mark.req("feedback-loop-notices/attention-push-arrives")
def test_accepted_push_is_delivered_and_topic_not_leaked(monkeypatch):
    monkeypatch.setenv("OPERATOR_NTFY_TOPIC", "secret-topic-123")
    seen = {}
    def opener(req, timeout):
        seen["url"], seen["title"] = req.full_url, req.get_header("Title")
        return Resp(200, b'{"id":"abc"}')
    out = notify.push("Rule … handed", "body", opener=opener)
    assert out["delivered"] and "abc" in out["evidence"]
    assert seen["url"].endswith("/secret-topic-123") and seen["title"].startswith("=?utf-8?")
    assert "secret-topic-123" not in json.dumps(out)


@pytest.mark.req("feedback-loop-notices/attention-push-arrives")
def test_topic_read_from_one_secrets_line(monkeypatch, tmp_path):
    f = tmp_path / "k.env"
    f.write_text("OTHER=x\nexport OPERATOR_NTFY_TOPIC='from-file'\n")
    monkeypatch.setenv("OPERATOR_SECRETS_FILE", str(f))
    assert notify.topic() == "from-file"


@pytest.mark.req("feedback-loop-notices/failed-push-is-not-delivered")
def test_no_topic_network_error_and_missing_id(monkeypatch):
    assert not notify.push("t", "b")["delivered"]
    monkeypatch.setenv("OPERATOR_NTFY_TOPIC", "t")
    def boom(req, timeout): raise urllib.error.URLError("down")
    assert not notify.push("t", "b", opener=boom)["delivered"]
    assert not notify.push("t", "b", opener=lambda r, timeout: Resp(200, b"{}"))["delivered"]
    assert not notify.push("t", "b", opener=lambda r, timeout: Resp(200, b"not json"))["delivered"]


@pytest.mark.req("feedback-loop-notices/no-project-meta-path")
def test_loop_scripts_call_no_project_meta_script():
    for name in ("problems.py", "label_items.py", "fix_owner.py", "policies.py", "alert.py", "notify.py"):
        text = (ROOT / "scripts" / "learning_loop" / name).read_text()
        for banned in ("PROJECT_META", "project-meta/scripts", "notify_operator", "operator_notify_router"):
            assert banned not in text, (name, banned)
    # collect_feedback.py still reads and writes the legacy learnings register (a later slice), but sends no notice through it.
    text = (ROOT / "scripts" / "learning_loop" / "collect_feedback.py").read_text()
    assert "notify_operator" not in text and "operator_notify_router" not in text


@pytest.mark.req("feedback-loop-notices/loop-failures-are-concerns")
def test_file_alert_runs_the_aes_concern_adapter():
    calls = []
    class R:  # stands in for subprocess.CompletedProcess
        returncode = 3
    out = alert.file_alert("k-1", "feedback-loop", "T", "B", runner=lambda cmd, **kw: calls.append((cmd, kw)) or R())
    cmd, kw = calls[0]
    assert out == 3 and cmd[1].endswith("scripts/concern_issue.py") and cmd[2] == "open"
    assert cmd[cmd.index("--key") + 1] == "k-1" and cmd[cmd.index("--source") + 1] == "feedback-loop"
    assert "--repo" in cmd and kw["timeout"] == 120
