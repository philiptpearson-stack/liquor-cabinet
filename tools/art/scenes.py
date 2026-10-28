"""Door 1 (The Founder's Gamble) scenes, the Maker's cast symbols, and the kit's generic icons."""
import math, pathlib
from art import *

REPO = pathlib.Path('/home/claude/liquor-cabinet')
D1 = REPO / 'src/pages/makers-mark/founders-gamble/scenes'
D1.mkdir(parents=True, exist_ok=True)
OUT = {}


def save(name, inner, label):
    OUT[name] = svg(inner, label)
    (D1 / f'{name}.svg').write_text(OUT[name] + '\n')


# ---------------------------------------------------------------- 1. Meet Bill Sr.
hills = wash('<path d="M0 172 Q70 146 160 162 T300 150 T400 158 L400 206 L0 206Z" fill="#c8d5b0" opacity=".6"/>')
sun = wash('<circle cx="336" cy="56" r="24" fill="#f2c776"/>')
shed = (wash('<rect x="286" y="156" width="66" height="44" fill="#d8b48f"/><path d="M280 158 L319 132 L358 158Z" fill="#b08463"/><rect x="336" y="126" width="9" height="22" fill="#b08463"/>')
        + lines('<rect x="286" y="156" width="66" height="44"/><path d="M280 158 L319 132 L358 158Z"/><rect x="336" y="126" width="9" height="22"/><path d="M312 200 V180 H326 V200"/>', boil=False, width=2))
b = bill(arm_r=[(22, -113), (36, -128), (40, -152)], arm_cls=('', 'wave-arm'))
m = margie(arm_l=[(-19, -108), (-33, -124), (-38, -148)], arm_cls=('wave-arm d2', ''))
hi = '<text class="letter pop" x="242" y="64" font-size="32" style="transform-origin:254px 54px">Hi!</text>'
hello_m = '<text class="letter pop d2" x="48" y="36" font-size="22" text-anchor="middle" style="transform-origin:48px 28px">Hello!</text>'
save('hello', sun + hills + shed + ground() + place(m, 78, 206, 1.0) + place(b, 158, 206, 1.05) + hi + hello_m,
     'Bill Samuels Sr., in a fedora and round glasses, and his wife Margie, in a polka-dot dress and pearls, wave hello')

# ---------------------------------------------------------------- 2. Padlocking the old distillery
bld = wash('<path d="M14 92 L104 50 L194 92Z" fill="#9b7663"/><rect x="148" y="44" width="16" height="34" fill="#9b7663"/>'
           '<rect x="22" y="90" width="164" height="116" fill="#c99b72"/><rect x="50" y="100" width="108" height="24" fill="#fbf3e3"/>'
           '<rect x="84" y="140" width="40" height="66" fill="#7a5f4a"/><rect x="34" y="134" width="34" height="30" fill="#e9d9c2"/><rect x="140" y="134" width="34" height="30" fill="#e9d9c2"/>')
bld += lines('<path d="M14 92 L104 50 L194 92"/><rect x="148" y="44" width="16" height="34"/><rect x="22" y="90" width="164" height="116"/>'
             '<rect x="50" y="100" width="108" height="24"/><rect x="84" y="140" width="40" height="66"/>'
             '<rect x="34" y="134" width="34" height="30"/><rect x="140" y="134" width="34" height="30"/>'
             '<path d="M30 138 L72 160 M30 160 L72 138 M136 138 L178 160 M136 160 L178 138" stroke-width="4" stroke="#7a5f4a"/>'
             '<path d="M40 104 h6 M40 116 h4 M164 106 h6 M168 118 h4 M30 186 h8 M140 190 h10 M46 196 h6" stroke-width="1.6"/>', boil=False)
bld += '<text class="letter" x="104" y="117" font-size="13" text-anchor="middle">T.W. SAMUELS</text>'
chain = lines('<path d="M86 166 q6 6 12 0 q6 -6 12 0 q6 6 12 0" stroke="#8a8f96" stroke-width="3"/>', boil=False)
lock = ('<g class="lock-swing" style="transform-origin:104px 164px">'
        + wash('<rect x="97" y="172" width="15" height="13" rx="2" fill="#e6b264"/>')
        + lines('<path d="M99.5 173 v-4 a5 5 0 0 1 10 0 v4"/><rect x="97" y="172" width="15" height="13" rx="2"/><path d="M104.5 177 v4" stroke-width="2"/>', boil=False)
        + '</g>')
