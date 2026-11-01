"""Week of 2026-11-01 visuals (Designer). Run: python3 week_1102.py && node render.js
YCEF close (Sun to Wed), the water carousel without World Cities Day, and COP31 "starts Monday".
Reuses the helpers from week_1016.py and the layouts from week_1026.py."""
from week_1016 import pg, st, photo, grad, stamp, tick, ONI, LEKKI, URL, LOGO_L, LOGO_D
from build import *

PH_RIVER = "file:///home/user/jomo-social/assets/photos/web/plastic-waste-riverbank-01.jpg"
CLOSE_FULL = "Tue 3 Nov, 11:59&nbsp;PM&nbsp;WAT"
ZAMBIA = "12:59 AM Wed 4 Nov in Zambia"

def story(name, label, head, body, sub=""):
    # 9:16 with the space between ~1150 and ~1600 left for the countdown and link stickers
    write(name, pg(f"""
 <style>.foot{{bottom:260px}}</style><div style="height:200px"></div>
 <div class="label">{label}</div>
 <div class="brico" style="font-size:150px;margin-top:40px">{head}</div>
 <div class="body" style="margin-top:44px;font-weight:700;font-size:48px">{body}</div>
 {f'<div class="body" style="margin-top:14px;font-size:36px;opacity:.8">{sub}</div>' if sub else ''}
""", "ink", 0, 0, 1080, 1920))

def x16(name, l1, l2, badge):
    write(name, pg(f"""
 <div class="label">Young Climate Educators Fellowship</div>
 <div class="brico" style="font-size:88px;margin-top:50px;max-width:840px;white-space:nowrap">{l1}<br><span style="color:{LIME}">{l2}</span></div>
 {badge}
""", "ink", 0, 0, 1600, 900))

def word_stamp(word, sub, size=150):
    return f'''<div style="position:absolute;right:62px;top:100px;width:610px;height:610px;border-radius:50%;border:5px dashed {LIME};transform:rotate(-6deg)"></div>
<div class="stamp" style="right:90px;top:128px;width:554px;height:554px;background:{LIME};color:{INK};flex-direction:column;transform:rotate(8deg)">
 <div class="brico" style="font-size:{size}px;letter-spacing:0;line-height:.9">{word}</div><div style="font-size:34px;margin-top:14px">{sub}</div></div>'''

# ===== Sun 1: new month, 2 days left =====
story("w01-ycef-story-9x16", "Happy new month &middot; YCEF",
      f"2 days<br><span style='color:{LIME}'>left to apply.</span>", f"Applications close<br>{CLOSE_FULL}.", ZAMBIA)
x16("w01-ycef-x-16x9", "Happy new month.", "2 days left<br>to apply.", stamp(2))

# ===== Mon 2: closes tomorrow (story with the facilitators carousel) =====
story("w02-ycef-story-9x16", "Young Climate Educators Fellowship",
      f"Closes<br><span style='color:{LIME}'>tomorrow.</span>", f"Applications close<br>{CLOSE_FULL}.", ZAMBIA)

# ===== Tue 3: last call (big swing), stories, LinkedIn, X =====
write("w03-ycef-01", pg(f"""
 <div style="position:absolute;z-index:0;left:0;top:0;width:1080px;height:1350px;background:{INK}"></div>{photo(ONI % '02', 0, 0, 1080, 760, "56% 40%")}{grad('bottom', 45, 1, 0, 760)}
 <div class="chip" style="left:90px;top:90px">Oniwaya clean-up &middot; From our archive</div>
 <div class="c" style="position:absolute;left:90px;right:90px;bottom:160px">
  <div class="label">Young Climate Educators Fellowship</div>
  <div class="brico" style="font-size:150px;margin-top:24px">{st('8 days left.', LIME, 'rgba(244,246,236,.55)', 12)}<br><span style="color:{LIME}">Tonight.</span></div>
  <div class="body" style="margin-top:30px;font-weight:700;font-size:38px">Applications close {CLOSE_FULL}<br><span style="font-weight:400;opacity:.85">{ZAMBIA}</span></div></div>
""", "ink", 0, 0))
story("w03-ycef-story-9x16", "Last call &middot; YCEF",
      f"{st('8 days left.', LIME, 'rgba(244,246,236,.55)', 12)}<br><span style='color:{LIME}'>Tonight.</span>",
      f"Applications close<br>{CLOSE_FULL}.", ZAMBIA)
