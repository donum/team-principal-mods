"""Crop hand-drawn car sheets into the game's 2048x1024 team car images.

A season's art/drawings.json lists sheets from an artist: square images of a
team's cars on a black background, stacked top to bottom. Each car is cut
out (the background made transparent; the tyres and wheel arches stay
black), scaled to the span car_art.py uses (1840 px wide) with the tyres
standing on y=720, so every team image sits on the same ground line, and
written:

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

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from scipy import ndimage

from car_art import CACHE, CANVAS, CAR_SPAN_PX, GROUND_Y, REPO, font, load_json

BLACK_MAX = 1        # background is 0-1; tyre rubber and arch gaps start at 2
SPECK_PX = 300       # car pixels in a smaller island are background noise
TYRE_R = 0.075       # tyre radius as a share of the car's length (search guess)
ARCH_GAP = 0.25      # the dark gap kept around a tyre, as a share of its radius
UNDERFLOOR = 0.6     # dark gaps up to this share of a tyre radius tall are
                     # filled in a car's lower part (splitter, diffuser)


def foreground(rgb):
    """Pixels that aren't the black background reachable from the edges."""
    dark = rgb.max(axis=2) <= BLACK_MAX
    labels, _ = ndimage.label(dark)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    bg = np.isin(labels, edge[edge > 0])
    # The background has a little noise just above the threshold next to
    # the tyres; drop those specks.
    labels, n = ndimage.label(~bg)
    sizes = ndimage.sum(~bg, labels, range(1, n + 1))
    return np.isin(labels, np.flatnonzero(sizes >= SPECK_PX) + 1)


def ground_row(alpha):
    """The row where both tyres touch the ground (lowest row with car pixels
    at the front and at the back), so a splitter or a stray pixel below the
    tyres doesn't move the car."""
    mask = np.asarray(alpha) > 128
    width = mask.shape[1]
    for y in range(mask.shape[0] - 1, -1, -1):
        xs = np.flatnonzero(mask[y])
        if len(xs) < 16:
            continue
        runs = np.split(xs, np.flatnonzero(np.diff(xs) > 1) + 1)
        long = [r for r in runs if len(r) >= 8]
        if len(long) >= 2 and long[-1][0] - long[0][-1] >= 0.4 * width:
            return y
    raise SystemExit("no tyres found on a car")


def split_cars(fg, n):
    """A car number (1..n, top to bottom) for every foreground pixel.

    Cars on a sheet can overlap in height (one car's tyres lower than the
    next car's wing top) and an antenna can touch the car above, so rows
    alone can't separate them. Thin vertical strokes (antennas) are set
    aside, the rest falls into connected parts, the n largest parts are the
    car bodies, and every other part joins the body it is closest to (wheels)
    or, for a thin stroke, the car it stands on.
    """
    eight = np.ones((3, 3), bool)
    core = ndimage.binary_opening(fg, structure=np.ones((1, 7), bool))
    labels, count = ndimage.label(core, structure=eight)
    sizes = ndimage.sum(core, labels, range(1, count + 1))
    objs = ndimage.find_objects(labels)
    bodies = sorted((int(i) + 1 for i in np.argsort(sizes)[::-1][:n]), key=lambda i: objs[i - 1][0].start)
    if len(bodies) < n:
        raise SystemExit(f"found {len(bodies)} cars, expected {n}")
    # Every other part (wheels, mirrors, an antenna mount) joins the body
    # most of its pixels are closest to.
    body = np.zeros(fg.shape, np.int8)
    for k, b in enumerate(bodies, start=1):
        body[labels == b] = k
    _, (iy, ix) = ndimage.distance_transform_edt(body == 0, return_indices=True)
    nearest = body[iy, ix]
    votes = np.zeros((count + 1, n + 1), np.int64)
    np.add.at(votes, (labels[core], nearest[core]), 1)
    assign = (votes[:, 1:].argmax(axis=1) + 1).astype(np.int8)
    assign[0] = 0
    car = assign[labels]
    thin, _ = ndimage.label(fg & (car == 0), structure=eight)
    for i, sl in enumerate(ndimage.find_objects(thin), start=1):
        # Look one pixel around the piece for the cars it touches.
        y0, x0 = max(sl[0].start - 1, 0), max(sl[1].start - 1, 0)
        win = (slice(y0, sl[0].stop + 1), slice(x0, sl[1].stop + 1))
        piece = thin[win] == i
        ring = ndimage.binary_dilation(piece, eight) & (car[win] > 0)
        ys, xs = np.nonzero(ring)
        if len(ys):
            # An antenna stands on its own car: take the car under its foot.
            car[win][piece] = car[win][ys.max(), xs[ys.argmax()]]
    return car


