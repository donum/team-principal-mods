# Team Principal Mods

Community season packs for
[Team Principal: A Racing Manager](https://store.steampowered.com/app/4340600/Team_Principal_A_Racing_Manager/),
published via the Steam Workshop.

The first goal is **historic DTM** (Deutsche Tourenwagen-Meisterschaft) seasons,
starting with **1991**. Formula 1 follows with the Vettel years, 2010 to 2013,
starting with **2012**.

| Season | Status | Folder |
|---|---|---|
| DTM 1987 | 🚧 generated and builds, not yet tested in-game or simulated; vanilla sounds | [`seasons/dtm-1987`](seasons/dtm-1987), on the Group A template (`dtm-1991`) |
| DTM 1990 | 🚧 generated and playable, not yet tested in-game | [`seasons/dtm-1990`](seasons/dtm-1990) |
| DTM 1991 | ✅ playable; lap times need calibrating | [`seasons/dtm-1991`](seasons/dtm-1991) |
| DTM 1992 | 🚧 generated and playable, not yet tested in-game | [`seasons/dtm-1992`](seasons/dtm-1992) |
| DTM 2012 | 🚧 generated, tuned with the simulator (lap times, two stops), feeder series; not yet played in-game | [`seasons/dtm-2012`](seasons/dtm-2012), on the era base [`bases/dtm-era4`](bases/dtm-era4) (2012–2018) |
| DTM 2013 | 🚧 generated and playable, not yet tested in-game | [`seasons/dtm-2013`](seasons/dtm-2013), on the era base [`bases/dtm-era4`](bases/dtm-era4) (2012–2018) |
| DTM 2003, 2006, 2010 | 🚧 generated and build, not yet tested in-game or simulated; vanilla sounds | [`seasons/dtm-2003`](seasons/dtm-2003) (mother season), [`dtm-2006`](seasons/dtm-2006), [`dtm-2010`](seasons/dtm-2010), on the era base [`bases/dtm-era3`](bases/dtm-era3) (2000–2011) |
| DTM 2018 | 🚧 generated and builds, two races per round, feeder series and portraits; not yet tested in-game or simulated | [`seasons/dtm-2018`](seasons/dtm-2018), on [`bases/dtm-era4`](bases/dtm-era4) |
| DTM 2020 | 🚧 generated and builds, two races per round, not yet tested in-game or simulated; vanilla sounds | [`seasons/dtm-2020`](seasons/dtm-2020) (mother season), on [`bases/dtm-era5`](bases/dtm-era5) (2019–2020, on top of era 4) |
| DTM 1984–2026 | 📚 research data ([season archive](tools/build_browser.py)) | `seasons/*/research` |
| All series | 📚 per-venue facts for the track values: grid side, pit lane, climate, race stats ([venues](docs/venues/README.md)); TV commentary and stills as a source ([tv_coverage](tools/tv_coverage/README.md)) | `docs/venues` |
| F1 2012 | 🚧 first Formula 1 pack: generated, tuned with the simulator, not yet played in-game | [`seasons/f1-2012`](seasons/f1-2012), on the era base [`bases/f1-v8`](bases/f1-v8) (2010–2013) |
| F1 2010, 2011, 2013 | 📋 planned on the same base ([plan](docs/plans/F1_V8.md)) | `seasons/f1-20xx/research` |
| BTCC 1991 | 🚧 first British Touring Car pack (first Super Touring year): generated and builds, placeholder tracks, not yet tested in-game or simulated ([backlog](docs/plans/BTCC1991_BACKLOG.md)) | [`seasons/btcc-1991`](seasons/btcc-1991) |

## How it works

The repo only contains **our own content**. A pack is assembled from:

1. a **base pack** taken from your local game install (e.g. `data/default26`),
   which supplies the engine files we don't touch (constants, audio, tyre
   model...), and
