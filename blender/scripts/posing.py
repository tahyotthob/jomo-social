"""Posing helpers shared by the test sheets and the animation library.

Rotations are written in *rig space* (X = character's left, Y = back, Z = up), as if the parent were
at rest, and converted to each bone's local quaternion. Because both rigs are built by the same code
with the same bone rolls, the same pose data gives the same motion on Tobi and Amara.
A pose is {bone: [(axis, degrees), ...]}. Bones ending ".L" are mirrored to ".R" with mirror_pose().
"""
import math
from mathutils import Quaternion, Vector

AX = {"x": Vector((1, 0, 0)), "y": Vector((0, 1, 0)), "z": Vector((0, 0, 1))}

def local_quat(rig, bone, axis, deg):
    R = rig.data.bones[bone].matrix_local.to_3x3()
    a = AX[axis] if isinstance(axis, str) else Vector(axis)
    return (R.inverted() @ Quaternion(a, math.radians(deg)).to_matrix() @ R).to_quaternion()

def mirror_axis(axis):
    a = AX[axis] if isinstance(axis, str) else Vector(axis)
    return Vector((a.x, -a.y, -a.z))

def mirror_pose(pose):
    """Copy every .L entry to .R (mirrored), unless .R is already given."""
    out = dict(pose)
    for b, rots in pose.items():
        if b.endswith(".L"):
            r = b[:-2] + ".R"
            if r not in pose: out[r] = [(mirror_axis(a), d) for a, d in rots]
    return out

def apply_pose(rig, pose, loc=None):
    """Reset every bone, then apply the pose. loc: {bone: (x, y, z)} offsets in rig space."""
    for pb in rig.pose.bones:
        pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)
    for b, rots in pose.items():
        if b not in rig.pose.bones: continue
        q = Quaternion()
        for a, d in rots: q = local_quat(rig, b, a, d) @ q
        rig.pose.bones[b].rotation_quaternion = q
    for b, v in (loc or {}).items():
        R = rig.data.bones[b].matrix_local.to_3x3()
        rig.pose.bones[b].location = R.inverted() @ Vector(v)

def curl(fingers=("index", "middle", "ring", "pinky"), deg=70, thumb=30, side=".L"):
    """Fist / relaxed curl helper: bend each finger segment about the hand's forward-ish axis."""
    p = {}
    for f in fingers:
        for i in (1, 2, 3): p[f"{f}_0{i}{side}"] = [("y", -deg * (0.8 if i == 1 else 1.0))]
    if thumb:
        for i in (1, 2, 3): p[f"thumb_0{i}{side}"] = [("z", -thumb * 0.5), ("y", -thumb * 0.4)]
    return p

# --- test poses used on the stage 2-3 sheets ---
def pose_arms_up():
    return mirror_pose({"upper_arm.L": [("y", -125)], "forearm.L": [("y", -10)], "shoulder.L": [("y", -15)], "spine_03": [("x", 5)]})

def pose_squat():
    return mirror_pose({"thigh.L": [("x", -100), ("y", -10)], "shin.L": [("x", 125)], "foot.L": [("x", -28)],
                        "hips": [("x", 12)], "spine_01": [("x", 12)], "spine_02": [("x", 10)], "neck": [("x", -18)],
                        "upper_arm.L": [("x", -70), ("y", 15)], "forearm.L": [("x", -20)]}), {"root": (0, 0, 0)}

def pose_twist():
    return {"spine_01": [("z", 18)], "spine_02": [("z", 18)], "spine_03": [("z", 16)], "neck": [("z", 10)],
            "hips": [("z", -8)],
            **mirror_pose({"upper_arm.L": [("y", 35)], "forearm.L": [("x", 50)]})}

TEST_POSES = {"rest": lambda: ({}, {}), "arms overhead": lambda: (pose_arms_up(), {}),
              "deep squat": lambda: pose_squat(), "torso twist": lambda: (pose_twist(), {})}

