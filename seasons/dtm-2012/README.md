# DTM 2012: Season Pack

Status: **v0.1, generated, built and installed; not yet played in-game.**
The data was generated with `tools/season_from_research.py` from
`research/`, configured in `gen.json`. For the sourced facts behind it
(calendar, entry list, standings, rules, sources and unverified points), see
[research/season.md](research/season.md).

2012 was the first season of the new DTM cars: BMW returned with the M3,
Audi raced the A5 and Mercedes the C-Coupé. One race per weekend, two-car
teams, no DRS and no option tyre yet.

**Era base:** 2012 builds on [`bases/dtm-era4`](../../bases/dtm-era4)
(`"base": "dtm-era4"`), like 2013. The rules, tyre and damage tuning,
tracks, engine and tyre logos, generator defaults and the private sounds
come from there. This folder only holds what is 2012's own, and the few
rules where 2012 differs (see below). See
[bases/README.md](../../bases/README.md).

## How it's built

- **Teams and drivers:**
  - 11 two-car teams and 22 drivers from `research/entries.csv`, with the
    real car numbers.
  - Team names follow the entry list. The four Mercedes entries are named
    after their main sponsor: "AMG-Mercedes" (HWA, #5, #6), "Thomas Sabo
    AMG-Mercedes" (HWA, #11, #12), "DHL AMG-Mercedes" (Mücke, #19, #20) and
    "Junge Sterne AMG-Mercedes" (Persson, #23, #24).
- **Ratings:** from the final 2012 standings, with the base's settings
  (average points per car, spread over 55–57.5; driver skill 11–18).
  Schnitzer (Spengler) and Thomas Sabo (Paffett) come out on top.
- **Previous position:** the 2011 teams' standing (Abt Sportsline 1st …
  Persson 8th). The three BMW teams, new in 2012, follow as 9th to 11th in
  car-number order (RMG, Schnitzer, RBM).
- **Rules** (base rules plus `patches/regulations.json`):
  - Points 25-18-15-12-10-8-6-4-2-1, knockout qualifying, no refuelling,
    no ERS, two cars per team, driver aids banned: as in the base.
  - **No DRS** (it came in 2013).
  - **One dry tyre:** `data/tyremodel.json` replaces the base's. The game
    may need a soft compound, and its code can't be checked, so the soft
    stays as an exact copy of the hard and no car starts on it. The
    two-compound rule is off.
  - Minimum weight **1,100 kg** (base: 1,110 kg), so a 955 kg chassis plus
    the game's 145 kg engine.
  - The car profile is the base's (fitted to the 2013 qualifying times),
    renamed "DTM 2012". 2012 lap times aren't calibrated yet.
- **Engines:** the base's three 4.0 V8s, unchanged.
- **Sponsors** (`sponsors` in `gen.json`): read from the drawings. Primary
  is the lower-numbered car's main sponsor, then the team-mate's, then
  partners. Each sponsor can be on one team only (wishlist E12), so Deutsche
  Post (E-Postbrief on Scheider's Audi and Werner's BMW) went to Abt
  Sportsline, and make-wide partners (Puma, Sonax, Würth...) are spread.
- **Tracks:** the base's traced venues, plus **Valencia** (Circuit Ricardo
  Tormo), newly traced into the base (`bases/dtm-era4/track_specs/valencia.json`,
  3,948 m vs 4,005 m). Its speed and tyre wear are first guesses. Race
  distances follow `research/calendar.csv` where they differ from 2013
  (`track_overrides`: Brands Hatch 97, Norisring 78, Zandvoort 43 laps).
  Both Hockenheim rounds use one track at 42 laps; the opener ran 40.
  The Munich stadium show was not a championship round and isn't in the
  calendar.
- **Art:**
  - Cars: drawn by Pappydhorn12 (used with permission, see
    [credits.txt](credits.txt)), cut from the team sheets with
    `tools/car_drawings.py` (`art/drawings.json`). Some sheets have faint
    shadow lines under the cars that joined the tyres to the body, so they
    set `shadow_max`. The other car of each team is in `art/liveries`.
  - Logos: the game shows team logos only as small icons in the team list,
    where they can't be recognised, so each team shows its maker's emblem
    there, as on the 2012-2013 TV timing graphics (`"team_tiles": "maker"`
    in `art/logos.json`). The emblems come from the base: chrome Audi rings,
    the BMW roundel and the chrome Mercedes star, drawn as large as the
    engine logos next to them. The team logos (ABT, HWA and Schnitzer from Commons, the others
    from the author's folders; Persson's SVG is rendered with headless Edge) are still listed in `art/logos.json` and
    built into `build/art/<season>/team_logos/`, but they are not in the
    pack or git: several are the teams' own logos, which aren't freely
    licensed. Hankook's flame sits over its wordmark, so it fills the small
    square the game gives the tyre logo.
  - Portraits: the 18 drivers who also raced in 2013 reuse its hand-picked
    photos. Schumacher, Frey, Coulthard and Wolff have the closest free
    Commons photos the tool found (2016, 2008, 2025 and 2019). Joey Hand
    keeps a helmet card.

## To check

- **Car numbers on two drawings:** Wickens' stern car is drawn as #21 and
  Wolff's TV Spielfilm car as #20. The entry list has #20 and #24. The pack
  uses the entry list, so the numbers on those two images differ from the
  game's.
- Coulthard's portrait is from 2025; a photo closer to 2012 would be better.
- In game: the single dry tyre (does the game cope, do cars stop twice?),
  lap times (base profile, not fitted to 2012), Valencia's speed and wear.

## Simplifications

Game gaps are listed in the
[wish list](../../docs/DEVELOPER_WISHLIST.md):
- **A5:** no Q4 single-lap shootout.
- **B5:** two mandatory stops inside pit windows can't be required; tyre wear
  decides the stops.
- **B7:** no single spec tyre (see Rules).
- **E12:** a sponsor can be on one team only.
- Also C4, D1, D3, D5, D6, D7, E1, E2, E4, E5, E6, E8, E9, as for 2013.
- Pit crews, punctures, cheating and espionage come from the era base, as
  for 2013 (game 0.99.6).

## Rebuild

```bash
python tools/season_from_research.py seasons/dtm-2012
```

```bash
python tools/car_drawings.py seasons/dtm-2012 --source "C:/Users/dan/Pictures/mods/dtm-2012" --preview
```

```bash
python tools/logo_art.py seasons/dtm-2012
```

```bash
python tools/portrait_art.py seasons/dtm-2012
```

```bash
python tools/build_pack.py seasons/dtm-2012 --install
```
