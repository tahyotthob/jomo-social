"""Blender bone rig for Tobi and Amara, and the renderer for their reel frames.

Each character is a fine mesh carrying its illustration. Bones (hips, spine, neck/head and both arms,
upper arm + forearm) bend it smoothly, so heads nod and arms gesture without tearing. Mouth and blink
patches from assets/avatars/puppet are mixed in the material and keyed per frame.

Run with Blender's Python module (pip install bpy):
  python3 rig.py plan.json tobi out_dir [width]
plan.json comes from reel.py: {"fps": 30, "total": 33.4, "lines": [{"who", "start", "dur", "env", "gestures"}]}
Writes out_dir/00000.png ... (transparent, width x width*4/3).
"""
import bpy, json, math, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
PUP = ROOT / "assets/avatars/puppet"
W, H = 1080, 1440  # illustration frame in pixels; 1 Blender unit = 100 px

# Joints in illustration pixels (x right, y down), measured from the cut-outs.
# sigma: how far (px) a bone's influence reaches; gate: limits which pixels a bone may move.
CHARS = {
    "tobi": {
        "parts": ["closed", "mouth", "eyes"],
        "bones": {
            "hips":    {"a": (500, 1400), "b": (500, 700), "parent": None,    "sigma": 260, "gate": ("y>", 640)},
            "spine":   {"a": (500, 700),  "b": (500, 260), "parent": "hips",  "sigma": 170, "gate": ("y<", 760)},
            "head":    {"a": (505, 235),  "b": (505, 30),  "parent": "spine", "sigma": 120, "gate": ("y<", 262)},
            "armR_up": {"a": (680, 250),  "b": (790, 320), "parent": "spine", "sigma": 55,  "gate": ("x>", 640)},
            "armR_lo": {"a": (790, 320),  "b": (900, 150), "parent": "armR_up", "sigma": 55, "gate": ("x>", 740)},
            "armL_up": {"a": (390, 270),  "b": (270, 450), "parent": "spine", "sigma": 60,  "gate": ("x<", 400)},
            "armL_lo": {"a": (270, 450),  "b": (300, 520), "parent": "armL_up", "sigma": 60, "gate": ("x<", 360)},
        },
    },
    "amara": {
        "parts": ["mouth", "eyes"],
        "bones": {
            "hips":    {"a": (530, 1400), "b": (530, 680), "parent": None,    "sigma": 260, "gate": ("y>", 620)},
            "spine":   {"a": (530, 680),  "b": (540, 250), "parent": "hips",  "sigma": 170, "gate": ("y<", 740)},
            "head":    {"a": (545, 222),  "b": (545, 20),  "parent": "spine", "sigma": 120, "gate": ("y<", 248)},
            "armL_up": {"a": (420, 260),  "b": (330, 470), "parent": "spine", "sigma": 55,  "gate": ("x<", 440)},
            "armL_lo": {"a": (330, 470),  "b": (290, 270), "parent": "armL_up", "sigma": 50, "gate": ("x<", 400)},
            "armR_up": {"a": (650, 270),  "b": (700, 480), "parent": "spine", "sigma": 55,  "gate": ("x>", 620)},
            "armR_lo": {"a": (700, 480),  "b": (800, 420), "parent": "armR_up", "sigma": 70, "gate": ("x>", 660)},
        },
    },
}

def P(x, y):
    return ((x - W / 2) / 100, (H / 2 - y) / 100, 0)

def seg_dist(px, py, a, b):
    ax, ay = a; bx, by = b; dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def gated(g, x, y):
    k, v = g
    return {"y>": y > v, "y<": y < v, "x>": x > v, "x<": x < v}[k]

