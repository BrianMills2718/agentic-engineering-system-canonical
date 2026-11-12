"""Tests for turning the LikeC4 diagram into import-linter contracts."""

import pytest

from lockstep.checks.arch import contracts_from_model, render

MODEL = {
    "elements": {
        "cli": {"id": "cli", "metadata": {"python": "app.cli"}},
        "detect": {"id": "detect", "metadata": {"python": "app.detect"}},
        "apply": {"id": "apply", "metadata": {"python": "app.apply"}},
        "docs": {"id": "docs"},
    },
    "relations": {
        "r1": {"source": {"model": "cli"}, "target": {"model": "detect"}},
        "r2": {"source": {"model": "cli"}, "target": {"model": "apply"}},
    },
}


@pytest.mark.req("lockstep-checks/arch-missing-arrow-forbids-the-import")
def test_missing_arrow_forbids_the_import():
    forbidden = contracts_from_model(MODEL)
    assert forbidden == {
        "app.apply": ["app.cli", "app.detect"],
        "app.cli": [],
        "app.detect": ["app.apply", "app.cli"],
    }


@pytest.mark.req("lockstep-checks/arch-diagram-changed-without-regenerating")
def test_diagram_changed_without_regenerating():
    old = render(contracts_from_model(MODEL), root="app")
    changed = {**MODEL, "relations": {**MODEL["relations"],
               "r3": {"source": {"model": "detect"}, "target": {"model": "apply"}}}}
    new = render(contracts_from_model(changed), root="app")
    assert old != new
    assert "app.apply" not in new.split("[importlinter:contract:app.detect]")[1].split("[")[0]


@pytest.mark.slow  # runs LikeC4 through npx (network or npx cache)
@pytest.mark.req("lockstep-checks/arch-invalid-diagram-stops-generation")
def test_invalid_diagram_stops_generation(tmp_path):
    from lockstep.checks.arch import export_model

    arch = tmp_path / "docs" / "architecture"
    arch.mkdir(parents=True)
    (arch / "model.c4").write_text(
        "specification {\n  element component\n}\n"
        "model {\n"
        "  cli = component 'Command line'\n"
        "  views = component 'Views'\n"
        "  cli -> views 'shows'\n"
        "}\n"
    )
    with pytest.raises(RuntimeError, match="Invalid"):
        export_model(tmp_path)