def claim_antennas(fg, owner, n):
    """Give each car back its antenna where it reaches into the car above.

    A car's topmost pixels are its antenna mount. From there, follow the
    antenna upwards row by row: take the narrow run of pixels next to where
    the last row's run was, until the runs get wide (the car above's body or
    tyre) or stop.
    """
    for k in range(2, n + 1):
        ys, xs = np.nonzero(owner == k)
        top = ys.min()
        x, reach, misses = float(np.median(xs[ys == top])), 16, 0
        for y in range(top - 1, max(top - 200, -1), -1):
            row = fg[y]
            lo, hi = max(int(x) - reach, 0), int(x) + reach + 1
            hits = np.flatnonzero(row[lo:hi]) + lo
            if not len(hits):
                misses += 1
                if misses > 2:
                    break
                continue
            # The run of pixels around the hit nearest the line.
            start = end = hits[np.abs(hits - x).argmin()]
            while start > 0 and row[start - 1]:
                start -= 1
            while end + 1 < len(row) and row[end + 1]:
                end += 1
            if end - start + 1 > 16:
                break
            # Specks along the antenna come with it.
            near = slice(max(start - 4, 0), end + 5)
            owner[y, near][row[near]] = k
            x, reach, misses = (start + end) / 2, 8, 0


def underfloor(mine, ground, radius):
    """Dark parts of the underfloor (the splitter's top, the diffuser) are
    as black as the background: fill short vertical gaps in a car's lower
    part, between the bodywork above and the splitter edge below."""
    size = max(3, int(UNDERFLOOR * radius)) | 1
    closed = cv2.morphologyEx(mine.astype(np.uint8), cv2.MORPH_CLOSE,
                              np.ones((size, 1), np.uint8)) > 0
    band = np.zeros_like(mine)
    band[max(int(ground - 1.2 * radius), 0):ground + 1] = True
    return closed & band & ~mine


def tyres(gray, mine):
    """Black around the tyres: each tyre's disc plus the gap up to the wheel
    arch, which the background cut-out partly eats (the rubber and the gap
    are as dark as the background).

    A tyre stands on the ground row; its rim is a clear circle (found with a
    Hough transform), and the tyre's radius is the rim centre's height above
    the ground.
    """
    ys, xs = np.nonzero(mine)
    x0, x1, y0 = xs.min(), xs.max(), ys.min()
    crop = mine[y0:ys.max() + 1, x0:x1 + 1]
    ground = y0 + ground_row(Image.fromarray((crop * 255).astype(np.uint8)))
    row = np.flatnonzero(mine[ground])
    runs = [r for r in np.split(row, np.flatnonzero(np.diff(row) > 1) + 1) if len(r) >= 8]
    guess = TYRE_R * (x1 - x0)
    extra = np.zeros_like(mine)
    radii = []
    yy, xx = np.ogrid[:mine.shape[0], :mine.shape[1]]
    for run in (runs[0], runs[-1]):
        cx = int(run.mean())
        wx0, wy0 = max(int(cx - 1.3 * guess), 0), max(int(ground - 2.3 * guess), 0)
        win = cv2.medianBlur(np.ascontiguousarray(gray[wy0:ground + 5, wx0:int(cx + 1.3 * guess)]), 5)
        found = cv2.HoughCircles(win, cv2.HOUGH_GRADIENT, dp=1, minDist=1000, param1=120, param2=25,
                                 minRadius=int(0.45 * guess), maxRadius=int(0.8 * guess))
        if found is None:
            raise SystemExit(f"no wheel rim found near x={cx}")
        hx, hy = found[0][0][0] + wx0, found[0][0][1] + wy0
        r = ground - hy
        radii.append(r)
        if not 0.8 * guess < r < 1.2 * guess:
            raise SystemExit(f"odd tyre radius {r:.0f} (expected about {guess:.0f})")
        dist = np.hypot(xx - hx, yy - hy)
        extra |= dist <= r
        # The arch gap: what closing the car's outline adds in a ring
        # around the tyre, above the ground.
        ring = (dist <= r * (1 + ARCH_GAP)) & (yy <= ground)
        size = max(3, int(r * ARCH_GAP)) | 1
        closed = cv2.morphologyEx((mine | extra).astype(np.uint8), cv2.MORPH_CLOSE,
                                  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))) > 0
        extra |= closed & ring
    return extra & ~mine, ground, float(np.mean(radii))


