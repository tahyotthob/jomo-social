# Tobi and Amara puppet kit

These layered parts let the motion-graphics tool animate the characters: talk, blink, breathe, sway and lean. AI characters, so follow `references/avatars.md` and safety checklist item 8.

| File | What it is |
|---|---|
| `tobi-body.png`, `amara-body.png` | Full figure, transparent background, 1080x1440 frame |
| `tobi-closed-patch.png` | Tobi's lips closed (his base face is an open grin) |
| `tobi-mouth-patch.png`, `amara-mouth-patch.png` | Mouth wide open |
| `tobi-eyes-patch.png`, `amara-eyes-patch.png` | Both eyes closed, for blinks (Tobi's left lid is drawn in code because Canva only produced a wink) |
| `src/` | The full-size Canva originals the patches are cut from (variants of media MAHY9JnuNlQ and MAHY9JCjN-k, exported from the Canva design "JOMO avatars – export sheet") |

Rebuild the patches: `python3 tools/video/avatar/make_parts.py` (regions in `tools/video/avatar/parts.json`).

Make a reel:
1. Write the lines (`tools/video/avatar/lines-*.json`).
2. Make the voices: `python3 tools/video/avatar/tts.py lines.json voices/`. This needs `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` as environment secrets. Tobi uses en-NG-AbeoNeural and Amara uses en-NG-EzinneNeural.
3. Render: `python3 tools/video/avatar/reel.py lines.json voices/ out.mp4`. Mouths follow the audio's loudness. With no voice files it renders a silent test with estimated timing.

## Blender bone rig (full animation)

`tools/video/avatar/blender/rig.py` turns each character into a fine mesh with bones: hips, spine, head, and both arms (upper arm and forearm). The bones bend the drawing smoothly, so heads nod and tilt, arms gesture and the torso leans, with no tearing. The mouth and blink patches above are mixed into the same material, so talking and blinking still work.

- **Joints and weights:** the `CHARS` table in `rig.py` (pixel positions measured on the cut-outs).
- **Gestures:**
  - Tobi: `point`, `wave`, `surprise`, `nod`.
  - Amara: `finger`, `tap`, `nod`.
  - Set them per line in the lines file, e.g. `"gestures": {"tobi": "wave", "amara": "nod"}`.
- **Automatic motion:** breathing, sway, leaning in while speaking, and small nods on stressed syllables.
- **Render a reel with Blender characters:** `python3 tools/video/avatar/reel.py lines.json voices/ out.mp4 --blender` (needs `pip install bpy`).
  - It renders with Cycles on the CPU, at about half a second per character frame at 640 px, so a 30-second reel takes roughly 15 to 20 minutes here.
  - A rented AWS graphics machine would only be needed to go much faster.
