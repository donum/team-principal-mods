"""Draw the feature-package diagrams for the developer explainer.

Builds each diagram once as SVG and writes:
  - docs/packages/img/<name>.svg  standalone images (light colours) for the repo
  - docs/packages/explainer.html  the explainer page (theme-aware), for publishing

Usage: python -I tools/package_diagrams.py
"""
import os
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'docs', 'packages', 'img')
PAGE = os.path.join(ROOT, 'docs', 'packages', 'explainer.html')

# Light and dark tokens, shared with docs/dtm_rules.html, plus diagram colours.
LIGHT = {
    'bg': '#f2f4f7', 'panel': '#ffffff', 'ink': '#151a22', 'muted': '#5b6474', 'line': '#c9d0db',
    'accent': '#1d4fd8', 'accent-bg': '#e3eaff',
    'fit': '#127a43', 'fit-bg': '#e2f4ea', 'apx': '#9a5b00', 'apx-bg': '#fbefd9',
    'no': '#b4232f', 'no-bg': '#fbe3e5',
    'c1': '#1d4fd8', 'c2': '#0f7a8a', 'c3': '#6b4bc4', 'c4': '#5b6474',
    'std': '#ffffff', 'opt': '#f2c230',
}
DARK = {
    'bg': '#0f1319', 'panel': '#171c24', 'ink': '#e7ebf1', 'muted': '#97a1b2', 'line': '#3a4250',
    'accent': '#7ea2ff', 'accent-bg': '#1c2a4d',
    'fit': '#5fd393', 'fit-bg': '#163325', 'apx': '#f0b44c', 'apx-bg': '#3a2b12',
    'no': '#ff7b85', 'no-bg': '#3d1a1e',
    'c1': '#7ea2ff', 'c2': '#4fc3d4', 'c3': '#b49cff', 'c4': '#97a1b2',
    'std': '#e7ebf1', 'opt': '#f2c230',
}
FONTS = {
    'display': '"Barlow Condensed","Arial Narrow",Arial,sans-serif',
    'body': '"Source Sans 3","Segoe UI",system-ui,sans-serif',
    'mono': '"JetBrains Mono",Consolas,monospace',
}

SVG_CSS = """
.pn{fill:var(--panel);stroke:var(--line);stroke-width:1.2}
.pn-d{fill:var(--panel);stroke:var(--muted);stroke-width:1.2;stroke-dasharray:6 4}
.pn-a{fill:var(--accent-bg);stroke:var(--accent);stroke-width:1.5}
.h{fill:var(--ink);font-family:var(--display);font-weight:600;font-size:19px}
.t{fill:var(--ink);font-family:var(--body);font-size:13.5px}
.tm{fill:var(--muted);font-family:var(--body);font-size:13px}
.tb{fill:var(--ink);font-family:var(--body);font-size:13.5px;font-weight:600}
.c{fill:var(--ink);font-family:var(--mono);font-size:12px}
.cm{fill:var(--muted);font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase}
.ca{fill:var(--accent);font-family:var(--mono);font-size:12px;font-weight:600}
.ta{fill:var(--accent);font-family:var(--body);font-size:13.5px;font-weight:600}
.ar{stroke:var(--muted);stroke-width:1.5;fill:none}
.ar-a{stroke:var(--accent);stroke-width:2;fill:none}
.ah{fill:var(--muted)} .ah-a{fill:var(--accent)}
.grid{stroke:var(--line);stroke-width:1}
.fit{fill:var(--fit-bg);stroke:var(--fit);stroke-width:1.2} .fit-t{fill:var(--fit);font-family:var(--mono);font-size:11.5px;font-weight:600}
.no{fill:var(--no-bg);stroke:var(--no);stroke-width:1.2} .no-t{fill:var(--no);font-family:var(--mono);font-size:11.5px;font-weight:600}
.no-z{fill:var(--no-bg)}
.apx{fill:var(--apx-bg);stroke:var(--apx);stroke-width:1.2} .apx-t{fill:var(--apx);font-family:var(--mono);font-size:11.5px;font-weight:600}
.std{fill:var(--std);stroke:var(--ink);stroke-width:1.2} .opt{fill:var(--opt);stroke:var(--ink);stroke-width:1.2}
.s1{fill:var(--c1)} .s2{fill:var(--c2)} .s3{fill:var(--c3)} .s4{fill:var(--c4)}
.st1{stroke:var(--c1)} .st2{stroke:var(--c2)} .st3{stroke:var(--c3)} .st4{stroke:var(--c4)}
.wt{fill:#ffffff;font-family:var(--mono);font-size:11.5px;font-weight:600}
.dot-on{fill:var(--fit)} .dot-off{fill:none;stroke:var(--muted);stroke-width:1.5}
.dot-need{fill:var(--accent-bg);stroke:var(--accent);stroke-width:2}
.dot-part{fill:var(--apx)}
"""


