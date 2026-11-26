"""Drawing kit for the IMG_0027 reel (software factories, ep. 1): RPN pixel variant, "factory line" look (copied from
img1858-rpn/scripts/kit.py; only the accent, canvas and seam changed).
  - one accent, conveyor yellow #F5E14A (factory hazard-line yellow; new for the series: not amber, cyan, lilac, red, clay,
    magenta, lime, boot blue, mint or signal orange): marks, numbers, the seam, chips.
  - the seam is a conveyor belt: a 2 px yellow line on rollers with pixel crates riding it to the right (code shipped by
    a factory), a pixel gear at the left
  - canvas: graphite black (#0C0C09), faint 24 px dot grid, low yellow glow, hard 6 px pixel shadows
Type: Pixelify Sans SemiBold caps (no AA), VT323 for numbers and tags (Pixelify's 5 reads as S and its 2 as 8)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{HERE}/..'); REPO = os.path.abspath(f'{R}/../..')
PX, VT = f'{REPO}/fonts/pixelifysans/PixelifySans[wght].ttf', f'{REPO}/fonts/vt323/VT323-Regular.ttf'
W, H, FPS, SEAM = 1080, 1920, 30, 960
INK, GRAPH, BOX, DIM, ACC = (250, 250, 244), (12, 12, 9), (22, 22, 16), (160, 158, 140), (245, 225, 74)
CARD, LINE, DOT = (30, 30, 22), (78, 76, 52), (34, 34, 24)
ZEROS = [14.134725, 21.02204, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073, 48.005151, 49.773832, 52.970321,
         56.446248, 59.347044, 60.831779, 65.112544, 67.079811, 69.546402, 72.067158, 75.704691, 77.14484]
LG = f'{R}/assets/logos'
_fc = {}

ease = lambda x: 1 - (1 - max(0.0, min(1.0, x))) ** 3
clamp = lambda x: max(0.0, min(1.0, x))


def font(size, vt=False, wt='SemiBold'):
    k = (size, vt, wt)
    if k not in _fc:
        f = ImageFont.truetype(VT if vt else PX, size, layout_engine=ImageFont.Layout.BASIC)
        if not vt: f.set_variation_by_name(wt)
        _fc[k] = f
    return _fc[k]


def text_im(s, size, fill=INK, vt=False, track=0, wt='SemiBold', upper=True):
    s = s.upper() if upper else s
    if not vt: assert '5' not in s and '2' not in s, f'Pixelify 5/2 misread: {s}'
    f = font(size, vt, wt); w = sum(f.getlength(c) + track for c in s) - track
    im = Image.new('RGBA', (int(w) + 16, int(size * 1.6) + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'; x = 8
    for c in s:                       # per character: no "fi" ligature, exact tracking
        d.text((x, 8), c, font=f, fill=fill); x += f.getlength(c) + track
    bb = im.getbbox()
    return im.crop(bb) if bb else Image.new('RGBA', (1, 1), (0, 0, 0, 0))


def mixed(s, size, fill=INK, track=2, numcol=ACC):
    """one line: words with digits in VT323 (accent), the rest Pixelify"""
    ims = [text_im(p, int(size * 1.3), numcol, vt=True, track=1) if any(c.isdigit() for c in p) else text_im(p, size, fill, track=track) for p in s.split(' ')]
    sp = int(size * 0.38); w = sum(i.width for i in ims) + sp * (len(ims) - 1); h = max(i.height for i in ims)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); x = 0
    for i in ims: out.alpha_composite(i, (x, (h - i.height) // 2)); x += i.width + sp
    return out


def fade(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * max(0, a)))); return im


def shadow(im, off=6, a=170):
    out = Image.new('RGBA', (im.width + off, im.height + off), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, a)); sh.putalpha(im.getchannel('A').point(lambda v: a if v > 20 else 0))
    out.alpha_composite(sh, (off, off)); out.alpha_composite(im); return out


def smear(im, k):
    if k <= 0.02: return im
    n = max(2, int(10 * k)); out = Image.new('RGBA', (im.width + n * 6, im.height), (0, 0, 0, 0))
    for i in range(n): out.alpha_composite(fade(im, 0.35 * (1 - i / n)), (n * 6 - i * 6, 0))
    out.alpha_composite(im, (n * 6, 0)); return out


def paste_c(fr, im, cx, cy):
    fr.alpha_composite(im, (round(cx - im.width / 2), round(cy - im.height / 2)))


def rounded_mask(size, r):
    m = Image.new('L', size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=255); return m


def floor(h=SEAM):
    fr = Image.new('RGB', (W, h), GRAPH); d = ImageDraw.Draw(fr)
    for x in range(12, W, 24):
        for y in range(12, h, 24): d.point((x, y), fill=DOT)
    g = Image.new('L', (W, h), 0); ImageDraw.Draw(g).ellipse([160, h * 0.12, 920, h * 0.9], fill=40); g = g.filter(ImageFilter.GaussianBlur(170))
    fr.paste(Image.new('RGB', (W, h), (92, 80, 10)), (0, 0), g)
    vg = Image.new('L', (W, h), 255); ImageDraw.Draw(vg).rounded_rectangle([-60, -60, W + 60, h + 60], 300, fill=0); vg = vg.filter(ImageFilter.GaussianBlur(120))
    fr.paste(Image.new('RGB', (W, h), (0, 0, 0)), (0, 0), vg.point(lambda x: x * 0.6))
    return fr.convert('RGBA')


_floors = {}


def base(h=SEAM):
    if h not in _floors: _floors[h] = floor(h)
    return _floors[h].copy()


# SERIES (5 steps): every episode keeps this accent, canvas, seam and type; only EP changes.
EP, N_EP = 1, 5
GEAR = ['..X.X..', '.XXXXX.', 'XXX.XXX', '.XX.XX.', 'XXX.XXX', '.XXXXX.', '..X.X..']


def diff_seam(fr, y=SEAM):
    """the series seam: a conveyor belt. 2 px yellow belt on pixel rollers, pixel crates riding right, a pixel gear at the left"""
    d = ImageDraw.Draw(fr)
    d.rectangle([0, y - 4, W, y - 1], fill=(0, 0, 0, 255)); d.rectangle([0, y - 6, W, y - 5], fill=ACC)
    for r, row in enumerate(GEAR):
        for c, ch in enumerate(row):
            if ch == 'X': d.rectangle([20 + c * 4, y - 36 + r * 4, 23 + c * 4, y - 33 + r * 4], fill=ACC)
    for x in range(64, W, 28):                    # rollers under the belt line
        d.rectangle([x, y - 12, x + 7, y - 9], fill=LINE)
    for k in range(N_EP):                         # series progress: one pip per step, this episode's and earlier ones lit
        x = W - 24 - (N_EP - k) * 26
        if k < EP: d.rectangle([x, y - 34, x + 17, y - 17], fill=ACC)
        else: d.rectangle([x, y - 34, x + 17, y - 17], outline=(120, 118, 96), width=3)
    for k, x in enumerate(range(96, W - 40 - N_EP * 26 - 30, 112)):   # crates riding the belt (one in four lit)
        col = ACC if k % 4 == 1 else (210, 206, 170)
        d.rectangle([x, y - 34, x + 23, y - 15], outline=col, width=4); d.rectangle([x + 10, y - 34, x + 13, y - 15], fill=col)


def tag(fr, s, x=None, y=SEAM - 82, cx=None, size=30):
    """VT323 source tag on a dark chip (real pages, posts and data only)"""
    im = text_im(s, size, INK, vt=True, track=1); bw, bh = im.width + 24, size + 10
    x0 = (cx - bw / 2) if cx is not None else (x if x is not None else 28)
    d = ImageDraw.Draw(fr); d.rectangle([x0, y, x0 + bw, y + bh], fill=(0, 0, 0, 200))
    fr.alpha_composite(im, (round(x0 + 12), round(y + (bh - im.height) / 2)))


def marker(im, rects, k, a=120, dark=False):
    """accent marker wiping across a phrase's line rects in reading order (k 0..1 over the whole phrase)"""
    if k <= 0 or not rects: return
    tot = sum(r[2] - r[0] for r in rects); done = clamp(k) * tot
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for r in rects:
        w = r[2] - r[0]
        if done <= 0: break
        d.rectangle([r[0], r[1], r[0] + min(w, done), r[3]], fill=ACC + (a,)); done -= w
    if dark:
        ul = Image.new('RGBA', im.size, (0, 0, 0, 0)); du = ImageDraw.Draw(ul); done = clamp(k) * tot
        for r in rects:
            w = r[2] - r[0]
            if done <= 0: break
            du.rectangle([r[0], r[1], r[0] + min(w, done), r[3]], fill=ACC + (46,)); du.rectangle([r[0], r[3] - 5, r[0] + min(w, done), r[3]], fill=ACC + (255,)); done -= w
        im.alpha_composite(ul); return
    # multiply, so the ink stays dark under the mark
    base_ = np.asarray(im).astype(np.float32); o = np.asarray(ov).astype(np.float32); al = o[..., 3:4] / 255
    mul = base_[..., :3] * (o[..., :3] / 255)
    base_[..., :3] = base_[..., :3] * (1 - al) + mul * al + base_[..., :3] * al * 0.0
    im.paste(Image.fromarray(base_.clip(0, 255).astype(np.uint8), 'RGBA'))


