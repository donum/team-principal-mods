"""Draw simple track layouts that show where the cars come back near the
finish line during a lap (the "Gegengerade" or back straight).

The game plays pass-bys at one point, the finish line. On some tracks a
listener there also hears the cars a second time, on a straight or a
corner close by. For each track this tool marks:

- the finish line (the listener, start of the `points` polyline);
- the part of the lap within RADIUS metres of it around the line (grey-red);
- every other part of the lap within RADIUS metres (blue): the second pass.

Usage:
    python tools/second_pass_maps.py [--radius 250] [--out DIR]

Writes one PNG per track and prints the lap progress of each second pass,
for wishlist item E22 and docs/requests/second-pass-sound.md.
"""

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
GAME = Path(r"X:\SteamLibrary\steamapps\common\Team Principal A Racing Manager")
OUT = REPO / "docs" / "requests" / "img" / "second-pass"

# (file name, label, track file, group). Vanilla first: the developer
# knows them. Group "yes" goes on all.png, "no" (no second pass) on
# counter.png.
F1 = GAME / "data/workshop_3821496627/tracks"  # workshop F1 pack
TRACKS = [
    ("monaco", "Monaco street circuit (vanilla: The Azure Promenade)", GAME / "data/default26/tracks/mon.json", "yes"),
    ("suzuka", "Suzuka (vanilla: Kitsune Ring)", GAME / "data/default26/tracks/jap.json", "yes"),
    ("abudhabi", "Abu Dhabi (vanilla: Dune Harbour)", GAME / "data/default26/tracks/abu.json", "yes"),
    ("sepang", "Sepang (workshop F1 pack)", F1 / "sepang.json", "yes"),
    ("sakhir", "Bahrain (workshop F1 pack)", F1 / "sakhir.json", "yes"),
    ("hungaroring", "Hungaroring (workshop F1 pack)", F1 / "hungaroring.json", "yes"),
    ("singapore", "Singapore (workshop F1 pack)", GAME / "data/workshop_3821665334/tracks/singapore.json", "yes"),
    ("adelaide", "Adelaide (workshop F1 1989)", GAME / "data/workshop_3821763947/tracks/ade89.json", "yes"),
    ("jarama", "Jarama (workshop F1 pack)", GAME / "data/workshop_3824621250/tracks/jarama.json", "yes"),
    ("donington", "Donington Park (BTCC 1991)", REPO / "seasons/btcc-1991/tracks/donington.json", "yes"),
    ("brandshatch", "Brands Hatch Indy (DTM 2013)", REPO / "seasons/dtm-2013/tracks/brandshatch.json", "yes"),
    ("brandshatch_gp", "Brands Hatch GP (DTM 2018)", GAME / "data/dtm2018/tracks/brandshatch_gp.json", "yes"),
    ("norisring", "Norisring (DTM 2013)", REPO / "seasons/dtm-2013/tracks/norisring.json", "yes"),
    ("hockenheim", "Hockenheim (DTM 2013)", REPO / "seasons/dtm-2013/tracks/hockenheim13.json", "yes"),
    ("oschersleben", "Oschersleben (DTM 2013)", REPO / "seasons/dtm-2013/tracks/oschersleben.json", "yes"),
    ("shanghai_pudong", "Shanghai Pudong street circuit (DTM 2010)", GAME / "data/dtm2010/tracks/shanghai.json", "yes"),
    ("valencia", "Valencia Ricardo Tormo (DTM 2010)", GAME / "data/dtm2010/tracks/valencia.json", "yes"),
    ("zandvoort", "Zandvoort (DTM 2013)", REPO / "seasons/dtm-2013/tracks/zandvoort.json", "yes"),
    ("melbourne", "Melbourne (vanilla: Banksia Park)", GAME / "data/default26/tracks/aus.json", "no"),
    ("redbullring", "Red Bull Ring (DTM 2013)", REPO / "seasons/dtm-2013/tracks/redbullring.json", "no"),
    ("lausitzring", "Lausitzring (DTM 2013)", REPO / "seasons/dtm-2013/tracks/lausitzring.json", "no"),
    ("monza", "Monza (workshop F1 pack)", F1 / "monza.json", "no"),
    ("imola", "Imola (workshop F1 pack)", F1 / "imola.json", "no"),
]

SIZE = 900
PAD = 70
BG = (250, 250, 248)
TRACK = (175, 175, 175)
NEAR = (215, 90, 70)
SECOND = (40, 110, 210)
INK = (40, 40, 40)


