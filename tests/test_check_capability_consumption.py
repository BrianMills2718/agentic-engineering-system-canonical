"""Tests for the import scanner that fills PROJECT_GRAPH.json depends_on.

Ported from Project Meta tests/test_check_capability_consumption.py; the two tests at the end are new
(graph and registry from configuration)."""

from __future__ import annotations

import json
import sys

import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_capability_consumption as scanner  # noqa: E402


def _repo(root: Path, name: str, files: dict[str, str]) -> Path:
    """Create a repo directory with the given relative files."""
    repo = root / name
    for rel, text in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return repo


def _graph(tmp_path: Path, records: list[dict]) -> Path:
    """Write a PROJECT_GRAPH.json and return its path."""
    path = tmp_path / "PROJECT_GRAPH.json"
    path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    return path


def _scan(tmp_path: Path, records: list[dict]) -> list[dict]:
    """Run the scan over records and return the undeclared-dependency findings."""
    scanner._IMPORT_CACHE.clear()
    scanner._LOCAL_NAMES_CACHE.clear()
    scanner._REFERENCE_CACHE.clear()
    registry = tmp_path / "registry.yaml"
    registry.write_text("entries: []\n", encoding="utf-8")
    result = scanner.run_scan(
        project_graph_path=_graph(tmp_path, records), capability_registry_path=registry
    )
    return [f for f in result.findings if f["kind"] == "undeclared_project_dependency"]


def _record(repo_id: str, path: Path, **extra) -> dict:
    """Build a minimal active repository record."""
    return {"id": repo_id, "path": str(path), "status": "active", **extra}


@pytest.mark.req("project-graph-dependency-scan/undeclared-use-is-found")
def test_import_of_another_repos_src_package_is_a_link(tmp_path: Path) -> None:
    """A repo importing a src-layout package owned by another repo gets that link, naming the package."""
    lib = _repo(tmp_path, "lib_repo", {"src/shiny_lib/__init__.py": ""})
    app = _repo(tmp_path, "app_repo", {"run.py": "import shiny_lib\n"})
    findings = _scan(tmp_path, [_record("shiny-lib", lib), _record("app", app)])
    assert [(f["consumer"], f["provider"], f["packages"]) for f in findings] == [
        ("app", "shiny-lib", ["shiny_lib"])
    ]


def test_import_that_resolves_locally_is_not_a_link(tmp_path: Path) -> None:
    """A repo importing its own module of the same name as another repo's package gets no link."""
    lib = _repo(tmp_path, "lib_repo", {"widgets/__init__.py": ""})
    app = _repo(tmp_path, "app_repo", {"widgets.py": "", "run.py": "import widgets\n"})
    assert _scan(tmp_path, [_record("lib", lib), _record("app", app)]) == []


def test_fork_with_the_same_package_resolves_to_the_record_named_after_it(tmp_path: Path) -> None:
    """Two clones claiming one package: the record whose id is the package name owns it."""
    main = _repo(tmp_path, "llm_client", {"llm_client/__init__.py": ""})
    fork = _repo(tmp_path, "fork", {"llm_client/__init__.py": ""})
    app = _repo(tmp_path, "app_repo", {"run.py": "from llm_client import call\n"})
    findings = _scan(
        tmp_path,
        [_record("llm_client", main), _record("other-llm-client", fork), _record("app", app)],
    )
    assert [(f["consumer"], f["provider"]) for f in findings] == [("app", "llm_client")]


def test_generic_package_name_never_identifies_an_owner(tmp_path: Path) -> None:
    """A unique but generic package name such as config is not evidence of a dependency."""
    lib = _repo(tmp_path, "lib_repo", {"config/__init__.py": ""})
    app = _repo(tmp_path, "app_repo", {"run.py": "import config\n"})
    assert _scan(tmp_path, [_record("lib", lib), _record("app", app)]) == []


def test_raw_copies_and_nested_repos_are_not_scanned(tmp_path: Path) -> None:
    """Imports inside raw/ captures or a nested git repository do not count for the outer repo."""
    lib = _repo(tmp_path, "lib_repo", {"src/shiny_lib/__init__.py": ""})
    app = _repo(
        tmp_path,
        "app_repo",
        {
            "raw/sources/copy.py": "import shiny_lib\n",
            "inner/.git/HEAD": "ref: refs/heads/main\n",
            "inner/run.py": "import shiny_lib\n",
        },
    )
    assert _scan(tmp_path, [_record("shiny-lib", lib), _record("app", app)]) == []


def test_declared_link_and_retired_records_are_skipped(tmp_path: Path) -> None:
    """An already declared link is not reported, and a retired consumer is not scanned."""
    lib = _repo(tmp_path, "lib_repo", {"src/shiny_lib/__init__.py": ""})
    app = _repo(tmp_path, "app_repo", {"run.py": "import shiny_lib\n"})
    old = _repo(tmp_path, "old_repo", {"run.py": "import shiny_lib\n"})
    records = [
        _record("shiny-lib", lib),
        _record("app", app, depends_on=["shiny-lib"]),
        _record("old", old, status="deleted"),
    ]
    assert _scan(tmp_path, records) == []


