# Decisions: JOMO 3D character set (Blender)

Decisions made while building the 3D versions of Tobi and Amara, so anyone can see why things are the way they are. The newest are at the bottom of each section.

## Characters (source: `references/avatars.md` and the approved 2D character sheets)
- **Two characters:** Tobi and Amara. They are the only characters in the set.
- **Heights:** Tobi 1.80 m, Amara 1.66 m. The 2D art gives no heights; these are typical for young Nigerian adults and keep Tobi a little taller, as in the art.
- **Builds:** Tobi is slim-athletic with broader shoulders, wearing an oversized tee. Amara is slim with narrower shoulders and slightly wider hips.
- **Skin:** Tobi is darker (#5A3820), Amara medium-dark (#8B5A3C). Both are sampled from the approved 2D art and rounded.
- **Brand palette for clothes and props:** Leaf Lime #A5CD39, Leaf Green #8FB73C, Olive #77962A, Charcoal #323534, Ink #1E2220, Off-white #F4F6EC. These come from `references/brand-guide.md`.
- **Signature colours:** Tobi is Leaf Lime (shirt, bandana). Amara is Off-white and Olive with Lime accents (lanyard), matching the art direction in `references/avatars.md`.
- **Personalities, for the signature animations:** Tobi is adventurous and influential. Amara is nerdy and follows the rules.

## Stage 1: base meshes
- **Built procedurally:** everything is built by Python from joint graphs (`blender/scripts/s1_mesh.py`), so it can be rebuilt any time. Bodies, clothes and shoes come from Blender's Skin modifier plus one subdivision level, which gives clean quad tubes.
- **Head:** a shaped quad-sphere.
- **Meshes per character:** `NAME_body`, `NAME_head`, `NAME_hair`, `NAME_eyes`, `NAME_brows`, `NAME_mouth`, `NAME_outfit` (shirt, trousers and shoes in one mesh with material slots), plus props.
  - Tobi's props: `tobi_bandana`, `tobi_bag` (with strap), `tobi_phone`, `tobi_pin`.
  - Amara's props: `amara_glasses`, `amara_lanyard`, `amara_tablet`, `amara_pin`.
- **Face parts:** brows and mouth are separate small meshes, so the face rig's shape keys stay simple and reusable.
- **Hidden body faces:** body faces that sit fully inside the clothes are deleted. That saves about 1,000 triangles and stops skin poking through when the characters move.
- **Rest pose:** an A-pose with the arms 45 degrees down. It deforms better than a T-pose at the shoulders.
- **Orientation:** characters face -Y with Z up, and their left side is +X (".L").
- **Triangle counts:** Tobi has about 8,100 triangles and Amara about 7,900, close to the bottom of the 8k to 15k target. This is deliberate: it leaves room for the outline shell at render time and keeps the meshes light for web use (.glb).
- **Hair:**
  - Tobi's twists are short six-sided cones on a cap.
  - Amara's braided bun is simplified to a smooth cap plus a bun. Earlier braid bumps read as a crown at this low polygon count, so they were removed.
- **Known minor issue:** at rest, tiny skin slivers can show where Amara's shirt hem meets her trousers at the hips. They aren't visible at normal framing.
- **Skin modifier gotcha:** every separate piece (each shoe, for example) needs its own root vertex, or the modifier silently drops that piece.
- **Material slots gotcha:** material slots must exist on a mesh before writing a bmesh into it. Otherwise Blender clamps every face to slot 0.

## Stage 2: shared rig
- **One rig definition for both characters:** `blender/scripts/s2_rig.py` builds `tobi_rig` and `amara_rig` from each character's own joints, but with identical bone names, hierarchy and rolls. Any Action made on one plays on the other.
- **Bones (61, 52 deform):** `root` → `hips` → `spine_01..03` → `neck` → `head`; per side `shoulder`, `upper_arm`, `forearm`, `hand`, five fingers × 3 (`thumb/index/middle/ring/pinky_01..03`), `thigh`, `shin`, `foot`, `toe`. Controls (no deform): `IK_hand`, `IK_foot`, `pole_elbow`, `pole_knee` (.L/.R), all children of `root`.
- **Root bone for locomotion:** sits on the floor at the character's origin, pointing back (+Y). Walk/run cycles animate in place; moving `root` moves the whole character.
- **IK:** 2-bone IK on forearms and shins, with poles behind the elbows and in front of the knees. Each limb has an FK/IK switch as a custom property on the rig (`ik_arm_L`, `ik_arm_R`, `ik_leg_L`, `ik_leg_R`), driving the IK and hand/foot rotation-copy influence. **Default is FK (0)** so the library Actions are plain bone rotations that export cleanly to .glb/.fbx; IK is for hand-posing in Blender (plants, contacts).
- **Rolls:** every limb, spine and finger bone has its local Z facing forward; feet and toes have Z up. This makes one rotation mean the same thing on both characters.
- **Posing in rig space:** `blender/scripts/posing.py` writes poses as rotations around the rig's X/Y/Z axes and converts them to each bone's local quaternion, with automatic left→right mirroring. All test poses and animations use it.
- **Parenting gotcha:** meshes are reparented from the stage 1 group empty to the rig with an identity parent-inverse; reassigning `matrix_world` before the rig's matrix updates left them offset from the bones.
- **Check:** `blender/renders/stage2/stage2_poses_rig.png` shows rest, arms overhead, deep squat, torso twist and an IK test (bones only; meshes not bound yet). Bones sit inside the meshes and every pose bends the right way.
