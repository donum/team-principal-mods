"""Listening candidates from a season's archive videos (TV, reviews, fan clips).

For a car generation with no onboard library (BTCC 1991): every source video
in the season's audio "sources" is scanned for stretches without speech,
and the best of them are cut for listening, by kind:

    passby  a single loud peak (8+ dB over the 2.5 s either side), with pan
            sweep and pitch drop as bonus; 5 s, peak at 2.2 s (game: 4 s)
    start   the level steps up 8+ dB for good after engine noise (a getaway);
            speech allowed, its share shown
    bed     8-30 s of engines with a level swing (cars coming and going)
    fireup  a jump of 15+ dB within 0.3 s out of a quiet stretch
    quiet   6-20 s well under the video's median level (crowd, paddock, PA)

Speech: Silero VAD (bundled with faster-whisper) on 16 kHz mono, padded by
0.4 s. Duplicate uploads are skipped by file name and length, duplicate cuts
by a coarse spectrogram fingerprint. Analysis is cached per video.

Writes private/engine_audio/pilot/<season tag>/<kind>/*.wav with a
candidates.json (file -> note) per folder, and a frame per pass-by in
_frames/ for telling the makes apart. The mod browser lists them on the
season's page (audio "candidate_dirs").

    python tools/engine_audio/archive_candidates.py --season btcc-1991
    python tools/engine_audio/archive_candidates.py --season btcc-1991 --list
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
import layers  # noqa: E402

DATA = REPO / "private" / "engine_audio"
VIDEO_EXT = {".mkv", ".mp4", ".webm"}
SR = 22050            # analysis rate
HOP = 0.1             # s per analysis frame
NFFT = 2048
VERSION = 2           # bump when the analysis changes

CAPS = {"passby": 60, "bed": 30, "start": 20, "fireup": 30, "quiet": 20}
LENGTH = {"passby": 5.0, "fireup": 6.0}


# ------------------------------------------------------------------ sources

def season_audio(season: str) -> dict:
    folder = layers.source_dir(season)
    sets = layers.audio_sets(folder)
    if not sets or sets[-1]["layer"] != folder.name:
        raise SystemExit(f"{season} has no sound set of its own")
    return sets[-1]


def sources(audio: dict) -> list[dict]:
    """[{path, kind, note}] from audio["sources"]: {glob, kind, note, skip}."""
    local = json.loads((REPO / "local.json").read_text(encoding="utf-8")) if (REPO / "local.json").exists() else {}
    root = Path(local.get("archive_video_root", r"C:\Users\dan\Videos\yt"))
    out, seen = [], {}
    for src in audio.get("sources", []):
        skip = re.compile(src["skip"], re.I) if src.get("skip") else None
        for p in sorted(root.glob(src["glob"])):
            if p.suffix.lower() not in VIDEO_EXT or ".part" in p.name or ".temp" in p.name:
                continue
            if skip and skip.search(p.name):
                continue
            key = re.sub(r"\W+", "", p.stem.lower())
            if key in seen:          # same upload in two playlists
                continue
            seen[key] = p
            notes = src.get("notes", {})
            note = next((n for pat, n in notes.items() if re.search(pat, p.name, re.I)), src.get("note", ""))
            out.append({"path": p, "kind": src["kind"], "note": note})
    return out


def short_name(p: Path) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", p.stem).strip("_")
    return s[:48]


LABELS = Path(__file__).with_name("archive_labels.csv")


def label_for(path: Path, t: float) -> dict:
    """Hand label (archive_labels.csv): the source's name starts with
    "source", within 1.5 s of at_s. car names the make for pass-bys,
    verdict "drop" keeps the cut out."""
    import csv
    if not LABELS.exists():
        return {}
    with open(LABELS, encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if path.stem.startswith(r["source"]) and abs(float(r["at_s"]) - t) <= 1.5:
                return r
    return {}


def labelled(note: str, lab: dict) -> str:
    bits = [f"car: {lab['car']}" if lab.get("car") else "", lab.get("note", "")]
    head = " · ".join(b for b in bits if b)
    return f"{head} · {note}" if head else note


# ------------------------------------------------------------------ analysis

def decode(path: Path, sr: int, channels: int, start: float = 0.0, dur: float | None = None) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}"]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-i", str(path), "-map", "0:a:0", "-ac", str(channels), "-ar", str(sr), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, channels).copy()


def write_wav(path: Path, x: np.ndarray, sr: int = 44100) -> None:
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(sr), "-ac", str(x.shape[1]), "-i", "-", str(path)]
    subprocess.run(cmd, input=pcm.tobytes(), check=True, capture_output=True)


def speech_mask(path: Path, n: int) -> np.ndarray:
    from faster_whisper.vad import VadOptions, get_speech_timestamps
    mono = decode(path, 16000, 1)[:, 0]
    opts = VadOptions(threshold=0.4, min_speech_duration_ms=200, min_silence_duration_ms=300, speech_pad_ms=400)
    mask = np.zeros(n, bool)
    chunk = 16000 * 600
    for off in range(0, len(mono), chunk):
        for ts in get_speech_timestamps(mono[off:off + chunk], opts):
            a = int((off + ts["start"]) / 16000 / HOP)
            b = int(np.ceil((off + ts["end"]) / 16000 / HOP))
            mask[max(a, 0):min(b, n)] = True
    return mask


def analyse(path: Path, cache: Path) -> dict:
    tag = hashlib.sha1(f"{path}|{path.stat().st_size}|{VERSION}".encode()).hexdigest()[:12]
    f = cache / f"{tag}.npz"
    if f.exists():
        return dict(np.load(f))
    x = decode(path, SR, 2)
    hop = int(SR * HOP)
    n = len(x) // hop
    mono = x[: n * hop].mean(1)
    frames = mono.reshape(n, hop)
    rms = 20 * np.log10(np.sqrt((frames ** 2).mean(1)) + 1e-6)
    lr = x[: n * hop].reshape(n, hop, 2)
    el, er = (lr[..., 0] ** 2).mean(1), (lr[..., 1] ** 2).mean(1)
    pan = 10 * np.log10((er + 1e-9) / (el + 1e-9))
    win = np.hanning(NFFT).astype(np.float32)
    freqs = np.fft.rfftfreq(NFFT, 1 / SR)
    cen, hf, flat = np.zeros(n), np.zeros(n), np.zeros(n)
    band = (freqs > 150) & (freqs < 4000)
    for i in range(n):
        seg = mono[i * hop: i * hop + NFFT]
        if len(seg) < NFFT:
            seg = np.pad(seg, (0, NFFT - len(seg)))
        s = np.abs(np.fft.rfft(seg * win)) ** 2 + 1e-12
        tot = s.sum()
        cen[i] = (s * freqs).sum() / tot
        hf[i] = s[freqs > 5000].sum() / tot
        b = s[band]
        flat[i] = np.exp(np.log(b).mean()) / b.mean()
    speech = speech_mask(path, n)
    res = {"rms": rms.astype(np.float32), "pan": pan.astype(np.float32), "cen": cen.astype(np.float32),
           "hf": hf.astype(np.float32), "flat": flat.astype(np.float32), "speech": speech}
    cache.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(f, **res)
    return res


def smooth(v: np.ndarray, k: int) -> np.ndarray:
    return np.convolve(v, np.ones(k) / k, mode="same") if k > 1 else v


def runs(mask: np.ndarray) -> list[tuple[int, int]]:
    d = np.diff(np.concatenate([[0], mask.astype(int), [0]]))
    return list(zip(np.flatnonzero(d == 1), np.flatnonzero(d == -1)))


# ------------------------------------------------------------------ finders

def find(a: dict, need_clean: bool = True) -> list[dict]:
    rms, speech = a["rms"], a["speech"]
    n = len(rms)
    if n < 50:
        return []
    r3 = smooth(rms, 3)
    med = float(np.median(rms[rms > -80])) if (rms > -80).any() else -60.0
    silent = rms < -70          # digital silence: black gaps, fades
    free = ~speech & ~silent
    out = []

    def clean(i0, i1):
        return free[max(i0, 0):min(i1, n)].all()

    # pass-bys
    w = 22
    for i in range(w, n - w):
        if r3[i] < r3[i - 3:i + 4].max() or r3[i] < med:
            continue
        before, after = r3[i - w:i - 10].min(), r3[i + 10:i + w].min()
        prom = min(r3[i] - before, r3[i] - after)
        if prom < (6 if need_clean else 10) or (need_clean and not clean(i - 25, i + 25)):
            continue
        p0, p1 = np.median(a["pan"][i - 15:i - 3]), np.median(a["pan"][i + 3:i + 15])
        sweep = abs(p1 - p0) if np.sign(p0) != np.sign(p1) else 0.0
        drop = (np.median(a["cen"][i - 12:i - 2]) - np.median(a["cen"][i + 2:i + 12])) / 1000
        score = prom + min(sweep, 6) + max(min(drop, 1.5), 0) * 3 - a["hf"][i] * 20
        out.append({"kind": "passby", "t": i * HOP, "start": i * HOP - 2.2, "dur": LENGTH["passby"],
                    "score": round(float(score), 2),
                    "note": f"peak {prom:.0f} dB over the sides, pan sweep {sweep:.0f} dB, pitch drop {drop * 1000:.0f} Hz"})
    if not need_clean:
        return out
    # getaways: level steps up for good after engines
    k = 60
    r10 = smooth(rms, 10)
    for i in range(k, n - k, 5):
        pre, post = r10[i - k:i - 5].mean(), r10[i + 5:i + k].mean()
        if post - pre < 8 or pre < med - 12:
            continue
        sp = float(speech[i - 50:i + 150].mean()) if i + 150 < n else 1.0
        if sp > 0.4 or silent[i - k:i + k].mean() > 0.05:
            continue
        out.append({"kind": "start", "t": i * HOP, "start": i * HOP - 6, "dur": 20.0,
                    "score": round(float(post - pre - 10 * sp), 2),
                    "note": f"steps up {post - pre:.0f} dB, speech {sp * 100:.0f} %"})
    # beds and quiet stretches
    for a0, a1 in runs(free):
        if a1 - a0 < 60:
            continue
        seg = rms[a0:a1]
        swing = np.percentile(seg, 95) - np.percentile(seg, 10)
        lvl = np.median(seg)
        if lvl > med - 6 and a1 - a0 >= 80:
            # long runs give several 20 s windows (fan clips are one long run)
            L = min(a1 - a0, 200)
            for b0 in range(a0, a1 - L + 1, 100):
                ws = rms[b0:b0 + L]
                wsw = np.percentile(ws, 95) - np.percentile(ws, 10)
                if wsw < 7:
                    continue
                dur = L * HOP
                out.append({"kind": "bed", "t": b0 * HOP, "start": b0 * HOP, "dur": dur,
                            "score": round(float(wsw + dur / 3 - np.mean(a["hf"][b0:b0 + L]) * 30), 2),
                            "note": f"{dur:.0f} s, level swing {wsw:.0f} dB"})
        elif lvl < med - 10:
            dur = min((a1 - a0) * HOP, 20.0)
            out.append({"kind": "quiet", "t": a0 * HOP, "start": a0 * HOP, "dur": dur,
                        "score": round(float(dur + (med - lvl) / 2), 2),
                        "note": f"{dur:.0f} s, {med - lvl:.0f} dB under the video's median"})
        # fire-ups inside the clean run
        for i in range(a0 + 20, a1 - 20):
            jump = rms[i:i + 3].max() - rms[i - 20:i - 1].max()
            if jump >= 15 and rms[i:i + 3].max() > med - 10 and rms[i - 20:i - 1].min() > -70 and jump < 45:
                out.append({"kind": "fireup", "t": i * HOP, "start": i * HOP - 1.0, "dur": LENGTH["fireup"],
                            "score": round(float(jump), 2), "note": f"jumps {jump:.0f} dB out of quiet"})
    return out


def thin(cands: list[dict], gap: float) -> list[dict]:
    """Best first, none closer than gap seconds to a better one of its kind."""
    kept = []
    for c in sorted(cands, key=lambda c: -c["score"]):
        if all(abs(c["t"] - k["t"]) >= gap for k in kept if k["kind"] == c["kind"]):
            kept.append(c)
    return kept


def fingerprint(x: np.ndarray, sr: int) -> np.ndarray:
    mono = x.mean(1)
    hop = len(mono) // 40 or 1
    fr = mono[: hop * 40].reshape(40, hop)
    spec = np.abs(np.fft.rfft(fr, axis=1))
    edges = np.geomspace(1, spec.shape[1], 25).astype(int)
    bands = np.stack([spec[:, a:b + 1].mean(1) for a, b in zip(edges[:-1], edges[1:])], 1)
    v = np.log(bands + 1e-9).ravel()
    v -= v.mean()
    return v / (np.linalg.norm(v) + 1e-9)


# ------------------------------------------------------------------ commentary removal

START_WORDS = re.compile(r"\b(lights?|green|away they go|they'?re away|they'?re off|the start|rolling start|grid)\b", re.I)
TRANSCRIPTS = REPO / "private" / "tv_coverage" / "transcripts"
MODELS = DATA / "models"


def transcript(path: Path) -> list[dict]:
    """Whisper segments of a video (tools/tv_coverage), matched by file stem."""
    stem = re.sub(r"\W+", "", path.stem.lower())
    for f in TRANSCRIPTS.rglob("*.json"):
        if re.sub(r"\W+", "", f.stem.split("__", 1)[-1].lower()) == stem:
            return json.loads(f.read_text(encoding="utf-8")).get("segments", [])
    return []


def separate(windows: list[tuple[Path, Path]], work: Path, model: str) -> None:
    """Commentary out: [(input wav, output wav)] through audio-separator."""
    from audio_separator.separator import Separator
    sep = Separator(model_file_dir=str(MODELS), output_dir=str(work), output_format="WAV")
    sep.load_model(model_filename=model)
    for src, dst in windows:
        if dst.exists():
            continue
        outs = [work / Path(o).name for o in sep.separate(str(src))]
        rest = [o for o in outs if "(vocals)" not in o.name.lower()]
        if not rest:
            raise RuntimeError(f"no non-vocal stem in {outs}")
        rest[0].replace(dst)
        for o in outs:
            o.unlink(missing_ok=True)


def tv_pass(srcs: list[dict], out_root: Path, cache: Path, n_passby: int, n_start: int, model: str) -> None:
    work = DATA / "separated_archive"
    work.mkdir(parents=True, exist_ok=True)
    jobs = []
    for s in srcs:
        if s["kind"] == "fan":
            continue
        a = analyse(s["path"], cache)
        for c in thin(find(a, need_clean=False), 8.0):
            jobs.append({**c, "src": s, "speech": float(a["speech"][int(c["t"] / HOP) - 15:int(c["t"] / HOP) + 15].mean())})
        for seg in transcript(s["path"]):
            if START_WORDS.search(seg["text"]):
                t = seg["start"]
                i = int(t / HOP)
                r = a["rms"]
                step = r[i:i + 150].mean() - r[max(i - 100, 0):i].mean() if i + 150 < len(r) else 0
                jobs.append({"kind": "start", "t": t, "start": t - 8, "dur": 30.0, "score": round(float(step), 2),
                             "src": s, "speech": 1.0,
                             "note": f"“{seg['text'].strip()[:80]}”, level after {step:+.0f} dB"})
    picked = {}
    for kind, cap, pre, dur, keep_pre, keep in (("passby", n_passby, 4.0, 9.0, 2.2, 5.0), ("start", n_start, 8.0, 30.0, 8.0, 30.0)):
        cands = sorted((j for j in jobs if j["kind"] == kind), key=lambda j: -(j["score"] - (5 * j["speech"] if kind == "passby" else 0)))
        sel, prints = [], []
        for j in cands:
            if len(sel) >= cap:
                break
            x = decode(j["src"]["path"], 44100, 2, max(j["t"] - pre, 0), dur)
            if len(x) < 44100 * 3:
                continue
            fp = fingerprint(x, 44100)
            if any(float(fp @ q) > 0.95 for q in prints):
                continue
            prints.append(fp)
            tag = hashlib.sha1(f"{j['src']['path']}|{j['t']:.1f}|{kind}".encode()).hexdigest()[:10]
            raw, sepd = work / f"{tag}_mix.wav", work / f"{tag}_{Path(model).stem}.wav"
            if not raw.exists():
                write_wav(raw, x)
            sel.append({**j, "raw": raw, "sep": sepd, "pre": pre, "keep_pre": keep_pre, "keep": keep})
        picked[kind] = sel
    separate([(j["raw"], j["sep"]) for sel in picked.values() for j in sel], work, model)
    for kind, sel in picked.items():
        d = out_root / f"{kind}_tv"
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*.wav"):
            old.unlink()
        meta = []
        for n, j in enumerate(sel, 1):
            lab = label_for(j["src"]["path"], j["t"])
            if not j["sep"].exists() or lab.get("verdict") == "drop":
                continue
            y = decode(j["sep"], 44100, 2)
            a0 = int((j["pre"] - j["keep_pre"]) * 44100)
            y = y[a0:a0 + int(j["keep"] * 44100)]
            y = y / (np.abs(y).max() + 1e-9) * 0.9
            p = j["src"]["path"]
            name = f"{n:02d}_{short_name(p)}_{int(j['t'] // 60)}m{int(j['t'] % 60):02d}s.wav"
            write_wav(d / name, y)
            frame = ""
            if kind == "passby":
                (out_root / "_frames").mkdir(exist_ok=True)
                frame = f"_frames/tv_{Path(name).stem}.jpg"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{j['t']:.2f}", "-i", str(p), "-frames:v", "1",
                                "-vf", "scale=480:-2", str(out_root / frame)], capture_output=True)
            mm, ss = divmod(j["t"], 60)
            meta.append({"file": name, "score": j["score"], "source": str(p), "at_s": round(j["t"], 1), "frame": frame,
                         "mix": str(j["raw"]), "car": lab.get("car", ""),
                         "note": labelled("", lab) + f"commentary removed ({Path(model).stem}) · score {j['score']} · {j['note']} · "
                                 f"speech {j['speech'] * 100:.0f} % · {j['src']['kind']} · {p.stem} @ {int(mm)}:{ss:04.1f}"})
        (d / "candidates.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"{kind}_tv: {len(meta)} clips in {d}")


# ------------------------------------------------------------------ main

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", required=True)
    ap.add_argument("--list", action="store_true", help="list the sources and stop")
    ap.add_argument("--tv", action="store_true", help="only the commentary-removal pass on TV pass-bys and starts")
    ap.add_argument("--tv-passbys", type=int, default=30)
    ap.add_argument("--tv-starts", type=int, default=16)
    ap.add_argument("--model", default="vocals_mel_band_roformer.ckpt")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    audio = season_audio(args.season)
    tag = audio.get("candidate_dirs", [f"pilot/{audio['overlay']}"])[0]
    out_root = DATA / tag
    cache = DATA / "features_archive"
    srcs = sources(audio)
    if args.list:
        for s in srcs:
            print(f"{s['kind']:10} {s['path'].relative_to(s['path'].parents[2])}  {s['note']}")
        print(len(srcs), "videos")
        return
    if args.tv:
        tv_pass(srcs, out_root, cache, args.tv_passbys, args.tv_starts, args.model)
        return
    weight = {"fan": 1.0, "tv": 0.9, "review": 0.75}
    allc = []
    for s in srcs:
        print("analysing", s["path"].name.encode("ascii", "replace").decode(), flush=True)
        a = analyse(s["path"], cache)
        found = thin(find(a), 8.0)
        for c in found:
            c.update(src=s, score=round(c["score"] * weight.get(s["kind"], 0.8), 2))
        allc += found
        print(f"  {len(a['rms']) * HOP / 60:.1f} min, speech {a['speech'].mean() * 100:.0f} %, "
              f"{len(found)} candidates", flush=True)
    for kind, cap in CAPS.items():
        d = out_root / kind
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*.wav"):
            old.unlink()
        meta, prints = [], []
        for c in sorted((c for c in allc if c["kind"] == kind), key=lambda c: -c["score"]):
            if len(meta) >= cap:
                break
            p = c["src"]["path"]
            lab = label_for(p, c["t"])
            if lab.get("verdict") == "drop":
                continue
            x = decode(p, 44100, 2, max(c["start"], 0), c["dur"])
            if len(x) < 44100:
                continue
            fp = fingerprint(x, 44100)
            if any(float(fp @ q) > 0.95 for q in prints):
                continue
            prints.append(fp)
            x = x / (np.abs(x).max() + 1e-9) * 0.9
            name = f"{len(meta) + 1:02d}_{short_name(p)}_{int(c['t'] // 60)}m{int(c['t'] % 60):02d}s.wav"
            write_wav(d / name, x)
            frame = ""
            if kind == "passby":
                fdir = out_root / "_frames"
                fdir.mkdir(exist_ok=True)
                frame = f"_frames/{Path(name).stem}.jpg"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['t']:.2f}", "-i", str(p), "-frames:v", "1",
                                "-vf", "scale=480:-2", str(out_root / frame)], capture_output=True)
            mm, ss = divmod(c["t"], 60)
            meta.append({"file": name, "score": c["score"], "source": str(p), "at_s": round(c["t"], 1),
                         "frame": frame, "car": lab.get("car", ""),
                         "note": labelled("", lab) + f"score {c['score']} · {c['note']} · {c['src']['kind']}"
                                 + (f" ({c['src']['note']})" if c['src']['note'] else "")
                                 + f" · {p.stem} @ {int(mm)}:{ss:04.1f}"})
        (d / "candidates.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"{kind}: {len(meta)} clips in {d}")


if __name__ == "__main__":
    main()
