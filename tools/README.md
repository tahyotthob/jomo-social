# Flyer tools

`build.py` writes each slide as an HTML file into `tools/html/`; `render.js` opens them in headless Chromium and saves PNGs into `tools/png/` at the right pixel size (1080×1350 by default, 1600×900 when the file name contains `16x9`, 1080×1920 when it contains `9x16`). It also warns when a headline or paragraph runs past the footer or the right edge.

```bash
cd tools
npm ci                                   # fonts (Anton, Bricolage Grotesque, Lato) + Playwright
npx playwright install chromium          # once per machine; not needed where Chromium is preinstalled
python3 build.py && node render.js
```

If Chromium is preinstalled somewhere else, point to it: `CHROMIUM_PATH=/path/to/chrome node render.js`.

`build.py` holds the shared brand CSS (`CSS`), the footer handle bar, the sprout shape and a `page()` helper. Add a post by writing its slides with `write("name", page(html, theme, n, total))`, where theme is `ink`, `lime` or `off`. `food.py` shows a one-off post built on top of it. For a photo-led slide, put the photo in `assets/photos/` and reference it with an absolute `file://` path in an `<img>` styled `object-fit: cover`.

`newsroom-map.html` is the interactive map of the twelve roles; open it in a browser.
