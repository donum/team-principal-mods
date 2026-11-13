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
| 1984 to 1985 | Minimum weight and rim width by engine size, 750 to 1425 kg. +70 kg for multi-valve engines (1985). | | ONS handicaps. | Weights changed mid-season at Diepholz 1985. |
| 1986 | By engine size. Turbo cars (Volvo 240T, Sierra) 1400 kg. | | | |
| 1987 | Per model: BMW M3 1000 kg, Sierra 1350 kg. | Success ballast per driver. | Weight changes after rounds 2, 4 and 6. | |
| 1988 | Per model. | Weight penalties. | Sierra turbo restrictor cut from 43.5 to 38 mm after round 1, then to 36 mm. | |
| 1989 | Per model. | Driver handicap weight. | Ford restrictor 36 to 40 mm after round 2. Weight changes at rounds 4 and 9. | |
| 1990 | Audi V8 1250 kg, BMW and Mercedes 1040 kg. | Up to 100 kg, taken off again after poor results. Newcomers start at zero. | Audi +80 kg for Diepholz, then 50 kg off again. | Audi V8 with four-wheel drive. |
| 1991 | BMW 980 kg, Audi 1290 kg. Audi 40 kg lighter from Wunstorf. | Up to 50 kg. Newcomers start at the maximum. | | Audi 4WD about a minute clear in the wet Hockenheim heat. |
| 1992 | Audi 1300 kg. | Success ballast. | BMW got a bigger splitter and wing from the Nordschleife round. | |
| 1993 to 1994 | | | 4WD, traction control, ABS and active diffs allowed. | Alfa 155 and Opel 4WD against rear-drive Mercedes. |
| 1995 | 1020 kg for 2WD, 1060 kg for 4WD. | | | |
| 1996 | 1040 kg for every drivetrain. | | | |
| 2000 to 2003 | Not listed in the research (?). | | | |
| 2004 | Year-old 2003 cars allowed next to the new ones. | | | |
| 2005 | New cars 1050 kg, year-old cars 1035 kg. | Per make: the winning make +10 kg, the third make −10 kg, at most ±20 kg, new cars only. | | |
| 2006 | | Per make ±10 kg per round, at most ±20 kg. | | |
| 2007 | | Per car generation, 7 kg steps, 5 kg from Mugello. | | |
| 2008 | Year-old cars 10 kg lighter mid-season. | Per car generation, 5 kg per place. | | |
| 2009 | 2009 cars 1050 kg, 2008 cars 1030 kg, 2007 cars 1010 kg. | Success ballast, last year. | | |
| 2010 to 2013 | | None from 2010. | | |
| 2014 | | Performance weights per make, up to 10 kg. | | |
| 2015 | 1105 to 1140 kg. | Performance weights per driver from round 3. | | |
| 2016 | | Weights set after qualifying from each make's best theoretical lap, 2.5 or 5 kg steps. | | |
| 2017 | 1095 to 1140 kg. | Performance weights, dropped from round 8. | | |
| 2018 | 1115 kg for all. | None. | | |
| 2019 to 2020 | Not listed in the research (?). | | | Class One turbo cars. |
| 2021 | | For the next race: 25, 18 and 15 kg for the top three. | AVL balance of performance per track. | GT3 cars from many makes. |
| 2022 | | 25, 15 and 5 kg. | BoP (?). | |
| 2023 to 2025 | Drivers ballasted to 85 kg (2023). | 20, 10 and 5 kg, races only, not in qualifying. | BoP per event. | |
| 2026 | | Assumed unchanged (?). | BoP assumed unchanged (?). | |

## Sources

- `seasons/dtm-<year>/research/season.md` for every season, summed up in
  `docs/dtm_rules.html`.
- Flagged in the research: 2026 ballast and BoP are assumed, not yet
  confirmed from the regulations. 2019 and 2020 balancing not listed.

## Discord post

=== post | DTM weight balancing history | dtm-weight-balancing
## DTM weight balancing, 1984 to 2026

Part five and the last of the DTM rules history, and the one F1 doesn't have. The table is below. What stood out to me:

- **Weights by engine size (1984 to 1986),** 750 to 1425 kg, then by model: BMW M3 1000 kg, Sierra 1350 kg, Audi V8 up to 1300 kg.
- **Changes during the season:** after set rounds, for one track (Audi +80 kg for Diepholz 1990), or restrictor cuts for the Sierra turbo.
- **Success ballast in many forms:** per driver up to 100 kg (1990), up to 50 kg with newcomers starting at the maximum (1991), per make (2005, 2006), per car generation (2007, 2008), per make or driver as "performance weights" (2014 to 2017), and since 2021 per finishing place for the next race.
- **Different weights per car generation** when year-old cars raced (2004 to 2009).
- **GT3 since 2021:** balance of performance per track plus success ballast, and drivers ballasted to 85 kg.

For the game this is a weight per make, model, generation or class, changes on a date or before a track, and ballast by result per driver, make or place. One rule type covers all of it: "if X happens, add Y kg to Z, up to a maximum". That would also cover BoP for the endurance mode.

That's the whole DTM series. Mistakes? Tell me!
