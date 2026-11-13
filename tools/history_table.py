"""Render the table of a docs/history/*.md file as a PNG for Discord.

Reads the first Markdown table under '## Table' and writes
docs/packages/img/png/<file stem>.png. '(?)' marks unconfirmed details and
is shown in amber. Uses headless Edge like tools/discord_posts.py.

Usage: python -I tools/history_table.py docs/history/f1-qualifying.md
"""
import os
import re
import subprocess
import sys
import time
from html import escape

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG = os.path.join(ROOT, 'docs', 'packages', 'img', 'png')
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
WIDTH = 1600

CSS = """
body{margin:0;background:#f8f9fa;font:15px/1.4 'Segoe UI',sans-serif;color:#212529}
.wrap{padding:28px 32px}
.kicker{font:14px Consolas,monospace;letter-spacing:.08em;color:#646a73;margin-bottom:6px}
h1{font-size:28px;margin:0 0 18px}
table{border-collapse:collapse;width:100%;background:#fff}
th{font:13px Consolas,monospace;letter-spacing:.06em;text-transform:uppercase;color:#646a73;
   text-align:left;padding:10px 12px;border-bottom:2px solid #ced4da;background:#f1f3f5}
td{padding:9px 12px;border-bottom:1px solid #e1e5e9;vertical-align:top}
td:first-child{font-weight:600;white-space:nowrap}
td:nth-child(2){font-weight:600;color:#1d4ed8}
tr:nth-child(even) td{background:#fafbfc}
code{font:13px Consolas,monospace}
.q{color:#b45309;font-weight:600}
.foot{margin-top:12px;color:#646a73;font-size:13px}
"""


def inline(text):
    text = escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    return text.replace('(?)', '<span class="q">(?)</span>')


def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    title = next(l[2:].strip() for l in lines if l.startswith('# '))
    start = lines.index('## Table')
    rows = []
    for line in lines[start + 1:]:
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if not all(set(c) <= set('-: ') for c in cells):
                rows.append(cells)
        elif rows:
            break
    return title, rows[0], rows[1:]


def render(path):
    title, head, body = parse(path)
    stem = os.path.splitext(os.path.basename(path))[0]
    html = (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="wrap">'
            f'<div class="kicker">RULES HISTORY</div><h1>{escape(title)}</h1><table><tr>'
            + ''.join(f'<th>{escape(h)}</th>' for h in head) + '</tr>'
            + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body)
            + '</table><div class="foot"><span class="q">(?)</span> not confirmed by the sources we read. '
            'Sources: Wikipedia race weekend, 107% rule, tyres and season articles.</div></div></body></html>')
    os.makedirs(PNG, exist_ok=True)
    tmp = os.path.join(PNG, stem + '.tmp.html')
    out = os.path.join(PNG, stem + '.png')
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(html)
    if os.path.exists(out):
        os.remove(out)
    profile = os.path.join(os.environ.get('TEMP', PNG), 'tp-edge-headless-' + stem)
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                    f'--user-data-dir={profile}', f'--window-size={WIDTH},6000', f'--screenshot={out}',
                    'file:///' + tmp.replace('\\', '/')],
                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    for _ in range(60):
        if os.path.exists(out) and os.path.getsize(out) > 0:
            break
        time.sleep(0.25)
    os.remove(tmp)
    # Trim the empty page below the content.
    im = Image.open(out).convert('RGB')
    bg = im.getpixel((5, im.height - 5))
    px = im.load()
    bottom = im.height - 1
    while bottom > 0 and all(px[x, bottom] == bg for x in range(0, im.width, 7)):
        bottom -= 1
    im.crop((0, 0, im.width, min(im.height, bottom + 28))).save(out)
    print(out, im.width, bottom + 28)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        render(p)
