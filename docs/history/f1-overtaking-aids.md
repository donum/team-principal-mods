# F1 overtaking aids, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops, race format, safety car, overtaking aids). Each file has the table,
the sources and a Discord post. The table image is made with
`python -I tools/history_table.py docs/history/f1-overtaking-aids.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Aid | How it works | Limits | Quirks |
|---|---|---|---|---|
| 1950 to 1967 | None. Slipstream only. | Follow close on a straight, pull out at the end. | | Cars have no wings, so following close costs little grip (?). |
| 1968 to 1969 | Movable high wings (Lotus and others). | Wings on tall struts on the suspension, some the driver could flatten on the straights. | Banned in 1969 after crashes in Spain: wings fixed to the body, no moving parts, a height limit. | The ban came in the middle of the Monaco weekend. "No moving aero parts" stays the rule for 40 years. |
| 1970 to 2008 | None. | | Moving aero parts banned. Fan car 1978: Brabham ran once and won, then it was withdrawn (?). | Wings and ground effect make following hard. Overtaking becomes rare (?). |
| 2009 | Adjustable front wing flap. KERS. | Flap: driver changes the angle by up to 6 degrees, at most twice per lap. KERS: about 60 kW for about 6.7 s per lap, by button. | KERS optional. Used by Ferrari, McLaren, Renault and BMW. Renault and BMW stopped during the year. | Hungary 2009: Hamilton, first win with KERS. Belgium 2009: Räikkönen passed with KERS boost. |
| 2010 | F-duct (McLaren, then others). No KERS. | The driver covers a hole in the cockpit with his leg. Air stalls the rear wing, about 10 km/h more on straights. | KERS still allowed, teams agree not to use it. | Legal because no part moves. Red Bull protested, the FIA said OK. |
| 2011 to 2013 | DRS. KERS again. | Rear wing flap opens up to 85 mm in a zone, if within 1 s of the car ahead at the detection point. | From lap 3, and 2 laps after a safety car restart. Off in the wet. Free use in practice and qualifying until 2012, zones only from 2013 (?). F-duct banned, front wing flap gone (?). | Montreal and Valencia 2011: two zones in a row, the car passed in the first can re-pass in the second. Minimum weight up 20 kg for KERS. |
| 2014 to 2021 | DRS. ERS doubles to 120 kW. | Same DRS. Electric power used all lap, a "boost" button helps attack and defence (?). | 2018 to 2019: some tracks get a third zone. | "DRS trains": a line of cars all within 1 s, each with DRS, nobody can pass (?). |
| 2022 to 2025 | DRS. | Same. Ground effect cars to make following easier (?). | From 2024: DRS from lap 2 and 1 lap after a restart. Up to 4 zones (Melbourne, Singapore). | Zones were changed after the FIA found DRS too easy at some tracks. DRS ends after 2025: Button was the first user in 2011, Antonelli the last. |
| 2026 | Active aero and overtake mode. | All cars: front and rear wings flatten on straights ("straight-line mode") and close for corners. Overtake mode: extra electric energy within 1 s of the car ahead. | Electric power up to 350 kW, engine 400 kW. Monaco: active aero off. | Every car opens its wings, not only the chaser. The extra energy is now the overtaking help. |

## DRS rules in short (2011 to 2025)

| Rule | Setting |
|---|---|
| Gap | within 1 s at the detection point (FIA could change it per race) |
| Where | only in the activation zone, 1 to 4 per track |
| When | from lap 3 (lap 2 from 2024), not under SC or VSC, 2 laps after a restart (1 from 2024) |
| Wet | race director can switch it off |
| Closes | button released or brakes |
| Effect | about 10 to 12 km/h at the end of the zone (FIA), others say 4 to 5 |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| DRS in zones, within 1 s | Yes | `drs_policy`, zones per track |
| DRS only in the race, per session rules | No | B6 |
| DRS uses per lap or race | No | B6 |
| KERS and ERS | Yes | `ers_policy` |
| Push-to-pass with a set number of uses | Partly | ERS spec stands in (B13) |
| Active aero, overtake mode (2026) | No |  |

## Sources

- Wikipedia, "Drag reduction system" (rules, zones, 2024 change, end in
  2025, first and last users, DTM since 2013), "Kinetic energy recovery
  system" (2009 users, 2010 pause, 2011 return, 2014 doubling), "McLaren
  MP4-25" (F-duct), season articles 1969, 2009, 2011 and 2026 (via
  summaries).
- Not confirmed, marked `(?)`: grip loss from following before wings,
  the 1978 fan car, overtaking numbers, the 2013 qualifying change, when the
  front flap ended, DRS trains, ERS boost button, ground effect intent.
- Open conflict: DRS speed gain, 4 to 5, 10 to 12 or 15 km/h.

## Discord post

=== post | F1 overtaking aids history | f1-overtaking-aids
## F1 overtaking aids, 1950 to 2026

Part seven of the rules history. The table is below. What stood out to me:

- **Moving wings were banned in 1969** after crashes, and stayed banned for 40 years.
- **2009 to 2010 was a busy time:** a front wing flap the driver could adjust, KERS with a boost button, and McLaren's F-duct where the driver covered a hole with his leg.
- **DRS from 2011 to 2025:** within 1 s at the detection point, only in a zone, not early in the race, not after a restart, not in the wet. Up to 4 zones per track.
- **2026:** every car flattens its wings on the straights. The help for the chasing car is now extra electric energy (overtake mode), again within 1 s.

The DRS rules fit in a small table (in the picture). For the game this is: an aid with a condition (gap at a point), where it works (zones per track), when it works (lap, after a restart, weather), which sessions, and how much it helps. DTM fits the same settings: DRS from 2013 in the race only, and later push-to-pass with a number of uses per race. A boost button with a limited number of uses is the same idea as KERS.

The last table in the picture shows what the game can do today: yes, partly or no.

Next up: engines and grid penalties. Mistakes? Tell me!
