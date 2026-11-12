"""Run the full example end to end in a fresh folder and record every step.

Each step runs real commands (git, aes, cog, the agent hook, pytest, mkdocs)
and states the exit code it expects; the run fails loudly the moment one
differs. The record (walkthrough/run.json) is what the walkthrough page shows.

    python e2e/run.py [--keep DIR]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXAMPLE = REPO / "example"
BIN = Path(sys.executable).parent

STEPS: list[dict] = []


class StepFailed(Exception):
    pass


def sh(cmd: str, cwd: Path, env: dict, stdin: str | None = None) -> tuple[int, str]:
    p = subprocess.run(cmd, shell=True, cwd=cwd, env=env, input=stdin, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)


def step(lane: str, title: str, why: str, cmds: list, cwd: Path, env: dict, show: list[str] | None = None) -> None:
    """cmds: list of (command, expected_exit) or (command, expected_exit, stdin)."""
    record = {"n": len(STEPS) + 1, "lane": lane, "title": title, "why": why, "commands": [], "files": []}
    for c in cmds:
        cmd, expect, stdin = (c + (None,))[:3]
        code, out = sh(cmd, cwd, env, stdin)
        out = out.replace(str(cwd), "<project>").replace(str(REPO), "<plan-code-wiki>").replace(str(Path.home()), "~").rstrip()
        try:  # show JSON answers (the hook's) readably
            out = json.dumps(json.loads(out), indent=2)
        except ValueError:
            pass
        shown = cmd if stdin is None else f"{cmd}  <<< {stdin}"
        shown = shown.replace(str(cwd), "<project>")
        record["commands"].append({"cmd": shown, "expect": expect, "exit": code, "output": out})
        if (expect == 0) != (code == 0):
            STEPS.append(record)
            raise StepFailed(f"step {record['n']} '{title}': `{cmd}` exited {code}, expected {'0' if expect == 0 else 'non-zero'}\n{out}")
    for rel in show or []:
        record["files"].append({"path": rel, "text": (cwd / rel).read_text(encoding="utf-8")})
    STEPS.append(record)
    print(f"  ok  {record['n']:>2}. [{lane}] {title}")


def hook_call(tool: str, rel: str, cwd: Path) -> str:
    return json.dumps({"hook_event_name": "PreToolUse", "tool_name": tool, "cwd": str(cwd),
                       "tool_input": {"file_path": str(cwd / rel), "old_string": "", "new_string": ""}})


def replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise StepFailed(f"{path}: expected text not found")
    path.write_text(text.replace(old, new), encoding="utf-8")


def run(proj: Path) -> None:
    # PCW_MODE=block: the example shows the hook refusing (what a fixed file gets); the default only warns (D7).
    env = {**os.environ, "PCW_MODE": "block", "PATH": f"{BIN}{os.pathsep}{os.environ['PATH']}", "GIT_AUTHOR_NAME": "example",
           "GIT_AUTHOR_EMAIL": "example@example.invalid", "GIT_COMMITTER_NAME": "example",
           "GIT_COMMITTER_EMAIL": "example@example.invalid", "PYTHONDONTWRITEBYTECODE": "1"}
    commit = "git add -A && git commit -q -m"

    # ---- PLAN
    (proj / ".gitignore").write_text(".venv/\n__pycache__/\nsite/\n.lockstep/\n")
    (proj / "pyproject.toml").write_text('[tool.pytest.ini_options]\npythonpath = ["src"]\n')
    step("plan", "Say what outcome, and for whom",
         "One outcome, written once, in the plan file. `aes hooks install` adds the commit gate.",
         [("git init -q -b main", 0),
          ('aes init --project-id people-finder --actor "a recruiter who needs people at a target company" '
           '--outcome "Given a company name, the recruiter gets the people who work there now and nobody else."', 0),
          ("aes hooks install", 0), (f"{commit} 'Initialize AES'", 0)], proj, env)

    shutil.copytree(EXAMPLE / "plans", proj / "plans")
    step("plan", "Write the requirement, how we will know, and what would disprove it",
         "The proposal names the requirement (NI-001), the success criterion and its disproof (SC-001), the files "
         "the code will live in, and the test that proves it. AES checks it, then writes it into the plan.",
         [("aes plan validate plans/plan-001-find-people.yaml", 0), ("aes plan accept plans/plan-001-find-people.yaml", 0),
          (f"{commit} 'Accept PLAN-001'", 0)], proj, env, show=["plans/plan-001-find-people.yaml"])

    # ---- SCAFFOLD
    helper = proj / "src/people_finder/helpers.py"
    helper.parent.mkdir(parents=True)
    helper.write_text("def unplanned(): ...\n")
    step("scaffold", "A file the plan does not name is refused",
         "Every file under src/ and tests/ must be in the plan, so every piece of code points back to the "
         "requirement it exists for. The commit gate refuses this one.",
         [(f"{commit} 'Add an unplanned helper'", 1)], proj, env)
    step("scaffold", "The agent hook catches it even earlier, at the edit",
         "The same rule, applied when the agent tries to write the file rather than at commit time. By default "
         "the hook only warns: the edit goes through and the agent is told what would have been refused (Brian's "
         "decision D7). It refuses for a file the plan marks fixed, and everywhere with PCW_MODE=block, which this "
         "example sets. Below is the JSON Claude Code sends the hook, and the hook's answer.",
         [("pcw-hook", 0, hook_call("Write", "src/people_finder/helpers.py", proj))], proj, env)
    sh("git reset -q && rm src/people_finder/helpers.py", proj, env)

    # ---- CODE
    step("code", "The agent opens a planned file and is handed the plan text",
         "Before the agent writes src/people_finder/__init__.py the hook answers with the requirement, criterion, "
         "disproof and proving test for that exact file, taken word for word from the plan.",
         [("pcw-hook", 0, hook_call("Write", "src/people_finder/__init__.py", proj))], proj, env)

    for rel in ["src/people_finder/__init__.py", "src/people_finder/profiles.json", "tests/test_find_people.py",
                "Makefile", "mkdocs.yml", "docs/gen_pages.py", ".claude/settings.json", ".codex/hooks.json"]:
        (proj / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(EXAMPLE / rel, proj / rel)
    step("code", "Write the code, then project the plan into its docstring",
         "The docstring holds a cog block. `make project` fills it from the plan, so the agent (and anyone "
         "reading the code) sees the requirement right where the code is. Nobody types this text by hand.",
         [("make project", 0), ("python -m pytest -p no:cacheprovider tests", 0),
          (f"{commit} 'Implement find_people (PLAN-001)'", 0)], proj, env, show=["src/people_finder/__init__.py"])

    step("code", "Run the planned test and bind the result to this exact commit",
         "AES runs the test named in the plan and records the result against the commit and the files it covered.",
         [("aes evidence record VS-FINDER --depends-on src/people_finder/__init__.py --depends-on src/people_finder/profiles.json", 0),
          (f"{commit} 'Record evidence for SC-001'", 0), ("aes evidence status", 0)], proj, env)

    # ---- WIKI
    step("wiki", "Build the wiki from the plan, the evidence and the docstrings",
         "The wiki pages are generated at build time, so there is no hand-written copy to drift. The code page "
         "renders the same docstrings cog wrote.",
         [("make wiki", 0), ("python -c \"from pathlib import Path; from lockstep.wiki import pages; "
                             "print(pages(Path('.'), 'people_finder')['components/CMP-FINDER.md'])\"", 0)], proj, env)

    # ---- CHANGE
    step("change", "The requirement changes: results must be in name order",
         "PLAN-002 changes NI-001 and SC-001 in the plan. Nothing else is edited yet. AES now treats the old "
         "test result as stale: it proved the old wording, not the new one.",
         [("aes plan validate plans/plan-002-sorted.yaml", 0), ("aes plan accept plans/plan-002-sorted.yaml", 0),
          (f"{commit} 'Accept PLAN-002'", 0), ("aes evidence status", 0)], proj, env, show=["plans/plan-002-sorted.yaml"])

    step("change", "The docstring is now out of date, and the check says so",
         "cog compares the docstring with what the plan now says. It fails, naming the file.",
         [("make check", 1)], proj, env)

    step("change", "The agent hook stops the edit until the docstring matches the plan",
         "If the agent tried to change the code now, it would be working from the old requirement. "
         "In this example (PCW_MODE=block) the hook refuses and tells it what to run; by default it lets the "
         "edit through with the same message as a warning, and refuses only for a file the plan marks fixed.",
         [("pcw-hook", 0, hook_call("Edit", "src/people_finder/__init__.py", proj))], proj, env)

    step("change", "Re-project; the hook now hands over the new requirement",
         "`make project` rewrites the docstring from the plan. The same edit is now allowed, and the agent "
         "receives the new text (name order).",
         [("make project", 0), ("pcw-hook", 0, hook_call("Edit", "src/people_finder/__init__.py", proj))],
         proj, env, show=["src/people_finder/__init__.py"])

    replace(proj / "tests/test_find_people.py",
            '''    handles = {p["handle"] for p in find_people("Northwind Robotics")}
    assert handles == {"@ada_builds", "@lin_ships", "@noor_ml"}  # lower-case employer included''',
            '''    handles = [p["handle"] for p in find_people("Northwind Robotics")]
    assert handles == ["@ada_builds", "@lin_ships", "@noor_ml"]  # name order; lower-case employer included''')
    step("change", "The agent updates the test first: it fails on the old code",
         "The test now asks for name order. The old code returns the people in file order, so it fails. "
         "This shows the test can actually catch the problem.",
         [("python -m pytest -p no:cacheprovider tests", 1)], proj, env)

    replace(proj / "src/people_finder/__init__.py",
            'return [p for p in profiles if p["employer"].casefold() == wanted]',
            'return sorted((p for p in profiles if p["employer"].casefold() == wanted), key=lambda p: p["name"])')
    step("change", "The agent changes the code; everything is back in step",
         "Code sorted, test passes, docstring matches the plan, the wiki builds, and AES records new evidence "
         "for the changed criterion.",
         [("make check", 0), (f"{commit} 'Return people in name order (PLAN-002)'", 0),
          ("aes evidence record VS-FINDER --depends-on src/people_finder/__init__.py --depends-on src/people_finder/profiles.json", 0),
          (f"{commit} 'Record evidence for SC-001 (PLAN-002)'", 0), ("aes status", 0), ("make wiki", 0),
          ("python -c \"from pathlib import Path; from lockstep.wiki import pages; "
           "print(pages(Path('.'), 'people_finder')['components/CMP-FINDER.md'])\"", 0)],
         proj, env, show=["src/people_finder/__init__.py"])

    step("observe", "Every hook decision was logged",
         "One append-only file per day: what file, which plan item, allowed or refused, and why.",
         [("cat .lockstep/hook-*.jsonl", 0)], proj, env)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", help="run in this folder (must not exist) and keep it")
    ap.add_argument("--out", default=str(REPO / "walkthrough" / "run.json"))
    args = ap.parse_args()
    base = Path(args.keep) if args.keep else Path(tempfile.mkdtemp(prefix="pcw-e2e-")) / "people-finder"
    base.mkdir(parents=True)
    started = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    ok, error = True, None
    try:
        run(base)
    except StepFailed as exc:
        ok, error = False, str(exc)
    aes_version = subprocess.run([str(BIN / "aes"), "--version"], capture_output=True, text=True).stdout.strip()
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    record = {"started": started, "ok": ok, "error": error, "aes_version": aes_version,
              "plan_code_wiki_commit": head, "steps": STEPS}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    if not args.keep:
        shutil.rmtree(base.parent, ignore_errors=True)
    passed = len(STEPS) - (0 if ok else 1)
    print(f"e2e: {passed} of {len(STEPS)} steps passed; {'OK' if ok else 'FAILED'}; record: {args.out}")
    if error:
        print(error, file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
