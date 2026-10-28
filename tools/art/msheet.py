import sys, pathlib, subprocess, json
from PIL import Image, ImageDraw
REPO = pathlib.Path('/home/claude/liquor-cabinet')
names = sys.argv[1].split(',')
times = [int(t) for t in sys.argv[2].split(',')]
css = (REPO / 'src/pages/makers-mark/margie/page.css').read_text()
kit = (REPO / 'src/kit/kit.css').read_text()
defs = (REPO / 'src/kit/defs.svg').read_text().replace('  </defs>', (REPO / 'src/pages/makers-mark/cast.svg').read_text() + '  </defs>')
figs = ''.join(f'<figure class="fig on" id="s-{n}" style="width:400px;margin:8px"><div class="sheet">{(REPO / "src/pages/makers-mark/margie/scenes" / (n + ".svg")).read_text()}</div></figure>' for n in names)
pathlib.Path('out/_sheet.html').write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{kit}\n{css}\nbody{{background:#ddd;margin:0}}</style></head><body>{defs}{figs}</body></html>')
js = """
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
 const pg = await b.newPage({ viewport: { width: 416, height: 800 }, deviceScaleFactor: 1.5 });
 await pg.route(/fonts\\.g/, r => r.abort());
 await pg.goto('file://' + %s); await pg.waitForTimeout(300);
 for (const t of %s) { await pg.evaluate(t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; }), t);
   for (const n of %s) await pg.locator('#s-' + n).screenshot({ path: 'out/f_' + n + '_' + t + '.png' }); }
 await b.close(); })();""" % (json.dumps(str(pathlib.Path('out/_sheet.html').resolve())), json.dumps(times), json.dumps(names))
pathlib.Path('out/_sheet.js').write_text(js)
subprocess.run('NODE_PATH=$(npm root -g) node out/_sheet.js', shell=True, check=True)
ims = [[Image.open(f'out/f_{n}_{t}.png') for t in times] for n in names]
w, h = ims[0][0].size
S = Image.new('RGB', (w * len(times), h * len(names)), 'white')
for i, row in enumerate(ims):
    for j, im in enumerate(row): S.paste(im, (j * w, i * h))
S = S.resize((S.width * 2 // 3, S.height * 2 // 3))
S.save(sys.argv[3]); print(S.size)
