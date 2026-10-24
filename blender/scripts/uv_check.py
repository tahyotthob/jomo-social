"""UV check: draws each character's UVs over the palette atlas and counts overlapping faces.

    python3 blender/scripts/uv_check.py blender/work/stage4.blend stage4
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *
from PIL import Image, ImageDraw

def count_overlaps(ob, faces=False):
    """Exact test: UV triangles (shrunk 2% so shared edges don't count) checked pairwise via a grid."""
    from mathutils.geometry import intersect_tri_tri_2d
    from collections import defaultdict
    me = ob.data; uv = me.uv_layers["UVMap"].data; tris = []
    for p in me.polygons:
        pts = [Vector((uv[li].uv.x, uv[li].uv.y, 0)) for li in p.loop_indices]
        c = sum(pts, Vector()) / len(pts); pts = [q + (c - q) * 0.02 for q in pts]
        for k in range(1, len(pts) - 1): tris.append((p.index, pts[0], pts[k], pts[k + 1]))
    G = 1 / 4096; grid = defaultdict(list); bad = set()
    for ti, (fi, a, b, c) in enumerate(tris):
        xs = (a.x, b.x, c.x); ys = (a.y, b.y, c.y)
        for gx in range(int(min(xs) / G), int(max(xs) / G) + 1):
            for gy in range(int(min(ys) / G), int(max(ys) / G) + 1):
                for tj in grid[(gx, gy)]:
                    fj, a2, b2, c2 = tris[tj]
                    if fj != fi and intersect_tri_tri_2d(a.xy, b.xy, c.xy, a2.xy, b2.xy, c2.xy): bad.add(fi)
                grid[(gx, gy)].append(ti)
    return bad if faces else len(bad)

def main():
    blend, stage = sys.argv[1], sys.argv[2]
    bpy.ops.wm.open_mainfile(filepath=blend)
    import numpy as np
    pal = Image.open(BL / "textures" / "jomo_palette.png").convert("RGB").resize((1024, 1024), Image.NEAREST)
    outs = []; report = []
    for name in ("tobi", "amara"):
        im = pal.copy(); d = ImageDraw.Draw(im); N = 1024
        cover = np.zeros((N, N), np.int16)
        for ob in sorted([o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith(name)], key=lambda o: o.name):
            uv = ob.data.uv_layers["UVMap"].data; obj_cover = Image.new("L", (N, N), 0); oc = ImageDraw.Draw(obj_cover)
            for p in ob.data.polygons:
                d.polygon([(uv[li].uv.x * N, (1 - uv[li].uv.y) * N) for li in p.loop_indices], outline=(255, 255, 255) if name else None)
            over = count_overlaps(ob)
            report.append(f"{ob.name}: {len(ob.data.polygons)} faces, {over} overlapping")
        outs.append(im)
    S = Image.new("RGB", (2048 + 30, 1024 + 40), (244, 246, 236)); dd = ImageDraw.Draw(S)
    dd.rectangle((0, 0, S.width, 34), fill=(165, 205, 57)); dd.text((10, 10), f"{stage}: UVs on the palette atlas (Tobi left, Amara right)", fill=(30, 34, 32))
    S.paste(outs[0], (0, 40)); S.paste(outs[1], (1054, 40))
    out = RENDERS / stage / f"{stage}_uv_layout.png"; out.parent.mkdir(parents=True, exist_ok=True); S.save(out)
    print("\n".join(report)); print("wrote", out)

if __name__ == "__main__":
    main()
