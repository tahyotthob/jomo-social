"""Build the two YCEF 2026 videos from the operator's CapCut AI clips (2026-10-22).

    python ycef_videos.py [a|b|all] [--keep]

Video A, promo reel: the clean AI gully shot from VID-20261022-WA0193, a real
JOMO clean-up photo, then brand cards and the end card.
Video B, AI avatar explainer: the avatar's accurate lines from
VID-20261022-WA0017 (voice separated from CapCut's background music), with
brand cards for everything she got wrong.

Each video is written twice: with the team-made music bed (music_bed.py) and
without music (for adding Meta Sound Collection music in the app, and for
LinkedIn and X).

Rules applied (team review, 2026-10-22): no AI people who look under 18 and no
crested uniforms; programme facts only on brand cards, never over AI people;
"AI-generated visuals" / "AI avatar" labels on screen; the "CapCut AI" mark is
never cropped or covered (frames are trimmed at the bottom only); all text is
added here, none comes from the generator.

Needs ffmpeg, numpy, Node with tools/node_modules (playwright) and Chromium
(CHROMIUM_PATH). Working files go to $VIDEO_WORK (default /tmp/jomo-video-work).
"""
import html, json, os, pathlib, shutil, subprocess, sys, wave

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
POST = ROOT / "content/posts/2026-10-22-ycef-videos"
SRC_A = POST / "source/v1-promo-VID-20261022-WA0193.mp4"
SRC_B = POST / "source/v2-avatar-VID-20261022-WA0017.mp4"
VOICE_B = POST / "source/v2-avatar-voice-only.wav"   # separate_voice.py output, music removed
PHOTO = ROOT / "assets/photos/events/oniwaya-cleanup/oniwaya-cleanup-11.jpg"   # consent row in content/consent-log.csv
FS = ROOT / "tools/node_modules/@fontsource"
LOGO = ROOT / "assets/logos/jomo-logo-light.png"
WORK = pathlib.Path(os.environ.get("VIDEO_WORK", "/tmp/jomo-video-work"))
FPS = 25
SR = 48000
INK, LIME, LEAF, OLIVE, CHAR, OFF = "#1E2220", "#A5CD39", "#8FB73C", "#77962A", "#323534", "#F4F6EC"
HANDLE = "@jomoclimatechange"   # operator still confirming against @jomoclimate
LINK = "jomoclimatechange.org/events?apply=ycef"


def run(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def ff(*args):
    run("ffmpeg", "-v", "error", "-y", *args)


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True, check=True).stdout)


# ---------------------------------------------------------------- overlay page

CSS = f"""
@font-face {{ font-family: Anton; src: url('file://{FS}/anton/files/anton-latin-400-normal.woff2'); }}
@font-face {{ font-family: Brico; font-weight: 800; src: url('file://{FS}/bricolage-grotesque/files/bricolage-grotesque-latin-800-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 400; src: url('file://{FS}/lato/files/lato-latin-400-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 700; src: url('file://{FS}/lato/files/lato-latin-700-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 900; src: url('file://{FS}/lato/files/lato-latin-900-normal.woff2'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:transparent; font-family:Lato; color:{OFF}; }}
.l {{ position:absolute; opacity:0; will-change:transform,opacity; }}
.full {{ left:0; top:0; width:1080px; height:1920px; }}
.ink {{ background:{INK}; color:{OFF}; }}
.lime {{ background:{LIME}; color:{INK}; }}
.off {{ background:{OFF}; color:{INK}; }}
.center {{ display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }}
.label {{ font-weight:900; font-size:30px; letter-spacing:.2em; text-transform:uppercase; }}
.anton {{ font-family:Anton; text-transform:uppercase; line-height:.95; letter-spacing:.005em; }}
.brico {{ font-family:Brico; font-weight:800; line-height:.98; letter-spacing:-.02em; }}
.pill {{ font-weight:700; font-size:24px; letter-spacing:.16em; text-transform:uppercase; padding:14px 26px 14px 22px;
         border-radius:40px; background:{INK}; color:{OFF}; display:flex; align-items:center; gap:12px; z-index:50; }}
.pill i {{ width:14px; height:14px; border-radius:50%; background:{LIME}; display:block; }}
.tape {{ font-weight:900; font-size:36px; letter-spacing:.16em; padding:20px 48px; text-transform:uppercase;
         background:{LIME}; color:{INK}; white-space:nowrap; }}
.cap {{ left:90px; width:900px; top:1062px; height:168px; padding:0 30px;
        display:flex; align-items:center; justify-content:center; text-align:center;
        font-weight:900; font-size:54px; line-height:1.1; color:{OFF}; }}
.cap b {{ color:{LIME}; font-weight:900; }}
.foot {{ left:90px; width:900px; top:1500px; height:110px; border-top:2px solid rgba(244,246,236,.25);
         display:flex; align-items:center; gap:16px; font-weight:700; font-size:30px; letter-spacing:.04em; }}
.foot svg {{ width:38px; height:38px; }}
"""

