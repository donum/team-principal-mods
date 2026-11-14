"""Fill the empty staff roles in docs/staff/dtm_staff.csv with period names.

Two kinds of filled rows:
- A manufacturer-level role (designer, engine, aero, dynamics) that another
  team of the same make already has a real person for in that season is
  filled with that same person, status "assumed". These go into
  docs/staff/dtm_staff.csv, so the real reference stays the one place for
  real people.
- Every other empty role gets a made-up name that fits the team's country
  and the period, status "fictional", in docs/staff/dtm_staff_fictional.csv.
  A fictional person keeps the job for a few seasons, has a birth year, and
  never shares a name with a real person in the reference.

Run:  python tools/fictional_staff.py
The output is deterministic: the same input always gives the same names.
"""
import csv
import glob
import hashlib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAFF = ROOT / "docs/staff/dtm_staff.csv"
FICT = ROOT / "docs/staff/dtm_staff_fictional.csv"
ROLES = ["team_principal", "technical_director", "chief_designer", "head_of_aero",
         "head_of_engine", "head_of_dynamics", "chief_mechanic"]
MAKE_ROLES = {"chief_designer", "head_of_engine", "head_of_aero", "head_of_dynamics"}
AGE = {"team_principal": (38, 62), "technical_director": (38, 58), "chief_designer": (35, 56),
       "head_of_aero": (30, 50), "head_of_engine": (38, 60), "head_of_dynamics": (30, 50),
       "chief_mechanic": (28, 52)}
TENURE = {"team_principal": 8, "technical_director": 5, "chief_designer": 5, "head_of_aero": 4,
          "head_of_engine": 6, "head_of_dynamics": 4, "chief_mechanic": 4}

