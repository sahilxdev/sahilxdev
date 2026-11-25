"""The sheets. Run: python3 sheets.py  ->  out/<name>-<theme>.svg"""
import math, os, random
from kit import Sheet, S4, S5, S6, PI, LIGHT, DARK, TNUM, f

OUT = os.environ.get('SHEETS_OUT') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
os.makedirs(OUT, exist_ok=True)
DOOR_X, DOOR_W = 120, 60        # the door that runs down through every sheet
M = 64                          # content margin


def poisson(rng, x0, y0, x1, y1, dmin, n, avoid=()):
    pts, tries = [], 0
    while len(pts) < n and tries < 20000:
        tries += 1
        p = (rng.uniform(x0, x1), rng.uniform(y0, y1))
        if any(math.dist(p, q) < dmin for q in pts): continue
        if any(ax0 <= p[0] <= ax1 and ay0 <= p[1] <= ay1 for ax0, ay0, ax1, ay1 in avoid): continue
        pts.append(p)
    return pts


# ---------------------------------------------------------------- entrance
def entrance(c):
    s = Sheet(600, c, 'Sahil Meena. Founder and CEO, Capvise Group. I build the rooms where builders meet capital.')
    W, H, T = s.W, s.H, s.T
    dy0, dw = 418, 64
    s.walls([('left', dy0, dw, None), ('right', dy0, dw, None), ('bottom', DOOR_X, DOOR_W, 'L')])
    # the two entrances, leaves swing in on load
    s.door('left', dy0, dw, 'L', cls='lf l1')
    s.door('right', dy0, dw, 'L', cls='lf l2')

    s.text(55, 206, 'Sahil Meena', S5, 158, c['ink'], ls=-0.058)
    s.add(f'<circle cx="{M + 5}" cy="255" r="5" fill="{c["sage"]}"/>')
    s.text(M + 20, 262, 'Founder and CEO, Capvise Group', S6, 21, c['ink'], ls=-0.005)
    s.runs(M - 2, 334, [('I build the rooms where ', S4, c['mute']), ('builders', PI, c['sage']),
                        (' meet capital.', S4, c['mute'])], 43, ls=-0.022)

    s.text(22, dy0 - 14, 'builders', PI, 23, c['sage'])
    s.text(W - 22, dy0 - 14, 'capital', PI, 23, c['ink'], anchor='end')

    rng = random.Random(11)
    avoid = [(0, dy0 - 40, 92, dy0 + dw + 14), (W - 92, dy0 - 40, W, dy0 + dw + 14),
             (DOOR_X - 20, H - 96, DOOR_X + DOOR_W + 26, H), (W - 250, H - 62, W, H)]
    pts = poisson(rng, 104, 400, W - 104, 550, 54, 34, avoid)
    pts.sort(key=lambda p: abs(p[0] - W / 2), reverse=True)
    r = 6.2
    door_l = (T + 2, dy0 + dw / 2); door_r = (W - T - 2, dy0 + dw / 2)
    for i, (x, y) in enumerate(pts):
        a = rng.uniform(0, math.pi)
        ox, oy = math.cos(a) * (r + 0.9), math.sin(a) * (r + 0.9)
        if ox > 0: ox, oy = -ox, -oy          # builder always on the door side it came from
        bx, by, cx, cy = x + ox, y + oy, x - ox, y - oy
        delay = 0.55 + i * 0.075 + rng.uniform(0, 0.12)
        for (px, py, door, fill) in ((bx, by, door_l, c['sage']), (cx, cy, door_r, c['ink'])):
            dur = 1.5 + math.dist((px, py), door) / 520
            s.add(f'<circle class="d" cx="{f(px)}" cy="{f(py)}" r="{r}" fill="{fill}" '
                  f'style="--x:{f(door[0] - px)}px;--y:{f(door[1] - py)}px;animation-delay:{delay:.2f}s;animation-duration:{dur:.2f}s"/>')

    s.text(W - M, H - 30, 'sahil.capvise.group', S4, 15.5, c['mute'], anchor='end')

    s.css.append(
        '.d{animation-name:in;animation-timing-function:cubic-bezier(.2,.7,.2,1);animation-fill-mode:both}'
        '@keyframes in{0%{transform:translate(var(--x),var(--y));opacity:0}12%{opacity:1}100%{transform:none;opacity:1}}'
        f'.lf{{animation:sw .9s cubic-bezier(.3,.8,.3,1) both}}.l1{{transform-origin:{T}px {dy0}px}}.l2{{transform-origin:{W - T}px {dy0}px}}'
        '@keyframes sw{from{transform:rotate(var(--r))}to{transform:none}}.l1{--r:90deg}.l2{--r:-90deg}'
        '@media (prefers-reduced-motion:reduce){.d,.lf{animation:none}}')
    return s


