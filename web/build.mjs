// Builds the JOMO Social Studio: a static site that shows the team's work as
// chat-style threads with downloads. No dependencies; runs on Vercel with
// `node web/build.mjs` (see vercel.json at the repo root).
//
// Reads  content/posts/*/ (captions, reviews, notes, visuals, videos),
//        content/posts/*.md (weekly plans and briefs),
//        content/calendar/calendar.csv, assets/logos/
// Writes web/dist/ (index.html, app.js, styles.css, data.json, media/)
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const POSTS = path.join(ROOT, "content/posts");
const DIST = path.join(HERE, "dist");
const MEDIA_EXT = new Set([".png", ".jpg", ".jpeg", ".webp", ".mp4", ".srt", ".mov", ".gif"]);
const SKIP_DIRS = new Set(["source", "stills"]); // originals and frame checks stay out of the site

const ROLE_ORDER = ["Editor-in-Chief", "Analyst", "Trend Scout", "Creative Director", "Copywriter", "Designer",
  "Video Producer", "Impact Storyteller", "Partnerships Liaison", "Fact-checker", "Policy and Safety Reviewer",
  "Community Manager", "Operator"];
const ROLE_BY_FILE = [
  [/^scripts/, "Video Producer"], [/^build-notes/, "Video Producer"], [/^source-review/, "Editor-in-Chief"],
  [/signoff-pack/, "Editor-in-Chief"], [/week-briefs/, "Creative Director"], [/^captions/, "Copywriter"], [/^review/, "Policy and Safety Reviewer"],
];

const read = (p) => fs.readFileSync(p, "utf8");
const exists = (p) => fs.existsSync(p);

function git(args) {
  try { return execSync(`git ${args}`, { cwd: ROOT, stdio: ["ignore", "pipe", "ignore"] }).toString().trim(); }
  catch { return ""; }
}
function fileDates(rel) {
  const first = git(`log --diff-filter=A --format=%aI -- "${rel}"`).split("\n").filter(Boolean).pop() || "";
  const last = git(`log -1 --format=%aI -- "${rel}"`) || first;
  return { created: first, updated: last };
}
function dateFromSlug(slug) {
  const m = slug.match(/^(\d{4}-\d{2}-\d{2})/);
  return m ? `${m[1]}T09:00:00+01:00` : "";
}

