"""Spirits 101 (the hub for the basic spirits lessons): Phil at the chalkboard, and a door per spirit.

    python3 tools/art/spirits101_scenes.py

The Bar's door to this page (a bottle in a mortarboard) is drawn in front_scenes.py, with the Bar's other door icons.
"""
import math
import pathlib
from art import *
from menu_art import bottle, glass, at, TWINKLE_CSS
from bartender import bartender
from front_scenes import backbar, counter, COUNTER

REPO = pathlib.Path(__file__).resolve().parents[2]
D = REPO / 'src/pages/spirits-101'
(D / 'scenes').mkdir(parents=True, exist_ok=True)

LEAF = '#6f9a4c'
CHALK = '#f4efe6'


# ---------------------------------------------------------------- props: what each spirit is made from (or where it's from)
def corn():
    """An ear of corn in its husk, standing at (0, 0): bourbon."""
    cob = 'M0 -48 Q9 -42 9 -24 Q9 -8 0 -2 Q-9 -8 -9 -24 Q-9 -42 0 -48Z'
    husk = 'M0 0 Q-17 -10 -15 -36 Q-7 -18 -1 -6Z M0 0 Q17 -10 14 -32 Q7 -16 1 -6Z'
    rows = ''.join(f'<path d="M{-7 + abs(y + 25) * .08:.1f} {y} Q0 {y + 2.2} {7 - abs(y + 25) * .08:.1f} {y}"/>' for y in range(-42, -6, 5))
    return (wash(f'<path d="{cob}" fill="#f2c94c"/><path d="{husk}" fill="{LEAF}"/>')
            + lines(rows + '<path d="M0 -46 V-4 M-4.5 -44 Q-6 -24 -4 -6 M4.5 -44 Q6 -24 4 -6"/>', boil=False, color='#c9962c', width=1.3)
            + lines(f'<path d="{cob}" stroke-width="2"/><path d="{husk}" stroke-width="2"/>', boil=False))


def thistle():
    """A thistle: Scotland's flower, for Scotch."""
    brush = ''.join(f'<path d="M{f(math.sin(a) * 3)} -38 L{f(math.sin(a) * 11)} {f(-38 - math.cos(a) * 13)}"/>' for a in [k * .2 for k in range(-5, 6)])
    leaf = 'M0 -10 L-6 -14 L-5 -10 L-12 -13 L-9 -8 L-15 -8 L-6 -4 Z'
    return (lines('<path d="M0 0 Q2.5 -15 0 -30" stroke-width="2.6"/>', boil=False, color='#4e7a3a')   # a curve: a dead-straight line has no width for the crayon filter
            + wash(f'<path d="{leaf}" fill="{LEAF}"/><ellipse cx="0" cy="-31" rx="8" ry="7" fill="{LEAF}"/>')
            + lines(f'<path d="{leaf}" stroke-width="1.6"/><ellipse cx="0" cy="-31" rx="8" ry="7" stroke-width="2"/>'
                    '<path d="M-5 -35 L4 -27 M5 -35 L-4 -27 M-7 -30 L0 -24 M7 -30 L0 -24" stroke-width="1" stroke="#3f6630"/>', boil=False)
            + lines(brush, boil=False, color='#8e4fa3', width=2.4))


def shamrock():
    """A shamrock, for Irish whiskey."""
    heart = 'M0 0 C-2 -4 -9 -6 -9 -11 C-9 -15 -4 -17 0 -13 C4 -17 9 -15 9 -11 C9 -6 2 -4 0 0Z'
    leaves = ''.join(f'<path d="{heart}" transform="translate(0 -24) rotate({r})"/>' for r in (0, 118, 242))
    return (lines('<path d="M0 -24 Q2 -10 -3 0" stroke-width="2.6"/>', boil=False, color='#3f7a35')
            + wash(f'<g fill="#4f9a45">{leaves}</g>') + lines(f'<g stroke-width="1.8">{leaves}</g>', boil=False))


def blossom(x, y, r=1.0):
    petals = ''.join(f'<ellipse cx="0" cy="-4.6" rx="3.3" ry="4.6" transform="rotate({k * 72})"/>' for k in range(5))
    return at(x, y, wash(f'<g fill="#f6c1cf">{petals}</g>') + lines(f'<g stroke-width="1.2">{petals}</g>', boil=False) + '<circle r="2" fill="#d9607a"/>', r)


def cherry_branch():
    """A cherry-blossom branch, for Japanese whisky."""
    return (lines('<path d="M-18 -4 Q-4 -18 2 -34 M-6 -15 Q6 -18 14 -26 M0 -28 Q-8 -36 -12 -44" stroke-width="2.6"/>', boil=False, color='#6b4632')
            + blossom(2, -36) + blossom(15, -27, .85) + blossom(-12, -46, .8) + blossom(-6, -18, .7))


