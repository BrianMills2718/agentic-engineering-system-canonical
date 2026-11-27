"""`planning.skills`: lockstep init writes the Company Planning plugin keys, `lockstep check project` reports drift."""

import json
from pathlib import Path
import subprocess

import pytest
import yaml

from lockstep.checks.cli import run
from lockstep.checks.config import planning_modes
from lockstep.checks.plugin_settings import INSTALL_LINE, PLUGIN, drift, merge, setting
from lockstep.init_repo import init_cli, init_repo
from lockstep.side_file import side_file_problems

MIRROR = "Inside-Success/company-planning"
SETTINGS = ".claude/settings.json"


def _repo(tmp_path: Path, skills: str | None = f"{{mode: block, marketplace: {MIRROR}}}") -> Path:
    root = tmp_path / "r"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    body = "schema: lockstep.side.v1\nowner: Acme\nplanning:\n  gate: warn\n"
    if skills is not None:
        body += f"  skills: {skills}\n"
    (root / "lockstep.yaml").write_text(body)
    return root


def _settings(root: Path) -> dict:
    return json.loads((root / SETTINGS).read_text())


def _write_settings(root: Path, data: dict) -> None:
    (root / ".claude").mkdir(exist_ok=True)
    (root / SETTINGS).write_text(json.dumps(data, indent=2) + "\n")


def _wanted_source(repo: str = MIRROR) -> dict:
    return {"source": {"source": "github", "repo": repo}}


@pytest.mark.req("lockstep-init/block-writes-the-keys-and-a-second-run-skips-them")
def test_block_writes_the_keys_and_a_second_run_skips_them(tmp_path, capsys):
    root = _repo(tmp_path)
    assert init_repo(root) == 0
    assert "wrote   planning.skills" in capsys.readouterr().out
    data = _settings(root)
    assert data["extraKnownMarketplaces"]["inside-success"] == _wanted_source()
    assert data["enabledPlugins"][PLUGIN] is True
    assert "PreToolUse" in data["hooks"]
    assert run(["project", "--repo", str(root)]) == 0
    out = capsys.readouterr().out
    assert "skills" not in out
    before = (root / SETTINGS).read_bytes()
    assert init_repo(root) == 0
    assert "skipped planning.skills" in capsys.readouterr().out
    assert (root / SETTINGS).read_bytes() == before


@pytest.mark.req("lockstep-init/warn-also-writes-the-keys")
def test_warn_also_writes_the_keys(tmp_path, capsys):
    root = _repo(tmp_path, f"{{mode: warn, marketplace: {MIRROR}}}")
    assert init_repo(root) == 0
    assert _settings(root)["enabledPlugins"][PLUGIN] is True


@pytest.mark.req("lockstep-init/the-keys-merge-into-existing-settings")
def test_the_keys_merge_into_existing_settings(tmp_path, capsys):
    root = _repo(tmp_path)
    other_hook = {"matcher": "Bash", "hooks": [{"type": "command", "command": "echo other"}]}
    _write_settings(root, {"model": "sonnet", "hooks": {"PreToolUse": [other_hook]},
                           "enabledPlugins": {"other@else": True}})
    assert init_repo(root) == 0
    data = _settings(root)
    assert data["model"] == "sonnet"
    assert data["hooks"]["PreToolUse"][0] == other_hook and len(data["hooks"]["PreToolUse"]) == 2
    assert data["enabledPlugins"] == {"other@else": True, PLUGIN: True}


@pytest.mark.req("lockstep-init/a-malformed-settings-file-exits-2")
def test_a_malformed_settings_file_exits_2(tmp_path, capsys):
    root = _repo(tmp_path)
    (root / ".claude").mkdir()
    (root / SETTINGS).write_text("{not json")
    assert init_cli(["--repo", str(root)]) == 2
    assert (root / SETTINGS).read_text() == "{not json"


