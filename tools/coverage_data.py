"""Season-by-season lever needs for the coverage explorer.

For every season of five series (F1, DTM, IndyCar, endurance, BTCC) this
lists which game features ("levers") the season's rules need and the game
lacks today. A season is playable as it was when all its levers are on.

DTM comes from docs/dtm_rules.html (rules rated "approximated" or "not
possible" with a wishlist item). The other series are hand-mapped from the
docs/history tables. Only rules that shape every race weekend are counted;
rare cases (half points, red-flag aggregates, time limits that rarely bite)
are left out.

Writes docs/history/coverage.html from tools/coverage_template.html.
Usage: python -I tools/coverage_data.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Lever id: (label, package, today, short explanation)
LEVERS = {
    'A1': ('Several races per weekend', 'Weekend format', 'Partly', 'Heats, sprints, two or three races a round, each with its own points and grid.'),
    'A2': ('Qualification race', 'Weekend format', 'No', 'A short race for the cars outside the direct grid places.'),
    'A3': ('Starts and race length', 'Weekend format', 'Partly', 'Rolling starts outside oval packs, races by time (minutes plus one lap, 6 or 24 hours), laps added after the safety car.'),
    'A5': ('Single-lap shootout', 'Weekend format', 'No', 'One timed lap each, alone on track: Superpole, Q4, Top-Qualifying, Fast Six.'),
    'A6': ('Qualifying as stages', 'Weekend format', 'Partly', 'Any number of sessions and cuts, lap limits, race fuel, reverse or drawn grids. Today: one 60-minute session or an F1 knockout.'),
    'B5': ('Mandatory stops and windows', 'Tyres and stops', 'No', 'A set number of stops, pit windows, what counts as a stop.'),
    'B7': ('Tyre allocation rules', 'Tyres and stops', 'Partly', 'Sets per race or race day, a must-use tyre, at most N new sets in qualifying. Sets per weekend already work.'),
    'B10': ('Pit-stop procedure', 'Tyres and stops', 'No', 'Crew size, what may happen at the same time (fuel, tyres, driver).'),
    'B12': ('Tyre and stop rules as data', 'Tyres and stops', 'No', 'Start on qualifying tyres, no tyre changes, tyre warmer bans.'),
    'D8': ('Own tyre compounds', 'Tyres and stops', 'Partly', 'Colours and allocation for any compound name. Names already come from the pack, colours follow the first letter.'),
    'D9': ('Tyre makers with own physics', 'Tyres and stops', 'Partly', 'Each tyre maker with its own warm-up, wear and wet grip.'),
    'B3': ('Points per race and drop results', 'Points and titles', 'No', 'Best N results, points per session, double points, points by race length.'),
    'B4': ('More titles and classes', 'Points and titles', 'No', 'Classes in one race, independents, best N cars per make, manufacturers only.'),
    'B8': ('Bonus and qualifying points', 'Points and titles', 'Partly', 'Points for qualifying, leading a lap, most laps led, fastest lap in the top 10. Today: +1 for pole and fastest lap.'),
    'B9': ('Guests who score nothing', 'Points and titles', 'No', 'Guest drivers race but the points go to the next eligible driver.'),
    'B1': ('Success ballast', 'Balance and homologation', 'No', 'Kilos or less power for good results, per driver, make or position.'),
    'B2': ('Weights and BoP per make', 'Balance and homologation', 'No', 'Weight, restrictor or power per make, class or engine type, changed on a date.'),
    'C4': ('Customer cars', 'Balance and homologation', 'No', 'Teams buy a chassis from a maker instead of building their own.'),
    'D7': ('Development freeze', 'Balance and homologation', 'No', 'Frozen engines or aero for a set time.'),
    'C1': ('More than three cars per team', 'Entries and crews', 'No', 'Four to six entries for one team.'),
    'C2': ('Entries per round', 'Entries and crews', 'No', 'Part-timers, one-off entries and guests for some rounds only.'),
    'C8': ('Driver crews per car', 'Entries and crews', 'No', 'Two or three drivers sharing one car, with drive time rules and ratings.'),
    'C9': ('Several car models per make', 'Entries and crews', 'No', 'Different cars or aero kits from one make, or two car types in one class.'),
    'B6': ('DRS rules per session', 'Race control and aids', 'Partly', 'DRS only in the race, uses per lap, a gap, no DRS in the last laps.'),
    'B11': ('Race control rules', 'Race control and aids', 'Partly', 'Pit lane closed under the safety car, full-course yellow, penalty lap.'),
    'B13': ('Push-to-pass', 'Race control and aids', 'Partly', 'A boost with a set number of uses or seconds per race.'),
    'N5': ('Restart and lapped-car rules', 'Race control and aids', 'Partly', 'Wave-around, double-file restarts, finishing under yellow, for formula packs. The oval mode has some of it.'),
    'N4': ('Active aero and overtake mode', 'Race control and aids', 'No', 'F1 2026: moving wings for all, extra energy for the chasing car.'),
    'D2': ('Drivetrain', 'Car model', 'No', 'Four-wheel drive with its own start and wet-weather strength.'),
    'N1': ('Cost cap and wind tunnel limits', 'Not in the wishlist yet', 'No', 'A spending cap and aero testing time by championship position.'),
    'N3': ('Penalty points and race bans', 'Not in the wishlist yet', 'No', 'Licence penalty points, 12 points means a race ban.'),
    'N7': ('Playoff eliminations and playoff points', 'Not in the wishlist yet', 'No', 'Elimination rounds, a win to advance, playoff points carried into each round.'),
    'N8': ('Energy limit per race', 'Not in the wishlist yet', 'No', 'A fixed amount of energy per race, energy taken off under the safety car.'),
    'N9': ('Motorcycles', 'Not in the wishlist yet', 'No', 'Bike physics and riders instead of cars.'),
    'N10': ('Rally stages', 'Not in the wishlist yet', 'No', 'Stages on closed roads, one car at a time against the clock, overall time, restart after retiring.'),
    'N11': ('Head-to-head knockout events', 'Not in the wishlist yet', 'No', 'Show events outside the championship: two cars at a time, a bracket, identical cars.'),
    'N12': ('Joker lap and mixed surfaces', 'Not in the wishlist yet', 'No', 'A longer route every driver must take once, tarmac and gravel in one lap.'),
    'N6': ('Team order ban', 'Not in the wishlist yet', 'No', 'Team orders banned, with fines when caught.'),
}

PACKAGES = ['Weekend format', 'Tyres and stops', 'Points and titles', 'Balance and homologation',
            'Entries and crews', 'Race control and aids', 'Car model', 'Not in the wishlist yet']


def yrs(spec):
    out = []
    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-')
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


# Hand-mapped needs: series -> list of (lever, years, why)
NEEDS = {
 'F1': [
  ('A6', '1950-1995', 'Two qualifying sessions, best lap of both counts.'),
  ('A6', '1996-2002', 'One hour with a 12-lap limit.'),
  ('A5', '2003-2005', 'One lap each, alone on track.'),
  ('A6', '2003-2009', 'Qualifying on race fuel, fuel credit in Q3.'),
  ('B12', '2005', 'One set of tyres for qualifying and race.'),
  ('B12', '2010-2021', 'Top 10 start on their qualifying tyres.'),
  ('C8', '1950-1957', 'Shared drives, points split.'),
  ('C1', '1950-1962', 'No limit on cars per team.'),
  ('C4', '1950-1980', 'Privateers race bought cars.'),
  ('C2', '1950-1980', 'Many one-off and privateer entries.'),
  ('B3', '1950-1990', 'Only the best N results count.'),
  ('B4', '1958-1978', 'Only the best car of each make scores for constructors.'),
  ('B4', '1950-1960', 'The Indianapolis 500 counts with its own rules.'),
  ('B2', '1950-1953', 'Engines with and without supercharger side by side.'),
  ('B2', '1977-1988', 'Turbo and non-turbo engines side by side.'),
  ('D9', '1950-1974', 'Several tyre makers, tyre wars.'),
  ('D9', '1977-1986', 'Tyre war Goodyear, Michelin, Pirelli.'),
  ('D9', '1989-1991', 'Goodyear and Pirelli.'),
  ('D9', '1997-2006', 'Tyre wars Goodyear, Bridgestone, Michelin.'),
  ('D8', '2016-2026', 'Named compounds per race (C1 to C5, colours).'),
  ('B11', '2007-2008', 'Pit lane closed under the safety car.'),
  ('B3', '2014', 'Double points at the last race.'),
  ('A1', '2021-2026', 'Sprint weekends.'),
  ('B3', '2021-2026', 'Sprint points.'),
  ('B8', '2019-2024', 'Fastest lap point only inside the top 10.'),
  ('D7', '2007-2013', 'Engine freeze.'),
  ('D7', '2022-2025', 'Engine freeze.'),
  ('N1', '2021-2026', 'Cost cap and wind tunnel time by position.'),
  ('N3', '2014-2026', 'Penalty points and race bans.'),
  ('N6', '2003-2010', 'Team orders banned.'),
  ('B5', '2025', 'Monaco: at least two stops.'),
  ('N4', '2026', 'Active aero and overtake mode.'),
 ],
 'IndyCar': [
  ('A3', '1979-2026', 'Rolling starts.'),
  ('N5', '1979-2026', 'Restarts, wave-arounds, finishing under yellow.'),
  ('A6', '1979-2026', 'Indy 500: four-lap runs over several days, 33 starters.'),
  ('A6', '2008-2026', 'Road courses: two groups, then Fast Twelve and Fast Six.'),
  ('A5', '2010-2026', 'Indy 500 shootout for pole.'),
  ('B3', '1979-1982', 'Points by race distance.'),
  ('B3', '2014-2022', 'Double points at the Indy 500 (and finale 2015 to 2019).'),
  ('B8', '1981-2026', 'Bonus points for pole and laps led.'),
  ('B8', '2010-2014', 'Points for Indy 500 qualifying.'),
  ('B8', '2016-2026', 'Points for Indy 500 qualifying.'),
  ('C4', '1979-2007', 'Teams buy chassis from Lola, Reynard, Dallara and others.'),
  ('C9', '2015-2017', 'Aero kits per maker.'),
  ('B2', '1996', 'Two engine types with different boost.'),
  ('B2', '2012-2026', 'Boost set by track type.'),
  ('B13', '2009-2026', 'Push-to-pass with a budget per race.'),
  ('A1', '2011', 'Two short races in one night (Texas).'),
  ('A1', '2020', 'Double-headers.'),
 ],
 'Endurance': [
  ('A3', '1953-1992', 'Races by time (24 hours, 12 hours) and the Le Mans start (to 1969).'),
  ('A3', '2012-2026', 'Races by time: 6, 8 and 24 hours.'),
  ('C8', '1953-1992', 'Two or three drivers per car.'),
  ('C8', '2012-2026', 'Three drivers per car, drive time limits, driver ratings.'),
  ('B4', '1953-1992', 'Several classes in one race, titles per class or for makes only.'),
  ('B4', '2012-2026', 'Hypercar, LMP2, GT classes with their own results.'),
  ('B2', '1953-1981', 'Classes by engine size.'),
  ('B2', '1982-1992', 'Group C fuel formula, C1 and C2.'),
  ('B2', '2012-2026', 'Balance of performance, hybrid against non-hybrid.'),
  ('B10', '1953-1992', 'Le Mans pit rules: engine off, no work while refuelling.'),
  ('B10', '2012-2026', 'Le Mans pit rules, driver change while refuelling.'),
  ('B3', '2012-2026', 'Points times race length, half a point for 11th and lower.'),
  ('A6', '2020-2026', 'Hyperpole.'),
  ('B11', '2014-2026', 'Slow zones and full-course yellow.'),
 ],
 'NASCAR': [
  ('B3', '1949-1974', 'Points by prize money, race length or laps.'),
  ('B8', '1975-2016', 'Bonus points for leading a lap and most laps led.'),
  ('N7', '2007-2013', 'Chase seeding with bonus points per win.'),
  ('N7', '2014-2025', 'Elimination rounds, a win advances, playoff points.'),
  ('A2', '1959-2026', 'Daytona 500 grid from the Duel races.'),
  ('A6', '2014-2026', 'Group and knockout qualifying, grids by formula.'),
  ('B2', '1988-2026', 'Restrictor plates or spacers: less power on superspeedways.'),
  ('B4', '1958-2026', 'Rookie of the Year with its own rules.'),
 ],
 'Super GT': [
  ('B4', '1994-2026', 'Two classes in one race, titles per class.'),
  ('B1', '1993-2026', 'Success ballast by results, then by championship points.'),
  ('B2', '2010-2026', 'Balance of performance per race in GT300.'),
  ('C8', '1993-2026', 'Two drivers per car, at most two thirds each.'),
  ('B5', '1993-2026', 'Compulsory stop with a driver change.'),
  ('D9', '1993-2026', 'Tyre war: Bridgestone, Michelin, Yokohama, Dunlop.'),
  ('A6', '2024-2026', 'Qualifying times of both drivers added up.'),
  ('B12', '2024-2026', 'Start on the qualifying tyres.'),
  ('A3', '2024-2026', 'Three-hour races.'),
  ('B8', '2024-2026', 'Qualifying points 3-2-1.'),
  ('B3', '2006-2017', 'More points for the Suzuka 1000 km.'),
 ],
 'IMSA': [
  ('B4', '1971-2026', 'Several classes in one race, titles per class.'),
  ('C8', '1971-2026', 'Two to five drivers per car.'),
  ('A3', '1971-2026', 'Races by time (24, 12, 6 hours) and rolling starts.'),
  ('B2', '1981-1993', 'Minimum weight by engine size, turbos heavier.'),
  ('B2', '2014-2026', 'Balance of performance per class.'),
  ('C9', '2014-2026', 'Different car types in one class (DP, LMP2, DPi, LMDh, LMH).'),
  ('B3', '2014-2026', 'Endurance Cup points at set times during the race.'),
  ('B8', '2021-2026', 'Points for qualifying.'),
  ('A6', '2019-2026', 'In LMP2 only the Bronze driver qualifies.'),
 ],
 'Formula E': [
  ('N8', '2014-2025', 'A fixed amount of energy per race.'),
  ('B13', '2014-2021', 'Fan Boost.'),
  ('B13', '2018-2025', 'Attack Mode through a zone, with a time budget.'),
  ('B10', '2014-2017', 'A car swap halfway through the race.'),
  ('A3', '2018-2021', 'Races of 45 minutes plus one lap.'),
  ('A3', '2022-2025', 'Laps added after the safety car.'),
  ('A6', '2014-2025', 'Qualifying in groups, then a shootout or duels.'),
  ('B8', '2014-2025', 'Pole worth 3 points, fastest lap only in the top 10.'),
  ('B3', '2014', 'The worst round is dropped.'),
  ('A1', '2014-2025', 'Two races on one weekend (double-headers).'),
  ('B4', '2023-2025', 'Manufacturers title from the best two cars of each make.'),
  ('B5', '2024-2025', 'Pit Boost: a mandatory charging stop.'),
 ],
 'MotoGP': [
  ('N9', '1949-2026', 'Motorcycles and riders.'),
  ('B3', '1949-1976', 'Only the best results count.'),
  ('B2', '2002-2011', 'Minimum weight by number of cylinders.'),
  ('B2', '2012-2026', 'Concessions and different rules for cheaper entries (CRT, Open class).'),
  ('B10', '2005-2026', 'Flag-to-flag: swap to a second bike in the rain.'),
  ('A6', '2013-2026', 'Q1 and Q2, the top 10 from practice go straight to Q2.'),
  ('B11', '2019-2026', 'Long lap penalty for track limits.'),
  ('A1', '2023-2026', 'Sprint race on Saturday with its own points.'),
 ],
 'WRC': [
  ('N10', '1973-2026', 'Special stages against the clock, one car at a time.'),
  ('C8', '1973-2026', 'Driver and co-driver.'),
  ('B4', '1973-2026', 'Several classes in one rally, makes score from nominated crews.'),
  ('B2', '1982-1986', 'Group B weight by engine size, turbos counted 1.4 times.'),
  ('B2', '1997-2021', 'Restrictor and weight rules by class.'),
  ('B8', '2011-2026', 'Power Stage bonus points.'),
  ('B3', '2024', 'Points for Saturday standings and Sunday stages.'),
  ('B3', '2025-2026', 'Extra points for the Sunday stages.'),
  ('B13', '2022-2024', 'Hybrid boost, settings chosen per stage.'),
 ],
 'NLS': [
  ('B4', '1977-2026', 'Many classes in one race, the title from class results.'),
  ('B3', '1977-2026', 'Points by class size, best results only.'),
  ('A3', '1977-2026', 'Races by time (4 and 6 hours), start in three groups.'),
  ('C8', '1977-2026', 'One to four drivers per car.'),
  ('B11', '2015-2026', 'Code 60 zones.'),
  ('B2', '2010-2026', 'Balance of performance for GT3 (SP9).'),
 ],
 'GT World Challenge': [
  ('B4', '1997-2026', 'Several classes in one race, by car (to 2011) or by driver rating.'),
  ('C8', '1997-2026', 'Two to four drivers per car.'),
  ('A3', '1997-2026', 'Races by time (2, 3, 6 and 24 hours).'),
  ('B2', '2011-2026', 'Balance of performance for GT3.'),
  ('A1', '2010-2026', 'Two races per weekend (GT1, then the Sprint Cup).'),
  ('B5', '2010-2026', 'Mandatory stop or driver change window.'),
  ('A6', '2018-2026', 'Qualifying with each driver, the times added up.'),
  ('B3', '2013-2026', 'Points during the Spa 24 Hours, two cups add up.'),
  ('C1', '2016-2026', 'Up to six cars per team.'),
 ],
 'Dakar': [
  ('N10', '1979-2026', 'Two weeks of stages against the clock, navigation, total time.'),
  ('N9', '1979-2026', 'Motorbikes in the same event.'),
  ('B4', '1979-2026', 'Bikes, cars and trucks with their own results, classes within each.'),
  ('C8', '1979-2026', 'Crews of two (cars) or three (trucks).'),
  ('B2', '2005-2026', 'Classes by engine size, drive and fuel.'),
  ('B10', '2005-2026', 'Unassisted riders who service their own bikes (?).'),
 ],
 'Rallycross': [
  ('A1', '2014-2025', 'Heats, semi-finals and a final in one event.'),
  ('A6', '2014-2021', 'Qualifying by intermediate points over four heats.'),
  ('A6', '2022-2025', 'One-lap SuperPole, heats by time, a progression race.'),
  ('B3', '2014-2021', 'Points for heats, semi-finals and the final.'),
  ('N12', '2014-2025', 'Joker lap, tarmac and gravel.'),
  ('C9', '2024-2025', 'Electric and petrol cars together.'),
 ],
 'Race of Champions': [
  ('N11', '1988-2025', 'Head-to-head knockout in identical cars.'),
  ('B4', '1999-2025', 'Nations Cup for two-driver teams.'),
 ],
 'BTCC': [
  ('B4', '1958-1990', 'Classes by engine size, the title from class points.'),
  ('A1', '2000-2003', 'Two races per meeting.'),
  ('A1', '2004-2026', 'Three races per meeting.'),
  ('A6', '2004-2026', 'Race 3 grid partly reversed, by a draw from 2006.'),
  ('B8', '2000-2026', 'A point for leading a lap.'),
  ('B4', '1992-2026', 'Independents\' titles.'),
  ('B4', '2000-2003', 'Production class with its own title.'),
  ('B5', '1998-2001', 'One mandatory two-tyre stop.'),
  ('B3', '2000', 'Best 20 of 24 results.'),
  ('B1', '2000-2021', 'Success ballast.'),
  ('C9', '2004-2010', 'BTC Touring and Super 2000 cars in one class.'),
  ('B13', '2022-2024', 'Hybrid boost, limited for the leaders.'),
  ('B13', '2025-2026', 'Turbo boost, limited for the leaders.'),
  ('A3', '2014-2026', 'Laps added after a long safety car.'),
 ],
}

SPANS = {
    'F1': '1950-2026',
    'DTM': '1984-1996,2000-2026',
    'IndyCar': '1979-2026',
    'Endurance': '1953-1992,2012-2026',
    'BTCC': '1958-2026',
    'NASCAR': '1949-2026',
    'Super GT': '1993-2026',
    'IMSA': '1971-2026',
    'Formula E': '2014-2025',
    'MotoGP': '1949-2026',
    'WRC': '1973-2026',
    'NLS': '1977-2026',
    'GT World Challenge': '1997-2026',
    'Dakar': '1979-2007,2009-2026',
    'Rallycross': '2014-2025',
    'Race of Champions': '1988-2012,2014-2015,2017-2020,2022-2023,2025',
}

NOTES = {
    'F1': 'Formula One World Championship.',
    'DTM': 'DPM 1984 and 1985, DTM, ITC 1996. No series from 1997 to 1999.',
    'IndyCar': 'CART 1979 to 2003, Champ Car to 2007, IRL and IndyCar from 1996, as one row.',
    'Endurance': 'World Sportscar Championship 1953 to 1992 and WEC from 2012. No world title from 1993 to 2011.',
    'BTCC': 'British Saloon Car Championship, BTCC from 1987.',
    'NASCAR': 'NASCAR Cup Series, rated as an oval pack: stages, chase, charters, free pass and green-white-checker exist there.',
    'Super GT': 'JGTC 1993 to 2004, Super GT from 2005.',
    'IMSA': 'IMSA GT 1971 to 1998, ALMS 1999 to 2013, WeatherTech from 2014, as one row.',
    'Formula E': 'Seasons by their start year: 2014 is the 2014-15 season.',
    'MotoGP': 'The premier class: 500cc 1949 to 2001, MotoGP from 2002.',
    'WRC': 'World Rally Championship, stage rallies.',
    'NLS': 'Nordschleife endurance series: Veedol, BFGoodrich, VLN, NLS from 2020.',
    'GT World Challenge': 'FIA GT 1997 to 2009, GT1 2010 to 2012, Blancpain, GT World Challenge Europe.',
    'Dakar': 'Rally raid with bikes, cars and trucks. Cancelled in 2008.',
    'Rallycross': 'FIA World Rallycross Championship 2014 to 2025.',
    'Race of Champions': 'A yearly one-off show event, as a proof of concept. Years without an event are left out.',
}


def dtm_needs():
    """Per season: wishlist item and rule text for every rule the game can't do exactly."""
    out = {}
    cur = None
    for line in open(os.path.join(ROOT, 'docs', 'dtm_rules.html'), encoding='utf-8').read().split('\n'):
        m = re.match(r'\{y:"(\d{4})"', line)
        if m:
            cur = int(m.group(1))
            out.setdefault(cur, [])
            continue
        m2 = re.match(r' \[(\w+),"(\w+)","((?:[^"\\]|\\.)*)"', line)
        if cur and m2 and m2.group(2) != 'fit':
            g = re.findall(r'"([A-D]\d+)"\]', line)
            if g and g[0] in LEVERS:
                text = re.sub(r'<[^>]+>', '', m2.group(3)).replace('\\"', '"')
                out[cur].append((g[0], text))
    return out


