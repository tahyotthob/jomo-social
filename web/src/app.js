/* JOMO Social Studio: a static viewer for the team's work. Data comes from data.json (built by build.mjs). */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const h = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const PLATFORMS = ["Instagram", "Facebook", "LinkedIn", "X"];
  const PLATFORM_COLOR = { Instagram: "#d62976", Facebook: "#1877f2", LinkedIn: "#0a66c2", X: "#000000" };
  const POSTING = {
    Instagram: "Schedule in Meta Business Suite, or post in the Instagram app when it needs stickers. Links go in the bio, not the caption.",
    Facebook: "Schedule in Meta Business Suite. Links work in the caption.",
    LinkedIn: "Post as the JOMO page and use LinkedIn's scheduler.",
    X: "Post by hand. For a thread, post 1 with the image, then reply to it with each next post in order.",
  };
  const chip = (plat) => `<span class="chip" style="--c:${PLATFORM_COLOR[plat] || "#8e8e93"}">${h(plat)}</span>`;
  const slug = (s) => String(s || "").toLowerCase().replace(/[^\w]+/g, "-").replace(/^-|-$/g, "");
  const ROLE_STYLE = {
    "Editor-in-Chief": ["EC", "#1d1d1f"], "Analyst": ["AN", "#5e5ce6"], "Trend Scout": ["TS", "#0a84ff"], "Creative Director": ["CD", "#bf5af2"],
    "Copywriter": ["CW", "#7aa31e"], "Designer": ["DS", "#ff9f0a"], "Video Producer": ["VP", "#ff375f"], "Impact Storyteller": ["IS", "#ac8e68"],
    "Partnerships Liaison": ["PL", "#64d2ff"], "Fact-checker": ["FC", "#30b0c7"], "Policy and Safety Reviewer": ["PS", "#ffb800"],
    "Community Manager": ["CM", "#34c759"], "Operator": ["OL", "#4b6b0d"],
  };
  const state = { data: null, route: {}, q: "" };

  // ---------- utilities
  const fmtDay = (iso) => iso ? new Intl.DateTimeFormat("en-GB", { weekday: "short", day: "numeric", month: "short", timeZone: "Africa/Lagos" }).format(new Date(iso)) : "";
  const fmtTime = (iso) => iso ? new Intl.DateTimeFormat("en-GB", { hour: "2-digit", minute: "2-digit", timeZone: "Africa/Lagos" }).format(new Date(iso)) : "";
  const dayKey = (iso) => iso ? new Intl.DateTimeFormat("en-CA", { timeZone: "Africa/Lagos" }).format(new Date(iso)) : "";
  const statusClass = (s) => "st-" + String(s || "drafting").toLowerCase().replace(/\s+/g, "-");
  const badge = (s) => `<span class="badge ${h(String(s || "").toLowerCase().replace(/\s+/g, "-"))}">${h(s || "Drafting")}</span>`;
  const mb = (n) => n > 1048576 ? (n / 1048576).toFixed(1) + " MB" : Math.round(n / 1024) + " KB";
  // cover-video-a-motion.jpg is the poster for video-a-ycef-motion.mp4: same letter, same "motion" or not
  const poster = (p, v) => { const letter = (v.file.match(/video-([a-z])/) || [])[1]; const motion = /motion/.test(v.file);
    return (p.media.find((m) => m.type === "image" && /cover/.test(m.file) && (!letter || m.file.includes(`video-${letter}`)) && /motion/.test(m.file) === motion) || p.media.find((m) => m.type === "image" && /cover/.test(m.file)) || {}).url || ""; };
  // the first frame of a post: its cover, else slide 1, else the first image
  const cover = (p) => (p.media.find((m) => m.type === "image" && m.current && /cover/.test(m.file)) || p.media.find((m) => m.type === "image" && /cover/.test(m.file))
    || p.media.find((m) => m.type === "image" && /slide-01|image-/.test(m.file)) || p.media.find((m) => m.type === "image"))?.url;
  const toast = (t) => { const el = $("#toast"); el.textContent = t; el.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(() => (el.hidden = true), 1800); };
  const md = (text) => {
    if (!window.marked) return `<pre>${h(text)}</pre>`;
    let html = marked.parse(text || "", { gfm: true, breaks: false });
    html = html.replace(/\b(PASS|FIX|BLOCK|Approved)\b(?=[^<]*(<|$))/g, (m) => `<span class="v-${m.toLowerCase()}">${m}</span>`);
    return window.DOMPurify ? DOMPurify.sanitize(html) : html;
  };
  const avatar = (role) => { const [ini, col] = ROLE_STYLE[role] || [role.slice(0, 2).toUpperCase(), "#8e8e93"]; return `<div class="avatar" style="background:${col}" title="${h(role)}">${ini}</div>`; };
  // "today" is worked out in the browser in Lagos time, so the site changes over at midnight WAT without a rebuild.
  // ?day=YYYY-MM-DD pretends it is another day (handy for checking a future day's list).
  const todayKey = () => new URLSearchParams(location.search).get("day") || dayKey(new Date().toISOString());
  // a slot due today that is signed off but not yet marked Posted in the calendar shows as Pending
  const liveStatus = (status, date) => date && date === todayKey() && /^(approved|scheduled)$/i.test(status || "") ? "Pending" : status;
  const todayRows = () => state.data.calendar.filter((r) => r.Date === todayKey()).sort((a, b) => (a["Time (WAT)"] || "").localeCompare(b["Time (WAT)"] || ""));
  const pendingToday = () => todayRows().filter((r) => liveStatus(r.Status, r.Date) === "Pending");
  const postStatus = (p) => (p.channels?.length ? p.channels.some((c) => liveStatus(c.status, c.date) === "Pending") : p.calendar.some((r) => liveStatus(r.Status, r.Date) === "Pending")) ? "Pending" : p.status;
  const rowPost = (r) => { const slug = (r["Asset link"] || r["Caption link"] || "").match(/content\/posts\/([^/]+)/)?.[1]; return state.data.posts.find((p) => p.slug === slug); };
  const weekOf = (date) => { const d = new Date(date + "T12:00:00Z"); const day = (d.getUTCDay() + 6) % 7; d.setUTCDate(d.getUTCDate() - day); return d.toISOString().slice(0, 10); };
  const copy = async (text, label = "Copied") => { try { await navigator.clipboard.writeText(text); toast(label); } catch { toast("Copy failed"); } };
  const downloadBlob = (blob, name) => { const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 4000); };
  const dlText = (text, name) => downloadBlob(new Blob([text], { type: "text/plain;charset=utf-8" }), name);
  const setTheme = (t) => { if (t) document.documentElement.dataset.theme = t; else delete document.documentElement.dataset.theme; try { t ? localStorage.setItem("theme", t) : localStorage.removeItem("theme"); } catch {} };

  // ---------- routing
  function parseRoute() {
    const hash = location.hash.replace(/^#\/?/, "");
    const [page = "", id = ""] = hash.split("/");
    return { page: page || "home", id: decodeURIComponent(id) };
  }
  function render() {
    state.route = parseRoute();
    document.querySelectorAll("#nav a, #tabbar a").forEach((a) => a.classList.toggle("active", a.dataset.route === state.route.page || (state.route.page === "posts" && a.dataset.route === "post") || (state.route.page === "plans" && a.dataset.route === "plan")));
    document.body.classList.remove("menu-open");
    const shell = $(".shell");
    shell.classList.remove("no-inspector", "no-sidebar", "show-inspector");
    renderSidebar();
    const { page, id } = state.route;
    if (state.q) return renderSearch();
    if (page === "post" && id) return renderPost(id);
    if (page === "plan" && id) return renderPlan(id);
    if (page === "posts") return renderPosts();
    if (page === "plans") return renderPlans();
    if (page === "calendar") return renderCalendar();
    return renderHome();
  }

  // ---------- sidebar
  function renderSidebar() {
    const { page, id } = state.route;
    const posts = state.data.posts;
    const groups = {};
    for (const p of posts) (groups[weekOf(p.date)] ||= []).push(p);
    let html = `<div class="side-head">Posts</div>`;
    for (const wk of Object.keys(groups).sort().reverse()) {
      html += `<div class="side-group">Week of ${fmtDay(wk + "T12:00:00+01:00")}</div>`;
      for (const p of groups[wk]) {
        const c = cover(p);
        html += `<a class="side-item ${statusClass(postStatus(p))} ${page === "post" && id === p.slug ? "active" : ""}" href="#/post/${encodeURIComponent(p.slug)}">
          ${c ? `<img class="thumb" src="${c}" alt="" loading="lazy">` : `<div class="thumb ph">${h(p.platforms.includes("X") ? "X" : "—")}</div>`}
          <div><div class="t">${h(p.title)}</div><div class="s"><span class="dot"></span>${h(postStatus(p))} · ${fmtDay(p.date + "T12:00:00+01:00")}</div></div></a>`;
      }
    }
    if (state.data.plans.length) {
      html += `<div class="side-head" style="margin-top:18px">Plans and briefs</div>`;
      for (const p of state.data.plans) html += `<a class="side-item ${page === "plan" && id === p.slug ? "active" : ""}" href="#/plan/${encodeURIComponent(p.slug)}"><div class="thumb ph">${h(fmtDay(p.date + "T12:00:00+01:00").slice(0, 3))}</div><div><div class="t">${h(p.title)}</div><div class="s">${h(p.role)}</div></div></a>`;
    }
    $("#sidebar").innerHTML = html;
  }

  // ---------- home
  function renderHome() {
    const d = state.data;
    $(".shell").classList.add("no-inspector");
    $("#inspector").innerHTML = "";
    const approved = d.posts.filter((p) => /approved|posted|scheduled/i.test(p.status)).length;
    const review = d.posts.filter((p) => /review|fix|block/i.test(p.status + p.verdict) && !/approved|posted/i.test(p.status)).length;
    const files = d.posts.reduce((s, p) => s + p.media.length, 0);
    const videos = d.posts.reduce((s, p) => s + p.media.filter((m) => m.type === "video").length, 0);
    const today = todayRows(), pending = pendingToday();
    const feed = d.posts.flatMap((p) => p.messages.map((m) => ({ ...m, post: p }))).filter((m) => m.created).sort((a, b) => b.created.localeCompare(a.created)).slice(0, 12);
    $("#main").innerHTML = `<div class="wrap">
      <div class="section-title first"><h2>Today · ${h(fmtDay(todayKey() + "T12:00:00+01:00"))}</h2><span class="small muted">${pending.length ? `${pending.length} pending` : today.length ? "All done" : ""}</span></div>
      ${todayList(today)}
      <div class="hero"><h1>Everything the team has made.</h1><p>Threads from each role, the visuals and videos, and the captions ready to copy for every channel.</p></div>
      <div class="stats">
        <div class="stat"><div class="n">${d.posts.length}</div><div class="l">Posts in progress</div></div>
        <div class="stat"><div class="n">${approved}</div><div class="l">Approved</div></div>
        <div class="stat"><div class="n">${review}</div><div class="l">Waiting on review or sign-off</div></div>
        <div class="stat"><div class="n">${videos}</div><div class="l">Videos</div></div>
        <div class="stat"><div class="n">${files}</div><div class="l">Files ready to download</div></div>
      </div>
      <div class="section-title"><h2>Ready to post</h2><a href="#/posts" class="small">All posts</a></div>
      ${cardGrid(d.posts.filter((p) => /approved|posted|scheduled/i.test(p.status)).sort((a, b) => (postStatus(b) === "Pending") - (postStatus(a) === "Pending")), "Nothing approved yet. Approved posts appear here with their download kits.")}
      <div class="section-title"><h2>Latest activity</h2></div>
      <div class="feed">${feed.map((m) => `<a href="#/post/${encodeURIComponent(m.post.slug)}">${avatar(m.role)}<div><div class="t">${h(m.role)} · ${h(m.title)}</div><div class="s">${h(m.post.title)}</div></div><time>${h(fmtDay(m.created))}</time></a>`).join("")}</div>
      <div class="section-title"><h2>In the works</h2></div>
      ${cardGrid(d.posts.filter((p) => !/approved|posted|scheduled/i.test(p.status)), "No drafts right now.")}
    </div>`;
  }
  // today's calendar slots, in posting order; each links to its post
  function todayList(rows) {
    if (!rows.length) return `<div class="empty">Nothing on the calendar for today.</div>`;
    return `<div class="feed today">${rows.map((r) => {
      const p = rowPost(r), st = liveStatus(r.Status, r.Date);
      const asset = p && p.media.find((m) => `content/posts/${p.slug}/${m.file}` === r["Asset link"]);
      const img = asset?.type === "image" ? asset.url : asset?.type === "video" ? poster(p, asset) || cover(p) : p && cover(p);
      const plats = PLATFORMS.filter((x) => new RegExp(x === "X" ? "(^|[^a-z])x([^a-z]|$)" : x, "i").test(r.Platform));
      const note = st === "Pending" ? "Signed off. Post it, then mark it Posted in the calendar." : /posted/i.test(st) ? "Posted." : "Not signed off yet: it can't go out until the operator approves it.";
      return `<a class="${statusClass(st)}" href="${p ? `#/post/${encodeURIComponent(p.slug)}` : "#/calendar"}">
        ${img ? `<img class="thumb" src="${img}" alt="" loading="lazy">` : `<div class="thumb ph">${h(plats[0] || "—")}</div>`}
        <div><div class="t">${h(r.Hook.replace(/~~[^~]*~~\s*/g, ""))}</div><div class="s">${plats.map(chip).join(" ")} <span>${h(r.Format)}</span></div><div class="s">${h(note)}</div></div>
        <div class="tr"><time>${h(r["Time (WAT)"] || "")}${r["Time (WAT)"] ? " WAT" : ""}</time>${badge(st)}</div></a>`; }).join("")}</div>`;
  }
  function cardGrid(posts, empty) {
    if (!posts.length) return `<div class="empty">${h(empty)}</div>`;
    return `<div class="cards">${posts.map((p) => { const c = cover(p); return `<a class="card" href="#/post/${encodeURIComponent(p.slug)}">
      ${c ? `<img class="cover" src="${c}" alt="" loading="lazy">` : `<div class="cover ph">${h(p.platforms || "Text post")}</div>`}
      <div class="cb"><div class="t">${h(p.title)}</div><div class="s">${badge(postStatus(p))}<span>${h(fmtDay(p.date + "T12:00:00+01:00"))}</span></div></div></a>`; }).join("")}</div>`;
  }
  function renderPosts() {
    $(".shell").classList.add("no-inspector"); $("#inspector").innerHTML = "";
    $("#main").innerHTML = `<div class="wrap"><div class="page-head"><h1>Posts</h1><p class="muted">Every post folder in the repo, newest first.</p></div>${cardGrid(state.data.posts, "No posts yet.")}</div>`;
  }
  function renderSearch() {
    $(".shell").classList.add("no-inspector"); $("#inspector").innerHTML = "";
    const q = state.q.toLowerCase();
    const hits = state.data.posts.filter((p) => [p.title, p.hook, p.slug, p.pillar, p.platforms, ...p.captionSets.flatMap((s) => Object.values(s.captions)), ...(p.channels || []).flatMap((c) => c.variants.map((v) => v.text)), ...p.messages.map((m) => m.body)].join(" ").toLowerCase().includes(q));
    $("#main").innerHTML = `<div class="wrap"><div class="page-head"><h1>Results for “${h(state.q)}”</h1><p class="muted">${hits.length} post${hits.length === 1 ? "" : "s"}</p></div>${cardGrid(hits, "Nothing matches.")}</div>`;
  }

  // ---------- post thread
  function renderPost(slug) {
    const p = state.data.posts.find((x) => x.slug === slug);
    if (!p) { $("#main").innerHTML = `<div class="empty">Post not found.</div>`; return; }
    let lastDay = "";
    const thread = p.messages.map((m, i) => {
      const k = dayKey(m.created);
      const sep = k && k !== lastDay ? `<div class="day">${h(fmtDay(m.created))}</div>` : "";
      lastDay = k || lastDay;
      const long = (m.body || "").length > 1800;
      let body = "";
      if (m.kind === "media") body = mediaGrid(m.media);
      else if (m.kind === "captions" && m.file === p.captionsFile && p.channels?.length) body = channelSummary(p);
      else if (m.kind === "captions" && m.sets?.length) body = captionBlocks(m.sets);
      else body = `<div class="md ${long ? "clamp" : ""}" data-i="${i}">${md(m.body)}</div>${long ? `<button class="more" data-more="${i}">Show more</button>` : ""}`;
      return `${sep}<div class="msg ${m.role === "Operator" ? "operator" : ""}">${avatar(m.role)}<div class="bubble">
        <div class="who"><span class="r">${h(m.role)}</span><span class="ti">${h(m.title)}</span>${m.file && m.file.endsWith(".md") ? `<span class="file">${h(m.file)}</span>` : ""}<time>${h(fmtTime(m.created))}</time></div>${body}</div></div>`;
    }).join("");
    $("#main").innerHTML = `<div class="wrap">
      <div class="page-head"><div class="eyebrow">${h(p.pillar || "Post")}</div><h1>${h(p.title)}</h1>${p.hook ? `<div class="hook">${h(p.hook)}</div>` : ""}
        <div class="meta">${badge(postStatus(p))}${p.when ? `<span>${h(p.when)}</span>` : `<span>${h(fmtDay(p.date + "T12:00:00+01:00"))}</span>`}${p.platforms ? `<span>${h(p.platforms)}</span>` : ""}</div>
        <div class="seg seg-mobile"><button class="active" data-pane="thread">Thread</button><button data-pane="content">Content</button></div></div>
      <div class="thread">${thread || `<div class="empty">No messages yet.</div>`}</div></div>`;
    renderInspector(p);
    $("#main").querySelectorAll("[data-more]").forEach((b) => b.addEventListener("click", () => { const el = $(`.md[data-i="${b.dataset.more}"]`); el.classList.toggle("clamp"); b.textContent = el.classList.contains("clamp") ? "Show more" : "Show less"; }));
    $("#main").querySelectorAll(".seg-mobile button").forEach((b) => b.addEventListener("click", () => { $(".shell").classList.toggle("show-inspector", b.dataset.pane === "content"); $(".seg-mobile .active").classList.remove("active"); b.classList.add("active"); }));
    bindMedia($("#main"));
    $("#main").querySelectorAll("[data-copy]").forEach((b) => b.addEventListener("click", () => copy(b.dataset.copy, "Caption copied")));
  }
  // one block per channel post in the thread: never two platforms in one block
  function channelSummary(p) {
    return p.channels.map((c) => `<div class="capset"><div class="cs-head">${chip(c.platform)} ${h(c.format || fmtOf(p, c))}${c.group ? ` <span class="cs-group">${h(c.group)}</span>` : ""}</div>
      <div class="cs-meta">${h([c.when, c.pillar].filter(Boolean).join(" · "))}</div>
      ${c.variants.map((v) => `<div class="cs-block"><div class="cs-label">${h(c.platform)}${v.label && v.label !== c.format ? ` · ${h(v.label)}` : ""}<button class="cs-copy" data-copy="${h(v.text)}">Copy</button></div><pre>${h(v.text)}</pre></div>`).join("")
        || `<div class="cs-block"><div class="cs-label">${h(c.platform)}</div><pre>No caption: the text is on the image.${c.visual ? " " + h(c.visual) : ""}</pre></div>`}</div>`).join("");
  }
  function captionBlocks(sets) {
    return sets.map((st) => `<div class="capset">${sets.length > 1 ? `<div class="cs-head">${h(st.heading)}</div>` : ""}
      ${st.when || st.platforms ? `<div class="cs-meta">${h([st.when, st.platforms, st.pillar].filter(Boolean).join(" · "))}</div>` : ""}
      ${st.hook ? `<div class="cs-hook">${h(st.hook)}</div>` : ""}
      ${[...PLATFORMS.filter((x) => st.captions[x]), ...Object.keys(st.captions).filter((x) => !PLATFORMS.includes(x))].map((plat) => `<div class="cs-block"><div class="cs-label">${h(plat)}<button class="cs-copy" data-copy="${h(st.captions[plat])}">Copy</button></div><pre>${h(st.captions[plat])}</pre></div>`).join("")}
      ${st.altText ? `<div class="cs-block"><div class="cs-label">Alt text<button class="cs-copy" data-copy="${h(st.altText)}">Copy</button></div><pre>${h(st.altText)}</pre></div>` : ""}</div>`).join("");
  }
  function mediaGrid(media) {
    return `<div class="media-grid">${media.map((m) => m.type === "video"
      ? `<div class="mi vid" data-src="${m.url}" data-type="video"><video src="${m.url}#t=0.5" preload="metadata" muted playsinline></video><div class="cap">${h(m.file)}</div></div>`
      : `<div class="mi" data-src="${m.url}" data-type="image"><img src="${m.url}" alt="${h(m.file)}" loading="lazy"><div class="cap">${h(m.file)}</div></div>`).join("")}</div>`;
  }
  function bindMedia(root) {
    root.querySelectorAll(".mi[data-src]").forEach((el) => el.addEventListener("click", () => openLightbox(el.dataset.src, el.dataset.type)));
  }
  function openLightbox(src, type) {
    const lb = $("#lightbox"); const body = $(".lb-body", lb);
    body.innerHTML = type === "video" ? `<video src="${src}" controls autoplay playsinline></video>` : `<img src="${src}" alt="">`;
    lb.hidden = false;
  }

  // ---------- inspector: one card per channel post, each with its own caption and kit
  const fmtOf = (p, c) => { const ms = mediaOf(p, c); return ms.some((m) => m.type === "video") ? "Video" : ms.length > 1 ? `Carousel, ${ms.length} slides` : ms.length ? "Image" : "Text"; };
  const mediaOf = (p, c) => c.media.map((f) => p.media.find((m) => m.file === f)).filter(Boolean);
  const slotLabel = (c) => c.date ? `${fmtDay(c.date + "T12:00:00+01:00")}${c.time ? " · " + c.time + " WAT" : ""}` : c.when;
  const dl = (m) => `<a class="dl" href="${m.url}" download title="Download ${h(m.file)}"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M10 3v10M6 9l4 4 4-4M4 16h12"/></svg></a>`;
  function renderInspector(p) {
    const videos = p.media.filter((m) => m.type === "video");
    const chans = p.channels || [];
    let html = `<div class="insp-title">Status</div><div class="kv">
      <dt>Status</dt><dd>${badge(postStatus(p))}</dd>${p.verdict ? `<dt>Review</dt><dd>${badge(p.verdict)}</dd>` : ""}
      ${chans.length ? `<dt>Channel posts</dt><dd>${chans.length}</dd>` : ""}${p.pillar ? `<dt>Pillar</dt><dd>${h(p.pillar)}</dd>` : ""}</div>`;
    const watch = (videos.some((v) => v.current) ? videos.filter((v) => v.current) : videos).slice(0, 2);
    if (watch.length) html += `<div class="insp-title">Watch</div>` + watch.map((v) => `<div class="player"><video src="${v.url}" controls preload="metadata" playsinline poster="${poster(p, v)}"></video></div>`).join("");
    if (chans.length) {
      const plats = PLATFORMS.filter((x) => chans.some((c) => c.platform === x));
      html += `<div class="insp-title">Posts by channel</div>`;
      if (plats.length > 1) html += `<div class="cap-tabs" data-filter><button class="active" data-f="">All ${chans.length}</button>${plats.map((x) => `<button data-f="${h(x)}">${h(x)} ${chans.filter((c) => c.platform === x).length}</button>`).join("")}</div>`;
      html += `<div class="chans">${chans.map((c, i) => channelCard(p, c, i)).join("")}</div>`;
      html += `<div class="kit"><button class="btn" id="kit-all">Download all ${chans.length} channel kits (.zip)</button><div class="note">One folder per channel post, each with its own caption, alt text, visuals and posting notes. Shared images are copied into every folder that uses them.</div></div>`;
    }
    if (p.media.length) html += `<details class="allfiles"><summary class="insp-title">All files in this post (${p.media.length})</summary><div class="files">${p.media.map((m) => `<div class="file-row">${m.type === "image" ? `<img src="${m.url}" alt="">` : `<div class="ph">${m.type === "video" ? "MP4" : "SRT"}</div>`}<div><div class="n">${h(m.file)}</div><div class="z">${mb(m.bytes)}</div></div>${dl(m)}</div>`).join("")}</div></details>`;
    if (!chans.length) html += `<div class="kit"><button class="btn primary" id="kit-all">Download kit (.zip)</button><div class="note">Every visual and video in this post.</div></div>`;
    const ins = $("#inspector");
    ins.innerHTML = html;
    ins.querySelectorAll("[data-f]").forEach((b) => b.addEventListener("click", () => {
      ins.querySelector("[data-filter] .active")?.classList.remove("active"); b.classList.add("active");
      ins.querySelectorAll(".chan").forEach((el) => (el.hidden = !!b.dataset.f && el.dataset.platform !== b.dataset.f));
    }));
    ins.querySelectorAll(".chan").forEach((el) => bindChannel(p, chans[+el.dataset.i], el));
    bindMedia(ins);
    $("#kit-all").addEventListener("click", (e) => buildKit(p, chans, e.currentTarget));
  }
  function channelCard(p, c, i) {
    const ms = mediaOf(p, c);
    const fmt = c.format || fmtOf(p, c);
    const tabs = c.variants.length > 1 ? `<div class="cap-tabs">${c.variants.map((v, k) => `<button class="${k ? "" : "active"}" data-v="${k}">${h(v.label || "Caption " + (k + 1))}</button>`).join("")}</div>` : "";
    return `<section class="chan" data-i="${i}" data-platform="${h(c.platform)}" style="--c:${PLATFORM_COLOR[c.platform] || "#8e8e93"}">
      <header><div class="ch-top">${chip(c.platform)}<span class="ch-fmt">${h(fmt)}</span>${badge(liveStatus(c.status, c.date))}</div>
        <div class="ch-slot">${h(slotLabel(c))}${c.group ? ` · ${h(c.group)}` : ""}</div></header>
      ${ms.length ? `<div class="ch-media">${ms.map((m) => m.type === "video"
        ? `<div class="mi vid" data-src="${m.url}" data-type="video"><video src="${m.url}#t=0.5" preload="metadata" muted playsinline></video></div>`
        : `<div class="mi" data-src="${m.url}" data-type="image"><img src="${m.url}" alt="${h(m.file)}" loading="lazy"></div>`).join("")}</div>
        <div class="ch-files">${ms.map((m) => `<span>${h(m.file.split("/").pop())}${dl(m)}</span>`).join("")}</div>` : `<div class="note">No visual: text only.</div>`}
      ${tabs}
      ${c.variants.length ? `<div class="cap-box"><div class="ch-label">${h(c.platform)} caption</div><pre class="ch-text"></pre>
        <div class="cap-actions"><button class="btn sm primary" data-act="copy">Copy caption</button><button class="btn sm" data-act="txt">.txt</button></div></div>`
        : `<div class="cap-box"><div class="ch-label">No caption</div><pre>The text is on the image.</pre></div>`}
      ${c.thread.length ? `<details class="ch-more"><summary>Copy one post at a time</summary>${c.thread.map((t, k) => `<div class="cs-block"><div class="cs-label">Post ${k + 1} of ${c.thread.length}<button class="cs-copy" data-copy="${h(t)}">Copy</button></div><pre>${h(t)}</pre></div>`).join("")}</details>` : ""}
      ${c.altText ? `<details class="ch-more"><summary>Alt text</summary><div class="cs-block"><div class="cs-label">Alt text<button class="cs-copy" data-copy="${h(c.altText)}">Copy</button></div><pre>${h(c.altText)}</pre></div></details>` : ""}
      ${c.visual ? `<details class="ch-more"${c.variants.length ? "" : " open"}><summary>Posting notes</summary><div class="note ch-notes">${h(c.visual)}</div></details>` : ""}
      <button class="btn sm ch-kit" data-act="kit">Download ${h(c.platform)} kit (.zip)</button>
    </section>`;
  }
  function bindChannel(p, c, el) {
    let v = 0;
    const show = () => { const pre = el.querySelector(".ch-text"); if (pre) pre.textContent = c.variants[v]?.text || ""; };
    el.querySelectorAll("[data-v]").forEach((b) => b.addEventListener("click", () => { el.querySelector("[data-v].active")?.classList.remove("active"); b.classList.add("active"); v = +b.dataset.v; show(); }));
    el.querySelector('[data-act="copy"]')?.addEventListener("click", () => copy(c.variants[v].text, `${c.platform} caption copied`));
    el.querySelector('[data-act="txt"]')?.addEventListener("click", () => dlText(c.variants[v].text, `${p.slug}-${c.id}${c.variants.length > 1 ? "-" + slug(c.variants[v].label) : ""}.txt`));
    el.querySelectorAll("[data-copy]").forEach((b) => b.addEventListener("click", () => copy(b.dataset.copy, "Copied")));
    el.querySelector('[data-act="kit"]').addEventListener("click", (e) => buildKit(p, [c], e.currentTarget));
    show();
  }
  // a kit holds exactly one channel post per folder; several channels → one folder each
  async function addChannel(zip, p, c, base) {
    const ms = mediaOf(p, c);
    const readme = [`${p.title}: ${c.platform}${c.format ? ` (${c.format})` : ""}`, "".padEnd(40, "="), "",
      `Channel: ${c.platform}`, `Format: ${c.format || fmtOf(p, c)}`, `Slot: ${c.when || "not set"}`, `Status: ${liveStatus(c.status, c.date)}`, !!c.group && `Part of: ${c.group}`, !!c.pillar && `Pillar: ${c.pillar}`, !!c.hook && `Hook: ${c.hook}`, "",
      "Files", ...(c.variants.length ? c.variants.map((v) => `- ${c.variants.length > 1 ? `caption-${slug(v.label)}.txt` : "caption.txt"}: the ${c.platform} caption${v.label ? ` (${v.label})` : ""}, ready to paste`) : ["- no caption: the text is on the image"]),
      c.thread.length && `- thread/: posts 1 to ${c.thread.length}, one file each, in posting order`,
      !!c.altText && "- alt-text.txt: alt text for the visuals", ...ms.map((m) => `- media/${m.file.split("/").pop()}`), "",
      "How to post", `- ${POSTING[c.platform] || "Post as planned."}`, "- Add the alt text where the platform offers it.", !!c.visual && `- Notes: ${c.visual}`, "",
      `Exported ${new Date().toLocaleString("en-GB", { timeZone: "Africa/Lagos", dateStyle: "medium", timeStyle: "short" })} WAT from JOMO Social Studio`].filter((x) => typeof x === "string").join("\n");
    zip.file(`${base}README.txt`, readme + "\n");
    c.variants.forEach((v) => zip.file(`${base}${c.variants.length > 1 ? `caption-${slug(v.label)}` : "caption"}.txt`, v.text + "\n"));
    c.thread.forEach((t, k) => zip.file(`${base}thread/post-${k + 1}-of-${c.thread.length}.txt`, t + "\n"));
    if (c.altText) zip.file(`${base}alt-text.txt`, c.altText + "\n");
    for (const m of ms) zip.file(`${base}media/${m.file.split("/").pop()}`, await (await fetch(m.url)).blob());
  }
  async function buildKit(p, chans, btn) {
    const label = btn.textContent; btn.disabled = true; btn.textContent = "Preparing…";
    try {
      const zip = new JSZip();
      let name;
      if (!chans.length) { for (const m of p.media) zip.file(`media/${m.file}`, await (await fetch(m.url)).blob()); name = `${p.slug}-kit.zip`; }
      else if (chans.length === 1) { await addChannel(zip, p, chans[0], ""); name = `${p.slug}-${chans[0].id}-kit.zip`; }
      else { for (const c of chans) await addChannel(zip, p, c, `${c.id}/`); name = `${p.slug}-all-channels-kit.zip`; }
      downloadBlob(await zip.generateAsync({ type: "blob" }), name);
      toast(chans.length === 1 ? `${chans[0].platform} kit downloaded` : "Kit downloaded");
    } catch (e) { console.error(e); toast("Could not build the kit"); }
    btn.disabled = false; btn.textContent = label;
  }

  // ---------- plans and calendar
  function renderPlans() {
    $(".shell").classList.add("no-inspector"); $("#inspector").innerHTML = "";
    $("#main").innerHTML = `<div class="wrap"><div class="page-head"><h1>Plans and briefs</h1><p class="muted">Weekly plans, creative briefs and sign-off packs.</p></div>
      <div class="feed">${state.data.plans.map((p) => `<a href="#/plan/${encodeURIComponent(p.slug)}">${avatar(p.role)}<div><div class="t">${h(p.title)}</div><div class="s">${h(p.role)}</div></div><time>${h(fmtDay(p.created))}</time></a>`).join("") || `<div class="empty">No plans yet.</div>`}</div></div>`;
  }
  function renderPlan(slug) {
    const p = state.data.plans.find((x) => x.slug === slug);
    $(".shell").classList.add("no-inspector"); $("#inspector").innerHTML = "";
    if (!p) { $("#main").innerHTML = `<div class="empty">Not found.</div>`; return; }
    $("#main").innerHTML = `<div class="wrap"><div class="page-head"><div class="eyebrow">${h(p.role)}</div><h1>${h(p.title)}</h1><div class="meta"><span>${h(fmtDay(p.created))}</span><span class="mono">${h(p.slug)}.md</span></div></div>
      <div class="thread"><div class="msg">${avatar(p.role)}<div class="bubble"><div class="md">${md(p.body)}</div></div></div></div></div>`;
  }
  function renderCalendar() {
    $(".shell").classList.add("no-inspector"); $("#inspector").innerHTML = "";
    const rows = state.data.calendar;
    const cols = ["Date", "Time (WAT)", "Platform", "Pillar", "Hook", "Format", "Status", "Notes"];
    $("#main").innerHTML = `<div class="wrap"><div class="page-head"><h1>Calendar</h1><p class="muted">content/calendar/calendar.csv, the source of truth for what is planned and posted.</p></div>
      <div class="tbl-wrap"><table class="table"><thead><tr>${cols.map((c) => `<th>${h(c)}</th>`).join("")}</tr></thead><tbody>${rows.map((r) => { const slug = (r["Asset link"] || r["Caption link"] || "").match(/content\/posts\/([^/]+)/)?.[1]; return `<tr class="${r.Date === todayKey() ? "is-today" : ""}">${cols.map((c) => `<td data-label="${h(c)}">${c === "Status" ? badge(liveStatus(r[c], r.Date)) : c === "Hook" && slug ? `<a href="#/post/${encodeURIComponent(slug)}">${h(r[c])}</a>` : h(r[c])}</td>`).join("")}</tr>`; }).join("") || `<tr><td colspan="8" class="empty">The calendar is empty.</td></tr>`}</tbody></table></div></div>`;
  }

  // ---------- boot
  async function boot() {
    try { const t = localStorage.getItem("theme"); if (t) setTheme(t); } catch {}
    $("#theme").addEventListener("click", () => { const dark = matchMedia("(prefers-color-scheme: dark)").matches; const cur = document.documentElement.dataset.theme || (dark ? "dark" : "light"); setTheme(cur === "dark" ? "light" : "dark"); });
    $("#menu").addEventListener("click", () => document.body.classList.toggle("menu-open"));
    $("#scrim").addEventListener("click", () => document.body.classList.remove("menu-open"));
    $("#lightbox").addEventListener("click", (e) => { if (e.target === e.currentTarget || e.target.classList.contains("close")) { $("#lightbox").hidden = true; $(".lb-body").innerHTML = ""; } });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") { $("#lightbox").hidden = true; $(".lb-body").innerHTML = ""; } });
    $("#q").addEventListener("input", (e) => { state.q = e.target.value.trim(); render(); });
    window.addEventListener("hashchange", () => { state.q = ""; $("#q").value = ""; render(); });
    const res = await fetch("data.json", { cache: "no-cache" });
    state.data = await res.json();
    render();
    const n = pendingToday().length;
    if (n) toast(`${n} post${n === 1 ? "" : "s"} pending today`);
    // roll over to the next day's list at midnight WAT if the page stays open
    let day = todayKey();
    setInterval(() => { if (todayKey() !== day) { day = todayKey(); render(); } }, 60000);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
