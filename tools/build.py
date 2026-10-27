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

Photos we don't have permission for yet (the Maker's Mark ad, product shots) live
in src/private/, which is never committed. Place one with <!--asset:name|alt text-->.
The public build (what Vercel serves) shows a labelled placeholder there; the review
build (review/, for private review links) shows the real image.

The build refuses to write a page whose words don't match copy.md exactly,
so copy can't drift. Run:  python3 tools/build.py
"""
import base64, html, json, mimetypes, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / 'src' / 'kit'
PAGES = ROOT / 'src' / 'pages'
PRIVATE = ROOT / 'src' / 'private'
REVIEW = ROOT / 'review'

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


def find_private(name: str):
    for ext in ('.webp', '.jpg', '.jpeg', '.png'):
        p = PRIVATE / (name + ext)
        if p.exists():
            return p
    return None


def place_assets(story: str, review: bool) -> str:
    def sub(m):
        name, alt = m.group(1), m.group(2) or ''
        p = find_private(name) if review else None
        if p:
            mime = mimetypes.guess_type(p.name)[0] or 'image/jpeg'
            data = base64.b64encode(p.read_bytes()).decode()
            return f'<img class="asset" src="data:{mime};base64,{data}" alt="{html.escape(alt)}">'
        return f'<div class="asset placeholder" role="img" aria-label="{html.escape(alt)}"><span>{html.escape(alt)}</span><small>Photo pending permission</small></div>'
    return re.sub(r'<!--asset:([\w-]+)(?:\|([^>]*?))?-->', sub, story)


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


def build_page(d: Path, template: str, kit: dict) -> list[str]:
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
    story, missing = place_scenes(story, d)
    if missing:
        problems.append(f'{slug}: missing scene file(s): {", ".join(missing)}')
    cast = cast_for(d)
    defs = kit['defs']
    if cast:
        defs = defs.replace('  </defs>', cast + '\n  </defs>')
    if any(p for p in problems if 'differ' in p or 'missing scene' in p):
        return problems
    for review in (False, True):
        out = template
        for key, value in {
            'title': html.escape(meta['title']), 'description': html.escape(meta.get('description', '')),
            'label': html.escape(meta['label']), 'kit_css': kit['css'],
            'page_css': (d / 'page.css').read_text() if (d / 'page.css').exists() else '',
            'defs': defs, 'story': place_assets(story, review).rstrip(), 'kit_js': kit['js'].rstrip(),
        }.items():
            out = out.replace('{{' + key + '}}', value)
        if '{{' in out:
            problems.append(f'{slug}: unfilled placeholder in the template')
            return problems
        dest = (REVIEW if review else ROOT) / slug
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'index.html').write_text(out)
        if not review:
            print(f'built {slug}/index.html ({len(out) // 1024} KB)')
    return problems


def redirect(target: str) -> str:
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={target}"><title>The Liquor Cabinet</title></head>'
            f'<body><a href="{target}">The Liquor Cabinet</a></body></html>\n')


def main() -> int:
    kit = {'css': (KIT / 'kit.css').read_text().rstrip(), 'defs': (KIT / 'defs.svg').read_text().rstrip(), 'js': (KIT / 'kit.js').read_text()}
    template = (KIT / 'page.html').read_text()
    site = json.loads((ROOT / 'src' / 'site.json').read_text())
    problems = []
    for d in sorted(p.parent for p in PAGES.rglob('page.json')):
        problems += build_page(d, template, kit)
    home = site['home'].strip('/') + '/index.html'
    (ROOT / 'index.html').write_text(redirect(home))
    REVIEW.mkdir(exist_ok=True)
    (REVIEW / 'index.html').write_text(redirect(home))
    for p in problems:
        print('PROBLEM:', p, file=sys.stderr)
    return 1 if any('differ' in p or 'placeholder' in p or 'missing scene' in p for p in problems) else 0


if __name__ == '__main__':
    sys.exit(main())
