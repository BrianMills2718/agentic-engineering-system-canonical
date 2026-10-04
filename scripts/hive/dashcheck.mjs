// Rendered check of the hive dashboard: nothing cut off, every map box opens something, tiles explain themselves, laptop layout.
import { chromium } from 'playwright';
const [file, outDir] = process.argv.slice(2);
const b = await chromium.launch({ args: ['--disable-gpu'] });
let failed = 0;
for (const [name, vw, vh] of [['phone', 390, 844], ['laptop', 1440, 900]]) {
  const p = await b.newPage({ viewport: { width: vw, height: vh } });
  const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto('file://' + file, { waitUntil: 'networkidle' });
  const keys = await p.$$eval('.node', (ns) => ns.map((n) => n.dataset.key));
  const opened = [];
  for (const k of keys) {
    // Tap where a finger would: the element at the box's centre must be the box itself (not covered), then click it.
    const hit = await p.$eval(`.node[data-key="${k}"]`, (n) => { n.scrollIntoView({ block: 'center' }); const r = n.getBoundingClientRect();
      const top = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2); const ok = !!top && n.contains(top);
      (ok ? top : n).dispatchEvent(new MouseEvent('click', { bubbles: true })); return ok; });
    if (!hit) console.log(`  box ${k} is covered by something else`);
    opened.push(await p.$eval('#info', (i) => ({ len: i.innerText.trim().length, md: i.querySelector('.mdout') ? i.querySelector('.mdout').innerHTML.length : -1,
      links: i.querySelectorAll('a').length, pc: !!i.querySelector('a[href*="paperclip.brianmills.dev/BRI/"]') })));
  }
  const brainOpen = opened.filter((o, i) => keys[i].startsWith('brain:'));
  await p.$eval('.tabs button[data-s="health"]', (t) => t.click());
  await p.$eval('.tile', (t) => t.dispatchEvent(new MouseEvent('click', { bubbles: true })));
  const sheet = await p.$eval('.tipsheet', (s) => !s.hidden && s.innerText.length);
  const r = await p.evaluate(() => ({
    ellipsis: (document.body.innerText.match(/…/g) || []).length + [...document.querySelectorAll('svg text')].filter((t) => t.textContent.includes('…')).length,
    hscroll: document.documentElement.scrollWidth > innerWidth + 1,
    tabs: getComputedStyle(document.querySelector('.tabs')).display,
    visibleScreens: [...document.querySelectorAll('.screen')].filter((s) => s.getBoundingClientRect().height > 0).length,
    tipped: document.querySelectorAll('[data-tip],[title],svg title').length }));
  await p.$eval('.tabs button[data-s="map"]', (t) => t.click());
  await p.screenshot({ path: `${outDir}/dash-${name}.png`, fullPage: name === 'laptop', timeout: 120000 });
  const empty = opened.filter((o) => o.len < 20).length;
  const ok = errs.length === 0 && r.ellipsis === 0 && !r.hscroll && empty === 0 && sheet > 20
    && brainOpen.every((o) => o.links > 0) && r.tabs !== 'none' && r.visibleScreens === 1 && opened.filter((o, i) => /^(agent|brain):/.test(keys[i])).every((o) => o.pc);
  if (!ok) failed++;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name} ${vw}px: boxes=${keys.length} boxes_opening_nothing=${empty} brain_panels_with_notes=${brainOpen.filter((o) => o.md > 50).length}/${brainOpen.length} `
    + `tile_explains=${!!sheet} ellipses=${r.ellipsis} explained_elements=${r.tipped} screens_visible=${r.visibleScreens} tab_bar=${r.tabs} sideways_scroll=${r.hscroll} js_errors=${errs.length}${errs.length ? ' ' + errs[0] : ''}`);
  await p.close();
}
await b.close();
console.log(`dashboard check: ${2 - failed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
