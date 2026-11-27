"""`lockstep init [--repo PATH] [--owner NAME] [--source URL]`: install Lockstep in a repository.

Implements: lockstep-init/init-installs-lockstep-in-a-repository-without-overwriting
Implements: lockstep-init/installed-files-name-no-machine-and-read-their-settings-from-lockstep-yaml
Implements: lockstep-init/init-upgrades-its-own-old-hook-command-only-where-lockstep-yaml-sets-the-guard

Writes, each only when absent (nothing is overwritten; what was written and what was skipped is printed):

    lockstep.yaml          every commit check set to block, owner, sources.human_pattern, the planning gates,
                           `guard: {mode: block}`, empty governed and layout
    .claude/settings.json  a PreToolUse hook running `lockstep-hook` (merged into an existing file)
    .codex/hooks.json      the same hook for Codex (merged into an existing file)
    lefthook.yml           a `lockstep` pre-commit command (added to an existing file)
    .gitignore             a `.lockstep/` line, the edit guard's log folder

The hook and lefthook commands install Lockstep from a git address with `uvx`, so no file holds an absolute path.
The hook command sets no `PCW_MODE`; an earlier init's `PCW_MODE=block` command is rewritten only when lockstep.yaml
already has a `guard:` section, so an installed repository never drops from refusing to warning unasked.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:init_repo.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-init/init-installs-lockstep-in-a-repository-without-overwriting, lockstep-init/installed-files-name-no-machine-and-read-their-settings-from-lockstep-yaml, lockstep-init/init-upgrades-its-own-old-hook-command-only-where-lockstep-yaml-sets-the-guard

### Requirement: Init installs Lockstep in a repository without overwriting

`lockstep init` SHALL write, for each of these that is absent, `lockstep.yaml` (a `checks:` map setting every commit check to `block` except `maintainability`, `helper-reuse` and `mutation`, which it writes as `off` with a comment saying what each does, `owner`, `sources.human_pattern`, a `planning:` section setting `gate` and `one_page_plans` to `block` with a comment saying what each does, a `guard:` section setting `mode` to `block` with a comment saying what it does, empty `governed` and `layout`), a Claude Code PreToolUse hook in `.claude/settings.json`, a Codex PreToolUse hook in `.codex/hooks.json`, neither setting `PCW_MODE`, and a `lockstep` pre-commit command in `lefthook.yml` (which leaves those three out). It SHALL print one line per file it wrote or skipped, SHALL leave an existing `lockstep.yaml` unchanged, SHALL add its hook to an existing settings or hooks file without removing other keys, and a second run SHALL change nothing.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations" (the three written off); Brian, 2026-11-25: "the whole systm should be configurable so you can congfigure what is on or off" (the planning section, docs/planning/next.goal.md slice 1, and the guard section, parking item `guard.mode`); Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, "A concrete example of the finished tool" step 1. Writing `block` so a fresh install refuses as the hardcoded `PCW_MODE=block` did is inferred by agent.

#### Scenario: Fresh repository gets all four

- **GIVEN** an empty git repository
- **WHEN** `lockstep init` runs
- **THEN** `lockstep.yaml`, `.claude/settings.json`, `.codex/hooks.json` and `lefthook.yml` exist and each names Lockstep,
  and `lockstep.yaml` sets every check to `block` except `maintainability`, `helper-reuse` and `mutation`, set to `off`, `planning:` sets `gate` and `one_page_plans` to `block`, `guard:` sets `mode` to `block`, and no hook command holds `PCW_MODE`

#### Scenario: A second run changes nothing

- **GIVEN** a repository `lockstep init` already ran in
- **WHEN** it runs again
- **THEN** every file is byte-identical and each is reported as skipped

#### Scenario: Existing settings keep their other keys

- **GIVEN** a `.claude/settings.json` with other keys and another PreToolUse hook
- **WHEN** `lockstep init` runs
- **THEN** those remain and the Lockstep hook is added once

### Requirement: Installed files name no machine and read their settings from lockstep.yaml

Files `lockstep init` writes SHALL contain no absolute path and no `/home/`; the hook commands SHALL install Lockstep from a git address with `uvx`. `--owner` SHALL set `owner:` in `lockstep.yaml`, else the owner of the git `origin` remote, else a placeholder. `--human-pattern` SHALL set `sources.human_pattern`, else the checks' own default. The checks SHALL read their modes, `owner` and `sources.human_pattern` from `lockstep.yaml`, so a file copied from one repository works in another.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, "Nothing names Brian's machine" and acceptance A5

#### Scenario: No written file holds an absolute path

- **GIVEN** a fresh repository
- **WHEN** `lockstep init` runs
- **THEN** no file it wrote contains `/home/`, `~/` or a path starting with `/`

#### Scenario: Owner lands in lockstep.yaml

- **GIVEN** a fresh repository
- **WHEN** `lockstep init --owner Acme` runs
- **THEN** `lockstep.yaml` says `owner: Acme`

#### Scenario: A lockstep.yaml copied to another repository is read there

- **GIVEN** a `lockstep.yaml` from `init` with one check set to `warn`
- **WHEN** it is copied into another repository
- **THEN** that repository's checks read the same modes and owner

### Requirement: Init upgrades its own old hook command only where lockstep.yaml sets the guard

When a settings or hooks file holds the edit-guard command an earlier `lockstep init` wrote (exactly `PCW_MODE=block uvx --from <source> lockstep-hook`, with its client prefix or suffix), `lockstep init` SHALL rewrite that command to the current one when the repository's `lockstep.yaml` has a `guard:` section, and SHALL otherwise leave it unchanged and print a line saying to add `guard: {mode: block}` to `lockstep.yaml` and run `lockstep init` again. Any other Lockstep hook command SHALL be left unchanged.

Source: inferred by agent: dropping the hardcode without this would leave installed repositories with `PCW_MODE=block`, which wins over `guard.mode`, while rewriting it in a repository whose `lockstep.yaml` has no `guard:` would silently turn its refusals into warnings; the same exact-match rule `lockstep init` already uses for its lefthook command.

#### Scenario: An old hook command is upgraded where guard is set

- **GIVEN** `.claude/settings.json` holding the old `PCW_MODE=block` command and `lockstep.yaml` with `guard: {mode: block}`
- **WHEN** `lockstep init` runs
- **THEN** the command no longer holds `PCW_MODE`, the file is reported as written, and a second run reports it skipped

#### Scenario: An old hook command stays where guard is not set

- **GIVEN** `.claude/settings.json` holding the old `PCW_MODE=block` command and `lockstep.yaml` with no `guard:` section
- **WHEN** `lockstep init` runs
- **THEN** the command is unchanged and the output says to add `guard: {mode: block}`

#### Scenario: A custom hook command is left alone

- **GIVEN** `.claude/settings.json` holding a `lockstep-hook` command init did not write and `lockstep.yaml` with `guard:`
- **WHEN** `lockstep init` runs
- **THEN** the command is unchanged

Tested by: tests/lockstep/test_lockstep_init.py, tests/test_plugin_settings.py
[[[end]]]
"""

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from lockstep.checks import plugin_settings
from lockstep.checks.config import CHECK_NAMES, DEFAULT_OFF
from lockstep.checks.sources import DEFAULT_HUMAN_PATTERN