def page_card(img, maxw=960, maxh=820, r=0):
    s = min(maxw / img.width, maxh / img.height); size = (round(img.width * s), round(img.height * s))
    c = img.resize(size, Image.LANCZOS).convert('RGBA')
    if r: c.putalpha(rounded_mask(size, r))
    return c, s


def logo(name, h=None, maxw=None, white=True):
    """official logo PNG; white=True renders it single-colour white (alpha kept), as the chart rule asks"""
    im = Image.open(f'{LG}/{name}.png').convert('RGBA'); im = im.crop(im.getbbox())
    if white:
        a = im.getchannel('A'); im = Image.new('RGBA', im.size, (255, 255, 255, 0)); im.putalpha(a)
    if h:
        k = h / im.height
        if maxw: k = min(k, maxw / im.width)
        im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    return im


def land(fr, im, cx, cy, t, rise=40, dur=0.27):
    if t < 0: return
    a = ease(t / dur); fr.alpha_composite(fade(im, a), (round(cx - im.width / 2), round(cy - im.height / 2 + (1 - a) * rise)))


def slide_in(fr, im, x, y, t, out_t=None, dist=260):
    """pixel text sliding in from the left with a smear (9 frames)"""
    k = ease(t / 0.3)
    if out_t is not None: k = min(k, 1 - ease((t - out_t) / 0.3))
    if k <= 0: return
    sm = smear(shadow(im), 1 - k); xx = x - (1 - k) * dist
    fr.alpha_composite(fade(sm, min(1, k * 2)), (round(xx - (sm.width - im.width - 6)), round(y)))


