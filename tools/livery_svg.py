"""Side-view livery drawings as SVG, in the style of the dtm.fandom / Oliver Pohlmann car drawings:
flat colours, black outline and panel lines, nose left.

Per season:
  art/svg/models/<model>.json    car outline: body, glass, line work, wheels (tools/svg_model.py)
  art/svg/liveries/<NN>.json     one car: "model", base colour, colour shapes, texts, number board,
                                 wheel colour/style; coordinates in the model's 2400 px frame
  -> art/svg/<NN>.svg            the drawing (tools/livery_status.py shows it as a final drawing)
  -> build/art/<season>/svg/<NN>.png   preview render (headless Edge), for the status page

Wheels: "wheel" = "star" (with "spokes", "spoke_w" = spoke width as a share of the rim radius, or "gap"/"taper"
for wedge windows, "hub", "outer", "twist" = sweep in degrees, "window", "lip"), "cross" (BBS mesh), "dish" or
"spoke"; "rim" is the rim colour. Take the rim design and colour from a photo of the car standing still
(grid, paddock), not from action shots, where wheels blur.

Livery layers are clipped to the body; glass, line work, lights, wheels and the outline go on top,
then "over_glass"/"over_texts" (window banners). Liveries are read from every reference we have for
the car: the TV graphics drawings (~/Pictures/mods/<season>/tv_artwork), the livery pack frames and
photos, and livery_pack/liveries.csv.

    python tools/livery_svg.py --season btcc-1991 [--car 11 | --car 44_soper] [--no-render] [--compare [--ref PICTURE]]

Files are named <NN>_<surname> (one drawing per driver: shared cars get one per driver, with that
driver's name on the window).
"""
import sys, json, math, html, argparse, pathlib, subprocess, tempfile

REPO = pathlib.Path(__file__).resolve().parents[1]
EDGE = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"


def render_png(svg, png, width):
    """Render an SVG file to PNG with headless Edge (no SVG library needed)."""
    import re
    s = pathlib.Path(svg).read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'viewBox="([\d.\-e ]+)"', s)
    if m:
        vw, vh = map(float, m.group(1).split()[2:])
    else:
        vw = float(re.search(r'<svg[^>]*?\swidth="([\d.]+)', s, re.S).group(1))
        vh = float(re.search(r'<svg[^>]*?\sheight="([\d.]+)', s, re.S).group(1))
    h = int(width * vh / vw)
    import os, uuid, shutil
    tag = f"{pathlib.Path(svg).stem}_{os.getpid()}_{uuid.uuid4().hex[:6]}"     # unique: renders may run in parallel
    page = pathlib.Path(tempfile.gettempdir()) / f"livery_svg_{tag}.html"
    prof = pathlib.Path(tempfile.gettempdir()) / f"livery_svg_edge_{tag}"
    page.write_text(f'<html><body style="margin:0;background:#fff"><img src="{pathlib.Path(svg).resolve().as_uri()}" '
                    f'style="width:{width}px;height:{h}px;display:block"></body></html>', encoding="utf-8")
    pathlib.Path(png).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={width},{h}",
                    f"--screenshot={pathlib.Path(png).resolve()}", "--allow-file-access-from-files", f"--user-data-dir={prof}", page.as_uri()],
                   capture_output=True, timeout=120)
    page.unlink(missing_ok=True); shutil.rmtree(prof, ignore_errors=True)


def d(p): return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in p) + " Z"
def shape(s):
    f = s.get("fill", "#000"); extra = f' opacity="{s["opacity"]}"' if "opacity" in s else ""
    st = f' stroke="{s["stroke"]}" stroke-width="{s.get("sw", 3)}"' if "stroke" in s else ""
    if "rect" in s:
        x, y, w, h = s["rect"]; r = s.get("r", 0)
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}"{st}{extra}/>'
    if "circle" in s:
        x, y, r = s["circle"]; return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}"{st}{extra}/>'
    if "path" in s: return f'<path d="{s["path"]}" fill="{f}"{st}{extra}/>'
    return f'<path d="{d(s["poly"])}" fill="{f}"{st}{extra}/>'
