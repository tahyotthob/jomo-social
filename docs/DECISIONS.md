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

## Stage 3: skin weights and face rig
- **Scripted weights instead of Blender's bone-heat solver:** `blender/scripts/s3_skin.py` scores every vertex against each bone by distance to the bone minus that bone's typical flesh radius (measured on the body), turns scores into soft weights, smooths them over mesh edges, then keeps the 4 strongest bones and normalises. It gives the same result every run and doesn't fail on the open body mesh (hidden faces were deleted in stage 1), which bone heat can.
- **Max 4 bones per vertex, all normalised:** works in game engines, web viewers and the .glb/.fbx exports. A script check confirms every vertex on every mesh sums to 1.
- **Each part listens only to sensible bones:** the shirt follows torso and arms; trousers follow hips and legs; shoes follow shin, foot and toe; the pin, lanyard and bag follow the torso. That stops a loose tee hem being dragged by the thighs in a squat.
- **Rigid parts:** head, hair, eyes, brows, mouth, glasses and bandana are 100% `head`. Tobi's phone is 100% `hand.R`; Amara's tablet is 100% `hand.L`.
- **Linear skinning, not "preserve volume":** glTF and most engines only support linear blend skinning, so the preview matches what exports. The cost is slight knee and elbow thinning in the deepest bends, which is acceptable at this style.
- **Extreme-pose check:** `blender/renders/stage3/stage3_poses_rig.png` shows arms overhead, deep squat, torso twist and the IK test with the bound meshes. No tearing, no skin through the clothes. Tobi's oversized tee hangs off the back in the squat, which reads as a loose tee.
- **Face rig as shape keys:** on `NAME_eyes`, `NAME_brows` and `NAME_mouth`, with the same names on both characters: `blink`, `blink_L`, `blink_R`, `smile`, `frown`, `open`, `sad`, `surprise`, and the speech shapes `vis_A`, `vis_E`, `vis_O`, `vis_U`, `vis_MBP`, `vis_FV`. Mouth shapes are re-projected onto the face, so they never sink into the chin.
- **One face control per expression:** each shape key is driven by a rig custom property of the same name (0 to 1) on `NAME_rig`. Animations key the rig's properties, so one Action drives body and face on either character. Drivers don't export to glTF/FBX, so stage 6 bakes them into per-mesh shape-key animation.
- **Blink:** the eye squashes to a thin line slightly below centre, like a closed lid. There is no separate eyelid mesh at this poly budget.
- **Known, for stage 4:** Amara's open-mouth shapes are in her lip colour, so they read with low contrast. Stage 4 gives both mouths a dark inner colour.

## Stage 4: UVs, palette atlas, materials
- **Palette atlas, not painted textures:** `blender/textures/jomo_palette.png` is 256×256 px, an 8×8 grid of flat 32 px swatches, one per palette colour, in `common.py` order. Unused cells are magenta so a stray UV shows up immediately. It's tiny, needs no painting, and keeps every colour exactly on brand.
- **One UV map per mesh (`UVMap`), non-overlapping:** each colour's faces are unwrapped on their own (Smart UV Project at 35°, then a minimum-stretch unwrap per island) and packed into that colour's cell, 3 px inside the cell edge so mipmaps don't bleed. The UVs are real unwraps, so the same map can carry a painted or baked texture later.
- **Overlap check:** `blender/scripts/uv_check.py` tests every UV triangle against every other (exact 2D test). The final count is 0 overlapping faces on all 22 meshes. Any face that folds onto another is cut into its own island and unwrapped again; that happened at Tobi's thumb roots, where the Skin modifier pinches the geometry. Layout: `blender/renders/stage4/stage4_uv_layout.png`.
- **Mesh clean-up:** 160 duplicate or zero-area faces from the bandana's solidify step and 13 from the glasses were removed before unwrapping. No visible change.
- **One material per character:** `M_tobi_toon` and `M_amara_toon`, palette texture with nearest-pixel sampling. Each has two outputs:
  - EEVEE: toon (Diffuse → Shader to RGB → two-step ramp × palette).
  - Cycles/export: Principled BSDF, base colour = palette, roughness 1, metallic 0. glTF and FBX carry this one; engines add their own toon shader on top of the palette if wanted.
- **Amara's inner mouth:** the middle 70% of her mouth is now the dark mouth colour, with her lip colour at the corners, so open-mouth and speech shapes read clearly (flagged in stage 3).
- **Check:** `blender/renders/stage4/stage4_turntable.png` and `stage4_poses_body.png` match the stage 1–3 colours exactly (the palette reproduces the swatches), with no magenta anywhere.

## Stage 5: animation library
- **17 Actions, 24 fps, all in `blender/work/stage5.blend` (and the final export):**

  | Action | Frames | Loop |
  |---|---|---|
  | `idle` | 96 | loop |
  | `walk` | 32 | loop |
  | `run` | 20 | loop |
  | `jump` | 44 | one-shot |
  | `wave` | 56 | one-shot |
  | `talk` | 96 | loop, with speech mouth shapes |
  | `celebrate` | 64 | one-shot |
  | `sit_down` | 48 | one-shot |
  | `stand_up` | 48 | one-shot |
  | `point` | 44 | one-shot |
  | `clap` | 36 | loop |
  | `dance` | 48 | loop, 120 bpm, 4 beats |
  | `react_surprise` | 48 | one-shot |
  | `react_sad` | 60 | one-shot |
  | `react_laugh` | 54 | one-shot |
  | `tobi_selfie_hype` | 84 | Tobi's signature |
  | `amara_fact_check` | 96 | Amara's signature |

