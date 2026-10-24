"""Week of 2026-10-26 visuals (Designer). Run: python3 week_1026.py && node render.js
Reuses the helpers and several layouts from week_1016.py with the new YCEF close date (Tue 3 Nov)."""
from week_1016 import pg, st, photo, grad, stamp, item, tick, ONI, LEKKI, BIKE, URL, LOGO_L, LOGO_D
from build import *

CLOSE = "Tue 3 Nov"
CLOSE_FULL = "Tue 3 Nov, 11:59&nbsp;PM&nbsp;WAT"
ZAMBIA = "12:59 AM Wed 4 Nov in Zambia"

# ===== 1. Mon 26: YCEF extension carousel (big swing), 4:5 =====
T = 5
write("w26-ycef-01", pg(f"""
 {photo(ONI % '02', 0, 0, 1080, 1350, "56% 50%")}{grad('bottom', 85, .97)}
 <div class="tape" style="background:{LIME};color:{INK};left:90px;top:110px;transform:rotate(-5deg)">Now closes {CLOSE}</div>
 <div class="c" style="position:absolute;left:90px;right:90px;bottom:160px">
  <div class="brico" style="font-size:120px">{st('Closes today.', LIME, 'rgba(244,246,236,.55)', 10)}<br><span style="color:{LIME}">More time to fix your street.</span></div></div>
""", "ink", 1, T))
write("w26-ycef-02", pg(f"""
 <div class="label">YCEF</div>
 <div class="brico" style="font-size:112px;margin-top:40px"><div style="line-height:1.08">{st('Someone should', INK, 'rgba(30,34,32,.4)', 10)}</div><div style="line-height:1.08">{st('fix it.', INK, 'rgba(30,34,32,.4)', 10)}</div><div style="line-height:1.08">You can.</div></div>
 <div class="body" style="margin-top:30px;font-weight:700;max-width:900px;font-size:38px">That blocked drain, that dump behind the market, that flooded corner.</div>
 {photo(ONI % '11', 90, 720, 900, 480, "50% 52%", "border-radius:28px")}
""", "lime", 2, T))
write("w26-ycef-03", pg(f"""
 {photo(ONI % '08', 0, 0, 1080, 590, "50% 22%")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:620px">
  <div class="label">What fellows do</div>
  {item(1, "Research one hyper-local climate challenge.", 38)}
  {item(2, "Design a youth-led &ldquo;sustenance engineering&rdquo; project: a local fix built to keep running.", 38)}
  {item(3, "Learn to pitch for seed funding.", 38)}
  <div class="label" style="margin-top:34px;opacity:.8">No funding guarantee</div></div>
""", "ink", 3, T))
write("w26-ycef-04", pg(f"""
 <div class="label">Who can apply</div>
 <div class="brico" style="font-size:96px;margin-top:40px">University students and grassroots community volunteers, 18+</div>
 <div class="brico" style="font-size:96px;margin-top:30px;color:{OFF}">Nigeria and Zambia</div>
 <div style="margin-top:44px;border-top:3px solid {INK}">
  <div class="brico" style="font-size:64px;padding:22px 0;border-bottom:3px solid {INK}">50 fellows</div>
  <div class="brico" style="font-size:64px;padding:22px 0;border-bottom:3px solid {INK}">3 virtual weekends</div>
  <div class="brico" style="font-size:64px;padding:22px 0">Weekend 1: Fri 13 Nov 2026</div></div>
""", "lime", 4, T))
write("w26-ycef-05", pg(f"""
 <div class="label">Young Climate Educators Fellowship</div>
 <div class="brico" style="font-size:118px;margin-top:50px">Applications<br>now close<br><span style="color:{LIME}">{CLOSE}.</span></div>
 <div class="body" style="margin-top:24px;font-weight:700;font-size:36px">11:59 PM WAT &middot; {ZAMBIA}</div>
 <div class="label" style="margin-top:44px">Apply</div>
 <div style="margin-top:18px;background:{LIME};color:{INK};font-weight:900;font-size:36px;padding:26px 30px;border-radius:16px;display:inline-block">{URL}</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:380px">
 {sprout(300, extra="right:-50px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 5, T))

# Mon 26 story, 9:16 (space for countdown and link stickers between 1150 and 1600)
write("w26-ycef-story-9x16", pg(f"""
 <style>.foot{{bottom:260px}}</style><div style="height:200px"></div>
 <div class="label">Young Climate Educators Fellowship</div>
 <div class="brico" style="font-size:150px;margin-top:40px">{st('Closes today.', LIME, 'rgba(244,246,236,.55)', 12)}<br><span style="color:{LIME}">More time.</span></div>
 <div class="body" style="margin-top:44px;font-weight:700;font-size:48px">Applications now close<br>{CLOSE_FULL}.</div>
 <div class="body" style="margin-top:14px;font-size:36px;opacity:.8">{ZAMBIA}</div>
""", "ink", 0, 0, 1080, 1920))

# Mon 26 LinkedIn, 16:9 lime
write("w26-ycef-li-16x9", pg(f"""
 <div class="label">Who should apply</div>
 <div class="brico" style="font-size:88px;margin-top:34px;max-width:1100px">University students and grassroots community volunteers, 18+</div>
 <div class="brico" style="font-size:88px;margin-top:20px;color:{OFF}">Nigeria and Zambia</div>
 <div class="body" style="margin-top:36px;font-weight:700;font-size:38px">50 fellows &middot; 3 virtual weekends &middot; Weekend 1: Fri 13 Nov 2026</div>
 <div style="position:absolute;right:90px;top:90px;background:#fff;border-radius:24px;padding:22px 30px"><img src="{LOGO_D}" style="width:250px;display:block"></div>
 <div class="tape" style="background:{INK};color:{LIME};right:90px;bottom:160px;transform:rotate(-3deg);font-size:28px">Applications now close {CLOSE}</div>
""", "lime", 0, 0, 1600, 900))

# Countdown X images
def countdown(name, num, l1, l2):
    write(name, pg(f"""
 <div class="label">Young Climate Educators Fellowship</div>
 <div class="brico" style="font-size:88px;margin-top:50px;max-width:840px;white-space:nowrap">{l1}<br><span style="color:{LIME}">{l2}</span></div>
 {stamp(num)}
""", "ink", 0, 0, 1600, 900))
countdown("w26-ycef-x-16x9", 8, "Deadline extended.", "Apply by<br>Tue 3 Nov.")
countdown("w29-ycef-x-16x9", 5, "Your street,<br>your fix.", "5 days left<br>to apply.")

# ===== 4. Tue 27: rain and drains, X 16:9 =====
write("w27-drain-x-16x9", pg(f"""
 {photo(ONI % '11', 800, 0, 800, 780, "50% 38%")}
 <div class="chip" style="left:830px;bottom:150px;background:{INK};color:{OFF}">Oniwaya clean-up &middot; From our archive</div>
 <div class="label">Climate, explained locally</div>
 <div class="h" style="font-size:96px;margin-top:50px;max-width:700px">Still raining<br>in Lagos?<br><span class="acc">Is your drain<br>ready?</span></div>
""", "ink", 0, 0, 1600, 900))

# ===== 5. Wed 28: Source, please (Media and Information Literacy Week), 4:5 =====
T = 6
write("w28-source-01", pg(f"""
 <div class="label">Media and Information Literacy Week</div>
 <div class="h" style="font-size:210px;margin-top:60px;line-height:.95">Source,<br><span class="acc">please.</span></div>
 <div class="body" style="margin-top:60px;max-width:880px;font-size:54px">3 checks before you share a climate stat.</div>
 {sprout(360, extra="right:-60px;bottom:150px;transform:rotate(-12deg)")}
 <div class="tape" style="background:{LIME};color:{INK};left:90px;bottom:200px;transform:rotate(-4deg)">Swipe &rarr;</div>
""", "ink", 1, T))
def check(n, title, body, theme):
    return pg(f"""
 <div class="label">Check {n} of 3</div>
 <div class="h" style="font-size:180px;margin-top:70px">{title}</div>
 <div class="body" style="margin-top:60px;max-width:880px;font-size:54px">{body}</div>
 <div class="stamp" style="right:90px;bottom:170px;width:240px;height:240px;border:6px solid currentColor;font-size:120px;font-family:Anton;letter-spacing:0">{n}</div>
""", theme, n + 1, T)
write("w28-source-02", check(1, "Who<br>said it?", "Find the original: the study, the agency, the report. Not a screenshot of a screenshot.", "lime"))
write("w28-source-03", check(2, "Count or<br><span class='acc'>projection?</span>", "&ldquo;Deaths&rdquo; and &ldquo;projected deaths&rdquo; are not the same thing. Read the small print.", "ink"))
write("w28-source-04", check(3, "When and<br>where?", "Check the date and the place. A photo from another year or another country can look like today.", "off"))
write("w28-source-05", pg(f"""
 <div class="label">We checked ours</div>
 <div class="h" style="font-size:230px;margin-top:40px;line-height:1">31,400</div>
 <div class="body" style="margin-top:30px;font-size:42px;max-width:880px">Last week we shared this El Ni&ntilde;o figure for Nigeria. Here's what the checks found:</div>
 <div style="margin-top:30px">
  {tick("Who: University of Chicago's<br>Climate Impact Lab")}
  {tick("A projection of extra deaths,<br>not a count")}
  {tick("Sept 2026 to Feb 2027, Nigeria")}
 </div>
""", "lime", 5, T))
write("w28-source-06", pg(f"""
 <div class="label">Before you share</div>
 <div class="h" style="font-size:132px;margin-top:60px">Can't check it?<br><span class="acc">Don't share<br>it yet.</span></div>
 <div class="body" style="margin-top:60px;max-width:880px;font-size:48px">Keep this for the next viral climate stat in the group chat.</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:340px">
 {sprout(320, extra="right:-50px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 6, T))

# ===== 6. Thu 29: Oniwaya before and after, 4:5 =====
T = 4
write("w29-oniwaya-01", pg(f"""
 <div class="label">One drain &middot; Oniwaya</div>
 <div class="brico" style="font-size:150px;margin-top:40px">{st('Blocked.')}<br><span style="color:{LIME}">Cleaned up.</span></div>
 <div style="position:absolute;left:160px;top:560px;width:760px;height:620px;transform:rotate(-2.5deg);border:10px solid {OFF};overflow:hidden;z-index:0;box-shadow:0 20px 40px rgba(0,0,0,.4)">
  <img src="{ONI % '01'}" style="position:absolute;left:0;top:-300px;width:1520px;height:1520px;max-width:none"></div>
 <div class="tape" style="background:{LIME};color:{INK};left:120px;top:520px;transform:rotate(-6deg);z-index:4">Before</div>
""", "ink", 1, T))
write("w29-oniwaya-02", pg(f"""
 <div style="position:absolute;z-index:0;left:0;top:310px;width:1080px;height:920px;overflow:hidden"><img src="{ONI % '01'}" style="position:absolute;left:0;top:-160px;width:1080px;height:1080px;max-width:none"></div>
 <div class="label" style="position:relative;z-index:3;color:{OFF}">Oniwaya &middot; From our archive</div>
 <div class="tape" style="z-index:4;background:{LIME};color:{INK};left:50px;top:200px;font-size:26px;padding:12px 28px;transform:rotate(-3deg)">Before</div>
 <div class="tape" style="z-index:4;background:{LIME};color:{INK};left:590px;top:200px;font-size:26px;padding:12px 28px;transform:rotate(3deg)">After</div>
""", "ink", 2, T))
write("w29-oniwaya-03", pg(f"""
 <div class="label">What it took</div>
 <div class="brico" style="font-size:130px;margin-top:36px">Volunteers with gloves. <span style="color:{OFF}">That's it.</span></div>
 {photo(ONI % '11', 90, 650, 900, 550, "50% 40%", "border-radius:28px")}
""", "lime", 3, T))
write("w29-oniwaya-04", pg(f"""
 <div class="label">Your turn</div>
 <div class="brico" style="font-size:118px;margin-top:40px">Which drain on <span style="color:{LIME}">your street</span> needs this?</div>
 <div class="body" style="margin-top:36px;font-weight:700;font-size:42px">YCEF applications close {CLOSE_FULL}.</div>
 <div style="margin-top:28px;background:{LIME};color:{INK};font-weight:900;font-size:34px;padding:24px 28px;border-radius:16px;display:inline-block">{URL}</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:340px">
""", "ink", 4, T))

# ===== 7 + 9. COP31 explainer: LinkedIn PDF carousel 4:5, X 16:9 =====
T = 5
write("w29-cop31-01", pg(f"""
 <div class="label">Climate, explained locally</div>
 <div class="h" style="font-size:190px;margin-top:60px;line-height:.95">COP31</div>
 <div class="h acc" style="font-size:110px;margin-top:20px">is in 11 days.</div>
 <div class="body" style="margin-top:50px;max-width:880px">What it is, in 5 slides.</div>
 {sprout(360, extra="right:-60px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 1, T))
write("w29-cop31-02", pg(f"""
 <div class="label">What is a COP?</div>
 <div class="h" style="font-size:136px;margin-top:60px">The yearly UN<br>climate<br>conference.</div>
 <div class="body" style="margin-top:60px;max-width:900px;font-size:50px">COP stands for &ldquo;Conference of the Parties&rdquo;: the countries that signed the UN climate convention. They meet once a year to agree on how the world responds to climate change.</div>
""", "lime", 2, T))
write("w29-cop31-03", pg(f"""
 <div class="label">When and where</div>
 <div class="h" style="font-size:150px;margin-top:50px">9&ndash;20 Nov<br><span class="acc">2026</span></div>
 <div class="h" style="font-size:110px;margin-top:40px">Antalya, T&uuml;rkiye</div>
 <div class="body" style="margin-top:50px;max-width:880px;font-size:50px">The 31st meeting, so: COP31.</div>
 {sprout(380, extra="right:-60px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 3, T))
write("w29-cop31-04", pg(f"""
 <div class="label">Why it matters on your street</div>
 <div class="h" style="font-size:150px;margin-top:60px">Heat. Floods.<br>Drains. Farms.</div>
 <div class="body" style="margin-top:60px;max-width:900px;font-size:50px">Countries agree targets and money for cutting emissions and for adapting to a hotter climate. That shapes how places like Lagos and Lusaka prepare.</div>
""", "off", 4, T))
write("w29-cop31-05", pg(f"""
 <div class="label">Follow along</div>
 <div class="h" style="font-size:124px;margin-top:60px">We'll explain<br>COP31 in<br><span class="acc">plain language.</span></div>
 <div class="body" style="margin-top:50px;max-width:880px;font-size:46px">What gets decided, and what it could mean for Nigeria and Zambia.</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:340px">
 {sprout(300, extra="right:-50px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 5, T))
write("w30-cop31-x-16x9", pg(f"""
 <div class="label">Climate, explained locally</div>
 <div class="h" style="font-size:170px;margin-top:40px;line-height:1">COP31</div>
 <div class="h acc" style="font-size:96px;margin-top:20px">starts in 10 days.</div>
 <div class="body" style="margin-top:30px">9&ndash;20 Nov 2026 &middot; Antalya, T&uuml;rkiye</div>
 {sprout(340, extra="right:80px;top:200px;transform:rotate(-12deg)")}
""", "ink", 0, 0, 1600, 900))

# ===== 10. Fri 30: TGIF story, 9:16 (poll sticker goes in the space below the text) =====
write("w30-tgif-story-9x16", pg(f"""
 <style>.foot{{bottom:260px}}</style><div style="height:240px"></div>
 <div class="label">TGIF &middot; one thing for the weekend</div>
 <div class="h" style="font-size:170px;margin-top:40px">Check the<br>drain outside<br><span class="acc">your gate.</span></div>
 <div class="body" style="margin-top:50px;font-size:50px">Bottles, nylon, sachets: put on gloves and pull them out before the next rain.</div>
""", "ink", 0, 0, 1080, 1920))

# ===== 11. Sat 31: World Cities Day carousel (safe homes), 4:5 =====
T = 5
write("w31-cities-01", pg(f"""
 {photo(LEKKI, 0, 0, 1080, 1350, "33.5% 50%")}{grad('bottom', 85, .97)}{grad('top', 22, .6, 0, 400)}
 <div class="chip" style="left:90px;top:90px">Stock photo &middot; Lekki, Lagos</div>
 <div class="tape" style="background:{LIME};color:{INK};right:90px;top:170px;transform:rotate(4deg);font-size:24px">World Cities Day &middot; 31 Oct</div>
 <div class="c" style="position:absolute;left:90px;right:90px;bottom:160px">
  <div class="h" style="font-size:134px">{st('Just rain.', th=11)}<br><span class="acc">A safe home<br>is climate<br>protection.</span></div></div>
""", "ink", 1, T))
write("w31-cities-02", pg(f"""
 <div class="label">Where it lands</div>
 <div class="h" style="font-size:136px;margin-top:70px">Heavy rain is<br>a climate risk.</div>
 <div class="h" style="font-size:136px;margin-top:50px;color:{OFF}">A weak home<br>or a blocked<br>drain is where<br>it lands.</div>
 {sprout(300, color1=OFF, color2=LEAF, extra="right:-50px;top:70px;transform:rotate(16deg);opacity:.9")}
""", "lime", 2, T))
write("w31-cities-03", pg(f"""
 <div style="position:absolute;z-index:0;left:0;top:0;width:1080px;height:1350px;background:{INK}"></div>{photo(BIKE, 0, 330, 1080, 1020, "50% 70%")}{grad('top', 40, 1, 330, 1020)}{grad('bottom', 14, .85)}
 <div class="chip" style="left:90px;bottom:160px">Stock photo</div>
 <div class="c"><div class="label">Water needs a way out</div>
  <div class="h" style="font-size:124px;margin-top:40px">Floods hit where<br>water has<br><span class="acc">nowhere to go.</span></div></div>
""", "ink", 3, T))
write("w31-cities-04", pg(f"""
 <div class="label">On your street</div>
 <div class="h" style="font-size:140px;margin-top:60px">Three things<br>you can do</div>
 <div style="margin-top:20px">{tick("Clear the drain<br>outside your gate")}{tick("Report what you<br>can't fix")}{tick("Notice where water<br>collects")}</div>
""", "lime", 4, T))
write("w31-cities-05", pg(f"""
 <div class="label">World Cities Day</div>
 <div class="h" style="font-size:124px;margin-top:60px">Liveable cities<br>are built<br><span class="acc">one street<br>at a time.</span></div>
 <div class="body" style="margin-top:40px;font-weight:700">Where does water collect on yours?</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:340px">
 {sprout(300, extra="right:-60px;bottom:140px;transform:rotate(-12deg)")}
""", "ink", 5, T))
write("w31-cities-li-16x9", pg(f"""
 {photo(ONI % '02', 820, 0, 780, 780, "56% 50%")}
 <div class="chip" style="left:850px;bottom:150px;background:{INK};color:{OFF}">JOMO volunteers &middot; From our archive</div>
 <div class="label">World Cities Day &middot; 31 October</div>
 <div class="h" style="font-size:100px;margin-top:50px;max-width:700px">Liveable cities<br>are built<br><span class="acc">one street<br>at a time.</span></div>
""", "ink", 0, 0, 1600, 900))
write("w31-cities-x-16x9", pg(f"""
 <div style="position:absolute;z-index:0;left:760px;top:0;width:840px;height:780px;overflow:hidden"><img src="{LEKKI}" style="position:absolute;left:-400px;top:-260px;width:1920px;height:1280px;max-width:none"></div>
 <div class="chip" style="right:40px;top:40px">Stock photo &middot; Lekki, Lagos</div>
 <div class="label">World Cities Day &middot; 31 Oct</div>
 <div class="h" style="font-size:100px;margin-top:50px;max-width:680px">When it rains,<br>where does<br><span class="acc">the water go</span><br>on your street?</div>
""", "ink", 0, 0, 1600, 900))
print("w1026 written")
