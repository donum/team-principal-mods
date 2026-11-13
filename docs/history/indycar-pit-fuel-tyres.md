# American open-wheel pit stops, fuel and tyres, 1979 to 2026

Part of the IndyCar rules history (points, qualifying and race, pit stops
fuel and tyres, cars and engines). Covers CART (1979 to 2003), Champ Car
World Series (2004 to 2007) and IRL / IndyCar (1996 to 2026). The table
image is made with
`python -I tools/history_table.py docs/history/indycar-pit-fuel-tyres.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Fuel | Tank | Tyres | Pit stops |
|---|---|---|---|---|
| 1979 to 1995 | Methanol, the standard since the 1964 Indy 500 fire. | | Goodyear, Firestone back in CART later (?). | Refuelling with a gravity hose. 1991: pit lane speed limits after a crash at Long Beach. |
| 1996 | Methanol. | | Firestone and Goodyear in the IRL. | |
| 1997 to 2003 | Methanol, with colour added so flames can be seen at night. | 35 US gallons (132 L). | Firestone and Goodyear (to 1999), Firestone alone from 2000. Own compounds per corner, new profile in 2003. | |
| 2004 to 2005 | Methanol. | 30 gallons (114 L). | Firestone. | Fuel hose with a built-in vent from the mid 2000s. |
| 2004 to 2007 | Champ Car: methanol (?). | | Bridgestone sponsor. Special tyres for a set part of the race (?). | |
| 2006 | 90% methanol, 10% ethanol. | | Firestone. | |
| 2007 to 2011 | "100% ethanol", really 98% ethanol and 2% petrol. | 22 gallons (83 L). | Firestone. Road courses: primary and alternate dry tyres (start year (?)), plus rain tyres, no intermediates. | |
| 2012 to 2022 | E85: 85% ethanol. | 18.5 gallons (70 L). | Same. Ovals: one tyre, different sizes left and right. | Single wheel nut, tyres premounted. A routine stop takes 6 to 10 seconds. |
| 2020 to 2022 | E85. | | | Seven crew over the wall, the seventh only cleans the aeroscreen. |
| 2023 to 2026 | 100% ethanol-based fuel (Shell). | | Firestone (Bridgestone). | |
| 2024 to 2026 | Hybrid: energy from braking (from Mid-Ohio 2024). | | | |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Refuelling at every stop | Yes | `formula_refueling` |
| Tank size | Partly | `formula_fuel_tank` 60, 80 or 100 kg |
| Fuel type (methanol, ethanol) | No |  |
| Primary and alternate tyres, both used | Partly | two-compound rule (B12) |
| One tyre on ovals | Partly | oval mode |
| Crew over the wall | No | B10 |
| Hybrid | Partly | `ers_policy` |

## Sources

- Wikipedia, "IndyCar Series" (fuel types and years, tank sizes, tyre
  suppliers and specs, hybrid), "Pit stop" (IndyCar stop procedure, crew
  of seven, 1991 speed limit), "Champ Car World Series", "Dallara DW12"
  (hybrid at Mid-Ohio 2024).
- Not covered: pit lane closed under yellow, pit speed values, the rule to
  use both road course tyres, refuelling fires, CART fuel and tyres before
  1996.

## Discord post

=== post | IndyCar pit stops and fuel history | indycar-pit-fuel-tyres
## IndyCar pit stops, fuel and tyres, 1979 to 2026

Part three of the IndyCar rules history. The table is below. What stood out to me:

- **Refuelling never stopped.** A gravity hose into the car, with fuel and four tyres at the same time. A stop takes 6 to 10 seconds.
- **The fuel changed:** methanol (since the 1964 Indy fire), a methanol and ethanol mix (2006), almost pure ethanol (2007), E85 (2012), and fully ethanol-based fuel since 2023.
- **Smaller tanks** as the fuel changed: 35 gallons, 30, 22, now 18.5. So a fuel-saving race plays out differently in every era.
- **Tyres:** a tyre war between Firestone and Goodyear until 1999, then Firestone alone. Primary and alternate tyres on road courses, one tyre on ovals with different sizes left and right.
- **Crew:** seven over the wall since 2020, the seventh only cleans the aeroscreen.
- **Hybrid** since mid-2024.

For the game: refuelling as part of a stop (F1 had it 1994 to 2009 too), a tank size and fuel type per era so fuel saving matters, and crew size per stop. The rules engine from my earlier posts already covers the tyre rules.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
