# Backlog: DTM 2018 pack

Everything still open for the 2018 pack, as of 14 November 2026. Game limits
are in [DEVELOPER_WISHLIST.md](../DEVELOPER_WISHLIST.md), not here. Era-wide
items (per-track values, audio, art rules) are in the
[2013 backlog](DTM2013_BACKLOG.md) and apply to 2018 too, since it builds on
`bases/dtm-era4`.

Priority: **P1** = changes how the game plays, **P2** = more of the real
2018 world, **P3** = presentation.

State: the pack is generated from `research/` and builds without errors
(`python tools/build_pack.py seasons/dtm-2018`). Nothing has been tested
in-game or simulated yet.

## 1. Tracks · P1

| Venue | Today | To do |
|---|---|---|
| Lausitzring GP, 4.570 km (round 2, official timing sheets) | traced into the base (`lausitzring_gp`): 4,504 m, −1.4%; 2018 sets `length_km` 4.57 | Calibrate `speed_scale`. 2020 uses the track too and still has en.wiki's 4.345 km: check 2020's timing sheets. |
| Brands Hatch GP, 3.916 km (round 6) | traced into the base (`brandshatch_gp`): 3,864 m | Calibrate `speed_scale` and `tyre_wear_mult` (first guess 0.9). Check the DRS zone: the tool put it on the longest traced straight (progress 0.41 to 0.56), which may not be where the DTM had it. |
| Misano, 4.226 km (round 7, night race) | traced into the base (`misano`): 4,171 m, start placed by hand | Calibrate `speed_scale`. |
| Hungaroring (round 3) | F1 base track, `speed_mult` 1.09 | Check the lap time in a simulated season. |

Then race-day maps for the new venues (race-track-themes, `tools/art_track.py`),
as for 2013.

## 2. Simulate and calibrate · P1

- Run `python tools/simulate.py dtm-2018 --runs 6` and compare poles,
  winners and point shares with `research/` (add `research/results/` per
  round first, as for 2012).
- 2018 cars lost their side winglets and some downforce against 2013: fit
  per-track `speed_mult` in `gen.json` from the 2018 poles, as 2012 did.
- Check that two races in a row at one track work in the game (the second
  week repeats practice and qualifying).
- Tyre wear: the base's values were tuned for two stops in a 2013 race of
  about 190 km. 2018 races are 55 minutes with one stop. Tune `tyre_wear_mult`.

## 3. Rules to check · P2

- Done (14 November 2026): one dry slick, no option tyre (as 2012:
  `data/tyremodel.json`, two-compound rule off); DRS on 12 laps per race
  (wish list B6); 1,115 kg confirmed. Simulate to check one stop per race.
- Still open: tyre sets per car per weekend in 2018.

## 4. Art · P3

- Car images: none yet. Ask whether Pappydhorn12 draws 2018 too, else
  placeholders with `tools/car_art.py` (needs C63 and M4 outlines).
- Team list icons: maker emblems from the base, like 2013 (`art/logos.json`
  with `"team_tiles": "maker"`, `tools/logo_art.py seasons/dtm-2018`).
- Portraits: done for the 21 DTM drivers (`art/portraits.json`, all
  pinned). Commons has little from 2018: six are from 2018 events, the rest
  from 2014 to 2024. Philipp Eng has a helmet card: his only 2018 photo
  (`Peng2018.jpg`) looks like a BMW press photo uploaded as own work.
  Better 2018 photos would come from InMotion (Dennis de Wolde, Zandvoort
  2018) if he allows portrait crops. Feeder drivers come from Wikidata
  automatically, with helmet cards where Commons has nothing.
- Main menu and team dashboards: see "Backgrounds" below.
- Colours in `gen.json` are first estimates; check them against 2018 photos.

### Backgrounds 🎨 (need ChatGPT image editing)

The 2018 photos are in the image gallery outside the repo:
`C:/Users/dan/Pictures/mods/dtm-2018/teams/<team>/` (credit CSVs per
folder), viewer `C:/Users/dan/Pictures/mods/gallery/` (season picker at the
top). 191 photos: Matt Buck's Brands Hatch set on Commons (CC BY-SA 2.0)
and 41 InMotion Zandvoort photos by Dennis de Wolde (permission). The
"Pools" view shows the picks per team and the menu picks under `_menu`
(`gallery/seasons/dtm-2018/pools.js`).

