"""`lockstep init` installs Lockstep in a repository: config, Claude Code and Codex hooks, lefthook."""

import json
from pathlib import Path
import subprocess

import pytest
import yaml

from lockstep.checks.config import CHECK_NAMES, load
from lockstep.init_repo import init_repo, owner_from_origin

FILES = ("lockstep.yaml", ".claude/settings.json", ".codex/hooks.json", "lefthook.yml")


def _git_repo(path: Path, origin: str | None = None) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    if origin:
        subprocess.run(["git", "-C", str(path), "remote", "add", "origin", origin], check=True)
    return path


def _snapshot(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file() and ".git/" not in p.as_posix()}


@pytest.mark.req("lockstep-init/fresh-repository-gets-all-four")
def test_fresh_repository_gets_all_four(tmp_path, capsys):
    root = _git_repo(tmp_path / "r")
    assert init_repo(root, owner="Acme") == 0
    for rel in FILES:
        assert (root / rel).is_file(), rel
    cfg = yaml.safe_load((root / "lockstep.yaml").read_text())
    assert set(cfg["checks"]) == set(CHECK_NAMES) and set(cfg["checks"].values()) == {"block"}
    assert cfg["layout"] == [] and "human_pattern" in cfg["sources"]
    for rel in (".claude/settings.json", ".codex/hooks.json"):
        hook = json.loads((root / rel).read_text())["hooks"]["PreToolUse"][0]["hooks"][0]
        assert "lockstep-hook" in hook["command"] and "uvx --from git+https://" in hook["command"]
    assert "--client codex" in (root / ".codex/hooks.json").read_text()
    lefthook = yaml.safe_load((root / "lefthook.yml").read_text())
    assert "lockstep" in lefthook["pre-commit"]["commands"]
    assert ".lockstep/" in (root / ".gitignore").read_text().splitlines()
    out = capsys.readouterr().out
    assert all(f"wrote   {rel}" in out for rel in FILES)


@pytest.mark.req("lockstep-init/a-second-run-changes-nothing")
def test_a_second_run_changes_nothing(tmp_path, capsys):
    root = _git_repo(tmp_path / "r")
    init_repo(root)
    before = _snapshot(root)
    capsys.readouterr()
    assert init_repo(root) == 0
    assert _snapshot(root) == before
    out = capsys.readouterr().out
    assert all(f"skipped {rel}" in out for rel in FILES) and "wrote=0" in out


@pytest.mark.req("lockstep-init/a-second-run-changes-nothing")
def test_an_existing_lockstep_yaml_is_never_overwritten(tmp_path):
    root = _git_repo(tmp_path / "r")
    (root / "lockstep.yaml").write_text("checks:\n  trace: off\n")
    init_repo(root, owner="Acme")
    assert (root / "lockstep.yaml").read_text() == "checks:\n  trace: off\n"


@pytest.mark.req("lockstep-init/existing-settings-keep-their-other-keys")
def test_existing_settings_keep_their_other_keys(tmp_path):
    root = _git_repo(tmp_path / "r")
    other = {"type": "command", "command": "echo other"}
    existing = {"model": "opus", "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [other]}],
                                           "PostToolUse": [{"matcher": "Edit", "hooks": [other]}]}}
    (root / ".claude").mkdir()
    (root / ".claude/settings.json").write_text(json.dumps(existing))
    init_repo(root)
    init_repo(root)
    data = json.loads((root / ".claude/settings.json").read_text())
    assert data["model"] == "opus"
    assert data["hooks"]["PostToolUse"][0] == existing["hooks"]["PostToolUse"][0]
    assert sum("lockstep refresh" in h["command"] for e in data["hooks"]["PostToolUse"] for h in e["hooks"]) == 1
    pre = data["hooks"]["PreToolUse"]
    assert pre[0] == existing["hooks"]["PreToolUse"][0]
    assert sum("lockstep-hook" in h["command"] for e in pre for h in e["hooks"]) == 1


@pytest.mark.req("lockstep-init/existing-settings-keep-their-other-keys")
def test_an_existing_lefthook_keeps_its_commands(tmp_path):
    root = _git_repo(tmp_path / "r")
    (root / "lefthook.yml").write_text("# mine\npre-commit:\n  commands:\n    lint:\n      run: ruff check\n")
    init_repo(root)
    text = (root / "lefthook.yml").read_text()
    data = yaml.safe_load(text)
    assert text.startswith("# mine") and set(data["pre-commit"]["commands"]) == {"lint", "lockstep"}


@pytest.mark.req('lockstep-doc-facts/installed-post-edit-hook-refreshes-and-precommit-rejects-stale')
def test_init_upgrades_recognized_lefthook_command(tmp_path):
    root = _git_repo(tmp_path/'r')
    init_repo(root)
    path = root/'lefthook.yml'
    data = yaml.safe_load(path.read_text())
    commands = data['pre-commit']['commands']
    commands['lockstep']['run'] = commands['lockstep']['run'].split(' && uvx')[0]
    commands['lint'] = {'run': 'ruff check'}
    path.write_text('# keep this\n'+yaml.safe_dump(data))
    init_repo(root)
    upgraded = yaml.safe_load(path.read_text())['pre-commit']['commands']
    assert 'project --check' in upgraded['lockstep']['run']
    assert upgraded['lint'] == {'run': 'ruff check'}
    assert path.read_text().startswith('# keep this')
    before = path.read_bytes()
    init_repo(root)
    assert path.read_bytes() == before


