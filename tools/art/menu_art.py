"""The Cocktail Menu: glasses, garnishes, bottles and ingredients.

Glasses are drawn in their own coordinates with the foot at (0, 0) and up negative, like the characters.
glass() draws one finished (full, iced, garnished) for heroes and door icons; the build scenes
(menu_build.py) use the same pieces, split up so each can move.
"""
import math
from art import *

# ---------------------------------------------------------------- glasses
# out: the crayon outline; back: the glass tint, behind the drink; inner: the inside (clip path);
# bottom / top: where the drink sits (inside bottom, full line); rim: (y, half width)
GLASS = {
    'coupe': dict(
        out='<path d="M-30 -68 Q0 -28 30 -68" stroke-width="2.4"/><path d="M-30 -68 Q0 -72 30 -68" stroke-width="1.6"/><path d="M0 -49 V-4 M-16 0 Q0 -6 16 0" stroke-width="2.4"/>',
        back='<path d="M-30 -68 Q0 -28 30 -68Z" fill="#e7f1fb" opacity=".35"/>',
        inner='M-28 -66 Q0 -32 28 -66Z', bottom=-49, top=-65, rim=(-68, 30),
        foam='M-27.4 -65.5 Q0 -70 27.4 -65.5 L24.6 -59.5 Q0 -55.5 -24.6 -59.5Z'),
    'martini': dict(
        out='<path d="M-34 -80 L0 -44 L34 -80" stroke-width="2.4"/><path d="M-34 -80 Q0 -84 34 -80" stroke-width="1.6"/><path d="M0 -44 V-4 M-17 0 Q0 -6 17 0" stroke-width="2.4"/>',
        back='<path d="M-34 -80 L0 -44 L34 -80Z" fill="#e7f1fb" opacity=".35"/>',
        inner='M-31 -78 L0 -46.5 L31 -78Z', bottom=-47, top=-74, rim=(-80, 34)),
    'rocks': dict(
        out='<path d="M-32 -60 L32 -60 L29 0 L-29 0Z" stroke-width="2.4"/><path d="M-28.6 -8 H28.6" stroke-width="1.6"/><path d="M-25.6 -52 L-26.4 -16" stroke="#fffaf1" stroke-width="2.6"/>',
        back='<path d="M-32 -60 L32 -60 L29 0 L-29 0Z" fill="#e7f1fb" opacity=".35"/>',
        inner='M-30 -58 L30 -58 L28.6 -8 L-28.6 -8Z', bottom=-8, top=-40, rim=(-60, 32)),
    'highball': dict(
        out='<path d="M-22 -104 L22 -104 L20 0 L-20 0Z" stroke-width="2.4"/><path d="M-19.6 -7 H19.6" stroke-width="1.6"/><path d="M-16.4 -94 L-15.4 -20" stroke="#fffaf1" stroke-width="2.6"/>',
        back='<path d="M-22 -104 L22 -104 L20 0 L-20 0Z" fill="#e7f1fb" opacity=".35"/>',
        inner='M-20 -102 L20 -102 L18.4 -7 L-18.4 -7Z', bottom=-7, top=-92, rim=(-104, 22),
        foam='M-20.6 -96 Q-23 -112 -11 -114 Q0 -124 11 -114 Q23 -112 20.6 -96 Q0 -92 -20.6 -96Z'),
    'flute': dict(
        out='<path d="M-12 -112 Q-14 -64 0 -46 Q14 -64 12 -112" stroke-width="2.2"/><path d="M-12 -112 Q0 -114 12 -112" stroke-width="1.4"/><path d="M0 -46 V-4 M-15 0 Q0 -5 15 0" stroke-width="2.2"/>',
        back='<path d="M-12 -112 Q-14 -64 0 -46 Q14 -64 12 -112Z" fill="#e7f1fb" opacity=".35"/>',
        inner='M-10.4 -110 Q-12.2 -64 0 -48.6 Q12.2 -64 10.4 -110Z', bottom=-49, top=-100, rim=(-112, 12)),
    'wine': dict(
        out='<path d="M-26 -112 Q-31 -80 -20 -64 Q-10 -56 0 -56 Q10 -56 20 -64 Q31 -80 26 -112" stroke-width="2.4"/><path d="M-26 -112 Q0 -116 26 -112" stroke-width="1.6"/>'
            '<path d="M0 -56 V-4 M-18 0 Q0 -6 18 0" stroke-width="2.4"/><path d="M-20 -100 Q-23 -84 -16 -72" stroke="#fffaf1" stroke-width="2.6"/>',
        back='<path d="M-26 -112 Q-31 -80 -20 -64 Q-10 -56 0 -56 Q10 -56 20 -64 Q31 -80 26 -112Z" fill="#e7f1fb" opacity=".35"/>',
        inner='M-24.4 -110 Q-28.6 -80 -18.6 -65.4 Q-10 -58.4 0 -58.4 Q10 -58.4 18.6 -65.4 Q28.6 -80 24.4 -110Z', bottom=-59, top=-97, rim=(-112, 26)),
    'mug': dict(   # a clear glass mug, for hot drinks
        out='<path d="M-26 -78 L26 -78 L23 -5 Q0 1 -23 -5Z" stroke-width="2.4"/><path d="M25.6 -66 Q42 -65 42 -46 Q42 -28 24.2 -26" stroke-width="2.4"/>'
            '<path d="M-21.6 -6 H21.6" stroke-width="1.4"/><path d="M-20 -68 L-18.6 -18" stroke="#fffaf1" stroke-width="2.6"/>',
        back='<path d="M-26 -78 L26 -78 L23 -5 Q0 1 -23 -5Z" fill="#e7f1fb" opacity=".35"/>',
        inner='M-24 -76 L24 -76 L21.4 -7 L-21.4 -7Z', bottom=-7, top=-60, rim=(-78, 26)),
    'julep-cup': dict(
        out='<path d="M-24 -74 Q0 -82 24 -74 Q0 -66 -24 -74Z" stroke-width="2.2"/><path d="M-24 -74 L-19 -7 Q0 -1 19 -7 L24 -74" stroke-width="2.4"/>'
            '<path d="M-16 -5 L-17 0 H17 L16 -5" stroke-width="2"/><path d="M-17 -60 L-14 -18" stroke="#ffffff" stroke-width="3"/>'
            + ''.join(f'<circle cx="{x}" cy="{y}" r=".9" fill="#ffffff" stroke="none"/>' for x, y in ((-8, -56), (4, -48), (12, -60), (-2, -34), (10, -28), (-12, -40), (6, -18))),
        back='<path d="M-24 -74 Q0 -82 24 -74 Q0 -66 -24 -74Z" fill="#7d858c"/>',
        front='<path d="M-24 -74 Q0 -66 24 -74 L19 -7 Q0 -1 -19 -7Z" fill="#c9d0d6"/>',
        inner='M-23 -90 L23 -90 L23 -74 L19 -6 L-19 -6 L-23 -74Z', bottom=-6, top=-75, rim=(-74, 24), opaque=True),
    'copper-mug': dict(
        out='<path d="M-32 -70 Q0 -79 32 -70 Q0 -61 -32 -70Z" stroke-width="2.2"/><path d="M-32 -70 L-31 -7 Q0 1 31 -7 L32 -70" stroke-width="2.4"/>'
            '<path d="M32 -60 Q49 -59 49 -40 Q49 -21 32 -20" stroke-width="5.5" stroke="#8a4a22"/><path d="M32 -60 Q49 -59 49 -40 Q49 -21 32 -20" stroke-width="2"/>'
            '<path d="M-24 -56 L-23.4 -16" stroke="#f6c89a" stroke-width="3"/><circle cx="26" cy="-58" r="1.4" fill="#8a4a22"/><circle cx="26" cy="-22" r="1.4" fill="#8a4a22"/>',
        back='<path d="M-32 -70 Q0 -79 32 -70 Q0 -61 -32 -70Z" fill="#7a3f1e"/>',
        front='<path d="M-32 -70 Q0 -61 32 -70 L31 -7 Q0 1 -31 -7Z" fill="#c46a32"/>',
        inner='M-31 -76 L31 -76 L31 -6 L-31 -6Z', bottom=-6, top=-71, rim=(-70, 32), opaque=True),
}

