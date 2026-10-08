import collections
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/learning_loop"))
import evidence as E
import effects as EF
import feedback_log as FL
import problems as PB


def event(i, ts, link):
    return {"id": i, "kind": "observation", "text": "a failure occurred", "session": i,
            "links": [link], "resolved_links": [link], "provenance": {"ts": ts}}


RECEIPT = {"enforced_at": "2026-10-08T16:00:00Z", "revision": "abc1234", "verification": "o/r#1"}


def test_same_day_before_and_after_events_use_the_full_timestamp():
    morning = event("morning", "2026-10-08T08:00:00Z", {"kind": "path", "ref": "/logs/morning.log:1"})
    evening = event("evening", "2026-10-08T17:00:00Z", {"kind": "path", "ref": "/logs/evening.log:1"})
    row = EF.measure([morning, evening], RECEIPT)
    assert (row["sightings_before"], row["sightings_after"]) == (1, 1)
    assert [r["id"] for r in row["matched_after"]] == ["evening"]


def test_timezone_offsets_compare_as_instants_and_date_only_is_unknown():
    before = event("before", "2026-10-08T12:00:00-04:00", {"kind": "path", "ref": "/logs/at-boundary.log:1"})
    unknown = event("unknown", "2026-10-08", {"kind": "path", "ref": "/logs/unknown.log:1"})
    row = EF.measure([before, unknown], RECEIPT)
    assert (row["sightings_before"], row["sightings_after"], row["unknown_timestamp_records"]) == (1, 0, 1)


def test_restatement_of_a_pre_fix_incident_is_not_a_recurrence():
    a = event("a", "2026-10-08T08:00:00Z", {"kind": "issue", "ref": "o/r#123"})
    b = event("b", "2026-10-08T17:00:00Z", {"kind": "url", "ref": "https://github.com/o/r/issues/123"})
    assert EF.measure([a, b], RECEIPT)["sightings_after"] == 0


def test_closeout_prose_and_closed_dates_are_not_enforcement_receipts():
    assert EF.enforcement_receipt([{"body": "Adopted and enforced today", "createdAt": "2026-10-08T17:00:00Z"}]) is None
    receipt = {"body": EF.MARKER + json.dumps(RECEIPT) + " -->", "createdAt": "2026-10-08T17:00:00Z"}
    assert EF.enforcement_receipt([receipt]) == RECEIPT
    receipt["createdAt"] = "2026-10-08T08:00:00Z"
    assert EF.enforcement_receipt([receipt]) is None


def test_resolution_checks_real_files_lines_and_missing_references(tmp_path):
    log = tmp_path / "run.log"
    log.write_text("first\nsecond\n")
    records = [event("valid", "2026-10-08T08:00:00Z", {"kind": "path", "ref": str(log) + ":2"}),
               event("missing", "2026-10-08T08:00:00Z", {"kind": "path", "ref": str(log) + ":3"})]
    counts = E.resolve_records(records, sqlite3.connect(":memory:"))
    assert counts == {"evidence_resolved": 1, "evidence_unresolved": 1}
    assert E.sightings(records) == [{"valid"}]


def test_github_resolution_rejects_missing_issues_and_routes_org_identity(monkeypatch):
    calls = []
    def run(args, **kwargs):
        calls.append(args)
        return type("Result", (), {"returncode": 1, "stdout": ""})()
    monkeypatch.setattr(E.subprocess, "run", run)
    assert not E.resolve({"kind": "issue", "ref": "Inside-Success/repo#999"})
    assert calls[0][:3] == ["gh-insidesuccess", "api", "repos/Inside-Success/repo/issues/999"]


def test_direct_corrections_enter_the_weekly_reader_without_agent_closeout(tmp_path):
    transcript = tmp_path / "session.jsonl"
    transcript.write_text('{"role":"user","text":"Only change repositories I own."}\n')
    item = {"id": "correction1", "client": "codex", "session_id": "s1", "byte_offset": 0,
            "ts": "2026-10-08T08:00:00Z", "quote": "Only change repositories I own.",
            "speaker": "brian", "source": "llm", "field": "correction", "transcript": str(transcript)}
    reports = FL.correction_reports([item, item])
    assert len(reports) == 1
    record = reports[0]["records"][0]
    assert record["text"] == item["quote"] and record["provenance"]["turn_offset"] == 0
    assert "source:human" in FL.issue_labels(reports[0])
    (tmp_path / "reports-2026-10-08.jsonl").write_text(json.dumps(reports[0]) + "\n")
    loaded = PB.load_records(tmp_path, 3650)
    E.resolve_records(loaded)
    assert [r["text"] for r in loaded] == [item["quote"]]
    assert PB.sightings(loaded) == [{"s1"}]
    assert FL.correction_reports([{**item, "speaker": "agent"}]) == []
    assert FL.correction_reports([{**item, "field": "learning"}]) == []