def tw(s, size=13.5, mono=False):
    """Rough text width in px."""
    return len(s) * (size * 0.6 if mono else size * 0.52)


class Svg:
    def __init__(self, name, w, h, label):
        self.name, self.w, self.h, self.label = name, w, h, label
        self.parts = []
        self.mid = 'ah-' + name

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, cls='t', anchor='start'):
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}" xml:space="preserve">{escape(s)}</text>')

    def rect(self, x, y, w, h, cls='pn', r=6):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" class="{cls}"/>')

    def arrow(self, x1, y1, x2, y2, accent=False):
        c = 'ar-a' if accent else 'ar'
        m = self.mid + ('-a' if accent else '')
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{c}" marker-end="url(#{m})"/>')

    def path_arrow(self, d, accent=False):
        c = 'ar-a' if accent else 'ar'
        m = self.mid + ('-a' if accent else '')
        self.add(f'<path d="{d}" class="{c}" marker-end="url(#{m})"/>')

    def chip(self, x, y, s, cls='pn', tcls='c', h=28, mono=True, size=12):
        w = tw(s, size, mono) + 22
        self.rect(x, y, w, h, cls, 5)
        self.text(x + w / 2, y + h / 2 + 4.2, s, tcls, 'middle')
        return w

    def svg(self, standalone=False):
        defs = (f'<defs><marker id="{self.mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" class="ah"/></marker>'
                f'<marker id="{self.mid}-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" class="ah-a"/></marker></defs>')
        body = '\n'.join(self.parts)
        if standalone:
            tokens = ';'.join(f'--{k}:{v}' for k, v in LIGHT.items()) + ';' + ';'.join(f'--{k}:{v}' for k, v in FONTS.items())
            style = f'<style>svg{{{tokens}}}{SVG_CSS}</style>'
            bg = f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="{LIGHT["bg"]}"/>'
            return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" role="img" aria-label="{escape(self.label)}">'
                    f'{style}{defs}{bg}{body}</svg>\n')
        return (f'<svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.label)}">'
                f'{defs}{body}</svg>')


# ---------------------------------------------------------------- diagrams

def big_picture():
    s = Svg('big-picture', 960, 470, 'Three game modes use five shared building blocks, which read pack data in the existing format.')
    modes = [('Formula mode', 'DTM, F1, touring cars', 'pn'), ('Oval mode', 'stock cars, IndyCar ovals', 'pn'),
             ('Endurance mode (coming)', 'Le Mans, WEC, GT racing', 'pn-d')]
    for i, (t, sub, cls) in enumerate(modes):
        x = 25 + i * 315
        s.rect(x, 12, 280, 62, cls)
        s.text(x + 140, 38, t, 'h', 'middle')
        s.text(x + 140, 60, sub, 'tm', 'middle')
        s.arrow(x + 140, 74, x + 140, 118)
    s.text(182, 112, 'Shared building blocks, built once', 'cm')
    blocks = [('Weekend builder', ['Q1 to Q4, shootouts', 'heats, sprint races', 'grid from last race']),
              ('Rules engine', ['two stops, pits closed', 'in laps 1 to 3', 'option tyre once']),
              ('Entry model', ['crews, guests', 'classes, privateers', 'number, code, livery']),
              ('Content as data', ['"Option" tyre, yellow', 'splitter, rear wing', 'supplier physics']),
              ('Dated world', ['Audi -40 kg', 'from week 23', 'rain in October'])]
    for i, (t, lines) in enumerate(blocks):
        x = 25 + i * 182
        s.rect(x, 124, 172, 118, 'pn-a')
        s.text(x + 14, 152, t, 'h')
        for j, ln in enumerate(lines):
            s.text(x + 14, 178 + j * 20, ln, 't')
    s.arrow(480, 242, 480, 300)
    s.text(492, 278, 'read', 'tm')
    s.text(25, 296, 'Pack data, in the format packs use today', 'cm')
    band = [('regulations.json', ['categories and options', 'voting, scripted_changes', 'an option names a block']),
            ('Named blocks (new)', ['qualifying stages', 'rule rows, points schemes', 'balance rows']),
            ('Presets', ['knockout, session_60 ...', 'rewritten as blocks', 'old packs unchanged'])]
    for i, (t, lines) in enumerate(band):
        x = 25 + i * 315
        s.rect(x, 306, 280, 140)
        s.text(x + 16, 336, t, 'h')
        for j, ln in enumerate(lines):
            s.text(x + 16, 364 + j * 22, ln, 't')
        if i < 2:
            s.arrow(x + 282, 376, x + 313, 376)
    return s


