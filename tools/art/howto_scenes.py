"""Cocktails How-To: the hub's door icons and hero, and the Golden Ratio's scenes."""
import pathlib
from art import *
from bartender import bartender, PLAID

REPO = pathlib.Path('/home/claude/liquor-cabinet')
HUB = REPO / 'src/pages/cocktails-how-to'
GR = HUB / 'golden-ratio'
for d in (HUB / 'scenes', GR / 'scenes'):
    d.mkdir(parents=True, exist_ok=True)
OUT = {}
CSS = {'hub': [], 'gr': []}


def save(where, name, inner, label, view=None):
    OUT[name] = svg(inner, label) if not view else svg_view(inner, label, view)
    (where / 'scenes' / f'{name}.svg').write_text(OUT[name] + '\n')


def kf(name, stops):
    return f'@keyframes {name}{{' + ''.join(f'{p:g}%{{{c}}}' for p, c in stops) + '}'


def window(name, on, off, fade=.5):
    return kf(name, [(0, 'opacity:0'), (on - fade, 'opacity:0'), (on, 'opacity:1'), (off, 'opacity:1'), (off + fade, 'opacity:0'), (100, 'opacity:0')])


# ---------------------------------------------------------------- props (feet / base at 0, 0)
def tin(s=1.0):
    d = 'M-13 0 L-16 -46 L16 -46 L13 0Z'
    return wash(f'<path d="{d}" fill="#c9c3b8"/>') + lines(f'<path d="{d}" stroke-width="2"/><path d="M-10 -40 L-8 -6" stroke="#f4f4f2" stroke-width="2.6"/>', boil=False)


def jigger():
    d = 'M-9 -32 L9 -32 L3 -16 L9 0 L-9 0 L-3 -16Z'
    return wash(f'<path d="{d}" fill="#c9c3b8"/>') + lines(f'<path d="{d} M-3 -16 H3" stroke-width="2"/>', boil=False)


def spoon(h=70):
    return lines(f'<path d="M0 0 L0 -{h}" stroke="#a9a29a" stroke-width="2.6"/>' + ''.join(f'<path d="M-2 -{y} l4 2" stroke="#8a8f96" stroke-width="1.3"/>' for y in range(10, h - 8, 9))
                 + f'<circle cx="0" cy="-{h + 3}" r="3.4" fill="#c9c3b8"/><ellipse cx="0" cy="2" rx="4" ry="2.4" fill="#c9c3b8"/>', boil=False, width=1.8)


def strainer():
    return (wash('<circle cx="0" cy="0" r="13" fill="#d8d3cb"/><rect x="12" y="-3" width="22" height="6" rx="3" fill="#c9c3b8"/>')
            + lines('<circle cx="0" cy="0" r="13" stroke-width="2"/><rect x="12" y="-3" width="22" height="6" rx="3" stroke-width="1.8"/>'
                    '<path d="M-10 4 q2.5 3 5 0 q2.5 -3 5 0 q2.5 3 5 0 q2.5 -3 5 0" stroke="#8a8f96" stroke-width="1.4"/>', boil=False))


def syrup_bottle():
    d = 'M-11 0 L-11 -26 Q-11 -32 -5 -34 L-5 -42 L5 -42 L5 -34 Q11 -32 11 -26 L11 0Z'
    return (wash(f'<path d="{d}" fill="#f3e3a8" opacity=".9"/><rect x="-8.5" y="-22" width="17" height="11" rx="1.5" fill="#fffaf1"/><rect x="-6" y="-47" width="12" height="5" rx="1" fill="#c25c86"/>')
            + lines(f'<path d="{d}" stroke-width="2"/><rect x="-8.5" y="-22" width="17" height="11" rx="1.5" stroke-width="1.4"/><rect x="-6" y="-47" width="12" height="5" rx="1" stroke-width="1.4"/>', boil=False)
            + '<text class="letter" x="0" y="-13.6" font-size="6.6" text-anchor="middle">syrup</text>')


def spirit_bottle():
    d = 'M-13 0 L-13 -38 Q-13 -46 -6 -50 L-5 -62 L5 -62 L6 -50 Q13 -46 13 -38 L13 0Z'
    return (wash(f'<path d="{d}" fill="#c98a3c"/><rect x="-10" y="-30" width="20" height="16" rx="2" fill="#fbf3e3"/><rect x="-5.5" y="-68" width="11" height="7" rx="1.5" fill="#7a5f4a"/>')
            + lines(f'<path d="{d}" stroke-width="2"/><rect x="-10" y="-30" width="20" height="16" rx="2" stroke-width="1.6"/><rect x="-5.5" y="-68" width="11" height="7" rx="1.5" stroke-width="1.6"/>', boil=False)
            + '<text class="letter" x="0" y="-19.4" font-size="6.8" text-anchor="middle">spirit</text>')


