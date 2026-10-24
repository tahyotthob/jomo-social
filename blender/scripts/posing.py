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
