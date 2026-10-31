# Things to check on

Open items that aren't today's work but mustn't get lost. Newest at the bottom.

## When the app's title page exists
- [ ] **Point the site's home at it.** Change `"home"` in `src/site.json` from `makers-mark` to the title page's folder. The site's front door follows, and so does every `href="@home"` link.
- [ ] **Check "← Back to the bottle" on shared hubs (Fermentation).** It returns readers to the bottle that sent them. When the page can't tell where they came from (a shared link, a fresh tab), it falls back to `@home`. That's Maker's Mark today and becomes the title page once `site.json` changes. Then decide whether the label should read differently in that case, since it would no longer land on a bottle. *(Philip, Oct 27 2026)*

## Pages waiting to be built (they show as "Coming soon" now)
- [x] **Margie Samuels: One of Whiskey's Most Iconic Women** (Maker's Mark door): built Oct 27 2026
- [x] **The Wall Street Journal Article that Changed *Everything*** (Maker's Mark door): built Oct 29 2026
- [ ] **What IS bourbon, anyway** (shared; Door 1 links to it)
- [ ] **But how did HUMANS Harness Fermentation?** (the second fermentation story; the hub shows it as coming soon)
- [ ] **Distillation hub**, built like the Fermentation hub, when we get there
- [x] **WSJ page, premium shelf: real bottle photos.** Philip sent Blanton's, Booker's, Knob Creek and Woodford Reserve, cut out and on the shelf Oct 29 2026.
- [ ] **The Bartender's Perspective** (concept agreed Oct 30 2026). The bartender is Phil. Maker's Mark's is built (Oct 30, late) from Philip's copy: a shot of Maker's on its own, then a Whiskey Sour from the Cocktail Menu. Waiting on Philip: the lines Claude added (recipe card kicker, a how-to line after each step title, "→ The Cocktail Menu", and the "If you like Maker's" section kept from his earlier notes). The Old Fashioned build animation is parked in `tools/art/drafts/` for the Old Fashioned's own page.
  - **"How would I drink it?"**: his honest take.
  - **A cocktail suggestion** from the Cocktail Menu (Maker's: the Whiskey Sour), with a complete how-to, linking to that cocktail's own page.
  - **"If you like this…"**: bottles to try next, as links.
  - Maybe: the Door 1 cast (flat cap guy, the posh lady, the working man) as his regulars.
  - Not sold yet: "Behind the stick" (one thing only a bartender knows).
- [ ] **Cocktail Menu**: not tied to any bottle; the front door to the whole cocktail / recipe / how-to side of the app. Each cocktail (Old Fashioned, Paper Plane, …) gets its own page.
- [ ] **Ask the Bartender**: shared how-tos any page can link to (neat, rocks or up; shaken or stirred; simple syrup …).
- [ ] **Front page idea:** "Welcome to my bar, ask me about a bottle." Not a shelf of every bottle (too many to draw); later, point the phone camera at a bottle and get its page.

## Once more pages exist
- [ ] **Pepper in rabbit-hole links.** Go back through the early pages (Maker's Mark and its three doors, Fermentation) and add links inside the story itself, wherever a line touches something that has its own page: wheated bourbon, what bourbon is, aging, the other bottles on the premium shelf, and so on. The links at the end stay; these would be extra. *(Philip, Oct 29 2026)*

## Before anyone outside friends sees it
- [ ] **Photo permissions.** Everything in `src/photos/` belongs to the brands. Suntory Global Spirits: the Maker's Mark bottle shots, the 1966 "It tastes expensive... and is." ad, Booker's and Knob Creek. Sazerac: Blanton's. Brown-Forman: Woodford Reserve. Get permission before launch; Philip has friends at Suntory for intros.
- [ ] **The repo is public**, so those photos are visible on GitHub. Philip chose this knowingly (Oct 27 2026). Revisit if anything changes.
- [ ] **Search engines.** Pages carry `noindex` (`src/kit/page.html`) and `robots.txt` blocks crawlers. Remove both at launch.
