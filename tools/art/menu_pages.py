"""The Cocktail Menu: writes every page (story, copy, meta, motion, scenes) for the Classics.

    python3 tools/art/menu_pages.py

The words live in menu_drinks.py; copy.md is written from the page so the build's copy check
starts out in step. Once Philip edits a page's words by hand, take that drink out of REWRITE below
(or edit menu_drinks.py and rerun), so his edits are never overwritten.
"""
import html, json, pathlib, re, sys
from art import *
from menu_art import *
from menu_build import Build, oz_text, BAR
from menu_drinks import DRINKS, BY_SLUG, SOON
from bartender import bartender
from shelves import plain_bottle

REPO = pathlib.Path('/home/claude/liquor-cabinet')
sys.path.insert(0, str(REPO / 'tools'))
from build import page_words   # noqa: E402

MENU = REPO / 'src/pages/cocktail-menu'
REWRITE = {d['slug'] for d in DRINKS}   # drinks whose pages this script may (re)write
GENRE_NAME = {'classics': 'Classics', **dict(SOON)}   # the parts of the menu, by folder


def genre(d):
    return d.get('genre', 'classics')
GLASS_WORD = {'coupe': 'coupe', 'martini': 'martini glass', 'rocks': 'rocks glass', 'highball': 'tall glass of ice', 'flute': 'Champagne flute'}
HERO_SCALE = {'coupe': 1.8, 'martini': 1.55, 'rocks': 1.45, 'highball': 1.3, 'flute': 1.25}
ICON_SCALE = {'coupe': 1.35, 'martini': 1.18, 'rocks': 1.3, 'highball': .93, 'flute': .87}
GARNISH_WORD = {'lime-wheel': 'a lime wheel', 'lemon-wheel': 'a lemon wheel', 'lime-wedge': 'a lime wedge', 'grapefruit-wedge': 'a grapefruit wedge',
                'lemon-twist': 'a lemon twist', 'orange-twist': 'an orange twist', 'orange-peel': 'an orange peel', 'cherry': 'a cherry',
                'olives': 'olives', 'mint': 'a sprig of mint', 'flower': 'an edible flower'}


def a_an(w):
    return ('an ' if w[0].lower() in 'aeiou' else 'a ') + w


# ---------------------------------------------------------------- hero: the finished drink, its ingredients beside it
def prop(spec):
    """(drawing with its feet at 0, 0, words for the alt text)"""
    if spec.startswith('fruit:'):
        k = spec[6:]
        return at(0, 0, fruit(k), 1.4), a_an(k)
    if spec.startswith('half:'):
        k = spec[5:]
        return at(0, 0, fruit(k, half=True), 1.4), f'half {a_an(k)}'
    if spec == 'honey':
        return at(0, 0, honey_jar(), 1.45), 'a jar of honey'
    if spec == 'egg':
        return at(0, 0, egg(), 1.5), 'an egg'
    if spec == 'mint':
        return at(0, 0, mint_bunch(), 1.25), 'fresh mint'
    if spec == 'bitters':
        return at(0, -18 * 1.5, bitters(), 1.5), 'a bottle of bitters'
    if spec == 'syrup':   # a bottle of simple syrup (Philip, Nov 3: the Daiquiri should show one)
        return at(0, 0, bottle('tall', '#f4ecd0', 'simple syrup', cap='#c25c86'), 1.5), 'a bottle of simple syrup'
    if spec == 'pear':
        return at(0, 0, pear(), 1.4), 'a pear'
    return at(0, 0, ing_bottle(spec), 1.55), f'a bottle of {ING[spec][0]}'


def iced(d):
    """Served on ice: ice goes into the glass, or the drink is poured in with its ice (the El Diablo)."""
    return any((a[0] == 'ice' and a[1] == 'glass') or a[0] == 'dump' for _, acts in d['steps'] for a in acts)


def hero(d):
    left, right = d['hero']
    out = wash('<rect x="0" y="0" width="400" height="236" fill="#efe3d0"/>' + f'<ellipse cx="200" cy="118" rx="98" ry="86" fill="{d["color"]}" opacity=".32"/>'
               ) + countertop(182)
    words = []
    for spec, x in zip(left, (78, 126)[-len(left):]):
        p, w = prop(spec)
        out += f'<g transform="translate({x} 184)">{p}</g>'
        words.append(w)
    for spec, x in zip(right, (274, 322)):
        p, w = prop(spec)
        out += f'<g transform="translate({x} 184)">{p}</g>'
        words.append(w)
    fizzy = any(a[0] == 'top' and a[1] in FIZZY for _, acts in d['steps'] for a in acts)
    served_iced = iced(d)
    layers = None
    if d['slug'] == 'dark-and-stormy':
        layers = [(.68, 1, '#5a2e14')]
    drink = glass(d['glass'], f'{d["slug"]}-hero', d['color'], d['garnish'], iced=served_iced, foam=d.get('foam', False), layers=layers, bubbles=fizzy,
                  top=d.get('level'))
    out += f'<g transform="translate(200 184) scale({HERO_SCALE[d["glass"]]})">{drink}</g>'
    out += sparkle(150, 46, 6, 'twinkle') + sparkle(258, 40, 5, 'twinkle d2') + sparkle(246, 100, 4, 'twinkle d3')
    g = ' and '.join(GARNISH_WORD[k] for k in d['garnish'])
    beside = ', '.join(words[:-1]) + (' and ' if len(words) > 1 else '') + words[-1]
    alt = f'{a_an(d["name"])} in {a_an(GLASS_WORD[d["glass"]])}, garnished with {g}, next to {beside}'
    return svg_view(out, alt, '52 24 296 180')