def text(t):
    fam = t.get("font", "Arial Black, Arial, Helvetica, sans-serif")
    tr = f' transform="rotate({t["rot"]} {t["x"]} {t["y"]})"' if t.get("rot") else ""
    if t.get("skew"): tr = f' transform="translate({t["x"]} {t["y"]}) skewX({t["skew"]}) translate({-t["x"]} {-t["y"]})"'
    st = f' stroke="{t["stroke"]}" stroke-width="{t.get("sw", 3)}" paint-order="stroke"' if t.get("stroke") else ""
    ls = f' textLength="{t["w"]}" lengthAdjust="spacingAndGlyphs"' if t.get("w") else ""
    return (f'<text x="{t["x"]}" y="{t["y"]}" font-family="{fam}" font-size="{t["size"]}" font-weight="{t.get("weight", "bold")}" '
            f'font-style="{"italic" if t.get("italic") else "normal"}" fill="{t.get("fill", "#000")}" text-anchor="{t.get("anchor", "middle")}"{ls}{st}{tr}>{html.escape(t["t"])}</text>')
def wheel(w, rim_col, style, liv=None):
    cx, cy = w["c"]; r, rr = w["tyre"], w["rim"]
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#1a1a1a" stroke="#000" stroke-width="3"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{rim_col}" stroke="#000" stroke-width="3"/>']
    if style == "cross":   # BBS-style mesh: rim-coloured cross spokes over dark openings, outer ring, lip
        lv = liv or {}
        o[-1] = f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{lv.get("window", "#2e2e2e")}" stroke="#000" stroke-width="3"/>'
        n = int(lv.get("spokes", 10)); rin = rr * 0.84
        for k in range(n):
            for sgn in (1, -1):
                a1 = 2 * math.pi * k / n; a2 = a1 + sgn * 2 * math.pi * 0.28
                o.append(f'<line x1="{cx+rin*math.cos(a1):.1f}" y1="{cy+rin*math.sin(a1):.1f}" x2="{cx+rr*0.3*math.cos(a2):.1f}" y2="{cy+rr*0.3*math.sin(a2):.1f}" '
                         f'stroke="{rim_col}" stroke-width="{rr*0.075:.1f}" stroke-linecap="round"/>')
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr*0.92}" fill="none" stroke="{rim_col}" stroke-width="{rr*0.16:.1f}"/>')
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr*0.36}" fill="{rim_col}" stroke="#000" stroke-width="2"/>')
        if lv.get("lip"):
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr*0.97}" fill="none" stroke="{lv["lip"]}" stroke-width="{rr*0.06:.1f}"/>')
    elif style == "star":  # N spokes; windows taper towards the hub ("taper" 0..1), optionally swept ("twist", degrees)
        liv = liv or {}; n = int(liv.get("spokes", 5)); gap = float(liv.get("gap", 0.4))
        ri, ro = rr * float(liv.get("hub", 0.3)), rr * float(liv.get("outer", 0.86))
        taper = float(liv.get("taper", 0.0)); tw = math.radians(float(liv.get("twist", 0)))
        win = liv.get("window", "#2a2a2a")
        P = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
        if liv.get("spoke_w"):                   # parallel-sided spokes of this width (share of the rim radius)
            sw = float(liv["spoke_w"]) * rr
            for k in range(n):
                ac = 2 * math.pi * (k + 0.5) / n - math.pi / 2; L, Rr = [], []
                for t in [i / 12 for i in range(13)]:
                    r = ri + (ro - ri) * t; half = math.pi / n - math.asin(min(1.0, sw / (2 * r)))
                    if half <= 0.01:
                        continue
                    L.append(P(r, ac - half + tw * t)); Rr.append(P(r, ac + half + tw * t))
                if len(L) < 2:
                    continue
                pts = L + Rr[::-1]
                o.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f' Z" fill="{win}" stroke="#000" '
                         f'stroke-width="{max(2, rr * 0.03):.1f}" stroke-linejoin="round"/>')
            n = 0                                # skip the wedge windows below
        for k in range(n):
            ac = 2 * math.pi * (k + 0.5) / n - math.pi / 2; wo = math.pi * gap / n; wi = wo * (1 - taper)
            pts = [P(ri, ac - wi), P((ri + ro) / 2, ac - (wi + wo) / 2 + tw / 2), P(ro, ac - wo + tw)]
            end = P(ro, ac + wo + tw); back = [P((ri + ro) / 2, ac + (wi + wo) / 2 + tw / 2), P(ri, ac + wi)]
            d = (f"M{pts[0][0]:.1f},{pts[0][1]:.1f} Q{pts[1][0]:.1f},{pts[1][1]:.1f} {pts[2][0]:.1f},{pts[2][1]:.1f} "
                 f"A{ro:.1f},{ro:.1f} 0 0 1 {end[0]:.1f},{end[1]:.1f} Q{back[0][0]:.1f},{back[0][1]:.1f} {back[1][0]:.1f},{back[1][1]:.1f} "
                 f"A{ri:.1f},{ri:.1f} 0 0 0 {pts[0][0]:.1f},{pts[0][1]:.1f} Z")
            o.append(f'<path d="{d}" fill="{win}" stroke="#000" stroke-width="2" stroke-linejoin="round"/>')
        if liv.get("lip"):
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr*0.93}" fill="none" stroke="{liv["lip"]}" stroke-width="{rr*0.1:.1f}"/>')
    elif style == "dish":  # flat dish with five round holes
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr*0.8}" fill="none" stroke="#000" stroke-width="2" opacity="0.35"/>')
        for k in range(5):
            a = 2 * math.pi * k / 5 - math.pi / 2
            o.append(f'<circle cx="{cx+rr*0.55*math.cos(a):.1f}" cy="{cy+rr*0.55*math.sin(a):.1f}" r="{rr*0.17:.1f}" fill="#555" stroke="#000" stroke-width="2"/>')
    else:                  # multi-spoke
        for k in range(10):
            a = 2 * math.pi * k / 10
            o.append(f'<line x1="{cx+rr*0.28*math.cos(a):.1f}" y1="{cy+rr*0.28*math.sin(a):.1f}" x2="{cx+rr*0.88*math.cos(a):.1f}" y2="{cy+rr*0.88*math.sin(a):.1f}" stroke="#000" stroke-width="5" opacity="0.55"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr*0.26}" fill="#8a8a8a" stroke="#000" stroke-width="2.5"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr*0.09}" fill="#333"/>')
    return "\n".join(o)