def apply_edits(im, edits):
    """Small text fixes on the artist's sheet. "cut" removes the columns
    [x0, x1) from rows [y0, y1) by moving what's right of them (up to
    "until") left, e.g. a letter too many in a name panel."""
    rgb = np.array(im)
    for edit in edits:
        (x0, x1), (y0, y1), until = edit["cut"], edit["rows"], edit["until"]
        width = x1 - x0
        rgb[y0:y1, x0:until - width] = rgb[y0:y1, x1:until].copy()
        # The vacated strip takes the panel's colour from just right of it.
        rgb[y0:y1, until - width:until] = rgb[y0:y1, until:until + width][:, ::-1]
    return Image.fromarray(rgb)


def cut_cars(path, n, edits=()):
    """The n cars on a sheet, top to bottom, as RGBA crops."""
    im = apply_edits(Image.open(path).convert("RGB"), edits)
    rgb = np.asarray(im)
    fg = foreground(rgb)
    owner = split_cars(fg, n)
    claim_antennas(fg, owner, n)
    for k in range(1, n + 1):
        # Specks cut off from a car (left over from a neighbour's antenna)
        # would be joined up by the underfloor fill: drop them.
        labels, count = ndimage.label(owner == k, structure=np.ones((3, 3), bool))
        sizes = ndimage.sum(owner == k, labels, range(1, count + 1))
        specks = np.isin(labels, np.flatnonzero(sizes < SPECK_PX // 5) + 1)
        owner[specks] = 0
        fg &= ~specks
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    masks = []
    for k in range(1, n + 1):
        own = owner == k
        add, ground, radius = tyres(gray, own)
        add |= underfloor(own | add, ground, radius)
        mine = own | add
        # Nothing of a car hangs below its tyres; a sliver there is the
        # antenna tip of the car underneath.
        mine[ground + 3:] = False
        # Where the fill behind a tyre or under the floor crosses a
        # neighbour's antenna, this car shows its dark underside instead.
        masks.append((mine, add & (owner > 0) & ~own))
    fg = np.logical_or.reduce([mine for mine, _ in masks])
    alpha = Image.fromarray((fg * 255).astype(np.uint8))
    # Pull the edge in by a pixel and soften it: the drawing is antialiased
    # against black, which would leave a dark fringe on a light background.
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    cars = []
    for mine, dark in masks:
        pixels = np.array(im)
        pixels[dark] = 0
        car = Image.new("RGBA", im.size, (0, 0, 0, 0))
        car.paste(Image.fromarray(pixels), mask=Image.fromarray(mine))
        car.putalpha(ImageChops.multiply(car.getchannel("A"), alpha))
        rows, cols = np.where(mine.any(axis=1))[0], np.where(mine.any(axis=0))[0]
        cars.append(car.crop((int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1)))
    return cars


def place(car):
    """A car crop on the game canvas, scaled to car_art.py's span, tyres on GROUND_Y."""
    scale = CAR_SPAN_PX / car.width
    w, h = CAR_SPAN_PX, round(car.height * scale)
    small = car.resize((w, h), Image.LANCZOS)
    top = GROUND_Y - ground_row(small.getchannel("A"))
    if top < 0 or top + h > CANVAS[1]:
        raise SystemExit(f"car doesn't fit the canvas (top {top}, height {h})")
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    canvas.alpha_composite(small, ((CANVAS[0] - w) // 2, top))
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
        cars = cut_cars(source / name, len(sheet["cars"]), sheet.get("edits", ()))
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
