"""YCEF 2026 motion-graphics videos (operator brief, 2026-10-23: "as if Apple made it").

    python ycef_motion.py [a|b|all] [--keep]

Pure motion graphics in JOMO's brand: no AI footage and no avatar. Video A uses
one real, consent-logged JOMO photo. Frames are rendered in Chromium at 60 fps
and blended in pairs to 30 fps, which gives natural motion blur. Music is the
code-made ambient bed (ambient_bed.py); a silent version is written too.

Needs ffmpeg, Node with tools/node_modules (playwright) and Chromium
(CHROMIUM_PATH). Working files go to $VIDEO_WORK (default /tmp/jomo-video-work).
"""
import json, os, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
POST = ROOT / "content/posts/2026-10-22-ycef-videos"
FS = ROOT / "tools/node_modules/@fontsource"
LOGO = ROOT / "assets/logos/jomo-logo-light.png"
PHOTO = ROOT / "assets/photos/events/oniwaya-cleanup/oniwaya-cleanup-11.jpg"   # consent row in content/consent-log.csv
WORK = pathlib.Path(os.environ.get("VIDEO_WORK", "/tmp/jomo-video-work"))
RENDER_FPS, OUT_FPS = 60, 30
INK, LIME, OLIVE, CHAR, OFF = "#1E2220", "#A5CD39", "#77962A", "#323534", "#F4F6EC"
HANDLE = "@jomoclimate"
LINK = "jomoclimatechange.org/events?apply=ycef"


