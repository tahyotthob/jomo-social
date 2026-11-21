"""Week of 2026-11-21 visuals (Designer). Run: python3 week_1123.py && node render.js
Week B of the YCEF three-week plan (Weekend 2, Educate), on the design system from week_1116.py:
series header, JOMO's own photos large, about 20 words per image, no decorative clip-art."""
from week_1116 import P, series, CUT, STYLE
from week_1016 import st, photo, grad, ONI
from build import *

BDAY = "file:///home/user/jomo-social/assets/photos/events/birthday-cleanup-2021/birthday-cleanup-2021-%s.jpg"

# ===== Sat 21: Weekend 2 story (poll) =====
write("w21-wk2-story-9x16", P(f"""<style>.series{{top:250px}} .foot{{bottom:260px}}</style>{series("YCEF 2026 &middot; Weekend 2", "Educate")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:420px">
  <div class="big" style="font-size:132px">Weekend 2:<br><span style="color:{LIME}">learning<br>to teach climate.</span></div>
  <div class="rule"></div>
  <div class="txt" style="font-size:46px;font-weight:700">Who first taught you about climate change?</div></div>
""", "ink", 0, 0, 1080, 1920))

# ===== Sun 22: facilitator, Ochanya Okoh (2.3 Micro-teaching) =====
def facilitator(name, role, session, title, slug, when, h=760):
    return P(f"""{series("YCEF 2026 &middot; Meet your facilitator", when)}
 <div style="position:absolute;z-index:0;left:0;top:92px;width:1080px;height:1258px;background:{INK}"></div>
 <div style="position:absolute;z-index:1;right:0;top:92px;width:560px;height:1088px;background:linear-gradient(180deg,#2a2f2c 0%,{INK} 100%)"></div>
 <img class="cut" src="{CUT % slug}" style="right:-90px;bottom:170px;height:{h}px">
 <div class="c" style="position:absolute;left:90px;top:190px;width:440px">
  <div class="kicker" style="color:{LIME}">Session {session}</div>
  <div class="big" style="font-size:56px;margin-top:20px;color:{OFF}">{title}</div>
  <div class="rule"></div>
  <div class="big" style="font-size:84px;color:{OFF}">{name}</div>
  <div class="txt" style="margin-top:20px;font-size:32px;color:{OFF};opacity:.85">{role}</div></div>
""", "ink", 0, 0)

write("w22-fac-ochanya", facilitator("Ochanya<br>Okoh", "Public policy and development professional.<br>Technical Adviser on Agriculture,<br>Benue State Government.",
      "2.3 &middot; Sun 22 Nov", "Micro-teaching: fellows practise and get feedback", "ochanya-okoh", "Sun 22 Nov", 640))

# ===== Mon 23: big swing, "Explain climate change in 60 seconds" (carousel, 5) =====
T = 5
YC2 = "YCEF 2026 &middot; Weekend 2"
write("w23-60s-01", P(f"""{series(YC2, "Educate")}
 <div style="position:absolute;z-index:0;left:0;top:0;width:1080px;height:1350px;background:{INK}"></div>{photo(ONI % '05', 0, 92, 1080, 700, "50% 20%")}{grad('bottom', 34, 1, 92, 700)}
 <div class="chip" style="right:40px;top:122px">JOMO volunteer &middot; Oniwaya, Lagos</div>
 <div class="c" style="position:absolute;left:90px;right:90px;bottom:170px">
  <div class="kicker" style="color:{LIME}">What fellows practised this weekend</div>
  <div class="big" style="font-size:104px;margin-top:20px">Explain climate change to your neighbour <span style="color:{LIME}">in 60 seconds.</span></div></div>
""", "ink", 1, T))
def step(n, sec, head, body, theme):
    acc = LIME if theme == "ink" else (OLIVE if theme == "off" else INK)
    return P(f"""{series(YC2, sec, theme)}
 <div class="c" style="position:absolute;left:90px;right:90px;top:280px">
  <div class="kicker" style="color:{acc}">{sec}</div>
  <div class="big" style="font-size:104px;margin-top:30px">{head}</div>
  <div class="rule"></div>
  <div class="txt" style="max-width:880px">{body}</div></div>
""", theme, n, T)
write("w23-60s-02", step(2, "0&ndash;15 seconds", "The sun warms<br>the Earth.", "Some of that heat should escape back into space.", "ink"))
write("w23-60s-03", step(3, "15&ndash;30 seconds", "We&rsquo;ve thickened<br>the blanket.", "Burning coal, oil and gas adds gases that trap the heat, like a thicker blanket.", "off"))
write("w23-60s-04", step(4, "30&ndash;45 seconds", "So we get<br>more extremes.", "Hotter days, heavier rain on blocked drains, longer dry spells on farms.", "ink"))
write("w23-60s-05", P(f"""{series(YC2, "45&ndash;60 seconds", "lime")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:280px">
  <div class="kicker" style="color:{INK}">45&ndash;60 seconds</div>
  <div class="big" style="font-size:104px;margin-top:30px">And we can<br>still act.</div>
  <div class="rule" style="background:{INK}"></div>
  <div class="txt" style="font-weight:700">Waste less, keep drains clear, plant trees, and talk about it. Now try it on someone.</div></div>
""", "lime", 5, T))

