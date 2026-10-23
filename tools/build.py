"""Build JOMO slides as HTML files; render.js turns them into PNGs."""
import os, pathlib

ROOT = pathlib.Path(__file__).parent
FS = ROOT / "node_modules/@fontsource"
OUT = ROOT / "html"
OUT.mkdir(exist_ok=True)

INK, LIME, LEAF, OLIVE, CHAR, OFF = "#1E2220", "#A5CD39", "#8FB73C", "#77962A", "#323534", "#F4F6EC"

CSS = f"""
@font-face {{ font-family: Anton; src: url('file://{FS}/anton/files/anton-latin-400-normal.woff2'); }}
@font-face {{ font-family: Brico; font-weight: 800; src: url('file://{FS}/bricolage-grotesque/files/bricolage-grotesque-latin-800-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 400; src: url('file://{FS}/lato/files/lato-latin-400-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 700; src: url('file://{FS}/lato/files/lato-latin-700-normal.woff2'); }}
@font-face {{ font-family: Lato; font-weight: 900; src: url('file://{FS}/lato/files/lato-latin-900-normal.woff2'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:var(--w); height:var(--h); overflow:hidden; font-family:Lato; }}
.s {{ position:relative; width:var(--w); height:var(--h); padding:90px 90px 0; overflow:hidden; }}
.ink {{ background:{INK}; color:{OFF}; }}
.lime {{ background:{LIME}; color:{INK}; }}
.off {{ background:{OFF}; color:{INK}; }}
.label {{ font-weight:900; font-size:26px; letter-spacing:.22em; text-transform:uppercase; }}
.ink .label {{ color:{LIME}; }}
.lime .label, .off .label {{ color:{INK}; opacity:.75; }}
.off .label {{ color:{OLIVE}; opacity:1; }}
.h {{ font-family:Anton; text-transform:uppercase; line-height:.98; letter-spacing:.005em; }}
.acc {{ color:{LIME}; }}
.off .acc {{ color:{OLIVE}; }}
.lime .acc {{ color:{OFF}; }}
.body {{ font-size:40px; line-height:1.35; font-weight:400; }}
.foot {{ position:absolute; left:90px; right:90px; bottom:0; height:120px; display:flex; align-items:center;
        justify-content:space-between; font-weight:700; font-size:26px; letter-spacing:.04em; border-top:2px solid currentColor; }}
.ink .foot {{ border-color:rgba(244,246,236,.25); }}
.lime .foot, .off .foot {{ border-color:rgba(30,34,32,.25); }}
.foot .icons {{ display:flex; gap:14px; align-items:center; }}
.foot svg {{ width:34px; height:34px; }}
.count {{ font-weight:900; letter-spacing:.2em; font-size:22px; opacity:.7; }}
.tape {{ position:absolute; font-weight:900; font-size:30px; letter-spacing:.2em; padding:18px 40px;
         text-transform:uppercase; white-space:nowrap; }}
.stamp {{ position:absolute; border-radius:50%; display:flex; align-items:center; justify-content:center; text-align:center;
          font-weight:900; text-transform:uppercase; letter-spacing:.12em; }}
.brico {{ font-family:Brico; font-weight:800; line-height:.95; letter-spacing:-.02em; }}
"""

def icons(color):
    ig = f'<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="{color}" stroke="none"/></svg>'
    li = f'<svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="4" fill="{color}"/><rect x="6" y="10" width="2.6" height="8" fill="BG"/><circle cx="7.3" cy="6.9" r="1.6" fill="BG"/><path d="M11 10h2.5v1.2c.5-.8 1.5-1.4 2.8-1.4 2 0 3 1.2 3 3.6V18h-2.6v-4.2c0-1.2-.4-1.9-1.4-1.9s-1.7.7-1.7 1.9V18H11z" fill="BG"/></svg>'
    return ig, li

def foot(theme, n, total):
    color = OFF if theme == "ink" else INK
    bg = {"ink": INK, "lime": LIME, "off": OFF}[theme]
    ig, li = icons(color)
    li = li.replace("BG", bg)
    count = f'<span class="count">{n:02d} / {total:02d}</span>' if total else ""
    return f'<div class="foot"><div class="icons">{ig}{li}<span>@jomoclimate</span></div>{count}</div>'

