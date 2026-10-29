"""The liquor store shelves, shared by The Founder's Gamble and the WSJ page."""
from art import *


def decanter(x, base, w=26, h=34, color='#c98a3c', label=None, label_fill='#f2c776', s=1.0):
    top = base - h
    d = (f'M{f(x - w / 2)} {f(base)} V{f(top + 7)} Q{f(x - w / 2)} {f(top)} {f(x - w / 2 + 7)} {f(top)} H{f(x - 4)} V{f(top - 7)} '
         f'H{f(x + 4)} V{f(top)} H{f(x + w / 2 - 7)} Q{f(x + w / 2)} {f(top)} {f(x + w / 2)} {f(top + 7)} V{f(base)}Z')
    lab_y = base - h * .62
    out = wash(f'<path d="{d}" fill="{color}"/><circle cx="{f(x)}" cy="{f(top - 11)}" r="4.6" fill="{color}"/>'
               f'<rect x="{f(x - w / 2 + 4)}" y="{f(lab_y)}" width="{f(w - 8)}" height="11" rx="1.5" fill="{label_fill}"/>')
    out += lines(f'<path d="{d}"/><circle cx="{f(x)}" cy="{f(top - 11)}" r="4.6"/><rect x="{f(x - w / 2 + 4)}" y="{f(lab_y)}" width="{f(w - 8)}" height="11" rx="1.5" stroke-width="1.6"/>', boil=False, width=2.2)
    if label:
        out += f'<text class="letter" x="{f(x)}" y="{f(lab_y + 8.2)}" font-size="7" text-anchor="middle">{label}</text>'
    return out


def plain_bottle(x, base, h, color):
    t = base - h
    d = f'M{x - 9} {base} L{x - 9} {t + 14} Q{x - 9} {t + 6} {x - 3} {t + 3} L{x - 3} {t} L{x + 3} {t} L{x + 3} {t + 3} Q{x + 9} {t + 6} {x + 9} {t + 14} L{x + 9} {base}Z'
    return wash(f'<path d="{d}" fill="{color}" opacity=".85"/>') + lines(f'<path d="{d}" stroke-width="2"/>', boil=False)


def jug(x, base, s=1.0, label='Bourbon'):
    """The cheap stuff: a stoneware jug. Feet at (x, base)."""
    J = 'M-18 -16 Q-20 -30 -6 -33 L-6 -40 L2 -40 L2 -33 Q16 -30 14 -16 Q16 0 -2 0 Q-20 0 -18 -16Z'
    body = wash(f'<path d="{J}" fill="#c99b72"/><rect x="-7" y="-44" width="10" height="5" rx="1.5" fill="#9b7663"/>'
                + ('<rect x="-17" y="-24" width="30" height="12" rx="2" fill="#fbf3e3"/>' if label else ''))
    body += lines(f'<path d="{J}"/><path d="M14 -26 q10 2 4 14"/><rect x="-7" y="-44" width="10" height="5" rx="1.5" stroke-width="1.6"/>', boil=False)
    if label:
        body += f'<text class="letter" x="-2" y="-15.2" font-size="7.6" text-anchor="middle">{label}</text>'
    return f'<g transform="translate({f(x)} {f(base)}) scale({f(s)})">{body}</g>'


def tag(x, y, text, size=11, w=None, tilt=-6, cls=''):
    """A price tag hanging on a string from (x, y)."""
    w = w or (size * .62 * len(text) + 12)
    c = f' class="{cls}" style="transform-origin:{f(x)}px {f(y)}px"' if cls else ''
    t = (wash(f'<path d="M{f(x - w / 2)} {f(y + 8)} H{f(x + w / 2)} V{f(y + 8 + size + 7)} H{f(x - w / 2)}Z" fill="#fffaf1"/>')
         + lines(f'<path d="M{f(x)} {f(y)} V{f(y + 8)}" stroke-width="1.4"/><path d="M{f(x - w / 2)} {f(y + 8)} H{f(x + w / 2)} V{f(y + 8 + size + 7)} H{f(x - w / 2)}Z" stroke-width="1.8"/>', boil=False)
         + f'<text class="letter" x="{f(x)}" y="{f(y + 8 + size + 2.2)}" font-size="{size}" text-anchor="middle">{text}</text>')
    return f'<g{c}><g transform="rotate({tilt} {f(x)} {f(y)})">{t}</g></g>'


