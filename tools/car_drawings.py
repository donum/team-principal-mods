"""Crop hand-drawn car sheets into the game's 2048x1024 team car images.

A season's art/drawings.json lists sheets from an artist: square images of a
team's cars on a black background, stacked top to bottom. Each car is cut
out (the background made transparent), scaled to the span car_art.py uses
(1840 px wide, wheels on y=720) and written:

* the team image to <season>/assets/Cars/<Team>.png (the game shows one car
  per team: the sheet's "team" takes its first car, "teams" names a car per
  team);
* every car to build/art/<season>/drawn_NN.png for checking.

car_art.py skips the teams listed here, so a rerun doesn't overwrite them.

The source folder is outside the repo: pass --source or set
"car_drawings": {"<season folder>": "<dir>"} in local.json.

Usage:
    python tools/car_drawings.py seasons/dtm-2013 [--source DIR] [--preview]
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from scipy import ndimage

from car_art import CACHE, CANVAS, CAR_SPAN_PX, GROUND_Y, REPO, font, load_json

BLACK_MAX = 6        # background is pure black; tyres and black bodies are lighter
MIN_CAR_ROWS = 80    # a band of rows shorter than this is not a car
BODY_ROW_PX = 40     # a row with fewer car pixels is an antenna or a gap


def foreground(rgb):
    """Pixels that aren't the black background reachable from the edges."""
    dark = rgb.max(axis=2) <= BLACK_MAX
    labels, _ = ndimage.label(dark)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    bg = np.isin(labels, edge[edge > 0])
    return ~bg


def cut_cars(path):
    """The cars on a sheet, top to bottom, as RGBA crops."""
    im = Image.open(path).convert("RGB")
    rgb = np.asarray(im)
    fg = foreground(rgb)
    # Cars can sit so close that one's antenna touches the car above, so
    # split on rows that are nearly empty (antennas only) rather than blank.
    count = fg.sum(axis=1)
    body = np.append(count >= BODY_ROW_PX, False)
    runs, start = [], None
    for y, on in enumerate(body):
        if on and start is None:
            start = y
        elif not on and start is not None:
            if y - start >= MIN_CAR_ROWS:
                runs.append((start, y))
            start = None
    cuts = [0] + [a_end + int(np.argmin(count[a_end:b_start]))
                  for (_, a_end), (b_start, _) in zip(runs, runs[1:])] + [len(count)]
    bands = list(zip(cuts, cuts[1:]))
    for (_, y1), (_, run_end) in zip(bands, runs):
        # Under a car's sill, a thin sliver is the next car's antenna tip.
        below = fg[run_end:y1]
        if not below.size:
            continue
        labels, n = ndimage.label(below)
        for i, sl in enumerate(ndimage.find_objects(labels), start=1):
            if sl[1].stop - sl[1].start < 12:
                below[labels == i] = False
    alpha = Image.fromarray((fg * 255).astype(np.uint8))
    # Pull the edge in by a pixel and soften it: the drawing is antialiased
    # against black, which would leave a dark fringe on a light background.
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    rgba = im.copy()
    rgba.putalpha(alpha)
    cars = []
    for y0, y1 in bands:
        band = np.zeros_like(fg)
        band[y0:y1] = fg[y0:y1]
        rows, cols = np.where(band.any(axis=1))[0], np.where(band.any(axis=0))[0]
        car = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
        car.paste(rgba, mask=Image.fromarray(band).convert("L").point(lambda v: 255 if v else 0))
        car.putalpha(ImageChops.multiply(car.getchannel("A"), alpha))
        cars.append(car.crop((int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1)))
    return cars


def place(car):
    """A car crop on the game canvas, scaled to car_art.py's span and ground line."""
    scale = CAR_SPAN_PX / car.width
    w, h = CAR_SPAN_PX, round(car.height * scale)
    if h > GROUND_Y:
        raise SystemExit(f"car too tall for the canvas ({h} px)")
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    canvas.alpha_composite(car.resize((w, h), Image.LANCZOS), ((CANVAS[0] - w) // 2, GROUND_Y - h))
    return canvas


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("season", type=Path)
    parser.add_argument("--source", type=Path, help="folder with the artist's sheets")
    parser.add_argument("--preview", action="store_true", help="also write build/art/drawings_preview.png")
    args = parser.parse_args()
    season = args.season.resolve()
    cfg = load_json(season / "art" / "drawings.json")
    source = args.source
    if source is None:
        local = load_json(REPO / "local.json") if (REPO / "local.json").exists() else {}
        source = local.get("car_drawings", {}).get(season.name)
        if not source:
            raise SystemExit(f'pass --source or set "car_drawings": {{"{season.name}": "<dir>"}} in local.json')
        source = Path(source)
    out_dir = season / "assets" / "Cars"
    all_dir = CACHE / season.name
    all_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, sheet in cfg["sheets"].items():
        cars = cut_cars(source / name)
        if len(cars) != len(sheet["cars"]):
            raise SystemExit(f"{name}: found {len(cars)} cars, drawings.json lists {len(sheet['cars'])}")
        by_number = dict(zip(sheet["cars"], (place(c) for c in cars)))
        for number, img in by_number.items():
            img.save(all_dir / f"drawn_{number:02d}.png", optimize=True)
        teams = {sheet["team"]: sheet["cars"][0]} if "team" in sheet else sheet["teams"]
        for team, number in teams.items():
            path = out_dir / f"{team.replace(' ', '')}.png"
            by_number[number].save(path, optimize=True)
            written.append((f"#{number} - {team}", by_number[number]))
            print(f"wrote {path.relative_to(REPO)} (#{number} from {name})")
    if args.preview:
        cols, w, h = 2, 1024, 512
        sheet = Image.new("RGB", (cols * w, math.ceil(len(written) / cols) * (h + 34)), (200, 200, 204))
        d = ImageDraw.Draw(sheet)
        for i, (label, img) in enumerate(written):
            x, y = (i % cols) * w, (i // cols) * (h + 34)
            small = img.resize((w, h), Image.LANCZOS)
            sheet.paste(small, (x, y + 34), small)
            d.text((x + 10, y + 8), label, fill=(0, 0, 0), font=font(22))
        sheet.save(CACHE / "drawings_preview.png")
        print(f"preview: {(CACHE / 'drawings_preview.png').relative_to(REPO)}")


if __name__ == "__main__":
    main()
