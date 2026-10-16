# JOMO social media team — starter repo

Claude Code runs JOMO Climate Change Initiative's social media team from this repo: twelve roles as subagents, the brand references they read, the content calendar, finished posts, and the flyer tools.

## Set up (once, about 10 minutes)

1. Create a new private GitHub repo (for example `jomo-social`) and push this folder to it.
2. In the repo settings, add a secret named `ANTHROPIC_API_KEY` (Settings → Secrets and variables → Actions). This lets the GitHub workflow run.
3. Install the Claude GitHub app on the repo (run `/install-github-app` from any Claude Code session, or install it from github.com/apps/claude).
4. Add JOMO photos to `assets/photos/` and a row for each in `content/consent-log.csv`. Copy the current calendar into `content/calendar/calendar.csv`.

## Running the team

**In a cloud session (Claude Code on the web or in the Claude app):** open the repo and type what you'd say here: "run the weekly session", "draft a one-off post for World Cleanup Day", "review these comments". The Editor-in-Chief agent calls the others and stops twice for your approval.

**From GitHub itself:** open an issue or comment `@claude run the weekly session`. Claude replies in the thread and opens a pull request with the post folders and the calendar update. Merge the PR when you've signed off.

**On your computer:** `cd jomo-social && claude`, then the same requests.

Nothing is ever posted to Instagram, Facebook, LinkedIn or X from this repo. After sign-off you schedule in Meta Business Suite and LinkedIn and post X by hand, as before.

## Folder map

| Folder | What's in it |
|---|---|
| `CLAUDE.md` | The non-negotiables and conventions every session reads first |
| `.claude/agents/` | One file per role; edit a file to change how that role works |
| `references/` | Brand guide, voice, platforms, safety checklist, reporting, team playbook |
| `assets/logos/`, `assets/photos/` | Logos; photos with consent on record |
| `content/calendar/` | `calendar.csv` is the source of truth; the Google Sheet is a mirror |
| `content/posts/` | One folder per post: captions.md, review.md, the PNGs |
| `content/analytics/` | Exports and weekly reports |
| `tools/` | Flyer builder and the interactive newsroom map |
| `.github/workflows/claude.yml` | The `@claude` GitHub workflow |
