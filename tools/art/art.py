"""Crayon art helpers for The Liquor Cabinet (house style: watercolor washes + plum crayon lines).

Every drawing is plain SVG. Fills go through the kit's #wash filter, lines through #boil
(characters, they "boil" like hand-drawn animation) or #crayon (props and scenery).
Characters are built in local coordinates with their feet at (0, 0), up is negative y.
"""
import math

INK = '#5b2c4c'
DARK = '#3b2233'
SKIN = '#f0c39d'
BLUSH = '#e48b7c'


def f(n):
    return ('%.1f' % n).rstrip('0').rstrip('.')


def pts(points):
    return ' '.join(f'{f(x)} {f(y)}' for x, y in points)


def wash(inner, extra=''):
    return f'<g filter="url(#wash)"{extra}>{inner}</g>'


def lines(inner, width=2.6, boil=True, color=INK, extra=''):
    flt = 'boil' if boil else 'crayon'
    return (f'<g filter="url(#{flt})" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}>{inner}</g>')


def limb(path_pts, w0, w1):
    """A tapered tube along a polyline: returns the closed outline path 'd'."""
    n = len(path_pts)
    left, right = [], []
    for i, (x, y) in enumerate(path_pts):
        if i == 0:
            dx, dy = path_pts[1][0] - x, path_pts[1][1] - y
        elif i == n - 1:
            dx, dy = x - path_pts[i - 1][0], y - path_pts[i - 1][1]
        else:
            dx, dy = path_pts[i + 1][0] - path_pts[i - 1][0], path_pts[i + 1][1] - path_pts[i - 1][1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    ring = left + right[::-1]
    d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in ring) + 'Z'
    return d


def arm(points, sleeve, hand_r=5.2, w0=11, w1=9, skin=SKIN):
    """A sleeved arm ending in a hand. Returns (fill svg, line svg)."""
    d = limb(points, w0, w1)
    hx, hy = points[-1]
    fill = f'<path d="{d}" fill="{sleeve}"/><circle cx="{f(hx)}" cy="{f(hy)}" r="{hand_r}" fill="{skin}"/>'
    line = f'<path d="{d}"/><circle cx="{f(hx)}" cy="{f(hy)}" r="{hand_r}"/>'
    return fill, line


def part(fill, line, cls='', origin=None, extra=''):
    """A movable piece (an arm, a head) with its own wash + boil, optionally animated.
    A fixed tilt (transform attribute) goes on its own outer group: Safari applies a CSS
    transform-origin to an SVG transform attribute too, which knocked heads off bodies."""
    style = f' style="transform-origin:{f(origin[0])}px {f(origin[1])}px"' if origin and cls else ''
    c = f' class="{cls}"' if cls else ''
    inner = f'<g{c}{style}>{wash(fill)}{lines(line)}</g>' if (c or style) else wash(fill) + lines(line)
    return f'<g{extra}>{inner}</g>' if extra else (inner if (c or style) else f'<g>{inner}</g>')


def place(inner, x, y, s=1.0, cls='', origin=None, flip=False):
    """Put a character (feet at 0,0) at x,y. An inner class group can be animated by CSS."""
    sx = -s if flip else s
    c = f' class="{cls}"' if cls else ''
    style = f' style="transform-origin:{f(origin[0])}px {f(origin[1])}px"' if origin else ''
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(sx)} {f(s)})"><g{c}{style}>{inner}</g></g>'


# ---------------------------------------------------------------- people

