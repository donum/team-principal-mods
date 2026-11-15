"""Collect the track announcer (PA) from fan recordings, all years.

The goal is a reference set to build track announcers for every track in an
authentic style: how they sound (horn speakers, echo off the stands) and
what they say. TV re-lives are left out: the commentators talk over the PA.

Sources: every fan recording in `spectator_recordings`, plus the archive
videos named in EXTRA (e.g. the 2014 feature on the Hockenheim announcer).
Each is run through faster-whisper (`small`, CPU, voice detection, language
per segment); speech stretches are cut with 0.5 s either side into
`pilot/track_announcer/` with `index.csv`: year, track, language, text and
two sound measures:
  voice_db  voice band (300-3400 Hz) over the 2 s either side: a PA over
            engines sits low, a fan talking into the phone sits high;
  low_db    energy under 250 Hz vs the voice band: horn speakers have
            almost no bass, a voice near the mic has plenty.
`kind` and `note` come from `announcer_labels.csv` (by hand, after reading and
listening: pa, feature, video, fan, crew, unsure; per stretch or per video);
transcripts are cached in `pilot/track_announcer/transcripts/`.

    python tools/engine_audio/announcer.py [--model small] [--only REGEX]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np

from common import DATA, UPLOAD_YEARS, decode, load_json, source_root, write_wav

OUT = DATA / "pilot" / "track_announcer"
RATE = 16000
LABELS = Path(__file__).with_name("announcer_labels.csv")   # hand labels, committed
# whisper's stock phrases on noise or silence
JUNK = r"\W*(thank you|you|thanks for watching|subscribe.*|copyright.*|untertitel.*|\.\.\.)\W*"
EXTRA = r"streckensprecher|pure sound|grid girls"     # archive titles worth a look
TRACKS = [
    ("Hockenheim", r"hockenheim"), ("Nurburgring", r"n.{1,2}rburgring"), ("Norisring", r"norisring"),
    ("Lausitzring", r"lausitz|eurospeedway"), ("Oschersleben", r"oschersleben"), ("Zandvoort", r"zandvoort"),
    ("Spielberg", r"spielberg|red bull ring"), ("Brands Hatch", r"brands"), ("Moscow", r"moscow|moskau"),
    ("Hungaroring", r"hungaroring|budapest"), ("Misano", r"misano"), ("Donington", r"donington"),
    ("Monza", r"monza"),
]


def sources(root: Path):
    for e in load_json(root / "spectator_recordings" / "done.json", []):
        yield e["id"], e["title"], root / "spectator_recordings" / e["file"] if e.get("file") else None
    for e in load_json(root / "done.json", []):
        if re.search(EXTRA, e["title"], re.I) and not re.search(r"onboard|re-?live", e["title"], re.I):
            yield e["id"], e["title"], root / e["file"]


def meta(vid: str, title: str, path: Path) -> tuple[str, str]:
    """Year from the title, the upload year list, or the archive's year folder."""
    years = re.findall(r"(?<!\d)((?:19|20)\d\d)(?!\d)", title)
    folder = next((p for p in path.parts if re.fullmatch(r"(?:19|20)\d\d", p)), "")
    year = years[0] if years else str(UPLOAD_YEARS.get(vid, folder))
    track = next((n for n, rx in TRACKS if re.search(rx, title, re.I)), "")
    return year, track


def band_db(x: np.ndarray, lo: float, hi: float) -> float:
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / RATE)
    return 10 * np.log10(spec[(f >= lo) & (f < hi)].sum() + 1e-9)


