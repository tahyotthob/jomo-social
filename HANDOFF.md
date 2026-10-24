# Handoff: where the JOMO social team stands (2026-10-24)

Read `CLAUDE.md` first, then use the `jomo-social-team` skill (`.claude/skills/jomo-social-team/SKILL.md`). This note covers what is in flight. Update it, or delete it, when it goes stale.

## Done and live

- **YCEF motion-graphics reels** posted on 2026-10-24 on Instagram, Facebook, LinkedIn and X: "Your street has a climate problem." and "Three weekends. One street. Your fix." Files, captions and review notes are in `content/posts/2026-10-22-ycef-videos/`. Calendar rows are Posted. The code-made music track was approved as a one-off exception to safety check 9.
- **AI content rule** (safety checklist item 8): AI avatars and AI visuals are allowed when labelled, never presented as real JOMO people, events or results, with no AI people who look under 18 and no removal of a tool's AI mark. The earlier AI remakes (`video-a-ycef-promo*`, `video-b-ycef-ai-avatar*`) are superseded and must not be posted.
- **Super El Niño heat posts** approved by the operator on 2026-10-24 (all four slots: IG+FB carousel Sat 24 Oct 18:00, X thread Sat 18:30, LinkedIn Sun 25 Oct 10:00, IG+FB story Sun 16:00 WAT). Files in `content/posts/2026-10-24-super-el-nino/`. Calendar rows are Approved; set them to Scheduled or Posted once they go out. Boosting not decided; the reviewer recommends organic only.
- **Social Studio**, a read-only viewer of the team's work (threads per post, videos, per-platform captions with copy and download, a zip kit per post): https://jomo-social-studio.vercel.app. Code in `web/`, built by `web/build.mjs`, configured by `vercel.json`. The Vercel project `jomo-social-studio` is linked to this repo and redeploys on every push to `main`. If a deploy ever doesn't start, a manual production deployment of `main` works.
- **Slack:** #social-media (channel ID C0CBQCY0AFP) in the "J'omo Climate Change Initiative" workspace. The rules for posting there are in `references/team-playbook.md`.

## Key facts to keep straight

- YCEF applications close **Mon 26 Oct 2026, 11:59 PM WAT**. Weekend 1 is Fri 13 Nov 2026. Link: https://jomoclimatechange.org/events?apply=ycef. Never promise funding.
- The handle is **@jomoclimate**. Some older drafts and images still print @jomoclimatechange; the facts in `references/brand-guide.md` win.
- Times are WAT (UTC+1). Zambia is one hour ahead.
- The operator is Olusegun Olusoji-Ojelade. Nothing is published or scheduled until he approves that specific post.

## Open items

0. **YCEF deadline may move to Tue 3 Nov 2026** (operator, 2026-10-24, not yet final). Announce Mon 26 Oct and repurpose the missed countdown, X and LinkedIn drafts for the new date. Confirm the exact close time and that the website form stays open, then update `references/brand-guide.md`.
0. **Two JOMO avatars and personas** requested. Recommended: illustrated adult characters made in Canva (apply for Canva for Nonprofits), animated with `tools/video/`, voiced with CapCut "Commercial use" text-to-speech. Waiting on the operator's choice of style and roles.

1. **Week of 16 Oct drafts** (`content/posts/2026-10-1*` and `2026-10-2[0-2]-*`) are reviewed but **unapproved**, and their dates have passed (the Friday 16 and Sunday 18 slots and the YCEF countdown days). Decide whether to re-date, rework or drop them. They still show as In review in Social Studio.
2. **Held-back posts:** three JOMO's Pods posts (waiting on the episode date and topic) and the Rotary tree-planting LinkedIn post (waiting on Rotary's approval to be named).
3. **Photos:** the Ketu Cleanup photos aren't used because they show Oxygen X branding that needs partner approval. The consent log marks event volunteers "18+ (not individually verified)" except `oniwaya-cleanup-11.jpg`, which the operator confirmed.
4. **Claude Tag** (Claude in Slack) isn't set up. It needs a Claude Team or Enterprise plan, a Claude organisation Owner, a Slack workspace admin and a GitHub organisation owner. Setup is at https://claude.ai/admin-settings/claude-tag. Whether Claude Tag loads the roles in `.claude/agents/` is undocumented; the skill is the fallback.
5. **Talking to the team from Social Studio** was proposed but not built. The options: post messages from the app to Slack (free, needs a Slack webhook stored as a Vercel secret); or live replies from Claude in the app (needs an Anthropic API key and a shared passcode, because it spends money). The operator hasn't chosen.
6. **Connectors** (Slack, Vercel) load only when a session starts, so connect them before starting a session that needs them.
7. **Housekeeping:** set the GitHub default branch to `main` if it still points at an old `ccr-…` branch, and delete spent `ccr-…` branches. The old Vercel project `jomo-social-studio-unlinked` was deleted.

## Tools you will need

- **Flyer and slide images:** `tools/build.py`, `tools/render.js` (see `tools/README.md`).
- **Videos:** `tools/video/ycef_motion.py` (motion graphics, rendered at 60 fps and blended to 30 fps), `ambient_bed.py` (code-made music), `render_frames.js`. Rendering needs Chromium (`CHROMIUM_PATH`) and ffmpeg. Run `npm install` in `tools/` first.
- **Social Studio:** `node web/build.mjs` builds into `web/dist/`; `cd web && npm run serve` previews it at http://localhost:8787.
