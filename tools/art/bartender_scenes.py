"""Maker's Mark / The Bartender's Perspective: scenes. Philip behind his bar."""
import pathlib
from art import *
from shelves import plain_bottle
from bartender import bartender

REPO = pathlib.Path('/home/claude/liquor-cabinet')
D = REPO / 'src/pages/makers-mark/bartender/scenes'
D.mkdir(parents=True, exist_ok=True)
OUT = {}


def save(name, inner, label, view=None):
    OUT[name] = svg(inner, label) if not view else f'<svg viewBox="{view}" role="img" aria-label="{label}">{inner}</svg>'
    (D / f'{name}.svg').write_text(OUT[name] + '\n')


# ---------------------------------------------------------------- the bar itself
COUNTER = 146   # top of the bar
BAR_VIEW = '70 24 260 172'   # framed on him, from the top shelf down to the front of the bar
colors = ['#c98a3c', '#a0522d', '#7f9a6c', '#e6d3bd', '#b9792c', '#c0583c', '#e7f1fb', '#8a6a3c', '#c98a3c', '#7f9a6c', '#a0522d', '#d8c3a5', '#b9792c', '#c0583c']
wall = wash('<rect x="0" y="0" width="400" height="236" fill="#6f5443"/><rect x="40" y="10" width="320" height="140" fill="#cfe0dc" opacity=".55"/>')
shelf = lambda y: wash(f'<rect x="40" y="{y}" width="320" height="4" fill="#bfe3dc" opacity=".9"/>') + lines(f'<path d="M40 {y} H360 M40 {y + 4} H360" stroke="#6aa59a" stroke-width="1.6"/>', boil=False)
backbar = (wall + shelf(56) + ''.join(plain_bottle(52 + i * 22.5, 56, (34, 40, 30, 38, 42, 32, 36)[i % 7], colors[i % 14]) for i in range(14))
           + shelf(102) + ''.join(plain_bottle(56 + i * 24, 102, (30, 36, 40, 32, 38)[i % 5], colors[(i + 5) % 14]) for i in range(13))
           + lines('<path d="M330 4 L352 146 M346 2 L368 146" stroke="#9b7663" stroke-width="3.4"/>'
                   + ''.join(f'<path d="M{333 + k * 3.1} {22 + k * 20} h16" stroke="#9b7663" stroke-width="2.6"/>' for k in range(6)), boil=False))
counter = ('<rect x="0" y="146" width="400" height="90" fill="#6e4b39"/>'
           + wash('<rect x="0" y="146" width="400" height="12" fill="#5a3e2e"/><rect x="0" y="158" width="400" height="78" fill="#7a5340"/>')
           + lines('<path d="M0 146 H400 M0 158 H400"/>' + ''.join(f'<rect x="{x}" y="170" width="70" height="52" rx="2" stroke-width="1.8"/>' for x in (20, 116, 212, 308)), boil=False, width=2.2))


def rocks(x, base=COUNTER, s=1.0, full=True):
    """A rocks glass: an Old Fashioned with a big cube and an orange peel."""
    g = wash('<path d="M-12 -18 L12 -18 L10.8 0 L-10.8 0Z" fill="#e7f1fb" opacity=".7"/>'
             + ('<path d="M-11.6 -12 L11.6 -12 L10.8 0 L-10.8 0Z" fill="#c9782c"/><rect x="-6" y="-16" width="12" height="11" rx="1.5" fill="#f4fbff" opacity=".85"/>'
                '<path d="M6 -21 q6 4 2 12 q-3 -5 -2 -12Z" fill="#e8892c"/>' if full else ''))
    g += lines('<path d="M-12 -18 L12 -18 L10.8 0 L-10.8 0Z" stroke-width="2"/>'
               + ('<rect x="-6" y="-16" width="12" height="11" rx="1.5" stroke-width="1.4"/><path d="M6 -21 q6 4 2 12 q-3 -5 -2 -12Z" stroke-width="1.4"/>' if full else ''), boil=False)
    return f'<g transform="translate({f(x)} {f(base)}) scale({f(s)})">{g}</g>'


def shot_glass(x, y, s=1.0, full=False, upside=False, rot=0):
    body = 'M-6 -15 L6 -15 L4.8 0 L-4.8 0Z' if not upside else 'M-4.8 -15 L4.8 -15 L6 0 L-6 0Z'
    g = wash(f'<path d="{body}" fill="#e7f1fb" opacity=".75"/>' + ('<path d="M-5.6 -10 L5.6 -10 L4.8 0 L-4.8 0Z" fill="#c9782c"/>' if full else ''))
    g += lines(f'<path d="{body}" stroke-width="1.8"/>' + ('<path d="M-5.4 -11 h10.8" stroke-width="1.3"/>' if upside else ''), boil=False)
    r = f' rotate({rot})' if rot else ''
    return f'<g transform="translate({f(x)} {f(y)}){r} scale({f(s)})">{g}</g>'


