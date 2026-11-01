# DTM 1991 results: sources

All CSVs were extracted from touringcarracing.net race pages (fetched 2026-11-01; the site only serves plain http).
Cross-checked against German Wikipedia: https://de.wikipedia.org/wiki/Deutsche_Tourenwagen-Meisterschaft_1991 (pole, fastest lap, winner, race distance; no lap times).

| Files | Source URL |
|---|---|
| 01-zolder-* | http://touringcarracing.net/Races/1991%20Zolder%20DTM.html |
| 02-hockenheim-* | http://touringcarracing.net/Races/1991%20Hockenheim%20DTM.html |
| 03-nuerburgring-* (Eifelrennen, 21 Apr) | http://touringcarracing.net/Races/1991%20Nurburgring%20Eifel.html |
| 04-avus-* | http://touringcarracing.net/Races/1991%20Avus.html |
| 05-wunstorf-* | http://touringcarracing.net/Races/1991%20Wunstorf.html |
| 06-norisring-* | http://touringcarracing.net/Races/1991%20Norisring.html |
| 07-diepholz-* | http://touringcarracing.net/Races/1991%20Diepholz.html |
| 08-nuerburgring-* (GP der Tourenwagen, 8 Sep) | http://touringcarracing.net/Races/1991%20Nurburgring.html |
| 09-alemannenring-* (Singen) | http://touringcarracing.net/Races/1991%20Singen.html |
| 10-hockenheim-* (ADAC-Preis, 29 Sep) | http://touringcarracing.net/Races/1991%20Hockenheim%20ADAC.html |

Season index: http://touringcarracing.net/Pages/1991%20DTM.html

## How the files were built

- `*-qualrace.csv`, `*-heat1.csv`, `*-heat2.csv`: the source tables row by row. `time` is the source time converted from `mm.ss,cc` to `mm:ss.cc`. `status` is `classified` or the source code (DNF/DNS/DSQ/NC). `notes` holds the source "reason out" remark plus the grid or qualifying position and time printed in that row.
- `gap` is **derived**: the time minus the winner's time on the same lap, or `+N laps`. It is not in the source.
- `fastest_lap` is filled only where the source marks it. The source marks only the heat's fastest lap, not every driver's best lap.
- `*-qualifying.csv`: the source has **no separate qualifying table**. This file merges the "qualifying position / qualifying time" columns from the three session tables, one row per car. `pos` is a **derived** rank by lap time. The position the source prints is in `notes`. That position is not always the time order: penalties apply, and drivers outside the top 16 went through the qualification race. `status`: `qualified (top grid)` means the driver was in the heat 1 table with a direct grid slot. `via qualification race` means the driver was in the qualification race. `DNQ` means the driver was in the qualification race but is not in the heat 1 table.
- Driver names keep the source's nationality suffix ("Johnny Cecotto, YV").

## Unverified points and discrepancies

- **R8 Nürburgring (8 Sep):** touringcarracing gives van Ommen pole (1:41.49) and the heat 1 fastest lap. Wikipedia gives Roland Asch both (pole and heat 1 fastest lap). Van Ommen was disqualified after the race for non-compliant fuel. That probably explains the gap; the source says this was later reversed but he did not get his points back. Asch's own qualifying time was 1:41.58. The heat 1 fastest lap is 1:53.52 in the table but 1:43.52 in the page header. The heat 1 winning time (43:18.41, about 138 km/h) does not match the header average speed (152.340 km/h). The heat 2 time (38:25.87, 156.0 km/h) does not match the header (151.976 km/h) either. The weather is given as "rainy and cool", so heat 1 may have been wet. None of this is resolved.
- **R7 Diepholz:** the source says 38 laps for both heats. Wikipedia gives 99.530 km for heat 1, which is 37 laps of 2.690 km, and 102.220 km for heat 2, which is 38 laps. The source's average speeds (158.280 and 159.504 km/h) both fit 37 laps better than 38. The lap count for heat 1 is unverified, and possibly heat 2 as well.
- **R5 Wunstorf:** the source says heat 2 was shortened to 19 laps. Wikipedia lists 101.0 km (20 laps) for both heats.
- **R10 Hockenheim (29 Sep):** the qualification race lap count is marked "8?" in the source. The winner's time gives 199 km/h at 8 laps, which is implausible in the rain, so the lap count is wrong. Heat 1 was red-flagged and shortened to 12 laps. Wikipedia agrees: 81.624 km.
- The lap counts for the qualification races at R3 and R8 (Nürburgring, "12?") and R9 (Singen, "18?") are marked uncertain in the source.
- **R9 Singen heat 2:** the winning time of 57:24.69 includes a long pace-car period after the Lohr/Asch accident. It does not represent a racing pace.
- Track length: touringcarracing gives 6.797 km for Hockenheim in April and 6.802 km in September. The Wikipedia distances (102.030 km = 15 × 6.802) support 6.802 km.
- Some lapped finishers have only a lap count and no time. Some `pos` gaps exist (for example Avus heat 2 has no P21) because the source table has them.
