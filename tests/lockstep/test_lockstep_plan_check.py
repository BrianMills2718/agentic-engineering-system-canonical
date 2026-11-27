"""`lockstep plan check`: runs Company Planning's validator the way ship does, plus the work-unit DAG.

The validator is replaced by a stand-in script through SHIP_PLANNING_VALIDATOR, the override ship's own tests use.
"""

import json
import sys
from pathlib import Path

import pytest

from lockstep.plan_check import plan_cli


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A repository with a planning package, and a stand-in validator whose exit status is $FAKE_EXIT."""
    root = tmp_path / "repo"
    (root / "docs/planning").mkdir(parents=True)
    (root / "docs/planning/planning-package.json").write_text("{}", encoding="utf-8")
    fake = tmp_path / "validate_planning_package.py"
    fake.write_text("import os, sys\nprint('validator ran on', sys.argv[-1])\n"
                    "sys.exit(0 if '--no-freshness' in sys.argv and os.environ.get('FRESH_ONLY') else int(os.environ['FAKE_EXIT']))\n",
                    encoding="utf-8")
    monkeypatch.setenv("SHIP_PLANNING_VALIDATOR", str(fake))
    monkeypatch.setenv("SHIP_VALIDATOR_PYTHON", sys.executable)
    monkeypatch.setenv("SHIP_LOG_DIR", str(tmp_path / "logs"))
    return root


@pytest.mark.req("lockstep-plan-check/the-validator-s-verdict-is-the-command-s-verdict")
@pytest.mark.parametrize("code", [0, 1])
def test_the_validators_verdict_is_the_commands_verdict(repo, monkeypatch, capsys, code):
    monkeypatch.setenv("FAKE_EXIT", str(code))
    assert plan_cli(["check", "--repo", str(repo)]) == code
    out = capsys.readouterr().out
    assert "validator ran on" in out and "planning-package.json" in out


@pytest.mark.req("lockstep-plan-check/a-package-out-of-date-only-by-freshness-passes-with-a-warning")
def test_a_package_out_of_date_only_by_freshness_passes_with_a_warning(repo, monkeypatch, capsys):
    monkeypatch.setenv("FAKE_EXIT", "1")
    monkeypatch.setenv("FRESH_ONLY", "1")
    assert plan_cli(["check", "--repo", str(repo)]) == 0
    assert "out of date" in capsys.readouterr().out


def test_an_unexpected_validator_status_cannot_check(repo, monkeypatch, capsys):
    monkeypatch.setenv("FAKE_EXIT", "3")
    assert plan_cli(["check", "--repo", str(repo)]) == 2
    assert "the validator exited 3" in capsys.readouterr().out


def test_ship_progress_lines_stay_off_json_output(repo, monkeypatch, capsys, tmp_path):
    """The real fetch path: the validator is archived from a company-planning clone's origin/main."""
    import subprocess
    validator = "plugins/company-planning/skills/planning-compliance/scripts/validate_planning_package.py"
    origin = tmp_path / "cp-origin"
    (origin / validator).parent.mkdir(parents=True)
    (origin / validator).write_text("import sys\nprint('real fetch ran')\nsys.exit(0)\n", encoding="utf-8")
    for cmd in (["init", "-q", "-b", "main"], ["add", "."], ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "v"]):
        subprocess.run(["git", "-C", str(origin), *cmd], check=True)
    clone = tmp_path / "cp"
    subprocess.run(["git", "clone", "-q", str(origin), str(clone)], check=True)
    monkeypatch.delenv("SHIP_PLANNING_VALIDATOR")
    monkeypatch.setenv("SHIP_COMPANY_PLANNING", str(clone))
    assert plan_cli(["check", "--repo", str(repo), "--json"]) == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "real fetch ran" in data["validator"]["output"] and "ship: fetch company-planning" in captured.err


@pytest.mark.req("lockstep-plan-check/a-repository-with-no-planning-package-cannot-be-checked")
def test_a_repository_with_no_planning_package_cannot_be_checked(repo, monkeypatch, capsys):
    monkeypatch.setenv("FAKE_EXIT", "0")
    (repo / "docs/planning/planning-package.json").unlink()
    assert plan_cli(["check", "--repo", str(repo)]) == 2
    assert "no planning package" in capsys.readouterr().out


@pytest.mark.req("lockstep-plan-check/work-unit-problems-are-added")
def test_work_unit_problems_are_added(repo, monkeypatch, capsys):
    monkeypatch.setenv("FAKE_EXIT", "0")
    (repo / "docs/planning/work-units.json").write_text(json.dumps({"record_type": "work_units", "units": [
        {"id": "A", "title": "a", "depends_on": ["Z"], "touches": ["x.py"], "status": "planned"}]}), encoding="utf-8")
    assert plan_cli(["check", "--repo", str(repo)]) == 1
    assert "work units: A: depends_on names Z" in capsys.readouterr().out


