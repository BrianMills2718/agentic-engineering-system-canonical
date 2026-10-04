"""Probe 0 temporary review projection (second real use: the AES plan gate).

Renders one self-contained HTML page from a project's .aes/target.yaml plus the
realized repository (git ls-files) so a person can judge the target without
reading YAML. With --proposal it renders the target that proposal would leave,
limited to what the proposal adds or changes and the chains they sit on.

This is a temporary validated projection in the Representation Router sense
(references/planning-review.md, "Reviewing a structured proposal or target
before implementation"): derived, never authority. The plan gate proposal
(proposals/aes-plan-gate/PLAN-AES-PLAN-GATE.yaml) promotes it to `aes review`.

Lenses: decision; product intent; derivation graph (outcome -> rules ->
criteria -> evidence -> proofs -> files) with existence and execution marks;
reference check with its method; port graph (Architecture lens: the data
passing between typed functions, laid out by ELK); review points; orphan files.

Usage: render_review.py --root <project> --out <file.html> [--decision <md>]
       [--proposal <proposal.yaml>] [--review-points <yaml>] [--elk <elk.bundled.js>]
"""

from __future__ import annotations

import argparse
import ast
import html
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

from agentic_engineering_system.evidence import assess
from agentic_engineering_system.planning import apply_delta, load_proposal, references
from agentic_engineering_system.records import TargetRecord, load_project, load_target, validate_target_refs

E = html.escape
HERE = Path(__file__).resolve().parent
# Types that carry no design information as a wire: a str or a Path joins everything to everything.
TRIVIAL = {"str", "int", "bool", "float", "bytes", "dict", "list", "set", "tuple", "Any", "Path", "None",
           "Sequence", "Mapping", "Iterable", "Literal", "Optional", "datetime", "object"}


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


# --------------------------------------------------------------------------- port model
def types_in(annotation: str | None) -> list[str]:
    """Names of the non-trivial types an annotation mentions: 'tuple[Finding, ...]' -> ['Finding']."""
    if not annotation:
        return []
    names = [n.id for n in ast.walk(ast.parse(annotation, mode="eval")) if isinstance(n, ast.Name)]
    return sorted({n for n in names if n not in TRIVIAL})


def parse_export(entry: str) -> dict | None:
    """'name(a: T) -> R' -> signature; a bare name (untyped export) -> None."""
    if "(" not in entry:
        return None
    fn = ast.parse(f"def {entry}:\n    pass\n").body[0]
    return {"name": fn.name, "ret": ast.unparse(fn.returns) if fn.returns else None,
            "args": [{"name": a.arg, "annotation": ast.unparse(a.annotation) if a.annotation else None}
                     for a in fn.args.args]}


def code_signatures(path: Path) -> list[dict]:
    """Public top-level functions of a realized Python file, with their annotations."""
    out = []
    for fn in ast.parse(path.read_text()).body:
        if isinstance(fn, ast.FunctionDef) and not fn.name.startswith("_"):
            out.append({"name": fn.name, "ret": ast.unparse(fn.returns) if fn.returns else None,
                        "args": [{"name": a.arg, "annotation": ast.unparse(a.annotation) if a.annotation else None}
                                 for a in fn.args.args]})
    return out


def port_model(target: TargetRecord, root: Path, scope: set[str] | None) -> dict:
    """Functions as nodes, typed arguments and returns as ports, a wire where a return type is an argument type.

    Planned typed exports are used where the target has them (proposed design). Where a
    planned Python source file has none, the realized file's own signatures are used and
    marked as read from the code. `scope` limits nodes to those artifact ids (proposal mode).
    """
    comp_of = {aid: c for c in target.components for aid in c.planned_artifact_refs}
    nodes, untyped, origin = [], [], set()
    for a in target.planned_artifacts:
        if a.kind != "source" or not a.locator.exact_path.endswith(".py") or (scope is not None and a.id not in scope):
            continue
        sigs = [s for s in (parse_export(e) for e in a.exports) if s]
        if sigs:
            origin.add("plan")
        else:
            if scope is not None:
                untyped.append(a.id)
                continue
            f = root / a.locator.exact_path
            sigs = code_signatures(f) if f.exists() else []
            if sigs:
                origin.add("code")
        comp = comp_of.get(a.id)
        label = (comp.id if comp else a.id).split("-", 2)[-1].replace("-", " ").title()
        for s in sigs:
            args = [dict(x, types=types_in(x["annotation"])) for x in s["args"]]
            nodes.append({"id": f"{a.id}::{s['name']}", "name": s["name"], "artifact": a.id,
                          "component": comp.id if comp else a.id, "component_label": label,
                          "ret": s["ret"], "ret_types": types_in(s["ret"]), "args": args, "proposed": False})
    wires = []
    for c in nodes:
        used = set()
        for arg in c["args"]:
            if not arg["types"]:
                continue
            cands = []
            for p in nodes:
                if p is c or p["id"] in used or not set(p["ret_types"]) & set(arg["types"]):
                    continue
                cands.append((0 if p["ret"] == arg["annotation"] else 1, p))
            if not cands:
                arg["unfed"] = True
                continue
            cands.sort(key=lambda x: x[0])
            best = cands[0]
            used.add(best[1]["id"])
            wires.append({"from": best[1]["id"], "to": c["id"], "to_arg": arg["name"], "label": best[1]["ret"],
                          "ambiguous": sum(1 for r, _ in cands if r == best[0]) > 1})
    # a function no wire touches is list-shaped: name it under the drawing instead of drawing it
    touched = {w["from"] for w in wires} | {w["to"] for w in wires}
    loose = [n for n in nodes if n["id"] not in touched and not any(a.get("unfed") for a in n["args"])]
    nodes = [n for n in nodes if n not in loose]
    return {"nodes": nodes, "wires": wires, "untyped": untyped, "origin": sorted(origin), "loose": loose,
            "mode": "proposal" if scope is not None else "target"}