write("w03-ycef-li-16x9", pg(f"""
 <div class="label">Young Climate Educators Fellowship</div>
 <div class="brico" style="font-size:118px;margin-top:40px">Last call.<br><span style="color:{OFF}">Closes tonight.</span></div>
 <div class="body" style="margin-top:36px;font-weight:700;font-size:40px">{CLOSE_FULL} &middot; {ZAMBIA}</div>
 <div class="body" style="margin-top:14px;font-size:36px">50 fellows &middot; 3 virtual weekends &middot; Nigeria and Zambia &middot; 18+</div>
 <div style="position:absolute;right:90px;top:90px;background:#fff;border-radius:24px;padding:22px 30px"><img src="{LOGO_D}" style="width:250px;display:block"></div>
""", "lime", 0, 0, 1600, 900))
x16("w03-ycef-x-16x9", "Last call.", "Closes tonight,<br>11:59 PM WAT.", word_stamp("Tonight", "11:59 PM WAT", 112))

# ===== Wed 4: applications closed, thank you =====
story("w04-thanks-story-9x16", "Young Climate Educators Fellowship",
      f"Applications<br>are closed.<br><span style='color:{LIME}'>Thank you.</span>",
      "Next: Weekend 1,<br>Fri 13 Nov 2026.")
write("w04-thanks-16x9", pg(f"""
 <div class="label">Young Climate Educators Fellowship</div>
 <div class="brico" style="font-size:118px;margin-top:40px">Applications are closed.<br><span style="color:{LIME}">Thank you.</span></div>
 <div class="body" style="margin-top:36px;font-weight:700;font-size:42px">Next: Weekend 1, Fri 13 Nov 2026.</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:300px">
 {sprout(300, extra="right:80px;top:420px;transform:rotate(-12deg)")}
""", "ink", 0, 0, 1600, 900))

# ===== Thu 5: water needs a way out (World Cities Day framing removed), 4:5 =====
T = 5
write("w05-water-01", pg(f"""
 {photo(LEKKI, 0, 0, 1080, 1350, "33.5% 50%")}{grad('bottom', 85, .97)}{grad('top', 22, .6, 0, 400)}
 <div class="chip" style="left:90px;top:90px">Stock photo &middot; Lekki, Lagos</div>
 <div class="c" style="position:absolute;left:90px;right:90px;bottom:160px">
  <div class="h" style="font-size:150px">{st('Just rain.', th=11)}<br><span class="acc">Water needs<br>a way out.</span></div></div>
""", "ink", 1, T))
write("w05-water-02", pg(f"""
 <div class="label">Where it lands</div>
 <div class="h" style="font-size:136px;margin-top:70px">Heavy rain is<br>a climate risk.</div>
 <div class="h" style="font-size:136px;margin-top:50px;color:{OFF}">A blocked<br>drain is where<br>it lands.</div>
 {sprout(300, color1=OFF, color2=LEAF, extra="right:-50px;top:70px;transform:rotate(16deg);opacity:.9")}
""", "lime", 2, T))
write("w05-water-03", pg(f"""
 <div style="position:absolute;z-index:0;left:0;top:0;width:1080px;height:1350px;background:{INK}"></div>{photo(PH_RIVER, 0, 330, 1080, 1020, "50% 50%")}{grad('top', 40, 1, 330, 1020)}{grad('bottom', 14, .85)}
 <div class="chip" style="left:90px;bottom:160px">Stock photo</div>
 <div class="c"><div class="label">What blocks it</div>
  <div class="h" style="font-size:124px;margin-top:40px">Floods hit where<br>water has<br><span class="acc">nowhere to go.</span></div></div>
""", "ink", 3, T))
write("w05-water-04", pg(f"""
 <div class="label">On your street</div>
 <div class="h" style="font-size:140px;margin-top:60px">Three things<br>you can do</div>
 <div style="margin-top:20px">{tick("Clear the drain<br>outside your gate")}{tick("Report what you<br>can't fix")}{tick("Notice where water<br>collects")}</div>
""", "lime", 4, T))
write("w05-water-05", pg(f"""
 <div class="label">Resilience starts with you</div>
 <div class="h" style="font-size:124px;margin-top:60px">Ready streets<br>are built<br><span class="acc">one drain<br>at a time.</span></div>
 <div class="body" style="margin-top:40px;font-weight:700">Where does water collect on yours?</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:340px">
 {sprout(300, extra="right:-60px;bottom:140px;transform:rotate(-12deg)")}
""", "ink", 5, T))

