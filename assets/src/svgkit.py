"""Small SVG toolkit for the profile assets.

GitHub shows README images through <img>, which cannot load web fonts, so every
piece of text is converted to vector outlines here. Each glyph is stored once in
<defs> (in font units, y flipped) and placed with <use>, which keeps files small.
Shaping goes through HarfBuzz so kerning matches the real fonts.
"""

import base64
import io
import os
from xml.sax.saxutils import escape

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_FILES = {
    "sora": os.path.join(HERE, "fonts", "sora.woff2"),
    "manrope": os.path.join(HERE, "fonts", "manrope.woff2"),
    "mono": os.path.join(HERE, "fonts", "jetbrains-mono.woff2"),
}

# Project Reborn tokens (dark theme, from reborn_ui/ui/tokens.css) plus the
# profile's restrained cyan accent.
C = {
    "night": "#08070c",
    "canvas": "#121215",
    "surface": "#1b1b1f",
    "raised": "#242429",
    "sunken": "#16161a",
    "line": "#2f2f36",
    "ink": "#f3f2f6",
    "muted": "#a8a6b3",
    "subtle": "#8f8d9b",
    "purple": "#a219ff",
    "purple_strong": "#8c1ff0",
    "purple_ink": "#c895ff",
    "purple_soft": "#2e1a45",
    "cyan": "#5be4ff",
}


class Font:
    _cache = {}

    def __init__(self, family, weight):
        tt = TTFont(FONT_FILES[family])
        if "fvar" in tt:
            tt = instancer.instantiateVariableFont(tt, {"wght": weight}, inplace=False)
        tt.flavor = None
        buf = io.BytesIO()
        tt.save(buf)
        self.tt = TTFont(io.BytesIO(buf.getvalue()))
        self.upm = self.tt["head"].unitsPerEm
        self.glyphset = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.cmap = self.tt.getBestCmap()
        self.hb = hb.Font(hb.Face(hb.Blob(buf.getvalue())))
        self.key = {"sora": "s", "manrope": "m", "mono": "j"}[family] + str(weight // 100)
        self.cap = getattr(self.tt["OS/2"], "sCapHeight", 0) or int(self.upm * 0.7)
        self._paths = {}

    @classmethod
    def get(cls, family, weight):
        k = (family, weight)
        if k not in cls._cache:
            cls._cache[k] = Font(family, weight)
        return cls._cache[k]

    def shape(self, text, features=None):
        for ch in text:
            if ch != " " and ord(ch) not in self.cmap:
                raise ValueError(f"{self.key}: no glyph for {ch!r} in {text!r}")
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, features or {"kern": True, "liga": True})
        return [
            (self.order[i.codepoint], p.x_advance, p.x_offset, p.y_offset)
            for i, p in zip(buf.glyph_infos, buf.glyph_positions)
        ]

    def path(self, gname):
        if gname not in self._paths:
            pen = SVGPathPen(self.glyphset, ntos=lambda v: str(round(v)))
            self.glyphset[gname].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
            self._paths[gname] = pen.getCommands()
        return self._paths[gname]


def fmt(v):
    """Compact number formatting for attributes."""
    v = round(v, 2)
    return str(int(v)) if v == int(v) else f"{v:.2f}".rstrip("0").rstrip(".")


