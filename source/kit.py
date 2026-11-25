"""Drawing kit: outlined type (HarfBuzz-shaped), themes, walls and doors."""
import io, math, os, random
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
import uharfbuzz as hb

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules', '@fontsource-variable')


class Face:
    def __init__(self, path, loc, name):
        f = TTFont(path)
        if 'fvar' in f:
            axes = {a.axisTag for a in f['fvar'].axes}
            loc = {k: v for k, v in loc.items() if k in axes}
            for a in f['fvar'].axes:
                loc.setdefault(a.axisTag, a.defaultValue)
            f = instancer.instantiateVariableFont(f, loc, inplace=False)
        f.flavor = None
        buf = io.BytesIO(); f.save(buf); data = buf.getvalue()
        self.tt = TTFont(io.BytesIO(data))
        self.upm = self.tt['head'].unitsPerEm
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.hb = hb.Font(hb.Face(data))
        self.name = name
        self._p = {}

    def shape(self, s, feat=None):
        b = hb.Buffer(); b.add_str(s); b.guess_segment_properties()
        hb.shape(self.hb, b, feat or {})
        return [(i.codepoint, p.x_advance, p.x_offset, p.y_offset)
                for i, p in zip(b.glyph_infos, b.glyph_positions)]

    def path(self, gid):
        if gid not in self._p:
            pen = SVGPathPen(self.gs, ntos=lambda v: str(int(round(v))))
            self.gs[self.order[gid]].draw(pen)
            self._p[gid] = pen.getCommands()
        return self._p[gid]

    def width(self, s, size, ls=0, feat=None):
        run = self.shape(s, feat)
        return (sum(r[1] for r in run) + ls * self.upm * max(len(run) - 1, 0)) * size / self.upm


S4 = Face(f'{FD}/instrument-sans/files/instrument-sans-latin-wght-normal.woff2', {'wght': 400}, 'a')
S5 = Face(f'{FD}/instrument-sans/files/instrument-sans-latin-wght-normal.woff2', {'wght': 500}, 'b')
S6 = Face(f'{FD}/instrument-sans/files/instrument-sans-latin-wght-normal.woff2', {'wght': 600}, 'c')
PI = Face(f'{FD}/playfair/files/playfair-latin-opsz-italic.woff2', {'wght': 400, 'opsz': 30}, 'p')

LIGHT = dict(name='light', paper='#F2F1EB', paper2='#E9E8DF', ink='#252823', ink2='#3B3E37',
             mute='#6E7167', faint='#A9AC9F', line='#D7D8CF', sage='#637149', sage2='#B9C49A', wall='#252823')
DARK = dict(name='dark', paper='#14170F', paper2='#1D2117', ink='#EEEDE5', ink2='#D2D2C8',
            mute='#9B9E90', faint='#62665A', line='#30342A', sage='#B4C491', sage2='#566440', wall='#D9D9CF')

TNUM = {'tnum': True}


