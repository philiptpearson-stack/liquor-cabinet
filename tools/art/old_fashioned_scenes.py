"""The Cocktail Menu / Old Fashioned: Phil, circa 1820, at the chalkboard (Philip, Nov 14 2026). Written by menu_pages.write_drink.

chalkboard  Phil in an 1820s getup (top hat, high collar and cravat, waistcoat, tailcoat) taps a chalkboard that cycles through
            Julep, Smash, Flip, Fizz and Sling, each one ≠ Cocktail.
Base styles are the still frame (reduced motion): "Julep ≠ Cocktail". Keyframes carry the motion.
"""
from art import *
from bartender import bartender
from martini_scenes import kf, window, counter_front

CHALK, GOLD = '#f4f1e6', '#f2c776'
COAT, LAPEL, VEST, BREECHES, LINEN, HAT = '#2f4a3a', '#25392d', '#c99a3c', '#cdb98f', '#fbf6ea', '#26222b'
WORDS = ['Julep', 'Smash', 'Flip', 'Fizz', 'Sling']
T = 8.0   # seconds a loop: each word gets a fifth of it


def coat_arm(points):
    """A tailcoat sleeve to the wrist, a white shirt cuff, the hand."""
    (sx, sy), (ex, ey), (hx, hy) = points
    upper = limb([(sx, sy), (ex, ey)], 12.5, 11.5)
    fore = limb([(ex, ey), (hx, hy)], 11, 10)
    dx, dy = hx - ex, hy - ey
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    cx, cy = hx - ux * 7, hy - uy * 7
    cuff = 'M' + ' L'.join(f'{f(cx + a * nx * 6 + b * ux * 2.6)} {f(cy + a * ny * 6 + b * uy * 2.6)}' for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))) + 'Z'
    fill = (f'<path d="{upper}" fill="{COAT}"/><path d="{fore}" fill="{COAT}"/><path d="{cuff}" fill="{LINEN}"/>'
            f'<circle cx="{f(hx)}" cy="{f(hy)}" r="5.6" fill="{SKIN}"/>')
    line = f'<path d="{upper}"/><path d="{fore}"/><path d="{cuff}" stroke-width="1.6"/><circle cx="{f(hx)}" cy="{f(hy)}" r="5.6"/>'
    return part(fill, line)


def period_body():
    fill = f'<path d="M-17 -62 L-16 -2 L16 -2 L17 -62Z" fill="{BREECHES}"/>'
    line = '<path d="M-17 -62 L-16 -2 M16 -2 L17 -62"/>'
    coat = 'M-27 -113 Q-31 -86 -25 -52 L25 -52 Q31 -86 27 -113 Q12 -120 0 -119 Q-12 -120 -27 -113Z'
    vest = 'M-12 -115 L12 -115 L9 -60 L-9 -60Z'
    lapel_l, lapel_r = 'M-13 -118 L-9 -94 L-18 -103 L-21 -114Z', 'M13 -118 L9 -94 L18 -103 L21 -114Z'
    fill += f'<path d="{coat}" fill="{COAT}"/><path d="{vest}" fill="{VEST}"/><path d="{lapel_l}" fill="{LAPEL}"/><path d="{lapel_r}" fill="{LAPEL}"/>'
    line += f'<path d="{coat}"/><path d="{vest}" stroke-width="1.6"/><path d="{lapel_l}" stroke-width="1.6"/><path d="{lapel_r}" stroke-width="1.6"/>'
    fill += ''.join(f'<circle cx="0" cy="{y}" r="1.4" fill="#7a5a1c"/>' for y in (-100, -90, -80, -70))
    # the stock and the cravat, tied in a soft bow
    cravat = 'M0 -111 L-8 -115.5 L-7 -106Z M0 -111 L8 -115.5 L7 -106Z'
    fill += f'<rect x="-8" y="-121" width="16" height="9" rx="2" fill="{LINEN}"/><path d="{cravat}" fill="{LINEN}"/><circle cx="0" cy="-111" r="2.2" fill="{LINEN}"/>'
    line += f'<rect x="-8" y="-121" width="16" height="9" rx="2" stroke-width="1.4"/><path d="{cravat}" stroke-width="1.4"/>'
    return part(fill, line)


