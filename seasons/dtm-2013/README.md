# DTM 2013: Season Pack

Status: **v0.2, one full season played in-game, lap times calibrated.** The data was generated
with `tools/season_from_research.py` from `research/`, configured in
`gen.json`. For the sourced facts behind it (calendar, entry list, standings,
rules, sources and unverified points), see
[research/season.md](research/season.md).

2013 is the season whose rules match the game best: one race per weekend,
two-car teams, DRS, a mandatory option tyre and knockout qualifying.

## How it's built

- **Teams and drivers:**
  - 11 two-car teams and 22 drivers from `research/entries.csv`, with the real
    car numbers.
  - Team names follow the entry list. The two HWA AG entries are
    "Euronics AMG-Mercedes" (#3, #4) and "STIHL AMG-Mercedes" (#9, #10).
- **Ratings, skills and salaries:** estimated from the final 2013 standings.
  Car ratings come from each team's average points per car
  (`team_rating_from: average`) and are spread over 55–57.5 (`rating_range`),
  because the three makes were close. Driver skill is spread over 11–18
  (`skill_range`). A first version rated each car from its team's best
  driver over 50–60; in the test season the champions' team-mates (Molina,
  Hand) then scored three to five times their real points. With 53–58 and
  10–19 (season 5) the four top teams still took 80% of the points
  (real: 58%) and Rockenfeller won 6 of 10, so both ranges were narrowed.
  These are estimates, not history.
