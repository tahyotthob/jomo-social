/* JOMO Social Studio: a static viewer for the team's work. Data comes from data.json (built by build.mjs). */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const h = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const PLATFORMS = ["Instagram", "Facebook", "LinkedIn", "X"];
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
  const cover = (p) => (p.media.find((m) => /cover/.test(m.file) && m.type === "image") || p.media.find((m) => m.type === "image"))?.url;
  const toast = (t) => { const el = $("#toast"); el.textContent = t; el.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(() => (el.hidden = true), 1800); };
  const md = (text) => {
    if (!window.marked) return `<pre>${h(text)}</pre>`;
    let html = marked.parse(text || "", { gfm: true, breaks: false });
    html = html.replace(/\b(PASS|FIX|BLOCK|Approved)\b(?=[^<]*(<|$))/g, (m) => `<span class="v-${m.toLowerCase()}">${m}</span>`);
    return window.DOMPurify ? DOMPurify.sanitize(html) : html;
  };
  const avatar = (role) => { const [ini, col] = ROLE_STYLE[role] || [role.slice(0, 2).toUpperCase(), "#8e8e93"]; return `<div class="avatar" style="background:${col}" title="${h(role)}">${ini}</div>`; };
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
        html += `<a class="side-item ${statusClass(p.status)} ${page === "post" && id === p.slug ? "active" : ""}" href="#/post/${encodeURIComponent(p.slug)}">
          ${c ? `<img class="thumb" src="${c}" alt="" loading="lazy">` : `<div class="thumb ph">${h(p.platforms.includes("X") ? "X" : "—")}</div>`}
          <div><div class="t">${h(p.title)}</div><div class="s"><span class="dot"></span>${h(p.status)} · ${fmtDay(p.date + "T12:00:00+01:00")}</div></div></a>`;
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
    const feed = d.posts.flatMap((p) => p.messages.map((m) => ({ ...m, post: p }))).filter((m) => m.created).sort((a, b) => b.created.localeCompare(a.created)).slice(0, 12);
    $("#main").innerHTML = `<div class="wrap">
      <div class="hero"><h1>Everything the team has made.</h1><p>Threads from each role, the visuals and videos, and the captions ready to copy for every channel.</p></div>
      <div class="stats">
        <div class="stat"><div class="n">${d.posts.length}</div><div class="l">Posts in progress</div></div>
        <div class="stat"><div class="n">${approved}</div><div class="l">Approved</div></div>
        <div class="stat"><div class="n">${review}</div><div class="l">Waiting on review or sign-off</div></div>
        <div class="stat"><div class="n">${videos}</div><div class="l">Videos</div></div>
        <div class="stat"><div class="n">${files}</div><div class="l">Files ready to download</div></div>
      </div>
      <div class="section-title"><h2>Ready to post</h2><a href="#/posts" class="small">All posts</a></div>
      ${cardGrid(d.posts.filter((p) => /approved|posted|scheduled/i.test(p.status)), "Nothing approved yet. Approved posts appear here with their download kits.")}
      <div class="section-title"><h2>Latest activity</h2></div>
      <div class="feed">${feed.map((m) => `<a href="#/post/${encodeURIComponent(m.post.slug)}">${avatar(m.role)}<div><div class="t">${h(m.role)} · ${h(m.title)}</div><div class="s">${h(m.post.title)}</div></div><time>${h(fmtDay(m.created))}</time></a>`).join("")}</div>
      <div class="section-title"><h2>In the works</h2></div>
      ${cardGrid(d.posts.filter((p) => !/approved|posted|scheduled/i.test(p.status)), "No drafts right now.")}
    </div>`;
  }
  function cardGrid(posts, empty) {
    if (!posts.length) return `<div class="empty">${h(empty)}</div>`;
    return `<div class="cards">${posts.map((p) => { const c = cover(p); return `<a class="card" href="#/post/${encodeURIComponent(p.slug)}">
      ${c ? `<img class="cover" src="${c}" alt="" loading="lazy">` : `<div class="cover ph">${h(p.platforms || "Text post")}</div>`}
      <div class="cb"><div class="t">${h(p.title)}</div><div class="s">${badge(p.status)}<span>${h(fmtDay(p.date + "T12:00:00+01:00"))}</span></div></div></a>`; }).join("")}</div>`;
  }
  function renderPosts() {
    $(".shell").classList.add("no-inspector"); $("#inspector").innerHTML = "";
    $("#main").innerHTML = `<div class="wrap"><div class="page-head"><h1>Posts</h1><p class="muted">Every post folder in the repo, newest first.</p></div>${cardGrid(state.data.posts, "No posts yet.")}</div>`;
  }
  function renderSearch() {
    $(".shell").classList.add("no-inspector"); $("#inspector").innerHTML = "";
    const q = state.q.toLowerCase();
    const hits = state.data.posts.filter((p) => [p.title, p.hook, p.slug, p.pillar, p.platforms, ...p.captionSets.flatMap((s) => Object.values(s.captions)), ...p.messages.map((m) => m.body)].join(" ").toLowerCase().includes(q));
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
      else if (m.kind === "captions" && m.sets?.length) body = captionBlocks(m.sets);
      else body = `<div class="md ${long ? "clamp" : ""}" data-i="${i}">${md(m.body)}</div>${long ? `<button class="more" data-more="${i}">Show more</button>` : ""}`;
      return `${sep}<div class="msg ${m.role === "Operator" ? "operator" : ""}">${avatar(m.role)}<div class="bubble">
        <div class="who"><span class="r">${h(m.role)}</span><span class="ti">${h(m.title)}</span>${m.file && m.file.endsWith(".md") ? `<span class="file">${h(m.file)}</span>` : ""}<time>${h(fmtTime(m.created))}</time></div>${body}</div></div>`;
    }).join("");
    $("#main").innerHTML = `<div class="wrap">
      <div class="page-head"><div class="eyebrow">${h(p.pillar || "Post")}</div><h1>${h(p.title)}</h1>${p.hook ? `<div class="hook">${h(p.hook)}</div>` : ""}
        <div class="meta">${badge(p.status)}${p.when ? `<span>${h(p.when)}</span>` : `<span>${h(fmtDay(p.date + "T12:00:00+01:00"))}</span>`}${p.platforms ? `<span>${h(p.platforms)}</span>` : ""}</div>
        <div class="seg seg-mobile"><button class="active" data-pane="thread">Thread</button><button data-pane="content">Content</button></div></div>
      <div class="thread">${thread || `<div class="empty">No messages yet.</div>`}</div></div>`;
    renderInspector(p);
    $("#main").querySelectorAll("[data-more]").forEach((b) => b.addEventListener("click", () => { const el = $(`.md[data-i="${b.dataset.more}"]`); el.classList.toggle("clamp"); b.textContent = el.classList.contains("clamp") ? "Show more" : "Show less"; }));
    $("#main").querySelectorAll(".seg-mobile button").forEach((b) => b.addEventListener("click", () => { $(".shell").classList.toggle("show-inspector", b.dataset.pane === "content"); $(".seg-mobile .active").classList.remove("active"); b.classList.add("active"); }));
    bindMedia($("#main"));
    $("#main").querySelectorAll("[data-copy]").forEach((b) => b.addEventListener("click", () => copy(b.dataset.copy, "Caption copied")));
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

  // ---------- inspector: content and downloads
  function renderInspector(p) {
    const sets = p.captionSets;
    const videos = p.media.filter((m) => m.type === "video");
    const dl = (m) => `<a class="dl" href="${m.url}" download title="Download"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M10 3v10M6 9l4 4 4-4M4 16h12"/></svg></a>`;
    let html = `<div class="insp-title">Status</div><div class="kv">
      <dt>Status</dt><dd>${badge(p.status)}</dd>${p.verdict ? `<dt>Review</dt><dd>${badge(p.verdict)}</dd>` : ""}
      ${p.when ? `<dt>Slot</dt><dd>${h(p.when)}</dd>` : ""}${p.platforms ? `<dt>Platforms</dt><dd>${h(p.platforms)}</dd>` : ""}${p.pillar ? `<dt>Pillar</dt><dd>${h(p.pillar)}</dd>` : ""}</div>`;
    const watch = (videos.some((v) => v.current) ? videos.filter((v) => v.current) : videos).slice(0, 2);
    if (watch.length) html += `<div class="insp-title">Watch</div>` + watch.map((v) => `<div class="player"><video src="${v.url}" controls preload="metadata" playsinline poster="${poster(p, v)}"></video></div>`).join("");
    if (p.media.length) html += `<div class="insp-title">Files</div><div class="files">${p.media.map((m) => `<div class="file-row">${m.type === "image" ? `<img src="${m.url}" alt="">` : `<div class="ph">${m.type === "video" ? "MP4" : "SRT"}</div>`}<div><div class="n">${h(m.file)}${m.current && videos.length > 2 ? ` <span class="badge pass" style="padding:1px 7px;font-size:10px">current</span>` : ""}</div><div class="z">${mb(m.bytes)}</div></div>${dl(m)}</div>`).join("")}</div>`;
    if (sets.length) {
      html += `<div class="insp-title">Captions</div>`;
      if (sets.length > 1) html += `<div class="cap-tabs" data-sets>${sets.map((s, i) => `<button class="${i ? "" : "active"}" data-set="${i}">${h(s.heading || "Set " + (i + 1))}</button>`).join("")}</div>`;
      html += `<div id="capset"></div>`;
    }
    html += `<div class="kit"><button class="btn primary" id="kit">Download kit (.zip)</button><div class="note">Captions as text files per platform, alt text, every visual and video, and a README with the slot and status.</div></div>`;
    $("#inspector").innerHTML = html;
    $("#inspector").querySelectorAll("[data-set]").forEach((b) => b.addEventListener("click", () => { $(".cap-tabs .active", $("#inspector"))?.classList.remove("active"); b.classList.add("active"); renderCapSet(p, +b.dataset.set); }));
    if (sets.length) renderCapSet(p, 0);
    $("#kit").addEventListener("click", () => buildKit(p));
  }
  function renderCapSet(p, i) {
    const s = p.captionSets[i];
    const plats = [...PLATFORMS.filter((x) => s.captions[x]), ...Object.keys(s.captions).filter((x) => !PLATFORMS.includes(x))];
    const first = plats[0];
    const box = $("#capset");
    box.innerHTML = `<div class="cap-tabs" data-plats>${plats.map((x) => `<button class="${x === first ? "active" : ""}" data-plat="${h(x)}">${h(x)}</button>`).join("")}${s.altText ? `<button data-plat="__alt">Alt text</button>` : ""}</div>
      <div class="cap-box"><pre id="captext"></pre><div class="cap-actions"><button class="btn sm primary" id="copycap">Copy</button><button class="btn sm" id="dlcap">Download .txt</button></div></div>`;
    const show = (plat) => { const t = plat === "__alt" ? s.altText : s.captions[plat]; $("#captext").textContent = t; box.dataset.plat = plat; };
    box.querySelectorAll("[data-plat]").forEach((b) => b.addEventListener("click", () => { box.querySelector("[data-plats] .active")?.classList.remove("active"); b.classList.add("active"); show(b.dataset.plat); }));
    $("#copycap").addEventListener("click", () => copy($("#captext").textContent, "Caption copied"));
    $("#dlcap").addEventListener("click", () => dlText($("#captext").textContent, `${p.slug}-${box.dataset.plat === "__alt" ? "alt-text" : box.dataset.plat.toLowerCase()}.txt`));
    show(first);
  }
  async function buildKit(p) {
    const btn = $("#kit"); btn.disabled = true; btn.textContent = "Preparing…";
    try {
      const zip = new JSZip();
      const readme = [`${p.title}`, "".padEnd(p.title.length, "="), "", `Status: ${p.status}${p.verdict ? ` (review: ${p.verdict})` : ""}`, p.when ? `Slot: ${p.when}` : "", p.platforms ? `Platforms: ${p.platforms}` : "", p.pillar ? `Pillar: ${p.pillar}` : "", p.hook ? `Hook: ${p.hook}` : "", "",
        "Contents", "- captions/: one text file per platform, ready to paste", "- alt-text.txt: alt text for the visuals", "- media/: visuals and videos at platform sizes", "",
        "Posting checklist", "- Instagram and Facebook: Meta Business Suite planner; put the link in the bio for Instagram", "- LinkedIn: post as the JOMO page with the built-in scheduler", "- X: post by hand, under 280 characters", "- Add alt text on every platform that offers it", "",
        `Exported ${new Date().toISOString().slice(0, 16).replace("T", " ")} from JOMO Social Studio`].join("\n");
      zip.file("README.txt", readme);
      p.captionSets.forEach((s, i) => {
        const base = p.captionSets.length > 1 ? `${(s.heading || "set-" + (i + 1)).replace(/[^\w]+/g, "-").replace(/^-|-$/g, "").toLowerCase()}/` : "";
        for (const [plat, text] of Object.entries(s.captions)) zip.file(`${base}captions/${plat.toLowerCase()}.txt`, text + "\n");
        if (s.altText) zip.file(`${base}alt-text.txt`, s.altText + "\n");
      });
      for (const m of p.media) { const r = await fetch(m.url); zip.file(`media/${m.file}`, await r.blob()); }
      downloadBlob(await zip.generateAsync({ type: "blob" }), `${p.slug}-kit.zip`);
      toast("Kit downloaded");
    } catch (e) { console.error(e); toast("Could not build the kit"); }
    btn.disabled = false; btn.textContent = "Download kit (.zip)";
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
      <div class="tbl-wrap"><table class="table"><thead><tr>${cols.map((c) => `<th>${h(c)}</th>`).join("")}</tr></thead><tbody>${rows.map((r) => { const slug = (r["Asset link"] || r["Caption link"] || "").match(/content\/posts\/([^/]+)/)?.[1]; return `<tr>${cols.map((c) => `<td data-label="${h(c)}">${c === "Status" ? badge(r[c]) : c === "Hook" && slug ? `<a href="#/post/${encodeURIComponent(slug)}">${h(r[c])}</a>` : h(r[c])}</td>`).join("")}</tr>`; }).join("") || `<tr><td colspan="8" class="empty">The calendar is empty.</td></tr>`}</tbody></table></div></div>`;
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
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
