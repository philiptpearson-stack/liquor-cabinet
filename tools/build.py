#!/usr/bin/env python3
"""Build every story page into one self-contained file: <slug>/index.html.

A page is any folder under src/pages/ that holds a page.json. Folders nest,
so src/pages/makers-mark/founders-gamble/ builds makers-mark/founders-gamble/index.html.

Each page folder holds:
  page.json    title, description, the label in the top bar
  story.html   the page itself: copy + crayon scenes
  page.css     that page's own scene motion (optional)
  copy.md      the approved copy, one line per line of text on the page
  scenes/      crayon scenes as .svg files, placed with <!--scene:name-->
  cast.svg     character drawings (<symbol>s), shared with every page nested below

Real photos (the Maker's Mark ad, product shots) live in src/photos/ and are baked into
the page. Place one with <!--asset:name|alt text-->; if the file is missing, the page shows
a labelled placeholder instead. Inside a crayon scene, <!--swap:name|x y w h-->drawing<!--/swap-->
puts the photo in that box, and keeps the crayon drawing if there's no photo.
Photos aren't licensed yet: the site is for friends, not for the public (see robots.txt).

A link written href="@home" goes to the page the site opens on (src/site.json), and
href="@page:<slug>" goes to that page, as a path from wherever the link sits.

Every page ends with the Common Spirits Questions footer (src/kit/questions.html, its copy
in src/kit/questions.md). A page never lists itself, and a page whose footer would be empty
gets none. A page can opt out with "questions": false in its page.json.

The build refuses to write a page whose words don't match copy.md exactly,
so copy can't drift. Run:  python3 tools/build.py
"""
import base64, html, json, mimetypes, posixpath, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / 'src' / 'kit'
PAGES = ROOT / 'src' / 'pages'
PHOTOS = ROOT / 'src' / 'photos'

BLOCK = r'p|h1|h2|h3|h4|div|section|nav|li|a|summary|details|dl|dt|dd|figcaption'


def page_words(story: str) -> list[str]:
    """The text a reader sees, outside the illustrations, one entry per line."""
    s = re.sub(r'<figure\b.*?</figure>', '\n', story, flags=re.S)
    s = re.sub(r'<svg\b.*?</svg>', '', s, flags=re.S)          # door icons
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(rf'</({BLOCK})>', '\n', s)
    s = re.sub(rf'<({BLOCK})\b[^>]*>', '\n', s)
    s = re.sub(r'<span class="stamp"[^>]*>', '\n', s)           # "Coming soon" stamps sit on their own line
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    return [' '.join(line.split()) for line in s.split('\n') if line.strip()]


def approved_words(copy_md: str) -> list[str]:
    lines = []
    for line in copy_md.split('\n'):
        if line.startswith('#') or not line.strip():
            continue
        line = re.sub(r'(\*\*|\*|_)', '', line)
        lines.append(' '.join(line.split()))
    return lines


def find_photo(name: str):
    for ext in ('.webp', '.jpg', '.jpeg', '.png'):
        p = PHOTOS / (name + ext)
        if p.exists():
            return p
    return None


def place_assets(story: str) -> str:
    def sub(m):
        name, alt = m.group(1), m.group(2) or ''
        p = find_photo(name)
        if p:
            return f'<img class="asset" src="{data_uri(p)}" alt="{html.escape(alt)}">'
        return f'<div class="asset placeholder" role="img" aria-label="{html.escape(alt)}"><span>{html.escape(alt)}</span><small>Photo pending permission</small></div>'
    return re.sub(r'<!--asset:([\w-]+)(?:\|([^>]*?))?-->', sub, story)


def data_uri(p: Path) -> str:
    mime = mimetypes.guess_type(p.name)[0] or ('image/webp' if p.suffix == '.webp' else 'image/jpeg')
    return f'data:{mime};base64,' + base64.b64encode(p.read_bytes()).decode()


def place_swaps(story: str) -> tuple[str, str]:
    """Swap marked drawings for real photos. Each photo is embedded once per page, as a
    <symbol> in the shared defs, and every scene that shows it points there with <use>."""
    symbols = {}
    def sub(m):
        name, box, drawing = m.group(1), m.group(2).split(), m.group(3)
        p = find_photo(name)
        if not p:
            return drawing
        x, y, w, h = box
        key = f'photo-{name}-' + f'{w}x{h}'.replace('.', '_')
        if key not in symbols:
            symbols[key] = (f'<symbol id="{key}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMax meet">'
                            f'<image href="{data_uri(p)}" width="{w}" height="{h}" preserveAspectRatio="xMidYMax meet"/></symbol>')
        return f'<use href="#{key}" x="{x}" y="{y}" width="{w}" height="{h}"/>'
    story = re.sub(r'<!--swap:([\w-]+)\|([^>]*?)-->(.*?)<!--/swap-->', sub, story, flags=re.S)
    return story, ''.join(symbols.values())


