// Checks every built page in a phone-sized browser before it ships.
//   NODE_PATH=$(npm root -g) node tools/check.js            (all pages)
//   NODE_PATH=$(npm root -g) node tools/check.js fermentation
// Looks for: script errors, broken images, sideways overflow at 390px,
// animation running with scripts OFF, a still page with reduced motion,
// and (where a page has one) the rewind picture and its era label in sync.
// Screenshots of every scene land in tools/shots/ (not committed).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const SHOTS = path.join(__dirname, 'shots');
const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
const pages = process.argv.slice(2).length ? process.argv.slice(2)
  : fs.readdirSync(path.join(ROOT, 'src', 'pages')).filter(d => fs.existsSync(path.join(ROOT, d, 'index.html')));

const md5 = b => crypto.createHash('md5').update(b).digest('hex').slice(0, 8);

(async () => {
  fs.mkdirSync(SHOTS, { recursive: true });
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  let failures = 0;
  const fail = (slug, msg) => { failures++; console.log(`  FAIL ${slug}: ${msg}`); };

  for (const slug of pages) {
    const url = 'file://' + path.join(ROOT, slug, 'index.html');
    console.log(`\n${slug}`);

    // 1. Scripts on, normal motion
    {
      const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(String(e)));
      page.on('requestfailed', r => { if (!/fonts\.g(oogleapis|static)\.com/.test(r.url())) errors.push('could not load ' + r.url()); });
      await page.route(/fonts\.g(oogleapis|static)\.com/, r => r.abort()); // web fonts aren't reachable from the build machine
      await page.goto(url);
      await page.waitForTimeout(500);
      const info = await page.evaluate(() => ({
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        broken: [...document.images].filter(i => !i.naturalWidth).length,
        figs: [...document.querySelectorAll('.fig')].map(f => f.id),
        js: document.documentElement.classList.contains('js'),
      }));
      if (errors.length) fail(slug, 'script errors: ' + errors.join(' | '));
      if (info.overflow > 0) fail(slug, `page is ${info.overflow}px wider than the phone`);
      if (info.broken) fail(slug, `${info.broken} broken image(s)`);
      if (!info.js) fail(slug, 'kit.js did not run');
      console.log(`  scripts on: ${info.figs.length} scenes, no overflow: ${info.overflow <= 0}`);

      for (const id of info.figs) {
        await page.evaluate(id => document.getElementById(id).scrollIntoView({ block: 'center' }), id);
        await page.waitForTimeout(250);
        await page.locator('#' + id).screenshot({ path: path.join(SHOTS, `${slug}_${id}.png`) });
      }

      if (info.figs.includes('rewind')) {
        const rows = await page.evaluate(() => {
          const f = document.getElementById('rewind'), strip = document.getElementById('strip');
          const anims = f.getAnimations({ subtree: true });
          const out = [];
          for (let t = 0; t < 12900; t += 50) {
            anims.forEach(a => { a.pause(); a.currentTime = t; });
            const m = new DOMMatrix(getComputedStyle(strip).transform);
            const op = +getComputedStyle(strip).opacity;
            const era = Math.min(4, Math.max(0, Math.floor((-m.e + 200) / 400)));
            if (Math.abs(((-m.e + 200) % 400)) < 3) continue; // exactly mid-pan: the label is mid-swap
            const shown = [...f.querySelectorAll('.chip.era b')].findIndex(b => +getComputedStyle(b).opacity > 0.5);
            out.push([t, era, shown, op]);
          }
          return out;
        });
        // During the fade back to the city the picture is invisible, so either label is fine there.
        const bad = rows.filter(([t, era, shown, op]) => op > 0.05 && era !== shown);
        const order = [...new Set(rows.filter(r => r[3] > 0.5).map(r => r[1]))].join(' > ');
        if (bad.length) fail(slug, `rewind label out of sync at ${bad.length} of ${rows.length} moments, e.g. ${JSON.stringify(bad.slice(0, 4))}`);
        else console.log(`  rewind: picture and label in sync at all ${rows.length} sampled moments; eras ${order}`);
      }
      await ctx.close();
    }

    // 2. Scripts OFF (phone file previews block them): scenes must still move
    {
      const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, javaScriptEnabled: false });
      const page = await ctx.newPage();
      await page.route(/fonts\.g(oogleapis|static)\.com/, r => r.abort());
      await page.goto(url);
      await page.waitForTimeout(400);
      const moving = [];
      for (const id of ['rewind', 's-bear', 's-ancestor', 's-yeast']) {
        const loc = page.locator('#' + id);
        if (!(await loc.count())) continue;
        await loc.scrollIntoViewIfNeeded();
        const a = md5(await loc.screenshot({ animations: 'allow' }));
        await page.waitForTimeout(id === 'rewind' ? 2600 : 900);
        const b = md5(await loc.screenshot({ animations: 'allow' }));
        if (a === b) fail(slug, `#${id} doesn't move with scripts off`); else moving.push(id);
      }
      console.log(`  scripts off: moving -> ${moving.join(', ') || 'nothing checked'}`);
      await ctx.close();
    }

    // 3. Reduced motion: a calm, still page
    {
      const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' });
      const page = await ctx.newPage();
      await page.route(/fonts\.g(oogleapis|static)\.com/, r => r.abort());
      await page.goto(url);
      await page.waitForTimeout(400);
      const r = await page.evaluate(() => ({
        running: document.querySelectorAll('.fig').length ? [...document.querySelectorAll('.fig *')].filter(el => getComputedStyle(el).animationName !== 'none').length : 0,
        still: document.documentElement.classList.contains('still'),
      }));
      if (r.running) fail(slug, `${r.running} elements still animate with reduced motion on`);
      console.log(`  reduced motion: still=${r.still}, animated elements=${r.running}`);
      await ctx.close();
    }
  }
  await browser.close();
  console.log(failures ? `\n${failures} problem(s)` : '\nall checks passed');
  process.exit(failures ? 1 : 0);
})();
