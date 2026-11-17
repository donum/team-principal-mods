# DTM 2013: Season Pack

Status: **v0.3 on the Steam Workshop since 2026-11-16, item [3834059242](https://steamcommunity.com/sharedfiles/filedetails/?id=3834059242). Workshop text in [workshop_description.txt](workshop_description.txt), preview [workshop_preview.jpg](workshop_preview.jpg).** For an update, reconnect the game's publisher to that item ID. The data was generated
with `tools/season_from_research.py` from `research/`, configured in
`gen.json`. For the sourced facts behind it (calendar, entry list, standings,
rules, sources and unverified points), see
[research/season.md](research/season.md).

2013 is the season whose rules match the game best: one race per weekend,
two-car teams, DRS, a mandatory option tyre and knockout qualifying.

**Era base:** 2013 builds on [`bases/dtm-era4`](../../bases/dtm-era4) (`"base": "dtm-era4"`),
which holds what every 2012–2018 season shares: the rules, the tyre and
damage tuning, the traced tracks, the engine and tyre logos, the generator
defaults and the engine sounds. They were tuned on 2013. This folder keeps
only what is 2013's own: teams, drivers, sponsors, calendar, car images,
team logos and portraits. See [bases/README.md](../../bases/README.md).

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
- **Previous position:** each team's `previous_position` in `gen.json` is its
  2012 teams' standing (Schnitzer 1st … Mücke 10th), not its 2013 result.
  MTEK, new in 2013, is last (11th). See research/season.md.
- **Rules** (`rules: "own"` in the base's `gen.json`, see the base's
  [`patches/regulations.json`](../../bases/dtm-era4/patches/regulations.json)):
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
- **Tyres:** Hankook only. The base's `data/tyremodel.json` makes the soft the option
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
- **Tracks:** 8 new venues traced from OpenStreetMap (the base's `track_specs/`), plus
  the 1991 Norisring (`shared_tracks`). Each new spec sets `race_laps` to
  the scheduled 2013 distance (`research/calendar.csv`, all about 190 km or
  70 minutes; the Nürburgring 49 laps, of which the wet race ran 45) and one
  DRS zone (`drs_zones`) on the longest straight. Zandvoort has none: DRS wasn't used there in 2013.
- **Art:**
  - Cars: drawn by Pappydhorn12 (used with permission, see
    [credits.txt](credits.txt)) and cropped from their team sheets with
    `tools/car_drawings.py` (`art/drawings.json`). The tool keeps the tyres,
    wheel-arch gaps and the black underfloor (splitter, diffuser), gives
    each car its whole antenna where it reaches into the car above on a
    sheet, and stands every car's tyres on the same ground line (y=720), so
    the image doesn't jump between teams in the menus. Checked against the
    2013 spotter guide on 2026-11-07: every livery matches, with two small
    text differences: #23's name panel read "T. Schneider", which the tool
    corrects to Scheider (an `edits` entry), and #5 has SCHAEFFLER on the
    rear quarter where the guide shows PLAYBOY. The first
    sheet named Schnitzer holds the 2013 RBM cars, which are used for RBM;
    the corrected Schnitzer sheet is saved as `BMW_Team_Schnitzer_1_2.png`.
    The sheet named RBM shows 2014 cars (BMW M4, Farfus in BMW Bank colours)
    and isn't used.
  - Placeholder cars (`tools/car_art.py`, no longer shipped; it skips every
    team in `drawings.json`): layered liveries drawn on our own outlines of the three cars, traced
    from Commons photos (`art/*_trace.json`, `art/cars.json`, see
    [credits.txt](credits.txt)). The colours and sponsor positions were read
    from period photos and Andy Blackmore's 2013 spotter guide. The guide was
    used as a reference only: no part of it is in the pack.
    `research/liveries.csv` lists the 22 liveries. The game shows one car per
    team, so each team image is its lower-numbered car.
  - Logos: the game shows team logos only as small icons in the team list,
    where they can't be recognised, so each team shows its maker's emblem
    there, as on the 2012-2013 TV timing graphics (`"team_tiles": "maker"`
    in `art/logos.json`). The emblems come from the base: chrome Audi rings,
    the BMW roundel and the chrome Mercedes star, drawn as large as the
    engine logos next to them. The team logos (ABT, HWA and Schnitzer from Commons, the others
    from the author's folder, MTEK without the BMW roundel) are still listed in `art/logos.json` and
    built into `build/art/<season>/team_logos/`, but they are not in the
    pack or git: several are the teams' own logos, which aren't freely
    licensed. Hankook's flame sits over its wordmark, so it fills the small
    square the game gives the tyre logo.
  - Portraits: free Commons photos where they exist (`art/portraits.json`).
    Every photo is picked by hand and pinned (`"pinned": true`). Most come
    from Stefan Brending's (2eight) photos of the 2014 Hockenheim finale,
    the closest free set to 2013. All heads are cropped to the same size
    (2.4 face widths, `FACE_SPAN` in `tools/portrait_art.py`). Wickens,
    Scheider and Priaulx only have tight close-ups, so their heads are
    larger. Joey Hand has a helmet card: no free photo shows him clearly.
  - Main menu: `assets/title_bg.png`, the field at Zandvoort 2013 (Kevin
    McGill, CC BY-SA 2.0; fence removed and extended to 16:9) with the
    2000-2016 DTM wordmark (`art/title_logo.png`, public-domain text logo)
    at the top right. Built by `tools/menu_art.py` from the `zandvoort`
    entry in `art/menu.json`. It has a free licence (`"in_pack": true`), so
    it ships in the pack and replaces the private BMW press photo, which
    `build_pack.py` no longer copies over it.
  - Team dashboards: `assets/dashboard_bgs/`, 23 photos, one to three
    per team, from the 2013 race weekends: Mark Seymour (CC BY 2.0), Kevin McGill
    (CC BY-SA 2.0) and Dennis de Wolde, InMotion Photos (used with
    permission, credit by name and a link). Each was extended to 16:9 and
    touched up with ChatGPT image editing (fences, watermarks and stray
    text removed), then the car was moved into the strip the dashboard
    leaves visible (below the info cards, right of the sidebar). JPEG at
    1672x941, the game's own size. The sources and every edit are listed
    in the image gallery outside the repo (`backgrounds-gpt/manifest.json`)
    and per file in [credits.txt](credits.txt). Ten more are left out for
    now: moving the car left a blurred band at the top and left, which the
    week-advance screen shows. They are flagged "Redo" in the gallery.
  - Oschersleben start, for every team: the field in the first corners,
    15 September 2013, seen from the stands (Jörg / Spieler Family, used
    with permission, credit by name and a link). Every team gets it as
    `<team>4.jpg`; slots 1 to 3 stay for the team's own photos. Built from
    the Flickr original (IMG_7144, 3903x1281): 16:9 crop at full height
    from 28% of the width, Lanczos to 1672x941, unsharp mask before
    (r 2.0, 60%) and after (r 0.8, 70%) the resize, contrast 1.07, colour
    1.08. Three more shots from the same start are in the gallery
    (`teams/_series/permission_spieler/`), left out for now.
  - Spectator dashboard: `assets/dashboard_bg.png` to `dashboard_bg12.png`,
    one livery per team (PNG copies of team backgrounds) and the
    Oschersleben photo as number 4. List in [credits.txt](credits.txt).
    The game shows this set when there is no player team, and they replace
    the vanilla pictures. Copy a team file again when it is redone.

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

**Track maps.** The overview images in `assets/tracks/` are clean
empty-venue illustrations from the race-track-themes project (style
`illustrated-realism`, stage C1: a quiet weekday, no people, no logos), one
per venue at the game's 1044×1080. Hockenheim uses one image for both rounds.

ChatGPT Images painted them with one generic prompt for every track
(race-track-themes `prompts/stages/c1-venue.txt`) from the race-tracks
`plan-natural` plan: every surface in its natural colour, the pit lane in
track asphalt with the traced pit-entry and pit-exit paint. race-track-themes'
`tools/align_track_art.py` aligned each image to the plan's racing line, and
`tools/line_overlay.py` then drew the white lines (track edges, pit-lane edges,
pit paint) crisp and smooth on top. All nine are in the race-tracks plan
frame, so `tools/art_track.py` writes every track file from the race-tracks
centreline (`track_art.json`); the speed scales keep the reference laps, and
`tools/map_check.py` finds no part of any lap off the drawn track. Revisions
used (2026-11-13, `final.png`): Hockenheim round-01 r0027, Brands Hatch r0032,
Red Bull Ring r0014, Lausitzring r0010, Norisring r0010, Moscow r0013,
Nürburgring r0011, Oschersleben r0010, Zandvoort r0014.

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

## Feeder series

`data/junior_series.json` holds five real 2013 series, generated by
`tools/season_from_research.py` from `research/juniors/` (entries,
teams, calendar and standings per series, with a dossier `.md` each):

| Series | Tier | Champion |
|---|---|---|
| FIA Formula 3 European Championship (F3EU) | 2 | Raffaele Marciello |
| Porsche Carrera Cup Deutschland (PCCD) | 2 | Kévin Estre |
| ATS Formel 3 Cup (GF3) | 3 | Marvin Kirchhöfer |
| ADAC Formel Masters (AFM) | 4 | Alessio Picariello |
| Deutsche Tourenwagen Challenge (DTC), the ADAC Procar series, called Deutscher Tourenwagen Cup from 2016 | 3 | Jens-Guido Weimann (Division 1), David Griessner (Division 2) |

Skills, talent, team quality and starting licence points are estimates
from the 2013 points (ranges in `gen.json` `juniors`). A driver who raced
in two series is placed in the one where they did most rounds; one-round
guests are left out. Every feeder stops at age 28 (Formel Masters at 20,
F3 Europe at 26), so the ex-F1 free agents can only sign in DTM. Older
gentleman drivers are left out for the same reason, among them the DTC
champion Weimann, and their seats go to free drivers the game picks. The DTC's Super 1600 class (Division 2) counts its
points at 70%. `driverslicense.json` matches the five series, so a
race seat still needs 10 licence points. Six hand-rated free agents join
them (`research/juniors/free_agents.csv`): Petrov, Kubica, Kovalainen and
di Grassi (no F1 seat in 2013), and the Red Bull juniors Félix da Costa
and Sainz. The game favours free agents, so the list is kept short. Da
Costa and Sainz fit the F3 age bands, so while unsigned they may race in
a feeder.

## Simplifications

The game features these would need are in the
[developer wish list](../../docs/DEVELOPER_WISHLIST.md) (item numbers in
brackets).

- **Later seasons** follow the real grid (`docs/teams`): ART joins in 2015,
  BMW Team RMR and a third HWA team in 2017, Aston Martin (R-Motorsport) and
  Audi Sport Team WRT in 2019, Orlen Team ART in 2020. MTEK, Schnitzer,
  Mücke and ART leave after 2016, Mercedes after 2018. The game keeps at
  least 10 teams (C10), so Audi Sport Team Abt stays from 2017 and one
  R-Motorsport team stays in 2020. Audi and BMW don't leave after 2020.
  Each joining team has its own history text and its real team principal
  (Vasseur at ART, Fritz at HWA, Kamelger and Bänziger at R-Motorsport,
  Vosse at WRT, Philippe at Orlen Team ART), signed to the team before it
  debuts. RMR's two real bosses already run RMG and RBM, so it has a
  made-up principal. Staff are hired on the market at debut.
- **Title sponsors** stay in the Mercedes team names, even when the deal
  ends (C11).
- **Feeder series** race once per weekend (C7). F3 and Formel Masters ran
  3 races, and the Carrera Cup, German F3 and the DTC 2. Each uses its main
  points table without bonus points, and results ignore the track. The
  DTC's two classes race as one field.
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
- **Series logo** is drawn into the menu photo, as a pack can't add its
  own logo. The game cuts the photo to fit the window, so the "DTM 2013"
  wordmark sits lower than it would on a real poster, to stay visible
  from 16:10 to 21:9 windows (E21).
- **Pass-bys** play at the finish line only. At the Norisring, Zandvoort,
  Brands Hatch, Hockenheim and Oschersleben the fans also hear the cars a
  second time, on the back straight or behind the pits; in the
  game that part of the lap is silent (E22).
- **Norisring:** Ekström's disqualification (no winner) is history, not a rule.
- **Pit crews** (game 0.99.6): team-mates share one crew, so a car that
  arrives while its team-mate is being serviced waits. We keep that on: later
  DTM rules banned double-stacking team-mates under the safety car, which only
  matters with one crew per team. Not confirmed for 2013.
- **Punctures** (game 0.99.6) are on at the game's rates, with contact a
  little likelier to cause one (4%). As in 2013, a stop for a puncture is
  just another stop, since the game doesn't count mandatory stops (B5).
- **Cheating and espionage:** 2013 had no such cases. AI teams fit banned
  aids at a fifth of the vanilla rate, and only one espionage operation per
  season is possible across the grid.
- **Language:** team texts are English only. The game is translated into seven languages, but a pack cannot add its own translations yet, so our texts show in English (E13).

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
after a safety car, so their wear went back up a little (0.65, 0.45). Later
rounds settled on 0.57 and 0.42.

After the v0.3 test season (2026-11-16) one-stoppers still won at Brands
Hatch, Moscow and the Norisring, most of all after a safety car. The game
can't require two stops, and short tracks get a simpler AI pit planner (see
the wishlist, B5). Eight single races per track (`simulate.py --track`) with
Brands Hatch at 0.46 and the Norisring at 0.61: one-stoppers in clean races
fell from about 20% to 2 to 3%, and 13 of 16 winners stopped twice (before:
17 of 44 won on one stop). About half the field now stops three times.
Moscow stays at 0.68: its one-stoppers come after a safety car, and more wear
only adds three-stoppers.

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
python tools/osm_track.py bases/dtm-era4/track_specs/*.json
```

```bash
python tools/car_art.py seasons/dtm-2013 --preview
```

```bash
python tools/car_drawings.py seasons/dtm-2013 --preview
```

Main menu background: a BMW press photo (`art/menu.json`; Hockenheim in use,
the Nürburgring photo held back, `"use"` picks one), placed against the right
edge so the cars sit beside the menu. It is not under
a free licence, so it goes to `private/menu_art/` and only onto a local install
(`build_pack.py --install`), never into `dist/` or the Workshop upload.

```bash
python tools/menu_art.py seasons/dtm-2013
```

`car_drawings.py` reads the artist's sheets from `--source` or
`"car_drawings": {"dtm-2013": "<folder>"}` in `local.json`.

```bash
python tools/logo_art.py seasons/dtm-2013
```

```bash
python tools/logo_art.py bases/dtm-era4
```

```bash
python tools/portrait_art.py seasons/dtm-2013
```

```bash
python tools/build_pack.py seasons/dtm-2013 --install
```