# Each layer animates in at data-in and out at data-out. The page is rendered frame by frame,
# so the animation is computed from t rather than left to CSS timing.
JS = """
const ease = t => 1 - Math.pow(1 - t, 3);
const clamp = x => Math.max(0, Math.min(1, x));
window.render = function (t) {
  document.querySelectorAll('[data-in]').forEach(el => {
    const tin = +el.dataset.in, tout = +(el.dataset.out || 1e9);
    const d = +(el.dataset.dur || 0.35), dOut = +(el.dataset.dout || 0.25), kind = el.dataset.anim || 'fade';
    const live = t >= tin && t < tout;
    const pin = kind === 'none' ? 1 : ease(clamp((t - tin) / d));
    const pout = el.dataset.hold ? 1 : 1 - ease(clamp((t - (tout - dOut)) / dOut));
    const p = live ? Math.min(pin, pout) : 0;
    let o = p, tr = '';
    if (kind === 'up') tr = `translateY(${(1 - p) * 70}px)`;
    if (kind === 'slide') { tr = `translateX(${(1 - pin) * 1080}px)`; o = live ? 1 : 0; }
    if (kind === 'rise') { tr = `translateY(${(1 - pin) * 1920}px)`; o = live ? 1 : 0; }
    el.style.opacity = o; el.style.transform = tr + (el.dataset.rot ? ` rotate(${el.dataset.rot}deg)` : '');
  });
};
"""


def icons():
    ig = (f'<svg viewBox="0 0 24 24" fill="none" stroke="{OFF}" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/>'
          f'<circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="{OFF}" stroke="none"/></svg>')
    # brand guide: the handle bar carries the Instagram and LinkedIn icons (same marks as tools/build.py)
    li = (f'<svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="4" fill="{OFF}"/>'
          f'<rect x="6" y="10" width="2.6" height="8" fill="{INK}"/><circle cx="7.3" cy="6.9" r="1.6" fill="{INK}"/>'
          f'<path d="M11 10h2.5v1.2c.5-.8 1.5-1.4 2.8-1.4 2 0 3 1.2 3 3.6V18h-2.6v-4.2c0-1.2-.4-1.9-1.4-1.9s-1.7.7-1.7 1.9V18H11z" fill="{INK}"/></svg>')
    return ig + li


def layer(inner, t_in, t_out, cls="", style="", anim="fade", dur=0.35, dout=0.25, hold=False):
    attrs = f'data-in="{t_in:.3f}" data-out="{t_out:.3f}" data-anim="{anim}" data-dur="{dur}" data-dout="{dout}"'
    if hold:
        attrs += ' data-hold="1"'
    return f'<div class="l {cls}" style="{style}" {attrs}>{inner}</div>'


def pill(text, t_in, t_out, side="left"):
    return layer(f"<i></i>{text}", t_in, t_out, cls="pill", style=f"{side}:60px;top:300px", anim="none", hold=True)


