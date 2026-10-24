# JOMO 3D characters: Tobi and Amara

A reusable, rigged and animated 3D set of JOMO's two avatars, built entirely by Python scripts in Blender. Only free tools are used: Blender, Python, Pillow and ffmpeg. There are no add-ons.

- **Style:** stylised low-poly with a flat palette texture and toon shading.
- **Scale:** real-world, in metres. Tobi is 1.80 m and Amara 1.66 m.
- **Characters:** both follow the personas in `references/avatars.md` and the approved 2D character sheets in `assets/avatars/`.

Why things are the way they are is logged in [`docs/DECISIONS.md`](../docs/DECISIONS.md).

## What's here

| File | What it is |
|---|---|
| `export/jomo_characters.blend` | Both characters, rigs, face rig and all 17 Actions. The palette texture is packed in. |
| `export/tobi.glb`, `export/amara.glb` | One file per character, centred at the origin: meshes, skin, shape keys and all 17 animations. For web viewers, three.js, Babylon, Godot. |
| `export/tobi.fbx`, `export/amara.fbx` | The same content as FBX, for Unity, Unreal and most DCC tools. |
| `export/previews/*.mp4` | One preview per animation, with both characters side by side. |
| `textures/jomo_palette.png` | 256 px palette atlas: one 32 px swatch per brand colour. |
| `renders/stageN/` | The check sheets rendered after each stage: turntables, pose sheets, UV layout, animation contact sheets. |
| `scripts/` | Everything that builds the set (see "Rebuilding"). |

### Characters

| | Tobi | Amara |
|---|---|---|
| Role | Adventurous, influential friend who makes things happen (24, male) | Nerdy fact-checker who follows the rules (23, female) |
| Height and build | 1.80 m, slim-athletic, broader shoulders | 1.66 m, slim, narrower shoulders |
| Skin and hair | #5A3820; short twists | #8B5A3C; low bun |
| Outfit | Oversized Leaf Lime tee, charcoal joggers, white sneakers, lime bandana | Off-white shirt over a dark tee, olive trousers, dark flats, round glasses |
| Props | Phone (right hand), crossbody bag, leaf pin | Tablet (left hand), lime lanyard, leaf pin |
| Signature colour | Leaf Lime #A5CD39 | Off-white #F4F6EC with Olive #77962A |
| Triangles | 8,652 | 8,720 |

**Mesh names:**
- **Per character:** `NAME_body`, `NAME_head`, `NAME_hair`, `NAME_eyes`, `NAME_brows`, `NAME_mouth`, `NAME_outfit` (shirt, trousers and shoes), `NAME_pin`.
- **Tobi's props:** `tobi_bandana`, `tobi_bag`, `tobi_phone`.
- **Amara's props:** `amara_glasses`, `amara_lanyard`, `amara_tablet`.

Each character has one material, `M_NAME_toon`, which uses the palette texture.

## The shared rig

Both rigs (`tobi_rig`, `amara_rig`) have the same bone names, hierarchy and bone rolls. Any animation made for one plays on the other.

**Rest pose and orientation:**
- The rest pose is an A-pose, with the arms 45° down.
- Characters face -Y in Blender (+Z forward in glTF) with Z up.
- `.L` is the character's left side.

### Bones (53 deform + 8 controls)

| Bone | Parent | Notes |
|---|---|---|
| `root` | none | On the floor. Move it to move the whole character (locomotion). Exported. |
| `hips` | `root` | Pelvis. Carries the body's up/down and sway. |
| `spine_01`, `spine_02`, `spine_03` | chain from `hips` | |
| `neck` → `head` | `spine_03` | Head, hair, face parts, glasses and bandana are rigid to `head`. |
| `shoulder.L/.R` | `spine_03` | Clavicles. |
| `upper_arm.L/.R` → `forearm.L/.R` → `hand.L/.R` | `shoulder` | The phone is rigid to `hand.R`; the tablet is rigid to `hand.L`. |
| `thumb_01..03`, `index_01..03`, `middle_01..03`, `ring_01..03`, `pinky_01..03` (`.L/.R`) | `hand` | Three bones per finger. |
| `thigh.L/.R` → `shin.L/.R` → `foot.L/.R` → `toe.L/.R` | `hips` | |
| `IK_hand.L/.R`, `IK_foot.L/.R` | `root` | IK targets (Blender only, not exported). |
| `pole_elbow.L/.R`, `pole_knee.L/.R` | `root` | IK pole targets (Blender only). |

**IK in Blender:** set the rig's custom properties `ik_arm_L`, `ik_arm_R`, `ik_leg_L` or `ik_leg_R` to 1, then move the `IK_*` bones. At 0 (the default) the limb is FK. All library animations are FK, so they export exactly.

**Skinning:** at most 4 bones per vertex, normalised. That works in every engine.

### Face rig

The face rig is made of shape keys on `NAME_eyes`, `NAME_brows` and `NAME_mouth`. The names are the same on both characters:

| Shape key | Meshes it's on |
|---|---|
| `blink`, `blink_L`, `blink_R` | eyes (plus a small brow drop on `blink`) |
| `smile`, `sad`, `surprise` | eyes, brows, mouth |
| `frown` | brows, mouth |
| `open` | mouth |
| `vis_A`, `vis_E`, `vis_O`, `vis_U`, `vis_MBP`, `vis_FV` | mouth (speech shapes) |

**In Blender:** each shape key is driven by a custom property of the same name on `NAME_rig`, from 0 to 1. Key the rig, not the meshes: one Action then animates body and face together.

**In the .glb and .fbx:** the face animation is baked onto the meshes' morph targets, per animation.

## Animation library (24 fps)