# ---------------------------------------------------------------- rooms 2025
ROOMS = [
    ('Bali', 'August', 100, 600, 'Founder × VC Happy Hour', 'alongside Coinfest Asia', '100+ seats', '600+ applied'),
    ('Singapore', 'September', 500, 4000, 'Founder × VC Summit', 'alongside TOKEN2049', '500 seats', '4,000+ applied'),
    ('Dubai', 'October', 150, 600, 'Founder × VC Happy Hour', 'alongside Blockchain Life', '150+ seats', '600+ applied'),
    ('Buenos Aires', 'November', 200, 1200, 'Somnia Dev City', 'alongside Devconnect Argentina', '200 seats', '1,200+ applied'),
]


def rooms(c):
    s = Sheet(930, c, 'Four rooms in four countries in four months of 2025. One dot is one person: 950 seats inside the rooms, 6,400 applications at the doors. Bali, Singapore, Dubai, Buenos Aires.')
    W, H = s.W, s.H
    s.walls([('top', DOOR_X, DOOR_W, None), ('bottom', DOOR_X, DOOR_W, 'L')])
    s.text(M - 3, 104, 'Four rooms, four countries, four months.', S5, 47, c['ink'], ls=-0.035)
    x = s.runs(M, 142, [('One dot is one person. In 2025, ', S4, c['mute']), ('950 had a seat', S6, c['sage']),
                        (' and ', S4, c['mute']), ('6,400 applied', S6, c['ink']), ('.', S4, c['mute'])], 19.5)

    p = 5; rows = 10
    s.extra_defs.append(f'<pattern id="q" width="{p}" height="{p}" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.45" fill="{c["ink"]}" opacity="{0.62 if c["name"] == "light" else 0.5}"/></pattern>')
    s.extra_defs.append(f'<pattern id="st" width="{p}" height="{p}" patternUnits="userSpaceOnUse"><rect x="0.9" y="0.9" width="3.2" height="3.2" rx="0.6" fill="{c["sage"]}"/></pattern>')
    xs = [65, 260, 620, 815]
    top = 262
    for (city, month, seats, apps, ev, along, seat_l, app_l), x0 in zip(ROOMS, xs):
        cols = seats // rows
        w = cols * p
        qrows = apps // cols
        # label
        s.text(x0 - 1, top - 50, city, S5, 27, c['ink'], ls=-0.02)
        s.text(x0, top - 27, month, S4, 15.5, c['mute'])
        # the room: wall, seats, door
        pad = 5; rx0, ry0, rw, rh = x0 - pad, top - pad, w + 2 * pad, rows * p + 2 * pad
        dwid = 14; dx = x0 + w / 2 - dwid / 2
        s.add(f'<path d="M{f(dx)} {f(ry0 + rh)}H{f(rx0)}V{f(ry0)}H{f(rx0 + rw)}V{f(ry0 + rh)}H{f(dx + dwid)}" fill="none" stroke="{c["wall"]}" stroke-width="2.2"/>')
        s.add(f'<path d="M{f(dx)} {f(ry0 + rh)}v{-dwid}" stroke="{c["wall"]}" stroke-width="1.1"/>'
              f'<path d="M{f(dx)} {f(ry0 + rh - dwid)}a{dwid} {dwid} 0 0 1 {dwid} {dwid}" fill="none" stroke="{c["faint"]}" stroke-width="0.8"/>')
        s.add(f'<rect x="{x0}" y="{top}" width="{w}" height="{rows * p}" fill="url(#st)"/>')
        qy = top + rows * p + pad + 15
        s.add(f'<rect x="{x0}" y="{qy}" width="{w}" height="{qrows * p}" fill="url(#q)"/>')
        # note hanging under the crowd
        ny = qy + qrows * p + 28
        s.text(x0, ny, app_l, S6, 16.5, c['ink'])
        s.text(x0, ny + 22, 'for ' + seat_l, S4, 16.5, c['sage'])
        yy = ny + 52
        for ln in s.wrap(ev + ',', S4, 15, 190):
            s.text(x0, yy, ln, S4, 15, c['mute']); yy += 20
        for ln in s.wrap(along, S4, 15, 150 if city == 'Buenos Aires' else 190):
            s.text(x0, yy, ln, S4, 15, c['mute']); yy += 20

    # speakers, set in the space the short crowds leave open
    s.para(620, H - 118, 'Twelve speakers took the stage, from Animoca Brands, Venom Foundation, Camp Network, Manta Network, Bitcoin.com, Somnia Network and others.',
           S4, 16.5, c['mute'], 316, 23)
    return s