def face(cx, cy, rx=15, ry=16.5, mood='smile', glasses=False, mustache=False, blush=True, skin=SKIN, eyes='dot'):
    fill = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{skin}"/>'
    fill += f'<ellipse cx="{cx - rx + 1}" cy="{cy + 1}" rx="3" ry="4.4" fill="{skin}"/><ellipse cx="{cx + rx - 1}" cy="{cy + 1}" rx="3" ry="4.4" fill="{skin}"/>'
    if blush:
        fill += f'<ellipse cx="{cx - 8.5}" cy="{cy + 6}" rx="4" ry="2.6" fill="{BLUSH}" opacity=".6"/><ellipse cx="{cx + 8.5}" cy="{cy + 6}" rx="4" ry="2.6" fill="{BLUSH}" opacity=".6"/>'
    line = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>'
    line += f'<path d="M{cx - rx + .5} {cy - 2} q-3.5 3 0 7"/><path d="M{cx + rx - .5} {cy - 2} q3.5 3 0 7"/>'
    ey = cy - 1
    if eyes == 'dot':
        line += f'<circle cx="{cx - 6}" cy="{ey}" r="1.6" fill="{DARK}" stroke="none"/><circle cx="{cx + 6}" cy="{ey}" r="1.6" fill="{DARK}" stroke="none"/>'
    elif eyes == 'x':
        line += f'<path d="M{cx - 8.5} {ey - 2.5} l5 5 M{cx - 3.5} {ey - 2.5} l-5 5 M{cx + 3.5} {ey - 2.5} l5 5 M{cx + 8.5} {ey - 2.5} l-5 5" stroke-width="1.9"/>'
    elif eyes == 'closed':
        line += f'<path d="M{cx - 8.5} {ey} q2.5 2 5 0 M{cx + 3.5} {ey} q2.5 2 5 0" stroke-width="1.8"/>'
    elif eyes == 'happy':
        line += f'<path d="M{cx - 8.5} {ey + 1} q2.5 -3.5 5 0 M{cx + 3.5} {ey + 1} q2.5 -3.5 5 0" stroke-width="1.9"/>'
    elif eyes == 'squeeze':   # screwed shut: > <
        line += f'<path d="M{cx - 8.5} {ey - 2.8} l4.6 2.8 l-4.6 2.8 M{cx + 8.5} {ey - 2.8} l-4.6 2.8 l4.6 2.8" stroke-width="1.9"/>'
    elif eyes == 'side':
        line += f'<circle cx="{cx - 4}" cy="{ey}" r="1.6" fill="{DARK}" stroke="none"/><circle cx="{cx + 8}" cy="{ey}" r="1.6" fill="{DARK}" stroke="none"/>'
    if glasses:
        line += (f'<circle cx="{cx - 6}" cy="{ey}" r="4.8" stroke-width="1.7"/><circle cx="{cx + 6}" cy="{ey}" r="4.8" stroke-width="1.7"/>'
                 f'<path d="M{cx - 1.2} {ey} h2.4 M{cx - 10.8} {ey - .6} L{cx - rx + 1} {ey - 2} M{cx + 10.8} {ey - .6} L{cx + rx - 1} {ey - 2}" stroke-width="1.6"/>')
    if mustache:
        fill += f'<path d="M{cx - 6} {cy + 7.5} q6 -4 12 0 q-6 2.5 -12 0Z" fill="#cfc6bd"/>'
        line += f'<path d="M{cx - 6} {cy + 7.5} q6 -4 12 0" stroke-width="1.8"/>'
    if mood == 'smile':
        line += f'<path d="M{cx - 4.5} {cy + 9.5} q4.5 4 9 0" stroke-width="2"/>'
    elif mood == 'grin':
        fill += f'<path d="M{cx - 7.5} {cy + 7} q7.5 10 15 0Z" fill="#fbf3e3"/>'
        line += f'<path d="M{cx - 7.5} {cy + 7} q7.5 10 15 0Z" stroke-width="2"/>'
    elif mood == 'sad':
        line += f'<path d="M{cx - 4.5} {cy + 11.5} q4.5 -3.5 9 0" stroke-width="2"/>'
    elif mood == 'wail':      # open, wobbly frown
        fill += f'<path d="M{cx - 5.5} {cy + 13.5} q5.5 -7.5 11 0 q-5.5 2.6 -11 0Z" fill="#7d2f58"/>'
        line += f'<path d="M{cx - 5.5} {cy + 13.5} q5.5 -7.5 11 0 q-5.5 2.6 -11 0Z" stroke-width="1.9"/>'
    elif mood == 'o':
        line += f'<ellipse cx="{cx}" cy="{cy + 10}" rx="2.6" ry="3.2" stroke-width="1.8"/>'
    elif mood == 'flat':
        line += f'<path d="M{cx - 4} {cy + 10} h8" stroke-width="2"/>'
    elif mood == 'smug':
        line += f'<path d="M{cx - 4} {cy + 10} q4 1.5 8 -1.5" stroke-width="2"/>'
    elif mood == 'goofy':
        fill += f'<path d="M{cx - 6} {cy + 8} q6 7 12 0Z" fill="#c0583c"/>'
        line += f'<path d="M{cx - 6} {cy + 8} q6 7 12 0Z" stroke-width="1.9"/>'
    return fill, line


