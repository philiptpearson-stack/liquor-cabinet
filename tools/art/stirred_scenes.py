"""Cocktails How-To / Stirred Drinks: the page's three scenes, its motion, and the drink doors it borrows from the menu.

    python3 tools/art/stirred_scenes.py

1. stir      Phil stirs a mixing glass; the chalkboard has the original Cocktail: spirit + sugar + water + bitters.
2. dilution  Stir it cold, then stir longer: the ice shrinks, the drink rises, and that rise is water.
3. dashes    Bitters, counted out: one, two, three, four.
Base styles are each scene's still frame (reduced motion); keyframes carry the motion.
"""
import pathlib, re
from art import *
from menu_art import bottle, bitters, glass, countertop, at, TWINKLE_CSS
from bartender import bartender

REPO = pathlib.Path('/home/claude/liquor-cabinet')
PAGE = REPO / 'src/pages/cocktails-how-to/stirred-drinks'
(PAGE / 'scenes').mkdir(parents=True, exist_ok=True)
CSS = ['/* Cocktails How-To / Stirred Drinks: scene motion. Written by tools/art/stirred_scenes.py; edit it there. */', TWINKLE_CSS.strip()]


def kf(name, stops):
    return f'@keyframes {name}{{' + ''.join(f'{p:g}%{{{c}}}' for p, c in stops) + '}'


def window(name, on, off, fade=.6):
    return kf(name, [(0, 'opacity:0'), (on - fade, 'opacity:0'), (on, 'opacity:1'), (off, 'opacity:1'), (off + fade, 'opacity:0'), (100, 'opacity:0')])


def save(name, inner, label, view):
    (PAGE / 'scenes' / f'{name}.svg').write_text(svg_view(inner, label, view) + '\n')


# the mixing glass, as on the drink pages (menu_build): rim 160-220 at y 96, inside bottom at 189, foot at 196
G_MIX = 'M160 96 L220 96 L214 196 L166 196Z'
G_MIX_IN = 'M162.4 99 L217.6 99 L212.3 189 L167.7 189Z'
MBOT = 189
CUBES = [(169, 171), (186, 172), (200, 170), (167, 154), (184, 155), (201, 153), (170, 137), (187, 138), (202, 136),
         (166, 120), (183, 121), (199, 119), (176, 104), (194, 103)]
AMBER = '#b8742e'


def cube_svg(x, y):
    return (f'<rect x="{x}" y="{y}" width="17" height="17" rx="3" fill="#eef8ff" opacity=".6" stroke="#8ecae6" stroke-width="1.6"/>'
            f'<path d="M{x + 4} {y + 5} h5" stroke="#fffaf1" stroke-width="1.8" stroke-linecap="round"/>')


def mixing_glass(uid, level, cube_cls=None, level_cls=None, h0=None):
    """The glass full of ice, the drink up to `level`. With level_cls, the drink's rect can grow from h0 to its full height."""
    H = MBOT + 1 - level
    origin = f' style="transform-origin:190px {MBOT + 1}px"'
    drink = f'<g class="{level_cls}"{origin}>' if level_cls else '<g>'
    drink += f'<rect x="158" y="{f(level)}" width="64" height="{f(H)}" fill="{AMBER}"/></g>'
    ice = ''.join(f'<g class="{cube_cls}" style="transform-origin:{x + 8.5}px {y + 8.5}px">{cube_svg(x, y)}</g>' if cube_cls else cube_svg(x, y) for x, y in CUBES)
    return (wash(f'<path d="{G_MIX}" fill="#e7f1fb" opacity=".35"/>') + f'<clipPath id="{uid}"><path d="{G_MIX_IN}"/></clipPath>'
            + f'<g clip-path="url(#{uid})"><g filter="url(#wash)">{drink}</g>{ice}</g>'
            + lines(f'<path d="{G_MIX}" stroke-width="2.4"/><path d="M166 189 H214" stroke-width="1.6"/><path d="M167 106 L164 160" stroke="#fffaf1" stroke-width="3"/>', boil=False))