def layout_ports(model: dict, elk: Path | None) -> str | None:
    if not model["nodes"] or elk is None:
        return None
    r = subprocess.run(["node", str(HERE / "port_layout.mjs"), "--elk", str(elk)], input=json.dumps(model),
                       capture_output=True, text=True, check=True)
    return r.stdout


# --------------------------------------------------------------------------- page
def render(root: Path, decision_md: str | None, proposal_path: Path | None, rp_path: Path | None, elk: Path | None) -> str:
    project = load_project(root / ".aes" / "project.yaml")
    target = load_target(root / ".aes" / "target.yaml")
    head = git(root, "rev-parse", "HEAD")
    tracked = set(git(root, "ls-files").splitlines())
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    proposed: set[str] = set()
    delta_violations: list[str] = []
    title_subject = f"{project.project_id}: what this project has accepted should be true"
    if proposal_path:
        proposal = load_proposal(proposal_path)
        target, delta_violations = apply_delta(target, proposal.target_delta)
        raw = yaml.safe_load(proposal_path.read_text())["target_delta"]
        for section in ("add", "change"):
            for fam, entries in (raw.get(section) or {}).items():
                for e in entries:
                    proposed.add(e.get("id") or e.get("evidence_requirement_ref"))
                    for sc_er in e.get("evidence_requirements", []) or []:
                        proposed.add(sc_er["id"])
        title_subject = f"{proposal.proposal_id}: what this plan would add to {project.project_id}"

    # execution marks: only observations of the root's own accepted target count
    standing = {}
    try:
        for cs in assess(root).criteria:
            for er in cs.requirements:
                standing[er.er_id] = er.status
    except Exception as exc:  # noqa: BLE001 - shown on the page, never hidden
        standing["__error__"] = str(exc)

    art_path = {a.id: a.locator.exact_path for a in target.planned_artifacts}
    exists = lambda p: p in tracked  # noqa: E731

    def short(text: str, n: int = 0) -> str:  # whole text on one line; boxes grow to fit, nothing is cut
        return " ".join(text.split())

    nodes: list[dict] = []
    edges: list[tuple[str, str, str]] = []
    for o in sorted(target.outcomes, key=lambda o: o.id not in proposed):
        nodes.append({"id": o.id, "layer": 0, "label": short(o.statement, 60), "state": "outcome", "mark": "outcome",
                      "full": o.statement.strip(), "extra": {"for": o.actor_or_consumer, "why": (o.rationale or "").strip(), "not trying to do": [g.replace("_", " ") for g in (o.non_goals or [])]}})
    for n in target.normative_items:
        nodes.append({"id": n.id, "layer": 1, "label": short(n.statement), "state": "rule", "mark": n.kind, "full": n.statement.strip(), "extra": {"kind": n.kind}})
        edges += [(ref, n.id, "derived from") for ref in n.outcome_refs]
    for sc in target.success_criteria:
        nodes.append({"id": sc.id, "layer": 2, "label": short(sc.statement), "state": "criterion", "mark": "criterion", "full": sc.statement.strip(),
                      "extra": {"what would disprove it": sc.disproof.strip()}})
        edges += [(ref, sc.id, "proves") for ref in sc.target_refs]
        for er in sc.evidence_requirements:
            st = standing.get(er.id)
            mark = {"SUPPORTED": "has run: supports", "REFUTED": "has run: refutes"}.get(st, "not run yet" if er.id not in proposed else "new: not run")
            nodes.append({"id": er.id, "layer": 3, "label": short(er.requirement), "state": "run" if st == "SUPPORTED" else ("refuted" if st == "REFUTED" else "notrun"),
                          "mark": mark, "full": er.requirement.strip(), "extra": {"kind of evidence": er.kind, "run status": mark}})
            edges.append((sc.id, er.id, "needs evidence"))
    for vs in target.verification_subjects:
        loc = vs.locator
        ex = None if loc.startswith("external:") else exists(loc)
        st = "external" if ex is None else ("exists" if ex else "missing")
        nodes.append({"id": vs.id, "layer": 4, "label": short(vs.purpose), "state": st, "mark": {"external": "outside the repo", "exists": "file exists", "missing": "not written yet"}[st],
                      "full": vs.purpose.strip(), "extra": {"proof kind": vs.proof_kind, "role": vs.proof_role, "where": loc}})
        edges += [(er, vs.id, "planned proof") for er in vs.evidence_requirement_refs]
        hit = next((a for a, p in art_path.items() if p == loc), None)
        if hit:
            edges.append((vs.id, hit, "lives in"))
    for b in target.external_boundaries:
        nodes.append({"id": "EXT:" + b.evidence_requirement_ref, "layer": 4, "label": short(b.boundary), "state": "external", "mark": "outside the repo",
                      "full": b.boundary.strip(), "extra": {"recorded by": "an observation written outside a test run"}})
        edges.append((b.evidence_requirement_ref, "EXT:" + b.evidence_requirement_ref, "planned proof"))
        if b.evidence_requirement_ref in proposed:
            proposed.add("EXT:" + b.evidence_requirement_ref)
    comp_of = {aid: c.id for c in target.components for aid in c.planned_artifact_refs}
    for a in target.planned_artifacts:
        ex = exists(a.locator.exact_path)
        nodes.append({"id": a.id, "layer": 5, "label": a.locator.exact_path.rsplit("/", 1)[-1], "state": "exists" if ex else "missing", "mark": "file exists" if ex else "not written yet",
                      "full": a.purpose.strip(), "extra": {"path": a.locator.exact_path, "kind": a.kind, "component": comp_of.get(a.id, "(none)")}})
        edges += [(ref, a.id, "justified by") for ref in a.semantic_justification_refs]
    known = {n["id"] for n in nodes}
    edges = [e for e in edges if e[0] in known and e[1] in known]

    if proposal_path:  # keep what the proposal touches and the chains it sits on
        down, up = {}, {}
        for a, b, _ in edges:
            down.setdefault(a, []).append(b)
            up.setdefault(b, []).append(a)
        keep = set(proposed & known)
        for m in (down, up):
            stack = list(proposed & known)
            while stack:
                x = stack.pop()
                for y in m.get(x, []):
                    if y not in keep:
                        keep.add(y)
                        stack.append(y)
        nodes = [n for n in nodes if n["id"] in keep]
        edges = [e for e in edges if e[0] in keep and e[1] in keep]
    for n in nodes:
        n["proposed"] = n["id"] in proposed

    layers = ["Outcome", "Rules it must obey", "What counts as success", "Evidence each needs", "Planned proofs", "Files committed to"]
    model = {"nodes": nodes, "edges": [{"from": a, "to": b, "kind": k} for a, b, k in edges], "layers": layers}

    # reference check (router step 2: run the record's own check, show numbers with the method)
    refs = references(target)
    ref_violations = validate_target_refs(target)
    scope = {a.id for a in target.planned_artifacts if a.id in proposed} if proposal_path else None
    ports = port_model(target, root, scope)
    for pn in ports["nodes"] + ports["loose"]:
        pn["proposed"] = pn["artifact"] in proposed
    unfed = [(pn["name"], a["annotation"]) for pn in ports["nodes"] for a in pn["args"] if a.get("unfed")]
    ambiguous = [w for w in ports["wires"] if w["ambiguous"]]
    ports_svg = layout_ports(ports, elk)

    out: list[str] = []
    w = out.append

    def bullets(items: list[str], cls: str = "") -> str:  # items are already-escaped HTML
        items = [i for i in items if i]
        return f"<ul class='pts {cls}'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>" if items else ""

    def md_block(text: str) -> str:
        """Paragraphs, "- " bullet lists and **bold** from a small markdown file."""
        import re
        parts = []
        for block in text.strip().split("\n\n"):
            lines = block.splitlines()
            fmt = lambda t: re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", re.sub(r"`([^`]+)`", r"<code>\1</code>", E(t)))  # noqa: E731
            if all(l.lstrip().startswith("- ") for l in lines):
                parts.append(bullets([fmt(l.lstrip()[2:]) for l in lines]))
            elif len(lines) > 1 and all(l.lstrip().startswith("- ") for l in lines[1:]):
                parts.append(f"<p>{fmt(lines[0])}</p>" + bullets([fmt(l.lstrip()[2:]) for l in lines[1:]]))
            else:
                parts.append(f"<p>{fmt(' '.join(lines))}</p>")
        return "".join(parts)
    w("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>")
    w(f"<title>{E(title_subject.split(':')[0])} review</title>")
    w(STYLE)
    w(f"</head><body><h1>{E(title_subject)}</h1>")
    w("<div class='lede'>" + bullets([
        "Built from the project's target record" + (" plus a proposed change, applied in memory" if proposal_path else "") + ", and the repository at one exact revision.",
        "Shows what is promised, what would prove each promise, which promised files exist and which proofs have run.",
        "A derived view, not the record: nothing here is authority."]) + "</div>")
    w(f"<p class='small'>Source: <code>.aes/target.yaml</code>" + (f" + <code>{E(str(proposal_path.name))}</code>" if proposal_path else "")
      + f" · repository <code>{E(project.project_id)}</code> at <code>{E(head[:12])}</code> · built {E(now)}</p>")

    if decision_md:
        w("<div class='box decision'><h2 class='h0'>Decision needed from you</h2>")
        w(md_block(decision_md))
        w("</div>")

    sec = 0

    def h2(text: str) -> None:
        nonlocal sec
        sec += 1
        w(f"<h2>{sec}. {text}</h2>")

    if rp_path:
        rps = yaml.safe_load(rp_path.read_text())["review_points"]
        h2(f"The {len(rps)} points where you would get something to open")
        w("<div class='lede'>" + bullets(["Each review point is a working slice you open, not a document.",
            "Before it reaches you, an automatic check loads it at phone width (390 px).",
            "The check fails it if it is blank, an error page, or throws a script error."]) + "</div><ol class='rps'>")
        for rp in rps:
            w(f"<li class='box'><p><strong>{E(rp['title'])}</strong> <span class='id'>{E(rp['id'])}</span></p><p class='small'>Open: <code>{E(rp['entrypoint'])}</code></p><p class='small'>Try:</p><ul>")
            for t in rp["try"]:
                w(f"<li>{E(t)}</li>")
            w(f"</ul><p class='small'>Covers: {', '.join(E(c) for c in rp.get('covers', []))} · render check: {E(rp.get('render_check', 'not run yet'))}</p></li>")
        w("</ol>")

    h2("What it is for")
    for o in target.outcomes:
        if proposal_path and o.id not in proposed:
            continue
        w(f"<div class='box'><p><strong>Outcome</strong> <span class='id'>{E(o.id)}</span> for <em>{E(o.actor_or_consumer)}</em></p><p>{E(o.statement.strip())}</p>")
        if o.non_goals:
            w("<p class='small'><strong>Not trying to do:</strong></p>" + bullets([E(x.replace("_", " ")) for x in o.non_goals], "small"))
        w("</div>")

    n_ex = sum(n["state"] == "exists" for n in nodes); n_miss = sum(n["state"] == "missing" for n in nodes)
    n_ext = sum(n["state"] == "external" for n in nodes); n_run = sum(n["state"] == "run" for n in nodes)
    h2("How the outcome turns into proof and files")
    w("<div class='lede'><p><strong>How to read it</strong></p>" + bullets([
        "Left to right: outcome → rules it implies → what counts as success → evidence each success needs → planned proof → file it lives in.",
        "The small words under each column heading say what a line into that column means.",
        "Tap a box to light up its chain; the panel lists every link with its meaning.",
        "On a phone the same chains are a list you open one step at a time; the drawing is one tap away."])
      + "<p><strong>Colours and outlines</strong></p>" + bullets([
        f"<span class='sw ex'></span> file exists ({n_ex})", f"<span class='sw miss'></span> not written yet ({n_miss})",
        f"<span class='sw run'></span> evidence has run and supports ({n_run})",
        f"<span class='sw ext'></span> proved outside the repository, by a person or a live run ({n_ext})",
        "<span class='sw prop'></span> thick dashed outline: added or changed by this proposal" if proposal_path else ""]) + "</div>")
    w("<div class='view'><div class='graphwrap'><svg id='g' role='img' aria-label='derivation graph from outcome to files'></svg></div>"
      "<aside id='insp' class='insp'><p class='small'>Nothing selected. Tap a box in the diagram.</p></aside></div>")
    w("<script id='model' type='application/json'>" + json.dumps(model).replace("</", "<\\/") + "</script>")
    w(DERIVATION_JS)

    h2("Does every reference resolve?")
    bad = len(ref_violations) + len(delta_violations)
    w(f"<p class='{'miss' if bad else 'okt'}'>{len(refs)} references checked, {bad} problem{'s' if bad != 1 else ''}.</p>")
    for v in delta_violations + ref_violations:
        w(f"<p class='small'>{E(v)}</p>")
    w("<p class='small'><strong>Method</strong></p>" + bullets([
        "Every id the target names (rules to outcomes, criteria to rules, components to files, proofs to evidence) is looked up with AES's own <code>references()</code> and <code>validate_target_refs()</code>.",
        "Those also catch duplicate ids and duplicate paths.",
        "Zero problems means the record is consistent. It does not mean the design is right."], "small"))

    h2("What data passes between the functions")
    if ports_svg:
        src = {"plan": "typed signatures in the plan", "code": "the functions in the code at this revision (the plan has no typed signatures)"}
        w("<div class='lede'>" + bullets([
            "Each box is one function.",
            "A wire means one function's result is the input another one needs, matched by type; the word on the wire is that type.",
            "A grey stub on top of a box is an input nothing here produces: it comes from outside.",
            "Solid outline: added by this proposal. Dashed outline: existing." if proposal_path else "",
            "Tap a function to see the file it lives in.",
            "On a phone each function is one entry: what it takes and from whom, what it gives and to whom.",
            f"Built from {' and '.join(src[o] for o in ports['origin'])}."]) + "</div>")
        # Phone: the drawing is wider than the screen and loses to a list there, so the same wires
        # are also written as one line per function (shown at phone width; the drawing is one tap away).
        name = {n["id"]: n["name"] for n in ports["nodes"]}
        w("<ul class='wiring'>")
        for n in ports["nodes"]:
            ins = [f"<code>{E(x['label'])}</code> from <code>{E(name[x['from']])}</code>" + (" (or another function giving the same type)" if x['ambiguous'] else "") for x in ports["wires"] if x["to"] == n["id"]]
            ins += [f"<code>{E(a['annotation'])}</code> from outside" for a in n["args"] if a.get("unfed")]
            outs = [f"<code>{E(name[x['to']])}</code>" for x in ports["wires"] if x["from"] == n["id"]]
            w(f"<li><a href='#' data-id='{E(n['artifact'])}' class='pfl'><strong><code>{E(n['name'])}</code></strong></a> <span class='id'>{E(n['component_label'])}{'' if n['proposed'] or not proposal_path else ', existing'}</span>"
              + bullets([f"takes {x}" for x in ins] or ["takes nothing from the functions here"])
              + bullets([f"gives <code>{E(n['ret'])}</code> to {', '.join(outs)}" if outs else (f"returns <code>{E(n['ret'])}</code> (used outside this drawing)" if n['ret'] else "")]) + "</li>")
        w("</ul>")
        w(f"<div class='graphwrap pg'>{ports_svg}</div>")
        w(bullets([f"{len(ports['nodes'])} functions, {len(ports['wires'])} wires",
                   f"{len(unfed)} inputs from outside" + (f": {', '.join(E(f'{n}: {t}') for n, t in unfed)}" if unfed else ""),
                   f"Not drawn, because no type joins them to anything: {', '.join(E(n['name']) for n in ports['loose'])}" if ports['loose'] else "",
                   f"{len(ambiguous)} wire{'s' if len(ambiguous) != 1 else ''} where more than one function could supply the input (drawn dashed)" if ambiguous else ""], "small"))
    else:
        w("<p class='miss'>Unavailable: no planned or realized typed function signatures to draw from"
          + ("" if elk else ", or no ELK layout engine given (--elk)") + ".</p>")
    if ports["untyped"]:
        w("<p class='miss'>Files this proposal adds or changes with no typed export, so they cannot be drawn: " + ", ".join(f"<code>{E(x)}</code>" for x in ports["untyped"]) + ".</p>")

    orphans = sorted(f for f in tracked if any(f.startswith(r) for r in project.governed_roots) and f not in set(art_path.values()))
    h2("Files under governed roots that nobody planned")
    if orphans:
        w("<p class='miss'>These files exist under a governed root but are not planned. Each one is a topology violation until it is planned or removed.</p><ul>")
        w("".join(f"<li><code>{E(f)}</code></li>" for f in orphans) + "</ul>")
    else:
        w("<p class='okt'>None. Every tracked file under " + ", ".join(f"<code>{E(r)}</code>" for r in project.governed_roots) + " is planned.</p>")

    h2("Where this comes from")
    w(bullets([
        "Governed roots: " + ", ".join(f"<code>{E(r)}</code>" for r in project.governed_roots),
        f"Target <code>{E(target.target_id)}</code>, schema <code>{E(target.schema_version)}</code>",
        "File marks come from <code>git ls-files</code> at the revision above: a file is tracked, not correct.",
        "Run marks come from <code>aes evidence status</code>: a current observation supports it.",
        f"Run status unavailable: {E(standing['__error__'])}" if "__error__" in standing else "",
        "Rendered by <code>scripts/probe/render_review.py</code> (temporary; the plan gate proposes <code>aes review</code>)."], "small"))
    w("</body></html>")
    return "".join(out)


STYLE = """<style>
:root{--bg:#fff;--fg:#1a1a1a;--muted:#5a5a5a;--line:#d0d0d0;--box:#f5f5f5;--accent:#1d4ed8;--warn:#c2410c;
--ex:#cfe0ff;--exs:#1d4ed8;--miss:#ffe1c7;--misss:#c2410c;--ext:#e6e6e6;--exts:#6b6b6b;--run:#1d4ed8}
@media (prefers-color-scheme:dark){:root{--bg:#131313;--fg:#ececec;--muted:#a8a8a8;--line:#3a3a3a;--box:#1e1e1e;--accent:#8ab4ff;--warn:#ffa463;
--ex:#1c3260;--exs:#8ab4ff;--miss:#5a2e10;--misss:#ffa463;--ext:#2c2c2c;--exts:#9a9a9a;--run:#8ab4ff}}
body{margin:0 auto;padding:16px;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif;max-width:1560px}
h1{font-size:1.45rem;margin:.2em 0}h2{font-size:1.15rem;margin:1.6em 0 .4em;border-bottom:1px solid var(--line);padding-bottom:.2em}.h0{margin-top:0;border:0}
.lede{color:var(--muted)}.box{background:var(--box);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:10px 0}
.decision{border-left:5px solid var(--warn)}.okt{color:var(--accent);font-weight:600}.miss{color:var(--warn);font-weight:600}
.id{font-family:ui-monospace,monospace;font-size:.85em;color:var(--muted)}code{font-family:ui-monospace,monospace;font-size:.9em;overflow-wrap:anywhere}
.small{font-size:.85rem;color:var(--muted)}ul{margin:.3em 0 .3em 1.2em}ol.rps{padding-left:0;list-style:none}
.view{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:12px;align-items:start}@media (max-width:900px){.view{grid-template-columns:minmax(0,1fr)}.insp{position:static;max-height:none}}
.graphwrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--box);padding:6px}
.insp{border:1px solid var(--line);border-radius:8px;padding:10px 12px;position:sticky;top:8px;max-height:90vh;overflow:auto;background:var(--bg)}.insp h3{margin:.2em 0 .4em;font-size:1.05rem}.insp{overflow-wrap:anywhere}
.sw{display:inline-block;width:.9em;height:.9em;border-radius:3px;vertical-align:-2px;margin-right:3px;border:1.5px solid var(--line)}
.sw.ex{background:var(--ex);border-color:var(--exs)}.sw.miss{background:var(--miss);border-color:var(--misss)}.sw.ext{background:var(--ext);border-color:var(--exts)}
.sw.run{background:var(--bg);border:2.5px solid var(--run)}.sw.prop{background:var(--bg);border:2.5px dashed var(--fg)}
svg .lay{font:600 12px system-ui,sans-serif;fill:var(--muted)}svg .rel{font:italic 10.5px system-ui,sans-serif;fill:var(--muted)}
ul.pts{margin:.25em 0 .5em 1.2em;padding:0}ul.pts li{margin:.15em 0}div.lede p{margin:.4em 0 .1em}
svg .node rect{fill:var(--bg);stroke:var(--line);stroke-width:1.2}svg .node.st-outcome rect{stroke:var(--fg);stroke-width:2}
svg .node.st-exists rect{fill:var(--ex);stroke:var(--exs)}svg .node.st-missing rect{fill:var(--miss);stroke:var(--misss)}svg .node.st-external rect{fill:var(--ext);stroke:var(--exts)}
svg .node.st-run rect{stroke:var(--run);stroke-width:2.5}svg .node.st-refuted rect{stroke:var(--warn);stroke-width:2.5}svg .node.st-notrun rect{stroke-dasharray:3 2}
svg .node.prop rect{stroke:var(--fg);stroke-width:2.6;stroke-dasharray:6 3}
svg .node{cursor:pointer}svg .node:focus{outline:none}svg .node:focus rect,svg .node.sel rect{stroke-width:3.4}
svg .node.dim{opacity:.22}svg .lbl{font:11.5px system-ui,sans-serif;fill:var(--fg)}svg .sub{font:9px ui-monospace,monospace;fill:var(--muted)}
svg .edge{fill:none;stroke:var(--muted);stroke-width:1.1;opacity:.45}svg .edge.lit{stroke:var(--accent);stroke-width:2.2;opacity:1}
.pg svg{display:block;max-width:none;height:auto}
.outline ul.tree,.outline ul{list-style:none;margin:0;padding-left:12px}.outline ul.tree{padding-left:0}.outline li{margin:4px 0}
.outline a{color:var(--fg);text-decoration:none}.outline summary{cursor:pointer}
.outline .ok-exists{border-left:4px solid var(--exs);padding-left:4px}.outline .ok-missing{border-left:4px solid var(--misss);padding-left:4px}
.outline .ok-external{border-left:4px solid var(--exts);padding-left:4px}.outline .ok-run{border-left:4px double var(--run);padding-left:4px}
.outline .prop{font-weight:600}
ul.wiring{display:none;list-style:none;padding:0}ul.wiring li{border-top:1px solid var(--line);padding:6px 0;font-size:.9rem}ul.wiring a{color:var(--fg)}
@media (max-width:700px){ul.wiring{display:block}}
.small,.box p{overflow-wrap:anywhere}
svg .pw{fill:none;stroke:var(--fg);stroke-width:1.3;opacity:.75}svg .pw.amb{stroke-dasharray:5 3}svg .pah{fill:var(--fg)}
svg .pwl{font:600 11px ui-monospace,monospace;fill:var(--fg);paint-order:stroke;stroke:var(--box);stroke-width:4px}
svg .pnode rect{fill:var(--bg);stroke-width:1.3;stroke-dasharray:5 3}svg .pnode.prop rect{stroke-width:2.4;stroke-dasharray:none}
svg .pnode{cursor:pointer}svg .pcl{font:700 10.5px system-ui,sans-serif}svg .pfn{font:11.5px ui-monospace,monospace;fill:var(--fg)}
svg .pc0 rect,svg rect.pc0{stroke:#1d4ed8}svg .pc0 .pcl,svg rect.pport.pc0{fill:#1d4ed8}
svg .pc1 rect,svg rect.pc1{stroke:#c2410c}svg .pc1 .pcl,svg rect.pport.pc1{fill:#c2410c}
svg .pc2 rect,svg rect.pc2{stroke:#6b6b6b}svg .pc2 .pcl,svg rect.pport.pc2{fill:#6b6b6b}
svg .pc3 rect,svg rect.pc3{stroke:#7c3aed}svg .pc3 .pcl,svg rect.pport.pc3{fill:#7c3aed}
@media (prefers-color-scheme:dark){svg .pc0 rect,svg rect.pc0{stroke:#8ab4ff}svg .pc0 .pcl,svg rect.pport.pc0{fill:#8ab4ff}svg .pc1 rect,svg rect.pc1{stroke:#ffa463}svg .pc1 .pcl,svg rect.pport.pc1{fill:#ffa463}svg .pc3 rect{stroke:#b69cff}svg .pc3 .pcl{fill:#b69cff}}
svg .pext{stroke:var(--muted);stroke-dasharray:2 2}svg .pel{font:10px ui-monospace,monospace;fill:var(--muted)}
</style>"""

DERIVATION_JS = r"""<script>
(function(){
const M=JSON.parse(document.getElementById('model').textContent);
const svg=document.getElementById('g'), insp=document.getElementById('insp');
const NS='http://www.w3.org/2000/svg';
// Boxes grow to hold their whole text: no label on this page is ever shortened.
const colW=210, gapX=34, gapY=10, padTop=46, lineH=14, subH=11, CH=31, SUBCH=36;
M.nodes.forEach(n=>{n.lines=wrap(n.label,CH);n.subl=wrap(n.id+' · '+n.mark,SUBCH);n.h=12+n.lines.length*lineH+4+n.subl.length*subH;});
const cols=M.layers.map((_,i)=>M.nodes.filter(n=>n.layer===i));
const used=cols.map((c,i)=>c.length?i:-1).filter(i=>i>=0);
const colH=c=>c.reduce((s,n)=>s+n.h+gapY,0)-gapY;
const maxH=Math.max(...used.map(li=>colH(cols[li])));
const H=padTop+maxH+10, W=used.length*(colW+gapX);
svg.setAttribute('viewBox',`0 0 ${W} ${H}`); svg.style.width='100%'; svg.style.minWidth=Math.min(1100,W)+"px"; svg.style.height='auto';
const layerOf=Object.fromEntries(M.nodes.map(n=>[n.id,n.layer]));
const kindInto={};M.edges.forEach(e=>{const l=layerOf[e.to];(kindInto[l]=kindInto[l]||new Set()).add(e.kind);});
const pos={};
used.forEach((li,i)=>{const c=cols[li];let y=padTop+(maxH-colH(c))/2;
  c.forEach(n=>{pos[n.id]={x:i*(colW+gapX),y,h:n.h};y+=n.h+gapY;});
  const t=el('text',{x:i*(colW+gapX),y:16,class:'lay'}); t.textContent=M.layers[li]; svg.appendChild(t);
  if(kindInto[li]){const k=el('text',{x:i*(colW+gapX),y:31,class:'rel'}); k.textContent='lines in: '+[...kindInto[li]].join(', '); svg.appendChild(k);}});
function el(tag,attrs){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);return e;}
const up={},down={};
M.edges.forEach(e=>{(down[e.from]=down[e.from]||[]).push(e.to);(up[e.to]=up[e.to]||[]).push(e.from);});
const edgeEls=[];
M.edges.forEach(e=>{const a=pos[e.from],b=pos[e.to];if(!a||!b)return;
  const x1=a.x+colW,y1=a.y+a.h/2,x2=b.x,y2=b.y+b.h/2,mx=(x1+x2)/2;
  const p=el('path',{d:`M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`,class:'edge','data-from':e.from,'data-to':e.to});
  const ti=el('title',{});ti.textContent=`${e.from} → ${e.to}: ${e.kind}`;p.appendChild(ti);svg.appendChild(p);edgeEls.push(p);});
const nodeEls={};
M.nodes.forEach(n=>{const p=pos[n.id];const g=el('g',{class:'node st-'+n.state+(n.proposed?' prop':''),transform:`translate(${p.x},${p.y})`,tabindex:'0',role:'button','data-id':n.id});
  g.appendChild(el('rect',{width:colW,height:n.h,rx:6}));
  n.lines.forEach((ln,i)=>{const t=el('text',{x:8,y:16+i*lineH,class:'lbl'});t.textContent=ln;g.appendChild(t);});
  n.subl.forEach((ln,i)=>{const t=el('text',{x:8,y:16+n.lines.length*lineH+2+i*subH,class:'sub'});t.textContent=ln;g.appendChild(t);});
  g.addEventListener('click',()=>select(n.id,true));g.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();select(n.id,true);}});
  svg.appendChild(g);nodeEls[n.id]=g;});
// Every word kept; a word longer than a line (a path, an id) is split across lines, never dropped.
function wrap(str,n){const words=[];String(str).split(' ').forEach(w=>{while(w.length>n){words.push(w.slice(0,n));w=w.slice(n);}if(w)words.push(w);});
  const out=[];let cur='';for(const w of words){if(cur&&(cur+' '+w).length>n){out.push(cur);cur=w;}else cur=cur?cur+' '+w:w;}if(cur)out.push(cur);return out.length?out:[''];}
function chain(id){const s=new Set([id]);const walk=(m,x)=>{(m[x]||[]).forEach(y=>{if(!s.has(y)){s.add(y);walk(m,y);}});};walk(up,id);walk(down,id);return s;}
function select(id,scroll){const n=M.nodes.find(x=>x.id===id);if(!n)return;const s=chain(id);
  Object.entries(nodeEls).forEach(([k,g])=>{g.classList.toggle('dim',!s.has(k));g.classList.toggle('sel',k===id);});
  edgeEls.forEach(p=>p.classList.toggle('lit',s.has(p.dataset.from)&&s.has(p.dataset.to)));
  let h=`<p class='small'>${M.layers[n.layer]}${n.proposed?' · added or changed by this proposal':''}</p><h3>${esc(n.full)}</h3>`;
  const ex=Object.keys(n.extra).filter(k=>Array.isArray(n.extra[k])?n.extra[k].length:n.extra[k]);
  const val=v=>Array.isArray(v)?`<ul class='pts'>${v.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:esc(v);
  if(ex.length)h+=`<ul class='pts'>${ex.map(k=>`<li><strong>${esc(k)}:</strong> ${val(n.extra[k])}</li>`).join('')}</ul>`;
  const kind=(a,b)=>(M.edges.find(e=>e.from===a&&e.to===b)||{}).kind||'';
  const upN=(up[id]||[]),dnN=(down[id]||[]);
  if(upN.length)h+=`<p class='small'><strong>Comes from</strong></p><ul class='pts small'>${upN.map(u=>`<li>${link(u)} <span class='id'>(${esc(kind(u,id))})</span></li>`).join('')}</ul>`;
  if(dnN.length)h+=`<p class='small'><strong>Leads to</strong></p><ul class='pts small'>${dnN.map(d=>`<li>${link(d)} <span class='id'>(${esc(kind(id,d))})</span></li>`).join('')}</ul>`;
  h+=`<p class='small'>Source: <code>.aes/target.yaml</code> id <code>${esc(id)}</code></p>`;
  insp.innerHTML=h;insp.querySelectorAll('a[data-id]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();select(a.dataset.id,true);}));
  if(scroll&&window.innerWidth<900)insp.scrollIntoView({block:'nearest'});}
function link(id){return `<a href='#' data-id='${id}'>${esc(id)}</a>`;}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
// Phone: a drawing 1000px wide does not beat a list at 390px, so show the same chains as a nested outline
// (same ids, same marks, same inspector) and keep the drawing one tap away.
if(window.matchMedia('(max-width:700px)').matches){
  const wrapEl=svg.parentElement, view=wrapEl.parentElement;
  const ol=document.createElement('div');ol.className='outline';
  const byId=Object.fromEntries(M.nodes.map(n=>[n.id,n]));
  const item=(id,depth,seen)=>{const n=byId[id];const kids=(down[id]||[]).filter(k=>!seen.has(k));
    const lab=`<span class='ok-${n.state}${n.proposed?' prop':''}'>${esc(n.label)}</span> <span class='id'>${esc(n.id)} · ${esc(n.mark)}</span>`;
    if(!kids.length||depth>6)return `<li><a href='#' data-id='${esc(id)}'>${lab}</a></li>`;
    const s2=new Set([...seen,id]);
    return `<li><details${depth<1?' open':''}><summary><a href='#' data-id='${esc(id)}'>${lab}</a> <span class='id'>(${kids.length})</span></summary><ul>${kids.map(k=>item(k,depth+1,s2)).join('')}</ul></details></li>`;};
  ol.innerHTML=`<ul class='tree'>${M.nodes.filter(n=>n.layer===0).map(n=>item(n.id,0,new Set())).join('')}</ul>`;
  ol.querySelectorAll('a[data-id]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();select(a.dataset.id,true);}));
  const d=document.createElement('details');d.innerHTML='<summary class="small">Show the drawing (wide: it scrolls sideways)</summary>';
  view.insertBefore(ol,wrapEl);view.insertBefore(d,wrapEl);d.appendChild(wrapEl);
}
document.addEventListener('DOMContentLoaded',()=>{
document.querySelectorAll('a.pfl').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();select(a.dataset.id,true);}));
if(window.matchMedia('(max-width:700px)').matches){document.querySelectorAll('.pg').forEach(pg=>{const d=document.createElement('details');d.innerHTML='<summary class="small">Show the drawing (wide: it scrolls sideways)</summary>';pg.parentElement.insertBefore(d,pg);d.appendChild(pg);});}
document.querySelectorAll('.pnode').forEach(g=>{const go=()=>select(g.dataset.id,true);g.addEventListener('click',go);g.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();go();}});});
});
const first=M.nodes.find(n=>n.layer===0&&n.proposed)||M.nodes.find(n=>n.layer===0);if(first)select(first.id,false);
})();
</script>"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--decision", type=Path, help="markdown file whose text is shown as the pending human decision")
    ap.add_argument("--proposal", type=Path, help="render the target this proposal would leave, limited to what it touches")
    ap.add_argument("--review-points", type=Path, help="YAML with review_points: [{id,title,entrypoint,try,covers,render_check}]")
    ap.add_argument("--elk", type=Path, help="elkjs lib/elk.bundled.js, for the port graph layout")
    a = ap.parse_args(argv)
    decision = a.decision.read_text() if a.decision else None
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(render(a.root.resolve(), decision, a.proposal and a.proposal.resolve(), a.review_points, a.elk))
    print(a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