def big_num(fr, s, cx, cy, t, size=220, col=ACC, glow=True, sub=None, subcol=DIM):
    if t < 0: return
    a = ease(t / 0.27); im = text_im(s, size, col, vt=True, track=2)
    if glow:
        g = Image.new('RGBA', (im.width + 140, im.height + 140), (0, 0, 0, 0)); g.alpha_composite(im, (70, 70))
        al = g.getchannel('A').filter(ImageFilter.GaussianBlur(26)); gl = Image.new('RGBA', g.size, ACC + (0,)); gl.putalpha(al.point(lambda v: min(255, v * 2)))
        paste_c(fr, fade(gl, a * 0.8), cx, cy - (1 - a) * 16)
    paste_c(fr, fade(im, a), cx, cy - (1 - a) * 16)
    if sub:
        s2 = text_im(sub, 44, subcol, vt=True, track=3); paste_c(fr, fade(s2, a), cx, cy + im.height / 2 + 40 - (1 - a) * 16)


def chip(s, size=40, bg=ACC, fg=GRAPH, vt=False, pad=18):
    im = text_im(s, size, fg, vt=vt, track=2 if not vt else 1)
    out = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2 - 6), bg + (255,)); out.alpha_composite(im, (pad, pad - 3)); return out


def outline_box(fr, x0, y0, x1, y1, col=INK, w=3, fill=None):
    ImageDraw.Draw(fr).rectangle([x0, y0, x1, y1], outline=col, width=w, fill=fill)


