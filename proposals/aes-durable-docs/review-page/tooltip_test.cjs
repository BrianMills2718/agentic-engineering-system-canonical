// Browser test for index.html: every visible element with a tooltip marker (data-tip)
// shows its styled tooltip within 200 ms on hover and on keyboard focus, carries a
// visible "i" mark, and (at phone width) shows it on tap. Also checks that no text in a
// diagram box spills outside its box and that the page has no horizontal scroll.
// Run: NODE_PATH=<dir containing playwright> node tooltip_test.cjs
const path = require("path");
const { chromium } = require("playwright");

const FILE = "file://" + path.join(__dirname, "index.html");
const VIEWPORTS = [
  { name: "1440", width: 1440, height: 900, touch: false },
  { name: "390", width: 390, height: 844, touch: true },
];

(async () => {
  const browser = await chromium.launch();
  let failures = 0, checked = 0;
  for (const vp of VIEWPORTS) {
    for (const scheme of ["light", "dark"]) {
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, hasTouch: vp.touch, colorScheme: scheme });
      const page = await ctx.newPage();
      await page.goto(FILE);
      const report = await page.evaluate(() => {
        const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== "hidden"; };
        const els = [...document.querySelectorAll("[data-tip]")].filter(vis);
        els.forEach((e, i) => e.setAttribute("data-test-id", String(i)));
        const noMark = els.filter((e) => !e.querySelector(".imark,.ibtn")).map((e) => e.getAttribute("aria-label").slice(0, 50));
        const orphanMarks = [...document.querySelectorAll(".imark,.ibtn")].filter((m) => vis(m) && !m.closest("[data-tip]")).length;
        const spill = [];
        document.querySelectorAll("g.node").forEach((g) => {
          if (!vis(g)) return;
          const rect = g.querySelector("rect").getBoundingClientRect();
          g.querySelectorAll(":scope > text").forEach((t) => {
            const b = t.getBoundingClientRect();
            if (b.left < rect.left - 1 || b.right > rect.right + 1 || b.top < rect.top - 1 || b.bottom > rect.bottom + 1)
              spill.push(t.textContent.slice(0, 40));
          });
        });
        const hscroll = document.documentElement.scrollWidth > document.documentElement.clientWidth;
        return { count: els.length, noMark, orphanMarks, spill, hscroll };
      });
      const label = `${vp.name}px ${scheme}`;
      let hoverFail = [], focusFail = [], slow = [];
      for (let i = 0; i < report.count; i++) {
        const sel = `[data-test-id="${i}"]`;
        const loc = page.locator(sel);
        await loc.scrollIntoViewIfNeeded();
        await page.mouse.move(1, 1);
        await page.evaluate(() => document.activeElement && document.activeElement.blur());
        // hover
        const t0 = Date.now();
        await loc.hover({ position: { x: 20, y: 20 } });
        const ok = await page.waitForFunction((s) => {
          const tip = document.getElementById("tip"), el = document.querySelector(s);
          return tip.classList.contains("show") && getComputedStyle(tip).opacity > 0.5 && tip.textContent === el.getAttribute("data-tip") && tip.getBoundingClientRect().width > 0;
        }, sel, { timeout: 1000 }).then(() => true, () => false);
        const ms = Date.now() - t0;
        if (!ok) hoverFail.push(i); else if (ms > 200) slow.push(`${i}:${ms}ms`);
        // keyboard focus
        await page.mouse.move(1, 1);
        await loc.focus();
        const fok = await page.waitForFunction((s) => {
          const tip = document.getElementById("tip"), el = document.querySelector(s);
          return tip.classList.contains("show") && tip.textContent === el.getAttribute("data-tip");
        }, sel, { timeout: 200 }).then(() => true, () => false);
        if (!fok) focusFail.push(i);
        checked++;
      }
      // tap (phone only): tap a node, tooltip stays after the tap
      let tapResult = "n/a";
      if (vp.touch) {
        await page.evaluate(() => document.activeElement && document.activeElement.blur());
        await page.mouse.move(1, 1);
        const loc = page.locator('[data-test-id="3"]');
        await loc.scrollIntoViewIfNeeded();
        await loc.tap({ position: { x: 20, y: 20 } });
        await page.waitForTimeout(250);
        tapResult = (await page.evaluate(() => document.getElementById("tip").classList.contains("show"))) ? "shown" : "NOT shown";
        if (tapResult !== "shown") failures++;
      }
      const f = hoverFail.length + focusFail.length + slow.length + report.noMark.length + report.orphanMarks + report.spill.length + (report.hscroll ? 1 : 0);
      failures += f;
      console.log(`${label}: ${report.count} tooltip elements; hover ok ${report.count - hoverFail.length}/${report.count}; focus ok ${report.count - focusFail.length}/${report.count}; slower than 200ms: ${slow.length}${slow.length ? " " + slow.join(",") : ""}; missing i mark: ${report.noMark.length}; i mark with no tooltip: ${report.orphanMarks}; text spilling out of a box: ${report.spill.length}${report.spill.length ? " " + JSON.stringify(report.spill) : ""}; horizontal scroll: ${report.hscroll ? "YES" : "no"}; tap: ${tapResult}`);
      await ctx.close();
    }
  }
  await browser.close();
  console.log(`RESULT: ${failures === 0 ? "PASS" : "FAIL"}, ${checked} element checks, ${failures} failures`);
  process.exit(failures === 0 ? 0 : 1);
})();