# History files: series key from the file name prefix.
PREFIX = {'f1': 'F1', 'dtm': 'DTM', 'indycar': 'IndyCar', 'wec': 'Endurance', 'btcc': 'BTCC',
          'nascar': 'NASCAR', 'supergt': 'Super GT', 'imsa': 'IMSA', 'fe': 'Formula E',
          'motogp': 'MotoGP', 'wrc': 'WRC', 'nls': 'NLS', 'gtwc': 'GT World Challenge',
          'dakar': 'Dakar', 'wrx': 'Rallycross', 'roc': 'Race of Champions'}


def year_span(cell):
    """Years a table row covers, from its first cell ('1950 to 1953', '1970s to 1992',
    '2005, rounds 1 to 6', 'Since 1939', '2014-15 to 2017-18'). None if unknown."""
    t = cell.replace('(?)', '').strip()
    ys = [int(x) for x in re.findall(r'\b(1[89]\d\d|20\d\d)(?=s\b|\b|-\d\d)', t)]
    if not ys:
        return None
    a, b = ys[0], ys[-1]
    if re.search(r'\b(1[89]\d0|20\d0)s$', t):
        b = int(re.findall(r'(\d{4})s$', t)[0]) + 9
    if t.lower().startswith('since'):
        b = 2026
    return [a, b]