def stretches(segs, gap: float = 1.5):
    """Whisper segments that pass the confidence checks, joined across short gaps."""
    out = []
    for s in segs:
        text = s["text"].strip()
        # A PA over engines often gets a high no-speech probability with the
        # right words, so only junk and very unsure text are dropped.
        if (s["avg_logprob"] < -1.3 or s["compression_ratio"] > 2.4 or len(text) < 6
                or re.fullmatch(JUNK, text, re.I)):
            continue
        if out and s["start"] - out[-1]["end"] < gap and s["language"] == out[-1]["language"]:
            out[-1]["end"] = s["end"]
            out[-1]["text"] += " " + text
            out[-1]["logprob"].append(s["avg_logprob"])
        else:
            out.append({"start": s["start"], "end": s["end"], "text": text,
                        "language": s["language"], "logprob": [s["avg_logprob"]]})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="small")
    ap.add_argument("--only", help="regex on the title")
    ap.add_argument("--threads", type=int, default=8)
    a = ap.parse_args()
    root = source_root()
    (OUT / "transcripts").mkdir(parents=True, exist_ok=True)
    model = None
    labels = {}
    if LABELS.exists():
        with open(LABELS, encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                labels[(r["video_id"], r["start_s"])] = r
    rows = []
    for vid, title, path in sources(root):
        if a.only and not re.search(a.only, title, re.I):
            continue
        if not path or not path.exists():
            print(f"missing: {title}", flush=True)
            continue
        cache = OUT / "transcripts" / f"{vid}.json"
        audio = decode(path, sr=RATE, channels=1)[:, 0]
        if cache.exists():
            segs = json.loads(cache.read_text(encoding="utf-8"))
        else:
            if model is None:
                from faster_whisper import WhisperModel   # user site-packages
                model = WhisperModel(a.model, device="cpu", compute_type="int8", cpu_threads=a.threads)
            it, info = model.transcribe(audio, vad_filter=True, beam_size=1, multilingual=True,
                                     condition_on_previous_text=False)
            segs = [{"start": s.start, "end": s.end, "text": s.text, "avg_logprob": s.avg_logprob,
                     "no_speech_prob": s.no_speech_prob, "compression_ratio": s.compression_ratio,
                     "language": getattr(s, "language", None) or info.language} for s in it]
            cache.write_text(json.dumps(segs, ensure_ascii=False, indent=1), encoding="utf-8")
        year, track = meta(vid, title, path)
        found = stretches(segs)
        for st in found:
            i0, i1 = int(st["start"] * RATE), int(st["end"] * RATE)
            voice = audio[i0:i1]
            if len(voice) < RATE:
                continue
            around = np.concatenate([audio[max(0, i0 - 2 * RATE):i0], audio[i1:i1 + 2 * RATE]])
            v_db = band_db(voice, 300, 3400) - 10 * np.log10(len(voice))
            a_db = band_db(around, 300, 3400) - 10 * np.log10(max(len(around), 1)) if len(around) > RATE // 2 else v_db
            name = f"{year or 'xxxx'}_{re.sub(r'[^A-Za-z]', '', track) or 'unknown'}_{vid}_{st['start']:.0f}s.wav"
            clip = decode(path, max(0, st["start"] - 0.5), st["end"] - st["start"] + 1.0, 44100, 2)
            write_wav(OUT / name, clip, 44100)
            rows.append({"file": name, "quality": round(float(np.exp(np.mean(st["logprob"]))), 3),
                         "year": year, "track": track, "language": st["language"],
                         "start_s": round(st["start"], 1), "end_s": round(st["end"], 1),
                         "voice_db": round(v_db - a_db, 1),
                         "low_db": round(band_db(voice, 40, 250) - band_db(voice, 300, 3400), 1),
                         "kind": "", "note": "", "text": st["text"], "video_id": vid, "title": title})
            # a label for this stretch (its start, within a second), else one for the whole video
            lab = next((r for (v, t), r in labels.items() if v == vid and t and abs(float(t) - st["start"]) < 1.0),
                       labels.get((vid, ""), {}))
            rows[-1].update(kind=lab.get("kind", ""), note=lab.get("note", ""))
        print(f"{year} {track or '?':12} {len(found):3} stretches  {title}", flush=True)
    rows.sort(key=lambda r: (r["year"], r["track"], r["video_id"], r["start_s"]))
    with open(OUT / "index.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["file"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} speech stretches -> {OUT / 'index.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