# first names: (born before 1960, born 1960 or later); surnames
NAMES = {
    "german": (["Klaus", "Jürgen", "Wolfgang", "Dieter", "Manfred", "Horst", "Rainer", "Peter", "Werner", "Helmut",
                "Gerhard", "Hans-Peter", "Bernd", "Uwe", "Karl-Heinz", "Rolf", "Norbert", "Hartmut", "Lothar", "Günter",
                "Reinhard", "Volker", "Heinz", "Ulrich", "Wilfried", "Detlef", "Friedhelm", "Siegfried", "Joachim", "Ralf"],
               ["Stefan", "Markus", "Thomas", "Michael", "Andreas", "Christian", "Frank", "Oliver", "Jens", "Sven",
                "Tobias", "Daniel", "Matthias", "Florian", "Sebastian", "Jan", "Dirk", "Carsten", "Holger", "Marc",
                "Patrick", "Timo", "Philipp", "Kai", "Benjamin", "Lars", "Nils", "Moritz", "Fabian", "Jonas"],
               ["Bauer", "Brandt", "Dietrich", "Engel", "Faber", "Fuchs", "Graf", "Haas", "Hahn", "Hartmann", "Heinrich",
                "Hofmann", "Jäger", "Kaiser", "Keller", "Kraus", "Krüger", "Lang", "Lehmann", "Lorenz", "Ludwig",
                "Maier", "Möller", "Neumann", "Otto", "Peters", "Pohl", "Roth", "Sauer", "Schäfer", "Scholz", "Schreiber",
                "Schröder", "Schulte", "Seidel", "Sommer", "Stein", "Vogel", "Voigt", "Walter", "Weber", "Werner",
                "Winkler", "Wolff", "Zimmermann", "Beckmann", "Brinkmann", "Dörr", "Eckert", "Frank", "Gebhardt",
                "Haase", "Kessler", "Lindner", "Martens", "Naumann", "Reuter", "Ritter", "Thiele", "Ziegler"]),
    "austrian": (["Helmut", "Franz", "Josef", "Herbert", "Gerhard", "Karl", "Alois", "Erich"],
                 ["Christoph", "Lukas", "Bernhard", "Florian", "Matthias", "Stefan", "Andreas", "Thomas"],
                 ["Gruber", "Huber", "Wimmer", "Pichler", "Moser", "Mayr", "Steiner", "Leitner", "Hofer", "Aigner",
                  "Wallner", "Ebner", "Lechner", "Brunner", "Fuchs", "Holzer"]),
    "swiss": (["Hansruedi", "Urs", "Beat", "Kurt", "Walter", "Peter", "Rolf", "Ernst"],
              ["Reto", "Marco", "Patrick", "Daniel", "Simon", "Lukas", "Fabian", "Adrian"],
              ["Ammann", "Baumann", "Bühler", "Frei", "Gerber", "Keller", "Meier", "Morf", "Rüegg", "Schmid",
               "Steiner", "Suter", "Widmer", "Zürcher", "Brunner", "Huber"]),
    "italian": (["Giorgio", "Sergio", "Franco", "Giancarlo", "Luigi", "Mario", "Bruno", "Gianni", "Carlo", "Renzo"],
                ["Marco", "Andrea", "Luca", "Matteo", "Davide", "Simone", "Alessandro", "Stefano", "Paolo", "Fabio"],
                ["Bianchi", "Colombo", "Conti", "Costa", "De Luca", "Ferrara", "Galli", "Gatti", "Greco", "Lombardi",
                 "Mancini", "Marini", "Moretti", "Pellegrini", "Rinaldi", "Rizzo", "Ruggeri", "Sala", "Testa", "Villa"]),
    "british": (["Brian", "Colin", "David", "Geoff", "Graham", "Keith", "Malcolm", "Nigel", "Roger", "Trevor"],
                ["Andrew", "Chris", "James", "Mark", "Matt", "Paul", "Richard", "Simon", "Steve", "Tom"],
                ["Atkins", "Bennett", "Carter", "Clarke", "Cooper", "Edwards", "Fletcher", "Gibson", "Hall", "Harris",
                 "Hughes", "Lawrence", "Marsh", "Mitchell", "Parker", "Shaw", "Turner", "Walsh", "Webb", "Wright"]),
    "belgian": (["Jean-Pierre", "Marc", "Luc", "Patrick", "Dirk", "Guy", "Willy", "Jacques"],
                ["Kevin", "Pieter", "Thomas", "Nicolas", "Bart", "Jeroen", "Maxime", "Stijn"],
                ["Peeters", "Janssens", "Maes", "Jacobs", "Mertens", "Willems", "Claes", "Goossens", "Wouters",
                 "Dubois", "Lambert", "Dupont", "Martin", "Leclercq", "Van den Broeck", "De Smet"]),
    "dutch": (["Jan", "Henk", "Kees", "Piet", "Gerrit", "Wim", "Joop", "Hans"],
              ["Bas", "Jeroen", "Ruud", "Sander", "Mark", "Niels", "Thijs", "Erik"],
              ["de Vries", "van Dijk", "Bakker", "Visser", "Smit", "Meijer", "de Boer", "Mulder", "Bos", "Vos",
               "Peters", "Hendriks", "van Leeuwen", "Dekker"]),
    "french": (["Jean-Claude", "Michel", "Alain", "Bernard", "Gérard", "Philippe", "Daniel", "Patrick"],
               ["Julien", "Nicolas", "Sébastien", "Olivier", "Thomas", "Romain", "Guillaume", "Mathieu"],
               ["Bernard", "Dubois", "Durand", "Fontaine", "Garnier", "Girard", "Lefèvre", "Mercier", "Moreau",
                "Morel", "Perrin", "Roux", "Simon", "Vincent"]),
    "swedish": (["Lars", "Bengt", "Göran", "Sven", "Kjell", "Lennart", "Rolf", "Stig"],
                ["Johan", "Fredrik", "Magnus", "Anders", "Henrik", "Niklas", "Patrik", "Mattias"],
                ["Andersson", "Johansson", "Karlsson", "Nilsson", "Eriksson", "Larsson", "Olsson", "Persson",
                 "Svensson", "Gustafsson", "Lindqvist", "Berg"]),
    "danish": (["Jørgen", "Henning", "Ole", "Bent", "Poul", "Erik"],
               ["Mads", "Rasmus", "Jesper", "Kasper", "Morten", "Søren"],
               ["Jensen", "Nielsen", "Hansen", "Pedersen", "Andersen", "Christensen", "Larsen", "Sørensen"]),
    "czech": (["Jiří", "Jan", "Petr", "Josef", "Miroslav", "Zdeněk"],
              ["Tomáš", "Martin", "Lukáš", "Jakub", "Ondřej", "David"],
              ["Novák", "Svoboda", "Dvořák", "Černý", "Procházka", "Kučera", "Veselý", "Horák"]),
    "spanish": (["José", "Antonio", "Manuel", "Francisco", "Juan", "Javier"],
                ["Carlos", "David", "Sergio", "Pablo", "Álvaro", "Raúl"],
                ["García", "Martínez", "López", "Sánchez", "Romero", "Navarro", "Torres", "Ruiz"]),
    "japanese": (["Hiroshi", "Takashi", "Kenji", "Masahiro", "Yoshio", "Akira"],
                 ["Daisuke", "Takuya", "Yuki", "Shinji", "Kazuki", "Ryo"],
                 ["Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Yamamoto", "Nakamura", "Kobayashi"]),
    "american": (["Bob", "Jim", "Bill", "Gary", "Larry", "Dennis"],
                 ["Mike", "Chris", "Jason", "Brian", "Kevin", "Scott"],
                 ["Miller", "Davis", "Wilson", "Anderson", "Taylor", "Moore", "Jackson", "Thompson"]),
}
CODE = {"GER": "german", "D": "german", "AUT": "austrian", "A": "austrian", "SUI": "swiss", "CH": "swiss",
        "ITA": "italian", "I": "italian", "GBR": "british", "GB": "british", "UK": "british", "BEL": "belgian",
        "B": "belgian", "NED": "dutch", "NL": "dutch", "FRA": "french", "F": "french", "SWE": "swedish",
        "S": "swedish", "DEN": "danish", "DK": "danish", "CZE": "czech", "CZ": "czech", "ESP": "spanish",
        "E": "spanish", "JPN": "japanese", "J": "japanese", "USA": "american"}
