import subprocess

from agentic_engineering_system.repository_context.render_html import render_html
from agentic_engineering_system.repository_context.resolver import resolve_repository_context


def test_html_is_human_surface_and_keeps_exact_paths(repo_factory):
    readme = "# x\nShared typed data contracts.\n"
    pyproject = "[project]\nname='demo_pkg'\n[tool.setuptools.packages.find]\nwhere=['src']\n"
    repo = repo_factory(readme=readme, pyproject=pyproject)
    (repo / "src" / "demo_pkg").mkdir(parents=True)
    (repo / "src" / "demo_pkg" / "__init__.py").write_text("", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "pkg"], check=True)
    artifact = resolve_repository_context(repo)
    page = render_html(artifact)
    assert "Repository context" in page
    assert "Next legitimate place to deepen" in page
    assert "src/demo_pkg/" in page
    assert "directory names alone do not establish semantic authority" in page
    assert "context.json" in page
