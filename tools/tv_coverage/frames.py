"""Still frames from the TV coverage, for reading facts off the picture
(grid side, pit-lane timing graphics, weather, the start).

    python tools/tv_coverage/frames.py --year 2013 --video "Spielberg.*Race" --from 0:10:00 --to 0:20:00 --every 30
    python tools/tv_coverage/frames.py --year 2013 --video "Spielberg.*Race" --at 0:14:35 --at 0:14:40

--every writes one contact sheet (a grid of small frames with their times);
--at writes full-size frames. Output goes to private/tv_coverage/frames/<year>/
(private: the pictures belong to the broadcaster). Find the times with
tools/tv_coverage/search.py.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transcribe import DATA, find_videos  # noqa: E402

FRAMES = DATA / "frames"


def secs(t: str) -> float:
    parts = [float(p) for p in t.split(":")]
    return sum(p * 60 ** i for i, p in enumerate(reversed(parts)))


def stamp(s: float) -> str:
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def grab(video: Path, at: float, out: Path, width: int) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.2f}", "-i", str(video), "-frames:v", "1",
                    "-vf", f"scale={width}:-2,drawtext=text='{stamp(at).replace(':', chr(92) + ':')}':x=8:y=8:"
                    "fontsize=28:fontcolor=yellow:box=1:boxcolor=black@0.6", str(out)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", required=True)
    ap.add_argument("--video", required=True, help="regex on the file name; must match one video")
    ap.add_argument("--at", action="append", default=[], help="h:mm:ss, repeatable")
    ap.add_argument("--from", dest="start", default="0:00:00")
    ap.add_argument("--to", dest="end")
    ap.add_argument("--every", type=float, help="seconds between frames on a contact sheet")
    ap.add_argument("--cols", type=int, default=5)
    a = ap.parse_args()

    videos = [v for v in find_videos(a.year, ".") if re.search(a.video, v.name, re.I) and v.suffix != ".m4a"]
    if len(videos) != 1:
        raise SystemExit(f"{len(videos)} videos match: " + "; ".join(v.name for v in videos))
    video = videos[0]
    out_dir = FRAMES / a.year
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = re.sub(r"\W+", "_", video.stem)[:60]

    for t in a.at:
        out = out_dir / f"{tag}_{t.replace(':', '')}.jpg"
        grab(video, secs(t), out, 1280)
        print(out)
    if a.every:
        import numpy as np
        from PIL import Image
        t0, t1 = secs(a.start), secs(a.end) if a.end else secs(a.start) + 20 * a.every
        times = list(np.arange(t0, t1 + 0.01, a.every))
        tiles = []
        for i, t in enumerate(times):
            tmp = out_dir / f"_tile{i}.jpg"
            grab(video, t, tmp, 384)
            tiles.append(Image.open(tmp).convert("RGB"))
            tmp.unlink()
        w, h = tiles[0].size
        rows = (len(tiles) + a.cols - 1) // a.cols
        sheet = Image.new("RGB", (w * a.cols, h * rows))
        for i, im in enumerate(tiles):
            sheet.paste(im, ((i % a.cols) * w, (i // a.cols) * h))
        out = out_dir / f"{tag}_{a.start.replace(':', '')}_every{a.every:g}.jpg"
        sheet.save(out, quality=85)
        print(out)


if __name__ == "__main__":
    main()
