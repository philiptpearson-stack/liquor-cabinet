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
    OUT[name] = svg(inner, label) if not view else svg_view(inner, label, view)
    (D / f'{name}.svg').write_text(OUT[name] + '\n')


def save_draft(name, inner, label, view=None):
    """A finished scene not on any page yet (tools/art/drafts/)."""
    (pathlib.Path(__file__).parent / 'drafts' / f'{name}.svg').write_text((svg(inner, label) if not view else svg_view(inner, label, view)) + '\n')


CSS = []   # this page's motion, written to page.css at the end (timings live next to the drawings)


def kf(name, stops):
    """@keyframes from [(percent, 'css'), ...]"""
    return f'@keyframes {name}{{' + ''.join(f'{p:g}%{{{c}}}' for p, c in stops) + '}'


def window(name, on, off, fade=.3):
    """opacity keyframes: hidden, then shown from on% to off%"""
    return kf(name, [(0, 'opacity:0'), (on - fade, 'opacity:0'), (on, 'opacity:1'), (off, 'opacity:1'), (off + fade, 'opacity:0'), (100, 'opacity:0')])


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
waving = p['left'] + p['body'] + p['head'] + f'<g class="hi-wave" style="transform-origin:23px -110px">{p["right"]}</g>'   # not .wave: the kit's .wave pivots on its own box
on_bar = generic_bottle(268, COUNTER, .62, swap='makers-bottle-sm') + rocks(300)
save('welcome', backbar + place(waving, 200, 206) + counter + on_bar,
     'Philip, the bartender, behind his bar: beard, plaid shirt, loose black tie, rolled sleeves. He waves hello. A bottle of Maker\'s Mark and an Old Fashioned sit on the bar',
     view=BAR_VIEW)

# ---------------------------------------------------------------- 2. A shot, a grin, a little buzz (8 s flipbook)
X = 200
bottle_on_bar = generic_bottle(300, COUNTER, .62, swap='makers-bottle-sm')
# beat 1: pour the shot (the glass fills)
p1 = bartender(eyes='dot', mood='smile', parts=True, arm_l=[(-23, -110), (-36, -86), (-31, -60)], arm_r=[(23, -110), (34, -88), (2, -94)])
pour = makers_poured(176, 120)
stream = lines('<path d="M175 121 q-2 6 -3 13" stroke="#c9782c" stroke-width="3"/>', boil=False)
fill_shot = '<g class="shot-fill" style="transform-origin:172px 146px"><path d="M166.4 135 L177.6 135 L176.8 146 L167.2 146Z" fill="#c9782c" opacity=".9"/></g>'
glug = '<text class="letter" x="132" y="96" font-size="15" text-anchor="middle">glug glug</text>'
beat1 = (place(p1['left'] + p1['body'] + p1['head'], X, 206) + counter + shot_glass(172, COUNTER) + fill_shot
         + place(p1['right'], X, 206) + pour + stream + glug)
# beat 2: throw it back
p2 = bartender(eyes='closed', mood='flat', head_tilt=-18, parts=True, arm_l=[(-23, -110), (-38, -122), (-15, -135)], arm_r=[(23, -110), (36, -86), (33, -60)])
held = shot_glass(X - 10.5, 206 - 141, full=False, rot=150)
gulp = '<text class="letter" x="246" y="62" font-size="16" text-anchor="middle">gulp!</text>' + lines('<path d="M226 70 l8 -4 M228 80 l9 0" stroke-width="2"/>', boil=False)
beat2 = place(p2['body'] + p2['head'] + p2['right'], X, 206) + counter + bottle_on_bar + place(p2['left'], X, 206) + held + gulp
# beat 3: slam it down, grin, feel that little buzz
p3 = bartender(eyes='happy', mood='grin', parts=True, arm_l=[(-23, -110), (-36, -88), (-26, -62)], arm_r=[(23, -110), (36, -86), (33, -60)])
flush = '<ellipse cx="-9.5" cy="-131" rx="5.4" ry="3.2" fill="#e8737a" opacity=".55"/><ellipse cx="9.5" cy="-131" rx="5.4" ry="3.2" fill="#e8737a" opacity=".55"/>'
buzzing = f'<g class="buzz" style="transform-origin:0 -118px">{p3["head"]}{flush}</g>'
stars = (f'<g class="orbit" style="transform-origin:{X}px 66px">' + sparkle(X - 26, 50, 5) + sparkle(X + 28, 56, 4.4, fill='#f6c27a') + sparkle(X + 4, 36, 4) + '</g>')
bub = 'M84 28 H182 Q190 28 190 36 V60 Q190 68 182 68 H168 L176 82 L156 68 H84 Q76 68 76 60 V36 Q76 28 84 28Z'
speech = ('<g class="pop-in" style="transform-origin:170px 74px">' + wash(f'<path d="{bub}" fill="#fffaf1"/>') + lines(f'<path d="{bub}" stroke-width="2"/>', boil=False)
          + '<text class="letter" x="133" y="45" font-size="15" text-anchor="middle">Whew!</text>'
          + '<text class="letter" x="133" y="61" font-size="12.5" text-anchor="middle">I needed that!</text></g>')
