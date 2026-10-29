"""The WSJ door's scenes."""
import pathlib, shutil
from art import *
from shelves import *

REPO = pathlib.Path('/home/claude/liquor-cabinet')
D = REPO / 'src/pages/makers-mark/wsj/scenes'
D.mkdir(parents=True, exist_ok=True)
OUT = {}


def save(name, inner, label):
    OUT[name] = svg(inner, label)
    (D / f'{name}.svg').write_text(OUT[name] + '\n')


# ---------------------------------------------------------------- 1. THWAP (the same paper that lands at the end of Bill's door)
shutil.copy(REPO / 'src/pages/makers-mark/founders-gamble/scenes/thwap.svg', D / 'thwap.svg')
OUT['thwap'] = 'copied'

# ---------------------------------------------------------------- 2. Bill Jr., buried in letters, phones ringing
wall = wash('<rect x="0" y="30" width="400" height="176" fill="#ead8c6" opacity=".5"/>')
envelope = lambda x, y, w=26, tilt=0: (f'<g transform="rotate({tilt} {f(x + w / 2)} {f(y + w * .32)})">'
                                       + wash(f'<rect x="{f(x)}" y="{f(y)}" width="{w}" height="{f(w * .64)}" rx="1.5" fill="#fffaf1"/>')
                                       + lines(f'<rect x="{f(x)}" y="{f(y)}" width="{w}" height="{f(w * .64)}" rx="1.5" stroke-width="1.5"/><path d="M{f(x)} {f(y)} L{f(x + w / 2)} {f(y + w * .36)} L{f(x + w)} {f(y)}" stroke-width="1.3"/>', boil=False)
                                       + '</g>')
pile = lambda x, n, w=28: ''.join(envelope(x + (i % 2) * 3 - 1, 146 - i * 9, w, (-6, 4, -2, 7, -4, 3, -7, 5, 0)[i % 9]) for i in range(n))
phone = lambda x: (wash(f'<path d="M{x - 17} 150 L{x - 12} 128 L{x + 12} 128 L{x + 17} 150Z" fill="#3b2233"/><circle cx="{x}" cy="140" r="7" fill="#e6d3bd"/>'
                        f'<path d="M{x - 20} 126 Q{x - 20} 116 {x - 12} 116 L{x + 12} 116 Q{x + 20} 116 {x + 20} 126 L{x + 14} 128 L{x - 14} 128Z" fill="#3b2233"/>')
                   + lines(f'<path d="M{x - 17} 150 L{x - 12} 128 L{x + 12} 128 L{x + 17} 150Z"/><circle cx="{x}" cy="140" r="7" stroke-width="1.5"/>'
                           f'<path d="M{x - 20} 126 Q{x - 20} 116 {x - 12} 116 L{x + 12} 116 Q{x + 20} 116 {x + 20} 126"/>', boil=False, width=2))
ring = lambda x, d: (f'<g class="ring" style="animation-delay:{d}s;transform-origin:{x}px 150px">{phone(x)}</g>'
                     f'<g class="ring-word" style="animation-delay:{d}s"><text class="letter" x="{x}" y="104" font-size="15" text-anchor="middle">RING!</text></g>'
                     + lines(f'<path d="M{x - 26} 120 l-7 -4 M{x + 26} 120 l7 -4 M{x - 24} 132 l-8 0 M{x + 24} 132 l8 0" stroke-width="2"/>', boil=False, extra=f' class="ring-word" style="animation-delay:{d}s"'))
desk = ('<rect x="52" y="152" width="296" height="54" fill="#d8c0a4"/>'
        + wash('<rect x="40" y="150" width="320" height="10" fill="#9b7663"/><rect x="52" y="160" width="296" height="46" fill="#b08463"/>')
        + lines('<path d="M40 150 H360 V160 H40Z M52 160 V206 M348 160 V206"/><path d="M190 172 h20 M190 190 h20" stroke-width="2"/>', boil=False, width=2.2))
