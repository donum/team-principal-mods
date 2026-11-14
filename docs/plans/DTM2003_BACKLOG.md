# Backlog: DTM 2003 pack and era 3 (2000–2011)

Everything still open for the 2003 pack, as of 13 November 2026. 2003 is the
mother template of [`bases/dtm-era3`](../../bases/dtm-era3), so the
**era-wide items** (tracks, calibration, sounds, rules) live here and apply
to [2006](DTM2006_BACKLOG.md) and [2010](DTM2010_BACKLOG.md) too. Game
limits are in [DEVELOPER_WISHLIST.md](../DEVELOPER_WISHLIST.md), not here.

Priority: **P1** = changes how the game plays, **P2** = more of the real
season, **P3** = presentation.

## 1. Era-wide (bases/dtm-era3)

| Item | What | Prio |
|---|---|---|
| Calibrate lap times | `car_profile: dtm_v8_silhouette` is era 4's 2013 profile with corner speed 1.10 instead of 1.13, a guess. Run `tools/simulate.py dtm-2003 --runs 6` and fit poles against `research/results/` (not collected yet: add 2003 qualifying times first). Then `speed_mult` per track as in the 2012 pack. | P1 |
| Two stops | `tyre_wear_mult` per track is the 2012 value scaled by laps. Check in the simulator that the field stops twice and that refuelling (60 kg tank) doesn't force a third stop. | P1 |
| Norisring speed | The 1991 Group A trace with `speed_mult` 1.27 (era 4 uses 1.29, 2012 1.233). Recheck with the sims. | P1 |
| Engine sounds | Collect 2003 onboard and trackside recordings (Abt-Audi TT-R, AMG-Mercedes CLK, Opel Astra V8) for the `dtm-era3` overlay (`ENGINE_AUDIO_BASE=dtm-era3`, its own `ENGINE_AUDIO_DATA`). Until then all era-3 packs keep vanilla sounds. Later A4 and C-Klasse recordings would need `recording_years` widened. | P2 |
| Opel logo | `assets/engines/Opel.png` and `Opel4.0V8.png` (`tools/logo_art.py`, add an `art/logos.json` like era 4's). Dunlop tyre logo `assets/tyre/Dunlop.png`. | P3 |
| Trace tracks | Done on 13 Nov 2026 in `bases/dtm-era3/track_specs/`: Adria (2,590 m, -4%), Donington GP (3,963 m), Lausitz long course (`lausitzring03`, 4,550 m along OSM way 115077605), Barcelona national (2,872 m, via the link after turn 2), Le Mans Bugatti (4,112 m). All `speed_scale` 1.0: calibrate with the sims. Open: confirm the 2003 Lausitz turn 1 (oval or infield); the Barcelona stadium section follows today's ways. Still placeholders: Hockenheim 3.736 km (2010; OSM's Kleiner Kurs is about 2.6 km, so the layout needs a source first) and the 2010 Shanghai street circuit (not in OSM; draw by hand with `via` points from a period map). For the other era-3 years: Sachsenring, Zolder, Spa, Istanbul, Brno, Estoril, Mugello, Dijon. | P2 |
| Lausitz short course | Era 4's trace is 3.478 km; 2006 raced 3.442 km. Fine for now. | P3 |
| Results | `research/results/` per round (poles, winners) for the simulator report. | P2 |

## 2. DTM 2003

- **Sponsors** · P2: `sponsors` in `gen.json` from period photos (Vodafone,
  Express-Service, Hasseröder, PlayStation 2, Red Bull, S line, OPC,
  Original-Teile, ARTA, Service 24h...).
- **Colours** · P3: every team colour is an estimate; check against photos.
- **Car images** · P3: none yet. Ask Pappydhorn12 whether 2003 drawings are
  possible; otherwise `tools/car_drawings.py` / `tools/car_art.py`.
- **Team logos and portraits** · P3: `tools/logo_art.py seasons/dtm-2003`,
  `tools/portrait_art.py`. Photo grants (de Wolde, Spieler) cover all years.
- **Unverified facts** · P2: car numbers at Rosberg and Kaneishi,
  Wendlinger's and Tomczyk's car spec, Lausitz layout length, minimum
  weight (see `research/season.md`).
- **Huisman** · P3: raced rounds 1–2 for Rosberg before Paffett; he is a
  reserve (wishlist C2).
