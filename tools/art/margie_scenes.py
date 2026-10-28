"""Margie's door scenes."""
import pathlib
from art import *

REPO = pathlib.Path('/home/claude/liquor-cabinet')
D = REPO / 'src/pages/makers-mark/margie/scenes'
D.mkdir(parents=True, exist_ok=True)
OUT = {}


def save(name, inner, label):
    OUT[name] = svg(inner, label)
    (D / f'{name}.svg').write_text(OUT[name] + '\n')


hills = wash('<path d="M0 172 Q70 146 160 162 T300 150 T400 158 L400 206 L0 206Z" fill="#c8d5b0" opacity=".6"/>')
sun = wash('<circle cx="64" cy="54" r="22" fill="#f2c776"/>')

# ---------------------------------------------------------------- 1. Meet Margie
m = margie(arm_r=[(19, -108), (33, -124), (38, -148)], arm_cls=('', 'wave-arm'))
hello = '<text class="letter pop" x="312" y="78" font-size="32" text-anchor="middle" style="transform-origin:312px 68px">Hello!</text>'
flowers = ''.join(lines(f'<path d="M{x} 206 V{196 - h}"/>', boil=False, color='#7f9a6c', width=2) + wash(f'<circle cx="{x}" cy="{192 - h}" r="5" fill="{c}"/>') + lines(f'<circle cx="{x}" cy="{192 - h}" r="5"/>', boil=False, width=1.6)
                  for x, h, c in [(300, 8, '#e48b7c'), (316, 2, '#f2c776'), (332, 10, '#c25c86'), (350, 4, '#e48b7c'), (84, 6, '#c25c86'), (100, 0, '#f2c776')])
save('hello', sun + hills + ground() + flowers + place(m, 180, 206, 1.1) + hello,
     'Margie Samuels, in a pink polka-dot dress, pearls and curls, waves hello')

# ---------------------------------------------------------------- 2. The bread test
oven = (wash('<rect x="14" y="96" width="92" height="110" rx="4" fill="#8a8f96"/><rect x="24" y="118" width="72" height="54" rx="3" fill="#3b2233"/>'
             '<path d="M24 172 L10 196 L110 196 L96 172Z" fill="#a9a29a"/><circle cx="34" cy="106" r="3.5" fill="#e6b264"/><circle cx="48" cy="106" r="3.5" fill="#e6b264"/>')
        + lines('<rect x="14" y="96" width="92" height="110" rx="4"/><rect x="24" y="118" width="72" height="54" rx="3"/><path d="M24 172 L10 196 L110 196 L96 172Z"/>'
                '<circle cx="34" cy="106" r="3.5"/><circle cx="48" cy="106" r="3.5"/>', boil=False, width=2.2)
        + wash('<path d="M36 166 Q60 140 84 166" fill="#e6874a" opacity=".55"/>'))
loaf = lambda x, y, c: (wash(f'<path d="M{x - 13} {y} Q{x - 14} {y - 15} {x} {y - 16} Q{x + 14} {y - 15} {x + 13} {y}Z" fill="{c}"/>')
                        + lines(f'<path d="M{x - 13} {y} Q{x - 14} {y - 15} {x} {y - 16} Q{x + 14} {y - 15} {x + 13} {y}Z"/><path d="M{x - 6} {y - 12} l3 4 M{x} {y - 13} l3 4 M{x + 6} {y - 12} l3 4" stroke-width="1.4"/>', boil=False, width=2))
flag = lambda x, y, t: (lines(f'<path d="M{x} {y} V{y - 22}"/>', boil=False, width=1.3)
                        + wash(f'<path d="M{x} {y - 22} h30 l-5 6 l5 6 h-30Z" fill="#fffaf1"/>')
                        + lines(f'<path d="M{x} {y - 22} h30 l-5 6 l5 6 h-30Z" stroke-width="1.2"/>', boil=False)
                        + f'<text class="letter" x="{x + 13}" y="{y - 13}" font-size="8.4" text-anchor="middle">{t}</text>')
# Margie, facing right, carrying a tray of test loaves out of the oven, each one flagged with its grain
tray_local = (wash('<rect x="22" y="-100" width="92" height="5" rx="2" fill="#a9a29a"/>') + lines('<rect x="22" y="-100" width="92" height="5" rx="2"/>', boil=False, width=1.8)
              + loaf(38, -100, '#c99b72') + loaf(68, -100, '#e0b47c') + loaf(98, -100, '#a0704c')
              + flag(24, -114, 'RYE') + flag(60, -128, 'WHEAT') + flag(92, -114, 'CORN'))
