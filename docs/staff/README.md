# DTM staff by season

Who held the game's staff roles at every DTM team, 1984 to 2026 (and ITC
1996). Use it when a new DTM pack needs `staff.json`: take the real people
from here and let the generator fill the rest.

- **Data:** [dtm_staff.csv](dtm_staff.csv), one row per person, role, team and
  season.
- **Built:** 2026-11-14, from six research passes (one per era) and a merge.
- **Size:** 1,016 people: 561 verified, 455 assumed.

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
| dtm-1984 | 35 | 10 | 12 | 7 | 5 |
| dtm-1985 | 38 | 8 | 9 | 3 | 6 |
| dtm-1986 | 22 | 7 | 8 | 4 | 4 |
| dtm-1987 | 18 | 8 | 14 | 6 | 8 |
| dtm-1988 | 32 | 15 | 30 | 11 | 19 |
| dtm-1989 | 28 | 13 | 24 | 9 | 15 |
| dtm-1990 | 16 | 6 | 13 | 6 | 7 |
| dtm-1991 | 22 | 8 | 15 | 6 | 9 |
| dtm-1992 | 17 | 6 | 12 | 5 | 7 |
| dtm-1993 | 33 | 16 | 25 | 7 | 18 |
| dtm-1994 | 19 | 10 | 22 | 3 | 19 |
| dtm-1995 | 13 | 11 | 25 | 5 | 20 |
| itc-1996 | 13 | 13 | 32 | 11 | 21 |
| dtm-2000 | 12 | 12 | 32 | 16 | 16 |
| dtm-2001 | 12 | 12 | 31 | 18 | 13 |
| dtm-2002 | 12 | 12 | 30 | 15 | 15 |
| dtm-2003 | 10 | 10 | 28 | 22 | 6 |
| dtm-2004 | 11 | 11 | 41 | 32 | 9 |
| dtm-2005 | 14 | 14 | 50 | 29 | 21 |
| dtm-2006 | 10 | 9 | 28 | 14 | 14 |
| dtm-2007 | 15 | 15 | 41 | 34 | 7 |
| dtm-2008 | 13 | 13 | 38 | 22 | 16 |
| dtm-2009 | 15 | 15 | 46 | 20 | 26 |
| dtm-2010 | 9 | 9 | 25 | 14 | 11 |
| dtm-2011 | 10 | 10 | 27 | 14 | 13 |
| dtm-2012 | 11 | 11 | 28 | 26 | 2 |
| dtm-2013 | 11 | 11 | 33 | 21 | 12 |
| dtm-2014 | 12 | 12 | 37 | 30 | 7 |
| dtm-2015 | 12 | 12 | 31 | 9 | 22 |
| dtm-2016 | 12 | 12 | 33 | 19 | 14 |
| dtm-2017 | 9 | 9 | 16 | 10 | 6 |
| dtm-2018 | 9 | 9 | 16 | 7 | 9 |
| dtm-2019 | 12 | 8 | 20 | 11 | 9 |
| dtm-2020 | 8 | 8 | 13 | 11 | 2 |
| dtm-2021 | 16 | 16 | 21 | 15 | 6 |
| dtm-2022 | 17 | 17 | 25 | 14 | 11 |
| dtm-2023 | 15 | 15 | 23 | 15 | 8 |
| dtm-2024 | 12 | 12 | 17 | 12 | 5 |
| dtm-2025 | 13 | 13 | 20 | 15 | 5 |
| dtm-2026 | 13 | 13 | 25 | 13 | 12 |

By role, over all seasons: team principal 457, chief designer 211, head of
engine 165, technical director 153, chief mechanic 20, head of aero 10, head
of dynamics 0.

## Known gaps

The research ran out of web searches in five of the six eras, so the thin
parts are not proof that nothing exists.

- **Head of aero and head of dynamics** are almost empty in every era. Only
  Lothar Pinske (Ford Sierra, 1987 to 1989) is in head of aero.
- **1984 to 1992 privateers:** most have no principal. Missing owners include
  Gubin, Isert, IPS/MS-Jet, Kamei, Bemani, Tauber, Valier, MM Diebels, Unitron,
  Auto Maass, BAS, Vanicek, Schübel, Bigazzi and Linder.
- **Mercedes / HWA:** no engine, aero or dynamics lead in any year. HWA's
  principal is its owner, Hans Werner Aufrecht (assumed for 2006 to 2012;
  Norbert Haug was the Mercedes motorsport boss above HWA).
- **BMW 2012 to 2019:** no chief designer or engine head for most years.
  Mike Krack (2012) is filed as technical director at manufacturer level.
- **2017, 2018 and 2020 to 2026:** mostly team principals only.
- **Doubtful credits:** Wikipedia names Dominic Harlow as designer of the
  2013 BMW M3 DTM and Wolfgang Dürheimer for the Audi RS 5. Both were left
  out; see the notes on the rows used instead.

Next targets for a second pass: the BMW and Audi press kits and media guides
(2013 to 2019), the owners of the privateer teams listed above, and the AMG,
Opel and Alfa aero and chassis leads.

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