# ---------------------------------------------------------------- 2027
Y27 = [('Feb', 'Whiskey & Whales', 'Hong Kong', 114.2), ('Apr', 'Curators & Allocators', 'Cannes', 7.0),
       ('Apr', 'ASEAN Rails', 'Bangkok', 100.5), ('May', 'Whiskey & Whales', 'Miami', -80.2),
       ('May', 'The MiCA Table', 'Amsterdam', 4.9), ('Jun', 'After the Bell', 'New York', -74.0),
       ('Jul', 'Hash & Capital', 'Nashville', -86.8), ('Aug', 'Whiskey & Whales', 'Bali', 115.2),
       ('Aug', 'Family Office Table', 'Hong Kong', 114.2), ('Aug', 'Agents & Apps', 'San Francisco', -122.4),
       ('Oct', 'Asia Capital Night', 'Singapore', 103.8), ('Oct', 'Agentic Commerce', 'Las Vegas', -115.1),
       ('Nov', 'Tokenised Funds', 'Singapore', 103.8), ('Nov', 'Whiskey & Whales', 'Bangkok', 100.5),
       ('Dec', 'Whiskey & Whales', 'Dubai', 55.3), ('Dec', 'Sovereign Capital', 'Abu Dhabi', 54.4)]


def y2027(c):
    s = Sheet(836, c, 'Sixteen rooms on the 2027 calendar, in thirteen cities from Hong Kong in February to Abu Dhabi in December, drawn by longitude.')
    W, H = s.W, s.H
    s.walls([('top', DOOR_X, DOOR_W, None), ('bottom', DOOR_X, DOOR_W, 'L')])
    s.text(M - 3, 104, 'Sixteen rooms on the 2027 calendar.', S5, 47, c['ink'], ls=-0.035)
    s.text(M, 142, 'Thirteen cities, February to December, drawn by longitude.', S4, 19.5, c['mute'])
    px0, px1, l0, l1 = 596, 928, -130.0, 125.0
    X = lambda lon: px0 + (lon - l0) * (px1 - px0) / (l1 - l0)
    top, rh = 232, 33
    bot = top + rh * (len(Y27) - 1)
    for lon, lab in ((-120, '120°W'), (-60, '60°W'), (0, '0°'), (60, '60°E'), (120, '120°E')):
        s.line(X(lon), top - 22, X(lon), bot + 20, c['line'], 1)
        s.text(X(lon), top - 32, lab, S4, 13.5, c['mute'], anchor='middle', feat=TNUM)
    pts = []; last = None
    for i, (mo, ev, city, lon) in enumerate(Y27):
        y = top + i * rh
        if mo != last:
            s.text(M, y + 6, mo, S4, 16, c['mute']); last = mo
            if i: s.line(M, y - rh / 2, 560, y - rh / 2, c['line'], 1)
        s.text(M + 58, y + 6, ev, S5, 18.5, c['ink'], ls=-0.01)
        s.text(332, y + 6, city, S4, 18.5, c['mute'], ls=-0.01)
        pts.append((X(lon), y))
    d = 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts)
    s.add(f'<path d="{d}" fill="none" stroke="{c["ink2"]}" stroke-width="1.3" stroke-linejoin="round"/>')
    for x, y in pts:
        s.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="5.6" fill="{c["sage"]}" stroke="{c["paper"]}" stroke-width="2.4"/>')
    s.text(W - M, H - 30, 'luma.com/capvise', S4, 15.5, c['mute'], anchor='end')
    return s