def spoon(cls, bx=204, by=182, top=(222, 70)):
    """A bar spoon standing in the mixing glass, its bowl at (bx, by)."""
    return (f'<g class="{cls}" style="transform-origin:{bx}px {by}px">'
            + lines(f'<path d="M{top[0]} {top[1]} L{bx} {by}" stroke="#a9a29a" stroke-width="3"/><circle cx="{top[0]}" cy="{top[1]}" r="4.2" fill="#c9c3b8"/>'
                    f'<ellipse cx="{bx}" cy="{by + 2}" rx="5" ry="3" fill="#c9c3b8"/>', boil=False, width=2) + '</g>')


def scaled(inner, x, y, s, ox=190, oy=196):
    """Draw something made in the mixing glass's own coordinates with its foot (ox, oy) at (x, y), scaled."""
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(s)}) translate({-ox} {-oy})">{inner}</g>'


# ---------------------------------------------------------------- 1. stir: Phil at work, the original Cocktail on the board
COUNTER = 176
wall = wash('<rect x="0" y="0" width="400" height="236" fill="#6f5443"/>')
board = (wash('<rect x="236" y="22" width="134" height="138" rx="4" fill="#2f3b36"/>') + lines('<rect x="236" y="22" width="134" height="138" rx="4" stroke="#9b7663" stroke-width="6"/>', boil=False)
         + '<text class="letter" x="303" y="50" font-size="17" text-anchor="middle" style="fill:#f2c776">The Cocktail</text>'
         + lines('<path d="M262 58 q41 4 82 0" stroke="#f2c776" stroke-width="1.4"/>', boil=False)
         + ''.join(f'<text class="letter" x="303" y="{y}" font-size="16" text-anchor="middle" style="fill:#f4f1e6">{w}</text>'
                   for y, w in ((80, 'spirit'), (101, '+ sugar'), (122, '+ water'), (143, '+ bitters'))))
GX, GS = 182, .62   # the mixing glass on the bar, a little in front of Phil
ARM_R = [(23, -110), (46, -118), (53, -143)]   # up to the spoon
p = bartender(eyes='happy', mood='grin', parts=True, arm_l=[(-23, -110), (-35, -86), (-27, -62)], arm_r=ARM_R)
phil = p['left'] + p['body'] + p['head'] + f'<g class="stir-arm" style="transform-origin:23px -110px">{p["right"]}</g>'
mg = scaled(mixing_glass('st-mg', 128) + spoon('stir-spoon'), GX, COUNTER + 2, GS)
props = (at(46, COUNTER, bottle('spirit', '#c98a3c', 'whiskey'), 1.25) + at(84, COUNTER, bottle('tall', '#f4ecd0', 'simple syrup', cap='#c25c86'), 1.2)
         + at(226, COUNTER - 18 * 1.3, bitters(), 1.3))
save('stir', wall + board + place(phil, 146, 236, .95) + countertop(COUNTER) + props + mg + sparkle(216, 34, 6, 'twinkle') + sparkle(30, 40, 5, 'twinkle d2'),
     'Phil, the bartender, stirs a mixing glass full of ice with a long bar spoon. On the bar: whiskey, simple syrup and bitters. '
     'The chalkboard behind him reads: The Cocktail. Spirit, plus sugar, plus water, plus bitters', '20 14 360 196')
CSS += ['/* 1. Phil stirs: the arm and the spoon go round together */',
        '.stir-arm,.stir-spoon{animation:.9s ease-in-out infinite alternate}',
        '.stir-arm{animation-name:stir-arm}', kf('stir-arm', [(0, 'transform:rotate(-5deg)'), (100, 'transform:rotate(5deg)')]),
        '.stir-spoon{animation-name:stir-spoon}', kf('stir-spoon', [(0, 'transform:rotate(-3.5deg)'), (100, 'transform:rotate(3.5deg)')])]

# ---------------------------------------------------------------- 2. dilution (12 s): stir, stir longer, and see the water
DIL = 1.35
h0 = 46   # the drink before the ice melts (drawn a little generous, so the rise reads)
H = h0 * DIL
LEVEL = MBOT + 1 - H
OLD = MBOT + 1 - h0
bg = wash('<rect x="0" y="0" width="400" height="236" fill="#f3e6d4"/>')
# the water, measured: a bracket from where the drink started to where it ended up
bracket = ('<g class="dl-water">' + lines(f'<path d="M228 {f(OLD)} h7 V{f(LEVEL)} h-7" stroke="#3f88b5" stroke-width="2.2"/>', boil=False)
           + f'<path d="M226 {f(OLD)} H156" stroke="#3f88b5" stroke-width="1.6" stroke-dasharray="3 3"/>'
           + f'<text class="letter" x="242" y="{f((OLD + LEVEL) / 2 + 5)}" font-size="16" style="fill:#3f88b5">+ water</text></g>')
