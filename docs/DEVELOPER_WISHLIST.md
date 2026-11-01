# Wish List for the Team Principal Developer

These are feature requests from building a historically accurate **DTM 1991**
season pack (German touring cars, Group A). Each item lists the real-world
need, what the game can't do today, our current workaround, and what would
solve it. Findings are based on game version 0.99.5. See
[CAPABILITIES.md](CAPABILITIES.md) for what we confirmed works.

Priority: **P1** = needed for an authentic series, **P2** = big gain,
**P3** = nice to have.

---

## A. Race weekend format

### A1. Several races per weekend (heats) · P1
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
- **1991:** places 1–16 came from qualifying. All other cars ran a ~50 km
  **qualification race** for places 17+.
- **Today:** no way to model this. Our 39-car field either all starts or is
  cut by DNQ.
- **Request:** a session type `qualification_race`, with `direct_grid_slots`
  and `distance_km`.

### A3. Configurable sessions and start · P2
- **Request:** two qualifying sessions (best time counts), standing or
  rolling start, red-flag and restart rules (Hockenheim 1991 heat 1 was
  stopped for rain and shortened), and race distance in km or minutes
  instead of `laps × lap_modifier`.

### A4. More than one event per week · P3
- **1991:** two rounds were on consecutive weekends (Nürburgring 8 Sep,
  Singen 15 Sep).
- **Today:** that works, but a double-header at one venue on one weekend
  can't be scheduled.
- **Request:** allow several events per week slot, or a real-date calendar
  (day of year).

## B. Rules and balance of performance

### B1. Success ballast · P1
- **1991:** weight penalties of up to **50 kg**, given for good results and
  removed for poor ones. Drivers new to the series started on the maximum.
- **Today:** not possible.
- **Request:** a regulation category with a per-position kg table, a
  maximum, a removal rule, and a value for newcomers.

### B2. Mid-season balance changes on a date · P1
- **1991:**
  - Audi had **40 kg removed from Wunstorf** onwards.
  - Opel could remove **50 kg after Hockenheim**.
  - Minimum weights depended on displacement and drivetrain (BMW and
    Mercedes 980 kg, Opel 1130 kg, Audi 1290 kg).
- **Today:** `scripted_changes` exists but has no documented format. The
  minimum weight is one global value.
- **Request:**
  - Scripted rule changes tied to season and week, e.g.
    `{"season": 1, "week": 23, "engine": "Audi", "mass_kg": -40}`.
  - Minimum weight per engine or car model.

### B3. Points table per race, drop scores · P2
- **Request:** points tables per session (heat 1 and heat 2 can differ),
  qualification-race points, and drop scores (Streichresultate, used in
  1992).

### B4. More classifications · P2
- **1991:** besides the drivers' title there were a **teams'** and a
  **manufacturers'** title (only the best car of each make scored), the
  **ITR Fahrerpokal** (DTM plus the non-championship Brno and Donington
  rounds) and a **privateer cup** paid in prize money.
- **Request:** a list of championships in data, each with its own events,
  points rules and eligible entries (e.g. `"privateer": true`).

## C. Entries, teams and drivers

