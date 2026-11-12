# Package: Entries, Drivers and Crews

The entry as the unit: car, number, code, drivers and tags. Part of the
[feature packages](README.md).

- **Wishlist items:** [C1](../DEVELOPER_WISHLIST.md#c1-more-than-3-cars-per-team--p1),
  [C2](../DEVELOPER_WISHLIST.md#c2-entry-lists-per-round-part-timers-and-guests--p1),
  [C3](../DEVELOPER_WISHLIST.md#c3-car-numbers-per-entry-and-fixed-numbers--p2),
  [C5](../DEVELOPER_WISHLIST.md#c5-retirement-and-age-tuning-in-data--p3),
  [C6](../DEVELOPER_WISHLIST.md#c6-driver-timing-codes--p3),
  [C8](../DEVELOPER_WISHLIST.md#c8-driver-crews-per-car-endurance--p3).
- **Modes:** all three; endurance needs crews most.
- **Status:** outline.

## 1. What the game has today

- One driver per car, contracts for a whole season.
- `formula_team_entry_cap` up to `three`; the oval mode has
  `oval_team_entry_cap` up to `entries_6` and a charter system.
- Car numbers per team; no timing code; `birth_year` since 0.99.6.

## 2. Every need we know

| Seasons | Need |
|---|---|
| DTM 1991, 1992 | 4 or 5 cars for one team (AMG) |
| DTM 1991 | Part-timers for set rounds (Schumacher 2 rounds, Röhrl 1) |
| DTM 1992 | A make that leaves mid-season (Audi after round 6) |
| DTM 1991 | Numbers on the entry, kept by reserves and guests |
| DTM 2013 | Three-letter timing codes (TSC for Scheider) |
| DTM 1984, 1987, 2018, 2021 on | Guest entries |
| DTM 1991 | Drivers racing into their 50s |
| Endurance | Two to four drivers per car |

## 3. The building blocks

- **Entry:** team, car (chassis, engine, tyres), number, image, one to
  three or four drivers, `rounds` it enters, and **tags**: `class`,
  `guest`, `privateer`, `rookie`, `customer`, `pro_am`.
- **Driver fields:** `code`, `birth_year`, retirement settings in data.
- **Drive-time rules** (crews): minimum per driver, maximum stint, maximum
  total, a driver rating rule for Pro-Am classes.
- **Driver change** as a pit-stop service
  ([Tyres and pit stops](tyres-and-stops.md)).

## 4. Fits the existing options

- `formula_team_entry_cap` gets the oval range (`four`, `five`, `six`).
- `teams.json` `entry_count` and driver contracts stay; a contract may add
  `rounds` and `number`.
- A one-driver entry behaves exactly like today's car.

## 5. Overlaps

| Shared block | Package |
|---|---|
| Tags decide who scores and in which title | [Points](points-and-championships.md) |
| Tags select BoP and ballast | [Balance](balance-and-homologation.md) |
| Groups and classes in qualifying | [Weekend format](weekend-format.md) |
| Per-entry image, code and portrait on screens | [Presentation](presentation.md) (E4, E15) |
| Junior eligibility flag | [Calendar and world](calendar-and-world.md) (C7) |

## 6. Endurance

- Crews, stints, fatigue, night and wet specialists (C8).
- A stint planner for the player, with AI teams on the same rules.
- One-off entries for the big race (Le Mans) and invitations.
- Driver ratings (Platinum to Bronze) and class rules built on them.

## Evidence log

| Item | Season | Need | Source | Status |
|---|---|---|---|---|
| C1, C2, C3 | DTM 1991 | 4 cars, part-timers, numbers | `seasons/dtm-1991/research` | Checked |
| C6 | DTM 2013 | Timing codes | `seasons/dtm-2013/research/spotter_guide.csv` | Checked |

## Open questions

- Does the endurance mode plan to share the entry model with formula
  packs?
