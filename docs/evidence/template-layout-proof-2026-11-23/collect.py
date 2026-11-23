"""Collect the evidence of the template-layout proof run into this folder (plan docs/planning/template-layout-2026-11-23.md, step 6).

Usage: python3 collect.py <copy> <run dir> <hook log> <start UTC> <links.json at the plan commit>
Absolute paths are replaced by <copy>, <runs> and <home> so the folder holds no machine paths.
"""

import json
import shutil
import sys
from pathlib import Path

copy, run, hook_log, start, links = sys.argv[1:6]
out = Path(__file__).resolve().parent
home = str(Path.home())
worktree = json.loads(Path(run, "summary.json").read_text())["worktree"]


def clean(text: str) -> str:
    for long, short in ((worktree, "<worktree>"), (copy, "<copy>"), (run, "<runs>"), (str(Path(copy).parent), "<proof>"),
                        (home, "<home>"), ("/tmp/claude-1000", "<tmp>"), ("/tmp/lockstep-writer-", "<writer>-")):
        text = text.replace(long, short)
    return text


summary = json.loads(Path(run, "summary.json").read_text())
keep = {k: summary.get(k) for k in ("change", "run_id", "ref", "head", "accept_files", "accept_before", "accept",
                                    "check_exit", "uncommitted", "departures", "peek_reads", "implementer_exit")}
(out / "summary.json").write_text(clean(json.dumps(keep, indent=1)) + "\n")
for name in ("accept-before.log", "accept.log", "implementer-prompt.md"):
    (out / name).write_text(clean(Path(run, name).read_text()))
check = Path(run, "check.log").read_text().splitlines()
(out / "check-tail.log").write_text(clean("\n".join(check[-25:])) + "\n")
shutil.copy(links, out / "links-at-plan-commit.json")

calls, results = [], {}
for line in Path(run, "implementer.jsonl").read_text().splitlines():
    event = json.loads(line)
    for part in event.get("message", {}).get("content", []) if isinstance(event.get("message"), dict) else []:
        if not isinstance(part, dict):
            continue
        if part.get("type") == "tool_use":
            arg = part["input"].get("command") or part["input"].get("file_path") or ""
            calls.append((part["id"], part["name"], arg))
        if part.get("type") == "tool_result":
            body = part.get("content")
            results[part["tool_use_id"]] = body if isinstance(body, str) else json.dumps(body)
with open(out / "tool-calls.txt", "w") as fh:
    for n, (ident, name, arg) in enumerate(calls, 1):
        head = clean(arg).replace("\n", " ")[:300]
        refused = " [REFUSED BY HOOK]" if "hook error" in results.get(ident, "") else ""
        fh.write(f"{n}. {name}: {head}{refused}\n")
        if refused:
            fh.write("   " + clean(results[ident]).splitlines()[0] + "\n")
first = next(results[i] for i, _, a in calls if "?? src/greeter/greet.py" in results.get(i, ""))
(out / "greet-first-text.py").write_text(first.split("?? src/greeter/greet.py", 1)[1])

records = [json.loads(x) for x in Path(hook_log).read_text().splitlines() if x.strip()]
window = [r for r in records if str(r.get("at") or "") >= start]
(out / "hook-log.jsonl").write_text("".join(clean(json.dumps(r)) + "\n" for r in window))
print(f"calls={len(calls)} hook_records={len(window)} of {len(records)}")
