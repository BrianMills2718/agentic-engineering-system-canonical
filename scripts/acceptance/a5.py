"""A5 run: portability. Writes docs/planning/runs/lockstep-acceptance/a5.json and a5-readme-agent.jsonl.

Repo 1 (origin example-org) is installed with the README's command; its files are scanned for machine paths, the
`sources` check is run with the setting block, warn and off, and its lockstep.yaml is copied into repo 2 (origin
other-org). Repo 3 (origin third-org) is installed by a fresh headless agent that sees only the README.
"""

import json
import os
import re
import shutil
import socket
import subprocess
from pathlib import Path

import yaml

from _common import ENV, RECORDS, ROOT, Trace, git, trim
from _install import (CANONICAL, fresh_env, fresh_repo, install_command, is_local, parse_args, readme_for_agent,
                      readme_text, under_test, uvx_source, written_files)

MODEL = "claude-haiku-5-5"
SPEC = "# demo Specification\n\n## Requirements\n\n### Requirement: Greets the user\n\nThe system SHALL greet the user.\n\n#### Scenario: Greeting\n\n- **WHEN** a user arrives\n- **THEN** it greets them\n"
SOURCE_URL_MASK = CANONICAL


def commit_spec(repo: Path) -> None:
    (repo / "openspec/specs/demo").mkdir(parents=True)
    (repo / "openspec/specs/demo/spec.md").write_text(SPEC)
    git(repo, "add", "openspec")
    git(repo, "commit", "-q", "-m", "add a requirement with no Source line")


def set_mode(repo: Path, name: str, mode: str) -> None:
    path = repo / "lockstep.yaml"
    path.write_text(re.sub(rf"(?m)^(  {name}:) \w+", rf"\1 {mode}", path.read_text()))


def outcome(step: dict) -> str:
    out = step["stdout"]["text"] + step["stderr"]["text"]
    if step["exit_code"] != 0:
        return "refused"
    if re.search(r"warning", out, re.I):
        return "allowed with a warning"
    return "allowed silently" if "no-source" not in out else "allowed with a finding"


def api_key() -> str | None:
    """ANTHROPIC_API_KEY from the environment or ~/.secrets/api_keys.env; the value is only passed on, never printed or stored."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"]
    f = Path.home() / ".secrets/api_keys.env"
    if f.is_file():
        m = re.search(r"(?m)^(?:export\s+)?ANTHROPIC_API_KEY=(.*)$", f.read_text())
        if m:
            return m.group(1).strip().strip("\"'")
    return None


def secret_values() -> list[str]:
    """Every secret-looking value this machine's env or secrets file holds, to check the saved transcript against."""
    vals = [v for k, v in os.environ.items() if re.search(r"KEY|TOKEN|SECRET|PASSWORD", k) and len(v) >= 12]
    f = Path.home() / ".secrets/api_keys.env"
    if f.is_file():
        for line in f.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                v = line.split("=", 1)[1].strip().strip("\"'")
                if len(v) >= 12:
                    vals.append(v)
    return vals


def scrub_transcript(text: str) -> str:
    """Drop machine details before publishing: the init event's plugin, skill and tool lists, session ids, home paths."""
    out = []
    for line in text.splitlines():
        if not line.startswith("{"):
            continue
        ev = json.loads(line)
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            ev = {"type": "system", "subtype": "init", "model": ev.get("model")}
        ev.pop("session_id", None)
        ev.pop("uuid", None)
        out.append(re.sub(r"/home/[^/\"\s]+", "~", json.dumps(ev)))
    return "\n".join(out) + "\n"


