"""The Bar (the app's front page) and the Spirits List: Phil waving from behind the bar, the shelf, and the door icons.

    python3 tools/art/front_scenes.py
"""
import pathlib
from art import *
from menu_art import bottle, glass, jigger, wheel, at, TWINKLE_CSS
from bartender import bartender
from shelves import plain_bottle

REPO = pathlib.Path('/home/claude/liquor-cabinet')
D = REPO / 'src/pages/bar'
SL = REPO / 'src/pages/spirits-list'
for _d in (D, SL):
    (_d / 'scenes').mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- the bar (the same bar as The Bartender's Perspective)
COUNTER = 146
colors = ['#c98a3c', '#a0522d', '#7f9a6c', '#e6d3bd', '#b9792c', '#c0583c', '#e7f1fb', '#8a6a3c', '#c98a3c', '#7f9a6c', '#a0522d', '#d8c3a5', '#b9792c', '#c0583c']
wall = wash('<rect x="0" y="0" width="400" height="236" fill="#6f5443"/><rect x="40" y="10" width="320" height="140" fill="#cfe0dc" opacity=".55"/>')
shelf = lambda y: wash(f'<rect x="40" y="{y}" width="320" height="4" fill="#bfe3dc" opacity=".9"/>') + lines(f'<path d="M40 {y} H360 M40 {y + 4} H360" stroke="#6aa59a" stroke-width="1.6"/>', boil=False)
backbar = (wall + shelf(56) + ''.join(plain_bottle(52 + i * 22.5, 56, (34, 40, 30, 38, 42, 32, 36)[i % 7], colors[i % 14]) for i in range(14))
           + shelf(102) + ''.join(plain_bottle(56 + i * 24, 102, (30, 36, 40, 32, 38)[i % 5], colors[(i + 5) % 14]) for i in range(13)))
counter = ('<rect x="0" y="146" width="400" height="90" fill="#6e4b39"/>'
           + wash('<rect x="0" y="146" width="400" height="12" fill="#5a3e2e"/><rect x="0" y="158" width="400" height="78" fill="#7a5340"/>')
           + lines('<path d="M0 146 H400 M0 158 H400"/>' + ''.join(f'<rect x="{x}" y="170" width="70" height="52" rx="2" stroke-width="1.8"/>' for x in (20, 116, 212, 308)), boil=False, width=2.2))

# Phil, waving hello
p = bartender(eyes='happy', mood='grin', parts=True, arm_l=[(-23, -110), (-36, -84), (-33, -58)], arm_r=[(23, -110), (40, -124), (43, -150)])
phil = p['left'] + p['body'] + p['head'] + f'<g class="hi-wave" style="transform-origin:23px -110px">{p["right"]}</g>'
# on the bar: the bottle and the bartender's tools. A cocktail and a shaker on one side, three bottles waiting to be asked about on the other
tin_d = 'M-13 0 L-16 -46 L16 -46 L13 0Z'
shaker = at(108, COUNTER, wash(f'<path d="{tin_d}" fill="#c9c3b8"/>') + lines(f'<path d="{tin_d}" stroke-width="2"/><path d="M-10 -40 L-8 -6" stroke="#f4f4f2" stroke-width="2.6"/>', boil=False), .78)
sour = at(136, COUNTER, glass('coupe', 'bar-hero-sour', '#ddb064', ['cherry'], foam=True), .62)
mystery = ''.join(at(x, COUNTER, bottle(shape, color, '?'), s) for x, shape, color, s in
                  ((262, 'tall', '#cfe6df', .62), (290, 'spirit', '#c98a3c', .6), (318, 'liqueur', '#b8621f', .64)))
sp = sparkle(104, 96, 5.5, 'twinkle') + sparkle(156, 90, 4.5, 'twinkle d2') + sparkle(326, 44, 5, 'twinkle d3') + sparkle(302, 100, 4, 'twinkle d2')


def bubble(x0, y0, w, h, tail, text, size=12.5, first=None, cls=''):
    """A speech bubble at (x0, y0), its tail pointing at tail=(x, y); text is a list of lines, each may hold <tspan>s.
    It pops from its tail when it has a class (see page.css)."""
    x1, y1 = x0 + w, y0 + h
    tx, ty = tail
    bx = min(max(tx - 10, x0 + 10), x1 - 22)
    d = (f'M{x0 + 8} {y0} H{x1 - 8} Q{x1} {y0} {x1} {y0 + 8} V{y1 - 8} Q{x1} {y1} {x1 - 8} {y1} H{bx + 20} L{tx} {ty} L{bx + 6} {y1} '
         f'H{x0 + 8} Q{x0} {y1} {x0} {y1 - 8} V{y0 + 8} Q{x0} {y0} {x0 + 8} {y0}Z')
    lh = size * 1.25
    top = y0 + (h - lh * len(text)) / 2 + size * .95
    words = ''.join(f'<text class="letter" x="{f(x0 + w / 2)}" y="{f(top + k * lh)}" font-size="{(first if (first and k == 0) else size)}" text-anchor="middle" style="fill:{INK_TEXT}">{t}</text>'
                    for k, t in enumerate(text))
    c = f' class="{cls}" style="transform-origin:{tx}px {ty}px"' if cls else ''
    return f'<g{c}><path d="{d}" fill="#fffaf1"/>' + wash(f'<path d="{d}" fill="#fffaf1"/>') + lines(f'<path d="{d}" stroke-width="2"/>', boil=False) + words + '</g>'


INK_TEXT = '#3a2532'
PLUM = '#8b3a63'
# Phil says two things (Philip, Nov 4): hello, then the question that opens the doors below. They pop in one after the other.
hello = (bubble(84, 28, 88, 42, (180, 66), ['Hi there!', "I'm Phil!"], 12.5, first=14, cls='hello-1')
         + bubble(250, 58, 76, 46, (226, 92), ['How can I', f'help <tspan style="fill:{PLUM};font-size:15px">YOU</tspan>?'], 12.5, cls='hello-2'))
scene = svg_view(backbar + place(phil, 200, 206) + counter + shaker + sour + mystery + sp + hello,
                 "Phil, the bartender, waves hello from behind his bar and says: Hi there! I'm Phil! Then: How can I help YOU? On the bar: a shaker and a whiskey sour on one side, "
                 'and three bottles with question marks on their labels on the other', '72 22 258 166')
(D / 'scenes' / 'bar.svg').write_text(scene + '\n')

# ---------------------------------------------------------------- door icons (120 x 120)
icons = {}
shelf_icon = (lines('<path d="M8 100 H112 M8 106 H112" stroke="#6aa59a" stroke-width="2"/>', boil=False)
              + at(24, 100, bottle('tall', '#cfe6df', '?'), .95) + at(48, 100, bottle('spirit', '#c98a3c', '?'), 1.0) + at(73, 100, bottle('wine', '#6b3326', '?'), .95)
              + at(98, 100, bottle('liqueur', '#b8621f', '?'), .95) + sparkle(104, 18, 5.5) + sparkle(14, 30, 4))
icons['spirits-icon'] = shelf_icon
more_bottles = (at(30, 108, bottle('tall', '#cfe6df', '?'), 1.15) + at(60, 112, bottle('spirit', '#c98a3c', '?'), 1.3)
                + at(92, 108, bottle('liqueur', '#b8621f', '?'), 1.15))
phone = 'M-24 -50 Q-24 -56 -18 -56 L18 -56 Q24 -56 24 -50 L24 50 Q24 56 18 56 L-18 56 Q-24 56 -24 50Z'
corners = 'M-14 -30 v-8 h8 M6 -38 h8 v8 M14 22 v8 h-8 M-6 30 h-8 v-8'
icons['camera-icon'] = at(60, 60, wash(f'<path d="{phone}" fill="#3b2233"/><rect x="-19" y="-46" width="38" height="86" rx="3" fill="#cfe0dc"/>')
                          + lines(f'<path d="{phone}" stroke-width="2.2"/><rect x="-19" y="-46" width="38" height="86" rx="3" stroke-width="1.6"/>', boil=False)
                          + at(0, 26, bottle('spirit', '#c98a3c', '?'), .62) + lines(f'<path d="{corners}" stroke="#fffaf1" stroke-width="2.6"/>', boil=False)
                          + '<circle cx="0" cy="50" r="2.6" fill="#8a6a78"/>') + sparkle(100, 22, 6) + sparkle(18, 96, 4.5)
cover = ('<rect x="-30" y="-44" width="60" height="88" rx="4" fill="#6b2f3a"/>')
icons['menu-icon'] = (at(52, 60, wash(cover) + lines('<rect x="-30" y="-44" width="60" height="88" rx="4" stroke-width="2.2"/><rect x="-23" y="-37" width="46" height="74" rx="2" stroke="#e6b264" stroke-width="1.8"/>', boil=False)
                         + '<text class="letter" x="0" y="-6" font-size="12" text-anchor="middle" style="fill:#f2c776">Cocktail</text>'
                         + '<text class="letter" x="0" y="9" font-size="12" text-anchor="middle" style="fill:#f2c776">Menu</text>' + sparkle(0, 24, 5))
                      + at(96, 112, glass('coupe', 'bar-menu-ic', '#ddb064', ['cherry'], foam=True), .82))
tin = 'M-13 0 L-16 -46 L16 -46 L13 0Z'
spoon = lines('<path d="M0 0 L0 -84" stroke="#a9a29a" stroke-width="2.6"/>' + ''.join(f'<path d="M-2 -{y} l4 2" stroke="#8a8f96" stroke-width="1.3"/>' for y in range(10, 76, 9))
              + '<circle cx="0" cy="-87" r="3.4" fill="#c9c3b8"/><ellipse cx="0" cy="2" rx="4" ry="2.4" fill="#c9c3b8"/>', boil=False, width=1.8)
icons['howto-icon'] = (at(34, 110, wash(f'<path d="{tin}" fill="#c9c3b8"/>') + lines(f'<path d="{tin}" stroke-width="2"/><path d="M-10 -40 L-8 -6" stroke="#f4f4f2" stroke-width="2.6"/>', boil=False), 1.25)
                       + at(70, 92, jigger(), 1.3) + at(96, 112, spoon, 1, 10) + at(70, 30, wheel('lemon', 9)) + sparkle(22, 30, 5.5))
# Dealer's Choice: a fanned hand of cards; the top one is the drink the bartender picked for you
def card(face):
    d = 'M-17 -50 h34 q4 0 4 4 v42 q0 4 -4 4 h-34 q-4 0 -4 -4 v-42 q0 -4 4 -4Z'
    if face:
        inner = (wash(f'<path d="{d}" fill="#fffaf1"/>') + lines(f'<path d="{d}" stroke-width="2"/>', boil=False)
                 + at(0, -12, glass('coupe', 'bar-deal-ic', '#ddb064', ['cherry'], foam=True), .5)
                 + '<text class="letter" x="-14" y="-38" font-size="9">?</text><text class="letter" x="14" y="-6" font-size="9" text-anchor="end">?</text>')
    else:
        inner = (wash(f'<path d="{d}" fill="#6b2f3a"/>') + lines(f'<path d="{d}" stroke-width="2"/><path d="M-13 -46 h26 v38 h-26Z" stroke="#e6b264" stroke-width="1.4"/>', boil=False)
                 + sparkle(0, -27, 5, fill='#f2c776'))
    return inner
icons['deal-icon'] = (at(56, 110, card(False), 1.45, -22) + at(58, 110, card(False), 1.45, -8) + at(62, 110, card(True), 1.45, 9)
                      + sparkle(100, 22, 6, 'twinkle') + sparkle(18, 40, 4.5, 'twinkle d2'))

(D / 'cast.svg').write_text('    <!-- The Bar (front page): door icons -->\n' + ''.join(f'    <symbol id="{k}" viewBox="0 0 120 120">{v}</symbol>\n' for k, v in icons.items()))

# ---------------------------------------------------------------- the Spirits List: the shelf, and a door per bottle
# the Maker's Mark door shows the bottle itself (a photo in the review build): story.html places it with <!--scene:makers-door-->
halo = wash('<ellipse cx="60" cy="74" rx="34" ry="42" fill="#f6e3a8" opacity=".6"/>')
(SL / 'scenes' / 'makers-door.svg').write_text(f'<svg class="door-icon" viewBox="0 0 120 120" aria-hidden="true">{halo}{generic_bottle(60, 114, 1.5, swap="makers-bottle-sm")}'
                                               f'{sparkle(98, 30, 6)}{sparkle(22, 50, 4.5)}</svg>\n')
(SL / 'cast.svg').write_text('    <!-- The Spirits List: door icons -->\n' + f'    <symbol id="more-bottles-icon" viewBox="0 0 120 120">{more_bottles}</symbol>\n')
# the shelf: Maker's Mark in a little pool of light on the bar, the rest of the back bar still to be asked about
glow = wash(f'<ellipse cx="200" cy="{COUNTER - 26}" rx="34" ry="44" fill="#f6e3a8" opacity=".6"/>')
makers = generic_bottle(200, COUNTER, .95, swap='makers-bottle-sm')
waiting = ''.join(at(x, COUNTER, bottle(shape, color, '?'), sc) for x, shape, color, sc in
                  ((116, 'wine', '#6b3326', .7), (146, 'tall', '#cfe6df', .72), (254, 'spirit', '#c98a3c', .7), (286, 'liqueur', '#b8621f', .74)))
shelf_sp = sparkle(166, 70, 5.5, 'twinkle') + sparkle(236, 62, 5, 'twinkle d2') + sparkle(228, 116, 4, 'twinkle d3')
(SL / 'scenes' / 'shelf.svg').write_text(svg_view(backbar + counter + glow + makers + waiting + shelf_sp,
                                                   "The back bar's shelves of bottles. On the bar in front, a bottle of Maker's Mark sits in a little pool of light, "
                                                   'with four more bottles beside it, question marks on their labels', '84 24 232 150') + '\n')
(SL / 'page.css').write_text('/* The Spirits List: scene motion. Written by tools/art/front_scenes.py; edit it there. */\n' + TWINKLE_CSS + '\n'
                             '.flow .doors .door-icon{width:96px;height:96px}.flow .doors .door.wide .door-icon{width:96px;height:96px}\n')

(D / 'page.css').write_text('/* The Bar (front page): scene motion. Written by tools/art/front_scenes.py; edit it there. */\n' + TWINKLE_CSS + '\n'
                            '.hi-wave{animation:hi-wave 1.3s ease-in-out infinite alternate}\n'
                            '@keyframes hi-wave{from{transform:rotate(-10deg)}to{transform:rotate(12deg)}}\n'
                            '/* the two speech bubbles: hello, then the question; they hold, then start again (8 s). Still frame: both. */\n'
                            '.hello-1,.hello-2{animation:8s ease-out infinite}.hello-1{animation-name:hello-1}.hello-2{animation-name:hello-2}\n'
                            '@keyframes hello-1{0%{transform:scale(0);opacity:1}4%{transform:scale(1.1)}6%{transform:scale(1)}92%{transform:scale(1);opacity:1}97%{opacity:0}100%{opacity:0;transform:scale(1)}}\n'
                            '@keyframes hello-2{0%{transform:scale(0);opacity:1}22%{transform:scale(0)}26%{transform:scale(1.1)}28%{transform:scale(1)}92%{transform:scale(1);opacity:1}97%{opacity:0}100%{opacity:0;transform:scale(1)}}\n'
                            '/* the front door: bigger pictures on the doors, like the Classics */\n'
                            '.flow .doors .door-icon{width:96px;height:96px}.flow .doors .door.wide .door-icon{width:96px;height:96px}\n'
                            '.flow .doors .door{min-height:10rem}\n')
print('bar and spirits list scenes written')