def test_collector_backfills_and_files_human_corrections_once(tmp_path, monkeypatch):
    import collect_feedback as C
    transcript = tmp_path / "session.jsonl"
    transcript.write_text("a real source remains available\n")
    item = {"id": "old-correction", "client": "codex", "session_id": "s1", "byte_offset": 0,
            "ts": "2026-10-08T08:00:00Z", "quote": "Only change repositories I own.",
            "speaker": "brian", "source": "llm", "field": "correction", "transcript": str(transcript)}
    (tmp_path / f"items-{C.dt.date.today().isoformat()}.jsonl").write_text(json.dumps(item) + "\n")
    monkeypatch.setattr(C, "OUT", tmp_path)
    monkeypatch.setattr(C, "discover", lambda: [])
    monkeypatch.setattr(C, "Register", lambda: type("Register", (), {"ids": []})())
    filed = []
    monkeypatch.setattr(FL, "file_report", lambda r: filed.append(r) or "https://github.com/o/r/issues/1")
    monkeypatch.setattr(sys, "argv", ["collect_feedback", "--file", "--reports-only"])
    assert C.main() == 0
    assert C.main() == 0
    assert [r["value"] for r in filed] == [item["quote"]]


def test_nightly_effects_keep_watching_when_group_id_changes_and_revoke_once(tmp_path, monkeypatch):
    import licences as LC
    monkeypatch.setattr(PB, "OUT", tmp_path)
    monkeypatch.setattr(PB.LI, "question_set", lambda: {})
    monkeypatch.setattr(PB.LI, "api_key", lambda: "unused")
    monkeypatch.setattr(PB, "family", lambda *a: {"families": ["N"], "cost": 0})
    monkeypatch.setattr(PB, "relate", lambda *a: {"relation": "same_problem"})
    monkeypatch.setattr(PB, "concern_enforcement", lambda key: RECEIPT)
    monkeypatch.setattr(PB, "put_view", lambda *a: "https://github.com/o/r/blob/main/VIEW.md")
    external = []
    def run(args, **kwargs):
        external.append(args)
        return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
    monkeypatch.setattr(PB.subprocess, "run", run)
    def row(i, ts):
        log = tmp_path / f"{i}.log"
        log.write_text("the tag was refused\n")
        return event(i, ts, {"kind": "path", "ref": str(log) + ":1"})
    members = [row("r1", "2026-10-08T08:00:00Z"), row("r2", "2026-10-08T09:00:00Z")]
    for r in members:
        r["report_id"] = r["id"]
    fix = {"text": "reject the bad tag", "intent": "Prevent", "rests_on": ["r1", "r2"]}
    analysis = {"cause_chain": [{"text": "the tag is invalid", "basis": "seen", "rests_on": ["r1", "r2"]}],
                "fixes": [fix]}
    db = PB.open_db(tmp_path)
    pid = PB.problem_id(members)
    db.execute("INSERT INTO problem VALUES (?,?,?,?)", (pid, "", "r1,r2", json.dumps(analysis)))
    db.commit()
    db.close()
    path = tmp_path / f"reports-{PB.dt.date.today().isoformat()}.jsonl"
    def write_reports(records):
        with path.open("w") as fh:
            for r in records:
                fh.write(json.dumps({"id": r["id"], "provenance": {"session_id": r["session"], "ts": r["provenance"]["ts"]},
                                     "records": [r]}) + "\n")
    write_reports(members)
    monkeypatch.setattr(sys, "argv", ["problems", "--effects-only", "--file", "--days", "3650"])
    assert PB.main() == 0
    assert not external
    evening = row("000-new", "2026-10-08T17:00:00Z")
    assert PB.problem_id(members + [evening]) != pid
    write_reports(members + [evening])
    assert PB.main() == 0
    assert sum("--occurrence" in args for args in external) == 1
    assert PB.main() == 0
    assert sum("--occurrence" in args for args in external) == 1
    with sqlite3.connect(tmp_path / "problems.sqlite") as db:
        assert db.execute("SELECT count(*) FROM revoked").fetchone()[0] == 1
