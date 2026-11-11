# Wish List for the Team Principal Developer

These are feature requests from building historically accurate DTM season
packs: 1990–1992 (Group A), 2012 and 2013. Each item lists the real-world need,
what the game can't do today, our current workaround, and what would solve
it. **Needed by** names the season packs (`seasons/dtm-*`) that would use
it. Findings are based on game version 0.99.5, rechecked against the
0.99.6 beta's modding guide (no item closed). See
[CAPABILITIES.md](CAPABILITIES.md) for what we confirmed works.

Priority: **P1** = needed for an authentic series, **P2** = big gain,
**P3** = nice to have.

Whenever a pack hits something the game can't do, it goes in here (a new
item, or the season added to an existing one), and in that pack's README
under "Simplifications".

| Season | Items |
|---|---|
| dtm-1990 | A1, B1, B2, D1, E1, E2 |
| dtm-1991 | A1–A4, B1–B4, C1–C5, D1–D4, E1–E7 |
| dtm-1992 | A1, B2, B3, C1, C2, D1, E1, E2 |
| dtm-2012 | A5, B5, B7, C4, D1, D3, D5, D6, D7, D8, E1, E2, E4, E5, E6, E8, E9, E12, E15 |
| dtm-2013 | A3, A5, B5, B6, B7, C4, C6, C7, D1, D3, D4, D5, D6, D7, D8, E1, E2, E4, E5, E6, E8, E9, E10, E11, E12, E13, E14, E15 |

Seasons without a pack yet (research only) are covered for qualifying and
race rules in [dtm_rules.html](dtm_rules.html), which maps every season's
rules to these items:

| Seasons | Items |
|---|---|
| dtm-1984 to dtm-1989 | A1, A2, A3, A5, B1, B2, B3, B7, B9 |
| dtm-1993 to itc-1996 | A1, A5, B2, B4, D2 |
| dtm-2000 to dtm-2011 | A1, A2, A3, A5, B1, B2, B3, B5, B7, B8, B10, B11 |
| dtm-2014 to dtm-2018 | A1, A3, B1, B5, B6, B7, B8, B9, B10 |
| dtm-2019 to dtm-2020 | A1, A3, B4, B6, B7, B8 |
| dtm-2021 to dtm-2026 | A3, B1, B2, B3, B4, B5, B7, B8, B9, B10, B11 |

---

## A. Race weekend format

### A1. Several races per weekend (heats) · P1
- **Needed by:** dtm-1990, dtm-1991, dtm-1992 (each runs one race per round at heat distance).
- **1991:** every DTM round had **two heats of about 100 km**, both with full
  points. The heat-2 grid was the heat-1 finishing order.
- **Today:** one race per scheduled week.
- **Workaround:** one race at heat distance, which gives half the season's
  points and races.
- **Request:** a weekend definition in data, e.g.
  `"races": [{"distance_km": 100}, {"distance_km": 100, "grid": "previous_result"}]`,
  with points per race. Grid options: `qualifying`, `previous_result`,
  `reversed_top_n`.

### A2. Qualification race · P1
- **Needed by:** dtm-1991.
- **1991:** places 1–16 came from qualifying. All other cars ran a ~50 km
  **qualification race** for places 17+.
- **Today:** no way to model this. Our 39-car field either all starts or is
  cut by DNQ.
- **Request:** a session type `qualification_race`, with `direct_grid_slots`
  and `distance_km`.

### A3. Configurable sessions and start · P2
- **Needed by:** dtm-1991, dtm-2013 (the wet 2013 Nürburgring and final Hockenheim races were time-limited to 75 minutes).
- **Request:** two qualifying sessions (best time counts), standing or
  rolling start, red-flag and restart rules (Hockenheim 1991 heat 1 was
  stopped for rain and shortened), and race distance in km or minutes
  instead of `laps × lap_modifier`.

### A4. More than one event per week · P3
- **Needed by:** dtm-1991.
- **1991:** two rounds were on consecutive weekends (Nürburgring 8 Sep,
  Singen 15 Sep).
- **Today:** that works, but a double-header at one venue on one weekend
  can't be scheduled.
- **Request:** allow several events per week slot, or a real-date calendar
  (day of year).

### A5. Single-lap shootout (Q4) · P2
- **Needed by:** dtm-2013, dtm-2012 (the top 4 also had a single-lap shootout).
- **2013:** the four fastest from Q3 ran one timed lap each, alone on the
  track, for the first two rows.