| Action | Frames | Loop | Notes |
|---|---|---|---|
| `idle` | 96 | yes | Breathing, small weight shift, one blink |
| `walk` | 32 | yes | In place. Intended speed 1.3 m/s (`root_speed_m_s` on the Action) |
| `run` | 20 | yes | In place. Intended speed 3.6 m/s |
| `jump` | 44 | no | Anticipation, take-off, tuck, landing |
| `wave` | 56 | no | Right hand |
| `talk` | 96 | yes | Hand gestures, nods and speech mouth shapes |
| `celebrate` | 64 | no | Fists up, pumps, laugh |
| `sit_down` | 48 | no | Seat height is about hip height minus 0.47 m |
| `stand_up` | 48 | no | `sit_down` reversed |
| `point` | 44 | no | Right index finger, forward |
| `clap` | 36 | yes | Four claps per loop |
| `dance` | 48 | yes | Afrobeats-style bounce, 120 bpm, 4 beats |
| `react_surprise` | 48 | no | |
| `react_sad` | 60 | no | |
| `react_laugh` | 54 | no | Hand on belly, shoulders bouncing |
| `tobi_selfie_hype` | 84 | no | **Tobi's signature:** phone up for a selfie, lean in, peace sign, wink |
| `amara_fact_check` | 96 | no | **Amara's signature:** tablet up, pushes glasses up, reads, nods "verified", taps the screen |

**Loops:** looping Actions have matching first and last keys, and their frame range stops one frame early, so they wrap seamlessly. Each Action carries the custom properties `fps`, `frames` and `loop`.

**Previews:** `export/previews/<action>.mp4`.

## Applying an animation to a different character

**In Blender:** every Action keys bones by name, so any rig built by `scripts/s2_rig.py` can play any Action.

1. Select the rig (`amara_rig`, for example). In the Dope Sheet, open the **Action Editor** and pick the Action, such as `tobi_selfie_hype`.
2. If Blender asks for a slot, pick the Action's only slot. Each Action has one slot. Blender 4.4 and later use slots.
3. To layer or sequence Actions, push them to NLA strips (Action Editor → Push Down) and arrange them in the NLA editor.

The same steps in Python:

```python
import bpy
rig = bpy.data.objects["amara_rig"]
act = bpy.data.actions["tobi_selfie_hype"]
rig.animation_data_create()
rig.animation_data.action = act
rig.animation_data.action_slot = act.slots[0]
```

**In a game engine or on the web:**
- **Both glTF files** contain all 17 animations. The bone names match exactly, so a clip from `tobi.glb` plays on Amara's skeleton without retargeting.
  - three.js: `mixer.clipAction(clip, amaraScene)`.
  - Godot: the AnimationPlayer's tracks resolve by bone name.
- **Unity:** import the FBX as a Humanoid rig and the clips retarget automatically. Map `hips`, `spine_01..03`, `neck`, `head`, `shoulder`, `upper_arm`, `forearm`, `hand`, the fingers, `thigh`, `shin`, `foot` and `toe`.
- **Unreal:** both skeletons have identical hierarchies, so use one Skeleton asset for both. Otherwise, retarget with an IK Retargeter.
- **Translations:** hips translations (jumps, sitting, bounce) are authored in metres on Tobi. On Amara (8% shorter) they look right; for a much smaller or larger character, scale the root/hips translation curves by the ratio of hip heights.

**For a brand-new character:**
1. Add an entry to `CHARS` in `scripts/common.py` (height, proportions, head size, colours).
2. Model it in `s1_mesh.py`.
3. Re-run the stages. The rig, weights, face rig and every Action follow automatically.

## Rebuilding

Every step is a script that can be re-run on its own. It needs Blender as a Python module (`pip install bpy`, Blender 4.4 or later) plus Pillow, numpy and ffmpeg.

```bash
python3 blender/scripts/s1_mesh.py          # stage 1: meshes and proportions  -> work/stage1.blend
python3 blender/scripts/s2_rig.py           # stage 2: shared rig              -> work/stage2.blend
python3 blender/scripts/s3_skin.py          # stage 3: weights + face rig      -> work/stage3.blend
python3 blender/scripts/s4_materials.py     # stage 4: UVs, palette, materials -> work/stage4.blend
python3 blender/scripts/s5_animations.py    # stage 5: animation library       -> work/stage5.blend
python3 blender/scripts/s6_export.py        # stage 6: .blend, .glb, .fbx      -> export/
python3 blender/scripts/verify_export.py    # re-import the .glb files, count everything, render stage6 checks
# or all of the above plus previews in one go: bash blender/scripts/build_all.sh

# checks
python3 blender/scripts/preview.py blender/work/stage5.blend stage5 all          # turntable + pose sheets
python3 blender/scripts/preview.py blender/work/stage3.blend stage3 rigdeformed  # extreme poses + face rig
python3 blender/scripts/uv_check.py blender/work/stage4.blend stage4             # UV layout + overlap count
python3 blender/scripts/preview_anim.py blender/work/stage5.blend sheet          # animation contact sheets
python3 blender/scripts/preview_anim.py blender/work/stage5.blend mp4            # preview MP4s
```

Notes on the scripts:
- `blender/work/` holds the intermediate files and is not committed.
- Previews render with Cycles on the CPU. EEVEE needs a GPU, which headless servers often don't have.
- `scripts/posing.py` holds the posing helpers and the small reach solver used for contact poses (clap, hand on belly, glasses push).

## Using the characters for JOMO posts

These are JOMO's AI avatars. The labelling rules in `references/safety-checklist.md` (item 8) and `references/avatars.md` apply to every post that uses them. Never present them as real JOMO people, activity or results.
