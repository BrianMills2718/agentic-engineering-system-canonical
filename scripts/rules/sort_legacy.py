#!/usr/bin/env python3
"""Sort project-meta's legacy rules into covered / keep / retire, with checked quotes (agent-router slice 1).

For each rule in project-meta policy/registry.yaml, one model call (through llm_client) decides:

- covered: an AES register rule or the workspace instruction file already says it;
- keep:    still true and useful; it moves into the AES register with a plain one-sentence rule;
- retire:  its documents or tools are gone, it was superseded, or it no longer applies.

Every answer must quote the text that justifies it. The quote is then checked, by plain substring
match, against the file it claims to come from; a failed check gets one retry on a stronger model,
and a second failure is recorded as `unresolved` (the rule stays legacy). Answers are cached by
rule id in OUT/legacy-sort.jsonl, so a rerun only calls the model for rules not yet sorted.

Run detached; prints one line per rule with its timing and a summary with counts and exit status:

    ~/code/llm_client/.venv/bin/python scripts/rules/sort_legacy.py [--limit N] [--workers 8]

Plan: proposals/agent-router/PLAN.md (slice 1).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "docs" / "rules" / "register.yaml"
PROJECT_META = Path(os.environ.get("PROJECT_META", Path.home() / "code" / "project-meta"))
LEGACY = PROJECT_META / "policy" / "registry.yaml"
INSTRUCTIONS = Path(os.environ.get("WORKSPACE_INSTRUCTIONS", Path.home() / "code" / "AGENTS.md"))
OUT = Path(os.environ.get("AGENT_ROUTER_OUT", Path.home() / "projects" / "data" / "agent-router"))
FIRST = os.environ.get("SORT_MODEL", "openrouter/deepseek/deepseek-v4-flash")
SECOND = os.environ.get("SORT_RETRY_MODEL", "openrouter/openai/gpt-5.6-sol")
SOURCE_CHARS = 6000


class Disposition(BaseModel):
    disposition: Literal["covered", "keep", "retire"]
    covered_by: str | None = None
    retire_kind: Literal["source_missing", "tool_missing", "superseded", "obsolete"] | None = None
    quote: str
    quote_from: Literal["source_doc", "workspace_instructions", "aes_register", "none"]
    reason: str
    rule: str
    applies_kind: Literal["always", "roles", "actions", "intent"]
    applies_value: str


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _resolve(rel: str) -> Path:
    """A source path as the legacy register wrote it: absolute, ~, project-meta-relative or workspace-relative."""
    p = Path(os.path.expanduser(rel))
    if p.is_absolute():
        return p
    for base in (PROJECT_META, PROJECT_META.parent, Path.home() / "projects"):
        if (base / p).exists():
            return base / p
    return PROJECT_META / p


def facts(rule: dict) -> dict:
    """Plain file facts the model must not contradict."""
    docs = [str(d) for d in rule.get("source_docs") or []]
    scripts = [str(s) for s in rule.get("linked_scripts") or []]
    present_docs = [d for d in docs if _resolve(d).is_file()]
    return {
        "source_docs": {d: (d in present_docs) for d in docs},
        "linked_scripts": {s: _resolve(s.split()[0]).exists() for s in scripts},
        "first_source": present_docs[0] if present_docs else None,
    }


def check(answer: Disposition, rule: dict, f: dict, sources: dict[str, str]) -> str | None:
    """Return why the answer fails its evidence check, or None when it passes."""
    if answer.disposition == "covered" and not answer.covered_by:
        return "covered needs covered_by"
    if answer.disposition == "covered" and answer.covered_by not in sources["aes_ids"] | {"workspace-instructions"}:
        return f"covered_by {answer.covered_by!r} is neither an AES register id nor workspace-instructions"
    if answer.disposition == "retire" and not answer.retire_kind:
        return "retire needs retire_kind"
    if answer.retire_kind == "source_missing" and any(f["source_docs"].values()):
        return "retire_kind source_missing, but a source document exists"
    if answer.retire_kind == "tool_missing" and (not f["linked_scripts"] or all(f["linked_scripts"].values())):
        return "retire_kind tool_missing, but no linked script is missing"
    if answer.retire_kind in ("source_missing", "tool_missing"):
        return None  # settled by the file facts, no quote needed
    if answer.quote_from == "none" or not answer.quote.strip():
        return "a quote is required for this disposition"
    haystack = {"source_doc": sources["source_doc"], "workspace_instructions": sources["instructions"],
                "aes_register": sources["register"]}[answer.quote_from]
    if len(_norm(answer.quote)) < 20:
        return "quote shorter than 20 characters"
    if _norm(answer.quote) not in _norm(haystack):
        return f"quote not found verbatim in {answer.quote_from}"
    return None


def prompt(rule: dict, f: dict, source_text: str, register_summary: str, instructions: str) -> str:
    fields = {k: rule.get(k) for k in ("id", "policy", "intent", "scope", "enforcement_status",
                                       "enforcement_mechanism", "gaps", "source_docs", "linked_scripts")}
    return f"""You are sorting one legacy rule from an old register before a migration.