# ice, inside the glass: one big cube in a rocks glass, a stack in a highball
ICE = {
    'rocks': [(-14, -37, 28, 0)],
    'rocks-crushed': [(-28.0, -18.0, 8, -25), (-18.8, -17.0, 7, 12), (-9.6, -16.0, 6, -1), (-0.4, -17.5, 8, -14), (8.8, -16.5, 7, 23), (18.0, -18.0, 6, 10), (-24.0, -23.1, 7, -2), (-14.8, -24.6, 6, -15), (-5.6, -23.6, 8, 22), (3.6, -22.6, 7, 9), (12.8, -24.1, 6, -4), (-28.0, -30.6, 6, 21), (-18.8, -29.6, 8, 8), (-9.6, -31.1, 7, -5), (-0.4, -30.1, 6, -18), (8.8, -29.1, 8, 19), (18.0, -30.6, 7, 6), (-24.0, -35.7, 8, -6), (-14.8, -37.2, 7, -19), (-5.6, -36.2, 6, 18), (3.6, -37.7, 8, 5), (12.8, -36.7, 7, -8), (-28.0, -43.2, 7, 17), (-18.8, -42.2, 6, 4), (-9.6, -43.7, 8, -9), (-0.4, -42.7, 7, -22), (8.8, -44.2, 6, 15), (18.0, -43.2, 8, 2), (-24.0, -50.8, 6, -10), (-14.8, -49.8, 8, -23), (-5.6, -48.8, 7, 14), (3.6, -50.3, 6, 1), (12.8, -49.3, 8, -12), (-28.0, -55.9, 8, 13), (-18.8, -57.4, 7, 0), (-9.6, -56.4, 6, -13), (-0.4, -55.4, 8, 24), (8.8, -56.9, 7, 11), (18.0, -55.9, 6, -2)],
    'highball-crushed': [(-18.0, -16.5, 7.5, -25), (-9.3, -15.5, 6.5, 12), (-0.6, -14.5, 5.5, -1), (8.1, -16.0, 7.5, -14), (-14.2, -21.1, 6.5, -2), (-5.6, -22.6, 5.5, -15), (3.1, -21.6, 7.5, 22), (-18.0, -28.3, 5.5, 21), (-9.3, -27.3, 7.5, 8), (-0.6, -28.8, 6.5, -5), (8.1, -27.8, 5.5, -18), (-14.2, -32.9, 7.5, -6), (-5.6, -34.4, 6.5, -19), (3.1, -33.4, 5.5, 18), (-18.0, -40.1, 6.5, 17), (-9.3, -39.1, 5.5, 4), (-0.6, -40.6, 7.5, -9), (8.1, -39.6, 6.5, -22), (-14.2, -47.2, 5.5, -10), (-5.6, -46.2, 7.5, -23), (3.1, -45.2, 6.5, 14), (-18.0, -51.9, 7.5, 13), (-9.3, -53.4, 6.5, 0), (-0.6, -52.4, 5.5, -13), (8.1, -51.4, 7.5, 24), (-14.2, -59.0, 6.5, -14), (-5.6, -58.0, 5.5, 23), (3.1, -59.5, 7.5, 10), (-18.0, -63.7, 5.5, 9), (-9.3, -65.2, 7.5, -4), (-0.6, -64.2, 6.5, -17), (8.1, -65.7, 5.5, 20), (-14.2, -70.8, 7.5, -18), (-5.6, -69.8, 6.5, 19), (3.1, -71.3, 5.5, 6), (-18.0, -78.0, 6.5, 5), (-9.3, -77.0, 5.5, -8), (-0.6, -76.0, 7.5, -21), (8.1, -77.5, 6.5, 16), (-14.2, -82.7, 5.5, -22), (-5.6, -84.2, 7.5, 15), (3.1, -83.2, 6.5, 2), (-18.0, -89.8, 7.5, 1), (-9.3, -88.8, 6.5, -12), (-0.6, -90.3, 5.5, -25), (8.1, -89.3, 7.5, 12), (-14.2, -94.5, 6.5, 24), (-5.6, -96.0, 5.5, 11), (3.1, -95.0, 7.5, -2)],
    'wine': [(-18, -84, 14, -6), (2, -86, 14, 5), (-8, -101, 14, 8), (-15, -72, 13, 3), (4, -72, 13, -5)],
    'julep-cup-crushed': [(-22.0, -17.5, 7.5, -25), (-13.3, -16.5, 6.5, 12), (-4.6, -15.5, 5.5, -1), (4.1, -17.0, 7.5, -14), (12.8, -16.0, 6.5, 23), (-18.2, -22.1, 6.5, -2), (-9.6, -23.6, 5.5, -15), (-0.9, -22.6, 7.5, 22), (7.8, -21.6, 6.5, 9), (-22.0, -29.3, 5.5, 21), (-13.3, -28.3, 7.5, 8), (-4.6, -29.8, 6.5, -5), (4.1, -28.8, 5.5, -18), (12.8, -27.8, 7.5, 19), (-18.2, -33.9, 7.5, -6), (-9.6, -35.4, 6.5, -19), (-0.9, -34.4, 5.5, 18), (7.8, -35.9, 7.5, 5), (-22.0, -41.1, 6.5, 17), (-13.3, -40.1, 5.5, 4), (-4.6, -41.6, 7.5, -9), (4.1, -40.6, 6.5, -22), (12.8, -42.1, 5.5, 15), (-18.2, -48.2, 5.5, -10), (-9.6, -47.2, 7.5, -23), (-0.9, -46.2, 6.5, 14), (7.8, -47.7, 5.5, 1), (-22.0, -52.9, 7.5, 13), (-13.3, -54.4, 6.5, 0), (-4.6, -53.4, 5.5, -13), (4.1, -52.4, 7.5, 24), (12.8, -53.9, 6.5, 11), (-18.2, -60.0, 6.5, -14), (-9.6, -59.0, 5.5, 23), (-0.9, -60.5, 7.5, 10), (7.8, -59.5, 6.5, -3), (-22.0, -64.7, 5.5, 9), (-13.3, -66.2, 7.5, -4), (-4.6, -65.2, 6.5, -17), (4.1, -66.7, 5.5, 20), (12.8, -65.7, 7.5, 7), (-18.2, -71.8, 7.5, -18), (-9.6, -70.8, 6.5, 19), (-0.9, -72.3, 5.5, 6), (7.8, -71.3, 7.5, -7), (-22.0, -79.0, 6.5, 5), (-13.3, -78.0, 5.5, -8), (-4.6, -77.0, 7.5, -21), (4.1, -78.5, 6.5, 16), (12.8, -77.5, 5.5, 3), (-18.2, -83.7, 5.5, -22), (-9.6, -85.2, 7.5, 15), (-0.9, -84.2, 6.5, 2), (7.8, -83.2, 5.5, -11)],
    'copper-mug': [(-21, -80, 13, -8), (-4, -82, 13, 6), (12, -79, 12, -5)],   # only their tops show, in the mouth of the mug
    'highball': [(-17.5, -23, 15, -6), (1.5, -22.5, 15, 5), (-12, -39, 15, 8), (3, -38.5, 15, -4), (-16, -55, 15, 3), (1, -54, 15, -7), (-8, -71, 15, 6)],
}


