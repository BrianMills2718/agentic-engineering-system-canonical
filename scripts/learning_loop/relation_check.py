#!/usr/bin/env python3
"""S2 measurement: does Jev judge how two feedback records relate well enough? (PLAN.md, "The S2 measurement").

  pairs   build N record pairs from a collector reports-<date>.jsonl: most-similar pairs (word overlap,
          different reports) plus random pairs, written without labels
  judge   run one judge (jev | strong) on every pair; same four options, same fields (sentence + links)
  score   compare each judge with the hand labels written into the pairs file before any judge ran

Relations: supports (B is evidence for or agrees with A), challenges (B contradicts or weakens A),
same_problem (A and B report the same failure or friction without one being evidence for the other),
unrelated. A judge that refuses or returns free text on any pair is out, not scored (parity rule).
Bar: 8 of 10 acceptable (24 of 30). Traces: feedback-collector/relation-check/<judge>/<pair id>.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from pathlib import Path

RELATIONS = ("supports", "challenges", "same_problem", "unrelated")
DEFINITIONS = {
    "supports": "B is evidence for A or states the same claim, so B makes A more credible",
    "challenges": "B contradicts A or is evidence against it",
    "same_problem": "A and B report the same failure, friction or issue, without one being evidence for the other",
    "unrelated": "A and B are about different things",
}
JEV = "openrouter/typesafe/jev-1.13"
STRONG = os.environ.get("FEEDBACK_STRONG_MODEL", "openrouter/openai/gpt-5.6-sol")  # any llm_client-allowlisted route
WORD = re.compile(r"[a-z][a-z0-9_]{3,}")


def _words(text: str) -> set[str]:
    return set(WORD.findall(text.lower()))


def _view(rec: dict) -> dict:
    return {"kind": rec["kind"], "text": rec["text"], "links": [lk["ref"] for lk in rec["links"]]}


def build_pairs(reports_path: Path, n: int, seed: int) -> list[dict]:
    recs = []
    for line in open(reports_path):
        rep = json.loads(line)
        for r in rep["records"]:
            recs.append((rep["id"], r))
    rng = random.Random(seed)
    scored = []
    for i, (ri, a) in enumerate(recs):
        wa = _words(a["text"])
        best = max(((len(wa & _words(b["text"])) / (len(wa | _words(b["text"])) or 1), j)
                    for j, (rj, b) in enumerate(recs) if rj != ri), default=(0, -1))
        if best[1] >= 0:
            scored.append((best[0], i, best[1]))
    scored.sort(reverse=True)
    seen, pairs = set(), []
    for _, i, j in scored:
        key = tuple(sorted((i, j)))
        if key not in seen and len(pairs) < n * 2 // 3:
            seen.add(key)
            pairs.append(key)
    while len(pairs) < n:
        i, j = rng.sample(range(len(recs)), 2)
        key = tuple(sorted((i, j)))
        if recs[i][0] != recs[j][0] and key not in seen:
            seen.add(key)
            pairs.append(key)
    rng.shuffle(pairs)
    return [{"pair_id": f"p{k:02d}", "a": _view(recs[i][1]), "b": _view(recs[j][1]),
             "a_id": recs[i][1]["id"], "b_id": recs[j][1]["id"], "label": None, "label_note": ""}
            for k, (i, j) in enumerate(pairs, 1)]


def _prompt(p: dict) -> str:
    defs = "\n".join(f"- {k}: {v}" for k, v in DEFINITIONS.items())
    return (f"Two records from AI coding agents' feedback reports.\nA ({p['a']['kind']}): {p['a']['text']} "
            f"links: {p['a']['links']}\nB ({p['b']['kind']}): {p['b']['text']} links: {p['b']['links']}\n"
            f"How does B relate to A?\n{defs}")


def judge(pairs: list[dict], which: str) -> list[dict]:
    from typing import Literal

    from pydantic import BaseModel

    from llm_client import ChoiceQuestion, call_decisions, call_llm_structured

    class Relation(BaseModel):
        relation: Literal["supports", "challenges", "same_problem", "unrelated"]

    out = []
    for p in pairs:
        trace = f"feedback-collector/relation-check/{which}/{p['pair_id']}"
        try:
            if which == "jev":
                r = call_decisions(JEV, state={"A": _view_text(p["a"]), "B": _view_text(p["b"])},
                                   questions={"relation": ChoiceQuestion(
                                       "How does record B relate to record A?", dict(DEFINITIONS))},
                                   task="feedback-collector.relation-check", trace_id=trace, max_budget=0.01)
                a = r.answers["relation"]
                out.append({"pair_id": p["pair_id"], "relation": a.choice,
                            "p": round(a.probabilities.get(a.choice, 0.0), 3), "cost": r.cost})
            else:
                res, meta = call_llm_structured(
                    STRONG, [{"role": "user", "content": _prompt(p)}], response_model=Relation,
                    **({"reasoning_effort": "medium"} if STRONG.startswith("openrouter/") else {}),
                    task="feedback-collector.relation-check", trace_id=trace, max_budget=0.05,
                    model_justification="S2 comparison judge (stronger model) per PLAN.md")
                out.append({"pair_id": p["pair_id"], "relation": res.relation, "cost": meta.cost})
        except Exception as exc:  # parity rule: a judge that fails a pair is out
            out.append({"pair_id": p["pair_id"], "relation": None, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
        print(f"{which} {p['pair_id']}: {out[-1].get('relation')}", flush=True)
    return out


def _view_text(v: dict) -> str:
    return f"({v['kind']}) {v['text']} links: {', '.join(v['links']) or 'none'}"


def score(pairs: list[dict], answers: list[dict]) -> dict:
    labels = {p["pair_id"]: p["label"] for p in pairs}
    if any(v not in RELATIONS for v in labels.values()):
        raise SystemExit("every pair needs a hand label in " + "|".join(RELATIONS) + " before scoring")
    got = {a["pair_id"]: a.get("relation") for a in answers}
    if any(got.get(k) not in RELATIONS for k in labels):
        return {"status": "out (parity: a pair has no valid relation)", "n": len(labels)}
    # a pair may list several defensible answers (`acceptable`), fixed with the label before any judge ran
    ok = {p["pair_id"]: set(p.get("acceptable") or [p["label"]]) for p in pairs}
    right = [k for k in labels if got[k] in ok[k]]
    wrong = [{"pair_id": k, "label": labels[k], "acceptable": sorted(ok[k]), "judge": got[k]}
             for k in labels if got[k] not in ok[k]]
    rate = len(right) / len(labels)
    return {"status": "scored", "n": len(labels), "correct": len(right), "rate": round(rate, 3),
            "meets_bar": rate >= 0.8, "wrong": wrong,
            "cost_usd": round(sum(a.get("cost") or 0 for a in answers), 4)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("pairs"); b.add_argument("reports"); b.add_argument("out"); b.add_argument("-n", type=int, default=30)
    b.add_argument("--seed", type=int, default=8)
    j = sub.add_parser("judge"); j.add_argument("pairs"); j.add_argument("which", choices=("jev", "strong")); j.add_argument("out")
    s = sub.add_parser("score"); s.add_argument("pairs"); s.add_argument("answers")
    a = ap.parse_args()
    if a.cmd == "pairs":
        Path(a.out).write_text(json.dumps(build_pairs(Path(a.reports), a.n, a.seed), indent=1))
        print(f"RESULT pairs={a.n} out={a.out} exit=0")
    elif a.cmd == "judge":
        pairs = json.loads(Path(a.pairs).read_text())
        if any(p["label"] not in RELATIONS for p in pairs):
            raise SystemExit("label every pair before any judge runs (parity rule)")
        ans = judge(pairs, a.which)
        Path(a.out).write_text(json.dumps(ans, indent=1))
        bad = sum(1 for x in ans if x.get("relation") is None)
        print(f"RESULT judge={a.which} pairs={len(ans)} failed={bad} exit={1 if bad else 0}")
        return 1 if bad else 0
    else:
        r = score(json.loads(Path(a.pairs).read_text()), json.loads(Path(a.answers).read_text()))
        print(json.dumps(r, indent=1))
        print(f"RESULT {r['status']} correct={r.get('correct')}/{r['n']} meets_bar={r.get('meets_bar')} exit=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
