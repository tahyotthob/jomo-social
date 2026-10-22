# YCEF videos: build notes (2026-10-22)

Built with `tools/video/ycef_videos.py`. All four files are 1080x1920, 25 fps, H.264 with AAC audio, and nothing has been published or scheduled.

| File | Length | Audio |
|---|---|---|
| `video-a-ycef-promo.mp4` | 14.8 s | Team-made music bed, -14 LUFS |
| `video-a-ycef-promo-no-music.mp4` | 14.8 s | Silent, for adding Meta Sound Collection music in the app, or for LinkedIn and X |
| `video-b-ycef-ai-avatar.mp4` | 15.0 s | Avatar voice plus team-made bed, ducked under the voice, -14 LUFS |
| `video-b-ycef-ai-avatar-voice-only.mp4` | 15.0 s | Avatar voice only, -16 LUFS |
| `video-b-ycef-ai-avatar.srt` | | Captions file for Facebook and LinkedIn uploads |
| `cover-video-a.jpg`, `cover-video-b.jpg` | | Reel covers: the gully frame with its label, and the "50 fellows" card |

Stills for review are in `stills/`: `a-0.5.jpg`, `a-1.6.jpg`, `a-3.8.jpg`, `a-6.6.jpg`, `a-8.9.jpg`, `a-12.0.jpg`, `b-1.0.jpg`, `b-2.6.jpg`, `b-4.2.jpg`, `b-6.2.jpg`, `b-8.4.jpg`, `b-9.95.jpg`, `b-12.5.jpg`, plus `a-contact-sheet.png` and `b-contact-sheet.png` (a frame every 0.5 s with timecodes).

## Video A timeline

| Time | Picture | On screen |
|---|---|---|
| 0.00–2.96 | AI gully and plastic waste (source 0.88–2.92 s, slowed 1.5x). No identifiable people; the only figures are tiny ones on the ridge. | Pill "AI-generated visuals". An edge-to-edge Ink band covers the text CapCut burned in, carrying "YCEF 2026" and "Your street has a climate problem." |
| 2.96–5.56 | Real photo, slow push-in: `oniwaya-cleanup-11.jpg` (consent row in `content/consent-log.csv`). Volunteer in a JOMO vest, face hidden, clearing a drain; the photo's own 2020 "World Clean Up Day" badge sits at the bottom. | Pill "Real photo · JOMO archive". Lower band: "You've got the fix." and "Real JOMO volunteers clearing a drain, Oniwaya clean-up" |
| 5.56–7.46 | Lime card | "Young Climate Educators Fellowship" / "50 fellows" / "Nigeria + Zambia" |
| 7.46–10.16 | Ink card | "3 virtual weekends" / "Starts Fri 13 Nov 2026" / "For university students and grassroots community volunteers, aged 18+" |
| 10.16–14.76 | End card | Logo / "Young Climate Educators Fellowship" / "Applications close" / "Mon 26 Oct" / "Apply now" / "jomoclimatechange.org/events?apply=ycef" / "The opening scene is AI-generated, not a real place or JOMO event. The clean-up photo is real." / @jomoclimatechange |

## Video B timeline

| Time | Picture | Voice | On screen |
|---|---|---|---|
| 0.00–3.40 | Avatar (source 0.28–3.68 s) | "Climate action training programme for young people in Nigeria and Zambia." | Pill "AI avatar". Captions in an Ink band. Lower third: "YCEF 2026" / "Young Climate Educators Fellowship" / "For ages 18+: university students and grassroots community volunteers" |
| 3.40–5.25 | Lime card | "Selecting 50 fellows." (source 4.61–5.78 s) | "YCEF 2026" / "Selecting" / "50 fellows" / "across Nigeria + Zambia" |
| 5.25–7.15 | Ink card | none | "3" / "virtual weekends" / "Starts Fri 13 Nov 2026" |
| 7.15–9.70 | Off-white card | none | "What fellows do" / "Research a local climate problem." / "Design a youth-led fix." / "Learn to pitch for seed funding." / "No funding guarantee." |
| 9.70–10.34 | Avatar (source 8.52–9.16 s) | "Apply now." | Caption "Apply now." on an Ink band that covers CapCut's garbled caption (y 1095–1190) |
| 10.34–14.94 | End card | none | As Video A, with the disclosure "The presenter is an AI avatar, not a JOMO team member." |

The "AI avatar" pill stays on from the first frame until the end card, including over the cards.

## Checks run on the finished files

- **Speech-to-text (Whisper small) on both Video B files** hears exactly: "Climate Action Training Program for young people in Nigeria and Zambia." / "Selecting 50 fellows." / "Apply now." It picks up no other words: none of the wrong dates, the garbled words or the wrong web address.
- **CapCut background music:**
  - The source avatar audio had a quiet music pad under her voice: steady tones at 211, 328 and 656 Hz in every pause.
  - The voice was separated with Demucs (`tools/video/separate_voice.py`), and a narrow notch at 1758 Hz removed one tone that remained.
  - Afterwards the pauses show no tonal peaks (spectral flatness 0.40–0.46, which is noise-like).
  - Video A uses none of its source audio.
- **Team-made bed** (`tools/video/music_bed.py`):
  - Written from scratch in code: synthesised pads, plucked notes, bass and drums.
  - It uses no samples, loops or AI music tools, and JOMO owns it outright.
  - It does not clip.
  - Its frequency balance is close to the original CapCut track's.
- **Loudness:** -14.0 LUFS (A) and -14.2 LUFS (B), with true peaks under -0.9 dBFS.
- **"CapCut AI" mark:** visible top left on every CapCut frame. Frames are trimmed at the bottom only, and the pills sit at y 268, below the mark.
- **Frame checks at full size:**
  - No burned-in CapCut text shows on any frame.
  - No orphan words.
  - All text stays between y 268 and 1640, with key content inside the 4:5 crop. The exceptions are the photo's own 2020 badge and the pill, which sit in the top and bottom reel margins.
- **Not checkable here:** how the music sounds to a listener (no one has played it), and whether the link opens (the site serves a JavaScript shell).

## Still open (operator)

1. Does https://jomoclimatechange.org/events?apply=ycef open the YCEF application on a phone, including in Instagram's browser? Does the Instagram bio link point there?
2. Is the handle @jomoclimatechange (as printed) or @jomoclimate?
3. What is the closing time on Mon 26 Oct? It is not shown; add it to the captions if known.
4. CapCut:
   - Were the avatar and the clips made from prompts only?
   - Is the avatar a stock CapCut avatar with a stock voice?
   - Did the materials carry CapCut's "Commercial use" mark?
   - Is there a sharper original export of the avatar video (the WhatsApp copy is 356x640)?
5. Music: approve the team-made bed as an exception to checklist item 9, or post the no-music versions and add Meta Sound Collection music in the app (Instagram and Facebook only).