def cube(x, y, w, rot=0, cls=''):
    """An ice cube, top-left (x, y); see-through, so the drink shows."""
    c = f' class="{cls}"' if cls else ''
    r = f' transform="rotate({rot} {f(x + w / 2)} {f(y + w / 2)})"' if rot else ''
    return (f'<g{c}><g{r}>' + wash(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(w)}" rx="{f(w * .18)}" fill="#f4fbff" opacity=".5"/>')
            + lines(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(w)}" rx="{f(w * .18)}" stroke="#7fb8d6" stroke-width="1.5"/>'
                    f'<path d="M{f(x + w * .22)} {f(y + w * .3)} h{f(w * .3)}" stroke="#fffaf1" stroke-width="2"/>', boil=False) + '</g></g>')


def ice(kind, crushed=False):
    return ''.join(cube(x, y, w, r) for x, y, w, r in ICE.get(kind + ('-crushed' if crushed else ''), ICE.get(kind, [])))


# ---------------------------------------------------------------- garnishes (each at its own (0, 0))
CITRUS = {   # flesh, rind
    'lemon': ('#f6e27a', '#e9c63a'), 'lime': ('#c9df7a', '#7f9a3c'), 'orange': ('#f6b25a', '#e8892c'), 'grapefruit': ('#f4a49a', '#e9845c'),
}


def wheel(fruit, r=8.5):
    """A citrus wheel, standing on edge with a slit over the rim."""
    flesh, rind = CITRUS[fruit]
    seg = ' '.join(f'M0 0 L{f(r * .72 * math.cos(a * math.pi / 4))} {f(r * .72 * math.sin(a * math.pi / 4))}' for a in range(8))
    return (wash(f'<circle r="{f(r)}" fill="{rind}"/><circle r="{f(r - 1.8)}" fill="{flesh}"/>')
            + lines(f'<circle r="{f(r)}" stroke-width="1.7"/><path d="{seg}" stroke="{rind}" stroke-width=".9"/>', boil=False))


def wedge(fruit):
    """A wedge perched on the rim (flat side up, tilted)."""
    flesh, rind = CITRUS[fruit]
    d = 'M-10 0 A10 10 0 0 0 10 0Z'
    return ('<g transform="rotate(-24)">' + wash(f'<path d="{d}" fill="{flesh}"/>')
            + lines(f'<path d="M-10 0 A10 10 0 0 0 10 0" stroke="{rind}" stroke-width="3.4"/><path d="{d}" stroke-width="1.7"/>'
                    f'<path d="M0 0 L-5 7 M0 0 L0 8.6 M0 0 L5 7" stroke="{rind}" stroke-width=".9"/>', boil=False) + '</g>')


def twist(fruit):
    """A long curl of peel hanging over the rim."""
    rind = CITRUS[fruit][1]
    d = 'M-3 -2 C4 -9 11 -4 9 3 C7 10 0 9 2 15 C3 19 8 20 10 18'
    return (lines(f'<path d="{d}" stroke-width="6"/>', boil=False) + f'<path d="{d}" fill="none" stroke="{rind}" stroke-width="3.4" stroke-linecap="round"/>'
            + f'<path d="M-1 -3 C4 -7 8 -4 8 0" fill="none" stroke="#fff3c8" stroke-width="1" stroke-linecap="round" opacity=".8"/>')


def peel(fruit):
    """A wide swath of peel, expressed and dropped in (leaning on the rim)."""
    flesh, rind = CITRUS[fruit]
    d = 'M-7 -12 Q5 -10 7 4 Q6 13 1 17 Q3 4 -7 -12Z'
    return wash(f'<path d="{d}" fill="{rind}"/>') + lines(f'<path d="{d}" stroke-width="1.7"/><path d="M-3 -8 Q3 -4 3 6" stroke="{flesh}" stroke-width="1.2"/>', boil=False)


def cherry(stem=True):
    return (wash('<circle r="4.6" fill="#b3202a"/>') + lines('<circle r="4.6" stroke-width="1.7"/>'
            + ('<path d="M1 -4.2 q2 -6 7 -9" stroke="#6b4228" stroke-width="1.7"/>' if stem else ''), boil=False)
            + '<circle cx="-1.6" cy="-1.6" r="1.1" fill="#f6b8b8"/>')


def olives():
    """Two olives on a pick, leaning across the glass."""
    o = lambda x, y: (wash(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="4" fill="#8a9a3c"/>') + lines(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="4" stroke-width="1.6"/>', boil=False)
                      + f'<circle cx="{x + 2.6}" cy="{y}" r="1.4" fill="#c0392b"/>')
    return (lines('<path d="M14 -20 L-14 22" stroke="#8a6a3c" stroke-width="2"/><circle cx="14.5" cy="-21" r="2.2" fill="#c0583c"/>', boil=False)
            + '<g transform="rotate(-56)">' + o(-4, 0) + o(7, 0) + '</g>')