def bill(pose='stand', mood='smile', head_tilt=0, arm_l=None, arm_r=None, suit='#6d7f99', arm_cls=('', ''), arm_origin=True, front_l=False, eyes='dot', holding_r=''):
    """Bill Samuels Sr.: fedora, round glasses, grey mustache, slate suit, plum tie."""
    fill, line = '', ''
    # shoes + trousers
    fill += '<ellipse cx="-11" cy="-3.5" rx="10.5" ry="4.6" fill="#4a3426"/><ellipse cx="11" cy="-3.5" rx="10.5" ry="4.6" fill="#4a3426"/>'
    fill += f'<path d="M-17 -64 L-15 -7 L-4 -7 L-1.5 -58 L1.5 -58 L4 -7 L15 -7 L17 -64Z" fill="{suit}"/>'
    line += '<ellipse cx="-11" cy="-3.5" rx="10.5" ry="4.6"/><ellipse cx="11" cy="-3.5" rx="10.5" ry="4.6"/>'
    line += '<path d="M-17 -64 L-15 -7 L-4 -7 L-1.5 -58 M1.5 -58 L4 -7 L15 -7 L17 -64"/>'
    # jacket, shirt, tie
    fill += f'<path d="M-24 -116 Q-27 -90 -22 -58 L22 -58 Q27 -90 24 -116 Q12 -124 0 -122 Q-12 -124 -24 -116Z" fill="{suit}"/>'
    fill += '<path d="M-9 -121 L0 -97 L9 -121Z" fill="#fbf3e3"/><path d="M-3 -119 L3 -119 L5 -93 L0 -85 L-5 -93Z" fill="#8b3a63"/>'
    line += '<path d="M-24 -116 Q-27 -90 -22 -58 L22 -58 Q27 -90 24 -116 Q12 -124 0 -122 Q-12 -124 -24 -116Z"/>'
    line += '<path d="M-9 -121 L0 -97 L9 -121" stroke-width="2"/><path d="M-3 -119 L3 -119 L5 -93 L0 -85 L-5 -93Z" stroke-width="1.8"/>'
    line += '<circle cx="0" cy="-76" r="1.6" fill="#3b2233" stroke="none"/><circle cx="0" cy="-67" r="1.6" fill="#3b2233" stroke="none"/>'
    body = part(fill, line)
    # head + fedora
    hf, hl = face(0, -141, glasses=True, mustache=True, mood=mood, eyes=eyes)
    hf = '<rect x="-5" y="-129" width="10" height="9" fill="#f0c39d"/>' + hf
    hf += '<path d="M-15.5 -148 q-1 6 1 9 M15.5 -148 q1 6 -1 9" fill="none" stroke="#cfc6bd" stroke-width="3"/>'
    hf += '<ellipse cx="0" cy="-155" rx="24" ry="4.8" fill="#7a5f4a"/><path d="M-14.5 -155 Q-16 -171 -6 -173 Q0 -169 6 -173 Q16 -171 14.5 -155Z" fill="#7a5f4a"/>'
    hl += '<ellipse cx="0" cy="-155" rx="24" ry="4.8"/><path d="M-14.5 -155 Q-16 -171 -6 -173 Q0 -169 6 -173 Q16 -171 14.5 -155"/>'
    hl += f'<path d="M-14.3 -159.5 L14.3 -159.5" stroke="{DARK}" stroke-width="3.2"/>'
    head = part(hf, hl, origin=(0, -125), extra=f' transform="rotate({head_tilt} 0 -125)"' if head_tilt else '')
    # arms (defaults hang down)
    al = arm_l or [(-22, -113), (-27, -88), (-25, -66)]
    ar = arm_r or [(22, -113), (27, -88), (25, -66)]
    af, aL = arm(al, suit)
    bf, bL = arm(ar, suit)
    left = part(af, aL, cls=arm_cls[0], origin=al[0] if arm_origin else None)
    right = part(bf, bL, cls=arm_cls[1], origin=ar[0] if arm_origin else None)
    right += holding_r
    if front_l:   # left arm folded across the front of the body
        return body + head + left + right
    return left + body + head + right


