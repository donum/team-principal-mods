"""Build the Discord version of the feature request.

Reads docs/packages/discord_posts.md (posts split by '=== post | <name> | <images>'),
exports the named diagrams as PNG (Discord doesn't preview SVG) and writes
docs/packages/discord.html: every post with its length, a copy button and the
pictures to attach.

Usage: python -I tools/discord_posts.py [--no-png]
"""
import os
import subprocess
import sys
import time
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import package_diagrams as pd  # noqa: E402

ROOT = pd.ROOT
SRC = os.path.join(ROOT, 'docs', 'packages', 'discord_posts.md')
PAGE = os.path.join(ROOT, 'docs', 'packages', 'discord.html')
PNG = os.path.join(pd.IMG, 'png')
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
LIMIT = 2000


def parse():
    posts = []
    for line in open(SRC, encoding='utf-8').read().split('\n'):
        if line.startswith('=== post'):
            _, name, imgs = [p.strip() for p in line.split('|')]
            posts.append({'name': name, 'images': [i.strip() for i in imgs.split(',') if i.strip()], 'lines': []})
        elif posts:
            posts[-1]['lines'].append(line)
    for p in posts:
        p['text'] = '\n'.join(p['lines']).strip('\n')
    return posts


def export_png(diagrams):
    os.makedirs(PNG, exist_ok=True)
    for name, svg in diagrams.items():
        html = os.path.join(PNG, name + '.tmp.html')
        with open(html, 'w', encoding='utf-8') as f:
            f.write('<html><body style="margin:0">' + svg.svg(standalone=True) + '</body></html>')
        out = os.path.join(PNG, name + '.png')
        # One profile per image: a second launch on a busy profile can hand off and write nothing.
        profile = os.path.join(os.environ.get('TEMP', PNG), 'tp-edge-headless-' + name)
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
                        f'--user-data-dir={profile}',
                        f'--window-size={svg.w},{svg.h}', f'--screenshot={out}', 'file:///' + html.replace('\\', '/')],
                       stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        # Edge can finish writing after the launcher exits.
        for _ in range(60):
            if os.path.exists(out) and os.path.getsize(out) > 0:
                break
            time.sleep(0.25)
        else:
            print('no PNG written for', name)
        os.remove(html)


CSS = """
.post{background:var(--panel);border:1px solid var(--line);border-radius:8px;display:grid;gap:0;overflow:hidden}
.post .bar{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;padding:10px 14px;border-bottom:1px solid var(--line)}
.post .bar b{font-family:var(--display);font-size:22px;font-weight:600}
.post .bar .n{font-family:var(--mono);font-size:12px;color:var(--accent);font-weight:600}
.count{font-family:var(--mono);font-size:12px;color:var(--fit);background:var(--fit-bg);padding:2px 7px;border-radius:3px}
.count.over{color:var(--no);background:var(--no-bg)}
.copy{margin-left:auto;font:600 14px var(--body);background:var(--accent);color:var(--panel);border:0;border-radius:4px;padding:6px 14px;cursor:pointer}
.copy:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.post pre{margin:0;padding:14px;white-space:pre-wrap;word-break:break-word;font-family:var(--mono);font-size:13px;line-height:1.55;max-height:420px;overflow:auto}
.att{border-top:1px solid var(--line);padding:12px 14px;display:grid;gap:10px}
.att .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.att .fig{border:1px solid var(--line);border-radius:6px;padding:8px;overflow-x:auto}
.att svg{display:block;width:100%;min-width:640px;height:auto}
.how{max-width:72ch;color:var(--muted);margin:0;display:grid;gap:6px}
"""

JS = """
document.querySelectorAll('.copy').forEach(function(b){
  b.addEventListener('click', function(){
    var pre = document.getElementById(b.dataset.for);
    var done = function(){ b.textContent = 'Copied'; setTimeout(function(){ b.textContent = 'Copy post'; }, 1600); };
    var fallback = function(){ var r = document.createRange(); r.selectNodeContents(pre); var s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = 'Selected, press Ctrl+C'; };
    try { navigator.clipboard.writeText(pre.textContent).then(done, fallback); } catch (e) { fallback(); }
  });
});
"""


def main():
    posts = parse()
    diagrams = {name: fn() for name, fn, *_ in pd.DIAGRAMS}
    used = {i for p in posts for i in p['images']}
    if '--no-png' not in sys.argv:
        export_png({k: v for k, v in diagrams.items() if k in used})
    cards = []
    for i, p in enumerate(posts, 1):
        n = len(p['text'])
        over = ' over' if n > LIMIT else ''
        att = ''
        if p['images']:
            figs = ''.join(f'<div class="fig">{diagrams[k].svg()}</div>' for k in p['images'])
            files = ', '.join(f'docs/packages/img/png/{k}.png' for k in p['images'])
            att = f'<div class="att"><div class="lbl">Attach: {escape(files)}</div>{figs}</div>'
        cards.append(f'<article class="post"><div class="bar"><span class="n">POST {i} OF {len(posts)}</span><b>{escape(p["name"])}</b>'
                     f'<span class="count{over}">{n:,} / {LIMIT:,}</span>'
                     f'<button class="copy" type="button" data-for="p{i}">Copy post</button></div>'
                     f'<pre id="p{i}">{escape(p["text"])}</pre>{att}</article>')
        print(f'post {i} {p["name"]}: {n} chars')
    light = '\n'.join(f'  --{k}:{v};' for k, v in pd.LIGHT.items())
    dark = ''.join(f'--{k}:{v};' for k, v in pd.DARK.items())
    css = pd.PAGE_CSS.replace('%LIGHT%', light).replace('%DARK%', dark)
    html = f"""<title>DTM Requests for Discord</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{css}{pd.SVG_CSS}{CSS}</style>
<div class="wrap">
<header>
<div class="eyebrow">Discord thread · {len(posts)} posts</div>
<h1>Racing rules as data</h1>
<p class="lede">The whole feature request, written for a Discord thread. Post them in order, one message each, with the pictures attached.</p>
</header>
<div class="how">
<div>Each post stays under Discord's 2,000-character limit. Copy one, paste it as a message, then attach the PNG files named under it.</div>
<div>Discord doesn't preview SVG images, so the PNG versions are in <code>docs/packages/img/png/</code>.</div>
</div>
{''.join(cards)}
<footer><div>Source: <code>docs/packages/discord_posts.md</code>. Edit it and rerun <code>python -I tools/discord_posts.py</code>.</div></footer>
</div>
<script>{JS}</script>
"""
    with open(PAGE, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', PAGE)


if __name__ == '__main__':
    main()