function roleOf(text, file) {
  const m = text.match(/^\*{0,2}Role:\s*([^*\n(·]+)/m);
  if (m) return normaliseRole(m[1].trim());
  const base = path.basename(file);
  for (const [re, role] of ROLE_BY_FILE) if (re.test(base)) return role;
  return "Editor-in-Chief";
}
function normaliseRole(r) {
  r = r.replace(/\s*\(.*$/, "").trim();
  const hit = ROLE_ORDER.find((x) => r.toLowerCase().startsWith(x.toLowerCase()));
  return hit || r;
}
function titleOf(text, fallback) {
  const m = text.match(/^#\s+(.+)$/m);
  return (m ? m[1] : fallback).replace(/^(Captions|Review|Creative Director briefs|Sign-off pack):\s*/i, "").trim();
}
function stripHeader(text) {
  return text.replace(/^#\s+.+\n/, "").replace(/^\*{0,2}Role:[^\n]*\*{0,2}\n/m, "").trim();
}

// Captions: "Caption — Instagram:" blocks, alt text, hook, slot. A file may hold several sections (## headings).
function parseCaptionSections(text) {
  const parts = text.split(/^(?=## )/m);
  const sections = [];
  for (const part of parts) {
    const heading = (part.match(/^## (.+)$/m) || [])[1] || "";
    const captions = {};
    let altText = "";
    const lines = part.split("\n");
    let cur = null, buf = [];
    const stop = /^(Caption — |Alt text|Sources:|AI label|Visual decision|Visual:|Hook:|## |### |\((\d|Approx|Under|roughly|about)|\*\*)/;
    const flush = () => {
      if (cur === null) return;
      const body = buf.join("\n").replace(/\n{3,}/g, "\n\n").trim();
      if (cur === "__alt") altText = altText || body; else if (body) captions[cur] = body;
      cur = null; buf = [];
    };
    for (const line of lines) {
      const c = line.match(/^Caption — ([A-Za-z]+)[^:]*:\s*(.*)$/);
      const a = line.match(/(?:^|\.\s+)Alt text[^:]*:\s*(.*)$/);
      if (c) { flush(); cur = c[1]; if (c[2]) buf.push(c[2]); continue; }
      if (a) { flush(); cur = "__alt"; if (a[1]) buf.push(a[1]); continue; }
      if (cur !== null && stop.test(line)) { flush(); continue; }
      if (cur !== null) buf.push(line);
    }
    flush();
    const slot = (part.match(/^### (.+)$/m) || [])[1] || "";
    const [when = "", platforms = "", pillar = ""] = slot.split(" · ");
    const hook = (part.match(/^Hook:\s*(.+)$/m) || [])[1] || "";
    const visual = (part.match(/^Visual:\s*(.+)$/m) || [])[1] || "";
    if (Object.keys(captions).length) sections.push({ heading: heading.replace(/^(Video [AB]):?/, "$1:"), when, platforms, pillar, hook, visual, captions, altText });
  }
  return sections;
}

// Channel posts: one entry per platform per slot, so a caption is never shared between channels.
// A slot is a "### <when> · <platforms> · <pillar>" heading; "## " headings above it name a group (e.g. "Video A").
const PLATFORM_NAMES = [["Instagram", /instagram/i], ["Facebook", /facebook/i], ["LinkedIn", /linkedin/i], ["X", /(^|[^a-z])x([^a-z]|$)|twitter/i]];
const platformOf = (s) => (PLATFORM_NAMES.find(([, re]) => re.test(s)) || [])[0] || "";
function parsePlatforms(str) {
  const items = str.split("+").map((x) => x.trim()).filter(Boolean).map((item) => {
    const platform = platformOf(item);
    const format = item.replace(/instagram|facebook|linkedin|twitter/ig, "").replace(/(^|\s)X(\s|$)/, " ").replace(/[()]/g, "").trim();
    return { platform, format };
  }).filter((x) => x.platform);
  const last = items[items.length - 1];
  if (last && /stor|reel|carousel/i.test(last.format)) for (const it of items) if (!it.format) it.format = last.format;
  return items;
}
function mediaForVisual(visual, media) {
  const names = media.map((m) => path.basename(m.file));
  const hits = new Set(names.filter((n) => visual.includes(n)));
  // "elnino-01.png to elnino-06.png": everything numbered in between
  for (const m of visual.matchAll(/`?(?:[\w./-]*\/)?([\w-]*?)(\d+)\.(png|jpe?g)`?\s+(?:to|-|–)\s+`?(?:[\w./-]*\/)?([\w-]*?)(\d+)\.\3`?/g)) {
    const [, pre, a, ext, , b] = m;
    for (const n of names) { const k = n.match(new RegExp(`^${pre.replace(/[-]/g, "\\-")}(\\d+)\\.${ext}$`)); if (k && +k[1] >= +a && +k[1] <= +b) hits.add(n); }
  }
  return media.filter((m) => hits.has(path.basename(m.file)));
}
function parseChannelPosts(text, media, calRows, postStatus) {
  const out = [];
  let group = "", prevAlt = "";
  const chunks = text.split(/^(?=##+ )/m);
  for (const chunk of chunks) {
    const g = chunk.match(/^## (.+)$/m);
    if (g && !chunk.startsWith("###")) { group = g[1].replace(/:\s*$/, "").trim(); continue; }
    const slot = (chunk.match(/^### (.+)$/m) || [])[1];
    if (!slot) continue;
    const [when = "", platformsStr = "", ...rest] = slot.split(" · ");
    const pillar = rest.join(" · ");
    const hook = (chunk.match(/^Hook:\s*(.+)$/m) || [])[1] || "";
    const visual = (chunk.match(/^Visual:\s*(.+)$/m) || [])[1] || "";
    const dm = when.match(/(\d{4}-\d{2}-\d{2}),?\s*(\d{1,2}:\d{2})?/);
    const date = dm?.[1] || "", time = dm?.[2] || "";
    // blocks: "Caption — Instagram (reel):", "Post 1:", "Post:", "Alt text…:"
    const blocks = []; let cur = null;
    // a caption may carry its own "Sources:" line (it's part of the post); notes after alt text are not
    const stop = /^(Visual:|Hook:|AI label|Visual decision|---\s*$|\((\d|Approx|Under|roughly|about|Each)|\*\*)/i;
    const altStop = /^(Sources?:|Story text)/i;
    for (const line of chunk.split("\n").slice(1)) {
      const c = line.match(/^Caption — ([^(:]+?)\s*(?:\(([^)]*)\))?\s*:\s*(.*)$/);
      const t = line.match(/^Post(?:\s+(\d+))?:\s*(.*)$/);
      const a = line.match(/(?:^|\.\s+)Alt text[^:]*:\s*(.*)$/);
      if (c) { cur = { kind: "caption", platform: platformOf(c[1]) || c[1].trim(), label: (c[2] || "").trim(), lines: [c[3]] }; blocks.push(cur); continue; }
      if (t) { cur = { kind: "post", n: +(t[1] || 1), lines: [t[2]] }; blocks.push(cur); continue; }
      if (a) { cur = { kind: "alt", lines: [a[1]] }; blocks.push(cur); continue; }
      if (cur && (stop.test(line) || (cur.kind === "alt" && altStop.test(line)))) { cur = null; continue; }
      if (cur) cur.lines.push(line);
    }
    const body = (b) => b.lines.join("\n").replace(/\n{3,}/g, "\n\n").trim();
    let alt = blocks.filter((b) => b.kind === "alt").map(body).filter(Boolean).join("\n\n");
    if (/^as for /i.test(alt)) alt = prevAlt; else if (alt) prevAlt = alt;
    const declared = parsePlatforms(platformsStr);
    const captionPlats = [...new Set(blocks.filter((b) => b.kind === "caption").map((b) => b.platform))];
    const posts = blocks.filter((b) => b.kind === "post");
    const plats = [...declared];
    for (const pl of captionPlats) if (!plats.some((d) => d.platform === pl)) plats.push({ platform: pl, format: "" });
    if (posts.length && !plats.some((d) => d.platform === "X")) plats.push({ platform: "X", format: "" });
    const slotMedia = mediaForVisual(visual, media);
    for (const { platform, format } of plats) {
      let variants = blocks.filter((b) => b.kind === "caption" && b.platform === platform).map((b) => ({ label: b.label, text: body(b) })).filter((v) => v.text);
      let thread = [];
      if (platform === "X" && !variants.length && posts.length) {
        if (posts.length > 1) { thread = posts.map(body); variants = [{ label: `thread of ${posts.length}`, text: thread.map((t, i) => `${i + 1}/${thread.length}\n${t}`).join("\n\n") }]; }
        else variants = [{ label: "", text: body(posts[0]) }];
      }
      const fmtLabel = format || (variants.length === 1 && variants[0].label) || "";
      const cal = calRows.find((r) => r.Date === date && (!time || r["Time (WAT)"] === time) && new RegExp(platform === "X" ? "(^|[^a-z])x([^a-z]|$)" : platform, "i").test(r.Platform));
      out.push({ platform, format: fmtLabel, group, when, date, time, pillar, hook, visual, variants, thread, altText: alt,
        media: slotMedia.map((m) => m.file), status: cal?.Status || postStatus });
    }
  }
  // number them in posting order, and give each a stable id
  out.forEach((c, i) => { c.n = i + 1; c.id = `${String(i + 1).padStart(2, "0")}-${c.platform.toLowerCase()}${c.format ? "-" + c.format.toLowerCase().replace(/[^\w]+/g, "-").replace(/^-|-$/g, "") : ""}`; });
  return out;
}

function verdictOf(reviewText) {
  if (/^## Operator sign-off/m.test(reviewText)) return "Approved";
  const all = [...reviewText.matchAll(/Verdict:?\**:?\s*\**\s*(PASS|FIX|BLOCK)/gi)];
  return all.length ? all[all.length - 1][1].toUpperCase() : "";
}

// Split a review into dated follow-up messages so a long review reads as a conversation.
function splitReview(text) {
  const parts = text.split(/^(?=## )/m);
  const main = [], extra = [];
  for (const p of parts) {
    const h = (p.match(/^## (.+)$/m) || [])[1] || "";
    const dated = /\b20\d\d-\d\d-\d\d\b/.test(h) || /^Operator sign-off/i.test(h);
    if (dated && main.length) extra.push({ heading: h, body: p.replace(/^## .+\n/, "").trim(), role: /operator/i.test(h) ? "Operator" : "Policy and Safety Reviewer" });
    else main.push(p);
  }
  return { main: main.join(""), extra };
}

function copyMedia(srcDir, slug, relBase = "") {
  const out = [];
  for (const entry of fs.readdirSync(srcDir, { withFileTypes: true })) {
    const rel = path.join(relBase, entry.name);
    if (entry.isDirectory()) { if (!SKIP_DIRS.has(entry.name)) out.push(...copyMedia(path.join(srcDir, entry.name), slug, rel)); continue; }
    const ext = path.extname(entry.name).toLowerCase();
    if (!MEDIA_EXT.has(ext)) continue;
    const dest = path.join(DIST, "media", slug, rel);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(path.join(srcDir, entry.name), dest);
    const type = [".mp4", ".mov"].includes(ext) ? "video" : ext === ".srt" ? "captions" : "image";
    out.push({ file: rel.replace(/\\/g, "/"), url: `media/${slug}/${rel.replace(/\\/g, "/")}`, type, bytes: fs.statSync(dest).size });
  }
  return out.sort((a, b) => a.file.localeCompare(b.file));
}

function parseCsv(text) {
  const rows = [];
  let row = [], cell = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (q) { if (ch === '"' && text[i + 1] === '"') { cell += '"'; i++; } else if (ch === '"') q = false; else cell += ch; }
    else if (ch === '"') q = true;
    else if (ch === ",") { row.push(cell); cell = ""; }
    else if (ch === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; }
    else if (ch !== "\r") cell += ch;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const [head, ...body] = rows.filter((r) => r.some((c) => c.trim()));
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h.trim(), (r[i] || "").trim()])));
}

// ------------------------------------------------------------------ build
fs.rmSync(DIST, { recursive: true, force: true });
fs.mkdirSync(path.join(DIST, "media/logos"), { recursive: true });
for (const f of ["index.html", "app.js", "styles.css"]) fs.copyFileSync(path.join(HERE, "src", f), path.join(DIST, f));
fs.cpSync(path.join(HERE, "src/vendor"), path.join(DIST, "vendor"), { recursive: true });
for (const f of ["jomo-logo.png", "jomo-logo-light.png"]) if (exists(path.join(ROOT, "assets/logos", f))) fs.copyFileSync(path.join(ROOT, "assets/logos", f), path.join(DIST, "media/logos", f));

const calendar = exists(path.join(ROOT, "content/calendar/calendar.csv")) ? parseCsv(read(path.join(ROOT, "content/calendar/calendar.csv"))) : [];

const posts = [];
for (const dir of fs.readdirSync(POSTS, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name).sort()) {
  const full = path.join(POSTS, dir);
  const mds = fs.readdirSync(full).filter((f) => f.endsWith(".md")).sort();
  const messages = [];
  let title = dir.replace(/^\d{4}-\d{2}-\d{2}-/, "").replace(/-/g, " ");
  let captionSets = [];
  let verdict = "";
  let primaryCaptionsDate = "";
  let primaryCaptionsText = "", primaryCaptionsFile = "";
  for (const f of mds) {
    const rel = path.join("content/posts", dir, f);
    const text = read(path.join(full, f));
    const dates = fileDates(rel);
    const role = roleOf(text, f);
    const created = dates.created || dateFromSlug(dir);
    const base = { file: f, role, created, updated: dates.updated || created };
    if (/^captions/.test(f)) {
      const sets = parseCaptionSections(text).map((s) => ({ ...s, file: f, updated: base.updated }));
      // the most recently edited captions file is the current one and names the post
      if (sets.length && (!primaryCaptionsDate || base.updated > primaryCaptionsDate)) { captionSets = sets; primaryCaptionsDate = base.updated; primaryCaptionsText = text; primaryCaptionsFile = f; title = titleOf(text, title); }
      messages.push({ ...base, title: titleOf(text, f), body: stripHeader(text), kind: "captions", sets });
    } else if (/^review/.test(f)) {
      verdict = verdictOf(text) || verdict;
      const { main, extra } = splitReview(text);
      messages.push({ ...base, title: titleOf(main, "Review"), body: stripHeader(main), kind: "review" });
      for (const e of extra) messages.push({ ...base, role: e.role, title: e.heading, body: e.body, kind: e.role === "Operator" ? "signoff" : "review", created: base.updated });
    } else {
      messages.push({ ...base, title: titleOf(text, f), body: stripHeader(text), kind: "note" });
    }
  }
  const media = copyMedia(full, dir);
  if (media.some((m) => m.type === "image" || m.type === "video")) {
    const vis = media.filter((m) => m.type !== "captions");
    const d = fileDates(path.join("content/posts", dir, vis[0].file));
    messages.push({ file: "visuals", role: /video/.test(dir) ? "Video Producer" : "Designer", created: d.created || dateFromSlug(dir), updated: d.updated,
      title: `${vis.length} file${vis.length > 1 ? "s" : ""} rendered`, body: "", kind: "media", media: vis });
  }
  const calRows = calendar.filter((r) => (r["Asset link"] || "").includes(dir) || (r["Caption link"] || "").includes(dir));
  const named = calRows.map((r) => path.basename(r["Asset link"] || "")).filter(Boolean);
  for (const m of media) m.current = named.includes(path.basename(m.file)) || (!named.length && !/no-music|voice-only/.test(m.file));
  media.sort((x, y) => Number(y.current) - Number(x.current) || x.file.localeCompare(y.file));
  const status = calRows[0]?.Status || (verdict === "Approved" ? "Approved" : verdict ? "In review" : "Drafting");
  for (const r of calRows.filter((r) => r.Status === "Approved" || r.Status === "Posted" || r.Status === "Scheduled")) {
    if (!messages.some((m) => m.kind === "signoff")) messages.push({ file: "calendar", role: "Operator", created: `${r.Date}T${r["Time (WAT)"] || "09:00"}:00+01:00`, updated: "",
      title: `${r.Status}: ${r.Hook}`, body: `${r.Platform} · ${r.Date} ${r["Time (WAT)"]} WAT\n\n${r.Notes || ""}`.trim(), kind: "signoff" });
  }
  const channels = primaryCaptionsText ? parseChannelPosts(primaryCaptionsText, media, calRows, status) : [];
  // a slot that names no files: use the calendar's asset for that slot, else every visual in the folder
  const visuals = media.filter((m) => m.type !== "captions");
  for (const c of channels) if (!c.media.length) {
    const row = calRows.find((r) => r.Date === c.date && r["Time (WAT)"] === c.time);
    const named = row ? visuals.filter((m) => path.basename(m.file) === path.basename(row["Asset link"] || "")) : [];
    c.media = (named.length ? named : visuals.filter((m) => m.current)).map((m) => m.file);
  }
  const rank = (m) => ROLE_ORDER.indexOf(m.role) < 0 ? 99 : ROLE_ORDER.indexOf(m.role);
  messages.sort((a, b) => (a.created || "").slice(0, 10).localeCompare((b.created || "").slice(0, 10)) || rank(a) - rank(b) || (a.created || "").localeCompare(b.created || ""));
  const first = captionSets[0] || {};
  posts.push({
    slug: dir, date: dir.slice(0, 10), title, status, verdict,
    hook: first.hook || calRows[0]?.Hook || "", when: first.when || "",
    platforms: channels.length ? [...new Set(channels.map((c) => c.platform))].join(" · ") : first.platforms || calRows[0]?.Platform || "",
    pillar: first.pillar || calRows[0]?.Pillar || "", captionSets, channels, captionsFile: primaryCaptionsFile, media, messages, calendar: calRows,
  });
}

const plans = [];
for (const f of fs.readdirSync(POSTS).filter((f) => f.endsWith(".md") && f !== "README.md").sort()) {
  const text = read(path.join(POSTS, f));
  const rel = path.join("content/posts", f);
  const dates = fileDates(rel);
  plans.push({ slug: f.replace(/\.md$/, ""), date: f.slice(0, 10), title: titleOf(text, f), role: roleOf(text, f),
    created: dates.created || dateFromSlug(f), updated: dates.updated, body: stripHeader(text) });
}

const data = { generatedAt: new Date().toISOString(), posts: posts.sort((a, b) => b.date.localeCompare(a.date) || b.slug.localeCompare(a.slug)), plans, calendar };
fs.writeFileSync(path.join(DIST, "data.json"), JSON.stringify(data));
const mb = (n) => (n / 1048576).toFixed(1);
const total = posts.flatMap((p) => p.media).reduce((s, m) => s + m.bytes, 0);
console.log(`built ${posts.length} posts, ${plans.length} plans, ${posts.reduce((s, p) => s + p.media.length, 0)} media files (${mb(total)} MB) → web/dist`);
