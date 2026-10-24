"""Shared settings for the JOMO 3D character set: paths, palette, character specs, scene helpers.

Every stage script imports this. Run stages with Blender's Python module (pip install bpy), e.g.
    python3 blender/scripts/s1_mesh.py
Units are metres. Characters face -Y, so their left side is +X (".L" names).
"""
import bpy, bmesh, math, pathlib, sys
from mathutils import Vector, Matrix

ROOT = pathlib.Path(__file__).resolve().parents[2]
BL = ROOT / "blender"
WORK, RENDERS, EXPORT = BL / "work", BL / "renders", BL / "export"
for d in (WORK, RENDERS, EXPORT):
    d.mkdir(parents=True, exist_ok=True)

def hexcol(h, a=1.0):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    # sRGB -> linear for Blender colour sockets
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c) + (a,)

# Brand palette (references/brand-guide.md) plus skin, hair and neutral swatches.
PALETTE = {
    "lime": "#A5CD39", "leaf": "#8FB73C", "olive": "#77962A", "charcoal": "#323534", "ink": "#1E2220", "offwhite": "#F4F6EC",
    "skin_tobi": "#5A3820", "skin_amara": "#8B5A3C", "hair": "#16130F", "white": "#F7F7F2", "eye_white": "#FBFAF5",
    "iris": "#2A1A10", "mouth": "#3A1414", "brow": "#120E0B", "trouser_tobi": "#262A26", "sole": "#D8D8D0",
    "gold": "#C9A227", "screen": "#E9F2D2", "metal": "#2B2B2B", "lip_amara": "#6E3B2B",
}

CHARS = {
    "tobi": {
        "height": 1.80, "shoulder": 0.118, "hip": 0.056, "torso": 1.0, "arm": 1.0, "leg": 1.0,
        "skin": "skin_tobi", "signature": "lime", "offset_x": -0.55,
        "head": {"w": 0.185, "d": 0.215, "h": 0.245, "jaw": 0.30},
        "role": "Adventurous, influential friend who makes things happen (24, male)",
    },
    "amara": {
        "height": 1.66, "shoulder": 0.104, "hip": 0.062, "torso": 0.90, "arm": 0.88, "leg": 0.97,
        "skin": "skin_amara", "signature": "offwhite", "offset_x": 0.55,
        "head": {"w": 0.175, "d": 0.205, "h": 0.235, "jaw": 0.36},
        "role": "Nerdy fact-checker who follows the rules (23, female)",
    },
}

def joints(name):
    """Joint positions (metres) for the A-pose rest shape. Left side only; mirror x for right."""
    c = CHARS[name]; H = c["height"]
    z = lambda f: f * H
    sh = c["shoulder"] * H; hp = c["hip"] * H
    J = {
        "root": (0, 0, 0),
        "pelvis": (0, 0.005, z(0.530)), "spine1": (0, 0.0, z(0.575)), "spine2": (0, -0.005, z(0.640)),
        "spine3": (0, -0.005, z(0.705)), "neck": (0, 0.0, z(0.775)), "head": (0, -0.005, z(0.832)),
        "clav": (0.022 * H, -0.01, z(0.770)), "shoulder": (sh, 0.005, z(0.785)),
        "hipj": (hp, 0.0, z(0.505)), "knee": (hp * 0.96, -0.012, z(0.275)), "ankle": (hp * 0.92, 0.012, z(0.048)),
        "ball": (hp * 0.95, -0.052 * H, z(0.018)), "toe": (hp * 0.96, -0.080 * H, z(0.016)),
    }
    # arms in a 45-degree A-pose, in the XZ plane
    a = math.radians(45); d = Vector((math.cos(a), 0, -math.sin(a)))
    s = Vector(J["shoulder"]); L1, L2 = 0.165 * H * c["arm"], 0.145 * H * c["arm"]
    e = s + d * L1; w = e + d * L2
    J["elbow"], J["wrist"] = tuple(e), tuple(w)
    J["palm"] = tuple(w + d * 0.050 * H * c["arm"])
    # fingers: spread along Y (thumb forward, -Y); 3 segments each, continuing the arm direction
    fdir = d; side = Vector((0, 1, 0)); palm = Vector(J["palm"])
    lens = {"thumb": (0.022, 0.020, 0.018), "index": (0.026, 0.017, 0.015), "middle": (0.028, 0.019, 0.016),
            "ring": (0.026, 0.017, 0.015), "pinky": (0.021, 0.014, 0.012)}
    offs = {"index": -0.0155, "middle": -0.0045, "ring": 0.0065, "pinky": 0.0165}
    for f, ls in lens.items():
        k = H * c["arm"] / 1.8
        if f == "thumb":
            base = Vector(J["wrist"]) + d * 0.018 * H + side * (-0.020 * H / 1.8) + Vector((0, 0, 0))
            dirn = (d * 0.55 + side * -0.55 + Vector((0, 0, -0.25))).normalized()
        else:
            base = palm + side * offs[f] * k * 1.0
            dirn = (fdir + side * offs[f] * 6).normalized()
        p = base; J[f"{f}_0"] = tuple(p)
        for i, l in enumerate(ls, 1):
            p = p + dirn * l * k * (1 if f != "thumb" else 1.0); J[f"{f}_{i}"] = tuple(p)
    return J

def mirror(p):
    return (-p[0], p[1], p[2])

# ---------------- scene helpers ----------------
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.unit_settings.system = "METRIC"; sc.unit_settings.scale_length = 1.0
    return sc

def link(obj, coll):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    coll.objects.link(obj)

def new_obj(name, mesh, coll):
    o = bpy.data.objects.new(name, mesh); coll.objects.link(o); return o

def from_bmesh(name, bm, coll, mats=None):
    """Material slots must exist before to_mesh, or Blender clamps every face to slot 0."""
    me = bpy.data.meshes.new(name)
    for k in (mats or []): me.materials.append(flat_material(f"M_{k}", k))
    bm.to_mesh(me); bm.free(); return new_obj(name, me, coll)

def tri_count(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)

def flat_material(name, color_key):
    """Stage 1-3 preview material: palette colour, named after the swatch so stage 4 can map it to the atlas."""
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    m["swatch"] = color_key
    bsdf = m.node_tree.nodes.get("Principled BSDF"); bsdf.inputs["Base Color"].default_value = hexcol(PALETTE[color_key])
    bsdf.inputs["Roughness"].default_value = 0.8
    return m

def set_mats(obj, keys):
    obj.data.materials.clear()
    for k in keys:
        obj.data.materials.append(flat_material(f"M_{k}", k))

def save(path):
    bpy.ops.wm.save_as_mainfile(filepath=str(path), compress=True)