beat3 = (place(p3['left'] + p3['body'] + buzzing + p3['right'], X, 206) + counter + shot_glass(174, COUNTER, upside=True) + bottle_on_bar + stars + speech)
save('shot', backbar + ''.join(f'<g class="b{k}{" poster" if k == 3 else ""}">{b}</g>' for k, b in enumerate((beat1, beat2, beat3), 1)),
     "Phil pours a shot of Maker's Mark, throws it back, then grins with rosy cheeks and a little buzz: Whew! I needed that!",
     view=BAR_VIEW)
CSS.append('/* 2. A shot (8 s flipbook): pour and fill, throw it back, grin with a buzz. Still frame: the grin. */\n'
           '.b1,.b2{opacity:0}\n.b1,.b2,.b3{animation:8s step-end infinite}\n.b1{animation-name:b1}.b2{animation-name:b2}.b3{animation-name:b3}\n'
           + kf('b1', [(0, 'opacity:1'), (36, 'opacity:0'), (100, 'opacity:0')]) + '\n'
           + kf('b2', [(0, 'opacity:0'), (36, 'opacity:1'), (54, 'opacity:0'), (100, 'opacity:0')]) + '\n'
           + kf('b3', [(0, 'opacity:0'), (54, 'opacity:1'), (100, 'opacity:1')]) + '\n'
           '.shot-fill{animation:shot-fill 8s linear infinite}\n'
           + kf('shot-fill', [(0, 'transform:scaleY(0)'), (6, 'transform:scaleY(0)'), (30, 'transform:scaleY(1)'), (100, 'transform:scaleY(1)')]) + '\n'
           '.buzz{animation:buzz 1.1s ease-in-out infinite alternate}\n' + kf('buzz', [(0, 'transform:rotate(-5deg)'), (100, 'transform:rotate(5deg)')]) + '\n'
           '.orbit{animation:orbit 2.6s linear infinite}\n' + kf('orbit', [(0, 'transform:rotate(0)'), (100, 'transform:rotate(360deg)')]) + '\n'
           '.pop-in{animation:pop-in 8s ease-out infinite}\n'
           + kf('pop-in', [(0, 'transform:scale(0)'), (58, 'transform:scale(0)'), (63, 'transform:scale(1.12)'), (66, 'transform:scale(1)'), (100, 'transform:scale(1)')]))

# ---------------------------------------------------------------- 3. The Cocktail Menu opens, flips, lands on the Whiskey Sour (8 s)
SP = 200          # the spine
T, B = 34, 196    # page top and bottom
paper = '#fbf3e3'
def half(side, inner, fill=paper, cls='', origin=True):
    """A page on one side of the spine; it folds and unfolds about the spine."""
    x0 = SP - 98 if side == 'L' else SP
    body = (f'<rect x="{x0}" y="{T}" width="98" height="{B - T}" rx="3" fill="{fill}"/>'   # solid, so the pages underneath don't show through
            + wash(f'<rect x="{x0}" y="{T}" width="98" height="{B - T}" rx="3" fill="{fill}"/>')) + lines(f'<rect x="{x0}" y="{T}" width="98" height="{B - T}" rx="3" stroke-width="2"/>', boil=False)
    c = f' class="{cls}"' if cls else ''
    st = f' style="transform-origin:{SP}px 115px"' if origin else ''
    return f'<g{c}{st}>{body}{inner}</g>'