def option_to_block():
    s = Svg('option-to-block', 960, 340, 'A regulation option points to a named block by id; voting still switches options.')
    s.rect(20, 16, 400, 236)
    s.text(38, 44, 'regulations.json (as today)', 'tb')
    left = ['{ "key": "qualifying_format",', '  "default": "dtm_2013",', '  "options": [', '    { "key": "knockout" },',
            '    { "key": "session_60" },', '    { "key": "dtm_2013",', '      "qualifying": "dtm_2013_q4" }', '  ] }']
    for i, ln in enumerate(left):
        s.text(38, 74 + i * 21, ln, 'ca' if '"qualifying":' in ln else 'c')
    s.rect(540, 16, 400, 236)
    s.text(558, 44, 'rulesets.json (new)', 'tb')
    right = ['"dtm_2013_q4": { "stages": [', '  { "type": "knockout",', '    "minutes": 16, "keep": 16 },',
             '  { "type": "knockout", "keep": 10 },', '  { "type": "knockout", "keep": 4 },',
             '  { "type": "single_lap", "cars": 4,', '    "run_order": "reverse" } ] }']
    for i, ln in enumerate(right):
        s.text(558, 74 + i * 21, ln, 'ca' if i == 0 else 'c')
    s.arrow(422, 200, 538, 74, accent=True)
    s.text(492, 174, 'by id', 'ta')
    notes = ['Voting still switches options.', 'Blocks never vote. They are data.',
             'No new field: today\'s behaviour.']
    for i, n in enumerate(notes):
        x = 20 + i * 310
        s.rect(x, 272, 300, 52, 'pn')
        s.text(x + 150, 303, n, 't', 'middle')
    return s


