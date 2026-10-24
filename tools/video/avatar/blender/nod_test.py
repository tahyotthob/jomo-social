"""Feasibility test: Tobi as a deforming mesh in Blender. Head nods and the pointing arm lifts,
using bones with smooth weights, so nothing ghosts or tears. Renders 3 stills (Cycles, CPU)."""
import bpy, math, sys, pathlib
OUT = pathlib.Path(sys.argv[-1]); OUT.mkdir(parents=True, exist_ok=True)
IMG = str(pathlib.Path(__file__).resolve().parents[4] / "assets/avatars/puppet/tobi-body.png")
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
W, H = 1080, 1440  # image frame; 1 Blender unit = 100 px
# subdivided plane with the image as an unlit, alpha-blended texture
bpy.ops.mesh.primitive_grid_add(x_subdivisions=90, y_subdivisions=120, size=1)
pl = bpy.context.object; pl.scale = (W / 100, H / 100, 1)
bpy.ops.object.transform_apply(scale=True)
mat = bpy.data.materials.new("tobi"); mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()
tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(IMG)
em = nt.nodes.new("ShaderNodeEmission"); tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mix = nt.nodes.new("ShaderNodeMixShader"); out = nt.nodes.new("ShaderNodeOutputMaterial")
nt.links.new(tex.outputs["Color"], em.inputs["Color"]); nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs["Surface"])
pl.data.materials.append(mat)
# pixel -> blender coords
P = lambda x, y: ((x - W / 2) / 100, (H / 2 - y) / 100, 0)
# armature: body root, neck->head, shoulder->hand (Tobi's pointing arm, image coords measured from the cut-out)
bpy.ops.object.armature_add(); arm = bpy.context.object; bpy.ops.object.mode_set(mode="EDIT")
eb = arm.data.edit_bones; root = eb[0]; root.name = "root"; root.head = P(560, 1400); root.tail = P(560, 700)
def bone(n, a, b, parent):
    x = eb.new(n); x.head = P(*a); x.tail = P(*b); x.parent = parent; return x
head = bone("head", (500, 250), (510, 60), root)
uarm = bone("arm", (700, 300), (840, 210), root)
bpy.ops.object.mode_set(mode="OBJECT")
# weights by distance: head region above the neck line, arm region beyond the shoulder
vg = {n: pl.vertex_groups.new(name=n) for n in ("root", "head", "arm")}
for v in pl.data.vertices:
    x = v.co.x * 100 + W / 2; y = H / 2 - v.co.y * 100
    h = min(1, max(0, (275 - y) / 50))                       # head: above y=275, soft 50 px band
    a = min(1, max(0, (x - 690) / 60)) * (1 if y < 420 else 0)  # arm: right of x=690, upper body only
    r = max(0, 1 - h - a)
    vg["head"].add([v.index], h, "REPLACE"); vg["arm"].add([v.index], a, "REPLACE"); vg["root"].add([v.index], r, "REPLACE")
pl.parent = arm; m = pl.modifiers.new("arm", "ARMATURE"); m.object = arm
# camera and render settings
bpy.ops.object.camera_add(location=(0, 0, 20)); cam = bpy.context.object; cam.data.type = "ORTHO"; cam.data.ortho_scale = H / 100; sc.camera = cam
sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.film_transparent = True
sc.render.engine = "CYCLES"; sc.cycles.samples = 8; sc.cycles.device = "CPU"
sc.view_settings.view_transform = "Standard"  # keep the flat colours exactly as drawn
pb = arm.pose.bones
for i, (hr, ar) in enumerate([(0, 0), (8, 0), (-6, -14)]):
    pb["head"].rotation_mode = pb["arm"].rotation_mode = "XYZ"
    pb["head"].rotation_euler = (0, 0, math.radians(hr)); pb["arm"].rotation_euler = (0, 0, math.radians(ar))
    sc.render.filepath = str(OUT / f"pose{i}.png"); bpy.ops.render.render(write_still=True)
print("done")
