# Things to check on

Open items that aren't today's work but mustn't get lost. Newest at the bottom.

## When the app's title page exists
- [ ] **Point the site's home at it.** Change `"home"` in `src/site.json` from `makers-mark` to the title page's folder. The site's front door follows, and so does every `href="@home"` link.
- [x] **"← Back to the bottle" on shared hubs (Fermentation).** It now says where it actually goes ("Back to The Founder's Gamble", "Back to Maker's Mark"); each page notes its name for the visit (sessionStorage). Opened fresh, it still says "Back to the bottle" and goes to `@home`. When the title page becomes home, that fallback label will need changing. *(Philip, Oct 27 and 31 2026)*

## Pages waiting to be built (they show as "Coming soon" now)
- [x] **Margie Samuels: One of Whiskey's Most Iconic Women** (Maker's Mark door): built Oct 27 2026
- [x] **The Wall Street Journal Article that Changed *Everything*** (Maker's Mark door): built Oct 29 2026
- [ ] **What IS bourbon, anyway** (shared; Door 1 links to it)
- [ ] **But how did HUMANS Harness Fermentation?** (the second fermentation story; the hub shows it as coming soon)
- [ ] **Distillation hub**, built like the Fermentation hub, when we get there
- [x] **WSJ page, premium shelf: real bottle photos.** Philip sent Blanton's, Booker's, Knob Creek and Woodford Reserve, cut out and on the shelf Oct 29 2026.
- [ ] **The Bartender's Perspective** (concept agreed Oct 30 2026). The bartender is Phil. Maker's Mark's is built (Oct 30, late) from Philip's copy: a shot of Maker's on its own, then a Whiskey Sour from the Cocktail Menu. Waiting on Philip: the lines Claude added (recipe card kicker, a how-to line after each step title, "→ The Cocktail Menu", and the "If you like Maker's" section kept from his earlier notes). The Old Fashioned build animation is parked in `tools/art/drafts/` for the Old Fashioned's own page.
  - **Title:** "The Bartender's Perspective:" in small type over the bottle's name, styled the way it is on the bottle's own page (`h1 .h1-lead` in the kit).
  - **"How would I drink it?"**: his honest take.
  - **A cocktail suggestion** from the Cocktail Menu (Maker's: the Whiskey Sour), with a complete how-to, linking to that cocktail's own page.
  - **"Want some suggestions of other bourbons to try?"**: a card that opens, with bottles to try next (as links, once they have pages).
  - Maybe: the Door 1 cast (flat cap guy, the posh lady, the working man) as his regulars.
  - Not sold yet: "Behind the stick" (one thing only a bartender knows).
- [ ] **Cocktail Menu**: not tied to any bottle; the front door to the whole cocktail / recipe / how-to side of the app. Each cocktail (Old Fashioned, Paper Plane, …) gets its own page.
- [ ] **Cocktails How-To** (`cocktails-how-to/`): built Oct 31 2026 as a hub like Fermentation (a door per technique; the Short Version card lives on the Golden Ratio page). **The Golden Ratio** is drafted from Philip's notes and waiting on his edits; to check in it: the "three dashes per ¼ oz of syrup" starting point and the Trinidad Sour aside. (Philip set the Negroni and Boulevardier at 2:1:1, so the equal-parts aside is gone.) Still to come: Shake or Stir?, Simple Syrup in Two Minutes, All About Ice, Neat / Rocks / Up, The Tools You Actually Need. The Maker's bartender page's note links here.
- [ ] **Front page idea:** "Welcome to my bar, ask me about a bottle." Not a shelf of every bottle (too many to draw); later, point the phone camera at a bottle and get its page.

## Once more pages exist
- [ ] **Pepper in rabbit-hole links.** Go back through the early pages (Maker's Mark and its three doors, Fermentation) and add links inside the story itself, wherever a line touches something that has its own page: wheated bourbon, what bourbon is, aging, the other bottles on the premium shelf, and so on. The links at the end stay; these would be extra. *(Philip, Oct 29 2026)*

## Before anyone outside friends sees it
- [ ] **Photo permissions.** Everything in `src/photos/` belongs to the brands. Suntory Global Spirits: the Maker's Mark bottle shots, the 1966 "It tastes expensive... and is." ad, Booker's and Knob Creek. Sazerac: Blanton's. Brown-Forman: Woodford Reserve. Get permission before launch; Philip has friends at Suntory for intros.
- [ ] **The repo is public**, so those photos are visible on GitHub. Philip chose this knowingly (Oct 27 2026). Revisit if anything changes.
- [ ] **Search engines.** Pages carry `noindex` (`src/kit/page.html`) and `robots.txt` blocks crawlers. Remove both at launch.
