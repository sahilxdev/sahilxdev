"""The scenes. python3 scenes.py [name...] -> out/<name>.svg"""
import math, os, random, sys
from kit2 import *

OUT = os.environ.get('SCENES_OUT') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
os.makedirs(OUT, exist_ok=True)


def kf(name, stops):
    return f'@keyframes {name}{{' + ''.join(f'{p}%{{{v}}}' for p, v in stops) + '}'


# ------------------------------------------------------------------ hero
def hero():
    s = Panel(604, INK, 'Sahil Meena. Founder and CEO, Capvise Group. I build the rooms where builders meet capital. An illustrated room: builders walk in through one door, capital through the other, they meet at the tables and leave together.')
    W, H = s.W, s.H
    s.extra_defs.append('<radialGradient id="gl"><stop offset="0" stop-color="#46523A" stop-opacity=".95"/><stop offset="1" stop-color="#171A14" stop-opacity="0"/></radialGradient>'
                        f'<linearGradient id="dl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6CF"/><stop offset="1" stop-color="{LAMP}"/></linearGradient>')
    s.add('<ellipse cx="725" cy="330" rx="470" ry="360" fill="url(#gl)"/>')
    iso = Iso(722, 196, 36)
    w, d, hh, t = 8.5, 7.5, 4.2, 0.28
    FLOOR, GRID = '#ECEBE1', '#D9D9CB'
    WR, WL, WT = '#6B7A4F', '#55633E', '#93A374'
    a = s.add
    # floor slab
    a(iso.box(0, 0, -0.34, w, d, 0.34, FLOOR, '#B9B9AA', '#A3A394'))
    for i in range(1, 6):
        a(iso.line((i * 1.5, 0), (i * 1.5, d), GRID, 1))
    for i in range(1, 5):
        a(iso.line((0, i * 1.5), (w, i * 1.5), GRID, 1))
    # light falling in through the two doors
    a(iso.poly([(0, 4.5), (0, 5.9), (3.3, 6.7), (3.3, 5.3)], LAMP, extra=' opacity=".30" class="spill"'))
    a(iso.poly([(5.6, 0), (7.0, 0), (7.8, 3.3), (6.4, 3.3)], LAMP, extra=' opacity=".30" class="spill"'))
    # walls
    a(iso.box(-t, 0, -0.34, t, d, hh + 0.34, WT, WR, WL))
    a(iso.box(-t, -t, -0.34, w + t, t, hh + 0.34, WT, WR, '#4A5736'))
    # doors
    a(iso.poly([(0, 4.5, 0), (0, 5.9, 0), (0, 5.9, 2.75), (0, 4.5, 2.75)], 'url(#dl)'))
    a(iso.poly([(5.6, 0, 0), (7.0, 0, 0), (7.0, 0, 2.75), (5.6, 0, 2.75)], 'url(#dl)'))
    # signs over the doors
    m = s.mark(); s.text(0, 0, 'builders', PI, 30, PAPER); s.group_since(m, f'<g transform="{iso.on_left_wall(6.5, 3.2)}">')
    m = s.mark(); s.text(0, 0, 'capital', PI, 30, PAPER); s.group_since(m, f'<g transform="{iso.on_right_wall(5.3, 3.2)}">')
    # the screen
    m = s.mark()
    sw_, sh_ = 3.5 * iso.u, 1.75 * iso.u
    a(f'<rect width="{f(sw_)}" height="{f(sh_)}" rx="5" fill="{INK}"/>')
    s.text(sw_ / 2, sh_ / 2 + 8, 'Founder × VC', S5, 24, PAPER, anchor='middle', ls=-0.01)
    a(f'<circle class="blink" cx="13" cy="13" r="3.4" fill="{LAMP}"/>')
    s.group_since(m, f'<g transform="{iso.on_right_wall(0.85, 3.62)}">')
    # stage and speakers
    a(iso.box(0.5, 0, 0, 4.2, 1.75, 0.3, '#DCDBCF', '#BDBDAE', '#ABAB9C'))
    for i, xx in enumerate((1.25, 2.15, 3.05, 3.95)):
        px, py = iso.p(xx, 0.95, 0.3)
        a(f'<g class="bob" style="animation-delay:-{i * .37:.2f}s">{person(px, py, INK2 if i % 2 else SAGE_D, 1.1)}</g>')

    # ---- everything standing on the floor, drawn back to front
    items = []
    tables = [(2.9, 3.6), (5.4, 3.0), (2.0, 6.1), (4.7, 5.5), (7.2, 4.7)]
    T, rng = 16.0, random.Random(5)
    bdoor, cdoor = (0.5, 5.2), (6.3, 0.5)
    for i, (tx, ty) in enumerate(tables):
        px, py = iso.p(tx, ty)
        pop = (f'<g transform="translate({f(px)} {f(py - 56)})"><path class="pop" style="animation-delay:-{i * T / 5:.2f}s" d="M-6 -6L6 6M6 -6L-6 6" '
               f'stroke="{LAMP}" stroke-width="3" stroke-linecap="round"/></g>')
        items.append((tx + ty, table(px, py, 1.3, top=INK2, leg=INK2) + pop))
        for who, (bx, by), door, col in (('b', (tx - 0.52, ty + 0.52), bdoor, SAGE), ('c', (tx + 0.52, ty - 0.52), cdoor, INK2)):
            k = min(w - bx, d - by) - 0.1
            ex = (bx + k, by + k)
            P0, P1, P2 = iso.p(*door), iso.p(bx, by), iso.p(*ex)
            o0 = f'translate({f(P0[0] - P1[0])}px,{f(P0[1] - P1[1])}px)'
            o2 = f'translate({f(P2[0] - P1[0])}px,{f(P2[1] - P1[1])}px)'
            nm = f'w{who}{i}'
            s.css.append(kf(nm, [(0, f'transform:{o0};opacity:0'), (3, f'transform:{o0};opacity:1'), (27, 'transform:translate(0,0);opacity:1'),
                                 (62, 'transform:translate(0,0);opacity:1'), (86, f'transform:{o2};opacity:1'), (91, f'transform:{o2};opacity:0'),
                                 (100, f'transform:{o2};opacity:0')]))
            g = (f'<g style="animation:{nm} {T}s linear infinite;animation-delay:-{i * T / 5:.2f}s">'
                 f'<g class="bob" style="animation-delay:-{rng.uniform(0, 1):.2f}s">{person(P1[0], P1[1], col, 1.22)}</g></g>')
            items.append((bx + by + 0.01, g))
    for (x, y, col) in ((1.2, 2.8, SAGE), (1.95, 2.5, INK2), (3.7, 2.4, SAGE), (4.4, 2.2, INK2), (6.1, 6.6, SAGE), (6.75, 6.85, INK2), (7.9, 2.4, SAGE), (7.6, 1.9, INK2), (0.9, 4.0, INK2), (3.6, 7.0, SAGE)):
        px, py = iso.p(x, y)
        items.append((x + y, f'<g class="bob" style="animation-delay:-{rng.uniform(0, 1):.2f}s">{person(px, py, col, 1.22)}</g>'))
    for (x, y) in ((7.9, 0.7), (0.7, 7.0), (7.95, 7.0)):
        px, py = iso.p(x, y)
        items.append((x + y, plant(px, py, 1.35)))
    for _, g in sorted(items, key=lambda q: q[0]):
        a(g)
    # pendant lamps
    for i, (x, y) in enumerate(((3.8, 4.5), (6.3, 3.8), (1.9, 6.4))):
        gx, gy = iso.p(x, y); lx, ly = iso.p(x, y, 3.25)
        a(f'<ellipse class="glow" style="animation-delay:-{i * 1.7}s" cx="{f(gx)}" cy="{f(gy)}" rx="74" ry="37" fill="{LAMP}" opacity=".2"/>')
        a(f'<path d="M{f(lx)} {f(ly - 150)}V{f(ly - 12)}" stroke="{INK3}" stroke-width="1.4"/>'
          f'<path d="M{f(lx - 5)} {f(ly - 13)}h10l8 13h-26z" fill="{INK2}"/><ellipse cx="{f(lx)}" cy="{f(ly)}" rx="13" ry="4.4" fill="{LAMP}"/>')

    # ---- type
    s.reveal(50, 196, 'Sahil', S5, 132, PAPER, ls=-0.058, t0=0.1)
    s.reveal(50, 310, 'Meena', S5, 132, PAPER, ls=-0.058, t0=0.3)
    a(f'<circle cx="65" cy="365" r="5" fill="{SAGE_L}"/>')
    s.text(80, 372, 'Founder and CEO, Capvise Group', S6, 20, PAPER, ls=-0.005)
    s.text(59, 436, 'I build the rooms where', S4, 31, MUTE_D, ls=-0.022)
    s.runs(58, 476, [('builders', PI, SAGE_L), (' meet capital.', S4, MUTE_D)], 31, ls=-0.022)
    s.text(60, H - 40, 'sahil.capvise.group', S4, 15.5, MUTE)

    s.css.append('.bob{animation:bob .52s ease-in-out infinite alternate}@keyframes bob{to{transform:translateY(-1.7px)}}'
                 '.pop{transform:scale(0);animation:pop 16s ease-out infinite}'
                 + kf('pop', [(0, 'transform:scale(0);opacity:0'), (27, 'transform:scale(0);opacity:0'), (31, 'transform:scale(1.25);opacity:1'),
                              (34, 'transform:scale(1);opacity:1'), (56, 'transform:scale(1);opacity:1'), (62, 'transform:scale(0);opacity:0'), (100, 'transform:scale(0);opacity:0')])
                 + '.sway{animation:sway 4.6s ease-in-out infinite alternate}@keyframes sway{from{transform:rotate(-3deg)}to{transform:rotate(3deg)}}'
                 '.glow{animation:glow 5s ease-in-out infinite alternate}@keyframes glow{from{opacity:.14}to{opacity:.26}}'
                 '.blink{animation:blink 1.6s steps(2,jump-none) infinite}@keyframes blink{to{opacity:.15}}')
    return s



