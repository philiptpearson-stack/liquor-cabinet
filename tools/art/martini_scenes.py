"""The Cocktail Menu / Martini: Phil's two scenes (Philip, Nov 12 2026). Written by menu_pages.write_drink.

chalkboard  Phil at the chalkboard, puzzling out a long, complicated equation that ends with "= Martini???"
            (the board as on Shaken or Stirred?): the lines chalk on one after another, he scratches his head.
bond        Phil in a tux pours a Martini from a shaker, sets the shaker down, then quick-draws a pistol and winks.
            A generic tuxedoed spy: no names, numbers or logos.
Base styles are each scene's still frame (reduced motion); keyframes carry the motion.
"""
import math
from art import *
from menu_art import glass, garnishes, GLASS
from bartender import bartender

CHALK, GOLD = '#f4f1e6', '#f2c776'
JACKET, LAPEL, SHIRT, TROUSERS = '#25222b', '#3b3644', '#fbf6ea', '#1d1b22'


def kf(name, stops):
    return f'@keyframes {name}{{' + ''.join(f'{p:g}%{{{c}}}' for p, c in stops) + '}'


def window(name, on, off, fade=1.5):
    """Shown from on% to off%, hidden before and after."""
    return kf(name, [(0, 'opacity:0'), (max(on - fade, 0), 'opacity:0'), (on, 'opacity:1'), (off, 'opacity:1'), (min(off + fade, 100), 'opacity:0'), (100, 'opacity:0')])


def counter_front(y=176):
    return ('<rect x="0" y="{0}" width="400" height="{1}" fill="#6e4b39"/>'.format(y, 236 - y)
            + wash(f'<rect x="0" y="{y}" width="400" height="10" fill="#5a3e2e"/><rect x="0" y="{y + 10}" width="400" height="{226 - y}" fill="#7a5340"/>')
            + lines(f'<path d="M0 {y} H400 M0 {y + 10} H400"/>', boil=False, width=2.2))


# ---------------------------------------------------------------- 1. chalkboard: "= Martini???"
EQ = ['(gin + vermouth)² ÷ ice',
      '– bitters?? + olive × 2:1',
      '× (shaken – stirred) ÷ 3:1',
      '+ lemon peel² – 15:1 . . .']
EQ_T = 9.0          # seconds a loop
EQ_ON = [6, 18, 30, 42]   # each line chalks on at this % ...
EQ_END = 56               # ... and "= Martini???" at this %


def chalkboard():
    css = ['/* 1. The chalkboard (9 s): the equation chalks on line by line, then "= Martini???"; Phil scratches his head,'
           ' question marks bob over him. Still frame: the whole equation. */']
    wall = wash('<rect x="0" y="0" width="400" height="236" fill="#6f5443"/>')
    board = (wash('<rect x="146" y="18" width="224" height="148" rx="4" fill="#2f3b36"/>')
             + lines('<rect x="146" y="18" width="224" height="148" rx="4" stroke="#9b7663" stroke-width="6"/>', boil=False))
    eq = ''
    for i, (t, on) in enumerate(zip(EQ, EQ_ON)):
        eq += f'<text class="letter eq{i}" x="160" y="{44 + i * 22}" font-size="14" style="fill:{CHALK}">{t}</text>'
        css += [f'.eq{i}{{animation:eq{i} {EQ_T}s linear infinite}}', window(f'eq{i}', on, 94, 1)]
    # a chalk arrow looping back
    eq += '<g class="eqx">' + lines('<path d="M340 48 q18 30 -6 52 l3 -7 M334 100 l8 2" stroke-width="1.6"/>', boil=False, width=1.6, color=CHALK) + '</g>'
    css += [f'.eqx{{animation:eqx {EQ_T}s linear infinite}}', window('eqx', 46, 94, 1)]
    eq += (f'<g class="eqm"><text class="letter" x="358" y="152" font-size="22" text-anchor="end" style="fill:{GOLD}">= Martini'
           f'<tspan class="qq">???</tspan></text></g>')
    css += [f'.eqm{{animation:eqm {EQ_T}s linear infinite}}', window('eqm', EQ_END, 94, 1),
            '.qq{animation:qq .5s ease-in-out infinite alternate}', kf('qq', [(0, 'opacity:.55'), (100, 'opacity:1')])]

    # Phil: one hand scratching his head, the other at the board with a stub of chalk; eyes on the board, mouth an "o"
    chalk = '<rect x="57" y="-135" width="9" height="3.4" rx="1" fill="#f4f1e6" stroke="#2c2230" stroke-width="1" transform="rotate(-35 61 -133)"/>'
    p = bartender(eyes='side', mood='o', parts=True, arm_l=[(-23, -110), (-42, -128), (-15, -157)], arm_r=[(23, -110), (42, -112), (58, -130)], holding=chalk)
    phil = (f'<g class="scratch" style="transform-origin:-23px -110px">{p["left"]}</g>' + p['body'] + p['head'] + p['right'])
    css += ['.scratch{animation:scratch .32s ease-in-out infinite alternate}', kf('scratch', [(0, 'transform:rotate(0)'), (100, 'transform:rotate(5deg)')])]
    huh = ''.join(f'<text class="letter huh h{i}" x="{x}" y="{y}" font-size="{s}" style="fill:#f2c776">?</text>' for i, (x, y, s) in enumerate(((64, 70, 20), (128, 58, 16), (100, 44, 13))))
    css += ['.huh{animation:huh 1.5s ease-in-out infinite alternate}.huh.h1{animation-delay:-.5s}.huh.h2{animation-delay:-1s}',
            kf('huh', [(0, 'transform:translateY(0)'), (100, 'transform:translateY(-5px)')])]
    inner = wall + board + eq + place(phil, 96, 236, .95) + counter_front() + huh + sparkle(30, 30, 6, 'twinkle')
    alt = ('Phil, the bartender, scratches his head at a chalkboard covered in a long, complicated equation: '
           '(gin + vermouth) squared, divided by ice, minus bitters, plus olive, times 2 to 1, shaken minus stirred, lemon peel squared, '
           'and on and on, until it ends: equals Martini, question mark, question mark, question mark.')
    return svg_view(inner, alt, '20 6 360 200'), css


