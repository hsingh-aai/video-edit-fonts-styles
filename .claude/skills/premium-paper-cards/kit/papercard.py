"""Premium paper cards: a real screenshot or UI 'printed' on white paper with torn, deckled edges, a strip of
translucent tape, a soft two-layer shadow and fine grain, plus a yellow highlighter that swipes across the exact
words as they are spoken. Sponsor-free and style-agnostic; see ../SKILL.md.

Reuses the Mariah Paper kit's noise (`_noise`) for grain; everything else here is new. PIL only.

    card = PaperCard(900, 420, seed=3)                 # fixed size -> torn mask, shadow and tape are cached
    rgba = card.render(content, marks=[Mark((x0, y0, x1, y1), t_at=1.2)], u=1.5)
    # place rgba with motion(): drop-and-settle or slide-up, see motion() below
"""
import math, os, random, sys
from functools import lru_cache
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../mariah-paper-style/kit'))
from mariahpaper import _noise          # noqa: E402  (shared paper noise)

PAPER = (251, 250, 246)                  # printer paper, a hair warm
MARKER = (255, 214, 50)                  # highlighter yellow (multiply on light, 55% over on dark)
TAPE = (236, 238, 232)                   # translucent matte tape
INK, MUTED, RED_PEN, GREEN_INK = (24, 22, 20), (128, 124, 118), (214, 48, 40), (22, 150, 80)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(x):
    x = clamp(x); return 1 - (1 - x) ** 3


# ---------- the torn sheet ----------
def _edge(n, seed, amp, fine):
    """1-D deckle profile: a slow wave plus fine jagged fibres, in pixels."""
    rnd = random.Random(seed)
    ph = [rnd.random() * 6.28 for _ in range(3)]
    out = []
    for i in range(n):
        x = i / max(1, n - 1)
        slow = amp * 0.45 * (math.sin(x * 9 + ph[0]) + 0.6 * math.sin(x * 23 + ph[1]) + 0.3 * math.sin(x * 51 + ph[2]))
        out.append(slow + rnd.uniform(-fine, fine))
    return out