def lemon():
    return (wash('<ellipse cx="0" cy="-11" rx="15" ry="11" fill="#f2d24a"/><path d="M14 -13 l5 -2 l-1 4Z" fill="#f2d24a"/>')
            + lines('<ellipse cx="0" cy="-11" rx="15" ry="11" stroke-width="2"/><path d="M14 -13 l5 -2 l-1 4" stroke-width="1.6"/><path d="M-7 -16 q4 -3 9 -2" stroke="#fff6c8" stroke-width="2"/>', boil=False))


def ice_cube(s=1.0):
    return (wash('<rect x="-16" y="-32" width="32" height="32" rx="6" fill="#eef8ff"/>') + lines('<rect x="-16" y="-32" width="32" height="32" rx="6" stroke="#5b8aa6" stroke-width="2.2"/><path d="M-10 -24 h9 M-10 -18 h5" stroke="#fffaf1" stroke-width="2.6"/>', boil=False))


def at(x, y, inner, s=1.0, rot=0):
    r = f' rotate({rot})' if rot else ''
    return f'<g transform="translate({f(x)} {f(y)}){r} scale({f(s)})">{inner}</g>'


# ---------------------------------------------------------------- the hub's door icons (120 x 120)
glasses = (at(30, 98, wash('<path d="M-12 -22 L12 -22 L10.5 0 L-10.5 0Z" fill="#e7f1fb" opacity=".7"/><path d="M-11.5 -14 L11.5 -14 L10.5 0 L-10.5 0Z" fill="#c98a3c"/>')
              + lines('<path d="M-12 -22 L12 -22 L10.5 0 L-10.5 0Z" stroke-width="2"/>', boil=False))
           + at(62, 98, wash('<path d="M-12 -24 L12 -24 L10.5 0 L-10.5 0Z" fill="#e7f1fb" opacity=".7"/><path d="M-11.6 -18 L11.6 -18 L10.5 0 L-10.5 0Z" fill="#c98a3c"/><rect x="-7" y="-22" width="13" height="12" rx="2" fill="#f4fbff" opacity=".85"/>')
                + lines('<path d="M-12 -24 L12 -24 L10.5 0 L-10.5 0Z" stroke-width="2"/><rect x="-7" y="-22" width="13" height="12" rx="2" stroke="#8ecae6" stroke-width="1.3"/>', boil=False))
           + at(95, 98, wash('<path d="M-17 -40 Q0 -14 17 -40Z" fill="#c98a3c"/>') + lines('<path d="M-19 -42 Q0 -10 19 -42 M0 -26 V-3 M-10 0 Q0 -4 10 0" stroke-width="2"/>', boil=False)))
icons = {
    'scale-icon': lines('<path d="M60 102 V36 M42 104 H78 M18 40 H102" stroke-width="3"/><path d="M60 30 l-6 8 h12Z" fill="#e6b264"/>'
                                              '<path d="M24 40 L14 70 M24 40 L34 70 M96 40 L86 70 M96 40 L106 70" stroke-width="1.6"/>', boil=False)
                  + wash('<path d="M10 70 Q24 82 38 70Z M82 70 Q96 82 110 70Z" fill="#e6b264"/>') + lines('<path d="M10 70 Q24 82 38 70Z M82 70 Q96 82 110 70Z" stroke-width="2"/>', boil=False)
                  + '<text class="letter" x="60" y="22" font-size="17" text-anchor="middle">2:1:1</text>',
    'shaker-icon': at(48, 108, tin()) + at(48, 62, '<g transform="scale(1 -1)">' + wash('<path d="M-11 0 L-14 30 L14 30 L11 0Z" fill="#e7f1fb" opacity=".8"/>') + lines('<path d="M-11 0 L-14 30 L14 30 L11 0Z" stroke-width="2"/>', boil=False) + '</g>')
                   + at(88, 108, spoon(74), 1, 12) + lines('<path d="M18 30 q-6 6 0 12 M78 22 q6 6 0 12" stroke="#8a6a78" stroke-width="2"/>', boil=False),
    'syrup-icon': at(46, 108, syrup_bottle(), 1.5) + wash('<rect x="78" y="80" width="18" height="18" rx="2" fill="#fffaf1"/><rect x="86" y="92" width="18" height="18" rx="2" fill="#fffaf1"/>')
                  + lines('<rect x="78" y="80" width="18" height="18" rx="2" stroke-width="1.8"/><rect x="86" y="92" width="18" height="18" rx="2" stroke-width="1.8"/>', boil=False),
    'ice-icon': at(46, 104, ice_cube(), 1.3) + at(84, 106, ice_cube(), .8) + sparkle(96, 40, 7) + sparkle(24, 32, 5),
    'glasses-icon': glasses,
    'tools-icon': at(32, 108, jigger(), 1.3) + at(64, 112, spoon(84), 1, 8) + at(92, 70, strainer(), 1, -30),
}
cast = ('    <!-- Cocktails How-To: door icons -->\n' + ''.join(f'    <symbol id="{k}" viewBox="0 0 120 120">{v}</symbol>\n' for k, v in icons.items()))
(HUB / 'cast.svg').write_text(cast)