# Bill walks away crying: eyes screwed shut, mouth open in a wail, tears dropping from both eyes. "sob!"
sad = bill(mood='wail', eyes='squeeze', head_tilt=9)
drop = lambda x, y, s=1.0: f'<path d="M{x} {y - 4 * s} q{-3.2 * s} {4.4 * s} 0 {7 * s} q{3.2 * s} {-2.6 * s} 0 {-7 * s}Z" fill="#8ecae6" stroke="#5b8aa6" stroke-width="1.1"/>'
# just tears falling straight down from under both lenses, fast
spray = ''.join(f'<g class="tear-fall" style="animation-delay:{d}s">{drop(x, -136, 1.25)}</g>' for x, d in ((-8, 0), (8, -.22), (-8, -.44), (8, -.6)))
tears = f'<g transform="rotate(9 0 -125)">{spray}</g>'
sob = '<text class="letter pop" x="-44" y="-164" font-size="19" text-anchor="middle" style="transform-origin:-44px -170px">sob!</text>'
walker = f'<g class="walk-away"><g class="bob">{sad}{tears}{sob}</g></g>'
save('padlock', bld + chain + lock + ground() + place(walker, 228, 206, .92),
     'Bill padlocks the old T.W. Samuels distillery and walks away sobbing, tears falling down his face')

# ---------------------------------------------------------------- 3. Eureka
# the classic thinker: one arm folded across the belly, the other elbow resting on it, hand at the chin
think = bill(arm_r=[(22, -113), (15, -87), (8, -121)], arm_l=[(-22, -113), (-21, -88), (13, -83)], front_l=True, mood='o')
bulb = ('<g class="bulb">'
        + '<g class="bulb-rays">' + lines('<path d="M72 14 l-8 -5 M68 28 h-10 M72 42 l-8 5 M118 14 l8 -5 M122 28 h10 M118 42 l8 5 M95 3 v-3" stroke="#e6a43c" stroke-width="3"/>', boil=False) + '</g>'
        + wash('<circle cx="95" cy="25" r="13" fill="#fbe39b"/><rect x="89" y="37" width="12" height="9" rx="2" fill="#a9a29a"/>')
        + lines('<circle cx="95" cy="25" r="13"/><rect x="89" y="37" width="12" height="9" rx="2"/><path d="M90.5 28 q2.2 -5 4.5 0 q2.2 -5 4.5 0" stroke-width="1.8"/>', boil=False)
        + '</g>')
cloud = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
                [(214, 70, 30), (250, 46, 34), (300, 40, 34), (346, 56, 32), (366, 98, 30), (338, 132, 30), (290, 142, 32), (240, 134, 30), (204, 106, 28), (290, 90, 54)])
bubble = ('<g class="float">' + wash(f'<g fill="#fffaf1">{cloud}</g>')
          + lines('<path d="M190 88 Q182 60 210 44 Q222 16 256 14 Q284 2 310 10 Q342 8 356 30 Q384 44 380 76 Q398 104 372 126 Q366 160 330 160 Q300 176 270 170 Q236 170 220 156 Q188 148 186 118 Q176 102 190 88Z"/>', boil=False)
          + '<text class="letter" x="288" y="56" font-size="14.5" text-anchor="middle">Make my bourbon softer?</text>'
          + '<text class="letter" x="288" y="78" font-size="14.5" text-anchor="middle">Sweeter?</text>'
          + '<text class="letter" x="288" y="102" font-size="14.5" text-anchor="middle">Make my bourbon...</text>'
          + '<text class="letter wiggle-word" x="284" y="138" font-size="22" text-anchor="middle" style="transform-origin:284px 130px">WHEATED??</text></g>')
trail = wash('<circle cx="126" cy="104" r="4" fill="#fffaf1"/><circle cx="142" cy="96" r="6" fill="#fffaf1"/><circle cx="162" cy="88" r="8" fill="#fffaf1"/>') + \
    lines('<circle cx="126" cy="104" r="4"/><circle cx="142" cy="96" r="6"/><circle cx="162" cy="88" r="8"/>', boil=False, width=2)
