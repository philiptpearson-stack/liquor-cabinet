"""Character sheet for Philip the bartender: python3 bartender_sheet.py out/bartender.png"""
import sys, pathlib, subprocess, json
from art import *
from shelves import plain_bottle, decanter
from bartender import bartender, PLAID

REPO = pathlib.Path('/home/claude/liquor-cabinet')

# ---- 1. Welcome to my bar
wall = wash('<rect x="0" y="0" width="400" height="236" fill="#6f5443"/><rect x="40" y="14" width="320" height="136" fill="#cfe0dc" opacity=".55"/>')
shelf = lambda y: wash(f'<rect x="40" y="{y}" width="320" height="4" fill="#bfe3dc" opacity=".9"/>') + lines(f'<path d="M40 {y} H360 M40 {y + 4} H360" stroke="#6aa59a" stroke-width="1.6"/>', boil=False)
colors = ['#c98a3c', '#a0522d', '#7f9a6c', '#e6d3bd', '#b9792c', '#c0583c', '#e7f1fb', '#8a6a3c', '#c98a3c', '#7f9a6c', '#a0522d', '#d8c3a5', '#b9792c', '#c0583c']
top = ''.join(plain_bottle(52 + i * 22.5, 58, (34, 40, 30, 38, 42, 32, 36)[i % 7], colors[i % 14]) for i in range(14))
mid = ''.join(plain_bottle(56 + i * 24, 104, (30, 36, 40, 32, 38)[i % 5], colors[(i + 5) % 14]) for i in range(13))
ladder = lines('<path d="M330 6 L352 150 M346 4 L368 150" stroke="#9b7663" stroke-width="3.4"/>' + ''.join(f'<path d="M{333 + k * 3.1} {24 + k * 20} h16" stroke="#9b7663" stroke-width="2.6"/>' for k in range(6)), boil=False)
counter = ('<rect x="0" y="146" width="400" height="90" fill="#6e4b39"/>' + wash('<rect x="0" y="146" width="400" height="12" fill="#5a3e2e"/><rect x="0" y="158" width="400" height="78" fill="#7a5340"/>')
           + lines('<path d="M0 146 H400 M0 158 H400"/>' + ''.join(f'<rect x="{x}" y="170" width="70" height="52" rx="2" stroke-width="1.8"/>' for x in (20, 116, 212, 308)), boil=False, width=2.2))
glass = (wash('<path d="M268 128 L292 128 L290 146 L270 146Z" fill="#e7f1fb" opacity=".7"/><path d="M269.4 134 L290.6 134 L290 146 L270 146Z" fill="#c98a3c"/>'
              '<rect x="273" y="130" width="12" height="11" rx="1.5" fill="#f4fbff" opacity=".85"/><path d="M286 126 q6 4 2 12 q-3 -5 -2 -12Z" fill="#e89a3c"/>')
         + lines('<path d="M268 128 L292 128 L290 146 L270 146Z" stroke-width="2"/><rect x="273" y="130" width="12" height="11" rx="1.5" stroke-width="1.4"/><path d="M286 126 q6 4 2 12 q-3 -5 -2 -12Z" stroke-width="1.4"/>', boil=False))
lean = bartender(eyes='dot', arm_l=[(-23, -110), (-36, -84), (-33, -58)], arm_r=[(23, -110), (36, -84), (33, -58)])
welcome = wall + shelf(58) + top + shelf(104) + mid + ladder + place(lean, 200, 206) + counter + glass

# ---- 2. Three looks
hello = bartender(eyes='dot', arm_l=[(-23, -110), (-42, -102), (-56, -114)], arm_r=[(23, -110), (42, -102), (56, -114)])
mixing = (wash('<path d="M2 -104 L20 -104 L18 -78 L4 -78Z" fill="#e7f1fb" opacity=".75"/><path d="M3 -96 L19 -96 L18 -78 L4 -78Z" fill="#c98a3c"/>')
          + lines('<path d="M2 -104 L20 -104 L18 -78 L4 -78Z" stroke-width="1.8"/><path d="M-1 -116 L9 -84" stroke="#8a8f96" stroke-width="1.8"/><circle cx="-1.5" cy="-117.5" r="2" fill="#8a8f96" stroke="#8a8f96"/>', boil=False))
st = bartender(mood='smug', eyes='wink', parts=True, arm_l=[(-23, -110), (-28, -92), (-2, -112)], arm_r=[(23, -110), (32, -90), (17, -84)])
stir = st['body'] + st['head'] + mixing + st['left'] + st['right']
thumb = wash(f'<rect x="-15.8" y="-112" width="5.6" height="11" rx="2.8" fill="{SKIN}"/>') + lines('<rect x="-15.8" y="-112" width="5.6" height="11" rx="2.8" stroke-width="1.8"/>')
g = bartender(hat='bat', parts=True, arm_l=[(-23, -110), (-38, -92), (-13, -98)], arm_r=[(23, -110), (40, -90), (25, -72)])
goof = g['body'] + g['head'] + g['left'] + thumb + g['right']   # thumbs-up arm crosses in front of him
looks = wash('<rect x="0" y="0" width="400" height="236" fill="#f3e6d4"/>') + ground(224) + place(hello, 72, 224, 1.05) + place(stir, 196, 224, 1.05) + place(goof, 316, 224, 1.05)

panels = {'welcome': svg(welcome, 'Philip behind his bar'), 'looks': svg(looks, 'Philip three ways')}
kit = (REPO / 'src/kit/kit.css').read_text()
defs = (REPO / 'src/kit/defs.svg').read_text().replace('  </defs>', PLAID + '\n  </defs>')
figs = ''.join(f'<figure class="fig on" id="{n}" style="width:400px;margin:8px"><div class="sheet">{s}</div></figure>' for n, s in panels.items())
out = pathlib.Path('out'); out.mkdir(exist_ok=True)
(out / '_bt.html').write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{kit}\nbody{{background:#ddd;margin:0}}</style></head><body>{defs}{figs}</body></html>')
js = """const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
 const pg = await b.newPage({ viewport: { width: 416, height: 600 }, deviceScaleFactor: 2.5 });
 await pg.route(/fonts\\.g/, r => r.abort());
 await pg.goto('file://' + %s); await pg.waitForTimeout(300);
 for (const n of %s) await pg.locator('#' + n).screenshot({ path: 'out/bt_' + n + '.png' });
 await b.close(); })();""" % (json.dumps(str((out / '_bt.html').resolve())), json.dumps(list(panels)))
(out / '_bt.js').write_text(js)
subprocess.run('NODE_PATH=$(npm root -g) node out/_bt.js', shell=True, check=True)
from PIL import Image
ims = [Image.open(f'out/bt_{n}.png') for n in panels]
S = Image.new('RGB', (ims[0].width, sum(i.height for i in ims) + 16), '#f7efe1')
y = 0
for im in ims:
    S.paste(im, (0, y)); y += im.height + 16
S.save(sys.argv[1]); print(S.size)
