"""Clean photo cut-outs for flyers (Designer).

    python3 tools/cutout.py <photo.jpg> <out.png> [--crop-bottom 0.905] [--model birefnet-portrait]

1. Person mask with rembg (BiRefNet portrait by default: cleanest hair and no stray background blobs).
2. Keep only the large connected shapes (drops specks of leftover background).
3. Choke the soft edge a little and recolour edge pixels from the person's own interior colours,
   so no light or dark fringe from the old background shows on a new one.
"""
import sys, argparse
import numpy as np, cv2
from PIL import Image
from rembg import remove, new_session

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--crop-bottom", type=float, default=1.0, help="keep this fraction of the height (crops off watermarks)")
ap.add_argument("--model", default="birefnet-portrait")
a = ap.parse_args()

im = Image.open(a.src).convert("RGB")
mask = np.asarray(remove(im, session=new_session(a.model), only_mask=True).convert("L")).astype(np.float32) / 255
rgb = np.asarray(im).astype(np.float32)

# 2. keep shapes bigger than 2% of the largest
n, lab, stats, _ = cv2.connectedComponentsWithStats((mask > 0.5).astype(np.uint8), 8)
if n > 1:
    big = stats[1:, cv2.CC_STAT_AREA].max()
    keep = np.zeros(n, bool); keep[1:] = stats[1:, cv2.CC_STAT_AREA] > 0.02 * big
    region = cv2.dilate(keep[lab].astype(np.uint8), np.ones((15, 15), np.uint8))   # keep each shape's soft edge
    mask = mask * region

# 3. choke the edge and decontaminate its colour
alpha = np.clip((mask - 0.12) / 0.83, 0, 1) ** 1.15
inner = (alpha > 0.97).astype(np.float32)
num = cv2.GaussianBlur(rgb * inner[..., None], (0, 0), 6); den = cv2.GaussianBlur(inner, (0, 0), 6)[..., None]
est = num / np.maximum(den, 1e-4)
edge = ((alpha > 0) & (alpha < 0.97))[..., None]
w = np.clip(1 - alpha, 0, 1)[..., None]                       # the softer the pixel, the more it takes the interior colour
out_rgb = np.where(edge, rgb * (1 - w) + est * w, rgb)
out = np.dstack([np.clip(out_rgb, 0, 255), alpha * 255]).astype(np.uint8)

h = int(out.shape[0] * a.crop_bottom)
img = Image.fromarray(out[:h], "RGBA"); img = img.crop(img.getbbox()); img.save(a.out)
print("saved", a.out, img.size)
