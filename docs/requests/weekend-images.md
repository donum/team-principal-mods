# Weekend images: track, session and result

- **Status:** draft, not posted
- **Wishlist:** E17
- **Attach:** pick from `img/weekend-images/` (suggested: 01, 02, 13, 05, 07, 10)
- **Length:** about 1,500 characters (Discord limit 2,000)

---

## Feature request: pictures for the race weekend

Hey! One more from the DTM packs, this time about the race weekend.

The team dashboard already shows a photo behind the panels, and it makes a big difference. The weekend itself has no pictures: the loading screens are a progress bar on black, Simulate / Take Part are two grey boxes, and the results are tables only.

So my idea: **a pack can add images to the weekend, and the game picks the one that fits.**

- **Loading cards:** practice, qualifying and race load over a picture of the track, with the session, round, weather and track outline. The game already knows all of these.
- **Between sessions:** a short card from the result, for example "Rockenfeller takes pole", with portrait and car.
- **Results for your team:** the picture follows how your team did: win, podium, points, no points or retired.
- **Optional archive:** an older picture of the track with the year and a caption.

Each picture falls back: the track's picture for that session, then one pack picture for that session, then today's screen without a picture. Packs without images look exactly as today.

```json
"weekend_images": {
  "practice": ["practice.jpg"],
  "qualifying": ["qualifying.jpg"],
  "race": ["race.jpg"],
  "nuerburgring13": {
    "practice": ["nbr_practice.jpg"],
    "qualifying": ["nbr_quali.jpg"],
    "race": ["nbr_start.jpg"],
    "archive": [{ "file": "nbr_1987.jpg", "year": 1987, "caption": "..." }]
  },
  "results": { "win": ["win.jpg"], "no_points": ["meh.jpg"], "retired": ["garage.jpg"] }
}
```

Mock-ups for the 2013 season are attached. What do you think?

---

## The mock-ups

All are 1920 × 1080, made from the game's own layout with the race we simulated
on 2026-11-14 (BMW Team MTEK, Nürburgring, round 7 of 10). The pink notes
explain each screen and are not part of the design.

| File | Proposal | Shows |
|---|---|---|
| `01-loading-practice.jpg` | 1 Loading cards | Practice loading over a track photo, title block and weather, track outline bottom right |
| `02-loading-qualifying.jpg` | 1 Loading cards | Qualifying card. Same layout; a wet session shows only in the weather chip |
| `03-race-choice.jpg` | 1 Loading cards | Simulate / Watch over the dimmed start photo, forecast strip |
| `04-week-loading.jpg` | 1 Loading cards | Week advance before a race week, with the pack's track art and a three-day forecast |
| `05-between-sessions.jpg` | 2 Weekend in three acts | Qualifying card: pole, top three, where your cars start |
| `06-starting-grid.jpg` | 2 Weekend in three acts | Grid table with a race strip in the empty space below |
| `07-results-no-points.jpg` | 2 Weekend in three acts | Results with a "no points" picture of our own car |
| `08-results-win.jpg` | 2 Weekend in three acts | The same race played as Schnitzer: "win" picture |
| `09-results-retired.jpg` | 2 Weekend in three acts | Played as Phoenix: "retired" picture, from the pack-wide set |
| `10-archive-loading.jpg` | 3 Track archive | Race loading with a 1987 picture, year and caption |
| `11-archive-story.jpg` | 3 Track archive | Winner card with a 2006 photo of Spengler at the same track |
| `12` to `19-loading-<track>.jpg` | 1 Loading cards | The same card at the other eight 2013 tracks (Hockenheim as the race card) |

The source page is in the session scratchpad and not kept; the screens are
simple HTML over the photos and can be rebuilt.

## The full weekend

`img/weekend-journey/` walks through one race weekend as BMW Team MTEK at the
Nürburgring, every session simulated: dashboard in the off week, next week,
dashboard in race week, practice, simulating practice, practice results,
qualifying, simulating qualifying, qualifying results, the card between
sessions, the starting grid, race, simulating race, race results and the
dashboard after the race. Two more screens show the fallback: the pack's
one picture for the session, and no picture at all (today's screen).

The starting grid (`11-starting-grid.jpg`) has the facts on top, the grid
as it stands on the track in the middle (cars face left, so the start line
is on the left and pole is in the lower lane), and the full table below.

## More screens: grid and pre-race

`img/weekend-grid/` has 20 more screens for the grid and the minutes
before and after the start, with every entry's livery: grid boxes, the
grid on the track art, front row, your cars, TV graphic, grid by rows,
race plan, lap-by-lap forecast, start lights, formation lap, grid walk,
pit lane open, spotter guide, team-mates, tower and photo, pole car
loading card, grid to flag, parc fermé and the first laps. Same race, same
pictures as above.

All mock-ups can be browsed in one gallery:
https://claude.ai/artifact/6cjkA3ucBe1gM5gB3WPemN (private).

## Pictures used

| Screen | Picture | Source and licence |
|---|---|---|
| 01, 02, 03, 05, 06, 07, 08, 11 | Nürburgring 2013 race weekend | BMW Group press photos (P90131860, P90131866, P90131935, P90131940, P90131947, P90131948, P90131950, P90131865), `Pictures/mods/dtm-2013/teams/*/press_bmw` |
| 12 to 19 | The other 2013 tracks | Hockenheim, Brands Hatch: Flickr CC (Hockenheimring May 8715506906; Brands Hatch 9265350692). Norisring: BMW press P90128281. Zandvoort: Dennis de Wolde (permission). Red Bull Ring (Motor VS Motor), Lausitzring (elJenso), Moscow (Andrey Velichko), Oschersleben (n0rmili): `ask_permission` folders, mock-up only |
| 09 | MTEK pit stop, Hockenheim 2013, greyscale | BMW Group press photo P90119239 |
| 04 | Nürburgring race-day art | Our own pack art, `seasons/dtm-2013/assets/tracks/nuerburgring13.png` |
| 10 | BMW M3, Nürburgring 1987 | Frame from an RTL TV recording (`dtm-1987/livery_pack/_video_candidates`). Mock-up only, not for a pack |
| 11 | Bruno Spengler, Nürburgring 2006 | Raimond Spekking, CC BY-SA 4.0, Wikimedia Commons |
| 05, 07 to 09, 11 | Portraits and car drawings | Our own pack files |

Before any of this goes into a pack, every photo needs the same check as the
dashboard backgrounds (`backgrounds-gpt/CREDITS.csv`). Press photos and TV
frames are fine for a mock-up, not automatically for a Workshop pack.

## Pictures still missing (ChatGPT prompts)

Three buckets have no good photo yet. These prompts follow the style of the
dashboard backgrounds: a real 2013 photo as the base when we have one,
otherwise a generic scene with no logos and no readable faces.

1. **Win (pack-wide).** "Photorealistic 16:9 image. A 2013 DTM touring car
   team celebrates at the pit wall as their car crosses the finish line. Crew
   in white race suits lean over the barrier with raised arms. Late afternoon
   light, shallow depth of field. No readable sponsor names, no faces in
   focus."
2. **Retired (pack-wide).** "Photorealistic 16:9 image. A 2013 DTM touring car
   stands inside a pit garage with the shutter half down. Two mechanics look
   at the open engine bay. Cool light, quiet mood. No readable sponsor names,
   no faces in focus."
3. **Practice, quiet paddock (per track, here the Nürburgring).** "Extend this
   photo to 16:9 for a loading screen: [attach a real Nürburgring 2013 pit lane
   photo]. Keep the cars and buildings as they are, add only sky and tarmac at
   the edges."
