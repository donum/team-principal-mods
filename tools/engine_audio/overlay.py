"""Apply or remove the private engine-audio overlay on an INSTALLED game pack.

package.py writes private/engine_audio/pack/<overlay id>/ with:
    files/...        audio files, at their path inside the pack
    overlay.json     {"files": [...], "clips": {manifest: [clip, ...]},
                      "set": {json file: {"dotted.key": value}},
                      "passby_by_make": {make: clip key}}

A pack plays a stack of sound sets (layers.audio_sets): its era base's,
and on top, its season's own set if it has one ("audio": {"overlay": ...}
in season.json). The stack is combined into one overlay, the upper set
winning per file, clip key and value, so a season set that makes only a
few slots keeps the base's other sounds. "passby_by_make" tags each engine
supplier whose name starts with the make, so it fits any season of the base.

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
sys.path.insert(0, str(REPO / "tools"))
import layers  # noqa: E402
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
    """Set a dotted key; a path the pack doesn't have is skipped, so one
    overlay fits every season of a base."""
    keys = dotted.split(".")
    for k in keys[:-1]:
        if not isinstance(data.get(k), dict):
            return
        data = data[k]
    data[keys[-1]] = value


def _slug(text: str) -> str:
    return "".join(c for c in text.lower() if c.isalnum())


def overlay_for(overlay_id: str) -> Path | None:
    src = PACK_ROOT / overlay_id
    return src if (src / "overlay.json").exists() else None


def combine(overlay_ids: list[str]) -> tuple[dict, dict[str, Path], list[str]] | None:
    """One overlay from a stack of sound sets, bottom first (layers.audio_sets):
    a later set wins per file, clip key, set value and make. Sets not built
    yet are skipped. Returns (overlay, {file: source folder}, ids used)."""
    ov = {"files": [], "clips": {}, "set": {}, "passby_by_make": {}}
    origin, used = {}, []
    for oid in overlay_ids:
        src = overlay_for(oid)
        if src is None:
            continue
        one = _read(src / "overlay.json")
        used.append(oid)
        for rel in one["files"]:
            if rel not in origin:
                ov["files"].append(rel)
            origin[rel] = src
        for rel, clips in one.get("clips", {}).items():
            by_key = {c["key"]: c for c in ov["clips"].get(rel, [])}
            by_key.update({c["key"]: c for c in clips})
            ov["clips"][rel] = list(by_key.values())
        for rel, values in one.get("set", {}).items():
            ov["set"].setdefault(rel, {}).update(values)
        ov["passby_by_make"].update(one.get("passby_by_make", {}))
    return (ov, origin, used) if used else None


def _ids(overlay_ids: str | list[str]) -> list[str]:
    return [overlay_ids] if isinstance(overlay_ids, str) else list(overlay_ids)


def apply(target: Path, overlay_ids: str | list[str], pack: str | None = None) -> str:
    """Apply one sound set, or a stack of them (bottom first)."""
    combined = combine(_ids(overlay_ids))
    if combined is None:
        return "no private audio overlay built"
    ov, origin, used = combined
    remove(target, quiet=True)                      # start from the clean pack
    state = target / STATE_DIR
    backup = state / "backup"
    backup.mkdir(parents=True, exist_ok=True)

    sets = {rel: dict(values) for rel, values in ov.get("set", {}).items()}
    if ov.get("passby_by_make") and (target / "engines.json").exists():
        for name in _read(target / "engines.json").get("suppliers", {}):
            key = next((k for make, k in ov["passby_by_make"].items() if _slug(name).startswith(_slug(make))), None)
            if key:
                sets.setdefault("engines.json", {})[f"suppliers.{name}.passby_audio"] = key
    touched = set(ov.get("clips", {})) | set(sets)
    for rel in sorted(touched):
        live = target / rel
        if live.exists():
            dst = backup / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(live, dst)
    for rel in ov["files"]:
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin[rel] / "files" / rel, dst)
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
    for rel, values in sets.items():
        path = target / rel
        data = _read(path)
        for dotted, value in values.items():
            _set(data, dotted, value)
        _write(path, data)
    _write(state / "applied.json", {"files": ov["files"], "touched": sorted(touched)})
    (target / MARKER).write_text(MARKER_TEXT.format(pack=pack or target.name), encoding="utf-8")
    return f"private audio overlay {' + '.join(used)} applied: {len(ov['files'])} files, {len(touched)} JSON files patched"


def bake(target: Path, overlay_ids: str | list[str]) -> str:
    """Apply the overlay for good: same files and JSON edits as apply(), but no
    backup and no do-not-upload marker. For sets that ship with the pack
    ("audio": {"in_pack": true}); build_pack.py bakes into dist/."""
    msg = apply(target, overlay_ids)
    shutil.rmtree(target / STATE_DIR, ignore_errors=True)
    (target / MARKER).unlink(missing_ok=True)
    return msg.replace("private audio overlay", "engine audio").replace("applied", "baked in")


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
    ap.add_argument("--pack", default="dtm2013", help="installed pack folder")
    ap.add_argument("--target", type=Path, help="installed pack folder (default: <game>/data/<pack>)")
    args = ap.parse_args()
    if args.target:
        target = args.target
    else:
        local = json.loads((REPO / "local.json").read_text(encoding="utf-8"))
        target = Path(local["game_path"]) / "data" / args.pack
    if not target.is_dir():
        raise SystemExit(f"pack not installed: {target}")
    season = layers.season_for_pack(args.pack)
    sounds = [s["overlay"] for s in layers.audio_sets(season)] if season else [args.pack]
    if args.action == "apply":
        print(apply(target, sounds, args.pack))
    elif args.action == "remove":
        print(remove(target))
    else:
        print("installed" if (target / STATE_DIR / "applied.json").exists() else "not installed",
              "| " + ", ".join(f"{s} {'built' if overlay_for(s) else 'not built'}" for s in sounds))
    return 0


if __name__ == "__main__":
    sys.exit(main())
