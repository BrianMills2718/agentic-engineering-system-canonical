"""`planning.skills`: the Company Planning plugin keys in a repository's `.claude/settings.json`.

`lockstep init` calls `merge` (wrote, skipped or conflict; never overwrites another source or an opt-out `false`);
`lockstep check project` calls `drift` (refusals and warnings). Neither touches the network or `~/.codex/`; Codex has no
per-repository plugin config, so init only prints `codex_commands`.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:plugin_settings.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-init/init-writes-the-company-planning-plugin-keys-when-planning-skills-is-on, lockstep-projection/the-project-check-reports-company-planning-plugin-drift

### Requirement: Init writes the Company Planning plugin keys when planning.skills is on

When `planning.skills` in `lockstep.yaml` is `{mode: block|warn, marketplace: OWNER/REPO}`, `lockstep init` SHALL merge into `.claude/settings.json` the marketplace `inside-success` (`extraKnownMarketplaces.inside-success.source` = `{source: github, repo: OWNER/REPO}`) and `enabledPlugins."company-planning@inside-success": true`, keeping every other key, and SHALL print `wrote`, `skipped` (everything already matches) or `conflict` for `planning.skills`. It SHALL never overwrite an `inside-success` entry with another source or repository, nor an `enabledPlugins` value that is not `true` (a `false` is a person opting out); each is named in a `conflict` line and left as it is. Extra fields such as `autoUpdate` SHALL be kept and SHALL NOT count as a difference. A `.claude/settings.json` that is not valid JSON SHALL make init exit 2. With `mode: off` or no `skills` key it SHALL write and remove nothing for this setting. When on, it SHALL print the two Codex commands with the configured address (`codex plugin marketplace add OWNER/REPO`, `codex plugin add company-planning@inside-success`), reading and writing nothing in `~/.codex/`, and the Claude Code project commands: list marketplaces, register the configured `OWNER/REPO` with `--scope project` only when `inside-success` is absent, then run `claude plugin install company-planning@inside-success --scope project`; it SHALL add that line once to an existing, non-symlinked `AGENTS.md` under a `## Company Planning plugin` heading, and otherwise only print it. A `skills` value with an unknown mode or a marketplace that is not `owner/repo` (or missing when on) SHALL make init exit 2 naming the line. A fresh `lockstep.yaml` SHALL hold the key commented out.

Source: Brian, 2026-11-25, the settings model adopted in docs/planning/next.goal.md ("Company Planning skills | per-person plugin install | slice 3": "the whole systm should be configurable so you can congfigure what is on or off"); slice 3 planned in full 2026-11-26 in docs/planning/next.goal.md, with one independent read. Inferred by agent: `off` is the default (this switch writes files), no default address (as slice 2), the AGENTS.md note goes only into an existing non-symlinked file (a symlinked AGENTS.md is another repository's source).

#### Scenario: Block writes the keys and a second run skips them

- **GIVEN** a repository whose `lockstep.yaml` says `planning: {skills: {mode: block, marketplace: Inside-Success/company-planning}}`
- **WHEN** `lockstep init` runs twice
- **THEN** the first run prints `wrote   planning.skills`, `.claude/settings.json` holds both keys beside the Lockstep hooks, `lockstep check project` reports no skills problem, and the second run prints `skipped planning.skills` and changes no file

#### Scenario: Warn also writes the keys

- **GIVEN** `planning.skills.mode: warn` with a marketplace
- **WHEN** `lockstep init` runs
- **THEN** both keys are written

#### Scenario: The keys merge into existing settings

- **GIVEN** a `.claude/settings.json` with other keys and hooks
- **WHEN** `lockstep init` runs with skills on
- **THEN** those keys and hooks remain and both plugin keys are added

#### Scenario: A malformed settings file exits 2

- **GIVEN** a `.claude/settings.json` that is not valid JSON and skills on
- **WHEN** `lockstep init` runs
- **THEN** it exits 2 and the file is unchanged

#### Scenario: Off writes nothing and keeps what exists

- **GIVEN** `planning.skills.mode: off`, or no `skills` key, and a settings file already holding the plugin keys
- **WHEN** `lockstep init` runs
- **THEN** the plugin keys are left exactly as they were, none are added to a file without them, and no Codex or install line is printed

#### Scenario: Another source or an opt-out is a conflict left as it is

- **GIVEN** a settings file whose `inside-success` names another repository, or whose `enabledPlugins` entry is `false`
- **WHEN** `lockstep init` runs with skills on
- **THEN** it prints `conflict planning.skills` with a line naming the key, and that value is unchanged

#### Scenario: autoUpdate is tolerated

- **GIVEN** the wanted `inside-success` entry with `autoUpdate: true` added
- **WHEN** `lockstep init` runs
- **THEN** it prints `skipped planning.skills` and the field stays

#### Scenario: Init prints the Codex commands and the install line

- **GIVEN** skills on with marketplace `Inside-Success/company-planning` and an existing `AGENTS.md`
- **WHEN** `lockstep init` runs twice
- **THEN** it prints `codex plugin marketplace add Inside-Success/company-planning`, `codex plugin add company-planning@inside-success` and the ordered Claude marketplace list, conditional project registration and project install commands, and `AGENTS.md` points to registration before its single install line

#### Scenario: A bad skills value stops init

- **GIVEN** `planning.skills` with mode `sometimes`, or a marketplace `not a repo`
- **WHEN** `lockstep init` runs
- **THEN** it exits 2 naming `planning.skills` and the line of `lockstep.yaml`

### Requirement: The project check reports Company Planning plugin drift

`lockstep check project` SHALL compare `.claude/settings.json` in the working tree with `planning.skills` in `lockstep.yaml`, with no network, looking only at whether `extraKnownMarketplaces.inside-success.source` is `{source: github, repo: <marketplace>}` (repository compared without letter case) and `enabledPlugins."company-planning@inside-success"` is `true`. A missing key or file SHALL print a `refused:` line under `mode: block` (and make the check exit 1) and a `warning:` line under `warn`; under `off` or no `skills` key nothing SHALL be looked at. A conflict (another source or repository, or an `enabledPlugins` value that is not `true`, such as an opt-out `false`) SHALL only print a `warning:` line naming the key, whatever the mode. Each line SHALL name `lockstep init` as the fix. A bad `skills` value (unknown mode, marketplace not `owner/repo` or missing when on) SHALL be refused naming its line in `lockstep.yaml`, and SHALL also be named by the side-file check; `ship`'s `planning_modes` SHALL NOT validate `skills`, so it never stops a merge. The check adds no name to `checks:`.

Source: Brian, 2026-11-25, the settings model adopted in docs/planning/next.goal.md ("Company Planning skills | per-person plugin install | slice 3"); slice 3 planned in full 2026-11-26 in docs/planning/next.goal.md ("Drift check, inside `lockstep check project`", "Not a ship gate"). Inferred by agent: the check rides on `project` so the lefthook command init generates stays unchanged in existing repositories.

#### Scenario: A deleted enabledPlugins entry refuses under block and warns under warn

- **GIVEN** a repository init wrote the keys into, then `enabledPlugins` lost its `company-planning@inside-success` entry
- **WHEN** `lockstep check project` runs with `planning.skills.mode` block, then warn
- **THEN** under block it prints a `refused:` line naming the key and `lockstep init` and exits 1; under warn it prints a `warning:` line and exits 0

#### Scenario: A conflict only warns

- **GIVEN** `.claude/settings.json` naming another `inside-success` repository, or `enabledPlugins` set to `false`
- **WHEN** `lockstep check project` runs under `block`
- **THEN** it prints a `warning:` line naming the key and the drift adds no failure

#### Scenario: Off is not looked at

- **GIVEN** `planning.skills.mode: off` and no plugin keys
- **WHEN** `lockstep check project` runs
- **THEN** it prints no skills line

#### Scenario: A bad skills value is named with its line and ship ignores it

- **GIVEN** `planning.skills` with an unknown mode, or a marketplace that is not `owner/repo`
- **WHEN** the side-file check and `lockstep check project` run, and `planning_modes` reads the file
- **THEN** both checks name `planning.skills` and the line, and `planning_modes` returns the gate modes without error

Tested by: tests/test_plugin_settings.py

Declares (typed signatures, from the plan):
  read_setting(text: str) -> tuple[Setting, str | None]
  setting(root: Path) -> Setting
  wanted(marketplace: str) -> dict
  merge(path: Path, wanted_setting: Setting) -> tuple[str, list[str]]
  drift(root: Path) -> tuple[list[str], list[str]]
  codex_commands(marketplace: str) -> list[str]
  agents_note(path: Path) -> str
[[[end]]]
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import NamedTuple

import yaml

MARKETPLACE = "inside-success"
PLUGIN = f"company-planning@{MARKETPLACE}"
SETTINGS = ".claude/settings.json"
SIDE_FILE = "lockstep.yaml"
MODES = ("block", "warn", "off")
INSTALL_LINE = f"claude plugin install {PLUGIN} --scope project"
AGENTS_HEADING = "## Company Planning plugin"
_REPO = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/[A-Za-z0-9._-]+$")


class Setting(NamedTuple):
    mode: str  # block, warn or off
    marketplace: str | None  # GitHub owner/repo of the marketplace, None when off and unset


def _skills_line(text: str) -> int | None:
    """The 1-based line of `planning.skills` in lockstep.yaml text, or None."""
    try:
        node = yaml.compose(text)
    except yaml.YAMLError:
        return None
    for path in ("planning", "skills"):
        if not isinstance(node, yaml.MappingNode):
            return None
        found = [(k, v) for k, v in node.value if getattr(k, "value", None) == path]
        if not found:
            return None
        key, node = found[0]
    return key.start_mark.line + 1


def read_setting(text: str) -> tuple[Setting, str | None]:
    """The `planning.skills` setting in lockstep.yaml text and its problem (None when sound).

    Absent means off. A bare `false`/`off` means off; otherwise it must be a mapping with `mode` (block, warn or off,
    bare true/false as elsewhere) and `marketplace` (`owner/repo`, required unless off).
    """
    try:
        data = yaml.safe_load(text) or {}
    except yaml.YAMLError:
        return Setting("off", None), None  # the side-file check names unreadable YAML
    planning = data.get("planning") if isinstance(data, dict) else None
    raw = planning.get("skills") if isinstance(planning, dict) else None
    off = Setting("off", None)
    if raw is None or raw is False or raw == "off":
        return off, None
    where = f"planning.skills ({SIDE_FILE} line {_skills_line(text)})"
    if not isinstance(raw, dict):
        return off, f"{where}: must be a mapping {{mode: block|warn|off, marketplace: OWNER/REPO}}, not {raw!r}"
    unknown = sorted(str(k) for k in set(raw) - {"mode", "marketplace"})
    if unknown:
        return off, f"{where}: unknown key {unknown[0]!r}; it holds only mode and marketplace"
    mode = raw.get("mode", "off")
    mode = "off" if mode is False else "block" if mode is True else mode
    if mode not in MODES:
        return off, f"{where}: mode is {mode!r}; it must be one of {', '.join(MODES)}"
    market = raw.get("marketplace")
    if market is None:
        if mode != "off":
            return off, f"{where}: marketplace is missing; name the GitHub OWNER/REPO of the Company Planning marketplace"
        return off, None
    if not isinstance(market, str) or not _REPO.match(market):
        return off, f"{where}: marketplace is {market!r}; it must be a GitHub OWNER/REPO such as Inside-Success/company-planning"
    return Setting(str(mode), market), None


def setting(root: Path) -> Setting:
    """The setting in `root/lockstep.yaml` (working tree); off when the file is absent.

    Raises:
        ValueError: The value is not usable (`read_setting`'s problem, with its line).
    """
    path = root / SIDE_FILE
    if not path.is_file():
        return Setting("off", None)
    found, problem = read_setting(path.read_text(encoding="utf-8"))
    if problem:
        raise ValueError(problem)
    return found


def wanted(marketplace: str) -> dict:
    """The two keys `.claude/settings.json` must hold for `marketplace` (GitHub owner/repo)."""
    return {"extraKnownMarketplaces": {MARKETPLACE: {"source": {"source": "github", "repo": marketplace}}},
            "enabledPlugins": {PLUGIN: True}}


def _compare(data: dict, marketplace: str) -> tuple[list[str], list[str]]:
    """(missing, conflicts) for parsed settings: each a dotted key, conflicts with what was found."""
    missing: list[str] = []
    conflicts: list[str] = []
    markets = data.get("extraKnownMarketplaces")
    entry = markets.get(MARKETPLACE) if isinstance(markets, dict) else None
    if entry is None:
        missing.append(f"extraKnownMarketplaces.{MARKETPLACE}")
    else:
        source = entry.get("source") if isinstance(entry, dict) else None
        ok = (isinstance(source, dict) and source.get("source") == "github"
              and str(source.get("repo", "")).lower() == marketplace.lower())
        if not ok:
            conflicts.append(f"extraKnownMarketplaces.{MARKETPLACE} names another source ({json.dumps(source)}),"
                             f" not github {marketplace}")
    plugins = data.get("enabledPlugins")
    value = plugins.get(PLUGIN) if isinstance(plugins, dict) else None
    if value is None:
        missing.append(f"enabledPlugins.{PLUGIN}")
    elif value is not True:
        why = " (opted out)" if value is False else ""
        conflicts.append(f"enabledPlugins.{PLUGIN} is {json.dumps(value)}{why}")
    return missing, conflicts


def _load(path: Path) -> dict:
    """Parsed settings (empty when absent). Raises ValueError when not a JSON object."""
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))  # json.JSONDecodeError is a ValueError
    if not isinstance(data, dict):
        raise ValueError(f"{SETTINGS} must hold a JSON object")
    return data


def merge(path: Path, wanted_setting: Setting) -> tuple[str, list[str]]:
    """Add the missing plugin keys to the settings file at `path`, keeping every other key.

    Returns:
        (`wrote` | `skipped` | `conflict`, notes). A conflicting value is never overwritten and is named in the notes;
        a missing key beside it is still added. Under `off` nothing is read or written (`skipped`).

    Raises:
        ValueError: The file is not a JSON object.
    """
    if wanted_setting.mode == "off" or not wanted_setting.marketplace:
        return "skipped", []
    data = _load(path)
    missing, conflicts = _compare(data, wanted_setting.marketplace)
    keys = wanted(wanted_setting.marketplace)
    for dotted in missing:
        section, key = dotted.split(".", 1)
        block = data.get(section)
        if not isinstance(block, dict):
            block = data[section] = {}
        block[key] = keys[section][key]
    if missing:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    if conflicts:
        return "conflict", [f"{c}; left as it is" for c in conflicts]
    return ("wrote" if missing else "skipped"), [f"added {m}" for m in missing]


def drift(root: Path) -> tuple[list[str], list[str]]:
    """(refusals, warnings) for `lockstep check project`: `.claude/settings.json` against `planning.skills`.

    A bad setting is a refusal naming its line. A missing key refuses under block and warns under warn; a conflict
    only warns; off looks at nothing.
    """
    path = root / SIDE_FILE
    if not path.is_file():
        return [], []
    found, problem = read_setting(path.read_text(encoding="utf-8"))
    if problem:
        return [problem], []
    if found.mode == "off" or not found.marketplace:
        return [], []
    fix = "; run: lockstep init"
    try:
        data = _load(root / SETTINGS)
    except ValueError as err:
        return [f"planning.skills: {SETTINGS} is not a JSON object ({err}){fix}"], []
    missing, conflicts = _compare(data, found.marketplace)
    lines = [f"planning.skills: {SETTINGS} has no {m}{fix}" for m in missing]
    warnings = [f"planning.skills: {SETTINGS} {c}; lockstep init leaves it as it is (change it by hand, or run"
                f" lockstep init after removing it)" for c in conflicts]
    if found.mode == "block":
        return lines, warnings
    return [], lines + warnings


def codex_commands(marketplace: str) -> list[str]:
    """Register the selected Git marketplace and install the plugin in Codex."""
    return [f"codex plugin marketplace add {marketplace}", f"codex plugin add {PLUGIN}"]


def agents_note(path: Path) -> str:
    """Add the per-clone install line to an existing, non-symlinked AGENTS.md once.

    Returns:
        `wrote`, `skipped` (already there) or `absent` (no file, or a symlink to another repository's source).
    """
    if path.is_symlink() or not path.is_file():
        return "absent"
    text = path.read_text(encoding="utf-8")
    if INSTALL_LINE in text:
        return "skipped"
    note = (f"\n{AGENTS_HEADING}\n\nThis repository's agents use the Company Planning skills (`planning.skills` in"
            f" `lockstep.yaml`). Once per clone, if the `inside-success` marketplace is absent, use the"
            f" registration command shown by `lockstep init`. Then run `{INSTALL_LINE}`. For Codex, run"
            f" `lockstep init` to see the Git marketplace and installation commands.\n")
    path.write_text(text + ("" if text.endswith("\n") else "\n") + note, encoding="utf-8")
    return "wrote"
