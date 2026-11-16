import io, json, sys, urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "learning_loop"))
import notify  # noqa: E402


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
def test_loop_scripts_name_no_project_meta_script():
    for name in ("problems.py", "label_items.py"):
        text = (ROOT / "scripts" / "learning_loop" / name).read_text()
        assert "project-meta/scripts" not in text and 'PROJECT_META /' not in text, name