### C1. More than 3 cars per team · P1
- **1991:** AMG ran **4 cars**, and some teams went up to 5.
- **Today:** `formula_team_entry_cap` stops at `three`.
- **Workaround:** Kreutzpointner (AMG #87) is a reserve driver.
- **Request:** allow 4–6 entries.

### C2. Entry lists per round (part-timers and guests) · P1
- **1991:**
  - Michael Schumacher drove 2 rounds for Zakspeed.
  - Walter Röhrl drove 1 round for SMS.
  - Bernd Schneider joined Zakspeed from round 8.
  - Jochen Mass did 3 rounds for MS-Jet.
- **Today:** contracts run the whole season.
- **Request:** a per-round entry list, or a contract with `rounds: [6, 7]`,
  so AI teams follow history in season 1.

### C3. Car numbers per entry and fixed numbers · P2
- **1991:** numbers went to the entry, like Ludwig #8 and Stuck #1, not
  per-team pairs.
- **Today:** numbers work, but reserves and guests can't keep their real
  numbers.
- **Request:** a `number` on the contract, including for reserves.

### C4. Customer cars and homologation · P2
- **1991:** privateers bought homologated cars (Evo models) from BMW,
  Mercedes and Opel. Chassis development was mostly the manufacturer's job,
  not the team's.
- **Today:** every team designs its own chassis.
- **Request:** a "customer car" contract type, like engines, where chassis
  and aero performance come from the supplier's homologated model. Also
  homologation steps (Evo kits) as data.

### C5. Retirement and age tuning in data · P3
- **1991:** drivers raced competitively into their 40s and 50s (Quester was
  51, Laffite 47).
- **Today:** we changed `DRIVER_RETIREMENT_*` in `constants.py`.
- **Request:** expose these in JSON (see E2).

## D. Cars and simulation

### D1. Touring-car part set · P1
- **Today:** the parts are open-wheel ones (front and rear wing, underfloor,
  diffuser, sidepods), plus ERS and DRS.
- **Request:** data-defined part categories with labels and effects, so a
  pack can use e.g. splitter, rear spoiler, suspension, brakes, gearbox and
  tyres. Also a way to remove categories completely.

### D2. Drivetrain · P2
- **1991:** the 4WD Audi V8 had a big advantage in the wet. In Hockenheim's
  wet heat 2 the Audis finished about a minute clear.
- **Request:** a `drivetrain` value (`rwd` / `fwd` / `awd`) that affects
  traction, wet performance and tyre wear.

### D3. Documented lap-time controls · P1
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
- **Request:** weather probability per date and region (e.g. April in the
  Eifel), red-flag or restart for heavy rain, and tyre changes to wets as
  real strategy.

## E. Modding and data format

### E1. Overlay (partial) packs · P1
- **Today:** a pack must be a full copy (~30 files plus audio and art). We
  build ours by copying the base pack, so updates to the base game don't
  reach our pack automatically.
- **Request:** `"base_pack": "default26"` in `workshop.json`, so a mod only
  ships the files it changes and the game merges them at load time.

### E2. Settings as data, not Python · P1
- **Today:** `constants.py` is **executed Python**. That's a security risk
  for Workshop content, and tools can't edit it safely.
- **Request:** move pack settings (start year, points, grid size, salaries,
  retirement ages) to `constants.json`, and stop running pack code.

### E3. Published schema and validation · P2
- **Request:**
  - A JSON schema for every pack file.
  - A validation mode that lists errors at load time (unknown team in a
    contract, missing track, bad enum value).
  - A list of fields that refer to team names: we found 10 files (sponsors,
    ownership, histories, technologies, parts contracts, ERS levels,
    buyouts, events, relationships, staff).

### E4. Documented asset names · P2
- **What we found:** engine logos are looked up by engine name without
  spaces (`fordcosworth.png`), and team images by team name without spaces.
- **Request:**
  - Document the lookups, and allow an explicit `"logo": "file.png"` field.
  - Allow a **car image per entry**, not just per team. In 1991, AMG's
    Ludwig ran König Pilsener black while Thiim ran West red-white.

### E5. Track editor features · P2
- **What we found:** `use_raw_canvas_coordinates` and `raw_canvas_size` are
  needed so cars follow the drawn track.
- **Requests:**
  - Document this, plus the race screen's safe area (the bottom of the map
    is hidden behind driver cards).
  - Several layouts per venue, e.g. Hockenheim 1991 vs 1992.
  - Import a track from GPS/GPX coordinates.
  - A per-track pit-lane path.

### E6. Currency and economy per pack · P3
- **1991:** DTM budgets were in Deutsche Mark and much smaller than F1.
- **Request:** a currency label and symbol per pack, and global scale
  factors for salaries, costs and prize money.

### E7. Historical start state · P3
- **Request:**
  - Previous-season standings and history per team and driver, to drive
    prestige and form.
  - A real date for each schedule week, for news and emails.

---

*Kept up to date as we find more. Collected while building
`seasons/dtm-1991`.*