def build(model, liv):
    W, H = model["size"]; x0, y0, bw, bh = model["bbox"]; pad = 12
    vb = f"{x0-pad} {y0-pad} {bw+2*pad} {bh+2*pad}"
    if liv.get("_full"): vb = f"0 0 {W} {H}"; bw, bh, pad = W, H, 0
    body = d(model["body"])
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{bw+2*pad}" height="{bh+2*pad}">',
         f'<title>{html.escape(liv.get("title", ""))}</title>',
         f'<defs><clipPath id="body"><path d="{body}"/></clipPath></defs>',
         f'<path d="{body}" fill="{liv.get("base", "#ffffff")}"/>',
         '<g clip-path="url(#body)">']
    o += [shape(s) for s in liv.get("shapes", [])]
    o += [text(t) for t in liv.get("texts", [])]
    if "number" in liv:
        n = liv["number"]; x, y, w, h = n["rect"]
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{n.get("r", 10)}" fill="{n.get("bg", "#fff")}" stroke="{n.get("border", "#000")}" stroke-width="3"/>')
        o.append(text({"t": n["n"], "x": x + w / 2, "y": y + h * 0.82, "size": h * 0.9, "fill": n.get("fg", "#000"), "font": n.get("font", "Arial Narrow, Arial, sans-serif"), "w": w * 0.8 if len(n["n"]) > 1 else None}))
    o.append('</g>')
    gl = liv.get("glass", "#3a3a3a")
    o += [f'<path d="{d(g)}" fill="{gl}" stroke="#000" stroke-width="2"/>' for g in model["glass"]]
    o.append('<g clip-path="url(#body)">' + "".join(shape(s) for s in liv.get("over_glass", [])) + "".join(text(t) for t in liv.get("over_texts", [])) + '</g>')
    if model.get("arch"):                         # photo outlines: dark wheel arch opening behind the tyre
        o.append('<g clip-path="url(#body)">' + "".join(f'<circle cx="{w["c"][0]}" cy="{w["c"][1]}" r="{w["tyre"] * model["arch"]:.1f}" fill="#111"/>' for w in model["wheels"]) + '</g>')
    o.append('<path fill="#000" fill-rule="evenodd" d="' + " ".join(d(p) for p in model["dark"] if len(p) >= 3) + '"/>')
    o += [f'<path d="{d(l["poly"])}" fill="{l["color"]}" stroke="#000" stroke-width="2"/>' for l in model.get("lights", [])]
    o += [wheel(w, liv.get("rim", "#c8c8c8"), liv.get("wheel", "spoke"), liv) for w in model["wheels"]]
    o.append(f'<path d="{body}" fill="none" stroke="#000" stroke-width="4" stroke-linejoin="round"/>')
    o.append('</svg>')
    return "\n".join(o)