def mint():
    """A sprig of mint standing up out of the glass."""
    leaf = lambda x, y, r, s=1: (f'<g transform="translate({x} {y}) rotate({r}) scale({s})">' + wash('<path d="M0 0 Q5 -6 0 -14 Q-5 -6 0 0Z" fill="#6fae4f"/>')
                                 + lines('<path d="M0 0 Q5 -6 0 -14 Q-5 -6 0 0Z M0 -1 V-12" stroke-width="1.3"/>', boil=False) + '</g>')
    return (lines('<path d="M0 8 Q1 -4 0 -16" stroke="#4f7a3a" stroke-width="2"/>', boil=False)
            + leaf(0, -14, 0) + leaf(0, -9, -48, .9) + leaf(0, -8, 48, .9) + leaf(0, -2, -70, .8) + leaf(0, -1, 70, .8))


def mint_leaf(x, y, r=0):
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({r})">' + wash('<path d="M0 0 Q4 -5 0 -11 Q-4 -5 0 0Z" fill="#6fae4f"/>')
            + lines('<path d="M0 0 Q4 -5 0 -11 Q-4 -5 0 0Z" stroke-width="1.2"/>', boil=False) + '</g>')


def flower():
    """An edible flower, floating."""
    petals = ''.join(f'<ellipse cx="0" cy="-5" rx="3.4" ry="5" transform="rotate({a * 72})"/>' for a in range(5))
    return (wash(f'<g fill="#a77bd1">{petals}</g>') + lines(f'<g stroke-width="1.3">{petals}</g>', boil=False)
            + '<circle r="2.2" fill="#f2c776" stroke="#5b2c4c" stroke-width="1"/>')


def grapefruit_wedge():
    return wedge('grapefruit')


# where each garnish sits on each glass: (drawing, x, y, rotation)
def garnish(kind, glass):
    g = GLASS[glass]
    ry, hw = g['rim']
    if kind == 'cherry':
        spot = {'coupe': (5, -69), 'martini': (4, -76), 'rocks': (9, -42), 'highball': (7, -95), 'flute': (0, -103), 'wine': (6, -99), 'mug': (8, -64), 'copper-mug': (8, -72),
                'julep-cup': (8, -80)}[glass]
        return at(*spot, cherry())
    if kind == 'olives':
        return at(6, ry + 18, olives())
    if kind == 'mint':
        return at(7, ry - 2, mint())
    if kind == 'flower':
        return at(-4, g['top'] - 2.5, flower(), 1.1)
    if kind.endswith('-wheel'):
        return at(hw - 5, ry - 1, wheel(kind.split('-')[0]))
    if kind.endswith('-wedge'):
        return at(hw - 3, ry - 1, wedge(kind.split('-')[0]))
    if kind.endswith('-twist'):
        return at(hw - 3, ry, twist(kind.split('-')[0]))
    if kind.endswith('-peel'):
        return at(hw - 8, ry + 6, peel(kind.split('-')[0]), 1, -8)
    if kind in ('salt-rim', 'sugar-rim'):
        return rim(kind, glass)
    top = g['top']
    if kind == 'celery':
        return at(hw - 12, ry + 8, lines('<path d="M0 0 L8 -46" stroke="#8fbf5a" stroke-width="5"/><path d="M0 0 L8 -46" stroke="#cfe39a" stroke-width="1.6"/>', boil=False)
                  + ''.join(mint_leaf(8 + dx, -46 + dy, r) for dx, dy, r in ((0, 2, -30), (3, 4, 30), (-2, 5, -70))))
    if kind == 'candied-ginger':
        return at(hw - 10, ry - 2, lines('<path d="M-14 6 L16 -10" stroke="#a9a29a" stroke-width="1.6"/>', boil=False)
                  + wash('<rect x="2" y="-9" width="9" height="8" rx="2" fill="#e9c46a" transform="rotate(-25 6 -5)"/>')
                  + lines('<rect x="2" y="-9" width="9" height="8" rx="2" stroke-width="1.4" transform="rotate(-25 6 -5)"/>', boil=False))
    if kind == 'paper-plane':
        return at(hw - 4, ry - 10, wash('<path d="M-10 0 L12 -6 L-2 4Z" fill="#fffaf1"/><path d="M-2 4 L12 -6 L0 -1Z" fill="#e7e1d6"/>')
                  + lines('<path d="M-10 0 L12 -6 L-2 4Z M-2 4 L0 -1 L12 -6" stroke-width="1.3"/>', boil=False), 1, -12)
    if kind == 'coffee-beans':
        return ''.join(at(x, top - 1.5, wash('<ellipse rx="3.4" ry="2.4" fill="#4a2a18"/>') + lines('<path d="M-2.4 0 Q0 -1 2.4 0" stroke="#c99a62" stroke-width=".9"/>', boil=False), 1, r)
                       for x, r in ((-8, -10), (0, 6), (8, -4)))
    if kind == 'pineapple':
        return at(hw - 4, ry - 1, wash('<path d="M-9 -2 L9 -2 L0 13Z" fill="#f6d36a"/><path d="M-9 -2 L9 -2 L8 -5 L-8 -5Z" fill="#c9a25a"/>'
                                      '<path d="M-2 -5 L-6 -16 L0 -8 L2 -18 L3 -8 L8 -14 L4 -5Z" fill="#6f9e4a"/>')
                  + lines('<path d="M-9 -2 L9 -2 L0 13Z M-9 -2 L-8 -5 L8 -5 L9 -2" stroke-width="1.4"/><path d="M-2 -5 L-6 -16 L0 -8 L2 -18 L3 -8 L8 -14 L4 -5" stroke-width="1.2"/>', boil=False))
    if kind == 'bitters-drops':
        return ''.join(f'<circle cx="{x}" cy="{f(top - 3)}" r="1.6" fill="#7d2f2a"/>' for x in (-8, -1, 6))
    if kind == 'straw':
        return lines(f'<path d="M-4 {f(g["bottom"] - 4)} L10 {f(ry - 26)}" stroke="#e8737a" stroke-width="3.4"/>', boil=False, width=2)
    if kind == 'cinnamon':
        return at(8, ry + 6, wash('<rect x="-2.6" y="-36" width="5.2" height="36" rx="2" fill="#9a5a2a"/>') + lines('<rect x="-2.6" y="-36" width="5.2" height="36" rx="2" stroke-width="1.4"/>', boil=False), 1, 12)
    if kind == 'nutmeg':
        return ''.join(f'<circle cx="{x}" cy="{f(top + dy)}" r=".9" fill="#8a5a2a"/>' for x, dy in ((-10, 1), (-5, 0), (-1, 1.4), (3, .4), (8, 1), (12, .2), (-14, .6)))
    if kind == 'berries':
        return ''.join(at(x, ry - 3, wash(f'<circle r="3.4" fill="{c}"/>') + lines('<circle r="3.4" stroke-width="1.2"/>', boil=False)) for x, c in ((-6, '#b3202a'), (1, '#4a1830'), (8, '#b3202a')))
    raise ValueError(kind)


