# Translation review site

A small PHP site where a team reviews the game's translations together. Every
message shows the place in the game that displays it, the English text, the
current translation, automatic checks, screenshots with a zoom on the text,
and the team's suggestions. Leads approve changes, put them into packages
and send those to the developers. After a game update the site shows which changes the developers
took.

One site serves all the game's languages (de, fr, es, it, pt-BR, ru). Each
language has its own reviews, glossary, claims, decisions and packages.
Screenshots are shared: a screen looks the same in every language, so a German
picture also shows a French reviewer where a text sits.

Terms are shared too. The Glossary tab is one terminology base for all
languages: each term is an English word with its meaning ("driver: the racing
driver, never a software driver"), and each language adds its own translation,
proposed by anyone and agreed by that language's leads. A term one team starts
shows up for every other team, with the translations already made.

Needs PHP 8.0 or newer with PDO SQLite (or MySQL) and Apache (`.htaccess`).
Nothing to install, no build step.

## Files

| File | What it is |
|---|---|
| `index.php` | The page (login, setup, invite, app shell) |
| `api.php` | Everything the page reads and writes |
| `lib.php` | Config, database, accounts (not reachable from the web) |
| `app.js`, `shots.js`, `app.css` | The page's code and look |
| `config.sample.php` | Copy to `config.php` |
| `.htaccess`, `.user.ini` | Lock the private files, allow 16 MB uploads |
| `data/` | Database, game data files, screenshots. Locked by its `.htaccess` |

## Put it on the web space (HostEurope, FileZilla)

1. Copy `config.sample.php` to `config.php`. The defaults work: SQLite, data
   in `data/`.
2. In FileZilla, make a folder `translation-review` next to `advent` and upload
   everything from this folder into it, including the hidden `.htaccess`,
   `.user.ini` and `data/.htaccess` (FileZilla: Server > Force showing hidden
   files). Don't upload `README.md` or `.gitignore`; it doesn't matter if you do.
3. In the HostEurope KIS, check that the domain runs PHP 8.1 or newer.
4. Open `https://<your domain>/translation-review/`. The first visit asks for
   the admin account (you). Choose a long password.
5. Check that the lock works: `https://<your domain>/translation-review/data/review.sqlite`
   and `.../config.php` must answer "Forbidden" (403), never a download.
6. Team tab > Load a game file: upload the `.json` from
   `private/locale_review/` (see below). Do it once per language.
7. Team tab > Invite someone: name and role. Copy the link and send it to the
   person. It works once, for 14 days.

If the page says "could not find driver", the server has no SQLite. Create a
MySQL database in the KIS and put its data into `config.php` (`db_dsn`,
`db_user`, `db_pass`).

## The game data files

They come from `tools/locale_review.py`, which reads the game's code to find
where each message shows:

```
python tools/locale_review.py                    # German, the game's own de.json
python tools/locale_review.py --lang fr
python tools/locale_review.py --file C:/path/to/de.json
```

Each run writes `private/locale_review/<lang>-<date>-<hash>.json`. Upload it in
the Team tab. Uploading a newer file for a language replaces the old one;
reviews, decisions and screenshots stay.

## The workflow

1. **Review** (everyone): "Looks good", or a suggested text with a reason.
2. **Decide** (leads): approve a text, reject, or mark for discussion.
3. **Package** (leads): approved changes go into a package in the tab
   "To the developers". Making a package sends nothing.
4. **Send** (leads): download the package's JSON file and table, send them to
   the developers yourself, press "Mark as sent". An unsent package can be
   deleted; its changes go back to "approved".
5. **Check** (after a game update): see below.

Nothing on the site changes the game or anyone's files. Everything is saved on
the server as soon as someone presses a button.

## Automatic in-game screenshots

`tools/screen_capture.py` draws the game's screens with its own code, in one
language, without starting the game, and finds where each translated text
lands. It uploads the pictures with a box per message:

```
python tools/screen_capture.py --lang de --push https://<your domain>/translation-review --user <admin name>
```

The password comes from `TP_REVIEW_PASSWORD` or a prompt. A new run replaces
the pictures of the earlier run for the same screens and language; pictures the
team added by hand stay. Without `--push` the results stay in `build/screens/`.
Today it covers the screens that open with just a career, their tabs, the
negotiation screens behind each market, and one simulated race weekend from the
tyre allocation to the results (76 screens, about 1,170 messages in German, about
25 minutes; `--no-weekend` takes 8). Run it for English too (`--lang en`): the
site shows a picture in any language on every language's messages, own language
first, then English. Live sessions still need more set-up. Mails and news get no pictures on purpose: they are full
sentences that read fine on their own, and the site leaves them out of "No
screenshot yet".

## After a game update

1. Run `tools/locale_review.py` again for each language and upload the files.
2. Follow-up tab: every change in a package marked as sent is now **taken**, **changed differently**,
   **still old** (send again) or **English changed** (the key is new, review
   the new message).

## Roles

- **Reviewer**: reviews, suggests, agrees, discusses, adds screenshots, claims
  areas. Any language.
- **Lead**: also approves or rejects, agrees glossary terms and makes and sends packages,
  for the languages set in the Team tab (empty = all).
- **Admin**: also invites people, changes roles, loads game files.

## Backups

Download the `data/` folder with FileZilla now and then. With SQLite it holds
everything: `review.sqlite` (and `review.sqlite-wal` while the site is busy),
`releases/` and `shots/`.

## Test it locally

```
php -S 127.0.0.1:8777 -t tools/review_site
```

with a `config.php` next to `index.php`. The built-in server ignores
`.htaccess`, so check the locks on the real server (step 5 above).
