# Backlog: DTM 2020 pack (and era 5)

Everything still open for the 2020 pack, as of 13 November 2026. Game limits
are in [DEVELOPER_WISHLIST.md](../DEVELOPER_WISHLIST.md), not here. 2020 is
the **mother season** of [`bases/dtm-era5`](../../bases/dtm-era5) (2019–2020),
so the era-wide items (sounds, engines, car profile, tracks) are listed here
and apply to 2019 too. Era 5 builds on `bases/dtm-era4`; the
[2013 backlog](DTM2013_BACKLOG.md) items for the shared tracks and tyre
model apply as well.

Priority: **P1** = changes how the game plays, **P2** = more of the real
2020 world, **P3** = presentation.

## 1. Tracks · P1

No placeholders left. Assen and Zolder are traced into the era base
(`bases/dtm-era5/track_specs/`, 13 November 2026):

| Track id | Venue | Traced | To do |
|---|---|---|---|
| `assen` | TT Circuit Assen, 4.555 km (2019 and 2020) | 4,500 m (−1.2%), start placed by hand | Calibrate `speed_scale` (1.0 now) and `tyre_wear_mult` (1.3, as Valencia). Check the DRS zone. |
| `zolder20` | Circuit Zolder, 4.011 km (2020) | 3,953 m (−1.4%) | Same. Named `zolder20` to keep it apart from `dtm-1991`'s Group A Zolder. |

Spa and the Nürburgring Grand
Prix circuit come from the F1 base with `speed_mult` 1.09 (ratio of era 4's
Hockenheim to the F1 base's): check them in the simulator, or trace DTM
copies into the base.

Race-day maps for all nine rounds, like 2013 (`tools/art_track.py`): P3.

## 2. Calibration · P1

Nothing is simulated yet. Run `tools/simulate.py dtm-2020 --runs 6`
against the 2020 poles and points (`research/results/` is still to be
written from the race pages) and tune:
- `car_profile: dtm_class1_turbo` (a guess from the 2013 profile) and
  per-track `speed_mult`;
- `tyre_wear_mult` so most cars stop once per race;
- the team spread (`rating_range` 53–58): Audi won 16 of 18 races;
- spec ERS as push-to-pass: does it give about the right gain?

## 3. Sounds · P2

No turbo recordings yet: the pack uses the game's vanilla sounds
(`bases/dtm-era5/base.json` `"audio"`, `in_pack: false`).
- Collect onboard and trackside videos of the 2020 Audi RS 5 Turbo and BMW
  M4 Turbo, then build the overlay with `tools/engine_audio`
  (`ENGINE_AUDIO_BASE=dtm-era5` with its own `ENGINE_AUDIO_DATA`).
- Pick `passby_audio` per engine; today it is the era 4 V8 choice.
- 2019 adds the Aston Martin Vantage (HWA AFR Turbo 2.0 I4).

## 4. Art · P3

- **Engine logos:** none for "Audi RC8 2.0 TFSI" and "BMW P48 Turbo"
  (era 4 has the V8 names). The maker emblems are in era 4's
  `assets/engines`; copy or name them for the new engines.
- **Car images:** none (the build warns for every team).
- **Team logos and portraits:** `tools/logo_art.py seasons/dtm-2020`,
  `tools/portrait_art.py`.
- Main menu and team dashboards: none yet. The photo permissions from 2013
  (Dennis de Wolde, Spieler Family) cover 2020 too.

## 5. Data · P2

- **Colours:** check every team against 2020 photos (all are estimates).
- **Sponsors:** none yet (`gen.json` `"sponsors"`): Orlen for ART, Schaeffler
  for Phoenix, and the others from the liveries.
- **Feeder series:** none (2013 has five).
- **Team histories:** short and generic; ART's DTM years and WRT's 2019
  start to check.
- **Unverified research:** lengths and laps come from racingyears only;
  qualifying session length; see `research/season.md`.

## 6. In-game checks · P1

- The calendar runs to week 48 because each race has its own week: does
  the end of the season still leave room for the off-season?
- WRT with three cars and `formula_team_entry_cap: three`.
- Spec ERS shows on the car screens: is the wording acceptable for
  push-to-pass?