def icon(d):
    served_iced = iced(d)
    layers = [(.68, 1, '#5a2e14')] if d['slug'] == 'dark-and-stormy' else None
    return at(60, 112, glass(d['glass'], f'{d["slug"]}-ic', d['color'], d['garnish'], iced=served_iced, foam=d.get('foam', False), layers=layers, top=d.get('level')),
              ICON_SCALE[d['glass']])


# ---------------------------------------------------------------- the rest of the menu: icons for the doors still to come
def soon_icons():
    ic = {}
    ic['modern-variations'] = (at(60, 112, glass('coupe', 'mv-ic', '#e98fa6', ['orange-twist']), 1.3) + sparkle(28, 30, 8) + sparkle(96, 22, 5.5) + sparkle(18, 70, 4))
    potion = 'M-14 0 Q-24 -2 -22 -20 Q-20 -34 -6 -38 L-6 -52 L6 -52 L6 -38 Q20 -34 22 -20 Q24 -2 14 0Z'
    ic['arcane-oddities'] = (at(60, 112, wash(f'<path d="{potion}" fill="#5b3a7a"/><rect x="-8" y="-60" width="16" height="9" rx="2" fill="#9b7663"/><path d="M-18 -18 Q0 -10 18 -18 Q20 -6 12 -2 L-12 -2 Q-20 -6 -18 -18Z" fill="#7fd1b9" opacity=".8"/>')
                                 + lines(f'<path d="{potion}" stroke-width="2.2"/><rect x="-8" y="-60" width="16" height="9" rx="2" stroke-width="1.8"/>', boil=False)
                                 + '<text class="letter" x="0" y="-22" font-size="22" text-anchor="middle" style="fill:#f2c776">?</text>', 1.35)
                              + sparkle(24, 34, 6) + sparkle(98, 46, 4.5) + lines('<path d="M92 14 a12 12 0 1 0 12 16 a9 9 0 1 1 -12 -16Z" fill="#f2c776"/>', boil=False))
    mug = 'M-16 0 L-19 -50 Q0 -56 19 -50 L16 0Z'
    ic['tiki-and-tropical'] = (at(56, 112, wash(f'<path d="{mug}" fill="#a0673a"/>') + lines(f'<path d="{mug}" stroke-width="2.2"/><path d="M-11 -36 h7 M4 -36 h7 M-9 -22 q9 6 18 0 M-14 -44 h28 M-12 -12 h24" stroke-width="2"/>', boil=False), 1.35)
                              + lines('<path d="M70 44 L96 14" stroke="#8a6a3c" stroke-width="2"/>', boil=False) + wash('<path d="M78 24 Q96 0 114 22Z" fill="#e8737a"/>')
                              + lines('<path d="M78 24 Q96 0 114 22Z M96 10 L90 24 M96 10 L102 23" stroke-width="1.8"/>', boil=False) + at(28, 50, wheel('orange', 9)))
    ic['low-and-no-proof'] = (at(56, 112, glass('highball', 'np-ic', '#f6c98a', ['lemon-wheel'], iced=True, bubbles=False), .93)
                              + wash('<rect x="80" y="70" width="32" height="20" rx="4" fill="#fbf3e3"/>') + lines('<rect x="80" y="70" width="32" height="20" rx="4" stroke-width="1.8"/>', boil=False)
                              + '<text class="letter" x="96" y="85" font-size="13" text-anchor="middle">0%</text>')
    cup = 'M-22 -40 L22 -40 L18 0 L-18 0Z'
    ic['warm-and-cozy'] = (at(56, 110, wash(f'<path d="{cup}" fill="#b35a3c"/>') + lines(f'<path d="{cup}" stroke-width="2.4"/><path d="M21 -32 q14 2 10 16 q-3 8 -12 6" stroke-width="2.4"/>', boil=False), 1.3)
                           + lines('<path d="M44 46 q-6 -8 0 -16 q6 -8 0 -16 M58 44 q-6 -8 0 -16 q6 -8 0 -16 M72 46 q-6 -8 0 -16 q6 -8 0 -16" stroke="#a9a29a" stroke-width="2.2"/>', boil=False)
                           + wash('<rect x="78" y="40" width="7" height="34" rx="2" fill="#8a5a2a" transform="rotate(18 81 57)"/>') + lines('<rect x="78" y="40" width="7" height="34" rx="2" transform="rotate(18 81 57)" stroke-width="1.6"/>', boil=False))
    bowl = 'M-46 -30 Q-44 0 0 2 Q44 0 46 -30Z'
    ic['punches'] = (at(60, 100, wash(f'<path d="{bowl}" fill="#e7f1fb" opacity=".5"/><path d="M-44 -22 Q-40 0 0 1 Q40 0 44 -22Z" fill="#e8737a"/>') + lines(f'<path d="{bowl}" stroke-width="2.2"/><path d="M-20 2 L-14 14 L14 14 L20 2" stroke-width="2.2"/>', boil=False)
                             + at(-20, -24, wheel('orange', 7)) + at(6, -22, wheel('lemon', 6.5)) + at(28, -25, wheel('lime', 6)), 1.15)
                     + lines('<path d="M86 66 L104 18 M104 18 q6 -4 8 2" stroke="#a9a29a" stroke-width="3"/>', boil=False))
    return ic


