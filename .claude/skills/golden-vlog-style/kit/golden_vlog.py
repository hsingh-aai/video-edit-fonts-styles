"""Golden Vlog kit: handmade overlays, uneven captions and the golden film grade.
Everything is a pure function of t, so any frame renders on its own. Frames are 1080x1920 RGBA (PIL).

    from golden_vlog import *
    phone_sticker('drone: @handle')                       # IG-style text box, for credits and asides
    marker_arrow(path, t, dur, label='it keeps going')     # white marker arrow that draws on, with handwriting
    cutout_sticker(Image.open('dish_cut.png'), 360)        # real-photo cutout with a white edge (lift.swift makes the cut)
    cutouts_layer([(img, width, cx, cy, tilt, t0), ...], t, dur)
    caption(words, key_index, chunk_index, u)              # -> (RGBA strip, centre y)
    title_card('biggest potluck', 'in', 'SF', t)            # opening title frame, <=4 words, on its own "Title" lane
    make_lut('golden_film.cube')                           # the grade as a 33^3 .cube
    film_finish(lut_path, dusk_t=None)                     # ffmpeg filter: LUT + halation + grain + vignette

Fonts come from this repo's fonts/ folder (Poppins, Instrument Serif, Gaegu) plus macOS Helvetica Neue."""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
REPO = Path(__file__).resolve().parents[4]
FD = REPO / 'fonts'
POP_SB = str(FD / 'poppins/Poppins-SemiBold.ttf')
POP_XB = str(FD / 'poppins/Poppins-ExtraBold.ttf')
SERIF_I = str(FD / 'instrumentserif/InstrumentSerif-Italic.ttf')
HAND = str(FD / 'gaegu/Gaegu-Bold.ttf')
HELV = '/System/Library/Fonts/HelveticaNeue.ttc'          # index 1 = Bold, like the IG "Classic" text box
INK = (20, 18, 16, 255); WHITE = (255, 255, 255, 255); HILITE = (255, 214, 92)
_fc = {}


def font(p, s, index=0):
    k = (p, s, index)
    if k not in _fc: _fc[k] = ImageFont.truetype(p, s, index=index)
    return _fc[k]


def ease_out(u):
    u = min(1, max(0, u)); return 1 - (1 - u) ** 3


def spring(t, hz=2.4, z=0.6):
    if t <= 0: return 0.0
    w = 2 * math.pi * hz
    return 1 - math.exp(-z * w * t) * math.cos(w * math.sqrt(1 - z * z) * t)


def fade_out(t, dur, d=0.2):
    u = min(1, max(0, (t - (dur - d)) / d)); return 1 - u * u * (3 - 2 * u)


def soft_shadow(im, r=8, off=6, a=110):
    sh = Image.new('RGBA', (im.width + 4 * r, im.height + 4 * r), (0, 0, 0, 0))
    m = im.split()[3].point(lambda v: a if v > 8 else 0)
    sh.paste((0, 0, 0, 255), (2 * r, 2 * r + off), m)
    sh = sh.filter(ImageFilter.GaussianBlur(r))
    sh.alpha_composite(im, (2 * r, 2 * r))
    return sh


def with_alpha(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a))); return im