def resample(points, step):
    """Points every `step` units along the closed polyline, with distance."""
    pts = points + [points[0]]
    out, carry, total = [], 0.0, 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        t = carry
        while t < seg:
            f = t / seg
            out.append((x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, total + t))
            t += step
        carry = t - seg
        total += seg
    return out, total


def font(size):
    for name in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def draw(key, label, path, radius, out_dir):
    d = json.loads(path.read_text(encoding="utf-8"))
    pts = [tuple(p[:2]) for p in d["points"]]
    _, poly_len = resample(pts, 1.0)
    m_per_unit = d["length_km"] * 1000 / poly_len
    samples, _ = resample(pts, 2.0 / m_per_unit)  # one sample every 2 m
    lap_m = d["length_km"] * 1000
    lx, ly = pts[0]

    flags = []
    for x, y, s in samples:
        dist = math.hypot(x - lx, y - ly) * m_per_unit
        along = min(s, poly_len - s) * m_per_unit  # track distance to the line
        if dist > radius:
            flags.append(0)
        elif along <= radius * 1.6:
            flags.append(1)  # the main straight around the line
        else:
            flags.append(2)  # a second pass

    # Second-pass stretches as lap progress ranges.
    ranges, start = [], None
    for i, f in enumerate(flags + [0]):
        if f == 2 and start is None:
            start = i
        if f != 2 and start is not None:
            a = samples[start][2] / poly_len
            b = samples[i - 1][2] / poly_len
            close = min(math.hypot(samples[j][0] - lx, samples[j][1] - ly) for j in range(start, i))
            if (b - a) * lap_m >= 40:
                ranges.append((a, b, close * m_per_unit))
            start = None

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    scale = (SIZE - 2 * PAD) / span
    ox = (SIZE - (max(xs) - min(xs)) * scale) / 2 - min(xs) * scale
    oy = (SIZE - (max(ys) - min(ys)) * scale) / 2 - min(ys) * scale + 20

    def tr(x, y):
        return x * scale + ox, y * scale + oy

    img = Image.new("RGB", (SIZE, SIZE), BG)
    g = ImageDraw.Draw(img)
    r_px = radius / m_per_unit * scale
    cx, cy = tr(lx, ly)
    for a in range(0, 360, 6):  # dashed hearing circle
        g.arc([cx - r_px, cy - r_px, cx + r_px, cy + r_px], a, a + 3, fill=(150, 150, 150), width=2)
    g.line([tr(*p) for p in pts + [pts[0]]], fill=TRACK, width=9, joint="curve")
    colour = {1: NEAR, 2: SECOND}
    for (x0, y0, _), (x1, y1, _), f in zip(samples, samples[1:], flags):
        if f:
            g.line([tr(x0, y0), tr(x1, y1)], fill=colour[f], width=11)
    g.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=INK)
    g.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=BG)

    g.text((PAD - 30, 22), label, fill=INK, font=font(30))
    f20, x = font(20), PAD - 30
    for i, (c, text) in enumerate([
        (INK, "finish line: the game plays pass-bys here"),
        (NEAR, "the cars around the line"),
        (SECOND, f"second pass: the cars come back within {radius} m"),
    ]):
        y = SIZE - 96 + i * 28
        g.rectangle([x, y + 6, x + 24, y + 18], fill=c)
        g.text((x + 34, y), text, fill=INK, font=f20)
    out_dir.mkdir(parents=True, exist_ok=True)
    img.save(out_dir / f"{key}.png", optimize=True)
    return ranges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--radius", type=int, default=250)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    for key, label, path, _ in TRACKS:
        if not path.exists():
            print(f"{key}: missing {path}")
            continue
        ranges = draw(key, label, path, args.radius, args.out)
        text = ", ".join(f"{a:.2f}-{b:.2f} (closest {c:.0f} m)" for a, b, c in ranges) or "none"
        print(f"{key}: {text}")
    for group, name in (("yes", "all.png"), ("no", "counter.png")):
        keys = [k for k, _, p, g in TRACKS if g == group and p.exists()]
        sheet(args.out, keys, name)


def sheet(out_dir, keys, name, cols=4, cell=450):
    """All layouts on one image, for the request post."""
    rows = math.ceil(len(keys) / cols)
    img = Image.new("RGB", (cols * cell, rows * cell), BG)
    for i, key in enumerate(keys):
        tile = Image.open(out_dir / f"{key}.png").resize((cell, cell), Image.LANCZOS)
        img.paste(tile, ((i % cols) * cell, (i // cols) * cell))
    img.save(out_dir / name, optimize=True)


if __name__ == "__main__":
    main()