def end_card(t_in, t_out, disclosure):
    """Full-screen Ink end card rising from the bottom. Everything sits inside the 4:5 feed crop."""
    inner = f"""
      <img src="file://{LOGO}" style="position:absolute;left:250px;top:300px;width:580px">
      <div class="label" style="position:absolute;left:0;width:1080px;top:640px;text-align:center;color:{LIME};font-size:28px">Young Climate Educators Fellowship</div>
      <div class="brico" style="position:absolute;left:0;width:1080px;top:700px;text-align:center;font-size:78px">Applications close</div>
      <div class="anton" style="position:absolute;left:0;width:1080px;top:800px;text-align:center;font-size:210px;color:{LIME}">Mon 26 Oct</div>
      <div style="position:absolute;left:0;width:1080px;top:1075px;display:flex;justify-content:center">
        <div class="tape" style="transform:rotate(-3deg)">Apply now</div></div>
      <div style="position:absolute;left:0;width:1080px;top:1220px;text-align:center;font-weight:700;font-size:38px">{html.escape(LINK)}</div>
      <div style="position:absolute;left:110px;width:860px;top:1318px;text-align:center;font-size:28px;line-height:1.35;opacity:.8">{disclosure}</div>
      <div class="foot" style="position:absolute">{icons()}<span>{HANDLE}</span></div>
    """
    return layer(inner, t_in, t_out, cls="full ink", anim="rise", dur=0.45, hold=True)


def card(inner, theme, t_in, t_out):
    return layer(inner, t_in, t_out, cls=f"full {theme} center", style="padding:0 80px", anim="slide", dur=0.35, hold=True)