scribble = lambda x0, y0, n: lines(''.join(f'<path d="M{x0} {y0 + i * 9} h{58 - (i * 13) % 22}" stroke="#b9a3c8" stroke-width="2"/>' for i in range(n)), boil=False)
def drink_page(name, glass, x0):
    return (f'<text class="letter" x="{x0 + 49}" y="{T + 24}" font-size="13" text-anchor="middle">{name}</text>' + glass + scribble(x0 + 20, T + 116, 4))
coupe_d = lambda cx, cy, s=1.0: (f'<g transform="translate({cx} {cy}) scale({s})">' + wash('<path d="M-20 -22 Q0 6 20 -22Z" fill="#f2d48a"/>')
                                + lines('<path d="M-22 -24 Q0 8 22 -24 M0 -9 V18 M-11 20 Q0 16 11 20" stroke-width="2"/>', boil=False) + '</g>')
rocks_d = lambda cx, cy: rocks(cx, cy, 1.5)
marg = (f'<g transform="translate({SP + 49} {T + 74})">' + wash('<path d="M-22 -26 L22 -26 L4 -6 L4 0 L-4 0 L-4 -6Z" fill="#cfe6a8"/>')
        + lines('<path d="M-24 -28 L24 -28 L4 -6 V20 M-4 -6 V20 M-12 22 H12" stroke-width="2"/>', boil=False) + '</g>')
cover_front = half('R', '<rect x="210" y="46" width="78" height="138" rx="3" fill="none" stroke="#e6b264" stroke-width="2"/>'
                   '<text class="letter" x="249" y="104" font-size="15" text-anchor="middle" style="fill:#f2c776">Cocktail</text>'
                   '<text class="letter" x="249" y="122" font-size="15" text-anchor="middle" style="fill:#f2c776">Menu</text>'
                   + sparkle(249, 146, 6), fill='#6b2f3a', cls='mf-cover')
cover_in = half('L', '<text class="letter" x="151" y="110" font-size="12" text-anchor="middle" style="fill:#8a6a78">Cheers!</text>', cls='mf-cover-in')
p1f = half('R', drink_page('Margarita', marg, SP), cls='mf-p1')
p1b = half('L', scribble(SP - 80, T + 30, 9), cls='mf-p1b')
p2f = half('R', drink_page('Negroni', rocks(SP + 49, T + 96, 1.5), SP), cls='mf-p2')
p2b = half('L', scribble(SP - 80, T + 30, 9), cls='mf-p2b')
p3f = half('R', drink_page('Daiquiri', coupe_d(SP + 49, T + 74, 1.2), SP), cls='mf-p3')
sour_glass = (f'<g transform="translate({SP - 49} {T + 86}) scale(1.5)">' + wash('<path d="M-20 -22 Q0 6 20 -22Z" fill="#e7b85c"/><path d="M-20.5 -22 Q0 -26 20.5 -22 L19 -18 Q0 -14 -19 -18Z" fill="#fffaf1"/>')
              + lines('<path d="M-22 -24 Q0 8 22 -24 M0 -9 V18 M-11 20 Q0 16 11 20" stroke-width="1.6"/>', boil=False) + '</g>')
p3b = half('L', f'<text class="letter" x="{SP - 49}" y="{T + 20}" font-size="11.5" text-anchor="middle">Classic</text>'
                f'<text class="letter" x="{SP - 49}" y="{T + 36}" font-size="13.5" text-anchor="middle">Whiskey Sour</text>' + sour_glass
                + sparkle(SP - 82, T + 70, 4.5, 'twinkle') + sparkle(SP - 14, T + 62, 4, 'twinkle d2'), cls='mf-p3b')
recipe_lines = ["2 oz Maker's Mark", '1 oz lemon juice', '1 oz simple syrup', '1 egg white']
final_r = half('R', ''.join(f'<text class="letter" x="{SP + 12}" y="{T + 34 + i * 20}" font-size="10.5">{t}</text>' for i, t in enumerate(recipe_lines))
               + lines(f'<path d="M{SP + 12} {T + 116} h70 M{SP + 12} {T + 126} h52" stroke="#b9a3c8" stroke-width="2"/>', boil=False), cls='mf-final', origin=False)
bar_strip = wash('<rect x="0" y="200" width="400" height="36" fill="#7a5340"/>') + lines('<path d="M0 200 H400"/>', boil=False)
book = f'<g class="mf-book">{final_r}{p3f}{p2f}{p1f}{cover_front}{cover_in}{p1b}{p2b}{p3b}</g>'
save('menu', wash('<rect x="0" y="0" width="400" height="236" fill="#efe3d0"/>') + bar_strip + book,
     'The Cocktail Menu opens and its pages flip past a Margarita, a Negroni and a Daiquiri, landing on the Classic Whiskey Sour: '
     "2 oz Maker's Mark, 1 oz lemon juice, 1 oz simple syrup, 1 egg white",
     view='72 22 256 196')