def md_tables(text):
    """Every Markdown table before '## Sources', with the '## ' heading above it."""
    out, heading, rows = [], '', None
    for line in text.split('\n') + ['']:
        if line.startswith('## Sources'):
            break
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            rows = rows or []
            if not all(set(c) <= set('-: ') for c in cells):
                rows.append(cells)
            continue
        if rows:
            out.append({'heading': heading, 'head': rows[0], 'rows': rows[1:]})
        rows = None
        if line.startswith('## '):
            heading = line[3:].strip()
    return out


def history():
    """All docs/history topic files, grouped by series, in file order.
    Rows of the main table carry their year span as a first element."""
    hdir = os.path.join(ROOT, 'docs', 'history')
    out = {}
    for f in sorted(os.listdir(hdir)):
        pre = f.split('-')[0]
        if not f.endswith('.md') or pre not in PREFIX:
            continue
        text = open(os.path.join(hdir, f), encoding='utf-8').read()
        title = next(l[2:].strip() for l in text.split('\n') if l.startswith('# '))
        tables = md_tables(text)
        for t in tables:
            if t['heading'] == 'Table':
                t['spans'] = [year_span(r[0]) for r in t['rows']]
        sources = text.split('## Sources', 1)[1].split('## Discord post')[0].strip() if '## Sources' in text else ''
        out.setdefault(PREFIX[pre], []).append({'file': f, 'title': title, 'tables': tables, 'sources': sources})
    for v in out.values():
        v.sort(key=topic_rank)
    return out