# ---------------------------------------------------------------- code
RM = '@media (prefers-reduced-motion:reduce){*{animation:none!important}}'


def work(c, title, alt, meta, desc, stack, fig):
    s = Sheet(262, c, alt)
    W, H = s.W, s.H
    s.walls([('top', DOOR_X, DOOR_W, None), ('bottom', DOOR_X, DOOR_W, None)])
    s.text(M - 2, 90, title, S5, 44, c['ink'], ls=-0.035)
    y = s.para(M, 128, desc, S4, 18, c['mute'], 520, 25.5)
    s.text(M, y + 8, stack, S4, 15, c['ink2'])
    s.text(W - M, 50, meta, S4, 15, c['mute'], anchor='end')
    fig(s, c)
    s.css.append(RM)
    return s


def fig_cwtch(s, c):
    x0, x1, ya, yb = 656, 932, 122, 180
    for y, lab in ((ya, 'You'), (yb, 'Them')):
        s.text(x0, y - 16, lab, S4, 14, c['mute'])
        s.line(x0, y, x1, y, c['faint'], 1.2)
        for i in range(0, 13):
            xx = x0 + i * (x1 - x0) / 12
            s.line(xx, y - 3, xx, y + 3, c['faint'], 1)
    s.add(f'<g class="ph"><path d="M{x0} {ya}V{yb}" stroke="{c["sage"]}" stroke-width="1.2" stroke-dasharray="2 4"/>'
          f'<circle cx="{x0}" cy="{ya}" r="7.5" fill="{c["ink"]}"/><circle cx="{x0}" cy="{yb}" r="7.5" fill="{c["sage"]}"/></g>')
    span = x1 - x0
    s.css.append(f'.ph{{transform:translateX({span * .42:.0f}px);animation:ph 9s linear infinite}}'
                 f'@keyframes ph{{0%{{transform:translateX(0)}}52%{{transform:translateX({span * .62:.0f}px)}}'
                 f'56%{{transform:translateX({span * .25:.0f}px)}}100%{{transform:translateX({span}px)}}}}')


def fig_omni(s, c):
    cx, cy = 706, 146
    rng = random.Random(7)
    specks = ''
    for i in range(18):
        a = i * 2.39996 + rng.uniform(-.25, .25); r = 12 + 44 * math.sqrt((i + .6) / 18)
        specks += f'<circle cx="{f(cx + math.cos(a) * r)}" cy="{f(cy + math.sin(a) * r * .82)}" r="{f(rng.uniform(1.7, 3.6))}"/>'
    s.add(f'<g class="sp" fill="{c["ink"]}">{specks}</g>')
    # the bridge between two chains
    bx = 808
    s.line(bx, cy - 40, bx, cy + 40, c['faint'], 1.2); s.line(bx + 22, cy - 40, bx + 22, cy + 40, c['faint'], 1.2)
    s.line(bx - 22, cy, bx + 44, cy, c['faint'], 1, dash='2 4')
    s.add(f'<circle cx="904" cy="{cy}" r="17" fill="none" stroke="{c["sage"]}" stroke-width="1.4"/>')
    s.add(f'<g class="cm"><circle class="cn" cx="{cx}" cy="{cy}" r="11" fill="{c["sage"]}"/></g>')
    s.text(cx, cy + 72, 'dust', S4, 14, c['mute'], anchor='middle')
    s.text(904, cy + 72, 'cash', S4, 14, c['mute'], anchor='middle')
    s.css.append(f'.sp{{transform-origin:{cx}px {cy}px;animation:sp 8s ease-in-out infinite}}'
                 '@keyframes sp{0%,8%{transform:scale(1);opacity:1}32%{transform:scale(.06);opacity:1}36%,88%{transform:scale(.06);opacity:0}100%{transform:scale(1);opacity:1}}'
                 f'.cn{{transform-origin:{cx}px {cy}px;transform:scale(0);animation:cn 8s ease-in-out infinite}}'
                 '@keyframes cn{0%,28%{transform:scale(0)}38%,84%{transform:scale(1)}90%,100%{transform:scale(0)}}'
                 f'.cm{{animation:cm 8s ease-in-out infinite}}@keyframes cm{{0%,42%{{transform:translateX(0)}}74%,100%{{transform:translateX({904 - cx}px)}}}}')


