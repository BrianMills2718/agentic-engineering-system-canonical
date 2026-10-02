#!/usr/bin/env python3
"""Label lessons with Jev into failure-mode families (AES learning loop, slices 1-2).

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
  python3 scripts/learning_loop/label_items.py issues [--dry-run] [--summary-issue N]

`issues` (slice 2) labels every open issue that has a `kind:*` label and no
`family:*`, `fact` or `other` label yet, records Jev's answer as an issue
comment, and prints the run summary (posted to --summary-issue if given).
GitHub token: GH_TOKEN or GITHUB_TOKEN, else `gh auth token`. Exit status: 0 =
every item labelled, 1 = some Jev or GitHub calls failed (those items stay
unlabelled and are retried next run), 2 = could not list issues.

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
REPO = "BrianMills2718/agentic-engineering-system-canonical"
KINDS = ("kind:lesson", "kind:friction", "kind:problem")


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


def github_token() -> str:
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not tok:
        import subprocess
        tok = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
    if not tok:
        sys.exit("no GitHub token: set GH_TOKEN or log in with gh")
    return tok


def gh(method: str, path: str, tok: str, body: dict | None = None):
    req = urllib.request.Request("https://api.github.com" + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read() or b"null")


def cmd_issues(args) -> int:
    qs, key, tok = question_set(), api_key(), github_token()
    try:
        seen = {}
        for kind in KINDS:
            for i in gh("GET", f"/repos/{args.repo}/issues?state=open&per_page=100&labels={kind}", tok):
                if "pull_request" not in i:
                    seen[i["number"]] = i
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        print(f"issues: could not list issues in {args.repo}: {e}", file=sys.stderr)
        return 2
    names = lambda i: {l["name"] for l in i["labels"]}
    todo = [i for i in seen.values() if not any(n.startswith("family:") or n in ("fact", "other") for n in names(i))]
    counts = collections.Counter(already_labelled=len(seen) - len(todo))
    lines, cost = [], 0.0
    for i in sorted(todo, key=lambda i: i["number"]):
        body = i.get("body") or ""
        m = re.search(r"^recommended_action:\s*(.+)$", body, re.M)
        state = {"learning": (i["title"] + "\n\n" + body)[:1800], "recommended_action": (m.group(1) if m else "")[:400]}
        r, err, secs = ask(state, qs["question"], key)
        if err:
            counts["error"] += 1
            lines.append(f"- #{i['number']}: Jev failed ({err[:120]}); left unlabelled")
            continue
        d = decide(r["answers"], qs)
        cost += r.get("usage", {}).get("cost") or 0
        labels = [f"family:{k}" for k in d["families"]] if d["outcome"] == "filed" else [d["outcome"]]
        labels += ["confident"] if d["confident"] and d["outcome"] == "filed" else []
        lines.append(f"- #{i['number']} {i['title'][:80]} -> {', '.join(labels)} (p={d['p']}, confidence={d['confidence']})")
        counts[d["outcome"]] += 1
        if args.dry_run:
            continue
        try:
            gh("POST", f"/repos/{args.repo}/issues/{i['number']}/labels", tok, {"labels": labels})
            gh("POST", f"/repos/{args.repo}/issues/{i['number']}/comments", tok, {"body": (
                f"Learning loop label run ({qs['version']} questions, {MODEL}): **{', '.join(labels)}**\n\n"
                f"choice `{d['choice']}`, p={d['p']}, confidence={d['confidence']}, runner-up `{d['second']}`. "
                "Wrong label? Relabel by hand and add `kind:friction` to a new issue saying why.")})
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            counts["error"] += 1
            lines[-1] += f" — GitHub write failed ({e}); not labelled"
            counts[d["outcome"]] -= 1
    summary = (f"learning loop issues run{' (dry run)' if args.dry_run else ''}: {len(seen)} open kind:* issues, "
               f"{dict(counts)}, cost=${cost:.4f}, questions={qs['version']}")
    print(summary)
    print("\n".join(lines))
    if args.summary_issue and not args.dry_run:
        gh("POST", f"/repos/{args.repo}/issues/{args.summary_issue}/comments", tok, {"body": summary + "\n\n" + "\n".join(lines)})
    return 1 if counts["error"] else 0


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
    c = sub.add_parser("issues")
    c.add_argument("--repo", default=REPO)
    c.add_argument("--dry-run", action="store_true")
    c.add_argument("--summary-issue", type=int, default=0)
    args = ap.parse_args()
    return {"legacy": cmd_legacy, "report": cmd_report, "issues": cmd_issues}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
