#!/usr/bin/env python3
"""Write and check a manifest of the Claude Code and Codex client settings on this machine (AES consolidation plan, item 9).

agent-skills already holds most client settings in git: `.rulesync/client-settings.jsonc` (models, effort, enabled
plugins, marketplaces, plugin options) and rulesync (`.rulesync/mcp.jsonc`, `hooks.jsonc`: MCP servers and hooks).
This manifest names, for every setting found on disk, who owns it, and holds the value only of a setting nobody
owns yet, so a clean machine loses nothing and the next unowned setting shows up as `unrecorded`.

    client_manifest.py build [--out FILE]        write the manifest (stdout without --out)
    client_manifest.py check [--manifest FILE]   disk against the manifest: same, differ, missing, unrecorded; exit 1 on differ or unrecorded

Read-only: it reads `~/.claude/settings.json`, `~/.claude.json` (MCP server names only), `~/.claude/plugins/
installed_plugins.json` and `known_marketplaces.json`, `~/.codex/config.toml` and the agent-skills manifests, and
writes nothing but `--out`. A value whose key name or text looks like a credential is never written, only its name.

Implements: client-manifest/every-setting-has-an-owner
Implements: client-manifest/owned-settings-hold-no-value
Implements: client-manifest/no-secret-values-are-written
Implements: client-manifest/disk-is-compared-with-the-manifest
Implements: client-manifest/output-is-stable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

import yaml

SETTINGS = "agent-skills client-settings"
SEEDED = "runtime (agent-skills client-settings seeds it)"
RULESYNC = "agent-skills rulesync"
RUNTIME = "runtime"
HERE = "client-layer"
NONE = "none"
# Codex keys whose content the client or a sync job rewrites; recorded by owner only, never compared by value.
CODEX_GROUPS = {"projects": RUNTIME, "hooks.state": RULESYNC + " (codex_hook_trust.py)",
                "tui.model_availability_nux": RUNTIME}
SECRET_NAME = re.compile(r"token|secret|passw|api[_-]?key|bearer|auth|credential|cookie|header", re.I)
SECRET_TEXT = re.compile(r"^(sk-|ghp_|gho_|ghs_|github_pat_|xox[abpr]-|AKIA)|^(?![/~{])(?=.*\d)(?=.*[A-Za-z])[A-Za-z0-9+/_=-]{32,}$")
WITHHELD = "<withheld: name only>"


def _jsonc(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(re.sub(r"^\s*//.*$", "", path.read_text(), flags=re.M))


def _json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def safe(key: str, value: Any, home: str) -> Any:
    """The value with the home folder as {{HOME}}; anything named or shaped like a credential is withheld.

    Implements: client-manifest/no-secret-values-are-written
    """
    if SECRET_NAME.search(key):
        return WITHHELD
    if isinstance(value, dict):
        return {k: safe(str(k), v, home) for k, v in value.items()}
    if isinstance(value, list):
        return [safe(key, v, home) for v in value]
    if isinstance(value, str):
        return WITHHELD if SECRET_TEXT.search(value) else value.replace(home, "{{HOME}}")
    return value


def _entry(owner: str, key: str, value: Any, home: str) -> dict:
    """Implements: client-manifest/owned-settings-hold-no-value"""
    return {"owner": owner, "value": safe(key, value, home)} if owner == HERE else {"owner": owner}


def _leaves(data: dict, prefix: str = "") -> dict[str, Any]:
    """Dotted leaf paths of a TOML table; the CODEX_GROUPS and each MCP server stop the descent."""
    out: dict[str, Any] = {}
    for k, v in data.items():
        path = f"{prefix}{k}"
        if path in CODEX_GROUPS or not isinstance(v, dict):
            out[path] = v
        else:
            out.update(_leaves(v, path + "."))
    return out


def build(home: Path, agent_skills: Path) -> dict:
    """The manifest as data, keys sorted, no timestamp.

    Implements: client-manifest/every-setting-has-an-owner
    Implements: client-manifest/output-is-stable
    """
    h = str(home)
    cs = _jsonc(agent_skills / ".rulesync/client-settings.jsonc")
    mcp = _jsonc(agent_skills / ".rulesync/mcp.jsonc")
    shared = set(mcp.get("mcpServers", {}))
    hooks_owned = (agent_skills / ".rulesync/hooks.jsonc").exists()
    cc, cx = cs.get("claudecode", {}), cs.get("codexcli", {})

    def claude_owner(key: str) -> str:
        if key == "hooks" and hooks_owned:
            return RULESYNC
        if key in cc.get("settings", {}):
            return SETTINGS
        return SEEDED if key in cc.get("defaults_only", {}) else HERE

    def codex_owner(key: str) -> str:
        if key in CODEX_GROUPS:
            return CODEX_GROUPS[key]
        if key in cx.get("settings", {}):
            return SETTINGS
        return SEEDED if key in cx.get("defaults_only", {}) else HERE

    settings = _json(home / ".claude/settings.json")
    claude_mcp = set(_json(home / ".claude.json").get("mcpServers", {}))
    want_claude_mcp = shared | set(mcp.get("claudecode", {}).get("mcpServers", {}))
    plugins = _json(home / ".claude/plugins/installed_plugins.json").get("plugins", {})
    enabled = cc.get("settings", {}).get("enabledPlugins", {})
    markets = _json(home / ".claude/plugins/known_marketplaces.json")
    known = cc.get("settings", {}).get("extraKnownMarketplaces", {})
    claude_plugins = {}
    for name, installs in sorted(plugins.items()):
        first = installs[0] if isinstance(installs, list) and installs else {}
        claude_plugins[name] = {"owner": SETTINGS if name in enabled else HERE,
                                "version": first.get("version"), "commit": first.get("gitCommitSha")}

    codex_path = home / ".codex/config.toml"
    codex = tomllib.loads(codex_path.read_text()) if codex_path.exists() else {}
    codex_mcp = set(codex.pop("mcp_servers", {}))
    want_codex_mcp = shared | set(mcp.get("codexcli", {}).get("mcpServers", {}))
    leaves = _leaves(codex)
    return {
        "generated_by": "aes scripts/client_manifest.py build",
        "claude": {
            "settings": {k: _entry(claude_owner(k), k, settings[k], h) for k in sorted(settings)},
            "mcp_servers": {n: {"owner": RULESYNC if n in want_claude_mcp else NONE} for n in sorted(claude_mcp)},
            "plugins": claude_plugins,
            "marketplaces": {n: _entry(SETTINGS if n in known else HERE, n, markets[n].get("source"), h)
                             for n in sorted(markets)},
        },
        "codex": {
            "settings": {k: _entry(codex_owner(k), k, leaves[k], h) for k in sorted(leaves)},
            "mcp_servers": {n: {"owner": RULESYNC if n in want_codex_mcp else NONE} for n in sorted(codex_mcp)},
        },
    }


def entries(manifest: dict) -> dict[str, dict]:
    """Every entry by `client section key`."""
    out: dict[str, dict] = {}
    for client in ("claude", "codex"):
        for section, items in (manifest.get(client) or {}).items():
            for key, entry in (items or {}).items():
                out[f"{client} {section} {key}"] = entry
    return out


def compare(current: dict, recorded: dict) -> dict[str, list[str]]:
    """same, differ (owner or recorded value changed), missing (in the manifest, not on disk), unrecorded
    (on disk, not in the manifest), and plugin versions that moved (reported, never a failure).

    Implements: client-manifest/disk-is-compared-with-the-manifest
    """
    now, before = entries(current), entries(recorded)
    out: dict[str, list[str]] = {"same": [], "differ": [], "missing": [], "unrecorded": [], "version-changed": []}
    for key in sorted(set(now) | set(before)):
        a, b = now.get(key), before.get(key)
        if a is None:
            out["missing"].append(key)
        elif b is None:
            out["unrecorded"].append(key)
        elif a.get("owner") != b.get("owner") or a.get("value") != b.get("value"):
            out["differ"].append(key)
        else:
            out["same"].append(key)
            if (a.get("version"), a.get("commit")) != (b.get("version"), b.get("commit")):
                out["version-changed"].append(key)
    return out


def dump(manifest: dict) -> str:
    return yaml.safe_dump(manifest, sort_keys=False, default_flow_style=False, width=1000)


def owners(manifest: dict) -> str:
    counts: dict[str, int] = {}
    for entry in entries(manifest).values():
        counts[entry["owner"]] = counts.get(entry["owner"], 0) + 1
    return ", ".join(f"{o} {n}" for o, n in sorted(counts.items()))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["build", "check"])
    ap.add_argument("--home", type=Path, default=Path.home())
    ap.add_argument("--agent-skills", type=Path, default=Path.home() / "code2/agent-skills")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--manifest", type=Path, default=Path.home() / "code2/aes-config/client-layer.yaml")
    a = ap.parse_args(argv)
    current = build(a.home, a.agent_skills)
    if a.command == "build":
        if a.out:
            a.out.write_text(dump(current))
            print(f"client_manifest: wrote {len(entries(current))} entries to {a.out} (owners: {owners(current)})")
        else:
            sys.stdout.write(dump(current))
        return 0
    if not a.manifest.exists():
        print(f"client_manifest: no manifest at {a.manifest}")
        return 1
    found = compare(current, yaml.safe_load(a.manifest.read_text()) or {})
    print(f"client_manifest: {a.manifest} against disk: same {len(found['same'])}, differ {len(found['differ'])}, "
          f"missing {len(found['missing'])}, unrecorded {len(found['unrecorded'])}; "
          f"plugin versions changed {len(found['version-changed'])} (not a failure)")
    print(f"client_manifest: owners on disk: {owners(current)}")
    for kind in ("differ", "missing", "unrecorded", "version-changed"):
        for key in found[kind]:
            print(f"  {kind}: {key}")
    rc = 1 if found["differ"] or found["unrecorded"] else 0
    print(f"RESULT client-manifest-check differ={len(found['differ'])} unrecorded={len(found['unrecorded'])} exit={rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