def run(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def ff(*args):
    run("ffmpeg", "-v", "error", "-y", *args)


CSS = f"""
@font-face {{ font-family: Brico; font-weight: 500; src: url('file://{FS}/bricolage-grotesque/files/bricolage-grotesque-latin-500-normal.woff2'); }}
@font-face {{ font-family: Brico; font-weight: 700; src: url('file://{FS}/bricolage-grotesque/files/bricolage-grotesque-latin-700-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 400; src: url('file://{FS}/lato/files/lato-latin-400-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 700; src: url('file://{FS}/lato/files/lato-latin-700-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 900; src: url('file://{FS}/lato/files/lato-latin-900-normal.woff2'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:{INK}; font-family:Lato;
  -webkit-font-smoothing:antialiased; text-rendering:geometricPrecision; }}
.scene {{ position:absolute; inset:0; opacity:0; }}
.dark {{ background:{INK}; color:{OFF}; }}
.light {{ background:{OFF}; color:{INK}; }}
.el {{ position:absolute; left:90px; right:90px; opacity:0; will-change:transform,opacity,filter; }}
.c {{ text-align:center; }}
.h {{ font-family:Brico; font-weight:700; letter-spacing:-.035em; line-height:1.0; }}
.line {{ display:block; overflow:hidden; padding-bottom:.08em; margin-bottom:-.08em; }}
.line > span {{ display:inline-block; will-change:transform; }}
.label {{ font-weight:700; font-size:30px; letter-spacing:.24em; text-transform:uppercase; }}
.body {{ font-size:46px; line-height:1.32; font-weight:400; }}
.acc {{ color:{LIME}; }}
.light .acc {{ color:{OLIVE}; }}
.muted {{ opacity:.62; }}
.btn {{ display:inline-block; background:{LIME}; color:{INK}; font-weight:900; font-size:44px; letter-spacing:.01em;
        padding:30px 74px; border-radius:80px; }}
.dot {{ display:inline-block; width:150px; height:150px; border-radius:50%; border:6px solid {OLIVE}; margin:0 22px; }}
.handle {{ display:flex; align-items:center; justify-content:center; gap:16px; font-weight:700; font-size:34px; }}
.handle svg {{ width:40px; height:40px; }}
"""

# Deterministic animation: window.render(t) sets every element for time t.
JS = """
const expoOut = x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x);
const inOut = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const clamp = x => Math.max(0, Math.min(1, x));
const els = [...document.querySelectorAll('[data-in]')];
window.render = function (t) {
  for (const el of els) {
    const tin = +el.dataset.in, tout = +el.dataset.out, a = el.dataset.a || 'fade';
    const d = +(el.dataset.d || .9), dx = +(el.dataset.dx || .45);
    if (t < tin - .001 || t > tout + .001) { el.style.opacity = 0; continue; }
    const p = expoOut(clamp((t - tin) / d));
    const q = el.dataset.hold ? 0 : inOut(clamp((t - (tout - dx)) / dx));   // exit progress
    let op = 1, tr = '', blur = 0;
    if (a === 'scene') {   // each new scene slides up over the previous one: no muddy crossfade between light and dark
      const k = tin <= 0 ? 1 : expoOut(clamp((t - tin) / .75));
      op = 1; tr = `translateY(${(1 - k) * 1920}px)`;
    }
    else if (a === 'mask') {
      el.querySelectorAll('.line > span').forEach((s, i) => {
        const pi = expoOut(clamp((t - tin - i * .09) / d));
        s.style.transform = `translateY(${(1 - pi) * 112}%)`;
      });
      op = 1 - q; tr = `translateY(${-40 * q}px)`; blur = 10 * q;
    }
    else if (a === 'fade') { op = p * (1 - q); tr = `translateY(${(1 - p) * 34 - 30 * q}px)`; blur = 12 * (1 - p) + 10 * q; }
    else if (a === 'scale') { op = p * (1 - q); tr = `scale(${.92 + .08 * p - .03 * q})`; }
    else if (a === 'slide') {
      const qq = el.dataset.hold ? 0 : inOut(clamp((t - (tout - dx)) / dx));
      op = p * (1 - qq); tr = `translateX(${(1 - p) * 140 - 140 * qq}px)`; blur = 8 * (1 - p) + 8 * qq;
    }
    el.style.opacity = op;
    el.style.transform = tr;
    el.style.filter = blur > .05 ? `blur(${blur}px)` : 'none';
    if (el.dataset.count) {
      const k = expoOut(clamp((t - tin) / 1.4));
      el.querySelector('b').textContent = Math.round(k * +el.dataset.count);
    }
    if (el.dataset.zoom) {
      const z = clamp((t - tin) / (tout - tin));
      el.querySelector('img').style.transform = `scale(${1.1 - .1 * z})`;
    }
    if (el.dataset.dots) {
      el.querySelectorAll('.dot').forEach((dot, i) => {
        const s = +el.dataset.dots.split(',')[i];
        const k = expoOut(clamp((t - s) / .6));
        dot.style.background = k > .02 ? `rgba(119,150,42,${k})` : 'transparent';
        dot.style.transform = `scale(${.85 + .15 * k})`;
      });
    }
  }
};
"""


def E(inner, t_in, t_out, top, a="fade", cls="", style="", d=None, dx=None, hold=False, extra=""):
    attrs = f'data-in="{t_in:.3f}" data-out="{t_out:.3f}" data-a="{a}"'
    if d: attrs += f' data-d="{d}"'
    if dx: attrs += f' data-dx="{dx}"'
    if hold: attrs += ' data-hold="1"'
    return f'<div class="el {cls}" style="top:{top}px;{style}" {attrs} {extra}>{inner}</div>'


def lines(*rows, size=150, cls=""):
    spans = "".join(f'<span class="line"><span>{r}</span></span>' for r in rows)
    return f'<div class="h {cls}" style="font-size:{size}px">{spans}</div>'


def scene(theme, t_in, t_out, *children, hold=False):
    # a scene stays up 0.8 s past its end so the next one can slide over it
    return (f'<div class="scene {theme}" data-in="{t_in:.3f}" data-out="{t_out + 0.8:.3f}" data-a="scene" data-hold="1">'
            + "".join(children) + "</div>")


def icons(color):
    ig = (f'<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/>'
          f'<circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="{color}" stroke="none"/></svg>')
    li = (f'<svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="4" fill="{color}"/>'
          f'<rect x="6" y="10" width="2.6" height="8" fill="{INK}"/><circle cx="7.3" cy="6.9" r="1.6" fill="{INK}"/>'
          f'<path d="M11 10h2.5v1.2c.5-.8 1.5-1.4 2.8-1.4 2 0 3 1.2 3 3.6V18h-2.6v-4.2c0-1.2-.4-1.9-1.4-1.9s-1.7.7-1.7 1.9V18H11z" fill="{INK}"/></svg>')
    return ig + li


def end_scene(t, total):
    """Shared end card: deadline, closing time, button, link, handle. Everything sits inside the 4:5 crop."""
    s = t + 0.15
    return scene("dark", t, total + 1,
        E(f'<img src="file://{LOGO}" style="width:500px">', s, total + 1, 300, "fade", "c", hold=True),
        E('<div class="label muted">Applications close</div>', s + .25, total + 1, 680, "fade", "c", hold=True),
        E(lines("Mon 26 Oct", size=156), s + .35, total + 1, 740, "mask", "c", hold=True),
        E(lines('<span class="acc">11:59 PM WAT</span>', size=96), s + .5, total + 1, 920, "mask", "c", hold=True),
        E('<span class="btn">Apply now</span>', s + .8, total + 1, 1110, "scale", "c", hold=True),
        E(f'<div class="body muted" style="font-size:36px">{LINK}</div>', s + 1.0, total + 1, 1290, "fade", "c", hold=True),
        E(f'<div class="handle">{icons(OFF)}<span>{HANDLE}</span></div>', s + 1.15, total + 1, 1520, "fade", "c", hold=True),
        hold=True)


# ---------------------------------------------------------------- Video A: "Your street has a climate problem."

def video_a_layers():
    T = 18.5
    return T, [3.0, 5.6, 8.6, 11.0, 14.2], [
        scene("dark", 0, 5.6,
            E(lines("Your street", "has a climate", '<span class="acc">problem.</span>', size=150), -0.45, 2.85, 640, "mask", d=1.0),   # readable on frame 0
            E(lines("Blocked drains.", size=128), 3.0, 3.9, 840, "mask", "c", d=.6, dx=.25),
            E(lines("Flooded roads.", size=128), 3.9, 4.75, 840, "mask", "c", d=.6, dx=.25),
            E(lines("Plastic everywhere.", size=112), 4.75, 5.6, 840, "mask", "c", d=.6, dx=.3)),
        scene("light", 5.6, 8.6,
            E(lines("You&rsquo;ve got", '<span class="acc">the fix.</span>', size=140), 5.8, 8.5, 300, "mask"),
            E(f'<div style="height:900px;border-radius:56px;overflow:hidden;box-shadow:0 40px 90px rgba(30,34,32,.22)">'
              f'<img src="file://{PHOTO}" style="width:100%;height:100%;object-fit:cover;object-position:50% 35%;transform-origin:50% 45%"></div>',
              6.0, 8.6, 640, "scale", d=1.1, extra='data-zoom="1"'),
            E('<div class="body muted" style="font-size:30px">A JOMO volunteer at the Oniwaya clean-up</div>', 6.5, 8.5, 1568, "fade", "c")),
        scene("dark", 8.6, 11.0,
            E('<div class="label acc">Now open</div>', 8.8, 10.8, 640, "fade", "c"),
            E(lines("Young Climate", "Educators", "Fellowship", size=136), 8.95, 10.8, 720, "mask", "c"),
            E(lines('<span class="acc">YCEF 2026</span>', size=96), 9.4, 10.8, 1170, "mask", "c")),
        scene("light", 11.0, 14.2,
            E('<div class="h" style="font-size:230px"><b>0</b></div><div class="label" style="margin-top:6px">Fellows</div>',
              11.2, 14.0, 330, "fade", "c", extra='data-count="50"'),
            E('<div class="h acc" style="font-size:96px;white-space:nowrap">Nigeria + Zambia</div>', 11.6, 14.0, 760, "fade", "c"),
            E('<div class="h" style="font-size:96px;white-space:nowrap">3 virtual weekends</div>', 12.0, 14.0, 900, "fade", "c"),
            E('<div class="body muted" style="font-size:40px">Starts Fri 13 Nov 2026<br>For university students and grassroots<br>community volunteers, aged 18+</div>',
              12.5, 14.0, 1090, "fade", "c")),
        end_scene(14.2, T),
    ]


# ---------------------------------------------------------------- Video B: what fellows do

def step(n, word, body, t_in, t_out, small=""):
    s = f'<div class="body muted" style="font-size:36px;margin-top:26px">{small}</div>' if small else ""
    return [
        E(f'<div class="label acc">Step 0{n} of 03</div>', t_in, t_out, 640, "slide", d=.7, dx=.35),
        E(f'<div class="h" style="font-size:190px">{word}</div>', t_in + .08, t_out, 710, "slide", d=.8, dx=.35),
        E(f'<div class="body" style="font-size:54px">{body}</div>{s}', t_in + .18, t_out, 940, "slide", d=.8, dx=.35),
    ]


def video_b_layers():
    T = 21.5
    return T, [3.0, 5.8, 8.6, 11.6, 14.4, 17.2], [
        scene("light", 0, 3.0,
            E(lines("Three weekends.", "One street.", '<span class="acc">Your fix.</span>', size=112), -0.45, 2.85, 700, "mask", d=1.0)),   # readable on frame 0
        scene("dark", 3.0, 11.6,
            *step(1, "Research.", "Study a climate problem<br>where you live.", 3.0, 5.8),
            *step(2, "Design.", "Plan a youth-led fix<br>for it.", 5.8, 8.6),
            *step(3, "Pitch.", "Learn to pitch it<br>for seed funding.", 8.6, 11.6, "There is no funding guarantee.")),
        scene("light", 11.6, 14.4,
            E(lines("3 virtual", '<span class="acc">weekends.</span>', size=150), 11.8, 14.3, 420, "mask", "c"),
            E('<span class="dot"></span><span class="dot"></span><span class="dot"></span>', 12.1, 14.3, 850, "fade", "c",
              extra='data-dots="12.4,12.7,13.0"'),
            E('<div class="body">Weekend 1 starts<br><b>Fri 13 Nov 2026</b></div>', 12.6, 14.3, 1110, "fade", "c")),
        scene("dark", 14.4, 17.2,
            E(lines("50 fellows.", '<span class="acc">Nigeria + Zambia.</span>', size=108), 14.6, 17.1, 600, "mask", "c"),
            E('<div class="body">For university students and<br>grassroots community volunteers,<br>aged 18+</div>', 15.2, 17.1, 900, "fade", "c")),
        end_scene(17.2, T),
    ]


# ---------------------------------------------------------------- build

def page(layers):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            + "".join(layers) + f"<script>{JS}</script></body></html>")


