"""Status that comes up from the code, and one page per requirement: its text, its status and its change log.

[[[cog import lockstep.cogtext as c; c.docstring("ART-REQUIREMENT-STATUS", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-4: A hook copies status from the code up into the normative
  documents: a hook copies status from the code up into the normative
  documents automatically: what exists, test results, and drift. It also
  keeps an automatic append-only change log of every normative change,
  including those made in a docstring, so the history is there.
BEH-4.1: Each requirement has one page, rendered from the plan and the code,
  none of it typed; its text first, then its status (what exists, each
  criterion's test result with the commit and time it was produced, and the
  drift between plan and code), then the change-log entries that touch it; a
  committed page that no longer matches a fresh build is caught before it is
  pushed or merged.
SC-4.1: The wiki has one page per requirement showing, in order, its text; a
  status block with each behavior's files, each criterion's standing with
  the commit and time of the test result behind it, and any drift AES
  reports; and the change-log entries that touch the requirement, newest
  last. A written page that differs from a fresh build is reported.
  Disproved if: A page shows a status someone typed; misses a file, test
  result, drift or change-log entry the code and plan have; shows a test
  result without its commit and time; or a written page that differs from a
  fresh build passes the check.
Proven by: VS-4.1-a (tests/test_requirement_status.py)
Declares (typed signatures, from the plan):
  requirement_status(root: Path) -> dict
  record_stale_evidence(root: Path) -> list[str]
  requirement_pages(root: Path, status: dict | None = None) -> dict[str, str]
  write_pages(root: Path, out_dir: Path) -> list[str]
  stale_pages(root: Path, out_dir: Path) -> list[str]
  main(argv: list[str] | None = None) -> int
[[[end]]] (sum: mRTdjm4VAf)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml
from agentic_engineering_system.characterize import check as characterize_check
from agentic_engineering_system.evidence import record

from lockstep.aes_bridge import find_root, run_aes, target
from lockstep.change_log import _plain, entries, render

BUILT = "Built from commit"  # starts the one line of a page a rebuild may change; stale_pages skips it


def _reconcile(root: Path) -> dict:
    proc = run_aes(root, "reconcile", "--json")
    # Exit 1 means drift or a refuted criterion, which is what the page must show: the JSON is
    # still complete. Anything else, or no JSON, means reconcile itself did not run.
    if proc.returncode not in (0, 1) or not proc.stdout.strip():
        raise RuntimeError(f"aes reconcile failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def _project(root: Path) -> dict:
    return yaml.safe_load((root / ".aes" / "project.yaml").read_text(encoding="utf-8"))


def _when(value: object) -> str:
    """An observation's or a run's time as `YYYY-MM-DD HH:MM UTC`."""
    t = value if isinstance(value, datetime) else datetime.fromisoformat(str(value))
    return t.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC")


def requirement_status(root: Path) -> dict:
    """`aes reconcile --json`, `aes characterize` and the evidence records, indexed for a page.

    Returns {"revision", "produced_at", "dirty", "criteria": {SC id: ...}, "artifacts": {artifact
    id: ...}, "gaps": {component id: [...]}, "drift": {artifact id: [{"kind", "path", "detail",
    "failing"}]}, "evidence": {ER id: [{"observation", "revision", "produced_at", "assessment",
    "freshness", "superseded"}]}}. Drift is every difference AES `characterize` finds between the
    plan and the code at the last commit (the same facts behavior 5.3 reports); a file in a
    governed folder that no planned file names is keyed "". `dirty` is whether the plan or a
    governed file has uncommitted changes (new evidence records and written pages do not count).
    Every value is produced by AES and git from the code and the evidence; nothing is typed by hand.
    """
    rec = _reconcile(root)
    drift: dict[str, list[dict]] = {}
    for d in characterize_check(root).drift:
        drift.setdefault(d.artifact_id or "", []).append(
            {"kind": d.kind, "path": d.path, "detail": d.detail, "failing": d.failing})
    project = _project(root)
    m = project["materialization"]
    fresh = {o["observation_id"]: o["freshness"] for o in rec["observations"]}
    evidence: dict[str, list[dict]] = {}
    for path in sorted((root / m["observations_root"]).glob("*.yaml")):
        o = yaml.safe_load(path.read_text(encoding="utf-8"))
        for a in o.get("assessments") or []:
            evidence.setdefault(a["evidence_requirement_ref"], []).append(
                {"observation": o["observation_id"], "revision": o.get("subject_revision") or "",
                 "produced_at": _when(o["produced_at"]), "assessment": a["assessment"],
                 "freshness": fresh.get(o["observation_id"], "UNKNOWN"),
                 "superseded": o.get("superseded_by") is not None})
    watched = [*(project.get("governed_roots") or []), m["target_path"], m["plans_root"]]
    dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all", "--", *watched],
                           capture_output=True, text=True, check=True).stdout.strip() != ""
    return {
        "revision": rec["subject_revision"],
        "produced_at": _when(rec["produced_at"]),
        "dirty": dirty,
        "criteria": {c["criterion_id"]: c for c in rec["criteria"]},
        "artifacts": {a["artifact_id"]: a for a in rec["artifacts"]},
        "gaps": {c["component_id"]: c["gaps"] for c in rec["components"]},
        "drift": drift,
        "evidence": evidence,
    }


def record_stale_evidence(root: Path) -> list[str]:
    """Run and record (`aes evidence record`) each test subject whose result is missing or stale.

    A subject is recorded when a criterion it routes has an evidence requirement with no current
    support. The record names the commit it ran at, so commit first: AES refuses when a file the
    test depends on has uncommitted changes. Returns the subjects recorded, in order.
    """
    rec = _reconcile(root)
    kinds = {v["id"]: v.get("proof_kind") for v in target(root).get("verification_subjects") or []}
    subjects = sorted({vs for c in rec["criteria"] for miss in c["missing"]
                       if miss["status"] == "NO_CURRENT_SUPPORT" for vs in miss["verification_subject_refs"]
                       if kinds.get(vs) == "deterministic_test"})
    locators = {v.get("id"): v.get("locator") for v in target(root).get("verification_subjects") or []}
    for vs in subjects:
        record(root, vs, _subprocess_dependencies(root, locators.get(vs) or ""))
    return subjects


def _subprocess_dependencies(root: Path, locator: str) -> list[str]:
    """Governed files a test reaches by running a subprocess, which AES cannot see from imports.

    AES discovers dependencies from a test's imports only (evidence.record, `depends_on` declared).
    A test that starts `e2e/*.py` as a subprocess also depends on every file that program imports,
    so it declares all of `src/` whenever it does that. Without this, a result stays current after
    the code it runs changes (Q49).
    """
    path = root / locator
    if not locator or not path.is_file() or "subprocess" not in path.read_text(encoding="utf-8"):
        return []
    return sorted(str(p.relative_to(root)) for p in (root / "src").rglob("*.py"))


def _ids_of(tgt: dict, req: str) -> tuple[list[dict], set[str]]:
    """The behaviors of requirement `req`, and every plan id that belongs to it."""
    behaviors = [n for n in tgt.get("normative_items") or [] if req in (n.get("outcome_refs") or [])]
    ids = {req, *(b["id"] for b in behaviors)}
    criteria = [s for s in tgt.get("success_criteria") or [] if ids & set(s.get("target_refs") or [])]
    ids |= {s["id"] for s in criteria}
    for c in tgt.get("components") or []:
        if ids & set(c.get("target_refs") or []):
            ids |= {c["id"], *(c.get("planned_artifact_refs") or [])}
    ids |= {v["id"] for v in tgt.get("verification_subjects") or []
            if {s["id"] for s in criteria} & set(v.get("criterion_refs") or [])}
    return behaviors, ids


def _result_line(er: dict, missing: dict | None, evidence: list[dict]) -> str:
    """One evidence requirement: its state, and the test result behind it with its commit and time."""
    live = [e for e in evidence if not e["superseded"]]
    current = [e for e in live if e["freshness"] == "CURRENT"]
    if missing is None:
        shown, word = [e for e in current if e["assessment"] == "SUPPORTS"], "supported"
    elif missing["status"] == "REFUTED":
        shown, word = [e for e in current if e["assessment"] == "REFUTES"], "refuted"
    else:
        shown, word = live[-1:], "no current result"
    line = f"    - {er['id']}: **{word}**"
    for e in shown:
        verb = {"SUPPORTS": "passed", "REFUTES": "failed"}.get(e["assessment"], e["assessment"].lower())
        line += (f" — test {verb} at commit `{e['revision'][:12]}`, {e['produced_at']} ({e['observation']}"
                 + ("" if e["freshness"] == "CURRENT" else f", {e['freshness'].lower()} since then") + ")")
    if missing is not None and not shown:
        line += f" — {missing['detail']}"
    older = len(live) - len(shown)
    return line + (f" ({older} older result(s) kept in the evidence records)" if older > 0 and shown else "")


def requirement_pages(root: Path, status: dict | None = None) -> dict[str, str]:
    """The pages behavior 4.1 asks for: `requirements/<id>.md` per requirement, an index and the change log.

    Each requirement page holds, in order: the requirement's text from the plan; a status block per
    behavior (each criterion's standing and the test result behind each evidence requirement, with
    the commit and time it was produced; the files; the drift between plan and code; open gaps);
    then the change-log entries that touch the requirement or anything under it, newest last.
    Every page carries one line starting with `BUILT`, which names the commit and time it was built.
    """
    tgt = target(root)
    status = status or requirement_status(root)
    by = {k: {x["id"]: x for x in tgt.get(k) or []} for k in ("components", "planned_artifacts", "success_criteria")}
    criteria, artifacts, gaps, drift, evidence = (status[k] for k in ("criteria", "artifacts", "gaps", "drift", "evidence"))
    log = entries(root)
    built = (f"{BUILT} `{status['revision'][:12]}` at {status['produced_at']}"
             + (" (the plan or code had uncommitted changes)" if status["dirty"] else "")
             + ". Edit the plan, not this page.")
    out: dict[str, str] = {}
    idx = ["# Requirements and their status", "", built, "",
           "One page per requirement: its text from the plan, then its status from the code and the test "
           "results, then its change log. `make status` records missing test results and rebuilds these pages.",
           "", "## Requirements", ""]
    for o in tgt.get("outcomes") or []:
        rid, (title, _, rest) = o["id"], o["statement"].partition(": ")
        behaviors, ids = _ids_of(tgt, rid)
        scs = [s for s in by["success_criteria"].values() if s["id"] in ids]
        supported = sum(criteria.get(s["id"], {}).get("standing") == "SUPPORTED" for s in scs)
        failing = sum(d["failing"] for aid in ids for d in drift.get(aid, []))
        idx.append(f"- [{rid}](requirements/{rid}.md) — {title.rstrip('.')}: {supported} of {len(scs)} criteria "
                   f"supported, {failing} failing difference(s) between plan and code")
        # A statement written "Title: sentence" shows its title as the heading and its sentence here, not both twice.
        p = [f"# {rid}: {title.rstrip('.')}", "", built, "",
             f"For {o['actor_or_consumer']}: {(rest or o['statement']).strip()}", ""]
        if o.get("rationale"):
            p += [f"Why: {o['rationale'].strip()}", ""]
        p += ["## Status", ""]
        if not behaviors:
            p += ["No behavior in the plan serves this requirement yet.", ""]
        for b in behaviors:
            p += [f"### {b['id']}", "", b["statement"].strip(), ""]  # a short heading; the sentence reads as text
            for s in scs:
                if b["id"] not in (s.get("target_refs") or []):
                    continue
                st = criteria.get(s["id"], {})
                missing = {m["er_id"]: m for m in st.get("missing", [])}
                p += [f"- **{s['id']}**: {s['statement'].strip()}", f"    - Disproved if: {s['disproof'].strip()}",
                      f"    - Standing now: **{st.get('standing', 'unknown')}**"]
                p += [_result_line(er, missing.get(er["id"]), evidence.get(er["id"], []))
                      for er in s.get("evidence_requirements") or []]
            comps = [c for c in by["components"].values() if b["id"] in (c.get("target_refs") or [])]
            arts = [aid for c in comps for aid in c.get("planned_artifact_refs") or []]
            files = [f"`{(by['planned_artifacts'].get(aid, {}).get('locator') or {}).get('exact_path', '')}` "
                     f"({aid}, {artifacts.get(aid, {}).get('status', 'unknown').lower()})" for aid in arts]
            found = [f"`{d['path']}` ({aid}) {d['kind']}: {d['detail']}" for aid in arts for d in drift.get(aid, [])]
            open_gaps = [f"{g['kind']}: {g['detail']}" for c in comps for g in gaps.get(c["id"], [])]
            p += [f"- Files: {'; '.join(files) if files else 'none planned'}",
                  f"- Drift between plan and code: {'; '.join(found) if found else 'none'}",
                  f"- Open gaps: {'; '.join(open_gaps) if open_gaps else 'none'}", ""]
        touching = [e for e in log if ids & {c.split()[-1] for c in e["changes"]}]
        p += ["## Change log", "", f"Newest last: {len(touching)} accepted plan change(s) touch {rid} or an item "
              "under it. Each is written once, automatically, when the change is accepted.", ""]
        for e in touching:
            mine = [c for c in e["changes"] if c.split()[-1] in ids]
            p += [f"- {_when(e['accepted_at'])}, `{e['id']}` (from {'a docstring' if e['origin'] == 'docstring' else 'the plan'}"
                  f", record `{e['record']}`): {e['title']}. On this requirement it {_plain(mine)}."]
        out[f"requirements/{rid}.md"] = "\n".join(p) + "\n"
    orphans = [f"- `{d['path']}`: {d['detail']}" for d in drift.get("", [])]
    idx += ["", "## Files no plan item names", "", *(orphans or ["None."])]
    idx += ["", "## Change log", "",
            f"- [Change log](change-log.md) — every accepted change to the plan, newest first ({len(log)} entries)"]
    out["index.md"] = "\n".join(idx) + "\n"
    out["change-log.md"] = render(log)
    return out


def write_pages(root: Path, out_dir: Path) -> list[str]:
    """Write `requirement_pages` under `out_dir`; returns the pages it wrote.

    A page whose content is unchanged apart from its built-at line is left alone, so committing the
    pages does not make them stale again (the pre-push hook would otherwise never pass); its built-at
    line then names the commit at which its content was last true, which is still true at HEAD.
    """
    changed = []
    for name, text in requirement_pages(root).items():
        path = out_dir / name
        if not path.is_file() or _content(path.read_text(encoding="utf-8")) != _content(text):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            changed.append(name)
    return changed


def _content(text: str) -> list[str]:
    return [line for line in text.splitlines() if not line.startswith(BUILT)]


def stale_pages(root: Path, out_dir: Path) -> list[str]:
    """Each written page under `out_dir` that differs from a fresh build in more than its built-at line."""
    built = requirement_pages(root)
    problems = []
    for name, text in built.items():
        path = out_dir / name
        if not path.is_file():
            problems.append(f"{out_dir / name} is missing; run `make status` and commit it.")
        elif _content(path.read_text(encoding="utf-8")) != _content(text):
            problems.append(f"{out_dir / name} differs from a fresh build; run `make status` and commit it.")
    problems += [f"{p} is no longer built (its requirement left the plan); remove it with `git rm`."
                 for p in sorted(out_dir.rglob("*.md")) if p.relative_to(out_dir).as_posix() not in built]
    return problems


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.requirement_status [--record] [--write DIR | --check DIR]`.

    With no option, print the status as JSON. `--record` first records each missing or stale test
    result; `--write DIR` writes the requirement pages under DIR; `--check DIR` fails (exit 1) when a
    page under DIR differs from a fresh build in more than its built-at line.
    """
    ap = argparse.ArgumentParser(prog="python -m lockstep.requirement_status", description=(main.__doc__ or "").splitlines()[0])
    ap.add_argument("--record", action="store_true", help="record missing or stale test results first")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--write", type=Path, metavar="DIR")
    group.add_argument("--check", type=Path, metavar="DIR")
    a = ap.parse_args(argv)
    root = find_root(Path.cwd())
    if root is None:
        print("no .aes/project.yaml here or above", file=sys.stderr)
        return 2
    recorded = record_stale_evidence(root) if a.record else []
    for vs in recorded:
        print(f"RECORDED {vs}")
    if a.check:
        problems = stale_pages(root, root / a.check)
        for p in problems:
            print(f"STALE {p}")
        print(f"OUTCOME stale={len(problems)} recorded={len(recorded)}")
        return 1 if problems else 0
    if a.write:
        changed = write_pages(root, root / a.write)
        for name in changed:
            print(f"WROTE {a.write / name}")
        print(f"OUTCOME recorded={len(recorded)} changed={len(changed)}")
        return 0
    print(json.dumps(requirement_status(root), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
