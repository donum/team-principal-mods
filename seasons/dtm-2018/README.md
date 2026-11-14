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
  - **One dry tyre.** The option tyre ended after 2016, so 2018 had one
    Hankook slick. As in 2012, `data/tyremodel.json` keeps the soft as an
    exact copy of the hard and no car starts on it, `tyre_suppliers` in
    `gen.json` gives the soft the hard's ratings, and the two-compound rule
    is off. Wear stays at the base hard's 0.018: in the 2012 simulator most
    cars then stopped once, which is the 2018 rule. Not yet simulated.
  - The rest is the base's: points 25-18-15-12-10-8-6-4-2-1, DRS, no
    refuelling, two cars per team.
- **Race length:** 55 minutes plus one lap. `track_overrides` sets each
  venue's laps from `research/calendar.csv`. Where the two races differ,
  the longer one counts (Lausitz race 1 ran only 21 laps: Rast rolled, the
  race was red flagged and the clock ran on).
- **Colours:** first estimates from each team's usual colours. Not yet
  checked against 2018 photos.

## Data checks (14 November 2026)

All entries, birth dates, points and the calendar were checked against
en.wiki, de.wiki and the official wige timing sheets (research/season.md):

- Numbers, birth dates, drivers', teams' and makes' points: all correct.
- Lausitzring: 4.570 km, not 4.345 km (timing sheets).
- Edoardo Mortara raced on a Swiss licence (CHE on every 2018 timing
  sheet), so he is Swiss in the pack. Both Wikipedias show an Italian flag.
- Ekström's guest car was entered as "Audi Sport Team Abt", not Abt
  Sportsline. `gen.json` maps both names to the Abt Sportsline team.
- Philipp Eng was entered by BMW Team RMR (the team totals add up only
  that way).
- Rules: one dry tyre (above), 8 engines per car, about a third less
  downforce, DRS on 12 laps per race.

## Feeder series

`juniors` in `gen.json`, from `research/juniors/` (one md dossier and
four CSVs per series, each checked against two sources where possible):

| Series | Tier | 2018 champion | Rounds | Seated in the game |
|---|---|---|---|---|
| FIA Formula 3 European Championship (F3EU) | 2 | Mick Schumacher | 10, seven at DTM weekends | 20 drivers, 7 teams |
| Porsche Carrera Cup Deutschland (PCCD) | 2 | Thomas Preining | 7, at ADAC GT Masters weekends | 21 drivers, 13 teams |
| ADAC TCR Germany (TCR) | 3 | Harald Proczyk | 7, at ADAC GT Masters weekends | 22 drivers, 17 teams |
| ADAC Formula 4 (F4) | 4 | Lirim Zendeli | 7, GT Masters, DTM and F1 weekends | 22 drivers, 7 teams |

- The game only seats drivers inside a series' age band, so older
  drivers are left out: in PCCD Ammermüller (2nd) and van Lagen, in TCR
  the champion Proczyk and Langeveld (3rd). Their teams still race.
- The Carrera Cup points scale (25-20-16-13-11-...) is worked out from
  the race results; de.wiki's printed scale does not match its totals.
- TCR's 20-place scale is used; its qualifying points (5-4-3-2-1) are not
  in the game.
- Free agents (`research/juniors/free_agents.csv`): Kubica, Maxime
  Martin, Tom Blomqvist, Maro Engel and Kelvin and Sheldon van der Linde.
  Blomqvist and the van der Lindes are young enough that the game can
  seat them in a feeder series.

## Portraits

`art/portraits.json`: a free Commons photo for every DTM driver, picked by
hand and pinned, and cropped by `tools/portrait_art.py`. Commons has little
from 2018 itself:

- From 2018 events: Paffett, Juncadella and Farfus (Matt Buck, Brands
  Hatch), di Resta and Duval (Le Mans), Ekström (World RX test).
- Close to 2018 (2016 to 2019): Wehrlein, Ogier, Auer, Mortara, Müller,
  Rast, Green and Eriksson. Several come from Audi's Flickr stream
  (CC BY 2.0).
- Further away: Rockenfeller and Zanardi (2014), Glock (2015), Spengler
  (2021), Frijns (2023), Wittmann (2024). No closer photo shows the face
  clearly.
- Philipp Eng has a helmet card. His only 2018 photo on Commons looks like
  a BMW press photo uploaded as own work, so it is not used.
- Feeder drivers get the photo closest to 2018 from Wikidata, or a helmet
  card in their team's colours.

## Tracks

| Round | Venue | Track id | How |
|---|---|---|---|
| 1, 10 | Hockenheim GP (4.574 km) | `hockenheim13` | base track |
| 2 | Lausitzring GP (4.570 km) | `lausitzring_gp` | base track, traced for 2018: 4,504 m (−1.4%); `length_km` 4.57 set for 2018 |
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
  DTM used from 2019. The official 2018 timing sheets give 4,570 m, so
  2018 sets `length_km` 4.57 in `track_overrides`; the trace is 1.4%
  shorter. The base keeps en.wiki's 4.345 km, which 2020 still uses
  (research/season.md).
- **Brands Hatch GP:** the raceway loop of OSM relation 7218462, clockwise.
- **Misano:** the raceway loop of OSM relation 8671383, clockwise. The
  start line is placed by hand on the pit straight (OSM has no named pit lane).

## Simplifications

Game limits, each in [DEVELOPER_WISHLIST.md](../../docs/DEVELOPER_WISHLIST.md):

- **A1, A4:** two races per weekend become two game weeks.
- **A6:** each race had its own short qualifying; the game runs one open session.
- **B5:** one mandatory pit stop per race; the game has no rule for it.
  Tyre wear and the two-compound rule make a stop the normal strategy.
- **B6:** DRS was limited to 12 laps per race (36 uses, within one second of the car ahead); the game has no limit.
- **B8:** 3-2-1 qualifying points; the game can only give pole one point.
- **B9:** the guest entries scored no points and drivers behind them moved
  up. In the game they are reserves only.
- **D3:** the new tracks' lap times are not calibrated yet.

## Not done yet

See the [backlog](../../docs/plans/DTM2018_BACKLOG.md): car images, logos,
sponsors, race-day maps for the three new venues, and a simulated season to
check lap times, points and one stop per race.
