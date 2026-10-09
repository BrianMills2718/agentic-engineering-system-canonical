#!/usr/bin/env python3
"""Sort project-meta's legacy rules into covered / keep / retire, with checked quotes (agent-router slice 1).

For each rule in project-meta policy/registry.yaml, one model call (through llm_client) decides:

- covered: an AES register rule or the workspace instruction file already says it;
- keep:    still true and useful; its complete policy stays in the private inventory register;
- retire:  its documents or tools are gone, it was superseded, or it no longer applies.

Every answer must quote its named source. Historical answers and attempts stay in
OUT/legacy-sort.jsonl. Offline --apply/--check read all current sources, bind their
inputs, reject stale evidence, and retain canonical policy text conservatively.
An inventory proposal never activates or removes a mandatory legacy rule.
Full source text stays outside the public checkout. Public dispositions contain
identifiers, validated outcomes and evidence hashes, never imported source prose.

Run detached; prints one line per rule with its timing and a summary with counts and exit status:

    python scripts/rules/sort_legacy.py --apply  # no model calls
    python scripts/rules/sort_legacy.py --check  # no calls or writes

Model-sorting mode (--sort) needs separate sort-call authority. The default is
the offline check, so an inspection cannot accidentally launch paid calls.

Plan: proposals/agent-router/PLAN.md (slice 1).
"""
from __future__ import annotations

import argparse
import hashlib
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
VALIDATION_VERSION = "current-source-inventory/v1"


class Disposition(BaseModel):
    disposition: Literal["covered", "keep", "retire"]
    covered_by: str | None = None
    retire_kind: Literal["source_missing", "tool_missing", "superseded", "obsolete"] | None = None
    quote: str
    quote_from: Literal["source_doc", "workspace_instructions", "aes_register", "legacy_registry", "none"]
    quote_source: str | None = None
    reason: str
    rule: str
    applies_kind: Literal["always", "roles", "actions", "intent"]
    applies_value: str


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


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
    if not answer.applies_value.strip():
        return "applicability needs a nonempty value"
    if answer.disposition == "keep" and not answer.rule.strip():
        return "keep needs a nonempty rule"
    if answer.disposition != "retire" and answer.retire_kind:
        return "retire_kind is only valid for retirement candidates"
    if answer.disposition == "covered" and not answer.covered_by:
        return "covered needs covered_by"
    if answer.disposition == "covered" and answer.covered_by not in sources["aes_ids"] | {"workspace-instructions"}:
        return f"covered_by {answer.covered_by!r} is neither an AES register id nor workspace-instructions"
    if answer.disposition == "retire" and not answer.retire_kind:
        return "retire needs retire_kind"
    if answer.retire_kind == "source_missing" and not f["source_docs"]:
        return "retire_kind source_missing, but no source documents were declared"
    if answer.retire_kind == "source_missing" and any(f["source_docs"].values()):
        return "retire_kind source_missing, but a source document exists"
    if answer.retire_kind == "tool_missing" and (not f["linked_scripts"] or all(f["linked_scripts"].values())):
        return "retire_kind tool_missing, but no linked script is missing"
    if answer.retire_kind in ("source_missing", "tool_missing"):
        return None  # settled by the file facts, no quote needed
    if answer.quote_from == "none" or not answer.quote.strip():
        return "a quote is required for this disposition"
    if answer.disposition == "covered":
        expected = "workspace_instructions" if answer.covered_by == "workspace-instructions" else "aes_register"
        if answer.quote_from != expected:
            return "covered quote must come from the named coverage target"
    haystack = {"source_doc": sources["source_doc"], "workspace_instructions": sources["instructions"],
                "aes_register": sources["register"], "legacy_registry": sources.get("legacy_policy", "")}[answer.quote_from]
    if answer.quote_from == "aes_register":
        haystack = sources.get("aes_targets", {}).get(answer.covered_by, "")
    if answer.quote_from == "source_doc" and sources.get("source_docs"):
        docs = sources["source_docs"]
        if answer.quote_source:
            haystack = docs.get(answer.quote_source, "")
        else:
            haystack = next((text for text in docs.values() if _norm(answer.quote) in _norm(text)), "")
    if answer.quote_from == "legacy_registry" and answer.quote != rule.get("policy"):
        return "registry evidence must quote this policy's complete canonical text"
    if len(_norm(answer.quote)) < 20:
        return "quote shorter than 20 characters"
    if _norm(answer.quote) not in _norm(haystack):
        return f"quote not found verbatim (whitespace normalized) in {answer.quote_from}"
    return None


