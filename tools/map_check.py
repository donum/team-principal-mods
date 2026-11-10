"""Check a pack's race-screen maps: does the whole lap show, and do the cars run on the drawn track?

    python tools/map_check.py dist/dtm2013 [--season seasons/dtm-2013]
    python tools/map_check.py dist/dtm2013 --shots "C:/Users/<you>/Pictures/mods/ingame screenshots"

Files (always): for every track with a race-tracks frame in <season>/track_art.json, the pack's line
(tracks/<id>.json points) against the race-tracks centreline drawn in the art (same view box):
mean / max distance in metres and how much of the lap leaves the asphalt; the lap's bounding box
against the visible map area; the start (first point) against race-tracks lap 0.

Screenshots (--shots, needs opencv-python): each 3840x2160 screenshot is matched to its track image
(SIFT + RANSAC affine), which gives the screen transform; the part of the image that shows through
the map panel is measured, and the lap is checked against it. Use it after an in-game session to
confirm the visible area (it differs with window size and aspect).

VISIBLE_BOX / COMPASS: measured 2026-11-10 at 3840x2160 (docs/CAPABILITIES.md).
"""
import argparse
import glob
import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import art_track  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
VISIBLE_BOX = (9, 124, 1035, 788)
PADDING = 16
COMPASS = (80, 210)


def seg_dist(p, Q):
    best = 1e18
    for a, b in zip(Q, Q[1:] + Q[:1]):
        ax, ay = b[0] - a[0], b[1] - a[1]
        L = ax * ax + ay * ay or 1e-9
        t = max(0.0, min(1.0, ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / L))
        best = min(best, math.hypot(a[0] + ax * t - p[0], a[1] + ay * t - p[1]))
    return best


def files_check(pack, season):
    cfg = json.loads((REPO / season / "track_art.json").read_text(encoding="utf-8"))
    root = art_track.race_tracks_root()
    ok = True
    print(f"{'track':15s} {'line vs drawn (m)':>18s} {'off asphalt':>11s} {'start':>7s} {'lap box (px)':>22s} {'fits':>5s}")
    for tid, c in cfg["tracks"].items():
        path = Path(pack) / "tracks" / f"{tid}.json"
        if not path.exists():
            continue
        g = json.loads(path.read_text(encoding="utf-8"))
        vx, vy, vw, _ = c.get("viewBoxMetres") or art_track.plan_view(root, c["race_tracks"]["track"], c["race_tracks"]["layout"])
        k = 1044 / vw
        cl = art_track.centreline(root, c["race_tracks"]["track"], c["race_tracks"]["layout"])
        drawn = [((x - vx) * k, (y - vy) * k) for x, y in cl[::3]]
        pts = [tuple(p) for p in g["points"]]
        d = [seg_dist(p, drawn) / k for p in pts]
        half = g["racing_surface"]["width_m"] / 2
        off = sum(x > half for x in d) / len(d)
        start = math.dist(pts[0], drawn[0]) / k
        h = half * k
        x0, x1 = min(p[0] for p in pts) - h, max(p[0] for p in pts) + h
        y0, y1 = min(p[1] for p in pts) - h, max(p[1] for p in pts) + h
        b = VISIBLE_BOX
        fits = (x0 >= b[0] + PADDING and x1 <= b[2] - PADDING and y0 >= b[1] + PADDING and y1 <= b[3] - PADDING
                and not any(p[0] < COMPASS[0] + h and p[1] < COMPASS[1] + h for p in pts))
        good = fits and off == 0 and start < 15
        ok &= good
        print(f"{tid:15s} {sum(d) / len(d):8.1f} / {max(d):6.1f}  {off * 100:9.1f}%  {start:5.0f} m "
              f"({x0:4.0f},{y0:4.0f})-({x1:4.0f},{y1:4.0f}) {'yes' if fits else 'NO':>5s}{'' if good else '  <--'}")
    return ok


def shots_check(pack, shots):
    import cv2
    import numpy as np
    sift = cv2.SIFT_create(6000)
    arts = {}
    for p in sorted(glob.glob(str(Path(pack) / "assets" / "tracks" / "*.png"))):
        arts[Path(p).stem] = sift.detectAndCompute(cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2GRAY), None)
    bf = cv2.BFMatcher()
    for f in sorted(glob.glob(os.path.join(shots, "*.png")), key=os.path.getmtime):
        im = cv2.imread(f)
        if im.shape[1] < 3000:
            continue
        crop = cv2.cvtColor(cv2.resize(im[244:1740, 16:2056], None, fx=.5, fy=.5, interpolation=cv2.INTER_AREA),
                            cv2.COLOR_BGR2GRAY)
        kp, d = sift.detectAndCompute(crop, None)
        best = None
        for name, (ka, da) in arts.items():
            if d is None or da is None:
                continue
            good = [m[0] for m in bf.knnMatch(da, d, k=2) if len(m) == 2 and m[0].distance < .75 * m[1].distance]
            if len(good) < 12:
                continue
            src = np.float32([ka[m.queryIdx].pt for m in good])
            dst = np.float32([kp[m.trainIdx].pt for m in good]) / .5 + np.float32([16, 244])
            A, inl = cv2.estimateAffine2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=6)
            if A is not None and (best is None or inl.sum() > best[1]):
                best = (name, int(inl.sum()), A)
        if not best or best[1] < 30:
            continue
        name, n, A = best
        art = cv2.imread(str(Path(pack) / "assets" / "tracks" / f"{name}.png"))
        w = cv2.warpAffine(art, A, (im.shape[1], im.shape[0]), borderValue=(255, 0, 255)).astype(np.int16)
        m = (np.abs(im.astype(np.int16) - w).sum(2) < 60).astype(np.uint8)
        rows, cols = m[:, :2100].mean(1), m[300:1500].mean(0)
        r0, r1 = int(np.argmax(rows > .5)), int(len(rows) - np.argmax(rows[::-1] > .5))
        c0, c1 = int(np.argmax(cols > .5)), int(len(cols) - np.argmax(cols[::-1] > .5))
        inv = lambda x, y: ((x - A[0][2]) / A[0][0], (y - A[1][2]) / A[1][1])
        (vx0, vy0), (vx1, vy1) = inv(c0, r0), inv(c1, r1)
        g = json.loads((Path(pack) / "tracks" / f"{name}.json").read_text(encoding="utf-8"))
        out = sum(1 for x, y in g["points"] if not (vx0 <= x <= vx1 and vy0 <= y <= vy1))
        print(f"{Path(f).name[:12]} {name:15s} scale {A[0][0]:.3f}/{A[1][1]:.3f}  visible x {vx0:.0f}-{vx1:.0f} "
              f"y {vy0:.0f}-{vy1:.0f}  line points outside: {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pack")
    ap.add_argument("--season", default="seasons/dtm-2013")
    ap.add_argument("--shots")
    a = ap.parse_args()
    ok = files_check(a.pack, a.season)
    if a.shots:
        shots_check(a.pack, a.shots)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
