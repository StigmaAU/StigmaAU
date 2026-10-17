"""Section artwork for the profile: headers, developer file, stack, systems,
repositories, philosophy and footer. Every fact shown comes from the Project
Reborn repositories (resource manifests, READMEs and git history)."""

import math
import os
import random

from svgkit import C, Doc, brand_icon, corner_brackets, fmt, lucide, png_data_uri

HERE = os.path.dirname(os.path.abspath(__file__))
W = 1200
CARD = "#111015"
PANEL = "#18171d"


# ---------------------------------------------------------------- helpers --

def wrap(d, text, family, weight, size, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = f"{cur} {wd}".strip()
        if d.measure(trial, family, weight, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def card(d, w, h, uid, rx=20, glow=(0.15, 0.0), grid=False):
    """Dark card with a violet edge light. Returns svg; adds defs."""
    gx, gy = glow
    d.defs.append(
        f'<radialGradient id="{uid}g" cx="{gx}" cy="{gy}" r="1"><stop offset="0" stop-color="{C["purple"]}" stop-opacity=".16"/>'
        f'<stop offset=".55" stop-color="{C["purple"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="{uid}e" x1="0" x2="1"><stop offset="0" stop-color="{C["purple"]}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{C["purple_ink"]}" stop-opacity=".9"/><stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></linearGradient>')
    out = [f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{CARD}"/>',
           f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="url(#{uid}g)"/>']
    if grid:
        d.defs.append(f'<pattern id="{uid}p" width="32" height="32" patternUnits="userSpaceOnUse">'
                      f'<path d="M32 0H0V32" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>')
        out.append(f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="url(#{uid}p)"/>')
    out.append(f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" stroke="{C["line"]}"/>')
    out.append(f'<rect x="{rx * 2}" y="0" width="{w - rx * 4}" height="1.5" fill="url(#{uid}e)"/>')
    return "".join(out)


def pill(d, x, y, label, h=34, family="manrope", weight=600, size=15, fill="#1a1920", stroke=None,
         color=None, icon=None, icon_kind="lucide", icon_color=None, pad=16, dot=None, dot_cls=None):
    """A Reborn pill. (x, y) is the top-left corner. Returns (svg, width)."""
    tw = d.measure(label, family, weight, size)
    isz = round(h * 0.5)
    lead = (isz + 8) if icon else (14 if dot else 0)
    w = pad * 2 + lead + tw
    parts = [f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{h}" rx="{h / 2}" fill="{fill}"'
             + (f' stroke="{stroke}"' if stroke else "") + "/>"]
    cx = x + pad
    if icon:
        iy = y + (h - isz) / 2
        if icon_kind == "brand":
            parts.append(brand_icon(icon, cx, iy, isz, fill=icon_color or C["ink"]))
        else:
            parts.append(lucide(icon, cx, iy, isz, stroke=icon_color or C["purple_ink"], sw=2))
    elif dot:
        cls = f' class="{dot_cls}"' if dot_cls else ""
        parts.append(f'<circle cx="{fmt(cx + 4)}" cy="{fmt(y + h / 2)}" r="4" fill="{dot}"{cls}/>')
    cap = 0.72 * size  # approximate cap height for vertical centring
    t, _ = d.text(label, cx + lead, y + h / 2 + cap / 2 - 0.5, family, weight, size, fill=color or C["ink"])
    parts.append(t)
    return "".join(parts), w


def icon_tile(x, y, name, size=48, rx=14):
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{rx}" fill="{C["purple_soft"]}" '
            f'stroke="{C["purple"]}" stroke-opacity=".45"/>'
            + lucide(name, x + size * 0.23, y + size * 0.23, size * 0.54, stroke=C["purple_ink"], sw=1.9))


# ---------------------------------------------------------------- headers --

HEADERS = [
    ("01", "map-pin", "City introduction", "WHO BUILDS THE CITY"),
    ("02", "layers", "The technology behind the city", "STACK"),
    ("03", "blocks", "Systems built for Reborn", "IN-HOUSE RESOURCES"),
    ("04", "activity", "Development telemetry", "LIVE FROM GITHUB"),
    ("05", "git-branch", "Project repositories", "PRIVATE SOURCE"),
    ("06", "scale", "Development philosophy", "HOW IT IS BUILT"),
]


def header(path, num, icon, title, right):
    h = 84
    d = Doc(W, h, f"{num}: {title}", f"Section {num} header: {title}.")
    d.style(".pulse{animation:hp 6s cubic-bezier(.4,0,.2,1) infinite}"
            "@keyframes hp{from{transform:translateX(0)}to{transform:translateX(var(--run))}}")
    body = [card(d, W, h, "h", rx=18, glow=(0.0, 0.5))]
    body.append(icon_tile(18, 18, icon))
    k, _ = d.text(f"SECTOR {num}", 84, 36, "mono", 600, 12.5, fill=C["cyan"], ls=0.16)
    t, tw = d.text(title, 84, 63, "sora", 700, 25, fill=C["ink"])
    r, rw = d.text(right, W - 28, 47, "mono", 500, 12.5, fill=C["muted"], anchor="end", ls=0.16)
    body += [k, t, r]
    x1, x2 = 84 + tw + 28, W - 28 - rw - 24
    d.defs.append(f'<linearGradient id="hl" x1="0" x2="1"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/>'
                  f'<stop offset="1" stop-color="{C["cyan"]}"/></linearGradient>'
                  f'<clipPath id="hc"><rect x="{fmt(x1)}" y="38" width="{fmt(x2 - x1)}" height="12"/></clipPath>')
    body.append(f'<path d="M{fmt(x1)} 44H{fmt(x2)}" stroke="{C["line"]}" stroke-width="1.5"/>'
                f'<circle cx="{fmt(x2)}" cy="44" r="3" fill="{C["purple_ink"]}"/>'
                f'<g clip-path="url(#hc)"><rect class="pulse" style="--run:{fmt(x2 - x1 + 90)}px" x="{fmt(x1 - 90)}" y="43" width="90" height="2" fill="url(#hl)"/></g>')
    d.add(*body)
    return d.save(path)


# ---------------------------------------------------------------- dossier --

ROLES = ["FiveM Developer", "ESX Systems Developer", "UI/UX Developer",
         "Server Infrastructure Developer", "Gameplay Systems Developer"]


def typing(d, roles, x, y, family="manrope", weight=700, size=28, color=None, cursor=None):
    """SMIL typing loop. Frame 0 shows the first role fully typed, so static renderers
    (and reduced motion) still read a complete line."""
    type_t, hold_t, del_t, gap_t = 0.065, 1.9, 0.03, 0.4
    widths = [[d.measure(r[:i], family, weight, size) if i else 0 for i in range(len(r) + 1)] for r in roles]
    seg = []  # (duration, role, width)
    order = list(range(len(roles)))
    for n, r in enumerate(order):
        seg.append((hold_t, r, widths[r][-1]))
        for i in range(len(roles[r]) - 1, -1, -1):
            seg.append((del_t, r, widths[r][i]))
        seg.append((gap_t, -1, 0))
        nxt = order[(n + 1) % len(order)]
        for i in range(1, len(roles[nxt])):
            seg.append((type_t, nxt, widths[nxt][i]))
    total = sum(s[0] for s in seg)
    starts, t = [], 0.0
    for s in seg:
        starts.append(t / total)
        t += s[0]

    def anim(attr, vals):
        kt, vv = [], []
        for st, v in zip(starts, vals):
            if not vv or vv[-1] != v:
                kt.append(st)
                vv.append(v)
        kt[0] = 0
        return (f'<animate attributeName="{attr}" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite" '
                f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" values="{";".join(fmt(v) for v in vv)}"/>')

    out = []
    for i, role in enumerate(roles):
        vals = [s[2] if s[1] == i else 0 for s in seg]
        w0 = vals[0]
        d.defs.append(f'<clipPath id="tc{i}"><rect x="{fmt(x)}" y="{fmt(y - size)}" width="{fmt(w0 + 2)}" '
                      f'height="{fmt(size * 1.5)}">{anim("width", [v + 2 if v else 0 for v in vals])}</rect></clipPath>')
        t, _ = d.text(role, x, y, family, weight, size, fill=color or C["ink"])
        out.append(f'<g clip-path="url(#tc{i})">{t}</g>')
    cx_vals = [x + s[2] + 4 for s in seg]
    out.append(f'<rect x="{fmt(cx_vals[0])}" y="{fmt(y - size * 0.78)}" width="3" height="{fmt(size * 0.95)}" rx="1.5" '
               f'fill="{cursor or C["cyan"]}" class="cur">{anim("x", cx_vals)}</rect>')
    return "".join(out)


def dossier(path):
    h = 372
    d = Doc(W, h, "StigmaAU, developer of Project Reborn RP",
            "Developer file: StigmaAU, owner and lead developer of Project Reborn RP. Roles: "
            + ", ".join(ROLES) + ". Based in Brisbane, Australia, building since 2024.")
    d.style(".cur{animation:cb 1s steps(1) infinite}@keyframes cb{50%{opacity:0}}"
            ".live{animation:lv 2.4s ease-in-out infinite}@keyframes lv{0%,100%{opacity:1}50%{opacity:.35}}"
            ".sweep{animation:sw 7s linear infinite}@keyframes sw{from{transform:translateY(-60px)}to{transform:translateY(420px)}}")
    body = [card(d, W, h, "k", glow=(0.1, 0.0), grid=True)]
    body.append(corner_brackets(16, 16, W - 32, h - 32, l=16, opacity=0.5))

    k, _ = d.text("DEVELOPER FILE  /  001", 48, 66, "mono", 600, 13, fill=C["cyan"], ls=0.16)
    name, nw = d.text("StigmaAU", 46, 132, "sora", 800, 62, fill=C["ink"], ls=-0.01)
    r1, r1w = d.text("Owner & lead developer,", 48, 172, "manrope", 600, 21, fill=C["muted"])
    r2, _ = d.text("Project Reborn RP", 48 + r1w + 7, 172, "manrope", 700, 21, fill=C["purple_ink"])
    body += [k, name, r1, r2]

    # terminal line with the typing roles
    body.append(f'<rect x="46" y="198" width="610" height="68" rx="34" fill="{C["sunken"]}" stroke="{C["line"]}"/>')
    p, pw = d.text(">", 74, 242, "mono", 700, 24, fill=C["cyan"])
    body.append(p)
    body.append(typing(d, ROLES, 104, 242, size=27))

    x = 46
    for label, kw in [("Shipping updates", dict(dot=C["cyan"], dot_cls="live")),
                      ("Brisbane, AEST", dict(icon="map-pin")),
                      ("Building since 2024", dict(icon="timer"))]:
        s, pw = pill(d, x, 294, label, h=38, size=15.5, stroke=C["line"], **kw)
        body.append(s)
        x += pw + 10

    # dossier fields
    px, py, pw_, ph = 700, 40, 460, h - 80
    d.defs.append(f'<clipPath id="pc"><rect x="{px}" y="{py}" width="{pw_}" height="{ph}" rx="18"/></clipPath>'
                  f'<linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/>'
                  f'<stop offset="1" stop-color="{C["cyan"]}" stop-opacity=".08"/></linearGradient>')
    body.append(f'<rect x="{px}" y="{py}" width="{pw_}" height="{ph}" rx="18" fill="{PANEL}" stroke="{C["line"]}"/>')
    body.append(f'<g clip-path="url(#pc)"><g class="sweep"><rect x="{px}" y="{py - 40}" width="{pw_}" height="40" fill="url(#sg)"/>'
                f'<rect x="{px}" y="{py}" width="{pw_}" height="1" fill="{C["cyan"]}" opacity=".35"/></g></g>')
    rows = [("CITY", "Project Reborn RP"),
            ("SETTING", "Los Santos, NSW-inspired"),
            ("FRAMEWORK", "ESX Legacy + ox stack"),
            ("SPECIALTY", "Gameplay, staff tools, NUI"),
            ("BASE", "Brisbane, Australia")]
    rh = ph / len(rows)
    for i, (lab, val) in enumerate(rows):
        ry = py + i * rh
        if i:
            body.append(f'<path d="M{px + 24} {fmt(ry)}H{px + pw_ - 24}" stroke="{C["line"]}"/>')
        l, _ = d.text(lab, px + 26, ry + rh / 2 + 4.5, "mono", 600, 12.5, fill=C["subtle"], ls=0.14)
        v, _ = d.text(val, px + 150, ry + rh / 2 + 6.5, "manrope", 600, 18.5, fill=C["ink"])
        body += [l, v]
    d.add(*body)
    return d.save(path)


# ------------------------------------------------------------------ stack --

STACK = [
    ("L5", "Interface", "what players touch", [
        ("NUI · HTML/CSS/JS", "html5", "brand"), ("React", "react", "brand"), ("TypeScript", "typescript", "brand"),
        ("Vite", "vite", "brand"), ("Reborn UI", "palette", "lucide")]),
    ("L4", "Gameplay", "the ox ecosystem", [
        ("ox_lib", "blocks", "lucide"), ("ox_inventory", "package", "lucide"), ("ox_target", "crosshair", "lucide"),
        ("lb-phone", "radio", "lucide"), ("illenium-appearance", "shirt", "lucide")]),
    ("L3", "Framework", "server logic", [
        ("Lua 5.4", "lua", "brand"), ("ESX Legacy", "layers", "lucide"), ("Statebags", "workflow", "lucide"),
        ("lib.callback", "route", "lucide")]),
    ("L2", "Data", "persistence", [
        ("MySQL / MariaDB", "mysql", "brand"), ("oxmysql", "database", "lucide"), ("SQL migrations", "file-code-2", "lucide")]),
    ("L1", "Runtime & ops", "how it ships", [
        ("FXServer", "fivem", "brand"), ("Node.js", "nodedotjs", "brand"), ("Git + submodules", "git", "brand"),
        ("Discord webhooks", "discord", "brand"), ("PowerShell", "terminal", "lucide")]),
]


def stack(path):
    band_h, gap, top = 72, 12, 28
    h = top * 2 + len(STACK) * band_h + (len(STACK) - 1) * gap
    names = [m[0] for layer in STACK for m in layer[3]]
    d = Doc(W, h, "The technology behind the city",
            "Project Reborn's stack in five layers. Interface: NUI, React, TypeScript, Vite, Reborn UI. "
            "Gameplay: ox_lib, ox_inventory, ox_target, lb-phone, illenium-appearance. Framework: Lua 5.4, ESX Legacy, "
            "statebags, lib.callback. Data: MySQL/MariaDB, oxmysql, SQL migrations. Runtime and ops: FXServer, Node.js, "
            "Git with submodules, Discord webhooks, PowerShell.")
    d.style(".pk{animation:pk 5s cubic-bezier(.45,0,.55,1) infinite}"
            f"@keyframes pk{{0%{{transform:translateY(0);opacity:0}}8%{{opacity:1}}92%{{opacity:1}}100%{{transform:translateY({h - top * 2 - 30}px);opacity:0}}}}"
            ".up{animation-name:pu}"
            f"@keyframes pu{{0%{{transform:translateY({h - top * 2 - 30}px);opacity:0}}8%{{opacity:1}}92%{{opacity:1}}100%{{transform:translateY(0);opacity:0}}}}")
    body = [card(d, W, h, "s", glow=(0.0, 0.0), grid=True)]
    bus_x = 262
    body.append(f'<path d="M{bus_x} {top + 14}V{h - top - 14}" stroke="{C["line"]}" stroke-width="2"/>')
    for i, delay in enumerate([0, -1.7, -3.4]):
        cls = "pk up" if i == 1 else "pk"
        col = C["purple_ink"] if i == 1 else C["cyan"]
        body.append(f'<circle class="{cls}" style="animation-delay:{delay}s" cx="{bus_x}" cy="{top + 22}" r="3.5" fill="{col}"/>')
    for i, (code, title, sub, mods) in enumerate(STACK):
        y = top + i * (band_h + gap)
        d.defs.append(f'<linearGradient id="b{i}" x1="0" x2="1"><stop offset="0" stop-color="{C["purple"]}" stop-opacity=".16"/>'
                      f'<stop offset=".4" stop-color="{C["purple"]}" stop-opacity=".04"/><stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></linearGradient>')
        body.append(f'<rect x="28" y="{y}" width="{W - 56}" height="{band_h}" rx="16" fill="url(#b{i})" stroke="{C["line"]}"/>')
        c, _ = d.text(code, 50, y + 31, "mono", 700, 13, fill=C["cyan"], ls=0.1)
        t, _ = d.text(title, 84, y + 32, "sora", 700, 19, fill=C["ink"])
        s, _ = d.text(sub, 50, y + 54, "mono", 500, 12.5, fill=C["subtle"], ls=0.04)
        body += [c, t, s, f'<circle cx="{bus_x}" cy="{y + band_h / 2}" r="5" fill="{CARD}" stroke="{C["purple_ink"]}" stroke-width="2"/>']
        # lay the pills out, shrinking the gap if needed
        widths = [pill(d, 0, 0, n, h=44, size=16, icon=ic, icon_kind=k)[1] for n, ic, k in mods]
        avail = W - 56 - (bus_x - 28) - 40
        g = min(14, (avail - sum(widths)) / max(len(widths) - 1, 1))
        x = bus_x + 26
        for (n, ic, k), pw in zip(mods, widths):
            sv, _ = pill(d, x, y + (band_h - 44) / 2, n, h=44, size=16, icon=ic, icon_kind=k,
                         stroke=C["line"], fill="#19181f")
            body.append(sv)
            x += pw + g
        assert x - g <= W - 40, f"layer {title} overflows: {x}"
    d.add(*body)
    return d.save(path)


# ---------------------------------------------------------------- systems --

def _scene_staff(d, x, y, w, h, u):
    d.style(f".{u}r{{transform-box:view-box;transform-origin:{x + w - 92}px {y + h / 2}px;animation:{u}r 4s linear infinite}}"
            f"@keyframes {u}r{{to{{transform:rotate(360deg)}}}}"
            f".{u}b{{animation:{u}b 4s steps(1) infinite}}@keyframes {u}b{{0%,30%{{opacity:0}}31%,70%{{opacity:1}}71%{{opacity:.2}}}}"
            f".{u}l{{animation:{u}l 3.2s ease-in-out infinite}}@keyframes {u}l{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}")
    s = []
    # sidebar
    s.append(f'<rect x="{x + 22}" y="{y + 20}" width="96" height="{h - 40}" rx="12" fill="#17161c" stroke="{C["line"]}"/>')
    for i in range(5):
        fill = C["purple"] if i == 1 else "#2a2931"
        s.append(f'<rect x="{x + 34}" y="{y + 34 + i * 20}" width="{72 if i != 1 else 64}" height="10" rx="5" fill="{fill}"/>')
    # stat tiles + log rows
    for i in range(3):
        tx = x + 132 + i * 92
        s.append(f'<rect x="{tx}" y="{y + 20}" width="82" height="50" rx="10" fill="#17161c" stroke="{C["line"]}"/>'
                 f'<rect x="{tx + 12}" y="{y + 32}" width="34" height="6" rx="3" fill="#3a3842"/>'
                 f'<rect x="{tx + 12}" y="{y + 46}" width="{[50, 38, 56][i]}" height="10" rx="5" fill="{[C["purple_ink"], C["cyan"], C["ink"]][i]}" opacity=".85"/>')
    for i in range(3):
        ly = y + 82 + i * 18
        s.append(f'<rect x="{x + 132}" y="{ly}" width="266" height="12" rx="6" fill="#17161c"/>'
                 f'<circle class="{u}l" style="animation-delay:-{i * 0.9}s" cx="{x + 142}" cy="{ly + 6}" r="3" fill="{[C["cyan"], C["purple_ink"], C["cyan"]][i]}"/>'
                 f'<rect x="{x + 152}" y="{ly + 4}" width="{[150, 110, 180][i]}" height="4" rx="2" fill="#3a3842"/>')
    # radar
    cx, cy, r = x + w - 92, y + h / 2, 56
    d.defs.append(f'<linearGradient id="{u}sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/>'
                  f'<stop offset="1" stop-color="{C["cyan"]}" stop-opacity=".45"/></linearGradient>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0d0d11" stroke="{C["line"]}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62:.1f}" fill="none" stroke="{C["line"]}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r * 0.26:.1f}" fill="none" stroke="{C["line"]}"/>'
             f'<path d="M{cx - r} {cy}H{cx + r}M{cx} {cy - r}V{cy + r}" stroke="{C["line"]}"/>'
             f'<path class="{u}r" d="M{cx} {cy}L{cx + r} {cy}A{r} {r} 0 0 0 {fmt(cx + r * math.cos(math.radians(-40)))} {fmt(cy + r * math.sin(math.radians(-40)))}Z" fill="url(#{u}sw)"/>'
             f'<circle class="{u}b" cx="{cx + 22}" cy="{cy - 18}" r="3.5" fill="{C["cyan"]}"/>'
             f'<circle class="{u}b" style="animation-delay:-2s" cx="{cx - 26}" cy="{cy + 20}" r="3.5" fill="{C["purple_ink"]}"/>')
    return "".join(s)


def _scene_skills(d, x, y, w, h, u):
    cx, cy, r = x + 92, y + h / 2, 50
    circ = 2 * math.pi * r
    d.style(f".{u}p{{animation:{u}p 6s cubic-bezier(.3,0,.2,1) infinite}}"
            f"@keyframes {u}p{{0%{{stroke-dashoffset:{circ * 0.8:.1f}}}70%,100%{{stroke-dashoffset:{circ * 0.12:.1f}}}}}"
            f".{u}x{{animation:{u}x 6s ease-out infinite}}@keyframes {u}x{{0%,55%{{opacity:0;transform:translateY(6px)}}65%{{opacity:1}}90%{{opacity:0;transform:translateY(-16px)}}100%{{opacity:0}}}}"
            f".{u}z{{animation:{u}z 2.4s ease-in-out infinite}}@keyframes {u}z{{0%,100%{{opacity:1}}50%{{opacity:.45}}}}")
    s = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0d0d11" stroke="#25242b" stroke-width="9"/>',
         f'<circle class="{u}p" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["purple"]}" stroke-width="9" stroke-linecap="round" '
         f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ * 0.12:.1f}" transform="rotate(-90 {cx} {cy})"/>',
         lucide("pickaxe", cx - 20, cy - 20, 40, stroke=C["ink"], sw=1.8)]
    xp, _ = d.text("+XP", cx + 46, cy - 40, "mono", 700, 15, fill=C["cyan"])
    s.append(f'<g class="{u}x">{xp}</g>')
    icons = ["pickaxe", "axe", "fish", "crosshair", "waves", "swords", "anvil", "hammer"]
    labels = ["Mining", "Woodcutting", "Fishing", "Hunting", "Diving", "Combat", "Smithing", "Carpentry"]
    gx, gy = x + 196, y + 22
    for i, (ic, lab) in enumerate(zip(icons, labels)):
        col, row = i % 4, i // 4
        tx, ty = gx + col * 90, gy + row * 58
        s.append(f'<rect x="{tx}" y="{ty}" width="80" height="48" rx="12" fill="#17161c" stroke="{C["line"]}"/>')
        s.append(lucide(ic, tx + 10, ty + 13, 22, stroke=C["purple_ink"], sw=1.9))
        bw = [34, 26, 30, 20, 24, 32, 28, 22][i]
        s.append(f'<rect x="{tx + 40}" y="{ty + 16}" width="30" height="5" rx="2.5" fill="#2e2d35"/>'
                 f'<rect x="{tx + 40}" y="{ty + 16}" width="{bw * 30 / 34:.1f}" height="5" rx="2.5" fill="{C["purple_ink"]}"/>'
                 f'<rect x="{tx + 40}" y="{ty + 27}" width="22" height="5" rx="2.5" fill="#2e2d35"/>')
    zp, zw = pill(d, gx, y + h - 34, "XP bomb active", h=26, size=12.5, icon="zap", fill=C["purple_soft"],
                  stroke=C["purple"], icon_color=C["cyan"], pad=12)
    s.append(f'<g class="{u}z">{zp}</g>')
    return "".join(s)


def _items():
    return {k: png_data_uri(os.path.join(HERE, "brand", "items", f"{k}.png"), width=72)[0]
            for k in ["ore", "ingot", "pickaxe", "axe", "chainbody", "platebody"]}


def _scene_crafting(d, x, y, w, h, u, items):
    d.style(f".{u}s{{animation:{u}s 1.6s ease-out infinite;opacity:0}}"
            f"@keyframes {u}s{{0%{{opacity:1;transform:translate(0,0)}}100%{{opacity:0;transform:translate(var(--dx),var(--dy))}}}}"
            f".{u}a{{animation:{u}a 2.2s linear infinite}}@keyframes {u}a{{to{{stroke-dashoffset:-24}}}}"
            f".{u}h{{transform-box:view-box;transform-origin:{x + w / 2 + 26}px {y + 52}px;animation:{u}h 1.6s cubic-bezier(.5,0,.5,1) infinite}}"
            f"@keyframes {u}h{{0%,100%{{transform:rotate(-28deg)}}45%{{transform:rotate(6deg)}}55%{{transform:rotate(6deg)}}}}")
    s = []
    cy = y + h / 2 - 6
    xs = [x + 70, x + w / 2, x + w - 70]
    for i, (k, lab) in enumerate([("ore", "ORE"), (None, "FORGE"), ("pickaxe", "TOOL")]):
        cx = xs[i]
        s.append(f'<rect x="{cx - 44}" y="{cy - 44}" width="88" height="88" rx="18" fill="#17161c" stroke="{C["line"] if k else C["purple"]}"/>')
        if k:
            s.append(f'<image href="{items[k]}" x="{cx - 32}" y="{cy - 32}" width="64" height="64"/>')
        t, _ = d.text(lab, cx, cy + 66, "mono", 600, 12, fill=C["subtle"], anchor="middle", ls=0.18)
        s.append(t)
    # anvil + hammer + sparks in the middle tile
    ax = xs[1]
    s.append(lucide("anvil", ax - 26, cy - 14, 52, stroke=C["ink"], sw=1.6))
    s.append(f'<g class="{u}h">' + lucide("hammer", ax + 2, cy - 40, 30, stroke=C["purple_ink"], sw=2) + "</g>")
    for i, (dx, dy) in enumerate([(-26, -22), (-12, -32), (14, -30), (28, -18), (-30, -6), (24, -4)]):
        s.append(f'<circle class="{u}s" style="--dx:{dx}px;--dy:{dy}px;animation-delay:{0.72 + i * 0.03:.2f}s" '
                 f'cx="{ax - 4}" cy="{cy - 10}" r="1.8" fill="{[C["cyan"], "#ffd9a8", C["purple_ink"]][i % 3]}"/>')
    # ingot output beneath the forge flow
    for a, b in [(xs[0] + 50, xs[1] - 50), (xs[1] + 50, xs[2] - 50)]:
        s.append(f'<path class="{u}a" d="M{a} {cy}H{b}" stroke="{C["purple_ink"]}" stroke-width="2" stroke-dasharray="6 6"/>'
                 f'<path d="M{b - 6} {cy - 6}L{b} {cy}L{b - 6} {cy + 6}" fill="none" stroke="{C["purple_ink"]}" stroke-width="2" stroke-linecap="round"/>')
    s.append(f'<image href="{items["ingot"]}" x="{fmt((xs[1] + xs[2]) / 2 - 18)}" y="{cy - 52}" width="36" height="36"/>')
    return "".join(s)


CAR = ("M8 58C10 48 22 43 46 40L86 24C100 17 128 14 152 16C170 18 182 22 196 30L222 40C238 43 248 48 250 56"
       "L250 62L222 62A20 20 0 0 0 182 62L82 62A20 20 0 0 0 42 62L8 62Z")
CAR_WIN = "M92 27C104 21 126 19 148 20C162 21 172 24 182 30L190 36L88 36Z"


def _scene_vehicles(d, x, y, w, h, u):
    cx, base = x + w / 2 - 80, y + h - 34
    d.defs.append(f'<linearGradient id="{u}sp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9d6ff" stop-opacity=".22"/>'
                  f'<stop offset="1" stop-color="#e9d6ff" stop-opacity="0"/></linearGradient>'
                  f'<radialGradient id="{u}fl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{C["purple"]}" stop-opacity=".45"/>'
                  f'<stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></radialGradient>')
    d.style(f".{u}c{{animation:{u}c 4.5s ease-in-out infinite alternate}}@keyframes {u}c{{from{{transform:translateX(-6px)}}to{{transform:translateX(6px)}}}}"
            f".{u}v{{animation:{u}v 3s cubic-bezier(.3,0,.2,1) infinite alternate}}@keyframes {u}v{{from{{transform:scaleX(.35)}}to{{transform:scaleX(1)}}}}")
    s = [f'<polygon points="{cx - 30},{y} {cx + 30},{y} {cx + 120},{base} {cx - 120},{base}" fill="url(#{u}sp)"/>',
         f'<ellipse cx="{cx}" cy="{base}" rx="150" ry="20" fill="url(#{u}fl)"/>',
         f'<ellipse cx="{cx}" cy="{base}" rx="128" ry="14" fill="none" stroke="{C["purple_ink"]}" stroke-width="1.5" opacity=".8"/>',
         f'<ellipse id="{u}orb" cx="{cx}" cy="{base - 26}" rx="168" ry="40" fill="none" stroke="{C["line"]}" stroke-dasharray="3 6"/>']
    car = (f'<g transform="translate({cx - 129} {base - 66})"><path d="{CAR}" fill="#0a090d" stroke="{C["purple_ink"]}" stroke-width="1.6"/>'
           f'<path d="{CAR_WIN}" fill="#1f1530" stroke="{C["purple"]}" stroke-opacity=".6"/>'
           f'<circle cx="62" cy="62" r="15" fill="#0a090d" stroke="#3a3842" stroke-width="3"/><circle cx="202" cy="62" r="15" fill="#0a090d" stroke="#3a3842" stroke-width="3"/>'
           f'<circle cx="62" cy="62" r="5" fill="{C["purple_ink"]}"/><circle cx="202" cy="62" r="5" fill="{C["purple_ink"]}"/>'
           f'<path d="M238 47h10" stroke="#e8fbff" stroke-width="3" stroke-linecap="round"/><path d="M10 52h8" stroke="{C["purple"]}" stroke-width="3" stroke-linecap="round"/></g>')
    s.append(f'<g class="{u}c">{car}</g>')
    s.append(f'<circle r="4.5" fill="{C["cyan"]}"><animateMotion dur="7s" repeatCount="indefinite" '
             f'path="M{cx + 168} {base - 26}A168 40 0 1 1 {cx - 168} {base - 26}A168 40 0 1 1 {cx + 168} {base - 26}"/></circle>')
    # spec bars
    sx = x + w - 150
    for i, (lab, frac) in enumerate([("SPEED", .82), ("ACCEL", .7), ("BRAKES", .58), ("GRIP", .76)]):
        ty = y + 30 + i * 30
        t, _ = d.text(lab, sx, ty, "mono", 600, 11, fill=C["subtle"], ls=0.14)
        s.append(t + f'<rect x="{sx}" y="{ty + 7}" width="120" height="6" rx="3" fill="#25242b"/>'
                 f'<rect class="{u}v" style="transform-box:fill-box;transform-origin:left;animation-delay:-{i * .4}s" x="{sx}" y="{ty + 7}" width="{120 * frac:.0f}" height="6" rx="3" fill="{C["purple"] if i else C["cyan"]}"/>')
    return "".join(s)


def _scene_inventory(d, x, y, w, h, u, items):
    keys = ["ore", "ingot", "pickaxe", "axe", "chainbody", "platebody"]
    slot, gap = 74, 12
    total = len(keys) * slot + (len(keys) - 1) * gap
    x0, sy = x + (w - total) / 2, y + 32
    steps = len(keys)
    frames = "".join(f"{i * 100 / steps:.2f}%{{transform:translateX({i * (slot + gap)}px)}}" for i in range(steps))
    d.style(f".{u}sel{{animation:{u}sel 7.2s steps(1) infinite}}@keyframes {u}sel{{{frames}}}")
    s = []
    for i, k in enumerate(keys):
        sx = x0 + i * (slot + gap)
        s.append(f'<rect x="{fmt(sx)}" y="{sy}" width="{slot}" height="{slot}" rx="14" fill="#17161c" stroke="{C["line"]}"/>'
                 f'<image href="{items[k]}" x="{fmt(sx + 9)}" y="{sy + 7}" width="56" height="56"/>')
        n, _ = d.text(str(i + 1), sx + 10, sy + 17, "mono", 600, 11, fill=C["subtle"])
        s.append(n)
        if k in ("pickaxe", "axe"):
            s.append(f'<rect x="{fmt(sx + 12)}" y="{sy + slot - 9}" width="{slot - 24}" height="3" rx="1.5" fill="#2e2d35"/>'
                     f'<rect x="{fmt(sx + 12)}" y="{sy + slot - 9}" width="{(slot - 24) * (0.8 if k == "pickaxe" else 0.55):.0f}" height="3" rx="1.5" fill="{C["cyan"]}"/>')
    s.append(f'<rect class="{u}sel" x="{fmt(x0 - 3)}" y="{sy - 3}" width="{slot + 6}" height="{slot + 6}" rx="16" fill="none" '
             f'stroke="{C["purple"]}" stroke-width="2.5"/>')
    tag, tw = pill(d, x0, sy + slot + 14, "metadata  ·  durability  ·  hooks", h=26, family="mono", weight=500, size=12,
                   fill="#141318", stroke=C["line"], color=C["muted"], pad=12)
    s.append(tag)
    return "".join(s)


def _scene_interface(d, x, y, w, h, u):
    d.style(f".{u}g{{animation:{u}g 5s ease-in-out infinite alternate}}"
            f"@keyframes {u}g{{from{{stroke-dashoffset:var(--a)}}to{{stroke-dashoffset:var(--b)}}}}"
            f".{u}t{{animation:{u}t 4s cubic-bezier(.34,1.56,.64,1) infinite alternate}}@keyframes {u}t{{0%,40%{{transform:translateX(0)}}60%,100%{{transform:translateX(66px)}}}}")
    s = []
    # HUD status rings
    rings = [("heart", .82, C["ink"]), ("shield", .6, C["purple_ink"]), ("brain", .34, C["cyan"])]
    for i, (ic, frac, col) in enumerate(rings):
        cx, cy, r = x + 56 + i * 70, y + h - 52, 25
        circ = 2 * math.pi * r
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0d0d11" stroke="#25242b" stroke-width="5"/>'
                 f'<circle class="{u}g" style="--a:{circ * (1 - frac):.1f};--b:{circ * (1 - frac + .18):.1f};animation-delay:-{i * 1.3}s" '
                 f'cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round" '
                 f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ * (1 - frac):.1f}" transform="rotate(-90 {cx} {cy})"/>')
        icn = ic if ic != "brain" else "zap"
        if icn == "heart":
            icn = "activity"
        s.append(lucide(icn, cx - 10, cy - 10, 20, stroke=col, sw=2))
    # theme switch capsule
    tx, ty = x + 26, y + 24
    s.append(f'<rect x="{tx}" y="{ty}" width="140" height="38" rx="19" fill="#17161c" stroke="{C["line"]}"/>'
             f'<rect class="{u}t" x="{tx + 4}" y="{ty + 4}" width="66" height="30" rx="15" fill="{C["purple"]}"/>')
    a, _ = d.text("Light", tx + 37, ty + 24, "manrope", 700, 13, fill=C["ink"], anchor="middle")
    b, _ = d.text("Dark", tx + 103, ty + 24, "manrope", 700, 13, fill=C["ink"], anchor="middle")
    s += [a, b]
    # controller + hints
    hints = [("A", "Select"), ("B", "Back"), ("LB/RB", "Tabs")]
    hw = sum(d.measure(k, "manrope", 800, 11.5) + 14 + 5 + d.measure(l, "manrope", 600, 12) + 10 for k, l in hints) - 10
    bw = hw + 32
    gx = x + w - 26 - bw
    s.append(f'<rect x="{fmt(gx)}" y="{y + 20}" width="{fmt(bw)}" height="{h - 40}" rx="16" fill="#17161c" stroke="{C["line"]}"/>')
    s.append(lucide("gamepad-2", gx + bw / 2 - 32, y + 32, 64, stroke=C["ink"], sw=1.5))
    hx = gx + 16
    for key, lab in hints:
        kw = d.measure(key, "manrope", 800, 11.5) + 14
        s.append(f'<rect x="{fmt(hx)}" y="{y + h - 48}" width="{fmt(kw)}" height="20" rx="10" fill="{C["purple_soft"]}" stroke="{C["purple"]}" stroke-opacity=".6"/>')
        kt, _ = d.text(key, hx + kw / 2, y + h - 34, "manrope", 800, 11.5, fill=C["purple_ink"], anchor="middle")
        lt, lw = d.text(lab, hx + kw + 5, y + h - 34, "manrope", 600, 12, fill=C["muted"])
        s += [kt, lt]
        hx += kw + 5 + lw + 10
    return "".join(s)


SYSTEMS = [
    ("staff", "shield-check", "STAFF & ADMIN", "Staff dashboard",
     "A modular admin NUI with 23 modules: bans, permissions, players, vehicles, finance and gangs, with every "
     "action sent to a rate-limited audit log.",
     ["staff v2.0.0", "reborn_logs v2.0.0"], _scene_staff),
    ("skills", "pickaxe", "SKILLS & PROGRESSION", "Skills ecosystem",
     "One core API drives eight skills (mining, woodcutting, fishing, hunting, diving, combat, smithing, "
     "carpentry) with XP bombs and leaderboards.",
     ["skills_core v1.2.0", "8 skills", "server-validated"], _scene_skills),
    ("crafting", "anvil", "CRAFTING & ECONOMY", "Crafting and trade",
     "One engine behind every crafting station (repairs, enhancements, leaderboards), a server-owned trade "
     "centre with restocks, and org-run black markets.",
     ["skills_crafting v2.0.0", "skills_vendors", "reborn_orgs"], _scene_crafting),
    ("vehicles", "car-front", "VEHICLE SYSTEMS", "Dealerships and classes",
     "Orbit-camera showrooms, server-side purchases, weekly limited-stock rotations, test drives and "
     "auto-captured vehicle photos, graded by one class system.",
     ["reborn_vehicleshop", "reborn_vehicleclass v2.0.0"], _scene_vehicles),
    ("inventory", "package", "INVENTORY INTEGRATIONS", "Items on ox_inventory",
     "Custom item lines like Rebornium ore, bars, tools and armour, metadata-driven phone cases, and hooks "
     "that log every item movement.",
     ["ox_inventory", "reborn_phone_cases", "reborn_logs hooks"], _scene_inventory),
    ("interface", "layout-dashboard", "INTERFACE & DEV TOOLS", "Reborn UI and tooling",
     "One design system for every NUI: two themes, controller support, restyled ox_lib, ox_target and "
     "ox_inventory, plus a pad probe and headless UI checks.",
     ["reborn_ui", "reborn_hud", "reborn_pad_probe"], _scene_interface),
]


def systems_row(path, pair, row):
    cw, ch, gap = 588, 418, 24
    d = Doc(W, ch, " and ".join(p[3] for p in pair),
            " ".join(f"{p[3]}: {p[4]} Resources: {', '.join(p[5])}." for p in pair))
    items = _items() if any(p[0] in ("crafting", "inventory") for p in pair) else None
    for i, (key, icon, kicker, title, desc, chips, scene) in enumerate(pair):
        ox = i * (cw + gap)
        u = f"{key[:2]}{i}"
        body = [card(d, cw, ch, u, glow=(0.5, 0.0))]
        ill_h = 168
        d.defs.append(f'<clipPath id="{u}cl"><rect x="1" y="1" width="{cw - 2}" height="{ill_h}" rx="19"/></clipPath>'
                      f'<linearGradient id="{u}ib" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1029"/>'
                      f'<stop offset="1" stop-color="{CARD}"/></linearGradient>')
        args = (d, 0, 0, cw, ill_h, u) + ((items,) if key in ("crafting", "inventory") else ())
        body.append(f'<g clip-path="url(#{u}cl)"><rect width="{cw}" height="{ill_h}" fill="url(#{u}ib)"/>{scene(*args)}</g>')
        body.append(f'<path d="M24 {ill_h + 0.5}H{cw - 24}" stroke="{C["line"]}"/>')
        body.append(icon_tile(26, ill_h + 22, icon, size=46))
        k, _ = d.text(f"SYS 0{row * 2 + i + 1}  /  {kicker}", 86, ill_h + 39, "mono", 600, 12, fill=C["cyan"], ls=0.14)
        t, _ = d.text(title, 86, ill_h + 67, "sora", 700, 24, fill=C["ink"])
        body += [k, t]
        lines = wrap(d, desc, "manrope", 500, 17.5, cw - 52)
        assert len(lines) <= 3, f"{key}: description needs {len(lines)} lines"
        for j, line in enumerate(lines):
            lt, _ = d.text(line, 26, ill_h + 106 + j * 26, "manrope", 500, 17.5, fill=C["muted"])
            body.append(lt)
        cx = 26
        for chip in chips:
            sv, pw = pill(d, cx, ch - 54, chip, h=32, family="mono", weight=500, size=14, fill="#17161c",
                          stroke=C["line"], color=C["ink"], pad=13)
            body.append(sv)
            cx += pw + 8
        assert cx <= cw - 18, f"{key}: chips overflow"
        d.add(f'<g transform="translate({ox} 0)">{"".join(body)}</g>')
    return d.save(path)


# ------------------------------------------------------------ repositories --

REPOS = [
    ("Reborn-Design-Vehicles", "car", "Civilian, police, EMS, fire and security fleets, wheels and paints."),
    ("Reborn-Design-Clothing", "shirt", "Civilian, police, EMS and business uniforms and outfits."),
    ("Reborn-Design-Maps", "map", "Curated MLOs, interiors, terrain and map fixes for the city."),
    ("Reborn-Design-Weapons", "crosshair", "Weapon models and skins, plus the Reborn pickaxes and axes."),
]


def repos(path):
    h = 470
    d = Doc(W, h, "Project repositories",
            "Private repositories behind Project Reborn RP. RebornRP: the server monorepo with 230+ resources, four asset "
            "submodules, written in Lua, TypeScript, JavaScript and SQL, repo created in October 2024. Asset submodules: "
            + "; ".join(f"{n}: {t}" for n, _, t in REPOS))
    d.style(".lk{animation:lk 3s ease-in-out infinite}@keyframes lk{0%,100%{opacity:1}50%{opacity:.4}}"
            ".fl{animation:fl 2.5s linear infinite}@keyframes fl{to{stroke-dashoffset:-20}}")
    body = [card(d, W, h, "r", glow=(0.2, 0.0), grid=True)]
    # featured monorepo
    fx, fy, fw, fh = 28, 28, 560, h - 56 - 52
    body.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="18" fill="{PANEL}" stroke="{C["purple"]}" stroke-opacity=".5"/>')
    body.append(lucide("lock", fx + 26, fy + 26, 20, stroke=C["purple_ink"], sw=2))
    n, nw = d.text("StigmaAU / RebornRP", fx + 56, fy + 42, "mono", 600, 17, fill=C["ink"])
    body.append(n)
    pv, _ = pill(d, fx + fw - 26 - 92, fy + 24, "Private", h=26, size=12.5, fill=C["purple_soft"], stroke=C["purple"],
                 color=C["purple_ink"], dot=C["purple_ink"], dot_cls="lk", pad=12)
    body.append(pv)
    t, _ = d.text("Project Reborn RP server", fx + 26, fy + 92, "sora", 700, 28, fill=C["ink"])
    body.append(t)
    for j, line in enumerate(wrap(d, "The whole city in one tree: every Reborn resource, framework configuration and "
                                     "integration, with streamed assets mounted as submodules so script developers "
                                     "never clone gigabytes they do not need.", "manrope", 500, 17, fw - 52)):
        lt, _ = d.text(line, fx + 26, fy + 128 + j * 25, "manrope", 500, 17, fill=C["muted"])
        body.append(lt)
    stats = [("230+", "resources"), ("4", "asset submodules"), ("2024", "repo created")]
    sw = (fw - 52 - 24) / 3
    for j, (num, lab) in enumerate(stats):
        sx = fx + 26 + j * (sw + 12)
        body.append(f'<rect x="{fmt(sx)}" y="{fy + 222}" width="{fmt(sw)}" height="82" rx="14" fill="#121116" stroke="{C["line"]}"/>')
        nn, _ = d.text(num, sx + 18, fy + 262, "sora", 700, 28, fill=C["ink"], features={"tnum": True, "kern": True})
        ll, _ = d.text(lab, sx + 18, fy + 288, "manrope", 600, 14, fill=C["subtle"])
        body += [nn, ll]
    lx = fx + 26
    for lang, col in [("Lua", C["purple"]), ("TypeScript", C["cyan"]), ("JavaScript", "#e9dcff"), ("SQL", C["purple_ink"])]:
        body.append(f'<circle cx="{lx + 5}" cy="{fy + fh - 28}" r="5" fill="{col}"/>')
        lt, lw = d.text(lang, lx + 16, fy + fh - 23, "manrope", 600, 15, fill=C["muted"])
        body.append(lt)
        lx += 16 + lw + 22

    # submodules
    rx, rw = fx + fw + 48, W - 28 - (fx + fw + 48)
    rh, rg = (fh - 3 * 12) / 4, 12
    trunk_x = fx + fw + 24
    body.append(f'<path d="M{fx + fw} {fy + 60}H{trunk_x}V{fy + fh - rh / 2}" fill="none" stroke="{C["line"]}" stroke-width="2"/>'
                f'<path class="fl" d="M{fx + fw} {fy + 60}H{trunk_x}V{fy + fh - rh / 2}" fill="none" stroke="{C["purple_ink"]}" stroke-width="2" stroke-dasharray="4 16"/>')
    for j, (name, icon, desc) in enumerate(REPOS):
        ry = fy + j * (rh + rg)
        body.append(f'<path d="M{trunk_x} {fmt(ry + rh / 2)}H{rx}" stroke="{C["line"]}" stroke-width="2"/>'
                    f'<circle cx="{trunk_x}" cy="{fmt(ry + rh / 2)}" r="4" fill="{C["purple_ink"]}"/>')
        body.append(f'<rect x="{rx}" y="{fmt(ry)}" width="{rw}" height="{fmt(rh)}" rx="16" fill="{PANEL}" stroke="{C["line"]}"/>')
        body.append(icon_tile(rx + 16, ry + (rh - 42) / 2, icon, size=42, rx=12))
        nt, _ = d.text(name, rx + 72, ry + rh / 2 - 4, "mono", 600, 15.5, fill=C["ink"])
        dt, _ = d.text(desc, rx + 72, ry + rh / 2 + 19, "manrope", 500, 14.5, fill=C["muted"])
        body += [nt, dt]
        body.append(lucide("lock", rx + rw - 36, ry + 16, 16, stroke=C["subtle"], sw=2))
    note, _ = d.text("Source is private: the city's code stays in the city. Every system on this page lives in these repositories.",
                     W / 2, h - 30, "manrope", 600, 15, fill=C["subtle"], anchor="middle")
    body.append(note)
    d.add(*body)
    return d.save(path)


# -------------------------------------------------------------- philosophy --

PRINCIPLES = [
    ("gauge", "Performance first", "Event-driven code, cached natives, ox_target and zones over polling loops."),
    ("shield-check", "The server decides", "Every price, rank and balance is checked server-side. Clients only ask."),
    ("boxes", "Modular resources", "Small resources, clean exports: one skills core feeds eight skills."),
    ("file-code-2", "Maintainable architecture", "Config-driven and documented, with SQL migrations and audits in-repo."),
    ("sparkles", "Polished interfaces", "One design system for every NUI: two themes and controller support."),
]


def philosophy(path):
    rows_h, top = 72, 30
    h = top * 2 + len(PRINCIPLES) * rows_h
    d = Doc(W, h, "Development philosophy",
            " ".join(f"{t}: {s}" for _, t, s in PRINCIPLES)
            + " Diagram: player input passes through the client to server validation, then oxmysql, then synced state.")
    d.style(".fp{animation:fp 4.8s linear infinite}@keyframes fp{0%{transform:translateY(0);opacity:0}6%{opacity:1}94%{opacity:1}100%{transform:translateY(var(--run));opacity:0}}"
            ".vn{animation:vn 2.4s ease-in-out infinite}@keyframes vn{0%,100%{opacity:.25}50%{opacity:.7}}")
    body = [card(d, W, h, "p", glow=(0.0, 1.0), grid=True)]
    lw = 760
    for i, (icon, title, text) in enumerate(PRINCIPLES):
        y = top + i * rows_h
        if i:
            body.append(f'<path d="M110 {y}H{lw}" stroke="{C["line"]}"/>')
        nm, _ = d.text(f"0{i + 1}", 30, y + 42, "mono", 600, 13, fill=C["cyan"], ls=0.1)
        body.append(nm)
        body.append(icon_tile(58, y + 13, icon, size=46))
        t, _ = d.text(title, 122, y + 32, "sora", 700, 19, fill=C["ink"])
        s, sw = d.text(text, 122, y + 56, "manrope", 500, 16, fill=C["muted"])
        assert 122 + sw < lw + 30, f"{title} too long"
        body += [t, s]

    # validation pipeline
    px, pw = lw + 60, W - 28 - (lw + 60)
    body.append(f'<rect x="{px}" y="{top - 4}" width="{pw}" height="{h - top * 2 + 8}" rx="18" fill="{PANEL}" stroke="{C["line"]}"/>')
    kk, _ = d.text("REQUEST PATH", px + 22, top + 24, "mono", 600, 12, fill=C["subtle"], ls=0.16)
    body.append(kk)
    nodes = [("gamepad-2", "Player input"), ("monitor", "NUI and client"), ("shield-check", "Server validation"),
             ("database", "oxmysql"), ("workflow", "Synced state")]
    ny0, nstep = top + 50, (h - top * 2 - 70) / (len(nodes) - 1)
    lx = px + 40
    run = nstep * (len(nodes) - 1)
    body.append(f'<path d="M{lx} {ny0}V{fmt(ny0 + run)}" stroke="{C["line"]}" stroke-width="2"/>')
    for j, delay in enumerate([0, -1.6, -3.2]):
        body.append(f'<circle class="fp" style="--run:{fmt(run)}px;animation-delay:{delay}s" cx="{lx}" cy="{ny0}" r="4" fill="{C["cyan"]}"/>')
    for j, (icon, lab) in enumerate(nodes):
        ny = ny0 + j * nstep
        key = j == 2
        if key:
            body.append(f'<rect class="vn" x="{px + 14}" y="{fmt(ny - 22)}" width="{pw - 28}" height="44" rx="22" fill="{C["purple"]}" opacity=".3"/>')
        body.append(f'<circle cx="{lx}" cy="{fmt(ny)}" r="15" fill="{C["purple"] if key else "#1f1e25"}" stroke="{C["purple_ink"] if key else C["line"]}"/>')
        body.append(lucide(icon, lx - 9, ny - 9, 18, stroke=C["ink"] if key else C["purple_ink"], sw=2))
        lt, _ = d.text(lab, lx + 28, ny + 5.5, "manrope", 700 if key else 600, 16, fill=C["ink"] if key else C["muted"])
        body.append(lt)
    d.add(*body)
    return d.save(path)


# ------------------------------------------------------------------ footer --

def footer(path):
    h = 230
    R = random.Random(11)
    d = Doc(W, h, "Built in Brisbane for the city of Reborn",
            "Footer: the Project Reborn R mark above a night skyline. Built in Brisbane for the city of Reborn.")
    rmark, _ = png_data_uri(os.path.join(HERE, "brand", "r-mark.png"), width=120, colors=96)
    d.style(".fw{animation:fw 5s ease-in-out infinite}@keyframes fw{0%,100%{opacity:.6}50%{opacity:1}}"
            ".fz{animation:fz 7s steps(1) infinite}@keyframes fz{0%,100%{opacity:.9}40%{opacity:.3}44%{opacity:.9}}")
    d.defs.append(f'<clipPath id="fc"><rect width="{W}" height="{h}" rx="20"/></clipPath>'
                  f'<linearGradient id="fsk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CARD}"/>'
                  f'<stop offset=".7" stop-color="#1d0d33"/><stop offset="1" stop-color="#2a0f4c"/></linearGradient>'
                  f'<radialGradient id="fgl" cx=".5" cy="1" r=".6"><stop offset="0" stop-color="{C["purple"]}" stop-opacity=".4"/>'
                  f'<stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></radialGradient>'
                  f'<linearGradient id="fe" x1="0" x2="1"><stop offset="0" stop-color="{C["purple"]}" stop-opacity="0"/>'
                  f'<stop offset=".5" stop-color="{C["purple_ink"]}"/><stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></linearGradient>')
    g = [f'<rect width="{W}" height="{h}" fill="url(#fsk)"/>', f'<rect width="{W}" height="{h}" fill="url(#fgl)" class="fw"/>']
    sky, lit, x = [], [], 0
    while x < W:
        w = R.randrange(16, 40)
        dist = abs(x + w / 2 - W / 2)
        top = h - R.randrange(18, 40) - (0 if dist < 260 else int((dist - 260) / 11) + R.randrange(0, 30))
        if dist < 150:
            top = h - R.randrange(14, 28)
        sky.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h - top}"/>')
        for _ in range(int((h - top) * w / 260)):
            lit.append(f'<rect x="{x + R.randrange(2, max(3, w - 4))}" y="{R.randrange(top + 4, h - 4)}" width="2.5" height="3.5"/>')
        x += w + R.randrange(0, 3)
    g.append(f'<g fill="#0a0712">{"".join(sky)}</g><g fill="{C["purple_ink"]}" class="fz">{"".join(lit)}</g>')
    g.append(f'<path d="M0 {h - 0.5}H{W}" stroke="url(#fe)" stroke-width="2"/>')
    g.append(f'<image href="{rmark}" x="{W / 2 - 24}" y="34" width="48" height="{48 * 357 / 360:.1f}"/>')
    t, _ = d.text("Built in Brisbane for the city of Reborn", W / 2, 124, "sora", 700, 24, fill=C["ink"], anchor="middle")
    s, _ = d.text("PROJECT REBORN RP  ·  NSW INSPIRED  ·  CUSTOM SCRIPTS", W / 2, 154, "mono", 500, 13, fill=C["muted"],
                  anchor="middle", ls=0.18)
    g += [t, s]
    d.add(f'<g clip-path="url(#fc)">{"".join(g)}</g>',
          f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="19.5" fill="none" stroke="{C["line"]}"/>')
    return d.save(path)


def discord_button(path):
    d = Doc(320, 56, "Join the city on Discord", "Button: join Project Reborn RP on Discord.")
    s, w = pill(d, 0, 0, "Join the city on Discord", h=56, size=18, weight=700, fill=C["purple"], icon="discord",
                icon_kind="brand", icon_color=C["ink"], pad=24)
    d.w = round(w)
    d.add(s)
    return d.save(path)


def _headers(_):
    sizes = {}
    for num, icon, title, right in HEADERS:
        name = f"header-{num}.svg"
        sizes[name] = header(os.path.join(os.path.dirname(HERE), name), num, icon, title, right)
    return sizes


def _systems(_):
    out = {}
    for row in range(3):
        name = f"systems-{row + 1}.svg"
        out[name] = systems_row(os.path.join(os.path.dirname(HERE), name), SYSTEMS[row * 2:row * 2 + 2], row)
    return out


TARGETS = {
    "headers": _headers,
    "dossier": dossier,
    "stack": stack,
    "systems": _systems,
    "repos": repos,
    "philosophy": philosophy,
    "footer": footer,
    "discord": discord_button,
}