def f(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return s if s else '0'


class Sheet:
    W = 1000
    T = 5  # wall thickness

    def __init__(self, H, theme, title):
        self.H = H; self.c = theme; self.title = title
        self.defs = {}; self.extra_defs = []; self.body = []; self.css = []

    # ---- type -------------------------------------------------------
    def text(self, x, y, s, face, size, fill, ls=0, anchor='start', feat=None, opacity=None, cls=None):
        run = face.shape(s, feat)
        k = size / face.upm
        tr = ls * face.upm
        wu = sum(r[1] for r in run) + tr * max(len(run) - 1, 0)
        x0 = x - (wu * k if anchor == 'end' else wu * k / 2 if anchor == 'middle' else 0)
        uses = []; cx = 0
        for gid, adv, xo, yo in run:
            d = face.path(gid)
            if d:
                gi = f'{face.name}{gid}'
                self.defs[gi] = d
                pos = f' x="{f(cx + xo)}"' if cx + xo else ''
                pos += f' y="{f(yo)}"' if yo else ''
                uses.append(f'<use href="#{gi}"{pos}/>')
            cx += adv + tr
        o = f' opacity="{opacity}"' if opacity is not None else ''
        cl = f' class="{cls}"' if cls else ''
        self.body.append(f'<g transform="translate({f(x0)} {f(y)}) scale({k:.5f} {-k:.5f})" fill="{fill}"{o}{cl}>{"".join(uses)}</g>')
        return wu * k

    def runs(self, x, y, parts, size, ls=0):
        """parts: [(string, face, fill)] set on one baseline."""
        for s, face, fill in parts:
            x += self.text(x, y, s, face, size, fill, ls=ls)
            x += ls * size
        return x

    @staticmethod
    def wrap(s, face, size, maxw, ls=0):
        lines, cur = [], ''
        for w in s.split(' '):
            t = (cur + ' ' + w).strip()
            if face.width(t, size, ls) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur); cur = w
        if cur: lines.append(cur)
        return lines

    def para(self, x, y, s, face, size, fill, maxw, lh, ls=0, anchor='start'):
        for i, ln in enumerate(self.wrap(s, face, size, maxw, ls)):
            self.text(x, y + i * lh, ln, face, size, fill, ls=ls, anchor=anchor)
        return y + (i + 1) * lh

    # ---- primitives -------------------------------------------------
    def add(self, s): self.body.append(s)

    def line(self, x1, y1, x2, y2, stroke, w=1, dash=None, cap='butt', opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{opacity}"' if opacity is not None else ''
        self.add(f'<path d="M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}" stroke="{stroke}" stroke-width="{f(w)}" stroke-linecap="{cap}" fill="none"{d}{o}/>')

    # ---- walls and doors -------------------------------------------
    def walls(self, doors=()):
        """doors: (side, pos, width, kind) ; kind 'open' = bare opening, or
        'L'/'R' hinge side for a leaf that swings into this room."""
        W, H, T, c = self.W, self.H, self.T, self.c
        h = T / 2
        segs = {'top': [(0, W)], 'bottom': [(0, W)], 'left': [(0, H)], 'right': [(0, H)]}
        for side, pos, wd, kind in doors:
            out = []
            for a, b in segs[side]:
                if a < pos and pos + wd < b: out += [(a, pos), (pos + wd, b)]
                else: out.append((a, b))
            segs[side] = out
        P = []
        for a, b in segs['top']: P.append(f'M{f(a)} {f(h)}H{f(b)}')
        for a, b in segs['bottom']: P.append(f'M{f(a)} {f(H - h)}H{f(b)}')
        for a, b in segs['left']: P.append(f'M{f(h)} {f(a)}V{f(b)}')
        for a, b in segs['right']: P.append(f'M{f(W - h)} {f(a)}V{f(b)}')
        self.add(f'<path d="{"".join(P)}" stroke="{c["wall"]}" stroke-width="{T}" fill="none" stroke-linecap="butt"/>')
        for side, pos, wd, kind in doors:
            # threshold: two hairlines across the opening
            if side in ('top', 'bottom'):
                yy = 0 if side == 'top' else H - T
                for dy in (0.5, T - 0.5):
                    self.line(pos, yy + dy, pos + wd, yy + dy, c['faint'], 1)
            else:
                xx = 0 if side == 'left' else W - T
                for dx in (0.5, T - 0.5):
                    self.line(xx + dx, pos, xx + dx, pos + wd, c['faint'], 1)
            if kind in ('L', 'R'):
                self.door(side, pos, wd, kind)

    def door(self, side, pos, wd, hinge, cls=None):
        """A leaf standing open at 90 degrees, with its swing arc."""
        W, H, T, c = self.W, self.H, self.T, self.c
        if side == 'bottom':
            y = H - T; hx = pos if hinge == 'L' else pos + wd; ox = pos + wd if hinge == 'L' else pos
            leaf = (hx, y, hx, y - wd); sweep = 1 if hinge == 'L' else 0
            arc = f'M{f(hx)} {f(y - wd)}A{wd} {wd} 0 0 {sweep} {f(ox)} {f(y)}'
        elif side == 'top':
            y = T; hx = pos if hinge == 'L' else pos + wd; ox = pos + wd if hinge == 'L' else pos
            leaf = (hx, y, hx, y + wd); sweep = 0 if hinge == 'L' else 1
            arc = f'M{f(hx)} {f(y + wd)}A{wd} {wd} 0 0 {sweep} {f(ox)} {f(y)}'
        elif side == 'left':
            x = T; hy = pos if hinge == 'L' else pos + wd; oy = pos + wd if hinge == 'L' else pos
            leaf = (x, hy, x + wd, hy); sweep = 1 if hinge == 'L' else 0
            arc = f'M{f(x + wd)} {f(hy)}A{wd} {wd} 0 0 {sweep} {f(x)} {f(oy)}'
        else:
            x = W - T; hy = pos if hinge == 'L' else pos + wd; oy = pos + wd if hinge == 'L' else pos
            leaf = (x, hy, x - wd, hy); sweep = 0 if hinge == 'L' else 1
            arc = f'M{f(x - wd)} {f(hy)}A{wd} {wd} 0 0 {sweep} {f(x)} {f(oy)}'
        self.add(f'<path d="{arc}" stroke="{c["faint"]}" stroke-width="1" fill="none" stroke-dasharray="2 3"/>')
        x1, y1, x2, y2 = leaf
        cl = f' class="{cls}"' if cls else ''
        self.add(f'<path{cl} d="M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}" stroke="{c["wall"]}" stroke-width="2" fill="none"/>')
        return leaf

    # ---- output -----------------------------------------------------
    def svg(self):
        W, H, c = self.W, self.H, self.c
        defs = ''.join(f'<path id="{k}" d="{v}"/>' for k, v in sorted(self.defs.items()))
        css = f'<style>{"".join(self.css)}</style>' if self.css else ''
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{self.title}">'
                f'<title>{self.title}</title>{css}<defs>{defs}{"".join(self.extra_defs)}</defs>'
                f'<rect width="{W}" height="{H}" fill="{c["paper"]}"/>{"".join(self.body)}</svg>\n')
