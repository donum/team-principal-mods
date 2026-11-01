"""Estimate lap times from a track's micro-sectors (calibration helper).

A point-mass model: corners are taken at their target speed, straights
accelerate from the corner before (power-limited, drag-limited towards the
target speed) and brake for the corner after. The result is a *reference*
time on the base game's speed scale. The game's own simulation applies the
season's car profile on top, so in-game times are compared through one
fitted factor per season (see docs/TRACKS.md, "Lap-time calibration").

Usage:
    python tools/laptime.py seasons/dtm-1991/tracks/*.json
"""

import json
import sys
from pathlib import Path

STEP_M = 2.0
ACCEL_MS2 = 9.0       # low-speed acceleration of the reference car
BRAKE_MS2 = 25.0      # braking of the reference car
V_REF_MAX = 370 / 3.6  # speed at which acceleration falls to zero


def profile(track):
    """Return a list of (length_m, cap_speed_ms, is_corner) along the lap."""
    length_m = track["length_km"] * 1000.0
    return [(s["length_pct"] / 100.0 * length_m, s["target_speed_kmh"] / 3.6, s["type"] != "straight")
            for s in track["micro_sectors"]]


def speed_profile(caps, step=STEP_M):
    """Reference speed (m/s) at each sample of a closed lap, given per-sample caps."""
    n = len(caps)
    v = caps[:]
    # Two passes around the loop so the start/finish wrap is consistent.
    for _ in range(2):
        for i in range(1, 2 * n):
            j, k = i % n, (i - 1) % n
            a = ACCEL_MS2 * max(0.0, 1 - (v[k] / V_REF_MAX) ** 2)
            v[j] = min(caps[j], (v[k] ** 2 + 2 * a * step) ** 0.5)
        for i in range(2 * n - 2, -1, -1):
            j, k = i % n, (i + 1) % n
            v[j] = min(v[j], (v[k] ** 2 + 2 * BRAKE_MS2 * step) ** 0.5)
    return v


def reference_time(track):
    caps = []
    for length, cap, corner in profile(track):
        caps += [cap] * max(1, int(length / STEP_M))
    v = speed_profile(caps)
    step = track["length_km"] * 1000.0 / len(caps)
    return sum(step / max(x, 1.0) for x in v)


def main():
    for path in sys.argv[1:]:
        track = json.loads(Path(path).read_text(encoding="utf-8"))
        t = reference_time(track)
        print(f"{Path(path).stem:15s} {track['length_km']:6.3f} km  reference {t:7.2f} s  "
              f"lap_modifier {track.get('lap_modifier')}")


if __name__ == "__main__":
    main()
