# GT World Challenge classes and balancing, 1997 to 2026

Part of the GT World Challenge rules history (classes and balancing, race
format and points). The SRO line: FIA GT Championship 1997 to 2009, FIA GT1
World Championship 2010 to 2012, Blancpain Endurance Series from 2011, a
sprint series from 2013 (FIA GT Series, then Blancpain Sprint Series from
2014), Blancpain GT Series 2014 to 2019, GT World Challenge Europe from 2020
(the sprint rounds from 2019). The table image is made with
`python -I tools/history_table.py docs/history/gtwc-classes-bop.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Series | Cars and classes | Balancing | Quirks |
|---|---|---|---|---|
| 1997 to 2009 | FIA GT Championship | GT1 and GT2 (1997, 1998), one GT class from 1999, N-GT added 2000 to 2004, GT1 and GT2 again from 2005. GT3 created for 2006 in its own series. | Weight penalties, extra limits on the Maserati MC12. | Spa 24 Hours part of the series 2001 to 2009. Titles for drivers and teams in each class, a makes' cup in some years from 2005. |
| 2010 to 2012 | FIA GT1 World Championship | GT1 cars (2010, 2011), GT3 only in 2012. | Weight and restrictor balancing, ballast for winners (to 2011). | |
| 2011 to 2015 | Blancpain Endurance Series, a sprint series from 2013 | GT3 (plus GT4 and Supersport in 2011). Pro, Pro-Am and Gentlemen classes. | "Extensive performance balancing and handicap weights" (2011, 2012). | Michelin tyres, Pirelli from 2013. |
| 2016 to 2022 | Blancpain GT Series, then GT World Challenge Europe | GT3 only. Pro, Silver (from 2018), Pro-Am, Am (own cup to 2020 in the Endurance Cup). | Balance of performance for GT3. | One to six cars per team. |
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
- Wikipedia "List of FIA GT Champions" (classes and titles per year).
  The Checkered Flag, December 2010 (2011 classes with GT4 and Supersport,
  Michelin 2011 and 2012, Pirelli from 2013).
- Not found: BoP per track. FIA GT Championship balancing is only
  described as weight penalties and MC12 limits.
- Wikipedia season articles: "2013 FIA GT Series" (first SRO sprint
  season after GT1, followed by the 2014 Blancpain Sprint Series), "2019
  Blancpain GT Series" (last season under the Blancpain name, sprint
  rounds called Blancpain GT World Challenge Europe), Endurance Cup 2019,
  2020 and 2021 (Am Cup standings in 2019 and 2020, not in 2021).
- The "GT World Challenge Europe" overview calls 2018 the last Am Cup
  season. The season articles show an Am Cup in the Endurance Cup to 2020.

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