def fig_hyper(s, c):
    x0, x1, cy, b, pitch = 656, 932, 150, 30, 46
    s.extra_defs.append(f'<clipPath id="cw"><rect x="{x0}" y="{cy - 40}" width="{x1 - x0}" height="80"/></clipPath>')
    blocks = ''
    for i in range(9):
        x = x0 + i * pitch
        blocks += f'<rect x="{x}" y="{cy - b / 2}" width="{b}" height="{b}" rx="2" fill="none" stroke="{c["ink2"]}" stroke-width="1.4"/>'
        blocks += f'<path d="M{x + b} {cy}h{pitch - b}" stroke="{c["faint"]}" stroke-width="1.2"/>'
    s.add(f'<g clip-path="url(#cw)"><g class="bl">{blocks}</g></g>')
    hx = x0 + 4 * pitch + b / 2
    s.add(f'<circle cx="{hx}" cy="{cy}" r="29" fill="none" stroke="{c["sage"]}" stroke-width="1.6"/>'
          f'<path d="M{hx + 21} {cy + 21}l16 16" stroke="{c["sage"]}" stroke-width="2.4" stroke-linecap="round"/>')
    s.css.append(f'.bl{{animation:bl 2.6s linear infinite}}@keyframes bl{{to{{transform:translateX(-{pitch}px)}}}}')


def builder(c):
    s = Sheet(214, c, 'Builder first. Then rooms. Full-stack products since 2023, hands-on with open-source image and video models, and still shipping code.')
    s.walls([('top', DOOR_X, DOOR_W, None), ('bottom', DOOR_X, DOOR_W, None)])
    s.runs(M - 3, 104, [('Builder first. ', S5, c['ink']), ('Then rooms.', S5, c['mute'])], 47, ls=-0.035)
    s.text(M, 144, 'Full-stack products since 2023, hands-on with open-source image and video models,', S4, 19.5, c['mute'])
    s.text(M, 171, 'and still shipping code. Three rooms of it follow.', S4, 19.5, c['mute'])
    return s


def cwtch(c):
    return work(c, 'Cwtch', 'Cwtch: private watch parties for two on Netflix, Prime Video and YouTube. Open source.',
                'Open source, 2026',
                'Private watch parties for two on Netflix, Prime Video and YouTube. Play, pause and seek stay in step, and room messages are encrypted before they leave the browser.',
                'Chrome extension, JavaScript, Node.js relay, AES-GCM', fig_cwtch)


def omni(c):
    return work(c, 'OmniSweep', 'OmniSweep: a gas relayer for wallets holding token dust and no gas. Built at ETHGlobal Buenos Aires, 2025.',
                'ETHGlobal Buenos Aires, 2025',
                'A gas relayer for wallets holding token dust and no gas to move it. It fronts the gas, repays itself from the swap and bridges what is left across chains.',
                'Solidity, LayerZero V2, 1inch, Next.js, ethers.js', fig_omni)


