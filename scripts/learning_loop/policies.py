"""Is each workspace rule documented and observed? (plan aes-learning-loop, S8)

Brian, 2026-10-12: "most improant thing is the new policy ad wheter it is docuemtned, and wehther it is
observable enforceable and connected to a feebdack loop". The rules agents load live in one place,
code2-workspace `agents/` (core.md and topics/*.md), which name rules as Policy `<id>`; Brian's words behind
each are in agents/rule-sources.md. For each id this reads, without changing anything:

  documented  agents/rule-sources.md names the id
  observed    nightly feedback reports (reports-*.jsonl) from the last --days that name the id

AES kept a second rules register (docs/rules/register.yaml) until 2026-11-25; it was retired so rules have
one home (Brian, 2026-11-25, "ia prpove yourr ecommednations though"; docs/retired/2026-11-25.md). How a rule
is enforced is said in the rule's own text, which names its check or hook.

Output: one JSON line per run in $FEEDBACK_OUT/policies-runs.jsonl and a table on stdout.
Exit 0 = every named rule is documented, 1 = some are not (a keyed agent concern is opened unless
--no-alert), 2 = crashed.

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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from alert import file_alert  # noqa: E402

HOME = Path.home()
OUT = Path(os.environ.get("FEEDBACK_OUT", HOME / "projects/data/feedback-collector"))
AGENTS_DIR = Path(os.environ.get("WORKSPACE_AGENTS_DIR", HOME / "code2/workspace/agents"))
POLICY_ID = re.compile(r"Polic(?:y|ies) `([a-z0-9]+(?:-[a-z0-9]+)+)`")


def named_policies(rules_text: str) -> list[str]:
    return sorted(set(POLICY_ID.findall(rules_text)))


def _rule_files(agents_dir: Path) -> list[Path]:
    """The files agents load as rules: core.md and every topic file."""
    return [agents_dir / "core.md", *sorted((agents_dir / "topics").glob("*.md"))]


def documented(sources: str, pid: str) -> bool:
    """The id appears in rule-sources.md as a whole id, not as part of a longer one (`foo` inside `foo-bar`)."""
    return re.search(rf"(?<![a-z0-9-]){re.escape(pid)}(?![a-z0-9-])", sources) is not None


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
    ids = named_policies("\n".join(f.read_text() for f in _rule_files(AGENTS_DIR)))
    sources = (AGENTS_DIR / "rule-sources.md").read_text()
    seen = observed(OUT, ids, today - dt.timedelta(days=days))
    rows = [{"id": pid, "documented": documented(sources, pid), "reports": seen[pid]} for pid in ids]
    gaps = [r["id"] for r in rows if not r["documented"]]
    return {"at": dt.datetime.now(dt.timezone.utc).isoformat(), "days": days, "policies": rows, "gaps": gaps}


def alert(gaps: list[str]) -> None:
    file_alert("workspace-policy-unregistered", "feedback-policies",
               f"{len(gaps)} workspace rules have no source entry",
               "Rules named as Policy `<id>` in code2-workspace agents/ (core.md, topics/) with no entry in "
               f"agents/rule-sources.md: {', '.join(gaps)}. Add each entry with Brian's words; rerun "
               "`python scripts/learning_loop/policies.py` (AES) until it exits 0.")


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
        print(f"{r['id']:32} documented={'yes' if r['documented'] else 'NO'} reports_{a.days}d={r['reports']}")
    code = 1 if result["gaps"] else 0
    print(f"RESULT policies named={len(result['policies'])} gaps={len(result['gaps'])} exit={code}")
    if code and not a.no_alert:
        alert(result["gaps"])
    return code


if __name__ == "__main__":
    raise SystemExit(main())