# ---------------------------------------------------------------- hub hero: the tools on the bar
bar = wash('<rect x="0" y="0" width="400" height="236" fill="#efe3d0"/><rect x="0" y="178" width="400" height="58" fill="#7a5340"/>') + lines('<path d="M0 178 H400"/>', boil=False)
hero = (bar + at(96, 178, tin(), 1.5) + at(150, 178, jigger(), 1.4) + at(200, 178, syrup_bottle(), 1.6) + at(258, 178, lemon(), 1.5) + at(322, 178, spirit_bottle(), 1.3)
        + at(126, 120, spoon(80), 1, -14) + sparkle(60, 60, 7, 'twinkle') + sparkle(352, 52, 6, 'twinkle d2') + sparkle(220, 40, 5, 'twinkle d3'))
save(HUB, 'tools', hero, 'A bar top laid out for cocktails: a shaker tin, a jigger, a bar spoon, simple syrup, a lemon and a bottle of spirit', view='30 20 340 196')
CSS['hub'].append('.twinkle{animation:twinkle 1.6s ease-in-out infinite}\n.twinkle.d2{animation-delay:-.55s}.twinkle.d3{animation-delay:-1.1s}\n'
                  '@keyframes twinkle{0%,100%{transform:scale(.55) rotate(0);opacity:.35}50%{transform:scale(1.15) rotate(20deg);opacity:1}}')

# ---------------------------------------------------------------- Golden Ratio 1: Phil at the chalkboard
wall = wash('<rect x="0" y="0" width="400" height="236" fill="#6f5443"/>')
board = (wash('<rect x="150" y="30" width="200" height="132" rx="4" fill="#2f3b36"/>') + lines('<rect x="150" y="30" width="200" height="132" rx="4" stroke="#9b7663" stroke-width="6"/>', boil=False)
         + '<text class="letter" x="250" y="96" font-size="44" text-anchor="middle" style="fill:#f4f1e6">2 : 1 : 1</text>'
         + ''.join(f'<text class="letter" x="{x}" y="128" font-size="14" text-anchor="middle" style="fill:#f2c776">{w}</text>' for x, w in ((204, 'spirit'), (250, 'sweet'), (297, 'sour')))
         + lines('<path d="M190 140 q60 6 120 0" stroke="#f4f1e6" stroke-width="1.6"/>', boil=False)
         + wash('<rect x="300" y="150" width="20" height="6" rx="2" fill="#f4f1e6"/>'))
p = bartender(eyes='wink', mood='smug', parts=True, arm_l=[(-23, -110), (-36, -86), (-31, -60)], arm_r=[(23, -110), (44, -124), (60, -138)])
phil = p['left'] + p['body'] + p['head'] + f'<g class="tap" style="transform-origin:23px -110px">{p["right"]}</g>'
counter = ('<rect x="0" y="176" width="400" height="60" fill="#6e4b39"/>' + wash('<rect x="0" y="176" width="400" height="10" fill="#5a3e2e"/><rect x="0" y="186" width="400" height="50" fill="#7a5340"/>')
           + lines('<path d="M0 176 H400 M0 186 H400"/>', boil=False, width=2.2))
save(GR, 'chalkboard', wall + board + place(phil, 104, 236, .95) + counter + sparkle(330, 50, 6, 'twinkle'),
     'Phil, the bartender, winks and points at a chalkboard that reads 2 : 1 : 1, spirit, sweet, sour', view='20 14 360 196')