RIMS = ('salt-rim', 'sugar-rim')


def rim(kind, glass):
    """Salt (or sugar) crusted on the outside of the rim, a band you can see from the side."""
    g = GLASS[glass]
    ry, hw = g['rim']
    dip = 0 if glass in ('rocks', 'highball') else 4
    path = f'M{-hw - .5} {ry + 1} Q0 {ry + 1 - dip} {hw + .5} {ry + 1}'
    grain = '#a9a29a' if kind == 'salt-rim' else '#d9b44a'
    dots = ''.join(f'<circle cx="{f(x * hw)}" cy="{f(ry + 1 + dy - dip * (1 - x * x) * .5)}" r=".9" fill="{grain}"/>'
                   for x, dy in ((-.85, 1.2), (-.6, -.6), (-.35, 1.4), (-.1, -.4), (.15, 1.1), (.4, -.7), (.62, 1.3), (.85, -.2)))
    return (lines(f'<path d="{path}"/>', boil=False, width=5.2, color='#fbfaf4') + lines(f'<path d="{path}" stroke-dasharray="1.2 2.6"/>', boil=False, width=1.4, color=grain)
            + dots)


def garnishes(kinds, glass):
    return ''.join(garnish(k, glass) for k in kinds)


def at(x, y, inner, s=1.0, rot=0):
    r = f' rotate({rot})' if rot else ''
    sc = f' scale({f(s)})' if s != 1 else ''
    return f'<g transform="translate({f(x)} {f(y)}){r}{sc}">{inner}</g>'


# ---------------------------------------------------------------- bottles (feet at 0, 0), no brands: a word on a plain label
SHAPES = {   # outline, height, label box (y, h), cap; bodies wide enough for a label you can read
    'spirit': ('M-14 0 L-14 -38 Q-14 -46 -6.5 -50 L-5 -62 L5 -62 L6.5 -50 Q14 -46 14 -38 L14 0Z', 68, (-33, 19), 'M-5.5 -68 h11 v7 h-11Z'),
    'tall': ('M-12 0 L-12 -46 Q-12 -53 -5 -56 L-4.5 -66 L4.5 -66 L5 -56 Q12 -53 12 -46 L12 0Z', 72, (-36, 19), 'M-5 -72 h10 v7 h-10Z'),
    'wine': ('M-13 0 L-13 -36 Q-13 -48 -4.5 -54 L-4 -68 L4 -68 L4.5 -54 Q13 -48 13 -36 L13 0Z', 74, (-32, 19), 'M-4.6 -74 h9.2 v8 h-9.2Z'),
    'liqueur': ('M-15 0 L-15 -28 Q-15 -37 -5 -40 L-4 -50 L4 -50 L5 -40 Q15 -37 15 -28 L15 0Z', 56, (-27, 18), 'M-5 -56 h10 v7 h-10Z'),
    'soda': ('M-9.5 0 L-9.5 -30 Q-9.5 -36 -3.5 -40 L-3.5 -50 L3.5 -50 L3.5 -40 Q9.5 -36 9.5 -30 L9.5 0Z', 54, (-27, 17), 'M-4.4 -54 h8.8 v5 h-8.8Z'),
}
LABEL_W = {'spirit': 25, 'tall': 21, 'wine': 23, 'liqueur': 27, 'soda': 17}


def label_text(words, w, ly, lh):
    """The words on a label, one or two lines, squeezed to fit if the hand font runs long."""
    parts = words.split(' ')
    if len(parts) == 1:
        rows = [words]
    else:   # two lines, as even as the words allow
        cut = min(range(1, len(parts)), key=lambda i: abs(len(' '.join(parts[:i])) - len(' '.join(parts[i:]))))
        rows = [' '.join(parts[:cut]), ' '.join(parts[cut:])]
    fs = 7.6 if len(rows) == 1 else 6.8
    avail = w - 3
    out = ''
    for i, row in enumerate(rows):
        y = ly + lh / 2 + fs * .36 + (i - (len(rows) - 1) / 2) * fs * 1.02
        fit = f' textLength="{avail:g}" lengthAdjust="spacingAndGlyphs"' if len(row) * fs * .5 > avail else ''
        out += f'<text class="letter" x="0" y="{y:.1f}" font-size="{fs}" text-anchor="middle"{fit}>{row}</text>'
    return out


def bottle(shape, glass_color, word, cap='#7a5f4a', foil=False):
    d, h, (ly, lh), capd = SHAPES[shape]
    w = LABEL_W[shape]
    fill = wash(f'<path d="{d}" fill="{glass_color}"/><rect x="{-w / 2:g}" y="{ly}" width="{w}" height="{lh}" rx="1.6" fill="#fbf3e3"/><path d="{capd}" fill="{cap}"/>'
                + (f'<path d="M-4.6 -74 h9.2 l1 16 h-11.2Z" fill="#d9b44a"/>' if foil else ''))
    line = lines(f'<path d="{d}" stroke-width="2"/><rect x="{-w / 2:g}" y="{ly}" width="{w}" height="{lh}" rx="1.6" stroke-width="1.5"/><path d="{capd}" stroke-width="1.5"/>'
                 + ('<path d="M-4.6 -74 h9.2 l1 16 h-11.2Z" stroke-width="1.4"/>' if foil else ''), boil=False)
    return fill + line + label_text(word, w, ly, lh)


def bitters(word='bitters'):
    """A dasher bottle of bitters (no brand), or of another sauce: the label says what's in it."""
    return (wash('<path d="M-9 -8 Q-9 -14 -4 -14 L-4 -20 L4 -20 L4 -14 Q9 -14 9 -8 L9 18 L-9 18Z" fill="#7d2f2a"/><rect x="-11" y="-2" width="22" height="14" rx="1.5" fill="#fbf3e3"/><rect x="-2.5" y="-25" width="5" height="5" fill="#c9c3b8"/>')
            + lines('<path d="M-9 -8 Q-9 -14 -4 -14 L-4 -20 L4 -20 L4 -14 Q9 -14 9 -8 L9 18 L-9 18Z"/><rect x="-11" y="-2" width="22" height="14" rx="1.5" stroke-width="1.5"/><rect x="-2.5" y="-25" width="5" height="5" stroke-width="1.4"/>', boil=False, width=2)
            + (f'<text class="letter" x="0" y="7.6" font-size="6.2" text-anchor="middle"' + (' textLength="19" lengthAdjust="spacingAndGlyphs"' if len(word) > 7 else '') + f'>{word}</text>'))


def jigger():
    d = 'M-9 -16 L9 -16 L3 0 L9 16 L-9 16 L-3 0Z'
    return wash(f'<path d="{d}" fill="#c9c3b8"/>') + lines(f'<path d="{d} M-3 0 H3" stroke-width="2"/>', boil=False)


