"""The generated docstring wiki links every tracked artifact relative to its own location."""

from __future__ import annotations

import subprocess
from pathlib import Path

from enforced_planning.docstring_wiki import render_docstring_wiki


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "docs" / "plans").mkdir(parents=True)
    (root / "docs" / "plans" / "my plan.md").write_text(
        "---\ndescription: A plan with a space in its file name.\n---\n\n# Plan\n", encoding="utf-8"
    )
    (root / "README.md").write_text("# Readme\n\nTop-level readme text.\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    return root


def test_links_are_relative_to_the_output_page(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    rendered = render_docstring_wiki(root, output_path=Path("wiki/_documents.md"))
    assert "### [`README.md`](../README.md)" in rendered
    assert "### [`docs/plans/my plan.md`](../docs/plans/my%20plan.md)" in rendered
    assert "A plan with a space in its file name." in rendered


def test_default_output_links_from_generated_folder(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    rendered = render_docstring_wiki(root)
    assert "### [`README.md`](../README.md)" in rendered
    rendered_root = render_docstring_wiki(root, output_path=Path("CATALOG.md"))
    assert "### [`README.md`](README.md)" in rendered_root
