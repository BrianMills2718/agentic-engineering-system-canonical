#!/usr/bin/env python3
"""Report functions a branch adds that rewrite an existing function under a new name (AES pilot).

The maintainability ratchet (`scripts/maintainability_ratchet.py`) catches copied code; it cannot see
an existing helper written again in different words. This check reads for meaning, with two model
calls through `llm_client` (plain-first: the whole index and the question):

  1. candidates: the index of every function at the merge base (one line each, sent first so the
     provider can cache it) plus the full source of each new function; the model names up to three
     existing functions each new one may duplicate;
  2. judge: each new function with the full source of its named candidates; the model gives
     same_job, partial_overlap or different.

New functions: module-level functions and class methods in changed `.py` files under the folders,
whose `path::name` is not on the base and whose source is not on the base under any name (a moved
function is not new). `main`, `test_*` and dunder methods are left out; short wrappers stay in, as they are the most
rewritten helpers (AES has 27 git wrappers).
Answers are cached by a hash of model and messages under `<git-common-dir>/helper-reuse/`.

Prints `RESULT helper-reuse new_functions=<n> flagged=<n> cost_usd=<x> exit=<0|1>`; exit 1 when a
function is same_job. A failed model call or tool step prints `RESULT helper-reuse tool-failed exit=2`.
It needs `llm_client` (run with that project's Python); it is report-only and not part of make check.
Traces: `aes/helper-reuse/<head>/<candidates|judge>`, task `aes.helper-reuse`.
Not covered: a rewrite of a function defined inside another function, and duplicates across repositories.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any, Literal, TypeVar

from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lockstep.ship import git as _git  # noqa: E402  # the path is set just above
PROMPTS = ROOT / "prompts" / "helper_reuse"
MODEL_TASK = os.environ.get("HELPER_REUSE_MODEL", "fast_cheap_mid")  # llm_client task selector or a route
REASONING = os.environ.get("HELPER_REUSE_REASONING", "high")  # llm_client requires it stated


_M = TypeVar("_M", bound=BaseModel)


class _Candidate(BaseModel):
    new_id: str = Field(description="id of the new function, exactly as given")
    existing_ids: list[str] = Field(description="up to three index ids that may do the same job; empty if none")


class _Candidates(BaseModel):
    items: list[_Candidate]


class _Verdict(BaseModel):
    new_id: str = Field(description="id of the new function, exactly as given")
    verdict: Literal["same_job", "partial_overlap", "different"]
    existing_id: str | None = Field(description="the existing function for same_job or partial_overlap, else null")
    reason: str = Field(description="one sentence pointing at the code")


class _Verdicts(BaseModel):
    items: list[_Verdict]


def _functions(path: str, text: str) -> dict[str, dict[str, Any]]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {}
    lines = text.splitlines()
    out: dict[str, dict[str, Any]] = {}

    def add(node: ast.FunctionDef | ast.AsyncFunctionDef, owner: str) -> None:
        name = f"{owner}{node.name}"
        start = min([d.lineno for d in node.decorator_list] + [node.lineno])
        source = textwrap.dedent("\n".join(lines[start - 1:node.end_lineno]))
        doc = (ast.get_docstring(node) or "").strip().split("\n")[0]
        out[f"{path}::{name}"] = {"id": f"{path}::{name}", "name": node.name, "source": source,
                                  "line": f"{path}::{name}({ast.unparse(node.args)}) {doc}".rstrip()}

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add(node, "")
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    add(item, f"{node.name}.")
    return out


def _in_folders(path: str, folders: list[str]) -> bool:
    return path.endswith(".py") and any(path.startswith(f.rstrip("/") + "/") for f in folders)


def _base_functions(repo: Path, base: str, folders: list[str]) -> dict[str, dict[str, Any]]:
    paths = [p for p in _git(repo, "ls-tree", "-r", "--name-only", base).splitlines() if _in_folders(p, folders)]
    found: dict[str, dict[str, Any]] = {}
    for p in paths:
        found.update(_functions(p, _git(repo, "show", f"{base}:{p}")))
    return found


def _read(repo: Path, head: str | None, path: str) -> str | None:
    """A file's text in the working tree (head None) or at revision head; None when absent."""
    if head is None:
        return (repo / path).read_text() if (repo / path).is_file() else None
    try:
        return _git(repo, "show", f"{head}:{path}")
    except subprocess.CalledProcessError:
        return None