# flips: a front folds away (scaleX 1 to 0) about the spine, then its back unfolds on the left (0 to 1)
fold = lambda name, a, b: kf(name, [(0, 'transform:scaleX(1);opacity:1'), (a, 'transform:scaleX(1);opacity:1'), (b, 'transform:scaleX(0);opacity:1'), (b + .1, 'opacity:0'), (100, 'opacity:0')])
unfold = lambda name, a, b: kf(name, [(0, 'transform:scaleX(0);opacity:0'), (a - .1, 'transform:scaleX(0);opacity:0'), (a, 'transform:scaleX(0);opacity:1'), (b, 'transform:scaleX(1);opacity:1'), (100, 'transform:scaleX(1);opacity:1')])
flips = [('mf-cover', 'mf-cover-in', 12), ('mf-p1', 'mf-p1b', 30), ('mf-p2', 'mf-p2b', 42), ('mf-p3', 'mf-p3b', 54)]
mf = ['/* 3. The Cocktail Menu (8 s): the cover opens, three pages flip, it lands on the Whiskey Sour. Still frame: that spread. */',
      '.mf-book{animation:mf-book 8s linear infinite}', kf('mf-book', [(0, 'opacity:0'), (3, 'opacity:1'), (93, 'opacity:1'), (98, 'opacity:0'), (100, 'opacity:0')]),
      '.mf-cover,.mf-p1,.mf-p2,.mf-p3,.mf-cover-in,.mf-p1b,.mf-p2b{opacity:0}']
for front, back, t in flips:
    mf += [f'.{front}{{animation:{front} 8s linear infinite}}', fold(front, t, t + 4), f'.{back}{{animation:{back} 8s linear infinite}}', unfold(back, t + 4, t + 8)]
CSS.append('\n'.join(mf))

# ---------------------------------------------------------------- 4. The Whiskey Sour, step by step (12 s)
# a Boston shaker: a clear mixing glass, and a metal tin that caps it for shaking
G = 'M160 96 L220 96 L214 196 L166 196Z'
G_IN = 'M162.4 99 L217.6 99 L212.3 189 L167.7 189Z'
layer = lambda cls, y0, y1, color: f'<g class="{cls}" style="transform-origin:190px {y1}px"><rect x="158" y="{y0}" width="64" height="{y1 - y0}" fill="{color}"/></g>'
ws_layers = (layer('ws-l1', 168, 189, '#c9782c') + layer('ws-l2', 158, 168, '#f1d75a') + layer('ws-l3', 149, 158, '#f3e3a8') + layer('ws-l4', 142, 149, '#fffaf1')
             + '<g class="ws-mixed"><rect x="158" y="142" width="64" height="47" fill="#ddb064"/><rect x="158" y="128" width="64" height="14" fill="#fffaf1"/></g>')
ice = ''.join(f'<g class="ws-ice i{k}"><rect x="{x}" y="{y}" width="17" height="17" rx="3" fill="#eef8ff" opacity=".85" stroke="#8ecae6" stroke-width="1.6"/></g>' for k, (x, y) in enumerate(((170, 150), (186, 160), (198, 146))))
ws_clip = f'<clipPath id="ws-inside"><path d="{G_IN}"/></clipPath>'
mix_glass = (wash(f'<path d="{G}" fill="#e7f1fb" opacity=".35"/>') + f'<g clip-path="url(#ws-inside)">{wash(ws_layers)}{ice}</g>'
             + lines(f'<path d="{G}" stroke-width="2.4"/><path d="M166 189 H214" stroke-width="1.6"/><path d="M167 106 L164 160" stroke="#fffaf1" stroke-width="3"/>', boil=False))
TIN = 'M154 114 L226 114 L220 58 L160 58Z'   # short enough to clear the caption
tin = (f'<g class="ws-tin">' + wash(f'<path d="{TIN}" fill="#c9c3b8"/>') + lines(f'<path d="{TIN}" stroke-width="2.4"/><path d="M160 104 H220" stroke-width="1.4"/><path d="M167 66 L164 104" stroke="#f4f4f2" stroke-width="3"/>', boil=False)
       + f'<g class="ws-frost">{sparkle(172, 72, 4, "twinkle")}{sparkle(206, 84, 4.4, "twinkle d2")}{sparkle(186, 100, 3.6, "twinkle d3")}</g></g>')