# the handset sits against his ear, beside the face (not across it), its cord curling down to the desk
HS = 'M-16 -156 q-9 0 -9 8 l0 24 q0 8 9 8 l3 0 l0 -7 q-5 0 -5 -4 l0 -18 q0 -4 5 -4 l0 -7Z'
receiver = (wash(f'<path d="{HS}" fill="#3b2233"/>') + lines(f'<path d="{HS}" stroke-width="1.8"/>', boil=False)
            + lines('<path d="M-24 -122 q-10 12 -4 22 q6 10 -4 20 q-10 10 -2 22" stroke="#3b2233" stroke-width="1.6"/>', boil=False))
junior = everyman(mood='o', eyes='dot', top='#5f6f8c', pants='#8c7a6b', tie='#8b3a63', hat='hair',
                  arm_l=[(-21, -109), (-34, -124), (-23, -140)], arm_r=[(21, -109), (34, -96), (46, -104)])
flying = ''.join(f'<g class="fly-in" style="animation-delay:{d}s">{envelope(x, y, 22, t)}</g>' for x, y, t, d in ((14, 40, -14, 0), (40, 70, 10, -1.1), (6, 96, -6, -2.2), (60, 30, 18, -3.3)))
save('letters', wall + place(junior + receiver, 200, 206, .95) + desk + pile(70, 6) + pile(250, 8) + pile(300, 4, 24) + ring(126, 0) + ring(276, -.4) + flying,
     'Bill Jr. at a desk buried in piles of letters, a phone at his ear while two more phones ring, and more letters flying in')

# ---------------------------------------------------------------- 3. Sold out: a Maker's-shaped gap on the top shelf
gap_x = 217
gap = ('<g transform="translate(%d %d) scale(.68)">' % (gap_x, TOP)
       + '<path d="M-13 0 L-13 -38 Q-13 -46 -6 -50 L-5 -62 L5 -62 L6 -50 Q13 -46 13 -38 L13 0Z M-5.5 -68 h11 v6 h-11Z" fill="none" stroke="#8a6a78" stroke-width="2.2" stroke-dasharray="4 4"/></g>')
sold_top = (decanter(180, TOP, color='#c98a3c', label='Scotch') + gap + decanter(256, TOP, w=22, h=36, color='#a0522d')
            + decanter(292, TOP, color='#7f9a6c', label='Scotch') + decanter(328, TOP, w=22, h=36, color='#c98a3c') + decanter(364, TOP, color='#a0522d', label='Scotch'))
sign = ('<g transform="rotate(-5 217 104)">'
        + wash('<rect x="174" y="88" width="88" height="40" rx="2" fill="#fffaf1"/>')
        + lines('<rect x="174" y="88" width="88" height="40" rx="2" stroke-width="1.8"/>', boil=False)
        + wash('<rect x="166" y="83" width="22" height="9" fill="#f2c776" opacity=".85" transform="rotate(-20 177 87)"/><rect x="248" y="83" width="22" height="9" fill="#f2c776" opacity=".85" transform="rotate(18 259 87)"/>')
        + '<text class="letter" x="218" y="106" font-size="15" text-anchor="middle" style="fill:#c0392b">SOLD OUT.</text>'
        + '<text class="letter" x="218" y="121" font-size="10.5" text-anchor="middle">Ask us next week!</text></g>')
shopper = everyman(mood='sad', eyes='side')
huh = '<text class="letter pop" x="120" y="40" font-size="26" style="transform-origin:126px 32px">?!</text>'
save('soldout', shelf_unit() + ground() + sold_top + middle_row() + bottom_shelf() + sign + place(shopper, 104, 206, .92) + huh,
     "A liquor store shelf with a Maker's-shaped gap on the top shelf and a handwritten sign taped to the edge: SOLD OUT. Ask us next week! A customer stares at it")

