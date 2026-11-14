"""Find sharp side-on car shots in race videos, as raw material for livery drawings.

Samples a video every --step seconds (ffmpeg, small frames), runs torchvision's
pretrained Faster R-CNN (COCO "car"/"truck") on each sample and keeps scenes with
one large, complete, wide car box (wide box = side-on view). For each hit it then
grabs a few full-resolution frames around the timestamp and keeps the sharpest
(variance of the Laplacian inside the car box).

Output per video: <out>/<video-stem>/<hh-mm-ss>.jpg (full frame), *_crop.jpg (car
with margin) and candidates.csv. Labelling (car number, side) is done by hand
afterwards; see tools/livery_pack.py.

    python tools/livery_frames.py VIDEO [VIDEO...] --out DIR [--step 2]
"""
import argparse, csv, os, subprocess, sys
from pathlib import Path

import cv2
import numpy as np
import torch
import torchvision

SMALL_W = 640                    # analysis width
MIN_W = 0.40                     # car box at least 40 % of frame width
MIN_ASPECT = 2.2                 # w/h of box; side-on DTM cars are ~2.4-3.2
EDGE = 0.01                      # box must not touch left/right edge (car complete)
MIN_SCORE = 0.6
GAP = 4.0                        # seconds between kept hits (one per scene)


def vname(path):
    """Output folder name; Windows drops trailing dots and spaces from folder names."""
    return path.stem[:80].rstrip(" .")


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:format=duration", "-of", "csv=p=0:s=,", str(path)],
                         capture_output=True, text=True).stdout.split()
    w, h = map(int, out[0].split(",")[:2])
    return w, h, float(out[-1].strip(","))


def frames(path, step, w, h):
    """Yield (t, rgb small frame) every `step` seconds."""
    sh = int(round(h * SMALL_W / w / 2) * 2)
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps=1/{step},scale={SMALL_W}:{sh}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n, size = 0, SMALL_W * sh * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield n * step, np.frombuffer(buf, np.uint8).reshape(sh, SMALL_W, 3)
        n += 1
    p.wait()


def grab(path, t):
    """Full-resolution BGR frame at t seconds."""
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
           "-f", "image2pipe", "-vcodec", "png", "-"]
    data = subprocess.run(cmd, capture_output=True).stdout
    return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR) if data else None


def sharpness(img, box):
    x0, y0, x1, y1 = box
    g = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(g, cv2.CV_64F).var()) if g.size else 0.0


def scan(model, path, out, step):
    w, h, dur = probe(path)
    sx = w / SMALL_W
    vdir = out / vname(path)
    vdir.mkdir(parents=True, exist_ok=True)
    rows, last = [], -1e9
    for t, small in frames(path, step, w, h):
        with torch.no_grad():
            r = model([torch.from_numpy(small).permute(2, 0, 1).float() / 255])[0]
        keep = [(b.tolist(), float(s)) for b, l, s in zip(r["boxes"], r["labels"], r["scores"])
                if int(l) in (3, 8) and float(s) >= MIN_SCORE]
        if not keep:
            continue
        (x0, y0, x1, y1), s = max(keep, key=lambda k: (k[0][2] - k[0][0]))
        bw, bh = x1 - x0, y1 - y0
        if bw < MIN_W * SMALL_W or bw / max(bh, 1) < MIN_ASPECT:
            continue
        if x0 < EDGE * SMALL_W or x1 > (1 - EDGE) * SMALL_W:
            continue
        if t - last < GAP:
            continue
        last = t
        box = [int(x0 * sx), int(y0 * sx), int(x1 * sx), int(y1 * sx)]
        best = None
        for dt in (-0.4, -0.2, 0.0, 0.2, 0.4):           # sharpest of five nearby frames
            img = grab(path, max(0, t + dt))
            if img is None:
                continue
            sh = sharpness(img, box)
            if best is None or sh > best[0]:
                best = (sh, t + dt, img)
        if best is None:
            continue
        sh, tt, img = best
        stamp = f"{int(tt // 3600):02d}-{int(tt % 3600 // 60):02d}-{int(tt % 60):02d}"
        mx, my = int(bw * sx * 0.06), int(bh * sx * 0.15)
        crop = img[max(0, box[1] - my):box[3] + my, max(0, box[0] - mx):box[2] + mx]
        for name, im in ((f"{stamp}.jpg", img), (f"{stamp}_crop.jpg", crop)):
            # imencode + tofile: cv2.imwrite fails silently on non-ASCII paths (Nürburgring)
            cv2.imencode(".jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 95])[1].tofile(str(vdir / name))
        rows.append({"file": f"{stamp}.jpg", "t": round(tt, 2), "score": round(s, 3),
                     "box_w": round(bw / SMALL_W, 3), "aspect": round(bw / bh, 2),
                     "sharpness": round(sh, 1), "width": w, "height": h})
        print(f"  {stamp} w={bw / SMALL_W:.2f} aspect={bw / bh:.2f} sharp={sh:.0f}", flush=True)
    with open(vdir / "candidates.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["file", "t", "score", "box_w", "aspect", "sharpness", "width", "height"])
        wr.writeheader()
        wr.writerows(rows)
    (vdir / "source.txt").write_text(str(path), encoding="utf-8")
    return len(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("videos", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--step", type=float, default=2.0)
    ap.add_argument("--threads", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    a = ap.parse_args()
    torch.set_num_threads(a.threads)
    model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(weights="DEFAULT").eval()
    for v in a.videos:
        if (a.out / vname(v) / "candidates.csv").exists():
            print("skip (done):", v.name)
            continue
        print("scan:", v.name, flush=True)
        print(" ->", scan(model, v, a.out, a.step), "candidates", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