shaker = f'<g class="ws-shaker"><g class="ws-shake" style="transform-origin:190px 116px">{mix_glass}{tin}</g></g>'
# step 1's pours
ws_mm = f'<g class="ws-mm" style="transform-origin:236px 62px">{makers_poured(236, 70, .8, -122)}</g>'
ws_mm_pour = lines('<path d="M235 71 Q214 110 194 180" stroke="#c9782c" stroke-width="4"/>', boil=False, extra=' class="ws-mm-pour"')
jig = wash('<path d="M-9 -16 L9 -16 L3 0 L9 16 L-9 16 L-3 0Z" fill="#c9c3b8"/>') + lines('<path d="M-9 -16 L9 -16 L3 0 L9 16 L-9 16 L-3 0Z M-3 0 H3" stroke-width="2"/>', boil=False)
ws_jig = lambda cls: f'<g class="{cls}" style="transform-origin:150px 58px"><g transform="translate(150 58)">{jig}</g></g>'
ws_pour = lambda cls, color: lines(f'<path d="M163 62 Q178 100 188 166" stroke="{color}" stroke-width="3.4"/>', boil=False, extra=f' class="{cls}"')
lemon = (f'<g class="ws-lemon-tag"><text class="letter" x="126" y="98" font-size="11">lemon</text></g>')
syr = (f'<g class="ws-syrup-tag"><text class="letter" x="126" y="98" font-size="11">syrup</text></g>')
egg_top = wash('<path d="M-11 0 Q-11 -18 0 -18 Q11 -18 11 0 L6 -3 L2 2 L-3 -3 L-7 2Z" fill="#f6ead2"/>') + lines('<path d="M-11 0 Q-11 -18 0 -18 Q11 -18 11 0 L6 -3 L2 2 L-3 -3 L-7 2Z" stroke-width="1.8"/>', boil=False)
egg_bot = wash('<path d="M-11 0 Q-11 14 0 14 Q11 14 11 0 L6 -3 L2 2 L-3 -3 L-7 2Z" fill="#f6ead2"/>') + lines('<path d="M-11 0 Q-11 14 0 14 Q11 14 11 0 L6 -3 L2 2 L-3 -3 L-7 2Z" stroke-width="1.8"/>', boil=False)
egg = (f'<g class="ws-egg"><g class="ws-egg-t" style="transform-origin:192px 72px"><g transform="translate(192 72)">{egg_top}</g></g>'
       f'<g class="ws-egg-b" style="transform-origin:192px 72px"><g transform="translate(192 72)">{egg_bot}</g></g></g>'
       '<g class="ws-white"><path d="M192 78 q-6 6 -2 11 q2 3 4 0 q4 -5 -2 -11Z" fill="#fffaf1" stroke="#c9c3b8" stroke-width="1.2"/></g>')
# step 4: strain into a coupe
CB = 'M262 128 Q290 162 318 128Z'
coupe_full = (f'<g class="ws-coupe">' + wash(f'<path d="{CB}" fill="#e7f1fb" opacity=".35"/>')
              + f'<clipPath id="ws-bowl"><path d="{CB}"/></clipPath>'
              + f'<g clip-path="url(#ws-bowl)" filter="url(#wash)"><g class="ws-c-fill" style="transform-origin:290px 154px"><rect x="258" y="128" width="64" height="30" fill="#ddb064"/></g>'
              + '<g class="ws-c-foam"><rect x="258" y="126" width="64" height="8" fill="#fffaf1"/></g></g>'
              + lines(f'<path d="M260 126 Q290 166 320 126" stroke-width="2.4"/><path d="M260 126 Q290 122 320 126" stroke-width="1.6"/><path d="M290 145 V190 M274 194 Q290 188 306 194" stroke-width="2.4"/>', boil=False) + '</g>')
s_tin = (wash('<path d="M-30 -14 L30 -10 L30 10 L-30 14Z" fill="#c9c3b8"/>') + lines('<path d="M-30 -14 L30 -10 L30 10 L-30 14Z" stroke-width="2.2"/><path d="M30 -10 Q36 0 30 10" stroke="#8a8f96" stroke-width="2"/>'
         '<path d="M31 -7 q3 2 0 4 q3 2 0 4 q3 2 0 4" stroke="#8a8f96" stroke-width="1.4"/>', boil=False))
