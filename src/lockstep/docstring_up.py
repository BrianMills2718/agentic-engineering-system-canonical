"""Turn an edit to a docstring's plan text into a draft plan change, which the coding agent accepts.

The plan copy in a docstring is cog output, and cog records a checksum of what it last wrote on the
block's end line. That checksum tells the two kinds of difference apart:

- the text still matches its checksum: nobody edited it, the plan has moved on, and `make project`
  simply regenerates it;
- the text no longer matches its checksum, and the checksum is that of the current plan's copy: a
  person or agent edited a current copy. The edit is read back into the plan items it was copied
  from, written as a proposal under `plans/` named `DOCSTRING-<artifact>-<time>` (so the change log
  shows it came from a docstring), and the copy is put back to the current plan. The plan is
  unchanged until the draft is accepted with `aes plan accept`, which also writes its change-log
  entry; `make project` then copies the accepted text back down. The coding agent accepts the draft
  itself when it is confident in it or the change is not significant, and otherwise leaves it and
  asks a person (Brian, 2026-11-07; the second half is an agent's working default).

Anything else is reported and the file is left alone: an edit to a copy that was written from an
earlier plan (which lines are the edit cannot be told), a block with no checksum, or an edit that
adds, removes or renames an item or changes a "Proven by" line (change the plan by a proposal).

[[[cog import lockstep.cogtext as c; c.docstring("ART-DOCSTRING-UP", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-3: A hook copies the normative text and typed signatures down
  into the code: a hook copies the full normative text, and the typed
  signatures, from the plan down into the code's docstrings automatically;
  nobody types the copy. For normative text the projection is two-way: the
  normative portion of a docstring can be edited where the agent is working,
  and the edit projects up into the plan; and when the normative text
  changes in the plan, every linked function, wherever it is, is marked for
  update and the agent is handed that list.
BEH-3.6: An edit to the normative part of a docstring becomes a draft plan
  change; the coding agent accepts it itself when it is confident in it or
  it is not significant, and otherwise leaves the draft and asks a person.
SC-3.6: An edit to a docstring's plan text produces a draft proposal
  carrying the edit, and the plan is unchanged until it is accepted.
  Disproved if: A docstring's normative edit is lost when the copy is
  regenerated, or reaches the plan without being accepted (accepting is what
  writes its change-log entry).
Proven by: VS-3.6-a (tests/test_docstring_up.py)
Declares (typed signatures, from the plan):
  draft_from_docstring(root: Path, rel: str, out_dir: Path) -> tuple[list[Path], list[str]]
  main(argv: list[str] | None = None) -> int
[[[end]]] (sum: tLRt2SilUm)
"""

from __future__ import annotations

import argparse
import copy
from datetime import UTC, datetime
from pathlib import Path

import yaml
from agentic_engineering_system.planning import PlanError, Proposal, validate_proposal
from cogapp.hashhandler import HashHandler

from lockstep.aes_bridge import context, target
from lockstep.change_log import DOCSTRING_PREFIX
from lockstep.check import COG_CALL
from lockstep.cogtext import END, OPEN, render

DECLARES = "Declares (typed signatures, from the plan):"
FAMILIES = ("outcomes", "normative_items", "success_criteria", "planned_artifacts")
_Key = tuple[str, str, str]  # (plan family, item id, field); an alias keeps cog's end marker out of this file


def _unwrap(text: str, more: str) -> str:
    """Join a continuation line the way textwrap split it: no space after a word broken at its hyphen."""
    if len(text) > 1 and text.endswith("-") and text[-2].isalnum():
        return text + more
    return f"{text} {more}"


