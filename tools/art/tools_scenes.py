"""Cocktail Basics and How-To's / The Tools You Actually Need: the hero (the five tools on the bar) and a drawing of each tool for its card.

    python3 tools/art/tools_scenes.py

Writes src/pages/cocktails-how-to/tools/scenes/bartop.svg, the page's cast.svg (one symbol per tool, 120 x 120) and page.css.
The hub's door icon for this page (a jigger, a bar spoon and a strainer) is drawn in howto_scenes.py.
"""
import pathlib
from art import *
from menu_art import at, TWINKLE_CSS

REPO = pathlib.Path(__file__).resolve().parents[2]
D = REPO / 'src/pages/cocktails-how-to/tools'
(D / 'scenes').mkdir(parents=True, exist_ok=True)

STEEL, STEEL_DARK, SHINE = '#c9c3b8', '#8a8f96', '#f4f4f2'


# ---------------------------------------------------------------- the tools (each standing or resting at 0, 0)
def jigger():
    """A Japanese-style jigger: a small cup over a big one, with lines inside the big one for the quarter ounces."""
    d = 'M-12 -84 L12 -84 L3.5 -50 L16 0 L-16 0 L-3.5 -50Z'
    ticks = ''.join(f'<path d="M{-(3.5 + 12.5 * (y + 50) / 50) + 3.5:.1f} {y} H{(3.5 + 12.5 * (y + 50) / 50) - 3.5:.1f}"/>' for y in (-12, -22, -32))
    return (wash(f'<path d="{d}" fill="{STEEL}"/>')
            + lines(ticks, boil=False, color=STEEL_DARK, width=1.4)
            + lines(f'<path d="{d}" stroke-width="2"/><path d="M-3.5 -50 H3.5" stroke-width="1.6"/><path d="M-8 -78 L-4 -56" stroke="{SHINE}" stroke-width="2.2"/>', boil=False))


def bar_spoon(h=104):
    """A long bar spoon: a little bowl at the bottom, a twisted handle, a teardrop weight on top."""
    twists = ''.join(f'<path d="M-2.2 -{y} l4.4 2.4"/>' for y in range(12, h - 10, 6))
    return (wash(f'<rect x="-2" y="-{h}" width="4" height="{h - 2}" fill="{STEEL}"/>')
            + lines(twists, boil=False, color=STEEL_DARK, width=1.2)
            + lines(f'<rect x="-2" y="-{h}" width="4" height="{h - 2}" stroke-width="1.3"/>', boil=False)
            + wash(f'<path d="M0 -{h + 12} Q5 -{h + 4} 0 -{h - 1} Q-5 -{h + 4} 0 -{h + 12}Z" fill="{STEEL}"/><ellipse cx="0" cy="3" rx="4.6" ry="7" fill="{STEEL}"/>')
            + lines(f'<path d="M0 -{h + 12} Q5 -{h + 4} 0 -{h - 1} Q-5 -{h + 4} 0 -{h + 12}Z" stroke-width="1.6"/><ellipse cx="0" cy="3" rx="4.6" ry="7" stroke-width="1.6"/>', boil=False))


def strainer(flat=1.0):
    """A Hawthorne strainer from above: a round plate with holes, the spring coiled around its edge, a handle.
    flat < 1 squashes it, lying on the bar."""
    import math
    coil = ''.join(f'<circle cx="{math.cos(a) * 25:.1f}" cy="{math.sin(a) * 25:.1f}" r="3.2"/>' for a in [math.radians(t) for t in range(25, 340, 15)])
    holes = ''.join(f'<circle cx="{x}" cy="{y}" r="1.6"/>' for x, y in ((-10, -6), (0, -10), (10, -6), (-12, 5), (0, 0), (12, 5), (-5, 12), (6, 12)))
    inner = (wash(f'<circle cx="0" cy="0" r="24" fill="{STEEL}"/><rect x="22" y="-4.5" width="38" height="9" rx="4.5" fill="{STEEL}"/>'
                  '<path d="M-6 -24 l-4 -9 h8Z M6 -24 l4 -9 h-8Z" fill="#c9c3b8"/>')
             + lines(holes, boil=False, color=STEEL_DARK, width=1.2)
             + lines(coil, boil=False, color='#7d8288', width=1.4)
             + lines('<circle cx="0" cy="0" r="24" stroke-width="2"/><rect x="22" y="-4.5" width="38" height="9" rx="4.5" stroke-width="1.8"/>'
                     '<path d="M-6 -24 l-4 -9 h8Z M6 -24 l4 -9 h-8Z" stroke-width="1.4"/><path d="M-14 -14 q6 -6 13 -7" stroke="' + SHINE + '" stroke-width="2.2"/>', boil=False))
    return f'<g transform="scale(1 {flat:g})">{inner}</g>' if flat != 1 else inner


