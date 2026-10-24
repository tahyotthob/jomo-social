"""Stage 6: export.

  blender/export/jomo_characters.blend   both characters, rigs, face rig, all Actions (palette packed)
  blender/export/tobi.glb, amara.glb     one per character: meshes, skin, shape keys, all Actions
  blender/export/tobi.fbx, amara.fbx     one per character: meshes, skin, shape keys, all Actions (bones)
Face animation: in Blender the rig's face properties drive the shape keys. Drivers don't export, so
for each Action the face-property curves are copied onto each face mesh's shape keys as an Action
of the same name (NLA track name), and the exporters merge them by that name.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *
from s3_skin import FACE_PROPS

FACE_MESHES = ("eyes", "brows", "mouth")

def final_blend():
    bpy.ops.wm.open_mainfile(filepath=str(WORK / "stage5.blend"))
    img = bpy.data.images.get("jomo_palette"); img.filepath = str(BL / "textures" / "jomo_palette.png"); img.reload(); img.pack()
    for n in ("tobi", "amara"):
        r = bpy.data.objects[f"{n}_rig"]; idle = bpy.data.actions["idle"]
        r.animation_data.action = idle; r.animation_data.action_slot = idle.slots[0]
        r.data.bones["root"].use_deform = True   # keeps the locomotion root in "deform bones only" exports
    bpy.context.scene.frame_start, bpy.context.scene.frame_end = 0, 95; bpy.context.scene.render.fps = 24
    save(EXPORT / "jomo_characters.blend")

def prop_curves(act):
    out = {}
    for layer in act.layers:
        for strip in layer.strips:
            for cb in strip.channelbags:
                for fc in cb.fcurves:
                    if fc.data_path.startswith('["'): out[fc.data_path[2:-2]] = fc
    return out

def to_nla(name):
    """NLA track per Action on the rig and on each face mesh's shape keys (same track names)."""
    rig = bpy.data.objects[f"{name}_rig"]; ad = rig.animation_data; ad.action = None
    meshes = {p: bpy.data.objects[f"{name}_{p}"] for p in FACE_MESHES}
    for ob in meshes.values():   # drivers would fight the baked curves
        k = ob.data.shape_keys
        if k.animation_data:
            for d in list(k.animation_data.drivers): k.animation_data.drivers.remove(d)
    acts = [a for a in bpy.data.actions if "frames" in a.keys()]
    for act in acts:
        tr = ad.nla_tracks.new(); tr.name = act.name
        st = tr.strips.new(act.name, 0, act); st.action_slot = act.slots[0]; tr.mute = False
        curves = prop_curves(act)
        for p, ob in meshes.items():
            key = ob.data.shape_keys; key.animation_data_create()
            ka = bpy.data.actions.new(f"{act.name}__{name}_{p}"); key.animation_data.action = ka
            for kb in key.key_blocks[1:]:
                fc = curves.get(kb.name)
                pts = [(kp.co[0], kp.co[1]) for kp in fc.keyframe_points] if fc else [(0, 0.0)]
                for f, v in pts:
                    kb.value = v; kb.keyframe_insert("value", frame=f)
            key.animation_data.action = None
            kt = key.animation_data.nla_tracks.new(); kt.name = act.name
            ks = kt.strips.new(act.name, 0, ka); ks.action_slot = ka.slots[0]
            for kb in key.key_blocks[1:]: kb.value = 0.0
    return rig

def export_prep():
    """Export copies only: the Principled output is the one exporters read; drop the EEVEE toon output."""
    for m in bpy.data.materials:
        if not m.node_tree: continue
        for n in list(m.node_tree.nodes):
            if n.type == "OUTPUT_MATERIAL":
                if n.target == "EEVEE": m.node_tree.nodes.remove(n)
                else: n.target = "ALL"; n.is_active_output = True

def select_char(name):
    bpy.ops.object.select_all(action="DESELECT")
    rig = bpy.data.objects[f"{name}_rig"]; rig.select_set(True); bpy.context.view_layer.objects.active = rig
    for o in rig.children: o.select_set(True)

def main():
    final_blend()
    for name in ("tobi", "amara"):
        bpy.ops.wm.open_mainfile(filepath=str(EXPORT / "jomo_characters.blend"))
        export_prep(); to_nla(name); select_char(name)
        bpy.data.objects[f"{name}_rig"].location = (0, 0, 0)   # each file has its character at the origin
        bpy.ops.export_scene.gltf(filepath=str(EXPORT / f"{name}.glb"), export_format="GLB", use_selection=True,
                                  export_animation_mode="NLA_TRACKS", export_def_bones=True, export_morph=True,
                                  export_morph_animation=True, export_skins=True, export_yup=True, export_apply=False,
                                  export_force_sampling=True, export_frame_range=False, export_anim_slide_to_zero=True)
        bpy.ops.export_scene.fbx(filepath=str(EXPORT / f"{name}.fbx"), use_selection=True, add_leaf_bones=False,
                                 use_armature_deform_only=True, bake_anim=True, bake_anim_use_all_actions=False,
                                 bake_anim_use_nla_strips=True, bake_anim_force_startend_keying=True,
                                 bake_anim_simplify_factor=0.0, path_mode="COPY", embed_textures=True,
                                 mesh_smooth_type="FACE", apply_scale_options="FBX_SCALE_UNITS")
        print("exported", name)

if __name__ == "__main__":
    main()
