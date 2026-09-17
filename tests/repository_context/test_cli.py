from agentic_engineering_system.repository_context.cli import main


def test_cli_reports_actionable_recovery_for_malformed_authoritative_manifest(repo_factory, tmp_path, capsys):
    repo = repo_factory(readme="# repo", manifest="authorities: [bad")
    output = tmp_path / "out"

    result = main(["--repo", str(repo), "--output", str(output)])

    captured = capsys.readouterr().out
    assert result == 2
    assert "ERROR" in captured
    assert "Recovery:" in captured
    assert "correct the authoritative repository declaration and retry" in captured
    assert "no legacy fallback was used" in captured
    assert (output / "context.json").is_file()
    assert (output / "index.html").is_file()
