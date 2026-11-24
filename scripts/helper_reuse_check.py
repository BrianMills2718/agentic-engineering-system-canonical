#!/usr/bin/env python3
"""Report functions a branch adds that rewrite an existing function under a new name (AES pilot).

The maintainability ratchet (`scripts/maintainability_ratchet.py`) catches copied code; it cannot see
an existing helper written again in different words. This check reads for meaning, with two model
calls through `llm_client` (plain-first: the whole index and the question):

  1. candidates: the index of every function at the merge base (one line each, sent first so the
     provider can cache it) plus the full source of each new function; the model names up to three
     existing functions each new one may duplicate;
  2. judge: each new function with the full source of its named candidates; the model gives
     same_job, partial_overlap or different (split into more calls only when one would pass the input budget).

New functions: module-level functions and class methods in changed `.py` files under the folders,
whose `path::name` is not on the base and whose code is not in the same file on the base under another
name (a function renamed in place, or in a renamed file, is not new; a copy in another file is). `main`, `test_*` and dunder methods are left out; short wrappers stay in, as they are the most
rewritten helpers (AES has 27 git wrappers).
Answers are cached by a hash of model and messages under `<git-common-dir>/helper-reuse/`.

Prints `RESULT helper-reuse new_functions=<n> flagged=<n> cost_usd=<x> exit=<0|1>`; exit 1 when a
function is same_job. A failed model call or tool step prints `RESULT helper-reuse tool-failed exit=2`.
It needs `llm_client` (run with that project's Python); it is report-only and not part of make check.
Traces: `aes/helper-reuse/<head>/candidates` and `.../judge/<n>`, task `aes.helper-reuse`.
Not covered: a rewrite of a function defined inside another function, two new functions that copy each other,
and duplicates across repositories. A base file that does not parse fails the run too.
"""
from __future__ import annotations

import argparse
import ast
import copy as copy_module
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal, TypeVar

from pydantic import BaseModel, Field, field_validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lockstep.ship import git as _git  # noqa: E402  # the path is set just above
PROMPTS = ROOT / "prompts" / "helper_reuse"
MODEL_TASK = os.environ.get("HELPER_REUSE_MODEL", "fast_cheap_mid")  # llm_client task selector or a route
# Input budget per call (both calls): the recorded candidates call on AES (trace aes/helper-reuse/0f882a1f8/candidates,
# 2026-11-24) took 45,739 prompt tokens for 170,364 characters (3.72 characters a token); 60,000 leaves room for the
# index to grow by about 30%. A prompt estimated over it fails (exit 2) instead of being sent.
CHARS_PER_TOKEN = 3.72
INPUT_BUDGET_TOKENS = 60_000
REASONING = os.environ.get("HELPER_REUSE_REASONING", "high")  # llm_client requires it stated


_M = TypeVar("_M", bound=BaseModel)


def _id(text: str) -> str:
    """An id as the prompts define it: the name part cut at its opening bracket (models sometimes copy the arguments).
    Only the part after `::` is cut, so a path holding a bracket keeps it."""
    path, sep, name = text.strip().partition("::")
    return f"{path}{sep}{name.split('(', 1)[0]}".strip()


class _Candidate(BaseModel):
    new_id: str = Field(description="id of the new function, exactly as given")
    existing_ids: list[str] = Field(description="up to three index ids that may do the same job; empty if none")

    @field_validator("new_id")
    @classmethod
    def _bare_new(cls, v: str) -> str:
        return _id(v)

    @field_validator("existing_ids")
    @classmethod
    def _bare_existing(cls, v: list[str]) -> list[str]:
        return [_id(e) for e in v]


class _Candidates(BaseModel):
    items: list[_Candidate]


class _Verdict(BaseModel):
    new_id: str = Field(description="id of the new function, exactly as given")
    verdict: Literal["same_job", "partial_overlap", "different"]
    existing_id: str | None = Field(description="the existing function for same_job or partial_overlap, else null")

    @field_validator("new_id", "existing_id")
    @classmethod
    def _bare(cls, v: str | None) -> str | None:
        return _id(v) if v else v
    reason: str = Field(description="one sentence pointing at the code")


class _Verdicts(BaseModel):
    items: list[_Verdict]


class _Failed(Exception):
    """A step that cannot give a trustworthy answer; main reports it as exit 2."""