def box_caption(s_ims, cy, fr):
    sp = 18; w = sum(i.width for i in s_ims) + sp * (len(s_ims) - 1)
    bw, bh = w + 44, 72; x0, y0 = (W - bw) / 2, cy - bh / 2
    ImageDraw.Draw(fr).rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 12, fill=BOX + (238,))
    x = x0 + 22
    for i in s_ims:
        fr.alpha_composite(i, (round(x), round(cy - i.height / 2))); x += i.width + sp


def robot(size=120, col=INK, eye=ACC):
    """a small pixel robot head (the 'agent' icon), drawn on a 12x12 grid"""
    g = ['....XXXX....', '.....XX.....', '.XXXXXXXXXX.', 'X..........X', 'X..EE..EE..X', 'X..EE..EE..X', 'X..........X',
         'X...XXXX...X', 'X..........X', '.XXXXXXXXXX.', '..X......X..', '..XX....XX..']
    c = size / 12; im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y, row in enumerate(g):
        for x, ch in enumerate(row):
            if ch != '.': d.rectangle([x * c, y * c, (x + 1) * c - 1, (y + 1) * c - 1], fill=eye if ch == 'E' else col)
    return im


def person(size=120, col=INK):
    g = ['....XXXX....', '...XXXXXX...', '...XXXXXX...', '...XXXXXX...', '....XXXX....', '............', '..XXXXXXXX..',
         '.XXXXXXXXXX.', '.XXXXXXXXXX.', '.XXXXXXXXXX.', '.XXXXXXXXXX.', '............']
    c = size / 12; im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y, row in enumerate(g):
        for x, ch in enumerate(row):
            if ch == 'X': d.rectangle([x * c, y * c, (x + 1) * c - 1, (y + 1) * c - 1], fill=col)
    return im


def check(size=48, col=ACC):
    g = ['.......XX', '......XX.', '.....XX..', 'XX..XX...', '.XXXX....', '..XX.....']
    c = size / 9; im = Image.new('RGBA', (size, round(c * 6)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y, row in enumerate(g):
        for x, ch in enumerate(row):
            if ch == 'X': d.rectangle([x * c, y * c, (x + 1) * c - 1, (y + 1) * c - 1], fill=col)
    return im


def callout(src_im, rects, k, maxw=1000, maxscale=1.0, pad=10):
    """magnified callout of a marked phrase: each line segment cut from the full-resolution card, stacked, marked,
    on white with a 3 px accent frame (so the words being read are big enough on a phone)"""
    segs = [src_im.crop((round(r[0] + 2), round(r[1] - pad), round(r[2] - 2), round(r[3] + pad))).convert('RGBA') for r in rects]   # rects already carry 6 px of side padding
    s = min(maxscale, maxw / max(g.width for g in segs)); segs = [g.resize((round(g.width * s), round(g.height * s)), Image.LANCZOS) for g in segs]
    gap = 6; w = max(g.width for g in segs) + 36; h = sum(g.height for g in segs) + gap * (len(segs) - 1) + 36
    out = Image.new('RGBA', (w, h), (255, 255, 255, 255)); y = 18
    tot = sum(g.width for g in segs); done = clamp(k) * tot
    for g in segs:
        g = g.copy(); kk = clamp(done / g.width) if g.width else 0; done -= g.width
        marker(g, [[0, pad * s * 0.4, g.width, g.height - pad * s * 0.2]], kk)
        out.alpha_composite(g, (18, y)); y += g.height + gap
    fr = Image.new('RGBA', (w + 6, h + 6), ACC + (255,)); fr.alpha_composite(out, (3, 3)); return fr
