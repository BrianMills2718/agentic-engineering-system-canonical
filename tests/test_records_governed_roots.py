"""A governed root written without a trailing slash must not capture sibling paths."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_engineering_system.records import RecordLoadError, load_project

FIXTURE = Path(__file__).parent / "greenfield/fixtures/whygame5-54043e2/.aes/project.yaml"


def _project(tmp_path: Path, roots: list[str]) -> Path:
    text = FIXTURE.read_text(encoding="utf-8").replace("  - src/\n  - tests/\n", "".join(f"  - {r}\n" for r in roots))
    path = tmp_path / "project.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_roots_load_with_one_trailing_slash(tmp_path: Path) -> None:
    project = load_project(_project(tmp_path, ["src", "tests//"]))
    assert project.governed_roots == ["src/", "tests/"]
    # planning/reconcile test containment with startswith(root); "src" alone matched "src_backup/x.py".
    assert not "src_backup/foo.py".startswith(project.governed_roots[0])


@pytest.mark.parametrize("root", ["/abs", "../up", "", "/"])
def test_roots_outside_the_repository_are_rejected(tmp_path: Path, root: str) -> None:
    with pytest.raises(RecordLoadError):
        load_project(_project(tmp_path, [repr(root) if root in ("", "/") else root]))
