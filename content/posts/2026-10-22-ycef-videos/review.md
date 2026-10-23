# Review: YCEF videos, 2026-10-22 · Video A (promo reel) and Video B (AI avatar explainer) · Instagram reel + Facebook reel + LinkedIn vertical video + X
Role: Policy and Safety Reviewer

This is the final review of the finished files and all eight captions. It follows my earlier review of the source videos and the remake plan.

I read build-notes.md, the "As built" section of scripts.md, captions.md and the SRT. I viewed the 13 stills, both contact sheets, both covers and source/v1-contact-sheet.png. I have not played the video or audio files. Nothing has been approved, scheduled or published.

## Verdicts

- **Video A, promo reel: FIX.**
  - The singular "volunteer" fix is applied in three captions and the alt text.
  - The Video Producer must run one frame check before sign-off: the AI figures on the ridge (below).
  - The operator items below also apply.
- **Video B, AI avatar explainer: BLOCK until the operator confirms where the avatar and voice came from.**
  - The risk: the presenter is a photorealistic AI woman with an AI voice. Nobody has confirmed that she and the voice are CapCut stock, rather than modelled on or cloned from a real person. Nobody has confirmed that they carry CapCut's "Commercial use" mark either.
  - If either answer is no, posting breaks item 8 and could use a real person's likeness without consent. No edit can fix that.
  - Everything else passes and needs no edits. Once the operator confirms (operator item 1), Video B is a PASS, subject to the shared operator items.
- **With-music files (video-a-ycef-promo.mp4, video-b-ycef-ai-avatar.mp4): BLOCK until the operator decides on item 9.**
  - The risk: item 9 allows platform-library music only, so using the bed needs the operator's exception.
  - The copyright risk of the bed itself is low. tools/video/music_bed.py makes every sound in code, reads no audio file and uses a stock chord progression.
  - The no-music and voice-only files are clear on item 9.

Video A is a FIX rather than a BLOCK on the same CapCut question because its AI clip is a landscape. If the answer is no, a JOMO photo can replace it.

## Edits made (captions.md)

These apply the Fact-checker's finding, which matches mine: the clean-up photo shows one volunteer, so "volunteers" was wrong.

- **Video A, Instagram, Facebook and LinkedIn.**
  - Was: "The clean-up photo is real: JOMO volunteers at the Oniwaya clean-up."
  - Now: "The clean-up photo is real: a JOMO volunteer at the Oniwaya clean-up."
- **Video A alt text:** it now quotes the re-rendered on-screen line, "Real JOMO volunteer clearing a drain, Oniwaya clean-up." I checked the updated stills/a-3.8.jpg and it matches.
- **Unchanged:** the Video A X post ("clean-up photo real").
- **Video B:** no edits.

## Needed from the Video Producer (video changes; I have not edited the build)

1. **Required before sign-off: check the AI figures on the ridge in Video A.**
   - **Where:** about 0.5–1.4 s (source about 1.2–1.8 s).
   - **Why:**
     - No full-size still shows them. a-0.5 is the last gully frame before that shot, and a-1.6 is the cascade after it.
     - The contact sheets show a small group of standing people: a-contact-sheet at 0.5 and 1.0 s, and source/v1-contact-sheet at 1.5 s.
     - I estimate they are roughly 150–200 px tall at full size, which is more than "tiny".
     - Most of the people in this source wear the crested school-style uniform.
   - **Do:**
     - Export full-size stills at about 0.6, 0.9 and 1.2 s.
     - Also export the first frame (0.00 s) and the last AI frame (about 2.92 s). These rule out any trace of the man in the crested polo or of the sketchbook.
     - Add the stills to stills/ and to the sign-off pack, and send them back to me.
     - If any figure looks under 18 or wears a uniform or crest, cut that shot. Re-time the opening from the gully and cascade frames on either side. Keep the band, the pill and the uncovered "CapCut AI" mark as they are.
2. **Recommended: move the label pills in both videos from y 268 to about y 300.**
   - y 300 is where the safe area in scripts.md starts.
   - At y 268, a feed that crops the reel to 4:5 (y 285–1635) clips the top of the "AI-generated visuals" and "AI avatar" labels.
   - The "CapCut AI" mark stays clear above the pills either way.
   - The re-rendered photo shot (a-3.8) still has its pill at y 268.

The singular photo line ("Real JOMO volunteer…") is already re-rendered, so nothing else is needed from the Video Producer on that.

## Operator must do before posting

