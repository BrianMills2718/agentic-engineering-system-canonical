// Phone-width screenshot + the render check the gate proposes: not blank, no error text.
// Usage: node shoot.mjs <out.png> <file-or-url> [...pairs]
import { chromium } from 'playwright';
import path from 'node:path';
const args = process.argv.slice(2);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1.5 });
let failed = 0;
for (let i = 0; i < args.length; i += 2) {
  const [png, src] = [args[i], args[i + 1]];
  const url = /^https?:|^file:/.test(src) ? src : 'file://' + path.resolve(src);
  const errs = [];
  p.removeAllListeners('pageerror'); p.on('pageerror', (e) => errs.push(String(e)));
  const resp = await p.goto(url, { waitUntil: 'networkidle' });
  const status = resp ? resp.status() : 0;
  const r = await p.evaluate(() => ({
    text: document.body.innerText.trim().length,
    svgs: document.querySelectorAll('svg').length,
    // signatures of real error pages, not the word "error" (this page talks about errors)
    error: /Traceback \(most recent call last\)|Internal Server Error|Cannot GET \/|Uncaught \w+Error|\b(404|500|502|503) (Not Found|Bad Gateway|Service Unavailable)/.test(document.body.innerText),
    overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
    h: document.documentElement.scrollHeight,
  }));
  await p.screenshot({ path: png, fullPage: true, timeout: 120000 });
  const ok = (r.text > 20 || r.svgs > 0) && !r.error && errs.length === 0 && (status === 0 || status < 400);
  if (!ok) failed++;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${png} text=${r.text} svgs=${r.svgs} error_text=${r.error} js_errors=${errs.length} http=${status} h_scroll=${r.overflow} height=${r.h}`);
}
await b.close();
console.log(`render check: ${args.length / 2 - failed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
