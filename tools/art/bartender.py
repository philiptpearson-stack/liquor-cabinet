"""Philip, the bartender: host of The Bartender's Perspective.

Short swept-up brown hair, full beard, big grin. Grey-blue plaid shirt with the sleeves
rolled, a skinny black tie worn a little loose, black bar apron, dark jeans, and a
tattoo sleeve on his right forearm. For when he's being ridiculous: the googly-eyed hat.
Feet at (0, 0), up is negative y, same scale as the rest of the cast.
"""
from art import *

PLAID_ID = 'plaid'
# the shirt's plaid; it lives once per page in the shared defs (cast.svg)
PLAID = (f'<pattern id="{PLAID_ID}" width="7" height="7" patternUnits="userSpaceOnUse">'
         '<rect width="7" height="7" fill="#b4c0cd"/>'
         '<path d="M0 3.5h7M3.5 0v7" stroke="#8796aa" stroke-width="1.9" opacity=".6"/>'
         '<path d="M0 .8h7M.8 0v7" stroke="#e3e9ef" stroke-width=".7" opacity=".8"/></pattern>')
HAIR = '#7a4a2c'
BEARD = '#8a5a3a'
TIE = '#2b2730'
APRON = '#302a33'
DENIM = '#4b5a73'
TATTOO = '#355866'


def rolled_arm(points, tattoo=False):
    """Shoulder, elbow, hand: plaid to the elbow, a rolled cuff, bare forearm."""
    (sx, sy), (ex, ey), (hx, hy) = points
    upper = limb([(sx, sy), (ex, ey)], 12, 11)
    fore = limb([(ex, ey), (hx, hy)], 9.6, 8.4)
    # the rolled cuff: a short fat band across the elbow
    dx, dy = hx - ex, hy - ey
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    cx, cy = ex + ux * 2.5, ey + uy * 2.5
    cuff = 'M' + ' L'.join(f'{f(cx + a * nx * 7 + b * ux * 3.2)} {f(cy + a * ny * 7 + b * uy * 3.2)}' for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))) + 'Z'
    fill = (f'<path d="{fore}" fill="{SKIN}"/><circle cx="{f(hx)}" cy="{f(hy)}" r="5.4" fill="{SKIN}"/>'
            f'<path d="{upper}" fill="url(#{PLAID_ID})"/><path d="{cuff}" fill="url(#{PLAID_ID})"/>')
    line = f'<path d="{fore}"/><circle cx="{f(hx)}" cy="{f(hy)}" r="5.4"/><path d="{upper}"/><path d="{cuff}" stroke-width="2"/>'
    if tattoo:   # a few inky doodles down the forearm
        ink = ''
        for t, mark in ((.32, 'star'), (.55, 'wave'), (.78, 'dot')):
            px, py = ex + dx * t, ey + dy * t
            if mark == 'star':
                ink += f'<path d="M{f(px - 2.6)} {f(py)} h5.2 M{f(px)} {f(py - 2.6)} v5.2 M{f(px - 1.8)} {f(py - 1.8)} l3.6 3.6 M{f(px + 1.8)} {f(py - 1.8)} l-3.6 3.6"/>'
            elif mark == 'wave':
                ink += f'<path d="M{f(px - 3 * nx - 2 * ux)} {f(py - 3 * ny - 2 * uy)} q{f(2 * ux + 1.5 * nx)} {f(2 * uy + 1.5 * ny)} {f(3 * nx)} {f(3 * ny)} t{f(3 * nx)} {f(3 * ny)}"/>'
            else:
                ink += f'<circle cx="{f(px)}" cy="{f(py)}" r="1.5"/>'
        line += f'<g stroke="{TATTOO}" stroke-width="1.3">{ink}</g>'
    return fill, line