# ---------------------------------------------------------------- Golden Ratio 2: the balance (16 s)
# a scale: the spirit tips it, the sweetener tips it back too far, the acid brings it level.
# Then the lemon comes off, and a bitter does the same job.
PX, PY, ARM = 200, 70, 110
beam = (wash(f'<rect x="{PX - ARM - 4}" y="{PY - 3}" width="{2 * ARM + 8}" height="6" rx="3" fill="#9b7663"/>')   # a rod, not a bare line: a flat line's crayon filter has no height to draw in
        + lines(f'<rect x="{PX - ARM - 4}" y="{PY - 3}" width="{2 * ARM + 8}" height="6" rx="3" stroke-width="2"/>', boil=False)) + wash(f'<circle cx="{PX}" cy="{PY}" r="5" fill="#e6b264"/>') + lines(f'<circle cx="{PX}" cy="{PY}" r="5" stroke-width="2"/>', boil=False)
stand = (lines(f'<path d="M{PX} {PY} V200 M{PX - 30} 202 H{PX + 30}" stroke-width="3.4"/>', boil=False) + wash(f'<path d="M{PX - 8} {PY + 12} L{PX} {PY - 2} L{PX + 8} {PY + 12}Z" fill="#e6b264"/>'))
def pan(side, contents):
    """A pan hanging from one end of the beam; it counter-turns so it always hangs straight."""
    x = PX + side * ARM
    hang = (lines(f'<path d="M{x} {PY} L{x - 24} {PY + 64} M{x} {PY} L{x + 24} {PY + 64}" stroke-width="1.6"/>', boil=False)
            + wash(f'<path d="M{x - 30} {PY + 64} Q{x} {PY + 82} {x + 30} {PY + 64}Z" fill="#e6b264"/>') + lines(f'<path d="M{x - 30} {PY + 64} Q{x} {PY + 82} {x + 30} {PY + 64}Z" stroke-width="2"/>', boil=False))
    return f'<g class="pan" style="transform-origin:{x}px {PY}px">{hang}{contents}</g>'


def bitters_bottle():
    """A tall bottle of something red and bitter (no brand)."""
    d = 'M-9 0 L-9 -34 Q-9 -40 -4 -42 L-4 -54 L4 -54 L4 -42 Q9 -40 9 -34 L9 0Z'
    return (wash(f'<path d="{d}" fill="#c42f2f"/><rect x="-7.5" y="-28" width="15" height="13" rx="1.5" fill="#fbf3e3"/><rect x="-5" y="-59" width="10" height="5" rx="1" fill="#3b2233"/>')
            + lines(f'<path d="{d}" stroke-width="2"/><rect x="-7.5" y="-28" width="15" height="13" rx="1.5" stroke-width="1.4"/><rect x="-5" y="-59" width="10" height="5" rx="1" stroke-width="1.4"/>', boil=False)
            + '<text class="letter" x="0" y="-18.6" font-size="5.6" text-anchor="middle">bitters</text>')


L, R = PX - ARM, PX + ARM
spirit = f'<g class="sc-spirit">{at(L - 10, PY + 66, spirit_bottle(), .78)}</g>'
sour = f'<g class="sc-sour">{at(L + 15, PY + 66, lemon(), .8)}</g>'
bitter = f'<g class="sc-bitter">{at(L + 14, PY + 66, bitters_bottle(), .85)}</g>'
sweet = f'<g class="sc-sweet">{at(R, PY + 66, syrup_bottle(), 1.05)}</g>'
scale_svg = f'<g class="beam" style="transform-origin:{PX}px {PY}px">{beam}{pan(-1, spirit + sour + bitter)}{pan(1, sweet)}</g>'
caps = [('c1', 'Start with the spirit...'), ('c2', 'The sweetener balances the spirit...'), ('c3', '...and the acid balances the sweet.'),
        ('c4', 'Balance!'), ('c5', 'Or let the bitters do it...'), ('c6', 'Balance!')]
captions = ''.join(f'<text class="letter sc-cap {c}" x="200" y="34" font-size="17" text-anchor="middle">{t}</text>' for c, t in caps)
ok = f'<g class="sc-ok">{sparkle(120, 52, 7, "twinkle")}{sparkle(286, 48, 6, "twinkle d2")}{sparkle(200, 214, 5, "twinkle d3")}</g>'
save(GR, 'balance', wash('<rect x="0" y="0" width="400" height="236" fill="#f3e6d4"/>') + stand + scale_svg + captions + ok,
     'A balance scale. A bottle of spirit tips it down on one side. Simple syrup on the other side tips it too far the other way. '
     'A lemon added next to the spirit brings it level: balance. Then the lemon comes off, a bottle of bitters goes on, and it balances again',
     view='40 6 320 222')