Decide one disposition:
- "covered": the CURRENT workspace instructions or the AES rules register already state this rule (same requirement, maybe other words). Set covered_by to the AES rule id, or "workspace-instructions".
  Covered means the requirement itself is stated there. A line that only says to read some document (for example "read its Deployment Hosting Policy") does NOT cover the rules inside that document: those are "keep" (or "retire").
- "keep": the rule is still a real, useful requirement for coding agents and is NOT already covered. Write `rule` as one plain sentence an agent can follow.
- "retire": its source documents or tools are gone (use the FILE FACTS), it was superseded by something newer, or it no longer applies to how work is done now.

Evidence is mandatory. `quote` must be copied VERBATIM (at least 20 characters, exact words) from the text named in quote_from:
- covered -> quote from workspace_instructions or aes_register, showing the same requirement;
- keep -> quote from source_doc showing the requirement;
- retire with superseded/obsolete -> quote from source_doc or workspace_instructions showing why;
- retire with source_missing/tool_missing -> quote may be empty and quote_from "none"; it must agree with FILE FACTS.

Also say when the rule applies, for injecting it at the right moment:
- applies_kind "always": safety-critical, must always be loaded;
- "actions": tied to a tool action; applies_value is the action (e.g. "gh pr merge", "git commit", "editing UI files");
- "roles": tied to a kind of agent; applies_value lists roles (e.g. "frontend, reviewer");
- "intent": tied to what the user wants; applies_value describes when.

FILE FACTS (checked by code, true): {json.dumps(f)}

LEGACY RULE:
{yaml.safe_dump(fields, sort_keys=False, allow_unicode=True)}
SOURCE DOCUMENT ({f['first_source'] or 'none present'}), first {SOURCE_CHARS} characters:
<<<
{source_text}
>>>

AES RULES REGISTER (id: rule):
<<<
{register_summary}
>>>

