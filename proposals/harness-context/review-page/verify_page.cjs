// Reuse the caller's existing Playwright and browser; never install dependencies.
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');

(async () => {
  const browser = await chromium.launch({headless: true,
    ...(process.env.BROWSER_EXECUTABLE ? {executablePath: process.env.BROWSER_EXECUTABLE} : {})});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(process.argv[2] || pathToFileURL(path.join(__dirname, 'index.html')).href);
    await page.waitForSelector('[data-role]');
    await page.evaluate(() => document.fonts.ready);
    for (const summary of await page.locator('summary').all()) await summary.click();
    let hover = 0, focus = 0;
    for (const control of await page.locator('button,a,summary').all()) {
      await control.scrollIntoViewIfNeeded();
      await control.hover();
      if (!await page.locator('#tip').isVisible() || !(await page.locator('#tip').innerText()).trim())
        throw Error('Hover tooltip missing');
      hover++;
      await control.focus();
      if (!await page.locator('#tip').isVisible()) throw Error('Focus tooltip missing');
      focus++;
    }
    const geometry = () => page.evaluate(() => {
      const nodes = [...document.querySelectorAll('.node')];
      const rects = nodes.map(node => node.getBoundingClientRect());
      let overlaps = 0;
      for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < rects.length; j++) {
        const a = rects[i], b = rects[j];
        if (a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top) overlaps++;
      }
      return {nodes: nodes.length, overlaps,
        overflow: nodes.filter(n => n.scrollWidth > n.clientWidth + 1 || n.scrollHeight > n.clientHeight + 1)
          .map(n => n.id || n.dataset.role)};
    });
    const desktop = await geometry();
    if (desktop.overlaps || desktop.overflow.length) throw Error(JSON.stringify(desktop));
    for (const role of await page.locator('[data-role]').all()) {
      await role.click();
      if (await page.locator('#detail-name').innerText() !== await role.locator('b').innerText())
        throw Error('Role selection failed');
    }
    await page.locator('[data-mode="current"]').click();
    if (!/720lines/.test(await page.locator('#detail-loads').innerText())) throw Error('Current view failed');
    await page.locator('[data-mode="proposed"]').click();
    await page.locator('#zoom-in').click();
    await page.locator('#fit').click();
    await page.setViewportSize({width: 390, height: 844});
    await page.evaluate(() => document.fonts.ready);
    const mobile = await geometry();
    if (mobile.overlaps || mobile.overflow.length) throw Error(JSON.stringify(mobile));
    if (await page.evaluate(() => document.documentElement.scrollWidth > innerWidth))
      throw Error('Mobile page overflow');
    const touchPage = await browser.newPage({viewport: {width: 390, height: 844},
      hasTouch: true, isMobile: true});
    touchPage.on('pageerror', error => errors.push(error.message));
    await touchPage.goto(page.url());
    await touchPage.evaluate(() => document.fonts.ready);
    await touchPage.locator('[data-role="review"]').tap();
    if (!await touchPage.locator('#tip').isVisible()) throw Error('Touch tooltip missing');
    await touchPage.close();
    if (errors.length) throw Error(errors.join(';'));
    const receipt = {hover_passed: hover, focus_passed: focus, touch_passed: 1,
      role_selection_passed: 7, other_interaction_passed: 4,
      desktop_geometry: desktop, mobile_geometry: mobile, page_errors: errors,
      passed: hover + focus + 14, failed: 0, exit_status: 0};
    fs.writeFileSync(path.join(__dirname, 'browser-verification.json'), JSON.stringify(receipt, null, 2) + '\n');
    console.log(JSON.stringify(receipt));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