NAME_HINT = [(r"alfa|jas|nordauto|tamagnini", "italian"), (r"brun|bemani|emil frey|r-motorsport|\bsss\b", "swiss"),
             (r"volvo|ips", "swedish"), (r"\brbm\b|\bwrt\b|comtoyou", "belgian"),
             (r"rover|tamchester|maxted|tom walkinshaw|twr", "british"), (r"kaučuk|kaucuk", "czech"),
             (r"tom'?s|nismo|kunimitsu|nissan|toyota|lexus", "japanese"), (r"grt|grasser|eggenberger", "austrian")]
MAKES = [("Audi", r"audi|abt|phoenix|rosberg.*audi|\bwrt\b|azr|sms schmidt"), ("BMW", r"bmw|schnitzer|\brbm\b|\brmg\b|\brmr\b|mtek|linder|bigazzi|isert"),
         ("Mercedes", r"mercedes|amg|\bhwa\b|zakspeed.*(merc|amg)|persson|mücke|muecke"), ("Opel", r"opel|irmscher|holzer|joest.*opel|calibra"),
         ("Alfa Romeo", r"alfa|jas\b|nordauto"), ("Ford", r"ford|grab|wolf racing|hwrt"), ("Volvo", r"volvo"),
         ("Rover", r"rover"), ("Lamborghini", r"lamborghini|grt\b"), ("Ferrari", r"ferrari|af corse|emil frey.*ferrari"),
         ("Porsche", r"porsche|manthey|ssr\b|toksport"), ("McLaren", r"mclaren|dörr|doerr"), ("Aston Martin", r"aston|r-motorsport")]


def h(*parts):
    return int(hashlib.sha1("|".join(map(str, parts)).encode("utf-8")).hexdigest(), 16)


