=== post | Intro | big-picture
## Feature requests from the DTM packs: racing rules as data

Hey! I'm the one making the DTM season packs (1990, 1991, 1992, 2012 and 2013). First of all: thanks for the game and for how moddable it already is. Building these packs was a lot of fun.

While building them I kept a list of everything the game can't do yet. It's around 50 items now. When I looked at it again I realised most of them aren't 50 separate things. They're parts of a few systems. So instead of a long wish list I'd like to suggest one idea:

**Build each racing rule once, as data, and let every series and every game mode use it.**

So formula, oval and the endurance mode you're working on would all use the same building blocks:
- **Weekend builder**: qualifying formats, heats, sprint races, grids
- **Rules engine**: pit stop and tyre rules, checked after the race and used by the AI
- **Entry model**: the car with its number, drivers (crews!), livery and tags
- **Content as data**: tyre compounds, parts, names and colours from the pack
- **Dated world**: changes on a date, like a weight change from a certain round

All of it in the file format packs use today, so nothing breaks.

I split it into a few posts below, one per topic, each with real examples from DTM and F1. The pictures should make it easier to follow. Happy to help with testing anytime!

=== post | How it fits | option-to-block, scopes
## 1. How it fits what's already there

I really like how regulations work right now: a category, options, voting and scripted_changes. I wouldn't change that at all.

My idea: an option just **points to a named block** for the details. You already do this for ovals, where `oval_stage_racing` keeps its stages in `config.json`.

Example for DTM 2013 qualifying:
```json
{ "key": "dtm_2013", "qualifying": "dtm_2013_q4" }
```
The block holds the stages: Q1 to Q3 knockout, then a one-lap Q4 for the top 4.

- the governing body still votes between options, scripted_changes still switch them
- blocks never vote, they're just data
- `knockout` and `session_60` become presets that work exactly like today
- a pack without new fields plays exactly as before

One more thing that would make it all scale: **one lookup for every value**. Set it for the season and override it for a session, a race, a track, a make or class, or a single entry. The most specific one wins. That alone covers:
- DRS in the race but not in qualifying (DTM 2013)
- one stop on Saturday, two on Sunday (DTM 2025)
- a minimum weight per make (DTM 1991: Audi 1,290 kg, BMW 980 kg)
- BoP per class for endurance

=== post | Quick wins | modes
## 2. Quick wins

**a) A few questions (no code needed, just answers)**
- What do `track_time_mult` and the other lap-time fields do exactly? I fitted lap times by running your physics offline.
- How are logos and car images looked up? An explicit `"logo": "file.png"` field would help a lot.
- Where is the safe area of the race map? Long track names wrap the header and hide the top of the track.
- When exactly does `grid_launch_NN` start? I found it's at the 3rd of five lights, 1.5 s before lights out.
- Can one sponsor back several teams? (Petronas on all Mercedes, Würth on all Audis in 2013)

**b) Oval features for formula packs**
A lot of what I asked for already exists in the oval mode, just not for formula packs:
- rolling start (`double_file_pace_lap`): DTM 2000, 2001 and 2021 on
- 4 to 6 cars per team: AMG ran 4 cars in 1991
- grid size as a regulation instead of a constant
- stage points and the chase format

And red flags already exist in the formula code, which endurance will need too.

If these became shared settings (`start_procedure`, `team_entry_cap`, `grid_limit`, `stage_racing`, `championship_format`, `red_flags`), every mode gets them, endurance included.

=== post | Rules engine | race-rules
## 3. Rules engine: pit stop and tyre rules as rows

This is the big one for me. Today there's one tyre rule (two compounds, on or off) and three allocation levels. In DTM almost every season had its own pit stop rules.

The idea: every rule is **one row**. The game checks the rows after the race, and the AI reads the same rows to plan a legal race.

