// Usage: node browser.mjs <playwright-module> <chromium-executable> <url>
// Verifies the rendered reviewer path; it does not certify policy effectiveness.
import { writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const [modulePath, executablePath, url] = process.argv.slice(2);
const { chromium } = await import(modulePath);
const dir = dirname(fileURLToPath(import.meta.url));
const results = [], errors = [];
const assert = (name, ok, detail = '') => results.push({ name, outcome: ok ? 'passed' : 'failed', detail });
const browser = await chromium.launch({ headless: true, executablePath });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(url);
  await page.evaluate(() => document.fonts.ready);
  const expected = ['authority', 'context', 'assurance', 'capabilities', 'planning', 'execution', 'learning'];
  const actual = await page.locator('.node').evaluateAll(ns => ns.map(n => n.dataset.id));
  assert('seven accepted responsibilities are present', expected.every(id => actual.includes(id)) && actual.every(id => expected.includes(id)), actual.join(', '));
  assert('desktop has no page-width overflow', await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  assert('whole architecture fits inside its canvas on load', await page.locator('#canvas').evaluate(c => c.scrollWidth <= c.clientWidth + 2 && c.scrollHeight <= c.clientHeight + 2));
  await page.locator('.node[data-id="assurance"]').click();
  assert('selected responsibility shows meaning and owner', /Rules, applicability/.test(await page.locator('#inspector').innerText()) && /Owner/.test(await page.locator('#inspector').innerText()));
  assert('native description is projected as text', !/\[object Object\]/.test(await page.locator('#inspector').innerText()));
  const source = page.locator('#inspector a.source').first();
  assert('source link is pinned to a git revision and line', /\/blob\/[a-f0-9]{40}\/.*#L\d+$/.test(await source.getAttribute('href')));
  await page.screenshot({ path: join(dir, 'desktop.png') });
  await page.locator('[data-view="policy_loop"]').click();
  assert('selection survives a view where the subject is absent', /outside the current view/.test(await page.locator('#inspector').innerText()) && /Policy and assurance/.test(await page.locator('#inspector').innerText()));
  await page.locator('.node[data-id="control"]').click();
  assert('partial control coverage is explicit', /Partial coverage/.test(await page.locator('#inspector').innerText()));
  await page.locator('.edge text').first().click();
  assert('edge inspection distinguishes a declared handoff from execution', /does not prove/.test(await page.locator('#inspector').innerText()) && /Endpoint owners/.test(await page.locator('#inspector').innerText()));
  let tooltipCount = 0;
  for (const view of ['whole_system', 'policy_loop', 'records', 'concern_lifecycle', 'evidence']) {
    await page.locator('[data-view="' + view + '"]').click();
    await page.locator('details').evaluate(d => { d.open = true; });
    const controls = page.locator('[data-help]');
    for (let i = 0; i < await controls.count(); i++) {
      const control = controls.nth(i);
      if (!await control.isVisible()) continue;
      await control.scrollIntoViewIfNeeded();
      let target = control;
      if (await control.evaluate(c => c.classList.contains('node'))) target = control.locator('rect');
      if (await control.evaluate(c => c.classList.contains('edge'))) target = control.locator('text');
      if (!await target.count()) continue;
      if (await control.getAttribute("id") === "canvas") await target.hover({position:{x:3,y:3}}); else await target.hover();
      await page.waitForTimeout(160);
      const help = await control.getAttribute('data-help');
      const visible = await page.locator('#tooltip').isVisible();
      const correct = visible && await page.locator('#tooltip').innerText() === help;
      assert('styled hover tooltip: ' + view + ' / ' + (await control.getAttribute('aria-label') || await control.innerText()).slice(0, 70), correct);
      tooltipCount++;
    }
    assert('no painted node label extends beyond its box: ' + view, await page.locator('.node').evaluateAll(nodes => nodes.every(n => {
      const rect = n.querySelector('rect').getBBox();
      return [...n.querySelectorAll('text')].every(t => { const b = t.getBBox(); return b.x >= -1 && b.y >= -1 && b.x + b.width <= rect.width + 1 && b.y + b.height <= rect.height + 1; });
    })));
  }
  assert('tooltip checks exercised real rendered controls', tooltipCount >= 50, String(tooltipCount));
  assert('reproduced defect remains visible as unfixed', /missing evidence.*clear|false-clear|unfixed/i.test(await page.locator('#canvas').innerText()) && /reproduced/i.test(await page.locator('#canvas').innerText()));
  await page.locator('[data-view="whole_system"]').focus();
  await page.waitForTimeout(160);
  assert('keyboard focus shows a custom tooltip', await page.locator('#tooltip').isVisible());
  const sourceDownload = await page.request.get(new URL('model-source.json', url).href);
  const downloaded = await sourceDownload.json();
  assert('machine-readable model source downloads through allowed serving type', sourceDownload.status() === 200 && downloaded.format === 'LikeC4' && downloaded.source.includes('view whole_system'));
  await page.locator('[data-view="evidence"]').click();
  const evidence = await page.locator('#canvas a').first().getAttribute('href');
  const evidenceResponse = await page.request.get(new URL(evidence, url).href);
  assert('retained reproduction evidence opens', evidenceResponse.status() === 200 && (await evidenceResponse.json()).reproduced === 2);
  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  mobile.on('pageerror', e => errors.push(e.message));
  await mobile.goto(url);
  assert('phone layout has no page-width overflow', await mobile.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await mobile.locator('[data-view="policy_loop"]').tap();
  await mobile.waitForTimeout(160);
  assert('phone tap shows a styled tooltip', await mobile.locator('#tooltip').isVisible());
  await mobile.locator('.node[data-id="control"]').tap();
  assert('phone can inspect a model part', /Guide or check the action/.test(await mobile.locator('#inspector').innerText()));
  await mobile.locator('[data-view="whole_system"]').tap();
  await mobile.screenshot({ path: join(dir, 'phone.png') });
  assert('no JavaScript page errors', errors.length === 0, errors.join('; '));
} catch (e) {
  results.push({ name: 'browser execution', outcome: 'errored', detail: e.stack });
} finally {
  await browser.close();
}
const summary = { passed: results.filter(r => r.outcome === 'passed').length, failed: results.filter(r => r.outcome === 'failed').length, errored: results.filter(r => r.outcome === 'errored').length, skipped: 0 };
const exit = summary.failed || summary.errored ? 1 : 0;
await writeFile(join(dir, 'browser-result.json'), JSON.stringify({ boundary: 'Rendered model reviewer path; not runtime policy certification or Brian acceptance.', viewport: ['1440x1000', '390x844'], results, ...summary, exit }, null, 2) + '\n');
console.log(JSON.stringify({ ...summary, exit, failures: results.filter(r => r.outcome !== 'passed') }));
process.exitCode = exit;