def pint(x, y, s=1.0, tilt=0):
    """A cold beer: foam on top, sweat on the glass."""
    g = wash('<path d="M-9 -34 L9 -34 L7 0 L-7 0Z" fill="#f2c45a"/><path d="M-9.6 -40 Q-6 -44 0 -42 Q6 -45 9.6 -40 L9 -33 L-9 -33Z" fill="#fffaf1"/>')
    g += lines('<path d="M-9.6 -40 L9.6 -40 L7 0 L-7 0Z" stroke-width="2"/><path d="M-9.6 -40 Q-6 -44 0 -42 Q6 -45 9.6 -40" stroke-width="1.6"/>', boil=False)
    g += ''.join(f'<path d="M{dx} {dy} q-1.4 2 0 3 q1.4 -1 0 -3Z" fill="#f4fbff" stroke="#8ecae6" stroke-width=".8"/>' for dx, dy in ((-4, -24), (3, -16), (-2, -9), (5, -28)))
    rot = f' rotate({tilt})' if tilt else ''
    return f'<g transform="translate({f(x)} {f(y)}){rot} scale({f(s)})">{g}</g>'


def makers_poured(mx, my, s=.62, angle=-118):
    """The Maker's bottle tipped over, mouth at (mx, my)."""
    return f'<g transform="translate({f(mx)} {f(my)}) rotate({angle})">{generic_bottle(0, 68 * s, s, swap="makers-bottle-sm")}</g>'


# ---------------------------------------------------------------- 1. Pull up a stool
wave_r = [(23, -110), (40, -124), (43, -150)]
p = bartender(eyes='dot', parts=True, arm_l=[(-23, -110), (-36, -84), (-33, -58)], arm_r=wave_r)
waving = p['left'] + p['body'] + p['head'] + f'<g class="wave" style="transform-origin:23px -110px">{p["right"]}</g>'
on_bar = generic_bottle(268, COUNTER, .62, swap='makers-bottle-sm') + rocks(300)
save('welcome', backbar + place(waving, 200, 206) + counter + on_bar,
     'Philip, the bartender, behind his bar: beard, plaid shirt, loose black tie, rolled sleeves. He waves hello. A bottle of Maker\'s Mark and an Old Fashioned sit on the bar',
     view=BAR_VIEW)

# ---------------------------------------------------------------- 2. Neat, with a beer back (a four-beat flipbook, 9 s)
X = 200
beer_on_bar = pint(262, COUNTER)
bottle_on_bar = generic_bottle(304, COUNTER, .62, swap='makers-bottle-sm')
# beat 1: pour the shot
p1 = bartender(eyes='dot', mood='smile', parts=True, arm_l=[(-23, -110), (-36, -86), (-31, -60)], arm_r=[(23, -110), (34, -88), (2, -94)])
pour = makers_poured(176, 120)
stream = lines('<path d="M175 121 q-2 6 -3 13" stroke="#c9782c" stroke-width="3"/>', boil=False)
glug = '<text class="letter" x="132" y="104" font-size="15" text-anchor="middle">glug</text>'
beat1 = place(p1['left'] + p1['body'] + p1['head'], X, 206) + counter + shot_glass(172, COUNTER) + beer_on_bar + place(p1['right'], X, 206) + pour + stream + glug
# beat 2: shoot it
p2 = bartender(eyes='closed', mood='o', head_tilt=-13, parts=True, arm_l=[(-23, -110), (-31, -118), (-11, -132)], arm_r=[(23, -110), (36, -86), (33, -60)])
held_shot = shot_glass(X - 11, 206 - 128, full=True, rot=-28)
beat2 = place(p2['body'] + p2['head'] + p2['right'], X, 206) + counter + beer_on_bar + bottle_on_bar + place(p2['left'], X, 206) + held_shot
# beat 3: slam it down, grin
p3 = bartender(eyes='happy', mood='grin', parts=True, arm_l=[(-23, -110), (-36, -88), (-26, -62)], arm_r=[(23, -110), (36, -86), (33, -60)])
ahh = '<text class="letter pop" x="116" y="70" font-size="22" text-anchor="middle" style="transform-origin:116px 62px">Ahh!</text>'
beat3 = place(p3['left'] + p3['body'] + p3['head'] + p3['right'], X, 206) + counter + shot_glass(174, COUNTER, upside=True) + beer_on_bar + bottle_on_bar + ahh
# beat 4: and a nice cold sip of beer
p4 = bartender(eyes='closed', mood='smile', head_tilt=-6, parts=True, arm_l=[(-23, -110), (-36, -88), (-26, -62)], arm_r=[(23, -110), (40, -100), (14, -112)])
sip = pint(X + 26, 206 - 96, 1, tilt=-40)   # rim at his mouth, glass tipped up
frost = sparkle(250, 62, 5, 'twinkle') + sparkle(262, 86, 4, 'twinkle d2')
beat4 = place(p4['left'] + p4['body'] + p4['head'], X, 206) + counter + shot_glass(174, COUNTER, upside=True) + bottle_on_bar + place(p4['right'], X, 206) + sip + frost
beats = ''.join(f'<g class="beat-{k}{" poster" if k == 3 else ""}">{b}</g>' for k, b in enumerate((beat1, beat2, beat3, beat4), 1))
save('neat', backbar + beats,
     'Philip pours a shot of Maker\'s Mark, throws it back, slams the glass down with a grin, Ahh!, then takes a long, cold sip of beer',
     view=BAR_VIEW)

