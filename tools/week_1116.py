"""Week of 2026-11-16 visuals (Designer). Run: python3 week_1116.py && node render.js
First batch on the new design rules (operator, 2026-11-13: "less AI-looking, more professional"):
- JOMO's own photos, full-bleed or in large frames;
- one series header bar per series (YCEF 2026, Climate explained locally, COP31);
- about 20 words on an image, with detail in the caption;
- no decorative leaves or squiggles; plain flat colour blocks and a hairline rule only.
Photos and cut-outs have consent on record."""
from week_1016 import pg, st, photo, grad, ONI
from build import *

CUT = "file:///home/user/jomo-social/assets/photos/cutouts/%s-cutout.png"
BDAY = "file:///home/user/jomo-social/assets/photos/events/birthday-cleanup-2021/birthday-cleanup-2021-%s.jpg"

STYLE = f"""<style>
.series {{ position:absolute; z-index:6; left:0; right:0; top:0; height:92px; display:flex; align-items:center; gap:18px; padding:0 90px;
          font-weight:900; font-size:22px; letter-spacing:.2em; text-transform:uppercase; }}
.series .dot {{ width:14px; height:14px; border-radius:50%; background:{LIME}; }}
.series .sub {{ margin-left:auto; font-weight:700; letter-spacing:.12em; opacity:.75; }}
.rule {{ height:3px; width:120px; background:{LIME}; margin:34px 0; }}
.kicker {{ font-weight:900; font-size:26px; letter-spacing:.18em; text-transform:uppercase; }}
.big {{ font-family:Brico; font-weight:800; letter-spacing:-.02em; line-height:1.0; }}
.txt {{ font-size:40px; line-height:1.35; }}
.credit {{ font-weight:700; font-size:26px; letter-spacing:.04em; }}
.frame {{ position:absolute; overflow:hidden; border-radius:22px; }}
.frame img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.cut {{ position:absolute; z-index:2; }}
.chip {{ position:absolute; z-index:4; background:{OFF}; color:{INK}; font-weight:900; font-size:20px; letter-spacing:.16em; text-transform:uppercase; padding:10px 18px; }}
</style>"""

def series(text, sub="", theme="ink"):
    bg = {"ink": "#151917", "lime": "#93BA2C", "off": "#E6E9DC"}[theme]
    col = OFF if theme == "ink" else INK
    return f'<div class="series" style="background:{bg};color:{col}"><span class="dot"></span>{text}<span class="sub">{sub}</span></div>'

def P(body, theme, n, total, w=1080, h=1350):
    return pg(STYLE + body, theme, n, total, w, h)

# ======================= Mon 16: Weekend 1 in plain language (carousel, 4) =======================
T = 4
YC = "YCEF 2026 &middot; Weekend 1"
write("w16-wk1-01", P(f"""{series(YC, "Understand")}
 <div style="position:absolute;z-index:0;left:0;top:92px;width:1080px;height:1258px;background:{INK}"></div>
 <div style="position:absolute;z-index:1;left:0;right:0;bottom:0;height:560px;background:linear-gradient(180deg,#2a2f2c 0%,{INK} 100%)"></div>
 <img class="cut" src="{CUT % 'muhammad-daniyal-kamal'}" style="left:40px;bottom:120px;height:640px">
 <img class="cut" src="{CUT % 'gome-ngona'}" style="left:380px;bottom:120px;height:620px">
 <img class="cut" src="{CUT % 'graham-favour'}" style="left:730px;bottom:120px;height:340px">
 <div class="c" style="position:absolute;left:90px;right:90px;top:150px">
  <div class="big" style="font-size:104px;color:{OFF}">Weekend 1,<br><span style="color:{LIME}">in plain language.</span></div>
  <div class="txt" style="margin-top:26px;color:{OFF};opacity:.85">Three things 50 young climate educators covered.</div></div>
""", "ink", 1, T))

