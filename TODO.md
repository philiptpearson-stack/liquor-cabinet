# Things to check on

Open items that aren't today's work but mustn't get lost. Newest at the bottom.

## When the app's title page exists
- [ ] **Point the site's home at it.** Change `"home"` in `src/site.json` from `makers-mark` to the title page's folder. The site's front door follows, and so does every `href="@home"` link.
- [ ] **Check "← Back to the bottle" on shared pages (Fermentation).** It returns readers to the bottle that sent them. When the page can't tell where they came from (a shared link, a fresh tab), it falls back to `@home`. That's Maker's Mark today and becomes the title page once `site.json` changes. Then decide whether the label should read differently in that case, since it would no longer land on a bottle. *(Philip, Oct 27 2026)*

## Before anyone outside friends sees it
- [ ] **Photo permissions.** The Maker's Mark bottle shot and the 1966 "It tastes expensive... and is." ad (`src/photos/`) belong to Suntory Global Spirits. Get permission before launch; Philip has friends there for intros.
- [ ] **The repo is public**, so those photos are visible on GitHub. Philip chose this knowingly (Oct 27 2026). Revisit if anything changes.
- [ ] **Search engines.** Pages carry `noindex` (`src/kit/page.html`) and `robots.txt` blocks crawlers. Remove both at launch.
