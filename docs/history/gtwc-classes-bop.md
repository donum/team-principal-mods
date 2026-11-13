# GT World Challenge classes and balancing, 1997 to 2026

Part of the GT World Challenge rules history (classes and balancing, race
format and points). The SRO line: FIA GT Championship 1997 to 2009, FIA GT1
World Championship 2010 to 2012, Blancpain Endurance and Sprint Series from
2011 and 2013, Blancpain GT Series 2014 to 2019, GT World Challenge Europe
from 2019 or 2020. The table image is made with
`python -I tools/history_table.py docs/history/gtwc-classes-bop.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Series | Cars and classes | Balancing | Quirks |
|---|---|---|---|---|
| 1997 to 2009 | FIA GT Championship | GT1 and GT2, N-GT from 2000, GT3 created for 2006 in its own series. | Weight penalties, extra limits on the Maserati MC12. | Spa 24 Hours part of the series 2001 to 2009. Titles for drivers, teams and makes in each class. |
| 2010 to 2012 | FIA GT1 World Championship | GT1 cars (2010, 2011), GT3 only in 2012. | Weight and restrictor balancing, ballast for winners (to 2011). | |
| 2011 to 2015 | Blancpain Endurance Series, Sprint Series from 2013 | GT3 (plus GT4 and Supersport in 2011). Pro, Pro-Am and Gentlemen classes. | "Extensive performance balancing and handicap weights" (2011, 2012). | Michelin tyres, Pirelli from 2013. |
| 2016 to 2022 | Blancpain GT Series, then GT World Challenge Europe | GT3 only. Pro, Silver (from 2018), Pro-Am, Am. | Balance of performance for GT3. | One to six cars per team. |
| 2023 to 2026 | GT World Challenge Europe | Pro, Gold, Silver, Bronze by FIA driver rating. Pro-Am ended after 2023 (only at Spa). | BoP. | The Bronze Cup winner gets a Le Mans entry. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Classes by driver rating in one race | No | B4, C8 |
| Balance of performance for GT3 | No | B2 |
| Up to six cars per team | No | C1 |
| One tyre maker | Yes | `tyre_suppliers.json` |

## Sources

- Wikipedia, "GT World Challenge Europe", "FIA GT Championship", "FIA GT1
  World Championship", "GT World Challenge Europe Endurance Cup" and
  "Sprint Cup" (classes, names, years, Le Mans entry, Michelin 2011 and
  2012, Pirelli from 2013), FIA GT1 World Championship balancing and
  ballast. 2024 Spa reports (Pro-Am class still run at Spa).
- Not found: BoP per track. FIA GT Championship balancing is only
  described as weight penalties and MC12 limits.
- Conflicts: when the Blancpain name ended (2018 or 2019), when the Am Cup
  ended (2018 or 2020), when the sprint series began (2013 or 2014).

## Discord post

=== post | GT World Challenge classes history | gtwc-classes-bop
## GT World Challenge classes and balancing, 1997 to 2026

The SRO's GT series, from FIA GT to today's GT World Challenge. The table is below. What stood out to me:

- **GT1, GT2, then GT3:** GT3 was created in 2006 and has been the only car type since 2012.
- **Classes by driver rating,** not by car: Pro, Gold, Silver, Bronze. All in the same GT3 cars.
- **Balance of performance** for many makes in one class.
- **Up to six cars per team.**
- **The Bronze Cup winner gets a Le Mans entry.**

For the game: classes by driver rating are the entry model again (crews with ratings) plus "more titles and classes". BoP and big teams are the same requests as in DTM and endurance.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
