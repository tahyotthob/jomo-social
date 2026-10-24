# JOMO Social Studio

A static site that shows what the social media team has made: one chat-style thread per post (each role's output as a message), the visuals and videos, and the captions ready to copy or download for every channel. Internal use only, so there is no login.

## How it works

`build.mjs` (plain Node, no dependencies) reads the repo and writes `web/dist/`:

- `content/posts/*/`: every `.md` file becomes a message from the role named in it (`Role: Copywriter`); `captions*.md` is parsed into per-platform captions and alt text; `review.md` is split into the review and its dated follow-ups; the visuals and videos become a Designer or Video Producer message and the download list.
- `content/posts/*.md`: weekly plans, briefs and sign-off packs.
- `content/calendar/calendar.csv`: the Calendar page, and the status of each post.
- Message dates come from git history, with the folder date as the fallback.

`src/` holds the page: `index.html`, `app.js`, `styles.css` and the vendored libraries (marked, DOMPurify, JSZip). "Download kit" builds a zip in the browser with one caption file per platform, the alt text, every media file and a README.

## Deploy on Vercel

1. In Vercel, **Add New → Project → Import** the `tahyotthob/jomo-social` repository.
2. Leave every setting as it is. The `vercel.json` at the repo root sets the build (`node web/build.mjs`) and the output folder (`web/dist`). There is nothing to install.
3. Deploy. Every push to the production branch rebuilds the site, so new posts appear as soon as they are committed.

The site needs no environment variables, database or authentication. If you want to keep it off search engines, Vercel's deployment protection (password or Vercel login) can be switched on for the project.

## Run locally

```bash
cd web
npm run serve      # builds, then serves http://localhost:8787
```
