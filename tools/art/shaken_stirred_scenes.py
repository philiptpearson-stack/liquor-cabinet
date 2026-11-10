"""Cocktails How-To / Shaken or Stirred?: the page's three scenes and their motion.

    python3 tools/art/shaken_stirred_scenes.py

1. chalkboard  Phil at the chalkboard (as on The Golden Ratio): a shaker, OR a mixing glass.
2. shakestir   A shaker shaking and a mixing glass stirring, side by side: in both the ice melts and the drink rises;
               the shaken one gets froth on top (+ water + air), the stirred one stays clear (+ water).
3. dilution    Stir until it's cold, then stir longer: the ice shrinks, the drink rises, and that rise is water.
Base styles are each scene's still frame (reduced motion); keyframes carry the motion.
"""
import pathlib
from art import *
from menu_art import countertop, TWINKLE_CSS
from bartender import bartender

REPO = pathlib.Path('/home/claude/liquor-cabinet')
PAGE = REPO / 'src/pages/cocktails-how-to/shaken-or-stirred'
(PAGE / 'scenes').mkdir(parents=True, exist_ok=True)
CSS = ['/* Cocktails How-To / Shaken or Stirred?: scene motion. Written by tools/art/shaken_stirred_scenes.py; edit it there. */', TWINKLE_CSS.strip()]
CHALK, GOLD = '#f4f1e6', '#f2c776'


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
AMBER = '#b8742e'    # a stirred drink: whiskey, sugar, bitters
CITRUS = '#d6c055'   # a shaken one: spirit, sugar, lemon or lime


def cube_svg(x, y):
    return (f'<rect x="{x}" y="{y}" width="17" height="17" rx="3" fill="#eef8ff" opacity=".6" stroke="#8ecae6" stroke-width="1.6"/>'
            f'<path d="M{x + 4} {y + 5} h5" stroke="#fffaf1" stroke-width="1.8" stroke-linecap="round"/>')


def mixing_glass(uid, level, cube_cls=None, level_cls=None, color=AMBER, cubes=CUBES, extra=''):
    """The glass full of ice, the drink up to `level` (its rect can grow, by class, from the bottom). `extra` goes in with the drink."""
    H = MBOT + 1 - level
    origin = f' style="transform-origin:190px {MBOT + 1}px"'
    drink = f'<g class="{level_cls}"{origin}>' if level_cls else '<g>'
    drink += f'<rect x="158" y="{f(level)}" width="64" height="{f(H)}" fill="{color}"/></g>'
    ice = ''.join(f'<g class="{cube_cls}" style="transform-origin:{x + 8.5}px {y + 8.5}px">{cube_svg(x, y)}</g>' if cube_cls else cube_svg(x, y) for x, y in cubes)
    return (wash(f'<path d="{G_MIX}" fill="#e7f1fb" opacity=".35"/>') + f'<clipPath id="{uid}"><path d="{G_MIX_IN}"/></clipPath>'
            + f'<g clip-path="url(#{uid})"><g filter="url(#wash)">{drink}</g>{extra}{ice}</g>'
            + lines(f'<path d="{G_MIX}" stroke-width="2.4"/><path d="M166 189 H214" stroke-width="1.6"/><path d="M167 106 L164 160" stroke="#fffaf1" stroke-width="3"/>', boil=False))


def spoon(cls, bx=204, by=182, top=(222, 70)):
    """A bar spoon standing in the mixing glass, its bowl at (bx, by)."""
    return (f'<g class="{cls}" style="transform-origin:{bx}px {by}px">'
            + lines(f'<path d="M{top[0]} {top[1]} L{bx} {by}" stroke="#a9a29a" stroke-width="3"/><circle cx="{top[0]}" cy="{top[1]}" r="4.2" fill="#c9c3b8"/>'
                    f'<ellipse cx="{bx}" cy="{by + 2}" rx="5" ry="3" fill="#c9c3b8"/>', boil=False, width=2) + '</g>')


