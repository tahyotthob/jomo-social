"""Stage 4: UVs, palette texture atlas and toon materials.

Palette atlas: blender/textures/jomo_palette.png, 256 x 256, an 8 x 8 grid of flat swatches (one per
PALETTE colour, see common.py). Every mesh gets one UV map ("UVMap"): its faces are unwrapped with
Smart UV Project one material at a time, and each material's islands are packed into that colour's
cell. So UVs never overlap, the palette colours come out exactly, and the same UVs can be used later
for a painted texture.
Materials: one shared material per character, M_<name>_toon, with two outputs:
  - EEVEE: toon shading (Diffuse -> Shader to RGB -> 2-step ramp) x palette colour
  - Cycles / export: Principled BSDF with the palette as base colour (roughness 1, no metal), which
    is what glTF and FBX carry.
Output: blender/work/stage4.blend
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *
from PIL import Image
from uv_check import count_overlaps

TEX = BL / "textures"; TEX.mkdir(exist_ok=True)
GRID, SIZE = 8, 256
CELL = SIZE // GRID
INSET = 3 / SIZE   # keep UVs 3 px inside each cell so mipmaps don't bleed

def swatch_cells():
    return {k: (i % GRID, i // GRID) for i, k in enumerate(PALETTE)}

def make_palette():
    im = Image.new("RGB", (SIZE, SIZE), (255, 0, 255))   # magenta = unused cell, easy to spot
    for k, (cx, cy) in swatch_cells().items():
        h = PALETTE[k].lstrip("#"); col = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        im.paste(col, (cx * CELL, (GRID - 1 - cy) * CELL, (cx + 1) * CELL, (GRID - cy) * CELL))   # UV v=0 is the bottom row
    path = TEX / "jomo_palette.png"; im.save(path); return path

def cell_rect(key):
    cx, cy = swatch_cells()[key]
    return (cx / GRID + INSET, cy / GRID + INSET, (cx + 1) / GRID - INSET, (cy + 1) / GRID - INSET)

def unwrap(ob, method="MINIMUM_STRETCH", cut=()):
    """Smart-project each material's faces on its own, then fit those UVs into its swatch cell."""
    me = ob.data
    if not me.uv_layers: me.uv_layers.new(name="UVMap")
    bpy.ops.object.select_all(action="DESELECT"); ob.select_set(True); bpy.context.view_layer.objects.active = ob
    keys = [m.get("swatch") for m in me.materials]; final = {}
    for key in dict.fromkeys(keys):   # slots that share a colour share a cell, so unwrap them together
        mis = {i for i, k in enumerate(keys) if k == key}
        faces = [p.index for p in me.polygons if p.material_index in mis]
        if not faces: continue
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_mode(type="FACE")
        bm = bmesh.from_edit_mesh(me)   # select exactly this colour's faces (verts and edges too)
        for e in bm.verts[:] + bm.edges[:] + bm.faces[:]: e.select_set(False)
        for f in bm.faces:
            if f.material_index in mis: f.select_set(True)
        bm.select_flush_mode(); bmesh.update_edit_mesh(me)
        bpy.ops.uv.smart_project(angle_limit=math.radians(35), island_margin=0.02, scale_to_bounds=False)
        # Smart UV Project can fold a few faces inside an island; re-solve each island as a proper unwrap
        bpy.ops.uv.select_all(action="SELECT"); bpy.ops.uv.seams_from_islands(mark_seams=True)
        if cut:   # faces that folded last time become their own islands
            bm = bmesh.from_edit_mesh(me); bm.faces.ensure_lookup_table()
            for fi in cut:
                for e in bm.faces[fi].edges: e.seam = True
            bmesh.update_edit_mesh(me)
        bpy.ops.uv.unwrap(method=method, margin=0.02)
        bpy.ops.object.mode_set(mode="OBJECT")
        uv = me.uv_layers["UVMap"].data; loops = [li for f in faces for li in me.polygons[f].loop_indices]
        us = [uv[li].uv.x for li in loops]; vs = [uv[li].uv.y for li in loops]
        u0, v0 = min(us), min(vs); s = max(max(us) - u0, max(vs) - v0, 1e-9)
        x0, y0, x1, y1 = cell_rect(key)
        for li in loops:   # stored, because unwrapping the next colour can disturb these UVs
            final[li] = (x0 + (uv[li].uv.x - u0) / s * (x1 - x0), y0 + (uv[li].uv.y - v0) / s * (y1 - y0))
    uv = me.uv_layers["UVMap"].data
    for li, co in final.items(): uv[li].uv = co