# ------------------------------------------------------------------ rooms, 2025 and 2026 together
# (city, event, applied, seats, applied label, seats label)
R25 = [('Bali', 'Founder × VC Happy Hour', 600, 100, '600+', '100+'), ('Singapore', 'Founder × VC Summit', 4000, 500, '4,000+', '500'),
       ('Dubai', 'Founder × VC Happy Hour', 600, 150, '600+', '150+'), ('Buenos Aires', 'Somnia Dev City', 1200, 200, '1,200+', '200')]
R26 = [('Hong Kong', 'Whiskey & Whales', 850, 150, '850+', '150'), ('Hong Kong', 'Whales After Dark', 750, 100, '750+', '100'),
       ('Cannes', 'Onchain Dev City', 600, 200, '600+', '200'), ('Cannes', 'Whiskey & Whales', 700, 100, '700+', '100'),
       ('Paris', 'Founders & Capital', 30, 30, '30+', '30'), ('Bali', 'Whiskey & Whales', 150, 50, '150+', '50'),
       ('Barcelona', 'Whiskey & Whales', 550, 150, '550+', '150'), ('Seoul', 'Kimchi & Whales', 0, 10, None, '10'),
       ('Singapore', 'Money Layer', 900, 300, '900+', '300'), ('Singapore', 'Institutions & Whales', 550, 25, '550+', '25'),
       ('Mumbai', 'Onchain Dev City', 1000, 250, '1,000+', '250'), ('Mumbai', 'Money Layer', 750, 250, '750+', '250'),
       ('London', 'Money Layer', 350, 150, '350+', '150')]


