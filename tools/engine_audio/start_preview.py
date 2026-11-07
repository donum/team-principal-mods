"""Hear a race start the way the game mixes it, from the installed pack.

The timing is the game's own (ui/screens/race_screen.py, ui/live_audio.py):

    -6.0 s  grid_idle_NN loops at layer level 0.65 x its clip gain
     0.0 s  start sequence; a light comes on every 0.5 s (start_light.wav)
     1.0 s  3rd light: idle fades out (0.2 s), grid_launch_NN starts once
            at layer level 0.75 x its clip gain
     2.5 s  lights out (lights_out.wav); the cars move at 3.0 s

(times here from the 1st light). The light cues are mixed at their file
level; the game's SFX volume may differ. One preview per installed pair:

    python tools/engine_audio/start_preview.py
      -> private/engine_audio/library/starts/ingame_start_NN.wav
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_pack import game_path, load_json  # noqa: E402
from common import LIBRARY_DIR, REPO, decode, write_wav  # noqa: E402

SR = 44100
PRE_S = 6.0                      # grid idle heard before the 1st light
LIGHT_S = [0.0, 0.5, 1.0, 1.5, 2.0]
LAUNCH_AT_S = 1.0                # 3rd light
LIGHTS_OUT_S = 2.5
IDLE_LEVEL, LAUNCH_LEVEL, IDLE_FADE_S = 0.65, 0.75, 0.2


def place(mix: np.ndarray, x: np.ndarray, at_s: float) -> None:
    k = int((PRE_S + at_s) * SR)
    n = min(len(x), len(mix) - k)
    mix[k:k + n] += x[:n]


def main(pack: str | None = None) -> int:
    """pack: an installed pack carrying the overlay (default: the first
    installed season on the sound library's base)."""
    if pack is None:
        sys.path.insert(0, str(REPO / "tools"))
        import layers
        from common import OVERLAY_ID
        packs = [load_json(s / "season.json")["pack_folder"] for s in layers.seasons_on_overlay(OVERLAY_ID)]
        pack = next((p for p in packs if (game_path(None) / "data" / p).is_dir()), packs[0] if packs else "dtm2013")
    race = game_path(None) / "data" / pack / "assets" / "audio" / "race"
    clips = {c["key"]: c for c in load_json(race / "race_engines.json")["clips"]}
    light, out = decode(race / "start_light.wav", sr=SR, channels=2), decode(race / "lights_out.wav", sr=SR, channels=2)
    dst = LIBRARY_DIR / "starts"
    dst.mkdir(parents=True, exist_ok=True)
    for old in dst.glob("ingame_start_*.wav"):
        old.unlink()
    i = 1
    while f"grid_idle_{i:02d}" in clips and f"grid_launch_{i:02d}" in clips:
        ic, lc = clips[f"grid_idle_{i:02d}"], clips[f"grid_launch_{i:02d}"]
        idle = decode(race / ic["file"], sr=SR, channels=2) * ic.get("gain", 1.0) * IDLE_LEVEL
        launch = decode(race / lc["file"], sr=SR, channels=2) * lc.get("gain", 1.0) * LAUNCH_LEVEL
        total = int((PRE_S + LAUNCH_AT_S) * SR) + len(launch)
        mix = np.zeros((total, 2), np.float32)
        stop = int((PRE_S + LAUNCH_AT_S) * SR)
        bed = np.tile(idle, (stop // len(idle) + 2, 1))[:stop + int(IDLE_FADE_S * 3 * SR)]
        t = np.arange(len(bed) - stop) / SR
        bed[stop:] *= np.exp(-t / IDLE_FADE_S)[:, None]       # the game's eased layer fade
        mix[:len(bed)] += bed
        place(mix, launch, LAUNCH_AT_S)
        for s in LIGHT_S:
            place(mix, light, s)
        place(mix, out, LIGHTS_OUT_S)
        path = dst / f"ingame_start_{i:02d}.wav"
        write_wav(path, np.clip(mix, -1, 1), SR)
        print(f"{path.name}: {lc.get('source', lc['file'])}")
        i += 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
