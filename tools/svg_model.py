"""Car model outline for SVG livery drawings (tools/livery_svg.py), taken from a flat side-view drawing.

The reference (an SVG, rendered with headless Edge, or a PNG; transparency is flattened onto white)
is scaled to 2400 px wide and turned nose-left, the view the TV graphics and the livery pack use.
Its pixels are split by colour:

* silhouette: everything that is not white (largest blob, holes filled) -> "body";
* glass: flat dark grey -> "glass" polygons;
* line work: near-black pixels that touch the outline or the glass, or are long -> "dark" polygons
  (the donor drawing's own livery text and small logos fall away; bigger logos are removed with --erase,
  missing lines added with --line);
* wheels: measured by hand on a gridded zoom and given with --wheel cx,cy,tyre,rim (automatic circle
  fits get confused by the arch shadows); they are redrawn by livery_svg.py.

The result is <season>/art/svg/models/<key>.json with the reference's credit and the build
arguments, so the outline can be rebuilt:

    python tools/svg_model.py --season btcc-1991 --key bmw_m3_e30 --ref "<path to svg/png>" --nose right         --source "..." --erase x0,y0,x1,y1 --line x,y,x,y --wheel 421,593,170,138 --wheel 1849,594,170,138

Coordinates for --erase/--line/--wheel are in the 2400 px nose-left frame (write a debug image of the
line layer with --debug and read positions off it).
"""
import sys, json, argparse, pathlib, tempfile, cv2, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from livery_svg import render_png  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--season", required=True); ap.add_argument("--key", required=True); ap.add_argument("--ref", required=True)
ap.add_argument("--nose", default="right"); ap.add_argument("--name", default=""); ap.add_argument("--source", default="")
ap.add_argument("--glass", default="40,60"); ap.add_argument("--lights", action="append", default=[])
ap.add_argument("--keep_dark_min", type=int, default=0); ap.add_argument("--drop", action="append", default=[])
ap.add_argument("--erase", action="append", default=[]); ap.add_argument("--line", action="append", default=[])
ap.add_argument("--wheel", action="append", default=[]); ap.add_argument("--debug", action="store_true")
ap.add_argument("--photo", help="x0,y0,x1,y1: the reference is a photo; cut the car out of this box (GrabCut)")
ap.add_argument("--rectify", help="photo mode: x1,y1,...,x4,y4 = four photo points on the car's side plane "
                "(front wheel centre, rear wheel centre, then the beltline above the rear and the front wheel), mapped to a "
                "true side view before cutting out: straightens three-quarter photos")
ap.add_argument("--smooth", type=int, default=2, help="photo mode: Chaikin passes on hand-traced polygons (round the curves)")
ap.add_argument("--poly", action="append", default=[], help="glass:x,y,... window shape; body:x,y,... hand-traced outline (photo mode, 2400 px nose-left frame)")
a = ap.parse_args()
out_json = REPO / "seasons" / a.season / "art" / "svg" / "models" / f"{a.key}.json"
out_json.parent.mkdir(parents=True, exist_ok=True)
ref = pathlib.Path(a.ref); W2 = 2400
tmp = pathlib.Path(tempfile.gettempdir()) / f"svg_model_{a.key}.png"
if ref.suffix.lower() == ".svg":
    render_png(ref, tmp, W2)
else:
    from PIL import Image
    im = Image.open(ref).convert("RGBA"); im = im.resize((W2, round(W2 * im.height / im.width)), Image.LANCZOS)
    bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im); bg.convert("RGB").save(tmp)
def chaikin(p, n):
    p = np.asarray(p, float)
    for _ in range(n):
        q = np.roll(p, -1, 0); p = np.stack([0.75 * p + 0.25 * q, 0.25 * p + 0.75 * q], 1).reshape(-1, 2)
    return p


