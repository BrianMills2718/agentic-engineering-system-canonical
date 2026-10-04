// Throwaway prototype: model.json -> generated diagrams, phone-width.
//   structure: UML-component-style dependency view (Mermaid text -> SVG), cycles highlighted
//   ports:     function-level port graph from typed export signatures (ELK layout -> SVG)
//   trace:     component -> criterion -> proof route as a TABLE (a graph adds nothing here)
// Usage: node render.mjs <model.json> <out-prefix> structure|ports|trace [...]
import fs from 'node:fs';
import path from 'node:path';
import ELK from 'elkjs/lib/elk.bundled.js';
import { chromium } from 'playwright';

const [, , modelPath, outPrefix, ...kinds] = process.argv;
const m = JSON.parse(fs.readFileSync(modelPath, 'utf8'));
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const nice = (id) => id.replace('RU-AES-', '').toLowerCase().replace(/(^|-)\w/g, (x) => x.toUpperCase()).replace(/-/g, ' ');
const sid = (s) => s.replace(/[^A-Za-z0-9]/g, '_');

// ---------------- structure (Mermaid) ----------------
function structure() {
  const pairs = new Map();
  for (const w of m.wires) {
    if (w.label.startsWith('_') || w.from === w.to) continue;
    const k = `${w.from}>${w.to}`;
    pairs.set(k, (pairs.get(k) || 0) + 1);
  }
  const has = (a, b) => pairs.has(`${a}>${b}`);
  const ids = m.components.map((c) => c.id);
  // hubs: a component everyone uses / that uses everyone gets a note instead of N arrows
  const usedBy = (id) => ids.filter((o) => o !== id && has(id, o));
  const uses = (id) => ids.filter((o) => o !== id && has(o, id));
  const big = Math.max(4, Math.ceil(ids.length * 0.6));
  const sinks = ids.filter((id) => usedBy(id).length >= big); // e.g. Records
  const tops = ids.filter((id) => uses(id).length >= big); // e.g. CLI
  const L = ['flowchart TB',
    'classDef hub fill:#eff6ff,stroke:#1d4ed8,stroke-width:2px;',
    'classDef new fill:#fff7ed,stroke:#c2410c,stroke-width:3px;',
    'classDef cyc fill:#fff7ed,stroke:#c2410c,stroke-width:2px,stroke-dasharray:6 3;'];
  const inCycle = new Set();
  for (const k of pairs.keys()) { const [a, b] = k.split('>'); if (has(b, a)) { inCycle.add(a); inCycle.add(b); } }
  for (const c of m.components) {
    let sub = `${c.files.length} file${c.files.length === 1 ? '' : 's'}`;
    if (sinks.includes(c.id)) sub = `used by ${usedBy(c.id).length} others`;
    if (tops.includes(c.id)) sub = `uses ${uses(c.id).length} others`;
    L.push(`${sid(c.id)}["<b>${nice(c.id)}</b><br/><span style='font-size:11px'>${sub}</span>"]`);
    if (c.new) L.push(`class ${sid(c.id)} new;`);
    else if (inCycle.has(c.id)) L.push(`class ${sid(c.id)} cyc;`);
    else if (sinks.includes(c.id) || tops.includes(c.id)) L.push(`class ${sid(c.id)} hub;`);
  }
  let i = 0; const cycLinks = [];
  for (const [k, n] of pairs) {
    const [a, b] = k.split('>'); // a provides, b uses -> draw "b uses a" as b --> a
    const cyc = has(b, a);
    if (!cyc && (sinks.includes(a) || tops.includes(b))) continue; // summarized by the hub note
    L.push(`${sid(b)} -->|${n}| ${sid(a)}`);
    if (cyc) cycLinks.push(i);
    i++;
  }
  if (cycLinks.length) L.push(`linkStyle ${cycLinks.join(',')} stroke:#c2410c,stroke-width:2.5px;`);
  for (const t of tops) for (const s of sinks) if (t !== s) { L.push(`${sid(t)} ~~~ ${sid(s)}`); }
  return { mmd: L.join('\n'), cycles: [...inCycle] };
}

