"""Draw the team car images (2048x1024 side views) from reference drawings.

Each car model has a side-view reference drawing (a PNG render of an SVG
illustration from Wikimedia Commons, see the model's "reference"). Its
pixels are classified by colour:

* thin dark lines (panel lines, outlines), glass, rims and lights are kept;
* thick dark areas on the body side are old livery and are repainted;
* every other body pixel is repainted with the team's base colour.

A team livery then comes from an Automobilista 2 livery texture: the
texture's side panel is mesh-warped onto the body band (window line to
sill), piecewise between anchors measured once per model (tail, rear axle,
front door edge, front axle). Outlines go back on top so the car keeps its
panel lines. Teams without an AMS2 livery get the base colour plus
lettering, or keep the reference's own livery ("keep_reference_livery").

Seasons without AMS2 textures use layered liveries instead ("cars" in
cars.json): a hand-traced outline (model reference "layered_trace") is
filled with the base colour, then colour zones, bands, text decals and the
number board are drawn on the body side, and glass, panel lines, wing and
wheels go on top. Layer coordinates are in the trace's own frame. Every car
is rendered to build/art/<season>/; the first car of each team becomes the
team image (the game shows one car per team).

Licensing: the reference drawings are CC BY-SA (see the model's credit), so
the generated car images are CC BY-SA 4.0. The AMS2 livery artwork is used
with its author's permission. See LICENSE-CONTENT.md.

Config: <season>/art/cars.json. local.json provides "ams2_mod_zip".
Downloads and decoded textures are cached under build/art/.

Usage:
    python tools/car_art.py seasons/dtm-1991 [--only "Team"] [--preview]
"""

import argparse
import io
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "build" / "art"
CANVAS = (2048, 1024)
CAR_SPAN_PX = 1840
GROUND_Y = 720
USER_AGENT = "team-principal-mods/0.1 (car art; reference drawings from Wikimedia Commons)"
GLASS_RGB = (51, 51, 51)


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ------------------------------------------------------------ sources