# ---------------------------------------------------------------- the Classics' hero: Phil behind the bar, the drinks lined up
def classics_hero():
    COUNTER = 146
    colors = ['#c98a3c', '#a0522d', '#7f9a6c', '#e6d3bd', '#b9792c', '#c0583c', '#e7f1fb', '#8a6a3c', '#c98a3c', '#7f9a6c', '#a0522d', '#d8c3a5', '#b9792c', '#c0583c']
    wall = wash('<rect x="0" y="0" width="400" height="236" fill="#6f5443"/><rect x="40" y="10" width="320" height="140" fill="#cfe0dc" opacity=".55"/>')
    shelf = lambda y: wash(f'<rect x="40" y="{y}" width="320" height="4" fill="#bfe3dc" opacity=".9"/>') + lines(f'<path d="M40 {y} H360 M40 {y + 4} H360" stroke="#6aa59a" stroke-width="1.6"/>', boil=False)
    backbar = (wall + shelf(56) + ''.join(plain_bottle(52 + i * 22.5, 56, (34, 40, 30, 38, 42, 32, 36)[i % 7], colors[i % 14]) for i in range(14))
               + shelf(102) + ''.join(plain_bottle(56 + i * 24, 102, (30, 36, 40, 32, 38)[i % 5], colors[(i + 5) % 14]) for i in range(13)))
    counter = ('<rect x="0" y="146" width="400" height="90" fill="#6e4b39"/>'
               + wash('<rect x="0" y="146" width="400" height="12" fill="#5a3e2e"/><rect x="0" y="158" width="400" height="78" fill="#7a5340"/>')
               + lines('<path d="M0 146 H400 M0 158 H400"/>' + ''.join(f'<rect x="{x}" y="170" width="70" height="52" rx="2" stroke-width="1.8"/>' for x in (20, 116, 212, 308)), boil=False, width=2.2))
    p = bartender(eyes='happy', mood='grin', parts=True, arm_l=[(-23, -110), (-50, -112), (-66, -130)], arm_r=[(23, -110), (50, -112), (66, -130)])
    phil = p['body'] + p['head'] + f'<g class="ta-da" style="transform-origin:-23px -110px">{p["left"]}</g>' + f'<g class="ta-da r" style="transform-origin:23px -110px">{p["right"]}</g>'
    lineup = [('coupe', 'daiquiri', 106, .5), ('martini', 'martini', 136, .46), ('rocks', 'old-fashioned', 200, .5), ('highball', 'tom-collins', 264, .44), ('flute', 'french-75', 292, .44)]
    drinks = ''
    for kind, slug, x, s in lineup:
        d = BY_SLUG[slug]
        iced = kind in ('rocks', 'highball')
        drinks += f'<g transform="translate({x} {COUNTER}) scale({s})">{glass(kind, "cl-" + slug, d["color"], d["garnish"], iced=iced, top=d.get("level"))}</g>'
    sp = sparkle(96, 40, 6, 'twinkle') + sparkle(306, 36, 5.5, 'twinkle d2') + sparkle(330, 90, 4, 'twinkle d3') + sparkle(70, 96, 4.4, 'twinkle d2')
    return svg_view(backbar + place(phil, 200, 206) + counter + drinks + sp,
                    'Phil, the bartender, throws his arms wide behind his bar. Lined up on the bar in front of him: a Daiquiri, a Martini, an Old Fashioned, a Tom Collins and a French 75',
                    '84 28 232 152')


