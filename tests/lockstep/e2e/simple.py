"""The smallest example: one function, one requirement, every part shown.

Runs the real tools (aes, cog, the agent hook, pytest, the wiki builder) in a
fresh folder and, after each step, snapshots the four things a person looks at:
the plan entry, the code, the wiki page, and what the agent is told.
Writes walkthrough/simple.json; fails loudly if any command's exit differs.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
EXAMPLE = REPO / "example-simple"
BIN = Path(sys.executable).parent
sys.path.insert(0, str(REPO.parents[1] / "src"))  # the AES checkout's src/

from lockstep.wiki import pages  # noqa: E402

STEPS: list[dict] = []


def sh(cmd: str, cwd: Path, env: dict, expect: int = 0, stdin: str | None = None) -> str:
    p = subprocess.run(cmd, shell=True, cwd=cwd, env=env, input=stdin, capture_output=True, text=True)
    if (p.returncode == 0) != (expect == 0):
        raise SystemExit(f"`{cmd}` exited {p.returncode}, expected {'0' if expect == 0 else 'non-zero'}\n{p.stdout}{p.stderr}")
    return p.stdout


def plan_view(proj: Path) -> dict:
    """The real plan file, plus a map of its links generated from it (no hand-written text)."""
    raw = (proj / ".aes/target.yaml").read_text()
    tgt = yaml.safe_load(raw)
    if not tgt.get("normative_items"):
        return {"tree": "", "yaml": raw}
    arts = {a["id"]: a for a in tgt.get("planned_artifacts") or []}
    vss = tgt.get("verification_subjects") or []
    out = []
    for o in tgt["outcomes"]:
        out.append(f"{o['id']}  outcome: {o['statement']}")
        for ni in [n for n in tgt["normative_items"] if o["id"] in n["outcome_refs"]]:
            out.append(f"└─ {ni['id']}  requirement: {ni['statement']}")
            scs = [c for c in tgt.get("success_criteria") or [] if ni["id"] in c["target_refs"]]
            cmps = [c for c in tgt.get("components") or [] if ni["id"] in c["target_refs"]]
            for sc in scs:
                out.append(f"   ├─ {sc['id']}  how we know: {sc['statement']}")
                out.append(f"   │    disproved if: {sc['disproof']}")
                for vs in [v for v in vss if sc["id"] in v["criterion_refs"]]:
                    out.append(f"   │    proven by {vs['id']}: {vs['locator']}")
            for k, c in enumerate(cmps):
                out.append(f"   └─ {c['id']}  component: {c['responsibility']}")
                refs = c["planned_artifact_refs"]
                for j, ref in enumerate(refs):
                    art = arts[ref]
                    why = ", ".join(art["semantic_justification_refs"])
                    branch = "└─" if j == len(refs) - 1 else "├─"
                    out.append(f"        {branch} {art['locator']['exact_path']:<26} {ref} ({art['kind']}, exists for {why})")
    return {"tree": "\n".join(_wrap(line) for line in out), "yaml": raw}


def _wrap(line: str, width: int = 92) -> str:
    """Wrap one tree line, continuing under its own branch so the tree stays readable."""
    import re
    import textwrap
    m = re.match(r"^([ │├└─]*(?:[A-Z]+-[A-Z0-9-]+\s+)?)", line)
    lead = m.group(1) if m else ""
    cont = re.sub(r"[├└]─", "│ ", lead.replace("└─", "  ")) if lead else ""
    cont = re.sub(r"[A-Z]+-[A-Z0-9-]+\s+", lambda x: " " * len(x.group(0)), cont)
    return "\n".join(textwrap.wrap(line, width, subsequent_indent=cont, break_on_hyphens=False)) or line


def agent_told(proj: Path, env: dict) -> tuple[str, str]:
    call = json.dumps({"tool_name": "Edit", "cwd": str(proj),
                       "tool_input": {"file_path": str(proj / "src/greeter/__init__.py")}})
    hso = json.loads(sh("pcw-hook", proj, env, stdin=call))["hookSpecificOutput"]
    text = hso.get("permissionDecisionReason") or hso.get("additionalContext") or ""
    text = text.split("\n\ncog said:")[0] if hso["permissionDecision"] == "deny" else text
    return hso["permissionDecision"], text


def snap(n: int, title: str, what: str, proj: Path, env: dict, *, agent: bool = False,
         status: dict | None = None) -> None:
    code = proj / "src/greeter/__init__.py"
    wiki = ""
    if code.exists():
        wiki = pages(proj, "greeter")["components/CMP-GREETER.md"]
    told = agent_told(proj, env) if agent else None
    STEPS.append({"n": n, "title": title, "what": what, "status": status or {},
                  "plan": plan_view(proj),
                  "code": code.read_text() if code.exists() else "",
                  "wiki": wiki,
                  "agent": {"decision": told[0], "text": told[1]} if told else None})
    print(f"  ok {n}. {title}")


def run(proj: Path) -> None:
    # PCW_MODE=block: the example shows the hook refusing (what a fixed file gets); the default only warns (D7).
    env = {**os.environ, "PCW_MODE": "block", "PATH": f"{BIN}{os.pathsep}{os.environ['PATH']}", "PYTHONDONTWRITEBYTECODE": "1",
           "GIT_AUTHOR_NAME": "example", "GIT_AUTHOR_EMAIL": "example@example.invalid",
           "GIT_COMMITTER_NAME": "example", "GIT_COMMITTER_EMAIL": "example@example.invalid"}
    commit = "git add -A && git commit -q -m"
    (proj / ".gitignore").write_text("__pycache__/\nsite/\n.pcw/\n")
    (proj / "pyproject.toml").write_text('[tool.pytest.ini_options]\npythonpath = ["src"]\n')
    shutil.copytree(EXAMPLE / "plans", proj / "plans")
    for rel in ["mkdocs.yml", "docs/gen_pages.py", "Makefile"]:
        (proj / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(EXAMPLE / rel, proj / rel)
    sh("git init -q -b main", proj, env)
    sh('aes init --project-id greeter --actor "someone who wants a greeting" '
       '--outcome "Calling greet with a name returns a greeting with that name."', proj, env)
    sh("aes hooks install", proj, env)
    sh(f"{commit} init", proj, env)

    # 1. Plan
    sh("aes plan accept plans/plan-001.yaml", proj, env)
    sh(f"{commit} 'plan 1'", proj, env)
    snap(1, "Write the requirement in the plan",
         "The requirement is written once, in the plan, with how we will know it is met and the test that proves it. "
         "No code exists yet.", proj, env)

    # 2. Code + docstring
    for rel in ["src/greeter/__init__.py", "tests/test_greet.py"]:
        (proj / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(EXAMPLE / rel, proj / rel)
    sh("make project", proj, env)
    sh("python -m pytest -q -p no:cacheprovider tests", proj, env)
    sh(f"{commit} 'greet'", proj, env)
    sh("aes evidence record VS-GREET --depends-on src/greeter/__init__.py", proj, env)
    sh(f"{commit} 'evidence'", proj, env)
    snap(2, "Write the code; the plan text is copied into its docstring",
         "The code has an empty marked block in its docstring. One command (cog) fills it from the plan. "
         "Nobody types the requirement into the code.", proj, env)

    # 3. Wiki
    sh("make wiki", proj, env)
    snap(3, "Build the wiki from the plan and the code",
         "The wiki page is generated from the plan, the test result and the docstring. "
         "There is no hand-written copy that could drift.", proj, env, status={"wiki": "test passed: SUPPORTED"})

    # 4. Agent handed the requirement
    snap(4, "An agent opens the code: it is handed the requirement",
         "Before the agent edits greet, the hook gives it the requirement for that exact file, word for word from the plan. "
         "It does not have to search the project for it.", proj, env, agent=True)

    # 5. Plan changes
    sh("aes plan accept plans/plan-002.yaml", proj, env)
    sh(f"{commit} 'plan 2'", proj, env)
    sh("make check", proj, env, expect=1)
    snap(5, "The requirement changes in the plan: refuse an empty name",
         "Only the plan is edited. The docstring still says the old thing, and the check notices.",
         proj, env, status={"code": "out of date with the plan", "wiki": "test result is now stale"})

    # 6. Agent blocked
    snap(6, "The agent tries to edit: it is stopped",
         "Working from the old docstring would mean coding the old requirement, so the hook refuses the edit "
         "and says what to run. (This example sets PCW_MODE=block; by default the hook only warns, and refuses "
         "for a file the plan marks fixed.)", proj, env, agent=True, status={"code": "out of date with the plan"})

    # 7. Back in step
    sh("make project", proj, env)
    code = proj / "src/greeter/__init__.py"
    code.write_text(code.read_text().replace('    return f"Hello, {name}!"',
                                             '    if not name:\n        raise ValueError("empty name")\n    return f"Hello, {name}!"'))
    test = proj / "tests/test_greet.py"
    test.write_text(test.read_text() + '\n\ndef test_refuses_an_empty_name():\n    import pytest\n\n'
                    '    with pytest.raises(ValueError):\n        greet("")\n')
    sh("make check", proj, env)
    sh(f"{commit} 'refuse empty name'", proj, env)
    sh("aes evidence record VS-GREET --depends-on src/greeter/__init__.py", proj, env)
    sh(f"{commit} 'evidence 2'", proj, env)
    snap(7, "Regenerate, edit, rebuild: everything agrees again",
         "One command refreshes the docstring; the agent is now handed the new requirement and changes the code; "
         "the test passes; the wiki shows the new text.", proj, env, agent=True,
         status={"wiki": "test passed: SUPPORTED"})


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=REPO / "walkthrough" / "simple.json")
    args = ap.parse_args()
    base = Path(tempfile.mkdtemp(prefix="pcw-simple-")) / "greeter"
    base.mkdir()
    try:
        run(base)
    finally:
        shutil.rmtree(base.parent, ignore_errors=True)
    out = args.out
    out.write_text(json.dumps({"steps": STEPS}, indent=1) + "\n")
    print(f"simple: {len(STEPS)} of 7 steps recorded; {out}")
    return 0 if len(STEPS) == 7 else 1


if __name__ == "__main__":
    raise SystemExit(main())