def fruit(kind, half=False):
    """A whole citrus (or a half, cut side out), resting at (0, 0)."""
    flesh, rind = CITRUS[kind]
    r = {'lemon': 13, 'lime': 11, 'orange': 15, 'grapefruit': 17}[kind]
    if half:
        seg = ' '.join(f'M0 {-r} L{f(r * .74 * math.cos(a * math.pi / 4))} {f(-r + r * .74 * math.sin(a * math.pi / 4))}' for a in range(8))
        return (wash(f'<circle cx="0" cy="{-r}" r="{r}" fill="{rind}"/><circle cx="0" cy="{-r}" r="{r - 2.4}" fill="{flesh}"/>')
                + lines(f'<circle cx="0" cy="{-r}" r="{r}" stroke-width="2"/><path d="{seg}" stroke="{rind}" stroke-width="1"/>', boil=False))
    rx = r * (1.25 if kind == 'lemon' else 1)
    return (wash(f'<ellipse cx="0" cy="{-r}" rx="{f(rx)}" ry="{r}" fill="{rind}"/>' + (f'<path d="M{f(rx - 1)} {-r - 2} l5 -2 l-1 4Z" fill="{rind}"/>' if kind == 'lemon' else ''))
            + lines(f'<ellipse cx="0" cy="{-r}" rx="{f(rx)}" ry="{r}" stroke-width="2"/><path d="M{f(-rx * .45)} {f(-r * 1.5)} q{f(rx * .3)} -3 {f(rx * .6)} -2" stroke="#fff6c8" stroke-width="2"/>'
                    + (f'<path d="M{f(rx - 1)} {-r - 2} l5 -2 l-1 4" stroke-width="1.6"/>' if kind == 'lemon' else ''), boil=False))


def mint_bunch():
    return at(-8, 0, mint(), 1.3, -12) + at(8, 0, mint(), 1.2, 14)


def honey_jar():
    return (wash('<path d="M-13 0 Q-15 -14 -12 -26 L12 -26 Q15 -14 13 0Z" fill="#e9b949"/><rect x="-13" y="-33" width="26" height="7" rx="2" fill="#c98a3c"/><rect x="-9" y="-19" width="18" height="10" rx="1.5" fill="#fbf3e3"/>')
            + lines('<path d="M-13 0 Q-15 -14 -12 -26 L12 -26 Q15 -14 13 0Z" stroke-width="2"/><rect x="-13" y="-33" width="26" height="7" rx="2" stroke-width="1.8"/><rect x="-9" y="-19" width="18" height="10" rx="1.5" stroke-width="1.4"/>', boil=False)
            + '<text class="letter" x="0" y="-11.6" font-size="6.6" text-anchor="middle">honey</text>')


def egg():
    return (wash('<ellipse cx="0" cy="-12" rx="9.5" ry="12" fill="#f6ead2"/>') + lines('<ellipse cx="0" cy="-12" rx="9.5" ry="12" stroke-width="2"/><path d="M-4 -19 q2 -3 5 -3" stroke="#fffaf1" stroke-width="2"/>', boil=False))


def syrup_jar(word, color):
    """A small bottle of syrup or juice with a word on it."""
    return bottle('soda', color, word, cap='#c25c86')


def pear():
    return (wash('<path d="M0 0 Q-15 0 -13 -14 Q-11 -22 -6 -26 Q-4 -36 0 -37 Q4 -36 6 -26 Q11 -22 13 -14 Q15 0 0 0Z" fill="#cfd96a"/>')
            + lines('<path d="M0 0 Q-15 0 -13 -14 Q-11 -22 -6 -26 Q-4 -36 0 -37 Q4 -36 6 -26 Q11 -22 13 -14 Q15 0 0 0Z" stroke-width="2"/><path d="M0 -37 q1 -5 4 -7" stroke="#6b4228" stroke-width="2"/>', boil=False)
            + wash('<path d="M4 -42 q7 -4 10 1 q-6 3 -10 -1Z" fill="#6fae4f"/>'))


