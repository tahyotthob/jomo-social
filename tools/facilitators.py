"""YCEF facilitator bio flyers: a 4-slide carousel (cover + one bio each), 1080x1350.
Bios: the facilitators' own bios in the Drive folder "YCEF Facilitator Profile and Pictures", condensed.
Photos: assets/photos/people/ycef-facilitators/ (consent rows in content/consent-log.csv).
Run: python3 facilitators.py && node render.js
"""
from build import *

PH = ROOT.parent / "assets/photos/people/ycef-facilitators"
SHADRACH = f"file://{PH}/akpem-terese-shadrach.jpg"
GOME = f"file://{PH}/gome-ngona.jpg"
DANIYAL = f"file://{PH}/muhammad-daniyal-kamal.jpg"   # cropped to head and shoulders from the full-length original
T = 4

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

def bio(n, label, name_html, role, photo, pos, points, total=T, name_size=100):
    pts = "".join(f'<div class="pt"><div class="dot"></div><div>{p}</div></div>' for p in points)
    return page(f"""{EXTRA}
  <div class="label">{label}</div>
  <div class="name" style="font-size:{name_size}px;margin-top:40px;width:440px">{name_html}</div>
  <div class="role" style="margin-top:28px;width:420px">{role}</div>
  <div style="position:absolute;right:66px;top:114px;width:440px;height:560px;border-radius:30px;background:{LIME}"></div>
  <div class="card" style="right:90px;top:90px;width:440px;height:560px"><img src="{photo}" style="object-position:{pos}"></div>
  <div class="pts" style="top:700px">{pts}</div>
""", "off", n, total)

# 1. Cover: all three facilitators
def portrait(photo, pos, name, sub, left, w=280):
    return f'''<div class="card" style="left:{left}px;top:520px;width:{w}px;height:470px"><img src="{photo}" style="object-position:{pos}"></div>
  <div style="position:absolute;left:{left}px;top:1012px;width:{w}px">
    <div class="name" style="font-size:40px">{name}</div>
    <div style="font-size:19px;font-weight:700;letter-spacing:.05em;margin-top:10px;color:{LIME}">{sub}</div></div>'''

write("ycef-facilitators-01", page(f"""{EXTRA}
  <div class="label">Young Climate Educators Fellowship</div>
  <div class="brico" style="font-size:150px;margin-top:50px">Meet your<br><span style="color:{LIME}">facilitators.</span></div>
  {sprout(200, extra="right:-30px;top:-30px;transform:rotate(-12deg)")}
  {portrait(SHADRACH, "50% 12%", "Dr. Akpem<br>Terese Shadrach", "VETERINARIAN &amp;<br>SOCIAL ENTREPRENEUR", 90)}
  {portrait(GOME, "50% 14%", "Gome<br>Ng&rsquo;ona", "YOUTH ADVOCATE<br>ZAMBIA", 400)}
  {portrait(DANIYAL, "50% 10%", "Muhammad<br>Daniyal Kamal", "CLIMATE ADVOCATE<br>PAKISTAN", 710)}
""", "ink", 1, T))

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
# 4. Muhammad Daniyal Kamal
write("ycef-facilitators-04", bio(4, "YCEF facilitator",
  "Muhammad<br>Daniyal<br><span style='color:" + OLIVE + "'>Kamal</span>",
  "Climate advocate and sustainability leader from Pakistan",
  DANIYAL, "50% 12%", [
    "<b>Co-founder, RE-AD: Resilience and Adaptation</b>, a youth-led group for climate education, disaster risk reduction and water stewardship for students across Pakistan",
    "<b>Official delegate for Pakistan at COP16</b> of the UN Convention to Combat Desertification, Riyadh",
    "<b>Secretary SDGs, The Buraaq Association</b> (2023&ndash;2025), leading youth initiatives on the UN SDGs",
    "Bachelor&rsquo;s in <b>Environmental Sciences</b>, Quaid-i-Azam University, Islamabad",
  ], name_size=84))
print("facilitators ok")