# ---------------------------------------------------------------- 3. The Old Fashioned, built step by step (12 s)
# glass, front view; the inside runs from y 110 (rim) to y 194 (the thick base)
GLASS = 'M148 106 L252 106 L245 206 L155 206Z'
inside = 'M150.6 110 L249.4 110 L243.6 194 L156.4 194Z'
clip = f'<clipPath id="of-inside"><path d="{inside}"/></clipPath>'
syrup = '<g class="of-syrup" style="transform-origin:200px 194px"><rect x="150" y="184" width="100" height="10" fill="#f3d58a"/></g>'
whiskey = '<g class="of-whiskey" style="transform-origin:200px 194px"><rect x="150" y="150" width="100" height="44" fill="#b8621f"/></g>'
rise = '<g class="of-rise" style="transform-origin:200px 150px"><rect x="150" y="138" width="100" height="12" fill="#b8621f"/></g>'
liquid = f'<g clip-path="url(#of-inside)" filter="url(#wash)">{syrup}{whiskey}{rise}</g>'
cube = ('<g class="of-ice">' + wash('<rect x="174" y="140" width="52" height="52" rx="7" fill="#eef8ff" opacity=".8"/>')
        + lines('<rect x="174" y="140" width="52" height="52" rx="7" stroke="#8ecae6" stroke-width="2"/><path d="M182 150 l10 0 M182 156 l5 0" stroke="#fffaf1" stroke-width="2.4"/>', boil=False) + '</g>')
glass_back = wash(f'<path d="{GLASS}" fill="#e7f1fb" opacity=".35"/>')   # behind the drink, so the whiskey stays rich
glass = (lines(f'<path d="{GLASS}" stroke-width="2.6"/><path d="M156 194 L244 194" stroke-width="1.8"/><path d="M158 118 L154 176" stroke="#fffaf1" stroke-width="3"/>', boil=False))
final_peel = ('<g class="of-peel-in">' + wash('<path d="M232 98 Q246 104 246 122 Q242 132 236 136 Q238 122 230 108Z" fill="#e8892c"/>')
              + lines('<path d="M232 98 Q246 104 246 122 Q242 132 236 136 Q238 122 230 108Z" stroke-width="1.8"/>', boil=False) + '</g>')
contents = f'<g class="of-contents">{liquid}{cube}{final_peel}</g>'
# step 1: syrup from a jigger, then two dashes of bitters
jig = wash('<path d="M-9 -16 L9 -16 L3 0 L9 16 L-9 16 L-3 0Z" fill="#c9c3b8"/>') + lines('<path d="M-9 -16 L9 -16 L3 0 L9 16 L-9 16 L-3 0Z M-3 0 H3" stroke-width="2"/>', boil=False)
jigger = f'<g class="of-jigger" style="transform-origin:164px 60px"><g transform="translate(164 60)">{jig}</g></g>'
syrup_pour = lines('<path d="M176 66 Q186 120 192 186" stroke="#f3d58a" stroke-width="3.4"/>', boil=False, extra=' class="of-syrup-pour"')
bit = (wash('<path d="M-9 -8 Q-9 -14 -4 -14 L-4 -20 L4 -20 L4 -14 Q9 -14 9 -8 L9 18 L-9 18Z" fill="#7d2f2a"/><rect x="-11" y="-2" width="22" height="14" rx="1.5" fill="#fbf3e3"/><rect x="-2.5" y="-25" width="5" height="5" fill="#c9c3b8"/>')
       + lines('<path d="M-9 -8 Q-9 -14 -4 -14 L-4 -20 L4 -20 L4 -14 Q9 -14 9 -8 L9 18 L-9 18Z"/><rect x="-11" y="-2" width="22" height="14" rx="1.5" stroke-width="1.5"/><rect x="-2.5" y="-25" width="5" height="5" stroke-width="1.4"/>', boil=False, width=2)
       + '<text class="letter" x="0" y="8.4" font-size="6.6" text-anchor="middle">bitters</text>')