# ---------------------------------------------------------------- ingredients
# key: caption (what the build scene says as it pours), how it goes in, the drink's color,
#      and for bottles: (shape, glass color, the word on the label)
ING = {
    'bourbon':        ('bourbon', 'bottle', '#c9782c', ('spirit', '#c98a3c', 'bourbon')),
    'rye':            ('rye', 'bottle', '#c47a30', ('spirit', '#c98a3c', 'rye')),
    'whiskey':        ('whiskey', 'bottle', '#c9782c', ('spirit', '#c98a3c', 'whiskey')),
    'scotch':         ('Scotch', 'bottle', '#d08a34', ('spirit', '#d49a48', 'Scotch')),
    'cognac':         ('cognac', 'bottle', '#b8621f', ('liqueur', '#b8621f', 'cognac')),
    'brandy':         ('brandy', 'bottle', '#b8621f', ('spirit', '#b8692a', 'brandy')),
    'gin':            ('gin', 'bottle', '#eef3f0', ('tall', '#cfe6df', 'gin')),
    'white-rum':      ('white rum', 'bottle', '#f1ecd8', ('tall', '#e3eee6', 'white rum')),
    'dark-rum':       ('dark rum', 'bottle', '#5a2e14', ('spirit', '#6b3a1c', 'dark rum')),
    'tequila':        ('tequila', 'bottle', '#f3efd9', ('tall', '#e3eedd', 'tequila')),
    'vodka':          ('vodka', 'bottle', '#eef2f4', ('tall', '#e4ecf1', 'vodka')),
    'aged-rum':       ('aged rum', 'bottle', '#b8742e', ('spirit', '#b8742e', 'aged rum')),
    'aperol':         ('Aperol', 'bottle', '#f26b21', ('tall', '#f26b21', 'Aperol')),
    'prosecco':       ('prosecco', 'bottle', '#f3ecc0', ('wine', '#5f7f3c', 'prosecco')),
    'orgeat':         ('orgeat', 'jigger', '#f0e3c8', None),
    'water':          ('cold water', 'jigger', '#e8f3f7', None),
    'hot-water':      ('hot water', 'kettle', '#f2ece4', None),
    'coffee':         ('hot coffee', 'kettle', '#3a2416', None),
    'hot-milk':       ('hot milk', 'kettle', '#fbf6ea', None),
    'mulled':         ('hot mulled wine', 'kettle', '#7a1f2a', None),
    'absinthe':       ('absinthe', 'bottle', '#b9d99a', ('tall', '#9ec27a', 'absinthe')),
    'islay':          ('Islay Scotch', 'bottle', '#c9a25a', ('spirit', '#b98a4a', 'Islay Scotch')),
    'irish-whiskey':  ('Irish whiskey', 'bottle', '#c9963c', ('spirit', '#c9a25a', 'Irish whiskey')),
    'amaro':          ('Amaro Nonino', 'bottle', '#c46a2a', ('liqueur', '#b8621f', 'Amaro Nonino')),
    'coffee-liqueur': ('coffee liqueur', 'bottle', '#3a2416', ('liqueur', '#3a2416', 'coffee liqueur')),
    'citrus-vodka':   ('citrus vodka', 'bottle', '#f1efd8', ('tall', '#f0ead0', 'citrus vodka')),
    'mezcal':         ('mezcal', 'bottle', '#eef0e2', ('tall', '#dfe6d2', 'mezcal')),
    'reposado':       ('reposado tequila', 'bottle', '#e9d29a', ('tall', '#e9d29a', 'reposado tequila')),
    'chartreuse':     ('green Chartreuse', 'bottle', '#a9cf6a', ('liqueur', '#8fbf5a', 'green Chartreuse')),
    'maraschino':     ('maraschino liqueur', 'bottle', '#eef2ea', ('tall', '#cfe0c8', 'maraschino')),
    'lillet':         ('Lillet Blanc', 'bottle', '#f0dfa0', ('wine', '#e9d48a', 'Lillet Blanc')),
    'fernet':         ('Fernet-Branca', 'bottle', '#3a3226', ('tall', '#3a3226', 'Fernet-Branca')),
    'angostura-oz':   ('Angostura bitters', 'bottle', '#5a1f1a', ('soda', '#5a1f1a', 'Angostura bitters')),
    'cherry-liqueur': ('cherry liqueur', 'bottle', '#7a1a2a', ('liqueur', '#7a1a2a', 'cherry liqueur')),
    'cachaca':        ('cachaça', 'bottle', '#eef2e6', ('tall', '#dde9d6', 'cachaça')),
    'pisco':          ('pisco', 'bottle', '#f1eedb', ('tall', '#e6eadb', 'pisco')),
    'rhum-agricole':  ('rhum agricole', 'bottle', '#eef0e0', ('tall', '#dfe8d4', 'rhum agricole')),
    'sherry':         ('sherry', 'bottle', '#c99a4a', ('wine', '#a8742e', 'sherry')),
    'peach-brandy':   ('peach brandy', 'bottle', '#e9a25a', ('liqueur', '#e09a52', 'peach brandy')),
    'red-wine':       ('red wine', 'bottle', '#6a1a2a', ('wine', '#4a1a26', 'red wine')),
    'ginger-ale':     ('ginger ale', 'bottle', '#efe2b0', ('soda', '#d9b97a', 'ginger ale')),
    'tomato':         ('tomato juice', 'jigger', '#c8402e', None),
    'honey-ginger':   ('honey-ginger syrup', 'jigger', '#e2b452', None),
    'espresso':       ('espresso', 'jigger', '#3a2416', None),
    'cranberry':      ('cranberry juice', 'jigger', '#b3202a', None),
    'agave':          ('agave syrup', 'jigger', '#f0d78a', None),
    'cream':          ('heavy cream', 'jigger', '#fbf6ea', None),
    'orange-juice':   ('orange juice', 'jigger', '#f6b25a', None),
    'coconut':        ('cream of coconut', 'jigger', '#f6f1e6', None),
    'pineapple':      ('pineapple juice', 'jigger', '#f6d86a', None),
    'demerara':       ('demerara syrup', 'jigger', '#d9a65a', None),
    'grapefruit-juice': ('grapefruit juice', 'jigger', '#f4b0a2', None),
    'cane-syrup':     ('cane syrup', 'jigger', '#e9c97a', None),
    'batter':         ('batter', 'jigger', '#e9c98a', None),
    'worcestershire': ('Worcestershire sauce', 'dash', '#5a2e14', None),
    'hot-sauce':      ('hot sauce', 'dash', '#c42f2f', None),
    'orange-flower':  ('orange flower water', 'dash', '#efe6d2', None),
    'applejack':      ('applejack', 'bottle', '#d39a4a', ('spirit', '#d8a256', 'applejack')),
    'sweet-vermouth': ('sweet vermouth', 'bottle', '#7a2a2a', ('wine', '#6b3326', 'sweet vermouth')),
    'dry-vermouth':   ('dry vermouth', 'bottle', '#f2ecc8', ('wine', '#a9c49a', 'dry vermouth')),
    'campari':        ('Campari', 'bottle', '#c42f2f', ('tall', '#c42f2f', 'Campari')),
    'orange-liqueur': ('orange liqueur', 'bottle', '#f3e2b0', ('liqueur', '#f0d79a', 'orange liqueur')),
    'benedictine':    ('Bénédictine', 'bottle', '#d9a640', ('liqueur', '#8a5a2a', 'Bénédictine')),
    'cassis':         ('crème de cassis', 'bottle', '#5a1b3a', ('liqueur', '#4a1830', 'crème de cassis')),
    'violette':       ('crème de violette', 'bottle', '#8a64b4', ('liqueur', '#7d5aa6', 'crème de violette')),
    'lemon':          ('lemon', 'jigger', '#f1e58a', None),
    'lime':           ('lime', 'jigger', '#cfe39a', None),
    'simple':         ('simple syrup', 'jigger', '#f3e9c4', None),
    'honey':          ('honey syrup', 'jigger', '#e9b949', None),
    'grenadine':      ('grenadine', 'jigger', '#b3202a', None),
    'pear':           ('pear nectar', 'jigger', '#e9df9f', None),
    'angostura':      ('Angostura bitters', 'dash', '#5a1f1a', None),
    'orange-bitters': ('orange bitters', 'dash', '#c8661e', None),
    'peychauds':      ("Peychaud's bitters", 'dash', '#c0283a', None),
    'egg':            ('egg white', 'egg', '#fffaf1', None),
    'mint':           ('mint leaves', 'mint', '#6fae4f', None),
    'salt':           ('a pinch of salt', 'salt', '#ffffff', None),
    'ginger-beer':    ('ginger beer', 'bottle', '#e9d49a', ('soda', '#b9783c', 'ginger beer')),
    'soda':           ('soda water', 'bottle', '#eaf6fb', ('soda', '#bfe0ea', 'soda water')),
    'grapefruit-soda': ('grapefruit soda', 'bottle', '#f6d9cf', ('soda', '#f2b8a6', 'grapefruit soda')),
    'champagne':      ('Champagne', 'bottle', '#f3e6a6', ('wine', '#3f6b3a', 'Champagne')),
}
FIZZY = {'ginger-beer', 'soda', 'grapefruit-soda', 'champagne', 'ginger-ale', 'prosecco'}


def ing_bottle(key):
    shape, glass_color, word = ING[key][3]
    return bottle(shape, glass_color, word, foil=(key == 'champagne'))


def bottle_height(key):
    return SHAPES[ING[key][3][0]][1]