def maple_leaf():
    """A maple leaf, for Canadian whisky."""
    P = [(0, -22), (4, -14), (8, -16), (7, -7), (15, -11), (13, -5), (18, -3), (10, 3), (12, 7), (2, 5), (1, 13),
         (-1, 13), (-2, 5), (-12, 7), (-10, 3), (-18, -3), (-13, -5), (-15, -11), (-7, -7), (-8, -16), (-4, -14)]
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in P) + 'Z'
    return at(0, -16, wash(f'<path d="{d}" fill="#c63f2e"/>') + lines(f'<path d="{d}" stroke-width="1.8"/><path d="M0 9 V-14 M0 0 L10 -5 M0 0 L-10 -5" stroke="#8a2a1f" stroke-width="1"/>', boil=False))


def agave():
    """A blue agave, for tequila and mezcal."""
    out = ''
    for a, ln in ((-62, 30), (62, 30), (-36, 40), (36, 40), (-14, 46), (14, 44), (0, 34)):
        d = f'M-4 0 Q-6 {-ln * .5:.0f} 0 {-ln} Q6 {-ln * .5:.0f} 4 0Z'
        out += f'<g transform="rotate({a})">' + wash(f'<path d="{d}" fill="#7fa8a0"/>') + lines(f'<path d="{d}" stroke-width="1.8"/>', boil=False) + '</g>'
    return out


def juniper():
    """A sprig of juniper, berries and all: gin."""
    needles = ''.join(f'<path d="M{f(x)} {f(y)} l{s * 7} -5"/>' for x, y in ((-10, -6), (-6, -13), (-2, -20), (2, -27), (5, -34)) for s in (-1, 1))
    berries = ''.join(f'<circle cx="{x}" cy="{y}" r="3.6"/>' for x, y in ((8, -14), (12, -20), (4, -24), (9, -28), (14, -10)))
    return (lines('<path d="M-14 0 Q-2 -18 6 -40" stroke-width="2.4"/>', boil=False, color='#6b4632')
            + lines(needles, boil=False, color='#4e7a3a', width=1.8)
            + wash(f'<g fill="#3f557f">{berries}</g>') + lines(f'<g stroke-width="1.4">{berries}</g>', boil=False)
            + ''.join(f'<circle cx="{x - 1.2}" cy="{y - 1.2}" r=".9" fill="#c9d4ea"/>' for x, y in ((8, -14), (12, -20), (4, -24), (9, -28), (14, -10))))


def wheat():
    """Three stalks of wheat: vodka (most of it, anyway)."""
    out = ''
    for x, h, lean in ((-8, 44, -8), (0, 50, 0), (8, 42, 8)):
        g = ''.join(f'<ellipse cx="{3 if k % 2 else -3}" cy="{-h + k * 5.5}" rx="2.6" ry="4.4" transform="rotate({20 if k % 2 else -20} 0 {-h + k * 5.5})"/>' for k in range(5))
        out += (f'<g transform="translate({x} 0) rotate({lean})">' + wash(f'<g fill="#e6c27a">{g}</g>')
                + lines(f'<path d="M0 0 V{-h + 22}"/>{g}<path d="M0 {-h - 2} l0 -8"/>', boil=False, color='#a67a2c', width=1.6) + '</g>')
    return out


def grapes():
    """A bunch of grapes: brandy."""
    spots = [(-8, -34), (0, -34), (8, -34), (-4, -27), (4, -27), (-8, -20), (0, -20), (8, -27), (-4, -13), (4, -13), (0, -6)]
    g = ''.join(f'<circle cx="{x}" cy="{y}" r="4.6"/>' for x, y in spots)
    return (wash(f'<path d="M2 -40 Q12 -50 20 -42 Q14 -36 2 -40Z" fill="{LEAF}"/><g fill="#6e3f78">{g}</g>')
            + lines(f'<g stroke-width="1.5">{g}</g><path d="M2 -40 Q12 -50 20 -42 Q14 -36 2 -40Z" stroke-width="1.6"/><path d="M0 -38 V-46" stroke-width="2.2"/>', boil=False)
            + ''.join(f'<circle cx="{x - 1.4}" cy="{y - 1.6}" r="1" fill="#d7b9de"/>' for x, y in spots[::2]))


def sugarcane():
    """Two stalks of sugarcane: rum."""
    out = ''
    for x, h, lean in ((-5, 56, -6), (6, 50, 7)):
        stalk = f'M-3 0 L-3 {-h} L3 {-h} L3 0Z'
        joints = ''.join(f'<path d="M-3.4 {-y} H3.4"/>' for y in range(10, h, 11))
        leaves = f'M0 {-h} Q-14 {-h - 8} -20 {-h + 4} M0 {-h} Q12 {-h - 12} 18 {-h - 2} M0 {-h + 2} Q-2 {-h - 14} 4 {-h - 18}'
        out += (f'<g transform="translate({x} 0) rotate({lean})">' + wash(f'<path d="{stalk}" fill="#b9c46a"/>')
                + lines(f'<path d="{stalk}" stroke-width="1.8"/>{joints}', boil=False, width=1.6) + lines(f'<path d="{leaves}"/>', boil=False, color='#4e7a3a', width=2.2) + '</g>')
    return out


