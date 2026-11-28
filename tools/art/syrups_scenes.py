"""Cocktail Basics and How-To's / Homemade Syrups: the hero (a pot on the stove, and the bottles it fills).

    python3 tools/art/syrups_scenes.py

Writes src/pages/cocktails-how-to/syrups/scenes/kitchen.svg and the page's page.css (the scene's motion, and the syrup cards).
The hub's door icon for this page (a syrup bottle and two sugar cubes) is drawn in howto_scenes.py.
"""
import pathlib
from art import *
from menu_art import at, label_text, steam, STEAM_CSS, TWINKLE_CSS

REPO = pathlib.Path(__file__).resolve().parents[2]
D = REPO / 'src/pages/cocktails-how-to/syrups'
(D / 'scenes').mkdir(parents=True, exist_ok=True)

# the syrups' colors, as the drink pages pour them (menu_art.ING)
SYRUPS = [('simple', '#f3e9c4'), ('demerara', '#d9a65a'), ('honey', '#e9b949'), ('honey ginger', '#e2b452'),
          ('grenadine', '#b3202a'), ('passion fruit', '#f0a83c'), ('orgeat', '#f0e3c8')]


def syrup_bottle(word, color):
    """A swing-top bottle of syrup, base at (0, 0), its label saying what's in it."""
    body = 'M-14 0 L-14 -30 Q-14 -37 -6 -39 L-5 -48 L5 -48 L6 -39 Q14 -37 14 -30 L14 0Z'
    neck = 'M-5 -48 L5 -48 L6 -39 L-6 -39Z'
    cap = 'M-5.5 -54 h11 v6 h-11Z'
    return (wash(f'<path d="{body}" fill="{color}"/><path d="{neck}" fill="#eef4f6" opacity=".85"/><path d="{cap}" fill="#f4efe6"/>'
                 '<rect x="-12.5" y="-28" width="25" height="19" rx="1.6" fill="#fbf3e3"/>')
            + lines(f'<path d="{body}" stroke-width="2"/><path d="{cap}" stroke-width="1.5"/><path d="M-6 -39 H6" stroke-width="1.2"/>'
                    '<rect x="-12.5" y="-28" width="25" height="19" rx="1.6" stroke-width="1.4"/><path d="M-10 -33 q-1 -4 3 -6" stroke="#ffffff" stroke-width="1.8"/>', boil=False)
            + label_text(word, 25, -28, 19))


def pot():
    """A saucepan on a burner, its handle to the left, a wooden spoon stirring (class "stir"); base at (0, 0)."""
    body = 'M-32 -32 L-30 0 L30 0 L32 -32Z'
    handle = 'M-33 -27 L-74 -33 Q-79 -29 -74 -24 L-33 -19Z'
    burner = 'M-40 0 h80 v7 h-80Z'
    spoon = ('<g class="stir">' + wash('<path d="M6 -28 L33 -86 Q36 -91 40 -88 Q42 -84 38 -82 L11 -26Z" fill="#c28a52"/>')
             + lines('<path d="M6 -28 L33 -86 Q36 -91 40 -88 Q42 -84 38 -82 L11 -26" stroke-width="1.8"/>', boil=False) + '</g>')
    return (spoon
            + wash(f'<path d="{burner}" fill="#3a3030"/><path d="{handle}" fill="#4a3428"/><path d="{body}" fill="#c9c3b8"/>')
            + lines(f'<path d="{burner}" stroke-width="1.6"/><path d="{handle}" stroke-width="1.8"/><path d="{body}" stroke-width="2"/>'
                    '<path d="M-35 -32 H35" stroke-width="2.4"/><path d="M-24 -24 L-22 -6" stroke="#f4f4f2" stroke-width="2.6"/>', boil=False))


def sugar_bag():
    """A paper bag of sugar, folded over at the top; base at (0, 0)."""
    d = 'M-14 0 L-15 -34 L-11 -40 L11 -40 L15 -34 L14 0Z'
    return (wash(f'<path d="{d}" fill="#efe2c4"/><path d="M-15 -34 L15 -34 L11 -40 L-11 -40Z" fill="#e2d1ab"/>')
            + lines(f'<path d="{d}" stroke-width="2"/><path d="M-15 -34 H15" stroke-width="1.4"/>', boil=False)
            + '<text class="letter" x="0" y="-15" font-size="8" text-anchor="middle">sugar</text>')


# ---------------------------------------------------------------- the hero: the kitchen
wall = wash('<rect x="0" y="0" width="400" height="236" fill="#efe3d0"/><rect x="0" y="178" width="400" height="58" fill="#7a5340"/>')
tiles = lines(''.join(f'<path d="M{x} 20 V178"/>' for x in range(30, 190, 32)) + ''.join(f'<path d="M30 {y} H186"/>' for y in range(42, 178, 32)),
              boil=False, color='#dccbb0', width=1.2)
counter = lines('<path d="M0 178 H400"/>', boil=False)
shelf = (wash('<path d="M196 100 H364 V107 H196Z" fill="#9a6a4c"/>')
         + lines('<path d="M196 100 H364 V107 H196Z" stroke-width="1.8"/><path d="M208 107 L208 120 L222 107 M352 107 L352 120 L338 107" stroke-width="1.8"/>', boil=False))
top_row = ''.join(at(x, 100, syrup_bottle(w, c), 1.25) for x, (w, c) in zip((217, 257, 297, 338), SYRUPS[:4]))
bottom_row = ''.join(at(x, 178, syrup_bottle(w, c), 1.35) for x, (w, c) in zip((236, 287, 337), SYRUPS[4:]))
hero = (wall + tiles + counter + shelf + top_row + bottom_row
        + at(108, 171, pot(), 1.15) + at(178, 178, sugar_bag(), 1.1)
        + steam(108, 128, 1.4)
        + sparkle(62, 48, 6, 'twinkle') + sparkle(176, 66, 5, 'twinkle d2') + sparkle(280, 40, 6, 'twinkle d3'))
label = ('A pot of syrup steaming on the stove, a wooden spoon stirring it, and a bag of sugar beside it. '
         'On the shelf and the counter, seven bottles of homemade syrup: simple, demerara, honey, honey ginger, grenadine, passion fruit and orgeat.')
(D / 'scenes' / 'kitchen.svg').write_text(svg_view(hero, label, '30 20 340 196') + '\n')

CSS = [
    "/* Cocktail Basics and How-To's / Homemade Syrups. Written by tools/art/syrups_scenes.py; edit it there. */",
    TWINKLE_CSS,
    STEAM_CSS,
    '/* the spoon stirs the pot */',
    '.stir{transform-box:fill-box;transform-origin:12% 100%;animation:stir 2.4s ease-in-out infinite}',
    '@keyframes stir{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(7deg)}}',
    '/* a syrup card: a recipe card with no drink count; the how-to and the drinks it goes in under the ingredients */',
    '.syrup-card .rc-glass{line-height:28px}',
    '.syrup-card{scroll-margin-top:5rem}',
]
(D / 'page.css').write_text('\n'.join(CSS) + '\n')
print('wrote', D / 'scenes' / 'kitchen.svg', 'and page.css')
