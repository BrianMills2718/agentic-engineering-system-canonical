// Probe 0 temporary port-graph layout for render_review.py (the Architecture lens).
// Reads a port model as JSON on stdin, lays it out with ELK (layered, ports on fixed sides),
// writes one SVG fragment to stdout. Same layout code as the plan-gate shaping prototype
// (proposals/aes-plan-gate/prototype/render.mjs ports() at commit 43b9670), with page-themed CSS classes.
// Usage: node port_layout.mjs --elk <path/to/elkjs/lib/elk.bundled.js> < model.json > ports.svg
import fs from 'node:fs';
import { createRequire } from 'node:module';

const elkPath = process.argv[process.argv.indexOf('--elk') + 1];
if (!elkPath || !fs.existsSync(elkPath)) { console.error('port_layout: --elk <elk.bundled.js> is required'); process.exit(2); }
const ELK = createRequire(import.meta.url)(elkPath);
const m = JSON.parse(fs.readFileSync(0, 'utf8'));
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const CW = 6.9; // px per character of 11.5px monospace (monospace advance is 0.6em)

const comps = [...new Set(m.nodes.map((n) => n.component))];
const proposalMode = m.mode === 'proposal';
const tag = (n) => (proposalMode && !n.proposed ? ' (existing)' : '');
const nodes = m.nodes.map((n) => {
  const ports = n.args.filter((a) => a.types.length).map((a) => ({ id: `${n.id}.in.${a.name}`, width: 7, height: 7, layoutOptions: { 'elk.port.side': 'NORTH' } }));
  if (n.ret_types.length) ports.push({ id: `${n.id}.out`, width: 7, height: 7, layoutOptions: { 'elk.port.side': 'SOUTH' } });
  const width = Math.max(n.name.length * CW + 18, (n.component_label + tag(n)).length * 6.4 + 18, 96);
  return { id: n.id, width, height: 40, ports, n };
});
const edges = m.wires.map((w, k) => ({ id: `e${k}`, sources: [`${w.from}.out`], targets: [`${w.to}.in.${w.to_arg}`],
  labels: [{ text: w.label, width: w.label.length * CW * 0.9 + 4, height: 12 }], w }));
const opts = { 'elk.algorithm': 'layered', 'elk.direction': 'DOWN', 'elk.edgeRouting': 'ORTHOGONAL',
  'elk.layered.spacing.nodeNodeBetweenLayers': '58', 'elk.spacing.nodeNode': '16', 'elk.spacing.edgeNode': '12',
  'elk.layered.spacing.edgeNodeBetweenLayers': '14', 'elk.portConstraints': 'FIXED_SIDE',
  'elk.layered.nodePlacement.strategy': 'BRANDES_KOEPF' };
const g = await new ELK().layout({ id: 'root', layoutOptions: opts, children: nodes, edges });

const P = [];
for (const e of g.edges) {
  const src = edges.find((x) => x.id === e.id).w;
  for (const s of e.sections || []) {
    const pts = [s.startPoint, ...(s.bendPoints || []), s.endPoint];
    P.push(`<path d="M${pts.map((p) => `${p.x},${p.y}`).join(' L')}" class="pw${src.ambiguous ? ' amb' : ''}" marker-end="url(#pa)"><title>${esc(src.label)}${src.ambiguous ? ' (more than one function could supply this; first one shown)' : ''}</title></path>`);
  }
  for (const l of e.labels || []) P.push(`<text x="${l.x}" y="${l.y + 10}" class="pwl">${esc(l.text)}</text>`);
}
for (const node of g.children) {
  const { n } = nodes.find((x) => x.id === node.id);
  const c = `pc${comps.indexOf(n.component) % 4}`;
  P.push(`<g class="pnode ${c}${n.proposed || !proposalMode ? ' prop' : ''}" data-id="${esc(n.artifact)}" tabindex="0" role="button" aria-label="${esc(n.name)} in ${esc(n.component_label)}">`);
  P.push(`<rect x="${node.x}" y="${node.y}" width="${node.width}" height="${node.height}" rx="7"/>`);
  P.push(`<text x="${node.x + 8}" y="${node.y + 14}" class="pcl">${esc(n.component_label + tag(n))}</text>`);
  P.push(`<text x="${node.x + 8}" y="${node.y + 31}" class="pfn">${esc(n.name)}</text></g>`);
  for (const p of node.ports) P.push(`<rect x="${node.x + p.x}" y="${node.y + p.y}" width="7" height="7" class="pport ${c}"/>`);
  n.args.filter((x) => x.types.length && x.unfed).forEach((a, k) => {
    // stagger stub labels so adjacent inputs do not overprint each other
    const p = node.ports.find((q) => q.id === `${n.id}.in.${a.name}`);
    const x = node.x + p.x + 3, y = node.y + p.y, len = 16 + (k % 2) * 13;
    P.push(`<line x1="${x}" y1="${y - len}" x2="${x}" y2="${y}" class="pext"/><text x="${x + 3}" y="${y - len + 9}" class="pel">${esc(a.annotation)}<title>input from outside: ${esc(a.name)}: ${esc(a.annotation)}</title></text>`);
  });
}
const longest = Math.max(0, ...m.nodes.flatMap((n) => n.args.filter((a) => a.unfed).map((a) => a.annotation.length)));
const W = Math.ceil(g.width) + 24 + Math.ceil(longest * 6), H = Math.ceil(g.height) + 46;
process.stdout.write(`<svg class="ports" xmlns="http://www.w3.org/2000/svg" viewBox="-12 -34 ${W} ${H}" width="${W}" role="img" aria-label="port graph: functions, the types they take and return, and the wires between them">
<defs><marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="pah"/></marker></defs>
${P.join('\n')}</svg>`);