def lesson(n, num, kicker, head, body, who, theme):
    acc = LIME if theme == "ink" else (OLIVE if theme == "off" else INK)
    return P(f"""{series(YC, f"Session 1.{num}", theme)}
 <div class="c" style="position:absolute;left:90px;right:90px;top:300px">
  <div class="kicker" style="color:{acc}">{kicker}</div>
  <div class="big" style="font-size:96px;margin-top:30px">{head}</div>
  <div class="rule"></div>
  <div class="txt" style="max-width:880px">{body}</div></div>
 <div class="credit" style="position:absolute;left:90px;bottom:160px;opacity:.8">Session 1.{num} &middot; led by {who}</div>
""", theme, n, T)

write("w16-wk1-02", lesson(2, 1, "The science", "It&rsquo;s already<br>1.1&deg;C warmer.",
      "Burning coal, oil and gas adds greenhouse gases that trap heat. The world was about 1.1&deg;C warmer in 2011&ndash;2020 than in the late 1800s.", "Kamal Daniyal", "ink"))
write("w16-wk1-03", lesson(3, 2, "Here at home", "Same climate.<br>Different streets.",
      "In Lagos, heavy rain meets blocked drains. In parts of Zambia, late rains and dry spells hit farms. Climate change looks local.", "Gome Ng&rsquo;ona", "lime"))
write("w16-wk1-04", lesson(4, 3, "Try it this week", "Map one<br>problem.",
      "Walk your street. Note where water collects and waste piles up. Ask the people who live there. Write down what you see.", "Graham Favour", "off"))

# ======================= Tue 17: COP31 oceans, nature and land (X 16:9) =======================
write("w17-cop31-ocean-x-16x9", P(f"""{series("Climate, explained locally", "COP31 &middot; Day 9", "ink")}
 <div class="c" style="position:absolute;left:90px;top:190px;width:1300px">
  <div class="kicker" style="color:{LIME}">Today at COP31: oceans, nature &amp; land</div>
  <div class="big" style="font-size:150px;margin-top:26px">Lagos lives<br><span style="color:{LIME}">on a lagoon.</span></div>
  <div class="txt" style="margin-top:30px;font-size:40px;opacity:.85">What ends up in our drains ends up in the water.</div></div>
""", "ink", 0, 0, 1600, 900))

# ======================= Wed 18: big swing (moved from Sat 14), carousel 4 =======================
T = 4
write("w18-edu-01", P(f"""{series("YCEF 2026", "Understand &middot; Educate &middot; Act")}
 <div style="position:absolute;z-index:0;left:0;top:0;width:1080px;height:1350px;background:{INK}"></div>{photo(ONI % '04', 0, 92, 1080, 690, "50% 22%")}{grad('bottom', 30, 1, 92, 690)}
 <div class="chip" style="right:40px;top:122px">JOMO volunteers &middot; Oniwaya, Lagos</div>
 <div class="c" style="position:absolute;left:90px;right:90px;bottom:170px">
  <div class="h" style="font-size:124px">{st('A classroom subject.', th=10, color='rgba(244,246,236,.6)')}<br><span class="acc">It&rsquo;s your street.</span></div></div>
""", "ink", 1, T))
write("w18-edu-02", P(f"""{series("YCEF 2026", "In plain language")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:320px">
  <div class="kicker" style="color:{LIME}">Climate literacy means</div>
  <div class="big" style="font-size:84px;margin-top:40px;line-height:1.12">knowing what&rsquo;s changing,<br>why it&rsquo;s changing,<br><span style="color:{LIME}">and what you can do.</span></div></div>
""", "ink", 2, T))
write("w18-edu-03", P(f"""{series("YCEF 2026", "From our archive")}
 <div style="position:absolute;z-index:0;left:0;top:0;width:1080px;height:1350px;background:{INK}"></div>{photo(BDAY % '09', 0, 92, 1080, 760, "50% 35%")}{grad('bottom', 34, 1, 92, 760)}
 <div class="c" style="position:absolute;left:90px;right:90px;top:820px">
  <div class="kicker" style="color:{LIME}">Some lessons happen outside</div>
  <div class="big" style="font-size:88px;margin-top:20px">Schools. Markets.<br>Drains.</div></div>
""", "ink", 3, T))
write("w18-edu-04", P(f"""{series("YCEF 2026", "Your turn", "lime")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:300px">
  <div class="big" style="font-size:112px">Where did you first learn about climate change?</div>
  <div class="rule" style="background:{INK}"></div>
  <div class="txt" style="font-weight:700">School, church, mosque, TV, the street? Tell us in the comments.</div></div>
""", "lime", 4, T))

