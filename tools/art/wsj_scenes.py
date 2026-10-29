"""The WSJ door's scenes."""
import math, pathlib
from art import *
from shelves import *

REPO = pathlib.Path('/home/claude/liquor-cabinet')
D = REPO / 'src/pages/makers-mark/wsj/scenes'
D.mkdir(parents=True, exist_ok=True)
OUT = {}


def save(name, inner, label, view=None):
    OUT[name] = svg(inner, label) if not view else f'<svg viewBox="{view}" role="img" aria-label="{label}">{inner}</svg>'

    (D / f'{name}.svg').write_text(OUT[name] + '\n')


# ---------------------------------------------------------------- 1. Everybody reads it, everybody thinks the same thing
def cloud(cx, cy, rx, ry, n=9):
    """A bumpy thought cloud: n bulges around an ellipse."""
    ring_ = [(cx + rx * math.cos(2 * math.pi * k / n - math.pi / 2), cy + ry * math.sin(2 * math.pi * k / n - math.pi / 2)) for k in range(n)]
    d = f'M{f(ring_[0][0])} {f(ring_[0][1])}'
    for k in range(n):
        a = 2 * math.pi * (k + .5) / n - math.pi / 2
        x2, y2 = ring_[(k + 1) % n]
        d += f' Q{f(cx + rx * 1.42 * math.cos(a))} {f(cy + ry * 1.42 * math.sin(a))} {f(x2)} {f(y2)}'
    return d + 'Z'


town = wash('<rect x="0" y="0" width="400" height="220" fill="#eef3f6" opacity=".7"/>'
            '<path d="M0 220 V120 H34 V96 H70 V132 H96 V84 H136 V118 H166 V100 H214 V126 H240 V78 H284 V112 H316 V94 H352 V124 H400 V220Z" fill="#d9cfe0" opacity=".55"/>')
paper_d = 'M-36 -121 L36 -123 L37 -64 L-35 -62Z'
paper = (wash(f'<path d="{paper_d}" fill="#fffaf1"/><rect x="-31" y="-118" width="62" height="6" fill="#3b2233" opacity=".8"/>')
         + lines(f'<path d="{paper_d}" stroke-width="2"/><path d="M0.5 -122 L1 -63" stroke-width="1.3"/>'
                 '<path d="M-30 -107 h26 M-30 -102 h22 M5 -107 h26 M5 -102 h18" stroke-width="2.4"/>'
                 '<path d="M-30 -96 h12 M-15 -96 h11 M-30 -91 h12 M-15 -91 h11 M-30 -86 h12 M-15 -86 h11 M-30 -81 h12 M-15 -81 h8 M-30 -76 h12 M-15 -76 h11 M-30 -71 h9'
                 ' M5 -96 h12 M20 -96 h11 M5 -91 h12 M20 -91 h11 M5 -86 h12 M20 -86 h11 M5 -81 h12 M20 -81 h9 M5 -76 h12 M20 -76 h11 M5 -71 h10" stroke-width="1.1"/>', boil=False)
         + '<text class="letter" x="0" y="-113.6" font-size="4.4" text-anchor="middle" style="fill:#fffaf1">AUGUST 1, 1980</text>')
thumbs = wash(f'<circle cx="-36" cy="-96" r="5" fill="{SKIN}"/><circle cx="36" cy="-98" r="5" fill="{SKIN}"/>') + lines('<circle cx="-36" cy="-96" r="5"/><circle cx="36" cy="-98" r="5"/>', width=2)


def reader(top, hat, hair, mood, tie, k):
    p = everyman(mood=mood, eyes='dot', top=top, tie=tie, hat=hat, hair=hair, parts=True,
                 arm_l=[(-21, -109), (-30, -102), (-35, -96)], arm_r=[(21, -109), (30, -104), (35, -98)])
    return p['left'] + p['right'] + p['body'] + p['head'] + f'<g class="rustle" style="transform-origin:0 -92px;animation-delay:{-k * .7:.1f}s">{paper}{thumbs}</g>'


