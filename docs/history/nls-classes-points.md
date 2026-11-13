# NLS classes and points, 1977 to 2026

Part of the NLS rules history (classes and points, race format). Endurance
races on the Nürburgring Nordschleife: Valvoline Langstreckenpokal 1977 to
1980, Veedol 1981 to 2000, BFGoodrich 2001 to 2009, VLN Langstreckenmeisterschaft
to 2019, NLS from 2020. The table image is made with
`python -I tools/history_table.py docs/history/nls-classes-points.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Classes | Balancing | Points | Champions |
|---|---|---|---|---|
| 1977 to 1998 | Many classes by engine size, from small hatchbacks up. | Classes by engine size. | Per class, by class size (?). | Mostly small cars: Simca Rallye, Audi 50, Fiat 127, Golf GTI, Opel Kadett, Citroën AX. BMW M3 in 1994, 1995 and 1998. |
| 1999 to 2008 | Same, plus big GT cars. | Same. | Same (?). | 1999: Chrysler Viper. Otherwise small BMW, Opel and Suzuki cars. |
| 2009 to 2019 | V classes (production cars), SP1 to SP8 by engine size, SP9 (GT3), SP10 (GT4), SP-Pro, SP-X, Cup classes, H (historic). 33 classes in 2009 (?). | SP9 balance of performance from 2010 (?). | Per class: 10 x (starters + 0.5 - place) / starters. A win in a full class is worth almost 10, a win alone 5. Two results dropped, best 7 of 9 when nine races run. | The cheap small classes win the title, they score the most. |
| 2020 to 2026 | Same groups, plus TCR, AT (alternative fuels), Cup 2 (Porsche Carrera Cup), Cup 3, Cup 5 (BMW M2 CS), Cup X. About 22 classes. | GT3 BoP (?). | Same formula (?). A separate Speed Trophy for the overall results. | Production cars won the drivers' title four years running to 2023. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| 20 or more classes in one race | No | B4 |
| Points by class size, title from class results | No | B3, B4 |
| Best 7 of 9 races | No | B3 |
| Balance of performance for GT3 | No | B2 |
| More than 100 cars | Partly | grid limit and pre-qualifying, at most 3 cars per team (C1) |

## Sources

- Wikipedia (English and German), "Nürburgring Langstrecken-Serie" (names,
  classes, points formula, discards, champions 1977 to 2009), "24 Hours of
  Nürburgring" (SP9 and SP10 from 2009).
- German Wikipedia champions list 1977 to 2024 (BMW M3 titles, 2000
  Suzuki Swift), drop rule (best 7 of 9, one drop if a race is cancelled).
- Not confirmed, marked `(?)`: points before 2009, BoP rules in NLS, the
  2009 class count.
- Conflict: VLN name from 2009 or 2010 (German Wikipedia: 2010).

## Discord post

=== post | NLS classes history | nls-classes-points
## NLS classes and points, 1977 to 2026

The Nordschleife's own endurance series, the opposite of a manager game's usual idea of a title. The table is below. What stood out to me:

- **Over 20 classes in one race,** from small production cars to GT3, more than 100 cars on track.
- **Points by class size:** 10 x (starters + 0.5 - place) / starters. A win in a full class is worth almost 10 points, a win alone only 5.
- **So small cars win the title:** Audi 50, Fiat 127, Golf GTI, Citroën AX, and recently BMW production cars. The fast GT3 cars race for the Speed Trophy.
- **Best 7 of 9 races** count.

For the game this is the "more titles and classes" lever at its extreme: many classes, points that depend on how many cars started in a class, and an overall title from class results.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
