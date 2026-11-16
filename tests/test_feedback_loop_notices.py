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


OK = b'{"ok":true,"result":{"message_id":77}}'


@pytest.fixture(autouse=True)
def clean_env(monkeypatch, tmp_path):
    monkeypatch.setenv("OPERATOR_SECRETS_FILE", str(tmp_path / "none.env"))
    for n in ("TELEGRAM_AGENTS_BOT_TOKEN", "OPERATOR_TELEGRAM_CHAT_ID"):
        monkeypatch.delenv(n, raising=False)


def configure(monkeypatch):
    monkeypatch.setenv("TELEGRAM_AGENTS_BOT_TOKEN", "tok-SECRET")
    monkeypatch.setenv("OPERATOR_TELEGRAM_CHAT_ID", "chat-555")


@pytest.mark.req("feedback-loop-notices/attention-push-arrives")
def test_accepted_message_is_delivered_send_only_and_secrets_not_leaked(monkeypatch):
    configure(monkeypatch)
    seen = []
    def opener(req, timeout):
        seen.append((req.full_url, json.loads(req.data)))
        return Resp(200, OK)
    out = notify.push("Rule handed", "body text", opener=opener)
    assert out["delivered"] and "77" in out["evidence"]
    assert len(seen) == 1 and seen[0][0].endswith("/sendMessage")
    assert "getUpdates" not in seen[0][0] and "deleteWebhook" not in seen[0][0]
    assert seen[0][1] == {"chat_id": "chat-555", "text": "Rule handed\n\nbody text"}
    assert "tok-SECRET" not in json.dumps(out) and "chat-555" not in json.dumps(out)


@pytest.mark.req("feedback-loop-notices/attention-push-arrives")
def test_credentials_read_from_secrets_file_lines(monkeypatch, tmp_path):
    f = tmp_path / "k.env"
    f.write_text("OTHER=x\nexport TELEGRAM_AGENTS_BOT_TOKEN='from-file'\nOPERATOR_TELEGRAM_CHAT_ID=9\n")
    monkeypatch.setenv("OPERATOR_SECRETS_FILE", str(f))
    assert notify.secret("TELEGRAM_AGENTS_BOT_TOKEN") == "from-file" and notify.secret("OPERATOR_TELEGRAM_CHAT_ID") == "9"


@pytest.mark.req("feedback-loop-notices/failed-push-is-not-delivered")
def test_missing_config_network_error_and_bad_answers(monkeypatch):
    assert not notify.push("t", "b")["delivered"]
    configure(monkeypatch)
    def boom(req, timeout): raise urllib.error.URLError("down")
    assert not notify.push("t", "b", opener=boom)["delivered"]
    for body in (b'{"ok":false}', b'{"ok":true,"result":{}}', b"not json"):
        assert not notify.push("t", "b", opener=lambda r, timeout, b=body: Resp(200, b))["delivered"]
    def http401(req, timeout): raise urllib.error.HTTPError("u", 401, "x", None, io.BytesIO(b""))
    assert "401" in notify.push("t", "b", opener=http401)["evidence"]


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


@pytest.mark.req("learnings-register-frozen/register-read-only")
def test_collector_reads_frozen_copy_and_refuses_writes(monkeypatch, tmp_path, capsys):
    import collect_feedback as C
    (tmp_path / "e1.json").write_text(json.dumps({"entry_id": "lrn-1", "lesson": "widgets break when frobbed twice"}))
    (tmp_path / "bad.json").write_text("not json")
    monkeypatch.setattr(C, "LEARNINGS_REGISTER", tmp_path)
    reg = C.Register()
    assert reg.ids == ["lrn-1"]
    with pytest.raises(RuntimeError, match="frozen"):
        C.file_item({"triage": {"kind": "x"}})
    monkeypatch.setattr(sys, "argv", ["collect_feedback.py", "--file", "--legacy-register"])
    with pytest.raises(SystemExit) as e:
        C.main()
    assert "frozen" in str(e.value)
    assert not hasattr(C, "PROJECT_META")
