# YCEF remakes: Video A (promo reel) and Video B (AI avatar explainer)

**Role: Video Producer** · 2026-10-22 · Status: Drafting. Next: Fact-checker, then Policy and Safety Review, then operator sign-off. Nothing here is approved, scheduled or published.

Inputs: `source-review.md` (usable footage and timings), `references/brand-guide.md` (every programme fact), the operator's brief of 2026-10-22 (deadline Mon 26 Oct 2026, closing time [TIME], Weekend 1 Fri 13 Nov 2026, link, never promise funding), `references/safety-checklist.md` item 8.

## As built (2026-10-22)

The videos were built with `tools/video/ycef_videos.py`. The build differs from the scripts below in five ways, after the Fact-checker's and the Policy and Safety Reviewer's findings and a full-size frame check.

1. **The planting shot is out of Video A.** At full size:
   - The man in the beige T-shirt wears an AI-invented crest.
   - The person at the left edge in the first frames (7.04–7.2 s) wears the crested school-style uniform.
   - Two of the planters could pass for under-18s.

   "You've got the fix." now runs over a real JOMO photo instead: `assets/photos/events/oniwaya-cleanup/oniwaya-cleanup-11.jpg`. It is consent-logged, shows a volunteer whose face is hidden clearing a drain, and carries the label "Real photo · JOMO archive".
2. **Programme facts sit only on brand cards, never over AI people.** Video A: "50 fellows · Nigeria + Zambia", then "3 virtual weekends · Starts Fri 13 Nov 2026 · university students and grassroots community volunteers, 18+".
3. **The gully shot is cut inside the dissolves.** It runs from source 0.88 s to 2.92 s, slowed 1.5x: after the man has fully gone and before the sketchbook fades in.
4. **The "CapCut AI" mark is never cropped or covered.** Frames are scaled to full width and trimmed at the bottom only, and the label pills sit at y 300, below the mark.
5. **Video B uses only the avatar's three accurate lines**, taken from her voice with the CapCut background music removed (`tools/video/separate_voice.py`, Demucs).

   | Line | Source time | On screen |
   |---|---|---|
   | "Climate action training programme for young people in Nigeria and Zambia" | 0.28–3.70 s | Avatar |
   | "Selecting 50 fellows" | 4.61–5.78 s | Lime card |
   | "Apply now" | 8.52–9.16 s | Avatar |

   A speech-to-text check of the finished audio hears exactly those words, and nothing from the wrong dates, the garbled words or the wrong web address. The "AI avatar" label stays on from the first frame until the end card. The caption band covers the garbled caption CapCut burned into the "Apply now" shot, at y 1095–1190.

Each video comes in two versions:
- **With the team-made music bed** (`tools/video/music_bed.py`: written from scratch in code, with no samples, loops or AI music tools). This version needs the operator's exception to checklist item 9.
- **Without music**, for adding Meta Sound Collection music in the Instagram or Facebook app, and for LinkedIn and X.

## At a glance

| | Video A: promo reel | Video B: AI avatar explainer |
|---|---|---|
| Length | 14.08 s, 1080x1920, no voice | 13.68 s, 1080x1920 |
| Hook (first 2 s) | "Your street has a climate problem." over the polluted gully, on screen from the first frame | Her face to camera from the first frame; "Climate action" in Lime, then the call-out "for young people in Nigeria and Zambia" at 1.40 s |
| One idea | You've got the fix: YCEF helps you research it, design it and learn to pitch it | What YCEF is, in her words plus three cards |
| Ask | End card: Apply by Mon 26 Oct 2026 + link | She says "Apply now." straight into the end card: Apply by Mon 26 Oct 2026 + link |
| AI label | AI-GENERATED VISUALS, inside the panel, over all footage | AI AVATAR, in the caption band, whenever she is seen or heard |

## Settle before export (each of these is burned into the video)

1. **[TIME]:** fill in the closing time on both end cards (and replace "WAT" if the deadline is set in another zone), or delete the "Applications close at [TIME] WAT" line. Never export the placeholder. Zambian applicants are an hour ahead (CAT), so consider giving both times.
2. **Link:** https://jomoclimatechange.org/events?apply=ycef is not yet confirmed to load. Type exactly what the end card shows into a phone browser before export.
3. **Handle:** @jomoclimatechange or @jomoclimate (operator confirming).
4. **CapCut plan:** confirm its terms allow organisational use, and whether it allows export without the "CapCut AI" mark (this decides the 4:5 crop, section 5).
5. **Video B source audio:** listen on headphones. If any music sits under her voice, it is library music with an unknown licence: flag it and don't use the clips.

