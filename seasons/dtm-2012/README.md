# DTM 2012: Season Pack

Status: **v0.2, lap times and stops tuned in the simulator; not yet played in-game.**
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
    two-compound rule is off. Its wear is 0.03 (the base hard: 0.018), so
    a stint lasts about a third of a race and two stops is the normal
    strategy, as the 2012 rules required. At 0.018 most cars stopped once
    in the simulator.
  - Minimum weight **1,100 kg** (base: 1,110 kg), so a 955 kg chassis plus
    the game's 145 kg engine.
  - The car profile is the base's (fitted to the 2013 qualifying times),
    renamed "DTM 2012". Each track's 2012 pace is set with `speed_mult` in
    `track_overrides` (see "Lap times").
- **Engines:** the base's three 4.0 V8s, unchanged.
- **Sponsors** (`sponsors` in `gen.json`): read from the drawings. Primary
  is the lower-numbered car's main sponsor, then the team-mate's, then
  partners. Each sponsor can be on one team only (wishlist E12), so Deutsche
  Post (E-Postbrief on Scheider's Audi and Werner's BMW) went to Abt
  Sportsline, and make-wide partners (Puma, Sonax, Würth...) are spread.
  Checked against period photos (`research/spotter_guide.csv`,
  `research/liveries.csv`): auto TEST (Scheider's bonnet) joins Abt
  Sportsline, and Samsung (Hand's bonnet and wing) replaces Allgeier at RMG,
  because Allgeier ran on every BMW.
- **Tracks:** the base's traced venues, plus **Valencia** (Circuit Ricardo
  Tormo), newly traced into the base (`bases/dtm-era4/track_specs/valencia.json`,
  3,948 m vs 4,005 m). Race distances follow `research/calendar.csv` where
  they differ from 2013 (`track_overrides`: Brands Hatch 97, Norisring 78,
  Zandvoort 43 laps). Both Hockenheim rounds use one track at 42 laps; the
  opener ran 40. The Munich stadium show was not a championship round and
  isn't in the calendar.
- **Track maps:** the eight venues 2012 shares with 2013 use copies of the
  2013 race-day images (`assets/tracks/`) and their art-matched track files
  (`tracks/`, listed in `track_art.json`). The layouts didn't change, so the
  cars run on the drawn track, but the trackside branding is 2013's.
  Valencia keeps the base's OSM map and file. That map isn't in the
  race-day frame, so `tools/map_check.py` finds most of the lap off the
  drawn track there. race-tracks has a 2012 Valencia plan
  (`dist/styles/plan/valencia/gp@2005.png` with an image brief) ready for a
  race-day image.
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
    keeps a helmet card. Feeder drivers and free agents: eight reuse their
    2013 picks (Juncadella, Wehrlein, Estre...), the tool found photos for
    most others, and 48 have helmet cards. These are the tool's picks, not
    checked by hand yet.
  - Team dashboards: every team shows the Oschersleben start photo (Jörg /
    Spieler Family, used with permission, 2013 like the DTM 2013 pack's
    `<team>4.jpg`) as `assets/dashboard_bgs/<team>.jpg`. The permissions
    granted for 2013 (Spieler, Dennis de Wolde) cover every year.
  - Main menu and the spectator dashboard set: still the base's. The 2012
    photo collection is in the image gallery outside the repo
    (`Pictures/mods/dtm-2012/teams/`, viewer in `dtm-2012-gallery/`), the
    picks in `research/photo_candidates.md`. The edits wait for ChatGPT
    image editing, see [the backlog](../../docs/plans/DTM2012_BACKLOG.md).

## Feeder series

`data/junior_series.json` holds five real 2012 series, generated from
`research/juniors/` (entries, teams, calendar and standings per series,
with a dossier `.md` each), in the same slots and with the same settings as
2013 (`juniors` in `gen.json`):

| Series | Tier | Champion |
|---|---|---|
| Formula 3 Euro Series (F3ES) | 2 | Daniel Juncadella |
| Porsche Carrera Cup Deutschland (PCCD) | 2 | René Rast |
| ATS Formel 3 Cup (GF3) | 3 | Jimmy Eriksson |
| ADAC Formel Masters (AFM) | 4 | Marvin Kirchhöfer |
| ADAC Procar Series (PRO), the Deutsche Tourenwagen Challenge | 3 | Jens-Guido Weimann (Division 1), Guido Thierfelder (Division 2) |

The F3 slot uses the Euro Series table, not the FIA F3 European
Championship's: the FIA one added two British F3 weekends and counted
only some races (see `research/juniors/f3_euro.md`). Rast, Weimann and
Thierfelder are older than the series' age bands, so they are left out, as
2013 left out the older gentlemen. Six hand-rated free agents
(`research/juniors/free_agents.csv`): Wittmann (BMW test driver), Sutil,
di Grassi, Alguersuari, Buemi and van der Zande. Unlike 2013's ex-F1 free
agents, all but Sutil are young enough to take a feeder seat while unsigned.

## Lap times

The real 2012 qualifying and race results are in `research/results/`
(official timing sheets saved on archive.org for most rounds, plus
racingyears.com; sources in its README). Every qualifying was dry except
Zandvoort (damp at the start, then drying). The car profile is the base's;
each track's 2012 pace is a `speed_mult` in `track_overrides`, fitted to
the real poles with `tools/simulate.py` (4 seasons per step). 2012 cars come
out about 1 to 3% slower than 2013's, except at Brands Hatch.

Three rounds of 4 simulated seasons (2026-11-12):

1. Base profile and the base's per-track tyre wear: poles 0.2 to 3.2% too
   fast (Valencia 2.6% too slow), and most cars stopped once.
2. After the first `speed_mult` fit and the 2012 tyre wear (0.03): poles
   within 1.6%, but tracks tuned for 2013's soft-plus-hard stints gave three
   stops (Hockenheim, Nürburgring) or one (Norisring).
3. With 2012's own `tyre_wear_mult` per track (in `track_overrides`, e.g.
   Hockenheim 1.5, Nürburgring 1.3, Norisring 0.75): every pole within 1%
   of 2012 (Valencia +0.9%, the Nürburgring -1.0%), and 66% of cars
   stopped twice, 21% once, 9% three times. Valencia (24% three stops) and
   Zandvoort (38% one stop) are the least even.