// ---------------- port graph (ELK) ----------------
const CW = 6.9; // px per char, 11.5px monospace
async function ports() {
  const elk = new ELK();
  const opts = { 'elk.algorithm': 'layered', 'elk.direction': 'DOWN', 'elk.edgeRouting': 'ORTHOGONAL',
    'elk.layered.spacing.nodeNodeBetweenLayers': '58', 'elk.spacing.nodeNode': '16', 'elk.spacing.edgeNode': '12',
    'elk.layered.spacing.edgeNodeBetweenLayers': '14', 'elk.portConstraints': 'FIXED_SIDE',
    'elk.layered.nodePlacement.strategy': 'BRANDES_KOEPF' };
  const fed = new Set(m.wires.map((w) => `${w.to}.${w.to_port}`));
  const nodes = []; const loose = [];
  for (const c of m.components) for (const e of c.exports.filter((x) => x.typed)) {
    const id = `${c.id}.${e.name}`;
    const ps = e.args.filter(([, t]) => t).map(([a, t]) => ({ id: `${id}.in.${a}`, side: 'NORTH', arg: a, t }));
    if (e.ret) ps.push({ id: `${id}.out`, side: 'SOUTH', t: e.ret });
    const unfed = e.args.filter(([a, t]) => t && !m.wires.some((w) => w.to === c.id && w.to_port === e.name && w.to_arg === a));
    unfed.forEach(([a, t]) => loose.push({ node: id, t, a }));
    const width = Math.max(e.name.length * CW + 18, (nice(c.id).length + (c.new ? 0 : 11)) * 6.4 + 18, 92);
    nodes.push({ id, width, height: 40, comp: c.id, name: e.name, isNew: c.new, unfed,
      ports: ps.map((p) => ({ id: p.id, width: 7, height: 7, layoutOptions: { 'elk.port.side': p.side }, t: p.t })) });
  }
  const edges = m.wires.map((w, k) => {
    const node = nodes.find((n) => n.id === `${w.to}.${w.to_port}`);
    const p = node.ports.find((q) => q.id === `${w.to}.${w.to_port}.in.${w.to_arg}`);
    return { id: `e${k}`, sources: [`${w.from}.${w.from_port}.out`], targets: [p.id], label: w.label,
      labels: [{ text: w.label, width: w.label.length * 6.2 + 4, height: 12 }] };
  });
  const g = await elk.layout({ id: 'root', layoutOptions: opts, children: nodes, edges });
  const pal = ['#1d4ed8', '#c2410c', '#475569', '#0f766e', '#7c3aed'];
  const comps = [...new Set(nodes.map((n) => n.comp))];
  const col = (c) => pal[comps.indexOf(c) % pal.length];
  const P = [];
  for (const e of g.edges) for (const s of e.sections || []) {
    const pts = [s.startPoint, ...(s.bendPoints || []), s.endPoint];
    P.push(`<path d="M${pts.map((p) => `${p.x},${p.y}`).join(' L')}" class="w" marker-end="url(#a)"/>`);
  }
  for (const e of g.edges) for (const l of e.labels || []) P.push(`<text x="${l.x}" y="${l.y + 10}" class="wl">${esc(l.text)}</text>`);
  for (const n of g.children) {
    const c = col(n.comp);
    P.push(`<g class="fnode" data-id="${esc(n.id)}" tabindex="0" role="button">`);
    P.push(`<rect x="${n.x}" y="${n.y}" width="${n.width}" height="${n.height}" rx="7" fill="#fff" stroke="${c}" stroke-width="${n.isNew ? 2.4 : 1.3}"${n.isNew ? '' : ' stroke-dasharray="5 3"'}/>`);
    P.push(`<text x="${n.x + 8}" y="${n.y + 14}" class="cl" fill="${c}">${esc(nice(n.comp))}${n.isNew ? '' : ' (existing)'}</text>`);
    P.push(`<text x="${n.x + 8}" y="${n.y + 31}" class="fn">${esc(n.name)}</text>`);
    P.push('</g>');
    for (const p of n.ports) P.push(`<rect x="${n.x + p.x}" y="${n.y + p.y}" width="7" height="7" fill="${c}"/>`);
    // inputs nothing in the plan provides: say where they enter
    n.unfed.forEach(([a, t], k) => {
      const p = n.ports.find((q) => q.id.endsWith(`.in.${a}`));
      const x = n.x + p.x + 3, y = n.y + p.y;
      P.push(`<line x1="${x}" y1="${y - 16}" x2="${x}" y2="${y}" class="ext"/><text x="${x + 3}" y="${y - 6 - k * 0}" class="el">${esc(t)}</text>`);
    });
  }
  const W = Math.ceil(g.width) + 24, H = Math.ceil(g.height) + 24;
  return { svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -20 ${W} ${H + 8}" width="${W}" font-family="system-ui,sans-serif">
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#334155"/></marker>
<style>.w{fill:none;stroke:#334155;stroke-width:1.4}.wl{font-size:11px;font-family:ui-monospace,monospace;fill:#0f172a;font-weight:600;paint-order:stroke;stroke:#fff;stroke-width:4px}
.cl{font-size:10.5px;font-weight:700;letter-spacing:.02em}.fn{font-size:11.5px;font-family:ui-monospace,monospace;fill:#0f172a}
.ext{stroke:#94a3b8;stroke-dasharray:2 2}.el{font-size:10px;fill:#64748b;font-family:ui-monospace,monospace}</style></defs>
${P.join('\n')}</svg>`, loose };
}

// ---------------- trace (table) ----------------
function trace() {
  const rows = m.criteria.map((s) => {
    const comps = m.components.filter((c) => c.criteria.includes(s.id)).map((c) => nice(c.id));
    const direct = s.proofs.filter((p) => p.role === 'direct').map((p) => p.id.replace('VS-GF-', ''));
    const route = [direct.length ? `test: ${direct.join(', ')}` : '', s.external.length ? 'outside the repo (a person or run records it)' : ''].filter(Boolean).join(' + ') || 'NO PROOF ROUTE';
    return `<tr><td><b>${esc(s.id)}</b><br>${esc(s.text)}</td><td>${esc(comps.join(', '))}</td><td>${esc(route)}</td></tr>`;
  });
  return `<table class="t"><thead><tr><th>Criterion</th><th>Built by</th><th>Proved by</th></tr></thead><tbody>${rows.join('')}</tbody></table>`;
}

async function mermaidSvg(src, page) {
  await page.setContent('<div id="c"></div>');
  await page.addScriptTag({ path: path.resolve('node_modules/mermaid/dist/mermaid.min.js') });
  return page.evaluate(async (s) => {
    window.mermaid.initialize({ startOnLoad: false, theme: 'base', flowchart: { htmlLabels: true, nodeSpacing: 18, rankSpacing: 38, padding: 8 },
      themeVariables: { fontSize: '14px', primaryColor: '#ffffff', primaryBorderColor: '#334155', lineColor: '#475569', fontFamily: 'system-ui,sans-serif' } });
    return (await window.mermaid.render('g', s)).svg;
  }, src);
}

const page = (title, note, body) => `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title><style>body{margin:0;padding:12px 16px;font-family:system-ui,sans-serif;background:#fff;color:#0f172a}
h1{font-size:17px;margin:4px 0}p{font-size:13px;color:#475569;margin:4px 0 10px}.d svg{max-width:100%;height:auto;display:block}
.t{border-collapse:collapse;font-size:12px;width:100%}.t td,.t th{border-top:1px solid #e2e8f0;padding:6px 4px;text-align:left;vertical-align:top}</style></head>
<body><h1>${esc(title)}</h1><p>${note}</p><div class="d">${body}</div></body></html>`;

const browser = await chromium.launch();
const pg = await browser.newPage();
const meta = {};
for (const k of kinds) {
  if (k === 'structure') {
    const { mmd, cycles } = structure();
    fs.writeFileSync(`${outPrefix}-structure.mmd`, mmd);
    const svg = await mermaidSvg(mmd, pg);
    fs.writeFileSync(`${outPrefix}-structure.svg`, svg);
    meta.cycles = cycles;
    fs.writeFileSync(`${outPrefix}-structure.html`, page('Which part uses which',
      'Generated. An arrow means “uses” (number = names it imports). Orange dashed = the two parts use each other (a cycle). Blue = used by, or uses, nearly everything, so those arrows are folded into the box.', svg));
  }
  if (k === 'ports') {
    const { svg, loose } = await ports();
    fs.writeFileSync(`${outPrefix}-ports.svg`, svg);
    meta.loose = loose;
    fs.writeFileSync(`${outPrefix}-ports.html`, page('What data passes between steps',
      'Generated from typed function signatures in the plan. A wire = one function’s output type is another’s input. Grey stubs = inputs nothing in the plan produces.', svg));
  }
  if (k === 'trace') fs.writeFileSync(`${outPrefix}-trace.html`, page('Criterion → built by → proved by', 'Generated. A table, because this chain is one-to-one almost everywhere.', trace()));
}
fs.writeFileSync(`${outPrefix}-meta.json`, JSON.stringify(meta, null, 1));
await browser.close();
console.log('wrote', outPrefix, kinds.join(','), JSON.stringify(meta));
