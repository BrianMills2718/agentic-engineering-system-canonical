"""The append-only change log: one entry per accepted plan change, never edited afterwards.

`aes plan accept` already writes one record per accepted change, `.aes/plans/<id>.yaml`, opened
for exclusive creation and carrying `accepted_at` and `accepted_at_revision`; `pcw check` refuses
a change that edits or removes one. So the log is those records read in order, not a second store
that could disagree with them. A docstring edit reaches the plan only as an accepted proposal
(behavior 3.6), whose id starts with `DOCSTRING-`, so its entry says it came from a docstring.

`history_problems` checks what a single diff cannot: every commit that touched `.aes/`, oldest
first, plus the uncommitted working tree. A commit that changes the plan without adding a record,
or edits or removes an earlier record, is reported. Merge commits are skipped (`--no-merges`); the
commits they bring in are checked one by one. `entry_edit_reason` stops the edit earlier: the edit
hook (`lockstep.hook`) refuses any write to a record, by an edit tool or the shell, before it happens.

[[[cog import lockstep.cogtext as c; c.docstring("ART-CHANGE-LOG", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-4: A hook copies status from the code up into the normative
  documents: a hook copies status from the code up into the normative
  documents automatically: what exists, test results, and drift. It also
  keeps an automatic append-only change log of every normative change,
  including those made in a docstring, so the history is there.
BEH-4.2: Every normative change, from the plan or from a docstring, gets an
  entry in an append-only change log, written automatically when the change
  is accepted; nobody edits or removes an entry, and the edit hook refuses
  an attempt. The generated change-log page shows, for each entry whose
  rationale ends with an `Agent call: ...` line, that line.
SC-4.2: Each accepted plan change and each docstring-originated change adds
  one log entry, earlier entries are never altered, and the edit hook
  refuses an edit, overwrite or removal of an entry; the generated page
  shows the `Agent call: ...` line of each entry whose rationale ends with
  one.
  Disproved if: A normative change has no entry, an entry was edited or
  removed, or the edit hook lets an edit, overwrite or shell removal of an
  entry through, or the page leaves out the Agent call line of an entry
  whose rationale ends with one.
Proven by: VS-4.2-a (tests/test_change_log.py)
Declares (typed signatures, from the plan):
  entries(root: Path) -> list[dict]
  history_problems(root: Path) -> list[str]
  entry_edit_reason(root: Path, rel: str) -> str | None
  render(log: list[dict]) -> str
  main(argv: list[str] | None = None) -> int
[[[end]]] (sum: 3bMk4EEv9k)
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from agentic_engineering_system.planning import load_plan
from agentic_engineering_system.records import load_project

from lockstep.check import SAFE_GIT

DOCSTRING_PREFIX = "DOCSTRING-"  # the id prefix behavior 3.6 gives a proposal drafted from a docstring

_Change = tuple[str, str]  # (git status letter, path)
_Commit = tuple[str, str, list[_Change]]  # (revision, subject, changes); an alias keeps cog's end marker out


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *SAFE_GIT, "-C", str(root), *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()[:300]}")
    return proc.stdout


def _paths(root: Path) -> tuple[str, str]:
    m = load_project(root / ".aes" / "project.yaml").materialization
    return Path(m.target_path).as_posix(), Path(m.plans_root).as_posix().rstrip("/") + "/"


AGENT_CALL = "Agent call:"  # a rationale that ends with this marker and the call after it carries the agent's own call


def _agent_call(rationale: str) -> str | None:
    """The `Agent call: ...` line a rationale ends with, or None. A folded YAML rationale puts it on one line."""
    start = rationale.rfind(AGENT_CALL)
    if start < 0 or (start and not rationale[start - 1].isspace()):
        return None
    return " ".join(rationale[start:].split())


def entries(root: Path) -> list[dict]:
    """Every accepted plan change, oldest first, as read from its record under the plans folder."""
    _, plans_rel = _paths(root)
    log = []
    for path in sorted((root / plans_rel).glob("*.yaml")):
        plan = load_plan(path)
        delta = plan.target_delta.model_dump(exclude_defaults=True)
        changes = [f"{verb} {family} {item['id'] if isinstance(item, dict) else item}"
                   for verb in ("add", "change", "remove")
                   for family, items in (delta.get(verb) or {}).items() for item in items or []]
        log.append({"id": plan.proposal_id, "title": plan.title, "accepted_at": plan.accepted_at.isoformat(),
                    "revision": plan.accepted_at_revision,
                    "origin": "docstring" if plan.proposal_id.startswith(DOCSTRING_PREFIX) else "plan",
                    "changes": changes, "agent_call": _agent_call(plan.rationale), "record": f"{plans_rel}{path.name}"})
    return sorted(log, key=lambda e: (e["accepted_at"], e["id"]))


def _commits(root: Path) -> list[_Commit]:
    """Each non-merge commit that touched `.aes/`, oldest first, then the working tree as "uncommitted"."""
    out: list[_Commit] = []
    raw = _git(root, "log", "--no-merges", "--reverse", "--no-renames", "--relative", "--name-status",
               "--format=%x00%H%x09%s", "--", ".aes")
    for block in raw.split("\x00")[1:]:
        head, *rest = block.splitlines()
        rev, _, subject = head.partition("\t")
        changes = [(line.split("\t")[0][0], line.split("\t")[-1]) for line in rest if "\t" in line]
        out.append((rev, subject, changes))
    pending = []
    for line in _git(root, "status", "--porcelain", "--no-renames", "-uall", "--", ".aes").splitlines():
        code, rel = line[:2], line[3:]
        pending.append(("A" if code == "??" or "A" in code else "D" if "D" in code else "M", rel))
    if pending:
        out.append(("uncommitted", "the working tree", pending))
    return out


def history_problems(root: Path) -> list[str]:
    """Each commit that changed the plan with no new log entry, or altered an entry already written."""
    target_rel, plans_rel = _paths(root)
    problems = []
    for rev, subject, changes in _commits(root):
        where = "the working tree" if rev == "uncommitted" else f"commit {rev[:12]} ({subject})"
        added = [p for s, p in changes if s == "A" and p.startswith(plans_rel) and p.endswith(".yaml")]
        for status, rel in changes:
            if rel.startswith(plans_rel) and rel.endswith(".yaml") and status != "A":
                verb = "removes" if status == "D" else "edits"
                problems.append(f"{where} {verb} the log entry {rel}; an entry is written once by "
                                "`aes plan accept` and never changed afterwards. Restore it from git.")
            if rel == target_rel and status == "M" and not added:
                problems.append(f"{where} changes the plan ({target_rel}) without adding a log entry under "
                                f"{plans_rel}: make the change a proposal and accept it with `aes plan accept`.")
            if rel == target_rel and status == "D":
                problems.append(f"{where} removes the plan ({target_rel}).")
    return problems


def entry_edit_reason(root: Path, rel: str) -> str | None:
    """Why the edit hook refuses a write to `rel`, or None: the log entries, their folder and `.aes` itself.

    Only `aes plan accept` writes an entry, so a hand-written new one is refused as well as an edit,
    overwrite or removal. Reading an entry is not a write and never reaches this check.
    """
    if not (root / ".aes" / "project.yaml").is_file():  # a layout plan keeps no AES log entries
        return None
    _, plans_rel = _paths(root)
    rel = rel.rstrip("/")
    parents = {p.as_posix() for p in Path(plans_rel).parents if p.as_posix() != "."} | {plans_rel.rstrip("/")}
    if rel not in parents and not rel.startswith(plans_rel):
        return None
    return (f"{rel} is part of the change log ({plans_rel}). Each entry is written once, automatically, by "
            "`aes plan accept`, and is never edited, overwritten or removed, by an agent or a person. To change "
            "the plan, write a new proposal and accept it (`aes plan validate`, then `aes plan accept`); that "
            "adds a new entry. To undo an earlier change, accept a proposal that reverses it.")


# The plan's field names in the words a reader uses (singular, plural); an unknown field keeps its own name.
_NOUNS = {"outcomes": ("requirement", "requirements"), "normative_items": ("behavior", "behaviors"),
          "success_criteria": ("success criterion", "success criteria"), "components": ("component", "components"),
          "planned_artifacts": ("planned file", "planned files"), "verification_subjects": ("test", "tests")}
_PAST = {"add": "added", "change": "changed", "remove": "removed"}


def _and(words: list[str]) -> str:
    return words[0] if len(words) == 1 else f"{', '.join(words[:-1])}{',' if len(words) > 2 else ''} and {words[-1]}"


def _plain(changes: list[str]) -> str:
    """An entry's changes ("add normative_items BEH-4.1", ...) as a phrase: "added behavior BEH-4.1, ..."."""
    groups: dict[str, dict] = {}  # verb -> field -> ids; a nested hint would end in cog's end marker
    for change in changes:
        verb, family, item = change.split(" ", 2)
        groups.setdefault(verb, {}).setdefault(family, []).append(item)
    phrases = []
    for verb, families in groups.items():
        things = []
        for family, ids in families.items():
            one, many = _NOUNS.get(family, (family.replace("_", " "),) * 2)
            things.append(f"{one if len(ids) == 1 else many} {_and(ids)}")
        phrases.append(f"{_PAST.get(verb, verb)} {_and(things)}")
    return "; ".join(phrases) or "changed nothing"


def render(log: list[dict]) -> str:
    """The change-log wiki page: every entry, newest first."""
    lines = ["# Change log", "",
             f"Every accepted change to the plan, newest first ({len(log)} entries). Each entry is the record "
             "`aes plan accept` wrote under the plans folder; it is written once and never edited, and "
             "`python -m lockstep.change_log` checks the whole history for a change with no entry.", ""]
    for e in reversed(log):
        origin = "from a docstring" if e["origin"] == "docstring" else "from the plan"
        lines += [f"- **{e['accepted_at'][:10]}** `{e['id']}` ({origin}, accepted at `{e['revision'][:12]}`): "
                  f"{e['title']}. It {_plain(e['changes'])}."]
        if e.get("agent_call"):
            lines += [f"  - {e['agent_call']}"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.change_log [--root .]`: check the change log is complete and unaltered; exit 1 if not."""
    ap = argparse.ArgumentParser(prog="python -m lockstep.change_log", description=main.__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    args = ap.parse_args(argv)
    root = args.root.resolve()
    problems = history_problems(root)
    for p in problems:
        print(p)
    print(f"change_log: entries={len(entries(root))} commits={len(_commits(root))} problems={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