def main() -> int:
    args = parse_args(__doc__)
    t = Trace("A5", "Portable, configurable and shareable")
    t.extra.update(under_test(args.source))
    readme = readme_text(args.source)
    given, command = install_command(readme, args.source)
    t.extra["install"] = {"readme_line": given, "command_run": command, "source": args.source,
                          "unmerged_build": is_local(args.source), "fresh_uv_cache": True}
    env, cache = fresh_env("a5")
    repo = fresh_repo("a5-one", "https://github.com/example-org/demo.git")
    step = t.run("repo 1: the README's command", command, repo, env=env)
    files = written_files(repo)
    init_step = step["name"]
    t.extra["repo1_files"] = sorted(files)

    # machine paths
    host = socket.gethostname()
    pats = {"/home/": "/home/", "/Users/": "/Users/", "~/code": "~/code", "C:\\": "C:\\"}
    counts = {label: sum(text.count(p) for text in files.values()) for label, p in pats.items()}
    counts["the host name of this machine"] = sum(text.count(host) for text in files.values()) if host else 0
    total = sum(counts.values())
    t.row("paths", "machine paths in every file init wrote (/home/, /Users/, ~/code, C:\\, the host name)", "0", str(total),
          init_step, {"per_pattern": counts, "files_scanned": sorted(files)})

    # switchable checks
    cfg_text = files.get("lockstep.yaml", "")
    pristine = cfg_text
    cfg = yaml.safe_load(cfg_text) or {}
    listed = re.search(r"runs one check \(([^)]*)\)", readme)
    names = re.findall(r"`([a-z-]+)`", listed.group(1)) if listed else []
    values = cfg.get("checks") or {}
    bad = {n: values.get(n) for n in names if values.get(n) not in ("block", "warn", "off", False)}
    missing = [n for n in names if n not in values]
    t.row("checks", "every check the README names has a block, warn or off value in lockstep.yaml",
          f"{len(names)} of {len(names)}: " + ", ".join(names),
          f"{len(names) - len(bad) - len(missing)} of {len(names)}: " + ", ".join(n for n in names if n not in bad and n not in missing),
          init_step, {"settings": {n: values.get(n) for n in names}})
    commit_spec(repo)
    check_cmd = f"uvx --from {uvx_source(args.source)} lockstep check sources"
    repo1_results = {}
    for mode, should in (("block", "refused"), ("warn", "allowed with a warning"), ("off", "allowed silently")):
        set_mode(repo, "sources", mode)
        s = t.run(f"repo 1: sources check set to {mode}", check_cmd, repo, env=env)
        repo1_results[mode] = (s["exit_code"], outcome(s), s["stdout"]["text"])
        t.row(f"sources-{mode}", f"`lockstep check sources` with sources: {mode} (a requirement has no Source line)", should,
              outcome(s), s["name"], {"command": check_cmd, "message": (s["stdout"]["text"] + s["stderr"]["text"]).strip(),
                                      "exit_code": s["exit_code"]})

    # owner
    owner = cfg.get("owner")
    masked = {p: tx.replace(SOURCE_URL_MASK, "") for p, tx in files.items()}
    named = {p: tx.count("BrianMills2718") for p, tx in masked.items() if "BrianMills2718" in tx}
    did = f"owner {owner}" + (", BrianMills2718 not named elsewhere" if not named else ", BrianMills2718 named in " + ", ".join(named))
    t.row("owner", "lockstep.yaml owner comes from origin, and no written file names BrianMills2718 outside the install address",
          "owner example-org, BrianMills2718 not named elsewhere", did, init_step)

    # copied config
    repo2 = fresh_repo("a5-two", "https://github.com/other-org/another.git")
    new_cfg = re.sub(r"(?m)^owner: .*$", "owner: other-org", pristine)
    (repo2 / "lockstep.yaml").write_text(new_cfg)
    commit_spec(repo2)
    diff = [(a, b) for a, b in zip(pristine.splitlines(), new_cfg.splitlines()) if a != b]
    t.row("copy-diff", "the copied lockstep.yaml differs from repo 1's only on the owner line", "1 line: owner",
          f"{len(diff)} line" + ("" if len(diff) == 1 else "s") + (": owner" if len(diff) == 1 and diff[0][0].startswith("owner") else ""),
          init_step, {"repo1_line": diff[0][0] if diff else "", "repo2_line": diff[0][1] if diff else ""})
    s = t.run("repo 2: sources check with the copied lockstep.yaml (sources: block)", check_cmd, repo2, env=env)
    t.row("copy-behaviour", "the sources check in repo 2 behaves as it did in repo 1 with sources: block (same exit status and output)",
          f"{repo1_results['block'][1]}, exit {repo1_results['block'][0]}",
          f"{outcome(s)}, exit {s['exit_code']}" + ("" if s["stdout"]["text"] == repo1_results["block"][2] else ", output differs"),
          s["name"], {"command": check_cmd, "message": (s["stdout"]["text"] + s["stderr"]["text"]).strip()})

    # README only
    agent_row(t, args, readme, env)
    t.write()
    for d in (repo.parent, repo2.parent, cache):
        shutil.rmtree(d, ignore_errors=True)
    return 0