people = [(46, 220, .68, '#9db08a', 'cap', '#6b4632', 'o', '#c0583c'), (124, 216, .71, '#c25c86', 'hair', '#3b2a22', 'smile', '#5b8aa6'),
          (202, 221, .68, '#6d7f99', 'fedora', '#6b4632', 'o', '#8b3a63'), (279, 216, .72, '#e6b264', 'hair', '#b9792c', 'smile', '#7f9a6c'),
          (356, 220, .68, '#b9a3c8', 'cap', '#3b2a22', 'o', '#c0583c')]
crowd, bubbles = '', ''
for k, (x, y, sc, top, hat, hair, mood, tie) in enumerate(people):
    crowd += place(reader(top, hat, hair, mood, tie, k), x, y, sc)
    head_top = y - 160 * sc
    cy = 40 + (k % 2) * 8
    trail = (wash(f'<circle cx="{x + 4}" cy="{f(head_top - 7)}" r="3" fill="#fffaf1"/><circle cx="{x + 8}" cy="{f(head_top - 17)}" r="4.4" fill="#fffaf1"/>')
             + lines(f'<circle cx="{x + 4}" cy="{f(head_top - 7)}" r="3"/><circle cx="{x + 8}" cy="{f(head_top - 17)}" r="4.4"/>', boil=False, width=1.7))
    cl = cloud(x, cy, 25, 21)
    bub = wash(f'<path d="{cl}" fill="#fffaf1"/>') + lines(f'<path d="{cl}"/>', boil=False, width=2)
    bottle = f'<g class="think-b k{k + 1}" style="transform-origin:{x}px {cy + 18}px">{generic_bottle(x, cy + 18, .5, swap="makers-bottle-sm")}</g>'
    bubbles += f'<g class="think k{k + 1}" style="transform-origin:{x + 4}px {f(head_top - 4)}px">{trail}{bub}{bottle}</g>'
save('readers', town + ground(220) + crowd + bubbles,
     "A crowd of people reading the August 1, 1980 newspaper, and one by one a bottle of Maker's Mark pops into a thought bubble over each of their heads")

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
# overwhelmed: both hands clutching his head, mouth open, sweat flying
jr = everyman(mood='o', eyes='dot', top='#5f6f8c', pants='#8c7a6b', tie='#8b3a63', hat='hair', parts=True,
              arm_l=[(-21, -109), (-39, -126), (-18, -150)], arm_r=[(21, -109), (39, -126), (18, -150)])
sweat_drop = lambda x, y: f'<path d="M{x} {y - 5} q-4 5.5 0 8.8 q4 -3.3 0 -8.8Z" fill="#8ecae6" stroke="#5b8aa6" stroke-width="1.2"/>'
sweat = ''.join(f'<g class="sweat {c}" style="animation-delay:{d}s">{sweat_drop(x, y)}</g>' for x, y, c, d in ((-27, -160, 'l', 0), (27, -162, 'r', -.5), (-31, -142, 'l', -.9), (31, -146, 'r', -1.3)))
brows = lines('<path d="M-11 -142 L-3 -146 M11 -142 L3 -146" stroke-width="2.2"/>')
junior = jr['body'] + jr['head'] + brows + jr['left'] + jr['right'] + sweat
flying = ''.join(f'<g class="fly-in" style="animation-delay:{d}s">{envelope(x, y, 22, t)}</g>' for x, y, t, d in ((14, 40, -14, 0), (40, 70, 10, -1.1), (6, 96, -6, -2.2), (60, 30, 18, -3.3)))
save('letters', wall + place(junior, 200, 206, .95) + desk + pile(70, 6) + pile(250, 8) + pile(300, 4, 24) + ring(126, 0) + ring(276, -.4) + flying,
     'Bill Jr. at a desk buried in piles of letters, clutching his head, while two phones ring and more letters fly in')

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
bangs = '<text class="letter pop" x="150" y="64" font-size="20" style="transform-origin:156px 56px">!!</text>'
save('line', ground() + store + case + shine + crowd + bangs,
     "A long line of people wrapped around a liquor store, every one of them staring at one bottle of Maker's Mark in a glass case in the window")