def source_context(rule: dict, base: list[dict], instructions: str) -> tuple[dict, dict]:
    """Read all declared documents; a navigation page cannot mask a later source."""
    f = facts(rule)
    docs = {path: _resolve(path).read_text(encoding="utf-8", errors="replace")
            for path, exists in f["source_docs"].items() if exists}
    targets = {r["id"]: r["rule"] for r in base}
    return f, {"source_doc": next(iter(docs.values()), ""), "source_docs": docs,
               "instructions": instructions, "legacy_policy": rule["policy"],
               "register": "\n".join(f"{rid}: {text}" for rid, text in targets.items()),
               "aes_targets": targets, "aes_ids": set(targets)}


def input_digest(rule: dict, f: dict, sources: dict) -> str:
    """Bind caller-owned workflow inputs, independently of model call receipts."""
    packet = {"validation_version": VALIDATION_VERSION, "legacy_record": rule, "facts": f,
              "documents": sources["source_docs"], "instructions": sources["instructions"],
              "resolved_documents": {path: str(_resolve(path).resolve()) for path in f["source_docs"]},
              "resolved_tools": {path: str(_resolve(path.split()[0]).resolve()) for path in f["linked_scripts"]},
              "pre_migration_targets": sources["aes_targets"],
              "classifier": {"schema": Disposition.model_json_schema(), "models": [FIRST, SECOND],
                             "efforts": [os.environ.get("SORT_EFFORT", "none"), os.environ.get("SORT_RETRY_EFFORT", "medium")]}}
    source_text = "\n\n".join(f"SOURCE {path}:\n{value}" for path, value in sources["source_docs"].items())
    packet["prompt_sha256"] = hashlib.sha256(prompt(rule, f, source_text, sources["register"], sources["instructions"]).encode()).hexdigest()
    return hashlib.sha256(json.dumps(packet, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


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
ALL CURRENT DECLARED SOURCE DOCUMENTS (labelled by path; set quote_source to the quoted path):
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


def sort_one(rule: dict, register_summary: str, instructions: str, aes_ids: set[str], aes_targets: dict | None = None) -> dict:
    from llm_client import call_llm_structured

    base = [{"id": rid, "rule": value} for rid, value in (aes_targets or {}).items()]
    f, sources = source_context(rule, base, instructions)
    full_sources = "\n\n".join(f"SOURCE {path}:\n{value}" for path, value in sources["source_docs"].items())
    text = prompt(rule, f, full_sources, sources["register"], instructions)
    digest = input_digest(rule, f, sources)
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
            return {"id": rule["id"], "status": "sorted", "facts": f, "input_sha256": digest, **answer.model_dump(), "attempts": attempts}
    return {"id": rule["id"], "status": "unresolved", "facts": f, "input_sha256": digest, "attempts": attempts}


DISPOSITIONS = ROOT / "docs" / "rules" / "legacy-dispositions.yaml"
# Semantic rejection stays recorded even when inventory conservatively retains the policy.
REVIEW_OVERRIDES = {
    "cc-hook-stop-second-brain-work-context": (
        "Retire reasoning rejected on review (2026-10-08): the quoted parity rule says hooks must behave the same in "
        "Claude Code and Codex, which argues for adding the hook to Codex, not for retiring the rule."),
}


SOURCE_REVIEWS = {
    "mcp-on-demand-default": ("docs/ops/MCP_TOOLING_POLICY.md",
        "A capability that is not needed in most sessions must not start one dedicated\nprocess per agent at session startup.",
        "actions", "registering or configuring agent tools, MCP helpers and local services"),
    "pm-runtime-metadata-ephemeral": ("AGENTS.md",
        "volatile fields (`generated_at_utc`, repo `git_head`, repo `is_dirty`) live in "
        "`generated/runtime/ecosystem_runtime_metadata.json` and are never committed",
        "actions", "generating or committing project-meta runtime metadata"),
    "pm-research-synthesis-cutover": ("AGENTS.md",
        "Forward-writing canonical docs must not contain `research_texts`; compatibility aliases and historical artifacts may.",
        "actions", "writing project-meta canonical documentation"),
    "derived-project-workspace-views": ("policy/proposals/2026-08-22-derived-project-workspace-views.yaml",
        "When operator workspace views are created, they derive from canonical project\n"
        "membership and repository checkout metadata.", "actions", "generating or updating operator project workspace views"),
}


def retain(rule: dict, row: dict, reason: str) -> Disposition:
    """Conservative fallback preserves authority, not a model's abbreviated rewrite.

    The registry itself is an authority route in project-meta's POLICY_SYSTEM.md.
    Missing/changed documentation is not permission to remove its current policy.
    Applicability remains an inventory proposal; this function activates no rule.
    """
    kind = row.get("applies_kind", "intent")
    value = row.get("applies_value", "")
    if kind not in {"always", "roles", "actions", "intent"} or not isinstance(value, str) or not value.strip():
        kind, value = "intent", rule.get("scope") or f"legacy policy {rule['id']}: retain existing applicability"
    return Disposition(disposition="keep", quote=rule["policy"], quote_from="legacy_registry",
                       quote_source=f"project-meta/policy/registry.yaml#policies/{rule['id']}/policy",
                       rule=rule["policy"], reason=reason, applies_kind=kind, applies_value=value)


def reviewed_answer(rule: dict, row: dict, f: dict, sources: dict) -> tuple[Disposition, str | None]:
    """Recheck historical proposals against current inputs; never call a model."""
    rid = rule["id"]
    if rid in SOURCE_REVIEWS:
        path, quote, kind, value = SOURCE_REVIEWS[rid]
        answer = retain(rule, row, "Offline source review: use the full current declared source; retain the complete canonical policy.")
        answer = answer.model_copy(update={"quote": quote, "quote_from": "source_doc", "quote_source": path,
                                           "applies_kind": kind, "applies_value": value})
        error = check(answer, rule, f, sources)
        if error:
            raise ValueError(f"{rid}: reviewed source changed: {error}")
        return answer, "historical unresolved or stale proposal replaced by current-source retention"
    if rid in REVIEW_OVERRIDES or rid == "real-tests-not-mocks":
        reason = REVIEW_OVERRIDES.get(rid, "Declared AGENTS anchor no longer contains the requirement; the current canonical registry still does. Retain it without inventing an AGENTS quotation.")
        return retain(rule, row, reason), reason
    error = None
    if row.get("status") != "sorted":
        error = "historical classifier did not produce an accepted answer"
    elif row.get("facts") != f:
        error = "declared source/tool facts changed since the historical call"
    elif row.get("input_sha256") and row["input_sha256"] != input_digest(rule, f, sources):
        error = "cached workflow input digest differs from current inputs"
    else:
        try:
            answer = Disposition.model_validate(row)
            error = check(answer, rule, f, sources)
            if not error and answer.disposition == "retire" and answer.retire_kind in {"obsolete", "superseded"}:
                error = "semantic retirement has no adopted retirement decision; conservatively retain the current policy"
        except ValueError as exc:
            error = f"invalid cached disposition/tag: {exc}"
    if error:
        return retain(rule, row, f"Offline conservative retention: {error}. Routing review remains separate."), error
    if answer.disposition == "keep":
        answer = answer.model_copy(update={"rule": rule["policy"]})
    if answer.quote_from == "source_doc" and not answer.quote_source:
        answer = answer.model_copy(update={"quote_source": next(path for path, text in sources["source_docs"].items()
                                                               if _norm(answer.quote) in _norm(text))})
    return answer, None


def apply(cache_path: Path, *, check_only: bool = False) -> int:
    """Materialize or check an input-bound inventory; preserve raw attempts unchanged."""
    private_register = OUT / "legacy-register.private.yaml"
    private_dispositions = OUT / "legacy-dispositions.private.yaml"
    for path in (private_register, private_dispositions):
        resolved = path.resolve()
        if resolved.is_relative_to(ROOT.resolve()) or any(
                (p / ".git").is_file() or (p / ".git" / "HEAD").is_file() for p in resolved.parents):
            raise ValueError("private inventory output must be outside the public repository and all Git checkouts")
    raw = cache_path.read_bytes()
    latest, cache_lines, historical = {}, {}, []
    for line_no, line in enumerate(raw.decode().splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        latest[row["id"]], cache_lines[row["id"]] = row, line_no
        historical.extend(row.get("attempts", []))
    policies = yaml.safe_load(LEGACY.read_text(encoding="utf-8"))["policies"]
    legacy = {r["id"]: r for r in policies}
    if len(legacy) != len(policies) or set(legacy) != set(latest):
        print(f"RESULT membership failed: duplicate_source_ids={len(policies)-len(legacy)}; "
              f"missing={sorted(set(legacy)-set(latest))}; extra={sorted(set(latest)-set(legacy))}; exit_status=1")
        return 1
    original_register = REGISTER.read_bytes()
    register = yaml.safe_load(original_register)
    base = [r for r in register["rules"] if r.get("origin") != "legacy-migrated"]
    if len({r["id"] for r in base}) != len(base):
        raise ValueError("ambiguous pre-migration coverage target ids")
    register["rules"] = list(base)
    instructions = INSTRUCTIONS.read_text(encoding="utf-8")
    rows = []
    for rid in sorted(legacy):
        rule, cached = legacy[rid], latest[rid]
        f, sources = source_context(rule, base, instructions)
        answer, rejected = reviewed_answer(rule, cached, f, sources)
        error = check(answer, rule, f, sources)
        if error:
            raise ValueError(f"{rid}: final inventory evidence failed: {error}")
        entry = {"id": rid, **answer.model_dump(exclude_none=True),
                 "input_sha256": input_digest(rule, f, sources), "source_facts": f,
                 "historical_cache": {"line": cache_lines[rid], "disposition": cached.get("disposition", cached["status"]),
                                      "input_bound": bool(cached.get("input_sha256"))},
                 "validation": VALIDATION_VERSION, "activation": "none"}
        if rejected:
            entry["historical_rejection"] = rejected
        if answer.disposition == "keep":
            kept_id = rid if rid not in sources["aes_ids"] else f"legacy-{rid}"
            entry["kept_as"] = kept_id
            register["rules"].append({
                "id": kept_id, "rule": rule["policy"], "origin": "legacy-migrated",
                "source": f"project-meta/policy/registry.yaml#policies/{rid}",
                "enforcement_status": rule.get("enforcement_status", "unstated"),
                "enforcement_mechanism": rule.get("enforcement_mechanism", "unstated"),
                "evidence": {k: entry[k] for k in ("quote", "quote_from", "quote_source", "input_sha256") if k in entry},
                "applies_when": {"kind": answer.applies_kind, "value": answer.applies_value,
                                 "proposed_by": VALIDATION_VERSION},
                "migrated_from": f"project-meta:{rid}",
                "feedback_path": "feedback record: an `obs (control)` line naming the rule id"})
        rows.append(entry)
    ids = [r["id"] for r in register["rules"]]
    if len(ids) != len(set(ids)):
        raise ValueError("inventory would duplicate an AES rule id")
    # Recheck every source before writing, including files changed during this run.
    for entry in rows:
        f, sources = source_context(legacy[entry["id"]], base, INSTRUCTIONS.read_text(encoding="utf-8"))
        if entry["input_sha256"] != input_digest(legacy[entry["id"]], f, sources):
            raise ValueError(f"{entry['id']}: source changed during inventory build; rerun offline")
    if REGISTER.read_bytes() != original_register or cache_path.read_bytes() != raw:
        raise ValueError("register/cache changed during inventory build; rerun offline")
    document = {"schema_version": "aes-legacy-dispositions/v1", "validation_version": VALIDATION_VERSION,
                "about": "Current-source inventory proposals only. Quotes match named current sources with whitespace normalization. Kept policies preserve complete canonical text. Retire is a candidate, never rule removal. Mandatory legacy baseline remains unchanged; applicability and semantic coverage need routing review.",
                "cache_sha256": hashlib.sha256(raw).hexdigest(),
                "historical_accounting": {"attempts": len(historical),
                    "known_cost_usd": sum(a["cost"] for a in historical if isinstance(a.get("cost"), (int, float))),
                    "unknown_cost_attempts": sum(not isinstance(a.get("cost"), (int, float)) for a in historical),
                    "complete_cost": all(isinstance(a.get("cost"), (int, float)) for a in historical)},
                "rules": rows}
    serialize = lambda value: yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=110)
    disposition_text, register_text = serialize(document), serialize(register)
    # Allowlist structural fields. Do not guess which source prose is private.
    # The complete source-linked record remains available to private consumers.
    public_rows = []
    for entry in rows:
        public = {key: entry[key] for key in
                  ("id", "disposition", "covered_by", "retire_kind", "kept_as", "quote_from",
                   "input_sha256", "validation", "activation", "applies_kind") if key in entry}
        for key in ("quote", "reason", "rule", "applies_value"):
            public[key + "_sha256"] = hashlib.sha256(entry.get(key, "").encode()).hexdigest()
        public_rows.append(public)
    public_document = {
        "schema_version": "aes-legacy-dispositions-public/v1",
        "validation_version": VALIDATION_VERSION,
        "about": "Inventory proposals only. Complete source text, quotes and applicability values remain in the private inventory. No mandatory rule is removed or activated.",
        "source": "project-meta/policy/registry.yaml",
        "cache_sha256": document["cache_sha256"],
        "private_dispositions_sha256": hashlib.sha256(disposition_text.encode()).hexdigest(),
        "private_register_sha256": hashlib.sha256(register_text.encode()).hexdigest(),
        "historical_accounting": document["historical_accounting"],
        "rules": public_rows,
    }
    public_text = serialize(public_document)
    # Keep the published baseline unchanged; migration is an inventory proposal.
    public_register = {**register, "rules": base}
    baseline_text = serialize(public_register)
    if check_only:
        expected = {DISPOSITIONS: public_text, REGISTER: baseline_text,
                    private_dispositions: disposition_text, private_register: register_text}
        ok = all(path.exists() and path.read_text() == text for path, text in expected.items())
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for path, text in ((private_dispositions, disposition_text), (private_register, register_text)):
            # Restrict permissions before writing private source text.
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(text)
        DISPOSITIONS.write_text(public_text, encoding="utf-8")
        REGISTER.write_text(baseline_text, encoding="utf-8")
        ok = True
    counts = {kind: sum(r["disposition"] == kind for r in rows) for kind in ("keep", "covered", "retire")}
    print(f"RESULT inventory {'check' if check_only else 'apply'}: exact_ids={len(rows)}; {json.dumps(counts, sort_keys=True)}; "
          f"failed={0 if ok else 1}; unknown_cost_attempts={document['historical_accounting']['unknown_cost_attempts']}; exit_status={0 if ok else 1}")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--limit", type=int, default=0, help="sort at most N not-yet-sorted rules (0 = all)")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--only", nargs="*", help="sort just these rule ids (ignores the cache for them)")
    parser.add_argument("--apply", action="store_true", help="write private full inventory and public hash-only dispositions; preserve published baseline")
    parser.add_argument("--check", action="store_true", help="revalidate cached inventory against current inputs, without calls or writes")
    parser.add_argument("--sort", action="store_true", help="explicit model-sorting mode; requires separate sort-call authority")
    args = parser.parse_args()
    if sum((args.apply, args.check, args.sort)) > 1:
        parser.error("choose one of --apply, --check or --sort")
    if not args.sort:
        return apply(OUT / "legacy-sort.jsonl", check_only=not args.apply)

    OUT.mkdir(parents=True, exist_ok=True)
    cache_path = OUT / "legacy-sort.jsonl"
    done = {}
    if cache_path.exists():
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            done[row["id"]] = row
    legacy = yaml.safe_load(LEGACY.read_text(encoding="utf-8"))["policies"]
    register = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    base = [r for r in register["rules"] if r.get("origin") != "legacy-migrated"]
    aes_targets = {r["id"]: r["rule"] for r in base}
    register_summary = "\n".join(f"{rid}: {text}" for rid, text in aes_targets.items())
    aes_ids = set(aes_targets)
    instructions = INSTRUCTIONS.read_text(encoding="utf-8")
    def fresh(rule: dict) -> bool:
        f, sources = source_context(rule, base, instructions)
        return done.get(rule["id"], {}).get("input_sha256") == input_digest(rule, f, sources)
    todo = [r for r in legacy if (args.only and r["id"] in args.only) or (not args.only and not fresh(r))]
    if args.limit:
        todo = todo[: args.limit]
    print(f"legacy rules {len(legacy)}; cached {len(done)}; to sort now {len(todo)}; models {FIRST} then {SECOND}", flush=True)

    t_start = time.monotonic()
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool, cache_path.open("a", encoding="utf-8") as out:
        futures = {pool.submit(sort_one, r, register_summary, instructions, aes_ids, aes_targets): r["id"] for r in todo}
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
    unknown = sum(a.get("cost") is None for row in results for a in row.get("attempts", []))
    unresolved = counts.get("unresolved", 0)
    print(f"RESULT sorted {len(results)} this run: {json.dumps(counts, sort_keys=True)}; known cost ${cost:.3f}; "
          f"unknown cost attempts {unknown}; {time.monotonic() - t_start:.0f}s; exit_status {1 if unresolved else 0}", flush=True)
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
