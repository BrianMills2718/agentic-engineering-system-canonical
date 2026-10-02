#!/usr/bin/env python3
"""Label lessons with Jev into failure-mode families (AES learning loop, slice 1).

Design: proposals/aes-learning-loop/DESIGN.md. The question set is frozen in
question_set_v2.json; changing it means re-running the judged test sets in
datasets/learning-loop/experiments/ before trusting it.

One Jev choice per item: 22 families (each option says what it covers and what
it is not for, per TypeSafe's choice guidance), plus `other` and
`not_a_failure`. Outcome: `fact` (not_a_failure), `other` (a failure no family
fits), else `filed` with every family within `near_top` of the top
probability. `confident` marks confidence >= `confident_at`.

  python3 scripts/learning_loop/label_items.py legacy --out datasets/learning-loop/legacy-learnings-labelled-v2.jsonl
  python3 scripts/learning_loop/label_items.py report --in datasets/learning-loop/legacy-learnings-labelled-v2.jsonl

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
from concurrent.futures import ThreadPoolExecutor
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAXONOMY = ROOT / "docs" / "failure-modes.md"
ENDPOINT = "https://openrouter.ai/api/v1/systemone"
MODEL = "typesafe/jev-1.13"
QUESTION_SET = Path(__file__).with_name("question_set_v2.json")
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


def question_set() -> dict:
    qs = json.loads(QUESTION_SET.read_text())
    missing = set(families()) - set(qs["letters"].values())
    if missing:
        sys.exit(f"{QUESTION_SET.name} has no option for families {sorted(missing)}")
    return qs


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


def decide(ans: dict, qs: dict) -> dict:
    a = ans["kind"]
    probs = {qs["letters"].get(k, k): v for k, v in a["probabilities"].items()}
    choice = qs["letters"].get(a["choice"], a["choice"])
    top = probs[choice]
    near = sorted((k for k, v in probs.items() if v >= top - qs["near_top"] and v > 0.05), key=lambda k: -probs[k])
    if choice == "not_a_failure":
        outcome = "fact"
    elif choice == "other":
        outcome = "other"
    else:
        outcome = "filed"
    return {"outcome": outcome, "choice": choice, "p": round(top, 3),
            "families": [k for k in near if k not in ("other", "not_a_failure")] if outcome == "filed" else [],
            "confidence": a.get("confidence"), "confident": (a.get("confidence") or 0) >= qs["confident_at"],
            "second": sorted(probs, key=lambda k: -probs[k])[1]}


def label_one(f: str, qs: dict, key: str) -> dict:
    d = json.load(open(f))
    text = entry_text(d)
    state = {"learning": text[:1800], "recommended_action": str(d.get("recommended_action") or "")[:400]}
    r, err, secs = ask(state, qs["question"], key)
    rec = {"entry_id": d.get("entry_id") or Path(f).stem, "recorded_at": d.get("recorded_at"), "project": d.get("project"),
           "text": text[:600], "questions": qs["version"], "model": MODEL, "seconds": round(secs, 2)}
    if err:
        rec["error"] = err
    else:
        rec.update(decide(r["answers"], qs))
        rec["cost"] = r.get("usage", {}).get("cost")
    return rec


def cmd_legacy(args) -> int:
    qs = question_set()
    key = api_key()
    out = Path(args.out)
    done = set()
    if out.exists():
        done = {r["entry_id"] for r in map(json.loads, filter(str.strip, out.open())) if r.get("questions") == qs["version"] and "error" not in r}
    files = sorted(glob.glob(os.path.expanduser(LEGACY_GLOB)))
    if args.limit:
        files = files[: args.limit]
    todo = [f for f in files if Path(f).stem not in done and json.load(open(f)).get("entry_id") not in done]
    counts = collections.Counter(skipped_done=len(files) - len(todo))
    cost = 0.0
    with out.open("a") as fh, ThreadPoolExecutor(max_workers=args.workers) as pool:
        for rec in pool.map(lambda f: label_one(f, qs, key), todo):
            counts["error" if "error" in rec else rec["outcome"]] += 1
            cost += rec.get("cost") or 0
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
    print(f"labelled: {dict(counts)} cost=${cost:.4f} out={out} questions={qs['version']}")
    return 1 if counts["error"] else 0


def cmd_report(args) -> int:
    qs = question_set()
    rows = [json.loads(l) for l in open(args.inp) if l.strip()]
    rows = [r for r in rows if r.get("questions") == qs["version"]]
    fams = families()
    ok = [r for r in rows if "error" not in r]
    print(f"items ({qs['version']}): {len(rows)}  labelled: {len(ok)}  errors: {len(rows) - len(ok)}  "
          f"cost: ${sum((r.get('cost') or 0) for r in ok):.4f}")
    print("outcomes:", dict(collections.Counter(r["outcome"] for r in ok)))
    filed = [r for r in ok if r["outcome"] == "filed"]
    print(f"filed with one family: {sum(len(r['families']) == 1 for r in filed)}, with several: "
          f"{sum(len(r['families']) > 1 for r in filed)}, confident (>= {qs['confident_at']}): {sum(r['confident'] for r in filed)}")
    first = collections.Counter(r["families"][0] for r in filed)
    anyf = collections.Counter(k for r in filed for k in r["families"])
    print("per family (top label / any label):")
    for k, (t, _) in fams.items():
        print(f"  {k} {first.get(k, 0):5} {anyf.get(k, 0):5}  {t}")
    random.seed(args.seed)
    sample = random.sample(filed, min(10, len(filed)))
    print("\nspot-check sample (10 filed items):")
    for r in sample:
        names = ", ".join(f"{k} ({fams[k][0]})" for k in r["families"])
        print(f"- {r['entry_id']} -> {names} p={r['p']}\n    {r['text'][:220]}")
    others = [r for r in ok if r["outcome"] == "other"]
    print(f"\nother (failures no family fits): {len(others)}")
    for r in random.sample(others, min(5, len(others))):
        print(f"- {r['entry_id']}: {r['text'][:200]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("legacy")
    a.add_argument("--out", required=True)
    a.add_argument("--limit", type=int, default=0)
    a.add_argument("--workers", type=int, default=8)
    b = sub.add_parser("report")
    b.add_argument("--in", dest="inp", required=True)
    b.add_argument("--seed", type=int, default=20261002)
    args = ap.parse_args()
    return cmd_legacy(args) if args.cmd == "legacy" else cmd_report(args)


if __name__ == "__main__":
    sys.exit(main())