def scaled(inner, x, y, s, ox=190, oy=196):
    """Draw something made in the mixing glass's own coordinates with its foot (ox, oy) at (x, y), scaled."""
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(s)}) translate({-ox} {-oy})">{inner}</g>'


def stir_states(name, a, b, n=12, deg=7):
    """The spoon going round between a% and b%."""
    return kf(name, [(0, 'transform:rotate(0)'), (a, 'transform:rotate(0)')] + [(a + (b - a) * i / n, f'transform:rotate({0 if i in (0, n) else (deg if i % 2 else -deg)}deg)') for i in range(n + 1)]
              + [(100, 'transform:rotate(0)')])


# ---------------------------------------------------------------- 1. chalkboard: a shaker, OR a mixing glass
wall = wash('<rect x="0" y="0" width="400" height="236" fill="#6f5443"/>')
board = wash('<rect x="150" y="30" width="200" height="132" rx="4" fill="#2f3b36"/>') + lines('<rect x="150" y="30" width="200" height="132" rx="4" stroke="#9b7663" stroke-width="6"/>', boil=False)
chalk_shaker = lines('<path d="M188 46 L214 46 L219 98 L183 98Z"/>'                       # the tin, upside down over...
                     '<path d="M186 96 L216 96 L212 136 L190 136Z"/>'                       # ...the glass
                     '<path d="M192 104 h7 v7 h-7Z M202 106 h7 v7 h-7Z M195 117 h7 v7 h-7Z" stroke-width="1.4"/>'
                     '<path d="M175 58 q-6 8 0 16 M227 58 q6 8 0 16 M170 52 q-9 14 0 28 M232 52 q9 14 0 28" stroke-width="1.6"/>', boil=False, width=2.2, color=CHALK)
chalk_glass = lines('<path d="M284 66 L316 66 L312 136 L288 136Z"/>'
                    '<path d="M290 112 h8 v8 h-8Z M300 110 h8 v8 h-8Z M293 98 h8 v8 h-8Z" stroke-width="1.4"/>'
                    '<path d="M324 48 L304 132" stroke-width="2"/><circle cx="324.6" cy="45.4" r="3"/>', boil=False, width=2.2, color=CHALK)
board += (chalk_shaker + chalk_glass + f'<text class="letter" x="250" y="100" font-size="24" text-anchor="middle" style="fill:{GOLD}">or</text>'
          + ''.join(f'<text class="letter" x="{x}" y="154" font-size="13" text-anchor="middle" style="fill:{CHALK}">{w}</text>' for x, w in ((201, 'shake'), (300, 'stir'))))
p = bartender(eyes='happy', mood='grin', parts=True, arm_l=[(-23, -110), (-36, -86), (-31, -60)], arm_r=[(23, -110), (44, -124), (60, -138)])
phil = p['left'] + p['body'] + p['head'] + f'<g class="tap" style="transform-origin:23px -110px">{p["right"]}</g>'
counter = ('<rect x="0" y="176" width="400" height="60" fill="#6e4b39"/>' + wash('<rect x="0" y="176" width="400" height="10" fill="#5a3e2e"/><rect x="0" y="186" width="400" height="50" fill="#7a5340"/>')
           + lines('<path d="M0 176 H400 M0 186 H400"/>', boil=False, width=2.2))
save('chalkboard', wall + board + place(phil, 104, 236, .95) + counter + sparkle(338, 18, 6, 'twinkle'),
     'Phil, the bartender, points at a chalkboard. On it, in chalk: a cocktail shaker, the word or, and a mixing glass with a bar spoon. Under them: shake, stir', '20 6 360 200')
CSS += ['/* 1. Phil taps the chalkboard */', '.tap{animation:tap 1.4s ease-in-out infinite}', kf('tap', [(0, 'transform:rotate(0)'), (50, 'transform:rotate(-7deg)'), (100, 'transform:rotate(0)')])]

