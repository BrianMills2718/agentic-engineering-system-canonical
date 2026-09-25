"""Probe 0 temporary review projection.

Renders one self-contained HTML page from a project's .aes/target.yaml plus the
realized repository (git ls-files) so a person can judge the accepted target
without reading YAML. This is a temporary validated projection in the
Representation Router sense: it is derived, never authority, and becomes a
durable `aes review` command only after repeated use proves it earns one.

Usage: render_review.py --root <project> --out <file.html> [--decision <md-file>]
"""

from __future__ import annotations

import argparse
import html
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from agentic_engineering_system.records import load_project, load_target

E = html.escape


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def render(root: Path, decision_md: str | None) -> str:
    project = load_project(root / ".aes" / "project.yaml")
    target = load_target(root / ".aes" / "target.yaml")
    head = git(root, "rev-parse", "HEAD")
    tracked = set(git(root, "ls-files").splitlines())
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    by_id: dict[str, object] = {}
    for fam in ("outcomes", "normative_items", "success_criteria", "components", "planned_artifacts", "verification_subjects"):
        for rec in getattr(target, fam):
            by_id[rec.id] = rec
    er_owner = {er.id: sc for sc in target.success_criteria for er in sc.evidence_requirements}
    vs_by_er: dict[str, list] = {}
    for vs in target.verification_subjects:
        for er in vs.evidence_requirement_refs:
            vs_by_er.setdefault(er, []).append(vs)
    art_by_id = {a.id: a for a in target.planned_artifacts}
    art_path = {a.id: a.locator.exact_path for a in target.planned_artifacts}

    def exists(path: str) -> bool:
        return path in tracked

    out: list[str] = []
    w = out.append
    w("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>")
    w(f"<title>{E(project.project_id)}: accepted target review</title>")
    w("""<style>
:root{--bg:#fff;--fg:#1a1a1a;--muted:#5a5a5a;--line:#d8d8d8;--ok:#1b7f3b;--miss:#b3261e;--warn:#9a6700;--box:#f5f5f5}
@media (prefers-color-scheme:dark){:root{--bg:#131313;--fg:#ececec;--muted:#a8a8a8;--line:#3a3a3a;--ok:#5fcf7a;--miss:#ff7b72;--warn:#e3b341;--box:#1e1e1e}}
body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif;max-width:1100px;margin-inline:auto}
h1{font-size:1.5rem;margin:.2em 0}h2{font-size:1.15rem;margin:1.6em 0 .4em;border-bottom:1px solid var(--line);padding-bottom:.2em}
.lede{color:var(--muted)}.box{background:var(--box);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:10px 0}
.decision{border-left:5px solid var(--warn)}table{border-collapse:collapse;width:100%;font-size:.92rem}th,td{border:1px solid var(--line);padding:6px 8px;vertical-align:top;text-align:left}
th{background:var(--box)}.ok{color:var(--ok);font-weight:600}.miss{color:var(--miss);font-weight:600}.id{font-family:ui-monospace,monospace;font-size:.85em;color:var(--muted)}
details>summary{cursor:pointer;color:var(--muted)}code{font-family:ui-monospace,monospace;font-size:.9em}.small{font-size:.85rem;color:var(--muted)}
ul{margin:.3em 0 .3em 1.2em}
@media (max-width:640px){table,tbody,tr,td{display:block;width:100%;box-sizing:border-box}thead,tr:has(th){display:none}tr{border:1px solid var(--line);margin:0 0 10px;border-radius:6px}td{border:0;border-top:1px solid var(--line)}td:first-child{border-top:0}td:empty{display:none}td[data-l]::before{content:attr(data-l);display:block;font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px}
</style></head><body>""")
    w(f"<h1>{E(project.project_id)}: what this project has accepted should be true</h1>")
    w("<p class='lede'>This page is built from the project's own target record and its repository at one exact revision. "
      "It shows what the project promises, what would prove each promise, and which promised files exist yet. "
      "It is a derived view, not the record itself: nothing here is authority.</p>")
    w(f"<p class='small'>Source: <code>.aes/target.yaml</code> · repository revision <code>{E(head[:12])}</code> · built {E(now)}</p>")

    if decision_md:
        w("<div class='box decision'><h2 style='margin-top:0;border:0'>Decision needed from you</h2>")
        for para in decision_md.strip().split("\n\n"):
            w(f"<p>{E(para).replace(chr(10), '<br>')}</p>")
        w("</div>")

    # Product intent
    w("<h2>1. What the project is for</h2>")
    for o in target.outcomes:
        w(f"<div class='box'><p><strong>Outcome</strong> <span class='id'>{E(o.id)}</span> for <em>{E(o.actor_or_consumer)}</em></p>")
        w(f"<p>{E(o.statement.strip())}</p>")
        if o.rationale:
            w(f"<p class='small'><strong>Why:</strong> {E(o.rationale.strip())}</p>")
        if o.non_goals:
            w("<p class='small'><strong>Not trying to do:</strong> " + "; ".join(E(n) for n in o.non_goals) + "</p>")
        w("</div>")

    w("<h2>2. The rules the system must obey</h2><p class='lede'>Each rule is a promise. The next section shows how each promise would be proved.</p><table><tr><th>Rule</th><th>Kind</th><th>Statement</th></tr>")
    for n in target.normative_items:
        w(f"<tr><td class='id' data-l='rule'>{E(n.id)}</td><td data-l='kind'>{E(n.kind)}</td><td data-l='statement'>{E(n.statement.strip())}</td></tr>")
    w("</table>")

    # Assurance matrix
    w("<h2>3. How each promise gets proved</h2>")
    w("<p class='lede'>A success criterion is only supported when <em>every</em> evidence requirement under it has current supporting evidence. "
      "A test passing is one requirement, not the whole criterion. Human review rows are requirements too.</p>")
    w("<table><tr><th>Criterion</th><th>What would prove it</th><th>Planned proof</th><th>Proof file exists?</th></tr>")
    for sc in target.success_criteria:
        first = True
        rows = sc.evidence_requirements
        for er in rows:
            subjects = vs_by_er.get(er.id, [])
            cells = []
            for vs in subjects:
                loc = vs.locator
                if loc.startswith("external:"):
                    cells.append(f"{E(vs.id)} <span class='small'>({E(vs.proof_kind)}, {E(vs.proof_role)}; external: {E(loc[9:])})</span>")
                else:
                    mark = "<span class='ok'>yes</span>" if exists(loc) else "<span class='miss'>not yet</span>"
                    cells.append(f"{E(vs.id)} <span class='small'>({E(vs.proof_kind)}, {E(vs.proof_role)})</span> <code>{E(loc)}</code> {mark}")
            proof = "<br>".join(cells) if cells else "<span class='miss'>no verification subject planned</span>"
            planned_exists = ""
            if subjects:
                internal = [vs for vs in subjects if not vs.locator.startswith("external:")]
                if internal:
                    planned_exists = "<span class='ok'>yes</span>" if all(exists(vs.locator) for vs in internal) else "<span class='miss'>not yet</span>"
                else:
                    planned_exists = "<span class='small'>outside the repo</span>"
            crit = ""
            if first:
                crit = (f"<span class='id'>{E(sc.id)}</span><br>{E(sc.statement.strip())}"
                        f"<details><summary>what would disprove it</summary>{E(sc.disproof.strip())}</details>")
                first = False
            w(f"<tr><td data-l='criterion'>{crit}</td><td data-l='what would prove it'><span class='id'>{E(er.id)}</span> <em>{E(er.kind)}</em><br>{E(er.requirement.strip())}</td><td data-l='planned proof'>{proof}</td><td data-l='proof file exists?'>{planned_exists}</td></tr>")
    w("</table>")

    # Realization map
    w("<h2>4. The files the project has committed to, and which exist</h2>")
    w("<div class='grid'>")
    planned_paths = set()
    for c in target.components:
        w(f"<div class='box'><p><strong>{E(c.id)}</strong><br><span class='small'>{E(c.responsibility.strip())}</span></p><ul>")
        for aid in c.planned_artifact_refs:
            p = art_path[aid]; planned_paths.add(p)
            mark = "<span class='ok'>exists</span>" if exists(p) else "<span class='miss'>not yet</span>"
            w(f"<li><code>{E(p)}</code> {mark}</li>")
        w("</ul></div>")
    w("</div>")
    unlisted = [a for a in target.planned_artifacts if a.id not in {aid for c in target.components for aid in c.planned_artifact_refs}]
    if unlisted:
        w("<p class='small'>Planned files not owned by a component: " + ", ".join(f"<code>{E(a.locator.exact_path)}</code>" + (" (exists)" if exists(a.locator.exact_path) else " (not yet)") for a in unlisted) + "</p>")
    # Orphans under governed roots
    orphans = sorted(f for f in tracked if any(f.startswith(r) for r in project.governed_roots) and f not in {a.locator.exact_path for a in target.planned_artifacts})
    w("<h2>5. Files under governed roots that nobody planned</h2>")
    if orphans:
        w("<p class='miss'>These files exist under a governed root but are not planned artifacts. Each one is a topology violation until it is planned or removed.</p><ul>")
        for f in orphans:
            w(f"<li><code>{E(f)}</code></li>")
        w("</ul>")
    else:
        w("<p class='ok'>None. Every tracked file under " + ", ".join(f"<code>{E(r)}</code>" for r in project.governed_roots) + " is a planned artifact.</p>")

    w("<h2>6. Where this comes from</h2><p class='small'>Governed roots: " + ", ".join(f"<code>{E(r)}</code>" for r in project.governed_roots) +
      f". Target id <code>{E(target.target_id)}</code>, schema <code>{E(target.schema_version)}</code>. "
      "Existence marks come from <code>git ls-files</code> at the revision above; they say a file is tracked, not that it is correct or that its tests ran.</p>")
    w("</body></html>")
    return "".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--decision", type=Path, help="markdown file whose text is shown as the pending human decision")
    a = ap.parse_args(argv)
    decision = a.decision.read_text() if a.decision else None
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(render(a.root.resolve(), decision))
    print(a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
