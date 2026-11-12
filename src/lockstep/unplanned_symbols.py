"""Report a top-level function or class the plan does not declare with its types (behavior 1.2).

For each planned source file written in Python, two things are reported:
  - a public top-level function or class (its name does not start with `_`) that the file's
    `exports` in the plan do not name;
  - a function the plan declares without its types: a bare name for what the code defines as a
    function, or a declared signature with a parameter or the return left unannotated.
A file's public symbols are read the way AES reads them (`characterize_python.analyze`, from the
working tree, never imported or run). A declared export the code lacks, or whose signature changed,
is behavior 5.3's report (`lockstep.plan_to_code`), not this one. `python -m lockstep.unplanned_symbols` is
part of `make check`.

[[[cog import lockstep.cogtext as c; c.docstring("ART-UNPLANNED-SYMBOLS", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-1: The plan declares the normative side and the whole file
  structure: the plan, written as structured YAML in the AES plan format,
  declares the normative side (requirements, success criteria and decisions)
  and declares every file and every strongly typed function and class; no
  code file, test or document exists without a declared reason.
BEH-1.2: Any top-level function or class in a planned source file that the
  plan does not declare in that file's exports, with its parameter and
  return types, is reported.
SC-1.2: An undeclared top-level function or class, or an export without
  types, is reported; declared typed symbols are not.
  Disproved if: A top-level function or class is missing from its file's
  exports, or is exported without types, and nothing reports it.
Proven by: VS-1.2-a (tests/test_unplanned_symbols.py)
Declares (typed signatures, from the plan):
  symbol_problems(root: Path, plan: dict) -> list[str]
  main(argv: list[str] | None = None) -> int
[[[end]]] (sum: S/hQ+kJlRj)
"""

from __future__ import annotations

import argparse
import ast
from typing import cast
import sys
from pathlib import Path

from agentic_engineering_system.characterize_python import analyze, parse_export

from lockstep.aes_bridge import find_root, target


def _untyped(entry: str) -> list[str]:
    """What a declared signature leaves without a type: parameter names, and `return`."""
    fn = cast(ast.FunctionDef, ast.parse(f"def {entry.strip()}:\n    pass\n").body[0])
    a = fn.args
    params = a.posonlyargs + a.args + a.kwonlyargs + [p for p in (a.vararg, a.kwarg) if p]
    return [p.arg for p in params if p.annotation is None] + (["return"] if fn.returns is None else [])


_Planned = tuple[str, str, list[str]]  # an alias: cog reads three closing brackets as its end marker


def _source_files(plan: dict) -> list[_Planned]:
    """(artifact id, path, declared exports) for each planned Python source file."""
    out = []
    for art in plan.get("planned_artifacts") or []:
        path = (art.get("locator") or {}).get("exact_path") or ""
        if art.get("kind") == "source" and path.endswith(".py"):
            out.append((art.get("id"), path, [str(e) for e in art.get("exports") or []]))
    return out


def symbol_problems(root: Path, plan: dict) -> list[str]:
    """One plain-words problem per undeclared public function or class, and per untyped declared function."""
    problems: list[str] = []
    for art, path, exports in _source_files(plan):
        declared: dict[str, str] = {}
        for entry in exports:
            try:
                name, signature = parse_export(entry)
            except ValueError as exc:
                problems.append(f"{art} ({path}): {exc}.")
                continue
            declared[name] = entry
            if signature is not None and _untyped(entry):
                problems.append(f"{art} ({path}) declares {entry!r} without types for "
                                f"{', '.join(_untyped(entry))}: give every parameter and the return a type.")
        file = root / path
        if not file.is_file():
            continue
        for sym in analyze(path, file.read_text(encoding="utf-8"), {}).symbols:
            if sym.kind not in ("function", "class"):
                continue
            if sym.name not in declared:
                shown = f"{sym.name}{sym.signature}" if sym.signature else sym.name
                problems.append(f"{path} defines the {sym.kind} {shown}, which the plan does not declare: add it "
                                f"to {art}'s exports with its types, through `aes plan prepare/validate/accept`, "
                                "or make it private (a name starting with _).")
            elif sym.kind == "function" and "(" not in declared[sym.name]:
                problems.append(f"{art} ({path}) declares the function {sym.name} by name only: declare it with its "
                                f"types, as {sym.name}{sym.signature}.")
    return problems


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.unplanned_symbols [--root DIR]`: print each problem; exit 1 if there is any."""
    ap = argparse.ArgumentParser(prog="lockstep.unplanned_symbols", description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    args = ap.parse_args(argv)
    root = find_root(args.root)
    if root is None:
        print(f"no .aes/project.yaml at or above {args.root}", file=sys.stderr)
        return 2
    plan = target(root)
    problems = symbol_problems(root, plan)
    for p in problems:
        print(p)
    files = _source_files(plan)
    print(f"unplanned_symbols: files={len(files)} written={sum((root / p).is_file() for _, p, _ in files)} "
          f"problems={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
