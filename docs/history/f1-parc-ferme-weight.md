# F1 parc fermé and minimum weight, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops, race format, safety car, overtaking aids, engines, parc fermé and
weight). Each file has the table, the sources and a Discord post. The
table image is made with
`python -I tools/history_table.py docs/history/f1-parc-ferme-weight.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Parc fermé | What may change | Checks after the race | Quirks |
|---|---|---|---|---|
| 1950 to 2002 | None between qualifying and race. | Anything: a new setup for the race, a race engine, the spare car (?). | Weight and legality checks, more and more over the years (?). | Brabham and Williams 1982: water tanks "for brake cooling" were emptied in the race and refilled before weighing. Piquet and Rosberg were disqualified in Brazil (?). Tyrrell 1984: lead in the water tank, the whole season struck off (?). |
| 2003 to 2020 | From qualifying until the race. Cars in a closed area overnight. | Only small things: tyres, fuel (to 2009), brake bleeding, front wing angle. Weather change: the race director can allow setup changes. Big damage: repairs allowed. | Fuel sample of at least 1 kg, weight, parts. | Breaking parc fermé: start from the pit lane. Teams pick a setup for qualifying and race at once. Spain 2012: Hamilton's car had too little fuel for the sample after qualifying, he started last (?). |
| 2021 to 2023 | Starts at the start of qualifying, so FP3 is the last chance to change setup (?). Sprint weekends: from Friday qualifying, after the only practice. | Same small things. | Same. Hungary 2021: Vettel disqualified, too little fuel for the sample (?). | USA 2023: Hamilton and Leclerc disqualified, the plank under the car was worn too much (?). |
| 2024 to 2026 | Sprint weekends: two periods, from sprint qualifying to the sprint, then from qualifying to the race. | Setup may change once between the sprint and qualifying. | Same. Spa 2024: Russell won but was disqualified, the car was 1.5 kg too light (?). | Teams can fix a bad sprint setup before qualifying. |

## Minimum weight

| Years | Minimum weight | Notes |
|---|---|---|
| 1950 to 1960 | None (?) | |
| 1961 to 1965 | 450 kg (?) | car without driver |
| 1966 to 1971 | 500 kg (?) | |
| 1972 to 1982 | 550 to 585 kg (?) | |
| 1983 to 1988 | 540 kg, 500 kg for cars without turbo in 1987 and 1988 (?) | turbo and non-turbo cars side by side |
| 1989 to 1994 | 500 to 505 kg (?) | |
| 1995 to 2008 | 595 to 605 kg (?) | now car and driver together |
| 2009 to 2010 | 605 kg, then 620 kg | heavier for KERS |
| 2011 to 2013 | 640 kg (2011), 642 kg (2013 (?)) | KERS back |
| 2014 to 2021 | 691 kg (2014), rising to 752 kg (2021) (?) | hybrid engines, wider cars from 2017. From 2019 the driver counts as at least 80 kg, lighter drivers carry ballast near the seat (?) |
| 2022 to 2025 | 798 kg, 800 kg in 2025 (?) | ground effect cars, 18-inch wheels |
| 2026 | 768 kg (?), Wikipedia says 724 kg | first big drop in weight |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Setup frozen after qualifying | Yes | the setup is locked for the race, only tyre pressures on the grid |
| Minimum weight | Yes | `chassis_minimum_weight` |
| Weight change from a season | Yes | `scripted_changes` |
| Driver weight, ballast | No | B1 |
| Checks after the race, disqualification | Partly | only the tyre rule and banned driver aids |

## Sources

- Wikipedia, "Parc fermé" (rules since 2003, allowed work, exceptions,
  pit lane start), "Formula One regulations" (weighing after qualifying,
  2026 weight 724 kg, sprint pit lane times), "Formula One car" (fuel
  sample, widths, 798 kg). From earlier research: parc fermé from 2021,
  two sprint periods from 2024, 2010 and 2011 weights for KERS.
- Not confirmed, marked `(?)`: almost every weight before 2009 and from
  2013 on, the 80 kg driver rule, all disqualification cases, what was
  allowed before 2003.
- Open conflict: 2026 minimum weight, 724 kg (regulations page) or 768 kg.
  The F1 car page also gives 798 kg without a year.

## Discord post

=== post | F1 parc fermé and weight history | f1-parc-ferme-weight
## F1 parc fermé and minimum weight, 1950 to 2026

Part nine of the rules history. The table is below. What stood out to me:

- **Until 2002 teams could change anything** between qualifying and the race: setup, engine, even the spare car.
- **Since 2003 parc fermé:** the car you qualify is the car you race. Only small things may change. A team that breaks it starts from the pit lane.
- **Sprint weekends** have one parc fermé from Friday (2021 to 2023), then two (since 2024), so the setup can change once.
- **Checks after the race** decide results: fuel sample, weight, plank wear. Russell lost a win in 2024 for 1.5 kg.
- **Minimum weight:** about 450 kg in the 1960s, about 800 kg in 2025, and down again with the 2026 cars. Since 2019 the driver counts as at least 80 kg.
- **Cheating with weight:** water tanks for "brake cooling" in 1982, lead in the water in 1984.

For the game this is: when the setup is frozen (none, after qualifying, after FP3, two periods on sprint weekends), what may still change, the penalty for breaking it, and a minimum weight per era. A minimum weight per make or class would also cover DTM: the 1991 weights per make and success ballast.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