# ===== Fri 6: COP31 starts Monday, X 16:9 =====
write("w06-cop31-x-16x9", pg(f"""
 <div class="label">Climate, explained locally</div>
 <div class="h" style="font-size:170px;margin-top:40px;line-height:1">COP31</div>
 <div class="h acc" style="font-size:96px;margin-top:20px">starts Monday.</div>
 <div class="body" style="margin-top:30px">9&ndash;20 Nov 2026 &middot; Antalya, T&uuml;rkiye</div>
 {sprout(340, extra="right:80px;top:200px;transform:rotate(-12deg)")}
""", "ink", 0, 0, 1600, 900))

# ===== Sat 7: COP31 explainer for Instagram and Facebook, 4:5 =====
write("w07-cop31-01", pg(f"""
 <div class="label">Climate, explained locally</div>
 <div class="h" style="font-size:190px;margin-top:60px;line-height:.95">COP31</div>
 <div class="h acc" style="font-size:110px;margin-top:20px">starts Monday.</div>
 <div class="body" style="margin-top:50px;max-width:880px">What it is, in 5 slides.</div>
 {sprout(360, extra="right:-60px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 1, T))
write("w07-cop31-02", pg(f"""
 <div class="label">What is a COP?</div>
 <div class="h" style="font-size:136px;margin-top:60px">The yearly UN<br>climate<br>conference.</div>
 <div class="body" style="margin-top:60px;max-width:900px;font-size:50px">COP stands for &ldquo;Conference of the Parties&rdquo;: the countries that have joined the UN climate convention. They meet once a year to agree on how the world responds to climate change.</div>
""", "lime", 2, T))
write("w07-cop31-03", pg(f"""
 <div class="label">When and where</div>
 <div class="h" style="font-size:150px;margin-top:50px">9&ndash;20 Nov<br><span class="acc">2026</span></div>
 <div class="h" style="font-size:110px;margin-top:40px">Antalya, T&uuml;rkiye</div>
 <div class="body" style="margin-top:50px;max-width:880px;font-size:50px">The 31st meeting, so: COP31.</div>
 {sprout(380, extra="right:-60px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 3, T))
write("w07-cop31-04", pg(f"""
 <div class="label">Why it matters on your street</div>
 <div class="h" style="font-size:150px;margin-top:60px">Heat. Floods.<br>Drains. Farms.</div>
 <div class="body" style="margin-top:60px;max-width:900px;font-size:50px">Countries agree targets and money for cutting emissions and for adapting to a hotter climate. That shapes how places like Lagos and Lusaka prepare.</div>
""", "off", 4, T))
write("w07-cop31-05", pg(f"""
 <div class="label">Follow along</div>
 <div class="h" style="font-size:124px;margin-top:60px">We'll explain<br>COP31 in<br><span class="acc">plain language.</span></div>
 <div class="body" style="margin-top:50px;max-width:880px;font-size:46px">What gets decided, and what it could mean for Nigeria and Zambia.</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:340px">
 {sprout(300, extra="right:-50px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 5, T))
print("w1102 written")
