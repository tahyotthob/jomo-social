from build import *
PHOTO = f"file://{ROOT}/../assets/photos/web/cracked-earth-nigeria-01.jpg"
T = 6

def photo_bg(pos="center 60%", fade=".35,.92"):
    a, b = fade.split(",")
    return f'''<img src="{PHOTO}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos}">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,34,32,{a}) 0%,rgba(30,34,32,{b}) 70%)"></div>'''

def rel(html):  # keep content above the photo layer
    return f'<div style="position:relative">{html}</div>'

write("elnino-01", page(photo_bg() + rel(f"""
  <div class="label">Climate, explained locally</div>
  <div class="h" style="font-size:150px;margin-top:70px">Super<br>El Ni&ntilde;o<br>is here.</div>
  <div class="h acc" style="font-size:112px;margin-top:40px">Is your family<br>ready for<br>the heat?</div>
""") + f"""
  <div class="tape" style="background:{LIME};color:{INK};left:90px;bottom:190px;transform:rotate(-4deg)">Swipe &rarr;</div>
  <div class="label" style="position:absolute;right:90px;bottom:150px;font-size:18px;opacity:.7">Stock photo: Jonathan Yakubu / Pexels</div>
""", "ink", 1, T))

write("elnino-02", page(f"""
  <div class="label">The projection</div>
  <div class="h" style="font-size:330px;margin-top:50px;line-height:1">31,400</div>
  <div class="h" style="font-size:104px;margin-top:50px">more heat-related<br>deaths in Nigeria</div>
  <div class="body" style="margin-top:56px;font-weight:700;font-size:44px">September 2026 to February 2027,<br>compared with an average year.</div>
  <div class="body" style="margin-top:60px;font-size:32px;max-width:880px">Source: Climate Impact Lab, University of Chicago, Sept 2026. A model projection, not a count, and not yet peer-reviewed.</div>
""", "lime", 2, T))

write("elnino-03", page(f"""
  <div class="label">Wait, what is El Ni&ntilde;o?</div>
  <div class="body" style="margin-top:50px;font-size:50px">A natural warming of the Pacific Ocean that shifts weather around the world.</div>
  <div class="h" style="font-size:132px;margin-top:70px">This one is<br><span class="acc">unusually strong.</span></div>
  <div class="body" style="margin-top:50px;font-size:42px">US weather agency NOAA puts the chance of a strong to very strong El Ni&ntilde;o through March 2027 at more than 83%.</div>
  <div class="body" style="margin-top:50px;font-size:36px;opacity:.8">Researchers call this heat a &ldquo;postcard from the future&rdquo;: close to what climate change is projected to bring in about 20 years.</div>
""", "ink", 3, T))

def who(txt):
    return f'<div style="font-size:50px;font-weight:900;line-height:1.15;padding:22px 0;border-bottom:3px solid rgba(30,34,32,.18)">{txt}</div>'
write("elnino-04", page(f"""
  <div class="label">Heat hits some people harder</div>
  <div class="h" style="font-size:120px;margin-top:50px">Who to<br><span class="acc">look out for</span></div>
  <div style="margin-top:40px">{who("People over 65")}{who("Babies and young children")}{who("People with heart, lung or kidney conditions")}{who("Outdoor workers: traders, farmers, bike riders")}{who("Anyone who lives alone")}</div>
""", "off", 4, T))

def check(txt):
    return f'''<div style="display:flex;align-items:center;gap:30px;margin-top:30px">
      <div style="flex:none;width:72px;height:72px;border-radius:50%;background:{INK};display:flex;align-items:center;justify-content:center">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="{LIME}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg></div>
      <div style="font-size:40px;font-weight:700;line-height:1.2">{txt}</div></div>'''
write("elnino-05", page(f"""
  <div class="label">5 heat-smart habits</div>
  <div class="h" style="font-size:112px;margin-top:40px">Heat no be<br>small thing.</div>
  <div style="margin-top:20px">
    {check("Drink water all day: 2 to 3 litres")}
    {check("Skip hard work in the hottest hours.<br>Find shade.")}
    {check("Open windows at night, close them<br>and block the sun by day")}
    {check("Light, loose clothes. Cool showers.")}
    {check("Never leave a child in a parked car")}
  </div>
""", "lime", 5, T))

write("elnino-06", page(f"""
  <div class="label">Know the danger signs</div>
  <div class="h" style="font-size:118px;margin-top:50px">Confused?<br>Fainting? Hot,<br><span class="acc">dry skin?</span></div>
  <div class="body" style="margin-top:44px;font-weight:700">That's an emergency. Get medical help fast and cool the person down.</div>
  <div class="body" style="margin-top:50px;font-size:36px;max-width:860px">A projection is not destiny. This week, check on one older neighbour, and follow NiMet for heat updates in your state.</div>
  {sprout(260, extra="right:-30px;top:120px;transform:rotate(14deg);opacity:.9")}
""", "ink", 6, T))

write("elnino-x-16x9", page(photo_bg("center 50%", ".55,.9") + rel(f"""
  <div class="label">Climate, explained locally</div>
  <div class="h" style="font-size:200px;margin-top:30px;line-height:1">31,400</div>
  <div class="h acc" style="font-size:84px;margin-top:34px">more heat-related deaths<br>projected in Nigeria</div>
  <div class="body" style="margin-top:26px;font-size:32px">Sept 2026 to Feb 2027 &middot; Climate Impact Lab, University of Chicago &middot; not yet peer-reviewed</div>
"""), "ink", 0, 0, 1600, 900))

write("elnino-story-9x16", page(f"""
  <div style="height:360px"></div>
  <div class="label">Super El Ni&ntilde;o &middot; heat check</div>
  <div class="h" style="font-size:170px;margin-top:50px">Who are you<br><span class="acc">checking on</span><br>this week?</div>
  <div class="body" style="margin-top:70px;font-size:54px">Grandma. The baby. The neighbour who lives alone. The trader in the sun all day.</div>
  <div class="body" style="margin-top:60px;font-weight:700;font-size:54px">Water. Shade. A cool room.<br>And a knock on the door.</div>
""", "ink", 0, 0, 1080, 1920))
print("ok")