def build(name):
    cfg = CHARS[name]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=108, y_subdivisions=144, size=1)
    pl = bpy.context.object; pl.scale = (W / 100, H / 100, 1); bpy.ops.object.transform_apply(scale=True)
    # material: base image, mouth/blink patches mixed on top (factor keyed per frame), emission only
    mat = bpy.data.materials.new(name); mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()
    def img(path):
        n = nt.nodes.new("ShaderNodeTexImage"); n.image = bpy.data.images.load(str(path)); n.interpolation = "Cubic"; return n
    base = img(PUP / f"{name}-body.png"); color = base.outputs["Color"]; facs = {}
    for part in cfg["parts"]:
        t = img(PUP / f"{name}-{part}-patch.png")
        v = nt.nodes.new("ShaderNodeValue"); v.name = f"show_{part}"; v.outputs[0].default_value = 0; facs[part] = v
        mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
        nt.links.new(t.outputs["Alpha"], mul.inputs[0]); nt.links.new(v.outputs[0], mul.inputs[1])
        mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
        ins = [s for s in mix.inputs if s.enabled]  # Factor, A, B
        nt.links.new(mul.outputs[0], ins[0]); nt.links.new(color, ins[1]); nt.links.new(t.outputs["Color"], ins[2])
        color = [s for s in mix.outputs if s.enabled][0]
    em = nt.nodes.new("ShaderNodeEmission"); tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader"); out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(color, em.inputs["Color"]); nt.links.new(base.outputs["Alpha"], mx.inputs["Fac"])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs["Surface"])
    pl.data.materials.append(mat)
    # armature
    bpy.ops.object.armature_add(); arm = bpy.context.object; bpy.ops.object.mode_set(mode="EDIT")
    eb = arm.data.edit_bones; eb.remove(eb[0])
    for bn, b in cfg["bones"].items():
        e = eb.new(bn); e.head = P(*b["a"]); e.tail = P(*b["b"])
        if b["parent"]: e.parent = eb[b["parent"]]
    bpy.ops.object.mode_set(mode="OBJECT")
    # weights: gaussian falloff from each bone segment, limited by its gate, normalised
    groups = {bn: pl.vertex_groups.new(name=bn) for bn in cfg["bones"]}
    for v in pl.data.vertices:
        x = v.co.x * 100 + W / 2; y = H / 2 - v.co.y * 100
        ws = {}
        for bn, b in cfg["bones"].items():
            if not gated(b["gate"], x, y): continue
            d = seg_dist(x, y, b["a"], b["b"]); ws[bn] = math.exp(-(d / b["sigma"]) ** 2)
        if not ws: ws = {"hips": 1.0}
        s = sum(ws.values()) or 1
        for bn, w in ws.items():
            if w / s > 0.01: groups[bn].add([v.index], w / s, "REPLACE")
    pl.parent = arm; m = pl.modifiers.new("rig", "ARMATURE"); m.object = arm
    for pb in arm.pose.bones: pb.rotation_mode = "XYZ"
    # camera framing the illustration exactly
    bpy.ops.object.camera_add(location=(0, 0, 20)); cam = bpy.context.object
    cam.data.type = "ORTHO"; cam.data.ortho_scale = H / 100; sc.camera = cam
    sc.render.engine = "CYCLES"; sc.cycles.samples = 2; sc.cycles.use_denoising = False; sc.cycles.device = "CPU"
    sc.render.film_transparent = True; sc.view_settings.view_transform = "Standard"
    sc.cycles.max_bounces = 0; sc.cycles.transparent_max_bounces = 4
    return sc, arm, facs

# ---------------- animation ----------------
def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def bump(t, t0, dur):
    """0 -> 1 -> 0 over [t0, t0+dur], smooth."""
    if t < t0 or t > t0 + dur: return 0.0
    return math.sin(math.pi * (t - t0) / dur)

# gestures: name -> function(t_rel, dur) returning {bone: degrees}
def g_point(u, d):   # Tobi: lift the pointing arm a little higher, twice
    k = bump(u, 0, min(d, 1.6)); return {"armR_up": 10 * k, "armR_lo": 8 * k, "head": 3 * k}
def g_wave(u, d):    # Tobi: forearm waves
    k = ease(u / 0.3) * ease((d - u) / 0.3); return {"armR_up": 12 * k, "armR_lo": 22 * k * math.sin(u * 12)}
def g_surprise(u, d):  # Tobi: head back, arm drops a bit
    k = bump(u, 0, min(d, 1.2)); return {"head": -7 * k, "spine": -2 * k, "armR_up": -10 * k}