def classics_lineup():
    """The Classics page: five of them lined up on the bar, close up."""
    COUNTER = 150
    colors = ['#c98a3c', '#a0522d', '#7f9a6c', '#e6d3bd', '#b9792c', '#c0583c', '#e7f1fb', '#8a6a3c', '#c98a3c', '#7f9a6c', '#a0522d', '#d8c3a5', '#b9792c', '#c0583c']
    wall = wash('<rect x="0" y="0" width="400" height="236" fill="#6f5443"/><rect x="40" y="10" width="320" height="140" fill="#cfe0dc" opacity=".55"/>')
    shelf = lambda y: wash(f'<rect x="40" y="{y}" width="320" height="4" fill="#bfe3dc" opacity=".9"/>') + lines(f'<path d="M40 {y} H360 M40 {y + 4} H360" stroke="#6aa59a" stroke-width="1.6"/>', boil=False)
    backbar = (wall + shelf(56) + ''.join(plain_bottle(52 + i * 22.5, 56, (34, 40, 30, 38, 42, 32, 36)[i % 7], colors[i % 14]) for i in range(14))
               + shelf(102) + ''.join(plain_bottle(56 + i * 24, 102, (30, 36, 40, 32, 38)[i % 5], colors[(i + 5) % 14]) for i in range(13)))
    lineup = [('coupe', 'daiquiri', 108, .84), ('martini', 'martini', 157, .78), ('rocks', 'negroni', 206, .86), ('highball', 'tom-collins', 254, .76), ('flute', 'french-75', 294, .76)]
    drinks = ''
    for kind, slug, x, sc in lineup:
        d = BY_SLUG[slug]
        drinks += f'<g transform="translate({x} {COUNTER}) scale({sc})">{glass(kind, "cl-" + slug, d["color"], d["garnish"], iced=kind in ("rocks", "highball"), top=d.get("level"))}</g>'
    sp = sparkle(96, 52, 6, 'twinkle') + sparkle(318, 44, 5.5, 'twinkle d2') + sparkle(226, 40, 4.5, 'twinkle d3')
    return svg_view(backbar + countertop(COUNTER) + drinks + sp,
                    'Five classics lined up on the bar: a Daiquiri, a Martini, a Negroni, a Tom Collins and a French 75', '76 34 248 150')


def search_index():
    """What the menu's search looks through, for each drink: its name, what's in it (shown under the name),
    and words people might type instead (whiskey for bourbon, brandy for cognac, bubbly for Champagne)."""
    FAMILY = {'bourbon': 'whiskey whisky', 'rye': 'whiskey whisky', 'scotch': 'whiskey whisky', 'cognac': 'brandy', 'applejack': 'brandy apple',
              'champagne': 'sparkling wine bubbly', 'campari': 'bitter aperitivo amaro', 'soda water': 'club soda bubbles', 'egg white': 'foam',
              'ginger beer': 'ginger', 'grapefruit soda': 'grapefruit bubbles', 'honey syrup': 'honey', 'crème de cassis': 'blackcurrant',
              'crème de violette': 'violet floral', 'orange liqueur': 'triple sec cointreau curacao', 'sweet vermouth': 'vermouth', 'dry vermouth': 'vermouth',
              'angostura bitters': 'bitters', "peychaud's bitters": 'bitters', 'orange bitters': 'bitters'}
    out = []
    for d in DRINKS:
        ings = []
        for q, u, text in d['recipe']:
            name = re.sub(r'\s*\(.*?\)', '', text).strip() or u
            name = re.sub(r', or another .*$', '', name)
            ings.append(html.unescape(name))
        extra = []
        for i in ings:
            for k, v in FAMILY.items():
                if k in i.lower():
                    extra.append(v)
        acts = [a for _, acts in d['steps'] for a in acts]
        if any(a[0] in ('shake', 'dry') for a in acts):
            method = 'shaken'
        elif any(a[0] == 'strain' for a in acts) or (any(a[0] == 'stir' for a in acts) and not any(a[0] == 'top' for a in acts)):
            method = 'stirred'          # in a mixing glass, or (the Old Fashioned) right in the glass
        else:
            method = 'built'            # poured over ice and topped up, maybe a quick stir
        part = html.unescape(GENRE_NAME[genre(d)]).lower()
        words = ' '.join(extra + [d['glass_line'][0], d['glass_line'][1], method, d['glass'], part, 'classic' if genre(d) == 'classics' else 'oddity'])
        out.append({'s': d['slug'], 'n': html.unescape(d['name']), 'h': d['slug'] + '/index.html', 'i': ' · '.join(ings), 'k': words})
    return out


# ---------------------------------------------------------------- page writing
def amt(q, u, text):
    qs = f'{q:g}'
    if u == 'oz':
        shown, us = oz_text(q), ''
    elif u == 'dash':
        shown, us = f'{qs} dash' + ('es' if q != 1 else ''), ''
    elif u == '':
        shown, us = qs, ''
    else:
        plural = {'pinch': 'pinches'}.get(u, u + 's')
        shown = f'{qs} {u if q == 1 else plural}'
        us = f' data-us="{plural}"' if plural != u + 's' else ''
    du = f' data-u="{u}"' if u else ''
    return f'<li><span class="amt" data-q="{qs}"{du}{us}>{shown}</span> {text}</li>'


