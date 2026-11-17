import json
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import client_manifest as m  # noqa: E402

SECRET = "ghp" + "_" + "TestNotARealValue0123456789abcdefABCD"  # assembled so secret scanners see no token literal


@pytest.fixture
def machine(tmp_path):
    """A home folder with both clients' settings and an agent-skills checkout that owns some of them."""
    home, skills = tmp_path / "home", tmp_path / "agent-skills"
    (home / ".claude/plugins").mkdir(parents=True)
    (home / ".codex").mkdir()
    (skills / ".rulesync").mkdir(parents=True)
    (skills / ".rulesync/client-settings.jsonc").write_text(
        "// comment\n" + json.dumps({
            "claudecode": {"defaults_only": {"model": "opus"},
                           "settings": {"availableModels": ["opus"], "enabledPlugins": {"router@router": True},
                                        "extraKnownMarketplaces": {"router": {}}}},
            "codexcli": {"defaults_only": {"model": "gpt"}, "settings": {"plugins.github@curated.enabled": True}}}))
    (skills / ".rulesync/mcp.jsonc").write_text(json.dumps({
        "mcpServers": {"context7": {}}, "claudecode": {"mcpServers": {"github": {}}}, "codexcli": {"mcpServers": {}}}))
    (skills / ".rulesync/hooks.jsonc").write_text("{}")
    (home / ".claude/settings.json").write_text(json.dumps({
        "model": "sonnet", "availableModels": ["opus", "haiku"], "enabledPlugins": {"router@router": True},
        "hooks": {"PreToolUse": []}, "advisorModel": "opus", "apiToken": SECRET, "note": SECRET,
        "statusPath": f"{home}/bin/status"}))
    (home / ".claude.json").write_text(json.dumps({"mcpServers": {
        "github": {"env": {"GITHUB_TOKEN": SECRET}}, "context7": {}, "handmade": {"headers": {"Authorization": SECRET}}}}))
    (home / ".claude/plugins/installed_plugins.json").write_text(json.dumps({"version": 2, "plugins": {
        "router@router": [{"version": "1.0", "gitCommitSha": "abc"}], "extra@official": [{"version": "2.0"}]}}))
    (home / ".claude/plugins/known_marketplaces.json").write_text(json.dumps({
        "router": {"source": {"source": "github", "repo": "someone/router"}},
        "official": {"source": {"source": "github", "repo": "vendor/official"}}}))
    (home / ".codex/config.toml").write_text(
        'model = "luna"\napprovals_reviewer = "user"\n'
        f'[mcp_servers.handmade]\nurl = "http://x"\nbearer_token = "{SECRET}"\n'
        '[plugins."github@curated"]\nenabled = true\n'
        f'[projects."{home}/repo"]\ntrust_level = "trusted"\n'
        f'[features]\nhooks = false\n[provider]\napi_key = "{SECRET}"\n')
    return home, skills


def _owners(manifest):
    return {k: e["owner"] for k, e in m.entries(manifest).items()}


@pytest.mark.req("client-manifest/every-setting-has-an-owner")
def test_every_setting_on_disk_gets_its_owner(machine):
    own = _owners(m.build(*machine))
    assert own["claude settings availableModels"] == m.SETTINGS
    assert own["claude settings model"] == m.SEEDED
    assert own["claude settings hooks"] == m.RULESYNC
    assert own["claude settings advisorModel"] == m.HERE
    assert own["claude mcp_servers github"] == m.RULESYNC
    assert own["claude mcp_servers handmade"] == m.NONE
    assert own["claude plugins router@router"] == m.SETTINGS
    assert own["claude plugins extra@official"] == m.HERE
    assert own["claude marketplaces router"] == m.SETTINGS
    assert own["claude marketplaces official"] == m.HERE
    assert own["codex settings model"] == m.SEEDED
    assert own["codex settings plugins.github@curated.enabled"] == m.SETTINGS
    assert own["codex settings approvals_reviewer"] == m.HERE
    assert own["codex settings features.hooks"] == m.HERE
    assert own["codex settings projects"] == m.RUNTIME
    assert own["codex mcp_servers handmade"] == m.NONE


@pytest.mark.req("client-manifest/owned-settings-hold-no-value")
def test_only_unowned_settings_carry_a_value(machine):
    for key, entry in m.entries(m.build(*machine)).items():
        assert ("value" in entry) == (entry["owner"] == m.HERE and " plugins " not in key), key
    built = m.build(*machine)
    assert built["claude"]["settings"]["advisorModel"]["value"] == "opus"
    assert built["claude"]["marketplaces"]["official"]["value"] == {"source": "github", "repo": "vendor/official"}


@pytest.mark.req("client-manifest/no-secret-values-are-written")
def test_no_credential_reaches_the_manifest(machine):
    home, _ = machine
    text = m.dump(m.build(*machine))
    assert SECRET not in text
    assert str(home) not in text
    built = m.build(*machine)
    assert built["claude"]["settings"]["apiToken"]["value"] == m.WITHHELD
    assert built["claude"]["settings"]["note"]["value"] == m.WITHHELD
    assert built["claude"]["settings"]["statusPath"]["value"] == "{{HOME}}/bin/status"
    assert built["codex"]["settings"]["provider.api_key"]["value"] == m.WITHHELD


@pytest.mark.req("client-manifest/disk-is-compared-with-the-manifest")
def test_check_counts_and_exit(machine, tmp_path, capsys):
    home, skills = machine
    saved = tmp_path / "client-layer.yaml"
    args = ["--home", str(home), "--agent-skills", str(skills), "--manifest", str(saved)]
    assert m.main(["build", "--out", str(saved), *args[:4]]) == 0
    assert m.main(["check", *args]) == 0
    assert "differ 0, missing 0, unrecorded 0" in capsys.readouterr().out

    settings = home / ".claude/settings.json"
    data = json.loads(settings.read_text())
    data["availableModels"] = ["sonnet"]  # owned by agent-skills: its own check compares the value
    settings.write_text(json.dumps(data))
    plugins = home / ".claude/plugins/installed_plugins.json"
    p = json.loads(plugins.read_text())
    p["plugins"]["router@router"][0]["version"] = "1.1"
    plugins.write_text(json.dumps(p))
    assert m.main(["check", *args]) == 0
    assert "plugin versions changed 1" in capsys.readouterr().out

    data["advisorModel"] = "haiku"
    del data["note"]
    data["newKey"] = 1
    settings.write_text(json.dumps(data))
    assert m.main(["check", *args]) == 1
    out = capsys.readouterr().out
    assert "differ 1, missing 1, unrecorded 1" in out
    assert "differ: claude settings advisorModel" in out
    assert "unrecorded: claude settings newKey" in out

    del data["advisorModel"], data["newKey"]
    settings.write_text(json.dumps(data))
    assert m.main(["check", *args]) == 0  # missing alone: a clean machine lacks settings until they are applied


@pytest.mark.req("client-manifest/disk-is-compared-with-the-manifest")
def test_check_without_a_manifest_fails(machine, tmp_path):
    home, skills = machine
    assert m.main(["check", "--home", str(home), "--agent-skills", str(skills),
                   "--manifest", str(tmp_path / "none.yaml")]) == 1


@pytest.mark.req("client-manifest/output-is-stable")
def test_build_is_stable_and_sorted(machine):
    first, second = m.dump(m.build(*machine)), m.dump(m.build(*machine))
    assert first == second
    keys = list(yaml.safe_load(first)["claude"]["settings"])
    assert keys == sorted(keys)
    assert "generated" in first and "20" not in yaml.safe_load(first)["generated_by"]