def sprout(size, color1=LIME, color2=LEAF, extra=""):
    # two-leaf sprout, echoing the logo
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 200 200" style="position:absolute;{extra}">
      <path d="M100 150 C60 150 15 120 5 70 C55 65 95 95 100 150Z" fill="{color1}"/>
      <path d="M100 150 C5 70 5 70 5 70" stroke="{color2}" stroke-width="0"/>
      <path d="M100 150 L5 70 C55 65 95 95 100 150Z" fill="{color2}" opacity=".55"/>
      <path d="M100 150 C100 95 135 40 195 20 C200 80 160 140 100 150Z" fill="{color1}"/>
      <path d="M100 150 L195 20 C200 80 160 140 100 150Z" fill="{color2}" opacity=".55"/>
    </svg>'''

def page(body, theme, n, total, w=1080, h=1350):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}</style></head>
<body><div class="s {theme}">{body}{foot(theme, n, total)}</div></body></html>"""

def write(name, html):
    (OUT / f"{name}.html").write_text(html)

# ---------------- Flood carousel (IG + FB, 1080x1350) ----------------
T = 6
write("flood-01", page(f"""
  <div class="label">Climate, explained locally</div>
  <div class="h" style="font-size:150px;margin-top:70px">Floods<br>don't start<br>when <span class="acc">the</span><br><span class="acc">rain does.</span></div>
  {sprout(420, extra="right:-70px;bottom:150px;transform:rotate(-12deg);opacity:.95")}
  <div class="tape" style="background:{LIME};color:{INK};left:90px;bottom:190px;transform:rotate(-4deg)">Swipe &rarr;</div>
""", "ink", 1, T))

grate = f'''<svg width="900" height="430" viewBox="0 0 900 430" style="position:absolute;left:90px;bottom:170px">
  <rect x="0" y="40" width="900" height="360" rx="28" fill="{INK}"/>
  {''.join(f'<rect x="{60+i*82}" y="90" width="44" height="260" rx="14" fill="#0f1210"/>' for i in range(10))}
  <rect x="120" y="120" width="190" height="96" rx="10" fill="{OFF}" transform="rotate(-14 215 168)"/>
  <rect x="140" y="146" width="150" height="14" rx="4" fill="{OLIVE}" transform="rotate(-14 215 168)"/>
  <rect x="380" y="70" width="90" height="250" rx="40" fill="{LEAF}" opacity=".9" transform="rotate(22 425 195)"/>
  <rect x="408" y="44" width="34" height="40" rx="8" fill="{OFF}" transform="rotate(22 425 195)"/>
  <path d="M600 230 q60 -90 140 -20 q40 40 -30 90 q-80 50 -110 -70z" fill="{OFF}" opacity=".85"/>
  <rect x="520" y="250" width="150" height="80" rx="8" fill="{CHAR}" stroke="{OFF}" stroke-width="4" transform="rotate(10 595 290)"/>
  <rect x="200" y="260" width="120" height="70" rx="8" fill="{OFF}" opacity=".7" transform="rotate(8 260 295)"/>