caps = [('c1', 'Stir until it\'s good and cold...'), ('c2', '...then, stir longer!'), ('c3', 'The melted ice is part of the drink.')]
captions = '<g class="cap-bob">' + ''.join(f'<text class="letter dl-cap {c}" x="190" y="40" font-size="15.5" text-anchor="middle">{t}</text>' for c, t in caps) + '</g>'
save('dilution', bg + countertop(196, (136, 244)) + mixing_glass('st-dl', LEVEL, 'dl-ice', 'dl-level') + spoon('dl-spoon') + bracket + captions
     + sparkle(118, 84, 6, 'twinkle') + sparkle(264, 74, 5, 'twinkle d2'),
     'A mixing glass full of ice, with whiskey in the bottom and a bar spoon in it. As the spoon stirs, the ice cubes shrink and the drink rises '
     'by about a third. A bracket marks the rise: plus water. The melted ice is part of the drink', '60 14 270 206')
sq = f'scaleY({h0 / H:.3f})'
CSS += ['/* 2. Dilution (12 s): the spoon stirs (8-62%), the ice shrinks and the drink rises, then the bracket shows the water.',
        '   Still frame: the finished drink, the water marked. */',
        '.dl-level,.dl-ice,.dl-spoon,.dl-water,.dl-cap{animation:12s ease-in-out infinite}',
        '.dl-level{animation-name:dl-level}', kf('dl-level', [(0, f'transform:{sq}'), (10, f'transform:{sq}'), (60, 'transform:scaleY(1)'), (100, 'transform:scaleY(1)')]),
        '.dl-ice{transform:scale(.8);animation-name:dl-ice}', kf('dl-ice', [(0, 'transform:scale(1)'), (10, 'transform:scale(1)'), (60, 'transform:scale(.8)'), (100, 'transform:scale(.8)')]),
        '.dl-spoon{animation-name:dl-spoon}', kf('dl-spoon', [(0, 'transform:rotate(0)'), (8, 'transform:rotate(0)')] + [(8 + 54 * i / 12, f'transform:rotate({0 if i in (0, 12) else (7 if i % 2 else -7)}deg)') for i in range(13)] + [(100, 'transform:rotate(0)')]),
        '.dl-water{animation-name:dl-water}', kf('dl-water', [(0, 'opacity:0'), (64, 'opacity:0'), (68, 'opacity:1'), (95, 'opacity:1'), (99, 'opacity:0'), (100, 'opacity:0')]),
        '.dl-cap{opacity:0}.dl-cap.c3{opacity:1}',
        '.cap-bob{animation:cap-bob 1.8s ease-in-out infinite alternate}', kf('cap-bob', [(0, 'transform:translateY(-1.5px)'), (100, 'transform:translateY(1.5px)')]),
        '.dl-cap.c1{animation-name:dl-c1}', window('dl-c1', 6, 34, 2),
        '.dl-cap.c2{animation-name:dl-c2}', window('dl-c2', 37, 60, 2),
        '.dl-cap.c3{animation-name:dl-c3}', window('dl-c3', 66, 95, 2)]

# ---------------------------------------------------------------- 3. dashes (9 s): one, two, three, four
BX, BY, BS = 230, 74, 1.8   # the bitters bottle, held tipped over the glass, its dasher pointing down and left
TIP = (BX - 12.5 * BS, BY + 21.6 * BS)
GLX, GLS = 172, 1.6
liquid_top = 196 - 40 * GLS
drops = ''.join(f'<g class="ds-drop d{i}"><ellipse cx="{f(TIP[0])}" cy="{f(TIP[1] + 4)}" rx="2.6" ry="3.6" fill="#6b1f1a"/></g>' for i in range(1, 5))
count = ''.join(f'<g class="ds-n n{i}"><text class="letter" x="96" y="112" font-size="52" text-anchor="middle" style="fill:#8b3a63">{i}</text>'
                f'<text class="letter" x="96" y="138" font-size="15" text-anchor="middle">{"dash" if i == 1 else "dashes!" if i == 4 else "dashes"}</text></g>' for i in range(1, 5))
