"""Week of 2026-10-16 visuals (Designer). Run: python3 week_1016.py && node render.js"""
from build import *

PH = "file:///home/user/jomo-social/assets/photos/"
LOGO_L = "file:///home/user/jomo-social/assets/logos/jomo-logo-light.png"
LOGO_D = "file:///home/user/jomo-social/assets/logos/jomo-logo.png"
ONI = PH + "events/oniwaya-cleanup/oniwaya-cleanup-%s.jpg"
LEKKI = PH + "web/flood-street-lekki-lagos-01.jpg"
BIKE = PH + "web/flood-bicycle-goods-01.jpg"
URL = "https://jomoclimatechange.org/events?apply=ycef"
EXTRA = ".foot{z-index:5}.c{position:relative;z-index:3}.chip{position:absolute;z-index:4;background:%s;color:%s;font-weight:900;font-size:22px;letter-spacing:.18em;text-transform:uppercase;padding:12px 20px}" % (OFF, INK)

def pg(body, theme, n, total, w=1080, h=1350):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}{EXTRA}</style></head>
<body><div class="s {theme}">{body}{foot(theme, n, total)}</div></body></html>"""

def st(txt, line=LIME, color=None, th=9):
    c = f"color:{color};" if color else ""
    return f'<span style="{c}text-decoration:line-through;text-decoration-thickness:{th}px;text-decoration-color:{line}">{txt}</span>'

def photo(src, x, y, w, h, pos="50% 50%", extra=""):
    return f'<div style="position:absolute;z-index:0;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:hidden;{extra}"><img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block"></div>'

def grad(frm, to_stop, a=.94, y0=0, h=1350, w=1080):
    # frm: 'bottom' or 'top'
    d = "to top" if frm == "bottom" else "to bottom"
    return f'<div style="position:absolute;z-index:1;left:0;top:{y0}px;width:{w}px;height:{h}px;background:linear-gradient({d},rgba(30,34,32,{a}) 0%,rgba(30,34,32,{a*.85}) {to_stop*.5}%,rgba(30,34,32,0) {to_stop}%)"></div>'

def stamp(num, w=1600):
    return f'''<div style="position:absolute;right:62px;top:100px;width:610px;height:610px;border-radius:50%;border:5px dashed {LIME};transform:rotate(-6deg)"></div>
<div class="stamp" style="right:90px;top:128px;width:554px;height:554px;background:{LIME};color:{INK};flex-direction:column;transform:rotate(8deg)">
 <div class="brico" style="font-size:380px;letter-spacing:0;line-height:.85">{num}</div><div style="font-size:38px;margin-top:6px">days left</div></div>'''

def item(n, txt, size=40):
    return f'''<div style="display:flex;gap:28px;align-items:flex-start;margin-top:34px">
 <div style="flex:none;width:64px;height:64px;border-radius:50%;background:{LIME};color:{INK};font-weight:900;font-size:32px;display:flex;align-items:center;justify-content:center">{n}</div>
 <div style="font-size:{size}px;line-height:1.28;font-weight:700;padding-top:4px">{txt}</div></div>'''

# ===== 1. World Food Day X, 1080x1080 =====
write("p1-food-day-1x1", pg(f"""
 <div class="label">World Food Day &middot; 16 October</div>
 {sprout(190, extra="right:70px;top:14px;transform:rotate(14deg)")}
 <div class="h" style="font-size:148px;margin-top:80px">{st('Food security.', th=11)}<br><span class="acc">Food on<br>your street.</span></div>
 <div class="body" style="margin-top:34px;max-width:880px;font-size:40px">What's one thing your street could grow, fix or stop wasting?</div>
