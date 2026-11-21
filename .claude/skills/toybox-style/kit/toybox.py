"""Toybox kit: the cartoonish pieces of Harnoor's Toybox style (PIL, 1080x1920, RGBA frames).

Pulled out of the first Toybox build (videos/system-design-reel/scripts/build.py, not committed).
Every function returns or draws on PIL RGBA images, so a build script can composite per frame:

    import toybox as tb
    bg = tb.paper_bg()                              # cobalt-blue mottled paper, make once
    fr = tb.split(top_rgb, face_rgb)                # hard 50/50: visual on top, face below
    tb.caption(fr, 'animated diagrams', cy=960)     # lowercase handwritten caption on the seam
    card = tb.card(screenshot_rgb, width=770)       # rounded phone-width card with a soft shadow
    im, xy = tb.zoom_in(card, t0, t, cx, cy)        # pop-in from 82% with a blur that clears
    art = tb.word_art('free', 120)                  # multicolour bubble letters with dot texture
    pill = tb.cta_pill('scale')                     # white pill: handwritten "comment" + blue keyword box

Fonts: fonts/gaegu/Gaegu-Bold.ttf (captions, OFL) and fonts/poppins/Poppins-Black.ttf (word art, keyword).
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = Path(__file__).resolve().parents[4]
W, H, HALF = 1080, 1920, 960
BLUE = (30, 111, 196)            # cobalt paper stage
SITE_CREAM = (244, 235, 224)     # warm cream for drawn UI and placeholder cards
INK = (25, 25, 60)               # bubble-letter outline
ART_COLORS = [(255, 94, 120), (255, 176, 46), (64, 196, 120), (70, 170, 255), (170, 110, 255), (255, 120, 200)]
CAP_FONT = str(REPO / 'fonts/gaegu/Gaegu-Bold.ttf')
ART_FONT = str(REPO / 'fonts/poppins/Poppins-Black.ttf')
CHIP_FONT = str(REPO / 'fonts/poppins/Poppins-SemiBold.ttf')

_fc = {}


def font(path, sz):
    if (path, sz) not in _fc:
        _fc[(path, sz)] = ImageFont.truetype(path, sz)
    return _fc[(path, sz)]


def ease(x):
    x = min(max(x, 0), 1)
    return 1 - (1 - x) ** 3


def tracked(txt, f, track):
    return sum(f.getlength(ch) + track for ch in txt) - track


def paper_bg(color=BLUE, seed=7):
    """cobalt paper: four octaves of soft noise plus grain and a light vignette."""
    rng = np.random.default_rng(seed)
    acc = np.zeros((H, W))
    for sc, amp in [(8, 10), (32, 7), (120, 5), (400, 4)]:
        n = rng.standard_normal((H // sc + 2, W // sc + 2))
        acc += amp * np.array(Image.fromarray(n.astype(np.float32)).resize((W, H), Image.BICUBIC))
    acc += rng.standard_normal((H, W)) * 3
    base = np.array(color, float)[None, None, :] + acc[:, :, None] * np.array([0.6, 0.8, 1.0])
    yy, xx = np.mgrid[0:H, 0:W]
    vig = 1 - 0.12 * (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * 4
    return Image.fromarray(np.clip(base * vig[:, :, None], 0, 255).astype(np.uint8)).convert('RGBA')


_capc = {}


def caption_img(txt, sz=86, track=7):
    """white Gaegu Bold, lowercase, wide tracking, soft dark-navy glow (no box, no highlight)."""
    txt = txt.lower()
    if (txt, sz) in _capc:
        return _capc[(txt, sz)]
    f = font(CAP_FONT, sz)
    lay = Image.new('RGBA', (int(tracked(txt, f, track)) + 60, sz + 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay); x = 30
    for ch in txt:
        d.text((x, 22), ch, font=f, fill='white', stroke_width=1, stroke_fill='white'); x += f.getlength(ch) + track
    glow = Image.new('RGBA', lay.size, (8, 18, 40, 0))
    glow.putalpha(lay.getchannel('A').filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * 0.8)))
    out = Image.new('RGBA', lay.size, (0, 0, 0, 0)); out.alpha_composite(glow); out.alpha_composite(lay)
    _capc[(txt, sz)] = out
    return out


def caption(fr, txt, cy, age=1.0):
    """draws a caption centred at y=cy; `age` is seconds since it appeared (a 0.1 s 90->100% pop)."""
    im = caption_img(txt)
    k = 0.9 + 0.1 * ease(age / 0.1)
    if k < 1:
        im = im.resize((int(im.width * k), int(im.height * k)), Image.BILINEAR)
    fr.alpha_composite(im, (W // 2 - im.width // 2, int(cy - im.height / 2)))
    return fr


def rounded(im, r):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = im.convert('RGBA'); out.putalpha(m); return out


def with_shadow(card, blur=26, off=18, alpha=110):
    pad = blur * 2
    sh = Image.new('RGBA', (card.width + 2 * pad, card.height + 2 * pad + off), (0, 0, 0, 0))
    a = Image.new('L', sh.size, 0); a.paste(card.getchannel('A').point(lambda v: v * alpha // 255), (pad, pad + off))
    sh.putalpha(a.filter(ImageFilter.GaussianBlur(blur)))
    sh.alpha_composite(card, (pad, pad))
    return sh, pad


def card(img, width=770, radius=30, aspect=None):
    """phone-width card (770 px) from a screenshot; aspect crops to w/h around the centre (1.62 for stack cards)."""
    img = img.convert('RGB')
    if aspect:
        h = int(img.width / aspect); y0 = max(0, (img.height - h) // 2)
        img = img.crop((0, y0, img.width, y0 + h))
    img = img.resize((width, int(img.height * width / img.width)), Image.LANCZOS)
    return with_shadow(rounded(img, radius), blur=26 if width > 700 else 20, off=18 if width > 700 else 12)


def zoom_in(card_pad, t0, t, cx, cy, push=0.03, dur=0.28):
    """returns (image, xy): pops in from 82% with a motion blur that clears, then a slow 3% push over 3 s."""
    c, pad = card_pad
    k = ease((t - t0) / dur)
    z = (0.82 + 0.18 * k) * (1 + push * min(max(t - t0, 0) / 3, 1))
    im = c.resize((int(c.width * z), int(c.height * z)), Image.BILINEAR)
    if k < 1:
        im = im.filter(ImageFilter.GaussianBlur(10 * (1 - k)))
        if k < 0.4:
            im.putalpha(im.getchannel('A').point(lambda v: int(v * k / 0.4)))
    return im, (int(cx - im.width / 2), int(cy - im.height / 2))


def word_art(txt, sz=110, track=4):
    """chunky multicolour bubble letters: Poppins Black, one colour per letter, white dot texture,
    a dark-navy outline and a hard drop shadow (the 'cartoon title' of the style)."""
    f = font(ART_FONT, sz)
    lay = Image.new('RGBA', (int(tracked(txt, f, track)) + 60, int(sz * 1.5)), (0, 0, 0, 0))
    x = 30; ci = 0
    for ch in txt:
        if ch == ' ':
            x += f.getlength(ch); continue
        g = Image.new('L', lay.size, 0); ImageDraw.Draw(g).text((x, 10), ch, font=f, fill=255)
        col = Image.new('RGBA', lay.size, ART_COLORS[ci % len(ART_COLORS)] + (255,))
        dots = Image.new('L', lay.size, 0); dd = ImageDraw.Draw(dots)
        for yy in range(0, lay.height, 9):
            for xx in range(int(x), int(x + f.getlength(ch)) + 1, 9):
                dd.ellipse((xx, yy, xx + 4, yy + 4), fill=70)
        col = Image.composite(Image.new('RGBA', lay.size, (255, 255, 255, 255)), col, dots); col.putalpha(g)
        out = Image.new('RGBA', lay.size, (0, 0, 0, 0)); od = ImageDraw.Draw(out)
        od.text((x + 5, 16), ch, font=f, fill=INK + (255,), stroke_width=6, stroke_fill=INK + (255,))
        od.text((x, 10), ch, font=f, fill=INK + (255,), stroke_width=5, stroke_fill=INK + (255,))
        out.alpha_composite(col); lay.alpha_composite(out)
        x += f.getlength(ch) + track; ci += 1
    return lay


def pop(art, t0, t, dur=0.3):
    """word-art entrance: 60% -> 100% with a fade."""
    k = ease((t - t0) / dur)
    if k <= 0:
        return None
    z = 0.6 + 0.4 * k
    im = art.resize((int(art.width * z), int(art.height * z)), Image.BILINEAR)
    im.putalpha(im.getchannel('A').point(lambda v: int(v * min(1, k * 1.5))))
    return im


def chip(txt, sz=22):
    """small credit chip (dark translucent pill)."""
    f = font(CHIP_FONT, sz)
    w = int(f.getlength(txt)) + 30
    im = Image.new('RGBA', (w, sz + 22), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, sz + 21), (sz + 22) // 2, fill=(0, 0, 0, 120))
    d.text((15, (sz + 22) // 2), txt, font=f, fill=(255, 255, 255, 230), anchor='lm')
    return im


def cta_pill(keyword):
    """white pill: handwritten 'comment' + the keyword in white Poppins Black caps on a cobalt box."""
    keyword = keyword.upper()
    f1 = font(CAP_FONT, 70); f2 = font(ART_FONT, 64)
    w1 = tracked('comment', f1, 5); w2 = f2.getlength(keyword)
    w = int(w1 + w2 + 110); h = 112
    im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((20, 28, 20 + w, 28 + h), 56, fill=(0, 0, 0, 90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d.rounded_rectangle((20, 20, 20 + w, 20 + h), 56, fill=(255, 255, 255, 250))
    x = 52
    for ch in 'comment':
        d.text((x, 20 + h // 2 + 4), ch, font=f1, fill=(20, 20, 30), anchor='lm'); x += f1.getlength(ch) + 5
    bx = x + 14
    d.rounded_rectangle((bx, 34, bx + w2 + 36, 20 + h - 14), 26, fill=BLUE)
    d.text((bx + 18, 20 + h // 2 + 2), keyword, font=f2, fill='white', anchor='lm')
    return im


def split(top, face):
    """hard 50/50 frame: `top` and `face` are 1080x960 RGB images (visual above, face below)."""
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    fr.paste(top.convert('RGB').resize((W, HALF)), (0, 0))
    fr.paste(face.convert('RGB').resize((W, HALF)), (0, HALF))
    return fr
