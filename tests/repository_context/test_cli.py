import json

from agentic_engineering_system.repository_context.cli import main


def test_cli_reports_actionable_recovery_for_malformed_authoritative_manifest(repo_factory, tmp_path, capsys):
    repo = repo_factory(
        readme="# repo\n",
        manifest="schema_version: '0.1-pilot'\nauthorities: [bad\n",
    )
    output = tmp_path / "out"

    result = main(["--repo", str(repo), "--output", str(output)])

    captured = capsys.readouterr().out
    assert result == 2
    assert "resolution: ERROR" in captured
    assert "Recovery:" in captured
    assert "Correct the authoritative manifest and retry" in captured
    assert (output / "context.json").is_file()
    assert (output / "index.html").is_file()

    artifact = json.loads((output / "context.json").read_text(encoding="utf-8"))
    assert "legacy fallback is disabled" in artifact["navigation"]["summary"]