# ===== Thu 26: World Sustainable Transport Day (carousel, 4) =====
T = 4
TD = "Sustainable Transport Day"
write("w26-transport-01", P(f"""{series("Climate, explained locally", TD)}
 <div class="c" style="position:absolute;left:90px;right:90px;top:240px">
  <div class="kicker" style="color:{LIME}">Your daily commute</div>
  <div class="big" style="font-size:150px;margin-top:30px">Danfo.<br>BRT.<br><span style="color:{LIME}">Your feet.</span></div>
  <div class="txt" style="margin-top:30px;opacity:.85">How you move is a climate choice too.</div></div>
""", "ink", 1, T))
write("w26-transport-02", P(f"""{series("Climate, explained locally", TD, "off")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:280px">
  <div class="kicker" style="color:{OLIVE}">Shared beats solo</div>
  <div class="big" style="font-size:100px;margin-top:30px">One full bus<br>carries more people<br>per litre of fuel.</div>
  <div class="rule"></div>
  <div class="txt">Fewer engines running for the same trip means less fuel burnt and cleaner air.</div></div>
""", "off", 2, T))
write("w26-transport-03", P(f"""{series("Climate, explained locally", TD, "ink")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:280px">
  <div class="kicker" style="color:{LIME}">Short trips</div>
  <div class="big" style="font-size:110px;margin-top:30px">Under 15 minutes?<br><span style="color:{LIME}">Walk it.</span></div>
  <div class="rule"></div>
  <div class="txt">No fuel, no fare, no go-slow. And you&rsquo;ll see your street up close.</div></div>
""", "ink", 3, T))
write("w26-transport-04", P(f"""{series("Climate, explained locally", TD, "lime")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:300px">
  <div class="big" style="font-size:112px">How do you get to school or work?</div>
  <div class="rule" style="background:{INK}"></div>
  <div class="txt" style="font-weight:700">Danfo, keke, BRT, bike, okada or your feet? Tell us below.</div></div>
""", "lime", 4, T))

# ===== Fri 27: Black Friday, "Buy less, fix more" (single image + story) =====
def bf(w, h, story=False):
    top = 420 if story else 92
    extra = "<style>.series{top:250px} .foot{bottom:260px}</style>" if story else ""
    ph = 600 if story else 700
    return P(f"""{extra}{series("Climate, explained locally", "Black Friday")}
 <div style="position:absolute;z-index:0;left:0;top:0;width:{w}px;height:{h}px;background:{INK}"></div>{photo(BDAY % '01', 0, top, w, ph, "50% 50%")}{grad('bottom', 40, 1, top, ph, w)}
 <div class="chip" style="right:40px;top:{top + 30}px">JOMO clean-up &middot; from our archive</div>
 <div class="c" style="position:absolute;left:90px;right:90px;top:{top + ph - (20 if story else 140)}px">
  <div class="h" style="font-size:{140 if story else 130}px">{st('Buy more.', th=11, color='rgba(244,246,236,.6)')}<br><span class="acc">Buy less,<br>fix more.</span></div>
  <div class="txt" style="margin-top:24px;opacity:.85">Everything we throw away ends up somewhere.</div></div>
""", "ink", 0, 0, w, h)
write("w27-blackfriday-01", bf(1080, 1350))
write("w27-blackfriday-story-9x16", bf(1080, 1920, True))
print("w1123 written")

# ===== Tue 24: how a COP decision gets made (X 16:9 + LinkedIn 4:5) =====
def copdec(w, h):
    tall = h > 1000
    return P(f"""{series("Climate, explained locally", "After COP31")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:{300 if tall else 170}px">
  <div class="kicker" style="color:{LIME}">COP31 &middot; Antalya, T&uuml;rkiye</div>
  <div class="big" style="font-size:{104 if tall else 112}px;margin-top:26px">How does a COP<br><span style="color:{LIME}">agree anything?</span></div>
  <div class="txt" style="margin-top:30px;opacity:.85">While we wait for COP31&rsquo;s final decisions to be published.</div></div>
""", "ink", 0, 0, w, h)
write("w24-cop31-decision-x-16x9", copdec(1600, 900))
write("w24-cop31-decision-li", copdec(1080, 1350))