def collar_and_hat():
    """Drawn over the head: the shirt's collar points standing up by his cheeks, and a top hat."""
    points = 'M-8 -121 L-12.5 -130 L-4.5 -122Z M8 -121 L12.5 -130 L4.5 -122Z'
    crown = 'M-13 -194 L13 -194 L12 -159 L-12 -159Z'
    brim = 'M-23 -159 Q0 -153 23 -159 Q0 -164 -23 -159Z'
    fill = (f'<path d="{points}" fill="{LINEN}"/><path d="{crown}" fill="{HAT}"/><rect x="-12.2" y="-167" width="24.4" height="5" fill="#6b3a2a"/>'
            f'<path d="{brim}" fill="{HAT}"/>')
    line = f'<path d="{points}" stroke-width="1.4"/><path d="{crown}"/><path d="{brim}"/><path d="M8 -190 L8 -170" stroke="#5c5560" stroke-width="1.6"/>'
    return part(fill, line)


def not_equal(x, y):
    """A chalk ≠, drawn (the board's handwriting font has no ≠)."""
    return lines(f'<path d="M{x - 11} {y - 5} H{x + 11} M{x - 11} {y + 5} H{x + 11} M{x + 6} {y - 15} L{x - 6} {y + 15}"/>', boil=False, width=3, color=CHALK)


def chalkboard():
    css = [f'/* Old Fashioned: Phil, circa 1820, at the chalkboard ({T:g} s): Julep, Smash, Flip, Fizz, Sling, each one ≠ Cocktail. '
           'Still frame: Julep ≠ Cocktail. */']
    wall = wash('<rect x="0" y="0" width="400" height="236" fill="#6f5443"/>')
    board = (wash('<rect x="142" y="26" width="230" height="138" rx="4" fill="#2f3b36"/>')
             + lines('<rect x="142" y="26" width="230" height="138" rx="4" stroke="#9b7663" stroke-width="6"/>', boil=False))
    words = ''
    n = len(WORDS)
    for i, w in enumerate(WORDS):
        on, off = 100 * i / n, 100 * (i + 1) / n
        words += f'<text class="letter ofw w{i}" x="186" y="106" font-size="27" text-anchor="middle" style="fill:{CHALK}">{w}</text>'
        if i == 0:   # the first word shows from the start and comes back in at the end of the loop
            css += [f'.w0{{animation:w0 {T}s linear infinite}}',
                    kf('w0', [(0, 'opacity:1'), (off - 1.5, 'opacity:1'), (off, 'opacity:0'), (100 - 1.5, 'opacity:0'), (100, 'opacity:1')])]
        else:
            css += [f'.w{i}{{opacity:0;animation:w{i} {T}s linear infinite}}', window(f'w{i}', on, off - 1.5, 1.5)]
    eq = (not_equal(252, 97) + f'<text class="letter" x="315" y="106" font-size="25" text-anchor="middle" style="fill:{GOLD}">Cocktail</text>'
          + lines('<path d="M160 136 q30 -6 60 0 M268 136 q36 -7 80 0" stroke-width="1.6"/>', boil=False, width=1.6, color=CHALK))
    p = bartender(eyes='happy', mood='grin', parts=True)
    left = coat_arm([(-23, -110), (-29, -86), (-26, -64)])
    right = coat_arm([(23, -110), (44, -124), (60, -138)])
    phil = left + period_body() + p['head'] + collar_and_hat() + f'<g class="tap" style="transform-origin:23px -110px">{right}</g>'
    css += ['.tap{animation:tap 1.4s ease-in-out infinite}', kf('tap', [(0, 'transform:rotate(0)'), (50, 'transform:rotate(-7deg)'), (100, 'transform:rotate(0)')])]
    inner = wall + board + words + eq + place(phil, 100, 236, .95) + counter_front() + sparkle(346, 16, 6, 'twinkle')
    alt = ('Phil, the bartender, dressed for the 1820s in a top hat, high collar, cravat and tailcoat, taps a chalkboard. '
           'On it, one word after another, Julep, Smash, Flip, Fizz, Sling, each one not equal to Cocktail.')
    return svg_view(inner, alt, '20 6 360 200'), css


def write(folder):
    svg, css = chalkboard()
    (folder / 'scenes' / 'chalkboard.svg').write_text(svg + '\n')
    return '\n'.join(css) + '\n'