# ---------------------------------------------------------------- 2. shake / stir, side by side (12 s)
# both: the ice melts and the drink rises (about a quarter of the finished drink is water); the shaken one also gets air: froth on top
DIL = 1.35
TIN = 'M164 28 L216 28 L225 122 L155 122Z'   # the shaker tin, upside down over the mixing glass (a Boston shaker)
SH_CUBES = [c for c in CUBES if c[1] >= 119]
h0s, h0m = 30, 40   # the shaker's drink sits lower, so its froth shows below the tin
Hs, Hm = h0s * DIL, h0m * DIL
LVs, LVm = MBOT + 1 - Hs, MBOT + 1 - Hm
froth = (f'<g class="ss-froth"><rect x="158" y="{f(LVs - 11)}" width="64" height="12" fill="#fffaf1"/>'
         + ''.join(f'<circle cx="{x}" cy="{f(LVs + dy)}" r="{r}" fill="#fffaf1" stroke="#cdb560" stroke-width="1.1"/>'
                   for x, dy, r in ((166, -8, 3), (176, -4, 2.4), (186, -9, 2.8), (197, -5, 2.6), (207, -8, 3.2), (215, -3, 2.2),
                                    (171, 8, 1.8), (190, 14, 1.6), (205, 7, 1.8), (180, 22, 1.5), (211, 19, 1.6), (196, 30, 1.4)))
         + '</g>')
tin = (wash(f'<path d="{TIN}" fill="#c9c3b8"/>') + lines(f'<path d="{TIN}" stroke-width="2.4"/><path d="M170 40 L176 110" stroke="#f4f4f2" stroke-width="3"/>'
                                                       '<path d="M157 112 H223" stroke="#a9a29a" stroke-width="1.6"/>', boil=False))
shaker = ('<g class="ss-shaker" style="transform-origin:190px 196px">'
          + mixing_glass('ss-sh', LVs, 'ss-ice', 'ss-lvl-s', CITRUS, SH_CUBES, froth) + tin
          + '</g>'
          + '<g class="ss-whoosh">' + lines('<path d="M140 70 q-10 16 0 32 M128 64 q-13 22 0 44 M240 70 q10 16 0 32 M252 64 q13 22 0 44" stroke="#8a6a78" stroke-width="2.2"/>', boil=False) + '</g>')
stirred = mixing_glass('ss-mx', LVm, 'ss-ice', 'ss-lvl-m', AMBER) + spoon('ss-spoon')
S, LX, RX, FOOT = .95, 112, 288, 204
labels = ''.join(f'<text class="letter" x="{x}" y="26" font-size="19" text-anchor="middle">{w}</text>' for x, w in ((LX, 'shake'), (RX, 'stir')))
result = ('<g class="ss-result">' + ''.join(f'<text class="letter" x="{x}" y="230" font-size="15" text-anchor="middle" style="fill:#f4ecd8">{w}</text>'
                                            for x, w in ((LX, '+ water + air'), (RX, '+ water'))) + '</g>')
save('shakestir', wash('<rect x="0" y="0" width="400" height="236" fill="#f3e6d4"/>') + countertop(FOOT)
     + scaled(shaker, LX, FOOT, S) + scaled(stirred, RX, FOOT, S) + labels + result
     + sparkle(200, 60, 6, 'twinkle') + sparkle(354, 96, 5, 'twinkle d2') + sparkle(40, 110, 4.5, 'twinkle d3'),
     'Side by side: a cocktail shaker, shaking, and a mixing glass, stirred with a bar spoon. In both, the ice melts and the drink rises. '
     'The shaken drink gets a layer of froth on top: plus water, plus air. The stirred drink stays clear: plus water', '20 4 360 232')
sq = f'scaleY({1 / DIL:.3f})'
shake = [(0, 'transform:translate(0,0) rotate(0)'), (8, 'transform:translate(0,0) rotate(0)')]
n = 26
for i in range(1, n):
    shake.append((8 + 50 * i / n, 'transform:translate(0px,-10px) rotate(-3deg)' if i % 2 else 'transform:translate(0px,4px) rotate(2deg)'))