def commons_png(title, width=3840):
    """Download (cached) a PNG render of a Wikimedia Commons file."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / ("ref_" + title.replace("File:", "").replace(" ", "_").rsplit(".", 1)[0] + ".png")
    if path.exists():
        return Image.open(path).convert("RGBA")
    api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url",
         "iiurlwidth": width, "format": "json"})
    info = json.loads(fetch(api))
    url = next(iter(info["query"]["pages"].values()))["imageinfo"][0]["thumburl"]
    path.write_bytes(fetch(url))
    return Image.open(path).convert("RGBA")


def fetch(url):
    for attempt in range(8):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            return urllib.request.urlopen(req, timeout=90).read()
        except urllib.error.HTTPError as err:
            if err.code != 429:
                raise
            time.sleep(15 * (attempt + 1))
    raise SystemExit(f"rate limited: {url}")


def ams2_texture(zip_path, member):
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / (Path(member).stem + ".png")
    if cached.exists():
        return Image.open(cached).convert("RGBA")
    with zipfile.ZipFile(zip_path) as zf:
        im = Image.open(io.BytesIO(zf.read(member)))
        im.load()
    im = im.convert("RGBA")
    im.save(cached)
    return im


# ------------------------------------------------------- classification

def classify(ref, model):
    """Masks (mode L) for outline, glass, kept pixels (rims, lights) and paint."""
    w, h = ref.size
    px = ref.load()
    dark = Image.new("L", ref.size, 0)
    glass = Image.new("L", ref.size, 0)
    d, g = dark.load(), glass.load()
    belt = model["belt_y"]
    lz0, lz1 = model["livery_zone"]
    for y in range(h):
        for x in range(w):
            r, gg, b, a = px[x, y]
            if a < 40:
                continue
            lum = 0.3 * r + 0.59 * gg + 0.11 * b
            spread = max(r, gg, b) - min(r, gg, b)
            if lum < 30 and spread < 30:
                d[x, y] = 255
            elif y < belt and spread < 14 and 35 < lum < 75:
                g[x, y] = 255

    # Lamps are explicit boxes: anything colourful elsewhere is old livery.
    ref_lights = Image.new("L", ref.size, 0)
    for x0, y0, x1, y1 in model.get("light_boxes", []):
        ImageDraw.Draw(ref_lights).rectangle([x0, y0, x1, y1], fill=255)
    colourful = Image.new("L", ref.size, 0)
    cpx = colourful.load()
    for x0, y0, x1, y1 in model.get("light_boxes", []):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                r, gg, b, a = px[x, y]
                if a > 40 and 0.3 * r + 0.59 * gg + 0.11 * b > 120 and (max(r, gg, b) - min(r, gg, b) > 40 or min(r, gg, b) > 200):
                    cpx[x, y] = 255
    lights = ImageChops.multiply(ImageChops.subtract(ref_lights, dark), colourful)
    gd = ImageDraw.Draw(glass)
    for poly in model.get("glass_polygons", []):
        gd.polygon([tuple(p) for p in poly], fill=255)

    rim_circles = Image.new("L", ref.size, 0)
    tyre_circles = Image.new("L", ref.size, 0)
    for cx, cy, tyre_r, rim_r in model["wheels"]:
        ImageDraw.Draw(rim_circles).ellipse([cx - rim_r, cy - rim_r, cx + rim_r, cy + rim_r], fill=255)
        # Include the wheel-arch liner around the tyre: it is dark bodywork, not livery.
        arch_r = tyre_r * model.get("arch_factor", 1.22)
        ImageDraw.Draw(tyre_circles).ellipse([cx - arch_r, cy - arch_r, cx + arch_r, cy + arch_r], fill=255)
    # Everything inside the rim circle is wheel (any rim colour, e.g. gold BBS).
    rims = ImageChops.multiply(rim_circles, ref.split()[3].point(lambda v: 255 if v >= 40 else 0))

    # Thick dark areas on the body side are livery (number boards, black
    # lettering), not panel lines: find them by morphological opening.
    k = model.get("thick_px", 15)
    thick = dark.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))
    zone = Image.new("L", ref.size, 0)
    ImageDraw.Draw(zone).rectangle([lz0, belt + 8, lz1, model["sill_y"]], fill=255)
    zone = ImageChops.subtract(zone, tyre_circles)
    livery_dark = ImageChops.multiply(thick, zone)
    erase = Image.new("L", ref.size, 0)
    for x0, y0, x1, y1 in model.get("erase_outline", []):
        ImageDraw.Draw(erase).rectangle([x0, y0, x1, y1], fill=255)
    livery_dark = ImageChops.lighter(livery_dark, ImageChops.multiply(erase, dark))
    outline = ImageChops.subtract(ImageChops.subtract(dark, livery_dark), glass)

    alpha = ref.split()[3].point(lambda v: 255 if v >= 40 else 0)
    keep = ImageChops.lighter(ImageChops.lighter(glass, lights), rims)
    paint = ImageChops.subtract(ImageChops.subtract(alpha, keep), outline)
    return outline, glass, keep, paint


# --------------------------------------------------------------- livery

def interp(anchors, x, idx):
    for a1, a2 in zip(anchors, anchors[1:]):
        if a1[0] <= x <= a2[0]:
            f = (x - a1[0]) / (a2[0] - a1[0])
            return a1[idx] + (a2[idx] - a1[idx]) * f
    return anchors[0][idx] if x < anchors[0][0] else anchors[-1][idx]


def warp_panel(tex, model, size):
    """Mesh-warp the texture side panel onto the body band.

    uv.anchors: [ref_x, texture_y, texture_x_at_window_line, texture_x_at_sill]
    """
    anchors = sorted(model["uv"]["anchors"])
    top, bot = model["belt_y"], model["sill_y"]
    mesh = []
    steps = 120
    x0, x1 = anchors[0][0], anchors[-1][0]
    for i in range(steps):
        xa = x0 + (x1 - x0) * i / steps
        xb = x0 + (x1 - x0) * (i + 1) / steps
        ta, tb = interp(anchors, xa, 1), interp(anchors, xb, 1)
        ua_t, ua_b = interp(anchors, xa, 2), interp(anchors, xa, 3)
        ub_t, ub_b = interp(anchors, xb, 2), interp(anchors, xb, 3)
        mesh.append(((int(xa), top, int(math.ceil(xb)), bot),
                     (ua_t, ta, ua_b, ta, ub_b, tb, ub_t, tb)))
    return tex.transform(size, Image.MESH, mesh, resample=Image.BICUBIC)


def font(size):
    for name in ("arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def traced_reference(trace_path):
    """Render a hand-traced side view (outline data) in the reference drawing style."""
    t = load_json(trace_path)
    fr = t["frame"]
    k = fr["scale"]
    P = lambda pt: ((pt[0] - fr["x0"]) * k, (pt[1] - fr["y0"]) * k)
    xs = [p[0] for p in t["body"]] + [w["c"][0] + w["tyre"] for w in t["wheels"]]
    ys = [p[1] for p in t["body"]] + [w["c"][1] + w["tyre"] for w in t["wheels"]]
    size = (int((max(xs) - fr["x0"]) * k) + 20, int((max(ys) - fr["y0"]) * k) + 20)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lw = t.get("line_px", 9)
    black = (12, 12, 12, 255)
    body = tuple(t["body_color"]) + (255,)
    d.polygon([P(p) for p in t["body"]], fill=body, outline=black, width=lw)
    d.polygon([P(p) for p in t["spoiler"]], fill=body, outline=black, width=lw)
    # Wheel arches cut into the body, with a flared lip outline (DTM arch flares).
    for w in t["wheels"]:
        cx, cy = P(w["c"])
        r = w["tyre"] * k * 1.16
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(22, 22, 22, 255))
        d.arc([cx - r - lw, cy - r - lw, cx + r + lw, cy + r + lw], 182, 358, fill=black, width=lw)
        d.arc([cx - r - 5 * lw, cy - r - 5 * lw, cx + r + 5 * lw, cy + r + 5 * lw], 190, 350, fill=black, width=lw // 2)
    for poly in t["glass"]:
        d.polygon([P(p) for p in poly], fill=GLASS_RGB + (255,), outline=black, width=lw)
    for poly in t.get("pillars", []):
        d.polygon([P(p) for p in poly], fill=black)
    for line in t["lines"]:
        d.line([P(p) for p in line], fill=black, width=max(3, lw // 2), joint="curve")
    d.polygon([P(p) for p in t["mirror"]], fill=body, outline=black, width=lw)
    for light in t["lights"]:
        d.polygon([P(p) for p in light["poly"]], fill=tuple(light["color"]) + (255,), outline=black, width=lw // 2)
    rim = tuple(t["rim_color"]) + (255,)
    for w in t["wheels"]:
        cx, cy = P(w["c"])
        R, r = w["tyre"] * k, w["rim"] * k
        d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(18, 18, 18, 255))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rim, outline=black, width=lw // 2)
        # BBS cross-spoke mesh.
        for i in range(10):
            a = 2 * math.pi * i / 10
            for off in (0.35, -0.35):
                x1, y1 = cx + math.cos(a) * r * 0.25, cy + math.sin(a) * r * 0.25
                x2, y2 = cx + math.cos(a + off) * r * 0.92, cy + math.sin(a + off) * r * 0.92
                d.line([(x1, y1), (x2, y2)], fill=(120, 95, 35, 255), width=lw // 2)
        d.ellipse([cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2], fill=(60, 50, 25, 255))
    return img, t


FONTS = {"bold": "arialbd.ttf", "black": "ariblk.ttf", "italic": "arialbi.ttf", "impact": "impact.ttf",
         "script": "segoescb.ttf", "serif": "georgiab.ttf", "condensed": "bahnschrift.ttf"}


def named_font(name, size):
    try:
        return ImageFont.truetype(FONTS.get(name, name), max(8, int(size)))
    except OSError:
        return font(int(size))


def chaikin(poly, passes=2):
    """Round a closed polygon's corners (Chaikin corner cutting) so traced outlines read as curves."""
    for _ in range(passes):
        out = []
        for a, b in zip(poly, poly[1:] + poly[:1]):
            out += [[0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]], [0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]]]
        poly = out
    return poly


