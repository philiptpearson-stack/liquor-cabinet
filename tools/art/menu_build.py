"""The Cocktail Menu: a drink's step-by-step build scene, made from its list of steps.

Each step is (words under the drawing, [actions]). Actions, in order:
  ('pour', ingredient, oz)   bottle or jigger, into the shaker (before a strain) or the glass
  ('dash', ingredient, n)    ('egg',)   ('mint',)   ('salt',)
  ('ice', 'mix' | 'glass')   ('dry',) dry shake   ('shake',)   ('stir',)   ('strain',)
  ('top', ingredient, oz)    ('float', ingredient, oz)   ('sink', ingredient, oz)   ('garnish',)
The still frame (reduced motion, and what the poster shows) is the finished drink; everything
that moves is hidden there. All motion is CSS keyframes, timed in seconds and written as percents.
"""
from menu_art import *

BAR = 196
MX, MRIM, MBOT = 190, 96, 189                      # the mixing glass: rim centre, inside bottom
G_MIX = 'M160 96 L220 96 L214 196 L166 196Z'
G_MIX_IN = 'M162.4 99 L217.6 99 L212.3 189 L167.7 189Z'
TIN = 'M154 114 L226 114 L220 58 L160 58Z'
BUILD_SCALE = {'highball': 1.2, 'rocks': 1.38, 'coupe': 1.5, 'flute': 1.0, 'martini': 1.3}
DUR = {'pour': 1.2, 'jigger': 1.15, 'dash': 1.2, 'egg': 1.3, 'mint': 1.0, 'salt': 1.0, 'ice': 1.0, 'ice-glass': 1.5,
       'dry': 2.4, 'shake': 2.9, 'stir': 2.8, 'strain': 2.5, 'top': 1.9, 'float': 1.9, 'sink': 1.9, 'garnish': 1.3}
LEAD, HOLD = .5, 2.8
VIEW = '104 14 240 204'


def visible(color):
    """A clear spirit still has to show up as it pours."""
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return '#d5e4e8' if (r + g + b) / 3 > 228 else color


def oz_text(q):
    w, r = int(q), round((q - int(q)) * 4)
    frac = ['', '¼', '½', '¾'][r]
    return (f'{w} {frac}' if w and frac else (str(w) if w else frac)) + ' oz'