# --- reach solver: find arm angles that put a hand (or fingertip) on a target ---
def nelder_mead(f, x0, step=12.0, iters=500, tol=1e-7):
    n = len(x0); pts = [list(x0)] + [[x0[j] + (step if j == i else 0) for j in range(n)] for i in range(n)]
    vals = [f(p) for p in pts]
    for _ in range(iters):
        order = sorted(range(n + 1), key=lambda i: vals[i]); pts = [pts[i] for i in order]; vals = [vals[i] for i in order]
        if vals[-1] - vals[0] < tol: break
        c = [sum(p[j] for p in pts[:-1]) / n for j in range(n)]
        xr = [c[j] + (c[j] - pts[-1][j]) for j in range(n)]; fr = f(xr)
        if fr < vals[0]:
            xe = [c[j] + 2 * (c[j] - pts[-1][j]) for j in range(n)]; fe = f(xe)
            pts[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]: pts[-1], vals[-1] = xr, fr
        else:
            xc = [c[j] + 0.5 * (pts[-1][j] - c[j]) for j in range(n)]; fc = f(xc)
            if fc < vals[-1]: pts[-1], vals[-1] = xc, fc
            else:
                pts = [pts[0]] + [[pts[0][j] + 0.5 * (p[j] - pts[0][j]) for j in range(n)] for p in pts[1:]]
                vals = [vals[0]] + [f(p) for p in pts[1:]]
    i = min(range(n + 1), key=lambda i: vals[i]); return pts[i], vals[i]

ARM_DOF = [("upper_arm", "x"), ("upper_arm", "y"), ("upper_arm", "z"), ("forearm", "x"), ("forearm", "z"), ("hand", "x"), ("hand", "z")]

def arm_entries(x):
    """Solver vector -> left-arm pose entries (rig-space degrees, applied after the A-pose rest)."""
    out = {}
    for (b, a), v in zip(ARM_DOF, x): out.setdefault(f"{b}.L", []).append((a, v))
    return out

def palm_normal(rig, side, ref=None):
    """Palm direction (armature space) of the posed hand: the palm faces down-in at rest.
    ref: any other rest-space direction carried by the hand (e.g. a held tablet's screen normal)."""
    b = rig.data.bones[f"hand{side}"]; d = (b.tail_local - b.head_local).normalized()
    n0 = -(d.cross(Vector((0, 1, 0)))).normalized()
    if side == ".R": n0 = -(Vector((0, 1, 0)).cross(d)).normalized()
    if ref is not None: n0 = Vector(ref).normalized()
    pb = rig.pose.bones[f"hand{side}"]
    return (pb.matrix.to_3x3() @ b.matrix_local.to_3x3().inverted() @ n0).normalized()

def reach(rig, base, target, side="L", tip="hand", normal=None, x0=None, wn=0.02, reg=2e-7, ref=None):
    """Solve the 7 arm angles so bone `tip` (tail) of that side reaches `target` (armature space, metres)
    with the palm facing `normal`. base: the rest of the pose. Returns left-convention arm entries,
    ready to pass through side(..., side)."""
    import bpy
    meshes = [o for o in rig.children if o.type == "MESH"]
    for o in meshes:
        for m in o.modifiers: m.show_viewport = False
    s = "." + side; tgt = Vector(target); nt = Vector(normal).normalized() if normal else None
    def f(x):
        e = arm_entries(x); e = e if side == "L" else _flip(e)
        p = {k: v for k, v in base.items() if not any(k.startswith(b) for b in ("upper_arm" + s, "forearm" + s, "hand" + s))}
        p.update(e)
        apply_pose(rig, p); bpy.context.view_layer.update()
        c = (rig.pose.bones[f"{tip}{s}"].tail - tgt).length_squared
        if nt is not None: c += wn * (1 - palm_normal(rig, s, ref).dot(nt))
        return c + reg * sum(v * v for v in x)
    best, val = nelder_mead(f, list(x0 or [-30, 20, 0, -60, 0, 0, 0]))
    best, val = nelder_mead(f, best, step=4)   # restart to polish
    for o in meshes:
        for m in o.modifiers: m.show_viewport = True
    return arm_entries([round(v, 1) for v in best]), val

def _flip(pose):
    out = {}
    for b, rots in pose.items():
        nb = b[:-2] + (".R" if b.endswith(".L") else ".L") if b.endswith((".L", ".R")) else b
        out[nb] = [(mirror_axis(a), d) for a, d in rots]
    return out

def carried(rig, side, rest_point):
    """Where a point carried rigidly by the hand (rest armature space) is in the current pose."""
    b = rig.data.bones[f"hand{side}"]; pb = rig.pose.bones[f"hand{side}"]
    return (pb.matrix @ b.matrix_local.inverted()) @ Vector(rest_point)