def mixing_glass(spoon=True):
    """A heavy mixing glass with a spout and cut sides, a stirred drink and ice inside, the bar spoon standing in it."""
    d = 'M-25 -62 L25 -62 L23 0 L-23 0Z'
    spout = 'M-25 -62 L-32 -66 L-26 -56'
    s = at(8, -14, bar_spoon(96), 1, 9) if spoon else ''
    return (wash(f'<path d="{d}" fill="#e7f1fb" opacity=".75"/><path d="M-24.3 -34 L24.3 -34 L23 -7 L-23 -7Z" fill="#c98a3c"/>'
                 '<rect x="-16" y="-44" width="14" height="13" rx="2.5" fill="#f4fbff" opacity=".85"/><rect x="2" y="-40" width="13" height="12" rx="2.5" fill="#f4fbff" opacity=".85"/>'
                 '<path d="M-23 -7 L23 -7 L23 0 L-23 0Z" fill="#cfe0ea"/>')
            + s
            + lines('<rect x="-16" y="-44" width="14" height="13" rx="2.5"/><rect x="2" y="-40" width="13" height="12" rx="2.5"/>', boil=False, color='#8ecae6', width=1.3)
            + lines('<path d="M-12 -60 L-11 -9 M0 -60 V-9 M12 -60 L11 -9"/>', boil=False, color='#a9c3d3', width=1.3)
            + lines(f'<path d="{d}" stroke-width="2"/><path d="{spout}" stroke-width="2"/><path d="M-23 -7 H23" stroke-width="1.4"/>', boil=False))


def tins():
    """A two-piece shaker: a big tin with the small tin sealed in it upside down, at a slight angle."""
    big = 'M-14 0 L-18 -56 L18 -56 L14 0Z'
    small = 'M-13 0 L-10.5 -40 L10.5 -40 L13 0Z'   # mouth down at 0
    return (wash(f'<path d="{big}" fill="{STEEL}"/>')
            + lines(f'<path d="{big}" stroke-width="2"/><path d="M-11 -50 L-9 -8" stroke="{SHINE}" stroke-width="2.6"/>', boil=False)
            + at(2, -46, wash(f'<path d="{small}" fill="#d8d3cb"/>') + lines(f'<path d="{small}" stroke-width="2"/><path d="M-6 -34 L-5 -6" stroke="{SHINE}" stroke-width="2.2"/>', boil=False), 1, 7))


# ---------------------------------------------------------------- a drawing per card (120 x 120, like the hub's door icons)
icons = {
    'tool-jigger': at(60, 112, jigger(), 1.22),
    'tool-spoon': at(40, 112, bar_spoon(88), 1.05, 32),
    'tool-strainer': at(44, 62, strainer(), 1.25, -18),
    'tool-mixing-glass': at(62, 114, mixing_glass(), 1.3),
    'tool-tins': at(58, 116, tins(), 1.18),
}
(D / 'cast.svg').write_text("    <!-- The Tools You Actually Need: a drawing of each tool, for its card -->\n"
                            + ''.join(f'    <symbol id="{k}" viewBox="0 0 120 120">{v}</symbol>\n' for k, v in icons.items()))

# ---------------------------------------------------------------- the hero: all five on the bar
bar = wash('<rect x="0" y="0" width="400" height="236" fill="#efe3d0"/><rect x="0" y="178" width="400" height="58" fill="#7a5340"/>') + lines('<path d="M0 178 H400"/>', boil=False)
hero = (bar
        + at(84, 178, tins(), 1.45)
        + at(160, 178, mixing_glass(), 1.3)
        + at(228, 178, jigger(), .95)
        + at(284, 186, strainer(.42), 1.15, -6)
        + sparkle(52, 52, 7, 'twinkle') + sparkle(222, 46, 6, 'twinkle d2') + sparkle(338, 70, 6, 'twinkle d3'))
label = ('The five tools on the bar: a two-piece shaker tin, a mixing glass with a stirred drink and a bar spoon in it, '
         'a jigger, and a Hawthorne strainer lying flat.')
(D / 'scenes' / 'bartop.svg').write_text(svg_view(hero, label, '30 20 340 196') + '\n')

CSS = [
    "/* Cocktail Basics and How-To's / The Tools You Actually Need. Written by tools/art/tools_scenes.py; edit it there. */",
    TWINKLE_CSS,
    '/* a tool card: the recipe card, with the tool drawn in its top corner */',
    '.tool-card{display:flow-root;scroll-margin-top:5rem}',
    '.tool-pic{float:right;width:5.4rem;height:5.4rem;margin:.1rem -.2rem .2rem .5rem}',
    '.tool-card .rc-glass{line-height:28px}',
]
(D / 'page.css').write_text('\n'.join(CSS) + '\n')
print('wrote', D / 'scenes' / 'bartop.svg', 'cast.svg and page.css')