strain = (f'<g class="ws-strain"><g transform="translate(244 84) rotate(28)">{s_tin}</g></g>'
          + lines('<path d="M272 104 Q284 116 289 136" stroke="#ddb064" stroke-width="3.4"/>', boil=False, extra=' class="ws-strain-pour"'))
ws_cheers = f'<g class="ws-cheers">{sparkle(254, 112, 6, "twinkle")}{sparkle(328, 108, 6, "twinkle d2")}{sparkle(322, 150, 4.5, "twinkle d3")}</g>'
ws_caps = [('1', 'Combine'), ('2', 'Dry shake (no ice!)'), ('3', 'Wet shake (with ice)'), ('4', 'Serve up'), ('5', 'Cheers!')]
caps_ws = ''.join(f'<text class="letter ws-cap c{n}" x="112" y="38" font-size="16">{(n + ". ") if n != "5" else ""}{t}</text>' for n, t in ws_caps)
save('whiskey-sour', f'<defs>{ws_clip}</defs>' + wash('<rect x="0" y="0" width="400" height="236" fill="#f3e6d4"/><rect x="0" y="196" width="400" height="40" fill="#7a5340"/>')
     + lines('<path d="M0 196 H400"/>', boil=False) + shaker + ws_mm + ws_mm_pour + ws_jig('ws-jig1') + ws_pour('ws-pour1', '#f1d75a') + lemon
     + ws_jig('ws-jig2') + ws_pour('ws-pour2', '#f3e3a8') + syr + egg + coupe_full + strain + ws_cheers + caps_ws,
     "A Whiskey Sour, step by step: Maker's Mark, lemon juice, simple syrup and an egg white go into the shaker; a hard dry shake with no ice; "
     "a wet shake with ice; then it's strained into a coupe, served up with a nice egg white foam. Cheers!",
     view='104 16 240 202')


def shake(stops_from, stops_to, amp=16, n=10):
    out = []
    for i in range(n + 1):
        p = stops_from + (stops_to - stops_from) * i / n
        out.append((round(p, 2), f'transform:rotate({0 if i in (0, n) else (amp if i % 2 else -amp)}deg)'))
    return out