@pytest.mark.req('lockstep-doc-facts/installed-post-edit-hook-refreshes-and-precommit-rejects-stale')
@pytest.mark.parametrize('custom', [False, True])
def test_init_preserves_custom_lefthook_and_does_not_skip_comments(tmp_path, custom):
    root = _git_repo(tmp_path/'r')
    commands = {'lint': {'run': 'ruff check'}}
    if custom:
        commands['lockstep'] = {'run': 'custom-lockstep-check --strict', 'priority': 2}
    path = root/'lefthook.yml'
    path.write_text('# custom lockstep integration\n'+yaml.safe_dump({'pre-commit': {'commands': commands}}))
    init_repo(root)
    installed = yaml.safe_load(path.read_text())['pre-commit']['commands']
    for name, value in commands.items():
        assert installed[name] == value
    assert any('project --check' in row['run'] for row in installed.values())
    assert path.read_text().startswith('# custom lockstep integration')
    before = path.read_bytes()
    init_repo(root)
    assert path.read_bytes() == before


@pytest.mark.req("lockstep-init/no-written-file-holds-an-absolute-path")
def test_no_written_file_holds_an_absolute_path(tmp_path):
    root = _git_repo(tmp_path / "r")
    init_repo(root)
    for rel, data in _snapshot(root).items():
        text = data.decode()
        assert "/home/" not in text and "~/" not in text and str(tmp_path) not in text, rel
        for token in text.replace('"', " ").replace("'", " ").split():
            assert not token.startswith("/"), (rel, token)


@pytest.mark.req("lockstep-init/owner-lands-in-lockstep-yaml")
def test_owner_lands_in_lockstep_yaml(tmp_path):
    root = _git_repo(tmp_path / "a")
    init_repo(root, owner="Acme")
    assert load(root).owner == "Acme"
    other = _git_repo(tmp_path / "b", origin="git@github.com:Widgets/thing.git")
    init_repo(other)
    assert load(other).owner == "Widgets"
    bare = _git_repo(tmp_path / "c")
    init_repo(bare)
    assert load(bare).owner not in (None, "")


def test_owner_is_read_from_https_and_ssh_origins():
    assert owner_from_origin("https://github.com/Foo/bar.git") == "Foo"
    assert owner_from_origin("git@github-personal:Foo/bar.git") == "Foo"
    assert owner_from_origin("") is None


@pytest.mark.req("lockstep-init/a-lockstep-yaml-copied-to-another-repository-is-read-there")
def test_a_lockstep_yaml_copied_to_another_repository_is_read_there(tmp_path):
    a = _git_repo(tmp_path / "a")
    init_repo(a, owner="Acme")
    text = (a / "lockstep.yaml").read_text().replace("trace: block", "trace: warn")
    b = _git_repo(tmp_path / "b")
    (b / "lockstep.yaml").write_text(text)
    cfg = load(b)
    assert cfg.mode("trace") == "warn" and cfg.mode("docmeta") == "block" and cfg.owner == "Acme"
    assert cfg.human_pattern == yaml.safe_load(text)["sources"]["human_pattern"]


def test_cli_wires_init(tmp_path, monkeypatch, capsys):
    from lockstep import check
    root = _git_repo(tmp_path / "r")
    monkeypatch.setattr("sys.argv", ["lockstep", "init", "--repo", str(root), "--owner", "Acme"])
    assert check.cli() == 0
    assert (root / "lockstep.yaml").is_file()


@pytest.mark.req("lockstep-init/fresh-repository-gets-all-four")
def test_init_counts_brian_source_lines_as_human_by_default_and_takes_a_pattern(tmp_path):
    """`lockstep init` wrote `human_pattern: "human"`, which matched none of 124 `Source: Brian, <date>` lines.

    It now writes the same default the checks use (code-88 session, 2026-11-12), and `--human-pattern` overrides it.
    """
    import re

    from lockstep.checks.sources import DEFAULT_HUMAN_PATTERN

    (tmp_path / "a").mkdir()
    init_repo(tmp_path / "a")
    pattern = yaml.safe_load((tmp_path / "a" / "lockstep.yaml").read_text())["sources"]["human_pattern"]
    assert pattern == DEFAULT_HUMAN_PATTERN
    assert re.match(pattern, "Brian, 2026-11-12", re.IGNORECASE)
    (tmp_path / "b").mkdir()
    init_repo(tmp_path / "b", human_pattern="tyler|brian")
    assert yaml.safe_load((tmp_path / "b" / "lockstep.yaml").read_text())["sources"]["human_pattern"] == "tyler|brian"
