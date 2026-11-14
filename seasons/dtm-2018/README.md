# DTM 2018: Season Pack

Status: **generated and builds, not yet tested in-game or simulated.** The
data comes from `research/` through `tools/season_from_research.py`,
configured in `gen.json`. The sourced facts (calendar, entries, standings,
rules, sources) are in [research/season.md](research/season.md). Open work
is in [docs/plans/DTM2018_BACKLOG.md](../../docs/plans/DTM2018_BACKLOG.md).

2018 was the last year of the 4.0 V8 cars and Mercedes' last DTM season:
three makes, nine two-car teams, two races per weekend, each with its own
qualifying.

**Era base:** [`bases/dtm-era4`](../../bases/dtm-era4) (`"base": "dtm-era4"`),
like 2012 and 2013. The rules, tyre model, damage, traced tracks, engine and
tyre logos, car profiles and **engine sounds** come from there, so 2018 has
the base's V8 sound overlay (recorded from 2012 and 2013 cars). This folder
only holds what is 2018's own.

## How it's built

- **Teams and drivers:** 9 teams and 18 race seats from
  `research/entries.csv`, with the real numbers. The three guest entries
  (Ekström at round 1, Zanardi at round 7, Ogier at round 9) are reserve
  drivers of their teams; their skills are set by hand in `gen.json`
  (`drivers`), since guests scored no points.
- **Ratings:** from each team's average points per car, over the base's
  55 to 57.5 range. Skills from the 2018 standings over 11 to 18.
- **Previous position:** each team's 2017 teams' standing
  (`seasons/dtm-2017/research/standings_other.csv`). Team names changed
  between years at Mercedes, so the PETRONAS, REMUS and SILBERPFEIL teams
  are matched to the 2017 Mercedes me, BWT and SILBERPFEIL entries by hand.
- **Weight:** 1,115 kg including the driver (research/season.md). The
  chassis figure is 970 kg, plus the base's 145 kg engine.
- **Two races per round:** `"races_per_round": 2` in `gen.json` puts each
  race in its own game week, both at the same track. Since 2017 every race
  had its own qualifying, so a full weekend in the game (practice,
  qualifying, race) per race is close to the real format. A round's second
  race goes in the following week, so the season ends one week later per
  round than the real dates.
- **Rules** (`patches/regulations.json`, over the base's):
  - One qualifying session per race (`session_60`), not knockout.
  - Pole gets one point (`pole_point`). The real system gave 3-2-1 to the
    top three in qualifying.
  - The rest is the base's: points 25-18-15-12-10-8-6-4-2-1, DRS, option
    and standard tyre, no refuelling, two cars per team.
- **Race length:** 55 minutes plus one lap. `track_overrides` sets each
  venue's laps from `research/calendar.csv`. Where the two races differ,
  the longer one counts (Lausitz race 1 ran only 21 laps; the sources don't say why).
- **Colours:** first estimates from each team's usual colours. Not yet
  checked against 2018 photos.

## Tracks

| Round | Venue | Track id | How |
|---|---|---|---|
| 1, 10 | Hockenheim GP (4.574 km) | `hockenheim13` | base track |
| 2 | Lausitzring GP (4.345 km) | `lausitzring_gp` | base track, traced for 2018: 4,504 m (+3.7%) |
| 3 | Hungaroring (4.381 km) | `hungaroring` | shared from `bases/f1-v8`, `speed_mult` 1.09 (first guess) |
| 4 | Norisring | `norisring` | shared from 1991, base values |
| 5 | Zandvoort | `zandvoort` | base track |
| 6 | Brands Hatch GP (3.916 km) | `brandshatch_gp` | base track, traced for 2018: 3,864 m (−1.3%) |
| 7 | Misano (4.226 km) | `misano` | base track, traced for 2018: 4,171 m (−1.3%) |
| 8 | Nürburgring Sprint | `nuerburgring13` | base track |
| 9 | Red Bull Ring | `redbullring` | base track |

The Hungaroring is the F1 base's track. The F1 and DTM tracks use different
speed scales: the base's DTM Hockenheim has about 9% higher target speeds
than the F1 base's Hockenheim on the same layout, so `speed_mult` 1.09 is
used as a first guess until a simulated season checks it.

The three new venues are traced from OpenStreetMap into the base
(`bases/dtm-era4/track_specs/`), so later seasons on the base (and 2020 on
`dtm-era5`) get them too. Their `speed_scale` is 1.0, not yet calibrated.

- **Lausitzring GP:** the base's short course start (the tight left into
  the infield at the end of the front straight, a hand-placed bridge, and
  the infield esses), then the full back straight to the far hairpin
  instead of the 2007 Kurzanbindung. Not the banked oval Turn 1, which the
  DTM used from 2019. The trace is 3.7% longer than 4.345 km, the length
  en.wiki gives; the exact 2018 layout is not confirmed (research/season.md).
- **Brands Hatch GP:** the raceway loop of OSM relation 7218462, clockwise.
- **Misano:** the raceway loop of OSM relation 8671383, clockwise. The
  start line is placed by hand on the pit straight (OSM has no named pit lane).

## Simplifications

Game limits, each in [DEVELOPER_WISHLIST.md](../../docs/DEVELOPER_WISHLIST.md):

- **A1, A4:** two races per weekend become two game weeks.
- **A6:** each race had its own short qualifying; the game runs one open session.
- **B5:** one mandatory pit stop per race; the game has no rule for it.
  Tyre wear and the two-compound rule make a stop the normal strategy.
- **B6:** DRS was limited to a number of uses per race; the game has no limit.
- **B8:** 3-2-1 qualifying points; the game can only give pole one point.
- **B9:** the guest entries scored no points and drivers behind them moved
  up. In the game they are reserves only.
- **D3:** the new tracks' lap times are not calibrated yet.

## Not done yet

See the [backlog](../../docs/plans/DTM2018_BACKLOG.md): car images, logos,
portraits, sponsors, race-day maps for the three new venues, a simulated season to check lap
times and points, and a check of the 2018 tyre rules.
