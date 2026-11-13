"""Copy tools/web/season-picker.js to every page that uses it.

The pages live in other folders and are opened from file:// or their own local
server, so each keeps its own copy. Edit the one here, then run:

    python -I tools/web/sync_season_picker.py

A target whose folder is missing on this machine is skipped.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "season-picker.js"
REPOS = HERE.parents[2]   # C:/_/repositories
TARGETS = [
    Path.home() / "Pictures" / "mods" / "gallery" / "season-picker.js",          # season image gallery
    REPOS / "race-tracks" / "browser" / "season-picker.js",                       # Race Tracks library
    REPOS / "race-track-themes" / "tools" / "templates" / "season-picker.js",     # track art batch pages (inlined by report_art_batch.py)
]

for t in TARGETS:
    if not t.parent.is_dir():
        print("skip (no folder):", t)
        continue
    shutil.copyfile(SRC, t)
    print("copied:", t)