@lru_cache(None)
def torn_mask(w, h, seed=1, amp=7, fine=3.2, torn=('top', 'bottom', 'left', 'right')):
    """Alpha mask of a torn sheet. Drawn at 2x and downsampled for clean fibres."""
    S = 2; W2, H2 = w * S, h * S; m = amp * S + 8
    pts = []
    step = 6
    top = _edge(W2 // step + 1, seed, amp * S if 'top' in torn else 0, fine * S if 'top' in torn else 0)
    right = _edge(H2 // step + 1, seed + 1, amp * S if 'right' in torn else 0, fine * S if 'right' in torn else 0)
    bot = _edge(W2 // step + 1, seed + 2, amp * S if 'bottom' in torn else 0, fine * S if 'bottom' in torn else 0)
    left = _edge(H2 // step + 1, seed + 3, amp * S if 'left' in torn else 0, fine * S if 'left' in torn else 0)
    for i, v in enumerate(top):
        pts.append((i * step, m + v))
    for i, v in enumerate(right):
        pts.append((W2 - m + v, i * step))
    for i, v in enumerate(bot[::-1]):
        pts.append((W2 - i * step, H2 - m + v))
    for i, v in enumerate(left[::-1]):
        pts.append((m + v, H2 - i * step))
    im = Image.new('L', (W2, H2), 0)
    ImageDraw.Draw(im).polygon(pts, fill=255)
    return im.resize((w, h), Image.LANCZOS)


@lru_cache(None)
def paper(w, h, seed=1):
    """Paper texture: flat stock with very fine grain and a faint fibre-lit torn edge."""
    g = _noise((w // 2 + 1, h // 2 + 1), seed, 0.7).resize((w, h))
    base = Image.new('RGB', (w, h), PAPER)
    dark = Image.new('RGB', (w, h), (238, 236, 230))
    return Image.composite(base, dark, g.point(lambda v: 255 if v > 96 else 215))


@lru_cache(None)
def _shadow(w, h, seed, pad):
    """Two-layer shadow: a tight contact shadow and a broad soft one, offset down."""
    a = torn_mask(w, h, seed)
    big = Image.new('L', (w + 2 * pad, h + 2 * pad), 0); big.paste(a, (pad, pad + 14))
    near = Image.new('L', big.size, 0); near.paste(a, (pad, pad + 4))
    soft = big.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.42))
    tight = near.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.30))
    sh = ImageChops.lighter(soft, tight)
    layer = Image.new('RGBA', big.size, (10, 8, 6, 0)); layer.putalpha(sh)
    return layer


@lru_cache(None)
def tape(w=190, h=54, seed=1, angle=-3):
    """A strip of translucent matte tape with ragged short ends."""
    rnd = random.Random(seed)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lx = [rnd.uniform(0, 7) for _ in range(9)]; rx = [rnd.uniform(0, 7) for _ in range(9)]
    pts = [(lx[i], i * h / 8) for i in range(9)] + [(w - rx[i], h - i * h / 8) for i in range(9)]
    d.polygon(pts, fill=TAPE + (178,))
    g = _noise((w // 3 + 1, h // 3 + 1), seed, 0.6).resize((w, h)).point(lambda v: 150 + v // 5)
    im.putalpha(ImageChops.multiply(im.split()[3], g))
    d = ImageDraw.Draw(im)
    d.line([(6, 3), (w - 6, 3)], fill=(255, 255, 255, 70), width=2)     # faint sheen
    return im.rotate(angle, resample=Image.BICUBIC, expand=True)


# ---------- highlighter ----------
class Mark:
    """Highlighter swipe over box (content coords) that draws left -> right from t_at over dur seconds."""
    def __init__(self, box, t_at, dur=0.25, color=MARKER, t_off=None):
        self.box, self.t_at, self.dur, self.color, self.t_off = box, t_at, dur, color, t_off


def marker(im, box, p, color=MARKER, seed=0):
    """Draw a highlighter swipe (progress p 0..1) on an RGB/RGBA image in place. Multiply on light ground; on
    dark ground (a dark-mode screenshot) it inverts under the swipe, so light text becomes dark ink on yellow."""
    if p <= 0:
        return
    x0, y0, x1, y1 = [int(v) for v in box]
    x0 -= 8; x1 += 8; y0 -= 3; y1 += 3
    xe = int(x0 + (x1 - x0) * ease_out(p))
    if xe <= x0 + 2:
        return
    region = im.crop((x0, y0, xe, y1)).convert('RGB')
    lum = sum(region.convert('L').getdata()) / max(1, region.width * region.height)
    sw = Image.new('L', region.size, 0); d = ImageDraw.Draw(sw)
    rnd = random.Random(seed)
    hh = region.height
    d.rounded_rectangle([0, 1 + rnd.uniform(0, 2), region.width - 1, hh - 2 - rnd.uniform(0, 2)], radius=max(2, hh // 6), fill=255)
    sw = sw.filter(ImageFilter.GaussianBlur(0.8))
    col = Image.new('RGB', region.size, color)
    if lum > 110:
        out = Image.composite(ImageChops.multiply(region, col), region, sw)
    else:
        inv = ImageOps.autocontrast(ImageOps.invert(region.convert('L')), cutoff=2).convert('RGB')
        out = Image.composite(ImageChops.multiply(inv, col), region, sw)
    im.paste(out, (x0, y0))


# ---------- the card ----------
class PaperCard:
    """A fixed-size torn paper card. render() prints `content` (RGB/RGBA, any size <= inner box) centred on the
    sheet, swipes the marks that are due at time u, then returns an RGBA with shadow and (optional) tape."""
    def __init__(self, w, h, seed=1, tape_at=None, tape_w=None, margin=30):
        self.w, self.h, self.seed, self.margin = w, h, seed, margin
        self.tape_at, self.tape_w = tape_at, tape_w or min(220, int(w * 0.24))
        self.pad = 60

    def render(self, content=None, marks=(), u=99.0, draw=None):
        sheet = paper(self.w, self.h, self.seed).copy()
        if content is not None:
            c = content.convert('RGBA')
            ox, oy = (self.w - c.width) // 2, (self.h - c.height) // 2
            sheet.paste(c, (ox, oy), c)
        else:
            ox = oy = 0
        if draw:
            draw(sheet, u)
        for i, mk in enumerate(marks):
            if u >= mk.t_at and (mk.t_off is None or u < mk.t_off):
                x0, y0, x1, y1 = mk.box
                marker(sheet, (x0 + ox, y0 + oy, x1 + ox, y1 + oy), (u - mk.t_at) / mk.dur, mk.color, seed=i + self.seed)
        sheet = sheet.convert('RGBA'); sheet.putalpha(torn_mask(self.w, self.h, self.seed))
        out = _shadow(self.w, self.h, self.seed, self.pad).copy()
        out.alpha_composite(sheet, (self.pad, self.pad))
        if self.tape_at is not None and u >= self.tape_at:
            tp = tape(self.tape_w, 54, self.seed, angle=-3 + (self.seed % 5))
            a = clamp((u - self.tape_at) / 0.08)
            if a < 1:
                tp = tp.copy(); tp.putalpha(tp.split()[3].point(lambda v: int(v * a)))
            out.alpha_composite(tp, (self.pad + self.w // 2 - tp.width // 2, self.pad - tp.height // 2 + 4))
        return out


# ---------- motion (pure functions of t) ----------
def _spring(t, zeta, f):
    if t <= 0:
        return 0.0
    w = 2 * math.pi * f; wd = w * math.sqrt(1 - zeta * zeta)
    return 1 - math.exp(-zeta * w * t) * (math.cos(wd * t) + (zeta * w / wd) * math.sin(wd * t))


def motion(t, t_in, t_out, mode='drop', rot=0.0, phase=0.0, H=1920):
    """(scale, rotation_deg, dy_px, alpha) for an element at time t. None when hidden.
    drop: falls from 90px above with a slight overshoot (spring zeta 0.55, 3.2 Hz), scale 1.06 -> 1, a 2.5 deg
          wobble that decays in ~0.6 s, then an idle 0.35 deg sway.
    slide: rises from below the frame on a softer spring (zeta 0.78, 2.3 Hz).
    Exit (last 0.22 s): drops 140px and fades."""
    if t < t_in or t >= t_out:
        return None
    u = t - t_in
    if mode == 'slide':
        k = _spring(u, 0.78, 2.3); dy = (1 - k) * (H * 0.6); s = 1.0; extra = 1.2 * math.exp(-5 * u) * math.sin(u * 14)
    else:
        k = _spring(u, 0.55, 3.2); dy = (1 - k) * -90; s = 1.06 - 0.06 * min(1.0, k)
        extra = 2.5 * math.exp(-6 * u) * math.cos(2 * math.pi * 2.4 * u)
    a = clamp(u / 0.08)
    idle = 0.35 * math.sin(2 * math.pi * 0.35 * u + phase)
    if t > t_out - 0.22:
        v = (t - (t_out - 0.22)) / 0.22
        dy += 140 * v * v; a *= 1 - v
    return s, rot + extra + idle, dy, a