1. **CapCut (item 8). Do not post until you confirm all three:**
   - (a) The gully clip and the avatar were made from prompts only, with no uploaded photo or video of a real person or place. Video A's end card says "not a real place".
   - (b) The avatar is a CapCut stock avatar and the voice is a stock voice. Neither is modelled on or cloned from anyone.
   - (c) The materials carried CapCut's "Commercial use" mark.
   - If (a) or (c) fails for Video A, replace the AI opening with a JOMO photo. If any of the three fails for Video B, don't post it.
2. **Music (item 9).** Choose one:
   - grant the exception for the team-made bed
   - or post video-a-ycef-promo-no-music.mp4 and video-b-ycef-ai-avatar-voice-only.mp4. On Instagram and Facebook you can add the platform's own music in the app. LinkedIn and X stay without music.
3. **Listen on headphones to both Video B files.**
   - CapCut's music was removed with Demucs, and so far only a machine has checked the result.
   - If you can hear any music under her voice, don't use those clips.
   - If you approve the bed, listen to it too.
4. **Consent (item 2).** Confirm that nobody in oniwaya-cleanup-11.jpg looks under 18.
   - The consent row says "18+ (not individually verified)", and this question has been open since 2026-10-16.
   - The face is hidden and no name is given, but she is the only real person in either video.
5. **AI labels (item 8).**
   - Instagram and Facebook: switch on Meta's "Add AI label" for both videos. It is required for realistic AI video and voice. If Meta Business Suite doesn't offer it when scheduling, post from the app.
   - X and LinkedIn: use their AI labels where offered.
   - TikTok or YouTube: if you also post there, switch on their AI settings.
6. **Link (item 12).**
   - Open https://jomoclimatechange.org/events?apply=ycef on a phone, including in Instagram's in-app browser, and confirm it opens the YCEF application.
   - Confirm the Instagram bio link points there.
   - Confirm the link can be tapped in the posted Facebook reels.
7. **Handle (item 12).** Both end cards print @jomoclimatechange. If the account is @jomoclimate:
   - re-render both videos (`HANDLE` in tools/video/ycef_videos.py)
   - change both alt texts.
8. **[TIME].**
   - Fill in the closing time in all eight captions, or delete ", [TIME] WAT". Never post the placeholder.
   - If you also give the Zambia time (CAT is one hour ahead), note that a close at 23:00 WAT or later falls on Tue 27 Oct in Zambia.
9. **Boosting (item 5).** Tell me first if you plan to boost either video.

## Checks: Video A (promo reel, all four captions)

1. **Accuracy.**
   - Mon 26 Oct and Fri 13 Nov 2026 fall on the right weekdays.
   - 50 fellows, 3 virtual weekends, Nigeria + Zambia, 18+, who can apply and what fellows do all match brand-guide.md.
   - Every caption that mentions pitching says there is no funding guarantee. Nothing mentions a prize or competition.
   - The photo line is now singular in the video, the captions and the alt text (above).
2. **Consent.**
   - oniwaya-cleanup-11.jpg has a row in content/consent-log.csv, and the face is hidden. Age confirmation is pending (operator 4).
   - The AI figures are not real people. Their apparent age is covered by Video Producer 1.
3. **Engagement bait.** None.
   - "Which would you fix first?" (Instagram) is a genuine question. It doesn't tell anyone to comment, vote or tag.
   - LinkedIn's "If you teach, mentor or lead young people…" gives the link and doesn't ask for shares.
4. **Apolitical.** No officials, parties, slogans or blame.
5. **Boosting.** No boost is planned (operator 9).
6. **No shaming.**
   - The real photo shows a volunteer cleaning, with the face hidden.
   - The AI scene shows waste. Its distant figures are not shown littering.
7. **Climate claims.** No statistics or predictions. The hook is JOMO's design signature (brand-guide.md).
8. **AI content.**
   - The "AI-generated visuals" pill is on every AI frame and on the cover. The real photo carries "Real photo · JOMO archive".
   - The end card and all four captions disclose the AI scene.
   - The "CapCut AI" mark sits top left and is never covered. It is faint on the misty frames from about 1.4 s and on the cover, but that is the footage, not an overlay.
   - CapCut's burned-in text sits under the band, and all on-screen text was added in the edit.
   - Still open: the ridge figures (Video Producer 1), the CapCut answers (operator 1) and the platform labels (operator 5).
9. **Copyright.**
   - The photo and logo are JOMO's own.
   - The fonts are Anton, Bricolage Grotesque and Lato, all open-licence Google Fonts.
   - No source audio is used.
   - The bed is blocked until the operator decides (above). The no-music file is clear.
   - Packaging visible in the litter is incidental.