def everyman(mood='smile', arm_l=None, arm_r=None, arm_cls=('', ''), head_cls='', head_tilt=0, eyes='dot', holding_r='',
             top='#9db08a', pants='#8c7a6b', tie='#c0583c', hat='cap', hair='#6b4632', press=False, extra_head='', holding_l='', parts=False):
    """Our lovely consumer: flat cap, bow tie, green cardigan. Re-dressed, he plays Bill Jr. and the reporter."""
    fill, line = '', ''
    fill += '<ellipse cx="-11" cy="-3.5" rx="10" ry="4.6" fill="#5a4636"/><ellipse cx="11" cy="-3.5" rx="10" ry="4.6" fill="#5a4636"/>'
    fill += f'<path d="M-16 -62 L-14 -7 L-4 -7 L-1.5 -56 L1.5 -56 L4 -7 L14 -7 L16 -62Z" fill="{pants}"/>'
    line += '<ellipse cx="-11" cy="-3.5" rx="10" ry="4.6"/><ellipse cx="11" cy="-3.5" rx="10" ry="4.6"/>'
    line += '<path d="M-16 -62 L-14 -7 L-4 -7 L-1.5 -56 M1.5 -56 L4 -7 L14 -7 L16 -62"/>'
    fill += f'<path d="M-23 -112 Q-27 -86 -21 -56 L21 -56 Q27 -86 23 -112 Q12 -119 0 -118 Q-12 -119 -23 -112Z" fill="{top}"/>'
    fill += '<path d="M-8 -117 L0 -100 L8 -117Z" fill="#fbf3e3"/>'
    line += '<path d="M-23 -112 Q-27 -86 -21 -56 L21 -56 Q27 -86 23 -112 Q12 -119 0 -118 Q-12 -119 -23 -112Z"/>'
    line += '<path d="M-8 -117 L0 -100 L8 -117 M0 -100 L0 -58" stroke-width="2"/>'
    line += ''.join(f'<circle cx="3.5" cy="{y}" r="1.5" fill="#3b2233" stroke="none"/>' for y in (-92, -80, -68))
    fill += f'<path d="M-8 -121 L-1 -117 L-8 -113Z M8 -121 L1 -117 L8 -113Z" fill="{tie}"/>'
    line += '<path d="M-8 -121 L-1 -117 L-8 -113Z M8 -121 L1 -117 L8 -113Z" stroke-width="1.6"/>'
    body = part(fill, line)
    hf, hl = face(0, -137, rx=15.5, ry=16, mood=mood, eyes=eyes)
    hf = '<rect x="-5" y="-125" width="10" height="8" fill="#f0c39d"/>' + hf
    hf += '<ellipse cx="2" cy="-139" rx="3.4" ry="4.2" fill="#e9a982"/>'
    hl += '<path d="M0 -142 q5 3 2 8" stroke-width="1.8"/>'
    if hat == 'cap':
        hf += '<path d="M-16 -146 Q-15 -160 2 -160 Q17 -159 16 -147 Q24 -146 25 -142 Q8 -142 -16 -146Z" fill="#9b7663"/>'
        hl += '<path d="M-16 -146 Q-15 -160 2 -160 Q17 -159 16 -147 Q24 -146 25 -142 Q8 -142 -16 -146Z"/>'
    elif hat == 'fedora':
        hf += '<ellipse cx="0" cy="-151" rx="24" ry="4.8" fill="#8a8f96"/><path d="M-14.5 -151 Q-16 -167 -6 -169 Q0 -165 6 -169 Q16 -167 14.5 -151Z" fill="#8a8f96"/>'
        hl += '<ellipse cx="0" cy="-151" rx="24" ry="4.8"/><path d="M-14.5 -151 Q-16 -167 -6 -169 Q0 -165 6 -169 Q16 -167 14.5 -151"/>'
        hl += '<path d="M-14.3 -155.5 L14.3 -155.5" stroke="#3b2233" stroke-width="3.2"/>'
        if press:
            hf += '<rect x="2" y="-166" width="12" height="9" fill="#fffaf1" transform="rotate(8 8 -161)"/>'
            hl += '<rect x="2" y="-166" width="12" height="9" stroke-width="1.2" transform="rotate(8 8 -161)"/>'
            hl += '<text class="letter" x="8" y="-159.4" font-size="4.6" text-anchor="middle" stroke="none" transform="rotate(8 8 -161)">PRESS</text>'
    elif hat == 'hair':
        hf += f'<path d="M-16 -140 Q-19 -160 0 -158 Q19 -160 16 -140 Q14 -150 4 -151 Q-2 -146 -9 -150 Q-14 -148 -16 -140Z" fill="{hair}"/>'
        hl += '<path d="M-16 -140 Q-19 -160 0 -158 Q19 -160 16 -140"/>'
    hf += extra_head
    head = part(hf, hl, cls=head_cls, origin=(0, -122), extra=f' transform="rotate({head_tilt} 0 -122)"' if head_tilt else '')
    al = arm_l or [(-21, -109), (-26, -86), (-24, -64)]
    ar = arm_r or [(21, -109), (26, -86), (24, -64)]
    af, aL = arm(al, top)
    bf, bL = arm(ar, top)
    left = f'<g class="{arm_cls[0]}" style="transform-origin:{f(al[0][0])}px {f(al[0][1])}px">{wash(af)}{lines(aL)}{holding_l}</g>'
    right = f'<g class="{arm_cls[1]}" style="transform-origin:{f(ar[0][0])}px {f(ar[0][1])}px">{wash(bf)}{lines(bL)}{holding_r}</g>'
    if parts:
        return {'left': left, 'body': body, 'head': head, 'right': right}
    return left + body + head + right


