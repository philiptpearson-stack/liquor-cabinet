#!/usr/bin/env python3
"""Build every story page into one self-contained file: <slug>/index.html.

Each page lives in src/pages/<slug>/:
  page.json   title, description, the label in the top bar
  story.html  the page itself: copy + crayon scenes
  page.css    that page's own scene motion
  copy.md     the approved copy, one line per line of text on the page

The build refuses to write a page whose words don't match copy.md exactly,
so copy can't drift. Run:  python3 tools/build.py
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / 'src' / 'kit'
PAGES = ROOT / 'src' / 'pages'


def page_words(story: str) -> list[str]:
    """The text a reader sees, outside the illustrations, one entry per line."""
    s = re.sub(r'<figure\b.*?</figure>', '\n', story, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'</(p|h1|h2|h3|div|section|span|li)>', lambda m: '\n' if m.group(1) != 'span' or False else '', s)
    s = re.sub(r'<(div|section|p|h1|h2|h3|li)\b[^>]*>', '\n', s)
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


def build_page(slug: str, template: str, kit: dict) -> list[str]:
    d = PAGES / slug
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
    out = template
    for key, value in {
        'title': html.escape(meta['title']), 'description': html.escape(meta.get('description', '')),
        'label': html.escape(meta['label']), 'kit_css': kit['css'], 'page_css': (d / 'page.css').read_text() if (d / 'page.css').exists() else '',
        'defs': kit['defs'], 'story': story.rstrip(), 'kit_js': kit['js'].rstrip(),
    }.items():
        out = out.replace('{{' + key + '}}', value)
    if '{{' in out:
        problems.append(f'{slug}: unfilled placeholder in the template')
    if not [p for p in problems if 'differ' in p or 'placeholder' in p]:
        (ROOT / slug).mkdir(exist_ok=True)
        (ROOT / slug / 'index.html').write_text(out)
        print(f'built {slug}/index.html ({len(out) // 1024} KB)')
    return problems


def main() -> int:
    kit = {'css': (KIT / 'kit.css').read_text().rstrip(), 'defs': (KIT / 'defs.svg').read_text().rstrip(), 'js': (KIT / 'kit.js').read_text()}
    template = (KIT / 'page.html').read_text()
    site = json.loads((ROOT / 'src' / 'site.json').read_text())
    problems = []
    for d in sorted(p for p in PAGES.iterdir() if p.is_dir()):
        problems += build_page(d.name, template, kit)
    home = site['home']
    (ROOT / 'index.html').write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0; url=/{home}/"><title>The Liquor Cabinet</title>'
        f'<link rel="canonical" href="/{home}/"></head><body><a href="/{home}/">The Liquor Cabinet</a></body></html>\n')
    for p in problems:
        print('PROBLEM:', p, file=sys.stderr)
    return 1 if any('differ' in p or 'placeholder' in p for p in problems) else 0


if __name__ == '__main__':
    sys.exit(main())