10. **Partners.** None named. The photo's "World Clean Up Day" badge is JOMO's own.
11. **Fundraising.** None. Seed funding appears only as something fellows learn to pitch for, next to the no-guarantee line.
12. **Links and handles.** The link and handle are unconfirmed (operator 6 and 7). No link shorteners.
13. **Hate and safety.**
    - Nothing mocks a group.
    - The AI scene is labelled as not a real place.
    - Oniwaya was a public clean-up, and the volunteer can't be identified.

## Checks: Video B (AI avatar explainer, all four captions)

1. **Accuracy.**
   - Speech-to-text (build-notes.md) hears only the three accurate lines. The wrong dates, garbled words and wrong address are gone, and she never says "YCEF".
   - The cards, the SRT and the captions match brand-guide.md.
   - "15 seconds" matches the 15.0 s file.
   - "No funding guarantee" is on the card and in every caption that mentions pitching.
2. **Consent.** No real people appear. The likeness question is under check 8.
3. **Engagement bait.** None. "If someone you work with fits, the application is here" is a call to action, not a request to share.
4. **Apolitical.** No political content.
5. **Boosting.** Same as Video A.
6. **No shaming.** Not applicable.
7. **Climate claims.** None.
8. **AI content.**
   - The "AI avatar" pill is on from the first frame to the end card. That includes the cards while her voice plays.
   - The end card says: "The presenter is an AI avatar, not a JOMO team member."
   - All four captions disclose the avatar, and three of them also name the AI voice.
   - She has no name or role, never says "we", and gives no testimonial. She is clearly an adult.
   - CapCut's garbled caption is covered (b-9.95 is clean), and the "CapCut AI" mark is visible.
   - Still open: whether the avatar and voice are stock with the "Commercial use" mark (the BLOCK), the headphone check (operator 3) and the platform labels (operator 5).
9. **Copyright.**
   - CapCut's library music was removed from the voice. Only a machine has checked this so far (operator 3).
   - The bed: same as Video A.
10. **Partners.** None.
11. **Fundraising.** None.
12. **Links and handles.** Same as Video A.
13. **Hate and safety.** Nothing.

## Other checks

- **Hashtags:**
  - Instagram: 5 (Video A) and 5 (Video B)
  - Facebook: 3 and 3
  - LinkedIn: 2 and 2
  - X: 1 and 2
- **Emojis:** only on Instagram and Facebook.
- **X length:** recounted at 272 characters (Video A) and 264 (Video B), counting the link as 23. Filling in [TIME] will change these.
- **What I checked:**
  - the 13 stills a-0.5 to b-12.5, with a-3.8 checked again after the re-render
  - both contact sheets, cover-video-a.jpg and cover-video-b.jpg
  - source/v1-contact-sheet.png
  - video-b-ycef-ai-avatar.srt
  - tools/video/music_bed.py
  - the consent row for oniwaya-cleanup-11.jpg

## Follow-up, 2026-10-22: re-rendered videos

The Video Producer cut the ridge shot and moved the pills. I checked:
- the new stills (a-0.0 to a-12.0, b-1.0 to b-12.5)
- both new contact sheets and both covers
- the updated build-notes.md.

**Verdicts (unchanged)**
- **Video A: FIX.** The required frame check is done, and nothing more is required from the Video Producer. One change is recommended (the cover, below). The operator items above still apply.
- **Video B: BLOCK** until the operator confirms the avatar and voice (operator item 1). The re-render changed only the pill position.
- **With-music files: BLOCK** until the operator decides on item 9.

**New Video A opening**
- The ridge shot is cut, and the opening now shows:
  - 0.00 to about 0.7 s: brown water and plastic. a-0.0 shows no trace of the man in the crested polo.
  - then to 2.36 s: the cascade. a-1.9 and the contact sheet show no trace of the sketchbook.
- **Silhouettes in the cascade (a-0.9, a-1.4, a-1.9): acceptable, PASS on items 6 and 8.**
  - What I see:
    - two figures on the hillside
    - a handful on the far bank
    - one on a rock beside the waterfall.
  - They are roughly 50–100 px tall, with no faces and no visible uniforms or crests, and nobody is littering or in distress.
  - At this size a smaller figure reads as further away, not as a child. The ridge group was about twice as big, which is why a small figure there could pass for a child.
  - They are on screen for about 1.6 s, moving, under the AI label and the hook.
  - Residual risk is small but real, because AI perspective is unreliable. If the operator wants no AI people at all, replacing the AI opening with a people-free JOMO drain photo also settles operator item 1(a) and (c) for Video A.