def h1_for(name):
    *first, last = name.split(' ')
    pre = (' '.join(first) + ' ') if first else ''
    return f'<h1><small class="h1-lead">The Cocktail Menu:</small> {pre}<span>{last}.</span></h1>'


LEAD = "Here's how you make one:"   # the line before the recipe card, unless a drink has its own


def drink_story(d):
    s = [h1_for(d['name']), '', '<div class="flow">', '  <figure class="fig" id="s-hero"><div class="sheet"><!--scene:hero--></div></figure>',
         ] + [f'  <p class="punch">{x}</p>' for x in ([d['punch']] if isinstance(d.get('punch'), str) else (d.get('punch') or []))]   # one big line, or a few
    s += [f'  <p class="t">{t}</p>' for t in d['lines']]
    if d.get('gr'):
        gr = d['gr'] if isinstance(d['gr'], list) else [d['gr']]   # one line, or a few short ones
        s += ['  <aside class="note">'] + [f'    <p><em>{g}</em></p>' for g in gr] + [f'    <p class="go"><a href="@page:cocktails-how-to/golden-ratio">{d.get("gr_link", "→ The Golden Ratio")}</a></p>', '  </aside>']
    if d.get('formula'):
        s += [f'  <p class="t">{d["formula"]}</p>']
    s += [f'  <p class="punch">{d.get("lead", LEAD)}</p>',   # in the big display type, like the opener (Philip, Nov 6)
          f'  <section class="recipe-card" aria-label="Recipe: {d["name"]}">',
          f'    <p class="rc-kicker">The Cocktail Menu · {GENRE_NAME[genre(d)]}</p>',
          f'    <p class="rc-name">{d["name"]}</p>',
          '    <p class="rc-serves">Makes <button class="rc-step" type="button" data-d="-1" aria-label="One fewer drink">−</button> <b class="rc-n">1</b> <button class="rc-step" type="button" data-d="1" aria-label="One more drink">+</button> <span class="rc-unit">drink</span></p>',
          '    <ul class="rc-list">']
    s += ['      ' + amt(*r) for r in d['recipe']]
    gl, gn = d['glass_line']
    s += ['    </ul>', f'    <p class="rc-glass"><b>Glass:</b> {gl} · <b>Garnish:</b> {gn}</p>']
    if d.get('note'):
        s += [f'    <p class="rc-note">{d["note"]}</p>']
    s += ['  </section>', '  <figure class="fig howto" id="s-build"><div class="sheet"><!--scene:build--></div>', '    <figcaption><ol class="steps howto-steps">']
    s += [f'      <li class="s{i}">{t}</li>' for i, (t, _) in enumerate(d['steps'], 1)]
    s += ['    </ol></figcaption>', '  </figure>']
    if d.get('tip'):
        s += [f'  <p class="t">{d["tip"]}</p>']
    s += ['', '  <nav class="end-doors" aria-label="Where next">', '    <h2>Keep exploring</h2>']
    for r in d['related']:
        s += [f'    <p class="go"><a href="../{r}/index.html">→ {BY_SLUG[r]["name"]}</a></p>']
    for slug, label in d.get('extra', []):
        s += [f'    <p class="go"><a href="@page:{slug}">→ {label}</a></p>']
    s += [f'    <p class="back"><a href="../{genre(d)}/index.html" data-back>← Back to {GENRE_NAME[genre(d)]}</a></p>', '  </nav>', '</div>', '']
    return '\n'.join(s)


def copy_lines(story):
    """The page's words, one line each, with Philip's markdown for emphasis."""
    md = story.replace('<strong>', '**').replace('</strong>', '**').replace('<em>', '*').replace('</em>', '*')
    md = re.sub(r'(<h1>.*?)<span>(.*?)</span>', r'\1***\2***', md, flags=re.S)
    md = re.sub(r'<b>(Glass:|Garnish:)</b>', r'**\1**', md)
    return page_words(md)


def write_copy(path, title, story, note):
    lines = copy_lines(story)
    path.write_text(f'# {title}: copy\n\n# One line per line of text on the page, in order. Illustrations are not included\n'
                    '# (words written under one, like the how-to steps, are).\n# The build refuses to publish the page if its words drift from this file.\n'
                    f'# {note}\n\n' + '\n'.join(lines) + '\n')