def agent_row(t: Trace, args, readme: str, env: dict) -> None:
    repo3 = fresh_repo("a5-three", "https://github.com/third-org/demo.git")
    text = readme_for_agent(readme, args.source)
    prompt = (f"{text}\n\n---\n\nInstall Lockstep in the repository in the current folder by following only this README. "
              "Report the files it wrote.")
    jsonl = RECORDS / "a5-readme-agent.jsonl"
    key = api_key()
    argv = ["claude", "-p", "--bare", "--model", MODEL, "--output-format", "stream-json", "--verbose",
            "--max-budget-usd", "0.50", "--allowedTools", "Bash"]
    run_env = {**env, **({"ANTHROPIC_API_KEY": key} if key else {})}
    RECORDS.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(argv, cwd=repo3, env=run_env, input=prompt, capture_output=True, text=True, timeout=900)
    transcript = p.stdout
    leaked = [i for i, v in enumerate(secret_values()) if v in transcript or v in p.stderr]
    if leaked or re.search(r"sk-[A-Za-z0-9_-]{16,}", transcript):
        raise SystemExit("secret-like text found in the agent transcript; not saving it")
    transcript = scrub_transcript(transcript)
    jsonl.write_text(transcript)
    t.steps.append({"name": "repo 3: a fresh headless agent follows only the README",
                    "command": " ".join(argv) + "   (prompt on stdin: the README text, then the instruction)", "cwd": str(repo3),
                    "stdin": prompt, "exit_code": p.returncode, "stdout": trim(transcript[-3000:]), "stderr": trim(p.stderr)})
    events = [json.loads(line) for line in transcript.splitlines() if line.startswith("{")]
    result = next((e for e in reversed(events) if e.get("type") == "result"), {})
    ran_init = any(b.get("type") == "tool_use" and "lockstep init" in json.dumps(b.get("input", {}))
                   for e in events if e.get("type") == "assistant" for b in e.get("message", {}).get("content", []) if isinstance(b, dict))
    files = written_files(repo3)
    need = ["lockstep.yaml", ".claude/settings.json", ".codex/hooks.json", "lefthook.yml"]
    absent = [f for f in need if f not in files]
    owner = (yaml.safe_load(files.get("lockstep.yaml", "")) or {}).get("owner")
    should = "lockstep.yaml and the hook entries exist, written by the agent following the README"
    if absent:
        did = "missing: " + ", ".join(absent)
    elif not ran_init:
        did = "files exist but the transcript shows no `lockstep init` call"
    else:
        did = should
    t.extra["readme_agent"] = {"model": MODEL, "exit_code": p.returncode, "cost_usd": result.get("total_cost_usd"),
                               "is_error": result.get("is_error"), "num_turns": result.get("num_turns"),
                               "agent_report": result.get("result", ""), "ran_lockstep_init": ran_init,
                               "owner_written": owner, "files_written": sorted(files), "auth": "ANTHROPIC_API_KEY (--bare)" if key else "none found",
                               "transcript": "a5-readme-agent.jsonl", "source_in_readme_given_to_agent": uvx_source(args.source),
                               "origin": "https://github.com/third-org/demo.git"}
    t.row("readme-agent", "a fresh agent that sees only the README installs Lockstep in a repository outside BrianMills2718",
          should, did, "repo 3: a fresh headless agent follows only the README",
          {"message": result.get("result", ""), "cost_usd": result.get("total_cost_usd")})
    shutil.rmtree(repo3.parent, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