**Team strength:** Schnitzer took 26% of the points (real 18%) and Thomas
Sabo 22% (real 17%), even after Schnitzer's car rating went down by hand
(`rating` 56.8 in `gen.json`). Spengler wins about 2 to 3 races a season
(real 4); the Audis (Mortara, Ekström) score a little low.

## To check

- **Car numbers on two drawings:** the drawings are wrong. Period photos
  show Wickens' stern car as #20 and Wolff's TV Spielfilm car as #24, as in
  the entry list and the pack (`research/spotter_guide.csv`). The drawings
  show #21 and #20. Other drawing slips: Merhi has a German flag (he is
  Spanish), Tambay an Italian one (French), and Wolff's car had a Scottish
  flag, not a Union flag.
- Coulthard's portrait is from 2025. Free 2012 photos exist (Tom Bayly,
  Brands Hatch 2012, CC BY-SA 2.0; see `research/photo_candidates.md`).
  Also 2012 photos for Schumacher and Wolff.
- In game: the single dry tyre, two stops, Valencia, and whether Schnitzer
  and Thomas Sabo are as strong as in the simulator.

## Simplifications

Game gaps are listed in the
[wish list](../../docs/DEVELOPER_WISHLIST.md):
- **A5:** no Q4 single-lap shootout.
- **B5:** two mandatory stops inside pit windows can't be required; tyre wear
  decides the stops.
- **B7:** no single spec tyre (see Rules).
- **A3:** the Norisring and Zandvoort races were stopped at the 75-minute
  limit after 78 and 43 laps (scheduled most likely 82 and 44). The pack
  uses the laps run; the game always runs the full lap
  count.
- **C6:** the timing codes are in `research/spotter_guide.csv` only.
- **C7:** feeder series race once a weekend (F3 and Formel Masters ran 3).
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
