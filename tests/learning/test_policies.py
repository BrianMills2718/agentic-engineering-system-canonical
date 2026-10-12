import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/learning_loop"))
import policies as P  # noqa: E402


def test_unregistered_and_undocumented_rules_are_gaps(tmp_path, monkeypatch, capsys):
    agents = tmp_path / "AGENTS.md"
    agents.write_text("Do this (Policy `read-the-trace`). Do that (Policy `md-file-cap`). Also Policy `root-cause`.\n")
    rules = tmp_path / "WORKING_RULES.md"
    rules.write_text("Policy `root-cause` explained before the section.\n## Sources for AGENTS.md rules\n"
                     "- read-the-trace: Brian said so\n- md-file-cap: Brian said so\n")
    register = tmp_path / "register.yaml"
    register.write_text("schema_version: aes-rules-register/v1\nrules:\n""- id: read-the-trace\n  enforcement_status: enforced\n"
                                             "  feedback_path: policy_friction.md\n- id: other\n  rule: x\n")
    out = tmp_path / "out"
    out.mkdir()
    (out / "reports-2026-10-11.jsonl").write_text(json.dumps({"value": "obs (control) read-the-trace misfired"}) + "\n")
    (out / "reports-2026-08-01.jsonl").write_text(json.dumps({"value": "read-the-trace old"}) + "\n")
    monkeypatch.setattr(P, "AGENTS_MD", agents)
    monkeypatch.setattr(P, "WORKING_RULES", rules)
    monkeypatch.setattr(P, "RULES_REGISTER", register)
    monkeypatch.setattr(P, "OUT", out)
    import datetime as dt
    result = P.check(30, today=dt.date(2026, 10, 12))
    rows = {r["id"]: r for r in result["policies"]}
    assert rows["read-the-trace"] == {"id": "read-the-trace", "documented": True, "registered": True,
                                      "enforcement_status": "enforced", "feedback_path": "policy_friction.md",
                                      "reports": 1}
    # a mention outside the Sources section does not count as documented
    assert rows["root-cause"]["documented"] is False
    assert rows["md-file-cap"]["registered"] is False
    assert sorted(result["gaps"]) == ["md-file-cap", "root-cause"]


def test_default_register_is_the_aes_one():
    assert P.RULES_REGISTER.parts[-3:] == ("docs", "rules", "register.yaml")
    assert "read-the-trace" in P.registry_entries(P.RULES_REGISTER.read_text())