def rooms():
    a25, s25 = sum(r[2] for r in R25), sum(r[3] for r in R25)
    a26, s26 = sum(r[2] for r in R26), sum(r[3] for r in R26)
    say = lambda rs: ' '.join(f'{ev}, {city}: {(al + " applied for ") if al else ""}{sl} seats.' for city, ev, _, _, al, sl in rs)
    alt = (f'Seventeen rooms so far. {a25 + a26:,}+ people applied for {s25 + s26:,}+ seats. Each little figure is 25 people. '
           f'2025, four rooms: {say(R25)} 2026, thirteen rooms: {say(R26)}')
    gap, sp, per, hh, t = 0.7, 0.58, 25, 1.9, 0.16
    WR, WL, WT, FLOOR = '#6B7A4F', '#55633E', '#93A374', '#FFFFFF'
    x0, x1 = 44, 956

    def measure(u):
        groups = []
        for rs in (R25, R26):
            cells = []
            for city, ev, apps, seats, al, sl in rs:
                side = max(math.sqrt(seats) / 4.4, 0.95)
                cols = max(2, round(side / sp))
                n_out = max(1, round(apps / per)) if apps else 0
                nrow = math.ceil(n_out / cols)
                ymax = side + (gap + nrow * sp if nrow else 0)
                cells.append(dict(city=city, ev=ev, seats=seats, al=al, sl=sl, side=side, cols=cols, n_out=n_out, rows=nrow,
                                  left=max(ymax * C30 * u + 6, 78), right=max(side * C30 * u + 6, 78),
                                  depth=(max(side, cols * sp) + ymax) * S30 * u))
            groups.append(cells)
        return groups

    def split(cells, n):                       # n balanced rows, in order
        wd = [c['left'] + c['right'] for c in cells]
        if n == 1: return [cells], sum(wd)
        best = None
        for sp_ in ((5, 4, 4), (4, 5, 4), (4, 4, 5)):
            i = 0; rw = []
            for k in sp_:
                rw.append(sum(wd[i:i + k])); i += k
            if best is None or max(rw) < best[0]: best = (max(rw), sp_)
        out, i = [], 0
        for k in best[1]:
            out.append(cells[i:i + k]); i += k
        return out, best[0]

    u = 22.0
    while True:                                # the largest scale at which every row fits
        g25, g26 = measure(u)
        l25, w25 = split(g25, 1); l26, w26 = split(g26, 3)
        if max(w25, w26) <= x1 - x0: break
        u -= 0.25
    fs = u / 21 * 0.66
    label_h, head_h, top = 74, 62, 148
    blocks = [('2025', 'Four rooms.', a25, f'{s25:,}+', l25), ('2026', 'Thirteen rooms.', a26, f'{s26:,}', l26)]
    hts = [[label_h + hh * u + max(c['depth'] for c in ln) + 26 for ln in lines] for *_, lines in blocks]
    s = Panel(round(top + sum(head_h + sum(h) for h in hts) + 50), PAPER, alt)
    W, H = s.W, s.H
    a = s.add
    s.text(53, 92, 'Seventeen rooms so far.', S5, 44, INK2, ls=-0.035)
    s.runs(56, 128, [(f'{a25 + a26:,}+ people applied for ', S4, MUTE), (f'{s25 + s26:,}+ seats', S6, SAGE), ('.', S4, MUTE)], 19.5)
    y, ri = top, 0
    for (yr, what, apps, seats_l, lines), hs in zip(blocks, hts):
        s.text(54, y + 40, yr, S5, 30, INK2, ls=-0.03, feat=TNUM)
        xe = s.runs(136, y + 39, [(what + ' ', S4, MUTE), (f'{apps:,}+ applied', S6, INK2), (' for ', S4, MUTE), (f'{seats_l} seats', S6, SAGE)], 16)
        s.line(xe + 18, y + 33, W - 54, y + 33, PAPER3, 1.4)
        y += head_h
        for ln, hgt in zip(lines, hs):
            slack = (x1 - x0 - sum(c['left'] + c['right'] for c in ln)) / len(ln)
            x = x0; oy = y + label_h + hh * u
            for c in ln:
                ox = x + slack / 2 + c['left']; x += c['left'] + c['right'] + slack
                iso = Iso(ox, oy, u); side = c['side']
                a(iso.box(0, 0, -0.2, side, side, 0.2, FLOOR, '#C9C9BB', '#B5B5A6'))
                a(iso.box(-t, 0, -0.2, t, side, hh + 0.2, WT, WR, WL))
                a(iso.box(-t, -t, -0.2, side + t, t, hh + 0.2, WT, WR, '#4A5736'))
                n_in = max(1, round(c['seats'] / per)); ic = max(1, round(math.sqrt(n_in))); nr = math.ceil(n_in / ic); k = 0
                inside = []
                for r in range(nr):
                    for ci in range(ic):
                        if k >= n_in: break
                        px, py = (ci + 0.5) * side / ic, (r + 0.5) * side / nr
                        inside.append((px + py, person(*iso.p(px, py), SAGE, fs, so=0.12))); k += 1
                for _, g in sorted(inside, key=lambda q: q[0]): a(g)
                k = 0
                for r in range(c['rows']):
                    row = ''
                    for ci in range(c['cols']):
                        if k >= c['n_out']: break
                        row += person(*iso.p((ci + 0.5) * sp, side + gap + (r + 0.5) * sp), INK2, fs, so=0.10); k += 1
                    a(f'<g class="rp" style="animation-delay:-{(c["rows"] - r) * 0.09 + ri * 0.31:.2f}s">{row}</g>')
                lx, ly = iso.p(0, 0, hh)
                s.text(lx, ly - 50, c['city'], S5, 19, INK2, ls=-0.02, anchor='middle')
                s.text(lx, ly - 32, c['ev'], S4, 13.5, MUTE, anchor='middle')
                if c['al']:
                    wA = S6.width(c['al'] + ' applied', 13.5); wS = S6.width(f'  {c["sl"]} seats', 13.5)
                    xx = lx - (wA + wS) / 2
                    s.text(xx, ly - 14, c['al'] + ' applied', S6, 13.5, INK2); s.text(xx + wA, ly - 14, f'  {c["sl"]} seats', S6, 13.5, SAGE)
                else:
                    s.text(lx, ly - 14, f'{c["sl"]} seats', S6, 13.5, SAGE, anchor='middle')
                ri += 1
            y += hgt
    lx, ly = 56, H - 40
    a(person(lx + 6, ly + 6, INK2, 0.75)); s.text(lx + 20, ly, 'one figure is 25 people', S4, 14.5, MUTE)
    a(person(lx + 206, ly + 6, SAGE, 0.75)); s.text(lx + 220, ly, 'sage figures had a seat', S4, 14.5, MUTE)
    s.css.append('.rp{animation:rp 2.6s ease-in-out infinite}' + kf('rp', [(0, 'transform:none'), (10, 'transform:translateY(-4px)'), (22, 'transform:none'), (100, 'transform:none')]))
    return s


# ------------------------------------------------------------------ 2027 map
CITY = {'Bali': (115.2, -8.4), 'Singapore': (103.8, 1.35), 'Dubai': (55.3, 25.2), 'Buenos Aires': (-58.4, -34.6), 'Hong Kong': (114.2, 22.3),
        'Cannes': (7.0, 43.55), 'Paris': (2.35, 48.86), 'Barcelona': (2.17, 41.39), 'Seoul': (126.98, 37.57), 'Mumbai': (72.88, 19.08),
        'London': (-0.13, 51.51), 'Bangkok': (100.5, 13.75), 'Miami': (-80.2, 25.76), 'Amsterdam': (4.9, 52.37), 'New York': (-74.0, 40.71),
        'Nashville': (-86.8, 36.16), 'San Francisco': (-122.4, 37.77), 'Las Vegas': (-115.1, 36.17), 'Abu Dhabi': (54.4, 24.45)}
# every room on the Capvise Global calendar, in order
YEARS = [('2025', '4 rooms', ['Bali', 'Singapore', 'Dubai', 'Buenos Aires']),
         ('2026', '13 rooms', ['Hong Kong', 'Hong Kong', 'Cannes', 'Cannes', 'Paris', 'Bali', 'Barcelona', 'Seoul', 'Singapore', 'Singapore', 'Mumbai', 'Mumbai', 'London']),
         ('2027', '16 on the calendar', ['Hong Kong', 'Cannes', 'Bangkok', 'Miami', 'Amsterdam', 'New York', 'Nashville', 'Bali', 'Hong Kong', 'San Francisco',
                                         'Singapore', 'Las Vegas', 'Singapore', 'Bangkok', 'Dubai', 'Abu Dhabi'])]
LBL = {'London': (-9, -3, 'end'), 'Amsterdam': (9, -4, 'start'), 'Paris': (-9, 10, 'end'), 'Cannes': (9, 7, 'start'), 'Barcelona': (-9, 13, 'end'),
       'Dubai': (-9, -5, 'end'), 'Abu Dhabi': (-9, 14, 'end'), 'Mumbai': (-9, 14, 'end'), 'Bangkok': (-9, -4, 'end'), 'Singapore': (-9, 11, 'end'),
       'Bali': (9, 10, 'start'), 'Hong Kong': (9, 5, 'start'), 'Seoul': (9, -5, 'start'), 'New York': (9, -5, 'start'), 'Nashville': (9, 16, 'start'),
       'Miami': (9, 13, 'start'), 'San Francisco': (-8, -12, 'start'), 'Las Vegas': (0, 20, 'middle'), 'Buenos Aires': (9, 5, 'start')}


def land_dots(step, lon0, lon1, lat0, lat1):
    import json
    from shapely.geometry import shape, Point
    from shapely.ops import unary_union
    from shapely.prepared import prep
    tp = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules/world-atlas/land-110m.json')))
    sc, tr = tp['transform']['scale'], tp['transform']['translate']
    arcs = []
    for arc in tp['arcs']:
        x = y = 0; pts = []
        for dx, dy in arc:
            x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
        arcs.append(pts)
    def ring(ix):
        out = []
        for i in ix:
            pts = arcs[i] if i >= 0 else arcs[~i][::-1]
            out += pts[1:] if out else pts
        return out
    geoms = []
    for g in tp['objects']['land']['geometries']:
        polys = g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]
        for poly in polys:
            rings = [ring(r) for r in poly]
            geoms.append(shape({'type': 'Polygon', 'coordinates': rings}).buffer(0))
    land = prep(unary_union(geoms))
    out = []
    lat = lat1
    while lat >= lat0:
        lon = lon0
        while lon <= lon1:
            if land.contains(Point(lon, lat)): out.append((lon, lat))
            lon += step
        lat -= step
    return out


