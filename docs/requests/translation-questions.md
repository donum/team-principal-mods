# Translation review: questions to the developers

- **Context:** the developers asked for a review of their translations,
  German first. Tool: `tools/locale_review.py`, team site `tools/review_site`.
- **Counts** are from `de.json` as of 2026-11-14 (12,919 texts), found with
  simple text searches, so close but not exact.
- **Wishlist:** E13 (pack texts) is related.

## Round 1 (asked 2026-11-16, no answers yet)

1. **Plurals:** 93 texts build plurals the English way, with an `{x_s}`
   placeholder that adds an "s". Examples are "{stops} pit stop{stops_s}" and
   "{sc} time{sc_s}". German plurals don't work like that
   ("Boxenstopp"/"Boxenstopps", "Mal"/"Male"), so the German text now reads
   "Boxenstopp {stops_s}". Could plural forms be added, for example separate
   `_one` and `_other` keys?
2. **Ordinals:** 140 texts use `{pos_ord}`. Does it come out as "1st" or as
   "1."? German writes "1." or "Erster", and the ending changes with the
   sentence ("als Erster", "auf dem ersten Platz").
3. **Grammatical gender:** "To the Team Principal" became "An die Team
   Principal", which is feminine. Does the game know the player's gender, so
   a text could say "An den Teamchef" or "An die Teamchefin"? If not, what
   should we use?
4. **"Du" or "Sie"?** About 1,000 texts use the formal "Sie". 37 use the
   informal "du", including the character creation screen ("DEINE
   IDENTITÄT"). Which one is wanted? Is it fine for quotes from drivers in
   the news to use "du"?
5. **News and mail texts:** 2,859 texts are mail and news templates. Are they
   final, or will they still change a lot? We'd rather review the stable
   parts first.
6. **Pack texts:** 958 `text.pack.*` texts come from the vanilla season
   packs. How is a key made from the English text? Can mod packs ship their
   own `de.json`?
7. **Which texts matter most?** There are 1,654 editor and validation
   messages, for example `$.categories[{i}].key must be…`, and 14 debug
   texts. Do these need German at all? Should they stay in English for
   modders?
8. **What format do you want our changes in?** We can send a JSON file with
   only the changed keys, in your format, plus a table with the English text,
   the old German, the new German and a reason. Does that work? And will keys
   stay the same between updates, so our changes still apply?

## Not asked yet (for round 2)

- **Currency:** English uses dollars ("$12M"). German mixes "${amount}M",
  "${amount} Mio." and "{amount} Mio. $", and has no euro. Stay in dollars,
  and in which format? Or follow the language or the season pack?
- **Number format:** does the game format placeholder numbers for German
  (1.000 and 2,5), or always the English way?
- **Speed units:** two texts show mph. km/h for German, or are they
  oval-only, where mph is right?
- **Game name:** keep "Team Principal" as the name and use "Teamchef" for
  the job?
- **Motorsport terms:** German words or the English ones German TV uses
  (Qualifying 94 times vs Qualifikation 38, Rennleitung vs Race Control,
  Grid vs Startaufstellung)? Our suggestion: follow German TV.
- **English left as is:** 385 texts are the same in English and German.
  Intended, or not translated yet?
- **Text length:** is there a length limit per screen, or does the game
  shorten long text? Which places are tight?
- **Other reviewers:** is someone already reviewing German?

## Fixed by us, no question needed

Machine translation picked the wrong meaning. We fix these in the review:
track as "Gleis" (25 times), circuit as "Schaltung"/"Stromkreis" (19),
compound as "Verbindung" (16), practice as "Praxis" (12), driver as
"Treiber" (18), docked points as "angedockt", "DRS Disabled" as "DRS
Behinderte".