ws = ['/* 4. The Whiskey Sour (12 s): combine, dry shake, wet shake, strain and serve up. Still frame: the finished coupe. */',
      '.ws-shaker,.ws-tin,.ws-shake,.ws-mm,.ws-mm-pour,.ws-jig1,.ws-jig2,.ws-pour1,.ws-pour2,.ws-lemon-tag,.ws-syrup-tag,.ws-egg,.ws-egg-t,.ws-egg-b,.ws-white,'
      '.ws-l1,.ws-l2,.ws-l3,.ws-l4,.ws-mixed,.ws-ice,.ws-frost,.ws-coupe,.ws-c-fill,.ws-c-foam,.ws-strain,.ws-strain-pour,.ws-cheers,.ws-cap{animation:12s linear infinite}',
      # the still frame: just the coupe, full, with its foam, and Cheers!
      '.ws-shaker,.ws-mm,.ws-mm-pour,.ws-jig1,.ws-jig2,.ws-pour1,.ws-pour2,.ws-lemon-tag,.ws-syrup-tag,.ws-egg,.ws-white,.ws-strain,.ws-strain-pour,.ws-cap{opacity:0}',
      '.ws-cap.c5{opacity:1}',
      '.ws-shaker{animation-name:ws-shaker}', window('ws-shaker', 2, 76),
      '.ws-l1{animation-name:ws-l1}', kf('ws-l1', [(0, 'transform:scaleY(0)'), (7, 'transform:scaleY(0)'), (14, 'transform:scaleY(1)'), (100, 'transform:scaleY(1)')]),
      '.ws-l2{animation-name:ws-l2}', kf('ws-l2', [(0, 'transform:scaleY(0)'), (16, 'transform:scaleY(0)'), (21, 'transform:scaleY(1)'), (100, 'transform:scaleY(1)')]),
      '.ws-l3{animation-name:ws-l3}', kf('ws-l3', [(0, 'transform:scaleY(0)'), (23, 'transform:scaleY(0)'), (27, 'transform:scaleY(1)'), (100, 'transform:scaleY(1)')]),
      '.ws-l4{animation-name:ws-l4}', kf('ws-l4', [(0, 'transform:scaleY(0)'), (31, 'transform:scaleY(0)'), (34, 'transform:scaleY(1)'), (100, 'transform:scaleY(1)')]),
      '.ws-mixed{animation-name:ws-mixed}', window('ws-mixed', 50, 100, fade=2),
      '.ws-mm{animation-name:ws-mm}', kf('ws-mm', [(0, 'opacity:0;transform:rotate(25deg)'), (5, 'opacity:0;transform:rotate(25deg)'), (6, 'opacity:1;transform:rotate(25deg)'), (8, 'opacity:1;transform:rotate(0)'),
                                                  (13, 'opacity:1;transform:rotate(0)'), (14.5, 'opacity:1;transform:rotate(25deg)'), (15, 'opacity:0'), (100, 'opacity:0')]),
      '.ws-mm-pour{animation-name:ws-mm-pour}', window('ws-mm-pour', 8, 13),
      '.ws-jig1{animation-name:ws-jig1}', kf('ws-jig1', [(0, 'opacity:0;transform:rotate(0)'), (15, 'opacity:0;transform:rotate(0)'), (15.5, 'opacity:1;transform:rotate(0)'), (17, 'opacity:1;transform:rotate(100deg)'),
                                                      (20.5, 'opacity:1;transform:rotate(100deg)'), (21.5, 'opacity:1;transform:rotate(0)'), (22, 'opacity:0'), (100, 'opacity:0')]),
      '.ws-pour1{animation-name:ws-pour1}', window('ws-pour1', 17, 20.5),
      '.ws-lemon-tag{animation-name:ws-lemon-tag}', window('ws-lemon-tag', 15.5, 21.5),
      '.ws-jig2{animation-name:ws-jig2}', kf('ws-jig2', [(0, 'opacity:0;transform:rotate(0)'), (22, 'opacity:0;transform:rotate(0)'), (22.5, 'opacity:1;transform:rotate(0)'), (24, 'opacity:1;transform:rotate(100deg)'),
                                                      (27, 'opacity:1;transform:rotate(100deg)'), (28, 'opacity:1;transform:rotate(0)'), (28.5, 'opacity:0'), (100, 'opacity:0')]),
      '.ws-pour2{animation-name:ws-pour2}', window('ws-pour2', 24, 27),
      '.ws-syrup-tag{animation-name:ws-syrup-tag}', window('ws-syrup-tag', 22.5, 28),
      '.ws-egg{animation-name:ws-egg}', window('ws-egg', 28.5, 33.5),
      '.ws-egg-t{animation-name:ws-egg-t}', kf('ws-egg-t', [(0, 'transform:translate(0,0)'), (30, 'transform:translate(0,0)'), (32, 'transform:translate(-8px,-8px) rotate(-30deg)'), (100, 'transform:translate(-8px,-8px) rotate(-30deg)')]),
      '.ws-egg-b{animation-name:ws-egg-b}', kf('ws-egg-b', [(0, 'transform:translate(0,0)'), (30, 'transform:translate(0,0)'), (32, 'transform:translate(8px,6px) rotate(30deg)'), (100, 'transform:translate(8px,6px) rotate(30deg)')]),
      '.ws-white{animation-name:ws-white}', kf('ws-white', [(0, 'opacity:0;transform:translateY(0)'), (30.5, 'opacity:0;transform:translateY(0)'), (31, 'opacity:1;transform:translateY(0)'),
                                                          (33.5, 'opacity:1;transform:translateY(60px)'), (34, 'opacity:0'), (100, 'opacity:0')]),
      '.ws-tin{animation-name:ws-tin}', kf('ws-tin', [(0, 'opacity:0;transform:translateY(-120px)'), (35, 'opacity:0;transform:translateY(-120px)'), (35.5, 'opacity:1;transform:translateY(-120px)'),
                                                    (38.5, 'opacity:1;transform:translateY(0)'), (55, 'opacity:1;transform:translateY(0)'), (58, 'opacity:1;transform:translateY(-120px)'),
                                                    (62, 'opacity:1;transform:translateY(-120px)'), (65, 'opacity:1;transform:translateY(0)'), (74, 'opacity:1;transform:translateY(0)'),
                                                    (76, 'opacity:1;transform:translateY(-120px)'), (76.5, 'opacity:0'), (100, 'opacity:0')]),
      '.ws-shake{animation-name:ws-shake}', kf('ws-shake', [(0, 'transform:rotate(0)')] + shake(39.5, 52) + shake(65.5, 73) + [(100, 'transform:rotate(0)')]),
      '.ws-ice{animation-name:ws-ice}', kf('ws-ice', [(0, 'opacity:0;transform:translateY(-110px)'), (58.5, 'opacity:0;transform:translateY(-110px)'), (59, 'opacity:1;transform:translateY(-110px)'),
                                                    (61.5, 'opacity:1;transform:translateY(0)'), (100, 'opacity:1;transform:translateY(0)')]),
      '.ws-ice.i1{animation-delay:-.1s}.ws-ice.i2{animation-delay:.12s}',
      '.ws-frost{animation-name:ws-frost}', window('ws-frost', 67, 75),
      '.ws-coupe{animation-name:ws-coupe}', window('ws-coupe', 76, 94, fade=1.5),
      '.ws-strain{animation-name:ws-strain}', window('ws-strain', 77, 87),
      '.ws-strain-pour{animation-name:ws-strain-pour}', window('ws-strain-pour', 78.5, 86),
      '.ws-c-fill{animation-name:ws-c-fill}', kf('ws-c-fill', [(0, 'transform:scaleY(0)'), (79, 'transform:scaleY(0)'), (86, 'transform:scaleY(1)'), (100, 'transform:scaleY(1)')]),
      '.ws-c-foam{animation-name:ws-c-foam}', window('ws-c-foam', 85, 100, fade=2),
      '.ws-cheers{animation-name:ws-cheers}', window('ws-cheers', 88, 94),
      '.ws-cap.c1{animation-name:ws-c1}', window('ws-c1', 5, 34.5),
      '.ws-cap.c2{animation-name:ws-c2}', window('ws-c2', 35, 55),
      '.ws-cap.c3{animation-name:ws-c3}', window('ws-c3', 55.5, 75.5),
      '.ws-cap.c4{animation-name:ws-c4}', window('ws-c4', 76, 87.5),
      '.ws-cap.c5{animation-name:ws-c5}', window('ws-c5', 88, 94)]