def qualifying():
    s = Svg('qualifying-stages', 960, 470, 'DTM 2012 qualifying as four stages that fill the grid, and other formats built from the same stages.')
    s.text(20, 22, 'Example: DTM 2012, 22 cars', 'cm')
    s.rect(20, 46, 96, 78, 'pn')
    s.text(68, 80, '22 cars', 'tb', 'middle')
    s.text(68, 102, 'entered', 'tm', 'middle')
    stages = [('Q1 · 16 min', 'all 22 run', '16 go on', 'P17 to P22', 's4', 'st4'),
              ('Q2', '16 run', '10 go on', 'P11 to P16', 's3', 'st3'),
              ('Q3', '10 run', '4 go on', 'P5 to P10', 's2', 'st2'),
              ('Q4 · one lap each', 'alone on track', 'reverse order', 'P1 to P4', 's1', 'st1')]
    xs = [140, 320, 500, 680]
    s.arrow(116, 85, 138, 85)
    for i, (t, a, b, out, fill, _st) in enumerate(stages):
        x = xs[i]
        s.rect(x, 40, 160, 90, 'pn-a' if i == 3 else 'pn')
        s.text(x + 14, 66, t, 'tb')
        s.text(x + 14, 90, a, 't')
        s.text(x + 14, 112, b, 't')
        if i < 3:
            s.arrow(x + 160, 85, xs[i + 1] - 2, 85)
        else:
            s.arrow(x + 160, 85, 868, 85)
        s.arrow(x + 80, 130, x + 80, 156)
        s.rect(x + 20, 158, 120, 28, fill, 5)
        s.text(x + 80, 177, out, 'wt', 'middle')
    # grid column
    s.text(905, 32, 'grid', 'cm', 'middle')
    segs = [('P1-4', 4, 's1'), ('P5-10', 6, 's2'), ('P11-16', 6, 's3'), ('P17-22', 6, 's4')]
    y = 40
    for lab, n, fill in segs:
        h = n * 7.5
        s.rect(870, y, 70, h - 2, fill, 3)
        s.text(905, y + h / 2 + 3, lab, 'wt', 'middle')
        y += h
    # other formats
    s.add(f'<line x1="20" y1="222" x2="940" y2="222" class="grid"/>')
    s.text(20, 248, 'Same stages, other formats', 'cm')
    rows = [('DTM 1991', [('timed, 2 sessions', 'pn'), ('top 16 start', 'pn-a'), ('the rest: 50 km qualification race', 'pn'), ('P17 on', 'pn-a')]),
            ('F1 2003', [('single lap', 'pn'), ('sets the run order', 'pn-a'), ('single lap, race fuel', 'pn'), ('grid, parc fermé', 'pn-a')]),
            ('DTM 2015 on', [('timed, 20 min', 'pn'), ('race 1 grid', 'pn-a'), ('timed, 20 min', 'pn'), ('race 2 grid', 'pn-a')]),
            ('F1 2021 sprint', [('timed', 'pn'), ('sprint grid', 'pn-a'), ('sprint result', 'pn'), ('Grand Prix grid', 'pn-a')]),
            ('F1 2016', [('slowest car out every 90 s', 'pn'), ('grid', 'pn-a')])]
    for r, (lab, chips) in enumerate(rows):
        y = 262 + r * 40
        s.text(20, y + 19, lab, 'tb')
        x = 160
        for k, (c, cls) in enumerate(chips):
            w = s.chip(x, y, c, cls, 'c')
            x += w
            if k < len(chips) - 1:
                gap = 30 if k % 2 == 0 else 46
                if k % 2 == 0:
                    s.arrow(x + 3, y + 14, x + gap - 3, y + 14)
                else:
                    s.text(x + gap / 2, y + 19, '|', 'tm', 'middle')
                x += gap
    return s


def race_rules():
    s = Svg('race-rules', 960, 440, 'A DTM 2013 race: two legal stops outside the closed laps, and a plan that breaks the rules.')
    x0, x1, n = 150, 930, 40
    lw = (x1 - x0) / n

    def lx(lap):  # left edge of a lap (1-based)
        return x0 + (lap - 1) * lw

    s.text(20, 22, 'Example: DTM 2013 rules, a 40-lap race', 'cm')
    s.rect(660, 9, 22, 14, 'std', 3)
    s.text(688, 21, 'standard', 'tm')
    s.rect(760, 9, 22, 14, 'opt', 3)
    s.text(788, 21, 'option', 'tm')
    s.rect(850, 9, 22, 14, 'no-z', 3)
    s.text(878, 21, 'closed', 'tm')
    # closed zones
    s.rect(lx(1), 44, 3 * lw, 200, 'no-z', 0)
    s.rect(lx(38), 44, 3 * lw, 200, 'no-z', 0)
    for lap in (1, 10, 20, 30, 40):
        s.text(lx(lap) + lw / 2, 60, f'lap {lap}' if lap == 1 else str(lap), 'tm', 'middle')
    s.text(lx(1) + 1.5 * lw, 238, 'laps 1-3', 'no-t', 'middle')
    s.text(lx(38) + 1.5 * lw, 238, 'laps 38-40', 'no-t', 'middle')

    def stint(y, a, b, cls):
        s.rect(lx(a), y, (b - a + 1) * lw, 26, cls, 3)

    def stop(y, lap, label, bad=False):
        x = lx(lap) + lw
        cls = 'no' if bad else 'pn-a'
        s.add(f'<line x1="{x:.1f}" y1="{y - 18}" x2="{x:.1f}" y2="{y + 32}" class="{"ar" if not bad else "ar"}" stroke-dasharray="3 3"/>')
        w = tw(label, 11.5, True) + 16
        s.rect(x - w / 2, y - 40, w, 22, cls, 4)
        s.text(x, y - 25, label, 'no-t' if bad else 'ca', 'middle')

    ya = 112
    s.text(20, ya + 12, 'Car A', 'tb')
    s.text(20, ya + 30, 'legal plan', 'tm')
    stint(ya, 1, 14, 'std'); stint(ya, 15, 27, 'opt'); stint(ya, 28, 40, 'std')
    stop(ya, 14, 'stop 1, lap 14'); stop(ya, 27, 'stop 2, lap 27')
    yb = 196
    s.text(20, yb + 12, 'Car B', 'tb')
    s.text(20, yb + 30, 'breaks a rule', 'tm')
    stint(yb, 1, 20, 'std'); stint(yb, 21, 38, 'opt'); stint(yb, 39, 40, 'std')
    stop(yb, 20, 'stop 1, lap 20')
    stop(yb, 38, 'lap 38: no count', bad=True)
    # rule checks
    s.add('<line x1="20" y1="262" x2="940" y2="262" class="grid"/>')
    s.text(20, 288, 'Rule rows (checked after the race)', 'cm')
    s.text(470, 288, 'Car A', 'cm')
    s.text(720, 288, 'Car B', 'cm')
    rows = [('mandatory_stops: 2', ('pass', '2 stops'), ('fail', '1 stop counts')),
            ('no_stop_first_laps: 3', ('pass', 'none in laps 1-3'), ('pass', 'none in laps 1-3')),
            ('no_stop_last_laps: 3', ('pass', 'none in laps 38-40'), ('fail', 'stop on lap 38')),
            ('must_use: option', ('pass', 'laps 15-27'), ('pass', 'laps 21-38'))]
    for i, (rule, a, b) in enumerate(rows):
        y = 300 + i * 30
        s.text(20, y + 17, rule, 'c')
        for x, (res, txt) in ((470, a), (720, b)):
            s.rect(x, y + 2, 46, 22, 'fit' if res == 'pass' else 'no', 4)
            s.text(x + 23, y + 17.5, res, 'fit-t' if res == 'pass' else 'no-t', 'middle')
            s.text(x + 56, y + 18, txt, 't')
    s.text(470, 432, 'classified', 'ta')
    s.text(720, 432, 'penalty', 'no-t')
    return s