def find_wheels(img, ratio=None):
    """Wheel centre x of the front and rear wheel and the roof top y in a nose-left side view on a plain
    background (TV graphic drawings, side photos): the car is what differs from the border colour, the
    tyres are the two biggest dark blobs in its lower part. Returns (front_x, rear_x, roof_y) or None."""
    import cv2, numpy as np
    h, w = img.shape[:2]; im = img.astype(np.int16)
    border = np.concatenate([im[0], im[-1], im[:, 0], im[:, -1]]); bg = np.median(border, axis=0)
    car = (np.abs(im - bg).sum(2) > 60).astype(np.uint8)
    car = cv2.morphologyEx(car, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    rows = np.where(car.mean(1) > 0.15)[0]
    if not len(rows):
        return None
    roof = int(rows[0])
    lum = im.mean(2); dark = ((lum < np.percentile(lum, 18)) & (np.arange(h)[:, None] > roof + 0.45 * (h - roof))).astype(np.uint8)
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(dark)
    blobs = sorted(((st[k, 4], cen[k][0]) for k in range(1, n) if st[k, 2] > 0.05 * w), reverse=True)[:8]
    cols = np.where(car.mean(0) > 0.1)[0]; length = cols[-1] - cols[0] if len(cols) else w
    want = (ratio or 0.62) * length               # wheelbase expected from our model's wheelbase/length
    pairs = [(abs(abs(xa - xb) - want) / want + 0.3 * abs(aa - ab) / max(aa, ab), min(xa, xb), max(xa, xb))
             for i, (aa, xa) in enumerate(blobs) for ab, xb in blobs[i + 1:]]
    pairs = [p for p in pairs if p[0] < 0.35]
    return (min(pairs)[1], min(pairs)[2], roof) if pairs else None


def compare(svg_png, model, ref, out, refwheels=None):
    """Size check: the reference (nose left) scaled to our wheelbase, wheel centres aligned, above our
    drawing, with guide lines at the wheel centres and every 100 model px."""
    import cv2, numpy as np
    ours = cv2.imread(str(svg_png)); r = cv2.imdecode(np.fromfile(str(ref), np.uint8), cv2.IMREAD_COLOR)
    wb = model["wheels"][1]["c"][0] - model["wheels"][0]["c"][0]
    wr = tuple(map(float, refwheels.split(","))) if refwheels else find_wheels(r, wb / model["bbox"][2])
    if wr is None:
        return False
    x0, y0, bw, bh = model["bbox"]; pad = 12; k_ours = ours.shape[1] / (bw + 2 * pad)
    f, b = model["wheels"][0]["c"], model["wheels"][1]["c"]
    fx, bx = (f[0] - x0 + pad) * k_ours, (b[0] - x0 + pad) * k_ours
    roof_ours = pad * k_ours                     # body top sits at the top of the viewBox (plus padding)
    k = (bx - fx) / (wr[1] - wr[0]); r2 = cv2.resize(r, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC)
    dx, dy = int(round(fx - wr[0] * k)), int(round(roof_ours - wr[2] * k))
    top = np.full_like(ours, 255)
    sx0, sy0 = max(0, -dx), max(0, -dy); tx0, ty0 = max(0, dx), max(0, dy)
    hh = min(r2.shape[0] - sy0, top.shape[0] - ty0); ww = min(r2.shape[1] - sx0, top.shape[1] - tx0)
    top[ty0:ty0 + hh, tx0:tx0 + ww] = r2[sy0:sy0 + hh, sx0:sx0 + ww]
    both = np.vstack([top, np.full((8, ours.shape[1], 3), 255, np.uint8), ours])
    for xm in range(0, 2400, 100):
        X = int((xm - x0 + pad) * k_ours)
        if 0 <= X < both.shape[1]:
            cv2.line(both, (X, 0), (X, both.shape[0]), (230, 200, 160), 1)
    for X in (int(fx), int(bx)):
        cv2.line(both, (X, 0), (X, both.shape[0]), (0, 0, 255), 2)
    cv2.imwrite(str(out), both); return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--season", required=True); ap.add_argument("--car", action="append", default=[])
    ap.add_argument("--no-render", action="store_true"); ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--compare", action="store_true", help="also write <car>_compare.png: best TV drawing scaled to our wheelbase above our drawing")
    ap.add_argument("--ref", help="with --compare: use this nose-left picture instead of the best TV drawing")
    ap.add_argument("--refwheels", help="with --compare: front wheel x, rear wheel x, roof top y in the reference's pixels "
                                        "(the automatic match is unreliable on blurry pictures: check the red lines)")
    a = ap.parse_args()
    root = REPO / "seasons" / a.season / "art" / "svg"
    for lp in sorted((root / "liveries").glob("*.json")):
        num = lp.stem.split("_")[0].lstrip("0")
        if a.car and not any(c.lstrip("0") in (num, lp.stem.lstrip("0")) for c in a.car):
            continue
        liv = json.load(open(lp, encoding="utf-8"))
        model = json.load(open(root / "models" / f"{liv['model']}.json", encoding="utf-8"))
        out = root / f"{lp.stem}.svg"
        out.write_text(build(model, liv), encoding="utf-8")
        if not a.no_render:
            png = REPO / "build" / "art" / a.season / "svg" / f"{lp.stem}.png"
            render_png(out, png, a.width)
            if a.compare:
                pics = pathlib.Path.home() / "Pictures" / "mods" / a.season / "tv_artwork" / "cars"
                tv = sorted(pics.glob(f"{int(lp.stem.split('_')[0]):02d} */[AB]_*cap*.png")) + sorted(pics.glob(f"{int(lp.stem.split('_')[0]):02d} */A_*.png"))
                ref = pathlib.Path(a.ref) if a.ref else (tv[0] if tv else None)
                if ref and compare(png, model, ref, png.with_name(f"{lp.stem}_compare.png"), a.refwheels):
                    print("  compare:", ref.name)
                else:
                    print("  compare: no reference / wheels not found")
        print(out)


if __name__ == "__main__":
    main()
