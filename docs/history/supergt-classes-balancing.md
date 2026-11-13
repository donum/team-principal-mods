# Super GT classes, balancing and tyres, 1993 to 2026

Part of the Super GT rules history (classes and balancing, race format and
points). JGTC 1993 to 2004, Super GT from 2005. The table image is made
with `python -I tools/history_table.py docs/history/supergt-classes-balancing.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Classes | Top class cars | Balancing | Tyres and fuel |
|---|---|---|---|---|
| 1993 | GT1 and GT2, one real JGTC car in each (a Skyline GT-R and a Silvia). They race with JSS cars. Only 4 races. | Skyline GT-R. | Power limits. No success weight yet. | |
| 1994 to 1995 | GT1 and GT2. | Skyline, Supra, Porsche, Ferrari F40. | Air restrictors by weight and power (from the end of 1995). | |
| 1996 to 2008 | GT500 and GT300 in one race. | 1996: McLaren F1 GTR wins. Then Supra, NSX, Skyline, Fairlady Z, Lexus SC 430, GT-R. | Weight for top places in qualifying and the race (since 1994), and for the fastest lap (to 2006). 2008: GT500 cars above 1,200 kg get a smaller restrictor instead. | Several tyre makers. |
| 2009 to 2013 | Same. | 2010: GT500 front-engine rear-drive only (Honda waiver to 2019). | 2 kg per championship point. Halved at the second-last race, removed at the last, for teams at every race. | From 2010 GT300 allows FIA GT3 cars. Bridgestone, Michelin, Yokohama, Dunlop. |
| 2014 to 2019 | Same. GT300: FIA GT3, JAF-GT and "Mother Chassis" cars. | 2.0 L four-cylinder turbo, about 650 hp. Aero and more than 60 parts shared with DTM ("Class 1"). | GT300: balance of performance per race (restrictor, weight, ride height, boost), public. GT500 ballast above 50 kg can become less fuel flow (2014, 2015), the rule returns in steps from 2017. | 2017: KERS banned. Michelin's last GT500 title 2015. |
| 2020 to 2022 | Same. | Full Class 1: common ECU and suspension. Supra, NSX, GT-R, then Nissan Z. | Same. | Bridgestone wins every GT500 title since 2016. |
| 2023 to 2025 | Same. | Same. | 2025: GT300 ballast includes refuelling time, 50 kg cap. | GT500 carbon-neutral fuel from 2023. |
| 2026 | Same. | Honda Prelude-GT. One engine per season. | GT500: 0 to 50 kg = 90.2 kg/h fuel flow, 51 to 67 kg = 88.0 kg/h, above that smaller refuelling restrictors. | Tyre war still on, last year: one tyre maker per class from 2027. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Two classes in one race | No | B4 |
| Success ballast by points | No | B1 |
| Less fuel flow instead of ballast | No | B1 |
| Balance of performance per race | No | B2 |
| Several tyre makers, tyre war | Partly | ratings per compound, no warm-up per maker (D9) |
| One engine per season | Yes | `seasonal_component_allocation_rule` |
| Shared common parts | Partly | ratings can be set level |

## Sources

- Wikipedia, "Super GT" (classes, GT500 and GT300 specs, ballast, BoP,
  champion cars with tyre makers), "All Japan Grand Touring Car
  Championship" (1993 to 2004), 2026 Super GT season (fuel flow table).
- Wikipedia, "2010 Super GT Series" (GT3 cars allowed from 2010, first
  GT3 title 2011), "2026 Super GT Series" (single tyre maker per class
  from 2027).
- Japanese Wikipedia, "SUPER GT" (success weight since 1994, by
  qualifying and race places to 2008, fastest lap to 2006, the 2008
  1,200 kg limit, fuel restrictor above 50 kg to 2015 and from 2017) and
  "全日本GT選手権" (weight for top results), Nismo 2006, "Weight handicap
  and restrictor". English Wikipedia, "Super GT" (ballast formerly by
  qualifying places and lap times), Super GT World, February 2017 ("fuel
  flow restrictors return").
- Wikipedia, "1996 All Japan Grand Touring Car Championship" and Japanese
  Wikipedia "全日本GT選手権": the names GT500 and GT300 start in 1996, GT1
  and GT2 before. The "Super GT" page is less exact here.
- Wikipedia, "1993 All Japan Grand Touring Car Championship" (GT1 and
  GT2 classes in the tables, grid mostly JSS cars) and Japanese Wikipedia
  "全日本GT選手権" (1993: one GT1 car, a Skyline GT-R, and one GT2 car, a
  Silvia, racing with JSS, 4 races held). Japanese Wikipedia "SUPER GT"
  (weight handicap from 1994, the second year) and Wikipedia "1994 All
  Japan Grand Touring Car Championship" (success ballast from 1994).
- Wikipedia "2026 Super GT Series" and Sportscar365, "GT500 fuel flow cut,
  new handicap system planned" (90.2 kg/h base, 88.0 kg/h above 50 kg).
- Note: the 1994 season article says 1994 "introduced" two classes. The
  1993 tables and Japanese Wikipedia show both classes already in 1993, so
  the table uses 1993. The English JGTC overview mentions weight penalties
  for winners without a year, the season and Japanese articles put the
  start in 1994.

## Discord post

=== post | Super GT classes history | supergt-classes-balancing
## Super GT classes, balancing and tyres, 1993 to 2026

Japan's GT series, as a test for classes and success ballast. The table is below. What stood out to me:

- **Two classes in one race** from the start in 1993 (GT1 and GT2, GT500 and GT300 since 1996), with their own results and titles.
- **Success ballast by championship points:** 2 kg per point, halved at the second-last race, removed at the last.
- **Above 50 kg, less fuel flow instead of more weight** (GT500 in 2014 and 2015, again from 2017). In 2026 a table: up to 50 kg, then a lower fuel flow, then smaller refuelling restrictors.
- **GT300 balance of performance per race,** made public.
- **A real tyre war, still today:** Bridgestone, Michelin, Yokohama, Dunlop. 2026 is the last year, then one maker per class.
- **GT500 shared rules with the DTM** ("Class 1") from 2014 to 2020.

For the game this is the same balancing rule as DTM and BTCC ("if X, add Y to Z"), with fuel flow as one more thing to add. Plus classes in one race, which endurance needs too.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
