"""Shared paths and helpers for the engine-audio pipeline.

Pipeline (each stage is a re-runnable CLI script, see README.md):
    catalog.py -> extract.py -> segment.py -> library.py -> package.py
                                    +-> events.py -> separate.py -> review.py -+

All audio lives under private/engine_audio (gitignored). Never commit it.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
import unicodedata
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
# ENGINE_AUDIO_DATA redirects everything (tests, or a bigger disk)
DATA = Path(os.environ.get("ENGINE_AUDIO_DATA", REPO / "private" / "engine_audio"))
DB_PATH = DATA / "library.sqlite"
AUDIO_DIR = DATA / "audio"          # extract.py: lossless audio tracks
FEATURE_DIR = DATA / "features"     # segment.py: per-video analysis cache
LIBRARY_DIR = DATA / "library"      # library.py: ranked clips + reports
PACK_DIR = DATA / "pack"            # package.py: game overlays, one per pack folder
SEPARATED_DIR = DATA / "separated"  # separate.py: event windows, original and commentary removed
CURATION = REPO / "tools" / "engine_audio" / "curation.csv"   # review.py decisions (metadata only)
DEFAULT_SOURCE = Path(r"C:\Users\dan\Videos\yt\DTM")

# Video types worth analysing for engine sound (features and animations are not).
ENGINE_TYPES = ("onboard", "onboard_bestof", "taxi", "trackview", "broadcast", "highlights", "spectator")
MAKES = ("Audi", "BMW", "Mercedes")


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