def write_drink(d):
    folder = MENU / d['slug']
    (folder / 'scenes').mkdir(parents=True, exist_ok=True)
    d = dict(d)
    d['build_alt'] = f'How to make {a_an(d["name"])}, step by step: ' + ' '.join(re.sub(r'<[^>]+>', '', t) for t, _ in d['steps']) + ' Cheers!'
    b = Build(d)
    (folder / 'scenes' / 'build.svg').write_text(b.scene() + '\n')
    (folder / 'scenes' / 'hero.svg').write_text(hero(d) + '\n')
    story = drink_story(d)
    (folder / 'story.html').write_text(story)
    write_copy(folder / 'copy.md', f'The Cocktail Menu / {html.unescape(d["name"])}', story,
               d.get('copy_note', "Nov 1 2026: CLAUDE'S DRAFT, waiting on Philip: the recipe, every line, and the steps.") + ' Written by tools/art/menu_pages.py from tools/art/menu_drinks.py.')
    (folder / 'page.json').write_text(json.dumps({
        'title': f'{html.unescape(d["name"])} · The Cocktail Menu · The Bottle and the Bartender',
        'description': f'How to make {a_an(html.unescape(d["name"]))}: the recipe, a step-by-step how-to, and a little history.',
        'label': f'The Cocktail Menu / {html.unescape(d["name"])}'}, indent=2, ensure_ascii=False) + '\n')
    (folder / 'page.css').write_text(f'/* The Cocktail Menu / {html.unescape(d["name"])}: scene motion. Written by tools/art/menu_pages.py; edit it there. */\n'
                                     + TWINKLE_CSS + '\n' + BUBBLE_CSS + '\n' + b.page_css() + '\n')
    return b.T


def write_menu():
    """The Cocktail Menu (the hub): Phil's lineup, "What'll it be?", a search, and a door per part of the menu."""
    (MENU / 'scenes').mkdir(parents=True, exist_ok=True)
    old = MENU / 'scenes' / 'classics.svg'
    if old.exists():
        old.unlink()
    (MENU / 'scenes' / 'menu.svg').write_text(classics_hero() + '\n')
    icons = {f'{d["slug"]}-icon': icon(d) for d in DRINKS}
    icons.update({f'{k}-icon': v for k, v in soon_icons().items()})
    icons['classics-icon'] = (at(30, 108, glass('martini', 'clx-m', BY_SLUG['martini']['color'], ['olives']), .72) + at(62, 110, glass('rocks', 'clx-r', BY_SLUG['old-fashioned']['color'], ['orange-peel'], iced=True, top=-44), .78)
                              + at(94, 108, glass('coupe', 'clx-c', BY_SLUG['daiquiri']['color'], ['lime-wheel']), .82) + sparkle(18, 30, 5) + sparkle(104, 24, 6))
    (MENU / 'cast.svg').write_text('    <!-- The Cocktail Menu: door icons (the hub, Classics and every drink page share them) -->\n'
                                   + ''.join(f'    <symbol id="{k}" viewBox="0 0 120 120">{v}</symbol>\n' for k, v in icons.items()))
    index = html.escape(json.dumps(search_index(), ensure_ascii=False), quote=True)
    live = {genre(d) for d in DRINKS}
    soon = [(f'    <a class="door" href="{k}/index.html"><svg class="door-icon" aria-hidden="true"><use href="#{k}-icon"/></svg><span class="door-label">{label}</span></a>' if k in live else
             f'    <div class="door soon" aria-disabled="true"><svg class="door-icon" aria-hidden="true"><use href="#{k}-icon"/></svg><span class="door-label">{label}</span><span class="stamp">Coming soon</span></div>')
            for k, label in SOON]
    story = '\n'.join([
        '<h1>The Cocktail <span>Menu.</span></h1>', '',
        '<div class="flow">',
        '  <figure class="fig" id="s-menu"><div class="sheet"><!--scene:menu--></div></figure>',
        "  <p class=\"punch\">What'll it be?</p>",
        f'  <form class="search" role="search" data-search="{index}" data-none="Nothing on the menu like that yet. Try a drink, or just one ingredient.">',
        '    <label for="menu-q">Looking for something?</label>',
        '    <input id="menu-q" type="search" placeholder="Try “Negroni” or “Old Fashioned”" autocomplete="off" enterkeyhint="go">',
        '    <p class="search-count" aria-live="polite"></p>',
        '    <ul class="search-results"></ul>',
        '  </form>', '',
        '  <nav class="doors" aria-label="The menu">',
        '    <a class="door wide" href="classics/index.html"><svg class="door-icon" aria-hidden="true"><use href="#classics-icon"/></svg><span class="door-text"><span class="door-label">Classics</span></span></a>'] + soon + ['  </nav>', '',
        '  <nav class="end-doors" aria-label="Where next">',
        '    <p class="back"><a href="@home" data-back>← Back to The Bar</a></p>',
        '  </nav>', '</div>', ''])
    (MENU / 'story.html').write_text(story)
    write_copy(MENU / 'copy.md', 'The Cocktail Menu', story,
               "Nov 3 2026: the menu's front door (Philip: Classics is its own door, like the rest; and a search). \"What'll it be?\" is Philip's (moved here from Classics). "
               "CLAUDE'S DRAFT, waiting on Philip: \"Looking for something?\" (and, not checked here because they aren't page text: the search box's hint, "
               "\"Try “Negroni” or “Old Fashioned”\", and its no-match line, \"Nothing on the menu like that yet. Try a drink, or just one ingredient.\"), and the genres' working titles.")
    (MENU / 'page.json').write_text(json.dumps({
        'title': 'The Cocktail Menu · The Bottle and the Bartender',
        'description': "What'll it be? Search the menu, or start with the Classics.",
        'label': 'The Cocktail Menu'}, indent=2, ensure_ascii=False) + '\n')
    (MENU / 'page.css').write_text('/* The Cocktail Menu: scene motion. Written by tools/art/menu_pages.py; edit it there. */\n' + TWINKLE_CSS + '\n'
                                   '.ta-da{animation:ta-da 1.5s ease-in-out infinite alternate}.ta-da.r{animation-delay:-.75s}\n'
                                   '@keyframes ta-da{from{transform:rotate(-6deg)}to{transform:rotate(6deg)}}\n'
                                   '.flow .doors .door-icon{width:96px;height:96px}.flow .doors .door.wide .door-icon{width:96px;height:96px}\n')
    write_classics()
    write_oddities()