def test_json_output_is_one_object(repo, monkeypatch, capsys):
    monkeypatch.setenv("FAKE_EXIT", "1")
    assert plan_cli(["check", "--repo", str(repo), "--json"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is False and data["validator"]["exit"] == 1 and data["work_units"] == []


def test_a_missing_validator_cannot_check(repo, monkeypatch, capsys, tmp_path):
    monkeypatch.setenv("SHIP_PLANNING_VALIDATOR", str(tmp_path / "absent.py"))
    assert plan_cli(["check", "--repo", str(repo)]) == 2
    assert "does not exist" in capsys.readouterr().out


VALIDATOR_PATH = "plugins/company-planning/skills/planning-compliance/scripts/validate_planning_package.py"


def _git(cwd, *args):
    import subprocess
    subprocess.run(["git", "-C", str(cwd), "-c", "user.email=t@t", "-c", "user.name=t", *args], check=True,
                   capture_output=True)


def _company_planning(tmp_path, branches=("main",)):
    """A Company Planning repository whose validator prints which branch it came from."""
    origin = tmp_path / "cp-configured"
    (origin / VALIDATOR_PATH).parent.mkdir(parents=True)
    _git(tmp_path, "init", "-q", "-b", "main", str(origin))
    for branch in branches:
        if branch != "main":
            _git(origin, "checkout", "-q", "-b", branch)
        (origin / VALIDATOR_PATH).write_text(f"import sys\nprint('validator from {branch}')\nsys.exit(0)\n",
                                             encoding="utf-8")
        _git(origin, "add", ".")
        _git(origin, "commit", "-qm", branch)
    _git(origin, "checkout", "-q", "main")
    return origin


def _settings_on_main(root, tmp_path, text):
    """Make root a repository whose origin/main holds lockstep.yaml with `text`."""
    bare = tmp_path / "repo-origin.git"
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(bare))
    _git(tmp_path, "init", "-q", "-b", "main", str(root))
    (root / "lockstep.yaml").write_text(text, encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "settings")
    _git(root, "remote", "add", "origin", str(bare))
    _git(root, "push", "-q", "origin", "main")
    _git(root, "fetch", "-q", "origin")


@pytest.fixture
def configured(repo, tmp_path, monkeypatch):
    """No validator environment variables, a private cache folder, and a stand-in default checkout that is absent."""
    monkeypatch.delenv("SHIP_PLANNING_VALIDATOR")
    monkeypatch.delenv("SHIP_COMPANY_PLANNING", raising=False)
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")
    return repo


@pytest.mark.req("lockstep-plan-check/a-configured-repository-is-the-source")
def test_a_configured_repository_is_the_source(configured, tmp_path, capsys):
    cp = _company_planning(tmp_path)
    _settings_on_main(configured, tmp_path, f"planning:\n  validator:\n    repo: {cp}\n")
    assert plan_cli(["check", "--repo", str(configured)]) == 0
    captured = capsys.readouterr()
    assert "validator from main" in captured.out
    assert f"ship: planning validator: {cp}" in captured.err


@pytest.mark.req("lockstep-plan-check/an-environment-variable-overrides-a-configured-repository-with-a-warning")
def test_an_environment_variable_overrides_a_configured_repository_with_a_warning(configured, tmp_path, capsys,
                                                                                    monkeypatch):
    cp = _company_planning(tmp_path)
    _settings_on_main(configured, tmp_path, "planning:\n  validator:\n    repo: git@example.invalid:x/y.git\n")
    clone = tmp_path / "cp-env"
    _git(tmp_path, "clone", "-q", str(cp), str(clone))
    monkeypatch.setenv("SHIP_COMPANY_PLANNING", str(clone))
    assert plan_cli(["check", "--repo", str(configured)]) == 0
    captured = capsys.readouterr()
    assert "validator from main" in captured.out
    assert "warning" in captured.err and "git@example.invalid:x/y.git" in captured.err


@pytest.mark.req("lockstep-plan-check/the-ref-picks-the-branch")
def test_the_ref_picks_the_branch(configured, tmp_path, capsys):
    cp = _company_planning(tmp_path, branches=("main", "release"))
    _settings_on_main(configured, tmp_path, f"planning:\n  validator:\n    repo: {cp}\n    ref: release\n")
    assert plan_cli(["check", "--repo", str(configured)]) == 0
    assert "validator from release" in capsys.readouterr().out


@pytest.mark.req("lockstep-plan-check/an-unreachable-configured-repository-cannot-be-fetched")
def test_an_unreachable_configured_repository_cannot_be_fetched(configured, tmp_path, capsys):
    missing = tmp_path / "no-such-company-planning"
    _settings_on_main(configured, tmp_path, f"planning:\n  validator:\n    repo: {missing}\n")
    assert plan_cli(["check", "--repo", str(configured)]) == 2
    assert str(missing) in capsys.readouterr().out


@pytest.mark.req("lockstep-plan-check/a-bad-validator-setting-is-a-configuration-error")
def test_a_bad_validator_setting_is_a_configuration_error(configured, tmp_path, capsys):
    _settings_on_main(configured, tmp_path, "planning:\n  validator: somewhere\n")
    assert plan_cli(["check", "--repo", str(configured)]) == 2
    assert "planning.validator" in capsys.readouterr().out


@pytest.mark.req("lockstep-plan-check/a-configured-repository-is-the-source")
def test_two_first_uses_share_one_validator_cache(configured, tmp_path, monkeypatch):
    import fcntl
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    from lockstep.plan_check import fetch_planning_validator
    from lockstep.ship import Run

    address = _company_planning(tmp_path)
    _settings_on_main(configured, tmp_path, f"planning:\n  validator:\n    repo: {address}\n")
    barrier = Barrier(2, timeout=15)
    acquire = fcntl.flock

    def acquire_together(handle, flags):
        barrier.wait()
        acquire(handle, flags)

    monkeypatch.setattr(fcntl, "flock", acquire_together)
    with ThreadPoolExecutor(max_workers=2) as pool:
        runs = [Run(configured, log_dir=tmp_path / f"log-{i}") for i in range(2)]
        outcomes = list(pool.map(fetch_planning_validator, runs))
    assert all(path and failure is None for path, failure in outcomes), outcomes
    assert len(list((tmp_path / "cache" / "lockstep").glob("*.git"))) == 1
    assert all("validator from main" in Path(path).read_text() for path, _ in outcomes)
