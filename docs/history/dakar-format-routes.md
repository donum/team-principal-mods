# Dakar format and routes, 1979 to 2026

Part of the Dakar rules history (classes and vehicles, format and routes).
The table image is made with
`python -I tools/history_table.py docs/history/dakar-format-routes.md`.

`(?)` marks a detail that the sources we read did not confirm. The sources
had little on navigation and penalty rules.

## Table

| Years | Route | Stages | Rules | Quirks |
|---|---|---|---|---|
| 1979 to 1991 | Paris to Dakar, through Algiers (to 1988), Tunis (1989), Tripoli (1990, 1991). 10,000 to 15,000 km. | Long stages, some over 900 km a day (1,656 km in 1986). | Lowest total time, penalties included, wins each class. | 1986: founder Thierry Sabine dies in a helicopter crash. 603 starters in 1988. |
| 1992 to 2007 | Cape Town (1992), back to Paris (1994), Granada, Dakar to Cairo (2000), starts in Arras, Marseille, Clermont-Ferrand, Barcelona, Lisbon. | Same. | GPS used for the first time in 1992. 2001: an hour's penalty for unsporting conduct decides the car class. | 688 starters in 2005, a record. |
| 2008 | Cancelled after threats in Mauritania. | | | A substitute in Hungary and Romania counts as the official 2008 edition. |
| 2009 to 2019 | South America: Argentina, Chile, Bolivia, Peru, Paraguay (2017). 2019 only Peru. | Same. | Same: lowest total time, penalties included. | |
| 2020 to 2026 | Saudi Arabia. | 2024: a prologue and 12 stages, about 5,000 km of stages, a "48-hour chrono" stage with a night stop in the desert. | Part of the World Rally-Raid Championship from 2022. From 2020 a crew that drops out of a stage may rejoin as "Dakar Experience". In 2024 they get a time penalty (2 hours per missed stage for bikes) and do not count as finishers. RallyGP bikes may not restart. | 2027: Portugal to Morocco as a one-off (announced October 2026), back to Saudi Arabia in 2028. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Two weeks of stages, total time | No | N10 |
| Navigation with a road book | No | N10 |
| Restart after a missed stage with a penalty | No | N10 |
| Points in a world championship of several raids | Partly | `points_system` for the season, not per stage |

## Sources

- Wikipedia, "Dakar Rally" (routes, history, safety, 2008), "2024 Dakar
  Rally" (stages, 48-hour stage, restart rule), "World Rally-Raid
  Championship".
- "1979 Paris-Dakar Rally" (route via Algiers, start 26 December 1978,
  finish January 1979: this explains the 1978 or 1979 conflict).
- The Checkered Flag, "2024 Dakar Rally: 47 approved for Dakar
  Experience" (one restart, time penalties, last place in the results);
  "2020 Dakar Rally" (Dakar Experience already used).
- Autosport and RACER, October 2026 (2027 in Portugal and Morocco,
  pending FIA approval, Saudi Arabia again in 2028).
- Not found: navigation rules in detail, rest day rules. FIA 2024
  regulations: missing 40 percent of the waypoints in a stage counts as
  a retirement (The Checkered Flag, December 2023).
- ASO, "Rally Dakar 2024 Supplementary Regulations" (FIM, bikes and
  quads), art. 11.15 and 11.16: a stage penalty of 2 hours for a missed
  stage, no restart for RallyGP, more than 3 stage penalties means
  disqualification, riders who miss part of the route are "Dakar
  Experience", not finishers. This settles the 2024 conflict: the
  Wikipedia note "no Dakar Experience category" does not match the
  regulations.
- Confirmation round: Red Bull, "The toughest Dakar Rally" and
  Motor1 Spain, "40 años de historia del Dakar" (1986: 15,000 km,
  five stages over 900 km, Kiffa to Saint-Louis 1,656 km); old
  Wikipedia route list on academickids.com (Paris-Alger-Dakar to
  1988, Tunis 1989, Tripoli 1990 and 1991); Al Jazeera and RACER,
  30 October 2026 (2027 route, Saudi Arabia in 2028).
- Wikipedia, "2015 Dakar Rally" (overall standings by time, time
  penalties, for example for an engine change).

## Discord post

=== post | Dakar format history | dakar-format-routes
## Dakar format and routes, 1979 to 2026

Part two and the last of the Dakar rules history. The table is below. What stood out to me:

- **Three continents:** Paris to Dakar (1979 to 2007), South America (2009 to 2019), Saudi Arabia (from 2020), Portugal to Morocco in 2027.
- **Cancelled in 2008** after threats in Mauritania.
- **Two weeks, thousands of kilometres:** in 2024 a prologue, 12 stages and a 48-hour stage with a night in the desert.
- **Navigation is part of the race:** GPS first used in 1992, a road book ever since.
- **A crew that drops out of a stage can come back** (since 2020, the "Dakar Experience"), in 2024 with a heavy time penalty.

For the game this is a different sport: no circuit, no wheel-to-wheel racing, total time over two weeks. I added it to show where the rule system ends, not as a pack idea.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the Dakar series. Mistakes? Tell me!
