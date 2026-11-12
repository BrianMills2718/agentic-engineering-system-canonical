"""`lockstep.yaml` sets each commit check to block, warn or off, and the other settings the checks read."""

import pytest

from lockstep.checks.cli import run as run_check
from lockstep.checks.config import ConfigError, load
from lockstep_checks_support import SPEC, write, repo  # noqa: F401  (fixture)

# The `repo` fixture has a spec whose requirement and scenario have no implementer or test: trace fails on it.


def _set(repo, text):
    write(repo, "lockstep.yaml", text)


@pytest.mark.req("lockstep-checks/a-missing-lockstep-yaml-means-every-check-blocks")
def test_a_missing_lockstep_yaml_means_every_check_blocks(repo, capsys):
    assert load(repo).mode("trace") == "block"
    assert run_check(["trace", "--repo", str(repo)]) == 1
    assert "RESULT trace findings=2 exit=1" in capsys.readouterr().out


@pytest.mark.req("lockstep-checks/warn-prints-a-warning-and-exits-zero")
def test_warn_prints_a_warning_and_exits_zero(repo, capsys):
    _set(repo, "checks:\n  trace: warn\n")
    assert run_check(["trace", "--repo", str(repo)]) == 0
    out = capsys.readouterr().out
    assert "warning: trace failed" in out and "RESULT trace findings=2 exit=1" in out


@pytest.mark.req("lockstep-checks/off-skips-the-check-and-exits-zero")
def test_off_skips_the_check_and_exits_zero(repo, capsys):
    _set(repo, "checks:\n  trace: off\n")
    assert run_check(["trace", "--repo", str(repo)]) == 0
    out = capsys.readouterr().out
    assert "skipped (off)" in out and "RESULT" not in out


@pytest.mark.req("lockstep-checks/block-set-explicitly-exits-one-and-other-checks-keep-their-own-mode")
def test_block_set_explicitly_exits_one_and_other_checks_keep_their_own_mode(repo, capsys):
    _set(repo, "checks:\n  trace: block\n  docmeta: off\n")
    assert run_check(["trace", "--repo", str(repo)]) == 1
    assert run_check(["docmeta", "--repo", str(repo)]) == 0
    assert "skipped (off)" in capsys.readouterr().out


@pytest.mark.req("lockstep-checks/a-bad-mode-or-unknown-check-is-an-error")
def test_a_bad_mode_or_unknown_check_is_an_error(repo, capsys):
    _set(repo, "checks:\n  trace: sometimes\n")
    with pytest.raises(ConfigError, match="sometimes"):
        load(repo)
    assert run_check(["trace", "--repo", str(repo)]) == 2
    _set(repo, "checks:\n  nonsense: warn\n")
    with pytest.raises(ConfigError, match="nonsense"):
        load(repo)


@pytest.mark.req("lockstep-checks/defaults-when-keys-are-absent")
def test_defaults_when_keys_are_absent(repo):
    _set(repo, "schema: lockstep.side.v1\n")
    cfg = load(repo)
    assert (cfg.human_pattern, cfg.owner, cfg.likec4) == ("brian", None, "likec4@1.60.0")


@pytest.mark.req("lockstep-checks/likec4-pin-and-owner-are-read")
def test_likec4_pin_and_owner_are_read(repo):
    _set(repo, "likec4: 1.70.0\nowner: Acme\n")
    cfg = load(repo)
    assert (cfg.likec4, cfg.owner) == ("likec4@1.70.0", "Acme")


@pytest.mark.req("lockstep-checks/sources-a-configured-human-pattern-replaces-the-default")
def test_a_configured_human_pattern_replaces_the_default(repo, capsys):
    write(repo, "openspec/specs/core/spec.md", SPEC.replace(
        "The tool SHALL do the thing.\n", 'The tool SHALL do the thing.\n\n    Source: Dana, 2026-10-15: "do it"\n'))
    assert run_check(["sources", "--repo", str(repo), "--json"]) == 0
    assert '"source": "other"' in capsys.readouterr().out
    _set(repo, "sources:\n  human_pattern: dana\n")
    assert run_check(["sources", "--repo", str(repo), "--json"]) == 0
    assert '"source": "brian"' in capsys.readouterr().out


@pytest.mark.req("lockstep-checks/lockstep-check-without-a-name-still-runs-the-tree-check")
def test_lockstep_check_without_a_name_still_runs_the_tree_check(tmp_path, monkeypatch, capsys):
    from lockstep import check as plan_check

    monkeypatch.setattr("sys.argv", ["lockstep", "check", "--repo", str(tmp_path)])
    monkeypatch.setattr(plan_check, "main", lambda argv: (print("whole-tree", argv), 0)[1])
    assert plan_check.cli() == 0
    assert "whole-tree ['--repo'" in capsys.readouterr().out


@pytest.mark.req("lockstep-checks/the-lockstep-command-runs-a-named-check")
def test_the_lockstep_command_runs_a_named_check(repo):
    import subprocess, sys
    done = subprocess.run([sys.executable, "-c", "import sys; sys.argv=['lockstep','check','trace','--repo',sys.argv[1]]; "
                           "from lockstep.check import cli; raise SystemExit(cli())", str(repo)], capture_output=True, text=True)
    assert done.returncode == 1 and "RESULT trace findings=2" in done.stdout