wheat = ''
for i, (x, h) in enumerate([(24, 44), (36, 56), (48, 40), (196, 30), (208, 36), (220, 28)]):
    grains = ''.join(f'<ellipse cx="{x + (3 if k % 2 else -3)}" cy="{206 - h + k * 6}" rx="2.6" ry="4.6" transform="rotate({20 if k % 2 else -20} {x} {206 - h + k * 6})"/>' for k in range(4))
    wheat += lines(f'<path d="M{x} 206 V{206 - h}"/>' + grains, boil=False, color='#b9792c', width=2)
save('eureka', ground() + wheat + place(think, 95, 206, .8) + bulb + trail + bubble,
     'A lightbulb goes on over Bill, chin in hand. His thought bubble says: Make my bourbon softer? Sweeter? Make my bourbon... WHEATED??')


# ---------------------------------------------------------------- the liquor store shelves (scenes 4 and 6 share them)
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


# ---------------------------------------------------------------- 4. Bourbon's reputation problem: the bottom shelf
top_row = (decanter(180, TOP, color='#c98a3c', label='Scotch') + decanter(214, TOP, w=22, h=36, color='#a0522d')
           + decanter(250, TOP, color='#7f9a6c', label='Scotch') + decanter(290, TOP, w=22, h=38, color='#c98a3c')
           + decanter(328, TOP, color='#a0522d', label='Scotch') + decanter(364, TOP, w=22, h=36, color='#7f9a6c'))
top_tag = shelf_label(182, TOP, '$$$', size=12.5) + shelf_label(252, TOP, '$$$', size=12.5, tilt=3)
shine = sparkle(196, 40, 6, 'twinkle') + sparkle(272, 36, 7.5, 'twinkle d2') + sparkle(346, 42, 6, 'twinkle d3')
lady = place(posh(arm_r=[(19, -106), (33, -126), (48, -142)], arm_cls='reach-up'), 122, 206, .95)
hmph = '<text class="letter pop" x="66" y="56" font-size="20" text-anchor="middle" style="transform-origin:66px 50px">Hmph!</text>'
save('reputation', shelf_unit() + ground() + top_row + top_tag + shine + middle_row() + bottom_shelf() + lady + hmph,
     'At the liquor store, a hoity-toity lady reaches for the fancy imported Scotch on the top shelf. '
     'Down on the bottom shelf, under a cobweb, sit the dusty bourbon jugs, priced in cents, with a fly buzzing around them')

# ---------------------------------------------------------------- 5. The pour, the sip, the grin
barrel = wash('<path d="M164 150 Q156 178 164 206 L236 206 Q244 178 236 150Z" fill="#b08463"/><ellipse cx="200" cy="150" rx="37" ry="8" fill="#c99b72"/>')
barrel += lines('<path d="M164 150 Q156 178 164 206 M236 150 Q244 178 236 206"/><ellipse cx="200" cy="150" rx="37" ry="8"/>'
                '<path d="M162 166 Q200 172 238 166 M161 190 Q200 196 239 190" stroke-width="3.4" stroke="#5a4636"/><path d="M186 156 Q184 180 186 205 M214 156 Q216 180 214 205" stroke-width="1.6"/>', boil=False)
pourer = bill(arm_r=[(22, -113), (44, -106), (58, -114)])
bottle = ('<g transform="translate(172 101) rotate(108) translate(0 30) scale(.78)">'
          + swappable('makers-bottle-sm', wash('<path d="M-13 0 L-13 -38 Q-13 -46 -6 -50 L-5 -62 L5 -62 L6 -50 Q13 -46 13 -38 L13 0Z" fill="#c98a3c"/><rect x="-10" y="-30" width="20" height="16" rx="2" fill="#fbf3e3"/>')
          + lines('<path d="M-13 0 L-13 -38 Q-13 -46 -6 -50 L-5 -62 L5 -62 L6 -50 Q13 -46 13 -38 L13 0Z"/><rect x="-10" y="-30" width="20" height="16" rx="2" stroke-width="1.8"/>', boil=False))
          + '</g>')
