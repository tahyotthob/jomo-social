// Render an animated HTML overlay to a transparent PNG sequence.
// Usage: node render_frames.js page.html outDir seconds [fps]
// The page must define window.render(t) that sets the scene for time t (seconds).
const { chromium } = require('../node_modules/playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const [html, outDir, secs, fpsArg] = process.argv.slice(2);
  const fps = Number(fpsArg || 25); const frames = Math.round(Number(secs) * fps);
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  for (let i = 0; i < frames; i++) {
    await p.evaluate(t => window.render(t), i / fps);
    await p.screenshot({ path: path.join(outDir, String(i).padStart(5, '0') + '.png'), omitBackground: true });
  }
  await b.close();
  console.log(`rendered ${frames} frames to ${outDir}`);
})();