def team_nations():
    """season -> team -> nationality, from pack data or the entry list's team base."""
    out = {}
    for d in glob.glob(str(ROOT / "seasons/*")):
        season = os.path.basename(d)
        m = {}
        tf = os.path.join(d, "data/teams.json")
        if os.path.exists(tf):
            j = json.load(open(tf, encoding="utf-8"))
            for t in (j["records"] if isinstance(j, dict) else j):
                m[t["name"]] = t.get("nationality") or "german"
        ef = os.path.join(d, "research/entries.csv")
        if os.path.exists(ef):
            for r in csv.DictReader(open(ef, encoding="utf-8")):
                base = r.get("team_base") or ""
                code = re.search(r"\(([A-Z]{1,3})\)", base)
                if r.get("entrant") and r["entrant"] not in m and code and code.group(1) in CODE:
                    m[r["entrant"].strip()] = CODE[code.group(1)]
        out[season] = m
    return out


def nationality(season, team, nations):
    n = nations.get(season, {}).get(team)
    if n in NAMES:
        return n
    low = team.lower()
    for pat, nat in NAME_HINT:
        if re.search(pat, low):
            return nat
    return "german"


def make_of(team):
    low = team.lower()
    for make, pat in MAKES:
        if re.search(pat, low):
            return make
    return None


def main():
    tb = json.load(open(ROOT / "docs/staff/teams_by_season.json", encoding="utf-8"))
    rows = list(csv.DictReader(open(STAFF, encoding="utf-8")))
    rows = [r for r in rows if not r["note"].startswith("Same manufacturer-level role as ")]  # rerun-safe
    real_names = {r["person"] for r in rows}
    filled = {(r["season"], r["team"], r["role"]) for r in rows}
    nations = team_nations()
    added_assumed, fict = [], []
    people = {}  # (key, role, block) -> (name, nat, born)
    used_per_season = {}

    for season in sorted(tb, key=lambda s: int(s.split("-")[1])):
        year = int(season.split("-")[1])
        used = used_per_season.setdefault(season, set())
        for team in tb[season]:
            make = make_of(team)
            for role in ROLES:
                if (season, team, role) in filled:
                    continue
                # 1. copy a real manufacturer-level person from a same-make team
                if role in MAKE_ROLES and make:
                    src = [r for r in rows if r["season"] == season and r["role"] == role and r["team"] != team
                           and make_of(r["team"]) == make and "manufacturer level" in r["note"].lower()]
                    if src:
                        s = src[0]
                        added_assumed.append(dict(season=season, team=team, role=role, person=s["person"], status="assumed",
                                                  source=s["source"],
                                                  note=f"Same manufacturer-level role as {s['team']} ({make}). " + s["note"]))
                        continue
                # 2. fictional person, kept for a few seasons
                nat = nationality(season, team, nations)
                key = make if (role in MAKE_ROLES and make and year >= 1990) else team
                block = year // TENURE[role]
                pk = (key, role, block)
                if pk not in people:
                    first_old, first_new, last = NAMES[nat]
                    lo, hi = AGE[role]
                    born = year - (lo + h(*pk, "age") % (hi - lo + 1))
                    firsts = first_old if born < 1960 else first_new
                    for i in range(200):
                        name = f"{firsts[h(*pk, 'f', i) % len(firsts)]} {last[h(*pk, 'l', i) % len(last)]}"
                        if name not in real_names and name not in used:
                            break
                    people[pk] = (name, nat, born)
                name, nat, born = people[pk]
                used.add(name)
                fict.append(dict(season=season, team=team, role=role, person=name, status="fictional",
                                 nationality=nat, born=born,
                                 note=("Shared by the " + make + " teams. " if key == make else "") +
                                      "Made-up name for an empty role; not a real person."))

    with open(STAFF, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["season", "team", "role", "person", "status", "source", "note"])
        w.writeheader()
        allrows = rows + added_assumed
        allrows.sort(key=lambda r: (int(r["season"].split("-")[1]), r["team"], ROLES.index(r["role"]), r["person"]))
        w.writerows(allrows)
    with open(FICT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["season", "team", "role", "person", "status", "nationality", "born", "note"])
        w.writeheader()
        w.writerows(fict)
    print(f"assumed copies added: {len(added_assumed)}, fictional rows: {len(fict)}, "
          f"fictional people: {len(set((p[0]) for p in people.values()))}")


if __name__ == "__main__":
    main()
