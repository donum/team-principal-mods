# American open-wheel points systems, 1979 to 2026

Part of the IndyCar rules history (points, qualifying and race, pit stops
fuel and tyres, cars and engines). Covers CART (1979 to 2003), Champ Car
World Series (2004 to 2007) and IRL / IndyCar (1996 to 2026). The table
image is made with
`python -I tools/history_table.py docs/history/indycar-points.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Series | Race points | Bonus points | Quirks |
|---|---|---|---|---|
| 1979 to 1980 | CART | By race distance: 2 points per mile for the winner. 200-mile race: 400-320-280 down to 20 for 12th, then 10 down to 2 for every finisher. | None. | A 500-mile race pays more than two 200-mile races. |
| 1981 to 1982 | CART | Same scale divided by 10: 20-16-14-12-10-8-6-5-4-3-2-1 per 100 miles. 1982: 300-mile points for all races of 300 miles and more. | Pole 1 and most laps led 1, per 100 miles. | |
| 1983 to 2003 | CART | 20-16-14-12-10-8-6-5-4-3-2-1, top 12, the same for every race. | Pole 1, most laps led 1. 2002 to 2003: also 1 for leading the slowest qualifying group. | |
| 1996 to 1997 | IRL | 35-33-32-31 down to 1, every car scores. | 1997: pole 2, most laps led 1. | 1996: points multiplied for Phoenix and Indianapolis (?). Sharp and Calkins were co-champions, there was no tie-break. |
| 1998 to 2003 | IRL | 50-40-35-32-30-28 down to 1 for 33rd. | Most laps led 2. Pole 3/2/1 (1998 to 2000 (?)). | Cars that did not start score from 1999. |
| 2004 to 2007 | Champ Car | 31-27-25-23-21 down to 1 for 20th. | Pole 1, fastest race lap 1, most positions gained 1, leading the slowest qualifying group 1. Leading a lap 1 (2004 to 2006). | The most bonus points of any era. |
| 2004 to 2012 | IndyCar | 50-40-35 down to 13 for 17th, then 12 and 10 for the rest of the 33. | Most laps led 3 (2004 to 2008), then 2. Pole 1 from 2009. | Non-starters full points (2004 to 2005), then half. Texas 2011: two short races with half points each. |
| 2013 to 2026 | IndyCar | 50-40-35 down to 5 for 25th, 5 for the rest. | Pole 1 (not at Indianapolis), leading a lap 1, most laps led 2. | Ties: most wins, then most 2nd places (2006 Hornish, 2015 Dixon). |

## Double points and Indianapolis qualifying points

| Years | Rule |
|---|---|
| 2014 | Double points at all 500-mile races: Indianapolis, Pocono, Fontana |
| 2014 to 2022 | Double points at the Indianapolis 500 |
| 2015 to 2019 | Double points at the season finale |
| 2023 on | No double points |
| 2010 to 2013 | Indy qualifying: 15-13-12 down to 6 for the top 9, 4 and 3 for the rest |
| 2014 | Indy qualifying: 33 down to 1 on Saturday, plus 9 down to 1 for the Fast Nine on Sunday |
| 2015 | Indy qualifying: no points, after last-minute rule changes |
| 2016 to 2017 | Indy qualifying: 42-40-38 down to 1, every starter |
| 2018 to 2021 | Indy qualifying: 9 down to 1 for the Fast Nine |
| 2022 on | Indy qualifying: 12 down to 1 for the top 12 |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Points for every finisher | Partly | own points list, long tables not tested |
| Pole point | Yes | `pole_point` |
| Most laps led bonus | Partly | oval mode only |
| Leading a lap bonus | No | B8 |
| Double points at one race | No | B3 |
| Qualifying points at one event | No | B8 |
| Points by race distance | No | B3 |
| Stage points | Partly | oval mode only |

## Sources

- Wikipedia, "List of American Championship car racing points scoring
  systems" (every table above, read in full), "IndyCar Series" (tie-break,
  1996 co-champions, via summary).
- Not confirmed, marked `(?)`: how the 1996 multiplier worked, the
  1998 to 2000 pole bonus.
- Not covered: Rookie of the Year rules, manufacturers' points.

## Discord post

=== post | IndyCar points history | indycar-points
## IndyCar points systems, 1979 to 2026

After F1 and DTM, here's American open-wheel racing (CART, Champ Car, IndyCar). The table is below. What stood out to me:

- **Points by distance (1979 to 1982):** 2 points per mile for the winner, so a 500-mile race paid much more than a short one.
- **Every car scores** in the IRL and IndyCar: down to 1 point (1996 to 2003), 10 points (2004 to 2012), 5 points (since 2013).
- **Bonus points everywhere:** pole, leading a lap, most laps led, and in Champ Car even fastest lap, most places gained and leading the slowest qualifying group.
- **Double points:** the Indy 500 (2014 to 2022), all 500-mile races (2014), the finale (2015 to 2019).
- **Points for Indianapolis qualifying,** changed almost every year: all 33 cars, the Fast Nine, the top 12, or none (2015).
- **1996:** two co-champions, because there was no tie-break.

For the game this means points per finishing place for every car, bonus points with conditions, a multiplier per race, points for a qualifying session at one event, and a tie-break rule. The oval mode has some of this already, so it could become a shared setting for all modes.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
