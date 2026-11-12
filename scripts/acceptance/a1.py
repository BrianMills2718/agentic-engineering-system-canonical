"""A1 run: the README's one command in a fresh repository. Writes docs/planning/runs/lockstep-acceptance/a1.json.

The command is parsed from the README text (see _install.py). The record keeps every written file's full text so the
receipt card can show it.
"""

import json
import re
import shutil

import yaml

from _common import Trace
from _install import CANONICAL, under_test, fresh_env, fresh_repo, install_command, is_local, parse_args, readme_text, written_files


def hook_commands(files: dict[str, str]) -> dict[str, list[str]]:
    """The command strings of each of the three hook entries, read from the written files."""
    out = {"claude": [], "codex": [], "lefthook": []}
    for key, path in (("claude", ".claude/settings.json"), ("codex", ".codex/hooks.json")):
        if path in files:
            data = json.loads(files[path])
            out[key] = [h.get("command", "") for e in data.get("hooks", {}).get("PreToolUse", []) for h in e.get("hooks", [])]
    if "lefthook.yml" in files:
        cmds = (yaml.safe_load(files["lefthook.yml"]) or {}).get("pre-commit", {}).get("commands", {})
        out["lefthook"] = [v.get("run", "") for k, v in cmds.items() if "lockstep" in k]
    return out


def main() -> int:
    args = parse_args(__doc__)
    t = Trace("A1", "One command sets Lockstep up in a new repository")
    readme = readme_text(args.source)
    given, command = install_command(readme, args.source)
    env, cache = fresh_env("a1")
    repo = fresh_repo("a1", "https://github.com/example-org/demo.git")
    step = t.run("the README's one command", command, repo, env=env)
    files = written_files(repo)
    hooks = hook_commands(files)
    t.extra["install"] = {"readme_line": given, "command_run": command, "source": args.source,
                          "unmerged_build": is_local(args.source), "fresh_uv_cache": True,
                          "uv_cache_dir": str(cache), "repo_origin": "https://github.com/example-org/demo.git"}
    t.extra.update(under_test(args.source))
    t.extra["files_written"] = files
    t.extra["hook_commands"] = hooks
    s = step["name"]
    t.row("exit", "the command exits 0", "0", str(step["exit_code"]), s)
    t.row("yaml", "lockstep.yaml is written", "written", "written" if "lockstep.yaml" in files else "missing", s)
    claude = [c for c in hooks["claude"] if "lockstep-hook" in c]
    t.row("claude", ".claude/settings.json has a PreToolUse entry calling lockstep-hook", "present",
          "present" if claude else "missing", s, {"command": claude[0] if claude else ""})
    codex = [c for c in hooks["codex"] if "lockstep-hook" in c]
    t.row("codex", ".codex/hooks.json has the Codex hook entry", "present", "present" if codex else "missing", s,
          {"command": codex[0] if codex else ""})
    lefthook = [c for c in hooks["lefthook"] if "lockstep" in c]
    t.row("lefthook", "lefthook.yml has a lockstep command", "present", "present" if lefthook else "missing", s,
          {"command": lefthook[0] if lefthook else ""})
    allhooks = claude + codex + lefthook
    wrong = [c for c in allhooks if CANONICAL not in c or "BrianMills2718/lockstep" in c]
    t.row("address", "the hook commands install from the AES canonical address, not the lockstep repository",
          "all 3 from agentic-engineering-system-canonical",
          "all 3 from agentic-engineering-system-canonical" if len(allhooks) == 3 and not wrong
          else f"{len(allhooks) - len(wrong)} of {len(allhooks)} from it", s)
    # PCW_MODE is only an environment variable name, not the pcw tool.
    second = {p: sorted(set(re.findall(r"code2check|pcw", text.replace("PCW_MODE", ""), re.I))) for p, text in files.items()}
    second = {p: v for p, v in second.items() if v}
    t.row("one-tool", "no second tool (pcw, code2check) is installed by any written file", "none named",
          "none named" if not second else "named in " + ", ".join(second), s, {"found": second})
    t.write()
    shutil.rmtree(repo.parent, ignore_errors=True)
    shutil.rmtree(cache, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
