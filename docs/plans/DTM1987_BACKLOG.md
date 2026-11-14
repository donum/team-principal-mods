# Backlog: DTM 1987 pack

Everything still open for the 1987 pack, as of 13 November 2026. Game limits
are in [DEVELOPER_WISHLIST.md](../DEVELOPER_WISHLIST.md), not here. 1987
builds on the DTM 1991 pack (`"template": "dtm-1991"`), so Group A items
that apply to 1990 to 1992 apply here too.

Priority: **P1** = changes how the game plays, **P2** = more of the real
1987 world, **P3** = presentation.

## 1. Tracks

| Item | What | Prio |
|---|---|---|
| AVUS long circuit | Traced (`track_specs/avus87.json`): the 1991 spec's carriageways and flat Nordkurve, with the south turn bridged at 52.4733 N so the lap is 8,038 m (real 8.110 km). The real 1987 south-turn position is undocumented; find a period map or photo and move it. Calibrate `speed_scale` (copied from 1991). | P2 |
| Salzburgring | Traced (`track_specs/salzburgring.json`, OSM relation 19552391): 4,187 m against 4.225 km. Today's layout: check which chicanes existed in 1987, and calibrate `speed_scale`. | P2 |
| Zolder and Diepholz lengths | 1987 Zolder was 4.184 km and Diepholz 2.6 km; the shared 1991 tracks only get a new `length_km`. Check whether the lap time needs a `speed_mult`. | P3 |
| Nürburgring round 7 | Ran 23 laps (round 3: 25). Both use one track id; a placeholder copy would give round 7 its own laps. | P3 |

## 2. Calibration

- **Lap times** · P1: run `python tools/simulate.py dtm-1987 --runs 6` after
  the build and compare the poles with `research/`. The car profiles and
  power ratings in `gen.json` are first guesses from the TCR car sheets.
  1987 cars were slower than the 1991 Evo cars, so the tracks shared with
  1991 may need a `speed_mult` below 1.
- **Make balance** · P1: in 1987 the M3s took the title, the Sierras won
  most races late in the year, and the Mercedes and Alfa were off the pace.
  Check that the simulated points per make look like that.
- **Tyre wear** · P2: no planned stops in 1987. Check that nobody stops in a
  normal dry race.

## 3. Rules

- **Mid-season weight changes** · P1 (wish list B2): BMW M3 +100 kg after
  Zolder; Alfa and Volvo -50 kg; Sierra -100 kg, then +50 kg before the
  Norisring; Mercedes -50 kg at the AVUS. Not possible in the game; the
  round 1 weights are used all year.
- **Success ballast** · P1 (wish list B1): weight penalties on top of the
  base weights. Not possible.
- **Points** · P2 (wish list B3): 1987 paid 18 places and dropped one
  result. The game pays the top ten.
- **Guest entries** · P2 (wish list B9): Ludwig at round 7.
- **Two car models per make** · P2: the BMW 635 CSi teams use a second
  supplier key (`BMW 635`). The wish list needs an entry for several car
  models per make, and for mid-season model changes (König, Reuter,
  Winkelhock and Hahne).

## 4. Entries

- **Colours** · P2: every team colour in `gen.json` is an estimate. Check
  them against 1987 photos.
- **Private entries** · P3: all private drivers share one team. Splitting
  von Löwis, Niederhof and Gröpper into their own teams needs a tool option
  to map entries by driver, not only by entrant.
- **Kissling Motorsport and MK Motorsport** · P3: left out. Add them back if
  the field should show every part-timer.
- **Missing birth dates and numbers** · P3: see `research/season.md`,
  "Unverified".
- **Team histories** · P3: short and partly empty in content. Add facts
  where sources are found (team bosses are not in the sources used).

## 5. Art

- **Car images** · P3: none yet. `tools/car_drawings.py` or
  `tools/car_art.py` with plain team colour liveries; outlines are needed
  for the 635 CSi, Sierra XR4Ti, Volvo 240 Turbo and Alfa 75.
- **Team logos** · P3: `tools/logo_art.py seasons/dtm-1987`. Reuse 1990 and
  1991 logos where the team existed then (Zakspeed, Isert, Alpina).
- **Portraits** · P3: `tools/portrait_art.py`; most drivers will need
  helmet cards.
- **Engine logos** · P3: Volvo, Alfa Romeo and Ford are new suppliers.

## 6. Sounds

Era 1 (1984 to 1992) has no sound overlay yet, so 1987 uses the game's
vanilla sounds. The Group A sounds still need collecting, ideally on an era
1 base that 1987 and 1990 to 1992 all share. The 1987 cars: BMW M3 (S14),
BMW 635 CSi (3.5 L6), Ford Sierra XR4Ti turbo and RS 500 Cosworth, Volvo
240 Turbo, Mercedes 190E 2.3-16, Alfa Romeo 75 Turbo, Rover Vitesse V8 and
Ford Mustang V8. · P3