stream = '<path class="stream" d="M195 109 Q221 105 233 122" fill="none" stroke="#d99a3c" stroke-width="4" stroke-linecap="round"/>'
glass_l = ('<g>' + wash('<path d="M-6 -10 L6 -10 L5 4 L-5 4Z" fill="#f6e6c8"/><path class="fill" d="M-5.4 -2 L5.4 -2 L5 4 L-5 4Z" fill="#d99a3c"/>')
           + lines('<path d="M-6 -10 L6 -10 L5 4 L-5 4Z" stroke-width="1.8"/>', boil=False) + '</g>')
# pose to pose: (a) glass out for the pour, (b) head back, glass at his lips, (c) glass down, big grin
glass_out = f'<g transform="translate(-50 -92)">{glass_l}</g>'
glass_up = f'<g transform="translate(-13 -133) rotate(-52)">{glass_l}</g>'
wait = everyman(mood='flat', arm_l=[(-21, -109), (-38, -92), (-50, -84)], holding_l=glass_out, parts=True)
sip = everyman(mood='smile', eyes='closed', head_tilt=14, arm_l=[(-21, -109), (-36, -100), (-18, -126)], holding_l=glass_up, parts=True)
grin = everyman(mood='grin', eyes='happy', parts=True)
cust = (wait['body'] + '<g class="pose-a">' + wait['left'] + '</g>' + '<g class="pose-b">' + sip['left'] + '</g>'
        + '<g class="head-a">' + wait['head'] + '</g>' + '<g class="pose-b">' + sip['head'] + '</g>' + '<g class="pose-c">' + grin['head'] + '</g>' + wait['right'])
sip_word = '<text class="letter pose-b" x="236" y="66" font-size="17" text-anchor="middle">sip...</text>'
mmm = '<g class="pose-c"><text class="letter pop" x="338" y="62" font-size="24" text-anchor="middle" style="transform-origin:338px 54px">Mmm!</text></g>'
spark = '<g class="pose-c">' + sparkle(306, 84, 6, 'twinkle') + sparkle(372, 86, 5, 'twinkle d2') + sparkle(296, 50, 4.5, 'twinkle d3') + '</g>'
save('pour', ground() + barrel + place(pourer, 118, 206, .92) + bottle + stream + place(cust, 288, 206, .92) + sip_word + mmm + spark,
     'Bill pours a glass of Maker\'s Mark over a whiskey barrel for a customer. The customer tips his head back, sips, and grins: Mmm!')

# ---------------------------------------------------------------- 6. The liquor store: reaching for the Scotch... wait, Maker's is up here too?
store_top = (decanter(180, TOP, color='#c98a3c', label='Scotch') + generic_bottle(217, TOP, .68, swap='makers-bottle-sm')
             + decanter(254, TOP, w=22, h=38, color='#a0522d') + decanter(290, TOP, color='#7f9a6c', label='Scotch')
             + decanter(328, TOP, w=22, h=36, color='#c98a3c') + decanter(364, TOP, color='#a0522d', label='Scotch'))
store_tags = shelf_label(178, TOP, '$$$', size=12) + shelf_label(218, TOP, '$$$', size=12, tilt=3)
wink = sparkle(232, 40, 8, 'twinkle') + sparkle(202, 46, 4.5, 'twinkle d2')
reacher = everyman(mood='o', eyes='side', arm_r=[(21, -109), (35, -126), (48, -142)], arm_cls=('', 'reach'))
think_bub = ('<g class="float">' + wash('<path d="M10 30 Q6 8 32 8 Q48 -2 70 6 Q92 -2 108 10 Q128 12 124 32 Q132 50 110 54 Q96 66 70 58 Q46 66 30 56 Q4 54 10 30Z" fill="#fffaf1"/>')
             + lines('<path d="M10 30 Q6 8 32 8 Q48 -2 70 6 Q92 -2 108 10 Q128 12 124 32 Q132 50 110 54 Q96 66 70 58 Q46 66 30 56 Q4 54 10 30Z"/>', boil=False)
             + '<text class="letter" x="66" y="28" font-size="11.5" text-anchor="middle">"It tastes expensive...</text>'
             + '<text class="letter" x="66" y="46" font-size="14" text-anchor="middle">...and is."</text></g>')