def snifter(uid):
    """A brandy snifter, a little brandy in the bottom, its foot at (0, 0)."""
    bowl = 'M-9 -46 Q-18 -38 -17 -26 Q-15 -14 -2 -12 L2 -12 Q15 -14 17 -26 Q18 -38 9 -46Z'
    return (f'<clipPath id="{uid}"><path d="{bowl}"/></clipPath>' + wash(f'<path d="{bowl}" fill="#eef4f6" opacity=".7"/>')
            + f'<g clip-path="url(#{uid})">' + wash('<rect x="-20" y="-25" width="40" height="16" fill="#b5651d"/>') + '</g>'
            + lines(f'<path d="{bowl}" stroke-width="2"/><path d="M0 -12 V-2 M-10 0 Q0 -4 10 0" stroke-width="2"/>'
                    '<path d="M-12 -34 Q-13 -26 -9 -20" stroke="#fffaf1" stroke-width="2.2"/>', boil=False))


# ---------------------------------------------------------------- door icons (120 x 120): the bottle, and what it's made from
icons = {
    # Whiskey 101: a bottle and a pour on the rocks
    'whiskey-101-icon': at(44, 112, bottle('spirit', '#c98a3c', 'Whiskey'), 1.3) + at(86, 112, glass('rocks', 's101-rocks', '#c98a3c', iced=True), .82)
                        + sparkle(102, 26, 5.5) + sparkle(16, 34, 4),
    'bourbon-icon': at(46, 112, bottle('spirit', '#b9792c', 'Bourbon'), 1.3) + at(88, 112, corn(), 1.15) + sparkle(102, 24, 5),
    'scotch-icon': at(46, 112, bottle('tall', '#d8a75a', 'Scotch'), 1.3) + at(88, 112, thistle(), 1.25) + sparkle(18, 26, 5),
    'irish-icon': at(46, 112, bottle('spirit', '#5e8a4a', 'Irish'), 1.3) + at(90, 112, shamrock(), 1.35) + sparkle(102, 26, 5),
    'japanese-icon': at(44, 112, bottle('liqueur', '#c98a3c', 'Japanese'), 1.25) + at(90, 112, cherry_branch(), 1.15),
    'canadian-icon': at(44, 112, bottle('tall', '#c98a3c', 'Canadian'), 1.3) + at(90, 104, maple_leaf(), 1.15) + sparkle(18, 26, 5),
    'tequila-icon': at(42, 112, bottle('tall', '#e7f1f3', 'Tequila'), 1.3) + at(88, 112, agave(), .95) + sparkle(102, 22, 5),
    'gin-icon': at(44, 112, bottle('spirit', '#d9ece9', 'Gin'), 1.3) + at(88, 112, juniper(), 1.3) + sparkle(18, 26, 5),
    'vodka-icon': at(44, 112, bottle('tall', '#eef4f6', 'Vodka'), 1.3) + at(88, 112, wheat(), 1.2) + sparkle(102, 22, 5),
    'brandy-icon': at(40, 112, bottle('wine', '#8a4a26', 'Brandy'), 1.25) + at(86, 112, snifter('s101-snifter'), 1.2) + at(104, 70, grapes(), .7),
    'liqueur-icon': at(38, 112, bottle('liqueur', '#d9822b', 'Orange'), 1.15) + at(80, 112, bottle('liqueur', '#6f9a3c', 'Herbal'), 1.05, 6)
                    + sparkle(100, 26, 5.5) + sparkle(16, 30, 4),
    'rum-icon': at(44, 112, bottle('spirit', '#6b3a1f', 'Rum'), 1.3) + at(90, 112, sugarcane(), 1.25),
}
(D / 'cast.svg').write_text('    <!-- Spirits 101: door icons -->\n' + ''.join(f'    <symbol id="{k}" viewBox="0 0 120 120">{v}</symbol>\n' for k, v in icons.items()))