baker = margie(arm_l=[(-19, -108), (6, -94), (30, -98)], arm_r=[(19, -108), (40, -94), (102, -98)])
mitt = wash('<ellipse cx="30" cy="-98" rx="7" ry="5.5" fill="#c0583c"/><ellipse cx="102" cy="-98" rx="7" ry="5.5" fill="#c0583c"/>') + lines('<ellipse cx="30" cy="-98" rx="7" ry="5.5"/><ellipse cx="102" cy="-98" rx="7" ry="5.5"/>', boil=False, width=1.8)
steam = lines('<path d="M-6 0 q-4 -6 0 -12 q4 -6 0 -12 M-6 0" />', boil=False, color='#b9a69a', width=1.8)
steams = ''.join(f'<g class="steam" style="animation-delay:{d}s" transform="translate({x} -120)">{steam}</g>' for x, d in ((40, 0), (70, -.7), (100, -1.4)))
# Bill, blindfolded, taking a bite of a slice
slice_ = wash('<path d="M2 -138 q0 -8 7 -8 q7 0 7 8 v9 h-14Z" fill="#e0b47c"/>') + lines('<path d="M2 -138 q0 -8 7 -8 q7 0 7 8 v9 h-14Z" stroke-width="1.6"/>', boil=False)
taster = bill(mood='o', arm_r=[(22, -113), (19, -92), (12, -130)], holding_r=slice_)
blindfold = (wash('<path d="M-17 -147 Q0 -151 17 -147 L17 -138 Q0 -142 -17 -138Z" fill="#7d2f58"/><path d="M17 -144 l9 -6 l1 8Z M17 -142 l8 6 l-6 3Z" fill="#7d2f58"/>')
             + lines('<path d="M-17 -147 Q0 -151 17 -147 L17 -138 Q0 -142 -17 -138Z M17 -144 l9 -6 l1 8Z M17 -142 l8 6 l-6 3Z" stroke-width="1.8"/>', boil=False))
chomp = '<text class="letter pop" x="350" y="40" font-size="21" text-anchor="middle" style="transform-origin:350px 32px">chomp!</text>'
save('bread', oven + ground() + place(baker + mitt + tray_local + steams, 134, 206, .98) + place(f'<g class="bite">{taster}{blindfold}</g>', 326, 206, .95) + chomp,
     'Margie carries a tray of fresh test loaves out of the oven, each flagged with its grain: rye, wheat, corn. Bill, blindfolded, takes a bite: chomp!')

# ---------------------------------------------------------------- 3. The pewter mark
# The mug sits upside down on a little side table; Margie holds a magnifying glass over the stamp on its bottom
side_table = (wash('<rect x="200" y="148" width="60" height="7" rx="2" fill="#b08463"/><path d="M208 155 L206 206 M252 155 L254 206" stroke="#9b7663" stroke-width="5"/>')
              + lines('<rect x="200" y="148" width="60" height="7" rx="2"/><path d="M208 155 L206 206 M252 155 L254 206"/>', boil=False, width=2))
mug = (wash('<path d="M216 148 L218 120 L242 120 L244 148Z" fill="#a9a29a"/><ellipse cx="230" cy="120" rx="12" ry="4" fill="#c9c3b8"/><path d="M244 128 q12 2 10 12 q-2 7 -11 6" fill="none" stroke="#8a8f96" stroke-width="4"/>')
       + lines('<path d="M216 148 L218 120 M242 120 L244 148 M216 148 Q230 151 244 148"/><ellipse cx="230" cy="120" rx="12" ry="4"/><path d="M244 128 q12 2 10 12 q-2 7 -11 6" stroke-width="1.8"/>'
               '<circle cx="230" cy="120" r="2" stroke-width="1.3"/>', boil=False, width=2)
       + lines('<path d="M221 134 h18" stroke="#fffaf1" stroke-width="1.6"/>', boil=False))
shower = margie(eyes='dot', arm_r=[(19, -108), (40, -110), (60, -118)])
lens = (lines('<path d="M196 92 L214 102" stroke="#7a5f4a" stroke-width="5"/>', boil=False)
        + wash('<circle cx="226" cy="108" r="13" fill="#e7f1fb" opacity=".75"/>') + lines('<circle cx="226" cy="108" r="13" stroke-width="3"/>', boil=False))