def scopes():
    s = Svg('scopes', 960, 330, 'One lookup for every rule: the most specific scope with a value wins.')
    cols = ['Season', 'Session', 'Race', 'Track', 'Make or class', 'Entry']
    cx = [230, 330, 430, 530, 630, 730]
    s.text(20, 46, 'Asked for', 'cm')
    for c, x in zip(cols, cx):
        s.text(x + 45, 46, c, 'cm', 'middle')
    s.text(895, 46, 'Answer', 'cm', 'middle')
    s.arrow(230, 20, 820, 20)
    s.text(525, 14, 'more specific wins', 'tm', 'middle')
    rows = [('drs', 'DTM 2013, qualifying', {0: 'on', 1: 'off'}, 1, 'off'),
            ('mandatory_stops', 'DTM 2025, Sunday race', {0: '1', 2: 'Sunday: 2'}, 2, '2'),
            ('min_mass_kg', 'DTM 1991, an Audi', {0: '980', 4: 'Audi: 1,290'}, 4, '1,290')]
    for r, (key, ctx, vals, win, ans) in enumerate(rows):
        y = 62 + r * 74
        s.text(20, y + 26, key, 'ca')
        s.text(20, y + 46, ctx, 'tm')
        for i, x in enumerate(cx):
            if i in vals:
                s.rect(x, y + 8, 90, 44, 'pn-a' if i == win else 'pn', 5)
                s.text(x + 45, y + 35, vals[i], 'tb' if i == win else 'tm', 'middle')
            else:
                s.add(f'<circle cx="{x + 45}" cy="{y + 30}" r="3" class="ah"/>')
        s.arrow(cx[win] + 92, y + 30, 848, y + 30, accent=True)
        s.rect(850, y + 8, 90, 44, 'fit', 5)
        s.text(895, y + 35, ans, 'fit-t', 'middle')
    s.text(20, 312, 'One function serves every feature: rule(key, season, session, race, track, make, entry).', 't')
    return s


