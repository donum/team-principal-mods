# DTM 1987: Season Pack

Status: **v0.1, generated and builds, not yet tested in-game.** The data was
generated with `tools/season_from_research.py` from `research/`, configured
in `gen.json`. For the sourced facts behind it (calendar, entry list,
standings, rules, sources and unverified points), see
[research/season.md](research/season.md). Open work is in
[docs/plans/DTM1987_BACKLOG.md](../../docs/plans/DTM1987_BACKLOG.md).

1987 is the earliest Group A season in the repo: one race of about 100 km
per round, no pit stops, and an open field of BMW M3 and 635 CSi, Ford
Sierra, Volvo 240 Turbo, Mercedes 190E and Alfa Romeo 75 Turbo cars.

**Template:** like 1990 and 1992, 1987 builds on the DTM 1991 pack
(`"template": "dtm-1991"`), not on an era base. It takes the 1991 Group A
rules, car profile and tyre suppliers, and adds its own engines, car
profiles, weights and points (`gen.json`, `patches/regulations.json`).

**Sounds:** the game's vanilla sounds. Era 1 (1984 to 1992) has no sound
overlay yet; 1987 will inherit whatever the Group A seasons get (see the
backlog).

## How it's built

- **Teams and drivers:**
  - 18 teams, 28 race seats and 49 drivers from `research/entries.csv`.
  - Drivers who entered at least half the rounds get race seats, up to 3 per
    team. Everyone else is a reserve driver, with their real number where
    known.
  - The many private entrants share one team, "Private entries" (von Löwis,
    Niederhof, Gröpper, plus reserves). Gröpper's Ford Mustang races as a
    BMW there.
  - Left out (`"skip"`): Kissling Motorsport (Peil, Opel Kadett then Volvo,
    5 rounds), MK Motorsport (3 starts) and Gerhard Müller's one Volvo
    start without a known entrant.
  - Guests and stand-ins (Ludwig, Soper, Hahne, Giroix) are reserves with
    hand-set skills (`drivers` in `gen.json`).
- **Ratings, skills and salaries:** estimated from the final 1987 standings
  (default ranges). These are estimates, not history.
- **Cars and engines** (`gen.json`):

  | Car | Supplier key | Engine | Weight (round 1) | Car mass + engine |
  |---|---|---|---|---|
  | BMW M3 | `BMW` | BMW S14 2.3 16V | 1000 kg | 860 + 140 |
  | BMW 635 CSi | `BMW 635` | BMW 3.5 L6 | 1200 kg | 1010 + 190 |
  | Ford Sierra XR4Ti | `Ford` | Ford 2.3 Turbo | 1350 kg | 1180 + 170 |
  | Volvo 240 Turbo | `Volvo` | Volvo B21ET 2.1 Turbo | 1315 kg | 1140 + 175 |
  | Mercedes 190E 2.3-16 | `Mercedes-Benz` | Mercedes-Benz 2.3-16 | 1060 kg | 920 + 140 |
  | Alfa Romeo 75 Turbo | `Alfa Romeo` | Alfa Romeo 1.8 Turbo | 1150 kg | 1000 + 150 |

  Power ratings follow the TCR car sheets (M3 300 hp, 635 335 hp, Sierra and
  Volvo 340 hp, 190E 260 hp, Alfa 282 hp). Car profiles (`profiles`) are
  first guesses: the turbos are quick on the straights and hard on tyres,
  the M3 and 190E are better in the corners.
- **Tracks:** all shared with other seasons (`shared_tracks`), with the 1987
  lap length and race laps in `track_overrides`:

  | Round | Venue | Track id | From | Laps |
  |---|---|---|---|---|
  | 1 | Hockenheim Motodrom | `hockenheim_short` | dtm-1992 | 40 |
  | 2 | Zolder | `zolder` | dtm-1991 | 24 |
  | 3, 7 | Nürburgring GP | `nuerburgring` | dtm-1991 | 25 (round 7 ran 23) |
  | 4 | AVUS long circuit | `avus87` | own trace (`track_specs/`): 1991 AVUS spec with the south turn moved south, 8,038 m | 13 |
  | 5 | Mainz-Finthen | `mainzfinthen` | dtm-1990 | 45 |
  | 6 | Norisring | `norisring` | dtm-1991 | 44 |
  | 8 | Wunstorf | `wunstorf` | dtm-1991 | 20 |
  | 9 | Diepholz | `diepholz` | dtm-1991 | 40 |
  | 10 | Salzburgring | `salzburgring` | own trace (`track_specs/`): OSM relation 19552391, 4,187 m | 25 |

  The non-championship Hockenheim event in October is not in the pack.
- **Art:** none yet. Teams have no car images, logos or portraits.

## Rules (`patches/regulations.json`, `season.json` constants)

| Rule | 1987 | In the game |
|---|---|---|
| Points | 20-18-16-15-14-13-12-11-10-9-8-7-6-5-4-3-2-1 to 18th, one drop result | `points_system: dtm_1987` and `POINTS_TOP10`: the top ten only, all results count |
| Weekend | Practice, qualifying, one race of about 100 km | One race at the real distance (`race_laps`) |
| Pit stops | None planned | Tyre wear from the 1991 tuning, no forced stop |
| Weights | Per model (table above), changed during the year | `chassis_minimum_weight: group_a_1987` (860 kg chassis) and per-team `car_mass_kg`, fixed for the year |
| Car base | Group A with DTM weight and tyre penalties | `car_profile: group_a_touring` from 1991 (to calibrate) |
| Tyres | Open: Pirelli, Dunlop, Michelin | Each team's supplier from the TCR car sheets |

## Simplifications

Wish list items in [DEVELOPER_WISHLIST.md](../../docs/DEVELOPER_WISHLIST.md):

- **Points (B3):** only the top ten score, and there is no drop result.
- **Guest entries (B9):** Ludwig won round 7 as a guest without points. In
  the game a reserve driver scores.
- **Part-timers and car changes (C2):** stand-ins (Bartels, Niedzwiedz,
  Soper, Hahne) and mid-season car changes (König from 635 CSi to M3,
  Reuter, Winkelhock and Hahne to the Sierra RS 500 Cosworth) are not
  modelled. Each team races one car all year.
- **One car model per make (C9):** the game has one engine per supplier, so the
  635 CSi teams use a second BMW supplier, `BMW 635`.
- **Weight changes (B1, B2):** success ballast and the mid-season weight
  changes (BMW M3 +100 kg after Zolder, Sierra -100 kg then +50 kg, Volvo and
  Alfa -50 kg, Mercedes -50 kg at the AVUS) are not modelled.
- **Tyres (D9):** the open tyre war uses the 1991 supplier ratings.
- **Tracks (D3):** the AVUS long circuit and the Salzburgring are traced from
  OpenStreetMap but not calibrated (`speed_scale` copied from the 1991
  tracks). The AVUS south turn position is undocumented; it is placed where
  the lap measures 8.11 km. The Salzburgring is today's layout.

## Rebuild

```bash
python tools/season_from_research.py seasons/dtm-1987
```

```bash
python tools/build_pack.py seasons/dtm-1987 --install
```
