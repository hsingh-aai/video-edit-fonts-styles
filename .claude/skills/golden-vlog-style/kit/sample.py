"""Render a Golden Vlog demo still from a drawn stand-in scene (no footage needed).
usage: python sample.py out.jpg [t]
Draws a street with one long table, then adds the marker arrow, a phone sticker, a caption,
the golden film LUT (applied in numpy), halation and grain, so you can check the look quickly."""
import sys, random, os, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import golden_vlog as gv

W, H = gv.W, gv.H


def stand_in_scene():
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):                                              # overcast sky to asphalt
        if y < 760:
            c = int(206 - y * 0.05); d.line([(0, y), (W, y)], fill=(c - 18, c - 6, c + 8))
        else:
            c = int(96 + (y - 760) * 0.03); d.line([(0, y), (W, y)], fill=(c, c, c + 4))
    vp = (420, 760)
    for side, col in ((-1, (196, 176, 150)), (1, (176, 164, 140))):        # house facades
        x0 = 0 if side < 0 else W
        d.polygon([(x0, 120), (vp[0] + side * 60, 640), (vp[0] + side * 60, 760), (x0, 1120)], fill=col)
    rnd = random.Random(4)
    for k in range(14):                                             # trees
        x = rnd.randint(80, 1000); y = rnd.randint(380, 640); r = rnd.randint(60, 150)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(84 + rnd.randint(0, 30), 104 + rnd.randint(0, 30), 60))
    d.polygon([(vp[0] + 30, 770), (vp[0] + 46, 770), (1080, 1500), (900, 1560)], fill=(214, 190, 150))    # the long table
    for k in range(40):                                             # people as soft shapes, no faces
        u = (k / 40) ** 1.6; x = vp[0] + 50 + (980 - vp[0]) * u; y = 780 + 740 * u; s = 8 + 60 * u
        d.ellipse([x - s, y - 2.6 * s, x + s, y], fill=rnd.choice([(150, 60, 50), (60, 70, 90), (200, 180, 120), (90, 110, 80)]))
    return im.filter(ImageFilter.GaussianBlur(1.5))


def apply_cube(im, path):
    lines = [l for l in open(path) if l[:1].isdigit() or l[:1] == '-' or (l[:1] == '0')]
    n = round(len(lines) ** (1 / 3))
    lut = np.array([[float(v) for v in l.split()] for l in lines]).reshape(n, n, n, 3)    # [b][g][r]
    a = np.asarray(im).astype(np.float32) / 255
    idx = np.clip(np.rint(a * (n - 1)).astype(int), 0, n - 1)
    out = lut[idx[..., 2], idx[..., 1], idx[..., 0]]
    return Image.fromarray((out * 255).clip(0, 255).astype(np.uint8))


def finish(im, halation=0.22):
    a = np.asarray(im).astype(np.float32)
    l = a.mean(-1, keepdims=True)
    glow = np.clip((l - 170) * 3, 0, 255) * np.array([1, 0.45, 0.12]) / 255 * 255
    g = np.asarray(Image.fromarray(glow.astype(np.uint8)).filter(ImageFilter.GaussianBlur(22))).astype(np.float32)
    a = 255 - (255 - a) * (255 - g * halation) / 255                   # screen blend
    a += np.random.default_rng(1).normal(0, 6, a.shape[:2])[..., None]  # grain
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def main(out, t=1.2):
    lut = gv.make_lut(os.path.join(tempfile.gettempdir(), 'golden_film.cube'))
    base = finish(apply_cube(stand_in_scene(), lut)).convert('RGBA')
    base.alpha_composite(gv.marker_arrow(gv.bez((1000, 1440), (960, 1010), (680, 850)), t, 3.0, label='it keeps going'))
    base.alpha_composite(gv.place_sticker(gv.phone_sticker('drone: @creator'), (64, 1730), t, 3.0))
    cap, y = gv.caption(['one', 'long', 'table'], 2, 0, 1.0)
    base.alpha_composite(cap, (0, int(y - cap.height / 2)))
    base.convert('RGB').save(out, quality=88)
    print('wrote', out)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'golden_vlog_sample.jpg', float(sys.argv[2]) if len(sys.argv) > 2 else 1.2)
