"""Main menu background (assets/title_bg.png) from a race photo.

The game draws the menu over the left ~40% of the background (logo, buttons
and a tint in the player's colour theme) and dims the whole image a little,
so the photo is placed against the right edge: it fills the full height and
the strip left over on the left (under the menu) is a blurred mirror of the
photo's edge. That keeps every car in the photo in the frame.

The game scales the image to fill the window and keeps the middle, so a
wider window loses the top and bottom (2.4:1 cuts 187 px of 1440) and a
narrower one the sides (16:10 cuts 128 px of 2560). Keep a logo at least
230 px from the top and 170 px from the right (the defaults).

Config: <season>/art/menu.json. Several photos can be kept; "use" picks the
one that is built.
    {"title_bg": {"use": "<name>",
                  "photos": {"<name>": {
                      "folder": "<key in local.json photo_folders>",
                      "file": "<path inside that folder>",
                      "crop": [x0, y0, x1, y1],      # fractions of the photo
                      "grade": "cinematic" | null,   # contrast, light on the right
                      "logo_shade": true,            # darken behind the game logo
                      "logo": {"file": "art/<png>", "width": 560, "right": 170, "top": 230},
                                                     # optional overlay, top right
                      "in_pack": true,               # free licence: ship it in the pack
                      "rights": "...", "page": "...", "caption": "..."}}}}

A photo with "in_pack": true has a free licence (or permission) and is written
to <season>/assets/title_bg.png, so it ships in the pack. Any other photo is
not free, so the image goes to private/menu_art/<season>/title_bg.png
(gitignored, never in dist/), and build_pack.py --install copies it onto the
installed pack only, unless the season has its own assets/title_bg.png.

Usage:
    python tools/menu_art.py seasons/dtm-2013 [--source FOLDER]
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

REPO = Path(__file__).resolve().parent.parent
PRIVATE = REPO / "private" / "menu_art"
SIZE = (2560, 1440)   # the game scales it (its own title_bg.png is 1672x941)


def load_json(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def private_title_bg(season_dir: Path) -> Path:
    return PRIVATE / season_dir.name / "title_bg.png"


def active_photo(season_dir: Path) -> dict:
    """The photo spec menu.json "use" points at."""
    cfg = load_json(season_dir / "art" / "menu.json")["title_bg"]
    return cfg["photos"][cfg["use"]]


def place_right(photo: Image.Image, w: int, h: int) -> Image.Image:
    """Photo at full height against the right edge; a blurred mirror fills the left."""
    s = h / photo.height
    photo = photo.resize((round(photo.width * s), h), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h))
    gap = w - photo.width
    if gap <= 0:
        canvas.paste(photo, (gap, 0))      # wider than 16:9: keep the right edge
        return canvas
    strip = photo.crop((0, 0, min(gap, photo.width), h)).transpose(Image.FLIP_LEFT_RIGHT)
    strip = ImageEnhance.Brightness(strip.resize((gap, h)).filter(ImageFilter.GaussianBlur(50))).enhance(0.7)
    canvas.paste(strip, (0, 0))
    canvas.paste(photo, (gap, 0))
    seam = 80
    band = canvas.crop((gap - seam, 0, gap + seam, h)).filter(ImageFilter.GaussianBlur(24))
    mask = Image.linear_gradient("L").rotate(90).resize((2 * seam, h))
    mask = Image.eval(mask, lambda v: 255 - abs(v - 128) * 2)
    canvas.paste(band, (gap - seam, 0), mask)
    return canvas


def cinematic(img: Image.Image) -> Image.Image:
    """More contrast and colour, cool shadows, warm highlights, light on the right."""
    a = np.asarray(img).astype(np.float32) / 255
    a = np.clip((a - 0.5) * 1.12 + 0.5, 0, 1)
    lum = a.mean(2, keepdims=True)
    a = lum + (a - lum) * 1.08
    a[..., 2] += (0.5 - lum[..., 0]) * 0.05
    a[..., 0] += (lum[..., 0] - 0.5) * 0.04
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w * 0.70) / (w * 0.55)) ** 2 + ((yy - h * 0.6) / (h * 0.75)) ** 2)
    a *= np.clip(1.08 - 0.45 * d ** 2, 0.55, 1.08)[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def logo_shade(img: Image.Image) -> Image.Image:
    """Darken softly behind the game's yellow logo (top left) so it stays readable."""
    a = np.asarray(img).astype(np.float32)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w * 0.22) / (w * 0.33)) ** 2 + ((yy - h * 0.2) / (h * 0.22)) ** 2)
    a *= (1 - 0.6 * np.exp(-d ** 2 * 1.6))[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def overlay_logo(img: Image.Image, logo: Image.Image, width: int, right: int, top: int) -> Image.Image:
    """Paste a logo (RGBA) at the top right with a soft drop shadow."""
    logo = logo.resize((width, round(logo.height * width / logo.width)), Image.LANCZOS)
    x, y = img.width - right - logo.width, top
    pad = 42
    shadow = Image.new("L", (logo.width + 2 * pad, logo.height + 2 * pad), 0)
    shadow.paste(logo.split()[3].point(lambda v: v * 170 // 255), (pad, pad))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    out = img.convert("RGBA")
    out.paste(Image.new("RGBA", shadow.size, (0, 0, 0, 255)), (x - pad + 4, y - pad + 6), shadow)
    out.alpha_composite(logo, (x, y))
    return out.convert("RGB")


def render(spec: dict, folder: Path, season: Path | None = None) -> Image.Image:
    photo = Image.open(folder / spec["file"]).convert("RGB")
    x0, y0, x1, y1 = spec.get("crop", [0, 0, 1, 1])
    pw, ph = photo.size
    photo = photo.crop((round(x0 * pw), round(y0 * ph), round(x1 * pw), round(y1 * ph)))
    img = place_right(photo, *SIZE)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2))
    if spec.get("grade") == "cinematic":
        img = cinematic(img)
    if spec.get("logo_shade"):
        img = logo_shade(img)
    if spec.get("logo") and season is not None:
        lg = spec["logo"]
        img = overlay_logo(img, Image.open(season / lg["file"]).convert("RGBA"),
                           lg.get("width", 560), lg.get("right", 170), lg.get("top", 230))
    return img


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("season", type=Path)
    parser.add_argument("--source", help='photo folder (else local.json "photo_folders")')
    args = parser.parse_args()
    season = args.season.resolve()
    spec = active_photo(season)
    local = load_json(REPO / "local.json") if (REPO / "local.json").exists() else {}
    folder = args.source or local.get("photo_folders", {}).get(spec.get("folder", season.name))
    if not folder:
        sys.exit('no photo folder: pass --source or set "photo_folders" in local.json')
    out = season / "assets" / "title_bg.png" if spec.get("in_pack") else private_title_bg(season)
    out.parent.mkdir(parents=True, exist_ok=True)
    render(spec, Path(folder), season).save(out, optimize=True)
    print(f"wrote {out.relative_to(REPO)} ({SIZE[0]}x{SIZE[1]}, photo \"{load_json(season / 'art' / 'menu.json')['title_bg']['use']}\")")


if __name__ == "__main__":
    main()
