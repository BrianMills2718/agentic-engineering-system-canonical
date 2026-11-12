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


# --- the code is checked against the committed contracts, not only the contracts against the diagram ---

import lockstep.checks.arch as arch_mod
from lockstep.checks.cli import run as run_check
from lockstep_checks_support import write, repo  # noqa: F401  (fixture)

CONTRACTS = render(contracts_from_model(MODEL), root="app")


def _app(repo, detect_source):
    write(repo, "src/app/__init__.py", "")
    write(repo, "src/app/cli.py", "from app.detect import greet\n")
    write(repo, "src/app/apply.py", "")
    write(repo, "src/app/detect.py", detect_source)
    write(repo, ".importlinter", CONTRACTS)
    # the diagram check is not under test here: pretend the committed file is current
    return repo


@pytest.fixture
def fresh(monkeypatch):
    monkeypatch.setattr(arch_mod, "generate", lambda root, likec4=arch_mod.LIKEC4: CONTRACTS)


@pytest.mark.req("lockstep-checks/arch-an-import-the-diagram-forbids-is-refused")
def test_an_import_the_diagram_forbids_is_refused(repo, fresh, capsys):
    _app(repo, "from app.cli import greet\n")
    assert run_check(["arch", "check", "--repo", str(repo)]) == 1
    out = capsys.readouterr().out
    assert "app.detect" in out and "app.cli" in out and "BROKEN" in out


@pytest.mark.req("lockstep-checks/arch-an-import-the-diagram-forbids-is-refused")
def test_code_that_follows_the_diagram_is_accepted(repo, fresh, capsys):
    _app(repo, "def greet():\n    return 'hello'\n")
    assert run_check(["arch", "check", "--repo", str(repo)]) == 0
    assert "exit=0" in capsys.readouterr().out


@pytest.mark.req("lockstep-checks/arch-missing-import-linter-fails-loudly")
def test_a_missing_import_linter_fails_loudly(repo, fresh, monkeypatch, capsys):
    _app(repo, "def greet():\n    return 'hello'\n")
    monkeypatch.setattr(arch_mod, "lint_imports_command", lambda: None)
    assert run_check(["arch", "check", "--repo", str(repo)]) == 1
    assert "import-linter is not installed" in capsys.readouterr().out