def tour():
    s = Panel(600, INK, 'Every room on the Capvise Global calendar, drawn as a route across a world map. 2025, four rooms: Bali, Singapore, Dubai, Buenos Aires. 2026, thirteen rooms: Hong Kong twice, Cannes twice, Paris, Bali, Barcelona, Seoul, Singapore twice, Mumbai twice and London. 2027, sixteen on the calendar: Hong Kong, Cannes, Bangkok, Miami, Amsterdam, New York, Nashville, Bali, Hong Kong, San Francisco, Singapore, Las Vegas, Singapore, Bangkok, Dubai and Abu Dhabi.')
    W, H = s.W, s.H
    a = s.add
    lon0, lon1, lat0, lat1 = -132.0, 152.0, -46.0, 60.0
    mx0, mx1, my0 = 48, 952, 150
    kx = (mx1 - mx0) / (lon1 - lon0)
    XY = lambda c: (mx0 + (CITY[c][0] - lon0) * kx, my0 + (lat1 - CITY[c][1]) * kx)
    d = ''.join(f'M{f(mx0 + (lo - lon0) * kx)} {f(my0 + (lat1 - la) * kx)}h0' for lo, la in land_dots(2.0, lon0, lon1, lat0, lat1))
    a(f'<path d="{d}" stroke="#4F5943" stroke-width="3.6" stroke-linecap="round" fill="none"/>')

    def arc(p, q):
        (x1, y1), (x2, y2) = p, q
        dist = math.hypot(x2 - x1, y2 - y1)
        cxm, cym = (x1 + x2) / 2, (y1 + y2) / 2 - min(dist * 0.22, 80)
        L = 0; px_, py_ = x1, y1
        for i in range(1, 25):
            tt = i / 24
            qx = (1 - tt) ** 2 * x1 + 2 * (1 - tt) * tt * cxm + tt * tt * x2; qy = (1 - tt) ** 2 * y1 + 2 * (1 - tt) * tt * cym + tt * tt * y2
            L += math.hypot(qx - px_, qy - py_); px_, py_ = qx, qy
        return f'Q{f(cxm)} {f(cym)} {f(x2)} {f(y2)}', L

    # one continuous journey, split into a trail per year
    legs, arrive, prev, total = [], [], None, 0.0
    for yi, (yr, cnt, cities) in enumerate(YEARS):
        seq = [c for i, c in enumerate(cities) if i == 0 or cities[i - 1] != c]
        start = prev if prev else seq[0]
        dpath = 'M{} {}'.format(*map(f, XY(start))); L0 = total
        for c in (seq if prev else seq[1:]):
            seg, L = arc(XY(start), XY(c)); dpath += seg; total += L; start = c
            arrive.append((c, total))
        if not prev: arrive.insert(0, (seq[0], 0.0))
        legs.append((dpath, L0, total)); prev = seq[-1]
    T, RUN = 42.0, 95.0                       # seconds per loop; % of the loop spent travelling
    full = legs[0][0] + ''.join(l[0][l[0].index('Q'):] for l in legs[1:])
    for yi, (dpath, L0, L1) in enumerate(legs):
        p0, p1 = L0 / total * RUN, L1 / total * RUN
        nm = f'tr{yi}'
        stops = [(0, 'stroke-dashoffset:1;opacity:1')] if p0 > 0 else []
        stops += [(f'{p0:.2f}', 'stroke-dashoffset:1;opacity:1'), (f'{p1:.2f}', 'stroke-dashoffset:0;opacity:1'),
                  (f'{min(p1 + 2.5, 99.5):.2f}', 'stroke-dashoffset:0;opacity:0'), (100, 'stroke-dashoffset:0;opacity:0')]
        s.css.append(kf(nm, stops))
        a(f'<path d="{dpath}" pathLength="1" fill="none" stroke="{LAMP}" stroke-width="2" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1" style="animation:{nm} {T}s linear infinite"/>')
        # the year, set large in the open Pacific
        yn = f'yr{yi}'
        s.css.append(kf(yn, [(0, 'opacity:0')] * (p0 > 0) + [(f'{p0:.2f}', 'opacity:0'), (f'{p0 + 1.2:.2f}', 'opacity:1'), (f'{p1 - 0.2:.2f}', 'opacity:1'), (f'{min(p1 + 1, 99.9):.2f}', 'opacity:0'), (100, 'opacity:0')]))
        m = s.mark()
        s.text(52, 492, YEARS[yi][0], S5, 92, PAPER, ls=-0.05, feat=TNUM)
        s.text(58, 526, YEARS[yi][1], S5, 19, SAGE_L)
        s.group_since(m, f'<g style="opacity:{1 if yi == 2 else 0};animation:{yn} {T}s linear infinite">')
    # every city, pinging when the line arrives
    for c, L in arrive:
        x, y = XY(c)
        a(f'<g transform="translate({f(x)} {f(y)})"><circle class="pg" style="animation-delay:{L / total * RUN / 100 * T - T:.2f}s" r="4" fill="{LAMP}" opacity="0"/></g>')
    for c in CITY:
        x, y = XY(c)
        a(f'<circle cx="{f(x)}" cy="{f(y)}" r="3.7" fill="{SAGE_L}" stroke="{INK}" stroke-width="1.4"/>')
        dx, dy, an = LBL[c]
        s.text(x + dx, y + dy, c, S5, 14, PAPER, anchor=an)
    a(f'<g><circle r="11" fill="{LAMP}" opacity=".25"/><circle r="5" fill="#FFF8D8"/>'
      f'<animateMotion dur="{T}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;1;1" keyTimes="0;{RUN / 100};1" path="{full}"/></g>')
    s.text(53, 92, 'And sixteen more on the calendar.', S5, 44, PAPER, ls=-0.035)
    s.text(56, 126, 'Every room from 2025 to 2027, in the order they happen.', S4, 19.5, MUTE_D)
    s.text(W - 56, H - 40, 'luma.com/capvise', S4, 15, MUTE, anchor='end')
    s.css.append(f'.pg{{animation:pg {T}s ease-out infinite}}' + kf('pg', [(0, 'transform:scale(1);opacity:.9'), (6, 'transform:scale(5);opacity:0'), (100, 'transform:scale(5);opacity:0')]))
    return s


# ------------------------------------------------------------------ code cards
class Card(Panel):
    def __init__(self, H, bg, title):
        super().__init__(H, bg, title, r=26)
        self.W = 400


def card_text(s, title, lines, tags, fg, sub, tagc, y0=340):
    s.text(30, y0, title, S5, 35, fg, ls=-0.035)
    y = y0 + 34
    for ln in lines:
        s.text(31, y, ln, S4, 17.5, sub); y += 24
    s.text(31, s.H - 30, tags, S5, 14, tagc)


def window(inner, x, y, rot, cls=''):
    return (f'<g transform="translate({x} {y}) rotate({rot})"><rect x="3" y="6" width="176" height="126" rx="13" fill="#000" opacity=".18"/>'
            f'<rect width="176" height="126" rx="13" fill="{PAPER}"/>'
            f'<circle cx="15" cy="13" r="3.2" fill="{PAPER3}"/><circle cx="26" cy="13" r="3.2" fill="{PAPER3}"/><circle cx="37" cy="13" r="3.2" fill="{PAPER3}"/>'
            f'<rect x="9" y="25" width="158" height="74" rx="6" fill="{INK2}"/>'
            f'<circle cx="128" cy="50" r="13" fill="{LAMP}"/><path d="M9 99V84C40 62 62 70 84 82C104 66 132 64 167 80V93a6 6 0 0 1-6 6Z" fill="{SAGE_M}"/>'
            f'<path d="M9 99V90C46 76 70 82 100 92C124 84 146 84 167 90V93a6 6 0 0 1-6 6H15a6 6 0 0 1-6-6Z" fill="{SAGE}"/>'
            f'<rect x="12" y="109" width="152" height="5" rx="2.5" fill="{PAPER3}"/>'
            f'<g transform="translate(12 109)"><rect class="pr" width="152" height="5" rx="2.5" fill="{SAGE}"/></g>'
            f'<g class="kn"><circle cx="12" cy="111.5" r="6" fill="{INK2}"/></g>{inner}</g>')


