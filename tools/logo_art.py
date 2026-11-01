"""Build team and engine-maker logo tiles (1024x1024, transparent) for a season.

Sources per entry in <season>/art/logos.json:

* "ams2":    a period decal cropped from an Automobilista 2 livery texture
             (used with the livery author's permission): texture, box
             [x0, y0, x1, y1], optional rotate. Shown as a sticker plate.
* "commons": a period logo file from Wikimedia Commons (public domain or
             free licence; recorded in the entry), optionally on a plate.
* "crest":   a plain period-style text crest in the team colours, for teams
             with no surviving free logo.

Team tiles go to assets/logos/<TeamName without spaces>.png. Engine tiles go
to assets/engines/ under both the supplier key and the engine name (the game
looks them up by name with spaces removed).

Usage:
    python tools/logo_art.py seasons/dtm-1991 [--only key] [--preview]
"""

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from car_art import CACHE, REPO, ams2_texture, commons_png, font, load_json

TILE = 1024
CONTENT = 860          # max logo extent inside the tile


def trim(img, bg=None, tol=24):
    """Crop to content: alpha, or pixels differing from the background colour."""
    rgba = img.convert("RGBA")
    if bg is None:
        box = rgba.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox()
    else:
        diff = ImageChops.difference(rgba.convert("RGB"), Image.new("RGB", rgba.size, tuple(bg)))
        mask = diff.convert("L").point(lambda v: 255 if v > tol else 0)
        mask = ImageChops.multiply(mask, rgba.split()[3].point(lambda v: 255 if v > 20 else 0))
        box = mask.getbbox()
    return rgba.crop(box) if box else rgba


def on_plate(logo, color, pad=0.10, radius=0.12, border=None):
    w, h = logo.size
    p = int(max(w, h) * pad)
    plate = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0))
    d = ImageDraw.Draw(plate)
    d.rounded_rectangle([0, 0, plate.size[0] - 1, plate.size[1] - 1], radius=int(min(plate.size) * radius),
                        fill=tuple(color) + (255,), outline=tuple(border) + (255,) if border else None,
                        width=max(2, plate.size[0] // 120) if border else 0)
    plate.paste(logo, (p, p), logo)
    return plate


def fit_tile(logo):
    scale = CONTENT / max(logo.size)
    logo = logo.resize((max(1, round(logo.size[0] * scale)), max(1, round(logo.size[1] * scale))), Image.LANCZOS)
    tile = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    tile.paste(logo, ((TILE - logo.size[0]) // 2, (TILE - logo.size[1]) // 2), logo)
    return tile


def crest(spec):
    """Period-style text crest: name in bold caps on a two-colour shield plate."""
    lines = spec["text"].split("\n")
    fg, bg, accent = (tuple(spec.get(k, d)) for k, d in
                      (("fg", [255, 255, 255]), ("bg", [20, 20, 22]), ("accent", [200, 30, 30])))
    W, H = 1200, 520 if len(lines) == 1 else 700
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=60, fill=bg + (255,), outline=accent + (255,), width=26)
    d.rectangle([60, H - 120, W - 60, H - 90], fill=accent + (255,))
    size = 190 if len(lines) == 1 else 150
    f = font(size)
    while max(d.textlength(t, font=f) for t in lines) > W - 160 and size > 40:
        size -= 6
        f = font(size)
    y = (H - 110) / 2 - (len(lines) - 1) * size * 0.55
    for t in lines:
        d.text((W / 2, y), t, font=f, fill=fg + (255,), anchor="mm")
        y += size * 1.1
    return img


def build_logo(spec, zip_path):
    kind = spec["source"]
    if kind == "ams2":
        tex = ams2_texture(zip_path, spec["texture"])
        crop = tex.crop(tuple(spec["box"])).rotate(spec.get("rotate", 0), expand=True)
        bg = spec.get("bg") or crop.convert("RGB").getpixel((2, 2))
        logo = trim(crop, bg)
        return on_plate(logo, bg, border=spec.get("border", [30, 30, 30]))
    if kind == "commons":
        logo = trim(commons_png(spec["file"], width=spec.get("width", 1600)))
        return on_plate(logo, spec["plate"], border=spec.get("border")) if spec.get("plate") else logo
    if kind == "crest":
        return crest(spec)
    raise SystemExit(f"unknown logo source {kind!r}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("season", type=Path)
    parser.add_argument("--only")
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    season = args.season.resolve()
    cfg = load_json(season / "art" / "logos.json")
    local = load_json(REPO / "local.json") if (REPO / "local.json").exists() else {}
    zip_path = local.get("ams2_mod_zip")
    done = []
    for group, folder in (("teams", "logos"), ("engines", "engines")):
        out_dir = season / "assets" / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        for key, spec in cfg.get(group, {}).items():
            if args.only and key != args.only:
                continue
            tile = fit_tile(build_logo(spec, zip_path))
            names = [key] + spec.get("also_as", [])
            for name in names:
                path = out_dir / f"{name.replace(' ', '')}.png"
                tile.save(path, optimize=True)
            done.append((key, tile))
            print(f"wrote {folder}/{names[0].replace(' ', '')}.png" + (f" (+{len(names) - 1})" if len(names) > 1 else ""))
    if args.preview and done:
        cols, s = 6, 256
        sheet = Image.new("RGB", (cols * s, math.ceil(len(done) / cols) * (s + 30)), (52, 56, 64))
        d = ImageDraw.Draw(sheet)
        for i, (key, tile) in enumerate(done):
            x, y = (i % cols) * s, (i // cols) * (s + 30)
            small = tile.resize((s, s), Image.LANCZOS)
            sheet.paste(small, (x, y + 30), small)
            d.text((x + 6, y + 6), key[:28], fill=(255, 255, 255), font=font(15))
        CACHE.mkdir(parents=True, exist_ok=True)
        sheet.save(CACHE / "logos_preview.png")
        print("preview: build/art/logos_preview.png")


if __name__ == "__main__":
    main()