def _body_key(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """The function's code with its own name blanked (also where it calls itself or a decorator names it), so a
    function renamed but not changed has the same key."""
    copy = copy_module.deepcopy(node)
    for sub in ast.walk(copy):
        if isinstance(sub, ast.Name) and sub.id == node.name:
            sub.id = ""
        elif isinstance(sub, ast.Attribute) and sub.attr == node.name:
            sub.attr = ""
    copy.name = ""
    return ast.dump(copy)


def _functions(path: str, text: str) -> dict[str, dict[str, Any]]:
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        raise _Failed(f"{path} does not parse: {exc}") from exc  # a skipped file would pass unread
    lines = text.split("\n")  # ast counts lines on newlines only; splitlines also splits on form feeds
    out: dict[str, dict[str, Any]] = {}

    def add(node: ast.FunctionDef | ast.AsyncFunctionDef, owner: str) -> None:
        name = f"{owner}{node.name}"
        start = min([d.lineno for d in node.decorator_list] + [node.lineno])
        source = textwrap.dedent("\n".join(lines[start - 1:node.end_lineno]))
        doc = (ast.get_docstring(node) or "").strip().split("\n")[0]
        out[f"{path}::{name}"] = {"id": f"{path}::{name}", "name": node.name, "source": source,
                                  "body": _body_key(node),
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


def _paths(raw: str) -> list[str]:
    return [p for p in raw.split("\0") if p]


def _base_functions(repo: Path, base: str, folders: list[str]) -> dict[str, dict[str, Any]]:
    paths = [p for p in _paths(_git(repo, "ls-tree", "-r", "-z", "--name-only", base)) if _in_folders(p, folders)]
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


def _changed(repo: Path, base: str, head: str | None) -> tuple[list[str], dict[str, str]]:
    """Changed paths (added, modified, renamed; untracked too when reading the working tree) and new->old renames."""
    status = _git(repo, "diff", "-z", "--name-status", "-M", "--diff-filter=AMRD", base, *([head] if head else []))
    fields, changed, renames, i = _paths(status), [], {}, 0
    while i < len(fields):
        if fields[i].startswith("R"):
            renames[fields[i + 2]] = fields[i + 1]
            changed.append(fields[i + 2])
            i += 3
        else:
            changed.append(fields[i + 1])  # a deleted path reads as absent below
            i += 2
    if head is None:
        changed += _paths(_git(repo, "ls-files", "-z", "--others", "--exclude-standard"))
    return changed, renames


def _moved_out(repo: Path, head: str | None, paths: list[str], renames: dict[str, str], folders: list[str],
               old: dict[str, dict[str, Any]]) -> set[str]:
    """Bodies of base functions whose file changed and that are no longer in that file (or its renamed copy) on the
    branch: code moved out, so the same body appearing in another file is a move, not a rewrite."""
    now_path = {old_path: new_path for new_path, old_path in renames.items()}
    touched = (set(paths) | set(renames.values())) - set(renames)  # base-side paths of every changed file
    base_files = {f["id"].split("::", 1)[0] for f in old.values()}
    gone: set[str] = set()
    for base_path in touched & base_files:
        path = now_path.get(base_path, base_path)
        text = _read(repo, head, path) if _in_folders(path, folders) else None
        now = {f["body"] for f in _functions(path, text).values()} if text is not None else set()
        gone |= {f["body"] for f in old.values() if f["id"].split("::", 1)[0] == base_path} - now
    return gone


def _new_functions(repo: Path, base: str, head: str | None, folders: list[str],
                   old: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Functions on the branch whose id (after file renames) and body (ignoring the name) are not on the base."""
    changed, renames = _changed(repo, base, head)
    moved = _moved_out(repo, head, changed, renames, folders, old)
    bodies_by_file: dict[str, set[str]] = {}
    for f in old.values():
        bodies_by_file.setdefault(f["id"].split("::", 1)[0], set()).add(f["body"])
    new = []
    for p in sorted(set(changed)):
        text = _read(repo, head, p) if _in_folders(p, folders) else None
        if text is None:
            continue
        for fid, f in _functions(p, text).items():
            src = renames.get(p, p)  # a renamed function counts as old only in its own file, never across files
            was = f"{src}::{fid.split('::', 1)[1]}"
            skip = (f["name"] == "main" or f["name"].startswith("test_")
                    or (f["name"].startswith("__") and f["name"].endswith("__")))
            if (not skip and was not in old and f["body"] not in bodies_by_file.get(src, set())
                    and f["body"] not in moved):
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


def _estimated_tokens(messages: list[dict[str, Any]]) -> int:
    return int(sum(len(str(m.get("content", ""))) for m in messages) / CHARS_PER_TOKEN)


def _read_cache(hit: Path, response_model: type[_M]) -> _M | None:
    """A cached answer, or None when there is none or it is damaged (then it is asked again, and said so)."""
    if not hit.is_file():
        return None
    try:
        return response_model.model_validate_json(hit.read_text())
    except ValueError:
        print(f"helper-reuse: damaged cache entry {hit.name}, asking again", file=sys.stderr)
        return None


def _cached_ask(cache: Path, model: str, messages: list[dict[str, str]], response_model: type[_M],
                trace_id: str, check: Callable[[_M], None]) -> tuple[_M, float]:
    """Ask once per distinct (model, reasoning, schema, messages); an answer is cached only after `check` accepts it."""
    if _estimated_tokens(messages) > INPUT_BUDGET_TOKENS:
        raise _Failed(f"{trace_id}: prompt of about {_estimated_tokens(messages)} tokens is over the "
                      f"{INPUT_BUDGET_TOKENS} input budget")
    key = hashlib.sha256(json.dumps([model, REASONING, response_model.model_json_schema(), messages],
                                    sort_keys=True).encode()).hexdigest()
    hit = cache / f"{key}.json"
    cached = _read_cache(hit, response_model)
    if cached is not None:
        check(cached)
        return cached, 0.0
    result, cost = _ask(model, messages, response_model, trace_id)
    check(result)
    cache.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=cache, suffix=".tmp")
    with os.fdopen(fd, "w") as out:
        out.write(result.model_dump_json())
    os.replace(tmp, hit)
    return result, cost


def _check_candidates(new_ids: list[str]) -> Callable[[_Candidates], None]:
    def check(found: _Candidates) -> None:
        got = [c.new_id for c in found.items]
        if sorted(got) != sorted(new_ids):
            raise _Failed(f"candidates answer covers {sorted(got)}, expected each of {sorted(new_ids)} once")
    return check


def _check_verdicts(pairs: list[dict[str, Any]]) -> Callable[[_Verdicts], None]:
    allowed = {p["id"]: {c["id"] for c in p["candidates"]} for p in pairs}

    def check(judged: _Verdicts) -> None:
        got = [v.new_id for v in judged.items]
        if sorted(got) != sorted(allowed):
            raise _Failed(f"judge answer covers {sorted(got)}, expected each of {sorted(allowed)} once")
        for v in judged.items:
            if v.verdict != "different" and v.existing_id not in allowed[v.new_id]:
                raise _Failed(f"judge named {v.existing_id!r} for {v.new_id}, not one of its candidates")
    return check


def _candidates_context(old: dict[str, dict[str, Any]], new: list[dict[str, Any]]) -> dict[str, Any]:
    """The template context for call 1: the base index (sorted, stable) and the new functions."""
    return {"index": "\n".join(f["line"] for _, f in sorted(old.items())),
            "new_functions": [{"id": f["id"], "source": f["source"]} for f in new]}


def _run(repo: Path, base: str, head_rev: str | None, folders: list[str],
         model: str) -> tuple[list[dict[str, Any]], list[_Verdict], float]:
    merge_base = _git(repo, "merge-base", base, head_rev or "HEAD").strip()
    head = _git(repo, "rev-parse", "--short", head_rev or "HEAD").strip()
    old = _base_functions(repo, merge_base, folders)
    new = _new_functions(repo, merge_base, head_rev, folders, old)
    if not new:
        return [], [], 0.0
    cache = Path(_git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir").strip()) / "helper-reuse"
    route = _resolve(model)
    found, cost1 = _cached_ask(cache, route, _render("candidates.yaml", **_candidates_context(old, new)),
                               _Candidates, f"aes/helper-reuse/{head}/candidates",
                               _check_candidates([f["id"] for f in new]))
    # an id the model invented is not in the index and is dropped; repeats are kept once
    by_new = {c.new_id: list(dict.fromkeys(e for e in c.existing_ids if e in old))[:3] for c in found.items}
    pairs = [{"id": f["id"], "source": f["source"],
              "candidates": [{"id": e, "source": old[e]["source"]} for e in by_new[f["id"]]]}
             for f in new if by_new[f["id"]]]
    if not pairs:
        return new, [], cost1
    verdicts, cost = [], cost1
    for n, batch in enumerate(_batches(pairs), 1):
        judged, spent = _cached_ask(cache, route, _render("judge.yaml", pairs=batch), _Verdicts,
                                    f"aes/helper-reuse/{head}/judge/{n}", _check_verdicts(batch))
        verdicts += judged.items
        cost += spent
    return new, verdicts, cost


TAG_CHARS = 120  # the judge template's wrapping tags around each function, counted generously


def _pair_chars(pair: dict[str, Any]) -> int:
    """Characters a pair adds to the rendered judge prompt, its wrapping tags included."""
    return (len(pair["source"]) + len(pair["id"]) + TAG_CHARS
            + sum(len(c["source"]) + len(c["id"]) + len(pair["id"]) + TAG_CHARS for c in pair["candidates"]))


def _batches(pairs: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Judge pairs in as few calls as fit the input budget (usually one); a pair alone over it fails at the call."""
    limit = INPUT_BUDGET_TOKENS * CHARS_PER_TOKEN - len((PROMPTS / "judge.yaml").read_text())
    out: list[list[dict[str, Any]]] = [[]]
    size = 0
    for pair in pairs:
        if out[-1] and size + _pair_chars(pair) > limit:
            out.append([])
            size = 0
        out[-1].append(pair)
        size += _pair_chars(pair)
    return out


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