# the zoomed-in stamp: a little crowned rose with the pewterer's initials
ZX, ZY = 290, 48
zoom = (wash(f'<circle cx="{ZX}" cy="{ZY}" r="40" fill="#d9dde2"/>') + lines(f'<circle cx="{ZX}" cy="{ZY}" r="40" stroke-width="2.6"/><circle cx="{ZX}" cy="{ZY}" r="33" stroke="#8a8f96" stroke-width="1.6"/>', boil=False)
        + lines(f'<path d="M{ZX - 14} {ZY - 12} l4 -10 l5 7 l5 -9 l5 9 l5 -7 l4 10Z" stroke="#5a5f66" stroke-width="2"/><circle cx="{ZX}" cy="{ZY + 6}" r="9" stroke="#5a5f66" stroke-width="2"/>'
                f'<path d="M{ZX} {ZY - 3} q5 5 0 9 q-5 5 0 9 M{ZX - 9} {ZY + 6} q5 -5 9 0 q5 5 9 0" stroke="#5a5f66" stroke-width="1.6"/>', boil=False)
        + f'<text class="letter" x="{ZX}" y="{ZY + 30}" font-size="10" text-anchor="middle" style="fill:#5a5f66;letter-spacing:.2em">I · M</text>')
zoom_line = lines(f'<path d="M236 98 L{ZX - 30} {ZY + 24}" stroke="#8a8f96" stroke-width="1.6" stroke-dasharray="3 4"/>', boil=False)
ooh = '<text class="letter pop" x="368" y="30" font-size="21" text-anchor="middle" style="transform-origin:368px 22px">Ooh!</text>'
look = bill(mood='o', eyes='dot')
save('pewter', ground() + side_table + mug + place(shower, 134, 206, 1.0) + f'<g class="peer">{lens}</g>' + zoom_line + f'<g class="float">{zoom}</g>' + place(look, 366, 206, .95) + ooh + sparkle(250, 112, 4.5, 'twinkle'),
     "Margie holds up a pewter mug and a magnifying glass. Blown up big, the little stamp on the bottom is a crowned rose with the pewterer's initials. Bill: Ooh!")

# ---------------------------------------------------------------- 4. The wax kitchen
table = ('<rect x="0" y="160" width="400" height="46" fill="#f2e6d6"/>' + wash('<rect x="0" y="150" width="400" height="10" fill="#b08463"/><rect x="0" y="160" width="400" height="46" fill="#e6d3bd"/>')
         + lines('<path d="M0 150 H400 M0 160 H400"/><path d="M90 168 v30 M190 168 v30 M290 168 v30" stroke-width="1.4" stroke="#b9a69a"/>', boil=False, width=2.2))
pm_bottle = (wash('<path d="M28 150 L28 110 Q28 100 38 96 L38 78 L50 78 L50 96 Q60 100 60 110 L60 150Z" fill="#cfc6bd"/>')
             + lines('<path d="M28 150 L28 110 Q28 100 38 96 L38 78 L50 78 L50 96 Q60 100 60 110 L60 150Z"/>'
                     '<path d="M30 120 l26 -6 M30 132 l28 4 M32 142 l24 -5 M40 90 l9 2" stroke="#9a8a92" stroke-width="1.3"/>', boil=False, width=2.2)
             + '<text class="letter" x="44" y="128" font-size="6.5" text-anchor="middle" style="fill:#7a6f6a">news</text>')
FX = 296
fryer = (wash(f'<path d="M{FX - 40} 150 L{FX - 34} 118 L{FX + 34} 118 L{FX + 40} 150Z" fill="#8a8f96"/><ellipse cx="{FX}" cy="118" rx="34" ry="7" fill="#b8312f"/>')
         + lines(f'<path d="M{FX - 40} 150 L{FX - 34} 118 M{FX + 34} 118 L{FX + 40} 150 M{FX - 40} 150 H{FX + 40}"/><ellipse cx="{FX}" cy="118" rx="34" ry="7"/><path d="M{FX - 34} 124 h-12 M{FX + 34} 124 h12" stroke-width="3"/>', boil=False, width=2.2))
