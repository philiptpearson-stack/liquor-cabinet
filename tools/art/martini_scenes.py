"""The Cocktail Menu / Martini: Phil's two scenes (Philip, Nov 12 2026). Written by menu_pages.write_drink.

chalkboard  Phil at the chalkboard, puzzling out a long, complicated equation that ends with "= Martini???"
            (the board as on Shaken or Stirred?): the lines chalk on one after another, he scratches his head.
bond        Phil in a tux pours a Martini from a shaker, sets the shaker down, then quick-draws a pistol and winks.
            A generic tuxedoed spy: no names, numbers or logos.
Base styles are each scene's still frame (reduced motion); keyframes carry the motion.
"""
import math
from art import *
from menu_art import glass, GLASS
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
BT = 8.0             # seconds a loop
POUR = (8, 38)       # the shaker pours (%)
DOWN = 44            # the shaker's down on the bar
DRAW = 50            # the quick-draw (%)
BACK = 92            # everything back for the next loop


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


def shaker(tilt=0):
    """A shaker tin, its mouth at (0, 0) pointing up before it tips."""
    d = 'M-8 0 L8 0 L11 34 L-11 34Z'
    return (f'<g transform="rotate({tilt})">' + wash(f'<path d="{d}" fill="#c9c3b8"/><rect x="-9" y="-3" width="18" height="4" rx="1.5" fill="#b8b1a5"/>')
            + lines(f'<path d="{d}"/><rect x="-9" y="-3" width="18" height="4" rx="1.5" stroke-width="1.5"/><path d="M6 6 L8 28" stroke="#fffaf1" stroke-width="2.4"/>', boil=False, width=2.2)
            + '</g>')


def pistol():
    """A cartoon pistol, barrel up, its grip at (0, 0)."""
    slide = 'M-4 -30 L4 -30 L4 2 L-4 2Z'
    grip = 'M-4 0 L5 0 L7 13 L-2 13Z'
    guard = 'M4 -6 q7 0 7 6 q0 5 -6 5'
    return (wash(f'<path d="{slide}" fill="#3c3a44"/><path d="{grip}" fill="#2c2a33"/>')
            + lines(f'<path d="{slide}"/><path d="{grip}"/><path d="{guard}" stroke-width="1.6"/><path d="M-1.5 -30 V-34 M1.5 -30 V-34" stroke-width="1.6"/>'
                    '<path d="M-2 -24 H2 M-2 -19 H2" stroke="#6a6674" stroke-width="1.2"/>', boil=False, width=2))


