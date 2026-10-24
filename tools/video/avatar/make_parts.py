"""Build puppet parts (mouth-open and eyes-closed patches) for Tobi and Amara.
Each Canva variant is aligned to the base image with ORB features and a similarity
transform, then only the mouth or eye region is cut out with a soft-edged mask.
Run from repo root: python3 tools/video/avatar/make_parts.py"""
import cv2, numpy as np, json, pathlib
SRC = pathlib.Path("assets/avatars/puppet/src"); OUT = pathlib.Path("assets/avatars/puppet"); OUT.mkdir(exist_ok=True)
CUT = pathlib.Path("assets/avatars/cutouts")
# face boxes (x0,y0,x1,y1) in the 1080x1440 export frame, and the feature regions inside them
CFG = json.loads(pathlib.Path("tools/video/avatar/parts.json").read_text())

def align(base, var, box):
    x0, y0, x1, y1 = box
    g1 = cv2.cvtColor(base[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY); g2 = cv2.cvtColor(var[y0-40:y1+40, x0-40:x1+40], cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(4000); k1, d1 = orb.detectAndCompute(g1, None); k2, d2 = orb.detectAndCompute(g2, None)
    m = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d1, d2), key=lambda m: m.distance)[:400]
    p1 = np.float32([k1[a.queryIdx].pt for a in m]) + [x0, y0]; p2 = np.float32([k2[a.trainIdx].pt for a in m]) + [x0-40, y0-40]
    M, inl = cv2.estimateAffinePartial2D(p2, p1, method=cv2.RANSAC, ransacReprojThreshold=2.0)
    return cv2.warpAffine(var, M, (base.shape[1], base.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE), M, int(inl.sum())

def soft_ellipse(shape, cx, cy, rx, ry, feather):
    m = np.zeros(shape[:2], np.float32); cv2.ellipse(m, (cx, cy), (rx, ry), 0, 0, 360, 1, -1)
    return cv2.GaussianBlur(m, (0, 0), feather)

report = {}
for name, c in CFG.items():
    base = cv2.imread(str(SRC / f"{name}-base.png"))
    cut = cv2.imread(str(CUT / f"{name}-cutout.png"), cv2.IMREAD_UNCHANGED)  # same 1080x1440 frame, alpha = figure
    for part in [k for k in ("mouth", "closed", "eyes") if k in c]:
        var = cv2.imread(str(SRC / f"{name}-{part}.png"))
        warped, M, inliers = align(base, var, c["face"])
        mask = np.zeros(base.shape[:2], np.float32)
        for e in c[part]:
            mask = np.maximum(mask, soft_ellipse(base.shape, *e))
        img = warped.copy()
        if part == "eyes":
            for (cx, cy, rx, ry) in c.get("lids", []):
                # draw a closed eyelid: skin tone from just under the eye, and a dark lash line
                skin = np.median(base[cy + ry + 4:cy + ry + 10, cx - rx // 2:cx + rx // 2].reshape(-1, 3), axis=0)
                lid = np.zeros(base.shape[:2], np.float32); cv2.ellipse(lid, (cx, cy), (rx + 3, ry + 3), 0, 0, 360, 1, -1)
                lid = cv2.GaussianBlur(lid, (0, 0), 2)[..., None]
                img = (img * (1 - lid) + skin * lid).astype(np.uint8)
                cv2.ellipse(img, (cx, cy - 1), (rx - 4, max(3, ry // 3)), -4, 20, 160, (30, 26, 24), 2, cv2.LINE_AA)
                mask = np.maximum(mask, soft_ellipse(base.shape, cx, cy, rx + 6, ry + 6, 3))
        a = (mask * (cut[:, :, 3] / 255.0)).clip(0, 1)
        rgba = np.dstack([img, (a * 255).astype(np.uint8)]); rgba[rgba[:, :, 3] == 0] = 0  # empty pixels compress to nothing
        cv2.imwrite(str(OUT / f"{name}-{part}-patch.png"), rgba)
        report[f"{name}-{part}"] = {"inliers": inliers, "scale": float(np.hypot(M[0, 0], M[1, 0])), "shift": [float(M[0, 2]), float(M[1, 2])]}
    cv2.imwrite(str(OUT / f"{name}-body.png"), cut)
print(json.dumps(report, indent=1))
