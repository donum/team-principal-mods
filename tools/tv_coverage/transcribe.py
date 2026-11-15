"""Transcribe downloaded TV coverage (race and qualifying re-lives, highlights)
into timestamped text, so research can search what the commentators said.

Works for any year in the video archive (default C:\\Users\\dan\\Videos\\yt\\DTM,
or "tv_coverage_source" / "engine_audio_source" in local.json): pick videos
with --year and a title regex. Each video becomes

    private/tv_coverage/transcripts/<year>/<stem>.json   segments with start/end seconds
    private/tv_coverage/transcripts/<year>/<stem>.txt    one "[h:mm:ss] text" line per segment

The transcripts stay private (the commentary belongs to the broadcaster);
only facts read from them go into the repo, with the video and time as source.

Driver and venue names from seasons/<series>-<year>/research/entries.csv and
calendar.csv go into Whisper's prompt so the names come out right.

Needs faster-whisper (python -m pip install --user faster-whisper) and ffmpeg.
Run with plain `python` (not -I), since faster-whisper is in the user site.

    python tools/tv_coverage/transcribe.py --year 2013 --match "re-?live" [--model medium] [--list]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "private" / "tv_coverage"
TRANSCRIPTS = DATA / "transcripts"
EXT_RANK = {".mkv": 0, ".mp4": 1, ".webm": 2, ".m4a": 3, ".opus": 4}   # same stem: take the first
RATE = 16000


def source_root() -> Path:
    local = REPO / "local.json"
    cfg = json.loads(local.read_text(encoding="utf-8")) if local.exists() else {}
    return Path(cfg.get("tv_coverage_source") or cfg.get("engine_audio_source") or r"C:\Users\dan\Videos\yt\DTM")


def find_videos(year: str, match: str, series: str = "") -> list[Path]:
    """One file per video stem under <source>/<year>/, best container first."""
    rx = re.compile(match, re.I)
    best: dict[str, Path] = {}
    for p in sorted((source_root() / year).rglob("*")):
        if p.suffix.lower() not in EXT_RANK or ".temp" in p.name or ".part" in p.name:
            continue
        if not rx.search(p.stem) or (series and not re.search(series, str(p), re.I)):
            continue
        key = str(p.with_suffix(""))
        if key not in best or EXT_RANK[p.suffix.lower()] < EXT_RANK[best[key].suffix.lower()]:
            best[key] = p
    return sorted(best.values())


def out_stem(year: str, video: Path) -> Path:
    folder = re.sub(r"[^\w\-]+", "_", video.parent.name).strip("_")
    return TRANSCRIPTS / year / f"{folder}__{video.stem}"


def prompt_words(year: str, series: str) -> str:
    """Names from the season research, so Whisper spells them right."""
    names: list[str] = []
    for season in sorted(REPO.glob(f"seasons/{series or '*'}-{year}")):
        for fname, col in (("entries.csv", "driver"), ("calendar.csv", "venue")):
            f = season / "research" / fname
            if f.exists():
                with f.open(encoding="utf-8") as fh:
                    names += [r[col] for r in csv.DictReader(fh) if r.get(col)]
    names = list(dict.fromkeys(names))
    return ("DTM race commentary. " + ", ".join(names) + ". Pit stop, option tyre, DRS, safety car.")[:800]


def decode(video: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", str(RATE),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def stamp(s: float) -> str:
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", required=True)
    ap.add_argument("--match", default="re-?live", help="regex on the file name")
    ap.add_argument("--series", default="dtm", help="season folder prefix for the name prompt")
    ap.add_argument("--model", default="medium")
    ap.add_argument("--language", default=None, help="en, de... (default: detect)")
    ap.add_argument("--threads", type=int, default=16)
    ap.add_argument("--list", action="store_true", help="only list what would be transcribed")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    videos = find_videos(a.year, a.match)
    todo = [v for v in videos if a.force or not out_stem(a.year, v).with_suffix(".json").exists()]
    print(f"{len(videos)} videos match, {len(todo)} to do")
    if a.list:
        for v in videos:
            print(("  todo " if v in todo else "  done ") + str(v.relative_to(source_root())))
        return

    from faster_whisper import WhisperModel   # user site, see docstring
    model = WhisperModel(a.model, device="cpu", compute_type="int8", cpu_threads=a.threads)
    prompt = prompt_words(a.year, a.series)
    for i, v in enumerate(todo, 1):
        t0 = time.time()
        audio = decode(v)
        language = a.language
        if not language:
            # Whisper detects the language from the first 30 s, which can be music or a
            # German stadium announcer (it then wrote English commentary out in German:
            # Spielberg 2013). Detect it from the middle of the video instead.
            mid = len(audio) // 2
            _, probe = model.transcribe(audio[mid:mid + 30 * RATE], vad_filter=True, beam_size=1)
            language = probe.language
        segs, info = model.transcribe(audio, language=language, vad_filter=True, beam_size=1,
                                      initial_prompt=prompt, condition_on_previous_text=False)
        rows = [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()} for s in segs]
        out = out_stem(a.year, v)
        out.parent.mkdir(parents=True, exist_ok=True)
        meta = {"video": str(v.relative_to(source_root())), "duration_s": round(len(audio) / RATE, 1),
                "model": a.model, "language": info.language, "segments": rows}
        out.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        out.with_suffix(".txt").write_text("".join(f"[{stamp(r['start'])}] {r['text']}\n" for r in rows),
                                           encoding="utf-8")
        print(f"[{i}/{len(todo)}] {v.name}: {meta['duration_s'] / 60:.0f} min in {(time.time() - t0) / 60:.0f} min "
              f"({info.language})", flush=True)


if __name__ == "__main__":
    sys.exit(main())
