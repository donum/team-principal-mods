# Driver careers: source checks

Written by `python -I tools/driver_careers.py build`. Each line is a place where two sources disagree. Fix the source data or add a name to aliases.csv, then rebuild.

- 1995 DTM round 2 heat 2: fandom winner Kurt Thiim, de.wikipedia Rennen wurde annulliert.
- 2000: wins differ from the Wikipedia race list (database vs list): Rennen wurde wegen Starkregen abgesagt 0 vs 2
- 2010: wins differ from the Wikipedia race list (database vs list): Gary Paffett 3 vs 2
- 2016: wins differ from the Wikipedia race list (database vs list): Mattias Ekström 0 vs 1
- 2012: wins fandom vs en.wikipedia: Mattias Ekström 1 vs 0
- 2021: wins fandom vs en.wikipedia: Liam Lawson 0 vs 3
- Names in en.wikipedia that the fandom table of the same season does not have (add to aliases.csv if they are the same person): Susie Wolff (2011), Esteban Muth (2021), Liam Lawson (2021), Sheldon van der Linde (2021), Sophia Flörsch (2021)
- Career wins that differ from the fandom career box (database vs box): Klaus Ludwig 37 vs 38; Mattias Ekström 22 vs 23; Kurt Thiim 18 vs 19; Nicola Larini 16 vs 18; Alessandro Nannini 13 vs 14; Manuel Reuter 10 vs 11; Steve Soper 9 vs 10; Frank Biela 7 vs 9; Christian Danner 4 vs 5; Olaf Manthey 2 vs 5