CURRENT WORKSPACE INSTRUCTIONS:
<<<
{instructions}
>>>
"""


def sort_one(rule: dict, register_summary: str, instructions: str, aes_ids: set[str]) -> dict:
    from llm_client import call_llm_structured

    f = facts(rule)
    full_source = _resolve(f["first_source"]).read_text(encoding="utf-8", errors="replace") if f["first_source"] else ""
    sources = {"source_doc": full_source, "instructions": instructions, "register": register_summary, "aes_ids": aes_ids}
    text = prompt(rule, f, full_source[:SOURCE_CHARS], register_summary, instructions)
    attempts = []
    for model, effort in ((FIRST, os.environ.get("SORT_EFFORT", "none")), (SECOND, os.environ.get("SORT_RETRY_EFFORT", "medium"))):
        messages = [{"role": "user", "content": text}]
        if attempts:
            messages.append({"role": "user", "content": f"Your previous answer failed its evidence check: "
                             f"{attempts[-1]['failed']}. Answer again; copy any quote exactly."})
        t0 = time.monotonic()
        try:
            answer, meta = call_llm_structured(
                model, messages, response_model=Disposition, reasoning_effort=effort,
                task="agent-router.legacy-sort", trace_id=f"agent-router/legacy-sort/{rule['id']}/{len(attempts)}",
                max_budget=0.05 if model == FIRST else 0.15, model_justification="agent-router PLAN.md slice 1: legacy rule sort")
        except Exception as exc:  # noqa: BLE001 -- a failed call is recorded, not retried on the same model
            attempts.append({"model": model, "failed": f"{type(exc).__name__}: {str(exc)[:200]}",
                             "seconds": round(time.monotonic() - t0, 1)})
            continue
        failed = check(answer, rule, f, sources)
        attempts.append({"model": model, "answer": answer.model_dump(), "failed": failed,
                         "cost": getattr(meta, "cost", None), "seconds": round(time.monotonic() - t0, 1)})
        if failed is None:
            return {"id": rule["id"], "status": "sorted", "facts": f, **answer.model_dump(), "attempts": attempts}
    return {"id": rule["id"], "status": "unresolved", "facts": f, "attempts": attempts}


DISPOSITIONS = ROOT / "docs" / "rules" / "legacy-dispositions.yaml"
# Answers rejected on human-or-agent review of the sort's output, with the reviewer's reason; such a rule stays legacy.
REVIEW_OVERRIDES = {
    "cc-hook-stop-second-brain-work-context": (
        "Retire reasoning rejected on review (2026-10-08): the quoted parity rule says hooks must behave the same in "
        "Claude Code and Codex, which argues for adding the hook to Codex, not for retiring the rule."),
}


def apply(cache_path: Path) -> int:
    """Write every legacy rule's disposition and move the kept ones into the AES register."""
    latest: dict[str, dict] = {}
    for line in cache_path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        latest[row["id"]] = row  # a later row for the same id (a rerun) replaces the earlier one
    legacy = {r["id"]: r for r in yaml.safe_load(LEGACY.read_text(encoding="utf-8"))["policies"]}
    missing = sorted(set(legacy) - set(latest))
    register = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    register["rules"] = [r for r in register["rules"] if r.get("origin") != "legacy-migrated"]
    rows = []
    for rid in sorted(legacy):
        row = latest.get(rid, {"status": "unsorted"})
        disp = row.get("disposition") if row.get("status") == "sorted" else row.get("status", "unsorted")
        if rid in REVIEW_OVERRIDES:
            disp = "unresolved"
        entry = {"id": rid, "disposition": disp}
        if rid in REVIEW_OVERRIDES:
            entry["review"] = REVIEW_OVERRIDES[rid]
        if row.get("status") == "sorted" and rid not in REVIEW_OVERRIDES:
            entry.update({k: row.get(k) for k in ("covered_by", "retire_kind", "reason", "quote_from", "quote") if row.get(k)})
            entry["sorted_by"] = row["attempts"][-1]["model"]
        rows.append(entry)
        if disp == "keep":
            old = legacy[rid]
            register["rules"].append({
                "id": rid, "rule": row["rule"], "origin": "legacy-migrated",
                "source": f"project-meta policy/registry.yaml ({', '.join(map(str, old.get('source_docs') or []))})",
                "enforcement_status": old.get("enforcement_status"),
                "enforcement_mechanism": old.get("enforcement_mechanism"),
                "evidence": {"quote": row["quote"], "quote_from": row["quote_from"]},
                "applies_when": {"kind": row["applies_kind"], "value": row["applies_value"], "proposed_by": row["attempts"][-1]["model"]},
                "migrated_from": f"project-meta:{rid}",
                "feedback_path": "feedback record: an `obs (control)` line naming the rule id",
            })
    DISPOSITIONS.write_text(yaml.safe_dump({
        "schema_version": "aes-legacy-dispositions/v1",
        "about": ("Every rule in project-meta policy/registry.yaml with its disposition from the agent-router slice 1 sort "
                  "(scripts/rules/sort_legacy.py): covered (already stated elsewhere), keep (moved into register.yaml), "
                  "retire, or unresolved (its evidence check failed twice; it stays legacy). Each quote was checked "
                  "verbatim against the file named in quote_from."),
        "rules": rows}, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")
    REGISTER.write_text(yaml.safe_dump(register, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["disposition"]] = counts.get(r["disposition"], 0) + 1
    print(f"RESULT applied {len(rows)} legacy rules: {json.dumps(counts, sort_keys=True)}; "
          f"not yet sorted {len(missing)}; exit {1 if missing else 0}")
    return 1 if missing else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--limit", type=int, default=0, help="sort at most N not-yet-sorted rules (0 = all)")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--only", nargs="*", help="sort just these rule ids (ignores the cache for them)")
    parser.add_argument("--apply", action="store_true", help="write dispositions and move kept rules into the register")
    args = parser.parse_args()
    if args.apply:
        return apply(OUT / "legacy-sort.jsonl")

    OUT.mkdir(parents=True, exist_ok=True)
    cache_path = OUT / "legacy-sort.jsonl"
    done = {}
    if cache_path.exists():
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            done[row["id"]] = row
    legacy = yaml.safe_load(LEGACY.read_text(encoding="utf-8"))["policies"]
    register = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    register_summary = "\n".join(f"{r['id']}: {r['rule']}" for r in register["rules"])
    aes_ids = {r["id"] for r in register["rules"]}
    instructions = INSTRUCTIONS.read_text(encoding="utf-8")
    todo = [r for r in legacy if (args.only and r["id"] in args.only) or (not args.only and r["id"] not in done)]
    if args.limit:
        todo = todo[: args.limit]
    print(f"legacy rules {len(legacy)}; cached {len(done)}; to sort now {len(todo)}; models {FIRST} then {SECOND}", flush=True)

    t_start = time.monotonic()
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool, cache_path.open("a", encoding="utf-8") as out:
        futures = {pool.submit(sort_one, r, register_summary, instructions, aes_ids): r["id"] for r in todo}
        for fut in as_completed(futures):
            rid = futures[fut]
            try:
                row = fut.result()
            except Exception as exc:  # noqa: BLE001 -- one bad rule must not erase the rest of the batch
                row = {"id": rid, "status": "unresolved", "attempts": [{"failed": f"{type(exc).__name__}: {exc}"}]}
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            results.append(row)
            secs = sum(a.get("seconds", 0) for a in row.get("attempts", []))
            print(f"[{time.monotonic() - t_start:7.1f}s] {rid}: {row['status']} {row.get('disposition', '')} "
                  f"({len(row.get('attempts', []))} attempt(s), {secs:.1f}s)", flush=True)

    counts: dict[str, int] = {}
    for row in results:
        key = row.get("disposition") or row["status"]
        counts[key] = counts.get(key, 0) + 1
    cost = sum((a.get("cost") or 0) for row in results for a in row.get("attempts", []))
    unresolved = counts.get("unresolved", 0)
    print(f"RESULT sorted {len(results)} this run: {json.dumps(counts, sort_keys=True)}; cost ${cost:.3f}; "
          f"{time.monotonic() - t_start:.0f}s; exit {1 if unresolved else 0}", flush=True)
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
