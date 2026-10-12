import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import collect_feedback as CF  # noqa: E402


def _line(rid, filing, records):
    return json.dumps({"id": rid, "filing": filing, "records": records, "run_id": "x"}) + "\n"


def test_a_deferred_report_reuses_its_last_clean_split(tmp_path):
    """A report the filing cap deferred keeps the records it was first split into: re-splitting with
    the light model can parse it differently, giving one record id two payloads (project-meta #2538)."""
    first = [{"id": "rec-1", "kind": "observation", "text": "first parse"}]
    later = [{"id": "rec-1", "kind": "observation", "text": "second parse"}]
    (tmp_path / "reports-2026-10-10.jsonl").write_text(_line("rep-a", "deferred_cap", first)
                                                         + _line("rep-b", "split_failed", []))
    (tmp_path / "reports-2026-10-11.jsonl").write_text(_line("rep-a", "deferred_cap", later)
                                                         + _line("rep-c", "https://x/1", first))
    got = CF.earlier_splits({"rep-a", "rep-b", "rep-d"}, tmp_path)
    assert got == {"rep-a": first}  # the first clean split wins; a failed split and unseen ids are not reused


def test_no_earlier_files_means_nothing_reused(tmp_path):
    assert CF.earlier_splits({"rep-a"}, tmp_path) == {}
