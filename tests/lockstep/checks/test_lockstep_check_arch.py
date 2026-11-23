"""Tests for turning the LikeC4 diagram into import-linter contracts."""

import subprocess

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


@pytest.mark.req("lockstep-checks/arch-a-diagram-that-maps-no-packages-passes")
def test_a_diagram_that_maps_no_packages_passes_without_running_import_linter(tmp_path, monkeypatch):
    """code2-workspace's diagram maps no Python packages: there is nothing to check, so the check passes.

    Before the fix import-linter crashed on the empty `root_packages =` and Lockstep counted that as one broken
    contract (reported by the code-88 session, 2026-11-12).
    """
    from lockstep.checks import arch as arch_mod

    (tmp_path / ".importlinter").write_text(arch_mod.HEADER + "[importlinter]\nroot_packages =\n")
    monkeypatch.setattr(arch_mod, "lint_imports_command", lambda: (_ for _ in ()).throw(AssertionError("ran")))
    broken, report = arch_mod.lint_imports(tmp_path)
    assert broken == 0
    assert "no contracts" in report


# --- a LikeC4 that could not run is a tool failure, not a verdict on the diagram ---

# npm's own output when it cannot write its cache: the 2026-11-18 nightly failure in enforced-planning,
# which `invalid_diagram=1` made look like a broken diagram (BRI-118).
NPM_EACCES = (
    "npm error code EACCES\n"
    "npm error syscall mkdir\n"
    "npm error path /home/node/.npm/_cacache\n"
    "npm error Your cache folder contains root-owned files, due to a bug in previous versions of npm\n"
)
LIKEC4_INVALID = "ERROR likec4 Invalid /repo/docs/architecture/model.c4\n    Line 5: Expecting token of type '}'\n"


def _npx(monkeypatch, validate: subprocess.CompletedProcess, version: subprocess.CompletedProcess):
    """Make npx present and answer `validate` and `--version` with the given results."""
    monkeypatch.setattr(arch_mod.shutil, "which", lambda name: f"/usr/bin/{name}")

    def run(command, *args, **kwargs):
        assert command[:3] == ["npx", "--yes", arch_mod.LIKEC4], command
        return version if command[3:] == ["--version"] else validate

    monkeypatch.setattr(arch_mod.subprocess, "run", run)


@pytest.mark.req("lockstep-checks/arch-a-missing-npx-is-a-tool-failure")
def test_a_missing_npx_is_a_tool_failure(repo, monkeypatch, capsys):
    monkeypatch.setattr(arch_mod.shutil, "which", lambda name: None)
    monkeypatch.setattr(arch_mod.subprocess, "run", lambda *a, **k: pytest.fail("npx was run anyway"))
    assert run_check(["arch", "check", "--repo", str(repo)]) == 1
    out = capsys.readouterr().out
    assert "RESULT arch-check tool_unavailable=1 exit=1" in out
    assert "invalid_diagram" not in out
    assert "npx is not installed" in out


@pytest.mark.req("lockstep-checks/arch-a-likec4-that-cannot-start-is-a-tool-failure")
def test_a_likec4_that_cannot_start_is_a_tool_failure(repo, monkeypatch, capsys):
    # npm fails before LikeC4 runs, so `--version` fails too: nothing was learned about the diagram.
    _npx(monkeypatch,
         validate=subprocess.CompletedProcess([], 1, "", NPM_EACCES),
         version=subprocess.CompletedProcess([], 1, "", NPM_EACCES))
    assert run_check(["arch", "check", "--repo", str(repo)]) == 1
    out = capsys.readouterr().out
    assert "RESULT arch-check tool_unavailable=1 exit=1" in out
    assert "invalid_diagram" not in out
    assert "root-owned files" in out  # npm's own report is carried through


@pytest.mark.req("lockstep-checks/arch-a-failing-diagram-export-is-a-tool-failure")
def test_a_failing_json_export_is_a_tool_failure(repo, monkeypatch, capsys):
    # The diagram validated, so a failing export is the tool's problem, not the diagram's.
    _npx(monkeypatch,
         validate=subprocess.CompletedProcess([], 0, "", ""),
         version=subprocess.CompletedProcess([], 0, "1.60.0\n", ""))

    def run(command, *args, **kwargs):
        exported = "export" in command
        return subprocess.CompletedProcess(command, 1 if exported else 0, "", "out of memory\n" if exported else "")

    monkeypatch.setattr(arch_mod.subprocess, "run", run)
    assert run_check(["arch", "check", "--repo", str(repo)]) == 1
    out = capsys.readouterr().out
    assert "RESULT arch-check tool_unavailable=1 exit=1" in out
    assert "invalid_diagram" not in out


@pytest.mark.req("lockstep-checks/arch-invalid-diagram-stops-generation")
def test_an_invalid_diagram_is_still_an_invalid_diagram(repo, monkeypatch, capsys):
    # LikeC4 ran (`--version` works), so its non-zero validate is a verdict on the diagram.
    _npx(monkeypatch,
         validate=subprocess.CompletedProcess([], 1, LIKEC4_INVALID, ""),
         version=subprocess.CompletedProcess([], 0, "1.60.0\n", ""))
    assert run_check(["arch", "check", "--repo", str(repo)]) == 1
    out = capsys.readouterr().out
    assert "RESULT arch-check invalid_diagram=1 exit=1" in out
    assert "tool_unavailable" not in out


@pytest.mark.slow  # runs LikeC4 through npx (network or npx cache)
@pytest.mark.req("lockstep-checks/arch-invalid-diagram-stops-generation")
def test_a_real_invalid_diagram_reports_invalid_diagram(repo, capsys):
    write(repo, "docs/architecture/model.c4",
          "specification {\n  element component\n}\n"
          "model {\n"
          "  cli = component 'Command line'\n"
          "  views = component 'Views'\n"  # `views` is a keyword LikeC4 cannot parse here
          "  cli -> views 'shows'\n"
          "}\n")
    assert run_check(["arch", "check", "--repo", str(repo)]) == 1
    out = capsys.readouterr().out
    assert "RESULT arch-check invalid_diagram=1 exit=1" in out
    assert "tool_unavailable" not in out