bubbles = ''.join(f'<circle class="wax-bubble" style="animation-delay:{d}s" cx="{FX + dx}" cy="118" r="{r}" fill="#d9483f" stroke="#5b2c4c" stroke-width="1"/>' for dx, r, d in ((-18, 3, 0), (14, 2.4, -.5), (24, 3.2, -1), (-6, 2, -1.4)))
# pose A: a bare bottle, upside down, going into the wax. pose B: the finished bottle held up, dripping red
bare = f'<g transform="translate({FX} 72) rotate(180) scale(.68)">{generic_bottle(0, 0, 1.0)}</g>'
done = generic_bottle(0, 0, .95, swap='makers-bottle-sm')
dipper_a = margie(arm_r=[(19, -108), (34, -120), (46, -124)], arm_l=[(-19, -108), (-25, -86), (-23, -66)])
dipper_b = margie(mood='grin', arm_r=[(19, -108), (34, -126), (40, -148)], arm_l=[(-19, -108), (-25, -86), (-23, -66)])
margie_a = f'<g class="pose-a">{place(dipper_a, 246, 206, 1.08)}{bare}</g>'
margie_b = f'<g class="pose-b">{place(dipper_b + f"<g transform=\"translate(40 -124)\">{done}</g>", 246, 206, 1.08)}' + sparkle(318, 30, 7, 'twinkle') + sparkle(336, 70, 5, 'twinkle d2') + sparkle(268, 40, 4.5, 'twinkle d3') + '</g>'
tada = '<g class="pose-b"><text class="letter pop" x="150" y="60" font-size="24" text-anchor="middle" style="transform-origin:150px 52px">Ta-da!</text></g>'
dip = '<g class="pose-a"><text class="letter" x="356" y="98" font-size="17" text-anchor="middle">dip...</text></g>'
save('wax', ground() + margie_a + margie_b + table + pm_bottle + fryer + bubbles + dip + tada,
     "Margie's kitchen: a papier-mache model bottle on the table and a deep fryer bubbling with red wax. Margie dips a bottle in upside down... and holds up the finished Maker's Mark, dripping red: Ta-da!")

# ---------------------------------------------------------------- 5. The restored distillery
def building(x, w, h, roof, body='#6b4632', shutters=True):
    top = 206 - h
    out = wash(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{body}"/><path d="M{x - 6} {top + 2} L{x + w / 2} {top - roof} L{x + w + 6} {top + 2}Z" fill="#4a3426"/>')
    wins = ''
    for wy in range(top + 14, 196 - 18, 30):
        for wx in range(x + 10, x + w - 14, 24):
            wins += f'<rect x="{wx}" y="{wy}" width="10" height="14" fill="#f6e6c8"/>'
            if shutters:
                wins += f'<rect x="{wx - 5}" y="{wy}" width="4" height="14" fill="#c0392b"/><rect x="{wx + 11}" y="{wy}" width="4" height="14" fill="#c0392b"/>'
    out += wash(wins)
    out += lines(f'<rect x="{x}" y="{top}" width="{w}" height="{h}"/><path d="M{x - 6} {top + 2} L{x + w / 2} {top - roof} L{x + w + 6} {top + 2}"/>', boil=False, width=2.2)
    return out
town = building(150, 78, 96, 26) + building(236, 64, 120, 30) + building(308, 84, 88, 24)
cupola = wash('<rect x="261" y="48" width="14" height="16" fill="#4a3426"/><path d="M257 50 L268 36 L279 50Z" fill="#4a3426"/>') + lines('<rect x="261" y="48" width="14" height="16"/><path d="M257 50 L268 36 L279 50Z"/>', boil=False, width=2)
path_ = wash('<path d="M0 222 Q120 214 180 208 L250 206 L232 214 Q120 226 0 236Z" fill="#e2cfa6"/>')
gleam = sparkle(176, 92, 6, 'twinkle') + sparkle(300, 70, 7, 'twinkle d2') + sparkle(372, 106, 5, 'twinkle d3') + sparkle(214, 128, 4, 'twinkle d2')
walkers = ''
for i, (top, pants, hat) in enumerate((('#9db08a', '#8c7a6b', 'cap'), ('#c25c86', '#6f6760', 'hair'), ('#6d7f99', '#8c7a6b', 'fedora'), ('#e6b264', '#5a4636', 'cap'))):
    person = everyman(mood='smile', top=top, pants=pants, hat=hat, hair='#6b4632')
    walkers += f'<g class="stroll" style="animation-delay:{-i * 2.5}s;--rest:{24 + i * 38}px">{place(f"<g class=\"bob\">{person}</g>", 0, 214, .42)}</g>'
save('restore', path_ + town + cupola + ground() + gleam + walkers,
     'The old Victorian distillery buildings, restored: dark brown with red shutters, gleaming, while a little line of visitors walks up the path')

print('scenes:', ', '.join(OUT))