def topic_rank(t):
    """Reading order: where the file is first linked in docs/history/README.md."""
    index = open(os.path.join(ROOT, 'docs', 'history', 'README.md'), encoding='utf-8').read()
    pos = index.find('(' + t['file'] + ')')
    return pos if pos >= 0 else len(index)


def dtm_rulebook():
    """Every DTM rulebook row per season: category, status, rule, game, lever."""
    cats = {'Q': 'Qualifying', 'R': 'Race', 'P': 'Pits and tyres', 'PT': 'Points', 'BL': 'Balance'}
    out, cur = {}, None
    for line in open(os.path.join(ROOT, 'docs', 'dtm_rules.html'), encoding='utf-8').read().split('\n'):
        m = re.match(r'\{y:"(\d{4})"', line)
        if m:
            cur = int(m.group(1))
            out.setdefault(cur, [])
            continue
        m2 = re.match(r' \[(\w+),"(\w+)","((?:[^"\\]|\\.)*)","((?:[^"\\]|\\.)*)"', line)
        if cur and m2:
            g = re.findall(r'"([A-D]\d+)"\]', line)
            clean = lambda x: re.sub(r'<[^>]+>', '', x).replace('\\"', '"')
            out[cur].append([cats.get(m2.group(1), m2.group(1)), m2.group(2), clean(m2.group(3)),
                             clean(m2.group(4)), g[0] if g else ''])
    return out


