# DTM staff by season

Who held the game's staff roles at every DTM team, 1984 to 2026 (and ITC
1996). Use it when a new DTM pack needs `staff.json`: take the real people
from here and let the generator fill the rest.

- **Data:** [dtm_staff.csv](dtm_staff.csv), one row per person, role, team and
  season.
- **Built:** 2026-11-14, from six research passes (one per era), a second pass on the gaps (privateer owners 1984 to 1995, works-team race engineers 2012 to 2019, engineering leads 1984 to 2011) and a merge.
- **Size:** 1,191 real people: 628 verified, 563 assumed. 512 of 631 team-seasons have a team principal.

- **Gaps:** [dtm_staff_fictional.csv](dtm_staff_fictional.csv) fills every
  empty role with a made-up name that fits the team's country and the
  period (3,237 rows, 1,451 people). Built by `tools/fictional_staff.py`.

## BTCC

The same layout for the BTCC: [btcc_staff.csv](btcc_staff.csv) (real
people, with an extra `born` column) and
[btcc_staff_fictional.csv](btcc_staff_fictional.csv). `fictional_staff.py`
fills both series in one run.

- **btcc-1991 (2026-11-16):** 25 real rows (15 verified, 10 assumed) for 14 of
  18 teams, mostly from Motor Sport magazine's 1991 issues. Nothing found
  for BMW Dealer Team Sweden, Techspeed, BRR and R&D Motorsport. The two Vic
  Lee teams share their made-up staff (one workshop). János Ódor's birth
  year is our estimate.
- **Joining teams 1992 to 2000 (2026-11-17):** 25 team principal rows (16
  verified, 9 assumed), one per team in its debut season (`btcc-1992` to
  `btcc-1999`), named as in `docs/teams/btcc_game_events.csv`. These seasons
  have no team list in `teams_by_season.json`, so `fictional_staff.py`
  skips them. Nothing found for TOM's GB (1993) and BMW (1995).
- **Open:** the Autosport scans on 1990sbtcc.com (`/as9101/` to `/as9112/`)
  are images and were not read; they likely name more engineers and team
  managers.

## Real and fictional names

The two files are kept apart on purpose. `dtm_staff.csv` holds only real
people. `dtm_staff_fictional.csv` holds made-up people for every role that is
still empty, so a pack can have a full staff list without putting a real
person into a job they never had.

- A fictional person keeps the job for a few seasons (a team principal about
  eight, a chief mechanic about four), has a birth year that fits the role,
  and never shares a name with a real person in the reference.
- Design, engine, aero and dynamics jobs at a works make (Audi, BMW,
  Mercedes, Opel, Alfa Romeo, …) from 1990 on are shared: one fictional
  person serves all teams of that make in a season.
