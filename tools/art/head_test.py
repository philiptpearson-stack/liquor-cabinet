"""Close-up of a few bartender heads side by side: python3 head_test.py out/heads.png"""
import sys, pathlib, subprocess, json, importlib
from art import *
import bartender as B
REPO = pathlib.Path('/home/claude/liquor-cabinet')
variants = [dict(eyes='dot'), dict(eyes='dot', beard=None), dict(mood='smug', eyes='wink'), dict(mood='smug', eyes='wink', beard=None), dict(hat='bat')]
inner = ''.join(place(B.bartender(**v, arm_l=[(-23, -110), (-29, -86), (-14, -70)]), 40 + i * 80, 236, 1.25) for i, v in enumerate(variants))
s = f'<svg viewBox="0 10 400 140" role="img" aria-label="heads">{inner}</svg>'
kit = (REPO / 'src/kit/kit.css').read_text()
defs = (REPO / 'src/kit/defs.svg').read_text().replace('  </defs>', B.PLAID + '\n  </defs>')
out = pathlib.Path('out'); out.mkdir(exist_ok=True)
(out / '_h.html').write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{kit}\nbody{{background:#f3e6d4;margin:0}}.still *{{animation:none}}</style></head><body class="still">{defs}<figure class="fig on" id="h" style="width:1000px;margin:0"><div class="sheet">{s}</div></figure></body></html>')
js = """const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
 const pg = await b.newPage({ viewport: { width: 1000, height: 400 }, deviceScaleFactor: 1 });
 await pg.route(/fonts\\.g/, r => r.abort()); await pg.goto('file://' + %s); await pg.waitForTimeout(300);
 await pg.locator('#h').screenshot({ path: %s }); await b.close(); })();""" % (json.dumps(str((out / '_h.html').resolve())), json.dumps(sys.argv[1]))
(out / '_h.js').write_text(js)
subprocess.run('NODE_PATH=$(npm root -g) node out/_h.js', shell=True, check=True)