SOURCE = "git+https://github.com/BrianMills2718/agentic-engineering-system-canonical"
OWNER_PLACEHOLDER = "YOUR-GITHUB-OWNER"
HOOK_NAMES = ("lockstep-hook", "pcw-hook")


def owner_from_origin(url: str) -> str | None:
    """The owner in a git remote URL (`https://host/OWNER/name.git` or `git@host:OWNER/name.git`), or None."""
    match = re.search(r"[:/]([^/:\s]+)/[^/\s]+?(?:\.git)?/?$", url.strip())
    return match.group(1) if match else None


def _origin_owner(root: Path) -> str | None:
    done = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"], capture_output=True, text=True)
    return owner_from_origin(done.stdout) if done.returncode == 0 else None


def lockstep_yaml(owner: str, human_pattern: str = DEFAULT_HUMAN_PATTERN) -> str:
    """The text of a fresh `lockstep.yaml`: every check on block except the DEFAULT_OFF three (off), the owner, the human-source pattern, an empty plan."""
    notes = {"maintainability": "new broad excepts, bare except-pass, complexity, duplicate blocks, file growth",
             "helper-reuse": "LLM report: new functions that duplicate an existing helper (needs llm_client)",
             "mutation": "nightly mutmut run listing surviving mutants (needs mutmut)"}
    checks = "\n".join(f"  {name}: off  # {notes[name]}; set block or warn to switch on" if name in DEFAULT_OFF
                        else f"  {name}: block" for name in CHECK_NAMES)
    return f"""# Lockstep's settings (docs: README.md, "Install Lockstep in a repository").
schema: lockstep.side.v1

# Each commit check (`lockstep check <name>`) is block (fail the commit), warn (print and pass) or off (skip).
checks:
{checks}

# The GitHub owner of this repository's organization or account.
owner: {owner}

sources:
  # A `Source:` line starting with this regex counts as a human's word; `Source: inferred by agent (...)` never does.
  human_pattern: "{human_pattern}"

# The planning part: ship's two planning gates, each block, warn (print the plan verdict and merge) or off.
# ship reads them from the default branch, so a branch cannot change its own gate.
planning:
  gate: block            # the Company Planning package (docs/planning/planning-package.json) must pass its validator
  one_page_plans: block  # a one-page plan under docs/plans/ must be complete
  # validator:            # where the validator comes from; unset means your local company-planning checkout
  #   repo: <git address of Company Planning or its mirror>
  #   ref: main
  # Load the Company Planning plugin for agents here: `lockstep init` writes its keys into .claude/settings.json and
  # `lockstep check project` reports drift (block, warn or off; marketplace is the plugin's GitHub OWNER/REPO).
  # skills: {{mode: block, marketplace: Inside-Success/company-planning}}

# The edit guard (the agent hook): block refuses an edit to an unplanned governed file, warn lets it through with the
# refusal text as a warning, and off skips the guard. A valid PCW_MODE overrides the setting for that session.
guard:
  mode: block

# Folders where every file must be planned (for example [src/]). Empty means the edit guard checks no folder.
governed: []

# The plan's files: path, purpose, implements (OpenSpec requirement IDs), tests. `lockstep layout` creates them.
layout: []
"""


