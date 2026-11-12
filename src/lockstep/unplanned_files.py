"""Report a file the plan does not declare (behavior 1.1).

The one rule both checks use: the edit hook at edit time (behavior 5.1, `lockstep.hook`)
and the whole-tree check before commit (behavior 5.2, `lockstep.check`). Code and tests under a
governed folder are declared in the AES plan; documents (files matching `documents.include`)
are declared in Lockstep's side file, `lockstep.yaml` (`lockstep.side_file`). A project with no side
file has no document rule. `python -m lockstep.unplanned_files` reports every document at once and
fails on an undeclared one or a problem in the side file; it is part of `make check`.

[[[cog import lockstep.cogtext as c; c.docstring("ART-UNPLANNED-FILES", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-1: The plan declares the normative side and the whole file
  structure: the plan, written as structured YAML in the AES plan format,
  declares the normative side (requirements, success criteria and decisions)
  and declares every file and every strongly typed function and class; no
  code file, test or document exists without a declared reason.
BEH-1.1: Any file in the project that the plan does not declare is reported,
  with why it counts: code and tests under a governed folder through the AES
  plan, documents through Lockstep's side file beside the plan, and, when
  the side file has a files section, every other tracked file through that
  section.
SC-1.1: An undeclared file under a governed folder is reported; a declared
  file, a legacy file and a file outside every governed folder are not,
  unless the side file has a files section, when an undeclared tracked file
  outside the governed folders is reported; an undeclared document is
  reported.
  Disproved if: An undeclared code file, test or document passes without a
  report, a tracked file declared nowhere passes when the side file has a
  files section, or a declared, legacy or (without a files section)
  ungoverned file is reported.
Proven by: VS-1.1-a (tests/test_unplanned_files.py)
Proven by: VS-1.1-b (tests/test_unplanned_documents.py)
Proven by: VS-1.1-c (tests/test_unplanned_other_files.py)
Declares (typed signatures, from the plan):
  governing_folder(root: Path, rel: str) -> str
  declared_file(side: SideFile, rel: str) -> str | None
  unplanned_reason(root: Path, rel: str, base: str | None = None) -> str | None
  document_report(root: Path) -> dict
  main(argv: list[str] | None = None) -> int
[[[end]]] (sum: 9r1rl/pbTN)
"""

from __future__ import annotations

import argparse
import subprocess
import fnmatch
import sys
from pathlib import Path, PurePosixPath

from lockstep.aes_bridge import artifact_for_path, find_root, governed_roots, is_governed, legacy_files, target
from lockstep.layout_plan import has_layout
from lockstep.side_file import SIDE_FILE, SideFile, load_side_file, side_file_problems


def governing_folder(root: Path, rel: str) -> str:
    """The governed root `rel` sits under, or an empty string."""
    return next((g for g in governed_roots(root) if rel.startswith(g)), "")


def _document_pattern(side: SideFile, rel: str) -> str | None:
    return next((g for g in side.include if PurePosixPath(rel).match(g)), None)


def declared_file(side: SideFile, rel: str) -> str | None:
    """The `files` entry in the side file (a path or a glob, `fnmatch` on the whole path) declaring `rel`, or None."""
    if rel in side.files:
        return rel
    return next((g for g in side.files if fnmatch.fnmatchcase(rel, g)), None)


def unplanned_reason(root: Path, rel: str, base: str | None = None) -> str | None:
    """Why `rel` is a file the plan does not declare, with how to declare it; or None.

    None when the plan or the side file declares the file, when it is a legacy file (`aes adopt`),
    or when it is neither under a governed folder nor a document the side file's include matches.
    While the side file cannot be read, every file outside the governed folders is refused except
    the side file itself, so a broken side file cannot let a document through. With `base`, the side
    file and the legacy list are read as committed at that revision (`pcw check`, issue #67).
    """
    if artifact_for_path(root, rel) is not None:
        return None
    try:
        side, unreadable = load_side_file(root, base), ""
    except ValueError as exc:
        side, unreadable = None, str(exc)
    if side is not None and rel in side.documents:
        return None
    governed = is_governed(root, rel, base)
    if unreadable and rel != SIDE_FILE and not governed:
        return f"{rel} cannot be checked against the side file: {unreadable}. Fix {SIDE_FILE} first."
    if governed:
        if has_layout(root):
            return (f"{rel} is not in the plan: it is under the governed folder {governing_folder(root, rel)}, "
                    f"and no `layout:` row in {SIDE_FILE} names it. Add a row for it (path, purpose, the OpenSpec "
                    "requirements it implements, its tests) and have the plan approved first.")
        return (f"{rel} is not in the plan: it is under the governed folder {governing_folder(root, rel)}, "
                "and .aes/target.yaml does not name it. Add it to .aes/target.yaml through "
                "`aes plan prepare/validate/accept` first.")
    pattern = _document_pattern(side, rel) if side is not None else None
    if pattern is None:
        if side is None or not side.whole_repo or declared_file(side, rel) is not None:
            return None
        return (f"{rel} is not declared: the side file {SIDE_FILE} has a files section, so every file outside "
                "the governed folders must be declared there or as a document. Add it under files in "
                f"{SIDE_FILE}, with a purpose and the plan items it serves (refs), first.")
    return (f"{rel} is not in the plan: it is a document (it matches {pattern} in {SIDE_FILE}), and "
            f"{SIDE_FILE} does not declare it. Add it under documents.declared in {SIDE_FILE}, with a "
            "purpose and the plan items it serves (refs), first.")


