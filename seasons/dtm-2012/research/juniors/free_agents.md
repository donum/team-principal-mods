# Extra free agents (DTM 2012 pack)

A small pool of drivers outside the covered feeder series (DTM, Formula 3 Euro Series, German F3, Carrera Cup Deutschland, ADAC Formel Masters, ADAC Procar) who could plausibly join a DTM team in 2012. Data in `free_agents.csv`.

- `f1_starts` counts F1 starts before the 2012 season.
- `f1_years` lists F1 race seasons before 2012.
- `status_2012` is what the driver actually did in 2012.
- Nobody in the list is on the 2012 DTM grid (checked against research/entries.csv).

## Suggested (6)

### BMW test driver

- **Marco Wittmann.** BMW's official DTM test driver in 2012, with no race seat. He only raced GT3 cars in endurance events. Joined the DTM in 2013 with BMW Team MTEK (8th, best rookie) and won the title in 2014. The clearest real link. **Raced DTM 2013.**

### Ex-F1

- **Adrian Sutil.** Lost his Force India seat and did not race in 2012. Returned to F1 with Force India in 2013. German, so a natural DTM fit in the game, but no real DTM link was found.
- **Lucas di Grassi.** Pirelli test driver in 2012 and one WEC race for Audi. Tested the Audi RS 5 DTM in 2013. A plausible Audi pick.
- **Jaime Alguersuari.** No racing in 2012 (Pirelli tester, radio work). Only 22. No real DTM link.
- **Sébastien Buemi.** Red Bull reserve in 2012 and a Toyota WEC debut. Tied to Red Bull and Toyota, so only a game pick.

### Ex-DTM

- **Renger van der Zande.** Raced DTM in 2011 for Mercedes (Persson). Dropped for 2012 and raced only a few WEC and Supercup rounds.

## Suggested ratings for gen.json

DTM skills run 11-18. Ratings are a judgement, set in the same range as the 2013 picks.

| Driver | Skill | Talent | Age on 1 March 2012 |
|---|---|---|---|
| Marco Wittmann | 13 | 84 | 22 |
| Adrian Sutil | 15 | 78 | 29 |
| Lucas di Grassi | 14 | 78 | 27 |
| Jaime Alguersuari | 13 | 80 | 21 |
| Sébastien Buemi | 14 | 80 | 23 |
| Renger van der Zande | 12 | 72 | 26 |

Age note: by season year minus birth year, Wittmann (23), Alguersuari (22), Buemi (24) and van der Zande (26) fall inside the 2013 F3 Euro age band (16-26), and some inside the Carrera Cup band (17-28). The importer will print a note that they can take a feeder seat.

## Not suggested, short reasons

- Timo Glock: F1 race seat with Marussia in 2012, so not free. Joined BMW for DTM 2013.
- Jarno Trulli: dropped by Caterham in February 2012, but 37 at season start.
- Nick Heidfeld: WEC race seat with Rebellion.
- Not checked in depth: Kubica (recovering from his 2011 rally injury), Liuzzi, Klien, Chandhok, d'Ambrosio (Lotus reserve with one 2012 GP start).

## Later DTM 2013 drivers and their 2012 series

- Daniel Juncadella: Formula 3 Euro Series champion with Prema (in `f3_euro`).
- Pascal Wehrlein: Formula 3 Euro Series runner-up with Mücke (in `f3_euro`).
- Marco Wittmann: no race series, BMW test driver (free agent here).
- Timo Glock: F1 with Marussia (not a free agent).

## Uncertain

- Glock's F1 starts are not filled in, and his and Trulli's birth dates are from general knowledge, not a fetched source. Neither is suggested.
- Sutil's DTM link: none found in the part of his Wikipedia page that was read.
- Buemi: the read part of his page does not mention DTM.

## Sources

- https://en.wikipedia.org/wiki/Marco_Wittmann
- https://en.wikipedia.org/wiki/Adrian_Sutil
- https://en.wikipedia.org/wiki/Lucas_di_Grassi
- https://en.wikipedia.org/wiki/Jaime_Alguersuari
- https://en.wikipedia.org/wiki/S%C3%A9bastien_Buemi
- https://en.wikipedia.org/wiki/Renger_van_der_Zande
- https://en.wikipedia.org/wiki/Daniel_Juncadella
- seasons/dtm-2013/research/juniors/free_agents.md (Heidfeld, di Grassi DTM test)
