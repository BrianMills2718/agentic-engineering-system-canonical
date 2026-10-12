#!/usr/bin/env python3
"""Build the eight-layer mapping review page from layers.json.

Writes agent-model-eight-layers.html: one static page, no external
dependencies. Fails if any agent-model section is missing from every layer.
"""
from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "layers.json").read_text())
OUT = HERE / "agent-model-eight-layers.html"

EW_REPO = "https://github.com/BrianMills2718/epistemic-warrant/blob"
O2A_REPO = "https://github.com/BrianMills2718/observation-to-action-metamodel/blob"
EW_REV = DATA["revisions"]["epistemic-warrant"]
O2A_REV = DATA["revisions"]["observation-to-action-metamodel"]
SPEC_URL = f"{O2A_REPO}/{O2A_REV}/formal/SPEC.md"

STATUS = {
    "used": ("Used", "The agent model already relies on this."),
    "partly": ("Partly used", "Cited or used for one piece only."),
    "unused": ("Not used", "Worked out upstream; the agent model never cites it."),
    "rebuilt": ("Rebuilt locally", "The agent model wrote its own version instead of using this one."),
    "tension": ("Conflicts", "Something in the agent model contradicts this decision."),
}
ORDER = ["used", "partly", "unused", "rebuilt", "tension"]


def check_coverage() -> None:
    covered = {m["sec"] for layer in DATA["layers"] for m in layer["model"]}
    missing = [s for s in DATA["spec_sections"] if s not in covered]
    unknown = sorted(covered - set(DATA["spec_sections"]))
    if missing or unknown:
        raise SystemExit(f"coverage error: missing={missing} unknown={unknown}")
    for layer in DATA["layers"]:
        for w in layer["worked"]:
            if w["status"] not in STATUS:
                raise SystemExit(f"unknown status {w['status']!r} in {layer['id']}")


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def chip(layer_id: str, idx: int, w: dict) -> str:
    label, _ = STATUS[w["status"]]
    tip = f"{label}: {w['text']}"
    return (
        f'<button class="chip s-{w["status"]}" data-key="{layer_id}:{idx}" '
        f'data-tip="{esc(tip)}" aria-label="{esc(w["ref"] + " — " + label)}">'
        f'<span class="mark" aria-hidden="true"></span>'
        f'<span class="ref">{esc(w["ref"])}</span>'
        f'<span class="stxt">{esc(label)}</span></button>'
    )


