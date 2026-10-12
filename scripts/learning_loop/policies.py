"""Is each workspace rule documented, enforced, observed and on a feedback path? (plan aes-learning-loop, S8)

Brian, 2026-10-12: "most improant thing is the new policy ad wheter it is docuemtned, and wehther it is
observable enforceable and connected to a feebdack loop". The workspace AGENTS.md names its rules as
Policy `<id>`. For each id this reads, without changing anything:

  documented  WORKING_RULES.md, "Sources for AGENTS.md rules", has an entry naming the id
  registered  AES docs/rules/register.yaml has `- id: <id>`, whose enforcement_status,
              enforcement_mechanism and feedback_path say how it is enforced and where friction goes
              (that register is current; project-meta policy/registry.yaml is legacy, per its own header)
  observed    nightly feedback reports (reports-*.jsonl) from the last --days that name the id

Output: one JSON line per run in $FEEDBACK_OUT/policies-runs.jsonl and a table on stdout.
Exit 0 = every named rule is documented and registered, 1 = some are not (a keyed agent concern is
opened unless --no-alert), 2 = crashed.

  python scripts/learning_loop/policies.py [--days 30] [--no-alert]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
OUT = Path(os.environ.get("FEEDBACK_OUT", HOME / "projects/data/feedback-collector"))
AGENTS_MD = Path(os.environ.get("WORKSPACE_AGENTS_MD", HOME / "projects/.claude/AGENTS.md"))
WORKING_RULES = Path(os.environ.get("WORKING_RULES_MD", HOME / "projects/.claude/WORKING_RULES.md"))
PROJECT_META = Path(os.environ.get("PROJECT_META", HOME / ".hive-brain/project-meta"))
RULES_REGISTER = Path(os.environ.get("RULES_REGISTER", Path(__file__).resolve().parents[2] / "docs/rules/register.yaml"))
POLICY_ID = re.compile(r"Polic(?:y|ies) `([a-z0-9]+(?:-[a-z0-9]+)+)`")


def named_policies(agents_md: str) -> list[str]:
    return sorted(set(POLICY_ID.findall(agents_md)))


def documented(working_rules: str, pid: str) -> bool:
    sources = working_rules.split("## Sources for AGENTS.md rules", 1)
    return len(sources) == 2 and pid in sources[1]


def registry_entries(registry: str) -> dict[str, dict]:
    """Top-level `- id:` blocks of registry.yaml, with the scalar fields this check reads."""
    entries: dict[str, dict] = {}
    for block in re.split(r"(?m)^- id: ", registry)[1:]:
        pid, _, body = block.partition("\n")
        fields = {}
        for key in ("enforcement_status", "enforcement_tier", "feedback_path", "enforcement_mechanism"):
            m = re.search(rf"(?m)^  {key}: (.+)$", body)
            fields[key] = m.group(1).strip() if m else None
        entries[pid.strip()] = fields
    return entries


def observed(out: Path, ids: list[str], since: dt.date) -> dict[str, int]:
    counts = dict.fromkeys(ids, 0)
    for f in sorted(out.glob("reports-*.jsonl")):
        m = re.match(r"reports-(\d{4}-\d{2}-\d{2})", f.name)
        if not m or dt.date.fromisoformat(m.group(1)) < since:
            continue
        for line in f.read_text(errors="replace").splitlines():
            try:
                value = json.loads(line).get("value") or ""
            except ValueError:
                continue
            for pid in ids:
                if pid in value:
                    counts[pid] += 1
    return counts


def check(days: int, today: dt.date | None = None) -> dict:
    today = today or dt.date.today()
    ids = named_policies(AGENTS_MD.read_text())
    rules = WORKING_RULES.read_text()
    registry = registry_entries(RULES_REGISTER.read_text())
    seen = observed(OUT, ids, today - dt.timedelta(days=days))
    rows = []
    for pid in ids:
        reg = registry.get(pid)
        rows.append({"id": pid, "documented": documented(rules, pid), "registered": reg is not None,
                     "enforcement_status": (reg or {}).get("enforcement_status"),
                     "feedback_path": (reg or {}).get("feedback_path"), "reports": seen[pid]})
    gaps = [r["id"] for r in rows if not (r["documented"] and r["registered"])]
    return {"at": dt.datetime.now(dt.timezone.utc).isoformat(), "days": days, "policies": rows, "gaps": gaps}


def alert(gaps: list[str]) -> None:
    subprocess.run([sys.executable, str(PROJECT_META / "scripts/notify_operator.py"), "--key", "workspace-policy-unregistered",
                    "--severity", "agent", "--source", "feedback-policies",
                    "--title", f"{len(gaps)} workspace rules are not registered or documented",
                    "--body", "Rules named as Policy `<id>` in the workspace AGENTS.md with no AES docs/rules/register.yaml "
                              "entry (enforcement, observation, feedback path) or no WORKING_RULES source entry: "
                              f"{', '.join(gaps)}. Add each entry; rerun "
                              "`python scripts/learning_loop/policies.py` (AES) until it exits 0."],
                   timeout=120)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--no-alert", action="store_true")
    a = ap.parse_args(argv)
    try:
        result = check(a.days)
    except Exception as exc:  # crash: still fail loudly
        print(f"RESULT policies crashed={exc!r} exit=2")
        return 2
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "policies-runs.jsonl").open("a") as fh:
        fh.write(json.dumps(result) + "\n")
    for r in result["policies"]:
        print(f"{r['id']:32} documented={'yes' if r['documented'] else 'NO'} registered={'yes' if r['registered'] else 'NO'} "
              f"enforcement={r['enforcement_status'] or '-'} feedback_path={r['feedback_path'] or '-'} reports_{a.days}d={r['reports']}")
    code = 1 if result["gaps"] else 0
    print(f"RESULT policies named={len(result['policies'])} gaps={len(result['gaps'])} exit={code}")
    if code and not a.no_alert:
        alert(result["gaps"])
    return code


if __name__ == "__main__":
    raise SystemExit(main())