TILT = [(0, 0), (2, 2.5), (4, -1.5), (5, 0), (8, -13),   # a little idle wobble first, so it's alive from the first frame
        (22, -13), (25, 9), (40, 9), (43, 0), (58, 0), (61, 9), (64, 9), (67, 0), (100, 0)]   # (percent, degrees); negative = the spirit side down
drop = lambda name, a, off=94, lift=None: kf(name, [(0, 'opacity:0;transform:translateY(-60px)'), (a, 'opacity:0;transform:translateY(-60px)'), (a + .5, 'opacity:1;transform:translateY(-60px)'),
                                                     (a + 2.5, 'opacity:1;transform:translateY(0)')]
                                         + ([(lift, 'opacity:1;transform:translateY(0)'), (lift + 2.5, 'opacity:0;transform:translateY(-60px)'), (100, 'opacity:0;transform:translateY(-60px)')] if lift else
                                            [(off, 'opacity:1;transform:translateY(0)'), (off + 3, 'opacity:0'), (100, 'opacity:0')]))
CSS['gr'] += [
    '/* 2. The balance (16 s): spirit tips it, sweet tips it back too far, the acid levels it; then the lemon comes off and bitters do the job.',
    '   Still frame: level, with the spirit, the syrup and the bitters on. */',
    '.beam,.pan,.sc-spirit,.sc-sweet,.sc-sour,.sc-bitter,.sc-cap,.sc-ok{animation:16s ease-in-out infinite}',
    '.beam{animation-name:beam}', kf('beam', [(p, f'transform:rotate({d}deg)') for p, d in TILT]),
    '.pan{animation-name:pan}', kf('pan', [(p, f'transform:rotate({-d}deg)') for p, d in TILT]),
    '.sc-spirit{animation-name:sc-spirit}', drop('sc-spirit', 4.5),
    '.sc-sweet{animation-name:sc-sweet}', drop('sc-sweet', 21.5),
    '.sc-sour{opacity:0;animation-name:sc-sour}', drop('sc-sour', 39.5, lift=58),
    '.sc-bitter{animation-name:sc-bitter}', drop('sc-bitter', 63),
    '.sc-cap{opacity:0}.sc-cap.c6,.sc-ok{opacity:1}',
    '.sc-cap.c1{animation-name:sc-c1}', window('sc-c1', 5, 21.5),
    '.sc-cap.c2{animation-name:sc-c2}', window('sc-c2', 22, 39.5),
    '.sc-cap.c3{animation-name:sc-c3}', window('sc-c3', 40, 49.5),
    '.sc-cap.c4{animation-name:sc-c4}', window('sc-c4', 50, 57.5),
    '.sc-cap.c5{animation-name:sc-c5}', window('sc-c5', 58, 74.5),
    '.sc-cap.c6{animation-name:sc-c6}', window('sc-c6', 75, 94),
    '.sc-ok{animation-name:sc-ok}', kf('sc-ok', [(0, 'opacity:0'), (49.5, 'opacity:0'), (50, 'opacity:1'), (57.5, 'opacity:1'), (58, 'opacity:0'), (74.5, 'opacity:0'), (75, 'opacity:1'), (94, 'opacity:1'), (94.5, 'opacity:0'), (100, 'opacity:0')]),
]
CSS['gr'] = ['/* Cocktails How-To / The Golden Ratio: scene motion. Written by tools/art/howto_scenes.py; edit it there. */',
             '.twinkle{animation:twinkle 1.6s ease-in-out infinite}', '.twinkle.d2{animation-delay:-.55s}.twinkle.d3{animation-delay:-1.1s}',
             '@keyframes twinkle{0%,100%{transform:scale(.55) rotate(0);opacity:.35}50%{transform:scale(1.15) rotate(20deg);opacity:1}}',
             '/* 1. Phil taps the chalkboard */', '.tap{animation:tap 1.4s ease-in-out infinite}', kf('tap', [(0, 'transform:rotate(0)'), (50, 'transform:rotate(-7deg)'), (100, 'transform:rotate(0)')])] + CSS['gr']
(GR / 'page.css').write_text('\n'.join(CSS['gr']) + '\n')
(HUB / 'page.css').write_text('/* Cocktails How-To: scene motion. Written by tools/art/howto_scenes.py; edit it there. */\n' + '\n'.join(CSS['hub']) + '\n')
print('scenes:', ', '.join(OUT))