def _items(lines: list[str], ids: dict[str, str]) -> dict:
    """{(family, id, field): text} read back from a rendered copy; exports under ("exports", "", "")."""
    out: dict = {}
    cur: _Key | None = None
    last_sc = None
    for n, line in enumerate(lines, start=1):
        if line.startswith("Part of ") and ": " in line:
            oid, _, text = line[len("Part of "):].partition(": ")
            cur = ("outcomes", oid, "statement")
            out[cur] = text
        elif line.startswith("Proven by: "):
            cur = None
            out[("proven", line, "")] = ""
        elif line == DECLARES:
            cur = ("exports", "", "")
            out[cur] = []
        elif line.startswith("  Disproved if: ") and last_sc:
            cur = ("success_criteria", last_sc, "disproof")
            out[cur] = line[len("  Disproved if: "):]
        elif line.startswith("  ") and cur is not None:
            out[cur] = out[cur] + [line.strip()] if cur[0] == "exports" else _unwrap(out[cur], line.strip())
        elif line.partition(": ")[0] in ids and ": " in line:
            iid, _, text = line.partition(": ")
            cur = (ids[iid], iid, "statement")
            out[cur] = text
            last_sc = iid if ids[iid] == "success_criteria" else last_sc
        else:
            raise ValueError(f"line {n} of the copy ({line.strip()[:60]!r}) is not plan text Lockstep can read back")
    return out


def _same(a: object, b: object) -> bool:
    return (a == b) if isinstance(a, list) else " ".join(str(a).split()) == " ".join(str(b).split())


def _blocks(lines: list[str]) -> list[tuple[int, int, str, int]]:
    """(spec line, end line, artifact id, indent) for each standard plan-copy block."""
    found = []
    for i, line in enumerate(lines):
        m = COG_CALL.fullmatch(line.rstrip("\n")) if OPEN in line else None
        end = next((k for k in range(i + 1, len(lines)) if END in lines[k]), None) if m else None
        if m and end is not None:
            found.append((i, end, m["id"], int(m["indent"] or 4)))
    return found


def _proposal(root: Path, rel: str, art_id: str, edits: dict, out_dir: Path) -> tuple[dict, str]:
    tgt = target(root)
    by_id = {fam: {x["id"]: x for x in tgt.get(fam) or []} for fam in FAMILIES}
    changed: dict = {}
    for (fam, iid, field), value in edits.items():
        if fam == "exports":
            fam, iid, field = "planned_artifacts", art_id, "exports"
        entry = changed.setdefault((fam, iid), copy.deepcopy(by_id[fam][iid]))
        entry[field] = value if isinstance(value, list) else " ".join(value.split())
    pid = f"{DOCSTRING_PREFIX}{art_id}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%S')}"
    names = ", ".join(sorted({iid for _, iid in changed}))
    draft_rel = (out_dir / f"{pid}.yaml").relative_to(root) if out_dir.is_relative_to(root) else out_dir / f"{pid}.yaml"
    delta: dict = {}
    for (fam, _), entry in changed.items():
        delta.setdefault(fam, []).append(entry)
    return {"schema_version": "aes.v0_2.proposal.probe0", "proposal_id": pid,
            "title": f"Edit to the plan text copied into {rel}: {names}",
            "rationale": (f"Drafted by `python -m lockstep.docstring_up` from an edit to the plan text in the docstring of "
                          f"{rel} ({art_id}). The plan is unchanged until this draft is accepted with "
                          f"`aes plan accept {draft_rel}`: the coding agent accepts it when it is confident in "
                          "it or the change is not significant, and otherwise leaves it for a person."),
            "closes_gaps": [],
            "trace_review": {"runs_traced_work": False,
                             "reason": "a change to plan text drafted from a docstring; no model, agent or pipeline runs."},
            "target_delta": {"change": delta}}, pid


