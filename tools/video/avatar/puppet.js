// JOMO puppet rig: Tobi and Amara as layered images (body + mouth/blink patches).
// A character's mouth follows a loudness envelope (one value per frame, 0..1); blinks are seeded,
// so the same video renders the same way every time.
window.Puppet = (() => {
  const FPS = 30;
  const rnd = (seed) => () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  function make(root, name, opts) {
    const el = document.createElement('div');
    el.className = 'pup'; el.style.cssText = `position:absolute;left:${opts.x}px;top:${opts.y}px;width:${opts.w}px;height:${opts.w * 1440 / 1080}px;transform-origin:50% 100%`;
    const layer = (src) => { const i = new Image(); i.src = src; i.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;opacity:0'; el.appendChild(i); return i; };
    const P = opts.dir;
    const body = layer(`${P}/${name}-body.png`); body.style.opacity = 1;
    const parts = {};
    for (const k of opts.parts) parts[k] = layer(`${P}/${name}-${k}-patch.png`);
    root.appendChild(el);
    const r = rnd(opts.seed || 7); const blinks = []; let t = 0.8 + r() * 1.5;
    while (t < 300) { blinks.push(t); t += 2.2 + r() * 2.8; }
    return { el, body, parts, name, opts, blinks, speech: [] };
  }
  // speech: [{start, env:[...]}] ; returns loudness at time t
  function loud(p, t) {
    for (const s of p.speech) { const i = Math.floor((t - s.start) * FPS); if (i >= 0 && i < s.env.length) return s.env[i]; }
    return -1;
  }
  function pose(p, t, extra = {}) {
    const L = loud(p, t); const talking = L >= 0;
    // mouth: Tobi has three states (closed, base grin, wide); Amara two (base closed smile, open)
    const pp = p.parts; for (const k in pp) pp[k].style.opacity = 0;
    if (talking) {
      if (pp.closed) { if (L < 0.18) pp.closed.style.opacity = 1; else if (L > 0.55) pp.mouth.style.opacity = 1; }
      else if (L > 0.22) pp.mouth.style.opacity = 1;
    } else if (pp.closed && extra.restClosed) pp.closed.style.opacity = 1;
    // blink: four frames
    if (pp.eyes && p.blinks.some((b) => t >= b && t < b + 4 / FPS)) pp.eyes.style.opacity = 1;
    // body: breathing, sway, and a small lean and bob while talking
    const br = Math.sin(t * 2.1 + (p.opts.seed || 0)) * 0.006;
    const sway = Math.sin(t * 1.3 + (p.opts.seed || 0)) * (p.opts.sway ?? 0.8);
    const lean = talking ? (p.opts.lean ?? 1.5) : 0;
    const bob = talking ? -Math.max(0, L) * 6 : 0;
    const enter = extra.enterX || 0;
    p.el.style.transform = `translate(${enter}px,${bob + (extra.dy || 0)}px) rotate(${sway + lean}deg) scale(${1 + br * 0.3},${1 + br})`;
  }
  return { make, pose, FPS };
})();
