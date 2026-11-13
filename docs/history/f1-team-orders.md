# F1 team orders, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops, race format, safety car, overtaking aids, engines, parc fermé and
weight, money and testing, entries and drivers, team orders). Each file
has the table, the sources and a Discord post. The table image is made
with `python -I tools/history_table.py docs/history/f1-team-orders.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Rule | Typical orders | Examples | Quirks |
|---|---|---|---|---|
| 1950 to 1957 | Allowed. A driver may hand his car to the team leader during the race, the points are shared. | Give up your car, let the leader win. | 1955 Aintree: Mercedes asked Fangio to let Moss win at home, Fangio finished under a second behind. Monza 1956: Collins handed his car to Fangio, who won the title (?). | The order could be "get out of your car". |
| 1958 to 1980 | Allowed. Car swaps no longer score. | Let the team mate in the title fight pass. Hold position. | Mexico 1964: Bandini let Surtees through, Surtees won the title. Germany 1979: Regazzoni told not to attack Jones. | |
| 1981 to 1996 | Allowed. | Same. Drivers start to refuse. | Brazil 1981: Reutemann ignored the order to let Jones pass, lost the title later by one point. France 1982: Arnoux did not let Prost pass. Imola 1982: Pironi passed Villeneuve against the team's plan (?). France 1992: Patrese waved Mansell through. | Refusing an order can split a team for the rest of the year. |
| 1997 to 2002 | Allowed. | Swap places, hold up the rivals, start light to block. | Australia 1998: Coulthard let Häkkinen win, an agreement before the race. Germany 1999: Salo gave Irvine the win, his only chance of a win. Austria 2002: Barrichello let Schumacher win on the last lap. USA 2002: Schumacher let Barrichello win by 0.011 s. | Austria 2002: Schumacher put Barrichello on the top step. The FIA fined Ferrari and both drivers for the podium, not for the order. |
| 2003 to 2010 | Banned: no team orders that change the race result. | Coded radio messages. | Singapore 2008: Renault ordered Piquet to crash, to bring out the safety car for Alonso. Germany 2010: "Fernando is faster than you", Massa let Alonso pass, Ferrari fined 100,000 USD, result kept. | Teams still gave orders, in code. The FIA said at the end of 2010 that the rule was not working. |
| 2011 to 2026 | Allowed again. Only a deliberate crash or similar is punished (?). | Hold position, swap back, let the faster car through, grid tricks. | US 2012: Ferrari broke Massa's gearbox seal for a grid penalty, to put Alonso on the clean side. Malaysia 2013: Vettel ignored "Multi 21" and passed Webber. Hungary 2017: Bottas let Hamilton pass, Hamilton gave the place back. Russia 2018: Bottas gave up the win to Hamilton. Brazil 2022: Verstappen refused to give a place to Perez. Hungary 2024: Norris gave the win back to Piastri. Italy 2025: McLaren swapped Norris and Piastri after a slow stop, Norris won the title by 2 points. | Orders now happen on open radio, the fans hear them live. |

## What a team order can be

| Order | Example |
|---|---|
| Let the team mate pass | Austria 2002, Germany 2010, Russia 2018 |
| Hold position, don't attack | Germany 1979, Malaysia 2013, Australia 2019 |
| Swap back after a pass | Hungary 2017, Hungary 2024 |
| Hand over the car | 1950s, points shared |
| Help the team mate on strategy | Japan 1997: Irvine started light to hold up the Williams cars |
| Take a penalty for the team mate | USA 2012: gearbox seal broken for a grid drop |
| Crash on purpose | Singapore 2008, punished |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Team orders during the race | Yes | built in |
| Driver refuses, team mood | Partly | team-order tension between drivers |
| Ban on team orders, fines | No |  |
| Car handover, shared points | No | C8 |

## Sources

- Wikipedia, "Team orders" (almost every example, the 2003 ban, the end
  of the ban for 2011), "2002 Austrian Grand Prix" (the fine), "2010 German
  Grand Prix" (radio quote, fine), "2013 Malaysian Grand Prix" (Vettel and
  Webber, via summary for "Multi 21").
- Not confirmed, marked `(?)`: Monza 1956, Imola 1982, whether any rule on
  orders is left after 2011.
- Conflicts: how much of the 2002 fine was paid, and on which lap the
  order came.

## Discord post

=== post | F1 team orders history | f1-team-orders
## F1 team orders, 1950 to 2026

Part twelve of the rules history, maybe the most team-boss one. The table is below. What stood out to me:

- **In the 1950s a driver could hand his car to the team leader** during the race and they shared the points.
- **Allowed for 50 years.** Let the team mate pass, hold position, and drivers who refused (Reutemann 1981, Arnoux 1982).
- **Austria 2002** changed it: Barrichello let Schumacher win on the last lap, and from 2003 orders that change the result were banned.
- **The ban didn't work.** Teams used coded messages. "Fernando is faster than you" (2010) cost Ferrari 100,000 USD, and the ban was dropped for 2011.
- **Since 2011 allowed again,** and now on open radio: Multi 21 (2013), Bottas in Russia (2018), McLaren's swaps (2024, 2025).

For the game this is a team boss decision during the race: order a swap, hold position, swap back, or leave them racing. Drivers can follow or refuse, and that changes their mood. Plus a season setting: orders allowed, banned (with a fine if caught), or the 1950s car handover. That would also fit DTM, where each make ran 6 to 8 cars.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
