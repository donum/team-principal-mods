"""Build team and engine-maker logo tiles (1024x1024, transparent) for a season.

Sources per entry in <season>/art/logos.json:

* "ams2":    a period decal cropped from an Automobilista 2 livery texture
             (used with the livery author's permission): texture, box
             [x0, y0, x1, y1], optional rotate. Shown as a sticker plate.
* "commons": a period logo file from Wikimedia Commons (public domain or
             free licence; recorded in the entry), optionally on a plate.
* "crest":   a plain period-style text crest in the team colours, for teams
             with no surviving free logo.
* "file":    a logo file from a local folder outside the repo (so the
             source files stay out of git): "logo_folders": {"<season or
             base folder name>": "<dir>"} in local.json, or --source.
             "bg": [r, g, b] trims a plain background colour off it.
             "origin" records where the file came from, for the credits.
             An entry may name another key of "logo_folders" with "folder"
             (e.g. 2012 reusing the 2013 folder). An .svg is rendered with headless Edge/Chrome ("browser" in
             local.json, else Edge's default path) into build/art/.

Optional layout keys for any source:

* "stack": true    split a side-by-side logo (emblem left, wordmark right) at
                   its widest empty column gap and stack the parts, emblem on
                   top, so a wide logo fills the square tile;
* "recolor": [[from_rgb, to_rgb, tolerance], ...]  swap a colour, e.g. a
                   black wordmark to white for the game's dark screens;
* "stack_color": [r, g, b]  with "stack": the emblem's colour, to split
                   emblem and wordmark that overlap in columns;
* "stack_ratio":   with "stack": wordmark width / emblem width (default 1.35);
* "lift":          raise the darkest tones to this value (0-255), so a
                   chrome logo reads as silver on dark screens;
* "pad":           plate padding as a share of the logo size (default 0.10);
* "crop": [x0, y0, x1, y1]  keep only this part of the logo, as shares of
                   its trimmed size (e.g. drop a slogan or a second emblem);
* "content":       the logo's largest side in the 1024 px tile (default 860);
                   a wide logo can take up to about 1000.
* "team_content":  (engines) the logo's size when it stands for a team, see
                   "team_tiles" below.
* "outline": {"width": px, "opacity": 0-1, "color": [r, g, b]}  a dark edge
                   around the logo's shape, in tile pixels (about 40 px per
                   screen pixel at the game's list-icon size), so a chrome
                   emblem stays visible on light team colours. Default
                   colour [15, 15, 18].

"team_tiles": "maker" in a season's logos.json puts each team's maker emblem
(the engine logo of its engine_supplier, from this file or the base's) in
assets/logos, sized by "team_content" (the game draws team icons a little
smaller than engine icons, so a larger value makes the two columns match). The game shows these tiles as small list icons,
where a team logo can't be recognised. The team logos are still built, into
build/art/<season>/team_logos/ (not in the pack or git), for when the game
shows them larger.

Team tiles go to assets/logos/<TeamName without spaces>.png. Engine tiles go
to assets/engines/ under both the supplier key and the engine name (the game
looks them up by name with spaces removed). Tyre supplier tiles ("tyres")
go to assets/tyre/<Supplier>.png.

Usage:
    python tools/logo_art.py seasons/dtm-1991 [--only key] [--preview]
"""

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

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


def split_color(logo, color, tol=80):
    """Split a logo into its emblem (pixels near `color`) and the rest."""
    import numpy as np
    a = np.asarray(logo).copy()
    near = (np.abs(a[:, :, :3].astype(int) - color).max(axis=2) <= tol) & (a[:, :, 3] > 20)
    emblem, rest = a.copy(), a.copy()
    emblem[~near, 3] = 0
    rest[near, 3] = 0
    return trim(Image.fromarray(emblem)), trim(Image.fromarray(rest))


def lift(logo, low):
    """Raise the darkest tones to `low` (0-255): a chrome logo stays 3D but
    reads as silver on the game's dark screens."""
    r, g, b, a = logo.split()
    ramp = lambda v: round(low + (255 - low) * v / 255)
    return Image.merge("RGBA", [c.point(ramp) for c in (r, g, b)] + [a])


def stack(logo, gap_share=0.12, emblem_color=None, ratio=1.35):
    """Stack emblem over wordmark: split at the widest fully transparent
    column run, or by the emblem's colour when the parts overlap."""
    if emblem_color:
        top, bottom = split_color(logo, emblem_color)
        return stack_parts(top, bottom, gap_share, ratio)
    alpha = logo.split()[3].point(lambda v: 255 if v > 20 else 0)
    w, h = logo.size
    cols = [alpha.crop((x, 0, x + 1, h)).getbbox() is None for x in range(w)]
    best, run, start = (0, 0), 0, 0
    for x, empty in enumerate(cols):
        if empty:
            run, start = (run + 1, start) if run else (1, x)
            if run > best[0]:
                best = (run, start)
        else:
            run = 0
    if not best[0]:
        return logo
    cut = best[1] + best[0] // 2
    return stack_parts(trim(logo.crop((0, 0, cut, h))), trim(logo.crop((cut, 0, w, h))), gap_share, ratio)


