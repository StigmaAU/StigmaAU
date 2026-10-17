"""Hero banner: Project Reborn RP over a Los Santos-inspired skyline at night."""

import math
import os
import random

from svgkit import C, Doc, corner_brackets, fmt, png_data_uri

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 470
BASE = 410  # street level of the main skyline


def _windows(R, x, top, w, base, density, lit_cls_count=3):
    """Lit windows for one building as (x, y, cls) tuples."""
    out = []
    cols = max(1, int((w - 6) // 7))
    rows = max(1, int((base - top - 8) // 9))
    x0 = x + (w - cols * 7) / 2 + 2
    for r in range(rows):
        for c in range(cols):
            if R.random() < density:
                out.append((x0 + c * 7, top + 7 + r * 9, R.randrange(lit_cls_count + 3)))
    return out


def _palm(x, base, h, lean, scale=1.0):
    """Palm tree silhouette: curved trunk plus a fan of fronds."""
    tx, ty = x + lean, base - h
    trunk = (f'<path d="M{fmt(x - 2.2 * scale)} {base}Q{fmt(x + lean * 0.2)} {fmt(base - h * 0.55)} '
             f'{fmt(tx - 1.2 * scale)} {fmt(ty)}L{fmt(tx + 1.2 * scale)} {fmt(ty)}'
             f'Q{fmt(x + lean * 0.2 + 3 * scale)} {fmt(base - h * 0.55)} {fmt(x + 2.2 * scale)} {base}Z"/>')
    fronds = []
    for ang, ln, droop in [(-170, 26, 9), (-140, 24, 7), (-110, 18, 4), (-70, 18, 4),
                           (-40, 24, 7), (-10, 26, 9), (-90, 12, 0), (160, 16, 10), (20, 16, 10)]:
        a = math.radians(ang)
        ex, ey = tx + math.cos(a) * ln * scale, ty + math.sin(a) * ln * scale + droop * scale
        mx, my = tx + math.cos(a) * ln * 0.55 * scale, ty + math.sin(a) * ln * 0.55 * scale - 4 * scale
        nx, ny = -math.sin(a) * 2.2 * scale, math.cos(a) * 2.2 * scale
        fronds.append(f'M{fmt(tx)} {fmt(ty)}Q{fmt(mx + nx)} {fmt(my + ny)} {fmt(ex)} {fmt(ey)}'
                      f'Q{fmt(mx - nx)} {fmt(my - ny)} {fmt(tx)} {fmt(ty)}Z')
    return trunk + f'<path d="{"".join(fronds)}"/>'


def build(out_path):
    R = random.Random(2024)
    d = Doc(W, H, "Project Reborn RP: more than just a project",
            "Cinematic banner: the Project Reborn wordmark over a Los Santos-inspired night skyline "
            "with violet neon, searchlights and drifting fog. Tagline: More than just a project. "
            "NSW inspired, custom scripts.")

    wordmark, (wm_w, wm_h) = png_data_uri(os.path.join(HERE, "brand", "wordmark.png"), width=1100, colors=48)
    rmark, _ = png_data_uri(os.path.join(HERE, "brand", "r-mark.png"), width=150, colors=96)

    d.style("""
.tw{animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}
.beam{transform-box:view-box;transform-origin:0 0;animation:sweep 11s ease-in-out infinite alternate}
@keyframes sweep{from{transform:rotate(-16deg)}to{transform:rotate(14deg)}}
.fogA{animation:drift 38s ease-in-out infinite alternate}
.fogB{animation:drift 29s ease-in-out infinite alternate-reverse}
@keyframes drift{from{transform:translateX(-90px)}to{transform:translateX(90px)}}
.p{animation:rise 10s linear infinite;opacity:0}
@keyframes rise{0%{transform:translateY(0);opacity:0}15%{opacity:.85}80%{opacity:.5}100%{transform:translateY(-120px);opacity:0}}
.lw{animation:flick 7s steps(1) infinite}
@keyframes flick{0%,100%{opacity:1}43%{opacity:.35}47%{opacity:1}71%{opacity:.6}}
.wheel{transform-box:view-box;transform-origin:128px 322px;animation:spin 70s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.rim{animation:chase 3s linear infinite}
@keyframes chase{to{stroke-dashoffset:-48}}
.car{animation:drive 6s linear infinite}
.rev{animation-name:driveBack}
@keyframes drive{from{transform:translateX(-20px)}to{transform:translateX(1330px)}}
@keyframes driveBack{from{transform:translateX(1220px)}to{transform:translateX(-120px)}}
.halo{animation:breathe 7s ease-in-out infinite}
@keyframes breathe{0%,100%{opacity:.75}50%{opacity:1}}
.blink{animation:blink 2.2s steps(1) infinite}
@keyframes blink{0%,60%{opacity:1}61%,100%{opacity:.15}}
.scan{animation:scan 9s linear infinite}
@keyframes scan{from{transform:translateY(0)}to{transform:translateY(720px)}}
.gl{opacity:0;animation:glitch 9s steps(1) infinite}
.gl2{animation-delay:.06s}
@keyframes glitch{0%,91%,95%,100%{opacity:0;transform:none}92%{opacity:.8;transform:translateX(-5px)}93%{opacity:.6;transform:translateX(4px)}94%{opacity:.7;transform:translateX(-2px)}}
.dot{animation:pulse 2.4s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
""")

    defs = d.defs
    defs.append(f'''
<clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#050409"/><stop offset=".42" stop-color="#0c0816"/>
 <stop offset=".7" stop-color="#1c0b33"/><stop offset=".86" stop-color="#3b1366"/><stop offset="1" stop-color="#210a3b"/>
</linearGradient>
<radialGradient id="glowHorizon" cx=".5" cy="1" r=".75"><stop offset="0" stop-color="{C["purple"]}" stop-opacity=".62"/><stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></radialGradient>
<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{C["purple"]}" stop-opacity=".34"/><stop offset=".55" stop-color="{C["purple"]}" stop-opacity=".1"/><stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#e9d6ff" stop-opacity=".34"/><stop offset=".6" stop-color="{C["purple_ink"]}" stop-opacity=".09"/><stop offset="1" stop-color="{C["purple_ink"]}" stop-opacity="0"/></linearGradient>
<linearGradient id="fog" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b2bb0" stop-opacity="0"/><stop offset=".5" stop-color="#6b2bb0" stop-opacity=".28"/><stop offset="1" stop-color="#6b2bb0" stop-opacity="0"/></linearGradient>
<linearGradient id="hills" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#221238"/><stop offset="1" stop-color="#130b22"/></linearGradient>
<linearGradient id="far" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1f1233"/><stop offset="1" stop-color="#170d27"/></linearGradient>
<linearGradient id="mid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#110a1d"/><stop offset="1" stop-color="#0a0712"/></linearGradient>
<linearGradient id="comet" x1="0" x2="1"><stop offset="0" stop-color="#e8fbff" stop-opacity="0"/><stop offset=".85" stop-color="#e8fbff" stop-opacity=".9"/><stop offset="1" stop-color="#fff"/></linearGradient>
<linearGradient id="tail" x1="1" x2="0"><stop offset="0" stop-color="{C["purple"]}" stop-opacity="0"/><stop offset=".85" stop-color="{C["purple_ink"]}" stop-opacity=".9"/><stop offset="1" stop-color="#f0e2ff"/></linearGradient>
<linearGradient id="refl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["purple"]}" stop-opacity=".32"/><stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["purple"]}" stop-opacity="0"/><stop offset=".5" stop-color="{C["purple_ink"]}"/><stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></linearGradient>
<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/><stop offset=".5" stop-color="{C["cyan"]}" stop-opacity=".07"/><stop offset="1" stop-color="{C["cyan"]}" stop-opacity="0"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>
<linearGradient id="road" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0812"/><stop offset="1" stop-color="#050408"/></linearGradient>
<linearGradient id="head" x1="0" x2="1"><stop offset="0" stop-color="#e8fbff" stop-opacity="0"/><stop offset="1" stop-color="#e8fbff"/></linearGradient>
<pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" opacity=".035"/></pattern>
<pattern id="winFar" width="6" height="8" patternUnits="userSpaceOnUse"><rect x="1" y="2" width="2" height="3" fill="#3a2560" opacity=".55"/></pattern>
<pattern id="winMid" width="7" height="9" patternUnits="userSpaceOnUse"><rect x="2" y="2" width="3" height="4" fill="#26193f" opacity=".55"/></pattern>
<linearGradient id="tagFade" x1="0" x2="1"><stop offset="0" stop-color="{C["purple_ink"]}" stop-opacity="0"/><stop offset="1" stop-color="{C["purple_ink"]}" stop-opacity=".9"/></linearGradient>
<linearGradient id="tagFadeR" x1="1" x2="0"><stop offset="0" stop-color="{C["purple_ink"]}" stop-opacity="0"/><stop offset="1" stop-color="{C["purple_ink"]}" stop-opacity=".9"/></linearGradient>
<clipPath id="tagSlice"><rect x="0" y="214" width="{W}" height="9"/></clipPath>
''')

    g = []  # everything inside the rounded frame
    g.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    g.append(f'<rect y="180" width="{W}" height="{H - 180}" fill="url(#glowHorizon)"/>')

    # stars, plus the Southern Cross (Crux) and its two pointers for an Australian sky
    stars = []
    for i in range(110):
        x, y = R.uniform(10, W - 10), R.uniform(8, 300) ** 1.0
        if 230 < x < 970 and 40 < y < 290:  # keep the title area clean
            if R.random() < 0.7:
                continue
        r = R.choice([0.5, 0.6, 0.7, 0.9, 1.1])
        op = R.uniform(0.25, 0.8) * (1 - y / 380)
        cls = ' class="tw"' if R.random() < 0.14 else ""
        delay = f' style="animation-delay:-{R.uniform(0, 4):.1f}s"' if cls else ""
        stars.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" opacity="{fmt(op)}"{cls}{delay}/>')
    g.append(f'<g fill="#fff">{"".join(stars)}</g>')
    crux = [(118, 54, 1.9), (104, 92, 2.2), (138, 98, 1.6), (150, 70, 1.3), (128, 84, 1.0)]
    pointers = [(62, 126, 1.8), (88, 120, 1.5)]
    cr = []
    for x, y, r in crux + pointers:
        cr.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>'
                  f'<circle cx="{x}" cy="{y}" r="{r * 3.2:.1f}" fill="{C["purple_ink"]}" opacity=".18"/>')
    cr.append(f'<path d="M118 54L104 92M150 70L138 98" stroke="{C["purple_ink"]}" stroke-width=".6" opacity=".25"/>')
    g.append(f'<g class="halo">{"".join(cr)}</g>')

    # searchlights from the city
    for bx, by, delay, dur in [(330, 400, 0, 11), (812, 402, -4, 13), (1132, 300, -7, 9.5)]:
        g.append(f'<g transform="translate({bx} {by})"><polygon class="beam" points="0,0 -26,-430 26,-430" '
                 f'fill="url(#beam)" style="animation-delay:{delay}s;animation-duration:{dur}s"/></g>')

    # distant hills (Vinewood) and a far mountain
    hills = ("M0 330 C60 300 120 286 190 300 C260 314 300 270 380 262 C450 255 500 292 560 300 "
             "C640 310 690 268 760 270 C840 272 870 300 940 296 C1010 292 1060 262 1120 270 "
             f"C1160 276 1185 290 1200 296 L1200 {BASE} L0 {BASE}Z")
    g.append(f'<path d="{hills}" fill="url(#hills)"/>')
    g.append(f'<path d="{hills.split(" L1200")[0]}" fill="none" stroke="{C["purple_ink"]}" stroke-width="1" opacity=".22"/>')

    hl = []
    for _ in range(70):
        hx = R.uniform(150, 1000)
        hy = R.uniform(292, 336)
        hl.append(f'<circle cx="{fmt(hx)}" cy="{fmt(hy)}" r="{R.choice([0.6, 0.7, 0.9])}"/>')
    g.append(f'<g fill="#eadcff" opacity=".45">{"".join(hl)}</g>')
    g.append(f'<g class="fogA"><rect x="-150" y="270" width="{W + 300}" height="90" fill="url(#fog)"/></g>')

    # far skyline layer
    far, x = [], -4
    while x < W:
        w = R.randrange(14, 34)
        if 960 < x < 1200:
            top = R.randrange(255, 330)
        elif x < 70:
            top = R.randrange(270, 320)
        else:
            top = R.randrange(318, 360)
        far.append((x, w, top))
        x += w + R.randrange(-2, 3)
    g.append('<g fill="url(#far)">' + "".join(
        f'<rect x="{x}" y="{t}" width="{w}" height="{BASE - t}"/>' for x, w, t in far) + "</g>")
    g.append('<g fill="url(#winFar)">' + "".join(
        f'<rect x="{x + 2}" y="{t + 4}" width="{w - 4}" height="{BASE - t - 6}"/>' for x, w, t in far) + "</g>")

    # main skyline: landmarks placed by hand, the rest procedural and kept low under the title
    mids = []
    x = -6
    while x < W:
        w = R.randrange(18, 42)
        if x < 64:
            top = R.randrange(222, 262)
        elif x < 250:
            top = R.randrange(338, 372)
        elif x < 950:
            top = R.randrange(306, 352)
        else:
            top = R.randrange(214, 300)
        mids.append([x, w, top])
        x += w + R.randrange(0, 4)
    shapes, lit = [], []
    for x, w, top in mids:
        if 990 <= x <= 1080:  # leave room for the tower
            continue
        shapes.append(f'<rect x="{x}" y="{top}" width="{w}" height="{BASE - top}"/>')
        if R.random() < 0.35:
            shapes.append(f'<rect x="{x + w * 0.2:.0f}" y="{top - 8}" width="{w * 0.6:.0f}" height="9"/>')
        if R.random() < 0.18:
            shapes.append(f'<rect x="{x + w / 2 - 0.6:.1f}" y="{top - 22}" width="1.2" height="22"/>')
        lit += _windows(R, x, top, w, BASE, 0.09 if 250 < x < 950 else 0.12)

    # landmark 1: a tapered tower with a slanted crown (Maze Bank-style)
    tower = "M1004 410 L1012 132 L1058 96 L1066 410Z"
    # landmark 2: stepped tower with spire (FIB-style)
    fib = "M1106 410 V196 H1114 V178 H1158 V196 H1166 V410Z M1135 178 V140 H1137 V178Z"
    # landmark 3: high-rise under construction with a crane (Mile High-style)
    mile = "M948 410 V214 H990 V410Z"
    crane = (f'<path d="M966 214 V160 M960 160 H1004 M966 160 L952 168 H966 M966 166 L1000 160 M996 160 V178" '
             f'stroke="#140c22" stroke-width="2.4" fill="none"/>')
    shapes += [f'<path d="{tower}"/>', f'<path d="{fib}"/>', f'<path d="{mile}"/>']
    lit += _windows(R, 1012, 140, 46, BASE, 0.16) + _windows(R, 1110, 200, 52, BASE, 0.14) + _windows(R, 950, 222, 38, BASE, 0.1)

    g.append('<g fill="url(#mid)">' + "".join(shapes) + "</g>" + crane)
    rims, neon = [], []
    for x, w, top in mids:
        if 990 <= x <= 1080:
            continue
        rims.append(f'<rect x="{x}" y="{top}" width="{w}" height="1"/>')
        if 280 < x < 940 and w > 28 and R.random() < 0.22:
            col = C["cyan"] if R.random() < 0.25 else C["purple_ink"]
            neon.append(f'<rect x="{x + 4}" y="{top + 5}" width="{w - 8}" height="2" rx="1" fill="{col}"/>'
                        f'<rect x="{x + 2}" y="{top + 2}" width="{w - 4}" height="8" rx="4" fill="{col}" opacity=".16"/>')
    g.append(f'<g fill="{C["purple_ink"]}" opacity=".3">{"".join(rims)}</g>' + "".join(neon))
    g.append('<g fill="url(#winMid)">' + "".join(
        f'<rect x="{x + 3}" y="{t + 5}" width="{w - 6}" height="{BASE - t - 8}"/>'
        for x, w, t in mids if not (990 <= x <= 1080)) + "</g>")
    colors = ["#e9dcff", C["purple_ink"], "#b77dff", "#f6efff", "#8f5cff", "#ffd9a8"]
    groups = {}
    for x, y, c in lit:
        groups.setdefault(c, []).append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="3" height="4"/>')
    for c, rects in groups.items():
        cls = ' class="lw"' if c in (1, 4) else ""
        delay = f' style="animation-delay:-{c * 1.3:.1f}s"' if cls else ""
        op = ".5" if c == 5 else ".85"
        g.append(f'<g fill="{colors[c % len(colors)]}" opacity="{op}"{cls}{delay}>{"".join(rects)}</g>')

    # neon trim on the landmarks
    g.append(f'<path d="M1012 132 L1058 96" stroke="{C["purple_ink"]}" stroke-width="2" opacity=".95"/>'
             f'<path d="M1012 132 L1058 96" stroke="{C["purple"]}" stroke-width="8" opacity=".25"/>'
             f'<path d="M1012 132 L1004 410 M1058 96 L1066 410" stroke="{C["purple"]}" stroke-width="1.2" opacity=".55"/>'
             f'<path d="M1114 178 H1158" stroke="{C["purple_ink"]}" stroke-width="1.5" opacity=".7"/>'
             f'<circle cx="1058" cy="93" r="2" fill="#ff5a6e" class="blink"/>'
             f'<circle cx="1136" cy="138" r="1.6" fill="#ff5a6e" class="blink" style="animation-delay:-1.1s"/>'
             f'<circle cx="1004" cy="158" r="1.6" fill="#ff5a6e" class="blink" style="animation-delay:-.5s"/>')

    g.append(f'<g class="fogB"><rect x="-150" y="350" width="{W + 300}" height="70" fill="url(#fog)" opacity=".8"/></g>')

    # Ferris wheel on the pier (Del Perro-style)
    cx, cy, r = 128, 322, 60
    spokes = "".join(
        f'M{cx} {cy}L{fmt(cx + r * math.cos(math.radians(a)))} {fmt(cy + r * math.sin(math.radians(a)))}'
        for a in range(0, 360, 20))
    cabins = "".join(
        f'<rect x="{fmt(cx + r * math.cos(math.radians(a)) - 2.5)}" y="{fmt(cy + r * math.sin(math.radians(a)) - 2)}" '
        f'width="5" height="5" rx="1"/>' for a in range(0, 360, 30))
    g.append(f'<path d="M{cx} {cy}L96 412M{cx} {cy}L160 412M104 380H152" stroke="#0d0817" stroke-width="3.2" fill="none"/>')
    g.append(f'<g class="wheel"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1a0f2c" stroke-width="3"/>'
             f'<path d="{spokes}" stroke="#2a1945" stroke-width="1"/>'
             f'<circle class="rim" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["purple_ink"]}" stroke-width="1.6" stroke-dasharray="2 6"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["purple"]}" stroke-width="6" opacity=".22"/>'
             f'<g fill="#e9dcff" opacity=".75">{cabins}</g></g>'
             f'<circle cx="{cx}" cy="{cy}" r="4" fill="{C["purple_ink"]}"/>')
    g.append(f'<rect x="0" y="408" width="290" height="5" fill="#0b0712"/>')

    # foreground: palms, street lights, highway with light trails
    g.append(f'<rect x="0" y="{BASE}" width="{W}" height="{H - BASE}" fill="url(#road)"/>')
    g.append(f'<path d="M0 {BASE + 0.5}H{W}" stroke="{C["purple"]}" stroke-width="1" opacity=".35"/>')
    palms = "".join(_palm(x, 444, h, lean, s) for x, h, lean, s in [
        (18, 118, -10, 1.45), (236, 92, 7, 1.15), (268, 108, -5, 1.3), (452, 70, 5, 1.0), (706, 76, -6, 1.05),
        (902, 96, 7, 1.2), (1184, 120, -11, 1.45)])
    g.append(f'<g fill="#07050c">{palms}</g>')
    lamps = []
    for lx in range(70, W, 118):
        lamps.append(f'<path d="M{lx} 444V414h9" stroke="#0a0711" stroke-width="2" fill="none"/>'
                     f'<circle cx="{lx + 9}" cy="415" r="7" fill="{C["purple"]}" opacity=".18"/>'
                     f'<circle cx="{lx + 9}" cy="415" r="1.8" fill="#f1e4ff"/>')
    g.append("".join(lamps))
    g.append(f'<rect x="0" y="444" width="{W}" height="26" fill="#060409"/>')
    g.append(f'<path d="M0 444.5H{W}" stroke="#2a1b40" stroke-width="1"/>')
    refl = [f'<rect x="1004" y="{BASE + 1}" width="62" height="33" fill="url(#refl)"/>',
            f'<rect x="1110" y="{BASE + 1}" width="52" height="30" fill="url(#refl)" opacity=".6"/>',
            f'<rect x="96" y="{BASE + 1}" width="64" height="30" fill="url(#refl)" opacity=".5"/>']
    for _ in range(26):
        rx = R.uniform(260, 950)
        refl.append(f'<rect x="{fmt(rx)}" y="{BASE + 2}" width="{R.choice([2, 3, 4])}" height="{R.randrange(10, 26)}" fill="url(#refl)"/>')
    g.append("".join(refl))
    cars = []
    for i in range(7):
        cars.append(f'<g class="car" style="animation-delay:-{i * 0.95 + R.uniform(0, .5):.2f}s;animation-duration:6.4s">'
                    f'<rect x="-110" y="449" width="110" height="6" rx="3" fill="url(#comet)" opacity=".18"/>'
                    f'<rect x="-110" y="451" width="110" height="2" rx="1" fill="url(#comet)"/></g>')
    for i in range(6):
        cars.append(f'<g class="car rev" style="animation-delay:-{i * 1.2 + R.uniform(0, .6):.2f}s;animation-duration:7.6s">'
                    f'<rect x="0" y="457" width="90" height="6" rx="3" fill="url(#tail)" opacity=".22"/>'
                    f'<rect x="0" y="459" width="90" height="2" rx="1" fill="url(#tail)"/></g>')
    g.append("".join(cars))

    # drifting particles
    parts = []
    for i in range(34):
        px, py = R.uniform(20, W - 20), R.uniform(250, 450)
        pr = R.choice([0.8, 1, 1.2, 1.5])
        col = R.choice(["#e9dcff", C["purple_ink"], C["purple_ink"], C["cyan"]])
        parts.append(f'<circle class="p" cx="{fmt(px)}" cy="{fmt(py)}" r="{pr}" fill="{col}" '
                     f'style="animation-delay:-{R.uniform(0, 12):.1f}s;animation-duration:{R.uniform(8, 15):.1f}s"/>')
    g.append("".join(parts))

    # title block
    g.append('<ellipse class="halo" cx="600" cy="168" rx="470" ry="150" fill="url(#halo)"/>')

    rm = 54
    g.append(f'<image href="{rmark}" x="{600 - rm / 2}" y="40" width="{rm}" height="{rm * 357 / 360:.1f}"/>')

    wm_draw_w = 600
    wm_draw_h = wm_draw_w * wm_h / wm_w
    pill_h = round(wm_draw_h)
    rp, rp_w = d.text("RP", 0, 0, "sora", 800, 30)
    pill_w = round(rp_w + 34)
    gap = 18
    total = wm_draw_w + gap + pill_w
    wx = 600 - total / 2
    wy = 118
    g.append(f'<image href="{wordmark}" x="{fmt(wx)}" y="{wy}" width="{wm_draw_w}" height="{fmt(wm_draw_h)}"/>')
    px = wx + wm_draw_w + gap
    g.append(f'<rect x="{fmt(px)}" y="{wy}" width="{pill_w}" height="{pill_h}" rx="{pill_h / 2:.1f}" fill="{C["purple"]}" fill-opacity=".14" '
             f'stroke="{C["purple_ink"]}" stroke-width="1.6"/>')
    rp_svg, _ = d.text("RP", px + pill_w / 2, wy + pill_h / 2 + 11, "sora", 800, 30, fill=C["ink"], anchor="middle")
    g.append(rp_svg)

    tag, tag_w = d.text("MORE THAN JUST A PROJECT", 600, 232, "sora", 600, 27, fill=C["ink"], anchor="middle", ls=0.36)
    g.append(tag)
    # glitch slices: offset copies of the tagline, visible for a fraction of a second every 9s
    t1, _ = d.text("MORE THAN JUST A PROJECT", 600, 232, "sora", 600, 27, fill=C["cyan"], anchor="middle", ls=0.36)
    t2, _ = d.text("MORE THAN JUST A PROJECT", 600, 232, "sora", 600, 27, fill=C["purple"], anchor="middle", ls=0.36)
    g.append(f'<g clip-path="url(#tagSlice)"><g class="gl">{t1}</g><g class="gl gl2">{t2}</g></g>')

    sub_y = 274
    s1, w1 = d.text("NSW INSPIRED", 0, 0, "manrope", 700, 18, ls=0.3)
    s2, w2 = d.text("CUSTOM SCRIPTS", 0, 0, "manrope", 700, 18, ls=0.3)
    gap2 = 44
    sx = 600 - (w1 + gap2 + w2) / 2
    a, _ = d.text("NSW INSPIRED", sx, sub_y, "manrope", 700, 18, fill=C["purple_ink"], ls=0.3)
    b, _ = d.text("CUSTOM SCRIPTS", sx + w1 + gap2, sub_y, "manrope", 700, 18, fill=C["purple_ink"], ls=0.3)
    bar_x = sx + w1 + gap2 / 2 - 2
    g.append(a + b + f'<rect x="{fmt(bar_x)}" y="{sub_y - 15}" width="2" height="18" rx="1" fill="{C["cyan"]}"/>')
    lx1, lx2 = sx - 22, sx + w1 + gap2 + w2 + 16
    g.append(f'<rect x="{fmt(lx1 - 110)}" y="{sub_y - 7}" width="110" height="1.4" fill="url(#tagFade)"/>'
             f'<rect x="{fmt(lx2)}" y="{sub_y - 7}" width="110" height="1.4" fill="url(#tagFadeR)"/>')

    # atmosphere overlays
    g.append(f'<g class="scan"><rect y="-120" width="{W}" height="110" fill="url(#scanG)"/></g>')
    g.append(f'<rect width="{W}" height="{H}" fill="url(#lines)"/>')
    g.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')

    # HUD chrome
    hud = []
    l1, _ = d.text("PROJECT REBORN RP  /  DEVELOPMENT HQ", 50, 44, "mono", 500, 12.5, fill=C["muted"], ls=0.12)
    hud.append(l1)
    l2, _ = d.text("EST. 2024", W - 50, 44, "mono", 500, 12.5, fill=C["muted"], anchor="end", ls=0.12)
    hud.append(l2)
    hud.append(f'<circle class="dot" cx="{W - 50 - _ - 14}" cy="39.5" r="3.2" fill="{C["cyan"]}"/>')
    l3, _ = d.text("33.8688° S  ·  151.2093° E", 50, H - 34, "mono", 500, 12.5, fill=C["muted"], ls=0.08)
    hud.append(l3)
    l4, _ = d.text("BUILT BY STIGMAAU", W - 50, H - 34, "mono", 500, 12.5, fill=C["muted"], anchor="end", ls=0.12)
    hud.append(l4)
    hud.append(corner_brackets(24, 24, W - 48, H - 48, l=22, opacity=0.65))
    g.append("".join(hud))

    d.add(f'<g clip-path="url(#frame)">{"".join(g)}</g>')
    d.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="21.5" fill="none" stroke="{C["line"]}"/>'
          f'<rect x="80" y="0" width="{W - 160}" height="1.5" fill="url(#edge)" opacity=".9"/>')
    return d.save(out_path)
