"""Happy new month: "Welcome to November" (Designer). Run: python3 newmonth.py && node render.js
After the operator's reference posts (May and June 2025): giant month name, a real JOMO volunteer
cut-out in front of it, handle bar at the foot. Pushed louder and younger: crossed-out last month,
tilted tape, hand-drawn sparkles and squiggles.
Cut-outs: assets/photos/cutouts/ (made with rembg from consented Oniwaya clean-up photos).
"""
from build import *

CUT = f"file://{ROOT.parent}/assets/photos/cutouts/oniwaya-cleanup-10-cutout.png"
NOISE = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .09 0'/></filter>"
         "<rect width='300' height='300' filter='url(%23n)'/></svg>\")")

STYLE = f"""<style>
.paper {{ background:{OFF} {NOISE}; }}
.month {{ font-family:Anton; text-transform:uppercase; line-height:.86; letter-spacing:-.01em;
          background:linear-gradient(180deg,{LIME} 0%,{LEAF} 55%,{OLIVE} 100%); -webkit-background-clip:text; background-clip:text; color:transparent;
          filter:drop-shadow(10px 10px 0 {INK}); }}
.cut {{ position:absolute; z-index:3; }}
.bar {{ position:absolute; z-index:6; left:0; right:0; bottom:0; height:130px; background:{INK}; }}
.foot {{ z-index:7; color:{OFF}; border-top:0 !important; }}
.tapeb {{ position:absolute; z-index:5; font-family:Brico; font-weight:800; letter-spacing:-.01em; white-space:nowrap; }}
.doodle {{ position:absolute; z-index:4; }}
</style>"""

def spark(x, y, s, col=INK, rot=0):
    return f'''<svg class="doodle" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)" width="{s}" height="{s}" viewBox="0 0 100 100">
      <path d="M50 4 C54 38 62 46 96 50 C62 54 54 62 50 96 C46 62 38 54 4 50 C38 46 46 38 50 4Z" fill="{col}"/></svg>'''

def squiggle(x, y, w, col=INK, rot=0):
    return f'''<svg class="doodle" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)" width="{w}" height="{w*0.3:.0f}" viewBox="0 0 200 60">
      <path d="M5 40 C25 5 45 5 55 30 S85 55 100 25 S135 0 150 28 S180 50 195 20" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round"/></svg>'''

def feed():
    body = f"""{STYLE}
 <div style="position:absolute;inset:0" class="paper"></div>
 <div style="position:absolute;z-index:2;left:90px;top:96px;font-family:Anton;font-size:64px;text-transform:uppercase;color:rgba(30,34,32,.42)">
   <span style="text-decoration:line-through;text-decoration-thickness:9px;text-decoration-color:{LIME}">October</span></div>
 <div class="tapeb" style="left:380px;top:84px;background:{INK};color:{LIME};font-size:58px;padding:12px 34px 18px;transform:rotate(-4deg)">Happy new month</div>
 <div class="tapeb" style="left:86px;top:220px;background:{LIME};color:{INK};font-size:44px;padding:8px 26px 12px;transform:rotate(2deg);z-index:5">Welcome to</div>
 <div class="month" style="position:absolute;z-index:1;left:62px;top:312px;font-size:248px">November</div>
 {spark(930, 200, 100, INK, 12)}{spark(990, 610, 56, OLIVE, 0)}
 <img class="cut" src="{CUT}" style="left:150px;bottom:110px;height:800px">
 <div class="tapeb" style="left:56px;top:640px;background:{OFF};color:{INK};font-size:34px;padding:10px 22px 14px;transform:rotate(-7deg);border:4px solid {INK};z-index:5">New month.<br>New fix. 🌱</div>
 {squiggle(40, 790, 150, LIME, -10)}
 <div class="bar"></div>
"""
    return page(body, "ink", 0, 0).replace('<div class="s ink">', '<div class="s ink" style="background:transparent">')

def story():
    # top 250 px and bottom 250 px are covered by the app; 380-560 is left empty for the countdown and link stickers
    body = f"""{STYLE}
 <style>.bar{{height:400px}} .foot{{bottom:270px}}</style>
 <div style="position:absolute;inset:0" class="paper"></div>
 <div class="tapeb" style="left:90px;top:280px;background:{OFF};color:{INK};font-size:40px;padding:10px 22px 14px;transform:rotate(-2deg);border:4px solid {INK}">YCEF: 2 days left to apply</div>
 <div style="position:absolute;z-index:2;left:90px;top:590px;font-family:Anton;font-size:72px;text-transform:uppercase;color:rgba(30,34,32,.42)">
   <span style="text-decoration:line-through;text-decoration-thickness:10px;text-decoration-color:{LIME}">October</span></div>
 <div class="tapeb" style="left:400px;top:600px;background:{INK};color:{LIME};font-size:60px;padding:12px 30px 18px;transform:rotate(-4deg)">Happy new month</div>
 <div class="tapeb" style="left:90px;top:735px;background:{LIME};color:{INK};font-size:48px;padding:8px 26px 12px;transform:rotate(2deg);z-index:5">Welcome to</div>
 <div class="month" style="position:absolute;z-index:1;left:62px;top:830px;font-size:248px">November</div>
 {spark(930, 300, 100, INK, 12)}{spark(990, 1120, 56, OLIVE, 0)}{squiggle(40, 1300, 150, LIME, -10)}
 <img class="cut" src="{CUT}" style="left:170px;bottom:400px;height:610px">
 <div class="bar"></div>
"""
    return page(body, "ink", 0, 0, 1080, 1920).replace('<div class="s ink">', '<div class="s ink" style="background:transparent">')

def x16():
    body = f"""{STYLE}
 <div style="position:absolute;inset:0" class="paper"></div>
 <div style="position:absolute;z-index:2;left:90px;top:80px;font-family:Anton;font-size:56px;text-transform:uppercase;color:rgba(30,34,32,.42)">
   <span style="text-decoration:line-through;text-decoration-thickness:8px;text-decoration-color:{LIME}">October</span></div>
 <div class="tapeb" style="left:360px;top:70px;background:{INK};color:{LIME};font-size:52px;padding:10px 30px 16px;transform:rotate(-3deg)">Happy new month</div>
 <div class="month" style="position:absolute;z-index:1;left:60px;top:190px;font-size:250px">November</div>
 {spark(1440, 60, 100, INK, 12)}{squiggle(80, 600, 180, LIME, -6)}
 <img class="cut" src="{CUT}" style="left:700px;bottom:110px;height:690px">
 <div class="bar" style="height:120px"></div>
"""
    return page(body, "ink", 0, 0, 1600, 900).replace('<div class="s ink">', '<div class="s ink" style="background:transparent">')

write("nm-november-01", feed())
write("nm-november-story-9x16", story())
write("nm-november-x-16x9", x16())
print("new month written")
