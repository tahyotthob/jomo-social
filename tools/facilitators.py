"""YCEF facilitator bio flyers: a 3-slide carousel (cover + one bio each), 1080x1350.
Bios: the facilitators' own bios in the Drive folder "YCEF Facilitator Profile and Pictures", condensed.
Photos: assets/photos/people/ycef-facilitators/ (consent rows in content/consent-log.csv).
Run: python3 facilitators.py && node render.js
"""
from build import *

PH = ROOT.parent / "assets/photos/people/ycef-facilitators"
SHADRACH = f"file://{PH}/akpem-terese-shadrach.jpg"
GOME = f"file://{PH}/gome-ngona.jpg"

EXTRA = f"""<style>
.card {{ position:absolute; border-radius:30px; overflow:hidden; background:#fff; }}
.card img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.name {{ font-family:Anton; text-transform:uppercase; line-height:1; letter-spacing:.01em; }}
.role {{ font-weight:700; font-size:30px; line-height:1.3; }}
.pts {{ position:absolute; left:90px; right:90px; }}
.pt {{ display:flex; gap:26px; align-items:flex-start; padding:17px 0; border-top:2px solid rgba(30,34,32,.14); font-size:31px; line-height:1.3; }}
.pt:first-child {{ border-top:0; }}
.pt .dot {{ flex:none; width:22px; height:22px; border-radius:50%; background:{LIME}; margin-top:11px; }}
.pt b {{ font-weight:900; }}
</style>"""

def bio(n, label, name_html, role, photo, pos, points, total=3):
    pts = "".join(f'<div class="pt"><div class="dot"></div><div>{p}</div></div>' for p in points)
    return page(f"""{EXTRA}
  <div class="label">{label}</div>
  <div class="name" style="font-size:100px;margin-top:40px;width:470px">{name_html}</div>
  <div class="role" style="margin-top:28px;width:470px">{role}</div>
  <div style="position:absolute;right:66px;top:114px;width:440px;height:560px;border-radius:30px;background:{LIME}"></div>
  <div class="card" style="right:90px;top:90px;width:440px;height:560px"><img src="{photo}" style="object-position:{pos}"></div>
  <div class="pts" style="top:700px">{pts}</div>
""", "off", n, total)

# 1. Cover: both facilitators
def portrait(photo, pos, name, sub, left):
    return f'''<div class="card" style="left:{left}px;top:540px;width:430px;height:470px"><img src="{photo}" style="object-position:{pos}"></div>
  <div style="position:absolute;left:{left}px;top:1036px;width:430px">
    <div class="name" style="font-size:50px">{name}</div>
    <div style="font-size:24px;font-weight:700;letter-spacing:.06em;margin-top:10px;color:{LIME}">{sub}</div></div>'''

write("ycef-facilitators-01", page(f"""{EXTRA}
  <div class="label">Young Climate Educators Fellowship</div>
  <div class="brico" style="font-size:150px;margin-top:50px">Meet your<br><span style="color:{LIME}">facilitators.</span></div>
  {sprout(200, extra="right:-30px;top:-30px;transform:rotate(-12deg)")}
  {portrait(SHADRACH, "50% 12%", "Dr. Akpem Terese<br>Shadrach", "VETERINARIAN &amp;<br>SOCIAL ENTREPRENEUR", 90)}
  {portrait(GOME, "50% 14%", "Gome<br>Ng&rsquo;ona", "YOUTH ADVOCATE<br>ZAMBIA", 560)}
""", "ink", 1, 3))

# 2. Dr. Akpem Terese Shadrach
write("ycef-facilitators-02", bio(2, "YCEF facilitator",
  "Dr. Akpem<br>Terese<br><span style='color:" + OLIVE + "'>Shadrach</span>",
  "Veterinarian, social entrepreneur and youth trainer",
  SHADRACH, "50% 15%", [
    "<b>Founder, Vet Konect:</b> digital animal health coverage for livestock farmers and pet owners in Nigeria and other African countries",
    "Has trained and mentored <b>30,000+ young people</b> in digital skills",
    "<b>Lead facilitator, Jobberman Nigeria</b> in Benue State, coordinating 60+ digital skills trainers",
    "<b>2023 Mandela Washington Fellow</b> and a 2024 Top Agri-food Pioneer (World Food Prize Foundation)",
  ]))

# 3. Gome Ng'ona
write("ycef-facilitators-03", bio(3, "YCEF facilitator",
  "Gome<br><span style='color:" + OLIVE + "'>Ng&rsquo;ona</span>",
  "Zambian cultural heritage practitioner, development professional and youth advocate",
  GOME, "50% 18%", [
    "Background in <b>education, climate advocacy and community engagement</b>",
    "Has worked on <b>youth-led climate action</b>, malaria elimination advocacy and environmental sustainability",
    "Passionate about <b>climate education and storytelling</b>",
    "Helps young people turn climate knowledge into <b>practical, community-led solutions</b>",
  ]))
print("facilitators ok")