def posh(eyes='closed', mood='smug', arm_r=None, arm_cls=''):
    """The hoity-toity consumer: pearls, fur stole, nose in the air, martini in hand."""
    fill, line = '', ''
    fill += '<path d="M-7 -4 l-4 -14 h7Z M7 -4 l4 -14 h-7Z" fill="#3b2233"/>'
    fill += '<path d="M-20 -110 Q-30 -60 -34 -20 Q0 -12 34 -20 Q30 -60 20 -110 Q0 -118 -20 -110Z" fill="#b9a3c8"/>'
    line += '<path d="M-20 -110 Q-30 -60 -34 -20 Q0 -12 34 -20 Q30 -60 20 -110 Q0 -118 -20 -110Z"/>'
    line += '<path d="M-7 -16 L-8 -4 M7 -16 L8 -4" stroke-width="2.6"/>'
    fill += '<path d="M-24 -112 Q0 -96 24 -112 Q28 -100 20 -94 Q0 -86 -20 -94 Q-28 -100 -24 -112Z" fill="#efe4cf"/>'
    line += '<path d="M-24 -112 Q0 -96 24 -112 Q28 -100 20 -94 Q0 -86 -20 -94 Q-28 -100 -24 -112Z" stroke-width="2.2"/>'
    line += '<path d="M-18 -104 q3 2 5 0 M-6 -99 q3 2 5 0 M6 -100 q3 2 5 0 M16 -105 q3 2 5 0" stroke-width="1.5"/>'
    body = part(fill, line)
    hf, hl = face(0, -133, rx=14, ry=15.5, mood=mood, eyes=eyes)
    hf = '<rect x="-4.5" y="-122" width="9" height="8" fill="#f0c39d"/>' + hf
    hf += ''.join(f'<circle cx="{x}" cy="{-119 + abs(x) * .12}" r="2.3" fill="#fffaf1"/>' for x in (-8, -4, 0, 4, 8))
    hl += ''.join(f'<circle cx="{x}" cy="{-119 + abs(x) * .12}" r="2.3" stroke-width="1"/>' for x in (-8, -4, 0, 4, 8))
    hf += '<path d="M-15 -138 Q-17 -154 0 -153 Q17 -154 15 -138 Q12 -147 0 -147 Q-12 -147 -15 -138Z" fill="#6b4632"/><circle cx="2" cy="-158" r="7.5" fill="#6b4632"/>'
    hl += '<path d="M-15 -138 Q-17 -154 0 -153 Q17 -154 15 -138"/><circle cx="2" cy="-158" r="7.5"/>'
    hf += '<path d="M4 -136 q7 2 9 -3" fill="none"/>'
    hl += '<path d="M0 -137 q9 1 9 5 q-4 2 -8 0" stroke-width="1.8"/>'
    head = part(hf, hl, cls='posh-head', origin=(0, -118), extra=' transform="rotate(-14 0 -118)"')
    # arm with martini (her left, raised), other hand on hip
    af, aL = arm([(-19, -106), (-30, -84), (-14, -70)], '#b9a3c8')
    if arm_r:   # reaching for something instead of holding her martini
        bf, bL = arm(arm_r, '#b9a3c8')
        return part(af, aL) + body + head + part(bf, bL, cls=arm_cls, origin=arm_r[0])
    bf, bL = arm([(19, -106), (32, -98), (40, -118)], '#b9a3c8')
    glass = lines('<path d="M33 -138 L47 -138 L40 -128 Z M40 -128 L40 -119 M35 -119 L45 -119" stroke-width="2"/>', boil=False)
    glass = wash('<path d="M34 -137 L46 -137 L40 -129Z" fill="#cfe2d6"/><circle cx="38" cy="-134" r="1.7" fill="#7f9a6c"/>') + glass
    return part(af, aL) + body + head + part(bf, bL) + glass