def entry_model():
    s = Svg('entry-model', 960, 420, 'An entry with tags; points, qualifying, balance, screens and pit stops all read the same entry.')
    # cards
    s.rect(325, 20, 310, 196, 'pn-a')
    s.text(343, 48, 'Entry (DTM 1991 example)', 'tb')
    card1 = [('number', '8'), ('team', 'AMG'), ('car', 'Mercedes 190E'), ('drivers', 'Klaus Ludwig'),
             ('rounds', 'all'), ('livery', 'König Pilsener black'), ('tags', 'works')]
    for i, (k, v) in enumerate(card1):
        s.text(343, 74 + i * 20, k, 'cm')
        s.text(420, 74 + i * 20, v, 'c')
    s.rect(325, 232, 310, 170, 'pn-d')
    s.text(343, 260, 'Entry (endurance example)', 'tb')
    card2 = [('number', '23'), ('drivers', 'A, B and C'), ('class', 'GT3'), ('tags', 'pro_am'),
             ('rules', 'min drive time each'), ('rounds', 'Le Mans only')]
    for i, (k, v) in enumerate(card2):
        s.text(343, 286 + i * 20, k, 'cm')
        s.text(420, 286 + i * 20, v, 'c')
    left = [('Points', 'who scores, which title', 'guests score nothing'),
            ('Qualifying', 'groups and classes', 'Hyperpole per class'),
            ('Balance', 'ballast and BoP', 'by make or class')]
    right = [('Screens', 'car image, portrait', 'timing code'),
             ('Pit stops', 'driver change', 'as a stop service'),
             ('Junior seats', 'who may take a seat', 'in feeder series')]
    for i, (t, a, b) in enumerate(left):
        y = 36 + i * 128
        s.rect(20, y, 230, 92)
        s.text(36, y + 28, t, 'h')
        s.text(36, y + 52, a, 't')
        s.text(36, y + 72, b, 'tm')
        s.arrow(323, 210, 252, y + 46)
    for i, (t, a, b) in enumerate(right):
        y = 36 + i * 128
        s.rect(710, y, 230, 92)
        s.text(726, y + 28, t, 'h')
        s.text(726, y + 52, a, 't')
        s.text(726, y + 72, b, 'tm')
        s.arrow(637, 210, 708, y + 46)
    return s


def modes():
    s = Svg('modes', 960, 330, 'Features that exist in one game mode today, and the shared setting each could become.')
    heads = [('Formula', 360), ('Oval', 470), ('Endurance', 580)]
    s.text(20, 30, 'Feature', 'cm')
    for t, x in heads:
        s.text(x, 30, t, 'cm', 'middle')
    s.text(660, 30, 'One shared setting', 'cm')
    rows = [('Rolling start', 'off', 'on', 'need', 'start_procedure'),
            ('4 to 6 cars per team', 'off', 'on', 'need', 'team_entry_cap'),
            ('Grid size as a rule', 'part', 'on', 'need', 'grid_limit'),
            ('Points for part of a race', 'off', 'on', 'need', 'stage_racing'),
            ('Playoffs', 'off', 'on', 'off', 'championship_format'),
            ('Red flags', 'on', 'off', 'need', 'red_flags')]
    for i, (t, f, o, e, key) in enumerate(rows):
        y = 48 + i * 40
        s.add(f'<line x1="20" y1="{y + 36}" x2="940" y2="{y + 36}" class="grid"/>')
        s.text(20, y + 23, t, 't')
        for st, (_h, x) in zip((f, o, e), heads):
            cls = {'on': 'dot-on', 'off': 'dot-off', 'need': 'dot-need', 'part': 'dot-part'}[st]
            s.add(f'<circle cx="{x}" cy="{y + 18}" r="8" class="{cls}"/>')
        s.text(660, y + 23, key, 'ca')
    leg = [('dot-on', 'has it today'), ('dot-part', 'partly (a constant)'), ('dot-off', 'not today'), ('dot-need', 'endurance will need it')]
    x = 20
    for cls, t in leg:
        s.add(f'<circle cx="{x + 8}" cy="{304}" r="7" class="{cls}"/>')
        s.text(x + 22, 309, t, 'tm')
        x += tw(t, 13) + 60
    return s


