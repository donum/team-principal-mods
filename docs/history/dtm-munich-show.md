# DTM Munich Olympic Stadium show event, 2011 to 2012

Part of the DTM rules history. A non-championship show event in the
middle of the season, in the style of the Race of Champions (see
`roc-format.md`). The table image is made with
`python -I tools/history_table.py docs/history/dtm-munich-show.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Event | Format | Winners | Quirks |
|---|---|---|---|---|
| 2011 | Munich Olympic Stadium, 16 and 17 July. No points. | Saturday: races between the makes. Sunday: knockout races. The whole DTM field took part. | Mortara (Saturday), Spengler (Sunday). | The DTM's first stadium event. Called a Race of Champions-style event. |
| 2012 | Same place, 14 and 15 July. No points. | Saturday: relay races. Sunday: knockout races. | Green and Ralf Schumacher (relay), Ekström (knockout) (?). | |
| 2013 | Dropped. | | | It could not be turned into a points event. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| A non-championship event in the calendar | No | every race scores (A4) |
| Knockout races between two cars | No | N11 |
| Relay races with team mates | No | N11, C8 |
| A short stadium track | Yes | track files |

## Sources

- Wikipedia, "2011 Deutsche Tourenwagen Masters season" and "2012 ..."
  (dates, non-championship, 2011 winners), "Olympiastadion (Munich)" (the
  end in 2013).
- Not confirmed, marked `(?)`: the 2012 winners (from a summary of the
  season page). Not found: cars, qualifying, prize money.

## Discord post

=== post | DTM Munich history | dtm-munich-show
## DTM in Munich's Olympic Stadium, 2011 and 2012

A short one: the DTM's two stadium shows. The table is below.

- **No points, the whole field,** two days in the middle of the season.
- **Races between the makes and relay races on Saturday, knockout races on Sunday.**
- **Dropped for 2013** because it couldn't be turned into a points event.

For the game: a non-championship event in the calendar with its own format. My Race of Champions post has the bigger version of this idea.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