</svg>'''
write("flood-02", page(f"""
  <div class="label">Here's how it happens</div>
  <div class="h" style="font-size:128px;margin-top:60px">They start<br>when the drain<br>is blocked.</div>
  {grate}
""", "lime", 2, T))

write("flood-03", page(f"""
  <div class="label">What's in the drain</div>
  <div class="h" style="font-size:190px;margin-top:60px;line-height:1">Nylon.<br>Bottles.<br><span class="acc">Sachets.</span></div>
  <div class="body" style="margin-top:60px;max-width:820px">Every one takes up the space the rainwater needs to move.</div>
  {sprout(300, extra="right:-40px;top:520px;transform:rotate(18deg);opacity:.35")}
""", "off", 3, T))

write("flood-04", page(f"""
  <div class="label">So when it rains</div>
  <div class="h" style="font-size:118px;margin-top:60px">The water goes<br>where it can:</div>
  <div class="h acc" style="font-size:150px;margin-top:70px;line-height:1.05">The road.<br>The shop.<br>Your house.</div>
""", "ink", 4, T))

def check(txt):
    return f'''<div style="display:flex;align-items:center;gap:34px;margin-top:44px">
      <div style="flex:none;width:84px;height:84px;border-radius:50%;background:{INK};display:flex;align-items:center;justify-content:center">
        <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="{LIME}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg></div>
      <div style="font-size:46px;font-weight:700;line-height:1.2">{txt}</div></div>'''
write("flood-05", page(f"""
  <div class="label">The fix starts small</div>
  <div class="h" style="font-size:140px;margin-top:60px">The fix starts<br>on your street.</div>
  <div style="margin-top:50px">{check("Keep the gutter clear")}{check("Bag your waste")}{check("Plan a clean-up with<br>your neighbours")}</div>
""", "lime", 5, T))

write("flood-06", page(f"""
  <div class="label">Young Climate Educators Fellowship</div>
  <div class="brico" style="font-size:150px;margin-top:60px">Got a<br><span style="color:{LIME}">bigger fix?</span></div>
  <div class="body" style="margin-top:50px;max-width:840px">Research a climate problem in your community.<br>Design a youth-led project to tackle it.</div>
  <div class="label" style="margin-top:40px">3 virtual weekends &middot; 50 fellows<br>Nigeria + Zambia</div>
  <div class="tape" style="background:{LIME};color:{INK};left:90px;bottom:200px;transform:rotate(-3deg)">Apply by Mon 26 Oct</div>
  <div class="stamp" style="right:90px;bottom:170px;width:220px;height:220px;border:5px solid {LIME};color:{LIME};font-size:26px;transform:rotate(10deg)">Link<br>in bio</div>
""", "ink", 6, T))

# ---------------- X thread image (1600x900) ----------------
write("flood-x-16x9", page(f"""
  <div class="label">Climate, explained locally</div>
  <div class="h" style="font-size:132px;margin-top:50px">Floods don't start<br><span class="acc">when the rain does.</span></div>
  <div class="body" style="margin-top:40px">They start in the drain outside your gate.</div>
  {sprout(380, extra="right:-50px;top:440px;transform:rotate(-12deg)")}
""", "ink", 0, 0, 1600, 900))

# ---------------- LinkedIn impact carousel (PDF, 1080x1350) ----------------
L = 5
write("li-01", page(f"""
  <div class="label">JOMO Climate Change Initiative</div>
  <div class="h" style="font-size:176px;margin-top:70px">Before YCEF,<br>there were<br><span class="acc">8 clean-ups.</span></div>
  {sprout(380, extra="right:-50px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 1, L))

write("li-02", page(f"""
  <div class="label">On the ground</div>
  <div class="h" style="font-size:560px;line-height:.9;margin-top:40px">8</div>
  <div class="h" style="font-size:96px;margin-top:10px">clean-ups</div>
  {sprout(340, extra="right:-40px;top:200px;transform:rotate(14deg);", color1=OFF, color2=LEAF)}
  <div class="body" style="margin-top:36px;max-width:820px">led by JOMO volunteers, alongside tree planting and climate lessons in schools.</div>
""", "lime", 2, L))

write("li-03", page(f"""
  <div class="label">Reach</div>
  <div class="h" style="font-size:225px;margin-top:70px;color:{OLIVE}">300,000+</div>
  <div class="h" style="font-size:96px;margin-top:20px">people reached</div>
  <div class="body" style="margin-top:40px;max-width:820px">through our fieldwork and online campaigns.</div>
  {sprout(380, extra="right:-60px;bottom:150px;transform:rotate(-12deg);opacity:.5")}
""", "off", 3, L))

def row(k, v):
    return f'''<div style="display:flex;gap:30px;align-items:baseline;padding:26px 0;border-bottom:2px solid rgba(244,246,236,.18)">
      <div class="label" style="width:250px;flex:none">{k}</div><div style="font-size:42px;font-weight:700">{v}</div></div>'''
write("li-04", page(f"""
  <div class="label">What we learned</div>
  <div class="body" style="margin-top:40px;font-size:44px">The people who know a street's climate<br>problem best are the young people<br>who live on it.</div>
  <div class="brico" style="font-size:118px;margin-top:50px;color:{LIME}">So we built YCEF.</div>
  <div style="margin-top:40px">{row("Format","3 virtual weekends")}{row("Fellows","50, Nigeria and Zambia")}{row("Open to","Students and grassroots volunteers, 18+")}</div>
""", "ink", 4, L))

write("li-05", page(f"""
  <div class="label">Young Climate Educators Fellowship</div>
  <div class="brico" style="font-size:150px;margin-top:60px">Applications<br>close Mon<br>26 Oct.</div>
  <div class="body" style="margin-top:50px;max-width:820px;font-weight:700">Apply via the link in the post.</div>
  <div style="position:absolute;left:90px;bottom:180px;background:#fff;border-radius:28px;padding:28px 36px">
    <img src="file://{ROOT}/../assets/logos/jomo-logo.png" style="width:330px;display:block"></div>
""", "lime", 5, L))

print("written", len(list(OUT.glob('*.html'))))
