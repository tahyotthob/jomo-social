"""Preview renders used after every stage: a turntable sheet and a pose sheet (PNG).

Rendering is Cycles on the CPU with a flat toon look built at render time (the saved .blend files
keep plain Principled materials for export): colour x a two-step light ramp, plus an inverted-hull
outline. Usage:
    python3 blender/scripts/preview.py blender/work/stageN.blend stageN [turntable|poses|all]
"""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *
from PIL import Image, ImageDraw

LIGHT = Vector((-0.45, -0.75, 0.55)).normalized()

def toonify():
    """Add a Cycles-only toon output to every material and an outline shell to every mesh."""
    out_mat = bpy.data.materials.get("OUTLINE") or bpy.data.materials.new("OUTLINE")
    out_mat.use_nodes = True; nt = out_mat.node_tree; nt.nodes.clear()
    geo = nt.nodes.new("ShaderNodeNewGeometry"); em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = hexcol("#141614")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(geo.outputs["Backfacing"], mx.inputs["Fac"]); nt.links.new(em.outputs[0], mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], o.inputs["Surface"])
    for m in bpy.data.materials:
        if m.name == "OUTLINE" or not m.use_nodes: continue
        nt = m.node_tree; bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if not bsdf: continue
        src = bsdf.inputs["Base Color"]
        col = src.links[0].from_socket if src.links else None
        geo = nt.nodes.new("ShaderNodeNewGeometry"); dot = nt.nodes.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
        dot.inputs[1].default_value = LIGHT; nt.links.new(geo.outputs["Normal"], dot.inputs[0])
        ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.interpolation = "CONSTANT"
        ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (0.62, 0.62, 0.66, 1)
        ramp.color_ramp.elements[1].position = 0.12; ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
        nt.links.new(dot.outputs["Value"], ramp.inputs["Fac"])
        mul = nt.nodes.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"
        ins = [s for s in mul.inputs if s.enabled]; ins[0].default_value = 1.0
        if col: nt.links.new(col, ins[1])
        else: ins[1].default_value = src.default_value
        nt.links.new(ramp.outputs["Color"], ins[2])
        em = nt.nodes.new("ShaderNodeEmission"); nt.links.new([s for s in mul.outputs if s.enabled][0], em.inputs["Color"])
        o = nt.nodes.new("ShaderNodeOutputMaterial"); o.target = "CYCLES"; nt.links.new(em.outputs[0], o.inputs["Surface"])
        for n in nt.nodes:
            if n.type == "OUTPUT_MATERIAL": n.is_active_output = (n == o)
    for ob in bpy.data.objects:
        if ob.type != "MESH" or ob.name.startswith("WIDGET"): continue
        ob.data.materials.append(out_mat)
        s = ob.modifiers.new("outline", "SOLIDIFY"); s.thickness = 0.0045 if "body" in ob.name or "outfit" in ob.name or "head" in ob.name or "hair" in ob.name else 0.0022
        s.offset = 1.0; s.use_flip_normals = True; s.use_rim = False; s.material_offset = len(ob.data.materials) - 1
        if any(k in ob.name for k in ("_mouth", "_brows", "_eyes")): ob.modifiers.remove(s)

def setup(sc, res=(1400, 1100), samples=4):
    sc.render.engine = "CYCLES"; sc.cycles.samples = samples; sc.cycles.use_denoising = False; sc.cycles.device = "CPU"
    sc.cycles.max_bounces = 0; sc.cycles.transparent_max_bounces = 8
    sc.render.resolution_x, sc.render.resolution_y = res; sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("bg"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = hexcol("#F4F6EC"); w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
    sc.render.film_transparent = False
    cam_data = bpy.data.cameras.new("cam"); cam_data.type = "ORTHO"; cam = bpy.data.objects.new("cam", cam_data)
    sc.collection.objects.link(cam); sc.camera = cam
    return cam

def aim(cam, target, dist=8.0, yaw=0.0, pitch=4.0, scale=2.3):
    t = Vector(target); d = Vector((math.sin(math.radians(yaw)) * math.cos(math.radians(pitch)), -math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)), math.sin(math.radians(pitch))))
    cam.location = t + d * dist; cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler(); cam.data.ortho_scale = scale

def tops():
    """The object that moves each character (armature in stage 2+, empty in stage 1)."""
    out = {}
    for n in ("tobi", "amara"):
        out[n] = bpy.data.objects.get(f"{n}_rig") or bpy.data.objects.get(f"{n}_grp")
    return out