def finish_audio(src, out):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    s = json.loads(r.stderr[r.stderr.rindex("{"):])
    ff("-i", src, "-af", f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={s['input_i']}:measured_TP={s['input_tp']}"
       f":measured_LRA={s['input_lra']}:measured_thresh={s['input_thresh']}:offset={s['target_offset']}:linear=true",
       "-ar", 48000, out)


def build(name, total, hits, layers):
    html = WORK / f"{name}.html"
    html.write_text(page(layers))
    frames = WORK / f"{name}-frames"
    if frames.exists():
        shutil.rmtree(frames)
    run("node", HERE / "render_frames.js", html, frames, f"{total:.3f}", RENDER_FPS, "jpg")
    # blend pairs of 60 fps frames: a 180-degree shutter's worth of motion blur at 30 fps
    video = WORK / f"{name}-video.mp4"
    ff("-framerate", RENDER_FPS, "-i", frames / "%05d.jpg", "-vf", "tmix=frames=2,framestep=2,format=yuv420p",
       "-r", OUT_FPS, "-c:v", "libx264", "-profile:v", "high", "-crf", "15", "-preset", "slow", "-tune", "animation", video)
    bed = WORK / f"{name}-bed.wav"
    run(sys.executable, HERE / "ambient_bed.py", bed, f"{total:.2f}", *[f"{h:.2f}" for h in hits])
    finish_audio(bed, WORK / f"{name}-audio.wav")
    outs = [POST / f"{name}.mp4", POST / f"{name}-no-music.mp4"]
    ff("-i", video, "-i", WORK / f"{name}-audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
       "-shortest", "-movflags", "+faststart", outs[0])
    ff("-i", video, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
       "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", outs[1])
    if "--keep" not in sys.argv:
        shutil.rmtree(frames)
    return outs


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    WORK.mkdir(parents=True, exist_ok=True)
    if which in ("a", "all"):
        total, hits, layers = video_a_layers()
        for o in build("video-a-ycef-motion", total, hits, layers):
            print("built", o.relative_to(ROOT))
    if which in ("b", "all"):
        total, hits, layers = video_b_layers()
        for o in build("video-b-ycef-motion", total, hits, layers):
            print("built", o.relative_to(ROOT))