def _new_functions(repo: Path, base: str, head: str | None, folders: list[str],
                   old: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    if head is None:
        changed = _git(repo, "diff", "--name-only", "--diff-filter=AMR", base).splitlines()
        changed += _git(repo, "ls-files", "--others", "--exclude-standard").splitlines()
    else:
        changed = _git(repo, "diff", "--name-only", "--diff-filter=AMR", base, head).splitlines()
    old_sources = {f["source"] for f in old.values()}
    new = []
    for p in sorted(set(changed)):
        text = _read(repo, head, p) if _in_folders(p, folders) else None
        if text is None:
            continue
        for fid, f in _functions(p, text).items():
            skip = (f["name"] == "main" or f["name"].startswith("test_")
                    or (f["name"].startswith("__") and f["name"].endswith("__")))
            if not skip and fid not in old and f["source"] not in old_sources:
                new.append(f)
    return new


def _render(template: str, **context: Any) -> list[dict[str, str]]:
    from llm_client import render_prompt

    return render_prompt(PROMPTS / template, **context)


def _ask(model: str, messages: list[dict[str, str]], response_model: type[_M], trace_id: str) -> tuple[_M, float]:
    from llm_client import call_llm_structured

    result, meta = call_llm_structured(model, messages, response_model=response_model, task="aes.helper-reuse",
                                       reasoning_effort=REASONING, trace_id=trace_id, max_budget=0.5,
                                       model_justification="AES helper-reuse pilot (slice 4 of the Reddit-ideas plan)")
    return result, float(meta.cost or 0.0)


def _resolve(model: str) -> str:
    if "/" in model:
        return model
    from llm_client.core.models import get_model

    return get_model(model)


def _read_cache(hit: Path, response_model: type[_M]) -> _M | None:
    """A cached answer, or None when there is none or it is damaged (then it is asked again)."""
    if not hit.is_file():
        return None
    try:
        return response_model.model_validate_json(hit.read_text())
    except ValueError:
        return None


def _cached_ask(cache: Path, model: str, messages: list[dict[str, str]], response_model: type[_M],
                trace_id: str) -> tuple[_M, float]:
    key = hashlib.sha256(json.dumps([model, messages], sort_keys=True).encode()).hexdigest()
    hit = cache / f"{key}.json"
    cached = _read_cache(hit, response_model)
    if cached is not None:
        return cached, 0.0
    result, cost = _ask(model, messages, response_model, trace_id)
    cache.mkdir(parents=True, exist_ok=True)
    tmp = hit.with_suffix(".tmp")
    tmp.write_text(result.model_dump_json())
    tmp.replace(hit)
    return result, cost


def _candidates_context(old: dict[str, dict[str, Any]], new: list[dict[str, Any]]) -> dict[str, Any]:
    """The template context for call 1: the base index (sorted, stable) and the new functions."""
    return {"index": "\n".join(f["line"] for _, f in sorted(old.items())),
            "new_functions": [{"id": f["id"], "source": f["source"]} for f in new]}


def _run(repo: Path, base: str, head_rev: str | None, folders: list[str], model: str) -> tuple[list[dict[str, Any]], list[_Verdict], float]:
    merge_base = _git(repo, "merge-base", base, head_rev or "HEAD").strip()
    head = _git(repo, "rev-parse", "--short", head_rev or "HEAD").strip()
    old = _base_functions(repo, merge_base, folders)
    new = _new_functions(repo, merge_base, head_rev, folders, old)
    if not new:
        return [], [], 0.0
    cache = Path(_git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir").strip()) / "helper-reuse"
    route = _resolve(model)
    found, cost1 = _cached_ask(cache, route, _render("candidates.yaml", **_candidates_context(old, new)),
                               _Candidates, f"aes/helper-reuse/{head}/candidates")
    by_new = {c.new_id: [e for e in c.existing_ids if e in old][:3] for c in found.items}
    pairs = [{"id": f["id"], "source": f["source"],
              "candidates": [{"id": e, "source": old[e]["source"]} for e in by_new.get(f["id"], [])]}
             for f in new if by_new.get(f["id"])]
    if not pairs:
        return new, [], cost1
    judged, cost2 = _cached_ask(cache, route, _render("judge.yaml", pairs=pairs), _Verdicts,
                                f"aes/helper-reuse/{head}/judge")
    return new, list(judged.items), cost1 + cost2


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--folders", default="src,scripts")
    ap.add_argument("--head", default=None, help="read the branch at this revision instead of the working tree")
    ap.add_argument("--model", default=MODEL_TASK)
    a = ap.parse_args(argv)
    try:
        new, verdicts, cost = _run(a.repo.resolve(), a.base, a.head, a.folders.split(","), a.model)
    except Exception as exc:  # noqa: BLE001  # any failed step must fail closed
        print(f"helper-reuse: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("RESULT helper-reuse tool-failed exit=2")
        return 2
    flagged = [v for v in verdicts if v.verdict == "same_job"]
    for v in verdicts:
        if v.verdict != "different":
            print(f"{v.verdict}: {v.new_id} -> {v.existing_id}: {v.reason}")
    print(f"RESULT helper-reuse new_functions={len(new)} flagged={len(flagged)} cost_usd={cost:.4f} "
          f"exit={1 if flagged else 0}")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