Example DTM 2013:
- `mandatory_stops: 2`
- `no_stop_first_laps: 3`, `no_stop_last_laps: 3` (pit window closed, a stop there doesn't count)
- `must_use: option` (one option set per race, every driver has to use it)

In the picture car B stops on lap 38. That stop doesn't count, so it only has one stop and gets a penalty.

Other rows from real seasons:
- windows per stop in laps, minutes or share of the race (DTM 2008: middle third; DTM 2025: stop 1 in minute 10 to 20, stop 2 in 39 to 45)
- what counts as a stop: four new tyres, not under safety car or FCY, not a damage stop
- stop count per race of the weekend (DTM 2025: 1 on Saturday, 2 on Sunday)
- `max_share_on` (DTM 2014: option tyre for half the race at most)
- `max_stint_laps` (F1 Qatar 2023: 18 laps)
- `min_sets_used` (F1 Monaco 2025: 3 sets)
- `start_on_qualifying_tyre` for the top N (F1 2010 to 2021, DTM 2023 on)
- set limits per weekend, per race day or per compound, max new sets in qualifying
- tyre warmers banned (DTM 2003, 2017)

Each row has a scope (race, weekend, season), who it applies to and a penalty. A new rule is a new row, not new code all over the place.

=== post | Weekend builder | qualifying-stages
## 4. Weekend builder: qualifying and race formats

Every qualifying format I found in DTM and F1 is a short list of stages. Each stage takes cars in and sends some on. So instead of `session_60` or a fixed Q1 to Q3, a format would be a list:
- `timed` (minutes, max laps, best of 2 sessions or aggregate)
- `knockout` with any number of parts and any cut
- `single_lap` (alone on track, reverse order or by last race)
- `qualification_race` (DTM 1989 to 1992: a 50 km race for places 17 on)
- `elimination` (F1 2016) and `prequalifying` (F1 1988 to 1992)

Per stage: car state (race fuel, parc fermé, start tyres), max new sets, the 107% cut and a points table.

Each race of the weekend names its grid: qualifying, a named session, the previous race (heats!), reverse top N or a drawn reverse grid.

That covers DTM from 1984 to 2026 (Top-Qualifying, qualification races, heats, Superpole, Q4, one qualifying per race) and every F1 format incl. sprints. Other series come for free: IndyCar, BTCC, Supercars, Super GT, MotoGP, Formula E, Le Mans Hyperpole.

For the race itself:
- race length in laps, km, **minutes + 1 lap**, or whatever comes first
- safety car laps added (DTM 2019, 2025)
- rolling start, also two abreast
- red flag result as an aggregate (Zolder 1986)
- heats with a gap and repair time between them

=== post | Entry model | entry-model
## 5. Entry model (endurance-ready)

Lots of my requests are really one thing: the **entry** as the unit instead of the team. An entry = car, number, timing code, livery, 1 to 4 drivers, the rounds it runs, and tags (`class`, `guest`, `privateer`, `rookie`).

Then many features just read the same entry:
- **Points**: who scores and in which title (guests score nothing, privateer cup, class titles)
- **Qualifying**: groups and classes, Hyperpole per class
- **Balance**: ballast and BoP by make or class
- **Screens**: car image and portrait per entry, timing codes
- **Pit stops**: driver change as a stop service
- **Junior seats**: who may take a feeder seat

DTM examples:
- 1991: AMG ran 4 cars, Schumacher did 2 rounds for Zakspeed, numbers belong to the entry (Ludwig #8, Stuck #1)
- 2013: three-letter codes on timing and car (Scheider was TSC), team-mates with different liveries on almost every team

A one-driver entry works like today's car. Crews are the endurance case, so this is probably work the endurance mode needs anyway.

=== post | Points |
## 6. Points and championships

Today it's one points table plus +1 for pole and fastest lap. Ovals already have stage points and the chase. What I'd love:
- a points table per session: race, heat, sprint, qualifying, qualification race (DTM 2001: 3-2-1 for the qualifying race)
- bonus rows with a condition: fastest lap only in the top 10 (DTM 2022), points for leading a lap
- half points for heats (DTM 1984, 1985) or shortened races, double points for a finale
- drop scores (DTM 1992) or best N results (F1 until 1990)
- guests that score nothing, their points go to the next driver (DTM 1987, 2018, 2021 on)
- a list of championships, each with its own rounds and entries: teams, makes (best car only), privateer cup, rookies, classes, even non-championship rounds (ITR Fahrerpokal 1991)
- stage points and the chase for any mode

For endurance: points by race length, double points for the big race, points for the whole crew.

=== post | Content and dates |
## 7. Content as data, and a world that knows dates

**Tyres, parts and names from the pack**
- compounds defined in `tyremodel.json` with name, letter and colour. DTM 2013 had "Standard" (white) and "Option" (yellow), 2012 only one dry tyre. Right now the option shows as a red "SOFT" and the allocation screen always lists a medium.
- tyre suppliers: the tyre war already works, which is great! Missing: own physics per supplier (warm-up, cliff), strength in the wet or heat, an own compound range, supplier logo and colour on screens
- part categories with labels and drawings from the pack: a touring car has a splitter, not a front wing

**Dates**
- a real date per schedule week, and several events per week (double-headers)
- scripted_changes with a week and a filter: Audi -40 kg from Wunstorf (1991), BMW's new wing from the Nordschleife (1992)
- success ballast by result or points (DTM 1990, 1991, Super GT)
- homologation: part categories frozen, with tokens or open (DTM 2012/2013 aero freeze), and customer cars like customer engines
- rain chance per date, so May and October at Hockenheim can differ

=== post | The rest and order | bundles
## 8. The rest, and what I'd do first

**Closed-car physics**: drivetrain (the 4WD Audi in the wet, 1991), a wider car_profile range or real values (480 hp, 1,110 kg, lots of drag), and damage you carry or repair instead of a swapped "front wing".

**Pack infrastructure**: overlay packs with a `base_pack`, settings as JSON instead of Python, a schema and a validation report at load. Every idea above adds data, so this makes all of it cheaper and safer.

**Sound**: engine sounds per make beyond pass-bys, ambience per track, a pit-entry sound, and a full field that sounds like a full field.

**If I had to pick an order:**
1. the quick wins (questions + oval features for formula packs)
2. rules engine, weekend builder and entry model. Once they exist, most later requests are a new row instead of new code
3. everything else plugs into those

Six of these bundles are things the endurance mode needs anyway (crews, classes, long races, stop services, BoP, rolling starts), so hopefully a lot of this lines up with what you're already planning.

I have the full list with every season written down, happy to share it. Thanks again for the game, and let me know if anything is unclear or if I can help test!