def bartender(mood='grin', eyes='happy', arm_l=None, arm_r=None, hat=None, holding='', parts=False, head_tilt=0):
    """arm_l is on the viewer's left (his right arm, the tattooed one)."""
    fill, line = '', ''
    # shoes, jeans, apron
    fill += '<ellipse cx="-11" cy="-3.5" rx="10.5" ry="4.6" fill="#3b2a22"/><ellipse cx="11" cy="-3.5" rx="10.5" ry="4.6" fill="#3b2a22"/>'
    line += '<ellipse cx="-11" cy="-3.5" rx="10.5" ry="4.6"/><ellipse cx="11" cy="-3.5" rx="10.5" ry="4.6"/>'
    fill += f'<path d="M-17 -62 L-15 -7 L-4 -7 L-1.5 -56 L1.5 -56 L4 -7 L15 -7 L17 -62Z" fill="{DENIM}"/>'
    line += '<path d="M-17 -62 L-15 -7 L-4 -7 L-1.5 -56 M1.5 -56 L4 -7 L15 -7 L17 -62"/>'
    # shirt
    shirt = 'M-25 -113 Q-29 -86 -22 -58 L22 -58 Q29 -86 25 -113 Q12 -120 0 -119 Q-12 -120 -25 -113Z'
    fill += f'<path d="{shirt}" fill="url(#{PLAID_ID})"/>'
    line += f'<path d="{shirt}"/>'
    # tie, worn a little loose and a little crooked
    fill += f'<path d="M-3 -114 L3 -114 L2.5 -109 L-2.5 -109Z M-2.5 -109 L2.5 -109 L5 -84 L1.5 -78 L-2 -84Z" fill="{TIE}"/>'
    line += '<path d="M-2.5 -109 L2.5 -109 L5 -84 L1.5 -78 L-2 -84Z" stroke-width="1.8"/>'
    # open collar
    fill += f'<path d="M-10 -120 L-3 -110 L-1 -117Z M10 -120 L3 -110 L1 -117Z" fill="url(#{PLAID_ID})"/>'
    line += '<path d="M-10 -120 L-3 -110 L-1 -117 M10 -120 L3 -110 L1 -117" stroke-width="1.8"/>'
    # bar apron, tied at the waist, with a towel tucked in
    apron = 'M-25 -66 L25 -66 L26.5 -30 Q0 -25 -26.5 -30Z'
    fill += f'<path d="{apron}" fill="{APRON}"/><path d="M14 -66 L22 -66 L21 -40 L15 -42Z" fill="#f4ede0"/>'
    line += f'<path d="{apron}"/><path d="M-25 -66 H25" stroke-width="3.2"/><path d="M-8 -52 h14 v12 h-14Z" stroke="#56505a" stroke-width="1.5"/>'
    line += '<path d="M14 -66 L22 -66 L21 -40 L15 -42Z" stroke-width="1.6"/><path d="M-25 -64 q-6 6 -3 14 M-25 -64 q-2 8 2 13" stroke-width="1.8"/>'
    body = part(fill, line)

    # head: grin, full beard, swept-up hair, brows
    hf, hl = face(0, -137, rx=15.5, ry=16, mood='flat' if mood == 'grin' else mood, eyes=eyes)
    hf = f'<rect x="-5.5" y="-125" width="11" height="9" fill="{SKIN}"/>' + hf
    hf += '<ellipse cx="2" cy="-139" rx="3.4" ry="4.2" fill="#e9a982"/>'
    hl += '<path d="M0 -142 q5 3 2 8" stroke-width="1.8"/>'
    beard = 'M-15.8 -140 Q-17.5 -126 -10 -119 Q0 -113.5 10 -119 Q17.5 -126 15.8 -140 L13 -137 Q12 -129 6.5 -130.5 Q0 -132.5 -6.5 -130.5 Q-12 -129 -13 -137Z'
    hf += f'<path d="{beard}" fill="{BEARD}"/>'
    hl += '<path d="M-15.8 -140 Q-17.5 -126 -10 -119 Q0 -113.5 10 -119 Q17.5 -126 15.8 -140" stroke-width="2"/>'
    hl += ''.join(f'<path d="M{x} {y} l{dx} 2" stroke="#6b4228" stroke-width="1.1"/>' for x, y, dx in ((-12, -128, 1.5), (-9, -123, 1), (9, -123, -1), (12, -128, -1.5), (-3, -119, .5), (3, -119, -.5)))
    if mood == 'grin':   # a big toothy grin, on top of the beard
        hl += '<path d="M-7.5 -130 q7.5 10 15 0Z" fill="#fbf3e3" stroke-width="2"/><path d="M-6.4 -128.4 h12.8" stroke-width="1"/>'
    # brows
    if eyes == 'wink':
        hl += f'<path d="M-10.5 -142.5 q4 1 8 0 M2.5 -146 q4.5 -3.4 8.5 -.5" stroke="{HAIR}" stroke-width="2.4"/>'
    else:
        hl += f'<path d="M-10.5 -145 q4 -2.4 8 -.6 M2.5 -145.6 q4 -1.8 8 .6" stroke="{HAIR}" stroke-width="2.4"/>'
    if hat == 'googly':   # the hat from the bar: a big black floppy creature with googly eyes
        tail = limb([(13, -165), (27, -170), (37, -160), (41, -142), (38, -124)], 14, 8)   # floppy, flopped down past his ear
        dome = 'M-19.5 -141 Q-23 -171 -2 -174 Q19 -176 19.5 -142 Q9 -148 0 -147.5 Q-10 -148 -19.5 -141Z'
        hf += f'<path d="{tail}" fill="#262229"/><path d="{dome}" fill="#262229"/>'
        hf += '<circle cx="-7" cy="-160" r="5" fill="#fffaf1"/><circle cx="6" cy="-161" r="5" fill="#fffaf1"/>'
        hl += f'<path d="{tail}"/><path d="{dome}"/><circle cx="-7" cy="-160" r="5" stroke-width="1.6"/><circle cx="6" cy="-161" r="5" stroke-width="1.6"/>'
        hl += ('<g class="googly" style="transform-origin:-7px -160px"><circle cx="-5.4" cy="-158.6" r="2.3" fill="#262229" stroke="none"/></g>'
               '<g class="googly g2" style="transform-origin:6px -161px"><circle cx="7.8" cy="-159.4" r="2.3" fill="#262229" stroke="none"/></g>')
    else:
        hair = 'M-15.8 -142 Q-17.5 -154 -10 -158 Q-4 -163 5 -162 Q15 -161 16.5 -151 Q17 -146 15.8 -142 Q14 -149 8 -151.5 Q2 -150 -4 -152 Q-10 -150 -13 -150.5 Q-15 -147 -15.8 -142Z'
        hf += f'<path d="{hair}" fill="{HAIR}"/>'
        hl += '<path d="M-15.8 -142 Q-17.5 -154 -10 -158 Q-4 -163 5 -162 Q15 -161 16.5 -151 Q17 -146 15.8 -142"/><path d="M-3 -158.5 q5 -3 11 -1.5 M0 -155 q4 -2.4 9 -1" stroke-width="1.5"/>'
    head = part(hf, hl, origin=(0, -122), extra=f' transform="rotate({head_tilt} 0 -122)"' if head_tilt else '')

    al = arm_l or [(-23, -110), (-29, -86), (-26, -64)]
    ar = arm_r or [(23, -110), (29, -86), (26, -64)]
    lf, ll = rolled_arm(al, tattoo=True)
    rf, rl = rolled_arm(ar)
    left, right = part(lf, ll), part(rf, rl) + holding
    if parts:
        return {'left': left, 'body': body, 'head': head, 'right': right}
    return left + body + head + right