def layered_car(trace_path, livery):
    """Draw a car from a traced outline with a layered livery (see module docstring).

    Trace keys: frame.scale, body, spoiler, glass, pillars, lines, mirror,
    lights, wheels [{c, tyre, rim}] (rear first). The photo's perspective is
    levelled by shearing so both wheel centres sit on one line.
    Livery keys: base_color, layers, number, mirror_color, wing_color,
    rim_color, spoke_color.
    Layers: {"poly": [[x, y], ...], "color"}; {"band": [y0, y1], "x": [x0, x1],
    "color"} (a stripe following the body); {"text", "at", "size", "color",
    "font", "rotate", "stroke", "stroke_color", "box": [w, h] (fit inside)}.
    """
    t = load_json(trace_path)
    passes = t.get("smooth", 2)
    t["body"], t["spoiler"] = chaikin(t["body"], passes), chaikin(t["spoiler"], passes)
    t["glass"] = [chaikin(g, passes) for g in t["glass"]]
    k = t["frame"]["scale"]
    rear, front = t["wheels"]
    (xr, yr), (xf, yf) = rear["c"], front["c"]
    slope = (yf - yr) / (xf - xr)
    margin = 30
    pts = t["body"] + t["spoiler"]
    xs = [p[0] for p in pts]
    min_x, max_x = min(xs) - 10, max(xs) + 10
    lvl = lambda p: (p[0], p[1] - slope * (p[0] - xr))
    lys = [lvl(p)[1] for p in pts] + [yr + w["tyre"] for w in t["wheels"]]
    min_y, max_y = min(lys) - 10, max(lys) + 10
    P = lambda p: ((lvl(p)[0] - min_x) * k + margin, (lvl(p)[1] - min_y) * k + margin)
    size = (int((max_x - min_x) * k) + 2 * margin, int((max_y - min_y) * k) + 2 * margin)
    lw = max(3, int(t.get("line_px", 3) * k))
    black = (14, 14, 16, 255)
    rgba = lambda c: tuple(c) + (255,) if len(c) == 3 else tuple(c)
    tyre_r = (rear["tyre"] + front["tyre"]) / 2
    rim_r = (rear["rim"] + front["rim"]) / 2
    wheels = [P((w["c"][0], yr + slope * (w["c"][0] - xr))) for w in t["wheels"]]

    # Body side paint: base colour, then the livery layers, clipped to the body.
    paint = Image.new("RGBA", size, rgba(livery.get("base_color", [245, 245, 245])))
    d = ImageDraw.Draw(paint)
    for layer in livery.get("layers", []):
        if "poly" in layer:
            d.polygon([P(p) for p in layer["poly"]], fill=rgba(layer["color"]))
        elif "band" in layer:
            (y0, y1), (x0, x1) = layer["band"], layer.get("x", [min_x, max_x])
            d.polygon([P((x0, y0)), P((x1, y0)), P((x1, y1)), P((x0, y1))], fill=rgba(layer["color"]))
        elif "text" in layer:
            paste_text(paint, layer, P, k)
    if livery.get("number") is not None:
        number_board(paint, livery, P, k)
    body = Image.new("L", size, 0)
    ImageDraw.Draw(body).polygon([P(p) for p in t["body"]], fill=255)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(paint, (0, 0), body)

    d = ImageDraw.Draw(out)
    d.polygon([P(p) for p in t["body"]], outline=black, width=lw)
    for cx, cy in wheels:
        r = tyre_r * k * 1.1
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(20, 20, 22, 255))
        d.arc([cx - r - lw, cy - r - lw, cx + r + lw, cy + r + lw], 180, 360, fill=black, width=lw)
    for poly in t["glass"]:
        d.polygon([P(p) for p in poly], fill=GLASS_RGB + (255,), outline=black, width=lw)
    for poly in t.get("pillars", []):
        d.polygon([P(p) for p in poly], fill=black)
    for line in t.get("lines", []):
        d.line([P(p) for p in line], fill=black, width=max(2, lw // 2), joint="curve")
    d.polygon([P(p) for p in t["mirror"]], fill=rgba(livery.get("mirror_color", livery.get("base_color", [245, 245, 245]))),
              outline=black, width=lw)
    for light in t.get("lights", []):
        d.polygon([P(p) for p in light["poly"]], fill=rgba(light["color"]), outline=black, width=max(2, lw // 2))
    d.polygon([P(p) for p in t["spoiler"]], fill=rgba(livery.get("wing_color", t.get("wing_color", [28, 28, 30]))),
              outline=black, width=lw)
    rim = rgba(livery.get("rim_color", t.get("rim_color", [40, 40, 44])))
    spoke = rgba(livery.get("spoke_color", t.get("spoke_color", [70, 70, 76])))
    for cx, cy in wheels:
        R, r = tyre_r * k, rim_r * k
        d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(16, 16, 18, 255))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rim, outline=(10, 10, 10, 255), width=max(2, lw // 2))
        n = t.get("spokes", 10)
        for i in range(n):
            a = 2 * math.pi * i / n
            d.line([(cx + math.cos(a) * r * 0.2, cy + math.sin(a) * r * 0.2),
                    (cx + math.cos(a) * r * 0.93, cy + math.sin(a) * r * 0.93)], fill=spoke, width=max(3, int(r * 0.09)))
        d.ellipse([cx - r * 0.18, cy - r * 0.18, cx + r * 0.18, cy + r * 0.18], fill=(30, 30, 30, 255))
        d.ellipse([cx - r * 0.06, cy - r * 0.06, cx + r * 0.06, cy + r * 0.06], fill=(200, 30, 30, 255))
    return out


def paste_text(img, layer, P, k):
    """Draw a text decal centred at layer["at"], optionally rotated and fitted into a box."""
    size = layer.get("size", 40) * k
    f = named_font(layer.get("font", "bold"), size)
    stroke = int(layer.get("stroke", 0) * k)
    probe = ImageDraw.Draw(img)
    if "box" in layer:
        bw, bh = layer["box"][0] * k, layer["box"][1] * k
        while size > 8:
            x0, y0, x1, y1 = probe.textbbox((0, 0), layer["text"], font=f, stroke_width=stroke)
            if x1 - x0 <= bw and y1 - y0 <= bh:
                break
            size *= 0.94
            f = named_font(layer.get("font", "bold"), size)
    x0, y0, x1, y1 = probe.textbbox((0, 0), layer["text"], font=f, stroke_width=stroke)
    tile = Image.new("RGBA", (x1 - x0 + 8, y1 - y0 + 8), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text((4 - x0, 4 - y0), layer["text"], font=f, fill=tuple(layer.get("color", [255, 255, 255])),
                              stroke_width=stroke, stroke_fill=tuple(layer.get("stroke_color", [0, 0, 0])))
    if layer.get("rotate"):
        tile = tile.rotate(layer["rotate"], expand=True, resample=Image.BICUBIC)
    cx, cy = P(layer["at"])
    img.alpha_composite(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2)))


def number_board(img, livery, P, k):
    """DTM-style number board: white panel, sponsor line on top, number, yellow strip below."""
    cx, cy = P(livery.get("number_at", [0, 0]))
    w, h = livery.get("number_size", [120, 115])
    w, h = w * k, h * k
    d = ImageDraw.Draw(img)
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=(255, 255, 255, 255), outline=(20, 20, 22, 255),
                width=max(2, int(k)))
    d.text((cx, cy - h * 0.33), "DEKRA", font=named_font("black", h * 0.2), anchor="mm", fill=(0, 125, 80, 255))
    d.text((cx, cy + h * 0.03), str(livery["number"]), font=named_font("black", h * 0.42), anchor="mm",
           fill=(20, 20, 22, 255))
    d.rectangle([cx - w / 2, cy + h * 0.27, cx + w / 2, cy + h / 2], fill=(255, 205, 0, 255))
    d.text((cx, cy + h * 0.385), "ADAC", font=named_font("black", h * 0.17), anchor="mm", fill=(20, 20, 22, 255))


def fit_canvas(out):
    """Fit a car image onto the game canvas: bumper to bumper CAR_SPAN_PX wide, tyres on GROUND_Y."""
    car = out.crop(out.getbbox())
    scale = CAR_SPAN_PX / car.size[0]
    car = car.resize((CAR_SPAN_PX, round(car.size[1] * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    canvas.paste(car, ((CANVAS[0] - CAR_SPAN_PX) // 2, GROUND_Y - car.size[1]), car)
    return canvas


def render_car(model, livery, zip_path, season=None):
    if "layered_trace" in model["reference"]:
        # Model defaults (number board position and size) apply unless the car overrides them.
        return fit_canvas(layered_car(season / model["reference"]["layered_trace"], {**model.get("defaults", {}), **livery}))
    if "trace" in model["reference"]:
        ref, _ = traced_reference(season / model["reference"]["trace"])
    else:
        ref = commons_png(model["reference"]["file"])
    if livery.get("keep_reference_livery"):
        out = ref.copy()
    else:
        outline, glass, keep, paint = classify(ref, model)
        out = Image.new("RGBA", ref.size, (0, 0, 0, 0))
        out.paste(ref, (0, 0), keep)
        out.paste(Image.new("RGBA", ref.size, GLASS_RGB + (255,)), (0, 0), glass)
        out.paste(Image.new("RGBA", ref.size, tuple(livery.get("base_color", [245, 245, 245])) + (255,)), (0, 0), paint)
        band = Image.new("L", ref.size, 0)
        ImageDraw.Draw(band).rectangle([0, model["belt_y"], ref.size[0], model["sill_y"]], fill=255)
        if livery.get("texture"):
            panel = warp_panel(ams2_texture(zip_path, livery["texture"]), model, ref.size)
            # Pure white in an AMS2 texture is empty UV space (e.g. wheel-arch cut-outs),
            # not paint: let the base colour show through there.
            r, g, b, a = panel.split()
            empty = ImageChops.darker(ImageChops.darker(r, g), b).point(lambda v: 255 if v >= 250 else 0)
            alpha = ImageChops.subtract(a, empty) if livery.get("white_is_empty", True) else a
            for x0, y0, x1, y1 in model.get("panel_clip", []):
                ImageDraw.Draw(alpha).rectangle([x0, y0, x1, y1], fill=0)
            mask = ImageChops.multiply(ImageChops.multiply(paint, band), alpha)
            out.paste(panel, (0, 0), mask)
        else:
            draw = ImageDraw.Draw(out)
            for stripe in livery.get("stripes", []):
                layer = Image.new("RGBA", ref.size, tuple(stripe["color"]) + (255,))
                m = Image.new("L", ref.size, 0)
                ImageDraw.Draw(m).rectangle([0, stripe["y0"], ref.size[0], stripe["y1"]], fill=255)
                out.paste(layer, (0, 0), ImageChops.multiply(m, paint))
            if livery.get("lettering"):
                # Rear half of the body side, shrunk to fit beside the number board.
                lz0, lz1 = model["livery_zone"]
                rear = model["wheels"][0]
                left = rear[0] + rear[2] * 1.25
                box_w = (model["number_at"][0] - 200) - left
                size = livery.get("lettering_size", 150)
                f = font(size)
                while draw.textlength(livery["lettering"], font=f) > box_w and size > 50:
                    size -= 6
                    f = font(size)
                x, y = livery.get("lettering_at", [left + box_w / 2,
                                                   (model["belt_y"] + model["sill_y"]) // 2])
                draw.text((x, y), livery["lettering"], font=f, anchor="mm",
                          fill=tuple(livery.get("lettering_color", [20, 20, 22])) + (255,))
            if livery.get("number"):
                bx, by = model["number_at"]
                s = 300
                draw.rounded_rectangle([bx - s / 2, by - s * 0.6, bx + s / 2, by + s * 0.6], radius=24,
                                       fill=(255, 255, 255, 255), outline=(20, 20, 22, 255), width=12)
                draw.text((bx, by - s * 0.33), "DEKRA", font=font(70), anchor="mm", fill=(20, 20, 22, 255))
                draw.text((bx, by + s * 0.12), str(livery["number"]), font=font(190), anchor="mm",
                          fill=(20, 20, 22, 255))
        out.paste(ref, (0, 0), outline)
    return fit_canvas(out)


def drawing_teams(season):
    """Teams whose image comes from an artist's drawing (<season>/art/drawings.json)."""
    path = season / "art" / "drawings.json"
    if not path.exists():
        return set()
    teams = set()
    for sheet in load_json(path)["sheets"].values():
        teams.update([sheet["team"]] if "team" in sheet else sheet["teams"])
    return teams


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("season", type=Path)
    parser.add_argument("--only", help="render just this team")
    parser.add_argument("--preview", action="store_true", help="also write build/art/preview.png")
    args = parser.parse_args()
    season = args.season.resolve()
    cfg = load_json(season / "art" / "cars.json")
    local = load_json(REPO / "local.json") if (REPO / "local.json").exists() else {}
    zip_path = local.get("ams2_mod_zip")
    out_dir = season / "assets" / "Cars"
    out_dir.mkdir(parents=True, exist_ok=True)
    rendered = []
    if "cars" in cfg:
        # Layered liveries: every car, first car of each team as the team image.
        all_dir = CACHE / season.name
        all_dir.mkdir(parents=True, exist_ok=True)
        # Teams with an artist's drawing (car_drawings.py) keep it.
        done = drawing_teams(season)
        for team in sorted(done):
            print(f"kept the drawing for {team} (tools/car_drawings.py)")
        for car in cfg["cars"]:
            if args.only and car["team"] != args.only:
                continue
            img = render_car(cfg["models"][car["model"]], car, zip_path, season)
            img.save(all_dir / f"{car['number']:02d}.png", optimize=True)
            rendered.append((f"#{car['number']} {car.get('driver', '')} - {car['team']}", img))
            if car["team"] not in done:
                done.add(car["team"])
                path = out_dir / f"{car['team'].replace(' ', '')}.png"
                img.save(path, optimize=True)
                print(f"wrote {path.relative_to(REPO)}")
    for team, livery in cfg.get("liveries", {}).items():
        if args.only and team != args.only:
            continue
        if livery.get("texture") and not zip_path:
            raise SystemExit("set ams2_mod_zip in local.json to render AMS2 liveries")
        img = render_car(cfg["models"][livery["model"]], livery, zip_path, season)
        path = out_dir / f"{team.replace(' ', '')}.png"
        img.save(path, optimize=True)
        rendered.append((team, img))
        print(f"wrote {path.relative_to(REPO)}")
    if args.preview and rendered:
        cols, w, h = 2, 1024, 512
        sheet = Image.new("RGB", (cols * w, math.ceil(len(rendered) / cols) * (h + 34)), (70, 70, 74))
        d = ImageDraw.Draw(sheet)
        for i, (team, img) in enumerate(rendered):
            x, y = (i % cols) * w, (i // cols) * (h + 34)
            small = img.resize((w, h), Image.LANCZOS)
            sheet.paste(small, (x, y + 34), small)
            d.text((x + 10, y + 8), team, fill=(255, 255, 255), font=font(22))
        CACHE.mkdir(parents=True, exist_ok=True)
        sheet.save(CACHE / "preview.png")
        print(f"preview: {(CACHE / 'preview.png').relative_to(REPO)}")


if __name__ == "__main__":
    main()
