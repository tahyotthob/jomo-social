"""Stage 2: one shared humanoid rig, built for each character from its own joint positions.

Bone names and hierarchy are identical for Tobi and Amara, so any Action works on both.
Deform bones: hips, spine_01-03, neck, head, shoulder/upper_arm/forearm/hand (.L/.R), 3 bones per
finger (thumb, index, middle, ring, pinky), thigh/shin/foot/toe (.L/.R). Control bones (no deform):
root (locomotion), IK_hand.L/R, IK_foot.L/R, pole_elbow.L/R, pole_knee.L/R.
IK constraints are on the forearms and shins (chain of 2). Their influence is driven by the rig's
custom properties ik_arm_L/R and ik_leg_L/R (0 = FK, the default; 1 = IK).
Output: blender/work/stage2.blend
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *

FINGERS = ("thumb", "index", "middle", "ring", "pinky")

def bone_table(name):
    """(bone, head, tail, parent, deform) in metres, character space."""
    J = joints(name); H = CHARS[name]["height"]; V = lambda p: Vector(p)
    t = [("root", (0, 0, 0), (0, 0.25, 0), None, False),
         ("hips", (0, 0.004, 0.505 * H), J["spine1"], "root", True),
         ("spine_01", J["spine1"], J["spine2"], "hips", True),
         ("spine_02", J["spine2"], J["spine3"], "spine_01", True),
         ("spine_03", J["spine3"], J["neck"], "spine_02", True),
         ("neck", J["neck"], J["head"], "spine_03", True),
         ("head", J["head"], (0, -0.005, H * 0.995), "neck", True)]
    for s, f in ((".L", lambda p: tuple(p)), (".R", mirror)):
        clav0 = (0.012 * H, -0.008, 0.768 * H)
        t += [(f"shoulder{s}", f(clav0), f(J["shoulder"]), "spine_03", True),
              (f"upper_arm{s}", f(J["shoulder"]), f(J["elbow"]), f"shoulder{s}", True),
              (f"forearm{s}", f(J["elbow"]), f(J["wrist"]), f"upper_arm{s}", True),
              (f"hand{s}", f(J["wrist"]), f(J["palm"]), f"forearm{s}", True)]
        for fg in FINGERS:
            for i in range(3):
                t.append((f"{fg}_0{i+1}{s}", f(J[f"{fg}_{i}"]), f(J[f"{fg}_{i+1}"]), f"hand{s}" if i == 0 else f"{fg}_0{i}{s}", True))
        t += [(f"thigh{s}", f(J["hipj"]), f(J["knee"]), "hips", True),
              (f"shin{s}", f(J["knee"]), f(J["ankle"]), f"thigh{s}", True),
              (f"foot{s}", f(J["ankle"]), f(J["ball"]), f"shin{s}", True),
              (f"toe{s}", f(J["ball"]), f(J["toe"]), f"foot{s}", True)]
        # IK controls (children of root) and poles
        w = V(f(J["wrist"])); a = V(f(J["ankle"])); e = V(f(J["elbow"])); k = V(f(J["knee"]))
        t += [(f"IK_hand{s}", tuple(w), tuple(w + Vector((0, 0, -0.08))), "root", False),
              (f"IK_foot{s}", tuple(a), tuple(a + Vector((0, -0.10, 0))), "root", False),
              (f"pole_elbow{s}", tuple(e + Vector((0, 0.35, 0))), tuple(e + Vector((0, 0.40, 0))), "root", False),
              (f"pole_knee{s}", tuple(k + Vector((0, -0.45, 0))), tuple(k + Vector((0, -0.50, 0))), "root", False)]
    return t

def roll_ref(bname):
    if bname.startswith(("foot", "toe", "root", "IK_foot")): return Vector((0, 0, 1))
    return Vector((0, -1, 0))   # Z axis faces forward on limbs, spine and fingers

def build_rig(name, coll):
    arm_data = bpy.data.armatures.new(f"{name}_rig"); arm_data.display_type = "OCTAHEDRAL"
    rig = bpy.data.objects.new(f"{name}_rig", arm_data); coll.objects.link(rig)
    bpy.context.view_layer.objects.active = rig; bpy.ops.object.mode_set(mode="EDIT")
    eb = arm_data.edit_bones; table = bone_table(name)
    for bn, h, tl, par, deform in table:
        b = eb.new(bn); b.head = Vector(h); b.tail = Vector(tl); b.use_deform = deform
    for bn, h, tl, par, deform in table:
        b = eb[bn]
        if par:
            b.parent = eb[par]; b.use_connect = (b.head - eb[par].tail).length < 1e-4 and bn not in ("hips",)
        ref = roll_ref(bn)
        if abs(b.vector.normalized().dot(ref)) > 0.95: ref = Vector((0, 0, 1)) if ref.z == 0 else Vector((0, -1, 0))
        b.align_roll(ref)
    bpy.ops.object.mode_set(mode="OBJECT")
    # IK constraints, driven by FK/IK switches on the rig object
    for s in (".L", ".R"):
        for limb, ctl, pole, prop in (("forearm", "IK_hand", "pole_elbow", "ik_arm"), ("shin", "IK_foot", "pole_knee", "ik_leg")):
            key = f"{prop}_{s[1]}"; rig[key] = 0.0
            pb = rig.pose.bones[f"{limb}{s}"]; c = pb.constraints.new("IK")
            c.target = rig; c.subtarget = f"{ctl}{s}"; c.pole_target = rig; c.pole_subtarget = f"{pole}{s}"
            c.pole_angle = math.radians(-90); c.chain_count = 2; c.use_tail = True
            d = c.driver_add("influence").driver; d.type = "AVERAGE"
            v = d.variables.new(); v.type = "SINGLE_PROP"; v.targets[0].id = rig; v.targets[0].data_path = f'["{key}"]'
        # with IK on, the hand and foot follow their control's rotation
        for bone, ctl, prop in (("hand", "IK_hand", "ik_arm"), ("foot", "IK_foot", "ik_leg")):
            c = rig.pose.bones[f"{bone}{s}"].constraints.new("COPY_ROTATION"); c.target = rig; c.subtarget = f"{ctl}{s}"
            d = c.driver_add("influence").driver; d.type = "AVERAGE"
            v = d.variables.new(); v.type = "SINGLE_PROP"; v.targets[0].id = rig; v.targets[0].data_path = f'["{prop}_{s[1]}"]'
    for pb in rig.pose.bones: pb.rotation_mode = "QUATERNION"
    return rig

def main():
    bpy.ops.wm.open_mainfile(filepath=str(WORK / "stage1.blend"))
    for name in ("tobi", "amara"):
        coll = bpy.data.collections[name.capitalize()]; grp = bpy.data.objects[f"{name}_grp"]
        rig = build_rig(name, coll); rig.location = grp.location.copy()
        for o in list(grp.children):   # rig sits exactly where the empty was, so local coordinates carry over
            o.parent = rig; o.matrix_parent_inverse.identity()
        bpy.data.objects.remove(grp)
        print(name, "bones:", len(rig.data.bones), "deform:", sum(b.use_deform for b in rig.data.bones))
    save(WORK / "stage2.blend")

if __name__ == "__main__":
    main()