# ---------------------------------------------------------------- the scene: Phil at the chalkboard, the class's bottles lined up on the bar
board_d = 'M0 0 H108 V66 H0Z'
board = at(212, 32, f'<rect x="-5" y="-5" width="118" height="76" rx="3" fill="#8a5a3a"/><path d="{board_d}" fill="#34463f"/>' + wash(f'<rect x="-5" y="-5" width="118" height="76" rx="3" fill="#8a5a3a"/><path d="{board_d}" fill="#34463f"/>')
           + lines(f'<rect x="-5" y="-5" width="118" height="76" rx="3" stroke-width="2.2"/><path d="{board_d}" stroke-width="1.6"/>', boil=False)
           + f'<text class="letter" x="54" y="26" font-size="17" text-anchor="middle" style="fill:{CHALK}">Spirits</text>'
           + f'<text class="letter" x="54" y="56" font-size="27" text-anchor="middle" style="fill:{CHALK}">101</text>'
           + lines('<path d="M30 60 Q54 64 80 59"/>', boil=False, color=CHALK, width=1.6)
           + lines('<path d="M86 70 h12" stroke-width="3"/>', boil=False, color='#fffaf1'), 1, -2)
# Phil points at the board with a bar spoon, his other hand on the bar
p = bartender(eyes='happy', mood='grin', parts=True, arm_l=[(-23, -110), (-40, -88), (-31, -63)], arm_r=[(23, -110), (44, -118), (60, -132)])
pointer = lines('<path d="M208 76 L236 56" stroke="#a9a29a" stroke-width="2.4"/><circle cx="237" cy="55" r="2.6" fill="#c9c3b8"/>', boil=False, width=1.6)
phil = place(p['left'] + p['body'] + p['head'] + p['right'], 150, 206)
# the class: a bottle of each, on the bar; an apple for the teacher
lineup = ''.join(at(x, COUNTER, bottle(shape, color, word), s) for x, shape, color, word, s in
                 ((214, 'spirit', '#c98a3c', 'Whiskey', .62), (240, 'tall', '#e7f1f3', 'Tequila', .62), (264, 'spirit', '#d9ece9', 'Gin', .6),
                  (288, 'tall', '#eef4f6', 'Vodka', .62), (313, 'spirit', '#6b3a1f', 'Rum', .62)))
apple_d = 'M0 -2 Q-11 2 -12 -9 Q-13 -20 -4 -19 Q0 -18 0 -17 Q0 -18 4 -19 Q13 -20 12 -9 Q11 2 0 -2Z'
apple = at(92, COUNTER - 13, wash(f'<path d="{apple_d}" fill="#c63f2e"/><path d="M1 -18 Q8 -26 13 -22 Q8 -17 1 -18Z" fill="{LEAF}"/>')
           + lines(f'<path d="{apple_d}" stroke-width="2"/><path d="M0 -17 Q0 -22 -2 -25" stroke-width="2"/><path d="M1 -18 Q8 -26 13 -22 Q8 -17 1 -18Z" stroke-width="1.5"/>'
                   '<path d="M-7 -14 Q-9 -10 -7 -6" stroke="#f3b0a4" stroke-width="2"/>', boil=False), 1.1)
books = at(92, COUNTER, wash('<rect x="-12" y="-7" width="24" height="7" fill="#6b2f3a"/><rect x="-10" y="-13" width="22" height="6" fill="#7f9a6c"/>')
           + lines('<rect x="-12" y="-7" width="24" height="7" stroke-width="1.6"/><rect x="-10" y="-13" width="22" height="6" stroke-width="1.6"/>', boil=False), 1)
sp = sparkle(330, 30, 5, 'twinkle') + sparkle(200, 40, 4.5, 'twinkle d2') + sparkle(124, 104, 4.5, 'twinkle d3')
scene = svg_view(backbar + board + phil + pointer + counter + lineup + books + apple + sp,
                 "Class is in session: Phil, the bartender, points a bar spoon at a chalkboard that says Spirits 101. On the bar: an apple for the teacher "
                 'on a stack of books, and a bottle each of whiskey, tequila, gin, vodka and rum', '72 22 258 166')
(D / 'scenes' / 'class.svg').write_text(scene + '\n')

(D / 'page.css').write_text('/* Spirits 101: scene motion and the whiskey shelf. Written by tools/art/spirits101_scenes.py; edit it there. */\n' + TWINKLE_CSS + '\n'
                            '.flow .doors .door-icon{width:96px;height:96px}.flow .doors .door.wide .door-icon{width:96px;height:96px}\n'
                            '/* Whiskey 101 on top, its five styles in a row of three and a row of two underneath */\n'
                            '.doors.styles{grid-template-columns:repeat(6,minmax(0,1fr));gap:.7rem;margin-top:-.15rem}\n'
                            '.doors.styles .door{grid-column:span 2;min-height:0;padding:.7rem .4rem .8rem;gap:.35rem}\n'
                            '.doors.styles .door:nth-child(4){grid-column:2/span 2}\n'
                            '.flow .doors.styles .door-icon{width:64px;height:64px}\n'
                            '.doors.styles .door-label{font-size:.92rem}\n'
                            '.doors.styles .stamp{font-size:.52rem;padding:.26rem .35rem .22rem}\n')
print('spirits 101 scenes written')
