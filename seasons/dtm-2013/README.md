# DTM 2013: Season Pack

Status: **v0.1, generated, not yet tested in-game.** The data was generated
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
  Team ratings are spread over 50–60 (`rating_range`) because the three makes
  were close. These are estimates, not history.
- **Rules** (`rules: "own"` in `gen.json`, see `patches/regulations.json`):
  - Points 25-18-15-12-10-8-6-4-2-1 (the game's `modern_top10`).
  - Knockout qualifying. The real Q4 single-lap shootout of the top 4 isn't
    in the game.
  - DRS enabled, no refuelling, no ERS, two cars per team, driver aids banned.
  - A `dtm_2013` car profile (corner 0.9, acceleration 0.74, braking 0.78,
    drag 1.18): a first guess, to be calibrated.
  - Minimum chassis mass 965 kg. The game adds the engine mass (145 kg) on
    top, for the real 1,110 kg. No success ballast.
- **Engines:** Audi 4.0 V8, BMW P66 4.0 V8 and Mercedes-AMG 4.0 V8 as works
  partners with near-equal ratings. BMW is rated a little higher (it won the
  2013 manufacturers' title).
- **Tyres:** Hankook only. `data/tyremodel.json` makes the soft the option
  tyre (about 2% more grip, quick wear) and the hard the standard tyre. The
  game's medium is rated like the hard, and no car starts on it.
  `formula_compound_usage` forces both compounds in a dry race.
- **Economy:** budgets and salaries use the game's currency at the scale of
  the other packs, so the game's development and part costs still work. They
  aren't real euros. Top driver salaries are capped at 2.5 (DTM scale), not F1
  levels.
- **Tracks:** 8 new venues traced from OpenStreetMap (`track_specs/`), plus
  the 1991 Norisring (`shared_tracks`). Each new spec sets `race_laps` from
  `research/calendar.csv` and one DRS zone (`drs_zones`) on the longest
  straight. Zandvoort has none: DRS wasn't used there in 2013.
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
| Lausitzring | 3.478 km | Via: the GP course with the 2007 Kurzanbindung hairpin, counter-clockwise as OSM tags it | 3,424 m (−1.6%) |
| Norisring | 2.300 km | Shared from 1991 | 2,207 m (−4%) |
| Moscow Raceway | 2.555 km | Via: the full circuit's way with the link that cuts the southern section | 2,550 m (−0.2%) |
| Nürburgring Sprint | 3.629 km | Via: the 1992 sprint route with the Mercedes Arena | 3,555 m (−2%) |
| Oschersleben | 3.696 km | Raceway loop | 3,626 m (−1.9%) |
| Zandvoort | 4.307 km | Raceway loop over today's (post-2020) layout | 4,205 m (−2.4%) |

**Open questions:**
- Lausitzring: did DTM 2013 take the banked Turn 1 or the infield T1–T5? The
  banked variant is the one that fits the length.
- Moscow: 2.555 km (fan wiki) vs 2.661 km (racingyears). The traced short
  layout fits 2.555 km.
- Start lines at Moscow, Nürburgring, Oschersleben and Zandvoort are placed
  by hand on the pit straight.

## Simplifications

- **Two mandatory pit stops** can't be forced. Tyre wear (`tyre_wear_mult`,
  scaled by race laps) is set so that about two stops should be the fastest
  strategy. This needs an in-game check.
- **DRS** was free once per lap anywhere on the track in 2013. The game uses
  zones, so each track has one zone on its longest straight. The game opens
  DRS from lap 3. The real ban on the last 3 laps isn't modelled.
- **Qualifying:** the game's Q1/Q2/Q3 knockout. There's no Q4 shootout.
- **Option tyre:** the rule was one set per race. The game asks for two
  different dry compounds.
- **Norisring:** Ekström's disqualification (no winner) is history, not a rule.

## Still to check in-game

- DRS opens, the option tyre gets used, and races have about two stops.
- Qualifying runs as knockout.
- Lap times: every `speed_scale` starts at 1.0. Calibrate with
  `tools/calibrate.py` against the 2013 poles. The real pole times aren't in
  `research/` yet: collect them first, as in `seasons/dtm-1991/research/results/`.

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