def drunk(eyes='x'):
    """The very drunk working man: overalls, plaid shirt, stubble, a jug labeled bourbon."""
    fill, line = '', ''
    fill += '<ellipse cx="-12" cy="-4" rx="11" ry="5" fill="#4a3426"/><ellipse cx="12" cy="-4" rx="11" ry="5" fill="#4a3426"/>'
    line += '<ellipse cx="-12" cy="-4" rx="11" ry="5"/><ellipse cx="12" cy="-4" rx="11" ry="5"/>'
    fill += '<path d="M-21 -112 Q-26 -86 -21 -58 L21 -58 Q26 -86 21 -112 Q10 -119 0 -118 Q-10 -119 -21 -112Z" fill="#c0583c"/>'
    line += '<path d="M-21 -112 Q-26 -86 -21 -58 L21 -58 Q26 -86 21 -112 Q10 -119 0 -118 Q-10 -119 -21 -112Z"/>'
    line += '<path d="M-20 -100 h40 M-21 -88 h42 M-10 -116 v52 M10 -116 v52" stroke="#8f3a28" stroke-width="1.6"/>'
    fill += '<path d="M-16 -92 L16 -92 L18 -58 L16 -7 L4 -7 L1 -50 L-1 -50 L-4 -7 L-16 -7 L-18 -58Z" fill="#6f86a6"/>'
    line += '<path d="M-16 -92 L16 -92 L18 -58 L16 -7 L4 -7 L1 -50 M-1 -50 L-4 -7 L-16 -7 L-18 -58Z"/>'
    line += '<path d="M-14 -92 L-18 -116 M14 -92 L18 -116" stroke-width="3.2"/><circle cx="-14" cy="-90" r="2" fill="#e6b264"/><circle cx="14" cy="-90" r="2" fill="#e6b264"/>'
    body = part(fill, line)
    hf, hl = face(0, -137, rx=15.5, ry=16, mood='goofy', eyes=eyes, blush=False)
    hf = '<rect x="-5" y="-125" width="10" height="8" fill="#f0c39d"/>' + hf
    hf += '<circle cx="0" cy="-134" r="4.4" fill="#e0675a"/>'
    hl += '<circle cx="0" cy="-134" r="4.4" stroke-width="1.7"/>'
    hl += ''.join(f'<circle cx="{x}" cy="{y}" r=".9" fill="#5b2c4c" stroke="none"/>' for x, y in ((-9, -127), (-5, -124), (5, -124), (9, -127), (-11, -131), (11, -131), (0, -123)))
    hf += '<path d="M-15 -146 Q-12 -158 0 -158 Q12 -158 15 -146 Q8 -150 0 -149 Q-8 -150 -15 -146Z" fill="#7a5f4a"/>'
    hl += '<path d="M-15 -146 Q-12 -158 0 -158 Q12 -158 15 -146"/>'
    head = part(hf, hl, origin=(0, -122), extra=' transform="rotate(10 0 -122)"')
    af, aL = arm([(-20, -110), (-36, -96), (-44, -112)], '#c0583c')
    bf, bL = arm([(20, -110), (30, -88), (34, -70)], '#c0583c')
    jug = wash('<path d="M26 -66 Q24 -80 34 -82 L34 -88 L40 -88 L40 -82 Q50 -80 48 -66 Q50 -46 37 -44 Q24 -46 26 -66Z" fill="#c99b72"/><rect x="28" y="-70" width="18" height="11" rx="2" fill="#fbf3e3"/>')
    jug += lines('<path d="M26 -66 Q24 -80 34 -82 L34 -88 L40 -88 L40 -82 Q50 -80 48 -66 Q50 -46 37 -44 Q24 -46 26 -66Z"/><path d="M48 -74 q8 2 4 12" />', boil=False)
    jug += '<text class="letter" x="37" y="-62.3" font-size="6.4" text-anchor="middle">bourbon</text>'
    return part(af, aL) + body + head + part(bf, bL) + jug