def photo_model():
    """Photo reference: crop to the car box, scale to 2400 px wide, nose left, cut the car out with
    GrabCut (the box edge is background). Glass and panel lines are not readable from a photo
    reliably, so they come from --poly glass:... and --line in the same 2400 px frame."""
    src = cv2.imread(str(ref)); x0, y0, x1, y1 = map(int, a.photo.split(","))
    if a.rectify:                               # side plane -> rectangle with the same wheelbase and height
        q = np.array(list(map(float, a.rectify.split(",")))).reshape(4, 2).astype(np.float32)
        wb = float(np.linalg.norm(q[1] - q[0])); hgt = float((np.linalg.norm(q[3] - q[0]) + np.linalg.norm(q[2] - q[1])) / 2)
        dst = np.float32([q[0], q[0] + [wb, 0], q[0] + [wb, -hgt], q[0] + [0, -hgt]])
        src = cv2.warpPerspective(src, cv2.getPerspectiveTransform(q, dst), (src.shape[1] * 2, src.shape[0]),
                                  borderValue=(255, 255, 255))
    mask = np.zeros(src.shape[:2], np.uint8); bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(src, mask, (x0, y0, x1 - x0, y1 - y0), bgd, fgd, 6, cv2.GC_INIT_WITH_RECT)
    fg = np.isin(mask, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.uint8)
    pad = 20; crop = fg[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad]
    k = W2 / crop.shape[1]; crop = cv2.resize(crop, None, fx=k, fy=k, interpolation=cv2.INTER_LINEAR)
    if a.nose == "right": crop = crop[:, ::-1].copy()
    crop = cv2.morphologyEx(crop, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    crop = cv2.morphologyEx(crop, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    crop = cv2.GaussianBlur(crop.astype(np.float32), (15, 15), 0) > 0.5
    n, lab, st, _ = cv2.connectedComponentsWithStats(crop.astype(np.uint8))
    sil = (lab == 1 + np.argmax(st[1:, 4])).astype(np.uint8)
    body = [p for p in a.poly if p.startswith("body:")]
    if body:                                    # hand-traced outline replaces the GrabCut silhouette
        pts = chaikin(np.array(list(map(float, body[0].split(":", 1)[1].split(",")))).reshape(-1, 2), a.smooth)
        sil = np.zeros_like(sil); cv2.fillPoly(sil, [pts.astype(np.int32)], 1)
    cs, _ = cv2.findContours(sil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    H = sil.shape[0]; bx, by, bw, bh = cv2.boundingRect(cs[0])
    glass = [chaikin(np.array(list(map(float, p.split(":", 1)[1].split(",")))).reshape(-1, 2), max(0, a.smooth - 1)).round(1).tolist()
             for p in a.poly if p.startswith("glass:")]
    lines = np.zeros_like(sil)
    for L in a.line:
        pts = np.array(list(map(int, L.split(",")))).reshape(-1, 2); cv2.polylines(lines, [pts], False, 1, 4)
    lines &= cv2.erode(sil, np.ones((5, 5), np.uint8))
    dcs, _ = cv2.findContours(lines, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    wheels = [{"c": [float(v.split(",")[0]), float(v.split(",")[1])], "tyre": float(v.split(",")[2]), "rim": float(v.split(",")[3])} for v in a.wheel]
    out = {"name": a.name, "source": a.source, "build": sys.argv[1:], "size": [W2, H], "bbox": [bx, by, bw, bh],
           "body": cv2.approxPolyDP(cs[0], 1.5, True).reshape(-1, 2).tolist(), "glass": glass,
           "dark": [cv2.approxPolyDP(c, 0.8, True).reshape(-1, 2).tolist() for c in dcs if len(c) >= 3],
           "wheels": wheels, "lights": [], "arch": 1.06}
    json.dump(out, open(out_json, "w", encoding="utf-8"))
    if a.debug:                                 # cut-out over the photo, for checking and reading coordinates
        src2 = src[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad]
        src2 = cv2.resize(src2, (sil.shape[1], sil.shape[0]))
        if a.nose == "right": src2 = src2[:, ::-1]
        dbg = src2.copy(); cv2.drawContours(dbg, cs, -1, (0, 0, 255), 3)
        for g in glass: cv2.polylines(dbg, [np.array(g, np.int32)], True, (0, 255, 255), 3)
        dbg[lines > 0] = (255, 0, 255)
        for w in wheels: cv2.circle(dbg, tuple(map(int, w["c"])), int(w["tyre"]), (0, 255, 0), 3); cv2.circle(dbg, tuple(map(int, w["c"])), int(w["rim"]), (0, 200, 0), 2)
        cv2.imwrite(str(out_json.with_suffix(".debug.png")), dbg); cv2.imwrite(str(out_json.with_suffix(".photo.png")), src2)
    print(out_json, "size", W2, H, "glass", len(glass), "lines", len(a.line), "wheels", wheels)


if a.photo:
    photo_model(); sys.exit()
im = cv2.imread(str(tmp))
if a.nose == "right": im = im[:, ::-1].copy()
H, W = im.shape[:2]
nonwhite = (im.min(2) < 240).astype(np.uint8)
# silhouette: largest component, holes filled
n, lab, st, _ = cv2.connectedComponentsWithStats(nonwhite)
big = 1 + np.argmax(st[1:, 4]); sil = (lab == big).astype(np.uint8)
cs, _ = cv2.findContours(sil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); sil = np.zeros_like(sil); cv2.drawContours(sil, cs, -1, 1, -1)
x0, y0, bw, bh = cv2.boundingRect(cs[0])
def poly(c, eps=1.2): return cv2.approxPolyDP(c, eps, True).reshape(-1, 2).tolist()
gray = im.astype(np.int16); spread = gray.max(2) - gray.min(2); lum = gray.mean(2)
glo, ghi = map(int, a.glass.split(","))
glass = ((lum >= glo) & (lum <= ghi) & (spread < 12) & (sil > 0)).astype(np.uint8)
glass = cv2.morphologyEx(glass, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
gcs, _ = cv2.findContours(glass, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
gcs = [c for c in gcs if cv2.contourArea(c) > 0.002 * bw * bh and cv2.boundingRect(c)[1] < y0 + 0.55 * bh]
black = ((gray.max(2) < 45) & (sil > 0)).astype(np.uint8)
# wheels: big black blobs in the lower half -> circles
wheels = []
g8 = cv2.GaussianBlur((255 - lum).clip(0, 255).astype(np.uint8), (5, 5), 0)
cir = cv2.HoughCircles(g8, cv2.HOUGH_GRADIENT, dp=1, minDist=int(0.4 * bw), param1=120, param2=40,
                       minRadius=int(0.22 * bh), maxRadius=int(0.42 * bh))
for cx, cy, r in (cir[0] if cir is not None else [])[:6]:
    if cy + r < y0 + 0.8 * bh: continue
    # refine tyre radius: walk down from centre until leaving black
    pts = cs[0].reshape(-1, 2).astype(float)
    sel = pts[(pts[:, 1] > cy + 0.3 * r) & (np.abs(pts[:, 0] - cx) < 1.1 * r)]
    for _ in range(3):                                         # circle fit on the tyre's lower arc
        A = np.c_[2 * sel, np.ones(len(sel))]; b = (sel ** 2).sum(1)
        cx, cy, c = np.linalg.lstsq(A, b, rcond=None)[0]; r2 = float(np.sqrt(c + cx * cx + cy * cy))
        res = np.abs(np.hypot(sel[:, 0] - cx, sel[:, 1] - cy) - r2); sel = sel[res < max(3, np.percentile(res, 70))]
    col = lum[int(cy):int(cy + r2), int(cx)]; k = len(col) - 6
    while k > 0 and col[k] < 45: k -= 1
    rim = float(k)
    wheels.append({"c": [round(float(cx), 1), round(float(cy), 1)], "tyre": round(r2, 1), "rim": round(rim, 1)})
wheels = sorted(wheels, key=lambda w: w["c"][0])[:2]
if a.wheel: wheels = [{"c": [float(v.split(',')[0]), float(v.split(',')[1])], "tyre": float(v.split(',')[2]), "rim": float(v.split(',')[3])} for v in a.wheel]
wheels.sort(key=lambda w: w["c"][0])
# dark line work: black minus the wheel discs (slightly enlarged)
lines = black.copy()
for w in wheels: cv2.circle(lines, (int(w["c"][0]), int(w["c"][1])), int(w["tyre"] * 1.02), 0, -1)
for b in a.erase:
    ex0, ey0, ex1, ey1 = map(int, b.split(",")); lines[ey0:ey1, ex0:ex1] = 0
for L in a.line:
    v = list(map(int, L.split(","))); pts = np.array(v).reshape(-1, 2)
    cv2.polylines(lines, [pts], False, 1, 3)
edge = cv2.dilate(sil, np.ones((3, 3), np.uint8)) - cv2.erode(sil, np.ones((9, 9), np.uint8))
gl_d = cv2.dilate(glass, np.ones((9, 9), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(lines)
keep = np.zeros_like(lines)
drops = [tuple(map(int, b.split(","))) for b in a.drop]
for i in range(1, n):
    x, y, w, h, ar = st[i]; m = lab == i
    if any(x >= b[0] and y >= b[1] and x + w <= b[2] and y + h <= b[3] for b in drops): continue
    touches = (edge[m] > 0).any() or (gl_d[m] > 0).any()
    if max(w, h) >= 0.06 * bw or touches:
        keep[m] = 1
        if max(w, h) >= 0.06 * bw and not touches: print("  big free comp", i, (x, y, x + w, y + h))
lines = keep
dcs, _ = cv2.findContours(lines, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
dark = [poly(c, 0.8) for c in dcs if len(c) >= 3]
if a.debug: cv2.imwrite(str(out_json.with_suffix(".debug.png")), 255 - lines * 255)
# arch openings = black area hugging each wheel above it (kept separately for drawing behind the tyre)
lights = []
for spec in a.lights:
    bx0, by0, bx1, by1, col = spec.split(",", 4)
    bx0, by0, bx1, by1 = map(int, (bx0, by0, bx1, by1))
    sub = im[by0:by1, bx0:bx1]; m = (sub.astype(np.int16).max(2) - sub.astype(np.int16).min(2) > 50).astype(np.uint8)
    lc, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in lc:
        if cv2.contourArea(c) > 30: lights.append({"poly": (np.array(poly(c)) + [bx0, by0]).tolist(), "color": col})
out = {"name": a.name, "source": a.source, "build": sys.argv[1:], "size": [W, H], "bbox": [x0, y0, bw, bh], "body": poly(cs[0], 1.0),
       "glass": [poly(c) for c in gcs], "dark": dark, "wheels": wheels, "lights": lights}
json.dump(out, open(out_json, "w", encoding="utf-8"))
print(out_json, "glass", len(gcs), "dark", len(dark), "wheels", wheels)