2. our **season overlay**: teams, drivers, staff, engines, tyres, calendar,
   regulation patches, traced tracks and our own artwork. A season can build
   on an **era base** ([`bases/`](bases/README.md)) that holds what a whole
   car generation shares (rules, tracks, engine art, sounds), so a new year
   of that generation only adds its own teams, drivers and calendar. Each
   season still exports one full pack.

```bash
python tools/build_pack.py seasons/dtm-1991
```

```bash
python tools/build_pack.py seasons/dtm-1991 --install
```

`--install` copies the pack into `<game>/data/<pack_folder>` and rebuilds the
**mod browser** for it (`tools/mod_browser.py`): one interactive page per
installed pack with drivers, teams and cars, engines, calendar and tracks,
every background (main menu, team dashboard, per-team dashboard slots, hub
tiles, news pages; pack slots vs shared game-wide art), every sound (vanilla
and ours side by side, plus sound candidates) and every file, each marked as
ours or vanilla. It is written to
`private/mod_browser/<pack_folder>/index.html` (gitignored: it can carry
private audio). Set your game
path with `--game`, or in a `local.json` file (gitignored):

```json
{ "game_path": "X:/SteamLibrary/steamapps/common/Team Principal A Racing Manager" }
```

The build validates cross-references: teams ↔ drivers ↔ engines ↔ tyres ↔
calendar ↔ tracks. Placeholder geometry is used for venues we haven't traced
yet, and is reported in the output.

### Simulating seasons without the game

`tools/simulate.py` plays whole seasons with the game's own code, in
spectator mode, without opening the game. It loads the game's Python modules
straight from `TeamPrincipal.exe` (unpacked once into `private/game_code/`)
and drives its real screens headlessly: week advance, AI management,
testing, practice, qualifying, race and scoring. Each run works in its own
sandbox under `build/sim/`, so the game install is never written to.

One-time setup, a venv with the Python and pygame versions the game uses:

```bash
py -V:3.13 -m venv private/sim-venv
```

```bash
private/sim-venv/Scripts/python -m pip install pygame==2.6.1
```

Then, after `tools/build_pack.py` (sims use `dist/<pack_folder>`):

```bash
python tools/simulate.py dtm-2013 --runs 6
```

That runs six new careers side by side (about 40 minutes for one season)
and writes `report.md`: simulated poles against the real ones per round,
winners, and team and driver point shares against the real season in
`research/results/`. `--seasons N` plays several seasons per career,
`--save` continues from a save, `--installed` uses the installed pack.
Each run keeps the game's own saves in `run-NN/saves/`, so
`tools/calibrate.py --observe-save` works on them too.

Limits: the game's code must match the installed game (a game update is
unpacked again automatically), and anything only the UI shows, like sounds
or screen layouts, still needs the real game.

## Docs

- [Modding capabilities and limits](docs/CAPABILITIES.md): what the game
  lets us change, what has to be approximated, and the open questions.
- [Wish list for the game developer](docs/DEVELOPER_WISHLIST.md): what the
  game would need for full historical accuracy.
- [DTM eras](docs/ERAS.md): the six eras from 1984 to today, and how each
  maps to the game.
- [Era bases](bases/README.md): one shared base per car generation, one
  season folder per year on top.
- [DTM 1991 season dossier](seasons/dtm-1991/README.md): sourced facts behind
  the data.

## License

- Tooling: [MIT](LICENSE)
- Content (season data, research, art): [CC BY-NC-SA 4.0](LICENSE-CONTENT.md)

This is unofficial community content. It is not affiliated with the game's
publisher, the DTM, or any manufacturer. Real names are used for historical
description only. Team and maker logos are their owners' trademarks, used
only to identify the teams and makers; the licence of each is in
[LICENSE-CONTENT.md](LICENSE-CONTENT.md) and each pack's `credits.txt`. The
artist's car drawings are not covered by our licences. No third-party mod
files are included.
