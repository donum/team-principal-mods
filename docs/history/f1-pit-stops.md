# F1 pit stop rules, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops). Each file has the table, the sources and a Discord post. The table
image is made with `python -I tools/history_table.py docs/history/f1-pit-stops.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Why cars stop | Fuel | Pit lane, safety car, penalties | Quirks |
|---|---|---|---|---|
| 1950 to 1960s | Rarely. Damage, worn tyres, or a driver change. Most cars run the whole race without a stop. | Refuelling allowed, but cars start with enough fuel. | No speed limit, no safety car. | Until 1957 a driver can take over a team mate's car and the points are shared. A stop can take a minute or more (?). |
| 1970s to 1981 | Tyres only when damaged or for rain. | Refuelling allowed, nobody plans it. | First safety car in 1973 (Canada, a Porsche 914). Not used again for years. | A stop is a loss, so teams build tyres and cars to last the race. |
| 1982 to 1983 | Brabham plans a stop for fuel and tyres: start light on soft tyres, stop halfway (?). | Refuelling allowed until 1983. | No speed limit. | Brabham's idea works, others copy it, then refuelling is banned. |
| 1984 to 1993 | Tyres. Soft tyres plus one stop can beat running non-stop. | No refuelling. Fuel limit per race in the turbo years (?). | Safety car official from 1993. No pit speed limit yet. | Portugal 1989: Mansell reversed in the pit lane and was disqualified. Portugal 1991: a wheel came off as he left the box. |
| 1994 to 2004 | Fuel and tyres. One, two or three stops, chosen by strategy. | Refuelling back from 1994, over 12 litres per second. Stops last 6 to 12 seconds. | Pit lane speed limit after Imola 1994, where a loose wheel hurt mechanics. Stop-go and drive-through penalties (start year (?)). | Hockenheim 1994: fire at Verstappen's Benetton stop. A fire extinguisher man became standard. France 2004: Schumacher won with four stops. |
| 2005 | Fuel only. | Refuelling. | Tyres may not be changed, unless damaged or wet. | One set of tyres for qualifying and the race. |
| 2006 | Fuel and tyres. | Refuelling. | Same as 2004. | |
| 2007 to 2008 | Fuel and tyres. Both dry compounds must be used. | Refuelling. | Pit lane closed as soon as the safety car comes out. Entering early: 10 s stop-go, unless out of fuel (?). | Cars low on fuel got a penalty for a stop they had to make. Singapore 2008: Piquet crashed on purpose just after Alonso's early stop. Massa drove off with the fuel hose still on. |
| 2009 | Fuel and tyres. | Refuelling, last year. | Pit lane open under safety car again. A minimum lap time to the pits stops cars racing in. | Red light at pit exit under safety car. Hamilton hit Räikkönen there in Canada 2008. |
| 2010 to 2013 | Tyres only. Both dry compounds must be used. | No refuelling. Cars start with fuel for the whole race. | Lapped cars may not unlap under the safety car (2010 to 2011). | Stops drop to about 3 seconds. Germany 2013: Webber's wheel hit a cameraman. Crew helmets became mandatory and the speed limit came down (?). |
| 2014 to 2020 | Tyres only. | Fuel limit per race, 100 kg, later 110 kg (?). | 5 s time penalty served at the next stop: nobody may touch the car for 5 s (?). Virtual safety car from 2015. Unsafe release: penalties and fines. | A stop under safety car or VSC costs less, so teams wait for one. Bahrain 2018: a Ferrari hit a tyre changer. Brazil 2019: Red Bull stop in 1.82 s. |
| 2021 to 2024 | Tyres only. | Fuel limit per race (?). | Restart rules after a safety car tightened (2022 ?). | Abu Dhabi 2021: Verstappen stopped for softs under the safety car, Hamilton didn't. The restart rules were changed after. Qatar 2023: McLaren stop in 1.80 s, the fastest so far. |
| 2025 | Tyres. Monaco: at least two stops. | Fuel limit per race (?). | | At Monaco teams used the extra stops for team play: one car slows the field while the other stops. |
| 2026 | Tyres. At least two dry compounds, unless it is wet. | Energy and fuel limits change with the new engines (?). | | Monaco two-stop rule dropped. |

## Rules across all years

- Under a red flag, teams may work on the car and change tyres in the pit
  lane (?).
- A typical crew today: four wheel gunners, eight tyre carriers, front and
  rear jack men, two stabilisers, front wing men and a fire extinguisher
  man. One crew for both cars, so a "double stack" makes the second car
  wait.
- Driving through the pit lane costs between about 15 and 30 seconds
  depending on the track. That loss is why stops are a strategy at all.

## Sources

- Wikipedia, "Pit stop" (refuelling years, stop times, crew, fires,
  records), "Safety car" (pit closure 2007 to 2008, 2009 change, VSC 2015,
  unlapping rules).
- From the tyres and qualifying research: 2005 tyre rule, two-compound rule,
  Monaco 2025 and 2026.
- Not confirmed, marked `(?)`: 1950s stop times, Brabham 1982, turbo fuel
  limits, penalty start years, speed limit values, 5 s penalty rules, fuel
  limits per year, red flag work.

## Discord post

=== post | F1 pit stop history | f1-pit-stops
## F1 pit stop rules, 1950 to 2026

Last part of the rules history (after qualifying, points and tyres). The table is below. What stood out to me:

- **For 30 years nobody planned a stop.** Cars ran the whole race. Brabham started planned stops in 1982, then refuelling was banned from 1984.
- **Refuelling 1994 to 2009.** Stops of 6 to 12 seconds, strategy by fuel load. Fires and a car leaving with the hose on.
- **Since 2010 only tyres.** About 2 to 3 seconds, the record is 1.80 s.
- **The safety car changes everything.** 2007 to 2008 the pit lane was even closed under the safety car, so a car low on fuel got a penalty for stopping.
- **Penalties at the stop:** drive-through, stop-go, 5 and 10 second time penalties served at the next stop, unsafe release.
- **Must-stop rules:** both dry compounds since 2007, two stops at Monaco in 2025.

For the game this is: why a car has to stop (fuel, tyre rule, minimum stops), what is allowed during a stop (fuel, tyres, driver change), pit lane loss per track, pit lane closed or open under the safety car, cheap stops under SC/VSC, and penalties served at a stop. In DTM the same blocks cover the pit windows, the two mandatory stops in 2013 and the 2025 rules.

That's the whole series: qualifying, points, tyres, pit stops. If you spot a mistake, tell me!
