"""Filing gate of the feedback collector: only closeout Learnings lines file, and a line already filed
is not filed again (2026-10-07 spot check: 2 of 10 filed entries were exact repeats)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import collect_feedback as C  # noqa: E402


def _item(i, quote, source="closeout", field="Learnings", filing="eligible_not_filed", reusable=0.9):
    return {"id": i, "quote": quote, "source": source, "field": field, "filing": filing,
            "triage": {"kind": "learning", "p": 0.95, "reusable_p": reusable}, "speaker": "agent", "client": "claude",
            "lesson": ""}


def test_only_closeout_learnings_auto_file():
    assert C.AUTO_FILE_SOURCES == {("closeout", "Learnings")}


def test_file_pending_skips_text_already_filed(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "OUT", tmp_path)
    day = tmp_path / "items-2026-10-06.jsonl"
    rows = [
        _item("a", "check   which version a project locks to", filing="lrn-x"),  # filed earlier
        _item("b", "check which version a project locks to"),                    # same text, other session
        _item("c", "a git branch name cannot sit under an existing branch name"),
        _item("d", "narration from the chat", source="llm", field="learning"),   # not an auto-file source
        _item("e", "renamed the third card for this page only", reusable=0.3),  # fails the reusable question
    ]
    day.write_text("".join(json.dumps(r) + "\n" for r in rows))
    filed = []
    monkeypatch.setattr(C, "file_item", lambda it: filed.append(it["id"]) or f"lrn-{it['id']}")
    monkeypatch.setattr(C, "repeats_filed", lambda quote, recent: False)
    n, errors = C.file_pending(day, cap=10)
    assert (n, errors, filed) == (1, [], ["c"])
    updates = [json.loads(l) for l in day.read_text().splitlines() if "filing_update" in l]
    assert {"id": "b", "filing_update": "duplicate_of_filed"} in updates
    assert C.norm(rows[2]["quote"]) in C.filed_quotes()


def test_file_pending_skips_a_reworded_repeat_and_defers_when_the_check_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "OUT", tmp_path)
    day = tmp_path / f"items-{C.dt.date.today().isoformat()}.jsonl"
    rows = [
        _item("a", "Codex on the command line can grade interactive pages; ChatGPT Chat cannot.", filing="lrn-x"),
        _item("b", "Codex grades interactive pages end to end and ChatGPT Chat can't."),  # same lesson, reworded
        _item("c", "Removing the worktree you are in blocks the shell; cd out first."),  # check fails -> deferred
        _item("d", "GitHub's file-editing API turns a linked file into a plain copy."),
    ]
    day.write_text("".join(json.dumps(r) + "\n" for r in rows))

    def fake_repeats(quote, recent):
        assert recent[0].startswith("Codex on the command line")
        if quote.startswith("Removing"):
            raise RuntimeError("model down")
        return quote.startswith("Codex grades")

    filed = []
    monkeypatch.setattr(C, "repeats_filed", fake_repeats)
    monkeypatch.setattr(C, "file_item", lambda it: filed.append(it["id"]) or f"lrn-{it['id']}")
    n, errors = C.file_pending(day, cap=10)
    assert (n, errors, filed) == (1, [], ["d"])
    updates = {u["id"]: u["filing_update"] for u in (json.loads(l) for l in day.read_text().splitlines()) if "filing_update" in u}
    assert updates == {"b": "repeats_filed", "c": "deferred_repeat_check", "d": "lrn-d"}