def _guard_command(source: str, client: str, prefix: str = "") -> str:
    """The edit-guard command for `client`; `prefix` is what an earlier init put before uvx (`PCW_MODE=block `)."""
    guard = f"{prefix}uvx --from {source} lockstep-hook"
    return f"{guard} --client codex" if client == "codex" else f'cd "$CLAUDE_PROJECT_DIR" && {guard}'


def _hook_entry(source: str, client: str) -> dict:
    """One PreToolUse entry for `client` (`claude` or `codex`): the edit guard, installed from `source` by uvx.

    No `PCW_MODE` in the command: the hook reads `guard.mode` from lockstep.yaml, which init writes.
    """
    matcher = "apply_patch|Edit|Write|Bash|shell|exec_command" if client == "codex" else "Edit|Write|MultiEdit|NotebookEdit|Bash"
    return {"matcher": matcher, "hooks": [{"type": "command", "command": _guard_command(source, client), "timeout": 30}]}


def _upgrade_old_guard(hooks: list, source: str, client: str, upgrade: bool) -> str | None:
    """Rewrite the exact command an earlier init wrote (`PCW_MODE=block uvx ...`) when `upgrade`.

    Returns `wrote` after a rewrite, `old` when the old command is there but `upgrade` is False, None when it is absent.
    """
    old, new = _guard_command(source, client, "PCW_MODE=block "), _guard_command(source, client)
    found = [h for e in hooks for h in e.get("hooks", []) if h.get("command") == old]
    if not found:
        return None
    if not upgrade:
        return "old"
    for h in found:
        h["command"] = new
    return "wrote"


