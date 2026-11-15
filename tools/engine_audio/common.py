"""Shared paths and helpers for the engine-audio pipeline.

Pipeline (each stage is a re-runnable CLI script, see README.md):
    catalog.py -> extract.py -> segment.py -> library.py -> package.py
                                    +-> events.py -> separate.py -> review.py -+
                                    +-> starts.py, start_preview.py, ambience.py (spectator) ----+

All audio lives under private/engine_audio (gitignored). Never commit it.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
import sys
import unicodedata
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
# The sound set this run makes: the "audio" section of an era base
# (bases/<id>/base.json) or of a season (seasons/<id>/season.json), merged
# over the layers below it (tools/layers.py). Every season on that layer
# plays it; a season's own set sits on top of its era's and fills only its
# "slots". ENGINE_AUDIO_BASE picks the layer (default the era-4 base); a
# new car generation gets its own ENGINE_AUDIO_DATA, since one library
# holds one generation, while a season set of the same generation shares
# the era's library.
sys.path.insert(0, str(REPO / "tools"))
import layers as _layers  # noqa: E402

BASE_ID = os.environ.get("ENGINE_AUDIO_BASE", "dtm-era4")
_SET_DIR = _layers.source_dir(BASE_ID)
if not (_layers.load_json(_layers.manifest_file(_SET_DIR)).get("audio") or {}).get("overlay"):
    raise SystemExit(f"{BASE_ID} has no sound set of its own (an \"audio\" section with an \"overlay\" id)")
AUDIO = next(a for a in _layers.audio_sets(_SET_DIR) if a["layer"] == _SET_DIR.name)
OVERLAY_ID = AUDIO["overlay"]
# The slot groups this set makes; the sets below it fill the rest.
SLOT_GROUPS = ("passby", "tv", "start", "pit", "cars", "crowd")
SLOTS = tuple(AUDIO.get("slots") or SLOT_GROUPS)
KEY_PREFIX = AUDIO.get("key_prefix", OVERLAY_ID.replace("-", ""))
RESEARCH = REPO / "seasons" / AUDIO["research_season"] / "research"   # who drove which make in the videos
# ENGINE_AUDIO_DATA redirects everything (tests, or a bigger disk)
DATA = Path(os.environ.get("ENGINE_AUDIO_DATA", REPO / "private" / "engine_audio"))
DB_PATH = DATA / "library.sqlite"
AUDIO_DIR = DATA / "audio"          # extract.py: lossless audio tracks
FEATURE_DIR = DATA / "features"     # segment.py: per-video analysis cache
LIBRARY_DIR = DATA / "library"      # library.py: ranked clips + reports
# What this set builds from the library (ambience/, starts/, pits/ loops and
# previews). The era-4 set came first and keeps library/ itself; every
# other set of the library gets library/sets/<overlay id>/.
SET_LIBRARY_DIR = LIBRARY_DIR if OVERLAY_ID == "dtm-era4" else LIBRARY_DIR / "sets" / OVERLAY_ID
PACK_DIR = DATA / "pack"            # package.py: game overlays, one per era base (OVERLAY_ID)
SEPARATED_DIR = DATA / "separated"  # separate.py: event windows, original and commentary removed
CURATION = REPO / "tools" / "engine_audio" / "curation.csv"   # review.py decisions (metadata only)
DEFAULT_SOURCE = Path(r"C:\Users\dan\Videos\yt\DTM")

# Video types worth analysing for engine sound (features and animations are not).
ENGINE_TYPES = ("onboard", "onboard_bestof", "taxi", "trackview", "broadcast", "highlights", "spectator")
MAKES = ("Audi", "BMW", "Mercedes")

# Era: only cars of the 2013 generation (Audi RS 5, BMW M3, Mercedes
# C-Coupé, raced 2012-2013) may be heard (user, 2026-11-07). 2011 and earlier
# cars and the 2014-2018 V8s sound different and are out, even in the bed.
# A video's year is the year in its title; titles without one take the
# upload year from the file's metadata (listed here by hand).
# The years are the base's "recording_years".
ERA = tuple(AUDIO["recording_years"])
UPLOAD_YEARS = {
    "EMSlNAM8zC0": 2013,   # "DTM Sound 1", Don Blech: 2013 pit lane, 2013 liveries
    "fk9f2Qt5x20": 2013,   # "DTM Finale at Hockenheim - Grid and Start"
    "Ks5j_yh9CN8": 2017,   # "für die ohren"
    "JDtk4MRd1d0": 2018,   # "DTM Sound Pure V8 - Downshifts & Starts" (Lausitzring 2018)
    "plmbOpRMwHs": 2017,   # "The Sounds of DTM!"
    "4pue6jM-VQY": 2010,   # "Brands Hatch Round of DTM - Start"
    "WR62Z_5KJM8": 2018,   # Misano night qualifying: the first DTM night race was Misano 2018
    "maJ-qIGkz_o": 2018,   # "the first ever DTM Race Weekend by night": Misano 2018
}
# In era by year but kept out anyway (reason shown in the mod browser).
ERA_EXCLUDE = {
    "YJSGHrT5x-s": "BMW promo film that mixes in the 1987 M3 E30",
    "-Kq_G6F1CYI": "same footage as ywftpjRPJPE (BigB.TV, Nürburgring 2013)",
}


def video_years(title: str) -> list[int]:
    years = [int(y) for y in re.findall(r"\b(20[0-2]\d)\b", title or "")]
    years += [2000 + int(y) for y in re.findall(r"\b\d{1,2}\.\d{1,2}\.(\d{2})\b", title or "")]
    return years


def era_reason(vid: str, title: str, video_type: str = "spectator") -> str | None:
    """None if the video's cars are of the era, else why not. Only fan
    (spectator) uploads need checking: the onboard, TV and archive
    playlists are the 2013 season itself."""
    if vid in ERA_EXCLUDE:
        return ERA_EXCLUDE[vid]
    if video_type != "spectator":
        return None
    years = video_years(title) or ([UPLOAD_YEARS[vid]] if vid in UPLOAD_YEARS else [])
    if not years:
        return "year unknown"
    bad = [y for y in years if not ERA[0] <= y <= ERA[1]]
    return f"{bad[0]} cars" if bad else None


def load_json(path: Path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def dump_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def source_root(arg: Path | None = None) -> Path:
    local = load_json(REPO / "local.json", {})
    return Path(arg or local.get("engine_audio_source", DEFAULT_SOURCE))


def game_path() -> Path:
    local = load_json(REPO / "local.json", {})
    return Path(local["game_path"])


def connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise SystemExit(f"no catalog at {DB_PATH}; run tools/engine_audio/catalog.py first")
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def slug(s: str | None, empty: str = "_none") -> str:
    if not s:
        return empty
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_") or empty


def run(cmd: list[str]) -> None:
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode:
        raise RuntimeError(f"{cmd[0]} failed: {res.stderr.strip()[-400:]}")


def decode(path: Path, start: float = 0.0, duration: float | None = None,
           sr: int = 44100, channels: int = 2) -> np.ndarray:
    """Decode a slice of the first audio stream to float32, shape (frames, channels)."""
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}"]
    if duration is not None:
        cmd += ["-t", f"{duration:.3f}"]
    cmd += ["-i", str(path), "-map", "0:a:0", "-ac", str(channels), "-ar", str(sr),
            "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, channels).copy()


def stream_decode(path: Path, sr: int, channels: int, block_s: float = 60.0):
    """Yield float32 blocks (frames, channels) of a whole file without loading it."""
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-ac", str(channels),
           "-ar", str(sr), "-f", "f32le", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    nbytes = int(block_s * sr) * channels * 4
    try:
        while True:
            buf = proc.stdout.read(nbytes)
            if not buf:
                break
            usable = len(buf) - len(buf) % (channels * 4)
            yield np.frombuffer(buf[:usable], dtype=np.float32).reshape(-1, channels)
    finally:
        proc.stdout.close()
        proc.wait()


def write_wav(path: Path, audio: np.ndarray, sr: int = 44100, codec: str = "pcm_s16le") -> None:
    """Write float audio (frames, channels) through ffmpeg (wav, ogg or flac by suffix)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    audio = np.clip(np.asarray(audio, dtype=np.float32), -1.0, 1.0)
    ch = 1 if audio.ndim == 1 else audio.shape[1]
    tmp = path.with_name(path.stem + ".tmp" + path.suffix)
    enc = {".ogg": ["-c:a", "libvorbis", "-q:a", "6"],
           ".flac": ["-c:a", "flac", "-sample_fmt", "s16"]}.get(path.suffix, ["-c:a", codec])
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", str(ch),
           "-i", "-", *enc, str(tmp)]
    subprocess.run(cmd, input=audio.tobytes(), check=True, capture_output=True)
    tmp.replace(path)


def audio_rows(db: sqlite3.Connection, include_legacy: bool = False, types=ENGINE_TYPES):
    statuses = ("done", "legacy") if include_legacy else ("done",)
    q = (f"SELECT * FROM videos WHERE status IN ({','.join('?' * len(statuses))}) "
         f"AND video_type IN ({','.join('?' * len(types))}) AND file IS NOT NULL "
         f"AND audio_codec IS NOT NULL ORDER BY folder, idx")
    return db.execute(q, (*statuses, *types)).fetchall()
