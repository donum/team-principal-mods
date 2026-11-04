"""Stage 4: browsable library of the best clips, plus a coverage report.

    private/engine_audio/library/
        index.html                         open in a browser: every cell, playable
        coverage.md                        make x track x category, clean seconds
        <make>/<track>/<session>/<label>/NN_q0.83_<driver>_<id>_<start>.wav

Clips are cut from the segment references (44.1 kHz stereo WAV, 0.25 s
padding). Re-running only cuts what changed and removes clips that dropped
out of the top N.

    python tools/engine_audio/library.py [--top 5] [--min-quality 0.15]
"""
from __future__ import annotations

import argparse
import html
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

from common import LIBRARY_DIR, MAKES, connect, decode, load_json, dump_json, slug, write_wav

LABELS = ["idle", "launch", "pit_exit", "full_throttle", "steady_high", "upshift",
          "downshift", "overrun", "passby"]
TRACKS = ["Hockenheim", "Brands Hatch", "Spielberg", "Lausitzring", "Norisring", "Moscow",
          "Nurburgring", "Oschersleben", "Zandvoort", "Hockenheim Final"]
PAD = 0.25
SR = 44100


def track_name(row) -> str:
    return "Hockenheim Final" if row["round"] == 10 else (row["track"] or "Unknown")