bitters = f'<g class="of-bitters"><g class="of-shake" style="transform-origin:222px 58px"><g transform="translate(222 58) rotate(200)">{bit}</g></g></g>'   # upside down, dasher pointing into the glass
dash = lambda c, d: f'<g class="of-dash {c}"><path d="M213 84 q-2.6 3.6 0 5.6 q2.6 -2 0 -5.6Z" fill="#7d2f2a"/></g>'
dashes = dash('d1', 0) + dash('d2', 0)
# step 2: the Maker's
mm = f'<g class="of-makers" style="transform-origin:226px 80px">{makers_poured(222, 88, .9, -122)}</g>'
mm_pour = lines('<path d="M221 89 Q214 130 206 182" stroke="#c9782c" stroke-width="4.6"/>', boil=False, extra=' class="of-makers-pour"')
# step 3: one big cube, then stir
splash = lines('<path d="M168 134 l-8 -8 M178 128 l-3 -10 M224 128 l3 -10 M233 134 l8 -8" stroke="#8ecae6" stroke-width="2.2"/>', boil=False, extra=' class="of-splash"')
spoon_d = 'M232 18 L214 170'
spoon = (f'<g class="of-spoon"><g class="of-stir" style="transform-origin:214px 170px">'
         + lines(f'<path d="{spoon_d}" stroke="#a9a29a" stroke-width="3"/><path d="M231 26 l-3 3 M229 40 l-3 3 M227 54 l-3 3 M225 68 l-3 3 M223 82 l-3 3 M221 96 l-3 3" stroke="#8a8f96" stroke-width="1.6"/>'
                 '<circle cx="232.5" cy="15" r="4.4" fill="#c9c3b8"/><ellipse cx="213.5" cy="173" rx="5" ry="3" fill="#c9c3b8"/>', boil=False, width=2)
         + '</g></g>')
# step 4: the orange peel, squeezed over the top, then in it goes
peel_d = 'M-17 -4 Q0 -11 17 -4 L15 5 Q0 -1 -15 5Z'
peel = (f'<g class="of-peel"><g class="of-twist" style="transform-origin:200px 64px"><g transform="translate(200 64) scale(1.45)">'
        + wash(f'<path d="{peel_d}" fill="#e8892c"/>') + lines(f'<path d="{peel_d}" stroke-width="2"/><path d="M-12 0 Q0 -5 12 0" stroke="#f6c27a" stroke-width="1.4"/>', boil=False) + '</g></g></g>')
mist = f'<g class="of-mist">{sparkle(186, 86, 4.5, "twinkle")}{sparkle(206, 94, 4, "twinkle d2")}{sparkle(196, 104, 3.6, "twinkle d3")}{sparkle(214, 82, 3.4, "twinkle")}</g>'
cheers = f'<g class="of-cheers">{sparkle(146, 96, 7, "twinkle")}{sparkle(258, 92, 6, "twinkle d2")}{sparkle(252, 150, 5, "twinkle d3")}</g>'
# a caption for each step, top left
captions = [('1', 'Syrup + bitters'), ('2', "Maker's Mark"), ('3', 'Big ice cube. Stir.'), ('4', 'Orange peel'), ('5', 'Cheers!')]
caps = ''.join(f'<text class="letter of-cap c{n}" x="84" y="36" font-size="17">{(n + ". ") if n != "5" else ""}{t}</text>' for n, t in captions)
bar_top = wash('<rect x="60" y="206" width="280" height="16" fill="#7a5340"/>') + lines('<path d="M60 206 H340"/>', boil=False)
save('old-fashioned', f'<defs>{clip}</defs>' + wash('<rect x="60" y="10" width="280" height="200" fill="#f3e6d4"/>') + bar_top
     + glass_back + contents + spoon + glass + jigger + syrup_pour + bitters + dashes + mm + mm_pour + splash + peel + mist + cheers + caps,
     "An Old Fashioned, built step by step in a rocks glass: a little simple syrup and two dashes of bitters, then the Maker's Mark, "
     "then one big ice cube and a stir, then an orange peel squeezed over the top and dropped in. Cheers!",
     view='70 14 260 210')

print('scenes:', ', '.join(OUT))