def build():
    seasons = {}
    for series, span in SPANS.items():
        seasons[series] = {y: {} for y in yrs(span)}
    for series, needs in NEEDS.items():
        for lever, spec, why in needs:
            for y in yrs(spec):
                if y in seasons[series]:
                    seasons[series][y].setdefault(lever, []).append(why)
    for y, rows in dtm_needs().items():
        if y in seasons['DTM']:
            for lever, why in rows:
                seasons['DTM'][y].setdefault(lever, []).append(why)
    return {
        'levers': [{'id': k, 'label': v[0], 'package': v[1], 'today': v[2], 'about': v[3]} for k, v in LEVERS.items()],
        'packages': PACKAGES,
        'history': history(),
        'dtm_rulebook': {str(k): v for k, v in dtm_rulebook().items()},
        'series': [{'name': s, 'note': NOTES[s],
                    'seasons': [{'y': y, 'needs': {k: v for k, v in sorted(n.items())}}
                                for y, n in sorted(seasons[s].items())]}
                   for s in SPANS],
    }


if __name__ == '__main__':
    data = build()
    tpl = open(os.path.join(ROOT, 'tools', 'coverage_template.html'), encoding='utf-8').read()
    out = os.path.join(ROOT, 'docs', 'history', 'coverage.html')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(tpl.replace('/*DATA*/null', json.dumps(data, ensure_ascii=False, separators=(',', ':'))))
    n = sum(len(s['seasons']) for s in data['series'])
    full = sum(1 for s in data['series'] for x in s['seasons'] if not x['needs'])
    print(out, n, 'seasons,', full, 'playable today')