# ---------------------------------------------------------------- 4. The line around the store
store = (wash('<rect x="252" y="46" width="148" height="160" fill="#c99b72"/><rect x="246" y="38" width="154" height="12" fill="#9b7663"/>'
              '<rect x="300" y="94" width="88" height="80" fill="#e7f1fb" opacity=".85"/><rect x="262" y="118" width="28" height="88" fill="#7a5f4a"/>')
         + lines('<rect x="252" y="46" width="148" height="160"/><rect x="246" y="38" width="154" height="12"/><rect x="300" y="94" width="88" height="80"/>'
                 '<rect x="262" y="118" width="28" height="88"/><circle cx="284" cy="164" r="2" fill="#3b2233"/><path d="M306 100 l14 -0 M306 106 l8 0" stroke="#fffaf1" stroke-width="2"/>', boil=False, width=2.2)
         + wash('<rect x="282" y="58" width="96" height="22" rx="3" fill="#8b3a63"/>') + lines('<rect x="282" y="58" width="96" height="22" rx="3"/>', boil=False)
         + '<text class="letter" x="330" y="74" font-size="13" text-anchor="middle" style="fill:#fffaf1;letter-spacing:.12em">LIQUORS</text>')
case = (wash('<rect x="322" y="150" width="44" height="18" fill="#b08463"/>') + lines('<rect x="322" y="150" width="44" height="18"/><rect x="326" y="108" width="36" height="42" stroke="#8ecae6" stroke-width="1.8"/>', boil=False)
        + generic_bottle(344, 150, .55, swap='makers-bottle-sm'))
shine = sparkle(318, 112, 6, 'twinkle') + sparkle(372, 120, 5, 'twinkle d2') + sparkle(344, 100, 4, 'twinkle d3')
crowd = ''
looks = [('#9db08a', 'cap'), ('#c25c86', 'hair'), ('#6d7f99', 'fedora'), ('#e6b264', 'cap'), ('#b9a3c8', 'hair'), ('#7f9a6c', 'fedora'), ('#c0583c', 'cap'), ('#8a8f96', 'hair'), ('#c98a3c', 'fedora')]
for i, (top, hat) in enumerate(looks):   # single file from the door, running off the left edge
    x = 240 - i * 30
    person = everyman(mood='o' if i % 3 == 0 else 'smile', eyes='side', top=top, hat=hat, hair=('#6b4632', '#3b2a22', '#b9792c')[i % 3])
    crowd += f'<g class="shuffle" style="animation-delay:{-i * .37:.2f}s">{place(person, x, 206, .5)}</g>'
back_row = ''
bangs = '<text class="letter pop" x="150" y="64" font-size="20" style="transform-origin:156px 56px">!!</text>'
save('line', ground() + store + case + shine + back_row + crowd + bangs,
     "A long line of people wrapped around a liquor store, every one of them staring at one bottle of Maker's Mark in a glass case in the window")

# ---------------------------------------------------------------- 5. The top shelf fills up, year by year
makers = generic_bottle(180, TOP, .68, swap='makers-bottle-sm')
newcomers = [(224, '1984', decanter(224, TOP, w=24, h=34, color='#c98a3c')), (264, '1988', decanter(264, TOP, w=22, h=38, color='#a0522d')),
             (304, '1992', decanter(304, TOP, w=26, h=32, color='#7f9a6c')), (346, '1996', decanter(346, TOP, w=24, h=36, color='#b9792c'))]
arrivals = ''.join(f'<g class="arrive a{i + 1}">{b}{shelf_label(x, TOP, yr, size=10.5, tilt=(-3, 3)[i % 2])}{sparkle(x + 12, 40, 5, "twinkle")}</g>' for i, (x, yr, b) in enumerate(newcomers))
first = shelf_label(180, TOP, '1958', size=10.5)
save('premium', shelf_unit() + ground() + makers + first + arrivals + middle_row() + bottom_shelf(),
     "The liquor store shelf again: Maker's Mark, since 1958, on the top shelf, and one fancy new bourbon after another arriving next to it: 1984, 1988, 1992, 1996. The cheap jugs still sit on the bottom shelf")

print('scenes:', ', '.join(OUT))
