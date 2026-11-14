# Backlog: DTM 2012 pack

Everything still open for the 2012 pack, as of 13 November 2026. Game limits
are in [DEVELOPER_WISHLIST.md](../DEVELOPER_WISHLIST.md), not here. Era-wide
items (per-track values, rule changes over time, audio) are in the
[2013 backlog](DTM2013_BACKLOG.md) and apply to 2012 too, since both build
on `bases/dtm-era4`.

Priority: **P1** = changes how the game plays, **P2** = more of the real
2012 world, **P3** = presentation.

**🎨 = needs ChatGPT image editing.** It is not available right now. These
items are ready to start as soon as it is: the photos are collected and the
picks are made.

## 1. Images waiting for ChatGPT 🎨

The 2012 photo collection is in the image gallery outside the repo:
`C:/Users/dan/Pictures/mods/dtm-2012/teams/<team>/` (sources and credit CSVs
per folder) and the shared viewer `C:/Users/dan/Pictures/mods/gallery/`
(season picker at the top; `python -I build.py dtm-2012`, see its README.txt). It holds 360 photos: 288 from
Commons (every free 2012 DTM file there), 31 Flickr CC photos that are not on
Commons, and the 29 InMotion Zandvoort photos. Its "Pools" view shows the
suggested picks per team (`pools.js`, 5 to 10 track and 0 to 5 box shots per
team) and the menu picks under `_menu`. Some car photos sit in a `people`
folder because of their Commons categories; the pools ignore folders. The
written picks with links are in
[`research/photo_candidates.md`](../../seasons/dtm-2012/research/photo_candidates.md).
Work the same way as for 2013 (see the "Art" section of the
[2013 README](../../seasons/dtm-2013/README.md)): extend to 16:9, remove
watermarks, fences and stray text, then move the car into the strip the
dashboard leaves visible. Keep the car's edges sharp: in 2013, moving the car
left a blurred band at the top and left in ten images, which were dropped.