def g_finger(u, d):  # Amara: raised finger bobs as she makes a point
    k = ease(u / 0.3) * ease((d - u) / 0.3); return {"armL_lo": -6 * k * (0.5 + 0.5 * math.sin(u * 7)), "armL_up": -3 * k, "head": 2 * k}
def g_tap(u, d):     # Amara: lifts the tablet towards camera and taps
    k = ease(u / 0.35) * ease((d - u) / 0.35); return {"armR_up": -6 * k, "armR_lo": 10 * k + 3 * k * math.sin(u * 9), "head": -3 * k}
def g_nod(u, d):
    k = bump(u, 0, min(d, 0.9)); return {"head": -5 * k, "spine": 1 * k}
GESTURES = {"point": g_point, "wave": g_wave, "surprise": g_surprise, "finger": g_finger, "tap": g_tap, "nod": g_nod}

def animate(sc, arm, facs, plan, name):
    fps = plan["fps"]; n = int(plan["total"] * fps)
    sc.frame_start, sc.frame_end = 0, n - 1; sc.render.fps = fps
    lines = [l for l in plan["lines"]]
    # blinks, seeded so renders repeat exactly
    seed = 3 if name == "tobi" else 11; blinks = []; t = 0.8
    while t < plan["total"]:
        seed = (seed * 16807) % 2147483647; t += 2.2 + 2.8 * seed / 2147483647; blinks.append(t)
    pb = arm.pose.bones; phase = 0 if name == "tobi" else 1.7
    for f in range(n):
        t = f / fps
        rot = {b: 0.0 for b in pb.keys()}
        # idle: breathing and sway
        rot["spine"] += 0.8 * math.sin(t * 1.3 + phase); rot["head"] += 1.2 * math.sin(t * 0.9 + phase)
        loud = -1
        for l in lines:
            u = t - l["start"]
            if l["who"] == name and 0 <= u < l["dur"]:
                i = int(u * fps); loud = l["env"][i] if i < len(l["env"]) else 0
                rot["spine"] += (2.0 if name == "tobi" else -2.0) * ease(u / 0.4)       # lean in while speaking
                rot["head"] += -3.0 * max(0, loud) * (1 if name == "tobi" else -1)     # small nods on stressed syllables
            g = l.get("gestures", {}).get(name)
            if g and 0 <= u < l["dur"] + 0.4:
                for b, deg in GESTURES[g](u, l["dur"] + 0.4).items(): rot[b] += deg
        for b, deg in rot.items():
            pb[b].rotation_euler = (0, 0, math.radians(deg)); pb[b].keyframe_insert("rotation_euler", frame=f)
        # mouth and blink
        show = {k: 0.0 for k in facs}
        if loud >= 0:
            if "closed" in facs:
                if loud < 0.18: show["closed"] = 1.0
                elif loud > 0.55: show["mouth"] = 1.0
            elif loud > 0.22: show["mouth"] = 1.0
        if "eyes" in facs and any(b <= t < b + 4 / fps for b in blinks): show["eyes"] = 1.0
        for k, v in facs.items():
            v.outputs[0].default_value = show[k]; v.outputs[0].keyframe_insert("default_value", frame=f)
    # constant interpolation for mouth/blink keys so they switch crisply
    for act in bpy.data.actions:
        for fc in getattr(act, "fcurves", []):
            if "default_value" in fc.data_path:
                for k in fc.keyframe_points: k.interpolation = "CONSTANT"
    return n

if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    plan_path, name, outdir = args[0], args[1], pathlib.Path(args[2]); width = int(args[3]) if len(args) > 3 else 640
    plan = json.loads(pathlib.Path(plan_path).read_text())
    sc, arm, facs = build(name)
    n = animate(sc, arm, facs, plan, name)
    sc.render.resolution_x = width; sc.render.resolution_y = round(width * H / W)
    outdir.mkdir(parents=True, exist_ok=True)
    sc.render.filepath = str(outdir / "#####"); sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
    only = [int(a) for a in args[4].split(",")] if len(args) > 4 else None
    if only:
        for f in only:
            sc.frame_set(f); sc.render.filepath = str(outdir / f"{f:05d}"); bpy.ops.render.render(write_still=True)
    else:
        bpy.ops.render.render(animation=True)
    print("rendered", name, n if not only else len(only), "frames")
