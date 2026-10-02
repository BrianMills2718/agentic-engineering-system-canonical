#!/usr/bin/env python3
"""Label lessons with Jev into failure-mode families (AES learning loop, slice 1).

Design: proposals/aes-learning-loop/DESIGN.md. Question set v1 is frozen here;
changing it means re-running the spot-check set before trusting thresholds.

  python3 scripts/learning_loop/label_items.py legacy --out datasets/learning-loop/legacy-learnings-labelled.jsonl
  python3 scripts/learning_loop/label_items.py report --in datasets/learning-loop/legacy-learnings-labelled.jsonl

Reads OPENROUTER_API_KEY from the environment, else by name from
~/.secrets/api_keys.env. Resumes: entries already in --out are skipped. A failed
call is written as an error record and counted, never guessed or retried twice.
"""
from __future__ import annotations

import argparse
import collections
import glob
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAXONOMY = ROOT / "docs" / "failure-modes.md"
ENDPOINT = "https://openrouter.ai/api/v1/systemone"
MODEL = "typesafe/jev-1.13"
QUESTIONS_VERSION = "v1"
FACT_BELOW = 0.7      # is_failure below this -> fact
FILE_AT = 0.6         # family probability at or above this -> filed
LEGACY_GLOB = "~/code/project-meta/learnings/entries/*.json"


def api_key() -> str:
    if os.environ.get("OPENROUTER_API_KEY"):
        return os.environ["OPENROUTER_API_KEY"]
    for line in open(os.path.expanduser("~/.secrets/api_keys.env")):
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip("\"'")
    sys.exit("OPENROUTER_API_KEY not found")


def families() -> dict[str, str]:
    text = TAXONOMY.read_text()
    out = {}
    for m in re.finditer(r"^## ([A-Z]) — (.+?)\s*(\*\*\[register\]\*\*)?\n+> \*(.+?)\*", text, re.M):
        out[m.group(1)] = (m.group(2).strip(), m.group(4).strip())
    if not out:
        sys.exit(f"no families parsed from {TAXONOMY}")
    return out


def questions(fams: dict[str, tuple[str, str]]) -> dict:
    titles = "; ".join(f"{k}: {t}" for k, (t, _) in fams.items())
    return {
        "is_failure": {"type": "noul", "instructions": "This learning describes a reasoning or control failure (an agent or system got something wrong), not just a plain fact about a tool or product."},
        "fits_well": {"type": "noul", "instructions": "One of these failure-mode families describes the failure in this learning well, not just loosely: " + titles},
        "family": {"type": "choice", "instructions": "Which failure-mode family does this recorded learning best illustrate? Pick the family whose guiding question this learning answers.",
                   "criteria": {k: f"{t}. Guiding question: {q}" for k, (t, q) in fams.items()}},
    }


def entry_text(d: dict) -> str:
    return str(d.get("learning") or d.get("finding") or d.get("lesson") or "")


def ask(state: str, q: dict, key: str) -> tuple[dict | None, str | None, float]:
    body = json.dumps({"model": MODEL, "state": state, "questions": q}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    t0 = time.perf_counter()
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=60).read())
        return r, None, time.perf_counter() - t0
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read()[:200].decode(errors='replace')}", time.perf_counter() - t0
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        return None, f"{type(e).__name__}: {e}", time.perf_counter() - t0


def decide(ans: dict) -> tuple[str, str | None]:
    is_f = ans["is_failure"]["noul"]
    fam = ans["family"]["choice"]
    p = ans["family"]["probabilities"][fam]
    if is_f < FACT_BELOW:
        return "fact", None
    if p >= FILE_AT:
        return "filed", fam
    return "unsorted", fam


def cmd_legacy(args) -> int:
    fams = families()
    q = questions(fams)
    key = api_key()
    out = Path(args.out)
    done = set()
    if out.exists():
        done = {json.loads(l)["entry_id"] for l in out.open() if l.strip()}
    files = sorted(glob.glob(os.path.expanduser(LEGACY_GLOB)))
    if args.limit:
        files = files[: args.limit]
    counts = collections.Counter()
    cost = 0.0
    with out.open("a") as fh:
        for f in files:
            d = json.load(open(f))
            eid = d.get("entry_id") or Path(f).stem
            if eid in done:
                counts["skipped_done"] += 1
                continue
            text = entry_text(d)
            state = f"Recorded learning:\n{text[:1800]}\nRecommended action: {str(d.get('recommended_action') or '')[:400]}"
            r, err, secs = ask(state, q, key)
            rec = {"entry_id": eid, "recorded_at": d.get("recorded_at"), "project": d.get("project"),
                   "text": text[:600], "questions": QUESTIONS_VERSION, "model": MODEL, "seconds": round(secs, 2)}
            if err:
                rec["error"] = err
                counts["error"] += 1
            else:
                a = r["answers"]
                outcome, fam = decide(a)
                rec.update({"outcome": outcome, "family": fam,
                            "p": round(a["family"]["probabilities"][a["family"]["choice"]], 3),
                            "confidence": a["family"].get("confidence"),
                            "is_failure": round(a["is_failure"]["noul"], 3),
                            "fits_well": round(a["fits_well"]["noul"], 3),
                            "second": sorted(a["family"]["probabilities"].items(), key=lambda kv: -kv[1])[1][0],
                            "cost": r.get("usage", {}).get("cost")})
                cost += rec["cost"] or 0
                counts[outcome] += 1
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
    print(f"labelled: {dict(counts)} cost=${cost:.4f} out={out}")
    return 1 if counts["error"] else 0


def cmd_report(args) -> int:
    rows = [json.loads(l) for l in open(args.inp) if l.strip()]
    fams = families()
    ok = [r for r in rows if "error" not in r]
    print(f"items: {len(rows)}  labelled: {len(ok)}  errors: {len(rows) - len(ok)}  "
          f"cost: ${sum((r.get('cost') or 0) for r in ok):.4f}")
    print("outcomes:", dict(collections.Counter(r['outcome'] for r in ok)))
    fc = collections.Counter(r["family"] for r in ok if r["outcome"] == "filed")
    print("filed per family:")
    for k, (t, _) in fams.items():
        print(f"  {k} {fc.get(k, 0):5}  {t}")
    novel = [r for r in ok if r["outcome"] != "fact" and r["fits_well"] < 0.65]
    print(f"novel-candidate (failure, fits_well < 0.65): {len(novel)}")
    random.seed(args.seed)
    filed = [r for r in ok if r["outcome"] == "filed"]
    sample = random.sample(filed, min(10, len(filed)))
    print("\nspot-check sample (10 filed items):")
    for r in sample:
        print(f"- {r['entry_id']} → {r['family']} ({fams[r['family']][0]}) p={r['p']}\n    {r['text'][:220]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("legacy")
    a.add_argument("--out", required=True)
    a.add_argument("--limit", type=int, default=0)
    b = sub.add_parser("report")
    b.add_argument("--in", dest="inp", required=True)
    b.add_argument("--seed", type=int, default=20261002)
    args = ap.parse_args()
    return cmd_legacy(args) if args.cmd == "legacy" else cmd_report(args)


if __name__ == "__main__":
    sys.exit(main())