def page(layers):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{''.join(layers)}<script>{JS}</script></body></html>"""


def render_overlay(name, layers, seconds):
    page_path = WORK / f"{name}.html"
    page_path.write_text(page(layers))
    frames = WORK / f"{name}-frames"
    if frames.exists():
        shutil.rmtree(frames)
    run("node", HERE / "render_frames.js", page_path, frames, f"{seconds:.3f}", FPS)
    return frames


# ---------------------------------------------------------------- picture

def clip(src, start, length, out, slow=1.0, avatar=False):
    """Cut, slow and scale a CapCut clip to 1080x1920, trimming only at the bottom so the
    "CapCut AI" mark in the top-left corner stays whole."""
    vf = [f"setpts={slow}*PTS", f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"] if slow != 1 else [f"fps={FPS}"]
    vf += ["scale=1080:-2:flags=lanczos", "crop=1080:1920:0:0"]
    vf += ["unsharp=5:5:0.7:5:5:0.0", "eq=contrast=1.03:saturation=1.04", "noise=alls=3:allf=t"] if avatar else ["eq=contrast=1.04:saturation=1.06"]
    ff("-ss", f"{start:.3f}", "-t", f"{length:.3f}", "-i", src, "-an", "-vf", ",".join(vf),
       "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", out)


def photo_clip(seconds, out, zoom=0.06):
    """Slow push-in on the real clean-up photo, cropped to 9:16 around the volunteer."""
    n = round(seconds * FPS)
    ff("-loop", "1", "-i", PHOTO, "-vf",
       "crop=788:1400:30:0,scale=2160:3840:flags=lanczos,"
       f"zoompan=z='1+{zoom}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps={FPS},"
       "eq=contrast=1.03:saturation=1.05",
       "-frames:v", n, "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", out)


def solid(seconds, out):
    ff("-f", "lavfi", "-i", f"color=c={INK}:s=1080x1920:r={FPS}", "-t", f"{seconds:.3f}",
       "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", out)


def concat(parts, out):
    lst = WORK / (pathlib.Path(out).stem + ".txt")
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out)


# ---------------------------------------------------------------- sound

def read_wav(path):
    with wave.open(str(path)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels())


def write_wav(path, x):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def voice_snippet(start, end):
    x = read_wav(VOICE_B)[int(start * SR):int(end * SR)].copy()
    f = int(0.015 * SR)
    x[:f] *= np.linspace(0, 1, f)[:, None]
    x[-f:] *= np.linspace(1, 0, f)[:, None]
    return x


def music(seconds, out):
    run(sys.executable, HERE / "music_bed.py", out, f"{seconds:.2f}")
    return read_wav(out)


def finish_audio(mix, out, target=-14):
    """Two-pass loudness normalisation (-14 LUFS, -1 dBTP), the level Instagram and Facebook play reels at."""
    raw = WORK / (pathlib.Path(out).stem + "-raw.wav")
    write_wav(raw, mix)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af", f"loudnorm=I={target}:TP=-1.0:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    s = json.loads(r.stderr[r.stderr.rindex("{"):])
    ff("-i", raw, "-af", f"loudnorm=I={target}:TP=-1.0:LRA=11:measured_I={s['input_i']}:measured_TP={s['input_tp']}"
       f":measured_LRA={s['input_lra']}:measured_thresh={s['input_thresh']}:offset={s['target_offset']}:linear=true",
       "-ar", SR, out)


def composite(base, frames, audio, out, seconds):
    inputs = ["-i", base, "-framerate", FPS, "-i", frames / "%05d.png"]
    maps = ["-map", "[v]"]
    if audio:
        inputs += ["-i", audio]
        maps += ["-map", "2:a", "-c:a", "aac", "-b:a", "192k"]
    ff(*inputs, "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]", *maps,
       "-t", f"{seconds:.3f}", "-c:v", "libx264", "-profile:v", "high", "-crf", "18", "-preset", "slow", "-r", FPS,
       "-movflags", "+faststart", out)


def silent_track(seconds, out):
    write_wav(out, np.zeros((int(seconds * SR), 2), np.float32))


# ---------------------------------------------------------------- Video A: promo reel

A_GULLY = (f'<div class="label" style="color:{LIME}">YCEF 2026</div>'
           f'<div class="brico" style="font-size:88px;margin-top:22px">Your street has<br>a climate problem.</div>')
A_FIX = (f'<div class="brico" style="font-size:112px;color:{LIME}">You&rsquo;ve got<br>the fix.</div>'
         f'<div style="font-weight:700;font-size:30px;margin-top:20px;opacity:.85">Real JOMO volunteer clearing a drain, Oniwaya clean-up</div>')
A_CARD_1 = (f'<div class="label" style="opacity:.75">Young Climate Educators Fellowship</div>'
            f'<div class="anton" style="font-size:250px;margin-top:40px">50 fellows</div>'
            f'<div style="font-weight:900;font-size:60px;margin-top:30px">Nigeria + Zambia</div>')
A_CARD_2 = (f'<div class="anton" style="font-size:150px">3 virtual<br><span style="color:{LIME}">weekends</span></div>'
            f'<div style="font-weight:900;font-size:56px;margin-top:44px">Starts Fri 13 Nov 2026</div>'
            f'<div style="font-weight:400;font-size:42px;margin-top:34px;line-height:1.35;opacity:.9">For university students and grassroots<br>community volunteers, aged 18+</div>')
A_DISCLOSURE = "The opening scene is AI-generated, not a real place or JOMO event. The clean-up photo is real."


def video_a():
    gully, photo = WORK / "a-gully.mp4", WORK / "a-photo.mp4"
    # Two people-free stretches of the polluted gully, slowed 2x: the brown water after the man in the crested
    # polo has dissolved out (0.86-1.22 s), then the cascade (2.00-2.92 s) before the sketchbook dissolves in.
    # The ridge shot between them (1.28-1.92 s) is left out: one of its AI figures could pass for a child.
    clip(SRC_A, 0.86, 0.36, WORK / "a-gully1.mp4", slow=2.0)
    clip(SRC_A, 2.00, 0.92, WORK / "a-gully2.mp4", slow=2.0)
    concat([WORK / "a-gully1.mp4", WORK / "a-gully2.mp4"], gully)
    photo_clip(2.6, photo)
    t1 = dur(gully)
    t2 = t1 + dur(photo)
    t3 = t2 + 1.9          # card 1
    t_end = t3 + 2.7       # card 2
    total = t_end + 4.6
    solid(total - t2 + 0.2, WORK / "a-cards.mp4")
    concat([gully, photo, WORK / "a-cards.mp4"], WORK / "a-base.mp4")

    layers = [
        # the band covers the text CapCut burned into the gully shot; it runs edge to edge because that text does
        layer("", 0, t1, style=f"left:0;top:780px;width:1080px;height:440px;background:{INK};box-shadow:0 18px 60px rgba(0,0,0,.35)",
              anim="none", hold=True),
        layer("", 0, t1, style=f"left:0;top:780px;width:1080px;height:12px;background:{LIME}", anim="none", hold=True),
        # the hook starts just before frame 0 so it is already readable on the first frame
        layer(A_GULLY, -0.3, t1, cls="center", style="left:0;top:792px;width:1080px;height:428px;padding:0 80px", anim="up", dur=0.4, hold=True),
        pill("AI-generated visuals", 0, t1),
        # the real photo keeps the volunteer's hands clear, so its band sits lower
        layer("", t1, t2, style=f"left:0;top:1300px;width:1080px;height:330px;background:{INK}", anim="none", hold=True),
        layer("", t1, t2, style=f"left:0;top:1300px;width:1080px;height:12px;background:{LIME}", anim="none", hold=True),
        layer(A_FIX, t1, t2, cls="center", style="left:0;top:1312px;width:1080px;height:318px;padding:0 70px", anim="up", dur=0.35, hold=True),
        pill("Real photo &middot; JOMO archive", t1, t2),
        card(A_CARD_1, "lime", t2, t3 + 0.5),
        card(A_CARD_2, "ink", t3, t_end + 0.5),
        end_card(t_end, total + 1, A_DISCLOSURE),
    ]
    frames = render_overlay("a-overlay", layers, total)
    outs = []
    bed = music(total, WORK / "a-bed.wav")
    finish_audio(bed, WORK / "a-audio.wav")
    outs.append(POST / "video-a-ycef-promo.mp4")
    composite(WORK / "a-base.mp4", frames, WORK / "a-audio.wav", outs[-1], total)
    silent_track(total, WORK / "a-silent.wav")
    outs.append(POST / "video-a-ycef-promo-no-music.mp4")
    composite(WORK / "a-base.mp4", frames, WORK / "a-silent.wav", outs[-1], total)
    return outs, total


# ---------------------------------------------------------------- Video B: AI avatar explainer

B_LINE_1 = (0.28, 3.70)   # "...climate action training programme for young people in Nigeria and Zambia" (starts after the garbled first word)
B_LINE_2 = (4.605, 5.78)  # "selecting 50 fellows": starts at its own "s" (4.61), after the garbled syllable; ends before the wrong dates
B_LINE_3 = (8.52, 9.16)   # "Apply now" (after the glass board has gone; ends before the wrong web address)
B_CAPTIONS_1 = [(-0.10, 1.18, "Climate action training programme"), (1.18, 1.92, "for young people"),
                (1.92, None, "in <b>Nigeria</b> and <b>Zambia</b>")]
B_CARD_1 = (f'<div class="label" style="opacity:.75">YCEF 2026</div>'
            f'<div style="font-weight:900;font-size:50px;letter-spacing:.14em;text-transform:uppercase;margin-top:60px">Selecting</div>'
            f'<div class="anton" style="font-size:250px;margin-top:10px">50 fellows</div>'
            f'<div style="font-weight:700;font-size:56px;margin-top:26px">across Nigeria + Zambia</div>')
B_CARD_2 = (f'<div class="anton" style="font-size:420px;color:{LIME};line-height:.9">3</div>'
            f'<div class="anton" style="font-size:140px">virtual weekends</div>'
            f'<div style="font-weight:900;font-size:56px;margin-top:40px">Starts Fri 13 Nov 2026</div>')
B_CARD_3 = (f'<div class="label" style="color:{OLIVE}">What fellows do</div>'
            f'<div class="brico" style="font-size:96px;margin-top:40px">Research a local<br>climate problem.</div>'
            f'<div class="brico" style="font-size:96px;margin-top:34px">Design a<br>youth-led fix.</div>'
            f'<div style="font-weight:700;font-size:44px;margin-top:50px;line-height:1.35">Learn to pitch for seed funding.<br>'
            f'<span style="font-weight:400">No funding guarantee.</span></div>')
B_DISCLOSURE = "The presenter is an AI avatar, not a JOMO team member."


def video_b():
    s1, s3 = WORK / "b-line1.mp4", WORK / "b-line3.mp4"
    clip(SRC_B, B_LINE_1[0], B_LINE_1[1] - B_LINE_1[0] - 0.02, s1, avatar=True)
    clip(SRC_B, B_LINE_3[0], B_LINE_3[1] - B_LINE_3[0], s3, avatar=True)
    t_cards = dur(s1)
    c2, c3 = t_cards + 1.85, t_cards + 3.75
    t_apply = t_cards + 6.3
    t_end = t_apply + dur(s3)
    total = t_end + 4.6
    solid(t_apply - t_cards, WORK / "b-cards.mp4")
    solid(total - t_end + 0.2, WORK / "b-end.mp4")
    concat([s1, WORK / "b-cards.mp4", s3, WORK / "b-end.mp4"], WORK / "b-base.mp4")

    cap_box = f"left:90px;width:900px;top:1062px;height:168px;background:{INK};border-radius:22px"
    layers = [
        layer("", 0, t_cards, style="left:0;top:1300px;width:1080px;height:620px;"
              "background:linear-gradient(rgba(30,34,32,0),rgba(30,34,32,.88) 45%)", anim="none", hold=True),
        layer(f'<div class="label" style="color:{LIME}">YCEF 2026</div>'
              f'<div class="brico" style="font-size:50px;margin-top:10px;white-space:nowrap">Young Climate Educators Fellowship</div>'
              f'<div style="font-weight:700;font-size:30px;margin-top:14px;line-height:1.3">For ages 18+: university students and<br>grassroots community volunteers</div>',
              0.2, t_cards, style="left:90px;top:1420px;width:900px", anim="up", dur=0.4, hold=True),
        # the caption box also covers the garbled caption CapCut burned into the "Apply now" shot
        layer("", 0, t_cards, style=cap_box, anim="none", hold=True),
        layer("", t_apply, t_end, style=cap_box, anim="none", hold=True),
    ]
    for s, e, text in B_CAPTIONS_1:
        layers.append(layer(f"<span>{text}</span>", s, t_cards if e is None else e, cls="cap", anim="fade", dur=0.08, dout=0.06,
                            hold=e is None))
    layers.append(layer("<span>Apply now.</span>", t_apply, t_end, cls="cap", anim="none", hold=True))
    layers += [
        card(B_CARD_1, "lime", t_cards, c2 + 0.5),
        card(B_CARD_2, "ink", c2, c3 + 0.5),
        card(B_CARD_3, "off", c3, t_apply + 0.04),
        pill("AI avatar", 0, t_end),   # on from the first frame until the end card, over the cards too
        end_card(t_end, total + 1, B_DISCLOSURE),
    ]
    frames = render_overlay("b-overlay", layers, total)

    n = int(total * SR)
    voice = np.zeros((n, 2), np.float32)
    marks = [(0.0, voice_snippet(*B_LINE_1)), (t_cards + 0.22, voice_snippet(*B_LINE_2)), (t_apply, voice_snippet(*B_LINE_3))]
    for t, v in marks:
        i = int(t * SR)
        voice[i:i + len(v)] += v[: n - i]
    outs = []
    bed = music(total, WORK / "b-bed.wav")[:n]
    gate = np.zeros(n, np.float32)
    for t, v in marks:
        i = int((t - 0.15) * SR)
        gate[max(i, 0): i + len(v) + int(0.3 * SR)] = 1
    k = int(0.12 * SR)
    gate = np.convolve(gate, np.ones(k) / k, "same")
    duck = 10 ** ((-15 * gate) / 20)
    finish_audio(voice + bed * 0.55 * duck[:, None], WORK / "b-audio.wav")
    outs.append(POST / "video-b-ycef-ai-avatar.mp4")
    composite(WORK / "b-base.mp4", frames, WORK / "b-audio.wav", outs[-1], total)
    finish_audio(voice, WORK / "b-voice.wav", target=-16)
    outs.append(POST / "video-b-ycef-ai-avatar-voice-only.mp4")
    composite(WORK / "b-base.mp4", frames, WORK / "b-voice.wav", outs[-1], total)

    srt = [(0.0, 1.18, "Climate action training programme"), (1.18, 1.92, "for young people"),
           (1.92, t_cards, "in Nigeria and Zambia"), (t_cards + 0.22, t_cards + 0.22 + B_LINE_2[1] - B_LINE_2[0], "Selecting 50 fellows"),
           (t_apply, t_end, "Apply now.")]
    stamp = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}"
    (POST / "video-b-ycef-ai-avatar.srt").write_text(
        "\n".join(f"{i}\n{stamp(a)} --> {stamp(b)}\n{txt}\n" for i, (a, b, txt) in enumerate(srt, 1)))
    return outs, total


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    WORK.mkdir(parents=True, exist_ok=True)
    built = []
    if which in ("a", "all"):
        built.append(video_a())
    if which in ("b", "all"):
        built.append(video_b())
    for outs, total in built:
        for out in outs:
            print(f"built {out.relative_to(ROOT)} ({total:.2f} s)")
    if "--keep" not in sys.argv:
        for d in WORK.glob("*-frames"):
            shutil.rmtree(d)
