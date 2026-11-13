# NASCAR Cup cars, engines and entries, 1949 to 2026

Part of the NASCAR rules history (points and playoffs, race format and
cautions, cars and entries). The table image is made with
`python -I tools/history_table.py docs/history/nascar-cars-entries.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Car | Engine | Tyres and fuel | Teams and entries |
|---|---|---|---|---|
| 1949 to 1964 | Gen 1: road cars, no changes allowed at first. | Stock engines. | | Many makes, little factory help. |
| 1965 to 1980 | Gen 2: modified chassis. Wheelbase at least 115 in. | From 1970 big engines get a restrictor plate. 1971: special "Aero Warriors" limited to 305 cu in. 1975 to 1977: limit down to 358 cu in. | | Only US makes with factory support by the mid 1960s. |
| 1981 to 1991 | Gen 3: wheelbase 110 in for the smaller road cars. | 358 cu in V8, carburettor. 1987: smaller carburettors at Talladega and Daytona after Allison's crash, restrictor plates there from 1988. | | Chrysler leaves after 1985. Four GM brands in 1991. |
| 1992 to 2006 | Gen 4. 2003: one common template after "twisted" bodies. | Same, plates on superspeedways. | Goodyear, the only supplier since 1995. | Dodge back in 2001, Pontiac gone after 2004. |
| 2007 to 2012 | Car of Tomorrow, full time from 2008. Rear wing to 2010. | Same. 2012: fuel injection replaces the carburettor. | Sunoco race fuel, E15 from 2011. | Toyota joins in 2007, Dodge leaves after 2012. |
| 2013 to 2021 | Gen 6, 3,200 lb without driver and fuel (2013 sources: 3,300 lb). | 2019: tapered spacers replace plates. 2019 to 2021: 550 hp on big tracks, 750 hp on short tracks and road courses. | Goodyear, compounds set by NASCAR. Rain tyres on road courses from 2020. | 2016: charters, 36 safe places in a 40-car field. |
| 2022 to 2026 | Next Gen: spec parts for everyone, one centre wheel nut, sequential gearbox, independent rear suspension. | 670 hp on most tracks, 510 hp on Daytona, Talladega and Atlanta (?). | Same. | Chevrolet, Ford, Toyota. Dodge back from 2027 with Kaulig. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta, as an oval pack. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Car makes with works and customer engines | Yes | `engines.json`, engine contracts |
| Restrictor plates and power per track type | No | B2 |
| Spec parts for everyone (Next Gen) | Partly | ratings can be set level, teams still develop |
| Refuelling at stops | Yes | `oval_refueling`, `oval_fuel_tank` |
| Pit crews | Yes | oval pit crews |
| One tyre maker, wet tyres on road courses | Yes | `tyre_suppliers.json`, wet tyres |
| Four or more cars per team | Yes | `oval_team_entry_cap`, any number |
| Charters | Yes | `oval_charter_system` |
| Part-time entries | Yes | oval part-time and guest agreements |

## Sources

- Wikipedia, "NASCAR Cup Series" (car generations, engines, plates and
  spacers, manufacturers, charters, owner points), "Car of Tomorrow",
  "Generation 6 (NASCAR)", "Next Gen (NASCAR)", "Restrictor plate"
  (1987 carburettors, plates from 1988), "Tire war" and 1995 season
  (Goodyear alone from 1995, exclusive deal 1997).
- NASCAR.com and Racer, November 2026 (Dodge returns in 2027 with Kaulig).
- Game support from the 0.99.6 oval code (pit crews, charters, entry cap,
  part-time agreements).
- Conflict: Gen 6 weight, 3,200 lb without driver and fuel (Wikipedia)
  or 3,300 lb (2013 launch reports).
- Not found: crew size over the wall, team limits per owner.

## Discord post

=== post | NASCAR cars history | nascar-cars-entries
## NASCAR Cup cars, engines and entries, 1949 to 2026

Part three and the last of the NASCAR rules history. The table is below. What stood out to me:

- **Seven car generations,** from road cars with no changes (1949) to the Next Gen with spec parts and one wheel nut (2022).
- **The 358 cubic inch V8 since 1975,** carburettor until 2012.
- **Restrictor plates at Daytona and Talladega** from 1988, after Allison's 1987 crash, tapered spacers from 2019. Power changes by track type.
- **Charters from 2016:** 36 safe places in a 40-car field.
- **Makes come and go:** Chrysler leaves (1985), Dodge returns (2001), leaves (2012) and comes back in 2027, Toyota joins (2007).

Most of this works in the oval mode today: makes and engines, refuelling, pit crews, big teams, charters and part-time entries. The real gap is power per track type, the restrictor plate.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the NASCAR series. Mistakes? Tell me!