def bundles():
    s = Svg('bundles', 960, 470, 'Ten delivery bundles in three groups: quick wins, the core, and what builds on the core.')
    cols = [('Quick wins', 20), ('The core', 340), ('Builds on the core', 660)]
    for t, x in cols:
        s.text(x, 24, t, 'cm')
    items = {
        20: [('0', 'Docs only', 'D3, E4, E5, E10, E12', 'no code, answers only', False),
             ('1', 'Oval rules for all', 'A3, C1, B3', 'rolling start, 6 cars', True),
             ('8', 'Pack infrastructure', 'E1, E2, E3', 'overlays, validation', False)],
        340: [('2', 'Rules engine', 'B5 to B12', 'two stops, closed laps', True),
              ('3', 'Weekend builder', 'A1 to A6, C7', 'Q4, heats, sprint', True),
              ('4', 'Entry model', 'C1 to C8, B4, B9, E4', 'crews, guests, classes', True)],
        660: [('5', 'Content as data', 'D1, D8, D9, E13', 'Option tyre, splitter', False),
              ('6', 'Dated world', 'A4, B1, B2, C4, D4, D7', 'Audi -40 kg in week 23', True),
              ('7', 'Closed-car physics', 'D2, D3, D5, D6', '480 hp, 1,110 kg', True),
              ('9', 'Sound', 'E8, E9, E11, E14', 'a BMW sounds like one', False)],
    }
    for x, lst in items.items():
        for i, (num, t, ids, ex, endu) in enumerate(lst):
            y = 36 + i * 92
            s.rect(x, y, 280, 80, 'pn-a' if x == 340 else 'pn')
            s.text(x + 16, y + 28, f'{num} · {t}', 'h')
            s.text(x + 16, y + 50, ids, 'c')
            s.text(x + 16, y + 70, ex, 'tm')
            if endu:
                s.chip(x + 280 - 96, y + 10, 'endurance', 'dot-need', 'ca', h=22, size=11)
    s.arrow(302, 160, 336, 160, accent=True)
    s.arrow(622, 160, 656, 160, accent=True)
    s.text(20, 440, 'Quick wins cost little. The core makes most later requests a new row instead of new code.', 't')
    s.text(660, 410, 'endurance tag: the endurance mode', 'tm')
    s.text(660, 428, 'needs this bundle anyway', 'tm')
    return s


DIAGRAMS = [
    ('big-picture', big_picture, 'The idea in one picture',
     'Build each racing rule once, as data. Every game mode uses the same blocks, and packs keep today\'s file format.',
     ['Formula, oval and the coming endurance mode share five building blocks.',
      'The blocks read the same regulation files packs use today, plus named blocks for bigger structures.',
      'Today\'s options become presets, so existing packs don\'t change.']),
    ('option-to-block', option_to_block, 'How it fits today\'s options',
     'A regulation option stays an option. It just names a block, the way the oval mode already keeps stage settings in config.json.',
     ['The governing body still votes between options, and scripted_changes still switch them.',
      'The block holds the detail: here the four stages of DTM qualifying.',
      'A pack that adds no new fields plays exactly as before.']),
    ('qualifying-stages', qualifying, 'Qualifying as stages',
     'Every qualifying format we found in DTM and F1 is a short list of stages. Each stage takes cars in and sends some on.',
     ['DTM 2012 needs one more stage than the game has: a single-lap Q4.',
      'The same few stage types also build qualification races, one-lap qualifying, a session per race and sprint grids.',
      'Presets mean most packs pick a format by name and never write a stage list.']),
    ('race-rules', race_rules, 'Race rules as rows',
     'Each rule is one row. The game checks the rows after the race, and the AI reads the same rows to plan a legal race.',
     ['DTM 2013: two stops, no stop in the first or last 3 laps, the option tyre used once.',
      'Car B stops on lap 38. The pits are closed for counting stops then, so it has only one stop and gets a penalty.',
      'Monaco 2025 is three rows too: two stops, three sets, two compounds.']),
    ('scopes', scopes, 'One lookup for every rule',
     'Any value can be set for the whole season and overridden for a session, a race, a track, a make or class, or one entry.',
     ['DRS on in the race but off in qualifying (DTM 2013).',
      'One stop on Saturday, two on Sunday (DTM 2025).',
      'A minimum weight per make (DTM 1991). Endurance BoP per class uses the same lookup.']),
    ('entry-model', entry_model, 'The entry as the unit',
     'An entry is the car with its number, drivers, livery and tags. Many features read the same entry, so it is built once.',
     ['Tags decide who scores, which title they score in, and which balance rules apply.',
      'A one-driver entry behaves like a car today. Crews of two to four drivers are the endurance case.',
      'Per-entry liveries and timing codes come with it.']),
    ('modes', modes, 'One feature, every mode',
     'Several things we asked for already exist in the oval mode. Shared settings give them to every mode, endurance included.',
     ['Rolling starts, big entries, stage points and playoffs are already in the oval code.',
      'Red flags are already in the formula code.',
      'Each becomes one setting any pack can turn on.']),
    ('bundles', bundles, 'Ten delivery bundles',
     'The requests grouped by the work the developer would do. Quick wins first, then the core that makes everything else cheap.',
     ['Bundles 0 and 1 cost little and help at once.',
      'Bundles 2 to 4 are the core. Most later requests become new rows instead of new code.',
      'Six bundles are work the endurance mode needs anyway.']),
]