- **Today:** the game's knockout stops at Q3.
- **Workaround:** the Q3 order is the grid.
- **Request:** a qualifying stage with `cars`, `laps_each: 1` and
  `run_order: "reverse"`.

## B. Rules and balance of performance

### B1. Success ballast · P1
- **Needed by:** dtm-1990 (up to 100 kg), dtm-1991.
- **1991:** weight penalties of up to **50 kg**, given for good results and
  removed for poor ones. Drivers new to the series started on the maximum.
- **Today:** not possible.
- **Request:** a regulation category with a per-position kg table, a
  maximum, a removal rule, and a value for newcomers.

### B2. Mid-season balance changes on a date · P1
- **Needed by:** dtm-1990 (Audi's 80 kg at Diepholz; the Mercedes 190E Evo II from the Nordschleife round), dtm-1991, dtm-1992 (BMW's bigger splitter and wing from the Nordschleife round).
- **1991:**
  - Audi had **40 kg removed from Wunstorf** onwards.
  - Opel could remove **50 kg after Hockenheim**.
  - Minimum weights depended on displacement and drivetrain (BMW and
    Mercedes 980 kg, Opel 1130 kg, Audi 1290 kg).
- **Today:** since 0.99.6 the guide documents `scripted_changes` rows
  (`key`, `effective_season`, `new_regulation`), but only per season, not per
  week or per make. The minimum weight is one global value.
- **Request:**
  - Scripted rule changes tied to season and week, e.g.
    `{"season": 1, "week": 23, "engine": "Audi", "mass_kg": -40}`.
  - Minimum weight per engine or car model.

### B3. Points table per race, drop scores · P2
- **Needed by:** dtm-1991, dtm-1992 (drop scores).
- **Request:** points tables per session (heat 1 and heat 2 can differ),
  qualification-race points, and drop scores (Streichresultate, used in
  1992).

### B4. More classifications · P2
- **Needed by:** dtm-1991.
- **1991:** besides the drivers' title there were a **teams'** and a
  **manufacturers'** title (only the best car of each make scored), the
  **ITR Fahrerpokal** (DTM plus the non-championship Brno and Donington
  rounds) and a **privateer cup** paid in prize money.
- **Request:** a list of championships in data, each with its own events,
  points rules and eligible entries (e.g. `"privateer": true`).

### B5. Mandatory pit stops · P1
- **Needed by:** dtm-2013, dtm-2012 (two mandatory stops, each inside a pit window).
- **2013:** **two mandatory stops**, no pit window, but none in the first or
  last 3 laps.
- **Today:** no regulation can require a number of stops.
- **Workaround:** tyre wear per track (`tyre_wear_mult`) is tuned so two
  stops is the fastest strategy. In season 5, 160 of 220 cars stopped twice;
  the rest stopped between zero and seven times.
- **Request:** `mandatory_stops: 2` with `no_stop_first_laps` and
  `no_stop_last_laps`.

### B6. DRS rules per session · P2
- **Needed by:** dtm-2013.
- **2013:** DRS in the **race only**, free use once per lap anywhere on the
  track, and not in the last 3 laps.
- **Today:** `drs_policy` is on or off for the whole weekend, so qualifying
  gets DRS too (8 km/h). It works in zones only, from lap 3, with no ban on
  the last laps.
- **Workaround:** one zone on each track's longest straight. Qualifying top
  speeds come out high (season 5: 285 km/h at Hockenheim).
- **Request:** DRS settings per session (`qualifying: false`), a per-lap
  activation budget instead of zones, and `disable_last_laps`.

### B7. Tyre allocation rules · P2
- **Needed by:** dtm-2013, dtm-2012 (one dry tyre for the whole season; the pack keeps the soft as a copy of the hard, since the game's need for a soft can't be checked).
- **2013:** the Hankook hard was the standard tyre, plus **one set of the
  option (soft) per race**, which every driver had to use.
- **2013 look:** the tyres were called **standard** (white sidewall) and
  **option** (yellow sidewall). There was no medium.
- **Today:** `formula_compound_usage` asks for two different dry compounds,
  with no limit on sets. The weekend allocation screen always lists soft,
  medium and hard, even when `tyremodel.json` sets the medium to null:
  `DRY_COMPOUNDS` is fixed in `managers/weekend_tyre_allocation.py` and in
  the screen. The presets also hand out medium sets. Compound names and
  colours (red, yellow, white) are fixed in the screens' code.
