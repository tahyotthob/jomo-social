"""Build a Tobi-and-Amara reel: lines.json -> HTML scene -> frames -> MP4 (1080x1920, 30 fps).
With voice files (from tts.py) the timing and mouths follow the audio; without them it makes a
silent rig test with estimated timing and a synthetic mouth envelope.
Usage (from repo root): python3 tools/video/avatar/reel.py lines.json voice_dir out.mp4 [--blender]
--blender renders the characters with the Blender bone rig (blender/rig.py) instead of the 2D puppet."""
import json, sys, pathlib, subprocess, wave, math, re
ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).parent
FS = ROOT / "tools/node_modules/@fontsource"
FPS = 30

def est_env(text):
    # silent test: ~2.7 words a second, a mouth pulse per syllable-ish
    words = len(text.split()); dur = max(0.8, words / 2.7); n = int(dur * FPS)
    syl = max(1, len(re.findall(r"[aeiouy]+", text.lower())))
    return [round(max(0, math.sin(i / n * syl * math.pi)) * (0.9 if i < n - 3 else 0), 3) for i in range(n)]

def main(lines_path, voice_dir, out):
    lines = json.loads(pathlib.Path(lines_path).read_text()); vd = pathlib.Path(voice_dir)
    t = 1.2; plan = []; audio = []
    for l in lines:
        wav = vd / f'{l["id"]}-{l["who"]}.wav'; envf = vd / f'{l["id"]}-{l["who"]}.env.json'
        if wav.exists():
            with wave.open(str(wav)) as w: dur = w.getnframes() / w.getframerate()
            env = json.loads(envf.read_text()); audio.append((t, wav))
        else:
            env = est_env(l["text"]); dur = len(env) / FPS
        plan.append({**l, "start": round(t, 3), "dur": round(dur, 3), "env": env}); t += dur + 0.35
    total = t + 1.6
    seq = "null"
    if "--blender" in sys.argv:
        plan_file = HERE / "_plan.json"; plan_file.write_text(json.dumps({"fps": FPS, "total": total, "lines": plan}))
        chars = HERE / "_chars"; subprocess.run(["rm", "-rf", str(chars)])
        for who in ("tobi", "amara"):
            subprocess.run(["python3", str(HERE / "blender/rig.py"), str(plan_file), who, str(chars / who), "640"], check=True)
        seq = json.dumps({"tobi": f"file://{chars / 'tobi'}", "amara": f"file://{chars / 'amara'}", "frames": int(total * FPS)})
    html = (HERE / "reel_template.html").read_text()
    html = html.replace("__FS__", f"file://{FS}").replace("__PUP__", f"file://{ROOT}/assets/avatars/puppet") \
               .replace("__LOGO__", f"file://{ROOT}/assets/logos/jomo-logo.png").replace("__PLAN__", json.dumps(plan)) \
               .replace("__TOTAL__", str(round(total, 2))).replace("__JS__", f"file://{HERE}/puppet.js").replace("__SEQ__", seq)
    page = HERE / "_reel.html"; page.write_text(html)
    frames = HERE / "_frames"; subprocess.run(["rm", "-rf", str(frames)])
    subprocess.run(["node", str(HERE.parent / "render_frames.js"), str(page), str(frames), str(total), str(FPS), "jpg"], check=True)
    v = ["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "%05d.jpg")]
    if audio:
        for st, w in audio: v += ["-itsoffset", str(st), "-i", str(w)]
        mix = "".join(f"[{i+1}:a]" for i in range(len(audio)))
        v += ["-filter_complex", f"{mix}amix=inputs={len(audio)}:normalize=0,apad[a]", "-map", "0:v", "-map", "[a]", "-shortest", "-c:a", "aac", "-b:a", "160k"]
    v += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", str(out)]
    subprocess.run(v, check=True); subprocess.run(["rm", "-rf", str(frames), str(HERE / "_chars")])
    print("wrote", out, f"{total:.1f}s", "with voice" if audio else "silent rig test")

if __name__ == "__main__":
    main(*[a for a in sys.argv[1:] if not a.startswith("--")][:3])
