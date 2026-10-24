"""Stage 3: skin weights and the face rig.

Weights are computed by script (not Blender's bone-heat solver), so they are the same every run:
  1. every vertex scores each allowed deform bone by its distance to the bone segment minus that
     bone's typical flesh radius (measured on the body), so thick and thin parts compete fairly;
  2. score -> weight with a soft falloff, then a few rounds of smoothing over the mesh edges;
  3. keep the 4 strongest bones per vertex (game-engine friendly) and normalise.
Each mesh part only listens to the bones it can sensibly follow (shirt: torso and arms, trousers:
hips and legs, shoes: feet ...). Head pieces and hand-held props are rigid.

Face rig: shape keys on NAME_eyes, NAME_brows and NAME_mouth with the same names on both characters,
each driven by a custom property of the same name on NAME_rig (0-1). Animations key the rig props,
so one Action drives body and face on either character.
Output: blender/work/stage3.blend
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_point_line

FACE_PROPS = ["blink", "blink_L", "blink_R", "smile", "frown", "open", "sad", "surprise",
              "vis_A", "vis_E", "vis_O", "vis_U", "vis_MBP", "vis_FV"]

TORSO = ["hips", "spine_01", "spine_02", "spine_03", "neck", "shoulder.L", "shoulder.R"]
ARMS = [f"{b}{s}" for s in (".L", ".R") for b in ("upper_arm", "forearm")]
LEGS = [f"{b}{s}" for s in (".L", ".R") for b in ("thigh", "shin")]
FEET = [f"{b}{s}" for s in (".L", ".R") for b in ("shin", "foot", "toe")]
RIGID = {"head": ("head", "hair", "eyes", "brows", "mouth", "glasses", "bandana"),
         "hand.R": ("phone",), "hand.L": ("tablet",)}

def segs(rig, names):
    mw = rig.matrix_world
    return {n: (mw @ rig.data.bones[n].head_local, mw @ rig.data.bones[n].tail_local) for n in names}

def seg_dist(p, a, b):
    q, t = intersect_point_line(p, a, b); t = min(max(t, 0.0), 1.0)
    return (p - (a + (b - a) * t)).length

def flesh_radii(body, S):
    """Median distance from each bone to the body vertices nearest to it."""
    near = {n: [] for n in S}
    for v in body.data.vertices:
        p = body.matrix_world @ v.co
        d = {n: seg_dist(p, *S[n]) for n in S}; n = min(d, key=d.get); near[n].append(d[n])
    out = {}
    for n, ds in near.items():
        ds.sort(); out[n] = ds[len(ds) // 2] if ds else 0.02
    return out

def compute_weights(ob, S, R, allowed_for, smooth=3):
    """allowed_for(vertex_index) -> list of bone names. Returns list of {bone: weight}."""
    me = ob.data; W = []
    for v in me.vertices:
        p = ob.matrix_world @ v.co; names = allowed_for(v.index)
        sc = {n: seg_dist(p, *S[n]) - R[n] for n in names}
        best = min(sc.values()); nb = min(sc, key=sc.get)
        sig = min(max(0.35 * R[nb], 0.0025), 0.02)
        w = {n: math.exp(-(s - best) / sig) for n, s in sc.items() if s - best < 6 * sig}
        W.append(w)
    nbrs = [[] for _ in me.vertices]
    for e in me.edges:
        a, b = e.vertices; nbrs[a].append(b); nbrs[b].append(a)
    for _ in range(smooth):
        new = []
        for i, w in enumerate(W):
            acc = {k: v * 0.5 for k, v in w.items()}; ns = nbrs[i]
            allowed = set(allowed_for(i))
            for j in ns:
                for k, v in W[j].items():
                    if k in allowed: acc[k] = acc.get(k, 0) + 0.5 * v / len(ns)
            new.append(acc)
        W = new
    out = []
    for w in W:
        tot = sum(w.values()); w = {k: v / tot for k, v in w.items()}
        top = sorted(w.items(), key=lambda kv: -kv[1])[:4]; top = [(k, v) for k, v in top if v > 0.01]
        tot = sum(v for _, v in top); out.append({k: v / tot for k, v in top})
    return out

def write_groups(ob, rig, W):
    ob.vertex_groups.clear()
    for b in rig.data.bones:
        if b.use_deform: ob.vertex_groups.new(name=b.name)
    for i, w in enumerate(W):
        for k, v in w.items(): ob.vertex_groups[k].add([i], v, "REPLACE")

def bind(ob, rig):
    m = ob.modifiers.new("Armature", "ARMATURE"); m.object = rig; m.use_deform_preserve_volume = False
    # armature first, so later modifiers (the preview outline) work on the posed shape
    while ob.modifiers[0] != m: bpy.ops.object.modifier_move_up({"object": ob}, modifier=m.name) if False else ob.modifiers.move(ob.modifiers.find(m.name), 0)

def skin_character(name):
    rig = bpy.data.objects[f"{name}_rig"]; body = bpy.data.objects[f"{name}_body"]
    deform = [b.name for b in rig.data.bones if b.use_deform]
    S = segs(rig, deform); R = flesh_radii(body, S)
    # body: every deform bone
    write_groups(body, rig, compute_weights(body, S, R, lambda i: deform)); bind(body, rig)
    # outfit: per part (material slot) bone lists
    of = bpy.data.objects[f"{name}_outfit"]; me = of.data
    vmat = [None] * len(me.vertices)
    for p in me.polygons:
        for vi in p.vertices: vmat[vi] = p.material_index
    part = {0: TORSO + ARMS, 4: TORSO, 1: ["hips", "spine_01"] + LEGS, 2: FEET, 3: FEET}
    write_groups(of, rig, compute_weights(of, S, R, lambda i: part.get(vmat[i], TORSO))); bind(of, rig)
    # torso props follow the shirt
    for prop in ("pin", "bag", "lanyard"):
        ob = bpy.data.objects.get(f"{name}_{prop}")
        if ob:
            allowed = TORSO if prop != "bag" else ["hips", "spine_01", "spine_02", "spine_03", "shoulder.R", "shoulder.L"]
            write_groups(ob, rig, compute_weights(ob, S, R, lambda i: allowed, smooth=2)); bind(ob, rig)
    for bone, parts in RIGID.items():
        for p in parts:
            ob = bpy.data.objects.get(f"{name}_{p}")
            if not ob: continue
            ob.vertex_groups.clear(); g = ob.vertex_groups.new(name=bone); g.add(list(range(len(ob.data.vertices))), 1.0, "REPLACE")
            bind(ob, rig)
    return rig

# ---------------- face rig ----------------
def add_key(ob, name, fn):
    """fn(index, rest_co) -> new co, in object space."""
    if not ob.data.shape_keys: ob.shape_key_add(name="Basis", from_mix=False)
    k = ob.shape_key_add(name=name, from_mix=False)
    for i, v in enumerate(ob.data.vertices): k.data[i].co = fn(i, v.co.copy())
    return k

def face_keys(name):
    rig = bpy.data.objects[f"{name}_rig"]; head = bpy.data.objects[f"{name}_head"]
    eyes, brows, mouth = (bpy.data.objects[f"{name}_{p}"] for p in ("eyes", "brows", "mouth"))
    hb = BVHTree.FromObject(head, bpy.context.evaluated_depsgraph_get(), deform=False)
    def on_face(co, lift=0.0025):
        """Move a point onto the face surface (along Y), just in front of it."""
        hit = hb.ray_cast(Vector((co.x, co.y - 0.3, co.z)), Vector((0, 1, 0)))
        return Vector((co.x, hit[0].y - lift, co.z)) if hit[0] else co
    # eyes: each side's centre and height
    ctr = {}
    for s in (1, -1):
        vs = [v.co for v in eyes.data.vertices if v.co.x * s > 0]
        ctr[s] = (sum(vs, Vector()) / len(vs), max(v.z for v in vs) - min(v.z for v in vs))
    def squash(sides, f, lower=0.35):
        def fn(i, co):
            s = 1 if co.x > 0 else -1
            if s not in sides: return co
            c, h = ctr[s]; zc = c.z - lower * h * 0.5   # lids meet a little below centre, like a real blink
            return Vector((co.x, co.y + 0.003 * (1 - f), zc + (co.z - zc) * f))
        return fn
    add_key(eyes, "blink", squash((1, -1), 0.08)); add_key(eyes, "blink_L", squash((1,), 0.08)); add_key(eyes, "blink_R", squash((-1,), 0.08))
    add_key(eyes, "smile", squash((1, -1), 0.72, lower=-0.6))       # happy squint from below
    add_key(eyes, "sad", squash((1, -1), 0.85, lower=0.9))
    def grow(i, co):
        s = 1 if co.x > 0 else -1; c, h = ctr[s]; d = co - c
        return c + Vector((d.x * 1.12, d.y, d.z * 1.22))
    add_key(eyes, "surprise", grow)
    # brows: two boxes; inner end = smaller |x|
    bx = {s: [v.co.x for v in brows.data.vertices if v.co.x * s > 0] for s in (1, -1)}
    def brow(dz_inner, dz_outer, dz_all=0.0):
        def fn(i, co):
            s = 1 if co.x > 0 else -1; xs = bx[s]; lo, hi = min(map(abs, xs)), max(map(abs, xs))
            t = (abs(co.x) - lo) / (hi - lo)   # 0 inner, 1 outer
            return Vector((co.x, co.y, co.z + dz_all + dz_inner * (1 - t) + dz_outer * t))
        return fn
    add_key(brows, "frown", brow(-0.007, 0.002)); add_key(brows, "sad", brow(0.006, -0.003))
    add_key(brows, "surprise", brow(0.004, 0.004, 0.006)); add_key(brows, "smile", brow(0.0, 0.0, 0.002))
    add_key(brows, "blink", brow(0.0, 0.0, -0.002))
    # mouth: 9 x 3 grid (bottom, middle, top rows); u = -1..1 across
    vs = mouth.data.vertices; xs = [v.co.x for v in vs]; half = max(xs)
    zrows = sorted({round(v.co.z, 5) for v in vs})
    zmid = sum(v.co.z for v in vs) / len(vs)
    row_of = {}
    cols = sorted({round(v.co.x, 5) for v in vs})
    for v in vs:
        same = sorted([w for w in vs if abs(w.co.x - v.co.x) < 1e-5], key=lambda w: w.co.z)
        row_of[v.index] = [w.index for w in same].index(v.index)   # 0 bottom, 1 middle, 2 top
    def mouth_shape(width=1.0, corner=0.0, top=0.0, bottom=0.0, round_=0.0, lip_in=0.0):
        """width: x scale; corner: corners up(+)/down(-) in m; top/bottom: lip opening (m) at the centre;
        round_: pulls the corners in towards an O; lip_in: lifts the lower lip (F/V)."""
        def fn(i, co):
            u = co.x / half; r = row_of[i]; bell = 1 - u * u
            x = co.x * width * (1 - round_ * 0.45)
            z = co.z + corner * u * u
            if r == 2: z += top * (bell ** (0.6 + round_))
            if r == 0: z -= bottom * (bell ** (0.6 + round_)) - lip_in * bell
            if r == 1: z += (top - bottom) * 0.5 * bell * 0.2
            return on_face(Vector((x, co.y, z)))
        return fn
    k = mouth_shape
    add_key(mouth, "smile", k(width=1.14, corner=0.009)); add_key(mouth, "frown", k(width=0.96, corner=-0.008))
    add_key(mouth, "sad", k(width=0.9, corner=-0.006, bottom=0.002))
    add_key(mouth, "open", k(top=0.004, bottom=0.020)); add_key(mouth, "surprise", k(width=0.72, top=0.006, bottom=0.017, round_=0.6))
    add_key(mouth, "vis_A", k(width=1.02, top=0.004, bottom=0.016)); add_key(mouth, "vis_E", k(width=1.16, corner=0.002, top=0.002, bottom=0.007))
    add_key(mouth, "vis_O", k(width=0.70, top=0.005, bottom=0.012, round_=0.7)); add_key(mouth, "vis_U", k(width=0.56, top=0.002, bottom=0.005, round_=0.8))
    add_key(mouth, "vis_MBP", k(width=0.94, top=-0.0015, bottom=-0.0015)); add_key(mouth, "vis_FV", k(width=1.0, top=0.002, bottom=0.002, lip_in=0.004))
    # rig props drive every shape key of the same name
    for p in FACE_PROPS:
        rig[p] = 0.0
        ui = rig.id_properties_ui(p); ui.update(min=0.0, max=1.0, soft_min=0.0, soft_max=1.0)
    for ob in (eyes, brows, mouth):
        for kb in ob.data.shape_keys.key_blocks[1:]:
            d = kb.driver_add("value").driver; d.type = "AVERAGE"
            v = d.variables.new(); v.name = "p"; v.type = "SINGLE_PROP"; v.targets[0].id = rig; v.targets[0].data_path = f'["{kb.name}"]'
    return [kb.name for ob in (eyes, brows, mouth) for kb in ob.data.shape_keys.key_blocks[1:]]

def main():
    bpy.ops.wm.open_mainfile(filepath=str(WORK / "stage2.blend"))
    for name in ("tobi", "amara"):
        skin_character(name); keys = face_keys(name)
        print(name, "weighted; shape keys:", sorted(set(keys)))
    save(WORK / "stage3.blend")

if __name__ == "__main__":
    main()
