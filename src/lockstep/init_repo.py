"""`lockstep init [--repo PATH] [--owner NAME] [--source URL]`: install Lockstep in a repository.

Implements: lockstep-init/init-installs-lockstep-in-a-repository-without-overwriting
Implements: lockstep-init/installed-files-name-no-machine-and-read-their-settings-from-lockstep-yaml

Writes, each only when absent (nothing is overwritten; what was written and what was skipped is printed):

    lockstep.yaml          every commit check set to block, owner, sources.human_pattern, empty governed and layout
    .claude/settings.json  a PreToolUse hook running `lockstep-hook` (merged into an existing file)
    .codex/hooks.json      the same hook for Codex (merged into an existing file)
    lefthook.yml           a `lockstep` pre-commit command (added to an existing file)
    .gitignore             a `.lockstep/` line, the edit guard's log folder

The hook and lefthook commands install Lockstep from a git address with `uvx`, so no file holds an absolute path.
"""

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

from ruamel.yaml import YAML

from lockstep.checks.config import CHECK_NAMES

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


def lockstep_yaml(owner: str) -> str:
    """The text of a fresh `lockstep.yaml`: every check on block, the owner, the human-source pattern, an empty plan."""
    checks = "\n".join(f"  {name}: block" for name in CHECK_NAMES)
    return f"""# Lockstep's settings (docs: README.md, "Install Lockstep in a repository").
schema: lockstep.side.v1

# Each commit check (`lockstep check <name>`) is block (fail the commit), warn (print and pass) or off (skip).
checks:
{checks}

# The GitHub owner of this repository's organization or account.
owner: {owner}

sources:
  # A `Source:` line starting with this regex counts as a human's word; `Source: inferred by agent (...)` never does.
  human_pattern: "human"

# Folders where every file must be planned (for example [src/]). Empty means the edit guard checks no folder.
governed: []

# The plan's files: path, purpose, implements (OpenSpec requirement IDs), tests. `lockstep layout` creates them.
layout: []
"""


def _hook_entry(source: str, client: str) -> dict:
    """One PreToolUse entry for `client` (`claude` or `codex`): the edit guard, installed from `source` by uvx."""
    guard = f"PCW_MODE=block uvx --from {source} lockstep-hook"
    if client == "codex":
        return {"matcher": "apply_patch|Edit|Write|Bash|shell|exec_command",
                "hooks": [{"type": "command", "command": f"{guard} --client codex", "timeout": 30}]}
    return {"matcher": "Edit|Write|MultiEdit|NotebookEdit|Bash",
            "hooks": [{"type": "command", "command": f'cd "$CLAUDE_PROJECT_DIR" && {guard}', "timeout": 30}]}


def _merge_hooks(path: Path, entry: dict) -> str:
    """Add `entry` to the file's PreToolUse hooks, keeping everything else. Returns `wrote` or `skipped`."""
    data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    pre = data.setdefault("hooks", {}).setdefault("PreToolUse", [])
    if any(name in h.get("command", "") for e in pre for h in e.get("hooks", []) for name in HOOK_NAMES):
        return "skipped"
    pre.append(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return "wrote"


def _lefthook(path: Path, source: str) -> str:
    """Add a `lockstep` pre-commit command to lefthook.yml (created if absent). Returns `wrote` or `skipped`."""
    names = " ".join(name for name in CHECK_NAMES if name not in ("arch", "test-first", "project"))
    # `lockstep check` with no name diffs against HEAD, which a repository's first commit does not have yet.
    skip_first = '[ -z "$c" ] && ! git rev-parse -q --verify HEAD >/dev/null && continue'
    run = f'for c in "" {names}; do {skip_first}; uvx --from {source} lockstep check $c || exit 1; done'
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    data = yaml.load(path) if path.is_file() else None
    if data is None:
        data = {}
    if "lockstep" in path.read_text(encoding="utf-8") if path.is_file() else False:
        return "skipped"
    commands = data.setdefault("pre-commit", {}).setdefault("commands", {})
    commands["lockstep"] = {"run": run}
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


def init_repo(root: Path, owner: str | None = None, source: str = SOURCE) -> int:
    """Install Lockstep in `root`, printing one line per file. Returns 0."""
    root = root.resolve()
    owner = owner or _origin_owner(root) or OWNER_PLACEHOLDER
    results: list[tuple[str, str]] = []
    config = root / "lockstep.yaml"
    if config.exists():
        results.append(("lockstep.yaml", "skipped"))
    else:
        config.write_text(lockstep_yaml(owner), encoding="utf-8")
        results.append(("lockstep.yaml", "wrote"))
    results.append((".claude/settings.json", _merge_hooks(root / ".claude/settings.json", _hook_entry(source, "claude"))))
    results.append((".codex/hooks.json", _merge_hooks(root / ".codex/hooks.json", _hook_entry(source, "codex"))))
    results.append(("lefthook.yml", _lefthook(root / "lefthook.yml", source)))
    results.append((".gitignore", _gitignore(root / ".gitignore")))
    for rel, what in results:
        print(f"{what:7} {rel}")
    print(f"RESULT init wrote={sum(w == 'wrote' for _, w in results)} skipped={sum(w == 'skipped' for _, w in results)} exit=0")
    return 0


def init_cli(argv: list[str]) -> int:
    """`lockstep init` with its options; returns the exit status (2 when the options or an existing file cannot be read)."""
    ap = argparse.ArgumentParser(prog="lockstep init", description="install Lockstep in a repository")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--owner", help="the GitHub owner to write in lockstep.yaml (default: the git origin's owner)")
    ap.add_argument("--source", default=SOURCE, help="the git address uvx installs Lockstep from")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return int(exit_.code or 0) if isinstance(exit_.code, int) else 2
    try:
        return init_repo(args.repo, args.owner, args.source)
    except (ValueError, OSError) as err:  # an existing settings or lefthook file that is not valid JSON or YAML
        print(f"error: {err}", file=sys.stderr)
        return 2
