"""The alias table stays consistent with the native catalogue records."""
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("aliases", Path(__file__).resolve().parents[1] / "scripts/check_capability_aliases.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

PM = {"entries": [{"capability_family_id": "a.x"}, {"capability_family_id": "b.y"}]}
ACA = {"capabilities": {"core": {}}}
CANDS = {"candidates": [{"id": "c1"}]}


def table(*rows):
    return {"aliases": [dict(id=f"r{i}", project_meta_families=f, aca=a) for i, (f, a) in enumerate(rows)]}


def test_complete_table_passes():
    assert mod.problems(table((["a.x"], []), (["b.y"], ["core", "c1"])), PM, ACA, CANDS) == []


@pytest.mark.parametrize("rows,fragment", [
    ((([ "a.x"], []), (["b.y"], ["core"])), "c1"),                     # missing candidate
    ((([ "a.x"], []), (["a.x", "b.y"], ["core", "c1"])), "a.x"),       # family twice
    ((([ "a.x", "zzz"], []), (["b.y"], ["core", "c1"])), "zzz"),       # unknown family
    ((([ "a.x"], []), (["b.y"], ["core", "c1", "nope"])), "nope"),     # unknown ACA id
])
def test_gaps_are_reported(rows, fragment):
    assert any(fragment in p for p in mod.problems(table(*rows), PM, ACA, CANDS))


def test_unreadable_source_fails_closed(tmp_path):
    with pytest.raises(SystemExit) as e:
        mod.load(tmp_path / "missing.yaml")
    assert "cannot read" in str(e.value)