def clean(ob):
    """Remove duplicate and zero-area faces (left by bmesh solidify on the bandana and glasses)."""
    bm = bmesh.new(); bm.from_mesh(ob.data); n0 = len(bm.faces)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    seen = set(); dup = []
    for f in bm.faces:
        k = frozenset(v.index for v in f.verts)
        if k in seen or f.calc_area() < 1e-9: dup.append(f)
        seen.add(k)
    bmesh.ops.delete(bm, geom=dup, context="FACES_ONLY")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bm.to_mesh(ob.data); n1 = len(bm.faces); bm.free(); return n0 - n1

def toon_material(name, img):
    m = bpy.data.materials.new(f"M_{name}_toon"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; L = nt.links.new
    tex = N("ShaderNodeTexImage"); tex.image = img; tex.interpolation = "Closest"; tex.location = (-700, 0)
    uvn = N("ShaderNodeUVMap"); uvn.uv_map = "UVMap"; uvn.location = (-900, 0); L(uvn.outputs[0], tex.inputs[0])
    bsdf = N("ShaderNodeBsdfPrincipled"); bsdf.location = (-300, -300)
    bsdf.inputs["Roughness"].default_value = 1.0; bsdf.inputs["Metallic"].default_value = 0.0
    L(tex.outputs["Color"], bsdf.inputs["Base Color"])
    out_c = N("ShaderNodeOutputMaterial"); out_c.target = "CYCLES"; out_c.location = (300, -300); L(bsdf.outputs[0], out_c.inputs[0])
    # EEVEE toon: light -> 2-step ramp -> x palette colour
    dif = N("ShaderNodeBsdfDiffuse"); dif.location = (-500, 300); s2r = N("ShaderNodeShaderToRGB"); s2r.location = (-300, 300)
    L(dif.outputs[0], s2r.inputs[0])
    ramp = N("ShaderNodeValToRGB"); ramp.location = (-100, 300); ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].color = (0.62, 0.62, 0.66, 1); ramp.color_ramp.elements[1].position = 0.12
    L(s2r.outputs["Color"], ramp.inputs["Fac"])
    mul = N("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.location = (150, 200)
    ins = [s for s in mul.inputs if s.enabled]; ins[0].default_value = 1.0
    L(tex.outputs["Color"], ins[1]); L(ramp.outputs["Color"], ins[2])
    em = N("ShaderNodeEmission"); em.location = (350, 200); L([s for s in mul.outputs if s.enabled][0], em.inputs["Color"])
    out_e = N("ShaderNodeOutputMaterial"); out_e.target = "EEVEE"; out_e.location = (550, 200); L(em.outputs[0], out_e.inputs[0])
    out_c.is_active_output = True
    return m

def main():
    bpy.ops.wm.open_mainfile(filepath=str(WORK / "stage3.blend"))
    # stage 4 adds a dark inner mouth for Amara: lip colour at the corners, dark in the middle
    am = bpy.data.objects["amara_mouth"]; me = am.data
    me.materials.append(flat_material("M_mouth", "mouth")); half = max(v.co.x for v in me.vertices)
    for p in me.polygons:
        if abs(p.center.x) < 0.70 * half: p.material_index = 1
    img = bpy.data.images.load(str(make_palette())); img.name = "jomo_palette"
    for name in ("tobi", "amara"):
        rig = bpy.data.objects[f"{name}_rig"]; mat = toon_material(name, img)
        for ob in [o for o in rig.children if o.type == "MESH"]:
            if ob.name.endswith(("_bandana", "_glasses")): print(ob.name, "removed", clean(ob), "duplicate/degenerate faces")
            cut = set()
            for attempt in range(3):   # unwrap; if any faces fold over each other, cut them free and retry
                unwrap(ob, cut=cut); bad = count_overlaps(ob, faces=True); n = len(bad)
                if n == 0: break
                cut |= bad
            if n: print(ob.name, "still has", n, "overlapping UV faces")
            # one material per mesh: the palette carries the colours now
            ob.data.materials.clear(); ob.data.materials.append(mat)
            for p in ob.data.polygons: p.material_index = 0
    for m in list(bpy.data.materials):
        if m.users == 0: bpy.data.materials.remove(m)
    img.filepath = "//../textures/jomo_palette.png"
    save(WORK / "stage4.blend")
    print("palette cells:", swatch_cells())

if __name__ == "__main__":
    main()
