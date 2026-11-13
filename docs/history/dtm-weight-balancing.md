# DTM weight balancing, 1984 to 2026

Part of the DTM rules history (qualifying, race format, pit stops and
tyres, points, weight balancing). Made from the season research in
`seasons/<id>/research/` and the rulebook page `docs/dtm_rules.html`.
The table image is made with
`python -I tools/history_table.py docs/history/dtm-weight-balancing.md`.

`(?)` marks a detail the research files flag as unverified or
conflicting. No DTM ran from 1997 to 1999.

## Table

| Years | Base weights | Success ballast | Other balancing | Quirks |
|---|---|---|---|---|
| 1984 to 1985 | Minimum weight and rim width by engine size, 750 to 1425 kg. +70 kg for multi-valve engines. | | ONS handicaps, up to 120 kg or narrower tyres (1984). | Weights changed mid-season at Diepholz 1985 (?). |
| 1986 | By engine size. Turbo cars (Volvo 240T, Sierra) 1400 kg. | | | |
| 1987 | Per model: BMW M3 1000 kg, Sierra 1350 kg. | Success ballast per driver. | Weight changes after round 2 (Zolder), and again before rounds 4 and 6. | |
| 1988 | Per model. | Weight penalties. | Sierra turbo restrictor cut from 43.5 to 38 mm after round 1, then to 36 mm. | |
| 1989 | Per model. | Driver handicap weight. | New Ford restrictor after round 2, 36 to 40 mm (?). Weight changes at rounds 4 and 9. | |
| 1990 | Audi V8 1220 to 1250 kg, BMW and Mercedes 1040 kg. | Up to 100 kg, taken off again after poor results. Newcomers start at zero. | Audi +80 kg for Diepholz, then 50 kg off again. | Audi V8 with four-wheel drive. |
| 1991 | BMW 980 kg, Audi 1290 kg. Audi 40 kg lighter from Wunstorf. | Up to 50 kg. Newcomers start at the maximum (?). | | Audi 4WD about a minute clear in the wet Hockenheim heat. |
| 1992 | Audi 1300 kg. | Success ballast. | BMW got a bigger splitter and wing from the Nordschleife round (?). | |
| 1993 to 1994 | | | 4WD, traction control, ABS and active suspension allowed. | Alfa 155 and Opel 4WD against rear-drive Mercedes. |
| 1995 | 1020 kg for 2WD, 1060 kg for 4WD. | | | |
| 1996 | 1040 kg for every drivetrain. | | | |
| 2000 to 2003 | 1080 kg with driver (2002). | No rule found (?). | | |
| 2004 | Year-old 2003 cars allowed next to the new ones. | | | |
| 2005 | New cars 1050 kg, year-old cars 1035 kg. | Per make: the winning make +10 kg, the third make −10 kg, at most ±20 kg, new cars only. | | |
| 2006 | | Per make: +5 kg for each win, 5 kg off after a race without a win, at most 20 kg. | | |
| 2007 | | Per car generation, 7 kg steps. Cut to 3.5 kg once, for the race after the half-points Lausitz race. 5 kg steps from round 6 (Mugello). | | |
| 2008 | From July, 2006 cars 1020 kg and 2007 cars 1030 kg. | Per car generation, 5 kg per place (?). | | |
| 2009 | 2009 cars 1050 kg, 2008 cars 1030 kg, 2007 cars 1010 kg. | Success ballast, last year. | | |
| 2010 to 2013 | | None from 2010. | | |
| 2014 | | Performance weights per make, up to 10 kg. | | |
| 2015 | 1105 to 1140 kg. | Performance weights per driver from round 3. | | |
| 2016 | | Weights set after qualifying from each make's best theoretical lap, 2.5 or 5 kg steps. | | |
| 2017 | Base 1125 kg. | Performance weights, dropped from round 8. | | |
| 2018 | 1115 kg for all. | None. | | |
| 2019 to 2020 | 1070 kg with driver (2019). | None. | No BoP. No weight break for the new Aston Martin (2019). | Class One turbo cars. |
| 2021 | | For the next race: 25, 18 and 15 kg for the top three. | AVL balance of performance per track. | GT3 cars from many makes. |
| 2022 | | 25, 15 and 5 kg. | BoP per track, can change at any event. | |
| 2023 to 2025 | Drivers ballasted to 85 kg (2023) (?). | 20, 10 and 5 kg, races only, not in qualifying. | BoP per event. | |
| 2026 | | 20, 10 and 5 kg, races only, not in qualifying. | BoP per event. | |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| One minimum weight | Yes | `chassis_minimum_weight` |
| Weight per make, model or generation | Partly | baked into team car mass (B2, C9) |
| Success ballast | No | B1 |
| Changes during the season | No | B2 |
| Restrictors, aero changes per make | No | B2 |
| Four-wheel drive | Partly | ratings only (D2) |
| BoP per track | No | B2 |