think_trail = wash('<circle cx="112" cy="66" r="4.5" fill="#fffaf1"/><circle cx="120" cy="74" r="3" fill="#fffaf1"/>') + lines('<circle cx="112" cy="66" r="4.5"/><circle cx="120" cy="74" r="3"/>', boil=False, width=1.8)
bang = '<text class="letter pop" x="160" y="58" font-size="26" style="transform-origin:166px 50px">!</text>'
save('store', shelf_unit() + ground() + store_top + store_tags + wink + middle_row() + bottom_shelf()
     + place(reacher, 132, 206, .92) + think_trail + think_bub + bang,
     'At the liquor store, the customer reaches for the Scotch on the top shelf and spots Maker\'s Mark sitting right next to it, '
     'priced the same. He remembers the ad: It tastes expensive... and is. Down on the bottom shelf, the cheap bourbon jugs gather dust')

# ---------------------------------------------------------------- 7. The trick (Bill Jr. and the reporter)
door = wash('<rect x="0" y="40" width="400" height="166" fill="#ead8c6" opacity=".55"/><rect x="18" y="62" width="74" height="144" fill="#7a5f4a"/><rect x="26" y="70" width="58" height="136" fill="#f6e6c8"/>')
door += lines('<rect x="18" y="62" width="74" height="144"/><rect x="26" y="70" width="58" height="136" stroke-width="1.8"/>', boil=False)
stack = wash('<ellipse cx="340" cy="126" rx="28" ry="6" fill="#c99b72"/><path d="M312 126 Q306 150 312 176 L368 176 Q374 150 368 126Z" fill="#b08463"/>') + \
    lines('<ellipse cx="340" cy="126" rx="28" ry="6"/><path d="M312 126 Q306 150 312 176 M368 126 Q374 150 368 176"/><path d="M310 140 Q340 146 370 140 M310 162 Q340 168 370 162" stroke-width="3" stroke="#5a4636"/>', boil=False)
stack += wash('<path d="M296 176 Q290 192 296 206 L384 206 Q390 192 384 176Z" fill="#b08463"/>') + lines('<path d="M296 176 Q290 192 296 206 M384 176 Q390 192 384 206 M294 190 Q340 196 386 190" />', boil=False)
sr = bill(mood='smile', arm_r=[(22, -113), (36, -128), (40, -152)], arm_cls=('', 'wave-arm'))
front = '<path d="M286 150 Q276 178 286 206 L378 206 Q388 178 378 150 Q332 140 286 150Z" fill="#b08463"/>' + wash('<ellipse cx="332" cy="150" rx="46" ry="9" fill="#c99b72"/><path d="M286 150 Q276 178 286 206 L378 206 Q388 178 378 150Z" fill="#b08463"/>') + \
    lines('<ellipse cx="332" cy="150" rx="46" ry="9"/><path d="M286 150 Q276 178 286 206 M378 150 Q388 178 378 206"/><path d="M283 166 Q332 174 381 166 M282 190 Q332 198 382 190" stroke-width="3.4" stroke="#5a4636"/><path d="M314 158 Q312 182 314 205 M350 158 Q352 182 350 205" stroke-width="1.6"/>', boil=False)
yikes = '<text class="letter pop" x="350" y="58" font-size="24" style="transform-origin:362px 50px">Hi!</text>'
pad = wash('<rect x="22" y="-112" width="16" height="20" rx="2" fill="#fffaf1"/>') + lines('<rect x="22" y="-112" width="16" height="20" rx="2" stroke-width="1.6"/><path d="M25 -106 h10 M25 -101 h10 M25 -96 h7" stroke-width="1.2"/>', boil=False)
reporter = everyman(mood='smile', top='#d8c3a5', pants='#6f6760', tie='#5b8aa6', hat='fedora', press=True,
                    arm_r=[(21, -109), (34, -98), (30, -104)], holding_r=pad)
junior = everyman(mood='grin', eyes='happy', top='#5f6f8c', pants='#8c7a6b', tie='#8b3a63', hat='hair',
                  arm_r=[(21, -109), (40, -100), (58, -104)])