# ---------------------------------------------------------------- 2. bond: pour, then the quick-draw
BT = 8.0                 # seconds a loop
TIP = (4, 10)            # the shaker tips over the glass (%)
POUR = (11, 36)          # the pour: the stream runs and the glass fills
UNTIP = (36, 40)
DOWN = 44                # the shaker's down on the bar
OLIVES = 47
DRAW = 53                # the quick-draw
BACK = 93                # everything back for the next loop


def tux_arm(points):
    """A black tux sleeve to the wrist, a white shirt cuff, the hand."""
    (sx, sy), (ex, ey), (hx, hy) = points
    upper = limb([(sx, sy), (ex, ey)], 12.5, 11.5)
    fore = limb([(ex, ey), (hx, hy)], 11, 10)
    dx, dy = hx - ex, hy - ey
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    cx, cy = hx - ux * 7, hy - uy * 7
    cuff = 'M' + ' L'.join(f'{f(cx + a * nx * 5.6 + b * ux * 2.4)} {f(cy + a * ny * 5.6 + b * uy * 2.4)}' for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))) + 'Z'
    fill = (f'<path d="{upper}" fill="{JACKET}"/><path d="{fore}" fill="{JACKET}"/><path d="{cuff}" fill="{SHIRT}"/>'
            f'<circle cx="{f(hx)}" cy="{f(hy)}" r="5.6" fill="{SKIN}"/>')
    line = f'<path d="{upper}"/><path d="{fore}"/><path d="{cuff}" stroke-width="1.6"/><circle cx="{f(hx)}" cy="{f(hy)}" r="5.6"/>'
    return part(fill, line)


def tux_body():
    fill = f'<path d="M-17 -62 L-16 -2 L16 -2 L17 -62Z" fill="{TROUSERS}"/>'
    line = '<path d="M-17 -62 L-16 -2 M16 -2 L17 -62"/>'
    jacket = 'M-26 -113 Q-30 -86 -24 -54 L24 -54 Q30 -86 26 -113 Q12 -120 0 -119 Q-12 -120 -26 -113Z'
    shirt = 'M-9 -118 L9 -118 L3 -78 L0 -74 L-3 -78Z'
    lapel_l, lapel_r = 'M-12 -118 L-3 -78 L-11 -92 L-16 -112Z', 'M12 -118 L3 -78 L11 -92 L16 -112Z'
    fill += f'<path d="{jacket}" fill="{JACKET}"/><path d="{shirt}" fill="{SHIRT}"/><path d="{lapel_l}" fill="{LAPEL}"/><path d="{lapel_r}" fill="{LAPEL}"/>'
    line += f'<path d="{jacket}"/><path d="{shirt}" stroke-width="1.6"/><path d="{lapel_l}" stroke-width="1.6"/><path d="{lapel_r}" stroke-width="1.6"/>'
    # bow tie, shirt studs, a pocket square, one button
    bow = 'M0 -113.5 L-8 -117.5 L-8 -109.5Z M0 -113.5 L8 -117.5 L8 -109.5Z'
    fill += f'<path d="{bow}" fill="#14121a"/><circle cx="0" cy="-113.5" r="2" fill="#14121a"/>'
    line += f'<path d="{bow}" stroke-width="1.5"/>'
    fill += ''.join(f'<circle cx="0" cy="{y}" r="1.1" fill="#2c2230"/>' for y in (-104, -96, -88))
    fill += f'<path d="M12 -100 L20 -100 L18.5 -95 L16 -98 L13.5 -95Z" fill="{SHIRT}"/><circle cx="0" cy="-66" r="1.6" fill="#55505e"/>'
    line += '<path d="M11 -100 H21" stroke-width="1.6"/>'
    return part(fill, line)