# ---------------- phone text sticker ----------------
def phone_sticker(text, size=46, dark=False):
    """A plain IG-style text box: white (or black) rounded box, Helvetica Neue Bold, left aligned. Use for credits."""
    f = font(HELV, size, 1)
    tw = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textlength(text, font=f)
    h = int(size * 1.65)
    im = Image.new('RGBA', (int(tw + size), h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, h - 1], radius=int(size * 0.3), fill=INK if dark else WHITE)
    d.text((size // 2, h // 2), text, font=f, fill=WHITE if dark else INK, anchor='lm')
    return im


def place_sticker(el, xy, t, dur):
    """fade in over 0.15 s at a fixed spot (no bounce: it should feel typed on a phone)"""
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fr.alpha_composite(with_alpha(soft_shadow(el, 6, 3, 70), ease_out(t / 0.15) * fade_out(t, dur)), xy)
    return fr


# ---------------- marker arrow / circle ----------------
def bez(p0, p1, p2, n=48):
    """quadratic curve, the usual shape for an arrow that points down a street or at a thing"""
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
             (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in (i / n for i in range(n + 1))]


def scribble_circle(cx, cy, rx, ry, seed=1, n=60):
    """a hand-drawn loop that overshoots its start, like a marker circle around a thing"""
    rnd = random.Random(seed); pts = []
    for i in range(n + 8):
        a = -math.pi / 2 + 2 * math.pi * i / n
        j = 1 + rnd.uniform(-0.03, 0.03)
        pts.append((cx + rx * j * math.cos(a), cy + ry * j * math.sin(a)))
    return pts


def marker_arrow(path, t, dur, label=None, label_xy=(60, 1470), label_tilt=7, head=True, width=15, col=(255, 255, 255, 245)):
    """Draw `path` on over 0.45 s, flick an arrow head on, then pop a 1-3 word handwritten label.
    Pass head=False with scribble_circle() for a circle."""
    S = 2
    im = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    prog = ease_out(t / 0.45)
    pts = path[:max(2, int(len(path) * prog))]
    d.line([(x * S, y * S) for x, y in pts], fill=col, width=width * S, joint='curve')
    for x, y in (pts[0], pts[-1]):
        d.ellipse([(x - width / 2) * S, (y - width / 2) * S, (x + width / 2) * S, (y + width / 2) * S], fill=col)
    if head and prog >= 1 and t > 0.45:
        hx, hy = path[-1]; px, py = path[-6]
        ang = math.atan2(hy - py, hx - px); hp = ease_out((t - 0.45) / 0.12)
        for s in (-1, 1):
            a = ang + math.pi - s * 0.55
            ex, ey = hx + math.cos(a) * 58 * hp, hy + math.sin(a) * 58 * hp
            d.line([(hx * S, hy * S), (ex * S, ey * S)], fill=col, width=width * S)
            d.ellipse([(ex - width / 2) * S, (ey - width / 2) * S, (ex + width / 2) * S, (ey + width / 2) * S], fill=col)
    im = im.resize((W, H), Image.LANCZOS)
    if label and t > 0.5:
        f = font(HAND, 92)
        tw = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textlength(label, font=f)
        txt = Image.new('RGBA', (int(tw + 30), 140), (0, 0, 0, 0))
        ImageDraw.Draw(txt).text((10, 70), label, font=f, fill=WHITE, anchor='lm', stroke_width=2, stroke_fill=(0, 0, 0, 60))
        s = min(1.0, 0.9 + 0.1 * spring(t - 0.5)); a = ease_out((t - 0.5) / 0.12)
        txt = txt.resize((int(txt.width * s), int(txt.height * s)), Image.LANCZOS).rotate(label_tilt, resample=Image.BICUBIC, expand=True)
        im.alpha_composite(with_alpha(soft_shadow(txt, 6, 3, 90), a), label_xy)
    return with_alpha(im, fade_out(t, dur))


# ---------------- real-photo cutouts ----------------
_cuts = {}


def cutout_sticker(img, width, edge=9):
    """img: RGBA subject (from lift.swift). Returns it scaled to `width` with an IG-style white cut edge and a shadow."""
    k = (id(img), width)
    if k in _cuts: return _cuts[k]
    im = img.convert('RGBA'); im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    pad = edge + 5
    big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.paste(im, (pad, pad), im)
    a = big.split()[3].point(lambda v: 255 if v > 90 else 0)
    rim = a.filter(ImageFilter.MaxFilter(2 * edge + 1)).filter(ImageFilter.GaussianBlur(1.2))
    out = Image.new('RGBA', big.size, (255, 255, 255, 0)); out.putalpha(rim)
    out = Image.composite(Image.new('RGBA', big.size, WHITE), out, rim)
    out.alpha_composite(big)
    _cuts[k] = soft_shadow(out, 10, 8, 120)
    return _cuts[k]


def cutouts_layer(items, t, dur):
    """items: [(rgba, width, cx, cy, tilt, t0)] - each lands on its spoken item with a soft spring and a slow sway"""
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for img, wd, cx, cy, tilt, t0 in items:
        tk = t - t0
        if tk <= 0: continue
        s = 0.55 + 0.45 * spring(tk, 3.0, 0.5)
        el = cutout_sticker(img, wd)
        el = el.resize((max(1, int(el.width * s)), max(1, int(el.height * s))), Image.BICUBIC)
        el = el.rotate(tilt + 1.2 * math.sin(2 * math.pi * 0.7 * tk + t0), resample=Image.BICUBIC, expand=True)
        fr.alpha_composite(el, (int(cx - el.width / 2), int(cy - el.height / 2)))
    return with_alpha(fr, fade_out(t, dur))


# ---------------- captions ----------------
def caption(words, key, idx, u, y=215):
    """Small lowercase captions that don't look templated.
    words: list; key: index of the punch word or None; idx: chunk number (seeds the variation); u: 0..1 pop progress.
    The emphasis rotates per beat: a marker swipe behind the word, a big serif italic word, or plain bold.
    Placement wanders by up to 60 px and 2 degrees. Returns (RGBA strip, centre y)."""
    rnd = random.Random(idx * 7 + 3)
    style = ('hilite', 'serif', 'plain', 'hilite', 'serif')[idx % 5] if key is not None else 'plain'
    f = font(POP_SB, 54)
    fk = {'hilite': font(POP_XB, 56), 'serif': font(SERIF_I, 80), 'plain': font(POP_XB, 58)}[style]
    d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    gap = d0.textlength(' ', font=f)
    ws = [d0.textlength(w, font=fk if i == key else f) for i, w in enumerate(words)]
    total = sum(ws) + gap * (len(words) - 1)
    img = Image.new('RGBA', (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    x = (W - total) / 2 + rnd.uniform(-60, 60); base = 112
    for i, w in enumerate(words):
        ff = fk if i == key else f
        if i == key and style == 'hilite':
            wipe = ease_out(u * 1.4)
            d.rounded_rectangle([x - 8, base - 34, x - 8 + (ws[i] + 16) * wipe, base + 22], radius=6, fill=HILITE + (235,))
            d.text((x, base), w, font=ff, fill=INK, anchor='ls')
        else:
            d.text((x, base), w, font=ff, fill=WHITE, anchor='ls', stroke_width=2, stroke_fill=(0, 0, 0, 70))
        x += ws[i] + gap
    img = soft_shadow(img, 5, 2, 120).rotate(rnd.uniform(-2.2, 2.2), resample=Image.BICUBIC)
    a = min(1, u * 2)
    return with_alpha(img, a), y + rnd.randint(-14, 14)


# ---------------- opening title ----------------
def title_card(line1, small, punch, t, dur=3.0, cy=1350, tilt=-3):
    """Opening title frame (full 1080x1920 RGBA): line1 in ExtraBold, then a serif-italic `small` word and the
    `punch` word on a yellow marker swipe. Keep it to 4 words in all and off the face (cy=1350 = chest band on a selfie)."""
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if t >= dur: return fr
    f1, fi, fs = font(POP_XB, 104), font(SERIF_I, 118), font(POP_XB, 112)
    strip = Image.new('RGBA', (W, 320), (0, 0, 0, 0)); d = ImageDraw.Draw(strip)
    w1 = d.textlength(line1, font=f1)
    d.text(((W - w1) / 2, 120), line1, font=f1, fill=WHITE, anchor='ls', stroke_width=2, stroke_fill=(0, 0, 0, 70))
    wi = d.textlength(small, font=fi) if small else 0
    ws, gap = d.textlength(punch, font=fs), (26 if small else 0)
    x = (W - (wi + gap + ws)) / 2 + 40
    if small:
        d.text((x, 262), small, font=fi, fill=WHITE, anchor='ls', stroke_width=2, stroke_fill=(0, 0, 0, 70))
    sx = x + wi + gap
    wipe = ease_out((t - 0.35) / 0.3)
    if wipe > 0:
        d.rounded_rectangle([sx - 14, 180, sx - 14 + (ws + 28) * wipe, 280], radius=10, fill=HILITE + (240,))
    d.text((sx, 262), punch, font=fs, fill=INK if wipe > 0.6 else WHITE, anchor='ls')
    strip = soft_shadow(strip, 7, 3, 130).rotate(tilt, resample=Image.BICUBIC)
    s = 0.88 + 0.12 * spring(t - 0.05, 2.6, 0.55)
    a = ease_out(t / 0.12) * fade_out(t, dur, 0.25)
    strip = strip.resize((int(strip.width * s), int(strip.height * s)), Image.LANCZOS)
    fr.alpha_composite(with_alpha(strip, a), (int((W - strip.width) / 2), int(cy - strip.height / 2)))
    return fr


# ---------------- grade ----------------
def make_lut(path, title='Golden Film', n=33):
    """Golden-hour film: gold in the highlights, a little teal in deep shadows, opened mids, film S-curve,
    faded blacks and rolled-off whites, +12% saturation. Tuned on overcast SF daylight; re-check skin on new light."""
    import numpy as np
    g = np.linspace(0, 1, n)
    b, gg, r = np.meshgrid(g, g, g, indexing='ij')
    x = np.stack([r, gg, b], -1).reshape(-1, 3)
    l0 = (x * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
    x = x + (0.055 * l0 ** 1.2) * np.array([1.0, 0.45, -0.75])
    x = x + (0.03 * (1 - l0) ** 3) * np.array([-0.35, 0.15, 0.45])
    x = np.clip(x, 0, 1) ** 0.94
    s2 = x * x * (3 - 2 * x); x = 0.74 * x + 0.26 * s2
    x = 0.035 + x * (0.955 - 0.035)
    l = (x * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
    x = np.clip(l + (x - l) * 1.12, 0, 1)
    with open(path, 'w') as f:
        f.write(f'TITLE "{title}"\nLUT_3D_SIZE {n}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for v in x: f.write(f'{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n')
    return path


def film_finish(lut, dusk_t=None, src='0:v', out='g'):
    """ffmpeg filter_complex chain for the preview: LUT, orange halation on highlights (a second, wider glow from
    dusk_t on, so evening lights bloom), grain and a soft vignette. FCP only gets the LUT (on the GRADE layer)."""
    dusk = f"gte(t,{dusk_t:.3f})" if dusk_t is not None else '0'
    return ';'.join([
        f"[{src}]lut3d='{lut}',split=3[g0][h0][h1]",
        "[h0]lutyuv=y='clip((val-170)*3,0,255)':u=128:v=128,gblur=sigma=22,colorchannelmixer=rr=1:gg=0.45:bb=0.12[hl]",
        "[h1]lutyuv=y='clip((val-120)*2.2,0,255)':u=128:v=128,gblur=sigma=34,colorchannelmixer=rr=1:gg=0.62:bb=0.22[hd]",
        "[g0][hl]blend=all_mode=screen:all_opacity=0.22[g1]",
        f"[g1][hd]blend=all_mode=screen:all_opacity=0.42:enable='{dusk}'[g2]",
        f"[g2]vignette=angle=PI/5.5,noise=c0s=9:c0f=t+u:c1s=3:c2s=3,format=yuv420p[{out}]",
    ])