- **Signature animations, from the personas:**
  - **Tobi, adventurous and influential:** `tobi_selfie_hype` raises his phone for a selfie, leans in, throws a peace sign and winks.
  - **Amara, nerdy rule-follower:** `amara_fact_check` lifts her tablet, pushes her glasses up with her index finger, reads, nods "verified" twice and taps the screen.
- **One Action, both characters:** every Action keys pose bones by name, plus the rig's face properties. Both rigs come from the same code with the same rolls, so the same keys play on either. The previews show both characters playing each Action side by side.
- **Authored on Tobi:** contact poses (clap, hand on belly, peace sign, selfie) are solved on Tobi's rig. On Amara the contacts land within a few centimetres; the measured distance between her palms in `clap` is 3.7 cm.
- **Contacts solved, not eyeballed:** a small Nelder–Mead solver (`posing.reach`) finds the 7 arm angles that put a hand or fingertip on a target, optionally with the palm facing a set direction. Amara's signature is solved on her own rig: the finger target is measured from her glasses' bridge, and the tap target is measured from the tablet screen as she holds it.
- **FK keys only:** IK is off (0) in every Action. The library is plain bone rotations, which export to glTF and FBX exactly, with no constraint baking.
- **Locomotion in place:** `walk` and `run` don't move the root bone; a game or web player moves the character. The intended speed is stored on the Action as `root_speed_m_s` (walk 1.3 m/s, run 3.6 m/s). Feet can slide slightly at other speeds.
- **Loops:** loops have identical first and last keys; their frame range stops one frame before the last key, and they're flagged `use_cyclic`. Each Action also stores `fps`, `loop` and `frames` as custom properties.
- **Hips translations are in metres (Tobi):** used for jumps, sitting and bounce. On Amara, who is 8% shorter, they read the same. Sitting drops the hips 0.40 m and back 0.40 m, about one thigh length, so the feet stay put.
- **Faces in Actions:** expressions and speech shapes are keyed on the rig's face properties (`smile`, `vis_A` and so on). They're baked to shape-key animation at export (stage 6).
- **Previews:** `blender/scripts/preview_anim.py` writes a key-frame contact sheet per Action (`blender/renders/stage5/anim_*.png`) and an MP4 per Action (`blender/export/previews/*.mp4`). Loops play three times; one-shots hold the last frame for half a second. Sitting Actions show a stool so the pose reads. The camera is a 3/4 view, so the arm nearest the lens looks foreshortened; front and side views were also checked.
- **Props on borrowed signatures:** props stay with their own character. When Amara plays `tobi_selfie_hype`, her tablet hand rises and the tablet passes near her head; when Tobi plays `amara_fact_check`, he "reads" his phone. That's expected: each signature is designed for its owner's props.

## Stage 6: export
- **Files:**
  - `blender/export/jomo_characters.blend`: both characters, rigs, face drivers, all 17 Actions, and the palette packed in.
  - `blender/export/tobi.glb` / `amara.glb` and `tobi.fbx` / `amara.fbx`: one character per file, centred at the origin.
  - `blender/export/previews/*.mp4`: one per Action.
- **Bones exported:** deform bones plus `root`, 53 in total. `root` is now flagged deform so engines get a locomotion root. IK and pole controls are Blender-only and stay out of the exports.
- **Animations in the exports:** each Action becomes an NLA track. glTF exports by track name; FBX exports one take per strip.
- **Face animation in the exports:** the rig's face-property curves are copied onto each face mesh's shape keys as NLA tracks with the same names, and the face drivers are removed in the export copy. The exporters then merge body and face into one clip per animation.
- **Export material:** exports carry the Principled/palette output. The EEVEE toon output stays in the .blend only, because exporters can't read Shader-to-RGB.
- **Round-trip check (`blender/scripts/verify_export.py`):** re-imports both .glb files into an empty scene and checks bones (53), meshes (11), triangles, shape keys and all 17 animations. It then renders `blender/renders/stage6/stage6_turntable.png` and `stage6_poses_from_glb.png` from the imported files.
  - A hand position after round-trip matched the source to the millimetre.
  - Morph weights play back: `celebrate` frame 15 gives `smile` 1.0 and `open` 0.75.
- **FBX check:** re-imported FBX has 53 bones, 11 meshes, shape keys on the 3 face meshes, and 17 body takes plus their face takes.
- **Importer quirk, not a file problem:** Blender's glTF importer adds an empty above each mesh that has animated morph weights, and an `Icosphere` it uses to display bones.
- **Head resolution raised after the first export check:** the clean-up in stage 4 left Tobi at 7,752 and Amara at 7,828 triangles, just under the 8k–15k target. The head quad-sphere went from 7 to 9 cuts, which also smooths the skull silhouette. Everything was rebuilt from the scripts (`blender/scripts/build_all.sh`): Tobi is now **8,652** and Amara **8,720** triangles, with 0 overlapping UVs. The stage 1–2 check sheets show the earlier head; stage 3, 5 and 6 sheets and all MP4s were re-rendered on the final meshes.
- **One-command rebuild:** `bash blender/scripts/build_all.sh` rebuilds stages 1–6, re-checks UVs and the exports, and re-renders the animation sheets and MP4s. Add `--no-previews` to skip the renders.
