"""Stage 5: the animation library, as reusable Actions (24 fps).

Every Action keys only pose bones (by name) and the rig's face properties, so it plays on any rig
built by s2_rig.py: assign it to NAME_rig.animation_data.action (and the action's one slot).
Poses are written in rig-space degrees with posing.py (see that file for the axis conventions):
  thigh/upper_arm x<0 = swing forward, shin x>0 = knee bend, foot x>0 = toes down,
  spine x>0 = bend forward, neck/head x>0 = look down, upper_arm.L y<0 = raise the arm sideways,
  forearm x<0 = bend the elbow forward. ".L" entries are mirrored to ".R" unless .R is given.
Locomotion cycles are in place; the root bone stays at the origin (engines move the character).
Hips translations are in metres for Tobi's proportions; on Amara they read the same at her scale.
Output: blender/work/stage5.blend
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *
import posing
from posing import mirror_pose, mirror_axis, apply_pose
from s3_skin import FACE_PROPS

FPS = 24

# ---------- pose helpers ----------
def M(*dicts):
    """Merge poses; later rotations on the same bone are appended (applied after)."""
    out = {}
    for d in dicts:
        for b, r in d.items(): out[b] = out.get(b, []) + list(r)
    return out

def flip(pose):
    """Swap sides: .L <-> .R with mirrored axes; centre bones mirrored too (twists reverse)."""
    out = {}
    for b, rots in pose.items():
        nb = b[:-2] + (".R" if b.endswith(".L") else ".L") if b.endswith((".L", ".R")) else b
        out[nb] = [(mirror_axis(a), d) for a, d in rots]
    return out

def side(pose, s):
    """Write a pose for the left side and use it on side s ('L' or 'R') only."""
    return pose if s == "L" else flip(pose)

def flip_loc(loc):
    return {b: (-v[0], v[1], v[2]) for b, v in loc.items()}

def curl(fingers=("index", "middle", "ring", "pinky"), deg=75, thumb=35, s="L"):
    p = posing.curl(fingers, deg, thumb, ".L")
    return side(p, s)

def open_hand(s="L", spread=6):
    p = {f"{f}_01.L": [("y", 4)] for f in ("index", "middle", "ring", "pinky")}
    return side(p, s)

RELAX = M(mirror_pose({"upper_arm.L": [("y", 36)], "forearm.L": [("x", -14)], "hand.L": [("x", -6)]}),
          curl(deg=18, thumb=10, s="L"), curl(deg=18, thumb=10, s="R"))

def K(frame, pose=None, loc=None, face=None):
    return (frame, pose or {}, loc or {}, face or {})

# ---------- contact poses, solved on a rig ----------
RIGS = {}   # filled in main(): the rigs the reach solver measures on

def arm_to(base, target, s="L", tip="hand", normal=None, who="tobi", ref=None):
    """Left-convention arm entries that put `tip` of side s on `target` (that rig's armature space),
    returned already on side s."""
    e, _ = posing.reach(RIGS[who], base, target, s, tip, normal, ref=ref)
    return side(e, s)

# ---------- the library ----------
def idle():
    a = M(RELAX, {"spine_02": [("x", -1.5)], "spine_03": [("x", -1)], "neck": [("x", 1)]})
    b = M(RELAX, {"spine_02": [("x", 1.0)], "spine_03": [("x", 1)], "head": [("z", 3), ("x", 2)],
                  "shoulder.L": [("y", -2)], "shoulder.R": [("y", 2)], "hips": [("z", -2)]})
    c = M(RELAX, {"spine_02": [("x", -1.0)], "head": [("z", -2)], "hips": [("z", 1.5)]})
    return dict(frames=96, loop=True, keys=[
        K(0, a, {"hips": (0.006, 0, 0)}), K(32, b, {"hips": (-0.008, 0, -0.004)}), K(64, c, {"hips": (0.004, 0, 0.002)}),
        K(80, c, face={"blink": 0}), K(83, c, face={"blink": 1}), K(86, c, face={"blink": 0}),
        K(96, a, {"hips": (0.006, 0, 0)})])

def walk_keys(L):
    """L = dict of angles for one half-cycle. Returns keys for a full in-place cycle."""
    half = L["n"] // 2
    def contact():
        p = {"thigh.L": [("x", L["tf"])], "shin.L": [("x", L["sf"])], "foot.L": [("x", L["ff"])],
             "thigh.R": [("x", L["tb"])], "shin.R": [("x", L["sb"])], "foot.R": [("x", L["fb"])], "toe.R": [("x", L["toe"])],
             "upper_arm.L": [("y", 34), ("x", L["arm"])], "upper_arm.R": [("y", -34), ("x", -L["arm"])],
             "forearm.L": [("x", -L["el"] * 0.6)], "forearm.R": [("x", -L["el"])],
             "hips": [("z", -L["tw"])], "spine_02": [("z", L["tw"] * 0.7)], "spine_03": [("z", L["tw"] * 0.6)],
             "spine_01": [("x", L["lean"])], "neck": [("x", -L["lean"] * 0.6)]}
        return M(p, curl(deg=20, thumb=10, s="L"), curl(deg=20, thumb=10, s="R"))
    def passing():
        p = {"thigh.L": [("x", L["pt"])], "shin.L": [("x", L["ps"])], "foot.L": [("x", -L["pt"] - L["ps"])],
             "thigh.R": [("x", L["st"])], "shin.R": [("x", L["ss"])], "foot.R": [("x", L["sw"])],
             "upper_arm.L": [("y", 34)], "upper_arm.R": [("y", -34)],
             "forearm.L": [("x", -L["el"] * 0.8)], "forearm.R": [("x", -L["el"] * 0.8)],
             "spine_01": [("x", L["lean"])], "neck": [("x", -L["lean"] * 0.6)]}
        return M(p, curl(deg=20, thumb=10, s="L"), curl(deg=20, thumb=10, s="R"))
    q = half // 4
    c, d, pz = contact(), passing(), L["bob"]
    hz = lambda z, x=0.0: {"hips": (x, 0, z)}
    return [K(0, c, hz(pz[0], L["sway"])), K(q, d if False else c, hz(pz[1], L["sway"])),
            K(2 * q, d, hz(pz[2], -L["sway"] * 0.2)),
            K(half, flip(c), hz(pz[0], -L["sway"])), K(half + 2 * q, flip(d), hz(pz[2], L["sway"] * 0.2)),
            K(L["n"], c, hz(pz[0], L["sway"]))]

def walk():
    L = dict(n=32, tf=-24, sf=6, ff=8, tb=16, sb=14, fb=-6, toe=-22, arm=-18, el=18, tw=5, lean=3,
             pt=-2, ps=6, st=-24, ss=56, sw=-22, bob=(-0.012, -0.03, 0.012), sway=0.012)
    keys = walk_keys(L)
    keys[1] = K(4, M(keys[0][1], {"shin.L": [("x", 12)], "foot.L": [("x", -10)]}), {"hips": (0.012, 0, -0.03)})
    keys.insert(4, K(20, flip(keys[1][1]), {"hips": (-0.012, 0, -0.03)}))
    keys = sorted(keys, key=lambda k: k[0])
    for k in keys: k[3].update({"smile": 0.15})
    return dict(frames=32, loop=True, keys=keys, speed=1.3)

def run():
    L = dict(n=20, tf=-42, sf=22, ff=-2, tb=30, sb=40, fb=-10, toe=-25, arm=-40, el=85, tw=9, lean=10,
             pt=-8, ps=40, st=-50, ss=110, sw=-30, bob=(-0.03, -0.05, 0.035), sway=0.008)
    keys = walk_keys(L)
    return dict(frames=20, loop=True, keys=keys, speed=3.6)

def jump():
    crouch = M(RELAX, mirror_pose({"thigh.L": [("x", -62)], "shin.L": [("x", 92)], "foot.L": [("x", -30)],
                                   "upper_arm.L": [("x", 45)], "forearm.L": [("x", -10)]}),
               {"spine_01": [("x", 18)], "spine_02": [("x", 10)], "neck": [("x", -14)]})
    push = M(mirror_pose({"thigh.L": [("x", 4)], "shin.L": [("x", 2)], "foot.L": [("x", 30)], "toe.L": [("x", -20)],
                          "upper_arm.L": [("y", -95), ("x", -25)], "forearm.L": [("x", -15)]}),
             {"spine_01": [("x", -4)], "neck": [("x", -6)]}, curl(deg=40, s="L"), curl(deg=40, s="R"))
    tuck = M(mirror_pose({"thigh.L": [("x", -45)], "shin.L": [("x", 70)], "foot.L": [("x", 5)],
                          "upper_arm.L": [("y", -80), ("x", -20)], "forearm.L": [("x", -20)]}), curl(deg=40, s="L"), curl(deg=40, s="R"))
    land = M(RELAX, mirror_pose({"thigh.L": [("x", -22)], "shin.L": [("x", 30)], "foot.L": [("x", -2)],
                                 "upper_arm.L": [("x", -30), ("y", -20)]}))
    absorb = M(RELAX, mirror_pose({"thigh.L": [("x", -55)], "shin.L": [("x", 80)], "foot.L": [("x", -25)],
                                   "upper_arm.L": [("x", -35)], "forearm.L": [("x", -25)]}),
               {"spine_01": [("x", 16)], "spine_02": [("x", 8)], "neck": [("x", -12)]})
    return dict(frames=44, loop=False, keys=[
        K(0, RELAX), K(9, crouch, {"hips": (0, 0.04, -0.17)}), K(14, push, {"hips": (0, 0, 0.05)}, {"surprise": 0.3}),
        K(20, tuck, {"hips": (0, 0, 0.36)}, {"smile": 0.8, "open": 0.4}), K(26, land, {"hips": (0, 0, 0.02)}),
        K(30, absorb, {"hips": (0, 0.03, -0.14)}, {"smile": 0.6}), K(44, RELAX)])

def wave():
    up = M(RELAX, side({"upper_arm.L": [("y", -36), ("y", -95), ("x", -12)], "forearm.L": [("y", -40)],
                        "hand.L": [("x", -10)]}, "R"), open_hand("R"), {"head": [("z", 6), ("y", -4)]})
    def sw(d): return M(up, side({"forearm.L": [("y", d)], "hand.L": [("y", d * 0.6)]}, "R"))
    f = {"smile": 0.9}
    return dict(frames=56, loop=False, keys=[
        K(0, RELAX), K(10, up, face=f), K(16, sw(-20), face=f), K(22, sw(18), face=f), K(28, sw(-20), face=f),
        K(34, sw(18), face=f), K(40, up, face=f), K(56, RELAX)])

def talk():
    base = M(mirror_pose({"upper_arm.L": [("y", 28), ("x", -22)], "forearm.L": [("x", -62)], "hand.L": [("z", 25)]}),
             open_hand("L"), open_hand("R"))
    gR = M(base, side({"upper_arm.L": [("x", -14), ("y", -14)], "forearm.L": [("x", -12), ("z", 30)], "hand.L": [("y", -20)]}, "R"),
           {"head": [("z", -5), ("x", -3)], "spine_03": [("z", -4)]})
    both = M(base, mirror_pose({"upper_arm.L": [("y", -16)], "forearm.L": [("z", 25)], "hand.L": [("y", -15)]}),
             {"head": [("x", 4)], "spine_02": [("x", 3)]})
    gL = M(base, side({"upper_arm.L": [("x", -14), ("y", -14)], "forearm.L": [("x", -12), ("z", 30)], "hand.L": [("y", -20)]}, "L"),
           {"head": [("z", 5), ("x", -3)], "spine_03": [("z", 4)]})
    vis = ["vis_A", "vis_E", "vis_MBP", "vis_O", "vis_E", "vis_A", "vis_U", "vis_FV", "vis_A", "vis_E", "vis_MBP", "vis_O"]
    keys = [K(0, base), K(24, gR, face={"surprise": 0.25}), K(48, both, face={"smile": 0.4}), K(72, gL), K(96, base)]
    # lip-sync style face keys every 4 frames, layered on the body keys at the nearest pose
    poses = {0: base, 24: gR, 48: both, 72: gL, 96: base}
    for i in range(0, 96, 4):
        v = vis[(i // 4) % len(vis)]; f = {p: 0.0 for p in vis}; f[v] = 1.0 if i % 24 not in (20,) else 0.0
        if i in poses: continue
        keys.append(K(i, None, None, f))
    return dict(frames=96, loop=True, keys=sorted(keys, key=lambda k: k[0]), face_only_ok=True)

def celebrate():
    vup = M(mirror_pose({"upper_arm.L": [("y", -125)], "forearm.L": [("y", -12)]}), curl(deg=85, thumb=45, s="L"), curl(deg=85, thumb=45, s="R"),
            {"neck": [("x", -10)], "spine_02": [("x", -5)]})
    pump = M(mirror_pose({"upper_arm.L": [("y", -100), ("x", -10)], "forearm.L": [("x", -55)]}), curl(deg=85, thumb=45, s="L"), curl(deg=85, thumb=45, s="R"),
             {"neck": [("x", -6)]})
    crouch = M(RELAX, mirror_pose({"thigh.L": [("x", -30)], "shin.L": [("x", 45)], "foot.L": [("x", -15)]}), {"spine_01": [("x", 10)]})
    laugh = {"smile": 1.0, "open": 0.75}
    return dict(frames=64, loop=False, keys=[
        K(0, RELAX), K(8, crouch, {"hips": (0, 0.02, -0.08)}), K(15, vup, {"hips": (0, 0, 0.10)}, laugh), K(22, vup, {}, laugh),
        K(30, pump, {"hips": (0, 0, -0.02)}, laugh), K(38, vup, {"hips": (0, 0, 0.02)}, laugh), K(46, pump, {"hips": (0, 0, -0.02)}, laugh),
        K(52, vup, {}, {"smile": 1.0, "open": 0.4}), K(64, RELAX, face={"smile": 0.5})])

LT = 0.40   # thigh length used for the seat drop (metres)
def seated():
    return M(mirror_pose({"thigh.L": [("x", -90)], "shin.L": [("x", 90)], "upper_arm.L": [("x", -38), ("y", 34)],
                          "forearm.L": [("x", -22)]}), curl(deg=25, s="L"), curl(deg=25, s="R"))

def sit_keys(reverse=False):
    lean = M(RELAX, mirror_pose({"thigh.L": [("x", -30)], "shin.L": [("x", 38)], "foot.L": [("x", -8)],
                                 "upper_arm.L": [("x", -30)]}), {"spine_01": [("x", 24)], "spine_02": [("x", 10)], "neck": [("x", -18)]})
    mid = M(mirror_pose({"thigh.L": [("x", -66)], "shin.L": [("x", 70)], "foot.L": [("x", -4)],
                         "upper_arm.L": [("x", -50), ("y", 20)], "forearm.L": [("x", -20)]}),
            {"spine_01": [("x", 30)], "spine_02": [("x", 12)], "neck": [("x", -24)]})
    touch = M(seated(), {"spine_01": [("x", 12)], "neck": [("x", -8)]})
    keys = [K(0, RELAX), K(12, lean, {"hips": (0, 0.10, -0.10)}), K(24, mid, {"hips": (0, 0.28, -0.29)}),
            K(36, touch, {"hips": (0, LT, -LT)}), K(48, seated(), {"hips": (0, LT, -LT)})]
    if reverse:
        keys = [K(48 - f, p, l, fc) for f, p, l, fc in reversed(keys)]
    return keys

def sit_down(): return dict(frames=48, loop=False, keys=sit_keys())
def stand_up(): return dict(frames=48, loop=False, keys=sit_keys(reverse=True))

def point():
    p = M(RELAX, side({"upper_arm.L": [("y", -36), ("x", -88), ("z", -28)], "forearm.L": [("x", -6)], "hand.L": [("x", -4)]}, "R"),
          side(posing.curl(("middle", "ring", "pinky"), 85, 40, ".L"), "R"), side({"index_01.L": [("y", 6)]}, "R"),
          {"head": [("z", -10)], "spine_03": [("z", -6)]})
    p2 = M(p, side({"upper_arm.L": [("x", -4)]}, "R"))
    return dict(frames=44, loop=False, keys=[K(0, RELAX), K(10, p, face={"smile": 0.3}), K(16, p2, face={"smile": 0.3, "vis_E": 0.5}),
                                             K(22, p, face={"smile": 0.3}), K(32, p, face={"smile": 0.3}), K(44, RELAX)])

def clap():
    apart = M(mirror_pose(arm_to({}, (0.16, -0.30, 1.15), normal=(-1, 0, 0))), open_hand("L"), open_hand("R"))
    shut = M(mirror_pose(arm_to({}, (0.022, -0.30, 1.13), normal=(-1, 0, 0))), open_hand("L"), open_hand("R"))
    f = {"smile": 0.85}
    return dict(frames=36, loop=True, keys=[K(0, apart, face=f), K(4, shut, {"hips": (0, 0, -0.008)}, f), K(9, apart, face=f),
                                            K(13, shut, {"hips": (0, 0, -0.008)}, f), K(18, apart, face=f),
                                            K(22, shut, {"hips": (0, 0, -0.008)}, f), K(27, apart, face=f),
                                            K(31, shut, {"hips": (0, 0, -0.008)}, f), K(36, apart, face=f)])

def dance():
    def beat(s, down):
        knees = {"thigh.L": [("x", -16 if down else -4)], "shin.L": [("x", 30 if down else 8)], "foot.L": [("x", -14 if down else -4)]}
        arms = {"upper_arm.L": [("y", 20), ("x", -28)], "forearm.L": [("x", -80)],
                "upper_arm.R": [("y", -20), ("x", 14)], "forearm.R": [("x", -70)], "shoulder.L": [("y", -8)]}
        p = M(mirror_pose(knees), arms, curl(deg=55, s="L"), curl(deg=55, s="R"),
              {"hips": [("z", 10), ("y", 4)], "spine_02": [("z", -8)], "spine_03": [("z", -4)], "head": [("x", 6 if down else -3), ("z", 4)]})
        return p if s == "L" else flip(p)
    f = {"smile": 0.7}
    keys = []
    for i, (s, x) in enumerate((("L", 0.035), ("R", -0.035))):
        t = i * 24
        keys += [K(t, beat(s, True), {"hips": (x, 0, -0.045)}, f), K(t + 6, beat(s, False), {"hips": (x * 0.6, 0, 0.0)}, f),
                 K(t + 12, beat(s, True), {"hips": (x, 0, -0.045)}, f), K(t + 18, beat(s, False), {"hips": (x * 0.2, 0, 0.0)}, f)]
    keys.append(K(48, beat("L", True), {"hips": (0.035, 0, -0.045)}, f))
    return dict(frames=48, loop=True, keys=keys)

def react_surprise():
    s = M(mirror_pose({"upper_arm.L": [("y", 18), ("x", -45)], "forearm.L": [("x", -70)], "hand.L": [("x", -25)]}),
          open_hand("L"), open_hand("R"), {"spine_02": [("x", -8)], "spine_03": [("x", -4)], "head": [("x", -6)], "neck": [("x", -4)]})
    face = {"surprise": 1.0}
    return dict(frames=48, loop=False, keys=[K(0, RELAX), K(5, s, {"hips": (0, 0.03, 0.01)}, face), K(30, s, {"hips": (0, 0.03, 0.0)}, face),
                                             K(48, RELAX, face={"surprise": 0.0})])

def react_sad():
    s = M(mirror_pose({"upper_arm.L": [("y", 42)], "forearm.L": [("x", -8)], "shoulder.L": [("y", 5)]}), curl(deg=12, s="L"), curl(deg=12, s="R"),
          {"spine_01": [("x", 6)], "spine_02": [("x", 8)], "spine_03": [("x", 6)], "neck": [("x", 12)], "head": [("x", 8), ("z", 5)]})
    face = {"sad": 1.0}
    return dict(frames=60, loop=False, keys=[K(0, RELAX), K(14, s, {"hips": (0, 0.01, -0.01)}, face),
                                             K(40, M(s, {"head": [("z", -6)]}), {"hips": (0, 0.01, -0.012)}, dict(face, blink=0.0)),
                                             K(43, s, None, dict(face, blink=0.7)), K(46, s, None, dict(face, blink=0.0)),
                                             K(60, RELAX, face={"sad": 0.0})])

def react_laugh():
    lean = {"spine_02": [("x", -6)], "neck": [("x", -8)], "head": [("x", -6)]}
    belly = arm_to(M(RELAX, lean), (-0.045, -0.165, 1.00), "R", normal=(0, 1, 0))   # right hand on the belly
    base = M(RELAX, lean); base.update(belly)
    hi = M(base, {"shoulder.L": [("y", -6)], "shoulder.R": [("y", 6)], "spine_02": [("x", -3)]})
    face = {"smile": 1.0, "open": 0.8, "blink": 0.55}
    keys = [K(0, RELAX)]
    for i, t in enumerate(range(6, 42, 6)):
        keys.append(K(t, hi if i % 2 else base, {"hips": (0, 0, -0.01 if i % 2 else 0.0)}, dict(face, open=0.8 if i % 2 else 0.5)))
    keys.append(K(54, RELAX, face={"smile": 0.6}))
    return dict(frames=54, loop=False, keys=keys)

def selfie_hype():
    """Tobi's signature: phone up for a selfie, lean in, peace sign, wink."""
    lean = {"spine_03": [("z", -6)], "head": [("z", -8), ("y", 8)]}
    ph = M(RELAX, lean); ph.update(arm_to(ph, (-0.30, -0.42, 1.72), "R"))                      # phone up and out front
    peace = dict(ph); peace.update(arm_to(ph, (0.17, -0.12, 1.66), "L", normal=(0, -1, 0)))   # peace sign by the face
    peace = M(peace, posing.curl(("ring", "pinky"), 90, 50, ".L"), {"index_01.L": [("z", 8)], "middle_01.L": [("z", -6)]})
    return dict(frames=84, loop=False, keys=[
        K(0, RELAX), K(14, ph, {"hips": (0, 0, 0)}, {"smile": 0.6}), K(26, peace, {"hips": (0.02, 0, -0.01)}, {"smile": 1.0}),
        K(36, peace, None, {"smile": 1.0, "blink_L": 0}), K(39, peace, None, {"smile": 1.0, "blink_L": 1}),
        K(46, peace, None, {"smile": 1.0, "blink_L": 1}), K(50, peace, None, {"smile": 1.0, "blink_L": 0}),
        K(60, M(peace, {"head": [("x", 6)]}), None, {"smile": 1.0, "open": 0.5}), K(84, RELAX, face={"smile": 0.4})])

def fact_check():
    """Amara's signature: tablet up, push glasses up, read, nod 'verified', tap the screen."""
    rig = RIGS["amara"]; look = {"neck": [("x", 12)], "head": [("x", 8)]}
    # tablet held in front of the chest, screen tilted up towards her face
    tab = M(RELAX, look); tab.update(arm_to(tab, (0.10, -0.29, 0.97), "L", who="amara", normal=(0, 0.5, 0.87), ref=(0, -1, 0)))
    # right index finger pushes the glasses up at the bridge
    gl = bpy.data.objects["amara_glasses"]; vs = [v.co for v in gl.data.vertices if abs(v.co.x) < 0.02]
    bridge = Vector((0, min(v.y for v in vs) - 0.012, sum(v.z for v in vs) / len(vs)))
    up = {"neck": [("x", -2)], "head": [("x", -4)]}
    gbase = M(dict(tab), up); glasses = dict(gbase)
    glasses.update(arm_to(gbase, bridge, "R", tip="index_03", who="amara"))
    glasses = M(glasses, side(posing.curl(("middle", "ring", "pinky"), 85, 40, ".L"), "R"))
    read = M(tab, {"neck": [("x", 4)]})
    # right index taps the middle of the screen
    tb = bpy.data.objects["amara_tablet"]; scr = [p for p in tb.data.polygons if p.normal.y < -0.9 and p.area > 0.015]
    c0 = scr[0].center if scr else sum((v.co for v in tb.data.vertices), Vector()) / len(tb.data.vertices)
    apply_pose(rig, read); bpy.context.view_layer.update()
    n = posing.palm_normal(rig, ".L", (0, -1, 0)); spot = posing.carried(rig, ".L", c0) + n * 0.01
    tap = dict(read); tap.update(arm_to(read, spot, "R", tip="index_03", who="amara"))
    tap = M(tap, side(posing.curl(("middle", "ring", "pinky"), 85, 40, ".L"), "R"))
    focus = {"frown": 0.35}
    return dict(frames=96, loop=False, keys=[
        K(0, RELAX), K(14, tab, None, focus), K(26, glasses, None, {"frown": 0.1}), K(32, glasses, None, {"frown": 0.1}),
        K(42, read, None, focus), K(54, read, None, focus),
        K(60, M(read, {"head": [("x", 10)]}), None, {"smile": 0.6}), K(66, M(read, {"head": [("x", -4)]}), None, {"smile": 0.6}),
        K(72, M(read, {"head": [("x", 10)]}), None, {"smile": 0.6}), K(80, tap, None, {"smile": 0.8, "vis_E": 0.4}),
        K(96, RELAX, face={"smile": 0.3})])

LIBRARY = {
    "idle": idle, "walk": walk, "run": run, "jump": jump, "wave": wave, "talk": talk, "celebrate": celebrate,
    "sit_down": sit_down, "stand_up": stand_up, "point": point, "clap": clap, "dance": dance,
    "react_surprise": react_surprise, "react_sad": react_sad, "react_laugh": react_laugh,
    "tobi_selfie_hype": selfie_hype, "amara_fact_check": fact_check,
}
SIGNATURE = {"tobi": "tobi_selfie_hype", "amara": "amara_fact_check"}

# ---------- baking keys into Actions ----------
def build_action(rig, name, spec):
    deform_and_root = [pb.name for pb in rig.pose.bones if pb.bone.use_deform or pb.name == "root"]
    act = bpy.data.actions.new(name); act.use_fake_user = True
    rig.animation_data_create(); rig.animation_data.action = act
    face_state = {p: 0.0 for p in FACE_PROPS}
    last_pose = ({}, {})
    for frame, pose, loc, face in spec["keys"]:
        if pose or loc or not face:
            last_pose = (pose, loc)
        apply_pose(rig, *last_pose)
        for pb in rig.pose.bones:
            q = pb.rotation_quaternion
            if q.w < 0: pb.rotation_quaternion = -q   # keep quaternions in one hemisphere so keys interpolate the short way
        if pose or loc or not face:
            for b in deform_and_root:
                pb = rig.pose.bones[b]
                pb.keyframe_insert("rotation_quaternion", frame=frame, group=b)
                if b in ("hips", "root"): pb.keyframe_insert("location", frame=frame, group=b)
        if face or frame == 0 or frame == spec["frames"]:
            # face props default back to 0 unless the key says otherwise
            st = {p: 0.0 for p in FACE_PROPS} if (pose or loc) else dict(face_state)
            st.update(face); face_state = st
            for p, v in st.items():
                rig[p] = v; rig.keyframe_insert(f'["{p}"]', frame=frame, group="face")
    act.use_frame_range = True; act.frame_start, act.frame_end = 0, spec["frames"] - (1 if spec["loop"] else 0)
    act.use_cyclic = spec["loop"]
    act["fps"] = FPS; act["loop"] = spec["loop"]; act["frames"] = spec["frames"]
    if "speed" in spec: act["root_speed_m_s"] = spec["speed"]
    return act

def main():
    bpy.ops.wm.open_mainfile(filepath=str(WORK / "stage4.blend"))
    sc = bpy.context.scene; sc.render.fps = FPS
    for n in ("tobi", "amara"):
        r = bpy.data.objects[f"{n}_rig"]; RIGS[n] = r
        if r.animation_data: r.animation_data.action = None
    rig = bpy.data.objects["tobi_rig"]   # authored once; the same Actions play on amara_rig
    for name, fn in LIBRARY.items():
        act = build_action(rig, name, fn())
        print(f"{name}: {act['frames']} frames, loop={act['loop']}, fcurves={sum(len(cb.fcurves) for l in act.layers for s in l.strips for cb in s.channelbags)}")
    for n in ("tobi", "amara"):
        r = bpy.data.objects[f"{n}_rig"]; r.animation_data_create()
        r.animation_data.action = bpy.data.actions["idle"]; r.animation_data.action_slot = bpy.data.actions["idle"].slots[0]
        posing.apply_pose(r, {})
    save(WORK / "stage5.blend")

if __name__ == "__main__":
    main()
