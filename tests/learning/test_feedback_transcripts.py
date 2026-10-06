"""Synthetic-transcript tests for scripts/learning_loop/transcripts.py (no real transcript text here)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import transcripts as T  # noqa: E402

CLOSEOUT = (
    "Work is merged.\n\n- **Answer** — None asked.\n- **Done** — merged PR 1.\n"
    "- **Policy** — The hook blocked a cd outside the worktree; split the command.\n"
    "- **Concerns** — Closeout lines are lost today.\n"
    "- **Learnings:** None; nothing reusable.\n"
    "- **Decisions** — Recorded lrn-20261006T194133058816Z-b9c6e11156 instead.\n"
    "- **Need anything from human** — No"
)


def write(path: Path, records: list[dict], partial: str = "") -> Path:
    path.write_text("".join(json.dumps(r) + "\n" for r in records) + partial)
    return path


def claude_records():
    return [
        {"type": "user", "entrypoint": "cli", "userType": "external", "sessionId": "s1",
         "timestamp": "2026-10-06T10:00:00Z", "message": {"content": "no, use the shared client"}},
        {"type": "user", "entrypoint": "cli", "isMeta": True, "timestamp": "2026-10-06T10:00:01Z",
         "message": {"content": "Stop hook feedback: closeout missing"}},
        {"type": "user", "entrypoint": "cli", "timestamp": "2026-10-06T10:00:02Z",
         "message": {"content": "<task-notification>done</task-notification>"}},
        {"type": "user", "entrypoint": "cli", "timestamp": "2026-10-06T10:00:03Z",
         "message": {"content": [{"type": "tool_result", "content": "output"}]}},
        {"type": "assistant", "timestamp": "2026-10-06T10:01:00Z",
         "message": {"content": [{"type": "tool_use", "name": "Bash"}, {"type": "text", "text": CLOSEOUT}]}},
        {"type": "assistant", "isSidechain": True, "timestamp": "2026-10-06T10:02:00Z",
         "message": {"content": [{"type": "text", "text": "sidechain text"}]}},
    ]


def test_claude_turns_keep_only_typed_human_text_and_agent_text(tmp_path):
    t = T.read_transcript(write(tmp_path / "s1.jsonl", claude_records()), "claude")
    assert t.interactive and t.session_id == "s1"
    assert [(x.role, x.text[:20]) for x in t.turns] == [("human", "no, use the shared c"), ("agent", CLOSEOUT[:20])]


def test_resume_reads_only_new_complete_lines(tmp_path):
    recs = claude_records()
    p = write(tmp_path / "s1.jsonl", recs[:1], partial='{"type": "assistant"')
    first = T.read_transcript(p, "claude")
    assert len(first.turns) == 1 and first.end_offset == len(json.dumps(recs[0])) + 1
    write(p, recs)
    second = T.read_transcript(p, "claude", offset=first.end_offset)
    assert [x.role for x in second.turns] == ["agent"]
    assert second.turns[0].offset > 0


def test_since_skips_older_records(tmp_path):
    t = T.read_transcript(write(tmp_path / "s1.jsonl", claude_records()), "claude", since="2026-10-06T10:00:30")
    assert [x.role for x in t.turns] == ["agent"]


def test_codex_session_meta_and_injected_context(tmp_path):
    recs = [
        {"type": "session_meta", "payload": {"id": "abc-123", "originator": "codex-tui", "source": "vscode",
                                             "thread_source": "user"}},
        {"timestamp": "2026-10-06T10:00:00Z", "type": "response_item", "payload": {
            "type": "message", "role": "user", "content": [{"type": "input_text", "text": "# AGENTS.md instructions for x"}]}},
        {"timestamp": "2026-10-06T10:00:01Z", "type": "response_item", "payload": {
            "type": "message", "role": "user", "content": [{"type": "input_text", "text": "why did you skip the tests"}]}},
        {"timestamp": "2026-10-06T10:00:02Z", "type": "response_item", "payload": {
            "type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "Running them now."}]}},
    ]
    t = T.read_transcript(write(tmp_path / "rollout-x.jsonl", recs), "codex")
    assert t.session_id == "abc-123" and t.interactive
    assert [(x.role, x.text) for x in t.turns] == [("human", "why did you skip the tests"), ("agent", "Running them now.")]
    recs[0]["payload"]["originator"] = "codex_exec"
    assert not T.read_transcript(write(tmp_path / "rollout-y.jsonl", recs), "codex").interactive


def test_split_closeout_fields_none_and_recorded():
    before, fields = T.split_closeout(CLOSEOUT)
    assert before == "Work is merged."
    assert fields["Policy"].startswith("The hook blocked")
    assert fields["Concerns"] == "Closeout lines are lost today."
    assert T.field_is_none(fields["Learnings"])
    assert not T.field_is_none(fields["Concerns"])
    assert T.already_recorded(fields["Decisions"])


def test_text_with_two_headings_is_not_a_closeout():
    text = "See **Learnings** — and **Concerns** — in the rules."
    assert T.split_closeout(text) == (text, {})
