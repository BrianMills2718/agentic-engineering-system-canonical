"""The pane diagram generator builds D2 from a LikeC4 view's titles, descriptions and arrow labels."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("pane_diagrams", Path(__file__).resolve().parents[1] / "scripts/pane_diagrams.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

VIEW = {"nodes": [{"id": "a", "title": "Planning", "description": {"txt": "Requirements and the order of the units"}},
                  {"id": "b.c", "title": "Lockstep"}],
        "edges": [{"source": "a", "target": "b.c", "label": "the plan"}]}


def test_build_uses_title_wrapped_description_and_arrow_label():
    d2, must = mod.build(VIEW, wrap=20)
    assert 'na: "Planning\\nRequirements and the\\norder of the units"' in d2
    assert 'nb_c: "Lockstep"' in d2 and 'na -> nb_c: "the plan"' in d2
    assert must == ["Planning", "Requirements and the", "order of the units", "Lockstep", "the plan"]