@pytest.mark.req("lockstep-init/off-writes-nothing-and-keeps-what-exists")
@pytest.mark.parametrize("skills", ["{mode: off}", "{mode: false}", None])
def test_off_writes_nothing_and_keeps_what_exists(tmp_path, capsys, skills):
    root = _repo(tmp_path, skills)
    assert init_repo(root) == 0
    out = capsys.readouterr().out
    assert PLUGIN not in (root / SETTINGS).read_text()
    assert "planning.skills" not in out and "codex plugin" not in out and INSTALL_LINE not in out
    kept = {"extraKnownMarketplaces": {"inside-success": _wanted_source("Someone/else")},
            "enabledPlugins": {PLUGIN: False}}
    _write_settings(root, kept)
    assert init_repo(root) == 0
    data = _settings(root)
    assert data["extraKnownMarketplaces"] == kept["extraKnownMarketplaces"]
    assert data["enabledPlugins"] == kept["enabledPlugins"]


@pytest.mark.req("lockstep-init/another-source-or-an-opt-out-is-a-conflict-left-as-it-is")
@pytest.mark.parametrize("existing, key", [
    ({"extraKnownMarketplaces": {"inside-success": _wanted_source("BrianMills2718/company-planning")}},
     "extraKnownMarketplaces.inside-success"),
    ({"extraKnownMarketplaces": {"inside-success": {"source": {"source": "directory", "path": "/x"}}}},
     "extraKnownMarketplaces.inside-success"),
    ({"enabledPlugins": {PLUGIN: False}}, f"enabledPlugins.{PLUGIN}"),
])
def test_another_source_or_an_opt_out_is_a_conflict_left_as_it_is(tmp_path, capsys, existing, key):
    root = _repo(tmp_path)
    _write_settings(root, existing)
    status, notes = merge(root / SETTINGS, setting(root))
    assert status == "conflict" and any(key in n for n in notes)
    data = _settings(root)
    for section, value in existing.items():
        assert data[section] == value  # never overwritten; the other key is still added
    assert init_repo(root) == 0
    out = capsys.readouterr().out
    assert "conflict planning.skills" in out and key in out


@pytest.mark.req("lockstep-init/autoupdate-is-tolerated")
def test_autoupdate_is_tolerated(tmp_path, capsys):
    root = _repo(tmp_path)
    _write_settings(root, {"extraKnownMarketplaces": {"inside-success": {**_wanted_source(), "autoUpdate": True}},
                           "enabledPlugins": {PLUGIN: True}})
    status, _ = merge(root / SETTINGS, setting(root))
    assert status == "skipped"
    assert _settings(root)["extraKnownMarketplaces"]["inside-success"]["autoUpdate"] is True
    assert drift(root) == ([], [])


@pytest.mark.req("lockstep-init/init-prints-the-codex-commands-and-the-install-line")
def test_init_prints_the_codex_commands_and_the_install_line(tmp_path, capsys):
    root = _repo(tmp_path)
    (root / "AGENTS.md").write_text("# Agents\n\nRules.\n")
    assert init_repo(root) == 0
    out = capsys.readouterr().out
    assert f"codex plugin marketplace add {MIRROR}" in out
    assert f"codex plugin add {PLUGIN}" in out
    assert INSTALL_LINE == f"claude plugin install {PLUGIN} --scope project" and INSTALL_LINE in out
    assert "wrote   AGENTS.md" in out
    assert init_repo(root) == 0
    assert "skipped AGENTS.md" in capsys.readouterr().out
    text = (root / "AGENTS.md").read_text()
    assert text.startswith("# Agents\n\nRules.\n") and text.count(INSTALL_LINE) == 1


@pytest.mark.req("lockstep-init/init-prints-the-codex-commands-and-the-install-line")
def test_init_leaves_a_missing_or_symlinked_agents_md_alone(tmp_path, capsys):
    root = _repo(tmp_path)
    assert init_repo(root) == 0
    assert not (root / "AGENTS.md").exists()
    assert INSTALL_LINE in capsys.readouterr().out
    source = tmp_path / "elsewhere.md"
    source.write_text("# Shared\n")
    (root / "AGENTS.md").symlink_to(source)
    assert init_repo(root) == 0
    assert source.read_text() == "# Shared\n"


@pytest.mark.req("lockstep-init/a-bad-skills-value-stops-init")
@pytest.mark.parametrize("skills, word", [(f"{{mode: sometimes, marketplace: {MIRROR}}}", "sometimes"),
                                          ("{mode: block, marketplace: not a repo}", "not a repo"),
                                          ("{mode: block}", "marketplace")])