def cwtch():
    s = Card(470, '#5D6B44', 'Cwtch. Private watch parties for two on Netflix, Prime Video and YouTube. Play, pause and seek stay in step. Open source, 2026.')
    a = s.add
    a(f'<circle cx="200" cy="150" r="170" fill="#6F7E53" opacity=".55"/>')
    a(window('', 22, 44, -6))
    a(window('', 200, 118, 5))
    heart = 'M0 6C-9 -2 -5 -9 0 -4C5 -9 9 -2 0 6Z'
    for i, (x, c) in enumerate(((182, LAMP), (214, PAPER), (198, LAMP))):
        a(f'<g transform="translate({x} 150)"><path class="ht" style="animation-delay:-{i * 1.3:.1f}s" d="{heart}" fill="{c}"/></g>')
    a(f'<g transform="translate(200 236)"><circle r="17" fill="{INK2}"/><rect x="-6.5" y="-2" width="13" height="10" rx="2.2" fill="{LAMP}"/>'
      f'<path d="M-4 -2v-3a4 4 0 0 1 8 0v3" fill="none" stroke="{LAMP}" stroke-width="2"/></g>')
    card_text(s, 'Cwtch', ['Watch parties for two. Play, pause', 'and seek stay in step.'], 'Chrome extension, 2026', PAPER, '#DDE3CC', LAMP)
    s.css.append('.pr{transform-origin:0 0;animation:pr 8s linear infinite}' + kf('pr', [(0, 'transform:scaleX(.04)'), (48, 'transform:scaleX(.62)'), (52, 'transform:scaleX(.22)'), (100, 'transform:scaleX(1)')])
                 + '.kn{animation:kn 8s linear infinite}' + kf('kn', [(0, 'transform:translateX(6px)'), (48, 'transform:translateX(94px)'), (52, 'transform:translateX(33px)'), (100, 'transform:translateX(152px)')])
                 + '.ht{animation:ht 3.9s ease-out infinite}' + kf('ht', [(0, 'transform:translateY(30px) scale(.8);opacity:0'), (15, 'opacity:1'), (70, 'opacity:1'), (100, 'transform:translateY(-120px) scale(2.6);opacity:0')]))
    return s


def omni():
    s = Card(470, INK, 'OmniSweep. A gas relayer that sweeps token dust into cash across chains, with nothing to pay upfront. Built at ETHGlobal Buenos Aires, 2025.')
    a = s.add
    a(f'<circle cx="200" cy="150" r="170" fill="{INK2}"/>')
    rng = random.Random(9)
    cx, cy = 92, 148
    specks = ''
    for i in range(22):
        ang = i * 2.39996 + rng.uniform(-.3, .3); r = 10 + 56 * math.sqrt((i + .5) / 22)
        specks += f'<circle cx="{f(cx + math.cos(ang) * r)}" cy="{f(cy + math.sin(ang) * r)}" r="{f(rng.uniform(2.2, 5.2))}" fill="{rng.choice([LAMP, SAGE_L, SAGE_M, PAPER])}"/>'
    # two chains and the bridge between them
    a(f'<rect x="28" y="214" width="138" height="12" rx="6" fill="{SAGE}"/><rect x="236" y="214" width="138" height="12" rx="6" fill="{SAGE}"/>')
    a(f'<path d="M150 214C170 150 230 150 252 214" fill="none" stroke="{SAGE_M}" stroke-width="2" stroke-dasharray="3 6" stroke-linecap="round"/>')
    a(f'<g class="sp2">{specks}</g>')
    # wallet
    a(f'<g transform="translate(306 168)"><g class="wl"><rect x="-34" y="-26" width="68" height="50" rx="9" fill="{PAPER}"/><rect x="-34" y="-26" width="68" height="15" rx="7" fill="{PAPER3}"/>'
      f'<rect x="10" y="-6" width="26" height="16" rx="8" fill="{SAGE}"/><circle cx="19" cy="2" r="3" fill="{PAPER}"/></g></g>')
    a(f'<g class="cmv"><g transform="translate({cx} {cy})"><g class="csc"><circle r="21" fill="{LAMP}"/><circle r="15" fill="none" stroke="#C9B866" stroke-width="2"/>'
      f'<path d="M0 -8V8M4.5 -4.5C2 -7.5 -5 -6.5 -5 -2.5S5 0 5 4 -2.5 8 -5 4.5" fill="none" stroke="#8C7E36" stroke-width="2.2" stroke-linecap="round"/></g></g></g>')
    card_text(s, 'OmniSweep', ['Sweeps token dust into cash,', 'with no gas to pay upfront.'], 'ETHGlobal Buenos Aires, 2025', PAPER, MUTE_D, LAMP)
    s.css.append(f'.sp2{{transform-origin:{cx}px {cy}px;animation:sp2 7s ease-in-out infinite}}' + kf('sp2', [(0, 'transform:scale(1) rotate(0);opacity:1'), (10, 'transform:scale(1) rotate(0);opacity:1'), (34, 'transform:scale(.05) rotate(200deg);opacity:1'), (36, 'transform:scale(.05) rotate(200deg);opacity:0'), (88, 'transform:scale(1) rotate(0);opacity:0'), (100, 'transform:scale(1) rotate(0);opacity:1')])
                 + '.csc{transform:scale(0);animation:csc 7s ease-in-out infinite}' + kf('csc', [(0, 'transform:scale(0)'), (30, 'transform:scale(0)'), (38, 'transform:scale(1)'), (74, 'transform:scale(1)'), (80, 'transform:scale(0)'), (100, 'transform:scale(0)')])
                 + '.cmv{animation:cmv 7s ease-in-out infinite}' + kf('cmv', [(0, 'transform:translate(0,0)'), (44, 'transform:translate(0,0)'), (52, 'transform:translate(70px,-34px)'), (60, 'transform:translate(110px,-52px)'), (68, 'transform:translate(160px,-30px)'), (76, 'transform:translate(214px,20px)'), (100, 'transform:translate(214px,20px)')])
                 + '.wl{animation:wl 7s ease-out infinite}' + kf('wl', [(0, 'transform:scale(1)'), (76, 'transform:scale(1)'), (80, 'transform:scale(1.14)'), (86, 'transform:scale(1)'), (100, 'transform:scale(1)')]))
    return s


