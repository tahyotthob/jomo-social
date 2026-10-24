"""First Tobi and Amara post: Source, please, burning refuse (Designer). Run: python3 avatars_test.py && node render.js"""
from build import *
AV = f"file://{ROOT}/../assets/avatars/cutouts/"
TOBI, AMARA = AV + "tobi-cutout-trim.png", AV + "amara-cutout-trim.png"
LOGO_L = f"file://{ROOT}/../assets/logos/jomo-logo-light.png"
X = """.ai{position:absolute;z-index:6;font-weight:900;font-size:20px;letter-spacing:.16em;text-transform:uppercase;padding:8px 14px;border-radius:999px}
.bub{position:absolute;z-index:5;border-radius:34px;padding:28px 34px;font-weight:700;font-size:38px;line-height:1.25}
.bub:after{content:'';position:absolute;bottom:-26px;width:0;height:0;border:16px solid transparent}
.bl:after{left:70px;border-top:28px solid var(--b);border-left:22px solid var(--b)}
.br:after{right:70px;border-top:28px solid var(--b);border-right:22px solid var(--b)}
.who{display:block;font-size:20px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;opacity:.7;margin-bottom:8px}
img.av{position:absolute;z-index:3}
.src{font-size:24px;line-height:1.35;opacity:.75}"""

def pg(body, theme, n, total, w=1080, h=1350):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}{X}</style></head>
<body><div class="s {theme}">{body}{foot(theme, n, total)}</div></body></html>"""

def chip(x, y, dark=True):
    bg, fg = (INK, LIME) if dark else (LIME, INK)
    return f'<div class="ai" style="left:{x}px;top:{y}px;background:{bg};color:{fg}">AI avatar</div>'

T = 5
write("av1-01", pg(f"""
 <div class="label">Source, please &middot; with Tobi and Amara</div>
 <div class="h" style="font-size:96px;margin-top:26px">Burning refuse: <span class="acc">clean fix or smoke trap?</span></div>
 <div class="bub bl" style="--b:{LIME};background:{LIME};color:{INK};left:90px;top:400px;width:540px;font-size:34px"><span class="who">Tobi &middot; AI avatar</span>My uncle says burning the refuse heap is the cleanest way to clear it.</div>
 <div class="bub br" style="--b:{INK};background:{INK};color:{OFF};right:90px;top:400px;width:340px;font-size:34px"><span class="who" style="color:{LIME}">Amara &middot; AI avatar</span>Source, please.</div>
 <img class="av" src="{TOBI}" style="left:150px;bottom:125px;height:600px">
 <img class="av" src="{AMARA}" style="right:150px;bottom:125px;height:600px">
""", "off", 1, T))

write("av1-02", pg(f"""
 <img class="av" src="{AMARA}" style="right:60px;bottom:120px;height:960px">
 {chip(500, 1000, dark=False)}
 <div style="position:relative;z-index:4;max-width:540px">
  <div class="label">What WHO says</div>
  <div class="h" style="font-size:118px;margin-top:40px">The smoke<br>doesn't<br><span class="acc">disappear.</span></div>
  <div class="body" style="margin-top:44px;font-size:42px">Burning waste releases air pollutants. Some harm both health and the climate.</div>
  <div class="src" style="margin-top:40px">Source: World Health Organization, <i>Open waste burning: sectoral solutions for air pollution and health</i>, July 2025</div>
 </div>
""", "ink", 2, T))

write("av1-03", pg(f"""
 <div class="label">Breathing the smoke can cause</div>
 <div class="h" style="font-size:150px;margin-top:50px;line-height:1.02">Coughing.<br>Skin<br>irritation.<br><span style="color:{OFF}">Breathing<br>problems.</span></div>
 <div class="body" style="margin-top:44px;font-size:40px;max-width:880px;font-weight:700">Short-term or long-term, says WHO.</div>
 {sprout(300, color1=OFF, color2=LEAF, extra="right:-40px;top:80px;transform:rotate(16deg);opacity:.9")}
""", "lime", 3, T))

def tick(txt):
    return f'''<div style="display:flex;align-items:flex-start;gap:24px;margin-top:40px">
 <div style="flex:none;width:64px;height:64px;border-radius:50%;background:{INK};display:flex;align-items:center;justify-content:center">
 <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="{LIME}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg></div>
 <div style="font-size:40px;font-weight:700;line-height:1.22;padding-top:2px">{txt}</div></div>'''
write("av1-04", pg(f"""
 <img class="av" src="{TOBI}" style="left:30px;bottom:120px;height:900px">
 {chip(330, 1080)}
 <div style="position:absolute;z-index:4;left:500px;right:80px;top:90px">
  <div class="label">Do this instead</div>
  <div class="h" style="font-size:104px;margin-top:30px">So wetin<br><span class="acc">we go do?</span></div>
  {tick("Bag it and keep it covered until it's collected")}
  {tick("Keep plastics, tyres and nylon out of any fire")}
  {tick("Agree on one collection point with your neighbours")}
 </div>
""", "off", 4, T))

write("av1-05", pg(f"""
 <div class="bub bl" style="--b:{LIME};background:{LIME};color:{INK};left:90px;top:110px;width:430px"><span class="who">Tobi &middot; AI avatar</span>Who's coming?</div>
 <div class="bub br" style="--b:{OFF};background:{OFF};color:{INK};right:90px;top:250px;width:430px"><span class="who">Amara &middot; AI avatar</span>And bring your facts.</div>
 <img class="av" src="{TOBI}" style="left:130px;bottom:210px;height:620px">
 <img class="av" src="{AMARA}" style="right:170px;bottom:210px;height:620px">
 <div class="src" style="position:absolute;z-index:6;left:90px;right:90px;bottom:150px;font-size:26px;text-align:center;opacity:.9">Tobi and Amara are JOMO's AI characters, not real people.</div>
""", "ink", 5, T))
print("ok")
