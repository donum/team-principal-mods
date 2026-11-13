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
  ('B1', '2000-2026', 'Success ballast.'),
  ('C9', '2004-2010', 'BTC Touring and Super 2000 cars in one class.'),
  ('B13', '2022-2026', 'Hybrid boost, limited for the leaders.'),
  ('A3', '2014-2026', 'Laps added after a long safety car.'),
 ],
}

SPANS = {
    'F1': '1950-2026',
    'DTM': '1984-1996,2000-2026',
    'IndyCar': '1979-2026',
    'Endurance': '1953-1992,2012-2026',
    'BTCC': '1958-2026',
}

NOTES = {
    'F1': 'Formula One World Championship.',
    'DTM': 'DPM 1984 and 1985, DTM, ITC 1996. No series from 1997 to 1999.',
    'IndyCar': 'CART 1979 to 2003, Champ Car to 2007, IRL and IndyCar from 1996, as one row.',
    'Endurance': 'World Sportscar Championship 1953 to 1992 and WEC from 2012. No world title from 1993 to 2011.',
    'BTCC': 'British Saloon Car Championship, BTCC from 1987.',
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