# ---------------------------------------------------------------- a finished drink, in one piece (heroes, icons)
def glass(kind, uid, color, garnish_kinds=(), iced=False, foam=False, layers=None, bubbles=False, top=None, cls_bubble='bub', crushed=False, hot=False):
    """A full glass with its foot at (0, 0). layers: [(from_frac, to_frac, color)] of the fill (0 = bottom, 1 = full line), drawn over color."""
    g = GLASS[kind]
    top = g['top'] if top is None else top
    span = g['bottom'] - top
    fill = f'<rect x="-40" y="{f(top)}" width="80" height="{f(span + 2)}" fill="{color}"/>'
    for a, b, c in (layers or []):
        fill += f'<rect x="-40" y="{f(g["bottom"] + 2 - (span + 2) * b)}" width="80" height="{f((span + 2) * (b - a))}" fill="{c}"/>'
    bub = ''
    if bubbles:
        bub = bubbles_in(kind, top)
    inside = f'<clipPath id="{uid}"><path d="{g["inner"]}"/></clipPath><g clip-path="url(#{uid})">{wash(fill)}{bub}{ice(kind, crushed) if iced else ""}</g>'
    out = wash(g['back']) + inside + (wash(g['front']) if 'front' in g else '')
    if foam and 'foam' in g:
        out += foam_on(kind, foam if isinstance(foam, str) else '#fff8e6')
    out += lines(g['out'], boil=False)
    out += garnishes(garnish_kinds, kind)
    if hot:
        out += steam(0, g['rim'][0] - 4)
    return out


def steam(x, y, s=1.0):
    """Three wisps rising off a hot drink (they drift on their own: STEAM_CSS)."""
    w = ''.join(f'<path class="steam s{i}" d="M{f(x + dx)} {f(y)} q-5 -7 0 -14 q5 -7 0 -14" stroke="#b9a8ad" stroke-width="{f(2 * s)}" fill="none" stroke-linecap="round" opacity=".8"/>'
                for i, dx in enumerate((-9 * s, 0, 9 * s)))
    return w


def kettle():
    """A kettle, centered at (0, 0), spout to the right (tip at 26, -10)."""
    body = 'M-17 12 L-14 -5 Q0 -13 14 -5 L17 12Z'
    return (wash(f'<path d="{body}" fill="#c9c3b8"/><path d="M14 1 Q24 -2 26 -10 L22 -10 Q20 -4 14 -3Z" fill="#c9c3b8"/>')
            + lines(f'<path d="{body}" stroke-width="2"/><path d="M14 1 Q24 -2 26 -10 M14 -3 Q20 -4 22 -10" stroke-width="1.8"/>'
                    '<path d="M-10 -8 Q0 -24 10 -8" stroke-width="2.4" stroke="#5a4a44"/><circle cx="0" cy="-12" r="2.2" fill="#5a4a44"/><path d="M-11 3 L-9 -2" stroke="#f4f4f2" stroke-width="2.4"/>', boil=False))


def foam_on(kind, color='#fff8e6'):
    g = GLASS[kind]
    spots = {'highball': ((-12, -104), (-4, -110), (5, -106), (13, -102))}.get(kind, ((-18, -63), (-9, -61), (2, -63.5), (11, -61.6), (19, -63.4)))
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="none" stroke="#d9c7a8" stroke-width=".9"/>' for x, y in spots)
    return f'<path d="{g["foam"]}" fill="{color}" stroke="{INK}" stroke-width="1.5"/>' + dots


def bubbles_in(kind, top, cls='bub'):
    """Little bubbles rising through the drink (they loop on their own)."""
    g = GLASS[kind]
    hw = {'highball': 15, 'flute': 6, 'coupe': 16, 'rocks': 22, 'martini': 12, 'copper-mug': 22, 'wine': 16, 'mug': 18, 'julep-cup': 16}[kind]
    out = ''
    for i, (fx, fy) in enumerate(((-.7, .15), (.1, .55), (.6, .3), (-.3, .8), (.35, .9), (-.55, .45))):
        x, y = fx * hw, max(g['bottom'] - (g['bottom'] - top) * fy * .6 - 3, top + 36)
        out += f'<circle class="{cls} u{i % 3}" cx="{f(x)}" cy="{f(y)}" r="{1.3 if i % 2 else 1.7}" fill="#fffaf1" stroke="#c9b98a" stroke-width=".6"/>'
    return out


def countertop(y, mat=None):
    """The bar top from y down: a wood counter with a darker front edge; mat=(x0, x1) puts a rubber bar mat on it."""
    out = (f'<rect x="0" y="{y}" width="400" height="{236 - y}" fill="#6e4b39"/>'
           + wash(f'<rect x="0" y="{y}" width="400" height="9" fill="#9a6b4c"/><rect x="0" y="{y + 9}" width="400" height="{227 - y}" fill="#6b4634"/>')
           + lines(f'<path d="M0 {y} H400 M0 {y + 9} H400"/>' + ''.join(f'<path d="M{x} {y + 9} V236" stroke-width="1.6"/>' for x in (64, 168, 262, 352))
                   + ''.join(f'<path d="M{x0} {y + 3.5} h{w}" stroke="#7d5640" stroke-width="1.2"/>' for x0, w in ((22, 38), (120, 54), (230, 30), (300, 46))), boil=False, width=2.2))
    if mat:
        x0, x1 = mat
        out += (f'<rect x="{x0}" y="{y - 4}" width="{x1 - x0}" height="8" rx="3" fill="#33403b"/>'
                + ''.join(f'<path d="M{x} {y - 2.4} v4.6" stroke="#55675f" stroke-width="1.6" stroke-linecap="round"/>' for x in range(x0 + 5, x1 - 3, 6))
                + lines(f'<rect x="{x0}" y="{y - 4}" width="{x1 - x0}" height="8" rx="3" stroke-width="1.8"/>', boil=False))
    return out


BUBBLE_CSS = ('.bub{animation:bub 2.4s linear infinite}.bub.u1{animation-delay:-.8s}.bub.u2{animation-delay:-1.6s}\n'
              '@keyframes bub{0%{transform:translateY(0);opacity:0}15%{opacity:.9}85%{opacity:.9}100%{transform:translateY(-34px);opacity:0}}')
STEAM_CSS = ('.steam{animation:steam 2.6s ease-in-out infinite}.steam.s1{animation-delay:-.9s}.steam.s2{animation-delay:-1.7s}\n'
             '@keyframes steam{0%{transform:translateY(4px);opacity:0}30%{opacity:.8}100%{transform:translateY(-10px);opacity:0}}')
TWINKLE_CSS = ('.twinkle{animation:twinkle 1.6s ease-in-out infinite}\n.twinkle.d2{animation-delay:-.55s}.twinkle.d3{animation-delay:-1.1s}\n'
               '@keyframes twinkle{0%,100%{transform:scale(.55) rotate(0);opacity:.35}50%{transform:scale(1.15) rotate(20deg);opacity:1}}')
