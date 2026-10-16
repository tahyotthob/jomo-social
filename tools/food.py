from build import *
RED="#D9442B"
def tomatoes(x,y,scale=1):
    pos=[(0,60),(110,40),(220,70),(60,150),(170,150),(280,160),(115,240),(225,250)]
    out=''
    for i,(a,b) in enumerate(pos):
        cx,cy=x+a*scale,y+b*scale; r=58*scale
        fade = ' opacity=".45"' if i in (5,7) else ''
        out+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{RED}"{fade}/><path d="M{cx-18*scale} {cy-r+6*scale} l18 {14*scale} l18 {-14*scale}" stroke="{LEAF}" stroke-width="{8*scale}" fill="none" stroke-linecap="round"/>'
    return out
write("food-01", page(f"""
  <div class="label">World Food Day &middot; 16 October</div>
  <div class="h" style="font-size:132px;margin-top:60px">What happens<br>to the tomatoes<br><span class="acc">that don't sell?</span></div>
  <div class="body" style="margin-top:44px;max-width:860px">Food that rots in drains and dumpsites<br>is a climate problem too.</div>
  <svg width="900" height="420" viewBox="0 0 900 420" style="position:absolute;left:90px;bottom:160px">
    <rect x="0" y="330" width="900" height="16" rx="8" fill="{CHAR}"/>
    {tomatoes(70,50)}
    <path d="M410 190 H520" stroke="{LIME}" stroke-width="10" stroke-linecap="round"/><path d="M500 165 L530 190 L500 215" stroke="{LIME}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <g transform="translate(560,40)">
      <rect x="0" y="40" width="300" height="250" rx="22" fill="none" stroke="{OFF}" stroke-width="8" stroke-dasharray="22 16"/>
      <text x="150" y="185" text-anchor="middle" font-family="Anton" font-size="64" fill="{LIME}">BIN?</text>
    </g>
  </svg>
""", "ink", 0, 0))
write("food-x-16x9", page(f"""
  <div class="label">World Food Day &middot; 16 October</div>
  <div class="h" style="font-size:120px;margin-top:50px">What happens to the<br><span class="acc">tomatoes that don't sell?</span></div>
  <div class="body" style="margin-top:40px">Food that rots in drains and dumpsites<br>is a climate problem too.</div>
  <svg width="420" height="330" viewBox="0 0 420 330" style="position:absolute;right:70px;bottom:135px">{tomatoes(60,30,.9)}</svg>
""", "ink", 0, 0, 1600, 900))
print("ok")