def shaker(tilt=0, cap=False):
    """A cobbler shaker: the spout at (0, 0), then the strainer top, the collar and the body, its base 48 below.
    Tipped (tilt in degrees), it pours from the spout. cap: the little cap on the spout (when it's sitting on the bar)."""
    spout = 'M-3.5 0 L3.5 0 L3.5 6 L-3.5 6Z'
    top = 'M-5 6 L5 6 L10 14 L-10 14Z'
    collar = 'M-11 14 L11 14 L11 17.5 L-11 17.5Z'
    body = 'M-11 17.5 L11 17.5 L13.5 45 L-13.5 45Z'
    base = 'M-14 45 L14 45 L14 48 L-14 48Z'
    capd = 'M-4.5 -5 Q0 -9 4.5 -5 L4 1 L-4 1Z'
    parts = [spout, top, collar, body, base] + ([capd] if cap else [])
    fills = ''.join(f'<path d="{d}" fill="{c}"/>' for d, c in zip(parts, ['#b8b1a5', '#cfc9be', '#b8b1a5', '#d4cec3', '#b8b1a5', '#cfc9be']))
    return (f'<g transform="rotate({tilt})">' + wash(fills)
            + lines(''.join(f'<path d="{d}"/>' for d in parts) + '<path d="M7 21 L9 41" stroke="#fffaf1" stroke-width="2.6"/><path d="M4 8 L6 12" stroke="#fffaf1" stroke-width="1.6"/>',
                    boil=False, width=2)
            + '</g>')


def pistol():
    """A cartoon pistol in profile, pointing right: the slide, a front sight, the hammer, the trigger guard and a wooden grip.
    Its grip (where the hand goes) is at (0, 0)."""
    slide = 'M-7 -14 L28 -14 L28 -5 L-7 -5Z'
    frame = 'M-5 -5 L15 -5 L15 -2 L-5 -2Z'
    grip = 'M-8 -5 L2 -5 L0 12 L-10 10Z'
    guard = 'M3 -2 Q3 5 9 5 Q14 5 14 -2'
    return (wash(f'<path d="{grip}" fill="#6b4630"/><path d="{frame}" fill="#34323b"/><path d="{slide}" fill="#3d3b46"/>'
                 '<path d="M24 -14 L24 -17 L27 -17 L27 -14Z M-7 -14 L-10 -18 L-7 -19 L-4 -14Z" fill="#3d3b46"/>')
            + lines(f'<path d="{slide}"/><path d="{frame}" stroke-width="1.6"/><path d="{grip}"/><path d="{guard}" stroke-width="1.8"/>'
                    '<path d="M24 -14 L24 -17 L27 -17 L27 -14 M-7 -14 L-10 -18 L-7 -19 L-4 -14" stroke-width="1.5"/>'
                    '<path d="M8 -2 q1 3 -1 5" stroke-width="1.5"/><path d="M-3 -11.5 H25" stroke="#9a96a8" stroke-width="1.4"/>'
                    '<path d="M-6 0 L-8 8 M-3 0 L-5 8" stroke="#3a2418" stroke-width="1"/>', boil=False, width=2.2))