def place_scenes(story: str, d: Path) -> tuple[str, list[str]]:
    missing = []
    def sub(m):
        f = d / 'scenes' / (m.group(1) + '.svg')
        if not f.exists():
            missing.append(m.group(1))
            return ''
        return f.read_text().strip()
    return re.sub(r'<!--scene:([\w-]+)-->', sub, story), missing


def cast_for(d: Path) -> str:
    """cast.svg from this page's folder and every folder above it, nearest last."""
    parts, cur = [], d
    while cur != PAGES.parent:
        f = cur / 'cast.svg'
        if f.exists():
            parts.append(f.read_text().strip())
        if cur == PAGES:
            break
        cur = cur.parent
    return '\n'.join(reversed(parts))


def questions_for(slug: str, kit: dict) -> str:
    """The shared footer, minus this page's own entry; '' when nothing is left."""
    def own(m):   # this page, or a page above it (a story inside the topic it answers)
        return '' if slug == m.group(1) or slug.startswith(m.group(1) + '/') else m.group(0)
    block = re.sub(r'\s*<p class="go" data-page="([\w/-]+)">.*?</p>', own, kit['questions'], flags=re.S)
    return block if 'data-page=' in block else ''


def build_page(d: Path, template: str, kit: dict, home: str) -> list[str]:
    slug = d.relative_to(PAGES).as_posix()
    meta = json.loads((d / 'page.json').read_text())
    story = (d / 'story.html').read_text()
    problems = []
    copy_file = d / 'copy.md'
    if copy_file.exists():
        have, want = page_words(story), approved_words(copy_file.read_text())
        if have != want:
            import difflib
            diff = '\n'.join(difflib.unified_diff(want, have, 'copy.md (approved)', 'story.html (page)', lineterm='', n=1))
            problems.append(f'{slug}: page words differ from copy.md\n{diff}')
    else:
        problems.append(f'{slug}: no copy.md, so the copy check was skipped')
    # the shared footer goes at the end of the story's main column
    if meta.get('questions', True):
        footer = questions_for(slug, kit)
        if footer:
            i = story.rstrip().rfind('</div>')
            story = story[:i].rstrip() + '\n\n  ' + footer.strip() + '\n' + story[i:]
    # href="@home" = the page the site opens on (src/site.json); href="@page:<slug>" = that page
    story = story.replace('href="@home"', 'href="' + posixpath.relpath(home + '/index.html', slug) + '"')
    story = re.sub(r'href="@page:([\w/-]+)"', lambda m: 'href="' + posixpath.relpath(m.group(1) + '/index.html', slug) + '"', story)
    story, missing = place_scenes(story, d)
    if missing:
        problems.append(f'{slug}: missing scene file(s): {", ".join(missing)}')
    cast = cast_for(d)
    defs = kit['defs']
    if cast:
        defs = defs.replace('  </defs>', cast + '\n  </defs>')
    if any(p for p in problems if 'differ' in p or 'missing scene' in p):
        return problems
    story, photo_defs = place_swaps(place_assets(story))
    if photo_defs:
        defs = defs.replace('  </defs>', photo_defs + '\n  </defs>')
    for _ in (1,):
        out = template
        for key, value in {
            'title': html.escape(meta['title']), 'description': html.escape(meta.get('description', '')),
            'label': html.escape(meta['label']), 'kit_css': kit['css'],
            'page_css': (d / 'page.css').read_text() if (d / 'page.css').exists() else '',
            'defs': defs, 'story': story.rstrip(), 'kit_js': kit['js'].rstrip(),
        }.items():
            out = out.replace('{{' + key + '}}', value)
        if '{{' in out:
            problems.append(f'{slug}: unfilled placeholder in the template')
            return problems
        dest = ROOT / slug
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'index.html').write_text(out)
        print(f'built {slug}/index.html ({len(out) // 1024} KB)')
    return problems


def redirect(target: str) -> str:
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={target}"><title>The Liquor Cabinet</title></head>'
            f'<body><a href="{target}">The Liquor Cabinet</a></body></html>\n')


def main() -> int:
    kit = {'css': (KIT / 'kit.css').read_text().rstrip(), 'defs': (KIT / 'defs.svg').read_text().rstrip(), 'js': (KIT / 'kit.js').read_text(),
           'questions': (KIT / 'questions.html').read_text()}
    template = (KIT / 'page.html').read_text()
    site = json.loads((ROOT / 'src' / 'site.json').read_text())
    problems = []
    if page_words(kit['questions']) != approved_words((KIT / 'questions.md').read_text()):
        problems.append('kit: Common Spirits Questions words differ from src/kit/questions.md')
    for d in sorted(p.parent for p in PAGES.rglob('page.json')):
        problems += build_page(d, template, kit, site['home'].strip('/'))
    home = site['home'].strip('/') + '/index.html'
    (ROOT / 'index.html').write_text(redirect(home))
    for p in problems:
        print('PROBLEM:', p, file=sys.stderr)
    return 1 if any('differ' in p or 'placeholder' in p or 'missing scene' in p for p in problems) else 0


if __name__ == '__main__':
    sys.exit(main())