push = f'<g class="nudge">{place(junior, 70, 206, .9)}{place(reporter, 150, 206, .9)}</g>'
save('trick', door + ground() + place(sr, 332, 206, .8) + front + push + yikes,
     "Bill Jr. nudges a reporter with a notepad through the distillery door while Bill Sr. looks up from a barrel and waves hi")

# ---------------------------------------------------------------- 8. Kentucky, one county at a time
KY = [(-89.42, 36.5), (-89.15, 36.97), (-88.6, 37.08), (-88.1, 37.45), (-87.6, 37.85), (-87.1, 37.78), (-86.6, 37.92), (-86.2, 38.0),
      (-85.76, 38.27), (-85.4, 38.7), (-85.18, 38.68), (-84.8, 38.79), (-84.5, 39.1), (-84.2, 38.86), (-83.7, 38.64), (-83.3, 38.6),
      (-83.0, 38.73), (-82.6, 38.47), (-82.6, 38.17), (-82.4, 37.9), (-81.97, 37.54), (-82.6, 37.2), (-83.1, 36.9), (-83.68, 36.6),
      (-85.5, 36.6), (-86.5, 36.64), (-87.8, 36.64), (-88.07, 36.68), (-88.05, 36.5)]
def proj(lon, lat):
    return (20 + (lon + 89.6) * 0.8 * 58, 26 + (39.25 - lat) * 58)
poly = [proj(*p) for p in KY]
d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in poly) + 'Z'
lx, ly = proj(-85.40, 37.63)
def inside(x, y):
    c = False
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c
import random
random.seed(11)
dots = []
while len(dots) < 26:
    x, y = random.uniform(30, 370), random.uniform(40, 200)
    if inside(x, y) and all(math.hypot(x - a, y - b) > 22 for a, b in dots + [(lx, ly)]) and not (lx - 70 < x < lx - 6 and ly - 8 < y < ly + 24):
        dots.append((x, y))
dots.sort(key=lambda p: math.hypot(p[0] - lx, p[1] - ly))
drop = lambda x, y, cls, delay: (f'<path class="{cls}" style="animation-delay:{delay:.2f}s;transform-origin:{x:.1f}px {y:.1f}px" '
                                 f'd="M{x:.1f} {y - 7:.1f} Q{x + 5:.1f} {y - 1:.1f} {x + 4:.1f} {y + 2:.1f} A4.2 4.2 0 1 1 {x - 4:.1f} {y + 2:.1f} Q{x - 5:.1f} {y - 1:.1f} {x:.1f} {y - 7:.1f}Z" '
                                 f'fill="#c0392b" stroke="{INK}" stroke-width="1.3"/>')
ky = wash(f'<path d="{d}" fill="#c8d5b0"/>') + lines(f'<path d="{d}"/>', boil=False, width=2.4)
ky += lines('<path d="' + 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in poly[1:20]) + '" />', boil=False, width=3, color='#8ecae6')
spread = drop(lx, ly, 'drip home', 0) + ''.join(drop(x, y, 'drip', .5 + i * .18) for i, (x, y) in enumerate(dots))
label = f'<text class="letter" x="{lx - 9:.1f}" y="{ly + 17:.1f}" font-size="14" text-anchor="end">Loretto</text>'
save('kentucky', ky + spread + label,
     'A crayon map of Kentucky. Little red drips spread out from Loretto, one county at a time')

# ---------------------------------------------------------------- 9. THWAP
paper = ('<g class="paper-drop">' + wash('<path d="M150 150 L250 136 L262 196 L160 212Z" fill="#f4efe3"/>')
         + lines('<path d="M150 150 L250 136 L262 196 L160 212Z"/><path d="M200 143 L210 204" stroke-width="1.6"/>'
                 '<path d="M160 160 L196 155 M162 168 L196 163 M164 176 L198 171 M166 184 L198 180 M168 192 L199 188 M214 160 L246 156 M216 168 L248 164 M218 176 L250 172 M220 184 L251 180" stroke-width="1.4" stroke="#8a6a78"/>', boil=False)
         + '<text class="letter" x="226" y="152" font-size="13" text-anchor="middle" transform="rotate(-8 226 152)">1980</text></g>')
burst_pts = []
for k in range(22):
    a = math.pi * k / 11
    r = 62 if k % 2 == 0 else 40
    burst_pts.append((205 + math.cos(a) * r * 1.35, 92 + math.sin(a) * r * .8))