def bond():
    css = [f'/* 2. Phil, in a tux ({BT:g} s): pours a Martini from the shaker ({POUR[0]}-{POUR[1]}%), sets it down, then quick-draws ({DRAW}%) '
           'and winks. Still frame: the pistol up, the Martini poured, the shaker on the bar. */']
    wall = wash('<rect x="0" y="0" width="400" height="236" fill="#3e2c3d"/>') + wash('<ellipse cx="150" cy="96" rx="120" ry="82" fill="#6b4a63" opacity=".55"/>')
    PX, PY, S = 136, 236, 1.0
    gx, gy, gs = 252, 176, .55             # the Martini glass on the bar
    # Phil's head, two ways: watching the pour (happy), then the wink
    h_pour = bartender(eyes='happy', mood='smile', parts=True)['head']
    h_draw = bartender(eyes='wink', mood='smug', parts=True)['head']
    left = tux_arm([(-24, -110), (-32, -86), (-20, -70)])           # hand at his waist
    # pouring arm: the hand out over the glass, the shaker tipped
    hand_pour = (64, -122)
    arm_pour = tux_arm([(24, -110), (46, -116), hand_pour])
    tin_pour = f'<g transform="translate({hand_pour[0] + 6} {hand_pour[1] - 4})">{shaker(118)}</g>'
    # the draw: the hand up by his face, the pistol pointing up
    hand_gun = (34, -146)
    arm_gun = tux_arm([(24, -110), (44, -122), hand_gun])
    gun = f'<g transform="translate({hand_gun[0]} {hand_gun[1] + 4}) rotate(8)">{pistol()}</g>'

    arm_rest = tux_arm([(24, -110), (32, -86), (22, -70)])        # the shaker's down: the hand back at his waist
    phil = (left + tux_body()
            + f'<g class="hpour">{h_pour}</g><g class="hdraw">{h_draw}</g>'
            + f'<g class="apour">{arm_pour}{tin_pour}</g><g class="arest">{arm_rest}</g>'
            + f'<g class="adraw" style="transform-origin:24px -110px">{gun}{arm_gun}</g>')
    css += [f'.apour{{opacity:0;animation:pour-on {BT}s linear infinite}}', kf('pour-on', [(0, 'opacity:1'), (DOWN - .5, 'opacity:1'), (DOWN, 'opacity:0'), (BACK, 'opacity:0'), (BACK + .5, 'opacity:1'), (100, 'opacity:1')]),
            f'.hpour{{opacity:0;animation:hpour {BT}s linear infinite}}', kf('hpour', [(0, 'opacity:1'), (DRAW, 'opacity:1'), (DRAW + .5, 'opacity:0'), (BACK, 'opacity:0'), (BACK + .5, 'opacity:1'), (100, 'opacity:1')]),
            f'.arest{{opacity:0;animation:arest {BT}s linear infinite}}', kf('arest', [(0, 'opacity:0'), (DOWN - .5, 'opacity:0'), (DOWN, 'opacity:1'), (DRAW, 'opacity:1'), (DRAW + .5, 'opacity:0'), (100, 'opacity:0')]),
            f'.hdraw{{animation:hdraw {BT}s linear infinite}}', kf('hdraw', [(0, 'opacity:0'), (DRAW, 'opacity:0'), (DRAW + .5, 'opacity:1'), (BACK, 'opacity:1'), (BACK + .5, 'opacity:0'), (100, 'opacity:0')]),
            f'.adraw{{animation:adraw {BT}s linear infinite}}',
            kf('adraw', [(0, 'opacity:0;transform:rotate(40deg)'), (DRAW, 'opacity:0;transform:rotate(40deg)'), (DRAW + .5, 'opacity:1;transform:rotate(40deg)'),
                         (DRAW + 3, 'opacity:1;transform:rotate(-6deg)'), (DRAW + 5, 'opacity:1;transform:rotate(0)'), (BACK, 'opacity:1;transform:rotate(0)'),
                         (BACK + .5, 'opacity:0;transform:rotate(0)'), (100, 'opacity:0;transform:rotate(40deg)')])]
    # where the tin's mouth lands in the scene, for the stream
    rim_y = gy + GLASS['martini']['rim'][0] * gs
    tip = (PX + (hand_pour[0] + 6) * S + 30, PY + (hand_pour[1] - 4) * S + 4)
    stream = lines(f'<path d="M{f(tip[0])} {f(tip[1])} Q{f(gx - 2)} {f(rim_y - 14)} {f(gx)} {f(gy - 50 * gs)}" stroke="#e8ecd8" stroke-width="3.2"/>', boil=False)
    css += [f'.stream{{opacity:0;animation:stream {BT}s linear infinite}}', window('stream', POUR[0] + 4, POUR[1] - 2, 1)]
    # the glass: empty, then full (fading in through the pour)
    g = GLASS['martini']
    empty = f'<g transform="translate({gx} {gy}) scale({gs})">' + wash(g['back']) + lines(g['out'], boil=False) + '</g>'
    full = f'<g class="full" transform="translate({gx} {gy}) scale({gs})">{glass("martini", "bond-m", "#eef0dc", ["olives"])}</g>'
    css += [f'.full{{animation:full {BT}s linear infinite}}', kf('full', [(0, 'opacity:0'), (POUR[0] + 6, 'opacity:0'), (POUR[1], 'opacity:1'), (BACK, 'opacity:1'), (BACK + 1, 'opacity:0'), (100, 'opacity:0')])]
    # the shaker, set down on the bar
    tin_bar = f'<g class="tinbar" transform="translate(206 {gy - 34})">{shaker(0)}</g>'
    css += [f'.tinbar{{animation:tinbar {BT}s linear infinite}}', kf('tinbar', [(0, 'opacity:0'), (DOWN - .5, 'opacity:0'), (DOWN, 'opacity:1'), (BACK, 'opacity:1'), (BACK + .5, 'opacity:0'), (100, 'opacity:0')])]
    # a flash of motion lines at the draw, and a twinkle on the wink
    whoosh = lines(f'<path d="M{PX + 50} {PY - 168} q10 -6 18 -2 M{PX + 56} {PY - 156} q10 -4 17 0 M{PX + 52} {PY - 180} q8 -7 16 -5" stroke="#f2c776" stroke-width="2"/>', boil=False)
    css += [f'.whoosh{{opacity:0;animation:whoosh {BT}s linear infinite}}', window('whoosh', DRAW + 1, DRAW + 7, 1)]
    inner = (wall + sparkle(44, 34, 6, 'twinkle') + sparkle(352, 40, 5, 'twinkle d2')
             + place(phil, PX, PY, S) + counter_front() + empty + f'<g class="stream">{stream}</g>' + full + tin_bar
             + f'<g class="whoosh">{whoosh}</g>' + sparkle(PX - 2, PY - 156, 5, 'twinkle d3'))
    alt = ('Phil, the bartender, in a tuxedo and bow tie, pours a Martini from a shaker into a glass on the bar. '
           'He sets the shaker down, then quick-draws a pistol, holds it up by his face like a movie spy, and winks.')
    return svg_view(inner, alt, '20 6 360 200'), css


def write(folder):
    """Write both scenes into the drink's scenes folder; return their CSS."""
    css = []
    for name, fn in (('chalkboard', chalkboard), ('bond', bond)):
        svg, c = fn()
        (folder / 'scenes' / f'{name}.svg').write_text(svg + '\n')
        css += c
    return '\n'.join(css) + '\n'
