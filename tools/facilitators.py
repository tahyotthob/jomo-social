"""YCEF facilitator flyers (Designer): a 4-slide carousel, 1080x1350. Cover + one slide each.
Redesign after operator feedback with reference posts (2026-11-01):
- everyone cut out onto the same brand backgrounds, so three very different photos read as one set;
- short bios: one bold line plus two or three sentences, in a card;
- name and role tags, an event bar with the YCEF dates, lime squiggles for energy.
Bios: the facilitators' own bios in the Drive folder "YCEF Facilitator Profile and Pictures", condensed.
Cut-outs: assets/photos/cutouts/ (made with tools/cutout.py; consent rows in content/consent-log.csv).
Run: python3 facilitators.py && node render.js
"""
from build import *

CUTS = ROOT.parent / "assets/photos/cutouts"
T = 4

STYLE = f"""<style>
.squig {{ position:absolute; z-index:1; }}
.panel {{ position:absolute; overflow:hidden; border-radius:26px; background:linear-gradient(170deg,{LIME} 0%,{LEAF} 60%,{OLIVE} 100%); }}
.panel img {{ position:absolute; left:50%; transform:translateX(-50%); }}
.nm {{ font-family:Anton; text-transform:uppercase; line-height:1.02; letter-spacing:.01em; }}
.rl {{ font-weight:900; text-transform:uppercase; letter-spacing:.08em; color:{LIME}; }}
.card {{ position:absolute; z-index:3; background:{OFF}; color:{INK}; border-radius:26px; padding:38px 40px; }}
.card .hook {{ font-weight:900; font-size:36px; line-height:1.22; }}
.card .bio {{ font-size:28px; line-height:1.42; margin-top:20px; }}
.blob {{ position:absolute; z-index:1; }}
.person {{ position:absolute; z-index:2; }}
.tag {{ position:absolute; z-index:4; background:{LIME}; color:{INK}; padding:14px 24px 16px; transform:rotate(-2deg); }}
.event {{ position:absolute; z-index:4; left:90px; right:90px; background:{LIME}; color:{INK}; border-radius:18px; padding:20px 28px;
          display:flex; justify-content:space-between; align-items:center; font-weight:900; font-size:23px; letter-spacing:.04em; text-transform:uppercase; }}
.event b {{ font-family:Anton; font-weight:400; font-size:34px; letter-spacing:.02em; }}
</style>"""

def squiggle(x, y, w, rot=0, col=LIME, stroke=26):
    return f'''<svg class="squig" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)" width="{w}" height="{w*0.45:.0f}" viewBox="0 0 220 100">
      <path d="M10 70 C40 10 80 10 95 50 S150 95 165 45 S200 5 210 30" fill="none" stroke="{col}" stroke-width="{stroke}" stroke-linecap="round"/></svg>'''

def blob(cx, cy, r, col=LIME):
    # wavy badge shape, like a rosette
    import math
    pts = []
    for i in range(0, 361, 6):
        a = math.radians(i); rr = r * (1 + 0.06 * math.sin(10 * a))
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<svg class="blob" style="left:0;top:0" width="1080" height="1350"><polygon points="{" ".join(pts)}" fill="{col}"/></svg>'

PEOPLE = [
    dict(slug="akpem-terese-shadrach", first="Shadrach", name="Dr. Akpem Terese Shadrach", short="Dr. Akpem<br>Terese Shadrach",
         role="Veterinarian &amp; social entrepreneur", cover_w=360, cover_top=20, w=560, top=330,
         hook="From animal health to 30,000+ young people trained.",
         bio="Dr. Shadrach is a veterinarian and social entrepreneur. He founded Vet Konect, a digital animal health platform for farmers and pet owners across Africa, and is a 2023 Mandela Washington Fellow."),
    dict(slug="gome-ngona", first="Gome", name="Gome Ng&rsquo;ona", short="Gome<br>Ng&rsquo;ona",
         role="Youth advocate &middot; Zambia", cover_w=330, cover_top=24, w=520, top=380,
         hook="Climate knowledge, turned into community-led solutions.",
         bio="Gome is a Zambian cultural heritage practitioner, development professional and youth advocate. He has worked on youth-led climate action and malaria elimination advocacy, and loves climate education and storytelling."),
    dict(slug="muhammad-daniyal-kamal", first="Daniyal", name="Muhammad Daniyal Kamal", short="Muhammad<br>Daniyal Kamal",
         role="Climate advocate &middot; Pakistan", cover_w=300, cover_top=26, w=500, top=380,
         hook="Youth-led climate education, from Pakistan to a UN COP.",
         bio="Daniyal is a climate advocate with a degree in Environmental Sciences. He co-founded RE-AD: Resilience and Adaptation, a youth-led climate education organisation, and was an official delegate at COP16 of the UN Convention to Combat Desertification."),
]

def cut(p):
    return f"file://{CUTS}/{p['slug']}-cutout.png"

# ---------- 1. cover ----------
panels = ""
for i, p in enumerate(PEOPLE):
    x = 90 + i * 310
    panels += f'''<div class="panel" style="left:{x}px;top:470px;width:280px;height:450px">
      <img src="{cut(p)}" style="top:{p['cover_top']}px;width:{p['cover_w']}px"></div>
    <div style="position:absolute;left:{x}px;top:944px;width:280px">
      <div class="nm" style="font-size:36px;color:{OFF}">{p['short']}</div>
      <div class="rl" style="font-size:17px;margin-top:10px">{p['role']}</div></div>'''

write("ycef-facilitators-01", page(f"""{STYLE}
  {squiggle(860, 150, 210, -14)}
  <div class="label" style="position:relative;z-index:3">Young Climate Educators Fellowship</div>
  <div class="brico" style="position:relative;z-index:3;font-size:132px;margin-top:40px">Meet your<br><span style="color:{LIME}">facilitators.</span></div>
  {panels}
  <div class="event" style="top:1110px"><span>3 virtual weekends</span><span>Weekend 1: <b>Fri 13 Nov</b></span></div>
""", "ink", 1, T))

# ---------- 2-4. one slide each ----------
for n, p in enumerate(PEOPLE, start=2):
    write(f"ycef-facilitators-0{n}", page(f"""{STYLE}
  {squiggle(820, 30, 240, -12)}
  <div class="blob" style="right:-120px;top:420px;width:640px;height:640px;border-radius:50%;background:{LIME}"></div>
  <div style="position:absolute;z-index:2;right:0;top:0;width:560px;height:1210px;overflow:hidden">
    <img src="{cut(p)}" style="position:absolute;right:{-60 if p['w'] > 540 else -30}px;top:{p['top']}px;width:{p['w']}px"></div>
  <div class="label" style="position:relative;z-index:3">YCEF facilitator &middot; {n - 1} of 3</div>
  <div class="brico" style="position:relative;z-index:3;font-size:120px;margin-top:30px">Meet<br><span style="color:{LIME}">{p['first']}.</span></div>
  <div class="card" style="left:90px;top:440px;width:560px">
    <div class="hook">{p['hook']}</div>
    <div class="bio">{p['bio']}</div></div>
  <div class="tag" style="left:90px;top:1030px"><div class="nm" style="font-size:40px">{p['name']}</div>
    <div style="font-weight:900;font-size:19px;letter-spacing:.08em;text-transform:uppercase;margin-top:6px">{p['role']}</div></div>
""", "ink", n, T))
print("facilitators ok")
