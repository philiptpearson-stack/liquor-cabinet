# The Liquor Cabinet

Little stories. Big spirits. A scroll-story app about what's in the bottle, drawn in a plum-crayon house style.

Live at https://the-liquor-cabinet.vercel.app (Vercel publishes this repo's `main` branch).

## How it's put together

```
src/
  kit/            the house style, shared by every page
    kit.css       paper, type, layout, scene motion, pause rules
    defs.svg      crayon / watercolor / "boil" filters and the character drawings (yeast-bud, ...)
    kit.js        optional extras: Pause button, reading bar, pausing scenes that are off screen
    page.html     the page template
    questions.html  the Common Spirits Questions footer every page ends with (copy in questions.md)
  pages/<slug>/   one folder per story (folders nest: makers-mark/founders-gamble/)
    page.json     title, link-preview description, top-bar label
    story.html    the page: copy + crayon scenes
    page.css      that page's own scene motion
    copy.md       the approved copy, one line per line of text
    scenes/       crayon scenes as .svg files, placed with <!--scene:name-->
    cast.svg      character drawings shared with every page below this folder
  photos/         real photos (product shots, old ads), baked into the pages
  site.json       which page the site opens on
tools/
  build.py        builds src/ into <slug>/index.html (one self-contained file per page)
  check.js        checks every page in a phone-sized browser
<slug>/index.html built pages (what Vercel serves; don't edit by hand)
```

## House rules

1. **The copy is the boss.** `copy.md` holds Philip's approved words. The build refuses to write a page whose words drift from it.
2. **Motion runs on CSS alone.** Pages must animate even where scripts are blocked (phone file previews). Scripts only add the Pause button, the reading bar and off-screen pausing.
3. **Calm when asked.** With reduced motion on, every scene sits still on its resting frame.
4. **One file per page.** Each built page works on its own: on Vercel, as a review link, or opened from a phone's Files app.
5. **Characters are drawn once.** Shared characters live in `defs.svg` so they look the same on every page.
6. **Plain web files.** No Vercel-only features, so the app can move hosts or be wrapped for the App Store later.
7. **Friends only, for now.** The brand photos aren't licensed yet, so pages ask search engines to stay away (`robots.txt`, `noindex`). Get permissions before launch.

## Things to check on

`TODO.md` keeps open items that come up along the way (the title page, photo permissions, launch switches).

## Building and checking

```
python3 tools/build.py
NODE_PATH=$(npm root -g) node tools/check.js
```

`check.js` needs Playwright with Chromium. It reports script errors, broken images, sideways overflow at phone width, motion with scripts off, reduced motion, and the rewind picture/label sync, and saves a screenshot of every scene to `tools/shots/`.