| Item | What | Picks | Prio |
|---|---|---|---|
| Main menu `title_bg.png` 🎨 | 16:9, add the 2000-2016 DTM wordmark like 2013 (`tools/menu_art.py`, `"in_pack": true`). CC BY-SA sources keep CC BY-SA 2.0. | Six crops to choose from, see "Main menu candidates" below. | P3 |
| Team dashboards 🎨 | One to three per team as `assets/dashboard_bgs/<team>2.jpg`, `<team>3.jpg`... at 1672x941 JPEG; slot 1 is the Oschersleben start for every team now. | Crop-only proposals exist (see below). Pools in the gallery: Brands Hatch (Rowan Harrison, Tom Bayly), Hockenheim (Cord Rodefeld, Kathrin Mezger's garage shots), Norisring (s.yuki), Zandvoort (Dennis de Wolde, Martin de Witte). | P3 |
| Spectator set `dashboard_bg*.png` 🎨 | One per team, PNG copies of the team backgrounds, plus the Oschersleben start. Until then the base's images show. | From the team dashboards above. | P3 |
| Valencia race-day map 🎨 | A race-day image for round 9 in the race-tracks plan frame, then `tools/art_track.py seasons/dtm-2012 valencia` with `--calibrate`. Today the base map puts the cars off the drawn track. | race-tracks has the plan and brief: `dist/styles/plan/valencia/gp@2005.png` and `.brief.md`; race-track-themes has the 2012 edition started (`art/valencia/gp@1999/2012/dtm/round-09`). | P2 |
| 2012 branding on the eight shared maps 🎨 | The maps are copies of 2013's, with 2013 sponsors and boards. Repaint them for the 2012 rounds (different round numbers and partners). | race-track-themes editions for 2012. | P3 |

**Crop-only proposals (no ChatGPT needed).** 23 team backgrounds (two per
team, three for Abt Sportsline) and six menu crops are in
`C:/Users/dan/Pictures/mods/dtm-2012/backgrounds-crop/`, made by
`make_crops.py` there: a 16:9 crop of the source photo, resized to 1672x941
and lightly sharpened, placed so that as much of the car as possible sits
outside the game's panels and the car is never cut off at the edge. The
gallery's Backgrounds tab shows them with the panels on top (badge "crop
only"). Review them there (keep, redo, drop) and paste "Copy review" back.
Kept ones can go into the pack now as slots 2 and 3; ChatGPT edits can replace
them later.

**What ChatGPT has to change.** Every proposal carries a written brief
(`"gpt"` in `manifest.json`, shown on the card in the Backgrounds tab;
"Copy ChatGPT briefs" copies them all for the current filter). The brief is
built from where the car sits in the crop against the band the screen leaves
clear:

- **Team dashboard:** right of the sidebar (from 19% across) and between the
  info cards and the button bar (47% to 86% down). That band is about 3.6:1,
  so a side-on car fits it well and a head-on car has to shrink.
- **Main menu:** right of the menu buttons (from 40% across) and clear of the
  wordmark in the top right corner.

Typical moves: most side-on shots need the car 6 to 8% further right and 5 to
7% lower; the two Norisring shots (RMG) need 24% right because the car sits in
the left third; Schnitzer #7 and Coulthard need 15 to 17% down; Junge Sterne
#24 and Thomas Sabo #11 need to come back left. Six already sit in the band.
Four need more than a move: Phoenix 3 (car far away, scale it up), DHL 3
(fence mesh over the car), Abt Sportsline 4 (garage clutter, fade the third
car) and the two Norisring shots (lift the shadows).

**Main menu candidates** (`backgrounds-crop/menu/`, all Brands Hatch unless
said otherwise):

| File | Shot | Photographer, licence | What ChatGPT must do |
|---|---|---|---|
| `title_bg_5.jpg` | Ekström's Red Bull Audi climbing Paddock Hill, full crowd bank behind | Rowan Harrison, CC BY-SA 2.0 | Little: car 7% right, 7% up. The only 2012 photo with a packed bank. |
| `title_bg_6.jpg` | Junge Sterne Mercedes in the pit lane under the DTM Race Control gantry | Tom Bayly, CC BY-SA 2.0 | Car 11% up; remove the "DTM Race Control" lettering if it crowds the wordmark. |
| `title_bg_1.jpg` | Wolff's pink #24 and Mortara's #21 up Paddock Hill (the research pick) | Rowan Harrison, CC BY-SA 2.0 | Remove the watermark; move the pair right so #24 clears the menu. |
| `title_bg_2.jpg` | The same pair, wider frame | Rowan Harrison, CC BY-SA 2.0 | Same, with more room to move. |
| `title_bg_3.jpg` | Pit lane queue: white BMW M3, Mercedes behind, ultimate and DEKRA banners | Tom Bayly, CC BY-SA 2.0 | Cars 22% right; straighten or remove the pit wall post. |
| `title_bg_4.jpg` | Parc fermé in the rain at the Norisring, six cars, fans with umbrellas | s.yuki, CC BY 2.0 | Paint out the official in the right foreground; keep the rain. |
| `title_bg_7.jpg` | **Plate:** Paddock Hill Bend from the outside, grandstand and E-Postbrief boards, almost empty track | Tom Bayly, CC BY-SA 2.0 | Draw a field of eight to twelve 2012 cars down the hill, as in the 2013 menu image. |

The plate is the way to get a whole field into the picture: no free 2012 photo
shows one. It works like the two 2013 turn-one images did (a real empty track
with the cars drawn on it), with one difference that makes it safer: Rowan
Harrison photographed nearly every 2012 car at this very corner, in the same
light and from the same angle, so every car can follow a real photo instead of
an invented livery. Those photos are the track pools in the gallery. The two
2013 turn-one images were deleted on 13 November 2026: they were never used,
and the cars behind the leaders had invented liveries.

Pick one for `title_bg.png` and keep a second for the Workshop page.

Before the edits, ask Dennis de Wolde for the full-size Zandvoort 2012 files
(the web copies are 900 px; see §3).

## 2. Can be done now (no ChatGPT)

- **Portraits** · P3
  - Pin the 2012 photos found: Coulthard (Tom Bayly, Brands Hatch 2012, CC
    BY-SA 2.0, 7232712624), Schumacher (Ian McWilliams, "Ralf Schumacher DTM
    Mercedes Scooter 2012", CC BY 2.0), Wolff (Ian McWilliams, "Susie Wolff
    DTM Brands Hatch 2012 003", CC BY 2.0). Links in `photo_candidates.md`.
  - Sutil got a helmet card although Commons has many photos of him: check
    why the tool missed him.
  - Check the 67 tool-picked feeder portraits by hand and pin them, as for
    2013. 48 feeder drivers have helmet cards.
  - Frey (2008 photo) and Hand (helmet card): no better free photo exists.
- **Menu music** · P3: the four Kevin MacLeod tracks are in
  `seasons/dtm-2013/assets/audio/music/` (uncommitted). Moving them to
  `bases/dtm-era4/assets/audio/music/` with `"vanilla_music": false` in each
  season would give 2012 the same playlist.
- **Car drawings** · P3: two numbers and three flags are wrong on
  Pappydhorn12's drawings (period photos in `research/spotter_guide.csv`):
  Wickens' stern car is #20 (drawn #21), Wolff's TV Spielfilm car #24 (drawn
  #20), Merhi has a German flag (Spanish), Tambay an Italian one (French),
  Wolff a Union flag (Scottish), and Tomczyk's name panel says "BMW". Ask
  the artist, or fix small text with an `edits` entry in `art/drawings.json`
  as for Scheider in 2013.
- **Workshop page** · P1 before upload: description (credit Pappydhorn12, the
  photographers and the map data from `credits.txt`), preview image, the
  gallery's Workshop tab for 2012 (a `seasons/dtm-2012/ws_build.py` in the
  gallery, modelled on 2013's).

## 3. Permissions

The permissions granted for 2013 cover every year (Spieler Family,
Dennis de Wolde). A yes to any of the open 2013 requests covers 2012 too.

| Who | 2012 material | Status |
|---|---|---|
| Dennis de Wolde (InMotion Photos) | Zandvoort 2012 album, 29 photos | granted; ask for full-size files |
| Harry Maurer (ma917) | Norisring weekend (29 June) and August 2012 | asked for 2013 on 2026-11-10, waiting |
| Erich Hirsch (mobilemuc) | Munich stadium show, July 2012: Werner's car, Schnitzer garage | asked for 2013 on 2026-11-10, waiting |
| Ralfs Motorsportwelt | April 2012 test, Spengler's title car | asked for 2013 on 2026-11-10, waiting |
| imago | agency archive | not asked |

The free photos cover only Hockenheim (April), Brands Hatch, the Norisring and
Zandvoort. Nothing free from the Lausitzring, Spielberg, the Nürburgring,
Oschersleben, Valencia or the finale.

## 4. Research gaps · P2

- Results: Q1 to Q3 times for rounds 1, 5, 6, 7 and 8; the Lausitzring race
  from 4th down (one source); stop laps and retirement reasons
  (`research/results/README.md`).
- Feeder series: F3 Euro Series points per race; birth dates for 13 drivers
  (most in the Procar series); German F3 team standings
  (`research/juniors/*.md`).
- Moscow is not on the 2012 calendar; nothing open there.

## 5. In-game checks · P1

After the simulator tuning (README "Lap times"), play a season and check:

- The single dry tyre: does the game cope with a soft that is a copy of the
  hard, and do most cars stop twice?
- Lap times, especially Valencia (base map, old track file).
- Schnitzer and Thomas Sabo: 26% and 22% of the points in the simulator
  against 18% and 17%.
- The team dashboards (slot 1 only) and the feeder series screens.
