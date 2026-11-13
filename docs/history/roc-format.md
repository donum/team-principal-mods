# Race of Champions, 1988 to 2025

A one-off event once a year: drivers from every kind of racing race each
other head-to-head in identical cars, usually in a stadium. Here as a
proof of concept for show events. The table image is made with
`python -I tools/history_table.py docs/history/roc-format.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Venue | Format | Cars | Quirks |
|---|---|---|---|---|
| 1988 to 1991 | Montlhéry (1988, for Henri Toivonen), then Nürburgring, Barcelona, Madrid. | 1988: the world rally champions of 1979 to 1988, timed runs on a rally stage. Head-to-head on a parallel track from 1989. | Group B and Group A rally cars: Audi Quattro S1, Peugeot 205 T16, Lancia Delta. | Kankkunen beats Salonen in the first final. |
| 1992 to 2003 | Gran Canaria. | Head-to-head knockout. Nations' Cup for two-driver teams from 1999. | Rally cars. | Side events for rally masters and classic Porsche 911s. |
| 2004 to 2012 | Stadiums: Stade de France, Wembley, Beijing's Bird's Nest, Düsseldorf, Bangkok. | Knockout only to 2008. From 2009 groups first, then the best eight in a knockout. The final is best of three runs. Two titles: Champion of Champions and the Nations' Cup. | Identical cars per run, chosen for each heat: ROC buggy, KTM X-Bow, Audi R8 LMS, Lamborghini, VW Scirocco, a EuroNASCAR Camaro (2010 to 2012). | Germany wins six Nations' Cups in a row. Kovalainen first non-rally winner (2004). 2013 cancelled (unrest in Bangkok). |
| 2014 to 2020 | Barbados, London, Miami, Riyadh, Mexico City. 2020 held online. | Same, eROC for sim racers from 2018. | Same idea. | Riyadh 2018: the first international motorsport event in Saudi Arabia. |
| 2022 to 2025 | Snow and ice at Piteå, Sweden (2022, 2023), Sydney (2025). | Same. | 2022: electric RX2e, Porsche Cayman GT4, Polaris side-by-sides, SuperCar Lites. 2025: KTM X-Bow, Toyota GR86, Subaru BRZ, SuperCar Lites. | No event in 2021, 2024 and 2026. 2027 planned for Wellington, New Zealand. |

The DTM's own version, the Munich Olympic Stadium races of 2011 and 2012,
is in `dtm-munich-show.md`.

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Head-to-head races on a parallel track | No | N11 |
| Round robin, then a knockout bracket | No | N11 |
| A one-off event outside the championship | No | A4, N11 |
| Identical cars handed out per heat | No | C9 |
| Team title for two drivers (Nations' Cup) | No | B4 |

## Sources

- Wikipedia, "Race of Champions" (history, format, venues, cars, winners
  to 2017), "2011 Deutsche Tourenwagen Masters season" and "2012 ..."
  (Munich events), "Olympiastadion (Munich)" (why it ended).
- Wikipedia "Race of Champions" car table (EuroNASCAR 2010 to 2012,
  cars of 2022 and 2025), editions list (2021 COVID-19, 2024 land use at
  Piteå, 2026 none, 2027 Wellington).
- Winners from 2018 are not used in the table. Cross-checked: 2018
  Coulthard (Autosport, RACER), 2019 Benito Guerra, who beat Duval in
  the final (RACER, Autosport; the earlier note "2019 Duval" was wrong),
  2022 Loeb (RACER, Formula1.com), 2023 Ekström (RACER, Formula1.com),
  2025 Loeb, his fifth (RACER, Speedcafe).
- Group stage: Wikipedia "2004", "2006", "2007" and "2008 Race of
  Champions" show knockout brackets only. "2009 Race of Champions" and a
  2009 preview on carmag.co.za describe four groups, then the best
  eight in a knockout.
- Wikipedia, "1988 Race of Champions" (the only edition run as timed
  single-car stages) and "1989 Race of Champions" (first parallel
  track, head-to-head in identical cars); Goodwood and Motor Sport,
  January 1989 (Audi Quattro S1, Peugeot 205 T16, Lancia Delta in
  1988).
- Not confirmed: prize money. Munich 2012 winners come from a summary
  of the season page.

## Discord post

=== post | Race of Champions history | roc-format
## Race of Champions, 1988 to 2025

A proof of concept for show events, plus the DTM's own stadium races in Munich. The table is below. What stood out to me:

- **Head-to-head in identical cars:** two drivers race each other on a stadium track, the car changes from heat to heat.
- **A round robin, then a knockout:** the best eight go into a bracket, the final is best of three.
- **Two titles:** Champion of Champions and the Nations' Cup for two-driver teams.
- **DTM in Munich's Olympic Stadium (2011, 2012):** the whole field over two days, no points. Races between the makes, relay races and knockout races. Dropped because it couldn't become a points event.

For the game: a one-off event with its own format, a bracket, and identical cars. It would make a fun mid-season event in a pack, and it shows what the weekend builder would need beyond normal races.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