""", "ink", 0, 0, 1080, 1080))

# ===== 2. Safe homes carousel =====
T = 5
write("p2-safe-01", pg(f"""
 {photo(LEKKI, 0, 0, 1080, 1350, "40% 50%")}{grad('bottom', 85, .97)}{grad('top', 22, .6, 0, 400)}
 <div class="chip" style="left:90px;top:90px">Stock photo &middot; Lekki, Lagos</div>
 <div class="c" style="position:absolute;left:90px;right:90px;bottom:160px">
  <div class="h" style="font-size:134px">{st('Just rain.', th=11)}<br><span class="acc">A safe home<br>is climate<br>protection.</span></div></div>
""", "ink", 1, T))
write("p2-safe-02", pg(f"""
 <div class="label">Where it lands</div>
 <div class="h" style="font-size:136px;margin-top:70px">Heavy rain is<br>a climate risk.</div>
 <div class="h" style="font-size:136px;margin-top:50px;color:{OFF}">A weak home<br>or a blocked<br>drain is where<br>it lands.</div>
 {sprout(300, color1=OFF, color2=LEAF, extra="right:-50px;top:70px;transform:rotate(16deg);opacity:.9")}
""", "lime", 2, T))
write("p2-safe-03", pg(f"""
 <div style="position:absolute;z-index:0;left:0;top:0;width:1080px;height:1350px;background:{INK}"></div>{photo(BIKE, 0, 330, 1080, 1020, "50% 70%")}{grad('top', 40, 1, 330, 1020)}{grad('bottom', 14, .85)}
 <div class="chip" style="left:90px;bottom:160px">Stock photo</div>
 <div class="c"><div class="label">Water needs a way out</div>
  <div class="h" style="font-size:124px;margin-top:40px">Floods hit where<br>water has<br><span class="acc">nowhere to go.</span></div></div>
""", "ink", 3, T))
def tick(txt):
    return f'''<div style="display:flex;align-items:flex-start;gap:30px;margin-top:46px">
 <div style="flex:none;width:76px;height:76px;border-radius:50%;background:{INK};display:flex;align-items:center;justify-content:center">
 <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="{LIME}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg></div>
 <div style="font-size:50px;font-weight:700;line-height:1.2;padding-top:2px">{txt}</div></div>'''
write("p2-safe-04", pg(f"""
 <div class="label">On your street</div>
 <div class="h" style="font-size:140px;margin-top:60px">Three things<br>you can do</div>
 <div style="margin-top:20px">{tick("Clear the drain<br>outside your gate")}{tick("Report what you<br>can't fix")}{tick("Notice where water<br>collects")}</div>
""", "lime", 4, T))
write("p2-safe-05", pg(f"""
 <div class="label">Tell us</div>
 <div class="h" style="font-size:134px;margin-top:60px">Where does<br><span class="acc">water collect</span><br>on your street?</div>
 <div class="body" style="margin-top:44px;font-weight:700">Tell us in the comments.</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:380px">
 {sprout(380, extra="right:-60px;bottom:140px;transform:rotate(-12deg)")}
""", "ink", 5, T))

# ===== 3. Safe homes X, 1600x900 =====
write("p3-safe-x-16x9", pg(f"""
 {photo(LEKKI, 760, 0, 840, 780, "58% 50%")}
 <div class="chip" style="right:40px;top:40px">Stock photo &middot; Lekki, Lagos</div>
 <div class="label">Climate, explained locally</div>
 <div class="h" style="font-size:100px;margin-top:50px;max-width:680px">When it rains,<br>where does<br><span class="acc">the water go</span><br>on your street?</div>
""", "ink", 0, 0, 1600, 900))

# ===== 4. Blocked drain X =====
write("p4-drain-x-16x9", pg(f"""
 {photo(ONI % '11', 800, 0, 800, 780, "50% 38%")}
 <div class="chip" style="left:830px;bottom:150px;background:{INK};color:{OFF}">Oniwaya cleanup &middot; From our archive</div>
 <div class="label">Climate, explained locally</div>
 <div class="h" style="font-size:104px;margin-top:50px;max-width:700px">That blocked<br>drain is a<br><span class="acc">flood waiting<br>for rain.</span></div>