@pytest.mark.req("project-graph-dependency-scan/write-only-adds")
def test_write_only_adds_and_keeps_hand_written_links(tmp_path: Path) -> None:
    """--write appends detected links after the existing ones and never removes any."""
    records = [
        {"id": "app", "status": "active", "depends_on": ["hand-written"]},
        {"id": "shiny-lib", "status": "active"},
    ]
    path = _graph(tmp_path, records)
    finding = {"kind": "undeclared_project_dependency", "consumer": "app", "provider": "shiny-lib"}
    assert scanner.write_detected_dependencies(path, [finding, finding]) == 1
    written = json.loads(path.read_text(encoding="utf-8"))
    assert written[0]["depends_on"] == ["hand-written", "shiny-lib"]
    assert path.read_text(encoding="utf-8") == json.dumps(written, indent=2) + "\n"


def _home_repos(tmp_path: Path, monkeypatch, repos: dict[str, dict[str, str]]) -> dict[str, Path]:
    """Create repos under a fake home's code2/ folder and point the scanner at that home."""
    monkeypatch.setattr(scanner, "HOME", tmp_path)
    return {name: _repo(tmp_path / "code2", name, files) for name, files in repos.items()}


def test_path_into_another_repo_in_code_is_a_link(tmp_path: Path, monkeypatch) -> None:
    """A shell script or Python string naming ~/code2/<repo>/... links to that repo."""
    repos = _home_repos(tmp_path, monkeypatch, {
        "store": {"README.md": "x"},
        "app": {"run.sh": "python ~/code2/store/scripts/export.py\n"},
        "tool": {"t.py": 'from pathlib import Path\nROOT = Path.home() / "code2" / "store"\n'},
    })
    records = [_record(name, path) for name, path in repos.items()]
    found = {(f["consumer"], f["provider"]): f["via"] for f in _scan(tmp_path, records)}
    assert found == {
        ("app", "store"): ["path ~/code2/store in run.sh"],
        ("tool", "store"): ["path ~/code2/store in t.py"],
    }


def test_paths_in_comments_docstrings_data_and_proposals_are_not_links(tmp_path: Path, monkeypatch) -> None:
    """Only code that runs counts: comments, docstrings, data files and proposal scripts only mention."""
    repos = _home_repos(tmp_path, monkeypatch, {
        "store": {"README.md": "x"},
        "app": {
            "run.sh": "# see ~/code2/store for the format\necho ok\n",
            "a.py": '"""Reads ~/code2/store."""\n',
            "index.json": '{"path": "~/code2/store"}\n',
            "proposals/probe.py": 'P = "~/code2/store/x"\n',
            "enforced_planning/claim.py": 'P = "~/code2/store/x"\n',
        },
    })
    records = [_record(name, path) for name, path in repos.items()]
    assert _scan(tmp_path, records) == []


def test_running_another_repos_command_is_a_link(tmp_path: Path, monkeypatch) -> None:
    """A command from a repo's [project.scripts] or a ~/.local/bin symlink into it links to that repo.

    Machine-wide wrappers, commands named like a repo, a name inside a label
    string, and JS/TS strings are not evidence.
    """
    repos = _home_repos(tmp_path, monkeypatch, {
        "brain": {
            "pyproject.toml": '[project]\nname = "brain"\n[project.scripts]\nbrain-alert = "brain.cli:main"\n',
            "wrap.py": "",
        },
        "infra": {"gh.sh": ""},
        "app": {
            "daily.sh": "brain-alert --quiet\nstorage-policy gate\nbrain status\n",
            "label.py": 'KEY = f"brain-alert:{1}"\n',
            "ui.ts": 'const SKILL = "brain-alert";\n',
        },
        "runner": {"run.py": 'import subprocess\nsubprocess.run(["brain-alert", "--now"])\n'},
    })
    bin_dir = tmp_path / ".local" / "bin"
    bin_dir.mkdir(parents=True)
    (bin_dir / "storage-policy").symlink_to(repos["infra"] / "gh.sh")
    records = [_record(name, path) for name, path in repos.items()]
    found = {(f["consumer"], f["provider"]): f["via"] for f in _scan(tmp_path, records)}
    assert found == {
        ("app", "brain"): ["runs brain-alert in daily.sh"],
        ("runner", "brain"): ["runs brain-alert in run.py"],
    }


@pytest.mark.req("project-graph-dependency-scan/graph-from-config")
def test_graph_comes_from_project_graph_and_registry_is_optional(tmp_path: Path, monkeypatch) -> None:
    """No Project Meta path: the graph is PROJECT_GRAPH's, and without a registry only depends_on gaps are found."""
    for cache in (scanner._IMPORT_CACHE, scanner._LOCAL_NAMES_CACHE, scanner._REFERENCE_CACHE):
        cache.clear()
    lib = _repo(tmp_path, "libx", {"src/libx/__init__.py": ""})
    app = _repo(tmp_path, "app", {"main.py": "import libx\n"})
    graph = _graph(tmp_path, [_record("libx", lib), _record("app", app)])
    monkeypatch.setenv("PROJECT_GRAPH", str(graph))
    monkeypatch.delenv("CAPABILITY_REGISTRY", raising=False)
    result = scanner.run_scan()
    assert result.capability_registry is None
    assert [(f["kind"], f["consumer"], f["provider"]) for f in result.findings] == [
        ("undeclared_project_dependency", "app", "libx")
    ]
    assert "known_consumers check was skipped" in scanner.format_text(result)


@pytest.mark.req("project-graph-dependency-scan/graph-from-config")
def test_a_missing_graph_stops_loudly_naming_where_to_put_it(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("PROJECT_GRAPH", str(tmp_path / "absent.json"))
    monkeypatch.setattr(sys, "argv", ["check_capability_consumption.py"])
    assert scanner.main() == 2
    assert "PROJECT_GRAPH" in capsys.readouterr().err
