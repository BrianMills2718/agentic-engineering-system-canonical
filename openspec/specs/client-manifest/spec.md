# client-manifest Specification

## Purpose

List every Claude Code and Codex client setting on a machine (models, effort, plugins, marketplaces, MCP servers and the rest of `~/.claude/settings.json` and `~/.codex/config.toml`) with who owns it, so a clean machine can be rebuilt without losing a setting that lives only on this disk (AES consolidation plan, item 9: "Model defaults and plugin settings into the manifest"). agent-skills already holds most of these in git (`.rulesync/client-settings.jsonc`, rulesync); this manifest names that owner and holds a value only for a setting nobody owns, so the two never disagree about a value. The machinery is public in AES; the manifest names a person's plugins, paths and preferences and lives in their private configuration repository.

Source: inferred by agent (AES consolidation plan item 9, "Model defaults and plugin settings into the manifest"; no record of Brian approving item 9 itself was found, Decision 25 approved items 1 to 5; harness grid review of 2026-11-16, row `agent-config/permission-and-session-settings`: "Put model, effort, enabledPlugins and pluginConfigs in the manifest"). Also inferred by agent: recording owners instead of copying values agent-skills already holds (one source per setting, consolidation plan item 8), treating `model` and Codex `model_reasoning_effort` as owned at run time (agent-skills `client-settings.jsonc` seeds them only), and reporting plugin versions without failing on them (model-router updates itself).

## Requirements

### Requirement: every-setting-has-an-owner

`scripts/client_manifest.py build` SHALL write one entry per top-level key of `~/.claude/settings.json`, per dotted leaf key of `~/.codex/config.toml`, per MCP server name in `~/.claude.json` and in Codex `mcp_servers`, per plugin in `~/.claude/plugins/installed_plugins.json` and per marketplace in `known_marketplaces.json`. Each entry SHALL carry an owner read at build time from the agent-skills checkout (default `~/code2/agent-skills`): `agent-skills client-settings` for a key its `settings` names, `runtime (agent-skills client-settings seeds it)` for a key its `defaults_only` names, `agent-skills rulesync` for hooks and for MCP servers `mcp.jsonc` lists, `runtime` for Codex `projects` and `tui.model_availability_nux`, `none` for an MCP server nobody lists, and otherwise `client-layer`. It changes nothing on the machine.

Source: inferred by agent (AES consolidation plan item 9; basis in Purpose above)

#### Scenario: every-setting-has-an-owner

- **WHEN** the settings hold a key client-settings owns, a seeded `model`, hooks, an unowned key, a listed and an unlisted MCP server, plugins and marketplaces inside and outside client-settings, and Codex trust records
- **THEN** each entry carries the matching owner

### Requirement: owned-settings-hold-no-value

A setting or marketplace owned by `client-layer` SHALL carry its value; every other entry SHALL carry only its owner. A plugin entry SHALL carry its version and commit, never a value.

Source: inferred by agent (AES consolidation plan item 9; basis in Purpose above)

#### Scenario: owned-settings-hold-no-value

- **WHEN** the manifest is built
- **THEN** only `client-layer` settings and marketplaces have a `value`

### Requirement: no-secret-values-are-written

The manifest SHALL never hold a value whose key name looks like a credential (token, secret, password, API key, bearer, auth, credential, cookie, header) or whose text looks like one (a known token prefix, or a long run of letters and digits that is not a path); it SHALL write `<withheld: name only>` instead. MCP servers SHALL be recorded by name only. The home folder SHALL be written as `{{HOME}}`.

Source: inferred by agent (AES consolidation plan item 9; basis in Purpose above)

#### Scenario: no-secret-values-are-written

- **WHEN** a setting, a Codex table or an MCP server's environment or headers hold a token-shaped value, and a setting holds a path under the home folder
- **THEN** the token does not appear in the manifest, and neither does the home folder's path

### Requirement: disk-is-compared-with-the-manifest

`check` SHALL rebuild the manifest in memory and compare it with the saved one (default `~/code2/aes-config/client-layer.yaml`), printing counts of same, differ (owner or recorded value changed), missing (in the manifest, not on disk), unrecorded (on disk, not in the manifest) and plugins whose version or commit moved, and naming each one that is not the same. It SHALL exit 1 when any entry differs or is unrecorded, or when there is no saved manifest; missing entries and moved plugin versions do not fail it (a clean machine lacks settings until they are applied, and plugins update themselves). The value of a setting another owner holds is that owner's check to compare.

Source: inferred by agent (AES consolidation plan item 9; basis in Purpose above)

#### Scenario: disk-is-compared-with-the-manifest

- **WHEN** an unowned setting changes, one is removed and a new key appears; separately, an owned setting changes and a plugin version moves
- **THEN** the first case prints differ 1, missing 1, unrecorded 1 and exits 1; the second exits 0 and reports the moved version; with only a removed key it exits 0

### Requirement: output-is-stable

The manifest SHALL carry no timestamp and SHALL list entries in sorted order, so an unchanged machine produces the same bytes.

Source: inferred by agent (AES consolidation plan item 9; basis in Purpose above)

#### Scenario: output-is-stable

- **WHEN** `build` runs twice on unchanged settings
- **THEN** the two outputs are identical and keys are sorted