**Crop-only proposals.** 27 team backgrounds (three per team, slots 2 to 4)
and seven menu crops are in `C:/Users/dan/Pictures/mods/dtm-2018/backgrounds-crop/`,
made by `make_crops.py` there (copied from 2012's). They are 16:9 crops at
1672x941, placed so as much of the car as possible sits outside the game's
panels. The gallery's Backgrounds tab shows them with the panels on top.
Review them there (keep, redo, drop) and paste "Copy review" back.

**What ChatGPT has to change.** Every item carries a brief (`"gpt"` in
`manifest.json`, on the card in the Backgrounds tab; "Copy ChatGPT briefs"
copies them all for the current filter). The targets are the same as 2012:

- **Team dashboard:** right of the sidebar (from 19% across) and between
  the info cards and the button bar (47% to 86% down).
- **Main menu:** right of the menu buttons (from 40% across) and clear of
  the wordmark top right. Use the flat 2015-2018 wordmark (docs/ERAS.md),
  not the 2000-2016 one in `gallery/workshop_src/`: it still has to be
  saved there.

Things to know before the edits:

- 16 of the 27 team picks are InMotion files at only 1278x852, so they are
  upscaled. Every one of their briefs asks to remove the watermark.
  **Ask Dennis de Wolde for the full-size Zandvoort 2018 files first.**
- Most side-on shots need only a small move (2 to 8%). The bigger jobs:
  RBM 2 (Eriksson through the catch fence, wide low photo), RBM 4 (pit
  lane, car runs off the right edge), RMG 3 (fence mesh and post),
  SILBERPFEIL 2 (fence wires), and the four head-on cars (Abt Sportsline 4,
  Phoenix 3, RMR 4, SILBERPFEIL 3), which have to shrink.
- Duval (#28), Ekström (#5) and Zanardi (#12) have no usable side-on shot.

**Main menu candidates** (`backgrounds-crop/menu/`). Unlike 2012, real
photos of the whole field exist, so no plate is needed:

| File | Shot | Photographer, licence | What ChatGPT must do |
|---|---|---|---|
| `title_bg_1.jpg` | **First pick.** The bunched field through a right-hander at Brands Hatch, packed grandstand and Deutsche Post boards behind | Matt Buck, CC BY-SA 2.0 | Extend the left by about 12% so the field clears the menu. |
| `title_bg_2.jpg` | The field under the Deutsche Post bridge, trees all round | Matt Buck, CC BY-SA 2.0 | Little: the field already sits right. Extend the left by about 8%. |
| `title_bg_6.jpg` | The field in the Zandvoort dunes, two green Audis in front | Dennis de Wolde, permission | Remove the watermark; upscaled, so ask for the full-size file. |
| `title_bg_3.jpg` | The field into a right-hander, packed grandstand above | Matt Buck, CC BY-SA 2.0 | Remove the loudspeaker pole bottom right; extend left. |
| `title_bg_4.jpg` | The field close up, two and three wide, Rast in front | Matt Buck, CC BY-SA 2.0 | The front cars sit under the menu: extend the left a lot. |
| `title_bg_5.jpg` | The field close up, Eng and Glock in front | Matt Buck, CC BY-SA 2.0 | Same as 4. |
| `title_bg_7.jpg` | Frijns leads Glock, Wittmann and Farfus, close up | Dennis de Wolde, permission | Remove the watermark; Farfus top left sits under the menu. |

**Decided (13 November 2026): `title_bg_1.jpg` for both the main menu and
the Workshop image.** Five finished looks of it are in
`backgrounds-crop/posters/` (`poster_versions.py`): A clean, B golden
afternoon, C spotlight, D cinematic, E speed. Each has `title_bg.png`
(2560x1440 with the flat DTM 2018 wordmark top right), `main_square.jpg`,
`main_wide.jpg` and a menu mock-up. The photo sits against the right edge
(as `tools/menu_art.py` does), so the field clears the menu without AI. The
ChatGPT briefs for each look are in `posters/BRIEFS.md`. Still to do: pick a
look, then wire it into `seasons/dtm-2018/art/menu.json` (`"in_pack": true`,
CC BY-SA 2.0, Matt Buck) and a Workshop builder like 2013's `ws_build.py`.
The local file is 1920 px wide; the Commons original is 5672 px and would
give a sharper 2560 px image.

**Update (14 November 2026): the pick changed to 3 with a blue sky and 7.**
ChatGPT versions were dropped (wrong race numbers, garbled lettering); the
images now stay with the real photo: gentle grade, light sharpening, sky
pixels swapped for a blue gradient on 3, the INMOTION watermark cut and filled
on 7. Finished sets are in `backgrounds-crop/final/` (`final.py`); seven more
candidates in `backgrounds-crop/round2/` (`round2.py`). All rounds are in the
gallery's Drafts tab for 2018. Still to do: choose between 3 and 7, wire it
into `art/menu.json` with credits, and build the Workshop images. For 7, ask
Dennis de Wolde for the full-size Zandvoort 2018 files (the web file is
upscaled 2.1x). 2012 drafts: `Pictures/mods/dtm-2012/backgrounds-crop/drafts2012.py`,
Drafts tab for 2012.

## 5. More of the real season · P2

- Sponsors per team (`sponsors` in `gen.json`, as in 2013): PETRONAS,
  REMUS, SILBERPFEIL Energy, Schaeffler, Shell, Deutsche Post, ZF and others.
- Feeder series: done (F3 European, Carrera Cup Deutschland, TCR Germany,
  ADAC F4, plus six free agents; see the README). Open: Carrera Cup points
  scale is reconstructed, and a few birth dates have one source only (see
  each `research/juniors/*.md`).
- Sounds: the base's overlay comes from 2012 and 2013 cars. The 2018
  engines were the same V8s, so it stays; 2018 recordings could replace it
  later.