- **Workaround:** the two-compound rule. The player sets the medium to 0 by
  hand each weekend.
- **Request:** a set limit per compound and race, and "must use compound X"
  as a rule. Take the dry compounds for the allocation screen and presets
  from `tyremodel.json` (see D8 for names and colours).
- **Other seasons:** 3 to 9 sets per weekend (2000 to 2006, 2015, 2019,
  2022 on; the game's lowest allocation is 12), a cap of half the race
  distance on the option (2014), the top 5 or top 10 must start on their
  qualifying tyres (2023 on), tyre warmer bans (2003, 2017).

### B8. Qualifying points · P2
- **Needed by:** dtm-2001, dtm-2002 (3-2-1 for the qualifying race), dtm-2017 to dtm-2026 (3-2-1 for the top three in qualifying), dtm-2022 (fastest-lap point only for a top-10 finisher).
- **Today:** `pole_point` gives +1 to pole only, and `fastest_lap_point`
  gives +1 to the fastest-lap holder wherever they finish.
- **Workaround:** pole point on, which gives 1 point instead of 3 and
  nothing to second and third.
- **Request:** a qualifying points table (`[3, 2, 1]`), and an optional
  `min_finish_position` for the fastest-lap point.

### B9. Non-scoring guest entries · P2
- **Needed by:** dtm-1984 (only German drivers scored), dtm-1987 (guest Ludwig won round 7 and scored nothing), dtm-2018, dtm-2021 to dtm-2026 (guest and wildcard drivers).
- **Today:** every entry scores.
- **Request:** a `guest: true` flag on a driver or entry. Guests race and
  are classified, but the points go to the next eligible drivers.

### B10. Pit-stop procedure rules · P3
- **Needed by:** dtm-2001 (25-minute service window between the races), dtm-2017 (8 mechanics, one wheelgun per side), dtm-2021 (a stop under safety car doesn't count), dtm-2022 to dtm-2026 (rear wheels first, 4 to 6 crew).
- **Today:** one stop-time model for every pack; no setting for crew size
  or what counts as the mandatory stop.
- **Request:** `pitstops.crew_size` or a base stop time per pack, and rules
  for which stops count (`not_under_sc`, `not_under_fcy`).

### B11. Race control rules · P3
- **Needed by:** dtm-2007 (pit lane closed under the safety car), dtm-2022 to dtm-2026 (full-course yellow at 60 km/h), dtm-2023 to dtm-2026 (penalty lap).
- **Today:** `safety_car_policy` picks the safety car and the virtual
  safety car. The VSC stands in for the FCY.
- **Request:** `pit_lane_closed_under_sc`, and a penalty-lap penalty type
  next to time penalties.

## C. Entries, teams and drivers

### C1. More than 3 cars per team · P1
- **Needed by:** dtm-1991, dtm-1992 (AMG ran 4 cars; Lohr is a reserve).
- **1991:** AMG ran **4 cars**, and some teams went up to 5.
- **Today:** `formula_team_entry_cap` stops at `three`.
- **Workaround:** Kreutzpointner (AMG #87) is a reserve driver.
- **Request:** allow 4–6 entries.

### C2. Entry lists per round (part-timers and guests) · P1
- **Needed by:** dtm-1991, dtm-1992 (Audi withdrew after round 6; in the game it races all season).
- **1991:**
  - Michael Schumacher drove 2 rounds for Zakspeed.
  - Walter Röhrl drove 1 round for SMS.
  - Bernd Schneider joined Zakspeed from round 8.
  - Jochen Mass did 3 rounds for MS-Jet.
- **Today:** contracts run the whole season.
- **Request:** a per-round entry list, or a contract with `rounds: [6, 7]`,
  so AI teams follow history in season 1.

### C3. Car numbers per entry and fixed numbers · P2
- **Needed by:** dtm-1991.
- **1991:** numbers went to the entry, like Ludwig #8 and Stuck #1, not
  per-team pairs.
- **Today:** numbers work, but reserves and guests can't keep their real
  numbers.
- **Request:** a `number` on the contract, including for reserves.

### C4. Customer cars and homologation · P2
- **Needed by:** dtm-1991, dtm-2013 (chassis and aero were homologated and largely frozen; in the game teams develop at different rates, and in season 5 the gap between the fastest and slowest car grew from 3.6 to 4.3 rating points), dtm-2012.
- **1991:** privateers bought homologated cars (Evo models) from BMW,
  Mercedes and Opel. Chassis development was mostly the manufacturer's job,
  not the team's.
- **Today:** every team designs its own chassis.
- **Request:** a "customer car" contract type, like engines, where chassis
  and aero performance come from the supplier's homologated model. Also
  homologation steps (Evo kits) as data.

### C5. Retirement and age tuning in data · P3
- **Needed by:** dtm-1991.
- **1991:** drivers raced competitively into their 40s and 50s (Quester was
  51, Laffite 47).
- **Today:** we changed `DRIVER_RETIREMENT_*` in `constants.py`.
- **Request:** expose these in JSON (see E2).

### C6. Driver timing codes · P3
- **Needed by:** dtm-2013.
- **2013:** every driver had a three-letter code on the timing screens and
  on the car (SPE, WER, PAF; Scheider was TSC, not SCH).
- **Today:** `drivers.json` has no field for it.
- **Workaround:** none. The codes are kept in
  `seasons/dtm-2013/research/spotter_guide.csv`.
- **Request:** an optional `code` per driver, shown in timing towers and
  results.

### C7. Feeder series with real race weekends · P2
- **Needed by:** dtm-2013 (five real feeder series in `junior_series.json`).
- **2013:** FIA F3 Europe and ADAC Formel Masters ran 3 races per weekend,
  German F3, the Carrera Cup and the DTC 2. The DTC scored two classes
  separately. German F3 gave points for pole and
  fastest lap, and its second race used a different points table.
- **Today:**
  - A junior series races at most once a week, so a weekend is one race.
  - Points go by finishing position only, with one table for all races.
  - The result is driver skill + 2 × team quality + luck. The track is
    only a label, and a venue without a track file has no country flag.
  - Feeder teams have colours but no logo, and the named drivers are only
    seated in the first season.
  - Any free driver inside a series' age band can take an open seat. A
    pack cannot keep a driver out, so ex-F1 drivers waiting for a DTM
    seat would race in F3 or the Carrera Cup.
- **Workaround:** one race per weekend, with the main race's points table.
  Venues of the DTM calendar use the DTM track ids. Every feeder stops at
  age 28, below the ex-F1 free agents (29 and up). The older gentleman
  drivers of the Carrera Cup, the DTC and the German F3 Trophy class are
  left out, among them the DTC champion Jens-Guido Weimann. The young
  Red Bull juniors still fit the F3 bands.
- **Request:** `races_per_event` and a points table per race (with
  pole/fastest-lap bonus) for junior series, a `nationality` per schedule
  entry, an optional team logo, and a per-driver flag (for example
  `"junior_eligible": false`) that keeps a free driver out of feeder seats.

### C8. Driver crews per car (endurance) · P3
- **Needed by:** no current pack. Fits the developers' planned endurance
  update.
- **Today:** one driver per car. Session tabs and timing are per driver.
- **Request:**
  - Entries as the unit: an entry has a car, a number, a car image (E4)
    and one to three drivers. Session tabs show entries; the driver card
    shows the crew.
  - Drive-time rules as pack data: minimum per driver, maximum stint,
    maximum total.
  - Fatigue that rises with stint length, heat and night driving.
  - A stint planner with an AI plan the player can accept or edit. AI
    teams use the same rules: swap at a stop that is already needed, give
    the faster driver the start and the finish, give the better wet driver
    the rain stint.

## D. Cars and simulation

### D1. Touring-car part set · P1
- **Needed by:** dtm-1990, dtm-1991, dtm-1992, dtm-2013, dtm-2012.
- **Today:** the parts are open-wheel ones (front and rear wing, underfloor,
  diffuser, sidepods), plus ERS and DRS.
- **Request:** data-defined part categories with labels and effects, so a
  pack can use e.g. splitter, rear spoiler, suspension, brakes, gearbox and
  tyres. Also a way to remove categories completely.
- **2013 workaround:** the six slots are relabelled through
  `car_parts.json` (front splitter, rear wing, underbody, diffuser, side
  bodywork, monocoque), with low wear per lap. The Aerodynamics screen in
  the Development Centre uses the pack's `abbr` in the part codes
  (FS-13-A-1, UB-13-A-1). Other screens not yet checked.
- **Part drawings:** the Aerodynamics screen draws open-wheel sketches (an
  F1 front wing, a rear wing on a pylon). They load from the install
  folder (`ui/assets/aero/frontwing.png`, `rearwing.png`, `floor.png`,
  `diffuser.png`, `sidepod.png`), not from the pack. Swapping them there
  changes every pack and a game update puts them back. The Car Setup
  screen has the same problem: its controls say "Front Wing" and "Change
  Wing", and a touring car has a front splitter and dive planes instead. The stat names on
  the cards (Low Speed, Dirty Air...) are fixed in code too.
- **Request (art):** a pack folder for part drawings (for example
  `assets/parts/<part_key>.png`), used before the game's own, and a
  drawing per part category once categories are data-defined. The `front_wing` key still drives
  the lap-one damage outcome and the "wing damage" radio bank.

### D2. Drivetrain · P2
- **Needed by:** dtm-1991.
- **1991:** the 4WD Audi V8 had a big advantage in the wet. In Hockenheim's
  wet heat 2 the Audis finished about a minute clear.
- **Request:** a `drivetrain` value (`rwd` / `fwd` / `awd`) that affects
  traction, wet performance and tyre wear.

### D3. Documented lap-time controls · P1
- **Needed by:** dtm-1991, dtm-2013 (we fitted lap times by running the game's physics model offline), dtm-2012.
- **What we found:**
  - `lap_modifier` sets the **number of laps**: race laps = `options.laps`
    × `lap_modifier`.
  - Lap time follows the micro-sector speeds and `car_profile`.
  - `track_time_mult` exists on some base tracks but is undocumented.
- **Request:**
  - Document every track and car field.
  - Add an explicit per-track lap-time multiplier.
  - Add a calibration helper that shows the expected pole time for a
    track and car profile.

### D4. Weather realism · P3
- **Needed by:** dtm-1991, dtm-2013 (a track has one
  `wet_weather_probability_multiplier` for every visit, so the May and
  October Hockenheim rounds can't have different rain chances).
- **Request:** weather probability per date and region (e.g. April in the
  Eifel), or at least per schedule round, red-flag or restart for heavy rain, and tyre changes to wets as
  real strategy.

### D5. Wider car-profile range · P2
- **Needed by:** dtm-2013, dtm-2012.
- **What we found:** `car_profile` multipliers must stay within 0.5–1.5 (the
  game raises an error otherwise). A 2013 DTM car (about 480 hp, 1,110 kg,
  a lot of drag) needs more drag and less acceleration than that allows.
- **Workaround:** drag 1.5 and acceleration 0.5, the limits. Top speeds still
  come out about 10 km/h high.
- **Request:** a wider range, or a profile given as power (hp), drag area and
  downforce instead of multipliers.

### D6. Damage repair at pit stops · P2
- **Needed by:** dtm-2013 (and the Group A packs), dtm-2012.
- **Real world:** a DTM front end is the splitter, bumper and bodywork, not
  a nose cone that clips off. After contact the crew pulls off loose
  pieces or tapes them up, and the driver carries the damage to the end.
  Swapping the front end costs far more than a tyre stop, so it rarely
  happens in a race.
- **Today:** contact sets part damage (`incidents.*_part_damage_fraction`,
  the lap-one `front_wing` outcome), and the pit-stop settings
  (`pitstops`) cover only tyre wear, pit-lane loss and stop failures.
  Seen in a 2013 race event log: "FRONT WING DAMAGE: <driver> has severe
  front wing damage", then at the next stop "FRONT WING: <driver> changed
  front wing". So the game swaps the part F1-style, and no setting turns
  that off or makes it slower.
- **Workaround:** lap-one pile-ups no longer break the front wing
  (`front_wing` 0.3 → 0, its share moved to `time_loss`), contact damages
  parts half as much as vanilla, and the radio lines say the driver carries
  on. Contact later in the race can still break it, and then it's swapped.
- **Request:** a per-pack `damage_repair` setting under `pitstops`: `none`
  (drive on with the damage), `repair` (fixed extra time, e.g. 20–40 s,
  restores part of the damage) or `swap` (today's behaviour), ideally per
  part.

### D7. Development freeze and homologation · P2
- **Needed by:** dtm-2013, dtm-2012.
- **Real world:** 2013 DTM cars were homologated before the season, and
  aero development was largely frozen during it. Teams built spares to
  replace crash damage, not new designs.
- **Today:** teams design and build new part versions all season, as in
  F1. `build_cost_m` and `staff_hours` in `car_parts.json` are
  manufacturing values, so raising them only makes spares scarce; it
  doesn't stop development.
- **Workaround:** none.
- **Request:** a regulation for each part category: `frozen` (spares of
  the homologated design only), `tokens: N` (a set number of updates per
  season), or `open`; or a homologation date after which new designs are
  blocked until the next season. C4 (customer cars) covers who owns the
  homologated design; this item covers when it may change.

### D8. Custom tyre compounds · P2
- **Needed by:** dtm-2013, dtm-2012.
- **Real world:** 2013 had two Hankook dry tyres, the **standard** tyre
  (white or silver sidewall) and the **option** (yellow sidewall). 2012 had
  one dry tyre only.
- **Today:** the compound keys are fixed to soft, medium, hard,
  intermediate and wet. A pack can tune their grip, wear and temperature
  in `tyremodel.json` and set the medium to null, but the allocation
  screen, the presets, the strategy tools and the race screens still use
  the fixed list. Names (SOFT, MEDIUM, HARD) and colours (red, yellow,
  white) are fixed in the code.
- **Workaround:** soft stands in for the option and hard for the standard
  tyre. The option shows as a red "SOFT".
- **Request:** compounds defined in `tyremodel.json`, each with
  - an id, a `label` and a short letter (for 2013: "Option", "O"),
  - a `color` used on every screen (allocation, timing, strategy,
    telemetry),
  - its grip, wear, cliff and temperature values, as today,
  - whether it is dry or wet,
  - how many there are: one, two or more dry compounds, with the screens
    showing only the ones the pack defines.

## E. Modding and data format

### E1. Overlay (partial) packs · P1
- **Needed by:** all packs.
- **Today:** a pack must be a full copy (~30 files plus audio and art). We
  build ours by copying the base pack, so updates to the base game don't
  reach our pack automatically.
- **Request:** `"base_pack": "default26"` in `workshop.json`, so a mod only
  ships the files it changes and the game merges them at load time.

### E2. Settings as data, not Python · P1
- **Needed by:** all packs.
- **Today:** since 0.99.6 a Workshop pack's `constants.py` is read as data
  (`workshop_manager.load_safe_constants`: literal assignments of
  whitelisted names, no calls or imports beyond `UITheme`). A local pack in
  `data/<pack>/` is still **executed Python**, and the file is still Python
  syntax, so tools can't edit it as data.
- **Request:** move pack settings (start year, points, grid size, salaries,
  retirement ages) to `constants.json`, and read local packs the safe way
  too.

### E3. Published schema and validation · P2
- **Needed by:** dtm-1991.
- **Request:**
  - A JSON schema for every pack file.
  - A validation mode that lists errors at load time (unknown team in a
    contract, missing track, bad enum value).
  - A list of fields that refer to team names: we found 10 files (sponsors,
    ownership, histories, technologies, parts contracts, ERS levels,
    buyouts, events, relationships, staff).

### E4. Documented asset names · P2
- **Needed by:** dtm-1991, dtm-2013, dtm-2012.
- **What we found:** engine logos are looked up by engine name without
  spaces (`fordcosworth.png`), and team images by team name without spaces.
- **Request:**
  - Document the lookups, and allow an explicit `"logo": "file.png"` field.
  - Allow a **car image per entry**, not just per team. In 1991, AMG's
    Ludwig ran König Pilsener black while Thiim ran West red-white.
  - **2013:** team-mates differed in sponsor and colour on almost every
    team (Schnitzer: BMW Bank black and a white-blue M3 car), down to
    details such as Abt Sportsline's red (#11) and yellow (#12) mirrors
    and dive planes. Wehrlein's #18 ran a one-off VfB Stuttgart design at
    one race. Request: a car image per entry, and optionally per round.
  - **Livery choice per team:** until per-entry images exist, let a pack
    ship several images for a team (for example `Cars/<Team>.png`,
    `Cars/<Team>_2.png`) and let the player pick which one the team shows,
    for any team. The 2013 pack has all 22 cars drawn and ready for this.
  - **Car Setup:** the screen draws the same open-wheel line art for every
    series. Request: show the selected entry's car image there instead.
    Fallback: entry image, then team image, then today's line art.
  - **Team selection:** the screen shows one car per team and the drivers
    as plain rows. Request: each driver row with portrait and car, and the
    big car image follows the selected driver. All optional: without
    per-entry images the team car shows, as today.
  - **Mockups** of this and E15 for the developers:
    https://claude.ai/artifact/Akt86veBSfVUJi4L1mYtSU

### E5. Track editor features · P2
- **Needed by:** dtm-1991, dtm-2013, dtm-2012.
- **What we found:** `use_raw_canvas_coordinates` and `raw_canvas_size` are
  needed so cars follow the drawn track.
- **Requests:**
  - Document this, plus the race screen's safe area (the bottom of the map
    is hidden behind driver cards). The session header at the top wraps to
    two lines (about 82 px) for long track names: in dtm-2013 it hid the top
    of Moscow, the Nürburgring and Zandvoort until we kept tracks below
    y=100.
  - Keep the map's aspect ratio. The overview image is stretched on each
    axis separately to fill the map panel, so a wide, short window squashes
    the track (Hockenheim 2013 at 976×423 px: ×0.94 across, ×0.39 down).
    Letterboxing, or fitting the track like the non-raw mode does, would
    keep corners the right shape.
  - Several layouts per venue, e.g. Hockenheim 1991 vs 1992.
  - Import a track from GPS/GPX coordinates.
  - A per-track pit-lane path and pit position. Today the pits are at the
    start line, so in dtm-2013 the start lines at Moscow, the Nürburgring,
    Oschersleben and Zandvoort were moved onto the pit straight.

### E6. Currency and economy per pack · P3
- **Needed by:** dtm-1991, dtm-2013, dtm-2012.
- **1991:** DTM budgets were in Deutsche Mark and much smaller than F1.
- **2013:** the real 2013 sponsors replace the vanilla starting deals, but
  each keeps the money of the vanilla deal it replaces ($25–325m a deal,
  $137–410m a team against budgets of about $90m), so the economy the
  pack was tested with doesn't change. The amounts aren't real.
- **Request:** a currency label and symbol per pack, and global scale
  factors for salaries, costs, sponsor money and prize money.

### E7. Historical start state · P3
- **Needed by:** dtm-1991.
- **Request:**
  - Previous-season standings and history per team and driver, to drive
    prestige and form.
  - A real date for each schedule week, for news and emails.

### E8. Engine sounds per supplier beyond pass-bys · P3
- **Needed by:** dtm-2013, dtm-2012.
- **2013:** three V8s with clearly different voices (Audi RS 5, BMW M3,
  Mercedes C-Coupé).
- **Today:** only pass-bys can be tagged per supplier (`passby_audio` in
  `engines.json`). Grid idle and launch, pit fire-up and pit exit are one
  random bank (`race/race_engines.json`) shared by every car.
- **Workaround:** per-make pass-bys, and a mixed bank for the rest.
- **Request:** the same `passby_audio`-style tag for `grid_idle`,
  `grid_launch`, `pit_fireup` and `pit_exit`, so a BMW leaving its box
  sounds like a BMW.

### E9. Ambience and start sounds per track · P3
- **Needed by:** dtm-2013, dtm-2012.
- **2013:** the venues sound very different: the Norisring street circuit
  between concrete walls and a packed grandstand, the open Lausitzring,
  the dunes at Zandvoort, a half-empty Moscow Raceway. The broadcasts give
  us a crowd and `cars_on_track` bed for every round.
- **Today:** `ambience/session_layers.json` and its files are one set per
  pack, so every round plays the same crowd, PA and track bed. The same
  holds for the grid and pit banks.
- **Workaround:** one season-wide set, picked for consistency.
- **Request:** an optional per-track override, for example a
  `tracks.<track id>` block in `session_layers.json` (and the race and
  session manifests) that names other files for that venue, falling back
  to the pack-wide set.

### E10. Documented start-sound timing · P3
- **Needed by:** dtm-2013.
- **Today:** `grid_launch_NN` reads like "the launch", but the game starts
  it when the **3rd** of five lights comes on (0.5 s apart), 1.5 s before
  lights out; the cars move 0.5 s after that. None of this is documented,
  and a clip that starts with the getaway roars off two lights early.
  We found it by reading the game's start sequence.
- **Workaround:** every launch clip opens with 1.6 s of grid revving, so
  the getaway lands on lights out (`tools/engine_audio/starts.py`).
- **Request:** document the timing next to `race_engines.json`, or let a
  clip carry a `go_s` (where its getaway is) that the game lines up with
  lights out.

### E11. A full field crossing the line · P3
- **Needed by:** dtm-2013.
- **2013:** 22 cars, and on the first laps the field crosses the line
  nose to tail: a wall of sound, cars clearly one after another.
- **Today** (read from `ui/audio_manager.py` and `ui/hotlap_audio.py`):
  - every car gets a voice (no cap, channels grow as needed), but
    `_refresh_flyby_mix` keeps only the **3** voices nearest the line at
    full weight and turns the rest to **0.4** (-8 dB);
  - a headroom term (`min(1/sqrt(sum w^2), 2.5/sum w)`) then scales the
    whole group, so a pack is never much louder than about 2.5 cars. In
    game a full field sounds like 7 or 8 cars;
  - `passby_audio` is one clip key per supplier, so every Audi plays
    the same recording; two Audis a few tenths apart fuse into one car.
- **Workaround:** none in data for the mix. For the fusing: untag the
  suppliers so cars pick at random from a larger bank (losing the make
  sound per car), or live with it.
- **Request:**
  - make the foreground count, the background weight and the headroom
    cap settings in `hotlap_flybys.json` (or raise them for races);
  - let `passby_audio` take a list of keys, picked at random per car, so
    a make can have several recordings.

### E12. A sponsor on several teams · P3
- **Needed by:** dtm-2013, dtm-2012 (Deutsche Post on Abt Sportsline's Audi and Schnitzer's BMW).
- **2013:** make-wide partners ran on every car of a make: Puma, Sonax,
  Allgeier, Sachs and H&R on all eight BMWs, Petronas on all six
  Mercedes, Würth on all eight Audis.
- **Today:** a sponsor is one record in `sponsors.json`, and every vanilla
  sponsor backs one team. We didn't test whether two teams can hold a
  deal with the same sponsor.
- **Workaround:** each partner goes to one team of its make.
- **Request:** document whether a sponsor can back several teams, or
  allow a make-wide (supplier) deal.

### E13. Translated pack texts · P3
- **Needed by:** all packs (German first: the DTM is a German series).
- **Today:** the game has no language setting. Pack texts are one string
  each, for example `team_histories.json` maps a team name to one text.
  A German version would have to be a second pack.
- **Workaround:** English texts only. `tools/translatable_strings.py`
  lists a pack's own in-game texts in `seasons/<season>/translations.csv`
  (DTM 2013: 51 strings, mostly team histories, rule descriptions and
  radio messages), ready for a translator.
- **Request:** an optional language map per text, for example
  `{"en": "...", "de": "..."}` in `team_histories.json`, with a game
  language setting that picks the matching text and falls back to English.

### E14. Pit-entry sound · P3
- **Needed by:** dtm-2013.
- **2013:** fan recordings at the Oschersleben pit lane hold cars braking
  in off the track and rolling in on the limiter, as distinct as the exits.
- **Today:** `race/race_engines.json` has pit exits, fire-ups and
  wheelguns; nothing plays when a car enters the pit lane, so the stop
  starts in silence (or with the wheelguns).
- **Workaround:** the pit-entry recording stays a preview in the mod
  browser, outside the pack.
- **Request:** an optional `pit_entry_NN` bank, played as a car crosses
  the pit-lane entry, paired by number like the other pit clips.

### E15. Car and portrait in session screens · P3
- **Needed by:** dtm-2013, dtm-2012.
- **Why:** the player knows a car by its livery long before they read the
  name in the timing tower. The packs ship car images and portraits, but
  the race screens show neither.
- **Today:** the in-session driver panel shows name, position and team
  colour. The driver tabs show a name and a flag. The results podium shows
  flags.
- **Request:**
  - Portrait and car image (E4) in the driver panel header and the driver
    tabs.
  - Optional small car thumbnails in the timing tower and results, next to
    the number and the timing code (C6).
  - Cars and portraits on the results podium.

---

*Kept up to date as we find more. Collected while building
`seasons/dtm-1990` to `dtm-1992` and `dtm-2013`.*
