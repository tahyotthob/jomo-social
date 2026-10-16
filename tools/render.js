const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  const dir = path.join(__dirname, 'html'); const out = path.join(__dirname, 'png');
  fs.mkdirSync(out, { recursive: true });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort()) {
    const wide = f.includes('16x9'); const tall = f.includes('9x16');
    const p = await b.newPage({ viewport: { width: wide ? 1600 : 1080, height: wide ? 900 : (tall ? 1920 : 1350) } });
    await p.goto('file://' + path.join(dir, f)); await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(150);
    // overflow check: any element extending past the footer line or right edge
    const issues = await p.evaluate(() => {
      const W = innerWidth, H = innerHeight, footTop = document.querySelector('.foot').getBoundingClientRect().top;
      const bad = [];
      document.querySelectorAll('.h,.body,.brico,.label').forEach(e => { const r = e.getBoundingClientRect();
        if (r.right > W - 60 || r.bottom > footTop) bad.push(e.className + ' ' + Math.round(r.right) + 'x' + Math.round(r.bottom)); });
      return bad;
    });
    if (issues.length) console.log('CHECK', f, issues);
    await p.screenshot({ path: path.join(out, f.replace('.html', '.png')) }); await p.close();
  }
  await b.close(); console.log('done');
})();
