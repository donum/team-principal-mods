"""Search the TV transcripts (tools/tv_coverage/transcribe.py) by regex.

    python tools/tv_coverage/search.py --year 2013 "drive.?through|pit ?lane"
    python tools/tv_coverage/search.py --year 2013 --video Norisring "safety car" --context 1

Prints video, time (h:mm:ss, ready for frames.py --at) and the line, with
--context segments before and after.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transcribe import TRANSCRIPTS, stamp  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pattern")
    ap.add_argument("--year", default="*")
    ap.add_argument("--video", default="", help="regex on the transcript file name")
    ap.add_argument("--context", type=int, default=0)
    a = ap.parse_args()
    rx = re.compile(a.pattern, re.I)
    sys.stdout.reconfigure(encoding="utf-8")
    hits = 0
    for f in sorted(TRANSCRIPTS.glob(f"{a.year}/*.json")):
        if a.video and not re.search(a.video, f.stem, re.I):
            continue
        segs = json.loads(f.read_text(encoding="utf-8"))["segments"]
        for i, s in enumerate(segs):
            if rx.search(s["text"]):
                hits += 1
                lo, hi = max(0, i - a.context), min(len(segs), i + a.context + 1)
                text = " | ".join(x["text"] for x in segs[lo:hi])
                print(f"{f.stem[:55]:55} {stamp(s['start'])}  {text}")
    print(f"{hits} hits", file=sys.stderr)


if __name__ == "__main__":
    main()
