from build import *
ZG, ZR, ZB, ZO = "#198A00", "#DE2010", "#000000", "#EF7D00"

def stripes(h, extra):
    # the four flag colours as a band (not a drawing of the flag)
    return "".join(f'<div style="position:absolute;top:0;height:{h}px;width:34px;background:{c};{extra}right:{i*34}px"></div>'
                   for i, c in enumerate([ZO, ZB, ZR, ZG]))

write("zambia-01", page(f"""
  <div class="label">24 October &middot; Zambia Independence Day</div>
  <div class="h" style="font-size:330px;margin-top:40px;line-height:1">62</div>
  <div class="h" style="font-size:140px;margin-top:10px">years.<br><span class="acc">Keep it green.</span></div>
  <div class="body" style="margin-top:50px;max-width:840px">The green on Zambia&rsquo;s flag stands for its farms and lush land. Happy Independence Day to every young Zambian keeping it that way.</div>
  <style>.foot{{right:190px}}</style>{stripes(1350, "")}
  {sprout(320, extra="right:200px;top:150px;transform:rotate(-10deg)")}
  <div class="tape" style="background:{LIME};color:{INK};left:90px;bottom:200px;transform:rotate(-3deg)">Happy Independence Day</div>
""", "ink", 0, 0))

write("zambia-x-16x9", page(f"""
  <div class="label">24 October &middot; Zambia Independence Day</div>
  <div class="h" style="font-size:150px;margin-top:40px;line-height:1">62 years.<br><span class="acc">Keep it green.</span></div>
  <div class="body" style="margin-top:40px;max-width:900px">The green on Zambia&rsquo;s flag stands for its farms and lush land. Happy Independence Day, Zambia.</div>
  <style>.foot{{right:190px}}</style>{stripes(900, "")}
  {sprout(300, extra="right:200px;bottom:150px;transform:rotate(-10deg)")}
""", "ink", 0, 0, 1600, 900))
print("ok")
