// Rendered check: no "…" in visible text, every derivation-graph label inside its box, page renders at 1440 and 390.
import { chromium } from 'playwright';
const [file, outDir] = process.argv.slice(2);
const b = await chromium.launch({ args: ['--disable-gpu'] });
let failed = 0;
for (const [name, vw] of [['desk', 1440], ['phone', 390]]) {
  const p = await b.newPage({ viewport: { width: vw, height: 900 }, deviceScaleFactor: 1.5 });
  const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto('file://' + file, { waitUntil: 'networkidle' });
  if (vw < 700) await p.evaluate(() => document.querySelectorAll('details').forEach((d) => (d.open = true)));
  const r = await p.evaluate(() => {
    const txt = document.body.innerText + [...document.querySelectorAll('svg text')].map((t) => t.textContent).join(' ');
    let outside = 0, checked = 0;
    document.querySelectorAll('#g .node').forEach((g) => {
      const rect = g.querySelector('rect').getBBox();
      g.querySelectorAll('text').forEach((t) => { const bb = t.getBBox(); checked++;
        if (bb.x + bb.width > rect.x + rect.width + 0.5 || bb.y + bb.height > rect.y + rect.height + 0.5) outside++; });
    });
    const insp = document.getElementById('insp'); const spill = [...insp.querySelectorAll('*')].filter((e) => e.getBoundingClientRect().right > insp.getBoundingClientRect().right + 0.5).length;
    return { inspSpill: spill, ellipsis: (txt.match(/…/g) || []).length, outside, checked, nodes: document.querySelectorAll('#g .node').length,
      hscroll: document.documentElement.scrollWidth > window.innerWidth + 1, bullets: document.querySelectorAll('ul.pts li').length };
  });
  await p.screenshot({ path: `${outDir}/${name}.png`, fullPage: true, timeout: 280000 });
  const ok = r.inspSpill === 0 && r.ellipsis === 0 && r.outside === 0 && errs.length === 0 && !r.hscroll && r.nodes > 0;
  if (!ok) failed++;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name} ${vw}px: ellipses=${r.ellipsis} panel_overflow=${r.inspSpill} labels_outside_box=${r.outside}/${r.checked} graph_boxes=${r.nodes} bullets=${r.bullets} js_errors=${errs.length} page_scrolls_sideways=${r.hscroll}`);
  await p.close();
}
await b.close();
console.log(`fit check: ${2 - failed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
