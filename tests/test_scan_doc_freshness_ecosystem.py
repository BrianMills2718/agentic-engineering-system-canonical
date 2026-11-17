"""Root instruction freshness follows the active source during migration."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "scan_doc_freshness_ecosystem.py"


def _scanner():
    spec = importlib.util.spec_from_file_location("scan_doc_freshness_ecosystem", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _commit(path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(path), "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "fixture"],
        check=True,
    )


@pytest.mark.req("instruction-audit/freshness-comes-from-git-history", existing=True)  # ported unchanged from Project Meta
@pytest.mark.parametrize("filename", ["AGENTS.md", "CLAUDE.md"])
def test_scanner_uses_the_active_root_instruction_file(tmp_path: Path, filename: str) -> None:
    """AGENTS-only and legacy repos both produce a real instruction freshness score."""
    (tmp_path / filename).write_text("# Rules\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
    _commit(tmp_path)

    report = _scanner().scan_project({"id": "fixture", "path": str(tmp_path)}, datetime.now(timezone.utc))
    assert report is not None
    assert report["status"] == "ok"
    assert report["primary_doc"] == filename
    assert {item["doc"] for item in report["docs"]} == {filename, "docs/guide.md"}


@pytest.mark.req("instruction-audit/freshness-comes-from-git-history", existing=True)  # ported unchanged from Project Meta
def test_docs_without_root_instructions_are_still_missing_instructions(tmp_path: Path) -> None:
    """A docs directory cannot make an instructionless repo appear healthy."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
    _commit(tmp_path)

    report = _scanner().scan_project({"id": "fixture", "path": str(tmp_path)}, datetime.now(timezone.utc))
    assert report is not None
    assert report["status"] == "no_instruction_file"


@pytest.mark.req("instruction-audit/the-project-graph-comes-from-the-settings")
@pytest.mark.parametrize("name", ["scan_doc_freshness_ecosystem", "audit_instruction_quality"])
def test_the_project_graph_comes_from_the_settings(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, name: str) -> None:
    """Both audits read PROJECT_GRAPH, else the private aes-config graph; never a path beside the script."""
    script = SCRIPT.with_name(f"{name}.py")

    def load():
        spec = importlib.util.spec_from_file_location(f"{name}_graph_default", script)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    monkeypatch.delenv("PROJECT_GRAPH", raising=False)
    assert load().DEFAULT_GRAPH_PATH == Path.home() / "code2/aes-config/PROJECT_GRAPH.json"
    monkeypatch.setenv("PROJECT_GRAPH", str(tmp_path / "graph.json"))
    assert load().DEFAULT_GRAPH_PATH == tmp_path / "graph.json"