word = ''
of = f'<g transform="translate({GLX} 196) scale({GLS})">{glass("rocks", "st-ds", "#c98a3c", (), iced=True)}</g>'
held = f'<g transform="translate({BX} {BY}) scale({BS})"><g class="ds-bottle" style="transform-origin:0px 0px">{bitters()}</g></g>'
save('dashes', wash('<rect x="0" y="0" width="400" height="236" fill="#f3e6d4"/>') + countertop(196, (120, 230)) + of + drops + held + count + word
     + f'<g class="ds-ok">{sparkle(126, 70, 6, "twinkle")}{sparkle(62, 82, 5, "twinkle d2")}</g>',
     'A bottle of bitters, tipped over a rocks glass with one big ice cube, shakes in its dashes: one, two, three, four dashes', '40 14 300 206')
DASH = (20, 33, 46, 59)   # percent: each shake of the bottle
bot = [(0, 'transform:rotate(-150deg)')]
for t in DASH:
    bot += [(t, 'transform:rotate(-150deg)'), (t + 1.5, 'transform:rotate(-166deg)'), (t + 3, 'transform:rotate(-150deg)')]
bot += [(100, 'transform:rotate(-150deg)')]
fall = liquid_top - TIP[1] - 2
CSS += ['/* 3. Dashes (9 s): the bottle, tipped, shakes four times, a drop each, and the count. Still frame: "4 dashes!" */',
        '.ds-bottle,.ds-drop,.ds-n,.ds-ok{animation:9s ease-in-out infinite}',
        '.ds-bottle{transform:rotate(-150deg);animation-name:ds-bottle}', kf('ds-bottle', bot),
        '.ds-drop{opacity:0}']
for i, t in enumerate(DASH, 1):
    CSS += [f'.ds-drop.d{i}{{animation-name:ds-d{i};animation-timing-function:ease-in}}',
            kf(f'ds-d{i}', [(0, 'opacity:0;transform:translateY(0)'), (t + 1.5, 'opacity:0;transform:translateY(0)'), (t + 2, 'opacity:1;transform:translateY(0)'),
                            (t + 6, f'opacity:1;transform:translateY({f(fall)}px)'), (t + 6.5, f'opacity:0;transform:translateY({f(fall)}px)'), (100, 'opacity:0')])]
CSS += ['.ds-n{opacity:0}.ds-n.n4{opacity:1}']
ends = list(DASH[1:]) + [96]
for i, (t, e) in enumerate(zip(DASH, ends), 1):
    CSS += [f'.ds-n.n{i}{{animation-name:ds-n{i}}}', window(f'ds-n{i}', t + 2.5, e + 1 if i < 4 else e, .8)]
CSS += ['.ds-ok{animation-name:ds-ok}', kf('ds-ok', [(0, 'opacity:0'), (61, 'opacity:0'), (63, 'opacity:1'), (95, 'opacity:1'), (97, 'opacity:0'), (100, 'opacity:0')]),
        '/* "Bitter-bitter, stir-stir-stir": break between the words, never at a hyphen */', '.nw{white-space:nowrap}',
        '/* the doors to the stirred drinks: bigger pictures, like Classics */',
        '.flow .doors .door-icon{width:104px;height:104px}', '.flow .doors .door{min-height:10.5rem}']
(PAGE / 'page.css').write_text('\n'.join(CSS) + '\n')

# ---------------------------------------------------------------- the drink doors: the menu's own icons, borrowed
FAMILY = ['old-fashioned', 'manhattan', 'martini', 'vieux-carre', 'negroni', 'boulevardier']
menu_cast = (REPO / 'src/pages/cocktail-menu/cast.svg').read_text()
syms = [re.search(rf'\s*<symbol id="{s}-icon".*?</symbol>', menu_cast, re.S).group(0).strip() for s in FAMILY]
(PAGE / 'cast.svg').write_text('    <!-- Cocktails How-To / Stirred Drinks: the drink doors (copied from the Cocktail Menu by tools/art/stirred_scenes.py) -->\n'
                               + ''.join(f'    {s}\n' for s in syms))
print('scenes: stir, dilution, dashes; doors:', ', '.join(FAMILY))