def hyper():
    s = Card(470, PAPER, 'HyperSight Explorer. A real-time block explorer for Hyperliquid, with a whale tracker. Built for the HyperEVM Hackathon, 2025.')
    a = s.add
    a(f'<circle cx="200" cy="150" r="170" fill="{PAPER2}"/>')
    # live blocks sliding past a lens
    s.extra_defs.append('<clipPath id="bw"><rect x="0" y="30" width="400" height="80"/></clipPath>')
    b, pitch = 38, 58
    blocks = ''.join(f'<rect x="{-20 + i * pitch}" y="{70 - b / 2}" width="{b}" height="{b}" rx="7" fill="{SAGE_P}" stroke="{SAGE}" stroke-width="2"/>'
                     f'<path d="M{-20 + i * pitch + b} 70h{pitch - b}" stroke="{SAGE}" stroke-width="2"/>' for i in range(10))
    a(f'<g clip-path="url(#bw)"><g class="blk">{blocks}</g></g>')
    a(f'<circle cx="230" cy="70" r="33" fill="{LAMP}" opacity=".35"/><circle cx="230" cy="70" r="33" fill="none" stroke="{INK2}" stroke-width="4"/>'
      f'<path d="M254 94l22 22" stroke="{INK2}" stroke-width="7" stroke-linecap="round"/>')
    # sea and whale
    wave = lambda y, ph: 'M' + f'{-80 + ph} {y}' + ''.join(f'q20 -12 40 0t40 0' for _ in range(8))
    a(f'<path class="wv" d="{wave(196, 0)}" fill="none" stroke="{SAGE_M}" stroke-width="2.4" stroke-linecap="round"/>')
    whale = (f'<path d="M2 4C-12 -4 -22 -22 -36 -24C-31 -12 -31 -2 -22 6C-31 12 -34 22 -38 31C-22 29 -10 16 2 4Z" fill="{INK2}"/>'
             f'<path d="M0 0C20 -30 80 -44 122 -30C144 -23 153 -8 151 5C149 21 131 31 105 31C60 31 20 22 0 8Z" fill="{INK2}"/>'
             f'<path d="M151 7C147 22 131 31 105 31C68 31 34 25 12 15C54 22 112 24 151 7Z" fill="{SAGE_L}"/>'
             f'<circle cx="127" cy="0" r="2.8" fill="{PAPER}"/><path d="M84 22C80 34 68 40 60 38C66 32 68 26 70 20Z" fill="{INK3}"/>'
             f'<g transform="translate(108 -34)"><g class="spt"><path d="M0 0C-3 -14 -15 -19 -22 -10M0 0C3 -14 15 -19 22 -10M0 0V-17" fill="none" stroke="{SAGE}" stroke-width="2.6" stroke-linecap="round"/></g></g>')
    a(f'<g transform="translate(120 232)"><g class="wh">{whale}</g></g>')
    a(f'<path class="wv w2" d="{wave(262, 20)}" fill="none" stroke="{SAGE}" stroke-width="2.4" stroke-linecap="round"/>')
    a(f'<path class="wv w3" d="{wave(284, 0)}" fill="none" stroke="{SAGE_M}" stroke-width="2.4" stroke-linecap="round" opacity=".6"/>')
    card_text(s, 'HyperSight', ['A live block explorer for', 'Hyperliquid, with a whale tracker.'], 'HyperEVM Hackathon, 2025', INK2, MUTE, SAGE)
    s.css.append(f'.blk{{animation:blk 2.4s linear infinite}}@keyframes blk{{to{{transform:translateX(-{pitch}px)}}}}'
                 '.wv{animation:wv 3.2s linear infinite}@keyframes wv{to{transform:translateX(80px)}}.w2{animation-duration:4.4s}.w3{animation-duration:5.6s}'
                 '.wh{animation:wh 3.6s ease-in-out infinite alternate}@keyframes wh{from{transform:translateY(-5px) rotate(-2deg)}to{transform:translateY(6px) rotate(2deg)}}'
                 '.spt{transform-origin:0 0;animation:spt 3.6s ease-in-out infinite}' + kf('spt', [(0, 'transform:scale(.2);opacity:0'), (20, 'transform:scale(1);opacity:1'), (55, 'transform:scale(1.1);opacity:1'), (75, 'transform:scale(1.2);opacity:0'), (100, 'transform:scale(.2);opacity:0')]))
    return s



# ------------------------------------------------------------------ ventures
def ic_globe():
    return (f'<circle r="25" fill="{PAPER}" stroke="{INK2}" stroke-width="2.4"/><path d="M-25 0H25" stroke="{INK2}" stroke-width="2"/>'
            f'<ellipse class="mer" rx="11" ry="25" fill="none" stroke="{INK2}" stroke-width="2"/><ellipse class="mer m2" rx="11" ry="25" fill="none" stroke="{SAGE}" stroke-width="2"/>')


def ic_flask():
    return (f'<path d="M-8 -26h16M-5 -26v16L-21 18a5 5 0 0 0 4.5 7.5h33A5 5 0 0 0 21 18L5 -10v-16" fill="{PAPER}" stroke="{INK2}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="M-13.5 6h27L20 18a4 4 0 0 1-3.5 6h-33A4 4 0 0 1-20 18Z" fill="{SAGE_M}"/>'
            + ''.join(f'<circle class="bub" style="animation-delay:-{i * .7:.1f}s" cx="{x}" cy="2" r="{r}" fill="{SAGE}"/>' for i, (x, r) in enumerate(((-4, 3), (5, 2.2), (0, 2.6)))))


def ic_media():
    return (f'<circle cx="-16" cy="0" r="7" fill="{INK2}"/>'
            + ''.join(f'<path class="arc" style="animation-delay:{i * .28:.2f}s" d="M{-6 + i * 11} {-9 - i * 6}a{14 + i * 9} {14 + i * 9} 0 0 1 0 {18 + i * 12}" fill="none" stroke="{SAGE if i else INK2}" stroke-width="2.6" stroke-linecap="round"/>' for i in range(3)))


def ic_growth():
    return (''.join(f'<g transform="translate({-24 + i * 13} 24)"><rect class="bar" style="animation-delay:{i * .18:.2f}s" x="0" y="{-(12 + i * 11)}" width="9" height="{12 + i * 11}" rx="2.5" fill="{SAGE if i < 3 else INK2}"/></g>' for i in range(4))
            + f'<path d="M-26 24H28" stroke="{INK2}" stroke-width="2.4" stroke-linecap="round"/>')


def ic_events():
    return (f'<g transform="translate(-22 -26)"><path class="beam b1" d="M0 0L10 52H34Z" fill="{LAMP}" opacity=".8"/></g>'
            f'<g transform="translate(22 -26)"><path class="beam b2" d="M0 0L-10 52H-34Z" fill="{PAPER}" opacity=".85"/></g>'
            f'<circle cx="-22" cy="-26" r="5" fill="{INK2}"/><circle cx="22" cy="-26" r="5" fill="{INK2}"/><path d="M-28 26H28" stroke="{INK2}" stroke-width="2.6" stroke-linecap="round"/>')