# ---------------------------------------------------------------- 5. The top shelf fills up, year by year
makers = generic_bottle(180, TOP, .68, swap='makers-bottle-sm')
# real bottle photos (src/photos), about as tall as the Maker's beside them; the crayon decanters stand in without them
photo = lambda name, x, h, drawing: f'<!--swap:{name}|{f(x - 16)} {TOP - h} 32 {h}-->{drawing}<!--/swap-->'
newcomers = [(224, '1984', photo('blantons-bottle', 224, 42, decanter(224, TOP, w=24, h=34, color='#c98a3c'))),
             (264, '1988', photo('bookers-bottle', 264, 49, decanter(264, TOP, w=22, h=38, color='#a0522d'))),
             (304, '1992', photo('knob-creek-bottle', 304, 44, decanter(304, TOP, w=26, h=32, color='#7f9a6c'))),
             (346, '1996', photo('woodford-bottle', 346, 46, decanter(346, TOP, w=24, h=36, color='#b9792c')))]
arrivals = ''.join(f'<g class="arrive a{i + 1}">{b}{shelf_label(x, TOP, yr, size=10.5, tilt=(-3, 3)[i % 2])}{sparkle(x + 12, 40, 5, "twinkle")}</g>' for i, (x, yr, b) in enumerate(newcomers))
first = shelf_label(180, TOP, '1958', size=10.5)
save('premium', shelf_unit() + ground() + makers + first + arrivals + middle_row() + bottom_shelf(),
     "The liquor store shelf again: Maker's Mark, since 1958, on the top shelf, and one premium bourbon after another arriving next to it: Blanton's in 1984, Booker's in 1988, Knob Creek in 1992, Woodford Reserve in 1996. The cheap jugs still sit on the bottom shelf",
     view='138 0 270 222')   # framed tight on the shelf so the bottles read on a phone

# ---------------------------------------------------------------- 6. Out the door, onto the truck, again and again
# Timing (page.css): each truck runs a 16 s loop, the second one 8 s behind the first. A truck backs in
# (0-1.2 s), loads (1.2-6.4 s), drives off (6.4-7.6 s). Bottle k leaves the door at starts[k] in every
# 8 s turn, lands 0.8 s later, and its twin in the truck bed switches on at that moment.
sky = wash('<rect x="0" y="0" width="400" height="206" fill="#eef3f6" opacity=".7"/><path d="M120 206 Q200 150 290 170 T400 150 V206Z" fill="#cfe0c4" opacity=".6"/>')
plant = (wash('<path d="M-6 74 L64 30 L134 74Z" fill="#7a4a34"/><rect x="0" y="72" width="128" height="134" fill="#9b6a4c"/>'
              '<rect x="72" y="118" width="50" height="88" fill="#3b2233"/><rect x="12" y="92" width="30" height="34" fill="#f6e6c8"/><rect x="76" y="86" width="42" height="18" fill="#fffaf1"/>')
         + lines('<path d="M-6 74 L64 30 L134 74"/><rect x="0" y="72" width="128" height="134"/><rect x="72" y="118" width="50" height="88"/>'
                 '<rect x="12" y="92" width="30" height="34"/><path d="M27 92 V126 M12 109 H42" stroke-width="1.6"/><rect x="76" y="86" width="42" height="18" stroke-width="1.6"/>'
                 '<path d="M6 150 h14 M30 170 h12 M10 188 h10 M46 140 h10 M50 196 h12" stroke-width="1.5"/>', boil=False, width=2.2)
         + '<text class="letter" x="97" y="99" font-size="8.6" text-anchor="middle">SHIPPING</text>')
waiting = ''.join(generic_bottle(x, 178, .5, swap='makers-bottle-sm') for x in (80, 92))   # more where those came from
belt = (wash('<rect x="88" y="178" width="64" height="5" fill="#8a8f96"/>')
        + lines('<path d="M88 178 H152 M88 183 H152 M96 183 V206 M144 183 V206" stroke-width="2"/>'
                + ''.join(f'<circle cx="{x}" cy="180.5" r="1.6" stroke-width="1.2"/>' for x in range(92, 152, 8)), boil=False))