# ======================= Thu 19: World Toilet Day (carousel, 4) =======================
T = 4
WT = "World Toilet Day &middot; 19 Nov"
write("w19-toilet-01", P(f"""{series("Climate, explained locally", WT)}
 <div style="position:absolute;z-index:0;left:0;top:0;width:1080px;height:1350px;background:{INK}"></div>{photo(BDAY % '01', 0, 92, 1080, 820, "50% 50%")}{grad('bottom', 40, 1, 92, 820)}
 <div class="chip" style="right:40px;top:122px">JOMO clean-up &middot; from our archive</div>
 <div class="c" style="position:absolute;left:90px;right:90px;bottom:170px">
  <div class="big" style="font-size:100px">When the drain floods,<br><span style="color:{LIME}">where does the toilet go?</span></div></div>
""", "ink", 1, T))
write("w19-toilet-02", P(f"""{series("Climate, explained locally", WT, "off")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:300px">
  <div class="kicker" style="color:{OLIVE}">Here&rsquo;s the problem</div>
  <div class="big" style="font-size:100px;margin-top:30px">Floodwater<br>mixes with<br>sewage.</div>
  <div class="rule"></div>
  <div class="txt" style="max-width:880px">That spreads diarrhoea and other diseases, and it hits homes without safe toilets hardest.</div></div>
""", "off", 2, T))
write("w19-toilet-03", P(f"""{series("Climate, explained locally", WT, "ink")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:300px">
  <div class="kicker" style="color:{LIME}">This year&rsquo;s theme</div>
  <div class="big" style="font-size:132px;margin-top:30px">Safe toilets.<br><span style="color:{LIME}">Equal futures.</span></div>
  <div class="rule"></div>
  <div class="txt" style="max-width:860px">Heavier rain makes safe sanitation a climate issue too.</div></div>
""", "ink", 3, T))
def tick(txt):
    return f'''<div style="display:flex;gap:28px;align-items:flex-start;padding:26px 0;border-top:2px solid rgba(30,34,32,.2)">
 <div style="flex:none;width:18px;height:18px;margin-top:16px;background:{INK}"></div><div style="font-size:44px;font-weight:700;line-height:1.25">{txt}</div></div>'''
write("w19-toilet-04", P(f"""{series("Climate, explained locally", WT, "lime")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:260px">
  <div class="big" style="font-size:96px">Three things<br>you can do</div>
  <div style="margin-top:50px">{tick("Never empty waste or sewage into drains")}{tick("Wash your hands with soap after floods")}{tick("Report blocked drains before the rain")}</div></div>
""", "lime", 4, T))

# ======================= Fri 20: COP31's last day (X 16:9 + LinkedIn 4:5) =======================
def lastday(w, h, n=0):
    return P(f"""{series("Climate, explained locally", "COP31 &middot; Final day")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:{340 if h > 1000 else 190}px">
  <div class="kicker" style="color:{LIME}">9&ndash;20 Nov 2026 &middot; Antalya, T&uuml;rkiye</div>
  <div class="big" style="font-size:{110 if h > 1000 else 120}px;margin-top:26px">COP31 ends today.<br><span style="color:{LIME}">What happens<br>on the last day?</span></div></div>
""", "ink", 0, 0, w, h)
write("w20-cop31-last-x-16x9", lastday(1600, 900))
write("w20-cop31-last-li", lastday(1080, 1350))
print("w1116 written")
