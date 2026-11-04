"""Stage 2: copy each video's audio track out losslessly (no re-encode).

    private/engine_audio/audio/<make>/<track>/<session>/<driver>/<id>.mka

<driver> is the driver for onboards, otherwise the video type (_tv_broadcast,
_trackview, ...). Only catalog rows with status "done" are used (add
--include-legacy for the old yt-dlp files). Re-running skips anything already
extracted from an unchanged source, and moves files whose metadata changed
(e.g. after an override).

    python tools/engine_audio/extract.py [--include-legacy] [--all-types]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import AUDIO_DIR, ENGINE_TYPES, audio_rows, connect, run, slug, source_root

SCHEMA = """CREATE TABLE IF NOT EXISTS audio (
    id TEXT PRIMARY KEY, path TEXT, codec TEXT, src_size INTEGER, src_mtime INTEGER,
    extracted TEXT)"""


def target_for(row) -> Path:
    who = row["driver"] if row["video_type"] == "onboard" and row["driver"] else f"_{row['video_type']}"
    track = row["track"] if row["track"] else "_unknown"
    if row["round"] == 10:
        track = "Hockenheim_Final"
    return (AUDIO_DIR / slug(row["manufacturer"], "_mixed") / slug(track) /
            slug(row["session"], "_any") / slug(who) / f"{row['id']}.mka")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", type=Path)
    ap.add_argument("--include-legacy", action="store_true")
    ap.add_argument("--all-types", action="store_true", help="also features and animations")
    args = ap.parse_args()

    import datetime as dt
    source = source_root(args.source)
    db = connect()
    db.execute(SCHEMA)
    have = {r["id"]: dict(r) for r in db.execute("SELECT * FROM audio")}
    types = ("onboard", "onboard_bestof", "taxi", "trackview", "broadcast", "highlights",
             "feature", "animation") if args.all_types else ENGINE_TYPES

    done = skipped = moved = failed = 0
    for row in audio_rows(db, args.include_legacy, types):
        src = source / row["file"]
        if not src.exists():
            continue
        st = src.stat()
        dst = target_for(row)
        prev = have.get(row["id"])
        if prev and prev["src_size"] == st.st_size and prev["src_mtime"] == int(st.st_mtime):
            old = Path(prev["path"])
            if old == dst and dst.exists():
                skipped += 1
                continue
            if old.exists() and old != dst:      # metadata changed: move, don't re-extract
                dst.parent.mkdir(parents=True, exist_ok=True)
                old.replace(dst)
                db.execute("UPDATE audio SET path=? WHERE id=?", (str(dst), row["id"]))
                moved += 1
                continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = dst.with_name(dst.stem + ".tmp.mka")
        try:
            run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-map", "0:a:0", "-vn",
                 "-c", "copy", str(tmp)])
            tmp.replace(dst)
        except RuntimeError as e:
            print(f"FAILED {row['id']} {row['title']}: {e}")
            tmp.unlink(missing_ok=True)
            failed += 1
            continue
        db.execute("INSERT OR REPLACE INTO audio VALUES (?,?,?,?,?,?)",
                   (row["id"], str(dst), row["audio_codec"], st.st_size, int(st.st_mtime),
                    dt.datetime.now().isoformat(timespec="seconds")))
        db.commit()
        done += 1
        print(f"extracted {dst.relative_to(AUDIO_DIR)}")
    db.commit()
    print(f"{done} extracted, {moved} moved, {skipped} up to date, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