X0, Y0 = 104, 178
back = [(266 - 20 * i, 172) for i in range(6)]
front = [(256 - 20 * i, 179) for i in range(6)]
slots = [p for pair in zip(back, front) for p in pair]   # fills from the cab end toward the tailgate
starts = [1.0 + .42 * k for k in range(len(slots))]      # seconds into each 8 s loading turn


def truck(color, cls, delay):
    bed = ''.join(f'<g class="stow{" late" if k >= 8 else ""}" style="animation-delay:{f(t + .8 - 8 + delay)}s">{generic_bottle(x, y, .6, swap="makers-bottle-sm")}</g>'
                  for k, (x, y), t in sorted(zip(range(len(slots)), slots, starts), key=lambda st: st[1][1]))   # back row first; "late" = still in transit in the still frame
    body = (wash('<rect x="150" y="176" width="190" height="10" fill="#5a4636"/>'
                 f'<path d="M278 186 L278 132 Q278 124 286 124 L312 124 Q318 124 322 132 L334 150 Q340 152 340 160 L340 186Z" fill="{color}"/>'
                 '<path d="M286 132 L311 132 L319 150 L286 150Z" fill="#e7f1fb"/>')
            + lines('<path d="M278 186 L278 132 Q278 124 286 124 L312 124 Q318 124 322 132 L334 150 Q340 152 340 160 L340 186Z"/>'
                    '<path d="M286 132 L311 132 L319 150 L286 150Z" stroke-width="1.8"/><path d="M298 156 h8" stroke-width="2"/><rect x="338" y="168" width="6" height="12" rx="1.5" stroke-width="1.8"/>'
                    '<path d="M150 176 H278 M150 186 H340"/>', boil=False, width=2.2))
    rails = (wash(f'<rect x="150" y="164" width="128" height="14" fill="{color}"/>')
             + lines('<rect x="150" y="164" width="128" height="14"/><path d="M152 178 V136 M194 164 V136 M236 164 V136 M276 178 V136 M150 137 H278" stroke-width="2.2"/>', boil=False, width=2.2))
    wheel = lambda cx: (f'<g class="wheel" style="transform-origin:{cx}px 192px;animation-delay:{delay}s">'
                        + wash(f'<circle cx="{cx}" cy="192" r="14" fill="#3b2233"/><circle cx="{cx}" cy="192" r="6" fill="#e6d3bd"/>')
                        + lines(f'<circle cx="{cx}" cy="192" r="14"/><path d="M{cx - 6} 192 H{cx + 6} M{cx} 186 V198" stroke="#3b2233" stroke-width="1.6"/>', boil=False, width=2)
                        + '</g>')
    return f'<g class="truck {cls}" style="animation-delay:{delay}s">{body}{bed}{rails}{wheel(182)}{wheel(312)}</g>'


fleet = truck('#6f86a6', 'truck-a', 0) + truck('#e6b264', 'truck-b', -8)
moving = ''.join(f'<g class="convey{" p1" if k == 8 else " p2" if k == 10 else ""}" style="--dx:{f(x - X0)}px;--dy:{f(y - Y0)}px;animation-delay:{f(t - 8)}s">'
                 f'{generic_bottle(X0, Y0, .6, swap="makers-bottle-sm")}</g>'
                 for k, ((x, y), t) in enumerate(zip(slots, starts)))
puffs = ''.join(wash(f'<path d="{cloud(x, y, rx, ry, 7)}" fill="#fffaf1"/>') + lines(f'<path d="{cloud(x, y, rx, ry, 7)}"/>', boil=False, width=1.6, color='#b9a3c8')
                for x, y, rx, ry in ((214, 44, 22, 11), (330, 70, 17, 9)))
save('trucks', sky + puffs + plant + waiting + belt + ground() + fleet + moving,
     "Bottle after bottle of Maker's Mark rolls out the distillery's shipping door and onto a waiting truck. The full truck drives off, the next one backs in, and the loading starts all over again")

print('scenes:', ', '.join(OUT))
