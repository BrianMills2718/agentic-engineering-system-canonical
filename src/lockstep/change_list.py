"""After a plan change, list every file and symbol whose plan text changed, as one list for the agent.

"Linked" uses AES's own inclusion rule for `aes context <artifact>` (the pinned
`agentic_engineering_system.context._closure`), the same rule that builds each docstring
copy, so the list names exactly the files whose copy carries a changed item. The hook adds
the list to its refusal when an edit meets a stale copy (behavior 3.4), so the agent gets all
the files at once instead of one refusal per file. `make project` refreshes the docstrings;
the code under them is the agent's to review.

[[[cog import lockstep.cogtext as c; c.docstring("ART-CHANGE-LIST", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-3: A hook copies the normative text and typed signatures down
  into the code: a hook copies the full normative text, and the typed
  signatures, from the plan down into the code's docstrings automatically;
  nobody types the copy. For normative text the projection is two-way: the
  normative portion of a docstring can be edited where the agent is working,
  and the edit projects up into the plan; and when the normative text
  changes in the plan, every linked function, wherever it is, is marked for
  update and the agent is handed that list.
BEH-3.5: When the plan's normative text changes, every file and symbol
  linked to the changed items is listed and handed to the agent as one list.
SC-3.5: After a plan change, the agent receives a list naming every file and
  symbol linked to each changed item.
  Disproved if: A file or symbol linked to a changed item is missing from
  the list, or the list never reaches the agent.
Proven by: VS-3.5-a (tests/test_change_list.py)
Declares (typed signatures, from the plan):
  changed_items(old: dict, new: dict) -> list[str]
  linked_files(old: dict, new: dict, changed: list[str]) -> list[dict]
  plan_base(root: Path) -> str | None
  change_list(root: Path, base: str | None = None) -> dict
  render(listing: dict) -> str
  main(argv: list[str] | None = None) -> int
[[[end]]] (sum: TOIyyhHK1G)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml
from agentic_engineering_system.context import _closure
from agentic_engineering_system.records import parse_target

from lockstep.aes_bridge import find_root

TARGET = ".aes/target.yaml"
NORMATIVE = ("outcomes", "normative_items", "success_criteria", "verification_subjects")


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def changed_items(old: dict, new: dict) -> list[str]:
    """IDs of requirements, behaviors, criteria (with their evidence requirements) and test routes
    that were added, removed or reworded between two plans, in plan order."""
    ids: list[str] = []
    for family in NORMATIVE:
        before = {x["id"]: x for x in old.get(family) or []}
        after = {x["id"]: x for x in new.get(family) or []}
        for rid in [*after, *(k for k in before if k not in after)]:
            if before.get(rid) != after.get(rid):
                ids.append(rid)
    return ids


def linked_files(old: dict, new: dict, changed: list[str]) -> list[dict]:
    """Each planned file whose docstring context, in the new plan or the old one, holds a changed
    item: its path, artifact ID, the changed items it carries and its declared symbols."""
    wanted = set(changed)
    hits: dict[str, set[str]] = {}
    planned: dict[str, dict] = {}
    for plan in (old, new):  # new last, so a file still planned shows its path and symbols as planned now
        if not plan:
            continue
        record = parse_target(plan, Path(TARGET))
        for art in plan.get("planned_artifacts") or []:
            planned[art["id"]] = art
            got = wanted & set().union(*_closure(record, "planned_artifacts", art["id"]).values())
            if got:
                hits.setdefault(art["id"], set()).update(got)
    entries = [{"artifact": aid, "path": planned[aid]["locator"]["exact_path"],
                "items": [i for i in changed if i in got], "symbols": list(planned[aid].get("exports") or [])}
               for aid, got in hits.items()]
    return sorted(entries, key=lambda e: e["path"])


def plan_base(root: Path) -> str | None:
    """The commit holding the plan before its latest change: HEAD while the plan has uncommitted
    edits, else the parent of the last commit that changed the plan; None if there was no plan before."""
    if _git(root, "rev-parse", "--verify", "-q", "HEAD").returncode != 0:
        return None
    if _git(root, "diff", "--quiet", "HEAD", "--", TARGET).returncode != 0:
        return "HEAD"
    last = _git(root, "log", "-1", "--format=%H", "--", TARGET).stdout.strip()
    parent = _git(root, "rev-parse", "--verify", "-q", f"{last}^").stdout.strip() if last else ""
    return parent or None


def change_list(root: Path, base: str | None = None) -> dict:
    """{"base", "changed", "files"} for the plan in the working tree against the plan at `base`
    (default: `plan_base(root)`)."""
    base = plan_base(root) if base is None else base
    old: dict = {}
    if base:
        shown = _git(root, "show", f"{base}:{TARGET}")
        if shown.returncode == 0:
            old = yaml.safe_load(shown.stdout) or {}
    new = yaml.safe_load((root / TARGET).read_text(encoding="utf-8"))
    changed = changed_items(old, new)
    return {"base": base, "changed": changed, "files": linked_files(old, new, changed)}


def render(listing: dict) -> str:
    """The list as the agent reads it."""
    since = f"commit {listing['base'][:12]}" if listing["base"] else "the start of the plan"
    if not listing["changed"]:
        return f"No plan text changed since {since}."
    lines = [f"Plan text changed since {since}: {', '.join(listing['changed'])}.",
             f"These {len(listing['files'])} file(s) carry that text. Run `make project` once to refresh every "
             "docstring, then check each file's code against the new text:"]
    for f in listing["files"]:
        symbols = f"; symbols: {', '.join(f['symbols'])}" if f["symbols"] else ""
        lines.append(f"- {f['path']} ({f['artifact']}): {', '.join(f['items'])}{symbols}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.change_list [--root DIR] [--base REF] [--json]`: print the list."""
    ap = argparse.ArgumentParser(prog="lockstep.change_list", description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--base", help="git revision holding the earlier plan (default: before the latest plan change)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    root = find_root(args.root)
    if root is None:
        print(f"no .aes/project.yaml at or above {args.root}", file=sys.stderr)
        return 2
    listing = change_list(root, args.base)
    print(json.dumps(listing, indent=2) if args.json else render(listing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
