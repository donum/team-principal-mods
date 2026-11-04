"""Apply or remove the private engine-audio overlay on an INSTALLED game pack.

package.py writes private/engine_audio/pack/<pack_folder>/ with:
    files/...        audio files, at their path inside the pack
    overlay.json     {"files": [...], "clips": {manifest: [clip, ...]},
                      "set": {json file: {"dotted.key": value}}}

apply() copies the files, upserts manifest clips by key, sets the values and
keeps a backup of every JSON file it touched, so remove() restores the pack
exactly. build_pack.py --install calls apply() after installing (the overlay
never enters dist/). Standard library only, so build_pack needs no numpy.

    python tools/engine_audio/overlay.py apply|remove|status [--pack dtm2013]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACK_ROOT = Path(os.environ.get("ENGINE_AUDIO_DATA", REPO / "private" / "engine_audio")) / "pack"
STATE_DIR = "assets/audio/_private_overlay"      # inside the installed pack
MARKER = "assets/audio/PRIVATE_AUDIO_DO_NOT_UPLOAD.txt"
MARKER_TEXT = """This pack has a PRIVATE engine-audio overlay (DTM/ITR broadcast audio,
personal use only). Do not upload this folder to the Steam Workshop.

Remove it first:   python tools/engine_audio/overlay.py remove --pack {pack}
or reinstall clean: python tools/build_pack.py seasons/<season> --install --no-private-audio
"""


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _set(data: dict, dotted: str, value) -> None:
    keys = dotted.split(".")
    for k in keys[:-1]:
        data = data[k]
    data[keys[-1]] = value


def overlay_for(pack: str) -> Path | None:
    src = PACK_ROOT / pack
    return src if (src / "overlay.json").exists() else None


def apply(target: Path, pack: str) -> str:
    src = overlay_for(pack)
    if src is None:
        return "no private audio overlay built"
    ov = _read(src / "overlay.json")
    remove(target, quiet=True)                      # start from the clean pack
    state = target / STATE_DIR
    backup = state / "backup"
    backup.mkdir(parents=True, exist_ok=True)

    touched = set(ov.get("clips", {})) | set(ov.get("set", {}))
    for rel in sorted(touched):
        live = target / rel
        if live.exists():
            dst = backup / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(live, dst)
    for rel in ov["files"]:
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / "files" / rel, dst)
    for rel, clips in ov.get("clips", {}).items():
        path = target / rel
        data = _read(path)
        by_key = {c["key"]: i for i, c in enumerate(data["clips"]) if "key" in c}
        for clip in clips:
            if clip["key"] in by_key:
                data["clips"][by_key[clip["key"]]] = clip
            else:
                data["clips"].append(clip)
        _write(path, data)
    for rel, values in ov.get("set", {}).items():
        path = target / rel
        data = _read(path)
        for dotted, value in values.items():
            _set(data, dotted, value)
        _write(path, data)
    _write(state / "applied.json", {"files": ov["files"], "touched": sorted(touched)})
    (target / MARKER).write_text(MARKER_TEXT.format(pack=pack), encoding="utf-8")
    return f"private audio overlay applied: {len(ov['files'])} files, {len(touched)} JSON files patched"


def remove(target: Path, quiet: bool = False) -> str:
    state = target / STATE_DIR
    applied = state / "applied.json"
    if not applied.exists():
        return "" if quiet else "no private audio overlay installed"
    info = _read(applied)
    for rel in info["files"]:
        (target / rel).unlink(missing_ok=True)
    for rel in info["touched"]:
        b = state / "backup" / rel
        if b.exists():
            shutil.copy2(b, target / rel)
    shutil.rmtree(state, ignore_errors=True)
    (target / MARKER).unlink(missing_ok=True)
    return f"private audio overlay removed ({len(info['files'])} files, {len(info['touched'])} JSON files restored)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["apply", "remove", "status"])
    ap.add_argument("--pack", default="dtm2013")
    ap.add_argument("--target", type=Path, help="installed pack folder (default: <game>/data/<pack>)")
    args = ap.parse_args()
    if args.target:
        target = args.target
    else:
        local = json.loads((REPO / "local.json").read_text(encoding="utf-8"))
        target = Path(local["game_path"]) / "data" / args.pack
    if not target.is_dir():
        raise SystemExit(f"pack not installed: {target}")
    if args.action == "apply":
        print(apply(target, args.pack))
    elif args.action == "remove":
        print(remove(target))
    else:
        print("installed" if (target / STATE_DIR / "applied.json").exists() else "not installed",
              "| built" if overlay_for(args.pack) else "| not built")
    return 0


if __name__ == "__main__":
    sys.exit(main())