def draft_from_docstring(root: Path, rel: str, out_dir: Path) -> tuple[list[Path], list[str]]:
    """(drafts written, problems) for the plan-copy blocks in one file; a drafted block is put back to the plan."""
    path = root / rel
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    tgt = target(root)
    ids = {x["id"]: fam for fam in FAMILIES[:3] for x in tgt.get(fam) or []}
    hashes = HashHandler(END)
    drafts: list[Path] = []
    problems: list[str] = []
    for start, end, art_id, indent in reversed(_blocks(lines)):
        pad = " " * indent
        plan_lines = [(pad + line).rstrip() + "\n" for line in render(context(root, art_id))]
        copy_lines = lines[start + 1:end]
        kind, recorded = hashes.extract_hash_from_line(lines[end])
        if copy_lines == plan_lines or (kind is None and not copy_lines):
            continue  # current, or a new block cog has not filled yet
        where = f"{rel} (the copy of {art_id}, lines {start + 2} to {end})"
        if kind is None:
            problems.append(f"{where} differs from the plan and has no cog checksum, so an edit cannot be told from "
                            "a newer plan: run cog with -c (`make project`), which records one.")
            continue
        as_recorded = hashes.hex_to_base64_hash if kind == "base64" else (lambda h: h)
        if recorded == as_recorded(hashes.compute_lines_hash(copy_lines)):
            continue  # untouched since cog wrote it: the plan moved on, and `make project` regenerates it
        if recorded != as_recorded(hashes.compute_lines_hash(plan_lines)):
            problems.append(f"{where} was edited, but it was copied from an earlier plan, so which lines are the edit "
                            "cannot be told. Keep your edit elsewhere, run `make project`, and redo the edit there.")
            continue
        try:
            if copy_lines[:2] != plan_lines[:2]:
                raise ValueError("its first line, which says where the copy comes from, was changed")
            mine = _items([line[len(pad):].rstrip("\n") for line in copy_lines[2:]], ids)
            plan = _items([line[len(pad):].rstrip("\n") for line in plan_lines[2:]], ids)
            if set(mine) != set(plan):
                raise ValueError("it adds, removes or renames a plan item or changes a 'Proven by' line")
        except ValueError as exc:
            problems.append(f"{where} was edited, but the edit cannot become a plan change: {exc}. "
                            "Change the plan through a proposal (`aes plan prepare/validate/accept`).")
            continue
        edits = {k: v for k, v in mine.items() if not _same(v, plan[k])}
        if not edits:
            lines[start + 1:end + 1] = [*plan_lines, hashes.format_end_line_with_hash(
                lines[end], hashes.compute_lines_hash(plan_lines), preserve_format=True)]
            continue  # only line breaks or spacing changed: put the copy back, nothing to propose
        doc, pid = _proposal(root, rel, art_id, edits, out_dir)
        try:
            validate_proposal(root, Proposal.model_validate(doc))
        except (PlanError, ValueError) as exc:
            problems.append(f"{where} was edited, but the draft does not validate: {str(exc).splitlines()[0]}")
            continue
        out_dir.mkdir(parents=True, exist_ok=True)
        draft = out_dir / f"{pid}.yaml"
        with draft.open("x", encoding="utf-8") as fh:
            yaml.safe_dump(doc, fh, sort_keys=False, allow_unicode=True, width=100)
        drafts.append(draft)
        lines[start + 1:end + 1] = [*plan_lines, hashes.format_end_line_with_hash(
            lines[end], hashes.compute_lines_hash(plan_lines), preserve_format=True)]
    text = "".join(lines)
    if text != path.read_text(encoding="utf-8"):
        path.write_text(text, encoding="utf-8")
    return list(reversed(drafts)), problems


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.docstring_up [--root .] [--out plans]`: draft a plan change from each edited copy; exit 1 on a problem."""
    ap = argparse.ArgumentParser(prog="python -m lockstep.docstring_up", description=main.__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--out", type=Path, default=Path("plans"))
    args = ap.parse_args(argv)
    root = args.root.resolve()
    out_dir = args.out if args.out.is_absolute() else root / args.out
    files = drafts = 0
    problems: list[str] = []
    for art in target(root).get("planned_artifacts") or []:
        rel = (art.get("locator") or {}).get("exact_path") or ""
        if not rel.endswith(".py") or not (root / rel).is_file() or OPEN not in (root / rel).read_text(encoding="utf-8"):
            continue
        files += 1
        written, found = draft_from_docstring(root, rel, out_dir)
        for d in written:
            shown = d.relative_to(root) if d.is_relative_to(root) else d
            print(f"drafted {shown} from the edit to {rel}; the plan is unchanged until it is accepted: "
                  f"run `aes plan accept {shown}` when you are confident in it or it is not significant, "
                  "otherwise leave it as a draft and ask a person, saying why")
        drafts += len(written)
        problems += found
    for p in problems:
        print(p)
    print(f"docstring_up: files={files} drafts={drafts} problems={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