def write_classics():
    """Classics: Philip's 19, a door each."""
    C = MENU / 'classics'
    (C / 'scenes').mkdir(parents=True, exist_ok=True)
    (C / 'scenes' / 'classics.svg').write_text(classics_lineup() + '\n')
    doors = []
    mine = [d for d in DRINKS if genre(d) == 'classics']
    for i, d in enumerate(mine):
        wide = i == len(mine) - 1 and len(mine) % 2
        if wide:
            doors.append(f'    <a class="door wide" href="../{d["slug"]}/index.html"><svg class="door-icon" aria-hidden="true"><use href="#{d["slug"]}-icon"/></svg><span class="door-text"><span class="door-label">{d["name"]}</span></span></a>')
        else:
            doors.append(f'    <a class="door" href="../{d["slug"]}/index.html"><svg class="door-icon" aria-hidden="true"><use href="#{d["slug"]}-icon"/></svg><span class="door-label">{d["name"]}</span></a>')
    story = '\n'.join([
        '<h1><small class="h1-lead">The Cocktail Menu:</small> <span>Classics.</span></h1>', '',
        '<div class="flow">',
        '  <figure class="fig" id="s-classics"><div class="sheet"><!--scene:classics--></div></figure>',
        '  <p class="t">These are the <em>Classics.</em></p>',
        '  <p class="t">Tap any drink for its recipe and step-by-step, animated how-to.</p>',
        '  <aside class="note">',
        '    <p><em>New to mixing drinks?</em></p>',
        '    <p class="go"><a href="@page:cocktails-how-to">Check out our tips and tricks page for all the cocktail basics you need →</a></p>',
        '  </aside>', '',
        '  <nav class="doors" aria-label="The Classics">'] + doors + ['  </nav>', '',
        '  <nav class="end-doors" aria-label="Where next">',
        '    <p class="back"><a href="../index.html">← Back to the Cocktail Menu</a></p>',
        '  </nav>', '</div>', ''])
    (C / 'story.html').write_text(story)
    write_copy(C / 'copy.md', 'The Cocktail Menu / Classics', story,
               "Nov 3 2026: Philip's copy from chat: the intro (third round), and the note (it goes to Cocktails How-To; the Golden Ratio is one step of many). "
               "The drink list is Philip's (his Classics, Oct 31). Claude's: \"← Back to the Cocktail Menu\".")
    (C / 'page.json').write_text(json.dumps({
        'title': 'Classics · The Cocktail Menu · The Bottle and the Bartender',
        'description': 'The classic cocktails, each with its recipe and a step-by-step how-to.',
        'label': 'The Cocktail Menu / Classics'}, indent=2, ensure_ascii=False) + '\n')
    (C / 'page.css').write_text('/* The Cocktail Menu / Classics: scene motion. Written by tools/art/menu_pages.py; edit it there. */\n' + TWINKLE_CSS + '\n'
                                '/* the drinks are the point of this page: bigger pictures on the doors */\n'
                                '.flow .doors .door-icon{width:104px;height:104px}.flow .doors .door.wide .door-icon{width:96px;height:96px}\n'
                                '.flow .doors .door{min-height:10.5rem}\n')