shake += [(58, 'transform:translate(0,0) rotate(0)'), (100, 'transform:translate(0,0) rotate(0)')]
CSS += ['/* 2. Shake and stir (12 s): the shaker shakes and the spoon stirs (8-58%); in both the ice shrinks and the drink rises;',
        '   the shaken one froths up; then the results show on the bar front. Still frame: both finished, results showing. */',
        '.ss-shaker,.ss-whoosh,.ss-spoon,.ss-ice,.ss-lvl-s,.ss-lvl-m,.ss-froth,.ss-result{animation:12s ease-in-out infinite}',
        '.ss-shaker{animation-name:ss-shake;animation-timing-function:linear}', kf('ss-shake', shake),
        '.ss-whoosh{opacity:0;animation-name:ss-whoosh}', window('ss-whoosh', 9, 57, 1),
        '.ss-spoon{animation-name:ss-spoon}', stir_states('ss-spoon', 8, 58),
        '.ss-ice{transform:scale(.8);animation-name:ss-ice}', kf('ss-ice', [(0, 'transform:scale(1)'), (10, 'transform:scale(1)'), (58, 'transform:scale(.8)'), (100, 'transform:scale(.8)')]),
        '.ss-lvl-s,.ss-lvl-m{animation-name:ss-lvl}', kf('ss-lvl', [(0, f'transform:{sq}'), (10, f'transform:{sq}'), (58, 'transform:scaleY(1)'), (100, 'transform:scaleY(1)')]),
        '.ss-froth{animation-name:ss-froth}', kf('ss-froth', [(0, 'opacity:0'), (30, 'opacity:0'), (56, 'opacity:1'), (96, 'opacity:1'), (99, 'opacity:0'), (100, 'opacity:0')]),
        '.ss-result{animation-name:ss-result}', kf('ss-result', [(0, 'opacity:0'), (60, 'opacity:0'), (64, 'opacity:1'), (95, 'opacity:1'), (99, 'opacity:0'), (100, 'opacity:0')])]

# ---------------------------------------------------------------- 3. dilution (12 s): stir until it's cold, then stir longer, and see the water
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
CSS += ['/* 3. Dilution (12 s): the spoon stirs (8-62%), the ice shrinks and the drink rises, then the bracket shows the water.',
        '   Still frame: the finished drink, the water marked. */',
        '.dl-level,.dl-ice,.dl-spoon,.dl-water,.dl-cap{animation:12s ease-in-out infinite}',
        '.dl-level{animation-name:dl-level}', kf('dl-level', [(0, f'transform:{sq}'), (10, f'transform:{sq}'), (60, 'transform:scaleY(1)'), (100, 'transform:scaleY(1)')]),
        '.dl-ice{transform:scale(.8);animation-name:dl-ice}', kf('dl-ice', [(0, 'transform:scale(1)'), (10, 'transform:scale(1)'), (60, 'transform:scale(.8)'), (100, 'transform:scale(.8)')]),
        '.dl-spoon{animation-name:dl-spoon}', stir_states('dl-spoon', 8, 62),
        '.dl-water{animation-name:dl-water}', kf('dl-water', [(0, 'opacity:0'), (64, 'opacity:0'), (68, 'opacity:1'), (95, 'opacity:1'), (99, 'opacity:0'), (100, 'opacity:0')]),
        '.dl-cap{opacity:0}.dl-cap.c3{opacity:1}',
        '.cap-bob{animation:cap-bob 1.8s ease-in-out infinite alternate}', kf('cap-bob', [(0, 'transform:translateY(-1.5px)'), (100, 'transform:translateY(1.5px)')]),
        '.dl-cap.c1{animation-name:dl-c1}', window('dl-c1', 6, 34, 2),
        '.dl-cap.c2{animation-name:dl-c2}', window('dl-c2', 37, 60, 2),
        '.dl-cap.c3{animation-name:dl-c3}', window('dl-c3', 66, 95, 2),
        '/* The Short Version, with nothing more to open: the card without its + */',
        '.cc-static{padding:.8rem 1rem .95rem}']
(PAGE / 'page.css').write_text('\n'.join(CSS) + '\n')
print('scenes: chalkboard, shakestir, dilution')