- Where another team of the same make already has a real person in a
  manufacturer-level role, the gap is filled with that real person instead,
  marked `assumed` in `dtm_staff.csv` (note: "Same manufacturer-level role
  as …").
- When research later finds a real person, add the row to `dtm_staff.csv`
  and rerun `python tools/fictional_staff.py`: the fictional row for that
  slot disappears.

## Pictures in the game

The game shows pictures for two kinds of people only:

| Who | File | Matched by |
|---|---|---|
| Drivers | `assets/portraits/FirstLast.png` | the driver's full name |
| Team principals | `assets/team_principals/FirstLast.png` | the full name in `teamprincipals.json` |

The six staff roles (technical director to chief mechanic) have no picture
in the game. So the only staff people who can get a picture are the team
principals: 518 real ones in `dtm_staff.csv` and 119 fictional ones. For
real principals, the same photo rules apply as for driver portraits
(licence, credit). Fictional principals would need drawn or generated
portraits that do not look like a real person.

## Columns

| Column | Meaning |
|---|---|
| `season` | `dtm-1987`, `itc-1996`, … |
| `team` | Exactly as in that season's team list (`data/teams.json`, or `research/entries.csv` for seasons without a pack) |
| `role` | One of the seven ids below |
| `person` | The name |
| `status` | `verified`: a source names the person in that role at that team in or around that season. `assumed`: a reasonable inference, the reason is in `note` |
| `source` | URL, or the repo file for rows taken from our own research |
| `note` | Why it is assumed, or where it applies (for example "manufacturer level") |

A role with no row is empty: nothing was found. No name is invented.

## Roles

The game has six staff roles plus the team principal (the player). In the DTM
they mean:

| Game role | In the DTM |
|---|---|
| `team_principal` | Team owner or team boss (Teamchef). Not the manufacturer's motorsport boss. |
| `technical_director` | The team's technical director. For works teams, the manufacturer's DTM technical chief (note: "manufacturer level"). |
| `chief_designer` | Who designed the car. Usually at manufacturer or builder level (HWA, Audi Sport, BMW M, AMG, Alfa Corse), so the same person appears for every team running that car. |
| `head_of_aero` | Aerodynamicist of the car programme. |
| `head_of_engine` | Head of the engine programme (Paul Rosche, Ulrich Baretzky, Bernd Ramler, …). |
| `head_of_dynamics` | Chassis and vehicle dynamics lead. |
| `chief_mechanic` | Chief mechanic, or the team's race engineer at the track (note says which). |

## In the packs

A pack reads this reference when its `season.json` names the season:
`"staff": {..., "reference": "dtm-2013"}`. `tools/build_pack.py` then writes:

- `staff.json`: for each team and role the real person, else the made-up
  name from `dtm_staff_fictional.csv`, else a period name. A person works
  for one team only, so a name shared by several teams goes to the team
  with the highest level; the others get a period name.
- `teamprincipals.json`: one principal per team, real where known, in place
  of the base game's fictional principals. Pictures for them go in the
  pack's `assets/team_principals/FirstLast.png`.

Birth years of real people are not in the reference yet. Until they are, a
real person gets a fixed made-up birth year, so the age is wrong but stays
the same person from pack to pack.

Packs using it: dtm-2012, dtm-2013.

## How to use it for a new pack

1. Filter the CSV on the season.
2. Use every `verified` row as it is.
3. Use `assumed` rows unless a better source turns up. If one does, fix the
   row here first, then build the pack.
4. Leave every empty role to the generator (`tools/build_pack.py`,
   `generate_staff`). Those names are fictional.
5. A person can sit in two roles or two teams (a manufacturer's chief
   designer for all its teams). The game needs one staff record per team
   and role, so give each team its own copy.

## Coverage

| Season | Teams | With principal | People | Verified | Assumed |
|---|---|---|---|---|---|
| dtm-1984 | 35 | 15 | 17 | 8 | 9 |
| dtm-1985 | 38 | 14 | 15 | 5 | 10 |
| dtm-1986 | 22 | 10 | 11 | 6 | 5 |
| dtm-1987 | 18 | 11 | 17 | 8 | 9 |
| dtm-1988 | 32 | 20 | 35 | 14 | 21 |
| dtm-1989 | 28 | 17 | 28 | 10 | 18 |
| dtm-1990 | 16 | 14 | 31 | 12 | 19 |
| dtm-1991 | 22 | 17 | 36 | 16 | 20 |
| dtm-1992 | 17 | 12 | 26 | 13 | 13 |
| dtm-1993 | 33 | 21 | 31 | 7 | 24 |
| dtm-1994 | 19 | 15 | 27 | 4 | 23 |
| dtm-1995 | 13 | 13 | 29 | 5 | 24 |
| itc-1996 | 13 | 13 | 36 | 11 | 25 |
| dtm-2000 | 12 | 12 | 34 | 18 | 16 |
| dtm-2001 | 12 | 12 | 33 | 18 | 15 |
| dtm-2002 | 12 | 12 | 33 | 15 | 18 |
| dtm-2003 | 10 | 10 | 30 | 22 | 8 |
| dtm-2004 | 11 | 11 | 41 | 32 | 9 |
| dtm-2005 | 14 | 14 | 50 | 29 | 21 |
| dtm-2006 | 10 | 9 | 28 | 14 | 14 |
| dtm-2007 | 15 | 15 | 41 | 34 | 7 |
| dtm-2008 | 13 | 13 | 38 | 22 | 16 |
| dtm-2009 | 15 | 15 | 46 | 20 | 26 |
| dtm-2010 | 9 | 9 | 25 | 14 | 11 |
| dtm-2011 | 10 | 10 | 27 | 14 | 13 |
| dtm-2012 | 11 | 11 | 28 | 26 | 2 |
| dtm-2013 | 11 | 11 | 31 | 17 | 14 |
| dtm-2014 | 12 | 12 | 42 | 34 | 8 |
| dtm-2015 | 12 | 12 | 36 | 10 | 26 |
| dtm-2016 | 12 | 12 | 41 | 27 | 14 |
| dtm-2017 | 9 | 9 | 28 | 19 | 9 |
| dtm-2018 | 9 | 9 | 29 | 11 | 18 |
| dtm-2019 | 12 | 8 | 24 | 18 | 6 |
| dtm-2020 | 8 | 8 | 13 | 11 | 2 |
| dtm-2021 | 16 | 16 | 21 | 15 | 6 |
| dtm-2022 | 17 | 17 | 25 | 14 | 11 |
| dtm-2023 | 15 | 15 | 23 | 15 | 8 |
| dtm-2024 | 12 | 12 | 17 | 12 | 5 |
| dtm-2025 | 13 | 13 | 20 | 15 | 5 |
| dtm-2026 | 13 | 13 | 25 | 13 | 12 |

By role, over all seasons: team principal 518, chief designer 237, head of
engine 181, technical director 153, chief mechanic 57, head of aero 22, head
of dynamics 0.

## Known gaps

The research ran out of web searches in five of the six eras, so the thin
parts are not proof that nothing exists.

- **Head of aero and head of dynamics** are almost empty in every era. Head
  of aero has Lothar Pinske (Ford Sierra, 1987 to 1989) and Richard Eppler
  (Mercedes 190E Evo II, 1990 to 1992). No chassis lead was found for any
  programme, after two passes.
- **1984 to 1995 privateers:** the second pass found Gubin, Isert, IPS/MS-Jet,
  MM Diebels, Schübel, Linder, Bemani and others. Still missing: about 50 small
  1980s entries (clubs, dealers, sponsor names), Bigazzi, Auto Maass, BAS,
  Kamei, Dellenbach, Eisele, Racing Dynamics, Marlboro BMW Dealer Team and a
  few 1993 to 1995 teams.
- **Mercedes / HWA:** no engine, aero or dynamics lead in any year. HWA's
  principal is its owner, Hans Werner Aufrecht (assumed for 2006 to 2012;
  Norbert Haug was the Mercedes motorsport boss above HWA).
- **BMW 2012 to 2019:** no chief designer or engine head for most years.
  Mike Krack (2012) is filed as technical director at manufacturer level.
  Race engineers (as chief mechanic) come from the 2014 and 2016 BMW media
  guides; the other years carry them over as assumed.
- **Fan wiki:** rows whose only source is the DTM fan wiki (dtm.fandom.com)
  are marked assumed, not verified.
- **2017, 2018 and 2020 to 2026:** mostly team principals only.
- **Doubtful credits:** Wikipedia names Dominic Harlow as designer of the
  2013 BMW M3 DTM and Wolfgang Dürheimer for the Audi RS 5. Both were left
  out; see the notes on the rows used instead.

Corrections made in the second pass: Audi 2019 head of engine is Stefan
Dreyer (not Baretzky); the Opel Vectra chief designer for 2004 and 2005 is
Jean-Claude Martens (Günther Steiner stays technical director); Dominic
Harlow is no longer listed as BMW chief designer in 2013 (BMW's 2014 guide
shows him as a race engineer).

## Team lists to clean up

The research found these problems in our season team lists. They are not
fixed yet; the CSV uses the names as they are.

- **Same team, several names in one season** (they share the same staff):
  - 1984: Brun Motorsport / Jägermeister Brun Motorsport
  - 1985: three HWRT Ford names
  - 1988: Ford-Grab / Hein Gericke Ford Grab, Euro Racing / Euro Racing PCD
  - 1993 to 1995: Schübel I / II and its sponsor splits, three Zakspeed entries
  - ITC 1996: three JAS entries
  - 2000: Opel Team Holzer next to Holzer (1) and (2)
  - 2005: Audi Sport Team Joest / Joest Racing
  - 2007 to 2016: Abt under two names each year
  - 2023: Mercedes-AMG Team BWT and Mann-Filter (both Landgraf)
  - 2024: two GRT Lamborghini entries
  - 2026: Winward's sponsor entries
- **Misspelt or placeholder names:** "ABR Ringhausen" (Ringshausen), "privat",
  "private" and "Private entries", "Opel (works entry)" (1988).
- **Wrong or split entries:**
  - 2006: AutoScout24/Junge Gebrauchte was two operators (Persson #21, Mücke #22).
  - 2019: "BMW Team RMR" does not match BMW's media guide (Glock was RMG,
    Eng was RBM). "Audi Sport Team Rosberg / Audi Sport Team WRT" is one
    driver's combined entry, not a team.
  - 2019: TOM'S, Nismo and Kunimitsu were Super GT guests at one round.
- **Missing from the lists but in `entries.csv`:** Kissling and MK
  Motorsport (1987), two HWA/Persson entries (2003), Stern and AMG-Mercedes
  (2010).
