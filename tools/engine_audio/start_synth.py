"""Race-start sound built from clean onboard recordings (no broadcast audio).

The broadcasts cannot give a clean start: the commentators talk loudest
exactly there, and no separation model removes that without artefacts. So
the start is simulated, car by car, from the 45 clean onboard laps:

  grid      22 cars on the staggered 2013 grid (8 m per position, two
            columns 3 m either side of the centre line), each its own
            onboard recording.
  idle      before lights out each car holds 5,000-6,500 rpm and jabs the
            throttle about once a second, up to 7,000 rpm or onto the 8,500
            rpm limiter (a short bounce): its onboard audio replayed at a
            pitch-controlled rate. The tracked rpm of the source sets the
            rate, so the pitch is exact. Duller than full throttle (no load).
  launch    at its own reaction time (0.15-0.45 s, a little later further
            back) each car dumps the clutch: a short rev flare, the bog as
            the clutch bites, then within a second its onboard
            acceleration at real speed, upshifts and all. Full throttle at
            once, with a bark on top; the first 0.6 s keeps more of the
            raw crackle.
  real pack from half a second after lights out, a real trackside recording
            of a DTM pack arriving (2015 Hockenheim, no commentary) is
            layered under the simulated field, 3 dB below it.
  motion    0-200 km/h-ish: v(t) = vmax (1 - exp(-t / tau)). Every car is
            heard through physics: emission-time solving (travel time and
            Doppler), 1/r level, distance damping of the highs, and an AB
            microphone pair 30 cm apart (natural stereo time differences).
            The listener stands 13-20 m from the grid, beside its front half.
  cleanup   a comb mask on each car's known rpm keeps the engine lines and
            removes the onboard wind/road noise (strong on the grid, mild
            when moving); stereo narrowed to the stock clips' width.
  venue     a short grandstand reflection pattern and a light diffuse tail.

render_start(seed) returns (idle_loop, launch) at 44.1 kHz stereo:
idle_loop is seamless, launch starts at lights out and fades as the field
leaves, matching the game's grid_idle_NN / grid_launch_NN clips.

    python tools/engine_audio/start_synth.py [--variants 4] [--out DIR]
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.ndimage import maximum_filter1d, median_filter, uniform_filter1d
from scipy.signal import butter, fftconvolve, sosfilt

from common import DATA, FEATURE_DIR, connect, decode, write_wav

SR = 44100
C = 343.0
FPS = 20                     # segment.py feature rate
LAUNCH_S = 10.9              # game clip lengths
IDLE_S = 8.0
GRID = 22                    # 2013 entry list
LIMIT = 8500                 # rev limiter (2013 DTM V8)
WIDTH = 0.35                 # side-channel scale: stock grid clips have L/R correlation ~0.8
MIX_2013 = {"Audi": 8, "BMW": 8, "Mercedes": 6}
# Real trackside recording of a DTM V8 pack arriving (2015 Hockenheim, no
# commentary): it swells from 82 s to 85 s. Layered under the simulated
# launch from just after lights out, it gives the start a real crowd of
# engines. (video id, source second that lines up with lights out + PACK_LAG)
REAL_PACK = ("Oz5JnogDN_Q", 81.5)
PACK_LAG = 0.5
PACK_DB = -3.0               # its level relative to the simulated field, 2-6 s after go


# ------------------------------------------------------------------ sources

@dataclass
class Source:
    video_id: str
    make: str
    who: str
    path: Path
    start_s: float           # launch window start in the source
    rpm: np.ndarray          # tracked rpm of the whole source, FPS rate


def find_sources(db, n_max: int = 60, window_s: float = 11.0) -> list[Source]:
    """Best clean acceleration window per onboard: no speech, no braking, upshifts."""
    out = []
    w = int(window_s * FPS)
    rows = db.execute("""SELECT v.id, v.manufacturer, v.driver, v.track, a.path FROM videos v
                         JOIN audio a ON a.id = v.id WHERE v.video_type = 'onboard'""").fetchall()
    for v in rows:
        f = FEATURE_DIR / f"{v['id']}.npz"
        if not f.exists():
            continue
        d = np.load(f)
        rpm, c, sp, mu = d["rpm"], d["clarity"], d["speech"], d["multi"]
        lr = np.log(np.maximum(rpm, 1))
        slope = np.gradient(uniform_filter1d(lr, 5)) * FPS
        jump = np.concatenate([lr[3:] - lr[:-3], np.zeros(3)])
        smooth = maximum_filter1d(np.abs(jump), 8) < 0.06
        brake = (smooth & (slope < -0.08)).astype(float)
        ups = (jump < -0.07).astype(np.int8)
        best = None
        for s in range(0, len(rpm) - w, 10):
            sl = slice(s, s + w)
            valid, talk, br = (c[sl] > 3).mean(), sp[sl].mean(), brake[sl].mean()
            n_up = int((np.diff(np.concatenate([[0], ups[sl]])) == 1).sum())
            if talk > 0.2 or br > 0.08 or valid < 0.55 or n_up < 1:
                continue
            score = valid - br - 0.5 * mu[sl].mean() + 0.05 * min(n_up, 3)
            if best is None or score > best[0]:
                best = (score, s / FPS)
        if best:
            clean = median_filter(np.where(c > 2.0, rpm, np.nan), size=5)
            idx = np.arange(len(clean))
            ok = np.isfinite(clean)
            filled = np.interp(idx, idx[ok], clean[ok]) if ok.any() else np.full(len(clean), 6500.0)
            out.append((best[0], Source(v["id"], v["manufacturer"] or "?",
                                        f"{v['driver']} {v['track']}", Path(v["path"]), best[1], filled)))
    out.sort(key=lambda t: -t[0])
    return [s for _, s in out[:n_max]]


def pick_grid(sources: list[Source], rng: np.random.Generator) -> list[Source]:
    """22 cars in the 2013 make mix, each from a different onboard, in random order."""
    by = {}
    for s in sources:
        by.setdefault(s.make, []).append(s)
    grid = []
    for make, n in MIX_2013.items():
        pool = by.get(make, [])
        grid += [pool[i] for i in rng.permutation(len(pool))[:n]]
    rest = [s for s in sources if s not in grid]
    grid += [rest[i] for i in rng.permutation(len(rest))[:max(0, GRID - len(grid))]]
    return [grid[i] for i in rng.permutation(len(grid))]


# ---------------------------------------------------------------- per car

def harmonic_mask(x: np.ndarray, rpm: np.ndarray, floor: float, fmax: float = 4000.0) -> np.ndarray:
    """Keep the engine's order-2 lines (multiples of rpm/30), damp what lies between.

    Onboard microphones at speed record wind and road noise; summed over a
    grid of cars it turns into hiss. The rpm of every output sample is known,
    so a soft comb mask in the STFT removes the noise but not the engine.
    """
    n_fft, hop = 2048, 512
    win = np.hanning(n_fft)
    pad = np.concatenate([np.zeros(n_fft), x, np.zeros(n_fft)])
    frames = np.lib.stride_tricks.sliding_window_view(pad, n_fft)[::hop] * win
    spec = np.fft.rfft(frames, axis=1)
    freqs = np.fft.rfftfreq(n_fft, 1 / SR)
    centres = np.clip(np.arange(len(frames)) * hop + n_fft // 2 - n_fft, 0, len(x) - 1)
    f2 = rpm[centres][:, None] / 30.0
    k = freqs[None, :] / f2
    dist = np.abs(k - np.round(k))                      # 0 on a line, 0.5 midway
    width = 0.5 * 24.0 / f2                             # ~±12 Hz tolerance per line
    mask = floor + (1 - floor) * np.exp(-0.5 * (dist / np.maximum(width, 0.06)) ** 2)
    mask[:, freqs > fmax] = floor
    mask[:, freqs < 0.6 * f2[:, 0].min()] = 1.0         # keep the rumble below the first line
    y = np.fft.irfft(spec * mask, n_fft, axis=1) * win
    out = np.zeros(len(pad))
    norm = np.zeros(len(pad))
    for i in range(len(frames)):
        out[i * hop:i * hop + n_fft] += y[i]
        norm[i * hop:i * hop + n_fft] += win ** 2
    return (out / np.maximum(norm, 1e-6))[n_fft:n_fft + len(x)]


def rate_play(src: np.ndarray, src_rpm, p0: float, target_rpm: np.ndarray, block: int = 441):
    """Play src from sample p0 so its pitch follows target_rpm (one value per output sample)."""
    n = len(target_rpm)
    pos = np.empty(n)
    p = p0
    for i in range(0, n, block):
        r = target_rpm[i] / max(src_rpm(p / SR), 1500.0)
        k = min(block, n - i)
        pos[i:i + k] = p + r * np.arange(k)
        p += r * k
    pos = np.clip(pos, 0, len(src) - 2)
    return np.interp(pos, np.arange(len(src)), src)


def car_dry(s: Source, go: float, t0: float, t1: float, rng) -> np.ndarray:
    """Mono emission signal of one car on the time grid [t0, t1) (go = its launch time)."""
    n = int((t1 - t0) * SR)
    t = t0 + np.arange(n) / SR
    pre = max(0.0, go - t0) + 0.2
    # source audio: idle material from before the launch window, launch from the window
    idle_from = max(0.0, s.start_s - 1.0 - pre * 1.8)
    src = decode(s.path, idle_from, (s.start_s - idle_from) + (t1 - go) + 1.0, SR, 1)[:, 0]
    src_rpm = lambda sec: np.interp((idle_from + sec) * FPS, np.arange(len(s.rpm)), s.rpm)

    # grid revs: drivers hold 5,000-6,500 rpm on the throttle, jab it every
    # second or so (some up to the limiter, bouncing off it), never steady
    hold = rng.uniform(5000, 6500)
    kr = 100                                                   # control rate (Hz)
    m_c = int((t1 - t0) * kr) + 2
    tc = t0 + np.arange(m_c) / kr
    jit = uniform_filter1d(rng.normal(0, 1, m_c), 12)
    ctrl = hold + 1400 * jit / (jit.std() + 1e-9) * 0.25
    tt = rng.uniform(t0, go - 0.25)
    while tt < go - 0.25:
        peak = rng.uniform(7000, LIMIT) if rng.random() < 0.75 else LIMIT
        att, dec = rng.uniform(0.06, 0.12), rng.uniform(0.2, 0.45)
        d = tc - tt
        env = np.where(d < 0, 0, np.where(d < att, d / att, np.exp(-(d - att) / dec)))
        ctrl = np.maximum(ctrl, hold + (peak - hold) * env)
        if peak >= LIMIT:                                       # limiter bounce
            hold_s = rng.uniform(0.2, 0.5)
            on = (d >= att) & (d < att + hold_s)
            saw = LIMIT - 350 * ((d - att) * rng.uniform(10, 14) % 1)
            ctrl = np.where(on, saw, ctrl)
        tt += rng.exponential(1.0) + 0.35
    ctrl = np.clip(ctrl, 3800, LIMIT)
    target = np.interp(t, tc, ctrl)
    idle = rate_play(src, src_rpm, 0.0, target)
    idle = harmonic_mask(idle, target, floor=0.15)
    idle = sosfilt(butter(2, rng.uniform(2800, 3600), fs=SR, output="sos"), idle)
    idle *= 0.3 + 0.3 * np.clip((target - 4000) / (LIMIT - 4000), 0, 1)   # louder when jabbed

    # launch: a flare as the clutch is dumped, the bog as it bites, then the
    # source's own full-throttle acceleration at native speed
    k0 = int((go - t0) * SR)
    m = n - k0
    w0 = (s.start_s - idle_from) * SR
    src_at_go = src_rpm(s.start_s - idle_from)
    tau = t[k0:] - go
    h0 = target[k0]
    flare = 0.07 * np.exp(-0.5 * ((tau - 0.05) / 0.04) ** 2)
    bog = 0.17 * np.exp(-0.5 * ((tau - 0.22) / 0.09) ** 2)
    want = h0 * (1 + flare - bog)
    ramp = np.clip((tau - 0.3) / rng.uniform(0.4, 0.7), 0, 1)
    ramp = ramp * ramp * (3 - 2 * ramp)                       # smoothstep
    rel = (want / src_at_go) * (1 - ramp) + ramp              # playback rate, 1 = native
    pos = np.empty(m)
    p = w0
    for i in range(0, m, 441):
        k = min(441, m - i)
        r = rel[i] if ramp[i] < 1 else 1.0
        pos[i:i + k] = p + r * np.arange(k)
        p += r * k
    pos = np.clip(pos, 0, len(src) - 2)
    launch = np.interp(pos, np.arange(len(src)), src)
    rate = np.gradient(pos)
    out_rpm = rate * src_rpm(pos / SR)
    rough = harmonic_mask(launch, out_rpm, floor=0.6)         # the bark: keep its crackle
    clean = harmonic_mask(launch, out_rpm, floor=0.35)
    mixr = np.clip(tau / 0.6, 0, 1)[:]
    launch = rough * (1 - mixr) + clean * mixr
    launch *= 1.0 + 0.6 * np.exp(-tau / 0.3)                 # full throttle at once, a bark on top

    out = idle.copy()
    xf = int(0.06 * SR)
    fade = np.linspace(0, 1, xf)
    out[k0:k0 + xf] = idle[k0:k0 + xf] * (1 - fade) + launch[:xf] * fade
    out[k0 + xf:] = launch[xf:]
    return out.astype(np.float32)


# ------------------------------------------------------------------- scene

def motion(t: np.ndarray, go: float, x0: float, vmax: float, tau: float) -> np.ndarray:
    tt = np.clip(t - go, 0, None)
    return x0 + vmax * (tt - tau * (1 - np.exp(-tt / tau)))


def render_scene(cars, t0: float, t1: float, listener, rng) -> np.ndarray:
    """Sum all cars as heard by an AB pair (30 cm) at listener=(x, y)."""
    n = int((t1 - t0) * SR)
    t = t0 + np.arange(n) / SR
    far_sos = butter(2, 2200, fs=SR, output="sos")
    out = np.zeros((n, 2))
    lx, ly = listener
    for car in cars:
        dry_t0 = t0 - 1.5                                      # covers the longest travel time
        dry = car["dry"]
        far = sosfilt(far_sos, dry)
        for ch, mx in enumerate((lx - 0.15, lx + 0.15)):
            tau = t.copy()
            for _ in range(4):
                x = motion(tau, car["go"], car["x0"], car["vmax"], car["tau"])
                r = np.hypot(x - mx, car["y"] - ly)
                tau = t - r / C
            idx = (tau - dry_t0) * SR
            ok = (idx >= 0) & (idx < len(dry) - 1)
            a = np.interp(idx, np.arange(len(dry)), dry) * ok
            b = np.interp(idx, np.arange(len(far)), far) * ok
            mix = np.clip((r - 20) / 160, 0, 0.85)
            # gentle directivity of each microphone (cardioid-ish, angled outwards)
            side = (x - mx) / r
            g = 0.65 + 0.35 * (side if ch == 1 else -side)
            out[:, ch] += ((1 - mix) * a + mix * b) * (12.0 / np.maximum(r, 6.0)) * g
    return out


def venue(x: np.ndarray, rng) -> np.ndarray:
    """Grandstand reflections (15-60 ms) plus a short diffuse tail."""
    n = int(0.9 * SR)
    ir = np.zeros((n, 2))
    ir[0] = 1.0
    for d, g in ((0.017, 0.32), (0.029, 0.24), (0.043, 0.18), (0.061, 0.12)):
        k = int(d * SR)
        ir[k, 0] += g * rng.uniform(0.8, 1.2)
        ir[k + int(rng.uniform(0.0005, 0.003) * SR), 1] += g * rng.uniform(0.8, 1.2)
    tail = rng.normal(0, 1, (n, 2)) * np.exp(-np.arange(n) / (0.18 * SR))[:, None] * 0.012
    tail[:int(0.03 * SR)] = 0
    ir += sosfilt(butter(2, 3000, fs=SR, output="sos"), tail, axis=0)
    return np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], axis=1)


def add_real_pack(mix: np.ndarray, k0: int, width: float) -> np.ndarray:
    """Layer the real pack recording from lights out + PACK_LAG (skipped if not extracted)."""
    try:
        db = connect()
        row = db.execute("SELECT path FROM audio WHERE id=?", (REAL_PACK[0],)).fetchone()
    except SystemExit:
        row = None
    if not row or not Path(row["path"]).exists():
        return mix
    start = k0 + int(PACK_LAG * SR)
    n = len(mix) - start
    real = decode(Path(row["path"]), REAL_PACK[1], n / SR, SR, 2)[:n]
    n = len(real)
    mid, side = (real[:, 0] + real[:, 1]) / 2, (real[:, 0] - real[:, 1]) / 2
    real = np.stack([mid + width * side, mid - width * side], axis=1)
    real *= np.clip(np.arange(n) / (0.8 * SR), 0, 1)[:, None]
    a, b = int(1.5 * SR), int(5.5 * SR)                        # 2-6 s after go
    rms = lambda x: np.sqrt(np.mean(np.square(x)) + 1e-12)
    g = 10 ** (PACK_DB / 20) * rms(mix[start + a:start + b]) / rms(real[a:b])
    out = mix.copy()
    out[start:start + n] += g * real
    return out


def render_start(sources: list[Source], seed: int, listener_x: float | None = None,
                 listener_y: float | None = None):
    rng = np.random.default_rng(seed)
    grid = pick_grid(sources, rng)
    lx = listener_x if listener_x is not None else rng.uniform(-70, 0)       # beside the front half of the grid
    ly = listener_y if listener_y is not None else -rng.uniform(13, 20)      # pit wall / front grandstand
    pre = IDLE_S + 1.5
    t0, t1 = -pre, LAUNCH_S + 0.5
    cars = []
    for k, s in enumerate(grid):
        row = k // 2
        go = rng.uniform(0.15, 0.4) + 0.012 * row
        car = dict(x0=-8.0 * k, y=(-3.0 if k % 2 == 0 else 3.0) + rng.normal(0, 0.3),
                   go=go, vmax=rng.uniform(66, 74), tau=rng.uniform(6.0, 7.5) + 0.05 * row)
        car["dry"] = car_dry(s, go, t0 - 1.5, t1, rng) * rng.uniform(0.75, 1.0)
        cars.append(car)
    mix = venue(render_scene(cars, t0, t1, (lx, ly), rng), rng)
    mid, side = (mix[:, 0] + mix[:, 1]) / 2, (mix[:, 0] - mix[:, 1]) / 2
    mix = np.stack([mid + WIDTH * side, mid - WIDTH * side], axis=1)
    k0 = int(pre * SR)                                          # lights out
    mix = add_real_pack(mix, k0, WIDTH * 1.6)
    launch = mix[k0 - int(0.05 * SR):k0 - int(0.05 * SR) + int(LAUNCH_S * SR)].copy()
    fo = int(1.5 * SR)
    launch[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
    # seamless idle loop: IDLE_S of grid sound, its tail crossfaded into its head
    xf = int(1.0 * SR)
    seg = mix[int(0.5 * SR):int(0.5 * SR) + int(IDLE_S * SR) + xf]
    loop = seg[:int(IDLE_S * SR)].copy()
    w = np.linspace(0, 1, xf)[:, None]
    loop[:xf] = seg[:xf] * w + seg[-xf:] * (1 - w)
    info = dict(seed=seed, listener=(round(lx, 1), round(ly, 1)),
                cars=[f"{s.make}: {s.who} ({s.video_id} @ {s.start_s:.1f}s)" for s in grid])
    return loop.astype(np.float32), launch.astype(np.float32), info


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--variants", type=int, default=4)
    ap.add_argument("--out", type=Path, default=DATA / "pilot" / "synth_start")
    args = ap.parse_args()
    sources = find_sources(connect())
    print(f"{len(sources)} clean onboard sources")
    for v in range(1, args.variants + 1):
        idle, launch, info = render_start(sources, seed=v)
        peak = max(np.abs(idle).max(), np.abs(launch).max()) + 1e-9
        g = 10 ** (-1 / 20) / peak
        write_wav(args.out / f"start_{v:02d}_grid_idle.wav", idle * g, SR)
        write_wav(args.out / f"start_{v:02d}_grid_launch.wav", launch * g, SR)
        write_wav(args.out / f"start_{v:02d}_idle_then_launch.wav", np.concatenate([idle, idle, launch]) * g, SR)
        print(f"variant {v}: listener {info['listener']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