def build() -> str:
    check_coverage()
    counts = Counter(w["status"] for l in DATA["layers"] for w in l["worked"])
    total = sum(counts.values())
    details = {}
    rows = []
    for layer in DATA["layers"]:
        lc = Counter(w["status"] for w in layer["worked"])
        bar = "".join(
            f'<span class="seg s-{s}" style="flex:{lc[s]}"></span>' for s in ORDER if lc[s]
        )
        secs = "".join(
            f'<li><button class="sec" data-tip="{esc(m["text"])}">'
            f'<b>{esc(m["sec"])}</b> {esc(m["text"])}</button></li>'
            for m in layer["model"]
        )
        chips = "".join(chip(layer["id"], i, w) for i, w in enumerate(layer["worked"]))
        for i, w in enumerate(layer["worked"]):
            details[f"{layer['id']}:{i}"] = {
                "layer": layer["name"],
                "ref": w["ref"],
                "text": w["text"],
                "status": STATUS[w["status"]][0],
                "statusKey": w["status"],
                "note": w["note"],
                "url": f"{EW_REPO}/{EW_REV}/{w['path']}",
                "path": w["path"],
            }
        unused = lc["unused"]
        rows.append(
            f'<tr id="row-{layer["id"]}"><th scope="row"><div class="lname">{esc(layer["name"])}</div>'
            f'<div class="plain">{esc(layer["plain"])}</div>'
            f'<div class="bar" data-tip="{esc(f"{unused} of {len(layer["worked"])} worked-out items not used")}" tabindex="0">{bar}</div></th>'
            f'<td data-label="In the agent model"><ul class="secs">{secs}</ul></td>'
            f'<td data-label="Already worked out in epistemic-warrant"><div class="chips">{chips}</div></td></tr>'
        )
    summary = "".join(
        f'<button class="sum s-{s}" data-filter="{s}" data-tip="{esc(STATUS[s][1])} Click to highlight.">'
        f'<span class="mark" aria-hidden="true"></span><b>{counts[s]}</b> {esc(STATUS[s][0])}</button>'
        for s in ORDER
    )
    return TEMPLATE.format(
        rows="".join(rows),
        summary=summary,
        total=total,
        unused=counts["unused"],
        ew=EW_REV[:8],
        o2a=O2A_REV[:8],
        spec_url=SPEC_URL,
        details=json.dumps(details).replace("</", "<\\/"),
    )


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agent Model Layers</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1f;--mute:#5d5d66;--line:#d9d6cf;--card:#fff;
--blue:#1f5fbf;--blue-soft:#d6e4fa;--orange:#c75b00;--orange-soft:#fde6d2;--grey:#8a8a93}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#141417;--fg:#ececf0;--mute:#a4a4ae;
--line:#33333a;--card:#1d1d22;--blue:#7fb0ff;--blue-soft:#1e3354;--orange:#ffa45c;--orange-soft:#4a2a10;--grey:#8d8d97}}}}
:root[data-theme="dark"]{{--bg:#141417;--fg:#ececf0;--mute:#a4a4ae;--line:#33333a;--card:#1d1d22;
--blue:#7fb0ff;--blue-soft:#1e3354;--orange:#ffa45c;--orange-soft:#4a2a10;--grey:#8d8d97}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}}
main{{max-width:1280px;margin:0 auto;padding:20px 16px 80px}}
h1{{font-size:22px;margin:0 0 6px}}
.lede{{margin:0 0 4px;max-width:900px}}
.status{{color:var(--mute);font-size:13px;margin:0 0 14px}}
.status a{{color:inherit}}
.summary{{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 6px}}
.sum{{display:flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--card);color:var(--fg);
border-radius:8px;padding:6px 10px;font:inherit;cursor:pointer}}
.sum b{{font-size:17px}}
.sum[aria-pressed="true"]{{outline:2px solid var(--fg)}}
.legend{{color:var(--mute);font-size:13px;margin:0 0 16px}}
table{{width:100%;border-collapse:separate;border-spacing:0;background:var(--card);border:1px solid var(--line);border-radius:10px}}
thead th{{text-align:left;font-size:12px;color:var(--mute);padding:10px 12px;border-bottom:1px solid var(--line)}}
tbody th,tbody td{{vertical-align:top;padding:12px;border-bottom:1px solid var(--line);text-align:left}}
tbody tr:last-child>*{{border-bottom:0}}
tbody th{{width:26%;font-weight:normal}}
.lname{{font-weight:650;font-size:16px}}
.plain{{color:var(--mute);font-size:13px;margin:2px 0 8px}}
.bar{{display:flex;height:8px;border-radius:4px;overflow:hidden;background:var(--line);max-width:220px}}
.seg.s-used{{background:var(--blue)}} .seg.s-partly{{background:repeating-linear-gradient(90deg,var(--blue) 0 3px,var(--blue-soft) 3px 6px)}}
.seg.s-unused{{background:repeating-linear-gradient(90deg,var(--grey) 0 2px,transparent 2px 5px)}}
.seg.s-rebuilt,.seg.s-tension{{background:var(--orange)}}
.secs{{list-style:none;margin:0;padding:0}}
.sec{{all:unset;display:block;cursor:help;font-size:13px;padding:2px 0}}
.sec:focus-visible{{outline:2px solid var(--blue)}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}}
.chip{{display:inline-flex;align-items:center;gap:6px;font:inherit;font-size:13px;color:var(--fg);cursor:pointer;
border-radius:999px;padding:4px 10px;background:var(--card);border:1.5px solid var(--line);text-align:left}}
.chip .stxt{{color:var(--mute);font-size:11px}}
.mark{{width:12px;height:12px;border-radius:50%;flex:none;display:inline-block}}
.s-used .mark{{background:var(--blue);border:2px solid var(--blue)}}
.s-partly .mark{{background:linear-gradient(90deg,var(--blue) 50%,transparent 50%);border:2px solid var(--blue)}}
.s-unused .mark{{border:2px dashed var(--grey)}}
.s-rebuilt .mark,.s-tension .mark{{border:2px solid var(--orange);border-radius:2px;background:var(--orange-soft)}}
.chip.s-used{{border-color:var(--blue);background:var(--blue-soft)}}
.chip.s-unused{{border-style:dashed;border-color:var(--grey)}}
.chip.s-rebuilt,.chip.s-tension{{border-color:var(--orange);background:var(--orange-soft)}}
.chip.s-rebuilt .ref::before,.chip.s-tension .ref::before{{content:"⚠ "}}
.chip[aria-pressed="true"]{{outline:2px solid var(--fg)}}
body.filtering .chip{{opacity:.25}} body.filtering .chip.hit{{opacity:1}}
#tip{{position:fixed;z-index:20;max-width:320px;background:var(--fg);color:var(--bg);font-size:13px;padding:6px 9px;
border-radius:6px;pointer-events:none;opacity:0;transition:opacity .12s;box-shadow:0 4px 14px rgba(0,0,0,.2)}}
#tip.on{{opacity:1}}
#panel{{position:fixed;right:16px;bottom:16px;width:min(420px,calc(100vw - 32px));max-height:60vh;overflow:auto;
background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:0 10px 30px rgba(0,0,0,.18);display:none}}
#panel.on{{display:block}}
#panel h2{{font-size:16px;margin:0 0 4px}}
#panel .meta{{color:var(--mute);font-size:12px;margin-bottom:8px}}
#panel a{{color:var(--blue)}}
#close{{position:absolute;top:8px;right:10px;font:inherit;font-size:18px;background:none;border:0;color:var(--mute);cursor:pointer}}
.ask{{margin-top:22px;max-width:900px;border-left:4px solid var(--blue);padding:4px 12px}}
@media (max-width:700px){{
 table,thead,tbody,tr,th,td{{display:block;width:100%}}
 thead{{display:none}}
 tbody tr{{border-bottom:1px solid var(--line);padding:4px 0}}
 tbody th,tbody td{{border-bottom:0;padding:8px 12px;width:100%}}
 tbody td::before{{content:attr(data-label);display:block;font-size:11px;color:var(--mute);margin-bottom:4px}}
}}
</style></head><body>
<main>
<h1>The agent model leaves most of the eight-layer work unused</h1>
<p class="lede">Each row is one layer of the canonical factorization from epistemic-warrant. The middle column is where the
agent model (o2a <a href="{spec_url}">formal/SPEC.md</a>) touches that layer. The right column is what epistemic-warrant
already worked out for it, and whether the agent model uses it. <b>{unused} of {total}</b> worked-out items are not used.</p>
<p class="status">Sources: epistemic-warrant at <code>{ew}</code>, agent model at <code>{o2a}</code> (both 2026-10-12).
Tap any item for its note and a link to the file.</p>
<div class="summary" role="group" aria-label="Filter by status">{summary}</div>
<p class="legend">Key: filled blue dot = used; half blue = partly used; dashed grey = not used;
orange square with ⚠ = rebuilt locally or conflicts. Words are always shown next to the mark.</p>
<table>
<thead><tr><th>Layer</th><th>In the agent model</th><th>Already worked out in epistemic-warrant</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="ask"><b>What this page asks you:</b> does the right column match the work you remember doing? If a layer is
missing something you worked out, say which. The next step rewrites the agent model on these eight layers, adopting
these items instead of the local versions.</div>
</main>
<div id="tip" role="tooltip"></div>
<aside id="panel" aria-live="polite"><button id="close" data-tip="Close the detail panel" aria-label="Close">×</button><div id="pbody"></div></aside>
<script>
const D={details};
const tip=document.getElementById('tip'),panel=document.getElementById('panel'),pbody=document.getElementById('pbody');
function show(el){{const t=el.getAttribute('data-tip');if(!t)return;tip.textContent=t;tip.classList.add('on');
const r=el.getBoundingClientRect();let x=Math.min(r.left,innerWidth-tip.offsetWidth-8),y=r.bottom+6;
if(y+tip.offsetHeight>innerHeight)y=r.top-tip.offsetHeight-6;tip.style.left=Math.max(8,x)+'px';tip.style.top=y+'px';}}
function hide(){{tip.classList.remove('on');}}
document.querySelectorAll('[data-tip]').forEach(el=>{{el.addEventListener('mouseenter',()=>show(el));el.addEventListener('mouseleave',hide);
el.addEventListener('focus',()=>show(el));el.addEventListener('blur',hide);}});
function esc(s){{return s.replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);}}
document.querySelectorAll('.chip').forEach(c=>c.addEventListener('click',()=>{{
 document.querySelectorAll('.chip[aria-pressed]').forEach(x=>x.removeAttribute('aria-pressed'));
 c.setAttribute('aria-pressed','true');const d=D[c.dataset.key];hide();
 pbody.innerHTML='<h2>'+esc(d.ref)+'</h2><div class="meta">'+esc(d.layer)+', '+esc(d.status)+'</div><p>'+esc(d.text)+'</p><p>'+esc(d.note)+
 '</p><p><a href="'+d.url+'" target="_blank" rel="noopener">Open '+esc(d.path)+'</a></p>';panel.classList.add('on');}}));
document.getElementById('close').addEventListener('click',()=>{{panel.classList.remove('on');hide();}});
let active=null;
document.querySelectorAll('.sum').forEach(b=>b.addEventListener('click',()=>{{
 const f=b.dataset.filter;active=active===f?null:f;
 document.querySelectorAll('.sum').forEach(x=>x.setAttribute('aria-pressed',x.dataset.filter===active));
 document.body.classList.toggle('filtering',!!active);
 document.querySelectorAll('.chip').forEach(c=>c.classList.toggle('hit',!!active&&c.classList.contains('s-'+active)));}}));
</script></body></html>
"""

if __name__ == "__main__":
    OUT.write_text(build())
    print(f"wrote {OUT.name}")