class Doc:
    def __init__(self, w, h, title, desc=""):
        self.w, self.h = w, h
        self.title, self.desc = title, desc
        self.defs = []
        self.glyph_ids = {}
        self.styles = []
        self.body = []

    # ---- text -------------------------------------------------------------
    def measure(self, text, family, weight, size, ls=0.0, features=None):
        f = Font.get(family, weight)
        run = f.shape(text, features)
        adv = sum(a for _, a, _, _ in run) + ls * f.upm * max(len(run) - 1, 0)
        return adv * size / f.upm

    def text(self, text, x, y, family="manrope", weight=500, size=16, fill=None,
             anchor="start", ls=0.0, opacity=None, cls=None, features=None, extra=""):
        """Place `text` with its baseline at y. ls is letter spacing in em.
        Returns (svg, width)."""
        f = Font.get(family, weight)
        run = f.shape(text, features)
        lsu = ls * f.upm
        total = sum(a for _, a, _, _ in run) + lsu * max(len(run) - 1, 0)
        k = size / f.upm
        if anchor == "middle":
            x -= total * k / 2
        elif anchor == "end":
            x -= total * k
        uses, pen = [], 0
        for gname, adv, xo, yo in run:
            if f.path(gname):
                gid = self._glyph(f, gname)
                attrs = f'href="#{gid}"'
                if pen + xo:
                    attrs += f' x="{round(pen + xo)}"'
                if yo:
                    attrs += f' y="{-yo}"'
                uses.append(f"<use {attrs}/>")
            pen += adv + lsu
        a = f' fill="{fill}"' if fill else ""
        if opacity is not None:
            a += f' opacity="{fmt(opacity)}"'
        if cls:
            a += f' class="{cls}"'
        svg = (f'<g transform="translate({fmt(x)} {fmt(y)}) scale({k:.5g})"{a}{extra}>'
               + "".join(uses) + "</g>")
        return svg, total * k

    def _glyph(self, f, gname):
        key = (f.key, gname)
        if key not in self.glyph_ids:
            gid = f"{f.key}{len(self.glyph_ids):x}"
            self.glyph_ids[key] = gid
            self.defs.append(f'<path id="{gid}" d="{f.path(gname)}"/>')
        return self.glyph_ids[key]

    # ---- assembly ---------------------------------------------------------
    def add(self, *parts):
        self.body.extend(parts)

    def style(self, css):
        self.styles.append(css)

    def render(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}" role="img" aria-labelledby="t d">'
                f'<title id="t">{escape(self.title)}</title><desc id="d">{escape(self.desc)}</desc>')
        css = ""
        if self.styles:
            css = ("<style>" + "".join(self.styles)
                   + "@media (prefers-reduced-motion: reduce){*{animation:none!important}}</style>")
        defs = "<defs>" + "".join(self.defs) + "</defs>" if self.defs else ""
        return head + css + defs + "".join(self.body) + "</svg>"

    def save(self, path):
        data = self.render()
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(data)
        return len(data.encode())


# ---- shared helpers -------------------------------------------------------

def png_data_uri(path, width=None, colors=None):
    im = Image.open(path).convert("RGBA")
    if width and im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    if colors:
        im = im.quantize(colors=colors, method=Image.FASTOCTREE, dither=Image.NONE)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.size


def lucide(name, x, y, size=24, stroke=None, sw=1.75, opacity=None, extra=""):
    from icons import LUCIDE
    k = size / 24
    o = f' opacity="{fmt(opacity)}"' if opacity is not None else ""
    return (f'<g transform="translate({fmt(x)} {fmt(y)}) scale({k:.4g})" fill="none" '
            f'stroke="{stroke or C["purple_ink"]}" stroke-width="{fmt(sw)}" stroke-linecap="round" '
            f'stroke-linejoin="round"{o}{extra}>{LUCIDE[name]}</g>')


def brand_icon(name, x, y, size=24, fill=None, opacity=None):
    from icons import BRANDS
    k = size / 24
    o = f' opacity="{fmt(opacity)}"' if opacity is not None else ""
    return (f'<path transform="translate({fmt(x)} {fmt(y)}) scale({k:.4g})" '
            f'fill="{fill or C["ink"]}"{o} d="{BRANDS[name]}"/>')


def corner_brackets(x, y, w, h, l=18, color=None, sw=1.5, opacity=0.8):
    c = color or C["cyan"]
    p = (f"M{x} {y + l}V{y}H{x + l}M{x + w - l} {y}H{x + w}V{y + l}"
         f"M{x + w} {y + h - l}V{y + h}H{x + w - l}M{x + l} {y + h}H{x}V{y + h - l}")
    return (f'<path d="{p}" fill="none" stroke="{c}" stroke-width="{sw}" '
            f'stroke-linecap="square" opacity="{fmt(opacity)}"/>')