def hyper(c):
    return work(c, 'HyperSight Explorer', 'HyperSight Explorer: a real-time block explorer for Hyperliquid. Built for the HyperEVM Hackathon, 2025.',
                'HyperEVM Hackathon, 2025',
                'A real-time block explorer for Hyperliquid, with live blocks and transactions, hash-aware search and a whale tracker.',
                'Next.js, TypeScript, TanStack Query, Lava RPC', fig_hyper)


# ---------------------------------------------------------------- group
VENT = [('Capvise Global', 'Capital', 'Founder and investor rooms'), ('Capvise Labs', 'Technology', 'Experiments with AI'),
        ('Capvise Media', 'Media', 'Technology journalism'), ('Capvise Growth', 'Marketing', 'Market entry'),
        ('Capvise Events', 'Events', 'Event production'), ('Creator Network', 'Creators', 'Creator collaborations'),
        ('Capvise Club', 'Communities', 'Technology communities'), ('The Rejected Club', 'Founders', 'Founder curation')]


def group(c):
    s = Sheet(640, c, 'Capvise Group, drawn as a floor plan of eight rooms: Capvise Global, Labs, Media, Growth, Events, Creator Network, Club and The Rejected Club.')
    W, H = s.W, s.H
    s.walls([('top', DOOR_X, DOOR_W, None), ('bottom', DOOR_X, DOOR_W, 'L')])
    s.text(M - 3, 104, 'One group, eight ventures.', S5, 47, c['ink'], ls=-0.035)
    s.text(M, 142, 'Each runs on its own. Capvise Global is the flagship.', S4, 19.5, c['mute'])
    x0, x1 = M, W - M
    y0, y1, y2, y3 = 204, 350, 412, 558
    tops = [x0, x0 + 304, x0 + 304 + 190, x0 + 304 + 380, x1]
    bots = [x0 + i * (x1 - x0) / 4 for i in range(5)]
    wall, thin = c['wall'], 2.4
    dw = 26
    P = []
    # outer wall, with the group's front door on the corridor at the left
    P.append(f'M{x0} {y1 + 12}V{y0}H{x1}V{y3}H{x0}V{y2 - 12}')
    s.add(f'<path d="{"".join(P)}" fill="none" stroke="{wall}" stroke-width="3.6" stroke-linejoin="miter"/>')
    Q = []
    for xx in tops[1:-1]: Q.append(f'M{f(xx)} {y0}V{y1}')
    for xx in bots[1:-1]: Q.append(f'M{f(xx)} {y2}V{y3}')
    doors = []
    for i in range(4):
        a, b = tops[i], tops[i + 1]; dx = b - 22 - dw
        Q.append(f'M{f(a)} {y1}H{f(dx)}M{f(dx + dw)} {y1}H{f(b)}'); doors.append((dx, y1, -1))
        a, b = bots[i], bots[i + 1]; dx = a + 22
        Q.append(f'M{f(a)} {y2}H{f(dx)}M{f(dx + dw)} {y2}H{f(b)}'); doors.append((dx, y2, 1))
    s.add(f'<path d="{"".join(Q)}" fill="none" stroke="{wall}" stroke-width="{thin}"/>')
    for dx, y, dr in doors:      # leaves swing into the rooms
        s.add(f'<path d="M{f(dx)} {y}v{dr * dw}" stroke="{wall}" stroke-width="1.3"/>'
              f'<path d="M{f(dx)} {y + dr * dw}a{dw} {dw} 0 0 {1 if dr < 0 else 0} {dw} {-dr * dw}" fill="none" stroke="{c["faint"]}" stroke-width="0.9" stroke-dasharray="2 3"/>')
    # flagship gets a tint
    s.body.insert(1, f'<rect x="{x0}" y="{y0}" width="{tops[1] - x0}" height="{y1 - y0}" fill="{c["paper2"]}"/>')
    for i, (name, dom, what) in enumerate(VENT):
        xx = (tops[i] if i < 4 else bots[i - 4]) + 18
        yy = (y0 if i < 4 else y2) + 40
        if i >= 4: yy += 30
        s.text(xx, yy, name, S5, 19.5, c['ink'], ls=-0.015)
        s.text(xx, yy + 24, dom, PI, 17.5, c['sage'])
        s.text(xx, yy + 47, what, S4, 14.5, c['mute'])
    s.text((x0 + x1) / 2, (y1 + y2) / 2 + 5.5, 'Capvise Group', S4, 15, c['mute'], anchor='middle', ls=0.02)
    s.text(W - M, H - 30, 'capvise.group', S4, 15.5, c['mute'], anchor='end')
    return s


