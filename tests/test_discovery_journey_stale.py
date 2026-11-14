"""Stale-receipt detection for the discovery journey (Q38)."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("dj", Path(__file__).parents[1] / "scripts" / "discovery_journey.py")
dj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dj)


def _receipt(path: Path, record: bool = True) -> dict:
    r = {"sources": [{"source": "catalogue", "path": str(path)}]}
    if record:
        r["source_digests"] = {"catalogue": dj.digest(path)}
    return r


def test_states(tmp_path):
    f = tmp_path / "c.yaml"
    f.write_text("a: 1\n")
    r = _receipt(f)
    assert dj.check_receipt(r)[0]["state"] == "fresh"
    f.write_text("a: 2\n")
    assert dj.check_receipt(r)[0]["state"] == "stale"
    f.unlink()
    assert dj.check_receipt(r)[0]["state"] == "missing"


def test_no_digest_is_never_fresh(tmp_path):
    f = tmp_path / "c.yaml"
    f.write_text("a: 1\n")
    assert dj.check_receipt(_receipt(f, record=False))[0]["state"] == "unrecorded"


def test_cli_exit_codes(tmp_path):
    import json
    f = tmp_path / "c.yaml"
    f.write_text("a: 1\n")
    rec = tmp_path / "r.json"
    rec.write_text(json.dumps(_receipt(f)))
    assert dj.main(["--check-receipt", str(rec)]) == 0
    f.write_text("a: 2\n")
    assert dj.main(["--check-receipt", str(rec)]) == 1
