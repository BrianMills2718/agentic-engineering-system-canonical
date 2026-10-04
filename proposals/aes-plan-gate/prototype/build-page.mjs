// Compose shaping.html from the generated diagrams (no diagram is drawn by hand here).
import fs from 'node:fs';
const read = (p) => fs.readFileSync(p, 'utf8');
const strip = (svg) => svg.replace(/<\?xml[^>]*>/, '');
const ports = strip(read('out/gate-plan-ports.svg'));
const draft = strip(read('out/gate-draft1-ports.svg'));
const struct = strip(read('out/aes-current-structure.svg'));
const traceHtml = read('out/aes-current-trace.html').match(/<table[\s\S]*<\/table>/)[0];
const model = JSON.parse(read('gate-plan.json'));
const nodes = {};
for (const c of model.components) for (const e of c.exports.filter((x) => x.typed)) {
  const id = `${c.id}.${e.name}`;
  nodes[id] = {
    comp: c.id.replace('RU-AES-', '').toLowerCase().replace(/(^|-)\w/g, (x) => x.toUpperCase()).replace(/-/g, ' '),
    sig: `${e.name}(${e.args.map(([a, t]) => `${a}: ${t}`).join(', ')}) -> ${e.ret}`,
    file: c.files.join(', '), isNew: c.new,
    from: model.wires.filter((w) => w.to === c.id && w.to_port === e.name).map((w) => `${w.from_port} (${w.label})`),
    to: model.wires.filter((w) => w.from === c.id && w.from_port === e.name).map((w) => w.to_port),
  };
}
const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AES Plan Gate</title>
<style>
:root{--bg:#ffffff;--fg:#0f172a;--muted:#475569;--line:#e2e8f0;--card:#f8fafc;--accent:#1d4ed8;--warn:#c2410c;--diagram:#ffffff}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0b1120;--fg:#e2e8f0;--muted:#94a3b8;--line:#1e293b;--card:#111827;--accent:#93c5fd;--warn:#fdba74;--diagram:#f8fafc}}
:root[data-theme="dark"]{--bg:#0b1120;--fg:#e2e8f0;--muted:#94a3b8;--line:#1e293b;--card:#111827;--accent:#93c5fd;--warn:#fdba74;--diagram:#f8fafc}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:720px;margin:0 auto;padding:14px 16px 48px}
h1{font-size:21px;line-height:1.25;margin:4px 0 6px}
h2{font-size:16px;margin:26px 0 6px}
p{margin:6px 0}
.status{font-size:12px;color:var(--muted);border-left:3px solid var(--line);padding-left:8px;margin:8px 0 14px}
.fig{background:var(--diagram);border:1px solid var(--line);border-radius:10px;padding:6px;margin:8px 0}
.fig{overflow-x:auto}.fig svg{width:100%;height:auto;display:block}#ports svg{min-width:540px}.swipe{font-size:12px;color:var(--muted);margin:2px 0}
.legend{font-size:12.5px;color:var(--muted);margin:4px 0 0;padding-left:18px}
.legend li{margin:2px 0}
.callout{border-left:3px solid var(--warn);background:var(--card);padding:8px 10px;border-radius:0 8px 8px 0;font-size:14px;margin:10px 0}
#detail{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 10px;font-size:13px;margin-top:8px}
#detail code{font-size:12px;word-break:break-word}
ol,ul{padding-left:20px;margin:6px 0}
li{margin:4px 0}
.rp1{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.rp1 code,.cmd{font-family:ui-monospace,Menlo,monospace;font-size:12.5px}
.cmd{display:block;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:6px 8px;overflow-x:auto;white-space:pre}
details{border-top:1px solid var(--line);padding:8px 0}
summary{cursor:pointer;font-weight:600}
.t{border-collapse:collapse;font-size:12.5px;width:100%}.t td,.t th{border-top:1px solid var(--line);padding:6px 4px;text-align:left;vertical-align:top}
.fnode{cursor:pointer}.fnode:focus{outline:none}.fnode.sel rect{stroke-width:3.5!important}
.rec{font-size:14px}.rec b{display:block}
</style></head>
<body><main>
<h1>Plan gate: should AES refuse plans you can't see?</h1>
<p>The proposed rule: <b>a plan is not accepted until AES can draw it from its own data, and it names 2–4 review points you can open on your phone.</b> Below is the gate's own plan, drawn by that rule.</p>
<div class="status">Generated 2026-10-04 from proposal PLAN-AES-PLAN-GATE (draft, not accepted, nothing built) on AES main at b9a708d. <code>aes plan validate</code>: OK, 16 additions, 2 changes. No diagram here was drawn by hand.</div>

<h2>What data passes between the new steps</h2>
<div class="fig" id="ports">${ports}</div>
<div class="swipe">Swipe the drawing sideways to see all of it. It stays at a readable size.</div>
<div id="detail" aria-live="polite">Tap a box in the drawing.</div>
<ul class="legend">
<li>Each box is one planned function; the small coloured label is the part of AES it lives in. Solid border = new part; dashed = existing part being changed.</li>
<li>A wire means one function's <i>output type</i> is another's <i>input</i>; the bold text on the wire is that type.</li>
<li>Grey stubs are inputs nothing in the plan makes (a file path, for example); they come from outside.</li>
<li>Tap a box to see its full signature.</li>
</ul>
<div class="callout"><b>The drawing caught a gap in the plan's first draft.</b> <code>render_check</code> needed a <code>ReviewPoint</code>, and no planned function made one. In the drawing that showed up as a loose stub. A new function, <code>review_points_of</code>, now makes it. The gate would turn that loose stub into a refusal.
<details><summary>See the first draft</summary><div class="fig">${draft}</div></details></div>

<h2>What the gate refuses</h2>
<ol>
<li>A new or changed source file whose functions have no typed signatures, because then there is nothing to draw ports from.</li>
<li>A new part with no wire to any other part.</li>
<li>Fewer than 2 or more than 4 review points, or a review point without a link or command, three things to try, and a phone-width screenshot check.</li>
<li>A custom visualization link whose Representation Router files are missing.</li>
</ol>

<h2>Review points</h2>
<ol>
<li><b>See a plan as pictures.</b> Any proposal opens as this page: the port graph, the structure view, and the review points.</li>
<li><b>Watch the gate say no.</b> Four broken example plans are each refused with the exact entry named. The screenshot check fails a blank page and an error page.</li>
<li><b>A real plan, from your phone.</b> The next real AES plan comes to your Telegram as a link. You approve it from the pictures alone.</li>
</ol>

<h2>At review point 1 you would</h2>
<div class="rp1">
<span class="cmd">aes plan diagrams proposals/aes-plan-gate/PLAN-AES-PLAN-GATE.yaml --publish</span>
<p>An agent runs this for you and sends a private link to your phone. Then:</p>
<ol>
<li>Tap <code>bundle</code>. Check that its three inputs are the three drawings, and that both the writer and the checker take its output.</li>
<li>Ask the agent to delete <code>review_points_of</code> from the plan and reload. A loose stub appears on <code>render_check</code>, and <code>aes plan validate</code> names it as a refusal.</li>
<li>Open "Which part uses which" for all of AES (below) and find the two orange pairs that depend on each other.</li>
</ol>
<p style="font-size:12.5px;color:var(--muted)">Automatic check before you get the link: a 390 px screenshot that must not be blank, an error page, or a page that throws a script error. This page passed it today. Blank, stack-trace and script-error test pages failed it, as they should.</p>
</div>

<details><summary>Bigger picture: which part of AES uses which today</summary>
<p style="font-size:13px">Drawn from AES's current plan and its code. The orange pairs depend on each other in both directions: Planning and Reconcile, and Records and Characterize. A list would not show this. Records is used by nine parts and the command line uses nine, so their arrows are folded into the box text.</p>
<div class="fig">${struct}</div></details>

<details><summary>Criteria and how each is proved (a table, not a drawing)</summary>
<p style="font-size:13px">This chain is almost one-to-one, so a drawing would add nothing. The gate generates it as a table.</p>${traceHtml}</details>

<details open><summary>Your calls (each has a safe default)</summary>
<ul class="rec">
<li><b>Build review point 1 first, alone.</b> It is the drawing generator plus this page, about half a day of work, and useful before the gate refuses anything. Default if you don't answer: yes.</li>
<li><b>Send review-point pages as private links, not local addresses.</b> A private link opens on your phone with no setup. Default: private links.</li>
<li><b>Turn the gate on for AES first, then whygame5.</b> Other projects stay unaffected until it has caught a real gap in a real plan. Default: yes.</li>
</ul></details>
</main>
<script>
const N=${JSON.stringify(nodes)};
const d=document.getElementById('detail');
function show(g){document.querySelectorAll('.fnode.sel').forEach(x=>x.classList.remove('sel'));g.classList.add('sel');
const n=N[g.dataset.id];if(!n)return;
d.innerHTML='<b>'+n.comp+(n.isNew?' (new)':' (existing, changed)')+'</b> · '+n.file+'<br><code>'+n.sig.replace(/</g,'&lt;')+'</code><br>'+
'Gets from: '+(n.from.length?n.from.join(', '):'outside the plan')+'<br>Feeds: '+(n.to.length?n.to.join(', '):'nothing; this is an end result');}
document.querySelectorAll('#ports .fnode').forEach(g=>{g.addEventListener('click',()=>show(g));g.addEventListener('keydown',e=>{if(e.key==='Enter')show(g)})});
</script>
</body></html>`;
fs.writeFileSync('shaping.html', html);
console.log('shaping.html', html.length, 'bytes');