# ---------------------------------------------------------------- title block
PATH = [('2026', 'Sat on the evaluation panel at Claude Impact Lab. Open-sourced Cwtch.'),
        ('2025', 'Founded Capvise Group. COO at BackersStage, April to December. Ran four rooms in four countries. Built OmniSweep at ETHGlobal Buenos Aires.'),
        ('2024', 'AI engineering with open-source image and video models. Data annotation at Innodata.'),
        ('2023', 'Started shipping full-stack products.')]
TOOLS = [('Web', 'TypeScript, Next.js, React, Node.js, Tailwind CSS'), ('Data', 'PostgreSQL, MongoDB, Redis, Prisma'),
         ('AI', 'Python, Stable Diffusion, ComfyUI, AnimateDiff, Segment Anything 2'),
         ('Onchain', 'Solidity, LayerZero V2, 1inch, ethers.js'), ('Infra', 'Docker, AWS, Cloudflare, Vercel')]


def block(c):
    s = Sheet(620, c, 'Title block. Path from 2023 to 2026, tools, and contact: sahil@capvise.group.')
    W, H = s.W, s.H
    s.walls([('top', DOOR_X, DOOR_W, None)])
    s.text(M, 86, 'Building something, or raising for it?', S4, 19.5, c['mute'])
    s.runs(M - 3, 140, [('Write to ', S5, c['ink']), ('sahil@capvise.group', S5, c['sage'])], 47, ls=-0.035)
    x0, x1, y0, y1 = M, W - M, 196, H - 62
    xa, xb = 470, 760
    hl = c['faint']
    s.add(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="none" stroke="{hl}" stroke-width="1.2"/>')
    s.line(xa, y0, xa, y1, hl, 1.2); s.line(xb, y0, xb, y1, hl, 1.2)
    lab = lambda x, y, t: s.text(x, y, t, PI, 17, c['sage'])
    lab(x0 + 18, y0 + 32, 'Path')
    y = y0 + 64
    for yr, t in PATH:
        s.text(x0 + 18, y, yr, S6, 15, c['ink'], feat=TNUM)
        y = s.para(x0 + 70, y, t, S4, 15, c['mute'], xa - x0 - 92, 21) + 10
    lab(xa + 18, y0 + 32, 'Tools')
    y = y0 + 64
    for k, t in TOOLS:
        s.text(xa + 18, y, k, S6, 15, c['ink'])
        y = s.para(xa + 92, y, t, S4, 15, c['mute'], xb - xa - 108, 21) + 10
    cells = [('Drawn by', 'Sahil Meena'), ('Scale', 'One dot, one person'), ('Based in', 'India'), ('Sheet', 'Last of nine')]
    ch = (y1 - y0) / len(cells)
    for i, (k, v) in enumerate(cells):
        yy = y0 + i * ch
        if i: s.line(xb, yy, x1, yy, hl, 1.2)
        lab(xb + 16, yy + 30, k)
        s.text(xb + 16, yy + 56, v, S5, 16, c['ink'])
    return s


SHEETS = {'entrance': entrance, 'rooms': rooms, 'y2027': y2027, 'builder': builder, 'cwtch': cwtch, 'omnisweep': omni, 'hypersight': hyper, 'group': group, 'block': block}

if __name__ == '__main__':
    import sys
    only = sys.argv[1:]
    for name, fn in SHEETS.items():
        if only and name not in only: continue
        for th in (LIGHT, DARK):
            svg = fn(th).svg()
            open(f'{OUT}/{name}-{th["name"]}.svg', 'w').write(svg)
            print(name, th['name'], len(svg) // 1024, 'KB')