def load_segments(db, include_flagged: bool):
    q = """SELECT s.*, v.manufacturer, v.track, v.round, v.session, v.driver, v.video_type,
                  v.title, a.path AS audio_path
           FROM segments s JOIN videos v ON v.id = s.video_id JOIN audio a ON a.id = s.video_id"""
    rows = [dict(r) for r in db.execute(q)]
    if not include_flagged:
        rows = [r for r in rows if not r["flags"]]
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=5, help="clips per cell")
    ap.add_argument("--min-quality", type=float, default=0.15)
    ap.add_argument("--include-flagged", action="store_true",
                    help="also rank segments flagged for commentary, wind or other cars")
    args = ap.parse_args()

    db = connect()
    segs = load_segments(db, args.include_flagged)
    cells = defaultdict(list)
    for s in segs:
        key = (s["manufacturer"] or "_mixed", track_name(s), s["session"] or "any", s["label"])
        cells[key].append(s)

    state_path = LIBRARY_DIR / "clips.json"
    state = load_json(state_path, {})          # relative path -> seg_id
    wanted = {}
    for key, items in cells.items():
        items.sort(key=lambda r: -r["quality"])
        top = [r for r in items if r["quality"] >= args.min_quality][:args.top]
        make, track, session, label = key
        for rank, r in enumerate(top, 1):
            who = r["driver"] or r["video_type"]
            name = (f"{rank:02d}_q{r['quality']:.2f}_{slug(who)}_{r['video_id']}_"
                    f"{int(r['start_s'] * 1000):08d}.wav")
            rel = "/".join([slug(make), slug(track), slug(session), label, name])
            wanted[rel] = r
            r["clip"] = rel

    # remove clips that dropped out, cut the new ones
    for rel in set(state) - set(wanted):
        (LIBRARY_DIR / rel).unlink(missing_ok=True)
    cut = 0
    for rel, r in wanted.items():
        dst = LIBRARY_DIR / rel
        if dst.exists() and state.get(rel) == r["seg_id"]:
            continue
        start = max(0.0, r["start_s"] - PAD)
        audio = decode(Path(r["audio_path"]), start, r["end_s"] - start + PAD, SR, 2)
        fade = min(len(audio) // 4, int(0.02 * SR))
        if fade:
            ramp = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
            audio[:fade] *= ramp
            audio[-fade:] *= ramp[::-1]
        write_wav(dst, audio, SR)
        cut += 1
    for d in sorted(LIBRARY_DIR.rglob("*"), reverse=True):     # prune empty folders
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
    dump_json(state_path, {rel: r["seg_id"] for rel, r in wanted.items()})

    write_coverage(segs, args.min_quality, args.include_flagged)
    write_index(wanted, segs, args.min_quality)
    print(f"{len(wanted)} clips in {len({k[:3] for k in cells})} make/track/session cells "
          f"({cut} newly cut) -> {LIBRARY_DIR / 'index.html'}")
    return 0


def coverage_table(segs, min_q):
    """{(make, track): {label: clean seconds}} for segments above min_q."""
    cov = defaultdict(lambda: defaultdict(float))
    for s in segs:
        if s["quality"] >= min_q:
            cov[(s["manufacturer"] or "_mixed", track_name(s))][s["label"]] += s["end_s"] - s["start_s"]
    return cov


def write_coverage(segs, min_q, flagged=False) -> None:
    cov = coverage_table(segs, min_q)
    db = connect()
    vids = db.execute("""SELECT manufacturer, round, track, status, video_type FROM videos
                         WHERE video_type IN ('onboard','trackview')""").fetchall()
    lines = ["# Engine-audio coverage", "",
             f"Seconds per category (quality >= {min_q}"
             + (", flagged segments included)." if flagged else ", no commentary/wind/other-car flags)."),
             "`done/known` = driver onboards and trackviews downloaded / listed in the queue.", ""]
    for make in (*MAKES, "_mixed"):
        lines += [f"## {make}", "",
                  "| track | videos | " + " | ".join(LABELS) + " |",
                  "|---|---|" + "---|" * len(LABELS)]
        for track in TRACKS:
            vs = [v for v in vids if v["manufacturer"] == make
                  and (("Hockenheim Final" if v["round"] == 10 else v["track"]) == track)]
            vcell = f"{sum(v['status'] == 'done' for v in vs)}/{len(vs)}" if vs else "."
            c = cov.get((make, track), {})
            lines.append(f"| {track} | {vcell} | " + " | ".join(
                f"{c[l]:.0f}" if c.get(l) else "." for l in LABELS) + " |")
        lines.append("")
    (LIBRARY_DIR / "coverage.md").parent.mkdir(parents=True, exist_ok=True)
    (LIBRARY_DIR / "coverage.md").write_text("\n".join(lines), encoding="utf-8")


def write_index(wanted, segs, min_q) -> None:
    cov = coverage_table(segs, min_q)
    by_cell = defaultdict(list)
    for rel, r in wanted.items():
        by_cell[(r["manufacturer"] or "_mixed", track_name(r))].append(r)
    e = html.escape
    out = ["<!doctype html><meta charset=utf-8><title>DTM 2013 engine library</title>",
           "<style>body{font:14px system-ui;margin:24px;color:#222;background:#fafafa}"
           "table{border-collapse:collapse;margin:8px 0 24px}td,th{border:1px solid #ddd;padding:4px 8px;"
           "text-align:right}th{background:#eee}td.l{text-align:left}audio{height:28px;vertical-align:middle}"
           "h2{margin-top:32px}.q{font-variant-numeric:tabular-nums;color:#555}</style>",
           "<h1>DTM 2013 engine library</h1>",
           "<p>Private, personal use only: source audio belongs to ITR / DTM. "
           f"Coverage in clean seconds (quality &ge; {min_q}).</p>"]
    for make in (*MAKES, "_mixed"):
        out.append(f"<h2>{e(make)}</h2><table><tr><th class=l>track</th>"
                   + "".join(f"<th>{l}</th>" for l in LABELS) + "</tr>")
        for track in TRACKS:
            c = cov.get((make, track), {})
            out.append(f"<tr><td class=l>{e(track)}</td>" + "".join(
                f"<td>{c[l]:.0f}</td>" if c.get(l) else "<td>.</td>" for l in LABELS) + "</tr>")
        out.append("</table>")
        for track in TRACKS:
            clips = sorted(by_cell.get((make, track), []), key=lambda r: (LABELS.index(r["label"])
                           if r["label"] in LABELS else 99, -r["quality"]))
            if not clips:
                continue
            out.append(f"<h3>{e(make)} &middot; {e(track)}</h3><table><tr><th class=l>category</th>"
                       "<th>quality</th><th>rpm</th><th class=l>source</th><th class=l>clip</th></tr>")
            for r in clips:
                rpm = f"{r['rpm_start']:.0f}&rarr;{r['rpm_end']:.0f}"
                src = f"{e(r['driver'] or r['video_type'])} &middot; {e(r['session'] or '')} @ {r['start_s']:.1f}s"
                out.append(f"<tr><td class=l>{r['label']}</td><td class=q>{r['quality']:.2f}</td>"
                           f"<td class=q>{rpm}</td><td class=l>{src}</td>"
                           f"<td class=l><audio controls preload=none src=\"{e(r['clip'])}\"></audio></td></tr>")
            out.append("</table>")
    (LIBRARY_DIR / "index.html").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