class Build:
    def __init__(self, d):
        self.d, self.slug = d, d['slug']
        self.kind = d['glass']
        self.g = GLASS[self.kind]
        self.css, self.base = [], []
        self.n = 0
        acts = []
        for i, (_, actions) in enumerate(d['steps']):
            for a in actions:
                acts.append([i] + list(a))
        self.uses_mix = any(a[1] == 'strain' for a in acts)
        self.gx, self.gs = (290, 1.0) if self.uses_mix else (224, BUILD_SCALE[self.kind])
        # timing: every action gets a slot; a step spans its actions
        t, self.steps = LEAD, []
        into = 'mix' if self.uses_mix else 'glass'
        for a in acts:
            kind = a[1]
            if kind == 'pour' and ING[a[2]][1] == 'jigger':
                dur = DUR['jigger']
            elif kind == 'ice' and a[2] == 'glass':
                dur = DUR['ice-glass'] if self.kind == 'highball' else DUR['ice']
            else:
                dur = DUR[kind]
            a.append(t)            # a[-2] = start
            a.append(t + dur)      # a[-1] = end
            a.insert(1, into if kind in ('pour', 'dash', 'egg', 'mint', 'salt', 'stir') else ('glass' if kind != 'ice' else a[2]))
            if kind == 'strain':
                into = 'glass'
            t += dur
        self.acts = acts           # [step, into, kind, *args, t0, t1]
        self.T = round(t + HOLD, 2)
        for i in range(len(d['steps'])):
            mine = [a for a in acts if a[0] == i]
            self.steps.append((mine[0][-2], mine[-1][-1]))
        self.strain_t = next((a[-2] for a in acts if a[2] == 'strain'), None)
        self.garnish_t = next((a[-2] for a in acts if a[2] == 'garnish'), self.T - HOLD)

    # ------------------------------------------------------------ helpers
    def cls(self, stem):
        self.n += 1
        return f'{stem}{self.n}'

    def pc(self, t):
        return max(0.0, min(100.0, round(t / self.T * 100, 2)))

    def emit(self, cls, states, base='opacity:0'):
        """states: [(seconds, {prop: value})], each carrying forward what it doesn't say."""
        keys = []
        for _, st in states:
            keys += [k for k in st if k not in keys]
        first = {k: next(st[k] for _, st in states if k in st) for k in keys}
        cur, stops, last = dict(first), [], -1
        for t, st in states:
            cur.update(st)
            p = self.pc(t)
            if p <= last:
                p = round(last + .01, 2)
            stops.append((p, dict(cur)))
            last = p
        if stops[0][0] > 0:
            stops.insert(0, (0, dict(stops[0][1])))
        if stops[-1][0] < 100:
            stops.append((100, dict(stops[-1][1])))
        body = ''.join(f'{p:g}%{{' + ';'.join(f'{k}:{v}' for k, v in s.items()) + '}' for p, s in stops)
        self.css.append(f'.{cls}{{animation:{cls} {self.T:g}s linear infinite}}@keyframes {cls}{{{body}}}')
        if base:
            self.base.append(f'.{cls}')

    def window(self, cls, t0, t1, fade=.12, base='opacity:0'):
        self.emit(cls, [(0, {'opacity': 0}), (max(t0 - fade, 0), {'opacity': 0}), (t0, {'opacity': 1}), (t1, {'opacity': 1}), (t1 + fade, {'opacity': 0})], base)

    def G(self, x, y):
        """glass-local to stage"""
        return self.gx + x * self.gs, BAR + y * self.gs

    def target(self, into):
        if into == 'mix':
            return MX, MRIM, MBOT
        rx, ry = self.G(0, self.g['rim'][0])
        return rx, ry, self.G(0, self.g['bottom'])[1]

    # ------------------------------------------------------------ the scene
    def scene(self):
        d, acts = self.d, self.acts
        layers_mix, actors, captions = [], [], []
        mix_vol = sum(a[4] for a in acts if a[1] == 'mix' and a[2] == 'pour') + (.8 if any(a[2] == 'egg' for a in acts) else 0)
        mix_t = next((a[-2] + .5 for a in acts if a[1] == 'mix' and a[2] in ('dry', 'shake', 'stir')), None)
        if mix_t is None:
            mix_t = next((a[-2] + .5 for a in acts if a[2] in ('dry', 'shake', 'stir')), None)
        # ---------- glass bands (bottom up), the float on top, the sink at the bottom
        bands = []
        for a in acts:
            k = a[2]
            if a[1] == 'glass' and k == 'pour':
                bands.append(('pour', a[4] if a[4] else .25, ING[a[3]][2], a))
            elif k == 'strain':
                bands.append(('strain', mix_vol * 1.2, d.get('base', d['color']), a))
            elif k in ('top', 'float', 'sink'):
                bands.append((k, a[4], ING[a[3]][2], a))
        g = self.g
        top_level, bottom = d.get('level', g['top']), g['bottom']
        span = bottom - top_level
        stack = [b for b in bands if b[0] != 'sink']
        total = sum(b[1] for b in stack) or 1
        y, geo = bottom + 1.5, []
        for b in stack:
            h = (span + 1.5) * b[1] / total
            geo.append((b, y - h, y))
            y -= h
        under = [x for x in geo if x[0][0] != 'float']
        floats = [x for x in geo if x[0][0] == 'float']
        sink = [b for b in bands if b[0] == 'sink']
        mixed_glass = len(under) > 1
        glass_mix_t = None
        if mixed_glass:
            stir_in_glass = [a for a in acts if a[1] == 'glass' and a[2] == 'stir']
            last_under = max(x[0][3][-1] for x in under)
            glass_mix_t = (stir_in_glass[-1][-2] + .8) if stir_in_glass and stir_in_glass[-1][-2] > under[-1][0][3][-2] else last_under - .2
        uid = f'{self.slug}-gl'
        under_svg, float_svg = '', ''
        for (kind, vol, color, a), y0, y1 in under + floats:
            c = self.cls('band')
            color = d['color'] if not mixed_glass and kind == 'strain' else color
            piece = f'<g class="{c}" style="transform-origin:0px {f(y1)}px"><rect x="-40" y="{f(y0 - .6)}" width="80" height="{f(y1 - y0 + .6)}" fill="{color}"/></g>'
            if kind == 'float':
                float_svg += piece    # drawn over the mixed drink, so the float stays on top
            else:
                under_svg += piece
            t0, t1 = a[-2], a[-1]
            on, off = t0 + (.45 if kind != 'strain' else .55), t1 - (.3 if kind != 'strain' else .35)
            self.emit(c, [(0, {'transform': 'scaleY(0)'}), (on, {'transform': 'scaleY(0)'}), (off, {'transform': 'scaleY(1)'})], base=None)
        overlay = ''
        if mixed_glass:
            u_top = min(y0 for _, y0, _ in under)
            c = self.cls('mixd')
            fizzy = any(a[2] == 'top' and a[3] in FIZZY for a in acts)
            overlay = (f'<g class="{c}">' + wash(f'<rect x="-40" y="{f(u_top - .6)}" width="80" height="{f(bottom + 2 - u_top)}" fill="{d["color"]}"/>')
                       + (bubbles_in(self.kind, top_level) if fizzy else '') + '</g>')
            self.emit(c, [(0, {'opacity': 0}), (glass_mix_t, {'opacity': 0}), (glass_mix_t + .5, {'opacity': 1})], base=None)
        elif any(a[2] == 'top' and a[3] in FIZZY for a in acts):
            overlay = bubbles_in(self.kind, top_level)
        sink_svg = ''
        for kind, vol, color, a in sink:
            c = self.cls('sink')
            h = span * .34
            sink_svg += (f'<g class="{c}">' + wash(f'<path d="M-40 {f(bottom + 2)} V{f(bottom - h)} q8 -5 16 0 t16 0 t16 0 t16 0 t16 0 V{f(bottom + 2)}Z" fill="{color}" opacity=".9"/>') + '</g>')
            self.emit(c, [(0, {'opacity': 0}), (a[-2] + .7, {'opacity': 0}), (a[-1] - .2, {'opacity': 1})], base=None)
        # ice in the glass
        ice_svg = ''
        ice_act = next((a for a in acts if a[2] == 'ice' and a[1] == 'glass'), None)
        if ice_act is not None or d.get('served_on_ice'):
            for k, (x, y_, w, r) in enumerate(ICE.get(self.kind, [])):
                c = self.cls('gice')
                ice_svg += f'<g class="{c}">{cube(x, y_, w, r)}</g>'
                t0 = ice_act[-2] + k * (.12 if self.kind == 'highball' else 0)
                self.emit(c, [(0, {'opacity': 0, 'transform': 'translateY(-130px)'}), (t0, {'opacity': 0, 'transform': 'translateY(-130px)'}), (t0 + .05, {'opacity': 1}),
                              (t0 + .45, {'transform': 'translateY(0)'})], base=None)
        # foam (egg white drinks): on the drink, once it's poured
        foam_svg = ''
        if d.get('foam'):
            c = self.cls('foam')
            sa = next(a for a in acts if a[2] == 'strain')
            foam_svg = f'<g class="{c}">{foam_on(self.kind)}</g>'
            self.emit(c, [(0, {'opacity': 0}), (sa[-1] - .5, {'opacity': 0}), (sa[-1] - .1, {'opacity': 1})], base=None)
        contents_c = self.cls('gc')
        self.emit(contents_c, [(0, {'opacity': 1}), (self.T - .8, {'opacity': 1}), (self.T - .25, {'opacity': 0})], base=None)
        gl = (wash(g['back']) + f'<g class="{contents_c}"><clipPath id="{uid}"><path d="{g["inner"]}"/></clipPath>'
              f'<g clip-path="url(#{uid})"><g filter="url(#wash)">{under_svg}</g>{overlay}<g filter="url(#wash)">{float_svg}</g>{sink_svg}{ice_svg}</g>{foam_svg}</g>'
              + lines(g['out'], boil=False))
        # garnish
        gc = self.cls('garn')
        gt = self.garnish_t
        garn = f'<g class="{gc}">{garnishes(d["garnish"], self.kind)}</g>'
        self.emit(gc, [(0, {'opacity': 0, 'transform': 'translateY(-60px)'}), (gt + .1, {'opacity': 0, 'transform': 'translateY(-60px)'}), (gt + .15, {'opacity': 1}),
                       (gt + .7, {'transform': 'translateY(0)'}), (self.T - .8, {'opacity': 1}), (self.T - .25, {'opacity': 0})], base=None)
        glass_svg = f'<g transform="translate({f(self.gx)} {BAR}) scale({f(self.gs)})">{gl}{garn}</g>'

        # ---------- the mixing glass and shaker tin
        mix_svg = ''
        if self.uses_mix:
            mix_svg = self.mixing_glass(acts, mix_t)
        # ---------- the actors
        for a in acts:
            actors.append(self.actor(a))
            cap = self.caption(a)
            if cap:
                c = self.cls('cap')
                captions.append(f'<text class="letter {c}" x="112" y="34" font-size="15">{cap}</text>')
                self.window(c, a[-2] + .05, a[-1] - .1)
        cheers = self.cls('cap')
        captions.append(f'<text class="letter {cheers}" x="112" y="34" font-size="16">Cheers!</text>')
        self.emit(cheers, [(0, {'opacity': 0}), (gt + .7, {'opacity': 0}), (gt + .8, {'opacity': 1}), (self.T - .6, {'opacity': 1}), (self.T - .45, {'opacity': 0})], base=None)
        # sparkles: two that always twinkle (so the scene never sits still), more for the finished drink
        rx, ry = self.G(0, g['rim'][0])
        ch = self.cls('cheer')
        cheer = f'<g class="{ch}">{sparkle(rx - 40, ry + 4, 6, "twinkle")}{sparkle(rx + 40, ry - 4, 5.5, "twinkle d2")}{sparkle(rx + 34, BAR - 40, 4.5, "twinkle d3")}</g>'
        self.window(ch, gt + .7, self.T - .5)
        always = sparkle(330, 30, 4, 'twinkle d2') + sparkle(116, 186, 3.6, 'twinkle d3')
        mat = (146, 334) if self.uses_mix else (int(self.gx - 52), int(self.gx + 52))
        bg = wash('<rect x="0" y="0" width="400" height="236" fill="#f3e6d4"/>') + countertop(196, mat)
        inner = bg + always + mix_svg + glass_svg + ''.join(actors) + cheer + ''.join(captions)
        return svg_view(inner, d['build_alt'], VIEW)

    # ------------------------------------------------------------ the mixing glass, its layers, ice, tin
    def mixing_glass(self, acts, mix_t):
        """The mixing glass: layers as they pour, a glass FULL of ice (best practice), the level rising as the
        ice melts into the drink (a good drink is about 30% water), then it tips over the glass and pours
        through its strainer."""
        d = self.d
        strain = next(a for a in acts if a[2] == 'strain')
        st0, st1 = strain[-2], strain[-1]
        gone = st1 - .1                       # after the pour, the mixing glass steps away
        shaken = any(a[2] in ('shake', 'dry') for a in acts)
        layers, y = '', MBOT + 1
        for a in acts:
            if a[1] != 'mix' or a[2] not in ('pour', 'egg', 'dash'):
                continue
            h = {'pour': 10 * (a[4] or 0), 'egg': 8, 'dash': 1.6}[a[2]]
            color = visible(ING[a[3]][2]) if a[2] != 'egg' else '#fffaf1'
            c = self.cls('ml')
            layers += f'<g class="{c}" style="transform-origin:190px {f(y)}px"><rect x="158" y="{f(y - h - .5)}" width="64" height="{f(h + .5)}" fill="{color}"/></g>'
            on = a[-2] + (.45 if a[2] == 'pour' else .5)
            off = a[-1] - .3
            self.emit(c, [(0, {'opacity': 1, 'transform': 'scaleY(0)'}), (on, {'transform': 'scaleY(0)'}), (off, {'transform': 'scaleY(1)'}),
                          (mix_t, {'opacity': 1}), (mix_t + .2, {'opacity': 0})], base=None)
            y -= h
        # dilution: the drink rises by about a third as the ice melts, during the stir (or the shake with ice)
        DIL = 1.35
        h0 = MBOT + 1 - y
        H = h0 * DIL
        dil = [a for a in acts if a[1] == 'mix' and a[2] in ('stir', 'shake')]
        d0, d1 = (dil[-1][-2] + .6, dil[-1][-1] - .5) if dil else (mix_t, mix_t + .1)
        mc = self.cls('mixed')
        mixed = f'<g class="{mc}" style="transform-origin:190px {f(MBOT + 1)}px"><rect x="158" y="{f(MBOT + 1 - H)}" width="64" height="{f(H)}" fill="{d.get("base", d["color"])}"/></g>'
        sq = f'scaleY({h0 / H:.3f})'
        self.emit(mc, [(0, {'opacity': 0, 'transform': sq}), (mix_t, {'opacity': 0}), (mix_t + .2, {'opacity': 1}), (d0, {'transform': sq}), (d1, {'transform': 'scaleY(1)'}),
                       (st0 + .6, {'transform': 'scaleY(1)'}), (st1 - .35, {'transform': 'scaleY(.12)'}), (gone, {'opacity': 1}), (gone + .05, {'opacity': 0})], base=None)
        if d.get('foam'):   # egg white whipped up on top, riding up with the level
            fc = self.cls('mfoam')
            mixed += f'<g class="{fc}"><rect x="158" y="{f(MBOT + 1 - H - 12)}" width="64" height="12.5" fill="#fffaf1"/></g>'
            lift = f'translateY({H - h0:.1f}px)'
            self.emit(fc, [(0, {'opacity': 0, 'transform': lift}), (mix_t, {'opacity': 0}), (mix_t + .2, {'opacity': 1}), (d0, {'transform': lift}), (d1, {'transform': 'translateY(0)'}),
                           (st0 + .6, {'opacity': 1}), (st1 - .35, {'opacity': 0})], base=None)
        # mint, muddled in with the rest
        mint_svg = ''
        for a in acts:
            if a[2] == 'mint':
                for k, (x, yy, r) in enumerate(((176, 182, -30), (192, 185, 20), (204, 180, 70))):
                    c = self.cls('leaf')
                    mint_svg += f'<g class="{c}">{mint_leaf(x, yy, r)}</g>'
                    t0 = a[-2] + .15 + k * .14
                    self.emit(c, [(0, {'opacity': 0, 'transform': 'translateY(-120px)'}), (t0, {'opacity': 0, 'transform': 'translateY(-120px)'}), (t0 + .05, {'opacity': 1}),
                                  (t0 + .5, {'transform': 'translateY(0)'}), (gone, {'opacity': 1}), (gone + .05, {'opacity': 0})], base=None)
        # ice: fill the mixing glass to the top, so the drink chills and dilutes properly
        ice_svg = ''
        CUBES = [(169, 171), (186, 172), (200, 170), (167, 154), (184, 155), (201, 153), (170, 137), (187, 138), (202, 136),
                 (166, 120), (183, 121), (199, 119), (176, 104), (194, 103)]
        for a in acts:
            if a[2] == 'ice' and a[1] == 'mix':
                for k, (x, yy) in enumerate(CUBES):
                    c = self.cls('mice')
                    ice_svg += (f'<g class="{c}" style="transform-origin:{x + 8.5}px {yy + 8.5}px"><rect x="{x}" y="{yy}" width="17" height="17" rx="3" fill="#eef8ff" opacity=".6" stroke="#8ecae6" stroke-width="1.6"/>'
                                f'<path d="M{x + 4} {yy + 5} h5" stroke="#fffaf1" stroke-width="1.8" stroke-linecap="round"/></g>')
                    t0 = a[-2] + .05 + k * .05
                    self.emit(c, [(0, {'opacity': 0, 'transform': 'translateY(-110px) scale(1)'}), (t0, {'opacity': 0, 'transform': 'translateY(-110px) scale(1)'}), (t0 + .05, {'opacity': 1}),
                                  (t0 + .35, {'transform': 'translateY(0px) scale(1)'}), (d0, {'transform': 'translateY(0px) scale(1)'}), (d1, {'transform': 'translateY(0px) scale(.8)'}),
                                  (gone, {'opacity': 1}), (gone + .05, {'opacity': 0})], base=None)
        clip = f'{self.slug}-mx'
        # the strainer that holds the ice back as it pours: a julep strainer for stirred drinks, a Hawthorne for shaken
        if shaken:
            strainer = lines('<path d="M160 96 H220" stroke="#a9a29a" stroke-width="3.4"/><path d="M162 100' + ' q3 3.4 6 0' * 10 + '" stroke="#8a8f96" stroke-width="1.5"/>'
                             '<path d="M160 96 L136 88" stroke="#a9a29a" stroke-width="3.4"/>', boil=False)
        else:
            strainer = lines('<path d="M162 98 Q190 111 218 98" stroke="#a9a29a" stroke-width="3.4"/><path d="M162 98 L134 84" stroke="#a9a29a" stroke-width="3"/>'
                             + ''.join(f'<circle cx="{x}" cy="{f(98 + 6.5 * (1 - ((x - 190) / 28) ** 2) - 1)}" r=".9" fill="#8a8f96"/>' for x in range(170, 214, 7)), boil=False)
        stc = self.cls('strainer')
        self.window(stc, st0 + .05, gone - .05)
        glass = (wash(f'<path d="{G_MIX}" fill="#e7f1fb" opacity=".35"/>') + f'<clipPath id="{clip}"><path d="{G_MIX_IN}"/></clipPath>'
                 + f'<g clip-path="url(#{clip})"><g filter="url(#wash)">{layers}{mixed}</g>{mint_svg}{ice_svg}</g>'
                 + lines(f'<path d="{G_MIX}" stroke-width="2.4"/><path d="M166 189 H214" stroke-width="1.6"/><path d="M167 106 L164 160" stroke="#fffaf1" stroke-width="3"/>', boil=False)
                 + f'<g class="{stc}">{strainer}</g>')
        # the tin: down for each shake, then back up
        tin_svg, shake_states, tin_states = '', [(0, {'transform': 'rotate(0)'})], [(0, {'opacity': 0, 'transform': 'translateY(-120px)'})]
        frost = ''
        if shaken:
            for a in acts:
                if a[2] not in ('shake', 'dry'):
                    continue
                t0, t1 = a[-2], a[-1]
                tin_states += [(t0, {'opacity': 0, 'transform': 'translateY(-120px)'}), (t0 + .05, {'opacity': 1}), (t0 + .45, {'transform': 'translateY(0)'}),
                               (t1 - .45, {'transform': 'translateY(0)'}), (t1 - .05, {'transform': 'translateY(-120px)'}), (t1, {'opacity': 0})]
                n, s0, s1 = 10, t0 + .55, t1 - .55
                shake_states += [(s0 - .01, {'transform': 'rotate(0)'})] + [(s0 + (s1 - s0) * i / n, {'transform': f'rotate({0 if i in (0, n) else (14 if i % 2 else -14)}deg)'}) for i in range(n + 1)]
                if a[2] == 'shake':
                    fc = self.cls('frost')
                    frost += f'<g class="{fc}">{sparkle(172, 72, 4, "twinkle")}{sparkle(206, 84, 4.4, "twinkle d2")}{sparkle(186, 100, 3.6, "twinkle d3")}</g>'
                    self.window(fc, t0 + 1.3, t1 - .5)
            tc = self.cls('tin')
            tin_svg = (f'<g class="{tc}">' + wash(f'<path d="{TIN}" fill="#c9c3b8"/>') + lines(f'<path d="{TIN}" stroke-width="2.4"/><path d="M160 104 H220" stroke-width="1.4"/><path d="M167 66 L164 104" stroke="#f4f4f2" stroke-width="3"/>', boil=False)
                       + frost + '</g>')
            self.emit(tc, tin_states)
        sc = self.cls('shk')
        self.emit(sc, shake_states + [(self.T, {'transform': 'rotate(0)'})], base=None)
        # the pour: the mixing glass itself lifts and tips over the glass (its lip lands just above the rim)
        gx, gy, _ = self.target('glass')
        self.lip = (gx - 14, gy - 20)
        dx, dy = self.lip[0] - 220, self.lip[1] - 96
        tip = self.cls('tip')
        rest, poured = 'translate(0px,0px) rotate(0deg)', f'translate({dx:.1f}px,{dy:.1f}px) rotate(68deg)'
        self.emit(tip, [(0, {'transform': rest}), (st0 + .05, {'transform': rest}), (st0 + .55, {'transform': poured}), (gone + .1, {'transform': poured}), (gone + .2, {'transform': rest})], base=None)
        wrap = self.cls('mix')
        self.emit(wrap, [(0, {'opacity': 1}), (gone - .1, {'opacity': 1}), (gone + .05, {'opacity': 0}), (self.T - .75, {'opacity': 0}), (self.T - .3, {'opacity': 1})])
        return f'<g class="{wrap}"><g class="{tip}" style="transform-origin:220px 96px"><g class="{sc}" style="transform-origin:190px 116px">{glass}{tin_svg}</g></g></g>'

    # ------------------------------------------------------------ one action's moving parts
    def actor(self, a):
        step, into, kind = a[0], a[1], a[2]
        t0, t1 = a[-2], a[-1]
        rx, ry, by = self.target(into)
        if kind in ('pour', 'top', 'float', 'sink') and ING[a[3]][1] == 'bottle':
            side = -1 if (into == 'glass' and self.uses_mix) else 1
            mx, my = rx + side * 44, max(ry - 24, 44)
            s = .8
            L = bottle_height(a[3]) * s
            ang = -122 * side
            c, sc = self.cls('btl'), self.cls('pour')
            body = f'<g class="{c}" style="transform-origin:{f(mx)}px {f(my)}px"><g transform="translate({f(mx)} {f(my)}) rotate({ang})"><g transform="translate(0 {f(L)}) scale({s})">{ing_bottle(a[3])}</g></g></g>'
            tilt = f'rotate({25 * side}deg)'
            self.emit(c, [(0, {'opacity': 0, 'transform': tilt}), (t0, {'opacity': 0, 'transform': tilt}), (t0 + .05, {'opacity': 1}), (t0 + .35, {'transform': 'rotate(0)'}),
                          (t1 - .3, {'transform': 'rotate(0)'}), (t1 - .08, {'transform': tilt}), (t1, {'opacity': 0})])
            end_y = by - 8 if kind != 'float' else ry + (by - ry) * .12
            if kind == 'sink':
                end_y = by - 4
            color = visible(ING[a[3]][2])
            stream = lines(f'<path d="M{f(mx)} {f(my + 1)} Q{f(rx + side * 16)} {f(my + (end_y - my) * .4)} {f(rx + side * 3)} {f(end_y)}" stroke="{color}" stroke-width="{3.4 if kind != "float" else 2.6}"/>',
                           boil=False, extra=f' class="{sc}"')
            self.window(sc, t0 + .38, t1 - .3)
            return body + stream
        if kind == 'pour':   # a jigger: juice, syrup
            px, py = rx - 40, max(ry - 38, 36)
            c, sc = self.cls('jig'), self.cls('pour')
            body = f'<g class="{c}" style="transform-origin:{f(px)}px {f(py)}px"><g transform="translate({f(px)} {f(py)})">{jigger()}</g></g>'
            self.emit(c, [(0, {'opacity': 0, 'transform': 'rotate(0)'}), (t0, {'opacity': 0, 'transform': 'rotate(0)'}), (t0 + .05, {'opacity': 1}), (t0 + .35, {'transform': 'rotate(100deg)'}),
                          (t1 - .35, {'transform': 'rotate(100deg)'}), (t1 - .1, {'transform': 'rotate(0)'}), (t1, {'opacity': 0})])
            stream = lines(f'<path d="M{f(px + 13)} {f(py + 4)} Q{f(rx - 12)} {f(ry + 4)} {f(rx - 2)} {f(by - 10)}" stroke="{ING[a[3]][2]}" stroke-width="3.2"/>', boil=False, extra=f' class="{sc}"')
            self.window(sc, t0 + .38, t1 - .38)
            return body + stream
        if kind == 'dash':
            bx, bby = rx + 22.5, max(ry - 37.5, 40)
            c, w = self.cls('dsh'), self.cls('dshw')
            body = (f'<g class="{w}"><g class="{c}" style="transform-origin:{f(bx)}px {f(bby)}px"><g transform="translate({f(bx)} {f(bby)}) rotate(200)">{bitters()}</g></g></g>')
            self.window(w, t0 + .05, t1 - .1)
            st = [(0, {'transform': 'rotate(0)'}), (t0 + .2, {'transform': 'rotate(0)'})]
            n = max(2, min(int(a[4]), 4))
            for i in range(n):
                tt = t0 + .25 + i * (t1 - t0 - .5) / n
                st += [(tt, {'transform': 'rotate(-12deg)'}), (tt + .1, {'transform': 'rotate(4deg)'})]
            st += [(t1, {'transform': 'rotate(0)'})]
            self.emit(c, st, base=None)
            drops = ''
            for i in range(n):
                dc = self.cls('drop')
                drops += f'<g class="{dc}"><path d="M{f(rx + 14)} {f(ry - 15)} q-2.6 3.6 0 5.6 q2.6 -2 0 -5.6Z" fill="{ING[a[3]][2]}"/></g>'
                tt = t0 + .32 + i * (t1 - t0 - .5) / n
                self.emit(dc, [(0, {'opacity': 0, 'transform': 'translateY(0)'}), (tt, {'opacity': 0, 'transform': 'translateY(0)'}), (tt + .03, {'opacity': 1}),
                               (tt + .35, {'opacity': 1, 'transform': f'translateY({f(by - ry + 4)}px)'}), (tt + .38, {'opacity': 0})])
            return body + drops
        if kind == 'egg':
            ex, ey = rx + 2, ry - 26
            et = wash('<path d="M-11 0 Q-11 -18 0 -18 Q11 -18 11 0 L6 -3 L2 2 L-3 -3 L-7 2Z" fill="#f6ead2"/>') + lines('<path d="M-11 0 Q-11 -18 0 -18 Q11 -18 11 0 L6 -3 L2 2 L-3 -3 L-7 2Z" stroke-width="1.8"/>', boil=False)
            eb = wash('<path d="M-11 0 Q-11 14 0 14 Q11 14 11 0 L6 -3 L2 2 L-3 -3 L-7 2Z" fill="#f6ead2"/>') + lines('<path d="M-11 0 Q-11 14 0 14 Q11 14 11 0 L6 -3 L2 2 L-3 -3 L-7 2Z" stroke-width="1.8"/>', boil=False)
            w, ct, cb, wh = self.cls('egg'), self.cls('egt'), self.cls('egb'), self.cls('egw')
            body = (f'<g class="{w}"><g class="{ct}" style="transform-origin:{f(ex)}px {f(ey)}px"><g transform="translate({f(ex)} {f(ey)})">{et}</g></g>'
                    f'<g class="{cb}" style="transform-origin:{f(ex)}px {f(ey)}px"><g transform="translate({f(ex)} {f(ey)})">{eb}</g></g></g>'
                    f'<g class="{wh}"><path d="M{f(ex)} {f(ey + 6)} q-6 6 -2 11 q2 3 4 0 q4 -5 -2 -11Z" fill="#fffaf1" stroke="#c9c3b8" stroke-width="1.2"/></g>')
            self.window(w, t0 + .05, t1 - .2)
            self.emit(ct, [(0, {'transform': 'translate(0,0)'}), (t0 + .4, {'transform': 'translate(0,0)'}), (t0 + .6, {'transform': 'translate(-8px,-8px) rotate(-30deg)'})], base=None)
            self.emit(cb, [(0, {'transform': 'translate(0,0)'}), (t0 + .4, {'transform': 'translate(0,0)'}), (t0 + .6, {'transform': 'translate(8px,6px) rotate(30deg)'})], base=None)
            self.emit(wh, [(0, {'opacity': 0, 'transform': 'translateY(0)'}), (t0 + .5, {'opacity': 0, 'transform': 'translateY(0)'}), (t0 + .55, {'opacity': 1}),
                           (t1 - .2, {'opacity': 1, 'transform': f'translateY({f(by - ey - 22)}px)'}), (t1 - .15, {'opacity': 0})])
            return body
        if kind == 'mint':
            return ''   # the leaves themselves live in the mixing glass
        if kind == 'salt':
            out = ''
            for i, (dx, dy) in enumerate(((-4, 0), (2, -3), (6, 2), (-1, 5))):
                c = self.cls('salt')
                out += f'<g class="{c}"><rect x="{f(rx + dx - 1.2)}" y="{f(ry - 30 + dy)}" width="2.4" height="2.4" fill="#fffaf1" stroke="#a9a29a" stroke-width=".6"/></g>'
                tt = t0 + .2 + i * .08
                self.emit(c, [(0, {'opacity': 0, 'transform': 'translateY(0)'}), (tt, {'opacity': 0, 'transform': 'translateY(0)'}), (tt + .05, {'opacity': 1}),
                              (tt + .55, {'opacity': 1, 'transform': f'translateY({f(by - ry + 18)}px)'}), (tt + .6, {'opacity': 0})])
            return out
        if kind == 'stir':
            # a bar spoon, swirling in the glass it's in
            if into == 'mix':
                bx, bby, top = 204, 182, (222, 70)
            else:
                bx, bby = rx + 6, by - 6
                top = (rx + 20, ry - 34)
            c, w = self.cls('spn'), self.cls('spnw')
            body = (f'<g class="{w}"><g class="{c}" style="transform-origin:{f(bx)}px {f(bby)}px">'
                    + lines(f'<path d="M{f(top[0])} {f(top[1])} L{f(bx)} {f(bby)}" stroke="#a9a29a" stroke-width="3"/><circle cx="{f(top[0])}" cy="{f(top[1]) }" r="4.2" fill="#c9c3b8"/>'
                            f'<ellipse cx="{f(bx)}" cy="{f(bby + 2)}" rx="5" ry="3" fill="#c9c3b8"/>', boil=False, width=2) + '</g></g>')
            self.window(w, t0 + .05, t1 - .1)
            st = [(0, {'transform': 'rotate(0)'}), (t0 + .15, {'transform': 'rotate(0)'})]
            n = 8
            for i in range(n + 1):
                st.append((t0 + .2 + (t1 - t0 - .45) * i / n, {'transform': f'rotate({0 if i in (0, n) else (7 if i % 2 else -7)}deg)'}))
            self.emit(c, st, base=None)
            return body
        if kind == 'strain':   # the mixing glass tips (see mixing_glass); this is its pour
            gx, gy, gby = self.target('glass')
            lx, ly = self.lip
            sc = self.cls('pour')
            stream = lines(f'<path d="M{f(lx + 1)} {f(ly + 2)} Q{f(lx + 8)} {f(ly + 16)} {f(gx - 1)} {f(gby - 6)}" stroke="{self.d.get("base", self.d["color"])}" stroke-width="3.4"/>', boil=False, extra=f' class="{sc}"')
            self.window(sc, t0 + .55, t1 - .4)
            return stream
        return ''

    def caption(self, a):
        kind = a[2]
        if kind in ('pour', 'top', 'float', 'sink'):
            q = a[4]
            word = ING[a[3]][0]
            return f'{oz_text(q)} {word}' if q and kind != 'top' else (f'{word}' if kind != 'top' else f'top with {word}')
        if kind == 'dash':
            n = int(a[4])
            return f'{n} dash{"es" if n > 1 else ""} {ING[a[3]][0].replace(" bitters", "")} bitters'
        return {'egg': '1 egg white', 'mint': 'fresh mint', 'salt': 'a pinch of salt', 'ice': 'ice', 'dry': 'dry shake', 'shake': 'shake!', 'stir': 'stir, stir, stir', 'strain': 'strain'}.get(kind)

    def step_css(self):
        out = []
        for i, (t0, t1) in enumerate(self.steps, 1):
            c = f'hs{i}'
            p0, p1 = self.pc(t0), self.pc(t1)
            out.append(f'.howto-steps li.s{i}{{animation:{c} {self.T:g}s linear infinite}}'
                       f'@keyframes {c}{{0%{{background-color:transparent}}{max(p0 - .6, 0):g}%{{background-color:transparent}}{p0:g}%{{background-color:var(--step-hl)}}'
                       f'{p1:g}%{{background-color:var(--step-hl)}}{min(p1 + .6, 100):g}%{{background-color:transparent}}100%{{background-color:transparent}}}}')
        return out

    def page_css(self):
        return ('/* the build, step by step (' + f'{self.T:g}' + ' s). Still frame: the finished drink. */\n'
                + (','.join(self.base) + '{opacity:0}\n' if self.base else '') + '\n'.join(self.css + self.step_css()))