## Sources

- `seasons/dtm-<year>/research/season.md` for every season, summed up in
  `docs/dtm_rules.html`.
- Open items check: touringcartimes July 2007 (DMSB cuts the steps from 7
  to 5 kg from Mugello). Autosport July 2019 (BoP scrapped in 2017, no
  concessions for Aston Martin) and de.wikipedia DTM-Saison 2019 (no
  ballast in the rule changes). Autosport 2020 (performance weights axed in
  late 2017, success ballast and BoP new for 2021). ran.de July 2026 (20, 10, 5 kg, not in
  qualifying, BoP before each event), auto motor und sport Aug 2026 (20 kg
  for the winner), pitdebrief 2026 Norisring BoP. 2000 to 2003: Autobild
  2002 gives 1080 kg with driver, no ballast rule found.
- Fact check: de.wikipedia DTM-Saison 1984 (weights by engine size,
  +70 kg for multi-valve), 2007 (ballast step cut from 7 to 3.5 kg once,
  after the half-points Lausitz race), 2022 (25, 15, 5 kg, BoP); Autobild
  2014; Autosport 2016; Motorsport.com 2017 (weights dropped for the last
  two rounds); en.wikipedia 2019.
- Confirmation round, 2007 steps: touringcartimes 25 May 2007 (after
  Lausitz the next race's steps were halved from 7 to 3.5 kg) and 14 July
  2007 (DMSB cuts the steps from 7 to 5 kg from round 6, Mugello). Both
  are true: a one-off halving, then a lasting change. de.wikipedia 2007
  gives the Lausitz part. Autosport 2007 (ballast against cars of the same
  age).
- Confirmation round, other years: touringcarracing.net race and car pages
  1986 to 1993 (Volvo and Sierra 1400 kg in 1986, 1987 weights and changes,
  Sierra restrictor 43.5, 38, 36 mm in 1988, Ford changes at rounds 3, 4
  and 9 in 1989, Audi 1220 to 1250 kg, 100 kg maximum, newcomers at zero,
  +80 kg at Diepholz and 50 kg off in 1990, 1991 weights and Wunstorf,
  1992 ballast and Audi 1300 kg). auto motor und sport (Audi V8 1230 kg in
  1990, 1290 kg in 1991). de.wikipedia 1984 and 1993. Motorsport.com (1040
  kg for all ITC cars, 40 kg break for 2WD before). crash.net and
  touringcartimes 2005 (1050 and 1035 kg, 10 kg per make, at most 20 kg).
  Autobild 2006 preview (5 kg per win, at most 20 kg). touringcartimes July
  2008 (older cars 1020 and 1030 kg). crash.net 2009 (1050, 1030, 1010
  kg) and touringcartimes 2010 (handicaps dropped). Autobild 2014 (up to
  10 kg per weekend per make). de.wikipedia 2015 to 2017 (1105 to 1140 kg
  from Norisring, 2016 system, base 1125 kg and weights dropped from the
  Red Bull Ring). en.wikipedia 2018 (1115 kg) and 2019 (1070 kg with
  driver). Autosport 2020 and 2023 (25, 18, 15 kg, then 20, 10, 5 kg).
  Not found: Diepholz 1985, the 1989 restrictor size, 1991 newcomers, the
  1992 BMW aero, the 2008 kg per place, the 2023 driver ballast.

## Discord post

=== post | DTM weight balancing history | dtm-weight-balancing
## DTM weight balancing, 1984 to 2026

Part five and the last of the DTM rules history, and the one F1 doesn't have. The table is below. What stood out to me:

- **Weights by engine size (1984 to 1986),** 750 to 1425 kg, then by model: BMW M3 1000 kg, Sierra 1350 kg, Audi V8 up to 1300 kg.
- **Changes during the season:** after set rounds, for one track (Audi +80 kg for Diepholz 1990), or restrictor cuts for the Sierra turbo.
- **Success ballast in many forms:** per driver up to 100 kg (1990), up to 50 kg with newcomers starting at the maximum (1991 (?)), per make (2005, 2006), per car generation (2007, 2008), per make or driver as "performance weights" (2014 to 2017), and since 2021 per finishing place for the next race.
- **Different weights per car generation** when year-old cars raced (2004 to 2009).
- **GT3 since 2021:** balance of performance per track plus success ballast, and drivers ballasted to 85 kg.

For the game this is a weight per make, model, generation or class, changes on a date or before a track, and ballast by result per driver, make or place. One rule type covers all of it: "if X happens, add Y kg to Z, up to a maximum". That would also cover BoP for the endurance mode.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the whole DTM series. Mistakes? Tell me!