SX0, SX1 = 152, 392                       # posts
TOP, MID, BOT = 86, 136, 192              # what sits on each shelf stands at these y's
def shelf_unit():
    boards = ''.join(f'<rect x="{SX0}" y="{y}" width="{SX1 - SX0 + 6}" height="7" fill="#b08463"/>' for y in (TOP, MID, BOT))
    out = wash(f'<rect x="{SX0}" y="30" width="{SX1 - SX0 + 6}" height="176" fill="#ead8c6" opacity=".55"/>'
               f'<rect x="{SX0 - 4}" y="26" width="{SX1 - SX0 + 14}" height="8" fill="#9b7663"/>{boards}'
               f'<rect x="{SX0}" y="{BOT + 7}" width="{SX1 - SX0 + 6}" height="{206 - BOT - 7}" fill="#9b7663"/>'
               f'<rect x="{SX0}" y="30" width="7" height="176" fill="#9b7663"/><rect x="{SX1 - 1}" y="30" width="7" height="176" fill="#9b7663"/>')
    out += lines(f'<rect x="{SX0 - 4}" y="26" width="{SX1 - SX0 + 14}" height="8"/>' + ''.join(f'<path d="M{SX0} {y} H{SX1 + 6} M{SX0} {y + 7} H{SX1 + 6}"/>' for y in (TOP, MID, BOT))
                 + f'<path d="M{SX0} 30 V206 M{SX1 + 6} 30 V206"/>', boil=False, width=2.2)
    sign = (wash('<rect x="226" y="4" width="96" height="19" rx="3" fill="#8b3a63"/>')
            + lines('<rect x="226" y="4" width="96" height="19" rx="3"/><path d="M246 23 V26 M302 23 V26" stroke-width="1.8"/>', boil=False)
            + '<text class="letter" x="274" y="18.6" font-size="12.5" text-anchor="middle" style="fill:#fffaf1;letter-spacing:.12em">LIQUORS</text>')
    return out + sign


def middle_row():
    return ''.join(plain_bottle(x, MID, h, c) for x, h, c in [(176, 24, '#8a8f96'), (204, 21, '#7f9a6c'), (234, 25, '#c9c3b8'), (290, 23, '#8a8f96'), (320, 20, '#7f9a6c'), (352, 25, '#c9c3b8')])


def shelf_label(x, board, text, size=10, tilt=-3):
    """A price card stuck to the front edge of a shelf."""
    w = size * .62 * len(text) + 10
    y = board - 1
    return (f'<g transform="rotate({tilt} {f(x)} {f(y + 7)})">'
            + wash(f'<rect x="{f(x - w / 2)}" y="{f(y)}" width="{f(w)}" height="{f(size + 6)}" rx="1.5" fill="#fffaf1"/>')
            + lines(f'<rect x="{f(x - w / 2)}" y="{f(y)}" width="{f(w)}" height="{f(size + 6)}" rx="1.5" stroke-width="1.6"/>', boil=False)
            + f'<text class="letter" x="{f(x)}" y="{f(y + size + 1.6)}" font-size="{size}" text-anchor="middle">{text}</text></g>')


def bottom_shelf():
    """Bourbon, down where nobody looks: dust, a cobweb, and a fly."""
    out = jug(244, BOT, s=1.15) + jug(298, BOT, s=.9, label=None)
    out += shelf_label(270, BOT, '¢', size=15, tilt=4)
    web = lines(f'<path d="M{SX1 - 1} {MID + 7} q-16 4 -24 24 M{SX1 - 1} {MID + 7} q-10 12 -10 30 M{SX1 - 1} {MID + 7} q-20 -2 -32 10 '
                f'M{SX1 - 12} {MID + 12} q4 6 2 12 M{SX1 - 20} {MID + 16} q4 8 0 16 M{SX1 - 28} {MID + 15} q6 4 4 10" stroke="#9a8a92" stroke-width="1.2"/>', boil=False)
    dust = lines(f'<path d="M196 {BOT - 3} q4 -3 8 0 q4 3 8 0 M298 {BOT - 3} q4 -3 8 0 q4 3 8 0 M330 {BOT - 3} q4 -3 8 0" stroke="#b9a69a" stroke-width="1.6"/>', boil=False)
    fly = ('<g transform="translate(270 154) scale(1.5)"><g class="fly-x"><g class="fly-y">'
           '<ellipse cx="-2.6" cy="-2.6" rx="3" ry="2" fill="#fffaf1" stroke="#5b2c4c" stroke-width="1" transform="rotate(30 -2.6 -2.6)"/>'
           '<ellipse cx="2.6" cy="-2.6" rx="3" ry="2" fill="#fffaf1" stroke="#5b2c4c" stroke-width="1" transform="rotate(-30 2.6 -2.6)"/>'
           '<circle r="2.4" fill="#3b2233"/></g></g></g>')
    return out + web + dust + fly


