"""Stage 6 check: re-import the exported .glb files into an empty scene and render a turntable and an
animation pose sheet from them, so the check shows exactly what ships.

    python3 blender/scripts/verify_export.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *
import preview
from PIL import Image

POSES = [("idle", 40), ("walk", 8), ("run", 5), ("jump", 20), ("wave", 22), ("talk", 30), ("celebrate", 15),
         ("sit_down", 48), ("point", 16), ("clap", 4), ("dance", 6), ("react_surprise", 20), ("react_sad", 30),
         ("react_laugh", 24), ("tobi_selfie_hype", 48), ("amara_fact_check", 30)]

def main():
    bpy.ops.wm.read_factory_settings(use_empty=True); report = []
    for name in ("tobi", "amara"):
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=str(EXPORT / f"{name}.glb"))
        new = [o for o in bpy.data.objects if o not in before]
        arm = next(o for o in new if o.type == "ARMATURE"); arm.name = f"{name}_rig"
        arm.location.x = CHARS[name]["offset_x"]
        meshes = [o for o in new if o.type == "MESH" and o.parent == arm]   # skip the importer's bone-shape icosphere
        report.append(f"{name}: {len(arm.data.bones)} bones, {len(meshes)} meshes, "
                      f"{sum(len(p.vertices) - 2 for o in meshes for p in o.data.polygons)} tris, "
                      f"shape keys on {sum(1 for o in meshes if o.data.shape_keys)} meshes")
    report.append(f"actions imported: {len(bpy.data.actions)}")
    preview.toonify()
    out = RENDERS / "stage6"; out.mkdir(parents=True, exist_ok=True)
    print("wrote", preview.turntable("stage6", out))
    sc = bpy.context.scene; cam = sc.camera; sc.render.resolution_x, sc.render.resolution_y = 560, 520
    tmp = out / "_ps"; tmp.mkdir(exist_ok=True); imgs = []
    for act_name, f in POSES:
        for n in ("tobi", "amara"):
            arm = bpy.data.objects[f"{n}_rig"]; ad = arm.animation_data or arm.animation_data_create()
            for t in ad.nla_tracks: t.mute = True
            # the importer stores each animation as one Action with a slot for the armature and one per face mesh
            act = bpy.data.actions[act_name]; ad.action = act
            ad.action_slot = next(sl for sl in act.slots if sl.identifier.startswith("OB"))
            for o in arm.children:
                k = o.data.shape_keys if o.type == "MESH" else None
                if not k: continue
                kad = k.animation_data or k.animation_data_create()
                for t in kad.nla_tracks: t.mute = True
                sl = next((sl for sl in act.slots if sl.identifier.startswith("KE") and o.name.split(".")[0] in sl.identifier), None)
                if sl: kad.action = act; kad.action_slot = sl
        sc.frame_set(f); preview.aim(cam, (0, 0, 0.95), yaw=22, pitch=6, scale=2.5)
        imgs.append(preview.label(preview.render_to(sc, tmp / f"{act_name}.png"), f"{act_name} f{f} (from .glb)"))
    print("wrote", preview.sheet(imgs, 4, out / "stage6_poses_from_glb.png", "stage6: animations played from the exported .glb files"))
    (out / "stage6_report.txt").write_text("\n".join(report) + "\n"); print("\n".join(report))

if __name__ == "__main__":
    main()