bd = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in burst_pts) + 'Z'
burst = ('<g class="burst" style="transform-origin:205px 92px">' + wash(f'<path d="{bd}" fill="#fbe39b"/>') + lines(f'<path d="{bd}"/>', boil=False, width=2.4)
         + '<text class="letter" x="205" y="102" font-size="27" text-anchor="middle">THWAP!</text></g>')
dust = lines('<path d="M128 206 q-10 -10 -22 -6 M282 204 q10 -10 24 -5 M140 214 q-14 0 -22 6 M270 214 q14 0 22 6" stroke-width="2"/>', boil=False, extra=' class="dust"')
save('thwap', ground() + burst + paper + dust,
     'A newspaper from 1980 drops from the sky and lands with a THWAP!')

# ---------------------------------------------------------------- cast symbols (door icons) and kit icons
CAST = REPO / 'src/pages/makers-mark/cast.svg'
CAST.write_text(
    '    <!-- Maker\'s Mark cast: door icons -->\n'
    f'    <symbol id="bill-icon" viewBox="-38 -182 76 76">{bill()}</symbol>\n'
    f'    <symbol id="margie-icon" viewBox="-38 -80 76 76">{margie_bust()}</symbol>\n')
newspaper_icon = (wash('<path d="M14 30 L98 20 L106 92 L22 102Z" fill="#f4efe3"/>')
                  + lines('<path d="M14 30 L98 20 L106 92 L22 102Z"/><path d="M60 25 L64 97" stroke-width="1.6"/>'
                          '<path d="M24 42 L54 38 M25 52 L55 48 M26 62 L56 58 M27 72 L57 68 M28 82 L58 78 M70 36 L96 33 M71 46 L97 43 M72 56 L98 53 M73 66 L99 63 M74 76 L100 73 M75 86 L101 83" stroke-width="1.5" stroke="#8a6a78"/>', boil=False))
bottle_icon = generic_bottle(60, 108, 1.32)
# The Bartender's Perspective: a bartender in a vest and bow tie, shaker up by his ear
shaker = (wash('<path d="M24 -150 L38 -150 L36 -172 L26 -172Z" fill="#c9c3b8"/><path d="M26.5 -172 L35.5 -172 L34 -181 L28 -181Z" fill="#a9a29a"/><rect x="29" y="-185" width="4" height="4" rx="1" fill="#a9a29a"/>')
          + lines('<path d="M24 -150 L38 -150 L36 -172 L26 -172Z"/><path d="M26.5 -172 L35.5 -172 L34 -181 L28 -181Z" stroke-width="2"/><rect x="29" y="-185" width="4" height="4" rx="1" stroke-width="1.6"/>'
                  '<path d="M27 -164 h8" stroke="#fffaf1" stroke-width="1.6"/>', boil=False)
          + lines('<path d="M44 -178 q4 3 0 6 M47 -168 q4 3 0 6 M18 -180 q-4 3 0 6" stroke="#8a6a78" stroke-width="1.8"/>', boil=False))
barkeep = everyman(mood='smile', eyes='happy', top='#4a3e4f', tie='#c0583c', hat='hair', hair='#3b2a22',
                   arm_r=[(21, -109), (38, -124), (31, -146)], holding_r=shaker)
bartender_icon = f'<g>{barkeep}</g>'
kit_icons = ('    <!-- Generic door icons -->\n'
             f'    <symbol id="newspaper-icon" viewBox="0 0 120 120">{newspaper_icon}</symbol>\n'
             f'    <symbol id="bottle-icon" viewBox="0 0 120 120">{bottle_icon}</symbol>\n'
             f'    <symbol id="bartender-icon" viewBox="-40 -190 90 90">{bartender_icon}</symbol>\n')
DEFS = REPO / 'src/kit/defs.svg'
defs = DEFS.read_text()
import re
defs = re.sub(r'    <!-- Generic door icons -->\n.*?(?=  </defs>)', '', defs, flags=re.S)
defs = defs.replace('  </defs>', kit_icons + '  </defs>')
DEFS.write_text(defs)
print('scenes:', ', '.join(OUT))
