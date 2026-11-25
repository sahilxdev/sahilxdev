"""Illustration kit: panels, isometric scenes, little people."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Sheet as _Base, S4, S5, S6, PI, TNUM, f  # noqa: F401

INK, INK2, INK3 = '#171A14', '#23271F', '#30352A'
PAPER, PAPER2, PAPER3 = '#F2F1EB', '#E4E3D8', '#CFCFC2'
SAGE, SAGE_D, SAGE_L, SAGE_P = '#637149', '#4C5838', '#B9C49A', '#DDE3CC'
SAGE_M = '#8A9A6B'
MUTE, MUTE_D = '#6E7167', '#9DA192'      # muted text on light / on dark
LAMP = '#F7E6A1'
C30, S30 = math.cos(math.radians(30)), 0.5
RM = '@media (prefers-reduced-motion:reduce){*{animation:none!important}}'


class Panel(_Base):
    """One self-contained picture with its own ground colour."""

    def __init__(self, H, bg, title, r=26):
        super().__init__(H, {'paper': bg, 'wall': INK, 'faint': MUTE}, title)
        self.bg, self.r = bg, r
        self.css.append(RM)

    def wrap_last(self, n, open_tag, close='</g>'):
        tail = self.body[-n:]
        del self.body[-n:]
        self.body.append(open_tag + ''.join(tail) + close)

    def mark(self): return len(self.body)

    def group_since(self, mark, open_tag, close='</g>'):
        tail = self.body[mark:]
        del self.body[mark:]
        self.body.append(open_tag + ''.join(tail) + close)

    def reveal(self, x, y, s, face, size, fill, ls=0, t0=0.1, step=0.035):
        """Type that rises into place, one letter after another."""
        run = face.shape(s)
        k = size / face.upm; tr = ls * face.upm
        cid = f'rv{len(self.extra_defs)}'
        wu = sum(r[1] for r in run) + tr * max(len(run) - 1, 0)
        self.extra_defs.append(f'<clipPath id="{cid}"><rect x="{f(x - 20)}" y="{f(y - size * 1.05)}" width="{f(wu * k + 40)}" height="{f(size * 1.32)}"/></clipPath>')
        out = []; cx = 0; i = 0
        for gid, adv, xo, yo in run:
            d = face.path(gid)
            if d:
                gi = f'{face.name}{gid}'; self.defs[gi] = d
                out.append(f'<use class="rv" href="#{gi}" x="{f(cx + xo)}" style="animation-delay:{t0 + i * step:.3f}s"/>')
                i += 1
            cx += adv + tr
        self.add(f'<g clip-path="url(#{cid})"><g transform="translate({f(x)} {f(y)}) scale({k:.5f} {-k:.5f})" fill="{fill}">{"".join(out)}</g></g>')
        rise = int(face.upm * 1.25)
        rule = f'.rv{{animation:rv .9s cubic-bezier(.2,.8,.2,1) both}}@keyframes rv{{from{{transform:translateY(-{rise}px)}}to{{transform:none}}}}'
        if rule not in self.css: self.css.append(rule)
        return wu * k

    def svg(self):
        W, H = self.W, self.H
        defs = ''.join(f'<path id="{k}" d="{v}"/>' for k, v in sorted(self.defs.items()))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{self.title}">'
                f'<title>{self.title}</title><style>{"".join(self.css)}</style><defs>{defs}{"".join(self.extra_defs)}'
                f'<clipPath id="pn"><rect width="{W}" height="{H}" rx="{self.r}"/></clipPath></defs>'
                f'<g clip-path="url(#pn)"><rect width="{W}" height="{H}" fill="{self.bg}"/>{"".join(self.body)}</g></svg>\n')


class Iso:
    """Isometric projection. x runs down-right, y runs down-left, z is up."""

    def __init__(self, ox, oy, u):
        self.ox, self.oy, self.u = ox, oy, u

    def p(self, x, y, z=0):
        return (self.ox + (x - y) * C30 * self.u, self.oy + (x + y) * S30 * self.u - z * self.u)

    def pts(self, P):
        return ' '.join(f'{f(a)},{f(b)}' for a, b in (self.p(*q) for q in P))

    def poly(self, P, fill, stroke=None, sw=1, extra=''):
        st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ''
        return f'<polygon points="{self.pts(P)}" fill="{fill}"{st}{extra}/>'

    def line(self, a, b, stroke, sw=1, extra=''):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        return f'<path d="M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}" stroke="{stroke}" stroke-width="{sw}" fill="none" stroke-linecap="round"{extra}/>'

    def box(self, x, y, z, w, d, h, top, left, right, stroke=None):
        """left = the face looking down-left (y max), right = the face looking down-right (x max)."""
        x1, y1, z1 = x + w, y + d, z + h
        return (self.poly([(x, y1, z), (x1, y1, z), (x1, y1, z1), (x, y1, z1)], left, stroke)
                + self.poly([(x1, y, z), (x1, y1, z), (x1, y1, z1), (x1, y, z1)], right, stroke)
                + self.poly([(x, y, z1), (x1, y, z1), (x1, y1, z1), (x, y1, z1)], top, stroke))

    def on_right_wall(self, x, z):          # matrix for art drawn flat on the y=0 wall
        px, py = self.p(x, 0, z)
        return f'matrix({C30:.4f} {S30} 0 1 {f(px)} {f(py)})'

    def on_left_wall(self, y, z):           # the x=0 wall, reading from far end to the corner
        px, py = self.p(0, y, z)
        return f'matrix({C30:.4f} {-S30} 0 1 {f(px)} {f(py)})'


def person(px, py, body, s=1.0, head=None, shadow='#000', so=0.16):
    """A little standing figure with its feet at (px, py)."""
    head = head or body
    w, h, r = 11 * s, 19 * s, 5.4 * s
    return (f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(8.5 * s)}" ry="{f(3.6 * s)}" fill="{shadow}" opacity="{so}"/>'
            f'<rect x="{f(px - w / 2)}" y="{f(py - h - 1.5 * s)}" width="{f(w)}" height="{f(h)}" rx="{f(w / 2)}" fill="{body}"/>'
            f'<circle cx="{f(px)}" cy="{f(py - h - 1.5 * s - r * .78)}" r="{f(r)}" fill="{head}"/>')


def table(px, py, s=1.0, top=PAPER, leg=INK2):
    h = 20 * s
    return (f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(7 * s)}" ry="{f(3.2 * s)}" fill="#000" opacity=".16"/>'
            f'<path d="M{f(px)} {f(py)}V{f(py - h)}" stroke="{leg}" stroke-width="{f(2.4 * s)}"/>'
            f'<ellipse cx="{f(px)}" cy="{f(py - h)}" rx="{f(12 * s)}" ry="{f(5.6 * s)}" fill="{top}" stroke="{leg}" stroke-width="1"/>')


def plant(px, py, s=1.0, leaf=SAGE_M, pot=PAPER3):
    lv = ''
    for a, l in ((-52, 20), (-24, 26), (0, 29), (24, 25), (50, 19)):
        lv += f'<ellipse cx="0" cy="{f(-l * s * .58)}" rx="{f(4.6 * s)}" ry="{f(l * s * .58)}" fill="{leaf}" transform="rotate({a})"/>'
    return (f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(9 * s)}" ry="{f(4 * s)}" fill="#000" opacity=".16"/>'
            f'<path d="M{f(px - 7 * s)} {f(py - 13 * s)}h{f(14 * s)}l{f(-2 * s)} {f(13 * s)}h{f(-10 * s)}z" fill="{pot}"/>'
            f'<g transform="translate({f(px)} {f(py - 13 * s)})"><g class="sway">{lv}</g></g>')