""", "ink", 0, 0, 1600, 900))

# ===== 5. YCEF countdown carousel =====
T = 5
write("p5-ycef-01", pg(f"""
 {photo(ONI % '02', 0, 0, 1080, 1350, "56% 50%")}{grad('bottom', 85, .97)}
 <div class="tape" style="background:{LIME};color:{INK};left:90px;top:110px;transform:rotate(-5deg)">5 days left</div>
 <div class="c" style="position:absolute;left:90px;right:90px;bottom:160px">
    <div class="brico" style="font-size:118px">Your street has a climate problem. <span style="color:{LIME}">You've got the fix.</span></div></div>
""", "ink", 1, T))
write("p5-ycef-02", pg(f"""
 <div class="label">YCEF</div>
 <div class="brico" style="font-size:112px;margin-top:40px"><div style="line-height:1.08">{st('Someone should', INK, 'rgba(30,34,32,.4)', 10)}</div><div style="line-height:1.08">{st('fix it.', INK, 'rgba(30,34,32,.4)', 10)}</div><div style="line-height:1.08">You can.</div></div>
 <div class="body" style="margin-top:30px;font-weight:700;max-width:900px;font-size:38px">That blocked drain, that dump behind the market, that flooded corner.</div>
 {photo(ONI % '11', 90, 720, 900, 480, "50% 52%", "border-radius:28px")}
""", "lime", 2, T))
write("p5-ycef-03", pg(f"""
 {photo(ONI % '08', 0, 0, 1080, 590, "50% 22%")}
 <div class="c" style="position:absolute;left:90px;right:90px;top:620px">
  <div class="label">What fellows do</div>
  {item(1, "Research one hyper-local climate challenge.", 38)}
  {item(2, "Design a youth-led &ldquo;sustenance engineering&rdquo; project: a local fix built to keep running.", 38)}
  {item(3, "Learn to pitch for seed funding.", 38)}
  <div class="label" style="margin-top:34px;opacity:.8">No funding guarantee</div></div>
""", "ink", 3, T))
write("p5-ycef-04", pg(f"""
 <div class="label">Who can apply</div>
 <div class="brico" style="font-size:96px;margin-top:40px">University students and grassroots community volunteers, 18+</div>
 <div class="brico" style="font-size:96px;margin-top:30px;color:{OFF}">Nigeria and Zambia</div>
 <div style="margin-top:44px;border-top:3px solid {INK}">
  <div class="brico" style="font-size:64px;padding:22px 0;border-bottom:3px solid {INK}">50 fellows</div>
  <div class="brico" style="font-size:64px;padding:22px 0;border-bottom:3px solid {INK}">3 virtual weekends</div>
  <div class="brico" style="font-size:64px;padding:22px 0">Weekend 1: Fri 13 Nov 2026</div></div>
""", "lime", 4, T))
write("p5-ycef-05", pg(f"""
 <div class="label">Young Climate Educators Fellowship</div>
 <div class="brico" style="font-size:124px;margin-top:50px">Applications<br>close<br><span style="color:{LIME}">Mon 26 Oct.</span></div>
 <div class="label" style="margin-top:56px">Apply</div>
 <div style="margin-top:18px;background:{LIME};color:{INK};font-weight:900;font-size:36px;padding:26px 30px;border-radius:16px;display:inline-block">{URL}</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:380px">
 {sprout(340, extra="right:-50px;bottom:150px;transform:rotate(-12deg)")}
