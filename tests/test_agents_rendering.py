from pathlib import Path

from enforced_planning.agents_rendering import RendererRuntime


def test_repo_relative_paths_use_posix_separators(tmp_path: Path) -> None:
    runtime = RendererRuntime(
        script_path=tmp_path / "scripts" / "meta" / "render_agents_md.py",
        repo_root=tmp_path,
        default_template=tmp_path / "meta-process" / "templates" / "agents.md.template",
    )

    target = tmp_path / "scripts" / "relationships.yaml"

    assert runtime.repo_relative(target, tmp_path) == "scripts/relationships.yaml"
    assert "\\" not in runtime.repo_relative(target, tmp_path)