def allowed_listing(root: Path, rel: str, cap: int = 15) -> str:
    """Plain text listing the files the plan does allow, for a refusal of `rel`; the same governed folder first.

    Reads whichever plan is in use (`lockstep.yaml` `layout:` rows or the planned artifacts of
    `.aes/target.yaml`). At most `cap` paths are shown, then "and N more". An empty string when the
    plan names no file.
    """
    paths = sorted({(a.get("locator") or {}).get("exact_path") or "" for a in target(root).get("planned_artifacts") or []} - {""})
    folder = rel.rsplit("/", 1)[0] + "/" if "/" in rel else ""
    paths.sort(key=lambda p: (not p.startswith(folder), p))  # stable: same folder first, each group alphabetical
    if not paths:
        return ""
    lines = ["The plan does allow these files:", *[f"  {p}" for p in paths[:cap]]]
    if len(paths) > cap:
        lines.append(f"  and {len(paths) - cap} more")
    return "\n".join(lines)


def _project_files(root: Path) -> list[str]:
    listed = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"],
                            capture_output=True, text=True, check=True).stdout.splitlines()
    return sorted({p for p in listed if (root / p).is_file()})


def document_report(root: Path) -> dict:
    """Every document against the side file: declared, undeclared, unbuilt, and the file's problems.

    A document is a tracked or new (not ignored) file matching `documents.include` that the AES
    plan does not already declare. `undeclared` holds one plain line per document the side file
    misses; `unbuilt` lists declared paths with no file yet (reported, not failing).
    """
    side = load_side_file(root)
    if side is None:
        return {"side_file": False, "declared": [], "undeclared": [], "unbuilt": [], "problems": [],
                "files": [], "undeclared_files": [], "unused_globs": []}
    planned = {(a.get("locator") or {}).get("exact_path") for a in target(root).get("planned_artifacts") or []}
    roots, legacy = governed_roots(root), legacy_files(root)
    files = _project_files(root)
    documents = [p for p in files if _document_pattern(side, p) is not None and p not in planned]
    undeclared = [reason for p in documents if (reason := unplanned_reason(root, p)) is not None]
    others = [p for p in files if side.whole_repo and _document_pattern(side, p) is None and p not in planned
              and not (any(p.startswith(g) for g in roots) and p not in legacy)]
    return {"side_file": True,
            "files": [p for p in others if declared_file(side, p) is not None],
            "undeclared_files": [r for p in others if declared_file(side, p) is None
                                 and (r := unplanned_reason(root, p)) is not None],
            "unused_globs": sorted(g for g in side.files if not any(fnmatch.fnmatchcase(p, g) for p in others)),
            "declared": [p for p in documents if p in side.documents],
            "undeclared": undeclared,
            "unbuilt": sorted(p for p in side.documents if not (root / p).is_file()),
            "problems": side_file_problems(root, target(root))}


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.unplanned_files [--root DIR]`: print each problem; exit 1 if any fails."""
    ap = argparse.ArgumentParser(prog="lockstep.unplanned_files", description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    args = ap.parse_args(argv)
    root = find_root(args.root)
    if root is None:
        print(f"no .aes/project.yaml at or above {args.root}", file=sys.stderr)
        return 2
    try:
        r = document_report(root)
    except ValueError as exc:
        print(exc)
        print("unplanned_files: side_file=unreadable")
        return 1
    if not r["side_file"]:
        print(f"unplanned_files: side_file=absent ({SIDE_FILE} not found; no document rule)")
        return 0
    for line in [*r["problems"], *r["undeclared"], *r["undeclared_files"]]:
        print(line)
    for glob in r["unused_globs"]:
        print(f"{SIDE_FILE}: files entry {glob} matches no file; remove it or fix its path.")
    for path in r["unbuilt"]:
        print(f"  {path} is declared in {SIDE_FILE}, not written yet.")
    print(f"unplanned_files: documents={len(r['declared']) + len(r['undeclared'])} declared={len(r['declared'])} "
          f"undeclared={len(r['undeclared'])} unbuilt={len(r['unbuilt'])} problems={len(r['problems'])} "
          f"other_files={len(r['files']) + len(r['undeclared_files'])} undeclared_files={len(r['undeclared_files'])} "
          f"unused_globs={len(r['unused_globs'])}")
    return 1 if r["problems"] or r["undeclared"] or r["undeclared_files"] or r["unused_globs"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
