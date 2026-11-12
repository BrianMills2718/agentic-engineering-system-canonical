"""A2 run: the edit guard on lifelike's plan. Writes docs/planning/runs/lockstep-acceptance/a2.json.

Four agent attempts as Bash tool calls, each fed to `lockstep-hook` as PreToolUse JSON in a fresh clone of lifelike
(the project the criterion names): three ways to write a file the plan does not list, and one read-only cp.
"""

import json
import re
import shutil
import tempfile
from pathlib import Path

from _common import BIN, ENV, Trace, git, tree

LIFELIKE = Path("/home/brian/code2/lifelike")
CASES = [
    ("cat", "cat > src/lifelike/extra.py", "refused", "cat > src/lifelike/extra.py <<'EOF'\nx = 1\nEOF"),
    ("echo", "echo > src/lifelike/extra.py", "refused", "echo x > src/lifelike/extra.py"),
    ("python", "python -c writing src/lifelike/zz.py", "refused",
     "python -c 'open(\"src/lifelike/zz.py\",\"w\").write(\"x=1\")'"),
    ("cp", "cp of a planned file (read only)", "allowed", "cp src/lifelike/rule.py /tmp/rulecopy.py"),
]
UNPLANNED = ["src/lifelike/extra.py", "src/lifelike/zz.py"]


def redact_private_plan_text(t) -> None:
    """lifelike is a private repository: keep the guard's decisions and file names, drop the plan text it quotes."""
    pat = re.compile(r'(\\?"additionalContext\\?": \\?")(.*?)(\\?"\}\})', re.S)
    for step in t.steps:
        for key in ("stdout", "stderr"):
            text = step[key]["text"]
            step[key]["text"] = pat.sub(lambda m: m.group(1) + f"[plan text from the private lifelike repository, {len(m.group(2))} characters, not published]" + m.group(3), text)


def main() -> int:
    t = Trace("A2", "The guard refuses writes the plan does not name and allows reads")
    work = Path(tempfile.mkdtemp(prefix="a2-lifelike-")) / "lifelike"
    git(LIFELIKE, "status", "--short")
    t.extra["source_repo"] = {"path": str(LIFELIKE), "revision": git(LIFELIKE, "rev-parse", "HEAD").strip()}
    git(work.parent, "clone", "-q", "--no-hardlinks", str(LIFELIKE), str(work))
    before = tree(work, "src", "tests")
    t.extra["files_before"] = before
    t.extra["unplanned_existed_before"] = {p: (work / p).exists() for p in UNPLANNED}
    # lifelike's own hook line is `PCW_MODE=block pcw-hook`; Lockstep's default mode only warns.
    env = {**ENV, "CLAUDE_PROJECT_DIR": str(work), "PCW_MODE": "block"}
    t.extra["hook_command"] = "cd $CLAUDE_PROJECT_DIR && PCW_MODE=block lockstep-hook  (as lifelike .claude/settings.json)"
    for cid, label, should, command in CASES:
        payload = {"hook_event_name": "PreToolUse", "cwd": str(work), "tool_name": "Bash",
                   "tool_input": {"command": command}}
        step = t.run(f"hook: {label}", [str(BIN / "lockstep-hook")], work, stdin=json.dumps(payload), env=env)
        out = step["stdout"]["text"].strip()
        decision = json.loads(out)["hookSpecificOutput"].get("permissionDecision", "") if out else ""
        reason = json.loads(out)["hookSpecificOutput"].get("permissionDecisionReason", "") if out else ""
        did = "refused" if decision == "deny" else "allowed"
        # The reason is the full refusal text, kept whole (the trimmed stdout above may cut lines).
        t.row(cid, label, should, did, step["name"], {"command": command, "decision": decision or "(no output)",
                                                         "message": reason})
    # The criterion also says the refusal shows the plan: its message should name the files the plan does allow.
    planned = sorted(set(re.findall(r"exact_path:\s*([^\s}]+)", (work / ".aes/target.yaml").read_text())))
    t.extra["planned_files_in_plan"] = planned
    refusal = next(r for r in t.rows if r["did"] == "refused")
    named = [p for p in planned if p in refusal["message"].replace(refusal["command"], "")]
    t.row("message", "the refusal message shows the plan (names the files the plan allows)",
          "names the planned files", "names the planned files" if named else "names none of the planned files",
          refusal["step"], {"planned_files_named": named, "message": refusal["message"],
                            "command": "(the first refused row's message)"})
    after = tree(work, "src", "tests")
    t.extra["files_after"] = after
    t.extra["unplanned_existed_after"] = {p: (work / p).exists() for p in UNPLANNED}
    t.extra["files_changed_by_run"] = sorted(set(after) ^ set(before))
    redact_private_plan_text(t)
    t.write()
    shutil.rmtree(work.parent, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