## Build specs (both videos)

- **Canvas:** 1080x1920 at 25 fps (the source frame rate), highest export quality. Times sit on the 25 fps grid (0.04 s a frame), which is why Video A's panels run 1.52 s: none is shorter than 1.5 s.
- **Safe area:** all text sits between y 300 and y 1600. That keeps it out of the top and bottom 250 px and inside the centred 4:5 crop (y 285–1635), so the feed version needs no new layout. Text is left-aligned at x 90, as in the flyer builder. Below y 1100, keep lines left of x 960, clear of the Like/Comment/Share buttons.
- **Colours:** Ink #1E2220, Lime #A5CD39, Off-white #F4F6EC. Lime and Off-white text on Ink; Ink text on Lime.
- **Type:**
  - Headlines: Bricolage Grotesque ExtraBold in sentence case, as on the existing YCEF slides in `tools/build.py`.
  - Labels: Lato Black capitals with wide letter spacing (0.22 em).
  - Captions and body text: Lato Bold.
  - Both families are free on Google Fonts. Tell the operator if CapCut forces a substitute.
  - The point sizes below are starting points. The rule is that the longest line fits between x 90 and x 990, checked at full size.
- **AI footage:** scale to 1080 wide and align to the top. That keeps the "CapCut AI" mark at top left whole (checklist item 8: never remove a tool's watermark) and lets the extra 20–24 px fall off the bottom.
- **Panels and bands:** solid Ink at 100% opacity, full width. They never move or fade while footage is under them; only the text inside changes, on a cut.
- **Cards:** build them in CapCut, or render them with the flyer builder (`tools/`: file names containing `9x16` give 1080x1920 PNGs). The builder puts its footer in the bottom 120 px and starts its padding at y 90, so move both inside the safe area.
- **Logo:** `assets/logos/jomo-logo-light.png` on Ink. The brand guide's path, `assets/jomo-logo-light.png`, doesn't exist. Leave clear space at least the height of the "J".

## 1. Video A: promo reel (14.08 s, no voice)

**Why 14.08 s:** the two usable shots, slowed down, give 7.56 s. With a 5 s end card that is 12.56 s, under the 13 s minimum. So a 1.52 s Lime card between the shots carries the second half of the campaign line and brings the total to 14.08 s.

### Clip prep

| Clip | Source in–out | Speed | Timeline |
|---|---|---|---|
| A1 gully | In: 1.00 (check no trace of the young man remains).<br>Out: the last clean frame before the sketchbook fades in, somewhere between 2.5 and 3.0 s (step through it). | About 0.6x, stretched to fill 3.00 s | 0.00–3.00 |
| A2 planting | In: 7.00 (the first frame with no trace of the girls' shot).<br>Out: 10.00.<br>The clip cuts from close to wide at source 9.00. | 0.66x, stretched to 4.56 s | 4.52–9.08 |

- Mute the source audio (CapCut library track, licence unknown).
- Smooth slow-motion (optical flow) is optional. Switch it off if hands, plastic or leaves warp.
- Nothing else from the source is used:
  - 0.0–1.0: the crested uniform.
  - 3.0–7.0: people who look under 18, and the garbled face.
- At full size, check the planting shot for lettering or a logo on clothing (the man on the left has a chest print). If it reads as text or a brand, tell the operator.
- No speech, so no subtitle file: every word is on screen.

### Panel over footage

- **Panel:** Ink, x 0–1080, y 760–1240, which sits inside the middle third (y 640–1280).
  - From the contact sheet, the burned-in text sits at about y 830–1190 at this scale, which leaves 50–70 px to spare.
  - Step through every frame at full size. If any letter shows, grow the panel toward y 640–1280.
- **Label row:** **AI-GENERATED VISUALS**, Lato Black caps 30 px, Lime, at x 90, top of the panel (about y 795). It is part of every panel, so it is on screen whenever AI footage is.
- **Headline:** Bricolage, Off-white, at x 90, centred vertically in the space under the label.

### Edit table

| Time (s) | Picture | Exact on-screen text | Audio |
|---|---|---|---|
| 0.00–3.00 | A1: polluted gully and stream with plastic waste, no identifiable people; Ink panel across the middle | **AI-GENERATED VISUALS**<br>**Your street has**<br>**a climate problem.**<br>(about 88 px; second line in Lime; on screen from the first frame, no fade) | Music bed from the first frame; no voice |
| 3.00–4.52 | Lime card, full frame. Optional: the two-leaf sprout in Off-white and Leaf Green, large and cropped at lower right, clear of the text (as on `li-02` in `tools/build.py`) | **You've got**<br>**the fix.**<br>(Ink, about 150 px, x 90, in the middle third) | Music; if the track has a drop, land it on this cut |
| 4.52–6.04 | A2 close shot (source 7.0–8.0), panel | **AI-GENERATED VISUALS**<br>**Research it.**<br>(about 130 px) | Music |
| 6.04–7.56 | A2 close shot (source 8.0–9.0), panel | **AI-GENERATED VISUALS**<br>**Design it.** | Music |
| 7.56–9.08 | A2 wide shot (source 9.0–10.0), panel | **AI-GENERATED VISUALS**<br>**Learn to**<br>**pitch it.**<br>("pitch it." in Lime) | Music |
| 9.08–14.08 | End card A on Ink (below) | End card A text (below) | Music; fade out 13.58–14.08 |

### End card A (9.08–14.08, Ink, static)

```
[JOMO logo, light version]
YOUNG CLIMATE EDUCATORS
FELLOWSHIP (YCEF)
Apply by
Mon 26 Oct 2026
Applications close at [TIME] WAT
3 virtual weekends · 50 fellows
Nigeria + Zambia · aged 18+
jomoclimatechange.org/events?apply=ycef
[Instagram icon] [LinkedIn icon] @jomoclimatechange
```

| Element | Style | y position |
|---|---|---|
| Logo | Light version, 400 px wide | from 360 |
| YOUNG CLIMATE EDUCATORS / FELLOWSHIP (YCEF) | Lato Black caps 30 px, Lime | 620–700 |
| Apply by / Mon 26 Oct 2026 | Bricolage, about 100 px; line 1 Off-white, line 2 Lime | 740–930 |
| Applications close at [TIME] WAT | Lato Bold 40 px, Off-white | about 965 |
| The two fact lines | Lato Regular 40 px, Off-white | 1070–1180 |
| Link | Lato Bold 38 px, Off-white | about 1260 |
| Handle bar | Icons and handle as in the flyer builder's footer (Lato Bold 30 px, thin rule above) | 1500–1580 |

There is no build-up animation, so all 5 s are reading time.

## 2. Video B: AI avatar explainer (13.68 s)

### Clip prep

| Clip | Source in–out | Use | Timeline |
|---|---|---|---|
| B1 | About 0.18–3.66: start exactly where "climate" begins (nothing of the garbled first word) and end after "Zambia" | Picture and voice | 0.00–3.48 |
| B2 | 4.52–5.66, "selecting 50 fellows" (nothing of the garbled word before it) | Voice only; picture discarded | 3.68–4.82 |
| B3 | 8.44–9.04, "Apply now". Stop before "jomoclimatechange.org" at 9.18, and check the first frames for any ghost of the glass board. | Picture and voice | 9.08–9.68 |

- Mute the source everywhere else, and put a 2-frame audio fade on every cut.
- The clips are 356x640, scaled about 303% (top-aligned), so they will look soft.
  - If the operator still has the CapCut project, re-export it at 1080x1920 and use the same in/out points.
  - Otherwise, treat this cut as a stopgap until the re-render (section 3).
- **B3 has a garbled caption burned in** at about y 1080–1210 at this scale (measured from the contact sheet; the source review doesn't mention it). The caption band below covers it. Step through B3 frame by frame at full size, and grow the band if any letter shows.

### Caption band

- **Band:** Ink, x 0–1080, y 1020–1280 (also inside the middle third). On screen 0.00–5.08 and 9.08–9.68.
- **Tag:** **AI AVATAR**, Lato Black caps 30 px, Lime, at x 90, top of the band (about y 1045). It stays on over the YCEF card because her voice, also AI, plays there.
- **Captions:** Lato Bold 54 px, Off-white, at x 90, up to two lines of about 28 characters. Key words in Lime, as listed under the SRT.

### Edit table

| Time (s) | Picture | Exact on-screen text | Audio |
|---|---|---|---|
| 0.00–3.48 | B1: avatar to camera at a desk; caption band | **AI AVATAR**<br>**Climate action**<br>**training programme** (0.00–1.40)<br>**for young people in**<br>**Nigeria and Zambia.** (1.40–3.48) | B1 voice; music bed low |
| 3.48–5.08 | Lime card, full frame (her face not shown); caption band | **YCEF**<br>**Young Climate Educators Fellowship**<br>("YCEF": Bricolage about 300 px, Ink, y 520–800; name: Lato Bold 46 px, Ink, about y 860)<br>Band: **AI AVATAR** + **Selecting 50 fellows.** (3.68–5.00) | B2 voice 3.68–4.82; music |
| 5.08–7.08 | Ink card, full frame | **3**<br>**virtual weekends**<br>**Weekend 1: Fri 13 Nov 2026**<br>("3": Bricolage about 360 px, Lime; "virtual weekends": Bricolage about 96 px, Off-white; date line: Lato Bold 46 px, Off-white) | Music only |
| 7.08–9.08 | Lime card, full frame | **WHO CAN APPLY**<br>**18+**<br>**University students and grassroots**<br>**community volunteers**<br>(label: Lato Black caps 30 px; "18+": Bricolage about 300 px; last two lines: Lato Bold 46 px; all Ink) | Music only |
| 9.08–9.68 | B3: avatar to camera; caption band covering the garbled caption | **AI AVATAR**<br>**Apply now.** | B3 voice; music |
| 9.68–13.68 | End card B on Ink (below) | End card B text (below) | Music; fade out 13.18–13.68 |

### Burned-in captions (SRT)

```
1
00:00:00,000 --> 00:00:01,400
Climate action
training programme

2
00:00:01,400 --> 00:00:03,480
for young people in
Nigeria and Zambia.

3
00:00:03,680 --> 00:00:05,000
Selecting 50 fellows.

4
00:00:09,080 --> 00:00:09,680
Apply now.
```

- **Words in Lime:** "Climate action" (1), "Nigeria and Zambia." (2), "50 fellows." (3), "Apply now." (4).
- **The 1.40 split** is estimated from the transcript. Snap it to the pause after "programme" on the waveform.
- **Spelling:** "programme" is JOMO's spelling of the word she says.

### End card B (9.68–13.68, Ink, static)

The same layout as End card A, without the two fact lines (the cards already carried them):

```
[JOMO logo, light version]
YOUNG CLIMATE EDUCATORS
FELLOWSHIP (YCEF)
Apply by
Mon 26 Oct 2026
Applications close at [TIME] WAT
jomoclimatechange.org/events?apply=ycef
[Instagram icon] [LinkedIn icon] @jomoclimatechange
```

## 3. Avatar script for a sharper re-render (CapCut)

This is a full, correct avatar version that can replace Video B later.

- About 60 words: roughly 22–24 s at CapCut's normal speed. That is an estimate, so check the render.
- With a 3–4 s end card, the reel stays under 30 s.

**Script** (replace [TIME] first, then paste exactly):

```
Your street has a climate problem. You've got the fix.
The Young Climate Educators Fellowship, Y-C-E-F, is three virtual weekends to research that problem, design your fix and learn to pitch it.
Fifty fellows, aged eighteen and over, across Nigeria and Zambia.
Applications close on Monday the twenty-sixth of October, at [TIME].
Apply now at jomo climate change dot org.
```

**Pronunciation:**
- **Y-C-E-F:** four letters, "why, see, ee, ef". Never as a word, and never "I-C-E-F" (the original avatar said it that way). If the preview gets it wrong, try "Y. C. E. F.", then the phonetic "Why See Ee Eff".
- **Web address:** type it as words, "jomo climate change dot org". Don't paste the URL, or the voice will read out "slash events question mark". The full link goes on screen in the edit.
- **jomo:** one word, the way the team says the name. Check it in the first preview.
- **[TIME]:** write it in words, the way it should be said, adding "West Africa Time" if that's the zone. If it isn't confirmed when you render, end the sentence after "October".
- **Numbers:** written as words so the voice can't misread them. Listen for "fifty" (not "fifteen") and "eighteen" (not "eighty").

**CapCut settings:**
1. **Avatar:** one of CapCut's stock avatars who is clearly an adult and not modelled on a real person (item 8). Don't give her a name or a JOMO role; that is why the script has no "I" or "we". Use a clear English stock voice, never a cloned one. A West or Southern African English voice suits the audience, if CapCut offers one.
2. **No AI-generated on-screen text or graphics:** switch off auto captions, titles, text templates, stickers, and any AI scene or B-roll inserts. (The original's glass board with garbled text was AI-generated.) Use a background with no readable text, signs or screens.
3. **Speed:** normal. If the render runs over 25 s, raise the speed slightly (no more than 1.1x) rather than cutting facts.
4. **Export:** 1080x1920 (9:16), 25 or 30 fps, highest quality, no music. Keep the "CapCut AI" mark unless your plan allows export without it.
5. **Check before editing:**
   - every word, especially the first one (the original's first word was garbled)
   - Y-C-E-F
   - the date
   - both numbers
   - the address
   - lip-sync
6. **Edit it like Video B:**
   - the caption band with **AI AVATAR** throughout
   - captions that follow the script, written as "YCEF" and "jomoclimatechange.org"
   - End card B for 3–4 s
   - optional: cut to the WHO CAN APPLY card while her voice says the "Fifty fellows" line (keep the tag on)

## 4. Music

- **Default: the platform's own library.**
  - Export Video A silent, and Video B with only the three voice clips.
  - At upload, add an instrumental with no lyrics in Instagram's editor. On Facebook, add one separately from Facebook's own library.
  - A business account may only be offered a smaller, commercially cleared set on Instagram. Pick from that.
- **Mood:** hopeful, upbeat and light.
  - **Video A:** set the track's start point so a drop or strong beat lands on the Lime card at 3.00.
  - **Video B:** keep the music well under her voice (for example, original audio 100 and music about 25), and check on a phone speaker.
- **Source music:** the source videos' music (CapCut library, licence for Instagram and Facebook unknown) stays out.
- **The team's own bed:** only if both of these are true:
  - JOMO made it and owns all of it in writing (no samples or loops from other libraries).
  - The operator approves it as an exception, because checklist item 9 currently says platform library only.
  - If approved, mix it in CapCut and duck it under her voice in Video B.
- **Feed uploads:** if a platform doesn't offer its library there, post Video A without music (it is built to work silent) rather than add an unlicensed track.

## 5. 4:5 feed version (1080x1350)

- **The crop:** a centred crop of each 9:16 master, y 285–1635, full width, no scaling.
  - Every text element was placed inside that window.
  - Video A's panel lands at y 475–955 and Video B's band at y 735–995.
  - The cards and end cards keep all their lines.
- **Watermark first:** the crop cuts off the "CapCut AI" mark at the top left of the AI footage.
  - Item 8 says don't remove a tool's watermark unless the plan allows export without it.
  - If the operator's plan doesn't allow it, or nobody is sure, skip the crop and share the 9:16 reel to the feed instead.
- **Video B headroom:** her hair sits close to the top edge of the crop.
  - If it looks cramped, build the 4:5 version as its own project and move the two avatar clips down about 40 px.
  - The band stays where it is and still covers B3's garbled caption. Check frame by frame.
- **Labels and music:** the same AI labels, caption disclosure and music rules as the reels.

## 6. Hand-offs

**Fact-checker:**
- **Sources:**
  - `references/brand-guide.md`: programme name, the 3-weekend virtual format, 50 fellows, Nigeria and Zambia, 18+, university students and grassroots community volunteers, research / design / learn to pitch.
  - The operator's brief of 2026-10-22 (matches the brand guide): deadline Mon 26 Oct 2026, Weekend 1 Fri 13 Nov 2026, closing time [TIME], link.
  - `source-review.md`: usable footage and voice timings.
- **Pitching:** "Learn to pitch it" is on file (fellows "learn to pitch for seed funding"). Nothing on screen or in the script mentions funding, prizes or a competition.
- **Still open:** whether the link loads, the handle, and [TIME] (see "Settle before export").

**Policy and Safety Reviewer (item 8):**
- **Covered in these scripts:**
  - The on-screen labels are specified above.
  - The under-18-looking shots and the garbled face are cut.
  - All garbled AI text is covered, and all text is added in the edit.
  - Nothing presents the AI people or the avatar as JOMO staff, fellows or a real JOMO event.
  - The gully shot shows no identifiable people (item 6).
- **Still to confirm:**
  - the caption disclosure and Meta's AI label (Copywriter and operator)
  - that the avatar is a CapCut stock avatar (operator)
  - CapCut plan terms (operator)
  - music (section 4)

**Copywriter:**
- **AI disclosure:** each caption must say so: that the visuals are AI-generated (A), or that the presenter is an AI avatar (B). The operator switches on Meta's AI label at upload.
- **What the videos leave out:** university students and grassroots community volunteers, 18+; Weekend 1 Fri 13 Nov 2026; the closing time; the link (Facebook) or "link in bio" (Instagram).
- **Funding:** if a caption mentions pitching, add that there is no funding guarantee.

**Designer:**
- **To build:** the Lime card, the three Video B cards and both end cards, to the specs above.
- **Covers:** the first frame of A (hook and label), and for B the YCEF card without the band.

**Operator:**
- **Before export:** the five items under "Settle before export".
- **Sharper source:** a 1080x1920 re-export of the original avatar project, if it still exists.
- **Optional, later:** a volunteer could film a real shot to replace A1: a 4 s vertical phone shot of a blocked drain or gully, steady, at street level, with no people in frame (name the place in the caption). That segment would then need no AI label.
