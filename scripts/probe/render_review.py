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
body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif;max-width:1560px;margin-inline:auto}
h1{font-size:1.5rem;margin:.2em 0}h2{font-size:1.15rem;margin:1.6em 0 .4em;border-bottom:1px solid var(--line);padding-bottom:.2em}
.lede{color:var(--muted)}.box{background:var(--box);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:10px 0}
.decision{border-left:5px solid var(--warn)}table{border-collapse:collapse;width:100%;font-size:.92rem}th,td{border:1px solid var(--line);padding:6px 8px;vertical-align:top;text-align:left}
th{background:var(--box)}.ok{color:var(--ok);font-weight:600}.miss{color:var(--miss);font-weight:600}.id{font-family:ui-monospace,monospace;font-size:.85em;color:var(--muted)}
details>summary{cursor:pointer;color:var(--muted)}code{font-family:ui-monospace,monospace;font-size:.9em}.small{font-size:.85rem;color:var(--muted)}
ul{margin:.3em 0 .3em 1.2em}
.view{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:12px;align-items:start}
@media (max-width:900px){.view{grid-template-columns:1fr}}
.graphwrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--box);padding:6px}
.insp{border:1px solid var(--line);border-radius:8px;padding:10px 12px;position:sticky;top:8px;max-height:90vh;overflow:auto;background:var(--bg)}
.insp h3{margin:.2em 0 .4em;font-size:1.05rem}
.sw{display:inline-block;width:.9em;height:.9em;border-radius:3px;vertical-align:-2px;margin-right:3px;border:1px solid var(--line)}
.sw.ok{background:#bfe8c9}.sw.miss{background:#f6c5c1}.sw.ext{background:#e8ddb5}
@media (prefers-color-scheme:dark){.sw.ok{background:#245c34}.sw.miss{background:#6e2a25}.sw.ext{background:#5a4a1a}}
svg .lay{font:600 12px system-ui,sans-serif;fill:var(--muted)}
svg .node rect{fill:var(--box);stroke:var(--line);stroke-width:1.2}
svg .node.st-outcome rect{fill:#dbe7ff;stroke:#3b63c4}svg .node.st-rule rect{fill:var(--bg)}svg .node.st-criterion rect{fill:var(--bg)}
svg .node[class*='st-req'] rect{fill:var(--bg);stroke-dasharray:3 2}
svg .node.st-exists rect{fill:#bfe8c9;stroke:#1b7f3b}svg .node.st-missing rect{fill:#f6c5c1;stroke:#b3261e}svg .node.st-external rect{fill:#e8ddb5;stroke:#9a6700}
@media (prefers-color-scheme:dark){svg .node.st-outcome rect{fill:#1f3566;stroke:#7aa2ff}svg .node.st-exists rect{fill:#245c34}svg .node.st-missing rect{fill:#6e2a25}svg .node.st-external rect{fill:#5a4a1a}}
svg .node{cursor:pointer}svg .node:focus{outline:none}svg .node:focus rect,svg .node.sel rect{stroke-width:3}
svg .node.dim{opacity:.22}svg .lbl{font:11.5px system-ui,sans-serif;fill:var(--fg)}svg .sub{font:9px ui-monospace,monospace;fill:var(--muted)}
svg .edge{fill:none;stroke:var(--line);stroke-width:1.2;opacity:.55}svg .edge.lit{stroke:#3b63c4;stroke-width:2.2;opacity:1}
@media (prefers-color-scheme:dark){svg .edge.lit{stroke:#7aa2ff}}
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

    # ---- Linked derivation view (Representation Router: composite-linked-view, native-web)
    import json as _json
    nodes: list[dict] = []
    edges: list[tuple[str, str, str]] = []

    def short(text: str, n: int = 44) -> str:
        t = " ".join(text.split())
        return t if len(t) <= n else t[: n - 1].rstrip(" ,;:") + "…"

    for o in target.outcomes:
        nodes.append({"id": o.id, "layer": 0, "label": short(o.statement, 60), "state": "outcome",
                      "full": o.statement.strip(), "extra": {"for": o.actor_or_consumer, "why": (o.rationale or "").strip(), "not trying to do": "; ".join(o.non_goals or [])}})
    for n in target.normative_items:
        nodes.append({"id": n.id, "layer": 1, "label": short(n.statement), "state": "rule", "full": n.statement.strip(), "extra": {"kind": n.kind}})
        for ref in n.outcome_refs:
            edges.append((ref, n.id, "derived from"))
    for sc in target.success_criteria:
        nodes.append({"id": sc.id, "layer": 2, "label": short(sc.statement), "state": "criterion", "full": sc.statement.strip(),
                      "extra": {"what would disprove it": sc.disproof.strip()}})
        for ref in sc.target_refs:
            edges.append((ref, sc.id, "proves"))
        for er in sc.evidence_requirements:
            nodes.append({"id": er.id, "layer": 3, "label": short(er.requirement), "state": "req-" + er.kind, "full": er.requirement.strip(), "extra": {"kind of evidence": er.kind}})
            edges.append((sc.id, er.id, "needs evidence"))
    for vs in target.verification_subjects:
        loc = vs.locator
        if loc.startswith("external:"):
            st = "external"; ex = None
        else:
            ex = exists(loc); st = "exists" if ex else "missing"
        nodes.append({"id": vs.id, "layer": 4, "label": short(vs.purpose), "state": st,
                      "full": vs.purpose.strip(), "extra": {"proof kind": vs.proof_kind, "role": vs.proof_role, "where": loc,
                                                            "exists in repo": ("yes" if ex else "not yet") if ex is not None else "outside the repository"}})
        for er in vs.evidence_requirement_refs:
            edges.append((er, vs.id, "planned proof"))
        if not loc.startswith("external:") and loc in art_path.values():
            edges.append((vs.id, next(a for a, pth in art_path.items() if pth == loc), "lives in"))
    comp_of = {aid: c.id for c in target.components for aid in c.planned_artifact_refs}
    for a in target.planned_artifacts:
        ex = exists(a.locator.exact_path)
        nodes.append({"id": a.id, "layer": 5, "label": a.locator.exact_path, "state": "exists" if ex else "missing",
                      "full": a.purpose.strip(), "extra": {"path": a.locator.exact_path, "kind": a.kind, "component": comp_of.get(a.id, "(none)"), "exists in repo": "yes" if ex else "not yet"}})
        for ref in a.semantic_justification_refs:
            edges.append((ref, a.id, "justified by"))
    known = {n["id"] for n in nodes}
    edges = [e for e in edges if e[0] in known and e[1] in known]
    layers = ["Outcome", "Rules it must obey", "What counts as success", "Evidence each needs", "Planned proofs", "Files committed to"]
    model = {"nodes": nodes, "edges": [{"from": a, "to": b, "kind": k} for a, b, k in edges], "layers": layers}

    n_exists = sum(1 for n in nodes if n["state"] == "exists"); n_missing = sum(1 for n in nodes if n["state"] == "missing")
    n_ext = sum(1 for n in nodes if n["state"] == "external")
    w("<h2>2. How the outcome turns into proof and files</h2>")
    w(f"<p class='lede'>Read left to right. The outcome on the left is broken into rules, each rule into success conditions, each condition into the evidence it needs, each piece of evidence into a planned proof, and proofs into files. "
      f"<span class='sw ok'></span> exists in the repository ({n_exists}) · <span class='sw miss'></span> promised, not yet there ({n_missing}) · <span class='sw ext'></span> proof happens outside the repository, such as your own review or a live run ({n_ext}). "
      "Click anything to light up its whole chain and read the full text on the right (below, on a phone).</p>")
    w("<div class='view'><div class='graphwrap'><svg id='g' role='img' aria-label='derivation graph from outcome to files'></svg></div>"
      "<aside id='insp' class='insp'><p class='small'>Nothing selected. Click a box in the diagram.</p></aside></div>")
    w("<script id='model' type='application/json'>" + _json.dumps(model).replace("</", "<\\/") + "</script>")
    w(r"""<script>
(function(){
const M=JSON.parse(document.getElementById('model').textContent);
const svg=document.getElementById('g'), insp=document.getElementById('insp');
const NS='http://www.w3.org/2000/svg';
const colW=168, gapX=26, nodeH=50, gapY=9, padTop=30;
const cols=M.layers.map((_,i)=>M.nodes.filter(n=>n.layer===i));
const maxRows=Math.max(...cols.map(c=>c.length));
const H=padTop+maxRows*(nodeH+gapY)+10, W=M.layers.length*(colW+gapX);
svg.setAttribute('viewBox',`0 0 ${W} ${H}`); svg.style.width='100%'; svg.style.minWidth="1000px"; svg.style.height='auto';
const pos={};
cols.forEach((c,i)=>{const total=c.length*(nodeH+gapY)-gapY; const y0=padTop+(maxRows*(nodeH+gapY)-gapY-total)/2;
  c.forEach((n,j)=>{pos[n.id]={x:i*(colW+gapX),y:y0+j*(nodeH+gapY)};});
  const t=el('text',{x:i*(colW+gapX),y:20,class:'lay'}); t.textContent=M.layers[i]; svg.appendChild(t);});
function el(tag,attrs){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);return e;}
const up={},down={};
M.edges.forEach(e=>{(down[e.from]=down[e.from]||[]).push(e.to);(up[e.to]=up[e.to]||[]).push(e.from);});
const edgeEls=[];
M.edges.forEach(e=>{const a=pos[e.from],b=pos[e.to];if(!a||!b)return;
  const x1=a.x+colW,y1=a.y+nodeH/2,x2=b.x,y2=b.y+nodeH/2,mx=(x1+x2)/2;
  const p=el('path',{d:`M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`,class:'edge','data-from':e.from,'data-to':e.to});
  const ti=el('title',{});ti.textContent=`${e.from} → ${e.to}: ${e.kind}`;p.appendChild(ti);svg.appendChild(p);edgeEls.push(p);});
const nodeEls={};
M.nodes.forEach(n=>{const p=pos[n.id];const g=el('g',{class:'node st-'+n.state,transform:`translate(${p.x},${p.y})`,tabindex:'0',role:'button','data-id':n.id});
  g.appendChild(el('rect',{width:colW,height:nodeH,rx:6}));
  const lines=wrap(n.label,25);
  lines.forEach((ln,i)=>{const t=el('text',{x:7,y:15+i*13,class:'lbl'});t.textContent=ln;g.appendChild(t);});
  const s=el('text',{x:7,y:44,class:'sub'});s.textContent=n.id;g.appendChild(s);
  g.addEventListener('click',()=>select(n.id));g.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();select(n.id);}});
  svg.appendChild(g);nodeEls[n.id]=g;});
function wrap(str,n){const words=str.split(' ');const out=[];let cur='';for(const w of words){if((cur+' '+w).trim().length>n){if(cur)out.push(cur);cur=w;}else cur=(cur+' '+w).trim();}if(cur)out.push(cur);if(out.length>2){out.length=2;out[1]=out[1].slice(0,n-1)+'…';}return out;}
function chain(id){const s=new Set([id]);const walk=(m,x)=>{(m[x]||[]).forEach(y=>{if(!s.has(y)){s.add(y);walk(m,y);}});};walk(up,id);walk(down,id);return s;}
function select(id){const s=chain(id);
  Object.entries(nodeEls).forEach(([k,g])=>{g.classList.toggle('dim',!s.has(k));g.classList.toggle('sel',k===id);});
  edgeEls.forEach(p=>p.classList.toggle('lit',s.has(p.dataset.from)&&s.has(p.dataset.to)));
  const n=M.nodes.find(x=>x.id===id);
  let h=`<p class='small'>${M.layers[n.layer]}</p><h3>${esc(n.label)}</h3><p>${esc(n.full)}</p>`;
  for(const k in n.extra){if(n.extra[k])h+=`<p><strong>${esc(k)}:</strong> ${esc(n.extra[k])}</p>`;}
  const upN=(up[id]||[]),dnN=(down[id]||[]);
  if(upN.length)h+=`<p class='small'><strong>comes from:</strong> ${upN.map(link).join(', ')}</p>`;
  if(dnN.length)h+=`<p class='small'><strong>leads to:</strong> ${dnN.map(link).join(', ')}</p>`;
  h+=`<p class='small'>Source: <code>.aes/target.yaml</code> id <code>${esc(id)}</code></p>`;
  insp.innerHTML=h;insp.querySelectorAll('a[data-id]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();select(a.dataset.id);}));
  if(window.innerWidth<900)insp.scrollIntoView({behavior:'smooth',block:'nearest'});}
function link(id){return `<a href='#' data-id='${id}'>${esc(id)}</a>`;}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
const first=M.nodes.find(n=>n.layer===0);if(first)select(first.id);
})();
</script>""")
    # Orphans under governed roots
    orphans = sorted(f for f in tracked if any(f.startswith(r) for r in project.governed_roots) and f not in {a.locator.exact_path for a in target.planned_artifacts})
    w("<h2>3. Files under governed roots that nobody planned</h2>")
    if orphans:
        w("<p class='miss'>These files exist under a governed root but are not planned artifacts. Each one is a topology violation until it is planned or removed.</p><ul>")
        for f in orphans:
            w(f"<li><code>{E(f)}</code></li>")
        w("</ul>")
    else:
        w("<p class='ok'>None. Every tracked file under " + ", ".join(f"<code>{E(r)}</code>" for r in project.governed_roots) + " is a planned artifact.</p>")

    w("<h2>4. Where this comes from</h2><p class='small'>Governed roots: " + ", ".join(f"<code>{E(r)}</code>" for r in project.governed_roots) +
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