""", "ink", 5, T))

# ===== 6. YCEF LinkedIn, 1600x900 lime =====
write("p6-ycef-li-16x9", pg(f"""
 <div class="label">Who should apply</div>
 <div class="brico" style="font-size:88px;margin-top:34px;max-width:1100px">University students and grassroots community volunteers, 18+</div>
 <div class="brico" style="font-size:88px;margin-top:20px;color:{OFF}">Nigeria and Zambia</div>
 <div class="body" style="margin-top:36px;font-weight:700;font-size:38px">50 fellows &middot; 3 virtual weekends &middot; Weekend 1: Fri 13 Nov 2026</div>
 <div style="position:absolute;right:90px;top:90px;background:#fff;border-radius:24px;padding:22px 30px"><img src="{LOGO_D}" style="width:250px;display:block"></div>
 <div class="tape" style="background:{INK};color:{LIME};right:90px;bottom:160px;transform:rotate(-3deg);font-size:28px">Applications close Mon 26 Oct</div>
""", "lime", 0, 0, 1600, 900))

# ===== 7 and 9. Countdown X =====
def countdown(name, num, l1, l2):
    write(name, pg(f"""
 <div class="label">Young Climate Educators Fellowship</div>
 <div class="brico" style="font-size:88px;margin-top:50px;max-width:840px;white-space:nowrap">{l1}<br><span style="color:{LIME}">{l2}</span></div>
 {stamp(num)}
""", "ink", 0, 0, 1600, 900))
countdown("p7-ycef-close-x-16x9", 5, "Applications close<br>Mon 26 Oct.", "Your street's fix<br>starts here.")
countdown("p9-ycef-last-x-16x9", 4, "Your street,<br>your fix.", "4 days left<br>to apply.")

# ===== 8. Oniwaya before/after carousel =====
T = 4
write("p8-oniwaya-01", pg(f"""
 <div class="label">One drain &middot; Oniwaya</div>
 <div class="brico" style="font-size:150px;margin-top:40px">{st('Blocked.')}<br><span style="color:{LIME}">Cleared.</span></div>
 <div style="position:absolute;left:160px;top:560px;width:760px;height:620px;transform:rotate(-2.5deg);border:10px solid {OFF};overflow:hidden;z-index:0;box-shadow:0 20px 40px rgba(0,0,0,.4)">
  <img src="{ONI % '01'}" style="position:absolute;left:0;top:-300px;width:1520px;height:1520px;max-width:none"></div>
 <div class="tape" style="background:{LIME};color:{INK};left:120px;top:520px;transform:rotate(-6deg);z-index:4">Before</div>
""", "ink", 1, T))
write("p8-oniwaya-02", pg(f"""
 {photo(ONI % '01', 0, 150, 1080, 1080)}
 <div class="label" style="position:relative;z-index:3;color:{OFF}">Oniwaya &middot; From our archive</div>
 <div class="tape" style="z-index:4;background:{LIME};color:{INK};left:50px;top:172px;font-size:26px;padding:12px 28px;transform:rotate(-3deg)">Before</div>
 <div class="tape" style="z-index:4;background:{LIME};color:{INK};left:590px;top:172px;font-size:26px;padding:12px 28px;transform:rotate(3deg)">After</div>
""", "ink", 2, T))
write("p8-oniwaya-03", pg(f"""
 <div class="label">What it took</div>
 <div class="brico" style="font-size:130px;margin-top:36px">Volunteers, gloves, rakes. <span style="color:{OFF}">That's it.</span></div>
 {photo(ONI % '11', 90, 640, 900, 560, "50% 52%", "border-radius:28px")}
""", "lime", 3, T))
write("p8-oniwaya-04", pg(f"""
 <div class="label">Your turn</div>
 <div class="brico" style="font-size:118px;margin-top:40px">Which drain on <span style="color:{LIME}">your street</span> needs this?</div>
 <div class="body" style="margin-top:36px;font-weight:700;font-size:42px">YCEF applications close Mon 26 Oct.</div>
 <div style="margin-top:28px;background:{LIME};color:{INK};font-weight:900;font-size:34px;padding:24px 28px;border-radius:16px;display:inline-block">{URL}</div>
 <img src="{LOGO_L}" style="position:absolute;left:90px;bottom:170px;width:340px">
""", "ink", 4, T))
print("w1016 written")