# ---------------------------------------------------------------- props & scenery

def ground(y=206, x0=0, x1=400):
    return lines(f'<path d="M{x0} {y} Q{x0 + (x1 - x0) * .3} {y - 5} {x0 + (x1 - x0) * .5} {y - 1} T{x1} {y - 2}"/>', boil=False)


BOTTLE_BOX = '-13.7 -68 27.4 68'   # where a real bottle photo sits in place of the generic one (feet at 0,0)


def swappable(name, inner):
    """Mark a drawing the private review build may replace with a real photo (src/private/<name>)."""
    return f'<!--swap:{name}|{BOTTLE_BOX}-->{inner}<!--/swap-->'


def generic_bottle(x, y, s=1.0, cls='', origin=None, swap=None):
    """A plain whiskey bottle: no label art, no wax, no brand."""
    inner = wash('<path d="M-13 0 L-13 -38 Q-13 -46 -6 -50 L-5 -62 L5 -62 L6 -50 Q13 -46 13 -38 L13 0Z" fill="#c98a3c"/>'
                 '<rect x="-10" y="-30" width="20" height="16" rx="2" fill="#fbf3e3"/><rect x="-5.5" y="-68" width="11" height="7" rx="1.5" fill="#7a5f4a"/>')
    inner += lines('<path d="M-13 0 L-13 -38 Q-13 -46 -6 -50 L-5 -62 L5 -62 L6 -50 Q13 -46 13 -38 L13 0Z"/>'
                   '<rect x="-10" y="-30" width="20" height="16" rx="2" stroke-width="1.8"/><rect x="-5.5" y="-68" width="11" height="7" rx="1.5" stroke-width="1.8"/>', boil=False)
    if swap:
        inner = swappable(swap, inner)
    return place(inner, x, y, s, cls=cls, origin=origin)


def sparkle(x, y, r=7, cls='', fill='#f2c776'):
    c = f' class="{cls}"' if cls else ''
    return (f'<g{c} style="transform-origin:{f(x)}px {f(y)}px"><path d="M{f(x)} {f(y - r)} L{f(x + r * .28)} {f(y - r * .28)} L{f(x + r)} {f(y)} '
            f'L{f(x + r * .28)} {f(y + r * .28)} L{f(x)} {f(y + r)} L{f(x - r * .28)} {f(y + r * .28)} L{f(x - r)} {f(y)} L{f(x - r * .28)} {f(y - r * .28)}Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/></g>')


def svg(inner, label, w=400, h=236):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}">' + inner + '</svg>')


def margie_bust():
    """Margie Samuels, head and shoulders, for her door: 1950s curls, pearls, a sly smile."""
    fill, line = '', ''
    fill += '<path d="M-34 0 Q-34 -26 -14 -32 L14 -32 Q34 -26 34 0Z" fill="#c25c86"/>'
    line += '<path d="M-34 0 Q-34 -26 -14 -32 L14 -32 Q34 -26 34 0"/>'
    fill += '<path d="M-10 -33 L0 -20 L10 -33Z" fill="#fbf3e3"/>'
    line += '<path d="M-10 -33 L0 -20 L10 -33" stroke-width="2"/>'
    hf, hl = face(0, -52, rx=15, ry=16.5, mood='smile', eyes='happy')
    hf = '<rect x="-5" y="-40" width="10" height="9" fill="#f0c39d"/>' + hf
    hf += ''.join(f'<circle cx="{x}" cy="{-33 + abs(x) * .1}" r="2.4" fill="#fffaf1"/>' for x in (-10, -5, 0, 5, 10))
    hl += ''.join(f'<circle cx="{x}" cy="{-33 + abs(x) * .1}" r="2.4" stroke-width="1"/>' for x in (-10, -5, 0, 5, 10))
    hf += '<circle cx="-15" cy="-46" r="2.6" fill="#fffaf1"/><circle cx="15" cy="-46" r="2.6" fill="#fffaf1"/>'
    curls = [(-17, -58), (-16, -66), (-10, -71), (-2, -73), (6, -72), (13, -68), (17, -61)]
    hf += ''.join(f'<circle cx="{x}" cy="{y}" r="6.5" fill="#7a4a34"/>' for x, y in curls)
    hl += ''.join(f'<path d="M{x - 5} {y + 2} a5.5 5.5 0 1 1 10 0" stroke-width="2"/>' for x, y in curls)
    lips = '<path d="M-4 -41.5 q4 3 8 0" stroke="#c0583c" stroke-width="2.4"/>'
    return part(fill, line) + part(hf, hl + lips)


