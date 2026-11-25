import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/learning_loop"))
import policies as P  # noqa: E402


def test_rules_with_no_source_entry_are_gaps(tmp_path, monkeypatch):
    agents = tmp_path / "agents"
    (agents / "topics").mkdir(parents=True)
    (agents / "core.md").write_text("Do this (Policy `read-the-trace`). Also Policy `root-cause`.\n")
    (agents / "topics" / "x.md").write_text("Do that (Policy `md-file-cap`).\n")
    (agents / "rule-sources.md").write_text("## Policy `read-the-trace` — Brian said so\n- md-file-cap: Brian said so\n")
    out = tmp_path / "out"
    out.mkdir()
    (out / "reports-2026-10-11.jsonl").write_text(json.dumps({"value": "obs (control) read-the-trace misfired"}) + "\n")
    (out / "reports-2026-08-01.jsonl").write_text(json.dumps({"value": "read-the-trace old"}) + "\n")
    monkeypatch.setattr(P, "AGENTS_DIR", agents)
    monkeypatch.setattr(P, "OUT", out)
    import datetime as dt
    result = P.check(30, today=dt.date(2026, 10, 12))
    rows = {r["id"]: r for r in result["policies"]}
    assert rows["read-the-trace"] == {"id": "read-the-trace", "documented": True, "reports": 1}
    assert rows["md-file-cap"]["documented"] is True  # named in a topic file
    assert result["gaps"] == ["root-cause"]


def test_default_reads_the_workspace_agents_folder():
    assert P.AGENTS_DIR.parts[-3:] == ("code2", "workspace", "agents")
    assert P._rule_files(P.AGENTS_DIR)[0].name == "core.md"


def test_an_id_inside_a_longer_id_is_not_documented():
    assert P.documented("## Policy `root-cause-over-symptom`", "root-cause") is False
    assert P.documented("## Policy `root-cause` — 2026-11-13", "root-cause") is True