def test_a_bad_skills_value_stops_init(tmp_path, capsys, skills, word):
    root = _repo(tmp_path, skills)
    assert init_cli(["--repo", str(root)]) == 2
    err = capsys.readouterr().err
    assert "planning.skills" in err and word in err and "line 5" in err


@pytest.mark.req("lockstep-projection/a-deleted-enabledplugins-entry-refuses-under-block-and-warns-under-warn")
def test_a_deleted_enabledplugins_entry_refuses_under_block_and_warns_under_warn(tmp_path, capsys):
    root = _repo(tmp_path)
    init_repo(root)
    data = _settings(root)
    del data["enabledPlugins"][PLUGIN]
    _write_settings(root, data)
    capsys.readouterr()
    assert run(["project", "--repo", str(root)]) == 1
    out = capsys.readouterr().out
    assert f"refused: planning.skills: {SETTINGS} has no enabledPlugins.{PLUGIN}" in out and "lockstep init" in out
    (root / "lockstep.yaml").write_text((root / "lockstep.yaml").read_text().replace("mode: block", "mode: warn"))
    assert run(["project", "--repo", str(root)]) == 0
    out = capsys.readouterr().out
    assert f"warning: planning.skills: {SETTINGS} has no enabledPlugins.{PLUGIN}" in out


@pytest.mark.req("lockstep-projection/a-conflict-only-warns")
@pytest.mark.parametrize("existing", [
    {"extraKnownMarketplaces": {"inside-success": _wanted_source("BrianMills2718/company-planning")},
     "enabledPlugins": {PLUGIN: True}},
    {"extraKnownMarketplaces": {"inside-success": _wanted_source()}, "enabledPlugins": {PLUGIN: False}},
])
def test_a_conflict_only_warns(tmp_path, capsys, existing):
    root = _repo(tmp_path)
    _write_settings(root, existing)
    refusals, warnings = drift(root)
    assert refusals == [] and len(warnings) == 1 and "lockstep init" in warnings[0]
    assert run(["project", "--repo", str(root)]) == 0
    assert "warning: planning.skills" in capsys.readouterr().out


def test_repository_is_compared_without_letter_case(tmp_path):
    root = _repo(tmp_path)
    _write_settings(root, {"extraKnownMarketplaces": {"inside-success": _wanted_source(MIRROR.lower())},
                           "enabledPlugins": {PLUGIN: True}})
    assert drift(root) == ([], [])


@pytest.mark.req("lockstep-projection/off-is-not-looked-at")
@pytest.mark.parametrize("skills", ["{mode: off}", None])
def test_off_is_not_looked_at(tmp_path, capsys, skills):
    root = _repo(tmp_path, skills)
    assert drift(root) == ([], [])
    assert run(["project", "--repo", str(root)]) == 0
    assert "skills" not in capsys.readouterr().out


@pytest.mark.req("lockstep-projection/a-bad-skills-value-is-named-with-its-line-and-ship-ignores-it")
@pytest.mark.parametrize("skills, word", [(f"{{mode: sometimes, marketplace: {MIRROR}}}", "sometimes"),
                                          ("{mode: warn, marketplace: https://github.com/a/b}", "https://github.com/a/b"),
                                          ("[block]", "mapping")])
def test_a_bad_skills_value_is_named_with_its_line_and_ship_ignores_it(tmp_path, capsys, skills, word):
    root = _repo(tmp_path, skills)
    problems = [p for p in side_file_problems(root, {}) if "planning.skills" in p]
    assert len(problems) == 1 and word in problems[0] and "line 5" in problems[0]
    assert run(["project", "--repo", str(root)]) == 1
    out = capsys.readouterr().out
    assert "refused: planning.skills" in out and "line 5" in out
    data = yaml.safe_load((root / "lockstep.yaml").read_text())
    assert planning_modes(data) == {"gate": "warn", "one_page_plans": "warn"}


def test_fresh_lockstep_yaml_holds_the_key_commented_out(tmp_path, capsys):
    root = tmp_path / "fresh"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    assert init_repo(root, owner="Acme") == 0
    text = (root / "lockstep.yaml").read_text()
    assert f"# skills: {{mode: block, marketplace: {MIRROR}}}" in text
    assert "skills" not in (yaml.safe_load(text)["planning"])
    assert PLUGIN not in (root / SETTINGS).read_text()