- **Recommended: change the Video A cover.**
  - cover-video-a.jpg is now the 1.4 s cascade frame, so it carries all of these figures as a still that stays on the grid and can be studied.
  - The frame at about 0.4 s (a-0.4) has the hook and the AI label, with only two tiny specks in the trees.
- **Pills:** at y 300 in both videos and on both covers, inside a 4:5 crop. The "CapCut AI" mark is visible and uncovered on every CapCut still. In Video B the "Apply now" band still hides CapCut's garbled caption (b-9.95).

**captions.md:** no edits needed in this round. The singular "volunteer" fix and its alt text are intact, and the Visual line already gives the new 14.2 s length.

**Not safety (for the Video Producer):**
- In both videos the first frame shows an empty caption band (a-0.0; b-contact-sheet at 0.0 s). The hook, lower third and captions fade in a moment later. The AI label is on from frame one, so disclosure is fine, but scripts.md wanted the hook visible from the first frame.
- build-notes.md calls cover A "the gully frame"; it is the cascade frame.

## Motion-graphics versions, 2026-10-23
Role: Policy and Safety Reviewer

These replace the AI versions above, so the CapCut, avatar and AI-label items no longer apply. I checked captions-motion.md (all eight captions and both alt texts), the 15 stills in stills/motion/, the consent row for oniwaya-cleanup-11.jpg, tools/video/ycef_motion.py (logo, photo, handle, fonts) and tools/video/ambient_bed.py. I have not played the video or audio files. Nothing is approved, scheduled or published.

**Verdicts**
- **Video A, "Your street has a climate problem." (18.5 s): PASS.** No edits.
- **Video B, "Three weekends. One street. Your fix." (21.5 s): PASS.** No edits.
- **With-music files (video-a-ycef-motion.mp4, video-b-ycef-motion.mp4): BLOCK until the operator decides on item 9.** Item 9 allows platform-library music only, so the team-made bed needs your exception. The copyright risk is low: ambient_bed.py only writes a WAV, reads no audio file and uses no samples. The no-music files are clear.

**Checks (both videos, all captions)**
1. Accuracy: every fact on screen and in the captions matches brand-guide.md and the operator's inputs. That covers 50 fellows, Nigeria + Zambia, 3 virtual weekends, Weekend 1 Fri 13 Nov 2026, university students and grassroots community volunteers 18+, and the close at Mon 26 Oct, 11:59 PM WAT. Both dates fall on the right weekdays. Every mention of pitching carries "There is no funding guarantee" (on screen in b-10.4 and in all eight captions). There is no prize or competition. "Now open" is true until the close.
2. Consent: oniwaya-cleanup-11.jpg has a consent row, now marked "18+ (confirmed by operator 2026-10-23)". The face is hidden and no name is given. She is the only real person in either video.
3. Engagement bait: none. "Which would you fix first?" is a genuine question.
4. Apolitical: no officials, parties, slogans or blame.
5. Boosting: none planned. Tell me first if that changes.
6. No shaming: the volunteer is shown cleaning, and the waste is the problem. Nobody is shown littering.
7. Climate claims: no statistics or predictions.
8. AI content: none (no AI footage, avatar or voice). No AI label is needed, so leave the platform AI labels off.
9. Copyright: the photo and the light logo are JOMO's own. Bricolage Grotesque and Lato are open-licence fonts. Music: see the BLOCK above.
10. Partners: none named.
11. Fundraising: none.
12. Links and handles: the link matches brand-guide.md and the operator confirmed it works. @jomoclimate is on both end cards and in ycef_motion.py. No shorteners.
13. Hate and safety: nothing. Oniwaya was a public clean-up, and the volunteer can't be identified.

Format: the hashtags (IG 5, FB 3, LinkedIn 2, X 1) and emojis are within voice.md. Both X posts are under 280 characters. All text sits clear of the top and bottom 250 px.

**Operator, before posting**
1. Music: grant the item 9 exception, or post the no-music files.
2. Confirm the Instagram bio link points to the YCEF application (the IG captions say "link in bio").
3. Fill in [POST DATE] and [POST TIME] before Mon 26 Oct, 11:59 PM WAT. Optional: 11:59 PM WAT is 12:59 AM Tue 27 Oct in Zambia (CAT). Consider saying so for Zambian applicants.

**Not safety (Video Producer):** the first frame of both videos is blank (a-0.0, b-0.0), and the hook only appears at about 1.8–2.0 s. The tagline under the light logo is barely legible on Ink.