CSS.append('\n'.join(ws))

# ---------------------------------------------------------------- Old Fashioned build (12 s): parked in drafts/ for the Old Fashioned's own page
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
save_draft('old-fashioned', f'<defs>{clip}</defs>' + wash('<rect x="60" y="10" width="280" height="200" fill="#f3e6d4"/>') + bar_top
     + glass_back + contents + spoon + glass + jigger + syrup_pour + bitters + dashes + mm + mm_pour + splash + peel + mist + cheers + caps,
     "An Old Fashioned, built step by step in a rocks glass: a little simple syrup and two dashes of bitters, then the Maker's Mark, "
     "then one big ice cube and a stir, then an orange peel squeezed over the top and dropped in. Cheers!",
     view='70 14 260 210')


PAGE_CSS = REPO / 'src/pages/makers-mark/bartender/page.css'
PAGE_CSS.write_text('/* The Bartender\'s Perspective (Maker\'s Mark): scene motion. Every loop runs on CSS alone.\n'
                    '   Written by tools/art/bartender_scenes.py, next to the drawings; edit it there. */\n'
                    '.pop{transform-box:view-box;animation:pop 2.4s ease-in-out infinite}\n'
                    '@keyframes pop{0%,100%{transform:scale(1) rotate(-4deg)}50%{transform:scale(1.14) rotate(4deg)}}\n'
                    '.twinkle{animation:twinkle 1.6s ease-in-out infinite}\n'
                    '.twinkle.d2{animation-delay:-.55s}.twinkle.d3{animation-delay:-1.1s}\n'
                    '@keyframes twinkle{0%,100%{transform:scale(.55) rotate(0);opacity:.35}50%{transform:scale(1.15) rotate(20deg);opacity:1}}\n\n'
                    '/* 1. Hello from behind the bar (not .wave: the kit\'s .wave pivots on its own box) */\n'
                    '.hi-wave{animation:hi-wave 1.3s ease-in-out infinite alternate}\n'
                    '@keyframes hi-wave{from{transform:rotate(-10deg)}to{transform:rotate(12deg)}}\n\n'
                    + '\n\n'.join(CSS) + '\n')
print('scenes:', ', '.join(OUT))
