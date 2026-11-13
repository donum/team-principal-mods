# F1 entries and drivers, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops, race format, safety car, overtaking aids, engines, parc fermé and
weight, money and testing, entries and drivers). Each file has the table,
the sources and a Discord post. The table image is made with
`python -I tools/history_table.py docs/history/f1-entries-drivers.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Entries | Drivers | Numbers | Quirks |
|---|---|---|---|---|
| 1950 to 1962 | No limit on cars per team. Works teams and privateers with bought cars side by side. Indy 500 entries count, F2 cars sometimes in the same race. | No licence. Two drivers can share one car and split the points (to 1957). | Set by each race organiser, a car can change number every race. | Rob Walker, a privateer, gave Cooper and Lotus their first wins. |
| 1963 to 1972 | Usually two cars per team, a third for a guest driver. | No licence. | Still set per race. | BRM entered more than three cars in 1971 and 1972. |
| 1973 to 1980 | Two cars normal, a third now and then. Privateers still buy cars from Lotus, Brabham and others. | No licence. | From 1974: fixed numbers per team for the whole season. Champion gets 1 and 2, the rest by last year's constructors' standings. | Ferrari kept 11 and 12, Tyrrell 3 and 4 for over 20 years. Lauda came back with a third Ferrari at Monza 1976. |
| 1981 to 1984 | From 1981 every team must own the design of its own chassis. Spain 1981: the last privateer next to a works team. | Super licence from 1984. Drivers struck at Kyalami 1982 over the licence terms (?). | Fixed team numbers. | Privateers won 20 races from 1950 to 1981. |
| 1985 to 1995 | At most two cars per team from 1985. Renault's third car in Germany 1985 was the last. Up to 39 entries, pre-qualifying (to 1992). | Super licence. | Fixed team numbers. | Damon Hill raced as number 0 in 1993 and 1994, the champion had left the team. |
| 1996 to 2013 | Two cars per team. Grid of 20 to 24 cars. | Super licence. Test and reserve drivers in Friday practice (?). | New numbers each year by last year's constructors' standings. Champion's team keeps 1 and 2. No 13. | Customer cars stay banned. Super Aguri and Toro Rosso ran cars close to Honda and Red Bull designs, which led to disputes (?). |
| 2014 to 2021 | Two cars per team. 10 or 11 teams. | Penalty points from 2014: 12 in 12 months means a one-race ban. Changed after 2015: points system for the licence, at least 18 years old, 40 points over three seasons. | Each driver picks a number for the career, 2 to 99. Number 1 only for the champion. | Verstappen started at 17 in 2015, the reason for the age limit. Number 17 retired for Bianchi. |
| 2022 to 2025 | Two cars per team. New teams pay 200 million USD. | Rookies must drive in FP1, twice per car per season (?). Free practice licence from 2019. | Same. A number frees up after two seasons without racing. | Magnussen 2024: the only one-race ban so far for penalty points. |
| 2026 | 11 teams, 22 cars: Audi and Cadillac new. | Same. | Drivers may ask to change their number: Verstappen moved from 33 to 3. | |

## Super licence points (examples)

| Series | Points for positions 1 to 10 |
|---|---|
| Formula 2 | 40, 40, 40, 30, 20, 10, 8, 6, 4, 3 |
| Formula 3 | 30, 25, 20, 15, 12, 9, 7, 5, 3, 2 |
| Needed | at least 40 over the last three seasons |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Two or three cars per team | Yes | `formula_team_entry_cap` |
| More than three cars | No | C1 |
| Privateers with bought cars | No | C4 |
| Rookies or reserves in practice | Partly | `compulsory_reserve_sessions`: the reserve driver in N practice sessions a season, or a fine |
| Licence points from junior series | Partly | `driverslicense.json`: 10 points needed for a race seat |
| Penalty points, race bans | No | bans only for banned driver aids |
| Numbers per driver | Partly | a number per driver, not per entry (C3) |
| Guests for a few rounds | No | C2 |

## Sources

- Wikipedia, "FIA Super Licence" (1984 start, 2015 change, age, points,
  penalty points, Magnussen 2024), "List of Formula One constructors"
  (cars per team by era, 1981 chassis rule, privateers, 2026 teams), "List
  of Formula One driver numbers" (every number era, 0, 13, 17, 2026
  changes). From earlier research: 200 million fee, pre-qualifying, the
  rookie FP1 rule.
- Not confirmed, marked `(?)`: Kyalami 1982, Friday test drivers, the
  customer car disputes, the exact rookie FP1 count.
- Note: the super licence page says 1984, not 1982.

## Discord post

=== post | F1 entries and drivers history | f1-entries-drivers
## F1 entries and drivers, 1950 to 2026

Part eleven of the rules history. The table is below. What stood out to me:

- **Until 1981 anyone could buy a car and enter.** Privateers like Rob Walker raced next to the works teams and won 20 races. Since 1981 each team must own its chassis design.
- **Cars per team:** no limit in the 1950s, usually two plus a guest car in the 1960s and 1970s, at most two since 1985.
- **Super licence from 1984.** Since 2015 with an age limit (18) and points from junior series, after Verstappen started at 17. Penalty points since 2014: 12 means a race ban.
- **Numbers:** set per race until 1973, fixed per team from 1974, by standings from 1996, and since 2014 each driver picks one for the career.
- **Rookies in FP1:** since 2022 each team must give young drivers a few Friday sessions.

For the game this is the entry model from my earlier post: an entry is a car with a number, its drivers and the rounds it runs. Plus a few rules: cars per team, guest or third cars, privateers with a bought chassis, how numbers are given out, and a licence check. In DTM the same model covers guest drivers, privateer teams and the 1990s four-car teams.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
