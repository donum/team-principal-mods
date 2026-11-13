# IMSA race format, drivers and points, 1971 to 2026

Part of the IMSA rules history (classes and balancing, race format and
points). The table image is made with
`python -I tools/history_table.py docs/history/imsa-race-format-points.md`.

`(?)` marks a detail that the sources we read did not confirm. The sources
had no points values, qualifying format or pit rules.

## Table

| Years | Races | Start and drivers | Qualifying | Points and titles |
|---|---|---|---|---|
| 1971 to 1998 | Daytona 24 h (6 h in 1972, none in 1974), Sebring 12 h, Watkins Glen 6 h (500 km or 3 h in some years), Road America 500 miles. | Rolling starts (Sebring from 1970, Daytona from 1971). Two to five drivers per car. | Not stated (?). | Titles per class. Not stated how points were given (?). |
| 1999 to 2013 | ALMS: Sebring 12 h, Petit Le Mans 10 h or 1,000 miles, sprints of 2 h 45 or 4 h. | Rolling start. GT Pro and Am in one class with no driver limits (?). | Not stated (?). | Class champions and runners-up got Le Mans invitations. |
| 2014 to 2020 | Daytona 24 h, Sebring 12 h, Watkins Glen 6 h, Petit Le Mans 10 h, sprints of 2 h 40. | Three to five drivers at Daytona. Amateurs must drive a set time (?). | Not stated (?). | Drivers', teams' and manufacturers' titles per class. North American Endurance Cup from 2014 (Michelin from 2019): points during the race, every 6 h at Daytona, every 4 h at Sebring. |
| 2021 to 2026 | Same. Road America 6 h from 2026. | Driver ratings decide the line-ups: GTD needs a Bronze or Silver driver, LMP2 at most one Gold. | LMP2: only the Bronze driver qualifies. | Points for qualifying since 2021, worth 10% of the race points. Three champions get a Le Mans invitation (?). |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Races by time (24, 12, 10, 6 hours) | No | A3 |
| Rolling start | No | oval packs only (A3) |
| Several drivers per car, driver ratings | No | C8 |
| Qualifying by a set driver | No | A6, C8 |
| Points for qualifying | Partly | pole point only (B8) |
| Points at set times during a race (Endurance Cup) | No | B3 |
| Titles per class, an extra endurance cup | No | B4 |
| Refuelling | Yes | `formula_refueling` |

## Sources

- Wikipedia, "IMSA SportsCar Championship" (driver rating rules, points
  for qualifying, titles), "24 Hours of Daytona", "12 Hours of Sebring",
  "6 Hours of Watkins Glen", "Petit Le Mans", "SportsCar Endurance Grand
  Prix" (race lengths, starts), "List of IMSA SportsCar Championship
  champions" (Endurance Cup points times).
- Autosport, Racer, Sportscar365 2020 reports (qualifying points from
  2021). Sportscar365, Racer (Road America 6 h in 2026). Wikipedia "12 Hours
  of Sebring" (rolling start from 1970).
- Not confirmed, marked `(?)`: the ALMS driver rule, which champions get a
  Le Mans invitation.
- Not found: race points values, qualifying format, pit and refuelling rules,
  drive time limits, full-course yellow rules. The IMSA rulebook is the
  next place to check.

## Discord post

=== post | IMSA race format history | imsa-race-format-points
## IMSA race format, drivers and points, 1971 to 2026

Part two and the last of the IMSA rules history. The sources had no points values or pit rules, so this is mostly race lengths and line-ups. What stood out to me:

- **The big races are by time:** Daytona 24 hours, Sebring 12, Petit Le Mans 10 (or 1,000 miles, whichever came first, until 2013), Watkins Glen 6, sprints of 2 hours 40.
- **Rolling starts** since 1970 at Sebring and 1971 at Daytona.
- **Line-ups by driver rating:** GTD needs a Bronze or Silver driver, LMP2 at most one Gold, and in LMP2 only the Bronze driver qualifies.
- **Points during the race** in the Endurance Cup: every 6 hours at Daytona, every 4 at Sebring.
- **Points for qualifying** since 2021.

For the game this is the entry model and the weekend builder together: crews with ratings, rules on who may qualify, races by time, and points at set times during a race.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the IMSA series. Mistakes? Tell me!