def ic_network():
    P = [(-22, 16), (22, 16), (0, -22), (0, 4)]
    E = [(0, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]
    return (''.join(f'<path d="M{P[a][0]} {P[a][1]}L{P[b][0]} {P[b][1]}" stroke="{INK2}" stroke-width="1.6" opacity=".45"/>'
                    f'<path class="pulse" style="animation-delay:-{i * .45:.2f}s" d="M{P[a][0]} {P[a][1]}L{P[b][0]} {P[b][1]}" stroke="{SAGE}" stroke-width="2.8" stroke-linecap="round" pathLength="1" stroke-dasharray=".25 1"/>' for i, (a, b) in enumerate(E))
            + ''.join(f'<circle cx="{x}" cy="{y}" r="{6 if i < 3 else 5}" fill="{PAPER if i < 3 else SAGE}" stroke="{INK2}" stroke-width="2.2"/>' for i, (x, y) in enumerate(P)))


def ic_club():
    return ''.join(f'<g class="bob" style="animation-delay:-{i * .21:.2f}s">{person(x, y, c, 1.25, so=.12)}</g>' for i, (x, y, c) in enumerate(((-17, 16, SAGE), (17, 16, SAGE_M), (0, 24, INK2))))


def ic_door():
    return (f'<rect x="-17" y="-27" width="34" height="52" rx="2" fill="{LAMP}" stroke="{INK2}" stroke-width="2.4"/>'
            f'<g transform="translate(-17 0)"><g class="leaf"><path d="M0 -27L34 -27L34 25L0 25Z" fill="{PAPER}" stroke="{INK2}" stroke-width="2.4" stroke-linejoin="round"/><circle cx="27" cy="1" r="2.4" fill="{INK2}"/></g></g>'
            f'<path d="M-28 25H28" stroke="{INK2}" stroke-width="2.4" stroke-linecap="round"/>')


VENT = [('Capvise Global', 'Capital', ic_globe), ('Capvise Labs', 'Technology', ic_flask), ('Capvise Media', 'Media', ic_media), ('Capvise Growth', 'Marketing', ic_growth),
        ('Capvise Events', 'Events', ic_events), ('Creator Network', 'Creators', ic_network), ('Capvise Club', 'Communities', ic_club), ('The Rejected Club', 'Founders', ic_door)]


def group():
    s = Panel(560, '#DCE2CA', 'One group, eight ventures: Capvise Global (capital), Capvise Labs (technology), Capvise Media (media), Capvise Growth (marketing), Capvise Events (events), Creator Network (creators), Capvise Club (communities) and The Rejected Club (founders).')
    W, H = s.W, s.H
    a = s.add
    s.text(53, 92, 'One group, eight ventures.', S5, 44, INK2, ls=-0.035)
    cw, ch, x0, y0 = 223.5, 196, 53, 132
    for i, (name, dom, ic) in enumerate(VENT):
        cx, cy = x0 + (i % 4) * cw, y0 + (i // 4) * ch
        a(f'<rect x="{f(cx)}" y="{cy}" width="{cw - 12}" height="{ch - 12}" rx="18" fill="{"#EEF1E2" if i else PAPER}"/>')
        a(f'<g transform="translate({f(cx + 58)} {cy + 62}) scale(1.35)">{ic()}</g>')
        s.text(cx + 20, cy + 142, name, S5, 20, INK2, ls=-0.02)
        s.text(cx + 20, cy + 165, dom, PI, 17, SAGE)
    s.css.append('.mer{animation:mer 3.2s linear infinite}@keyframes mer{0%{transform:scaleX(2.27)}50%{transform:scaleX(0)}100%{transform:scaleX(2.27)}}.m2{animation-delay:-1.6s}'
                 '.bub{animation:bub 2.1s ease-in infinite}@keyframes bub{0%{transform:translateY(14px);opacity:0}25%{opacity:1}100%{transform:translateY(-34px);opacity:0}}'
                 '.arc{animation:arc 1.7s ease-in-out infinite}@keyframes arc{0%,100%{opacity:.15}40%{opacity:1}}'
                 '.bar{transform-origin:0 0;animation:bar 2.6s ease-in-out infinite}@keyframes bar{0%,100%{transform:scaleY(.25)}45%,75%{transform:scaleY(1)}}'
                 '.beam{transform-origin:0 0;animation:beam 3.4s ease-in-out infinite alternate}@keyframes beam{from{transform:rotate(-9deg)}to{transform:rotate(9deg)}}.b2{animation-delay:-1.7s}'
                 '.pulse{animation:pulse 2.7s linear infinite}@keyframes pulse{from{stroke-dashoffset:1.25}to{stroke-dashoffset:0}}'
                 '.bob{animation:bob .52s ease-in-out infinite alternate}@keyframes bob{to{transform:translateY(-2.4px)}}'
                 '.leaf{transform-origin:0 0;animation:leaf 4s ease-in-out infinite}@keyframes leaf{0%,15%{transform:skewY(0) scaleX(1)}45%,70%{transform:skewY(-14deg) scaleX(.42)}100%{transform:skewY(0) scaleX(1)}}')
    return s


# ------------------------------------------------------------------ path
def path_():
    s = Panel(430, PAPER, 'The path so far. 2023: started shipping full-stack products. 2024: AI engineering with open-source image and video models, and data annotation at Innodata. 2025: founded Capvise Group, COO at BackersStage, four rooms in four countries, built OmniSweep at ETHGlobal Buenos Aires. 2026: thirteen rooms, sat on the evaluation panel at Claude Impact Lab and open-sourced Cwtch.')
    W, H = s.W, s.H
    a = s.add
    s.runs(53, 92, [('Builder first. ', S5, INK2), ('Then rooms.', S5, SAGE)], 44, ls=-0.035)
    xs = [140, 380, 620, 860]; base = 232
    road = f'M-20 {base + 30}C60 {base + 30} 80 {base} {xs[0]} {base}S300 {base - 34} {xs[1]} {base - 12}S540 {base + 30} {xs[2]} {base + 6}S780 {base - 40} {xs[3]} {base - 18}S1000 {base + 10} 1040 {base - 6}'
    ys = [base, base - 12, base + 6, base - 18]
    a(f'<path d="{road}" fill="none" stroke="{PAPER3}" stroke-width="14" stroke-linecap="round"/>')
    a(f'<path d="{road}" fill="none" stroke="{PAPER}" stroke-width="2" stroke-dasharray="2 12" stroke-linecap="round"/>')
    icons = []
    icons.append(f'<rect x="-30" y="-24" width="60" height="44" rx="8" fill="{INK2}"/><path d="M-9 -10l-9 8 9 8M9 -10l9 8-9 8M4 -14l-8 24" fill="none" stroke="{LAMP}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    icons.append(f'<rect x="-20" y="-28" width="52" height="40" rx="7" fill="{SAGE_L}" transform="rotate(8)"/><rect x="-30" y="-22" width="54" height="42" rx="7" fill="{SAGE}"/>'
                 f'<circle cx="10" cy="-9" r="6" fill="{LAMP}"/><path d="M-30 14V8L-12 -6 2 6 10 0 24 12v2a6 6 0 0 1-6 6H-24a6 6 0 0 1-6-6Z" fill="{SAGE_P}"/>'
                 f'<path class="tw" d="M30 -30l2.6 7 7 2.6-7 2.6-2.6 7-2.6-7-7-2.6 7-2.6Z" fill="{INK2}"/>')
    iso = Iso(0, -26, 17)
    icons.append(iso.box(0, 0, -0.2, 2.4, 2.4, 0.2, '#FFFFFF', '#C9C9BB', '#B5B5A6') + iso.box(-0.16, 0, -0.2, 0.16, 2.4, 2.0, '#93A374', '#6B7A4F', '#55633E')
                 + iso.box(-0.16, -0.16, -0.2, 2.56, 0.16, 2.0, '#93A374', '#6B7A4F', '#4A5736')
                 + ''.join(f'<g class="bob" style="animation-delay:-{i * .2}s">{person(*iso.p(x, y), c, 0.72, so=.12)}</g>' for i, (x, y, c) in enumerate(((0.8, 0.9, SAGE), (1.7, 1.0, INK2), (1.2, 1.8, SAGE)))))
    icons.append(f'<rect x="-34" y="-2" width="68" height="20" rx="5" fill="{INK2}"/>'
                 + ''.join(f'<g class="bob" style="animation-delay:-{i * .25}s"><rect x="{x - 7}" y="-22" width="14" height="24" rx="7" fill="{c}"/><circle cx="{x}" cy="-28" r="6.6" fill="{c}"/></g>' for i, (x, c) in enumerate(((-20, SAGE), (0, SAGE_M), (20, SAGE))))
                 + f'<rect x="-34" y="-2" width="68" height="20" rx="5" fill="{INK2}"/><path d="M-8 8l5 5 10-10" fill="none" stroke="{LAMP}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    notes = [('2023', ['Started shipping', 'full-stack products']), ('2024', ['AI engineering: open-source', 'image and video models']),
             ('2025', ['Founded Capvise Group.', 'Four rooms. OmniSweep.']), ('2026', ['Thirteen rooms. Cwtch.', 'Claude Impact Lab panel.'])]
    for i, (x, y) in enumerate(zip(xs, ys)):
        a(f'<path d="M{x} {y}v-34" stroke="{INK2}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="8" fill="{PAPER}" stroke="{INK2}" stroke-width="3"/>'
          f'<circle class="png" style="animation-delay:{i * 3 - 12}s" cx="{x}" cy="{y}" r="8" fill="none" stroke="{SAGE}" stroke-width="2.4"/>')
        a(f'<g transform="translate({x} {y - 66})">{icons[i]}</g>')
        yr, lines = notes[i]
        s.text(x, y + 62, yr, S5, 30, INK2, ls=-0.03, anchor='middle', feat=TNUM)
        for j, ln in enumerate(lines):
            s.text(x, y + 88 + j * 21, ln, S4, 15.5, MUTE, anchor='middle')
    a(f'<g><circle r="13" fill="{SAGE}" opacity=".25"/><circle r="6.5" fill="{SAGE}"/><animateMotion dur="12s" repeatCount="indefinite" path="{road}"/></g>')
    s.css.append('.bob{animation:bob .52s ease-in-out infinite alternate}@keyframes bob{to{transform:translateY(-2px)}}'
                 '.tw{transform-origin:30px -20px;animation:tw 1.8s ease-in-out infinite alternate}@keyframes tw{from{transform:scale(.5) rotate(-20deg)}to{transform:scale(1.15) rotate(10deg)}}'
                 '.png{transform-box:fill-box;transform-origin:center;animation:png 12s ease-out infinite}' + kf('png', [(0, 'transform:scale(1);opacity:0'), (6, 'transform:scale(1);opacity:1'), (22, 'transform:scale(3.4);opacity:0'), (100, 'transform:scale(3.4);opacity:0')]))
    return s


# ------------------------------------------------------------------ tools strip and contact
TOOLS1 = ['TypeScript', 'Next.js', 'React', 'Node.js', 'PostgreSQL', 'MongoDB', 'Redis', 'Prisma', 'Docker', 'AWS', 'Cloudflare']
TOOLS2 = ['Python', 'Stable Diffusion', 'ComfyUI', 'AnimateDiff', 'Segment Anything 2', 'Solidity', 'LayerZero V2', '1inch', 'ethers.js', 'Vercel']


def band(s, words, y, col, dotc, cls, size=33):
    m = s.mark(); x = 0
    for rep in range(2):
        for wd in words:
            x += s.text(x, y, wd, S5, size, col, ls=-0.02) + 22
            s.add(f'<circle cx="{f(x)}" cy="{f(y - size * .3)}" r="4" fill="{dotc}"/>'); x += 26
        if rep == 0: period = x
    s.group_since(m, f'<g class="{cls}">')
    return period


def stack():
    s = Panel(150, INK, 'Tools: ' + ', '.join(TOOLS1 + TOOLS2) + '.')
    p1 = band(s, TOOLS1, 66, '#8B9774', SAGE, 'mq1')
    p2 = band(s, TOOLS2, 116, '#5F6A4E', SAGE_D, 'mq2')
    s.css.append(f'.mq1{{animation:mq1 46s linear infinite}}@keyframes mq1{{to{{transform:translateX(-{f(p1)}px)}}}}'
                 f'.mq2{{transform:translateX(-{f(p2)}px);animation:mq2 54s linear infinite}}@keyframes mq2{{to{{transform:translateX(0)}}}}')
    return s


def contact():
    s = Panel(350, INK, 'Building something, or raising for it? Write to sahil@capvise.group.')
    W, H = s.W, s.H
    a = s.add
    s.extra_defs.append(f'<linearGradient id="spl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{LAMP}" stop-opacity="0"/><stop offset="1" stop-color="{LAMP}" stop-opacity=".5"/></linearGradient>'
                        '<radialGradient id="dg"><stop offset="0" stop-color="#5A6340" stop-opacity=".9"/><stop offset="1" stop-color="#171A14" stop-opacity="0"/></radialGradient>'
                        f'<linearGradient id="dl2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF8D6"/><stop offset="1" stop-color="{LAMP}"/></linearGradient>')
    dx, dy = 838, 92
    a(f'<ellipse cx="{dx + 40}" cy="{dy + 90}" rx="260" ry="200" fill="url(#dg)"/>')
    a(f'<path class="glow" d="M{dx} {dy + 176}L{dx - 250} {dy + 232}H{dx + 30}L{dx + 84} {dy + 176}Z" fill="url(#spl)"/>')
    a(f'<rect x="{dx - 8}" y="{dy - 8}" width="100" height="184" rx="4" fill="{SAGE_D}"/><rect x="{dx}" y="{dy}" width="84" height="176" fill="url(#dl2)"/>')
    a(f'<path d="M{dx + 84} {dy}l52 22v176l-52 -22Z" fill="{SAGE}"/><circle cx="{dx + 124}" cy="{dy + 112}" r="4" fill="{LAMP}"/>')
    for i in range(3):
        a(f'<g class="wk" style="animation-delay:-{i * 3:.1f}s"><g class="bob">{person(dx + 42, dy + 190, INK2 if i % 2 else SAGE_D, 1.9, so=.25)}</g></g>')
    s.text(56, 132, 'Building something, or raising for it?', S4, 21, MUTE_D)
    s.text(53, 196, 'Write to', S5, 58, PAPER, ls=-0.04)
    s.text(53, 262, 'sahil@capvise.group', S5, 58, SAGE_L, ls=-0.04)
    s.css.append('.glow{animation:glow 4s ease-in-out infinite alternate}@keyframes glow{from{opacity:.6}to{opacity:1}}'
                 '.bob{animation:bob .5s ease-in-out infinite alternate}@keyframes bob{to{transform:translateY(-3px)}}'
                 '.wk{animation:wk 9s linear infinite}' + kf('wk', [(0, 'transform:translate(-330px,58px) scale(1.25);opacity:0'), (8, 'opacity:1'), (78, 'transform:translate(-20px,0) scale(1);opacity:1'), (92, 'transform:translate(0,-6px) scale(.94);opacity:0'), (100, 'transform:translate(0,-6px) scale(.94);opacity:0')]))
    return s


SCENES = {'hero': hero, 'path': path_, 'cwtch': cwtch, 'omnisweep': omni, 'hypersight': hyper, 'stack': stack, 'rooms': rooms, 'tour': tour, 'group': group, 'contact': contact}

if __name__ == '__main__':
    only = sys.argv[1:]
    for name, fn in SCENES.items():
        if only and name not in only: continue
        svg = fn().svg()
        open(f'{OUT}/{name}.svg', 'w').write(svg)
        print(name, len(svg) // 1024, 'KB')