- **Rules** (`rules: "own"` in `gen.json`, see `patches/regulations.json`):
  - Points 25-18-15-12-10-8-6-4-2-1 (the game's `modern_top10`).
  - Knockout qualifying. The real Q4 single-lap shootout of the top 4 isn't
    in the game.
  - DRS enabled, no refuelling, no ERS, two cars per team, driver aids banned.
  - Physical safety car only: there was no VSC or full-course yellow in 2013.
  - A `dtm_2013` car profile (corner 1.13, acceleration 0.5, braking 1.0,
    drag 1.5; the game allows 0.5–1.5). It was fitted with the game's own
    physics model to the 2013 qualifying times. Acceleration and drag sit at
    the game's limits to keep top speeds down (see "Lap times").
  - Minimum chassis mass 965 kg. The game adds the engine mass (145 kg) on
    top, for the real 1,110 kg. No success ballast.
- **Engines:** Audi 4.0 V8, BMW P66 4.0 V8 and Mercedes-AMG 4.0 V8 as works
  partners with near-equal ratings. BMW is rated a little higher (it won the
  2013 manufacturers' title).
- **Tyres:** Hankook only. `data/tyremodel.json` makes the soft the option
  tyre (about 2% more grip, quick wear) and the hard the standard tyre, plus
  the wet. There was no medium, so it is removed (a `null` in the merged
  file; the game takes its compounds from this file and treats any other
  compound name as the default, the hard). `formula_compound_usage` forces
  both compounds in a dry race.
- **Sponsors** (`sponsors` in `gen.json`): each team starts with its real
  2013 sponsors from the liveries (`research/spotter_guide.csv`,
  `research/liveries.csv`): the lower-numbered car's main sponsor as
  primary, the team-mate's next, then partners seen on the team's cars
  (Schnitzer: BMW Bank, Puma, H&R; Phoenix: Schaeffler, TAG Heuer). The
  manufacturers' own campaigns (bmw.com/m3, AMG, Audi ultra, Audi Cup) and
  the series partners (DEKRA, ADAC, Hankook) are left out. `build_pack.py`
  swaps them in for the vanilla deals each team inherits from its clone.
  Every real sponsor keeps the slot, contract length, rating and money of
  the deal it replaces (left-over money goes to the primary), so sponsor
  income is unchanged from v0.2. The replaced fictional sponsors leave the
  pool; the other 29 stay as the free market for later seasons. Names are
  used descriptively only; there are no sponsor logos.
- **Economy:** budgets and salaries use the game's currency at the scale of
  the other packs, so the game's development and part costs still work. They
  aren't real euros. Top driver salaries are capped at 2.5 (DTM scale), not F1
  levels.
- **Tracks:** 8 new venues traced from OpenStreetMap (`track_specs/`), plus
  the 1991 Norisring (`shared_tracks`). Each new spec sets `race_laps` to
  the scheduled 2013 distance (`research/calendar.csv`, all about 190 km or
  70 minutes; the Nürburgring 49 laps, of which the wet race ran 45) and one
  DRS zone (`drs_zones`) on the longest straight. Zandvoort has none: DRS wasn't used there in 2013.
- **Art:**
  - Cars: layered liveries drawn on our own outlines of the three cars, traced
    from Commons photos (`art/*_trace.json`, `art/cars.json`, see
    [credits.txt](credits.txt)). The colours and sponsor positions were read
    from period photos and Andy Blackmore's 2013 spotter guide. The guide was
    used as a reference only: no part of it is in the pack.
    `research/liveries.csv` lists the 22 liveries. The game shows one car per
    team, so each team image is its lower-numbered car.
  - Logos: public-domain Commons logos for Abt, HWA and Schnitzer, crests for
    the other teams, and the Audi, BMW and Mercedes-Benz logos in use in 2013
    (`art/logos.json`).
  - Portraits: free Commons photos where they exist (`art/portraits.json`).

## Tracks

| Venue | 2013 length | How it's built | Traced |
|---|---|---|---|
| Hockenheim | 4.574 km | Raceway loop over OSM circuit relation 284588 (today's GP circuit) | 4,517 m (−1.2%) |
| Brands Hatch Indy | 1.929 km | Raceway loop over the Indy circuit relation 11248425 | 1,906 m (−1.2%) |
| Red Bull Ring | 4.326 km | Raceway loop over relation 5309181, without the MotoGP additions | 4,269 m (−1.3%) |
| Lausitzring | 3.478 km | Via: the DTM short course, with the Turn 1 hairpin at the end of the front straight (a hand-placed bridge: OSM maps it only as a junction) and the 2007 Kurzanbindung hairpin, counter-clockwise as OSM tags it | 3,388 m (−2.6%) |
| Norisring | 2.300 km | Shared from 1991 | 2,207 m (−4%) |
| Moscow Raceway | 2.555 km | Via: the full circuit's way with the link that cuts the southern section | 2,550 m (−0.2%) |
| Nürburgring Sprint | 3.629 km | Via: the 1992 sprint route with the Mercedes Arena, the Kurzanbindung and the Formula 1 version of the NGK/Veedol-Schikane (sharp left, then a long right; way 1149161211) | 3,560 m (−1.9%) |
| Oschersleben | 3.696 km | Raceway loop | 3,626 m (−1.9%) |
| Zandvoort | 4.307 km | Raceway loop over today's (post-2020) layout | 4,205 m (−2.4%) |

**Open questions:**
- Moscow: 2.555 km (fan wiki) vs 2.661 km (racingyears). The traced short
  layout fits 2.555 km.
- Start lines at Moscow, Nürburgring, Oschersleben and Zandvoort are placed
  by hand on the pit straight (the game puts the pits at the start line).
- Lausitzring: the DTM used the short infield course from 2005 and the
  banked oval Turn 1 only again from 2019. The first trace took the GP
  course's wide Turn 1 sweep, which made the lap 14.5% too fast; the
  infield course fits both the length and the 2013 pole.
- Norisring: the 1991 tracing needs a speed factor of 1.26 for 2013 cars
  (`speed_mult` in its track override).
- Nürburgring: OSM has two ways through the NGK/Veedol-Schikane. The one it
  names "NGK-Schikane" (way 820679450) is an even S, which looks like the
  motorcycle and 24-hour variant built in 1997. The other is a sharp left
  and a long right, like the V on the 2013 circuit map, so the trace uses
  that one as the Formula 1 chicane. Until season 7 the trace took the S;
  the F1 chicane adds about 2 s to the model lap, so `speed_scale` went
  from 0.94 to 0.978.

## Simplifications

The game features these would need are in the
[developer wish list](../../docs/DEVELOPER_WISHLIST.md) (item numbers in
brackets).

- **Two mandatory pit stops** can't be forced (B5). Tyre wear
  (`tyre_wear_mult`, scaled by race laps) is set so that two stops is the
  fastest strategy: in season 5, 160 of 220 cars stopped twice.
- **DRS** was free once per lap anywhere on the track in 2013, in the race
  only (B6). The game uses zones, so each track has one zone on its longest
  straight. It opens DRS from lap 3 and in qualifying too. The real ban on
  the last 3 laps isn't modelled.
- **Qualifying:** the game's Q1/Q2/Q3 knockout. There's no Q4 shootout (A5).
- **Option tyre:** the rule was one set per race. The game asks for two
  different dry compounds (B7).
- **Top speeds** come out about 10 km/h high: the car profile is at the
  game's limits for drag and acceleration (D5).
- **Development:** chassis and aero were homologated, but in the game teams
  still develop at different rates during the season (C4, D7).
- **Parts** keep the game's open-wheel slots under touring-car names: front
  splitter, rear wing, underbody, diffuser, side bodywork, monocoque (D1).
  Bodywork wears little per lap; contact is what damages it.
- **Damage:** a damaged front end was driven home, not swapped at a stop.
  The game's repair at a stop isn't in the data (D6), so lap-one pile-ups
  never break the front wing and contact damages parts half as much as vanilla.
- **Time-limited races:** the wet Nürburgring and final Hockenheim races
  were stopped at 75 minutes, after 45 of 49 and 41 of 42 laps. The game
  always runs the full lap count (A3). In season 6 the dry races took 66–77
  minutes, against 69–75 for the real dry races.
- **Pits** are at the start line, so four start lines sit on the pit
  straight (E5).
- **Wet races:** the Nürburgring and the final Hockenheim were rain races
  in 2013, which is why their race times are slow; qualifying was dry, so
  the poles still calibrate the dry pace. The game rolls the weather per
  track (base chance of a wet race 5%, the Nürburgring 1.4×), so these
  rounds are usually dry in the game.
- **Driver codes:** the three-letter timing codes (SPE, WER, TSC...) are in
  `research/spotter_guide.csv`; the game has no field for them (C6).
- **One car image per team:** team-mates' different liveries, Abt
  Sportsline's red (#11) and yellow (#12) mirrors and Wehrlein's one-off
  VfB Stuttgart design can't be shown (E4).
- **Sponsors:** make-wide partners (Puma, Sonax, Würth, Petronas...) ran on
  every car of a make; here each is on one team (E12). Sponsor money is the
  vanilla deals' and not real (E6).
- **Norisring:** Ekström's disqualification (no winner) is history, not a rule.

## Lap times

The real 2013 qualifying and race results are in `research/results/`
(sources in its README). The calibration ran in two steps:

1. The game's physics model (its `RealisticPhysicsModel`, run offline on our
   track files) gives a neutral car's lap. In the test season every pole was
   0.927 of that model lap, within ±0.7% on all nine tracks, so the model
   predicts the game.
2. The car profile was fitted to the poles, then each track's remaining
   error went into its `speed_scale` (Norisring: `speed_mult`).
3. Season 5 poles were all within 0.8% of 2013 (0.927–0.935 of the model
   lap). The profile was refitted at acceleration 0.5 and each track's scale
   set from its own season-5 ratio: Hockenheim 1.091, Brands Hatch 0.987,
   Red Bull Ring 1.088, Lausitzring 1.046, Norisring 1.29, Moscow 1.132,
   Nürburgring 0.94 (0.978 with the F1 chicane), Oschersleben 1.014,
   Zandvoort 1.014.

Predicted poles match 2013 to within 0.1%. The narrower team ratings make
the top car a little slower, so in-game poles may come out a few tenths slow.

**Top speeds** come out high. Season-5 qualifying traps were 285 km/h at
Hockenheim, 280 at the Lausitzring and the Norisring and 267 at Zandvoort.
The game opens DRS in qualifying too (8 km/h), and drag can't go above 1.5.
Acceleration 0.5 takes about 2.5% off (an estimated 278 at Hockenheim).

## Still to check in-game

Season 6 (after the refit) had every pole within 0.4% of 2013, five
different winners (2013: seven) and team point shares within a few points
of 2013, except STIHL AMG (20% vs 15%) and Schnitzer (6% vs 11%).

Season 7 had seven different winners like 2013, poles within 0.8% and
races of 68–77 minutes. Farfus took 8 of 10 poles (in 2013 nobody took more
than two). STIHL AMG (23%) and Schnitzer (5%) were off again, so their car
ratings were swapped by hand (`rating` in `gen.json`: STIHL 56.9, Schnitzer
57.3). Nine cars one-stopped at the Norisring and five at Brands Hatch, both
after a safety car, so their wear went back up a little (0.65, 0.45).

- Top speeds: about 2.5% lower than season 5 (not measured since).
- The Nürburgring lap with the F1 chicane.
- Two stops at the long races. In seasons 5 and 6 most finishers stopped
  three times or more at Brands Hatch (98 laps), Moscow (74) and the
  Norisring (83), so their tyre wear went down to 0.4, 0.55 and 0.58. In
  season 6, 15 cars one-stopped at Oschersleben after a safety car, so its
  wear went up to 1.25.

## Rebuild

```bash
python tools/season_from_research.py seasons/dtm-2013
```

```bash
python tools/osm_track.py seasons/dtm-2013/track_specs/*.json
```

```bash
python tools/car_art.py seasons/dtm-2013 --preview
```

```bash
python tools/logo_art.py seasons/dtm-2013
```

```bash
python tools/portrait_art.py seasons/dtm-2013
```

```bash
python tools/build_pack.py seasons/dtm-2013 --install
```