def _merge_hooks(path: Path, entry: dict, event: str = "PreToolUse",
                 upgrade: tuple[str, str, bool] | None = None) -> str:
    """Add `entry` to the file's `event` hooks, keeping everything else. Returns `wrote`, `skipped` or `old`.

    `upgrade` is (source, client, allowed) for the PreToolUse guard: its old generated command is rewritten when
    allowed, else left and `old` returned.
    """
    data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    pre = data.setdefault("hooks", {}).setdefault(event, [])
    names = ("lockstep refresh",) if event == "PostToolUse" else HOOK_NAMES
    if any(name in h.get("command", "") for e in pre for h in e.get("hooks", []) for name in names):
        status = _upgrade_old_guard(pre, *upgrade) if upgrade else None
        if status != "wrote":
            return status or "skipped"
    else:
        pre.append(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return "wrote"


def _refresh_entry(source: str, client: str) -> dict:
    """Native PostToolUse hook: update declared source-owned fact projections only."""
    command = f"uvx --from {source} lockstep refresh --client {client}"
    if client == "claude":
        command = f'cd "$CLAUDE_PROJECT_DIR" && {command}'
    matcher = "apply_patch|Edit|Write|Bash|shell|exec_command" if client == "codex" else "Edit|Write|MultiEdit|NotebookEdit|Bash"
    return {"matcher": matcher, "hooks": [{"type": "command", "command": command, "timeout": 30}]}


def _install_hooks(path: Path, source: str, client: str, upgrade: bool = False, notes: list[str] | None = None) -> str:
    """Install the guard and refresh hooks; `upgrade` allows rewriting init's old `PCW_MODE=block` guard command."""
    before = _merge_hooks(path, _hook_entry(source, client), upgrade=(source, client, upgrade))
    after = _merge_hooks(path, _refresh_entry(source, client), "PostToolUse")
    if before == "old" and notes is not None:
        notes.append(f"{path.parent.name}/{path.name} keeps PCW_MODE=block in its hook command; add `guard: {{mode: block}}` "
                     "to lockstep.yaml and run `lockstep init` again to move the setting there")
    return "wrote" if "wrote" in (before, after) else "skipped"


def _has_guard(config: Path) -> bool:
    """True when lockstep.yaml has a `guard:` section (an unreadable file counts as not having one)."""
    try:
        data = YAML(typ="safe").load(config.read_text(encoding="utf-8")) if config.is_file() else None
    except (YAMLError, OSError, UnicodeDecodeError):  # unreadable: do not rewrite the hook
        return False
    return isinstance(data, dict) and "guard" in data


def _lefthook(path: Path, source: str) -> str:
    """Add a `lockstep` pre-commit command to lefthook.yml (created if absent). Returns `wrote` or `skipped`."""
    names = " ".join(name for name in CHECK_NAMES if name not in ("arch", "test-first", "project", *DEFAULT_OFF))
    # `lockstep check` with no name diffs against HEAD, which a repository's first commit does not have yet.
    skip_first = '[ -z "$c" ] && ! git rev-parse -q --verify HEAD >/dev/null && continue'
    old_run = f'for c in "" {names}; do {skip_first}; uvx --from {source} lockstep check $c || exit 1; done'
    freshness = f'uvx --from {source} lockstep check project --check'
    run = f'{old_run} && {freshness}'
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    data = yaml.load(path) if path.is_file() else None
    if data is None:
        data = {}
    commands = data.setdefault("pre-commit", {}).setdefault("commands", {})
    existing = commands.get('lockstep')
    if existing is None:
        commands['lockstep'] = {'run': run}
    elif existing.get('run') == run:
        return 'skipped'
    elif existing.get('run') == old_run:
        # Only an exact known generated command is safe to upgrade in place.
        existing['run'] = run
    else:
        # Preserve custom policy, including old/custom Lockstep loops; add a separate gate.
        guard = commands.get('lockstep-project')
        if guard is not None:
            if guard.get('run') == freshness:
                return 'skipped'
            raise ValueError('lefthook command lockstep-project is custom; keep it and add lockstep check project --check under a free command name')
        commands['lockstep-project'] = {'run': freshness}
    with path.open("w", encoding="utf-8") as fh:
        yaml.dump(data, fh)
    return "wrote"


def _gitignore(path: Path) -> str:
    """Add the `.lockstep/` line to .gitignore. Returns `wrote` or `skipped`."""
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    if ".lockstep/" in text.splitlines():
        return "skipped"
    path.write_text(text + ("" if not text or text.endswith("\n") else "\n") + ".lockstep/\n", encoding="utf-8")
    return "wrote"


def init_repo(root: Path, owner: str | None = None, source: str = SOURCE,
              human_pattern: str = DEFAULT_HUMAN_PATTERN) -> int:
    """Install Lockstep in `root`, printing one line per file. Returns 0."""
    root = root.resolve()
    owner = owner or _origin_owner(root) or OWNER_PLACEHOLDER
    results: list[tuple[str, str]] = []
    skills = plugin_settings.setting(root)  # a bad planning.skills value stops init before anything is written
    config = root / "lockstep.yaml"
    if config.exists():
        results.append(("lockstep.yaml", "skipped"))
    else:
        config.write_text(lockstep_yaml(owner, human_pattern), encoding="utf-8")
        results.append(("lockstep.yaml", "wrote"))
    upgrade = _has_guard(config)
    notes: list[str] = []
    results.append((".claude/settings.json", _install_hooks(root / ".claude/settings.json", source, "claude", upgrade, notes)))
    results.append((".codex/hooks.json", _install_hooks(root / ".codex/hooks.json", source, "codex", upgrade, notes)))
    results.append(("lefthook.yml", _lefthook(root / "lefthook.yml", source)))
    results.append((".gitignore", _gitignore(root / ".gitignore")))
    if skills.mode != "off" and skills.marketplace:
        status, plugin_notes = plugin_settings.merge(root / plugin_settings.SETTINGS, skills)
        notes.extend(plugin_notes)
        results.append(("planning.skills", status))
        agents = plugin_settings.agents_note(root / "AGENTS.md")
        if agents != "absent":
            results.append(("AGENTS.md", agents))
    for rel, what in results:
        print(f"{what:7} {rel}")
    for note in notes:
        print(f"note    {note}")
    if skills.mode != "off" and skills.marketplace:
        print("Each person runs once per clone, for Claude Code (the settings turn the plugin on but do not download it):")
        print(f"  {plugin_settings.INSTALL_LINE}")
        print("and once per machine for Codex (it has no per-repository plugin setting):")
        for command in plugin_settings.codex_commands(skills.marketplace):
            print(f"  {command}")
    print(f"RESULT init wrote={sum(w == 'wrote' for _, w in results)} skipped={sum(w == 'skipped' for _, w in results)} exit=0")
    return 0


def init_cli(argv: list[str]) -> int:
    """`lockstep init` with its options; returns the exit status (2 when the options or an existing file cannot be read)."""
    ap = argparse.ArgumentParser(prog="lockstep init", description="install Lockstep in a repository")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--owner", help="the GitHub owner to write in lockstep.yaml (default: the git origin's owner)")
    ap.add_argument("--source", default=SOURCE, help="the git address uvx installs Lockstep from")
    ap.add_argument("--human-pattern", default=DEFAULT_HUMAN_PATTERN,
                    help="regex a `Source:` line must start with to count as a person's word (default: %(default)s)")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return int(exit_.code or 0) if isinstance(exit_.code, int) else 2
    try:
        return init_repo(args.repo, args.owner, args.source, args.human_pattern)
    except (ValueError, OSError) as err:  # an existing settings or lefthook file that is not valid JSON or YAML
        print(f"error: {err}", file=sys.stderr)
        return 2