def margie(arm_l=None, arm_r=None, arm_cls=('', ''), mood='smile', eyes='happy'):
    """Margie Samuels, full length: 1950s polka-dot dress, belted waist, pearls, curls. Feet at 0,0."""
    fill, line = '', ''
    fill += '<ellipse cx="-8" cy="-3.6" rx="7.5" ry="3.8" fill="#7a4a34"/><ellipse cx="8" cy="-3.6" rx="7.5" ry="3.8" fill="#7a4a34"/>'
    line += '<ellipse cx="-8" cy="-3.6" rx="7.5" ry="3.8"/><ellipse cx="8" cy="-3.6" rx="7.5" ry="3.8"/>'
    fill += f'<rect x="-11" y="-30" width="6" height="25" fill="{SKIN}"/><rect x="5" y="-30" width="6" height="25" fill="{SKIN}"/>'
    line += '<path d="M-11 -28 V-6 M-5 -28 V-6 M5 -28 V-6 M11 -28 V-6" stroke-width="2"/>'
    dress = 'M-20 -113 Q-24 -96 -16 -82 L-36 -28 Q0 -20 36 -28 L16 -82 Q24 -96 20 -113 Q0 -120 -20 -113Z'
    fill += f'<path d="{dress}" fill="#c25c86"/>'
    fill += ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#fbf3e3" opacity=".85"/>' for x, y in
                    ((-20, -40), (-8, -50), (6, -38), (18, -52), (-12, -64), (10, -66), (24, -36), (-26, -33), (0, -30), (-2, -92), (12, -100), (-12, -102)))
    fill += '<rect x="-17" y="-84" width="34" height="6" rx="1.5" fill="#7d2f58"/><path d="M-10 -114 L0 -101 L10 -114Z" fill="#fbf3e3"/>'
    line += f'<path d="{dress}"/><rect x="-17" y="-84" width="34" height="6" rx="1.5" stroke-width="1.8"/><path d="M-10 -114 L0 -101 L10 -114" stroke-width="2"/>'
    body = part(fill, line)
    hf, hl = face(0, -133, rx=15, ry=16.5, mood=mood, eyes=eyes)
    hf = '<rect x="-5" y="-121" width="10" height="9" fill="#f0c39d"/>' + hf
    hf += ''.join(f'<circle cx="{x}" cy="{-114 + abs(x) * .1}" r="2.4" fill="#fffaf1"/>' for x in (-10, -5, 0, 5, 10))
    hl += ''.join(f'<circle cx="{x}" cy="{-114 + abs(x) * .1}" r="2.4" stroke-width="1"/>' for x in (-10, -5, 0, 5, 10))
    hf += '<circle cx="-15" cy="-127" r="2.6" fill="#fffaf1"/><circle cx="15" cy="-127" r="2.6" fill="#fffaf1"/>'
    curls = [(-17, -139), (-16, -147), (-10, -152), (-2, -154), (6, -153), (13, -149), (17, -142)]
    hf += ''.join(f'<circle cx="{x}" cy="{y}" r="6.5" fill="#7a4a34"/>' for x, y in curls)
    hl += ''.join(f'<path d="M{x - 5} {y + 2} a5.5 5.5 0 1 1 10 0" stroke-width="2"/>' for x, y in curls)
    hl += '<path d="M-4 -122.5 q4 3 8 0" stroke="#c0583c" stroke-width="2.4"/>'
    head = part(hf, hl)
    al = arm_l or [(-19, -108), (-25, -86), (-23, -66)]
    ar = arm_r or [(19, -108), (25, -86), (23, -66)]
    af, aL = arm(al, '#c25c86')
    bf, bL = arm(ar, '#c25c86')
    return part(af, aL, cls=arm_cls[0], origin=al[0]) + body + head + part(bf, bL, cls=arm_cls[1], origin=ar[0])
