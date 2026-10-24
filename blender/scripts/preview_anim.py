"""Animation previews: a key-frame contact sheet per action, and an MP4 per action.

    python3 blender/scripts/preview_anim.py blender/work/stage5.blend sheet [action ...]
    python3 blender/scripts/preview_anim.py blender/work/stage5.blend mp4 [action ...]
Both characters play the same Action side by side (Tobi left, Amara right). Sitting actions get a
stool so the pose reads. Output: blender/renders/stage5/ (sheets) and blender/export/previews/ (MP4).
"""
import sys, pathlib, subprocess, shutil
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *
import preview
from preview import toonify, setup, aim, render_to, label, sheet
from PIL import Image
import os
YAW = float(os.environ.get("YAW", 28))

def stage(res=(960, 600)):
    toonify(); sc = bpy.context.scene; cam = setup(sc, res, samples=2)
    sc.render.fps = 24
    floor = bpy.data.meshes.new("floor"); floor.from_pydata([(-40, -40, 0), (40, -40, 0), (40, 40, 0), (-40, 40, 0)], [], [(0, 1, 2, 3)])
    m = bpy.data.materials.new("floor"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = hexcol("#E4E9D3"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o.inputs[0]); floor.materials.append(m)
    fo = bpy.data.objects.new("PREVIEW_floor", floor); sc.collection.objects.link(fo)
    return sc, cam

def stools(on):
    for n in ("tobi", "amara"):
        name = f"PREVIEW_stool_{n}"; ob = bpy.data.objects.get(name)
        if on and not ob:
            rig = bpy.data.objects[f"{n}_rig"]; hz = rig.data.bones["hips"].head_local.z
            top = hz - 0.40 - 0.075; bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
            for v in bm.verts: v.co = Vector((v.co.x * 0.38, v.co.y * 0.36, (v.co.z + 0.5) * top))
            me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
            me.materials.append(bpy.data.materials.get("floor"))
            ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
            ob.location = (rig.location.x, 0.42, 0)
            mat = bpy.data.materials.new("stool"); mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()
            e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = hexcol("#8FB73C"); o = nt.nodes.new("ShaderNodeOutputMaterial")
            nt.links.new(e.outputs[0], o.inputs[0]); me.materials[0] = mat
        if ob: ob.hide_render = not on

def assign(act):
    for n in ("tobi", "amara"):
        r = bpy.data.objects[f"{n}_rig"]; r.animation_data_create()
        r.animation_data.action = act; r.animation_data.action_slot = act.slots[0]

def frame_set(sc, f):
    sc.frame_set(int(f), subframe=f - int(f))

def contact_sheet(sc, cam, name, outdir, n=6):
    act = bpy.data.actions[name]; assign(act); stools(name in ("sit_down", "stand_up"))
    end = int(act.frame_range[1]); frames = [round(end * i / (n - 1)) for i in range(n)]
    sc.render.resolution_x, sc.render.resolution_y = 560, 520
    tmp = outdir / "_anim"; tmp.mkdir(parents=True, exist_ok=True); imgs = []
    for f in frames:
        frame_set(sc, f); aim(cam, (0, 0, 0.95), yaw=YAW, pitch=6, scale=2.5)
        imgs.append(label(render_to(sc, tmp / f"{name}_{f}.png"), f"{name}  f{f}"))
    return imgs

def mp4(sc, cam, name, outdir):
    act = bpy.data.actions[name]; assign(act); stools(name in ("sit_down", "stand_up"))
    end = int(act.frame_range[1]); loop = bool(act.get("loop"))
    sc.render.resolution_x, sc.render.resolution_y = 960, 600
    tmp = outdir / f"_frames_{name}"; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
    aim(cam, (0, 0, 1.0), yaw=24, pitch=5, scale=3.6)
    frames = list(range(0, end + 1))
    reps = 3 if loop else 1
    for f in frames:
        frame_set(sc, f); sc.render.filepath = str(tmp / f"{f:04d}.png"); bpy.ops.render.render(write_still=True)
    # caption + repeat loops 3x (or hold the last frame for half a second on one-shots)
    from PIL import ImageDraw
    seq = []
    for r in range(reps): seq += frames
    if not loop: seq += [frames[-1]] * 12
    cap = tmp / "cap"; cap.mkdir()
    for i, f in enumerate(seq):
        im = Image.open(tmp / f"{f:04d}.png").convert("RGB"); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, im.width, 30), fill=(30, 34, 32))
        d.text((10, 9), f"JOMO 3D  |  {name}  |  24 fps  |  {'loop' if loop else 'one-shot'}  |  frame {f}/{end}  |  Tobi (left), Amara (right)", fill=(244, 246, 236))
        im.save(cap / f"{i:05d}.png")
    out = outdir / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", str(cap / "%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22", "-movflags", "+faststart", str(out)], check=True)
    shutil.rmtree(tmp); return out

def main():
    blend, mode = sys.argv[1], sys.argv[2]; names = sys.argv[3:]
    bpy.ops.wm.open_mainfile(filepath=blend); sc, cam = stage()
    import s5_animations
    names = names or list(s5_animations.LIBRARY)
    if mode == "sheet":
        outdir = RENDERS / "stage5"; outdir.mkdir(parents=True, exist_ok=True)
        for nm in names:
            p = sheet(contact_sheet(sc, cam, nm, outdir), 6, outdir / f"anim_{nm}.png", f"stage5: {nm} (Tobi left, Amara right)")
            print("wrote", p)
    else:
        outdir = EXPORT / "previews"; outdir.mkdir(parents=True, exist_ok=True)
        for nm in names: print("wrote", mp4(sc, cam, nm, outdir))

if __name__ == "__main__":
    main()