def stack_parts(top, bottom, gap_share, ratio=1.35):
    # The emblem keeps its size; the wordmark is scaled to the emblem's width.
    scale = top.size[0] * ratio / bottom.size[0]
    bottom = bottom.resize((round(bottom.size[0] * scale), round(bottom.size[1] * scale)), Image.LANCZOS)
    gap = int(top.size[1] * gap_share)
    out = Image.new("RGBA", (max(top.size[0], bottom.size[0]), top.size[1] + gap + bottom.size[1]), (0, 0, 0, 0))
    out.paste(top, ((out.size[0] - top.size[0]) // 2, 0), top)
    out.paste(bottom, ((out.size[0] - bottom.size[0]) // 2, top.size[1] + gap), bottom)
    return out


def recolor(logo, rules):
    """Swap colours: every pixel within tolerance of a source colour gets the target colour."""
    px = logo.load()
    for y in range(logo.size[1]):
        for x in range(logo.size[0]):
            r, g, b, a = px[x, y]
            if not a:
                continue
            for src, dst, tol in rules:
                if max(abs(r - src[0]), abs(g - src[1]), abs(b - src[2])) <= tol:
                    px[x, y] = (dst[0], dst[1], dst[2], a)
                    break
    return logo


def crop_share(logo, box):
    w, h = logo.size
    return trim(logo.crop((round(box[0] * w), round(box[1] * h), round(box[2] * w), round(box[3] * h))))


def fit_tile(logo, content=CONTENT):
    scale = content / max(logo.size)
    logo = logo.resize((max(1, round(logo.size[0] * scale)), max(1, round(logo.size[1] * scale))), Image.LANCZOS)
    tile = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    tile.paste(logo, ((TILE - logo.size[0]) // 2, (TILE - logo.size[1]) // 2), logo)
    return tile


def outlined(tile, spec):
    """Put a dark edge of spec["width"] px around the tile's opaque shape."""
    if not spec:
        return tile
    r = spec["width"]
    alpha = tile.split()[3]
    grown = alpha.copy()
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                grown = ImageChops.lighter(grown, ImageChops.offset(alpha, dx, dy))
    grown = grown.filter(ImageFilter.GaussianBlur(max(1, r / 8)))
    grown = grown.point(lambda v: round(v * spec.get("opacity", 1.0)))
    edge = Image.new("RGBA", tile.size, tuple(spec.get("color", [15, 15, 18])) + (0,))
    edge.putalpha(grown)
    return Image.alpha_composite(edge, tile)


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


def build_logo(spec, zip_path, folder=None):
    return load_logo(spec, zip_path, folder)


EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def render_svg(path, height=600):
    """Render an SVG to a transparent PNG (cached) with a headless browser."""
    import re
    import subprocess
    import tempfile
    text = path.read_text(encoding="utf-8")
    if re.search(r"<script|href=\"(?:https?:)?//", text):
        raise SystemExit(f"{path.name}: SVG with scripts or external links, not rendered")
    m = re.search(r'<svg[^>]*?\swidth="([\d.]+)[a-z]*"[^>]*?\sheight="([\d.]+)[a-z]*"', text, re.S)
    w, h = (float(m.group(1)), float(m.group(2))) if m else (1000.0, 1000.0)
    W, H = round(w * height / h), height
    out = CACHE / ("svg_" + path.stem + f"_{H}.png")
    if out.exists() and out.stat().st_mtime > path.stat().st_mtime:
        return Image.open(out).convert("RGBA")
    local = load_json(REPO / "local.json") if (REPO / "local.json").exists() else {}
    browser = Path(local.get("browser", EDGE))
    CACHE.mkdir(parents=True, exist_ok=True)
    import time
    out.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        page = Path(tmp) / "svg.html"
        page.write_text(f'<html><body style="margin:0;background:transparent">'
                        f'<img src="{path.resolve().as_uri()}" style="display:block;width:{W}px;height:{H}px"></body></html>',
                        encoding="utf-8")
        subprocess.run([str(browser), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--user-data-dir={Path(tmp) / 'profile'}", "--default-background-color=00000000",
                        f"--window-size={W},{H}", f"--screenshot={out}", page.as_uri()],
                       check=True, capture_output=True, timeout=120)
        # The browser's launcher returns before its renderer has written the
        # screenshot: wait for the file to appear and stop growing.
        size = -1
        for _ in range(120):
            time.sleep(0.5)
            if out.exists() and out.stat().st_size == size > 0:
                break
            size = out.stat().st_size if out.exists() else -1
        else:
            raise SystemExit(f"{path.name}: the browser wrote no image ({browser})")
    return Image.open(out).convert("RGBA")


def load_logo(spec, zip_path, folder):
    kind = spec["source"]
    if kind == "file":
        if folder is None:
            raise SystemExit('a "file" logo needs --source or "logo_folders" in local.json')
        src = Path(folder) / spec["file"]
        raw = render_svg(src) if src.suffix.lower() == ".svg" else Image.open(src).convert("RGBA")
        logo = trim(raw, spec.get("bg"))
        if spec.get("crop"):
            logo = crop_share(logo, spec["crop"])
            if spec.get("bg"):
                logo = trim(logo, spec["bg"])
        if spec.get("recolor"):
            logo = recolor(logo, spec["recolor"])
        if spec.get("plate"):
            return on_plate(logo, spec["plate"], pad=spec.get("pad", 0.10), border=spec.get("border"))
        return logo
    if kind == "ams2":
        tex = ams2_texture(zip_path, spec["texture"])
        crop = tex.crop(tuple(spec["box"])).rotate(spec.get("rotate", 0), expand=True)
        bg = spec.get("bg") or crop.convert("RGB").getpixel((2, 2))
        logo = trim(crop, bg)
        return on_plate(logo, bg, border=spec.get("border", [30, 30, 30]))
    if kind == "commons":
        logo = trim(commons_png(spec["file"], width=spec.get("width", 1600)))
        if spec.get("crop"):
            logo = crop_share(logo, spec["crop"])
        if spec.get("recolor"):
            logo = recolor(logo, spec["recolor"])
        if spec.get("lift"):
            logo = lift(logo, spec["lift"])
        if spec.get("stack"):
            logo = stack(logo, emblem_color=spec.get("stack_color"), ratio=spec.get("stack_ratio", 1.35))
        if spec.get("plate"):
            return on_plate(logo, spec["plate"], pad=spec.get("pad", 0.10), border=spec.get("border"))
        return logo
    if kind == "crest":
        return crest(spec)
    raise SystemExit(f"unknown logo source {kind!r}")


def team_maker_tiles(season, cfg, zip_path):
    """assets/logos/<Team>.png = the team's maker emblem ("team_tiles": "maker")."""
    import layers
    engines = {}
    for layer in layers.chain(season):
        engines.update(load_json(layer / "art" / "logos.json").get("engines", {}) if (layer / "art" / "logos.json").exists() else {})
    engines.update(cfg.get("engines", {}))
    teams = load_json(layers.files(season, "data")["teams.json"])
    teams = teams["records"] if isinstance(teams, dict) else teams
    out_dir = season / "assets" / "logos"
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.png"):
        old.unlink()
    cache, done = {}, []
    for team in teams:
        make = team["engine_supplier"]
        if make not in engines:
            raise SystemExit(f"team {team['name']}: no engine logo for {make!r} to use as its tile")
        if make not in cache:
            spec = engines[make]
            cache[make] = outlined(fit_tile(build_logo(spec, zip_path), spec.get("team_content", spec.get("content", CONTENT))),
                                   spec.get("outline"))
        cache[make].save(out_dir / f"{team['name'].replace(' ', '')}.png", optimize=True)
        done.append((team["name"], cache[make]))
        print(f"wrote logos/{team['name'].replace(' ', '')}.png ({make} emblem)")
    return done


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("season", type=Path)
    parser.add_argument("--only")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--source", help='folder of "file" logos (else local.json "logo_folders")')
    args = parser.parse_args()
    season = args.season.resolve()
    cfg = load_json(season / "art" / "logos.json")
    local = load_json(REPO / "local.json") if (REPO / "local.json").exists() else {}
    zip_path = local.get("ams2_mod_zip")
    folders = local.get("logo_folders", {})
    done = []
    maker_tiles = cfg.get("team_tiles") == "maker"
    for group, folder in (("teams", "logos"), ("engines", "engines"), ("tyres", "tyre")):
        # With maker tiles the team logos stay out of the pack and of git
        # (some are the teams' own, non-free logos): build/art/<season>/team_logos.
        out_dir = CACHE / season.name / "team_logos" if group == "teams" and maker_tiles else season / "assets" / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        for key, spec in cfg.get(group, {}).items():
            if args.only and key != args.only:
                continue
            logo_dir = args.source or folders.get(spec.get("folder", season.name))
            tile = outlined(fit_tile(build_logo(spec, zip_path, logo_dir), spec.get("content", CONTENT)), spec.get("outline"))
            names = [key] + spec.get("also_as", [])
            for name in names:
                path = out_dir / f"{name.replace(' ', '')}.png"
                tile.save(path, optimize=True)
            done.append((key, tile))
            print(f"wrote {folder}/{names[0].replace(' ', '')}.png" + (f" (+{len(names) - 1})" if len(names) > 1 else ""))
    if maker_tiles and not args.only:
        done += team_maker_tiles(season, cfg, zip_path)
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