def render_to(sc, path):
    sc.render.filepath = str(path); bpy.ops.render.render(write_still=True); return Image.open(path).convert("RGB")

def label(img, text):
    d = ImageDraw.Draw(img); d.rectangle((0, 0, img.width, 34), fill=(30, 34, 32)); d.text((10, 10), text, fill=(244, 246, 236)); return img

def sheet(imgs, cols, path, title):
    w, h = imgs[0].size; rows = (len(imgs) + cols - 1) // cols
    S = Image.new("RGB", (w * cols, h * rows + 44), (244, 246, 236)); d = ImageDraw.Draw(S)
    d.rectangle((0, 0, S.width, 44), fill=(165, 205, 57)); d.text((12, 14), title, fill=(30, 34, 32))
    for i, im in enumerate(imgs): S.paste(im, ((i % cols) * w, 44 + (i // cols) * h))
    S.save(path); return path

def turntable(stage, outdir):
    sc = bpy.context.scene; cam = setup(sc, (900, 1000)); T = tops(); imgs = []
    tmp = outdir / "_tt"; tmp.mkdir(exist_ok=True)
    base = {n: o.rotation_euler.z for n, o in T.items()}
    for i, ang in enumerate(range(0, 360, 45)):
        for n, o in T.items(): o.rotation_euler.z = base[n] + math.radians(ang)
        aim(cam, (0, 0, 0.92), scale=2.25)
        imgs.append(label(render_to(sc, tmp / f"{i}.png"), f"{ang} deg"))
    for n, o in T.items(): o.rotation_euler.z = base[n]
    return sheet(imgs, 4, outdir / f"{stage}_turntable.png", f"{stage}: turntable (Tobi left, Amara right), 45-degree steps")

def face_closeups(stage, outdir, extra=()):
    """Head close-ups: neutral plus any (label, setter) pairs passed in."""
    sc = bpy.context.scene; cam = sc.camera or setup(sc); imgs = []; tmp = outdir / "_ps"; tmp.mkdir(exist_ok=True)
    sc.render.resolution_x, sc.render.resolution_y = 520, 520
    for n in ("tobi", "amara"):
        head = bpy.data.objects[f"{n}_head"]; dg = bpy.context.evaluated_depsgraph_get()
        ev = head.evaluated_get(dg); ws = [head.matrix_world @ v.co for v in ev.data.vertices]
        c = sum(ws, Vector()) / len(ws)
        for lab, fn in [("neutral", None)] + list(extra):
            if fn: fn(n, True)
            aim(cam, c + Vector((0, 0, -0.01)), dist=3, yaw=12 if n == "tobi" else -12, pitch=3, scale=0.42)
            imgs.append(label(render_to(sc, tmp / f"face_{n}_{lab}.png"), f"{n} {lab}"))
            if fn: fn(n, False)
    return imgs

if __name__ == "__main__":
    blend, stage = sys.argv[1], sys.argv[2]; what = sys.argv[3] if len(sys.argv) > 3 else "all"
    bpy.ops.wm.open_mainfile(filepath=blend); toonify()
    outdir = RENDERS / stage; outdir.mkdir(parents=True, exist_ok=True)
    if what in ("turntable", "all"): print("wrote", turntable(stage, outdir))
    if what in ("poses", "all"):
        sc = bpy.context.scene
        if not sc.camera: setup(sc)
        imgs = []
        cam = sc.camera; sc.render.resolution_x, sc.render.resolution_y = 520, 1000
        tmp = outdir / "_ps"; tmp.mkdir(exist_ok=True)
        for n in ("tobi", "amara"):
            T = tops()[n]; x = T.location.x
            for yaw, lab in ((0, "front"), (90, "side"), (180, "back")):
                aim(cam, (x, 0, 0.9), yaw=yaw, scale=2.0)
                imgs.append(label(render_to(sc, tmp / f"{n}_{lab}.png"), f"{n} {lab}"))
        faces = face_closeups(stage, outdir)
        faces = [f.resize((520, 520)) for f in faces]
        S1 = sheet(imgs, 6, outdir / f"{stage}_poses_body.png", f"{stage}: front, side and back")
        S2 = sheet(faces, 2, outdir / f"{stage}_poses_face.png", f"{stage}: faces")
        print("wrote", S1, S2)