def oddities_scene():
    """Arcane Oddities: a dark back bar under a crescent moon, odd bottles on the shelf, the Dark and Stormy out front."""
    COUNTER = 168
    wall = wash('<rect x="0" y="0" width="400" height="236" fill="#3b2a45"/><rect x="40" y="10" width="320" height="150" fill="#5a4468" opacity=".45"/>')
    shelf = wash('<rect x="40" y="96" width="320" height="4" fill="#8f7aa3"/>') + lines('<path d="M40 96 H360 M40 100 H360" stroke="#b9a3c8" stroke-width="1.6"/>', boil=False)
    potion = 'M-14 0 Q-24 -2 -22 -20 Q-20 -34 -6 -38 L-6 -52 L6 -52 L6 -38 Q20 -34 22 -20 Q24 -2 14 0Z'
    odd = (at(98, 96, wash(f'<path d="{potion}" fill="#6b4a8a"/><path d="M-18 -18 Q0 -10 18 -18 Q20 -6 12 -2 L-12 -2 Q-20 -6 -18 -18Z" fill="#7fd1b9" opacity=".8"/><rect x="-8" y="-60" width="16" height="9" rx="2" fill="#9b7663"/>')
               + lines(f'<path d="{potion}" stroke="#d9c7e6" stroke-width="2"/><rect x="-8" y="-60" width="16" height="9" rx="2" stroke="#d9c7e6" stroke-width="1.6"/>', boil=False), .9)
           + at(136, 96, bottle('wine', '#2f4a3a', '?'), .62) + at(268, 96, bottle('liqueur', '#7a2d4a', '?'), .66) + at(302, 96, bottle('tall', '#2f3f5a', '?'), .6))
    moon = lines('<path d="M318 30 a16 16 0 1 0 16 22 a12 12 0 1 1 -16 -22Z" fill="#f2c776" stroke="#f2c776"/>', boil=False)
    stars = (sparkle(70, 30, 4, 'twinkle') + sparkle(170, 22, 3.4, 'twinkle d2') + sparkle(230, 44, 4.4, 'twinkle d3') + sparkle(288, 70, 3.2, 'twinkle')
             + sparkle(120, 58, 3, 'twinkle d3'))
    d = BY_SLUG['dark-and-stormy']
    drink = f'<g transform="translate(205 {COUNTER}) scale(1.05)">{glass("highball", "odd-ds", d["color"], d["garnish"], iced=True, layers=[(.68, 1, "#5a2e14")], bubbles=True)}</g>'
    return svg_view(wall + moon + stars + shelf + odd + countertop(COUNTER) + drink,
                    'A dark back bar under a crescent moon and twinkling stars. Odd bottles line the shelf, one a round purple potion bottle. '
                    'Out front on the bar: a Dark and Stormy, dark rum floating over ginger beer', '62 14 276 174')


def write_oddities():
    """Arcane Oddities: the odd ones (so far, the Dark and Stormy), a door each, and room for more."""
    C = MENU / 'arcane-oddities'
    (C / 'scenes').mkdir(parents=True, exist_ok=True)
    (C / 'scenes' / 'oddities.svg').write_text(oddities_scene() + '\n')
    mine = [d for d in DRINKS if genre(d) == 'arcane-oddities']
    doors = [f'    <a class="door" href="../{d["slug"]}/index.html"><svg class="door-icon" aria-hidden="true"><use href="#{d["slug"]}-icon"/></svg><span class="door-label">{d["name"]}</span></a>' for d in mine]
    if len(mine) % 2:   # an odd number of oddities: the last spot is a promise
        doors.append('    <div class="door soon" aria-disabled="true"><svg class="door-icon" aria-hidden="true"><use href="#arcane-oddities-icon"/></svg><span class="door-label">More oddities</span><span class="stamp">Coming soon</span></div>')
    story = '\n'.join([
        '<h1><small class="h1-lead">The Cocktail Menu:</small> Arcane <span>Oddities.</span></h1>', '',
        '<div class="flow">',
        '  <figure class="fig" id="s-oddities"><div class="sheet"><!--scene:oddities--></div></figure>',
        '  <p class="t">These are the <em>Arcane Oddities.</em></p>',
        '  <p class="t">Tap any drink for its recipe and step-by-step, animated how-to.</p>', '',
        '  <nav class="doors" aria-label="The Arcane Oddities">'] + doors + ['  </nav>', '',
        '  <nav class="end-doors" aria-label="Where next">',
        '    <p class="back"><a href="../index.html">← Back to the Cocktail Menu</a></p>',
        '  </nav>', '</div>', ''])
    (C / 'story.html').write_text(story)
    write_copy(C / 'copy.md', 'The Cocktail Menu / Arcane Oddities', story,
               "Nov 3 2026: Philip moved the Dark and Stormy here, so Arcane Oddities opened. CLAUDE'S DRAFT, waiting on Philip: the page follows Classics "
               "(\"These are the *Arcane Oddities.*\"; \"Tap any drink...\" is Philip's line from Classics), and \"More oddities\".")
    (C / 'page.json').write_text(json.dumps({
        'title': 'Arcane Oddities · The Cocktail Menu · The Bottle and the Bartender',
        'description': 'The odd ones on the menu, each with its recipe and a step-by-step how-to.',
        'label': 'The Cocktail Menu / Arcane Oddities'}, indent=2, ensure_ascii=False) + '\n')
    (C / 'page.css').write_text('/* The Cocktail Menu / Arcane Oddities: scene motion. Written by tools/art/menu_pages.py; edit it there. */\n' + TWINKLE_CSS + '\n' + BUBBLE_CSS + '\n'
                                '.flow .doors .door-icon{width:104px;height:104px}\n.flow .doors .door{min-height:10.5rem}\n')

if __name__ == '__main__':
    write_menu()
    for d in DRINKS:
        if d['slug'] in REWRITE:
            print(f'{d["slug"]}: {write_drink(d):g} s build')
