"""Week of 2026-11-08 visuals (Designer). Run: python3 week_1108.py && node render.js
COP31 themed days (Mon 9 food and farming, Wed 11 zero waste, Sat 14 youth, education and skills),
YCEF Weekend 1 (Fri 13), and "COP31 starts today" for the explainer that missed Sunday.
Photos: JOMO's own (Oniwaya clean-up, Victoria Graham's birthday clean-up), consent on record."""
from week_1016 import pg, st, photo, grad, ONI, LOGO_L
from build import *

BDAY = "file:///home/user/jomo-social/assets/photos/events/birthday-cleanup-2021/birthday-cleanup-2021-%s.jpg"
COPLINE = "9&ndash;20 Nov 2026 &middot; Antalya, T&uuml;rkiye"

# ===== Mon 9: COP31 starts today (the explainer cover and X image, re-dated) =====
write("w09-cop31-01", pg(f"""
 <div class="label">Climate, explained locally</div>
 <div class="h" style="font-size:190px;margin-top:60px;line-height:.95">COP31</div>
 <div class="h acc" style="font-size:110px;margin-top:20px">starts today.</div>
 <div class="body" style="margin-top:50px;max-width:880px">What it is, in 5 slides.</div>
 {sprout(360, extra="right:-60px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 1, 5))
write("w09-cop31-x-16x9", pg(f"""
 <div class="label">Climate, explained locally</div>
 <div class="h" style="font-size:170px;margin-top:40px;line-height:1">COP31</div>
 <div class="h acc" style="font-size:96px;margin-top:20px">starts today.</div>
 <div class="body" style="margin-top:30px">{COPLINE}</div>
 {sprout(340, extra="right:80px;top:200px;transform:rotate(-12deg)")}
""", "ink", 0, 0, 1600, 900))

# ===== Mon 9: LinkedIn, COP31 Day 1: food, agriculture and health =====
write("w09-cop31-day1", pg(f"""
 <div class="label">COP31 &middot; Day 1</div>
 <div class="h" style="font-size:118px;margin-top:50px">Food.<br>Farming.<br><span class="acc">Health.</span></div>
 <div class="body" style="margin-top:46px;max-width:880px;font-size:44px">Today&rsquo;s COP31 theme. Heat and unpredictable rain change what farmers grow, what reaches the market and what it costs.</div>
 <div class="body" style="margin-top:34px;max-width:880px;font-size:38px;font-weight:700;color:{LIME}">We&rsquo;ll follow the themed days in plain language.</div>
 {sprout(260, extra="right:-40px;top:60px;transform:rotate(14deg)")}
""", "ink", 0, 0))

# ===== Wed 11: X, zero waste day, Oniwaya before/after =====
write("w11-zerowaste-x-16x9", pg(f"""
 <div style="position:absolute;z-index:0;left:760px;top:0;width:840px;height:780px;overflow:hidden"><img src="{ONI % '01'}" style="position:absolute;left:0;top:-150px;width:840px;height:940px;object-fit:cover"></div>
 <div class="chip" style="left:790px;top:30px;background:{INK};color:{OFF}">Oniwaya, Lagos &middot; before / after</div>
 <div class="label">COP31 &middot; Zero waste day</div>
 <div class="h" style="font-size:92px;margin-top:46px;max-width:640px">Zero waste<br>looks like<br><span class="acc">this drain.</span></div>
""", "ink", 0, 0, 1600, 900))

# ===== Fri 13: YCEF Weekend 1 =====
write("w13-weekend1-story-9x16", pg(f"""
 <style>.foot{{bottom:260px}}</style><div style="height:200px"></div>
 <div class="label">Young Climate Educators Fellowship</div>
 <div class="brico" style="font-size:150px;margin-top:40px">Weekend 1<br><span style="color:{LIME}">starts today.</span></div>
 <div class="body" style="margin-top:44px;font-weight:700;font-size:56px">Welcome, fellows. 🌱</div>
 <div class="body" style="margin-top:20px;font-size:38px;opacity:.85">3 virtual weekends &middot; Nigeria and Zambia</div>
""", "ink", 0, 0, 1080, 1920))
write("w13-weekend1-16x9", pg(f"""
 <div class="label">Young Climate Educators Fellowship</div>
 <div class="brico" style="font-size:118px;margin-top:40px">Weekend 1<br><span style="color:{LIME}">starts today.</span></div>
 <div class="body" style="margin-top:34px;font-weight:700;font-size:44px">Welcome, fellows. 🌱</div>
 <div class="body" style="margin-top:12px;font-size:34px;opacity:.85">3 virtual weekends &middot; Nigeria and Zambia</div>
 {sprout(380, extra="right:90px;top:150px;transform:rotate(-12deg)")}
""", "ink", 0, 0, 1600, 900))

# ===== Sat 14: big swing, COP31 youth, education and skills day, 4:5 =====
T = 5
write("w14-edu-01", pg(f"""
 <div style="position:absolute;z-index:0;left:0;top:0;width:1080px;height:1350px;background:{INK}"></div>{photo(ONI % '04', 0, 0, 1080, 740, "50% 22%")}{grad('bottom', 35, 1, 0, 740)}
 <div class="chip" style="right:40px;top:40px">JOMO volunteers &middot; Oniwaya, Lagos</div>
 <div class="tape" style="background:{LIME};color:{INK};left:90px;top:700px;transform:rotate(-2deg);font-size:24px;z-index:4">COP31 &middot; Youth, education &amp; skills</div>
 <div class="c" style="position:absolute;left:90px;right:90px;bottom:160px">
  <div class="h" style="font-size:124px">{st('A classroom subject.', th=10, color='rgba(244,246,236,.6)')}<br><span class="acc">It&rsquo;s your street.</span></div></div>
""", "ink", 1, T))
write("w14-edu-02", pg(f"""
 <div class="label">Today at COP31</div>
 <div class="h" style="font-size:128px;margin-top:60px">Youth.<br>Education.<br>Skills.</div>
 <div class="body" style="margin-top:50px;max-width:900px;font-size:46px">Today&rsquo;s theme is about teaching climate in schools and building &ldquo;green skills&rdquo;: the know-how for work and projects that cut pollution or help communities adapt.</div>
""", "lime", 2, T))
write("w14-edu-03", pg(f"""
 <div class="label">In plain language</div>
 <div class="h" style="font-size:120px;margin-top:60px">Climate<br>literacy <span class="acc">=</span></div>
 <div style="margin-top:40px">
  <div class="body" style="font-size:50px;font-weight:700">knowing what&rsquo;s changing,</div>
  <div class="body" style="font-size:50px;font-weight:700;margin-top:14px">why it&rsquo;s changing,</div>
  <div class="body" style="font-size:50px;font-weight:700;margin-top:14px;color:{LIME}">and what you can do about it.</div></div>
 {sprout(320, extra="right:-50px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 3, T))
write("w14-edu-04", pg(f"""
 <div style="position:absolute;z-index:0;left:0;top:0;width:1080px;height:1350px;background:{INK}"></div>{photo(BDAY % '09', 0, 0, 1080, 760, "50% 35%")}{grad('bottom', 40, 1, 0, 760)}
 <div class="chip" style="left:90px;top:90px">JOMO clean-up &middot; from our archive</div>
 <div class="c" style="position:absolute;left:90px;right:90px;top:780px">
  <div class="label">Some lessons happen outside</div>
  <div class="h" style="font-size:96px;margin-top:24px">Schools. Markets.<br><span class="acc">Drains.</span></div>
  <div class="body" style="margin-top:24px;font-size:38px">JOMO volunteers take climate lessons to the places where climate shows up.</div></div>
""", "ink", 4, T))
write("w14-edu-05", pg(f"""
 <div class="label">Your turn</div>
 <div class="h" style="font-size:124px;margin-top:60px">Where did you<br>first learn about<br><span class="acc">climate change?</span></div>
 <div class="body" style="margin-top:40px;font-weight:700">School, church, mosque, TV, the street? Tell us in the comments.</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:340px">
 {sprout(300, extra="right:-60px;bottom:140px;transform:rotate(-12deg)")}
""", "ink", 5, T))
write("w14-edu-x-16x9", pg(f"""
 {photo(ONI % '04', 820, 0, 780, 780, "50% 40%")}
 <div class="chip" style="left:850px;bottom:150px;background:{INK};color:{OFF}">JOMO volunteers &middot; Oniwaya</div>
 <div class="label">COP31 &middot; Youth, education &amp; skills</div>
 <div class="h" style="font-size:88px;margin-top:46px;max-width:700px">{st('A classroom<br>subject.', th=9, color='rgba(244,246,236,.6)')}<br><span class="acc">It&rsquo;s your street.</span></div>
""", "ink", 0, 0, 1600, 900))
print("w1108 written")