def bond():
    css = [f'/* 2. Phil, in a tux ({BT:g} s): tips the shaker over the glass, pours (the stream runs, the Martini fills from the point up), '
           f'sets it down, the olives go in, then he quick-draws ({DRAW}%) and winks. Still frame: the pistol out, the Martini poured, the shaker on the bar. */']
    wall = wash('<rect x="0" y="0" width="400" height="236" fill="#3e2c3d"/>') + wash('<ellipse cx="170" cy="96" rx="130" ry="84" fill="#6b4a63" opacity=".55"/>')
    PX, PY = 150, 236
    gx, gy, gs = 262, 176, .85                   # the Martini glass on the bar: rim at y 108, the bowl's point at y 136.5
    g = GLASS['martini']

    def anim(cls, stops):
        css.append(f'.{cls}{{animation:{cls} {BT}s linear infinite}}')
        css.append(kf(cls, stops))

    def shown(on, off, fade=.5):   # visible from on% to off% (on may be 0, off may be 100)
        st = [(0, 'opacity:' + ('1' if on == 0 else '0'))]
        if on:
            st += [(on - fade, 'opacity:0'), (on, 'opacity:1')]
        if off < 100:
            st += [(off, 'opacity:1'), (off + fade, 'opacity:0')]
        return st + [(100, 'opacity:' + ('1' if off == 100 else '0'))]

    # heads: watching the pour, then the wink
    h_pour = bartender(eyes='happy', mood='smile', parts=True)['head']
    h_draw = bartender(eyes='wink', mood='smug', parts=True, head_tilt=-5)['head']
    # his right arm (viewer's right): out over the glass with the shaker, then back at his waist
    H = (80, -148)                                # the hand, over the glass
    arm_pour = tux_arm([(24, -110), (52, -124), H])
    ts, th = .95, 122                             # the shaker: its scale, and how far it tips
    mid = (-26 * ts * math.sin(math.radians(th)), 26 * ts * math.cos(math.radians(th)))   # where the hand holds it (the collar), from the spout, tipped
    mouth = (H[0] - mid[0], H[1] - mid[1])
    tin = (f'<g class="tilt" style="transform-origin:{f(H[0])}px {f(H[1])}px">'
           f'<g transform="translate({f(mouth[0])} {f(mouth[1])}) scale({ts})">{shaker(th)}</g></g>')
    rest_r = tux_arm([(24, -110), (32, -86), (22, -70)])
    # his left arm (viewer's left, the tattooed one): at his waist, then out straight with the pistol, aimed off to the left
    rest_l = tux_arm([(-24, -110), (-32, -86), (-20, -70)])
    G = (-80, -118)
    gun_arm = (f'<g transform="translate({G[0] - 4} {G[1] - 3}) scale(-1 1)">{pistol()}</g>'
               + tux_arm([(-24, -110), (-52, -115), G]))
    phil = (f'<g class="lrest">{rest_l}</g>' + tux_body()
            + f'<g class="hpour">{h_pour}</g><g class="hdraw">{h_draw}</g>'
            + f'<g class="apour">{arm_pour}{tin}</g><g class="arest">{rest_r}</g>'
            + f'<g class="lgun" style="transform-origin:-24px -110px">{gun_arm}</g>')
    css += ['.hpour,.apour,.lrest,.stream,.whoosh,.ting{opacity:0}']
    anim('hpour', shown(0, DRAW) [:-1] + [(BACK, 'opacity:0'), (BACK + .5, 'opacity:1'), (100, 'opacity:1')])
    anim('hdraw', shown(DRAW, BACK))
    anim('apour', shown(0, DOWN)[:-1] + [(BACK, 'opacity:0'), (BACK + .5, 'opacity:1'), (100, 'opacity:1')])
    anim('arest', [(0, 'opacity:0'), (DOWN - .5, 'opacity:0'), (DOWN, 'opacity:1'), (BACK, 'opacity:1'), (BACK + .5, 'opacity:0'), (100, 'opacity:0')])
    anim('lrest', shown(0, DRAW)[:-1] + [(BACK, 'opacity:0'), (BACK + .5, 'opacity:1'), (100, 'opacity:1')])
    anim('lgun', [(0, 'opacity:0;transform:rotate(-70deg)'), (DRAW, 'opacity:0;transform:rotate(-70deg)'), (DRAW + .3, 'opacity:1;transform:rotate(-70deg)'),
                  (DRAW + 2.5, 'opacity:1;transform:rotate(6deg)'), (DRAW + 4, 'opacity:1;transform:rotate(0)'), (BACK, 'opacity:1;transform:rotate(0)'),
                  (BACK + .5, 'opacity:0;transform:rotate(0)'), (100, 'opacity:0;transform:rotate(-70deg)')])
    anim('tilt', [(0, 'transform:rotate(-75deg)'), (TIP[0], 'transform:rotate(-75deg)'), (TIP[1], 'transform:rotate(0)'), (UNTIP[0], 'transform:rotate(0)'),
                  (UNTIP[1], 'transform:rotate(-75deg)'), (100, 'transform:rotate(-75deg)')])
    # the stream, outlined so it reads against the wall, from the tin's mouth into the bowl
    mx, my = PX + mouth[0], PY + mouth[1]
    apex = (gx, gy - 46.5 * gs)
    path = f'M{f(mx)} {f(my + 2)} Q{f(apex[0] - 2)} {f(my + 6)} {f(apex[0])} {f(apex[1] - 2)}'
    stream = (lines(f'<path d="{path}" stroke-width="6.4"/>', boil=False) + lines(f'<path d="{path}" stroke="#eef1dc" stroke-width="3.6"/>', boil=False))
    anim('stream', shown(POUR[0], POUR[1]))
    # the glass: the Martini fills it from the point up (a cone scaled from its point fills like a cone), then the olives drop in
    liquid = f'<g class="liq" style="transform-origin:0px -46.5px"><path d="{g["inner"]}" fill="#e6eac2"/><path d="M-31 -78 H31" stroke="#c9cfa0" stroke-width="1.6"/></g>'
    anim('liq', [(0, 'transform:scale(0)'), (POUR[0], 'transform:scale(0)'), (POUR[1], 'transform:scale(1)'), (BACK, 'transform:scale(1)'), (BACK + .5, 'transform:scale(0)'), (100, 'transform:scale(0)')])
    olive = f'<g class="olv">{garnishes(["olives"], "martini")}</g>'
    anim('olv', [(0, 'opacity:0;transform:translateY(-30px)'), (OLIVES, 'opacity:0;transform:translateY(-30px)'), (OLIVES + .5, 'opacity:1;transform:translateY(-30px)'),
                 (OLIVES + 3, 'opacity:1;transform:translateY(0)'), (BACK, 'opacity:1;transform:translateY(0)'), (BACK + .5, 'opacity:0'), (100, 'opacity:0')])
    the_glass = (f'<g transform="translate({gx} {gy}) scale({gs})">' + wash(g['back'])
                 + f'<clipPath id="bond-cone"><path d="{g["inner"]}"/></clipPath><g clip-path="url(#bond-cone)">{wash(liquid)}</g>'
                 + lines(g['out'], boil=False) + olive + '</g>')
    # the shaker, set down on the bar
    tin_bar = f'<g class="tinbar" transform="translate(206 {f(gy - 48 * ts)}) scale({ts})">{shaker(0, cap=True)}</g>'
    anim('tinbar', [(0, 'opacity:0'), (DOWN - .5, 'opacity:0'), (DOWN, 'opacity:1'), (BACK, 'opacity:1'), (BACK + .5, 'opacity:0'), (100, 'opacity:0')])
    # the draw: motion lines where the arm swept up, and a glint off the pistol
    gxs, gys = PX + G[0], PY + G[1]
    whoosh = lines(f'<path d="M{gxs + 6} {gys + 26} q-10 -8 -12 -20 M{gxs + 16} {gys + 30} q-9 -10 -10 -22 M{gxs + 26} {gys + 32} q-6 -10 -6 -20" stroke="#f2c776" stroke-width="2"/>', boil=False)
    anim('whoosh', shown(DRAW + 1, DRAW + 8, 1))
    ting = sparkle(gxs - 26, gys - 22, 7, '')
    anim('ting', shown(DRAW + 4, DRAW + 16, 1))
    inner = (wall + sparkle(352, 40, 5, 'twinkle d2') + sparkle(300, 24, 4, 'twinkle')
             + place(phil, PX, PY) + counter_front() + the_glass + tin_bar + f'<g class="stream">{stream}</g>'
             + f'<g class="whoosh">{whoosh}</g><g class="ting">{ting}</g>')
    alt = ('Phil, the bartender, in a tuxedo and bow tie, tips a shaker over a Martini glass on the bar and pours; the glass fills. '
           'He sets the shaker down, the olives drop in, then he quick-draws a pistol, aims it off to the side like a movie spy, and winks.')
    return svg_view(inner, alt, '20 6 360 200'), css


def write(folder):
    """Write both scenes into the drink's scenes folder; return their CSS."""
    css = []
    for name, fn in (('chalkboard', chalkboard), ('bond', bond)):
        svg, c = fn()
        (folder / 'scenes' / f'{name}.svg').write_text(svg + '\n')
        css += c
    return '\n'.join(css) + '\n'