PAGE_CSS = """
:root{
  /* Layout: one column of numbered figures, each a picture with three short takeaways. Same tokens as docs/dtm_rules.html. */
%LIGHT%
  --display:"Barlow Condensed","Arial Narrow",Arial,sans-serif;
  --body:"Source Sans 3","Segoe UI",system-ui,sans-serif;
  --mono:"JetBrains Mono",Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){%DARK% color-scheme:dark}}
:root[data-theme="dark"]{%DARK% color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.5}
.wrap{max-width:1040px;margin:0 auto;padding-block:32px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:44px}
h1,h2{font-family:var(--display);text-wrap:balance;margin:0;letter-spacing:.01em}
h1{font-size:clamp(36px,6vw,56px);font-weight:700;line-height:1}
h2{font-size:28px;font-weight:600;display:flex;gap:12px;align-items:baseline}
h2 .n{font-family:var(--mono);font-size:13px;color:var(--accent);font-weight:600}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.lede{max-width:66ch;color:var(--muted);margin:12px 0 0;font-size:17px}
header{display:grid;gap:4px;border-bottom:2px solid var(--ink);padding-bottom:20px}
section{display:grid;gap:12px}
section p.goal{margin:0;max-width:70ch}
.fig{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px}
.fig svg{display:block;width:100%;min-width:760px;height:auto}
ul.take{margin:0;padding-left:20px;display:grid;gap:4px;max-width:75ch;color:var(--muted)}
ul.take li::marker{color:var(--accent)}
footer{color:var(--muted);font-size:14px;border-top:1px solid var(--line);padding-top:16px;display:grid;gap:6px}
code{font-family:var(--mono);font-size:.9em}
"""


def main():
    os.makedirs(IMG, exist_ok=True)
    sections = []
    for i, (name, fn, title, goal, take) in enumerate(DIAGRAMS, 1):
        svg = fn()
        with open(os.path.join(IMG, name + '.svg'), 'w', encoding='utf-8') as f:
            f.write(svg.svg(standalone=True))
        lis = ''.join(f'<li>{escape(t)}</li>' for t in take)
        sections.append(f'<section id="{name}"><h2><span class="n">{i:02d}</span>{escape(title)}</h2>'
                        f'<p class="goal">{escape(goal)}</p><div class="fig">{svg.svg()}</div><ul class="take">{lis}</ul></section>')
    light = '\n'.join(f'  --{k}:{v};' for k, v in LIGHT.items())
    dark = ''.join(f'--{k}:{v};' for k, v in DARK.items())
    css = PAGE_CSS.replace('%LIGHT%', light).replace('%DARK%', dark)
    html = f"""<title>Racing Rules as Data</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{css}{SVG_CSS}</style>
<div class="wrap">
<header>
<div class="eyebrow">Team Principal · feature requests from the DTM season packs</div>
<h1>Racing rules as data</h1>
<p class="lede">Our wish list has about fifty gaps. Most of them are parts of a few systems. These pictures show the idea with real examples from DTM and Formula 1: build each racing rule once, as data, and let every series and every game mode use it.</p>
</header>
{''.join(sections)}
<footer>
<div>Based on game version 0.99.6 (beta). DTM rules come from our season research; F1 and other-series facts are from memory and still being sourced.</div>
<div>Details for each part are in the wish list (<code>docs/DEVELOPER_WISHLIST.md</code>) and the feature packages (<code>docs/packages/</code>) of the team-principal-mods repository.</div>
</footer>
</div>
"""
    with open(PAGE, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', PAGE, 'and', len(DIAGRAMS), 'images in', IMG)


if __name__ == '__main__':
    main()
